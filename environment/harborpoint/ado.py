"""Thin Azure DevOps Services REST client used by the HarborPoint provisioner.

Design
------
* Every call is described by a :class:`Req` built by a pure function on :class:`Api`
  (URL, query parameters, headers, JSON body). Builders never touch the network, so the
  dry-run planner and the unit tests can inspect exactly what would be sent.
* :class:`AdoClient` sends a ``Req`` through a pluggable *transport* (``requests`` by
  default). It adds Basic auth (empty user name, PAT as password), paces calls
  (default <= 8 requests/second, strictly sequential), retries 429/5xx with exponential
  backoff honouring ``Retry-After``, and raises :class:`AdoError` with the HTTP status,
  the Azure DevOps ``typeKey``/message, the request (never the PAT) and a human hint.

PAT scopes required (organization-scoped PAT; owner must be a Project Collection Administrator)
----------------------------------------------------------------------------------------------
See :data:`PAT_SCOPES` (also printed by ``python -m harborpoint.provision --help``).
"""
from __future__ import annotations

import base64
import json
import random
import re
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Mapping
from urllib.parse import quote, urlencode, urlparse

# --------------------------------------------------------------------------- constants

API = "7.1"                      # GA version for core, wit, work, wiki, security
API_DASHBOARD = "7.1-preview.3"  # dashboards
API_WIDGET = "7.1-preview.2"     # widgets
API_GRAPH = "7.1-preview.1"      # graph (vssps)
API_ENTITLEMENT = "7.1-preview.3"  # user entitlements (vsaex)

AGILE_PROCESS_TYPE_ID = "adcc42ab-9882-485e-a3ed-7678f01f66bc"
QUERY_FOLDER_NAMESPACE = "71356614-aad7-4757-8f2c-0fb3bff6f680"  # WorkItemQueryFolders

PAT_SCOPES = """\
PAT scopes (create an ORGANIZATION-scoped PAT, "Custom defined"; the PAT owner must be a
Project Collection Administrator because bypassRules and project creation need it):
  Project and Team ....... Read, write, & manage   (vso.project_manage)   project, teams
  Work Items ............. Read & write            (vso.work_write)       nodes, team settings,
                                                                          work items, queries, plans
  Wiki ................... Read & write            (vso.wiki_write)       project wiki pages
  Team Dashboard ......... Read & manage           (vso.dashboards_manage) dashboards + widgets
  Security ............... Manage                  (vso.security_manage)  query-folder permissions
  Graph .................. Read                    (vso.graph)            group/user descriptors
  Identity ............... Read                    (vso.identity)         ACE identity descriptors
  Analytics .............. Read                    (vso.analytics)        pilot OData checks (optional)
  Member Entitlement Mgmt  Read & write            (vso.memberentitlementmanagement_write)
                                                    only for --participant-map (adds users)
  Graph .................. Read & manage           (vso.graph_manage)     only for --participant-map
                                                    (team membership)"""

# Azure DevOps error codes -> friendly hints.
ERROR_HINTS: dict[str, str] = {
    "VS402625": "Revision dates must increase: every System.ChangedDate must be strictly later than the "
                "item's previous revision (including revisions created server-side, e.g. by adding a link). "
                "If this happened while creating a CHILD with a parent link, the parent probably received a "
                "link revision; re-run the pilot and use the --order / --parent-links mode it recommends.",
    "VS403417": "ChangedBy cannot be empty when bypassRules is specified. Re-run with --changed-by "
                "'<display name>' so System.ChangedBy is set explicitly on each revision.",
    "TF401256": "Missing Write permission on a query folder. The PAT owner must be a Project Administrator "
                "(or have Contribute on the Shared Queries folder).",
    "TF400733": "Rate limited (TSTU budget exhausted). The client backs off automatically; if this persists, "
                "lower --max-rps and retry later.",
    "TF400813": "The PAT owner is not authorized for this resource (check PAT scopes and organization).",
    "TF200016": "Project not found. Run the 'project' step first or check --project.",
    "TF237124": "Work item type not found in this process; the project must use the Agile process.",
    "VS403437": "Possibly an invalid identity or field value; check --assign-map entries.",
    "TF51535": "Field not found on this work item type (fields must exist; bypassRules does not add fields).",
    "VS402323": "Too many items / request too large; split the request.",
    "VS402337": "WIQL result exceeds 20,000 items; narrow the query.",
}

STATUS_HINTS: dict[int, str] = {
    401: "Unauthorized: the PAT is missing, expired, revoked, or for another organization.",
    403: "Forbidden: the PAT lacks a scope (see --help) or the owner lacks the permission "
         "(Project Collection Administrator; 'Bypass rules on work item updates'; "
         "'Suppress notifications for work item updates').",
    404: "Not found: check the org URL, project name, team name or resource path.",
    409: "Conflict: the resource already exists or was changed concurrently (stale ETag).",
    412: "Precondition failed: stale ETag/If-Match (re-read the resource and retry).",
}


# --------------------------------------------------------------------------- data types

@dataclass
class Req:
    """A fully described REST request (no secrets inside)."""
    method: str
    url: str                                   # absolute URL without query string
    params: dict[str, str] = field(default_factory=dict)
    body: Any = None                           # JSON-serialisable or str (sent as-is)
    headers: dict[str, str] = field(default_factory=dict)
    label: str = ""                            # short plan label, e.g. "workitems.create"
    unsafe: bool = False                       # non-idempotent write: retry only 429 (never 5xx/network)

    @property
    def content_type(self) -> str:
        return self.headers.get("Content-Type", "application/json")

    def full_url(self) -> str:
        return self.url + ("?" + urlencode(self.params, quote_via=quote, safe="$/@") if self.params else "")

    def describe(self) -> str:
        return f"{self.method} {self.full_url()}"


@dataclass
class Resp:
    status: int
    headers: Mapping[str, str]
    data: Any                                  # parsed JSON or text or None

    def header(self, name: str) -> str | None:
        for k, v in self.headers.items():
            if k.lower() == name.lower():
                return v
        return None


class AdoError(RuntimeError):
    """An Azure DevOps REST failure with enough context to act on."""

    def __init__(self, status: int, req: Req, message: str = "", type_key: str = "", body: Any = None):
        self.status = status
        self.req = req
        self.message = message
        self.type_key = type_key
        self.body = body
        self.code = _error_code(message)
        self.hint = hint_for(status, message, type_key)
        text = f"HTTP {status} on {req.describe()}"
        if type_key:
            text += f" [{type_key}]"
        if message:
            text += f": {message}"
        if self.hint:
            text += f"\n  Hint: {self.hint}"
        super().__init__(text)


def _error_code(message: str) -> str:
    m = re.search(r"\b((?:VS|TF)\d{5,6})\b", message or "")
    return m.group(1) if m else ""


def hint_for(status: int, message: str = "", type_key: str = "") -> str:
    code = _error_code(message)
    if code in ERROR_HINTS:
        return ERROR_HINTS[code]
    if "bypass" in (message or "").lower() and status in (400, 403):
        return ("The caller lacks 'Bypass rules on work item updates'. Use a PAT owned by a Project "
                "Collection Administrator.")
    if type_key == "ProjectAlreadyExistsException":
        return "A project with this name already exists (the provisioner will reuse it)."
    return STATUS_HINTS.get(status, "")


# --------------------------------------------------------------------------- transport

Transport = Callable[[str, str, Mapping[str, str], bytes | None, float], tuple[int, Mapping[str, str], bytes]]


def requests_transport() -> Transport:
    """Default transport built on a single ``requests.Session`` (imported lazily)."""
    import requests  # noqa: WPS433 (lazy: dry-run and tests never need it)

    session = requests.Session()

    def send(method: str, url: str, headers: Mapping[str, str], data: bytes | None, timeout: float):
        r = session.request(method, url, headers=dict(headers), data=data, timeout=timeout)
        return r.status_code, r.headers, r.content

    return send


# --------------------------------------------------------------------------- client

class AdoClient:
    """Sequential, paced, retrying REST client."""

    RETRY_STATUSES = (429, 500, 502, 503, 504)

    def __init__(self, pat: str, transport: Transport | None = None, *, max_rps: float = 8.0,
                 max_retries: int = 6, timeout: float = 60.0, sleep: Callable[[float], None] = time.sleep,
                 clock: Callable[[], float] = time.monotonic, log: Callable[[str], None] = print,
                 user_agent: str = "harborpoint-provisioner/1.0"):
        if not pat:
            raise ValueError("A PAT is required for live calls")
        self._auth = "Basic " + base64.b64encode((":" + pat).encode()).decode()
        self._transport = transport or requests_transport()
        self._min_interval = 1.0 / max_rps if max_rps > 0 else 0.0
        self._max_retries = max_retries
        self._timeout = timeout
        self._sleep = sleep
        self._clock = clock
        self._log = log
        self._last = -1e9
        self._ua = user_agent
        self.count = 0

    def send(self, req: Req, *, allow: Iterable[int] = ()) -> Resp:
        """Send ``req``. 2xx and statuses in ``allow`` return a :class:`Resp`; others raise."""
        allow = set(allow)
        headers = {"Accept": "application/json", "User-Agent": self._ua, **req.headers,
                   "Authorization": self._auth}
        data: bytes | None = None
        if req.body is not None:
            data = req.body.encode() if isinstance(req.body, str) else json.dumps(req.body).encode()
            headers.setdefault("Content-Type", "application/json")
        url = req.full_url()
        attempt = 0
        while True:
            self._pace()
            self.count += 1
            try:
                status, rh, raw = self._transport(req.method, url, headers, data, self._timeout)
            except Exception as exc:  # network error: retry like a 503 (unless the write is unsafe)
                if attempt >= self._max_retries or req.unsafe:
                    raise AdoError(0, req, f"network error: {exc}") from exc
                delay = self._backoff(attempt, None)
                self._log(f"  network error ({exc.__class__.__name__}); retrying in {delay:.1f}s")
                self._sleep(delay)
                attempt += 1
                continue
            parsed = _parse(raw, rh)
            if 200 <= status < 300 or status in allow:
                self._respect_rate_headers(rh)
                return Resp(status, rh, parsed)
            retryable = status == 429 or (status in self.RETRY_STATUSES and not req.unsafe)
            if retryable and attempt < self._max_retries:
                delay = self._backoff(attempt, _header(rh, "Retry-After"))
                self._log(f"  HTTP {status} on {req.method} {req.url.split('/_apis/')[-1][:60]}; "
                          f"retry {attempt + 1}/{self._max_retries} in {delay:.1f}s")
                self._sleep(delay)
                attempt += 1
                continue
            message, type_key = _error_fields(parsed)
            raise AdoError(status, req, message, type_key, parsed)

    # -- internals
    def _pace(self) -> None:
        now = self._clock()
        wait = self._min_interval - (now - self._last)
        if wait > 0:
            self._sleep(wait)
        self._last = self._clock()

    @staticmethod
    def _backoff(attempt: int, retry_after: str | None) -> float:
        if retry_after:
            try:
                return max(1.0, float(retry_after))
            except ValueError:
                pass
        return min(60.0, 2.0 ** attempt) + random.Random(attempt).uniform(0, 0.5)

    def _respect_rate_headers(self, headers: Mapping[str, str]) -> None:
        """Slow down when Azure DevOps signals throttling (X-RateLimit-Delay / Remaining)."""
        delay = _header(headers, "X-RateLimit-Delay")
        remaining = _header(headers, "X-RateLimit-Remaining")
        try:
            if delay and float(delay) > 0:
                self._sleep(min(30.0, float(delay)))
            elif remaining is not None and float(remaining) < 10:
                self._sleep(2.0)
        except ValueError:
            pass


def _header(headers: Mapping[str, str], name: str) -> str | None:
    for k, v in headers.items():
        if k.lower() == name.lower():
            return v
    return None


def _parse(raw: bytes, headers: Mapping[str, str]) -> Any:
    if not raw:
        return None
    text = raw.decode("utf-8", "replace")
    ctype = (_header(headers, "Content-Type") or "").lower()
    if "json" in ctype or text[:1] in "{[":
        try:
            return json.loads(text)
        except ValueError:
            return text
    return text


def _error_fields(parsed: Any) -> tuple[str, str]:
    if isinstance(parsed, dict):
        return str(parsed.get("message") or parsed.get("Message") or ""), str(parsed.get("typeKey") or "")
    if isinstance(parsed, str):
        # HTML error pages: keep the first line only
        return parsed.strip().splitlines()[0][:300] if parsed.strip() else "", ""
    return "", ""


# --------------------------------------------------------------------------- URL helpers

def seg(text: str) -> str:
    """URL-encode one path segment (spaces -> %20, '/' encoded)."""
    return quote(str(text), safe="")


def seg_path(path: str, sep: str = "\\") -> str:
    """Encode a multi-level path (e.g. ``PI 4\\Sprint 13``) as ``PI%204/Sprint%2013``."""
    return "/".join(seg(p) for p in str(path).split(sep) if p)


def org_hosts(org_url: str) -> tuple[str, str, str]:
    """Return (core, vssps, vsaex) base URLs for an org URL.

    Supports https://dev.azure.com/{org} and legacy https://{org}.visualstudio.com.
    """
    org_url = org_url.rstrip("/")
    u = urlparse(org_url)
    if u.scheme != "https" or not u.netloc:
        raise ValueError(f"--org must be an https URL like https://dev.azure.com/ORG (got {org_url!r})")
    if u.netloc.lower() == "dev.azure.com":
        name = u.path.strip("/").split("/")[0]
        if not name:
            raise ValueError("--org must include the organization name: https://dev.azure.com/ORG")
        return (f"https://dev.azure.com/{name}", f"https://vssps.dev.azure.com/{name}",
                f"https://vsaex.dev.azure.com/{name}")
    if u.netloc.lower().endswith(".visualstudio.com"):
        name = u.netloc.split(".")[0]
        return (f"https://{name}.visualstudio.com", f"https://{name}.vssps.visualstudio.com",
                f"https://{name}.vsaex.visualstudio.com")
    raise ValueError(f"Unrecognised Azure DevOps org URL: {org_url}")


# --------------------------------------------------------------------------- endpoint builders

class Api:
    """Pure request builders. ``project`` and ``team`` may be names or GUIDs."""

    def __init__(self, org_url: str):
        self.org, self.vssps, self.vsaex = org_hosts(org_url)

    # ---- core / preflight
    def connection_data(self) -> Req:
        return Req("GET", f"{self.org}/_apis/connectionData", label="preflight.connectionData")

    def processes(self) -> Req:
        return Req("GET", f"{self.org}/_apis/process/processes", {"api-version": API}, label="preflight.processes")

    def get_project(self, name_or_id: str) -> Req:
        return Req("GET", f"{self.org}/_apis/projects/{seg(name_or_id)}",
                   {"includeCapabilities": "true", "api-version": API}, label="project.get")

    def create_project(self, name: str, description: str, process_type_id: str) -> Req:
        body = {"name": name, "description": description, "visibility": "private",
                "capabilities": {"versioncontrol": {"sourceControlType": "Git"},
                                 "processTemplate": {"templateTypeId": process_type_id}}}
        return Req("POST", f"{self.org}/_apis/projects", {"api-version": API}, body, label="project.create")

    def get_operation(self, op_id: str) -> Req:
        return Req("GET", f"{self.org}/_apis/operations/{seg(op_id)}", {"api-version": API}, label="project.poll")

    # ---- classification nodes
    def get_nodes(self, project: str, group: str) -> Req:
        assert group in ("Areas", "Iterations")
        return Req("GET", f"{self.org}/{seg(project)}/_apis/wit/classificationnodes/{group}",
                   {"$depth": "14", "api-version": API}, label=f"classification.get{group}")

    def create_node(self, project: str, group: str, parent_rel: str, name: str,
                    start: str | None = None, finish: str | None = None) -> Req:
        url = f"{self.org}/{seg(project)}/_apis/wit/classificationnodes/{group}"
        if parent_rel:
            url += "/" + seg_path(parent_rel)
        body: dict[str, Any] = {"name": name}
        if start and finish:
            body["attributes"] = {"startDate": iso_midnight(start), "finishDate": iso_midnight(finish)}
        return Req("POST", url, {"api-version": API}, body, label=f"classification.create{group[:-1]}")

    def update_iteration_dates(self, project: str, rel_path: str, start: str, finish: str) -> Req:
        url = f"{self.org}/{seg(project)}/_apis/wit/classificationnodes/Iterations/{seg_path(rel_path)}"
        body = {"attributes": {"startDate": iso_midnight(start), "finishDate": iso_midnight(finish)}}
        return Req("PATCH", url, {"api-version": API}, body, label="classification.updateIterationDates")

    # ---- teams
    def list_teams(self, project_id: str) -> Req:
        return Req("GET", f"{self.org}/_apis/projects/{seg(project_id)}/teams",
                   {"$top": "500", "api-version": API}, label="teams.list")

    def create_team(self, project_id: str, name: str, description: str) -> Req:
        return Req("POST", f"{self.org}/_apis/projects/{seg(project_id)}/teams", {"api-version": API},
                   {"name": name, "description": description}, label="teams.create")

    def _team_base(self, project: str, team: str) -> str:
        return f"{self.org}/{seg(project)}/{seg(team)}/_apis/work/teamsettings"

    def set_team_field_values(self, project: str, team: str, default_area: str,
                              values: list[tuple[str, bool]]) -> Req:
        body = {"defaultValue": default_area,
                "values": [{"value": v, "includeChildren": inc} for v, inc in values]}
        return Req("PATCH", self._team_base(project, team) + "/teamfieldvalues", {"api-version": API}, body,
                   label="teams.areas")

    def get_team_field_values(self, project: str, team: str) -> Req:
        return Req("GET", self._team_base(project, team) + "/teamfieldvalues", {"api-version": API},
                   label="teams.getAreas")

    def list_team_iterations(self, project: str, team: str) -> Req:
        return Req("GET", self._team_base(project, team) + "/iterations", {"api-version": API},
                   label="teams.listIterations")

    def add_team_iteration(self, project: str, team: str, iteration_guid: str) -> Req:
        return Req("POST", self._team_base(project, team) + "/iterations", {"api-version": API},
                   {"id": iteration_guid}, label="teams.addIteration")

    def update_team_settings(self, project: str, team: str, body: dict) -> Req:
        return Req("PATCH", self._team_base(project, team), {"api-version": API}, body, label="teams.settings")

    def set_team_days_off(self, project: str, team: str, iteration_guid: str,
                          ranges: list[tuple[str, str]]) -> Req:
        body = {"daysOff": [{"start": iso_midnight(s), "end": iso_midnight(e)} for s, e in ranges]}
        return Req("PATCH", self._team_base(project, team) + f"/iterations/{seg(iteration_guid)}/teamdaysoff",
                   {"api-version": API}, body, label="teams.daysOff")

    # ---- work items
    def _wi_params(self, bypass: bool = True, suppress: bool = True, validate_only: bool = False) -> dict:
        p: dict[str, str] = {}
        if validate_only:
            p["validateOnly"] = "true"
        if bypass:
            p["bypassRules"] = "true"
        if suppress:
            p["suppressNotifications"] = "true"
        p["api-version"] = API
        return p

    def create_work_item(self, project: str, wit: str, patch: list[dict], *, bypass: bool = True,
                         suppress: bool = True) -> Req:
        return Req("POST", f"{self.org}/{seg(project)}/_apis/wit/workitems/${seg(wit)}",
                   self._wi_params(bypass, suppress), patch,
                   {"Content-Type": "application/json-patch+json"}, label="workitems.create", unsafe=True)

    def update_work_item(self, project: str, wi_id: int, patch: list[dict], *, bypass: bool = True,
                         suppress: bool = True, validate_only: bool = False, label: str = "workitems.update") -> Req:
        return Req("PATCH", f"{self.org}/{seg(project)}/_apis/wit/workitems/{int(wi_id)}",
                   self._wi_params(bypass, suppress, validate_only), patch,
                   {"Content-Type": "application/json-patch+json"}, label=label, unsafe=not validate_only)

    def get_work_item(self, project: str, wi_id: int, fields: list[str] | None = None,
                      expand: str | None = None) -> Req:
        params = {"api-version": API}
        if fields:
            params["fields"] = ",".join(fields)
        if expand:
            params["$expand"] = expand
        return Req("GET", f"{self.org}/{seg(project)}/_apis/wit/workitems/{int(wi_id)}", params,
                   label="workitems.get")

    def get_revisions(self, project: str, wi_id: int) -> Req:
        return Req("GET", f"{self.org}/{seg(project)}/_apis/wit/workitems/{int(wi_id)}/revisions",
                   {"$expand": "relations", "api-version": API}, label="workitems.revisions")

    def delete_work_item(self, project: str, wi_id: int, destroy: bool = False) -> Req:
        params = {"api-version": API}
        if destroy:
            params["destroy"] = "true"
        return Req("DELETE", f"{self.org}/{seg(project)}/_apis/wit/workitems/{int(wi_id)}", params,
                   label="workitems.delete")

    def wiql(self, project: str, query: str, top: int | None = None, time_precision: bool = False) -> Req:
        params = {"api-version": API}
        if top:
            params["$top"] = str(top)
        if time_precision:
            params["timePrecision"] = "true"
        return Req("POST", f"{self.org}/{seg(project)}/_apis/wit/wiql", params, {"query": query}, label="wiql")

    def work_item_url(self, wi_id: int) -> str:
        """Canonical work item URL used in relations."""
        return f"{self.org}/_apis/wit/workItems/{int(wi_id)}"

    def wit_states(self, project: str, wit: str) -> Req:
        return Req("GET", f"{self.org}/{seg(project)}/_apis/wit/workitemtypes/{seg(wit)}/states",
                   {"api-version": API}, label="pilot.states")

    # ---- queries
    def get_query(self, project: str, path: str, depth: int = 0) -> Req:
        params = {"api-version": API}
        if depth:
            params["$depth"] = str(depth)
        return Req("GET", f"{self.org}/{seg(project)}/_apis/wit/queries/{seg_path(path, '/')}", params,
                   label="queries.get")

    def create_query_item(self, project: str, parent_path: str, name: str, wiql: str | None = None) -> Req:
        body: dict[str, Any] = {"name": name}
        if wiql is None:
            body["isFolder"] = True
        else:
            body["wiql"] = wiql
        return Req("POST", f"{self.org}/{seg(project)}/_apis/wit/queries/{seg_path(parent_path, '/')}",
                   {"api-version": API}, body, label="queries.createFolder" if wiql is None else "queries.create")

    def update_query(self, project: str, query_id: str, wiql: str) -> Req:
        return Req("PATCH", f"{self.org}/{seg(project)}/_apis/wit/queries/{seg(query_id)}",
                   {"api-version": API}, {"wiql": wiql}, label="queries.update")

    # ---- security / graph / identities
    def security_namespace(self, ns: str) -> Req:
        return Req("GET", f"{self.org}/_apis/securitynamespaces/{seg(ns)}", {"api-version": API},
                   label="security.namespace")

    def list_acls(self, ns: str, token: str, recurse: bool = True) -> Req:
        return Req("GET", f"{self.org}/_apis/accesscontrollists/{seg(ns)}",
                   {"token": token, "recurse": "true" if recurse else "false", "api-version": API},
                   label="security.acls")

    def set_aces(self, ns: str, token: str, descriptor: str, allow: int, deny: int = 0) -> Req:
        body = {"token": token, "merge": True,
                "accessControlEntries": [{"descriptor": descriptor, "allow": allow, "deny": deny,
                                          "extendedInfo": {}}]}
        return Req("POST", f"{self.org}/_apis/accesscontrolentries/{seg(ns)}", {"api-version": API}, body,
                   label="security.setAces")

    def graph_descriptor(self, storage_key: str) -> Req:
        return Req("GET", f"{self.vssps}/_apis/graph/descriptors/{seg(storage_key)}", {"api-version": API_GRAPH},
                   label="graph.descriptor")

    def graph_groups(self, scope_descriptor: str) -> Req:
        return Req("GET", f"{self.vssps}/_apis/graph/groups",
                   {"scopeDescriptor": scope_descriptor, "api-version": API_GRAPH}, label="graph.groups")

    def identities_by_subject(self, subject_descriptor: str) -> Req:
        return Req("GET", f"{self.vssps}/_apis/identities",
                   {"subjectDescriptors": subject_descriptor, "queryMembership": "None", "api-version": API},
                   label="identities.read")

    def add_membership(self, subject_descriptor: str, container_descriptor: str) -> Req:
        return Req("PUT", f"{self.vssps}/_apis/graph/memberships/{seg(subject_descriptor)}/"
                          f"{seg(container_descriptor)}", {"api-version": API_GRAPH}, label="graph.addMembership")

    def add_user_entitlement(self, email: str, project_id: str) -> Req:
        body = {"accessLevel": {"accountLicenseType": "express", "licensingSource": "account"},
                "user": {"principalName": email, "subjectKind": "user"},
                "projectEntitlements": [{"group": {"groupType": "projectContributor"},
                                         "projectRef": {"id": project_id}}]}
        return Req("POST", f"{self.vsaex}/_apis/userentitlements", {"api-version": API_ENTITLEMENT}, body,
                   label="participants.entitlement")

    # ---- wiki
    def list_wikis(self, project: str) -> Req:
        return Req("GET", f"{self.org}/{seg(project)}/_apis/wiki/wikis", {"api-version": API}, label="wiki.list")

    def create_project_wiki(self, project: str, project_id: str, name: str) -> Req:
        return Req("POST", f"{self.org}/{seg(project)}/_apis/wiki/wikis", {"api-version": API},
                   {"type": "projectWiki", "name": name, "projectId": project_id}, label="wiki.create")

    def get_wiki_page(self, project: str, wiki_id: str, path: str) -> Req:
        return Req("GET", f"{self.org}/{seg(project)}/_apis/wiki/wikis/{seg(wiki_id)}/pages",
                   {"path": path, "includeContent": "true", "api-version": API}, label="wiki.getPage")

    def put_wiki_page(self, project: str, wiki_id: str, path: str, content: str, etag: str | None = None,
                      comment: str = "HarborPoint provisioner") -> Req:
        headers = {"Content-Type": "application/json"}
        if etag:
            headers["If-Match"] = etag
        return Req("PUT", f"{self.org}/{seg(project)}/_apis/wiki/wikis/{seg(wiki_id)}/pages",
                   {"path": path, "comment": comment, "api-version": API}, {"content": content}, headers,
                   label="wiki.updatePage" if etag else "wiki.createPage")

    # ---- dashboards
    def _dash_base(self, project: str, team: str | None) -> str:
        base = f"{self.org}/{seg(project)}"
        if team:
            base += f"/{seg(team)}"
        return base + "/_apis/dashboard/dashboards"

    def list_dashboards(self, project: str, team: str | None) -> Req:
        return Req("GET", self._dash_base(project, team), {"api-version": API_DASHBOARD}, label="dashboards.list")

    def create_dashboard(self, project: str, team: str | None, body: dict) -> Req:
        return Req("POST", self._dash_base(project, team), {"api-version": API_DASHBOARD}, body,
                   label="dashboards.create")

    def get_dashboard(self, project: str, team: str | None, dashboard_id: str) -> Req:
        return Req("GET", self._dash_base(project, team) + f"/{seg(dashboard_id)}", {"api-version": API_DASHBOARD},
                   label="dashboards.get")

    def create_widget(self, project: str, team: str | None, dashboard_id: str, body: dict) -> Req:
        return Req("POST", self._dash_base(project, team) + f"/{seg(dashboard_id)}/widgets",
                   {"api-version": API_WIDGET}, body, label="dashboards.addWidget")

    # ---- delivery plans
    def list_plans(self, project: str) -> Req:
        return Req("GET", f"{self.org}/{seg(project)}/_apis/work/plans", {"api-version": API}, label="plans.list")

    def create_plan(self, project: str, body: dict) -> Req:
        return Req("POST", f"{self.org}/{seg(project)}/_apis/work/plans", {"api-version": API}, body,
                   label="plans.create")

    # ---- analytics (pilot checks only; printed, not called)
    def odata_revisions_url(self, project: str, wi_id: int) -> str:
        host = self.org.replace("https://dev.azure.com/", "https://analytics.dev.azure.com/")
        return (f"{host}/{seg(project)}/_odata/v4.0-preview/WorkItemRevisions?"
                f"$filter=WorkItemId%20eq%20{int(wi_id)}&$select=Revision,ChangedDate,State,IterationPath,"
                f"StoryPoints&$orderby=Revision")


# --------------------------------------------------------------------------- small utilities

def iso_midnight(day: str) -> str:
    """'2026-10-26' -> '2026-10-26T00:00:00Z' (iteration/day-off dates are date-only, midnight UTC)."""
    day = str(day)[:10]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
        raise ValueError(f"Not a YYYY-MM-DD date: {day!r}")
    return day + "T00:00:00Z"


def redact(obj: Any, max_str: int = 160) -> Any:
    """Return a copy safe to print: long strings truncated, auth-like keys masked."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if str(k).lower() in ("authorization", "pat", "password", "token_secret"):
                out[k] = "***"
            else:
                out[k] = redact(v, max_str)
        return out
    if isinstance(obj, list):
        if len(obj) > 12:
            return [redact(x, max_str) for x in obj[:12]] + [f"... ({len(obj) - 12} more)"]
        return [redact(x, max_str) for x in obj]
    if isinstance(obj, str) and len(obj) > max_str:
        return obj[:max_str] + f"... ({len(obj)} chars)"
    return obj

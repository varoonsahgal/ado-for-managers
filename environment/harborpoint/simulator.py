"""In-memory simulator of the Azure DevOps REST subset used by the provisioner.

It is a *transport* for :class:`harborpoint.ado.AdoClient`, so the provisioner's real step
code runs unchanged against it. ``--dry-run`` uses it to produce an exact request plan with no
network access, and the unit tests use it to assert URLs, headers and bodies.

The simulator deliberately enforces the server rules that matter for seeding (as documented
in the research notes) so bugs surface offline:

* work item writes must use ``application/json-patch+json``;
* setting System.CreatedDate/ChangedDate requires ``bypassRules=true``;
* System.CreatedDate only on revision 1; System.ChangedDate strictly increasing (VS402625);
* no revision in the future (relative to the simulator clock);
* area/iteration paths and relation targets must exist; parents of nodes/queries/wiki pages
  must exist; wiki edits need ``If-Match``; team days off need the iteration selected; etc.

``link_side_effect`` models the UNCERTAIN behaviour of the *other* end of a link:
``"none"`` (no revision on the target), ``"same_time"`` (target gets a revision stamped with
the source's ChangedDate) or ``"now"`` (target gets a revision stamped with server time).
"""
from __future__ import annotations

import itertools
import json
import re
import uuid
from datetime import datetime, timezone
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

WIT_STATES = {
    "Epic": ["New", "Active", "Resolved", "Closed", "Removed"],
    "Feature": ["New", "Active", "Resolved", "Closed", "Removed"],
    "User Story": ["New", "Active", "Resolved", "Closed", "Removed"],
    "Bug": ["New", "Active", "Resolved", "Closed"],
    "Task": ["New", "Active", "Closed", "Removed"],
}
STATE_CATEGORY = {"New": "Proposed", "Active": "InProgress", "Resolved": "InProgress",
                  "Closed": "Completed", "Removed": "Removed"}
LINK_TYPES = {
    "System.LinkTypes.Hierarchy-Reverse": "System.LinkTypes.Hierarchy-Forward",
    "System.LinkTypes.Hierarchy-Forward": "System.LinkTypes.Hierarchy-Reverse",
    "System.LinkTypes.Dependency-Forward": "System.LinkTypes.Dependency-Reverse",
    "System.LinkTypes.Dependency-Reverse": "System.LinkTypes.Dependency-Forward",
    "System.LinkTypes.Related": "System.LinkTypes.Related",
}
BAD_NODE_CHARS = set('\\/:*?"<>|#$&+')


class SimError(Exception):
    def __init__(self, status: int, message: str, type_key: str = "SimulatedException"):
        super().__init__(message)
        self.status, self.message, self.type_key = status, message, type_key


def _parse_dt(s: str) -> datetime:
    s = str(s).replace("Z", "+00:00")
    dt = datetime.fromisoformat(s)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


class AdoSimulator:
    """Callable transport: ``sim(method, url, headers, data, timeout) -> (status, headers, bytes)``."""

    def __init__(self, org: str = "sim", *, now: datetime | None = None, link_side_effect: str = "none",
                 existing_project: str | None = None, fail_labels: dict[str, int] | None = None):
        self.org = org
        self.now = now or datetime.now(timezone.utc)
        self.link_side_effect = link_side_effect
        self.fail_patterns = fail_labels or {}   # regex on "METHOD path" -> status to force
        self.calls: list[dict] = []
        self._ticks = itertools.count(1)
        self._ids = itertools.count(1)
        self.projects: dict[str, dict] = {}
        self.ops: dict[str, str] = {}
        self.nodes: dict[str, dict[str, dict]] = {}
        self.teams: dict[str, list[dict]] = {}
        self.team_cfg: dict[str, dict] = {}
        self.workitems: dict[int, dict] = {}
        self._wi_ids = itertools.count(1)
        self.queries: dict[str, dict[str, dict]] = {}
        self.wikis: dict[str, list[dict]] = {}
        self.pages: dict[str, dict[str, dict]] = {}
        self.dashboards: dict[tuple, list[dict]] = {}
        self.plans: dict[str, list[dict]] = {}
        self.aces: list[dict] = []
        self.memberships: list[tuple[str, str]] = []
        if existing_project:
            self._make_project(existing_project, "pre-existing")

    def server_now(self) -> str:
        """Server-side timestamp: advances 1 ms per stamp, like a real clock."""
        from datetime import timedelta
        return (self.now + timedelta(milliseconds=next(self._ticks))).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # ------------------------------------------------------------------ transport entry
    def __call__(self, method: str, url: str, headers: dict, data: bytes | None, timeout: float = 0):
        u = urlparse(url)
        q = {k: v[0] for k, v in parse_qs(u.query, keep_blank_values=True).items()}
        body = json.loads(data.decode()) if data else None
        record = {"method": method, "url": url, "path": unquote(u.path), "query": q, "headers": dict(headers),
                  "body": body, "host": u.netloc}
        self.calls.append(record)
        for pattern, status in self.fail_patterns.items():
            if re.search(pattern, f"{method} {unquote(u.path)}"):
                return self._resp(status, {"message": f"forced failure ({pattern})", "typeKey": "Forced"})
        try:
            status, payload, extra = self._route(method, u.netloc, unquote(u.path), q, headers, body)
        except SimError as e:
            return self._resp(e.status, {"message": e.message, "typeKey": e.type_key})
        return self._resp(status, payload, extra)

    @staticmethod
    def _resp(status: int, payload: Any, extra_headers: dict | None = None):
        h = {"Content-Type": "application/json; charset=utf-8", **(extra_headers or {})}
        raw = b"" if payload is None else json.dumps(payload).encode()
        return status, h, raw

    # ------------------------------------------------------------------ routing
    def _route(self, method, host, path, q, headers, body):
        parts = [p for p in path.split("/") if p]
        if host.startswith("vssps.") or ".vssps." in host:
            return self._vssps(method, parts[1:], q, body)
        if host.startswith("vsaex.") or ".vsaex." in host:
            return self._vsaex(method, parts[1:], q, body)
        parts = parts[1:]  # drop org name
        if "_apis" not in parts:
            raise SimError(404, "no _apis segment")
        i = parts.index("_apis")
        scope, rest = parts[:i], parts[i + 1:]
        if not scope:
            return self._org_level(method, rest, q, body)
        project = self._project(scope[0])
        team = self._team(project, scope[1]) if len(scope) > 1 else None
        return self._project_level(method, project, team, rest, q, headers, body)

    # ------------------------------------------------------------------ org level
    def _org_level(self, method, rest, q, body):
        key = "/".join(rest[:2])
        if rest == ["connectionData"]:
            return 200, {"authenticatedUser": {"id": "sim-user", "providerDisplayName": "Sim Admin"},
                         "instanceId": "sim-instance"}, None
        if key == "process/processes":
            return 200, {"count": 2, "value": [
                {"id": "adcc42ab-9882-485e-a3ed-7678f01f66bc", "name": "Agile", "isDefault": True},
                {"id": "6b724908-ef14-45cf-84f8-768b5384da45", "name": "Scrum"}]}, None
        if rest[0] == "projects" and len(rest) == 1 and method == "POST":
            self._require_version(q, "7.1")
            name = body["name"]
            if name in self.projects:
                raise SimError(409, f"TF200019: project {name} already exists", "ProjectAlreadyExistsException")
            tid = body["capabilities"]["processTemplate"]["templateTypeId"]
            if tid != "adcc42ab-9882-485e-a3ed-7678f01f66bc":
                raise SimError(400, "unexpected process (sim expects Agile)")
            self._make_project(name, body.get("description", ""))
            op = str(uuid.uuid4())
            self.ops[op] = "succeeded"
            return 202, {"id": op, "status": "queued", "url": f"https://dev.azure.com/{self.org}/_apis/operations/{op}"}, None
        if rest[0] == "projects" and len(rest) == 2 and method == "GET":
            p = self._find_project(rest[1])
            if not p:
                raise SimError(404, f"TF200016: The following project does not exist: {rest[1]}",
                               "ProjectDoesNotExistWithNameException")
            return 200, self._project_json(p), None
        if rest[0] == "projects" and len(rest) == 3 and rest[2] == "teams":
            p = self._find_project(rest[1])
            if not p:
                raise SimError(404, "project not found")
            if method == "GET":
                return 200, {"count": len(self.teams[p["id"]]), "value": self.teams[p["id"]]}, None
            if method == "POST":
                if any(t["name"].lower() == body["name"].lower() for t in self.teams[p["id"]]):
                    raise SimError(400, "team exists", "TeamAlreadyExists")
                t = self._make_team(p, body["name"], body.get("description", ""))
                return 200, t, None
        if rest[0] == "operations":
            return 200, {"id": rest[1], "status": self.ops.get(rest[1], "failed")}, None
        if rest[0] == "securitynamespaces":
            return 200, {"count": 1, "value": [{"namespaceId": rest[1], "name": "WorkItemQueryFolders",
                         "actions": [{"bit": 1, "name": "Read"}, {"bit": 2, "name": "Contribute"},
                                     {"bit": 4, "name": "Delete"}, {"bit": 8, "name": "ManagePermissions"},
                                     {"bit": 16, "name": "FullControl"}]}]}, None
        if rest[0] == "accesscontrollists":
            token = q.get("token", "")
            out = []
            for p in self.projects.values():
                sq = self.queries[p["id"]]["Shared Queries"]
                t = f"$/{p['id']}/{sq['id']}"
                if t.startswith(token) or token.startswith(f"$/{p['id']}"):
                    out.append({"token": t, "inheritPermissions": True, "acesDictionary": {}})
            return 200, {"count": len(out), "value": out}, None
        if rest[0] == "accesscontrolentries" and method == "POST":
            for ace in body["accessControlEntries"]:
                if not str(ace["descriptor"]).startswith("Microsoft.TeamFoundation.Identity;"):
                    raise SimError(400, "ACE descriptor must be an identity descriptor")
            if not str(body["token"]).startswith("$/"):
                raise SimError(400, "bad token")
            self.aces.append(body)
            return 200, {"count": 1, "value": body["accessControlEntries"]}, None
        raise SimError(404, f"sim: unknown org route {method} {'/'.join(rest)}")

    # ------------------------------------------------------------------ vssps / vsaex
    def _vssps(self, method, parts, q, body):
        rest = parts[parts.index("_apis") + 1:]
        if rest[:2] == ["graph", "descriptors"]:
            return 200, {"value": f"scp.{rest[2]}"}, None
        if rest[:2] == ["graph", "groups"]:
            pid = q["scopeDescriptor"].replace("scp.", "")
            p = self._find_project(pid)
            name = p["name"] if p else "?"
            return 200, {"count": 2, "value": [
                {"principalName": f"[{name}]\\Contributors", "displayName": "Contributors",
                 "descriptor": f"vssgp.contrib-{pid}"},
                {"principalName": f"[{name}]\\Readers", "displayName": "Readers", "descriptor": f"vssgp.read-{pid}"}]}, None
        if rest == ["identities"]:
            d = q["subjectDescriptors"]
            return 200, {"count": 1, "value": [{"id": "id-" + d, "descriptor": "Microsoft.TeamFoundation.Identity;S-1-9-" + d}]}, None
        if rest[:2] == ["graph", "memberships"] and method == "PUT":
            self.memberships.append((rest[2], rest[3]))
            return 201, {"memberDescriptor": rest[2], "containerDescriptor": rest[3]}, None
        raise SimError(404, f"sim: unknown vssps route {'/'.join(rest)}")

    def _vsaex(self, method, parts, q, body):
        rest = parts[parts.index("_apis") + 1:]
        if rest == ["userentitlements"] and method == "POST":
            email = body["user"]["principalName"]
            return 200, {"isSuccess": True, "userEntitlement": {"user": {"principalName": email,
                         "descriptor": "aad." + email}}}, None
        raise SimError(404, "sim: unknown vsaex route")

    # ------------------------------------------------------------------ project level
    def _project_level(self, method, p, team, rest, q, headers, body):
        pid = p["id"]
        if rest[:3] == ["wit", "classificationnodes", "Areas"] or rest[:3] == ["wit", "classificationnodes", "Iterations"]:
            return self._nodes(method, p, rest[2], rest[3:], q, body)
        if rest[:2] == ["wit", "workitems"]:
            return self._workitems(method, p, rest[2:], q, headers, body)
        if rest[:2] == ["wit", "workitemtypes"]:
            return 200, {"value": [{"name": s, "category": STATE_CATEGORY[s]} for s in WIT_STATES.get(rest[2], [])]}, None
        if rest[:2] == ["wit", "wiql"]:
            return self._wiql(p, body, q)
        if rest[:2] == ["wit", "queries"]:
            return self._queries(method, p, rest[2:], q, body)
        if rest[:2] == ["work", "teamsettings"]:
            if not team:
                raise SimError(404, "team settings need a team")
            return self._teamsettings(method, p, team, rest[2:], q, body)
        if rest[:2] == ["wiki", "wikis"]:
            return self._wiki(method, p, rest[2:], q, headers, body)
        if rest[:2] == ["dashboard", "dashboards"]:
            return self._dashboards(method, p, team, rest[2:], q, body)
        if rest[:2] == ["work", "plans"]:
            if method == "GET":
                return 200, {"count": len(self.plans[pid]), "value": self.plans[pid]}, None
            team_ids = {t["id"] for t in self.teams[pid]}
            for m in body["properties"]["teamBacklogMappings"]:
                if m["teamId"] not in team_ids:
                    raise SimError(400, f"unknown team {m['teamId']}")
                if m["categoryReferenceName"] not in ("Microsoft.EpicCategory", "Microsoft.FeatureCategory",
                                                      "Microsoft.RequirementCategory"):
                    raise SimError(400, "bad category")
            plan = {"id": str(uuid.uuid4()), "name": body["name"], "type": body["type"], "revision": 1,
                    "properties": body["properties"]}
            self.plans[pid].append(plan)
            return 201, plan, None
        raise SimError(404, f"sim: unknown project route {method} {'/'.join(rest)}")

    # ------------------------------------------------------------------ nodes
    def _nodes(self, method, p, group, rel, q, body):
        root = self.nodes[p["id"]][group]
        if method == "GET":
            node = self._node_at(root, rel)
            if node is None:
                raise SimError(404, "TF401347: Invalid tree name given for work item -1, field System.AreaPath.")
            return 200, node, None
        if method == "POST":
            parent = self._node_at(root, rel)
            if parent is None:
                raise SimError(404, f"VS402371: parent node {'/'.join(rel)} not found")
            name = body["name"]
            if BAD_NODE_CHARS & set(name):
                raise SimError(400, f"VS402407: invalid node name {name}")
            if any(c["name"].lower() == name.lower() for c in parent.get("children", [])):
                raise SimError(409, f"VS402371: node {name} already exists", "ClassificationNodeDuplicateNameException")
            node = self._new_node(parent, name, group)
            if body.get("attributes"):
                if group != "Iterations":
                    raise SimError(400, "areas have no date attributes")
                node["attributes"] = self._dates(body["attributes"])
            return 201, node, None
        if method == "PATCH":
            node = self._node_at(root, rel)
            if node is None:
                raise SimError(404, "node not found")
            node["attributes"] = self._dates(body["attributes"])
            return 200, node, None
        raise SimError(405, "method")

    @staticmethod
    def _dates(attrs):
        s, f = attrs.get("startDate"), attrs.get("finishDate")
        for v in (s, f):
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T00:00:00Z", str(v)):
                raise SimError(400, f"iteration dates must be midnight UTC ISO strings: {v}")
        if s > f:
            raise SimError(400, "VS402411: start after finish")
        return {"startDate": s, "finishDate": f}

    def _node_at(self, root, rel):
        node = root
        for name in rel:
            node = next((c for c in node.get("children", []) if c["name"].lower() == name.lower()), None)
            if node is None:
                return None
        return node

    def _new_node(self, parent, name, group):
        node = {"id": next(self._ids), "identifier": str(uuid.uuid4()), "name": name,
                "structureType": "area" if group == "Areas" else "iteration", "hasChildren": False,
                "path": parent["path"] + "\\" + name, "children": []}
        parent.setdefault("children", []).append(node)
        parent["hasChildren"] = True
        return node

    def _all_paths(self, p, group) -> dict[str, dict]:
        """Full work-item-field paths (``Proj\\A\\B``) -> node."""
        out = {}

        def walk(node, prefix):
            out[prefix] = node
            for c in node.get("children", []):
                walk(c, prefix + "\\" + c["name"])
        walk(self.nodes[p["id"]][group], p["name"])
        return out

    # ------------------------------------------------------------------ team settings
    def _teamsettings(self, method, p, team, rest, q, body):
        cfg = self.team_cfg[team["id"]]
        if rest == ["teamfieldvalues"]:
            if method == "GET":
                return 200, cfg["fieldvalues"], None
            areas = self._all_paths(p, "Areas")
            for v in [body["defaultValue"]] + [x["value"] for x in body["values"]]:
                if v not in areas:
                    raise SimError(400, f"TF400499: area path {v} not found (note: no '\\Area\\' segment)")
            cfg["fieldvalues"] = body
            return 200, body, None
        if rest == ["iterations"]:
            its = {n["identifier"]: (path, n) for path, n in self._all_paths(p, "Iterations").items()}
            if method == "GET":
                return 200, {"count": len(cfg["iterations"]), "value": [
                    {"id": g, "name": its[g][1]["name"], "path": its[g][0],
                     "attributes": its[g][1].get("attributes", {})} for g in cfg["iterations"]]}, None
            if method == "POST":
                g = body["id"]
                if g not in its:
                    raise SimError(400, f"iteration {g} is not an iteration identifier GUID")
                if g in cfg["iterations"]:
                    raise SimError(409, "already selected")
                cfg["iterations"].append(g)
                return 200, {"id": g, "name": its[g][1]["name"], "path": its[g][0]}, None
        if len(rest) == 3 and rest[0] == "iterations" and rest[2] == "teamdaysoff" and method == "PATCH":
            if rest[1] not in cfg["iterations"]:
                raise SimError(404, "iteration not selected for team")
            for d in body["daysOff"]:
                self._dates({"startDate": d["start"], "finishDate": d["end"]})
            cfg["daysoff"][rest[1]] = body["daysOff"]
            return 200, body, None
        if rest == [] and method == "PATCH":
            its = {n["identifier"] for n in self._all_paths(p, "Iterations").values()}
            if "backlogIteration" in body and body["backlogIteration"] not in its:
                raise SimError(400, "backlogIteration must be an iteration identifier GUID")
            if body.get("bugsBehavior") not in (None, "off", "asRequirements", "asTasks"):
                raise SimError(400, "bad bugsBehavior")
            for k in body.get("backlogVisibilities", {}):
                if k not in ("Microsoft.EpicCategory", "Microsoft.FeatureCategory", "Microsoft.RequirementCategory"):
                    raise SimError(400, f"bad backlog category {k}")
            if body.get("defaultIterationMacro") not in (None, "@currentIteration"):
                raise SimError(400, "bad macro")
            cfg["settings"].update(body)
            return 200, cfg["settings"], None
        raise SimError(404, f"sim: unknown teamsettings route {'/'.join(rest)}")

    # ------------------------------------------------------------------ work items
    def _workitems(self, method, p, rest, q, headers, body):
        if method in ("POST", "PATCH"):
            if headers.get("Content-Type") != "application/json-patch+json":
                raise SimError(415, "work item writes need application/json-patch+json")
            if not isinstance(body, list):
                raise SimError(400, "JSON patch must be a list")
        if method == "POST" and rest and rest[0].startswith("$"):
            wit = rest[0][1:]
            if wit not in WIT_STATES:
                raise SimError(404, f"TF237124: Work Item Type '{wit}' does not exist.")
            wi_id = next(self._wi_ids)
            wi = {"id": wi_id, "type": wit, "fields": {"System.TeamProject": p["name"],
                                                       "System.WorkItemType": wit}, "relations": [],
                  "revisions": [], "project": p["id"]}
            self._apply(p, wi, body, q, first=True)
            if q.get("validateOnly") != "true":
                self.workitems[wi_id] = wi
            return 200, self._wi_json(wi), None
        if not rest:
            raise SimError(404, "no id")
        wi = self.workitems.get(int(rest[0]))
        if wi is None:
            raise SimError(404, f"TF401232: Work item {rest[0]} does not exist")
        if method == "GET" and len(rest) == 2 and rest[1] == "revisions":
            return 200, {"count": len(wi["revisions"]), "value": wi["revisions"]}, None
        if method == "GET":
            return 200, self._wi_json(wi), None
        if method == "PATCH":
            if q.get("validateOnly") == "true":
                import copy
                probe = copy.deepcopy(wi)
                self._apply(p, probe, body, q, first=False, side_effects=False)
                return 200, self._wi_json(probe), None
            self._apply(p, wi, body, q, first=False)
            return 200, self._wi_json(wi), None
        if method == "DELETE":
            del self.workitems[wi["id"]]
            return 200, {"id": wi["id"]}, None
        raise SimError(405, "method")

    def _apply(self, p, wi, ops, q, *, first: bool, side_effects: bool = True):
        bypass = q.get("bypassRules") == "true"
        new_fields = dict(wi["fields"])
        new_rels = list(wi["relations"])
        added_links = []
        for op in ops:
            if op.get("op") not in ("add", "replace", "remove", "test"):
                raise SimError(400, f"bad op {op.get('op')}")
            path = op["path"]
            if path.startswith("/fields/"):
                ref = path[len("/fields/"):]
                if op["op"] == "remove":
                    new_fields.pop(ref, None)
                else:
                    new_fields[ref] = op.get("value")
            elif path == "/relations/-" and op["op"] == "add":
                rel = op["value"]
                if rel["rel"] not in LINK_TYPES:
                    raise SimError(400, f"unknown link type {rel['rel']}")
                m = re.search(r"/_apis/wit/workItems/(\d+)$", rel["url"])
                if not m or int(m.group(1)) not in self.workitems:
                    raise SimError(400, f"TF201036: relation target not found: {rel['url']}")
                if rel["rel"] == "System.LinkTypes.Hierarchy-Reverse" and any(
                        r["rel"] == rel["rel"] for r in new_rels):
                    raise SimError(400, "TF201036: only one parent allowed")
                new_rels.append(rel)
                added_links.append((int(m.group(1)), rel))
            elif op["op"] != "test":
                raise SimError(400, f"unsupported path {path}")
        # --- dates
        for ref in ("System.CreatedDate", "System.ChangedDate", "System.ChangedBy", "System.CreatedBy"):
            if ref in new_fields and new_fields.get(ref) != wi["fields"].get(ref) and not bypass:
                raise SimError(400, f"{ref} can only be set with bypassRules=true (sim strict mode)")
        if not first and new_fields.get("System.CreatedDate") != wi["fields"].get("System.CreatedDate"):
            raise SimError(400, "System.CreatedDate can only be set on the first revision")
        changed = new_fields.get("System.ChangedDate")
        prev = wi["fields"].get("System.ChangedDate")
        supplied = any(o["path"] == "/fields/System.ChangedDate" for o in ops)
        if not supplied:
            changed = self.server_now()
            new_fields["System.ChangedDate"] = changed
        cd = _parse_dt(changed)
        if supplied and cd > self.now:
            raise SimError(400, "VS402624 (sim): ChangedDate in the future is not allowed")
        if prev is not None and cd <= _parse_dt(prev):
            raise SimError(400, "VS402625: Dates must be increasing with each revision.")
        if first:
            new_fields.setdefault("System.CreatedDate", changed)
            if _parse_dt(new_fields["System.CreatedDate"]) != cd:
                raise SimError(400, "sim: CreatedDate must equal ChangedDate on revision 1")
        # --- values
        if not new_fields.get("System.Title"):
            raise SimError(400, "TF401320: Title is required")
        state = new_fields.get("System.State", "New")
        new_fields["System.State"] = state
        if state not in WIT_STATES[wi["type"]]:
            raise SimError(400, f"TF401324: state {state} not valid for {wi['type']}")
        areas = self._all_paths(p, "Areas")
        its = self._all_paths(p, "Iterations")
        new_fields.setdefault("System.AreaPath", p["name"])
        new_fields.setdefault("System.IterationPath", p["name"])
        if new_fields["System.AreaPath"] not in areas:
            raise SimError(400, f"TF401347: Invalid tree name {new_fields['System.AreaPath']} (AreaPath)")
        if new_fields["System.IterationPath"] not in its:
            raise SimError(400, f"TF401347: Invalid tree name {new_fields['System.IterationPath']} (IterationPath)")
        for ref in new_fields:
            if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z0-9_]+)+", ref):
                raise SimError(400, f"TF51535: Cannot find field {ref}")
        # --- link side effects on the other end (UNCERTAIN live behaviour)
        if side_effects:
            for target_id, rel in added_links:
                target = self.workitems[target_id]
                back = {"rel": LINK_TYPES[rel["rel"]], "url": f"https://dev.azure.com/{self.org}/_apis/wit/workItems/{wi['id']}"}
                if self.link_side_effect == "none":
                    target["relations"].append(back)
                    continue
                stamp = changed if self.link_side_effect == "same_time" else self.server_now()
                tprev = target["fields"]["System.ChangedDate"]
                if _parse_dt(stamp) <= _parse_dt(tprev):
                    raise SimError(400, f"VS402625: Dates must be increasing with each revision. "
                                        f"(link target {target_id})")
                target["relations"].append(back)
                target["fields"]["System.ChangedDate"] = stamp
                self._snapshot(target)
        wi["fields"], wi["relations"] = new_fields, new_rels
        self._snapshot(wi)

    def _snapshot(self, wi):
        rev = len(wi["revisions"]) + 1
        wi["rev"] = rev
        wi["revisions"].append({"id": wi["id"], "rev": rev, "fields": dict(wi["fields"]),
                                "relations": list(wi["relations"])})

    def _wi_json(self, wi):
        return {"id": wi["id"], "rev": wi.get("rev", 0), "fields": wi["fields"], "relations": wi["relations"],
                "url": f"https://dev.azure.com/{self.org}/_apis/wit/workItems/{wi['id']}"}

    def _wiql(self, p, body, q):
        query = body["query"]
        if "{" in query:
            raise SimError(400, "WIQL contains unreplaced token")
        ids = [w["id"] for w in self.workitems.values() if w["project"] == p["id"]]
        m = re.search(r"\[System\.Title\]\s*=\s*'((?:[^']|'')*)'", query)
        if m:
            title = m.group(1).replace("''", "'")
            ids = [i for i in ids if self.workitems[i]["fields"].get("System.Title") == title]
        top = int(q.get("$top", "0") or 0)
        if top:
            ids = ids[:top]
        return 200, {"queryType": "flat", "workItems": [{"id": i} for i in ids]}, None

    # ------------------------------------------------------------------ queries
    def _queries(self, method, p, rest, q, body):
        store = self.queries[p["id"]]
        path = "/".join(rest)
        if method == "GET":
            item = store.get(path) or next((v for v in store.values() if v["id"] == path), None)
            if item is None:
                raise SimError(404, f"TF401243: query {path} not found")
            return 200, self._q_json(store, item, int(q.get("$depth", "0") or 0)), None
        if method == "POST":
            parent = store.get(path)
            if parent is None or not parent["isFolder"]:
                raise SimError(404, f"parent folder {path} not found")
            child = path + "/" + body["name"]
            if child in store:
                raise SimError(409, f"TF237018: {body['name']} already exists", "QueryItemAlreadyExistsException")
            if re.search(r'[/\\<>*?"+|:]', body["name"]):
                raise SimError(400, "invalid query name")
            if not body.get("isFolder"):
                wiql = body.get("wiql", "")
                if not wiql.lstrip().upper().startswith("SELECT") or "{" in wiql:
                    raise SimError(400, "TF51006: invalid WIQL")
            item = {"id": str(uuid.uuid4()), "name": body["name"], "path": child,
                    "isFolder": bool(body.get("isFolder")), "wiql": body.get("wiql")}
            store[child] = item
            return 201, item, None
        if method == "PATCH":
            item = next((v for v in store.values() if v["id"] == path), None)
            if item is None:
                raise SimError(404, "query not found")
            item["wiql"] = body["wiql"]
            return 200, item, None
        raise SimError(405, "method")

    def _q_json(self, store, item, depth):
        out = {k: v for k, v in item.items() if v is not None}
        if item["isFolder"] and depth > 0:
            kids = [v for k, v in store.items() if k.rsplit("/", 1)[0] == item["path"] and k != item["path"]]
            out["hasChildren"] = bool(kids)
            out["children"] = [self._q_json(store, k, depth - 1) for k in kids]
        return out

    # ------------------------------------------------------------------ wiki
    def _wiki(self, method, p, rest, q, headers, body):
        pid = p["id"]
        if not rest:
            if method == "GET":
                return 200, {"count": len(self.wikis[pid]), "value": self.wikis[pid]}, None
            if any(w["type"] == "projectWiki" for w in self.wikis[pid]):
                raise SimError(400, "project wiki already exists", "WikiAlreadyExistsException")
            w = {"id": str(uuid.uuid4()), "name": body["name"], "type": body["type"], "projectId": body["projectId"]}
            self.wikis[pid].append(w)
            self.pages[w["id"]] = {}
            return 201, w, None
        wiki = next((w for w in self.wikis[pid] if rest[0] in (w["id"], w["name"])), None)
        if wiki is None:
            raise SimError(404, "wiki not found")
        pages = self.pages[wiki["id"]]
        if rest[1:] == ["pages"]:
            path = q.get("path", "")
            if method == "GET":
                pg = pages.get(path)
                if pg is None:
                    raise SimError(404, f"Wiki page '{path}' could not be found.", "WikiPageNotFoundException")
                return 200, {"path": path, "content": pg["content"]}, {"ETag": f'"{pg["version"]}"'}
            if method == "PUT":
                if "#" in path or not path.startswith("/"):
                    raise SimError(400, "bad page path")
                parent = path.rsplit("/", 1)[0]
                if parent and parent not in pages:
                    raise SimError(400, f"parent page {parent} missing (sim strict)")
                existing = pages.get(path)
                etag = headers.get("If-Match")
                if existing and not etag:
                    raise SimError(409, "WikiPageAlreadyExistsException: If-Match required to update",
                                   "WikiPageAlreadyExistsException")
                if existing and etag.strip('"') != existing["version"]:
                    raise SimError(412, "stale ETag")
                version = uuid.uuid4().hex[:12]
                pages[path] = {"content": body["content"], "version": version}
                return (200 if existing else 201), {"path": path, "id": len(pages)}, {"ETag": f'"{version}"'}
        raise SimError(404, "sim: unknown wiki route")

    # ------------------------------------------------------------------ dashboards
    def _dashboards(self, method, p, team, rest, q, body):
        key = (p["id"], team["id"] if team else None)
        boards = self.dashboards.setdefault(key, [])
        if not rest:
            if method == "GET":
                return 200, {"value": [{k: v for k, v in b.items() if k != "widgets"} for b in boards]}, None
            if method == "POST":
                self._require_version(q, "7.1-preview.3")
                if any(b["name"] == body["name"] for b in boards):
                    raise SimError(409, "dashboard exists")
                b = {"id": str(uuid.uuid4()), "name": body["name"], "description": body.get("description", ""),
                     "eTag": "1", "widgets": [], "dashboardScope": "project_Team" if team else "project"}
                for w in body.get("widgets", []):
                    self._check_widget(p, w)
                    b["widgets"].append(dict(w, id=str(uuid.uuid4())))
                boards.append(b)
                return 200, b, None
        b = next((x for x in boards if x["id"] == rest[0]), None)
        if b is None:
            raise SimError(404, "dashboard not found")
        if rest[1:] == [] and method == "GET":
            return 200, b, None
        if rest[1:] == ["widgets"] and method == "POST":
            self._require_version(q, "7.1-preview.2")
            if body.get("dashboard", {}).get("eTag") != b["eTag"]:
                raise SimError(409, "dashboard eTag mismatch")
            self._check_widget(p, body)
            w = dict(body, id=str(uuid.uuid4()))
            b["widgets"].append(w)
            b["eTag"] = str(int(b["eTag"]) + 1)
            return 200, dict(w, dashboard={"eTag": b["eTag"]}), None
        raise SimError(404, "sim: unknown dashboard route")

    def _check_widget(self, p, w):
        for k in ("name", "position", "size", "contributionId"):
            if k not in w:
                raise SimError(400, f"widget missing {k}")
        if w["contributionId"].endswith("MarkdownWidget"):
            return
        settings = json.loads(w["settings"]) if w.get("settings") else {}
        qid = settings.get("queryId") or (settings.get("query") or {}).get("queryId") or settings.get("groupKey")
        if qid is not None and not any(v["id"] == qid for v in self.queries[p["id"]].values()):
            raise SimError(400, f"widget references unknown query {qid}")
        team_ids = {t["id"] for t in self.teams[p["id"]]}
        tid = settings.get("teamId")
        if tid is not None and tid not in team_ids:
            raise SimError(400, "widget references unknown team")

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _require_version(q, version):
        if q.get("api-version") != version:
            raise SimError(400, f"api-version {q.get('api-version')} != expected {version} (sim)")

    def _make_project(self, name, description):
        pid = str(uuid.uuid4())
        p = {"id": pid, "name": name, "description": description}
        self.projects[name] = p
        self.teams[pid] = []
        team = self._make_team(p, f"{name} Team", f"The default project team.")
        p["defaultTeam"] = {"id": team["id"], "name": team["name"]}
        self.nodes[pid] = {
            "Areas": {"id": next(self._ids), "identifier": str(uuid.uuid4()), "name": name, "structureType": "area",
                      "hasChildren": False, "path": f"\\{name}\\Area", "children": []},
            "Iterations": {"id": next(self._ids), "identifier": str(uuid.uuid4()), "name": name,
                           "structureType": "iteration", "hasChildren": False, "path": f"\\{name}\\Iteration",
                           "children": []}}
        sq = {"id": str(uuid.uuid4()), "name": "Shared Queries", "path": "Shared Queries", "isFolder": True}
        mq = {"id": str(uuid.uuid4()), "name": "My Queries", "path": "My Queries", "isFolder": True}
        self.queries[pid] = {"Shared Queries": sq, "My Queries": mq}
        self.wikis[pid] = []
        self.plans[pid] = []
        return p

    def _make_team(self, p, name, description):
        t = {"id": str(uuid.uuid4()), "name": name, "description": description, "projectId": p["id"]}
        self.teams[p["id"]].append(t)
        self.team_cfg[t["id"]] = {"fieldvalues": {"defaultValue": None, "values": []}, "iterations": [],
                                  "settings": {}, "daysoff": {}}
        return t

    def _project_json(self, p):
        return {"id": p["id"], "name": p["name"], "description": p["description"], "state": "wellFormed",
                "capabilities": {"processTemplate": {"templateName": "Agile",
                                                     "templateTypeId": "adcc42ab-9882-485e-a3ed-7678f01f66bc"}},
                "defaultTeam": p["defaultTeam"]}

    def _find_project(self, key):
        return self.projects.get(key) or next((p for p in self.projects.values() if p["id"] == key), None)

    def _project(self, key):
        p = self._find_project(key)
        if not p:
            raise SimError(404, f"TF200016: The following project does not exist: {key}")
        return p

    def _team(self, p, key):
        t = next((t for t in self.teams[p["id"]] if key in (t["id"], t["name"])), None)
        if not t:
            raise SimError(404, f"team {key} not found")
        return t

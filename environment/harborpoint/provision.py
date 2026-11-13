"""HarborPoint provisioner: apply a ``harborpoint-dataset/1`` file to Azure DevOps Services.

Usage (run from environment/)::

    python -m harborpoint.provision --org https://dev.azure.com/ORG --dataset out/dataset.json --dry-run
    python -m harborpoint.provision --org https://dev.azure.com/ORG --dataset out/dataset.json --steps pilot
    python -m harborpoint.provision --org https://dev.azure.com/ORG --dataset out/dataset.json --yes

Steps (in order; select with ``--steps a,b,c``; default = all):
    preflight, project, classification, teams, workitems, links, queries, wiki, dashboards,
    plans, participants, summary
Special steps (never part of "all"): ``pilot`` (areas/iterations, one team, one Feature + one
story with 4 backdated revisions, then a checklist) and ``pilot-cleanup`` (deletes the pilot items).

The run is idempotent and resumable: ``--state`` (default out/state.json) records every created
ID, and every step looks existing objects up by name before creating anything.
``--dry-run`` performs NO network access: it validates the dataset and executes every step
against an in-memory simulator (harborpoint.simulator) to print an exact request plan.

PAT scopes: see harborpoint.ado.PAT_SCOPES (printed by --help).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

from .ado import (AGILE_PROCESS_TYPE_ID, PAT_SCOPES, QUERY_FOLDER_NAMESPACE, AdoClient, AdoError, Api, Req,
                  Resp, redact)
from .dataset_check import (Report, expand_participants, parse_ts, sprint_leaf_map, team_area_values, validate)
from . import widgets as W

STEPS = ["preflight", "project", "classification", "teams", "workitems", "links", "queries", "wiki",
         "dashboards", "plans", "participants", "summary"]
SPECIAL_STEPS = ["pilot", "pilot-cleanup"]
LINK_REL = {"Predecessor": "System.LinkTypes.Dependency-Reverse",
            "Successor": "System.LinkTypes.Dependency-Forward",
            "Related": "System.LinkTypes.Related"}
PARENT_REL = "System.LinkTypes.Hierarchy-Reverse"
AVG_LATENCY_S = 0.35          # typical round trip for a work item write (used for estimates)
ENV_DIR = Path(__file__).resolve().parent.parent
DEFAULT_PAT_FILE = "~/.config/harborpoint/pat"


# =========================================================================== state

class State:
    """JSON state file mapping dataset keys to created IDs (written atomically)."""

    def __init__(self, path: Path | None, data: dict | None = None):
        self.path = path
        self.data = data or {"version": 1}

    @classmethod
    def load(cls, path: Path | None) -> "State":
        if path and path.exists():
            return cls(path, json.loads(path.read_text()))
        return cls(path)

    def section(self, name: str) -> dict:
        return self.data.setdefault(name, {})

    def save(self) -> None:
        if not self.path:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(self.data, indent=1, sort_keys=True))
        os.replace(tmp, self.path)


@dataclass
class Options:
    content_dir: Path = ENV_DIR / "content"
    assign_map: dict[str, str] = field(default_factory=dict)
    participant_map: list[tuple[str, str]] = field(default_factory=list)
    order: str = "item"                  # item | chronological
    parent_links: str = "create"         # create (in revision 1) | final (links step, not backdated)
    changed_by: str | None = None
    experimental_widgets: bool = False
    allow_existing_items: bool = False
    pilot_team: str | None = None
    poll_interval: float = 3.0
    project_timeout: float = 600.0
    dry_run: bool = False


class StepError(RuntimeError):
    pass


# =========================================================================== helpers

def ado_ts(value: Any) -> str:
    """Normalise an ISO timestamp to Azure DevOps' UTC form with milliseconds."""
    dt = parse_ts(value)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt.microsecond // 1000:03d}Z"


def wiql_quote(text: str) -> str:
    return "'" + str(text).replace("'", "''") + "'"


def read_pat(pat_file: str | None) -> str:
    """--pat-file wins, then AZDO_PAT, then the default file. The PAT is never printed."""
    candidates = []
    if pat_file:
        candidates.append(Path(pat_file).expanduser())
    elif os.environ.get("AZDO_PAT"):
        return os.environ["AZDO_PAT"].strip()
    else:
        candidates.append(Path(DEFAULT_PAT_FILE).expanduser())
    for p in candidates:
        if p.is_file():
            mode = p.stat().st_mode
            if mode & 0o077:
                print(f"WARNING: {p} is readable by other users; run: chmod 600 {p}", file=sys.stderr)
            pat = p.read_text().strip()
            if pat:
                return pat
    raise StepError(f"No PAT found. Put it in {candidates[0]} (chmod 600) or set AZDO_PAT.")


def retarget_project(ds: dict, new_name: str) -> None:
    """Rename the project in a dataset: rewrites Area/Iteration path prefixes in all revisions."""
    old = ds["project"]["name"]
    if new_name == old:
        return
    ds["project"]["name"] = new_name
    for wi in ds["work_items"]:
        for rev in wi["revisions"]:
            f = rev.get("fields") or {}
            for ref in ("System.AreaPath", "System.IterationPath"):
                v = f.get(ref)
                if isinstance(v, str) and (v == old or v.startswith(old + "\\")):
                    f[ref] = new_name + v[len(old):]


def read_csv_map(path: str | None, cols: tuple[str, str]) -> list[tuple[str, str]]:
    if not path:
        return []
    rows = []
    with open(Path(path).expanduser(), newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        missing = [c for c in cols if c not in (reader.fieldnames or [])]
        if missing:
            raise StepError(f"{path}: header must contain {', '.join(cols)} (missing {missing})")
        for row in reader:
            a, b = (row.get(cols[0]) or "").strip(), (row.get(cols[1]) or "").strip()
            if a:
                rows.append((a, b))
    return rows


# =========================================================================== provisioner

class Provisioner:
    def __init__(self, api: Api, client: AdoClient, ds: dict, state: State, opts: Options,
                 log: Callable[[str], None] = print, sleep: Callable[[float], None] = time.sleep):
        self.api, self.client, self.ds, self.state, self.opts = api, client, ds, state, opts
        self.log, self.sleep = log, sleep
        self.project = ds["project"]["name"]
        self.project_id: str | None = self.state.data.get("project_id")
        self.default_team: dict | None = self.state.data.get("default_team")
        self.process_type_id = AGILE_PROCESS_TYPE_ID
        self.area_nodes: dict[str, dict] | None = None
        self.iter_nodes: dict[str, dict] | None = None
        self.team_ids: dict[str, str] | None = None
        self.query_cache: dict[str, dict] = {}
        self.current_step = ""
        self.step_counts: dict[str, Counter] = OrderedDict()
        self.samples: dict[str, Req] = OrderedDict()
        self.leaf = sprint_leaf_map(ds["calendar"]["iterations"])

    # ------------------------------------------------------------------ plumbing
    def send(self, req: Req, allow=()) -> Resp:
        self.step_counts.setdefault(self.current_step, Counter())[req.label] += 1
        self.samples.setdefault(req.label, req)
        return self.client.send(req, allow=allow)

    def manual(self, key: str, text: str) -> None:
        self.state.section("manual")[key] = text
        self.state.save()
        self.log(f"  MANUAL FOLLOW-UP [{key}]:\n    " + text.replace("\n", "\n    "))

    def run(self, steps: list[str]) -> None:
        for step in steps:
            self.current_step = step
            self.log(f"\n=== {step} ===")
            getattr(self, "step_" + step.replace("-", "_"))()
            done = self.state.data.setdefault("steps_done", [])
            if step not in done:
                done.append(step)
            self.state.save()

    # ------------------------------------------------------------------ lookups
    def ensure_project_loaded(self) -> None:
        if self.project_id and self.default_team:
            return
        r = self.send(self.api.get_project(self.project), allow=(404,))
        if r.status == 404:
            raise StepError(f"Project {self.project!r} does not exist yet; run the 'project' step first.")
        self._remember_project(r.data)

    def _remember_project(self, data: dict) -> None:
        self.project_id = data["id"]
        self.default_team = data.get("defaultTeam")
        self.state.data["project_id"] = self.project_id
        self.state.data["default_team"] = self.default_team
        self.state.save()

    def load_nodes(self, refresh: bool = False) -> None:
        if self.area_nodes is not None and not refresh:
            return
        self.ensure_project_loaded()
        self.area_nodes = self._flatten(self.send(self.api.get_nodes(self.project_id, "Areas")).data)
        self.iter_nodes = self._flatten(self.send(self.api.get_nodes(self.project_id, "Iterations")).data)

    @staticmethod
    def _flatten(root: dict) -> dict[str, dict]:
        """Map relative path ('' = root, 'PI 4\\Sprint 13') -> node, built from names (not 'path')."""
        out: dict[str, dict] = {}

        def walk(node: dict, rel: str) -> None:
            out[rel] = node
            for child in node.get("children", []) or []:
                walk(child, f"{rel}\\{child['name']}" if rel else child["name"])
        walk(root, "")
        return out

    def load_teams(self, refresh: bool = False) -> dict[str, str]:
        if self.team_ids is not None and not refresh:
            return self.team_ids
        self.ensure_project_loaded()
        teams = self.send(self.api.list_teams(self.project_id)).data.get("value", [])
        self.team_ids = {t["name"]: t["id"] for t in teams}
        for t in self.ds["teams"]:
            if t.get("is_default") and self.default_team:
                self.team_ids[t["name"]] = self.default_team["id"]
        return self.team_ids

    def iteration_guid(self, rel: str) -> str:
        self.load_nodes()
        node = self.iter_nodes.get(rel)
        if not node:
            raise StepError(f"Iteration {rel!r} does not exist (run the classification step)")
        return node["identifier"]

    # ------------------------------------------------------------------ preflight
    def step_preflight(self) -> None:
        r = self.send(self.api.connection_data())
        user = (r.data or {}).get("authenticatedUser", {})
        self.log(f"  Authenticated as: {user.get('providerDisplayName', '?')}")
        procs = self.send(self.api.processes()).data.get("value", [])
        agile = next((p for p in procs if p.get("name") == "Agile"), None)
        if not agile:
            raise StepError("The Agile process was not found in this organization.")
        self.process_type_id = agile["id"]
        self.log(f"  Agile process typeId: {self.process_type_id}")
        r = self.send(self.api.get_project(self.project), allow=(404,))
        if r.status == 404:
            self.log(f"  Project {self.project!r} does not exist yet (the 'project' step will create it).")
        else:
            tmpl = r.data.get("capabilities", {}).get("processTemplate", {}).get("templateName")
            self.log(f"  Project {self.project!r} exists (process: {tmpl}).")
            self._remember_project(r.data)
        now = parse_ts(self.ds["now"])
        self.log(f"  Dataset 'now' = {self.ds['now']} (age {(datetime.now(timezone.utc) - now)})")
        self.log("  Permission notes: the PAT owner must be a Project Collection Administrator (create project, "
                 "'Bypass rules on work item updates', 'Suppress notifications for work item updates').")

    # ------------------------------------------------------------------ project
    def step_project(self) -> None:
        r = self.send(self.api.get_project(self.project), allow=(404,))
        if r.status != 404:
            tmpl = r.data.get("capabilities", {}).get("processTemplate", {}).get("templateName")
            if tmpl and tmpl != "Agile":
                raise StepError(f"Project {self.project!r} exists but uses process {tmpl!r}, not Agile.")
            self.log(f"  Project exists: {r.data['id']}")
            self._remember_project(r.data)
            return
        op = self.send(self.api.create_project(self.project, self.ds["project"].get("description", ""),
                                               self.process_type_id)).data
        self.log(f"  Project creation queued (operation {op['id']}); polling...")
        deadline = time.monotonic() + self.opts.project_timeout
        while True:
            status = self.send(self.api.get_operation(op["id"])).data.get("status")
            if status == "succeeded":
                break
            if status in ("failed", "cancelled"):
                raise StepError(f"Project creation {status}. Check Organization settings > Projects.")
            if time.monotonic() > deadline:
                raise StepError("Timed out waiting for project creation; re-run the 'project' step later.")
            self.sleep(self.opts.poll_interval)
        for _ in range(10):  # the project can take a moment to become readable
            r = self.send(self.api.get_project(self.project), allow=(404,))
            if r.status != 404:
                break
            self.sleep(self.opts.poll_interval)
        if r.status == 404:
            raise StepError("Project created but not readable yet; re-run the 'project' step.")
        self._remember_project(r.data)
        self.log(f"  Project created: {self.project_id}")

    # ------------------------------------------------------------------ classification
    def step_classification(self) -> None:
        self.load_nodes(refresh=True)
        created = 0
        for rel in self.ds["areas"]:
            if rel in self.area_nodes:
                continue
            parent, _, name = rel.rpartition("\\")
            node = self.send(self.api.create_node(self.project_id, "Areas", parent, name)).data
            self.area_nodes[rel] = node
            created += 1
        has_items = bool(self.state.data.get("workitems"))
        for it in self.ds["calendar"]["iterations"]:
            rel, start, finish = it["path"], it["start"], it["finish"]
            node = self.iter_nodes.get(rel)
            if node is None:
                parent, _, name = rel.rpartition("\\")
                node = self.send(self.api.create_node(self.project_id, "Iterations", parent, name,
                                                      start, finish)).data
                self.iter_nodes[rel] = node
                created += 1
                continue
            attrs = node.get("attributes") or {}
            if str(attrs.get("startDate", ""))[:10] != start or str(attrs.get("finishDate", ""))[:10] != finish:
                if has_items:
                    self.log(f"  WARNING: changing dates of {rel} after work items exist corrupts history charts.")
                self.send(self.api.update_iteration_dates(self.project_id, rel, start, finish))
                self.log(f"  Updated dates of {rel} -> {start}..{finish}")
        self.log(f"  {created} nodes created; {len(self.ds['areas'])} areas and "
                 f"{len(self.ds['calendar']['iterations'])} iterations present.")

    # ------------------------------------------------------------------ teams
    def step_teams(self, only: list[str] | None = None) -> None:
        self.load_nodes()
        ids = self.load_teams(refresh=True)
        done = self.state.section("teams")
        for t in self.ds["teams"]:
            name = t["name"]
            if only and name not in only:
                continue
            if done.get(name, {}).get("configured"):
                self.log(f"  {name}: already configured (state)")
                continue
            if t.get("is_default"):
                tid = self.default_team["id"]
                if self.default_team.get("name") != name:
                    self.log(f"  WARNING: default team is {self.default_team.get('name')!r}, dataset says {name!r}")
            elif name in ids:
                tid = ids[name]
            else:
                tid = self.send(self.api.create_team(self.project_id, name, t.get("description", ""))).data["id"]
                ids[name] = tid
                self.log(f"  Created team {name}")
            done[name] = {"id": tid}
            self.state.save()
            self.configure_team(t, tid)
            done[name]["configured"] = True
            self.state.save()
        self.log(f"  {len(self.ds['teams']) if not only else len(only)} team(s) configured.")

    def configure_team(self, t: dict, tid: str) -> None:
        pid = self.project_id
        default_area, values = team_area_values(t, self.project)
        self.send(self.api.set_team_field_values(pid, tid, default_area, values))
        existing = {i["id"] for i in self.send(self.api.list_team_iterations(pid, tid)).data.get("value", [])}
        for rel in t.get("iterations", []):
            guid = self.iteration_guid(rel)
            if guid not in existing:
                self.send(self.api.add_team_iteration(pid, tid, guid))
        levels = t.get("backlog_levels", {})
        body = {"backlogIteration": self.iteration_guid(t.get("backlog_iteration", "")),
                "defaultIterationMacro": t.get("default_iteration_macro", "@currentIteration"),
                "bugsBehavior": t.get("bugs_behavior", "asRequirements"),
                "backlogVisibilities": {"Microsoft.EpicCategory": bool(levels.get("epics", False)),
                                        "Microsoft.FeatureCategory": bool(levels.get("features", True)),
                                        "Microsoft.RequirementCategory": bool(levels.get("stories", True))},
                "workingDays": t.get("working_days", ["monday", "tuesday", "wednesday", "thursday", "friday"])}
        self.send(self.api.update_team_settings(pid, tid, body))
        by_iter: dict[str, list[tuple[str, str]]] = OrderedDict()
        for d in t.get("team_days_off", []) or []:
            by_iter.setdefault(d["iteration"], []).append((d["start"], d["end"]))
        for rel, ranges in by_iter.items():
            self.send(self.api.set_team_days_off(pid, tid, self.iteration_guid(rel), ranges))

    # ------------------------------------------------------------------ work items
    def schedule(self) -> list[tuple[int, int]]:
        """(item index, revision index) in application order."""
        ops = [(i, n) for i, wi in enumerate(self.ds["work_items"]) for n in range(len(wi["revisions"]))]
        if self.opts.order == "chronological":
            ops.sort(key=lambda o: (parse_ts(self.ds["work_items"][o[0]]["revisions"][o[1]]["at"]), o[0], o[1]))
        return ops

    def build_patch(self, wi: dict, n: int, parent_id: int | None) -> list[dict]:
        """JSON patch for revision ``n`` (0-based) of dataset item ``wi``."""
        rev = wi["revisions"][n]
        at = ado_ts(rev["at"])
        ops: list[dict] = []
        if n == 0:
            ops.append({"op": "add", "path": "/fields/System.CreatedDate", "value": at})
        ops.append({"op": "add", "path": "/fields/System.ChangedDate", "value": at})
        if self.opts.changed_by:
            if n == 0:
                ops.append({"op": "add", "path": "/fields/System.CreatedBy", "value": self.opts.changed_by})
            ops.append({"op": "add", "path": "/fields/System.ChangedBy", "value": self.opts.changed_by})
        for ref, val in (rev.get("fields") or {}).items():
            if ref in ("System.CreatedDate", "System.ChangedDate", "System.CreatedBy", "System.ChangedBy"):
                continue
            if ref == "System.AssignedTo" and val:
                val = self.opts.assign_map.get(val, val)
            if val is None or val == "" and ref != "System.AssignedTo":
                if n > 0:
                    ops.append({"op": "remove", "path": f"/fields/{ref}"})
                continue
            ops.append({"op": "add", "path": f"/fields/{ref}", "value": val})
        if rev.get("comment"):
            ops.append({"op": "add", "path": "/fields/System.History", "value": rev["comment"]})
        if n == 0 and parent_id is not None and self.opts.parent_links == "create":
            ops.append({"op": "add", "path": "/relations/-",
                        "value": {"rel": PARENT_REL, "url": self.api.work_item_url(parent_id)}})
        return ops

    def step_workitems(self) -> None:
        self.ensure_project_loaded()
        items = self.ds["work_items"]
        st = self.state.section("workitems")
        by_key = {wi["key"]: wi for wi in items}
        if not st and not self.opts.allow_existing_items:
            pilot_ids = {v["id"] for v in self.state.section("pilot").get("items", {}).values()}
            r = self.send(self.api.wiql(self.project_id, "SELECT [System.Id] FROM WorkItems WHERE "
                                        "[System.TeamProject] = @project", top=50))
            found = [w["id"] for w in r.data.get("workItems", []) if w["id"] not in pilot_ids]
            if found:
                raise StepError(f"Project already contains work items (e.g. {found[:5]}) but the state file has no "
                                "work items. Use the state file of the earlier run (--state) to resume, delete the "
                                "project for a clean seed, or pass --allow-existing-items to create duplicates.")
        self._recover_inflight(by_key)
        ops = self.schedule()
        total = len(items)
        created_before = len(st)
        t0 = time.monotonic()
        made = 0
        for i, n in ops:
            wi = items[i]
            key = wi["key"]
            rec = st.get(key)
            if n == 0 and rec:
                continue
            if n > 0 and (not rec or rec["rev"] > n):
                if not rec:
                    raise StepError(f"{key}: revision {n + 1} scheduled before creation (dataset order)")
                continue
            parent_id = None
            if n == 0 and wi.get("parent"):
                prec = st.get(wi["parent"])
                if not prec:
                    raise StepError(f"{key}: parent {wi['parent']} has not been created yet "
                                    f"(order={self.opts.order}); check the dataset ordering")
                parent_id = prec["id"]
            patch = self.build_patch(wi, n, parent_id)
            self.state.data["workitems_inflight"] = {"key": key, "rev": n + 1, "at": wi["revisions"][n]["at"]}
            self.state.save()
            self._write_revision(wi, n, patch, by_key)
            if n == 0:
                made += 1
                done = created_before + made
                if done % 25 == 0 or done == total:
                    rate = made / max(1e-6, time.monotonic() - t0)
                    eta = (total - done) / rate if rate else 0
                    self.log(f"  created {done}/{total} work items ({rate:.2f} items/s, ~{eta / 60:.0f} min left)")
        self.log(f"  {len(st)}/{total} work items present; all revisions applied.")

    def _write_revision(self, wi: dict, n: int, patch: list[dict], by_key: dict[str, dict]) -> None:
        """Send one revision; on a lost response / 5xx check whether it landed before retrying."""
        st = self.state.section("workitems")
        key = wi["key"]
        for attempt in range(4):
            try:
                if n == 0:
                    data = self.send(self.api.create_work_item(self.project_id, wi["type"], patch)).data
                    st[key] = {"id": data["id"], "rev": 1}
                else:
                    self.send(self.api.update_work_item(self.project_id, st[key]["id"], patch))
                    st[key]["rev"] = n + 1
                break
            except AdoError as exc:
                transient = exc.status == 0 or exc.status >= 500
                if transient and attempt < 3:
                    self.log(f"  {key} revision {n + 1}: {('HTTP ' + str(exc.status)) if exc.status else 'network error'}"
                             f"; checking whether the write landed before retrying")
                    self.sleep(2.0 * (attempt + 1))
                    self._recover_inflight(by_key, keep=True)
                    if (n == 0 and key in st) or (n > 0 and st[key]["rev"] >= n + 1):
                        break
                    continue
                self.state.data["workitems_inflight"] = None
                self.state.save()
                title = wi["revisions"][0]["fields"].get("System.Title", "")
                raise StepError(f"Failed on {key} ({wi['type']} {title!r}) revision {n + 1} at "
                                f"{wi['revisions'][n]['at']}:\n{exc}") from exc
        self.state.data["workitems_inflight"] = None
        self.state.save()

    def _recover_inflight(self, by_key: dict[str, dict], keep: bool = False) -> None:
        """After a crash mid-request: find out whether the in-flight write reached the server."""
        inflight = self.state.data.get("workitems_inflight")
        if not inflight:
            return
        st = self.state.section("workitems")
        key, rev_no = inflight["key"], inflight["rev"]
        wi = by_key.get(key)
        if wi is None:
            self.state.data["workitems_inflight"] = None
            return
        at = parse_ts(inflight["at"])
        if rev_no == 1 and key not in st:
            title = wi["revisions"][0]["fields"].get("System.Title", "")
            q = (f"SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = @project AND "
                 f"[System.Title] = {wiql_quote(title)} AND [System.WorkItemType] = {wiql_quote(wi['type'])}")
            for cand in self.send(self.api.wiql(self.project_id, q)).data.get("workItems", []):
                f = self.send(self.api.get_work_item(self.project_id, cand["id"],
                                                     ["System.CreatedDate", "System.ChangedDate"])).data["fields"]
                if parse_ts(f["System.CreatedDate"]) == at:
                    applied = sum(1 for r in wi["revisions"] if parse_ts(r["at"]) <= parse_ts(f["System.ChangedDate"]))
                    st[key] = {"id": cand["id"], "rev": max(1, applied)}
                    self.log(f"  Recovered in-flight creation of {key} as #{cand['id']}")
                    break
        elif key in st and st[key]["rev"] < rev_no:
            f = self.send(self.api.get_work_item(self.project_id, st[key]["id"], ["System.ChangedDate"])).data["fields"]
            if parse_ts(f["System.ChangedDate"]) >= at:
                st[key]["rev"] = rev_no
                self.log(f"  Recovered in-flight revision {rev_no} of {key}")
        if not keep:
            self.state.data["workitems_inflight"] = None
        self.state.save()

    # ------------------------------------------------------------------ links
    def step_links(self) -> None:
        self.ensure_project_loaded()
        st = self.state.section("workitems")
        done = self.state.section("links")
        seen: set[tuple] = set()
        todo: list[tuple[str, str, str, str | None]] = []   # (source key, rel, target key, comment)
        if self.opts.parent_links == "final":
            for wi in self.ds["work_items"]:
                if wi.get("parent"):
                    todo.append((wi["key"], PARENT_REL, wi["parent"], None))
        for wi in self.ds["work_items"]:
            for link in wi.get("links") or []:
                src, tgt, typ = wi["key"], link["target"], link["type"]
                if typ == "Related":
                    canon = ("R",) + tuple(sorted((src, tgt)))
                elif typ == "Predecessor":   # tgt -> src
                    canon = ("D", tgt, src)
                else:                        # Successor: src -> tgt
                    canon = ("D", src, tgt)
                if canon in seen:
                    continue
                seen.add(canon)
                todo.append((src, LINK_REL[typ], tgt, link.get("comment")))
        added = 0
        for src, rel, tgt, comment in todo:
            lk = f"{src}|{rel}|{tgt}"
            if done.get(lk):
                continue
            if src not in st or tgt not in st:
                raise StepError(f"Link {lk}: work items not created yet (run the workitems step)")
            value: dict[str, Any] = {"rel": rel, "url": self.api.work_item_url(st[tgt]["id"])}
            if comment:
                value["attributes"] = {"comment": comment}
            for attempt in range(3):
                try:
                    self.send(self.api.update_work_item(self.project_id, st[src]["id"],
                                                        [{"op": "add", "path": "/relations/-", "value": value}],
                                                        label="links.add"))
                    break
                except AdoError as exc:
                    if "already exists" in exc.message.lower() or exc.code == "TF201035":
                        break
                    if (exc.status == 0 or exc.status >= 500) and attempt < 2:
                        self.sleep(2.0 * (attempt + 1))
                        continue
                    raise
            done[lk] = True
            added += 1
            self.state.save()
        self.log(f"  {added} links added ({len(todo)} total).")

    # ------------------------------------------------------------------ queries
    def participants(self) -> list[dict]:
        out = []
        for t in self.ds["teams"]:
            if t.get("participant"):
                default_area, _ = team_area_values(t, self.project)
                out.append({"participant": t["participant"], "team": t["name"], "sandbox_area": default_area})
        return out

    def expand(self, items: list[dict]) -> list[tuple[dict, dict]]:
        """Yield (item, token map) pairs, multiplying per_participant items."""
        base = {"project": self.project}
        out = []
        for it in items:
            if it.get("per_participant"):
                for p in self.participants():
                    out.append((it, {**base, "participant": p["participant"], "sandbox_area": p["sandbox_area"]}))
            else:
                out.append((it, base))
        return out

    @staticmethod
    def fill(text: str, tokens: dict) -> str:
        return re.sub(r"\{(project|participant|sandbox_area)\}", lambda m: tokens.get(m.group(1), m.group(0)), text)

    def finish_wiql(self, wiql: str) -> str:
        """Inject team ids into @CurrentIteration('[Project]\\Team') macros (UI-saved form)."""
        def repl(m: re.Match) -> str:
            proj, team = m.group(1), m.group(2).strip()
            tid = (self.team_ids or {}).get(team)
            return f"@CurrentIteration('[{proj}]\\{team} <id:{tid}>')" if tid else m.group(0)
        return re.sub(r"@CurrentIteration\('\[([^\]]+)\]\\([^'<]+?)'\)", repl, wiql, flags=re.I)

    def get_query(self, path: str) -> dict | None:
        if path in self.query_cache:
            return self.query_cache[path]
        req = self.api.get_query(self.project_id, path)
        req.params["$expand"] = "wiql"
        r = self.send(req, allow=(404,))
        if r.status == 404:
            return None
        self.query_cache[path] = r.data
        return r.data

    def step_queries(self) -> None:
        self.ensure_project_loaded()
        self.load_teams()
        art = self.ds.get("artifacts") or {}
        st = self.state.section("queries")
        folders_made = queries_made = 0
        for f, tok in self.expand(art.get("query_folders", []) or []):
            path = self.fill(f["path"], tok)
            if self.get_query(path):
                continue
            parent, _, name = path.rpartition("/")
            self._ensure_folder_chain(parent)
            data = self.send(self.api.create_query_item(self.project_id, parent, name)).data
            self.query_cache[path] = data
            st[path] = data["id"]
            folders_made += 1
        for q, tok in self.expand(art.get("queries", []) or []):
            folder = self.fill(q["path"], tok)
            path = f"{folder}/{self.fill(q['name'], tok)}"
            wiql = self.finish_wiql(self.fill(q["wiql"], tok))
            digest = hashlib.sha1(wiql.encode()).hexdigest()
            existing = self.get_query(path)
            if existing:
                # The server may reformat WIQL; only rewrite when OUR desired text changed (or is unknown).
                last = st.get(f"wiql:{path}")
                if last != digest and (existing.get("wiql") or "").strip() != wiql.strip():
                    self.send(self.api.update_query(self.project_id, existing["id"], wiql))
                    existing["wiql"] = wiql
                st[path] = existing["id"]
                st[f"wiql:{path}"] = digest
                continue
            self._ensure_folder_chain(folder)
            data = self.send(self.api.create_query_item(self.project_id, folder, path.rsplit("/", 1)[1], wiql)).data
            data.setdefault("wiql", wiql)
            self.query_cache[path] = data
            st[path] = data["id"]
            st[f"wiql:{path}"] = digest
            queries_made += 1
        self.state.save()
        self.log(f"  {folders_made} folders and {queries_made} queries created.")
        for f in art.get("query_folders", []) or []:
            if f.get("grant_contributors"):
                self._grant_contributors(f["path"])

    def _ensure_folder_chain(self, path: str) -> None:
        parts = path.split("/")
        for i in range(2, len(parts) + 1):
            sub = "/".join(parts[:i])
            if not self.get_query(sub):
                data = self.send(self.api.create_query_item(self.project_id, "/".join(parts[:i - 1]),
                                                            parts[i - 1])).data
                self.query_cache[sub] = data

    def _grant_contributors(self, folder_path: str) -> None:
        """Grant project Contributors Read+Contribute+Manage Permissions on a query folder."""
        key = f"grant:{folder_path}"
        if self.state.section("queries").get(key):
            return
        manual = (f"Boards > Queries > All > Shared Queries > {folder_path.split('/', 1)[1]} > More actions (...) > "
                  f"Security > Add '[{self.project}]\\Contributors' > set Contribute = Allow and Manage Permissions = "
                  f"Allow > Save.")
        try:
            ns = self.send(self.api.security_namespace(QUERY_FOLDER_NAMESPACE)).data["value"][0]
            bits = {a["name"]: a["bit"] for a in ns["actions"]}
            allow = bits["Read"] | bits["Contribute"] | bits["ManagePermissions"]
            scope = self.send(self.api.graph_descriptor(self.project_id)).data["value"]
            groups = self.send(self.api.graph_groups(scope)).data.get("value", [])
            grp = next(g for g in groups if g.get("principalName", "").endswith("\\Contributors"))
            ident = self.send(self.api.identities_by_subject(grp["descriptor"])).data["value"][0]["descriptor"]
            shared = self.get_query("Shared Queries")
            chain = [self.get_query("/".join(folder_path.split("/")[:i]))["id"]
                     for i in range(2, len(folder_path.split("/")) + 1)]
            acls = self.send(self.api.list_acls(QUERY_FOLDER_NAMESPACE, f"$/{self.project_id}")).data.get("value", [])
            base = next((a["token"] for a in acls if a["token"].endswith("/" + shared["id"])),
                        f"$/{self.project_id}/{shared['id']}")
            token = "/".join([base] + chain)
            self.send(self.api.set_aces(QUERY_FOLDER_NAMESPACE, token, ident, allow))
            self.state.section("queries")[key] = token
            self.state.save()
            self.log(f"  Granted Contributors Contribute+Manage Permissions on {folder_path} (token {token}).")
            self.manual(f"verify-{key}", "Verify (UI): " + manual.replace(" > set", ": expect").replace(
                " > Save.", ". (Token format is UNCERTAIN; fix in the UI if not shown.)"))
        except (AdoError, KeyError, StopIteration, IndexError, TypeError) as exc:
            self.manual(key, f"Could not set query folder permissions automatically ({str(exc).splitlines()[0]}). "
                             + manual)

    # ------------------------------------------------------------------ wiki
    def step_wiki(self) -> None:
        self.ensure_project_loaded()
        pages = (self.ds.get("artifacts") or {}).get("wiki_pages", []) or []
        wikis = self.send(self.api.list_wikis(self.project_id)).data.get("value", [])
        wiki = next((w for w in wikis if w.get("type") == "projectWiki"), None)
        if not wiki:
            try:
                wiki = self.send(self.api.create_project_wiki(self.project_id, self.project_id,
                                                              f"{self.project}.wiki")).data
                self.log(f"  Created project wiki {wiki.get('name')}")
            except AdoError as exc:
                wikis = self.send(self.api.list_wikis(self.project_id)).data.get("value", [])
                wiki = next((w for w in wikis if w.get("type") == "projectWiki"), None)
                if not wiki:
                    raise StepError(f"Could not create the project wiki: {exc}") from exc
        st = self.state.section("wiki")
        st["wiki_id"] = wiki["id"]
        changed = 0
        for page in pages:
            path = page["path"]
            content = self.fill((self.opts.content_dir / page["file"]).read_text(encoding="utf-8"),
                                {"project": self.project})
            r = self.send(self.api.get_wiki_page(self.project_id, wiki["id"], path), allow=(404,))
            if r.status == 404:
                self.send(self.api.put_wiki_page(self.project_id, wiki["id"], path, content))
                changed += 1
            elif (r.data or {}).get("content", "").strip() != content.strip():
                etag = r.header("ETag")
                if not etag:
                    raise StepError(f"Wiki page {path} exists but no ETag was returned")
                self.send(self.api.put_wiki_page(self.project_id, wiki["id"], path, content, etag=etag))
                changed += 1
            st[path] = True
        self.state.save()
        self.log(f"  {changed} wiki pages created/updated ({len(pages)} total).")

    # ------------------------------------------------------------------ dashboards
    def step_dashboards(self) -> None:
        self.ensure_project_loaded()
        self.load_nodes()
        teams = self.load_teams()
        st = self.state.section("dashboards")
        for d in (self.ds.get("artifacts") or {}).get("dashboards", []) or []:
            team_id = teams[d["team"]] if d.get("team") else None
            existing = self.send(self.api.list_dashboards(self.project_id, team_id), allow=(404,))
            boards = [] if existing.status == 404 else (existing.data or {}).get("value") or \
                (existing.data or {}).get("dashboardEntries") or []
            hit = next((b for b in boards if b.get("name") == d["name"]), None)
            if hit:
                st[d["name"]] = hit["id"]
                self.log(f"  Dashboard {d['name']!r} exists; left unchanged.")
                continue
            safe, risky = [], []
            for w in d.get("widgets", []) or []:
                try:
                    body = self._widget_body(d, w)
                except StepError as exc:
                    self.manual(f"widget:{d['name']}:{w.get('title')}", f"{exc}\n" + W.manual_widget_steps(d, w))
                    continue
                (safe if w["type"] in W.SAFE else risky).append((w, body))
            if not self.opts.experimental_widgets:
                for w, _ in risky:
                    self.manual(f"widget:{d['name']}:{w.get('title')}", W.manual_widget_steps(d, w))
                risky = []
            body = {"name": d["name"], "description": d.get("description", ""), "widgets": [b for _, b in safe]}
            try:
                dash = self.send(self.api.create_dashboard(self.project_id, team_id, body)).data
                failed = []
            except AdoError as exc:
                self.log(f"  Dashboard create with widgets failed (HTTP {exc.status}); retrying empty, then "
                         f"adding widgets one by one.")
                try:
                    dash = self.send(self.api.create_dashboard(self.project_id, team_id,
                                                               {**body, "widgets": []})).data
                except AdoError as exc2:
                    scope = f"team '{d['team']}'" if d.get("team") else "project (Team Dashboard unchecked)"
                    self.manual(f"dashboard:{d['name']}",
                                f"Dashboard creation failed (HTTP {exc2.status}: {exc2.message[:120]}). Create it "
                                f"in the UI: Overview > Dashboards > New Dashboard > name '{d['name']}', scope "
                                f"{scope} > Create; then add these widgets:\n"
                                + "\n".join(W.manual_widget_steps(d, w) for w in d.get("widgets", [])))
                    continue
                failed = safe
            for w, wbody in failed + risky:
                try:
                    etag = self.send(self.api.get_dashboard(self.project_id, team_id, dash["id"])).data.get("eTag")
                    self.send(self.api.create_widget(self.project_id, team_id, dash["id"],
                                                     {**wbody, "dashboard": {"eTag": etag}}))
                except AdoError as exc:
                    self.manual(f"widget:{d['name']}:{w.get('title')}",
                                f"REST widget creation failed (HTTP {exc.status}).\n" + W.manual_widget_steps(d, w))
            st[d["name"]] = dash["id"]
            self.state.save()
            self.log(f"  Created dashboard {d['name']!r} with {len(safe)} widgets via REST.")

    def _widget_body(self, d: dict, w: dict) -> dict:
        team_name = w.get("team") or d.get("team")
        team_id = (self.team_ids or {}).get(team_name) if team_name else None
        query = None
        if w.get("query"):
            q = self.get_query(w["query"])
            if not q:
                raise StepError(f"Query {w['query']!r} not found (run the queries step first)")
            query = {"id": q["id"], "name": q.get("name", w["query"].rsplit("/", 1)[-1]), "wiql": q.get("wiql", "")}
        iteration = None
        if w.get("iteration"):
            node = self.iter_nodes.get(w["iteration"])
            cal = next((i for i in self.ds["calendar"]["iterations"] if i["path"] == w["iteration"]), None)
            if not node or not cal:
                raise StepError(f"Iteration {w['iteration']!r} not found")
            iteration = {"id": node["identifier"], "path": f"{self.project}\\{w['iteration']}",
                         "start": cal["start"] + "T00:00:00Z", "finish": cal["finish"] + "T00:00:00Z"}
        return W.widget_body(w, project_id=self.project_id, team_id=team_id, query=query, iteration=iteration)

    # ------------------------------------------------------------------ plans
    def step_plans(self) -> None:
        self.ensure_project_loaded()
        teams = self.load_teams()
        st = self.state.section("plans")
        existing = {p["name"]: p["id"] for p in self.send(self.api.list_plans(self.project_id)).data.get("value", [])}
        dates = {leaf: (it["start"], it["finish"]) for leaf, it in self.leaf.items()}
        for plan in (self.ds.get("artifacts") or {}).get("delivery_plans", []) or []:
            if plan["name"] in existing:
                st[plan["name"]] = existing[plan["name"]]
                self.log(f"  Plan {plan['name']!r} exists; left unchanged.")
                continue
            body = W.plan_body(plan, teams, dates)
            try:
                data = self.send(self.api.create_plan(self.project_id, body)).data
            except AdoError as exc:
                self.manual(f"plan:{plan['name']}", self._plan_manual(plan, exc))
                continue
            st[plan["name"]] = data["id"]
            self.state.save()
            self.log(f"  Created plan {plan['name']!r}.")
            if plan.get("markers"):
                self.manual(f"verify-plan:{plan['name']}",
                            f"Open Boards > Delivery Plans > {plan['name']} and confirm the markers "
                            + ", ".join(f"'{m['label']}' ({m['at']} of {m['sprint']})" for m in plan["markers"])
                            + " are visible (marker property names are UNCERTAIN). If not: Settings > Markers > Add.")

    def _plan_manual(self, plan: dict, exc: Exception) -> str:
        teams = ", ".join(f"{t['team']} ({t['backlog'].replace('Microsoft.', '').replace('Category', 's')})"
                          for t in plan["teams"])
        marks = "; ".join(f"{m['label']} on the {m['at']} date of {m['sprint']} ({m['color']})"
                          for m in plan.get("markers", []))
        return (f"REST plan creation failed ({str(exc).splitlines()[0]}). Create it in the UI: Boards > Delivery "
                f"Plans > New plan > name '{plan['name']}'; Teams: {teams}; Create. Then Settings > Markers: {marks}. "
                f"Settings > Fields: show {', '.join(plan.get('card_fields', []))}.")

    # ------------------------------------------------------------------ participants
    def step_participants(self) -> None:
        self.ensure_project_loaded()
        teams = self.load_teams()
        plist = self.participants()
        admin_steps = ("For each participant: Project settings > Teams > 'P## Sandbox' > Settings > Administrators "
                       "> Add > the participant's account > Save. (Team-admin REST API is undocumented.)")
        if not self.opts.participant_map:
            self.manual("participants", "No --participant-map given. For each participant: Organization settings > "
                                        "Users > Add users > email, Access level = Basic, Add to project "
                                        f"'{self.project}' as Contributors. Then add them to their 'P## Sandbox' "
                                        "team (Project settings > Teams > team > Add). " + admin_steps)
            return
        known = {p["participant"]: p for p in plist}
        st = self.state.section("participants")
        for pid, email in self.opts.participant_map:
            if pid not in known:
                self.log(f"  WARNING: {pid} has no sandbox team in the dataset; skipped.")
                continue
            if st.get(pid):
                continue
            try:
                r = self.send(self.api.add_user_entitlement(email, self.project_id)).data
                user = (r.get("userEntitlement") or r.get("operationResult", {}).get("result") or {}).get("user", {})
                descriptor = user.get("descriptor")
                if not descriptor:
                    raise StepError(f"no user descriptor returned for {email}")
                team_desc = self.send(self.api.graph_descriptor(teams[known[pid]["team"]])).data["value"]
                self.send(self.api.add_membership(descriptor, team_desc))
                st[pid] = email
                self.state.save()
                self.log(f"  {pid}: {email} added (Basic, Contributors, member of {known[pid]['team']}).")
            except (AdoError, StepError, KeyError) as exc:
                self.manual(f"participant:{pid}", f"Could not add {email} automatically ({str(exc).splitlines()[0]}). "
                                                  f"Add the user (Basic) and make them a member of "
                                                  f"'{known[pid]['team']}' in the UI.")
        self.manual("participants-admins", admin_steps)

    # ------------------------------------------------------------------ summary
    def step_summary(self) -> None:
        base = f"{self.api.org}/{self.project.replace(' ', '%20')}"
        st = self.state.data
        self.log(f"  Project:     {base}")
        self.log(f"  Boards:      {base}/_boards")
        self.log(f"  Queries:     {base}/_queries")
        self.log(f"  Wiki:        {base}/_wiki")
        self.log(f"  Dashboards:  {base}/_dashboards")
        self.log(f"  Plans:       {base}/_deliveryplans")
        self.log(f"  Created: {len(st.get('workitems', {}))} work items, {len(st.get('links', {}))} links, "
                 f"{len([k for k in st.get('queries', {}) if not k.startswith(('grant:', 'wiql:'))])} queries/folders, "
                 f"{len(st.get('dashboards', {}))} dashboards, {len(st.get('plans', {}))} plans.")
        manual = st.get("manual", {})
        self.log(f"\n  MANUAL FOLLOW-UPS ({len(manual)}):")
        for i, (k, text) in enumerate(sorted(manual.items()), 1):
            self.log(f"  {i:2d}. [{k}] " + text.replace("\n", "\n      "))
        self.log("\n  Always check: Analytics has caught up (velocity for Mobile Banking shows Sprints 9-13), "
                 "and every participant can open the wiki, Shared Queries/Training and their sandbox board.")

    # ------------------------------------------------------------------ pilot
    def step_pilot(self) -> None:
        """Minimal live validation of backdating before the full seed (see README)."""
        from .pilot import run_pilot
        run_pilot(self)

    def step_pilot_cleanup(self) -> None:
        from .pilot import cleanup_pilot
        cleanup_pilot(self)


# =========================================================================== dry-run

def estimate_seconds(counts: dict[str, Counter], max_rps: float) -> float:
    total = sum(sum(c.values()) for c in counts.values())
    per = max(AVG_LATENCY_S, 1.0 / max_rps if max_rps else 0)
    return total * per + (60 if counts.get("project", Counter()).get("project.create") else 0)


def dry_run(ds: dict, opts: Options, steps: list[str], max_rps: float, log=print) -> int:
    from .simulator import AdoSimulator
    sim = AdoSimulator("example", now=datetime.now(timezone.utc))
    client = AdoClient("dry-run-no-pat", transport=sim, max_rps=0, sleep=lambda s: None, log=lambda s: None)
    api = Api("https://dev.azure.com/example")
    prov = Provisioner(api, client, ds, State(None), opts, log=lambda s: None, sleep=lambda s: None)
    try:
        prov.run(steps)
    except (StepError, AdoError) as exc:
        log(f"\nDRY-RUN FAILED in step {prov.current_step!r}:\n{exc}")
        return 1
    log("\nPLAN (executed against the offline simulator; a fresh organization is assumed)")
    total = 0
    for step, c in prov.step_counts.items():
        n = sum(c.values())
        total += n
        detail = ", ".join(f"{k} x{v}" for k, v in c.most_common())
        log(f"  {step:<13} {n:6d} requests  ({detail})")
    secs = estimate_seconds(prov.step_counts, max_rps)
    log(f"  {'TOTAL':<13} {total:6d} requests; estimated runtime {secs / 60:.0f} min "
        f"(~{AVG_LATENCY_S}s per request, sequential, <= {max_rps:g} req/s)")
    log("\nSAMPLE REQUESTS (one per kind, bodies redacted/truncated):")
    for label, req in prov.samples.items():
        hdr = {k: v for k, v in req.headers.items()}
        log(f"  [{label}] {req.method} {req.full_url()}" + (f"  headers={hdr}" if hdr else ""))
        if req.body is not None:
            log("      " + json.dumps(redact(req.body), ensure_ascii=False)[:700])
    manual = prov.state.data.get("manual", {})
    log(f"\nMANUAL FOLLOW-UPS that a live run would print ({len(manual)}):")
    for k, text in sorted(manual.items()):
        log(f"  - [{k}] " + text.splitlines()[0][:220])
    return 0


# =========================================================================== CLI

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m harborpoint.provision",
        description="Provision the HarborPoint Azure DevOps training project from out/dataset.json.",
        epilog=PAT_SCOPES + "\n\nSteps: " + ", ".join(STEPS) + "  (special: pilot, pilot-cleanup)",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--org", required=True, help="https://dev.azure.com/ORG")
    p.add_argument("--project", help="project name (default: dataset project.name)")
    p.add_argument("--dataset", default="out/dataset.json")
    p.add_argument("--content-dir", default=str(ENV_DIR / "content"), help="where wiki page files live")
    p.add_argument("--pat-file", help=f"file holding the PAT (default {DEFAULT_PAT_FILE}, or env AZDO_PAT)")
    p.add_argument("--dry-run", action="store_true", help="no network: validate and print the request plan")
    p.add_argument("--steps", default="all", help="comma list of steps, 'all', 'pilot' or 'pilot-cleanup'")
    p.add_argument("--state", default="out/state.json", help="resume state file")
    p.add_argument("--assign-map", help="CSV 'name,identity' mapping fictional display names to identities")
    p.add_argument("--participant-map", help="CSV 'participant,email' (adds users to P## Sandbox teams)")
    p.add_argument("--yes", action="store_true", help="do not ask for confirmation")
    p.add_argument("--order", choices=["item", "chronological"], default="item",
                   help="revision application order (the pilot tells which one is safe)")
    p.add_argument("--parent-links", choices=["create", "final"], default="create",
                   help="parent link in revision 1 (create) or in the links step (final)")
    p.add_argument("--changed-by", help="set System.ChangedBy/CreatedBy to this value (only if VS403417 occurs)")
    p.add_argument("--experimental-widgets", action="store_true",
                   help="also try burndown/CFD/cycle/lead-time widgets via REST (settings JSON is undocumented)")
    p.add_argument("--allow-existing-items", action="store_true",
                   help="create work items even if the project has items the state file does not know")
    p.add_argument("--pilot-team", help="team used by the pilot (default: first delivery team)")
    p.add_argument("--max-rps", type=float, default=8.0, help="request pacing (default 8/s)")
    return p


def resolve_steps(spec: str) -> list[str]:
    if spec in ("all", ""):
        return list(STEPS)
    steps = [s.strip() for s in spec.split(",") if s.strip()]
    bad = [s for s in steps if s not in STEPS + SPECIAL_STEPS]
    if bad:
        raise StepError(f"Unknown step(s): {', '.join(bad)}. Valid: {', '.join(STEPS + SPECIAL_STEPS)}")
    if any(s in SPECIAL_STEPS for s in steps) and len(steps) > 1:
        raise StepError("pilot / pilot-cleanup must be run on their own")
    return sorted(steps, key=lambda s: (STEPS + SPECIAL_STEPS).index(s))


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        steps = resolve_steps(args.steps)
        ds_path = Path(args.dataset)
        if not ds_path.is_file():
            raise StepError(f"Dataset {ds_path} not found. Run: python -m harborpoint.generate")
        ds = json.loads(ds_path.read_text(encoding="utf-8"))
        if args.project:
            retarget_project(ds, args.project)
        opts = Options(content_dir=Path(args.content_dir), order=args.order, parent_links=args.parent_links,
                       changed_by=args.changed_by, experimental_widgets=args.experimental_widgets,
                       allow_existing_items=args.allow_existing_items, pilot_team=args.pilot_team,
                       dry_run=args.dry_run)
        opts.assign_map = dict(read_csv_map(args.assign_map, ("name", "identity")))
        opts.participant_map = read_csv_map(args.participant_map, ("participant", "email"))
        if args.project and args.project != "HarborPoint":
            print(f"NOTE: --project {args.project}: work item paths were retargeted, but WIQL/wiki text that "
                  f"hard-codes 'HarborPoint\\...' will not match. Use a separate project only for the pilot.")
        report: Report = validate(ds, opts.content_dir, order=opts.order)
        for w in report.warnings[:40]:
            print(f"WARNING: {w}")
        if len(report.warnings) > 40:
            print(f"WARNING: ... {len(report.warnings) - 40} more warnings")
        for e in report.errors:
            print(f"ERROR: {e}")
        print(f"Dataset: {report.stats} -> {'OK' if report.ok else f'{len(report.errors)} error(s)'}")
        if not report.ok:
            return 1
        Api(args.org)  # validates the org URL
        if args.dry_run:
            return dry_run(ds, opts, steps if steps != ["pilot-cleanup"] else [], args.max_rps)
        pat = read_pat(args.pat_file)
        state_path = Path(args.state)
        state = State.load(state_path)
        if state.data.get("org") and state.data.get("org") != args.org.rstrip("/"):
            raise StepError(f"State file {state_path} belongs to {state.data['org']}; use another --state.")
        if state.data.get("project") and state.data.get("project") != ds["project"]["name"]:
            raise StepError(f"State file {state_path} belongs to project {state.data['project']}; use another --state.")
        state.data.update(org=args.org.rstrip("/"), project=ds["project"]["name"])
        if not args.yes:
            if not sys.stdin.isatty():
                raise StepError("Refusing to modify Azure DevOps without --yes in a non-interactive shell.")
            answer = input(f"About to run {', '.join(steps)} against {args.org} project "
                           f"{ds['project']['name']!r}. Type the project name to continue: ")
            if answer.strip() != ds["project"]["name"]:
                print("Aborted.")
                return 1
        client = AdoClient(pat, max_rps=args.max_rps)
        prov = Provisioner(Api(args.org), client, ds, state, opts)
        t0 = time.monotonic()
        prov.run(steps)
        print(f"\nDone in {(time.monotonic() - t0) / 60:.1f} min ({client.count} requests).")
        return 0
    except (StepError, AdoError, ValueError) as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\nInterrupted; state saved. Re-run the same command to resume.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())

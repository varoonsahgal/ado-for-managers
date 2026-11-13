"""Offline validation of a ``harborpoint-dataset/1`` file before provisioning.

``validate(dataset, content_dir)`` returns a :class:`Report` with ``errors`` (block
provisioning) and ``warnings`` (worth a look). It checks the DATASET CONTRACT: schema,
revision ordering, nothing after ``now``, parents before children, every path used in
fields/teams/artifacts exists, link targets exist, field names plausible, and that every
artifact reference (query paths, teams, iterations, wiki files) resolves.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "harborpoint-dataset/1"
WIT_STATES = {
    "Epic": {"New", "Active", "Resolved", "Closed", "Removed"},
    "Feature": {"New", "Active", "Resolved", "Closed", "Removed"},
    "User Story": {"New", "Active", "Resolved", "Closed", "Removed"},
    "Bug": {"New", "Active", "Resolved", "Closed"},
}
PARENT_TYPES = {"Epic": set(), "Feature": {"Epic"}, "User Story": {"Feature"}, "Bug": {"Feature"}}
LINK_TYPES = {"Predecessor", "Successor", "Related"}
FIELD_RE = re.compile(r"^(System|Microsoft\.VSTS|Custom)\.[A-Za-z][A-Za-z0-9_.]*$")
KNOWN_VALUES = {
    "Microsoft.VSTS.Common.Risk": {"1 - High", "2 - Medium", "3 - Low"},
    "Microsoft.VSTS.Common.Severity": {"1 - Critical", "2 - High", "3 - Medium", "4 - Low"},
    "Microsoft.VSTS.Common.ValueArea": {"Business", "Architectural"},
}
DATE_FIELDS = {"Microsoft.VSTS.Common.ActivatedDate", "Microsoft.VSTS.Common.ResolvedDate",
               "Microsoft.VSTS.Common.ClosedDate", "Microsoft.VSTS.Common.StateChangeDate",
               "Microsoft.VSTS.Scheduling.StartDate", "Microsoft.VSTS.Scheduling.TargetDate"}
WIDGET_TYPES = {"markdown", "query_tile", "query_results", "chart", "velocity", "sprint_burndown", "cfd",
                "cycle_time", "lead_time"}
TEAM_WIDGETS = {"velocity", "sprint_burndown", "cfd", "cycle_time", "lead_time"}
QUERY_WIDGETS = {"query_tile", "query_results", "chart"}
BACKLOG_CATEGORIES = {"Microsoft.EpicCategory", "Microsoft.FeatureCategory", "Microsoft.RequirementCategory"}
WIQL_TOKENS = {"project", "participant", "sandbox_area"}
BAD_NODE_CHARS = set('\\/:*?"<>|#$&+')
BAD_TEAM_CHARS = set('\\/:*?"<>;#$*{},+=[]|')


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    stats: dict[str, Any] = field(default_factory=dict)

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    @property
    def ok(self) -> bool:
        return not self.errors


def parse_ts(value: Any) -> datetime:
    s = str(value).strip().replace("Z", "+00:00")
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        raise ValueError(f"timestamp without timezone: {value!r}")
    return dt.astimezone(timezone.utc)


def team_area_values(team: dict, project: str) -> tuple[str, list[tuple[str, bool]]]:
    """Return (default_area_full_path, [(full_path, include_children)]) for a team object.

    Supports the multi-area form ``areas: [{path, include_children}]`` + ``default_area`` and
    falls back to the single ``area`` / ``include_sub_areas`` fields.
    """
    def full(rel: str) -> str:
        rel = (rel or "").strip("\\")
        if rel == project or rel.startswith(project + "\\"):
            return rel
        return project + ("\\" + rel if rel else "")

    if team.get("areas"):
        values = [(full(a.get("path", "")), bool(a.get("include_children", a.get("includeChildren", False))))
                  for a in team["areas"]]
        default = full(team["default_area"]) if "default_area" in team else values[0][0]
        return default, values
    area = full(team.get("area", ""))
    return area, [(area, bool(team.get("include_sub_areas", False)))]


def sprint_leaf_map(calendar_iterations: list[dict]) -> dict[str, dict]:
    """'Sprint 16' -> iteration entry (leaf name lookup used by plan markers)."""
    return {it["path"].split("\\")[-1]: it for it in calendar_iterations}


def expand_participants(dataset: dict) -> list[str]:
    return [t["participant"] for t in dataset.get("teams", []) if t.get("participant")]


def validate(ds: dict, content_dir: Path | None = None, *, wall_now: datetime | None = None,
             order: str = "item") -> Report:
    r = Report()
    if ds.get("schema") != SCHEMA:
        r.err(f"schema must be {SCHEMA!r} (got {ds.get('schema')!r})")
    for key in ("now", "project", "calendar", "areas", "teams", "work_items"):
        if key not in ds:
            r.err(f"missing top-level key {key!r}")
    if r.errors:
        return r
    project = ds["project"].get("name", "")
    if not project or set(project) & set('\\/:*?"\'<>;#$*{},+=[]|'):
        r.err(f"invalid project name {project!r}")
    if ds["project"].get("process") != "Agile":
        r.err("project.process must be 'Agile'")
    try:
        now = parse_ts(ds["now"])
    except Exception as exc:  # noqa: BLE001
        r.err(f"bad 'now': {exc}")
        return r
    wall_now = wall_now or datetime.now(timezone.utc)
    if now > wall_now:
        r.err(f"dataset 'now' ({ds['now']}) is in the future; regenerate the dataset or wait")
    elif (wall_now - now).total_seconds() > 2 * 86400:
        r.warn(f"dataset 'now' is {(wall_now - now).days} days old; the class 'now' (Sprint 14 week 2) will "
               f"drift. Regenerate before seeding.")

    # ---- calendar / areas
    iters = ds["calendar"].get("iterations", [])
    it_paths: set[str] = set()
    for it in iters:
        path = it.get("path", "")
        parent = path.rsplit("\\", 1)[0] if "\\" in path else ""
        if parent and parent not in it_paths:
            r.err(f"iteration {path!r} listed before its parent {parent!r}")
        leaf = path.split("\\")[-1]
        if not leaf or BAD_NODE_CHARS & set(leaf.replace("\\", "")):
            r.err(f"invalid iteration name {path!r}")
        try:
            s, f = it["start"], it["finish"]
            if datetime.fromisoformat(s) > datetime.fromisoformat(f):
                r.err(f"iteration {path} starts after it finishes")
        except Exception:  # noqa: BLE001
            r.err(f"iteration {path!r} needs start/finish YYYY-MM-DD")
        it_paths.add(path)
    area_paths: set[str] = set()
    for a in ds["areas"]:
        parent = a.rsplit("\\", 1)[0] if "\\" in a else ""
        if parent and parent not in area_paths:
            r.err(f"area {a!r} listed before its parent {parent!r}")
        if BAD_NODE_CHARS & set(a.split("\\")[-1]):
            r.err(f"invalid area name {a!r}")
        area_paths.add(a)
    full_areas = {project} | {f"{project}\\{a}" for a in area_paths}
    full_iters = {project} | {f"{project}\\{i}" for i in it_paths}

    # ---- teams
    team_names: set[str] = set()
    defaults = 0
    for t in ds["teams"]:
        name = t.get("name", "")
        if not name or len(name) > 64 or BAD_TEAM_CHARS & set(name) or name.startswith("_"):
            r.err(f"invalid team name {name!r}")
        if name in team_names:
            r.err(f"duplicate team {name!r}")
        team_names.add(name)
        defaults += bool(t.get("is_default"))
        default_area, values = team_area_values(t, project)
        for v, _ in values:
            if v not in full_areas:
                r.err(f"team {name}: area {v!r} does not exist")
        if default_area not in {v for v, _ in values}:
            r.err(f"team {name}: default area {default_area!r} is not one of its areas")
        for ip in t.get("iterations", []):
            if ip not in it_paths:
                r.err(f"team {name}: iteration {ip!r} does not exist")
        if t.get("backlog_iteration", "") not in ("", *it_paths):
            r.err(f"team {name}: backlog iteration {t['backlog_iteration']!r} does not exist")
        if t.get("bugs_behavior", "asRequirements") not in ("off", "asRequirements", "asTasks"):
            r.err(f"team {name}: bad bugs_behavior")
        for d in t.get("team_days_off", []):
            if d.get("iteration") not in t.get("iterations", []):
                r.err(f"team {name}: day off in {d.get('iteration')!r}, which the team does not select")
            it = next((i for i in iters if i["path"] == d.get("iteration")), None)
            if it and not (it["start"] <= d["start"] <= d["end"] <= it["finish"]):
                r.err(f"team {name}: day off {d['start']}..{d['end']} outside {it['path']}")
    if defaults != 1:
        r.err(f"exactly one team must have is_default=true (found {defaults})")

    # ---- work items
    keys: dict[str, dict] = {}
    rev_count = 0
    first_at: dict[str, datetime] = {}
    for idx, wi in enumerate(ds["work_items"]):
        key = wi.get("key")
        where = f"work item {key or '#' + str(idx)}"
        if not key or key in keys:
            r.err(f"{where}: missing or duplicate key")
            continue
        wit = wi.get("type")
        if wit not in WIT_STATES:
            r.err(f"{where}: unknown type {wit!r}")
            continue
        parent = wi.get("parent")
        if parent is not None:
            if parent not in keys:
                r.err(f"{where}: parent {parent!r} missing or listed after the child")
            elif keys[parent]["type"] not in PARENT_TYPES[wit]:
                r.warn(f"{where}: unusual parent type {keys[parent]['type']} for {wit}")
        revs = wi.get("revisions") or []
        if not revs:
            r.err(f"{where}: no revisions")
            keys[key] = wi
            continue
        prev = None
        state = None
        for n, rev in enumerate(revs, 1):
            rev_count += 1
            try:
                at = parse_ts(rev["at"])
            except Exception as exc:  # noqa: BLE001
                r.err(f"{where} rev {n}: bad 'at' ({exc})")
                continue
            if prev and at <= prev:
                r.err(f"{where} rev {n}: 'at' {rev['at']} is not after the previous revision")
            if at > now:
                r.err(f"{where} rev {n}: 'at' {rev['at']} is after dataset now {ds['now']}")
            if at.weekday() >= 5:
                r.warn(f"{where} rev {n}: event on a weekend ({rev['at']})")
            prev = at
            fields = rev.get("fields") or {}
            if n == 1:
                first_at[key] = at
                if not fields.get("System.Title"):
                    r.err(f"{where}: revision 1 needs System.Title")
                if "Microsoft.VSTS.Common.StackRank" not in fields:
                    r.warn(f"{where}: revision 1 has no StackRank")
            for ref, val in fields.items():
                if not FIELD_RE.match(ref):
                    r.err(f"{where} rev {n}: implausible field name {ref!r}")
                if ref == "System.CreatedDate" and n > 1:
                    r.err(f"{where} rev {n}: System.CreatedDate can only be set on revision 1")
                if ref in ("System.CreatedDate", "System.ChangedDate") and val is not None and \
                        parse_ts(val) != at:
                    r.err(f"{where} rev {n}: {ref} differs from 'at'")
                if ref == "System.AreaPath" and val not in full_areas:
                    r.err(f"{where} rev {n}: area {val!r} does not exist")
                if ref == "System.IterationPath" and val not in full_iters:
                    r.err(f"{where} rev {n}: iteration {val!r} does not exist")
                if ref == "System.State":
                    if val not in WIT_STATES[wit]:
                        r.err(f"{where} rev {n}: state {val!r} invalid for {wit}")
                    state = val
                if ref in KNOWN_VALUES and val not in KNOWN_VALUES[ref] and val is not None:
                    r.err(f"{where} rev {n}: {ref}={val!r} not an allowed value")
                if ref == "Microsoft.VSTS.Common.Priority" and val is not None and val not in (1, 2, 3, 4):
                    r.err(f"{where} rev {n}: Priority {val!r} not in 1..4")
                if ref in DATE_FIELDS and val is not None:
                    try:
                        if parse_ts(val) > now and ref not in ("Microsoft.VSTS.Scheduling.StartDate",
                                                               "Microsoft.VSTS.Scheduling.TargetDate"):
                            r.err(f"{where} rev {n}: {ref} is after now")
                    except Exception:  # noqa: BLE001
                        r.err(f"{where} rev {n}: {ref} is not an ISO timestamp")
                if ref.endswith("By") and ref.startswith("Microsoft.VSTS.Common.") and val:
                    r.warn(f"{where} rev {n}: {ref} set; By fields with fictional names may be rejected")
            if n == 1 and state is None:
                r.warn(f"{where}: revision 1 has no System.State (server default 'New')")
        if order == "chronological" and parent in first_at and key in first_at and \
                first_at[key] < first_at[parent]:
            r.err(f"{where}: created before its parent {parent} (chronological order needs parent first)")
        keys[key] = wi
    for wi in ds["work_items"]:
        for link in wi.get("links", []) or []:
            if link.get("type") not in LINK_TYPES:
                r.err(f"work item {wi.get('key')}: bad link type {link.get('type')!r}")
            if link.get("target") not in keys:
                r.err(f"work item {wi.get('key')}: link target {link.get('target')!r} does not exist")
            if link.get("target") == wi.get("key"):
                r.err(f"work item {wi.get('key')}: self link")

    # ---- artifacts
    validate_artifacts(ds.get("artifacts") or {}, r, project=project, teams=team_names, it_paths=it_paths,
                       iters=iters, participants=expand_participants(ds), content_dir=content_dir)
    r.stats.update(work_items=len(keys), revisions=rev_count,
                   links=sum(len(w.get("links") or []) for w in ds["work_items"]),
                   teams=len(ds["teams"]), areas=len(ds["areas"]), iterations=len(iters))
    return r


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"\{([a-z_]+)\}", text))


def validate_artifacts(a: dict, r: Report, *, project: str, teams: set[str], it_paths: set[str],
                       iters: list[dict], participants: list[str], content_dir: Path | None) -> None:
    folders: set[str] = set()
    for f in a.get("query_folders", []) or []:
        path = f.get("path", "")
        if not path.startswith("Shared Queries/"):
            r.err(f"query folder {path!r} must start with 'Shared Queries/'")
        parent = path.rsplit("/", 1)[0]
        if parent != "Shared Queries" and parent not in folders:
            r.err(f"query folder {path!r} listed before its parent")
        if "{participant}" in path and not f.get("per_participant"):
            r.err(f"query folder {path!r} uses {{participant}} but per_participant is not true")
        folders.add(path)
    queries: set[str] = set()
    for q in a.get("queries", []) or []:
        path, name, wiql = q.get("path", ""), q.get("name", ""), q.get("wiql", "")
        if path != "My Queries" and path not in folders:
            r.err(f"query {name!r}: folder {path!r} is not defined in query_folders")
        if re.search(r'[/\\<>*?"+|:]', name) or not name:
            r.err(f"query name {name!r} is invalid")
        bad = _tokens(wiql) - WIQL_TOKENS
        if bad:
            r.err(f"query {name!r}: unknown tokens {sorted(bad)}")
        if ("{participant}" in path + wiql or "{sandbox_area}" in wiql) and not q.get("per_participant"):
            r.err(f"query {name!r} uses participant tokens but per_participant is not true")
        if not re.match(r"\s*SELECT\b", wiql, re.I):
            r.err(f"query {name!r}: WIQL must start with SELECT")
        if "WorkItemLinks" in wiql and "MODE (" not in wiql:
            r.err(f"query {name!r}: link query without MODE (...)")
        if "@project" not in wiql:
            r.warn(f"query {name!r}: no [System.TeamProject] = @project clause")
        full = f"{path}/{name}"
        if full in queries:
            r.err(f"duplicate query {full!r}")
        queries.add(full)
        if q.get("per_participant") and not participants:
            r.warn(f"query {name!r} is per_participant but the dataset has no participant teams")
    for page in a.get("wiki_pages", []) or []:
        p = page.get("path", "")
        if not p.startswith("/") or "#" in p or p.endswith("."):
            r.err(f"wiki page path {p!r} is invalid")
        if content_dir is not None:
            f = content_dir / page.get("file", "")
            if not f.is_file():
                r.err(f"wiki page {p!r}: file {f} not found")
    seen_pages: set[str] = set()
    for page in a.get("wiki_pages", []) or []:
        parent = page["path"].rsplit("/", 1)[0]
        if parent and parent not in seen_pages:
            r.warn(f"wiki page {page['path']!r} has no parent page listed before it ({parent!r})")
        seen_pages.add(page["path"])
    leaf_map = sprint_leaf_map(iters)
    for d in a.get("dashboards", []) or []:
        if d.get("team") and d["team"] not in teams:
            r.err(f"dashboard {d.get('name')!r}: team {d['team']!r} does not exist")
        cells: dict[tuple[int, int], str] = {}
        for w in d.get("widgets", []) or []:
            t = w.get("type")
            title = w.get("title", "?")
            if t not in WIDGET_TYPES:
                r.err(f"dashboard {d['name']!r}: unknown widget type {t!r}")
                continue
            if t in QUERY_WIDGETS and w.get("query") not in queries:
                r.err(f"dashboard {d['name']!r} widget {title!r}: query {w.get('query')!r} is not defined")
            if t in TEAM_WIDGETS:
                if (w.get("team") or d.get("team")) not in teams:
                    r.err(f"dashboard {d['name']!r} widget {title!r}: team {w.get('team')!r} does not exist")
            if t == "sprint_burndown" and w.get("iteration") not in it_paths:
                r.err(f"dashboard {d['name']!r} widget {title!r}: iteration {w.get('iteration')!r} does not exist")
            row, col = int(w.get("row", 0)), int(w.get("column", 0))
            rs, cs = int(w.get("row_span", 1)), int(w.get("column_span", 1))
            if row < 1 or col < 1 or col + cs - 1 > 10:
                r.err(f"dashboard {d['name']!r} widget {title!r}: position outside the 10-column grid")
            for rr in range(row, row + rs):
                for cc in range(col, col + cs):
                    if (rr, cc) in cells:
                        r.err(f"dashboard {d['name']!r}: widgets {cells[(rr, cc)]!r} and {title!r} overlap")
                    cells[(rr, cc)] = title
    for plan in a.get("delivery_plans", []) or []:
        tl = plan.get("teams", [])
        if len(tl) > 15:
            r.warn(f"plan {plan['name']!r}: more than 15 teams")
        for t in tl:
            if t.get("team") not in teams:
                r.err(f"plan {plan['name']!r}: team {t.get('team')!r} does not exist")
            if t.get("backlog") not in BACKLOG_CATEGORIES:
                r.err(f"plan {plan['name']!r}: backlog {t.get('backlog')!r} invalid")
        for m in plan.get("markers", []) or []:
            if m.get("sprint") not in leaf_map:
                r.err(f"plan {plan['name']!r}: marker sprint {m.get('sprint')!r} does not exist")
            if m.get("at") not in ("start", "end"):
                r.err(f"plan {plan['name']!r}: marker 'at' must be start|end")
            if not re.fullmatch(r"#[0-9a-fA-F]{6}", str(m.get("color", "#000000"))):
                r.err(f"plan {plan['name']!r}: marker color must be #rrggbb")

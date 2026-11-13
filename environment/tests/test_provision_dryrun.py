"""Offline tests for the HarborPoint provisioner (no network: HTTP is the in-memory simulator).

Run: cd environment && ../.venv/bin/python -m unittest discover -s tests -v
"""
from __future__ import annotations

import base64
import contextlib
import io
import json
import socket
import sys
import tempfile
import unittest
import unittest.mock
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ENV = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENV))

from harborpoint import provision as P  # noqa: E402
from harborpoint.ado import AdoClient, AdoError, Api, Req  # noqa: E402
from harborpoint.dataset_check import validate  # noqa: E402
from harborpoint.simulator import AdoSimulator, _parse_dt  # noqa: E402

ORG = "https://dev.azure.com/example"


def _ts(d: date, hh: int, mm: int = 0) -> str:
    return datetime(d.year, d.month, d.day, hh, mm, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def fixture_dataset() -> dict:
    """Small dataset positioned so that 'now' is in Sprint 14 week 2 (relative to today)."""
    today = datetime.now(timezone.utc).date()
    s14 = today - timedelta(days=today.weekday() + 7)          # Monday of last week
    s13 = s14 - timedelta(days=14)
    s15 = s14 + timedelta(days=14)
    fri = lambda d: d + timedelta(days=11)
    now = datetime.now(timezone.utc) - timedelta(minutes=5)
    day = lambda start, n: start + timedelta(days=(n - 1) + 2 * ((n - 1) // 5))
    iters = [{"path": "PI 4", "start": s13.isoformat(), "finish": fri(s15).isoformat()},
             {"path": "PI 4\\Sprint 13", "start": s13.isoformat(), "finish": fri(s13).isoformat()},
             {"path": "PI 4\\Sprint 14", "start": s14.isoformat(), "finish": fri(s14).isoformat()},
             {"path": "PI 4\\Sprint 15", "start": s15.isoformat(), "finish": fri(s15).isoformat()}]
    team_common = {"iteration": None, "backlog_iteration": "", "default_iteration_macro": "@currentIteration",
                   "bugs_behavior": "asRequirements",
                   "working_days": ["monday", "tuesday", "wednesday", "thursday", "friday"]}
    teams = [
        {"name": "HarborPoint Team", "description": "Program", "is_default": True,
         "areas": [{"path": "", "include_children": False}, {"path": "Digital", "include_children": True},
                   {"path": "Member Support", "include_children": True}], "default_area": "",
         "iterations": ["PI 4\\Sprint 13", "PI 4\\Sprint 14", "PI 4\\Sprint 15"],
         "backlog_levels": {"epics": True, "features": True, "stories": True}, "team_days_off": [],
         "participant": None},
        {"name": "Mobile Banking", "description": "Delivery team", "is_default": False,
         "area": "Digital\\Mobile Banking", "include_sub_areas": False,
         "iterations": ["PI 4\\Sprint 13", "PI 4\\Sprint 14", "PI 4\\Sprint 15"],
         "backlog_levels": {"epics": False, "features": True, "stories": True},
         "team_days_off": [{"iteration": "PI 4\\Sprint 15", "start": day(s15, 3).isoformat(),
                            "end": day(s15, 4).isoformat()}], "participant": None},
        {"name": "Member Support", "description": "Delivery team", "is_default": False,
         "area": "Member Support", "include_sub_areas": False,
         "iterations": ["PI 4\\Sprint 13", "PI 4\\Sprint 14", "PI 4\\Sprint 15"],
         "backlog_levels": {"epics": False, "features": True, "stories": True}, "team_days_off": [],
         "participant": None},
        {"name": "P01 Sandbox", "description": "Participant sandbox", "is_default": False,
         "area": "Training\\P01", "include_sub_areas": True, "iterations": ["PI 4\\Sprint 15"],
         "backlog_levels": {"epics": False, "features": True, "stories": True}, "team_days_off": [],
         "participant": "P01"},
    ]
    for t in teams:
        t.update({k: v for k, v in team_common.items() if k not in t and v is not None})
    mb = "HarborPoint\\Digital\\Mobile Banking"

    def story(key, title, pts, rank, offset):
        return {"key": key, "type": "User Story", "parent": "F1", "links": [], "revisions": [
            {"at": _ts(s13 - timedelta(days=3), 16, offset),
             "fields": {"System.Title": title, "System.State": "New", "System.Reason": "New", "System.AreaPath": mb,
                        "System.IterationPath": "HarborPoint", "System.AssignedTo": "Hannah Cole",
                        "Microsoft.VSTS.Scheduling.StoryPoints": pts, "Microsoft.VSTS.Common.StackRank": rank}},
            {"at": _ts(s13, 16, 10 + offset), "fields": {
                "System.IterationPath": "HarborPoint\\PI 4\\Sprint 13", "System.State": "Active",
                "System.Reason": "Implementation started",
                "Microsoft.VSTS.Common.ActivatedDate": _ts(s13, 16, 10 + offset),
                "Microsoft.VSTS.Common.StateChangeDate": _ts(s13, 16, 10 + offset)},
             "comment": "Started."},
            {"at": _ts(day(s13, 6), 17, offset), "fields": {
                "System.State": "Closed", "System.Reason": "Acceptance tests pass",
                "Microsoft.VSTS.Common.ClosedDate": _ts(day(s13, 6), 17, offset),
                "Microsoft.VSTS.Common.StateChangeDate": _ts(day(s13, 6), 17, offset)}}]}

    work_items = [
        {"key": "E1", "type": "Epic", "parent": None, "links": [], "revisions": [
            {"at": _ts(s13 - timedelta(days=14), 16), "fields": {
                "System.Title": "Digital Banking Modernization", "System.State": "New", "System.AreaPath": "HarborPoint",
                "System.IterationPath": "HarborPoint", "Microsoft.VSTS.Common.StackRank": 1000.0}}]},
        {"key": "F1", "type": "Feature", "parent": "E1", "links": [{"type": "Related", "target": "E1"}], "revisions": [
            {"at": _ts(s13 - timedelta(days=7), 16), "fields": {
                "System.Title": "Mobile Check Deposit", "System.State": "New", "System.AreaPath": mb,
                "System.IterationPath": "HarborPoint\\PI 4", "System.Tags": "PI4-Committed",
                "Microsoft.VSTS.Common.Risk": "2 - Medium", "Microsoft.VSTS.Common.StackRank": 2000.0}},
            {"at": _ts(s13, 16, 30), "fields": {
                "System.State": "Active", "System.Reason": "Implementation started",
                "Microsoft.VSTS.Common.ActivatedDate": _ts(s13, 16, 30),
                "Microsoft.VSTS.Common.StateChangeDate": _ts(s13, 16, 30)}}]},
        story("S1", "Capture check image", 5, 3000.0, 1),
        story("S2", "Endorsement validation", 3, 3001.0, 2),
    ]
    work_items[3]["links"] = [{"type": "Predecessor", "target": "S1", "comment": "needs image capture"}]
    work_items[2]["links"] = [{"type": "Successor", "target": "S2"}]   # same link from the other side
    artifacts = {
        "query_folders": [{"path": "Shared Queries/HarborPoint Reports"},
                          {"path": "Shared Queries/Training", "grant_contributors": True},
                          {"path": "Shared Queries/Training/{participant}", "per_participant": True},
                          {"path": "Shared Queries/Training/{participant}/Lab 11 - Inherited queries",
                           "per_participant": True}],
        "queries": [
            {"path": "Shared Queries/HarborPoint Reports", "name": "Program - Current sprint (all teams)",
             "wiql": "SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.TeamProject] = @project "
                     "AND [System.IterationPath] = @CurrentIteration('[HarborPoint]\\HarborPoint Team')"},
            {"path": "Shared Queries/HarborPoint Reports", "name": "Portfolio - Epics and Features",
             "wiql": "SELECT [System.Id], [System.Title] FROM WorkItemLinks WHERE ([Source].[System.TeamProject] = "
                     "@project AND [Source].[System.WorkItemType] = 'Epic') AND ([System.Links.LinkType] = "
                     "'System.LinkTypes.Hierarchy-Forward') AND ([Target].[System.WorkItemType] = 'Feature') "
                     "MODE (Recursive)"},
            {"path": "Shared Queries/Training/{participant}/Lab 11 - Inherited queries", "name": "Open work",
             "per_participant": True,
             "wiql": "SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = @project AND "
                     "[System.AreaPath] UNDER '{sandbox_area}' AND [System.State] <> 'Closed'"},
            {"path": "My Queries", "name": "MS - Waiting for sign-off", "private": True,
             "wiql": "SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = @project AND "
                     "[System.State] = 'Resolved'"}],
        "wiki_pages": [{"path": "/Home", "file": "wiki/home.md"},
                       {"path": "/Program", "file": "wiki/program.md"},
                       {"path": "/Program/Program Charter", "file": "wiki/charter.md"}],
        "dashboards": [
            {"name": "HarborPoint Program Overview", "description": "Program", "team": None, "widgets": [
                {"type": "markdown", "title": "Lighthouse", "row": 1, "column": 1, "row_span": 2, "column_span": 4,
                 "markdown": "## Project Lighthouse\n1. Protect every member"},
                {"type": "query_tile", "title": "Current sprint", "row": 1, "column": 5, "row_span": 1,
                 "column_span": 1, "query": "Shared Queries/HarborPoint Reports/Program - Current sprint (all teams)",
                 "rules": [{"op": ">", "value": 0, "color": "#cc293d"}]}]},
            {"name": "Member Support - Delivery Health", "description": "Leo", "team": "Member Support", "widgets": [
                {"type": "markdown", "title": "Header", "row": 1, "column": 1, "row_span": 2, "column_span": 3,
                 "markdown": "Maintained by Leo Fischer, PMO"},
                {"type": "query_tile", "title": "Waiting for sign-off", "row": 1, "column": 4, "row_span": 1,
                 "column_span": 1, "query": "My Queries/MS - Waiting for sign-off"},
                {"type": "velocity", "title": "Velocity", "row": 3, "column": 1, "row_span": 2, "column_span": 4,
                 "team": "Member Support"},
                {"type": "sprint_burndown", "title": "Sprint burndown (current sprint)", "row": 3, "column": 5,
                 "row_span": 2, "column_span": 4, "team": "Member Support", "iteration": "PI 4\\Sprint 13"}]}],
        "delivery_plans": [{"name": "HarborPoint Program Plan", "description": "Plan",
                            "teams": [{"team": "Mobile Banking", "backlog": "Microsoft.FeatureCategory"},
                                      {"team": "Member Support", "backlog": "Microsoft.FeatureCategory"}],
                            "markers": [{"sprint": "Sprint 15", "at": "end", "label": "PI 4 System Demo",
                                         "color": "#0078d4"}],
                            "card_fields": ["System.AssignedTo", "Microsoft.VSTS.Scheduling.TargetDate"]}],
    }
    return {"schema": "harborpoint-dataset/1", "generated_at": now.isoformat(), "now": now.isoformat(),
            "project": {"name": "HarborPoint", "description": "HarborPoint Financial training", "process": "Agile"},
            "calendar": {"sprint14_start": s14.isoformat(), "iterations": iters},
            "areas": ["Digital", "Digital\\Mobile Banking", "Member Support", "Training", "Training\\P01"],
            "teams": teams, "work_items": work_items, "artifacts": artifacts}


def make_content_dir(tmp: Path) -> Path:
    content = tmp / "content"
    (content / "wiki").mkdir(parents=True)
    (content / "wiki" / "home.md").write_text("# HarborPoint\nWelcome to {project}.\n")
    (content / "wiki" / "program.md").write_text("# Program\n")
    (content / "wiki" / "charter.md").write_text("# Program Charter\n")
    return content


class Harness:
    """Provisioner wired to a simulator; records nothing outside a temp dir."""

    def __init__(self, ds, content, *, sim=None, state_path=None, transport=None, **opts):
        self.sim = sim or AdoSimulator("example")
        self.logs: list[str] = []
        self.client = AdoClient("secret-pat-value", transport=transport or self.sim, max_rps=0,
                                sleep=lambda s: None, log=self.logs.append)
        self.state = P.State.load(state_path) if state_path else P.State(None)
        self.prov = P.Provisioner(Api(ORG), self.client, ds, self.state,
                                  P.Options(content_dir=content, **opts), log=self.logs.append,
                                  sleep=lambda s: None)

    def run(self, steps=None):
        self.prov.run(steps or P.STEPS)
        return self

    def writes(self, contains=""):
        return [c for c in self.sim.calls if c["method"] in ("POST", "PATCH", "PUT", "DELETE")
                and contains in c["path"]]


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.content = make_content_dir(self.tmp)
        self.ds = fixture_dataset()

    def test_fixture_is_valid(self):
        r = validate(self.ds, self.content)
        self.assertEqual(r.errors, [])
        self.assertEqual(r.stats["work_items"], 4)
        self.assertEqual(r.stats["revisions"], 9)

    def test_detects_contract_violations(self):
        ds = self.ds
        s1 = ds["work_items"][2]
        s1["revisions"][2]["at"] = s1["revisions"][1]["at"]                     # not increasing
        ds["work_items"][3]["revisions"][2]["at"] = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
        ds["work_items"][1]["revisions"][0]["fields"]["System.AreaPath"] = "HarborPoint\\Nowhere"
        ds["work_items"][1]["revisions"][0]["fields"]["bad field"] = 1
        ds["work_items"][0]["links"] = [{"type": "Successor", "target": "F99"}]
        ds["work_items"][2]["parent"] = "S2"                                      # child listed before parent
        ds["artifacts"]["dashboards"][0]["widgets"][1]["query"] = "Shared Queries/Nope/Missing"
        ds["teams"][1]["iterations"].append("PI 9\\Sprint 99")
        errors = "\n".join(validate(ds, self.content).errors)
        for needle in ("is not after the previous revision", "is after dataset now", "Nowhere",
                       "implausible field name", "F99", "listed after the child", "Nope/Missing", "PI 9"):
            self.assertIn(needle, errors)

    def test_wiki_file_missing(self):
        (self.content / "wiki" / "charter.md").unlink()
        self.assertTrue(any("charter.md" in e for e in validate(self.ds, self.content).errors))

    def test_team_multi_area_form(self):
        from harborpoint.dataset_check import team_area_values
        default, values = team_area_values(self.ds["teams"][0], "HarborPoint")
        self.assertEqual(default, "HarborPoint")
        self.assertEqual(values, [("HarborPoint", False), ("HarborPoint\\Digital", True),
                                  ("HarborPoint\\Member Support", True)])
        default, values = team_area_values(self.ds["teams"][1], "HarborPoint")
        self.assertEqual(values, [("HarborPoint\\Digital\\Mobile Banking", False)])


class TestRequestBuilders(unittest.TestCase):
    def setUp(self):
        self.api = Api(ORG)
        self.tmp = Path(tempfile.mkdtemp())
        self.h = Harness(fixture_dataset(), make_content_dir(self.tmp))

    def test_create_work_item_request(self):
        req = self.api.create_work_item("HarborPoint", "User Story", [])
        self.assertEqual(req.method, "POST")
        self.assertEqual(req.url, f"{ORG}/HarborPoint/_apis/wit/workitems/$User%20Story")
        self.assertEqual(req.params, {"bypassRules": "true", "suppressNotifications": "true", "api-version": "7.1"})
        self.assertEqual(req.headers["Content-Type"], "application/json-patch+json")
        self.assertTrue(req.full_url().endswith("?bypassRules=true&suppressNotifications=true&api-version=7.1"))
        self.assertTrue(req.unsafe)

    def test_revision_patches(self):
        ds = self.h.prov.ds
        s1 = ds["work_items"][2]
        first = self.h.prov.build_patch(s1, 0, parent_id=42)
        paths = {o["path"]: o.get("value") for o in first}
        at = P.ado_ts(s1["revisions"][0]["at"])
        self.assertEqual(paths["/fields/System.CreatedDate"], at)
        self.assertEqual(paths["/fields/System.ChangedDate"], at)
        self.assertRegex(at, r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$")
        self.assertEqual(paths["/relations/-"], {"rel": "System.LinkTypes.Hierarchy-Reverse",
                                                 "url": f"{ORG}/_apis/wit/workItems/42"})
        self.assertEqual(paths["/fields/System.AssignedTo"], "Hannah Cole")
        self.assertTrue(all(o["op"] == "add" for o in first))
        second = self.h.prov.build_patch(s1, 1, parent_id=None)
        paths2 = [o["path"] for o in second]
        self.assertNotIn("/fields/System.CreatedDate", paths2)
        self.assertIn("/fields/System.ChangedDate", paths2)
        self.assertIn("/fields/System.History", paths2)
        self.assertNotIn("/relations/-", paths2)

    def test_assign_map_and_clearing(self):
        prov = self.h.prov
        prov.opts.assign_map = {"Hannah Cole": "Hannah Cole <hannah.cole@example.test>"}
        s1 = prov.ds["work_items"][2]
        s1["revisions"][2]["fields"]["Microsoft.VSTS.Common.ResolvedDate"] = None
        first = {o["path"]: o.get("value") for o in prov.build_patch(s1, 0, None)}
        self.assertEqual(first["/fields/System.AssignedTo"], "Hannah Cole <hannah.cole@example.test>")
        third = prov.build_patch(s1, 2, None)
        self.assertIn({"op": "remove", "path": "/fields/Microsoft.VSTS.Common.ResolvedDate"}, third)

    def test_classification_and_team_urls(self):
        req = self.api.create_node("pid", "Iterations", "PI 4", "Sprint 13", "2026-10-12", "2026-10-23")
        self.assertEqual(req.url, f"{ORG}/pid/_apis/wit/classificationnodes/Iterations/PI%204")
        self.assertEqual(req.body, {"name": "Sprint 13", "attributes": {"startDate": "2026-10-12T00:00:00Z",
                                                                      "finishDate": "2026-10-23T00:00:00Z"}})
        req = self.api.set_team_days_off("pid", "tid", "guid", [("2026-11-25", "2026-11-26")])
        self.assertTrue(req.url.endswith("/pid/tid/_apis/work/teamsettings/iterations/guid/teamdaysoff"))
        self.assertEqual(req.body, {"daysOff": [{"start": "2026-11-25T00:00:00Z", "end": "2026-11-26T00:00:00Z"}]})

    def test_query_and_wiki_urls(self):
        req = self.api.create_query_item("pid", "Shared Queries/PMO Reporting", "MS - Open work", "SELECT 1")
        self.assertEqual(req.url, f"{ORG}/pid/_apis/wit/queries/Shared%20Queries/PMO%20Reporting")
        req = self.api.put_wiki_page("pid", "wid", "/Templates/Executive Briefing (BLUF)", "x", etag='"abc"')
        self.assertEqual(req.headers["If-Match"], '"abc"')
        self.assertIn("path=/Templates/Executive%20Briefing%20%28BLUF%29", req.full_url())


class TestClient(unittest.TestCase):
    def test_auth_retry_and_errors(self):
        calls, sleeps = [], []
        responses = [(429, {"Retry-After": "7"}, b'{"message":"TF400733: Request was blocked"}'),
                     (503, {}, b""),
                     (200, {"Content-Type": "application/json"}, b'{"ok": true}')]

        def transport(method, url, headers, data, timeout):
            calls.append(headers)
            return responses.pop(0)
        c = AdoClient("my-pat", transport=transport, max_rps=0, sleep=sleeps.append, log=lambda s: None)
        r = c.send(Req("GET", f"{ORG}/_apis/projects", {"api-version": "7.1"}))
        self.assertEqual(r.data, {"ok": True})
        self.assertEqual(calls[0]["Authorization"], "Basic " + base64.b64encode(b":my-pat").decode())
        self.assertEqual(sleeps[0], 7.0)          # honoured Retry-After
        self.assertEqual(len(calls), 3)

    def test_unsafe_write_not_retried_on_5xx(self):
        n = []

        def transport(method, url, headers, data, timeout):
            n.append(1)
            return 503, {}, b'{"message":"boom"}'
        c = AdoClient("my-pat", transport=transport, max_rps=0, sleep=lambda s: None, log=lambda s: None)
        with self.assertRaises(AdoError):
            c.send(Api(ORG).create_work_item("p", "Bug", []))
        self.assertEqual(len(n), 1)

    def test_error_has_context_and_hides_pat(self):
        def transport(method, url, headers, data, timeout):
            return 400, {"Content-Type": "application/json"}, json.dumps(
                {"message": "VS402625: Dates must be increasing with each revision.",
                 "typeKey": "RuleValidationException"}).encode()
        c = AdoClient("super-secret", transport=transport, max_rps=0, sleep=lambda s: None, log=lambda s: None)
        with self.assertRaises(AdoError) as ctx:
            c.send(Api(ORG).update_work_item("p", 5, []))
        text = str(ctx.exception)
        for needle in ("HTTP 400", "PATCH", "/workitems/5", "RuleValidationException", "VS402625", "Hint:"):
            self.assertIn(needle, text)
        self.assertNotIn("super-secret", text)
        self.assertNotIn(base64.b64encode(b":super-secret").decode(), text)


class TestFullRunAgainstSimulator(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.content = make_content_dir(self.tmp)
        self.ds = fixture_dataset()

    def test_all_steps_then_idempotent_rerun(self):
        state = self.tmp / "state.json"
        h = Harness(self.ds, self.content, state_path=state).run()
        sim = h.sim
        self.assertEqual(len(sim.workitems), 4)
        # every work item write: json-patch, bypassRules + suppressNotifications, api 7.1
        wi_writes = [c for c in h.writes("/_apis/wit/workitems")]
        self.assertEqual(len(wi_writes), 9 + 2)                       # 9 revisions + 2 unique links
        for c in wi_writes:
            self.assertEqual(c["headers"]["Content-Type"], "application/json-patch+json")
            self.assertEqual(c["query"].get("bypassRules"), "true")
            self.assertEqual(c["query"].get("suppressNotifications"), "true")
            self.assertEqual(c["query"].get("api-version"), "7.1")
        # backdated ChangedDate strictly increasing per item and CreatedDate == first ChangedDate
        for wi in sim.workitems.values():
            dates = [_parse_dt(r["fields"]["System.ChangedDate"]) for r in wi["revisions"]]
            backdated = [d for d in dates if d < sim.now - timedelta(minutes=1)]
            self.assertEqual(backdated, sorted(set(backdated)))
            self.assertEqual(wi["revisions"][0]["fields"]["System.CreatedDate"],
                             wi["revisions"][0]["fields"]["System.ChangedDate"])
        s2 = next(w for w in sim.workitems.values() if w["fields"]["System.Title"] == "Endorsement validation")
        rels = {r["rel"] for r in s2["relations"]}
        self.assertIn("System.LinkTypes.Hierarchy-Reverse", rels)
        self.assertIn("System.LinkTypes.Dependency-Reverse", rels)   # S1 is S2's predecessor
        self.assertEqual(s2["fields"]["System.State"], "Closed")
        self.assertEqual(s2["fields"]["System.IterationPath"], "HarborPoint\\PI 4\\Sprint 13")
        # team configuration
        pid = sim.projects["HarborPoint"]["id"]
        teams = {t["name"]: t["id"] for t in sim.teams[pid]}
        self.assertEqual(set(teams), {"HarborPoint Team", "Mobile Banking", "Member Support", "P01 Sandbox"})
        default_cfg = sim.team_cfg[teams["HarborPoint Team"]]
        self.assertEqual(default_cfg["fieldvalues"]["defaultValue"], "HarborPoint")
        self.assertEqual(default_cfg["fieldvalues"]["values"][0], {"value": "HarborPoint", "includeChildren": False})
        mb = sim.team_cfg[teams["Mobile Banking"]]
        self.assertEqual(mb["settings"]["bugsBehavior"], "asRequirements")
        self.assertEqual(mb["settings"]["backlogVisibilities"]["Microsoft.EpicCategory"], False)
        self.assertEqual(len(mb["iterations"]), 3)
        self.assertEqual(len(mb["daysoff"]), 1)
        # queries: tokens expanded, team id injected, per-participant folders, My Queries
        store = sim.queries[pid]
        self.assertIn("Shared Queries/Training/P01/Lab 11 - Inherited queries/Open work", store)
        self.assertIn("HarborPoint\\Training\\P01", store["Shared Queries/Training/P01/Lab 11 - Inherited queries/"
                                                          "Open work"]["wiql"])
        cur = store["Shared Queries/HarborPoint Reports/Program - Current sprint (all teams)"]["wiql"]
        self.assertIn(f"<id:{teams['HarborPoint Team']}>", cur)
        self.assertIn("My Queries/MS - Waiting for sign-off", store)
        self.assertEqual(len(sim.aces), 1)
        self.assertEqual(sim.aces[0]["accessControlEntries"][0]["allow"], 1 | 2 | 8)
        # wiki, dashboards, plan
        wiki_id = sim.wikis[pid][0]["id"]
        self.assertEqual(list(sim.pages[wiki_id]), ["/Home", "/Program", "/Program/Program Charter"])
        self.assertIn("Welcome to HarborPoint.", sim.pages[wiki_id]["/Home"]["content"])
        proj_dash = sim.dashboards[(pid, None)][0]
        self.assertEqual(len(proj_dash["widgets"]), 2)
        ms_dash = sim.dashboards[(pid, teams["Member Support"])][0]
        self.assertEqual([w["name"] for w in ms_dash["widgets"]], ["Header", "Waiting for sign-off", "Velocity"])
        manual = h.state.data["manual"]
        self.assertTrue(any("Sprint burndown" in k for k in manual))   # uncertain widget -> manual steps
        self.assertIn("Iteration: 'Sprint 13'", "\n".join(manual.values()))
        plan = sim.plans[pid][0]
        self.assertEqual(plan["properties"]["markers"][0]["label"], "PI 4 System Demo")
        self.assertEqual(plan["properties"]["markers"][0]["date"], self.ds["calendar"]["iterations"][3]["finish"]
                         + "T00:00:00Z")
        self.assertTrue(plan["properties"]["cardSettings"]["fields"]["showAssignedTo"])
        # rerun with the same state: no writes at all except none
        before = len(sim.calls)
        h2 = Harness(self.ds, self.content, sim=sim, state_path=state).run()
        new_writes = [c for c in sim.calls[before:] if c["method"] in ("POST", "PUT", "DELETE")
                      or (c["method"] == "PATCH" and "/wit/" in c["path"])]
        self.assertEqual([(c["method"], c["path"]) for c in new_writes], [])
        self.assertEqual(len(sim.workitems), 4)
        self.assertEqual(len(sim.plans[pid]), 1)

    def test_resume_after_failure(self):
        state = self.tmp / "state.json"
        sim = AdoSimulator("example", fail_labels={r"PATCH .*/workitems/4$": 400})
        h = Harness(self.ds, self.content, sim=sim, state_path=state)
        with self.assertRaises(P.StepError) as ctx:
            h.run(["preflight", "project", "classification", "teams", "workitems"])
        self.assertIn("S2", str(ctx.exception))
        sim.fail_patterns = {}
        Harness(self.ds, self.content, sim=sim, state_path=state).run(["workitems", "links"])
        self.assertEqual(len(sim.workitems), 4)
        self.assertTrue(all(len(w["revisions"]) >= len(d["revisions"]) for w, d in
                            zip(sim.workitems.values(), self.ds["work_items"])))

    def test_lost_response_does_not_duplicate(self):
        sim = AdoSimulator("example")
        state = {"lost": 0}

        def flaky(method, url, headers, data, timeout):
            result = sim(method, url, headers, data, timeout)
            if method == "POST" and "/workitems/$User%20Story" in url and state["lost"] == 0:
                state["lost"] = 1
                raise ConnectionError("connection reset after the server committed")
            return result
        h = Harness(self.ds, self.content, sim=sim, transport=flaky)
        h.run(["project", "classification", "teams", "workitems"])
        self.assertEqual(len(sim.workitems), 4)
        self.assertTrue(any("Recovered in-flight creation" in line for line in h.logs))

    def test_refuses_unknown_existing_items(self):
        sim = AdoSimulator("example")
        Harness(self.ds, self.content, sim=sim).run(["project", "classification", "teams", "workitems"])
        with self.assertRaises(P.StepError):
            Harness(self.ds, self.content, sim=sim).run(["workitems"])

    def test_order_modes_vs_link_side_effects(self):
        # parent gets a revision stamped with the child's date: item order breaks, chronological works
        with self.assertRaises(P.StepError) as ctx:
            Harness(self.ds, self.content, sim=AdoSimulator("example", link_side_effect="same_time"),
                    order="item").run(["project", "classification", "teams", "workitems"])
        self.assertIn("VS402625", str(ctx.exception))
        Harness(self.ds, self.content, sim=AdoSimulator("example", link_side_effect="same_time"),
                order="chronological").run(["project", "classification", "teams", "workitems"])
        # parent gets a revision stamped 'now': item order works, chronological breaks
        Harness(self.ds, self.content, sim=AdoSimulator("example", link_side_effect="now"),
                order="item").run(["project", "classification", "teams", "workitems"])
        with self.assertRaises(P.StepError):
            Harness(self.ds, self.content, sim=AdoSimulator("example", link_side_effect="now"),
                    order="chronological").run(["project", "classification", "teams", "workitems"])

    def test_parent_links_final_mode(self):
        h = Harness(self.ds, self.content, parent_links="final").run(
            ["project", "classification", "teams", "workitems", "links"])
        creates = [c for c in h.writes("/workitems/$")]
        self.assertFalse(any(o["path"] == "/relations/-" for c in creates for o in c["body"]))
        parents = [w for w in h.sim.workitems.values()
                   if any(r["rel"] == "System.LinkTypes.Hierarchy-Reverse" for r in w["relations"])]
        self.assertEqual(len(parents), 3)

    def test_wiki_update_uses_etag(self):
        sim = AdoSimulator("example")
        Harness(self.ds, self.content, sim=sim).run(["project", "wiki"])
        (self.content / "wiki" / "home.md").write_text("# Changed\n")
        before = len(sim.calls)
        Harness(self.ds, self.content, sim=sim).run(["wiki"])
        puts = [c for c in sim.calls[before:] if c["method"] == "PUT"]
        self.assertEqual(len(puts), 1)
        self.assertIn("If-Match", puts[0]["headers"])

    def test_dashboard_fallback_to_single_widgets(self):
        sim = AdoSimulator("example", fail_labels={r"^POST /example/[^/]+/_apis/dashboard/dashboards$": 400})
        h = Harness(self.ds, self.content, sim=sim)
        h.run(["project", "classification", "teams", "queries", "dashboards"])
        self.assertTrue(any(k.startswith("dashboard:HarborPoint Program Overview") for k in h.state.data["manual"]))
        pid = sim.projects["HarborPoint"]["id"]
        self.assertEqual(len([d for k, v in sim.dashboards.items() if k[1] for d in v]), 1)

    def test_pilot_findings(self):
        cases = {"none": "safe", "same_time": "chronological", "now": "--order item"}
        for side, expect in cases.items():
            h = Harness(self.ds, self.content, sim=AdoSimulator("example", link_side_effect=side))
            h.run(["pilot"])
            findings = h.state.data["pilot"]["findings"]
            self.assertEqual(findings["link_side_effect"], side, side)
            out = "\n".join(h.logs)
            self.assertIn(expect, out)
            self.assertIn("CHECK IN THE UI", out)
            if side != "now":
                story = next(w for w in h.sim.workitems.values() if w["type"] == "User Story")
                self.assertEqual(len(story["revisions"]), 4)
                self.assertEqual(story["fields"]["System.State"], "Closed")
            self.assertEqual(len(h.sim.workitems), 2)
            self.assertIn("rejected", findings["future_changed_date"])
            pid = h.sim.projects["HarborPoint"]["id"]
            self.assertEqual(len(h.sim.teams[pid]), 2)                 # default + the pilot team only
        Harness(self.ds, self.content, sim=h.sim, state_path=None)     # cleanup path below
        h.prov.run(["pilot-cleanup"])
        self.assertEqual(len(h.sim.workitems), 0)


class TestCli(unittest.TestCase):
    def test_dry_run_cli_makes_no_network_calls(self):
        tmp = Path(tempfile.mkdtemp())
        content = make_content_dir(tmp)
        ds_path = tmp / "dataset.json"
        ds_path.write_text(json.dumps(fixture_dataset()))
        real_connect = socket.socket.connect

        def no_net(*a, **k):
            raise AssertionError("network access during dry-run")
        socket.socket.connect = no_net
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out):
                code = P.main(["--org", ORG, "--dataset", str(ds_path), "--content-dir", str(content), "--dry-run"])
        finally:
            socket.socket.connect = real_connect
        text = out.getvalue()
        self.assertEqual(code, 0, text)
        for needle in ("PLAN", "workitems.create x4", "workitems.update x5", "estimated runtime",
                       "bypassRules=true&suppressNotifications=true", "MANUAL FOLLOW-UPS", "Sprint burndown"):
            self.assertIn(needle, text)
        self.assertFalse((tmp / "out").exists())

    def test_dry_run_fails_on_invalid_dataset(self):
        tmp = Path(tempfile.mkdtemp())
        content = make_content_dir(tmp)
        ds = fixture_dataset()
        ds["work_items"][1]["parent"] = "NOPE"
        ds_path = tmp / "dataset.json"
        ds_path.write_text(json.dumps(ds))
        with contextlib.redirect_stdout(io.StringIO()):
            code = P.main(["--org", ORG, "--dataset", str(ds_path), "--content-dir", str(content), "--dry-run"])
        self.assertEqual(code, 1)

    def test_pilot_dry_run_on_separate_project(self):
        tmp = Path(tempfile.mkdtemp())
        content = make_content_dir(tmp)
        ds_path = tmp / "dataset.json"
        ds_path.write_text(json.dumps(fixture_dataset()))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = P.main(["--org", ORG, "--dataset", str(ds_path), "--content-dir", str(content), "--dry-run",
                           "--steps", "pilot", "--project", "HarborPoint-Pilot"])
        self.assertEqual(code, 0, out.getvalue())
        self.assertIn("pilot", out.getvalue())
        self.assertIn("workitems.create x2", out.getvalue())

    def test_help_lists_pat_scopes(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), self.assertRaises(SystemExit):
            P.main(["--help"])
        for scope in ("vso.project_manage", "vso.work_write", "vso.wiki_write", "vso.dashboards_manage",
                      "vso.security_manage"):
            self.assertIn(scope, out.getvalue())

    def test_live_run_requires_yes_when_not_interactive(self):
        tmp = Path(tempfile.mkdtemp())
        content = make_content_dir(tmp)
        ds_path = tmp / "dataset.json"
        ds_path.write_text(json.dumps(fixture_dataset()))
        pat = tmp / "pat"
        pat.write_text("x")
        pat.chmod(0o600)
        err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err), \
                unittest.mock.patch("sys.stdin", io.StringIO("")):
            code = P.main(["--org", ORG, "--dataset", str(ds_path), "--content-dir", str(content),
                           "--pat-file", str(pat), "--state", str(tmp / "s.json")])
        self.assertEqual(code, 2)
        self.assertIn("--yes", err.getvalue())


if __name__ == "__main__":
    unittest.main()

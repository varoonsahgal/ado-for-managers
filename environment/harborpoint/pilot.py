"""``--steps pilot``: validate backdating on a live org before seeding ~1,500 items.

What it does (all idempotent, recorded in the state file under "pilot"):

1. preflight + project + classification (ALL areas and iterations, final dates);
2. ONE team (``--pilot-team``, default: the first delivery team with a Stories backlog), fully
   configured (areas, iterations, settings, days off);
3. ONE Feature and ONE User Story (child of the Feature) with 4 backdated story revisions in the
   last completed sprint, applied in chronological order:

   ====  ================================  ======================================================
   F r1  Monday before the sprint, 16:05Z  Feature created, New
   S r1  Friday before the sprint, 16:10Z  Story created, New, backlog (root iteration), 5 pts,
                                           parent link to the Feature
   S r2  sprint day 1, 16:20Z              moved into the sprint, Active (ActivatedDate)
   F r2  sprint day 1, 16:25Z              Feature Active
   S r3  sprint day 4, 17:00Z              Resolved (ResolvedDate)
   S r4  sprint day 7, 17:30Z              Closed (ClosedDate) + comment
   ====  ================================  ======================================================

4. read-only probes: the Feature's revision list after the child got its parent link (does the
   parent receive a server-side revision, and with which ChangedDate?), User Story state
   categories, and a ``validateOnly`` PATCH with a FUTURE ChangedDate (is it rejected?);
5. prints the checklist of what to verify in the UI / Analytics and which --order /
   --parent-links mode the full run should use.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import TYPE_CHECKING

from .ado import AdoError
from .dataset_check import team_area_values

if TYPE_CHECKING:  # pragma: no cover
    from .provision import Provisioner

PILOT_TAG = "pilot"


def _at(day: date, hh: int, mm: int) -> str:
    return datetime(day.year, day.month, day.day, hh, mm, tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def pick_team(prov: "Provisioner") -> dict:
    teams = prov.ds["teams"]
    if prov.opts.pilot_team:
        t = next((t for t in teams if t["name"] == prov.opts.pilot_team), None)
        if not t:
            raise ValueError(f"--pilot-team {prov.opts.pilot_team!r} is not in the dataset")
        return t
    for t in teams:
        if not t.get("is_default") and not t.get("participant") and t.get("backlog_levels", {}).get("stories", True) \
                and t.get("iterations"):
            return t
    raise ValueError("No delivery team with iterations found in the dataset")


def pick_sprint(prov: "Provisioner", team: dict) -> dict:
    """The latest sprint selected by the team that finished at least one day before 'now'."""
    now = datetime.now(timezone.utc).date()
    cal = {i["path"]: i for i in prov.ds["calendar"]["iterations"]}
    done = [cal[p] for p in team["iterations"] if p in cal and date.fromisoformat(cal[p]["finish"]) < now
            and "\\" in p]
    if not done:
        raise ValueError(f"Team {team['name']} has no completed sprint before today; cannot backdate a pilot")
    return max(done, key=lambda i: i["finish"])


def build_pilot_items(prov: "Provisioner", team: dict, sprint: dict) -> list[dict]:
    """Return dataset-shaped Feature + Story with revisions (story parent = feature)."""
    project = prov.project
    area, _ = team_area_values(team, project)
    start = date.fromisoformat(sprint["start"])
    while start.weekday() != 0:      # snap to Monday (sprints start on Monday)
        start -= timedelta(days=1)
    day = lambda n: start + timedelta(days=(n - 1) + 2 * ((n - 1) // 5))   # working day n (1-based)
    f1, s1 = start - timedelta(days=7), start - timedelta(days=3)
    sprint_path = f"{project}\\{sprint['path']}"
    pi_path = f"{project}\\{sprint['path'].rsplit(chr(92), 1)[0]}"
    owner = next((r["fields"]["System.AssignedTo"] for wi in prov.ds["work_items"] for r in wi["revisions"]
                  if r.get("fields", {}).get("System.AssignedTo")), "Pilot Owner")
    feature = {"key": "PILOT-F", "type": "Feature", "parent": None, "revisions": [
        {"at": _at(f1, 16, 5), "fields": {
            "System.Title": "PILOT - Backdating check (Feature)", "System.State": "New", "System.Reason": "New",
            "System.AreaPath": area, "System.IterationPath": pi_path, "System.Tags": PILOT_TAG,
            "Microsoft.VSTS.Common.StackRank": 999999999.0}},
        {"at": _at(day(1), 16, 25), "fields": {
            "System.State": "Active", "System.Reason": "Implementation started",
            "Microsoft.VSTS.Common.ActivatedDate": _at(day(1), 16, 25),
            "Microsoft.VSTS.Common.StateChangeDate": _at(day(1), 16, 25)}}]}
    story = {"key": "PILOT-S", "type": "User Story", "parent": "PILOT-F", "revisions": [
        {"at": _at(s1, 16, 10), "fields": {
            "System.Title": "PILOT - Backdating check (Story)", "System.State": "New", "System.Reason": "New",
            "System.AreaPath": area, "System.IterationPath": project, "System.AssignedTo": owner,
            "System.Tags": PILOT_TAG, "Microsoft.VSTS.Scheduling.StoryPoints": 5,
            "Microsoft.VSTS.Common.StackRank": 999999999.0}},
        {"at": _at(day(1), 16, 20), "fields": {
            "System.IterationPath": sprint_path, "System.State": "Active", "System.Reason": "Implementation started",
            "Microsoft.VSTS.Common.ActivatedDate": _at(day(1), 16, 20),
            "Microsoft.VSTS.Common.StateChangeDate": _at(day(1), 16, 20)},
         "comment": "Pilot: pulled into the sprint and started on day 1."},
        {"at": _at(day(4), 17, 0), "fields": {
            "System.State": "Resolved", "System.Reason": "Code complete and unit tests pass",
            "Microsoft.VSTS.Common.ResolvedDate": _at(day(4), 17, 0),
            "Microsoft.VSTS.Common.StateChangeDate": _at(day(4), 17, 0)}},
        {"at": _at(day(7), 17, 30), "fields": {
            "System.State": "Closed", "System.Reason": "Acceptance tests pass",
            "Microsoft.VSTS.Common.ClosedDate": _at(day(7), 17, 30),
            "Microsoft.VSTS.Common.StateChangeDate": _at(day(7), 17, 30)},
         "comment": "Pilot: accepted by QA on day 7."}]}
    return [feature, story]


def run_pilot(prov: "Provisioner") -> None:
    log = prov.log
    prov.step_preflight()
    prov.step_project()
    prov.step_classification()
    team = pick_team(prov)
    log(f"  Pilot team: {team['name']}")
    prov.step_teams(only=[team["name"]])
    sprint = pick_sprint(prov, team)
    feature, story = build_pilot_items(prov, team, sprint)
    st = prov.state.section("pilot")
    items = st.setdefault("items", {})
    findings = st.setdefault("findings", {})
    # chronological schedule: F1, S1 (+parent), S2, F2, S3, S4
    schedule = [(feature, 0), (story, 0), (story, 1), (feature, 1), (story, 2), (story, 3)]
    for wi, n in schedule:
        rec = items.get(wi["key"])
        if (n == 0 and rec) or (rec and rec["rev"] > n):
            continue
        parent_id = items[wi["parent"]]["id"] if n == 0 and wi.get("parent") else None
        saved_mode = prov.opts.parent_links
        prov.opts.parent_links = "create"
        patch = prov.build_patch(wi, n, parent_id)
        prov.opts.parent_links = saved_mode
        try:
            if n == 0:
                data = prov.send(prov.api.create_work_item(prov.project_id, wi["type"], patch)).data
                items[wi["key"]] = {"id": data["id"], "rev": 1}
            else:
                prov.send(prov.api.update_work_item(prov.project_id, rec["id"], patch))
                rec["rev"] = n + 1
        except AdoError as exc:
            findings[f"{wi['key']} r{n + 1}"] = f"FAILED: HTTP {exc.status} {exc.code} {exc.message[:200]}"
            prov.state.save()
            log(f"  {wi['key']} revision {n + 1} FAILED: {exc}")
            if wi["key"] == "PILOT-F" and n == 1 and exc.code == "VS402625":
                findings["link_side_effect"] = "now"
            elif wi["key"] == "PILOT-S" and n == 0 and exc.code == "VS402625":
                findings["link_side_effect"] = "same_time?"
            break
        prov.state.save()
        log(f"  {wi['key']} revision {n + 1} applied at {wi['revisions'][n]['at']}")
        if wi["key"] == "PILOT-S" and n == 0:
            _probe_parent_revisions(prov, items["PILOT-F"]["id"], wi["revisions"][0]["at"], findings)
    _probe_states(prov, findings)
    if "PILOT-S" in items:
        _probe_future(prov, items["PILOT-S"]["id"], findings)
    prov.state.save()
    print_checklist(prov, team, sprint, items, findings)


def _probe_parent_revisions(prov, feature_id: int, child_at: str, findings: dict) -> None:
    try:
        revs = prov.send(prov.api.get_revisions(prov.project_id, feature_id)).data.get("value", [])
    except AdoError as exc:
        findings["parent_revisions"] = f"could not read: {exc.status}"
        return
    dates = [r.get("fields", {}).get("System.ChangedDate") for r in revs]
    findings["parent_revisions"] = dates
    if len(revs) <= 1:
        findings.setdefault("link_side_effect", "none")
    elif str(dates[-1])[:19] == str(child_at)[:19]:
        findings.setdefault("link_side_effect", "same_time")
    else:
        findings.setdefault("link_side_effect", "now")


def _probe_states(prov, findings: dict) -> None:
    try:
        states = prov.send(prov.api.wit_states(prov.project_id, "User Story")).data.get("value", [])
        findings["user_story_state_categories"] = {s["name"]: s.get("category") for s in states}
    except AdoError as exc:
        findings["user_story_state_categories"] = f"could not read: {exc.status}"


def _probe_future(prov, story_id: int, findings: dict) -> None:
    future = (datetime.now(timezone.utc) + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    patch = [{"op": "add", "path": "/fields/System.ChangedDate", "value": future},
             {"op": "add", "path": "/fields/System.History", "value": "pilot probe (validateOnly)"}]
    try:
        prov.send(prov.api.update_work_item(prov.project_id, story_id, patch, validate_only=True,
                                            label="pilot.futureProbe"))
        findings["future_changed_date"] = "ACCEPTED by validateOnly (the dataset must never contain future times)"
    except AdoError as exc:
        findings["future_changed_date"] = f"rejected: HTTP {exc.status} {exc.code} {exc.message[:160]}"


def recommendation(findings: dict) -> str:
    side = findings.get("link_side_effect", "unknown")
    if side == "none":
        return ("Parent links do not create a revision on the parent: the default (--order item "
                "--parent-links create) is safe.")
    if side == "same_time":
        return ("The parent receives a revision stamped with the CHILD's ChangedDate: use --order chronological "
                "(keeps every item's dates increasing). --order item would fail with VS402625.")
    if side == "now":
        return ("The parent receives a revision stamped with the CURRENT time: use --order item (default). "
                "Expect Epic/Feature 'Changed Date' to equal the seeding time.")
    return ("Could not determine the parent-link behaviour; inspect the Feature's History tab and choose "
            "--order chronological if its link revision carries the story's date, else --order item.")


def print_checklist(prov, team: dict, sprint: dict, items: dict, findings: dict) -> None:
    log = prov.log
    base = f"{prov.api.org}/{prov.project.replace(' ', '%20')}"
    fid = items.get("PILOT-F", {}).get("id")
    sid = items.get("PILOT-S", {}).get("id")
    sname = sprint["path"].split("\\")[-1]
    log("\n  PILOT FINDINGS")
    for k, v in findings.items():
        log(f"    {k}: {v}")
    log(f"\n  RECOMMENDATION: {recommendation(findings)}")
    log("\n  CHECK IN THE UI / ANALYTICS (allow 5-30 min for Analytics to catch up):")
    checks = [
        f"Story #{sid}: {base}/_workitems/edit/{sid} -> History tab shows 4 revisions with the backdated times "
        f"(created {sname} minus 3 days, Active on day 1, Resolved day 4, Closed day 7), NOT today.",
        f"Story #{sid}: Created Date / Activated Date / Resolved Date / Closed Date / State Change Date fields "
        f"show the backdated values (bypassRules does not set them; we did).",
        f"Feature #{fid}: History tab - is there an extra 'link added' revision, and what Changed Date does it "
        f"have? (Probe above: {findings.get('parent_revisions')})",
        f"Assigned To on the story shows the plain display name (no avatar/profile) and does not raise errors.",
        f"Analytics revisions: open {prov.api.odata_revisions_url(prov.project, sid or 0)} in a browser signed "
        f"in to the org: expect Revisions 1-4 with the backdated ChangedDate, IterationPath moving to {sname}.",
        f"Team '{team['name']}' > Boards > Backlogs: the story is NOT on the backlog (Closed); the Feature is "
        f"Active on the Features backlog.",
        f"Dashboard > add a Velocity widget for team '{team['name']}' (Story Points): {sname} shows Planned 5 "
        f"and Completed 5 (the story entered the sprint on day 1 before end of day).",
        f"Team '{team['name']}' > Analytics/Cycle Time widget: cycle time for the story is 6-7 days "
        f"(Active day 1 -> Closed day 7); Lead time ~10 days.",
        f"Board for '{team['name']}': with 'Show completed' the story is in the Closed column (board column "
        f"follows bypassed state changes?).",
        "Queries: run 'Tags Contains pilot' - both pilot items appear; Changed Date of the story = its Closed "
        "time (not today).",
        f"User Story state categories (Resolved -> InProgress or Resolved?): "
        f"{findings.get('user_story_state_categories')}",
        f"Future ChangedDate probe: {findings.get('future_changed_date')}",
        f"Org time zone: Organization settings > Overview > Time zone. Event times 16:00-19:00 UTC keep the "
        f"same calendar day for US/EU zones; Asia/Pacific zones would shift a day.",
    ]
    for i, c in enumerate(checks, 1):
        log(f"   {i:2d}. {c}")
    log("\n  NEXT: if everything checks out, either remove the pilot items (--steps pilot-cleanup) or seed a "
        "fresh project. Then run the full seed with the recommended --order flag.")


def cleanup_pilot(prov: "Provisioner") -> None:
    prov.ensure_project_loaded()
    items = prov.state.section("pilot").get("items", {})
    for key in ("PILOT-S", "PILOT-F"):
        rec = items.get(key)
        if not rec:
            continue
        try:
            prov.send(prov.api.delete_work_item(prov.project_id, rec["id"]))
            prov.log(f"  Deleted {key} #{rec['id']} (moved to the Recycle Bin)")
        except AdoError as exc:
            if exc.status != 404:
                raise
        items.pop(key, None)
        prov.state.save()
    prov.manual("pilot-cleanup", "Empty the Recycle Bin (Boards > Work items > Recycle bin) to remove the pilot "
                                 "items permanently. Deleted items are excluded from Analytics.")

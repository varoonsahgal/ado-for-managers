"""Recompute every checkable World Bible number from a generated dataset's revisions.

Nothing here reads scenario.py: all numbers are derived by replaying the dataset's revision
history with Azure DevOps Analytics semantics, then compared with EXPECTED, a table transcribed
independently from facilitator/world-bible.md (sections 3-12).

Semantics
- Planned (sprint s) = Story Points of User Stories whose Iteration Path = s at the END OF DAY 1.
- Completed (s) = User Stories that entered Closed during s while assigned to s (points at that time).
- Carry-over (s) = stories in s at end of day 1, not Closed at the end of s, and in s+1 at the end
  of s+1's day 1.
- Cycle time = first entry into Active/Resolved -> entry into Closed (days, fractional).
- Bugs "open" = any state other than Closed. Sprint windows run Monday 00:00Z to the next sprint's Monday.
"""
from __future__ import annotations

import bisect
import datetime as dt
from collections import Counter, defaultdict

UTC = dt.timezone.utc
P = "HarborPoint"
WD_OFF = [0, 1, 2, 3, 4, 7, 8, 9, 10, 11]
TEAMS = ("Mobile Banking", "Digital Accounts", "Security", "Core Platform", "Branch Experience", "Member Support")
TEAM_AREA = {"Mobile Banking": P + "\\Digital\\Mobile Banking", "Digital Accounts": P + "\\Digital\\Digital Accounts",
             "Security": P + "\\Security", "Core Platform": P + "\\Core Platform",
             "Branch Experience": P + "\\Branch Experience", "Member Support": P + "\\Member Support"}
HIST = (9, 10, 11, 12, 13)
PI_OF = {s: (3 if s <= 12 else 4 if s <= 16 else 5) for s in range(9, 21)}

# ============================================================================ EXPECTED (World Bible)
EXPECTED = {
    # section 6 tables: sprint -> (planned, done, n done, (carry n, carry pts)). Member Support = what ADO
    # RECORDS (section 6.6): velocity 18,17,19,13,8. Recorded n and S13 planned are derived from the planted
    # problems: 2 (S12) and 3 (S13) stories left Resolved, and S13's taxonomy story has blank points (3).
    "velocity": {
        "Mobile Banking": {9: (38, 33, 12, (2, 5)), 10: (44, 37, 12, (3, 7)), 11: (50, 41, 13, (4, 9)),
                           12: (56, 45, 12, (5, 11)), 13: (62, 44, 12, (6, 18))},
        "Digital Accounts": {9: (26, 24, 9, (1, 2)), 10: (26, 26, 10, (0, 0)), 11: (25, 25, 10, (0, 0)),
                             12: (27, 24, 9, (1, 3)), 13: (26, 26, 10, (0, 0))},
        "Security": {9: (24, 22, 8, (1, 2)), 10: (25, 21, 8, (1, 4)), 11: (26, 22, 8, (1, 4)),
                     12: (30, 21, 7, (3, 9)), 13: (32, 20, 7, (4, 12))},
        "Core Platform": {9: (21, 20, 7, (1, 1)), 10: (22, 20, 7, (1, 2)), 11: (21, 21, 7, (0, 0)),
                          12: (21, 19, 7, (1, 2)), 13: (22, 20, 7, (1, 2))},
        "Branch Experience": {9: (19, 18, 7, (1, 1)), 10: (20, 17, 6, (1, 3)), 11: (18, 18, 7, (0, 0)),
                              12: (19, 16, 6, (1, 3)), 13: (20, 18, 7, (1, 2))},
        "Member Support": {9: (20, 18, 7, (1, 2)), 10: (19, 17, 6, (1, 2)), 11: (21, 19, 7, (1, 2)),
                           12: (20, 13, 5, (1, 2)), 13: (18, 8, 4, (1, 2))},
    },
    "ms_true_done": {9: (7, 18), 10: (6, 17), 11: (7, 19), 12: (7, 18), 13: (7, 19)},
    "ms_resolved_left": {12: (2, 5), 13: (3, 8)},
    "ms_blank_closed": {13: ["Request category taxonomy cleanup"]},
    "ms_blank_true_pts": {(13, "F13"): 3},
    "ms_recorded_velocity": [18, 17, 19, 13, 8],
    # closed-story mix by Feature (n, pts); None = orphan. Member Support = true mix (closed + left Resolved).
    "mix": {
        "Mobile Banking": {9: {"F1": (9, 24), None: (3, 9)}, 10: {"F1": (6, 18), "F2": (3, 8), None: (3, 11)},
                           11: {"F1": (4, 13), "F2": (5, 16), None: (4, 12)},
                           12: {"F2": (4, 15), "F3": (4, 14), None: (4, 16)},
                           13: {"F2": (3, 11), "F3": (3, 10), None: (6, 23)}},
        "Digital Accounts": {9: {"F8": (7, 19), None: (2, 5)}, 10: {"F8": (5, 13), "F7": (4, 10), None: (1, 3)},
                             11: {"F8": (4, 10), "F7": (3, 8), "F6": (2, 5), None: (1, 2)},
                             12: {"F8": (2, 5), "F7": (3, 8), "F6": (4, 11)},
                             13: {"F8": (2, 5), "F7": (2, 5), "F6": (5, 14), None: (1, 2)}},
        "Security": {9: {"F10": (5, 14), None: (3, 8)}, 10: {"F10": (4, 11), "F11": (3, 8), None: (1, 2)},
                     11: {"F10": (3, 9), "F11": (3, 8), None: (2, 5)},
                     12: {"F10": (2, 6), "F11": (2, 5), "F21": (3, 10)},
                     13: {"F10": (1, 3), "F11": (1, 3), "F21": (3, 9), "F22": (2, 5)}},
        "Core Platform": {9: {"F24": (5, 15), None: (2, 5)}, 10: {"F24": (5, 14), None: (2, 6)},
                          11: {"F24": (3, 9), "F23": (3, 9), None: (1, 3)},
                          12: {"F24": (3, 8), "F23": (3, 9), None: (1, 2)},
                          13: {"F24": (2, 6), "F23": (4, 11), None: (1, 3)}},
        "Branch Experience": {9: {"F17": (6, 16), None: (1, 2)}, 10: {"F17": (5, 14), None: (1, 3)},
                              11: {"F17": (4, 11), "F19": (3, 7)},
                              12: {"F17": (2, 5), "F19": (3, 8), None: (1, 3)},
                              13: {"F19": (3, 8), "F18": (2, 5), None: (2, 5)}},
        "Member Support": {9: {"F15": (5, 13), None: (2, 5)}, 10: {"F15": (5, 14), None: (1, 3)},
                           11: {"F15": (3, 8), "F13": (4, 11)},
                           12: {"F15": (2, 5), "F13": (4, 11), None: (1, 2)},
                           13: {"F13": (4, 11), "F14": (2, 5), None: (1, 3)}},
    },
    "mobile_cycle": {9: 3.5, 10: 4.5, 11: 6.0, 12: 7.5, 13: 9.0},
    "cycle_tolerance": 0.3,
    "da_cycle_range": (4.0, 5.0),
    "steady_cycle_range": (3.0, 6.0),
    "mobile_orphan_pct": {9: 27, 10: 30, 11: 29, 12: 36, 13: 52},
    "mobile_reliability_pct": {9: 87, 10: 84, 11: 82, 12: 80, 13: 71},
    # Bible: "Commitment reliability 92-100%" but its own table gives S12 24/27 = 89%. We expect the table.
    "da_reliability_pct": {9: 92, 10: 100, 11: 100, 12: 89, 13: 100},
    "da_velocity_mean": 25.0, "da_velocity_range": (24, 26),
    "da_orphan_pct_aggregate_max": 12,  # "Orphan share is low (<= 12%)": read as the S9-S13 aggregate
    # bugs: start (open before S9), per sprint (opened, closed, open at end; S14 = now)
    "bugs": {
        "Mobile Banking": dict(start=8, flow={9: (4, 3, 9), 10: (6, 3, 12), 11: (8, 2, 18), 12: (11, 3, 26),
                                              13: (13, 2, 37), 14: (6, 1, 42)}),
        "Digital Accounts": dict(start=7, flow={9: (3, 3, 7), 10: (2, 3, 6), 11: (3, 3, 6), 12: (2, 3, 5),
                                                13: (2, 3, 4), 14: (1, 1, 4)}),
        "Member Support": dict(start=5, flow={9: (2, 2, 5), 10: (2, 1, 6), 11: (2, 2, 6), 12: (3, 1, 8),
                                              13: (3, 1, 10), 14: (2, 0, 12)}),
    },
    "mobile_open_severity": {"1 - Critical": 3, "2 - High": 11, "3 - Medium": 18, "4 - Low": 10},
    "mobile_open_priority": {1: 4, 2: 14, 3: 18, 4: 6},
    "mobile_open_state": {"New": 30, "Active": 9, "Resolved": 3},
    "mobile_p1_unassigned": ["Check deposit fails for images larger than 5 MB"],
    "mobile_escaped_since_s11_pct": (40, 50),  # "about 45%"
    # Sprint 14 snapshot (section 6): planned at end of day 1, added later, totals, state counts (n, pts)
    "s14": {
        "Mobile Banking": dict(planned=60, added=5, total=(19, 65), Closed=(4, 12), Resolved=(3, 11), Active=7,
                               New=5, by_parent={"F2": (8, 29), "F3": (3, 11), "F9": (3, 13), None: (5, 12)}),
        "Digital Accounts": dict(planned=26, added=0, total=(9, 26), Closed=(4, 10), Active=3, New=2),
        "Security": dict(planned=36, added=0, total=(10, 36), Closed=(2, 6)),
        "Core Platform": dict(planned=22, added=0, total=(7, 22), Closed=(2, 5)),
        "Branch Experience": dict(planned=19, added=0, total=(7, 19), Closed=(2, 5)),
        # Derived from the section 6.6 item table (the Bible gives no totals): 8 items, 23 pts.
        "Member Support": dict(planned=23, added=0, total=(8, 23), Closed=(1, 3), Resolved=(1, 3), Active=4, New=2),
    },
    "security_compliance_pct": 58,
    "security_features_in_progress": ["F10", "F11", "F21", "F22"],
    # section 5: key -> (child stories, pts total, pts done (Closed), %, state). F13/F14 derived from 6.6.
    "features": {
        "F1": (19, 55, 55, 100, "Closed"), "F2": (26, 93, 57, 61, "Active"), "F3": (15, 51, 27, 53, "Active"),
        "F4": (0, 0, 0, None, "New"), "F5": (20, 105, 0, 0, "New"), "F6": (19, 56, 33, 59, "Active"),
        "F7": (17, 43, 38, 88, "Active"), "F8": (20, 52, 52, 100, "Closed"), "F9": (11, 51, 2, 4, "Active"),
        "F10": (21, 65, 43, 66, "Active"), "F11": (14, 43, 27, 63, "Active"), "F12": (8, 34, 0, 0, "New"),
        "F13": (22, 53, 20, 38, "Active"), "F14": (7, 20, 5, 25, "New"), "F15": (15, 40, 40, 100, "Active"),
        "F16": (6, 21, 0, 0, "New"), "F17": (17, 46, 46, 100, "Closed"), "F18": (10, 33, 5, 15, "Active"),
        "F19": (13, 33, 28, 85, "Active"), "F20": (5, 21, 0, 0, "New"), "F21": (13, 43, 22, 51, "Active"),
        "F22": (7, 23, 5, 22, "Active"), "F23": (14, 38, 31, 82, "Active"), "F24": (22, 68, 55, 81, "Active"),
    },
    "feature_target": {"F1": 11, "F2": 14, "F3": 16, "F4": 20, "F5": 17, "F6": 16, "F7": 15, "F8": 13, "F9": 16,
                       "F10": 17, "F11": 16, "F12": 20, "F13": 15, "F14": 17, "F15": 12, "F16": 19, "F17": 12,
                       "F18": 17, "F19": 15, "F20": 20, "F21": 18, "F22": 18, "F23": 15, "F24": 16},
    "feature_closed_sprint": {"F1": 11, "F8": 13, "F17": 12},
    "feature_owner": {"Mobile Banking": "Hannah Cole", "Digital Accounts": "Ben Adeyemi", "Security": "Aisha Karimi",
                      "Core Platform": "Nadia Petrova", "Branch Experience": "Maya Johnson",
                      "Member Support": "Isaac Thompson"},
    "f5_estimated": (16, 105), "f5_unestimated": 4, "f5_mvp_pts": 44,
    "f5_mvp_titles": ["Card lock and unlock service and API", "Lock and unlock a card in online banking and the app",
                      "Real-time card status sync with card processor", "Travel notice self-service",
                      "Card control change notifications", "Card controls audit trail",
                      "Accessibility review for card controls", "Fraud team view of member-locked cards"],
    "f5_should_title": "Travel notice auto-expiry and reminders",
    "lab3_at_risk": ["F2", "F7", "F9", "F13", "F15", "F19", "F21", "F23"],
    "lab3_high_priority_incomplete": ["F2", "F5", "F9", "F10", "F21"],
    "lab3_completed_last_sprint_digital": ["F2", "F3", "F6", "F7", "F8"],
    "features_without_children": ["F4"],
    "features_without_target": [],
    "e2_features": {"count": 8, "Closed": 2, "Active": 4, "New": 2},
    "f9_child_areas": 3,
    "epic_order": ["E1", "E2", "E3", "E4", "E5", "E6"],
    "e6_created": (12, 3),
    "ethan_active": 6,
    "kyle_items": {"Active": 2, "New": 2},
    "ms_zombies": 3, "ms_root_p1_bugs": 2, "ms_open_p1_in_area": 0, "ms_removed": 4, "ms_resolved": 6,
    "ms_open_work_inflation": 10,
    "f13_tags": {"omnichannel": 6, "omni-channel": 3, "omnichanel": 2},
    "f14_child_states": {"Closed": 2, "Resolved": 1, "Active": 2, "New": 2},
    "duplicate_title": ("Service request status tracker", 2),
    "dependencies": {("F10", "F9"): "conflict", ("F23", "F9"): "ok", ("F24", "F4"): "ok",
                     ("SEC-1", "MB-15"): "conflict", ("SEC-1", "MB-2"): "conflict",
                     ("SEC-2", "MB-5"): "same sprint", ("CP-1", "MB-4"): "ok",
                     ("F5-01", "MB-5"): "hidden risk (predecessor unscheduled)"},
    "f10_change": dict(sprint=14, day=2, old_target=15, new_target=17,
                       comment=("Re-planned: exam-readiness work (F21/F22) takes priority until exam fieldwork in "
                                "Sprint 18. The risk-score API for Fraud Alerts moves to Sprint 16. — AK")),
    "f2_at_risk_sprint": 13,
    # staleness: (min, max) calendar days between the last change and "now"
    "stale": {"Auto-capture check edges with on-device ML": (9, 11), "Retry flow for failed check uploads": (10, 12)},
    "qa_wait": {"Deposit limit messaging by member tier": (5, 7), "Face ID and fingerprint enrollment": (4, 6),
                "Biometric step-up for high-risk actions": (1, 3)},
    "kyle_min_age": 25, "zombie_min_age": 25, "recent_touch_days": (1, 3),
    "mobile_added": {"Holiday promo banner (marketing request)": 3, "App Store listing refresh": 4},
    "lab9_forecast": {25: (12, 73), 20: (10, 55), 15: (8, 42)},
    "lab9_mvp_reordered_lands_at": 15,
    "sandbox_l11": {  # n -> (type, state, sprint or None, points or None, tag or None, area)
        1: ("User Story", "Resolved", 13, 3, "omnichannel", "P"), 2: ("User Story", "Resolved", 13, 2, "omni-channel", "P"),
        3: ("User Story", "Closed", 13, 5, None, "P"), 4: ("User Story", "Closed", 13, None, None, "P"),
        5: ("User Story", "Active", 14, 3, "omnichannel", "P"), 6: ("User Story", "New", 14, 3, "omni-channel", "P"),
        7: ("User Story", "Active", 12, 3, None, "P"), 8: ("User Story", "Active", 12, 5, None, "P"),
        9: ("User Story", "Active", 12, 2, None, "P"), 10: ("User Story", "New", 15, None, None, "P"),
        11: ("User Story", "Closed", 14, 3, None, "P"), 12: ("User Story", "Active", 14, 5, "omnichanel", "P"),
        13: ("User Story", "Active", 14, 2, "omnichannel", "P"), 14: ("Bug", "New", None, None, None, "Training"),
        15: ("Bug", "Active", None, None, None, "Training"), 16: ("Bug", "Active", None, None, None, "P"),
        17: ("User Story", "Removed", None, None, None, "P"), 18: ("User Story", "Removed", None, None, None, "P"),
    },
    "default_team_areas": [("", False), ("Digital", True), ("Security", True), ("Core Platform", True),
                           ("Branch Experience", True), ("Member Support", True)],
}


# ============================================================================ replay model
def ts(s: str) -> dt.datetime:
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


class WI:
    def __init__(self, raw: dict):
        self.key, self.type, self.parent, self.links = raw["key"], raw["type"], raw["parent"], raw["links"]
        self.times, self.snaps, self.revs = [], [], raw["revisions"]
        cur = {}
        for r in raw["revisions"]:
            cur = {**cur, **r["fields"]}
            self.times.append(ts(r["at"]))
            self.snaps.append(cur)
        self.final = cur

    def at(self, t: dt.datetime) -> dict | None:
        i = bisect.bisect_right(self.times, t)
        return self.snaps[i - 1] if i else None

    def get(self, field, t=None, default=None):
        s = self.final if t is None else self.at(t)
        return default if s is None else s.get(field, default)

    @property
    def title(self):
        return self.final["System.Title"]

    @property
    def area(self):
        return self.final["System.AreaPath"]

    @property
    def created(self):
        return self.times[0]

    def changes(self, field):
        """[(time, old, new)] for every revision that changed field."""
        out, prev = [], None
        for t, snap in zip(self.times, self.snaps):
            v = snap.get(field)
            if v != prev:
                out.append((t, prev, v))
            prev = v
        return out

    def entered(self, state):
        return [t for t, _o, n in self.changes("System.State") if n == state]

    def tags(self, t=None):
        s = self.get("System.Tags", t, "") or ""
        return [x.strip() for x in s.split(";") if x.strip()]

    def pts(self, t=None):
        return self.get("Microsoft.VSTS.Scheduling.StoryPoints", t) or 0


class Facts:
    def __init__(self, data: dict):
        self.data = data
        self.now = ts(data["now"])
        self.s14 = dt.date.fromisoformat(data["calendar"]["sprint14_start"])
        self.items = [WI(w) for w in data["work_items"]]
        self.by_key = {w.key: w for w in self.items}
        self.checks: list[dict] = []
        self.out: dict = {}

    # --- calendar
    def start(self, n):
        return self.s14 + dt.timedelta(days=14 * (n - 14))

    def finish(self, n):
        return self.start(n) + dt.timedelta(days=11)

    def day(self, n, d):
        return self.start(n) + dt.timedelta(days=WD_OFF[d - 1])

    @staticmethod
    def eod(d: dt.date) -> dt.datetime:
        return dt.datetime(d.year, d.month, d.day, 23, 59, 59, tzinfo=UTC)

    def window(self, n):
        a = self.start(n)
        b = self.start(n + 1)
        return dt.datetime(a.year, a.month, a.day, tzinfo=UTC), dt.datetime(b.year, b.month, b.day, tzinfo=UTC)

    def sprint_end(self, n):
        return min(self.eod(self.finish(n)), self.now)

    def sprint_day_of(self, t: dt.datetime):
        """(sprint, day) for a working-day timestamp."""
        off = (t.date() - self.start(9)).days
        n, o = 9 + off // 14, off % 14
        return n, (WD_OFF.index(o) + 1 if o in WD_OFF else None)

    def iter_path(self, n):
        return f"{P}\\PI {PI_OF[n]}\\Sprint {n}"

    def sprint_of_path(self, path):
        if path and "\\Sprint " in path:
            return int(path.rsplit(" ", 1)[1])
        return None

    def sprint_of_finish(self, d: dt.date):
        for n in range(1, 30):
            if self.finish(n) == d:
                return n
        return None

    # --- selections
    def stories(self, area=None, under=None):
        out = [w for w in self.items if w.type == "User Story"]
        if area:
            out = [w for w in out if w.area == area]
        if under:
            out = [w for w in out if w.area == under or w.area.startswith(under + "\\")]
        return out

    def bugs(self, area=None, under=None):
        out = [w for w in self.items if w.type == "Bug"]
        if area is not None:
            out = [w for w in out if w.area == area]
        if under:
            out = [w for w in out if w.area == under or w.area.startswith(under + "\\")]
        return out

    def real(self, w):
        return not w.area.startswith(P + "\\Training")

    # --- checks
    def check(self, cid, expected, actual, ok=None, note=""):
        if ok is None:
            ok = expected == actual
        self.checks.append(dict(id=cid, expected=expected, actual=actual, ok=bool(ok), note=note))
        return ok

    # ======================================================================= computations
    def velocity(self, team, n):
        area = TEAM_AREA[team]
        path = self.iter_path(n)
        d1 = self.eod(self.day(n, 1))
        w0, w1 = self.window(n)
        end = self.sprint_end(n)
        planned, comp, carry, resolved_left, blank = [], [], [], [], []
        for w in self.stories(area):
            if w.get("System.IterationPath", d1) == path and w.get("System.State", d1) != "Removed":
                planned.append(w)
                closed_at_end = w.get("System.State", end) == "Closed"
                if n < 14 and not closed_at_end:
                    nxt = self.eod(self.day(n + 1, 1))
                    if w.get("System.IterationPath", nxt) == self.iter_path(n + 1):
                        carry.append(w)
                    elif w.get("System.State", end) == "Resolved":
                        resolved_left.append(w)
            for t in w.entered("Closed"):
                if w0 <= t < w1 and t <= self.now and w.get("System.IterationPath", t) == path:
                    comp.append((w, t))
                    if not w.get("Microsoft.VSTS.Scheduling.StoryPoints", t):
                        blank.append(w.title)
        return dict(planned=sum(w.pts(d1) for w in planned),
                    done=sum(w.pts(t) for w, t in comp), n=len(comp),
                    carry=(len(carry), sum(w.pts(end) for w in carry)),
                    resolved_left=(len(resolved_left), sum(w.pts(end) for w in resolved_left)),
                    blank_closed=blank, completed=comp)

    def cycle(self, comp):
        cts, dwell = [], []
        for w, t in comp:
            starts = [x for x in w.entered("Active") + w.entered("Resolved") if x <= t]
            if starts:
                cts.append((t - min(starts)).total_seconds() / 86400)
            res = [x for x in w.entered("Resolved") if x <= t]
            if res:
                dwell.append((t - max(res)).total_seconds() / 86400)
        avg = lambda v: round(sum(v) / len(v), 2) if v else None
        return avg(cts), avg(dwell), (round(min(cts), 2), round(max(cts), 2)) if cts else None

    def mix(self, comp, extra=()):
        m = defaultdict(lambda: [0, 0])
        for w, t in list(comp) + list(extra):
            m[w.parent][0] += 1
            m[w.parent][1] += w.pts(t)
        return {k: tuple(v) for k, v in m.items()}

    def bug_flow(self, team):
        area = TEAM_AREA[team]
        bugs = self.bugs(area)
        s9 = dt.datetime.combine(self.start(9), dt.time(0), UTC)
        start_open = sum(1 for b in bugs if b.created < s9 and b.get("System.State", s9) != "Closed")
        flow = {}
        for n in range(9, 15):
            w0, w1 = self.window(n)
            end = self.sprint_end(n)
            opened = sum(1 for b in bugs if w0 <= b.created < w1)
            closed = sum(1 for b in bugs for t in b.entered("Closed") if w0 <= t < w1)
            open_end = sum(1 for b in bugs if b.created <= end and b.get("System.State", end) != "Closed")
            flow[n] = (opened, closed, open_end)
        return start_open, flow

    def s14_snapshot(self, team):
        area = TEAM_AREA[team]
        path = self.iter_path(14)
        d1 = self.eod(self.day(14, 1))
        items = [w for w in self.stories(area) if w.get("System.IterationPath") == path]
        snap = dict(planned=sum(w.pts(d1) for w in items if w.get("System.IterationPath", d1) == path),
                    added=sum(w.pts() for w in items if w.get("System.IterationPath", d1) != path),
                    total=(len(items), sum(w.pts() for w in items)))
        for st in ("Closed", "Resolved", "Active", "New"):
            sel = [w for w in items if w.final["System.State"] == st]
            snap[st] = (len(sel), sum(w.pts() for w in sel))
        bp = defaultdict(lambda: [0, 0])
        for w in items:
            bp[w.parent][0] += 1
            bp[w.parent][1] += w.pts()
        snap["by_parent"] = {k: tuple(v) for k, v in bp.items()}
        return snap, items

    # ======================================================================= run all
    def run(self):
        E = EXPECTED
        self.structural()
        self.out["velocity"], self.out["mix"], self.out["cycle"] = {}, {}, {}
        for team in TEAMS:
            ev = E["velocity"][team]
            vt, mt, ct = {}, {}, {}
            for n in HIST:
                v = self.velocity(team, n)
                vt[n] = dict(planned=v["planned"], done=v["done"], n=v["n"], carry=v["carry"],
                             resolved_left=v["resolved_left"], blank_closed=v["blank_closed"])
                p, d, k, c = ev[n]
                self.check(f"velocity.{team}.S{n}", dict(planned=p, done=d, n=k, carry=c),
                           dict(planned=v["planned"], done=v["done"], n=v["n"], carry=v["carry"]))
                resolved_extra = []
                if team == "Member Support":
                    self.check(f"ms.resolved_left.S{n}", E["ms_resolved_left"].get(n, (0, 0)), v["resolved_left"])
                    self.check(f"ms.blank_closed.S{n}", E["ms_blank_closed"].get(n, []), v["blank_closed"])
                    area = TEAM_AREA[team]
                    end = self.sprint_end(n)
                    resolved_extra = [(w, end) for w in self.stories(area)
                                      if w.get("System.IterationPath", self.eod(self.day(n, 1))) == self.iter_path(n)
                                      and w.get("System.State", end) == "Resolved"
                                      and w.get("System.IterationPath", end) == self.iter_path(n)]
                    tn = v["n"] + len(resolved_extra)
                    tp = v["done"] + sum(w.pts(t) for w, t in resolved_extra) + \
                        sum(x for (s, _g), x in E["ms_blank_true_pts"].items() if s == n)
                    self.check(f"ms.true_done.S{n}", E["ms_true_done"][n], (tn, tp))
                m = self.mix(v["completed"], resolved_extra)
                exp_m = dict(E["mix"][team][n])
                if team == "Member Support":
                    exp_m = {g: (a, b - E["ms_blank_true_pts"].get((n, g), 0)) for g, (a, b) in exp_m.items()}
                mt[n] = m
                self.check(f"mix.{team}.S{n}", exp_m, m)
                avg, dwell, rng_ = self.cycle(v["completed"])
                ct[n] = dict(avg=avg, resolved_dwell=dwell, range=rng_)
            self.out["velocity"][team], self.out["mix"][team], self.out["cycle"][team] = vt, mt, ct
            # cycle-time profiles
            if team == "Mobile Banking":
                for n in HIST:
                    a = ct[n]["avg"]
                    self.check(f"cycle.Mobile.S{n}", E["mobile_cycle"][n], a,
                               ok=a is not None and abs(a - E["mobile_cycle"][n]) <= E["cycle_tolerance"])
                dw = [ct[n]["resolved_dwell"] for n in HIST]
                self.check("cycle.Mobile.resolved_dwell_rising", "strictly increasing", dw,
                           ok=all(x < y for x, y in zip(dw, dw[1:])))
            else:
                lo, hi = E["da_cycle_range"] if team == "Digital Accounts" else E["steady_cycle_range"]
                avgs = [ct[n]["avg"] for n in HIST]
                self.check(f"cycle.{team}.steady", f"{lo}-{hi} days", avgs,
                           ok=all(a is not None and lo <= a <= hi for a in avgs))
        self.check("ms.recorded_velocity", E["ms_recorded_velocity"],
                   [self.out["velocity"]["Member Support"][n]["done"] for n in HIST])
        self.lifecycle_rules()
        self.mobile_signals()
        self.digital_accounts_signals()
        self.bug_facts()
        self.sprint14_facts()
        self.feature_facts()
        self.portfolio_queries()
        self.people_and_hygiene()
        self.dependency_facts()
        self.staleness_facts()
        self.lab9_facts()
        self.sandbox_facts()
        self.team_facts()
        return self

    # ----------------------------------------------------------------------- structural
    def structural(self):
        data, now = self.data, self.now
        problems = []
        if data.get("schema") != "harborpoint-dataset/1":
            problems.append("schema")
        areas = {P} | {f"{P}\\{a}" for a in data["areas"]}
        iters = {P} | {f"{P}\\{i['path']}" for i in data["calendar"]["iterations"]}
        seen = set()
        for w in self.items:
            if w.parent and w.parent not in seen:
                problems.append(f"{w.key}: parent after child")
            seen.add(w.key)
            for a, b in zip(w.times, w.times[1:]):
                if not a < b:
                    problems.append(f"{w.key}: times not strictly increasing")
            for i, (t, r) in enumerate(zip(w.times, w.revs)):
                if t > now:
                    problems.append(f"{w.key}: revision after now")
                if t.weekday() >= 5 or not (16 <= t.hour < 19 or (t.hour == 19 and t.minute == 0)):
                    problems.append(f"{w.key}: revision outside 16:00-19:00 UTC working day ({r['at']})")
                f = r["fields"]
                if i == 0 and (f.get("System.State") != "New" or "Microsoft.VSTS.Common.StackRank" not in f):
                    problems.append(f"{w.key}: revision 1 must be New with StackRank")
                if i > 0 and "System.State" in f:
                    st = f["System.State"]
                    if f.get("Microsoft.VSTS.Common.StateChangeDate") != r["at"] or not f.get("System.Reason"):
                        problems.append(f"{w.key}: state change without StateChangeDate/Reason")
                    need = {"Resolved": "Microsoft.VSTS.Common.ResolvedDate",
                            "Closed": "Microsoft.VSTS.Common.ClosedDate"}.get(st)
                    if need and f.get(need) != r["at"]:
                        problems.append(f"{w.key}: {st} without {need}")
            if w.entered("Active") and w.final.get("Microsoft.VSTS.Common.ActivatedDate") != \
                    w.revs[[i for i, s in enumerate(w.snaps) if s.get("System.State") == "Active"][0]]["at"]:
                problems.append(f"{w.key}: ActivatedDate mismatch")
            for snap in (w.snaps[0], w.final):
                if snap["System.AreaPath"] not in areas:
                    problems.append(f"{w.key}: unknown area {snap['System.AreaPath']}")
                if snap["System.IterationPath"] not in iters:
                    problems.append(f"{w.key}: unknown iteration {snap['System.IterationPath']}")
            for ln in w.links:
                if ln["target"] not in self.by_key:
                    problems.append(f"{w.key}: link target {ln['target']} missing")
        # unique titles among real-team stories/bugs except the planted duplicate
        titles = Counter(w.title for w in self.items if self.real(w) and w.type in ("User Story", "Bug"))
        dups = {t: c for t, c in titles.items() if c > 1}
        self.check("structure.problems", [], problems[:20], ok=not problems, note=f"{len(problems)} problems")
        self.check("structure.duplicate_titles", {EXPECTED["duplicate_title"][0]: EXPECTED["duplicate_title"][1]}, dups)
        self.out["counts"] = dict(work_items=len(self.items), revisions=sum(len(w.times) for w in self.items),
                                  by_type=dict(Counter(w.type for w in self.items)))

    # ----------------------------------------------------------------------- lifecycle rules (section 12)
    def lifecycle_rules(self):
        E = EXPECTED
        bad_days, not_via_resolved, late_s14 = [], [], []
        resolved_use = Counter()
        d5 = self.eod(self.day(14, 5))
        w14 = self.window(14)[0]
        for team in TEAMS:
            for n in HIST:
                for w, t in self.velocity(team, n)["completed"]:
                    if w.get("System.IterationPath", self.eod(self.day(n, 1))) != self.iter_path(n):
                        continue
                    cn, cd = self.sprint_day_of(t)
                    acts = w.entered("Active")
                    an, ad = self.sprint_day_of(acts[0])
                    if not (cn == n and cd and 2 <= cd <= 10 and ad and 1 <= ad <= 6):
                        bad_days.append(f"{w.key}: activated S{an} d{ad}, closed S{cn} d{cd}")
                    res = [x for x in w.entered("Resolved") if x <= t]
                    resolved_use[(team == "Mobile Banking", bool(res))] += 1
                    if team == "Mobile Banking" and not res:
                        not_via_resolved.append(w.key)
        for w in self.items:
            if not self.real(w):
                continue
            for t, r in zip(w.times, w.revs):
                if t > d5 and t >= w14:
                    f = set(r["fields"])
                    qa = w.title in E["qa_wait"] and r["fields"].get("System.State") == "Resolved"
                    if f and not qa:
                        late_s14.append(f"{w.key} {r['at']} {sorted(f)}")
        self.check("lifecycle.history_days", "activated days 1-6, closed days 2-10", bad_days[:10], ok=not bad_days)
        self.check("lifecycle.mobile_via_resolved", [], not_via_resolved, ok=not not_via_resolved)
        other = resolved_use[(False, True)] / max(1, resolved_use[(False, True)] + resolved_use[(False, False)])
        self.check("lifecycle.other_teams_resolved_share", "about 30%", round(100 * other), ok=0.15 <= other <= 0.45)
        self.check("lifecycle.s14_explicit_events_days_1_5",
                   "after S14 day 5 only comments (touches) and now-relative QA-wait resolutions", late_s14[:10],
                   ok=not late_s14)

    # ----------------------------------------------------------------------- team signals
    def mobile_signals(self):
        E, v = EXPECTED, self.out["velocity"]["Mobile Banking"]
        orphan = {n: round(100 * self.out["mix"]["Mobile Banking"][n].get(None, (0, 0))[1] / v[n]["done"])
                  for n in HIST}
        rel = {n: round(100 * v[n]["done"] / v[n]["planned"]) for n in HIST}
        self.out["mobile_orphan_pct"], self.out["mobile_reliability_pct"] = orphan, rel
        self.check("mobile.orphan_pct", E["mobile_orphan_pct"], orphan)
        self.check("mobile.reliability_pct", E["mobile_reliability_pct"], rel)

    def digital_accounts_signals(self):
        E, v = EXPECTED, self.out["velocity"]["Digital Accounts"]
        rel = {n: round(100 * v[n]["done"] / v[n]["planned"]) for n in HIST}
        vel = [v[n]["done"] for n in HIST]
        orph = sum(self.out["mix"]["Digital Accounts"][n].get(None, (0, 0))[1] for n in HIST)
        agg = round(100 * orph / sum(vel), 1)
        per = {n: round(100 * self.out["mix"]["Digital Accounts"][n].get(None, (0, 0))[1] / v[n]["done"])
               for n in HIST}
        self.out["da"] = dict(reliability_pct=rel, velocity=vel, mean=sum(vel) / len(vel), orphan_pct=per,
                              orphan_pct_aggregate=agg)
        self.check("da.reliability_pct", E["da_reliability_pct"], rel)
        self.check("da.velocity_mean", E["da_velocity_mean"], sum(vel) / len(vel))
        self.check("da.velocity_range", E["da_velocity_range"], (min(vel), max(vel)))
        self.check("da.orphan_pct_aggregate", f"<= {E['da_orphan_pct_aggregate_max']}", agg,
                   ok=agg <= E["da_orphan_pct_aggregate_max"], note=f"per sprint {per}")

    def bug_facts(self):
        E = EXPECTED
        self.out["bugs"] = {}
        for team in TEAMS:
            start, flow = self.bug_flow(team)
            self.out["bugs"][team] = dict(start=start, flow=flow)
            if team in E["bugs"]:
                self.check(f"bugs.{team}", E["bugs"][team], dict(start=start, flow=flow))
        mob = [b for b in self.bugs(TEAM_AREA["Mobile Banking"]) if b.final["System.State"] != "Closed"]
        sev = dict(Counter(b.final["Microsoft.VSTS.Common.Severity"] for b in mob))
        pri = dict(Counter(b.final["Microsoft.VSTS.Common.Priority"] for b in mob))
        st = dict(Counter(b.final["System.State"] for b in mob))
        p1u = sorted(b.title for b in mob if b.final["Microsoft.VSTS.Common.Priority"] == 1
                     and not b.final.get("System.AssignedTo"))
        s11 = dt.datetime.combine(self.start(11), dt.time(0), UTC)
        since = [b for b in self.bugs(TEAM_AREA["Mobile Banking"]) if b.created >= s11]
        esc = [b for b in since if "escaped-defect" in b.tags()]
        pct = round(100 * len(esc) / len(since), 1)
        self.out["mobile_open_bugs"] = dict(severity=sev, priority=pri, state=st, p1_unassigned=p1u,
                                            escaped_since_s11=f"{len(esc)}/{len(since)} = {pct}%")
        self.check("mobile.open_bugs.severity", E["mobile_open_severity"], sev)
        self.check("mobile.open_bugs.priority", E["mobile_open_priority"], pri)
        self.check("mobile.open_bugs.state", E["mobile_open_state"], st)
        self.check("mobile.p1_unassigned", E["mobile_p1_unassigned"], p1u)
        lo, hi = E["mobile_escaped_since_s11_pct"]
        self.check("mobile.escaped_defect_share", f"{lo}-{hi}%", pct, ok=lo <= pct <= hi)

    def sprint14_facts(self):
        E = EXPECTED
        self.out["s14"] = {}
        for team in TEAMS:
            snap, items = self.s14_snapshot(team)
            v14 = self.velocity(team, 14)
            snap["done_so_far"] = (v14["n"], v14["done"])
            self.out["s14"][team] = snap
            exp = E["s14"][team]
            act = {}
            for k, val in exp.items():
                if k in ("Active", "New"):
                    act[k] = snap[k][0]
                else:
                    act[k] = snap[k]
            self.check(f"s14.{team}", exp, act)
        sec, _ = self.s14_snapshot("Security")
        sec_items = [w for w in self.stories(TEAM_AREA["Security"])
                     if w.get("System.IterationPath") == self.iter_path(14)]
        comp = sum(w.pts() for w in sec_items if w.parent in ("F21", "F22"))
        pct = round(100 * comp / sec["total"][1])
        # "4 Features in progress at once": Active Features with Security work in Sprint 14
        inprog = sorted({w.parent for w in sec_items if w.parent
                         and self.by_key[w.parent].final["System.State"] == "Active"
                         and self.by_key[w.parent].area == TEAM_AREA["Security"]}, key=lambda k: int(k[1:]))
        self.out["security_compliance"] = dict(points=comp, total=sec["total"][1], pct=pct, features_in_progress=inprog)
        self.check("security.compliance_pct", E["security_compliance_pct"], pct)
        self.check("security.features_in_progress", E["security_features_in_progress"], inprog)
        added = {w.title: self.sprint_day_of(w.created) for w in self.stories(TEAM_AREA["Mobile Banking"])
                 if w.title in E["mobile_added"]}
        self.check("mobile.mid_sprint_additions", {t: (14, d) for t, d in E["mobile_added"].items()}, added)

    def feature_facts(self):
        E = EXPECTED
        res = {}
        feats = [w for w in self.items if w.type == "Feature" and self.real(w)]
        for f in feats:
            ch = [w for w in self.items if w.type == "User Story" and w.parent == f.key
                  and w.final["System.State"] != "Removed"]
            tot = sum(w.pts() for w in ch)
            done = sum(w.pts() for w in ch if w.final["System.State"] == "Closed")
            tgt = self.sprint_of_finish(ts(f.final["Microsoft.VSTS.Scheduling.TargetDate"]).date())
            res[f.key] = dict(title=f.title, state=f.final["System.State"], children=len(ch), pts=tot, done=done,
                              pct=round(100 * done / tot) if tot else None, target=tgt,
                              iteration=f.final["System.IterationPath"], owner=f.final.get("System.AssignedTo"),
                              tags=f.tags(), priority=f.final.get("Microsoft.VSTS.Common.Priority"),
                              risk=f.final.get("Microsoft.VSTS.Common.Risk"), area=f.area,
                              child_areas=sorted({w.area for w in ch}))
            r = res[f.key]
            self.check(f"feature.{f.key}", E["features"][f.key],
                       (r["children"], r["pts"], r["done"], r["pct"], r["state"]))
            self.check(f"feature.{f.key}.target", E["feature_target"][f.key], tgt)
            self.check(f"feature.{f.key}.iteration", f"{P}\\PI {PI_OF[E['feature_target'][f.key]]}", r["iteration"])
            team = next(t for t, a in TEAM_AREA.items() if a == f.area)
            self.check(f"feature.{f.key}.owner", E["feature_owner"][team], r["owner"])
            # lifecycle: Active when first child activates; Closed 1-2 working days after last child
            acts = [min(w.entered("Active")) for w in ch if w.entered("Active")]
            f_act = f.entered("Active")
            if f.key != "F14" and acts:
                self.check(f"feature.{f.key}.activated_with_first_child", min(acts).date(),
                           f_act[0].date() if f_act else None)
            if f.key in E["feature_closed_sprint"]:
                last = max(max(w.entered("Closed")) for w in ch)
                fc = f.entered("Closed")[0]
                gap = sum(1 for k in range(1, (fc.date() - last.date()).days + 1)
                          if (last.date() + dt.timedelta(days=k)).weekday() < 5)
                self.check(f"feature.{f.key}.closed", (E["feature_closed_sprint"][f.key], "1-2 working days"),
                           (self.sprint_day_of(fc)[0], gap), ok=self.sprint_day_of(fc)[0] ==
                           E["feature_closed_sprint"][f.key] and 1 <= gap <= 2)
        self.out["features"] = res
        f5 = [w for w in self.items if w.parent == "F5"]
        est = [w for w in f5 if w.pts()]
        self.check("f5.estimated", E["f5_estimated"], (len(est), sum(w.pts() for w in est)))
        self.check("f5.unestimated", E["f5_unestimated"], len(f5) - len(est))
        mvp = sum(w.pts() for w in f5 if w.title in E["f5_mvp_titles"])
        self.check("f5.mvp_pts", E["f5_mvp_pts"], mvp)
        self.check("f5.unscheduled", True, all(w.final["System.IterationPath"] == P and
                                               w.final["System.State"] == "New" for w in f5))
        # F10 target change, F2 at-risk, E6 creation and rank
        f10 = self.by_key["F10"]
        ch = [(t, o, n) for t, o, n in f10.changes("Microsoft.VSTS.Scheduling.TargetDate") if o is not None]
        x = E["f10_change"]
        if ch:
            t, o, n = ch[0]
            idx = f10.times.index(t)
            actual = dict(sprint_day=self.sprint_day_of(t), old=self.sprint_of_finish(ts(o).date()),
                          new=self.sprint_of_finish(ts(n).date()), comment=f10.revs[idx].get("comment"))
        else:
            actual = None
        self.check("f10.target_change", dict(sprint_day=(x["sprint"], x["day"]), old=x["old_target"],
                                             new=x["new_target"], comment=x["comment"]), actual)
        f2 = self.by_key["F2"]
        added = [t for t, o, n in f2.changes("System.Tags") if n and "at-risk" in n and (not o or "at-risk" not in o)]
        self.check("f2.at_risk_added_sprint", E["f2_at_risk_sprint"], self.sprint_day_of(added[0])[0] if added else None)

    def portfolio_queries(self):
        E, now = EXPECTED, self.now
        feats = [w for w in self.items if w.type == "Feature"]  # all Features, sandboxes included
        horizon = (now + dt.timedelta(days=21)).date()
        risk = []
        for f in feats:
            tgt = f.final.get("Microsoft.VSTS.Scheduling.TargetDate")
            c1 = tgt and ts(tgt).date() <= horizon and f.final["System.State"] != "Closed"
            if c1 or f.final.get("Microsoft.VSTS.Common.Risk") == "1 - High" or "at-risk" in f.tags():
                risk.append(f.key)
        order = lambda ks: sorted(ks, key=lambda k: (len(k), k))
        self.out["lab3_at_risk"] = order(risk)
        self.check("lab3.at_risk_query", E["lab3_at_risk"], order(risk))
        hp = [f.key for f in feats if f.final.get("Microsoft.VSTS.Common.Priority") == 1
              and f.final["System.State"] not in ("Closed", "Removed")]
        self.check("lab3.high_priority_incomplete", E["lab3_high_priority_incomplete"], order(hp))
        parents = set()
        for team in ("Mobile Banking", "Digital Accounts"):
            for w, _t in self.velocity(team, 13)["completed"]:
                if w.parent:
                    parents.add(w.parent)
        self.check("lab3.completed_last_sprint_digital", E["lab3_completed_last_sprint_digital"], order(parents))
        with_children = {w.parent for w in self.items if w.parent}
        self.check("features_without_children", E["features_without_children"],
                   order([f.key for f in feats if f.key not in with_children]))
        self.check("features_without_target", E["features_without_target"],
                   [f.key for f in feats if not f.final.get("Microsoft.VSTS.Scheduling.TargetDate")])
        e2 = [f for f in feats if f.parent == "E2"]
        c = Counter(f.final["System.State"] for f in e2)
        self.check("e2.features", E["e2_features"], dict(count=len(e2), Closed=c["Closed"], Active=c["Active"],
                                                         New=c["New"]))
        self.check("f9.child_areas", E["f9_child_areas"], len(self.out["features"]["F9"]["child_areas"]))
        epics = sorted([w for w in self.items if w.type == "Epic"],
                       key=lambda w: w.snaps[0]["Microsoft.VSTS.Common.StackRank"])
        self.check("epic_order", E["epic_order"], [e.key for e in epics])
        self.check("e6_created", E["e6_created"], self.sprint_day_of(self.by_key["E6"].created))
        self.check("epics_active", True, all(e.final["System.State"] == "Active" for e in epics))

    def people_and_hygiene(self):
        E = EXPECTED
        ethan = [w for w in self.items if w.final.get("System.AssignedTo") == "Ethan Brooks"
                 and w.final["System.State"] == "Active"]
        self.out["ethan_active"] = sorted(w.title for w in ethan)
        self.check("ethan_active", E["ethan_active"], len(ethan))
        kyle = [w for w in self.items if self.real(w) and w.final.get("System.AssignedTo") == "Kyle Morgan"]
        self.check("kyle_items", E["kyle_items"], dict(Counter(w.final["System.State"] for w in kyle)))
        ms = TEAM_AREA["Member Support"]
        zombies = [w for w in self.stories(ms) if w.final["System.State"] == "Active"
                   and w.final["System.IterationPath"] == self.iter_path(12)]
        self.check("ms.zombies", E["ms_zombies"], len(zombies))
        root_p1 = [b for b in self.bugs(area=P) if b.final["Microsoft.VSTS.Common.Priority"] == 1
                   and b.final["System.State"] != "Closed"]
        self.check("ms.root_p1_bugs", E["ms_root_p1_bugs"], len(root_p1))
        tile = [b for b in self.bugs(under=ms) if b.final["Microsoft.VSTS.Common.Priority"] == 1
                and b.final["System.State"] != "Closed"]
        self.check("ms.open_p1_tile", E["ms_open_p1_in_area"], len(tile))
        under = [w for w in self.items if w.area == ms and w.final["System.State"] != "Closed"]
        removed = sum(1 for w in under if w.final["System.State"] == "Removed")
        resolved = sum(1 for w in under if w.final["System.State"] == "Resolved")
        self.check("ms.removed", E["ms_removed"], removed)
        self.check("ms.resolved", E["ms_resolved"], resolved)
        self.check("ms.open_work_inflation", E["ms_open_work_inflation"], removed + resolved)
        f13 = [w for w in self.stories() if w.parent == "F13"]
        tags = Counter(t for w in f13 for t in w.tags() if t.startswith("omni"))
        self.check("ms.f13_tag_drift", E["f13_tags"], dict(tags))
        f14 = Counter(w.final["System.State"] for w in self.stories() if w.parent == "F14")
        self.check("ms.f14_child_states", E["f14_child_states"], dict(f14))
        f15 = [w for w in self.stories() if w.parent == "F15"]
        self.check("ms.f15_all_children_closed", (15, "Active"),
                   (sum(1 for w in f15 if w.final["System.State"] == "Closed"), self.by_key["F15"].final["System.State"]))
        self.out["ms"] = dict(zombies=[w.title for w in zombies], root_p1=[b.title for b in root_p1],
                              kyle=[w.title for w in kyle], removed=removed, resolved=resolved)

    def dependency_facts(self):
        E = EXPECTED
        res = {}

        def end(w):
            if w.type in ("Feature", "Epic"):
                t = w.final.get("Microsoft.VSTS.Scheduling.TargetDate")
                return ts(t).date() if t else None
            n = self.sprint_of_path(w.final["System.IterationPath"])
            return self.finish(n) if n else None

        for w in self.items:
            for ln in w.links:
                if ln["type"] != "Predecessor":
                    continue
                pred, succ = self.by_key[ln["target"]], w
                pe, se = end(pred), end(succ)
                if pe is None:
                    status = "hidden risk (predecessor unscheduled)"
                elif se < pe:
                    status = "conflict"
                elif se == pe:
                    status = "same sprint"
                else:
                    status = "ok"
                res[(pred.key, succ.key)] = status
        self.out["dependencies"] = {f"{a} -> {b}": s for (a, b), s in res.items()}
        self.check("dependencies", {f"{a} -> {b}": s for (a, b), s in E["dependencies"].items()},
                   self.out["dependencies"])

    def staleness_facts(self):
        E, today = EXPECTED, self.now.date()
        age = lambda w: (today - w.times[-1].date()).days
        res, bad = {}, []
        lo, hi = E["recent_touch_days"]
        for w in self.items:
            if w.type not in ("User Story", "Bug") or w.final["System.State"] != "Active":
                continue
            t = w.title.split(" - ", 1)[1] if w.area.startswith(P + "\\Training") and " - " in w.title else w.title
            a = age(w)
            if w.title in E["stale"]:
                mn, mx = E["stale"][w.title]
                res[w.title] = a
                self.check(f"stale.{w.title}", f"{mn}-{mx} days", a, ok=mn <= a <= mx)
            elif w.final.get("System.AssignedTo") == "Kyle Morgan":
                if a < E["kyle_min_age"]:
                    bad.append(f"{w.key} Kyle item changed {a} days ago")
            elif w.final["System.IterationPath"] == self.iter_path(12):
                lim = 20 if w.area.startswith(P + "\\Training") else E["zombie_min_age"]
                if a < lim:
                    bad.append(f"{w.key} zombie changed {a} days ago")
            elif not lo <= a <= hi:
                bad.append(f"{w.key} active item last changed {a} days ago ({t})")
        kyle_new = [w for w in self.items if w.final.get("System.AssignedTo") == "Kyle Morgan"]
        bad += [f"{w.key} Kyle item changed {age(w)} days ago" for w in kyle_new if age(w) < E["kyle_min_age"]]
        self.check("staleness.rules", [], bad, ok=not bad)
        for title, (mn, mx) in E["qa_wait"].items():
            w = next(x for x in self.items if x.title == title)
            r = w.entered("Resolved")
            a = (today - r[-1].date()).days if r else None
            res[f"QA wait: {title}"] = a
            self.check(f"qa_wait.{title}", f"{mn}-{mx} days", a, ok=a is not None and mn <= a <= mx
                       and w.final["System.State"] == "Resolved")
        self.out["staleness"] = res

    def lab9_facts(self):
        E = EXPECTED
        sand = [w for w in self.items if w.type == "Feature" and w.title.endswith("(planning copy)")]
        out = {}
        for f in sand:
            ch = sorted([w for w in self.items if w.parent == f.key],
                        key=lambda w: w.snaps[0]["Microsoft.VSTS.Common.StackRank"])
            pts = [w.pts() for w in ch]
            pid = f.title.split(" - ")[0]
            fc = {}
            for v in E["lab9_forecast"]:
                cap, cum, k = 3 * v, 0, 0
                for p in pts:
                    if cum + p > cap:
                        break
                    cum, k = cum + p, k + 1
                fc[v] = (k, cum)
            titles = [w.title.split(" - ", 1)[1] for w in ch]
            mvp_first = [i for i, t in enumerate(titles) if t in E["f5_mvp_titles"]]
            mvp_cum = sum(pts[i] for i in mvp_first)
            lands_at = min(v for v in (25, 20, 15, 10) if mvp_cum <= 3 * v) if mvp_cum <= 75 else None
            lands = [v for v in (25, 20, 15, 10, 5) if mvp_cum <= 3 * v]
            out[pid] = dict(forecast=fc, stories=len(ch), unestimated_at_bottom=all(p == 0 for p in pts[-4:]),
                            mvp_reordered_pts=mvp_cum, mvp_lands_at_min_velocity=min(lands) if lands else None)
            self.check(f"lab9.{pid}.forecast", E["lab9_forecast"], fc)
            self.check(f"lab9.{pid}.mvp_reordered", (E["f5_mvp_pts"], True),
                       (mvp_cum, mvp_cum <= 3 * E["lab9_mvp_reordered_lands_at"]))
            self.check(f"lab9.{pid}.unestimated_at_bottom", True, out[pid]["unestimated_at_bottom"])
        # Real Digital Accounts backlog order: committed F6/F7 New work above F5, F5 in Bible order.
        da = [w for w in self.stories(TEAM_AREA["Digital Accounts"]) if w.final["System.State"] not in ("Closed", "Removed")]
        da.sort(key=lambda w: w.snaps[0]["Microsoft.VSTS.Common.StackRank"])
        f5_pos = [i for i, w in enumerate(da) if w.parent == "F5"]
        f5_titles = [da[i].title for i in f5_pos]
        new_f67 = [i for i, w in enumerate(da) if w.parent in ("F6", "F7") and w.final["System.State"] == "New"]
        self.out["da_backlog_top"] = [w.title for w in da[:20]]
        self.check("da.backlog_order", True, bool(f5_pos) and max(new_f67) < min(f5_pos)
                   and f5_titles[0] == "Card lock and unlock service and API" and f5_pos == list(range(f5_pos[0], f5_pos[0] + 20)),
                   note="in-progress S14 items, then F6/F7 New work (20 pts), then F5 in order")
        self.check("da.committed_new_f6_f7_pts", 20, sum(da[i].pts() for i in new_f67))
        self.out["lab9"] = out

    def sandbox_facts(self):
        E = EXPECTED
        feats = [w for w in self.items if w.type == "Feature" and w.title.endswith("(sandbox)")]
        res = {}
        for f in feats:
            pid = f.title.split(" - ")[0]
            area = f"{P}\\Training\\{pid}"
            ch = [w for w in self.items if w.parent == f.key]
            got = {}
            for w in ch:
                n = int(w.key.rsplit("-", 1)[1])
                tag = next((t for t in w.tags() if t.startswith("omni")), None)
                sp = self.sprint_of_path(w.final["System.IterationPath"])
                pts = w.final.get("Microsoft.VSTS.Scheduling.StoryPoints")
                ar = "P" if w.area == area else ("Training" if w.area == f"{P}\\Training" else w.area)
                got[n] = (w.type, w.final["System.State"], sp, pts, tag, ar)
            ok_titles = all(w.title.startswith(f"{pid} - ") for w in ch + [f])
            res[pid] = dict(items=len(ch), feature_state=f.final["System.State"])
            self.check(f"sandbox.{pid}.lab11_items", E["sandbox_l11"], got)
            self.check(f"sandbox.{pid}.titles_prefixed", True, ok_titles)
            self.check(f"sandbox.{pid}.feature_new", "New", f.final["System.State"])
            kyle = [w for w in ch if w.final.get("System.AssignedTo") == "Kyle Morgan"]
            self.check(f"sandbox.{pid}.kyle_stale", True,
                       len(kyle) == 2 and all((self.now.date() - w.times[-1].date()).days >= 25 for w in kyle))
        self.out["sandboxes"] = res

    def team_facts(self):
        E = EXPECTED
        teams = {t["name"]: t for t in self.data["teams"]}
        d = teams.get("HarborPoint Team", {})
        self.check("team.default_areas", E["default_team_areas"],
                   [(a["path"], a["include_children"]) for a in d.get("areas", [])])
        self.check("team.default_is_default", True, d.get("is_default"))
        real = [t for t in self.data["teams"] if not t.get("participant")]
        sb = [t for t in self.data["teams"] if t.get("participant")]
        self.check("team.real_iterations", True, all(len(t["iterations"]) == 12 and t["iterations"][0].endswith("Sprint 9")
                                                     for t in real))
        self.check("team.sandbox_iterations", True, all([i.rsplit(" ", 1)[1] for i in t["iterations"]] ==
                                                        [str(n) for n in range(15, 21)] for t in sb))
        self.check("team.bugs_with_requirements", True, all(t["bugs_behavior"] == "asRequirements"
                                                            for t in self.data["teams"]))
        self.out["teams"] = [t["name"] for t in self.data["teams"]]

    # ======================================================================= reporting
    @property
    def failures(self):
        return [c for c in self.checks if not c["ok"]]

    def to_json(self) -> dict:
        def norm(o):
            if isinstance(o, dict):
                return {("orphan" if k is None else str(k)): norm(v) for k, v in o.items()}
            if isinstance(o, (list, tuple)):
                return [norm(x) for x in o]
            if isinstance(o, (dt.date, dt.datetime)):
                return o.isoformat()
            return o

        return norm(dict(now=self.data["now"], sprint14_start=self.data["calendar"]["sprint14_start"],
                         passed=not self.failures, checks_total=len(self.checks), failures=self.failures,
                         facts=self.out, checks=self.checks))

    def to_markdown(self) -> str:
        o, L = self.out, []
        fmt = lambda x: "-" if x is None else (f"{x[0]}/{x[1]}" if isinstance(x, tuple) else str(x))
        L.append("# HarborPoint dataset facts\n")
        L.append(f"- now: `{self.data['now']}` - Sprint 14 starts `{self.data['calendar']['sprint14_start']}`")
        L.append(f"- work items: {o['counts']['work_items']} ({o['counts']['by_type']}), revisions: {o['counts']['revisions']}")
        L.append(f"- checks: {len(self.checks)}, failures: **{len(self.failures)}**\n")
        if self.failures:
            L.append("## FAILURES\n")
            for c in self.failures:
                L.append(f"- `{c['id']}` expected `{c['expected']}` got `{c['actual']}` {c['note']}")
            L.append("")
        L.append("## Velocity (Analytics semantics: Planned at end of day 1, Completed = Closed in sprint)\n")
        L.append("| Team | Sprint | Planned | Completed | n | Carry n/pts | Left Resolved | Avg cycle (d) | Resolved dwell (d) |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for team in TEAMS:
            for n in HIST:
                v, c = o["velocity"][team][n], o["cycle"][team][n]
                L.append(f"| {team} | {n} | {v['planned']} | {v['done']} | {v['n']} | {fmt(v['carry'])} | "
                         f"{fmt(v['resolved_left'])} | {c['avg']} | {c['resolved_dwell'] if c['resolved_dwell'] is not None else '-'} |")
        L.append("\n## Closed mix by Feature (n/pts; Member Support includes stories left Resolved)\n")
        L.append("| Team | Sprint | Mix |")
        L.append("|---|---|---|")
        for team in TEAMS:
            for n in HIST:
                m = o["mix"][team][n]
                L.append(f"| {team} | {n} | " + ", ".join(f"{k or 'orphan'} {fmt(v)}" for k, v in
                                                      sorted(m.items(), key=lambda kv: (kv[0] is None, str(kv[0])))) + " |")
        L.append("\n## Mobile Banking signals\n")
        L.append(f"- Orphan share of completed points: {o['mobile_orphan_pct']}")
        L.append(f"- Commitment reliability: {o['mobile_reliability_pct']}")
        L.append(f"- Open bugs now: {o['mobile_open_bugs']}")
        L.append(f"- Ethan Brooks active items ({len(o['ethan_active'])}): {', '.join(o['ethan_active'])}")
        L.append(f"\n## Digital Accounts\n\n- {o['da']}")
        L.append("\n## Bugs per sprint (opened, closed, open at end; S14 = now)\n")
        L.append("| Team | Start | S9 | S10 | S11 | S12 | S13 | S14 | Source |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for team in TEAMS:
            b = o["bugs"][team]
            src = "World Bible" if team in EXPECTED["bugs"] else "generated (not in World Bible)"
            L.append(f"| {team} | {b['start']} | " + " | ".join("+{}/-{} = {}".format(*b['flow'][n]) for n in range(9, 15))
                     + f" | {src} |")
        L.append("\n## Sprint 14 snapshot (now)\n")
        L.append("| Team | Planned day 1 | Added later | Total n/pts | Closed | Resolved | Active | New | Done so far |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for team in TEAMS:
            s = o["s14"][team]
            L.append(f"| {team} | {s['planned']} | {s['added']} | {fmt(s['total'])} | {fmt(s['Closed'])} | "
                     f"{fmt(s['Resolved'])} | {fmt(s['Active'])} | {fmt(s['New'])} | {fmt(s['done_so_far'])} |")
        L.append(f"\n- Security compliance (F21+F22): {o['security_compliance']}")
        L.append("\n## Features (rollup by Story Points, Closed only)\n")
        L.append("| Key | Feature | State | Target | Children | Pts | Done | % | Tags |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for k in sorted(o["features"], key=lambda k: int(k[1:])):
            f = o["features"][k]
            L.append(f"| {k} | {f['title']} | {f['state']} | S{f['target']} | {f['children']} | {f['pts']} | {f['done']} | "
                     f"{fmt(f['pct'])} | {', '.join(f['tags'])} |")
        L.append(f"\n## Queries and portfolio\n\n- Lab 3 at-risk query: {', '.join(o['lab3_at_risk'])}")
        L.append("\n## Dependencies\n")
        for k, v in o["dependencies"].items():
            L.append(f"- {k}: **{v}**")
        L.append(f"\n## Member Support hygiene\n\n- {o['ms']}")
        L.append(f"\n## Staleness (days since last change / since Resolved)\n\n- {o['staleness']}")
        L.append(f"\n## Lab 9 forecast (sandbox planning copies)\n\n- {o['lab9']}")
        L.append(f"- Digital Accounts backlog (top 20 open): {o['da_backlog_top']}")
        L.append(f"\n## Sandboxes\n\n- {o['sandboxes']}")
        L.append("\n## All checks\n")
        L.append("| Check | Result |")
        L.append("|---|---|")
        for c in self.checks:
            L.append(f"| `{c['id']}` | {'PASS' if c['ok'] else '**FAIL**'} |")
        return "\n".join(L) + "\n"


def compute(data: dict) -> Facts:
    return Facts(data).run()

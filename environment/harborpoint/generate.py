"""Generate the HarborPoint seed dataset (schema harborpoint-dataset/1).

Usage (from the environment/ directory):
    python -m harborpoint.generate [--now ISO] [--sprint14-start YYYY-MM-DD] [--participants N]
                                   [--out out/dataset.json] [--artifacts content/artifacts.yaml]

Defaults: now = current UTC minus 5 minutes; sprint14_start = the Monday of the week BEFORE now's week,
so "now" falls in Sprint 14 week 2. Sprint n starts sprint14_start + 14*(n-14) days.

The output is fully deterministic for the same (now, sprint14_start, participants, artifacts) inputs:
every random choice uses a purpose-specific random.Random seeded from scenario.SEED.

Rules implemented (World Bible section 12 and the dataset contract):
- Stories are created 1-3 sprints before their first sprint in the backlog (iteration = project root)
  and moved into the sprint on its day 1 (or the Friday before). Carry-overs move on day 1 of the next
  sprint. Velocity "Planned" = points in the sprint at end of day 1; "Completed" = closed in the sprint
  while assigned to it.
- Activated days 1-6, Closed days 2-10; Mobile Banking always passes through Resolved, with cycle and
  Resolved dwell times rising per section 6.1. Other teams: steady 3-6 day cycle times, ~30% use Resolved.
- Because the provisioner uses bypassRules, every state change sets System.Reason, StateChangeDate and the
  matching ActivatedDate / ResolvedDate / ClosedDate explicitly (By fields are omitted).
- All events happen 16:00-19:00 UTC on working days and strictly before "now". Active items get a
  recent touch 1-3 calendar days before now, except the planted stale items.
"""
from __future__ import annotations

import argparse
import datetime as dt
import itertools
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

from . import scenario as sc

UTC = dt.timezone.utc
SCHEMA = "harborpoint-dataset/1"
P = sc.PROJECT_NAME
AT = "@at"  # placeholder: replaced by the revision's timestamp when times are assigned
WD_OFF = [0, 1, 2, 3, 4, 7, 8, 9, 10, 11]  # calendar offset of sprint day 1..10 from the sprint's Monday
ACT_OFFS = WD_OFF[:6]   # activation on days 1-6
CLOSE_OFFS = WD_OFF[1:]  # closure on days 2-10
FIB = (1, 2, 3, 5, 8, 13)
EXT = (1, 2, 3, 4, 5, 6, 8, 13)
TEAM_PREFIX = {"Mobile Banking": "MOB", "Digital Accounts": "DAC", "Security": "SEC", "Core Platform": "CPL",
               "Branch Experience": "BRX", "Member Support": "MSU"}

F_STATE = "System.State"
F_REASON = "System.Reason"
F_ITER = "System.IterationPath"
F_AREA = "System.AreaPath"
F_TAGS = "System.Tags"
F_ASSIGNED = "System.AssignedTo"
F_TITLE = "System.Title"
F_POINTS = "Microsoft.VSTS.Scheduling.StoryPoints"
F_ACTIVATED = "Microsoft.VSTS.Common.ActivatedDate"
F_RESOLVED = "Microsoft.VSTS.Common.ResolvedDate"
F_CLOSED = "Microsoft.VSTS.Common.ClosedDate"
F_STATECHANGE = "Microsoft.VSTS.Common.StateChangeDate"
F_STACKRANK = "Microsoft.VSTS.Common.StackRank"
F_PRIORITY = "Microsoft.VSTS.Common.Priority"
F_SEVERITY = "Microsoft.VSTS.Common.Severity"
F_START = "Microsoft.VSTS.Scheduling.StartDate"
F_TARGET = "Microsoft.VSTS.Scheduling.TargetDate"

REASONS = {
    "default": {"New": "New", "Active": "Implementation started", "Resolved": "Code complete and unit tests pass",
                "Closed": "Acceptance tests pass", "Removed": "Removed from the backlog"},
    "Bug": {"New": "New", "Active": "Approved", "Resolved": "Fixed", "Closed": "Verified"},
}


# ============================================================================ calendar
class Calendar:
    """Sprint calendar relative to the Sprint 14 Monday."""

    def __init__(self, sprint14_start: dt.date):
        if sprint14_start.weekday() != 0:
            raise ValueError(f"sprint14_start {sprint14_start} is not a Monday")
        self.s14 = sprint14_start

    def start(self, n: int) -> dt.date:
        return self.s14 + dt.timedelta(days=14 * (n - 14))

    def finish(self, n: int) -> dt.date:
        return self.start(n) + dt.timedelta(days=11)

    def day(self, n: int, d: int) -> dt.date:
        return self.start(n) + dt.timedelta(days=WD_OFF[d - 1])

    def off(self, n: int, o: int) -> dt.date:
        return self.start(n) + dt.timedelta(days=o)

    def friday_before(self, n: int) -> dt.date:
        return self.start(n) - dt.timedelta(days=3)

    @staticmethod
    def is_wd(d: dt.date) -> bool:
        return d.weekday() < 5

    def wdays(self, a: dt.date, b: dt.date) -> list[dt.date]:
        out, d = [], a
        while d <= b:
            if self.is_wd(d):
                out.append(d)
            d += dt.timedelta(days=1)
        return out

    def add_wd(self, d: dt.date, k: int) -> dt.date:
        step = 1 if k >= 0 else -1
        while k != 0:
            d += dt.timedelta(days=step)
            if self.is_wd(d):
                k -= step
        return d

    @staticmethod
    def latest_wd(d: dt.date) -> dt.date:
        while d.weekday() >= 5:
            d -= dt.timedelta(days=1)
        return d

    @staticmethod
    def nearest_wd(d: dt.date) -> dt.date:
        if d.weekday() == 5:
            return d - dt.timedelta(days=1)
        if d.weekday() == 6:
            return d + dt.timedelta(days=1)
        return d

    def sprint_days(self, n: int, last_day: int = 10) -> list[dt.date]:
        return [self.day(n, d) for d in range(1, last_day + 1)]


def iso(t: dt.datetime) -> str:
    return t.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_now(s: str) -> dt.datetime:
    s = s.strip().replace("Z", "+00:00")
    t = dt.datetime.fromisoformat(s)
    if t.tzinfo is None:
        t = t.replace(tzinfo=UTC)
    return t.astimezone(UTC).replace(microsecond=0)


def default_sprint14_start(now: dt.datetime) -> dt.date:
    d = now.date()
    return d - dt.timedelta(days=d.weekday()) - dt.timedelta(days=7)


def date_field(d: dt.date) -> str:
    """Date-only fields (Start/Target) at 16:00 UTC so the calendar day is the same in US and EU zones."""
    return f"{d.isoformat()}T16:00:00Z"


def full_area(rel: str) -> str:
    return P if not rel else f"{P}\\{rel}"


def full_iter(sprint: int | None) -> str:
    return P if sprint is None else f"{P}\\{sc.iteration_rel(sprint)}"


def full_pi(pi: int) -> str:
    return f"{P}\\PI {pi}"


def tag_str(tags) -> str:
    return "; ".join(tags)


# ============================================================================ helpers
def split_points(n: int, total: int, rng: random.Random) -> list[int]:
    """n story-point values summing to total, preferring Fibonacci values close to the average."""
    if n == 0:
        if total != 0:
            raise ValueError(f"cannot split {total} points over 0 stories")
        return []
    for allowed in (FIB, EXT):
        combos = [c for c in itertools.combinations_with_replacement(allowed, n) if sum(c) == total]
        if combos:
            avg = total / n
            combos.sort(key=lambda c: (sum((v - avg) ** 2 for v in c), c))
            pick = list(rng.choice(combos[: min(4, len(combos))]))
            rng.shuffle(pick)
            return pick
    raise ValueError(f"cannot split {total} points over {n} stories")


def solve_cycle(slots: list[dict], target: float, rng: random.Random) -> list[tuple[int, int]]:
    """Choose (activation offset, close offset) per slot so the mean cycle time (days) hits target.

    slot: {"a": fixed activation offset or None, "max_c": latest close offset}.
    """
    cands = []
    for sl in slots:
        a_opts = [sl["a"]] if sl.get("a") is not None else ACT_OFFS
        c_opts = [c for c in CLOSE_OFFS if c <= sl.get("max_c", 11)]
        cands.append([(a, c) for a in a_opts for c in c_opts if c > a])
    goal = round(target * len(slots))
    choice = []
    for cs in cands:
        want = target + rng.gauss(0, 1.5)
        best = min(abs((c - a) - want) for a, c in cs)
        choice.append(rng.choice([x for x in cs if abs((x[1] - x[0]) - want) == best]))
    for _ in range(20000):
        total = sum(c - a for a, c in choice)
        diff = goal - total
        if diff == 0:
            break
        i = rng.randrange(len(choice))
        cur = choice[i][1] - choice[i][0]
        better = [x for x in cands[i] if abs(diff - ((x[1] - x[0]) - cur)) < abs(diff)]
        if better:
            choice[i] = rng.choice(better)
    return choice


# ============================================================================ work item model
class Item:
    def __init__(self, key: str, wit: str, parent: str | None = None):
        self.key, self.type, self.parent = key, wit, parent
        self.events: list[dict] = []
        self.links: list[dict] = []
        self.state = None
        self.activated = False
        self.created: dt.date | None = None
        self.meta: dict = {}

    # --- event recording (dates only; times are assigned later)
    def ev(self, date: dt.date, fields: dict | None = None, comment: str | None = None, after=None, sort=0):
        self.events.append(dict(date=date, fields=dict(fields or {}), comment=comment, after=after, sort=sort))
        return self.events[-1]

    def create(self, date: dt.date, fields: dict, comment: str | None = None):
        assert not self.events, self.key
        self.created = date
        f = {F_STATE: "New", F_REASON: "New"}
        f.update(fields)
        self.state = "New"
        return self.ev(date, f, comment)

    def transition(self, date: dt.date, state: str, extra: dict | None = None, comment=None, after=None, sort=0):
        reasons = REASONS["Bug"] if self.type == "Bug" else REASONS["default"]
        f = {F_STATE: state, F_REASON: reasons[state], F_STATECHANGE: AT}
        if state == "Active" and not self.activated:
            f[F_ACTIVATED] = AT
            self.activated = True
        elif state == "Resolved":
            f[F_RESOLVED] = AT
        elif state == "Closed":
            f[F_CLOSED] = AT
        if extra:
            f.update(extra)
        self.state = state
        return self.ev(date, f, comment, after=after, sort=sort)

    def last_date(self) -> dt.date:
        return max(e["date"] for e in self.events)


# ============================================================================ generator
class Generator:
    def __init__(self, now: dt.datetime, sprint14_start: dt.date, participants: int, artifacts: dict):
        self.now = now
        self.cal = Calendar(sprint14_start)
        self.participants = participants
        self.artifacts = artifacts
        off = (now.date() - sprint14_start).days
        if not 7 <= off <= 13:
            raise ValueError(f"now ({iso(now)}) must fall in Sprint 14 week 2 "
                             f"({self.cal.day(14, 6)} .. {sprint14_start + dt.timedelta(days=13)})")
        if not 0 <= participants <= sc.MAX_PARTICIPANTS:
            raise ValueError(f"--participants must be 0..{sc.MAX_PARTICIPANTS}")
        self.items: dict[str, Item] = {}
        self.order: list[str] = []
        self.rank_order: list[str] = []
        self.feature_spec = {f["key"]: f for f in sc.FEATURES}
        self.feature_created: dict[str, dt.date] = {}

    # --- utilities
    @staticmethod
    def rng(*parts) -> random.Random:
        return random.Random("|".join([sc.SEED, *map(str, parts)]))

    def new_item(self, key: str, wit: str, parent: str | None = None) -> Item:
        if key in self.items:
            raise ValueError(f"duplicate key {key}")
        it = Item(key, wit, parent)
        self.items[key] = it
        self.order.append(key)
        return it

    def creation_date(self, rng, first_sprint: int | None, parent: str | None, latest: dt.date | None = None):
        """Random working day 1-3 sprints before first_sprint, after the parent's creation, before now."""
        cal = self.cal
        lo = cal.start(first_sprint - 3) if first_sprint else cal.start(13)
        hi = latest or (cal.start(first_sprint) - dt.timedelta(days=4) if first_sprint else cal.day(14, 5))
        hi = min(hi, cal.day(14, 5))
        if parent and parent in self.items and self.items[parent].created:
            lo = max(lo, cal.add_wd(self.items[parent].created, 1))
        if lo > hi:  # far-future items: created in recent backlog refinement
            lo = max(cal.start(13), cal.add_wd(self.items[parent].created, 1) if parent in self.items else cal.start(13))
            hi = cal.day(14, 5)
        days = cal.wdays(lo, hi)
        if not days:
            raise ValueError(f"no creation day for parent={parent} first={first_sprint}")
        return rng.choice(days)

    def story_fields(self, title, team_area_rel, pts, tags=(), assigned=None, iteration=None, priority=2):
        f = {F_TITLE: title, F_AREA: full_area(team_area_rel), F_ITER: iteration or P, F_PRIORITY: priority,
             "Microsoft.VSTS.Common.ValueArea": "Architectural" if "tech-debt" in tags else "Business"}
        if pts is not None:
            f[F_POINTS] = pts
        if tags:
            f[F_TAGS] = tag_str(tags)
        if assigned:
            f[F_ASSIGNED] = assigned
        return f

    # ------------------------------------------------------------------ portfolio skeleton
    def build_portfolio(self):
        cal = self.cal
        for e in sc.EPICS:
            it = self.new_item(e["key"], "Epic")
            created = cal.day(*sc.E6_CREATED) if e["key"] == "E6" else cal.day(5, 1)
            f = {F_TITLE: e["title"], F_AREA: full_area(e["area"]), F_ITER: P, F_ASSIGNED: e["owner"],
                 F_PRIORITY: e["priority"], F_START: date_field(cal.start(e["start"])),
                 F_TARGET: date_field(cal.finish(e["target"])), "Microsoft.VSTS.Common.ValueArea": e["value_area"],
                 "System.Description": f"<p>{e['description']}</p>"}
            if e["tags"]:
                f[F_TAGS] = tag_str(e["tags"])
            it.create(created, f)
            act = cal.day(12, 3) if e["key"] == "E6" else cal.day(9, 1)
            it.transition(act, "Active", comment="Initiative approved by the Executive Committee." if e["key"] != "E6"
                          else "Added for the regulatory examination (mandatory).")
            self.rank_order.append(e["key"])
        special_created = {"F16": (10, 2), "F21": (11, 6), "F22": (12, 4)}
        prio = {k: p for p, ks in sc.FEATURE_PRIORITY.items() for k in ks}
        for f in sc.FEATURES:
            it = self.new_item(f["key"], "Feature", f["epic"])
            s, d = special_created.get(f["key"], (max(5, f["start"] - 4), 2))
            created = cal.day(s, d)
            self.feature_created[f["key"]] = created
            orig_target = f.get("original_target", f["target"])
            late_tags = [t for t in f["tags"] if t in sc.TAG_EVENTS
                         and created < cal.day(*sc.TAG_EVENTS[t])]
            tags0 = [t for t in f["tags"] if t not in late_tags]
            fields = {F_TITLE: f["title"], F_AREA: full_area(sc.TEAM_AREA[f["team"]]),
                      F_ITER: full_pi(sc.pi_of(orig_target)), F_ASSIGNED: sc.PRODUCT_OWNER[f["team"]],
                      F_PRIORITY: prio[f["key"]], F_START: date_field(cal.start(f["start"])),
                      F_TARGET: date_field(cal.finish(orig_target)),
                      "Microsoft.VSTS.Common.BusinessValue": f["bv"], "Microsoft.VSTS.Common.TimeCriticality": f["tc"],
                      "Microsoft.VSTS.Common.Risk": sc.RISK_LABEL[f["risk"]],
                      "Microsoft.VSTS.Common.ValueArea": f.get("value_area", "Business"),
                      "System.Description": f"<p>{f['description']}</p>"}
            if f["effort"] is not None:
                fields["Microsoft.VSTS.Scheduling.Effort"] = f["effort"]
            if tags0:
                fields[F_TAGS] = tag_str(tags0)
            it.create(created, fields)
            it.meta["tags"] = list(tags0)
            it.meta["late_tags"] = late_tags
        # Feature rank: by Epic rank, then table order (E6's Features therefore last).
        epic_rank = [e["key"] for e in sc.EPICS]
        for ek in epic_rank:
            self.rank_order += [f["key"] for f in sc.FEATURES if f["epic"] == ek]

    # ------------------------------------------------------------------ history (sections 6.1-6.6)
    def build_history(self, team: str):
        cal, spec = self.cal, sc.HISTORY[team]
        rng = self.rng("hist", team)
        area = sc.TEAM_AREA[team]
        pools = {g: list(t) for (tm, g), t in sc.HISTORY_TITLES.items() if tm == team}
        plans, pending = [], defaultdict(list)
        for s in sc.HISTORY_SPRINTS:
            for g, (n, p) in spec["mix"][s].items():
                cin = [x for x in pending[s] if x["group"] == g]
                ov = sc.HISTORY_OVERRIDES.get((team, s, g), {})
                for x in cin:
                    x["final"], x["outcome"] = s, ov.get("carry_in_outcome", "Closed")
                n_new, p_new = n - len(cin), p - sum(x["pts"] for x in cin)
                if "new" in ov:
                    specs = ov["new"]
                    assert len(specs) == n_new and sum(x.get("true_pts") or x["pts"] for x in specs) == p_new, \
                        (team, s, g)
                else:
                    specs = [dict(pts=v, outcome="Closed") for v in split_points(n_new, p_new, rng)]
                for x in specs:
                    plans.append(dict(group=g, first=s, final=s, pts=x["pts"], outcome=x["outcome"],
                                      title=x.get("title") or pools[g].pop(0), tags=x.get("tags", [])))
            for fs, g, n, p in spec["carries"]:
                if fs == s:
                    for v in split_points(n, p, rng):
                        x = dict(group=g, first=s, final=None, pts=v, outcome=None, title=pools[g].pop(0), tags=[])
                        plans.append(x)
                        pending[s + 1].append(x)
        leftovers = {g: t for g, t in pools.items() if t}
        assert not leftovers, f"unused titles for {team}: {leftovers}"
        assert all(x["final"] for x in plans), team

        # Lifecycle per sprint: activation/close offsets solved to hit the cycle-time profile.
        closing = {f["closed_sprint"]: f["key"] for f in sc.FEATURES
                   if f.get("closed_sprint") and f["team"] == team}
        for s in sc.HISTORY_SPRINTS:
            done = [x for x in plans if x["final"] == s]
            slots = []
            for x in done:
                sl = {"max_c": 10 if closing.get(s) == x["group"] else 11}
                if x["first"] < s and spec.get("carried_started"):
                    x["a_prev"] = rng.choice([3, 4, 7])  # started late (days 4-6) in the previous sprint
                    sl["a"] = x["a_prev"] - 14
                slots.append(sl)
            for x, (a, c) in zip(done, solve_cycle(slots, spec["cycle"][s], rng)):
                x["a"], x["c"] = a, c
                use_resolved = spec.get("always_resolved") or x["outcome"] == "Resolved" or rng.random() < 0.3
                x["r"] = None
                if use_resolved:
                    if spec.get("always_resolved"):
                        want = c - max(0.0, spec["resolved_dwell"][s] + rng.gauss(0, 0.6))
                    else:
                        want = c - rng.choice([0, 1])
                    opts = [o for o in range(max(a, 0), c + 1) if cal.is_wd(cal.off(s, o))]
                    x["r"] = min(opts, key=lambda o: (abs(o - want), -o))
                if x["outcome"] == "Resolved":
                    x["r"] = c

        eng = sc.ENGINEERS[team]
        for i, x in enumerate(plans, 1):
            key = f"US-{TEAM_PREFIX[team]}-{i:03d}"
            it = self.new_item(key, "User Story", x["group"])
            created = self.creation_date(rng, x["first"], x["group"])
            it.create(created, self.story_fields(x["title"], area, x["pts"], x["tags"]))
            move1 = cal.day(x["first"], 1) if rng.random() < 0.8 or created >= cal.friday_before(x["first"]) \
                else cal.friday_before(x["first"])
            it.ev(move1, {F_ITER: full_iter(x["first"])})
            who = rng.choice(eng)
            s = x["final"]
            if x["first"] < s:
                if "a_prev" in x:
                    it.transition(cal.off(x["first"], x["a_prev"]), "Active", {F_ASSIGNED: who})
                it.ev(cal.day(s, 1), {F_ITER: full_iter(s)}, comment="Carried over from the previous sprint.")
            if not it.activated:
                it.transition(cal.off(s, x["a"]), "Active", {F_ASSIGNED: who})
            if x["r"] is not None:
                it.transition(cal.off(s, x["r"]), "Resolved")
            if x["outcome"] == "Closed":
                it.transition(cal.off(s, x["c"]), "Closed")
            it.meta.update(team=team, history=True)

    # ------------------------------------------------------------------ Sprint 14 explicit items
    def build_sprint14(self, team: str):
        cal, now = self.cal, self.now
        rng = self.rng("s14", team)
        area = sc.TEAM_AREA[team]
        for i, x in enumerate(sc.S14_ITEMS[team], 1):
            key = x.get("key") or (f"MB14-{x['n']:02d}" if team == "Mobile Banking"
                                   else f"{TEAM_PREFIX[team]}14-{i:02d}")
            it = self.new_item(key, "User Story", x["parent"])
            it.meta.update(team=team, s14=True, spec=x)
            carried = tuple(x.get("carried", ()))
            tags = list(x.get("tags", []))
            assigned_new = x["assigned"] if x["state"] == "New" else None
            stale = x.get("stale_days")
            stale_date = cal.latest_wd(now.date() - dt.timedelta(days=stale)) if stale else None
            if x.get("added_day") or x.get("created_day"):
                d = cal.day(14, x.get("added_day") or x.get("created_day"))
                it.create(d, self.story_fields(x["title"], area, x["pts"], tags, assigned_new, full_iter(14)))
            else:
                first = carried[0] if carried else 14
                created = self.creation_date(rng, first, x["parent"])
                it.create(created, self.story_fields(x["title"], area, x["pts"], tags, assigned_new))
                for j, s in enumerate(carried + (14,)):
                    if s == 14:
                        move = cal.day(14, 1)
                        if stale_date and stale_date < move:
                            move = stale_date  # the Friday before Sprint 14
                        elif not carried and rng.random() < 0.2:
                            move = cal.friday_before(14)
                        it.ev(move, {F_ITER: full_iter(14)},
                              comment="Carried over from the previous sprint." if carried else None)
                    else:
                        it.ev(cal.day(s, 1), {F_ITER: full_iter(s)},
                              comment="Carried over from the previous sprint." if j > 0 else None)
                        if j == 0 and x["state"] != "New":
                            act_day = 5 if s == 12 else rng.choice([3, 4, 5, 6])
                            it.transition(cal.day(s, act_day), "Active", {F_ASSIGNED: x["assigned"]})
            # Sprint 14 progression (explicit day-of-sprint events on days 1-5)
            st = x["state"]
            act = None
            if st in ("Active", "Resolved", "Closed") and not it.activated:
                if x.get("added_day"):
                    act = cal.day(14, x["added_day"])
                else:
                    act = cal.day(14, rng.choice([1, 2]) if (st == "Closed" or x.get("comment")) else rng.choice([1, 2, 3]))
                it.transition(act, "Active", {F_ASSIGNED: x["assigned"]})
            if x.get("comment"):
                cday, text, ctags = x["comment"]
                tags = tags + list(ctags)
                it.ev(cal.day(14, cday), {F_TAGS: tag_str(tags)}, comment=text)
            if st == "Resolved":
                if x.get("resolved_days_ago"):
                    rd = cal.nearest_wd(now.date() - dt.timedelta(days=x["resolved_days_ago"]))
                else:
                    rd = cal.day(14, rng.choice([3, 4]))
                it.transition(rd, "Resolved")
            if st == "Closed":
                a_date = act or cal.day(14, 1)
                close_opts = [d for d in cal.sprint_days(14, 5) if d > a_date]
                cd = rng.choice(close_opts)
                if team == "Mobile Banking":
                    res_opts = [d for d in cal.sprint_days(14, 5) if a_date <= d <= cd]
                    it.transition(rng.choice(res_opts), "Resolved")
                it.transition(cd, "Closed")
            if stale_date and stale_date > it.last_date():
                it.ev(stale_date, {}, comment=sc.STALE_COMMENTS.get(x["title"], "Still in progress."))
            if stale:
                it.meta["stale_days"] = stale
            self.s14_keys.setdefault(team, []).append(key)

    # ------------------------------------------------------------------ future / backlog / planted stories
    def build_future(self):
        cal = self.cal
        counters = defaultdict(int)
        for team, parent, title, pts, sprint, key in sc.FUTURE_ITEMS:
            rng = self.rng("future", title)
            counters[team] += 1
            key = key or f"US-{TEAM_PREFIX[team]}-F{counters[team]:02d}"
            it = self.new_item(key, "User Story", parent)
            created = self.creation_date(rng, sprint if sprint else None, parent)
            it.create(created, self.story_fields(title, sc.TEAM_AREA[team], pts, (), None,
                                                 full_iter(sprint) if sprint else None))
            it.meta.update(team=team, future=True, sprint=sprint)
        # F5: 20 stories, all New, unscheduled, created during backlog refinement in Sprint 13
        days = cal.wdays(cal.day(13, 2), cal.day(13, 8))
        for i, (title, pts, _mvp) in enumerate(sc.F5_STORIES, 1):
            it = self.new_item(f"F5-{i:02d}", "User Story", "F5")
            it.create(days[(i - 1) * len(days) // len(sc.F5_STORIES)],
                      self.story_fields(title, sc.TEAM_AREA["Digital Accounts"], pts))
            it.meta.update(team="Digital Accounts", f5=i)

    def build_member_support_planted(self):
        cal = self.cal
        area = sc.TEAM_AREA["Member Support"]
        for i, z in enumerate(sc.MS_ZOMBIES, 1):
            it = self.new_item(f"US-MSU-Z{i}", "User Story", z["parent"])
            d = cal.day(12, z["day"])
            it.create(d, self.story_fields(z["title"], area, z["pts"], z["tags"], None, full_iter(12)),
                      comment="Added mid-sprint.")
            it.transition(cal.add_wd(d, 1), "Active", {F_ASSIGNED: z["assigned"]})
            it.meta.update(team="Member Support", zombie=True)
        for i, k in enumerate(sc.MS_KYLE_BACKLOG, 1):
            it = self.new_item(f"US-MSU-K{i}", "User Story", k["parent"])
            it.create(cal.day(11, 3 + 2 * i), self.story_fields(k["title"], area, k["pts"], (), "Kyle Morgan"))
            it.meta.update(team="Member Support", kyle=True)
        for i, r in enumerate(sc.MS_REMOVED, 1):
            it = self.new_item(f"US-MSU-R{i}", "User Story", None)
            it.create(cal.day(*r["created"]), self.story_fields(r["title"], area, r["pts"]))
            it.transition(cal.day(*r["removed"]), "Removed", comment="Descoped.")
            it.meta.update(team="Member Support", removed=True)

    # ------------------------------------------------------------------ bugs
    def build_bugs(self, team: str):
        cal, now = self.cal, self.now
        rng = self.rng("bugs", team)
        flow = sc.BUG_FLOW[team]
        planted = [b for b in sc.PLANTED_BUGS if b["team"] == team]
        bugs = []
        pre_days = cal.wdays(cal.start(7), cal.finish(8))
        for _ in range(flow["start"]):
            bugs.append(dict(created=rng.choice(pre_days), sprint=8, planted=None))
        for s in range(9, 15):
            opened, _closed = flow["flow"][s]
            here = [b for b in planted if b["created"][0] == s]
            days = cal.sprint_days(s, 5 if s == 14 else 10)
            for b in here:
                bugs.append(dict(created=cal.day(*b["created"]), sprint=s, planted=b))
            for _ in range(opened - len(here)):
                bugs.append(dict(created=rng.choice(days), sprint=s, planted=None))
        bugs.sort(key=lambda b: (b["created"], b["planted"] is not None))
        titles = list(sc.BUG_TITLES[team])
        gen = [b for b in bugs if not b["planted"]]
        assert len(titles) == len(gen), f"{team}: {len(titles)} bug titles for {len(gen)} generated bugs"
        for b, t in zip(gen, titles):
            b["title"] = t
        # closures
        for s in range(9, 15):
            k = flow["flow"][s][1]
            days = cal.sprint_days(s, 5 if s == 14 else 10)
            for cd in sorted(rng.sample(days, k)):
                cands = [b for b in bugs if not b["planted"] and "close" not in b
                         and b["created"] <= cd - dt.timedelta(days=3)]
                cands.sort(key=lambda b: b["created"])
                b = rng.choice(cands[: max(1, int(len(cands) * 0.6))])
                b["close"] = cd
                b["close_sprint"] = s
        open_gen = [b for b in gen if "close" not in b]
        eng = sc.ENGINEERS[team]
        # attributes of open bugs
        if team == "Mobile Banking":
            sev_pool, pri_pool, st_pool = [], [], []
            for v, n in sc.MOBILE_OPEN_SEVERITY.items():
                sev_pool += [v] * (n - sum(1 for p in planted if p["severity"] == v))
            for v, n in sc.MOBILE_OPEN_PRIORITY.items():
                pri_pool += [v] * (n - sum(1 for p in planted if p["priority"] == v))
            for v, n in sc.MOBILE_OPEN_STATE.items():
                st_pool += [v] * (n - sum(1 for p in planted if p["state"] == v))
            assert len(sev_pool) == len(pri_pool) == len(st_pool) == len(open_gen), team
            rng.shuffle(sev_pool)
            rng.shuffle(st_pool)
            for b, sv, st in zip(open_gen, sev_pool, st_pool):
                b["severity"], b["state"] = sv, st
            by_sev = sorted(open_gen, key=lambda b: (b["severity"], rng.random()))
            pri_sorted = sorted(pri_pool)
            for _ in range(6):  # light shuffle: neighbours swap
                j = rng.randrange(len(pri_sorted) - 1)
                pri_sorted[j], pri_sorted[j + 1] = pri_sorted[j + 1], pri_sorted[j]
            for b, pr in zip(by_sev, pri_sorted):
                b["priority"] = pr
        else:
            for b in open_gen:
                r = rng.random()
                b["state"] = "New" if r < 0.55 else ("Active" if r < 0.9 or team == "Member Support" else "Resolved")
        for b in gen:
            if "severity" not in b:
                b["severity"] = rng.choices([1, 2, 3, 4], [5, 25, 45, 25])[0]
            if "priority" not in b:
                b["priority"] = min(4, max(1, b["severity"] + rng.choice([-1, 0, 0, 1])))
            if team == "Member Support":
                b["priority"] = max(2, b["priority"])  # no P1 bugs inside the MS area (section 9 #5)
        # escaped-defect tags
        if team == "Mobile Banking":
            recent = [b for b in gen if b["sprint"] >= 11]
            need = sc.MOBILE_ESCAPED_SINCE_S11 - sum(1 for p in planted if "escaped-defect" in p["tags"])
            for b in rng.sample(recent, need):
                b["escaped"] = True
            for b in gen:
                if b["sprint"] < 11 and rng.random() < 0.2:
                    b["escaped"] = True
        else:
            for b in gen:
                b["escaped"] = rng.random() < 0.3
        # parents (~40%): Features of the team in flight, never a Feature closed before the bug is
        team_features = [f for f in sc.FEATURES if f["team"] == team]
        for b in gen:
            s = max(b["sprint"], 9)
            ok = [f["key"] for f in team_features if f["start"] <= s <= f.get("original_target", f["target"])
                  and (not f.get("closed_sprint") or b.get("close_sprint", 99) <= f["closed_sprint"])]
            b["parent"] = rng.choice(ok) if ok and rng.random() < 0.4 else None
        # emit
        area = sc.TEAM_AREA[team]
        eng_open = [e for e in eng if e != "Ethan Brooks"] if team == "Mobile Banking" else eng
        last_open_day = cal.day(14, 5)
        for i, b in enumerate(bugs, 1):
            p = b["planted"]
            if p:
                key, title, parent = p["key"], p["title"], p["parent"]
                pri, sev, state, tags, assigned = p["priority"], p["severity"], p["state"], list(p["tags"]), p["assigned"]
            else:
                key, title, parent = f"BUG-{TEAM_PREFIX[team]}-{i:03d}", b["title"], b["parent"]
                pri, sev = b["priority"], b["severity"]
                state = "Closed" if "close" in b else b["state"]
                tags = ["escaped-defect"] if b.get("escaped") else []
                assigned = None
                if state == "Closed":
                    assigned = rng.choice(eng)
                elif state in ("Active", "Resolved") or pri == 1 or rng.random() < 0.5:
                    assigned = rng.choice(eng_open)
            it = self.new_item(key, "Bug", parent)
            it.meta.update(team=team, bug=True)
            fields = {F_TITLE: title, F_AREA: full_area(area), F_ITER: P, F_PRIORITY: pri,
                      F_SEVERITY: sc.SEVERITY_LABEL[sev],
                      "Microsoft.VSTS.TCM.ReproSteps": repro_steps(title)}
            if tags:
                fields[F_TAGS] = tag_str(tags)
            if assigned and state == "New":
                fields[F_ASSIGNED] = assigned
            it.create(b["created"], fields)
            self.bug_lifecycle(it, rng, b["created"], state, assigned, b.get("close"), last_open_day)

    def bug_lifecycle(self, it, rng, created, state, assigned, close, last_open_day):
        cal = self.cal
        if state == "New":
            return
        end = close or last_open_day
        span = cal.wdays(cal.add_wd(created, 1), end) or [created]
        if state == "Closed":
            ai = rng.randrange(max(0, len(span) - 4), len(span))
            ri = rng.randrange(ai, len(span))
            it.transition(span[ai], "Active", {F_ASSIGNED: assigned} if assigned else None)
            it.transition(span[ri], "Resolved")
            it.transition(close, "Closed")
            return
        ai = rng.randrange(0, len(span))
        it.transition(span[ai], "Active", {F_ASSIGNED: assigned} if assigned else None)
        if state == "Resolved":
            it.transition(span[rng.randrange(ai, len(span))], "Resolved")

    def build_root_bugs(self):
        cal = self.cal
        for b in sc.ROOT_BUGS:
            rng = self.rng("rootbug", b["key"])
            it = self.new_item(b["key"], "Bug", b["parent"])
            it.meta.update(team=None, bug=True, root_bug=True)
            it.create(cal.day(*b["created"]), {
                F_TITLE: b["title"], F_AREA: P, F_ITER: P, F_PRIORITY: b["priority"],
                F_SEVERITY: sc.SEVERITY_LABEL[b["severity"]], "Microsoft.VSTS.TCM.ReproSteps": repro_steps(b["title"])})
            self.bug_lifecycle(it, rng, cal.day(*b["created"]), b["state"], b["assigned"], None, cal.day(14, 5))

    # ------------------------------------------------------------------ sandboxes (section 9)
    def build_sandboxes(self):
        for n in range(1, self.participants + 1):
            self.build_sandbox(f"P{n:02d}")

    def build_sandbox(self, pid: str):
        cal = self.cal
        rng = self.rng("sandbox", pid)
        area = f"Training\\{pid}"
        keys = []
        # Lab 9 planning copy of F5
        f9 = self.new_item(f"{pid}-L9", "Feature", None)
        f9.create(cal.day(14, 3), {
            F_TITLE: f"{pid} - {sc.SANDBOX_L9_FEATURE}", F_AREA: full_area(area), F_ITER: full_pi(5),
            F_PRIORITY: 2, F_START: date_field(cal.start(15)), F_TARGET: date_field(cal.finish(17)),
            "Microsoft.VSTS.Common.BusinessValue": 20, "Microsoft.VSTS.Common.TimeCriticality": 20,
            "Microsoft.VSTS.Scheduling.Effort": 105, "Microsoft.VSTS.Common.Risk": sc.RISK_LABEL[2],
            "Microsoft.VSTS.Common.ValueArea": "Business",
            "System.Description": "<p>Your planning copy of F5 Instant Card Controls (Lab 9). Reorder, tag, "
                                  "re-estimate and schedule freely.</p>"})
        f9.meta.update(sandbox=pid)
        l9_keys = []
        for i, (title, pts, _mvp) in enumerate(sc.F5_STORIES, 1):
            it = self.new_item(f"{pid}-L9-{i:02d}", "User Story", f9.key)
            it.create(cal.day(14, 3 if i <= 10 else 4), self.story_fields(f"{pid} - {title}", area, pts))
            it.meta.update(sandbox=pid, lab=9, order=i)
            l9_keys.append(it.key)
        # Lab 11 mini set
        f11 = self.new_item(f"{pid}-L11", "Feature", None)
        f11.create(cal.day(12, 1), {
            F_TITLE: f"{pid} - {sc.SANDBOX_L11_FEATURE}", F_AREA: full_area(area), F_ITER: full_pi(4),
            F_PRIORITY: 2, F_START: date_field(cal.start(13)), F_TARGET: date_field(cal.finish(16)),
            "Microsoft.VSTS.Common.Risk": sc.RISK_LABEL[2], "Microsoft.VSTS.Common.ValueArea": "Business",
            "System.Description": "<p>Sandbox copy of Member Support's omnichannel work (Lab 11). Fix data and "
                                  "queries only here.</p>"})
        f11.meta.update(sandbox=pid)
        l11_keys = []
        for x in sc.SANDBOX_L11_ITEMS:
            wit = x["type"]
            it = self.new_item(f"{pid}-L11-{x['n']:02d}", wit, f11.key)
            it.meta.update(sandbox=pid, lab=11, n=x["n"], spec=x)
            if x.get("stale_days"):
                it.meta["stale_days"] = x["stale_days"]
            item_area = x.get("area") or area
            title = f"{pid} - {x['title']}"
            st, s = x["state"], x["sprint"]
            if wit == "Bug":
                created = cal.day(13, 7) if x["n"] == 14 else cal.day(14, 1 if x["n"] == 16 else 2)
                it.create(created, {F_TITLE: title, F_AREA: full_area(item_area), F_ITER: P,
                                    F_PRIORITY: x["priority"], F_SEVERITY: sc.SEVERITY_LABEL[x["severity"]],
                                    "Microsoft.VSTS.TCM.ReproSteps": repro_steps(x["title"])})
                if st == "Active":
                    it.transition(cal.add_wd(created, 1), "Active")
            elif st == "Removed":
                it.create(cal.day(11, 5), self.story_fields(title, item_area, x["pts"]))
                it.transition(cal.day(13, 3), "Removed", comment="Descoped.")
            elif s == 12:  # zombies: added mid-S12, never moved
                d = cal.day(12, 3 if x["n"] < 9 else 4)
                it.create(d, self.story_fields(title, item_area, x["pts"], x.get("tags", ()), None, full_iter(12)))
                it.transition(cal.add_wd(d, 1), "Active", {F_ASSIGNED: x["assigned"]})
            elif x.get("duplicate"):
                it.create(cal.day(14, 1), self.story_fields(title, item_area, x["pts"], x.get("tags", ()),
                                                            None, full_iter(14)))
            elif s == 15:
                it.create(cal.day(13, 5), self.story_fields(title, item_area, x["pts"], (), None, full_iter(15)))
            else:  # Sprint 13 or 14 work
                it.create(cal.day(12, rng.choice([6, 7, 8])) if s == 13 else cal.day(13, rng.choice([4, 5, 6])),
                          self.story_fields(title, item_area, x["pts"], x.get("tags", ())))
                it.ev(cal.day(s, 1), {F_ITER: full_iter(s)})
                a = cal.day(s, rng.choice([2, 3]) if s == 13 else rng.choice([1, 2]))
                it.transition(a, "Active", {F_ASSIGNED: x.get("assigned")} if x.get("assigned") else None)
                if st in ("Resolved", "Closed") and s == 13:
                    r = cal.day(13, rng.choice([5, 6, 7]))
                    if st == "Resolved":
                        it.transition(r, "Resolved")
                    else:
                        it.transition(r, "Resolved")
                        it.transition(cal.day(13, rng.choice([8, 9])), "Closed")
                elif st == "Closed":
                    it.transition(cal.day(14, rng.choice([3, 4, 5])), "Closed")
            l11_keys.append(it.key)
        self.sandbox_rank += l9_keys + l11_keys
        self.sandbox_features += [f9.key, f11.key]

    # ------------------------------------------------------------------ recent touches
    def add_recent_touches(self):
        cal, now = self.cal, self.now
        window = [now.date() - dt.timedelta(days=k) for k in (1, 2, 3)]
        window = [d for d in window if cal.is_wd(d)]
        for key in self.order:
            it = self.items[key]
            if it.type not in ("User Story", "Bug") or it.state != "Active" or it.meta.get("stale_days") \
                    or it.meta.get("zombie"):
                continue
            rng = self.rng("touch", key)
            opts = [d for d in window if d >= it.last_date()]
            if not opts:
                continue
            it.ev(rng.choice(opts), {}, comment=rng.choice(sc.PROGRESS_COMMENTS))

    # ------------------------------------------------------------------ times
    def assign_times(self, it: Item):
        rng = self.rng("time", it.key)
        dates = [e["date"] for e in it.events]
        assert dates == sorted(dates), f"{it.key}: events out of order {dates}"
        prev = None
        for e in it.events:
            d = e["date"]
            assert self.cal.is_wd(d), f"{it.key}: event on non-working day {d}"
            base = dt.datetime(d.year, d.month, d.day, 16, 0, tzinfo=UTC)
            if prev is not None and prev.date() == d:
                t = prev + dt.timedelta(minutes=rng.randint(2, 9))
            else:
                t = base + dt.timedelta(minutes=rng.randint(0, 80))
            if e.get("after") is not None and t <= e["after"]:
                t = e["after"] + dt.timedelta(minutes=rng.randint(1, 4))
            if prev is not None and t <= prev:
                t = prev + dt.timedelta(minutes=1)
            assert t <= base + dt.timedelta(hours=3), f"{it.key}: time overflow {t}"
            assert t < self.now, f"{it.key}: event {t} after now"
            e["at"] = t
            prev = t

    @staticmethod
    def event_time(it: Item, state: str):
        for e in it.events:
            if e["fields"].get(F_STATE) == state:
                return e["at"]
        return None

    # ------------------------------------------------------------------ Feature lifecycle
    def finish_features(self):
        cal = self.cal
        children = defaultdict(list)
        for k in self.order:
            it = self.items[k]
            if it.type == "User Story" and it.parent:
                children[it.parent].append(it)
        for f in sc.FEATURES:
            it = self.items[f["key"]]
            evs = []
            for tag in it.meta["late_tags"]:
                evs.append((cal.day(*sc.TAG_EVENTS[tag]), "tag", tag))
            if f["key"] == "F10":
                ch = sc.F10_CHANGE
                evs.append((cal.day(ch["sprint"], ch["day"]), "f10", None))
            acts = [t for t in (self.event_time(c, "Active") for c in children[f["key"]]) if t]
            if f["state"] in ("Active", "Closed") and acts:
                first = min(acts)
                evs.append((first.date(), "activate", first))
            if f["state"] == "Closed":
                last = max(self.event_time(c, "Closed") for c in children[f["key"]])
                limit = cal.finish(f["closed_sprint"])
                k = self.rng("fclose", f["key"]).choice([1, 2])
                d = cal.add_wd(last.date(), k)
                if d > limit:
                    d = cal.add_wd(last.date(), 1)
                assert d <= limit, f"{f['key']}: cannot close within Sprint {f['closed_sprint']}"
                evs.append((d, "close", None))
            evs.sort(key=lambda e: (e[0], ["tag", "activate", "f10", "close"].index(e[1])))
            tags = list(it.meta["tags"])
            for d, kind, arg in evs:
                if kind == "tag":
                    tags.append(arg)
                    comment = {"PI4-Committed": sc.PI4_COMMENT, "PI5-Candidate": sc.PI5_COMMENT,
                               "at-risk": sc.AT_RISK_COMMENT}[arg]
                    it.ev(d, {F_TAGS: tag_str(tags)}, comment=comment)
                elif kind == "activate":
                    it.transition(d, "Active", after=arg)
                elif kind == "f10":
                    ch = sc.F10_CHANGE
                    it.ev(d, {F_TARGET: date_field(cal.finish(ch["new_target"])),
                              F_ITER: full_pi(sc.pi_of(ch["new_target"]))}, comment=ch["comment"])
                elif kind == "close":
                    it.transition(d, "Closed", comment="All child stories closed.")
            assert it.state == f["state"], (f["key"], it.state, f["state"])
            self.assign_times(it)
        for e in sc.EPICS:
            self.assign_times(self.items[e["key"]])

    # ------------------------------------------------------------------ links, ranks
    def build_links(self):
        for pred, succ in sc.DEPENDENCIES:
            assert pred in self.items and succ in self.items, (pred, succ)
            self.items[succ].links.append({"type": "Predecessor", "target": pred})
        for a, b, comment in sc.RELATED_LINKS:
            assert a in self.items and b in self.items, (a, b)
            self.items[a].links.append({"type": "Related", "target": b, "comment": comment})

    def stack_ranks(self) -> dict[str, float]:
        order = list(self.rank_order)  # Epics, Features
        by_title = {}
        for team in sc.DELIVERY_TEAMS:
            team_items = [k for k in self.order if self.items[k].meta.get("team") == team
                          and self.items[k].type == "User Story"]
            s14 = [k for k in self.s14_keys[team] if self.items[k].state != "Closed"]
            first = []
            if team == "Digital Accounts":
                title_of = {k: self.events_title(k) for k in team_items}
                by_title = {title_of[k]: k for k in team_items}
                committed = [by_title[t] for t in sc.DA_COMMITTED_ORDER]
                first = [k for k in s14 if k not in committed] + committed + \
                        [f"F5-{i:02d}" for i in range(1, len(sc.F5_STORIES) + 1)]
            else:
                first = s14
            future = sorted([k for k in team_items if self.items[k].meta.get("future") and k not in first],
                            key=lambda k: self.items[k].meta.get("sprint") or 99)
            rest = [k for k in team_items if k not in first and k not in future]
            open_rest = [k for k in rest if self.items[k].state not in ("Closed", "Removed")]
            done_rest = [k for k in rest if k not in open_rest]
            bugs = [k for k in self.order if self.items[k].meta.get("team") == team and self.items[k].type == "Bug"]
            open_bugs = [k for k in bugs if self.items[k].state != "Closed"]
            order += first + future + open_rest + open_bugs + done_rest + [k for k in bugs if k not in open_bugs]
        order += [k for k in self.order if self.items[k].meta.get("root_bug")]
        order += self.sandbox_features + self.sandbox_rank
        ranked = set(order)
        missing = [k for k in self.order if k not in ranked]
        assert not missing, f"no stack rank for {missing[:5]}"
        assert len(order) == len(set(order)), "duplicate stack rank entries"
        return {k: float((i + 1) * 10) for i, k in enumerate(order)}

    def events_title(self, key: str) -> str:
        return self.items[key].events[0]["fields"][F_TITLE]

    # ------------------------------------------------------------------ build
    def build(self) -> dict:
        self.s14_keys: dict[str, list[str]] = {}
        self.sandbox_rank: list[str] = []
        self.sandbox_features: list[str] = []
        self.build_portfolio()
        for team in sc.DELIVERY_TEAMS:
            self.build_history(team)
        for team in sc.DELIVERY_TEAMS:
            self.build_sprint14(team)
        self.build_future()
        self.build_member_support_planted()
        for team in sc.DELIVERY_TEAMS:
            self.build_bugs(team)
        self.build_root_bugs()
        self.build_sandboxes()
        self.add_recent_touches()
        portfolio = {e["key"] for e in sc.EPICS} | {f["key"] for f in sc.FEATURES}
        for k in self.order:
            if k not in portfolio:
                self.assign_times(self.items[k])
        self.finish_features()
        self.build_links()
        ranks = self.stack_ranks()
        return self.emit(ranks)

    def emit(self, ranks: dict[str, float]) -> dict:
        cal = self.cal
        work_items, seen = [], set()
        for k in self.order:
            it = self.items[k]
            if it.parent:
                assert it.parent in seen, f"{k}: parent {it.parent} not emitted first"
            revs = []
            for i, e in enumerate(it.events):
                stamp = iso(e["at"])
                fields = {f: (stamp if v == AT else v) for f, v in e["fields"].items()}
                if i == 0:
                    fields[F_STACKRANK] = ranks[k]
                rev = {"at": stamp, "fields": fields}
                if e["comment"]:
                    rev["comment"] = e["comment"]
                revs.append(rev)
            for a, b in zip(revs, revs[1:]):
                assert a["at"] < b["at"], f"{k}: revision times not increasing"
            work_items.append({"key": k, "type": it.type, "parent": it.parent, "revisions": revs, "links": it.links})
            seen.add(k)
        iterations = []
        for pi, sprints in sc.PIS.items():
            iterations.append({"path": f"PI {pi}", "start": cal.start(sprints[0]).isoformat(),
                               "finish": cal.finish(sprints[-1]).isoformat()})
            for s in sprints:
                iterations.append({"path": sc.iteration_rel(s), "start": cal.start(s).isoformat(),
                                   "finish": cal.finish(s).isoformat()})
        pids = [f"P{n:02d}" for n in range(1, self.participants + 1)]
        areas = list(sc.TOP_AREAS) + [f"Training\\{p}" for p in pids]
        return {
            "schema": SCHEMA,
            "generated_at": iso(self.now),
            "now": iso(self.now),
            "project": {"name": P, "description": sc.PROJECT_DESCRIPTION, "process": sc.PROCESS},
            "calendar": {"sprint14_start": cal.s14.isoformat(), "iterations": iterations},
            "areas": areas,
            "teams": self.teams(pids),
            "work_items": work_items,
            "artifacts": self.artifacts,
        }

    def teams(self, pids) -> list[dict]:
        cal = self.cal
        days_off = [{"iteration": sc.iteration_rel(s), "start": cal.day(s, ds[0]).isoformat(),
                     "end": cal.day(s, ds[-1]).isoformat()} for s, ds in sc.TEAM_DAYS_OFF.items()]

        def team(name, areas, levels, sprints, participant=None, is_default=False):
            return {
                "name": name, "description": sc.TEAM_DESCRIPTIONS.get(name, f"Training sandbox for {participant}."),
                "is_default": is_default,
                # "areas"/"default_area" are the authoritative team field values (contract extension);
                # "area"/"include_sub_areas" mirror the default value for older consumers.
                "areas": [{"path": p, "include_children": c} for p, c in areas],
                "default_area": areas[0][0],
                "area": areas[0][0], "include_sub_areas": areas[0][1],
                "iterations": [sc.iteration_rel(s) for s in sprints],
                "backlog_iteration": "", "default_iteration_macro": "@currentIteration",
                "bugs_behavior": "asRequirements",
                "backlog_levels": {"epics": levels[0], "features": levels[1], "stories": levels[2]},
                "working_days": list(sc.WORKING_DAYS),
                "team_days_off": [d for d in days_off if int(d["iteration"].rsplit(" ", 1)[1]) in sprints],
                "participant": participant,
            }

        out = [team("HarborPoint Team", sc.DEFAULT_TEAM_AREAS, (True, True, True), sc.ALL_SPRINTS, is_default=True),
               team("Digital Portfolio", [("Digital", True)], (True, True, False), sc.ALL_SPRINTS)]
        for t in sc.DELIVERY_TEAMS:
            out.append(team(t, [(sc.TEAM_AREA[t], False)], (False, True, True), sc.ALL_SPRINTS))
        for p in pids:
            out.append(team(f"{p} Sandbox", [(f"Training\\{p}", False)], (False, True, True), tuple(range(15, 21)),
                            participant=p))
        return out


def repro_steps(title: str) -> str:
    return (f"<p><b>Observed:</b> {title}.</p><ol><li>Sign in as a test member.</li>"
            f"<li>Follow the flow described in the title.</li><li>Observe the behavior.</li></ol>"
            f"<p><b>Expected:</b> the flow completes correctly.</p>")


# ============================================================================ artifacts
PLACEHOLDER_ARTIFACTS = {"query_folders": [], "queries": [], "wiki_pages": [], "dashboards": [],
                         "delivery_plans": [], "_placeholder": "content/artifacts.yaml not found"}


def load_artifacts(path: Path | None, sprint14_start: dt.date) -> dict:
    """Load content/artifacts.yaml (optional) and substitute {sprint14_start} and {project}."""
    if path is None or not path.exists():
        return json.loads(json.dumps(PLACEHOLDER_ARTIFACTS))
    import yaml  # PyYAML, installed in the project venv

    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}

    def sub(v):
        if isinstance(v, str):
            return v.replace("{sprint14_start}", sprint14_start.isoformat()).replace("{project}", P)
        if isinstance(v, list):
            return [sub(x) for x in v]
        if isinstance(v, dict):
            return {k: sub(x) for k, x in v.items()}
        return v

    return sub(data)


def build_dataset(now: dt.datetime | str | None = None, sprint14_start: dt.date | str | None = None,
                  participants: int = 3, artifacts_path: Path | str | None = "default") -> dict:
    if now is None:
        now = (dt.datetime.now(UTC) - dt.timedelta(minutes=5)).replace(second=0, microsecond=0)
    elif isinstance(now, str):
        now = parse_now(now)
    if sprint14_start is None:
        sprint14_start = default_sprint14_start(now)
    elif isinstance(sprint14_start, str):
        sprint14_start = dt.date.fromisoformat(sprint14_start)
    if artifacts_path == "default":
        artifacts_path = Path(__file__).resolve().parent.parent / "content" / "artifacts.yaml"
    artifacts = load_artifacts(Path(artifacts_path) if artifacts_path else None, sprint14_start)
    return Generator(now, sprint14_start, participants, artifacts).build()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m harborpoint.generate", description=__doc__.split("\n")[0])
    ap.add_argument("--now", help="ISO-8601 UTC timestamp (default: current UTC minus 5 minutes)")
    ap.add_argument("--sprint14-start", help="Monday of Sprint 14 (default: Monday of the week before now)")
    ap.add_argument("--participants", type=int, default=3, help="number of participant sandboxes (default 3)")
    ap.add_argument("--out", default="out/dataset.json")
    ap.add_argument("--artifacts", default="content/artifacts.yaml", help="optional artifacts YAML to merge")
    args = ap.parse_args(argv)
    try:
        data = build_dataset(args.now, args.sprint14_start, args.participants, args.artifacts)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=1, ensure_ascii=False, sort_keys=False) + "\n", encoding="utf-8")
    n_rev = sum(len(w["revisions"]) for w in data["work_items"])
    print(f"wrote {out}: {len(data['work_items'])} work items, {n_rev} revisions, now={data['now']}, "
          f"sprint14_start={data['calendar']['sprint14_start']}, participants={args.participants}"
          + ("" if "_placeholder" not in data["artifacts"] else " (artifacts placeholder)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

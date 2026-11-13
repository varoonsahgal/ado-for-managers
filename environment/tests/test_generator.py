"""Unit tests for the HarborPoint seed generator and World Bible facts verification (offline, stdlib only)."""
from __future__ import annotations

import copy
import datetime as dt
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from harborpoint import generate, verify  # noqa: E402
from harborpoint.facts import compute  # noqa: E402

UTC = dt.timezone.utc
S14 = dt.date(2026, 10, 26)  # World Bible example: Sprint 14 = Mon 26 Oct - Fri 6 Nov 2026
NOW = "2026-11-03T10:00:00Z"  # Sprint 14 day 7 (Tuesday, week 2)

_cache: dict = {}


def dataset(now=NOW, s14=S14, participants=3):
    key = (now, s14, participants)
    if key not in _cache:
        _cache[key] = generate.build_dataset(now, s14, participants)
    return _cache[key]


def ts(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


class GeneratorStructureTests(unittest.TestCase):
    def test_deterministic(self):
        a = json.dumps(generate.build_dataset(NOW, S14, 3), sort_keys=True)
        b = json.dumps(generate.build_dataset(NOW, S14, 3), sort_keys=True)
        self.assertEqual(a, b)

    def test_revisions_strictly_increasing_and_not_after_now(self):
        d = dataset()
        now = ts(d["now"])
        for w in d["work_items"]:
            times = [ts(r["at"]) for r in w["revisions"]]
            self.assertTrue(all(a < b for a, b in zip(times, times[1:])), w["key"])
            self.assertTrue(all(t <= now for t in times), w["key"])
            for t in times:
                self.assertLess(t.weekday(), 5, w["key"])
                self.assertTrue(dt.time(16, 0) <= t.time() <= dt.time(19, 0), (w["key"], t))

    def test_parents_before_children(self):
        seen = set()
        for w in dataset()["work_items"]:
            if w["parent"]:
                self.assertIn(w["parent"], seen, w["key"])
            seen.add(w["key"])

    def test_revision_one_is_new_with_stack_rank(self):
        for w in dataset()["work_items"]:
            f = w["revisions"][0]["fields"]
            self.assertEqual(f["System.State"], "New", w["key"])
            self.assertIn("Microsoft.VSTS.Common.StackRank", f, w["key"])
            self.assertTrue(f["System.AreaPath"].startswith("HarborPoint"), w["key"])

    def test_contract_shape(self):
        d = dataset()
        self.assertEqual(d["schema"], "harborpoint-dataset/1")
        self.assertEqual(d["project"], {"name": "HarborPoint", "description": d["project"]["description"],
                                        "process": "Agile"})
        self.assertEqual(d["calendar"]["sprint14_start"], "2026-10-26")
        paths = [i["path"] for i in d["calendar"]["iterations"]]
        self.assertEqual(paths[:2], ["PI 3", "PI 3\\Sprint 9"])
        self.assertEqual(len(paths), 15)
        self.assertIn("Training\\P03", d["areas"])
        self.assertLess(d["areas"].index("Training"), d["areas"].index("Training\\P01"))
        names = [t["name"] for t in d["teams"]]
        self.assertEqual(names[:2], ["HarborPoint Team", "Digital Portfolio"])
        self.assertIn("P01 Sandbox", names)
        default = d["teams"][0]
        self.assertEqual(default["areas"][0], {"path": "", "include_children": False})
        self.assertNotIn("Training", [a["path"] for a in default["areas"]])

    def test_sprint_calendar(self):
        it = {i["path"]: i for i in dataset()["calendar"]["iterations"]}
        self.assertEqual(it["PI 4\\Sprint 14"], {"path": "PI 4\\Sprint 14", "start": "2026-10-26",
                                                 "finish": "2026-11-06"})
        self.assertEqual(it["PI 3"]["start"], it["PI 3\\Sprint 9"]["start"])
        self.assertEqual(it["PI 5"]["finish"], it["PI 5\\Sprint 20"]["finish"])

    def test_default_sprint14_start_is_monday_of_previous_week(self):
        for day in range(7, 14):
            now = dt.datetime.combine(S14 + dt.timedelta(days=day), dt.time(12), UTC)
            self.assertEqual(generate.default_sprint14_start(now), S14)

    def test_now_outside_sprint14_week2_rejected(self):
        with self.assertRaises(ValueError):
            generate.build_dataset("2026-10-28T12:00:00Z", S14, 1)
        with self.assertRaises(ValueError):
            generate.build_dataset("2026-11-09T12:00:00Z", S14, 1)

    def test_artifacts_merged_or_placeholder(self):
        d = dataset()
        for k in ("query_folders", "queries", "wiki_pages", "dashboards", "delivery_plans"):
            self.assertIn(k, d["artifacts"])
        txt = json.dumps(d["artifacts"])
        self.assertNotIn("{project}", txt)
        self.assertNotIn("{sprint14_start}", txt)
        missing = generate.build_dataset(NOW, S14, 1, artifacts_path=Path(tempfile.gettempdir()) / "nope.yaml")
        self.assertIn("_placeholder", missing["artifacts"])

    def test_participant_sandboxes(self):
        d = dataset(participants=5)
        titles = [w["revisions"][0]["fields"]["System.Title"] for w in d["work_items"]]
        for p in ("P01", "P05"):
            self.assertIn(f"{p} - Omnichannel Service Requests (sandbox)", titles)
            self.assertIn(f"{p} - Instant Card Controls (planning copy)", titles)
            self.assertEqual(sum(t.startswith(f"{p} - ") for t in titles), 2 + 18 + 20)
        self.assertNotIn("P06 - Agent queue view", titles)


class WorldBibleFactsTests(unittest.TestCase):
    def assertFacts(self, data):
        f = compute(data)
        msg = "\n".join(f"{c['id']}: expected {c['expected']!r} got {c['actual']!r}" for c in f.failures)
        self.assertEqual(f.failures, [], msg)
        self.assertGreater(len(f.checks), 250)
        return f

    def test_all_world_bible_facts_pass(self):
        f = self.assertFacts(dataset())
        o = f.out
        self.assertEqual([o["velocity"]["Member Support"][n]["done"] for n in range(9, 14)], [18, 17, 19, 13, 8])
        self.assertEqual(o["lab3_at_risk"], ["F2", "F7", "F9", "F13", "F15", "F19", "F21", "F23"])
        self.assertEqual(o["features"]["F2"]["pct"], 61)
        self.assertEqual(o["security_compliance"]["pct"], 58)

    def test_facts_pass_for_several_now_values_in_sprint14_week2(self):
        nows = ["2026-11-02T08:30:00Z",  # Monday (day 6), before the 16:00 event window
                "2026-11-04T18:30:00Z",  # Wednesday (day 8), inside the event window
                "2026-11-06T23:00:00Z",  # Friday (day 10), late
                "2026-11-08T12:00:00Z"]  # Sunday after day 10
        for now in nows:
            with self.subTest(now=now):
                self.assertFacts(dataset(now=now))

    def test_other_sprint14_start(self):
        self.assertFacts(dataset(now="2027-03-09T17:45:00Z", s14=dt.date(2027, 3, 1), participants=30))

    def test_verify_detects_mismatch(self):
        d = copy.deepcopy(dataset())
        # Inflate one Mobile Banking history story: velocity, mix and Feature rollups must all fail.
        w = next(x for x in d["work_items"] if x["key"] == "US-MOB-001")
        w["revisions"][0]["fields"]["Microsoft.VSTS.Scheduling.StoryPoints"] += 5
        ids = {c["id"] for c in compute(d).failures}
        self.assertIn("velocity.Mobile Banking.S9", ids)
        self.assertIn("feature.F1", ids)
        # A revision in the future must also be caught.
        d2 = copy.deepcopy(dataset())
        d2["work_items"][10]["revisions"][-1]["at"] = "2026-11-04T17:00:00Z"
        self.assertIn("structure.problems", {c["id"] for c in compute(d2).failures})

    def test_cli_generate_and_verify(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "dataset.json"
            buf = io.StringIO()
            with redirect_stdout(buf), redirect_stderr(buf):
                rc = generate.main(["--now", NOW, "--sprint14-start", "2026-10-26", "--participants", "2",
                                    "--out", str(out), "--artifacts", str(ROOT / "content" / "artifacts.yaml")])
                self.assertEqual(rc, 0, buf.getvalue())
                rc = verify.main([str(out)])
            self.assertEqual(rc, 0, buf.getvalue())
            self.assertTrue((Path(tmp) / "facts.md").exists())
            facts = json.loads((Path(tmp) / "facts.json").read_text())
            self.assertTrue(facts["passed"])
            # verify exits non-zero on a broken dataset
            data = json.loads(out.read_text())
            data["work_items"] = [w for w in data["work_items"] if w["key"] != "MB14-07"]
            out.write_text(json.dumps(data))
            with redirect_stdout(buf), redirect_stderr(buf):
                self.assertEqual(verify.main([str(out)]), 1)


if __name__ == "__main__":
    unittest.main()

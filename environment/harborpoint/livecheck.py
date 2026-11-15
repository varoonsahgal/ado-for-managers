"""Live checks of lab claims against a provisioned project (read-only).

Runs WIQL queries the way participants build them, and prints the numbers the labs quote.
Usage: python -m harborpoint.livecheck --org https://dev.azure.com/ORG [--project HarborPoint] [--pat-file F]
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

API = "7.1"


class Live:
    def __init__(self, org: str, project: str, pat: str):
        self.org, self.project = org.rstrip("/"), project
        self.auth = "Basic " + base64.b64encode(f":{pat}".encode()).decode()

    def _req(self, method: str, url: str, body=None):
        data = json.dumps(body).encode() if body is not None else None
        r = urllib.request.Request(url, data=data, method=method,
                                   headers={"Authorization": self.auth, "Content-Type": "application/json"})
        with urllib.request.urlopen(r) as resp:
            return json.loads(resp.read() or b"{}")

    def wiql(self, q: str, team: str | None = None) -> list[int]:
        base = f"{self.org}/{urllib.parse.quote(self.project)}"
        if team:
            base += "/" + urllib.parse.quote(team)
        d = self._req("POST", f"{base}/_apis/wit/wiql?api-version={API}", {"query": q})
        if "workItemRelations" in d:
            return d["workItemRelations"]
        return [w["id"] for w in d.get("workItems", [])]

    def items(self, ids: list[int], fields: list[str]) -> list[dict]:
        out = []
        for i in range(0, len(ids), 200):
            chunk = ids[i:i + 200]
            d = self._req("POST", f"{self.org}/{urllib.parse.quote(self.project)}/_apis/wit/workitemsbatch?api-version={API}",
                          {"ids": chunk, "fields": fields})
            out += d["value"]
        return [{"id": w["id"], **w["fields"]} for w in out]


P = "HarborPoint"
F = ["System.Id", "System.Title", "System.WorkItemType", "System.State", "System.AssignedTo", "System.AreaPath",
     "System.IterationPath", "System.Tags", "Microsoft.VSTS.Scheduling.StoryPoints", "System.Parent",
     "Microsoft.VSTS.Common.Priority", "Microsoft.VSTS.Common.Severity", "System.ChangedDate", "System.NodeName"]


def who(v):
    return (v or {}).get("displayName") if isinstance(v, dict) else v


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--org", required=True)
    ap.add_argument("--project", default=P)
    ap.add_argument("--pat-file", default="~/.config/harborpoint/pat")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    pat = os.environ.get("AZDO_PAT") or Path(a.pat_file).expanduser().read_text().strip()
    L = Live(a.org, a.project, pat)
    only = set(filter(None, a.only.split(",")))

    def sec(name):
        return not only or name in only

    titles: dict[int, str] = {}

    def title(i):
        if i is None:
            return None
        if i not in titles:
            titles[i] = L.items([i], ["System.Title"])[0]["System.Title"]
        return titles[i]

    teams = {"Mobile Banking": r"HarborPoint\Digital\Mobile Banking", "Digital Accounts": r"HarborPoint\Digital\Digital Accounts",
             "Security": r"HarborPoint\Security", "Core Platform": r"HarborPoint\Core Platform",
             "Branch Experience": r"HarborPoint\Branch Experience", "Member Support": r"HarborPoint\Member Support"}

    if sec("lab2-part1"):
        print("== Lab 2 Part 1: Sprint 14 stories by Feature, per team")
        for team, area in teams.items():
            ids = L.wiql(f"SELECT [System.Id] FROM WorkItems WHERE [System.AreaPath] UNDER '{area}' AND "
                         f"[System.IterationPath] = @CurrentIteration AND [System.WorkItemType] = 'User Story'", team)
            rows = L.items(ids, F)
            agg = defaultdict(lambda: [0, 0])
            for r in rows:
                k = title(r.get("System.Parent")) or "(no parent)"
                agg[k][0] += 1
                agg[k][1] += r.get("Microsoft.VSTS.Scheduling.StoryPoints") or 0
            print(f"  {team}: " + " · ".join(f"{k} ({n}, {p:g})" for k, (n, p) in agg.items()))

    if sec("lab2-signals"):
        mb = teams["Mobile Banking"]
        print("== Lab 2 signals (Mobile Banking)")
        rows = L.items(L.wiql(f"SELECT [System.Id] FROM WorkItems WHERE [System.AreaPath] UNDER '{mb}' AND "
                              "[System.WorkItemType] = 'Bug' AND [Microsoft.VSTS.Common.Priority] = 1 AND [System.State] <> 'Closed'"), F)
        print(f"  A open P1 bugs: {len(rows)}; unassigned: {[r['System.Title'] for r in rows if not r.get('System.AssignedTo')]}")
        rows = L.items(L.wiql(f"SELECT [System.Id] FROM WorkItems WHERE [System.AreaPath] UNDER '{mb}' AND [System.State] = 'Active'"), F)
        c = Counter(who(r.get("System.AssignedTo")) for r in rows)
        print(f"  B active by person: {c.most_common()}")
        top = c.most_common(1)[0][0]
        print(f"    {top}: {[(r['System.WorkItemType'], r['System.Title']) for r in rows if who(r.get('System.AssignedTo')) == top]}")
        rows = L.items(L.wiql(f"SELECT [System.Id] FROM WorkItems WHERE [System.AreaPath] UNDER '{mb}' AND [System.State] = 'Active' "
                              "AND [System.ChangedDate] < @Today - 7"), F)
        print(f"  C stale: {[(r['System.Title'], who(r.get('System.AssignedTo')), r['System.ChangedDate'][:10]) for r in rows]}")
        rows = L.items(L.wiql(f"SELECT [System.Id] FROM WorkItems WHERE [System.AreaPath] UNDER '{mb}' AND "
                              "[System.IterationPath] = @CurrentIteration AND [System.Tags] CONTAINS 'unplanned'", "Mobile Banking"), F)
        print(f"  D unplanned: {[(r['System.Title'], r.get('Microsoft.VSTS.Scheduling.StoryPoints')) for r in rows]}")
        rows = L.items(L.wiql(f"SELECT [System.Id] FROM WorkItems WHERE [System.AreaPath] UNDER '{mb}' AND [System.WorkItemType] = 'User Story' "
                              "AND [System.State] = 'Closed' AND [System.IterationPath] = @CurrentIteration - 1", "Mobile Banking"), F)
        orph = [r for r in rows if not r.get("System.Parent")]
        print(f"  E closed last sprint: {len(rows)} stories, {sum(r.get('Microsoft.VSTS.Scheduling.StoryPoints') or 0 for r in rows):g} pts; "
              f"no parent: {len(orph)} stories, {sum(r.get('Microsoft.VSTS.Scheduling.StoryPoints') or 0 for r in orph):g} pts")
        rows = L.items(L.wiql(f"SELECT [System.Id] FROM WorkItems WHERE [System.AreaPath] UNDER '{mb}' AND [System.WorkItemType] = 'Bug' "
                              "AND [System.State] <> 'Closed'"), F)
        print(f"  F open bugs: {len(rows)}; severity {Counter(r.get('Microsoft.VSTS.Common.Severity') for r in rows)}; "
              f"state {Counter(r['System.State'] for r in rows)}")


if __name__ == "__main__":
    main()

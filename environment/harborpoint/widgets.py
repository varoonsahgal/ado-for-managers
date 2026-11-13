"""Dashboard widget and Delivery Plan payload builders.

Widget ``settings`` are JSON *strings* (Markdown widget: raw Markdown). Shapes follow the
research notes (Microsoft Demo Generator templates); widgets are split into:

* ``SAFE`` types created by default: markdown, query_tile, query_results, chart, velocity;
* ``UNCERTAIN`` types (sprint_burndown, cfd, cycle_time, lead_time) whose settings JSON is not
  documented. They are only attempted with ``--experimental-widgets``; otherwise (or when the
  attempt fails) the provisioner prints exact manual UI steps.
"""
from __future__ import annotations

import json
import re
from typing import Any

P = "ms.vss-dashboards-web.Microsoft.VisualStudioOnline.Dashboards."
CONTRIBUTION = {
    "markdown": P + "MarkdownWidget",
    "query_tile": P + "QueryScalarWidget",
    "query_results": "ms.vss-mywork-web.Microsoft.VisualStudioOnline.MyWork.WitViewWidget",
    "chart": P + "WitChartWidget",
    "velocity": P + "VelocityWidget",
    "sprint_burndown": P + "AnalyticsSprintBurndownWidget",
    "cfd": P + "CumulativeFlowDiagramWidget",
    "cycle_time": P + "CycleTimeWidget",
    "lead_time": P + "LeadTimeWidget",
}
SETTINGS_VERSION = {"chart": (3, 0, 0)}
SAFE = {"markdown", "query_tile", "query_results", "chart", "velocity"}
UNCERTAIN = {"sprint_burndown", "cfd", "cycle_time", "lead_time"}
UI_NAME = {"markdown": "Markdown", "query_tile": "Query Tile", "query_results": "Query Results",
           "chart": "Chart for Work Items", "velocity": "Velocity", "sprint_burndown": "Sprint Burndown",
           "cfd": "Cumulative Flow Diagram", "cycle_time": "Cycle Time", "lead_time": "Lead Time"}
CHART_TYPES = {"pie": "PieChart", "bar": "BarChart", "column": "ColumnChart", "stackedBar": "StackedBarChart",
               "stackedColumn": "StackedColumnChart", "pivot": "PivotTable", "table": "PivotTable",
               "line": "LineChart", "area": "AreaChart"}
COLUMN_LABELS = {
    "System.Id": "ID", "System.WorkItemType": "Work Item Type", "System.Title": "Title", "System.State": "State",
    "System.AssignedTo": "Assigned To", "System.AreaPath": "Area Path", "System.IterationPath": "Iteration Path",
    "System.Tags": "Tags", "System.ChangedDate": "Changed Date",
    "Microsoft.VSTS.Scheduling.StartDate": "Start Date", "Microsoft.VSTS.Scheduling.TargetDate": "Target Date",
    "Microsoft.VSTS.Common.Priority": "Priority", "Microsoft.VSTS.Common.Severity": "Severity",
    "Microsoft.VSTS.Scheduling.StoryPoints": "Story Points", "Microsoft.VSTS.Common.Risk": "Risk",
}
CARD_TOGGLES = {"System.AssignedTo": "showAssignedTo", "System.State": "showState", "System.Tags": "showTags",
                "System.Id": "showId"}


def wiql_columns(wiql: str) -> list[str]:
    m = re.search(r"SELECT(.*?)FROM", wiql, re.S | re.I)
    if not m:
        return ["System.Id", "System.Title", "System.State"]
    return re.findall(r"\[([A-Za-z0-9_.]+)\]", m.group(1))


def widget_body(w: dict, *, project_id: str, team_id: str | None, query: dict | None,
                iteration: dict | None = None) -> dict:
    """Build the REST body for one widget spec (artifacts.yaml schema).

    ``query`` = {"id", "name", "wiql"}; ``iteration`` = {"id" (GUID), "path", "start", "finish"}.
    """
    t = w["type"]
    title = w.get("title") or UI_NAME[t]
    settings: Any
    if t == "markdown":
        settings = w.get("markdown", "")
    elif t == "query_tile":
        rules = [{"isEnabled": True, "backgroundColor": r["color"], "thresholdCount": r["value"],
                  "operator": r["op"]} for r in w.get("rules", [])]
        settings = {"defaultBackgroundColor": "#292e6b", "queryId": query["id"], "queryName": query["name"],
                    "colorRules": rules, "lastArtifactName": query["name"]}
    elif t == "query_results":
        cols = [{"name": COLUMN_LABELS.get(c, c.split(".")[-1]), "referenceName": c}
                for c in wiql_columns(query.get("wiql", ""))]
        settings = {"query": {"queryId": query["id"], "queryName": query["name"]}, "selectedColumns": cols,
                    "lastArtifactName": query["name"]}
    elif t == "chart":
        chart = w.get("chart") or {}
        settings = {"scope": "WorkitemTracking.Queries", "groupKey": query["id"], "title": title,
                    "chartType": CHART_TYPES.get(chart.get("type", "pie"), "PieChart"),
                    "transformOptions": {"filter": query["id"], "groupBy": chart.get("group_by", "System.State"),
                                         "orderBy": {"direction": "descending", "propertyName": "value"},
                                         "measure": {"aggregation": "count", "propertyName": ""},
                                         "historyRange": None},
                    "userColors": [], "lastArtifactName": query["name"]}
    elif t == "velocity":
        settings = {"projectId": project_id, "teamId": team_id,
                    "workItemTypeFilter": {"identifier": "BacklogCategory",
                                           "settings": "Microsoft.RequirementCategory"},
                    "aggregation": {"identifier": 1, "settings": "Microsoft.VSTS.Scheduling.StoryPoints"},
                    "numberOfIterations": int(w.get("iterations", 6)), "plannedWorkDelay": 0, "lateWorkDelay": 0,
                    "lastArtifactName": None, "showResolvedItemsAsCompleted": False}
    elif t == "sprint_burndown":
        settings = {"team": {"projectId": project_id, "teamId": team_id},
                    "iterationId": iteration["id"] if iteration else None,
                    "iterationPath": iteration["path"] if iteration else None,
                    "aggregation": {"identifier": 1, "settings": "Microsoft.VSTS.Scheduling.StoryPoints"},
                    "workItemTypeFilter": {"identifier": "BacklogCategory",
                                           "settings": "Microsoft.RequirementCategory"},
                    "timePeriodConfiguration": {"startDate": iteration["start"] if iteration else None,
                                                "endDate": iteration["finish"] if iteration else None},
                    "lastArtifactName": None}
    elif t == "cfd":
        settings = {"chartDataSettings": {"project": project_id, "team": team_id, "board": "Stories",
                                          "boardLane": None, "timePeriod": {"identifier": 0, "settings": 30},
                                          "desiredBoardColumnIds": []}, "themeName": "", "lastArtifactName": None}
    elif t in ("cycle_time", "lead_time"):
        settings = {"dataSettings": {"project": project_id, "teamIds": [team_id],
                                     "witSelector": {"identifier": "BacklogCategory",
                                                     "settings": "Microsoft.RequirementCategory"},
                                     "swimLane": None, "fieldFilters": [],
                                     "timePeriod": {"identifier": 0, "settings": 30}}, "lastArtifactName": None}
    else:  # pragma: no cover - validated earlier
        raise ValueError(f"unknown widget type {t}")
    major, minor, patch = SETTINGS_VERSION.get(t, (1, 0, 0))
    return {"name": title, "position": {"row": int(w["row"]), "column": int(w["column"])},
            "size": {"rowSpan": int(w.get("row_span", 1)), "columnSpan": int(w.get("column_span", 1))},
            "settings": settings if isinstance(settings, str) else json.dumps(settings),
            "settingsVersion": {"major": major, "minor": minor, "patch": patch},
            "contributionId": CONTRIBUTION[t]}


def manual_widget_steps(dashboard: dict, w: dict) -> str:
    """Exact UI steps for a widget that could not be (safely) created by REST."""
    scope = f"team '{dashboard['team']}'" if dashboard.get("team") else "the project"
    lines = [f"Dashboards -> '{dashboard['name']}' ({scope}) -> Edit -> Add widget -> search "
             f"'{UI_NAME[w['type']]}' -> Add. Drag it to row {w['row']}, column {w['column']}; size "
             f"{w.get('column_span', 1)}x{w.get('row_span', 1)} (columns x rows)."]
    cfg = [f"Title: '{w.get('title', UI_NAME[w['type']])}'"]
    if w.get("team") or dashboard.get("team"):
        cfg.append(f"Team: '{w.get('team') or dashboard['team']}'")
    if w.get("iteration"):
        cfg.append(f"Iteration: '{w['iteration'].split(chr(92))[-1]}' (exactly this sprint)")
    if w.get("query"):
        cfg.append(f"Query: '{w['query']}'")
    if w["type"] in ("sprint_burndown", "velocity"):
        cfg.append("Burndown/measure on: Story Points (sum)")
    if w["type"] == "cfd":
        cfg.append("Backlog: Stories; rolling period: 30 days")
    if w["type"] in ("cycle_time", "lead_time"):
        cfg.append("Backlog: Stories; rolling period: 30 days")
    lines.append("   Configure: " + "; ".join(cfg) + ". Save, then Done editing.")
    return "\n".join(lines)


def plan_body(plan: dict, team_ids: dict[str, str], sprint_dates: dict[str, tuple[str, str]]) -> dict:
    """Delivery Plan create body. ``sprint_dates``: leaf name -> (start, finish) YYYY-MM-DD."""
    toggles = {"showId": True, "showState": False, "showTags": False, "showAssignedTo": False}
    additional = []
    for ref in plan.get("card_fields", []) or []:
        if ref in CARD_TOGGLES:
            toggles[CARD_TOGGLES[ref]] = True
        else:
            additional.append({"referenceName": ref})
    markers = []
    for m in plan.get("markers", []) or []:
        start, finish = sprint_dates[m["sprint"]]
        day = finish if m.get("at") == "end" else start
        markers.append({"date": day + "T00:00:00Z", "label": m["label"], "color": m.get("color", "#106ebe")})
    return {"name": plan["name"], "description": plan.get("description", ""), "type": "deliveryTimelineView",
            "properties": {
                "teamBacklogMappings": [{"teamId": team_ids[t["team"]], "categoryReferenceName": t["backlog"]}
                                        for t in plan["teams"]],
                "cardSettings": {"fields": {**toggles, "assignedToDisplayFormat": "avatarAndFullName",
                                            "additionalFields": additional}},
                "markers": markers}}

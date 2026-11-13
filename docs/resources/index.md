---
title: "Resources"
---

# Resources

Reference material for the course and for Monday morning back at work. Everything here is written at Feature and portfolio altitude.

<div class="grid cards" markdown>

-   :material-database-search:{ .lg .middle } **Query Cookbook**

    ---

    Thirty ready-to-use manager queries, with clause tables, WIQL, the macro cheat sheet and chart limits.

    [:octicons-arrow-right-24: Open the cookbook](query-cookbook.md)

-   :material-chart-timeline-variant:{ .lg .middle } **Metrics Field Guide**

    ---

    Velocity, throughput, lead and cycle time, CFD, rollups and forecasts: how each is computed, how to read it, and how it lies.

    [:octicons-arrow-right-24: Open the guide](metrics-field-guide.md)

-   :material-file-document-edit-outline:{ .lg .middle } **Templates**

    ---

    Copy-ready Markdown for status reports, BLUF briefings, options matrices, PI outlooks, persona canvases and more.

    [:octicons-arrow-right-24: Open the templates](templates.md)

-   :material-book-alphabet:{ .lg .middle } **Glossary**

    ---

    Azure DevOps and management terms in plain language, with HarborPoint examples.

    [:octicons-arrow-right-24: Open the glossary](glossary.md)

-   :material-ferry:{ .lg .middle } **Welcome aboard**

    ---

    How the labs work, your participant ID, and the pre-flight checklist.

    [:octicons-arrow-right-24: Start here](../start/index.md)

-   :material-map-marker-path:{ .lg .middle } **Environment map**

    ---

    Areas, sprints, teams, fields, pre-built artifacts and your `P##` conventions.

    [:octicons-arrow-right-24: Open the map](../start/environment.md)

</div>

## Printable cheat sheet

The twelve paths and macros you'll use most. Print this page (the hints and code blocks expand in print).

| # | What | Where or how |
|:-:|:--|:--|
| 1 | Portfolio priorities (ranked Epics) | **Boards › Backlogs** › `HarborPoint Team` › level **Epics** |
| 2 | A team's Features with progress | **Boards › Backlogs** › team › **Features** › **Column Options** › **+ Add a rollup column** |
| 3 | Features under their Epics | Backlog **View options** › **Parents** On |
| 4 | Velocity and CFD | **Boards › Backlogs** › team › **Analytics** › **View full report** |
| 5 | Sprint burndown | **Boards › Sprints** › team › sprint › **Analytics** |
| 6 | Cross-team calendar and dependencies | **Boards › Delivery Plans** |
| 7 | Queries | **Boards › Queries** › **All** › **New query**; save to `Shared Queries/Training/P##/` |
| 8 | Dashboards | **Overview › Dashboards** › **+ New Dashboard** (name it `P## - …`) |
| 9 | Who changed what, when | Work item › **History** tab |
| 10 | This sprint, any team | `Iteration Path` `=` `@CurrentIteration` + team parameter (`± n` for other sprints) |
| 11 | Relative dates | `@Today - 14`, `@StartOfMonth - 1`, `@StartOfWeek` |
| 12 | "Open" and "nothing set" | `State Not In Closed,Removed` · a field `=` with a blank value means "has no value" |

!!! warning "Remember"
    The six delivery teams' items, order, estimates and settings are **read-only**. Your changes go in your sandbox (`HarborPoint\Training\P##`) and under your `P##` names.

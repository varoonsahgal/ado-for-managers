---
title: "Glossary"
---

# Glossary

Plain-language definitions for the Azure DevOps and management terms used in the labs. Where it helps, there's a HarborPoint example.

**Jump to:** [Azure DevOps terms](#azure-devops-terms) · [Management terms](#management-terms)

## Azure DevOps terms

Access level (Basic vs Stakeholder)
:   What you're licensed to do in Azure DevOps. **Basic** covers everything in these labs. **Stakeholder** is free and can view and add work items, view dashboards and plans, but can't reorder backlogs, use query charts, forecast, view capacity, use Analytics views or save shared queries. Executives who only read roadmaps can use Stakeholder; managers who build them need Basic.

Analytics
:   The reporting store behind Velocity, CFD, burndowns, Lead and Cycle Time, rollup columns, Analytics views and Power BI. It isn't real time: changes take a short while to appear, and trend charts are built from daily snapshots.

Area path
:   A tree that says **which team owns** a work item. *Example:* `HarborPoint\Digital\Mobile Banking`. Teams select the areas they own; a team that includes sub-areas sees all the work beneath its node.

Backlog levels
:   The rungs of the backlog hierarchy. In the Agile process: **Epics** › **Features** › **Stories** (User Stories, plus Bugs when bugs are managed with requirements). Each team chooses which levels it shows.

Capacity
:   How much work a team can take on in a sprint. The **Capacity** tab sets it per person in hours for task-based planning; at Feature level, managers estimate capacity from velocity adjusted for days off and other commitments.

Delivery Plan
:   A calendar view (**Boards › Delivery Plans**) of up to 20 team backlogs side by side, by sprint. It shows Features and Epics on a timeline, rollup progress, markers for key dates, and dependency lines. *Example:* **HarborPoint Program Plan**.

Dependency (predecessor and successor)
:   A **Predecessor/Successor** link says one item must finish before another. The predecessor finishes first; the successor waits. Delivery Plans draw these links and turn them red when a successor is scheduled to finish before its predecessor.

In-context report
:   A chart built into a page rather than a dashboard: the **Analytics** tab on a backlog (Velocity, CFD) or a sprint (Burndown Trend). Its settings are personal to you; use **Copy to Dashboard** to share it.

Inherited process
:   A customizable copy of a system process (such as Agile) at organization level, used to add fields, rules and states. Changes apply immediately to **every project** on that process, so they're a governance decision, not a team preference.

Iteration path
:   A tree of time boxes. *Example:* `HarborPoint\PI 4\Sprint 14`. Stories go in sprints; HarborPoint's Features sit on the PI node that contains their target sprint.

Macro
:   A query placeholder that resolves when the query runs, such as `@Me`, `@Today - 14` or `@CurrentIteration`. Macros keep saved queries correct as time moves on. See the [macro cheat sheet](query-cookbook.md#macro-cheat-sheet).

Portfolio backlog
:   The Features and Epics backlogs. They're ordered lists of the big work. *Example:* the **HarborPoint Team** Epics backlog is the portfolio's ranked priority list.

Query types
:   **Flat list of work items** (the only type you can chart), **Work items and direct links** (one hop of links: dependencies, orphans, empty Features) and **Tree of work items** (the Parent/Child hierarchy).

Rollup
:   A backlog column that summarizes a parent's descendants: a progress bar or a total. Progress counts only **Closed** descendants, through Parent/Child links. *Example:* **Progress by Story Points** on the Features backlog.

Stack Rank
:   The hidden field that stores backlog order in the Agile process. Dragging an item on a backlog changes it, for everyone who sees that backlog. Never bulk-edit it.

State category
:   The bucket each state belongs to: **Proposed**, **In Progress**, **Resolved**, **Completed** or **Removed**. Charts and rollups read the category, not the state name, and only **Completed** (Closed) counts as done.

Story Points
:   A team's relative size estimate for a User Story. Points are a local currency: they mean something only within one team, over time.

Tags
:   Free-text labels on work items for cross-cutting slices. *Example:* `PI4-Committed`, `blocked`. Spelling matters: a query for one spelling misses the others.

Team
:   A group with its own areas, sprints, backlogs, boards and dashboards. Most Boards views and metrics belong to one team, picked in the team selector. *Example:* **Digital Portfolio** is a portfolio team that sees both digital delivery teams.

Team days off
:   Days the whole team isn't working, such as a company holiday, set on the sprint's **Capacity** tab. Burndown ideal lines and capacity respect them; the Forecasting tool does not.

Velocity
:   Work a team completed per sprint, as a sum of Story Points or a count of items, from the **Velocity** report or widget. Useful for a team's own planning; meaningless for comparing teams. See the [Metrics Field Guide](metrics-field-guide.md#velocity).

Widget
:   A tile on a dashboard: a **Query Tile** (a count), **Query Results** (a list), **Chart for Work Items**, **Velocity**, **Cumulative Flow Diagram (CFD)**, **Markdown** and more.

WIQL
:   Work Item Query Language, the SQL-like text behind every saved query. You rarely need to write it, but reading it helps when you share or debug queries.

Work item templates
:   Team-scoped presets that pre-fill fields on a new or existing work item, managed under **Project settings › Boards › Team configuration › Templates**. Useful for standard Feature intake.

## Management terms

BLUF
:   **Bottom Line Up Front.** Put the answer and the ask in the first sentences, then the evidence. Executives read the top and decide whether to read on. See the [Executive Briefing template](templates.md#executive-briefing-bluf).

Carry-over
:   Work planned into a sprint, not finished, and moved into the next one. A little is normal. The same item carrying twice is a signal worth asking about.

Commitment reliability
:   Completed points ÷ planned points for a sprint. A steady decline matters more than any single sprint.

Cycle time
:   Days from starting work to finishing it. Azure DevOps measures from first entering an In Progress or Resolved state to Closed.

Definition of Done (DoD)
:   The team's shared checklist for "finished": tested, reviewed, accepted and **Closed**. If the definition stops short of Closed, every report under-counts the team. *Example:* `/Practices/Working Agreements and Definition of Done` in the HarborPoint wiki.

Goodhart's law
:   "When a measure becomes a target, it ceases to be a good measure." Set a velocity target and points inflate.

Lead time
:   Days from an item's creation to its completion: the requester's view of how long things take.

Little's Law
:   On average, **time in process ≈ work in progress ÷ throughput**. To deliver faster, start less.

MVP
:   **Minimum viable product.** The smallest release that delivers the core value to members. Cutting to an MVP is often the most honest way to keep a date.

Orphan work
:   Stories or bugs with no parent Feature. Some is healthy (small fixes, tech debt); a growing share means effort that serves no portfolio priority.

PI (Program Increment)
:   A fixed planning interval of several sprints. At HarborPoint, four two-week sprints. *Example:* PI 4 = Sprints 13 to 16.

PI objectives
:   What each team commits to deliver in a PI, with business value and committed vs stretch. *Example:* `/Program/PI 4 Objectives` in the wiki.

Persona
:   A research-based portrait of a type of member, used to make trade-offs explicit. *Example:* the starter personas under `/Personas/` in the wiki.

Point inflation
:   Velocity rising because estimates grow, not because output does. Visible when velocity by points climbs while the count of items finished stays flat.

RAG
:   **Red / Amber / Green** status. Only useful with written definitions that stay the same every week. See the [Status Report template](templates.md#status-report).

Throughput
:   The **count** of items finished per period. Harder to inflate than velocity, and a strong forecasting input.

Watermelon status
:   Green on the outside, red on the inside: a report that says "on track" while the data says otherwise.

WIP (work in progress)
:   Items started but not finished. Too much WIP slows everything down, at story level and at Feature level.

WSJF
:   **Weighted Shortest Job First.** A prioritization score: cost of delay (business value + time criticality + risk reduction) ÷ job size. Azure DevOps has no WSJF field, but a Feature's **Business Value**, **Time Criticality** and **Effort** let you approximate it.

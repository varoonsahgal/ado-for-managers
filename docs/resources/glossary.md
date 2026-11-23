---
title: "Glossary"
---

# Glossary

Plain-language definitions for the Azure DevOps and management terms in the labs, with a HarborPoint example where it helps and the lab that teaches each one.

**Jump to:** [Azure DevOps terms](#azure-devops-terms) · [Management terms](#management-terms) · [Course terms](#course-terms)

## Azure DevOps terms

Access level (Basic vs Stakeholder)
:   What you're licensed to do. **Basic** covers everything in these labs. **Stakeholder** is free and can view and add work items, dashboards and plans, but can't reorder backlogs, use query charts, forecast, view capacity, use Analytics views or save shared queries. Executives who only read roadmaps can use Stakeholder; managers who build them need Basic.

Analytics
:   The reporting store behind Velocity, CFD, burndowns, Lead and Cycle Time, rollup columns, Analytics views and Power BI. It isn't real time: changes take a short while to appear, and trend charts are built from daily snapshots.

Area path
:   A tree that says **which team owns** a work item. *Example:* `HarborPoint\Digital\Mobile Banking`. Teams select the areas they own; a team that includes sub-areas sees all the work beneath its node. Owning a Feature (its area) is not the same as building it (its children's areas) ([Lab 1](../day-1/lab-01-explore-the-program.md)).

Backlog levels
:   The rungs of the backlog hierarchy. In the Agile process: **Epics** › **Features** › **Stories** (User Stories, plus Bugs when bugs are managed with requirements). Each team chooses which levels it shows.

Backlog order
:   The ranking you see on a backlog, stored in the hidden **Stack Rank** field. Dragging an item changes it for everyone who sees that backlog, so never drag or bulk-edit a shared one. Priority fields are opinions; the order is the real ranking ([Lab 1](../day-1/lab-01-explore-the-program.md)).

Delivery Plan
:   A calendar view (**Boards › Delivery Plans**) of up to 20 team backlogs side by side, by sprint, with rollup progress, markers for key dates and dependency lines. It's a live editing surface: dragging a card changes the real work item. *Example:* **HarborPoint Program Plan** ([Lab 7](../day-2/lab-07-cross-team-bottleneck.md)).

Dependency (predecessor and successor)
:   A **Predecessor/Successor** link says one item must finish before another. A Delivery Plan draws the line red when the predecessor's end date falls after the successor's; equal end dates never count as a conflict. Plans draw only links between dated items on the plan, so pair every plan with a direct-links query ([Lab 7](../day-2/lab-07-cross-team-bottleneck.md), [cookbook D3](query-cookbook.md#d3)).

In-context report
:   A chart built into a page rather than a dashboard: the **Analytics** tab on a backlog (Velocity, CFD) or a sprint (Burndown Trend). Its settings are personal to you; use **Copy to Dashboard** to share it.

Inherited process
:   A customizable copy of a system process (such as Agile) at organization level, used to add fields, rules and states. Changes apply immediately to **every project** on that process, so they're a governance decision, not a team preference ([Lab 11](../day-3/lab-11-dashboard-wrong.md)).

Iteration path
:   A tree of time boxes. *Example:* `HarborPoint\PI 4\Sprint 14`. Stories go in sprints; HarborPoint's Features sit on the PI node that contains their target sprint.

Macro
:   A query placeholder that resolves when the query runs, such as `@Me`, `@Today - 14` or `@CurrentIteration`. Macros keep saved queries correct as time moves on. `@CurrentIteration` picks a sprint, not a team: pair it with an area clause ([Lab 3](../day-1/lab-03-query-toolkit.md), [macro cheat sheet](query-cookbook.md#macro-cheat-sheet)).

Portfolio backlog
:   The Features and Epics backlogs: ordered lists of the big work. *Example:* the **HarborPoint Team** Epics backlog is the portfolio's ranked priority list.

Query types
:   **Flat list of work items** for lists and charts (the only type you can chart), **Work items and direct links** for "what's missing?" (dependencies, orphans, empty Features) and **Tree of work items** for "what does this work serve?" ([Lab 3](../day-1/lab-03-query-toolkit.md)).

Rollup
:   A backlog column on a parent's row that summarizes its descendants, through Parent/Child links: a progress bar or a total. Progress counts only **Closed** descendants, and a Feature with no children shows nothing. *Example:* **Progress by Story Points** on the Features backlog ([Lab 1](../day-1/lab-01-explore-the-program.md)).

State category
:   The bucket each state belongs to: **Proposed**, **In Progress**, **Resolved**, **Completed** or **Removed**. Charts and rollups read the category, not the state name, and only **Completed** (Closed) counts as done. A story in Resolved is not done ([Lab 1](../day-1/lab-01-explore-the-program.md)).

Story Points
:   A team's relative size estimate for a User Story. Points are a local currency: they mean something only within one team, over time.

Tags
:   Free-text labels on work items for cross-cutting slices. *Example:* `PI4-Committed`, `blocked`. Spelling matters: a query for one spelling misses the others, and a tag finds only what people remembered to record ([Lab 3](../day-1/lab-03-query-toolkit.md), [Lab 11](../day-3/lab-11-dashboard-wrong.md)).

Team
:   A group with its own areas, sprints, backlogs, boards and dashboards. Most Boards views and metrics belong to one team, picked in the team selector. *Example:* **Digital Portfolio** is a portfolio team that sees both digital delivery teams.

Team days off
:   Days the whole team isn't working, such as a company holiday, set on the sprint's **Capacity** tab. Burndown ideal lines and capacity respect them; the Forecasting tool does not ([Lab 9](../day-3/lab-09-meet-the-deadline.md)).

Velocity
:   Work a team completed per sprint, as a sum of Story Points or a count of items, from the **Velocity** report or widget. It measures estimates, so it tells you how busy a team was, not what it delivered. Useful for a team's own planning; meaningless for comparing teams ([Lab 2](../day-1/lab-02-monday-morning-manager.md), [Metrics Field Guide](metrics-field-guide.md#velocity)).

Widget
:   A tile on a dashboard: a **Query Tile** (a count), **Query Results** (a list), **Chart for Work Items**, **Velocity**, **Cumulative Flow Diagram (CFD)**, **Markdown** and more. Analytics widgets read one team, so name the team in the title ([Lab 5](../day-2/lab-05-command-center.md)).

WIQL
:   Work Item Query Language, the SQL-like text behind every saved query. You rarely need to write it, but reading it helps when you share or debug queries.

Work item templates
:   Team-scoped presets that pre-fill fields on a new or existing work item, managed under **Project settings › Boards › Team configuration › Templates**. Useful for standard Feature intake.

## Management terms

BLUF
:   **Bottom Line Up Front.** Put the answer and the ask first, then the evidence. Executives read the top and decide whether to read on ([Lab 2](../day-1/lab-02-monday-morning-manager.md), [Lab 8](../day-2/lab-08-executive-status-review.md), [Executive Briefing template](templates.md#executive-briefing-bluf)).

Capacity
:   What a team will actually deliver in a period: its normal-sprint velocity minus absences, holidays, work already committed and support load. Velocity is the rate; capacity is what you'll get, and it's the only number worth forecasting with. State it as a range ([Lab 9](../day-3/lab-09-meet-the-deadline.md)).

Carry-over
:   Work planned into a sprint, not finished, and moved into the next one. It shows only as the gap between the **Planned** and **Completed** bars on the Velocity report, not as Incomplete. A little is normal; the same item carrying twice is worth asking about ([Lab 2](../day-1/lab-02-monday-morning-manager.md)).

Commitment reliability (Completed ÷ Planned)
:   The share of a sprint's planned work the team finished: Completed ÷ Planned, read from the Velocity report. Report it and its trend per team, never one team's points against another's. A steady decline matters more than any single sprint ([Lab 4](../day-1/lab-04-sprint-delivery-report.md)).

Cycle time
:   Days from starting work to finishing it: the team's view. Azure DevOps measures from first entering an In Progress or Resolved state to Closed, so a test queue shows up here ([Lab 6](../day-2/lab-06-which-team-needs-help.md)).

Definition of Done (DoD)
:   The team's shared checklist for "finished": tested, reviewed, accepted and **Closed**. If the definition stops short of Closed, every report under-counts the team. *Example:* `/Practices/Working Agreements and Definition of Done` in the HarborPoint wiki.

Empty Feature
:   A Feature with no child stories or bugs. It can't be rolled up, forecast or tracked: it's an idea with a date on it ([Lab 3](../day-1/lab-03-query-toolkit.md), [cookbook A5](query-cookbook.md#a5)).

Escaped defect
:   A bug found in production, tagged `escaped-defect` at HarborPoint. *Example:* the unowned P1 on `Mobile Check Deposit 2.0` ([Lab 2](../day-1/lab-02-monday-morning-manager.md)).

Goodhart's law
:   "When a measure becomes a target, it ceases to be a good measure." Set a velocity target and points inflate; score people on data hygiene and they game the record ([Lab 6](../day-2/lab-06-which-team-needs-help.md)).

Lead time
:   Days from an item's creation to its completion: the requester's view of how long things take.

Little's Law
:   On average, **time in process ≈ work in progress ÷ throughput**. To deliver faster, start less ([Lab 6](../day-2/lab-06-which-team-needs-help.md)).

MVP
:   **Minimum viable product.** The smallest release that delivers the core value to members. Cutting to an MVP, and ordering it ahead of the "shoulds", is often the most honest way to keep a date ([Lab 9](../day-3/lab-09-meet-the-deadline.md)).

Options matrix
:   A table of ways forward (re-sequence, reduce scope, move capacity, move the date, change the dependency) against a do-nothing baseline, each with its effect on the date, its risk, who pays and a named decider ([Lab 7](../day-2/lab-07-cross-team-bottleneck.md), [template](templates.md#options-matrix)).

Orphan work
:   Stories or bugs with no parent Feature. Some is healthy (small fixes, tech debt); a growing share means effort that serves no portfolio priority. The backlog's **Parents** view groups them under **Unparented Stories** ([Lab 3](../day-1/lab-03-query-toolkit.md), [cookbook F4](query-cookbook.md#f4)).

PI (Program Increment)
:   A fixed planning interval of several sprints. At HarborPoint, four two-week sprints. *Example:* PI 4 = Sprints 13 to 16.

PI objectives
:   What each team commits to deliver in a PI, with business value and committed vs stretch. *Example:* `/Program/PI 4 Objectives` in the wiki.

Persona
:   A research-based portrait of a type of member: behaviors, goals and breaks backed by evidence, with everything else marked as an assumption. It changes what gets built only when it reaches the acceptance criteria. *Example:* the starter personas under `/Personas/` in the wiki ([Lab 10](../day-3/lab-10-personas.md)).

Point inflation
:   Velocity rising because estimates grow, not because output does. Visible when velocity by points climbs while the count of items finished stays flat ([Lab 6](../day-2/lab-06-which-team-needs-help.md)).

RAG
:   **Red / Amber / Green** status. Only useful with written definitions that stay the same every week and a sentence of evidence beside each color ([Lab 4](../day-1/lab-04-sprint-delivery-report.md), [Status Report template](templates.md#status-report)).

Signal families (output, flow, outcomes)
:   The three kinds of evidence to read before judging a team. **Output:** how much finished (velocity, throughput, reliability). **Flow:** where work waits (CFD, cycle time, WIP). **Outcomes:** what the output was worth (quality, alignment, Feature progress). Act when all three agree; when they disagree, ask the team ([Lab 6](../day-2/lab-06-which-team-needs-help.md)).

Spill
:   Work targeted to one PI that will finish in the next. It uses next PI's capacity without appearing on next PI's list ([Lab 12](../day-3/lab-12-capstone.md)).

Stale work
:   Items **Active** but untouched for a week or more (Lab 2 uses 7 days; the Lab 11 watchlist and cookbook F1 use 14): stuck, abandoned or quietly done. Count stories and bugs only: nobody edits a Feature while its stories move ([Lab 2](../day-1/lab-02-monday-morning-manager.md), [cookbook F1](query-cookbook.md#f1)).

Throughput
:   The **count** of items finished per period. Harder to inflate than velocity, and a strong forecasting input.

Watchlist
:   A few team-level queries whose healthy answer is zero (stale work, Resolved but not closed, work left in past sprints and so on), reviewed weekly to catch bad data before it reaches an executive ([Lab 11](../day-3/lab-11-dashboard-wrong.md)).

Watermelon status
:   Green on the outside, red on the inside: a report that says "on track" while the data says otherwise ([Lab 4](../day-1/lab-04-sprint-delivery-report.md)).

WIP (work in progress)
:   Items started but not finished. Too much WIP slows everything down, at story level and at Feature level.

WSJF
:   **Weighted Shortest Job First.** A prioritization score: cost of delay (business value + time criticality + risk reduction) ÷ job size. Azure DevOps has no WSJF field; Lab 10's "WSJF-lite" uses a Feature's (**Business Value** + **Time Criticality**) ÷ **Effort** ([Lab 10](../day-3/lab-10-personas.md)).

## Course terms

Takeaway
:   The one-sentence lesson in the box that closes every Part of a lab. A lab's **Key takeaways** gather them.

One thing
:   The single sentence each lab asks you to remember, shown with its "Back in your own harbor" moves. All twelve are on [your Field Card](field-card.md).

Reef
:   A trap the data invites: a plausible but wrong conclusion. Each lab names at least one, after you've had the chance to fall in.

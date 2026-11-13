---
title: "Metrics Field Guide"
---

# Metrics Field Guide

Every metric in Azure DevOps answers a narrow question, and every one of them can be made to lie. This guide gives you, for each one, what it is, how Azure DevOps calculates it, where to find it, how to read it, how it misleads, and the questions a good manager asks before believing it.

!!! insight "Three rules before any metric"
    1. **Azure DevOps measures; you interpret.** A chart reports what was recorded, not what happened. Ask "how do we know?" before "what does it mean?"
    2. **The state category decides what counts.** Charts don't read state names. They read categories, and only **Completed** (Closed) is done.
    3. **Compare a team with its own past, never with another team.** Points are a local currency.

## How Azure DevOps decides what's "done"

Every state belongs to a **state category**. Charts, rollups and forecasts work on the category.

| State (Agile) | Category | Velocity | Rollup progress | Burndowns | CFD | Lead / cycle time |
|:--|:--|:--|:--|:--|:--|:--|
| New | Proposed | Not counted (only **Planned** if in the sprint on day 1) | Not done | Remaining | First column | Lead clock started at creation |
| Active | In Progress | **Incomplete** | Not done | Remaining | Its board column | Cycle clock starts |
| Resolved (story, Feature) | In Progress | **Incomplete** | **Not done** | Remaining | Resolved column | Clocks still running |
| Resolved (bug) | Resolved | **Excluded** entirely | Not done | Remaining, unless the Burndown/Burnup widget's **Show Resolved work items as Completed** is on | Resolved column | Clocks still running |
| Closed | Completed | **Completed** (or **Completed Late**) | **Done** | Burned down | Last column | Clocks stop |
| Removed | Removed | Excluded | Excluded | Excluded | Hidden | n/a |

<!-- VERIFY: category of the Resolved state on Agile User Story and Feature (expected In Progress) under Organization settings › Boards › Process › Agile. -->

!!! reef "Reef ahead: \"finished\" vs Closed"
    If a team's definition of done stops at **Resolved**, every chart under-reports them: velocity sags, rollups stall, and lead times stretch. Before you read any team's metrics, find out where their work actually stops.

Analytics also isn't real time. Rollups, Velocity, CFD and burndowns can lag edits by a short while; rollup columns show a "Data last refreshed" time on hover. Trend charts are built from **daily snapshots**.

## Sprint and team metrics

### Velocity

| | |
|:--|:--|
| **What it is** | The amount of work a team completed per sprint, as a sum of Story Points or a count of items |
| **How Azure DevOps computes it** | **Planned**: items in the sprint at the end of day 1 (a historical snapshot). **Completed**: Completed-category items finished by the sprint's end. **Completed Late**: finished after the end. **Incomplete**: still In Progress. Proposed and Resolved-category items are excluded. With bugs managed as requirements, bugs are included (usually with no points) |
| **Where** | **Boards › Backlogs** › team › **Analytics** tab › **Velocity** card › **View full report** (**Velocity by** points or **Count of Work Items**; up to 15 iterations). Dashboard: **Velocity** widget, one team per widget, with **Display planned work for iterations** and **Highlight work completed late** |
| **How to read it** | Look at the *trend* and the *range* over five or six sprints, and at the gap between Planned and Completed. Switch **Velocity by** between points and count: they should tell the same story |
| **How it misleads** | Points can inflate. Unestimated items add zero. Items left in Resolved don't count. Bars for past sprints depend on states being updated on time |
| **Ask** | Does velocity by *count* move with velocity by *points*? How much of the completed work served a Feature? What was added after day 1? |
| **Don't** | Compare velocity across teams. Set velocity targets. Reward "more points" |

<!-- SHOT: res-metrics-velocity-report | Boards › Backlogs › team Digital Accounts › Analytics › Velocity full report, Velocity by Sum of Story Points, Last 6 iterations, Planned / Completed / Completed Late / Incomplete bars visible | crop: chart and the two controls -->

### Planned vs completed (commitment reliability)

| | |
|:--|:--|
| **What it is** | The share of planned work a team finished in the sprint: Completed ÷ Planned |
| **How Azure DevOps computes it** | It doesn't, directly. Read both bars from the **Velocity** report (Planned comes from the day-1 snapshot) and divide |
| **Where** | Velocity report or widget with **Display planned work for iterations** on. Select a bar to open a query of those items |
| **How to read it** | Steady values in the 80s and 90s mean planning and delivery agree. A steady *decline* is the signal, more than any single sprint |
| **How it misleads** | Teams can score 100% by planning less. Mid-sprint additions don't appear in Planned, so a team absorbing urgent work looks unreliable |
| **Ask** | What's carrying over, and how often has the same item carried? What came in mid-sprint, and who asked for it? |
| **Don't** | Treat it as a performance score. Punish honest planning |

### Sprint burndown

| | |
|:--|:--|
| **What it is** | Work remaining in one sprint, day by day, against an ideal line |
| **How Azure DevOps computes it** | Remaining = items not in the Completed category. **Burndown on** a count or a sum (Story Points). The **Ideal Trend** uses the team's working days and days off. **Total Scope** rises when work is added |
| **Where** | **Boards › Sprints** › team › sprint › **Analytics** tab (**Burndown Trend**). Dashboard: **Sprint Burndown** widget (**Select Iteration**: `@CurrentIteration` or a specific sprint) |
| **How to read it** | A staircase is normal. A flat line followed by a cliff means items close in batches at the end. A rising scope line means the sprint was re-planned on the fly |
| **How it misleads** | Items parked in Resolved never burn. A widget pointed at a fixed sprint goes stale when the sprint changes |
| **Ask** | Is the line flat because nothing finished, or because nobody updated states? What raised the scope? |
| **Don't** | Manage the line day by day. Read it at Feature level instead of hours. This course doesn't use Remaining Work |

## Flow metrics

### Throughput

| | |
|:--|:--|
| **What it is** | The **number** of items finished per period |
| **How Azure DevOps computes it** | Velocity with **Velocity by** = **Count of Work Items**, or a query of items Closed in a date range |
| **Where** | Velocity report (count), or [Query Cookbook C4](query-cookbook.md#c4) as a chart |
| **How to read it** | Stable throughput is the best forecasting input you have. It can't be inflated by re-estimating |
| **How it misleads** | Items differ in size. Splitting work raises throughput without delivering more |
| **Ask** | Did throughput change, or did item size change? |
| **Don't** | Compare throughput across teams with different kinds of work |

### Lead time

| | |
|:--|:--|
| **What it is** | Elapsed days from **creation** to **Completed**: the member's view of how long things take |
| **How Azure DevOps computes it** | Created Date to entering the Completed category. Reopened items count from creation to their *last* completion. Only items completed in the chart period are plotted |
| **Where** | Dashboard **Lead Time** widget (team, backlog or work item type, rolling period). There's no in-context report |
| **How to read it** | Dots are completed items; the line is the moving average; the shaded band is the spread. Quote it as a range |
| **How it misleads** | Old ideas that sat in the backlog for months make lead time look terrible, even when delivery is fast |
| **Ask** | How much of the lead time is waiting before work starts? |
| **Don't** | Quote the average alone. Use average ± spread |

### Cycle time

| | |
|:--|:--|
| **What it is** | Elapsed days from **starting** work to **Completed**: the team's view |
| **How Azure DevOps computes it** | From the *first* entry into an In Progress or Resolved state to the *last* entry into Completed. Time in Resolved counts, so a test queue shows up here |
| **Where** | Dashboard **Cycle Time** widget. Analytics views expose *Cycle Time Days* |
| **How to read it** | A rising average or a widening band means work is waiting somewhere between start and done. Outliers are retrospective topics |
| **How it misleads** | Items moved straight from New to Closed have almost no cycle time. Late state updates distort it both ways |
| **Ask** | Where in the flow do items wait? Which column grows? |
| **Don't** | Push people to "work faster". Cycle time falls when you start less and finish more |

<!-- SHOT: res-metrics-cycle-time | Dashboard Cycle Time widget configured for team Core Platform, Stories backlog, rolling 60 days; dots, moving average line and standard deviation band visible | crop: widget only -->

### Work in progress (WIP)

| | |
|:--|:--|
| **What it is** | How many items are started but not finished, right now |
| **How Azure DevOps computes it** | Items in In Progress and Resolved categories. The CFD reports "Average work in progress" (completed items excluded). Board columns can carry WIP limits |
| **Where** | **Analytics** tab › **Cumulative Flow Diagram** card; the board; a query of `State In Active,Resolved` |
| **How to read it** | At Feature level: how many Features is one team pushing at once? At story level: how many items per person? |
| **How it misleads** | Items nobody touches still count, so WIP can look busy when nothing moves |
| **Ask** | What would we stop starting so we can finish? |
| **Don't** | Read high WIP as high productivity |

### Cumulative Flow Diagram (CFD)

| | |
|:--|:--|
| **What it is** | Stacked bands of how many items sat in each board column, day by day |
| **How Azure DevOps computes it** | Daily snapshots of items per **board column** (not state), for one team and backlog level |
| **Where** | **Boards › Backlogs** › team › **Analytics** › **Cumulative Flow Diagram** › **View full report** (rolling period 14 to 180 days). Dashboard: **Cumulative Flow Diagram (CFD)** widget |
| **How to read it** | Band **thickness** is WIP in that column. Horizontal distance is roughly time in process. A band that keeps widening is a bottleneck. Flat lines mean nothing moved, or nobody updated it |
| **How it misleads** | Columns are team-specific, so two teams' CFDs aren't comparable. It shows no lead or cycle time numbers |
| **Ask** | Which band is widening, and who works that column? |
| **Don't** | Use it alone. Pair it with Cycle Time to quantify what you see |

## Portfolio and quality metrics

### Feature progress rollups

| | |
|:--|:--|
| **What it is** | A progress bar or total on each Feature or Epic, rolled up from its descendants |
| **How Azure DevOps computes it** | Through Parent/Child links only. Progress counts only **Completed** (Closed) descendants. **Progress by all Work Items** counts items; **Progress by Story Points** sums points. Rollup ignores your filters and lags Analytics slightly |
| **Where** | Backlog **Column Options** › **+ Add a rollup column** (quick list or **Configure custom rollup**). Delivery Plan cards with **Show child rollup data** |
| **How to read it** | Read percentage *and* remaining points next to the Target Date. "70% done" means little until you know what's left and how long remains |
| **How it misleads** | Unestimated children add nothing to points progress. A Feature with no children shows nothing at all. Resolved children count as not done. Count and points can disagree sharply |
| **Ask** | Is everything decomposed and estimated? What's left, in points, versus the team's real pace? |
| **Don't** | Report a percentage without the remaining work and the date beside it |

### Burnup (release level)

| | |
|:--|:--|
| **What it is** | Completed work rising toward a total scope line, across one or more teams and several sprints |
| **How Azure DevOps computes it** | **Burnup** widget: teams (multi-select), a backlog or work item type, optional **Field criteria** (historical: evaluated at each point in time), count or sum, start and end dates, plotted by date or **Iteration**. Options include **Show total scope** and **Show Resolved work items as Completed**, plus a projected completion |
| **Where** | Dashboard **Burnup** widget (its twin is **Burndown**) |
| **How to read it** | The gap between the completed line and the scope line is the work left. A rising scope line explains most "why are we still not done?" questions |
| **How it misleads** | Field criteria and tags are historical, so items tagged after the start date show up as scope increase on the day they were tagged. **Show Resolved as Completed** flatters progress |
| **Ask** | How much did scope grow, and who agreed to it? |
| **Don't** | Trust the projection line without checking that scope is stable |

### Defect trend

| | |
|:--|:--|
| **What it is** | Open bugs over time, by state, severity or team |
| **How Azure DevOps computes it** | A trend chart (**Stacked area**, **Line** or **Area**) on a flat bug query, over a rolling period. Trend charts come from the work-tracking store, not Analytics |
| **Where** | **Boards › Queries** › bug query › **Charts** › **New chart**; on a dashboard, **Chart for Work Items**. See [Query Cookbook E1 and E3](query-cookbook.md#e1) |
| **How to read it** | Arrival rate versus closure rate. A line that rises sprint after sprint is quality debt compounding |
| **How it misleads** | Bugs filed in the wrong area escape a team-scoped query. Bugs closed without a fix flatter the trend |
| **Ask** | How many are escaped defects? Is capacity reserved for fixing bugs? |
| **Don't** | Reward a low bug count. Teams stop filing bugs |

## Forecasting

### Forecast ranges

| | |
|:--|:--|
| **What it is** | An honest "when" or "how much", stated as a range with assumptions |
| **How Azure DevOps computes it** | The backlog **Forecasting** tool walks the Stories backlog in order, filling each future sprint with the velocity you type, and carries unused velocity forward. It ignores items in progress and ignores iteration assignments. It lives on the Stories level only, and is disabled while **Parents** is on or a filter is active |
| **Where** | **Boards › Backlogs** › team › **Stories** › **View options**: Parents Off, In Progress Items Off, Completed Child Items Off, **Forecasting** On. Type the velocity in the banner |
| **How to read it** | Run it **twice**: once at the low end of recent velocity and once at the high end. The answer is the range between the two lines. Adjust velocity for known capacity changes (days off, people out, mandatory work) first |
| **How it misleads** | Unestimated stories count as zero points, so they look free. It assumes the team works only on this backlog. One velocity number looks precise and isn't |
| **Ask** | Which assumptions would change the answer? What's the date at the pessimistic end? What could we cut to make the date? |
| **Don't** | Give a single date. Forecast from another team's velocity |

<!-- VERIFY: whether the Forecasting velocity value and toggle are saved per user or per team. -->

## Two laws every manager should know

!!! insight "Goodhart's law"
    *"When a measure becomes a target, it ceases to be a good measure."* Set a velocity target and points inflate. Reward low bug counts and bugs stop being filed. Score teams on commitment reliability and they plan less. Use metrics to ask better questions, not to grade people.

!!! insight "Little's Law, intuitively"
    **Average time in process ≈ work in progress ÷ throughput.** If a team has 12 items in progress and finishes about 4 a week, a new item waits about three weeks. To deliver faster you can finish more (hard) or start less (easy). Cutting WIP is the cheapest speed-up a manager can order.

## Signal combinations

One metric is a rumor. Two that disagree are a lead.

| You see… | …together with | It probably means | Check next |
|:--|:--|:--|:--|
| Velocity rising | Throughput (count) flat | **Point inflation**: same output, bigger estimates | Average points per item, sprint by sprint |
| High velocity | Features barely moving in rollups | Effort is going to **orphan** or off-priority work | Completed items by Parent ([F4](query-cookbook.md#f4)) |
| Lead time rising | Cycle time steady | Work **waits longer before it starts**: the queue, not the team, is slow | Backlog size and age; WIP limits on intake |
| Commitment reliability falling | Planned rising every sprint | **Over-commitment**; carry-over compounding | Carry-over items and their History |
| Cycle time rising | One CFD band widening | A **bottleneck** in that stage, often testing or review | Who works that column; WIP in it |
| Burndown flat, then a cliff | Normal velocity | **Batching**: items closed in bulk at sprint end | Closed Dates within the sprint |
| Open bugs rising | Velocity steady | **Quality debt**: speed borrowed from the future | Escaped defects ([E3](query-cookbook.md#e3)) and capacity for fixes |
| Burnup scope rising | Completed line steady | **Scope creep**, not slow delivery | What was added, by whom, when |
| Feature at a high % | Target Date passed | Finished but **not closed**, or the last items are the hard ones | Remaining children and their states |
| Rollup 0% | Children are Active or Resolved | **Nothing closed yet**, not "nothing done" | Child states |
| Low throughput | Steady velocity and reliability | **Bigger items**, often a healthy, predictable team | Item size; don't "fix" what isn't broken |

## Which metric answers which question?

| The question you were asked | Start with | Then check |
|:--|:--|:--|
| "Will this Feature make its date?" | Rollup progress + remaining points vs Target Date | Velocity range, dependencies, unestimated children |
| "Is this team in trouble?" | Velocity trend by points **and** count | Commitment reliability, CFD, cycle time, open bugs |
| "Why is everything taking so long?" | Cycle time | CFD bands, WIP |
| "What did we deliver?" | Features Closed; stories Closed by parent | Orphan share |
| "How much can we take on next PI?" | Velocity range × sprints, adjusted for capacity | Mandatory work, days off, unestimated backlog |
| "Is quality getting worse?" | Defect trend | Escaped defects, reopened bugs |

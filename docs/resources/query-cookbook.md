---
title: "Query Cookbook"
---

# Query Cookbook

Thirty ready-to-use queries for managers, written at Feature and portfolio altitude. Each recipe gives you the question it answers, the query type, the clauses, and how to use the result. Power users get the WIQL in a collapsed block.

!!! tip "How to use this page"
    1. **Boards › Queries** › **All** › **New query**, then build the clauses from the table. Or open an existing shared query and use **More actions** (…) › **Save as**.
    2. Save into `Shared Queries/Training/P##/`. Only shared queries can feed dashboard widgets.
    3. Swap in your own team and area. Examples use `Mobile Banking` and `HarborPoint\Digital`; any team works.
    4. Only **Flat list of work items** queries can be charted. Tree and direct-links queries go on a dashboard through the **Query Results** widget.

In the clause tables, **(blank)** means leave **Value** empty, and `@CurrentIteration [Mobile Banking]` means the macro with the team parameter set to that team.

## Recipe index

| # | Query | Answers | Type |
|:--|:--|:--|:--|
| [A1](#a1) | Portfolio roll-call | What makes up the portfolio? | Tree |
| [A2](#a2) | Feature portfolio status | Where does every Feature stand? | Flat · chart |
| [A3](#a3) | Open Features by value | Are we working on the most valuable things? | Flat |
| [A4](#a4) | A PI's Features | What's planned for a PI? | Flat · chart |
| [A5](#a5) | Features with no stories | Which Features aren't broken down yet? | Direct links |
| [A6](#a6) | Unsized or undated Features | Which Features can't be planned? | Flat |
| [B1](#b1) | This sprint, by Feature | What is a team working on now? | Flat · chart |
| [B2](#b2) | Sliding sprint window | Last, current and next sprint at once | Flat |
| [B3](#b3) | Blocked work | What is waiting on someone else? | Flat · tile |
| [B4](#b4) | Unplanned work this sprint | What arrived after planning? | Flat · tile |
| [B5](#b5) | Who's carrying what | Is the load spread sensibly? | Flat · pivot |
| [C1](#c1) | Finished last sprint | Which Features actually moved? | Flat |
| [C2](#c2) | What a PI delivered | How did the last PI end? | Flat · chart |
| [C3](#c3) | Features closed late | How often do we miss targets? | Flat |
| [C4](#c4) | Last month's throughput | How many items did we finish? | Flat · chart |
| [D1](#d1) | Due soon, not done | What's about to be late? | Flat · tile |
| [D2](#d2) | Self-reported or high risk | What do teams say is at risk? | Flat |
| [D3](#d3) | Cross-team dependencies | Who does a team wait on, and who waits on it? | Direct links |
| [D4](#d4) | Every open dependency | All predecessor links in the program | Direct links |
| [D5](#d5) | Overdue Features | What has already passed its target? | Flat · tile |
| [E1](#e1) | Open bugs by severity | How much quality debt, and where? | Flat · chart |
| [E2](#e2) | Urgent bugs with no owner | Who is fixing the worst bugs? | Flat · tile |
| [E3](#e3) | Escaped defects trend | Is production quality improving? | Flat · trend |
| [E4](#e4) | Reopened bugs | Are fixes sticking? | Flat |
| [F1](#f1) | Stale active work | What hasn't moved in two weeks? | Flat · tile |
| [F2](#f2) | Resolved but not closed | What's finished but not counted? | Flat · tile |
| [F3](#f3) | Unestimated stories | What will forecasting treat as free? | Flat |
| [F4](#f4) | Orphan stories | What work serves no Feature? | Direct links |
| [F5](#f5) | Unfinished work in past sprints | What was left behind? | Flat |
| [F6](#f6) | Work at the root area | What belongs to no team? | Flat |
| [G1](#g1) | My radar | What should I be watching? | Flat |

<!-- SHOT: res-cookbook-editor | Boards › Queries › New query, Editor tab, Flat list of work items, clauses from recipe A2 (Work Item Type = Feature, State <> Removed, Area Path Under HarborPoint) | crop: query type dropdown and clause grid -->

## A · Portfolio and Features

### A1 · Portfolio roll-call {#a1}

*Which Epics and Features make up the portfolio, and what sits under each?*

**Type:** Tree of work items · **Type of tree:** Parent/Child · **Match top-level work items first**

Filters for top-level work items:

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | = | `Epic` |
| And | State | <> | `Removed` |

Filters for linked work items:

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | In | `Feature,User Story` |
| And | State | <> | `Removed` |

**Use it:** a **Query Results** widget on a program dashboard, or the backbone of a portfolio review. The linked filter applies at every level, so it must list both `Feature` and `User Story`. Collapse to Features for an executive walk-through.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.WorkItemType], [System.Title], [System.State],
           [System.AreaPath], [Microsoft.VSTS.Scheduling.TargetDate]
    FROM WorkItemLinks
    WHERE ([Source].[System.WorkItemType] = 'Epic'
           AND [Source].[System.State] <> 'Removed')
      AND ([System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Forward')
      AND ([Target].[System.WorkItemType] IN ('Feature', 'User Story')
           AND [Target].[System.State] <> 'Removed')
    MODE (Recursive)
    ```

### A2 · Feature portfolio status {#a2}

*Where does every Feature stand, by team and state?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | = | `Feature` |
| And | State | <> | `Removed` |
| And | Area Path | Under | `HarborPoint` |

**Columns:** Title, State, Assigned To, **Node Name**, Target Date, Effort, Tags.
**Use it:** charts. **Pie** by State; **Stacked bar** of Node Name × State; **Pivot table** of Node Name × State with **Sum** of Effort. Group by **Node Name**, not Area Path, so each team gets its own bar.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Title], [System.State], [System.AssignedTo],
           [System.NodeName], [Microsoft.VSTS.Scheduling.TargetDate],
           [Microsoft.VSTS.Scheduling.Effort], [System.Tags]
    FROM WorkItems
    WHERE [System.WorkItemType] = 'Feature'
      AND [System.State] <> 'Removed'
      AND [System.AreaPath] UNDER 'HarborPoint'
    ORDER BY [Microsoft.VSTS.Scheduling.TargetDate]
    ```

### A3 · Open Features by value {#a3}

*Are the most valuable, most time-critical Features the ones getting attention?*

**Type:** Flat list of work items · **Sorting:** Business Value descending, then Time Criticality descending

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | = | `Feature` |
| And | State | Not In | `Closed,Removed` |

**Columns:** Title, Node Name, State, Business Value, Time Criticality, Effort, Risk, Priority, Target Date.
**Use it:** a prioritization conversation. Put it next to the Features backlog order and ask why the two lists differ. Add a rollup column on the backlog to see which high-value Features are moving.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Title], [System.NodeName], [System.State],
           [Microsoft.VSTS.Common.BusinessValue], [Microsoft.VSTS.Common.TimeCriticality],
           [Microsoft.VSTS.Scheduling.Effort], [Microsoft.VSTS.Common.Risk],
           [Microsoft.VSTS.Common.Priority], [Microsoft.VSTS.Scheduling.TargetDate]
    FROM WorkItems
    WHERE [System.WorkItemType] = 'Feature'
      AND [System.State] NOT IN ('Closed', 'Removed')
    ORDER BY [Microsoft.VSTS.Common.BusinessValue] DESC,
             [Microsoft.VSTS.Common.TimeCriticality] DESC
    ```

### A4 · A PI's Features {#a4}

*What is planned for the next PI?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | = | `Feature` |
| And | Iteration Path | Under | `HarborPoint\PI 5` |
| And | State | <> | `Removed` |

**Use it:** PI planning and outlook work. Chart **Pie** by Node Name, or **Pivot** Node Name × State with Sum of Effort. Variant: replace the Iteration Path clause with `Tags` `Contains` `PI5-Candidate` and compare the two lists. Any difference is a conversation.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Title], [System.NodeName], [System.State],
           [Microsoft.VSTS.Scheduling.Effort], [Microsoft.VSTS.Scheduling.TargetDate], [System.Tags]
    FROM WorkItems
    WHERE [System.WorkItemType] = 'Feature'
      AND [System.IterationPath] UNDER 'HarborPoint\PI 5'
      AND [System.State] <> 'Removed'
    ```

### A5 · Features with no stories {#a5}

*Which open Features haven't been broken down into work yet?*

**Type:** Work items and direct links · **Return selected link types:** Child · **Only return items that do not have matching links**

Filters for top-level work items:

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | = | `Feature` |
| And | State | Not In | `Closed,Removed` |

Filters for linked work items:

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | In | `User Story,Bug` |

**Use it:** before PI planning. A Feature with no children can't be forecast, rolled up or tracked. It's an idea with a date on it.

<!-- VERIFY: exact option wording "Only return items that do not have matching links" (Learn shows "don't") and the link-type checklist labels in New Boards Hub. -->

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Title], [System.State], [System.AreaPath]
    FROM WorkItemLinks
    WHERE ([Source].[System.WorkItemType] = 'Feature'
           AND [Source].[System.State] NOT IN ('Closed', 'Removed'))
      AND ([System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Forward')
      AND ([Target].[System.WorkItemType] IN ('User Story', 'Bug'))
    MODE (DoesNotContain)
    ```

### A6 · Unsized or undated Features {#a6}

*Which Features can't be planned because they lack a size or a date?*

**Type:** Flat list of work items

| Group | And/Or | Field | Operator | Value |
|:-:|:--|:--|:--|:--|
| | | Work Item Type | = | `Feature` |
| | And | State | Not In | `Closed,Removed` |
| ┌ | And | Effort | = | (blank) |
| │ | Or | Start Date | = | (blank) |
| └ | Or | Target Date | = | (blank) |

**Use it:** a Feature "definition of ready" check. Group the three Or clauses, or the query returns every Feature with no Target Date regardless of state.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Title], [System.NodeName], [System.State],
           [Microsoft.VSTS.Scheduling.Effort], [Microsoft.VSTS.Scheduling.StartDate],
           [Microsoft.VSTS.Scheduling.TargetDate]
    FROM WorkItems
    WHERE [System.WorkItemType] = 'Feature'
      AND [System.State] NOT IN ('Closed', 'Removed')
      AND ([Microsoft.VSTS.Scheduling.Effort] = ''
           OR [Microsoft.VSTS.Scheduling.StartDate] = ''
           OR [Microsoft.VSTS.Scheduling.TargetDate] = '')
    ```

## B · Current work

### B1 · This sprint, by Feature {#b1}

*What is one team working on right now, and which Features does it serve?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | In | `User Story,Bug` |
| And | Iteration Path | = | `@CurrentIteration [Mobile Banking]` |

**Columns:** **Parent**, Title, State, Assigned To, Story Points, Tags. The Parent column shows each item's Feature (blank means no Feature).
**Use it:** a weekly readout. Chart **Pie** by State with **Sum** of Story Points. For a hierarchy, build the same filter as a **Tree of work items** with `Feature` on top and these clauses in the linked filters; it reads well in a **Query Results** widget but can't be charted.

<!-- VERIFY: where the @CurrentIteration team parameter box sits in the New Boards Hub editor, and whether charts can group by Parent. -->

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Parent], [System.Title], [System.State],
           [System.AssignedTo], [Microsoft.VSTS.Scheduling.StoryPoints], [System.Tags]
    FROM WorkItems
    WHERE [System.WorkItemType] IN ('User Story', 'Bug')
      AND [System.IterationPath] = @CurrentIteration('[HarborPoint]\Mobile Banking <id:…>')
    ```
    The editor writes the team's id for you. Copy the WIQL from a saved query rather than typing the id.

### B2 · Sliding sprint window {#b2}

*What did a team finish last sprint, what's in flight now, and what's lined up next?*

**Type:** Flat list of work items

| Group | And/Or | Field | Operator | Value |
|:-:|:--|:--|:--|:--|
| | | Work Item Type | In | `User Story,Bug` |
| ┌ | And | Iteration Path | = | `@CurrentIteration - 1 [Mobile Banking]` |
| │ | Or | Iteration Path | = | `@CurrentIteration [Mobile Banking]` |
| └ | Or | Iteration Path | = | `@CurrentIteration + 1 [Mobile Banking]` |

**Columns:** Iteration Path, Parent, Title, State, Story Points.
**Use it:** a stand-up or Monday review that never needs editing: it rolls forward on its own when the sprint changes. Chart a **Stacked bar** of Iteration Path × State: the chart shows only the leaf, which here is exactly the sprint name you want.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.IterationPath], [System.Parent], [System.Title],
           [System.State], [Microsoft.VSTS.Scheduling.StoryPoints]
    FROM WorkItems
    WHERE [System.WorkItemType] IN ('User Story', 'Bug')
      AND ([System.IterationPath] = @CurrentIteration('[HarborPoint]\Mobile Banking <id:…>') - 1
           OR [System.IterationPath] = @CurrentIteration('[HarborPoint]\Mobile Banking <id:…>')
           OR [System.IterationPath] = @CurrentIteration('[HarborPoint]\Mobile Banking <id:…>') + 1)
    ```

### B3 · Blocked work {#b3}

*What across the program is waiting on someone else?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | In | `User Story,Bug` |
| And | Tags | Contains | `blocked` |
| And | State | Not In | `Closed,Removed` |

**Columns:** Node Name, Parent, Title, Assigned To, Iteration Path.
**Use it:** a **Query Tile** that turns red at 1 or more. Then open each item's **Discussion**: the tag says *that* it's blocked, the comment says *by whom*.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.NodeName], [System.Parent], [System.Title],
           [System.AssignedTo], [System.IterationPath]
    FROM WorkItems
    WHERE [System.WorkItemType] IN ('User Story', 'Bug')
      AND [System.Tags] CONTAINS 'blocked'
      AND [System.State] NOT IN ('Closed', 'Removed')
    ```

### B4 · Unplanned work this sprint {#b4}

*What entered a team's sprint after planning?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | In | `User Story,Bug` |
| And | Iteration Path | = | `@CurrentIteration [Mobile Banking]` |
| And | Tags | Contains | `unplanned` |

**Columns:** Title, Parent, Story Points, Created Date, Assigned To.
**Use it:** a tile next to the sprint burndown. Unplanned work with no parent Feature is double trouble: it consumes capacity *and* serves no priority. The tag works only if teams use it; the Velocity report's **Planned** bar is the tag-free check.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Title], [System.Parent],
           [Microsoft.VSTS.Scheduling.StoryPoints], [System.CreatedDate], [System.AssignedTo]
    FROM WorkItems
    WHERE [System.WorkItemType] IN ('User Story', 'Bug')
      AND [System.IterationPath] = @CurrentIteration('[HarborPoint]\Mobile Banking <id:…>')
      AND [System.Tags] CONTAINS 'unplanned'
    ```

### B5 · Who's carrying what {#b5}

*Is active work spread sensibly, or is someone juggling too much?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | In | `User Story,Bug` |
| And | State | = | `Active` |
| And | Area Path | Under | `HarborPoint\Digital` |

**Columns:** Assigned To, Work Item Type, Parent, Title, Changed Date.
**Use it:** **Pivot table** with Assigned To as rows and Work Item Type as columns (count). Look for people with many active items across several parents: that's context switching. Ask about it, don't assign blame.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.AssignedTo], [System.WorkItemType], [System.Parent],
           [System.Title], [System.ChangedDate]
    FROM WorkItems
    WHERE [System.WorkItemType] IN ('User Story', 'Bug')
      AND [System.State] = 'Active'
      AND [System.AreaPath] UNDER 'HarborPoint\Digital'
    ORDER BY [System.AssignedTo]
    ```

## C · Delivery and completion

### C1 · Finished last sprint {#c1}

*What did a team actually finish last sprint, and which Features moved?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | In | `User Story,Bug` |
| And | State | = | `Closed` |
| And | Iteration Path | = | `@CurrentIteration - 1 [Mobile Banking]` |

**Columns:** Parent, Title, Story Points, Closed Date.
**Use it:** the "delivered" line of a status report. Read it through the Parent column: points finished on items with no parent didn't move any Feature. Items that carried over don't appear here; use the **Velocity** report and each item's **History** for that.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Parent], [System.Title],
           [Microsoft.VSTS.Scheduling.StoryPoints], [Microsoft.VSTS.Common.ClosedDate]
    FROM WorkItems
    WHERE [System.WorkItemType] IN ('User Story', 'Bug')
      AND [System.State] = 'Closed'
      AND [System.IterationPath] = @CurrentIteration('[HarborPoint]\Mobile Banking <id:…>') - 1
    ```

### C2 · What a PI delivered {#c2}

*How did the last PI end, across Features and stories?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | In | `Feature,User Story` |
| And | Iteration Path | Under | `HarborPoint\PI 3` |
| And | State | <> | `Removed` |

**Use it:** a **Stacked bar** of Work Item Type × State, or a **Pivot** of Node Name × State. `Under` catches the PI node (where Features sit) *and* its sprints (where stories sit).

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.WorkItemType], [System.Title], [System.State], [System.NodeName]
    FROM WorkItems
    WHERE [System.WorkItemType] IN ('Feature', 'User Story')
      AND [System.IterationPath] UNDER 'HarborPoint\PI 3'
      AND [System.State] <> 'Removed'
    ```

### C3 · Features closed late {#c3}

*How often do Features close after their Target Date?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | = | `Feature` |
| And | State | = | `Closed` |
| And | Closed Date | > [Field] | `Target Date` |

**Use it:** a field-to-field comparison. Pick the operator `> [Field]` and the Value list shows only date fields. A Feature closed weeks after its work finished also shows up here, so check its children before calling it late.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Title], [System.NodeName],
           [Microsoft.VSTS.Scheduling.TargetDate], [Microsoft.VSTS.Common.ClosedDate]
    FROM WorkItems
    WHERE [System.WorkItemType] = 'Feature'
      AND [System.State] = 'Closed'
      AND [Microsoft.VSTS.Common.ClosedDate] > [Microsoft.VSTS.Scheduling.TargetDate]
    ```

### C4 · Last month's throughput {#c4}

*How many stories and bugs did a team finish last calendar month?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | In | `User Story,Bug` |
| And | State | = | `Closed` |
| And | Area Path | Under | `HarborPoint\Digital\Digital Accounts` |
| And | Closed Date | >= | `@StartOfMonth - 1` |
| And | Closed Date | < | `@StartOfMonth` |

**Use it:** a **Column** chart by Work Item Type. Throughput is a count, not points, so it can't be inflated by re-estimating. Compare a team with its own past, never with another team.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.WorkItemType], [System.Title], [Microsoft.VSTS.Common.ClosedDate]
    FROM WorkItems
    WHERE [System.WorkItemType] IN ('User Story', 'Bug')
      AND [System.State] = 'Closed'
      AND [System.AreaPath] UNDER 'HarborPoint\Digital\Digital Accounts'
      AND [Microsoft.VSTS.Common.ClosedDate] >= @StartOfMonth - 1
      AND [Microsoft.VSTS.Common.ClosedDate] < @StartOfMonth
    ```

## D · Risk and dependencies

### D1 · Due soon, not done {#d1}

*Which Features are due in the next two weeks, or already past due, and still open?*

**Type:** Flat list of work items · **Sorting:** Target Date ascending

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | = | `Feature` |
| And | State | Not In | `Closed,Removed` |
| And | Target Date | <= | `@Today + 14` |

**Columns:** Title, Node Name, State, Target Date, Risk, Tags.
**Use it:** a **Query Tile** and a **Query Results** widget. A Feature on this list isn't automatically in trouble; one that's nearly done is fine. Check its rollup before you escalate.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Title], [System.NodeName], [System.State],
           [Microsoft.VSTS.Scheduling.TargetDate], [Microsoft.VSTS.Common.Risk], [System.Tags]
    FROM WorkItems
    WHERE [System.WorkItemType] = 'Feature'
      AND [System.State] NOT IN ('Closed', 'Removed')
      AND [Microsoft.VSTS.Scheduling.TargetDate] <= @Today + 14
    ORDER BY [Microsoft.VSTS.Scheduling.TargetDate]
    ```

### D2 · Self-reported or high risk {#d2}

*Which open Features do teams themselves flag as risky?*

**Type:** Flat list of work items

| Group | And/Or | Field | Operator | Value |
|:-:|:--|:--|:--|:--|
| | | Work Item Type | = | `Feature` |
| | And | State | Not In | `Closed,Removed` |
| ┌ | And | Risk | = | `1 - High` |
| └ | Or | Tags | Contains | `at-risk` |

**Use it:** a starting point, not a verdict. It shows what teams *say*. Combine it with D1 and the rollups to find what the data says, and look hardest at Features that should be on this list but aren't.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Title], [System.NodeName], [System.State],
           [Microsoft.VSTS.Common.Risk], [System.Tags], [Microsoft.VSTS.Scheduling.TargetDate]
    FROM WorkItems
    WHERE [System.WorkItemType] = 'Feature'
      AND [System.State] NOT IN ('Closed', 'Removed')
      AND ([Microsoft.VSTS.Common.Risk] = '1 - High'
           OR [System.Tags] CONTAINS 'at-risk')
    ```

### D3 · Cross-team dependencies {#d3}

*Which of a team's open items depend on, or are depended on by, another team?*

**Type:** Work items and direct links · **Return selected link types:** Predecessor, Successor · **Only return items that have matching links**

Filters for top-level work items:

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Area Path | Under | `HarborPoint\Digital\Mobile Banking` |
| And | State | Not In | `Closed,Removed` |

Filters for linked work items:

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Area Path | Not Under | `HarborPoint\Digital\Mobile Banking` |

**Columns:** Work Item Type, Title, State, Area Path, Iteration Path.
**Use it:** what a Delivery Plan can't show you. A plan draws lines only between cards on the plan, in expanded rows, with dates. This query lists every link, including ones to teams or items that aren't on any plan. Check the linked item's Iteration Path: a predecessor with no sprint is a risk with no date.

<!-- SHOT: res-cookbook-dependencies | Query D3 open in the Editor tab: Work items and direct links, the two filter grids, Predecessor and Successor ticked, "Only return items that have matching links" selected | crop: link options and both grids -->

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.WorkItemType], [System.Title], [System.State],
           [System.AreaPath], [System.IterationPath]
    FROM WorkItemLinks
    WHERE ([Source].[System.AreaPath] UNDER 'HarborPoint\Digital\Mobile Banking'
           AND [Source].[System.State] NOT IN ('Closed', 'Removed'))
      AND ([System.Links.LinkType] = 'System.LinkTypes.Dependency-Reverse'
           OR [System.Links.LinkType] = 'System.LinkTypes.Dependency-Forward')
      AND ([Target].[System.AreaPath] NOT UNDER 'HarborPoint\Digital\Mobile Banking')
    MODE (MustContain)
    ```
    `Dependency-Reverse` is **Predecessor** (the linked item must finish first); `Dependency-Forward` is **Successor**.

### D4 · Every open dependency {#d4}

*What does the whole program wait on?*

**Type:** Work items and direct links · **Return selected link types:** Predecessor · **Only return items that have matching links**

Filters for top-level work items:

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | In | `Feature,User Story` |
| And | State | Not In | `Closed,Removed` |

Filters for linked work items:

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | State | Not In | `Closed,Removed` |

**Use it:** a standing agenda item for a program sync. Each row is "this item waits on that item". Add Area Path and Iteration Path columns and read across: is the predecessor scheduled before the successor?

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.WorkItemType], [System.Title], [System.State],
           [System.AreaPath], [System.IterationPath]
    FROM WorkItemLinks
    WHERE ([Source].[System.WorkItemType] IN ('Feature', 'User Story')
           AND [Source].[System.State] NOT IN ('Closed', 'Removed'))
      AND ([System.Links.LinkType] = 'System.LinkTypes.Dependency-Reverse')
      AND ([Target].[System.State] NOT IN ('Closed', 'Removed'))
    MODE (MustContain)
    ```

### D5 · Overdue Features {#d5}

*Which open Features have already passed their Target Date?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | = | `Feature` |
| And | State | Not In | `Closed,Removed` |
| And | Target Date | < | `@Today` |

**Use it:** a **Query Tile** that should read zero. Anything here is either late or finished but never closed. Both are worth a conversation, and they need different ones.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Title], [System.NodeName], [System.State],
           [Microsoft.VSTS.Scheduling.TargetDate]
    FROM WorkItems
    WHERE [System.WorkItemType] = 'Feature'
      AND [System.State] NOT IN ('Closed', 'Removed')
      AND [Microsoft.VSTS.Scheduling.TargetDate] < @Today
    ```

## E · Quality

### E1 · Open bugs by severity {#e1}

*How much quality debt is there, and where?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | = | `Bug` |
| And | State | <> | `Closed` |
| And | Area Path | Under | `HarborPoint\Digital` |

**Columns:** Title, Node Name, Severity, Priority, State, Assigned To, Parent.
**Use it:** a **Stacked bar** of Node Name × Severity, or a **Pivot** of Severity × Priority. Severity is impact; Priority is urgency. A Severity 1 with Priority 3 deserves a question.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Title], [System.NodeName], [Microsoft.VSTS.Common.Severity],
           [Microsoft.VSTS.Common.Priority], [System.State], [System.AssignedTo], [System.Parent]
    FROM WorkItems
    WHERE [System.WorkItemType] = 'Bug'
      AND [System.State] <> 'Closed'
      AND [System.AreaPath] UNDER 'HarborPoint\Digital'
    ```

### E2 · Urgent bugs with no owner {#e2}

*Who is fixing the most urgent bugs?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | = | `Bug` |
| And | State | In | `New,Active` |
| And | Priority | <= | `2` |
| And | Assigned To | = | (blank) |

**Use it:** a **Query Tile** with a red rule at 1 or more. Leave the Area Path out on purpose: a bug filed in the wrong area is still a bug.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Title], [System.AreaPath], [Microsoft.VSTS.Common.Priority],
           [Microsoft.VSTS.Common.Severity], [System.CreatedDate]
    FROM WorkItems
    WHERE [System.WorkItemType] = 'Bug'
      AND [System.State] IN ('New', 'Active')
      AND [Microsoft.VSTS.Common.Priority] <= 2
      AND [System.AssignedTo] = ''
    ```

### E3 · Escaped defects trend {#e3}

*Are production defects piling up or clearing?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | = | `Bug` |
| And | Tags | Contains | `escaped-defect` |
| And | State | <> | `Closed` |

**Use it:** a trend chart (**Stacked area** grouped by State) over a rolling four or eight weeks. A rising open line means bugs arrive faster than they're fixed. Keep trend queries under 1,000 items.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Title], [System.State], [System.NodeName],
           [Microsoft.VSTS.Common.Severity]
    FROM WorkItems
    WHERE [System.WorkItemType] = 'Bug'
      AND [System.Tags] CONTAINS 'escaped-defect'
      AND [System.State] <> 'Closed'
    ```

### E4 · Reopened bugs {#e4}

*Are fixes sticking?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | = | `Bug` |
| And | State | Was Ever | `Resolved` |
| And | State | = | `Active` |

**Use it:** a quality conversation with a team lead. `Was Ever` scans history, so add `Changed Date >= @Today - 90` if the query is slow.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Title], [System.NodeName], [System.AssignedTo]
    FROM WorkItems
    WHERE [System.WorkItemType] = 'Bug'
      AND EVER [System.State] = 'Resolved'
      AND [System.State] = 'Active'
    ```

## F · Data hygiene

Reports are only as honest as the data under them. Run these weekly; most should return very little.

### F1 · Stale active work {#f1}

*What is "in progress" but hasn't been touched in two weeks?*

**Type:** Flat list of work items · **Sorting:** Changed Date ascending

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | In | `Feature,User Story,Bug` |
| And | State | = | `Active` |
| And | Changed Date | < | `@Today - 14` |

**Use it:** a tile. Stale items are either stuck, abandoned or quietly done. Any comment resets Changed Date, so this catches neglect, not slow work.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.WorkItemType], [System.Title], [System.NodeName],
           [System.AssignedTo], [System.ChangedDate]
    FROM WorkItems
    WHERE [System.WorkItemType] IN ('Feature', 'User Story', 'Bug')
      AND [System.State] = 'Active'
      AND [System.ChangedDate] < @Today - 14
    ORDER BY [System.ChangedDate]
    ```

### F2 · Resolved but not closed {#f2}

*What looks finished but isn't counted as done?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | In | `Feature,User Story,Bug` |
| And | State | = | `Resolved` |
| And | Resolved Date | < | `@Today - 5` |

**Use it:** a tile. Rollups and Velocity credit only **Closed** items. Items that linger in Resolved make progress look worse than it is, or hide a testing queue. Find out which before you act.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.WorkItemType], [System.Title], [System.NodeName],
           [System.AssignedTo], [Microsoft.VSTS.Common.ResolvedDate]
    FROM WorkItems
    WHERE [System.WorkItemType] IN ('Feature', 'User Story', 'Bug')
      AND [System.State] = 'Resolved'
      AND [Microsoft.VSTS.Common.ResolvedDate] < @Today - 5
    ```

### F3 · Unestimated stories {#f3}

*Which open stories have no Story Points?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | = | `User Story` |
| And | State | Not In | `Closed,Removed` |
| And | Story Points | = | (blank) |

**Columns:** Parent, Title, Node Name, Iteration Path.
**Use it:** before forecasting. The Forecasting tool counts an unestimated story as zero points, so it looks free. Velocity undercounts unestimated work that gets closed, too.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Parent], [System.Title], [System.NodeName], [System.IterationPath]
    FROM WorkItems
    WHERE [System.WorkItemType] = 'User Story'
      AND [System.State] NOT IN ('Closed', 'Removed')
      AND [Microsoft.VSTS.Scheduling.StoryPoints] = ''
    ```

### F4 · Orphan stories {#f4}

*Which stories serve no Feature?*

**Type:** Work items and direct links · **Return selected link types:** Parent · **Only return items that do not have matching links**

Filters for top-level work items:

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | = | `User Story` |
| And | State | <> | `Removed` |
| And | Area Path | Under | `HarborPoint\Digital` |

Filters for linked work items:

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | = | `Feature` |

**Use it:** an alignment check. Some orphan work is healthy (small fixes, tech debt). A growing share of points on orphans means a team is busy on things no priority asked for. The backlog's **Parents** view option groups the same items under **Unparented Stories**.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Title], [System.State], [System.NodeName], [System.IterationPath]
    FROM WorkItemLinks
    WHERE ([Source].[System.WorkItemType] = 'User Story'
           AND [Source].[System.State] <> 'Removed'
           AND [Source].[System.AreaPath] UNDER 'HarborPoint\Digital')
      AND ([System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Reverse')
      AND ([Target].[System.WorkItemType] = 'Feature')
    MODE (DoesNotContain)
    ```

### F5 · Unfinished work in past sprints {#f5}

*What was left behind in a sprint that has already ended?*

**Type:** Flat list of work items

| Group | And/Or | Field | Operator | Value |
|:-:|:--|:--|:--|:--|
| | | Work Item Type | In | `User Story,Bug` |
| | And | State | In | `New,Active,Resolved` |
| ┌ | And | Iteration Path | = | `@CurrentIteration - 1 [Mobile Banking]` |
| │ | Or | Iteration Path | = | `@CurrentIteration - 2 [Mobile Banking]` |
| └ | Or | Iteration Path | = | `@CurrentIteration - 3 [Mobile Banking]` |

**Use it:** items here are invisible on the current sprint board, yet they still count as open work everywhere else. Each one needs a decision: move it, close it, or remove it.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Title], [System.State], [System.IterationPath],
           [System.AssignedTo], [System.ChangedDate]
    FROM WorkItems
    WHERE [System.WorkItemType] IN ('User Story', 'Bug')
      AND [System.State] IN ('New', 'Active', 'Resolved')
      AND ([System.IterationPath] = @CurrentIteration('[HarborPoint]\Mobile Banking <id:…>') - 1
           OR [System.IterationPath] = @CurrentIteration('[HarborPoint]\Mobile Banking <id:…>') - 2
           OR [System.IterationPath] = @CurrentIteration('[HarborPoint]\Mobile Banking <id:…>') - 3)
    ```

### F6 · Work at the root area {#f6}

*What open work belongs to no team?*

**Type:** Flat list of work items

| And/Or | Field | Operator | Value |
|:--|:--|:--|:--|
| | Work Item Type | In | `Feature,User Story,Bug` |
| And | Area Path | = | `HarborPoint` |
| And | State | Not In | `Closed,Removed` |

**Use it:** `=` (not `Under`) finds items sitting on the root node itself. They appear on no delivery team's backlog or board, and any query scoped to a team area misses them.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.WorkItemType], [System.Title], [System.State],
           [Microsoft.VSTS.Common.Priority], [System.CreatedDate]
    FROM WorkItems
    WHERE [System.WorkItemType] IN ('Feature', 'User Story', 'Bug')
      AND [System.AreaPath] = 'HarborPoint'
      AND [System.State] NOT IN ('Closed', 'Removed')
    ```

## G · Your radar

### G1 · My radar {#g1}

*What am I following, where was I mentioned, and what did I touch recently?*

**Type:** Flat list of work items

| Group | And/Or | Field | Operator | Value |
|:-:|:--|:--|:--|:--|
| ┌ | | ID | In | `@Follows` |
| │ | Or | ID | In | `@RecentMentions` |
| └ | Or | ID | In | `@MyRecentActivity` |

**Use it:** your personal start-of-day list. Save it in **My Queries**. `@Me`-style macros show each person their own items, so a shared version works for everyone.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.WorkItemType], [System.Title], [System.State], [System.ChangedDate]
    FROM WorkItems
    WHERE ([System.Id] IN (@Follows)
           OR [System.Id] IN (@RecentMentions)
           OR [System.Id] IN (@MyRecentActivity))
    ORDER BY [System.ChangedDate] DESC
    ```

<!-- VERIFY: WIQL form of the ID macros (IN (@Follows) vs IN @Follows). -->

## Macro cheat sheet

| Macro | Use with | Example | Watch out |
|:--|:--|:--|:--|
| `@Me` | Identity fields (Assigned To, Created By…) | `Assigned To = @Me` | Means the person **viewing**. A shared dashboard shows each viewer their own items |
| `@Today ± n` | Date fields | `Target Date <= @Today + 14` | Days. Midnight today; results can shift by time zone |
| `@StartOfDay ± n` | Date fields | `Closed Date >= @StartOfDay - 7` | Days |
| `@StartOfWeek ± n` | Date fields | `Changed Date >= @StartOfWeek - 2` | Weeks. Which day starts the week depends on settings |
| `@StartOfMonth ± n` | Date fields | `Created Date >= @StartOfMonth - 3` | Months. Good for calendar-month reporting |
| `@StartOfYear ± n` | Date fields | `Target Date >= @StartOfYear` | Years |
| `@CurrentIteration` | Iteration Path (`=`) | `@CurrentIteration [Mobile Banking]` | Needs a **team parameter**. The team must have a sprint whose dates cover today. Copied queries keep the original team |
| `@CurrentIteration ± n` | Iteration Path | `@CurrentIteration - 1 [Mobile Banking]` | Sprints. The team must have enough sprints selected to cover the offset |
| `@TeamAreas` | Area Path (`=` only) | `Area Path = @TeamAreas [Security]` | Pulls in the team's areas, so the query follows the team's settings |
| `@Project` | Team Project | `Team Project = @Project` | Restricts a cross-project query to this project |
| `@Follows` | ID (`In`) | `ID In @Follows` | Items you follow |
| `@MyRecentActivity` | ID (`In`, `Not In`) | `ID In @MyRecentActivity` | Items you viewed or changed in roughly the last 30 days |
| `@RecentMentions` | ID (`In`, `Not In`) | `ID In @RecentMentions` | Items where you were @mentioned in the last 30 days |
| `@RecentProjectActivity` | ID (`In`, `Not In`) | `ID In @RecentProjectActivity` | Recently created or changed items in the project, capped at 5,000 |

!!! warning "Web-only macros"
    `@CurrentIteration`, `@TeamAreas`, `@Follows`, `@MyRecentActivity`, `@RecentMentions` and `@RecentProjectActivity` work only in the web portal. They don't work in notification filters, Excel, Visual Studio, or REST and CLI calls, which may silently return nothing.

## Operators by field type

| Field type | Examples | Operators |
|:--|:--|:--|
| **String / picklist** | State, Work Item Type, Risk, Severity, Tags, Value Area | `=`, `<>`, `In`, `Not In`, `Contains`, `Does Not Contain`, `In Group`, `Not In Group`, `Was Ever`, field-to-field (not Tags) |
| **Number** | Priority, Story Points, Effort, Business Value, ID | `=`, `<>`, `>`, `<`, `>=`, `<=`, `In`, `Not In`, field-to-field |
| **Date** | Target Date, Closed Date, Changed Date, Created Date | `=`, `<>`, `>`, `<`, `>=`, `<=`, `In`, `Not In`, field-to-field |
| **Identity** | Assigned To, Created By, Closed By | comparison set, `Contains`, `In`, `In Group`, `Was Ever` (with `@Me`) |
| **Tree path** | Area Path, Iteration Path | `=`, `<>`, `In`, `Not In`, `Under`, `Not Under`. **No `Was Ever`** |
| **Long text** | Title (words), Description, Acceptance Criteria, History | `Contains Words`, `Does Not Contain Words`; `Is Empty` and `Is Not Empty` on rich-text fields only |

Three habits that save time:

- **"Has no value"** on non-text fields is `=` with a blank Value (`Assigned To =`, `Story Points =`). `Is Empty` works only on rich-text fields.
- **Group your Or clauses.** An ungrouped `Or` applies to everything above it, and the query returns far more than you meant.
- **Prefer macros to typed values.** A hard-coded sprint name or date is right today and quietly wrong next sprint. Typed dates also depend on your locale.

!!! reef "Reef ahead: \"open\" isn't one clause"
    `State <> Closed` also returns **Removed** items, and **Resolved** items count as open too. Decide what "open" means for the question, then say it explicitly: `State Not In Closed,Removed`, or `State In New,Active`.

## What charts can and can't do

| Limitation | What it means | Workaround |
|:--|:--|:--|
| Flat queries only | Tree and direct-links queries have no chart | Use a flat query, or show the tree in a **Query Results** widget |
| Shared queries only on dashboards | Charts on **My Queries** have no **Add to dashboard** and only you see them | Save into `Shared Queries/Training/P##/` first |
| Save before charting | The **Charts** tab needs a saved query | Save, then **Charts** › **New chart** |
| Group by lists only fields in the query | A field must be in the clauses or **Column options** | Add it as a column and save |
| No grouping by ID, Title, dates, rich text or Tags on the Queries page | Tags work only in the dashboard **Chart for Work Items** widget | Use that widget, or one query per tag |
| Area and Iteration Path show only the leaf | Two "Sprint 14" nodes merge into one bar | Group by **Node Name** |
| 8 series (12 on a resized widget) | Extra values roll up into *(other)* | Narrow the query or pick a field with fewer values |
| Trend charts: up to 1,000 items | Bigger queries make the widget fail | Tighten the filter |
| Basic access required | Stakeholders don't see the **Charts** tab | Stakeholders can still view charts on dashboards |
| Viewers need Read on the query | Otherwise the widget shows *Widget failed to load* | Keep dashboard queries in a folder everyone can read |

<!-- VERIFY: whether "Group by Tags" in the Chart for Work Items widget is generally available or still behind the preview toggle "Enable group by tags for work item chart widget on dashboard". -->

!!! insight "Lighthouse insight"
    A query is a **question you can re-ask** for free. Save the questions you get asked every week, name them as questions (`Features due in 14 days`), and put them where your stakeholders can run them. The best status report is one nobody has to compile.

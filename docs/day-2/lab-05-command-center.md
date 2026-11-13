---
title: "Build HarborPoint's Management Command Center"
lab: 5
day: 2
module: "Module 5 · Building Management Dashboards"
duration: 60
sea_state: calm
role: "Delivery Manager, Digital Banking"
summary: "Build a Digital Banking dashboard that answers five management questions at a glance, then cut it down to an executive view a VP can read in thirty seconds."
---

!!! briefing "Mission briefing"
    Yesterday you answered Priya's questions one query at a time. That worked once. It won't work every Monday, and it doesn't work at all when Priya asks at 7:40 and you're still on the train.

    Today you build the **Digital Banking Command Center**: one project dashboard that answers the questions a delivery manager gets asked about the Digital Banking initiative, from current work and delivered Features to outstanding bugs, delivery progress and risks. You build it from the query toolkit you made in [Lab 3](../day-1/lab-03-query-toolkit.md), plus a handful of Analytics widgets that no query can give you.

    Then you do the harder part: you cut it down. Dana Whitfield doesn't want twelve widgets. She wants to know whether Digital is on course and what you need from her.

    **Done looks like:** `P## - Digital Banking Command Center` with every widget tied to a question, a six-widget `P## - Digital Banking Exec View`, and a partner who can answer your five questions from your dashboard in thirty seconds.

<div class="msg" data-initials="PR" data-tone="teal" markdown>
<p class="msg-head"><strong>Priya Raman</strong><span>Director, Digital Banking · 8:05 AM</span></p>

Your queries yesterday were exactly right. Now I'd like to stop asking for them. Can you build me one page I can open before any meeting that tells me what's in flight, what landed, what's broken and what's at risk across both digital teams? If Dana could read a version of it without a translator, even better.
</div>

## What you'll walk away with

- Design a dashboard from the questions it must answer, not from the widget catalog
- Connect shared queries to Query Tile, Query Results and Chart for Work Items widgets, and set thresholds that mean something
- Configure team-scoped Analytics widgets (Velocity, Sprint Burndown, Cumulative Flow, Cycle Time) for the right team
- Decide what belongs on a manager's dashboard and what belongs on an executive's, and defend what you dropped
- Keep a dashboard honest: ownership, refresh, edit rights and a review cadence

## Before you set sail

- **Access:** Basic, as a Contributor. Contributors can create **project dashboards** and edit only the ones they create. You won't touch any team's dashboard, including Leo's.
- **Your ID** is set (the **Crew** chip). Your query folder `Shared Queries/Training/P##/` exists from [Lab 3](../day-1/lab-03-query-toolkit.md), with `04 Features at risk` and `06 Orphan work` in it. Skipped Lab 3? The fallback definitions are in Part 3.
- **Team context:** the widgets read `Mobile Banking` and `Digital Accounts` data. You select those teams *inside each widget's configuration*. You never change their team settings, backlogs or boards.
- **You'll create:** two project dashboards and six small queries in `Shared Queries/Training/P##/`, all prefixed `CC - ` so they sort together.
- **Time-box:** 60 minutes. Parts 3 and 4 are the build; protect 15 minutes for Parts 5 and 6. The exec cut is where the judgment lives.

!!! warning "Dashboards are public in this project"
    Every member of the HarborPoint project can **view** every dashboard. There are no private dashboards. Build as if Priya, Leo and Dana will all open yours, because they can.

## Part 1 — Start with questions, not widgets

The most common dashboard is a wall: every widget the builder found, arranged by when they found it. Nobody can read a wall. Before you open the catalog, decide what this page is *for*.

!!! challenge "Challenge: Five questions"
    Write down the **five questions** your Command Center must answer for Priya, one line each, phrased the way she'd ask them. Then, next to each, write **who acts on the answer** and **how often** they'd look. You'll test the finished dashboard against this list in Part 6, so keep it.

    Constraint: at least one question must be about **Features**, not stories, and at least one must be about something that could go wrong *next* sprint, not something that already did.

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    The course outline gives you a head start: *current work, completed items, outstanding bugs, delivery progress, potential risks*. Turn each phrase into a question Priya would actually ask, with a time window in it.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    Good dashboard questions have a **scope** (both digital teams), a **window** (this sprint, the last five sprints, the next three weeks) and an **action** behind them. "How many bugs are there?" has no action. "Are there urgent bugs nobody is fixing?" does.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    A model list. Yours can differ; the shape matters more than the words.

    | # | Question | Who acts | How often |
    |:-:|:--|:--|:--|
    | Q1 | **What are both teams working on this sprint, and is the sprint on track?** | You, with Diego and Grace | Daily |
    | Q2 | **What have we delivered, and is delivery steady?** | You and Priya | Every sprint |
    | Q3 | **Are there urgent bugs, and are they growing?** | Engineering managers | Daily |
    | Q4 | **How are the Digital Features progressing toward their target dates?** | Priya, Product Owners | Weekly |
    | Q5 | **What's at risk or blocked, and is our effort going where the portfolio needs it?** | You, escalating to Priya | Twice a week |

    Q4 and Q5 are Feature questions. Q5's second half (effort going where the portfolio needs it) is the orphan-work signal from Lab 2.

!!! insight "Lighthouse insight: a dashboard is a set of answers"
    Every widget should earn its place by answering a question someone acts on. If you can't say which question a widget answers, it's decoration. If two widgets answer the same question, one of them is noise. The five questions are also your **removal test**: when the dashboard grows (and it will), anything that doesn't serve one of them goes.

!!! checkpoint "Checkpoint"
    - [ ] I have five written questions, each with who acts and how often
    - [ ] At least one is about Features and one looks forward

## Part 2 — Create the dashboard and its header

!!! speedrun "Speed run · 6 minutes"
    Create a **project** dashboard named `P## - Digital Banking Command Center` that refreshes itself, and add a **Markdown** widget across the top with: who owns the page, what it's for, when it was last reviewed, a color legend, and links to the Program Charter wiki page, the **HarborPoint Program Plan** and your query folder.

<div class="timer" data-minutes="6" data-label="Speed run"></div>

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Dashboards live under **Overview**. The create dialog asks for a **Dashboard Type**. A *team* dashboard belongs to one team's admins; a *project* dashboard belongs to you.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    **Overview › Dashboards** › **+ New Dashboard**. Tick **Automatically refresh the dashboard every 5 minutes** and pick **Project Dashboard**. In edit mode, search the **Add Widget** pane for `Markdown`. Size lives in the widget's **Configuration** panel, not on the canvas.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    1. **Overview › Dashboards** › **+ New Dashboard**.
    2. **Name** `P## - Digital Banking Command Center`. **Description** `Digital Banking delivery: current work, delivery, bugs, Feature progress and risk. Mobile Banking + Digital Accounts.`
    3. Tick **Automatically refresh the dashboard every 5 minutes**.
    4. **Dashboard Type**: **Project Dashboard**. Select **Create**.
    5. Select **Edit**. In **Add Widget**, search `Markdown`, select it, then **Add**.
    6. Hover the widget, select **⋯** › **Configure**. Set **Width** to the widest value that fits your screen (try `6`) and **Height** `2`. Choose **Custom markdown** and paste the block below, replacing the placeholders with URLs copied from your browser's address bar.
    7. **Save**, then **Done Editing**.

    ```markdown
    ## Digital Banking Command Center
    **Owner:** P## (Delivery Manager, Digital Banking) · **Reviewed:** Sprint 14 · **Teams:** Mobile Banking, Digital Accounts

    Answers five questions: current work · delivery · urgent bugs · Feature progress · risk and alignment.
    **Tiles:** green = nothing to do · amber = look today · red = act today. Select any tile to open its query.

    [Program Charter](<paste wiki page URL>) · [HarborPoint Program Plan](<paste plan URL>) · [My queries](<paste query folder URL>)
    ```

    **Expected result:** an empty dashboard with a header that tells a stranger whose page this is, what it's for and how fresh it is.

<!-- VERIFY: dashboard type labels "Team Dashboard" / "Project Dashboard" and the auto-refresh checkbox wording in the live Create a dashboard dialog; whether a plain Contributor can create a Project Dashboard (expected yes). -->

<!-- SHOT: lab05-create-dialog | Overview › Dashboards › + New Dashboard, Create a dashboard dialog filled in: name P## - Digital Banking Command Center, auto-refresh ticked, Project Dashboard selected | crop: dialog only; highlight the auto-refresh checkbox and Project Dashboard radio -->

Two details in that header do more work than they look. **Reviewed: Sprint 14** tells the reader how much to trust the page. The **legend** turns tile colors from your private code into a shared rule, which matters the first time someone asks why a tile is red.

!!! checkpoint "Checkpoint"
    - [ ] `P## - Digital Banking Command Center` exists as a project dashboard with auto-refresh on
    - [ ] Its Markdown header names the owner, the review sprint, the legend and three working links

## Part 3 — Wire up the queries

Query widgets are the backbone: counts that turn red, and lists you can click into. They have two rules. The query must be **shared** (a query in *My Queries* can't be used, and others couldn't see it anyway), and charts need a **flat list** query. Anything you save in `Shared Queries/Training/P##/` qualifies.

You'll build four tiles and one list. Each answers part of Q3 or Q5.

### 3a. The risk tile (and a trap)

1. **Edit** › **Add Widget** › search `Query Tile` › **Add**.
2. **Configure**: **Title** `Features at risk`. **Query**: `Shared Queries/Training/P##/04 Features at risk` (from Lab 3).
3. **Conditional formatting** › **+ Add rule**: amber **If number of work items** `>=` `1`. Add a second rule: red `>=` `3`. **Save**.

Look at the number before you read on. Then write one sentence in your notes: what would Priya conclude from it?

??? info "Skipped Lab 3? Fallback definitions"
    Save each in `Shared Queries/Training/P##/`.

    **`04 Features at risk`** (Flat list of work items)

    | Group | And/Or | Field | Operator | Value |
    |:-:|:--|:--|:--|:--|
    | | | Work Item Type | = | `Feature` |
    | ┌ | And | Target Date | <= | `@Today + 21` |
    | │ | And | State | <> | `Closed` |
    | │ | Or | Risk | = | `1 - High` |
    | └ | Or | Tags | Contains | `at-risk` |

    Group the last four rows. Inside that group, also group Target Date with State, so "not Closed" applies only to the date test. **Expected:** 8 Features.

    **`06 Orphan work`** (Work items and direct links): top level `Work Item Type` `=` `User Story`; linked work items `Work Item Type` `=` `Feature`; **Filter options** **Only return items that do not have matching links**; **Types of links** **Return selected link types** with only **Parent** ticked.

<!-- VERIFY: nested grouping renders as described in New Boards Hub (select the rows, then Group clauses); exact wording "Only return items that do not have matching links" / "Return selected link types". -->

!!! reef "Reef ahead: the right query on the wrong page"
    Your tile says **8**, in red. On a page titled *Digital Banking*, Priya reads that as "eight Digital Features are at risk". There are three. The Lab 3 query covers the **whole program**: it also catches Member Support, Branch Experience, Security and Core Platform Features. Reusing a query is smart. Reusing it without checking its **scope** against the page it lands on is how dashboards start lying. Every widget inherits the scope of its query or its team, and the dashboard title promises a scope too. They have to match.

Fix it without breaking Lab 3:

4. Open `04 Features at risk` in **Boards › Queries**, add a clause **outside** the OR group: `And` `Area Path` `Under` `HarborPoint\Digital`. Use **Save as** (not **Save**) to `CC - Digital Features at risk`.
5. Back on the dashboard, point the tile at `CC - Digital Features at risk`.

**You should see 3:** `Mobile Check Deposit 2.0`, `Spending Insights` and `Real-Time Fraud Alerts`. Real-Time Fraud Alerts serves the Fraud Epic, but it's owned by Mobile Banking, so its area is under Digital. That's correct for this page: it's Digital's work to deliver.

??? info "Under the hood: WIQL"
    ```sql
    SELECT [System.Id], [System.Title], [System.State], [Microsoft.VSTS.Scheduling.TargetDate]
    FROM WorkItems
    WHERE [System.WorkItemType] = 'Feature'
      AND [System.AreaPath] UNDER 'HarborPoint\Digital'
      AND (
            ([Microsoft.VSTS.Scheduling.TargetDate] <= @Today + 21 AND [System.State] <> 'Closed')
         OR [Microsoft.VSTS.Common.Risk] = '1 - High'
         OR [System.Tags] CONTAINS 'at-risk'
      )
    ```

### 3b. The at-risk list

A count says *how many*. Priya's next question is always *which ones*.

6. **Add Widget** › `Query Results` › **Add**. **Configure**: **Title** `Digital Features at risk`, **Query** `CC - Digital Features at risk`, wide enough to show columns `Title`, `State`, `Target Date`, `Node Name`, `Risk`, `Tags`. Columns come from the saved query, so set them in **Column options** on the query and **Save** it if they're missing.

<!-- VERIFY: whether the Query Results widget config offers its own column selection or always uses the saved query's columns. -->

Read the three rows. `Spending Insights` is here because its Target Date is close, and it's 88% done. `Mobile Check Deposit 2.0` is due this sprint at 61%. `Real-Time Fraud Alerts` is 4% done. One tile, three very different conversations. That's why a risk count should always sit next to the list behind it.

### 3c. Urgent bugs and blocked work

7. Create two flat queries in `Shared Queries/Training/P##/` and give each a Query Tile:

    **`CC - Open P1-P2 bugs (Digital)`** (Flat list of work items)

    | And/Or | Field | Operator | Value |
    |:--|:--|:--|:--|
    | | Work Item Type | = | `Bug` |
    | And | Area Path | Under | `HarborPoint\Digital` |
    | And | State | <> | `Closed` |
    | And | Priority | <= | `2` |

    **`CC - Blocked work (Digital)`** (Flat list of work items)

    | And/Or | Field | Operator | Value |
    |:--|:--|:--|:--|
    | | Area Path | Under | `HarborPoint\Digital` |
    | And | Tags | Contains | `blocked` |
    | And | State | Not In | `Closed,Removed` |

8. Tile rules: for bugs, amber `>=` `1`, red `>=` `10`. For blocked, red `>=` `1` (a blocked item is a request for help, and one is enough).

**You should see** at least **18** open P1/P2 bugs, and 18 of them are Mobile Banking's (4 Priority 1, 14 Priority 2). Add `Node Name` as a column to check. **Blocked** shows **1**: Mobile Banking's `Member confirms or denies a flagged transaction`, waiting on Security's API. You'll pull that thread in [Lab 7](lab-07-cross-team-bottleneck.md).

<!-- VERIFY: count of Digital Accounts open bugs at Priority 1-2 in the seeded data (World Bible gives DA 4 open bugs but no priority split), and that no other open Digital item carries the blocked tag. -->

### 3d. The alignment tile

!!! challenge "Challenge: Orphans on the dashboard"
    Add a Query Tile titled `Orphan stories this sprint` that counts **Digital stories in the current sprint with no parent Feature**, for both teams. Save its query as `CC - Orphan stories this sprint (Digital)`. Start from your Lab 3 `06 Orphan work` query.

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Orphans are a question about a **missing link**, so this stays a *Work items and direct links* query. You only need to narrow the **top-level** filters: which area, which sprint.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    Add `Area Path` `Under` `HarborPoint\Digital` and `Iteration Path` `=` `@CurrentIteration` to the top-level clauses. `@CurrentIteration` needs a team: pick `Mobile Banking`. Both digital teams share the same sprint nodes, so one team's current sprint is Sprint 14 for both.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    1. Open `06 Orphan work`, then **Save as** `CC - Orphan stories this sprint (Digital)`.
    2. **Filters for top level work items**:

        | And/Or | Field | Operator | Value |
        |:--|:--|:--|:--|
        | | Work Item Type | = | `User Story` |
        | And | Area Path | Under | `HarborPoint\Digital` |
        | And | Iteration Path | = | `@CurrentIteration` (team `Mobile Banking`) |

    3. **Filters for linked work items**: `Work Item Type` `=` `Feature`. **Filter options**: **Only return items that do not have matching links**. **Types of links**: **Return selected link types**, **Parent** only. **Save**.
    4. Add a Query Tile for it with amber `>=` `1` and red `>=` `5`.

    **Expected result: 6.** Five are Mobile Banking's (`Dark mode polish for redesigned screens`, `Upgrade analytics SDK`, `Holiday promo banner (marketing request)`, `App Store listing refresh`, `Upgrade push notification SDK`) and one is Digital Accounts' (`Statement search by date range`). Some orphan work is legitimate, like SDK upgrades. A marketing banner added on day 3 is a different conversation.

    ??? info "Under the hood: WIQL"
        ```sql
        SELECT [System.Id], [System.Title]
        FROM WorkItemLinks
        WHERE ([Source].[System.WorkItemType] = 'User Story'
               AND [Source].[System.AreaPath] UNDER 'HarborPoint\Digital'
               AND [Source].[System.IterationPath] = @currentIteration('[HarborPoint]\Mobile Banking'))
          AND ([System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Reverse')
          AND ([Target].[System.WorkItemType] = 'Feature')
        MODE (DoesNotContain)
        ```

<!-- VERIFY: that the Query Tile widget accepts a Work items and direct links query and counts top-level rows (6). If it doesn't, use a Query Results widget for the same query and note the count in its title. -->

<!-- SHOT: lab05-query-tile-config | P## - Digital Banking Command Center in edit mode, Configuration panel of the "Orphan stories this sprint" Query Tile showing the query path and two conditional formatting rules | crop: config panel and the tile; highlight the conditional formatting rows -->

!!! insight "Lighthouse insight: a threshold is a policy"
    The moment a tile turns red at 10 bugs, you've made a rule: *ten urgent bugs is an emergency*. Did anyone agree to that? Put thresholds in the legend, agree them with the people who'll be judged by them, and change them deliberately. Otherwise every color is your opinion wearing a uniform.

!!! checkpoint "Checkpoint"
    - [ ] My risk tile and list read `CC - Digital Features at risk` and show **3** Features
    - [ ] I have tiles for urgent bugs (at least 18), blocked work (1) and orphan stories this sprint (6), each with color rules
    - [ ] I can say which of my five questions each tile answers

## Part 4 — Add the charts and team metrics

Now the pictures: two query charts for the shape of the work, and four Analytics widgets for delivery and flow. Analytics widgets are **team-scoped**. On a project dashboard, every one of them has a **Team** selector, and that selector is the single most important field in the panel.

### 4a. Two query charts

9. Create two flat queries and add a **Chart for Work Items** widget for each (**Add Widget** › `Chart for Work Items` › **Configure**). If you made a Digital Features query in [Lab 4](../day-1/lab-04-sprint-delivery-report.md), reuse it.

| Query (flat list) | Clauses | Chart |
|:--|:--|:--|
| `CC - Digital Features by State` | `Work Item Type` `=` `Feature` · `Area Path` `Under` `HarborPoint\Digital` · `State` `<>` `Removed` | **Pie**, **Group by** `State`, **Count** |
| `CC - Current sprint stories (Digital)` | `Work Item Type` `=` `User Story` · `Area Path` `Under` `HarborPoint\Digital` · `Iteration Path` `=` `@CurrentIteration` (team `Mobile Banking`) | **Stacked bar**, `Node Name` by `State`, **Count** |

Add `Node Name`, `State`, `Story Points`, `Parent` and `Tags` as columns on both queries before saving. Charts can only group by fields that are in the query.

<!-- VERIFY: Stacked bar axis labels in the Chart for Work Items config (e.g., "Y-axis" / "Group by" and "Stacked by"). -->

**You should see:**

- **Features by State:** 9 Features. **Active 5**, **New 2**, **Closed 2**. The ninth is Real-Time Fraud Alerts, under the Fraud Epic but owned by Mobile.
- **Current sprint stories:** Mobile Banking **19** (Closed 4, Resolved 3, Active 7, New 5) and Digital Accounts **9** (Closed 4, Active 3, New 2). Switch **Aggregation** to **Sum** of `Story Points` for a moment: 65 points against 26. Notice how much of Mobile's bar is *Resolved*. You'll come back to that in [Lab 6](lab-06-which-team-needs-help.md).

The **Chart for Work Items** widget can also **Group by** `Tags`, which the Queries page can't. Remember that for the Extra knots.

### 4b. Delivery and flow, one team at a time

10. Add these four Analytics widgets. For every one, set **Team** first, then put the team's name in the **Title**.

| Widget | Title | Key settings |
|:--|:--|:--|
| **Velocity** | `Velocity · Mobile Banking` | **Team** `Mobile Banking` · **Work items** **Backlog** `Stories` · **Velocity** **Sum** of `Story Points` · **Number of Iterations** `6` · tick **Display planned work for iterations** |
| **Velocity** | `Velocity · Digital Accounts` | Same, with **Team** `Digital Accounts` |
| **Sprint Burndown** | `Sprint 14 burndown · Mobile Banking` | **Team** `Mobile Banking` · **Backlogs and work items** `Stories` · **Burndown On** **Sum** of `Story Points` · **Select Iteration** `@CurrentIteration` · tick **Show total scope** |
| **Cumulative Flow Diagram (CFD)** | `Flow · Mobile Banking` | **Team** `Mobile Banking` · **Backlog** `Stories` · **Time period** **Rolling period** reaching back to Sprint 9 (about `90` days) |
| **Cycle Time** | `Cycle time · Mobile Banking` | **Team** `Mobile Banking` · **Work items** **Work item type** `User Story` · **Rolling period** about `90` days |

<!-- VERIFY: maximum rolling period accepted by the CFD widget and the Cycle Time widget (the in-context CFD allows 14-180 days); which team the Team selector defaults to on a project dashboard. -->

<!-- SHOT: lab05-velocity-config | Configuration panel of the Velocity widget on P## - Digital Banking Command Center: Team = Mobile Banking, Backlog Stories, Sum of Story Points, 6 iterations, Display planned work ticked | crop: config panel; highlight the Team selector -->

**You should see:**

- **Mobile Banking velocity:** Completed 33, 37, 41, 45, 44 for Sprints 9 to 13, against Planned 38, 44, 50, 56, 62. Sprint 14 shows 12 so far against 60 planned.
- **Digital Accounts velocity:** Completed 24, 26, 25, 24, 26 against Planned 26, 26, 25, 27, 26. Sprint 14 shows 10 so far.
- **Sprint burndown:** a **Total Scope Increase** of 5 points (60 became 65 mid-sprint) and 12 points completed.
- **CFD and Cycle Time:** for now, just confirm they render. Reading them is Lab 6's job.

Why does the CFD include bugs? Mobile Banking manages bugs with requirements, so its 42 open bugs live on the Stories backlog and flow through the same board columns. That's real work competing for the same people, so leave them in.

!!! reef "Reef ahead: the widget that reports on the wrong team"
    A Velocity widget doesn't say which team it reads unless you write it in the title. Leave **Team** on whatever the panel offers and you may chart the program team, the default team, or the last team you looked at, and the chart will look perfectly plausible. A Velocity widget that reads `HarborPoint Team` adds up six teams' estimates into one meaningless number. **Set Team first, title second, and put the team name in every team-scoped title.** Dashboard copies make this worse: copied to a project dashboard, widgets keep their original team.

!!! reef "Reef ahead: velocity on a manager's wall"
    You just put two velocity charts side by side, so someone will compare them. Mobile's 44 looks better than Digital Accounts' 26. It isn't. Story Points are each team's private scale, and velocity is a capacity-planning input for the team that produced it, not a productivity score. Keep the two widgets, but in **separate columns** with the team name in each title, and add one line to your Markdown legend: *Velocity is per team; never compare across teams.* Lab 6 shows exactly how badly this comparison misleads.

!!! checkpoint "Checkpoint"
    - [ ] Features by State shows 9 Features (Active 5, New 2, Closed 2)
    - [ ] Current sprint stories shows Mobile Banking 19 and Digital Accounts 9, stacked by State
    - [ ] Two Velocity widgets, a Sprint Burndown, a CFD and a Cycle Time widget each show the team name in the title and read the right team

### 4c. Arrange it

Drag widgets into a reading order (edit mode only). People read a dashboard like a page: top-left first, and they rarely scroll. A layout that works:

| Row | Left | | | Right |
|:-:|:--|:--|:--|:--|
| 1 | **Header** (Markdown) | Tile: Features at risk | Tile: Urgent bugs | Tile: Blocked · Tile: Orphans |
| 2 | **Digital Features at risk** (Query Results, wide) | | Features by State (pie) | Current sprint stories |
| 3 | Sprint 14 burndown · Mobile | Velocity · Mobile | Velocity · Digital Accounts | |
| 4 | Flow · Mobile (CFD) | Cycle time · Mobile | | |

Top row: *is anything on fire?* Second row: *where are the Features?* Below the fold: the diagnostics you use when the top rows say something's wrong.

<!-- SHOT: lab05-command-center-full | P## - Digital Banking Command Center, view mode, all widgets laid out as in the layout table; tiles showing 3 / 18+ / 1 / 6 | full page; highlight the top row -->

## Part 5 — Cut it down for executives

You now have about fourteen widgets. You need every one of them on a bad Tuesday. Dana needs about five, every time.

!!! challenge "Challenge: The executive cut"
    Create `P## - Digital Banking Exec View` with **at most six widgets**, built from your Command Center. For every widget you **drop**, write one line on why. For every widget you **keep**, write the question Dana would ask that it answers.

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Ask of each widget: *does an executive make a decision from this, or does a team?* Executives decide about **outcomes, dates, risks and trade-offs**. Teams decide about sprints, flow and estimates.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    Don't use **Copy Dashboard** for this. It duplicates every query into a new Shared Queries folder, and you'll end up maintaining two copies of everything. Instead, create an empty project dashboard, then use each kept widget's **⋯** › **Copy to Dashboard**. The copies point at the same queries, so fixing a query fixes both pages.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    1. **Overview › Dashboards** › **+ New Dashboard** › **Name** `P## - Digital Banking Exec View`, **Project Dashboard**, auto-refresh on. **Create**.
    2. Back on the Command Center, select **Edit**, then for each kept widget: **⋯** › **Copy to Dashboard** › `P## - Digital Banking Exec View`.
    3. On the Exec View, rewrite the Markdown header as a bottom line, for example: *"Digital Banking, Sprint 14. Mobile Check Deposit 2.0 will miss this sprint; Real-Time Fraud Alerts is at risk for PI 4 (Security dependency). Decision needed: see risks below. Owner P##."*

    **A model cut (six):**

    | Keep | Dana's question |
    |:--|:--|
    | Markdown header, rewritten as a bottom line | "Are we going to make it, and what do you need from me?" |
    | Digital Features at risk (Query Results) | "Which commitments are in trouble?" |
    | Digital Features by State (pie) | "How much of the initiative is done, in flight, or not started?" |
    | Urgent bugs (tile) | "Is quality under control?" |
    | Blocked work (tile) | "Is anything stuck that I could unstick?" |
    | Orphan stories this sprint (tile) | "Is the effort going to our priorities?" |

    | Drop | Why |
    |:--|:--|
    | Both Velocity widgets | Team planning tools. Side by side, they invite the cross-team comparison you just warned against |
    | Sprint burndown | Sprint-tactical; it changes daily and an exec can't act on it |
    | CFD and Cycle Time | Diagnostics that need interpretation. That interpretation is your job, delivered as a sentence in the header |
    | Current sprint stories | Story altitude. Execs live at Features |
    | The risk count tile | Redundant next to the list; the list already has three rows |

    Reasonable people swap the orphan tile for a link to your status report, or the pie for a Features list sorted by Target Date. What you can't do is keep the diagnostics "just in case". Every extra widget makes the important ones harder to find.

<!-- VERIFY: Copy to Dashboard keeps the widget's query binding (not a copied query) when copying between project dashboards. -->

<!-- SHOT: lab05-exec-view | P## - Digital Banking Exec View, view mode, six widgets: bottom-line Markdown header, Digital Features at risk list, Features by State pie, three tiles | full page -->

!!! insight "Lighthouse insight: managers need diagnostics; executives need decisions"
    A manager's dashboard is a cockpit: dense, diagnostic, read daily by someone who knows what every gauge means. An executive's dashboard is a windscreen: few things, big, and each one tied to a decision. The most useful widget on an exec view is often the Markdown header, because it's the only one where *you* say what the numbers mean. A chart can't tell Dana "this will miss and here's the choice". You can.

!!! checkpoint "Checkpoint"
    - [ ] `P## - Digital Banking Exec View` has at most six widgets, copied from the Command Center
    - [ ] Its header states a bottom line in one or two sentences
    - [ ] I have a one-line reason for every widget I dropped

## Part 6 — Share it and keep it honest

A dashboard is a promise that someone is keeping it true. Make that promise explicit before anyone relies on it.

11. **Who can edit:** **Overview › Dashboards**, hover your Command Center row, **⋮** › **Security**. As creator you hold **Edit dashboard**, **Delete dashboard** and **Manage Permissions**. Everyone in the project can already *view* it. Close the dialog without changing anything, unless you want to name a co-owner.
12. **Freshness:** confirm auto-refresh is on (**⋯** › **Dashboard settings**). Analytics widgets lag edits by up to about 30 seconds, and trend widgets use daily snapshots, so "live" means "a few minutes old", which is fine for a manager.
13. **Ownership and cadence:** your header already names an owner and a review sprint. Add one line: `Reviewed every Monday before stand-up; thresholds agreed with Diego and Grace.` (Write what's true for you.)

<!-- VERIFY: the entry point for dashboard settings (⋯ › Dashboard settings vs a gear icon) and that it shows the auto-refresh checkbox. -->

!!! reef "Reef ahead: the dashboard nobody owns"
    In [Lab 11](../day-3/lab-11-dashboard-wrong.md) you'll meet Leo's Member Support dashboard. It still shows last sprint as "current", and a director believes her team has collapsed. Nobody did anything wrong on purpose. The page just drifted while everyone kept trusting it. A stale dashboard is **worse than no dashboard**, because no dashboard makes people ask, and a stale one answers them wrongly. Name an owner, put the review date on the page, and delete widgets you stop maintaining.

!!! challenge "Challenge: The 30-second test"
    Swap with a partner. Open their **Command Center** (find it in **Overview › Dashboards**; filter by their `P##`). Give them your five questions from Part 1, read aloud, and start a 30-second timer. They answer from your dashboard only, without opening a single query or asking you anything. Then swap roles.

    Score one point per question answered correctly. Anything under 5/5 tells you which widget to fix, move or rename.

<div class="timer" data-minutes="1" data-label="30-second test: call time at 0:30"></div>

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    When your partner hesitates, notice *where*. Hesitating on what a number means is a **title or legend** problem. Hesitating on where to look is a **layout** problem. Getting the answer wrong is a **scope** problem.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    The usual fixes: titles that are questions or plain statements (`Urgent bugs (P1-P2, both teams)` beats `Query Tile`), team names in every team-scoped title, the answer to Q5 in the top row, and the diagnostics below the fold.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    Reference answers your partner should be able to read off a good Command Center:

    | Question | Where | Answer today |
    |:--|:--|:--|
    | Q1 Current work, on track? | Current sprint stories; Sprint 14 burndown | 28 stories across both teams; Mobile has 3 sitting in Resolved and added 5 points mid-sprint |
    | Q2 Delivered, steady? | Velocity widgets; Features by State | Two Digital Features closed; Digital Accounts steady at 24 to 26 points; Mobile's planned vs completed gap is widening |
    | Q3 Urgent bugs? | Urgent bugs tile | At least 18 open P1/P2, essentially all Mobile's |
    | Q4 Feature progress? | Features by State; at-risk list | 5 Active, 2 New, 2 Closed; Mobile Check Deposit 2.0 due now at 61% |
    | Q5 Risk and alignment? | At-risk list; blocked and orphan tiles | 3 Features flagged (one is nearly done); 1 blocked story on Fraud Alerts; 6 orphan stories this sprint |

!!! checkpoint "Checkpoint"
    - [ ] I opened my dashboard's **Security** dialog and know who can edit it
    - [ ] My header names an owner and a review cadence
    - [ ] A partner scored my dashboard in the 30-second test, and I fixed at least one thing they stumbled on

## Knowledge check

<div class="quiz" markdown>

**Your Command Center's "Features at risk" tile shows 8, but only three Digital Features are in trouble. What's the most likely cause?**

- [ ] The tile caches an old result until the dashboard refreshes
- [x] The tile's query covers the whole program, not the Digital area
- [ ] Query Tiles count child stories as well as Features
- [ ] The tile is bound to the wrong team

<div class="quiz-why" markdown>
Query widgets inherit the scope of their query, and nothing on the tile shows that scope. The page title says *Digital*; the query said *everything*. Check every reused query against the scope the dashboard promises.
</div>

</div>

<div class="quiz" markdown>

**A Velocity widget on a colleague's project dashboard shows about 150 points a sprint, far more than any single HarborPoint team. What do you check first?**

- [ ] Whether the teams have started inflating their estimates
- [ ] Whether the widget counts bugs
- [x] Which team the widget is configured for, because a program-level team adds up several teams' points
- [ ] Whether auto-refresh is turned on

<div class="quiz-why" markdown>
Team-scoped widgets read one team's area and sprints. Point one at a team whose area includes sub-areas, like the program team, and you get a sum of six private scales: a number that's accurate and meaningless.
</div>

</div>

<div class="quiz" markdown>

**Dana will look at your Exec View for a minute before a steering meeting. Which widget is the strongest candidate to drop?**

- [ ] The list of Digital Features at risk
- [ ] The Markdown header with the bottom line
- [x] The Sprint 14 burndown for Mobile Banking
- [ ] The blocked-work tile

<div class="quiz-why" markdown>
A sprint burndown is a team's daily steering tool. It changes every day and leads to no decision an executive can make. The header and the risk list carry the decisions; the blocked tile is a direct "can you help?".
</div>

</div>

## Captain's log

!!! log "Captain's log"
    1. Think of the dashboard you look at most at work. Could you write down the five questions it answers? Could its owner?
    2. Which widget on your real dashboards would fail the 30-second test, and is the problem its title, its scope, or its existence?
    3. Who in your organization reads velocity as productivity? What would you put on the page instead to stop that?
    4. What's the review cadence for your team's dashboards today? Who would notice first if one went stale?
    5. If you could give your executive sponsor only three widgets, which would they be?

!!! bonus "Extra knots"
    1. **Group by tags.** Add a **Chart for Work Items** on `CC - Current sprint stories (Digital)` with **Group by** `Tags` and **Selected tags** `unplanned`, `tech-debt` and `blocked`. What share of Mobile Banking's sprint is work nobody planned? (Two `unplanned` stories, 5 points, both added after day 1.)
    2. **A release burnup.** Add a **Burnup** widget for **Teams** `Mobile Banking` and `Digital Accounts`, **Work items** backlog `Stories`, **Sum** of `Story Points`, plotted by **Iteration** from Sprint 13 to Sprint 16, with **Show total scope** on. Does the scope line climb faster than the completed line? What would you say about PI 4 if it did?
    3. **The dependency register.** If you finished Lab 7's Extra knots, add your program dependency query as a **Query Results** widget below the fold. It renders direct-links queries, which charts can't.

<!-- VERIFY: Extra knot 1 assumes Group by Tags is generally available in the Chart for Work Items widget (Learn notes a possible preview toggle); Extra knot 2 assumes the Burnup widget's Iteration plot interval accepts Sprint 13 to Sprint 16. -->

## Key takeaways

- Design from questions. Five questions, each with someone who acts on the answer, decide which widgets earn a place.
- Every widget inherits a scope from its query or its team. Check it against the scope your dashboard's title promises, and put team names in titles.
- Pair a count with the list behind it. A risk tile starts a conversation; the list tells you which conversation.
- Managers need diagnostics; executives need decisions. Cut the exec view to a handful of widgets and say in words what the numbers mean.
- A dashboard is only as good as its upkeep: a named owner, a review date on the page, and the discipline to delete what you no longer maintain.

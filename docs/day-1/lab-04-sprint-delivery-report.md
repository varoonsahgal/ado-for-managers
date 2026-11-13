---
title: "The Sprint Delivery Report"
lab: 4
day: 1
module: "Module 4 · Turning Query Results into Useful Information"
duration: 50
sea_state: choppy
role: "Delivery Manager, Digital Banking"
summary: "Turn queries into charts leadership can read, catch the ones that mislead, and write a one-page Digital Banking status report."
---

!!! briefing "Mission briefing"
    Leadership wants an update on Digital Banking: what was delivered, what's still outstanding, and what's at risk. You have the evidence already, scattered across a toolkit of queries, two teams' velocity reports and a portfolio backlog. Now it has to become something a busy executive can read in two minutes and trust.

    Charts are the obvious tool, and also the most dangerous one. A chart persuades before anyone checks it. The same data can say "on track" or "in trouble" depending on the slice, the measure and the time window you pick. In this lab you'll build the charts, deliberately make a few of them lie, and then write a one-page status report that would survive the CIO asking "how do you know?"

    **Done looks like:** four saved charts in your shared folder, a planned-versus-completed comparison for both Digital teams, and the wiki page `/Training/P##/Sprint Delivery Report` with an evidence-backed RAG status, a Feature table, risks and asks.

<div class="msg" data-initials="PR" data-tone="teal" markdown>
<p class="msg-head"><strong>Priya Raman</strong><span>Director, Digital Banking · 1:10 PM</span></p>

Dana wants a Digital Banking update for her staff meeting: what we delivered last sprint, where this sprint stands, what's outstanding and what's at risk. **One page.** Use charts if they help, not if they decorate. Marcus will be in the room, so every number needs to survive "how do you know?" And please don't hand me a green status unless it's actually green.
</div>

## What you'll walk away with

- Charts built from saved queries that answer one management question each, by state, team, priority and trend
- A planned-versus-completed reading for each team, without the cross-team comparison trap
- A working knowledge of what query charts can't do, so you don't promise a view Azure DevOps won't draw
- A sharp eye for misleading metrics: counts versus points, cherry-picked time windows, percentages without a deadline
- A one-page status report with a RAG rating you can defend

## Before you set sail

- **Access:** Basic. If you can't see a **Charts** tab on a saved query, you have Stakeholder access. Tell your instructor.
- **Charts work only on saved flat queries.** Tree and direct-link queries can't be charted. Save every chart query in `Shared Queries/Training/P##` (you created it in [Lab 3](lab-03-query-toolkit.md); if not, create it now). Charts on **My Queries** are visible only to you, and they can't be added to a dashboard.
- **Names for today:** `10 Digital Features (chart)`, `11 Digital stories this sprint (chart)`, `12 Open Digital bugs (chart)`.
- **Team views you'll read:** `Mobile Banking` and `Digital Accounts` (Velocity), and `Digital Portfolio` (Features backlog). Report settings and column options are per user, so adjust freely.
- **Time-box:** 50 minutes. Save 15 for the report in Part 5. That's the deliverable, and the charts exist to serve it.

## Part 1 — What does Digital Banking's portfolio look like?

!!! speedrun "Speed run · 8 minutes"
    Build `10 Digital Features (chart)`: every **Feature** owned by a team under `HarborPoint\Digital`, with a **pie chart by State**. Then answer: how many Features, and how many in each state?

<div class="timer" data-minutes="8" data-label="Speed run"></div>

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    A flat query, saved to your shared folder first. The chart lives on the query's **Charts** tab.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    `Work Item Type` `=` `Feature` and `Area Path` `Under` `HarborPoint\Digital`. Save it, then **Charts** › **New chart** › **Pie**, **Group by** `State`, aggregation **Count of work items**.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    1. **Boards › Queries** › **New** › **New query**, **Flat list of work items**:

        | And/Or | Field | Operator | Value |
        |:--|:--|:--|:--|
        | | Work Item Type | = | `Feature` |
        | And | Area Path | Under | `HarborPoint\Digital` |

    2. **Column options**: `Title`, `State`, `Node Name`, `Target Date`, `Tags`. **Save** as `10 Digital Features (chart)` in `Shared Queries/Training/P##`.
    3. **Charts** › **New chart**. Chart type **Pie**, **Group by** `State`, aggregation **Count of work items**. Title it `Digital Features by State`. Select **OK**.

        <!-- VERIFY: chart dialog labels (Chart type, Group by, Aggregation, "Count of work items") and the save button (OK vs Save). -->

    **Expected:** **9** Features. **Active 5** (`Mobile Check Deposit 2.0`, `Biometric Login`, `Online Account Opening`, `Spending Insights`, `Real-Time Fraud Alerts`), **Closed 2** (`Mobile App Redesign`, `Paperless Statements & Documents`) and **New 2** (`Member-to-Member Transfers`, `Instant Card Controls`).

<!-- SHOT: lab04-features-pie | Boards › Queries › Shared Queries/Training/P##/10 Digital Features (chart), Charts tab, pie "Digital Features by State" | crop: chart with legend showing Active 5, Closed 2, New 2 -->

**Wait: nine?** In Lab 1 you counted **8** Features under *Digital Banking Modernization*. The ninth is `Real-Time Fraud Alerts`. Mobile Banking builds it, so it sits in a Digital area, but it serves the number one Epic, *Fraud Detection & Security*.

Neither number is wrong. They answer different questions:

| Scope | Answers | Count |
|---|---|---|
| **By Area Path** (who builds it) | "What are my teams delivering?" | 9 |
| **By Epic** (what it serves) | "How is the Digital Banking initiative doing?" | 8 |

Leadership asked about the *initiative*, so your report is about the 8. But the ninth is Mobile Banking's, it's priority #1, and it's in trouble. A report scoped strictly to the Epic would leave out the most important thing your teams are working on. **Decide your scope out loud**, and put it on the page.

!!! insight "Lighthouse insight: every chart answers exactly one question"
    Before you build a chart, write the question it answers in its title. "Digital Features by State" is a title. "Is the Digital Banking initiative on track?" is a question, and a pie by state can't answer it, because it counts a finished 55-point Feature and an empty one as equal slices. If the chart can't answer the question in its title, you need a different chart.

!!! checkpoint "Checkpoint"
    - [ ] `10 Digital Features (chart)` has a pie showing 9 Features: Active 5, Closed 2, New 2
    - [ ] I can explain the difference between the 9 (area) and the 8 (Epic), and I've decided which one my report uses

## Part 2 — What got done, against what was planned?

The first question in any status meeting: did the teams deliver what they said they would?

### Read the Velocity reports

For each Digital team: **Boards › Backlogs**, pick the team, **Stories** level, the **Analytics** tab, then **View full report** on the **Velocity** card. Hover over a sprint's bars to read **Planned**, **Completed** and **Incomplete**.

<!-- VERIFY: "Analytics" tab placement on the backlog in New Boards Hub and the Velocity card label ("Velocity" / "Average Velocity"). -->

Fill in Sprint 13 before you look at the hint:

| Team | Planned (pts) | Completed (pts) | Completed ÷ Planned |
|---|---|---|---|
| Mobile Banking | | | |
| Digital Accounts | | | |

<!-- SHOT: lab04-velocity-mobile | Boards › Backlogs, team Mobile Banking, Stories level, Analytics › Velocity full report, Sum of Story Points, Sprint 9 to Sprint 14 | crop: chart; highlight Sprint 13 Planned 62 vs Completed 44 -->

Now a quick gut check. **Which team delivered more last sprint?** Commit to an answer before you open the hint.

??? pilot "Harbor Pilot · Hint: the numbers"
    | Team | Planned | Completed | Completed ÷ Planned |
    |---|---|---|---|
    | Mobile Banking | 62 | 44 | **71%** |
    | Digital Accounts | 26 | 26 | **100%** |

    The trend matters as much as the sprint. Mobile's completion rate has fallen every sprint: 87%, 84%, 82%, 80%, then 71%. Digital Accounts has completed at least 89% of its plan in every one of the last five sprints, and all of it in three.

    Switch **Velocity by** to **Count of Work Items**. Mobile's bars flatten to roughly a dozen stories a sprint, while its points climbed from 33 to 45. You'll take that apart properly in [Lab 6](../day-2/lab-06-which-team-needs-help.md).

    <!-- VERIFY: whether Count of Work Items includes closed bugs (bugs are managed with requirements), which would add 2-3 per sprint to Mobile's count. -->

!!! reef "Reef ahead: “Mobile delivered 44, Digital Accounts only 26”"
    If you answered "Mobile Banking", you compared two teams' Story Points as if they were the same currency. They aren't. Each team sizes its own work, so 44 Mobile points and 26 Digital Accounts points aren't comparable, just as 44 euros and 26 dollars aren't. The only fair comparison is each team **against its own plan**. On that measure, Digital Accounts did everything it promised and Mobile Banking missed by almost a third.

    Two more things the Velocity chart won't say out loud. **Planned** is a snapshot from the sprint's first day, so the 5 points Mobile added mid-sprint in Sprint 14 never appear as planned work. And **Resolved stories don't count as Completed.** Mobile has 11 points sitting in Resolved right now, waiting for its one tester.

### Chart this sprint, by team and state

1. Build `11 Digital stories this sprint (chart)` as a flat query:

    | And/Or | Field | Operator | Value |
    |:--|:--|:--|:--|
    | | Work Item Type | = | `User Story` |
    | And | Area Path | Under | `HarborPoint\Digital` |
    | And | Iteration Path | = | `@CurrentIteration` · team `Mobile Banking` |

    Columns: `Title`, `State`, `Node Name`, `Story Points`, `Parent`. Save it.

2. **New chart** › **Stacked bar**, `Node Name` by `State`, **Count of work items**. Title: `This sprint: stories by team and state`.
3. **New chart** › **Pivot table**, **Rows** `Node Name`, **Columns** `State`, aggregation **Sum** of `Story Points`. Title: `This sprint: points by team and state`.

    <!-- VERIFY: stacked bar axis labels and the pivot table's Rows/Columns labels in the chart dialog. -->

**You should see:**

| Team | Closed | Resolved | Active | New | Total |
|---|---|---|---|---|---|
| Mobile Banking | 4 stories · 12 pts | 3 · 11 pts | 7 · 29 pts | 5 · 13 pts | **19 · 65 pts** |
| Digital Accounts | 4 · 10 pts | – | 3 · 10 pts | 2 · 6 pts | **9 · 26 pts** |

<!-- SHOT: lab04-sprint-pivot | Shared Queries/Training/P##/11 Digital stories this sprint (chart), Charts tab, pivot table Node Name by State with Sum of Story Points | crop: pivot grid; highlight Mobile Banking's Closed 12 and Resolved 11 cells -->

**So what?** We're six or seven days into a ten-day sprint. Digital Accounts has closed 38% of its points with a normal amount of work in flight. Mobile Banking has closed **18%**. Even if all three Resolved stories pass QA today, it reaches 35%, with 29 points still Active and 13 not started. This sprint is going the way the last one went.

!!! info "What query charts can't do"
    Plan your report around these limits, not into them:

    | You want to… | Reality |
    |---|---|
    | Chart a tree or direct-links query | Not possible. **Flat** queries only |
    | Group by **Parent**, **Tags**, **Title** or a date | Not offered in query charts. (The **Chart for Work Items** dashboard widget can group by Tags, Lab 5) |
    | Group by team | Use **Node Name**. Area Path and Iteration Path show only the last segment, so same-named nodes merge |
    | Show more than 8 categories | The rest roll up into *(other)* |
    | Trend a big query | Keep trend queries to 1,000 items or fewer |
    | Show progress % per Feature | Not a chart. Use the backlog's rollup columns |
    | Share a chart from **My Queries** | Only you can see it. Save to a shared folder |

    <!-- VERIFY: whether Parent appears in the chart Group by list in New Boards Hub (research: uncertain). -->

!!! checkpoint "Checkpoint"
    - [ ] I recorded Sprint 13 Planned vs Completed for both teams (62/44 and 26/26)
    - [ ] My pivot shows Mobile Banking at 12 of 65 points Closed and 11 in Resolved
    - [ ] I can say why comparing the two teams' velocity is meaningless

## Part 3 — What's outstanding: the quality trend

Unfinished stories are only half of what's outstanding. The other half is the bug backlog, and it's the half that quietly eats next sprint's capacity.

1. Build `12 Open Digital bugs (chart)`:

    | And/Or | Field | Operator | Value |
    |:--|:--|:--|:--|
    | | Work Item Type | = | `Bug` |
    | And | Area Path | Under | `HarborPoint\Digital` |
    | And | State | <> | `Closed` |

    Columns: `Title`, `State`, `Priority`, `Severity`, `Node Name`, `Assigned To`. (Bugs have no Removed state, so `<> Closed` is safe here.) Save it.

2. **New chart** › **Stacked area** (a trend chart), **Group by** `Node Name`. Set the rolling period to the **longest** option available. Title: `Open Digital bugs, by team`.

    <!-- VERIFY: trend chart type names and the rolling-period dropdown values; confirm the longest option covers Sprint 9 onward (about 12 weeks), and that backdated seed revisions render in the trend. -->

3. **New chart** › **Stacked bar**, `Node Name` by `Priority`, **Count of work items**. Title: `Open Digital bugs by priority`.

**You should see 46 open bugs today:** **42** in Mobile Banking and **4** in Digital Accounts. Over the trend window, Mobile's band climbs steadily from **8** open bugs at the start of Sprint 9, while Digital Accounts' thin band slips from 7 to 4. Mobile's 42 break down as Priority 1: **4**, Priority 2: **14**, Priority 3: **18**, Priority 4: **6**. Three are Severity **1 - Critical**.

<!-- SHOT: lab04-bug-trend | Shared Queries/Training/P##/12 Open Digital bugs (chart), Charts tab, stacked area trend grouped by Node Name over the longest rolling period | crop: chart; highlight Mobile Banking's band rising from 8 to 42 -->

**So what?** A team that opens 13 bugs and closes 2 in a sprint, as Mobile did in Sprint 13, isn't finishing work. It's moving it from the sprint backlog to the bug backlog. A fivefold rise in open bugs over five sprints is what "velocity going up" looked like from the other side.

!!! checkpoint "Checkpoint"
    - [ ] My trend chart shows Mobile Banking's open bugs climbing from 8 to 42, and Digital Accounts' falling to 4
    - [ ] I know how many of Mobile's open bugs are Priority 1 (4) and Critical (3)

## Part 4 — Make the chart lie

You'll learn to spot a misleading chart faster by building one.

!!! challenge "Challenge: Make the chart lie, then make it honest"
    Pick **two** of these headlines and build a chart (or set up a report view) that genuinely seems to support each one, using only real HarborPoint data:

    1. **"Mobile Banking is on track."**
    2. **"The bug situation is under control."**
    3. **"Mobile Banking delivers 70% more than Digital Accounts."**

    For each, write down: **what makes it misleading**, and **what you'd show instead**.

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Lies in charts come from three places: **what you count** (items or size), **when you look** (the time window), and **what you compare** (things on different scales).

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    1. **Save as** `10` with the area narrowed to Mobile Banking, and look at the pie.
    2. Shorten your bug trend's rolling period to the shortest option.
    3. Open both teams' Velocity reports next to each other and read only the Sprint 13 Completed bars.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    | Headline | The lie | Why it misleads | Show this instead |
    |---|---|---|---|
    | "Mobile is on track" | Pie of Mobile's 5 Features by State: 1 Closed, 3 Active, 1 New. "Four out of five done or under way" | **Counting** treats every Feature as equal. It hides that `Mobile Check Deposit 2.0` is due *this sprint* with 36 points left, and that `Real-Time Fraud Alerts` is at 4% | A Feature table with progress by points, remaining points and Target Date |
    | "Bugs are under control" | Bug trend over the shortest window: a handful of new bugs, a gentle slope | The **window** hides the scale. Over five sprints it's 8 → 42 | The longest window, plus opened versus closed per sprint (Sprint 13: 13 opened, 2 closed) |
    | "Mobile delivers 70% more" | Sprint 13 Completed: 44 vs 26 | Points are **team-specific**. Mobile's stories also grew larger while its count stayed flat | Each team against its own plan: 71% vs 100%, with the five-sprint trend |

    The tell is the same every time. The chart answers a narrower question than its headline claims.

!!! reef "Reef ahead: “61% done”"
    `Mobile Check Deposit 2.0` is 61% complete by Story Points. That sounds like solid progress. But it's due at the **end of this sprint**, and 61% of 93 points leaves **36 points** with a few working days to go, more than a full sprint of Mobile's work on that Feature. A percentage without a deadline is a mood, not a status. Always report **what's left against the time left**.

!!! checkpoint "Checkpoint"
    - [ ] I built at least two misleading views from real data
    - [ ] For each one, I wrote what makes it misleading and what I'd show instead

## Part 5 — Write the one-page report

Now turn the evidence into something Dana can read in two minutes.

!!! challenge "Challenge: Digital Banking Status, Sprint 13 and Sprint 14 to date"
    Write one page with:

    1. **Overall status** (Red, Amber or Green) and a **one-sentence justification**
    2. **Delivered** in Sprint 13
    3. **Feature progress**: a table of Digital Banking's Features with state, progress, Target sprint and a status for each
    4. **Top risks** (three at most), each with its evidence
    5. **Asks and decisions**: what you need, from whom, by when

    State your scope (the 8 Features of the Epic, plus `Real-Time Fraud Alerts` because Mobile Banking owns it) and the as-of point (Sprint 14, week 2).

!!! deliverable "Deliverable"
    A wiki page `/Training/P##/Sprint Delivery Report`.

    1. **Overview › Wiki** › open `/Templates/Status Report`, select **Edit**, copy its Markdown, then close without saving.
    2. Go to your `/Training/P##` page (you created it in Lab 2) and add a sub-page named `Sprint Delivery Report`. Paste the template and fill it in.
    3. **Live data:** the wiki can embed a query's results as a table with `:::query-table <query-ID>:::`. Copy the ID from the query's URL (**More actions** › **Copy query URL**). Try it with `04 Features at risk`.
    4. **Charts:** the wiki can't embed a live query chart. Paste a screenshot, and label it with the as-of sprint, because it won't update.

    <!-- VERIFY: the query-table embed syntax and that it renders in the project wiki; the label of the wiki's "add sub-page" action; that /Templates/Status Report's sections match the five listed in the challenge. -->

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Start with the bottom line, then the evidence. For progress, open the **Digital Portfolio** Features backlog with a **Progress by Story Points** rollup column (from Lab 1). Your Lab 3 queries already hold the risks.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    Rate each **team and Feature** separately before you rate the whole. Digital Accounts is green on every measure you looked at. Mobile Banking is not. An honest overall rating can't average those away. Your strongest risks are the ones with two independent pieces of evidence each.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    A model one-pager. Yours can differ on judgment calls, but not on facts.

    **Overall: Amber, trending Red.** Digital Accounts is delivering exactly to plan. Mobile Banking will miss a committed Feature this sprint, and the priority #1 Feature it owns is blocked by another team.

    **Delivered in Sprint 13:** `Paperless Statements & Documents` closed. Digital Accounts completed 26 of 26 planned points, advancing Online Account Opening and Spending Insights. Mobile Banking completed 44 of 62 (71%), advancing Mobile Check Deposit 2.0 and Biometric Login, but 23 of those 44 points were work with no parent Feature.

    | Feature | Team | State | Progress (pts) | Target | Status |
    |---|---|---|---|---|---|
    | Mobile Check Deposit 2.0 | Mobile Banking | Active | 61%, 36 pts left | Sprint 14 | **Red**: will miss |
    | Biometric Login | Mobile Banking | Active | 53% | Sprint 16 | Amber: 24 pts left, work waiting on QA |
    | Real-Time Fraud Alerts *(serves Fraud Detection & Security)* | Mobile Banking | Active | 4% | Sprint 16 | **Red**: blocked on Security's risk-score API |
    | Online Account Opening | Digital Accounts | Active | 59% | Sprint 16 | Green |
    | Spending Insights | Digital Accounts | Active | 88% | Sprint 15 | Green |
    | Instant Card Controls | Digital Accounts | New | 0% | Sprint 17 | Amber: not started, 105 pts plus 4 unestimated stories |
    | Member-to-Member Transfers | Mobile Banking | New | no stories yet | Sprint 20 | Amber: needs decomposing before PI 5 planning |
    | Paperless Statements & Documents | Digital Accounts | Closed | 100% | Sprint 13 | Delivered |
    | Mobile App Redesign | Mobile Banking | Closed | 100% | Sprint 11 | Delivered |

    **Top risks**

    1. **Check Deposit misses Sprint 14.** 36 points remain. One story has carried over twice, and a Priority 1 bug on the Feature has no owner.
    2. **Fraud Alerts (priority #1) will slip.** Its dependency on `Fraud Scoring Engine v2` is red on the Delivery Plan, and Mobile's confirm/deny story is already blocked waiting for Security.
    3. **Mobile Banking's quality debt.** 42 open bugs, up from 8 five sprints ago, 3 of them Critical. 11 points are waiting on a single tester, and plan completion has fallen to 71%.

    **Asks**

    - **Priya and Hannah Cole, this week:** agree a new date or a reduced scope for Check Deposit, before the sprint ends rather than after.
    - **Simone Laurent:** a decision on the Fraud Alerts dependency. Options to follow (Lab 7).
    - **Priya:** support for protecting Mobile's capacity. That means no mid-sprint intake, time reserved for bugs, and help with testing.

    *Evidence: `Shared Queries/Training/P##` queries 03, 04, 06, 10 to 12, and the Mobile Banking and Digital Accounts Velocity reports.*

<!-- SHOT: lab04-status-report | Overview › Wiki › Training › P## › Sprint Delivery Report, rendered (not edit mode), showing the overall status line, the Feature table and an embedded query-table | crop: top half of the page -->

!!! reef "Reef ahead: the watermelon"
    The easiest status to write is **Green**: most Features are Active, one closed last sprint, and one team is flawless. It's green on the outside and red on the inside. The second easiest is **Amber with no explanation**, which averages a red team and a green team into a colour that describes neither. A RAG rating is only as good as the sentence next to it. If you can't name the evidence for your colour, you've chosen a mood.

!!! insight "Lighthouse insight: a status report is a request for decisions"
    Dana doesn't need to know that charts exist. She needs to know what's true, what it means, and what you need from her. Every risk on the page should end in an ask, and every ask should name a person. A report that informs but asks for nothing hands all the risk back to you.

!!! checkpoint "Checkpoint"
    - [ ] `/Training/P##/Sprint Delivery Report` exists, with an overall RAG and a one-sentence justification
    - [ ] My Feature table includes remaining work and Target sprint, not only a percentage
    - [ ] Each of my risks has evidence, and each ask names a person

## Knowledge check

<div class="quiz" markdown>

**Mobile Banking completed 44 points in Sprint 13 and Digital Accounts completed 26. What can you conclude?**

- [ ] Mobile Banking is about 70% more productive
- [ ] Digital Accounts needs help to catch up
- [x] Nothing about relative output. Compare each team with its own plan: 71% versus 100%
- [ ] The teams should agree on a common point scale so they can be compared

<div class="quiz-why" markdown>
Story Points are a team's private yardstick. Comparing them across teams is like comparing prices in two currencies without an exchange rate. Normalizing points across teams sounds tidy, but it invites gaming (Goodhart's law) and still says nothing about value. Commitment reliability and trends within a team are the fair comparisons.
</div>

</div>

<div class="quiz" markdown>

**`Mobile Check Deposit 2.0` is 61% complete and due at the end of this sprint. What's the most useful way to report it?**

- [ ] "61% complete, progressing well"
- [x] "36 points remain with a few days left in the sprint, so it will miss. A new date or a reduced scope is needed"
- [ ] "Amber"
- [ ] "8 stories in the sprint, 2 closed"

<div class="quiz-why" markdown>
A percentage without a deadline hides the question leadership cares about: will it land? Remaining work against remaining time answers it, and naming the decision turns a status into an action.
</div>

</div>

<div class="quiz" markdown>

**Your bug trend chart over the last week shows Mobile Banking's open bugs rising by a few. Over five sprints, they've gone from 8 to 42. Which view belongs in the status report?**

- [ ] The one-week view, because it's the most current
- [ ] Neither. Bug counts are a team-level concern, not a leadership one
- [x] The five-sprint view, because the trend is the message and a short window hides it
- [ ] Whichever one Mobile Banking prefers

<div class="quiz-why" markdown>
The time window is a choice, and it decides the story. A fivefold rise in open bugs, with 3 Critical, is a delivery risk to everything Mobile touches. The window should match the question: "is quality getting worse?" needs the long view.
</div>

</div>

## Captain's log

!!! log "Captain's log"
    1. Think of the last status report you sent. Which number in it would struggle with "how do you know?"
    2. Which chart in your organization's regular reporting compares things that aren't on the same scale?
    3. What would happen if you reported Amber, with a clear sentence, when your organization expects Green?
    4. Who chooses the time windows on your team's charts? Was it a decision or a default?
    5. Which of today's charts would you actually put in front of your own leadership, and which would you leave out?

!!! bonus "Extra knots"
    1. **The PI view.** **Save as** `11` as `11b Digital stories in PI 4 (chart)` and change the iteration clause to `Iteration Path` `Under` `HarborPoint\PI 4`. Build a **Stacked bar** of `Node Name` by `State`. Which team is the only one with a Resolved segment, and what does that tell you about where its work is waiting?

    <!-- VERIFY: only Mobile Banking shows a Resolved segment for PI 4 stories (expected: its 3 Sprint 14 stories awaiting QA). -->

    2. **Who's carrying the load?** Build a flat query of Mobile Banking's **Active** user stories and bugs, then a **Bar** chart by `Assigned To`. How many active items does Ethan Brooks hold, and what does that suggest about context switching on Check Deposit?
    3. **Preview Lab 5.** On any of today's charts, open its menu and select **Add to dashboard**. It's only offered because the query is shared. Which of today's four charts would earn a place on an executive dashboard, and which wouldn't?

## Key takeaways

- Charts work only on **saved, shared, flat** queries. Plan your evidence around what Azure DevOps can draw.
- Every chart answers one question. Decide your scope (area or Epic) and say it on the page.
- Compare each team with **its own plan**, never with another team's points.
- Counts, windows and percentages can all lie. Report **what's left against the time left**, over a window that fits the question.
- A status colour is only as good as its evidence, and a status report is a request for decisions.

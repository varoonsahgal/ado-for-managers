---
title: "The Executive Status Review"
lab: 8
day: 2
module: "Module 8 · Using Dashboards to Drive Decisions"
duration: 45
sea_state: choppy
role: "Delivery Manager, Digital Banking"
summary: "Leadership is worried. Sharpen your dashboard to the indicators that matter, name the two biggest risks, and brief bottom line up front."
---

!!! briefing "Mission briefing"
    The Executive Committee meets on Thursday, and Project Lighthouse is on the agenda for the wrong reasons. Leadership has heard "delays" from three directions and wants to know whether the program is in trouble. Dana Whitfield, the program sponsor, has asked you for the short version.

    You have more evidence than you can use. Lab 5 gave you a Command Center with a dozen widgets, Lab 6 showed you which team needs help, and Lab 7 left you with an options matrix for Real-Time Fraud Alerts. None of that is a briefing yet. Executives don't need everything you know. They need the two things that matter most, the evidence behind them, and the decisions only they can make.

    **Done looks like:** a seven-widget executive dashboard where every widget earns its place, two risks you can defend against the alternatives, and a one-page bottom-line-up-front (BLUF) briefing that you can deliver in three minutes and that survives Dana's questions.

<div class="msg" data-initials="DW" data-tone="navy" markdown>
<p class="msg-head"><strong>Dana Whitfield</strong><span>EVP, Member Experience · 7:41 AM</span></p>

The Executive Committee is nervous about Lighthouse. "Delays" is all I keep hearing, and nobody can tell me which ones matter. I have ten minutes on Thursday. Priya says you have the clearest picture of Fraud Alerts and Mobile. Send me one page: are we going to make it, what are the two things that worry you most, and **what do you need me to decide?** No forty-slide decks, please.
</div>

## What you'll walk away with

- Separate the risks that threaten portfolio priorities from the noise, and defend your choice against the alternatives
- Design an executive dashboard as an argument: each widget answers a question and points at a decision
- Connect delivery metrics to member and business impact, in words an executive committee uses
- Write and deliver a one-page BLUF briefing with specific, owned asks
- Set up a weekly and monthly review rhythm that keeps the picture honest

## Before you set sail

- **Access:** Basic, as a Contributor. You can create project dashboards and edit only the ones you create.
- **From earlier labs** (each has a fallback below if you skipped it): your `P## - Digital Banking Exec View` dashboard from [Lab 5](lab-05-command-center.md), your `Features at risk` query from [Lab 3](../day-1/lab-03-query-toolkit.md), and your options page `/Training/P##/Fraud Alerts Options` and `Fraud Alerts dependencies` query from [Lab 7](lab-07-cross-team-bottleneck.md).
- **Team data you'll read but never change:** every delivery team. Your writes go to `Shared Queries/Training/P##/`, your own dashboard, and your wiki pages under `/Training/P##/`.
- **You'll create:** the dashboard `P## - METP Executive Status`, a few small queries, and the wiki page `/Training/P##/Executive Briefing`.
- **Time-box:** 45 minutes. Part 1 is 8, Part 2 is 12, Part 3 is 12, Part 4 is 7 and Part 5 is 6. If you're short on time, keep the dashboard to five widgets and protect Parts 3 and 4.

## Part 1 — Choose your two risks

Dana asked for two, not ten. Choosing is the hardest part of the job, so do it before you build anything. A dashboard built before you know your argument turns into a wall of widgets.

!!! challenge "Challenge: Triage the candidates"
    Here are seven things someone in the program has called "a delay" this week. Rank them by threat to the **portfolio priorities**, and pick the **two** you'd put in front of the Executive Committee. For each one you *don't* pick, write one line saying why.

    | Candidate | What people are saying |
    |---|---|
    | **Real-Time Fraud Alerts** | "A bit behind." 4% done, due at the PI 4 System Demo |
    | **Mobile Check Deposit 2.0** | Due at the end of this sprint, 61% done |
    | **Mobile Banking's open bugs** | "The bug count is getting silly" |
    | **Audit Evidence Automation** | Mandatory exam work, Risk `1 - High`, about half done |
    | **In-Branch Digital Onboarding** | Only 15% done |
    | **Member Support velocity** | "Their chart fell off a cliff: 18, 17, 19, then 13, then 8" |
    | **Fraud Scoring Engine v2** | Target Date moved back two sprints |

    Use any view you like: your Command Center, the Features backlogs, Velocity reports, your Lab 7 plan. Spend no more than 8 minutes. A good risk has three things: a **portfolio priority** at stake, **evidence** you can show, and a **decision** someone senior can make about it.

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Some candidates are symptoms of the same cause, so group them before you rank them. Then ask of each one: which Epic does it serve, where does that Epic rank, and would anyone above Priya have to decide something?

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    - Fraud Scoring Engine v2's slip *is* the Fraud Alerts problem. You traced it in Lab 7.
    - Check Deposit, the bug count and the falling commitment reliability all live in one team, which also owns Fraud Alerts.
    - For In-Branch Digital Onboarding, compare its **Start Date** and **Target Date** with how much is left and Branch Experience's velocity.
    - Before you believe a velocity cliff, ask what Azure DevOps counts as "completed". Open one of Member Support's past sprints and look for stories that are finished but not **Closed**.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    **Risk 1: Real-Time Fraud Alerts will miss PI 4.** It serves priority number one, *Protect every member*. It's 4% done (2 of 51 points) and due at the end of Sprint 16. Security moved the risk-score API to Sprint 16 to protect mandatory exam work, and Mobile's confirm/deny story is already `blocked` waiting for it. Fraud Scoring Engine v2's slip belongs here, as the cause. The decision is Simone's (Lab 7).

    **Risk 2: Mobile Banking's delivery health.** It threatens priority number two, *Digital that feels human*, and Fraud Alerts too, because Mobile owns it. Check Deposit is due this sprint at 61%, with 36 points left, 14 of them already planned for Sprint 15. Mobile delivered 44 of 62 planned points in Sprint 13 (71%, down from 87% five sprints ago). Open bugs rose from 8 to 42, 3 of them Critical. Three stories sit in **Resolved** waiting for the team's only tester. Check Deposit and the bug count are symptoms. The team's health is the risk.

    **Why not the others?**

    - **Audit Evidence Automation** is real and immovable, but it is being protected: Security spends 58% of its sprint on exam work. Its cost shows up in Risk 1. Keep it on the watch list.
    - **In-Branch Digital Onboarding** started in Sprint 13 and targets Sprint 17. It has 28 points left and Branch Experience has delivered 16 to 18 points every sprint. It's early, not late.
    - **Member Support's cliff** is a data problem, not a delivery problem. Finished stories were left in **Resolved**, and one Closed story has no Story Points, so velocity undercounts them. You'll prove it in [Lab 11](../day-3/lab-11-dashboard-wrong.md). Tell Dana not to act on that chart yet.

!!! reef "Reef ahead: the loudest chart in the room"
    If Member Support made your top two, you're in good company: a velocity line that drops from 19 to 8 in two sprints looks like an emergency. It isn't. The team delivered about as much as ever. It just stopped closing its stories. Put that chart in front of an Executive Committee and you trigger a rescue nobody needs, aimed at a team that, in Carmen Diaz's words, "has never worked harder." Before you escalate a trend, ask how the number is made. A risk you can't explain from the data is a question, not a risk.

!!! checkpoint "Checkpoint"
    - [ ] I picked two risks, each tied to a portfolio priority, with evidence and a decision owner
    - [ ] I wrote one line for each candidate I rejected, including why Member Support's chart isn't one of them

## Part 2 — Build the executive view

Your Lab 5 exec view was a smaller Command Center. This one is different: it's the evidence for *your* two risks, plus the program's overall health. A dashboard is an argument for a decision. Build it like one.

Here's the target. Seven widgets, each answering one question.

| # | Widget | Question it answers | Decision it informs |
|:-:|---|---|---|
| 1 | **Markdown**: the BLUF panel | What's the bottom line this week? | Everything below |
| 2 | **Query Tile**: Features at risk | How many Features need attention? | Where to look first |
| 3 | **Query Tile**: Mobile open P1 bugs | Are members hitting serious defects? | Mobile stabilization (Risk 2) |
| 4 | **Query Tile**: PI 4 committed Features closed | How much of what we promised is done? | PI 4 re-planning |
| 5 | **Chart for Work Items**: PI 4 committed Features by team and State | Where does our PI 4 commitment sit? | Which team needs a conversation |
| 6 | **Chart for Work Items**: Mobile open bugs, trend | Is quality getting better or worse? | Mobile stabilization (Risk 2) |
| 7 | **Query Results**: Fraud Alerts dependencies | Who is Fraud Alerts waiting on? | Simone's trade (Risk 1) |

Lay it out so the eye reads it in order: the BLUF panel across the top, the three tiles beneath it, then the two charts, then Fraud Alerts.

!!! speedrun "Speed run · 12 minutes"
    Create the project dashboard `P## - METP Executive Status` with the seven widgets above. Save every query in `Shared Queries/Training/P##/`. Give each tile **conditional formatting** that turns it red when the number is bad, and write your thresholds into the BLUF panel's legend. Leave the BLUF text as a placeholder; you'll write it in Part 3.

<div class="timer" data-minutes="12" data-label="Speed run"></div>

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Fastest route: open `P## - Digital Banking Exec View` and use **⋯** › **+ Copy Dashboard**, then cut it down. Query widgets accept only **shared** queries, and charts need **flat-list** queries. Query Results is the one widget here that can show a direct-links query.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    You need four flat queries, plus Lab 7's direct-links query:

    - `Features at risk` (Lab 3)
    - `Exec - Mobile open P1 bugs`: Bugs under the Mobile Banking area, not Closed, Priority 1
    - `Exec - Mobile open bugs`: the same without the Priority clause
    - `Exec - PI 4 committed Features`: Features tagged `PI4-Committed`. Tile 4 uses a copy with `State = Closed` added.

    In the Query Tile configuration, set **Default background color** to your "bad" color and add a **+ Add rule** for the good case. For the trend chart, pick a trend chart type and a rolling period that reaches back to Sprint 9.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    **1. The dashboard.** Either open `P## - Digital Banking Exec View` › **⋯** › **+ Copy Dashboard**, or go to **Overview › Dashboards** › **+ New Dashboard**. **Name** `P## - METP Executive Status`. **Dashboard Type** **Project Dashboard**. Tick **Automatically refresh the dashboard every 5 minutes**. If you copy, set **Select folder location for queries** to `Shared Queries/Training/P##`, then delete any widget that isn't in the table.

    **2. The queries.** **Boards › Queries** › **New query**, query type **Flat list of work items**. Save each in `Shared Queries/Training/P##/`.

    `Exec - Mobile open P1 bugs`:

    | And/Or | Field | Operator | Value |
    |:--|:--|:--|:--|
    | | Work Item Type | = | `Bug` |
    | And | Area Path | Under | `HarborPoint\Digital\Mobile Banking` |
    | And | State | <> | `Closed` |
    | And | Priority | = | `1` |

    **Expected result: 4.** Save, then delete the Priority clause and **Save as** `Exec - Mobile open bugs`. **Expected result: 42.**

    `Exec - PI 4 committed Features`:

    | And/Or | Field | Operator | Value |
    |:--|:--|:--|:--|
    | | Work Item Type | = | `Feature` |
    | And | Tags | Contains | `PI4-Committed` |

    **Expected result: 13.** Add `State` `=` `Closed` and **Save as** `Exec - PI 4 committed Features closed`. **Expected result: 0.**

    No `Features at risk` query from Lab 3? Build it now, flat list:

    | Group | And/Or | Field | Operator | Value |
    |:-:|:--|:--|:--|:--|
    | | | Work Item Type | = | `Feature` |
    | | And | State | <> | `Closed` |
    | ┌ | And | Target Date | <= | `@Today + 21` |
    | │ | Or | Risk | = | `1 - High` |
    | └ | Or | Tags | Contains | `at-risk` |

    **Expected result: 8** (Mobile Check Deposit 2.0, Spending Insights, Real-Time Fraud Alerts, Omnichannel Service Requests, Agent Knowledge Base, Lobby Check-In & Queue Management, Audit Evidence Automation, Unified Notification Service).

    No Lab 7 query? Build a flat list with `Parent` `=` *the ID of* `Real-Time Fraud Alerts` and columns `Title`, `State`, `Node Name`, `Iteration Path`, `Tags`. It returns its **11** stories, and you lose only the predecessor rows.

    **3. The widgets.** Select **Edit**, then add from the **Add Widget** pane. Select **Done Editing** when you're finished.

    | Widget | Configuration |
    |---|---|
    | **Markdown** | Width 6 (or wider), placeholder text for now |
    | **Query Tile** `Features at risk` | **Default background color** amber. Rule: **If number of work items** `<=` `3`, green |
    | **Query Tile** `Mobile open P1 bugs` | Default red. Rule: `<=` `0`, green |
    | **Query Tile** `PI 4 Features closed` | Default neutral grey, no rule (see the reef below) |
    | **Chart for Work Items** | Query `Exec - PI 4 committed Features`, **Chart type** **Stacked bar**, rows by `Node Name`, stacked by `State` |
    | **Chart for Work Items** | Query `Exec - Mobile open bugs`, **Chart type** **Stacked area** (trend), series by `State`, a rolling period of about 12 weeks |
    | **Query Results** | Query `Fraud Alerts dependencies` (Lab 7) |

    <!-- VERIFY: Query Tile conditional-formatting operators beyond <= and the evaluation order when several rules match; Stacked bar field labels in the Chart for Work Items widget; the exact rolling-period options for trend charts (need one that reaches Sprint 9, about 12 weeks back); whether the dashboard settings entry point is ⋯ > Dashboard settings or a gear. -->

    **Expected result:** the tiles read **8**, **4** and **0**. The stacked bar shows **13** committed Features across six teams: Mobile Banking 3, and Digital Accounts, Security, Core Platform, Branch Experience and Member Support 2 each. All are **Active** except one **New** Feature in Member Support. The bug trend climbs from single digits in Sprint 9 to **42**.

    <!-- VERIFY: the query trend chart reflects the back-dated seed history (open Mobile bugs rising from 8 to 42 across Sprints 9 to 14). If it shows a flat line from the seeding date, fall back to the Velocity widget for Mobile Banking with "Display planned work for iterations" on. -->

<!-- SHOT: lab08-tile-rules | Query Tile Configuration panel for Exec - Mobile open P1 bugs: Default background color red, one Conditional formatting rule "If number of work items <= 0" green | crop: configuration panel; highlight the rule row -->

Look at the stacked bar before you move on. One Member Support Feature is still **New**, although its team is building it right now. That's another data problem, and another reason not to read Member Support's numbers at face value until Lab 11.

!!! reef "Reef ahead: a number with no baseline"
    "Zero of 13 committed Features closed" sounds like a fire. It isn't, on its own. PI 4 is four sprints long and you're halfway through the second, and Features usually close near their Target Dates. The tile is useful only next to *when* each Feature is due: Check Deposit was due this sprint and won't close, which matters. The other 12 aren't due yet. That's why tile 4 has no red rule. An executive tile without a baseline or a target invites the wrong conversation. Give every number a comparison: against plan, against last month, or against a threshold you wrote down.

!!! insight "Lighthouse insight: a dashboard is an argument for a decision"
    A Command Center helps you *find* problems, so it can afford twelve widgets. An executive view helps someone *decide*, so every widget must point at a question and a decision, and anything that doesn't gets cut. Test each widget with one question: "If this number changed tomorrow, would Dana do anything differently?" If the answer is no, it belongs on your Command Center, not here. More charts don't make a dashboard more credible. Fewer, sharper charts with written thresholds do.

!!! checkpoint "Checkpoint"
    - [ ] `P## - METP Executive Status` has at most seven widgets, each tied to a question in the table
    - [ ] My tiles read 8, 4 and 0, and two of them change color at a threshold I wrote down
    - [ ] Fraud Alerts' dependencies are visible without leaving the dashboard

## Part 3 — Write the BLUF

**Bottom line up front** means the answer comes first and the supporting detail comes after it, in order of importance. An executive should be able to stop reading after the first two sentences and still know what to do.

Before you write, translate. The Executive Committee doesn't think in Story Points. Connect each indicator to what it means for members and for HarborPoint.

!!! challenge "Challenge: From metric to member"
    Complete one line per indicator. The middle column is the hard one.

    | Indicator on your dashboard | What it means for members and the business | Decision it supports |
    |---|---|---|
    | Fraud Alerts 4% done, API in Sprint 16 | | |
    | Mobile open bugs 42, 3 Critical, 4 at P1 | | |
    | Mobile delivered 71% of plan | | |
    | Check Deposit misses its sprint | | |

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Think about what members experience, not what teams experience. Who is exposed while a Feature isn't live? Who meets a defect? Which promise to the Executive Committee does a number put at risk?

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    About 45% of the Mobile bugs created since Sprint 11 are tagged `escaped-defect`: members found them in production. Fraud Alerts is how members will learn within seconds that a transaction looks wrong. A 71% delivery rate means that any date built on Mobile's plan is about 30% optimistic.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    | Indicator | Member and business meaning | Decision |
    |---|---|---|
    | Fraud Alerts 4% done, API in Sprint 16 | Every sprint without it is another sprint in which members find out about fraud from their statement, not from their phone. It is priority number one and a committed PI 4 objective | Simone's trade, or a formal date move |
    | 42 open Mobile bugs, 3 Critical, 4 at P1 | Members are hitting defects in production, including a deposit failure on large check images that nobody owns yet. Each one costs trust and support calls | Mobile stabilization |
    | 71% of plan delivered | Every Mobile date is about 30% optimistic, including Fraud Alerts' integration work | Stop mid-sprint intake, re-plan honestly |
    | Check Deposit misses the sprint | A visible miss on priority number two. On its own it's small. As a pattern it's the story of the team | Re-plan its Target Date with Hannah |

Now write. Open **Overview › Wiki** › `Templates` › `Executive Briefing (BLUF)` and copy its contents. Create a sub-page `Executive Briefing` under your `/Training/P##` page, paste, and fill it in. Keep it to one page.

<!-- VERIFY: label of the wiki page menu action for adding a sub-page (e.g., "Add sub-page"), and the headings in /Templates/Executive Briefing (BLUF). The brief below should map onto them; if the template's order differs, follow the template. -->

!!! deliverable "Deliverable"
    `/Training/P##/Executive Briefing`, one page, with:

    1. **Bottom line** in two sentences or fewer: are we going to make it, and what do you need?
    2. **The two risks**, each with three lines of evidence and its member impact
    3. **Options** for each risk, short (link your Lab 7 options page for detail)
    4. **Recommended actions**, each with an owner
    5. **Decisions needed**, each naming the decider: Dana, Simone, or both
    6. **What I'll watch next week**, as measurable signals
    7. A link to `P## - METP Executive Status`

    Then paste your two-sentence bottom line, the decisions needed and your thresholds legend into the dashboard's **Markdown** widget, with "Updated: Sprint 14, week 2" at the top.

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Write the bottom line last, then move it to the top. Each decision should be something one person can say yes or no to. "Support for Mobile" is not a decision. "Approve no mid-sprint intake for Mobile for two sprints" is.

??? pilot "Harbor Pilot · Hint 2: Set the heading (model briefing)"
    > **Bottom line.** PI 4 will not deliver Real-Time Fraud Alerts, our number one priority, unless Simone makes one trade this week. Mobile Banking, which owns it, is overloaded and losing ground on quality, and I need Dana's backing for two sprints of stabilization.
    >
    > **Risk 1: Real-Time Fraud Alerts will miss PI 4.** It's 4% done and due at the PI 4 System Demo (end of Sprint 16). Security moved the risk-score API to Sprint 16 to protect mandatory exam work, and Mobile's confirm/deny screen is built but `blocked` until it arrives. Security spends 58% of this sprint on exam work, and the Compliance Epic is still ranked last of six. *Member impact:* every sprint without it, members learn about fraud from their statement, not their phone.
    >
    > **Risk 2: Mobile Banking's delivery health.** Mobile Check Deposit 2.0 misses its Sprint 14 date at 61%, with 14 of its remaining 36 points already planned for Sprint 15. Mobile delivered 44 of 62 planned points last sprint (71%, down from 87%), and open bugs rose from 8 to 42, including 3 Critical and an unowned P1. Three finished stories wait for the team's only tester. *Member impact:* defects reach members, and every Mobile date, including Fraud Alerts' integration, is about 30% optimistic.
    >
    > **Options.** For Fraud Alerts: pull the API into Sprint 15 by deferring 8 to 10 points of Adaptive MFA work, ship a smaller MVP (alerts plus confirm/deny) in PI 4, borrow Core Platform capacity, or move the date to Sprint 17. Detail: *Fraud Alerts Options*. For Mobile: stop mid-sprint intake, reserve capacity for bugs, add or borrow test capacity, and re-plan Check Deposit honestly.
    >
    > **Decisions needed.**
    > 1. **Simone, this week:** pull the risk-score API into Sprint 15 and hold Sprint 16 for the MVP, *or* move Fraud Alerts to Sprint 17 now. Both sides of the trade are your priorities.
    > 2. **Dana:** approve two sprints of Mobile stabilization: no mid-sprint intake, including marketing requests, and temporary test capacity.
    > 3. **Simone, with the Executive Committee:** rank the Compliance Epic where reality has it, or reserve Security capacity for it through Sprint 18.
    >
    > **I'll watch next week:** the risk-score API's sprint; whether the confirm/deny story is still `blocked`; Mobile's open Critical bugs and the size of the Resolved queue; Mobile's Sprint 14 delivered-versus-planned; Check Deposit's new Target Date.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (Markdown panel)"
    The panel is the BLUF in miniature. The widget renders CommonMark only, so no HTML.

    ```markdown
    ## METP Executive Status · Updated: Sprint 14, week 2
    **Bottom line:** Fraud Alerts (priority 1) misses PI 4 unless Simone makes one trade this week.
    Mobile Banking needs two sprints of stabilization.

    **Decisions needed:** (1) Simone: API into Sprint 15 or Fraud Alerts to Sprint 17.
    (2) Dana: no mid-sprint intake for Mobile, plus temporary test capacity.

    **Thresholds:** at-risk Features green at 3 or fewer · Mobile P1 bugs green at 0 ·
    PI 4 closed: read against Target Dates

    [Full briefing](<paste your Executive Briefing page URL>) · [Fraud Alerts options](<paste URL>)
    ```

<!-- SHOT: lab08-exec-dashboard | Overview › Dashboards › P## - METP Executive Status with all seven widgets: BLUF Markdown panel across the top, tiles reading 8 / 4 / 0, PI 4 committed Features stacked bar, Mobile open bugs trend, Fraud Alerts dependencies Query Results | full dashboard; highlight the BLUF panel and the red P1 tile -->

<!-- SHOT: lab08-bluf-page | Overview › Wiki › Training › P## › Executive Briefing, filled in, showing the Bottom line and Decisions needed sections | crop: page body top half -->

!!! reef "Reef ahead: RAG without evidence"
    "Overall status: Amber" tells an executive nothing they can act on, and a colour picked by feel invites the watermelon: green outside, red inside. If your briefing has a RAG, attach the evidence and the rule that set it: "Red, because a committed PI 4 objective cannot land by its date without a decision." Better still, lead with the decision, because that's what Dana is reading for.

!!! checkpoint "Checkpoint"
    - [ ] My briefing's first two sentences answer "are we going to make it?" and "what do you need?"
    - [ ] Each risk has three lines of evidence and a member impact
    - [ ] Every decision names one decider and can be answered yes or no
    - [ ] The dashboard's Markdown panel carries the bottom line, the decisions and the thresholds

## Part 4 — Survive Dana's questions

A briefing is tested by its questions. Pair up. One of you is Dana, the other briefs. Three minutes for the briefing, then Dana draws two cards. Swap roles.

!!! challenge "Challenge: Dana's question cards"
    Dana picks any two. Answer each in under 30 seconds, using your dashboard or one click from it.

    1. **"Are we going to make it?"** Yes or no first, then the condition.
    2. **"How do you know?"** Show the evidence, not your opinion of it.
    3. **"What happens if we do nothing?"**
    4. **"Why didn't we know sooner?"**
    5. **"If I give you one more engineer, what changes?"**
    6. **"I saw Member Support's chart. Aren't they the real problem?"**

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Each card is testing something: a straight answer (1), evidence (2), the cost of not deciding (3), the system behind the miss (4), the limits of adding people (5), and whether you fell for the trap (6).

??? pilot "Harbor Pilot · Hint 2: Bring it into port (model answers)"
    1. "Not as planned. Fraud Alerts makes PI 4 only if the risk-score API moves into Sprint 15. That's Simone's call this week."
    2. "Aisha's Target Date change and her comment on Fraud Scoring Engine v2, the blocked confirm/deny story, and Security's sprint: 21 of 36 points on exam work. It's all in the tile and the dependency list."
    3. "The API lands in Sprint 16, Mobile integrates and tests it after that with one tester, and we find out at the System Demo that our number one priority slipped into PI 5."
    4. "The re-plan was recorded on one work item, and nothing downstream moved: Fraud Alerts kept its date and its `PI4-Committed` tag. Nobody was forced to decide, because the Compliance Epic was never ranked. That's decision 3."
    5. "In Security, not much this PI: a new engineer needs weeks to be productive and slows the team at first. In Mobile, a tester helps faster than a developer, because finished work is queuing for QA. Trades beat headcount here."
    6. "No. Their delivery is steady at about 18 points a sprint. The drop is finished work left in Resolved and a missing estimate. We're checking the data this week, and I wouldn't act on that chart yet."

!!! checkpoint "Checkpoint"
    - [ ] I delivered my briefing in three minutes or less
    - [ ] I answered two of Dana's cards from the dashboard or one click away
    - [ ] I changed at least one line of my briefing because of a question

## Part 5 — Set the review rhythm

A briefing is a snapshot. Dana's next question will be "and next week?" Ruth's Program Charter lists the program's governance cadence, but a cadence on a wiki page doesn't keep a dashboard honest. A review with an owner, a time-box and a fixed agenda does.

!!! challenge "Challenge: Design two reviews, 30 minutes each"
    Design a **weekly delivery review** and a **monthly steering review**. For each: who attends, which dashboard and queries, the agenda, and what comes out of it. Each must fit in 30 minutes.

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    The two reviews answer different questions. Weekly asks "what changed and what's stuck?" for the people who can act this sprint. Monthly asks "are we still working on the right things?" for the people who own the priorities.

??? pilot "Harbor Pilot · Hint 2: Bring it into port (a model design)"
    | | Weekly delivery review | Monthly steering review |
    |---|---|---|
    | **Purpose** | Unblock and re-plan inside the PI | Decide trade-offs between priorities |
    | **Who** | You, Ruth, the six Product Owners or leads; Aisha and Hannah for cross-team items | Dana, Simone, Priya, Carmen, Hector, Marcus, Nadia, Ruth |
    | **Looks at** | `P## - Digital Banking Command Center`, `Features at risk`, `Fraud Alerts dependencies`, open P1 bugs, your Delivery Plan | `P## - METP Executive Status`, the PI Objectives page, the Epic backlog order |
    | **Agenda** | 5 min: what changed since last week (dates, tags, scope). 15 min: red items and blocked dependencies, each leaving with an owner. 10 min: escalations to monthly | 5 min: BLUF. 15 min: the two or three decisions, with options. 10 min: priorities, rank and capacity across Epics |
    | **Output** | Updated dates and tags in Azure DevOps, a refreshed BLUF panel, an escalation list | Recorded decisions, an updated Epic rank, changes to PI objectives |
    | **Rule** | If a date moved in Azure DevOps, the dependent dates move in the same meeting | No decision without options and a named owner |

    The rule in the last row is the lesson of Lab 7. The re-plan that hurt Fraud Alerts was visible in one work item for days, and nobody's review was looking at it.

!!! insight "Lighthouse insight: a dashboard decays unless someone owns it"
    A stale dashboard is worse than no dashboard, because people trust it. Give every executive view an owner, a weekly refresh of its Markdown panel with the date at the top, and a place in a recurring review. If the BLUF panel still says "Sprint 14" in Sprint 16, the dashboard is telling the Executive Committee something false in your name.

!!! checkpoint "Checkpoint"
    - [ ] My weekly and monthly reviews each have attendees, views, a 30-minute agenda and an output
    - [ ] At least one rule in my design would have caught the Fraud Scoring Engine v2 re-plan within a week

## Knowledge check

<div class="quiz" markdown>

**Member Support's velocity chart reads 18, 17, 19, 13, 8. What belongs in your executive briefing?**

- [ ] Member Support as risk 2: delivery has collapsed and needs intervention
- [ ] Nothing at all: it's Carmen's problem, not the program's
- [x] At most a line saying the drop is being checked as a data issue, with no action requested yet
- [ ] A request for Dana to add engineers to Member Support

<div class="quiz-why" markdown>
Velocity counts only **Closed** stories. Member Support left finished work in **Resolved** and missed an estimate, so the chart undercounts real delivery, which has stayed at about 18 to 19 points. Escalating an unverified trend aims leadership at the wrong problem. Mentioning it briefly gets ahead of the question, because Dana may well have seen the chart.
</div>

</div>

<div class="quiz" markdown>

**Which "decision needed" is written best?**

- [ ] "Leadership support for Fraud Alerts"
- [ ] "Security to prioritize Fraud Alerts"
- [x] "Simone: pull the risk-score API into Sprint 15 by deferring 8 to 10 points of Adaptive MFA work, or move Fraud Alerts to Sprint 17 now"
- [ ] "Approval to escalate the Fraud Alerts dependency"

<div class="quiz-why" markdown>
A good ask names one decider, offers a choice they can say yes or no to, and states its cost. The other three are requests for sympathy. They leave the real decision with a team that doesn't own both priorities.
</div>

</div>

<div class="quiz" markdown>

**Your executive dashboard has a tile reading "PI 4 committed Features closed: 0". What should you do with it?**

- [ ] Colour it red: nothing has been delivered
- [x] Show it next to when those Features are due, and call out only the ones already past their Target Date
- [ ] Remove it: executives don't need delivery counts
- [ ] Replace it with velocity, which shows the work being done

<div class="quiz-why" markdown>
Features close near their Target Dates, and most PI 4 Features aren't due yet. A count with no baseline creates a false alarm or, worse, false comfort. The honest signal is "one committed Feature, Mobile Check Deposit 2.0, is due this sprint and won't close."
</div>

</div>

## Captain's log

!!! log "Captain's log"
    1. Look at the last status report you sent upward. Could the reader find the decision you needed in the first two sentences?
    2. Which chart in your organization gets the most attention in leadership meetings? How is its number made, and when did someone last check?
    3. Name one widget on a dashboard you own that wouldn't change any decision if its number changed. Why is it still there?
    4. When a date moves in one team's backlog, which review in your organization is designed to notice it?
    5. Which decision is your sponsor not making because nobody has framed it as a choice with costs?

!!! bonus "Extra knots"
    1. **The 30-second test, executive edition.** Give your dashboard to someone who hasn't seen it. Can they tell you the bottom line and the two decisions in 30 seconds without your help? If not, what would you cut?
    2. **Trend the right thing.** Mobile's open bug count is a lagging signal. Add a Velocity widget for `Mobile Banking` with **Display planned work for iterations** on, and compare Planned with Completed across five sprints. Is the reliability trend a better early warning than the bug trend? Would you swap it in for one of your seven widgets?
    3. **Write Marcus's version.** Marcus Reed, the CIO, will ask "how do you know?" about every number. Add a short "Evidence" section to your briefing that links each claim to the query or work item behind it.

## Key takeaways

- Choose the argument before you build the dashboard. A good risk has a priority at stake, evidence, and a decision someone senior can make.
- An executive dashboard is an argument for a decision: few widgets, each tied to a question, each number with a threshold or a baseline.
- Translate metrics into member impact. "42 open bugs" means little to an Executive Committee. "Members are finding defects in production" means a great deal.
- Bottom line up front: the answer and the ask first, evidence second, every decision owned by one named person.
- Check how a number is made before you escalate it. The loudest chart in the room is often a data problem.

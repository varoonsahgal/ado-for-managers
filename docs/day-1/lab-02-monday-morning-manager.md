---
title: "The Monday Morning Manager Challenge"
lab: 2
day: 1
module: "Module 2 · Understanding What Teams Are Working On"
duration: 50
sea_state: choppy
role: "Delivery Manager, Digital Banking"
summary: "You're back from leave and mobile banking is behind. Build a Feature-level readout of what each team is doing, what shipped, and what needs you, before 10 a.m."
---

!!! briefing "Mission briefing"
    You took a week of leave you'd booked before you accepted the job. You're back, it's Sprint 14, week 2, and your inbox has 140 unread messages. One of them matters.

    Dana, the EVP, asked Priya why mobile banking has fallen behind, and Priya needs an answer by ten. Not a story-by-story tour, and not an opinion: a Feature-level picture she can repeat to Dana. Every claim needs evidence you can show when Marcus asks "how do you know?"

    **Done looks like:** five bottom-line-up-front bullets on a wiki page, each backed by a view or a query you can open in ten seconds.

<div class="msg" data-initials="PR" data-tone="teal" markdown>
<p class="msg-head"><strong>Priya Raman</strong><span>Director, Digital Banking · 7:41 AM</span></p>

Welcome back. Bad timing, sorry. Dana stopped me last night: "Why has mobile banking fallen behind?" I need a readout from you at **10:00**. What each team is working on, what we shipped last sprint, what's unfinished, and what needs us. Feature level please, I don't need the story-by-story. Five bullets. If something's on fire, lead with it.
</div>

## What you'll walk away with

- Read any team's current workload at **Feature** level in minutes, across six teams
- Separate what a team *completed* from what it *planned*, and know where carry-over hides
- Judge whether a Feature will make its date from the evidence, not from its progress bar
- Run a fast **signals hunt** for the things that need a manager: unowned urgency, overload, stale work, scope creep, unaligned effort and quality debt
- Write a status readout that leads with the bottom line and asks for something specific

## Before you set sail

- **You'll read:** `Mobile Banking` and `Digital Accounts` closely, and the other four teams briefly. All read-only.
- **You'll create:** scratch queries in **My Queries** (your private folder; the shared `P##` folder comes in Lab 3), and one wiki page, `/Training/P##/Monday Readout`.
- **Shared queries are shared.** You'll add columns to a query in `Shared Queries/HarborPoint Reports`. Don't **Save** it; use **Save as** into **My Queries** if you want to keep your version.
- **Team context matters today.** Every sprint view, Velocity report and `@CurrentIteration` clause belongs to one team. When a step names a team, check the team selector before you read a number.
- **Time-box:** 50 minutes. Protect the last 10 for the readout. Five honest bullets beat twelve thorough ones delivered at 10:20.

## Part 1 — Who's on what, right now

Start wide. Before you explain one team, know what all six are doing.

!!! speedrun "Speed run · 8 minutes"
    For each of the six delivery teams, list the **Features** its Sprint 14 stories serve, and how much of the sprint serves **no Feature at all**. Ignore bugs for now. One line per team.

<div class="timer" data-minutes="8" data-label="Speed run"></div>

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    You don't need six sprint boards. There's a shared query that already lists the current sprint for every team. It just doesn't show the one column you need.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    Open **Boards › Queries** › **All** › `Shared Queries/HarborPoint Reports/Program - Current sprint (all teams)`. **Column options**: add `Parent`, `Node Name` and `Story Points`. Use the results **Filter** to show only **User Story** under **Work Item Types**. Sort by `Node Name`: you can't sort by Parent, but within each team the parent titles are easy to scan. Don't save over the shared query.

    The slower route: **Boards › Sprints**, pick each team, `Sprint 14`, **Backlog** tab, **Column Options** › add `Parent`.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    | Team | Features this sprint (stories, points) | Serving no Feature |
    |:--|:--|:--|
    | Mobile Banking | Mobile Check Deposit 2.0 (8, 29) · Biometric Login (3, 11) · Real-Time Fraud Alerts (3, 13) | **5 stories, 12 points** |
    | Digital Accounts | Online Account Opening (5, 17) · Spending Insights (3, 7) | 1 story, 2 points |
    | Security | Audit Evidence Automation (4, 14) · Access Review Automation (2, 7) · Fraud Scoring Engine v2 (2, 7) · Adaptive Multi-Factor Authentication (2, 8) | none |
    | Core Platform | Unified Notification Service (3, 6) · Member API Gateway (2, 8) · Real-Time Fraud Alerts (1, 5) | 1 story, 3 points |
    | Branch Experience | In-Branch Digital Onboarding (3, 10) · Lobby Check-In & Queue Management (3, 7) | 1 story, 2 points |
    | Member Support | Omnichannel Service Requests (5, 13) · Secure Messaging & Chat (3, 10) | none |

    Three things a manager should notice in that table, even before looking at Mobile:

    - **Security has four Features in flight** with six people, and 21 of its 36 points go to the two Compliance Features.
    - **Real-Time Fraud Alerts appears twice**, in Mobile Banking and Core Platform, but has no Security story this sprint, though Security owns part of it.
    - **Member Support has `Service request status tracker` twice**: one Active, one New and unassigned. That's a duplicate, and it double-counts scope. (Day 3 has a whole lab on Member Support's data.)

<!-- SHOT: lab02-current-sprint-by-feature | Boards › Queries › Shared Queries/HarborPoint Reports/Program - Current sprint (all teams), Results tab, columns Parent, Node Name, Story Points added, filter Work Item Types = User Story, sorted by Node Name | crop: the Mobile Banking rows; highlight the rows with an empty Parent cell -->

!!! checkpoint "Checkpoint"
    - [ ] I have one line per team: its Sprint 14 Features and its unaligned work
    - [ ] I noted at least one thing outside Mobile Banking worth a question

## Part 2 — What shipped in Sprint 13

"Fallen behind" is a claim about the past. Check the last sprint first.

**What was delivered at Feature level.** Open `Shared Queries/HarborPoint Reports/Portfolio - Features by target date`. Add `Closed Date` and `Node Name` as columns (don't save). One Feature closed in Sprint 13: **`Paperless Statements & Documents`**, Digital Accounts. Mobile Banking closed no Features last sprint. Its last delivery was `Mobile App Redesign`, at the end of Sprint 11.

**Planned against completed.** Now compare each team with its own plan.

1. **Boards › Backlogs**, team `Mobile Banking`, level **Stories**, then the **Analytics** tab.
2. On the **Velocity** card, select **View full report**. Set **Velocity by** to Story Points if it isn't already, and keep **Last 6 iterations**.
3. Hover over the Sprint 13 bars. Then switch the team selector to `Digital Accounts` and do the same.

<!-- SHOT: lab02-mobile-velocity | Boards › Backlogs › Analytics › Velocity full report, team Mobile Banking, Stories level, Velocity by Sum of Story Points, Last 6 iterations | crop: chart and legend; highlight Sprint 13 Planned 62 vs Completed 44 -->

**You should see:**

| Team | Sprint 13 planned | Sprint 13 completed | Share of plan |
|:--|:-:|:-:|:-:|
| Mobile Banking | 62 | 44 | **71%** |
| Digital Accounts | 26 | 26 | 100% |

Mobile's gap of 18 points is six stories that weren't finished and moved into Sprint 14 on its first day. Velocity shows the gap between **Planned** and **Completed**. To see one carried story's journey, open `Auto-capture check edges with on-device ML` and select **History**: its **Iteration Path** moved from Sprint 12 to Sprint 13, then from Sprint 13 to Sprint 14. It has been "nearly done" for three sprints.

<!-- VERIFY: whether Mobile's Sprint 13 bar shows the carried items as "Incomplete" (the docs say Incomplete counts items still in the sprint; these were moved to Sprint 14) or only as the Planned − Completed gap. Text above works either way. -->

!!! note "Why not just query for carry-over?"
    The query editor's **Was Ever** operator doesn't support **Iteration Path**, so "stories that were ever in Sprint 12" isn't a query you can build there. Use the **Velocity** report for the size of the gap and each item's **History** for the evidence.

!!! challenge "Challenge: Two teams, one verdict"
    Mobile Banking completed 44 points last sprint. Digital Accounts completed 26. A colleague says, "So Mobile delivered 70% more than Digital Accounts." Write a one-line reply, and say which team had the better sprint.

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    What is a Story Point a unit *of*? Is a Mobile point the same size as a Digital Accounts point?

??? pilot "Harbor Pilot · Hint 2: Bring it into port (full solution)"
    *"Points are each team's own yardstick, so you can't add or compare them across teams. Compare each team with its own plan: Digital Accounts delivered 100% of what it committed and closed a Feature, Mobile delivered 71% and carried six stories."* Digital Accounts had the better sprint. Each team's velocity is useful for forecasting **that team's** work and nothing else. Day 2 has a full lab on why the "faster" team here is the one that needs help.

!!! checkpoint "Checkpoint"
    - [ ] I can name the Feature that closed in Sprint 13, and Mobile's last delivered Feature
    - [ ] I have Mobile's and Digital Accounts' Sprint 13 planned and completed points
    - [ ] I found the story that has carried over twice, and the History that proves it

## Part 3 — What's unfinished, Feature by Feature

Now the question Dana actually asked. Look at Mobile Banking through its Features first.

1. **Boards › Backlogs**, team `Mobile Banking`, level **Features**. **View options**: **In Progress Items** On, **Completed Child Items** On.
2. **Column Options**: make sure you have `Target Date`, `Tags`, **Progress by Story Points** and **Sum of Story Points**. Column choices are per backlog, so the ones you set on `Digital Portfolio` in Lab 1 may not be here.

**You should see** three Features in flight and one not started:

| Feature | Due | Progress (points) | Left | Tags |
|:--|:--|:-:|:-:|:--|
| `Mobile Check Deposit 2.0` | end of **Sprint 14** | 61% | 36 points | `PI4-Committed` `at-risk` |
| `Biometric Login` | end of Sprint 16 | 53% | 24 points | `PI4-Committed` `cross-team` |
| `Real-Time Fraud Alerts` | end of Sprint 16 | **4%** | 49 points | `PI4-Committed` `cross-team` |
| `Member-to-Member Transfers` | end of Sprint 20 | *(no children)* | | `PI5-Candidate` |

`Mobile Check Deposit 2.0` is due in a few working days. Your first job is to decide whether it will make it.

!!! challenge "Challenge: Will Mobile Check Deposit 2.0 make it?"
    Give a yes or no, and three pieces of evidence that would convince Marcus. Stay at Feature level, and drop to stories only for the evidence.

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    61% says nothing about time. Ask where the remaining 36 points *are*: which sprint they're planned in, what state they're in, and who has them.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    Expand `Mobile Check Deposit 2.0` on the Features backlog and add `Iteration Path`, `State`, `Assigned To` and `Story Points` columns. Compare the remaining points with how much Mobile has completed so far this sprint (the Sprint 14 bar on the Velocity report).

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    **No.** The evidence:

    1. **The team's own plan already says no.** Of the 36 points left, **14 are scheduled for Sprint 15**, after the Feature's Target Date: `Endorsement guidance animation`, `Deposit hold explanations` and `Multiple checks in one deposit session`. Nobody moved the date.
    2. **What's left in Sprint 14 isn't moving.** The other 22 points sit in six stories: two Active but untouched for over a week (both with Ethan Brooks), one Active, one Resolved and waiting for the only tester, and two not started, one of them unassigned. Mobile has closed 12 points across *all* its work so far this sprint.
    3. **There's a Priority 1 bug on it that nobody owns.** `Check deposit fails for images larger than 5 MB`, filed this sprint, is a child of this Feature. A Feature with an open P1 escaped defect isn't done, whatever the bar says.

    **So what?** The miss isn't news to the team, but it is news to the portfolio: the Feature is still due this sprint, still `PI4-Committed`, and the only warning is a tag. The manager's move is to re-forecast **now**, and offer Priya a choice: move the Target Date, or ship what's done and split the three Sprint 15 stories into a follow-up.

<!-- SHOT: lab02-f2-children-iterations | Boards › Backlogs, team Mobile Banking, Features level, Mobile Check Deposit 2.0 expanded, columns Iteration Path, State, Assigned To, Story Points | crop: the expanded children; highlight the three Sprint 15 stories and the two unassigned or New stories in Sprint 14 -->

**The other two in-flight Features, in one line each:**

- **`Biometric Login`** is roughly on track. 24 points are left with two and a half sprints to go, but 8 of them are finished and waiting in **Resolved** for testing. One story belongs to Security, in Sprint 15. The risk here is the test queue, not the build.
- **`Real-Time Fraud Alerts`** is the one that should worry you most, because it serves priority number one. Open **Boards › Delivery Plans** › `HarborPoint Program Plan` and find its card in the Mobile Banking row. The chain-link badge on the card is **red**. Select it: its predecessor, `Fraud Scoring Engine v2` (Security), now ends in Sprint 17, a sprint after Fraud Alerts is due. In Mobile's sprint, `Member confirms or denies a flagged transaction` is tagged `blocked`, and its Discussion says *"UI done; can't integrate until Security's risk-score API exists."* Note it and move on. You'll take this apart on Day 2 in [Lab 7](../day-2/lab-07-cross-team-bottleneck.md).

<!-- SHOT: lab02-program-plan-f9-badge | Boards › Delivery Plans › HarborPoint Program Plan, Mobile Banking and Security rows at Features level, Dependencies dialog open from the red badge on Real-Time Fraud Alerts | crop: the card with its red badge plus the dialog; highlight Fraud Scoring Engine v2 ending in Sprint 17 -->

**One level down: where the work is waiting.** **Boards › Boards**, team `Mobile Banking`, level **Stories**. The **Resolved** column holds three stories (11 points) alongside some Resolved bugs, all waiting for Ava Patel, the team's only QA engineer: `Deposit limit messaging by member tier` (6 days), `Face ID and fingerprint enrollment` (5 days) and `Biometric step-up for high-risk actions` (2 days). Finished code that nobody can test is inventory, not progress.

!!! checkpoint "Checkpoint"
    - [ ] I have a yes/no on `Mobile Check Deposit 2.0` with three pieces of evidence
    - [ ] I saw the red dependency badge on `Real-Time Fraud Alerts` and know which Feature it waits on
    - [ ] I know how many finished stories are waiting for testing, and who they're waiting for

## Part 4 — What needs you

A manager's Monday is about the handful of items that won't fix themselves. Six signals usually find them.

!!! challenge "Challenge: The signals hunt"
    For **Mobile Banking**, find the evidence for each signal below. Build each one as a quick query and save it in **My Queries** as `Scratch - <signal>`, so you can open it in front of Priya. Record the count, the item or person that matters, and the Feature it puts at risk. The stories are evidence; the Feature is the message.

    | # | Signal | What you're looking for |
    |:-:|:--|:--|
    | A | Urgency nobody owns | Open Priority 1 bugs with no one assigned |
    | B | One person holding too much | Who has the most Active items |
    | C | Work nobody has touched | Active items unchanged for over a week |
    | D | Work that arrived after planning | This sprint's items tagged `unplanned` |
    | E | Effort that serves no Feature | Last sprint's completed stories with no parent |
    | F | Quality debt | Open bugs in total, and how bad |

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Every query starts with the same clause: **Area Path** **Under** `HarborPoint\Digital\Mobile Banking`. After that, each signal is one or two more clauses on **Priority**, **Assigned To**, **State**, **Changed Date**, **Iteration Path**, **Tags** or **Parent**.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    - **A:** Bug, Priority 1, not Closed; add the `Assigned To` column and look for blanks.
    - **B:** State Active; **Column options** › **Sorting** by `Assigned To`.
    - **C:** State Active and **Changed Date** `<` `@Today - 7`.
    - **D:** **Iteration Path** `=` `@CurrentIteration` with team `Mobile Banking`, and **Tags** **Contains** `unplanned`.
    - **E:** User Story, State Closed, **Iteration Path** `=` `@CurrentIteration - 1` with team `Mobile Banking`; add `Parent` and `Story Points` columns.
    - **F:** Bug, not Closed; add `Severity` and `State` columns.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    **Boards › Queries** › **New** › **New query**. **Query type**: **Flat list of work items** for all six. Each starts with:

    | And/Or | Field | Operator | Value |
    |:--|:--|:--|:--|
    | | Area Path | Under | `HarborPoint\Digital\Mobile Banking` |

    Then add the clauses below, run, and save to **My Queries**.

    **A · Urgency nobody owns**

    | And/Or | Field | Operator | Value |
    |:--|:--|:--|:--|
    | And | Work Item Type | = | `Bug` |
    | And | Priority | = | `1` |
    | And | State | <> | `Closed` |

    Columns: `Assigned To`, `Parent`, `Severity`, `Tags`. **4** open P1 bugs. One has no owner: `Check deposit fails for images larger than 5 MB`, parent `Mobile Check Deposit 2.0`, tagged `escaped-defect`, filed on day 2 of this sprint.

    <!-- VERIFY: the generated Mobile P1 bugs are all assigned, so "Check deposit fails for images larger than 5 MB" is the only unassigned row. -->

    **B · One person holding too much**

    | And/Or | Field | Operator | Value |
    |:--|:--|:--|:--|
    | And | State | = | `Active` |

    **Column options** › **Sorting**: `Assigned To`. **Ethan Brooks** has **6** Active items: four stories (`Auto-capture check edges with on-device ML`, `Retry flow for failed check uploads`, `Endorsement detection on check back`, `Holiday promo banner (marketing request)`) and two bugs (`App crashes when switching accounts during deposit`, `Deposit confirmation email shows wrong amount`). They split between `Mobile Check Deposit 2.0` and work with no Feature at all.

    <!-- VERIFY: no other Mobile Banking person has as many Active items once generated bugs are assigned. -->

    **C · Work nobody has touched**

    | And/Or | Field | Operator | Value |
    |:--|:--|:--|:--|
    | And | State | = | `Active` |
    | And | Changed Date | < | `@Today - 7` |

    **2** stories, both on `Mobile Check Deposit 2.0`, both Ethan's: `Auto-capture check edges with on-device ML` (last changed 9 days ago) and `Retry flow for failed check uploads` (10 days).

    **D · Work that arrived after planning**

    | And/Or | Field | Operator | Value |
    |:--|:--|:--|:--|
    | And | Iteration Path | = | `@CurrentIteration` (team `Mobile Banking`) |
    | And | Tags | Contains | `unplanned` |

    **2** stories, **5 points**: `Holiday promo banner (marketing request)` (3, added on day 3, Ethan) and `App Store listing refresh` (2, added on day 4). Neither serves a Feature. The sprint started at 60 points and is now at 65.

    **E · Effort that serves no Feature**

    | And/Or | Field | Operator | Value |
    |:--|:--|:--|:--|
    | And | Work Item Type | = | `User Story` |
    | And | State | = | `Closed` |
    | And | Iteration Path | = | `@CurrentIteration - 1` (team `Mobile Banking`) |

    Columns: `Parent`, `Story Points`. **12** stories, **44** points, matching Sprint 13's velocity. **6** of them, **23 points**, have an empty Parent: **52%** of last sprint's completed effort served no Feature.

    **F · Quality debt**

    | And/Or | Field | Operator | Value |
    |:--|:--|:--|:--|
    | And | Work Item Type | = | `Bug` |
    | And | State | <> | `Closed` |

    Columns: `Severity`, `Priority`, `State`. **42** open bugs: 3 Critical, 11 High. **30** of the 42 are still New. Five sprints ago, at the start of Sprint 9, the number was 8. You'll chart that climb in [Lab 4](lab-04-sprint-delivery-report.md).

<!-- SHOT: lab02-stale-query | Boards › Queries › My Queries › Scratch - stale work, Editor and Results, clauses Area Path Under HarborPoint\Digital\Mobile Banking, State = Active, Changed Date < @Today - 7 | crop: clause grid plus the two result rows; highlight Changed Date and Assigned To -->

!!! reef "Reef ahead: “Their velocity is near its highest ever, so they're fine”"
    Did your first instinct in Part 2 say Mobile is doing well? Sprint 13 velocity was 44 points, second only to Sprint 12, and up from 33 in Sprint 9. Now set signal E beside it. Of those 44 points, **23 went to work that serves no Feature**, and only 11 moved `Mobile Check Deposit 2.0`, the Feature due this sprint. Velocity measures **estimates completed**, not value delivered, and it can't tell you *what* the points were spent on. A busy team that's behind on everything that matters looks exactly like a high-velocity team, until you ask which Features moved.

!!! insight "Lighthouse insight: Feature progress is the truth serum for velocity"
    When a team reports high velocity and its Features aren't moving, believe the Features. Feature progress only rises when work someone *decided* was valuable gets finished. For every velocity number you're shown, ask "and which Features did those points move?"

!!! checkpoint "Checkpoint"
    - [ ] I have six scratch queries in **My Queries**, one per signal, each with a count
    - [ ] For each signal I can name the item or person that matters most
    - [ ] I can explain why high velocity and a Feature that's behind aren't a contradiction

## Part 5 — The 10:00 readout

It's 9:40. Priya asked for five bullets.

!!! challenge "Challenge: The 10:00 readout"
    Write **exactly five** bullets for Priya, bottom line first.

    - **Bullet 1** is the answer to Dana's question in one sentence.
    - **Bullets 2–4** cover what shipped, what's unfinished and what needs attention, at Feature level, each with one number.
    - **Bullet 5** is what you need: a specific ask, with a named person.

    No story titles unless one is the evidence. No adjectives you can't back with a view.

!!! deliverable "Deliverable"
    A wiki page `/Training/P##/Monday Readout` with your five bullets, and under them, links to your evidence: the Velocity report, the Mobile Banking Features backlog, and your six scratch queries. Open **Overview › Wiki**, find `Training`. If there's no `P##` page under it yet, create it (the page's **⋯** menu › **Add sub-page**), then add `Monday Readout` beneath it. The `/Templates/Executive Briefing (BLUF)` page shows the shape if you want a starting point.

<!-- VERIFY: label of the wiki page menu action for adding a sub-page ("Add sub-page"), and whether /Training/P## pages are pre-created by provisioning. -->

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    BLUF means the reader can stop after any bullet and still have the most important thing. Ask yourself what Priya will repeat to Dana in one breath. That's bullet 1.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    Mobile isn't behind because it isn't working: its points are high. It's behind because its effort is spread across unaligned work, interrupted mid-sprint, and stuck waiting for one tester and one dependency. Say that, and then say what you need to change it.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    A model readout. Yours can differ, but it should be this short and this specific.

    > 1. **Bottom line:** Mobile Banking isn't short of effort, it's short of *focus*. `Mobile Check Deposit 2.0` will miss its end-of-Sprint-14 date (61% done, 36 points left, 14 of them already scheduled for Sprint 15), and we should re-forecast it today rather than at sprint review.
    > 2. **Shipped:** Sprint 13 delivered `Paperless Statements & Documents` (Digital Accounts, 26 of 26 points). Mobile completed 44 of 62 planned points (71%) and carried six stories; **52% of its completed points served no Feature**.
    > 3. **Unfinished:** `Biometric Login` is roughly on track for Sprint 16 if testing keeps pace. `Real-Time Fraud Alerts`, priority number one, is 4% done and blocked on a Security API that now lands after its Sprint 16 date. That needs a cross-team decision, not more effort from Mobile.
    > 4. **Needs us:** a Priority 1 escaped defect on Check Deposit with **no owner**; Ethan Brooks holding **6** active items, two of them stale for over a week; **11 points** of finished work waiting on our one tester; **5 points** of unplanned work added mid-sprint; **42** open bugs, up from 8 five sprints ago.
    > 5. **Asks:** (a) Diego and Hannah assign the P1 today, freeze mid-sprint intake, and swarm on testing; (b) your agreement to move Check Deposit's date or split it, before Dana hears it from someone else; (c) 30 minutes with Aisha Karimi this week on the Fraud Alerts dependency.

!!! checkpoint "Checkpoint"
    - [ ] `/Training/P##/Monday Readout` exists with exactly five bullets
    - [ ] Bullet 1 answers Dana's question in one sentence
    - [ ] Every number on the page links to, or names, the view or query it came from
    - [ ] Bullet 5 asks a named person for something specific

## Knowledge check

<div class="quiz" markdown>

**Mobile Banking's Sprint 13 velocity was 44 points, close to its highest ever. Its Feature due this sprint is 61% done. What best explains both being true?**

- [ ] The velocity chart is double-counting carried-over stories
- [x] Much of the completed effort went to work with no parent Feature, so points rose without moving the Features that matter
- [ ] Rollup progress lags velocity by one sprint
- [ ] The Feature's estimate is wrong and should be lowered

<div class="quiz-why" markdown>
Velocity sums the estimates of everything closed, aligned or not. 23 of Mobile's 44 points last sprint had no parent Feature. Feature progress rises only when Feature work is finished, which is why it's the better test of whether a team is delivering what the portfolio needs.
</div>

</div>

<div class="quiz" markdown>

**Three of Mobile's stories have sat in Resolved for two to six days, all waiting for the team's only tester. What's the most useful thing to do first?**

- [ ] Ask the developers to close the stories so progress reflects reality
- [ ] Ask the developers to pick up new stories while they wait
- [x] Treat testing as the constraint: get the team to swarm on testing, or find test capacity, before starting anything new
- [ ] Nothing. Resolved means the work is basically done

<div class="quiz-why" markdown>
Closing untested work makes the bars look better and the product worse. Starting more work grows the queue in front of the tester. When finished work waits, the fastest way to deliver more is to help the bottleneck, not to feed it.
</div>

</div>

<div class="quiz" markdown>

**Your stale-work query (`State = Active` and `Changed Date < @Today - 7`) found two stories. What can it miss?**

- [ ] Stories assigned to people who left the company
- [ ] Bugs, because Changed Date doesn't exist on bugs
- [x] Items that someone touched trivially, such as a comment or a tag, without any real progress
- [ ] Nothing. Changed Date is updated only when the State changes

<div class="quiz-why" markdown>
Changed Date moves on **every** save, including a "still working on it" comment. The query finds items nobody has touched, not items nobody has progressed. For a sharper signal, pair it with the board: an item sitting in the same column for days is stuck, whatever its Changed Date says.
</div>

</div>

## Captain's log

!!! log "Captain's log"
    1. When you come back from a week away, how long does it take you to know what your teams are working on at Feature level? What would get that under 15 minutes?
    2. Which of the six signals would light up first in your own teams right now? Which one would you not have thought to look for?
    3. What share of your teams' effort last sprint served no Feature or Epic? How would you find out?
    4. When a Feature is going to miss, who usually knows first, and how long until the portfolio knows?
    5. Read your five bullets again. Which one would Marcus challenge with "how do you know?", and can you open the evidence in ten seconds?

!!! bonus "Extra knots"
    1. **The last PI scorecard.** Open `Portfolio - Features by target date`, add `Closed Date` and `Iteration Path`, and list what PI 3 delivered. Two Features closed. A third finished all of its work in PI 3 but was never closed. Which one, and how would it distort a "PI 3 delivered" slide?
    2. **The quiet team.** Run all six signals for `Digital Accounts` in five minutes: copy each scratch query with **Save as** and change the area to `HarborPoint\Digital\Digital Accounts`, and the team on `@CurrentIteration` too. What does a healthy team's signals hunt look like? (Hint: 4 open bugs.)
    3. **Keep watch.** **Follow** `Mobile Check Deposit 2.0` and `Real-Time Fraud Alerts` from their work item forms, so changes to state, dates and discussion reach your inbox. What's the risk of following too many items?

## Key takeaways

- Start wide: six teams' work at Feature level in one query, then zoom in on the team in question.
- Compare each team with **its own plan**. Velocity never compares across teams, and the gap between Planned and Completed is where carry-over hides.
- A Feature's progress bar doesn't tell you whether it will make its date. Where the remaining work is planned, what state it's in and who owns it does.
- Six signals find most of what needs a manager: unowned urgency, overload, stale work, mid-sprint scope, unaligned effort and quality debt. Each one is a two-clause query.
- **Feature progress is the truth serum for velocity.** Report what moved the portfolio, lead with the bottom line, and end with a specific ask.

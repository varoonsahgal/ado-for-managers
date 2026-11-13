---
title: "Which Team Needs Help?"
lab: 6
day: 2
module: "Module 6 · Understanding Delivery Metrics and Team Performance"
duration: 50
sea_state: rough
role: "Delivery Manager, Digital Banking"
summary: "Two teams, two very different stories. Read velocity, throughput, cycle time and flow, then decide who actually needs help and what kind."
---

!!! briefing "Mission briefing"
    Both of Priya's delivery teams build for *Digital Banking Modernization*, and on paper they couldn't look more different. **Mobile Banking** completed 44 points last sprint, and its velocity is up by a third in five sprints. **Digital Accounts** completed 26 points, the same as it always does.

    This morning a slide in the steering pack put those two numbers side by side, and someone asked whether Digital Accounts "needs help getting its numbers up". Diego Ramirez, Mobile's engineering manager, says his team is flat out. Both statements can be true. Only one of them points at the team that needs help.

    You'll make a gut call first, then build a **case file** from the evidence Azure DevOps already holds: output, predictability, flow, quality and alignment. Then you'll decide, and write a half-page help plan that names actions, owners and the metric that will tell you whether each action worked.

    **Done looks like:** a completed evidence table, a verdict that rests on at least three independent signals, and `/Training/P##/Mobile Banking Help Plan` (or whichever team you conclude needs it) in the wiki.

<div class="msg" data-initials="PR" data-tone="teal" markdown>
<p class="msg-head"><strong>Priya Raman</strong><span>Director, Digital Banking · 9:12 AM</span></p>

Steering went sideways. Someone saw 44 against 26 and asked if Grace's team needs support. Diego tells me Mobile is drowning. I'd rather not guess. Which of my teams needs help, what kind of help, and what should I *not* do? Evidence, not adjectives. I see Dana at two.
</div>

## What you'll walk away with

- Read velocity for what it is (a sum of a team's own estimates) and pair it with throughput to spot point inflation
- Use planned vs completed, the cumulative flow diagram and cycle time to find where work really gets stuck
- Apply the **three signals rule**: never reach a verdict on one chart
- Separate a capacity fact ("this team finishes less") from a health problem ("this team is getting worse")
- Turn a diagnosis into management actions with owners and a metric to watch, and name what you won't do

## Before you set sail

- **Teams you'll read (never change):** `Mobile Banking` and `Digital Accounts`. In-context Analytics report settings (**Velocity by**, rolling periods) are **per user**, so change them freely. They don't change what anyone else sees.
- **Your Command Center** from [Lab 5](lab-05-command-center.md) already holds Mobile's Velocity, CFD and Cycle Time widgets. That's your fastest route. No dashboard? Every signal below also has an in-context route.
- **You'll create:** at most two extra widgets on your own Command Center, and the wiki page `/Training/P##/Mobile Banking Help Plan`.
- **Work in pairs if you can.** One of you takes Mobile Banking, the other Digital Accounts, and you merge the case file. It halves the clicking and doubles the arguing, which is the good part.
- **Time-box:** 50 minutes. Gut call 3, case file 30, verdict and help plan 15, debrief 2.

## Part 1 — Make the gut call

Before you look at a single chart, commit. Here is everything the steering group saw:

| Sprint 13 | Mobile Banking | Digital Accounts |
|:--|--:|--:|
| Points completed | **44** | **26** |
| Stories completed | 12 | 10 |
| Velocity, Sprint 9 → Sprint 13 | 33 → 44 | 24 → 26 |

Write three things at the top of a new wiki page `/Training/P##/Mobile Banking Help Plan` (you can rename it later if your verdict changes):

1. **Gut call:** which team needs help? Mobile Banking, Digital Accounts, or neither.
2. **Confidence:** 1 to 5.
3. **The one number that drove it.**

Your instructor will take a show of hands. Don't edit your gut call afterwards. Comparing it with your verdict is half the lesson.

!!! checkpoint "Checkpoint"
    - [ ] My gut call, confidence and deciding number are written at the top of my help plan page

## Part 2 — Open the case file

A good diagnosis looks at a team from several **independent** angles. If they agree, you have a finding. If they disagree, you have a question to ask the team, and that's still progress.

Copy this table into your page. You'll fill it in over the next three challenges.

| # | Signal | Where it lives | Mobile Banking | Digital Accounts | What it means |
|:-:|:--|:--|:--|:--|:--|
| 1 | Velocity (Sum of Story Points), S9 → S13 | Velocity | | | |
| 2 | Throughput (stories completed), S9 → S13 | Velocity by count | | | |
| 3 | Commitment reliability (completed ÷ planned) | Velocity, Planned vs Completed | | | |
| 4 | Work waiting in the flow | Cumulative Flow Diagram | | | |
| 5 | Cycle time trend and spread | Cycle Time widget | | | |
| 6 | Open bug trend | Query trend chart | | | |
| 7 | Share of completed points with no parent Feature | Velocity drill-down or orphan query | | | |
| 8 | Feature progress | Features backlog rollup | | | |

!!! insight "Lighthouse insight: the three signals rule"
    One chart is an anecdote. Velocity can rise because a team got faster, or because its estimates grew. A burndown can flatten because the team is stuck, or because nobody moved the cards. Before you act, look for **three independent signals** from different families: **output** (velocity, throughput), **flow** (CFD, cycle time, WIP) and **outcomes** (quality, Feature progress, alignment). When all three point the same way, act. When they disagree, go and ask the team, because the disagreement *is* the finding.

## Part 3 — Output and predictability

!!! challenge "Challenge: Is Mobile really faster?"
    Fill rows 1 to 3 for **both** teams, Sprints 9 to 13. For row 3, compute completed ÷ planned per sprint. Then answer in one sentence: *is Mobile Banking's rising velocity good news?*

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    One report answers all three rows. It can sum Story Points or count work items, and it shows a **Planned** bar next to **Completed**. It lives on each team's backlog, and you put a copy of it on your Command Center yesterday.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    **Boards › Backlogs**, team `Mobile Banking`, **Stories** level, **Analytics** tab, **Velocity** card › **View full report**. Toggle **Velocity by** between **Sum of Story Points** and **Count of Work Items**. Repeat for team `Digital Accounts`. Bugs live on these backlogs, so the count includes a few closed bugs. For stories only, temporarily set your Command Center Velocity widget to **Work item type** `User Story` with **Count**.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    | Sprint | 9 | 10 | 11 | 12 | 13 |
    |:--|--:|--:|--:|--:|--:|
    | **Mobile** planned / completed points | 38 / 33 | 44 / 37 | 50 / 41 | 56 / 45 | 62 / 44 |
    | **Mobile** stories completed | 12 | 12 | 13 | 12 | 12 |
    | **Mobile** points per story | 2.75 | 3.08 | 3.15 | 3.75 | 3.67 |
    | **Mobile** reliability | 87% | 84% | 82% | 80% | **71%** |
    | **Digital Accounts** planned / completed points | 26 / 24 | 26 / 26 | 25 / 25 | 27 / 24 | 26 / 26 |
    | **Digital Accounts** stories completed | 9 | 10 | 10 | 9 | 10 |
    | **Digital Accounts** reliability | 92% | 100% | 100% | 89% | 100% |

    **Reading:** Mobile's points went up by a third while the number of stories it finished didn't move. Each story simply got bigger on paper: **point inflation**. Meanwhile Mobile plans more every sprint (38 → 62) and delivers a smaller share of it, and carry-over grew from 2 stories (5 points) to 6 stories (18 points). Digital Accounts plans about 26 and delivers about 26, sprint after sprint.

    One-sentence answer: *No. Mobile's velocity rose because its estimates grew, not its output, and the gap between what it promises and what it delivers is widening.*

<!-- VERIFY: whether Count of Work Items in the in-context Velocity report includes closed bugs for these teams (bugs managed with requirements), and the Count values shown; the story-only counts above come from the seeded data. -->

<!-- SHOT: lab06-velocity-points-vs-count | Boards › Backlogs, team Mobile Banking, Stories, Analytics › Velocity full report, shown twice side by side: Velocity by Sum of Story Points (33, 37, 41, 45, 44 rising) and by Count of Work Items (flat) | crop: both charts; highlight the rising points bars against the flat count bars -->

!!! reef "Reef ahead: “Digital Accounts has the lowest throughput, so it needs help”"
    If your gut call was Digital Accounts, you're in good company. Half of most rooms say the same, and the steering group said it this morning. It's also wrong. Digital Accounts does finish fewer stories (9 or 10 against Mobile's 12) and fewer points. But look at what came with that number: it finishes **what it plans**, every sprint, at 89 to 100%. Lower throughput is a **capacity fact**. It tells you how much to plan with this team, not that something's broken. "Help" aimed at a healthy, predictable team usually means pressure, and pressure on a predictable team buys you inflated estimates and a less predictable team. And Digital Accounts' 26 and Mobile's 44 aren't even on the same scale: each team's Story Points are its own currency.

!!! insight "Lighthouse insight: velocity measures estimates, throughput measures finishing"
    **Velocity** is the sum of a team's own estimates for what it finished. It's a fine planning input *for that team*, and nothing else. **Throughput** is the count of items finished. It can't inflate, because nobody can re-estimate a "1". When velocity climbs and throughput stays flat, the yardstick changed, not the speed. Watch both, always, and never compare either across teams with different work and different scales.

!!! checkpoint "Checkpoint"
    - [ ] Rows 1 to 3 are filled for both teams
    - [ ] I can explain point inflation using Mobile's numbers in one sentence

## Part 4 — Follow the flow

Output tells you *what* came out. Flow tells you *where it gets stuck on the way*. Mobile Banking moves stories New → Active → Resolved → Closed, and **Resolved** means *code complete, waiting for QA*. Hold that thought.

!!! challenge "Challenge: Find the bottleneck"
    Fill rows 4 and 5 for both teams. Then name **where** in Mobile Banking's process work waits, **why**, and **what's waiting there right now**.

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    In a cumulative flow diagram, each band is a board column. A band that gets **thicker** over time is a queue forming in front of the next step. The Cycle Time widget shows whether that queue costs time.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    **CFD:** **Boards › Backlogs**, team `Mobile Banking`, **Stories**, **Analytics** › **Cumulative Flow Diagram** › **View full report**. Set **Rolling period** to cover back to Sprint 9 (about 90 days). Repeat for `Digital Accounts`. **Cycle time:** use `Cycle time · Mobile Banking` on your Command Center, then add a second **Cycle Time** widget for **Team** `Digital Accounts`, same settings (**Work item type** `User Story`, about 90 days). **Right now:** **Boards › Sprints**, team `Mobile Banking`, `Sprint 14`, and look at what's in **Resolved** and who it's assigned to.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    | Signal | Mobile Banking | Digital Accounts |
    |:--|:--|:--|
    | **CFD** | The **Resolved** band widens sprint after sprint. Stories pile up between "code complete" and "tested" | Thin, parallel bands. Work arrives and leaves at about the same rate |
    | **Cycle time** | Average rises from about **3.5 days** (Sprint 9) to about **9 days** (Sprint 13), and the shaded spread widens | Steady at **4 to 5 days**, narrow spread |
    | **Right now** | 3 stories, 11 points, sit in Resolved waiting for **Ava Patel, the team's only tester**: 6 days, 5 days and 2 days | Nothing queued |

    **Diagnosis:** Mobile has a testing bottleneck. Four engineers produce work faster than one tester can verify it. Each sprint more work waits in Resolved, cycle time stretches, and stories miss the sprint end, which shows up as carry-over and falling reliability. Rising cycle time and a widening Resolved band are two independent signals pointing at one cause.

    And Resolved isn't done: velocity and rollups credit only Closed work, so 11 points of finished code show as *not delivered* while they wait.

<!-- VERIFY: Mobile Banking's board columns are New / Active / Resolved / Closed (the CFD bands follow board columns, not states); maximum rolling period accepted by the CFD and Cycle Time widgets. -->

<!-- SHOT: lab06-cfd-mobile | Boards › Backlogs, team Mobile Banking, Stories, Analytics › Cumulative Flow Diagram full report, rolling period about 90 days | crop: chart; highlight the Resolved band widening from Sprint 9 to Sprint 14 -->

<!-- SHOT: lab06-cycle-time-pair | P## - Digital Banking Command Center, Cycle time · Mobile Banking and Cycle time · Digital Accounts widgets side by side, User Story, about 90 days | crop: both widgets; highlight Mobile's rising moving average and wider band against Digital Accounts' flat one -->

!!! insight "Lighthouse insight: more in progress means slower, not faster"
    Little's Law, in plain words: **average time in progress ≈ work in progress ÷ finishing rate**. Mobile has about 10 stories in progress (7 Active, 3 Resolved) and finishes about 12 a sprint, so a story spends most of a sprint in flight. Digital Accounts has 3 in progress and finishes about 10, so its stories move through in days. Starting more work doesn't make a team finish more; it makes everything take longer. When a team says it's "flat out", count what it has *started*. Ethan Brooks alone has six active items.

!!! checkpoint "Checkpoint"
    - [ ] Rows 4 and 5 are filled for both teams
    - [ ] I can name Mobile's bottleneck, its cause, and what's waiting there now

## Part 5 — Quality and alignment

A team can finish plenty and still fall behind if what it finishes is rework, or isn't the work the portfolio needs.

!!! challenge "Challenge: What is the output worth?"
    Fill rows 6 to 8 for both teams. For row 7, compute the orphan share for **Sprint 9 and Sprint 13** at least. For row 8, stay at Feature altitude: which of each team's Features moved, and which are due?

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Row 6 is a **trend chart** on a bug query. Row 7 is hiding behind the Velocity report's bars: selecting a bar opens the items behind it. Row 8 is a rollup column on a Features backlog, which you used in Lab 1.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    - **Bugs:** reuse your Lab 4 bug trend, or create a flat query `CC - Open bugs (Digital)` (`Work Item Type` `=` `Bug`, `Area Path` `Under` `HarborPoint\Digital`, `State` `<>` `Closed`, with `Node Name` as a column). **Charts** › **New chart** › **Stacked area**, grouped by `Node Name`, over a period that reaches before Sprint 9 (about three months).
    - **Orphans:** in Mobile's Velocity report, select the Sprint 13 **Completed** bar. Add the `Parent` and `Story Points` columns to the query that opens, and add up the points with no parent. Repeat for Sprint 9, and for Digital Accounts.
    - **Features:** **Boards › Backlogs**, team `Digital Portfolio`, **Features**, with **Target Date** and the **Progress by Story Points** rollup column.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    | Signal | Mobile Banking | Digital Accounts |
    |:--|:--|:--|
    | **Open bugs** | **8 → 42** across five sprints, more than fivefold. 3 are Severity 1-Critical, and one Priority 1 bug on Mobile Check Deposit 2.0 has no owner | **7 → 4**, falling |
    | **Orphan share of completed points** | S9 27% · S10 30% · S11 29% · S12 36% · **S13 52%** (23 of 44 points, 6 of 12 stories) | **21%** in Sprint 9, then about a tenth or less every sprint since (S13: 2 of 26 points) |
    | **Feature progress** | `Mobile Check Deposit 2.0` due **this sprint** at 61%: it will miss. `Real-Time Fraud Alerts` 4% (blocked on Security, Lab 7). `Biometric Login` 53%, due Sprint 16 | `Paperless Statements & Documents` **closed** last sprint. `Spending Insights` 88%. `Online Account Opening` 59%, due Sprint 16 |

    **Reading:** last sprint, more than half of Mobile's "record" velocity went to work that serves no Feature, while its most urgent Feature slipped. Its bug backlog is the debt it's taking on to look fast. Digital Accounts' smaller output lands almost entirely on its Features, and they're closing.

<!-- VERIFY: selecting a Completed bar in the in-context Velocity report opens a query of those items that accepts Column options; the trend chart's rolling-period options reach back before Sprint 9. -->

<!-- SHOT: lab06-bug-trend | Boards › Queries › Shared Queries/Training/P##/CC - Open bugs (Digital), Charts tab, Stacked area trend grouped by Node Name over about three months | crop: chart; highlight Mobile Banking rising from 8 to 42 and Digital Accounts falling to 4 -->

!!! checkpoint "Checkpoint"
    - [ ] Rows 6 to 8 are filled for both teams
    - [ ] I know what share of Mobile's Sprint 13 points served no Feature

## Part 6 — Decide, and write the help plan

Look at your eight rows. Count how many families (output, flow, outcomes) point at each team. Then look back at your gut call.

!!! challenge "Challenge: The help plan"
    Write the verdict and a half-page help plan on `/Training/P##/Mobile Banking Help Plan`:

    1. **Verdict** in two sentences, citing at least three signals from different families.
    2. **Three actions.** For each: what changes, **who owns it** (a real HarborPoint name), and **the metric you'll watch** to know it worked, with the direction you expect it to move.
    3. **What we will not do**, in two or three bullets.
    4. **One sentence about the other team.**

!!! deliverable "Deliverable"
    The wiki page `/Training/P##/Mobile Banking Help Plan` (a sub-page of your `P##` page under **Overview › Wiki**) with your gut call at the top, your completed evidence table, the verdict, three owned actions with metrics, and the "will not do" list. You'll use it in [Lab 8](lab-08-executive-status-review.md).

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Every action should attack a **cause** you found, not a number. The causes: a testing bottleneck, too much work started, unplanned work entering mid-sprint, quality debt, and estimates that drifted. Owners are people who can actually change the cause: Diego Ramirez (engineering manager), Hannah Cole (Product Owner), and Priya when the pressure comes from outside the team.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    Metrics to watch should come from your Command Center, so you can check them every Monday: cycle time, the Resolved band, planned vs completed, the urgent-bug tile, the orphan tile, and throughput by count. Mid-sprint intake shows up in Sprint 14's burndown as **Total Scope Increase** (5 points this sprint, all of it orphan work).

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    **Verdict.** *Mobile Banking needs help, and it's help with its system, not its effort. Its velocity is inflated (points up a third, stories flat), reliability fell from 87% to 71%, open bugs went from 8 to 42, cycle time more than doubled behind a single-tester bottleneck, and 52% of last sprint's points served no Feature.*

    | # | Action | Owner | Metric to watch |
    |:-:|:--|:--|:--|
    | 1 | **Unblock testing.** Finish before starting: engineers pair with Ava Patel and test each other's stories before picking up new work, with a limit of three stories in Resolved. Make the case to Priya for a second tester or test automation in PI 5. | Diego Ramirez | **Cycle time** back toward 5 days within two sprints; the **Resolved band** in the CFD stops widening |
    | 2 | **Protect the sprint and limit WIP.** No new work after day 1 without swapping something of equal size out. Marketing and other requests go through Hannah, and Priya backs her when they push. Cap active items per person (Ethan has six). | Hannah Cole, backed by Priya | **Reliability** back above 85%; **Total Scope Increase** at 0 on the sprint burndown |
    | 3 | **Pay down quality debt and re-anchor the work.** Reserve about a fifth of each sprint for bugs, P1s first, starting with the unowned P1 on Mobile Check Deposit 2.0. Agree a Definition of Done that ends at Closed with no open Severity 1 or 2 bugs. Every story gets a parent Feature or an explicit reason it doesn't. | Diego and Hannah | **Urgent bugs** tile trending down; **orphan share** under 20%; **throughput by count** holds steady while points stop climbing |

    **What we will not do:**

    - Set a velocity target, or praise or blame either team by velocity
    - Compare Mobile's and Digital Accounts' velocity, or ask Digital Accounts to "go faster"
    - Move more work onto Mobile because "it has the highest velocity"

    **The other team:** *Digital Accounts is healthy and predictable; protect it by planning with its real velocity of about 25 and keeping unplanned work away from it.*

    Also strong: re-anchoring estimation with a few reference stories so Mobile's points mean what they used to, and an honest conversation with Priya about Mobile Check Deposit 2.0's date now, not at sprint review.

!!! reef "Reef ahead: fixing the number instead of the team"
    The fastest way to "fix" Mobile's dashboard is to make reliability look better: plan less, estimate higher, close stories before Ava tests them. Every one of those moves a number and makes the team worse. Push for "more points" and points will appear, because the team controls the estimates. If your actions could be satisfied by changing what people *type* rather than what they *do*, rewrite them.

!!! insight "Lighthouse insight: Goodhart's law, and metrics as conversation starters"
    *When a measure becomes a target, it ceases to be a good measure.* Velocity is the classic victim: make it a target and estimates inflate until the target is met and nothing has changed. Mobile's chart may already show the early signs. Use metrics to **open** a conversation with a team ("your cycle time doubled; what's happening in Resolved?"), never to close one ("your velocity is up, well done"). The team usually knows the cause. Diego knows Ava is swamped. The metric's job is to make that visible enough that someone with authority acts on it.

!!! checkpoint "Checkpoint"
    - [ ] My verdict cites at least three signals from different families
    - [ ] I have three actions, each with a named owner and a metric with an expected direction
    - [ ] My page has a "will not do" list and one sentence about the other team
    - [ ] I compared my verdict with my Part 1 gut call

## Knowledge check

<div class="quiz" markdown>

**Which pair of signals most strongly points to a testing bottleneck on Mobile Banking?**

- [ ] Rising velocity and a rising bug count
- [x] A widening Resolved band in the CFD and rising cycle time
- [ ] Falling commitment reliability and rising orphan share
- [ ] A sprint burndown that flattens mid-sprint

<div class="quiz-why" markdown>
The CFD shows *where* work queues (Resolved means "waiting for QA" on this team) and cycle time shows that the queue costs time. Two independent views of the same cause. The other pairs are real problems, but neither one locates the step where work waits.
</div>

</div>

<div class="quiz" markdown>

**In steering, someone points out that Digital Accounts completed 26 points to Mobile Banking's 44. What can you conclude about the two teams?**

- [ ] Mobile Banking is about 70% more productive
- [ ] Digital Accounts needs coaching to raise its velocity
- [x] Nothing about relative productivity: each team's Story Points are its own scale
- [ ] Digital Accounts is estimating too low

<div class="quiz-why" markdown>
Velocity sums a team's own estimates, so it's only comparable with that team's past. The useful comparison is each team against itself: Digital Accounts delivers what it plans; Mobile delivers a shrinking share of a growing plan.
</div>

</div>

<div class="quiz" markdown>

**Dana suggests a stretch goal: Mobile Banking reaches 50 points a sprint next PI. What's the best response?**

- [ ] Agree, since the trend is already heading there
- [ ] Agree, but measure throughput by count instead
- [x] Push back: a velocity target will inflate estimates; propose targets on the causes, like cycle time and reliability
- [ ] Ask Digital Accounts to set a matching goal so the teams stay fair

<div class="quiz-why" markdown>
Goodhart's law. Mobile controls its own estimates, so a points target is met by re-estimating, and the last five sprints suggest it's already happening. Targets belong on things the team can't game by typing: time to finish, share of plan delivered, defects escaping.
</div>

</div>

<div class="quiz" markdown>

**Mobile wants to finish more stories per sprint. Which change most directly shortens its cycle time?**

- [ ] Start more stories at the beginning of each sprint
- [x] Limit how much work is in progress, and finish (test) before starting new work
- [ ] Re-estimate the backlog with larger points
- [ ] Move testing to the end of the sprint so engineers can keep building

<div class="quiz-why" markdown>
Time in progress grows with work in progress. With one tester, starting more only lengthens the Resolved queue. Finishing first shrinks the queue, and cycle time falls with it.
</div>

</div>

## Captain's log

!!! log "Captain's log"
    1. Was your gut call right? What would have changed your mind sooner?
    2. Which of your teams has the "best" numbers right now? Which three signals would you check before you believed them?
    3. Where in your own delivery process does work wait for one person or one role? How would you know if that queue were growing?
    4. Has anyone in your organization turned velocity, or a similar metric, into a target? What happened to the estimates?
    5. Think of a team that's predictable but "slow". What would you say to the leader who wants it to go faster?

!!! bonus "Extra knots"
    1. **Two burndowns, one sprint.** Open Sprint 14's burndown for both teams (**Boards › Sprints**, team, `Sprint 14`, **Analytics**, **Burndown on** Story Points). Mobile shows a **Total Scope Increase** of 5 points (two `unplanned` stories added on days 3 and 4, neither on a Feature) and 12 of 65 points done. Digital Accounts: 10 of 26, no scope added. What does each picture say about the next sprint?
    2. **How old is the debt?** Add a **Lead Time** widget for `Mobile Banking` with **Work item type** `Bug`. Lead time runs from creation, so it shows how long fixed bugs waited. What would you expect it to show for the 30 bugs still in **New**, and why can't the widget show them?
    3. **Pre-empt the next bad idea.** Write the two sentences you'd say if someone proposed giving Digital Accounts' biggest upcoming Feature to Mobile Banking "because it has the highest velocity". You'll need them in [Lab 9](../day-3/lab-09-meet-the-deadline.md).

## Key takeaways

- Velocity is a team's sum of its own estimates. Pair it with throughput: rising points over flat counts is point inflation, not speed.
- Never reach a verdict on one chart. Look for three independent signals across output, flow and outcomes.
- Lower throughput with steady, reliable delivery is a capacity fact to plan around, not a problem to fix.
- The CFD shows where work waits, cycle time shows what the wait costs, and too much work in progress makes everything slower.
- Help means changing the system (WIP, intake, testing, quality bar), with an owner and a metric for each change. It never means a velocity target.

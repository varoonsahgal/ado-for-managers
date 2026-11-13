---
title: "Can HarborPoint Meet the Deadline?"
lab: 9
day: 3
module: "Module 9 · Forecasting Delivery and Managing Capacity"
duration: 55
sea_state: rough
role: "Acting Program Manager, METP"
summary: "The EVP wants all of Instant Card Controls before holiday travel. Use velocity, capacity and the forecast tool to give her an honest answer and a better option."
---

!!! briefing "Mission briefing"
    Ruth Ellison retires at the end of PI 4, and as of this morning you're acting Program Manager for Project Lighthouse. Your first request from Dana Whitfield is a big one.

    **Instant Card Controls** lets members lock and unlock a card, set travel notices and control how a card can be used, from the app or online banking. It's Digital Accounts' Feature, it carries the `leadership-ask` tag because Dana asked for it directly, and it hasn't started: 20 stories, 105 estimated points, four stories with no estimate at all. It's planned for Sprints 15 to 17. Dana wants all of it by the end of Sprint 17, before holiday travel.

    You won't answer with a gut feeling or a single date. You'll read the team's history, work out its real capacity, run the forecast tool honestly in your sandbox, find out where the tool flatters you, and give Dana a range and a better option. **Done looks like:** a capacity worksheet, three forecast runs, a reshaped MVP that fits, and a bottom-line-up-front note to Dana that she can act on.

<div class="msg" data-initials="DW" data-tone="navy" markdown>
<p class="msg-head"><strong>Dana Whitfield</strong><span>EVP, Member Experience · 8:06 AM</span></p>

Welcome to the hot seat. First question for you as program manager: members need Instant Card Controls before holiday travel. Lock a lost card, tell us they're traveling, the works. **All of it, by the end of Sprint 17.** Can we do it? I'd like a yes, but I'll take a true answer. By end of day, please.
</div>

## What you'll walk away with

- Turn velocity history and team availability into a capacity number you can defend, line by line
- Run the backlog forecast tool and know exactly what it assumes, what it ignores and where it flatters you
- Reshape scope so a deadline becomes achievable, and prove it with the same tool
- Answer "can we?" with a range, its conditions and the options, not a promise
- Resist the most common resourcing fix and explain why it fails

## Before you set sail

- **Access:** Basic. Forecasting and the Capacity tab are not available with Stakeholder access.
- **Your sandbox:** team `P## Sandbox`, area `HarborPoint\Training\P##`. It holds `P## - Instant Card Controls (planning copy)`: the same 20 stories as the real Feature, with the same points and order, and no sprints. **You may reorder, tag and re-estimate these freely.** Every sandbox title starts with `P## - `; this lab drops the prefix when it names a story. Your sandbox team selects Sprints 15 to 20 only, so its forecast starts at Sprint 15, because Sprint 14 is already committed. The same area also holds the Lab 11 practice set (`P## - Omnichannel Service Requests (sandbox)`): leave it alone today, and keep it below the planning copy.
- **Read only:** `Digital Accounts` (backlog, Velocity, Capacity) and `Mobile Banking`. View options and report settings are per user, so changing those is fine. Dragging, tagging or re-estimating on a real team's backlog is not.
- **You'll create:** the wiki page `/Training/P##/Card Controls Outlook`.
- **Time-box:** 55 minutes. Part 1 is 6, Part 2 is 10, Part 3 is 12, Part 4 is 8, Part 5 is 7 and Part 6 is 12. Protect Part 6.

!!! warning "Two backlogs, two rules"
    In your **sandbox** backlog, drag, tag and estimate as much as you like. On **Digital Accounts'** backlog you only look. Dragging a story there re-ranks it for the team and for everyone in the room.

## Part 1 — Read the history

Every forecast starts from what the team has actually done. Digital Accounts is the steadiest team in the program. Find out how steady.

!!! speedrun "Speed run · 6 minutes"
    For team `Digital Accounts`, find:

    1. Completed Story Points for each of Sprints 9 to 13, and their mean
    2. Planned versus completed for each sprint: how reliable is the team's plan?
    3. The points Dana's request needs per sprint, if all 105 estimated points must land in Sprints 15, 16 and 17

<div class="timer" data-minutes="6" data-label="Speed run"></div>

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    The team's backlog has an **Analytics** tab. The Velocity report there shows planned and completed work per sprint.

??? pilot "Harbor Pilot · Hint 2: Bring it into port (full solution)"
    **Boards › Backlogs**, team `Digital Accounts`, **Stories** level › **Analytics** › **Velocity** › **View full report**. Set **Velocity by** to Sum of Story Points and **Number of Iterations** to **Last 6 iterations**.

    | Sprint | 9 | 10 | 11 | 12 | 13 |
    |---|:-:|:-:|:-:|:-:|:-:|
    | Planned | 26 | 26 | 25 | 27 | 26 |
    | Completed | **24** | **26** | **25** | **24** | **26** |

    **Mean 25.0, range 24 to 26.** The plan holds: the weakest sprint was Sprint 12, with 24 of 27. Sprint 14 is still in progress, so leave it out of the mean.

    Dana's request: 105 points in three sprints is **35 points per sprint**, for Card Controls alone. Digital Accounts has never completed more than 26 in a sprint, for *all* its work.

    <!-- VERIFY: whether the Average Velocity card on the Analytics tab includes the in-progress Sprint 14 (10 points so far). If it does, tell participants to compute the mean from Sprints 9 to 13 themselves. -->

<!-- SHOT: lab09-da-velocity | Boards › Backlogs › Digital Accounts › Stories › Analytics › Velocity full report, Sum of Story Points, last 6 iterations, Sprints 9 to 14 | crop: chart; highlight the five completed bars 24/26/25/24/26 -->

!!! insight "Lighthouse insight: a stable team is a forecastable team"
    Digital Accounts' greatest asset isn't speed. It's that 25 means 25. A team whose output varies by two points a sprint can be forecast. A team whose velocity climbs while its finished-story count stays flat, as Mobile Banking's does, can't. Predictability is a feature you protect, not a weakness you push against.

!!! checkpoint "Checkpoint"
    - [ ] I have Digital Accounts' completed points for Sprints 9 to 13 and their mean, 25
    - [ ] I know Dana's request needs 35 points per sprint for Card Controls alone

## Part 2 — Work out the real capacity

A velocity of 25 describes a normal sprint with five engineers present. Sprints 15 to 17 aren't normal: there's a holiday, a vacation, an absence and a new hire. Velocity tells you the rate. Capacity tells you how much of the rate you'll actually get.

1. Open **Overview › Wiki** › `Teams` › `Digital Accounts Availability`. Note who is out, when, and who joins.
2. Open **Boards › Sprints**, team `Digital Accounts`, `Sprint 16`, **Capacity** tab. Look at the **Team days off** row. You're viewing; don't **Save** anything.

<!-- VERIFY: the seeded Team days off for Digital Accounts in Sprint 16 shows 2 days on the Capacity tab, and the grid has no user rows (the team members are fictional names, not real users). -->

<!-- SHOT: lab09-capacity-s16 | Boards › Sprints, team Digital Accounts, Sprint 16, Capacity tab, showing the Team days off row with 2 days | crop: capacity grid; highlight Team days off -->

**So what does a points-per-day rate look like?** Digital Accounts has **five delivery engineers**: Olivia Grant, Noah Kim, Fatima Hassan, Lucas Meyer and Chloe Martin. Five engineers for ten working days is **50 engineer-days**, and the team completes about **25 points** in a normal sprint. That's **0.5 points per engineer-day**. It's crude, and it's good enough.

!!! challenge "Challenge: The capacity worksheet"
    Complete the worksheet, then work out how many points Card Controls can realistically get.

    | Sprint | Normal engineer-days | Days lost (who, why) | Available engineer-days | Points at 0.5 per day |
    |---|:-:|---|:-:|:-:|
    | Sprint 15 | 50 | | | |
    | Sprint 16 | 50 | | | |
    | Sprint 17 | 50 | | | |
    | **Total** | | | | |

    Then subtract what Digital Accounts must deliver before Card Controls gets a point:

    - **Online Account Opening** is a committed PI 4 Feature, due at the end of Sprint 16
    - **Spending Insights** is committed too, due at the end of Sprint 15
    - Bugs and support work don't stop because a Feature is important

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    The holiday is a team day off, so it costs every engineer a day. A vacation costs one person. A new hire adds capacity, but not at full speed. For the committed Features, open each one from the **Features** backlog and look at its remaining children after Sprint 14.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    - Sprint 15: Noah Kim is out 3 days.
    - Sprint 16: a 2-day company holiday for everyone, and Olivia Grant is out 5 days.
    - Sprint 17: a 1-day holiday for everyone. Wes Turner joined in Sprint 16. He's ramping up, so count about 0 points from him in Sprint 16 and about 2 in Sprint 17.
    - After Sprint 14, Online Account Opening has **9 points** left and Spending Insights has **5**. Reserve about **10%** of capacity for bugs and support.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    | Sprint | Normal | Days lost | Available | Points |
    |---|:-:|---|:-:|:-:|
    | Sprint 15 | 50 | Noah Kim, 3 days | 47 | **23.5** |
    | Sprint 16 | 50 | Holiday, 2 days × 5 people = 10; Olivia Grant, 5 days | 35 | **17.5** |
    | Sprint 17 | 50 | Holiday, 1 day × 5 people = 5 | 45 | 22.5, plus Wes Turner about 2 = **24.5** |
    | **Total** | | | | **≈ 65** |

    | Capacity | Points |
    |---|:-:|
    | Sprints 15 to 17, if 100% went to Card Controls | ≈ 65 |
    | minus Online Account Opening (remaining after Sprint 14) | − 9 |
    | minus Spending Insights (remaining after Sprint 14) | − 5 |
    | minus about 10% for bugs and support | ≈ − 6.5 |
    | **Left for Instant Card Controls** | **≈ 45** |

    **Full scope is 105 estimated points plus four unestimated stories. That isn't late. It's impossible.** Even if Digital Accounts dropped everything else, 65 is not 105. The question is no longer "can we?" It's "what can members have by Sprint 17?"

!!! reef "Reef ahead: \"just use the average\""
    "The team does 25 a sprint, so three sprints is 75" is the most common forecast in any organization, and here it's wrong by 30 points. It assumes everyone is present, all the capacity goes to one Feature, and nothing else is committed. Velocity is a rate for a normal sprint. Before you multiply it, ask who is out, what else is promised and what always turns up unplanned.

!!! checkpoint "Checkpoint"
    - [ ] My worksheet gives about 23.5, 17.5 and 24.5 points for Sprints 15, 16 and 17, about 65 in total
    - [ ] After the committed work and a bug allowance, about 45 points are left for Card Controls

## Part 3 — Forecast in the sandbox

Now let the tool do the arithmetic, story by story. The forecast tool walks the backlog in order, adds up Story Points, and draws a line at each sprint where the velocity you entered runs out. It's quick, visual and very literal.

**Set it up** in your sandbox:

1. **Boards › Backlogs**, team `P## Sandbox`, **Stories** level.
2. **View options**: **Parents** Off, **In Progress Items** Off, **Completed Child Items** Off, **Side Pane** Off. Then turn **Forecasting** On.
3. Clear any filter (**Clear and dismiss filtering**). A filter disables Forecasting.
4. Add `Story Points` and `Tags` with **Column Options**, if they aren't showing.
5. Check the top of the list. The first item should be `P## - Card lock and unlock service and API`, and the 20 planning-copy stories should follow in order. If other sandbox items (such as the Lab 11 practice stories) sit above it, select them and use **Move to bottom** from the context menu. Anything with Story Points above the planning copy would eat into your forecast.
6. In the banner **Forecasting based on velocity of**, select the number and type `25`.

<!-- VERIFY: (a) the planning-copy stories carry the same titles as the real F5 stories (with or without a P## prefix) and sit at the top of the sandbox Stories backlog, above the Lab 11 sandbox items; (b) the Forecasting toggle is greyed out while Parents is On; (c) the forecast velocity is stored per user; (d) Move to bottom is offered in the multi-select context menu. -->

A **Forecast** column appears on the left, with a line under the last story that fits in each sprint. Your first line is **Sprint 15**.

!!! challenge "Challenge: Three velocities, three answers"
    Run the forecast at **25**, **20** and **15**. For each, record the last story above the **Sprint 17** line, the points that land by Sprint 17, and whether the whole MVP lands. The eight MVP stories are #1, #2, #3, #4, #6, #7, #8 and #9 in the original order (44 points). #5 is a "should".

    | Velocity | Last story above the Sprint 17 line | Points by Sprint 17 | Whole MVP lands? |
    |:-:|---|:-:|:-:|
    | 25 | | | |
    | 20 | | | |
    | 15 | | | |

    Then decide: which of the three would you show Dana, and why?

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Three sprints at a given velocity is a cumulative budget: unused velocity carries into the next sprint. So the Sprint 17 line falls under the last story whose running total fits within three times the velocity.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    The budgets are 75, 60 and 45 points. Keep a running total down the Story Points column, and compare each with Part 2: which of the three velocities matches the points Card Controls will actually get?

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    | Velocity | Last story above the Sprint 17 line | Points by Sprint 17 | Whole MVP lands? |
    |:-:|---|:-:|:-:|
    | 25 | #12 `International transaction toggle` | **73** (#1 to #12) | Yes, plus three more |
    | 20 | #10 `Spending limits by category` | **55** (#1 to #10) | Yes |
    | 15 | #8 `Accessibility review for card controls` | **42** (#1 to #8) | **No.** MVP story #9, `Fraud team view of member-locked cards`, misses |

    **Show Dana 15.** It's the only one that matches Part 2: about 45 points over three sprints is an average of 15 a sprint for Card Controls. Twenty-five is the team's *whole* velocity, as if Online Account Opening, Spending Insights, bugs, the holiday and two absences didn't exist. Twenty is a hopeful middle with no evidence behind it.

    Look at the Sprint 16 line, too. The tool uses one velocity for every sprint, but Sprint 16 has only 17.5 points of real capacity. The per-sprint lines are wrong even when the Sprint 17 total is right.

<!-- SHOT: lab09-forecast-15 | Boards › Backlogs, team P## Sandbox, Stories level, Forecasting on at velocity 15, Parents/In Progress/Completed Child Items off; Forecast column showing Sprint 15, 16 and 17 lines | crop: Forecast column, Title and Story Points for stories #1 to #10; highlight the Sprint 17 line under Accessibility review for card controls and Fraud team view of member-locked cards just below it -->

!!! checkpoint "Checkpoint"
    - [ ] My table shows 73, 55 and 42 points by Sprint 17 at velocities 25, 20 and 15
    - [ ] I can say why 15 is the honest velocity for Card Controls, and why the Sprint 16 line is still optimistic

## Part 4 — Reshape the scope

At an honest velocity, the MVP misses by one story. You could stop there and report a miss. A program manager first asks: is the order right?

!!! challenge "Challenge: Make the MVP fit"
    In your sandbox, with Forecasting on at **15**:

    1. Tag the eight MVP stories `MVP`.
    2. Change the order so the **whole MVP lands by Sprint 17**, without changing a single estimate.
    3. Then run the trap: drag #17, `Recurring payment exceptions when a card is locked`, to the top of the list. Watch the forecast lines. What happened, and what does it tell you?

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    One story above the MVP's last item isn't MVP. For the trap, look at the story's Story Points.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    Multi-select the eight MVP stories, open the context menu › **Edit**, add the **Tags** field with `MVP`, and **Save changes**. Or tag each one on its form. Then drag #5, `Travel notice auto-expiry and reminders` (3 points), to just below #9.

    <!-- VERIFY: the bulk Edit work items dialog offers Tags (Add) or Tags for appending a tag without replacing existing tags. -->

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    **The MVP fits.** With #5 below the MVP set, the first eight stories are the MVP: 8 + 5 + 8 + 5 + 5 + 5 + 3 + 5 = **44 points**, inside the 45-point budget. The Sprint 17 line now falls under `Fraud team view of member-locked cards`, and `Travel notice auto-expiry and reminders` sits just below it. A "should" story was standing in front of a "must". Ordering is a scope decision.

    **The buffer is about one point.** That's effectively none. One sick week, one urgent bug, or one story that turns out bigger than its estimate, and the MVP misses.

    **The trap.** Move #17 to the top and the lines don't move at all. It has no Story Points, so the tool treats it as free. It's still a whole piece of work, and it's not a trivial one: if a member locks a card, what happens to their recurring bills? That may well be an MVP question. The four unestimated stories (#17 to #20) are invisible to every forecast you've run today. Drag #17 back to the bottom before you continue.

<!-- SHOT: lab09-forecast-mvp-reordered | P## Sandbox Stories backlog, Forecasting at velocity 15, Tags column showing MVP on the first eight stories, Travel notice auto-expiry and reminders moved below Fraud team view of member-locked cards | crop: Forecast, Title, Story Points, Tags; highlight the Sprint 17 line under the eighth MVP story -->

!!! reef "Reef ahead: zero points look free"
    The forecast tool adds up Story Points. A story with none adds nothing, so you can put four unestimated stories at the top of a backlog and the forecast stays exactly the same. "It all fits" often means "we haven't sized the hard parts yet." Before anyone quotes a forecast, ask how many items in its scope have no estimate. Here the answer is four out of twenty.

!!! insight "Lighthouse insight: forecast in ranges"
    A single date is a promise. A range is information. "Sprint 17" invites Dana to stop thinking. "The MVP by Sprint 17 if three things hold, the rest in PI 5" tells her what you know, what you don't, and what she can influence. The forecast tool gives you one line per velocity. Run it at a pessimistic and a realistic velocity, and the gap between the lines *is* your range.

!!! checkpoint "Checkpoint"
    - [ ] Eight stories in my sandbox carry the `MVP` tag
    - [ ] At velocity 15, all eight land above the Sprint 17 line after I moved `Travel notice auto-expiry and reminders` below them
    - [ ] I saw that moving an unestimated story to the top didn't move the lines, and I moved it back

## Part 5 — Run the naive forecast on the real backlog

Your sandbox was set up for an honest forecast: future sprints only, Card Controls only. Most people run the tool on the real backlog. See what it would have told you.

1. **Boards › Backlogs**, team `Digital Accounts`, **Stories** level.
2. **View options**: **Parents** Off, **In Progress Items** Off, **Completed Child Items** Off, **Side Pane** Off, **Forecasting** On. These settings are yours alone.
3. Set the velocity to `25`, the team's average. **Don't drag anything.**

!!! challenge "Challenge: Spot the blind spots"
    Look at the first forecast line and the stories above it. Which sprint does the tool think they land in? What's already in that sprint? Then find where Card Controls starts and how far it gets by Sprint 17. List every reason this forecast is more optimistic than Part 2.

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    With **In Progress Items** Off, everything that's Active right now is hidden from the list and from the forecast. And the tool doesn't read the **Iteration Path** at all.

??? pilot "Harbor Pilot · Hint 2: Bring it into port (full solution)"
    The first line reads **Sprint 14**. Above it sit the remaining committed Online Account Opening and Spending Insights stories, all New, **20 points**. The tool pours them into Sprint 14 as if it were empty. It isn't: Sprint 14 already holds 26 points of committed work, and the tool can't see the stories that are Active or Closed, so the sprint looks empty. Card Controls then starts in Sprint 15 with almost the whole velocity to itself, and the tool shows about the same flattering answer as your sandbox at 25: stories #1 to #12 by Sprint 17.

    The blind spots, all from how the tool works:

    - **It ignores in-progress work.** Active and Resolved items don't count, so a full sprint looks empty.
    - **It ignores sprint assignments.** Only backlog order and Story Points matter.
    - **It uses one velocity for every sprint.** It knows nothing about the holiday, Noah's or Olivia's days out, or Wes ramping up.
    - **It counts unestimated items as zero.** Unestimated bugs and the four unsized Card Controls stories are free.
    - **It reserves nothing** for bugs and support.

    <!-- VERIFY: on a team that selects Sprints 9 to 20, the first forecast line is labeled Sprint 14 (the current sprint), as the World Bible states; research marks this UNCERTAIN. If it starts elsewhere, keep the point (in-progress work is invisible, so the first bucket looks empty) and adjust the sprint name. -->

<!-- SHOT: lab09-real-backlog-forecast | Boards › Backlogs, team Digital Accounts, Stories level, Forecasting on at velocity 25, In Progress Items off; the Sprint 14 line under the last remaining Spending Insights story and the first Card Controls stories below it | crop: Forecast column and titles for the first 12 rows; highlight the Sprint 14 line -->

!!! reef "Reef ahead: the forecast tool's blind spots"
    The forecast tool is a calculator, not an oracle. It does exactly one thing well: "at this velocity, in this order, which stories fit?" Everything else, from absences and committed work to in-progress items and unsized stories, is your job to feed in or subtract. That's why you set up a sandbox that starts at Sprint 15 and used a velocity you'd worked out. Run it naively and it tells an executive what she hoped to hear, with the authority of a chart.

!!! checkpoint "Checkpoint"
    - [ ] I saw the real backlog's forecast put 20 points of committed work into Sprint 14
    - [ ] I can list at least four reasons the naive forecast is more optimistic than my capacity math
    - [ ] I turned Forecasting off on Digital Accounts' backlog and dragged nothing

## Part 6 — Answer Dana

Before you could send anything, a second message arrived.

<div class="msg" data-initials="DW" data-tone="navy" markdown>
<p class="msg-head"><strong>Dana Whitfield</strong><span>EVP, Member Experience · 11:52 AM</span></p>

Thinking about this over lunch. If Digital Accounts can't do all of it, **give it to Mobile Banking**. They have the highest velocity in the program. Problem solved?
</div>

!!! challenge "Challenge: Reply in three sentences"
    Before you read on, write a three-sentence reply to Dana. Be respectful, be specific, and offer her something better.

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Look at Mobile Banking's velocity next to its count of completed stories, its planned-versus-completed, its open bugs, and the Features it already owns. Then recall where Card Controls' first story shows up in Fraud Alerts (Lab 7).

??? pilot "Harbor Pilot · Hint 2: Bring it into port (a model reply)"
    > Mobile's velocity looks highest, but points aren't comparable across teams, and Mobile's climb from 33 points to the mid-40s came with a flat 12 or so stories a sprint. They delivered 71% of their plan last sprint, carry 42 open bugs and already own two of our most at-risk Features, Check Deposit and Fraud Alerts, so moving Card Controls would put three priorities at risk instead of one. I'd rather give members the part of Card Controls they need for holiday travel by Sprint 17 with the team that knows it, and I'll send you that plan this afternoon.

!!! reef "Reef ahead: \"give it to the team with the highest velocity\""
    It sounds like a resourcing decision. It's a measurement error. Each team calibrates its own points, so 44 points in Mobile Banking and 26 in Digital Accounts aren't the same amount of work, and Mobile's points have been inflating while its story count stays flat. Worse, the "fast" team is the overloaded one: falling reliability, a growing bug count, one tester. And there's a cost even good teams pay: a team new to a codebase starts slowly and slows the original team while it learns. Adding people to late work tends to make it later. That's Brooks's law, and it applies to borrowed teams as much as to new hires, which is why Wes Turner counts for about 2 points in his second sprint, not the 4.5 a settled engineer would add.

Now give Dana the real answer.

!!! challenge "Challenge: Options, then a recommendation"
    Build a short options table: at least one option each for **scope**, **resources** and **timeline**, plus "say yes and hope" as a baseline. For each: what members get by Sprint 17, the risk, and who decides. Then write your BLUF note.

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    You have three dials: what you deliver (scope), who delivers it (resources) and when (timeline). Everything you found today constrains them: about 45 points, a 44-point MVP, a one-point buffer, four unknowns, and two committed Features Digital Accounts can't drop.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    - The MVP covers what members need for travel: locking and unlocking, real-time status, travel notices, notifications, the audit trail, accessibility and the fraud team's view.
    - "MVP minus one" gives you a real buffer: which MVP story could follow a sprint later with the least harm to members?
    - Online Account Opening is a committed PI 4 objective due in Sprint 16. Taking capacity from it moves a problem, it doesn't solve one.
    - Someone needs to size the four unestimated stories this week. Who owns that?
    - `Card lock and unlock service and API` is also the predecessor that Fraud Alerts' auto-lock story waits on (Lab 7). Putting it first helps two Features.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (model options and note)"
    | Option | What members get by Sprint 17 | Risk | Who decides |
    |---|---|---|---|
    | **0. Say yes to all of it** (baseline) | On paper, everything. In practice, about 45 of 105 points, in whatever order the work happens to land | A public miss before holiday travel, and Online Account Opening slips too | Nobody, until Sprint 17 |
    | **1. Scope: the MVP by Sprint 17**, the rest in PI 5 | Lock and unlock, travel notices, notifications, status sync, audit trail, fraud team view | About one point of buffer | Dana, with Ben Adeyemi |
    | **2. Scope: MVP minus one** (for example, the fraud team view a sprint later) | All the member-facing controls | Low; buffer of about six points | Dana and Simone (the fraud team view is a fraud operations tool) |
    | **3. Resources: borrow engineers or move it to Mobile** | Probably less, not more, by Sprint 17 | Ramp-up cost; destabilizes Mobile or the lender | Dana, but don't recommend it |
    | **4. Timeline: all of it, later** | Nothing by Sprint 17 that isn't in the MVP anyway | The remaining 61 points, plus four unsized stories, land in Sprint 20 at the earliest, even if Card Controls gets almost all of Digital Accounts' PI 5 capacity | Dana |
    | **5. Take capacity from Online Account Opening** | A few more Card Controls points | Breaks a committed PI 4 objective due in Sprint 16 | Dana and Priya; recommend against |

    **A model BLUF note** (`/Training/P##/Card Controls Outlook`):

    > **Bottom line.** We can't deliver all of Instant Card Controls by Sprint 17: it's 105 points plus four unsized stories, and Digital Accounts has about 45 points for it in Sprints 15 to 17. We *can* deliver the member-facing MVP, including card lock and unlock and travel notices, by Sprint 17, and I recommend we commit to that.
    >
    > **Forecast, as a range.** MVP (44 points) by end of Sprint 17: likely, about four chances in five, if Online Account Opening and Spending Insights finish as planned, no new work is added mid-sprint, and the four unsized stories stay out of the MVP. MVP minus the fraud team view: very likely. Full scope: late PI 5, Sprint 20 at the earliest, and that's before the four unsized stories are estimated.
    >
    > **Why not Mobile Banking.** Points aren't comparable across teams, and Mobile is already the most stretched team in the program: 71% of plan delivered, 42 open bugs, and it owns Check Deposit and Fraud Alerts.
    >
    > **Decisions needed from you.** (1) Approve the MVP as the Sprint 17 commitment, with the rest in PI 5. (2) Keep Online Account Opening's Sprint 16 date protected. (3) Ask Ben Adeyemi to size the four unestimated stories this week, starting with recurring payments on a locked card, which may belong in the MVP.
    >
    > **What I'm doing next.** Card lock and unlock goes first, because Fraud Alerts' auto-lock story also depends on it. I'll re-run this forecast at the start of each sprint and tell you the moment the buffer is gone.

!!! deliverable "Deliverable"
    A wiki page `/Training/P##/Card Controls Outlook` (a sub-page of your `P##` page under **Overview › Wiki**) with your bottom line, your forecast as a range with its conditions, your options table, the decisions you need from Dana, and your capacity worksheet as an appendix.

<!-- VERIFY: label of the wiki page menu action for adding a sub-page (e.g., "Add sub-page"). -->

!!! checkpoint "Checkpoint"
    - [ ] My reply to "give it to Mobile" is three sentences and offers a better option
    - [ ] My options table has at least one scope, one resource and one timeline option, plus a baseline
    - [ ] My note opens with the bottom line, gives a range with conditions, and asks Dana for specific decisions
    - [ ] It's saved at `/Training/P##/Card Controls Outlook`

## Knowledge check

<div class="quiz" markdown>

**At velocity 25, the forecast shows 12 Card Controls stories landing by Sprint 17. Why shouldn't you take that to Dana?**

- [ ] The forecast tool can't see beyond two sprints
- [x] 25 is the team's whole velocity in a normal sprint. Card Controls gets about 15 a sprint after absences, committed work and a bug allowance
- [ ] Digital Accounts' velocity is too stable to trust
- [ ] The forecast tool only works for Features, not stories

<div class="quiz-why" markdown>
The forecast is only as honest as the velocity you type in. Capacity math turns "the team does 25" into "this Feature gets about 45 over three sprints." The tool can't do that subtraction for you.
</div>

</div>

<div class="quiz" markdown>

**You drag an unestimated story to the top of the backlog and the forecast lines don't move. What's the right conclusion?**

- [ ] The story is small enough not to matter
- [ ] The forecast already allows for it
- [x] The tool treats it as zero points, so the forecast can't tell you whether it fits until it's estimated
- [ ] Forecasting is disabled for unestimated stories

<div class="quiz-why" markdown>
The tool sums Story Points, and a blank adds nothing. Four of Card Controls' twenty stories are unsized, and one of them, recurring payments on a locked card, may matter to members a great deal. Estimate before you promise.
</div>

</div>

<div class="quiz" markdown>

**Dana says: "Give it to Mobile Banking, they have the highest velocity." What's the strongest reason not to?**

- [ ] Mobile Banking doesn't work on cards
- [ ] Digital Accounts would lose its velocity
- [x] Velocity isn't comparable across teams, and Mobile is the most overloaded team in the program
- [ ] It would need a new Delivery Plan

<div class="quiz-why" markdown>
Each team sizes its own points, and Mobile's points have inflated while its story count stayed flat. Its plan reliability is 71%, its bug count has grown fivefold, and it owns two at-risk Features already. Moving work to the busiest team makes the whole program later.
</div>

</div>

## Captain's log

!!! log "Captain's log"
    1. When did someone last ask you "can we do all of it by…?" How did you answer, and how did it turn out?
    2. Does your organization forecast from velocity alone, or does anyone subtract absences, committed work and support load first?
    3. How many items in your biggest backlog have no estimate? What would your forecast say if they were sized?
    4. Which of your teams would you describe as "slow"? Is it slow, or is it predictable?
    5. How would your sponsor react to a range instead of a date? What would make the range easier for them to accept?

!!! bonus "Extra knots"
    1. **Required velocity.** In your sandbox, restore the original order and raise the velocity until every estimated story lands by Sprint 17. You need **35**, and at that velocity all four unestimated stories land too, for free. Compare 35 with Digital Accounts' best-ever sprint for *all* its work.
    2. **Size the unknowns.** Give the four unestimated stories your own placeholder estimates in the sandbox, restore the original order and forecast at velocity 25. How many sprint lines does the full scope need? That's how many sprints of Digital Accounts' *entire* capacity all of Card Controls costs. Does it change your PI 5 range?
    3. **Protect the predecessor.** In your sandbox at velocity 15, which sprint does `Card lock and unlock service and API` land in? Now check that against your capacity worksheet: how many points does Card Controls really get in Sprint 15, once the committed work comes first? Fraud Alerts' auto-lock story needs the API by Sprint 16. Draft the one-line message you'd send Hannah Cole and Ben Adeyemi so the two dates are agreed, not assumed.

## Key takeaways

- Velocity is a rate for a normal sprint. Capacity is how much of it you'll actually get. Subtract absences, committed work and support load before you forecast.
- The forecast tool is a calculator: one velocity, backlog order and Story Points. It ignores in-progress work, sprint assignments and unestimated items, so feed it honest inputs.
- Order is scope. Moving one "should" below the MVP turned a miss into a fit without changing a single estimate.
- Forecast in ranges with conditions. A single date is a promise; a range is information a sponsor can act on.
- Never compare velocity across teams, and be wary of moving work to the "fastest" team. It's usually the busiest one.

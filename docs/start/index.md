---
title: Welcome Aboard
description: How the HarborPoint labs work, your participant ID, and what to check before Day 1.
---

# Welcome aboard

You already know your way around Azure DevOps. This course is not about where the buttons are. It's about what a manager can **see**, **conclude** and **decide** with the data that is already sitting in Boards.

For three days you'll work inside **HarborPoint Financial**, a member-owned financial cooperative in the middle of a big transformation program. Its delivery data lives in a real Azure DevOps project: six teams, twenty-four Features, five sprints of history, and every messy, realistic problem you've ever had to explain to a VP.

<div class="msg" data-initials="RE" data-tone="teal" markdown>
<p class="msg-head"><strong>Ruth Ellison</strong><span>Program Manager, METP · 7:55 AM</span></p>

Welcome to Project Lighthouse. A word of advice from someone who's run more programs than she cares to count: **the dashboard is never the territory.** Learn to ask *how do we know?* and you'll be fine. Grab a coffee, set your crew number, and I'll see you in the briefing.
</div>

## How the three days flow

| Day | Theme | You'll leave able to… |
|---|---|---|
| **1 · Charting the Waters** | Finding answers in Azure DevOps | Trace any Feature to the portfolio priority it serves, read a team's real workload at Feature level, build reusable management queries and charts |
| **2 · The Lighthouse** | Dashboards, metrics and cross-team visibility | Build dashboards that answer management questions, read delivery metrics without being fooled, untangle cross-team dependencies |
| **3 · Setting the Course** | Forecasting, personas and strategic decisions | Forecast honestly with ranges, prioritize by member impact, fix the data your reports depend on, brief leadership on the next PI |

## The rhythm of every lab

Each lab is a **mission** with the same shape, so you always know where you are:

1. **Mission briefing**: the situation, your role, and what "done" looks like.
2. **Speed runs**: think you know this already? Prove it against the clock and skip ahead.
3. **Guided parts and challenges**: the hands-on work, ending in a judgment call.
4. **Harbor Pilot hints**: three tiers of help, from a nudge to the full solution.
5. **Checkpoints**: observable outcomes you tick off. Your progress is saved.
6. **Knowledge check and Captain's log**: test your judgment, then connect it to your own job.

### Try the components

These are live. Go ahead and click them.

!!! speedrun "Speed run · 2 minutes"
    Without looking anything up: name **three things** a Feature-level manager can learn from a backlog that a sprint taskboard will never tell them.

<div class="timer" data-minutes="2" data-label="Speed run"></div>

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Think about *time* (what's due when), *alignment* (what serves which priority), and *completeness* (how much is really left).

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    Picture the **Features** backlog with a **Progress by Story Points** rollup column, the **Target Date** column and **Parents** turned on.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    A few good answers:

    - **How far along each Feature really is**, using rollup progress by points and not by optimism.
    - **What's due soon versus how much is left**, comparing Target Date with remaining points.
    - **Which work serves which portfolio priority**, and which work serves *none* (orphan stories).
    - **Where the portfolio order and the team's actual effort disagree.**

!!! insight "Lighthouse insight"
    Most status meetings argue about **opinions** of progress. Azure DevOps already holds the **evidence**: dates, states, links, history. Your edge as a manager is knowing which evidence answers which question, and where it lies to you.

!!! reef "Reef ahead: the green dashboard"
    A dashboard can be green on the outside and red on the inside, a "watermelon". Every lab includes at least one trap like this. Fall into it on purpose here, so you don't fall into it on Monday.

<div class="quiz" markdown>

**A team's velocity doubled in three sprints, and stories completed per sprint stayed flat. What is the most likely explanation?**

- [ ] The team doubled its productivity
- [x] Average story size (estimates) grew, a pattern often called point inflation
- [ ] The team stopped estimating bugs
- [ ] The velocity chart is broken

<div class="quiz-why" markdown>
Velocity is a sum of **estimates**, not a measure of output. When the *count* of items finished stays flat while points climb, the yardstick changed, not the speed. You'll meet a team exactly like this on Day 2.
</div>

</div>

!!! checkpoint "Checkpoint: try one"
    - [ ] I opened all three Harbor Pilot hints above (no shame, that's what they're for)
    - [ ] I answered the knowledge check

## Your participant ID

Your instructor will give you a **participant ID** (for example `P07`). Many things you create in Azure DevOps are named with it so that twenty managers can work in one project without colliding. In the labs it appears as `P##`. **Save your ID here** (or with the **Crew** chip in the header) and every `P##` on this site is filled in for you.

<div class="hp-pid-form"></div>

| You create… | Where / named | Example |
|---|---|---|
| Shared queries | `Shared Queries/Training/P##/` | `Shared Queries/Training/P##/Features at risk` |
| Dashboards | Project dashboard named `P## - …` | `P## - Digital Banking Command Center` |
| Delivery Plans | `P## - …` | `P## - Fraud Alerts Plan` |
| Wiki pages | `/Training/P##/…` | `/Training/P##/Sprint Delivery Report` |
| Work items | Only in your sandbox area `HarborPoint\Training\P##` | `P## - Member Onboarding Redesign` |

!!! warning "Look, but don't touch"
    The six HarborPoint delivery teams' backlogs, boards, estimates, ordering and settings are **shared by everyone in the room**. Treat them as **read-only**. Anything you change, you change for twenty colleagues. All hands-on changes happen in your **sandbox** (`HarborPoint\Training\P##` and the **P## Sandbox** team), where you can't break anything that matters.

## Sea states (difficulty)

| Sea state | What to expect |
|---|---|
| <span class="hp-sea hp-sea--calm"><span class="hp-sea__bars"><i></i><i></i><i></i><i></i></span>Calm</span> | Guided steps with challenges along the way |
| <span class="hp-sea hp-sea--choppy"><span class="hp-sea__bars"><i></i><i></i><i></i><i></i></span>Choppy</span> | A mix of guided work and challenges you solve yourself |
| <span class="hp-sea hp-sea--rough"><span class="hp-sea__bars"><i></i><i></i><i></i><i></i></span>Rough</span> | Mostly challenges, with Harbor Pilot hints if you need them |
| <span class="hp-sea hp-sea--storm"><span class="hp-sea__bars"><i></i><i></i><i></i><i></i></span>Storm</span> | Open-ended. You decide the approach and defend it |

## Before you set sail

!!! checkpoint "Pre-flight checklist"
    - [ ] I can sign in to the training organization at the URL my instructor shared, and open the **HarborPoint** project
    - [ ] I have **Basic** access. **Boards › Queries** shows a **Charts** tab on a saved query (Stakeholder access can't do that)
    - [ ] I know my participant ID and saved it on this page
    - [ ] I can see my sandbox area `HarborPoint\Training\P##` and the **P## Sandbox** team
    - [ ] I skimmed [Meet HarborPoint](harborpoint.md) and the [environment map](environment.md)

!!! tip "Use two windows"
    Keep these instructions on one side of your screen and Azure DevOps on the other. Most labs flip between the two constantly.

## Progress and privacy

Checkpoints, completed labs and your participant ID are stored **only in this browser** (local storage). Nothing is sent anywhere. To start over:

<button type="button" class="hp-btn hp-btn--line" data-hp-reset>Reset my lab progress</button>

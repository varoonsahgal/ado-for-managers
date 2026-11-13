---
title: "Why Is the Dashboard Wrong?"
lab: 11
day: 3
module: "Module 11 · Management Best Practices and Reporting Governance"
duration: 60
sea_state: rough
role: "Acting Program Manager, METP"
summary: "Member Support's dashboard says the team has collapsed. It hasn't. Find every data and query defect, fix them in your sandbox, and stop it happening again."
---

!!! briefing "Mission briefing"
    The **Member Support - Delivery Health** dashboard has been circulating with the program pack. Its velocity chart reads 18, 17, 19, then 13, then 8. Its open-work tile keeps climbing, and it shows zero open P1 bugs. Anyone who reads it concludes that Member Support has fallen off a cliff over two sprints. Some people already have.

    You've seen a hint of this before. In Lab 3, a Member Support Feature turned up in your at-risk query although its work finished a PI ago. Now it's your program and your problem. Somewhere between what the team did and what the dashboard shows, the record broke. Your job is to find exactly where, prove it, repair a copy of it in your sandbox, and put practices in place so it doesn't happen again. You'll do all of that without touching Member Support's real items.

    **Done looks like:** a defect log with evidence for at least 8 of the 12 planted defects, a reconciled velocity, a repaired sandbox with before-and-after numbers on `P## - Sandbox Health`, a data-quality watchlist, and five practices plus a 15-minute weekly routine that would have prevented all of it.

<div class="msg" data-initials="CD" data-tone="coral" markdown>
<p class="msg-head"><strong>Carmen Diaz</strong><span>Director, Member Support · 7:36 AM</span></p>

Your dashboard says we've collapsed. My team has never worked harder. We've been an engineer short since Kyle left in Sprint 12, and we still ship every sprint. I've had two calls this week asking whether Member Support needs "intervention". Either the dashboard is wrong or I am, and I'd like to know which before Dana reads it again.
</div>

<div class="msg" data-initials="LF" data-tone="gold" markdown>
<p class="msg-head"><strong>Leo Fischer</strong><span>PMO Reporting Analyst · 7:52 AM</span></p>

That's my dashboard, sorry. I set it up for the Sprint 13 review and I've been on four other reports since. The queries are in `Shared Queries/PMO Reporting`. You can open them, but you can't save over them, so please Save As into your own folder if you change anything. I'll fix the real one with whatever you find. Be gentle with me.
</div>

## What you'll walk away with

- Tell a **delivery** problem from a **data** problem in minutes, using the evidence Azure DevOps already holds
- Recognize the dozen ways a dashboard lies: states, estimates, people, iterations, areas, tags, Feature states, duplicates, query logic, widget settings and permissions
- Fix the record at its source, then prove the fix with before-and-after numbers
- Build a small watchlist that catches bad data before it reaches an executive
- Recommend governance that sticks: working agreements, templates, rules, notifications, ownership and permissions, without turning hygiene into surveillance

## Before you set sail

- **Read-only today:** everything that belongs to Member Support. That means the **Member Support - Delivery Health** dashboard (you aren't on the team, so you can view it but not edit it), Leo's queries in `Shared Queries/PMO Reporting/`, and Member Support's backlog, board, items and **Velocity** report.
- **Yours to fix:** the miniature copy in your sandbox. Its Feature is `P## - Omnichannel Service Requests (sandbox)` in `HarborPoint\Training\P##`, and every item title starts `P## - `. Your copies of Leo's queries are in `Shared Queries/Training/P##/Lab 11 - Inherited queries/`.
- **One shared corner:** two of your sandbox bugs were deliberately filed in the parent area `HarborPoint\Training`, alongside everyone else's. Touch only the ones with **your** prefix.
- **You'll create:** fixed queries prefixed `Fixed - ` in `Shared Queries/Training/P##/`, a `Watchlist` sub-folder, the project dashboard `P## - Sandbox Health`, and the wiki page `/Training/P##/Dashboard Remediation`.
- **Time-box:** 60 minutes. Part 1: 18. Part 2: 5. Part 3: 12. Part 4: 10. Part 5: 7. Part 6: 8. If you fall behind, build three watchlist queries instead of six. Protect Part 6.

## Part 1 — Read the dashboard like a detective

Start where Dana starts: the dashboard, read cold.

!!! speedrun "Speed run · 4 minutes"
    Open **Overview › Dashboards** and find **Member Support - Delivery Health**. Don't open anything behind it yet. Write down, in plain words, the **five claims** the dashboard is making about Member Support, the way an executive skimming it would read them.

<div class="timer" data-minutes="4" data-label="Speed run"></div>

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    One claim per tile: velocity trend, current sprint, completed work, open work, open P1 bugs, omnichannel progress, burndown. Read the titles as the dashboard's author meant them.

??? pilot "Harbor Pilot · Hint 2: Bring it into port (full solution)"
    Roughly: (1) velocity has collapsed from about 18 to 8 in two sprints; (2) the team completed little in the "current" sprint, and the burndown agrees; (3) open work keeps growing; (4) quality is fine, with zero open P1 bugs; (5) omnichannel progress is modest. Hold on to that list. Most of it is false, and one claim is the dangerous kind: it's false in the *reassuring* direction.

<!-- SHOT: lab11-ms-dashboard | Overview › Dashboards › Member Support - Delivery Health (team dashboard, Member Support), full view: Markdown header "Maintained by Leo Fischer, PMO", query tiles for the five MS queries, Velocity widget (18, 17, 19, 13, 8), Sprint Burndown showing Sprint 13 dates | crop: whole dashboard; highlight the Velocity widget and the Open P1 bugs tile showing 0 -->

Now go behind every tile. Leo's dashboard has **twelve** planted defects. Some live in the **data** (the items), some in the **queries**, some in the **widgets**, and one in **permissions**.

!!! challenge "Challenge: The defect hunt"
    Find **at least 8 of the 12** defects without changing anything that belongs to Member Support. For each one, log the evidence somewhere you can paste into a wiki page later:

    | # | Defect | Type (data / query / widget / permission) | Evidence (item, query clause or widget setting) | Effect on the dashboard |
    |:-:|---|---|---|---|

    **Scoring:** 1 point for each defect with evidence, plus 1 for the right type. That's 24 points available. 20 or more is harbor-master work. Under 12, open Hint 1.

    You may build any read-only queries you like in **My Queries** or your `P##` folder. Running a query never changes data.

??? pilot "Harbor Pilot · Hint 1: Eleven places a defect can hide"
    Check each of these for Member Support (`Area Path` `Under` `HarborPoint\Member Support`):

    1. **States.** Is "done" work really Closed?
    2. **Estimates.** Do finished and upcoming stories have Story Points?
    3. **People.** Is everyone in **Assigned To** still at HarborPoint? (Check `/Program/Team Directory`, and Carmen's message.)
    4. **Iterations.** Is any active work still sitting in a sprint that has ended?
    5. **Areas.** Is any Member Support work filed outside Member Support's area?
    6. **Tags.** Is one idea spelled more than one way?
    7. **Feature states.** Do the Features' states match their children?
    8. **Duplicates.** Is any story on the backlog twice?
    9. **Query logic.** Open each PMO query in its **Editor** tab. What does each clause really ask?
    10. **Widget settings.** Which sprint is each sprint-based widget showing?
    11. **Permissions.** Does every tile load for you?

??? pilot "Harbor Pilot · Hint 2: The detective's kit"
    Flat queries, all with `Area Path` `Under` `HarborPoint\Member Support` unless noted. Add **Iteration Path**, **Story Points**, **Tags**, **Assigned To** and **Changed Date** as columns.

    | Looking for | Clauses to add |
    |---|---|
    | Done but not closed | `Work Item Type` `=` `User Story`, `State` `=` `Resolved` |
    | Missing estimates | `Work Item Type` `=` `User Story`, `Story Points` `=` *(leave Value blank)*, `State` `<>` `Removed` |
    | A departed owner | `Assigned To` `Contains` `Kyle Morgan` |
    | Zombies | `State` `=` `Active`, `Changed Date` `<` `@Today - 14` |
    | Misfiled work (**drop the area clause**) | `Area Path` `=` `HarborPoint` |
    | Tag drift | three queries: `Tags` `Contains` `omnichannel`, then `omni-channel`, then `omnichanel` |
    | Duplicates | sort by **Title**, or `Title` `Contains Words` `status tracker` |

    For **Feature states**, open **Boards › Backlogs**, team `Member Support`, **Features** level, and add **Progress by Story Points**. For **widgets**, read the date range on the burndown. For **query logic**, open each `PMO Reporting` query and select **Editor**.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    | # | Defect | Type | Evidence | Effect |
    |:-:|---|---|---|---|
    | 1 | **Done but left in Resolved** | Data | 6 stories in **Resolved**: 2 from Sprint 12 (5 points), 3 from Sprint 13 (8 points) and `Unified request intake form` in Sprint 14 | Velocity credits only Closed work: 13 and 8 instead of 18 and 19 |
    | 2 | **Missing Story Points** | Data | `Request category taxonomy cleanup` is Closed in Sprint 13 with no points (it should be 3), plus 3 New stories: `Member notifications on request updates`, `Agent workload balancing`, `Co-browse for complex requests` | Velocity undercounts by 3, and any forecast is unreliable |
    | 3 | **Departed owner** | Data | 4 items assigned to **Kyle Morgan**, who left in Sprint 12: 2 Active (`Escalation rules for priority members`, `Agent presence indicator`) unchanged for 25+ days, plus 2 New under Callback Scheduling | Work looks staffed. Nobody is doing it |
    | 4 | **Zombies in a past sprint** | Data | 3 stories still **Active** in **Sprint 12**: Kyle's two plus `Request attachment virus scanning` (Nora Fitzgerald) | Invisible on the current board, but counted as open work |
    | 5 | **Wrong area** | Data | 2 **Priority 1** bugs at the root area `HarborPoint`: `Chat disconnects after 60 seconds`, `Service request emails sent twice` | The **Open P1 bugs** tile shows **0** |
    | 6 | **Tag drift** | Data | `omnichannel` on 6 stories, `omni-channel` on 3, `omnichanel` on 2 | The omnichannel tile counts 6 of 11 |
    | 7 | **Feature states not maintained** | Data | **Secure Messaging & Chat** is **New**, though its children are 2 Closed, 1 Resolved and 2 Active. **Agent Knowledge Base** is **Active** at 100%, with all 15 children Closed and a target of Sprint 12 | Portfolio views show finished work as in flight, and started work as not started |
    | 8 | **Duplicate** | Data | `Service request status tracker` twice: one Active (Leila Ahmadi), one New and unassigned, created on Sprint 14 day 1 | Scope is double-counted |
    | 9 | **Hard-coded sprint** | Query | `MS - Current sprint work` and `MS - Completed this sprint` use `Iteration Path` `=` `HarborPoint\PI 4\Sprint 13` | "Current" is last sprint |
    | 10 | **"Open" means `<> Closed`** | Query | `MS - Open work` uses `State` `<>` `Closed` | It counts 4 Removed and 6 Resolved items as open: **10** too many |
    | 11 | **Burndown on the wrong sprint** | Widget | The Sprint Burndown widget is set to Sprint 13, not `@CurrentIteration` | A finished sprint, presented as now |
    | 12 | **Private query on a shared dashboard** | Permission | A tile bound to a query in its author's **My Queries** | Everyone but Leo sees an error instead of a number |

    `MS - Open P1 bugs` is correct as a query. Its zero comes from data filed in the wrong place, which is why #5 is a data defect.

    <!-- VERIFY: (a) whether defect #12 was provisioned (it is optional in the World Bible); if not, score out of 22; (b) the exact error text on a tile bound to another user's My Queries query ("Widget failed to load" or a permissions message); (c) that Assigned To Contains works on the seeded plain-string identity "Kyle Morgan"; (d) that Area Path = HarborPoint returns exactly the 2 root-area bugs. -->

<!-- SHOT: lab11-leo-query-editor | Boards › Queries › Shared Queries/PMO Reporting/MS - Current sprint work, Editor tab, clauses Area Path Under HarborPoint\Member Support and Iteration Path = HarborPoint\PI 4\Sprint 13 | crop: the clause grid; highlight the hard-coded Iteration Path value -->

!!! checkpoint "Checkpoint"
    - [ ] I wrote down the dashboard's five claims before I investigated
    - [ ] My defect log has at least 8 defects, each with evidence and a type
    - [ ] I changed nothing that belongs to Member Support

## Part 2 — Rebuild the true numbers

Carmen asked a yes-or-no question: is the dashboard wrong, or is she? Answer it with arithmetic.

!!! challenge "Challenge: Reconcile 13 and 8"
    Open **Boards › Backlogs**, team `Member Support`, **Stories** level, **Analytics** › **Velocity** › **View full report**. Explain, point by point, how a team that truly finished **18** points in Sprint 12 and **19** in Sprint 13 shows **13** and **8**. Then say what happened to **Planned** over the same sprints.

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Velocity credits one thing: points on stories that reached **Closed** within the sprint. List every way a finished story can fail that test.

??? pilot "Harbor Pilot · Hint 2: Bring it into port (full solution)"
    | Sprint | Truly done | Left in Resolved | Closed with no points | Velocity shows |
    |---|:-:|:-:|:-:|:-:|
    | 12 | 18 | −5 (2 Omnichannel Service Requests stories) | | **13** |
    | 13 | 19 | −8 (3 stories: 5 points of Omnichannel Service Requests, 3 of Secure Messaging & Chat) | −3 (taxonomy cleanup) | **8** |

    **Planned** stayed flat at 20 and 21, so the team didn't plan less. Completion didn't fall either. The **recording** of completion fell. Run your "done but not closed" query from Part 1 and the evidence is right there: finished stories still parked in sprints that have ended.

    <!-- VERIFY: how the Sprint 12 and 13 bars show the Resolved stories and the Active zombies (expected: as Incomplete, since Resolved for User Story is In Progress category); and, if items are closed now, whether they appear as Completed Late in Sprints 12 and 13 rather than restoring Completed to 18 and 19. -->

<!-- SHOT: lab11-velocity-ms | Boards › Backlogs › Member Support, Stories, Analytics › Velocity full report, Sum of Story Points, last 6 iterations: Planned vs Completed for Sprints 9 to 14 | crop: chart; annotate Sprint 12 (13) and Sprint 13 (8) against flat Planned -->

!!! insight "Lighthouse insight: the chart is right, the data is wrong"
    Nothing in this lab is a bug in Azure DevOps. The Velocity widget does exactly what it promises: it sums Story Points on Closed items. Every number on Leo's dashboard is computed correctly from records that are wrong. That's the uncomfortable truth about reporting. A dashboard is a **contract**. The team promises to keep states, estimates, owners, sprints and areas true. The report promises to read them faithfully. When either side breaks the deal, the chart stays crisp and confident, and it's wrong.

!!! reef "Reef ahead: blaming the team for a reporting defect"
    Did your speed-run list say "Member Support is in trouble"? That's the trap the dashboard set, and two people fell into it this week by calling Carmen about "intervention". Read the evidence again. The team kept finishing about 18 to 19 points a sprint, while one engineer down. What fell apart was **closing** work and **keeping records**, and Leo's queries amplified it. There is a real conversation to have with Member Support about hygiene. "Your delivery collapsed" isn't it. If you open with that, you lose Carmen's trust and you learn nothing about the cause.

!!! checkpoint "Checkpoint"
    - [ ] I can show, point by point, how 18 became 13 and 19 became 8
    - [ ] I can tell Carmen in one sentence that her delivery didn't collapse, and what did break

## Part 3 — Repair the record in your sandbox

Your sandbox holds a miniature of Member Support's mess: one Feature, 13 stories, 3 bugs and 2 Removed items, with defects 1 to 8 planted in it. Fix the data first. The queries come next.

1. **Record your "before" numbers.** Run each query in `Shared Queries/Training/P##/Lab 11 - Inherited queries/` and write down its count:

    | Inherited query | Before (expected) |
    |---|---|
    | `Current sprint work` | **4** (the Sprint 13 stories) |
    | `Completed this sprint` | **2** (5 points, one of them unestimated) |
    | `Open P1 bugs` | **0** |
    | `Open work` | **14** rows from the Lab 11 set, plus your Lab 9 and Lab 10 work in the same area |
    | `Omnichannel stories` | **3** |

    <!-- VERIFY: the inherited query names and counts against the provisioned artifacts. Counts assume the sandbox bugs are not in Sprint 13 or Sprint 14; if they are, add them. "Open work" has no type filter, so it also includes the Lab 11 Feature and any Lab 9/10 sandbox items. -->

2. **Open the full set.** Save a scratch flat query in **My Queries**: `Area Path` `Under` `HarborPoint\Training\P##` OR (`Area Path` `=` `HarborPoint\Training` AND `Title` `Contains` `P##`). Add the columns **Work Item Type**, **State**, **Assigned To**, **Iteration Path**, **Area Path**, **Story Points**, **Tags**, **Parent** and **Changed Date**. Group the second pair of clauses.

!!! challenge "Challenge: Repair the record"
    Fix all eight data defects in your sandbox. Each fix that changes an owner, a sprint or a state gets a one-line **Discussion** comment saying why. In real life, that comment is what stops someone undoing your fix next week.

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Work through your defect log, rows 1 to 8, and find each defect's twin in the sandbox. For each one, decide the **true** state of the world before you click: is it done, who owns it, when will it happen, where does it belong?

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    - Multi-select rows in query results and use **Edit** to change State or Iteration Path on several items at once. The rows stay **bold** until you select **Save items**.
    - Kyle Morgan has left, and you can only pick real identities, so **unassign** his items. Don't assign them to yourself to make the report look staffed.
    - When nobody is working on a zombie, the honest place for it is the backlog (`Iteration Path` `HarborPoint`) in **New**.
    - For the duplicate, keep the item with work in progress and remove the other, leaving a link behind so the history makes sense.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    | # | Sandbox item(s) | Fix |
    |:-:|---|---|
    | 1 | `P## - Request intake form`, `P## - Request status page` (Resolved, Sprint 13) | **State** `Closed`. Comment: *"Finished in Sprint 13; closing so it counts as done."* |
    | 2 | `P## - Category taxonomy cleanup` (Closed, no points), `P## - Member notifications` (New, no points) | **Story Points** `3` on the first (its real twin is a 3). Estimate the second, and comment *"Estimate to confirm at refinement."* |
    | 3 | `P## - Escalation rules`, `P## - Presence indicator` (Kyle Morgan) | Clear **Assigned To**. Comment: *"Kyle Morgan left in Sprint 12. Needs an owner decision from the PO."* |
    | 4 | The same two plus `P## - Attachment scanning` (Active, Sprint 12) | **Iteration Path** `HarborPoint`, **State** `New`. Comment: *"Not in progress; back to the backlog for re-planning."* |
    | 5 | `P## - Chat disconnects after 60 seconds`, `P## - Request emails sent twice` (P1 bugs in `HarborPoint\Training`) | **Area Path** `HarborPoint\Training\P##`. Only yours. |
    | 6 | `P## - Request status page` (`omni-channel`), `P## - Secure file upload` (`omnichanel`) | Remove the wrong tag with its **x** and add `omnichannel` |
    | 7 | `P## - Omnichannel Service Requests (sandbox)` (New) | **State** `Active`. It has Closed and Active children. |
    | 8 | `P## - Routing rules engine`, twice | On the **New** one: **Links** › **Add link** › **Existing item**, **Link type** **Duplicate Of**, pointing at the Active one. Then **State** `Removed`, with a comment. |

    <!-- VERIFY: the Duplicate link-type labels in New Boards Hub ("Duplicate" / "Duplicate Of") and which one to choose on the item being removed; that State can move Active > New for User Story in the Agile process. -->

!!! warning "Don't fix Member Support"
    You've now found every defect in Member Support's real data, and every one of them is a two-click fix. Leave them. Those items are Carmen's team's record, twenty colleagues share them, and a fix made by an outsider without the team is how working agreements die. Your findings go to Carmen and Leo as a recommendation in Part 6.

!!! checkpoint "Checkpoint"
    - [ ] I recorded the five "before" counts before I changed anything
    - [ ] My sandbox has no Resolved stories, no unestimated stories, no Kyle Morgan, no Active items in Sprint 12, no misfiled P1 bugs, one spelling of `omnichannel`, an Active Feature and one `Routing rules engine`
    - [ ] Every owner, sprint or state change carries a comment

## Part 4 — Fix the queries and prove it

Now repair the instruments. Open each inherited query, change it, and use **More actions** › **Save as** into `Shared Queries/Training/P##/` with the prefix `Fixed - `. Keep the originals so you can compare.

!!! challenge "Challenge: Five queries, honestly"
    Rewrite all five inherited queries so they would survive next sprint, next quarter and the next reorganization. Then add one new one, `Fixed - Completed last sprint`. Before you save `Fixed - Current sprint work`, run it once with the **P## Sandbox** team in the macro, and explain the result.

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Two defects are about **time** (a sprint typed in by hand), one is about **meaning** (what "open" means), and one is about **vocabulary** (tags). One of the five queries was never wrong.

??? pilot "Harbor Pilot · Hint 2: Set the heading"
    Use `@CurrentIteration` and `@CurrentIteration - 1`, which carry a **team parameter**. Use `State` `Not In` `Closed,Removed`. For tags, use a grouped **Or** across the three spellings. And ask why your sandbox team's current sprint comes back empty. It selects only Sprints 15 to 20, from Lab 9.

??? pilot "Harbor Pilot · Hint 3: Bring it into port (full solution)"
    All are **Flat list of work items**, and all keep `Area Path` `Under` `HarborPoint\Training\P##`.

    | Saved as | Change | Expected, after Part 3 |
    |---|---|---|
    | `Fixed - Current sprint work` | `Iteration Path` `=` `@CurrentIteration`, team `Member Support`; add `State` `<>` `Removed` | **4** stories: `Routing rules engine`, `Chat transcript export`, `Secure file upload`, `Typing indicators` |
    | `Fixed - Completed this sprint` | Same, plus `State` `=` `Closed` | **1**: `Chat transcript export` |
    | `Fixed - Completed last sprint` *(new)* | `@CurrentIteration - 1`, team `Member Support`, plus `State` `=` `Closed` | **4** stories, **13** points (it was 2 stories and 5 points) |
    | `Fixed - Open P1 bugs` | None. The query was right; the data was wrong | **2** |
    | `Fixed - Open work` | `State` `Not In` `Closed,Removed`; `Work Item Type` `In` `User Story,Bug` | **10** Lab 11 rows (7 stories, 3 bugs), plus your Lab 9 and Lab 10 stories |
    | `Fixed - Omnichannel stories` | `State` `<>` `Removed`, plus the grouped tag clauses below | **5** |

    | Group | And/Or | Field | Operator | Value |
    |:-:|:--|:--|:--|:--|
    | | | Area Path | Under | `HarborPoint\Training\P##` |
    | | And | State | <> | `Removed` |
    | ┌ | And | Tags | Contains | `omnichannel` |
    | │ | Or | Tags | Contains | `omni-channel` |
    | └ | Or | Tags | Contains | `omnichanel` |

    **Why the sandbox team returns nothing:** `@CurrentIteration` means "the sprint of *this team* whose dates include today". Your sandbox team plans only future sprints, so it has none. The macro is only as good as the team behind it, and a query copied with **Save as** keeps its old team until you change it. In the real fix, Leo would use team `Member Support`. After your tag clean-up, the original one-tag query also returns 5. The Or-group is a bridge, and the vocabulary is the fix.

    <!-- VERIFY: where the @CurrentIteration team parameter appears in the New Boards Hub query editor and how "- 1" is entered; whether any sandbox bugs sit in Sprint 14 (add them to the first expected count if so). -->

??? info "Under the hood: WIQL for the current-sprint fix"
    ```sql
    SELECT [System.Id], [System.Title], [System.State], [Microsoft.VSTS.Scheduling.StoryPoints]
    FROM WorkItems
    WHERE [System.TeamProject] = @project
      AND [System.AreaPath] UNDER 'HarborPoint\Training\P##'
      AND [System.IterationPath] = @currentIteration('[HarborPoint]\Member Support')
      AND [System.State] <> 'Removed'
    ```

!!! reef "Reef ahead: fixing the chart instead of the data"
    The fastest way to make **Open P1 bugs** show 2 is to widen it to `Area Path` `Under` `HarborPoint\Training`. Try it, then look at what comes back: every participant's misfiled bugs. With 30 sandboxes, that's up to **60**. On the real dashboard the same shortcut, `Under HarborPoint`, pulls in every team's P1 bugs. A query that compensates for bad data gets wrong in a new way each time the data changes. Fix the data, keep the query honest, and catch misfiled work with a watchlist (Part 5).

### Validate on a dashboard

Build a project dashboard, **Overview › Dashboards** › **+ New Dashboard**, named `P## - Sandbox Health` (**Project Dashboard**). Add:

- a **Markdown** widget: the owner (you), its purpose, a review cadence ("every Monday"), the definitions *done = Closed* and *open = not Closed or Removed*, and your before-and-after table from this Part
- **Query Tile** widgets for each `Fixed - ` query. Give `Fixed - Open P1 bugs` a rule that turns it red at 1 or more.
- a **Sprint Burndown** widget: **Team** `Member Support`, **Select Iteration** `@CurrentIteration`. That's defect 11, fixed on a dashboard you own.

<!-- SHOT: lab11-sandbox-health | Overview › Dashboards › P## - Sandbox Health: Markdown before/after table, Query Tiles for the Fixed queries (Open P1 bugs = 2 in red, Completed last sprint = 4), Sprint Burndown for Member Support on @CurrentIteration (Sprint 14) | crop: whole dashboard; highlight the before/after table and the red P1 tile -->

!!! checkpoint "Checkpoint"
    - [ ] Six `Fixed - ` queries are saved in `Shared Queries/Training/P##/`, and `Fixed - Completed last sprint` returns 4 stories and 13 points
    - [ ] I can explain why `@CurrentIteration` for my sandbox team returns nothing
    - [ ] `P## - Sandbox Health` shows before and after, and its burndown is on Sprint 14

## Part 5 — Build a watchlist

Fixing the data once is a cleanup. Catching it every week is management. A watchlist is a handful of queries whose healthy answer is **zero**.

!!! challenge "Challenge: Six queries that should say zero"
    Create the folder `Shared Queries/Training/P##/Watchlist` and build **at least three** of these against **Member Support's real area**. Running queries is read-only. Record each count:

    1. Active work nobody has touched in 14 days
    2. Stories that have sat in Resolved for more than 5 days
    3. Stories with no Story Points that aren't Removed
    4. Active work still sitting in one of the last three sprints
    5. Open work assigned to someone who has left
    6. Anything filed at the project's root area

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Every one of these is a date clause, a blank-value clause or an iteration macro. You built most of them in the Part 1 detective's kit. Now save them with names a team lead would understand in two seconds.

??? pilot "Harbor Pilot · Hint 2: Bring it into port (full solution)"
    All flat, with `Area Path` `Under` `HarborPoint\Member Support` except #6.

    | # | Name | Clauses | Member Support today |
    |:-:|---|---|:-:|
    | 1 | `Stale active work` | `Work Item Type` `In` `User Story,Bug`; `State` `=` `Active`; `Changed Date` `<` `@Today - 14` | **3** |
    | 2 | `Resolved but not closed` | `Work Item Type` `=` `User Story`; `State` `=` `Resolved`; `Resolved Date` `<` `@Today - 5` | **5** (6 if `Unified request intake form` was resolved more than 5 days ago) |
    | 3 | `Unestimated stories` | `Work Item Type` `=` `User Story`; `Story Points` `=` *(blank)*; `State` `<>` `Removed` | **4** |
    | 4 | `Active in a past sprint` | `State` `=` `Active`; grouped **Or**: `Iteration Path` `=` `@CurrentIteration - 1`, `- 2`, `- 3`, each with team `Member Support` | **3** |
    | 5 | `Assigned to a leaver` | `Assigned To` `Contains` `Kyle Morgan`; `State` `Not In` `Closed,Removed` | **4** |
    | 6 | `Root-area work` | `Area Path` `=` `HarborPoint` (no Under) | **2** |

    Number 5 is the weakest, because a query can't know who has left. The durable fix is an off-boarding step: *reassign open work before the last day*. Number 6 works for every team at once. Put it on the program dashboard.

    <!-- VERIFY: watchlist #2 count depends on when "Unified request intake form" was seeded as Resolved; #1 assumes no other Member Support item is Active and untouched for 14+ days. -->

<!-- SHOT: lab11-watchlist | Boards › Queries › Shared Queries/Training/P##/Watchlist, folder expanded showing the six queries, with "Active in a past sprint" open in Editor (grouped @CurrentIteration - 1/-2/-3 with team Member Support) and Results showing 3 rows | crop: folder tree plus clause grid -->

!!! checkpoint "Checkpoint"
    - [ ] My `Watchlist` folder holds at least three queries, each with today's Member Support count
    - [ ] I can say which watchlist query a process rule could replace, and which it couldn't

## Part 6 — Make it stop happening

Carmen doesn't need a better chart. She needs a team that keeps its record true, and a PMO that reads it carefully, without either of them spending Friday afternoons on it. Choose your levers carefully. Some are cheap and team-owned. Some change the whole organization.

| Lever | What it prevents here | Who can set it up | Watch out for |
|---|---|---|---|
| **Working agreement and Definition of Done** (`/Practices/Working Agreements and Definition of Done`) | #1, #2, #7: "Done means Closed. Estimate before Active. The PO closes the Feature." | The team | It already exists, and Member Support hasn't adopted it. An agreement nobody reads is decoration |
| **Team work item templates** | #2, #6: pre-filled area, tags and criteria skeleton | Team members, for their own team | Team-scoped; other teams don't see them |
| **Inherited process rules**, for example on User Story: `A work item state changes to` `Active` › `Make required` `Story Points` | #2 | Project Collection Administrators | Applies **immediately to every project** on that process. Rules **can't** target Area or Iteration Path, so #4 and #5 still need the watchlist |
| **Notifications and Follow** | #7, #8: Follow the Features you report on, and subscribe to state changes in your area | Anyone (personal); team admins (team subscriptions) | Notification filters don't support `@CurrentIteration`. Too many emails and people stop reading |
| **Dashboard ownership and review** | #9, #11: a named owner, a "last reviewed" line, a monthly widget check | The dashboard owner | A dashboard with no owner decays one sprint at a time |
| **Shared queries and permissions** | #12: dashboard tiles only from shared folders the audience can read | Folder owners (**Security** on the folder) | Viewers without **Read** on a query see an error, not a number |
| **Off-boarding checklist** | #3: reassign open work before someone's last day | The line manager | Nobody owns it until someone writes it down |

<!-- VERIFY: the exact wording of the rule condition/action pickers in Organization settings › Boards › Process (User Story › Rules › New rule). -->

!!! reef "Reef ahead: hygiene police"
    Once a watchlist exists, someone will want it per person, ranked, in the weekly pack: "Nora has a stale item." That's when people learn to game the record instead of keeping it true. They close early, split stories to look busy, and leave out the work that's hard to estimate. Goodhart's law works on data quality too. Keep the watchlist **team-level**, look at it **with** the team, and measure success by how fast items leave it, not by who put them there.

!!! deliverable "Deliverable"
    The wiki page `/Training/P##/Dashboard Remediation` with:

    1. **Your defect log** from Part 1, with your score
    2. **The reconciliation**: 18 → 13 and 19 → 8, explained in two lines
    3. **Before and after** from your sandbox, with a link to `P## - Sandbox Health`
    4. **Five practices that would have prevented this.** Each one names the defects it prevents, who owns it, and what it costs.
    5. **A 15-minute weekly hygiene routine**: what is looked at, by whom, in which order, and what happens to each finding
    6. **A five-sentence note to Carmen and Leo**: the bottom line first, what broke, what you recommend, what you need from each of them, and what you'll check next week

??? pilot "Harbor Pilot · Hint 1: Take a bearing"
    Group the twelve defects by **who could have stopped them**: the team (states, estimates, duplicates), a manager (leavers, zombies), the dashboard owner (queries, widgets, permissions) and the platform (rules, templates). One practice per group is a good start.

??? pilot "Harbor Pilot · Hint 2: Bring it into port (full solution)"
    **Five practices (model):**

    1. **Adopt the Definition of Done, ending in Closed.** The PO closes stories at the sprint review, and closes the Feature when its last child closes. Prevents #1 and #7. Owners: Isaac Thompson and the team. Cost: five minutes a sprint.
    2. **Estimate before Active, enforced lightly.** A team agreement first; a `Make required` `Story Points` rule only if the agreement fails, and only after the process owner tests it on a copy. Prevents #2.
    3. **Close every sprint properly.** On the last day, move unfinished work to the next sprint or the backlog, and resolve duplicates at refinement. Prevents #4 and #8.
    4. **Off-board the work, not just the person.** Reassign or unassign open items before someone leaves, and run the `Root-area work` and `Assigned to a leaver` checks monthly. Prevents #3 and #5.
    5. **Give every dashboard an owner and a contract.** Use only shared queries, use macros instead of typed sprints, define "open" and "done" on the dashboard itself, and review the widgets monthly. Add a tag vocabulary on the wiki. Prevents #6 and #9 to #12.

    **The 15-minute Monday routine (model):** the team lead and PO open `P## - Sandbox Health` (or its real equivalent). Minutes 0 to 5: the six watchlist tiles. Anything above zero gets fixed on the spot or gets a named owner. Minutes 5 to 10: scan the Features' states against their rollup, and close or activate as needed. Minutes 10 to 15: one dashboard check, which rotates weekly between queries, widgets and permissions. Findings go into the team's own backlog, not into a status report.

## Knowledge check

<div class="quiz" markdown>

**A team's velocity drops from 19 to 8 in one sprint, and its Planned line is flat. What do you check first?**

- [ ] Whether the team needs extra capacity
- [ ] Whether the Velocity widget is set to the right team
- [x] Whether finished work actually reached Closed, with Story Points, in that sprint
- [ ] Whether the team has been inflating its estimates

<div class="quiz-why" markdown>
Velocity sums points on Closed items only. A sudden drop with flat planning is usually a recording problem: work left in Resolved, points left blank, items parked in old sprints. Check the data before you diagnose the team.
</div>

</div>

<div class="quiz" markdown>

**"Open P1 bugs" shows 0, and you find two P1 bugs filed at the project root. What's the best fix?**

- [ ] Change the tile's query to `Area Path Under HarborPoint` so it catches them
- [x] Move the bugs into the team's area, keep the query as it is, and add a root-area check to a watchlist
- [ ] Delete the tile, because it can't be trusted
- [ ] Add a Markdown note under the tile saying the real number is 2

<div class="quiz-why" markdown>
Widening the query pulls in every team's P1 bugs, and a note goes stale the day the data changes. Fix the record at its source, and make the class of defect visible so it can't hide again.
</div>

</div>

<div class="quiz" markdown>

**Which of today's defects could an inherited process rule actually prevent?**

- [ ] Active stories left behind in a past sprint
- [x] Stories moving to Active with no Story Points
- [ ] Work filed at the root area
- [ ] Three spellings of the same tag

<div class="quiz-why" markdown>
Rules can make a field required on a state change, but they can't target Area Path or Iteration Path, and they don't govern tag vocabulary. The others need agreements and a watchlist. Even the rule that works applies to every project on the process, so it's a governance decision, not a quick fix.
</div>

</div>

## Captain's log

!!! log "Captain's log"
    1. Which dashboard in your organization would you least like to audit the way you audited Leo's today? What's the first query you'd run?
    2. When a team's numbers look bad in your status pack, what happens next: a conversation with the team, or a conversation about the team?
    3. What does "done" mean in your tools today, and does every team mean the same thing?
    4. Who owns each of your dashboards? If the answer is "whoever built it", what happens when they move on?
    5. Which governance change would you make centrally, and which would you leave to teams? Where's the line between hygiene and micromanagement for you?

!!! bonus "Extra knots"
    1. **The honest late bar.** Add a **Velocity** widget for team `Member Support` to `P## - Sandbox Health` with **Highlight work completed late** turned on. If Carmen's team closed its old Resolved stories today, would Sprints 12 and 13 jump back to 18 and 19, or show the work as completed late? Which would you rather show Dana, and why?
    2. **Program-wide hygiene.** Copy watchlist #1 and #3 with the area clause set to `Area Path` `Not Under` `HarborPoint\Training`. Which other teams appear, and does Mobile Banking's stale work show up at 14 days or only at 7?
    3. **Write the tag vocabulary.** Draft a short `/Training/P##/Tag Vocabulary` page with the canonical tags from today and from [Lab 10](lab-10-personas.md), who may add a new tag, and how a misspelling gets retired. Tags can't be renamed in the web UI. What does that mean for your process?

<!-- VERIFY: Extra knot 1, whether "Highlight work completed late" shows recently closed items from ended sprints as Completed Late, and which sprint receives the credit. -->

## Key takeaways

- When a team's numbers fall off a cliff, suspect the record before the team. Delivery rarely collapses in one sprint. Hygiene often does.
- Fix data at the source. A query that compensates for bad data gets wrong in a new way each time the data changes.
- Typed-in sprints, "not Closed" for open, and single-spelling tags are the three most common query defects. Macros, explicit state lists and a written vocabulary prevent them.
- Every dashboard is a data-quality contract: an owner, defined terms, shared queries, and a weekly look at a watchlist whose healthy answer is zero.
- Governance has a cost and a reach. Team agreements are cheap and local. Process rules land on every project at once. Per-person hygiene scores get gamed.

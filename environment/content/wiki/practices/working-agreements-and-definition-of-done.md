# Working Agreements and Definition of Done

[[_TOC_]]

| | |
|---|---|
| Applies to | All Project Lighthouse delivery teams |
| Owner | Ruth Ellison, Program Manager, with the team Engineering Managers and Product Owners |
| Review | At each PI planning |

Program reporting is only as good as the data in Azure DevOps. Dashboards, velocity, rollups and delivery plans all read the same work items. These agreements keep that data honest so that leaders can trust what they see and teams are not judged on stale or broken numbers.

## 1. Work item hygiene

### States mean what they say

| State | Means | Moves on when |
|---|---|---|
| New | Not started | Someone starts work |
| Active | Being worked on now | Code complete and ready for testing |
| Resolved | Code complete, waiting for test or acceptance | Accepted by the Product Owner |
| Closed | Done (meets the Definition of Done) | |
| Removed | Will not be done | |

- **Close what is done.** Azure DevOps counts only **Closed** items in velocity, burndown and Feature rollups. An item left in Resolved is reported as not done. The Product Owner closes accepted items **no later than the sprint review**.
- **Keep Feature states current.** The Product Owner moves a Feature to **Active** when its first child starts and to **Closed** when its last child is accepted. Review Feature states at every sprint review.

### Every story is estimated

- No story enters a sprint without **Story Points**. Unestimated stories are refined first.
- Closed stories keep their estimate. Never clear Story Points on a finished item.
- Bugs are not normally estimated.

### Every item has a real owner

- **Assigned To** is a person currently on the team, or blank if nobody has picked it up.
- When someone leaves or changes teams, the Engineering Manager reassigns or unassigns all of their open items **within one working day**.
- Every **Priority 1** bug has a named owner within one working day of being filed.

### Close the sprint cleanly

At the end of each sprint, before the next sprint's planning:
- Every unfinished item is moved to the next sprint or back to the backlog. **No Active or New items stay in a past sprint.**
- Items that are no longer needed are set to **Removed** with a short reason.

### File work in the right place

- Every work item, including bugs, is filed in the **owning team's Area Path**. Nothing is left at the root area `HarborPoint`.
- Ruth's team triages anything found at the root area at the weekly delivery review.
- Stories have a **parent Feature**. Work with no parent is the exception and is agreed with the Product Owner.

### Use the canonical tags

Use only the tags listed below, spelled exactly as shown. Check the spelling in the tag picker before creating a new tag. New program-wide tags are agreed at the weekly delivery review.

| Tag | Use on |
|---|---|
| `PI4-Committed`, `PI5-Candidate` | Features |
| `at-risk` | Features rated Amber or Red |
| `cross-team`, `enabler`, `mandatory`, `leadership-ask` | Features |
| `blocked`, `unplanned`, `tech-debt`, `compliance` | Stories |
| `escaped-defect` | Bugs found in production |
| `omnichannel` | Member Support omnichannel stories |

### Search before you create

Before creating a story, search the backlog for an existing item. If you find a duplicate, link the two with a **Duplicate** link and set the newer one to **Removed**.

## 2. Sprint agreements

- **Limit work in progress.** Finish before starting. No one should have more than two or three items Active at once.
- **Protect the sprint.** New work added after sprint planning is tagged `unplanned` and agreed with the Product Owner, who decides what comes out to make room.
- **Reserve capacity** for bugs and support each sprint.
- **Swarm on testing** when items queue in Resolved. Developers help test rather than starting new work.
- **Raise blockers early.** Tag the item `blocked`, add a comment naming who you are waiting on, and link the dependency (Predecessor/Successor).

## 3. Definition of Ready (story)

A story is ready for sprint planning when:
- [ ] It has a clear title and description, written from the member's or user's point of view
- [ ] It has acceptance criteria
- [ ] It has Story Points
- [ ] It has a parent Feature
- [ ] It is in the owning team's Area Path
- [ ] Its dependencies are linked and the predecessor is scheduled in an earlier or the same sprint

## 4. Definition of Done (story)

A story is done, and can be **Closed**, when:
- [ ] All acceptance criteria are met
- [ ] Code is reviewed and merged
- [ ] Automated tests are written and pass
- [ ] It has been tested by QA (or by a teammate who did not write it)
- [ ] No open Priority 1 or Priority 2 bugs remain against it
- [ ] Accessibility checks pass for member-facing changes
- [ ] It is deployed to the staging environment
- [ ] The Product Owner has accepted it
- [ ] The work item is set to **Closed**, with Story Points and Assigned To still filled in

### Definition of Done (Feature)

- [ ] All child stories are Closed or Removed
- [ ] The Feature's outcome has been demonstrated at a sprint review or system demo
- [ ] Release notes and support guidance are published
- [ ] The Feature is set to **Closed** by its owner

## 5. Query and dashboard standards

Anything shared with leaders follows these rules.

- **Never hard-code a sprint.** Use `@CurrentIteration` (with the team selected) or `@CurrentIteration - 1` for the previous sprint.
- **"Open" means not Closed and not Removed.** Use `State Not In (Closed, Removed)`. Decide explicitly whether Resolved counts as open, and say so in the query name.
- **Check the area scope.** Make sure the query catches items filed in the wrong place, or pair it with a hygiene query that does.
- **Tag-based queries need canonical tags.** If a tag has variants, fix the data or include every variant.
- **Shared dashboards use Shared Queries only.** A widget bound to a query in *My Queries* shows an error to everyone else.
- **Sprint widgets follow the current sprint.** Check burndown and sprint widgets at the start of every sprint.
- **Label every widget** with what it counts and its scope, for example "Open P1 bugs, Member Support area".
- Review each shared dashboard with the team it describes before publishing it.

## Known gaps

- **Member Support has not adopted these working agreements.** The team still follows its own older conventions for closing work, tagging and sprint close. Adoption is on the program's list but has no owner or date yet.
- The **PMO Reporting** queries and the **Member Support - Delivery Health** dashboard were built before section 5 was written and have not been reviewed against it.

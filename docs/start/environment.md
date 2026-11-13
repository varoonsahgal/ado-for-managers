---
title: "Your Azure DevOps Environment"
---

# Your Azure DevOps Environment

This is the field map: where HarborPoint's work lives in Azure DevOps, which team view shows what, and where *your* work goes. Skim it once now and come back whenever a lab says "switch to the … team".

| Setting | Value |
|:--|:--|
| Service | Azure DevOps **Services** (dev.azure.com). Your instructor gives you the organization URL |
| Project | **HarborPoint** |
| Process | **Agile**: Epic › Feature › User Story, plus Bug. **No Tasks are used** |
| Bugs | Every team uses **Bugs are managed with requirements**, so bugs sit on the Stories backlog and board |
| Estimation | **Story Points** on User Stories. Bugs are normally not estimated |
| Working days | Monday to Friday |
| Now | **Sprint 14, week 2**, in **PI 4** |

## Areas: who owns what

The **Area Path** says which team owns a work item. Each delivery team owns one node; the **Training** branch holds one sandbox per participant.

```text
HarborPoint
├── Digital
│   ├── Mobile Banking
│   └── Digital Accounts
├── Security
├── Core Platform
├── Branch Experience
├── Member Support
└── Training
    └── P01 … P30        (participant sandboxes, one is yours)
```

<!-- SHOT: start-env-area-tree | Project settings › Boards › Project configuration › Areas, tree fully expanded, showing Digital (Mobile Banking, Digital Accounts), Security, Core Platform, Branch Experience, Member Support and Training › P01 to P30 | crop: tree only; highlight Training › P## -->

## Iterations: the calendar

Sprints sit under their PI node, so a sprint's full path looks like `HarborPoint\PI 4\Sprint 14`. A Feature's **Iteration Path** is the **PI** that contains its Target sprint (for example `HarborPoint\PI 4`), and its **Target Date** is the last day of that sprint.

```text
HarborPoint
├── PI 3   Sprint 9 · Sprint 10 · Sprint 11 · Sprint 12      last PI (complete)
├── PI 4   Sprint 13 · Sprint 14 · Sprint 15 · Sprint 16     current PI   ◀ Sprint 14 = now
└── PI 5   Sprint 17 · Sprint 18 · Sprint 19 · Sprint 20     next PI
```

Sprints are two weeks; a PI is four sprints. Every team's **backlog iteration** is the root, `HarborPoint`, so unscheduled work still shows on backlogs.

## Teams: pick the right lens

Almost every view in **Boards** (backlogs, boards, sprints, Velocity, CFD, `@CurrentIteration`) belongs to **one team**. The team selector at the top left of the page decides what you see. Picking the right team is the first step of nearly every lab.

| Team | Area it covers | Backlog levels | Sprints selected | Use it to see… |
|:--|:--|:--|:--|:--|
| **HarborPoint Team** (project default) | `HarborPoint`, **including sub-areas** | Epics, Features, Stories | Sprint 9 – Sprint 20 | The whole program in one place. The **Epics** backlog is the portfolio's ranked priority list. Ruth's view |
| **Digital Portfolio** | `HarborPoint\Digital`, **including sub-areas** | Epics, Features | Sprint 9 – Sprint 20 | Both digital teams' Features side by side. Priya's view |
| **Mobile Banking** | `HarborPoint\Digital\Mobile Banking` | Features, Stories | Sprint 9 – Sprint 20 | One delivery team's Features, stories, sprints and metrics |
| **Digital Accounts** | `HarborPoint\Digital\Digital Accounts` | Features, Stories | Sprint 9 – Sprint 20 | as above |
| **Security** | `HarborPoint\Security` | Features, Stories | Sprint 9 – Sprint 20 | as above |
| **Core Platform** | `HarborPoint\Core Platform` | Features, Stories | Sprint 9 – Sprint 20 | as above |
| **Branch Experience** | `HarborPoint\Branch Experience` | Features, Stories | Sprint 9 – Sprint 20 | as above |
| **Member Support** | `HarborPoint\Member Support` | Features, Stories | Sprint 9 – Sprint 20 | as above |
| **P## Sandbox** (yours) | `HarborPoint\Training\P##` | Features, Stories | **Sprint 15 – Sprint 20 only** | Your own practice backlog. You're its team administrator |

<!-- SHOT: start-env-team-selector | Boards › Backlogs with the team selector open, listing HarborPoint Team, Digital Portfolio, the six delivery teams and a P## Sandbox team | crop: selector dropdown and the level selector (Epics / Features / Stories); highlight both -->

!!! reef "Reef ahead: the wrong team"
    "My Feature is missing" is almost always a team-context problem. The **Digital Portfolio** team can't show you Security's work, and a delivery team can't show you Epics. Before you conclude that something isn't there, check the team selector and the backlog level selector.

!!! note "Your sandbox plans the future"
    Your **P## Sandbox** team selects only Sprints 15 to 20, because you use it to plan work that hasn't started. That means it has **no current sprint**: `@CurrentIteration` with your sandbox team returns nothing. When a query needs "this sprint", use a real team (such as `Mobile Banking`) as the macro's team parameter. Reading a team's sprint in a query changes nothing for that team.

## Work item types and fields

At Feature altitude you'll use a handful of fields again and again.

| Type | Fields that matter to a manager |
|:--|:--|
| **Epic** | Title, State, Assigned To (owner), Area Path, Start Date, Target Date, Business Value, Priority, Value Area (Business or Architectural), Tags |
| **Feature** | Title, State, **Assigned To** (the owning team's Product Owner), **Area Path** (owning team), **Iteration Path** (a PI node), **Start Date**, **Target Date**, **Business Value**, **Time Criticality**, **Effort**, **Risk** (`1 - High`, `2 - Medium`, `3 - Low`), **Priority** (1 = highest), Value Area, Tags, Description |
| **User Story** | Title, State, Assigned To, Area Path, Iteration Path (a sprint), **Story Points**, Priority, Tags, Acceptance Criteria. **Parent** = a Feature, or none |
| **Bug** | Title, State, Assigned To, Area Path, Iteration Path, **Priority** (1 to 4), **Severity** (`1 - Critical` to `4 - Low`), Tags, Repro Steps. Parent = a Feature, or none |

Useful system dates for queries: **Created Date**, **Changed Date** (every save), **Activated Date**, **Resolved Date**, **Closed Date** and **State Change Date**. They're set automatically as items move between states.

### States, and what Azure DevOps counts as "done"

Epics, Features and User Stories move **New → Active → Resolved → Closed** (or **Removed**). Bugs move **New → Active → Resolved → Closed**. Azure DevOps maps each state to a **state category**, and the category, not the state name, is what every chart and rollup counts.

| State | Category | Shows on backlogs? | Counts as done in rollups and velocity? |
|:--|:--|:--|:--|
| New | Proposed | Yes | No |
| Active | In Progress | Yes | No |
| Resolved | In Progress for stories and Features; Resolved for bugs | Yes | **No** |
| Closed | Completed | No (last board column) | **Yes, the only state that does** |
| Removed | Removed | No | No (excluded) |

<!-- VERIFY: state category of Resolved on Agile User Story and Feature (expected In Progress) under Organization settings › Boards › Process › Agile › User Story › States. -->

!!! insight "Lighthouse insight: Resolved is not done"
    Rollup progress bars, Velocity and burndowns credit only **Closed** items. A story sitting in **Resolved** counts as unfinished, however finished it feels to the team. When a chart and a team's story disagree, the state category is the first place to look.

### Canonical tags

Tags are free text, so spelling matters: a query for one spelling misses the others. These are the spellings HarborPoint agreed on.

| Tag | Used on | Meaning |
|:--|:--|:--|
| `PI4-Committed` | Features | Committed in PI 4 planning |
| `PI5-Candidate` | Features | Proposed for PI 5 |
| `at-risk` | Features | The owning team reports the Feature at risk |
| `cross-team` | Features | Delivered by more than one team |
| `enabler` | Features | Architectural or platform enabler |
| `mandatory` | Epics, Features | Regulatory, non-discretionary |
| `leadership-ask` | Features | Requested directly by the EVP |
| `blocked` | Stories | Waiting on someone else |
| `unplanned` | Stories | Added after sprint planning |
| `tech-debt` | Stories | Engineering hygiene |
| `compliance` | Stories | Exam work |
| `escaped-defect` | Bugs | Found in production |

Some labs ask you to add tags to items in your sandbox. The lab names the tag.

### Link types

| Link | Means | Where it shows up |
|:--|:--|:--|
| **Parent / Child** | "is part of": Epic › Feature › Story or Bug | Backlog hierarchy, **Parents** view option, rollup columns, tree queries |
| **Predecessor / Successor** | "must finish before / after" | Dependency lines on Delivery Plans, direct-links queries |
| **Related** | context only | Work item **Links** tab. Never drawn on a plan |
| **Duplicate / Duplicate Of** | the same work recorded twice | Work item **Links** tab |

## What's already built for you

### Shared queries (**Boards › Queries › All**)

| Folder | Query | What it's for |
|:--|:--|:--|
| `Shared Queries/HarborPoint Reports/` | **Portfolio - Epics and Features** | Tree of Epics and their Features |
| | **Portfolio - Features by target date** | Flat list of Features, sorted by Target Date |
| | **Program - Current sprint (all teams)** | Stories and bugs in the current sprint across the program |
| | **Program - Open bugs** | Open bugs with Area, Priority and Severity |
| `Shared Queries/PMO Reporting/` | Member Support reporting queries | Maintained by Leo Fischer. They feed the Member Support dashboard. You'll meet them on Day 3 |
| `Shared Queries/Training/` | your `P##` folder | Where you save every shared query you build |

<!-- SHOT: start-env-shared-queries | Boards › Queries › All tab, Shared Queries expanded to show HarborPoint Reports (4 queries), PMO Reporting and Training › P## | crop: folder tree; highlight Training › P## -->

### Dashboards (**Overview › Dashboards**)

| Dashboard | Type | What it's for |
|:--|:--|:--|
| **HarborPoint Program Overview** | Project dashboard | The program at a glance. You'll explore it on Day 1 and critique it on Day 2 |
| **Member Support - Delivery Health** | Member Support team dashboard | Built by Leo Fischer for Carmen Diaz's team |

### Delivery Plan (**Boards › Delivery Plans**)

**HarborPoint Program Plan** shows all six delivery teams at the **Features** level on one calendar, with three markers: **PI 4 System Demo** (end of Sprint 16), **PI 5 Planning** (start of Sprint 17) and **Regulatory exam fieldwork** (start of Sprint 18). Open it, read it, never drag on it. Build your own plans when you need to change settings.

### Project wiki (**Overview › Wiki**, `HarborPoint.wiki`)

| Page | What's there |
|:--|:--|
| `/Home` | The program hub |
| `/Program/Program Charter` | Priorities, initiatives and governance cadence |
| `/Program/PI 4 Objectives` | Each team's PI 4 objectives, with business value and committed vs stretch |
| `/Program/Team Directory` | Who's who |
| `/Teams/Digital Accounts Availability` | Who's out in the coming sprints |
| `/Research/Onboarding Research Findings` | Member onboarding research |
| `/Research/Member Pulse Survey Q3` | The latest member survey |
| `/Personas/Dee Harmon`, `/Personas/Jordan Reyes`, `/Personas/Amara Okafor` | Starter member personas |
| `/Practices/Working Agreements and Definition of Done` | How teams say they work |
| `/Templates/Status Report`, `/Templates/Executive Briefing (BLUF)`, `/Templates/Persona Canvas` | Templates for your write-ups (copy-ready versions are on the [Templates](../resources/templates.md) page) |
| `/Training/` | Your `/Training/P##/…` pages go here |

## Your conventions

Twenty managers share one project, so everything you create carries your participant ID. Save your ID on the [Welcome page](index.md#your-participant-id) and every `P##` on this site fills itself in.

| You create… | Where, and how it's named | Example |
|:--|:--|:--|
| Shared queries | `Shared Queries/Training/P##/` (scratch work can go in **My Queries**) | `Shared Queries/Training/P##/Features at risk` |
| Dashboards | Project dashboard named `P## - <name>` | `P## - Digital Banking Command Center` |
| Delivery Plans | `P## - <name>` | `P## - Fraud Alerts Plan` |
| Wiki pages | `/Training/P##/<page>` | `/Training/P##/Sprint Delivery Report` |
| Work items | Only in your sandbox area `HarborPoint\Training\P##`; Feature titles start with `P## - ` | `P## - Member Onboarding Redesign` |

Your sandbox isn't empty. It comes with practice copies used on Day 3, such as `P## - Instant Card Controls (planning copy)` and `P## - Omnichannel Service Requests (sandbox)`, and your query folder may already hold a `Lab 11 - Inherited queries` subfolder. Leave them alone until the lab that uses them. If `Shared Queries/Training/P##/` doesn't exist yet, you'll create it in [Lab 3](../day-1/lab-03-query-toolkit.md).

!!! warning "The read-only rule"
    The six delivery teams' work items, backlog order, estimates, boards and team settings are shared by everyone in the room. **Never** edit, move, re-order or re-estimate their items, and never change their team or board settings. Per-user things are fine: column options, view options, filters, and the settings of in-context reports only change *your* view. Everything you change for real happens in your sandbox or under your `P##` names.

## Access you need

| You need | Why | How to check |
|:--|:--|:--|
| **Basic** access | Stakeholder access can't use query charts, the Forecasting tool, Capacity, Analytics views, or save shared queries | A saved query shows a **Charts** tab |
| **Contributor** in HarborPoint | Create your own project dashboards and Delivery Plans. You can edit only what you create | **+ New Dashboard** works under **Overview › Dashboards** |
| **Contribute** on `Shared Queries/Training` | By default only Project Administrators can save shared queries. The instructor granted this folder to you | You can save a query into `Shared Queries/Training/P##/` |
| **Team administrator** of `P## Sandbox` | Lets you change your sandbox team's own settings | Your sandbox team's settings open without a permissions error |

If any check fails, tell your instructor before Lab 1. It's a two-minute fix now and a lost lab later.

## Where do I find…

| I want to… | Go to |
|:--|:--|
| See the portfolio's ranked Epics | **Boards › Backlogs**, team `HarborPoint Team`, level **Epics** |
| See a team's Features and how far along they are | **Boards › Backlogs**, pick the team, level **Features**, then **Column Options** › **+ Add a rollup column** |
| See Features under their Epics | Backlog **View options** › **Parents** On |
| Find stories with no parent Feature | Stories backlog with **Parents** On: they're grouped under **Unparented Stories** at the bottom |
| See a Feature board | **Boards › Boards**, pick the team, level **Features** |
| See what a team is doing this sprint | **Boards › Sprints**, pick the team, **Backlog** or **Taskboard** tab |
| See Velocity or the CFD | **Boards › Backlogs**, pick the team, **Analytics** tab, then **View full report** on a card |
| See a sprint burndown | **Boards › Sprints**, pick the team and sprint, **Analytics** tab |
| Forecast a backlog | **Boards › Backlogs**, level **Stories**, **View options**: Parents Off, In Progress Items Off, Forecasting On (in your sandbox) |
| Build or run a query | **Boards › Queries** › **All** › **New query** |
| See dependencies on a calendar | **Boards › Delivery Plans** |
| Open a dashboard | **Overview › Dashboards** |
| Read or write wiki pages | **Overview › Wiki** |
| See who changed what, and when | Open the work item › **History** tab |
| Follow a Feature | Work item › **Follow**. Followed items appear under **Boards › Work items** › **Following** |
| See (not change) a team's areas and sprints | **Project settings › Boards › Team configuration**, team picker in the breadcrumb |
| See the full area and iteration trees | **Project settings › Boards › Project configuration** |

<!-- VERIFY: rollup quick-list label on the Features backlog ("Progress by Story Points" vs "Progress by User Story"); and that Contributors can open Project settings › Boards › Team configuration read-only. -->

## Your first five minutes

!!! checkpoint "Orientation checklist"
    - [ ] I opened the **HarborPoint** project and switched the team selector between `HarborPoint Team`, `Digital Portfolio` and one delivery team
    - [ ] On **Boards › Backlogs** for `HarborPoint Team`, I opened the **Epics** level and saw six Epics
    - [ ] On **Boards › Queries › All**, I found `Shared Queries/HarborPoint Reports` and `Shared Queries/Training`
    - [ ] I found my sandbox team `P## Sandbox` and its area `HarborPoint\Training\P##`
    - [ ] I opened **HarborPoint Program Plan** under **Boards › Delivery Plans** (looking, not dragging)
    - [ ] I saved my participant ID on the [Welcome page](index.md#your-participant-id)

<!-- SHOT: start-env-digital-features | Boards › Backlogs, team Digital Portfolio, level Features, Parents On (Epics shown above their Features), no rollup columns | crop: backlog grid, team selector and level selector -->

!!! tip "Next"
    Ready? Head to [Day 1](../day-1/index.md). Bookmark the [Query Cookbook](../resources/query-cookbook.md) and the [Metrics Field Guide](../resources/metrics-field-guide.md): you'll want both by Day 2.

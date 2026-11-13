# Program Charter: Member Experience Transformation Program (Project Lighthouse)

[[_TOC_]]

| | |
|---|---|
| Sponsor | Dana Whitfield, EVP Member Experience |
| Program Manager | Ruth Ellison |
| Technology partner | Marcus Reed, Chief Information Officer |
| Risk and compliance | Simone Laurent, Chief Risk Officer |
| PMO reporting | Leo Fischer, PMO Reporting Analyst |
| Page owner | Ruth Ellison |

## Purpose

The Member Experience Transformation Program (METP), "Project Lighthouse", is HarborPoint's multi-year program to modernize how members bank, get help and stay safe. It brings digital banking, member support, branches, security and platform work into one portfolio with one set of priorities.

We serve **1.9 million members** across **74 branches**. Every decision in this program should be explainable to a member.

## FY2027 portfolio priorities

Ranked by the Executive Committee. When priorities conflict, the higher rank wins unless the Sponsor decides otherwise.

| Rank | Strategic priority | Initiative (Epic) | Executive owner |
|---|---|---|---|
| 1 | **Protect every member** | Fraud Detection & Security | Simone Laurent, Chief Risk Officer |
| 2 | **Digital that feels human** | Digital Banking Modernization | Priya Raman, Director, Digital Banking |
| 3 | **Effortless support** | Customer Support Modernization | Carmen Diaz, Director, Member Support |
| 4 | **Branches as relationship hubs** | Branch Experience Transformation | Hector Alvarez, VP, Branch Network |
| Enabler | Platform that scales | Platform Foundations | Nadia Petrova, Platform Lead |
| Mandatory | Regulatory exam (non-negotiable date) | Compliance: Examination Readiness | Simone Laurent |

**Mandatory work** is regulatory and non-discretionary. It is resourced ahead of discretionary priorities. Regulatory **exam fieldwork begins in Sprint 18**.

**Enabler work** is funded because the ranked priorities depend on it, not because it competes with them.

## Initiatives

Each initiative is an Epic in the `HarborPoint` project. The Epic backlog of the **HarborPoint Team** holds the portfolio rank.

| Initiative (Epic) | Owning area | Executive owner | Horizon | Notes |
|---|---|---|---|---|
| Fraud Detection & Security | Security | Simone Laurent | Sprint 9 to Sprint 20 | Includes Real-Time Fraud Alerts, delivered by Mobile Banking with Security and Core Platform |
| Digital Banking Modernization | Digital | Priya Raman | Sprint 9 to Sprint 20 | Mobile Banking and Digital Accounts |
| Customer Support Modernization | Member Support | Carmen Diaz | Sprint 9 to Sprint 19 | |
| Branch Experience Transformation | Branch Experience | Hector Alvarez | Sprint 9 to Sprint 20 | |
| Platform Foundations | Core Platform | Nadia Petrova | Sprint 9 to Sprint 16 | Architectural enabler |
| Compliance: Examination Readiness | Security | Simone Laurent | Sprint 12 to Sprint 18 | Added in Sprint 12. Mandatory |

## Scope and altitude

- The program plans and reports at **Feature** level. Features roll up to the initiatives above.
- User Stories and Bugs are team-level detail. Program reports use them as **evidence** for a Feature-level conclusion, not as the conclusion itself.
- Every Feature has an owning team (its Area Path), a Start Date, a Target Date and an owner (the owning team's Product Owner).

## Governance cadence

| Forum | Cadence | Chair | Attendees | Purpose |
|---|---|---|---|---|
| **Weekly delivery review** | Weekly | Ruth Ellison | Engineering Managers and Product Owners of the six delivery teams, Leo Fischer | Feature status and RAG, dependencies, risks, escalations |
| **Sprint planning** | Day 1 of every sprint | Each team's Product Owner | Team | Commit sprint scope |
| **Sprint review** | Last day of every sprint | Each team's Product Owner | Team, stakeholders, Program Manager (optional) | Demo completed work, accept or reject stories, update Feature state |
| **Executive steering** | Every other sprint | Dana Whitfield | Marcus Reed, Simone Laurent, initiative owners, Ruth Ellison | Portfolio rank, target-date changes for committed Features, capacity moves between teams |
| **PI planning** | Every 4 sprints, at the start of the PI | Ruth Ellison | All teams, initiative owners | Agree PI objectives, committed vs stretch, cross-team dependencies |
| **PI system demo** | End of every PI | Ruth Ellison | All teams, Sponsor, initiative owners | Demonstrate integrated outcomes, score PI objectives |

Upcoming:
- **PI 4 System Demo:** end of Sprint 16
- **PI 5 Planning:** start of Sprint 17
- **Regulatory exam fieldwork:** begins Sprint 18

## Status and RAG definitions

RAG is assessed per Feature and rolled up to initiative and program level. A RAG rating must be backed by evidence in Azure DevOps (rollup progress, dependency status, open bugs, carry-over), not by opinion.

| Status | Definition | Expected action |
|---|---|---|
| **Green** | On track to meet the Target sprint. No unresolved blocking dependency. Progress is consistent with the remaining time. | Report normally |
| **Amber** | At risk. The Target sprint is achievable only with intervention (scope, sequencing or capacity), or a dependency is late or unconfirmed, or the data cannot be trusted. | Owner presents a recovery plan at the next weekly delivery review. Tag the Feature `at-risk` |
| **Red** | Will miss the Target sprint without a decision above team level, or a predecessor is planned to finish after the successor's Target, or there is a direct risk to member safety or exam readiness. | Escalate the same day (see below). Tag the Feature `at-risk` |

Rules:
- Changing the **Target Date of a committed Feature** requires agreement from the initiative owner and notice to the Program Manager. Record the reason in the Feature's Discussion.
- "Done" means **Closed**. Azure DevOps rollups and velocity count only Closed items. Resolved is not done.

## Escalation path

| Level | Who | When to use | Expected response |
|---|---|---|---|
| 1 | Team Engineering Manager and Product Owner | Issues the team can solve within its own sprint | Within the sprint |
| 2 | Program Manager (Ruth Ellison) | Cross-team dependencies, Amber Features, capacity conflicts between teams | Next weekly delivery review, or same day for Red |
| 3 | Initiative executive owner | Trade-offs within an initiative, scope changes, target changes for committed Features | Within 2 working days |
| 4 | Sponsor (Dana Whitfield) and Executive steering | Portfolio re-ranking, moving people between teams, changes affecting more than one initiative | Next executive steering, or an ad hoc session for Red items |

Anything that affects **member safety (fraud)** or **exam readiness** is also raised directly with **Simone Laurent** on the same day, at any level.

## Roles and decision rights

| Decision | Decides | Consulted | Informed |
|---|---|---|---|
| Portfolio rank of initiatives | Executive Committee / Sponsor | Initiative owners, Program Manager | All teams |
| Feature priority within an initiative | Initiative owner | Product Owners | Program Manager |
| Sprint scope | Team (Product Owner) | Engineering Manager | Program Manager |
| Committed Feature target change | Initiative owner | Program Manager, dependent teams | Sponsor |
| Moving people between teams | Sponsor | Directors, Engineering Managers | Program Manager |

## Sources of truth

- **Portfolio rank:** Epic backlog of the HarborPoint Team
- **Feature schedule and dependencies:** Delivery Plan **HarborPoint Program Plan**
- **Program health:** dashboard **HarborPoint Program Overview**
- **Standard reports:** Shared Queries > **HarborPoint Reports**
- **PI commitments:** [PI 4 Objectives](/Program/PI-4-Objectives)

## Program leadership transition

Ruth Ellison retires at the **end of PI 4**. Dana Whitfield will name an acting Program Manager to take over the weekly delivery review and PI 5 Planning.

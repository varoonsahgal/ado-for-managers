---
title: "Templates"
---

# Templates

Copy-ready Markdown for the write-ups managers produce every week. Each one pastes straight into an Azure DevOps wiki page. Use the copy button at the top right of each block.

!!! tip "How to use these templates"
    - Create your page under **Overview › Wiki** at `/Training/P##/<page name>`, paste the template, then replace every `[bracketed]` prompt.
    - The project wiki also holds `/Templates/Status Report`, `/Templates/Executive Briefing (BLUF)` and `/Templates/Persona Canvas`. They follow the same shape as the versions here. If a lab points you at the wiki copy, use that one.
    - Link evidence instead of pasting screenshots: a link to a shared query or dashboard stays current, a screenshot goes stale by Friday.
    - Delete any section you don't need. A short page that gets read beats a complete one that doesn't.

| Template | Use it when | Length |
|:--|:--|:--|
| [Status Report](#status-report) | Regular delivery status for a sponsor or steering group | 1 page |
| [Executive Briefing (BLUF)](#executive-briefing-bluf) | An executive needs a decision or a straight answer | ½ to 1 page |
| [Options Matrix](#options-matrix) | Several ways forward, and someone has to choose | 1 table + 5 sentences |
| [Dependency Escalation](#dependency-escalation) | Another team's work is putting your Feature at risk | ½ page |
| [PI Outlook](#pi-outlook) | Planning what the next PI can realistically hold | 1 to 2 pages |
| [Persona Canvas](#persona-canvas) | Designing or prioritizing for real members | 1 page per persona |
| [Monday Readout](#monday-readout) | Your weekly five-minute read of a team or portfolio | 5 bullets |
| [Data Hygiene Routine](#data-hygiene-routine) | Keeping the data behind your reports honest | 15 minutes a week |
| [Dashboard Design Canvas](#dashboard-design-canvas) | Before you add a single widget | 1 page |

## Status Report

**How to use it:** one page, Feature level, honest colors. Fill the RAG definitions in once and keep them identical every week, or the colors mean nothing. Every RAG call needs a one-line reason and a link to the evidence.

```markdown
# Status Report: [Initiative or team] · [Sprint NN], [PI N]

**Owner:** [your name] · **Audience:** [sponsor / steering group] · **Overall:** 🟢 / 🟡 / 🔴

## RAG definitions (unchanged every week)
| Color | Means |
|---|---|
| 🟢 Green | On track for the Target Date with the current scope and capacity. No help needed |
| 🟡 Amber | At risk. A recovery plan exists and is within the team's control. Watch closely |
| 🔴 Red | Will miss the Target Date or scope without a decision from outside the team |

## Headline
[One or two sentences: the single most important thing the reader must know.]

## Features
| Feature | Target | Progress (points done / total) | RAG | Why (one line) |
|---|---|---|---|---|
| [Feature title] | [Sprint NN] | [nn / nn] | 🟢 | [reason] |
| [Feature title] | [Sprint NN] | [nn / nn] | 🟡 | [reason] |

## Delivered since last report
- [Feature or meaningful story closed, and why it matters to members]

## Risks and issues
| Risk / issue | Impact | Owner | Next step | Needed by |
|---|---|---|---|---|
| [description] | [which Feature, how much] | [name] | [action] | [Sprint NN] |

## Decisions or help needed
- [Specific ask, from whom, by when. Or "None this week."]

## Evidence
- Dashboard: [link] · Query: [link] · Delivery Plan: [link]
```

!!! reef "Reef ahead: the watermelon"
    Green outside, red inside. If every Feature is green but the remaining points exceed what the team can finish before the Target Date, the report is wrong, not the data. Check progress against time before you pick a color.

## Executive Briefing (BLUF)

**How to use it:** **B**ottom **L**ine **U**p **F**ront. The first three lines must stand alone: if the reader stops there, they still know the answer and what you need from them. Ask for decisions by name.

```markdown
# [Topic]: Executive Briefing · [Sprint NN]

**To:** [name, role] · **From:** [your name] · **Decision needed by:** [Sprint NN / meeting]

## Bottom line
[One sentence: the answer. "We will / won't make X by Y because Z."]

## What I need from you
1. [Decision 1, phrased so the answer is yes or no]
2. [Decision 2]

## Why (the evidence, three bullets maximum)
- [Fact, with a number and a link]
- [Fact, with a number and a link]
- [Fact, with a number and a link]

## Options considered
| Option | Effect on the date | Cost / who pays | Risk |
|---|---|---|---|
| [Recommended] | | | |
| [Alternative] | | | |
| Do nothing | | | |

## What happens next
- If you agree: [next step, owner, when]
- If not: [what we'll do instead]

## Confidence
[High / Medium / Low], because [one line]. Range: [best case] to [worst case].
```

## Options Matrix

**How to use it:** list at least four real options plus a **do-nothing baseline**, so the decider can see the cost of not deciding. Every option needs a named decider: whoever's priority gives way. Close with a recommendation in exactly five sentences.

```markdown
# Options: [The problem in one line]

**Decision owner:** [name] · **Decide by:** [Sprint NN]

| Option | What changes (items, teams) | Effect on the date | Risk | Who pays (what gives way) | Who decides |
|---|---|---|---|---|---|
| 0. Do nothing (baseline) | | | | | |
| 1. Re-sequence | | | | | |
| 2. Reduce scope | | | | | |
| 3. Add or move capacity | | | | | |
| 4. Move the date | | | | | |
| 5. Change the dependency | | | | | |

## Recommendation (five sentences)
1. **Bottom line:** [the situation in one sentence]
2. **Recommend:** [the option or combination]
3. **Cost:** [what gives way, and who feels it]
4. **Decision needed:** [exactly what, from whom]
5. **Prevention:** [how we stop this happening again]
```

## Dependency Escalation

**How to use it:** for when your Feature waits on another team's work and talking it through hasn't fixed it. Stay factual and blame-free; the other team is usually doing exactly what its priorities told it to. Send it to both team leads and the person who owns the competing priorities.

```markdown
# Dependency escalation: [Successor Feature] waits on [Predecessor item]

**Raised by:** [name] · **To:** [team leads], cc [priority owner] · **Raised in:** [Sprint NN]

## The dependency
| | Item | Team | Scheduled | State |
|---|---|---|---|---|
| Waits on (predecessor) | [title, link] | [team] | [Sprint NN / unscheduled] | [state] |
| Blocked (successor) | [title, link] | [team] | [Sprint NN] | [state] |

## Impact
- [Which Feature and portfolio priority is affected]
- [Date effect if nothing changes: "lands Sprint NN instead of Sprint NN"]

## What we've already tried
- [Conversation, workaround, mock or contract]

## Options (see options matrix if needed)
1. [Option, who pays]
2. [Option, who pays]

## Ask
[Specific decision, from whom, by when.]

## Evidence
- Delivery Plan: [link] · Dependency query: [link] · Relevant comments: [links]
```

## PI Outlook

**How to use it:** forecast in **ranges**, from each team's own recent velocity, after adjusting for known capacity changes. State assumptions explicitly. A range with named assumptions survives an executive's questions; a single number doesn't.

```markdown
# PI [N] Outlook · prepared in [Sprint NN]

**Owner:** [your name] · **Audience:** [sponsor / Executive Committee]

## Bottom line
[One sentence: what PI N can realistically deliver, and the one decision that changes it most.]

## Capacity by team (ranges)
| Team | Recent velocity (low–high) | Sprints | Adjustments (days off, people out, mandatory work) | PI capacity range |
|---|---|---|---|---|
| [Team] | [nn–nn] | 4 | [e.g. 2 holiday days, 1 person out 5 days] | [nn–nn] |

## Candidate Features vs capacity
| Feature | Priority / value | Owning team | Remaining size | Fits? (likely / possible / unlikely) |
|---|---|---|---|---|
| [Feature] | [rank, BV] | [team] | [nn pts / unestimated] | [likely] |

## Assumptions
- [Velocity based on Sprints NN–NN]
- [Mandatory work reserved: nn% of team X until Sprint NN]
- [Unestimated items: nn stories, sized at roughly nn as a placeholder]

## Risks to the outlook
- [Dependency, people, unknown scope]

## Decisions needed
1. [What to commit vs stretch]
2. [Where capacity should move, if anywhere]
```

## Persona Canvas

**How to use it:** one canvas per persona. Ground every line in research, not opinion, and cite it. Then turn the needs into persona-tagged stories with acceptance criteria.

```markdown
# Persona: [Name], [age]

> "[A quote that captures how they feel about banking with us.]"

| | |
|---|---|
| **Who they are** | [life stage, work, relationship with HarborPoint] |
| **How they bank** | [branch / mobile / online / mix; devices; times of day] |
| **Digital confidence** | [low / medium / high, with an example] |
| **Goals** | [what they're trying to get done] |
| **Frustrations** | [where we fail them today] |
| **Fears** | [fraud, being rushed, losing a person to talk to…] |
| **What "great" looks like** | [in their words] |
| **Evidence** | [research page, survey figure, link] |

## Needs → stories
| Need | Story ("As [persona], I want…, so that…") | Tag | Acceptance criteria (headline) |
|---|---|---|---|
| [need] | [story] | `persona-[name]` | [criteria] |

## Design guardrails
- Do: [what must be true for this persona]
- Don't: [what would push them away]
```

## Monday Readout

**How to use it:** five bullets, five minutes, Feature level, every Monday. Write it from the data (rollups, the sliding sprint window, the risk queries), then read it to your manager before they ask. The [Query Cookbook](query-cookbook.md) has the queries.

```markdown
# Monday Readout: [Team or portfolio] · [Sprint NN], week [1/2]

1. **Delivered:** [Features closed or meaningfully advanced since last week]
2. **At risk:** [Features that may miss their Target, with the one-line reason]
3. **Blocked / waiting:** [cross-team dependencies or blocked items, and who owns the unblock]
4. **Attention:** [urgent unowned bugs, stale work, overloaded people, unplanned work]
5. **My ask / my next move:** [the one thing I need, or will do, this week]

Evidence: [dashboard link] · [query links]
```

## Data Hygiene Routine

**How to use it:** a 15-minute weekly routine for each team or portfolio you report on. Run the queries, fix what you own, and *ask* the owning team about the rest. Never fix another team's data for them; that hides the habit that caused it.

```markdown
# Weekly data hygiene · [Team / scope] · [Sprint NN], week [1/2]

**Time-box:** 15 minutes · **Owner:** [name]

## Run the watchlist (expected: close to zero)
- [ ] Active items not changed in 14+ days: [n] → [action]
- [ ] Resolved for 5+ days but not Closed: [n] → [action]
- [ ] Open stories with no Story Points in current or next sprint: [n] → [action]
- [ ] Open items still in a past sprint: [n] → [action]
- [ ] Open items at the root area (no team): [n] → [action]
- [ ] Urgent bugs (Priority 1–2) with no owner: [n] → [action]
- [ ] Work assigned to people no longer on the team: [n] → [action]

## Check the portfolio fields
- [ ] Every open Feature has a Target Date, Effort and an owner
- [ ] Feature states match their children (all children Closed → Feature Closed)
- [ ] Tags use the agreed spellings
- [ ] Stories completed this sprint have a parent Feature (or a reason not to)

## Check the reports
- [ ] Dashboard widgets point at the current sprint (macros, not hard-coded names)
- [ ] Every dashboard tile's query is shared and readable by its audience

## Follow-ups
| Item | Who I asked | By when |
|---|---|---|
| | | |
```

## Dashboard Design Canvas

**How to use it:** design questions first, widgets last. Every widget must answer one question for one audience. If you can't name the decision a widget informs, leave it off.

```markdown
# Dashboard design: [P## - Dashboard name]

**Audience:** [who opens it, how often] · **Owner:** [who maintains it] · **Review cadence:** [e.g. every PI]

## The questions it must answer (max 6)
| # | Question | Decision it informs | Widget | Source (query / team / backlog) | Healthy looks like |
|---|---|---|---|---|---|
| 1 | [e.g. Which Features are due in 14 days and not done?] | [escalate or not] | [Query Results] | [shared query link] | [0–2 items] |
| 2 | | | | | |

## Layout (top = most important)
- Row 1: [Markdown header: purpose, owner, links, legend]
- Row 2: [headline tiles]
- Row 3: [trend and flow charts]
- Row 4: [detail lists]

## Data-quality contract
- [Which fields and states this dashboard depends on, and who keeps them right]

## What this dashboard is NOT for
- [e.g. comparing teams' velocity, judging individuals]
```

!!! insight "Lighthouse insight"
    A template is a thinking tool, not a form. The value is in the prompts it forces you to answer: *what's the bottom line, who decides, what does it cost, how do we know?* Skip a prompt only when you're sure the reader won't ask it.

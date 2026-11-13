# HarborPoint training environment

This tooling builds the seeded Azure DevOps Services project **HarborPoint** for *Azure DevOps for Managers*. The project uses the Agile process. Its realistic, backdated history makes velocity, burndown, CFD, cycle time, rollups and delivery plans show exactly what the labs describe.

| Piece | Module | What it does |
|---|---|---|
| Generator | `harborpoint.generate` | Turns the World Bible into `out/dataset.json` (the `harborpoint-dataset/1` contract). It is deterministic. |
| Verifier | `harborpoint.verify` | Recomputes every checkable number from the generated revisions and fails on any mismatch. It writes `out/facts.md` and `out/facts.json`. |
| Provisioner | `harborpoint.provision` | Applies the dataset to an org over REST. It is idempotent and resumable, and has `--dry-run` and `--steps pilot`. |
| REST client | `harborpoint.ado` | Handles Basic auth, pacing, retries with backoff and `Retry-After`, and error hints. It also holds the pure request builders. |
| Simulator | `harborpoint.simulator` | An in-memory Azure DevOps stand-in. Dry-run and the unit tests use it, so nothing touches the network. |
| Content | `content/artifacts.yaml`, `content/wiki/**` | Shared queries, dashboards, the delivery plan and the wiki pages (World Bible section 8). |

## Prerequisites

- **A dedicated organization** for the class, on Azure DevOps Services (`https://dev.azure.com/ORG`). Don't use a production org: the seed creates fictional people as plain-text *Assigned To* values and bypasses work item rules.
- **The person running the seed is a Project Collection Administrator.** That role is needed to:
  - create the project,
  - use *Bypass rules on work item updates*, which backdating requires,
  - use *Suppress notifications for work item updates*.
- **Participants have Basic access.** Stakeholder access can't use query charts, forecasting, Analytics views, or save shared queries.
- **The org time zone** is US or Europe (*Organization settings > Overview > Time zone*). Seeded events happen between 16:00 and 19:00 UTC, which keeps the same calendar day in those zones. An Asia/Pacific zone shifts history by one day.
- **Python 3.11** with `requests` and `PyYAML`, using the repo's `.venv`. Run every command from `environment/`:

  ```bash
  cd environment
  PY=../.venv/bin/python
  ```

## Personal access token (PAT)

1. Sign in to the org as the Project Collection Administrator. Open **User settings > Personal access tokens > + New Token**.
2. Fill in the token:
   - **Name:** `harborpoint-seed`.
   - **Organization:** the class org. Don't pick *All accessible organizations*, because global PATs are being retired.
   - **Expiration:** 7 days.
3. Choose **Custom defined**, then **Show all scopes**, and tick these scopes:

| PAT UI scope | Level | Scope id | Needed for |
|---|---|---|---|
| Project and Team | Read, write, & manage | `vso.project_manage` | Project and teams |
| Work Items | Read & write | `vso.work_write` | Areas, iterations, team settings, work items, links, queries, plans |
| Wiki | Read & write | `vso.wiki_write` | Project wiki pages |
| Team Dashboard | Read & manage | `vso.dashboards_manage` | Dashboards and widgets |
| Security | Manage | `vso.security_manage` | Contribute on `Shared Queries/Training` |
| Graph | Read | `vso.graph` | Looking up the Contributors group |
| Identity | Read | `vso.identity` | ACE identity descriptor |
| Analytics | Read | `vso.analytics` | Pilot OData checks (optional) |
| Member Entitlement Management | Read & write | `vso.memberentitlementmanagement_write` | Only with `--participant-map` |
| Graph | Read & manage | `vso.graph_manage` | Only with `--participant-map` (team membership) |

4. Select **Create** and copy the token. It is shown only once. Store it with owner-only permissions:

   ```bash
   mkdir -p ~/.config/harborpoint && umask 077 && pbpaste > ~/.config/harborpoint/pat   # or paste with an editor
   chmod 600 ~/.config/harborpoint/pat
   ```

   Alternatively, set `export AZDO_PAT=...`. The tool never prints the PAT, and `--help` prints the same scope list.

## Commands

```bash
# 1. Generate the dataset ("now" = now; Sprint 14 started the Monday of last week)
$PY -m harborpoint.generate --participants 12 --out out/dataset.json

# 2. Verify every World Bible number against the generated history (non-zero exit on mismatch)
$PY -m harborpoint.verify out/dataset.json

# 3. Offline plan: validates the dataset and executes every step against the simulator
$PY -m harborpoint.provision --org https://dev.azure.com/ORG --dataset out/dataset.json --dry-run

# 4. Pilot on a throwaway project (see the next section)
$PY -m harborpoint.provision --org https://dev.azure.com/ORG --dataset out/dataset.json \
    --project HarborPoint-Pilot --state out/state-pilot.json --steps pilot

# 5. Full seed
$PY -m harborpoint.provision --org https://dev.azure.com/ORG --dataset out/dataset.json \
    [--order item|chronological] [--assign-map people.csv] [--participant-map participants.csv] --yes

# Unit tests (offline)
$PY -m unittest discover -s tests -v
```

**Steps**, in order (pass `--steps a,b` to run a subset; the default is all):

1. `preflight`: connection, Agile process lookup, existing project, permission notes.
2. `project`: create and poll.
3. `classification`: areas and dated iterations.
4. `teams`: areas, sprints, backlog iteration, default-iteration macro, bugs as requirements, backlog levels, working days, days off.
5. `workitems`: revision 1 is a POST and every later revision is a PATCH. Each uses `bypassRules=true&suppressNotifications=true` with backdated `System.ChangedDate`.
6. `links`: predecessor, successor and related links.
7. `queries`: folders, queries and per-participant copies, plus Contributors permissions on `Shared Queries/Training`.
8. `wiki`.
9. `dashboards`.
10. `plans`.
11. `participants`.
12. `summary`: URLs and manual follow-ups.

`pilot` and `pilot-cleanup` are special steps and always run on their own.

**Option formats:**

- **`--participants N`** (generator): creates `P01 … PNN` sandboxes. Use the class size, up to 30.
- **`--assign-map people.csv`**: maps fictional display names to identities. Without it, plain names are stored.

  ```csv
  name,identity
  Hannah Cole,Hannah Cole <hannah.cole@yourtrainingtenant.example>
  ```

- **`--participant-map participants.csv`**: adds each user with Basic access and Contributors, then makes them a member of their `P## Sandbox` team. Making them team admin is a manual step.

  ```csv
  participant,email
  P01,alex@client.example
  ```

- **`--order`**: the revision application order. The pilot tells you which one to use.
- **`--parent-links create|final`**: whether the parent link is added in revision 1 (the default) or in the links step.
- **`--experimental-widgets`**: also tries the Sprint Burndown, CFD and cycle/lead time widgets over REST.
- **`--changed-by NAME`**: sets `System.ChangedBy`. Use it only if you hit VS403417.

## Pilot first (do this once per org, before the real seed)

Backdating through `bypassRules` is documented only partly, so validate it on a throwaway project:

1. **Prepare.** Run `generate`, `verify` and `--dry-run`. All three must pass.
2. **Run the pilot.** Use the `--steps pilot` command above. It creates the project, all areas and iterations, one team (`--pilot-team`, default Mobile Banking), and one Feature plus one Story. The Story gets four backdated revisions in Sprint 13: created in the backlog, moved into the sprint and made Active on day 1, Resolved on day 4, Closed on day 7.
3. **Read the probe results.** The pilot then prints its findings:
   - whether linking a child creates a revision on the parent, and with which date;
   - the User Story state categories;
   - whether a future `ChangedDate` is rejected;
   - a **RECOMMENDATION** for `--order`.
4. **Check the UI.** Wait about 15–30 minutes for Analytics, then go through the printed checklist:
   - The story's History shows the backdated times.
   - The Activated, Resolved and Closed dates are set.
   - OData `WorkItemRevisions` shows four revisions.
   - A Velocity widget for the pilot team shows **Sprint 13: Planned 5, Completed 5**.
   - The cycle time is about 6–7 days.
   - The plain-text Assigned To renders.
5. **Delete the pilot project:** *Project settings > Overview > Delete*. Then run the full seed with the recommended `--order`.

   If you piloted inside the real `HarborPoint` project instead, run `--steps pilot-cleanup` and empty the Recycle Bin before seeding. Otherwise the pilot story adds 5 points to Mobile Banking's Sprint 13.

## When to seed, and how long it takes

- **Timing is the facilitator's decision.** "Now" must fall in **Sprint 14, week 2**, which is day 6–7 of 10 in the World Bible.
  - The generator derives Sprint 14 from the time you generate: Sprint 14 starts on the Monday of the week *before* generation day. So generate **on a weekday of the week the class runs**, no earlier than 2 days before Day 1. Monday or Tuesday is ideal.
  - Labs quote sprint names only. Saturday and Sunday aren't safe days to generate, because "now" would fall after Sprint 14 ends.
  - The provisioner refuses a dataset whose `now` is in the future. It warns when `now` is more than 2 days old, so generate and provision in one sitting.
- **How long it takes:**
  - With 3 participants, the seed is about **6,100 requests**, or about **35–40 minutes**. Each participant adds about 100 requests.
  - `--dry-run` prints the exact request count and an estimate.
  - The project-creation poll takes about 1 minute.
  - Allow another **30 minutes** for Analytics to catch up before checking velocity and CFD.
- **Pacing:** requests are sequential, at most 8 per second, with backoff on 429 or 5xx. The tool prints progress every 25 work items.

## Re-running safely, resuming, resetting

- **Resuming.** `out/state.json` records every created ID, including the last revision applied to each work item. Re-run the same command to resume after a failure or Ctrl-C.
  - Every step also looks up existing objects by name: project, nodes, teams, query folders, queries, wiki pages, dashboards and plans.
  - Existing dashboards and plans are left unchanged. Queries and wiki pages are updated in place; wiki updates use the page's ETag.
- **Lost responses.** If a work item write's response is lost (network error or 5xx), the tool checks whether the write reached the server before it retries, so it doesn't create duplicates.
- **Existing items guard.** If the project already has work items but the state file has none, the `workitems` step stops. Use the original `--state`, or reset.
- **One state file per target.** Use a separate `--state` file for each org and project; a mismatched state file is refused.
- **Reset.** Delete the project (*Project settings > Overview > Delete*) and the state file, then seed again.
  - Deleted projects can be restored for 28 days. Whether the same name can be reused right away is **UNCERTAIN**; if creation fails, permanently delete the project or use a new name.
  - Never change iteration dates or delete areas after seeding: that permanently corrupts the history charts.

## Manual follow-ups printed by the tool

The `summary` step lists them all. They are also kept in the state file. Typical items:

- **Team admins:** add each participant as administrator of their `P## Sandbox` team. There is no documented REST API for this.
- **Participants:** without `--participant-map`, add users (Basic, project Contributors) and their team membership by hand.
- **Sprint Burndown widget** on *Member Support - Delivery Health* (planted defect #11), plus any CFD, cycle time or lead time widgets. Their settings JSON is undocumented, so the tool prints exact UI steps.
  - The widget must point at **Sprint 13**.
  - Use `--experimental-widgets` to try creating them anyway.
- **Verify the permission and markers:**
  - the Contributors permission on `Shared Queries/Training`, because the token format is UNCERTAIN;
  - the Delivery Plan markers, because the marker property names are UNCERTAIN.
- **Planted defect #12 is intentional.** The *Waiting for sign-off* tile on the Member Support dashboard points at a query in the **seeding account's My Queries**. Every other viewer sees a permissions error, as designed. If you seed with a service account, that account is the "author".

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `HTTP 401` | PAT missing, expired, or for another org | Re-create an org-scoped PAT; check `~/.config/harborpoint/pat` or `AZDO_PAT`. |
| `HTTP 403` on project or work items | Missing scope, or the user isn't a PCA | Add the scopes above; make the PAT owner a Project Collection Administrator. |
| `VS402625: Dates must be increasing` | A revision is not later than the item's previous one. This often means a link revision on a parent. | Run the pilot and use its recommended `--order`, or try `--parent-links final`. Check that `verify` passed. |
| `VS403417: ChangedBy value cannot be empty` | The service requires ChangedBy with bypassRules | Re-run with `--changed-by "Seed Admin"` (any display name). |
| `TF400733` / HTTP 429 | Rate limit | The tool backs off automatically. If it persists, use `--max-rps 4` and resume later. |
| `TF401256` on queries | No write permission on Shared Queries | The PAT owner must be a Project Administrator or PCA. |
| `Project already contains work items…` | Wrong or missing state file | Use the original `--state`, or delete the project and seed fresh. |
| `dataset 'now' is in the future` / "N days old" | Clock skew, or a stale dataset | Regenerate the dataset right before provisioning. |
| Velocity or CFD empty right after seeding | Analytics latency | Wait 15–30 minutes; check OData `WorkItemRevisions` for one item. |
| History shows today's date instead of the backdated one | Bypass not honoured | Confirm the PCA role; re-run the pilot. Don't proceed. |
| A widget shows "configuration required" | Undocumented settings JSON | Follow the printed manual steps. |
| Dashboard or plan exists but looks wrong | Existing objects are not modified | Delete it in the UI, then re-run `--steps dashboards` (or `plans`). |
| `State file … belongs to …` | Reused state file | Pass a different `--state` for each org and project. |

## Behaviors to check in the live pilot (UNCERTAIN in the docs)

- Does a parent link added in revision 1 create a revision on the parent, and with which `ChangedDate`? This decides `--order`.
- Does the server reject a future `ChangedDate`? (The pilot sends a `validateOnly` probe.)
- Is ChangedBy required (VS403417)?
- Do Analytics Velocity "Planned", CFD and cycle time honour backdated revisions?
- Do board columns follow bypassed state changes? How do plain-text identities render?
- What is the state category of *Resolved* for User Story?
- What happens on a `remove` op for a field that was never set? (It clears Resolved/Closed dates.)
- Undocumented formats:
  - the `@CurrentIteration('[HarborPoint]\HarborPoint Team <id:GUID>')` form used in saved WIQL;
  - the query-folder ACL token format;
  - project-scoped dashboard creation (no team in the URL);
  - widget settings: Query Tile color rules, Chart `chartType` names, Velocity sum-of-Story-Points aggregation (`identifier: 1`);
  - the Delivery Plan `markers` and `cardSettings` property names;
  - the user-entitlement response shape.
- Is `connectionData` accepted without an `api-version`?

# Azure DevOps for Managers: HarborPoint Labs

Hands-on lab site for a three-day course that teaches managers to turn Azure DevOps data into management decisions, at the Feature and portfolio level. The labs are set in **HarborPoint Financial**, a fictional member-owned financial cooperative.

**Live site:** https://varoonsahgal.github.io/ado-for-managers/

## Run locally

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve        # http://127.0.0.1:8000
```

Pushing to `main` publishes the site through GitHub Actions (`.github/workflows/pages.yml`).

## Layout

| Path | What |
|---|---|
| `docs/` | Site content: start pages, the 12 labs (`day-1/` to `day-3/`), resources |
| `overrides/` | Theme templates (home page hero, lab mission headers, logbook) |
| `docs/stylesheets/`, `docs/javascripts/` | HarborPoint theme and interactive components (participant ID, checkpoints, quizzes, timers) |
| `environment/` | Tooling and content used to seed the HarborPoint Azure DevOps training project |

HarborPoint Financial and everyone in it are fictional. Azure DevOps is a Microsoft product.

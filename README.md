# Azure DevOps for Managers: HarborPoint Labs

Hands-on lab site for a three-day course that teaches managers to turn Azure DevOps data into management decisions, at the Feature and portfolio level. The labs are set in **HarborPoint Financial**, a fictional member-owned financial cooperative.

**Live site:** https://varoonsahgal.github.io/ado-for-managers/ · **Slides:** https://varoonsahgal.github.io/ado-for-managers/slides/

## Run locally

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve        # http://127.0.0.1:8000
```

Pushing to `main` publishes the site through GitHub Actions (`.github/workflows/pages.yml`).

## Slides

The course deck (92 slides) lives at `docs/slides/` and is built from the partials in `slides-src/`:

```bash
.venv/bin/python tools/build_slides.py      # rebuild docs/slides/index.html
```

Each lab's takeaways slide and the "course in twelve sentences" slide are generated from the labs' `one_thing` and `## Key takeaways`, and screenshot title bars come from `tools/shots.yaml`, so the deck can't drift from the labs. CI fails if the deck is stale. In the deck: arrow keys or Space to move, **G** for the slide index, **N** for speaker notes, **F** for fullscreen, **P** to print or save as PDF.

## Layout

| Path | What |
|---|---|
| `docs/` | Site content: start pages, the 12 labs (`day-1/` to `day-3/`), resources, and the built slide deck (`slides/`) |
| `slides-src/` | Hand-written slide partials, assembled by `tools/build_slides.py` |
| `overrides/` | Theme templates (home page hero, lab mission headers, logbook) |
| `docs/stylesheets/`, `docs/javascripts/` | HarborPoint theme and interactive components (participant ID, checkpoints, quizzes, timers) |
| `environment/` | Tooling and content used to seed the HarborPoint Azure DevOps training project |

HarborPoint Financial and everyone in it are fictional. Azure DevOps is a Microsoft product.

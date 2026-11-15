"""Replace <!-- SHOT: id | ... --> markers with framed, captioned screenshots.

A marker is replaced only when docs/assets/shots/<id>.png exists and tools/shots.yaml has an
entry for <id> with `bar` (where in Azure DevOps) and `caption` (what to notice). Re-running is
safe: embedded figures carry a `data-shot` attribute and are refreshed in place.

Usage: python tools/embed_shots.py [--check]
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SHOTS = DOCS / "assets" / "shots"

MARKER = re.compile(r"<!-- SHOT: (?P<id>[\w-]+) \|[^>]*-->")
FIGURE = re.compile(r'<figure class="hp-shot" data-shot="(?P<id>[\w-]+)" markdown>.*?</figure>', re.S)


def figure(md_file: Path, sid: str, meta: dict) -> str:
    rel = Path("../" * (len(md_file.relative_to(DOCS).parts) - 1)) / "assets" / "shots" / f"{sid}.png"
    alt = re.sub(r"[*`_\[\]]", "", meta.get("alt") or meta["caption"])
    return (
        f'<figure class="hp-shot" data-shot="{sid}" markdown>\n'
        f'<div class="hp-shot__bar" aria-hidden="true"><i></i><i></i><i></i>'
        f'<span>{html.escape(meta["bar"])}</span></div>\n\n'
        f'![{alt.replace("]", ")")}]({rel.as_posix()}){{ loading=lazy }}\n\n'
        f'<figcaption markdown>{meta["caption"]}</figcaption>\n'
        f"</figure>"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report only, change nothing")
    a = ap.parse_args()
    meta = yaml.safe_load((ROOT / "tools" / "shots.yaml").read_text()) or {}
    pending, embedded = [], 0
    for md in sorted(DOCS.rglob("*.md")):
        text = md.read_text()
        new = text

        def sub(m: re.Match) -> str:
            nonlocal embedded
            sid = m.group("id")
            if (SHOTS / f"{sid}.png").exists() and sid in meta:
                embedded += 1
                return figure(md, sid, meta[sid])
            pending.append(f"{md.relative_to(DOCS)}: {sid}")
            return m.group(0)

        new = MARKER.sub(sub, new)
        new = FIGURE.sub(lambda m: figure(md, m.group("id"), meta[m.group("id")])
                         if m.group("id") in meta else m.group(0), new)
        if new != text and not a.check:
            md.write_text(new)
    print(f"embedded {embedded} new; {len(pending)} markers still waiting for a capture or caption")
    for p in pending:
        print("  -", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())

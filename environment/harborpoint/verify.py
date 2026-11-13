"""Verify a generated dataset against the World Bible.

Usage (from the environment/ directory):
    python -m harborpoint.verify out/dataset.json [--out-dir out]

Recomputes every checkable number from the dataset's revisions (harborpoint.facts), writes
facts.md and facts.json next to the dataset (or into --out-dir) and exits non-zero on any mismatch.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .facts import compute


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m harborpoint.verify", description="Verify dataset facts")
    ap.add_argument("dataset", nargs="?", default="out/dataset.json")
    ap.add_argument("--out-dir", help="where to write facts.md / facts.json (default: dataset's directory)")
    args = ap.parse_args(argv)
    path = Path(args.dataset)
    data = json.loads(path.read_text(encoding="utf-8"))
    facts = compute(data)
    out_dir = Path(args.out_dir) if args.out_dir else path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "facts.json").write_text(json.dumps(facts.to_json(), indent=1, ensure_ascii=False) + "\n",
                                        encoding="utf-8")
    (out_dir / "facts.md").write_text(facts.to_markdown(), encoding="utf-8")
    fails = facts.failures
    print(f"{len(facts.checks)} checks, {len(fails)} failures -> {out_dir / 'facts.md'}")
    for c in fails:
        print(f"FAIL {c['id']}: expected {c['expected']!r}, got {c['actual']!r} {c['note']}", file=sys.stderr)
    if fails:
        print("VERIFY FAILED: dataset does not match the World Bible", file=sys.stderr)
        return 1
    print("VERIFY PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())

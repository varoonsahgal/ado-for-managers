"""Copy a browser capture into docs/assets/shots/<id>.png with optional highlight boxes.

Usage:
  python tools/shot.py <id> <source.png> [--box x0,y0,x1,y1 ...] [--crop x0,y0,x1,y1] [--max-width 1600]

Box coordinates are in source-image pixels (after --crop, relative to the cropped image).
Highlights use the site's brass accent so screenshots match the lab theme.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent.parent / "docs" / "assets" / "shots"
BRASS = (224, 122, 63)  # --hp-coral / brass accent used for highlights


def quad(s: str) -> tuple[int, int, int, int]:
    a = [int(float(v)) for v in s.split(",")]
    if len(a) != 4:
        raise argparse.ArgumentTypeError("expected x0,y0,x1,y1")
    return a[0], a[1], a[2], a[3]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("src")
    ap.add_argument("--box", type=quad, action="append", default=[])
    ap.add_argument("--crop", type=quad)
    ap.add_argument("--max-width", type=int, default=1600)
    a = ap.parse_args()

    im = Image.open(a.src).convert("RGB")
    if a.crop:
        im = im.crop(a.crop)
    if a.box:
        overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)
        w = max(3, round(im.width / 450))
        for x0, y0, x1, y1 in a.box:
            d.rounded_rectangle((x0, y0, x1, y1), radius=10, fill=BRASS + (16,), outline=BRASS + (255,), width=w)
        im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
    if im.width > a.max_width:
        im = im.resize((a.max_width, round(im.height * a.max_width / im.width)), Image.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / f"{a.id}.png"
    im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(dst, optimize=True)
    print(f"{dst.relative_to(OUT.parent.parent.parent)}  {im.width}x{im.height}  {dst.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()

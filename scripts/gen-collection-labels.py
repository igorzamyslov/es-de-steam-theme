#!/usr/bin/env python3
"""Generate clean white text-label wordmarks for the auto-collections (one-off build step).

The bundled auto-collection logos (system-logo-color/auto-*.svg) are stylised icons; for the
rail we want plain Steam-style white labels instead. ES-DE's SVG rasterizer can't be relied on
to render <text>, so we vectorise the label text into <path> outlines from the theme's display
font (Rubik ExtraBold) and write committed SVG wordmarks. gen-system-capsules.py then composites
these (on a neutral plate) for the collection capsules.

Requires fontTools (NOT stdlib). Run only when the label text or font changes:
    python3 -m venv .venv && .venv/bin/pip install fonttools
    .venv/bin/python scripts/gen-collection-labels.py
"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME = os.path.join(REPO, "steam-ui")
FONT = os.path.join(THEME, "fonts", "rubik-extrabold.ttf")
OUT = os.path.join(THEME, "system-logos", "system-label")

LABELS = {
    "auto-allgames": "Library",
    "auto-favorites": "Favorites",
    "auto-lastplayed": "Recent",
}


def label_svg(text, font):
    upm = font["head"].unitsPerEm
    asc = font["OS/2"].sTypoAscender
    desc = -font["OS/2"].sTypoDescender  # positive magnitude
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    space_adv = hmtx["space"][0] if "space" in hmtx.metrics else int(upm * 0.25)

    x = 0
    parts = []
    for ch in text:
        if ch == " ":
            x += space_adv
            continue
        gname = cmap.get(ord(ch))
        if gname is None:
            x += space_adv
            continue
        pen = SVGPathPen(glyphs)
        glyphs[gname].draw(pen)
        d = pen.getCommands()
        if d:
            parts.append(f'<path transform="translate({x} 0)" d="{d}"/>')
        x += hmtx[gname][0]

    w, h = x, asc + desc
    # font glyphs are y-up; flip into SVG y-down and drop the baseline at y=asc
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">\n'
        f'  <g fill="#ffffff" transform="translate(0 {asc}) scale(1 -1)">\n'
        f'    {"".join(parts)}\n'
        f'  </g>\n'
        f'</svg>\n'
    )


def main():
    os.makedirs(OUT, exist_ok=True)
    font = TTFont(FONT)
    for key, text in LABELS.items():
        open(os.path.join(OUT, key + ".svg"), "w", encoding="utf-8").write(label_svg(text, font))
        print(f"wrote {key}.svg  ({text!r})")


if __name__ == "__main__":
    main()

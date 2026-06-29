#!/usr/bin/env python3
"""Generate a per-system hero-art prompt manifest from the bundled system metadata.

Reads each steam-bigpicture-es-de/system-metadata/<system>.xml, pulls the top-level
<variables> (NOT the per-language overrides), and expands a locked prompt template.
Writes docs/hero-art/prompts.tsv: system<TAB>prompt<TAB>primary_color<TAB>palette.

See docs/hero-art-style-spec.md for the look these prompts target.
"""
import os
import sys
import xml.etree.ElementTree as ET

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = os.path.join(REPO, "steam-bigpicture-es-de", "system-metadata")
OUT = os.path.join(REPO, "docs", "hero-art", "prompts.tsv")

FIELDS = (
    "systemName", "systemManufacturer", "systemReleaseYear",
    "systemHardwareType", "systemColor",
    "systemColorPalette1", "systemColorPalette2",
    "systemColorPalette3", "systemColorPalette4",
)


def read_vars(path):
    """Return the top-level <variables> as a dict (ignores <language> blocks)."""
    root = ET.parse(path).getroot()
    block = root.find("variables")
    if block is None:
        return {}
    return {child.tag: (child.text or "").strip() for child in block}


def build_prompt(v):
    name = v.get("systemName") or "this system"
    maker = v.get("systemManufacturer") or ""
    year = v.get("systemReleaseYear") or ""
    htype = (v.get("systemHardwareType") or "system").lower()
    color = v.get("systemColor") or "333333"
    maker_year = " ".join(p for p in (maker, year) if p).strip()
    origin = f" ({maker_year})" if maker_year else ""
    return (
        f"Detailed pixel-art poster, 1280x720, of the {name}{origin} {htype} as the hero "
        f"subject in an atmospheric scene evoking its era. Dominant light keyed to #{color}; "
        f"neon rim light; glowing marquee sign reading \"{name}\". Saturated midtones, "
        f"painterly depth. Left 45% and bottom 30% darkened for overlaid white text. "
        f"No copyrighted character likenesses."
    )


def main():
    rows = []
    for fn in sorted(os.listdir(META)):
        if not fn.endswith(".xml") or fn.startswith("_"):
            continue
        system = fn[:-4]
        v = read_vars(os.path.join(META, fn))
        if not v:
            continue
        palette = ",".join(
            v.get(f"systemColorPalette{i}", "") for i in range(1, 5)
        )
        rows.append((system, build_prompt(v), v.get("systemColor", "333333"), palette))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("system\tprompt\tprimary_color\tpalette\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    print(f"wrote {len(rows)} prompts to {os.path.relpath(OUT, REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

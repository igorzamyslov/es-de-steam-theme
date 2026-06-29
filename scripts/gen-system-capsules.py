#!/usr/bin/env python3
"""Bake one colour-logo capsule SVG per system for the system-view rail.

The rail is a Steam-style shelf of branded capsules: each system's full-colour logo
(`system-logos/system-logo-color/<system>.svg`) sits on a dark plate with a diagonal
bloom of that system's ${systemColor} (read from the bundled system-metadata and baked
in as a literal hex, so no runtime tinting is needed). ES-DE's carousel has no per-item
plate, so the plate is composited into the item asset here.

Engine-safe SVG only: the theme's shipped assets use `linearGradient` + `<g>` and never
`radialGradient` or nested `<svg>`, so the bloom is a diagonal linear gradient and the
logo is placed with a `<g transform>` (computed from its viewBox), not a nested `<svg>`.

Run `python3 scripts/gen-system-capsules.py`. Idempotent: overwrites system-capsule/*.svg.
"""
import os
import re
import sys
import xml.etree.ElementTree as ET

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME = os.path.join(REPO, "steam-bigpicture-es-de")
META = os.path.join(THEME, "system-metadata")
LOGOS = os.path.join(THEME, "system-logos", "system-logo-color")
OUT = os.path.join(THEME, "system-logos", "system-capsule")

# Capsule geometry (viewBox units). 2.2:1 matches the rail itemSize aspect.
VB_W, VB_H = 440.0, 200.0
# Logo placement box: fraction of the plate, centred.
BOX_XF, BOX_YF, BOX_WF, BOX_HF = 0.11, 0.18, 0.78, 0.64

DEFAULT_COLOR = "33a8ff"  # neutral Steam blue when a system has no metadata colour

# Namespaces some source logos use on kept-verbatim editor nodes; declared on the capsule
# root so the markup validates (the renderer ignores foreign-namespace nodes).
NS = (
    'xmlns:xlink="http://www.w3.org/1999/xlink" '
    'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
    'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" '
    'xmlns:i="http://ns.adobe.com/AdobeIllustrator/10.0/" '
)

# Per-system fit multipliers for wordmarks that read poorly at the default fit
# (1.0 = fill the box; <1 = shrink; >1 = enlarge). Populated by eyeballing the output.
FIT_OVERRIDES = {}


def system_color(system):
    """Top-level <variables>/<systemColor> for a system, or the default."""
    path = os.path.join(META, system + ".xml")
    if not os.path.isfile(path):
        return DEFAULT_COLOR
    block = ET.parse(path).getroot().find("variables")
    if block is None:
        return DEFAULT_COLOR
    el = block.find("systemColor")
    val = (el.text or "").strip() if el is not None else ""
    return val if re.fullmatch(r"[0-9a-fA-F]{6}", val or "") else DEFAULT_COLOR


def logo_parts(path):
    """Return (viewBox tuple minx,miny,w,h ; inner markup) for a colour-logo SVG."""
    raw = open(path, encoding="utf-8").read()
    raw = re.sub(r"<\?xml.*?\?>", "", raw, flags=re.S)
    raw = re.sub(r"<!DOCTYPE.*?>", "", raw, flags=re.S)
    open_m = re.search(r"<svg\b[^>]*>", raw, flags=re.S)
    inner = raw[open_m.end():raw.rfind("</svg>")].strip()
    root_tag = open_m.group(0)
    # Keep the editor metadata verbatim (the renderer ignores foreign-namespace nodes, as it
    # does in the originals); we only declare their namespaces on the capsule root. The two
    # exceptions carry an undefined entity (&ns_ai;) once the DOCTYPE is stripped, so drop them:
    inner = re.sub(r"<metadata\b.*?</metadata>", "", inner, flags=re.S)        # RDF block
    inner = re.sub(r"<foreignObject\b.*?</foreignObject>", "", inner, flags=re.S)  # Adobe PGF
    inner = re.sub(r"&ns_[A-Za-z0-9_]+;", "", inner)                          # any stray AI entity
    vb_m = re.search(r'viewBox="([^"]+)"', root_tag)
    if vb_m:
        minx, miny, w, h = (float(x) for x in re.split(r"[ ,]+", vb_m.group(1).strip()))
    else:  # fall back to width/height (strip units)
        def dim(name):
            m = re.search(name + r'="([\d.]+)', root_tag)
            return float(m.group(1)) if m else 100.0
        minx, miny, w, h = 0.0, 0.0, dim("width"), dim("height")
    return (minx, miny, w, h), inner


def capsule_svg(color, vb, inner, fit_mult):
    minx, miny, w, h = vb
    bx, by = BOX_XF * VB_W, BOX_YF * VB_H
    bw, bh = BOX_WF * VB_W, BOX_HF * VB_H
    s = min(bw / w, bh / h) * fit_mult
    tx = bx + (bw - w * s) / 2 - minx * s
    ty = by + (bh - h * s) / 2 - miny * s
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" {NS}'
        f'viewBox="0 0 {VB_W:.0f} {VB_H:.0f}" preserveAspectRatio="xMidYMid meet">\n'
        f'  <defs>\n'
        f'    <linearGradient id="base" x1="0" y1="0" x2="0" y2="1">\n'
        f'      <stop offset="0" stop-color="#1d2734"/>'
        f'<stop offset="0.5" stop-color="#121925"/>'
        f'<stop offset="1" stop-color="#0a0e15"/>\n'
        f'    </linearGradient>\n'
        f'    <linearGradient id="bloom" x1="0" y1="0" x2="1" y2="1">\n'
        f'      <stop offset="0" stop-color="#{color}" stop-opacity="0.50"/>\n'
        f'      <stop offset="0.6" stop-color="#{color}" stop-opacity="0"/>\n'
        f'    </linearGradient>\n'
        f'  </defs>\n'
        f'  <rect width="{VB_W:.0f}" height="{VB_H:.0f}" fill="url(#base)"/>\n'
        f'  <rect width="{VB_W:.0f}" height="{VB_H:.0f}" fill="url(#bloom)"/>\n'
        f'  <g transform="translate({tx:.3f} {ty:.3f}) scale({s:.5f})">{inner}</g>\n'
        f'</svg>\n'
    )


def fallback_svg():
    """Neutral capsule for systems with no colour logo (carousel defaultImage)."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" {NS}'
        f'viewBox="0 0 {VB_W:.0f} {VB_H:.0f}" preserveAspectRatio="xMidYMid meet">\n'
        f'  <defs>\n'
        f'    <linearGradient id="base" x1="0" y1="0" x2="0" y2="1">\n'
        f'      <stop offset="0" stop-color="#1d2734"/><stop offset="1" stop-color="#0a0e15"/>\n'
        f'    </linearGradient>\n'
        f'  </defs>\n'
        f'  <rect width="{VB_W:.0f}" height="{VB_H:.0f}" fill="url(#base)"/>\n'
        f'  <g transform="translate(196 70) scale(1)" fill="none" stroke="#5c6675" '
        f'stroke-width="3" stroke-linecap="round" stroke-linejoin="round">\n'
        f'    <rect x="0" y="6" width="48" height="28" rx="13"/>'
        f'<line x1="11" y1="20" x2="21" y2="20"/><line x1="16" y1="15" x2="16" y2="25"/>'
        f'<circle cx="33" cy="16" r="2.4"/><circle cx="39" cy="24" r="2.4"/>\n'
        f'  </g>\n'
        f'</svg>\n'
    )


def main():
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for fn in sorted(os.listdir(LOGOS)):
        if not fn.endswith(".svg"):
            continue
        system = fn[:-4]
        vb, inner = logo_parts(os.path.join(LOGOS, fn))
        svg = capsule_svg(system_color(system), vb, inner, FIT_OVERRIDES.get(system, 1.0))
        open(os.path.join(OUT, fn), "w", encoding="utf-8").write(svg)
        n += 1
    open(os.path.join(OUT, "_fallback.svg"), "w", encoding="utf-8").write(fallback_svg())
    print(f"wrote {n} capsules + _fallback.svg to {os.path.relpath(OUT, REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

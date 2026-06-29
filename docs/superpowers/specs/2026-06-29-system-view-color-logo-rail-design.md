# System view — colour-logo capsule rail — design

Date: 2026-06-29

Redesign the **system view** of the Steam Big Picture for ES-DE theme so it reads as
Steam. The single highest-leverage change: the bottom **rail** stops using monochrome
controller-outline icons (`system-controllers-outline/`) and instead shows each system's
**full-colour logo** on a branded capsule — the colour assets the theme already bundles
(`system-logos/system-logo-color/`, 204 systems) but currently discards. The neon hero's
subject also moves from the flat white logo to the colour logo, with a per-system colour
bloom. The **game view is unchanged** — it is already art-forward (colour cover capsules,
selector frame, green Play); this work brings the system view *into* that language, which
previously clashed.

A browseable mockup of the target (system + game view, with a font-size switch) lives at
`docs/mockup/steam-system-redesign.html` (generator: `docs/mockup/gen-system-redesign-mockup.py`).

## Constraints / environment notes

- **No ES-DE renderer and no rasterizer in this workspace.** Verification here is limited
  to XML well-formedness, asset-reference checks, and lint (the repo's pre-commit hooks).
  Every visual claim must be confirmed by the user in a real ES-DE install; the plan will
  list exactly what to eyeball. All new assets must therefore be **vector SVG** (authored
  by a Python generator), never rasterised here.
- **ES-DE is a baked-asset engine, not CSS.** It has *no* backdrop blur, *no*
  box-shadow/glow, and *no* radial or >2-stop gradient as an XML property (`color`/
  `colorEnd`/`gradientType` is two-stop **linear** only). Gradients, glows, scrims and
  frosted panels are realised as **baked image assets** tinted by a variable — exactly the
  existing pattern (`hero-bg.svg`, `tint.svg` coloured `${systemColor}cc`, `panel.svg`,
  `selector-frame.svg`). A radial bloom is fine **inside** an SVG asset (it is just a
  texture ES-DE multiplies), it just cannot be expressed in theme XML.
- **`${systemColor}` is a theme-authored per-system variable** (each
  `system-metadata/<system>.xml`), not an ES-DE-provided value. Reliable because the theme
  owns it; any new per-system colour must come from those files. (Pattern already used by
  `scripts/gen-dark-accent-overrides.py`.)
- **Carousel limits (this is what shapes the rail design).** A `<carousel>`:
  - has **no per-item background plate** and **no `selectorImage`/focus frame** — selection
    is conveyed only by `itemScale`, `imageSelectedColor`, and dimming the rest
    (`unfocusedItemOpacity` / `unfocusedItemSaturation` / `unfocusedItemDimming`);
  - **cannot style an item conditionally** (e.g. by game count) — every item is the same
    `staticImage` template;
  - renders a **multicolour SVG in its native colours only if `imageColor` is left unset**
    (default `FFFFFF`); `imageColor` is a per-pixel **multiply**, so any non-white value
    tints/darkens the whole logo.
  - The `<grid>` element *does* have per-item plates + a focus frame, but it is a wrapping
    X×Y grid with derived column counts — not a clean single horizontal scroller — so it is
    the wrong element for a rail.

## Resolved decisions (with the user)

1. **Rail subject:** monochrome controller outlines → full-colour `system-logo-color`
   wordmarks on a branded capsule.
2. **Rail element stays a `<carousel>`.** The capsule "plate" is **baked into each item
   asset** (a vector composite of plate + colour logo), since the carousel has no per-item
   plate. Focus = `itemScale` (zoom) + the others dimmed/desaturated. **No focus frame** —
   the carousel cannot draw one; scale + dim is how Steam Deck's own shelf reads, so this
   is accepted, not a compromise to fix later.
3. **Neon hero subject:** the focused system's **colour** logo (was flat white), enlarged,
   over a per-system colour bloom derived from `${systemColor}`.
4. **Info block** gets a solid baked panel behind it (no live blur).
5. **Corners stay rectangular** (`radTile`/`rad`/`radButton` = 0). Softening is a one-token
   change; deferred, not part of this work.
6. **Typography is unchanged** — it inherits `_inc/scale.xml`, and readability is governed
   by the ES-DE **Theme font size** setting. **Large** is the right default on 5–7"
   handhelds (the README already says so). The redesign introduces no new fixed-size text.
7. **Game view: no required changes.** It already matches; confirm consistency only.

## Implementability summary

| Mockup element | Verdict | Realisation in ES-DE |
| --- | --- | --- |
| Colour wordmarks in the rail | native | `carousel staticImage` → baked capsule SVG; `imageColor` unset |
| Focused capsule pops, others recede | native | `itemScale` + `unfocusedItemOpacity`/`Saturation`/`Dimming` |
| Per-system colour bloom / plate | baked | radial gradient + logo composited into one SVG per system, tinted by `${systemColor}` |
| Neon hero colour logo + bloom | native + baked | path swap to `system-logo-color`; bloom is a baked tinted asset |
| Solid info panel | baked | semi-opaque `info-panel.svg` (no live blur) |
| Per-tile focus **frame** on the rail | **not possible** | carousel has none; accept scale + dim |
| Per-tile "empty/0 games" styling on the rail | **not possible** | carousel can't vary per item; show emptiness in the **hero count** instead |

## Changes

### A. Asset generator — baked capsule assets

- New `scripts/gen-system-capsules.py` (mirrors `gen-dark-accent-overrides.py`): for every
  `system-metadata/<system>.xml`, read `${systemColor}` (and `systemColorPalette1..4`), load
  `system-logos/system-logo-color/<system>.svg`, and emit a **vector** composite to
  `steam-ui/system-logos/system-capsule/<system>.svg`. Each composite is:
  - a rectangular plate: a dark base gradient with a **radial bloom of `systemColor`** from a
    top-left-ish origin (SVG `radialGradient` — baked, so allowed);
  - the colour logo embedded (nested `<svg>`/`<g>`), **fit** to roughly 78% width × 64%
    height of the plate, centred, preserving aspect.
  - Authored at the capsule aspect (landscape, ≈16:9) so `imageFit` does not distort.
- Emit a generic **fallback** capsule (`system-capsule/_fallback.svg`: neutral plate + a
  controller glyph) for unknown systems.
- Skip non-system metadata files (`_default`, `_labels`, `README`, `Fix.py`) — same filter
  as the existing generator.
- Committed output (the asset-reference checker requires the files to exist).

### B. Factor the rail into a shared include + re-point it

- Extract the duplicated `<carousel name="rail">` (identical in `_inc/system_hero_neon.xml`
  and `_inc/system_hero_art.xml`) into new `_inc/system_rail.xml`; both hero files
  `<include>./system_rail.xml</include>` in its place.
- New carousel definition:
  - `staticImage` → `./../system-logos/system-capsule/${system.theme}.svg`;
    `defaultImage` → `./../system-logos/system-capsule/_fallback.svg`.
  - **Remove `imageColor`** (or set `ffffffff`) so the colour logo renders native;
    `imageSelectedColor` `ffffffff` (focused at full brightness).
  - Focus/dim: `unfocusedItemOpacity` ≈ `0.5`, add `unfocusedItemSaturation` ≈ `0.7` and
    `unfocusedItemDimming` ≈ `0.7` so unfocused capsules recede (Steam Deck behaviour).
  - `itemSize` → landscape (≈ `0.15 0.12`; tune so the wordmark capsule is ~16:9);
    `itemScale` ≈ `1.12`; `maxItemCount` ≈ `7` (wider tiles fit fewer); `imageCornerRadius`
    `${radTile}`; `color` `00000000`.
  - Keep `text ${system.fullName}` + `textColor 00000000` as the no-asset fallback label.

### C. Neon hero subject → colour logo + bloom (`_inc/system_hero_neon.xml`)

- `heroLogo`: `path` `system-logos/system-logo-white/${system.theme}.svg` →
  `system-logos/system-logo-color/${system.theme}.svg`; **remove the `<color>e8edf2ff</color>`
  tint** (let native colours show); enlarge `maxSize` (≈ `0.44 0.46` → `0.52 0.48`).
- Add a baked **bloom** behind the logo: new `assets/ui/hero-bloom.svg` (white radial,
  transparent edges) as an `<image>` coloured `${systemColor}` (alpha ~`66`), zIndex between
  `heroBg`/`heroTint` (≤2) and the scrims (≤8). The existing `heroTint` (already
  `${systemColor}cc`) stays.
- Art variant hero subject (per-system raster art) is **unchanged**.

### D. Info panel behind the bottom-left text (both hero files)

- Add `assets/ui/info-panel.svg` (semi-opaque dark rectangle, fully rectangular) as an
  `<image>` positioned behind the `sysName`/`sysSpec`/`sysCount`/`sysDesc` block, zIndex
  above the scrims (≤8) and below the text (10). Polish: improves the "card" read the mockup
  shows; the left scrim already gives baseline legibility, so this is additive.

### E. Empty-state honesty

- Per-tile "0 games"/dimmed styling on the rail is **not possible** (carousel limitation,
  §Constraints). Emptiness is communicated by the existing hero `sysCount`
  (`<systemdata>gamecount</systemdata>`). Add a code comment recording this so it is not
  "fixed" later by trying to style the carousel per item.

### F. Outlier wordmark normalisation

- Some colour logos have internal whitespace and read oddly when fit naively — confirmed:
  **`n64`** (the "N" and "64" sit far apart) and **`gc`** (small mark). The generator's
  default bounding-box fit handles most; add a small per-system **fit-override table**
  (extra scale/padding) in `gen-system-capsules.py` for the handful that need it. Build the
  list by eyeballing the generated capsules; `n64` and `gc` are known starting entries.

### G. README + screenshots

- Update the system-view description: the platform rail now shows **full-colour system
  logos** on branded capsules (was monochrome). Refresh the system-view screenshot(s).
- Re-affirm the small-screen tip (Large/X-Large) already present.

## Non-goals

- A per-tile focus **frame** on the rail, or switching the rail to a `<grid>` to get one
  (grid wraps to X×Y with derived columns — wrong element for a horizontal rail).
- Per-tile empty/game-count styling on the rail (engine cannot vary items conditionally).
- Live blur, CSS-style box-shadow/glow, or radial/multi-stop gradients expressed in theme
  XML (all baked into assets instead).
- Per-system **raster hero art** — that is the separate hero-art generation kit.
- Rebuilding or restyling the **game view** (already consistent).
- Softening corners (one-token change, deferred); portrait / `1:1` layouts.

## Verification

- **Automated (here):** `pre-commit run --all-files` — xmllint well-formedness, the
  asset-reference checker (must resolve every `system-capsule/<system>.svg` referenced by the
  carousel, incl. `_fallback`), markdownlint. `scripts/gen-system-capsules.py` must lint
  clean and run against the full `system-metadata/` tree, emitting one SVG per system;
  `tools/check-theme-paths.sh` / `scripts/check-asset-refs.py` clean.
- **Manual (user, in ES-DE — plan will spell out):**
  - rail shows colourful per-system capsules; the focused one scales up and the others
    dim/desaturate (no frame, by design);
  - neon hero shows the focused system's **colour** logo over a `systemColor` bloom; the art
    variant hero is unchanged; both variants share the new rail;
  - an empty system shows `0` in the hero count (rail tile looks the same — expected);
  - `n64` and `gc` capsules fill their tiles sensibly after the fit-override pass;
  - at **Large** on a 7"/1080p panel, system name, spec, count, description and the rail
    labels are comfortably legible.

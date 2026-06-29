# System view — colour-logo capsule rail — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the system view's monochrome controller-outline rail with full-colour
system-logo capsules, and make the neon hero's subject the colour logo over a per-system
colour bloom — bringing the system view into the game view's Steam language.

**Architecture:** A Python generator bakes one **vector** capsule SVG per system (dark plate
+ diagonal `systemColor` bloom + the embedded colour logo, placed via a `<g transform>`).
The rail `<carousel>` is factored into a shared `_inc/system_rail.xml` and re-pointed at those
capsules; focus is scale + dim/desaturate (carousel has no focus frame). The neon hero swaps
its white logo for the colour logo plus a baked `hero-bloom.svg`.

**Tech Stack:** ES-DE theme XML (3.x engine), Python 3 (stdlib only, like the existing
`scripts/gen-*.py`), SVG assets.

## Global Constraints

- **Vector SVG only** — no rasterizer in this workspace; all generated/baked assets are SVG.
- **Engine-supported SVG features only:** `linearGradient` + `stop-color`/`stop-opacity`,
  `fill="url(#…)"`, `<g transform>`, `preserveAspectRatio`. **No** `radialGradient`, **no**
  nested `<svg>`, **no** `filter`/blur (none appear in the theme's shipped assets).
- **Carousel limits:** no per-item plate, no focus frame, no per-item conditional styling;
  multicolour SVG renders native **only if `imageColor` is unset/`ffffffff`** (it is a multiply).
- `${systemColor}` is a theme variable in `system-metadata/<system>.xml`; the generator reads
  it and bakes the **literal hex** into each capsule (no runtime tint).
- **Python:** stdlib only; skip non-system metadata files (`_default`, `_labels`, `README*`,
  `*.py`). Match the style of `scripts/gen-dark-accent-overrides.py`.
- **No ES-DE renderer here** — verification is xmllint well-formedness, the asset-reference
  checker, lint, and rendering the generated SVGs in a browser. Real-engine confirmation is a
  manual user step (checklist in Task 8).
- Corners stay rectangular (`radTile`/`rad`/`radButton` = 0). Commit messages: no co-author trailer.

---

### Task 1: Capsule asset generator

**Files:**
- Create: `scripts/gen-system-capsules.py`
- Reads: `steam-bigpicture-es-de/system-metadata/*.xml`, `steam-bigpicture-es-de/system-logos/system-logo-color/*.svg`
- Writes: `steam-bigpicture-es-de/system-logos/system-capsule/<system>.svg` + `_fallback.svg`

**Produces:** one capsule SVG per system the colour-logo set covers; `_fallback.svg` for the rest.

- [ ] **Step 1: Write the generator.** Capsule viewBox `0 0 440 200` (2.2:1, matches the rail
  `itemSize`). Composition, bottom→top:
  1. base plate: `<rect width=440 height=200 fill="url(#base)">` with a vertical `linearGradient`
     `#1d2734`→`#0a0e15`;
  2. bloom overlay: `<rect …>` with a **diagonal** `linearGradient` (x1=0 y1=0 → x2=1 y2=1)
     from `<systemColorHex>` `stop-opacity=0.50` at offset 0 → `stop-opacity=0` at ~0.6;
  3. logo: parse the colour-logo root `viewBox` (`minx miny w h`; synthesize from width/height
     if absent). Target box = 78%×64% centred: `bx=0.11*440, by=0.18*200, bw=0.78*440, bh=0.64*200`.
     `s = min(bw/w, bh/h) * fitMult`; `tx = bx + (bw - w*s)/2 - minx*s`; `ty = by + (bh - h*s)/2 - miny*s`.
     Strip the logo's outer `<svg …>`/`</svg>` and its `<?xml…?>`, keep the inner markup, wrap in
     `<g transform="translate(tx ty) scale(s)">…</g>`. `fitMult` defaults to `1.0` (override table in Task 2).
  - `_fallback.svg`: same plate (neutral, use `#33a8ff` bloom) with the existing
    `assets/icons/fallback.svg` glyph placed by the same box math, OR a centred "?" — neutral.
- [ ] **Step 2: Run it.** `python3 scripts/gen-system-capsules.py` → expect `wrote N capsules`
  (N ≈ 200+). Confirm `system-logos/system-capsule/` is populated incl. `_fallback.svg`.
- [ ] **Step 3: Validate well-formedness.**
  Run: `xmllint --noout steam-bigpicture-es-de/system-logos/system-capsule/*.svg`
  Expected: no output (all well-formed). Fix any logo whose inner markup breaks nesting.
- [ ] **Step 4: Render spot-check.** Copy ~6 capsules (`nes,snes,n64,gc,ps2,gb`) into the
  preview-served `docs/mockup/` dir (or point the static server at `system-capsule/`) and open them
  in the browser preview; confirm plate bloom + logo placement look right at capsule aspect.
- [ ] **Step 5: Commit.**
```bash
git add scripts/gen-system-capsules.py steam-bigpicture-es-de/system-logos/system-capsule/
git commit -m "feat(system): generate colour-logo capsule assets for the rail"
```

### Task 2: Outlier wordmark fit overrides

**Files:** Modify `scripts/gen-system-capsules.py`; regenerate `system-capsule/`.

**Consumes:** Task 1's `fitMult` hook.

- [ ] **Step 1:** Add `FIT_OVERRIDES = {"n64": …, "gc": …}` (per-system `fitMult`, and optional
  y-offset) near the top. Apply in the placement math. Seed with `n64` (wide internal gap — reduce
  so it doesn't dominate) and `gc` (small mark — scale up toward the box).
- [ ] **Step 2:** Regenerate (`python3 scripts/gen-system-capsules.py`).
- [ ] **Step 3:** Render-check `n64`, `gc` in the preview browser; tune the multipliers until each
  capsule reads cleanly. Add any other outliers discovered.
- [ ] **Step 4: Commit.**
```bash
git add scripts/gen-system-capsules.py steam-bigpicture-es-de/system-logos/system-capsule/
git commit -m "feat(system): per-system fit overrides for outlier wordmarks"
```

### Task 3: Baked hero assets (bloom + info panel)

**Files:**
- Create: `steam-bigpicture-es-de/assets/ui/hero-bloom.svg`
- Create: `steam-bigpicture-es-de/assets/ui/info-panel.svg`

**Produces:** `hero-bloom.svg` (tinted at runtime by `${systemColor}`); `info-panel.svg` (static).

- [ ] **Step 1:** `hero-bloom.svg` — `viewBox 0 0 100 100` `preserveAspectRatio="none"`, a **white**
  diagonal `linearGradient` (`stop-opacity` ~0.7→0) so the `<image>` `<color>${systemColor}…</color>`
  multiply tints it (same trick as `tint.svg`). Edges transparent.
- [ ] **Step 2:** `info-panel.svg` — `viewBox 0 0 100 100` `preserveAspectRatio="none"`, a solid
  semi-opaque dark fill (`#0c0f14` `fill-opacity` ~0.85), fully rectangular.
- [ ] **Step 3:** `xmllint --noout` both; open both in the preview to sanity-check.
- [ ] **Step 4: Commit.**
```bash
git add steam-bigpicture-es-de/assets/ui/hero-bloom.svg steam-bigpicture-es-de/assets/ui/info-panel.svg
git commit -m "feat(system): baked hero-bloom and info-panel assets"
```

### Task 4: Shared rail include + re-point the carousel

**Files:**
- Create: `steam-bigpicture-es-de/_inc/system_rail.xml`
- Modify: `steam-bigpicture-es-de/_inc/system_hero_neon.xml` (replace the `<carousel name="rail">` block with `<include>./system_rail.xml</include>`)
- Modify: `steam-bigpicture-es-de/_inc/system_hero_art.xml` (same replacement)

**Consumes:** `system-capsule/<system>.svg` + `_fallback.svg` (Task 1/2).

- [ ] **Step 1:** Create `_inc/system_rail.xml` wrapping one `<view name="system"><carousel name="rail">…`:
  - `pos 0 0.75`, `size 1 0.15`, `type horizontal`, `zIndex 40` (unchanged);
  - `staticImage ./../system-logos/system-capsule/${system.theme}.svg`;
    `defaultImage ./../system-logos/system-capsule/_fallback.svg`;
  - **no `imageColor`**; `imageSelectedColor ffffffff`;
  - `unfocusedItemOpacity 0.5`, `unfocusedItemSaturation 0.7`, `unfocusedItemDimming 0.7`;
  - `itemSize 0.15 0.12`, `itemScale 1.12`, `maxItemCount 7`, `imageCornerRadius ${radTile}`,
    `color 00000000`; keep `text ${system.fullName}` + `textColor 00000000`.
  - Add a comment: empty/0-game systems cannot be styled per item here (carousel limit); emptiness
    shows in the hero count.
- [ ] **Step 2:** In both hero files, delete the full `<carousel name="rail">…</carousel>` element and
  add `<include>./system_rail.xml</include>` at the same point (keep `railScrim`/`rail-shelf` as-is).
- [ ] **Step 3: Validate.**
  Run: `xmllint --noout steam-bigpicture-es-de/_inc/system_rail.xml steam-bigpicture-es-de/_inc/system_hero_neon.xml steam-bigpicture-es-de/_inc/system_hero_art.xml`
  Expected: no output.
- [ ] **Step 4: Asset refs.** Run `python3 scripts/check-asset-refs.py` (and `tools/check-theme-paths.sh`).
  Expected: the `system-capsule/${system.theme}.svg` + `_fallback` references resolve; no missing assets.
- [ ] **Step 5: Commit.**
```bash
git add steam-bigpicture-es-de/_inc/system_rail.xml steam-bigpicture-es-de/_inc/system_hero_neon.xml steam-bigpicture-es-de/_inc/system_hero_art.xml
git commit -m "feat(system): colour-logo capsule rail via shared include"
```

### Task 5: Neon hero colour logo + bloom + info panel

**Files:** Modify `steam-bigpicture-es-de/_inc/system_hero_neon.xml`; Modify `steam-bigpicture-es-de/_inc/system_hero_art.xml` (info panel only).

**Consumes:** `hero-bloom.svg`, `info-panel.svg` (Task 3).

- [ ] **Step 1 (neon):** `heroLogo` — `path` → `./../system-logos/system-logo-color/${system.theme}.svg`;
  **remove** `<color>e8edf2ff</color>`; enlarge `maxSize 0.44 0.46` → `0.52 0.48`.
- [ ] **Step 2 (neon):** add `<image name="heroBloom">` — `pos 0.30 0`, `size 0.70 1`,
  `path ./../assets/ui/hero-bloom.svg`, `color ${systemColor}66`, `zIndex 3` (above `heroTint`=2,
  below `railScrim`=6 / scrims). Keep existing `heroTint`.
- [ ] **Step 3 (both):** add `<image name="infoPanel">` behind the bottom-left text block —
  `pos 0.035 ${sized to wrap sysName→sysDesc}`, `size ~0.50 ~0.30`, `path ./../assets/ui/info-panel.svg`,
  `zIndex 9` (above scrims ≤8, below text 10). Tune pos/size against `heroNameY`/`heroDescY`/`heroDescH`.
- [ ] **Step 4: Validate.** `xmllint --noout` both hero files; `python3 scripts/check-asset-refs.py`.
  Expected: clean; `hero-bloom.svg`/`info-panel.svg`/`system-logo-color` refs resolve.
- [ ] **Step 5: Commit.**
```bash
git add steam-bigpicture-es-de/_inc/system_hero_neon.xml steam-bigpicture-es-de/_inc/system_hero_art.xml
git commit -m "feat(system): neon hero colour logo + bloom; info panel on both heroes"
```

### Task 6: README description

**Files:** Modify `README.md`.

- [ ] **Step 1:** Update the system-view sentence/intro: the platform rail now shows **full-colour
  system logos** on branded capsules (was monochrome controller outlines); the neon hero shows the
  focused system's colour logo. Leave the existing small-screen (Large/X-Large) tip in place.
  Note screenshots will be refreshed from a real ES-DE render (cannot be produced here).
- [ ] **Step 2: Commit.**
```bash
git add README.md
git commit -m "docs: README describes the colour-logo capsule rail"
```

### Task 7: Full validation pass

- [ ] **Step 1:** `pre-commit run --all-files` (xmllint, asset-reference checker, markdownlint, link
  check). Expected: pass. Fix anything flagged; re-run.
- [ ] **Step 2:** Confirm the generator is reproducible: `python3 scripts/gen-system-capsules.py`
  produces no git diff (assets already committed match a fresh run).
- [ ] **Step 3: Commit** any lint fixes (if needed).

### Task 8: ES-DE eyeball checklist (handoff to user)

Not code — produce the list of things to confirm in a real ES-DE install, since none of it can be
rendered here:
- rail shows colourful per-system capsules; the focused one scales up and the rest dim/desaturate;
- neon hero shows the focused system's **colour** logo over a `systemColor` bloom; art hero unchanged;
  both variants share the new rail;
- `info-panel` improves (not harms) text legibility in both heroes;
- an empty system shows `0` in the hero count (rail tile looks the same — expected);
- `n64`/`gc` capsules read cleanly; scan for any other outlier needing a `FIT_OVERRIDES` entry;
- at **Large** on a 7"/1080p panel everything is comfortably legible.

## Self-Review

- **Spec coverage:** A→generator(T1)+overrides(T2); B(rail include)→T4; C(neon hero)→T5;
  D(info panel)→T3+T5; E(empty-state comment)→T4 step1; F(outliers)→T2; G(README)→T6. All covered.
- **Refinement vs spec:** spec said "radial bloom"; the engine's shipped assets use only
  `linearGradient`, so the plate/bloom use a **diagonal linear** gradient and the logo is placed via
  `<g transform>` (not nested `<svg>`). Recorded in Global Constraints.
- **Placeholders:** none — exact paths, property values, and commands throughout. The few "tune"
  values (`itemSize`, `fitMult`, `infoPanel` pos) are explicitly visual-iteration steps with a
  render/eyeball check, not unspecified gaps.
- **Type/name consistency:** `system-capsule/<system>.svg` + `_fallback.svg`, `system_rail.xml`,
  `hero-bloom.svg`, `info-panel.svg`, `gen-system-capsules.py`, `FIT_OVERRIDES` used consistently.

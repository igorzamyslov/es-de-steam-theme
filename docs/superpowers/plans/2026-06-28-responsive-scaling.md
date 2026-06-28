# Responsive Scaling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a user-selectable size (ES-DE *Theme font size*: medium/large/x-large) that scales all text and the grid together, and make grid tiles stay 2:3 portrait on any screen aspect (fixing square tiles on phones).

**Architecture:** All sizing lives in one new include `_inc/scale.xml` that defines theme variables per `<fontSize>` selection (type scale + grid height/spacing) and per `<aspectRatio>` (grid item width, to keep portrait). `capabilities.xml` declares the options. Every element file references variables instead of hardcoded sizes. Because each aspect now produces a true 2:3 cell, the cell-shaped SVGs (selector frame, shadows) move to a 2:3 viewBox.

**Tech Stack:** ES-DE modern theme engine; XML; LunaSVG. Verification: `xmllint --noout` + `tools/check-theme-paths.sh` + in-engine load by the user (no unit-test framework for themes).

## Global Constraints
- Medium **font** values = current exact values (no text change at default). Medium **grid** intentionally changes to 2:3 portrait (this is the square-tile fix, applies at all sizes).
- ES-DE resolves variables in **declaration order**: `_inc/scale.xml` MUST be included before the element files; none of its variable names may be declared in `theme.xml`'s root `<variables>` (root wins and blocks overrides).
- Valid `<fontSize>` names: `medium`, `large`, `x-large`. Valid aspect names used: `16:9`, `16:10`, `4:3`, `5:4`, `19.5:9`, `20:9`, `21:9`.
- Each task leaves the theme loadable. After each edit: `xmllint --noout` the changed files; the path check is `bash tools/check-theme-paths.sh` from repo root.
- Repo root: `/Users/igorzamyslov/Projects/es-de-steam-theme`. Theme dir: `steam-bigpicture-es-de/`.

---

## File Structure
- **Create** `steam-bigpicture-es-de/_inc/scale.xml` — all `<fontSize>`/`<aspectRatio>` variable blocks.
- **Modify** `steam-bigpicture-es-de/capabilities.xml` — declare fontSize + aspect options.
- **Modify** `steam-bigpicture-es-de/theme.xml` — include scale.xml.
- **Modify** element files — swap hardcoded sizes for variables: `_inc/system_hero_neon.xml`, `_inc/system_hero_art.xml`, `_inc/section-strip.xml`, `_inc/status.xml`, `_inc/helpsystem.xml`, `_inc/gamelist_list.xml`, `_inc/detail.xml`, `_inc/detail_wide.xml`, `_inc/gamelist_grid.xml`.
- **Modify** `assets/ui/selector-frame.svg`, `assets/ui/capsule-shadow-soft.svg`, `assets/ui/capsule-shadow.svg` — 2:3 viewBox + recomputed geometry (+ shadow softening).

---

## Task 1: Declare capabilities (fontSize + aspect ratios)

**Files:**
- Modify: `steam-bigpicture-es-de/capabilities.xml`

- [ ] **Step 1: Add fontSize + aspect declarations.** Replace the existing aspectRatio block:

```xml
    <aspectRatio>16:9</aspectRatio>
    <aspectRatio>16:10</aspectRatio>
    <aspectRatio>4:3</aspectRatio>
```

with:

```xml
    <aspectRatio>16:9</aspectRatio>
    <aspectRatio>16:10</aspectRatio>
    <aspectRatio>4:3</aspectRatio>
    <aspectRatio>5:4</aspectRatio>
    <aspectRatio>19.5:9</aspectRatio>
    <aspectRatio>20:9</aspectRatio>
    <aspectRatio>21:9</aspectRatio>

    <fontSize>medium</fontSize>
    <fontSize>large</fontSize>
    <fontSize>x-large</fontSize>
```

- [ ] **Step 2: Validate.** Run: `xmllint --noout steam-bigpicture-es-de/capabilities.xml && echo OK` — Expected: `OK`.
- [ ] **Step 3: Commit.**

```bash
git add steam-bigpicture-es-de/capabilities.xml
git commit -m "feat(scale): declare font-size + phone aspect-ratio options"
```

---

## Task 2: Central scale variables (`_inc/scale.xml`)

**Files:**
- Create: `steam-bigpicture-es-de/_inc/scale.xml`
- Modify: `steam-bigpicture-es-de/theme.xml`

**Interfaces — Produces** (variables consumed by later tasks):
- Type scale: `${fsHero} ${fsHeader} ${fsList} ${fsClock} ${fsTitleWide} ${fsTitle} ${fsCount} ${fsButton} ${fsLabel} ${fsMetaWide} ${fsMeta} ${fsTab}`
- Grid: `${gridItemX}` (per aspect×size), `${gridItemY}` and `${gridSpacing}` (per size). Grid uses `<itemSize>${gridItemX} ${gridItemY}</itemSize>` and `<itemSpacing>${gridSpacing}</itemSpacing>`.

- [ ] **Step 1: Create `_inc/scale.xml`** with this exact content:

```xml
<theme>
    <!-- Type scale + grid sizing per Theme Font Size (medium = current). Included before the
         element files so these variables are defined before use (ES-DE resolves in order). -->
    <fontSize name="medium">
        <variables>
            <fsHero>0.052</fsHero><fsHeader>0.032</fsHeader><fsList>0.030</fsList>
            <fsClock>0.030</fsClock><fsTitleWide>0.028</fsTitleWide><fsTitle>0.026</fsTitle>
            <fsCount>0.022</fsCount><fsButton>0.021</fsButton><fsLabel>0.020</fsLabel>
            <fsMetaWide>0.019</fsMetaWide><fsMeta>0.0185</fsMeta><fsTab>0.018</fsTab>
            <gridItemY>0.20</gridItemY><gridSpacing>0.010 0.014</gridSpacing>
        </variables>
    </fontSize>
    <fontSize name="large">
        <variables>
            <fsHero>0.058</fsHero><fsHeader>0.038</fsHeader><fsList>0.036</fsList>
            <fsClock>0.034</fsClock><fsTitleWide>0.033</fsTitleWide><fsTitle>0.031</fsTitle>
            <fsCount>0.026</fsCount><fsButton>0.025</fsButton><fsLabel>0.024</fsLabel>
            <fsMetaWide>0.023</fsMetaWide><fsMeta>0.022</fsMeta><fsTab>0.022</fsTab>
            <gridItemY>0.235</gridItemY><gridSpacing>0.012 0.017</gridSpacing>
        </variables>
    </fontSize>
    <fontSize name="x-large">
        <variables>
            <fsHero>0.064</fsHero><fsHeader>0.044</fsHeader><fsList>0.042</fsList>
            <fsClock>0.038</fsClock><fsTitleWide>0.038</fsTitleWide><fsTitle>0.036</fsTitle>
            <fsCount>0.030</fsCount><fsButton>0.028</fsButton><fsLabel>0.027</fsLabel>
            <fsMetaWide>0.026</fsMetaWide><fsMeta>0.025</fsMeta><fsTab>0.025</fsTab>
            <gridItemY>0.27</gridItemY><gridSpacing>0.014 0.020</gridSpacing>
        </variables>
    </fontSize>

    <!-- grid item WIDTH per aspect x size: itemX = itemY * (2/3) / (W:H) keeps tiles ~2:3 portrait -->
    <aspectRatio name="4:3, 5:4">
        <fontSize name="medium"><variables><gridItemX>0.100</gridItemX></variables></fontSize>
        <fontSize name="large"><variables><gridItemX>0.117</gridItemX></variables></fontSize>
        <fontSize name="x-large"><variables><gridItemX>0.135</gridItemX></variables></fontSize>
    </aspectRatio>
    <aspectRatio name="16:10">
        <fontSize name="medium"><variables><gridItemX>0.083</gridItemX></variables></fontSize>
        <fontSize name="large"><variables><gridItemX>0.098</gridItemX></variables></fontSize>
        <fontSize name="x-large"><variables><gridItemX>0.113</gridItemX></variables></fontSize>
    </aspectRatio>
    <aspectRatio name="16:9">
        <fontSize name="medium"><variables><gridItemX>0.075</gridItemX></variables></fontSize>
        <fontSize name="large"><variables><gridItemX>0.088</gridItemX></variables></fontSize>
        <fontSize name="x-large"><variables><gridItemX>0.101</gridItemX></variables></fontSize>
    </aspectRatio>
    <aspectRatio name="19.5:9, 20:9, 21:9">
        <fontSize name="medium"><variables><gridItemX>0.060</gridItemX></variables></fontSize>
        <fontSize name="large"><variables><gridItemX>0.071</gridItemX></variables></fontSize>
        <fontSize name="x-large"><variables><gridItemX>0.081</gridItemX></variables></fontSize>
    </aspectRatio>
</theme>
```

- [ ] **Step 2: Include it from `theme.xml`** — add the include immediately after the colors include. Replace:

```xml
    <include>./_inc/fonts.xml</include>
    <include>./_inc/colors.xml</include>
```

with:

```xml
    <include>./_inc/fonts.xml</include>
    <include>./_inc/colors.xml</include>
    <!-- size/scale variables (font-size + aspect-ratio); must precede the variant includes -->
    <include>./_inc/scale.xml</include>
```

- [ ] **Step 3: Validate.** Run: `xmllint --noout steam-bigpicture-es-de/_inc/scale.xml steam-bigpicture-es-de/theme.xml && echo OK` — Expected: `OK`. Then `cd /Users/igorzamyslov/Projects/es-de-steam-theme && bash tools/check-theme-paths.sh 2>&1 | grep -i scale.xml || echo "scale.xml resolves OK"`.
- [ ] **Step 4: Commit.**

```bash
git add steam-bigpicture-es-de/_inc/scale.xml steam-bigpicture-es-de/theme.xml
git commit -m "feat(scale): central scale.xml (type scale + grid matrix)"
```

---

## Task 3: Wire system view + chrome fonts to variables

**Files:**
- Modify: `_inc/system_hero_neon.xml`, `_inc/system_hero_art.xml`, `_inc/section-strip.xml`, `_inc/status.xml`, `_inc/helpsystem.xml` (all under `steam-bigpicture-es-de/`)

**Interfaces — Consumes:** `${fsHero} ${fsLabel} ${fsCount} ${fsTab} ${fsClock}` from Task 2.

- [ ] **Step 1: Hero files.** In BOTH `_inc/system_hero_neon.xml` and `_inc/system_hero_art.xml`, replace the three font sizes (these exact substrings each occur once per file):
  - `<fontSize>0.052</fontSize>` → `<fontSize>${fsHero}</fontSize>` (sysName)
  - sysFull line `<fontPath>${fontSemiBold}</fontPath><fontSize>0.020</fontSize>` → `<fontPath>${fontSemiBold}</fontPath><fontSize>${fsLabel}</fontSize>`
  - sysCount line `<fontPath>${fontSemiBold}</fontPath><fontSize>0.022</fontSize>` → `<fontPath>${fontSemiBold}</fontPath><fontSize>${fsCount}</fontSize>`

- [ ] **Step 2: section-strip.xml.** Replace all four tab font sizes `<fontPath>${fontSemiBold}</fontPath><fontSize>0.018</fontSize>` → `<fontPath>${fontSemiBold}</fontPath><fontSize>${fsTab}</fontSize>` (use replace-all; 4 occurrences).

- [ ] **Step 3: status.xml.** Replace `<fontSize>0.03</fontSize>` → `<fontSize>${fsClock}</fontSize>` (clock).

- [ ] **Step 4: helpsystem.xml.** Replace `<fontSize>0.02</fontSize>` → `<fontSize>${fsLabel}</fontSize>` (help).

- [ ] **Step 5: Validate.** Run:
```bash
cd /Users/igorzamyslov/Projects/es-de-steam-theme/steam-bigpicture-es-de
xmllint --noout _inc/system_hero_neon.xml _inc/system_hero_art.xml _inc/section-strip.xml _inc/status.xml _inc/helpsystem.xml && echo OK
```
Expected: `OK`. (At medium, rendering is unchanged.)

- [ ] **Step 6: Commit.**
```bash
git add steam-bigpicture-es-de/_inc/system_hero_neon.xml steam-bigpicture-es-de/_inc/system_hero_art.xml steam-bigpicture-es-de/_inc/section-strip.xml steam-bigpicture-es-de/_inc/status.xml steam-bigpicture-es-de/_inc/helpsystem.xml
git commit -m "feat(scale): wire system view + chrome fonts to variables"
```

---

## Task 4: Wire list + detail-panel fonts to variables

**Files:**
- Modify: `_inc/gamelist_list.xml`, `_inc/detail.xml`, `_inc/detail_wide.xml`

**Interfaces — Consumes:** `${fsHeader} ${fsTab} ${fsList} ${fsTitle} ${fsTitleWide} ${fsMeta} ${fsMetaWide} ${fsButton}`.

- [ ] **Step 1: gamelist_list.xml.**
  - glHeader `<fontPath>${fontDisplay}</fontPath><fontSize>0.032</fontSize>` → `...<fontSize>${fsHeader}</fontSize>`
  - glCount `<fontPath>${fontSemiBold}</fontPath><fontSize>0.018</fontSize>` → `...<fontSize>${fsTab}</fontSize>`
  - textlist `<fontSize>0.030</fontSize>` → `<fontSize>${fsList}</fontSize>`

- [ ] **Step 2: detail.xml.**
  - detailTitle `<fontSize>0.026</fontSize>` → `<fontSize>${fsTitle}</fontSize>`
  - Replace-all `<fontSize>0.0185</fontSize>` → `<fontSize>${fsMeta}</fontSize>` (metadata keys/values, descLabel, desc — 10 occurrences)
  - detailPlayLabel `<fontSize>0.021</fontSize>` → `<fontSize>${fsButton}</fontSize>`

- [ ] **Step 3: detail_wide.xml.**
  - detailTitle `<fontSize>0.028</fontSize>` → `<fontSize>${fsTitleWide}</fontSize>`
  - Replace-all `<fontSize>0.019</fontSize>` → `<fontSize>${fsMetaWide}</fontSize>` (metadata + desc — 10 occurrences)
  - descLabel `<fontSize>0.0185</fontSize>` → `<fontSize>${fsMetaWide}</fontSize>` (1 occurrence)
  - detailPlayLabel `<fontSize>0.021</fontSize>` → `<fontSize>${fsButton}</fontSize>`

- [ ] **Step 4: Validate.** Run:
```bash
cd /Users/igorzamyslov/Projects/es-de-steam-theme/steam-bigpicture-es-de
xmllint --noout _inc/gamelist_list.xml _inc/detail.xml _inc/detail_wide.xml && echo OK
grep -cE '<fontSize>0\.[0-9]+</fontSize>' _inc/detail.xml _inc/detail_wide.xml
```
Expected: `OK`; the grep reports `0` for both detail files (no literal sizes remain — all are variables now).

- [ ] **Step 5: Commit.**
```bash
git add steam-bigpicture-es-de/_inc/gamelist_list.xml steam-bigpicture-es-de/_inc/detail.xml steam-bigpicture-es-de/_inc/detail_wide.xml
git commit -m "feat(scale): wire list + detail-panel fonts to variables"
```

---

## Task 5: Responsive grid (variables + 2:3 cell SVGs + softer shadow)

**Files:**
- Modify: `_inc/gamelist_grid.xml`
- Modify: `assets/ui/selector-frame.svg`, `assets/ui/capsule-shadow-soft.svg`, `assets/ui/capsule-shadow.svg`

**Interfaces — Consumes:** `${gridItemX} ${gridItemY} ${gridSpacing} ${fsHeader} ${fsTab}`.

- [ ] **Step 1: gamelist_grid.xml fonts + sizing.**
  - glHeader `<fontPath>${fontDisplay}</fontPath><fontSize>0.032</fontSize>` → `...<fontSize>${fsHeader}</fontSize>`
  - glCount `<fontPath>${fontSemiBold}</fontPath><fontSize>0.018</fontSize>` → `...<fontSize>${fsTab}</fontSize>`
  - grid text fallback `<fontSize>0.018</fontSize>` → `<fontSize>${fsTab}</fontSize>`
  - `<itemSize>0.095 0.195</itemSize>` → `<itemSize>${gridItemX} ${gridItemY}</itemSize>`
  - `<itemSpacing>0.010 0.014</itemSpacing>` → `<itemSpacing>${gridSpacing}</itemSpacing>`

- [ ] **Step 2: selector-frame.svg** — rewrite to a 2:3 viewBox (cell is now true 2:3):

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 300">
  <!-- thin light-grey focus frame near the cell edge (cell is now 2:3 portrait) -->
  <rect x="1.3" y="1.3" width="197.4" height="297.4"
        fill="none" stroke="#d6dee6" stroke-opacity="0.92" stroke-width="2.6"/>
</svg>
```

- [ ] **Step 3: capsule-shadow-soft.svg** — rewrite for 2:3 (card at 0.91 centered = x9 y13.5 w182 h273), softer halo (7 stops) + crisp band eased to 0.26:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 300">
  <!-- soft ambient halo (7 stops) + crisp bottom-right band + card; all within the cell margin -->
  <rect x="0"   y="4.5"  width="200"   height="291"   fill="#000000" fill-opacity="0.02"/>
  <rect x="1.5" y="6"    width="197"   height="288"   fill="#000000" fill-opacity="0.035"/>
  <rect x="3"   y="7.5"  width="194"   height="285"   fill="#000000" fill-opacity="0.05"/>
  <rect x="4.5" y="9"    width="191"   height="282"   fill="#000000" fill-opacity="0.065"/>
  <rect x="6"   y="10.5" width="188"   height="279"   fill="#000000" fill-opacity="0.08"/>
  <rect x="7.2" y="11.7" width="185.6" height="276.6" fill="#000000" fill-opacity="0.095"/>
  <rect x="8.1" y="12.6" width="183.8" height="274.8" fill="#000000" fill-opacity="0.11"/>
  <rect x="11.5" y="16.5" width="182" height="273" fill="#000000" fill-opacity="0.26"/>
  <rect x="9"    y="13.5" width="182" height="273" fill="#1a222d"/>
</svg>
```

- [ ] **Step 4: capsule-shadow.svg** (crisp variant, kept consistent) — rewrite for 2:3:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 300">
  <!-- CRISP drop variant: two offset dark rects bottom-right + card (2:3 cell) -->
  <rect x="16" y="22.5" width="182" height="273" fill="#000000" fill-opacity="0.13"/>
  <rect x="13" y="18.5" width="182" height="273" fill="#000000" fill-opacity="0.26"/>
  <rect x="9"  y="13.5" width="182" height="273" fill="#1a222d"/>
</svg>
```

- [ ] **Step 5: Validate.** Run:
```bash
cd /Users/igorzamyslov/Projects/es-de-steam-theme/steam-bigpicture-es-de
xmllint --noout _inc/gamelist_grid.xml assets/ui/selector-frame.svg assets/ui/capsule-shadow-soft.svg assets/ui/capsule-shadow.svg && echo OK
```
Expected: `OK`.

- [ ] **Step 6: Commit.**
```bash
git add steam-bigpicture-es-de/_inc/gamelist_grid.xml steam-bigpicture-es-de/assets/ui/selector-frame.svg steam-bigpicture-es-de/assets/ui/capsule-shadow-soft.svg steam-bigpicture-es-de/assets/ui/capsule-shadow.svg
git commit -m "feat(scale): responsive portrait grid + 2:3 cell SVGs + softer shadow"
```

---

## Task 6: Final verification

**Files:** none (validation only).

- [ ] **Step 1: Full XML + path check.**
```bash
cd /Users/igorzamyslov/Projects/es-de-steam-theme
find steam-bigpicture-es-de -name '*.xml' -print0 | xargs -0 xmllint --noout && echo "ALL XML OK"
bash tools/check-theme-paths.sh 2>&1 | grep -ciE 'MISSING' | xargs echo "MISSING (optional per-system includes only):"
```
Expected: `ALL XML OK`; MISSING count is only the known optional per-system templated includes.

- [ ] **Step 2: Confirm no stray hardcoded sizes remain in wired elements.**
```bash
cd /Users/igorzamyslov/Projects/es-de-steam-theme/steam-bigpicture-es-de
grep -rnoE '<fontSize>0\.[0-9]+</fontSize>' _inc | grep -v scale.xml || echo "no literal fontSizes outside scale.xml"
```
Expected: `no literal fontSizes outside scale.xml`.

- [ ] **Step 3: In-engine (user).** Load in ES-DE: at **medium**, text matches the previous look and grid tiles are 2:3 portrait (de-squared); switch *UI Settings → Theme font size* to **large** / **x-large** — all text + grid scale up with no overlaps. On the phone (19.5:9 / 20:9): tiles are portrait, text legible.

---

## Self-Review notes
- Spec coverage: A (type scale) → Tasks 2–5; B (portrait grid + aspects) → Tasks 1,2,5; C (shadow) → Task 5; capabilities → Task 1; non-goals respected (no repositioning, no separate grid control).
- Type consistency: variable names identical across scale.xml (producer) and all consumers (`fsHero/fsHeader/fsList/fsClock/fsTitleWide/fsTitle/fsCount/fsButton/fsLabel/fsMetaWide/fsMeta/fsTab`, `gridItemX/gridItemY/gridSpacing`).
- Medium grid note: tiles change to 2:3 at medium by design (square-tile fix), while medium fonts are unchanged.

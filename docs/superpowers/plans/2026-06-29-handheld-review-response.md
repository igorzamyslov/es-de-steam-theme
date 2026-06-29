# Handheld Review Response Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Address two external reviews of the Steam Big Picture ES-DE theme — make the grid/detail render art on real libraries, kill empty-state clutter, make the accent per-system, add budget-handheld aspect ratios, tell the truth in the README, and ship a hero-art generation kit.

**Architecture:** Pure ES-DE theme XML edits plus README/doc copy plus one Python generator script. No app code, no build. ES-DE resolves `<variables>` globally and in declaration order across the parsed theme set; several edits depend on that ordering.

**Tech Stack:** ES-DE theme XML/SVG, Markdown, Python 3 (stdlib `xml.etree.ElementTree`).

## Global Constraints

- No ES-DE renderer or image generator is available in this workspace. Automated verification is XML/SVG well-formedness + asset-reference resolution only; visual results need the user's eyes in ES-DE.
- Verification commands (mirror the CI pre-commit hooks; `pre-commit` itself is not installed here):
  - XML/SVG well-formedness: `xmllint --noout <files>`
  - Theme asset references resolve: `python3 scripts/check-asset-refs.py`
- ES-DE color values are `RRGGBB` or `RRGGBBAA`; variable concatenation like `${systemColor}ff` is valid (the hero tint already uses `${systemColor}cc`).
- Do not modify vendored dirs: `system-logos/`, `system-controllers-outline/`, `system-metadata/`.
- Never add a `Co-Authored-By` trailer to commits.
- Theme file root is `steam-bigpicture-es-de/`. Spec: `docs/superpowers/specs/2026-06-29-handheld-review-response-design.md`.

---

### Task 1: Art fallback chains (grid + detail still)

**Files:**
- Modify: `steam-bigpicture-es-de/_inc/gamelist_grid.xml` (line 16)
- Modify: `steam-bigpicture-es-de/theme.xml` (lines 28–31)

**Interfaces:**
- Produces: nothing consumed by later tasks (self-contained).

- [ ] **Step 1: Widen the grid image type**

In `gamelist_grid.xml`, change line 16 from:

```xml
            <imageType>cover</imageType>
```

to:

```xml
            <imageType>cover, miximage, screenshot, marquee</imageType>
```

- [ ] **Step 2: Make the detail still fall back instead of going straight to placeholder**

In `theme.xml`, replace the four colorScheme lines (28–31) with:

```xml
    <colorScheme name="marqueeVideo"><variables><detailMediaType>marquee, screenshot, cover</detailMediaType><mediaDelay>2.5</mediaDelay></variables></colorScheme>
    <colorScheme name="screenshotVideo"><variables><detailMediaType>screenshot, cover</detailMediaType><mediaDelay>2.5</mediaDelay></variables></colorScheme>
    <colorScheme name="marqueeStill"><variables><detailMediaType>marquee, screenshot, cover</detailMediaType><mediaDelay>100000</mediaDelay></variables></colorScheme>
    <colorScheme name="screenshotStill"><variables><detailMediaType>screenshot, cover</detailMediaType><mediaDelay>100000</mediaDelay></variables></colorScheme>
```

(`detail.xml` / `detail_wide.xml` keep `<imageType>${detailMediaType}</imageType>` and the `capsule-placeholder.svg` final fallback unchanged.)

- [ ] **Step 3: Verify well-formedness**

Run: `xmllint --noout steam-bigpicture-es-de/_inc/gamelist_grid.xml steam-bigpicture-es-de/theme.xml`
Expected: no output (success).

- [ ] **Step 4: Verify asset references still resolve**

Run: `python3 scripts/check-asset-refs.py`
Expected: exits 0, prints its OK summary.

- [ ] **Step 5: Commit**

```bash
git add steam-bigpicture-es-de/_inc/gamelist_grid.xml steam-bigpicture-es-de/theme.xml
git commit -m "fix(art): fall back through miximage/screenshot/marquee so the grid and detail panel render on any scrape profile"
```

---

### Task 2: Empty-state polish (stars, muted contrast, blank-label note)

**Files:**
- Modify: `steam-bigpicture-es-de/_inc/detail.xml` (line 38; add a comment near 46)
- Modify: `steam-bigpicture-es-de/_inc/detail_wide.xml` (line 38)
- Modify: `steam-bigpicture-es-de/_inc/colors.xml` (line 10)

**Interfaces:**
- Produces: nothing consumed by later tasks.

- [ ] **Step 1: Hide the rating row when zero (grid panel)**

In `detail.xml` line 38, change `<hideIfZero>false</hideIfZero>` to `<hideIfZero>true</hideIfZero>`.

- [ ] **Step 2: Hide the rating row when zero (wide panel)**

In `detail_wide.xml` line 38, change `<hideIfZero>false</hideIfZero>` to `<hideIfZero>true</hideIfZero>`.

- [ ] **Step 3: Document the blank-label limitation**

In `detail.xml`, immediately before the `detailGenreKey` element (currently line 46), add this comment line (matching the file's indentation):

```xml
        <!-- NOTE: ES-DE has no per-element "hide if metadata empty", so these key labels
             (Genre/Developer/Players/Released/Description) still render for unscraped games.
             Known limitation; do not "fix" by deleting labels (they're correct once scraped). -->
```

- [ ] **Step 4: Bump muted text contrast for sunlit handheld screens**

In `colors.xml` line 10, change:

```xml
        <cMuted>6d7884ff</cMuted>
```

to:

```xml
        <cMuted>8a94a0ff</cMuted>
```

- [ ] **Step 5: Verify well-formedness**

Run: `xmllint --noout steam-bigpicture-es-de/_inc/detail.xml steam-bigpicture-es-de/_inc/detail_wide.xml steam-bigpicture-es-de/_inc/colors.xml`
Expected: no output.

- [ ] **Step 6: Commit**

```bash
git add steam-bigpicture-es-de/_inc/detail.xml steam-bigpicture-es-de/_inc/detail_wide.xml steam-bigpicture-es-de/_inc/colors.xml
git commit -m "fix(detail): hide empty star row, lift muted-text contrast for handhelds, document the blank-label limitation"
```

---

### Task 3: Per-system accent (the riskiest task — needs ES-DE visual confirmation later)

**Files:**
- Modify: `steam-bigpicture-es-de/_inc/system_hero_neon.xml` (include block, lines 4–21)
- Modify: `steam-bigpicture-es-de/_inc/system_hero_art.xml` (include block, lines 4–21)
- Modify: `steam-bigpicture-es-de/_inc/section-state/_default.xml`
- Modify: `steam-bigpicture-es-de/_inc/section-state/auto-allgames.xml`
- Modify: `steam-bigpicture-es-de/_inc/section-state/auto-favorites.xml`
- Modify: `steam-bigpicture-es-de/_inc/section-state/auto-lastplayed.xml`
- Modify: `steam-bigpicture-es-de/_inc/colors.xml` (remove `cAccent`)

**Interfaces:**
- Consumes: `${systemColor}` (defined by `system-metadata/*.xml` and overridden for collections by `section-accent/auto-*.xml`).
- Produces: the section-strip underline color is now `${systemColor}ff` for the active tab; `cAccent` no longer exists (no task may reference it).

- [ ] **Step 1: Reorder includes in the neon hero so `${systemColor}` precedes the section-strip**

In `system_hero_neon.xml`, replace the include block (the `helpsystem`→`spec-overrides` includes plus their comments, currently lines 2–21) with this exact order and comments:

```xml
    <include>./helpsystem.xml</include>
    <include>./status.xml</include>
    <!-- official ES-DE per-system metadata FIRST: defines ${systemName} + ${systemColor};
         everything below (section-accent, section-state) reads ${systemColor}. -->
    <include>./../system-metadata/_default.xml</include>
    <include>./../system-metadata/${system.theme}.xml</include>
    <!-- targeted overrides for ES-DE short names that collapse to the manufacturer (e.g. nes -> NES) -->
    <include>./name-overrides/${system.theme}.xml</include>
    <!-- collection accent: overrides ${systemColor} for the auto-collections (after metadata) -->
    <include>./section-accent/${system.theme}.xml</include>
    <!-- spec-line composition (after metadata so the nested vars resolve) -->
    <include>./spec-overrides/_default.xml</include>
    <include>./spec-overrides/${system.theme}.xml</include>
    <!-- section-strip highlight state: now AFTER metadata so the active underline can be
         ${systemColor}. _default first, then per-collection override (last include wins). -->
    <include>./section-state/_default.xml</include>
    <include>./section-state/${system.theme}.xml</include>
    <!-- Steam-style persistent section nav (consumes the section-state vars above) -->
    <include>./section-strip.xml</include>
```

- [ ] **Step 2: Reorder includes in the art hero identically**

In `system_hero_art.xml`, replace its include block (currently lines 2–21) with the **exact same** block from Step 1.

- [ ] **Step 3: Point the default active underline at the system color**

In `section-state/_default.xml`, change the underline line from:

```xml
        <secUnPlat>3a9bffff</secUnPlat>
```

to:

```xml
        <secUnPlat>${systemColor}ff</secUnPlat>
```

Also update the comment block at the top of the file: replace the line
`active text = e8edf2 (cText), inactive = 8f98a0 (readable grey);` ... `underline accent = 3a9bff (cAccent) / transparent.`
with:

```xml
         active text = e8edf2 (cText), inactive = 8f98a0 (readable grey);
         active underline = ${systemColor} (per-platform / per-collection) / transparent. -->
```

- [ ] **Step 4: Point the collection underlines at the system color**

- In `section-state/auto-allgames.xml`, change `<secUnLibrary>3a9bffff</secUnLibrary>` to `<secUnLibrary>${systemColor}ff</secUnLibrary>`.
- In `section-state/auto-favorites.xml`, change `<secUnFav>3a9bffff</secUnFav>` to `<secUnFav>${systemColor}ff</secUnFav>`.
- In `section-state/auto-lastplayed.xml`, change `<secUnRecent>3a9bffff</secUnRecent>` to `<secUnRecent>${systemColor}ff</secUnRecent>`.

- [ ] **Step 5: Remove the now-dead `cAccent` variable**

In `colors.xml`, delete the line `<cAccent>3a9bffff</cAccent>` and update the surrounding comment so it no longer claims a baked accent. The `<variables>` block becomes:

```xml
    <variables>
        <cText>e8edf2ff</cText>
        <cText2>aab4c0ff</cText2>
        <cMuted>8a94a0ff</cMuted>
        <cStar>f5c518ff</cStar>
    </variables>
```

And change the leading comment's last sentence to: `The accent is per-system: the section-strip underline tracks ${systemColor} (see section-state/). Background/panel/green colours remain baked into the SVG assets in assets/ui/.`

- [ ] **Step 6: Confirm no dangling `cAccent` / `3a9bff` references remain**

Run: `grep -rn "cAccent\|3a9bff" steam-bigpicture-es-de/ --include=*.xml`
Expected: no matches.

- [ ] **Step 7: Verify well-formedness + asset refs**

Run: `xmllint --noout steam-bigpicture-es-de/_inc/system_hero_neon.xml steam-bigpicture-es-de/_inc/system_hero_art.xml steam-bigpicture-es-de/_inc/section-state/*.xml steam-bigpicture-es-de/_inc/colors.xml && python3 scripts/check-asset-refs.py`
Expected: no xmllint output; checker exits 0.

- [ ] **Step 8: Commit**

```bash
git add steam-bigpicture-es-de/_inc/system_hero_neon.xml steam-bigpicture-es-de/_inc/system_hero_art.xml steam-bigpicture-es-de/_inc/section-state steam-bigpicture-es-de/_inc/colors.xml
git commit -m "feat(accent): make the active section-strip underline track per-system ${systemColor}; remove the dead cAccent variable"
```

---

### Task 4: Add 3:2 and 5:3 aspect ratios

**Files:**
- Modify: `steam-bigpicture-es-de/capabilities.xml` (after line 11)
- Modify: `steam-bigpicture-es-de/_inc/gamelist_grid.xml` (line 49)
- Modify: `steam-bigpicture-es-de/_inc/scale.xml` (after the existing aspectRatio blocks)

**Interfaces:**
- Produces: nothing consumed by later tasks.

- [ ] **Step 1: Declare the ratios as capabilities**

In `capabilities.xml`, after the `21:9` line (line 11), add:

```xml
    <aspectRatio>3:2</aspectRatio>
    <aspectRatio>5:3</aspectRatio>
```

- [ ] **Step 2: Include the side-panel layout for the new ratios**

In `gamelist_grid.xml` line 49, change:

```xml
    <aspectRatio name="16:9, 16:10, 4:3, 5:4, 19.5:9, 20:9, 21:9">
```

to:

```xml
    <aspectRatio name="16:9, 16:10, 4:3, 5:4, 3:2, 5:3, 19.5:9, 20:9, 21:9">
```

- [ ] **Step 3: Add per-font-size capsule widths**

In `scale.xml`, after the `21:9` aspectRatio block (ends ~line 114), add (values are `itemX = itemY · (2/3) / (W:H)` with the per-size `gridItemY` 0.240 / 0.236 / 0.357):

```xml
    <aspectRatio name="3:2">
        <fontSize name="medium"><variables><gridItemX>0.1067</gridItemX></variables></fontSize>
        <fontSize name="large"><variables><gridItemX>0.1049</gridItemX></variables></fontSize>
        <fontSize name="x-large"><variables><gridItemX>0.1587</gridItemX></variables></fontSize>
    </aspectRatio>
    <aspectRatio name="5:3">
        <fontSize name="medium"><variables><gridItemX>0.0960</gridItemX></variables></fontSize>
        <fontSize name="large"><variables><gridItemX>0.0944</gridItemX></variables></fontSize>
        <fontSize name="x-large"><variables><gridItemX>0.1428</gridItemX></variables></fontSize>
    </aspectRatio>
```

- [ ] **Step 4: Verify well-formedness**

Run: `xmllint --noout steam-bigpicture-es-de/capabilities.xml steam-bigpicture-es-de/_inc/gamelist_grid.xml steam-bigpicture-es-de/_inc/scale.xml`
Expected: no output.

- [ ] **Step 5: Commit**

```bash
git add steam-bigpicture-es-de/capabilities.xml steam-bigpicture-es-de/_inc/gamelist_grid.xml steam-bigpicture-es-de/_inc/scale.xml
git commit -m "feat(aspect): support 3:2 and 5:3 (common budget-handheld landscape ratios)"
```

---

### Task 5: Steam-like system-to-system transition

**Files:**
- Modify: `steam-bigpicture-es-de/capabilities.xml` (line 35)

**Interfaces:**
- Produces: nothing consumed by later tasks.

- [ ] **Step 1: Change systemToSystem to slide**

In `capabilities.xml` line 35, change:

```xml
        <systemToSystem>instant</systemToSystem>
```

to:

```xml
        <systemToSystem>slide</systemToSystem>
```

(Leave `gamelistToGamelist` as `instant`.)

- [ ] **Step 2: Verify well-formedness**

Run: `xmllint --noout steam-bigpicture-es-de/capabilities.xml`
Expected: no output.

- [ ] **Step 3: Commit**

```bash
git add steam-bigpicture-es-de/capabilities.xml
git commit -m "tweak(transitions): slide on system-to-system for a more Steam-like feel; keep gamelist instant"
```

---

### Task 6: README + presentation honesty

**Files:**
- Modify: `README.md`

**Interfaces:**
- Produces: nothing consumed by later tasks.

- [ ] **Step 1: Reframe the intro accent + add the ES-DE-only line**

In `README.md`, in the first paragraph (line 3), change the trailing sentence
`The palette is dark throughout — Steam's characteristic navy with a neon-cyan accent.`
to:

```markdown
The palette is dark throughout — Steam's characteristic navy, with a per-platform accent: the active nav underline picks up each system's signature color. **ES-DE only** — it runs on Steam Deck, desktop, and the distros that bundle ES-DE (it is not a muOS/Knulli/ROCKNIX/Batocera theme).
```

- [ ] **Step 2: Make enabling collections the FIRST install step**

In `README.md`, in the `## Install` section, insert a new step before the current step 1 (so collections come first), and keep the existing copy steps renumbered after it:

```markdown
1. **Enable automatic collections first.** This theme's top nav (**Library / Favorites / Recent / Platforms**) is its Steam-style spine; the first three are ES-DE *automatic collections*, which are **off by default**. Without them, three of the four tabs lead to empty systems and the theme looks half-broken. In ES-DE: **Game Collection Settings → Enable automatic game collections** (details in [Collections](#collections-library-favorites-recent)).
2. Download or clone this repository.
3. Copy (or symlink) the `steam-bigpicture-es-de/` directory into your ES-DE themes folder:
```

(Renumber the remaining sub-steps/launch step accordingly; keep the existing folder paths and the "select Steam Big Picture" step.)

- [ ] **Step 3: Add a small-screen legibility tip in Install**

Immediately after the install steps (before or merged with the existing `> **Note:**` block), add:

```markdown
> **Small screens (5–6" handhelds):** the default **Medium** font size is the densest grid. For comfortable reading set **UI Settings → Theme font size** to **Large** or **X-Large**.
```

And update the existing downloader note to frame it as a known next step:

```markdown
> **Not in the ES-DE theme downloader yet** — manual installation (above) is required for now. Getting it listed is a tracked follow-up.
```

- [ ] **Step 4: Tell the truth about device/aspect support**

Replace the body of the `## Aspect ratios` section with:

```markdown
The same side-panel layout (grid/list on the left, detail panel on the right) is used across every supported aspect ratio — the grid just packs more columns on wider screens:

- **First-class handhelds:** Steam Deck (`16:10`) and Windows handhelds — ROG Ally / Legion Go (`16:9`).
- **Also supported:** desktop/TV `4:3` and `5:4`; budget-handheld landscape `3:2` and `5:3` (Anbernic / Powkiddy / Miyoo class); phone-style ultrawide `19.5:9`, `20:9`, `21:9`.
- **Not yet supported:** square `1:1` (e.g. CubeXX, RGB30) and any **portrait** orientation — these need a different layout than the side-panel design.
```

- [ ] **Step 5: Add a version-spread caveat to Requirements**

In `## Requirements`, change the ES-DE bullet to:

```markdown
- **ES-DE 2.0 or later** (developed and tested against the 3.4.x series). Handheld distros often bundle older builds — **below 3.x, expect rough edges**.
```

- [ ] **Step 6: Reorder + recaption the hero-art screenshot**

In `## Screenshots`, move the `### System view — per-platform hero art` block (image `04`) so it appears **after** the `### Theme settings` block (image `05`), and change its heading + caption to:

```markdown
### System view — per-platform hero art *(after you add your own art)*

![Example Game Boy Advance hero — produced by adding your own per-platform art; see "Adding hero art"](screenshots/04-system-hero-art.png)
```

- [ ] **Step 7: Lint + link-check the markdown if tooling is present, else eyeball**

Run: `command -v markdownlint >/dev/null && markdownlint --config .markdownlint.jsonc README.md || echo "markdownlint not installed — skipping (CI will run it)"`
Expected: either clean output, or the skip message. Manually confirm all heading levels and list numbering are sequential.

- [ ] **Step 8: Commit**

```bash
git add README.md
git commit -m "docs(readme): honest device/aspect claims, collections as install step 1, small-screen tip, version caveat, recaptioned hero-art shot"
```

---

### Task 7: Hero-art generation kit

**Files:**
- Create: `docs/hero-art-style-spec.md`
- Create: `scripts/gen-hero-art-prompts.py`
- Create: `docs/hero-art/prompts.tsv` (generated, committed)
- Modify: `docs/hero-art-pipeline.md` (link to the style spec)

**Interfaces:**
- Consumes: `steam-bigpicture-es-de/system-metadata/*.xml` (top-level `<variables>` only).
- Produces: a TSV manifest, one row per system; not consumed by other tasks.

- [ ] **Step 1: Write the locked style spec**

Create `docs/hero-art-style-spec.md`:

```markdown
# Hero art — locked style spec

The `Hero (art)` variant loads one poster per system at
`steam-bigpicture-es-de/systems/art/<system>.jpg`. This spec locks the look so a full
pack stays visually consistent. The shipped `gba.jpg` is the reference frame.

## Canvas & technical

- **Size:** 1280×720 px, JPG, sRGB.
- **Composition:** the system's hardware (console/handheld) is the hero subject, set in
  an atmospheric scene evoking that platform's era and signature games (no copyrighted
  character likenesses if redistribution license is a concern — favour generic motifs).
- **Left-darkening:** the left ~45% must read dark enough for white title/spec/description
  text (the theme draws a left scrim, but bake in extra falloff).
- **Bottom-darkening:** the bottom ~30% sits under the icon rail shelf — keep it calm.

## Look (reference: gba.jpg)

- Detailed **pixel-art poster** style, painterly lighting, neon rim light.
- A glowing marquee/sign carrying the system name (the manifest provides the exact text).
- Saturated midtones; atmospheric depth (fog/bokeh) behind the subject.

## 8-mood palette anchor

Tie each poster's dominant light to the system's `${systemColor}` (provided per row in
the manifest) so the art and the in-theme per-system accent agree. Keep one of 8 mood
families: warm torchlight, cool fog, magenta neon, emerald CRT, amber sunset, violet
synthwave, teal abyss, crimson arcade. Pick the family nearest the system color.

## Generation workflow

1. Generate 5–8 anchors; lock a style reference + weight.
2. Batch the per-system prompts from `docs/hero-art/prompts.tsv` (see
   `scripts/gen-hero-art-prompts.py`) through your image model with that style ref.
3. Expect ~15–20% regeneration for drift.
4. Confirm the model's output license permits CC-BY-NC-SA redistribution.

## Post-process

- Crop/cover to 1280×720; apply the left + bottom darkening; export JPG (quality ~85).
- Save as `steam-bigpicture-es-de/systems/art/<system>.jpg` where `<system>` is the
  ES-DE `${system.theme}` key (the manifest's first column).
```

- [ ] **Step 2: Write the manifest generator**

Create `scripts/gen-hero-art-prompts.py`:

```python
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
```

- [ ] **Step 3: Generate the manifest and sanity-check it**

Run: `python3 scripts/gen-hero-art-prompts.py`
Expected: prints `wrote <N> prompts to docs/hero-art/prompts.tsv` with N ≈ 210+ (every non-`_` system file).

Run: `head -3 docs/hero-art/prompts.tsv && wc -l docs/hero-art/prompts.tsv`
Expected: a header row plus one row per system; the `snes` row's prompt names "Super Nintendo" and color `df5142`.

Run: `grep -P '^snes\t' docs/hero-art/prompts.tsv`
Expected: a line whose prompt contains `Super Nintendo` and `#df5142`.

- [ ] **Step 4: Link the style spec from the pipeline doc**

In `docs/hero-art-pipeline.md`, add near the top (after line 1's heading):

```markdown
> The locked look, palette, and post-process live in **[hero-art-style-spec.md](hero-art-style-spec.md)**.
> Per-system prompts are generated into `docs/hero-art/prompts.tsv` by
> `scripts/gen-hero-art-prompts.py` — run it, then batch the rows through your image model.
```

- [ ] **Step 5: Verify the script is clean**

Run: `python3 -m py_compile scripts/gen-hero-art-prompts.py && echo OK`
Expected: `OK`.

- [ ] **Step 6: Commit**

```bash
git add docs/hero-art-style-spec.md scripts/gen-hero-art-prompts.py docs/hero-art/prompts.tsv docs/hero-art-pipeline.md
git commit -m "docs(hero-art): add a generation kit — locked style spec, per-system prompt generator, and committed manifest"
```

---

## Final verification (after all tasks)

- [ ] **Run the full automated suite that mirrors CI:**

```bash
xmllint --noout $(git ls-files 'steam-bigpicture-es-de/*.xml' 'steam-bigpicture-es-de/*.svg' | grep -Ev 'system-logos|system-controllers-outline|system-metadata')
python3 scripts/check-asset-refs.py
```
Expected: no xmllint output; checker exits 0.

- [ ] **Hand the user the ES-DE visual checklist** (cannot be verified here): grid renders capsules on a screenshot/marquee-only library; detail panel is populated for a marquee-less game; an unrated game shows no star row; the active tab underline shows the platform/collection color (e.g. SNES red, Favorites amber); a 3:2 / 5:3 device packs a sane column count; system→system slides.

# ES-DE "Steam Big Picture" Theme — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an ES-DE theme that recreates modern Steam Big Picture / Deck UI, with a hero+rail (and no-hero) system view, a grid/list gamelist, and a disciplined "Dead Cells" atmospheric hero layer, offered as 6 user-selectable variants.

**Architecture:** A modern ES-DE theme (engine ≥ 2.0). `capabilities.xml` declares 6 variants (3 system layouts × 2 gamelist layouts) + colorScheme + aspect ratios. `theme.xml` composes each variant from shared layout modules in `_inc/` via `<include>`. Per-system icons/logos/colors come from ES-DE's official asset repos pulled in as `git subtree`. Hero art is a deferred asset layer (placeholder now).

**Tech Stack:** ES-DE theme engine (XML), SVG/PNG/WebP assets, TTF font (Inter), git + git-subtree, `xmllint` for validation.

## Global Constraints

- **Engine:** ES-DE modern theme engine, min 2.0.0; target latest stable 3.4.x.
- **Theme directory name MUST end in `-es-de`:** `steam-bigpicture-es-de`.
- **`capabilities.xml`** is mandatory, lives at the theme root, and is **only re-read on full ES-DE restart** (not `Ctrl+R`).
- **Filenames lowercase** (Linux is case-sensitive). Asset paths relative to the theme file use `./`.
- **Fonts** must be TTF/OTF (SVG fonts unsupported). Use **Inter** (OFL); optionally Motiva Sans if the user supplies it.
- **Reference resolution 1920×1080 (16:9).** `fontSize`/`pos.y`/`size.y` are fractions of screen height; `pos.x`/`size.x` of width.
- **Color format** is `RRGGBBAA` (alpha last). Blue `3a9bff` is **focus/interactive only**; rating stars gold `f5c518`; Play accent green.
- **One primary element per view** (`carousel`/`grid`/`textlist`); a carousel/grid item shows **image XOR text**, never both.
- **System view renders per-system:** `${system.theme}` / `${system.name}` resolve to the *focused* system; a secondary image keyed to it follows the selection. A plain `<path>` image needs **no** `gameselector`; `imageType`-based media in the system view **does**.
- **No engine blur / no CSS / no animated SVG (SMIL).** Pre-blur background art in the source file. Animation only via Lottie `.json`, `.gif`, or video.
- **License:** CC-BY-NC-SA; include the disclaimer "Logos and trademarks are the property of their respective owners." Only bundle ES-DE official assets (and OFL font); no other trademarked logos.

## Verification convention (every task)

Because ES-DE themes have no automated test harness, each task's "test" is:
1. **`xmllint --noout <each xml file touched>`** → exits 0 (well-formed).
2. **Install + load in ES-DE:** symlink or copy the theme dir into the ES-DE themes folder, launch ES-DE (or `Ctrl+R` to reload theme.xml; **restart** after editing `capabilities.xml`), select the theme/variant, and **confirm the specific named behavior** in the task. Debug aids: `Ctrl+I` highlights image/animation elements, `Ctrl+T` highlights text elements.
3. **Compare to the mockup** `docs/mockup/steam-mockup.html` for layout/hierarchy intent.
4. **Commit.**

Install location (user's ES-DE on external drive): `/Volumes/Untitled/ES-DE/themes/steam-bigpicture-es-de/` (or `~/ES-DE/themes/`). A one-time dev symlink is set up in Task 2.

**Spec reference:** `docs/superpowers/specs/2026-06-28-es-de-steam-big-picture-theme-design.md`. **Visual reference:** `docs/mockup/steam-mockup.html`.

---

## File structure (created across the plan)

```
steam-bigpicture-es-de/
  capabilities.xml                 # Task 14 (6 variants, colorScheme, aspect ratios, transitions)
  theme.xml                        # Task 2 (root; Task 14 expands to compose variants)
  _inc/
    colors.xml                     # Task 4 (dark colorScheme variables)
    fonts.xml                      # Task 3 (font path variables)
    helpsystem.xml                 # Task 7
    status.xml                     # Task 8 (systemstatus + clock)
    detail.xml                     # Task 9 (shared gamelist detail panel)
    system_hero_neon.xml           # Task 10
    system_nohero.xml              # Task 11
    system_hero_art.xml            # Task 12
    gamelist_grid.xml              # Task 13
    gamelist_list.xml              # Task 13b
  fonts/inter-regular.ttf, inter-semibold.ttf, inter-extrabold.ttf   # Task 3
  assets/icons/fallback.svg        # Task 6
  assets/ui/capsule-placeholder.svg, play.svg                        # Task 6 / 9
  system-logos/                    # Task 5 (git subtree)
  system-controllers-outline/      # Task 5 (git subtree)
  system-metadata/                 # Task 5 (git subtree)
  systems/art/                     # Task 12/17 (per-platform hero art; placeholders for now)
  systems/backgrounds/             # Task 17 (pre-blurred per-system bg; optional)
  LICENSE, README.md, ATTRIBUTION.md   # Task 1 / Task 18
```

---

### Task 1: Repository + license scaffold

**Files:**
- Create: `LICENSE`, `README.md`, `ATTRIBUTION.md`, `.gitignore`

- [ ] **Step 1: Init git (repo is not yet under version control)**

Run:
```bash
cd /Users/igorzamyslov/Projects/es-de-steam-theme
git init -b main
```

- [ ] **Step 2: Write `.gitignore`**

```
.DS_Store
*.swp
/scratch/
```

- [ ] **Step 3: Write `LICENSE`** — paste the full CC BY-NC-SA 4.0 legal text (from https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.txt), then append:

```
---
Logos and trademarks are the property of their respective owners.
System icons, logos and metadata are sourced from the ES-DE official asset
repositories (gitlab.com/es-de/themes) and remain under their respective terms.
The Inter font is licensed under the SIL Open Font License 1.1.
```

- [ ] **Step 4: Write `README.md`** (stub — expanded in Task 18)

```markdown
# Steam Big Picture for ES-DE

A theme for ES-DE (EmulationStation Desktop Edition) recreating the modern
Steam Big Picture / Steam Deck UI.

Status: in development. See `docs/superpowers/specs/` for the design and
`docs/superpowers/plans/` for the implementation plan.
```

- [ ] **Step 5: Write `ATTRIBUTION.md`**

```markdown
# Attribution

- System logos & icons: ES-DE official asset repos (gitlab.com/es-de/themes/system-logos, system-controllers-outline) — see their licenses.
- System metadata & colors: gitlab.com/es-de/themes/system-metadata (CC BY-NC-SA).
- Font: Inter by Rasmus Andersson (SIL OFL 1.1).
- Logos and trademarks are the property of their respective owners.
```

- [ ] **Step 6: Commit**

```bash
git add LICENSE README.md ATTRIBUTION.md .gitignore docs/
git commit -m "chore: scaffold repo, license, attribution, design docs"
```

---

### Task 2: Minimal loadable theme

Goal: the smallest theme ES-DE will load and navigate, so every later task has a working base to verify against.

**Files:**
- Create: `steam-bigpicture-es-de/capabilities.xml`
- Create: `steam-bigpicture-es-de/theme.xml`

**Interfaces:**
- Produces: a theme dir ES-DE lists as "Steam Big Picture", with a `system` and `gamelist` view that render (textlist primaries) and navigate.

- [ ] **Step 1: Write minimal `steam-bigpicture-es-de/capabilities.xml`**

```xml
<!-- Steam Big Picture for ES-DE -->
<themeCapabilities>
    <themeName>Steam Big Picture</themeName>
    <aspectRatio>16:9</aspectRatio>
    <colorScheme name="dark">
        <label language="en_US">Dark</label>
    </colorScheme>
</themeCapabilities>
```

- [ ] **Step 2: Write minimal `steam-bigpicture-es-de/theme.xml`**

```xml
<theme>
    <view name="system">
        <textlist name="systemList">
            <pos>0.05 0.1</pos>
            <size>0.9 0.8</size>
            <primaryColor>aab4c0ff</primaryColor>
            <selectedColor>ffffffff</selectedColor>
            <selectedBackgroundColor>3a9bffff</selectedBackgroundColor>
            <fontSize>0.045</fontSize>
        </textlist>
    </view>
    <view name="gamelist">
        <textlist name="gameList">
            <pos>0.05 0.1</pos>
            <size>0.9 0.8</size>
            <primaryColor>aab4c0ff</primaryColor>
            <selectedColor>ffffffff</selectedColor>
            <selectedBackgroundColor>3a9bffff</selectedBackgroundColor>
            <fontSize>0.045</fontSize>
        </textlist>
    </view>
</theme>
```

- [ ] **Step 3: Validate XML**

Run: `xmllint --noout steam-bigpicture-es-de/capabilities.xml steam-bigpicture-es-de/theme.xml`
Expected: no output, exit 0.

- [ ] **Step 4: Install via dev symlink + load in ES-DE**

Run:
```bash
ln -sfn "$(pwd)/steam-bigpicture-es-de" "/Volumes/Untitled/ES-DE/themes/steam-bigpicture-es-de"
```
Then launch ES-DE → UI Settings → Theme → select "Steam Big Picture".
Expected: theme loads with no error popup; system view shows a vertical list of system names; entering a system shows a list of games. (This is the throwaway baseline UI — later tasks replace it.)

- [ ] **Step 5: Commit**

```bash
git add steam-bigpicture-es-de/
git commit -m "feat: minimal loadable ES-DE theme (textlist baseline)"
```

---

### Task 3: Fonts

**Files:**
- Create: `steam-bigpicture-es-de/fonts/inter-regular.ttf`, `inter-semibold.ttf`, `inter-extrabold.ttf`
- Create: `steam-bigpicture-es-de/_inc/fonts.xml`
- Modify: `steam-bigpicture-es-de/theme.xml` (include fonts.xml; use the font)

**Interfaces:**
- Produces: variables `${fontRegular}`, `${fontSemiBold}`, `${fontExtraBold}` (paths to the TTFs).

- [ ] **Step 1: Download Inter TTFs into `fonts/`**

Run:
```bash
cd steam-bigpicture-es-de/fonts
curl -L -o inter.zip "https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip"
unzip -j inter.zip "*/Inter-Regular.ttf" "*/Inter-SemiBold.ttf" "*/Inter-ExtraBold.ttf"
mv Inter-Regular.ttf inter-regular.ttf
mv Inter-SemiBold.ttf inter-semibold.ttf
mv Inter-ExtraBold.ttf inter-extrabold.ttf
rm inter.zip
cd ../..
```
Expected: three lowercase `.ttf` files present (verify `ls steam-bigpicture-es-de/fonts`).

- [ ] **Step 2: Write `_inc/fonts.xml`**

```xml
<theme>
    <variables>
        <fontRegular>./fonts/inter-regular.ttf</fontRegular>
        <fontSemiBold>./fonts/inter-semibold.ttf</fontSemiBold>
        <fontExtraBold>./fonts/inter-extrabold.ttf</fontExtraBold>
    </variables>
</theme>
```

- [ ] **Step 3: Include fonts.xml and apply it in `theme.xml`** — add `<include>./_inc/fonts.xml</include>` as the first child of `<theme>`, and add `<fontPath>${fontSemiBold}</fontPath>` to both textlists.

- [ ] **Step 4: Validate + load**

Run: `xmllint --noout steam-bigpicture-es-de/_inc/fonts.xml steam-bigpicture-es-de/theme.xml`
In ES-DE: `Ctrl+R`. Expected: list text now renders in Inter (compare letterforms to a system-default font).

- [ ] **Step 5: Commit**

```bash
git add steam-bigpicture-es-de/fonts steam-bigpicture-es-de/_inc/fonts.xml steam-bigpicture-es-de/theme.xml
git commit -m "feat: bundle Inter font and wire font variables"
```

---

### Task 4: Color scheme variables

**Files:**
- Create: `steam-bigpicture-es-de/_inc/colors.xml`
- Modify: `steam-bigpicture-es-de/theme.xml` (include colors.xml; use variables)

**Interfaces:**
- Produces color variables: `${cBg1}`, `${cBg2}`, `${cPanel}`, `${cLine}`, `${cAccent}`, `${cText}`, `${cText2}`, `${cMuted}`, `${cStar}`, `${cGreen}` — all 8-digit `RRGGBBAA`.

- [ ] **Step 1: Write `_inc/colors.xml`**

```xml
<theme>
    <colorScheme name="dark">
        <variables>
            <cBg1>15181dff</cBg1>
            <cBg2>0b0e12ff</cBg2>
            <cPanel>191d23ff</cPanel>
            <cLine>2b313aff</cLine>
            <cAccent>3a9bffff</cAccent>
            <cText>e8edf2ff</cText>
            <cText2>aab4c0ff</cText2>
            <cMuted>6d7884ff</cMuted>
            <cStar>f5c518ff</cStar>
            <cGreen>7fb23bff</cGreen>
        </variables>
    </colorScheme>
</theme>
```

- [ ] **Step 2: Include and apply** — add `<include>./_inc/colors.xml</include>` to `theme.xml`; replace the hard-coded textlist colors with `${cText2}`, `${cText}`, `${cAccent}`.

- [ ] **Step 3: Validate + load**

Run: `xmllint --noout steam-bigpicture-es-de/_inc/colors.xml steam-bigpicture-es-de/theme.xml`
In ES-DE: `Ctrl+R`. Expected: selection highlight is the blue accent; unselected text is muted grey.

- [ ] **Step 4: Commit**

```bash
git add steam-bigpicture-es-de/_inc/colors.xml steam-bigpicture-es-de/theme.xml
git commit -m "feat: dark color scheme variables"
```

---

### Task 5: Official asset repos via git subtree

**Files:**
- Create (subtrees): `steam-bigpicture-es-de/system-controllers-outline/`, `system-logos/`, `system-metadata/`

**Interfaces:**
- Produces: per-system icon at `./system-controllers-outline/<system>.svg`, logo at `./system-logos/<system>.svg` (and `-white` variant), metadata at `./system-metadata/<system>/...`. Confirm the exact in-repo path layout after pulling (Step 2) and record it in a comment in `theme.xml`.

- [ ] **Step 1: Add subtrees**

Run:
```bash
cd /Users/igorzamyslov/Projects/es-de-steam-theme
git remote add es-controllers https://gitlab.com/es-de/themes/system-controllers-outline.git
git remote add es-logos https://gitlab.com/es-de/themes/system-logos.git
git remote add es-metadata https://gitlab.com/es-de/themes/system-metadata.git
git subtree add --prefix=steam-bigpicture-es-de/system-controllers-outline --squash es-controllers master
git subtree add --prefix=steam-bigpicture-es-de/system-logos --squash es-logos master
git subtree add --prefix=steam-bigpicture-es-de/system-metadata --squash es-metadata master
```
(If `master` is not the default branch, use `main`.)

- [ ] **Step 2: Record the actual path layout**

Run: `ls steam-bigpicture-es-de/system-controllers-outline | head; ls steam-bigpicture-es-de/system-logos | head`
Expected: per-system SVG files (e.g. `snes.svg`, `gc.svg`). Note the exact naming (whether `gc` vs `gamecube` etc. — this is the ES-DE `${system.theme}` value) and confirm a few of the user's systems exist: `gba`, `gbc`, `gc`, `megadrive`, `n64`, `nes`, `pico8`, `ps2`, `snes`, `wiiu`.

- [ ] **Step 3: Commit** (subtree add already commits; this records the layout note)

Add a comment to `theme.xml` documenting the confirmed icon path pattern, then:
```bash
git add steam-bigpicture-es-de/theme.xml
git commit -m "docs: record system asset path layout"
```

---

### Task 6: Fallback icon + UI assets

**Files:**
- Create: `steam-bigpicture-es-de/assets/icons/fallback.svg`
- Create: `steam-bigpicture-es-de/assets/ui/capsule-placeholder.svg`, `steam-bigpicture-es-de/assets/ui/play.svg`

- [ ] **Step 1: Write `assets/icons/fallback.svg`** (generic gamepad, white, centered on a 64×64 canvas so ES-DE can tint it)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <g fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
    <rect x="8" y="22" width="48" height="22" rx="11"/>
    <line x1="17" y1="33" x2="23" y2="33"/>
    <line x1="20" y1="30" x2="20" y2="36"/>
    <circle cx="42" cy="30" r="2.4" fill="#ffffff"/>
    <circle cx="47" cy="35" r="2.4" fill="#ffffff"/>
  </g>
</svg>
```

- [ ] **Step 2: Write `assets/ui/capsule-placeholder.svg`** (neutral 600×900 plate for missing covers)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 900">
  <rect width="600" height="900" fill="#202830"/>
  <rect x="1" y="1" width="598" height="898" fill="none" stroke="#ffffff14" stroke-width="2"/>
</svg>
```

- [ ] **Step 3: Write `assets/ui/play.svg`** (decorative play glyph for the detail panel — see note in Task 9; launching is via the A button)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M8 5.5v13l11-6.5z" fill="#102b06"/></svg>
```

- [ ] **Step 4: Validate + commit**

Run: `xmllint --noout steam-bigpicture-es-de/assets/icons/fallback.svg steam-bigpicture-es-de/assets/ui/*.svg`
```bash
git add steam-bigpicture-es-de/assets
git commit -m "feat: fallback icon and UI placeholder assets"
```

---

### Task 7: Help system module

**Files:**
- Create: `steam-bigpicture-es-de/_inc/helpsystem.xml`

**Interfaces:**
- Produces: a styled `helpsystem` to be included by every view module.

- [ ] **Step 1: Write `_inc/helpsystem.xml`**

```xml
<theme>
    <view name="system, gamelist">
        <helpsystem name="help">
            <pos>0.03 0.955</pos>
            <origin>0 0.5</origin>
            <textColor>aab4c0ff</textColor>
            <iconColor>aab4c0ff</iconColor>
            <textColorDimmed>6d7884ff</textColorDimmed>
            <iconColorDimmed>6d7884ff</iconColorDimmed>
            <fontPath>${fontSemiBold}</fontPath>
            <fontSize>0.028</fontSize>
            <entrySpacing>0.012</entrySpacing>
            <iconTextSpacing>0.006</iconTextSpacing>
            <letterCase>capitalize</letterCase>
        </helpsystem>
    </view>
</theme>
```

- [ ] **Step 2: Validate**

Run: `xmllint --noout steam-bigpicture-es-de/_inc/helpsystem.xml`
Expected: exit 0. (Visual verification happens once a module includes it, Task 10.)

- [ ] **Step 3: Commit**

```bash
git add steam-bigpicture-es-de/_inc/helpsystem.xml
git commit -m "feat: styled help system module"
```

---

### Task 8: Status overlay module (battery + clock)

**Files:**
- Create: `steam-bigpicture-es-de/_inc/status.xml`

**Interfaces:**
- Produces: a `systemstatus` (battery + wifi) and a `clock`, top-right, for inclusion by every view module.

- [ ] **Step 1: Write `_inc/status.xml`**

```xml
<theme>
    <view name="system, gamelist">
        <systemstatus name="status">
            <pos>0.978 0.028</pos>
            <origin>1 0.5</origin>
            <height>0.03</height>
            <color>aab4c0ff</color>
            <fontPath>${fontSemiBold}</fontPath>
            <entries>battery, wifi</entries>
        </systemstatus>
        <clock name="clock">
            <pos>0.905 0.028</pos>
            <origin>1 0.5</origin>
            <fontPath>${fontSemiBold}</fontPath>
            <fontSize>0.03</fontSize>
            <color>aab4c0ff</color>
            <format>%H:%M</format>
        </clock>
    </view>
</theme>
```

- [ ] **Step 2: Validate + commit**

Run: `xmllint --noout steam-bigpicture-es-de/_inc/status.xml`
```bash
git add steam-bigpicture-es-de/_inc/status.xml
git commit -m "feat: status overlay (battery + clock)"
```
Note: battery only renders on devices with a battery; verify visually in Task 10. (Dev tip: `SystemStatusDisplayAll=true` in `es_settings.xml` forces all indicators on for testing.)

---

### Task 9: Shared gamelist detail panel

**Files:**
- Create: `steam-bigpicture-es-de/_inc/detail.xml`

**Interfaces:**
- Produces: the right-hand detail panel (`<view name="gamelist">` fragment) included by both gamelist modules. Uses `${cText}`, `${cText2}`, `${cMuted}`, `${cStar}`, `${fontExtraBold}`, `${fontSemiBold}`.

**Note (engine reality):** ES-DE launches a game with the **A button**, not an on-screen button. The "Play" affordance is therefore a **decorative** styled element signalling the action; the real launch hint lives in the `helpsystem` (A = Launch). Keep it decorative.

- [ ] **Step 1: Write `_inc/detail.xml`** (panel occupies the right ~30% of the screen)

```xml
<theme>
    <view name="gamelist">
        <!-- panel background -->
        <image name="detailPanelBg">
            <pos>0.70 0</pos>
            <size>0.30 1</size>
            <path>./assets/ui/panel.svg</path>
            <zIndex>10</zIndex>
        </image>
        <!-- screenshot / fanart -->
        <image name="detailShot">
            <pos>0.72 0.06</pos>
            <maxSize>0.26 0.16</maxSize>
            <imageType>screenshot</imageType>
            <default>./assets/ui/capsule-placeholder.svg</default>
            <cornerRadius>0.01</cornerRadius>
            <zIndex>20</zIndex>
        </image>
        <!-- title -->
        <text name="detailTitle">
            <pos>0.72 0.24</pos>
            <size>0.26 0.10</size>
            <metadata>name</metadata>
            <container>false</container>
            <fontPath>${fontExtraBold}</fontPath>
            <fontSize>0.030</fontSize>
            <color>${cText}</color>
            <zIndex>20</zIndex>
        </text>
        <!-- rating (gold) -->
        <rating name="detailRating">
            <pos>0.72 0.35</pos>
            <size>0 0.025</size>
            <color>${cStar}</color>
            <hideIfZero>false</hideIfZero>
            <zIndex>20</zIndex>
        </rating>
        <!-- metadata block: genre / developer / players -->
        <text name="detailMetaKeys">
            <pos>0.72 0.40</pos>
            <size>0.07 0.16</size>
            <text>Genre&#10;Developer&#10;Players&#10;Released</text>
            <fontPath>${fontSemiBold}</fontPath>
            <fontSize>0.020</fontSize>
            <color>${cMuted}</color>
            <lineSpacing>1.7</lineSpacing>
            <zIndex>20</zIndex>
        </text>
        <text name="detailGenre">
            <pos>0.80 0.40</pos><size>0.18 0.04</size>
            <metadata>genre</metadata><fontPath>${fontSemiBold}</fontPath>
            <fontSize>0.020</fontSize><color>${cText2}</color><zIndex>20</zIndex>
        </text>
        <text name="detailDeveloper">
            <pos>0.80 0.434</pos><size>0.18 0.04</size>
            <metadata>developer</metadata><fontPath>${fontSemiBold}</fontPath>
            <fontSize>0.020</fontSize><color>${cText2}</color><zIndex>20</zIndex>
        </text>
        <text name="detailPlayers">
            <pos>0.80 0.468</pos><size>0.18 0.04</size>
            <metadata>players</metadata><fontPath>${fontSemiBold}</fontPath>
            <fontSize>0.020</fontSize><color>${cText2}</color><zIndex>20</zIndex>
        </text>
        <datetime name="detailReleased">
            <pos>0.80 0.502</pos><size>0.18 0.04</size>
            <metadata>releasedate</metadata><format>%Y</format>
            <fontPath>${fontSemiBold}</fontPath><fontSize>0.020</fontSize>
            <color>${cText2}</color><zIndex>20</zIndex>
        </datetime>
        <!-- description: the only scroll region -->
        <text name="detailDesc">
            <pos>0.72 0.56</pos>
            <size>0.26 0.30</size>
            <metadata>description</metadata>
            <container>true</container>
            <containerType>vertical</containerType>
            <fontPath>${fontRegular}</fontPath>
            <fontSize>0.020</fontSize>
            <color>${cText2}</color>
            <lineSpacing>1.5</lineSpacing>
            <zIndex>20</zIndex>
        </text>
        <!-- decorative Play affordance (launch is via A; see note) -->
        <image name="detailPlayBg">
            <pos>0.72 0.90</pos><size>0.26 0.06</size>
            <path>./assets/ui/play-button.svg</path><zIndex>20</zIndex>
        </image>
        <text name="detailPlayLabel">
            <pos>0.85 0.93</pos><origin>0.5 0.5</origin>
            <text>PLAY</text><fontPath>${fontExtraBold}</fontPath>
            <fontSize>0.022</fontSize><color>102b06ff</color>
            <horizontalAlignment>center</horizontalAlignment><zIndex>21</zIndex>
        </text>
    </view>
</theme>
```

- [ ] **Step 2: Create the two referenced SVGs** `assets/ui/panel.svg` (a `0.30×1`-proportioned dark gradient plate, e.g. 600×2000, fill `#12161c` with a 2px left border `#2b313a`) and `assets/ui/play-button.svg` (a rounded green pill, ~600×140, fill gradient `#a1cd44`→`#5f9626`, `rx=18`).

```xml
<!-- assets/ui/panel.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 2000"><rect width="600" height="2000" fill="#12161c"/><rect x="0" y="0" width="2" height="2000" fill="#2b313a"/></svg>
```
```xml
<!-- assets/ui/play-button.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 140"><rect width="600" height="140" rx="18" fill="#7fb23b"/></svg>
```

- [ ] **Step 3: Validate**

Run: `xmllint --noout steam-bigpicture-es-de/_inc/detail.xml steam-bigpicture-es-de/assets/ui/panel.svg steam-bigpicture-es-de/assets/ui/play-button.svg`
Expected: exit 0. (Visual verification in Task 13.)

- [ ] **Step 4: Commit**

```bash
git add steam-bigpicture-es-de/_inc/detail.xml steam-bigpicture-es-de/assets/ui
git commit -m "feat: shared gamelist detail panel"
```

---

### Task 10: System module — Hero · neon

**Files:**
- Create: `steam-bigpicture-es-de/_inc/system_hero_neon.xml`
- Modify: `steam-bigpicture-es-de/theme.xml` (temporarily include this module's system view to verify in isolation)

**Interfaces:**
- Consumes: `${fontExtraBold}`, `${fontSemiBold}`, colors, `${cAccent}`.
- Produces: a `system` view = bottom `carousel` rail of system icons + a large hero image (system logo, focus-tracked) + name/count text + included help/status.

- [ ] **Step 1: Write `_inc/system_hero_neon.xml`**

```xml
<theme>
    <include>./helpsystem.xml</include>
    <include>./status.xml</include>
    <view name="system">
        <!-- atmospheric background plate (per-system bg added in Task 17) -->
        <image name="heroBg">
            <pos>0 0</pos><size>1 1</size>
            <path>./assets/ui/hero-bg.svg</path>
            <zIndex>1</zIndex>
        </image>
        <!-- big focus-tracked system logo as the "neon" hero subject -->
        <image name="heroLogo">
            <pos>0.70 0.40</pos><origin>0.5 0.5</origin>
            <maxSize>0.44 0.46</maxSize>
            <path>./system-logos/${system.theme}.svg</path>
            <default>./assets/icons/fallback.svg</default>
            <color>e8edf2ff</color>
            <zIndex>5</zIndex>
        </image>
        <!-- left scrim for text legibility -->
        <image name="heroScrim">
            <pos>0 0</pos><size>0.62 1</size>
            <path>./assets/ui/scrim-left.svg</path>
            <zIndex>8</zIndex>
        </image>
        <!-- system name + count -->
        <text name="sysName">
            <pos>0.05 0.62</pos><size>0.55 0.12</size>
            <systemdata>fullname</systemdata>
            <fontPath>${fontExtraBold}</fontPath><fontSize>0.058</fontSize>
            <color>${cText}</color><zIndex>10</zIndex>
        </text>
        <text name="sysCount">
            <pos>0.05 0.74</pos><size>0.5 0.05</size>
            <systemdata>gamecount</systemdata>
            <fontPath>${fontSemiBold}</fontPath><fontSize>0.024</fontSize>
            <color>${cText2}</color><zIndex>10</zIndex>
        </text>
        <!-- bottom rail of system icons -->
        <carousel name="rail">
            <pos>0 0.80</pos><size>1 0.18</size>
            <type>horizontal</type>
            <staticImage>./system-controllers-outline/${system.theme}.svg</staticImage>
            <defaultImage>./assets/icons/fallback.svg</defaultImage>
            <maxItemCount>9</maxItemCount>
            <itemSize>0.085 0.13</itemSize>
            <itemScale>1.18</itemScale>
            <imageColor>aab4c0ff</imageColor>
            <imageSelectedColor>ffffffff</imageSelectedColor>
            <color>00000000</color>
            <text>${system.fullName}</text>
            <textColor>00000000</textColor>
            <zIndex>40</zIndex>
        </carousel>
    </view>
</theme>
```

- [ ] **Step 2: Create referenced SVGs** `assets/ui/hero-bg.svg` (1920×1080 dark vertical gradient `#15181d`→`#0b0e12` — per-system tint comes later) and `assets/ui/scrim-left.svg` (1200×1080, left-to-transparent black gradient).

```xml
<!-- assets/ui/hero-bg.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#15181d"/><stop offset="1" stop-color="#0b0e12"/></linearGradient></defs><rect width="1920" height="1080" fill="url(#g)"/></svg>
```
```xml
<!-- assets/ui/scrim-left.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1080"><defs><linearGradient id="s" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000000" stop-opacity="0.8"/><stop offset="1" stop-color="#000000" stop-opacity="0"/></linearGradient></defs><rect width="1200" height="1080" fill="url(#s)"/></svg>
```

- [ ] **Step 3: Temporarily wire it into `theme.xml`** — replace the system `<view>` block with `<include>./_inc/system_hero_neon.xml</include>` (keep the gamelist textlist for now).

- [ ] **Step 4: Validate + load**

Run: `xmllint --noout steam-bigpicture-es-de/_inc/system_hero_neon.xml steam-bigpicture-es-de/assets/ui/hero-bg.svg steam-bigpicture-es-de/assets/ui/scrim-left.svg steam-bigpicture-es-de/theme.xml`
In ES-DE: restart (new includes), open system view. Expected: a bottom rail of system icons; scrolling it updates the big hero logo + the system name/count; clock (and battery if present) top-right; help bar bottom-left. Unmapped systems show the fallback gamepad.

- [ ] **Step 5: Commit**

```bash
git add steam-bigpicture-es-de/_inc/system_hero_neon.xml steam-bigpicture-es-de/assets/ui steam-bigpicture-es-de/theme.xml
git commit -m "feat: system view module - hero (neon) + rail"
```

---

### Task 11: System module — No hero

**Files:**
- Create: `steam-bigpicture-es-de/_inc/system_nohero.xml`

**Interfaces:**
- Produces: a `system` view = full-screen `grid` of system icon tiles + a compact header (name + count) + help/status.

- [ ] **Step 1: Write `_inc/system_nohero.xml`**

```xml
<theme>
    <include>./helpsystem.xml</include>
    <include>./status.xml</include>
    <view name="system">
        <image name="bgPlate">
            <pos>0 0</pos><size>1 1</size>
            <path>./assets/ui/hero-bg.svg</path><zIndex>1</zIndex>
        </image>
        <text name="sgName">
            <pos>0.035 0.06</pos><size>0.6 0.07</size>
            <systemdata>fullname</systemdata>
            <fontPath>${fontExtraBold}</fontPath><fontSize>0.04</fontSize>
            <color>${cText}</color><zIndex>10</zIndex>
        </text>
        <text name="sgCount">
            <pos>0.035 0.115</pos><size>0.5 0.04</size>
            <systemdata>gamecount</systemdata>
            <fontPath>${fontSemiBold}</fontPath><fontSize>0.022</fontSize>
            <color>${cMuted}</color><zIndex>10</zIndex>
        </text>
        <grid name="sysGrid">
            <pos>0.035 0.17</pos><size>0.93 0.74</size>
            <staticImage>./system-controllers-outline/${system.theme}.svg</staticImage>
            <defaultImage>./assets/icons/fallback.svg</defaultImage>
            <itemSize>0.10 0.16</itemSize>
            <itemSpacing>0.012 0.018</itemSpacing>
            <itemScale>1.06</itemScale>
            <scaleInwards>true</scaleInwards>
            <imageColor>aab4c0ff</imageColor>
            <imageSelectedColor>ffffffff</imageSelectedColor>
            <backgroundColor>1a1f27ff</backgroundColor>
            <selectorColor>3a9bffff</selectorColor>
            <selectorLayer>bottom</selectorLayer>
            <text>${system.fullName}</text>
            <textColor>00000000</textColor>
            <zIndex>40</zIndex>
        </grid>
    </view>
</theme>
```

- [ ] **Step 2: Validate + load** (temporarily swap the system include in theme.xml to this module)

Run: `xmllint --noout steam-bigpicture-es-de/_inc/system_nohero.xml`
In ES-DE: restart. Expected: a multi-row grid of system tiles fills the screen, header top-left, focus highlight on the selected tile, no hero.

- [ ] **Step 3: Commit**

```bash
git add steam-bigpicture-es-de/_inc/system_nohero.xml
git commit -m "feat: system view module - no hero (tile grid)"
```

---

### Task 12: System module — Hero · art

**Files:**
- Create: `steam-bigpicture-es-de/_inc/system_hero_art.xml`
- Create: `steam-bigpicture-es-de/systems/art/.gitkeep`, `steam-bigpicture-es-de/assets/ui/art-placeholder.svg`

**Interfaces:**
- Produces: a `system` view identical to hero·neon except the hero subject is per-platform **art** (`./systems/art/${system.theme}.*`) with a placeholder default until bespoke art exists.

- [ ] **Step 1: Write `assets/ui/art-placeholder.svg`** (1280×720 dark plate with a dashed frame + "PLATFORM ART" label)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"><rect width="1280" height="720" fill="#141a21"/><rect x="40" y="40" width="1200" height="640" fill="none" stroke="#ffffff2e" stroke-width="3" stroke-dasharray="14 12"/><text x="640" y="368" fill="#8a97a6" font-family="sans-serif" font-size="34" letter-spacing="6" text-anchor="middle">PLATFORM ART</text></svg>
```

- [ ] **Step 2: Write `_inc/system_hero_art.xml`** — copy of `system_hero_neon.xml` (Step 1 of Task 10) with the `heroLogo` image replaced by:

```xml
        <image name="heroArt">
            <pos>0.70 0.40</pos><origin>0.5 0.5</origin>
            <maxSize>0.5 0.62</maxSize>
            <path>./systems/art/${system.theme}.jpg</path>
            <default>./assets/ui/art-placeholder.svg</default>
            <cornerRadius>0.012</cornerRadius>
            <zIndex>5</zIndex>
        </image>
```
(Keep the rail, scrim, name, count, help, status exactly as in the neon module.)

- [ ] **Step 3: Validate + load** (temporarily swap the system include)

Run: `xmllint --noout steam-bigpicture-es-de/_inc/system_hero_art.xml steam-bigpicture-es-de/assets/ui/art-placeholder.svg`
In ES-DE: restart. Expected: hero shows the dashed "PLATFORM ART" placeholder for systems without art; rail + name/count unchanged.

- [ ] **Step 4: Commit**

```bash
git add steam-bigpicture-es-de/_inc/system_hero_art.xml steam-bigpicture-es-de/systems steam-bigpicture-es-de/assets/ui/art-placeholder.svg
git commit -m "feat: system view module - hero (art) with placeholder"
```

---

### Task 13: Gamelist module — Grid

**Files:**
- Create: `steam-bigpicture-es-de/_inc/gamelist_grid.xml`

**Interfaces:**
- Produces: a `gamelist` view = header + capsule `grid` (left 70%) + included shared detail panel.

- [ ] **Step 1: Write `_inc/gamelist_grid.xml`**

```xml
<theme>
    <include>./helpsystem.xml</include>
    <include>./status.xml</include>
    <include>./detail.xml</include>
    <view name="gamelist">
        <text name="glHeader">
            <pos>0.035 0.05</pos><size>0.6 0.06</size>
            <metadata>systemFullname</metadata>
            <fontPath>${fontExtraBold}</fontPath><fontSize>0.036</fontSize>
            <color>${cText}</color><zIndex>20</zIndex>
        </text>
        <gamelistinfo name="glCount">
            <pos>0.035 0.11</pos><size>0.3 0.03</size>
            <fontPath>${fontSemiBold}</fontPath><fontSize>0.02</fontSize>
            <color>${cMuted}</color><zIndex>20</zIndex>
        </gamelistinfo>
        <grid name="capsules">
            <pos>0.035 0.16</pos><size>0.64 0.80</size>
            <imageType>cover</imageType>
            <defaultImage>./assets/ui/capsule-placeholder.svg</defaultImage>
            <itemSize>0.10 0.22</itemSize>
            <itemSpacing>0.014 0.02</itemSpacing>
            <itemScale>1.06</itemScale>
            <scaleInwards>true</scaleInwards>
            <imageFit>contain</imageFit>
            <imageCornerRadius>0.006</imageCornerRadius>
            <selectorColor>3a9bffff</selectorColor>
            <selectorLayer>bottom</selectorLayer>
            <zIndex>30</zIndex>
        </grid>
    </view>
</theme>
```

- [ ] **Step 2: Validate + load** (temporarily set the gamelist `<view>` in theme.xml to `<include>./_inc/gamelist_grid.xml</include>`)

Run: `xmllint --noout steam-bigpicture-es-de/_inc/gamelist_grid.xml`
In ES-DE: `Ctrl+R`, enter a populated system (e.g. `gba`). Expected: 2:3 capsule grid; selected capsule highlighted (no edge clipping); right panel shows the selected game's shot/title/rating/genre/developer/players/description; long descriptions scroll; covers of odd ratios letterbox cleanly; missing covers show the placeholder.

- [ ] **Step 3: Commit**

```bash
git add steam-bigpicture-es-de/_inc/gamelist_grid.xml steam-bigpicture-es-de/theme.xml
git commit -m "feat: gamelist module - capsule grid + detail"
```

---

### Task 13b: Gamelist module — List

**Files:**
- Create: `steam-bigpicture-es-de/_inc/gamelist_list.xml`

**Interfaces:**
- Produces: a `gamelist` view = header + `textlist` of game names (left 70%) + included shared detail panel.

- [ ] **Step 1: Write `_inc/gamelist_list.xml`**

```xml
<theme>
    <include>./helpsystem.xml</include>
    <include>./status.xml</include>
    <include>./detail.xml</include>
    <view name="gamelist">
        <text name="glHeader">
            <pos>0.035 0.05</pos><size>0.6 0.06</size>
            <metadata>systemFullname</metadata>
            <fontPath>${fontExtraBold}</fontPath><fontSize>0.036</fontSize>
            <color>${cText}</color><zIndex>20</zIndex>
        </text>
        <gamelistinfo name="glCount">
            <pos>0.035 0.11</pos><size>0.3 0.03</size>
            <fontPath>${fontSemiBold}</fontPath><fontSize>0.02</fontSize>
            <color>${cMuted}</color><zIndex>20</zIndex>
        </gamelistinfo>
        <textlist name="gameList">
            <pos>0.035 0.16</pos><size>0.64 0.80</size>
            <primaryColor>aab4c0ff</primaryColor>
            <selectedColor>ffffffff</selectedColor>
            <selectedBackgroundColor>1b222cff</selectedBackgroundColor>
            <selectedSecondaryBackgroundColor>1b222cff</selectedSecondaryBackgroundColor>
            <selectorVerticalOffset>0</selectorVerticalOffset>
            <fontPath>${fontSemiBold}</fontPath>
            <fontSize>0.032</fontSize>
            <horizontalMargin>0.012</horizontalMargin>
            <lineSpacing>1.6</lineSpacing>
            <indicators>symbols</indicators>
            <zIndex>30</zIndex>
        </textlist>
    </view>
</theme>
```

- [ ] **Step 2: Validate + load** (temporarily swap the gamelist include to this module)

Run: `xmllint --noout steam-bigpicture-es-de/_inc/gamelist_list.xml`
In ES-DE: `Ctrl+R`. Expected: a vertical list of game names; selected row highlighted; the same detail panel updates on the right; favorites/collection indicators show as symbols.

- [ ] **Step 3: Commit**

```bash
git add steam-bigpicture-es-de/_inc/gamelist_list.xml
git commit -m "feat: gamelist module - list + detail"
```

---

### Task 14: capabilities.xml — 6 variants + theme.xml composition

**Files:**
- Modify: `steam-bigpicture-es-de/capabilities.xml`
- Modify: `steam-bigpicture-es-de/theme.xml` (replace the temporary single-view body with full variant composition)

**Interfaces:**
- Consumes: all six `_inc/system_*` and `_inc/gamelist_*` modules.
- Produces: 6 selectable variants.

- [ ] **Step 1: Rewrite `capabilities.xml`**

```xml
<!-- Steam Big Picture for ES-DE -->
<themeCapabilities>
    <themeName>Steam Big Picture</themeName>

    <aspectRatio>16:9</aspectRatio>
    <aspectRatio>16:10</aspectRatio>
    <aspectRatio>4:3</aspectRatio>

    <colorScheme name="dark">
        <label language="en_US">Dark</label>
    </colorScheme>

    <transitions name="steam">
        <label language="en_US">Steam</label>
        <selectable>true</selectable>
        <systemToSystem>instant</systemToSystem>
        <systemToGamelist>slide</systemToGamelist>
        <gamelistToGamelist>instant</gamelistToGamelist>
        <gamelistToSystem>slide</gamelistToSystem>
        <startupToSystem>fade</startupToSystem>
        <startupToGamelist>fade</startupToGamelist>
    </transitions>

    <variant name="heroNeonGrid"><label language="en_US">Hero (neon) · Grid</label><selectable>true</selectable></variant>
    <variant name="heroNeonList"><label language="en_US">Hero (neon) · List</label><selectable>true</selectable></variant>
    <variant name="heroArtGrid"><label language="en_US">Hero (art) · Grid</label><selectable>true</selectable></variant>
    <variant name="heroArtList"><label language="en_US">Hero (art) · List</label><selectable>true</selectable></variant>
    <variant name="noHeroGrid"><label language="en_US">No hero · Grid</label><selectable>true</selectable></variant>
    <variant name="noHeroList"><label language="en_US">No hero · List</label><selectable>true</selectable></variant>
</themeCapabilities>
```

- [ ] **Step 2: Rewrite `theme.xml`** to compose every variant from modules

```xml
<theme>
    <include>./_inc/fonts.xml</include>
    <include>./_inc/colors.xml</include>

    <variant name="heroNeonGrid">
        <include>./_inc/system_hero_neon.xml</include>
        <include>./_inc/gamelist_grid.xml</include>
    </variant>
    <variant name="heroNeonList">
        <include>./_inc/system_hero_neon.xml</include>
        <include>./_inc/gamelist_list.xml</include>
    </variant>
    <variant name="heroArtGrid">
        <include>./_inc/system_hero_art.xml</include>
        <include>./_inc/gamelist_grid.xml</include>
    </variant>
    <variant name="heroArtList">
        <include>./_inc/system_hero_art.xml</include>
        <include>./_inc/gamelist_list.xml</include>
    </variant>
    <variant name="noHeroGrid">
        <include>./_inc/system_nohero.xml</include>
        <include>./_inc/gamelist_grid.xml</include>
    </variant>
    <variant name="noHeroList">
        <include>./_inc/system_nohero.xml</include>
        <include>./_inc/gamelist_list.xml</include>
    </variant>
</theme>
```

- [ ] **Step 3: Validate + load**

Run: `xmllint --noout steam-bigpicture-es-de/capabilities.xml steam-bigpicture-es-de/theme.xml`
In ES-DE: **restart** (capabilities changed). UI Settings → Theme variant: confirm all 6 entries appear and each renders its system+gamelist correctly (spot-check `Hero (neon) · Grid`, `No hero · List`, `Hero (art) · Grid`).

- [ ] **Step 4: Commit**

```bash
git add steam-bigpicture-es-de/capabilities.xml steam-bigpicture-es-de/theme.xml
git commit -m "feat: 6 variants composed from layout modules"
```

---

### Task 15: Aspect-ratio adjustments (16:10, 4:3)

**Files:**
- Create: `steam-bigpicture-es-de/_inc/aspect_16_10.xml`, `steam-bigpicture-es-de/_inc/aspect_4_3.xml`
- Modify: `steam-bigpicture-es-de/theme.xml` (add `<aspectRatio>` blocks)

**Interfaces:**
- Produces: per-aspect overrides of element `pos`/`size` so the layout reflows (4:3 = fewer grid columns / taller rail / repositioned hero).

- [ ] **Step 1: Write `_inc/aspect_4_3.xml`** — override the elements that need it for narrow screens. Example (grid columns via larger `itemSize`, hero text repositioned):

```xml
<theme>
    <view name="gamelist">
        <grid name="capsules"><pos>0.04 0.17</pos><size>0.62 0.78</size><itemSize>0.13 0.27</itemSize></grid>
        <textlist name="gameList"><pos>0.04 0.17</pos><size>0.62 0.78</size></textlist>
    </view>
    <view name="system">
        <text name="sysName"><pos>0.05 0.58</pos><fontSize>0.05</fontSize></text>
        <text name="sysCount"><pos>0.05 0.70</pos></text>
        <carousel name="rail"><pos>0 0.78</pos><size>1 0.20</size><maxItemCount>6</maxItemCount></carousel>
    </view>
</theme>
```

- [ ] **Step 2: Write `_inc/aspect_16_10.xml`** — smaller deltas off the 16:9 baseline:

```xml
<theme>
    <view name="system">
        <carousel name="rail"><pos>0 0.80</pos><size>1 0.18</size><maxItemCount>8</maxItemCount></carousel>
    </view>
</theme>
```

- [ ] **Step 3: Add to `theme.xml`** (inside `<theme>`, after the variant blocks)

```xml
    <aspectRatio name="4:3">
        <include>./_inc/aspect_4_3.xml</include>
    </aspectRatio>
    <aspectRatio name="16:10">
        <include>./_inc/aspect_16_10.xml</include>
    </aspectRatio>
```

- [ ] **Step 4: Validate + load**

Run: `xmllint --noout steam-bigpicture-es-de/_inc/aspect_4_3.xml steam-bigpicture-es-de/_inc/aspect_16_10.xml steam-bigpicture-es-de/theme.xml`
In ES-DE: set the application resolution / test on a 4:3 and 16:10 window if possible. Expected: at 4:3 the grid uses fewer/larger capsules and the hero text doesn't collide with the rail; at 16:10 the rail shows ~8 tiles.

- [ ] **Step 5: Commit**

```bash
git add steam-bigpicture-es-de/_inc/aspect_4_3.xml steam-bigpicture-es-de/_inc/aspect_16_10.xml steam-bigpicture-es-de/theme.xml
git commit -m "feat: 16:10 and 4:3 aspect-ratio adjustments"
```

---

### Task 16: Per-system mood / hero tint

**Files:**
- Create: `steam-bigpicture-es-de/_inc/systems/<system>.xml` (one tiny file per system defining its mood color), e.g. `gc.xml`, `snes.xml`, … for the user's systems + common ones
- Create: `steam-bigpicture-es-de/_inc/mood_default.xml`
- Modify: the hero modules to load a per-system color via `${system.theme}` include and use it for `heroBg` tint / `heroLogo` glow color

**Interfaces:**
- Consumes: `system-metadata/<system>/` color palettes (read the value, map to one of the 8 moods).
- Produces: variable `${cHero}` per system, consumed by the hero background/logo tint.

- [ ] **Step 1: Define the 8 mood colors in `_inc/mood_default.xml`**

```xml
<theme>
    <variables>
        <cHero>1b2330ff</cHero>          <!-- slate default -->
        <cHeroRim>3a9bffff</cHeroRim>
    </variables>
</theme>
```

- [ ] **Step 2: Per-system overrides** — for each system, a file like `_inc/systems/gc.xml`:

```xml
<theme>
    <variables>
        <cHero>2a1d3aff</cHero>          <!-- royal -->
        <cHeroRim>b06cffff</cHeroRim>
    </variables>
</theme>
```
Map each system to a mood by reading `system-metadata/<system>/` (or the spec's mood assignments): slate, ocean, teal, toxic, royal, crimson, ember, gold. Create one file per system you want themed; unmapped systems fall back to `mood_default.xml`.

- [ ] **Step 3: Load per-system mood in the hero modules** — in `system_hero_neon.xml` and `system_hero_art.xml`, before the views, add:

```xml
    <include>./mood_default.xml</include>
    <include>./systems/${system.theme}.xml</include>
```
(An include with a variable-populated missing path only logs a debug entry, so unmapped systems silently keep the default.) Then change `heroBg` to a tinted plate driven by `${cHero}` — replace the static `heroBg` image with a colored `image` using `<color>${cHero}</color>` over a neutral gradient texture, and set the `heroLogo` `<color>` glow toward `${cHeroRim}` where desired.

- [ ] **Step 4: Validate + load**

Run: `xmllint --noout` on `mood_default.xml`, every `_inc/systems/*.xml`, and the two hero modules.
In ES-DE: restart, scroll the rail across several systems. Expected: each themed system shows a distinct mood tint; unmapped systems show the slate default without errors.

- [ ] **Step 5: Commit**

```bash
git add steam-bigpicture-es-de/_inc/mood_default.xml steam-bigpicture-es-de/_inc/systems steam-bigpicture-es-de/_inc/system_hero_neon.xml steam-bigpicture-es-de/_inc/system_hero_art.xml
git commit -m "feat: per-system mood tint for the hero"
```

---

### Task 17: Hero-art production pipeline (deferred art) + docs

**Files:**
- Create: `docs/hero-art-pipeline.md`
- Create: `steam-bigpicture-es-de/systems/art/README.md`

- [ ] **Step 1: Write `docs/hero-art-pipeline.md`** documenting the chosen approach for producing the per-platform Dead Cells posters:

```markdown
# Hero art production

Target: one atmospheric "poster" per system at `systems/art/<system>.jpg` (1280×720,
pre-darkened on the left for text legibility; pre-blurred if used as background).

Recommended path — AI generation with a locked style spec:
1. Pick the style direction once (warm torchlight vs cool fog, complementary,
   neo-pixel-art, saturated midtones, atmospheric depth — describe, don't say
   "Dead Cells").
2. Generate 5–8 anchor images; lock a style reference + weight for all systems.
3. Generate per system; keep the mood palette (8 moods) consistent; expect
   ~15–20% regeneration for drift.
4. Confirm the generator's output license permits CC-BY-NC-SA redistribution.

Until posters exist, the `Hero (art)` variant shows the dashed placeholder.
```

- [ ] **Step 2: Write `systems/art/README.md`** explaining the filename convention (`<system>.jpg` matching the ES-DE `${system.theme}` value) and that missing files fall back to the placeholder.

- [ ] **Step 3: Commit**

```bash
git add docs/hero-art-pipeline.md steam-bigpicture-es-de/systems/art/README.md
git commit -m "docs: hero-art production pipeline"
```

---

### Task 18: Final polish, README, full verification

**Files:**
- Modify: `README.md`
- Verify: all variants × aspect ratios

- [ ] **Step 1: Expand `README.md`** with: what the theme is, ES-DE version requirement, install instructions (theme downloader vs manual into `~/ES-DE/themes/`), the 6 variants and how to switch (UI Settings → Theme variant), enabling auto-collections for Library/Favorites/Recent, the attribution/disclaimer, and a screenshot per variant.

- [ ] **Step 2: Full verification matrix in ES-DE**

For each of the 6 variants, at 16:9 (and spot-check 16:10, 4:3): confirm system view + gamelist view render with no error popup, the rail/grid navigates, the hero/detail tracks selection, long strings (an 80+ char game name, a 1000+ char description) don't break layout, missing covers/art show placeholders, and the help/status/clock render. Record results in the commit message.

- [ ] **Step 3: Validate every XML file**

Run: `find steam-bigpicture-es-de -name '*.xml' -exec xmllint --noout {} +`
Expected: exit 0.

- [ ] **Step 4: Commit**

```bash
git add README.md steam-bigpicture-es-de
git commit -m "docs: README + final verification pass"
```

---

## Self-review (completed)

- **Spec coverage:** §3 engine constraints → Global Constraints + Task 14; §4a variants → Tasks 10–14; §5 system view (hero/no-hero) → Tasks 10–12, 16; §6 gamelist grid+list+detail → Tasks 9, 13, 13b; §7 palette/fonts/focus → Tasks 3, 4; §8 art direction/production → Tasks 12, 17; §9 icons/assets (official repos) → Tasks 5, 6; §10 capabilities → Task 14; §11 structure → file-structure map; §13 aspect ratios → Task 15; §14 status/clock → Task 8; §15 licensing → Task 1; §16 scope (v1) → all tasks; §17 risks → called out in Tasks 10/16 verification. Covered.
- **Placeholder scan:** no "TBD/handle errors/similar to Task N" — each module's XML is written in full. The only deliberately deferred artifact is the bespoke hero *art* (Task 12 ships a real placeholder; Task 17 documents production), which is an explicit spec scope decision, not a plan gap.
- **Type/name consistency:** variable names (`${cText}`, `${cAccent}`, `${fontExtraBold}`, `${cHero}`), element `name`s, and module filenames are consistent across tasks; `theme.xml` variant names match `capabilities.xml` exactly.

> ⚠️ **Execution reality:** exact `pos`/`size`/`fontSize`/`maxItemCount` values are first-pass and **will be tuned in-engine** during each task's verification step (the only way to get pixel-accuracy without a running ES-DE). Treat the numbers as a correct starting point to adjust against the mockup, not final.

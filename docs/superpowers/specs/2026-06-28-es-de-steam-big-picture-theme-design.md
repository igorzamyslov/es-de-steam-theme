# ES-DE "Steam Big Picture" Theme — Design Spec

**Date:** 2026-06-28
**Status:** Approved design, ready for implementation planning
**Visual reference:** [`docs/mockup/steam-mockup.html`](../../mockup/steam-mockup.html) (open in a browser; the dark strip at the very top is mockup-only chrome with switchers for View / System variant / Game variant, not part of the theme)

---

## 1. Overview & goal

A theme for **ES-DE (EmulationStation Desktop Edition)** that recreates the look and feel of **modern Steam Big Picture / Steam Deck UI**, adapted to ES-DE's two-view model. Platforms are presented as the top-level navigation (the way Steam presents Library/collections), and games are presented as a Steam-style poster grid.

The theme is **Big-Picture-faithful in its chrome** (navigation, tiles, typography, focus, help bar) and **Big-Picture-*inspired* in its hero art layer**, which uses an atmospheric, stylized "poster" treatment referencing the visual language of *Dead Cells* (moody, rim-lit, saturated midtones). This mirrors how Big Picture itself pairs clean chrome with lush full-bleed key art.

## 2. Targets & constraints

- **Engine:** ES-DE modern theme engine (introduced 2.0.0; legacy unsupported since 2.2.0). Target latest stable (3.4.x).
- **Reference resolution:** **16:9 @ 1920×1080** — all spacing and font sizes tuned to land cleanly here. `fontSize` is a fraction of screen height (e.g. `0.045` ≈ 49px at 1080p).
- **Aspect ratios:** 16:9 (primary), 16:10 (Steam Deck, 1280×800), 4:3 (graceful). Others degrade acceptably.
- **Input:** controller-first (Big Picture is a controller UI). All actions reachable via the help bar; no mouse-only affordances.
- **Devices:** desktop and handhelds (incl. Steam Deck). Battery/Wi-Fi status shown where the device has it.

## 3. ES-DE engine model & hard constraints

These shaped every design decision; implementation must respect them:

1. **Two views only:** `system` (pick a system) and `gamelist` (its games). They are separate screens with a transition between them — there is **no persistent interactive top-nav across both**. (There is also an `all` view, used only for navigation-sound definitions.)
2. **Exactly one primary element per view** — a `carousel`, `grid`, or `textlist` — plus unlimited secondary elements (`image`, `video`, `text`, `badges`, `rating`, `datetime`, `gamelistinfo`, `animation`), and special elements (`gameselector`, `helpsystem`, `clock`, `systemstatus`).
3. **A carousel/grid item shows an image XOR text, never both.** Per-item "icon + caption" is impossible; item text only appears as a fallback when no image exists. (Labels can, however, be baked *into* a `staticImage` SVG.)
4. **The system view is rendered per system.** System variables (`${system.theme}`, `${system.name}`, `${system.fullName}`) resolve to the **currently focused** system, so a large secondary `image` keyed to `${system.theme}` naturally shows the focused system's art and swaps as the carousel scrolls. (You cannot make a secondary element show a *non-focused* carousel item.)
5. **Auto-collections** ("All Games", "Favorites", "Last Played") are real, cross-platform systems that appear in the same single system carousel as platforms. They are distinguished via the `system.*.autoCollections` / `.customCollections` / `.noCollections` variable suffixes and `letterCaseAutoCollections`. The theme **cannot reorder systems or force collections first** — that is a user/ES-DE setting. **ES-DE hides systems that have zero games by default.**
6. **Game media in the system view requires a `gameselector`** (for `imageType`-based images/video/text/rating/datetime). A plain `<path>` image (e.g. a per-system logo/art file) does **not** need a gameselector.
7. **No blur filter in-engine** — any blurred background art must be pre-blurred in the source file. **No CSS / animated-SVG (SMIL)**; animation is via Lottie `.json` or `.gif`/video (`<animation>` / `<video>`). Static images: SVG, PNG, JPG, WebP, unanimated GIF.
8. **`capabilities.xml` is mandatory** at the theme root and is only re-read on full restart (not `Ctrl+R`). Linux filesystems are case-sensitive — use lowercase filenames.

## 4. Information architecture & navigation

- **System view = the landing screen.** A horizontal **rail (carousel) of system tiles** along the bottom; a large **hero "poster"** of the focused system fills the upper area. Auto-collections (Library = All Games, Favorites, Recent = Last Played) appear in the rail alongside platforms. There is **no separate "Home"** — the system view *is* home.
- **Gamelist view = the Steam library grid.** A `grid` of vertical 2:3 poster capsules + a right-hand **detail panel** (screenshot, title, metadata, description, Play).
- **Transitions:** smooth slide/fade (`systemToGamelist` = slide, etc.) so moving between the two screens reads as connected, like switching Steam tabs.
- **Collections are functional and cross-platform** natively — no theme work beyond styling; the user enables auto-collections in ES-DE settings.

## 4a. Variants (user-selectable "theme mods")

The theme offers user-selectable layout options via ES-DE **variants**. ES-DE exposes a **single variant selector** (not independent per-view dropdowns), so the two independent axes are enumerated as the **cartesian product (6 variants)**, each composed from shared layout modules via `<include>` (3 system modules + 2 gamelist modules → no real duplication):

- **System-view axis (3):**
  - `Hero · neon` — hero poster with a glowing rim-lit system icon + bottom rail (default).
  - `Hero · art` — same hero+rail, but the hero shows per-platform art (bespoke art deferred; falls back to a tinted logo placeholder for now).
  - `No hero` — no hero; the system selector becomes a full-screen **multi-row grid of system tiles** (fast to scan, everything visible), with a compact header (focused name + count).
- **Gamelist-view axis (2):**
  - `Grid` — vertical 2:3 capsule grid + detail panel (default).
  - `List` — a vertical `textlist` of game names (with year + favorite marker) + the same detail panel.

The 6 variant names: `Hero (neon) · Grid`, `Hero (neon) · List`, `Hero (art) · Grid`, `Hero (art) · List`, `No hero · Grid`, `No hero · List`. Default = `Hero (neon) · Grid`. All are demonstrated in the mockup (top-bar switchers).

## 5. System view design

The system view has three variant layouts (§4a). The two **hero** variants share the layout below; the **No hero** variant replaces the hero with a system-tile grid.

**Hero layout (16:9 reference):** hero ≈ upper 65–74%, rail ≈ 150px band at the bottom, help bar at the very bottom. A floating status overlay (battery + clock) sits top-right and costs no layout height.

**Hero (per-system poster):**
- Full-bleed atmospheric background keyed to the system's **mood** (see §7), with a soft vignette and a single light grain layer.
- A large **rim-lit silhouette/art of the system**, composed off-balance (bleeding off the top/right edge), with a directional rim-light glow and a soft spotlight behind it. In v1 this is the system's art/logo; ideally bespoke per-platform poster art (see §8).
- A **left/bottom scrim** behind the text block guarantees legibility over any art.
- Text block (bottom-left): kind label (Collection/Platform), full system name, game count, and a "Last played" line for collections. Empty systems render a **dimmed** hero with a graceful "No games yet" message (rare in practice — ES-DE hides empty systems).

**Rail (system selector):**
- Tiles show a **consistent monochrome system icon** + a short name label. Focus = accent outline + soft glow + scale (Deck-style; **not** white-fill).
- A **position indicator** ("7 / 16") sits just above the rail.
- **LB/RB pages the rail** (jumps by a screenful) — the right primitive for vendor-prefixed system names where alphabetical letter-jump collapses (many systems start with "Nintendo"/"Sega").

**No-hero layout:** the primary `carousel`/`grid` of system tiles fills the screen (multi-row wrap), with a small header (`text` systemdata `fullname` + `gamecount`). No hero image; no separate rail.

**ES-DE element mapping:**
| Piece | Element |
|---|---|
| Rail / system-grid | horizontal `carousel` (rail) or `grid` (no-hero) of system tiles, `staticImage` = `./systems/icons/${system.theme}.svg` with `defaultImage` fallback; `maxItemCount`/`itemScale` (rail) for sizing/selection |
| Tile label | the carousel/grid item label is its `text` (fallback) — OR bake the short name into the icon SVG. Decide during implementation; baked-label keeps icon+name together |
| Hero art | secondary `image`, `path` = `./systems/art/${system.theme}.*` (or logo), with `<default>` fallback; tracks focused system automatically |
| Blurred background | secondary full-bleed `image` (pre-blurred source), low `zIndex` |
| System name / count | `text` with `systemdata` = `fullname` / `gamecount` |
| Status (battery/clock) | `systemstatus` (entries: `battery`, `wifi`, optionally `bluetooth`) + `clock` |
| Controller hints | `helpsystem` |

## 6. Gamelist view design

The gamelist view has two variant layouts (§4a): **Grid** (default) and **List**. Both share the right-hand detail panel.

### 6a. Grid layout

- **Primary:** `grid` of vertical **2:3 capsules**, `imageType="cover"` (with `3dbox`/`miximage` as alternates to evaluate). **Hybrid art:** `imageFit="contain"` so non-2:3 covers letterbox cleanly; `defaultImage` = a styled placeholder for missing covers. Set **`scaleInwards="true"`** so the selected item's scale/glow is not clipped at grid edges.
- **Selected capsule:** accent outline + glow + scale.
- **Header:** system name + game count (`gamelistinfo`) + sort indicator. No redundant breadcrumb.
- **Detail panel (right, fixed width):** in this vertical order — screenshot/video (`image`/`video`, `screenshot`/`fanart`); title (`text` metadata `name`, wraps/balances for the 80+ char real-world cases); badges (`rating` in gold, players, year — `badges`/`rating`/`datetime`/`text`); **metadata block** (genre, developer, platform, players — `text` metadata; genre is a wrapping line, not a pill, because real genres run 70+ chars); **description** (`text` metadata `description`, the **only** scroll region, via `container` scrolling); **Play button pinned at the bottom, always visible** regardless of description length.
- **Long-string handling** (validated against the user's real library — names to 81 chars, genres to 72, descriptions to 1655, counts to 1094): titles clamp/wrap, genre wraps in the metadata block, description scrolls, Play stays pinned, capsule titles clamp to 3 lines.

### 6b. List layout

- **Primary:** `textlist` of game names (left ~⅔ width). Each row shows the game name (truncates with ellipsis on the 80+ char cases), with a year and a favorite marker. Selected row uses the accent left-bar + subtle fill (faithful to Steam/Deck list rows).
- **Detail panel:** the same right-hand panel as Grid (screenshot/metadata/description/pinned Play).
- **Why offer it:** lists scan faster for large libraries (1094 games) and for users who prefer names over cover art; `textlist` is a first-class ES-DE primary element.

## 7. Visual system

- **Palette (chrome):** neutral charcoal — `--bg` ≈ `#15181d`/`#0b0e12`, panels `#191d23`, lines `#2b313a`, text `#e8edf2`/`#aab4c0`/muted `#6d7884`. **Blue (`#3a9bff`) is reserved for focus/interactive only.** Rating stars are gold (`#f5c518`), distinct from the focus accent. Play action is green (faithful to the Deck game page).
- **Typography:** Steam's *Motiva Sans* if shippable; otherwise **Inter** (OFL) as the substitute, embedded as TTF/OTF (ES-DE doesn't support SVG fonts). Type scale tuned at 1080p.
- **Focus language (everywhere):** dark element + accent outline + soft glow + slight scale. Never invert-to-white.
- **Hero "mood" palette:** instead of a free per-system hue (which collides at scale), a curated set of ~8 moods (slate, ocean, teal, toxic, royal, crimson, ember, gold), each defining a background hue/saturation and a rim-light hue. Each system is assigned a mood. **Source of truth:** ES-DE's `system-metadata` per-system color palettes (map them onto the mood set).

## 8. Art direction — Dead Cells hero posters

**Direction:** *Dead Cells* is vibrant (saturated midtones), not grimdark — warm torchlight vs. cool fog, complementary lighting, atmospheric depth, bioluminescent accents, neo-pixel-art rather than "8-bit."

**Discipline rules (consistency across ~80–100 posters):**
- Every poster = **[curated mood gradient] + [single rim-lit focal silhouette, off-balance] + [shared grain @≈4% + shared soft vignette]**.
- **No global scanlines** (they read as a cheap CRT filter and clash thematically — reserve for Arcade only, if at all). Grain felt, not seen. Embers/particles are **per-platform opt-in**, never in the shared template. Rim light is **directional**, not a symmetric halo. Focal art should be a **filled, lit mass**, not a scaled-up line icon.
- Constrain to the **mood palette**, not free hue, for both consistency and per-poster text-contrast control.

**Production plan (realistic for a hobby theme):**
- **Recommended:** AI image generation with a **locked style spec** — run a style tuner once, generate 5–8 anchor images, lock a style reference + weight on every generation; budget ~15–20% regeneration for drift. ~$30/mo tool + ~20–35h for ~80 posters. Prefer descriptive keywords (warm/cool lighting, complementary, neo-pixel-art, atmospheric) over the literal phrase "Dead Cells style." Verify output-licensing of the chosen tool.
- **Hybrid alternative:** procedurally render an atmospheric base layer offline → static PNG/WebP, with a per-system focal logo/silhouette on top.
- v1 can ship with the **mood-gradient + tinted system logo** treatment (no bespoke paintings) and add bespoke posters incrementally.

## 9. Icons & assets

- **System rail icons:** ES-DE's official **`system-controllers-outline`** (consistent silhouette per system, full coverage) and/or **`system-logos`** (color + white; the white variant is built for color-shifting/tinting via `imageColor`).
- **Per-system colors:** ES-DE official **`system-metadata`** (color palettes → mood mapping).
- **Workflow:** add the official repos as **git subtrees** (the documented ES-DE approach); files ship inside the theme. A custom-drawn **generic fallback** glyph covers any unmapped system.
- **Source repos:** `gitlab.com/es-de/themes/system-logos`, `…/system-controllers-outline`, `…/system-metadata`, `…/system-graphics-mini`.

## 10. capabilities.xml plan

- `<themeName>`: "Steam Big Picture".
- **colorSchemes:** `dark` (primary). Structure ready for a `light` later. (Steam is dark; v1 = dark only.)
- **aspectRatios:** `16:9`, `16:10`, `4:3` (+ verticals later if needed).
- **transitions:** a profile with `systemToGamelist`/`gamelistToSystem` = slide, `systemToSystem`/`gamelistToGamelist` = instant or slide; startup = fade.
- **variants (6):** the cartesian product of {Hero·neon, Hero·art, No-hero} × {Grid, List} (see §4a), each composed via `<include>` of one system module + one gamelist module. Default `Hero (neon) · Grid`. Optionally add a `noMedia` override variant so art-less libraries still look intentional.

## 11. File / directory structure

```
es-de-steam-theme/                 (theme dir; ES-DE expects a name ending in -es-de → likely "steam-ui")
  capabilities.xml
  theme.xml                        # root; includes the rest, defines variants/colorSchemes/aspectRatios
  _inc/
    colors.xml                     # colorScheme variables (dark)
    fonts.xml                      # Inter (or Motiva Sans)
    helpsystem.xml
    status.xml                     # systemstatus (battery/wifi) + clock
    detail.xml                     # shared gamelist detail panel
    system_hero_neon.xml           # system module: hero (neon icon) + rail
    system_hero_art.xml            # system module: hero (per-platform art) + rail
    system_nohero.xml              # system module: full-screen system tile grid
    gamelist_grid.xml              # gamelist module: capsule grid
    gamelist_list.xml              # gamelist module: textlist
    # theme.xml composes the 6 variants by including one system_* + one gamelist_*
  systems/
    icons/                         # from system-controllers-outline (subtree) + fallback
    art/                           # per-system hero posters (or generated/tinted logos)
    backgrounds/                   # pre-blurred per-system backgrounds
    metadata/                      # from system-metadata (subtree) → colors
  fonts/
  assets/                          # capsule placeholder, gradients, ui glyphs
  LICENSE                          # CC-BY-NC-SA + logo/trademark disclaimer
```

## 12. Theming details / behaviors

- **Hybrid covers:** `imageFit="contain"` + styled `defaultImage`.
- **Edge clipping:** grid `scaleInwards="true"`.
- **Jump speed:** LB/RB page the rail; position indicator for orientation; rely on ES-DE's own system order.
- **Empty systems:** dimmed hero state (mostly moot — ES-DE hides zero-game systems; relevant for empty custom collections).
- **SVG crispness:** SVGs stay sharp at any size (`interpolation`/`mipmap` are no-ops for SVG); icons tinted uniformly via `imageColor`.

## 13. Resolution & aspect-ratio handling

- Author at **1080p 16:9**. Provide `aspectRatio` blocks for **16:10** (Deck) and **4:3** that adjust hero/rail/grid proportions (e.g. fewer grid columns, taller rail) off the 16:9 baseline. Normalized coordinates handle pure scaling; the aspect blocks handle reflow.

## 14. Status & clock

- `systemstatus` element (battery with charge/capacity icons + percentage; Wi-Fi; Bluetooth) + `clock` (`%H:%M`), styled as a quiet top-right overlay. Shows only on devices that have the hardware; absent on a batteryless desktop.

## 15. Licensing

- Theme released under **CC-BY-NC-SA** (the ES-DE/EmulationStation community norm). Include the standard disclaimer: *"Logos and trademarks are the property of their respective owners."* Non-commercial. If AI-generated hero art is used, confirm the generator's output license permits redistribution under these terms.

## 16. Scope

**v1:**
- `capabilities.xml` (dark colorScheme; 16:9 + 16:10 + 4:3; the **6 variants** of §4a).
- System modules: `Hero · neon` (mood gradient + tinted system logo/icon + scrim + status), `Hero · art` (art slot; tinted-logo placeholder until bespoke art exists), `No hero` (system tile grid). Bottom icon rail uses official controller-outline icons; help bar.
- Gamelist modules: `Grid` (hybrid capsule grid) and `List` (textlist), both with the shared detail panel (metadata → scrolling description → pinned Play).
- Auto-collections styled as first-class system entries.
- Official asset repos wired in via subtree; generic fallback icon.

**Deferred:**
- Bespoke per-platform Dead Cells poster art (the `Hero · art` variant ships with a tinted-logo placeholder; add posters incrementally).
- Light colorScheme; further variants (video-forward, compact); 21:9 / vertical aspect ratios.
- Per-platform opt-in atmospheric extras (embers/scanlines for Arcade, etc.).

## 17. Risks / to verify in-engine

- **Hero-follows-focus** via `${system.theme}` secondary image — standard pattern (bundled Modern/Slate themes do it), but confirm on the target version.
- **Carousel as a small bottom rail** with `maxItemCount`/`itemScale` — confirmed feasible per docs; tune visual feel in-engine.
- **`systemstatus`** rendering/positioning on desktop vs handheld.
- **Baked-label vs separate-label** for rail tiles (icon SVG with baked short name, vs carousel text) — prototype both.
- **`capabilities.xml`** only reloads on restart — factor into the dev loop.

## 18. Verification approach

- No automated theme tests exist for ES-DE; verification is **manual in ES-DE** across 16:9 / 16:10 / 4:3, with a real (partially-populated) library to exercise long strings, missing art, and empty/large systems.
- The **HTML mockup** (`docs/mockup/steam-mockup.html`) is the approved visual reference for layout, hierarchy, palette, focus, and behavior — implementation should match it, then be tuned in-engine.

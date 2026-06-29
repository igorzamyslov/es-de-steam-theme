# Handheld review response — design

Date: 2026-06-29

Response to two external reviews of the **Steam Big Picture for ES-DE** theme: a
"prospective handheld user" presentation review (README / device claims / first-run
experience) and a theme-files code review (art fallbacks, empty states, accent wiring,
transitions). This spec captures the agreed scope, the resolved design forks, and the
explicit non-goals.

## Constraints / environment notes

- **No ES-DE renderer and no image generator/rasterizer are available in this
  workspace.** Verification is limited to XML well-formedness, asset-reference checks,
  and markdown lint (the repo's existing pre-commit hooks). Anything whose payoff is
  *visual* — the per-system accent, the new aspect ratios, the detail-media fallback —
  must be confirmed by the user in a real ES-DE install. The implementation plan will
  list exactly what to eyeball.
- Theme variables are resolved **globally and in declaration order** across the whole
  parsed theme set (this is why `${systemName}`, defined in the system-hero module,
  already resolves in the gamelist). The per-system accent rework relies on this and on
  fixing declaration order.

## Resolved design forks (decided with the user)

1. **Aspect ratios:** add `3:2` and `5:3` (common budget-handheld landscape ratios);
   stay honest that `1:1` and portrait are not supported.
2. **Detail media default:** keep **Marquee → Video** as the default scheme. Address the
   "logo on black" emptiness via a *still fallback chain*, not a default change.
3. **Accent:** **per-system** — the active section-strip underline tracks
   `${systemColor}` instead of a hardcoded hex.
4. **Transitions:** `systemToSystem` `instant` → `slide`; gamelist stays `instant`.
5. **Hero art:** I cannot paint the raster pack here. Ship a **generation kit** (locked
   style spec + per-system prompt manifest + post-process recipe) and keep the README
   honest. No vector stand-in.

## Changes

### A. Render art on real libraries (highest leverage)

- `_inc/gamelist_grid.xml`: `<imageType>cover</imageType>` →
  `<imageType>cover, miximage, screenshot, marquee</imageType>`. This is the real fix
  for the "wall of game-name text" in screenshot 02. **Correction to the review:** the
  grid has no per-tile platform badge to suppress — the repeated text *was* the no-art
  fallback; the fallback chain is what fixes it.
- `theme.xml` color schemes: make the detail-panel *still* fall back instead of jumping
  straight to the placeholder, while preserving the chosen marquee-first default:
  - `marqueeVideo` / `marqueeStill`: `detailMediaType` = `marquee, screenshot, cover`
  - `screenshotVideo` / `screenshotStill`: `detailMediaType` = `screenshot, cover`
  - `detail.xml` / `detail_wide.xml` keep `<imageType>${detailMediaType}</imageType>` and
    the existing `capsule-placeholder.svg` as the final `defaultImage`.

### B. Stop looking unfinished on thin libraries

- `_inc/detail.xml` and `_inc/detail_wide.xml`: `<hideIfZero>false</hideIfZero>` →
  `true` on `detailRating` (no row of empty stars on unrated games).
- `_inc/colors.xml`: bump `cMuted` `6d7884ff` → `8a94a0ff` (a notch lighter for sunlit
  handheld legibility). `cText2` stays `aab4c0ff`.
- **Known limitation (documented, not hacked):** ES-DE has no clean per-element
  "hide if the metadata value is empty," so the Genre/Developer/Players/Released/
  Description *key labels* still render on unscraped games. Add a short code comment in
  `detail.xml` noting this; no behavioral change.

### C. Per-system accent

- **Include reorder** in both `_inc/system_hero_neon.xml` and `_inc/system_hero_art.xml`
  so `${systemColor}` is defined before the section-strip consumes it. New order:
  `helpsystem`, `status`, `system-metadata/_default`, `system-metadata/${system.theme}`,
  `name-overrides/${system.theme}`, `section-accent/${system.theme}`,
  `spec-overrides/_default`, `spec-overrides/${system.theme}`,
  `section-state/_default`, `section-state/${system.theme}`, `section-strip`.
  (Preserves every existing "_default before override" relationship; only moves the
  metadata/accent group ahead of the section-state group.)
- `_inc/section-state/_default.xml` and the three `auto-*.xml`: replace each literal
  `3a9bffff` active-underline value with `${systemColor}`. The inactive underlines stay
  `00000000`. Result: a console's active "Platforms" underline = its platform color;
  Library/Favorites/Recent = their collection colors (already defined in
  `section-accent/`).
- `_inc/colors.xml`: **remove** `cAccent`. It is now genuinely superseded by
  `${systemColor}` (this resolves the "dead variable" *and* the "magic hex duplicated
  across files" complaints — the literal disappears from the section-state files rather
  than being re-pointed at another centralized constant).
- **Selector frame stays neutral white** (`selector-frame.svg` is already `#d6dee6`, not
  blue as the review claimed). A bright neutral focus ring is more Steam-accurate than a
  colored one, so it is intentionally *not* tinted per-system. The **Play button stays
  green** — Steam's Play is always green, not the accent.
- Unknown systems with no metadata fall back to the metadata `_default` `systemColor`
  (`333333`, dim). Accepted: the bundled system-metadata has full coverage, so this only
  affects genuinely unrecognized systems.

### D. Aspect ratios (add 3:2, 5:3)

- `capabilities.xml`: add `<aspectRatio>3:2</aspectRatio>` and `<aspectRatio>5:3</aspectRatio>`.
- `_inc/gamelist_grid.xml`: add `3:2, 5:3` to the
  `<aspectRatio name="16:9, 16:10, 4:3, 5:4, 19.5:9, 20:9, 21:9">` group (this also pulls
  in `detail.xml` for them).
- `_inc/scale.xml`: add `gridItemX` rows for `3:2` and `5:3` at all three font sizes,
  using the established `itemX = itemY · (2/3) / (W:H)` formula:
  - `3:2` (W/H 1.5): medium `0.1067`, large `0.1049`, x-large `0.1587`
  - `5:3` (W/H 1.667): medium `0.0960`, large `0.0944`, x-large `0.1428`
  - (exact values recomputed from the per-size `gridItemY` during implementation)
- The list variant needs no aspect entry (it is aspect-independent).

### E. Transitions

- `capabilities.xml` `transitions name="steam"`: `systemToSystem` `instant` → `slide`;
  leave `gamelistToGamelist` `instant`.

### F. README + presentation honesty

- Make **enabling automatic collections the first install step**, not a mid-page note
  (fixes the "3 of 4 nav tabs dead on a fresh install" impression).
- Rewrite Requirements / Aspect ratios:
  - "ES-DE only — runs on Steam Deck, desktop, and the distros that bundle ES-DE."
  - Steam Deck (`16:10`) + Windows handhelds (`16:9`) first-class; `4:3`/`5:4`,
    `3:2`/`5:3`, and phone `19.5:9`/`20:9`/`21:9` supported; `1:1` and portrait not yet.
  - Version caveat: tested on 3.4.x; below 3.x expect rough edges.
- Add a small-screen tip near Install: on a 5" handheld, set **Theme font size** to
  Large/X-Large for legibility.
- Replace the "neon-cyan accent" line with a description of the **per-platform** accent.
- Screenshots: move the hero-art shot (`04`) below the settings shot and recaption it
  "example after you add your own art (see Adding hero art)."
- Theme-downloader submission is an external maintainer process; document it as a
  recommended next step, not a code change.

### G. Hero-art generation kit

Turns "BYO art, good luck" into "run these exact prompts and drop the files in."

- `docs/hero-art-style-spec.md`: the locked master style — canvas `1280×720`, the
  pixel-art-poster look matching the existing `gba.jpg`, the 8-mood palette, left-side
  darkening for text legibility, and a reusable style-reference prompt block. Supersedes
  the thin guidance currently in `hero-art-pipeline.md` (which links to it).
- `scripts/gen-hero-art-prompts.py`: reads every `system-metadata/*.xml`, extracts
  `systemName`, `systemManufacturer`, `systemReleaseYear`, `systemHardwareType`,
  `systemColor`, and `systemColorPalette1..4`, and expands a prompt template per system.
  Emits a manifest. Skips non-system files (`_default`, `_labels`, `README`, `Fix.py`).
- `docs/hero-art/prompts.tsv` (generated, committed): one row per system —
  `system  prompt  primary_color  palette` — ready to batch through any image model.
- Post-process recipe in the style spec: crop/cover to `1280×720`, left-darken, export
  to `steam-bigpicture-es-de/systems/art/<system>.jpg`.

## Non-goals

- Painting the raster hero-art pack (no image model here).
- Any vector hero-art stand-in (clashes with `gba.jpg`; overlaps the neon hero).
- A `1:1` or portrait layout (different layout problem, out of scope).
- Submitting the theme to the ES-DE downloader (external maintainer process).
- Tinting the selector frame or Play button per-system (intentionally neutral/green).

## Verification

- Automated (available here): `pre-commit run --all-files` — xmllint well-formedness,
  the asset-reference checker, markdownlint, link check. The new Python script must lint
  clean and run against the real metadata tree.
- Manual (user, in ES-DE — the implementation plan will spell these out): grid renders
  capsules on a screenshot/marquee-only library; detail panel is populated for a
  marquee-less game; unrated game shows no star row; active tab underline shows the
  platform/collection color; `3:2` and `5:3` devices pack a sane column count; system →
  system slide feels right.

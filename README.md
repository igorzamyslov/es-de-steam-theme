# Steam Big Picture for ES-DE

A theme for [ES-DE](https://es-de.org/) (EmulationStation Desktop Edition) that recreates the modern Steam Big Picture / Steam Deck UI. The system view presents a bottom rail of platform icons over a full-bleed hero area; the gamelist shows a capsule grid (or a list) with a detail panel on the right. The palette is dark throughout — Steam's characteristic navy with a neon-cyan accent.

It adapts to your display and settings: a per-font-size type-and-density scale, a desktop side-panel layout for `16:9 / 16:10 / 4:3 / 5:4`, and a full-width hero-banner layout for phone/ultrawide (`19.5:9 / 20:9 / 21:9`). Four variants (hero style × gamelist layout) combine with four color-scheme media modes.

---

## Requirements

- **ES-DE 2.0 or later** (developed and tested against the 3.4.x series).
- `xmllint` is not required to run the theme; it is only used during development for XML validation.

---

## Install

1. Download or clone this repository.
2. Copy (or symlink) the `steam-bigpicture-es-de/` directory into your ES-DE themes folder:
   - **Linux / macOS:** `~/ES-DE/themes/`
   - **Windows:** `%USERPROFILE%\ES-DE\themes\`
   - If you customized the ES-DE data directory, look for `<your data path>/themes/`.
3. Launch ES-DE, open **UI Settings → Theme**, and select **Steam Big Picture**.

> **Note:** This theme is not listed in the ES-DE theme downloader. Manual installation is required.

> **Recommended:** For the full Steam-like experience, **enable automatic collections** (see [Collections](#collections-library-favorites-recent) below). They power the persistent **Library / Favorites / Recent** nav tabs at the top of every screen — without them, those tabs have nothing to show.

---

## Variants

Switch variants under **UI Settings → Theme variant**. There are **4 variants** — every combination of two independent choices. The default is **Hero (neon) · Grid**.

- **System view:** `Hero (neon)` (gradient hero + focus-tracked system logo) · `Hero (art)` (per-platform background art — placeholder until you add art, see below)
- **Gamelist:** `Grid` (capsule grid + right detail panel) · `List` (scrollable list + wider detail panel)

| Variant | System hero | Gamelist |
| --- | --- | --- |
| Hero (neon) · Grid *(default)* | neon | grid |
| Hero (neon) · List | neon | list |
| Hero (art) · Grid | art | grid |
| Hero (art) · List | art | list |

---

## Detail media (color schemes)

The **color scheme** axis is repurposed to pick how the detail panel presents a game's media. Switch it under **UI Settings → Theme color scheme** (all four share the one dark palette). The default is **Marquee → Video**.

| Color scheme | Behavior |
| --- | --- |
| **Marquee → Video** *(default)* | marquee still shows first, then the game's video auto-plays |
| **Screenshot → Video** | screenshot still shows first, then the video auto-plays |
| **Marquee (no video)** | marquee still only — no video playback |
| **Screenshot (no video)** | screenshot still only — no video playback |

If the chosen still or the video isn't scraped for a game, the panel falls back to a placeholder.

---

## Theme font size

The theme scales its typography **and** grid density to the **UI Settings → Theme font size** setting:

- **Medium** — most capsules per screen (densest grid), compact type.
- **Large** — fewer, larger capsules; a wider detail panel with a bigger video.
- **X-Large** — largest capsules and type, for couch/TV viewing distance.

Pick whichever suits your screen size and viewing distance.

---

## Aspect ratios

The layout reflows automatically by aspect ratio:

- **Desktop / TV** (`16:9`, `16:10`, `4:3`, `5:4`): grid (or list) on the left, detail panel on the right.
- **Phone / ultrawide** (`19.5:9`, `20:9`, `21:9`): a full-width hero banner across the top of the gamelist with the focused game's title and compact metadata, and the grid below.

---

## Collections (Library, Favorites, Recent)

This theme is built around a persistent **Library / Favorites / Recent / Platforms** nav strip across the top of every screen — the Steam-style spine of the UI. The first three are ES-DE *automatic collections*, so **enabling them is strongly recommended for the best experience**. Without them, those tabs lead to empty systems.

Enable them in ES-DE under:

**Game Collection Settings → Enable automatic game collections**

Once enabled, ES-DE aggregates games across all platforms and surfaces them as virtual systems, and the Library / Favorites / Recent tabs come to life.

---

## Adding hero art

The "Hero (art)" variants show a placeholder hero area until you add per-platform background art. To produce and install your own:

- See **`docs/hero-art-pipeline.md`** for the production workflow (canvas size, naming convention, export settings).
- See **`steam-bigpicture-es-de/systems/art/README.md`** for where to place the files so the theme picks them up.

---

## Screenshots

### System view — Library collection (hero · neon)
![Library system view with the persistent Library / Favorites / Recent / Platforms nav strip](screenshots/01-system-library.png)

### Gamelist — capsule grid with detail panel
![Capsule grid gamelist with a right-hand detail panel](screenshots/02-gamelist-grid.png)

### Gamelist — list with wide detail panel
![List gamelist with a wide detail panel](screenshots/03-gamelist-list.png)

### System view — per-platform hero art
![Game Boy Advance system view with per-platform hero art](screenshots/04-system-hero-art.png)

### Theme settings (variant · color scheme · font size)
![ES-DE theme settings showing the variant, color-scheme media modes, and font-size options](screenshots/05-settings.png)

---

## Credits & License

This theme is released under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** license. See `LICENSE` for the full text.

Asset sources:

- **System logos & icons:** ES-DE official asset repositories (`gitlab.com/es-de/themes/system-logos`, `system-controllers-outline`) — see their individual licenses.
- **System metadata & colors:** `gitlab.com/es-de/themes/system-metadata` (CC BY-NC-SA).
- **Fonts:** Inter by Rasmus Andersson and Rubik (display face) — both under the SIL Open Font License 1.1.
- Logos and trademarks used in system icons and metadata are the property of their respective owners.

See `ATTRIBUTION.md` for a full attribution list.

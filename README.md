# Steam Big Picture for ES-DE

A theme for [ES-DE](https://es-de.org/) (EmulationStation Desktop Edition) that recreates the modern Steam Big Picture / Steam Deck UI. The system view presents a bottom rail of platform icons alongside a full-bleed hero area; the gamelist shows a capsule grid or list with a detail panel on the right. The color scheme is dark throughout, using Steam's characteristic navy and neon-cyan accent palette. Six layout variants let you mix hero styles with grid or list gamelists. Aspect ratios 16:9, 16:10, and 4:3 are all supported.

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

---

## Variants

Switch variants under **UI Settings → Theme variant**. Six variants are available:

| Variant | Hero style | Gamelist layout |
|---|---|---|
| Hero (neon) · Grid | Neon-gradient hero with system icon | Capsule grid |
| Hero (neon) · List | Neon-gradient hero with system icon | Scrollable list |
| Hero (art) · Grid | Placeholder hero area (per-platform art — see below) | Capsule grid |
| Hero (art) · List | Placeholder hero area (per-platform art — see below) | Scrollable list |
| No hero · Grid | No hero, full icon grid | Capsule grid |
| No hero · List | No hero, full icon grid | Scrollable list |

---

## Collections (Library, Favorites, Recent)

To get the **Library**, **Favorites**, and **Recent** entries in the system view rail, enable automatic collections in ES-DE:

**Game Collection Settings → Enable automatic game collections**

Once enabled, ES-DE aggregates games across all platforms and surfaces them as virtual systems in the rail.

---

## Adding hero art

The "Hero (art)" variants ship with a placeholder hero area. Per-platform background art is a planned addition. To produce and install your own hero art:

- See **`docs/hero-art-pipeline.md`** for the production workflow (canvas size, naming convention, export settings).
- See **`steam-bigpicture-es-de/systems/art/README.md`** for where to place the files so the theme picks them up.

---

## Screenshots

Screenshots for each variant will be added once the theme is verified in-engine. Check back after the first release.

---

## Credits & License

This theme is released under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** license. See `LICENSE` for the full text.

Asset sources:

- **System logos & icons:** ES-DE official asset repositories (`gitlab.com/es-de/themes/system-logos`, `system-controllers-outline`) — see their individual licenses.
- **System metadata & colors:** `gitlab.com/es-de/themes/system-metadata` (CC BY-NC-SA).
- **Font:** Inter by Rasmus Andersson (SIL Open Font License 1.1).
- Logos and trademarks used in system icons and metadata are the property of their respective owners.

See `ATTRIBUTION.md` for a full attribution list.

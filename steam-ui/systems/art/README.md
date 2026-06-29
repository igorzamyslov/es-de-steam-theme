# Hero art file naming

## Filename format

Name each image `<system>.jpg` where `<system>` matches the ES-DE `${system.theme}` value. Examples:

- `gc.jpg` — GameCube
- `snes.jpg` — Super Nintendo
- `nes.jpg` — Nintendo Entertainment System
- `ps1.jpg` — PlayStation 1

Images must be 1280×720 px, pre-darkened on the left for text legibility, and optionally pre-blurred if used as a background.

## Fallback behavior

If a system's image is missing, the variant falls back to `assets/ui/art-placeholder.svg` — the UI stays functional until all per-system images are added.

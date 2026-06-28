# Hero art file naming convention

## Filename format

Each hero art image follows the naming convention: `<system>.jpg`

where `<system>` matches the ES-DE `${system.theme}` value. For example:
- `gc.jpg` for GameCube
- `snes.jpg` for Super Nintendo
- `nes.jpg` for Nintendo Entertainment System
- `ps1.jpg` for PlayStation 1

Images must be 1280×720 pixels, pre-darkened on the left for text legibility, and optionally pre-blurred if used as a background.

## Fallback behavior

If a hero art image for a system is missing, the variant falls back to the dashed placeholder:
`assets/ui/art-placeholder.svg`

This ensures the UI remains functional and visually consistent until all per-system hero art images are produced.

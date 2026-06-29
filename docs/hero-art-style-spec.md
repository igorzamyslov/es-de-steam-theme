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

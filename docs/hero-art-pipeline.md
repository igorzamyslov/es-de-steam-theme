# Hero art production

> The locked look, palette, and post-process live in **[hero-art-style-spec.md](hero-art-style-spec.md)**.
> Per-system prompts are generated into `docs/hero-art/prompts.tsv` by
> `scripts/gen-hero-art-prompts.py` — run it, then batch the rows through your image model.

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

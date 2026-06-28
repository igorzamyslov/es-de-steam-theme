# Responsive Scaling (font size + portrait grid) — Design

**Goal:** Make the theme readable and well-proportioned on small/wide screens (phones, esp. landscape ~19.5:9 / 20:9), via (a) a single user-selectable size that scales all text **and** the grid together, and (b) a fix so grid tiles stay portrait on any aspect ratio. Plus a minor shadow-softening tweak.

**Architecture:** Centralize all sizing in one new include `_inc/scale.xml`, which defines theme variables per ES-DE `<fontSize>` selection and per `<aspectRatio>`. Element files stop hardcoding sizes and reference variables. `capabilities.xml` declares the font-size options and the extra aspect ratios so ES-DE exposes them and matches the device.

**Tech stack:** ES-DE modern theme engine. Mechanisms: `<fontSize>` capability + variables (UI Settings → *Theme font size*); `<aspectRatio>` variables (auto-matched to display); `<fontSize>` nested inside `<aspectRatio>` for the grid matrix. Variables are string substitution, so a whole `itemSize` pair can live in one variable.

## Global Constraints
- Medium = exact current values (no visual change at the default).
- ES-DE resolves variables in declaration order; `scale.xml` must be included **before** the element files that consume its variables, and root `<variables>` must not redeclare these names (root wins and would block per-size/per-aspect overrides).
- ES-DE `<fontSize>` valid names: `medium, large, x-large` (we use these three). Valid horizontal aspect names used: `16:9, 16:10, 4:3, 5:4, 19.5:9, 20:9, 21:9`.
- Positions stay fixed (existing spacing has slack for x-large); the plan must verify no overlap at x-large on load.

## A. Type scale (text)

One variable per role; medium = current value. large ≈ ×1.2, x-large ≈ ×1.4, except `fsHero` (already large) which is capped to avoid overflow.

| Variable | Role / elements | medium | large | x-large |
| --- | --- | --- | --- | --- |
| `fsHero` | system name (sysName) | 0.052 | 0.058 | 0.064 |
| `fsHeader` | gamelist header (glHeader, grid+list) | 0.032 | 0.038 | 0.044 |
| `fsList` | textlist game rows | 0.030 | 0.036 | 0.042 |
| `fsClock` | clock | 0.030 | 0.034 | 0.038 |
| `fsTitleWide` | list detail title | 0.028 | 0.033 | 0.038 |
| `fsTitle` | grid detail title | 0.026 | 0.031 | 0.036 |
| `fsCount` | system game count (sysCount) | 0.022 | 0.026 | 0.030 |
| `fsButton` | Play label | 0.021 | 0.025 | 0.028 |
| `fsLabel` | manufacturer (sysFull), help | 0.020 | 0.024 | 0.027 |
| `fsMetaWide` | list detail metadata + desc | 0.019 | 0.023 | 0.026 |
| `fsMeta` | grid detail metadata + desc | 0.0185 | 0.022 | 0.025 |
| `fsTab` | section tabs, glCount, grid text-fallback | 0.018 | 0.022 | 0.025 |

## B. Grid sizing (portrait + scale)

Keep tiles ~**2:3 portrait** on every aspect: `itemX = itemY × (2/3) / (W:H ratio)`. `itemY` and spacing scale with the size setting; `itemX` also depends on aspect.

- `gridItemY` (per size): medium **0.20**, large **0.235**, x-large **0.27**
- `gridSpacing` (per size): medium **0.010 0.014**, large **0.012 0.017**, x-large **0.014 0.020**
- `gridItemX` per (aspect group × size), from the formula:

| Aspect group (ratio) | medium (itemY .20) | large (.235) | x-large (.27) |
| --- | --- | --- | --- |
| 4:3 / 5:4 (~1.333) | 0.100 | 0.117 | 0.135 |
| 16:10 (1.6) | 0.083 | 0.098 | 0.113 |
| 16:9 (1.778) | 0.075 | 0.088 | 0.101 |
| 19.5:9 / 20:9 / 21:9 (~2.22) | 0.060 | 0.071 | 0.081 |

Grid consumes: `<itemSize>${gridItemX} ${gridItemY}</itemSize>`, `<itemSpacing>${gridSpacing}</itemSpacing>`. (This also de-squares 16:9, where tiles were ~0.86, to true 2:3.)

## C. Shadow softening

`capsule-shadow-soft.svg`: add 1–2 intermediate stops to the soft halo for a smoother ramp at small (phone) tile sizes, and ease the crisp band from `0.32` → ~`0.26`. Geometry unchanged.

## capabilities.xml changes
- Add: `<fontSize>medium</fontSize>`, `<fontSize>large</fontSize>`, `<fontSize>x-large</fontSize>`.
- Add aspect ratios: `19.5:9`, `20:9`, `21:9` (keep `16:9`, `16:10`, `4:3`; add `5:4` grouping is optional).

## File changes
- **New** `_inc/scale.xml`: all `<fontSize>` and `<aspectRatio>` variable blocks (type scale + grid matrix). Included from `theme.xml` **before** the variant includes.
- `theme.xml`: add `<include>./_inc/scale.xml</include>` early; ensure none of these variable names are declared in the root `<variables>` block (root wins over includes and would block per-size/per-aspect overrides).
- `_inc/gamelist_grid.xml`: itemSize/itemSpacing → variables; text fontSize → `${fsTab}`; header → `${fsHeader}`.
- `_inc/gamelist_list.xml`: textlist → `${fsList}`; header → `${fsHeader}`; count → `${fsTab}`.
- `_inc/system_hero_neon.xml` / `_inc/system_hero_art.xml`: sysName → `${fsHero}`, sysFull → `${fsLabel}`, sysCount → `${fsCount}`.
- `_inc/detail.xml`: title → `${fsTitle}`, metadata/desc → `${fsMeta}`, Play → `${fsButton}`.
- `_inc/detail_wide.xml`: title → `${fsTitleWide}`, metadata/desc → `${fsMetaWide}`, Play → `${fsButton}`.
- `_inc/section-strip.xml`: tabs → `${fsTab}`.
- `_inc/helpsystem.xml`: help → `${fsLabel}`.
- `_inc/status.xml`: clock → `${fsClock}`.
- `assets/ui/capsule-shadow-soft.svg`: extra stops + softer crisp band.

## Non-goals
- No per-size repositioning of elements (positions stay fixed; verified to not overlap at x-large).
- No separate grid-size control (folded into the font-size scale, per decision).
- Vertical/portrait screen orientations not addressed (landscape only).

## Verification
- `xmllint` all changed/new files; run `tools/check-theme-paths.sh`.
- Load in ES-DE at medium (must look identical to current), then large and x-large (no overlaps; grid tiles bigger/fewer).
- On the phone (19.5:9 or 20:9): tiles render portrait (not square); text legible at large/x-large.

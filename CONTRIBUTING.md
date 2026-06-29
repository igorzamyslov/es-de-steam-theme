# Contributing

## Linting & checks

All checks are defined in [`.pre-commit-config.yaml`](.pre-commit-config.yaml) — the single source
of truth. CI runs exactly the same set via `pre-commit run --all-files`.

Set it up once, then the checks run automatically on every `git commit`:

```bash
pip install pre-commit   # or: pipx install pre-commit
pre-commit install
```

Run them all on demand:

```bash
pre-commit run --all-files
```

What runs:

| Check | Tool | What it catches |
| --- | --- | --- |
| Whitespace / line endings | `pre-commit-hooks` | trailing spaces, missing final newline, CRLF |
| XML + SVG well-formedness | `xmllint` | malformed files that break theme loading |
| Asset references | `scripts/check-asset-refs.py` | a `<path>` / `<include>` / `<fontPath>` / `<defaultImage>` … pointing at a file that doesn't exist |
| Markdown style | `markdownlint` | doc formatting issues |
| Doc links | `lychee` (CI only) | broken links in the docs |

`xmllint` must be on `PATH` (macOS: preinstalled; Debian/Ubuntu: `sudo apt-get install libxml2-utils`).
`python3` is needed for the asset-reference check (standard library only). pre-commit bootstraps
everything else (including Node for `markdownlint`).

The asset-reference check is the theme-specific one worth knowing about: ES-DE silently ignores a
missing asset (you just get a blank element or a skipped include), so this guards against typo'd or
moved paths. Paths containing an ES-DE variable (`${system.theme}`, etc.) are skipped — they resolve
at runtime and can't be verified statically.

## Updating the vendored ES-DE assets

`system-logos`, `system-controllers-outline`, and `system-metadata` are vendored from the official
ES-DE GitLab repos as git subtrees (committed in-tree so the theme is self-contained — see the README
note on why they are not submodules). To pull upstream updates:

```bash
git subtree pull --prefix=steam-bigpicture-es-de/system-logos                es-logos       master --squash
git subtree pull --prefix=steam-bigpicture-es-de/system-controllers-outline  es-controllers master --squash
git subtree pull --prefix=steam-bigpicture-es-de/system-metadata             es-metadata    master --squash
```

(The `es-logos` / `es-controllers` / `es-metadata` remotes are already configured; run
`git remote -v` to confirm.)

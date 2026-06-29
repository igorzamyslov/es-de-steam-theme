# Contributing

## Linting & checks

All checks are defined in [`.pre-commit-config.yaml`](.pre-commit-config.yaml). CI runs the same set via `pre-commit run --all-files`.

Set up once; checks run automatically on every `git commit`:

```bash
pip install pre-commit   # or: pipx install pre-commit
pre-commit install
```

Run on demand:

```bash
pre-commit run --all-files
```

What runs:

| Check | Tool | What it catches |
| --- | --- | --- |
| Whitespace / line endings | `pre-commit-hooks` | trailing spaces, missing final newline, CRLF |
| XML + SVG well-formedness | `xmllint` | malformed files that break theme loading |
| Asset references | `scripts/check-asset-refs.py` | `<path>` / `<include>` / `<fontPath>` / `<defaultImage>` pointing at a missing file |
| Markdown style | `markdownlint` | doc formatting issues |
| Doc links | `lychee` (CI only) | broken links in the docs |

`xmllint` must be on `PATH` (macOS: preinstalled; Debian/Ubuntu: `sudo apt-get install libxml2-utils`).
`python3` is needed for the asset-reference check (standard library only); pre-commit bootstraps everything else (including Node for `markdownlint`).

The asset-reference check is the theme-specific one worth knowing: ES-DE silently ignores missing assets (you get a blank element or a skipped include), so this guards against typo'd or moved paths. Paths with ES-DE variables (`${system.theme}`, etc.) are skipped — they resolve at runtime.

## Updating the vendored ES-DE assets

`system-logos`, `system-controllers-outline`, and `system-metadata` are vendored as git subtrees (committed in-tree so the theme is self-contained). To pull upstream updates:

```bash
git subtree pull --prefix=steam-ui/system-logos                es-logos       master --squash
git subtree pull --prefix=steam-ui/system-controllers-outline  es-controllers master --squash
git subtree pull --prefix=steam-ui/system-metadata             es-metadata    master --squash
```

The `es-logos` / `es-controllers` / `es-metadata` remotes are already configured; run `git remote -v` to confirm.

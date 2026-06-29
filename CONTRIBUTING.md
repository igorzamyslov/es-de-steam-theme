# Contributing

## Linting & checks

All checks run in CI (`.github/workflows/ci.yml`) on every push and PR. To run them locally:

```bash
bash scripts/lint.sh
```

This runs:

| Check | Tool | What it catches |
| --- | --- | --- |
| XML + SVG well-formedness | `xmllint` | malformed files that break theme loading |
| Asset references | `scripts/check-asset-refs.py` | a `<path>` / `<include>` / `<fontPath>` / `<defaultImage>` … pointing at a file that doesn't exist |
| Markdown style | `markdownlint` | doc formatting issues |
| Doc links | `lychee` (CI only) | broken links in the docs |

**Prerequisites**

- `xmllint` — macOS: preinstalled; Debian/Ubuntu: `sudo apt-get install libxml2-utils`.
- `python3` — for the asset-reference check (standard library only).
- *(optional)* Node/`npx` or `markdownlint-cli` — for Markdown linting; the script skips it if absent.

**Optional pre-commit hooks** (run the checks automatically on `git commit`):

```bash
pipx install pre-commit   # or: pip install pre-commit
pre-commit install
```

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

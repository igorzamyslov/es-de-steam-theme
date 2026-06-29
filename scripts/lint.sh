#!/usr/bin/env bash
# Run all theme checks. Used locally and by CI (.github/workflows/ci.yml).
#   - xmllint:            XML + SVG well-formedness (a malformed file breaks theme load)
#   - check-asset-refs:   every static <path>/<include>/<fontPath>/... resolves
#   - markdownlint:       docs style (skipped if neither markdownlint nor npx is present)
set -euo pipefail
cd "$(dirname "$0")/.."
THEME=steam-bigpicture-es-de
status=0

echo "==> xmllint: XML + SVG well-formedness"
find "$THEME" \
  \( -path "$THEME/system-logos" -o -path "$THEME/system-controllers-outline" \
     -o -path "$THEME/system-metadata" \) -prune -o \
  \( -name '*.xml' -o -name '*.svg' \) -print0 \
  | xargs -0 xmllint --noout && echo "    OK" || status=1

echo "==> asset references resolve"
python3 scripts/check-asset-refs.py || status=1

echo "==> markdownlint (docs)"
if command -v markdownlint >/dev/null 2>&1; then
  markdownlint . || status=1
elif command -v npx >/dev/null 2>&1; then
  npx --yes markdownlint-cli '**/*.md' || status=1
else
  echo "    skipped (install 'markdownlint-cli' or Node/npx to enable)"
fi

if [ "$status" -ne 0 ]; then
  echo "FAILED"
  exit 1
fi
echo "All checks passed."

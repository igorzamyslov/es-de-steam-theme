#!/bin/bash
# Verifies that ./-relative path values inside _inc/*.xml resolve to real files.
# ${system.theme} is substituted with a known system ("gc"). Other ${...} are skipped.
cd "$(git rev-parse --show-toplevel)/steam-bigpicture-es-de" || exit 2
fail=0
for f in _inc/*.xml; do
  dir="$(dirname "$f")"
  # extract path-like values
  grep -oE '<(path|staticImage|selectorImage|backgroundImage|default|defaultImage|include|fontRegular|fontSemiBold|fontExtraBold)>[^<]*</' "$f" \
   | sed -E 's/<[^>]+>//; s|</||' | while read -r p; do
      [ -z "$p" ] && continue
      case "$p" in ./*) ;; *) continue;; esac          # only ./-relative
      rp="${p/\$\{system.theme\}/gc}"
      case "$rp" in *'${'*) continue;; esac             # skip other variables
      resolved="$dir/$rp"
      if [ ! -e "$resolved" ]; then echo "MISSING: $f : $p  ->  $resolved"; fi
    done
done

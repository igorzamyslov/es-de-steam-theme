#!/usr/bin/env python3
"""Verify every STATIC file path referenced in the theme XML actually exists.

ES-DE silently ignores a missing <path>/<include>/<fontPath>/... (you just get a blank
element or a failed include), so a typo'd or moved asset is easy to ship. This walks the
theme's own XML, finds element text that looks like a relative file path, resolves it
relative to the file that references it, and checks it exists.

Paths containing an ES-DE variable (${...}) are skipped — they resolve at runtime
(e.g. ./../systems/art/${system.theme}.jpg) and cannot be checked statically.
The vendored upstream asset dirs are skipped (not ours to validate).
"""
import os
import re
import sys
import xml.etree.ElementTree as ET

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME = os.path.join(REPO, "steam-bigpicture-es-de")
VENDORED = {"system-logos", "system-controllers-outline", "system-metadata"}
# relative path ending in a known asset/include extension
PATH_RE = re.compile(r"^\.{1,2}/.*\.(svg|ttf|otf|jpe?g|png|xml|json)$", re.IGNORECASE)


def xml_files():
    for root, dirs, files in os.walk(THEME):
        dirs[:] = [d for d in dirs if d not in VENDORED]
        for fn in files:
            if fn.endswith(".xml"):
                yield os.path.join(root, fn)


def main():
    missing = []
    checked = 0
    for fp in xml_files():
        try:
            tree = ET.parse(fp)
        except ET.ParseError as exc:
            missing.append((fp, "<parse error>", str(exc)))
            continue
        base = os.path.dirname(fp)
        for el in tree.iter():
            txt = (el.text or "").strip()
            if not txt or "${" in txt or not PATH_RE.match(txt):
                continue
            checked += 1
            target = os.path.normpath(os.path.join(base, txt))
            if not os.path.exists(target):
                missing.append((os.path.relpath(fp, REPO), txt,
                                os.path.relpath(target, REPO)))

    if missing:
        print("FAIL: missing/unresolved asset references:")
        for ref in missing:
            print("  " + "  ->  ".join(ref))
        return 1
    print(f"OK: {checked} static asset references all resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

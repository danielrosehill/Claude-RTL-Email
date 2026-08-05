#!/usr/bin/env bash
# Render an email HTML file to PNG so you can look at it before sending.
#
# A browser render proves the markup is sound — direction, alignment, and that
# identifiers have not been reordered. It cannot prove Outlook is happy; the
# dir attributes in the templates are the insurance for that.
#
# Usage: ./scripts/preview.sh path/to/file.html [out.png]

set -euo pipefail

src="${1:?usage: preview.sh <file.html> [out.png]}"
out="${2:-${src%.html}.png}"

chrome=""
for c in google-chrome chromium chromium-browser brave-browser; do
  command -v "$c" >/dev/null 2>&1 && { chrome="$c"; break; }
done
[ -n "$chrome" ] || { echo "no chromium-family browser found" >&2; exit 1; }

# --window-size sets the viewport; RTL layout bugs show up at narrow widths
# more readily than wide ones, so this is deliberately not full-page.
"$chrome" --headless --disable-gpu --hide-scrollbars \
  --window-size=700,600 --screenshot="$out" "$src" 2>/dev/null

echo "wrote $out"

#!/bin/sh
# Rebuild slide decks into ../materials/.
#   ./build-decks.sh            all decks
#   ./build-decks.sh w03-foo    just that one (name with or without .qmd)
# Files beginning with "_" are templates and are skipped.
# NB: `quarto render a.qmd b.qmd` renders only the first file, hence the loop.
set -e
cd "$(dirname "$0")"
if [ $# -gt 0 ]; then set -- "${1%.qmd}.qmd"; else set -- $(ls *.qmd | grep -v '^_'); fi
for f in "$@"; do
  case "$f" in _*) continue ;; esac
  quarto render "$f" >/dev/null 2>&1 && echo "built ../materials/${f%.qmd}.html"
  # A <span class="math"> in the output means the LaTeX -> MathML conversion
  # failed and raw source is being shown. Unsupported commands (\small inside
  # \text, for one) do this silently, so check every build.
  if grep -q '<span class="math' "../materials/${f%.qmd}.html" 2>/dev/null; then
    echo "  !! UNCONVERTED MATH in ${f%.qmd}.html - check for unsupported LaTeX"
  fi
done
# type: website emits a stub index; decks are linked from the book instead.
rm -f ../materials/index.html ../materials/search.json

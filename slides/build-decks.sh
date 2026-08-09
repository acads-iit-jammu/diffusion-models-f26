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
done
# type: website emits a stub index; decks are linked from the book instead.
rm -f ../materials/index.html ../materials/search.json

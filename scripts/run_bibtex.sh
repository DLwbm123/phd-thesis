#!/usr/bin/env bash
set -euo pipefail
if command -v bibtex >/dev/null 2>&1; then
  exec bibtex "$@"
elif command -v bibtex.original >/dev/null 2>&1; then
  exec bibtex.original "$@"
elif [[ -x /usr/bin/bibtex.original ]]; then
  exec /usr/bin/bibtex.original "$@"
else
  echo "BibTeX executable not found. Install a complete TeX distribution." >&2
  exit 127
fi

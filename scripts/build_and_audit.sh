#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex
python3 scripts/style_audit.py --input chapters --patterns qa/style_red_flags.csv --output qa/style_audit_report.md
python3 scripts/reference_overlap_audit.py --thesis chapters --reference sources/reference_thesis --output qa/reference_overlap_report.md

#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

quiet=0
if [[ $# -gt 0 && "$1" == "--quiet" ]]; then
  quiet=1
  shift
fi

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 [--quiet] chapters/chXX_name.tex" >&2
  exit 2
fi

target="${1#./}"
if [[ ! -f "$target" || "${target##*.}" != "tex" ]]; then
  echo "Target must be an existing .tex file: $target" >&2
  exit 2
fi

if git diff --quiet HEAD -- "$target"; then
  echo "No uncommitted changes found in $target." >&2
  exit 3
fi
git diff --check HEAD
if ! git diff --quiet HEAD -- sources; then
  echo "Refusing fast verification: sources/ appears in the working diff." >&2
  exit 4
fi

tmp_root="$(mktemp -d /tmp/phd-thesis-fast-check.XXXXXX)"
cleanup() {
  python3 - "$tmp_root" <<'PY'
from pathlib import Path
import shutil
import sys

target = Path(sys.argv[1]).resolve()
if target.parent == Path("/tmp").resolve() and target.name.startswith("phd-thesis-fast-check."):
    shutil.rmtree(target, ignore_errors=True)
PY
}
trap cleanup EXIT

git diff --unified=0 HEAD -- "$target" \
  | awk '/^\+\+\+ / {next} /^\+/ {sub(/^\+/, ""); print}' \
  > "$tmp_root/changed.tex"

if ! grep -q '[^[:space:]]' "$tmp_root/changed.tex"; then
  echo "No added text extracted from $target." >&2
  exit 5
fi

python3 scripts/style_audit.py \
  --input "$tmp_root/changed.tex" \
  --patterns qa/style_red_flags.csv \
  --output "$tmp_root/style.md"
python3 scripts/reference_overlap_audit.py \
  --thesis "$tmp_root/changed.tex" \
  --reference sources/reference_thesis \
  --output "$tmp_root/overlap.md"

if ! latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex \
  >"$tmp_root/latexmk.log" 2>&1; then
  tail -n 160 "$tmp_root/latexmk.log" >&2
  exit 6
fi

if grep -Eqi \
  'LaTeX Error|Emergency stop|Undefined control sequence|Citation .* undefined|Reference .* undefined|There were undefined references|multiply defined' \
  main.log; then
  echo "Build log contains an unresolved LaTeX, citation, reference, or duplicate-label error." >&2
  tail -n 160 "$tmp_root/latexmk.log" >&2
  exit 7
fi

python3 - <<'PY'
import csv
import re
from pathlib import Path

bib = Path("bibliography/references.bib").read_text(encoding="utf-8")
keys = re.findall(r"(?im)^\s*@\w+\s*\{\s*([^,\s]+)", bib)
if len(keys) != len(set(k.casefold() for k in keys)):
    raise SystemExit("Duplicate BibTeX key detected")

entries = re.split(r"(?im)(?=^\s*@\w+\s*\{)", bib)
seen_doi, seen_title = set(), set()
for entry in entries:
    doi = re.search(r"(?im)^\s*doi\s*=\s*[{\"]?([^}\",\s]+)", entry)
    if doi:
        value = doi.group(1).strip().casefold()
        if value in seen_doi:
            raise SystemExit(f"Duplicate DOI detected: {value}")
        seen_doi.add(value)
    title = re.search(r'(?im)^\s*title\s*=\s*[{"](.+?)[}"]\s*,?\s*$', entry)
    if title:
        value = re.sub(r"[^a-z0-9]+", "", re.sub(r"\\[A-Za-z]+|[{}$]", "", title.group(1)).casefold())
        if value and value in seen_title:
            raise SystemExit(f"Duplicate normalized title detected: {value}")
        if value:
            seen_title.add(value)

for filename, width, unique_column in [
    ("evidence/claims.csv", 11, "claim_id"),
    ("qa/terminology.csv", 5, "term_en"),
]:
    with Path(filename).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows or len(rows[0]) != width:
        raise SystemExit(f"Invalid header width in {filename}")
    if any(len(row) != width for row in rows[1:]):
        raise SystemExit(f"Invalid CSV width in {filename}")
    index = rows[0].index(unique_column)
    values = [row[index].strip().casefold() for row in rows[1:] if row[index].strip()]
    if len(values) != len(set(values)):
        raise SystemExit(f"Duplicate {unique_column} detected in {filename}")
print(f"Fast metadata checks passed: {len(keys)} BibTeX keys; {len(values)} terminology keys.")
PY

fingerprint="$(python3 scripts/latex_input_fingerprint.py)"
marker="/tmp/phd-thesis-local-build.$fingerprint.ok"
date +%s >"$marker"

if [[ "$quiet" -eq 0 ]]; then
  echo "--- Added-text style audit ---"
  cat "$tmp_root/style.md"
  echo "--- Added-text reference-overlap audit ---"
  cat "$tmp_root/overlap.md"
fi
echo "Fast section verification passed for $target; local-build fingerprint=$fingerprint."

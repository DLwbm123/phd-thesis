#!/usr/bin/env bash
set -euo pipefail
: "${MMWHS_ROOT:?set MMWHS_ROOT}" "${SCRIBBLECL_OUTPUT_ROOT:?set SCRIBBLECL_OUTPUT_ROOT}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; export PYTHONPATH="$ROOT"
S="$SCRIBBLECL_OUTPUT_ROOT/scribbles/42"
python "$ROOT/scripts/generate_mmwhs_scribbles.py" --mmwhs-root "$MMWHS_ROOT" --output-root "$SCRIBBLECL_OUTPUT_ROOT" --seed 42
for family in pce zs; do python -m scribblecl.run --method "$family" --stage 1 --seed 42 --mmwhs-root "$MMWHS_ROOT" --scribble "$S/stage1.npz" --output-root "$SCRIBBLECL_OUTPUT_ROOT" "$@"; done
for method in pce pce_mib zs zs_mib; do
  family="${method%%_mib}"; parent="$SCRIBBLECL_OUTPUT_ROOT/${family}_seed42_stage1/best.pt"
  for st in 2 3; do python -m scribblecl.run --method "$method" --stage "$st" --seed 42 --mmwhs-root "$MMWHS_ROOT" --scribble "$S/stage${st}.npz" --output-root "$SCRIBBLECL_OUTPUT_ROOT" --parent "$parent" "$@"; parent="$SCRIBBLECL_OUTPUT_ROOT/${method}_seed42_stage${st}/best.pt"; done
done

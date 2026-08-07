#!/usr/bin/env bash
set -euo pipefail

CODE=${CODE:-$(cd "$(dirname "$0")/.." && pwd)}
OUT=${OUT:-/remote-home/wangbomin/ScribbleCL/static_task1_zs_v2}
MMWHS=${MMWHS:-/remote-home/wangbomin/CL_Benchmark/data/MMWHS}
SCRIBBLE=${SCRIBBLE:-/remote-home/wangbomin/ScribbleCL/v2_artifacts/scribbles/v2/42/S2/stage1.npz}
PYTHON=${PYTHON:-/root/anaconda3/bin/python}
DEVICE=${DEVICE:-cuda:0}
SOURCE_COMMIT=${SOURCE_COMMIT:-$(git -C "$CODE/../.." rev-parse HEAD 2>/dev/null || echo UNKNOWN)}

mkdir -p "$OUT" "$OUT/logs" "$OUT/smoke_repeat1" "$OUT/smoke_repeat2" "$OUT/diagnostic20" "$OUT/full"
cd "$CODE"

status_of() {
  "$PYTHON" - "$1" <<'PY'
import json,sys
try:
    print(json.load(open(sys.argv[1]))["status"])
except Exception:
    print("missing")
PY
}

run_static() {
  local level=$1 kind=$2 epochs=$3 root=$4 log=$5
  shift 5
  local directory="$root/static_${level}_sgd_seed42_${kind}"
  if [[ "$(status_of "$directory/run_manifest.json")" == completed ]]; then
    echo "SKIP_COMPLETED level=$level kind=$kind root=$root"
    return
  fi
  local resume=()
  [[ -s "$directory/last.pt" ]] && resume=(--resume)
  PYTHONPATH=. "$PYTHON" -m scribblecl.static_task1 \
    --level "$level" --mmwhs-root "$MMWHS" --scribble "$SCRIBBLE" \
    --output-root "$root" --optimizer sgd --lr .004 --epochs "$epochs" \
    --device "$DEVICE" --source-commit "$SOURCE_COMMIT" --run-kind "$kind" \
    "${resume[@]}" "$@" > "$log" 2>&1
}

single_gate() {
  local checkpoint=$1 output=$2 label=$3
  PYTHONPATH=. "$PYTHON" scripts/evaluate_static_gate.py \
    "$checkpoint" "$checkpoint" "$output" "$label"
}

pair_gate() {
  local previous=$1 current=$2 output=$3 label=$4
  PYTHONPATH=. "$PYTHON" scripts/evaluate_static_gate.py \
    "$previous" "$current" "$output" "$label"
}

PYTHONPATH=. "$PYTHON" -m pytest -q | tee "$OUT/pytest.log"
PYTHONPATH=. "$PYTHON" scripts/audit_shape_oracle.py \
  --mmwhs-root "$MMWHS" --csv results/mmwhs_shape_oracle.csv \
  --report reports/MMWHS_SHAPE_ORACLE.md

# Two-batch deterministic forward/backward gate. E explicitly exercises its
# spatial component although the full run remains locked to epoch-15 warm-up.
for level in A0 A C1 C2 C3 D E; do
  for repeat in 1 2; do
    extra=()
    [[ "$level" == E ]] && extra=(--force-spatial-smoke)
    run_static "$level" smoke 1 "$OUT/smoke_repeat$repeat" \
      "$OUT/logs/${level}_smoke_repeat${repeat}.log" --max-batches 2 --grad-every 1 "${extra[@]}"
  done
  if [[ "$level" =~ ^(C1|C2|C3|D|E)$ ]]; then
    PYTHONPATH=. "$PYTHON" scripts/summarize_static_smoke.py \
      --level "$level" \
      --repeat1 "$OUT/smoke_repeat1/static_${level}_sgd_seed42_smoke" \
      --repeat2 "$OUT/smoke_repeat2/static_${level}_sgd_seed42_smoke" \
      --output "reports/${level}_SMOKE.md"
  fi
done

# Twenty-epoch validation-only diagnostics are sequential. Any numerical or
# prediction-distribution failure prevents the next component from starting.
for level in A C1 C2 C3 D E; do
  run_static "$level" diagnostic20 20 "$OUT/diagnostic20" \
    "$OUT/logs/${level}_diagnostic20.log"
  single_gate \
    "$OUT/diagnostic20/static_${level}_sgd_seed42_diagnostic20/best_val.pt" \
    "$OUT/diagnostic20/gate_${level}.json" "${level}_diagnostic20"
  if [[ "$level" =~ ^(C1|C2|C3|D|E)$ ]]; then
    PYTHONPATH=. "$PYTHON" scripts/summarize_static_smoke.py \
      --level "$level" \
      --repeat1 "$OUT/smoke_repeat1/static_${level}_sgd_seed42_smoke" \
      --repeat2 "$OUT/smoke_repeat2/static_${level}_sgd_seed42_smoke" \
      --diagnostic "$OUT/diagnostic20/static_${level}_sgd_seed42_diagnostic20" \
      --output "reports/${level}_SMOKE.md"
  fi
done

# Full static runs and foreground-only component gates.
run_static A full 150 "$OUT/full" "$OUT/logs/A_full.log"
previous="$OUT/full/static_A_sgd_seed42_full/best_val.pt"
for level in C1 C2 C3 D E; do
  run_static "$level" full 150 "$OUT/full" "$OUT/logs/${level}_full.log"
  current="$OUT/full/static_${level}_sgd_seed42_full/best_val.pt"
  if ! pair_gate "$previous" "$current" "$OUT/full/gate_to_${level}.json" "to_${level}"; then
    printf '%s\n' 'DECISION: NO-GO-ZS' > reports/ZS_STATIC_TASK1_GATE_V2.md
    exit 2
  fi
  previous=$current
done

printf '%s\n\n%s\n' \
  'DECISION: GO-COVERAGE-RESELECT' \
  'All formal MMWHS Task-1 foreground gates passed. Test labels were not used.' \
  > reports/ZS_STATIC_TASK1_GATE_V2.md

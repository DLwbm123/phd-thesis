#!/usr/bin/env bash
set -euo pipefail

CODE=/remote-home/wangbomin/ScribbleCL/experiments/scribblecl_v2_commit470b0d0
OUT=/remote-home/wangbomin/ScribbleCL/static_task1_commit470b0d0
A_DIR=/remote-home/wangbomin/ScribbleCL/static_task1_commit951b182/static_A_sgd_seed42
MMWHS=/remote-home/wangbomin/CL_Benchmark/data/MMWHS
SCRIBBLE=/remote-home/wangbomin/ScribbleCL/v2_artifacts/scribbles/v2/42/S2/stage1.npz
PYTHON=/root/anaconda3/bin/python
DEVICE=cuda:1
SOURCE_COMMIT=470b0d0

cd "$CODE"

status_of() {
  "$PYTHON" - "$1" <<'PY'
import json,sys
try: print(json.load(open(sys.argv[1]))['status'])
except Exception: print('missing')
PY
}

run_one() {
  local level=$1 variant=$2 name=$3 log=$4
  local dir="$OUT/static_${name}_sgd_seed42"
  if [[ "$(status_of "$dir/run_manifest.json")" == completed ]]; then
    echo "SKIP_COMPLETED $name"
    return
  fi
  local resume=()
  [[ -s "$dir/last.pt" ]] && resume=(--resume)
  PYTHONPATH=. "$PYTHON" -m scribblecl.static_task1 \
    --level "$level" --variant "$variant" --mmwhs-root "$MMWHS" \
    --scribble "$SCRIBBLE" --output-root "$OUT" --optimizer sgd --lr .004 \
    --epochs 150 --device "$DEVICE" --source-commit "$SOURCE_COMMIT" \
    "${resume[@]}" > "$OUT/$log" 2>&1
}

gate() {
  local previous=$1 current=$2 output=$3 label=$4
  "$PYTHON" - "$previous" "$current" "$output" "$label" <<'PY'
import json,sys,torch
prev_path,cur_path,out,label=sys.argv[1:]
def read(path):
    ck=torch.load(path,map_location='cpu',weights_only=False)
    return ck['validation']
p,c=read(prev_path),read(cur_path)
classes={str(k):{'previous':p['patient_per_class'][k],
                 'current':c['patient_per_class'][k],
                 'ratio':c['patient_per_class'][k]/p['patient_per_class'][k]}
         for k in ('1','2','3')}
mean_drop=p['benchmark_mean']-c['benchmark_mean']
failed=[]
if mean_drop>0.03: failed.append(f'mean_drop={mean_drop:.10f}>0.03')
for k,v in classes.items():
    if v['ratio']<0.5: failed.append(f'class_{k}_ratio={v["ratio"]:.10f}<0.5')
result={'gate':label,'previous_epoch':p['epoch'],'current_epoch':c['epoch'],
        'previous_mean':p['benchmark_mean'],'current_mean':c['benchmark_mean'],
        'mean_drop':mean_drop,'classes':classes,'decision':'PASS' if not failed else 'STOP',
        'failure_reasons':failed}
open(out,'w').write(json.dumps(result,indent=2)+'\n'); print(json.dumps(result))
raise SystemExit(0 if not failed else 2)
PY
}

# Do not interfere with the already-running B process.
if [[ -f "$OUT/B.pid" ]]; then
  bpid=$(cat "$OUT/B.pid")
  while kill -0 "$bpid" 2>/dev/null; do sleep 30; done
fi
[[ "$(status_of "$OUT/static_B_sgd_seed42/run_manifest.json")" == completed ]] || exit 20

if gate "$A_DIR/best_val.pt" "$OUT/static_B_sgd_seed42/best_val.pt" "$OUT/gate_A_to_B.json" A_to_B; then
  b_pass=1
else
  b_pass=0
fi

# Required references/diagnostics use the identical framework and controls.
run_one A fg_only A0 A0.log
run_one A legacy_ratio A_ratio A_ratio.log
run_one A dense Dense_v2 Dense_v2.log

[[ $b_pass -eq 1 ]] || exit 0
run_one C standard C C.log
gate "$OUT/static_B_sgd_seed42/best_val.pt" "$OUT/static_C_sgd_seed42/best_val.pt" "$OUT/gate_B_to_C.json" B_to_C || exit 0
run_one D standard D D.log
gate "$OUT/static_C_sgd_seed42/best_val.pt" "$OUT/static_D_sgd_seed42/best_val.pt" "$OUT/gate_C_to_D.json" C_to_D || exit 0
run_one E standard E E.log
gate "$OUT/static_D_sgd_seed42/best_val.pt" "$OUT/static_E_sgd_seed42/best_val.pt" "$OUT/gate_D_to_E.json" D_to_E || exit 0

#!/usr/bin/env python3
from __future__ import annotations

import argparse, csv, json
from pathlib import Path

p=argparse.ArgumentParser(); p.add_argument("--runs-root",required=True); p.add_argument("--output",required=True); a=p.parse_args()
rows=[]
for manifest in Path(a.runs_root).rglob("run_manifest.json"):
    run=json.loads(manifest.read_text())
    if run.get("status")!="complete": continue
    rows.append({"run_id":run["run_id"],"scenario":run["scenario"],"method":run["method"],"seed":run["seed"],**run.get("summary",{})})
out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
with out.open("w",newline="") as f:
    fields=sorted({k for r in rows for k in r}); w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

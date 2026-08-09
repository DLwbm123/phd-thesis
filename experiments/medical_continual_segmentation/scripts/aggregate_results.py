#!/usr/bin/env python3
"""Aggregate completed manifests without selecting runs or seeds."""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from medcl.data import tasks_for


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--runs-root",type=Path,required=True); parser.add_argument("--output",type=Path,required=True); parser.add_argument("--reference-scenario",choices=("class","domain","organ")); parser.add_argument("--reference-output",type=Path); parser.add_argument("--attach-rma",action="store_true"); args=parser.parse_args(); rows=[]
    manifests=[]
    for path in sorted(args.runs_root.rglob("run_manifest.json")):
        value=json.loads(path.read_text())
        if value.get("status")!="complete": continue
        manifests.append(value)
        row={key:value.get(key) for key in ("run_id","scenario","method","seed","status","validity")}; row.update(value.get("summary",{})); rows.append(row)
    keys=sorted({key for row in rows for key in row}); args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("w",newline="") as stream: writer=csv.DictWriter(stream,fieldnames=keys); writer.writeheader(); writer.writerows(rows)
    if args.reference_scenario:
        if args.reference_output is None: raise ValueError("--reference-output is required")
        tasks=tasks_for(args.reference_scenario); by_task={x["task"]:x["summary"]["score"] for x in manifests if x.get("scenario")==args.reference_scenario and x.get("reference_type")=="independent_from_scratch" and x.get("seed")==42}; ordered=[by_task.get(x.code) for x in tasks]
        if any(value is None for value in ordered[1:]): raise RuntimeError("incomplete independent references")
        args.reference_output.parent.mkdir(parents=True,exist_ok=True); args.reference_output.write_text(json.dumps({"scenario":args.reference_scenario,"seed":42,"scores":ordered},indent=2,sort_keys=True)+"\n")
        if args.attach_rma:
            for path in sorted((args.runs_root/args.reference_scenario).glob("*/run_manifest.json")):
                value=json.loads(path.read_text())
                if value.get("status")!="complete" or value.get("reference_type"): continue
                matrix=[]
                with (path.parent/"performance_matrix.csv").open() as stream:
                    reader=csv.reader(stream); next(reader)
                    for row in reader: matrix.append([float(item) if item else float("nan") for item in row[1:]])
                diagonal=[matrix[index][index] for index in range(len(tasks))]; rma=sum(diagonal[index]/ordered[index] for index in range(1,len(tasks)))/(len(tasks)-1); value["summary"]["RMA"]=rma; value["rma_reference_file"]=args.reference_output.name; (path.parent/"summary.json").write_text(json.dumps(value["summary"],indent=2,sort_keys=True)+"\n"); path.write_text(json.dumps(value,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"rows":len(rows),"output":str(args.output)},indent=2))


if __name__=="__main__": main()

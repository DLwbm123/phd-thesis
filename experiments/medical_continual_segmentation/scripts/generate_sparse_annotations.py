#!/usr/bin/env python3
"""Generate deterministic foreground/background/unknown v2 S2 annotations."""
from __future__ import annotations
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys
import h5py
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from medcl.data import dataset_path, tasks_for
from medcl.data.sparse import digest, generate


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--scenario",choices=("class","domain","organ"),required=True); parser.add_argument("--data-root",type=Path,required=True); parser.add_argument("--output-root",type=Path,required=True); parser.add_argument("--seed",type=int,default=42); parser.add_argument("--foreground-area-multiplier",type=float,default=1.0); parser.add_argument("--background-area-multiplier",type=float,default=1.0); args=parser.parse_args(); rows=[]
    for task in tasks_for(args.scenario):
        path=dataset_path(args.data_root,task)
        with h5py.File(path,"r") as handle: labels=np.asarray(handle["train_labels"][:]).transpose(2,0,1).astype(np.int16)
        output=args.output_root/args.scenario/f"{task.code}_v2_s2_seed{args.seed}.npz"; previous=output.with_suffix(".json"); old=json.loads(previous.read_text()).get("stats") if previous.exists() else None
        annotations,stats=generate(labels,task.label_shift if args.scenario=="class" else 0,args.seed,args.foreground_area_multiplier,args.background_area_multiplier); output.parent.mkdir(parents=True,exist_ok=True); np.savez_compressed(output,annotations=annotations)
        metadata={"scenario":args.scenario,"task":task.code,"seed":args.seed,"protocol":"v2_S2_area_scaled","foreground_width_px":3,"labels":{"background":0,"unknown":-100},"area_scaling":{"requested_foreground_multiplier":args.foreground_area_multiplier,"requested_background_multiplier":args.background_area_multiplier,"previous_stats":old,"realized_foreground_multiplier":None if not old else stats.foreground_pixels/max(1,old["foreground_pixels"]),"realized_background_multiplier":None if not old else stats.background_pixels/max(1,old["background_pixels"])},"stats":asdict(stats)}; metadata["content_sha256"]=digest(annotations,metadata); output.with_suffix(".json").write_text(json.dumps(metadata,indent=2,sort_keys=True)+"\n"); rows.append({"task":task.code,"file":f"{args.scenario}/{output.name}",**metadata})
    print(json.dumps(rows,indent=2,sort_keys=True))


if __name__=="__main__": main()

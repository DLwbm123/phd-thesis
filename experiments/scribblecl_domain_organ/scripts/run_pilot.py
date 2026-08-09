#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import shutil
import sys
from datetime import datetime, timezone

import numpy as np
import torch
from torch.utils.data import DataLoader
import yaml

from scribblecl_do.data import domain_prostate, organ_tasks
from scribblecl_do.data.protocols import DOMAIN_TASKS, ORGAN_TASKS, EXPECTED_H5_SHA256, order_checksum
from scribblecl_do.data.scribbles import scribble_path
from scribblecl_do.methods.ewc import OnlineEWC, estimate_sparse_fisher
from scribblecl_do.methods.si import SynapticIntelligence
from scribblecl_do.metrics.matrix import matrix_summary
from scribblecl_do.models import DomainSegmenter, OrganSegmenter, build_backbone
from scribblecl_do.trainers.engine import evaluate_matrix_row, train_stage
from scribblecl_do.utils.provenance import file_sha256, seed_everything, tree_sha256


def jdump(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def jsonable_row(row):
    return [None if not np.isfinite(x) else float(x) for x in row]


def mapping_sha256(value: dict) -> str:
    payload=json.dumps(value,sort_keys=True,separators=(",",":")).encode()
    return sha256(payload).hexdigest()


def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("--config",required=True); p.add_argument("--data-root",required=True); p.add_argument("--scribble-root",required=True); p.add_argument("--runs-root",required=True); p.add_argument("--device",default="cuda:0"); p.add_argument("--shared-stage1-from"); p.add_argument("--paired-ft-run"); p.add_argument("--independent-scores"); a=p.parse_args()
    cfg=yaml.safe_load(Path(a.config).read_text()); scenario=cfg["scenario"]; method=cfg["method"]; seed=int(cfg["seed"])
    if cfg["supervision"]=="zs": raise RuntimeError("ZS blocked_by_static_gate")
    seed_everything(seed); tasks=DOMAIN_TASKS if scenario=="domain" else ORGAN_TASKS; factory=domain_prostate if scenario=="domain" else organ_tasks
    run_id=f"{scenario}_{method}_seed{seed}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"; run=Path(a.runs_root)/scenario/run_id; run.mkdir(parents=True,exist_ok=False); (run/"checkpoints").mkdir()
    shutil.copyfile(a.config,run/"config_resolved.yaml")
    source_root=Path(__file__).resolve().parents[1]
    prefix="Domain_Prostate" if scenario=="domain" else "Task_incre"
    h5_hashes={task.code:EXPECTED_H5_SHA256[f"{prefix}/{task.h5_name}"] for task in tasks}
    scribble_paths={task.code:scribble_path(a.scribble_root,scenario,task.code,seed) for task in tasks}
    scribble_hashes={code:file_sha256(path) for code,path in scribble_paths.items()}
    manifest={"run_id":run_id,"scenario":scenario,"method":method,"seed":seed,"status":"running","backbone":cfg["backbone"],"head":"shared_binary" if scenario=="domain" else "task_specific_binary","order_sha256":order_checksum(tasks),"split_h5_sha256":h5_hashes,"split_checksum_sha256":mapping_sha256(h5_hashes),"scribble_sha256":scribble_hashes,"scribble_protocol":"v2_S2_width3","checkpoint_selection":cfg["checkpoint_selection"],"test_for_selection":bool(cfg["test_for_selection"]),"source_tree_sha256":tree_sha256(source_root/"scribblecl_do"),"history_images":False,"replay":False,"zs_gate":"blocked_by_static_gate"}
    jdump(run/"run_manifest.json",manifest); (run/"environment.txt").write_text(f"python={sys.version}\nplatform={platform.platform()}\ntorch={torch.__version__}\ncuda={torch.version.cuda}\ndevice={a.device}\n")
    for name in ("train.jsonl","validation.jsonl","stdout.log","stderr.log"): (run/name).touch()
    model=(DomainSegmenter(build_backbone(cfg["backbone"])) if scenario=="domain" else OrganSegmenter(build_backbone(cfg["backbone"]))).to(a.device)
    ewc=OnlineEWC(cfg.get("ewc",{}).get("lambda",1.0),cfg.get("ewc",{}).get("gamma",0.1)) if method.endswith("ewc") else None
    si=SynapticIntelligence(cfg.get("si",{}).get("c",5.0),cfg.get("si",{}).get("xi",1.0)) if method.endswith("si") else None
    rows=[]; stage_records=[]; fisher_records=[]; parent_sha=None
    # Random initialization is evaluated only for Domain E-FWT.
    random_scores=None
    if scenario=="domain":
        random_scores,_=evaluate_matrix_row(model,tasks,lambda t,s: factory.dense_dataset(a.data_root,t,s),a.device,scenario,-1,cfg["batch_size"])
    for stage,task in enumerate(tasks):
        if scenario=="organ":
            model.activate_head(stage)
        npz=scribble_paths[task.code]
        weak=factory.weak_dataset(a.data_root,task,npz); loader=DataLoader(weak,batch_size=cfg["batch_size"],shuffle=True,num_workers=0,generator=torch.Generator().manual_seed(seed+stage))
        skipped=False
        if stage==0 and a.shared_stage1_from:
            parent=Path(a.shared_stage1_from); checkpoint=parent/"checkpoints/stage_1.pt"; model.load_state_dict(torch.load(checkpoint,map_location=a.device,weights_only=True)); parent_sha=file_sha256(checkpoint); skipped=True; resource={"seconds":0.0,"steps":0,"last_loss":None,"peak_memory_bytes":0,"shared_parent":str(checkpoint)}
        else:
            resource=train_stage(model,loader,a.device,None if scenario=="domain" else stage,cfg["supervision"],cfg["epochs"],cfg["learning_rate"],cfg["lr_decay_epoch"],cfg["lr_decay_rate"],run/"train.jsonl",ewc=ewc,si=si)
        row,details=evaluate_matrix_row(model,tasks,lambda t,s: factory.dense_dataset(a.data_root,t,s),a.device,scenario,stage,cfg["batch_size"]); rows.append(row)
        if stage==1:
            current=details[stage]
            gate={"finite":bool(np.isfinite(row[stage])),"current_nonempty":current["prediction_fg_fraction"]>0,"ewc_penalty_finite":True}
            if ewc is not None:
                gate["ewc_penalty_finite"]=bool(torch.isfinite(ewc.penalty(model)))
                if a.paired_ft_run:
                    paired=json.loads((Path(a.paired_ft_run)/"stage_rows.json").read_text())["rows"][stage][stage]
                    gate["current_vs_ft_ratio"]=row[stage]/paired; gate["current_at_least_50pct_ft"]=gate["current_vs_ft_ratio"]>=.5
            jdump(run/"STAGE2_GATE.json",gate)
            if not all(v for k,v in gate.items() if isinstance(v,bool)):
                jdump(run/"STAGE2_BLOCKER.json",gate); raise RuntimeError(f"stage-2 engineering gate failed: {gate}")
        # Fisher is always current-task sparse PCE, including for a shared parent.
        if ewc is not None:
            fisher_loader=DataLoader(weak,batch_size=cfg["batch_size"],shuffle=False,num_workers=0)
            fisher,summary=estimate_sparse_fisher(model,fisher_loader,a.device,None if scenario=="domain" else stage,cfg["ewc"].get("fisher_max_batches")); ewc.consolidate(model,fisher); fisher_records.append({"stage":stage+1,**summary.__dict__})
            ewc_path=run/f"checkpoints/ewc_state_stage_{stage+1}.pt"; torch.save(ewc.state_dict(),ewc_path); resource["ewc_state_sha256"]=file_sha256(ewc_path)
        if si is not None:
            si.consolidate(model)
            si_path=run/f"checkpoints/si_state_stage_{stage+1}.pt"; torch.save(si.state_dict(),si_path); resource["si_state_sha256"]=file_sha256(si_path)
        checkpoint=run/f"checkpoints/stage_{stage+1}.pt"; torch.save(model.state_dict(),checkpoint)
        resource.update({"stage":stage+1,"task":task.code,"checkpoint_sha256":file_sha256(checkpoint),"ewc_state_bytes":ewc.state_nbytes() if ewc else 0,"si_state_bytes":si.state_nbytes() if si else 0,"model_parameters":sum(p.numel() for p in model.parameters())}); stage_records.append(resource)
        if scenario=="organ": model.freeze_completed_head(stage)
        weak.close(); jdump(run/"stage_rows.json",{"rows":[jsonable_row(x) for x in rows],"details":details})
    matrix=np.asarray(rows,dtype=np.float64)
    with (run/"performance_matrix.csv").open("w",newline="") as stream:
        writer=csv.writer(stream); writer.writerow(["stage"]+[t.code for t in tasks]);
        for i,row in enumerate(matrix): writer.writerow([i+1]+["" if not np.isfinite(x) else f"{x:.10f}" for x in row])
    with (run/"stage_metrics.csv").open("w",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=sorted({k for r in stage_records for k in r})); writer.writeheader(); writer.writerows(stage_records)
    jdump(run/"fisher_summary.json",fisher_records)
    summary={"A-Dice":float(np.mean(matrix[-1])),"BWTR":float(np.mean((matrix[-1,:-1]-np.diag(matrix)[:-1])/np.diag(matrix)[:-1])),"mean_current":float(np.mean(np.diag(matrix))),"final_old_mean":float(np.mean(matrix[-1,:-1]))}
    if scenario=="domain": summary["E-FWT"]=float(np.mean([matrix[t,i]-random_scores[i] for t in range(len(tasks)-1) for i in range(t+1,len(tasks))]))
    if a.independent_scores:
        refs=json.loads(Path(a.independent_scores).read_text())["scores"]; summary["RMA"]=float(np.mean(np.diag(matrix)[1:]/np.asarray(refs)[1:]))
    else: summary["RMA"]=None
    jdump(run/"summary.json",summary); (run/"best_checkpoint_pointer.txt").write_text(str(run/f"checkpoints/stage_{len(tasks)}.pt")+"\n")
    manifest.update(status="complete",completed_at=datetime.now(timezone.utc).isoformat(),parent_checkpoint_sha256=parent_sha,summary=summary); jdump(run/"run_manifest.json",manifest)
    print(run)


if __name__=="__main__": main()

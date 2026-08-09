#!/usr/bin/env python3
"""Per-task from-scratch PCE references required by Benchmark RMA."""
from __future__ import annotations

import argparse, json
from pathlib import Path

import torch
from torch.utils.data import DataLoader
import yaml

from scribblecl_do.data import domain_prostate, organ_tasks
from scribblecl_do.data.protocols import DOMAIN_TASKS, ORGAN_TASKS
from scribblecl_do.data.scribbles import scribble_path
from scribblecl_do.metrics.segmentation import evaluate_patient_loader
from scribblecl_do.models import DomainSegmenter, OrganSegmenter, build_backbone
from scribblecl_do.trainers.engine import train_stage
from scribblecl_do.utils.provenance import seed_everything


def main():
    p=argparse.ArgumentParser(); p.add_argument("--config",required=True); p.add_argument("--data-root",required=True); p.add_argument("--scribble-root",required=True); p.add_argument("--output",required=True); p.add_argument("--device",default="cuda:0"); a=p.parse_args()
    cfg=yaml.safe_load(Path(a.config).read_text()); scenario=cfg["scenario"]; tasks=DOMAIN_TASKS if scenario=="domain" else ORGAN_TASKS; factory=domain_prostate if scenario=="domain" else organ_tasks; out=Path(a.output); out.mkdir(parents=True,exist_ok=False); scores=[]; records=[]
    for task in tasks:
        seed_everything(cfg["seed"]); model=(DomainSegmenter(build_backbone(cfg["backbone"])) if scenario=="domain" else OrganSegmenter(build_backbone(cfg["backbone"]))).to(a.device)
        if scenario == "organ": model.activate_head(task.index)
        weak=factory.weak_dataset(a.data_root,task,scribble_path(a.scribble_root,scenario,task.code,cfg["seed"])); loader=DataLoader(weak,batch_size=cfg["batch_size"],shuffle=True,num_workers=0,generator=torch.Generator().manual_seed(cfg["seed"])); resource=train_stage(model,loader,a.device,None if scenario=="domain" else task.index,"pce",cfg["epochs"],cfg["learning_rate"],cfg["lr_decay_epoch"],cfg["lr_decay_rate"],out/"train.jsonl"); dense=factory.dense_dataset(a.data_root,task,"test"); metric=evaluate_patient_loader(model,DataLoader(dense,batch_size=cfg["batch_size"],shuffle=False),dense.patient_info,a.device,None if scenario=="domain" else task.index); scores.append(metric["benchmark_mean"]); records.append({"task":task.code,"score":metric["benchmark_mean"],**resource}); dense.close(); weak.close()
    (out/"independent_scores.json").write_text(json.dumps({"scenario":scenario,"seed":cfg["seed"],"scores":scores,"records":records},indent=2,sort_keys=True)+"\n")


if __name__=="__main__": main()

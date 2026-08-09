#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader, Subset

from scribblecl_do.data import domain_prostate, organ_tasks
from scribblecl_do.data.protocols import DOMAIN_TASKS, ORGAN_TASKS
from scribblecl_do.methods.ft import sparse_pce
from scribblecl_do.metrics.segmentation import binary_patient_dice
from scribblecl_do.models import DomainSegmenter, OrganSegmenter, build_backbone
from scribblecl_do.utils.provenance import seed_everything


@torch.no_grad()
def score(model, batches, device, task_id):
    model.eval(); pred=[]; target=[]
    for x, y in batches:
        z = model(x.to(device)) if task_id is None else model(x.to(device), task_id)
        pred.append(z.argmax(1).cpu().numpy()); target.append(y.numpy())
    return float(binary_patient_dice(np.concatenate(pred), np.concatenate(target))[1])


def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("--scenario",choices=["domain","organ"],required=True); p.add_argument("--task",required=True); p.add_argument("--data-root",required=True); p.add_argument("--scribble-root",required=True); p.add_argument("--output",required=True); p.add_argument("--supervision",choices=["dense","pce"],required=True); p.add_argument("--backbone",default="resunet32",choices=["resunet32","zs_unet"]); p.add_argument("--device",default="cuda:0"); p.add_argument("--steps",type=int,default=500); p.add_argument("--lr",type=float,default=1e-3); p.add_argument("--seed",type=int,default=42); a=p.parse_args()
    seed_everything(a.seed)
    tasks = DOMAIN_TASKS if a.scenario=="domain" else ORGAN_TASKS; task=next(t for t in tasks if t.code==a.task); factory=domain_prostate if a.scenario=="domain" else organ_tasks
    dense=factory.dense_dataset(a.data_root,task,"train")
    positives=[]
    for i in range(len(dense)):
        _,y=dense[i]
        if bool((y==1).any()): positives.append(i)
        if len(positives)==12: break
    if len(positives)<8: raise RuntimeError("fewer than eight positive dense slices")
    # Dense gate uses one fixed full batch so BatchNorm running statistics
    # represent the complete tiny set rather than whichever micro-batch ran last.
    dense_batches=list(DataLoader(Subset(dense,positives),batch_size=len(positives),shuffle=False))
    if a.supervision=="dense": train_batches=dense_batches
    else:
        npz=Path(a.scribble_root)/a.scenario/f"{task.code}_v2_s3_seed{a.seed}.npz"; weak=factory.weak_dataset(a.data_root,task,npz); train_batches=list(DataLoader(Subset(weak,positives[:8]),batch_size=4,shuffle=False))
    model=(DomainSegmenter(build_backbone(a.backbone)) if a.scenario=="domain" else OrganSegmenter(build_backbone(a.backbone))).to(a.device); task_id=None if a.scenario=="domain" else task.index
    if task_id is not None: model.activate_head(task_id)
    optimizer=torch.optim.Adam(model.parameters(),lr=a.lr); log=[]
    for step in range(1,a.steps+1):
        model.train(); x,y=train_batches[(step-1)%len(train_batches)]; x,y=x.to(a.device),y.to(a.device); logits=model(x) if task_id is None else model(x,task_id); loss=torch.nn.functional.cross_entropy(logits,y) if a.supervision=="dense" else sparse_pce(logits,y); optimizer.zero_grad(); loss.backward(); optimizer.step()
        if step==1 or step%25==0:
            row={"step":step,"loss":float(loss.detach()),"dense_fg_dice":score(model,dense_batches,a.device,task_id)}; log.append(row)
            if a.supervision=="dense" and row["dense_fg_dice"]>=.95: break
            if a.supervision=="pce" and step>=50 and row["loss"] <= .25*log[0]["loss"]: break
    status = log[-1]["dense_fg_dice"]>=.95 if a.supervision=="dense" else log[-1]["loss"]<log[0]["loss"]
    out=Path(a.output); out.mkdir(parents=True,exist_ok=True); (out/"metrics.json").write_text(json.dumps({"status":"PASS" if status else "FAIL","indices":positives,"log":log},indent=2)+"\n")
    if not status: raise SystemExit(2)


if __name__=="__main__": main()

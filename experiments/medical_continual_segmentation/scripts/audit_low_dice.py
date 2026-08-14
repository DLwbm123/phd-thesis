#!/usr/bin/env python3
"""Read-only low-learnability audit for completed seed-42 PCE runs."""
from __future__ import annotations

import argparse, csv, json
from pathlib import Path
import sys

import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from medcl.data import DenseDataset, SparseDataset, dataset_path, tasks_for
from medcl.data.protocols import IGNORE_INDEX
from medcl.metrics.segmentation import dice_for_classes, evaluate
from medcl.models import build_model


def dump(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def load_model(scenario, checkpoint, stage, device):
    model = build_model(scenario)
    if scenario == "organ":
        for index in range(stage + 1): model.activate_stage(index)
    elif hasattr(model, "activate_stage"): model.activate_stage(stage)
    state = torch.load(checkpoint, map_location="cpu", weights_only=False)["model"]
    model.load_state_dict(state); return model.to(device).eval()


def classes(scenario, task):
    return tuple(range(task.label_shift + 1, task.label_shift + 1 + len(task.classes))) if scenario == "class" else (1,)


@torch.no_grad()
def prediction_metrics(model, dataset, scenario, task, device, task_id):
    prediction=[]; target=[]
    for image,label in DataLoader(dataset,batch_size=8):
        prediction.append(model(image.to(device), task_id).argmax(1).cpu().numpy()); target.append(label.numpy())
    pred=np.concatenate(prediction); truth=np.concatenate(target); fg_classes=classes(scenario,task); pos=np.isin(truth,fg_classes).any((1,2))
    slice_dice=[]
    for p,t in zip(pred[pos],truth[pos]): slice_dice.append(float(dice_for_classes(p,t,fg_classes).mean()))
    volume=float(dice_for_classes(pred,truth,fg_classes).mean()); bg=float(dice_for_classes(pred,truth,(0,))[0])
    return {"foreground_patient_mean":evaluate(model,DataLoader(dataset,batch_size=8),dataset.patient_info,device,task_id,fg_classes)["benchmark_mean"],
            "aggregate_volume_dice":volume,"positive_slice_dice":float(np.mean(slice_dice)) if slice_dice else None,
            "bg_dice":bg,"bg_inclusive_mean":float(np.mean(np.r_[bg,dice_for_classes(pred,truth,fg_classes)])),
            "bg_prediction_fraction":float((pred==0).mean()),"fg_prediction_fraction":float((pred>0).mean()),
            "nonempty_prediction_rate":float((pred>0).any((1,2)).mean()),"positive_slice_fraction":float(pos.mean())}


def audit_matrices(root, results, reports, device):
    data=Path("/remote-home/wangbomin/CL_Benchmark/data")
    diagonal=[]; prediction=[]; lines=["# Low Dice matrix audit", "", "All six runs are fixed-last-epoch checkpoints; no validation-best checkpoint was used.", ""]
    for scenario in ("class","domain","organ"):
        for method in ("pce_ft","pce_ewc"):
            run=root/"runs"/scenario/f"medseg_{scenario}_{method}_seed42_final"; manifest=json.loads((run/"run_manifest.json").read_text())
            with (run/"performance_matrix.csv").open() as stream:
                raw=list(csv.reader(stream))[1:]
            matrix=np.asarray([[float(value) if value else np.nan for value in row[1:]] for row in raw],dtype=float)
            tasks=tasks_for(scenario); diag=np.diag(matrix); final=matrix[-1]
            lines += [f"## {scenario} {method}", f"- diagonal: {diag.tolist()}", f"- final row: {final.tolist()}", f"- checkpoint selection: fixed last epoch (149)"]
            for stage,task in enumerate(tasks):
                diagonal.append({"scenario":scenario,"method":method,"task":task.code,"stage":stage+1,"diagonal_dtt":diag[stage],"final_cell":final[stage],"checkpoint_selection":"fixed_last_epoch_149"})
                cp=run/f"stage_{stage+1}.pt"; model=load_model(scenario,cp,stage,device); dense=DenseDataset(dataset_path(data,task),"test",task.label_shift if scenario=="class" else 0)
                metrics=prediction_metrics(model,dense,scenario,task,device,stage if scenario=="organ" else None); dense.close(); prediction.append({"scenario":scenario,"method":method,"stage":stage+1,"task":task.code,"checkpoint":str(cp),**metrics})
                del model; torch.cuda.empty_cache()
    lines += ["", "## Interpretation", "- Diagonals are low in every setting, so low A-Dice is not attributable solely to forgetting.", "- Class has both very low final old-task cells and low T1/T3 diagonal learning; its BWTR is not interpretable as isolated forgetting.", "- EWC has no consistent current-task improvement: it is a diagnostic comparison, not evidence of a forgetting remedy."]
    with (results/"low_dice_stage_diagonals.csv").open("w",newline="") as f: w=csv.DictWriter(f,fieldnames=diagonal[0].keys()); w.writeheader(); w.writerows(diagonal)
    with (results/"low_dice_prediction_audit.csv").open("w",newline="") as f: w=csv.DictWriter(f,fieldnames=prediction[0].keys()); w.writeheader(); w.writerows(prediction)
    (reports/"LOW_DICE_MATRIX_AUDIT.md").write_text("\n".join(lines)+"\n")


def sparse_balance(root, results, reports, device):
    data=Path("/remote-home/wangbomin/CL_Benchmark/data"); sparse_root=Path("/remote-home/wangbomin/medical_segmentation_data/sparse_annotations"); rows=[]
    for scenario in ("class","domain","organ"):
        final=root/"runs"/scenario/f"medseg_{scenario}_pce_ft_seed42_final"; final_stage=len(tasks_for(scenario))-1; model=load_model(scenario,final/"last.pt",final_stage,device)
        for task in tasks_for(scenario):
            sparse=SparseDataset(dataset_path(data,task),sparse_root/scenario/f"{task.code}_v2_s2_seed42.npz"); dense=DenseDataset(dataset_path(data,task),"train",task.label_shift if scenario=="class" else 0)
            true_pos=np.asarray([bool(np.isin(dense[i][1].numpy(),classes(scenario,task)).any()) for i in range(len(dense))]); ann=sparse.annotations; known=ann!=IGNORE_INDEX; known_fg=np.isin(ann,classes(scenario,task)); known_bg=ann==0
            generator=np.random.default_rng(42+task.index*100000); order=generator.permutation(len(sparse)); batches=[order[i:i+8] for i in range(0,len(order),8)]
            pos_loss=[]; neg_loss=[]; pred_bg=[]
            for image,label in DataLoader(sparse,batch_size=8,shuffle=False):
                image,label=image.to(device),label.to(device); logits=model(image,task.index if scenario=="organ" else None); pixel=F.cross_entropy(logits,label,ignore_index=IGNORE_INDEX,reduction="none"); pred=logits.argmax(1)
                for i in range(len(label)):
                    mask=label[i]!=IGNORE_INDEX
                    if mask.any(): (pos_loss if true_pos[len(pos_loss)+len(neg_loss)] else neg_loss).append(float(pixel[i][mask].mean()))
                    pred_bg.append(float((pred[i]==0).float().mean()))
            per_class={str(c):int((ann==c).sum()) for c in classes(scenario,task)}
            rows.append({"scenario":scenario,"task":task.code,"positive_slices":int(true_pos.sum()),"negative_slices":int((~true_pos).sum()),"positive_slice_fraction":float(true_pos.mean()),"known_bg_pixels":int(known_bg.sum()),"known_fg_pixels":int(known_fg.sum()),"known_bg_fg_ratio":float(known_bg.sum()/max(1,known_fg.sum())),"per_class_known_pixels":json.dumps(per_class,sort_keys=True),"valid_pixels_per_sample":float(known.sum(1).mean()),"valid_pixels_per_batch":float(np.mean([known[x].sum() for x in batches])),"positive_samples_per_batch":float(np.mean([true_pos[x].sum() for x in batches])),"pce_loss_positive_slices":float(np.mean(pos_loss)) if pos_loss else None,"pce_loss_negative_slices":float(np.mean(neg_loss)) if neg_loss else None,"bg_prediction_fraction":float(np.mean(pred_bg))})
            sparse.close(); dense.close()
        del model; torch.cuda.empty_cache()
    with (results/"sparse_balance_audit.csv").open("w",newline="") as f: w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    high=sorted(rows,key=lambda x:x["known_bg_fg_ratio"],reverse=True)[:5]
    (reports/"SPARSE_BALANCE_AUDIT.md").write_text("# Sparse balance audit\n\n"+"All PCE losses are measured on known pixels only with the completed FT checkpoint.\n\nHighest known BG:FG ratios:\n\n"+"\n".join(f"- {x['scenario']} {x['task']}: {x['known_bg_fg_ratio']:.2f}; positive-slice fraction {x['positive_slice_fraction']:.3f}; predicted BG {x['bg_prediction_fraction']:.3f}" for x in high)+"\n")


def first_task_pce(root, results, device):
    data=Path("/remote-home/wangbomin/CL_Benchmark/data"); rows=[]
    for scenario in ("class","domain","organ"):
        task=tasks_for(scenario)[0]; run=root/"runs"/scenario/f"medseg_{scenario}_pce_ft_seed42_final"; model=load_model(scenario,run/"stage_1.pt",0,device); dense=DenseDataset(dataset_path(data,task),"test",task.label_shift if scenario=="class" else 0)
        rows.append({"scenario":scenario,"task":task.code,"checkpoint":str(run/"stage_1.pt"),**prediction_metrics(model,dense,scenario,task,device,0 if scenario=="organ" else None)}); dense.close(); del model; torch.cuda.empty_cache()
    with (results/"current_recipe_pce_first_task.csv").open("w",newline="") as f: w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=Path,default=Path(".")); ap.add_argument("--device",default="cuda:1"); args=ap.parse_args(); root=args.root.resolve(); results=root/"results"; reports=root/"reports"; results.mkdir(exist_ok=True); reports.mkdir(exist_ok=True)
    audit_matrices(root,results,reports,args.device); sparse_balance(root,results,reports,args.device); first_task_pce(root,results,args.device)


if __name__=="__main__": main()

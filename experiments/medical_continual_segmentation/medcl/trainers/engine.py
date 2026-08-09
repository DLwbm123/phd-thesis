from __future__ import annotations

from dataclasses import asdict, dataclass
import csv
import json
import os
from pathlib import Path
import random
import shutil
import time

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset, Subset

from medcl.data import DenseDataset, SparseDataset, dataset_path, tasks_for
from medcl.data.protocols import EXPECTED_SHA256, IGNORE_INDEX, order_sha256
from medcl.methods import OnlineEWC, SynapticIntelligence, estimate_fisher
from medcl.metrics import evaluate, matrix_summary
from medcl.models import build_model
from medcl.supervision import supervision_loss
from medcl.utils import CheckpointController, file_sha256, seed_all, tree_sha256


@dataclass
class RunOptions:
    scenario: str
    method: str
    data_root: Path
    sparse_root: Path
    runs_root: Path
    seed: int = 42
    epochs: int = 150
    batch_size: int = 8
    learning_rate: float = 0.008
    lr_decay_epoch: int = 80
    lr_decay_rate: float = 0.5
    fisher_batches: int = 50
    device: str = "cuda:0"
    run_id: str | None = None
    resume: Path | None = None
    stage1_parent: Path | None = None
    max_stage: int | None = None
    current_gate_min: float = 0.10
    independent_scores: Path | None = None


class _MemorySparse(Dataset):
    exposes_dense = False

    def __init__(self, images, labels): self.images, self.labels = images, labels
    def __len__(self): return len(self.images)
    def __getitem__(self, index): return self.images[index], self.labels[index]


def _json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


def _append(path: Path, value) -> None:
    with path.open("a") as stream: stream.write(json.dumps(value, sort_keys=True) + "\n")


def _activate(model, stage: int) -> None:
    if hasattr(model, "activate_stage"): model.activate_stage(stage)


def _model_task(scenario: str, evaluated_stage: int):
    return evaluated_stage if scenario == "organ" else None


def _classes(scenario: str, task) -> tuple[int, ...]:
    if scenario == "class": return tuple(range(task.label_shift + 1, task.label_shift + 1 + len(task.classes)))
    return (1,)


def _optimizer(model, options):
    return torch.optim.SGD([p for p in model.parameters() if p.requires_grad], lr=options.learning_rate, momentum=0.9, weight_decay=0.0)


def _annotation_path(root: Path, scenario: str, code: str, seed: int) -> Path:
    return root / scenario / f"{code}_v2_s2_seed{seed}.npz"


def _loaders(options: RunOptions, task, supervision: str):
    path = dataset_path(options.data_root, task)
    if supervision == "pce":
        train = SparseDataset(path, _annotation_path(options.sparse_root, options.scenario, task.code, options.seed))
    else:
        train = DenseDataset(path, "train", task.label_shift if options.scenario == "class" else 0)
    val = DenseDataset(path, "val", task.label_shift if options.scenario == "class" else 0)
    test = DenseDataset(path, "test", task.label_shift if options.scenario == "class" else 0)
    generator = torch.Generator().manual_seed(options.seed + task.index)
    return train, DataLoader(train, batch_size=options.batch_size, shuffle=True, generator=generator, num_workers=0), val, test


def _manifest(options: RunOptions, run_id: str, tasks, source_root: Path) -> dict:
    audit_path=source_root/"reports"/f"{options.scenario}_data_audit.json"; audited={}
    if audit_path.exists():
        audit=json.loads(audit_path.read_text())
        if audit.get("status")=="PASS": audited={row["task"]:row["sha256"] for row in audit["tasks"]}
    files = {task.code: audited.get(task.code) or file_sha256(dataset_path(options.data_root, task)) for task in tasks}
    sparse = {}; annotation_stats = {}
    if options.method.startswith("pce_") or options.method.endswith("ewc"):
        sparse = {task.code: file_sha256(_annotation_path(options.sparse_root, options.scenario, task.code, options.seed)) for task in tasks}
        for task in tasks:
            sidecar=_annotation_path(options.sparse_root,options.scenario,task.code,options.seed).with_suffix(".json"); value=json.loads(sidecar.read_text()); stats=value["stats"]; total=stats["foreground_pixels"]+stats["background_pixels"]+stats["unknown_pixels"]; dense_bg=total-stats["dense_foreground_pixels"]
            annotation_stats[task.code]={**stats,"foreground_coverage":stats["foreground_pixels"]/max(1,stats["dense_foreground_pixels"]),"background_annotation_ratio":stats["background_pixels"]/max(1,dense_bg),"total_annotation_ratio":(stats["foreground_pixels"]+stats["background_pixels"])/total,"content_sha256":value["content_sha256"]}
    public_options={key:("<external_data>" if key in {"data_root","sparse_root"} else "<run_root>" if key=="runs_root" else None if value is None else Path(value).name if key in {"resume","stage1_parent","independent_scores"} else value) for key,value in asdict(options).items()}
    result = {
        "run_id": run_id, "status": "running", "validity": "pending_gates",
        "scenario": options.scenario, "method": options.method, "seed": options.seed,
        "main_entry": "main.py", "backbone": "U-Net", "history_images": False,
        "replay": False, "test_for_selection": False, "enhanced_gate": "blocked_by_static_gate",
        "resume_command": f"python main.py --scenario {options.scenario} --method {options.method} --data-root <external_data> --sparse-root <external_data> --runs-root <run_root> --resume last.pt",
        "order_sha256": order_sha256(tasks), "dataset_sha256": files,
        "expected_dataset_sha256": {task.code: EXPECTED_SHA256[f"{task.folder}/{task.file}"] for task in tasks},
        "annotation_sha256": sparse, "annotation_stats":annotation_stats, "source_tree_sha256": tree_sha256(source_root),
        "options": public_options,
    }
    if options.stage1_parent: result["parent_checkpoint_sha256"]=file_sha256(options.stage1_parent)
    if options.resume: result["resume_checkpoint_sha256"]=file_sha256(options.resume)
    return result


def dry_run(scenario: str, method: str, device: str = "cpu") -> dict:
    if method.startswith("enhanced_"): raise RuntimeError("blocked_by_static_gate")
    seed_all(42); model = build_model(scenario).to(device); stage = 0; _activate(model, stage)
    size = 32
    images = torch.randn(2, 1, size, size, device=device)
    task_id = stage if scenario == "organ" else None
    logits = model(images, task_id)
    labels = torch.full((2, size, size), IGNORE_INDEX, dtype=torch.long, device=device)
    labels[:, 4:7, 4:24] = 0; labels[:, 14:18, 12:20] = 1
    loss = supervision_loss("pce" if method.startswith("pce_") else "dense", logits, labels if method.startswith("pce_") else labels.clamp_min(0))
    loss.backward()
    result = {"status": "PASS", "scenario": scenario, "method": method, "backbone": type(model.backbone).__name__, "shape": list(logits.shape), "finite": bool(torch.isfinite(loss)), "loss": float(loss.detach())}
    if method == "pce_ewc":
        loader = DataLoader(_MemorySparse(images.detach().cpu(), labels.detach().cpu()), batch_size=1)
        fisher, summary = estimate_fisher(model, loader, device, task_id=task_id, max_batches=2)
        result["fisher"] = asdict(summary); result["fisher_nonnegative"] = all(bool((x >= 0).all()) for x in fisher.values())
    return result


def _tiny_indices(dense: DenseDataset, classes: tuple[int, ...], count: int = 16) -> list[int]:
    ids = []
    for index in range(len(dense)):
        _, label = dense[index]
        if all(bool((label == value).any()) for value in classes): ids.append(index)
        if len(ids) == count: break
    if len(ids) < count: raise RuntimeError(f"only {len(ids)} coverage slices for classes {classes}")
    return ids


def _tiny_score(model, loader, device, task_id, classes):
    model.eval(); prediction=[]; target=[]
    with torch.no_grad():
        for images, labels in loader:
            prediction.append(model(images.to(device), task_id).argmax(1).cpu().numpy()); target.append(labels.numpy())
    prediction, target = np.concatenate(prediction), np.concatenate(target); values=[]
    for value in classes:
        p, t = prediction == value, target == value
        values.append(float((2 * np.logical_and(p, t).sum() + 1e-5) / (p.sum() + t.sum() + 1e-5)))
    return float(np.mean(values)), values


def _known_pixel_fit(model, loader, device, task_id, classes):
    model.eval(); correct=known=0; predicted_current=False
    with torch.no_grad():
        for images,labels in loader:
            labels=labels.to(device); prediction=model(images.to(device),task_id).argmax(1); mask=labels!=IGNORE_INDEX; correct+=int((prediction[mask]==labels[mask]).sum()); known+=int(mask.sum()); predicted_current=predicted_current or any(bool((prediction==value).any()) for value in classes)
    return correct/max(1,known),predicted_current,known


def run_tiny_gate(options: RunOptions, task_code: str, supervision: str, steps: int = 700) -> dict:
    tasks = tasks_for(options.scenario); task = next(x for x in tasks if x.code == task_code); seed_all(options.seed)
    dense = DenseDataset(dataset_path(options.data_root, task), "train", task.label_shift if options.scenario == "class" else 0)
    classes = _classes(options.scenario, task); indices = _tiny_indices(dense, classes); eval_loader = DataLoader(Subset(dense, indices), batch_size=4, shuffle=False)
    sparse_contract=None
    if supervision == "dense": train = Subset(dense, indices)
    else:
        sparse = SparseDataset(dataset_path(options.data_root, task), _annotation_path(options.sparse_root, options.scenario, task.code, options.seed))
        train = Subset(sparse, indices)
        if getattr(sparse, "exposes_dense", None) is not False: raise AssertionError("sparse loader exposed dense labels")
        values=sorted(np.unique(sparse.annotations[indices]).astype(int).tolist()); required={IGNORE_INDEX,0,*classes}; sparse_contract={"values":values,"has_unknown":IGNORE_INDEX in values,"has_background":0 in values,"has_all_current_foreground":set(classes)<=set(values)}
        if not all(sparse_contract[key] for key in ("has_unknown","has_background","has_all_current_foreground")): raise RuntimeError("sparse label contract failed")
    train_loader = DataLoader(train, batch_size=4, shuffle=False); batches = list(train_loader)
    model = build_model(options.scenario).to(options.device); _activate(model, task.index); task_id = task.index if options.scenario == "organ" else None
    optimizer = torch.optim.Adam([p for p in model.parameters() if p.requires_grad], lr=1e-3)
    initial_loss = None; log = []; started = time.monotonic()
    for step in range(1, steps + 1):
        model.train(); images, labels = batches[(step - 1) % len(batches)]; images, labels = images.to(options.device), labels.to(options.device)
        logits = model(images, task_id); loss = supervision_loss(supervision, logits, labels); optimizer.zero_grad(set_to_none=True); loss.backward(); optimizer.step()
        if initial_loss is None: initial_loss = float(loss.detach())
        if step == 1 or step % 25 == 0:
            score, per_class = _tiny_score(model, eval_loader, options.device, task_id, classes)
            row = {"step": step, "loss": float(loss.detach()), "aggregate_fg_dice": score, "per_class": per_class}
            if supervision=="pce": row["known_pixel_accuracy"],row["current_fg_nonempty"],row["known_pixels"]=_known_pixel_fit(model,train_loader,options.device,task_id,classes)
            log.append(row)
            if supervision=="dense" and score>=.95 and float(loss.detach())<initial_loss: break
            if supervision=="pce" and row["known_pixel_accuracy"]>=.98 and row["current_fg_nonempty"] and float(loss.detach())<initial_loss: break
    final = log[-1]
    passed = (final["aggregate_fg_dice"]>=.95 if supervision=="dense" else final["known_pixel_accuracy"]>=.98 and final["current_fg_nonempty"]) and final["loss"]<initial_loss and np.isfinite(final["loss"])
    result = {"status": "PASS" if passed else "FAIL", "scenario": options.scenario, "task": task.code, "supervision": supervision, "seed": options.seed, "indices": indices, "training_batches":len(batches), "criterion":"dense aggregate FG Dice >= 0.95" if supervision=="dense" else "known-pixel accuracy >= 0.98 with nonempty current FG", "initial_loss": initial_loss, "final": final, "runtime_seconds": time.monotonic() - started, "sparse_loader_exposes_dense": None if supervision == "dense" else False, "sparse_label_contract":sparse_contract, "log": log}
    output = options.runs_root / "gates" / f"{options.scenario}_{task.code}_{supervision}_seed{options.seed}.json"; _json(output, result)
    if not passed: raise RuntimeError(f"tiny gate failed: {output}")
    return result


def _load_parent(model, path: Path) -> None:
    value = torch.load(path, map_location="cpu", weights_only=False)
    state = value["model"] if "model" in value else value
    model.load_state_dict(state)
    return value


def _write_matrix(path: Path, matrix: np.ndarray, tasks) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.writer(stream); writer.writerow(["after_stage"] + [x.code for x in tasks])
        for index, row in enumerate(matrix): writer.writerow([tasks[index].code] + ["" if np.isnan(x) else f"{x:.10f}" for x in row])


def run_independent_task(options: RunOptions, task_code: str, source_root: Path) -> dict:
    if options.method != "pce_ft": raise ValueError("independent references use pce_ft")
    tasks=tasks_for(options.scenario); task=next(item for item in tasks if item.code==task_code); seed_all(options.seed); model=build_model(options.scenario).to(options.device); _activate(model,task.index); task_id=task.index if options.scenario=="organ" else None
    run_id=options.run_id or f"medseg_{options.scenario}_independent_{task.code}_seed{options.seed}_{time.strftime('%Y%m%dT%H%M%SZ',time.gmtime())}"; run_dir=options.runs_root/"references"/options.scenario/run_id; run_dir.mkdir(parents=True,exist_ok=False); controller=CheckpointController(run_dir)
    manifest=_manifest(options,run_id,(task,),source_root); manifest.update(reference_type="independent_from_scratch",task=task.code); _json(run_dir/"run_manifest.json",manifest)
    train=SparseDataset(dataset_path(options.data_root,task),_annotation_path(options.sparse_root,options.scenario,task.code,options.seed)); optimizer=_optimizer(model,options); scheduler=torch.optim.lr_scheduler.StepLR(optimizer,step_size=options.lr_decay_epoch,gamma=options.lr_decay_rate); started=time.monotonic()
    for epoch in range(options.epochs):
        model.train(); total=known=0; generator=torch.Generator().manual_seed(options.seed+task.index*100_000+epoch); loader=DataLoader(train,batch_size=options.batch_size,shuffle=True,generator=generator,num_workers=0)
        for images,labels in loader:
            images,labels=images.to(options.device),labels.to(options.device); optimizer.zero_grad(set_to_none=True); loss=supervision_loss("pce",model(images,task_id),labels); loss.backward(); optimizer.step(); count=int((labels!=IGNORE_INDEX).sum()); total+=float(loss.detach())*count; known+=count
        scheduler.step(); _append(run_dir/"train.jsonl",{"epoch":epoch,"loss":total/known,"lr":optimizer.param_groups[0]["lr"],"finite":True}); controller.save(model,optimizer,scheduler,task.index,epoch,[],reference_task=task.code)
        if controller.should_stop(): manifest.update(status="stopped_after_checkpoint",last_complete_epoch=epoch,checkpoint_sha256=file_sha256(run_dir/"last.pt")); _json(run_dir/"run_manifest.json",manifest); train.close(); return manifest
    dense=DenseDataset(dataset_path(options.data_root,task),"test",task.label_shift if options.scenario=="class" else 0); score=evaluate(model,DataLoader(dense,batch_size=options.batch_size),dense.patient_info,options.device,task_id,_classes(options.scenario,task)); dense.close(); train.close(); summary={"score":score["benchmark_mean"],"per_class":score["per_class"],"runtime_seconds":time.monotonic()-started}; _json(run_dir/"summary.json",summary); manifest.update(status="complete",validity="valid_final_backbone_reference",summary=summary,last_checkpoint_sha256=file_sha256(run_dir/"last.pt")); _json(run_dir/"run_manifest.json",manifest); return manifest


def run_sequence(options: RunOptions, source_root: Path) -> dict:
    if options.method.startswith("enhanced_"): raise RuntimeError("blocked_by_static_gate")
    if options.seed != 42: raise RuntimeError("seeds_43_44_blocked_until_seed42_complete")
    if options.method not in {"dense_ft", "dense_ewc", "pce_ft", "pce_ewc", "pce_si"}: raise ValueError(options.method)
    supervision = "pce" if options.method.startswith("pce_") else "dense"; tasks = tasks_for(options.scenario); seed_all(options.seed)
    run_id = options.run_id or f"medseg_{options.scenario}_{options.method}_seed{options.seed}_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    run_dir = options.resume.parent if options.resume else options.runs_root / options.scenario / run_id
    run_dir.mkdir(parents=True, exist_ok=bool(options.resume))
    model = build_model(options.scenario).to(options.device); ewc = OnlineEWC(1.0, .1) if options.method.endswith("ewc") else None; si = SynapticIntelligence(5.0, 1.0) if options.method.endswith("si") else None
    if options.resume and (run_dir / "run_manifest.json").exists(): manifest = json.loads((run_dir / "run_manifest.json").read_text()); manifest["status"] = "running_resumed"
    else: manifest = _manifest(options, run_id, tasks, source_root)
    _json(run_dir / "run_manifest.json", manifest); controller = CheckpointController(run_dir)
    matrix = np.full((len(tasks), len(tasks)), np.nan); random_scores = []
    start_stage = 0; resume_value = None; parent_value = None
    if options.resume:
        resume_value = torch.load(options.resume, map_location="cpu", weights_only=False); start_stage = int(resume_value["stage"])
        for stage in range(start_stage + 1): _activate(model, stage)
        model.load_state_dict(resume_value["model"]); matrix = np.asarray(resume_value.get("matrix", matrix), dtype=float)
        if ewc is not None and resume_value.get("ewc") is not None: ewc.load_state_dict(resume_value["ewc"],options.device)
        if si is not None and resume_value.get("si") is not None: si.load_state_dict(resume_value["si"],options.device)
    elif options.stage1_parent:
        _activate(model, 0); parent_value=_load_parent(model, options.stage1_parent); start_stage = 1
    if options.scenario=="domain":
        if resume_value and resume_value.get("random_scores") is not None: random_scores=list(resume_value["random_scores"])
        elif parent_value and parent_value.get("random_scores") is not None: random_scores=list(parent_value["random_scores"])
        elif options.stage1_parent: raise ValueError("Domain stage-1 parent is missing the random baseline")
        else:
            for task in tasks:
                dense = DenseDataset(dataset_path(options.data_root, task), "test"); loader = DataLoader(dense, batch_size=options.batch_size); random_scores.append(evaluate(model, loader, dense.patient_info, options.device, None, (1,))["benchmark_mean"]); dense.close()
    started = time.monotonic(); stage_rows=list(resume_value.get("rows",[])) if resume_value else []; fisher_path=run_dir/"fisher_summary.json"; fisher_rows=json.loads(fisher_path.read_text()) if resume_value and fisher_path.exists() else []
    if torch.cuda.is_available() and str(options.device).startswith("cuda"): torch.cuda.reset_peak_memory_stats(options.device)
    if options.stage1_parent:
        evaluated={}; indices=range(len(tasks)) if options.scenario=="domain" else range(1)
        for index in indices:
            item=tasks[index]; dense = DenseDataset(dataset_path(options.data_root, item), "test", item.label_shift if options.scenario == "class" else 0); score = evaluate(model, DataLoader(dense, batch_size=options.batch_size), dense.patient_info, options.device, _model_task(options.scenario, index), _classes(options.scenario, item)); matrix[0, index] = score["benchmark_mean"]; evaluated[item.code]=score; dense.close()
        first=tasks[0]; stage_rows.append({"stage":0,"task":first.code,"current_task_dice":matrix[0,0],"evaluated":evaluated,"source":"shared_stage1_parent"}); shutil.copyfile(options.stage1_parent,run_dir/"stage_1.pt"); _json(run_dir/"stage_1_checkpoint.json",{"sha256":file_sha256(run_dir/"stage_1.pt"),"size_bytes":(run_dir/"stage_1.pt").stat().st_size,"source":"shared_stage1_parent"})
        if ewc is not None:
            sparse = SparseDataset(dataset_path(options.data_root, first), _annotation_path(options.sparse_root, options.scenario, first.code, options.seed)); loader=DataLoader(sparse,batch_size=options.batch_size,shuffle=False,num_workers=0); fisher, summary=estimate_fisher(model,loader,options.device,_model_task(options.scenario,0),options.fisher_batches); ewc.consolidate(model,fisher); fisher_rows.append({"stage":0,"task":first.code,**asdict(summary)}); sparse.close()
    last_stage_done=-1
    for stage, task in enumerate(tasks):
        if stage < start_stage: continue
        if options.max_stage is not None and stage > options.max_stage: break
        _activate(model, stage)
        if options.scenario == "organ" and stage > 0: model.freeze_stage(stage - 1)
        train_set, train_loader, val_set, test_set = _loaders(options, task, supervision)
        optimizer = _optimizer(model, options); scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=options.lr_decay_epoch, gamma=options.lr_decay_rate)
        first_epoch = 0
        if resume_value is not None and stage == start_stage:
            optimizer.load_state_dict(resume_value["optimizer"]); scheduler.load_state_dict(resume_value["scheduler"]); first_epoch = int(resume_value["epoch"]) + 1
            random.setstate(resume_value["python_rng"]); np.random.set_state(resume_value["numpy_rng"]); torch.set_rng_state(resume_value["torch_rng"])
            if torch.cuda.is_available() and resume_value.get("cuda_rng") is not None: torch.cuda.set_rng_state_all(resume_value["cuda_rng"])
        if si is not None: si.begin(model)
        task_id = stage if options.scenario == "organ" else None
        completed_resume=resume_value is not None and stage==start_stage and (resume_value.get("stage_complete") or len(resume_value.get("rows",[]))>stage)
        if completed_resume:
            stage_path=run_dir/f"stage_{stage+1}.pt"; shutil.copyfile(run_dir/"last.pt",stage_path); _json(run_dir/f"stage_{stage+1}_checkpoint.json",{"sha256":file_sha256(stage_path),"size_bytes":stage_path.stat().st_size,"source":"completed_stage_resume"}); [value.close() for value in (train_set,val_set,test_set)]; last_stage_done=stage; resume_value=None; continue
        for epoch in range(first_epoch, options.epochs):
            model.train(); total = known = 0; epoch_generator=torch.Generator().manual_seed(options.seed + stage*100_000 + epoch); epoch_loader=DataLoader(train_set,batch_size=options.batch_size,shuffle=True,generator=epoch_generator,num_workers=0)
            for images, labels in epoch_loader:
                images, labels = images.to(options.device), labels.to(options.device); optimizer.zero_grad(set_to_none=True)
                loss = supervision_loss(supervision, model(images, task_id), labels)
                if ewc is not None: loss = loss + ewc.penalty(model)
                if si is not None: loss = loss + si.penalty(model)
                if not torch.isfinite(loss): raise FloatingPointError("non-finite training loss")
                loss.backward()
                if si is not None: si.accumulate(model, optimizer.param_groups[0]["lr"])
                optimizer.step(); count = int((labels != IGNORE_INDEX).sum()) if supervision == "pce" else int(labels.numel()); total += float(loss.detach()) * count; known += count
            scheduler.step(); row = {"stage": stage, "task": task.code, "epoch": epoch, "loss": total / known, "lr": optimizer.param_groups[0]["lr"], "finite": True}; _append(run_dir / "train.jsonl", row)
            controller.save(model, optimizer, scheduler, stage, epoch, stage_rows, ewc, si, matrix=matrix,random_scores=random_scores,stage_complete=False)
            if controller.should_stop():
                manifest.update(status="stopped_after_checkpoint", last_complete_stage=stage, last_complete_epoch=epoch, checkpoint_sha256=file_sha256(run_dir / "last.pt")); _json(run_dir / "run_manifest.json", manifest); return manifest
        validation=evaluate(model,DataLoader(val_set,batch_size=options.batch_size),val_set.patient_info,options.device,task_id,_classes(options.scenario,task))
        _append(run_dir/"validation.jsonl",{"stage":stage,"task":task.code,"fixed_last_epoch":options.epochs-1,"score":validation})
        evaluation_indices = range(len(tasks)) if options.scenario == "domain" else range(stage + 1)
        evaluated = {}
        for index in evaluation_indices:
            item = tasks[index]; dense = DenseDataset(dataset_path(options.data_root, item), "test", item.label_shift if options.scenario == "class" else 0); loader = DataLoader(dense, batch_size=options.batch_size)
            score = evaluate(model, loader, dense.patient_info, options.device, _model_task(options.scenario, index), _classes(options.scenario, item)); matrix[stage, index] = score["benchmark_mean"]; evaluated[item.code] = score; dense.close()
        current = float(matrix[stage, stage]); stage_row={"stage":stage,"task":task.code,"current_task_dice":current,"validation_current":validation,"evaluated":evaluated}
        if options.scenario=="organ": stage_row.update(active_heads=len(model.heads),head_parameter_count=sum(p.numel() for head in model.heads.values() for p in head.parameters()))
        stage_rows.append(stage_row); _json(run_dir / "stage_rows.json", stage_rows)
        if options.scenario == "class" and stage == 1:
            gate_score=validation["benchmark_mean"]; gate={"status":"PASS" if gate_score >= options.current_gate_min else "FAIL","threshold":options.current_gate_min,"validation_current_task_dice":gate_score,"test_not_used_for_gate":True}; _json(run_dir / "STAGE2_CURRENT_LEARNING_GATE.json", gate)
            if gate["status"] != "PASS": raise RuntimeError("class_stage2_current_learning_gate_failed")
        if ewc is not None:
            fisher_set = train_set if supervision == "pce" else SparseDataset(dataset_path(options.data_root, task), _annotation_path(options.sparse_root, options.scenario, task.code, options.seed))
            fisher_loader=DataLoader(fisher_set,batch_size=options.batch_size,shuffle=False,num_workers=0); fisher, summary=estimate_fisher(model,fisher_loader,options.device,task_id,options.fisher_batches); ewc.consolidate(model,fisher); fisher_rows.append({"stage":stage,"task":task.code,**asdict(summary)}); _json(run_dir/"fisher_summary.json",fisher_rows)
            if fisher_set is not train_set: fisher_set.close()
        if si is not None: si.consolidate(model)
        controller.save(model,optimizer,scheduler,stage,options.epochs-1,stage_rows,ewc,si,matrix=matrix,random_scores=random_scores,stage_complete=True)
        stage_path=run_dir/f"stage_{stage+1}.pt"; shutil.copyfile(run_dir/"last.pt",stage_path)
        _json(run_dir/f"stage_{stage+1}_checkpoint.json",{"sha256":file_sha256(stage_path),"size_bytes":stage_path.stat().st_size})
        for value in (train_set,val_set,test_set): value.close()
        last_stage_done=stage
    refs = None
    if options.independent_scores: refs = json.loads(options.independent_scores.read_text())["scores"]
    summary = matrix_summary(matrix, options.scenario, refs, random_scores if options.scenario == "domain" else None)
    if options.scenario == "class" and last_stage_done==len(tasks)-1:
        whole_path=options.data_root/"MMWHS"/"whole_heart_test.h5"; whole=DenseDataset(whole_path,"test"); whole_score=evaluate(model,DataLoader(whole,batch_size=options.batch_size),whole.patient_info,options.device,None,tuple(range(1,8))); whole.close(); summary["WCD"]=whole_score["benchmark_mean"]; summary["WCD_per_class"]=whole_score["per_class"]; _json(run_dir/"whole_class_dice.json",whole_score)
    elif options.scenario=="class": summary["WCD"]=None
    runtime=time.monotonic()-started; state_bytes=sum(p.numel()*p.element_size() for p in model.parameters()) + (0 if ewc is None else ewc.nbytes()) + (0 if si is None else si.nbytes())
    summary.update(runtime_seconds=runtime,state_size_bytes=state_bytes,peak_gpu_bytes=(torch.cuda.max_memory_allocated(options.device) if torch.cuda.is_available() and str(options.device).startswith("cuda") else 0))
    if manifest.get("annotation_stats"): summary["mean_annotation_ratio"]=float(np.mean([x["total_annotation_ratio"] for x in manifest["annotation_stats"].values()]))
    if options.scenario == "organ": summary["head_count"] = len(model.heads); summary["head_growth"]=[row["active_heads"] for row in stage_rows if "active_heads" in row]; summary["head_parameter_count"] = sum(p.numel() for head in model.heads.values() for p in head.parameters())
    _write_matrix(run_dir/"performance_matrix.csv",matrix,tasks); _json(run_dir/"summary.json",summary)
    complete=last_stage_done==len(tasks)-1; manifest.update(status="complete" if complete else "partial_stage_complete",validity="valid_final_backbone_evidence" if complete else "engineering_smoke_only",summary=summary,completed_at=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),last_checkpoint_sha256=file_sha256(run_dir/"last.pt")); _json(run_dir/"run_manifest.json",manifest)
    return manifest

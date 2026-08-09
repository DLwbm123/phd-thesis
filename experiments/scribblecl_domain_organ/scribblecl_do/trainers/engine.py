from __future__ import annotations

import json
from pathlib import Path
import time

import torch
from torch import nn

from ..methods.current_supervision import supervision_loss
from ..metrics.segmentation import evaluate_patient_loader


def _append_jsonl(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True) + "\n")


def train_stage(
    model: nn.Module,
    loader,
    device: str,
    task_id: int | None,
    supervision: str,
    epochs: int,
    learning_rate: float,
    decay_epoch: int,
    decay_rate: float,
    train_log: Path,
    ewc=None,
    si=None,
) -> dict:
    if torch.cuda.is_available() and str(device).startswith("cuda"):
        torch.cuda.reset_peak_memory_stats(device)
    optimizer = torch.optim.SGD((p for p in model.parameters() if p.requires_grad), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=decay_epoch, gamma=decay_rate)
    if si is not None:
        si.begin(model)
    started = time.perf_counter()
    total_steps = 0
    last_loss = None
    for epoch in range(epochs):
        model.train()
        total = 0.0
        finite = True
        for images, target in loader:
            images, target = images.to(device), target.to(device)
            optimizer.zero_grad(set_to_none=True)
            logits = model(images) if task_id is None else model(images, task_id)
            current = supervision_loss(supervision, logits, target)
            penalty = current.new_zeros(())
            if ewc is not None:
                penalty = penalty + ewc.penalty(model)
            if si is not None:
                penalty = penalty + si.penalty(model)
            loss = current + penalty
            if not bool(torch.isfinite(loss)):
                finite = False
                raise FloatingPointError("non-finite training loss")
            loss.backward()
            if si is not None:
                si.accumulate_after_backward(model, optimizer.param_groups[0]["lr"])
            optimizer.step()
            total += float(loss.detach())
            total_steps += 1
        scheduler.step()
        last_loss = total / max(1, len(loader))
        _append_jsonl(
            train_log,
            {
                "epoch": epoch,
                "loss": last_loss,
                "lr": optimizer.param_groups[0]["lr"],
                "finite": finite,
                "task_id": task_id,
            },
        )
    elapsed = time.perf_counter() - started
    peak = torch.cuda.max_memory_allocated(device) if torch.cuda.is_available() and str(device).startswith("cuda") else 0
    return {"seconds": elapsed, "steps": total_steps, "last_loss": last_loss, "peak_memory_bytes": int(peak)}


def evaluate_matrix_row(model, tasks, dataset_factory, device: str, scenario: str, stage: int, batch_size: int = 8) -> tuple[list[float], list[dict]]:
    from torch.utils.data import DataLoader

    values: list[float] = []
    details: list[dict] = []
    for index, task in enumerate(tasks):
        if scenario == "organ" and index > stage:
            values.append(float("nan"))
            details.append({"status": "future_head_inactive"})
            continue
        dataset = dataset_factory(task, "test")
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=0)
        metric = evaluate_patient_loader(model, loader, dataset.patient_info, device, None if scenario == "domain" else index)
        values.append(float(metric["benchmark_mean"]))
        details.append(metric)
        dataset.close()
    return values, details

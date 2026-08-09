from __future__ import annotations

import numpy as np
import torch

from ..data.h5_dataset import patient_ranges


def binary_patient_dice(prediction: np.ndarray, target: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    pred = np.asarray(prediction)
    true = np.asarray(target)
    scores = []
    for class_id in (0, 1):
        p, t = pred == class_id, true == class_id
        scores.append((2.0 * np.logical_and(p, t).sum() + eps) / (p.sum() + t.sum() + eps))
    return np.asarray(scores, dtype=np.float64)


@torch.no_grad()
def evaluate_patient_loader(model, loader, patient_info, device, task_id: int | None = None) -> dict:
    model.eval()
    predictions, targets = [], []
    for images, dense in loader:
        images = images.to(device)
        logits = model(images) if task_id is None else model(images, task_id)
        predictions.append(logits.argmax(1).cpu().numpy())
        targets.append(dense.numpy())
    pred, target = np.concatenate(predictions), np.concatenate(targets)
    ranges = patient_ranges(patient_info)
    per_patient = np.stack([binary_patient_dice(pred[a:b], target[a:b]) for a, b in ranges])
    return {
        "benchmark_mean": float(per_patient.mean()),
        "background": float(per_patient[:, 0].mean()),
        "foreground": float(per_patient[:, 1].mean()),
        "per_patient": per_patient.tolist(),
        "prediction_fg_fraction": float((pred == 1).mean()),
    }

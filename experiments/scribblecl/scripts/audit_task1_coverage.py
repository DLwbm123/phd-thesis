#!/usr/bin/env python3
"""Read-only validation audit for completed Task-1 coverage runs.

This never opens test labels and never mutates a run directory.  Dense train
labels are read only to classify already-generated zero-supervision slices.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import h5py
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch.utils.data import DataLoader

from scribblecl.data import MMWHS
from scribblecl.losses import masked_logits
from scribblecl.metrics import dice
from scribblecl.model import ResUNet32

CLASS_NAMES = {1: "MYO", 2: "LV", 3: "LA"}
RUNS = (("Dense", "dense"), ("B1", "pce"), ("B1", "zs"),
        ("B2", "pce"), ("B2", "zs"), ("B3", "pce"), ("B3", "zs"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def finite_checkpoint(path: Path) -> bool:
    state = torch.load(path, map_location="cpu")["model"]
    return all(torch.isfinite(v).all().item() for v in state.values())


def validation_metrics(checkpoint: Path, root: Path, device: torch.device):
    model = ResUNet32().to(device)
    model.load_state_dict(torch.load(checkpoint, map_location=device)["model"])
    model.eval(); scores = {c: [] for c in CLASS_NAMES}; positives = {c: 0 for c in CLASS_NAMES}
    nonempty = {c: 0 for c in CLASS_NAMES}; pred_pixels = {c: [] for c in CLASS_NAMES}
    with torch.no_grad():
        for x, y in DataLoader(MMWHS(str(root), 1, "val"), batch_size=4):
            pred = masked_logits(model(x.to(device)), (0, 1, 2, 3)).argmax(1).cpu().numpy()
            truth = y.numpy()
            for p, t in zip(pred, truth):
                for c in CLASS_NAMES:
                    scores[c].append(dice(p, t, c))
                    pred_pixels[c].append(int((p == c).sum()))
                    if (t == c).any():
                        positives[c] += 1
                        nonempty[c] += int((p == c).any())
    rows = []
    for c, name in CLASS_NAMES.items():
        rows.append({"class_id": c, "class_name": name, "validation_dice": float(np.mean(scores[c])),
                     "positive_validation_cases": positives[c], "nonempty_predictions_on_positive_cases": nonempty[c],
                     "nonempty_prediction_rate": nonempty[c] / positives[c] if positives[c] else float("nan"),
                     "mean_predicted_pixels": float(np.mean(pred_pixels[c]))})
    return rows, float(np.mean([x["validation_dice"] for x in rows]))


def train_summary(path: Path):
    records = [json.loads(x) for x in path.read_text().splitlines() if x.strip()]
    values = np.array([r["loss"] for r in records], dtype=float)
    return {"final_epoch": int(records[-1]["epoch"]), "final_train_loss": float(values[-1]),
            "last20_train_loss_mean": float(values[-20:].mean()), "last20_train_loss_std": float(values[-20:].std()),
            "nonfinite_train_loss": bool((~np.isfinite(values)).any())}


def coverage_rows(path: Path):
    x = json.loads(path.read_text())["stages"]["1"]
    return [{"class_id": c, "class_name": CLASS_NAMES[int(c)], **x[c]} for c in ("1", "2", "3")]


def zero_slice_audit(mmwhs_root: Path, scribble: Path, output: Path):
    with h5py.File(mmwhs_root / "myo_lv_la.h5", "r") as h:
        dense = h["train_labels"][:].transpose(2, 0, 1)
    sparse = np.load(scribble)["scribbles"]
    rows = []
    for i, (y, s) in enumerate(zip(dense, sparse)):
        n_active = int((y > 0).sum()); n_scribble = int((s != -100).sum())
        if n_scribble == 0:
            rows.append({"slice_id": i, "active_gt_pixels": n_active, "scribble_pixels": n_scribble,
                         "category": "A_true_negative" if n_active == 0 else "B_missing_positive_scribble"})
    with output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=("slice_id", "active_gt_pixels", "scribble_pixels", "category"))
        writer.writeheader(); writer.writerows(rows)
    return rows


def make_overlays(mmwhs_root: Path, figure_dir: Path):
    figure_dir.mkdir(parents=True, exist_ok=True)
    with h5py.File(mmwhs_root / "myo_lv_la.h5", "r") as h:
        imgs = h["val_images"][:].transpose(2, 0, 1)
        labels = h["val_labels"][:].transpose(2, 0, 1)
    for c, name in CLASS_NAMES.items():
        choices = np.argsort([(x == c).sum() for x in labels])[-3:][::-1]
        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        for ax, idx in zip(axes, choices):
            ax.imshow(imgs[idx], cmap="gray")
            ax.contour(labels[idx] == c, levels=[0.5], colors=["lime"], linewidths=1.4)
            ax.set_title(f"val slice {int(idx)}; pixels={(labels[idx] == c).sum()}"); ax.axis("off")
        fig.suptitle(f"Class ID {c}: {name}; green contour is validation GT")
        fig.tight_layout(); fig.savefig(figure_dir / f"class_{c}_{name}.png", dpi=160); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mmwhs-root", required=True); ap.add_argument("--coverage-runs", required=True)
    ap.add_argument("--coverage-outputs", required=True); ap.add_argument("--output", required=True)
    ap.add_argument("--code-commit", required=True); ap.add_argument("--device", default="cuda:0")
    a = ap.parse_args(); root = Path(a.mmwhs_root); runs_root = Path(a.coverage_runs)
    outputs = Path(a.coverage_outputs); out = Path(a.output); out.mkdir(parents=True, exist_ok=True)
    device = torch.device(a.device); run_rows = []; class_rows = []; curve_rows = []
    for budget, method in RUNS:
        run_dir = runs_root / budget / f"{method}_seed42_stage1"
        manifest = json.loads((run_dir / "run_manifest.json").read_text())
        checkpoint, config, train = run_dir / "best.pt", run_dir / "config_resolved.yaml", run_dir / "train.jsonl"
        summary = train_summary(train); metrics, mean = validation_metrics(checkpoint, root, device)
        budget_coverage = [{"class_id": c, "class_name": CLASS_NAMES[c], "foreground_coverage": 1.0,
                            "scribble_pixels": "NA", "dense_foreground_pixels": "NA"} for c in CLASS_NAMES] if budget == "Dense" else coverage_rows(outputs / "scribbles/42" / budget / "coverage_summary.json")
        cv = {int(r["class_id"]): r for r in budget_coverage}
        for r in metrics:
            class_rows.append({"run_id": manifest["run_id"], "method": method, "budget": budget, "seed": 42,
                               **r, **cv[r["class_id"]]})
        for record in [json.loads(x) for x in train.read_text().splitlines() if x.strip()]:
            curve_rows.append({"run_id": manifest["run_id"], "method": method, "budget": budget,
                               "epoch": record["epoch"], "train_loss": record["loss"]})
        run_rows.append({"run_id": manifest["run_id"], "method": method, "budget": budget, "seed": 42,
                         "completion_status": manifest["completion_status"], "checkpoint_selection": "final_epoch_only",
                         "best_epoch": "NA_not_saved", "best_validation_mean_dice": "NA_not_evaluated_per_epoch",
                         "final_validation_mean_dice": mean, "validation_loss": "NA_not_logged",
                         "zs_loss_components": "NA_not_logged" if method == "zs" else "not_applicable",
                         "gradient_norm": "NA_not_logged", "checkpoint_sha256": sha256(checkpoint),
                         "config_sha256": sha256(config), "code_commit": a.code_commit,
                         "checkpoint_all_finite": finite_checkpoint(checkpoint), **summary})
    def write(name, rows):
        with (out / name).open("w", newline="") as f:
            fields = list(dict.fromkeys(key for row in rows for key in row))
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    write("task1_coverage_runs.csv", run_rows); write("task1_coverage_classwise.csv", class_rows)
    write("task1_coverage_curves.csv", curve_rows)
    write("task1_coverage_summary.csv", [{k: r[k] for k in ("run_id", "method", "budget", "seed", "final_validation_mean_dice", "final_epoch", "last20_train_loss_mean", "last20_train_loss_std", "completion_status")} for r in run_rows])
    zero = zero_slice_audit(root, outputs / "scribbles/42/B1/stage1.npz", out / "zero_supervision_slice_audit.csv")
    make_overlays(root, out / "figures/label_semantics_audit")
    (out / "audit_status.json").write_text(json.dumps({"code_commit": a.code_commit, "zero_slices": len(zero),
        "missing_positive_scribble_slices": sum(x["category"] == "B_missing_positive_scribble" for x in zero),
        "selection_split": "validation_only", "test_set_opened": False}, indent=2))

if __name__ == "__main__":
    main()

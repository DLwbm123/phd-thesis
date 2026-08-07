"""Validation-only MMWHS Task-1 runner for the paper-compatible ZS ladder."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import time
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader

from .data import MMWHS
from .gate import checkpoint_selection_score
from .losses import soft_partial_cross_entropy
from .metrics import benchmark_patient_summary, dice
from .model import ResUNet32
from .protocol import IGNORE_INDEX, stage
from .zs_components import (
    LAMBDA_GLOBAL,
    LAMBDA_SHAPE,
    LAMBDA_SPATIAL,
    OCCLUSION_SIZE,
    PUZZLEMIX_CONFIG,
    SPATIAL_WARMUP_EPOCH,
    active_probabilities,
    apply_occlusion,
    apply_shared_geometry,
    classwise_shape_loss,
    component_gradient_norm,
    probability_pce,
    puzzlemix_native,
    spatial_enabled,
    spatial_prior_loss,
    symmetric_global_consistency,
)


FORMAL_LEVELS = ("A0", "A", "C1", "C2", "C3", "D", "E")
LEVEL_INDEX = {name: index for index, name in enumerate(FORMAL_LEVELS)}
SHAPE_ELIGIBLE_CLASSES = (1, 2)
COMPONENTS = ("pce_unmixed", "pce_mixed", "global", "shape", "spatial")


def file_sha(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def append_json(path, value):
    with open(path, "a") as stream:
        stream.write(json.dumps(value, sort_keys=True) + "\n")


def evaluate(model, root, device):
    dataset = MMWHS(root, 1, "val")
    allowed = (0, 1, 2, 3)
    predictions, targets = [], []
    model.eval()
    with torch.no_grad():
        for image, target in DataLoader(dataset, batch_size=8, shuffle=False):
            prediction = active_probabilities(model(image.to(device)), allowed).argmax(1)
            predictions.append(prediction.cpu().numpy())
            targets.append(target.numpy())
    prediction = np.concatenate(predictions)
    target = np.concatenate(targets)
    summary = benchmark_patient_summary(
        prediction, target, dataset.patient_info, allowed
    )
    summary["benchmark_mean"] = summary["benchmark_mean_bg_included"]
    summary["all_slice"] = {
        class_id: float(np.mean([dice(p, t, class_id) for p, t in zip(prediction, target)]))
        for class_id in allowed[1:]
    }
    summary["positive_slice"] = {
        class_id: float(
            np.mean(
                [dice(p, t, class_id) for p, t in zip(prediction, target) if (t == class_id).any()]
            )
        )
        for class_id in allowed[1:]
    }
    summary["aggregate_volume"] = {
        class_id: dice(prediction, target, class_id) for class_id in allowed
    }
    summary["background_fraction"] = float((prediction == 0).mean())
    summary["foreground_fraction"] = float((prediction > 0).mean())
    summary["prediction_class_fraction"] = {
        class_id: float((prediction == class_id).mean()) for class_id in allowed
    }
    summary["nonempty_prediction_rate"] = {
        class_id: float(np.mean([(p == class_id).any() for p in prediction]))
        for class_id in allowed[1:]
    }
    return summary


def parser():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--level", choices=FORMAL_LEVELS, required=True)
    argument_parser.add_argument("--seed", type=int, default=42)
    argument_parser.add_argument("--mmwhs-root", required=True)
    argument_parser.add_argument("--scribble", required=True)
    argument_parser.add_argument("--output-root", required=True)
    argument_parser.add_argument("--optimizer", choices=("sgd",), default="sgd")
    argument_parser.add_argument("--lr", type=float, default=0.004)
    argument_parser.add_argument("--epochs", type=int, default=150)
    argument_parser.add_argument("--batch-size", type=int, default=8)
    argument_parser.add_argument("--device", default="cuda:0")
    argument_parser.add_argument("--max-batches", type=int)
    argument_parser.add_argument("--grad-every", type=int, default=10)
    argument_parser.add_argument("--resume", action="store_true")
    argument_parser.add_argument("--source-commit", required=True)
    argument_parser.add_argument(
        "--run-kind", choices=("smoke", "diagnostic20", "full"), default="full"
    )
    argument_parser.add_argument("--force-spatial-smoke", action="store_true")
    return argument_parser


def component_seed(seed, epoch, batch_index, offset=0):
    return seed * 1_000_000 + epoch * 1_000 + batch_index + offset


def main():
    arguments = parser().parse_args()
    if arguments.seed != 42:
        raise ValueError("static fidelity gate is locked to seed 42")
    if arguments.lr != 0.004:
        raise ValueError("formal ladder is locked to SGD lr=0.004")
    if arguments.run_kind == "diagnostic20" and arguments.epochs != 20:
        raise ValueError("diagnostic20 requires exactly 20 epochs")
    if arguments.force_spatial_smoke and (
        arguments.run_kind != "smoke" or arguments.level != "E"
    ):
        raise ValueError("force-spatial-smoke is allowed only for the E smoke test")

    os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
    random.seed(arguments.seed)
    np.random.seed(arguments.seed)
    torch.manual_seed(arguments.seed)
    torch.cuda.manual_seed_all(arguments.seed)
    torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False

    device = torch.device(arguments.device)
    model = ResUNet32().to(device)
    initial_vector = torch.cat(
        [parameter.detach().cpu().flatten() for parameter in model.parameters()]
    )
    initial_sha = hashlib.sha256(initial_vector.numpy().tobytes()).hexdigest()
    output = (
        Path(arguments.output_root)
        / f"static_{arguments.level}_sgd_seed42_{arguments.run_kind}"
    )
    output.mkdir(parents=True, exist_ok=True)

    level_index = LEVEL_INDEX[arguments.level]
    manifest = {
        "run_id": output.name,
        "scope": "MMWHS_Task1_validation_only",
        "training_dataset": "MMWHS_sparse_labels_only",
        "dense_training_labels_accessed": False,
        "future_class_logits_excluded": True,
        "formal_level": arguments.level,
        "formal_level_order": list(FORMAL_LEVELS),
        "seed": arguments.seed,
        "optimizer": "SGD",
        "lr": arguments.lr,
        "epochs": arguments.epochs,
        "batch_size": arguments.batch_size,
        "run_kind": arguments.run_kind,
        "scribble_sha256": file_sha(arguments.scribble),
        "initialization_sha256": initial_sha,
        "checkpoint_selection_metric": "foreground_patient_mean",
        "background_reported_but_not_selected": True,
        "common_augmentation": arguments.level != "A0",
        "puzzlemix": level_index >= LEVEL_INDEX["C1"],
        "occlusion": level_index >= LEVEL_INDEX["C2"],
        "global_consistency": level_index >= LEVEL_INDEX["C3"],
        "global_reverse_uses_transported_sources": True,
        "shape": level_index >= LEVEL_INDEX["D"],
        "em_spatial": level_index >= LEVEL_INDEX["E"],
        "shape_eligible_classes": list(SHAPE_ELIGIBLE_CLASSES),
        "shape_oracle_rule": "train_GT_mean_retention>=0.99_and_p95_slices_retention>=0.95",
        "warmup_epoch": SPATIAL_WARMUP_EPOCH,
        "loss_weights": {
            "pce_unmixed": 1.0,
            "pce_mixed": 1.0,
            "global": LAMBDA_GLOBAL,
            "shape": LAMBDA_SHAPE,
            "spatial": LAMBDA_SPATIAL,
        },
        "puzzlemix_config": PUZZLEMIX_CONFIG,
        "transport_execution": "per_sample_chunks_exactly_equivalent_to_released_batch_math",
        "occlusion_size": OCCLUSION_SIZE,
        "occlusion_target_mode": "background",
        "native_input_shape": [256, 256],
        "adversarial_noise_enabled": False,
        "force_spatial_smoke": arguments.force_spatial_smoke,
        "test_set_used": False,
        "source_commit": arguments.source_commit,
        "status": "running",
        "start_time": time.time(),
        "resume_count": 0,
    }
    manifest_path = output / "run_manifest.json"
    if arguments.resume and manifest_path.exists():
        previous = json.loads(manifest_path.read_text())
        manifest["start_time"] = previous.get("start_time", manifest["start_time"])
        manifest["resume_count"] = previous.get("resume_count", 0) + 1
        manifest["last_resume_time"] = time.time()
    manifest_path.write_text(json.dumps(manifest, indent=2))
    (output / "config_resolved.json").write_text(
        json.dumps(vars(arguments), indent=2)
    )

    train = MMWHS(arguments.mmwhs_root, 1, "train", arguments.scribble)
    allowed = (0,) + stage(1).active
    optimizer = torch.optim.SGD(model.parameters(), lr=arguments.lr)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=80, gamma=0.5)
    best = -1.0
    best_epoch = None
    start_epoch = 0
    if arguments.resume and (output / "last.pt").exists():
        checkpoint = torch.load(output / "last.pt", map_location="cpu", weights_only=False)
        model.load_state_dict(checkpoint["model"])
        optimizer.load_state_dict(checkpoint["optimizer"])
        scheduler.load_state_dict(checkpoint["scheduler"])
        for optimizer_state in optimizer.state.values():
            for key, value in optimizer_state.items():
                if torch.is_tensor(value):
                    optimizer_state[key] = value.to(device)
        best = checkpoint["best"]
        best_epoch = checkpoint["best_epoch"]
        start_epoch = checkpoint["epoch"] + 1

    for epoch in range(start_epoch, arguments.epochs):
        generator = torch.Generator().manual_seed(arguments.seed + epoch)
        loader = DataLoader(
            train,
            batch_size=arguments.batch_size,
            shuffle=True,
            generator=generator,
            num_workers=2,
            pin_memory=True,
        )
        model.train()
        weighted_values = {name: [] for name in COMPONENTS}
        raw_values = {name: [] for name in COMPONENTS}
        totals = []
        valid_counts = {name: [] for name in COMPONENTS}
        gradient_record = None

        for batch_index, (image, sparse) in enumerate(loader):
            image, sparse = image.to(device), sparse.to(device)
            seed = component_seed(arguments.seed, epoch, batch_index)
            if arguments.level != "A0":
                image, sparse, _ = apply_shared_geometry(image, sparse, seed)

            optimizer.zero_grad(set_to_none=True)
            zero = None
            extras = {}
            if level_index >= LEVEL_INDEX["C1"]:
                puzzle = puzzlemix_native(model, image, sparse, allowed, seed + 101)
                source_probabilities = puzzle["source_probabilities"]
                pce_unmixed = probability_pce(source_probabilities, sparse, allowed)
                mixed_image = puzzle["mixed_image"]
                mixed_target = puzzle["mixed_target"]
                keep = torch.ones_like(mixed_image[:, :1])
                if level_index >= LEVEL_INDEX["C2"]:
                    mixed_image, mixed_target, keep, boxes = apply_occlusion(
                        mixed_image, mixed_target, seed + 211, mode="background"
                    )
                    extras["occlusion_boxes"] = boxes
                mixed_probabilities = active_probabilities(model(mixed_image), allowed)
                pce_mixed = soft_partial_cross_entropy(mixed_probabilities, mixed_target)
                zero = source_probabilities.sum() * 0.0
                global_raw = zero
                if level_index >= LEVEL_INDEX["C3"]:
                    reverse_image = puzzle["reverse_image"] * keep
                    reverse_probabilities = active_probabilities(model(reverse_image), allowed)
                    global_raw = symmetric_global_consistency(
                        puzzle["expected_12"] * keep,
                        mixed_probabilities,
                        puzzle["expected_21"] * keep,
                        reverse_probabilities,
                    )
            else:
                source_probabilities = active_probabilities(model(image), allowed)
                zero = source_probabilities.sum() * 0.0
                pce_unmixed = probability_pce(source_probabilities, sparse, allowed)
                pce_mixed = zero
                global_raw = zero

            shape_result = {"loss": zero, "valid_pixel_count": 0}
            if level_index >= LEVEL_INDEX["D"]:
                shape_result = classwise_shape_loss(
                    source_probabilities, sparse, SHAPE_ELIGIBLE_CLASSES
                )
            spatial_result = {
                "loss": zero,
                "valid_pixel_count": 0,
                "em_ratios": None,
                "negative_counts": {},
            }
            if level_index >= LEVEL_INDEX["E"] and (
                spatial_enabled(epoch) or arguments.force_spatial_smoke
            ):
                spatial_result = spatial_prior_loss(
                    source_probabilities, image, sparse, allowed
                )

            raw_parts = {
                "pce_unmixed": pce_unmixed,
                "pce_mixed": pce_mixed,
                "global": global_raw,
                "shape": shape_result["loss"],
                "spatial": spatial_result["loss"],
            }
            weights = {
                "pce_unmixed": 1.0,
                "pce_mixed": 1.0,
                "global": LAMBDA_GLOBAL,
                "shape": LAMBDA_SHAPE,
                "spatial": LAMBDA_SPATIAL,
            }
            weighted_parts = {name: raw_parts[name] * weights[name] for name in COMPONENTS}
            total = sum(weighted_parts.values(), zero)
            if not torch.isfinite(total):
                manifest.update(
                    {
                        "status": "failed_nonfinite",
                        "failure_epoch": epoch,
                        "failure_batch": batch_index,
                        "end_time": time.time(),
                    }
                )
                manifest_path.write_text(json.dumps(manifest, indent=2))
                raise FloatingPointError(
                    f"nonfinite epoch={epoch} batch={batch_index} parts={raw_parts}"
                )

            if batch_index == 0 and epoch % arguments.grad_every == 0:
                gradient_record = {"epoch": epoch}
                for name in COMPONENTS:
                    gradient_record[f"{name}_raw"] = component_gradient_norm(
                        raw_parts[name], model
                    )
                    gradient_record[f"{name}_weighted"] = component_gradient_norm(
                        weighted_parts[name], model
                    )
                gradient_record["total"] = component_gradient_norm(total, model)

            total.backward()
            optimizer.step()
            for name in COMPONENTS:
                raw_values[name].append(float(raw_parts[name].detach()))
                weighted_values[name].append(float(weighted_parts[name].detach()))
            totals.append(float(total.detach()))
            valid_counts["pce_unmixed"].append(int(sparse.ne(IGNORE_INDEX).sum()))
            valid_counts["pce_mixed"].append(
                int(mixed_target[:, :-1].sum().detach())
                if level_index >= LEVEL_INDEX["C1"]
                else 0
            )
            valid_counts["global"].append(
                int(keep.sum().detach()) if level_index >= LEVEL_INDEX["C3"] else 0
            )
            valid_counts["shape"].append(shape_result["valid_pixel_count"])
            valid_counts["spatial"].append(spatial_result["valid_pixel_count"])
            if batch_index == 0 and spatial_result["em_ratios"] is not None:
                append_json(
                    output / "em_spatial.jsonl",
                    {
                        "epoch": epoch,
                        "em_ratios": spatial_result["em_ratios"].cpu().tolist(),
                        "negative_counts": spatial_result["negative_counts"],
                        "normalization": spatial_result["normalization"],
                    },
                )
            if batch_index == 0 and extras:
                append_json(output / "augmentation_trace.jsonl", {"epoch": epoch, **extras})
            if arguments.max_batches and batch_index + 1 >= arguments.max_batches:
                break

        scheduler.step()
        row = {"epoch": epoch, "lr": optimizer.param_groups[0]["lr"]}
        for name in COMPONENTS:
            row[f"{name}_raw"] = float(np.mean(raw_values[name]))
            row[f"{name}_weighted"] = float(np.mean(weighted_values[name]))
            row[f"{name}_valid_pixels"] = float(np.mean(valid_counts[name]))
        row["total"] = float(np.mean(totals))
        append_json(output / "train_components.jsonl", row)
        if gradient_record is not None:
            append_json(output / "gradient_norms.jsonl", gradient_record)

        validation = evaluate(model, arguments.mmwhs_root, device)
        validation["epoch"] = epoch
        append_json(output / "validation.jsonl", validation)
        append_json(
            output / "prediction_distribution.jsonl",
            {
                "epoch": epoch,
                "background_fraction": validation["background_fraction"],
                "foreground_fraction": validation["foreground_fraction"],
                "prediction_class_fraction": validation["prediction_class_fraction"],
                "nonempty_prediction_rate": validation["nonempty_prediction_rate"],
            },
        )
        score = checkpoint_selection_score(validation)
        improved = score > best
        if improved:
            best, best_epoch = score, epoch
        state = {
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "scheduler": scheduler.state_dict(),
            "epoch": epoch,
            "validation": validation,
            "best": best,
            "best_epoch": best_epoch,
            "checkpoint_selection_metric": "foreground_patient_mean",
        }
        torch.save(state, output / "last.pt.tmp")
        os.replace(output / "last.pt.tmp", output / "last.pt")
        if improved:
            torch.save(state, output / "best_val.pt.tmp")
            os.replace(output / "best_val.pt.tmp", output / "best_val.pt")

    manifest.update(
        {
            "status": "completed",
            "end_time": time.time(),
            "best_foreground_patient_mean": best,
            "best_epoch": best_epoch,
        }
    )
    manifest_path.write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

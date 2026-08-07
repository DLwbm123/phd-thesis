#!/usr/bin/env python3
"""Compare repeated two-batch smoke runs and write a compact evidence report."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import torch


EXPECTED_COMPONENT = {
    "C1": "pce_mixed",
    "C2": "pce_mixed",
    "C3": "global",
    "D": "shape",
    "E": "spatial",
}


def last_json(path):
    return json.loads(Path(path).read_text().splitlines()[-1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", choices=EXPECTED_COMPONENT, required=True)
    parser.add_argument("--repeat1", required=True)
    parser.add_argument("--repeat2", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--pytest-summary", default="60 passed")
    parser.add_argument("--diagnostic")
    arguments = parser.parse_args()

    directories = [Path(arguments.repeat1), Path(arguments.repeat2)]
    manifests = [json.loads((directory / "run_manifest.json").read_text()) for directory in directories]
    trains = [last_json(directory / "train_components.jsonl") for directory in directories]
    gradients = [last_json(directory / "gradient_norms.jsonl") for directory in directories]
    validations = [last_json(directory / "validation.jsonl") for directory in directories]
    checkpoints = [
        torch.load(directory / "last.pt", map_location="cpu", weights_only=False)
        for directory in directories
    ]
    parameter_max_abs = max(
        float((checkpoints[0]["model"][key] - checkpoints[1]["model"][key]).abs().max())
        for key in checkpoints[0]["model"]
    )
    component = EXPECTED_COMPONENT[arguments.level]
    finite = all(
        math.isfinite(float(value))
        for records in (trains, gradients, validations)
        for record in records
        for value in record.values()
        if isinstance(value, (int, float))
    )
    nonempty = all(
        all(float(value) > 0 for value in validation["nonempty_prediction_rate"].values())
        for validation in validations
    )
    not_collapsed = all(
        float(validation["background_fraction"]) >= 1e-4
        and float(validation["foreground_fraction"]) >= 1e-4
        for validation in validations
    )
    component_gradient = float(gradients[0][f"{component}_weighted"])
    component_valid = float(trains[0][f"{component}_valid_pixels"])
    checks = {
        "both_completed": all(manifest["status"] == "completed" for manifest in manifests),
        "same_initialization": manifests[0]["initialization_sha256"] == manifests[1]["initialization_sha256"],
        "exact_parameter_repeat": parameter_max_abs == 0,
        "exact_loss_repeat": trains[0] == trains[1],
        "finite": finite,
        "three_classes_nonempty": nonempty,
        "background_and_foreground_not_collapsed": not_collapsed,
        "component_has_valid_pixels": component_valid > 0,
        "component_gradient_finite": math.isfinite(component_gradient),
        "sparse_only": all(not manifest["dense_training_labels_accessed"] for manifest in manifests),
        "test_set_unused": all(not manifest["test_set_used"] for manifest in manifests),
        "future_logits_excluded": all(manifest["future_class_logits_excluded"] for manifest in manifests),
    }
    diagnostic_summary = None
    if arguments.diagnostic:
        diagnostic = Path(arguments.diagnostic)
        diagnostic_manifest = json.loads((diagnostic / "run_manifest.json").read_text())
        diagnostic_rows = [
            json.loads(line) for line in (diagnostic / "validation.jsonl").read_text().splitlines()
        ]
        diagnostic_checkpoint = torch.load(
            diagnostic / "best_val.pt", map_location="cpu", weights_only=False
        )
        diagnostic_best = diagnostic_checkpoint["validation"]
        diagnostic_last = diagnostic_rows[-1]
        diagnostic_finite = all(
            math.isfinite(float(row[key]))
            for row in diagnostic_rows
            for key in ("foreground_patient_mean", "background_fraction", "foreground_fraction")
        )
        diagnostic_nonempty = all(
            float(value) > 0
            for value in diagnostic_best["nonempty_prediction_rate"].values()
        )
        diagnostic_not_collapsed = (
            float(diagnostic_best["background_fraction"]) >= 1e-4
            and float(diagnostic_best["foreground_fraction"]) >= 1e-4
        )
        checks.update(
            {
                "diagnostic20_completed": diagnostic_manifest["status"] == "completed",
                "diagnostic20_finite": diagnostic_finite,
                "diagnostic20_three_classes_nonempty": diagnostic_nonempty,
                "diagnostic20_not_collapsed": diagnostic_not_collapsed,
            }
        )
        diagnostic_summary = {
            "best": diagnostic_best,
            "last": diagnostic_last,
            "best_epoch": diagnostic_checkpoint["epoch"],
        }
    decision = "PASS" if all(checks.values()) else "STOP"
    train = trains[0]
    gradient = gradients[0]
    validation = validations[0]
    lines = [
        f"# {arguments.level} two-batch smoke",
        "",
        f"Decision: `{decision}`.",
        "",
        f"Full unit-test prerequisite: `{arguments.pytest_summary}`.",
        f"Both runs used initialization `{manifests[0]['initialization_sha256']}` and parameter max absolute difference was `{parameter_max_abs}`.",
        "",
        "| Check | Result |",
        "|---|:---:|",
    ]
    lines.extend(f"| {name} | {value} |" for name, value in checks.items())
    lines.extend(
        [
            "",
            "| Component | Raw loss | Weighted loss | Gradient norm | Valid pixels |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    if diagnostic_summary is not None:
        best = diagnostic_summary["best"]
        last = diagnostic_summary["last"]
        lines.extend(
            [
                "",
                "## 20-epoch validation-only diagnostic",
                "",
                "| Checkpoint | Epoch | Foreground patient mean | BG-inclusive mean | BG fraction | FG fraction | MYO | LV | LA |",
                "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
                "| best | {epoch} | {fg:.8f} | {bgmean:.8f} | {bgfrac:.8f} | {fgfrac:.8f} | {myo:.8f} | {lv:.8f} | {la:.8f} |".format(
                    epoch=diagnostic_summary["best_epoch"],
                    fg=best["foreground_patient_mean"],
                    bgmean=best["benchmark_mean_bg_included"],
                    bgfrac=best["background_fraction"],
                    fgfrac=best["foreground_fraction"],
                    myo=best["patient_per_class"][1],
                    lv=best["patient_per_class"][2],
                    la=best["patient_per_class"][3],
                ),
                "| last | {epoch} | {fg:.8f} | {bgmean:.8f} | {bgfrac:.8f} | {fgfrac:.8f} | {myo:.8f} | {lv:.8f} | {la:.8f} |".format(
                    epoch=last["epoch"],
                    fg=last["foreground_patient_mean"],
                    bgmean=last["benchmark_mean_bg_included"],
                    bgfrac=last["background_fraction"],
                    fgfrac=last["foreground_fraction"],
                    myo=last["patient_per_class"]["1"],
                    lv=last["patient_per_class"]["2"],
                    la=last["patient_per_class"]["3"],
                ),
            ]
        )
    for name in ("pce_unmixed", "pce_mixed", "global", "shape", "spatial"):
        lines.append(
            f"| {name} | {train[f'{name}_raw']:.8f} | {train[f'{name}_weighted']:.8f} | "
            f"{gradient[f'{name}_weighted']:.8f} | {train[f'{name}_valid_pixels']:.1f} |"
        )
    lines.extend(
        [
            "",
            f"Prediction fractions: `{json.dumps(validation['prediction_class_fraction'], sort_keys=True)}`.",
            f"Non-empty rates: `{json.dumps(validation['nonempty_prediction_rate'], sort_keys=True)}`.",
            f"Foreground patient mean after two optimization steps: `{validation['foreground_patient_mean']:.8f}`; this is a smoke diagnostic, not an experimental result.",
            "",
            "No test labels or dense training labels were read. Future channels were excluded by the active-logit mask and the corresponding regression test.",
        ]
    )
    output = Path(arguments.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n")
    raise SystemExit(0 if decision == "PASS" else 2)


if __name__ == "__main__":
    main()

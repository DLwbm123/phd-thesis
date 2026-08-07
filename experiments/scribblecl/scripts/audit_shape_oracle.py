#!/usr/bin/env python3
"""Audit whether class-wise largest components are valid on Task-1 train GT."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import h5py
import numpy as np

from scribblecl.protocol import stage
from scribblecl.zs_components import largest_component_mask


CLASS_NAMES = {1: "MYO", 2: "LV", 3: "LA"}


def patient_ranges(patient_ends):
    starts = [0] + [int(value) + 1 for value in patient_ends[:-1]]
    ends = [int(value) + 1 for value in patient_ends]
    return list(zip(starts, ends))


def retention(mask):
    if not mask.any():
        return None
    return float(largest_component_mask(mask).sum() / mask.sum())


def summarize(values):
    array = np.asarray(values, dtype=np.float64)
    if array.size == 0:
        return {
            "nonempty_slices": 0,
            "mean_retention": float("nan"),
            "p05_retention": float("nan"),
            "minimum_retention": float("nan"),
            "fraction_retention_ge_0_95": float("nan"),
            "multicomponent_slices": 0,
        }
    return {
        "nonempty_slices": int(array.size),
        "mean_retention": float(array.mean()),
        "p05_retention": float(np.quantile(array, 0.05)),
        "minimum_retention": float(array.min()),
        "fraction_retention_ge_0_95": float((array >= 0.95).mean()),
        "multicomponent_slices": int((array < 1.0).sum()),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mmwhs-root", required=True)
    parser.add_argument("--csv", required=True)
    parser.add_argument("--report", required=True)
    arguments = parser.parse_args()

    spec = stage(1)
    path = Path(arguments.mmwhs_root) / spec.h5_name
    with h5py.File(path, "r") as handle:
        labels = handle["train_labels"][:].transpose(2, 0, 1).astype("int16")
        patient_ends = handle["patient_info_train"][:]
    mapped = np.zeros_like(labels)
    for source, destination in spec.local_to_global.items():
        mapped[labels == source] = destination

    rows = []
    global_values = {class_id: [] for class_id in spec.active}
    for patient_index, (start, end) in enumerate(patient_ranges(patient_ends)):
        for class_id in spec.active:
            values = [
                value
                for value in (retention(item == class_id) for item in mapped[start:end])
                if value is not None
            ]
            global_values[class_id].extend(values)
            row = {
                "scope": "patient",
                "patient_index": patient_index,
                "class_id": class_id,
                "class_name": CLASS_NAMES[class_id],
                **summarize(values),
            }
            rows.append(row)

    eligibility = {}
    for class_id, values in global_values.items():
        summary = summarize(values)
        eligible = (
            summary["mean_retention"] >= 0.99
            and summary["fraction_retention_ge_0_95"] >= 0.95
        )
        eligibility[class_id] = eligible
        rows.append(
            {
                "scope": "global",
                "patient_index": "ALL",
                "class_id": class_id,
                "class_name": CLASS_NAMES[class_id],
                **summary,
                "eligible": eligible,
            }
        )

    csv_path = Path(arguments.csv)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "scope",
        "patient_index",
        "class_id",
        "class_name",
        "nonempty_slices",
        "multicomponent_slices",
        "mean_retention",
        "p05_retention",
        "minimum_retention",
        "fraction_retention_ge_0_95",
        "eligible",
    ]
    with open(csv_path, "w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    global_rows = [row for row in rows if row["scope"] == "global"]
    lines = [
        "# Task-1 class-wise shape oracle",
        "",
        "This audit reads MMWHS Task-1 **training labels only**. Validation and test labels are not used.",
        "The pre-registered eligibility rule is mean largest-component retention >= 0.99 and at least 95% of non-empty slices with retention >= 0.95.",
        "",
        "| Class | Non-empty slices | Multi-component slices | Mean retention | P05 | Minimum | Fraction >=0.95 | Eligible |",
        "|---|---:|---:|---:|---:|---:|---:|:---:|",
    ]
    for row in global_rows:
        lines.append(
            "| {class_id} {class_name} | {nonempty_slices} | {multicomponent_slices} | "
            "{mean_retention:.6f} | {p05_retention:.6f} | {minimum_retention:.6f} | "
            "{fraction_retention_ge_0_95:.6f} | {eligible} |".format(**row)
        )
    lines.extend(
        [
            "",
            "Formal shape-loss classes: "
            + ", ".join(
                f"{class_id} {CLASS_NAMES[class_id]}"
                for class_id, eligible in eligibility.items()
                if eligible
            )
            + ".",
            "",
            "Machine-readable eligibility: `" + json.dumps(eligibility, sort_keys=True) + "`.",
        ]
    )
    report_path = Path(arguments.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

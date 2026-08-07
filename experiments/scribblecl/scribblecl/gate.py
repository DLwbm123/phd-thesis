"""Foreground-only checkpoint selection and static collapse gates."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Mapping


FOREGROUND_CLASSES = (1, 2, 3)


def class_value(mapping: Mapping, class_id: int):
    """Read class-indexed mappings from checkpoints or JSON round-trips."""
    if class_id in mapping:
        return mapping[class_id]
    return mapping[str(class_id)]


def foreground_mean_from_mapping(
    mapping: Mapping, classes: tuple[int, ...] = FOREGROUND_CLASSES
) -> float:
    return float(sum(float(class_value(mapping, class_id)) for class_id in classes) / len(classes))


def checkpoint_selection_score(
    validation: Mapping, classes: tuple[int, ...] = FOREGROUND_CLASSES
) -> float:
    """Return the registered validation-best score, never a BG-inclusive mean."""
    if "foreground_patient_mean" in validation:
        return float(validation["foreground_patient_mean"])
    return foreground_mean_from_mapping(validation["patient_per_class"], classes)


def _finite(value) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def compare_validations(
    previous: Mapping,
    current: Mapping,
    label: str,
    classes: tuple[int, ...] = FOREGROUND_CLASSES,
    max_mean_drop: float = 0.03,
    min_class_ratio: float = 0.5,
    min_prediction_fraction: float = 1e-4,
) -> dict:
    """Apply the pre-registered engineering collapse gate."""
    previous_mean = checkpoint_selection_score(previous, classes)
    current_mean = checkpoint_selection_score(current, classes)
    mean_drop = previous_mean - current_mean
    failures: list[str] = []
    class_rows = {}
    for class_id in classes:
        old = float(class_value(previous["patient_per_class"], class_id))
        new = float(class_value(current["patient_per_class"], class_id))
        ratio = new / old if old > 0 else (math.inf if new > 0 else 1.0)
        class_rows[str(class_id)] = {"previous": old, "current": new, "ratio": ratio}
        if not all(_finite(value) for value in (old, new, ratio)):
            failures.append(f"class_{class_id}_nonfinite")
        elif ratio < min_class_ratio:
            failures.append(f"class_{class_id}_ratio={ratio:.10f}<{min_class_ratio}")

    if not all(_finite(value) for value in (previous_mean, current_mean, mean_drop)):
        failures.append("foreground_mean_nonfinite")
    elif mean_drop > max_mean_drop:
        failures.append(f"foreground_mean_drop={mean_drop:.10f}>{max_mean_drop}")

    nonempty = current.get("nonempty_prediction_rate", {})
    for class_id in classes:
        rate = float(class_value(nonempty, class_id)) if nonempty else 0.0
        if not _finite(rate) or rate <= 0:
            failures.append(f"class_{class_id}_prediction_empty")

    background_fraction = float(current.get("background_fraction", math.nan))
    foreground_fraction = float(current.get("foreground_fraction", math.nan))
    for name, fraction in (
        ("background", background_fraction),
        ("foreground", foreground_fraction),
    ):
        if not _finite(fraction):
            failures.append(f"{name}_fraction_nonfinite")
        elif fraction < min_prediction_fraction:
            failures.append(f"{name}_collapse={fraction:.10f}<{min_prediction_fraction}")

    return {
        "gate": label,
        "metric": "foreground_patient_mean",
        "previous_epoch": previous.get("epoch"),
        "current_epoch": current.get("epoch"),
        "previous_foreground_mean": previous_mean,
        "current_foreground_mean": current_mean,
        "foreground_mean_drop": mean_drop,
        "previous_bg_included_mean": previous.get(
            "benchmark_mean_bg_included", previous.get("benchmark_mean")
        ),
        "current_bg_included_mean": current.get(
            "benchmark_mean_bg_included", current.get("benchmark_mean")
        ),
        "background_fraction": background_fraction,
        "foreground_fraction": foreground_fraction,
        "classes": class_rows,
        "decision": "PASS" if not failures else "STOP",
        "failure_reasons": failures,
    }


def load_checkpoint_validation(path: str | Path) -> dict:
    """Load a project-owned checkpoint validation record."""
    import torch

    checkpoint = torch.load(path, map_location="cpu", weights_only=False)
    return checkpoint["validation"]


from __future__ import annotations

from pathlib import Path

from .h5_dataset import DenseH5Dataset, WeakH5Dataset
from .protocols import DOMAIN_TASKS, TaskSpec


def h5_path(data_root: str | Path, task: TaskSpec) -> Path:
    if task not in DOMAIN_TASKS:
        raise ValueError("not a Domain-CL task")
    return Path(data_root) / "Domain_Prostate" / task.h5_name


def dense_dataset(data_root: str | Path, task: TaskSpec, split: str) -> DenseH5Dataset:
    return DenseH5Dataset(h5_path(data_root, task), split)


def weak_dataset(data_root: str | Path, task: TaskSpec, scribble_path: str | Path) -> WeakH5Dataset:
    return WeakH5Dataset(h5_path(data_root, task), scribble_path)

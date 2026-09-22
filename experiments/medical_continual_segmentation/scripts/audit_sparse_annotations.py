#!/usr/bin/env python3
"""Audit that sparse v2 annotations are shape- and label-safe."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

import h5py
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from medcl.data import dataset_path, tasks_for
from medcl.data.protocols import IGNORE_INDEX


def _sha256(path: Path) -> str:
    value = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=("class", "domain", "organ"), required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--sparse-root", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    rows = []
    for task in tasks_for(args.scenario):
        with h5py.File(dataset_path(args.data_root, task), "r") as handle:
            dense = np.asarray(handle["train_labels"][:]).transpose(2, 0, 1).astype(np.int16)
        path = args.sparse_root / args.scenario / f"{task.code}_v2_s2_seed{args.seed}.npz"
        annotations = np.load(path, allow_pickle=False)["annotations"]
        foreground = annotations > 0
        expected = np.where(dense > 0, dense + (task.label_shift if args.scenario == "class" else 0), 0)
        allowed = set(range(8)) | {IGNORE_INDEX}
        row = {
            "task": task.code,
            "shape_match": annotations.shape == dense.shape,
            "valid_values": set(np.unique(annotations).tolist()) <= allowed,
            "foreground_label_errors": int((foreground & (annotations != expected)).sum()),
            "background_on_dense_foreground": int(((annotations == 0) & (dense > 0)).sum()),
            "foreground_pixels": int(foreground.sum()),
            "background_pixels": int((annotations == 0).sum()),
            "unknown_pixels": int((annotations == IGNORE_INDEX).sum()),
            "npz_sha256": _sha256(path),
        }
        row["pass"] = bool(row["shape_match"] and row["valid_values"] and row["foreground_label_errors"] == 0 and row["background_on_dense_foreground"] == 0)
        rows.append(row)
    print(json.dumps({"scenario": args.scenario, "pass": all(row["pass"] for row in rows), "tasks": rows}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import h5py
import numpy as np

from scribblecl_do.data.protocols import DOMAIN_TASKS, ORGAN_TASKS
from scribblecl_do.data.scribbles import generate_volume_scribbles, scribble_hash


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=["domain", "organ"], required=True)
    parser.add_argument("--data-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--width", type=int, default=3, choices=[1, 3, 5])
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    tasks = DOMAIN_TASKS if args.scenario == "domain" else ORGAN_TASKS
    folder = "Domain_Prostate" if args.scenario == "domain" else "Task_incre"
    out_root = Path(args.output_root) / args.scenario
    out_root.mkdir(parents=True, exist_ok=True)
    summary = []
    for task in tasks:
        h5_path = Path(args.data_root) / folder / task.h5_name
        with h5py.File(h5_path, "r") as h:
            stored = np.asarray(h["train_labels"][:])
        masks = stored.transpose(2, 0, 1).astype(np.int64, copy=False)
        scribbles, stats = generate_volume_scribbles(masks, args.width, args.seed)
        metadata = {"scenario": args.scenario, "task": task.code, "width": args.width, "seed": args.seed}
        digest = scribble_hash(scribbles, metadata)
        npz_path = out_root / f"{task.code}_v2_s{args.width}_seed{args.seed}.npz"
        np.savez_compressed(npz_path, scribbles=scribbles)
        record = {**metadata, **stats.__dict__, "fg_coverage": stats.fg_coverage, "bg_annotation_ratio": stats.bg_annotation_ratio, "total_annotation_ratio": stats.total_annotation_ratio, "scribble_sha256": digest, "npz": str(npz_path)}
        (out_root / f"{task.code}_manifest.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        summary.append(record)
    (out_root / "annotation_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()

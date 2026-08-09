#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from hashlib import sha256
import json
from pathlib import Path

import h5py
import numpy as np

from scribblecl_do.data.h5_dataset import patient_ranges
from scribblecl_do.data.protocols import DOMAIN_TASKS, ORGAN_TASKS, EXPECTED_H5_SHA256, order_checksum
from scribblecl_do.utils.provenance import file_sha256


def audit_scenario(scenario: str, data_root: Path, verify_full_hash: bool) -> list[dict]:
    tasks = DOMAIN_TASKS if scenario == "domain" else ORGAN_TASKS
    folder = "Domain_Prostate" if scenario == "domain" else "Task_incre"
    rows = []
    for task in tasks:
        path = data_root / folder / task.h5_name
        with h5py.File(path, "r") as h:
            row = {"scenario": scenario, "index": task.index, "code": task.code, "source": task.source, "modality": task.modality, "foreground": task.foreground, "path": str(path)}
            for split in ("train", "val", "test"):
                row[f"{split}_slices"] = int(h[f"{split}_images"].shape[2])
                ends = np.asarray(h[f"patient_info_{split}"][:], dtype=np.int64)
                row[f"{split}_patients"] = int(len(ends))
                row[f"{split}_patient_ranges"] = patient_ranges(ends)
            key = f"{folder}/{task.h5_name}"
            row["expected_sha256"] = EXPECTED_H5_SHA256[key]
            row["actual_sha256"] = file_sha256(path) if verify_full_hash else "not_recomputed"
            row["hash_match"] = row["actual_sha256"] == row["expected_sha256"] if verify_full_hash else None
        rows.append(row)
    return rows


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--data-root", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--verify-full-hash", action="store_true")
    a = p.parse_args()
    output = Path(a.output); output.mkdir(parents=True, exist_ok=True)
    rows = audit_scenario("domain", Path(a.data_root), a.verify_full_hash) + audit_scenario("organ", Path(a.data_root), a.verify_full_hash)
    payload = {"domain_order_sha256": order_checksum(DOMAIN_TASKS), "organ_order_sha256": order_checksum(ORGAN_TASKS), "rows": rows}
    (output / "data_audit.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    with (output / "data_audit.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=[k for k in rows[0] if not k.endswith("ranges")])
        writer.writeheader(); writer.writerows([{k: v for k, v in r.items() if not k.endswith("ranges")} for r in rows])


if __name__ == "__main__":
    main()

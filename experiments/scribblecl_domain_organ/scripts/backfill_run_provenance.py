#!/usr/bin/env python3
"""Backfill immutable split/scribble provenance for an already-started run."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

from scribblecl_do.data.protocols import DOMAIN_TASKS, ORGAN_TASKS, EXPECTED_H5_SHA256
from scribblecl_do.data.scribbles import scribble_path
from scribblecl_do.utils.provenance import file_sha256


def mapping_sha256(value: dict) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    parser.add_argument("--scribble-root", required=True)
    args = parser.parse_args()
    run = Path(args.run)
    path = run / "run_manifest.json"
    manifest = json.loads(path.read_text())
    scenario = manifest["scenario"]
    tasks = DOMAIN_TASKS if scenario == "domain" else ORGAN_TASKS
    prefix = "Domain_Prostate" if scenario == "domain" else "Task_incre"
    h5_hashes = {task.code: EXPECTED_H5_SHA256[f"{prefix}/{task.h5_name}"] for task in tasks}
    scribble_hashes = {
        task.code: file_sha256(scribble_path(args.scribble_root, scenario, task.code, manifest["seed"]))
        for task in tasks
    }
    manifest.update(
        split_h5_sha256=h5_hashes,
        split_checksum_sha256=mapping_sha256(h5_hashes),
        scribble_sha256=scribble_hashes,
        scribble_protocol="v2_S2_width3",
        checkpoint_selection="fixed_last_epoch",
        test_for_selection=False,
    )
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()

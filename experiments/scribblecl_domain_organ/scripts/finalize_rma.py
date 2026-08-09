#!/usr/bin/env python3
"""Attach Benchmark RMA after independent PCE references finish."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from scribblecl_do.metrics.matrix import rma


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    parser.add_argument("--independent-scores", required=True)
    args = parser.parse_args()
    run = Path(args.run)
    manifest = json.loads((run / "run_manifest.json").read_text())
    refs = json.loads(Path(args.independent_scores).read_text())
    if refs["scenario"] != manifest["scenario"] or int(refs["seed"]) != int(manifest["seed"]):
        raise ValueError("independent-score scenario/seed mismatch")
    with (run / "performance_matrix.csv").open(newline="") as stream:
        rows = list(csv.reader(stream))[1:]
    matrix = np.asarray([[float(x) if x else np.nan for x in row[1:]] for row in rows])
    summary = json.loads((run / "summary.json").read_text())
    summary["RMA"] = rma(matrix, refs["scores"])
    summary["rma_reference"] = str(Path(args.independent_scores).resolve())
    write_json(run / "summary.json", summary)
    manifest["summary"] = summary
    manifest["rma_reference"] = summary["rma_reference"]
    write_json(run / "run_manifest.json", manifest)


if __name__ == "__main__":
    main()

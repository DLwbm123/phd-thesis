#!/usr/bin/env python3
"""Render the dispatcher status without estimating an ETA."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs-root", type=Path, default=Path("runs"))
    options = parser.parse_args()
    status = options.runs_root / "core_queue_status.json"
    if not status.is_file():
        raise SystemExit(f"status unavailable: {status}")
    payload = json.loads(status.read_text())
    print("Scenario Method Seed Stage Epoch PID GPU Status ETA source Log")
    for job in payload["jobs"]:
        processes = job.get("pids") or []
        pid = str(processes[0].get("pid", "-")) if processes else "-"
        stage = job.get("independent_task") or ("EWC" if job["method"] == "pce_ewc" else "FT")
        print(f"{job['scenario']:8} {job['method']:8} {job['seed']:4} {stage:5} "
              f"{str(job.get('epoch') or '-'):5} {pid:>6} {str(job.get('gpu') or '-'):3} "
              f"{job['status']:10} ETA unavailable -")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

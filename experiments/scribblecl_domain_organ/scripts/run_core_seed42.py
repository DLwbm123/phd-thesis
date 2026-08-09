#!/usr/bin/env python3
"""Prints the gate-respecting seed-42 command order; run_pilot executes each item."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
for scenario in ("domain","organ"):
    for method in ("pce_ft","pce_ewc"):
        print(ROOT/"configs"/scenario/f"{method}.yaml")
print("ZS configs: blocked_by_static_gate")

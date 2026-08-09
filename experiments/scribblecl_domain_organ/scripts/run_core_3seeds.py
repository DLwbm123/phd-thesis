#!/usr/bin/env python3
"""Seeds 43/44 are emitted only after a GO seed-42 gate report exists."""
from pathlib import Path
import sys

root=Path(__file__).resolve().parents[1]
for scenario in ("domain","organ"):
    gate=root/"reports"/f"{scenario.upper()}_SEED42_GATE.md"
    if not gate.exists() or not gate.read_text().startswith(f"DECISION: GO-{scenario.upper()}-SEEDS43-44"):
        raise SystemExit(f"blocked: {gate} is not GO")
print("seed-42 gates passed; resolve configs with seed=43 and seed=44 without changing other fields")

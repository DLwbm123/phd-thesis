#!/usr/bin/env python3
"""Sole entry point for class, domain and organ continual segmentation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from medcl.trainers import RunOptions, dry_run, run_independent_task, run_sequence, run_tiny_gate


SCENARIOS = ("class", "domain", "organ")
METHODS = ("dense_ft", "dense_ewc", "pce_ft", "pce_ewc", "pce_si", "enhanced_ft", "enhanced_ewc", "enhanced_si")


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description="Unified anonymous continual medical segmentation runner")
    value.add_argument("--scenario", choices=SCENARIOS, required=True)
    value.add_argument("--method", choices=METHODS, required=True)
    value.add_argument("--config", type=Path)
    value.add_argument("--data-root", type=Path)
    value.add_argument("--sparse-root", type=Path)
    value.add_argument("--runs-root", type=Path, default=Path("runs"))
    value.add_argument("--device", default="cuda:0")
    value.add_argument("--seed", type=int, default=42)
    value.add_argument("--epochs", type=int)
    value.add_argument("--batch-size", type=int)
    value.add_argument("--learning-rate", type=float)
    value.add_argument("--fisher-batches", type=int)
    value.add_argument("--run-id")
    value.add_argument("--resume", type=Path)
    value.add_argument("--stage1-parent", type=Path)
    value.add_argument("--max-stage", type=int)
    value.add_argument("--independent-scores", type=Path)
    value.add_argument("--dry-run", action="store_true")
    value.add_argument("--tiny-overfit", action="store_true")
    value.add_argument("--task", help="Task code used by --tiny-overfit")
    value.add_argument("--supervision", choices=("dense", "pce"), help="Tiny-gate supervision")
    value.add_argument("--tiny-steps", type=int, default=700)
    value.add_argument("--independent-task", help="Train one from-scratch RMA reference task")
    return value


def _options(args) -> RunOptions:
    config = {}
    if args.config:
        config = yaml.safe_load(args.config.read_text()) or {}
        if config.get("scenario") != args.scenario or config.get("method") != args.method: raise ValueError("config route mismatch")
    def choose(name, default=None):
        cli = getattr(args, name)
        return cli if cli is not None else config.get(name, default)
    data_root = choose("data_root")
    sparse_root = choose("sparse_root")
    if data_root is None or sparse_root is None: raise ValueError("--data-root and --sparse-root are required outside dry-run")
    return RunOptions(
        scenario=args.scenario, method=args.method, data_root=Path(data_root), sparse_root=Path(sparse_root), runs_root=args.runs_root,
        seed=args.seed, epochs=int(choose("epochs", 150)), batch_size=int(choose("batch_size", 8)), learning_rate=float(choose("learning_rate", .008)),
        lr_decay_epoch=int(config.get("lr_decay_epoch", 80)), lr_decay_rate=float(config.get("lr_decay_rate", .5)), fisher_batches=int(choose("fisher_batches", 50)),
        device=args.device, run_id=args.run_id, resume=args.resume, stage1_parent=args.stage1_parent, max_stage=args.max_stage, independent_scores=args.independent_scores,
        current_gate_min=float(config.get("current_gate_min", .10)),
    )


def main() -> None:
    args = parser().parse_args()
    if args.method.startswith("enhanced_"): raise RuntimeError("blocked_by_static_gate")
    if args.dry_run:
        print(json.dumps(dry_run(args.scenario, args.method, args.device), indent=2, sort_keys=True)); return
    options = _options(args)
    if args.tiny_overfit:
        if not args.task or not args.supervision: raise ValueError("--task and --supervision are required by --tiny-overfit")
        print(json.dumps(run_tiny_gate(options, args.task, args.supervision, args.tiny_steps), indent=2, sort_keys=True)); return
    if args.independent_task:
        print(json.dumps(run_independent_task(options,args.independent_task,Path(__file__).resolve().parent),indent=2,sort_keys=True)); return
    print(json.dumps(run_sequence(options, Path(__file__).resolve().parent), indent=2, sort_keys=True))


if __name__ == "__main__": main()

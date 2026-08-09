#!/usr/bin/env python3
"""Control-plane dispatcher for the frozen three-setting core experiment.

This program deliberately contains no training implementation.  Every launch
is an unmodified ``python main.py ...`` invocation in the supplied runtime.
Deploy this file *outside* a frozen training tree when a run's provenance hash
must remain unchanged.
"""
from __future__ import annotations

import argparse
import csv
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone


FROZEN_SOURCE_HASH = "fb27dfe49f0503f3b9c0f5f55c6265dff8256ab3cb6edc074d1d250f7fc2caa7"
DATA_ROOT = "/remote-home/wangbomin/CL_Benchmark/data"
SPARSE_ROOT = "/remote-home/wangbomin/medical_segmentation_data/sparse_annotations"
EWC_ORDER = ("domain", "organ", "class")


@dataclass(frozen=True)
class Job:
    scenario: str
    method: str
    run_id: str
    config: str
    priority: str
    independent_task: str | None = None

    @property
    def run_dir(self) -> Path:
        if self.independent_task:
            return Path("runs") / "references" / self.scenario / self.run_id
        return Path("runs") / self.scenario / self.run_id


def core_jobs() -> list[Job]:
    jobs: list[Job] = []
    for scenario in ("class", "domain", "organ"):
        jobs.append(Job(scenario, "pce_ft", f"medseg_{scenario}_pce_ft_seed42_final",
                        f"configs/{scenario}/pce_ft.yaml", "P2"))
        jobs.append(Job(scenario, "pce_ewc", f"medseg_{scenario}_pce_ewc_seed42_final",
                        f"configs/{scenario}/pce_ewc.yaml", "P1"))
    for scenario, tasks in (("class", ("T2", "T3")),
                            ("domain", ("B", "C", "D", "E", "F")),
                            ("organ", ("T2", "T3", "T4"))):
        for task in tasks:
            jobs.append(Job(scenario, "pce_ft", f"medseg_{scenario}_independent_{task}_seed42",
                            f"configs/{scenario}/pce_ft.yaml", "P3", task))
    return jobs


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def process_table() -> dict[str, dict]:
    result = subprocess.run(["ps", "-eo", "pid=,stat=,etime=,args="], text=True,
                            capture_output=True, check=True)
    rows: dict[str, dict] = {}
    for line in result.stdout.splitlines():
        match = re.match(r"\s*(\d+)\s+(\S+)\s+(\S+)\s+(.*)", line)
        if not match:
            continue
        pid, state, elapsed, command = match.groups()
        if "main.py" in command:
            rows[pid] = {"pid": int(pid), "process_state": state, "elapsed": elapsed,
                         "command": command}
    return rows


def gpu_ids() -> list[str]:
    result = subprocess.run(["nvidia-smi", "--query-gpu=index", "--format=csv,noheader"],
                            text=True, capture_output=True, check=True)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def gpu_for_command(command: str) -> str | None:
    match = re.search(r"--device\s+cuda:(\d+)", command)
    return match.group(1) if match else None


def process_matches_run(command: str, run_id: str) -> bool:
    """Match the argument value, not a prefix such as ``seed42_final``."""
    return re.search(r"--run-id\s+" + re.escape(run_id) + r"(?:\s|$)", command) is not None


def manifest_for(job: Job, root: Path) -> tuple[Path, dict]:
    path = root / job.run_dir / "run_manifest.json"
    return path, read_json(path)


def latest_epoch(run_dir: Path) -> int | None:
    last = run_dir / "last.pt"
    if not last.exists() or last.stat().st_size == 0:
        return None
    epochs: list[int] = []
    for log in run_dir.glob("*.jsonl"):
        try:
            for line in log.read_text().splitlines()[-20:]:
                value = json.loads(line).get("epoch")
                if isinstance(value, int):
                    epochs.append(value)
        except (OSError, json.JSONDecodeError):
            continue
    return max(epochs) if epochs else None


def parent_ready(job: Job, root: Path) -> tuple[bool, Path | None, str | None]:
    if job.method != "pce_ewc":
        return False, None, None
    parent = root / "runs" / job.scenario / f"medseg_{job.scenario}_pce_ft_seed42_final" / "stage_1.pt"
    if not parent.is_file() or parent.stat().st_size == 0:
        return False, None, None
    return True, parent, sha256(parent)


def command_for(job: Job, root: Path, gpu: str, resume: bool = False) -> list[str]:
    command = [sys.executable, "main.py", "--scenario", job.scenario, "--method", job.method,
               "--config", job.config, "--data-root", DATA_ROOT, "--sparse-root", SPARSE_ROOT,
               "--runs-root", "runs", "--device", f"cuda:{gpu}", "--run-id", job.run_id]
    if job.independent_task:
        command.extend(["--independent-task", job.independent_task])
    if job.method == "pce_ewc":
        ready, parent, _ = parent_ready(job, root)
        if not ready or parent is None:
            raise RuntimeError(f"EWC parent unavailable for {job.run_id}")
        command.extend(["--stage1-parent", str(parent.relative_to(root))])
    if resume:
        last = root / job.run_dir / "last.pt"
        if last.is_file() and last.stat().st_size:
            command.extend(["--resume", str(last.relative_to(root))])
    return command


def job_state(job: Job, root: Path, processes: dict[str, dict]) -> dict:
    manifest_path, manifest = manifest_for(job, root)
    run_dir = manifest_path.parent
    command_matches = [p for p in processes.values() if process_matches_run(p["command"], job.run_id)]
    config_path = root / job.config
    state = {
        "scenario": job.scenario, "method": job.method, "seed": 42, "run_id": job.run_id,
        "priority": job.priority, "independent_task": job.independent_task,
        "run_dir": str(run_dir), "manifest": str(manifest_path), "manifest_status": manifest.get("status", "absent"),
        "epoch": latest_epoch(run_dir), "source_hash": manifest.get("source_tree_sha256"),
        "config_hash": sha256(config_path) if config_path.is_file() else None,
        "checkpoint": str(run_dir / "last.pt") if (run_dir / "last.pt").is_file() else None,
        "stage1_checkpoint": str(run_dir / "stage_1.pt") if (run_dir / "stage_1.pt").is_file() else None,
        "pids": command_matches,
    }
    if command_matches:
        state["status"] = "running"
        state["gpu"] = gpu_for_command(command_matches[0]["command"])
    elif manifest.get("status") == "complete":
        state["status"] = "complete"
        state["gpu"] = None
    elif job.independent_task and manifest:
        # Frozen reference entry points have no --resume contract.  Preserve a
        # checkpointed interruption for audit; never overwrite or relaunch it.
        state["status"] = "stopped_nonresumable_reference"
        state["gpu"] = None
    elif manifest and (run_dir / "last.pt").is_file():
        state["status"] = "resumable"
        state["gpu"] = None
    else:
        state["status"] = "pending"
        state["gpu"] = None
    if job.method == "pce_ewc":
        ready, parent, parent_hash = parent_ready(job, root)
        state.update({"parent_ready": ready, "parent_checkpoint": str(parent) if parent else None,
                      "parent_sha256": parent_hash})
    return state


def manifest_inventory(root: Path, processes: dict[str, dict]) -> list[dict]:
    """Audit every persisted run without treating an old PID as authority."""
    rows: list[dict] = []
    for path in sorted((root / "runs").glob("**/run_manifest.json")):
        manifest = read_json(path)
        options = manifest.get("options", {})
        run_id = manifest.get("run_id", path.parent.name)
        matches = [item for item in processes.values() if process_matches_run(item["command"], run_id)]
        scenario, method = manifest.get("scenario"), manifest.get("method")
        config = root / "configs" / str(scenario) / f"{method}.yaml"
        rows.append({
            "run_dir": str(path.parent), "run_id": run_id, "scenario": scenario, "method": method,
            "seed": manifest.get("seed", options.get("seed")), "manifest_status": manifest.get("status", "unknown"),
            "epoch": latest_epoch(path.parent), "pids": matches,
            "gpu": gpu_for_command(matches[0]["command"]) if matches else None,
            "checkpoint": str(path.parent / "last.pt") if (path.parent / "last.pt").is_file() else None,
            "stage1_checkpoint": str(path.parent / "stage_1.pt") if (path.parent / "stage_1.pt").is_file() else None,
            "source_hash": manifest.get("source_tree_sha256"),
            "config_hash": sha256(config) if config.is_file() else None,
            "output_directory": str(path.parent),
        })
    return rows


def start(job: Job, root: Path, gpu: str, status_dir: Path, resume: bool) -> dict:
    log_dir = root / "reports" / "dispatcher_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log = log_dir / f"{job.run_id}.{stamp}.log"
    command = command_for(job, root, gpu, resume)
    with log.open("x") as handle:
        process = subprocess.Popen(command, cwd=root, stdout=handle, stderr=subprocess.STDOUT,
                                   start_new_session=True)
    event = {"at": now(), "event": "started", "run_id": job.run_id, "priority": job.priority,
             "pid": process.pid, "gpu": gpu, "command": command, "log": str(log), "resume": resume}
    with (status_dir / "core_dispatcher_events.jsonl").open("a") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
    return event


def write_progress(root: Path, states: list[dict]) -> None:
    results = root / "results" / "live"
    results.mkdir(parents=True, exist_ok=True)
    path = results / "core_progress.csv"
    fields = ["scenario", "method", "seed", "run_id", "priority", "independent_task", "status", "epoch", "gpu", "source_hash", "config_hash", "checkpoint"]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for state in states:
            writer.writerow({key: state.get(key) for key in fields})


def one_cycle(root: Path, status_dir: Path, no_launch: bool, allow_p3: bool) -> dict:
    processes = process_table()
    jobs = core_jobs()
    states = [job_state(job, root, processes) for job in jobs]
    busy = {str(state["gpu"]) for state in states if state.get("status") == "running" and state.get("gpu") is not None}
    idle = [gpu for gpu in gpu_ids() if gpu not in busy]
    # A first stage that is already within the last 10% must reserve a slot
    # for its EWC fork.  A non-resumable reference cannot be allowed to turn
    # this short boundary into a second full reference run.
    near_parent_ready = any(
        state["priority"] == "P2" and state["method"] == "pce_ft"
        and state["status"] == "running" and isinstance(state.get("epoch"), int)
        and state["epoch"] >= 135 and not state.get("stage1_checkpoint")
        for state in states
    )
    launches: list[dict] = []
    if not no_launch:
        # P1 is always considered before P2 and P3; Domain wins EWC ties.
        ordered = sorted(jobs, key=lambda j: ({"P1": 0, "P2": 1, "P3": 2}[j.priority],
                                                EWC_ORDER.index(j.scenario) if j.priority == "P1" else 0,
                                                j.run_id))
        for job in ordered:
            if not idle:
                break
            state = next(s for s in states if s["run_id"] == job.run_id)
            if state["status"] == "complete" or state["status"] == "running":
                continue
            if state["status"] == "stopped_nonresumable_reference":
                continue
            if job.priority == "P1" and not state.get("parent_ready"):
                continue
            if job.priority == "P3" and near_parent_ready:
                continue
            # Frozen independent-task currently retains only last.pt.  P3 is
            # held until its external validation-best checkpoint selector is
            # available; silently reporting last-epoch references is invalid.
            if job.priority == "P3" and not allow_p3:
                continue
            # Existing final FT jobs are protected P0; only a stopped final FT/EWC is P2-resumable.
            resume = state["status"] == "resumable"
            launches.append(start(job, root, idle.pop(0), status_dir, resume))
    # Refresh after launches so the JSON documents actual child PIDs on the next cycle.
    payload = {"updated_at": now(), "max_gpu_jobs": 4, "frozen_source_hash": FROZEN_SOURCE_HASH,
               "training_entry": "python main.py", "launches_this_cycle": launches,
               "jobs": states, "manifest_inventory": manifest_inventory(root, process_table()),
               "near_parent_ready_hold": near_parent_ready,
               "p3_gate": "open" if allow_p3 else "blocked_validation_best_selector_required",
               "disabled": ["enhanced", "si", "mib", "replay", "history_image_cache"]}
    (status_dir / "core_queue_status.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    write_progress(root, states)
    return payload


def acquire_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a+")
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as error:
        raise SystemExit(f"dispatcher lock already held: {path}") from error
    handle.seek(0)
    handle.truncate()
    handle.write(json.dumps({"pid": os.getpid(), "started_at": now()}) + "\n")
    handle.flush()
    return handle


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--poll-seconds", type=int, default=45, choices=range(30, 61))
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--no-launch", action="store_true")
    parser.add_argument("--allow-p3", action="store_true", help="requires a validation-best selector")
    arguments = parser.parse_args()
    root = arguments.runtime_root.resolve()
    if not (root / "main.py").is_file():
        raise SystemExit(f"not a runtime root: {root}")
    status_dir = root / "runs"
    lock = acquire_lock(status_dir / ".core_dispatcher.lock")
    try:
        while True:
            one_cycle(root, status_dir, arguments.no_launch, arguments.allow_p3)
            if arguments.once:
                return 0
            time.sleep(arguments.poll_seconds)
    finally:
        lock.close()


if __name__ == "__main__":
    raise SystemExit(main())

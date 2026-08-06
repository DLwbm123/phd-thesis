#!/usr/bin/env python3
"""Bounded Task-1 coverage queue; it never dispatches seeds 43/44 or later tasks."""
import json
import subprocess
import time
from pathlib import Path

ROOT = Path('/remote-home/wangbomin/ScribbleCL')
CODE = ROOT / 'experiments/scribblecl'
DATA = Path('/remote-home/wangbomin/CL_Benchmark/data/MMWHS')
OUT = ROOT / 'coverage_runs'
SCRIBBLES = ROOT / 'coverage_outputs/scribbles/42'
PYTHON = '/root/anaconda3/bin/python'

jobs = [
    ('Dense', 'dense', None, '.008', 'cuda:0'),
    ('B1', 'pce', SCRIBBLES/'B1/stage1.npz', '.004', 'cuda:1'),
    ('B1', 'zs',  SCRIBBLES/'B1/stage1.npz', '.008', 'cuda:0'),
    ('B2', 'pce', SCRIBBLES/'B2/stage1.npz', '.004', 'cuda:1'),
    ('B2', 'zs',  SCRIBBLES/'B2/stage1.npz', '.008', 'cuda:0'),
    ('B3', 'pce', SCRIBBLES/'B3/stage1.npz', '.004', 'cuda:1'),
    ('B3', 'zs',  SCRIBBLES/'B3/stage1.npz', '.008', 'cuda:0'),
]

def command(budget, method, scribble, lr, device):
    cmd = [PYTHON, '-m', 'scribblecl.run', '--method', method, '--stage', '1',
           '--seed', '42', '--mmwhs-root', str(DATA), '--output-root', str(OUT/budget),
           '--epochs', '150', '--batch-size', '8', '--lr', lr, '--device', device]
    if scribble: cmd += ['--scribble', str(scribble)]
    return cmd

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    state_path = OUT/'queue_status.json'
    state = {'protocol': 'Task 1 validation only; seed 42 only', 'started_at': time.time(),
             'jobs': [], 'completion_status': 'running'}
    active = []
    pending = list(jobs)
    while pending or active:
        while pending and len(active) < 2:
            job = pending.pop(0); budget, method, scribble, lr, device = job
            run_dir = OUT/budget/f'{method}_seed42_stage1'
            log_dir = run_dir; log_dir.mkdir(parents=True, exist_ok=True)
            proc = subprocess.Popen(command(*job), cwd=CODE, env={**__import__('os').environ, 'PYTHONPATH': str(CODE)},
                                    stdout=open(log_dir/'stdout.log','w'), stderr=open(log_dir/'stderr.log','w'))
            row = {'budget':budget,'method':method,'stage':1,'seed':42,'device':device,
                   'pid':proc.pid,'run_dir':str(run_dir),'started_at':time.time(),'status':'running'}
            state['jobs'].append(row); active.append((proc,row)); state_path.write_text(json.dumps(state,indent=2))
        time.sleep(10)
        for proc,row in active[:]:
            code=proc.poll()
            if code is not None:
                row.update({'status':'completed' if code == 0 else 'failed','returncode':code,'ended_at':time.time()})
                active.remove((proc,row)); state_path.write_text(json.dumps(state,indent=2))
    state.update({'completion_status':'completed','ended_at':time.time()})
    state_path.write_text(json.dumps(state,indent=2))

if __name__ == '__main__': main()

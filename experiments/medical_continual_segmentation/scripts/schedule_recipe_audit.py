#!/usr/bin/env python3
"""Schedule only pre-registered first-task PCE recipe diagnostics.

It never launches continual-learning, replay, SI, enhanced, RMA, or extra
seeds.  Each child remains an ordinary ``python main.py`` process.
"""
from __future__ import annotations

import argparse, fcntl, json, os, re, subprocess, sys, time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


DATA="/remote-home/wangbomin/CL_Benchmark/data"; SPARSE="/remote-home/wangbomin/medical_segmentation_data/sparse_annotations"

@dataclass(frozen=True)
class Spec:
    scenario: str
    variant: str
    label: str
    @property
    def run_id(self): return f"medseg_{self.scenario}_{'A' if self.scenario=='domain' else 'T1'}_pce_{self.label}_20e_seed42"
    @property
    def run_dir(self): return Path("runs")/"pce_rescue"/self.scenario/self.run_id

SPECS=[Spec(s,v,l) for s in ("domain","class","organ") for v,l in (("original_optimizer","R1"),("balanced_sampler","R2"),("current_recipe","R0"))]

def now(): return datetime.now(timezone.utc).isoformat(timespec="seconds")

def ps():
    text=subprocess.run(["ps","-eo","pid=,args="],capture_output=True,text=True,check=True).stdout
    rows=[]
    for line in text.splitlines():
        match=re.match(r"\s*(\d+)\s+(.*)",line)
        if match: rows.append({"pid":int(match.group(1)),"command":match.group(2)})
    return rows

def device(command):
    found=re.search(r"--device\s+cuda:(\d+)",command); return found.group(1) if found else None

def exact(command,run_id): return re.search(r"--run-id\s+"+re.escape(run_id)+r"(?:\s|$)",command) is not None

def dense_complete(root,scenario):
    path=root/"runs"/"dense_first_task"/scenario/f"medseg_{scenario}_dense_first_task_seed42"/"run_manifest.json"
    if not path.is_file(): return False
    return json.loads(path.read_text()).get("status")=="complete"

def state(root,spec,processes):
    manifest=root/spec.run_dir/"run_manifest.json"; current=[p for p in processes if exact(p["command"],spec.run_id)]
    if current: return {"status":"running","pid":current[0]["pid"],"gpu":device(current[0]["command"])}
    if manifest.is_file():
        value=json.loads(manifest.read_text()); return {"status":value.get("status","unknown"),"pid":None,"gpu":None}
    return {"status":"pending","pid":None,"gpu":None}

def command(spec,gpu):
    return [sys.executable,"main.py","--scenario",spec.scenario,"--method","pce_ft","--config",f"configs/{spec.scenario}/pce_ft.yaml","--data-root",DATA,"--sparse-root",SPARSE,"--runs-root","runs","--device",f"cuda:{gpu}","--epochs","20","--run-id",spec.run_id,"--pce-rescue-variant",spec.variant]

def cycle(root):
    processes=ps(); states={spec.run_id:state(root,spec,processes) for spec in SPECS}
    occupied={device(p["command"]) for p in processes if "main.py" in p["command"] and device(p["command"]) is not None}
    free=[str(x) for x in range(4) if str(x) not in occupied]; launched=[]
    # P1: R1/R2 for a setting immediately after its matching Dense gate. P2: R0.
    ordered=sorted(SPECS,key=lambda s:(0 if s.label in {"R1","R2"} else 1,("domain","class","organ").index(s.scenario),s.label))
    for spec in ordered:
        if not free or not dense_complete(root,spec.scenario) or states[spec.run_id]["status"]!="pending": continue
        gpu=free.pop(0); log=root/"reports"/"recipe_audit_logs"; log.mkdir(parents=True,exist_ok=True); path=log/f"{spec.run_id}.log"
        with path.open("x") as handle: child=subprocess.Popen(command(spec,gpu),cwd=root,stdout=handle,stderr=subprocess.STDOUT,start_new_session=True)
        launched.append({"run_id":spec.run_id,"variant":spec.label,"pid":child.pid,"gpu":gpu,"command":command(spec,gpu),"log":str(path)})
    payload={"updated_at":now(),"allowed_training":"PCE first-task R0/R1/R2 only","blocked":["continual_learning","rma","seeds_43_44","si","enhanced","mib","replay"],"launches":launched,"dense_complete":{s:dense_complete(root,s) for s in ("class","domain","organ")},"jobs":[{"scenario":s.scenario,"variant":s.label,"run_id":s.run_id,**states[s.run_id]} for s in SPECS]}
    (root/"runs"/"recipe_audit_status.json").write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=Path,required=True); ap.add_argument("--poll",type=int,default=30,choices=range(30,61)); args=ap.parse_args(); root=args.root.resolve(); lock=root/"runs"/".recipe_audit_scheduler.lock"; handle=lock.open("a+")
    try: fcntl.flock(handle.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError: raise SystemExit("recipe audit scheduler lock is held")
    handle.seek(0); handle.truncate(); handle.write(json.dumps({"pid":os.getpid(),"started_at":now()})+"\n"); handle.flush()
    while True: cycle(root); time.sleep(args.poll)

if __name__=="__main__": main()

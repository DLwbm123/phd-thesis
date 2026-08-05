#!/usr/bin/env python3
"""Bounded two-worker dispatcher for the four core methods and seeds 42/43/44."""
import argparse, json, os, subprocess, sys, time
from pathlib import Path

PCE={'pce','pce_mib'}
def complete(path):
    try: return json.loads((path/'run_manifest.json').read_text()).get('completion_status') == 'completed' and (path/'best.pt').exists()
    except FileNotFoundError: return False
def active(path):
    try:
        pid=int((path/'pid').read_text().strip()); os.kill(pid, 0); return True
    except (FileNotFoundError, ProcessLookupError, ValueError): return False
def main():
    p=argparse.ArgumentParser(); p.add_argument('--app-root',required=True); p.add_argument('--output-root',required=True); p.add_argument('--mmwhs-root',required=True); p.add_argument('--seed',type=int,required=True); p.add_argument('--device',default='cuda:0'); p.add_argument('--max-parallel',type=int,default=2); p.add_argument('--family',choices=['pce','zs'],required=True); a=p.parse_args()
    app,out=Path(a.app_root),Path(a.output_root); scrib=out.parent/'outputs'/'scribbles'/str(a.seed); env={**os.environ,'PYTHONPATH':str(app)}
    jobs=[]
    for family,methods,lr in [('pce',['pce','pce_mib'],'.004'),('zs',['zs','zs_mib'],'.008')]:
        if family != a.family: continue
        t1=out/f'{family}_seed{a.seed}_stage1'
        if not complete(t1) and not active(t1): jobs.append((family,1,lr))
        for method in methods:
            jobs.extend([(method,2,lr),(method,3,lr)])
    running=[]
    while jobs or running:
        running=[x for x in running if x.poll() is None]
        if len(running) >= a.max_parallel or not jobs: time.sleep(15); continue
        method,stage,lr=jobs.pop(0); family='pce' if method in PCE else 'zs'; parent=out/f'{family if stage==2 else method}_seed{a.seed}_stage{stage-1}'/'best.pt'; target=out/f'{method}_seed{a.seed}_stage{stage}'
        if complete(target): continue
        if stage>1 and not parent.exists(): jobs.append((method,stage,lr)); time.sleep(5); continue
        cmd=[sys.executable,'-m','scribblecl.run','--method',method,'--stage',str(stage),'--seed',str(a.seed),'--mmwhs-root',a.mmwhs_root,'--output-root',str(out),'--epochs','150','--batch-size','8','--lr',lr,'--device',a.device,'--scribble',str(scrib/f'stage{stage}.npz')]
        if stage>1: cmd += ['--parent',str(parent)]
        target.mkdir(parents=True,exist_ok=True); so=open(target/'stdout.log','a'); se=open(target/'stderr.log','a'); proc=subprocess.Popen(cmd,cwd=app,env=env,stdout=so,stderr=se); (target/'pid').write_text(str(proc.pid)); running.append(proc)
if __name__=='__main__': main()

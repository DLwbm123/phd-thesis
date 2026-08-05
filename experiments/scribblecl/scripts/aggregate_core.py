#!/usr/bin/env python3
"""Aggregate only completed final-stage core runs; incomplete values remain NA."""
import argparse, csv, json, statistics
from pathlib import Path
import sys; sys.path.insert(0,str(Path(__file__).parents[1]))
from scribblecl.metrics import matrix_summary

METHODS=['pce','pce_mib','zs','zs_mib']; SEEDS=[42,43,44]
def load(path):
    try: return json.loads((path/'run_manifest.json').read_text())
    except FileNotFoundError: return {}
def main():
 p=argparse.ArgumentParser(); p.add_argument('--runs-root',required=True); p.add_argument('--results-root',required=True); a=p.parse_args(); runs,results=Path(a.runs_root),Path(a.results_root); results.mkdir(parents=True,exist_ok=True); rows=[]; manifests=[]
 for method in METHODS:
  for seed in SEEDS:
   stages=[runs/f'{method}_seed{seed}_stage{i}' for i in (1,2,3)]; ms=[load(x) for x in stages]
   manifests.append({'method':method,'seed':seed,'stage1_status':ms[0].get('completion_status','NA'),'stage2_status':ms[1].get('completion_status','NA'),'stage3_status':ms[2].get('completion_status','NA')})
   if not all(m.get('completion_status')=='completed' for m in ms): rows.append({'method':method,'seed':seed,'stage':3,'A-Dice':'NA','BWTR':'NA','RMA':'NA','WCD':'NA','mean_current_task_dice':'NA','completion_status':'incomplete'}); continue
   matrix=[]
   for i,path in enumerate(stages,1):
    values=[float(r['dice']) for r in csv.DictReader(open(path/'stage_metrics.csv'))]; matrix.append(values+[float('nan')]*(3-len(values)))
   # matrix has lower triangle only; principal/last rows suffice for these metrics.
   summary=matrix_summary(__import__('numpy').array(matrix),[matrix[i][i] for i in range(3)])
   # Independent weak-supervision references are deliberately outside this run.
   summary['RMA']='NA_requires_independent_reference'
   rows.append({'method':method,'seed':seed,'stage':3,**summary,'WCD':'NA_not_yet_classwise','completion_status':'completed'})
 for name,data in [('core_runs_manifest.csv',manifests),('core_metrics_per_seed.csv',rows)]:
  with open(results/name,'w',newline='') as f: w=csv.DictWriter(f,fieldnames=data[0].keys()); w.writeheader(); w.writerows(data)
 summary=[]
 for method in METHODS:
  done=[r for r in rows if r['method']==method and r['completion_status']=='completed']; summary.append({'method':method,'completed_seeds':len(done),'A-Dice_mean_std':'NA' if len(done)<3 else f"{statistics.mean(float(x['A-Dice']) for x in done):.6f} ± {statistics.stdev(float(x['A-Dice']) for x in done):.6f}",'BWTR_mean_std':'NA' if len(done)<3 else f"{statistics.mean(float(x['BWTR']) for x in done):.6f} ± {statistics.stdev(float(x['BWTR']) for x in done):.6f}",'RMA_mean_std':'NA_requires_independent_reference'})
 with open(results/'core_metrics_summary.csv','w',newline='') as f: w=csv.DictWriter(f,fieldnames=summary[0].keys()); w.writeheader(); w.writerows(summary)
if __name__=='__main__': main()

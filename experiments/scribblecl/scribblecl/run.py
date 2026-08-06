"""Reproducible single-run entry point. Outputs are external to the repository."""
import argparse, csv, hashlib, json, os, platform, random, time
from copy import deepcopy
from pathlib import Path
import numpy as np, torch
from torch.utils.data import DataLoader
from .data import MMWHS, DenseMMWHS
from .losses import partial_cross_entropy, pce_ratio_flip_legacy_loss, consistency_loss, scribble_mib_loss, masked_logits
from .metrics import benchmark_patient_dice
from .model import ResUNet32
from .protocol import stage, old_classes

def sha(path):
    h=hashlib.sha256();
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def evaluate(model, root, stages, trained_stage, device):
    model.eval(); values=[]; class_values=[]
    with torch.no_grad():
        for s in stages:
            d=MMWHS(root,s,'val'); predictions=[]; targets=[]
            for x,y in DataLoader(d,batch_size=4):
                # Benchmark Class-CL protocol: future classes are unavailable at stage t.
                seen=(0,)+tuple(c for s in range(1,trained_stage+1) for c in stage(s).active)
                p=masked_logits(model(x.to(device)),seen).argmax(1).cpu().numpy(); y=y.numpy()
                predictions.append(p); targets.append(y)
            predictions=np.concatenate(predictions); targets=np.concatenate(targets)
            score, per_class=benchmark_patient_dice(predictions,targets,d.patient_info,(0,)+stage(s).active)
            values.append(score)
            for c in stage(s).active:
                class_values.append({'evaluated_task':s,'class_id':c,'dice':per_class[c]})
    return values, class_values

def main():
 p=argparse.ArgumentParser(); p.add_argument('--method',required=True,choices=['pce','pce_ratio_flip_legacy','pce_mib_legacy','dense','dense_mib_legacy']); p.add_argument('--stage',type=int,required=True); p.add_argument('--seed',type=int,required=True); p.add_argument('--mmwhs-root',required=True); p.add_argument('--scribble',default=None); p.add_argument('--output-root',required=True); p.add_argument('--parent',default=None); p.add_argument('--epochs',type=int,default=150); p.add_argument('--batch-size',type=int,default=8); p.add_argument('--lr',type=float,default=.008); p.add_argument('--device',default='cuda:0'); p.add_argument('--max-batches',type=int,default=None); p.add_argument('--fixed-batches',action='store_true'); a=p.parse_args()
 random.seed(a.seed); np.random.seed(a.seed); torch.manual_seed(a.seed); device=torch.device(a.device); out=Path(a.output_root)/f'{a.method}_seed{a.seed}_stage{a.stage}'; out.mkdir(parents=True,exist_ok=True)
 manifest={'run_id':out.name,'method':a.method,'model_seed':a.seed,'scribble_seed':a.seed,'stage':a.stage,'active_classes':stage(a.stage).active,'old_classes':old_classes(a.stage),'source_dense_training_labels':a.method.startswith('dense'),'completion_status':'running','parent_checkpoint_sha256':sha(a.parent) if a.parent else None,'start_time':time.time(),'device':a.device,'torch':torch.__version__,'python':platform.python_version()}; (out/'run_manifest.json').write_text(json.dumps(manifest,indent=2)); (out/'config_resolved.yaml').write_text('\n'.join(f'{k}: {v}' for k,v in vars(a).items())+'\n'); (out/'environment.txt').write_text(json.dumps({'python':platform.python_version(),'torch':torch.__version__,'cuda':torch.version.cuda},indent=2))
 model=ResUNet32().to(device); teacher=None
 if a.parent:
   ck=torch.load(a.parent,map_location=device); model.load_state_dict(ck['model'])
   if 'mib' in a.method: teacher=deepcopy(model).eval(); [setattr(q,'requires_grad',False) for q in teacher.parameters()]
 train=DenseMMWHS(a.mmwhs_root,a.stage,'train') if a.method.startswith('dense') else MMWHS(a.mmwhs_root,a.stage,'train',a.scribble); loader=DataLoader(train,batch_size=a.batch_size,shuffle=True,num_workers=2,pin_memory=True); fixed=list(loader)[:a.max_batches] if a.fixed_batches and a.max_batches else None; opt=torch.optim.SGD(model.parameters(),lr=a.lr,momentum=.9)
 allowed=(0,)+stage(a.stage).active; log=open(out/'train.jsonl','w')
 for epoch in range(a.epochs):
   model.train(); losses=[]
   for batch_i,(x,y) in enumerate(fixed if fixed is not None else loader):
     x,y=x.to(device),y.to(device); logits=model(x)
     sparse=y
     legacy_ratio = a.method == 'pce_ratio_flip_legacy'
     loss=pce_ratio_flip_legacy_loss(logits,sparse,stage(a.stage).active) if legacy_ratio else partial_cross_entropy(logits,sparse,allowed)
     if legacy_ratio: loss=loss+.1*consistency_loss(logits,model(torch.flip(x,[-1])).flip(-1),stage(a.stage).active)
     if teacher: loss=loss+10*scribble_mib_loss(logits,teacher(x),sparse,old_classes(a.stage))
     if not torch.isfinite(loss):
      manifest.update({'completion_status':'failed_nonfinite_loss','failure_reason':f'nonfinite loss at epoch {epoch} batch {batch_i}','end_time':time.time()}); (out/'run_manifest.json').write_text(json.dumps(manifest,indent=2)); raise FloatingPointError(manifest['failure_reason'])
     opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0); opt.step(); losses.append(float(loss.detach()))
     if a.max_batches and batch_i + 1 >= a.max_batches: break
   log.write(json.dumps({'epoch':epoch,'loss':float(np.mean(losses))})+'\n'); log.flush()
   if epoch==79: [g.update(lr=g['lr']*.5) for g in opt.param_groups]
 torch.save({'model':model.state_dict(),'epoch':a.epochs-1},out/'best.pt'); (out/'best_checkpoint_pointer.txt').write_text(str(out/'best.pt'))
 vals,class_vals=evaluate(model,a.mmwhs_root,list(range(1,a.stage+1)),a.stage,device); (out/'stage_metrics.csv').write_text('evaluated_task,dice\n'+'\n'.join(f'{i+1},{v}' for i,v in enumerate(vals))+'\n');
 with open(out/'class_metrics.csv','w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=('evaluated_task','class_id','dice')); w.writeheader(); w.writerows(class_vals)
 manifest.update({'completion_status':'completed','end_time':time.time(),'validation_dice':vals}); (out/'run_manifest.json').write_text(json.dumps(manifest,indent=2)); log.close()
if __name__=='__main__': main()

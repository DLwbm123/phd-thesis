"""Controlled validation-only MMWHS Task-1 A--E runner."""
import argparse,json,random,time,hashlib,os
from pathlib import Path
import numpy as np,torch
from torch.utils.data import DataLoader
from .data import MMWHS,DenseMMWHS
from .losses import partial_cross_entropy,legacy_ratio_mse
from .metrics import benchmark_patient_dice,dice
from .model import ResUNet32
from .protocol import stage,IGNORE_INDEX
from .zs_components import (active_probabilities,apply_basic_geometry,
    original_puzzlemix_cutout,integrity_loss,spatial_pseudo_correction,
    component_gradient_norm)

def file_sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def evaluate(model,root,device):
    d=MMWHS(root,1,'val'); allowed=(0,1,2,3); preds=[]; targets=[]
    model.eval()
    with torch.no_grad():
        for x,y in DataLoader(d,batch_size=8,shuffle=False):
            preds.append(active_probabilities(model(x.to(device)),allowed).argmax(1).cpu().numpy())
            targets.append(y.numpy())
    p=np.concatenate(preds); y=np.concatenate(targets)
    main,pc=benchmark_patient_dice(p,y,d.patient_info,allowed)
    all_slice={c:float(np.mean([dice(a,b,c) for a,b in zip(p,y)])) for c in allowed[1:]}
    positive={c:float(np.mean([dice(a,b,c) for a,b in zip(p,y) if (b==c).any()])) for c in allowed[1:]}
    aggregate={c:dice(p,y,c) for c in allowed}
    return {'benchmark_mean':main,'patient_per_class':pc,'all_slice':all_slice,
        'positive_slice':positive,'aggregate_volume':aggregate,
        'background_fraction':float((p==0).mean()),'foreground_fraction':float((p>0).mean()),
        'nonempty_prediction_rate':{c:float(np.mean([(a==c).any() for a in p])) for c in allowed[1:]}}

def append_json(path,obj):
    with open(path,'a') as f: f.write(json.dumps(obj,sort_keys=True)+'\n')

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--level',choices=list('ABCDE'),required=True); p.add_argument('--seed',type=int,default=42)
    p.add_argument('--mmwhs-root',required=True); p.add_argument('--scribble',required=True); p.add_argument('--output-root',required=True)
    p.add_argument('--optimizer',choices=['adam','sgd'],required=True); p.add_argument('--lr',type=float,required=True)
    p.add_argument('--epochs',type=int,default=150); p.add_argument('--batch-size',type=int,default=8)
    p.add_argument('--device',default='cuda:0'); p.add_argument('--max-batches',type=int); p.add_argument('--grad-every',type=int,default=10)
    p.add_argument('--resume',action='store_true'); p.add_argument('--source-commit',required=True)
    p.add_argument('--variant',choices=['standard','fg_only','legacy_ratio','dense'],default='standard')
    a=p.parse_args(); assert a.seed==42, 'static gate is seed 42 only'
    random.seed(a.seed); np.random.seed(a.seed); torch.manual_seed(a.seed); torch.cuda.manual_seed_all(a.seed)
    torch.backends.cudnn.benchmark=False; torch.backends.cudnn.deterministic=True
    if a.variant!='standard': assert a.level=='A', 'diagnostic/reference variants are level A only'
    device=torch.device(a.device); model=ResUNet32().to(device); initial_sha=hashlib.sha256(torch.cat([q.detach().cpu().flatten() for q in model.parameters()]).numpy().tobytes()).hexdigest()
    names={'standard':a.level,'fg_only':'A0','legacy_ratio':'A_ratio','dense':'Dense_v2'}
    out=Path(a.output_root)/f'static_{names[a.variant]}_{a.optimizer}_seed42'; out.mkdir(parents=True,exist_ok=True)
    manifest={'run_id':out.name,'scope':'MMWHS_Task1_validation_only','level':a.level,'seed':a.seed,
        'optimizer':a.optimizer,'lr':a.lr,'epochs':a.epochs,'batch_size':a.batch_size,'variant':a.variant,
        'scribble_sha256':file_sha(a.scribble),'initialization_sha256':initial_sha,
        'warmup_epoch':8,'ratio_mse':a.variant=='legacy_ratio','diagnostic_only':a.variant=='legacy_ratio',
        'dense_training_labels':a.variant=='dense','test_set_used':False,'source_commit':a.source_commit,
        'status':'running','start_time':time.time(),'resume_count':0}
    manifest_path=out/'run_manifest.json'
    if a.resume and manifest_path.exists():
        previous=json.loads(manifest_path.read_text()); manifest['start_time']=previous.get('start_time',manifest['start_time']); manifest['status']='running'; manifest['resume_count']=previous.get('resume_count',0)+1; manifest['last_resume_time']=time.time()
    manifest_path.write_text(json.dumps(manifest,indent=2)); (out/'config_resolved.json').write_text(json.dumps(vars(a),indent=2))
    train=DenseMMWHS(a.mmwhs_root,1,'train') if a.variant=='dense' else MMWHS(a.mmwhs_root,1,'train',a.scribble)
    allowed=(0,)+stage(1).active
    opt=torch.optim.Adam(model.parameters(),lr=a.lr,weight_decay=1e-4) if a.optimizer=='adam' else torch.optim.SGD(model.parameters(),lr=a.lr)
    scheduler=torch.optim.lr_scheduler.StepLR(opt,step_size=80,gamma=.5)
    best=-1.; best_epoch=None; start_epoch=0
    if a.resume and (out/'last.pt').exists():
        ck=torch.load(out/'last.pt',map_location='cpu',weights_only=False); model.load_state_dict(ck['model']); opt.load_state_dict(ck['optimizer']); scheduler.load_state_dict(ck['scheduler'])
        for state in opt.state.values():
            for key,value in state.items():
                if torch.is_tensor(value): state[key]=value.to(device)
        best=ck['best']; best_epoch=ck['best_epoch']; start_epoch=ck['epoch']+1
        random.setstate(ck['rng_python']); np.random.set_state(ck['rng_numpy']); torch.set_rng_state(ck['rng_torch'])
        if torch.cuda.is_available() and ck.get('rng_cuda') is not None: torch.cuda.set_rng_state_all(ck['rng_cuda'])
    for epoch in range(start_epoch,a.epochs):
        gen=torch.Generator().manual_seed(a.seed+epoch)
        loader=DataLoader(train,batch_size=a.batch_size,shuffle=True,generator=gen,num_workers=2,pin_memory=True)
        model.train(); component_names=('pce','augmentation','consistency','integrity','pseudo','ratio')
        sums={k:[] for k in component_names+('total',)}
        raw_sums={k:[] for k in component_names}
        grad_record={}
        for bi,(x,sparse) in enumerate(loader):
            x,sparse=x.to(device),sparse.to(device)
            if a.variant=='fg_only':
                sparse=sparse.clone(); sparse[sparse==0]=IGNORE_INDEX
            if a.level>='B':
                code=int(np.random.default_rng(a.seed*100000+epoch*1000+bi).integers(0,16)); x,sparse=apply_basic_geometry(x,sparse,code)
            logits=model(x); probs=active_probabilities(logits,allowed)
            parts={'pce':partial_cross_entropy(logits,sparse,allowed),'augmentation':logits.sum()*0,
                   'consistency':logits.sum()*0,'integrity':logits.sum()*0,'pseudo':logits.sum()*0,
                   'ratio':logits.sum()*0}
            raw_parts=dict(parts)
            aux={}
            if a.level>='C':
                cparts=original_puzzlemix_cutout(model,x,sparse,allowed)
                parts.update({k:v for k,v in cparts.items() if k in parts}); raw_parts.update({k:v for k,v in cparts.items() if k in raw_parts})
                raw_parts['consistency']=cparts['consistency_unweighted']
            if a.level>='D': parts['integrity']=integrity_loss(probs,sparse)
            if a.level>='E' and epoch>=8:
                e=spatial_pseudo_correction(probs,x,sparse,allowed); parts['pseudo']=e['pseudo']; aux=e
            if a.variant=='legacy_ratio': parts['ratio']=.05*legacy_ratio_mse(logits,sparse,stage(1).active); raw_parts['ratio']=parts['ratio']/.05
            for k in ('integrity','pseudo'): raw_parts[k]=parts[k]
            total=sum(parts.values())
            if not torch.isfinite(total):
                manifest.update({'status':'failed_nonfinite','failure_epoch':epoch,'failure_batch':bi,'end_time':time.time()}); manifest_path.write_text(json.dumps(manifest,indent=2))
                raise FloatingPointError(f'nonfinite epoch={epoch} batch={bi} parts={parts}')
            if bi==0 and epoch%a.grad_every==0:
                for k,v in parts.items():
                    grad_record[f'{k}_weighted']=component_gradient_norm(v,model)
                    grad_record[f'{k}_unweighted']=component_gradient_norm(raw_parts[k],model)
            opt.zero_grad(set_to_none=True); total.backward(); opt.step()
            for k,v in parts.items(): sums[k].append(float(v.detach()))
            for k,v in raw_parts.items(): raw_sums[k].append(float(v.detach()))
            sums['total'].append(float(total.detach()))
            if bi==0 and aux:
                append_json(out/'em_spatial.jsonl',{'epoch':epoch,'em_ratios':aux['em_ratios'].cpu().tolist() if aux['em_ratios'] is not None else None,'spatial_mean':float(aux['spatial_mean'])})
            if a.max_batches and bi+1>=a.max_batches: break
        scheduler.step(); row={'epoch':epoch,'lr':opt.param_groups[0]['lr'],**{k:float(np.mean(v)) for k,v in sums.items()}}
        row.update({f'{k}_weighted':float(np.mean(sums[k])) for k in component_names})
        row.update({f'{k}_unweighted':float(np.mean(raw_sums[k])) for k in component_names})
        append_json(out/'train_components.jsonl',row)
        if grad_record: append_json(out/'gradient_norms.jsonl',{'epoch':epoch,**grad_record})
        val=evaluate(model,a.mmwhs_root,device); val['epoch']=epoch; append_json(out/'validation.jsonl',val)
        append_json(out/'prediction_distribution.jsonl',{'epoch':epoch,**{k:val[k] for k in ('background_fraction','foreground_fraction','nonempty_prediction_rate')}})
        improved=val['benchmark_mean']>best
        if improved: best=val['benchmark_mean']; best_epoch=epoch
        state={'model':model.state_dict(),'optimizer':opt.state_dict(),'scheduler':scheduler.state_dict(),
            'epoch':epoch,'validation':val,'best':best,'best_epoch':best_epoch,'rng_python':random.getstate(),
            'rng_numpy':np.random.get_state(),'rng_torch':torch.get_rng_state(),
            'rng_cuda':torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None}
        torch.save(state,out/'last.pt.tmp'); os.replace(out/'last.pt.tmp',out/'last.pt')
        if improved:
            torch.save(state,out/'best_val.pt.tmp'); os.replace(out/'best_val.pt.tmp',out/'best_val.pt')
    manifest.update({'status':'completed','end_time':time.time(),'best_validation':best,'best_epoch':best_epoch})
    manifest_path.write_text(json.dumps(manifest,indent=2))
if __name__=='__main__': main()

#!/usr/bin/env python3
"""Emit exact first-10-step A fingerprints for cross-commit parity."""
import argparse,hashlib,json,random
import numpy as np,torch
from torch.utils.data import DataLoader
from scribblecl.data import MMWHS
from scribblecl.losses import partial_cross_entropy
from scribblecl.model import ResUNet32

def sha(t): return hashlib.sha256(t.detach().cpu().contiguous().numpy().tobytes()).hexdigest()
p=argparse.ArgumentParser(); p.add_argument('--mmwhs-root',required=True); p.add_argument('--scribble',required=True); p.add_argument('--output',required=True); p.add_argument('--device',default='cuda:0'); a=p.parse_args()
seed=42; random.seed(seed); np.random.seed(seed); torch.manual_seed(seed); torch.cuda.manual_seed_all(seed)
torch.backends.cudnn.benchmark=False; torch.backends.cudnn.deterministic=True; device=torch.device(a.device)
torch.use_deterministic_algorithms(True)
model=ResUNet32().to(device); opt=torch.optim.SGD(model.parameters(),lr=.004); data=MMWHS(a.mmwhs_root,1,'train',a.scribble)
loader=DataLoader(data,batch_size=8,shuffle=True,generator=torch.Generator().manual_seed(seed),num_workers=2,pin_memory=True)
rows=[]
for step,(x,y) in enumerate(loader):
    x,y=x.to(device),y.to(device); logits=model(x); loss=partial_cross_entropy(logits,y,(0,1,2,3))
    opt.zero_grad(set_to_none=True); loss.backward()
    grads=torch.cat([q.grad.detach().flatten() for q in model.parameters() if q.grad is not None])
    before=torch.cat([q.detach().flatten() for q in model.parameters()]); opt.step(); after=torch.cat([q.detach().flatten() for q in model.parameters()])
    rows.append({'step':step,'logits_sha256':sha(logits),'loss':float(loss.detach()),'gradients_sha256':sha(grads),'parameters_before_sha256':sha(before),'parameters_after_sha256':sha(after)})
    if step==9: break
open(a.output,'w').write(json.dumps(rows,indent=2)+'\n')

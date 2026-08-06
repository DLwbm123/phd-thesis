#!/usr/bin/env python3
"""Offline only: dense labels are read here, never by the training dataset."""
import argparse, csv, hashlib, json
from pathlib import Path
import h5py, numpy as np
from skimage.morphology import skeletonize
import sys; sys.path.insert(0,str(Path(__file__).parents[1]))
from scribblecl.data import make_sparse
from scribblecl.protocol import stage

p=argparse.ArgumentParser(); p.add_argument('--mmwhs-root',required=True); p.add_argument('--output-root',required=True); p.add_argument('--seed',type=int,required=True); p.add_argument('--width',type=int,choices=(1,3,5),default=3); a=p.parse_args(); root=Path(a.mmwhs_root); budget={1:1,3:2,5:3}[a.width]; out=Path(a.output_root)/'scribbles'/str(a.seed)/f'B{budget}'; out.mkdir(parents=True,exist_ok=True); rows=[]; coverage={"seed":a.seed,"budget_id":f"B{budget}","width":a.width,"stages":{}}
for idx in (1,2,3):
 s=stage(idx)
 with h5py.File(root/s.h5_name,'r') as h: local=h['train_labels'][:].transpose(2,0,1).astype('int16')
 sparse=np.stack([make_sparse(x,idx,skeletonize,a.width) for x in local]); np.savez_compressed(out/f'stage{idx}.npz',scribbles=sparse); coverage["stages"][str(idx)]={}
 for k,c in s.local_to_global.items():
  pix=int((sparse==c).sum()); dense=int((local==k).sum()); per_slice=(sparse==c).reshape(len(sparse),-1).sum(1); coverage["stages"][str(idx)][str(c)]={"scribble_pixels":pix,"dense_foreground_pixels":dense,"foreground_coverage":pix/dense if dense else 0.0,"zero_supervision_slices":int((per_slice==0).sum())}; rows.append({'case_id':s.h5_name,'slice_id':'all','stage':idx,'class_id':c,'class_name':f'class_{c}','scribble_seed':a.seed,'foreground_scribble_pixels':pix,'background_scribble_pixels':0,'image_pixels':int(sparse.size),'annotation_ratio':pix/sparse.size,'source_split':'train'})
 zero_slice=(sparse!=-100).reshape(len(sparse),-1).sum(1)==0
 # Match the training sampler's deterministic torch.randperm(seed) order,
 # rather than counting contiguous HDF5 slices as if they were batches.
 import torch
 shuffled=torch.randperm(len(zero_slice),generator=torch.Generator().manual_seed(a.seed)).numpy()
 zero_batches=sum(zero_slice[shuffled[i:i+8]].all() for i in range(0,len(shuffled),8))
 n_batches=(len(shuffled)+7)//8
 coverage["stages"][str(idx)]["zero_supervision_slices"]=int(zero_slice.sum())
 coverage["stages"][str(idx)]["zero_supervision_slice_ratio"]=float(zero_slice.mean())
 coverage["stages"][str(idx)]["zero_supervision_batches_batch8"]=int(zero_batches)
 coverage["stages"][str(idx)]["zero_supervision_batch_ratio_batch8"]=float(zero_batches/n_batches)
with open(out/'scribble_manifest.csv','w',newline='') as f: w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
(out/'coverage_summary.json').write_text(json.dumps(coverage,indent=2))

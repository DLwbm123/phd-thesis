#!/usr/bin/env python3
"""Offline only: dense labels are read here, never by the training dataset."""
import argparse, csv, hashlib
from pathlib import Path
import h5py, numpy as np
from skimage.morphology import skeletonize
import sys; sys.path.insert(0,str(Path(__file__).parents[1]))
from scribblecl.data import make_sparse
from scribblecl.protocol import stage

p=argparse.ArgumentParser(); p.add_argument('--mmwhs-root',required=True); p.add_argument('--output-root',required=True); p.add_argument('--seed',type=int,required=True); a=p.parse_args(); root=Path(a.mmwhs_root); out=Path(a.output_root)/'scribbles'/str(a.seed); out.mkdir(parents=True,exist_ok=True); rows=[]
for idx in (1,2,3):
 s=stage(idx)
 with h5py.File(root/s.h5_name,'r') as h: local=h['train_labels'][:].transpose(2,0,1).astype('int16')
 sparse=np.stack([make_sparse(x,idx,skeletonize) for x in local]); np.savez_compressed(out/f'stage{idx}.npz',scribbles=sparse)
 for k,c in s.local_to_global.items():
  pix=int((sparse==c).sum()); rows.append({'case_id':s.h5_name,'slice_id':'all','stage':idx,'class_id':c,'class_name':f'class_{c}','scribble_seed':a.seed,'foreground_scribble_pixels':pix,'background_scribble_pixels':0,'image_pixels':int(sparse.size),'annotation_ratio':pix/sparse.size,'source_split':'train'})
with open(Path(a.output_root)/'scribble_manifest.csv','w',newline='') as f: w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)

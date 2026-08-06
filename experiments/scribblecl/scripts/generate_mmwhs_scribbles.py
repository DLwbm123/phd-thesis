#!/usr/bin/env python3
"""Offline generator: only the selected stage-local dense labels are read here."""
import argparse,csv,json,sys
from pathlib import Path
import h5py,numpy as np,torch
from skimage.morphology import skeletonize
sys.path.insert(0,str(Path(__file__).parents[1]))
from scribblecl.data import make_sparse,make_sparse_v2
from scribblecl.protocol import stage,IGNORE_INDEX

p=argparse.ArgumentParser(); p.add_argument('--mmwhs-root',required=True); p.add_argument('--output-root',required=True)
p.add_argument('--seed',type=int,required=True); p.add_argument('--width',type=int,choices=(1,3,5),default=3)
p.add_argument('--protocol',choices=('v2','legacy_fg'),default='v2'); p.add_argument('--stage',type=int,choices=(1,2,3),action='append')
a=p.parse_args(); root=Path(a.mmwhs_root); budget={1:1,3:2,5:3}[a.width]
out=Path(a.output_root)/'scribbles'/a.protocol/str(a.seed)/f'S{budget}'; out.mkdir(parents=True,exist_ok=True)
rows=[]; coverage={'protocol':a.protocol,'seed':a.seed,'budget_id':f'S{budget}','width':a.width,'stages':{}}
for idx in (a.stage or [1,2,3]):
    s=stage(idx)
    with h5py.File(root/s.h5_name,'r') as h: local=h['train_labels'][:].transpose(2,0,1).astype('int16')
    fn=make_sparse_v2 if a.protocol=='v2' else make_sparse
    sparse=np.stack([fn(x,idx,skeletonize,a.width) for x in local])
    np.savez_compressed(out/f'stage{idx}.npz',scribbles=sparse)
    info={}; coverage['stages'][str(idx)]=info
    for src,c in s.local_to_global.items():
        pix=int((sparse==c).sum()); dense=int((local==src).sum())
        info[str(c)]={'scribble_pixels':pix,'dense_foreground_pixels':dense,'foreground_coverage':pix/dense if dense else 0.}
        rows.append({'stage':idx,'class_id':c,'scribble_seed':a.seed,'foreground_scribble_pixels':pix,
                     'background_scribble_pixels':int((sparse==0).sum()),'image_pixels':int(sparse.size),
                     'annotation_ratio':float((sparse!=IGNORE_INDEX).mean()),'source_split':'train','protocol':a.protocol})
    zero=(sparse!=IGNORE_INDEX).reshape(len(sparse),-1).sum(1)==0
    order=torch.randperm(len(zero),generator=torch.Generator().manual_seed(a.seed)).numpy()
    zb=sum(zero[order[i:i+8]].all() for i in range(0,len(order),8))
    info.update({'foreground_scribble_pixels':int((sparse>0).sum()),'background_scribble_pixels':int((sparse==0).sum()),
        'unknown_pixels':int((sparse==IGNORE_INDEX).sum()),'zero_supervision_slices':int(zero.sum()),
        'zero_supervision_batches_batch8':int(zb),'total_annotation_ratio':float((sparse!=IGNORE_INDEX).mean())})
with open(out/'scribble_manifest.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
(out/'coverage_summary.json').write_text(json.dumps(coverage,indent=2))
print(out)

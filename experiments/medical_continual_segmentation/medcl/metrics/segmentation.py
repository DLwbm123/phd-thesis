from __future__ import annotations
import numpy as np
import torch
from medcl.data.datasets import patient_ranges


def dice_for_classes(pred, target, classes, eps=1e-5):
    values=[]
    for c in classes:
        p,t=pred==c,target==c; values.append((2*np.logical_and(p,t).sum()+eps)/(p.sum()+t.sum()+eps))
    return np.asarray(values,dtype=float)


@torch.no_grad()
def evaluate(model, loader, patient_info, device, task_id, classes):
    model.eval(); predictions=[]; targets=[]
    for images,dense in loader:
        logits=model(images.to(device),task_id); predictions.append(logits.argmax(1).cpu().numpy()); targets.append(dense.numpy())
    pred,target=np.concatenate(predictions),np.concatenate(targets); rows=patient_ranges(patient_info); per=np.stack([dice_for_classes(pred[a:b],target[a:b],classes) for a,b in rows])
    return {"benchmark_mean":float(per.mean()),"per_class":per.mean(0).tolist(),"per_patient":per.tolist(),"prediction_fg_fraction":float((pred>0).mean())}

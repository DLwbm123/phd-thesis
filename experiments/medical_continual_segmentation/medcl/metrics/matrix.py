from __future__ import annotations
import numpy as np


def matrix_summary(matrix, scenario, independent=None, random_scores=None):
    x=np.asarray(matrix,dtype=float); completed=np.flatnonzero(np.isfinite(np.diag(x)))
    if not len(completed): raise ValueError("empty performance matrix")
    last=int(completed[-1]); diagonal=np.diag(x)[:last+1]; final=x[last,:last+1]
    old=final[:-1]; old_diagonal=diagonal[:-1]
    out={"A-Dice":float(np.nanmean(final)),"BWTR":0.0 if not len(old) else float(np.mean((old-old_diagonal)/old_diagonal)),"mean_current":float(np.mean(diagonal)),"final_old_mean":None if not len(old) else float(np.mean(old))}
    if independent is None or last == 0: out["RMA"] = None
    else:
        reference=np.asarray(independent,dtype=float)
        if reference.shape != (len(x),) or np.any(reference[1:last+1] <= 0): raise ValueError("RMA reference mismatch")
        out["RMA"]=float(np.mean(diagonal[1:]/reference[1:last+1]))
    if scenario=="domain":
        if random_scores is None: raise ValueError("Domain E-FWT requires random scores")
        cells=[x[t,i]-random_scores[i] for t in range(last+1) for i in range(t+1,len(x)) if np.isfinite(x[t,i])]
        out["E-FWT"]=None if not cells else float(np.mean(cells))
    return out

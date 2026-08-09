from __future__ import annotations
import os, random, signal
from pathlib import Path
import numpy as np
import torch


class CheckpointController:
    def __init__(self, run_dir):
        self.run_dir=Path(run_dir); self.stop_requested=False
        signal.signal(signal.SIGTERM,self._stop); signal.signal(signal.SIGINT,self._stop)
    def _stop(self,*_): self.stop_requested=True
    def should_stop(self): return self.stop_requested or (self.run_dir/"STOP_AFTER_EPOCH").exists()
    def save(self,model,optimizer,scheduler,stage,epoch,rows,ewc=None,si=None,**extra):
        value={"model":model.state_dict(),"optimizer":optimizer.state_dict(),"scheduler":scheduler.state_dict(),"stage":stage,"epoch":epoch,"rows":rows,"ewc":None if ewc is None else ewc.state_dict(),"si":None if si is None else si.state_dict(),"python_rng":random.getstate(),"numpy_rng":np.random.get_state(),"torch_rng":torch.get_rng_state(),"cuda_rng":torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,**extra}
        tmp=self.run_dir/"last.pt.tmp"; final=self.run_dir/"last.pt"; torch.save(value,tmp); os.replace(tmp,final); return final
    @staticmethod
    def load(path,model,optimizer=None,scheduler=None,ewc=None,si=None,map_location="cpu"):
        x=torch.load(path,map_location=map_location,weights_only=False); model.load_state_dict(x["model"])
        if optimizer is not None: optimizer.load_state_dict(x["optimizer"])
        if scheduler is not None: scheduler.load_state_dict(x["scheduler"])
        device=next(model.parameters()).device
        if ewc is not None and x["ewc"] is not None: ewc.load_state_dict(x["ewc"],device)
        if si is not None and x["si"] is not None: si.load_state_dict(x["si"],device)
        random.setstate(x["python_rng"]); np.random.set_state(x["numpy_rng"]); torch.set_rng_state(x["torch_rng"])
        if torch.cuda.is_available() and x["cuda_rng"] is not None: torch.cuda.set_rng_state_all(x["cuda_rng"])
        return x

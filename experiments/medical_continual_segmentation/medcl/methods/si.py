from __future__ import annotations

import torch
from .ewc import selected


class SynapticIntelligence:
    def __init__(self, c=5.0, xi=1.0): self.c=float(c); self.xi=float(xi); self.anchor={}; self.big={}; self.small={}
    def begin(self, model):
        params=selected(model)
        if not self.anchor: self.anchor={n:p.detach().clone() for n,p in params.items()}
        for n,p in params.items():
            if n not in self.anchor: self.anchor[n]=p.detach().clone()
        self.small={n:torch.zeros_like(p) for n,p in params.items()}
    def accumulate(self, model, lr):
        for n,p in selected(model).items():
            if p.grad is not None: self.small[n].add_(float(lr)*p.grad.detach().square())
    def penalty(self, model):
        params=selected(model)
        if not self.big: return next(iter(params.values())).sum()*0
        return self.c*sum((self.big[n]*(params[n]-self.anchor[n]).square()).sum() for n in self.big)
    def consolidate(self, model):
        params=selected(model)
        for n,p in params.items(): self.big[n]=self.big.get(n,torch.zeros_like(p))+self.small[n]/((p.detach()-self.anchor[n]).square()+self.xi)
        self.anchor={n:p.detach().clone() for n,p in params.items()}; self.small={n:torch.zeros_like(p) for n,p in params.items()}
    def state_dict(self): return {"c":self.c,"xi":self.xi,"anchor":self.anchor,"big":self.big,"small":self.small}
    def load_state_dict(self,state,device=None):
        self.c=state["c"]; self.xi=state["xi"]
        move=lambda values:{n:x.to(device) if device is not None else x for n,x in values.items()}
        self.anchor=move(state["anchor"]); self.big=move(state["big"]); self.small=move(state["small"])
    def nbytes(self): return sum(x.numel()*x.element_size() for x in [*self.anchor.values(),*self.big.values(),*self.small.values()])

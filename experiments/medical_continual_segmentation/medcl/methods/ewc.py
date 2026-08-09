from __future__ import annotations

from dataclasses import dataclass
import torch

from medcl.supervision.losses import sparse_loss


def selected(model):
    source = model.importance_named_parameters() if hasattr(model, "importance_named_parameters") else model.named_parameters()
    return {name: parameter for name, parameter in source if parameter.requires_grad}


@dataclass
class FisherSummary:
    batches: int
    known_pixels: int
    parameter_count: int
    nonzero: int
    minimum: float
    maximum: float
    mean: float


def estimate_fisher(model, loader, device, task_id=None, max_batches=50):
    if getattr(loader.dataset, "exposes_dense", None) is not False: raise ValueError("Fisher requires sparse-only loader")
    params = selected(model); fisher = {n: torch.zeros_like(p) for n, p in params.items()}; was_training = model.training; model.eval(); batches = known_pixels = 0
    for images, annotations in loader:
        if max_batches is not None and batches >= max_batches: break
        images, annotations = images.to(device), annotations.to(device); known = annotations != -100
        if not bool(known.any()): continue
        model.zero_grad(set_to_none=True); logits = model(images, task_id) if task_id is not None else model(images); sparse_loss(logits, annotations).backward()
        for name, parameter in params.items():
            if parameter.grad is not None: fisher[name].add_(parameter.grad.detach().square())
        batches += 1; known_pixels += int(known.sum())
    if not batches: raise RuntimeError("empty Fisher")
    for value in fisher.values(): value.div_(batches)
    model.train(was_training); flat = torch.cat([x.flatten() for x in fisher.values()])
    if not torch.isfinite(flat).all() or bool((flat < 0).any()): raise FloatingPointError("invalid Fisher")
    return fisher, FisherSummary(batches, known_pixels, flat.numel(), int((flat > 0).sum()), float(flat.min()), float(flat.max()), float(flat.mean()))


class OnlineEWC:
    def __init__(self, lambda_=1.0, gamma=.1): self.lambda_=float(lambda_); self.gamma=float(gamma); self.fisher={}; self.anchor={}; self.names=(); self.fisher_flat=None; self.anchor_flat=None
    def consolidate(self, model, current):
        params=selected(model)
        if set(params)!=set(current): raise ValueError("importance scope mismatch")
        self.fisher={n:(self.gamma*self.fisher[n]+current[n].detach() if n in self.fisher else current[n].detach()).clone() for n in params}; self.anchor={n:p.detach().clone() for n,p in params.items()}; self._cache()
    def _cache(self): self.names=tuple(self.anchor); self.fisher_flat=torch.cat([self.fisher[n].flatten() for n in self.names]); self.anchor_flat=torch.cat([self.anchor[n].flatten() for n in self.names])
    def penalty(self, model):
        params=selected(model)
        if not self.anchor: return next(iter(params.values())).sum()*0
        current=torch.cat([params[n].reshape(-1) for n in self.names]); return self.lambda_*(self.fisher_flat*(current-self.anchor_flat).square()).sum()
    def state_dict(self): return {"lambda":self.lambda_,"gamma":self.gamma,"fisher":self.fisher,"anchor":self.anchor}
    def load_state_dict(self,state,device=None): self.lambda_=state["lambda"]; self.gamma=state["gamma"]; self.fisher={n:x.to(device) if device is not None else x for n,x in state["fisher"].items()}; self.anchor={n:x.to(device) if device is not None else x for n,x in state["anchor"].items()}; self._cache()
    def nbytes(self): return sum(x.numel()*x.element_size() for x in [*self.fisher.values(),*self.anchor.values()])

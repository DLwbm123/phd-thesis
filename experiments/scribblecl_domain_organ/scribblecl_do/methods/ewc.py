"""Online diagonal EWC with sparse-current-task Fisher estimation only."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import torch
from torch import nn

from .ft import sparse_pce


def _selected(model: nn.Module) -> dict[str, nn.Parameter]:
    source = model.fisher_named_parameters() if hasattr(model, "fisher_named_parameters") else model.named_parameters()
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


def estimate_sparse_fisher(
    model: nn.Module,
    loader: Iterable,
    device: torch.device | str,
    task_id: int | None = None,
    max_batches: int | None = None,
) -> tuple[dict[str, torch.Tensor], FisherSummary]:
    """Estimate Fisher from current train images and sparse PCE only.

    The loader must be weak-only.  Dense masks, pseudo labels and auxiliary
    losses are structurally absent from this function.
    """
    dataset = getattr(loader, "dataset", None)
    if dataset is not None and getattr(dataset, "exposes_dense", None) is not False:
        raise ValueError("Fisher requires a weak-only loader")
    params = _selected(model)
    fisher = {name: torch.zeros_like(parameter, memory_format=torch.preserve_format) for name, parameter in params.items()}
    was_training = model.training
    model.eval()
    batches = 0
    known_pixels = 0
    for images, sparse in loader:
        if max_batches is not None and batches >= max_batches:
            break
        images, sparse = images.to(device), sparse.to(device)
        known = sparse != -100
        if not bool(known.any()):
            continue
        model.zero_grad(set_to_none=True)
        logits = model(images) if task_id is None else model(images, task_id)
        loss = sparse_pce(logits, sparse)
        loss.backward()
        for name, parameter in params.items():
            if parameter.grad is not None:
                fisher[name].add_(parameter.grad.detach().square())
        batches += 1
        known_pixels += int(known.sum())
    if batches == 0:
        raise RuntimeError("no sparse-supervised Fisher batches")
    for value in fisher.values():
        value.div_(batches)
        if not bool(torch.isfinite(value).all()) or bool((value < 0).any()):
            raise FloatingPointError("invalid Fisher diagonal")
    model.train(was_training)
    flat = torch.cat([value.flatten() for value in fisher.values()])
    summary = FisherSummary(
        batches=batches,
        known_pixels=known_pixels,
        parameter_count=int(flat.numel()),
        nonzero=int((flat > 0).sum()),
        minimum=float(flat.min()),
        maximum=float(flat.max()),
        mean=float(flat.mean()),
    )
    return fisher, summary


class OnlineEWC:
    """Benchmark online consolidation: F <- gamma*F + F_current."""

    def __init__(self, lambda_: float = 1.0, gamma: float = 0.1):
        self.lambda_ = float(lambda_)
        self.gamma = float(gamma)
        self.fisher: dict[str, torch.Tensor] = {}
        self.theta_star: dict[str, torch.Tensor] = {}
        self._names: tuple[str, ...] = ()
        self._fisher_flat: torch.Tensor | None = None
        self._theta_flat: torch.Tensor | None = None

    def penalty(self, model: nn.Module) -> torch.Tensor:
        params = _selected(model)
        if not self.theta_star:
            anchor = next(iter(params.values()))
            return anchor.sum() * 0.0
        if tuple(params) != self._names or self._fisher_flat is None or self._theta_flat is None:
            self._refresh_flat_cache(params)
        current = torch.cat([params[name].reshape(-1) for name in self._names])
        return self.lambda_ * (self._fisher_flat * (current - self._theta_flat).square()).sum()

    def consolidate(self, model: nn.Module, current_fisher: dict[str, torch.Tensor]) -> None:
        params = _selected(model)
        if set(params) != set(current_fisher):
            raise ValueError("Fisher parameter scope mismatch")
        if self.fisher:
            self.fisher = {name: self.gamma * self.fisher[name] + current_fisher[name].detach().clone() for name in params}
        else:
            self.fisher = {name: value.detach().clone() for name, value in current_fisher.items()}
        self.theta_star = {name: parameter.detach().clone() for name, parameter in params.items()}
        self._refresh_flat_cache(params)

    def _refresh_flat_cache(self, params: dict[str, nn.Parameter]) -> None:
        self._names = tuple(params)
        self._fisher_flat = torch.cat([self.fisher[name].reshape(-1) for name in self._names])
        self._theta_flat = torch.cat([self.theta_star[name].reshape(-1) for name in self._names])

    def state_nbytes(self) -> int:
        return sum(v.numel() * v.element_size() for v in [*self.fisher.values(), *self.theta_star.values()])

    def state_dict(self) -> dict:
        return {"lambda": self.lambda_, "gamma": self.gamma, "fisher": self.fisher, "theta_star": self.theta_star}

"""Benchmark-compatible Synaptic Intelligence parameter regularizer."""
from __future__ import annotations

import torch
from torch import nn

from .ewc import _selected


class SynapticIntelligence:
    def __init__(self, c: float = 5.0, xi: float = 1.0):
        self.c = float(c)
        self.xi = float(xi)
        self.checkpoint: dict[str, torch.Tensor] = {}
        self.big_omega: dict[str, torch.Tensor] = {}
        self.small_omega: dict[str, torch.Tensor] = {}

    def begin(self, model: nn.Module) -> None:
        params = _selected(model)
        if not self.checkpoint:
            self.checkpoint = {n: p.detach().clone() for n, p in params.items()}
        self.small_omega = {n: torch.zeros_like(p) for n, p in params.items()}

    def penalty(self, model: nn.Module) -> torch.Tensor:
        params = _selected(model)
        if not self.big_omega:
            return next(iter(params.values())).sum() * 0.0
        return self.c * sum((self.big_omega[n] * (params[n] - self.checkpoint[n]).square()).sum() for n in params)

    def accumulate_after_backward(self, model: nn.Module, learning_rate: float) -> None:
        # Exact Benchmark implementation accumulates lr * grad^2.
        for name, parameter in _selected(model).items():
            if parameter.grad is not None:
                self.small_omega[name].add_(float(learning_rate) * parameter.grad.detach().square())

    def consolidate(self, model: nn.Module) -> None:
        params = _selected(model)
        if not self.small_omega:
            raise RuntimeError("SI begin/accumulation missing")
        for name, parameter in params.items():
            delta2 = (parameter.detach() - self.checkpoint[name]).square()
            addition = self.small_omega[name] / (delta2 + self.xi)
            self.big_omega[name] = self.big_omega.get(name, torch.zeros_like(addition)) + addition
        self.checkpoint = {n: p.detach().clone() for n, p in params.items()}
        self.small_omega = {n: torch.zeros_like(p) for n, p in params.items()}

    def state_nbytes(self) -> int:
        values = [*self.checkpoint.values(), *self.big_omega.values(), *self.small_omega.values()]
        return sum(v.numel() * v.element_size() for v in values)

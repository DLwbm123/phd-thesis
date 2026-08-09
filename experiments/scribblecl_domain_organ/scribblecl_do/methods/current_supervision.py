from __future__ import annotations

import torch
import torch.nn.functional as F

from .ft import sparse_pce


def supervision_loss(kind: str, logits: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    if kind == "dense":
        return F.cross_entropy(logits, target)
    if kind == "pce":
        return sparse_pce(logits, target)
    if kind == "zs":
        raise RuntimeError("ZS is blocked_by_static_gate and is not runnable in this workspace")
    raise ValueError(kind)

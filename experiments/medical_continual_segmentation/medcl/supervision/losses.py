from __future__ import annotations

import torch
import torch.nn.functional as F

from medcl.data.protocols import IGNORE_INDEX


def _assert_logits(value: torch.Tensor) -> None:
    if value.ndim != 4: raise ValueError("expected NCHW logits")
    sums = value.detach().softmax(1).sum(1)
    if not torch.isfinite(sums).all(): raise FloatingPointError("non-finite logits")


def dense_loss(logits, target):
    _assert_logits(logits); return F.cross_entropy(logits, target)


def sparse_loss(logits, target):
    _assert_logits(logits); known = target != IGNORE_INDEX
    if not bool(known.any()): raise ValueError("no known sparse pixels")
    return F.cross_entropy(logits, target, ignore_index=IGNORE_INDEX, reduction="sum") / known.sum()


def supervision_loss(kind, logits, target):
    if kind == "dense": return dense_loss(logits, target)
    if kind == "pce": return sparse_loss(logits, target)
    raise RuntimeError("blocked_by_static_gate")

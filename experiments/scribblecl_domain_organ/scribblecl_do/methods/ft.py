from __future__ import annotations

import torch
import torch.nn.functional as F

from ..data.protocols import IGNORE_INDEX


def sparse_pce(logits: torch.Tensor, scribbles: torch.Tensor, ignore_index: int = IGNORE_INDEX) -> torch.Tensor:
    """Partial CE over explicit BG/FG pixels only; unknown contributes zero."""
    known = scribbles != ignore_index
    if not bool(known.any()):
        return logits.sum() * 0.0
    return F.cross_entropy(logits, scribbles, ignore_index=ignore_index, reduction="sum") / known.sum()

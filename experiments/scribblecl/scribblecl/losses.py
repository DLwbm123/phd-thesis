"""Small, testable loss modules ported from ZScribbleSeg concepts.

Sources: /root/ZScribble/ZScribbleSeg_MSCMR/models/segmentation.py and
engines.py.  Changes: dynamic classes, ignore masks, no hard-coded device or
task name, and no pseudo-label supervision for old/future classes.
"""
import torch
import torch.nn.functional as F
from .protocol import IGNORE_INDEX

def masked_logits(logits: torch.Tensor, allowed: tuple[int, ...]) -> torch.Tensor:
    """Mask non-protocol classes before a supervised softmax competition."""
    mask = torch.full((logits.shape[1],), -1e9, device=logits.device, dtype=logits.dtype)
    mask[list(allowed)] = 0
    return logits + mask.view(1, -1, 1, 1)

def partial_cross_entropy(logits: torch.Tensor, sparse: torch.Tensor, allowed: tuple[int, ...]) -> torch.Tensor:
    valid = sparse.ne(IGNORE_INDEX)
    if not valid.any():
        return logits.sum() * 0.0
    return F.cross_entropy(masked_logits(logits, allowed), sparse, ignore_index=IGNORE_INDEX)

def soft_partial_cross_entropy(probabilities: torch.Tensor,
                               targets: torch.Tensor) -> torch.Tensor:
    """Cross entropy for transported sparse targets with an unknown channel.

    ``targets`` contains one channel per active probability followed by the
    explicit unknown channel.  Only pixels whose known-channel mass is
    positive contribute to the loss.
    """
    known_targets = targets[:, :probabilities.shape[1]]
    known_mass = known_targets.sum(1)
    valid = known_mass.gt(0)
    if not valid.any():
        return probabilities.sum() * 0.0
    per_pixel = -(known_targets * torch.log(probabilities.clamp_min(1e-12))).sum(1)
    return per_pixel[valid].sum() / known_mass[valid].sum().clamp_min(1e-12)

def pce_ratio_flip_legacy_loss(logits: torch.Tensor, sparse: torch.Tensor, active: tuple[int, ...],
                         ratio_weight: float = 0.05) -> torch.Tensor:
    """Diagnostic-only legacy ratio loss; this is not ZScribbleSeg."""
    allowed = (0,) + active
    pce = partial_cross_entropy(logits, sparse, allowed)
    known = sparse.ne(IGNORE_INDEX)
    if not known.any():
        return pce
    return pce + ratio_weight * legacy_ratio_mse(logits, sparse, active)

def legacy_ratio_mse(logits: torch.Tensor, sparse: torch.Tensor, active: tuple[int, ...]) -> torch.Tensor:
    """Invalid legacy diagnostic, isolated from every formal method."""
    known = sparse.ne(IGNORE_INDEX)
    if not known.any(): return logits.sum() * 0.0
    allowed = (0,) + active
    observed = torch.stack([(sparse == c).float()[known].mean() for c in active])
    probs = torch.softmax(masked_logits(logits, allowed), 1)
    predicted = torch.stack([probs[:, c].mean() for c in active])
    return F.mse_loss(predicted, observed)

zs_current_task_loss = pce_ratio_flip_legacy_loss  # archived-run compatibility only

def consistency_loss(logits_a: torch.Tensor, logits_b: torch.Tensor, active: tuple[int, ...]) -> torch.Tensor:
    allowed = (0,) + active
    pa = torch.softmax(masked_logits(logits_a, allowed), 1)
    pb = torch.softmax(masked_logits(logits_b, allowed), 1)
    return F.mse_loss(pa[:, allowed], pb[:, allowed])

def scribble_mib_loss(student: torch.Tensor, teacher: torch.Tensor, sparse: torch.Tensor,
                       old: tuple[int, ...]) -> torch.Tensor:
    """Weak MiB adaptation: teacher only protects old+background on non-scribbles."""
    if not old:
        return student.sum() * 0.0
    channels = (0,) + old
    valid = sparse.eq(IGNORE_INDEX)
    if not valid.any():
        return student.sum() * 0.0
    s = F.log_softmax(student[:, channels], dim=1)
    t = F.softmax(teacher[:, channels].detach(), dim=1)
    kl = F.kl_div(s, t, reduction="none").sum(1)
    return kl[valid].mean()

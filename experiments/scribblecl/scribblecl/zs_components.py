"""Paper-compatible, Class-CL-safe ZScribbleSeg component adapters."""

from __future__ import annotations

from contextlib import contextmanager
from types import SimpleNamespace

import numpy as np
import torch
import torch.nn.functional as F
from scipy import ndimage

from .losses import masked_logits
from .protocol import IGNORE_INDEX


LAMBDA_GLOBAL = 0.05
LAMBDA_SPATIAL = 1.0
LAMBDA_SHAPE = 1.0
SPATIAL_WARMUP_EPOCH = 15
OCCLUSION_SIZE = 32
PUZZLEMIX_CONFIG = {
    "transport": True,
    "graph": True,
    "box": False,
    "mixup_alpha": 0.5,
    "neigh_size": 4,
    "n_labels": 3,
    "beta": 1.2,
    "gamma": 0.5,
    "eta": 0.2,
    "t_eps": 0.8,
    "t_size": 4,
    "adv_p": 0.0,
}


def active_probabilities(logits, allowed):
    return torch.softmax(masked_logits(logits, allowed), 1)[:, allowed]


def sparse_onehot(sparse, allowed):
    """Known channels followed by an explicit unknown channel."""
    out = torch.zeros(
        (sparse.shape[0], len(allowed) + 1, *sparse.shape[1:]),
        device=sparse.device,
    )
    for index, class_id in enumerate(allowed):
        out[:, index] = sparse == class_id
    out[:, -1] = sparse == IGNORE_INDEX
    return out.float()


def probability_pce(probs, sparse, allowed):
    known = sparse.ne(IGNORE_INDEX)
    if not known.any():
        return probs.sum() * 0
    loss = probs.sum() * 0
    for index, class_id in enumerate(allowed):
        mask = sparse.eq(class_id)
        loss = loss - torch.log(probs[:, index].clamp_min(1e-12))[mask].sum()
    return loss / known.sum()


@contextmanager
def fixed_component_seed(seed: int, cuda: bool = False):
    """Temporarily seed released components that use global NumPy/Torch RNGs."""
    numpy_state = np.random.get_state()
    torch_state = torch.random.get_rng_state()
    cuda_state = torch.cuda.get_rng_state_all() if cuda and torch.cuda.is_available() else None
    np.random.seed(seed)
    torch.manual_seed(seed)
    if cuda and torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    try:
        yield
    finally:
        np.random.set_state(numpy_state)
        torch.random.set_rng_state(torch_state)
        if cuda_state is not None:
            torch.cuda.set_rng_state_all(cuda_state)


def apply_shared_geometry(x, sparse, seed: int):
    """Paired flips and arbitrary-angle rotation shared by all formal methods."""
    from torchvision.transforms import InterpolationMode
    from torchvision.transforms import functional as TF

    rng = np.random.default_rng(seed)
    images = []
    labels = []
    parameters = []
    for image, target in zip(x, sparse):
        horizontal = bool(rng.integers(0, 2))
        vertical = bool(rng.integers(0, 2))
        angle = float(rng.uniform(0.0, 360.0))
        if horizontal:
            image, target = image.flip(-1), target.flip(-1)
        if vertical:
            image, target = image.flip(-2), target.flip(-2)
        image = TF.rotate(
            image,
            angle,
            interpolation=InterpolationMode.NEAREST,
            fill=0.0,
        )
        target = TF.rotate(
            target.unsqueeze(0),
            angle,
            interpolation=InterpolationMode.NEAREST,
            fill=IGNORE_INDEX,
        ).squeeze(0)
        images.append(image)
        labels.append(target)
        parameters.append(
            {"horizontal_flip": horizontal, "vertical_flip": vertical, "angle": angle}
        )
    return torch.stack(images), torch.stack(labels), parameters


def puzzlemix_native(model, x, sparse, allowed, seed: int):
    """Run released PuzzleMix on the native 256x256 MMWHS grid, without padding."""
    if tuple(x.shape[-2:]) != (256, 256):
        raise ValueError(f"formal MMWHS PuzzleMix requires native 256x256, got {x.shape[-2:]}")
    from .vendor.zscribble.mixup import mixup_process

    x_variable = x.detach().requires_grad_(True)
    probabilities = active_probabilities(model(x_variable), allowed)
    pce = probability_pce(probabilities, sparse, allowed)
    gradient = torch.autograd.grad(
        pce, x_variable, retain_graph=True, create_graph=False
    )[0]
    unary = torch.sqrt(torch.mean(gradient**2, dim=1))
    target = sparse_onehot(sparse, allowed)
    config = SimpleNamespace(
        mixup_alpha=PUZZLEMIX_CONFIG["mixup_alpha"],
        in_batch=False,
        mean=torch.tensor(0.0, device=x.device),
        std=torch.tensor(1.0, device=x.device),
        box=PUZZLEMIX_CONFIG["box"],
        graph=PUZZLEMIX_CONFIG["graph"],
        beta=PUZZLEMIX_CONFIG["beta"],
        gamma=PUZZLEMIX_CONFIG["gamma"],
        eta=PUZZLEMIX_CONFIG["eta"],
        neigh_size=PUZZLEMIX_CONFIG["neigh_size"],
        n_labels=PUZZLEMIX_CONFIG["n_labels"],
        transport=PUZZLEMIX_CONFIG["transport"],
        t_eps=PUZZLEMIX_CONFIG["t_eps"],
        t_size=PUZZLEMIX_CONFIG["t_size"],
        device=x.device,
        return_reverse=True,
    )
    with fixed_component_seed(seed, cuda=x.is_cuda):
        mixed, mixed_target, indices, mask, reverse_image = mixup_process(
            x_variable,
            target,
            args=config,
            grad=unary,
            noise=None,
        )
    if not torch.isfinite(mixed).all() or not torch.isfinite(mixed_target).all():
        raise FloatingPointError("non-finite PuzzleMix output")
    channel_sum = mixed_target.sum(1)
    if not torch.allclose(channel_sum, torch.ones_like(channel_sum), atol=1e-5):
        raise AssertionError("PuzzleMix target channels do not sum to one")
    shuffled = probabilities[indices]
    expected_12 = probabilities * mask + shuffled * (1 - mask)
    expected_21 = shuffled * mask + probabilities * (1 - mask)
    return {
        "mixed_image": mixed,
        "mixed_target": mixed_target,
        "indices": indices,
        "mask": mask,
        "source_probabilities": probabilities,
        "expected_12": expected_12,
        "expected_21": expected_21,
        "reverse_image": reverse_image,
        "native_shape": tuple(x.shape[-2:]),
        "adversarial_noise_enabled": False,
    }


def apply_occlusion(
    images,
    targets,
    seed: int,
    length: int = OCCLUSION_SIZE,
    mode: str = "background",
):
    """Occlude a full 32x32 square and update the sparse target explicitly."""
    if mode not in {"background", "ignore"}:
        raise ValueError(mode)
    height, width = images.shape[-2:]
    if length > height or length > width:
        raise ValueError("occlusion is larger than the input")
    rng = np.random.default_rng(seed)
    keep = torch.ones(
        (images.shape[0], 1, height, width), device=images.device, dtype=images.dtype
    )
    boxes = []
    for batch_index in range(images.shape[0]):
        y0 = int(rng.integers(0, height - length + 1))
        x0 = int(rng.integers(0, width - length + 1))
        keep[batch_index, :, y0 : y0 + length, x0 : x0 + length] = 0
        boxes.append((y0, x0, length, length))
    occluded_images = images * keep
    occluded_targets = targets.clone()
    hole = keep.eq(0).expand_as(occluded_targets)
    occluded_targets[hole] = 0
    destination = 0 if mode == "background" else occluded_targets.shape[1] - 1
    occluded_targets[:, destination : destination + 1] = torch.where(
        keep.eq(0),
        torch.ones_like(occluded_targets[:, destination : destination + 1]),
        occluded_targets[:, destination : destination + 1],
    )
    return occluded_images, occluded_targets, keep, boxes


def _negative_cosine(left, right):
    left = left.flatten(1)
    right = right.flatten(1)
    return -F.cosine_similarity(left, right, dim=1, eps=1e-8).mean()


def symmetric_global_consistency(u12, v12, u21, v21):
    """Paper Eq. (2): symmetric negative-cosine global consistency."""
    return 0.5 * (_negative_cosine(u12, v12) + _negative_cosine(u21, v21))


def largest_component_mask(mask: np.ndarray) -> np.ndarray:
    labels, count = ndimage.label(mask)
    if count == 0:
        return np.zeros_like(mask, dtype=bool)
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    return labels == sizes.argmax()


def classwise_largest_component_labels(prediction, eligible_classes):
    """Filter each eligible class independently; leave other classes untouched."""
    array = np.asarray(prediction)
    result = array.copy()
    for class_id in eligible_classes:
        keep = largest_component_mask(array == class_id)
        result[(array == class_id) & ~keep] = 0
    return result


def classwise_shape_loss(probs, sparse, eligible_classes):
    """Eq. (9) on retained unknown pixels of GT-oracle eligible classes."""
    predicted = probs.detach().argmax(1).cpu().numpy()
    unknown = sparse.eq(IGNORE_INDEX)
    values = []
    valid_count = 0
    for batch_index, prediction in enumerate(predicted):
        for class_id in eligible_classes:
            keep = largest_component_mask(prediction == class_id)
            retained = torch.as_tensor(keep, device=probs.device) & unknown[batch_index]
            if retained.any():
                values.append(
                    -torch.log(probs[batch_index, class_id].clamp_min(1e-12))[retained]
                )
                valid_count += int(retained.sum())
    loss = torch.cat(values).mean() if values else probs.sum() * 0
    return {"loss": loss, "valid_pixel_count": valid_count}


def em_ratios(probs, sparse, allowed, iterations=100, tol=1e-3):
    """Paper Eq. (4)-(5), using predictions on unlabeled pixels only."""
    labeled = sparse.ne(IGNORE_INDEX)
    unlabeled = sparse.eq(IGNORE_INDEX)
    counts = torch.stack([(sparse == class_id)[labeled].sum() for class_id in allowed]).float()
    present = counts > 0
    prior = torch.zeros(len(allowed), device=probs.device, dtype=probs.dtype)
    if not present.any():
        return prior
    frequency = counts.to(probs.device, probs.dtype) / counts.sum().clamp_min(1)
    prior[present] = frequency[present] / frequency[present].sum()
    if not unlabeled.any():
        return prior
    q = probs.permute(0, 2, 3, 1)[unlabeled].detach()
    present_indices = torch.nonzero(
        present.to(probs.device), as_tuple=False
    ).flatten()
    base = frequency[present_indices].clamp_min(1e-12)
    current = prior[present_indices]
    for _ in range(iterations):
        numerator = current * q[:, present_indices] / base
        responsibility = numerator / numerator.sum(1, keepdim=True).clamp_min(1e-12)
        updated = responsibility.mean(0)
        updated = updated / updated.sum().clamp_min(1e-12)
        if (updated - current).abs().sum() < tol:
            current = updated
            break
        current = updated
    prior[present_indices] = current
    prior[~present.to(probs.device)] = 0
    return prior


def spatial_prior_loss(probs, x, sparse, allowed, normalization="full_image"):
    """Paper Eq. (8) with the pre-registered full-image masked mean."""
    if normalization != "full_image":
        raise ValueError("formal spatial normalization is fixed to full_image")
    from .vendor.zscribble.spatial_function import ModelWeightGatedCRF

    ratios = em_ratios(probs, sparse, allowed)
    spatial = ModelWeightGatedCRF()(
        probs,
        [{"weight": 1, "xy": 6, "rgb": 0.1}],
        5,
        x.detach().clone(),
        x.shape[-2],
        x.shape[-1],
    )
    unlabeled = sparse.eq(IGNORE_INDEX)
    losses = []
    negative_counts = {}
    for channel_index, class_id in enumerate(allowed):
        if class_id == 0:
            continue
        locations = torch.nonzero(unlabeled, as_tuple=False)
        count = int(locations.shape[0])
        positive_count = int(round(count * float(ratios[channel_index])))
        negative_count = max(count - positive_count, 0)
        negative_counts[str(class_id)] = negative_count
        if negative_count == 0:
            continue
        energy = spatial[:, channel_index][unlabeled]
        negative_indices = torch.argsort(energy)[:negative_count]
        selected_locations = locations[negative_indices]
        selected_probabilities = probs[
            selected_locations[:, 0],
            channel_index,
            selected_locations[:, 1],
            selected_locations[:, 2],
        ]
        losses.append(-torch.log((1 - selected_probabilities).clamp_min(1e-12)).sum())
    denominator = probs.shape[0] * probs.shape[-2] * probs.shape[-1]
    loss = sum(losses, probs.sum() * 0) / denominator
    return {
        "loss": loss,
        "em_ratios": ratios.detach(),
        "spatial_mean": spatial.mean().detach(),
        "valid_pixel_count": sum(negative_counts.values()),
        "negative_counts": negative_counts,
        "normalization": normalization,
    }


def spatial_enabled(epoch: int) -> bool:
    return epoch >= SPATIAL_WARMUP_EPOCH


# Compatibility wrappers below are diagnostic-only and are not used by the formal ladder.
def original_puzzlemix_cutout(model, x, sparse, allowed, lambda2=0.01):
    """Released-code-compatible legacy bundle retained only for diagnostics."""
    from .vendor.zscribble.cutout import Cutout, rotate_back, rotate_invariant
    from .vendor.zscribble.mixup import mixup_process

    x_variable = x.detach().requires_grad_(True)
    probabilities = active_probabilities(model(x_variable), allowed)
    pce = probability_pce(probabilities, sparse, allowed)
    gradient = torch.autograd.grad(pce, x_variable, retain_graph=True, create_graph=False)[0]
    unary = torch.sqrt(torch.mean(gradient**2, dim=1))
    onehot = sparse_onehot(sparse, allowed)
    args = SimpleNamespace(
        mixup_alpha=0.5,
        in_batch=False,
        mean=torch.tensor(0.0, device=x.device),
        std=torch.tensor(1.0, device=x.device),
        box=False,
        graph=True,
        beta=1.2,
        gamma=0.5,
        eta=0.2,
        neigh_size=4,
        n_labels=3,
        transport=True,
        t_eps=0.8,
        t_size=4,
        device=x.device,
    )
    mixed, mixed_target, indices, mask = mixup_process(
        x_variable, onehot, args=args, grad=unary, noise=None
    )
    cut, cut_target, cut_mask = Cutout(mixed, mixed_target, x.device)
    cut, cut_target, angles = rotate_invariant(cut, cut_target)
    cut_probs = active_probabilities(model(cut), allowed)
    _, cut_back, cut_target = rotate_back(
        cut, cut_probs, cut_target[:, : len(allowed)], angles
    )
    cut_probs = cut_back["pred_masks"]
    annotated = cut_target.sum(1, keepdim=True)
    augmentation = (-cut_target * torch.log(cut_probs.clamp_min(1e-12))).sum(
        1, keepdim=True
    )
    augmentation = (augmentation * annotated).mean()
    shuffled = probabilities[indices]
    expected = (probabilities * mask + shuffled * (1 - mask)) * cut_mask[:, :1]
    consistency_raw = 1 - F.cosine_similarity(cut_probs, expected, dim=1).mean()
    return {
        "augmentation": augmentation,
        "consistency": lambda2 * consistency_raw,
        "consistency_unweighted": consistency_raw,
        "puzzlemix_mask_mean": mask.mean().detach(),
    }


def integrity_loss(probs, sparse):
    return classwise_shape_loss(probs, sparse, range(1, probs.shape[1]))["loss"]


def spatial_pseudo_correction(probs, x, sparse, allowed):
    result = spatial_prior_loss(probs, x, sparse, allowed)
    return {
        "pseudo": result["loss"],
        "em_ratios": result["em_ratios"],
        "spatial_mean": result["spatial_mean"],
    }


def component_gradient_norm(loss, model):
    if not loss.requires_grad:
        return 0.0
    gradients = torch.autograd.grad(
        loss,
        [parameter for parameter in model.parameters() if parameter.requires_grad],
        retain_graph=True,
        allow_unused=True,
    )
    terms = [(gradient.detach() ** 2).sum() for gradient in gradients if gradient is not None]
    total = sum(terms, torch.tensor(0.0, device=loss.device))
    return float(torch.sqrt(total))

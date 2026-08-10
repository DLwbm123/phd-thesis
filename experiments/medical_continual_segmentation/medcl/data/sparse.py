from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import numpy as np
from scipy import ndimage as ndi
from skimage.morphology import skeletonize

from .protocols import IGNORE_INDEX


@dataclass
class AnnotationStats:
    foreground_pixels: int
    background_pixels: int
    unknown_pixels: int
    dense_foreground_pixels: int
    zero_foreground_slices: int
    minimum_valid_pixels: int
    maximum_valid_pixels: int


def _background(mask: np.ndarray, seed: int, index: int) -> np.ndarray:
    safe = ndi.distance_transform_edt(~mask) >= 5
    h, w = mask.shape; out = np.zeros_like(mask, dtype=bool)
    rng = np.random.default_rng(seed * 1_000_003 + index); span = 28
    x = int(rng.integers(8, max(9, w - span - 8))); y = int(rng.integers(8, max(9, h - span - 8)))
    out[4:7, x:x+span] = True; out[h-7:h-4, w-x-span:w-x] = True
    out[y:y+span, 4:7] = True; out[h-y-span:h-y, w-7:w-4] = True
    return out & safe


def _expand(seed_mask: np.ndarray, allowed: np.ndarray, multiplier: float) -> np.ndarray:
    """Deterministically grow a stroke only within its semantically valid area."""
    if multiplier <= 1:
        return seed_mask & allowed
    target = min(int(allowed.sum()), int(round(seed_mask.sum() * multiplier)))
    if target <= int(seed_mask.sum()):
        return seed_mask & allowed
    distance = ndi.distance_transform_edt(~seed_mask)
    candidates = np.flatnonzero(allowed)
    order = np.lexsort((candidates, distance.ravel()[candidates]))
    chosen = candidates[order[:target]]
    output = np.zeros(allowed.shape, dtype=bool, order="C")
    # ``allowed`` originates from transposed H5 slices and may be
    # non-contiguous.  Both the target and its flat indexing must be C-order;
    # otherwise a later boolean assignment can move background candidates.
    output.flat[chosen] = True
    return output


def generate(labels: np.ndarray, shift: int, seed: int = 42, foreground_area_multiplier: float = 1.0, background_area_multiplier: float = 1.0) -> tuple[np.ndarray, AnnotationStats]:
    if foreground_area_multiplier < 1 or background_area_multiplier < 1:
        raise ValueError("area multipliers must be >= 1")
    result = np.full(labels.shape, IGNORE_INDEX, dtype=np.int16)
    for index, dense in enumerate(labels):
        foreground = dense > 0
        for local_class in sorted(set(np.unique(dense).tolist()) - {0}):
            line = ndi.binary_dilation(skeletonize(dense == local_class), iterations=1) & (dense == local_class)
            line = _expand(line, dense == local_class, foreground_area_multiplier)
            result[index][line] = int(local_class) + int(shift)
        base_bg = _background(foreground, seed, index) & (result[index] == IGNORE_INDEX)
        bg = _expand(base_bg, (~foreground) & (result[index] == IGNORE_INDEX), background_area_multiplier)
        result[index][bg] = 0
    valid = result != IGNORE_INDEX
    stats = AnnotationStats(int((result > 0).sum()), int((result == 0).sum()), int((result == IGNORE_INDEX).sum()), int((labels > 0).sum()), int((~(result > 0).reshape(len(result), -1).any(1)).sum()), int(valid.reshape(len(result), -1).sum(1).min()), int(valid.reshape(len(result), -1).sum(1).max()))
    return result, stats


def scale_existing(labels: np.ndarray, annotations: np.ndarray, shift: int, foreground_area_multiplier: float, background_area_multiplier: float) -> tuple[np.ndarray, AnnotationStats]:
    """Scale the *persisted* v2 strokes, retaining the exact current baseline."""
    if labels.shape != annotations.shape:
        raise ValueError("labels and annotations must have identical shapes")
    if foreground_area_multiplier < 1 or background_area_multiplier < 1:
        raise ValueError("area multipliers must be >= 1")
    result = np.full(labels.shape, IGNORE_INDEX, dtype=np.int16)
    for index, dense in enumerate(labels):
        foreground = dense > 0; old = annotations[index]
        for local_class in sorted(set(np.unique(dense).tolist()) - {0}):
            value = int(local_class) + int(shift)
            expanded = _expand(old == value, dense == local_class, foreground_area_multiplier)
            result[index][expanded] = value
        expanded_bg = _expand(old == 0, (~foreground) & (result[index] == IGNORE_INDEX), background_area_multiplier)
        result[index][expanded_bg] = 0
    valid = result != IGNORE_INDEX
    stats = AnnotationStats(int((result > 0).sum()), int((result == 0).sum()), int((result == IGNORE_INDEX).sum()), int((labels > 0).sum()), int((~(result > 0).reshape(len(result), -1).any(1)).sum()), int(valid.reshape(len(result), -1).sum(1).min()), int(valid.reshape(len(result), -1).sum(1).max()))
    return result, stats


def digest(array: np.ndarray, metadata: dict) -> str:
    h = sha256(); h.update(np.ascontiguousarray(array).tobytes()); h.update(json.dumps(metadata, sort_keys=True).encode()); return h.hexdigest()

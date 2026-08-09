"""Deterministic FG/BG/unknown v2 binary scribble generation."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi
from skimage.morphology import skeletonize

from .protocols import IGNORE_INDEX


LEVEL_BY_WIDTH = {1: "s1", 3: "s2", 5: "s3"}


def scribble_filename(task_code: str, seed: int, width: int = 3) -> str:
    """Return a strategy-level name; Benchmark v2 S2 is the 3 px rule."""
    if width not in LEVEL_BY_WIDTH:
        raise ValueError("bounded S1/S2/S3 widths are 1, 3 or 5")
    return f"{task_code}_v2_{LEVEL_BY_WIDTH[width]}_seed{int(seed)}.npz"


def scribble_path(root: str | Path, scenario: str, task_code: str, seed: int, width: int = 3) -> Path:
    return Path(root) / scenario / scribble_filename(task_code, seed, width)


@dataclass(frozen=True)
class ScribbleStats:
    slices: int
    foreground_pixels: int
    background_pixels: int
    unknown_pixels: int
    dense_foreground_pixels: int
    positive_slices: int
    zero_fg_slices: int
    min_valid_per_slice: int
    max_valid_per_slice: int

    @property
    def fg_coverage(self) -> float:
        return self.foreground_pixels / max(1, self.dense_foreground_pixels)

    @property
    def bg_annotation_ratio(self) -> float:
        total = self.slices * 256 * 256
        return self.background_pixels / total

    @property
    def total_annotation_ratio(self) -> float:
        total = self.slices * 256 * 256
        return (self.foreground_pixels + self.background_pixels) / total


def _background_strokes(mask: np.ndarray, seed: int, slice_index: int) -> np.ndarray:
    """Sparse deterministic border/interior BG strokes away from foreground."""
    safe = ndi.distance_transform_edt(~mask) >= 5
    h, w = mask.shape
    bg = np.zeros_like(mask, dtype=bool)
    # Four short border strokes.  Positions are deterministic but domain/task
    # independent, so no future data can influence them.
    rng = np.random.default_rng(seed * 1_000_003 + slice_index)
    span = 28
    x = int(rng.integers(8, max(9, w - span - 8)))
    y = int(rng.integers(8, max(9, h - span - 8)))
    bg[4:7, x : x + span] = True
    bg[h - 7 : h - 4, w - x - span : w - x] = True
    bg[y : y + span, 4:7] = True
    bg[h - y - span : h - y, w - 7 : w - 4] = True
    # A short safe interior diagonal gives explicit BG even on cropped FOVs.
    cy, cx = h // 2, w // 2
    for d in range(-10, 11):
        yy, xx = cy + d, cx + d
        if 0 <= yy < h and 0 <= xx < w:
            bg[yy, xx] = True
    return bg & safe


def generate_binary_scribble(mask: np.ndarray, width: int = 3, seed: int = 42, slice_index: int = 0) -> np.ndarray:
    """Return -100 unknown, 0 explicit BG and 1 explicit FG."""
    if width not in LEVEL_BY_WIDTH:
        raise ValueError("bounded S1/S2/S3 widths are 1, 3 or 5")
    dense = np.asarray(mask, dtype=np.int64) == 1
    out = np.full(dense.shape, IGNORE_INDEX, dtype=np.int16)
    if dense.any():
        fg = skeletonize(dense)
        if width > 1:
            fg = ndi.binary_dilation(fg, iterations=(width - 1) // 2)
        fg &= dense
        out[fg] = 1
    bg = _background_strokes(dense, seed, slice_index)
    bg &= out != 1
    out[bg] = 0
    return out


def generate_volume_scribbles(masks: np.ndarray, width: int = 3, seed: int = 42) -> tuple[np.ndarray, ScribbleStats]:
    if masks.ndim != 3:
        raise ValueError("expected [N,H,W]")
    result = np.stack([generate_binary_scribble(m, width, seed, i) for i, m in enumerate(masks)])
    valid = result != IGNORE_INDEX
    dense_fg = masks == 1
    stats = ScribbleStats(
        slices=int(len(result)),
        foreground_pixels=int((result == 1).sum()),
        background_pixels=int((result == 0).sum()),
        unknown_pixels=int((result == IGNORE_INDEX).sum()),
        dense_foreground_pixels=int(dense_fg.sum()),
        positive_slices=int(dense_fg.reshape(len(result), -1).any(1).sum()),
        zero_fg_slices=int((~(result == 1).reshape(len(result), -1).any(1)).sum()),
        min_valid_per_slice=int(valid.reshape(len(result), -1).sum(1).min()),
        max_valid_per_slice=int(valid.reshape(len(result), -1).sum(1).max()),
    )
    return result, stats


def scribble_hash(scribbles: np.ndarray, metadata: dict) -> str:
    h = sha256()
    h.update(np.ascontiguousarray(scribbles).tobytes())
    h.update(json.dumps(metadata, sort_keys=True, separators=(",", ":")).encode())
    return h.hexdigest()

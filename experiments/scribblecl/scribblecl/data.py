"""HDF5 data adapter. Dense train labels are intentionally generator-only."""
from pathlib import Path
import h5py
import numpy as np
import torch
from torch.utils.data import Dataset
from .protocol import IGNORE_INDEX, stage

class MMWHS(Dataset):
    def __init__(self, root: str, stage_index: int, split: str, scribble_file: str | None = None):
        spec = stage(stage_index); self.path = Path(root) / spec.h5_name
        self.split, self.spec = split, spec
        with h5py.File(self.path, "r") as h:
            self.images = h[f"{split}_images"][:].transpose(2, 0, 1).astype("float32")
            self.patient_info = list(h[f"patient_info_{'test' if split == 'test' else 'val'}"][:]) if split != "train" else None
            if split == "train":
                if not scribble_file: raise ValueError("train requires offline scribbles")
                self.sparse = np.load(scribble_file)["scribbles"].astype("int16")
            else:
                local = h[f"{split}_labels"][:].transpose(2, 0, 1).astype("int16")
                self.dense = np.zeros_like(local)
                for src, dst in spec.local_to_global.items(): self.dense[local == src] = dst
    def __len__(self): return len(self.images)
    def __getitem__(self, i):
        # Benchmark adapter applies no intensity normalization to the H5 slice.
        x = torch.from_numpy(self.images[i]).unsqueeze(0)
        if self.split == "train": return x, torch.from_numpy(self.sparse[i]).long()
        return x, torch.from_numpy(self.dense[i]).long()

class DenseMMWHS(MMWHS):
    """Reference-only dataset; dense labels are permitted by the protocol."""
    def __init__(self, root: str, stage_index: int, split: str = "train"):
        spec = stage(stage_index); self.path = Path(root) / spec.h5_name
        self.split, self.spec = split, spec
        with h5py.File(self.path, "r") as h:
            self.images = h[f"{split}_images"][:].transpose(2, 0, 1).astype("float32")
            self.patient_info = None
            local = h[f"{split}_labels"][:].transpose(2, 0, 1).astype("int16")
            self.dense = np.zeros_like(local)
            for src, dst in spec.local_to_global.items(): self.dense[local == src] = dst
    def __getitem__(self, i):
        x = torch.from_numpy(self.images[i]).unsqueeze(0)
        return x, torch.from_numpy(self.dense[i]).long()

def make_sparse(local: np.ndarray, stage_index: int, skeletonize, width: int = 3) -> np.ndarray:
    spec = stage(stage_index); out = np.full(local.shape, IGNORE_INDEX, dtype=np.int16)
    for src, dst in spec.local_to_global.items():
        mask = local == src
        if mask.any():
            skel = skeletonize(mask)
            # Dilation remains inside the same current class; never accesses other labels.
            from scipy.ndimage import binary_dilation
            grown = binary_dilation(skel, iterations=(width - 1) // 2) if width > 1 else skel
            out[grown & mask] = dst
    return out

def make_sparse_v2(local: np.ndarray, stage_index: int, skeletonize, width: int = 3,
                   background_margin: int = 5, background_stroke_length: int = 16) -> np.ndarray:
    """Deterministic FG/BG/unknown labels using only a stage-local label map."""
    from scipy.ndimage import binary_dilation, distance_transform_edt
    spec = stage(stage_index)
    out = np.full(local.shape, IGNORE_INDEX, dtype=np.int16)
    current_fg = np.zeros(local.shape, dtype=bool)
    for src, dst in spec.local_to_global.items():
        mask = local == src
        current_fg |= mask
        if mask.any():
            skel = skeletonize(mask)
            grown = binary_dilation(skel, iterations=(width - 1) // 2) if width > 1 else skel
            out[grown & mask] = dst

    local_background = local == 0
    safe = local_background & (distance_transform_edt(local_background) >= background_margin)
    if not safe.any():
        raise ValueError("no stage-local background satisfies the safety margin")

    bg = np.zeros_like(safe)
    h, w = safe.shape
    # Stable body-exterior/border strokes.
    for row in (0, min(1, h - 1), max(0, h - 2), h - 1):
        xs = np.flatnonzero(safe[row])
        if xs.size:
            start = xs[(xs.size - 1) // 2]
            bg[row, start:min(w, start + background_stroke_length)] |= safe[row, start:min(w, start + background_stroke_length)]
    # Deterministic short interior strokes, independent of foreground width.
    for row in np.linspace(0, h - 1, 5, dtype=int)[1:-1]:
        xs = np.flatnonzero(safe[row])
        if not xs.size:
            continue
        splits = np.split(xs, np.flatnonzero(np.diff(xs) > 1) + 1)
        segment = max(splits, key=len)
        start = segment[max(0, (len(segment) - background_stroke_length) // 2)]
        bg[row, start:min(w, start + background_stroke_length)] |= safe[row, start:min(w, start + background_stroke_length)]
    if not bg.any():
        y, x = np.argwhere(safe)[0]
        bg[y, x] = True
    assert not np.any(bg & current_fg)
    out[bg] = 0
    return out

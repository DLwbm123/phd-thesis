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
            if split == "train":
                if not scribble_file: raise ValueError("train requires offline scribbles")
                self.sparse = np.load(scribble_file)["scribbles"].astype("int16")
            else:
                local = h[f"{split}_labels"][:].transpose(2, 0, 1).astype("int16")
                self.dense = np.zeros_like(local)
                for src, dst in spec.local_to_global.items(): self.dense[local == src] = dst
    def __len__(self): return len(self.images)
    def __getitem__(self, i):
        x = torch.from_numpy((self.images[i] - self.images[i].mean()) / (self.images[i].std() + 1e-6)).unsqueeze(0)
        if self.split == "train": return x, torch.from_numpy(self.sparse[i]).long()
        return x, torch.from_numpy(self.dense[i]).long()

class DenseMMWHS(MMWHS):
    """Reference-only dataset; dense labels are permitted by the protocol."""
    def __init__(self, root: str, stage_index: int, split: str = "train"):
        spec = stage(stage_index); self.path = Path(root) / spec.h5_name
        self.split, self.spec = split, spec
        with h5py.File(self.path, "r") as h:
            self.images = h[f"{split}_images"][:].transpose(2, 0, 1).astype("float32")
            local = h[f"{split}_labels"][:].transpose(2, 0, 1).astype("int16")
            self.dense = np.zeros_like(local)
            for src, dst in spec.local_to_global.items(): self.dense[local == src] = dst
    def __getitem__(self, i):
        x = torch.from_numpy((self.images[i] - self.images[i].mean()) / (self.images[i].std() + 1e-6)).unsqueeze(0)
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

from __future__ import annotations

from pathlib import Path
import h5py
import numpy as np
import torch
from torch.utils.data import Dataset

from .protocols import IGNORE_INDEX, Task


def dataset_path(root: str | Path, task: Task) -> Path:
    return Path(root) / task.folder / task.file


def patient_ranges(ends) -> list[tuple[int, int]]:
    ends = [int(x) for x in ends]
    starts = [0] + [x + 1 for x in ends[:-1]]
    return list(zip(starts, [x + 1 for x in ends]))


class DenseDataset(Dataset):
    exposes_dense = True

    def __init__(self, path: str | Path, split: str, label_shift: int = 0):
        self.path, self.split, self.label_shift = str(path), split, int(label_shift)
        with h5py.File(self.path, "r") as handle:
            self.length = int(handle[f"{split}_images"].shape[2])
            key = f"patient_info_{split}"
            self.patient_info = np.asarray(handle[key][:], dtype=np.int64)
        self._handle = None

    def _open(self):
        if self._handle is None:
            self._handle = h5py.File(self.path, "r")
        return self._handle

    def __len__(self): return self.length

    def __getitem__(self, index):
        h = self._open()
        image = np.asarray(h[f"{self.split}_images"][:, :, index], dtype=np.float32)
        target = np.asarray(h[f"{self.split}_labels"][:, :, index]).astype(np.int64)
        if self.label_shift:
            target = np.where(target > 0, target + self.label_shift, 0)
        return torch.from_numpy(image[None]), torch.from_numpy(target.copy()).long()

    def close(self):
        if self._handle is not None: self._handle.close(); self._handle = None


class SparseDataset(Dataset):
    exposes_dense = False

    def __init__(self, path: str | Path, annotation_path: str | Path):
        self.path = str(path); self._handle = None
        with h5py.File(self.path, "r") as handle:
            self.images = np.asarray(handle["train_images"][:], dtype=np.float32).transpose(2, 0, 1)
        archive = np.load(annotation_path, allow_pickle=False)
        if set(archive.files) != {"annotations"}: raise ValueError("sparse archive contract violation")
        self.annotations = np.asarray(archive["annotations"], dtype=np.int16)
        if self.annotations.shape != self.images.shape: raise ValueError("annotation shape mismatch")
        if not set(np.unique(self.annotations).tolist()) <= set(range(8)) | {IGNORE_INDEX}:
            raise ValueError("invalid sparse labels")

    def __len__(self): return len(self.images)
    def __getitem__(self, index):
        return torch.from_numpy(self.images[index][None]), torch.from_numpy(self.annotations[index].astype(np.int64, copy=True)).long()
    def close(self): self.images = None

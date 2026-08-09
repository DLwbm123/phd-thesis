"""Benchmark-compatible dense and weak HDF5 datasets.

The weak loader intentionally has no dense-mask path or dense-label handle.
It reads images from the immutable Benchmark HDF5 and sparse labels from a
separate NPZ created offline.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterator

import h5py
import numpy as np
import torch
from torch.utils.data import Dataset

from .protocols import IGNORE_INDEX


def patient_ranges(last_indices: np.ndarray | list[int]) -> list[tuple[int, int]]:
    """Convert Benchmark inclusive patient-end indices to half-open ranges."""
    ends = [int(x) for x in last_indices]
    starts = [0] + [x + 1 for x in ends[:-1]]
    return list(zip(starts, [x + 1 for x in ends]))


def _effective_mask(a: np.ndarray) -> np.ndarray:
    # Exact executable behavior: cv2.resize to the already-256x256 shape,
    # followed by torch.long.  Stored interpolated boundary values in (0,1)
    # therefore become background.
    return np.asarray(a).astype(np.int64, copy=False)


class DenseH5Dataset(Dataset):
    """Dense labels, allowed only for audit/generation/evaluation/tiny gates."""

    exposes_dense = True

    def __init__(self, h5_path: str | Path, split: str):
        if split not in {"train", "val", "test"}:
            raise ValueError(split)
        self.h5_path = str(h5_path)
        self.split = split
        self._file: h5py.File | None = None
        with h5py.File(self.h5_path, "r") as h:
            self.length = int(h[f"{split}_images"].shape[2])
            key = f"patient_info_{split}"
            self.patient_info = np.asarray(h[key][:], dtype=np.int64) if key in h else np.asarray([], dtype=np.int64)

    def _open(self) -> h5py.File:
        if self._file is None:
            self._file = h5py.File(self.h5_path, "r")
        return self._file

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        h = self._open()
        image = np.asarray(h[f"{self.split}_images"][:, :, index], dtype=np.float32)
        mask = _effective_mask(h[f"{self.split}_labels"][:, :, index])
        return torch.from_numpy(image[None]), torch.from_numpy(mask.copy()).long()

    def close(self) -> None:
        if self._file is not None:
            self._file.close()
            self._file = None


class WeakH5Dataset(Dataset):
    """Training-only image+sparse-label loader that cannot access dense masks."""

    exposes_dense = False

    def __init__(self, h5_path: str | Path, scribble_npz: str | Path, preload_current_images: bool = True):
        self.h5_path = str(h5_path)
        self.scribble_npz = str(scribble_npz)
        self._file: h5py.File | None = None
        with h5py.File(self.h5_path, "r") as h:
            self.length = int(h["train_images"].shape[2])
            self.spatial_shape = tuple(int(x) for x in h["train_images"].shape[:2])
            # Current-stage images may reside in RAM only for the lifetime of
            # this dataset. No label or historical-stage image is cached.
            self.current_images = (
                np.asarray(h["train_images"][:], dtype=np.float32).transpose(2, 0, 1)
                if preload_current_images
                else None
            )
        archive = np.load(self.scribble_npz, allow_pickle=False, mmap_mode="r")
        if set(archive.files) != {"scribbles"}:
            raise ValueError("weak archive must contain only sparse scribbles")
        scribbles = np.asarray(archive["scribbles"])
        if scribbles.shape != (self.length, *self.spatial_shape):
            raise ValueError(f"scribble shape {scribbles.shape} does not match train split")
        values = set(np.unique(scribbles).tolist())
        if not values <= {IGNORE_INDEX, 0, 1}:
            raise ValueError(f"invalid sparse labels: {values}")
        self.scribbles = scribbles.astype(np.int16, copy=False)

    def _open(self) -> h5py.File:
        if self._file is None:
            self._file = h5py.File(self.h5_path, "r")
        return self._file

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        image = self.current_images[index] if self.current_images is not None else np.asarray(self._open()["train_images"][:, :, index], dtype=np.float32)
        sparse = np.asarray(self.scribbles[index], dtype=np.int64)
        return torch.from_numpy(image[None]), torch.from_numpy(sparse.copy()).long()

    def close(self) -> None:
        if self._file is not None:
            self._file.close()
            self._file = None
        self.current_images = None

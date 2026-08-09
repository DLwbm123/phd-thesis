from __future__ import annotations

from pathlib import Path
import sys

import h5py
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


@pytest.fixture
def binary_h5(tmp_path):
    path = tmp_path / "tiny.h5"
    with h5py.File(path, "w") as h:
        for split, n in (("train", 4), ("val", 2), ("test", 2)):
            images = np.random.default_rng(7).normal(size=(16, 16, n)).astype(np.float32)
            labels = np.zeros((16, 16, n), dtype=np.float32)
            labels[4:12, 4:12, :] = 1
            h[f"{split}_images"] = images
            h[f"{split}_labels"] = labels
            h[f"patient_info_{split}"] = np.asarray([n - 1], dtype=np.int64)
    return path


@pytest.fixture
def sparse_npz(tmp_path):
    path = tmp_path / "sparse.npz"
    labels = np.full((4, 16, 16), -100, dtype=np.int16)
    labels[:, 0, :4] = 0
    labels[:, 6:10, 8] = 1
    np.savez_compressed(path, scribbles=labels)
    return path

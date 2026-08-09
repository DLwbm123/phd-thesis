from __future__ import annotations

import h5py
import numpy as np

from scribblecl_do.data.h5_dataset import DenseH5Dataset, WeakH5Dataset, patient_ranges
from scribblecl_do.data.protocols import DOMAIN_TASKS, ORGAN_TASKS
from scribblecl_do.data.scribbles import generate_binary_scribble


def test_domain_order_matches_benchmark():
    assert [x.h5_name for x in DOMAIN_TASKS] == ["BIDMC.h5", "HK.h5", "ISBI.h5", "UCL.h5", "ISBI_1.5.h5", "I2CVB.h5"]
    assert [x.code for x in DOMAIN_TASKS] == list("ABCDEF")


def test_organ_order_matches_benchmark():
    assert [x.h5_name for x in ORGAN_TASKS] == ["UtahI.h5", "UCL.h5", "Lits.h5", "brain.h5"]
    assert [x.foreground for x in ORGAN_TASKS] == ["left atrium", "prostate", "liver", "brain tumor"]


def test_splits_match_benchmark():
    domain_train = [301, 168, 345, 166, 582, 704]
    organ_train = [762, 166, 1421, 1963]
    assert sum(domain_train) == 2266
    assert sum(organ_train) == 4312


def test_patient_boundaries_are_inclusive_ends():
    assert patient_ranges([2, 5]) == [(0, 3), (3, 6)]


def test_no_dense_label_in_weak_loader(binary_h5, sparse_npz):
    weak = WeakH5Dataset(binary_h5, sparse_npz)
    assert weak.exposes_dense is False
    weak[0]
    assert weak.current_images is not None and weak._file is None
    assert not hasattr(weak, "labels") and not hasattr(weak, "dense")
    weak.close(); assert weak.current_images is None


def test_dense_loader_is_explicit(binary_h5):
    assert DenseH5Dataset(binary_h5, "train").exposes_dense is True


def test_scribble_bg_fg_unknown_partition():
    mask = np.zeros((64, 64), dtype=np.uint8); mask[20:44, 22:42] = 1
    scribble = generate_binary_scribble(mask, width=3, seed=42)
    assert set(np.unique(scribble)) == {-100, 0, 1}
    assert np.all(scribble[scribble == 1] == mask[scribble == 1])
    assert not np.any((scribble == 0) & (mask == 1))


def test_no_future_data_access():
    mask = np.zeros((32, 32), dtype=np.uint8); mask[8:24, 8:24] = 1
    a = generate_binary_scribble(mask, width=3, seed=42)
    b = generate_binary_scribble(mask, width=3, seed=42)
    assert np.array_equal(a, b)

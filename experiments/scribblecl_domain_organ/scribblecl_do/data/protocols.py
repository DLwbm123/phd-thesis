"""Frozen metadata transcribed from the remote Benchmark executable tree.

Paths are resolved from an explicit data root.  This module never probes an
alternative split or creates a random split.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Mapping, Sequence

IGNORE_INDEX = -100


@dataclass(frozen=True)
class TaskSpec:
    index: int
    code: str
    name: str
    h5_name: str
    source: str
    modality: str
    foreground: str
    shared_semantics: bool


# seq_prostate.py maps task ids 1..6 to these exact HDF5 files.  The A..F
# names and dataset sources come from the Benchmark protocol, while the HDF5
# mapping comes from the executable loader.
DOMAIN_TASKS: tuple[TaskSpec, ...] = (
    TaskSpec(0, "A", "Center A", "BIDMC.h5", "NCI-ISBI 2013", "T2 MRI", "prostate", True),
    TaskSpec(1, "B", "Center B", "HK.h5", "NCI-ISBI 2013", "T2 MRI", "prostate", True),
    TaskSpec(2, "C", "Center C", "ISBI.h5", "I2CVB", "T2 MRI", "prostate", True),
    TaskSpec(3, "D", "Center D", "UCL.h5", "PROMISE12", "T2 MRI", "prostate", True),
    TaskSpec(4, "E", "Center E", "ISBI_1.5.h5", "PROMISE12", "T2 MRI", "prostate", True),
    TaskSpec(5, "F", "Center F", "I2CVB.h5", "PROMISE12", "T2 MRI", "prostate", True),
)

ORGAN_TASKS: tuple[TaskSpec, ...] = (
    TaskSpec(0, "T1", "left atrium", "UtahI.h5", "LAScarQS", "LGE MRI", "left atrium", False),
    TaskSpec(1, "T2", "prostate", "UCL.h5", "PROMISE12 Center D", "T2 MRI", "prostate", False),
    TaskSpec(2, "T3", "liver", "Lits.h5", "LiTS", "CT", "liver", False),
    TaskSpec(3, "T4", "brain tumor", "brain.h5", "FeTS 2021", "FLAIR MRI", "brain tumor", False),
)

# Full-file SHA-256 values computed on the remote immutable Benchmark HDF5s.
EXPECTED_H5_SHA256: Mapping[str, str] = {
    "Domain_Prostate/BIDMC.h5": "66e24bbda2717b59fe086d7bcb17de550e3c2452bcca61a0b200f6599f25dc52",
    "Domain_Prostate/HK.h5": "9729bd78317a3279a6ff1148a123c4a6637c71ad2833bfd393346ff6d7157f06",
    "Domain_Prostate/ISBI.h5": "9a1a9503d456604321f23f25732081978ef43a00fdf66e470f1b4725c55d02d3",
    "Domain_Prostate/UCL.h5": "76ef6354b8156a637da058357e807992ea5a1d6ceb2e70104689e67810d798a9",
    "Domain_Prostate/ISBI_1.5.h5": "2370e1239fef32b976e93e5bdc1622f3449a44b270e58ac07a932eea5b076126",
    "Domain_Prostate/I2CVB.h5": "1c1f49ab26b828f5b33fb48c8843d9e766bf6c3b083e238c55338b132f0b79ee",
    "Task_incre/UtahI.h5": "4b9cc27f7519f6b94d4886a7bc6771b1420ce1cec508d6a31efd65f4b3b0e26d",
    "Task_incre/UCL.h5": "76ef6354b8156a637da058357e807992ea5a1d6ceb2e70104689e67810d798a9",
    "Task_incre/Lits.h5": "b0a2a0a50cef089a2e33ded07de60783473b870028fdddfaba97c79fc976be9c",
    "Task_incre/brain.h5": "84edefa8eb88a958f377e27b8125d243996a3d3ca217f422ebb8f93f50eab90e",
}


def order_checksum(tasks: Sequence[TaskSpec]) -> str:
    payload = [
        {"index": t.index, "code": t.code, "h5": t.h5_name, "source": t.source, "foreground": t.foreground}
        for t in tasks
    ]
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


DOMAIN_ORDER_SHA256 = order_checksum(DOMAIN_TASKS)
ORGAN_ORDER_SHA256 = order_checksum(ORGAN_TASKS)

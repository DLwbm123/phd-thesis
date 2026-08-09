from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json

IGNORE_INDEX = -100


@dataclass(frozen=True)
class Task:
    index: int
    code: str
    folder: str
    file: str
    classes: tuple[str, ...]
    label_shift: int = 0


CLASS_TASKS = (
    Task(0, "T1", "MMWHS", "myo_lv_la.h5", ("MYO", "LV", "LA"), 0),
    Task(1, "T2", "MMWHS", "ra_rv.h5", ("RA", "RV"), 3),
    Task(2, "T3", "MMWHS", "ao_pa.h5", ("AO", "PA"), 5),
)
DOMAIN_TASKS = tuple(
    Task(i, code, "Domain_Prostate", file, ("prostate",), 0)
    for i, (code, file) in enumerate((
        ("A", "BIDMC.h5"), ("B", "HK.h5"), ("C", "ISBI.h5"),
        ("D", "UCL.h5"), ("E", "ISBI_1.5.h5"), ("F", "I2CVB.h5"),
    ))
)
ORGAN_TASKS = tuple(
    Task(i, code, "Task_incre", file, (name,), 0)
    for i, (code, file, name) in enumerate((
        ("T1", "UtahI.h5", "left_atrium"), ("T2", "UCL.h5", "prostate"),
        ("T3", "Lits.h5", "liver"), ("T4", "brain.h5", "brain_tumor"),
    ))
)

EXPECTED_SHA256 = {
    "MMWHS/myo_lv_la.h5": "1f3d2cbccf977200ffdd02ce69c28032e0617c221c26c8727181c3e563abf4c1",
    "MMWHS/ra_rv.h5": "dc27406b3147ca6ff86faf5838766359f5e771ce0703e149ed332a263cb28ec3",
    "MMWHS/ao_pa.h5": "785b823825e6ea0b38cc27247632980902ca3a37d764c2f5ce73dbbff94c5834",
    "MMWHS/whole_heart_test.h5": "4d22c59d2e3cde018ee5b0fd7088d3891731999f452608708f0a1b8e017d011f",
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


def tasks_for(scenario: str) -> tuple[Task, ...]:
    return {"class": CLASS_TASKS, "domain": DOMAIN_TASKS, "organ": ORGAN_TASKS}[scenario]


def order_sha256(tasks: tuple[Task, ...]) -> str:
    value = [(x.index, x.code, x.folder, x.file, x.classes, x.label_shift) for x in tasks]
    return sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()

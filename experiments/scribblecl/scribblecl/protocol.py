"""Source: Benchmark_pa/datasets/seq_mmwhs.py; adapted to explicit metadata."""
from dataclasses import dataclass

IGNORE_INDEX = -100
NUM_CLASSES = 8

@dataclass(frozen=True)
class Stage:
    index: int
    h5_name: str
    active: tuple[int, ...]
    local_to_global: dict[int, int]

STAGES = (
    Stage(1, "myo_lv_la.h5", (1, 2, 3), {1: 1, 2: 2, 3: 3}),
    Stage(2, "ra_rv.h5", (4, 5), {1: 4, 2: 5}),
    Stage(3, "ao_pa.h5", (6, 7), {1: 6, 2: 7}),
)

def stage(index: int) -> Stage:
    return STAGES[index - 1]

def old_classes(index: int) -> tuple[int, ...]:
    return tuple(c for item in STAGES[: index - 1] for c in item.active)

def future_classes(index: int) -> tuple[int, ...]:
    return tuple(c for item in STAGES[index:] for c in item.active)

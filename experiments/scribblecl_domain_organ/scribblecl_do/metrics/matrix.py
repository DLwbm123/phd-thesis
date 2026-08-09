from __future__ import annotations

import numpy as np


def _square(matrix) -> np.ndarray:
    x = np.asarray(matrix, dtype=np.float64)
    if x.ndim != 2 or x.shape[0] != x.shape[1]:
        raise ValueError("performance matrix must be square")
    return x


def adice(matrix) -> float:
    x = _square(matrix)
    return float(np.mean(x[-1]))


def bwtr(matrix) -> float:
    x = _square(matrix)
    diagonal = np.diag(x)[:-1]
    if np.any(diagonal <= 0):
        raise ValueError("BWTR requires positive task-acquisition Dice")
    return float(np.mean((x[-1, :-1] - diagonal) / diagonal))


def rma(matrix, independent_scores) -> float:
    x = _square(matrix)
    ref = np.asarray(independent_scores, dtype=np.float64)
    if ref.shape != (len(x),) or np.any(ref[1:] <= 0):
        raise ValueError("RMA reference mismatch")
    return float(np.mean(np.diag(x)[1:] / ref[1:]))


def efwt(matrix, random_scores, scenario: str = "domain") -> float:
    if scenario != "domain":
        raise ValueError("E-FWT is defined only for Domain-CL")
    x = _square(matrix)
    random = np.asarray(random_scores, dtype=np.float64)
    if random.shape != (len(x),):
        raise ValueError("random baseline mismatch")
    values = [x[t, i] - random[i] for t in range(len(x) - 1) for i in range(t + 1, len(x))]
    return float(np.mean(values))


def matrix_summary(matrix, independent_scores, scenario: str, random_scores=None) -> dict[str, float]:
    x = _square(matrix)
    out = {
        "A-Dice": adice(x),
        "BWTR": bwtr(x),
        "RMA": rma(x, independent_scores),
        "mean_current": float(np.mean(np.diag(x))),
        "final_old_mean": float(np.mean(x[-1, :-1])),
    }
    if scenario == "domain":
        if random_scores is None:
            raise ValueError("Domain E-FWT requires random scores")
        out["E-FWT"] = efwt(x, random_scores, scenario)
    elif scenario != "organ":
        raise ValueError(scenario)
    return out

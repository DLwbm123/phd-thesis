import numpy as np

def dice(pred, target, cls):
    p, t = pred == cls, target == cls
    denom = p.sum() + t.sum()
    return 1.0 if denom == 0 else float(2 * (p & t).sum() / denom)

def benchmark_patient_dice(pred, target, patient_info, classes, eps=1e-5):
    """Exact MMWHS aggregation: per-patient volumes, BG included, then mean."""
    starts = [0] + [int(x) + 1 for x in patient_info[:-1]]
    ends = [int(x) + 1 for x in patient_info]
    per_patient = []
    per_class = {c: [] for c in classes}
    for start, end in zip(starts, ends):
        pv, tv = pred[start:end], target[start:end]
        row = []
        for c in classes:
            p, t = pv == c, tv == c
            score = float((2 * np.logical_and(p, t).sum() + eps) /
                          (p.sum() + t.sum() + eps))
            row.append(score); per_class[c].append(score)
        per_patient.append(row)
    return float(np.mean(per_patient)), {c: float(np.mean(v)) for c, v in per_class.items()}

def matrix_summary(matrix, independent):
    n = len(matrix); diag = np.diag(matrix)
    return {
        "A-Dice": float(np.mean(matrix[-1])),
        "BWTR": float(np.mean([(matrix[-1,i]-diag[i])/diag[i] for i in range(n-1)])) if n > 1 else 0.0,
        "RMA": float(np.mean([diag[i]/independent[i] for i in range(1,n)])) if n > 1 else 1.0,
        "mean_current_task_dice": float(np.mean(diag)),
    }

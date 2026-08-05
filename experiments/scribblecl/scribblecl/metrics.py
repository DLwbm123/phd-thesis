import numpy as np

def dice(pred, target, cls):
    p, t = pred == cls, target == cls
    denom = p.sum() + t.sum()
    return 1.0 if denom == 0 else float(2 * (p & t).sum() / denom)

def matrix_summary(matrix, independent):
    n = len(matrix); diag = np.diag(matrix)
    return {
        "A-Dice": float(np.mean(matrix[-1])),
        "BWTR": float(np.mean([(matrix[-1,i]-diag[i])/diag[i] for i in range(n-1)])) if n > 1 else 0.0,
        "RMA": float(np.mean([diag[i]/independent[i] for i in range(1,n)])) if n > 1 else 1.0,
        "mean_current_task_dice": float(np.mean(diag)),
    }

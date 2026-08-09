"""Domain trainer API alias; implementation lives in the shared engine."""
from .engine import train_stage, evaluate_matrix_row

__all__ = ["train_stage", "evaluate_matrix_row"]

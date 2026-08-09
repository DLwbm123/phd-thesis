"""Organ trainer API alias; old-head freezing is enforced by OrganSegmenter."""
from .engine import train_stage, evaluate_matrix_row

__all__ = ["train_stage", "evaluate_matrix_row"]

from __future__ import annotations

from copy import deepcopy

import torch
from torch import nn


class BinaryHead(nn.Module):
    def __init__(self, in_channels: int, batchnorm: bool, out_channels: int = 2):
        super().__init__()
        # ZS original uses Conv bias + BN; Benchmark ResUNet uses bias=False.
        self.conv = nn.Conv2d(in_channels, out_channels, 1, bias=batchnorm)
        self.norm = nn.BatchNorm2d(out_channels, eps=1e-3, momentum=0.01) if batchnorm else nn.Identity()

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.norm(self.conv(features))


class SingleHeadSegmenter(nn.Module):
    """Shared backbone with one semantic head (binary or parity-only 4ch)."""

    def __init__(self, backbone: nn.Module, out_channels: int = 2):
        super().__init__()
        self.backbone = backbone
        self.head = BinaryHead(backbone.out_channels, backbone.head_batchnorm, out_channels)

    def forward(self, x: torch.Tensor, task_id: int | None = None) -> torch.Tensor:
        return self.head(self.backbone(x))

    def fisher_named_parameters(self):
        return self.named_parameters()


class DomainSegmenter(SingleHeadSegmenter):
    """Shared backbone and shared BG/prostate binary head."""

    scenario = "domain"

    def __init__(self, backbone: nn.Module):
        super().__init__(backbone, out_channels=2)


class OrganSegmenter(nn.Module):
    """Shared backbone with known-task binary heads."""

    scenario = "organ"

    def __init__(self, backbone: nn.Module, n_tasks: int = 4):
        super().__init__()
        self.backbone = backbone
        self.heads = nn.ModuleDict({"0": BinaryHead(backbone.out_channels, backbone.head_batchnorm)})
        self.n_tasks = n_tasks

    def add_head(self, task_id: int) -> None:
        task_id = int(task_id)
        if not 0 <= task_id < self.n_tasks:
            raise ValueError(task_id)
        key = str(task_id)
        if key not in self.heads:
            reference = next(self.backbone.parameters())
            self.heads[key] = BinaryHead(self.backbone.out_channels, self.backbone.head_batchnorm).to(
                device=reference.device, dtype=reference.dtype
            )

    def forward(self, x: torch.Tensor, task_id: int) -> torch.Tensor:
        return self.heads[str(int(task_id))](self.backbone(x))

    def freeze_completed_head(self, task_id: int) -> None:
        head = self.heads[str(int(task_id))]
        head.eval()
        for parameter in head.parameters():
            parameter.requires_grad_(False)

    def activate_head(self, task_id: int) -> None:
        self.add_head(task_id)
        head = self.heads[str(int(task_id))]
        for parameter in head.parameters():
            parameter.requires_grad_(True)

    def fisher_named_parameters(self):
        # Organ EWC/SI constrain only the shared backbone.
        return ((f"backbone.{name}", value) for name, value in self.backbone.named_parameters())

    def head_parameter_counts(self) -> dict[int, int]:
        return {int(i): sum(p.numel() for p in head.parameters()) for i, head in self.heads.items()}


def copy_single_head_from_organ(model: OrganSegmenter, task_id: int) -> DomainSegmenter:
    """Test helper proving a selected multi-head path equals single-head use."""
    single = DomainSegmenter(deepcopy(model.backbone))
    single.head.load_state_dict(model.heads[str(task_id)].state_dict())
    return single

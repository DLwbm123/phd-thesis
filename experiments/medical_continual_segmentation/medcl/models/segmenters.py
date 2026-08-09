from __future__ import annotations

import torch
from torch import nn

from .unet import UNetBackbone


class OutputHead(nn.Module):
    def __init__(self, channels: int):
        super().__init__(); self.conv = nn.Conv2d(64, channels, 1, bias=True); self.norm = nn.BatchNorm2d(channels, eps=1e-3, momentum=0.01)
    def forward(self, features): return self.norm(self.conv(features))


class DomainSegmenter(nn.Module):
    scenario = "domain"
    def __init__(self): super().__init__(); self.backbone = UNetBackbone(); self.head = OutputHead(2)
    def forward(self, x, task_id=None): return self.head(self.backbone(x))
    def importance_named_parameters(self): return self.named_parameters()


class OrganSegmenter(nn.Module):
    scenario = "organ"
    def __init__(self): super().__init__(); self.backbone = UNetBackbone(); self.heads = nn.ModuleDict({"0": OutputHead(2)}); self.active_stage = 0
    def activate_stage(self, stage):
        key = str(int(stage)); self.active_stage = int(stage)
        if key not in self.heads:
            ref = next(self.backbone.parameters()); self.heads[key] = OutputHead(2).to(ref.device)
    def freeze_stage(self, stage):
        for p in self.heads[str(stage)].parameters(): p.requires_grad_(False)
        self.heads[str(stage)].eval()
    def forward(self, x, task_id=None): return self.heads[str(self.active_stage if task_id is None else int(task_id))](self.backbone(x))
    def importance_named_parameters(self): return ((f"backbone.{n}", p) for n, p in self.backbone.named_parameters())


class ClassSegmenter(nn.Module):
    scenario = "class"
    block_sizes = (3, 2, 2)
    def __init__(self):
        super().__init__(); self.backbone = UNetBackbone(); self.background = OutputHead(1); self.blocks = nn.ModuleList(OutputHead(n) for n in self.block_sizes); self.active_stage = 0; self.block_calls = [0, 0, 0]
    def activate_stage(self, stage): self.active_stage = int(stage)
    def load_stage1_static_state(self, state):
        """Load a four-channel static U-Net state without changing channel order."""
        backbone = {name: value for name, value in state.items() if not (name.startswith("Conv.") or name.startswith("Norm."))}
        self.backbone.load_state_dict(backbone)
        with torch.no_grad():
            self.background.conv.weight.copy_(state["Conv.weight"][0:1]); self.background.conv.bias.copy_(state["Conv.bias"][0:1])
            self.blocks[0].conv.weight.copy_(state["Conv.weight"][1:4]); self.blocks[0].conv.bias.copy_(state["Conv.bias"][1:4])
            for target, source, part in ((self.background.norm, "Norm", slice(0, 1)), (self.blocks[0].norm, "Norm", slice(1, 4))):
                target.weight.copy_(state[f"{source}.weight"][part]); target.bias.copy_(state[f"{source}.bias"][part]); target.running_mean.copy_(state[f"{source}.running_mean"][part]); target.running_var.copy_(state[f"{source}.running_var"][part]); target.num_batches_tracked.copy_(state[f"{source}.num_batches_tracked"])
    def forward(self, x, task_id=None):
        stage = self.active_stage if task_id is None else int(task_id); features = self.backbone(x); parts = [self.background(features)]
        for index in range(stage + 1): self.block_calls[index] += 1; parts.append(self.blocks[index](features))
        return torch.cat(parts, dim=1)
    def importance_named_parameters(self):
        for name, value in self.backbone.named_parameters(): yield f"backbone.{name}", value
        for name, value in self.background.named_parameters(): yield f"background.{name}", value
        for index in range(self.active_stage + 1):
            for name, value in self.blocks[index].named_parameters(): yield f"blocks.{index}.{name}", value


def build_model(scenario: str):
    return {"class": ClassSegmenter, "domain": DomainSegmenter, "organ": OrganSegmenter}[scenario]()

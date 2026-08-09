from __future__ import annotations

import torch
from torch import nn
import torch.nn.functional as F


class ConvBlock(nn.Module):
    def __init__(self, inputs: int, outputs: int):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(inputs, outputs, 3, bias=True), nn.ReLU(inplace=True), nn.BatchNorm2d(outputs),
            nn.Conv2d(outputs, outputs, 3, bias=True), nn.ReLU(inplace=True), nn.BatchNorm2d(outputs, eps=1e-3, momentum=0.01),
        )
    def forward(self, x): return self.conv(x)


class UpBlock(nn.Module):
    def __init__(self, inputs: int, outputs: int):
        super().__init__()
        self.up = nn.Sequential(nn.Upsample(scale_factor=2), nn.Conv2d(inputs, outputs, 3, padding=1, bias=True), nn.ReLU(inplace=True), nn.BatchNorm2d(outputs, eps=1e-3, momentum=0.01))
    def forward(self, x): return self.up(x)


def center_crop(source: torch.Tensor, shape: tuple[int, int]) -> torch.Tensor:
    dh, dw = source.shape[-2] - shape[0], source.shape[-1] - shape[1]
    top, left = dh // 2, dw // 2
    return source[..., top:top+shape[0], left:left+shape[1]]


class UNetBackbone(nn.Module):
    """Dynamic valid-convolution U-Net returning the final 64-channel feature map."""
    out_channels = 64

    def __init__(self):
        super().__init__(); f = [64, 128, 256, 512, 1024]
        self.Pad = nn.ConstantPad2d((92, 92, 92, 92), 0)
        self.Maxpool1 = nn.MaxPool2d(2); self.Maxpool2 = nn.MaxPool2d(2); self.Maxpool3 = nn.MaxPool2d(2); self.Maxpool4 = nn.MaxPool2d(2)
        self.Conv1 = ConvBlock(1, f[0]); self.Conv2 = ConvBlock(f[0], f[1]); self.Conv3 = ConvBlock(f[1], f[2]); self.Conv4 = ConvBlock(f[2], f[3]); self.Conv5 = ConvBlock(f[3], f[4])
        self.Up4 = UpBlock(f[4], 4); self.Up_conv4 = ConvBlock(516, f[3])
        self.Up3 = UpBlock(f[3], 4); self.Up_conv3 = ConvBlock(260, f[2])
        self.Up2 = UpBlock(f[2], f[1]); self.Up_conv2 = ConvBlock(f[2], f[1])
        self.Up1 = UpBlock(f[1], f[0]); self.Up_conv1 = ConvBlock(f[1], f[0])

    def forward(self, x):
        original = x.shape[-2:]
        ah, aw = (4 - x.shape[-2] % 16) % 16, (4 - x.shape[-1] % 16) % 16
        if ah or aw: x = F.pad(x, (aw//2, aw-aw//2, ah//2, ah-ah//2))
        e1 = self.Conv1(self.Pad(x)); e2 = self.Conv2(self.Maxpool1(e1)); e3 = self.Conv3(self.Maxpool2(e2)); e4 = self.Conv4(self.Maxpool3(e3)); e5 = self.Conv5(self.Maxpool4(e4))
        u4 = self.Up4(e5); d4 = self.Up_conv4(torch.cat((u4, center_crop(e4, u4.shape[-2:])), 1))
        u3 = self.Up3(d4); d3 = self.Up_conv3(torch.cat((u3, center_crop(e3, u3.shape[-2:])), 1))
        u2 = self.Up2(d3); d2 = self.Up_conv2(torch.cat((u2, center_crop(e2, u2.shape[-2:])), 1))
        u1 = self.Up1(d2); d1 = self.Up_conv1(torch.cat((u1, center_crop(e1, u1.shape[-2:])), 1))
        return center_crop(d1, original)

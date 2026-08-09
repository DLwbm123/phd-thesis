"""Backbones audited against Benchmark ResUNet32 and ZScribbleSeg U-Net."""
from __future__ import annotations

import torch
from torch import nn
import torch.nn.functional as F


class ResidualConv(nn.Module):
    def __init__(self, input_dim: int, output_dim: int, stride: int, padding: int):
        super().__init__()
        self.bn1 = nn.BatchNorm2d(input_dim)
        self.conv1 = nn.Conv2d(input_dim, output_dim, 3, stride=stride, padding=padding, bias=False)
        self.bn2 = nn.BatchNorm2d(output_dim)
        self.conv2 = nn.Conv2d(output_dim, output_dim, 3, padding=1, bias=False)
        self.conv_skip = nn.Conv2d(input_dim, output_dim, 3, stride=stride, padding=1, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        shortcut = self.conv_skip(x)
        out = self.conv1(F.relu(self.bn1(x)))
        out = self.conv2(F.relu(self.bn2(out)))
        return out + shortcut


class ResUNet32Backbone(nn.Module):
    """Feature-producing form of Benchmark ``resunet32('mid')``."""

    out_channels = 32
    head_batchnorm = False

    def __init__(self):
        super().__init__()
        f = [32, 64, 128, 256]
        self.conv1 = nn.Conv2d(1, f[0], 3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(f[0])
        self.conv2 = nn.Conv2d(f[0], f[0], 3, padding=1, bias=False)
        self.residual_conv_1 = ResidualConv(f[0], f[1], 2, 1)
        self.residual_conv_2 = ResidualConv(f[1], f[2], 2, 1)
        self.bridge = ResidualConv(f[2], f[3], 2, 1)
        self.up_residual_conv1 = ResidualConv(f[3] + f[2], f[2], 1, 1)
        self.up_residual_conv2 = ResidualConv(f[2] + f[1], f[1], 1, 1)
        self.up_residual_conv3 = ResidualConv(f[1] + f[0], f[0], 1, 1)

    @staticmethod
    def _up(x: torch.Tensor) -> torch.Tensor:
        return F.interpolate(x, scale_factor=2, mode="bilinear", align_corners=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x1 = self.conv2(F.relu(self.bn1(self.conv1(x))))
        x2 = self.residual_conv_1(x1)
        x3 = self.residual_conv_2(x2)
        x4 = self.bridge(x3)
        x6 = self.up_residual_conv1(torch.cat([self._up(x4), x3], dim=1))
        x8 = self.up_residual_conv2(torch.cat([self._up(x6), x2], dim=1))
        return self.up_residual_conv3(torch.cat([self._up(x8), x1], dim=1))


class ConvBlock(nn.Module):
    def __init__(self, in_ch: int, out_ch: int):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, 1, 0, bias=True),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(out_ch),
            nn.Conv2d(out_ch, out_ch, 3, 1, 0, bias=True),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(out_ch, eps=1e-3, momentum=0.01),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.conv(x)


class UpConv(nn.Module):
    def __init__(self, in_ch: int, out_ch: int):
        super().__init__()
        self.up = nn.Sequential(
            nn.Upsample(scale_factor=2),
            nn.Conv2d(in_ch, out_ch, 3, 1, 1, bias=True),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(out_ch, eps=1e-3, momentum=0.01),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.up(x)


def center_crop(source: torch.Tensor, spatial_shape: tuple[int, int]) -> torch.Tensor:
    dh, dw = source.shape[-2] - spatial_shape[0], source.shape[-1] - spatial_shape[1]
    if dh < 0 or dw < 0:
        raise ValueError("source is smaller than requested crop")
    top, left = dh // 2, dw // 2
    return source[..., top : top + spatial_shape[0], left : left + spatial_shape[1]]


class ZSUNetBackbone(nn.Module):
    """Original valid-convolution U-Net returning the 64-channel decoder map."""

    out_channels = 64
    head_batchnorm = True

    def __init__(self):
        super().__init__()
        f = [64, 128, 256, 512, 1024]
        self.Pad = nn.ConstantPad2d((92, 92, 92, 92), 0)
        self.Maxpool1 = nn.MaxPool2d(2, 2)
        self.Maxpool2 = nn.MaxPool2d(2, 2)
        self.Maxpool3 = nn.MaxPool2d(2, 2)
        self.Maxpool4 = nn.MaxPool2d(2, 2)
        self.Conv1 = ConvBlock(1, f[0])
        self.Conv2 = ConvBlock(f[0], f[1])
        self.Conv3 = ConvBlock(f[1], f[2])
        self.Conv4 = ConvBlock(f[2], f[3])
        self.Conv5 = ConvBlock(f[3], f[4])
        self.Up4 = UpConv(f[4], 4)
        self.Up_conv4 = ConvBlock(516, f[3])
        self.Up3 = UpConv(f[3], 4)
        self.Up_conv3 = ConvBlock(260, f[2])
        self.Up2 = UpConv(f[2], f[1])
        self.Up_conv2 = ConvBlock(f[2], f[1])
        self.Up1 = UpConv(f[1], f[0])
        self.Up_conv1 = ConvBlock(f[1], f[0])

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        original = x.shape[-2:]
        add_h, add_w = (4 - x.shape[-2] % 16) % 16, (4 - x.shape[-1] % 16) % 16
        if add_h or add_w:
            x = F.pad(x, (add_w // 2, add_w - add_w // 2, add_h // 2, add_h - add_h // 2))
        e1 = self.Conv1(self.Pad(x))
        e2 = self.Conv2(self.Maxpool1(e1))
        e3 = self.Conv3(self.Maxpool2(e2))
        e4 = self.Conv4(self.Maxpool3(e3))
        e5 = self.Conv5(self.Maxpool4(e4))
        d4 = self.Up4(e5)
        d4 = self.Up_conv4(torch.cat((d4, center_crop(e4, d4.shape[-2:])), 1))
        d3 = self.Up3(d4)
        d3 = self.Up_conv3(torch.cat((d3, center_crop(e3, d3.shape[-2:])), 1))
        d2 = self.Up2(d3)
        d2 = self.Up_conv2(torch.cat((d2, center_crop(e2, d2.shape[-2:])), 1))
        d1 = self.Up1(d2)
        d1 = self.Up_conv1(torch.cat((d1, center_crop(e1, d1.shape[-2:])), 1))
        return center_crop(d1, original)


def build_backbone(name: str) -> nn.Module:
    if name == "resunet32":
        return ResUNet32Backbone()
    if name == "zs_unet":
        return ZSUNetBackbone()
    raise ValueError(name)

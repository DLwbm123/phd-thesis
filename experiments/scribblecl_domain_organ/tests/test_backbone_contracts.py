from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sys

import pytest
import torch

from scribblecl_do.models import DomainSegmenter, SingleHeadSegmenter, ResUNet32Backbone, ZSUNetBackbone


def _load_module(name, path):
    spec=importlib.util.spec_from_file_location(name,path); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module


@pytest.mark.skipif("BENCHMARK_ROOT" not in os.environ, reason="remote Benchmark source not configured")
def test_resunet32_feature_parity_with_benchmark():
    root=Path(os.environ["BENCHMARK_ROOT"]); sys.path.insert(0,str(root)); benchmark=_load_module("benchmark_resunet",root/"backbone/ResUnet.py").resunet32("mid").eval(); adapted=ResUNet32Backbone().eval(); adapted.load_state_dict({k:v for k,v in benchmark.state_dict().items() if not k.startswith("last.")}); x=torch.randn(1,1,32,32)
    with torch.no_grad(): assert torch.equal(benchmark.features(x),adapted(x))


@pytest.mark.skipif("ZS_ORIGINAL_ROOT" not in os.environ or not torch.cuda.is_available(), reason="original ZS CUDA source not configured")
def test_zs_unet_212_four_channel_parity():
    root=Path(os.environ["ZS_ORIGINAL_ROOT"]); sys.path.insert(0,str(root)); original=_load_module("original_zs_unet",root/"models/UNet.py").Unet(1,4).cuda().eval(); adapted=SingleHeadSegmenter(ZSUNetBackbone(),4).cuda().eval(); state=original.state_dict(); adapted.backbone.load_state_dict({k:v for k,v in state.items() if not (k.startswith("Conv.") or k.startswith("Norm."))}); adapted.head.conv.load_state_dict({k.removeprefix("Conv."):v for k,v in state.items() if k.startswith("Conv.")}); adapted.head.norm.load_state_dict({k.removeprefix("Norm."):v for k,v in state.items() if k.startswith("Norm.")}); x=torch.randn(1,1,212,212,device="cuda")
    with torch.no_grad(): delta=(torch.softmax(adapted(x),1)-original(x)).abs().max()
    assert float(delta)<=1e-6


@pytest.mark.skipif(not torch.cuda.is_available(), reason="large U-Net shape contract uses CUDA")
def test_zs_unet_256_output_same_size():
    model=DomainSegmenter(ZSUNetBackbone()).cuda().eval()
    with torch.no_grad(): out=model(torch.randn(1,1,256,256,device="cuda"))
    assert out.shape==(1,2,256,256)

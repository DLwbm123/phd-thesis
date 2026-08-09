from __future__ import annotations
import importlib.util
import os
from pathlib import Path
import sys

import pytest
import torch
from torch import nn

from medcl.models import ClassSegmenter, DomainSegmenter, OrganSegmenter, OutputHead, UNetBackbone, build_model
from medcl.supervision.losses import dense_loss


class _Features(nn.Module):
    def forward(self,x): return x.repeat(1,64,1,1)


def _static_state(backbone,head):
    value={name:tensor.clone() for name,tensor in backbone.state_dict().items()}
    for name,tensor in head.conv.state_dict().items(): value[f"Conv.{name}"]=tensor.clone()
    for name,tensor in head.norm.state_dict().items(): value[f"Norm.{name}"]=tensor.clone()
    return value


@pytest.mark.skipif(not torch.cuda.is_available(),reason="full U-Net contracts require CUDA")
def test_unet_256_output_shape():
    model=DomainSegmenter().cuda().eval()
    with torch.no_grad(): result=model(torch.randn(1,1,256,256,device="cuda"))
    assert result.shape==(1,2,256,256)


@pytest.mark.skipif("UNET_REFERENCE_ROOT" not in os.environ or not torch.cuda.is_available(),reason="reference source and CUDA are required")
def test_unet_212_original_parity():
    root=Path(os.environ["UNET_REFERENCE_ROOT"]); sys.path.insert(0,str(root)); spec=importlib.util.spec_from_file_location("reference_unet",root/"models/UNet.py"); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    torch.manual_seed(7); reference=module.Unet(1,4).cuda().eval(); backbone=UNetBackbone().cuda().eval(); head=OutputHead(4).cuda().eval(); state=reference.state_dict(); backbone.load_state_dict({k:v for k,v in state.items() if not(k.startswith("Conv.") or k.startswith("Norm."))}); head.conv.load_state_dict({k.removeprefix("Conv."):v for k,v in state.items() if k.startswith("Conv.")}); head.norm.load_state_dict({k.removeprefix("Norm."):v for k,v in state.items() if k.startswith("Norm.")}); x=torch.randn(1,1,212,212,device="cuda")
    with torch.no_grad(): delta=(torch.softmax(head(backbone(x)),1)-reference(x)).abs().max()
    assert float(delta)<=1e-6


@pytest.mark.skipif(not torch.cuda.is_available(),reason="full U-Net contracts require CUDA")
def test_class_stage1_four_channel_parity():
    torch.manual_seed(9); backbone=UNetBackbone().cuda(); head=OutputHead(4).cuda(); model=ClassSegmenter().cuda(); model.load_stage1_static_state(_static_state(backbone,head)); backbone.eval(); head.eval(); model.eval(); x=torch.randn(1,1,32,32,device="cuda")
    with torch.no_grad(): assert float((model(x)-head(backbone(x))).abs().max())<=1e-6


def test_cross_entropy_receives_logits(monkeypatch):
    logits=torch.randn(2,3,4,4,requires_grad=True); target=torch.zeros(2,4,4,dtype=torch.long); seen={}
    def fake(value,labels,**kwargs): seen["same"]=value is logits; return value.sum()*0
    monkeypatch.setattr(torch.nn.functional,"cross_entropy",fake); dense_loss(logits,target); assert seen["same"]


def test_all_methods_share_same_backbone_type():
    assert {type(build_model(s).backbone) for s in ("class","domain","organ")}=={UNetBackbone}


def test_no_resunet_final_config():
    root=Path(__file__).resolve().parents[1]
    assert all("resunet" not in path.read_text().lower() for path in [*root.glob("configs/**/*.yaml"),*root.glob("medcl/models/*.py")])


def test_class_future_blocks_not_called():
    model=ClassSegmenter(); model.backbone=_Features(); model.activate_stage(0); model(torch.randn(1,1,4,4)); assert model.block_calls==[1,0,0]


def test_class_future_blocks_no_gradient():
    model=ClassSegmenter(); model.backbone=_Features(); model.activate_stage(0); model(torch.randn(1,1,4,4)).sum().backward(); assert all(p.grad is None for block in model.blocks[1:] for p in block.parameters())


def test_class_final_eight_channel_order():
    model=ClassSegmenter(); model.backbone=_Features(); model.activate_stage(2); model.eval()
    for index,head in enumerate([model.background,*model.blocks]):
        nn.init.zeros_(head.conv.weight); nn.init.constant_(head.conv.bias,float(index)); head.norm.weight.data.fill_(1); head.norm.bias.data.zero_(); head.norm.running_mean.zero_(); head.norm.running_var.fill_(1)
    result=model(torch.ones(1,1,2,2)); assert result.shape[1]==8; means=result.mean((0,2,3)); assert torch.all(means[1:4]==means[1]); assert torch.all(means[4:6]==means[4]); assert torch.all(means[6:8]==means[6]); assert means[0]<means[1]<means[4]<means[6]


def test_organ_old_heads_are_frozen():
    model=OrganSegmenter(); model.activate_stage(1); model.freeze_stage(0); assert all(not p.requires_grad for p in model.heads["0"].parameters()); assert all(p.requires_grad for p in model.heads["1"].parameters())

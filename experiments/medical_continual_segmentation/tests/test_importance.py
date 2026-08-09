import pytest
import torch
from torch.utils.data import DataLoader, Dataset

from medcl.methods import OnlineEWC, SynapticIntelligence, estimate_fisher
from medcl.models import ClassSegmenter, DomainSegmenter, OrganSegmenter


class SparsePixels(Dataset):
    exposes_dense=False
    def __len__(self): return 1
    def __getitem__(self,index):
        labels=torch.full((32,32),-100,dtype=torch.long); labels[2:5,2:20]=0; labels[14:17,10:18]=1
        return torch.randn(1,32,32),labels


class DensePixels(SparsePixels): exposes_dense=True


@pytest.mark.skipif(not torch.cuda.is_available(),reason="full U-Net Fisher requires CUDA")
def test_unet_fisher_nonnegative():
    model=DomainSegmenter().cuda(); fisher,summary=estimate_fisher(model,DataLoader(SparsePixels()),"cuda",max_batches=1); assert summary.minimum>=0; assert all(bool((value>=0).all()) for value in fisher.values())


def test_unet_fisher_sparse_pce_only():
    with pytest.raises(ValueError,match="sparse-only"): estimate_fisher(DomainSegmenter(),DataLoader(DensePixels()),"cpu",max_batches=1)


def test_class_new_block_not_in_old_penalty():
    model=ClassSegmenter(); model.activate_stage(0); method=OnlineEWC(); current={name:torch.ones_like(p) for name,p in model.importance_named_parameters()}; method.consolidate(model,current); model.activate_stage(1)
    with torch.no_grad(): next(model.blocks[1].parameters()).add_(1)
    assert float(method.penalty(model))==0


def test_domain_head_in_ewc_scope():
    assert any(name.startswith("head.") for name,_ in DomainSegmenter().importance_named_parameters())


def test_organ_heads_outside_ewc_scope():
    assert all(name.startswith("backbone.") for name,_ in OrganSegmenter().importance_named_parameters())


@pytest.mark.parametrize("scenario,expected",[("class",("backbone.","background.","blocks.0.")),("domain",("backbone.","head.")),("organ",("backbone.",))])
def test_si_scope_matches_scenario(scenario,expected):
    model={"class":ClassSegmenter,"domain":DomainSegmenter,"organ":OrganSegmenter}[scenario](); method=SynapticIntelligence(); method.begin(model); assert all(any(name.startswith(prefix) for prefix in expected) for name in method.small)

from __future__ import annotations

import torch
from torch.utils.data import DataLoader

from scribblecl_do.data.h5_dataset import WeakH5Dataset
from scribblecl_do.methods.ewc import OnlineEWC, estimate_sparse_fisher
from scribblecl_do.models import DomainSegmenter, OrganSegmenter, ResUNet32Backbone


def _ones(model):
    return {n: torch.ones_like(p) for n,p in model.fisher_named_parameters() if p.requires_grad}


def test_ewc_zero_on_saved_parameters():
    model=DomainSegmenter(ResUNet32Backbone()); ewc=OnlineEWC(); ewc.consolidate(model,_ones(model))
    assert float(ewc.penalty(model)) == 0


def test_ewc_positive_after_parameter_change():
    model=DomainSegmenter(ResUNet32Backbone()); ewc=OnlineEWC(); ewc.consolidate(model,_ones(model)); next(model.parameters()).data.add_(1)
    assert float(ewc.penalty(model)) > 0


def test_fisher_nonnegative(binary_h5, sparse_npz):
    model=DomainSegmenter(ResUNet32Backbone()); weak=WeakH5Dataset(binary_h5,sparse_npz); fisher,_=estimate_sparse_fisher(model,DataLoader(weak,batch_size=2),"cpu",max_batches=1)
    assert all(bool((x>=0).all()) for x in fisher.values())


def test_fisher_uses_sparse_pce_only(binary_h5, sparse_npz):
    weak=WeakH5Dataset(binary_h5,sparse_npz); assert weak.exposes_dense is False
    fisher,summary=estimate_sparse_fisher(DomainSegmenter(ResUNet32Backbone()),DataLoader(weak,batch_size=2),"cpu",max_batches=1)
    assert summary.known_pixels == 16


def test_fisher_never_reads_dense_mask(binary_h5, sparse_npz):
    class Forbidden(WeakH5Dataset):
        @property
        def dense(self): raise AssertionError("dense read")
    dataset=Forbidden(binary_h5,sparse_npz)
    estimate_sparse_fisher(DomainSegmenter(ResUNet32Backbone()),DataLoader(dataset,batch_size=2),"cpu",max_batches=1)


def test_domain_ewc_includes_shared_head():
    names={n for n,_ in DomainSegmenter(ResUNet32Backbone()).fisher_named_parameters()}
    assert any(n.startswith("head.") for n in names)


def test_organ_ewc_backbone_only():
    names={n for n,_ in OrganSegmenter(ResUNet32Backbone()).fisher_named_parameters()}
    assert names and all(n.startswith("backbone.") for n in names)


def test_old_organ_heads_not_penalized():
    model=OrganSegmenter(ResUNet32Backbone()); ewc=OnlineEWC(); ewc.consolidate(model,_ones(model)); model.heads["0"].conv.weight.data.add_(2)
    assert float(ewc.penalty(model)) == 0


def test_online_consolidation_matches_benchmark():
    model=DomainSegmenter(ResUNet32Backbone()); ewc=OnlineEWC(gamma=.1); one=_ones(model); ewc.consolidate(model,one); two={n:2*x for n,x in one.items()}; ewc.consolidate(model,two)
    assert all(torch.allclose(v,torch.full_like(v,2.1)) for v in ewc.fisher.values())

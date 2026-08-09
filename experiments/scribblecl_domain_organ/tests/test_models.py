from __future__ import annotations

from copy import deepcopy

import torch

from scribblecl_do.models import DomainSegmenter, OrganSegmenter, ResUNet32Backbone
from scribblecl_do.models.task_heads import copy_single_head_from_organ


def test_domain_shared_head():
    model = DomainSegmenter(ResUNet32Backbone())
    assert hasattr(model, "head") and not hasattr(model, "heads")


def test_organ_task_specific_heads():
    model = OrganSegmenter(ResUNet32Backbone())
    for task_id in (1, 2, 3): model.add_head(task_id)
    assert len(model.heads) == 4 and len({id(x) for x in model.heads.values()}) == 4


def test_domain_binary_head_shape():
    model = DomainSegmenter(ResUNet32Backbone()).eval()
    assert model(torch.randn(2, 1, 32, 32)).shape == (2, 2, 32, 32)


def test_organ_multihead_shape():
    model = OrganSegmenter(ResUNet32Backbone()).eval()
    model.add_head(3)
    assert model(torch.randn(2, 1, 32, 32), 3).shape == (2, 2, 32, 32)


def test_singlehead_multihead_equivalence():
    multi = OrganSegmenter(ResUNet32Backbone()).eval()
    multi.add_head(2)
    single = copy_single_head_from_organ(multi, 2).eval()
    x = torch.randn(1, 1, 32, 32)
    with torch.no_grad():
        assert torch.equal(multi(x, 2), single(x))


def test_inactive_head_no_gradient():
    model = OrganSegmenter(ResUNet32Backbone())
    model.add_head(1)
    model(torch.randn(1, 1, 32, 32), 1).sum().backward()
    assert all(p.grad is None for p in model.heads["0"].parameters())
    assert all(p.grad is not None for p in model.heads["1"].parameters())


def test_old_heads_frozen():
    model = OrganSegmenter(ResUNet32Backbone()); model.freeze_completed_head(0)
    assert all(not p.requires_grad for p in model.heads["0"].parameters())


def test_old_organ_heads_not_penalized_or_updated():
    model = OrganSegmenter(ResUNet32Backbone()); model.add_head(1); model.freeze_completed_head(0)
    before={k:v.clone() for k,v in model.heads["0"].state_dict().items()}
    opt=torch.optim.SGD((p for p in model.parameters() if p.requires_grad),lr=.01); loss=model(torch.randn(1,1,32,32),1).sum(); loss.backward(); opt.step()
    assert all(torch.equal(before[k],v) for k,v in model.heads["0"].state_dict().items())

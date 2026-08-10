from __future__ import annotations
import random
import numpy as np
import torch

from medcl.data.sparse import generate
from medcl.metrics.matrix import matrix_summary
from medcl.utils import CheckpointController, file_sha256


def test_v2_s2_label_contract_and_determinism():
    labels=np.zeros((2,64,64),dtype=np.int16); labels[0,20:44,20:44]=1; labels[1,15:50,28:36]=2
    a,stats=generate(labels,3,42); b,_=generate(labels,3,42); assert np.array_equal(a,b); assert set(np.unique(a))<={-100,0,4,5}; assert stats.foreground_pixels>0 and stats.background_pixels>0 and stats.unknown_pixels>0


def test_area_scaled_annotations_expand_without_label_leakage():
    labels=np.zeros((2,48,48),dtype=np.int16); labels[:,10:38,10:38]=1
    base,_=generate(labels,0,42); scaled,_=generate(labels,0,42,foreground_area_multiplier=8,background_area_multiplier=10)
    assert (scaled==1).sum() >= (base==1).sum()
    assert (scaled==0).sum() >= (base==0).sum()
    assert not np.any((scaled==1) & (labels!=1))


def test_matrix_metrics_and_domain_only_efwt():
    matrix=np.array([[.8,.3],[.7,.75]]); domain=matrix_summary(matrix,"domain",[.82,.78],[.2,.2]); organ=matrix_summary(matrix,"organ",[.82,.78]); assert set(("A-Dice","BWTR","RMA","E-FWT"))<=set(domain); assert "E-FWT" not in organ


def test_checkpoint_contains_resume_state(tmp_path):
    model=torch.nn.Linear(2,2); optimizer=torch.optim.SGD(model.parameters(),lr=.1,momentum=.9); scheduler=torch.optim.lr_scheduler.StepLR(optimizer,1); controller=CheckpointController(tmp_path); original={name:value.detach().clone() for name,value in model.state_dict().items()}; path=controller.save(model,optimizer,scheduler,1,7,[],matrix=np.eye(2)); value=torch.load(path,weights_only=False); assert {"optimizer","scheduler","python_rng","numpy_rng","torch_rng","matrix"}<=set(value)
    with torch.no_grad(): next(model.parameters()).add_(10)
    restored=CheckpointController.load(path,model,optimizer,scheduler); assert restored["stage"]==1 and restored["epoch"]==7; assert all(torch.equal(model.state_dict()[name],tensor) for name,tensor in original.items()); assert file_sha256(path)==file_sha256(path)

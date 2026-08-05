import torch
from scribblecl.losses import partial_cross_entropy, scribble_mib_loss
from scribblecl.protocol import IGNORE_INDEX, old_classes, future_classes, stage

def test_stage_sets_are_disjoint_and_complete():
    assert stage(2).active == (4,5) and old_classes(2)==(1,2,3) and future_classes(2)==(6,7)
    assert stage(3).active == (6,7) and old_classes(3)==(1,2,3,4,5)

def test_ignore_pixels_have_no_supervision_gradient():
    logits=torch.randn(1,8,2,2,requires_grad=True); labels=torch.full((1,2,2),IGNORE_INDEX); labels[0,0,0]=1
    partial_cross_entropy(logits,labels,(0,1,2,3)).backward()
    assert logits.grad[0,:,1,1].abs().sum()==0

def test_teacher_excludes_current_scribble_and_future_logits():
    s=torch.randn(1,8,2,2,requires_grad=True); t=torch.randn(1,8,2,2); labels=torch.full((1,2,2),IGNORE_INDEX); labels[0,0,0]=4
    scribble_mib_loss(s,t,labels,(1,2,3)).backward()
    assert s.grad[0,:,0,0].abs().sum()==0
    assert s.grad[0,6:].abs().sum()==0

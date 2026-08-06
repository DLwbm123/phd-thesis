import torch
from scribblecl.losses import partial_cross_entropy, scribble_mib_loss, masked_logits
from scribblecl.protocol import IGNORE_INDEX, old_classes, future_classes, stage
from scribblecl.metrics import benchmark_patient_dice
import numpy as np

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

def test_future_logits_are_masked_at_stage_evaluation():
    logits=torch.zeros(1,8,1,1); logits[:,7]=100
    assert masked_logits(logits,(0,1,2,3)).argmax(1).item() == 0

def test_seeded_shuffle_is_reproducible_for_zero_batch_audit():
    order=torch.randperm(17,generator=torch.Generator().manual_seed(42)).numpy()
    zero=np.zeros(17,dtype=bool); zero[order[:8]]=True
    assert zero[order[:8]].all() and not zero[order[8:16]].all()

def test_benchmark_metric_aggregates_patient_volumes_and_includes_background():
    target=np.array([[[0,1]],[[0,1]],[[0,1]],[[0,1]]])
    pred=target.copy(); pred[0,0,1]=0; pred[1,0,1]=0
    mean, per_class=benchmark_patient_dice(pred,target,[1,3],(0,1))
    eps=1e-5
    patient1_bg=(4+eps)/(6+eps); patient1_fg=eps/(2+eps)
    expected=np.mean([[patient1_bg,patient1_fg],[1.0,1.0]])
    assert abs(mean-expected)<1e-12
    assert set(per_class)=={0,1}

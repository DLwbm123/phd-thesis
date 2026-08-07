import torch
from scribblecl.losses import pce_ratio_flip_legacy_loss,legacy_ratio_mse
from scribblecl.protocol import IGNORE_INDEX

def test_ratio_term_supervises_unknown_pixels_and_background_only_slice():
    z=torch.zeros(1,8,2,2,requires_grad=True)
    y=torch.full((1,2,2),IGNORE_INDEX); y[0,0,0]=0
    pce_ratio_flip_legacy_loss(z,y,(1,2,3),1.0).backward()
    assert z.grad[0,0,1,1] < 0
    assert z.grad[0,1:4,1,1].sum() > 0
    assert z.grad[0,:,1,1].abs().sum() > 0

def test_isolated_ratio_matches_legacy_combined_difference():
    z=torch.randn(1,8,2,2,requires_grad=True); y=torch.full((1,2,2),IGNORE_INDEX); y[0,0,0]=0; y[0,0,1]=1
    from scribblecl.losses import partial_cross_entropy
    combined=pce_ratio_flip_legacy_loss(z,y,(1,2,3),.05)
    expected=partial_cross_entropy(z,y,(0,1,2,3))+.05*legacy_ratio_mse(z,y,(1,2,3))
    assert torch.allclose(combined,expected)

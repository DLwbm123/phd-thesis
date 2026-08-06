import numpy as np,torch
from scribblecl.model import ResUNet32
from scribblecl.protocol import IGNORE_INDEX
from scribblecl.zs_components import active_probabilities,sparse_onehot,em_ratios,integrity_loss,spatial_pseudo_correction,original_puzzlemix_cutout

def sample(n=2,size=32):
    x=torch.rand(n,1,size,size); y=torch.full((n,size,size),IGNORE_INDEX)
    y[:,0,:8]=0; y[:,8:10,8:16]=1; y[:,12:14,12:20]=2; y[:,16:18,16:24]=3
    return x,y

def test_probability_and_unknown_encoding():
    x,y=sample(); m=ResUNet32(); p=active_probabilities(m(x),(0,1,2,3)); o=sparse_onehot(y,(0,1,2,3))
    assert torch.allclose(p.sum(1),torch.ones_like(p[:,0]),atol=1e-6)
    assert torch.equal(o.sum(1),torch.ones_like(o[:,0])) and o[:,-1].bool().eq(y==IGNORE_INDEX).all()

def test_em_integrity_spatial_are_finite_and_backward_safe():
    x,y=sample(size=32); m=ResUNet32(); p=active_probabilities(m(x),(0,1,2,3))
    r=em_ratios(p,y,(0,1,2,3)); assert torch.isfinite(r).all() and abs(float(r.sum())-1)<1e-5
    integ=integrity_loss(p,y); e=spatial_pseudo_correction(p,x,y,(0,1,2,3))
    total=integ+e['pseudo']; assert torch.isfinite(total); total.backward()
    assert any(q.grad is not None for q in m.parameters())

def test_original_puzzlemix_cutout_consistency_smoke():
    np.random.seed(42); torch.manual_seed(42); x,y=sample(size=32); m=ResUNet32()
    parts=original_puzzlemix_cutout(m,x,y,(0,1,2,3))
    loss=parts['augmentation']+parts['consistency']; assert torch.isfinite(loss); loss.backward()

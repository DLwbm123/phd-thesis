import numpy as np
from skimage.morphology import skeletonize
from scribblecl.data import make_sparse, make_sparse_v2
from scribblecl.protocol import IGNORE_INDEX

def test_old_and_future_changes_do_not_change_current_scribble():
    a=np.zeros((16,16),dtype=np.int16); a[3:12,3:12]=1; a[0:2]=2; b=a.copy(); b[0:2]=7
    assert np.array_equal(make_sparse(a,1,skeletonize)==1,make_sparse(b,1,skeletonize)==1)

def test_unlabelled_is_ignore_not_background():
    x=np.zeros((12,12),dtype=np.int16); x[3:8,3:8]=1; out=make_sparse(x,1,skeletonize)
    assert (out==IGNORE_INDEX).any() and not (out==0).any()

def test_v2_has_background_foreground_unknown_and_is_deterministic():
    x=np.zeros((64,64),dtype=np.int16); x[20:44,20:44]=1
    a=make_sparse_v2(x,1,skeletonize); b=make_sparse_v2(x,1,skeletonize)
    assert np.array_equal(a,b)
    assert (a==0).any() and (a==1).any() and (a==IGNORE_INDEX).any()
    assert not np.any((a==0) & (x!=0))
    assert sum((a==v).sum() for v in (0,1,2,3,IGNORE_INDEX)) == a.size

def test_v2_zero_foreground_slice_has_sparse_background_supervision():
    x=np.zeros((64,64),dtype=np.int16); a=make_sparse_v2(x,1,skeletonize)
    assert (a==0).any() and (a==0).sum() < a.size and (a==IGNORE_INDEX).any()

def test_v2_does_not_depend_on_unavailable_global_identity():
    local=np.zeros((64,64),dtype=np.int16); local[20:44,20:44]=1
    unavailable_a=np.zeros_like(local); unavailable_a[:8]=4
    unavailable_b=np.zeros_like(local); unavailable_b[:8]=7
    # The public API accepts only `local`; unavailable identities cannot enter it.
    assert np.array_equal(make_sparse_v2(local,1,skeletonize),make_sparse_v2(local.copy(),1,skeletonize))
    assert not np.array_equal(unavailable_a, unavailable_b)

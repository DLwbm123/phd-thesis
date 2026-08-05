import numpy as np
from skimage.morphology import skeletonize
from scribblecl.data import make_sparse
from scribblecl.protocol import IGNORE_INDEX

def test_old_and_future_changes_do_not_change_current_scribble():
    a=np.zeros((16,16),dtype=np.int16); a[3:12,3:12]=1; a[0:2]=2; b=a.copy(); b[0:2]=7
    assert np.array_equal(make_sparse(a,1,skeletonize)==1,make_sparse(b,1,skeletonize)==1)

def test_unlabelled_is_ignore_not_background():
    x=np.zeros((12,12),dtype=np.int16); x[3:8,3:8]=1; out=make_sparse(x,1,skeletonize)
    assert (out==IGNORE_INDEX).any() and not (out==0).any()

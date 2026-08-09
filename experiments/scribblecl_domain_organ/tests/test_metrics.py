import numpy as np
import pytest

from scribblecl_do.metrics.matrix import adice,bwtr,rma,efwt,matrix_summary


def test_domain_matrix_metrics_match_benchmark():
    x=np.array([[.8,.2,.1],[.7,.75,.3],[.6,.65,.7]])
    assert adice(x)==pytest.approx((.6+.65+.7)/3)
    assert bwtr(x)==pytest.approx(np.mean([(.6-.8)/.8,(.65-.75)/.75]))
    assert rma(x,[.8,.70,.70])==pytest.approx(np.mean([.75/.70,.7/.70]))
    assert efwt(x,[.0,.1,.05])==pytest.approx(np.mean([.2-.1,.1-.05,.3-.05]))


def test_organ_matrix_metrics_match_benchmark():
    x=np.array([[.8,np.nan],[.6,.7]])
    assert adice(x)==pytest.approx(.65)
    assert bwtr(x)==pytest.approx(-.25)
    assert rma(x,[.8,.7])==pytest.approx(1.)


def test_efwt_domain_only():
    assert isinstance(efwt([[.8,.2],[.7,.75]],[.1,.1],"domain"),float)


def test_no_efwt_organ():
    with pytest.raises(ValueError): efwt([[.8,.2],[.7,.75]],[.1,.1],"organ")
    assert "E-FWT" not in matrix_summary([[.8,.2],[.7,.75]],[.8,.75],"organ")

"""Class-CL-safe adapters for the vendored ZScribbleSeg components."""
from types import SimpleNamespace
import numpy as np
import torch
import torch.nn.functional as F
from scipy import ndimage
from .losses import masked_logits
from .protocol import IGNORE_INDEX

def active_probabilities(logits, allowed):
    return torch.softmax(masked_logits(logits, allowed), 1)[:, allowed]

def sparse_onehot(sparse, allowed):
    """Known channels followed by an explicit unknown channel."""
    out=torch.zeros((sparse.shape[0],len(allowed)+1,*sparse.shape[1:]),device=sparse.device)
    for i,c in enumerate(allowed): out[:,i]=(sparse==c)
    out[:,-1]=(sparse==IGNORE_INDEX)
    return out.float()

def probability_pce(probs, sparse, allowed):
    known=sparse.ne(IGNORE_INDEX)
    if not known.any(): return probs.sum()*0
    loss=probs.sum()*0
    for i,c in enumerate(allowed):
        m=sparse.eq(c); loss=loss-torch.log(probs[:,i].clamp_min(1e-12))[m].sum()
    return loss/known.sum()

def apply_basic_geometry(x, sparse, code):
    """Paired right-angle geometry; code is supplied independently of the loader."""
    k=code%4; flip_h=(code//4)%2; flip_v=(code//8)%2
    x=torch.rot90(x,k,(-2,-1)); sparse=torch.rot90(sparse,k,(-2,-1))
    if flip_h: x=x.flip(-1); sparse=sparse.flip(-1)
    if flip_v: x=x.flip(-2); sparse=sparse.flip(-2)
    return x,sparse

def original_puzzlemix_cutout(model,x,sparse,allowed,lambda2=0.01):
    """Original PuzzleMix/Cutout/rotation equations with explicit probability adaptation."""
    from .vendor.zscribble.mixup import mixup_process
    from .vendor.zscribble.cutout import Cutout,rotate_invariant,rotate_back
    xvar=x.detach().requires_grad_(True)
    probs=active_probabilities(model(xvar),allowed)
    pce=probability_pce(probs,sparse,allowed)
    grad=torch.autograd.grad(pce,xvar,retain_graph=True,create_graph=False)[0]
    unary=torch.sqrt(torch.mean(grad**2,dim=1))
    onehot=sparse_onehot(sparse,allowed)
    args=SimpleNamespace(mixup_alpha=.5,in_batch=False,mean=torch.tensor(0.,device=x.device),
        std=torch.tensor(1.,device=x.device),box=False,graph=True,beta=1.2,gamma=.5,
        eta=.2,neigh_size=4,n_labels=3,transport=True,t_eps=.8,t_size=4,
        device=x.device)
    mixed,mixed_target,indices,mask=mixup_process(xvar,onehot,args=args,grad=unary,noise=None)
    cut,cut_target,cut_mask=Cutout(mixed,mixed_target,x.device)
    cut,cut_target,angles=rotate_invariant(cut,cut_target)
    cut_probs=active_probabilities(model(cut),allowed)
    _,cut_back,cut_target=rotate_back(cut,cut_probs,cut_target[:,:len(allowed)],angles)
    cut_probs=cut_back['pred_masks']
    annotated=cut_target.sum(1,keepdim=True)
    augmentation=(-cut_target*torch.log(cut_probs.clamp_min(1e-12))).sum(1,keepdim=True)
    augmentation=(augmentation*annotated).mean()
    shuffled=probs[indices]
    expected=probs*mask+shuffled*(1-mask)
    expected=expected*cut_mask[:,:1]
    consistency=lambda2*(1-F.cosine_similarity(cut_probs,expected,dim=1).mean())
    return {'augmentation':augmentation,'consistency':consistency,
            'puzzlemix_mask_mean':mask.mean().detach()}

def _largest_components(pred):
    result=np.zeros_like(pred,dtype=np.int64)
    heart=ndimage.label(pred>0)[0]
    if heart.max():
        sizes=np.bincount(heart.ravel()); sizes[0]=0; heart_keep=heart==sizes.argmax()
    else: heart_keep=np.zeros_like(pred,dtype=bool)
    for c in range(1,int(pred.max())+1):
        blobs,n=ndimage.label(pred==c)
        if n:
            sizes=np.bincount(blobs.ravel()); sizes[0]=0
            result[(blobs==sizes.argmax())&heart_keep]=c
    return result

def integrity_loss(probs,sparse):
    pseudo=[]
    for p in probs.detach().argmax(1).cpu().numpy(): pseudo.append(_largest_components(p))
    pseudo=torch.as_tensor(np.stack(pseudo),device=probs.device)
    unknown=sparse.eq(IGNORE_INDEX); values=[]
    for c in range(probs.shape[1]):
        m=unknown & pseudo.eq(c)
        if m.any(): values.append(-torch.log(probs[:,c].clamp_min(1e-12))[m])
    return torch.cat(values).mean() if values else probs.sum()*0

def em_ratios(probs,sparse,allowed,iterations=100,tol=1e-3):
    """Stable adaptation of the source EM on known scribble pixels only."""
    known=sparse.ne(IGNORE_INDEX)
    if not known.any(): return None
    g=torch.stack([(sparse==c)[known].float() for c in allowed],1)
    q=probs.permute(0,2,3,1)[known].detach()
    base=g.mean(0).clamp_min(1e-6); prior=base/base.sum()
    for _ in range(iterations):
        num=prior*q/base; new=(num/num.sum(1,keepdim=True).clamp_min(1e-12)).mean(0)
        if (new-prior).abs().sum()<tol: prior=new; break
        prior=new
    return prior

def spatial_pseudo_correction(probs,x,sparse,allowed):
    from .vendor.zscribble.spatial_function import ModelWeightGatedCRF
    ratios=em_ratios(probs,sparse,allowed)
    zero=probs.sum()*0
    if ratios is None: return {'pseudo':zero,'em_ratios':None,'spatial_mean':zero.detach()}
    spatial=ModelWeightGatedCRF()(probs,[{'weight':1,'xy':6,'rgb':.1}],5,
        x.detach().clone(),x.shape[-2],x.shape[-1])
    unknown=sparse.eq(IGNORE_INDEX); negative=torch.zeros_like(probs,dtype=torch.bool)
    for c in range(1,len(allowed)):
        vals=spatial[:,c][unknown]
        if vals.numel():
            keep=max(int(vals.numel()*(1-float(ratios[c])))-1,0)
            threshold=torch.sort(vals).values[keep]
            negative[:,c]=unknown & spatial[:,c].lt(threshold)
    selected=negative.any(1)
    remaining=(probs*(~negative)).sum(1).clamp_min(1e-12)
    pseudo=(-torch.log(remaining)[selected]).mean() if selected.any() else zero
    return {'pseudo':pseudo,'em_ratios':ratios.detach(),'spatial_mean':spatial.mean().detach()}

def component_gradient_norm(loss,model):
    grads=torch.autograd.grad(loss,[p for p in model.parameters() if p.requires_grad],
                              retain_graph=True,allow_unused=True)
    return float(torch.sqrt(sum((g.detach()**2).sum() for g in grads if g is not None)))

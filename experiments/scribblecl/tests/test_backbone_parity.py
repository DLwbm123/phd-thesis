import torch
import torch.nn as nn
import torch.nn.functional as F
from scribblecl.model import ResUNet32

class RefBlock(nn.Module):
    def __init__(self,a,b,stride=1):
        super().__init__(); self.bn1=nn.BatchNorm2d(a); self.conv1=nn.Conv2d(a,b,3,stride,1,bias=False); self.bn2=nn.BatchNorm2d(b); self.conv2=nn.Conv2d(b,b,3,1,1,bias=False); self.skip=nn.Conv2d(a,b,3,stride,1,bias=False)
    def forward(self,x): return self.conv2(F.relu(self.bn2(self.conv1(F.relu(self.bn1(x))))))+self.skip(x)
class Ref(nn.Module):
    def __init__(self):
        super().__init__(); self.c1=nn.Conv2d(1,32,3,1,1,bias=False); self.bn=nn.BatchNorm2d(32); self.c2=nn.Conv2d(32,32,3,1,1,bias=False); self.d1=RefBlock(32,64,2); self.d2=RefBlock(64,128,2); self.b=RefBlock(128,256,2); self.u1=RefBlock(384,128); self.u2=RefBlock(192,64); self.u3=RefBlock(96,32); self.last=nn.Conv2d(32,8,1,bias=False)
    def forward(self,x):
        a=self.c2(F.relu(self.bn(self.c1(x)))); b=self.d1(a); c=self.d2(b); d=self.b(c)
        d=self.u1(torch.cat([F.interpolate(d,scale_factor=2,mode='bilinear'),c],1)); d=self.u2(torch.cat([F.interpolate(d,scale_factor=2,mode='bilinear'),b],1)); return self.last(self.u3(torch.cat([F.interpolate(d,scale_factor=2,mode='bilinear'),a],1)))

def test_exact_benchmark_resunet32_forward_parity():
    torch.manual_seed(42); ref=Ref(); cur=ResUNet32()
    assert sum(p.numel() for p in ref.parameters())==sum(p.numel() for p in cur.parameters())==2916000
    assert [p.shape for p in ref.parameters()]==[p.shape for p in cur.parameters()]
    with torch.no_grad():
        for a,b in zip(ref.parameters(),cur.parameters()): b.copy_(a)
    ref.eval(); cur.eval(); x=torch.randn(2,1,64,64)
    assert torch.equal(ref(x),cur(x))

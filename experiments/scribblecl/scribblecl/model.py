"""ResUNet32-compatible compact backbone.

Source: Benchmark_pa/backbone/ResUnet.py (ResidualConv/ResUNet topology).
Adaptation: fixed eight-channel head is explicit for Class-CL.
"""
import torch.nn as nn
import torch.nn.functional as F

class Block(nn.Module):
    def __init__(self, a, b, stride=1):
        super().__init__(); self.net=nn.Sequential(nn.BatchNorm2d(a),nn.ReLU(),nn.Conv2d(a,b,3,stride,1,bias=False),nn.BatchNorm2d(b),nn.ReLU(),nn.Conv2d(b,b,3,1,1,bias=False)); self.skip=nn.Conv2d(a,b,3,stride,1,bias=False)
    def forward(self,x): return self.net(x)+self.skip(x)

class ResUNet32(nn.Module):
    def __init__(self, channels=8, width=32):
        super().__init__(); self.stem=nn.Sequential(nn.Conv2d(1,width,3,1,1,bias=False),nn.BatchNorm2d(width),nn.ReLU(),nn.Conv2d(width,width,3,1,1,bias=False)); self.d1=Block(width,width*2,2); self.d2=Block(width*2,width*4,2); self.bridge=Block(width*4,width*8,2); self.u1=Block(width*8+width*4,width*4); self.u2=Block(width*4+width*2,width*2); self.u3=Block(width*2+width,width); self.head=nn.Conv2d(width,channels,1,bias=False)
    def forward(self,x):
        a=self.stem(x); b=self.d1(a); c=self.d2(b); d=self.bridge(c)
        d=F.interpolate(d,size=c.shape[-2:],mode='bilinear',align_corners=False); d=self.u1(__import__('torch').cat([d,c],1))
        d=F.interpolate(d,size=b.shape[-2:],mode='bilinear',align_corners=False); d=self.u2(__import__('torch').cat([d,b],1))
        d=F.interpolate(d,size=a.shape[-2:],mode='bilinear',align_corners=False); return self.head(self.u3(__import__('torch').cat([d,a],1)))

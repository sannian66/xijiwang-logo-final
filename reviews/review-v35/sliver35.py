# v3.5 review: detect hairline "double line" inside the outline band: ink - lighter - ink sandwich of <=4 px along columns AND rows, whole frame
import numpy as np; from PIL import Image
def alpha(f,s):
    g=np.asarray(Image.open(f'f{s}/f{f:04d}.png').convert('L'),float)
    return np.clip((255-g)/(255-36),0,1) if s=='l' else np.clip(g/245,0,1)
def sandwich(a,axis):
    A=a if axis==0 else a.T; hits=[]; depth=0
    for gap in (1,2,3,4):
        up=A[:-gap-1]; dn=A[gap+1:]
        mid=np.min(np.stack([A[1+k:A.shape[0]-gap+k] for k in range(gap)]),0)
        lo=np.minimum(up,dn); m=(lo>.85)&(mid<lo-.12)
        if m.any(): hits.append(m.sum()); depth=max(depth,float((lo-mid)[m].max()))
    return sum(hits),depth
for s in 'ld':
    print('==',s)
    for f in range(118,152):
        a=alpha(f,s); n0,d0=sandwich(a,0); n1,d1=sandwich(a,1)
        if n0+n1: print(f'f{f} hairline px {n0+n1:5d}  max dip {max(d0,d1):.2f}')

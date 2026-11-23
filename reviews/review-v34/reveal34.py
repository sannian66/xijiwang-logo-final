# per-frame on-screen lion metrics f126-f175 (light): ink coverage (alpha-weighted), mane bbox (alpha>.5), nose-tip x; ring arc below chin
from PIL import Image; import numpy as np
print('frame  t      inkArea(px,alpha-wtd)  bbox(w x h, alpha>.5)  bboxCenterY  bottomY')
prev=None
for f in range(126,176):
    a=np.asarray(Image.open(f'fl/f{f:04d}.png').convert('L'),float)
    al=np.clip((255-a)/(255-36),0,1)
    ys,xs=np.nonzero(al>.5)
    area=al.sum()
    w=xs.max()-xs.min(); h=ys.max()-ys.min()
    print(f'f{f} {f/60:.3f} {area:10.0f} {w:5d} x {h:5d}  cy {(ys.max()+ys.min())/2:7.1f} bot {ys.max()}')

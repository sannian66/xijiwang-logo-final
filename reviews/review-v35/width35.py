# v3.5 review: on-screen band thickness f126-f146 (ink area / half outer+inner perimeter), nose excluded, light & dark
import numpy as np; from PIL import Image
from scipy import ndimage as nd
for s in 'ld':
    print('==',s); prev=None
    for f in range(126,147):
        g=np.asarray(Image.open(f'f{s}/f{f:04d}.png').convert('L'),float)
        a=np.clip((255-g)/219,0,1) if s=='l' else np.clip(g/245,0,1)
        H,W=a.shape; yy,xx=np.mgrid[:H,:W]
        cy,cx=np.argwhere(a[650:850,1150:1400]>.5).mean(0)+[650,1150]
        ring=a*(np.hypot(yy-cy,xx-cx)>60)
        b=ring>.5; per=(b^np.roll(b,1,0)).sum()+(b^np.roll(b,1,1)).sum()
        w=2*ring.sum()/per*0.785   # *pi/4 corrects 4-connected perimeter overcount
        line=f'f{f} band~{w:6.2f}px area {ring.sum():8.0f}'
        if prev: line+=f'  width x{w/prev:5.3f}'
        prev=w; print(line)

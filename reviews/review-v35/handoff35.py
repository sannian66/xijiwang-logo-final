# v3.5 review: ring -> outline handoff continuity f112-f126: ring bbox, ink area of ring, mean stroke width, frame-to-frame deltas
import numpy as np; from PIL import Image
for s in 'ld':
    print('==',s); prev=None
    for f in range(112,127):
        g=np.asarray(Image.open(f'f{s}/f{f:04d}.png').convert('L'),float)
        a=np.clip((255-g)/219,0,1) if s=='l' else np.clip(g/245,0,1)
        H,W=a.shape; yy,xx=np.mgrid[:H,:W]
        # nose ▶ = ink within 120px of its own centroid near frame centre region
        cy,cx=np.argwhere(a[600:900,1150:1450]>.5).mean(0)+[600,1150]
        ring=a*(np.hypot(yy-cy,xx-cx)>140)
        ys,xs=np.where(ring>.5); area=ring.sum()
        # perimeter estimate via boundary count -> width = area/(perimeter/2)
        b=(ring>.5); per=(b^np.roll(b,1,0)).sum()+(b^np.roll(b,1,1)).sum()
        w=2*area/per
        line=f'f{f} nose({cx:.1f},{cy:.1f}) bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} area {area:9.0f} width~{w:5.2f}px'
        if prev: line+=f'  dArea {100*(area/prev-1):+5.2f}%'
        prev=area; print(line)

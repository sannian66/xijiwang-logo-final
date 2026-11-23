# hairline detector: pixels lighter (light mode) / darker (dark) than ink while ink sits 3px left and right
from PIL import Image; import numpy as np
for m in 'ld':
  for f in range(86,126):
    a=np.asarray(Image.open(f'v34{m}/f%04d.png'%f).convert('L')).astype(int)
    ink=a.min() if m=='l' else a.max()
    isink=np.abs(a-ink)<12
    L=np.roll(isink,3,1); R=np.roll(isink,-3,1)
    mid=np.abs(a-ink)>=8
    s=mid&L&R
    ys,xs=np.nonzero(s)
    if len(xs): print(m,f,'seam px',len(xs),'cols',xs.min(),xs.max(),'max contrast',np.abs(a-ink)[s].max())
    else: print(m,f,'no seam')

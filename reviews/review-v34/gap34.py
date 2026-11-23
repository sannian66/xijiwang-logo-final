# gap between the two morph halves along 5 rows through the glyph, f94-f104; reports the lightest (light) / darkest (dark) interior pixel between the halves
from PIL import Image; import numpy as np
for m in 'ld':
  for f in range(94,106):
    a=np.asarray(Image.open(f'f{m}/f%04d.png'%f).convert('L')).astype(int)
    al=np.clip((255-a)/219,0,1) if m=='l' else np.clip(a/245,0,1)
    out=[]
    for y in (700,725,750,775,800):
        r=al[y,1100:1470]; ink=np.nonzero(r>.9)[0]
        if len(ink)<2: out.append('-'); continue
        seg=r[ink.min():ink.max()+1]; mn=seg.min(); gapw=(seg<.5).sum()
        out.append(f'minα {mn:.2f} gap {gapw}px')
    print(m,f,' | '.join(out))

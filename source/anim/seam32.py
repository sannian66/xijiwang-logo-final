# seam check: frames f84..f120 (1.40–2.00s), top/bottom silhouette of the nose shape must be clean (no notches/steps)
import numpy as np, sys
from PIL import Image
d=sys.argv[1]; dark=len(sys.argv)>2
cx,cy=None,None
tiles=[]
for f in range(84,121):
    a=np.asarray(Image.open(f'{d}/f{f:04d}.png').convert('L')).astype(int)
    ink=(a>128) if dark else (a<128)
    # restrict to the button region around the nose centre (find bbox of ink inside central window)
    H,W=a.shape; win=ink[H//2-350:H//2+350, :]
    ys,xs=np.nonzero(win)
    # button ink: exclude ring (thin) by taking largest component near centre
    from scipy.ndimage import label, binary_opening
    lab,n=label(win); 
    sizes=np.bincount(lab.ravel()); sizes[0]=0
    from scipy.ndimage import find_objects
    ids=[i+1 for i,sl in enumerate(find_objects(lab)) if sl is not None and sizes[i+1]>2000 and (sl[1].stop-sl[1].start)<450 and (sl[0].stop-sl[0].start)<450]
    keep=np.isin(lab, ids)
    ys,xs=np.nonzero(keep)
    if len(xs)==0: print(f,'none'); continue
    x0,x1=xs.min(),xs.max(); 
    tops=[];bots=[];cols=[]
    for x in range(x0,x1+1):
        c=np.nonzero(keep[:,x])[0]
        if len(c): cols.append(x); tops.append(c.min()); bots.append(c.max())
    cols=np.array(cols); tops=np.array(tops); bots=np.array(bots)
    # interior 15%..85% of width (excludes outer rounded corners & tip)
    m=(cols>x0+.15*(x1-x0))&(cols<x0+.85*(x1-x0))
    res=[]
    for e in (tops,bots):
        pf=np.polyfit(cols[m],e[m],1); r=e[m]-np.polyval(pf,cols[m]); res.append(np.abs(r).max())
    gap=(x1-x0+1)-len(cols)
    print(f, f'{f/60:.3f}s', 'width',x1-x0+1,'gapcols',gap,'top dev px %.1f'%res[0],'bot dev px %.1f'%res[1])
    tiles.append(np.asarray(Image.open(f'{d}/f{f:04d}.png').convert('L'))[H//2-350+min(ys)-20:H//2-350+max(ys)+20, x0-20:x1+20])

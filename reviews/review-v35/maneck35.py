# v3.5 review: radial 720-sample contour vs true mane outer contour (lion-local units). read-only import of a copy of mane35.py
import sys; sys.path.insert(0,'/tmp'); import numpy as np, mane35
SRC='../../assets/xijiwang-horizontal-primary-af6d799ceb5b.svg'
r,pts,ang=mane35.samples(SRC,N=720)
C=complex(131.5,147); a=-np.pi+2*np.pi*np.arange(720)/720; poly=C+r*np.exp(1j*a)
# distance from every true contour point to the polygon (dense)
P=np.concatenate([np.linspace(poly[k],poly[(k+1)%720],8,endpoint=False) for k in range(720)])
from scipy.spatial import cKDTree
t=cKDTree(np.c_[P.real,P.imag]); d,_=t.query(np.c_[pts.real,pts.imag])
print('true contour -> radial polygon: max %.3f u, p99 %.3f, mean %.4f'%(d.max(),np.percentile(d,99),d.mean()))
bad=d>0.3; print('points >0.3u:',bad.sum(),'of',len(d))
if bad.any():
    angs=np.degrees(np.angle(pts[bad]-C)); print('angles of deviation (deg, 0=right, +90=down): %.1f..%.1f'%(angs.min(),angs.max()))
    i=d.argmax(); print('worst at',pts[i],'angle %.1f'%np.degrees(np.angle(pts[i]-C)))
# angular monotonicity (star-shapedness)
u=np.unwrap(ang); du=np.diff(u); s=np.sign(u[-1]-u[0]); back=(du*s<0); print('backtracking steps',back.sum())
if back.any(): print('backtrack angles deg', np.round(np.degrees(np.angle(pts[1:][back]-C))[::max(1,back.sum()//10)],1))
# polygon edge length in 2K px at final scale (lion unit -> px: 2560/1280*... )
seg=np.abs(np.diff(np.r_[poly,poly[:1]])); print('polygon seg len u: max %.3f mean %.3f'%(seg.max(),seg.mean()))

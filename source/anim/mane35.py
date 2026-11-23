# v3.5: radial samples of the mane's outer contour about the nose centre (131.5,147), lion-local units
import re, numpy as np
from svgpathtools import parse_path
C=complex(131.5,147)
def samples(svg='src.svg', N=360):
    s=open(svg).read(); ds=re.findall(r'd="([^"]*)"',s)
    outer=[x.strip() for x in re.split(r'(?=M)',ds[0]) if x.strip()][0]
    p=parse_path(outer)
    pts=np.array([p.point(t) for t in np.linspace(0,1,20000,endpoint=False)])
    ang=np.angle(pts-C); rad=np.abs(pts-C)
    out=[]
    for k in range(N):
        a=-np.pi+2*np.pi*k/N
        d=np.angle(np.exp(1j*(ang-a)))
        m=np.abs(d)<0.004
        out.append(rad[m].max())
    return np.array(out), pts, ang
if __name__=='__main__':
    r,pts,ang=samples()
    print(r.min(),r.max())
    # star-shaped check: angle along contour monotone?
    u=np.unwrap(ang); du=np.diff(u); print('nonmonotone steps',(du<0).sum() if u[-1]>u[0] else (du>0).sum(), 'total turn',(u[-1]-u[0])/np.pi)

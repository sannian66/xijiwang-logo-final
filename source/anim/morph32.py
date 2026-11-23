# Baked pause->play(nose) morph keyframes for v3.2 (imported by build31.py).
# Two halves; seam corners always lie on the common top/bottom silhouette line, so no kink or hairline.
import numpy as np
def bez(x1,y1,x2,y2):
    def f(t):
        # solve x(s)=t then y(s)
        s=t
        for _ in range(30):
            x=3*(1-s)**2*s*x1+3*(1-s)*s**2*x2+s**3; dx=3*(1-s)**2*x1+6*(1-s)*s*(x2-x1)+3*s**2*(1-x2)
            if abs(dx)<1e-9: break
            s=min(1,max(0,s-(x-t)/dx))
        return 3*(1-s)**2*s*y1+3*(1-s)*s**2*y2+s**3
    return f
emph=bez(.2,0,0,1)
L=lambda a,b,p: a+(b-a)*p
def fmt(v): return ('%.4f'%v).rstrip('0').rstrip('.').replace('-0','-0') if abs(v)>5e-4 else '0'
def P(*pts): return ' '.join(fmt(v) for v in pts)
def shapes(p):
    # seam closes faster than the rest (q), so the gap never lingers as a hairline
    q=1-(1-min(p/0.9,1))**2
    r=2.5*max(0,1-q/0.5)                        # v3.2: seam corners go sharp before the halves touch (no V-notch)
    # outer anchor points (left half TL corner end, right half tip-start) lerp with p
    LTLe=(L(-9,-8.617,p),L(-13,-11.468,p))      # end of left TL rounding (start of top edge)
    RTRs=(L(9,8.617,p),L(-13,-2.532,p))         # start of right TR rounding (end of top edge)
    line=lambda x: LTLe[1]+(RTRs[1]-LTLe[1])*(x-LTLe[0])/(RTRs[0]-LTLe[0])
    xL=L(-3.5,0.95,q); xR=L(3.5,-0.95,q)   # v3.2: halves overlap more
    yL=line(xL); yR=line(xR)
    # left half
    dl=np.array([xL-LTLe[0],yL-LTLe[1]]); dl/=np.hypot(*dl)
    aL=(xL-r*dl[0],yL-r*dl[1])
    left=("M"+P(L(-11.5,-13.5,p),L(-10.5,-8.5,p))+" Q"+P(L(-11.5,-13.5,p),L(-13,-14,p),*LTLe)+
          " L"+P(*aL)+" Q"+P(xL,yL,xL,yL+r)+" L"+P(xL,-yL-r)+" Q"+P(xL,-yL,aL[0],-aL[1])+
          " L"+P(LTLe[0],-LTLe[1])+" Q"+P(L(-11.5,-13.5,p),L(13,14,p),L(-11.5,-13.5,p),L(10.5,8.5,p))+" Z")
    dr=np.array([RTRs[0]-xR,RTRs[1]-yR]); dr/=np.hypot(*dr)
    bR=(xR+r*dr[0],yR+r*dr[1])
    right=("M"+P(xR,yR+r)+" Q"+P(xR,yR,*bR)+" L"+P(*RTRs)+
           " Q"+P(L(11.5,11.0585,p),L(-13,-1.266,p),L(11.5,11.0585,p),L(-10.5,0,p))+
           " L"+P(L(11.5,11.0585,p),L(10.5,0,p))+
           " Q"+P(L(11.5,11.0585,p),L(13,1.266,p),RTRs[0],-RTRs[1])+
           " L"+P(bR[0],-bR[1])+" Q"+P(xR,-yR,xR,-yR-r)+" Z")
    return left,right
def keyframes(n=30):
    outL=[];outR=[]
    for k in range(n+1):
        p=emph(k/n); l,r=shapes(p); pc=fmt(100*k/n)+'%'
        outL.append(f'    {pc} {{ d: path("{l}"); }}'); outR.append(f'    {pc} {{ d: path("{r}"); }}')
    return "@keyframes morphL {\n"+"\n".join(outL)+"\n  }\n  @keyframes morphR {\n"+"\n".join(outR)+"\n  }"
def jsdata(n=60):
    # v3.2: keyframes for the JS driver (Safari has no CSS d:path()). Same eased curve, linear between keyframes.
    import json
    L_=[];R_=[]
    for k in range(n+1):
        l,r=shapes(emph(k/n)); L_.append(l); R_.append(r)
    return json.dumps({'L':L_,'R':R_})
if __name__=='__main__':
    for p in (0,1): print(shapes(p))

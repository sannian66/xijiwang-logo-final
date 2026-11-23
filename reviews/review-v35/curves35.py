# v3.5 review: per-frame values of the JS/CSS drivers (re-implemented from template35.html): morph m, thicken f, outline width, mask width, feature opacity, cam
import sys; sys.path.insert(0,'/tmp'); 
def bez(x1,y1,x2,y2):
    def f(t):
        if t<=0: return 0.
        if t>=1: return 1.
        s=t
        for _ in range(40):
            x=3*(1-s)**2*s*x1+3*(1-s)*s*s*x2+s**3-t; dx=3*(1-s)**2*x1+6*(1-s)*s*(x2-x1)+3*s*s*(1-x2)
            if abs(dx)<1e-9: break
            s=min(1,max(0,s-x/dx))
        return 3*(1-s)**2*s*y1+3*(1-s)*s*s*y2+s**3
    return f
E=bez(.2,0,0,1); T=bez(.35,0,.15,1); S=bez(.4,0,.2,1); cl=lambda v:min(1,max(0,v))
print('frame  t(ms)   m(morph)  dm     f(thick)  df     OLw(u)  maskW(u) feat  cam')
pm=pf=0
for fr in range(116,182):
    ms=fr*1000/60; s=1+.6*E(cl((ms-1900)/1600)); w0=1.6*s/.9
    m=E(cl((ms-2000)/450)); f=T(cl((ms-2200)/700))
    olw=w0*(1-f) if 2000<=ms<2950 else 0; mw=0 if ms<2200 else 2*w0*(1-f)+220*f
    feat=S(cl((ms-2400)/220)); cam=1+1.8*(1-E(cl((ms-1900)/1600)))
    print(f'f{fr:3d} {ms:7.1f}  {m:7.3f} {m-pm:+6.3f}  {f:7.3f} {f-pf:+6.3f}  {olw:6.2f}  {mw:7.2f}  {feat:4.2f}  {cam:5.3f}')
    pm,pf=m,f

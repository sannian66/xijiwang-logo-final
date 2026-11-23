# reproduces the v3.3 timing functions from template33.html to tabulate reveal radius / fade, and morph progress
def cubic(x1,y1,x2,y2):
    def f(x):
        if x<=0: return 0.
        if x>=1: return 1.
        s=x
        for _ in range(40):
            X=3*(1-s)**2*s*x1+3*(1-s)*s*s*x2+s**3-x; dX=3*(1-s)**2*x1+6*(1-s)*s*(x2-x1)+3*s*s*(1-x2)
            if abs(dX)<1e-9: break
            s=min(1,max(0,s-X/dX))
        return 3*(1-s)**2*s*y1+3*(1-s)*s*s*y2+s**3
    return f
DEC=cubic(.05,.7,.1,1); EMPH=cubic(.2,0,0,1)
print('frame  t     r(clip)  %travel  fadeOpacity')
for fr in range(132,160):
    t=fr/60*1000; g=(t-2200)/900
    r=0 if g<0 else 86+42*DEC(min(g,1)); op=min(1,max(0,(t-2200)/100))
    print(f'f{fr} {t/1000:.3f} {r:7.2f} {100*(r-86)/42 if r else 0:6.1f}% {op:.2f}')
print('\nmorph progress (EMPH over 1.45-2.05):')
for fr in range(86,125,2):
    t=fr/60; x=(t-1.45)/.6; print(f'f{fr} {t:.3f} {100*EMPH(max(0,min(1,x))):5.1f}%')

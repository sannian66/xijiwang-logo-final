# v3.4 timing: camera scale (emph 1.9s+1.6s, 2.8->1) x reveal grow (decel 2.2s+.7s, .72->1) = on-screen lion scale; plus ring opacity & lion fade
def cubic(x1,y1,x2,y2):
    def f(x):
        if x<=0: return 0.
        if x>=1: return 1.
        s=x
        for _ in range(50):
            X=3*(1-s)**2*s*x1+3*(1-s)*s*s*x2+s**3-x; dX=3*(1-s)**2*x1+6*(1-s)*s*(x2-x1)+3*s*s*(1-x2)
            if abs(dX)<1e-9: break
            s=min(1,max(0,s-X/dX))
        return 3*(1-s)**2*s*y1+3*(1-s)*s*s*y2+s**3
    return f
DEC=cubic(.05,.7,.1,1); EMPH=cubic(.2,0,0,1); SOFT=cubic(.4,0,.2,1)
cam=lambda t:2.8-1.8*EMPH((t-1.9)/1.6)
grow=lambda t:.72+.28*DEC((t-2.2)/.7)
print('frame t     cam    grow   net(on-screen, rel. to f133)  lionOpacity ringOpacity')
n0=cam(133/60)*grow(133/60)
for fr in range(130,160):
    t=fr/60
    print(f'f{fr} {t:.3f} {cam(t):.3f} {grow(t):.3f} {cam(t)*grow(t)/n0:6.3f}   {min(1,max(0,(t-2.2)/.05)):.2f}  {1-SOFT(min(1,max(0,(t-2.18)/.12))):.2f}')
# alternative: camera starts 2.40 instead of 1.9 for the lion part? report net with cam delayed by d
for d in (0,.25,.4):
    print('cam delay',d, ' net on-screen peak / f133:', max(cam(fr/60-d)*grow(fr/60) for fr in range(133,200))/(cam(133/60-d)*grow(133/60)))

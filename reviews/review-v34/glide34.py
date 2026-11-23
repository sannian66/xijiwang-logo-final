# glide pitch progress (sfx34 smoothstep) vs visual morph progress (soft bezier) — time at which each reaches 10/50/90 %
import sys; sys.dont_write_bytecode=True
import numpy as np, sys; sys.path.insert(0,'../../source/anim'); from morph34 import bez
S=bez(.4,0,.2,1); t=np.linspace(0,.6,6001); x=t/.6
vis=np.array([S(v) for v in x]); aud=x*x*(3-2*x)
for q in (.1,.25,.5,.75,.9):
    tv=1.45+t[np.argmax(vis>=q)]; ta=1.45+t[np.argmax(aud>=q)]
    print(f'{int(q*100):3d}%  visual {tv:.3f}s  audio pitch {ta:.3f}s  audio lag {1000*(ta-tv):+.0f} ms')
print('max |aud-vis| = %.3f at t=%.3f'%(np.abs(aud-vis).max(),1.45+t[np.abs(aud-vis).argmax()]))

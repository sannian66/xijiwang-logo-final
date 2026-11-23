# which easing is baked into the delivered v3.4 HTML morph table? compare against morph34.shapes() under emph vs soft
import sys; sys.dont_write_bytecode=True
import re,json,os,sys,importlib
sys.path.insert(0,'../../source/anim')
h=open('../../deliverables/xijiwang-logo-v3.4-play.html').read()
m=re.search(r'(\{"L":\s*\[.*?\],\s*"R":\s*\[.*?\]\})',h,re.S); D=json.loads(m.group(1))
res={}
for e in ('emph','soft'):
    os.environ['MORPH_EASE']=e
    import morph34; importlib.reload(morph34)
    J=json.loads(morph34.jsdata(60)); res[e]=sum(a==b for a,b in zip(J['L'],D['L']))+sum(a==b for a,b in zip(J['R'],D['R']))
print('keyframes matching (of 122):',res)
# progress per frame under soft
from morph34 import bez
S=bez(.4,0,.2,1); E=bez(.2,0,0,1)
for fr in range(86,125,2):
    t=fr/60; x=max(0,min(1,(t-1.45)/.6)); print(f'f{fr} {t:.3f} soft {100*S(x):5.1f}%  (emph would be {100*E(x):5.1f}%)')
import numpy as np
xs=np.linspace(0,1,2001); ys=np.array([S(x) for x in xs]); print('soft peak speed x linear: %.2f at x=%.2f'%(np.max(np.diff(ys)/np.diff(xs)),xs[np.argmax(np.diff(ys))]))

# Re-runs a read-only copy of source/anim/sfx33.py in-process, tagging each add() by its start time,
# and recovers the limiter's gain-reduction curve. Writes nothing into the repo outside review-v33/.
import numpy as np, sys, re
src=open('../../source/anim/sfx33.py').read()
src=src.replace("def add(sig,start,pan=0.0,gain=1.0):","COMP={}\ndef add(sig,start,pan=0.0,gain=1.0):\n    k=round(start,3); i0=int(round(start*SR)); s2=sig[:max(0,N-i0)]*gain; c=COMP.setdefault(k,np.zeros(N)); c[i0:i0+len(s2)]+=s2")
src=src.replace("for it in range(12):","PRE=st.copy()\nfor it in range(12):")
src=src.replace("w=wave.open(OUT,'wb')","raise SystemExit")
sys.argv=['x','/tmp/probe33.wav']; g={}
try: exec(compile(src,'sfx33_probe','exec'),g)
except SystemExit: pass
SR=g['SR']; st=g['st']; PRE=g['PRE']; COMP=g['COMP']
gain=np.sqrt((st**2).sum(1)+1e-20)/np.sqrt((PRE**2).sum(1)+1e-20)
ref=np.median(gain[int(3.0*SR):int(3.5*SR)])
def db(x): return 20*np.log10(np.maximum(np.abs(x),1e-9))
print('limiter gain relative to unlimited level (dB), 5 ms means:')
for t in np.arange(2.18,2.56,.01):
    a=int(t*SR); print(f'  {t:.2f}s  {db(gain[a:a+240].mean()/ref):6.2f}')
print('\ncomponent RMS (dB) in 10 ms windows:')
keys=sorted(COMP); print('  t     '+' '.join(f'{k:>7}' for k in keys))
for t in np.arange(2.36,2.48,.01):
    a=int(t*SR); print(f'  {t:.2f} '+' '.join(f'{db(np.sqrt((COMP[k][a:a+480]**2).mean())):7.1f}' for k in keys))
# where does the final signal's 2.40-2.44 rise come from: compare final vs pre-limiter envelope
for name,x in (('final',st.mean(1)),('prelimit',PRE.mean(1))):
    e=[10*np.log10((x[int(t*SR):int(t*SR)+480]**2).mean()+1e-20) for t in np.arange(2.38,2.46,.005)]
    print(name,' '.join(f'{v:.1f}' for v in e))

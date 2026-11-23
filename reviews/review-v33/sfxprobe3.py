# isolates the 2.40-2.43 s bump: dry bus vs reverb return, Hilbert envelopes in 5 ms bins, mono sum, final gain applied
import numpy as np, sys
from scipy.signal import hilbert, butter, sosfilt
src=open('../../source/anim/sfx33.py').read()
src=src.replace("st=np.stack([L+.6*verb(L),R+.6*verb(R)],1)","DRY=np.stack([L,R],1); WET=np.stack([.6*verb(L),.6*verb(R)],1); st=DRY+WET")
src=src.replace("for it in range(12):","PRE=st.copy()\nfor it in range(12):")
src=src.replace("w=wave.open(OUT,'wb')","raise SystemExit")
sys.argv=['x','/tmp/probe33c.wav']; g={}
try: exec(compile(src,'p','exec'),g)
except SystemExit: pass
SR=g['SR']; st=g['st']; PRE=g['PRE']; k=np.sqrt((st**2).sum()/(PRE**2).sum())
hp=butter(2,30,'highpass',fs=SR,output='sos')
def env(x):
    x=sosfilt(hp,x)*k; e=np.abs(hilbert(x)); w=int(.005*SR); a=int(2.30*SR); b=int(2.55*SR)
    return 20*np.log10(e[a:b][:(b-a)//w*w].reshape(-1,w).mean(1)+1e-9)
D=env(g['DRY'].mean(1)); W=env(g['WET'].mean(1)); M=env(st.mean(1)/k)
print(' t      dry    wet   mix   (dB, 5 ms Hilbert envelope)')
for i,t in enumerate(np.arange(2.30,2.55,.005)[:len(D)]): print(f'{t:.3f} {D[i]:6.1f} {W[i]:6.1f} {M[i]:6.1f}')

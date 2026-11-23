# per-add() tagging by call order; hilbert envelope (>150 Hz and full band) of each part and of the final mix around 2.2-2.6 s
import numpy as np, sys
from scipy.signal import hilbert, butter, sosfiltfilt
src=open('../../source/anim/sfx33.py').read()
src=src.replace("def add(sig,start,pan=0.0,gain=1.0):","PARTS=[]\ndef add(sig,start,pan=0.0,gain=1.0):\n    i0=int(round(start*SR)); s2=sig[:max(0,N-i0)]*gain; c=np.zeros(N); c[i0:i0+len(s2)]+=s2; PARTS.append((start,c))")
src=src.replace("for it in range(12):","PRE=st.copy()\nfor it in range(12):")
src=src.replace("w=wave.open(OUT,'wb')","raise SystemExit")
sys.argv=['x','/tmp/probe33b.wav']; g={}
try: exec(compile(src,'p','exec'),g)
except SystemExit: pass
SR=g['SR']; P=g['PARTS']; st=g['st']; PRE=g['PRE']; k=np.sqrt((st**2).sum()/(PRE**2).sum())
names=['tick','click','click-body','release','glide','swell','thump-sine','thump-noise','thump-air']+[f'resolve{i}' for i in range(4)]
hp=butter(4,150,'highpass',fs=SR,output='sos')
def envdb(x,a,b,hpf=False):
    y=sosfiltfilt(hp,x) if hpf else x
    e=np.abs(hilbert(y[int(a*SR)-4800:int(b*SR)+4800]))[4800:-4800]
    w=int(.005*SR); e=e[:len(e)//w*w].reshape(-1,w).mean(1); return 20*np.log10(e+1e-9)
ts=np.arange(2.30,2.55,.005)
mix=st.mean(1)
# compare to delivered wav
import subprocess
raw=subprocess.run(['ffmpeg','-v','error','-i','../../deliverables/xijiwang-logo-v3.3-sfx.wav','-f','f32le','-'],capture_output=True).stdout
d=np.frombuffer(raw,np.float32).reshape(-1,2)
print('probe vs delivered WAV max abs diff:',float(np.abs(d[:len(st)]-st[:len(d)]).max()))
rows={'MIX full':envdb(mix,2.30,2.55),'MIX >150Hz':envdb(mix,2.30,2.55,True)}
for (s,c),n in zip(P,names):
    if 2.0<s<2.5: rows[n+' full']=envdb(c*k,2.30,2.55); rows[n+' >150']=envdb(c*k,2.30,2.55,True)
print('t(s)   '+'  '.join(f'{n[:14]:>14}' for n in rows))
for i,t in enumerate(ts[:len(rows['MIX full'])]):
    print(f'{t:.3f} '+'  '.join(f'{rows[n][i]:14.1f}' for n in rows))

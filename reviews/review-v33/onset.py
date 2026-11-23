# short-time energy + spectral-flux onsets for a wav or the audio track of an mp4
import sys,subprocess,numpy as np
from scipy.signal import stft
f=sys.argv[1]; SR=48000
raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-map','0:a','-f','f32le','-ac','2','-ar',str(SR),'-'],capture_output=True).stdout
x=np.frombuffer(raw,np.float32).reshape(-1,2).mean(1)
hop=int(.0025*SR); win=int(.010*SR)
e=np.array([np.sum(x[i:i+win]**2) for i in range(0,len(x)-win,hop)]); edb=10*np.log10(e/win+1e-12)
fr,t,Z=stft(x,SR,nperseg=1024,noverlap=1024-hop)
M=np.log1p(np.abs(Z)*100); flux=np.maximum(0,np.diff(M,axis=1)).sum(0); tf=t[1:]
# band flux (>2k) to catch clicks
hb=fr>2000; fluxh=np.maximum(0,np.diff(M[hb],axis=1)).sum(0)
def peaks(v,tt,thr,mind=.04):
    out=[];last=-1
    for i in range(1,len(v)-1):
        if v[i]>thr and v[i]>=v[i-1] and v[i]>=v[i+1] and tt[i]-last>mind: out.append((round(tt[i],4),round(float(v[i]),1))); last=tt[i]
    return out
med=np.median(flux); print('flux onsets (>6x median):',peaks(flux,tf,6*med))
medh=np.median(fluxh); print('HF flux onsets (>6x median):',peaks(fluxh,tf,6*medh))
te=np.arange(len(edb))*hop/SR+win/2/SR
print('energy dB 2.15-2.60 (2.5ms hop):')
for i in range(len(te)):
    if 2.15<=te[i]<=2.6: print(f'  {te[i]:.4f} {edb[i]:6.1f}  flux {flux[min(i,len(flux)-1)]:.1f}')

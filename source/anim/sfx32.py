# v3.2 sound: tick -> click -> glide -> swell -> thump -> resolve. Every cue tied to a visual time (s).
import numpy as np, wave, sys
import pyloudnorm as pyln
from scipy.signal import resample_poly, lfilter, butter, sosfilt
from scipy.ndimage import minimum_filter1d
SR=48000; DUR=float(sys.argv[2]) if len(sys.argv)>2 else 7.5; N=int(SR*DUR)
OUT=sys.argv[1] if len(sys.argv)>1 else 'sfx32.wav'
T=dict(tick=0.20, click=1.41, glide=1.45, glide_end=1.95, swell=1.75, thump=2.38, resolve=3.85)
L=np.zeros(N); R=np.zeros(N); rng=np.random.default_rng(32)
def t_(d): return np.arange(int(SR*d))/SR
def add(sig,start,pan=0.0,gain=1.0):
    i=int(round(start*SR)); sig=sig[:max(0,N-i)]*gain
    L[i:i+len(sig)]+=sig*np.cos((pan+1)*np.pi/4)*2**.5; R[i:i+len(sig)]+=sig*np.sin((pan+1)*np.pi/4)*2**.5
def bpf(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],'bandpass',fs=SR,output='sos'),x)
def lpf(x,fc,o=2): return sosfilt(butter(o,fc,'lowpass',fs=SR,output='sos'),x)
def env(n,a,d): t=np.arange(n)/SR; return np.minimum(t/a,1)*np.exp(-np.maximum(t-a,0)/d)
def bell(f,d,dec,bright=1.):
    t=t_(d); s=sum(g*np.sin(2*np.pi*f*m*t)*np.exp(-t*k/dec) for m,g,k in [(1,1,1),(2.0,.3*bright,1.7),(3.0,.12*bright,2.6)])
    return s*np.minimum(t/.006,1)

# 0 TICK — soft, ~-18 dB under the click: the button fades in (btnIn starts 0.20s) while the ring draws
t=t_(.035); tk=bpf(rng.standard_normal(len(t)),3500,10000)*np.exp(-t*200)+.35*np.sin(2*np.pi*2600*t)*np.exp(-t*260)
add(tk*np.minimum(t/.0015,1),T['tick'],-.1,.07)

# 1 CLICK — at the visual press bottom (press 40% = 1.408s, tap 45% = 1.417s)
t=t_(.05); down=bpf(rng.standard_normal(len(t)),2500,9000)*np.exp(-t*260)+.5*np.sin(2*np.pi*1900*t)*np.exp(-t*320)
add(down,T['click'],.1,.55)
t=t_(.25); add(np.sin(2*np.pi*(95+50*np.exp(-t*40))*t)*env(len(t),.002,.05),T['click'],0,.30)   # body of the press
t=t_(.04); add(bpf(rng.standard_normal(len(t)),3000,9000)*np.exp(-t*300),T['click']+.11,.1,.18)  # release (press returns)

# 2 GLIDE — bars morph to play, 1.45–1.95 (emphasized curve: fast start, long settle)
d=.62; t=t_(d); p=1-(1-np.minimum(t/.5,1))**3
f=392*2**(p*7/12); ph=2*np.pi*np.cumsum(f)/SR
g=(np.sin(ph)+.18*np.sin(2*ph))*env(len(t),.012,.18)
add(g,T['glide'],0,.20)

# 3 SWELL — morph settles, camera pull-back + button shrinks to the nose, 1.75 -> crest exactly at thump
d=T['thump']-T['swell']; t=t_(d); x=t/d
n=rng.standard_normal(len(t)); sw=np.zeros_like(t)
for k,(lo,hi) in enumerate([(300,900),(700,2000),(1500,4500)]):   # spectral rise
    sw+=bpf(n,lo,hi)*np.clip(x*3-k,0,1)
sw*=x**2.2
tone=sum(np.sin(2*np.pi*f*t)*.12 for f in [196,293.66,392])*x**2.5
add(lpf(sw,6000)*.9+tone,T['swell'],-.15,.45)

# 4 THUMP — lion first visibly blooms past the nose (reveal starts 2.37 at r=20, expo; first visible fill frame f143 = 2.383)
t=t_(1.2); th=np.sin(2*np.pi*(46+34*np.exp(-t*16))*t)*env(len(t),.004,.32)
add(th,T['thump'],0,.75)
t=t_(.12); add(lpf(rng.standard_normal(len(t)),700)*env(len(t),.002,.03),T['thump'],0,.5)
t=t_(1.0); add(lpf(bpf(rng.standard_normal(len(t)),200,3000),2500)*env(len(t),.01,.25),T['thump'],.2,.10)  # air tail

# 5 RESOLVE — wordmark arrives (zh rise starts 3.80, mostly up by ~3.9), long tail through the hold
t=t_(3.6); pad=np.zeros_like(t)
for f in [130.81,196.0,261.63,329.63,392.0]:
    for det in (-.5,.5): pad+=np.sin(2*np.pi*(f+det)*t+rng.random()*6)*(.55 if f<300 else .32)
pad=lpf(pad,1600)*np.minimum(t/.25,1)*np.exp(-np.maximum(t-.5,0)/1.1)
add(pad,T['resolve'],0,.12)
for f,pn in [(523.25,-.2),(783.99,.2),(1046.5,0)]: add(bell(f,3.3,1.1,.7),T['resolve']+.02,pn,.20)

# space: short plate
ir_t=t_(1.6)
def verb(x):
    ir=rng.standard_normal(len(ir_t))*np.exp(-ir_t*3.6); ir=lpf(ir,5500); ir/=np.sqrt((ir**2).sum())*6
    return np.fft.irfft(np.fft.rfft(x,len(x)+len(ir))*np.fft.rfft(ir,len(x)+len(ir)))[:len(x)]
st=np.stack([L+.6*verb(L),R+.6*verb(R)],1)
st=sosfilt(butter(2,30,'highpass',fs=SR,output='sos'),st,axis=0)
fade=np.ones(N); fade[-int(.6*SR):]=np.linspace(1,0,int(.6*SR))**2; st*=fade[:,None]

# loudness: -16 LUFS integrated, true peak <= -2.0 dBTP (margin for AAC), lookahead limiter on 4x-oversampled peak
meter=pyln.Meter(SR); TARGET=-15.985; TP=10**(-2.0/20)   # TARGET: set so ffmpeg ebur128 reads -16.0 on both the WAV and the AAC in the MP4s
def tp(x): return np.abs(resample_poly(x,4,1,axis=0)).max()
for it in range(12):
    st*=10**((TARGET-meter.integrated_loudness(st))/20)
    pk=tp(st)
    if pk<=TP and abs(meter.integrated_loudness(st)-TARGET)<0.02: break   # v3.2: also require I on target (gating is non-linear)
    os_=np.abs(resample_poly(st,4,1,axis=0)).max(1)
    gr=np.minimum(1,TP*0.97/np.maximum(os_,1e-9)).reshape(-1,4).min(1)
    gr=minimum_filter1d(gr,int(.003*SR))                       # 3 ms lookahead/hold
    a=np.exp(-1/(.06*SR)); gr=np.minimum(gr,lfilter([1-a],[1,-a],gr,zi=[gr[0]*a])[0])  # 60 ms release
    gr=np.convolve(gr,np.ones(int(.001*SR))/int(.001*SR),'same')
    st*=gr[:,None]
I=meter.integrated_loudness(st); print(f'{OUT}: I={I:.2f} LUFS, TP~{20*np.log10(tp(st)):.2f} dBTP, iters={it+1}')
w=wave.open(OUT,'wb'); w.setnchannels(2); w.setsampwidth(3); w.setframerate(SR)
q=np.clip(np.round(st*8388607),-8388608,8388607).astype('<i4')
w.writeframes(np.ascontiguousarray(q.reshape(-1).astype('<i4')).view(np.uint8).reshape(-1,4)[:,:3].tobytes()); w.close()

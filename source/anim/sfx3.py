import numpy as np, wave
SR=48000; DUR=7.5; N=int(SR*DUR)
L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(7)
def t_(d): return np.arange(int(SR*d))/SR
def add(sig,start,pan=0.0,gain=1.0):
    i=int(start*SR); sig=sig[:max(0,N-i)]*gain
    l=np.cos((pan+1)*np.pi/4); r=np.sin((pan+1)*np.pi/4)
    L[i:i+len(sig)]+=sig*l*1.414/2*2**.5; R[i:i+len(sig)]+=sig*r*1.414/2*2**.5
def lp(x,fc):  # one-pole lowpass, fc may be array
    fc=np.broadcast_to(fc,x.shape); a=np.exp(-2*np.pi*fc/SR); y=np.zeros_like(x); s=0.
    for k in range(len(x)): s=(1-a[k])*x[k]+a[k]*s; y[k]=s
    return y
def bp(x,fc): return lp(x,fc)-lp(lp(x,fc*0.5),fc*0.5)
def env(n,a,d):  # attack, exp decay
    t=np.arange(n)/SR; return np.minimum(t/a,1)*np.exp(-np.maximum(t-a,0)/d)
def bell(f,d=1.2,dec=.5,bright=1.):
    t=t_(d); s=np.zeros_like(t)
    for m,g,k in [(1,1,1),(2.0,.35*bright,1.6),(3.01,.18*bright,2.4),(4.2,.08*bright,3.5)]:
        s+=g*np.sin(2*np.pi*f*m*t)*np.exp(-t*k/dec)
    return s*np.minimum(t/.004,1)

# 0 ring appears: soft sine "ui on" tone
t=t_(1.0); add((np.sin(2*np.pi*660*t)+.3*np.sin(2*np.pi*990*t))*env(len(t),.02,.25),0.05,0,.12)
add(bp(rng.standard_normal(len(t_(.9))),2500)*np.sin(np.pi*t_(.9)/.9)**2,0.0,.2,.12)
# cursor glide: faint air
d=.7; t=t_(d); add(bp(rng.standard_normal(len(t)),3500)*np.sin(np.pi*t/d)**2,0.6,.5,.10)
# click: crisp two-part mouse click
t=t_(.06); clk=bp(rng.standard_normal(len(t)),5000)*np.exp(-t*220)+np.sin(2*np.pi*2200*t)*np.exp(-t*300)*.6
add(clk,1.33,.15,.9); add(clk*.5,1.43,.15,.6)
t=t_(.3); add(np.sin(2*np.pi*(90+60*np.exp(-t*30))*t)*env(len(t),.003,.06),1.33,0,.35)
# morph pause->play: rising glassy glide
d=.55; t=t_(d); f=520*2**(np.minimum(t/.45,1)*0.583)  # up a fifth-ish
ph=2*np.pi*np.cumsum(f)/SR; add((np.sin(ph)+.25*np.sin(2*ph))*env(len(t),.01,.25),1.45,0,.22)
# shrink to nose + ring expansion: soft reverse-swell into outline draw
d=1.3; t=t_(d); n=rng.standard_normal(len(t))
sw=bp(n,500+2800*(t/d)**1.5)*np.sin(np.pi*np.minimum(t/d,1)*.95)**2
add(sw,1.95,-.3,.5)
shim=sum(np.sin(2*np.pi*f*t+rng.random()*6)*.02 for f in [1760,2217,2637,3520])*(t/d)**2
add(shim*np.exp(-np.maximum(t-1.15,0)*8),1.95,.3,1)
# nose lands: tiny pluck
add(bell(1046.5,.8,.15,.5),2.6,0,.25)
# fill bloom
t=t_(1.4); thump=(np.sin(2*np.pi*(52+40*np.exp(-t*18))*t)*env(len(t),.008,.35))
add(thump,2.85,0,.45); add(lp(rng.standard_normal(len(t)),900)*env(len(t),.005,.08),2.85,0,.5)
# eyes / mouth plucks
add(bell(1318.5,1.0,.18,.6),3.1,-.3,.3); add(bell(1661.2,1.0,.18,.6),3.22,.3,.28); add(bell(1975.5,1.0,.18,.6),3.3,0,.28)
# slide whoosh 3.5-4.7 panned R->L
d=1.2; t=t_(d); x=t/d
wh=bp(rng.standard_normal(len(t)),400+1800*np.sin(np.pi*x))*np.sin(np.pi*x)**1.8*.5
i0=int(3.5*SR); pan=np.linspace(.4,-.5,len(wh)); L[i0:i0+len(wh)]+=wh*np.cos((pan+1)*np.pi/4); R[i0:i0+len(wh)]+=wh*np.sin((pan+1)*np.pi/4)
# zh ticks
for i in range(5):
    t=t_(.25); tk=np.sin(2*np.pi*(880+i*55)*t)*np.exp(-t*45)+.4*bp(rng.standard_normal(len(t)),3000)*np.exp(-t*80)
    add(tk,4.05+i*.065+.12,-.3+i*.15,.18)
# en sparkles
for i in range(13): add(bell(3500+i*90,.4,.06,.2),4.45+i*.028+.1,-.6+i*.1,.035)
# resolve chord + bell sting
t=t_(3.0); pad=np.zeros_like(t)
for f in [130.81,196.0,246.94,329.63,587.33]:
    for det in (-.6,.6): pad+=np.sin(2*np.pi*(f+det)*t+rng.random()*6)*(.6 if f<300 else .35)
pad=lp(pad,1800)*np.minimum(t/.35,1)*np.exp(-np.maximum(t-.6,0)/1.0)
add(pad,4.8,0,.13)
for f,p in [(523.25,-.2),(783.99,.2),(1046.5,0)]: add(bell(f,2.7,1.0,.8),4.83,p,.26)
t=t_(1.4); add(bp(rng.standard_normal(len(t)),6000)*np.sin(np.pi*t/1.4)**2,5.2,-.4,.12)
# blink pop
t=t_(.12); add(np.sin(2*np.pi*(1200-600*t/.12)*t)*np.exp(-t*60),6.0,0,.12)
# reverb
ir_t=t_(1.8); 
def verb(x):
    ir=rng.standard_normal(len(ir_t))*np.exp(-ir_t*3.2); ir=lp(ir,5000); ir/=np.abs(ir).sum()/6
    return np.fft.irfft(np.fft.rfft(x,len(x)+len(ir))*np.fft.rfft(ir,len(x)+len(ir)))[:len(x)]
L2=L+.35*verb(L); R2=R+.35*verb(R)
st=np.stack([L2,R2],1); st=np.tanh(st*1.1)/np.tanh(1.1)
fade=np.ones(N); fade[-int(.4*SR):]=np.linspace(1,0,int(.4*SR)); st*=fade[:,None]
st*=0.89/np.abs(st).max()  # ~-1 dBFS peak
w=wave.open('sfx3.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st*32767).astype('<i2').tobytes()); w.close(); print('ok')

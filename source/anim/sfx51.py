import numpy as np, wave, sys
SR=48000
def make(DUR, demo, out):
    N=int(SR*DUR); L=np.zeros(N); R=np.zeros(N); rng=np.random.default_rng(11)
    T=lambda d: np.arange(int(SR*d))/SR
    def add(sig,st,pan=0.,g=1.):
        i=int(st*SR); sig=sig[:max(0,N-i)]*g
        L[i:i+len(sig)]+=sig*np.cos((pan+1)*np.pi/4)*1.414; R[i:i+len(sig)]+=sig*np.sin((pan+1)*np.pi/4)*1.414
    def lp(x,fc):
        fc=np.broadcast_to(fc,x.shape); a=np.exp(-2*np.pi*fc/SR); y=np.zeros_like(x); s=0.
        for k in range(len(x)): s=(1-a[k])*x[k]+a[k]*s; y[k]=s
        return y
    def bp(x,fc): return lp(x,fc)-lp(lp(x,fc*.5),fc*.5)
    def env(n,a,d): t=np.arange(n)/SR; return np.minimum(t/a,1)*np.exp(-np.maximum(t-a,0)/d)
    def bell(f,d=1.,dec=.3,br=.6):
        t=T(d); s=sum(g*np.sin(2*np.pi*f*m*t)*np.exp(-t*k/dec) for m,g,k in [(1,1,1),(2,.3*br,1.6),(3.01,.15*br,2.4),(4.2,.07*br,3.5)])
        return s*np.minimum(t/.004,1)
    def tick(f=3200,g=1.):  # small mechanical tick
        t=T(.05); return (bp(rng.standard_normal(len(t)),f)*np.exp(-t*260)+.5*np.sin(2*np.pi*f*.6*t)*np.exp(-t*200))*g
    def ratchet(st,dur,rate,f0,f1,g,pan=0):
        n=int(dur*rate)
        for j in range(n): add(tick(f0+(f1-f0)*j/max(n-1,1)),st+j/rate,pan+.3*np.sin(j),g*(1-.5*j/n))
    def swoosh(st,d,f0,f1,g,pan=0,pw=2):
        t=T(d); x=t/d; add(bp(rng.standard_normal(len(t)),f0+(f1-f0)*x)*np.sin(np.pi*x)**pw,st,pan,g)
    def click(st,g=1.):
        t=T(.06); c=bp(rng.standard_normal(len(t)),5000)*np.exp(-t*220)+.6*np.sin(2*np.pi*2200*t)*np.exp(-t*300)
        add(c,st,.15,.8*g); add(c*.5,st+.09,.15,.5*g)
        t=T(.25); add(np.sin(2*np.pi*(95+60*np.exp(-t*30))*t)*env(len(t),.003,.05),st,0,.3*g)
    def glide(st,f0,f1,g):
        d=.45; t=T(d); f=f0*(f1/f0)**np.minimum(t/.3,1); ph=2*np.pi*np.cumsum(f)/SR
        add((np.sin(ph)+.25*np.sin(2*ph))*env(len(t),.01,.2),st,0,g)
    # ---- intro v5 ----
    t=T(.6); add((np.sin(2*np.pi*110*t)*.8+np.sin(2*np.pi*220*t)*.2)*np.sin(np.pi*np.minimum(t/.55,1))**2,0.0,0,.2)
    for i,(tt,f,p) in enumerate([(.5,196.0,-.5),(.62,261.63,0),(.74,329.63,.5)]):   # X J W 浮现：木质轻敲 + 音高
        tk=T(.25); add(bp(rng.standard_normal(len(tk)),900)*np.exp(-tk*45),tt,p,.35); add(bell(f*2,1.2,.35,.4),tt+.01,p,.16)
    for tt,f0,f1,p in [(1.62,800,2600,-.4),(1.45,600,1800,0),(1.55,500,1500,.4)]:   # 形变滑行 X/J/W
        swoosh(tt-.05,.95,f0,f1,.35,p,1)
    for tt,f,p in [(2.35,1046.5,0),(2.45,1318.5,.2),(2.57,1567.98,.3)]: add(bell(f,1,.2),tt,p,.16)   # 五官落定 J/W/X
    add(bell(1046.5,1.2,.25),2.15,0,.26); t=T(.6); add(np.sin(2*np.pi*(70+30*np.exp(-t*20))*t)*env(len(t),.004,.2),2.15,0,.22)  # ▶ 弹出
    click(2.85,.6)                                                                     # ▶ 落位
    for k in range(14): add(tick(2400+k*110),2.60+k*.03,-.8+k*.12,.28)                 # 鬃毛依次弹开
    d=.8; t=T(d); x=t/d; wh=bp(rng.standard_normal(len(t)),400+1800*np.sin(np.pi*x))*np.sin(np.pi*x)**1.8*.4
    i0=int(2.75*SR); pan=np.linspace(.4,-.5,len(wh)); L[i0:i0+len(wh)]+=wh*np.cos((pan+1)*np.pi/4)*1.41; R[i0:i0+len(wh)]+=wh*np.sin((pan+1)*np.pi/4)*1.41
    for i in range(5): swoosh(3.4+i*.065+.04,.18,2500,5500,.12,-.3+i*.15)
    swoosh(3.92,.55,3000,7000,.16,0)
    for i in range(13): add(bell(3600+i*80,.35,.05,.2),4.02+i*.012,-.6+i*.1,.03)
    t=T(3.0); pad=np.zeros_like(t)
    for f in [130.81,196.0,246.94,329.63,587.33]:
        for det in (-.6,.6): pad+=np.sin(2*np.pi*(f+det)*t+rng.random()*6)*(.6 if f<300 else .35)
    pad=lp(pad,1800)*np.minimum(t/.25,1)*np.exp(-np.maximum(t-.5,0)/.9); add(pad,4.4,0,.12)
    for f,p in [(523.25,-.2),(783.99,.2),(1046.5,0)]: add(bell(f,2.5,.9,.8),4.45,p,.24)
    swoosh(4.45,.45,5000,9000,.12,-.4)
    t=T(.5); add(np.sin(2*np.pi*(55+20*np.exp(-t*15))*t)*env(len(t),.01,.15),4.55,0,.3)
    if demo:
        swoosh(5.4,.7,3000,4500,.06,.5)
        bed=lp(rng.standard_normal(N),500); bed*=0.004/np.sqrt(np.mean(bed**2)); i0=int(4.6*SR); ramp=np.minimum(np.arange(N-i0)/SR/1.5,1)
        L[i0:]+=bed[i0:]*ramp; R[i0:]+=np.roll(bed,999)[i0:]*ramp
        for i,tt in enumerate([6.5,8.7,10.7,12.7]):
            pause = i%2==0
            click(tt-.005)
            if pause: glide(tt,783.99,523.25,.2); swoosh(tt,.5,2500,800,.2)
            else:     glide(tt,523.25,783.99,.2); swoosh(tt,.5,800,2800,.2)
            add(bell(1046.5 if not pause else 659.25,1,.25),tt+.12,0,.12)
    # reverb + master
    irt=T(1.6)
    def verb(x):
        ir=rng.standard_normal(len(irt))*np.exp(-irt*3.4); ir=lp(ir,5000); ir/=np.abs(ir).sum()/6
        n=len(x)+len(ir); return np.fft.irfft(np.fft.rfft(x,n)*np.fft.rfft(ir,n))[:len(x)]
    st=np.stack([L+.3*verb(L),R+.3*verb(R)],1); st=np.tanh(st*1.1)/np.tanh(1.1)
    fade=np.ones(N); fade[-int(.35*SR):]=np.linspace(1,0,int(.35*SR)); st*=fade[:,None]; st*=.89/np.abs(st).max()
    w=wave.open(out,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype('<i2').tobytes()); w.close()
make(5.6,False,'sfx51-intro.wav'); make(14.2,True,'sfx51-demo.wav'); print('ok')

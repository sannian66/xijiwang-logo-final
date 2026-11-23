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
    def swoosh(st,d,f0,f1,g,pan=0):
        t=T(d); x=t/d; add(bp(rng.standard_normal(len(t)),f0+(f1-f0)*x)*np.sin(np.pi*x)**2,st,pan,g)
    def click(st,g=1.):
        t=T(.06); c=bp(rng.standard_normal(len(t)),5000)*np.exp(-t*220)+.6*np.sin(2*np.pi*2200*t)*np.exp(-t*300)
        add(c,st,.15,.8*g); add(c*.5,st+.09,.15,.5*g)
        t=T(.25); add(np.sin(2*np.pi*(95+60*np.exp(-t*30))*t)*env(len(t),.003,.05),st,0,.3*g)
    def glide(st,f0,f1,g):
        d=.45; t=T(d); f=f0*(f1/f0)**np.minimum(t/.3,1); ph=2*np.pi*np.cumsum(f)/SR
        add((np.sin(ph)+.25*np.sin(2*ph))*env(len(t),.01,.2),st,0,g)
    # ---- intro ----
    t=T(.5); add(np.sin(2*np.pi*110*t)*np.sin(np.pi*np.minimum(t/.45,1))**2*.8+np.sin(2*np.pi*220*t)*np.sin(np.pi*np.minimum(t/.45,1))**2*.2,0.05,0,.25)
    swoosh(.4,.8,500,2600,.45,-.2)
    for k in range(8): add(tick(2600+k*120,1),.42+k*.012+.5,-.7+k*.2,.3)
    swoosh(1.08,.6,3000,900,.35,.2); ratchet(1.1,.45,34,4200,2600,.22)
    t=T(.12); add(bp(rng.standard_normal(len(t)),1800)*np.exp(-t*60),1.2,0,.5)   # iris settle "chk"
    t=T(.8); add(np.sin(2*np.pi*(60+30*np.exp(-t*20))*t)*env(len(t),.005,.25),1.4,0,.4)
    add(bell(1046.5,1,.2),1.39,0,.3); add(bell(1318.5,1,.18),1.57,-.3,.26); add(bell(1567.98,1,.18),1.63,.3,.26)
    glide(1.75,1567.98,2093,.14)
    d=.8; t=T(d); x=t/d; wh=bp(rng.standard_normal(len(t)),400+1800*np.sin(np.pi*x))*np.sin(np.pi*x)**1.8*.45
    i0=int(2.2*SR); pan=np.linspace(.4,-.5,len(wh)); L[i0:i0+len(wh)]+=wh*np.cos((pan+1)*np.pi/4)*1.41; R[i0:i0+len(wh)]+=wh*np.sin((pan+1)*np.pi/4)*1.41
    for i in range(5): swoosh(2.58+i*.06+.05,.18,2500,5500,.12,-.3+i*.15)
    swoosh(3.0,.6,3000,7000,.16,0)
    for i in range(13): add(bell(3600+i*80,.35,.05,.2),3.02+i*.02,-.6+i*.1,.03)
    t=T(.12); add(np.sin(2*np.pi*1500*t)*np.exp(-t*40),3.45,.3,.12)
    t=T(3.0); pad=np.zeros_like(t)
    for f in [130.81,196.0,246.94,329.63,587.33]:
        for det in (-.6,.6): pad+=np.sin(2*np.pi*(f+det)*t+rng.random()*6)*(.6 if f<300 else .35)
    pad=lp(pad,1800)*np.minimum(t/.25,1)*np.exp(-np.maximum(t-.5,0)/.9); add(pad,3.5,0,.12)
    for f,p in [(523.25,-.2),(783.99,.2),(1046.5,0)]: add(bell(f,2.5,.9,.8),3.55,p,.24)
    swoosh(3.6,.4,5000,9000,.12,-.4)
    t=T(.5); add(np.sin(2*np.pi*(55+20*np.exp(-t*15))*t)*env(len(t),.01,.15),3.65,0,.3)
    if demo:
        swoosh(5.0,.7,3000,4500,.06,.5)
        for i,tt in enumerate([6.0,8.2,10.2,12.2]):
            pause = i%2==0
            click(tt)
            if pause: glide(tt,783.99,523.25,.2); ratchet(tt+.06,.4,30,3000,2200,.16); swoosh(tt,.5,2500,800,.2)
            else:     glide(tt,523.25,783.99,.2); ratchet(tt+.06,.4,30,2200,3600,.16); swoosh(tt,.5,800,2800,.2)
            add(bell(1046.5 if not pause else 659.25,1,.25),tt+.12,0,.12)
    # reverb + master
    irt=T(1.6)
    def verb(x):
        ir=rng.standard_normal(len(irt))*np.exp(-irt*3.4); ir=lp(ir,5000); ir/=np.abs(ir).sum()/6
        n=len(x)+len(ir); return np.fft.irfft(np.fft.rfft(x,n)*np.fft.rfft(ir,n))[:len(x)]
    st=np.stack([L+.3*verb(L),R+.3*verb(R)],1); st=np.tanh(st*1.1)/np.tanh(1.1)
    fade=np.ones(N); fade[-int(.35*SR):]=np.linspace(1,0,int(.35*SR)); st*=fade[:,None]; st*=.89/np.abs(st).max()
    w=wave.open(out,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype('<i2').tobytes()); w.close()
make(4.6,False,'sfx42-intro.wav'); make(13.6,True,'sfx42-demo.wav'); print('ok')

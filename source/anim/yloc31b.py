import subprocess, sys, numpy as np
W,H=2560,1440; fs=W*H*3//2; f=sys.argv[1]; lo_t=int(sys.argv[2]); hi_t=int(sys.argv[3])
p=subprocess.Popen(['ffmpeg','-v','error','-i',f,'-f','rawvideo','-pix_fmt','yuv420p','-'],stdout=subprocess.PIPE); n=0; out=[]
while True:
    b=p.stdout.read(fs)
    if len(b)<fs: break
    y=np.frombuffer(b,np.uint8)[:W*H].reshape(H,W); m=(y<lo_t)|(y>hi_t)
    if m.any(): ys,xs=np.nonzero(m); out.append((n,int(m.sum()),int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max()),int(y.min()),int(y.max())))
    n+=1
print(f, len(out),'frames'); [print(o) for o in out[:40]]

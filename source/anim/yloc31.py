import subprocess, sys, numpy as np
W,H=2560,1440; fs=W*H*3//2; f=sys.argv[1]
p=subprocess.Popen(['ffmpeg','-v','error','-i',f,'-f','rawvideo','-pix_fmt','yuv420p','-'],stdout=subprocess.PIPE); n=0; bad=[]
while True:
    b=p.stdout.read(fs)
    if len(b)<fs: break
    y=np.frombuffer(b,np.uint8)[:W*H].reshape(H,W)
    lo=(y<16).sum(); hi=(y>235).sum()
    if lo or hi:
        ys,xs=np.nonzero((y<16)|(y>235)); bad.append((n,int(lo),int(hi),int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max()),int(y.min()),int(y.max())))
    n+=1
print(len(bad),'frames with out-of-range'); [print(b) for b in bad[:: max(1,len(bad)//25)]]

import subprocess, sys, numpy as np
W,H=2560,1440; fs=W*H*3//2
for f in sys.argv[1:]:
    p=subprocess.Popen(['ffmpeg','-v','error','-i',f,'-f','rawvideo','-pix_fmt','yuv420p','-'],stdout=subprocess.PIPE)
    mn,mx=255,0; n=0; first=last=None
    while True:
        b=p.stdout.read(fs)
        if len(b)<fs: break
        y=np.frombuffer(b,np.uint8)[:W*H]; mn=min(mn,int(y.min())); mx=max(mx,int(y.max())); n+=1
        if first is None: first=int(y[5*W+5])
        last=int(y[5*W+5])
    r=subprocess.run(['ffmpeg','-v','error','-i',f,'-vf','select=eq(n\\,0)','-frames:v','1','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True).stdout
    rgb=np.frombuffer(r,np.uint8).reshape(H,W,3)[5,5].tolist()
    print(f"{f}: frames={n} Y min={mn} max={mx} bgY first={first} last={last} decoded RGB bg={rgb}")

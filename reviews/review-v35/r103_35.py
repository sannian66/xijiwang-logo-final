# EBU R103-style check on the decoded Y plane: share of samples outside 16-235 and outside the 5-246 tolerance band
import subprocess,sys,numpy as np
n=2560*1440; fs=n*3//2
p=subprocess.Popen(['ffmpeg','-v','error','-i',sys.argv[1],'-map','0:v','-f','rawvideo','-pix_fmt','yuv420p','-'],stdout=subprocess.PIPE)
a=[];b=[]
while True:
    buf=p.stdout.read(fs)
    if len(buf)<fs: break
    y=np.frombuffer(buf[:n],np.uint8); a.append(((y<16)|(y>235)).mean()); b.append(((y<5)|(y>246)).mean())
a=np.array(a);b=np.array(b)
print(sys.argv[1].split('/')[-1], f'outside16-235: max {100*a.max():.3f}% mean {100*a.mean():.3f}% | outside5-246: max {100*b.max():.4f}% frames>0 {(b>0).sum()}')

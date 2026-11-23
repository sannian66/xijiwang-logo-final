import subprocess,sys,numpy as np
n=1440*2560
raw=subprocess.run(['ffmpeg','-v','error','-i',sys.argv[1],'-f','rawvideo','-pix_fmt','yuv420p','-'],capture_output=True).stdout
y=np.frombuffer(raw,np.uint8).reshape(-1,n*3//2)[:,:n]
o=((y<16)|(y>235)).mean(1); print(f'{sys.argv[1]:24s} out-of-range max {100*o.max():.4f}%  Ymin {y.min()} Ymax {y.max()}')

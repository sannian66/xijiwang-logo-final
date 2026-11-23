# per-frame share of luma samples outside 16..235 in the decoded MP4 (also vs. "edge" pixels = non-flat)
import subprocess,sys,numpy as np,json
f=sys.argv[1]; W,H=2560,1440; n=W*H
p=subprocess.Popen(['ffmpeg','-v','error','-i',f,'-map','0:v','-f','rawvideo','-pix_fmt','yuv420p','-'],stdout=subprocess.PIPE)
fs=n*3//2; rows=[]
i=0
while True:
    b=p.stdout.read(fs)
    if len(b)<fs: break
    y=np.frombuffer(b[:n],np.uint8)
    lo=(y<16).sum(); hi=(y>235).sum()
    ink=((y>40)&(y<210)).sum()  # transition/AA pixels
    rows.append((i,int(lo),int(hi),int(ink),int(y.min()),int(y.max()))); i+=1
a=np.array(rows)
out=(a[:,1]+a[:,2])
print(f, 'frames',len(a),'frames_with_out',int((out>0).sum()),
      'max_out_frac_of_frame %.4f%%'%(100*out.max()/n),'mean %.4f%%'%(100*out.mean()/n),
      'worst frame',int(a[out.argmax(),0]),'Ymin',a[:,4].min(),'Ymax',a[:,5].max())
np.savetxt(sys.argv[2],a,fmt='%d',header='frame below16 above235 aa_pixels ymin ymax')

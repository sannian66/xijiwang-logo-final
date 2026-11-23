# light/dark coverage parity on accurate_rnd decodes: light ink #202624 (L≈36) on 255; dark ink #f5f5f7 (L≈245) on 0
from PIL import Image; import numpy as np
res=[]
for f in range(0,450,3):
    l=np.asarray(Image.open(f'fl/f{f:04d}.png').convert('L'),float)[::2,::2]; d=np.asarray(Image.open(f'fd/f{f:04d}.png').convert('L'),float)[::2,::2]
    al=np.clip((255-l)/(255-36),0,1); ad=np.clip(d/245,0,1)
    diff=np.abs(al-ad); res.append((f,diff.mean(),(diff>.25).mean()))
r=np.array(res); i=r[:,1].argmax()
print('mean |alpha_l-alpha_d| max %.5f at f%d; overall mean %.5f; max share px differing >25%%: %.4f%% at f%d'%(r[i,1],r[i,0],r[:,1].mean(),100*r[:,2].max(),r[r[:,2].argmax(),0]))
for f,m,s in res:
    if 126<=f<=160: print(f'f{int(f)} mean {m:.5f} >25% {100*s:.4f}%')

# light/dark coverage parity: ink alpha from each decoded frame (light: ink #202624 on white; dark: #f5f5f7 on black)
from PIL import Image; import numpy as np
res=[]
for f in range(0,450,3):
    l=np.asarray(Image.open(f'fl/f{f:04d}.png').convert('L'),float)[::2,::2]; d=np.asarray(Image.open(f'fd/f{f:04d}.png').convert('L'),float)[::2,::2]
    al=np.clip((253-l)/(253-36),0,1); ad=np.clip(d/244,0,1)   # bg/ink levels as decoded by default swscale
    diff=np.abs(al-ad); res.append((f,diff.mean(),(diff>.25).mean()))
r=np.array(res); i=r[:,1].argmax()
print('mean |alpha_l-alpha_d| max %.5f at f%d; overall mean %.5f; max share px differing >25%%: %.5f%% at f%d'%(r[i,1],r[i,0],r[:,1].mean(),100*r[:,2].max(),r[r[:,2].argmax(),0]))

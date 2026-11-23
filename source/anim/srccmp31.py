import asyncio, sys, numpy as np
from PIL import Image
from playwright.async_api import async_playwright
svg=open('/workspace/projects/0b4d0196-ffe5-4f80-a356-b2ae9513897b/files/uploads/xijiwang-horizontal-primary-af6d799ceb5b.svg').read()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':2560,'height':1440})
    for bg,ink,name in [('#ffffff',None,'src31_light.png'),('#000000','#f5f5f7','src31_dark.png')]:
        s=svg if ink is None else svg.replace('#202624',ink)
        html=f'<html><body style="margin:0;height:100vh;background:{bg};display:grid;place-items:center"><div style="width:51vw">'+s.replace('<svg ','<svg style="width:100%;height:auto;display:block" ',1)+'</div></body></html>'
        await pg.set_content(html); await pg.screenshot(path=name)
    await b.close()
asyncio.run(m())
for src,fr in [('src31_light.png',sys.argv[1]),('src31_dark.png',sys.argv[2])]:
    a=np.array(Image.open(src).convert('RGB')).astype(int); f=np.array(Image.open(fr).convert('RGB')).astype(int)
    d=np.abs(a-f).max(2); print(fr,'vs source: max diff',d.max(),'px>0',(d>0).sum(),'px>16',(d>16).sum(),'ink sample', f[f.sum(2).argmin()//2560, f.sum(2).argmin()%2560] if 'l' in fr else '')

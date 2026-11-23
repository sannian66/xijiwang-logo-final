# final frame vs source SVG: (a) Chromium render of the delivered play.html seeked to 7.49 s (lossless), (b) decoded MP4 last frame
import asyncio, os, numpy as np
from PIL import Image
from playwright.async_api import async_playwright
svg=open('../../assets/xijiwang-horizontal-primary-af6d799ceb5b.svg').read()
html34=os.path.abspath('../../deliverables/xijiwang-logo-v3.4-play.html')
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':2560,'height':1440})
    for bg,ink,name in [('#ffffff',None,'src_light.png'),('#000000','#f5f5f7','src_dark.png')]:
        s=svg if ink is None else svg.replace('#202624',ink)
        h=f'<html><body style="margin:0;height:100vh;background:{bg};display:grid;place-items:center"><div style="width:51vw">'+s.replace('<svg ','<svg style="width:100%;height:auto;display:block" ',1)+'</div></body></html>'
        await pg.set_content(h); await pg.screenshot(path=name)
    for hv,name in [('','html_last_light.png'),('#dark','html_last_dark.png')]:
        await pg.goto('file://'+html34+hv); await pg.evaluate("document.body.classList.add('capture')"); await pg.wait_for_timeout(300)
        await pg.evaluate("seek(7483.33)"); await pg.screenshot(path=name)
    await b.close()
asyncio.run(m())
def cmp(a,b,label):
    A=np.array(Image.open(a).convert('RGB')).astype(int); B=np.array(Image.open(b).convert('RGB')).astype(int)
    d=np.abs(A-B).max(2); print(f'{label}: max {d.max()}, px>0 {(d>0).sum()}, px>8 {(d>8).sum()}, px>32 {(d>32).sum()}, mean {d.mean():.4f}')
    Image.fromarray(np.clip(d*4,0,255).astype(np.uint8)).save('diff_'+label+'.png')
cmp('src_light.png','html_last_light.png','html_vs_src_light'); cmp('src_dark.png','html_last_dark.png','html_vs_src_dark')
cmp('src_light.png','fl/f0449.png','mp4_vs_src_light'); cmp('src_dark.png','fd/f0449.png','mp4_vs_src_dark')

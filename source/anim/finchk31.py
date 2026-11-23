import asyncio, os, sys, io, numpy as np
from PIL import Image
from playwright.async_api import async_playwright
src=np.array(Image.open('src31_light.png').convert('L')).astype(int)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':2560,'height':1440})
        await pg.goto('file://'+os.path.abspath(sys.argv[1])); await pg.evaluate("document.body.classList.add('capture')"); await pg.wait_for_timeout(300)
        await pg.evaluate("seek(7483)")
        def rep(tag,im):
            d=np.abs(src-np.array(Image.open(io.BytesIO(im)).convert('L')).astype(int))
            for n,(x0,x1) in {'lion':(600,1030),'word':(1080,2000)}.items(): print(tag,n,'max',d[:,x0:x1].max(),'n>16',(d[:,x0:x1]>16).sum())
        rep('anim-end',await pg.screenshot())
        await pg.evaluate("document.querySelectorAll('.en').forEach(e=>e.style.filter='none')"); rep('no-blur-filter?',await pg.screenshot())
        await pg.evaluate("document.getAnimations().forEach(a=>a.cancel()); document.querySelectorAll('.zh,.en').forEach(e=>e.style.animation='none'); document.querySelector('#growC').setAttribute('r','128'); document.querySelector('#growC').style.animation='none';document.querySelector('#growC').style.r='128px'")
        await pg.evaluate("document.querySelectorAll('.nose,.btn,.ring,.ripple,.cursor').forEach(e=>{e.style.animation='none'}); document.querySelector('.nose').style.opacity=1; document.querySelector('.btn').style.opacity=0;document.querySelector('.ring').style.opacity=0;document.querySelector('.cursor').style.opacity=0")
        rep('no-anim',await pg.screenshot())
        await b.close()
asyncio.run(main())

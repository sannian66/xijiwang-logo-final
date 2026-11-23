import asyncio, os, io, numpy as np
from PIL import Image
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':2560,'height':1440})
        await pg.goto('file://'+os.path.abspath('v32.html')); await pg.evaluate("document.body.classList.add('capture')"); await pg.wait_for_timeout(300)
        g=lambda im: np.array(Image.open(io.BytesIO(im)).convert('L')).astype(int)
        await pg.evaluate("seek(1960)"); A=g(await pg.screenshot())
        await pg.evaluate("document.querySelector('.bnose').style.opacity=0;document.querySelector('.barL').style.opacity=1;document.querySelector('.barR').style.opacity=1"); B=g(await pg.screenshot())
        d=np.abs(A-B); print('1.95 swap halves vs whole nose: max',d.max(),'n>16',(d>16).sum(),'n>64',(d>64).sum())
        await pg.evaluate("seek(2360)"); A=g(await pg.screenshot())
        await pg.evaluate("document.querySelector('.nose').style.opacity=0;document.querySelector('.btn').style.opacity=1"); B=g(await pg.screenshot())
        d=np.abs(A-B); print('2.35 swap btn-nose vs lion nose: max',d.max(),'n>16',(d>16).sum(),'n>64',(d>64).sum())
        await b.close()
asyncio.run(main())

import asyncio, os, io, numpy as np
from PIL import Image
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':2560,'height':1440})
        errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.goto('file://'+os.path.abspath('v31.html')); await pg.evaluate("document.body.classList.add('capture')")
        await pg.wait_for_timeout(8000)
        src=np.array(Image.open('src31_light.png').convert('L')).astype(int)
        a=np.array(Image.open(io.BytesIO(await pg.screenshot())).convert('L')).astype(int); d=np.abs(a-src); print('live end vs src max',d.max(),'n>16',(d>16).sum())
        await pg.click('#replay', force=True) if False else await pg.evaluate("document.getElementById('replay').click()")
        await pg.wait_for_timeout(1000); m=np.array(Image.open(io.BytesIO(await pg.screenshot())).convert('L')); print('replay@1s ink px', (m<128).sum())
        await pg.evaluate("document.getElementById('theme').click()"); await pg.wait_for_timeout(8000)
        print('hash after toggle', await pg.evaluate("location.hash"), 'dark?', await pg.evaluate("document.body.classList.contains('dark')"))
        a=np.array(Image.open(io.BytesIO(await pg.screenshot())).convert('L')).astype(int); s2=np.array(Image.open('src31_dark.png').convert('L')).astype(int); d=np.abs(a-s2); print('live dark end vs src max',d.max(),'n>16',(d>16).sum())
        print('errors',errs); await b.close()
asyncio.run(main())

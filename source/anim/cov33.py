# coverage of lion ink (sum of ink alpha, px) per frame + per-frame delta; fragment test: every ink component inside the head must connect to mane
import asyncio, os, io, sys, numpy as np
from PIL import Image
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':2560,'height':1440})
        await pg.goto('file://'+os.path.abspath(sys.argv[3])+sys.argv[4]); await pg.evaluate("document.body.classList.add('capture')"); await pg.wait_for_timeout(300)
        prev=None
        for f in range(int(sys.argv[1]),int(sys.argv[2])):
            await pg.evaluate(f"seek({f*1000/60})")
            await pg.evaluate("document.querySelectorAll('.ui,.nose,.zh,.en,.zhAll,.enAll').forEach(e=>e.style.visibility='hidden')")
            a=np.array(Image.open(io.BytesIO(await pg.screenshot())).convert('L')).astype(float)
            await pg.evaluate("document.querySelectorAll('.ui,.nose,.zh,.en,.zhAll,.enAll').forEach(e=>e.style.visibility='')")
            ink=(255-a)/(255-32) if sys.argv[4]=='' else a/245
            c=ink.sum()
            print(f,f'{f/60:.3f}', 'cov %.0f'%c, 'd %.0f'%(c-prev) if prev is not None else '')
            prev=c
        await b.close()
asyncio.run(main())

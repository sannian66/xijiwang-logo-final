import asyncio, os, sys, numpy as np, io
from PIL import Image
from playwright.async_api import async_playwright
async def shot(pg): return np.array(Image.open(io.BytesIO(await pg.screenshot())).convert('L')).astype(int)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':2560,'height':1440})
        await pg.goto('file://'+os.path.abspath(sys.argv[1])+sys.argv[2]); await pg.evaluate("document.body.classList.add('capture')"); await pg.wait_for_timeout(300)
        for t in [float(x) for x in sys.argv[3].split(',')]:
            await pg.evaluate(f"seek({t-0.01})"); A=await shot(pg)
            await pg.evaluate(f"seek({t})"); B=await shot(pg)
            d=np.abs(A-B); print(f'swap @{t}ms diff max',d.max(),'px>8',(d>8).sum(),'px>32',(d>32).sum())
        await b.close()
asyncio.run(main())

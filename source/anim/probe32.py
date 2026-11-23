import asyncio, os, io, sys, numpy as np
from PIL import Image
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':2560,'height':1440})
        errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.goto('file://'+os.path.abspath('v32probe.html')); await pg.evaluate("document.body.classList.add('capture')"); await pg.wait_for_timeout(300)
        g=lambda im: np.array(Image.open(io.BytesIO(im)).convert('L'))<128
        for f in range(int(sys.argv[1]),int(sys.argv[2])):
            await pg.evaluate(f"seek({f*1000/60})")
            await pg.evaluate("document.querySelector('.ring').style.visibility='hidden'")
            lion=g(await pg.screenshot())
            await pg.evaluate("document.querySelector('.ring').style.visibility='';document.querySelectorAll('.reveal,.nose,.lionAll,.btn,.cursor,.ripple').forEach(e=>e.style.visibility='hidden')")
            ring=np.array(Image.open(io.BytesIO(await pg.screenshot())).convert('L'))<250
            await pg.evaluate("document.querySelectorAll('.reveal,.nose,.lionAll,.btn,.cursor,.ripple').forEach(e=>e.style.visibility='')")
            ys,xs=np.nonzero(ring); 
            # min distance from lion ink to ring
            from scipy.ndimage import distance_transform_edt
            dist=distance_transform_edt(~ring)
            md=dist[lion].min() if lion.any() else -1
            print(f, f'{f/60:.3f}s', 'ringW', (xs.max()-xs.min()+1) if len(xs) else 0, 'lionpx', lion.sum(), 'min lion->ring dist', round(float(md),1))
        print(errs); await b.close()
asyncio.run(main())

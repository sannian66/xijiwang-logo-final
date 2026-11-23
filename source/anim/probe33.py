# v3.3 probe: per frame ring diameter/opacity, ring-vs-lion overlap (any visible ink), reveal radius, lion ink coverage & fragment test
import asyncio, os, io, sys, numpy as np
from PIL import Image
from playwright.async_api import async_playwright
from scipy.ndimage import distance_transform_edt
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':2560,'height':1440})
        errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.goto('file://'+os.path.abspath(sys.argv[3])); await pg.evaluate("document.body.classList.add('capture')"); await pg.wait_for_timeout(300)
        H="document.querySelectorAll('.reveal,.nose,.lionAll,.btn,.cursor,.ripple').forEach(e=>e.style.visibility=%s)"
        g=lambda im: np.array(Image.open(io.BytesIO(im)).convert('L')).astype(int)
        for f in range(int(sys.argv[1]),int(sys.argv[2])):
            await pg.evaluate(f"seek({f*1000/60})")
            await pg.evaluate(H%"'hidden'"); ringim=g(await pg.screenshot())
            op=await pg.evaluate("getComputedStyle(document.querySelector('.ring')).opacity")
            r=await pg.evaluate("document.getElementById('growC').getAttribute('r')")
            rop=await pg.evaluate("getComputedStyle(document.querySelector('.reveal')).opacity")
            await pg.evaluate(H%"''"); await pg.evaluate("document.querySelector('.ring').style.visibility='hidden'")
            lionim=g(await pg.screenshot())
            await pg.evaluate("document.querySelector('.ring').style.visibility=''")
            await pg.evaluate(H%"'hidden'"); await pg.evaluate("document.querySelector('.ring').style.opacity=1")
            ring=g(await pg.screenshot())<200
            await pg.evaluate(H%"''")
            lion=lionim<250
            ys,xs=np.nonzero(ring); W=(xs.max()-xs.min()+1) if len(xs) else 0
            md=distance_transform_edt(~ring)[lion].min() if lion.any() and ring.any() else -1
            # visible ring darkness at lion-adjacent pixels
            print(f, f'{f/60:.3f}s', 'ringDiam', W, 'ringOp %.3f'%float(op), 'ringDarkest', 255-ringim.min(), 'lion->ring(geom) %.1f'%md, 'r', r, 'revealOp %.3f'%float(rop), 'lionInk', int((lionim<128).sum()))
        print(errs); await b.close()
asyncio.run(main())

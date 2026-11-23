import asyncio, os, sys, io, numpy as np
from PIL import Image
from playwright.async_api import async_playwright
src=np.array(Image.open(sys.argv[2]).convert('L')).astype(int)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':2560,'height':1440})
        await pg.goto('file://'+os.path.abspath(sys.argv[1])+(sys.argv[3] if len(sys.argv)>3 else '')); await pg.evaluate("document.body.classList.add('capture')"); await pg.wait_for_timeout(300)
        await pg.evaluate("seek(7483)")
        def rep(tag,im):
            d=np.abs(src-np.array(Image.open(io.BytesIO(im)).convert('L')).astype(int))
            out=[]
            for n,(x0,x1,y0,y1) in {'lion':(600,1030,0,1440),'zh':(1080,2000,0,760),'en':(1080,2000,760,1440)}.items(): out.append(f"{n} max {d[y0:y1,x0:x1].max()} n>16 {(d[y0:y1,x0:x1]>16).sum()}")
            print(tag,' | '.join(out))
        rep('as-is',await pg.screenshot())
        for js,tag in [("document.querySelectorAll('[clip-path=\"url(#zhWindow)\"]').forEach(e=>e.removeAttribute('clip-path'))",'no zh clip'),
                       ("document.getAnimations().forEach(a=>a.cancel());document.querySelector('.lockup g[transform=\"translate(138.35 146.3)\"]').style.display='none'",'all canceled')]:
            await pg.evaluate(js); rep(tag,await pg.screenshot())
        await b.close()
asyncio.run(main())

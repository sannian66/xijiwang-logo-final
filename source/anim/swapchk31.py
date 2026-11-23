import asyncio, os, sys, numpy as np, io
from PIL import Image
from playwright.async_api import async_playwright
SRC=sys.argv[1]; H=sys.argv[2]
JS_A={'1':"for(const s of ['.barL','.barR','.bnose']){const e=document.querySelector(s);e.getAnimations().forEach(a=>{a.currentTime=1950})}",}
async def shot(pg):
    return np.array(Image.open(io.BytesIO(await pg.screenshot())).convert('L')).astype(int)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':2560,'height':1440})
        await pg.goto('file://'+os.path.abspath(SRC)+H); await pg.evaluate("document.body.classList.add('capture')"); await pg.wait_for_timeout(300)
        q=lambda s:f"document.querySelector('{s}')"
        # swap 1 @1.95: bars (morph end) vs bnose, everything else frozen at 1.95
        await pg.evaluate("seek(1950)")
        await pg.evaluate(f"{q('.barL')}.style.opacity=1;{q('.barR')}.style.opacity=1;{q('.bnose')}.style.opacity=0;"+
            "for(const s of ['.barL','.barR','.bnose']) document.querySelector(s).style.animationName='none'")
        await pg.evaluate(f"{q('.barL')}.style.d=getComputedStyle({q('.barL')}).d")
        await pg.evaluate("seek(1950)")
        # set morph end shapes explicitly
        A=await shot(pg)
        await pg.evaluate(f"{q('.barL')}.style.opacity=0;{q('.barR')}.style.opacity=0;{q('.bnose')}.style.opacity=1")
        B=await shot(pg)
        d=np.abs(A-B); print('swap1 @1.95 diff max',d.max(),'px>0',(d>0).sum(),'px>8',(d>8).sum())
        await pg.reload(); await pg.evaluate("document.body.classList.add('capture')"); await pg.wait_for_timeout(300)
        await pg.evaluate("seek(2500)")
        await pg.evaluate(f"{q('.ring')}.style.display='none';{q('.btn')}.style.animationName='btnShrink';")
        await pg.evaluate("seek(2500)")
        await pg.evaluate(f"{q('.btn')}.style.opacity=1;{q('.nose')}.style.animationName='none';{q('.nose')}.style.opacity=0;{q('#growC')}.style.animationName='none'")
        A=await shot(pg)
        await pg.evaluate(f"{q('.btn')}.style.opacity=0;{q('.nose')}.style.opacity=1")
        B=await shot(pg)
        d=np.abs(A-B); print('swap2 @2.50 diff max',d.max(),'px>0',(d>0).sum(),'px>8',(d>8).sum(), 'ink px',(A<128).sum())
        await b.close()
asyncio.run(main())

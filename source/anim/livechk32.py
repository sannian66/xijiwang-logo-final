import asyncio, os, io, numpy as np
from PIL import Image
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':2560,'height':1440})
        errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('console',lambda m: errs.append('console:'+m.text) if m.type=='error' else None)
        await pg.goto('file://'+os.path.abspath('v32.html')); await pg.evaluate("document.body.classList.add('capture')")
        # sample the JS-driven d / r during live playback
        samp=[]
        for _ in range(30):
            await pg.wait_for_timeout(100)
            samp.append(await pg.evaluate("[Math.round(LIVE[0].currentTime), document.querySelector('.barL').getAttribute('d').slice(0,22), document.getElementById('growC').getAttribute('r')]"))
        print('live samples (t ms, barL d head, growC r):'); [print('  ',s) for s in samp[::3]]
        print('distinct barL d during live:',len(set(s[1] for s in samp)),' distinct r:',len(set(s[2] for s in samp)))
        await pg.wait_for_timeout(5000)
        src=np.array(Image.open('src31_light.png').convert('L')).astype(int)
        a=np.array(Image.open(io.BytesIO(await pg.screenshot())).convert('L')).astype(int); d=np.abs(a-src); print('live end vs src max',d.max(),'n>16',(d>16).sum())
        await pg.evaluate("document.getElementById('replay').click()")
        await pg.wait_for_timeout(1000); m=np.array(Image.open(io.BytesIO(await pg.screenshot())).convert('L')); print('replay@1s ink px', (m<128).sum())
        await pg.evaluate("document.getElementById('theme').click()"); await pg.wait_for_timeout(8000)
        print('hash after toggle', await pg.evaluate("location.hash"), 'dark?', await pg.evaluate("document.body.classList.contains('dark')"))
        a=np.array(Image.open(io.BytesIO(await pg.screenshot())).convert('L')).astype(int); s2=np.array(Image.open('src31_dark.png').convert('L')).astype(int); d=np.abs(a-s2); print('live dark end vs src max',d.max(),'n>16',(d>16).sum())
        print('errors',errs); await b.close()
asyncio.run(main())

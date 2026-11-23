import asyncio, os
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.webkit.launch(); pg=await b.new_page(viewport={'width':1280,'height':720})
        errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.goto('file://'+os.path.abspath('v32.html'))
        for t in (1500,1700,1900,2500,2700):
            await pg.evaluate(f"seek({t})"); print(t, await pg.evaluate("[document.querySelector('.barL').getAttribute('d').slice(0,30), document.getElementById('growC').getAttribute('r'), getComputedStyle(document.querySelector('.barL')).opacity]"))
            await pg.screenshot(path=f'chk32/wk_{t}.png')
        print('errors',errs); await b.close()
asyncio.run(main())

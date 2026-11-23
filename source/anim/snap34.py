import asyncio, os, sys
from playwright.async_api import async_playwright
src,out,h=sys.argv[1],sys.argv[2],sys.argv[3]; frames=[int(x) for x in sys.argv[4].split(',')]
async def main():
    os.makedirs(out,exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':2560,'height':1440}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.goto('file://'+os.path.abspath(src)+h); await pg.evaluate("document.body.classList.add('capture')"); await pg.wait_for_timeout(300)
        for f in frames:
            await pg.evaluate(f"seek({f*1000/60})"); await pg.screenshot(path=f'{out}/f{f:04d}.png')
        print(errs); await b.close()
asyncio.run(main())

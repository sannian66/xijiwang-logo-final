import asyncio, os, sys
from playwright.async_api import async_playwright
src,out,hashv=sys.argv[1],sys.argv[2],sys.argv[3]; times=[float(x) for x in sys.argv[4].split(',')]; W=int(sys.argv[5]) if len(sys.argv)>5 else 1280
async def main():
    os.makedirs(out,exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':W,'height':W*9//16})
        await pg.goto('file://'+os.path.abspath(src)+hashv); await pg.evaluate("document.body.classList.add('capture')"); await pg.wait_for_timeout(300)
        for t in times:
            await pg.evaluate(f"seek({t*1000})"); await pg.screenshot(path=f'{out}/t{int(round(t*1000)):05d}.png')
        await b.close()
asyncio.run(main())

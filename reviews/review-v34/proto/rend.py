import asyncio, os, sys
from playwright.async_api import async_playwright
src,out,hashv,a,b=sys.argv[1],sys.argv[2],sys.argv[3].replace('none',''),int(sys.argv[4]),int(sys.argv[5]); W=int(sys.argv[6])
async def main():
    os.makedirs(out,exist_ok=True)
    async with async_playwright() as p:
        br=await p.chromium.launch(); pg=await br.new_page(viewport={'width':W,'height':W*9//16})
        await pg.goto('file://'+os.path.abspath(src)+hashv); await pg.evaluate("document.body.classList.add('capture')"); await pg.wait_for_timeout(300)
        for i in range(a,b):
            await pg.evaluate(f"seek({i*1000/60})"); await pg.screenshot(path=f'{out}/f{i:04d}.png')
        await br.close()
asyncio.run(main())

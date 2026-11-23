import asyncio, os, sys
from playwright.async_api import async_playwright
src, out, hashv = sys.argv[1], sys.argv[2], sys.argv[3]
async def main():
    os.makedirs(out,exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1920,'height':1080})
        await pg.goto('file://'+os.path.abspath(src)+hashv)
        await pg.evaluate("document.body.classList.add('capture')")
        await pg.wait_for_timeout(300)
        fps=30; dur=5.6
        for i in range(int(fps*dur)):
            await pg.evaluate(f"seek({i*1000/fps})")
            await pg.screenshot(path=f'{out}/f{i:04d}.png')
        await b.close()
asyncio.run(main())

import asyncio, os
from playwright.async_api import async_playwright
async def main():
    os.makedirs('frames',exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1600,'height':600})
        await pg.goto('file://'+os.path.abspath('xijiwang-logo-animation.html'))
        await pg.evaluate("document.body.classList.add('capture')")
        await pg.wait_for_timeout(300)
        fps=30; dur=4.8
        for i in range(int(fps*dur)):
            await pg.evaluate(f"seek({i*1000/fps})")
            await pg.screenshot(path=f'frames/f{i:04d}.png')
        await b.close()
asyncio.run(main())

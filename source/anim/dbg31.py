import asyncio, os, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':2560,'height':1440})
        await pg.goto('file://'+os.path.abspath(sys.argv[1])); await pg.evaluate("document.body.classList.add('capture')"); await pg.wait_for_timeout(300)
        print(await pg.evaluate("seek(7483); document.getAnimations().map(a=>(a.effect.target.getAttribute('class')||a.effect.target.id)+':'+a.animationName+':'+a.playState).join('  ')"))
        print(await pg.evaluate("[...document.querySelectorAll('.zh')].slice(0,2).map(e=>getComputedStyle(e).transform+' '+getComputedStyle(e).transformBox).join(' | ')"))
        await b.close()
asyncio.run(main())

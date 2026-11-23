import re, asyncio
from playwright.async_api import async_playwright
U='/workspace/projects/0b4d0196-ffe5-4f80-a356-b2ae9513897b/files/uploads/'
src={'v4.2':U+'xijiwang-horizontal-primary-af6d799ceb5b.svg','v5.6':U+'西几王传媒_横版-da23028ec272.svg'}
def icon_group(s):
    i=s.index('<g'); depth=0; j=i
    for m in re.finditer(r'<g\b|</g>',s[i:]):
        depth+= 1 if m.group()!='</g>' else -1
        if depth==0: j=i+m.end(); break
    return s[i:j]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page()
        for k,f in src.items():
            g=icon_group(open(f,encoding='utf-8').read())
            await pg.set_content(f'<svg id=s xmlns="http://www.w3.org/2000/svg" viewBox="0 0 782 256" width=782 height=256>{g}</svg>')
            bb=await pg.evaluate("(()=>{const b=document.querySelector('#s > g').getBBox();return [b.x,b.y,b.width,b.height]})()")
            # 头像：图标居中，占画面约 66%，圆形裁切也安全
            x,y,w,h=bb; side=max(w,h)/0.66; cx,cy=x+w/2,y+h/2; vx,vy=cx-side/2,cy-side/2
            # bbox 在 g 的本地坐标里（含 transform 前？）—用屏幕坐标更稳
            r=await pg.evaluate("(()=>{const r=document.querySelector('#s > g').getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
            x,y,w,h=r; side=max(w,h)/0.66; cx,cy=x+w/2,y+h/2; vx,vy=cx-side/2,cy-side/2
            svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx:.2f} {vy:.2f} {side:.2f} {side:.2f}" width="1024" height="1024">'
                 f'<title>西几王传媒 XIJIWANG MEDIA · {k} 头像</title><rect x="{vx:.2f}" y="{vy:.2f}" width="{side:.2f}" height="{side:.2f}" fill="#FFFFFF"/>{g}</svg>')
            name=f'xijiwang-avatar-{k}'
            open(name+'.svg','w',encoding='utf-8').write(svg)
            for px in (1024,):
                await pg.set_viewport_size({'width':px,'height':px})
                await pg.set_content(f'<html><body style="margin:0">{svg.replace("width=\"1024\" height=\"1024\"",f"width=\"{px}\" height=\"{px}\"")}</body></html>')
                await pg.screenshot(path=f'{name}-{px}.png',clip={'x':0,'y':0,'width':px,'height':px})
            print(k,r)
        await b.close()
asyncio.run(main())

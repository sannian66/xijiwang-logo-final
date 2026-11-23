import re
from svgpathtools import parse_path
s=open('/workspace/projects/0b4d0196-ffe5-4f80-a356-b2ae9513897b/files/uploads/xijiwang-horizontal-primary-af6d799ceb5b.svg').read()
ds=re.findall(r'd="([^"]*)"',s)
def groups(d):
    subs=[x.strip() for x in re.split(r'(?=M)',d) if x.strip()]
    items=[]
    for sp in subs:
        b=parse_path(sp).bbox(); items.append([b[0],b[1],[sp]])
    items.sort(key=lambda x:x[0]); out=[]
    for it in items:
        if out and it[0] <= out[-1][1]:
            out[-1][1]=max(out[-1][1],it[1]); out[-1][2]+=it[2]
        else: out.append(it)
    return [' '.join(g[2]) for g in out]
zh=groups(ds[3]); en=groups(ds[4])
face=[x.strip() for x in re.split(r'(?=M)',ds[2]) if x.strip()]
nose,mouth=face[0],face[1]
assert len(zh)==5 and len(en)==13, (len(zh),len(en))
zh_paths='\n'.join(f'<path class="zh" style="--i:{i}" fill-rule="evenodd" d="{d}"/>' for i,d in enumerate(zh))
en_paths='\n'.join(f'<path class="en" style="--i:{i}" fill-rule="evenodd" d="{d}"/>' for i,d in enumerate(en))
zh_clip='\n'.join(f'<path fill-rule="evenodd" clip-rule="evenodd" d="{d}"/>' for d in zh)
tpl=open(__import__('sys').argv[1]).read()
html=(tpl.replace('{{MANE}}',ds[0]).replace('{{EYES}}',ds[1]).replace('{{NOSE}}',nose).replace('{{MOUTH}}',mouth)
      .replace('{{ZH}}',zh_paths).replace('{{EN}}',en_paths).replace('{{ZHCLIP}}',zh_clip))
open(__import__('sys').argv[2],'w').write(html)
print('ok')

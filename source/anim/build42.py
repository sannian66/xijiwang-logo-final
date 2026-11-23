import re, math, sys
from svgpathtools import parse_path
s=open('/workspace/projects/0b4d0196-ffe5-4f80-a356-b2ae9513897b/files/uploads/xijiwang-horizontal-primary-af6d799ceb5b.svg').read()
ds=re.findall(r'd="([^"]*)"',s)
def split(d): return [x.strip() for x in re.split(r'(?=M)',d) if x.strip()]
outer,face=split(ds[0])
eyeL,eyeR=split(ds[1])
mouth=split(ds[2])[1]
def groups(d):
    items=[]
    for sp in split(d):
        b=parse_path(sp).bbox(); items.append([b[0],b[1],[sp]])
    items.sort(key=lambda x:x[0]); out=[]
    for it in items:
        if out and it[0]<=out[-1][1]: out[-1][1]=max(out[-1][1],it[1]); out[-1][2]+=it[2]
        else: out.append(it)
    return [' '.join(g[2]) for g in out]
zh=groups(ds[3]); en=groups(ds[4])
CX,CY=128,123.75
clips=[];blades=[]
for k in range(8):
    a0=math.radians(-90+k*45-3.5); a1=math.radians(-90+(k+1)*45+3.5)
    R=150
    m=(a0+a1)/2; pts=[(CX-6*math.cos(m),CY-6*math.sin(m))]+[(CX+R*math.cos(a0+(a1-a0)*j/6),CY+R*math.sin(a0+(a1-a0)*j/6)) for j in range(7)]
    clips.append(f'<clipPath id="bl{k}"><polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x,y in pts)}"/></clipPath>')
    # pivot: rim point on leading edge
    pa=math.radians(-90+k*45); px=CX+100*math.cos(pa); py=CY+100*math.sin(pa)
    blades.append(f'<g class="bladeState" style="transform-origin:{px:.2f}px {py:.2f}px"><g class="bladeIntro" style="--k:{(7-k+3)%8}"><g clip-path="url(#bl{k})"><path d="{outer}"/></g></g></g>')
seams=[]
for k in range(8):
    a=math.radians(-90+k*45)
    def P(r,da): return (CX+r*math.cos(a+math.radians(da)), CY+r*math.sin(a+math.radians(da)))
    p0=P(10,40); c=P(62,26); p1=P(112,0)
    seams.append(f'<path d="M{p0[0]:.2f} {p0[1]:.2f} Q{c[0]:.2f} {c[1]:.2f} {p1[0]:.2f} {p1[1]:.2f}"/>')
zh_paths='\n'.join(f'<path class="zh" style="--i:{i}" fill-rule="evenodd" d="{d}"/>' for i,d in enumerate(zh))
en_paths='\n'.join(f'<path class="en" style="--i:{i}" fill-rule="evenodd" d="{d}"/>' for i,d in enumerate(en))
t=open(sys.argv[1]).read()
for k,v in {'CLIPS':'\n'.join(clips),'BLADES':'\n'.join(blades),'SEAMS':'\n'.join(seams),'OUTER':outer,'FACE':face,'EYEL':eyeL,'EYER':eyeR,'MOUTH':mouth,'ZH':zh_paths,'EN':en_paths}.items():
    t=t.replace('{{'+k+'}}',v)
open(sys.argv[2],'w').write(t); print('ok')

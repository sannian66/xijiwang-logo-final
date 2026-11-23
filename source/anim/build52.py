import re, math, sys, json
import numpy as np
from svgpathtools import parse_path
s=open('v5src.svg').read()
P={m.group(1):m.group(2) for m in re.finditer(r'<path id="([^"]+)"[^>]*?d="([^"]+)"',s)}
TX,TY,SC=-4.90401985,-10.37941049,0.2233921801
def V(z): return np.array([TX+SC*z.real, TY+SC*z.imag])
N=220
def sample(d):
    p=parse_path(d); L=p.length(); pts=[]
    for j in range(N):
        pts.append(V(p.point(p.ilength(L*j/N, s_tol=1e-4) if hasattr(p,'ilength') else j/N)))
    return np.array(pts)
def area(a): x,y=a[:,0],a[:,1]; return .5*np.sum(x*np.roll(y,-1)-np.roll(x,-1)*y)
def resample_poly(poly):
    poly=np.array(poly+[poly[0]],float); seg=np.linalg.norm(np.diff(poly,axis=0),axis=1); cum=np.r_[0,np.cumsum(seg)]
    out=[]
    for j in range(N):
        d=cum[-1]*j/N; i=np.searchsorted(cum,d,side='right')-1; f=(d-cum[i])/seg[i]; out.append(poly[i]+(poly[i+1]-poly[i])*f)
    return np.array(out)
# ---- 字母（粗黑几何字形，局部坐标，以中心为原点）
a,b,c=19,22,11
def X_poly():
    s=(a-c)/(2*a-c); k=-(-b+s*2*b)
    return [(-a,-b),(-a+c,-b),(0,-k),(a-c,-b),(a,-b),(c/2,0),(a,b),(a-c,b),(0,k),(-a+c,b),(-a,b),(-c/2,0)]
def J_poly():
    pts=[(3,-22),(13,-22),(13,6)]
    pts+=[(13*math.cos(t),6+13*math.sin(t)) for t in np.linspace(0,math.pi,24)[1:]]
    pts+=[(-13,2),(-4,2)]
    pts+=[(3*math.cos(t)+0, 6+3*math.sin(t)) for t in np.linspace(math.pi,0,12)]
    return pts
def W_poly():
    return [(-26,-16),(-17,-16),(-10,7),(-4,-10),(4,-10),(10,7),(17,-16),(26,-16),(15,16),(6,16),(0,-1),(-6,16),(-15,16)]
# ---- 中英文分字
blocks=re.findall(r'<g fill="#000000" transform="translate\(274 ([\d.]+)\)">(.*?)</g>',s,re.S)
def split(d): return [x.strip() for x in re.split(r'(?=M)',d) if x.strip()]
def groups(ds):
    items=[]
    for d in ds:
        for sp in split(d):
            bb=parse_path(sp).bbox(); items.append([bb[0],bb[1],[sp]])
    items.sort(key=lambda x:x[0]); out=[]
    for it in items:
        if out and it[0]<=out[-1][1]-0.5: out[-1][1]=max(out[-1][1],it[1]); out[-1][2]+=it[2]
        else: out.append(it)
    return [' '.join(g[2]) for g in out]
zh=groups(re.findall(r'd="([^"]+)"',blocks[0][1])); en=groups(re.findall(r'd="([^"]+)"',blocks[1][1]))

def glyph_pts(d):
    subs=[x for x in split(d)]; sp=max(subs,key=lambda q: abs(parse_path(q).area()) if hasattr(parse_path(q),'area') else len(q))
    p=parse_path(sp); Lg=p.length(); return np.array([[z.real,z.imag] for z in (p.point(p.ilength(Lg*j/N,s_tol=1e-4)) for j in range(N))])
CAP=56.0
G={k:glyph_pts(en[i]) for k,i in (('x',0),('j',2),('w',4))}
hx=np.ptp(G['x'][:,1]); sc=CAP/hx
letters={}; pos={}; base=G['x'][:,1].max()
widths={k:np.ptp(G[k][:,0])*sc for k in 'xjw'}; gap=CAP*.16
tot=sum(widths.values())+2*gap; x0=135.2-tot/2
for k in 'xjw':
    g=G[k]; c=np.array([(g[:,0].min()+g[:,0].max())/2,(g[:,1].min()+g[:,1].max())/2])
    letters[k]=list(map(tuple,(g-c)*sc))
    cy=125.5+((c[1]-base)*sc+CAP/2)   # 共用基线
    pos[k]=[round(x0+widths[k]/2,2),round(cy,2)]; x0+=widths[k]+gap
print('pos',pos,widths)

targets={'x':'cross-eye','j':'nose','w':'mouth'}
data={}
for k in 'xjw':
    T=sample(P[targets[k]]); L=resample_poly(letters[k])
    if np.sign(area(T))!=np.sign(area(L)): L=L[::-1]
    tc=(T.min(0)+T.max(0))/2; Tr=T-tc
    Ln=(L-(L.min(0)+L.max(0))/2)/np.ptp(L,0).max(); Tn=Tr/np.ptp(Tr,0).max()
    costs=sorted(range(N),key=lambda o: np.sum((np.roll(Ln,-o,0)-Tn)**2))[:8]
    best=None
    for o in costs:
        A=np.roll(Ln,-o,0); Dm=np.linalg.norm(A[:,None]-Tn[None],axis=2)
        C=np.full((N+1,N+1),np.inf); C[0,0]=0
        for i in range(1,N+1):
            row=C[i]; prev=C[i-1]; d=Dm[i-1]
            for j in range(1,N+1):
                m=prev[j-1]
                if prev[j]<m: m=prev[j]
                if row[j-1]<m: m=row[j-1]
                row[j]=d[j-1]+m
        if best is None or C[N,N]<best[0]: best=(C[N,N],o,C)
    _,o,C=best; i,j=N,N; path=[]
    while i>0 and j>0:
        path.append((i-1,j-1)); opts=[(C[i-1,j-1],i-1,j-1),(C[i-1,j],i-1,j),(C[i,j-1],i,j-1)]; _,i,j=min(opts)
    path=path[::-1]; Lr=np.roll(L,-o,0)
    PA=np.array([Lr[a] for a,_ in path]); PB=np.array([Tr[c] for _,c in path])
    seg=np.linalg.norm(np.diff(PA,axis=0),axis=1)+np.linalg.norm(np.diff(PB,axis=0),axis=1); cum=np.r_[0,np.cumsum(seg)]
    M2=260; idx=np.interp(np.linspace(0,cum[-1],M2,endpoint=False),cum,np.arange(len(path)))
    f=idx-np.floor(idx); i0=np.floor(idx).astype(int); i1=np.minimum(i0+1,len(path)-1)
    L=PA[i0]*(1-f)[:,None]+PA[i1]*f[:,None]; Tr=PB[i0]*(1-f)[:,None]+PB[i1]*f[:,None]
    data[k]={'L':np.round(L,2).flatten().tolist(),'T':np.round(Tr,2).flatten().tolist(),'tc':np.round(tc,2).tolist(),'p':pos[k]}
# ---- 鬃毛楔形分片
mane=P['mane']; subs=[x.strip() for x in re.split(r'(?=M)',mane) if x.strip()]; outer=subs[0]; facehole=subs[3]
CX,CY=135.2,125.5; K=14; clips=[]; wedges=[]
for k in range(K):
    a0=math.radians(-90+k*360/K-1.5); a1=math.radians(-90+(k+1)*360/K+1.5); R=160
    pts=[(CX,CY)]+[(CX+R*math.cos(a0+(a1-a0)*j/5),CY+R*math.sin(a0+(a1-a0)*j/5)) for j in range(6)]
    clips.append(f'<clipPath id="w{k}"><polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x,y in pts)}"/></clipPath>')
    wedges.append(f'<g class="wedge" style="--k:{k}" clip-path="url(#w{k})"><g transform="translate({TX} {TY}) scale({SC})"><path fill-rule="evenodd" d="{mane}"/></g></g>')
print('zh',len(zh),'en',len(en),'ty',[b[0] for b in blocks])
rep={'CLIPS':'\n'.join(clips),'WEDGES':'\n'.join(wedges),'OUTER':outer,'LT':f'translate({TX} {TY}) scale({SC})',
     'CROSS':P['cross-eye'],'NOSE':P['nose'],'MOUTH':P['mouth'],'MORPH':json.dumps(data),'ENY':blocks[1][0],
     'ZH':'\n'.join(f'<path class="zh" style="--i:{i}" fill-rule="evenodd" d="{d}"/>' for i,d in enumerate(zh)),
     'EN':'\n'.join(f'<path class="en" style="--i:{i}" fill-rule="evenodd" d="{d}"/>' for i,d in enumerate(en))}
t=open(sys.argv[1]).read()
rep.update({'MANE':mane,'FACEHOLE':facehole,'PLAYEYE':P['play-eye']})
for k,v in rep.items(): t=t.replace('{{'+k+'}}',v)
open(sys.argv[2],'w').write(t); print('ok')

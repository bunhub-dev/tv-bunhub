import math, random, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
random.seed(7)
P=dict(void="#0F161E",hull="#27323E",rim="#F0EECF",fleece="#B49FCC",
 play="#0BF591",volt="#F8ED0F",live="#F42EE3",signal="#F42A36",coral="#F64C60",amber="#E5B620")
def rgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def lerp(a,b,t): return tuple(a[i]+(b[i]-a[i])*t for i in range(3))
SPEC=[P["play"],P["volt"],P["coral"],P["live"]]
def spec(t):
    t=max(0,min(1,t))*(len(SPEC)-1); i=min(int(t),len(SPEC)-2)
    return lerp(rgb(SPEC[i]),rgb(SPEC[i+1]),t-i)
# ---------- mark geometry in 1000x1000 box ----------
def mark_geometry():
    G=[]  # (pts, colorfn, width, kind)
    cx,cy,rx,ry=500,430,300,250
    bell=[(cx+rx*math.cos(math.pi+a*math.pi/60*1), cy+ry*math.sin(math.pi+a*math.pi/60)) for a in range(0,61)]
    bell=[(cx+rx*math.cos(math.pi*(1+k/60)), cy+ry*math.sin(math.pi*(1+k/60))) for k in range(61)]
    G.append((bell,lambda t:rgb(P["rim"]),26,"rim"))
    # base lip
    G.append(([(cx-rx,cy),(cx+rx,cy)],lambda t:rgb(P["rim"]),26,"rim"))
    # bun pleats: curves fanning from top apex-ish to base
    for k,fx in enumerate((-0.62,-0.31,0,0.31,0.62)):
        pts=[]
        for s in range(41):
            u=s/40
            x=cx+fx*rx*(0.15+0.85*u)+ (fx*40)*math.sin(u*math.pi)
            y=cy-ry*0.92*(1-u)**0.9*(1-0.0*abs(fx))+ (0)
            y=cy-ry*(1-u**1.15)*math.sqrt(max(0,1-(fx*(0.15+0.85*u))**2))
            pts.append((x,y))
        G.append((pts,lambda t,k=k:spec(0.12+0.18*k+0.0*t),12,"pleat"))
    # tentacles
    for k in range(9):
        x0=cx-rx*0.82+k*(rx*1.64/8)
        L=430+random.randint(-60,90); amp=14+random.random()*20; ph=random.random()*6.28; fr=2.2+random.random()*1.6
        pts=[(x0+amp*math.sin(fr*(s/60)*math.pi*2+ph)*(s/60)**0.6 - (x0-cx)*0.25*(s/60), cy+8+L*(s/60)) for s in range(61)]
        G.append((pts,lambda t,k=k:spec(0.04+0.92*(t*0.8+k/8*0.2)),max(5,11-k%3*2),"tent"))
    return G
def draw_mark(size=1000,glow=True,bg=None):
    S=3; W=size*S; k=W/1000
    base=Image.new("RGBA",(W,W),(0,0,0,0)); d=ImageDraw.Draw(base)
    for pts,cf,w,kind in mark_geometry():
        n=len(pts)
        for i in range(n-1):
            t=i/(n-1); c=tuple(int(v) for v in cf(t))+(255,)
            if kind=="tent": ww=w*k*(1-0.55*t)
            else: ww=w*k
            (x0,y0),(x1,y1)=pts[i],pts[i+1]
            d.line([(x0*k,y0*k),(x1*k,y1*k)],fill=c,width=max(1,int(ww)))
            r=ww/2; d.ellipse([x1*k-r,y1*k-r,x1*k+r,y1*k+r],fill=c)
    # spores
    for _ in range(46):
        x=random.uniform(250,750); y=random.uniform(480,980); r=random.uniform(2,7)*k
        c=tuple(int(v) for v in spec(random.random()))+(255,)
        d.ellipse([x*k-r,y*k-r,x*k+r,y*k+r],fill=c)
    out=base
    if glow:
        g=base.filter(ImageFilter.GaussianBlur(14*k)); g=Image.merge("RGBA",(*g.split()[:3],g.split()[3].point(lambda a:int(a*0.9))))
        out=Image.alpha_composite(Image.new("RGBA",(W,W),(0,0,0,0)),g); out=Image.alpha_composite(out,base)
    out=out.resize((size,size),Image.LANCZOS)
    if bg: 
        b=Image.new("RGBA",(size,size),rgb(bg)+(255,)); out=Image.alpha_composite(b,out)
    return out
def svg_mark():
    defs=[];body=[]
    for i,(pts,cf,w,kind) in enumerate(mark_geometry()):
        d="M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts)
        if kind=="rim": stroke=P["rim"]
        else:
            y0=min(p[1] for p in pts); y1=max(p[1] for p in pts)+1
            c0="#%02X%02X%02X"%tuple(int(v) for v in cf(0)); c1="#%02X%02X%02X"%tuple(int(v) for v in cf(1))
            defs.append(f'<linearGradient id="g{i}" gradientUnits="userSpaceOnUse" x1="0" y1="{y0:.0f}" x2="0" y2="{y1:.0f}"><stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/></linearGradient>')
            stroke=f"url(#g{i})"
        body.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs>'+"".join(defs)+
            '<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><g filter="url(#glow)">'+"".join(body)+'</g></svg>')
open("logo/jellybun-mark.svg","w").write(svg_mark())
m=draw_mark(2048); m.save("logo/jellybun-mark-2048.png")
draw_mark(2048,bg=P["void"]).convert("RGB").save("logo/jellybun-mark-on-void-2048.png")
draw_mark(512).save("logo/jellybun-mark-512.png"); draw_mark(180,glow=False,bg=P["void"]).convert("RGB").save("logo/apple-touch-icon-180.png")
# ---------- fonts ----------
F="/Users/js/Library/Fonts/"
def gsf(sz,w=500,rond=100):
    f=ImageFont.truetype(F+"GoogleSansFlex-VariableFont_ROND,opsz,slnt,wdth,wght.ttf",sz)
    try:
        ax=f.get_variation_axes(); vals=[]
        for a in ax:
            n=a["name"] if isinstance(a["name"],str) else a["name"].decode()
            vals.append({"Weight":w,"Roundness":rond}.get(n,a["default"]))
        f.set_variation_by_axes(vals)
    except Exception as e: print("axes",e)
    return f
major=lambda s:ImageFont.truetype(F+"MajorMonoDisplay-Regular.ttf",s)
mono=lambda s:ImageFont.truetype(F+"AtkinsonHyperlegibleMono-VariableFont_wght.ttf",s)
# ---------- wordmark lockups ----------
def stars(img,n,seed=3):
    r=random.Random(seed); d=ImageDraw.Draw(img); W,H=img.size
    for _ in range(n):
        x,y=r.randrange(W),r.randrange(H); a=r.choice((60,90,140,200)); s=r.choice((1,1,1,2))
        d.ellipse([x,y,x+s,y+s],fill=(240,238,207,a))
def lockup(path,W=3000,H=1000,bg=None):
    img=Image.new("RGBA",(W,H),rgb(bg)+(255,) if bg else (0,0,0,0))
    mk=draw_mark(820); img.alpha_composite(mk,(90,90))
    d=ImageDraw.Draw(img)
    d.text((1000,230),"tv.bunhub",font=major(300),fill=rgb(P["rim"]))
    d.text((1010,600),"drift in.  press play.",font=gsf(104,420),fill=rgb(P["fleece"]))
    d.text((1010,760),"BUNHUB.DEV / TV",font=mono(54),fill=rgb(P["play"]))
    img.save(path)
lockup("logo/lockup-horizontal-on-void.png",bg=P["void"]); lockup("logo/lockup-horizontal-transparent.png")
# ---------- brand board 3840x2160 ----------
W,H=3840,2160
B=Image.new("RGBA",(W,H),rgb(P["void"])+(255,)); stars(B,2600)
d=ImageDraw.Draw(B)
pad=160
# header
d.text((pad,pad-20),"tv.bunhub.dev — BRAND BOARD v0.1",font=mono(46),fill=rgb(P["play"]))
d.text((pad,pad+60),"Jellynaut",font=major(190),fill=rgb(P["rim"]))
d.text((pad+8,pad+290),"One quiet hero in a loud, living dark.",font=gsf(64,380),fill=rgb(P["fleece"]))
# hero mark
B.alpha_composite(draw_mark(1100),(W-pad-1100,pad-40))
# palette
y0=720; d.text((pad,y0-80),"PALETTE  /  void + glow",font=mono(40),fill=rgb(P["rim"]))
sw=[("VOID",P["void"],"canvas"),("HULL",P["hull"],"surfaces"),("RIM",P["rim"],"text · outlines"),("FLEECE",P["fleece"],"house llama · secondary"),
    ("PLAY",P["play"],"primary · focus"),("VOLT",P["volt"],"highlight · now"),("CORAL",P["coral"],"warm · resume"),("LIVE",P["live"],"requests · live"),("SIGNAL",P["signal"],"alerts only"),("AMBER",P["amber"],"warnings")]
sx=pad; w=330; gap=22
for i,(n,h,r) in enumerate(sw):
    x=sx+i*(w+gap)
    d.rounded_rectangle([x,y0,x+w,y0+300],24,fill=rgb(h),outline=rgb(P["hull"]) ,width=3)
    ink=rgb(P["void"]) if sum(rgb(h))>380 else rgb(P["rim"])
    d.text((x+24,y0+28),n,font=gsf(46,700),fill=ink); d.text((x+24,y0+96),h,font=mono(34),fill=ink)
    d.text((x+24,y0+236),r,font=gsf(30,420),fill=ink)
# spectrum bar
bar=Image.new("RGBA",(W-2*pad,56)); bd=ImageDraw.Draw(bar)
for x in range(bar.width): bd.line([(x,0),(x,56)],fill=tuple(int(v) for v in spec(x/bar.width))+(255,))
mask=Image.new("L",bar.size,0); ImageDraw.Draw(mask).rounded_rectangle([0,0,bar.width,56],28,fill=255)
glow=bar.filter(ImageFilter.GaussianBlur(26)); B.alpha_composite(Image.composite(glow,Image.new("RGBA",bar.size,(0,0,0,0)),mask),(pad,y0+340)) if False else None
B.paste(bar,(pad,y0+350),mask)
d.text((pad,y0+420),"GLOW SPECTRUM  —  play → volt → coral → live.  Neon is light, never fill: use on dark, as stroke / glow / single accents. Max two spectrum hues per screen.",font=gsf(34,400),fill=rgb(P["fleece"]))
# type
ty=1330
d.text((pad,ty-80),"TYPE  /  three open families (OFL)",font=mono(40),fill=rgb(P["rim"]))
d.text((pad,ty),"tv.bunhub",font=major(150),fill=rgb(P["rim"]))
d.text((pad,ty+190),"Major Mono Display — wordmark & splash titles only, lowercase",font=gsf(34,400),fill=rgb(P["fleece"]))
d.text((pad+1250,ty),"Soft, round, watchable.",font=gsf(110,640),fill=rgb(P["rim"]))
d.text((pad+1250,ty+150),"Google Sans Flex — UI & copy · ROND 100 · 400/500/700",font=gsf(34,400),fill=rgb(P["fleece"]))
d.text((pad+2300,ty),"S01E04 · 2160p · HDR10",font=mono(70),fill=rgb(P["play"]))
d.text((pad+2300,ty+150),"Atkinson Hyperlegible Mono — metadata, badges, codes",font=gsf(34,400),fill=rgb(P["fleece"]))
# UI sample
uy=1670
d.text((pad,uy-60),"UI  /  Jellyfin skin sample",font=mono(40),fill=rgb(P["rim"]))
for i,(t,c) in enumerate([("Play",P["play"]),("Resume",P["coral"]),("Request",P["live"]),("Now",P["volt"])]):
    x=pad+i*370
    d.rounded_rectangle([x,uy+10,x+330,uy+120],55,fill=rgb(c) if i==0 else None,outline=rgb(c),width=5)
    d.text((x+165,uy+65),t,font=gsf(52,650),fill=rgb(P["void"]) if i==0 else rgb(c),anchor="mm")
# poster cards w/ glow
for i in range(4):
    x=pad+1600+i*250; y=uy-10
    d.rounded_rectangle([x,y,x+210,y+315],18,fill=rgb(P["hull"]))
    d.rounded_rectangle([x,y,x+210,y+315],18,outline=rgb(P["play"]) if i==1 else rgb(P["hull"]),width=6)
# splash thumb
th=Image.open("/Users/js/projects/bcu-posters/source/jellynaut.jpg").convert("RGBA").resize((560,315),Image.LANCZOS)
B.alpha_composite(th,(W-pad-560,uy-10))
d.text((W-pad-560,uy+325),"reference: jellynaut.jpg",font=mono(30),fill=rgb(P["fleece"]))
B.convert("RGB").save("board/brand-board-v0.1.png")
json.dump(P,open("tokens/palette.json","w"),indent=1)
print("ok")

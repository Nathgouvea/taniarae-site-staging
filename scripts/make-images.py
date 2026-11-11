#!/usr/bin/env python3
"""Regenerate all website images from the two original photos.

Run this when Tania's photo changes:

    pip install Pillow          # once
    python3 scripts/make-images.py path/to/tania.jpg path/to/tania-avatar.jpg

It writes into assets/images/:
  - tania-{320,480,720}.{avif,webp,jpg}   about-me photo (4:5 crop)
  - tania-900.jpg                          used in structured data
  - tania-avatar-{80,120}.{avif,webp,jpg}  header avatar
  - og-image.jpg                           1200x630 social sharing image
  - favicon-32.png, apple-touch-icon.png, icon-192.png, icon-512.png
(favicon.svg is hand-written and does not need regenerating.)
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
IMG = str(ROOT / "assets/images") + "/"
FONTS = str(ROOT / "assets/fonts") + "/"
PHOTO, AVATAR = sys.argv[1], sys.argv[2]

# --- Responsive photos ---------------------------------------------------
src = Image.open(PHOTO).convert('RGB')
w, h = src.size; ch = int(w * 5 / 4); top = int((h - ch) * 0.40)
crop = src.crop((0, top, w, top + ch))
for W in (320, 480, 720):
    im = crop.resize((W, int(W * 5 / 4)), Image.LANCZOS)
    im.save(f'{IMG}tania-{W}.jpg', quality=80, optimize=True, progressive=True)
    im.save(f'{IMG}tania-{W}.webp', quality=78, method=6)
    im.save(f'{IMG}tania-{W}.avif', quality=60)
crop.save(f'{IMG}tania-900.jpg', quality=82, optimize=True, progressive=True)
av = Image.open(AVATAR).convert('RGB')
for W in (80, 120):
    im = av.resize((W, W), Image.LANCZOS)
    im.save(f'{IMG}tania-avatar-{W}.jpg', quality=82, optimize=True)
    im.save(f'{IMG}tania-avatar-{W}.webp', quality=80, method=6)
    im.save(f'{IMG}tania-avatar-{W}.avif', quality=60)

# --- Social image + icons --------------------------------------------------
PAPER=(251,248,241); INK=(30,43,69); HAND=(38,64,143); YEL=(246,201,76); MUTED=(89,96,111)
def F(n,s): return ImageFont.truetype(FONTS+n,s)
serif=F('instrument-serif-latin-400-normal.woff2',78); serif_i=F('instrument-serif-latin-400-italic.woff2',78)
hand=F('caveat-latin-600-normal.woff2',60); body=F('figtree-latin-600-normal.woff2',30); body4=F('figtree-latin-400-normal.woff2',26)
S=2; W,H=1200*S,630*S
og=Image.new('RGB',(W,H),PAPER)
# polaroid
p=Image.open(IMG+'tania-720.jpg').resize((330*S,412*S),Image.LANCZOS)
b=10*S; pol=Image.new('RGBA',(p.width+2*b,p.height+2*b),(255,255,255,255)); pol.paste(p,(b,b))
sh=Image.new('RGBA',(pol.width+120*S,pol.height+120*S),(0,0,0,0))
ImageDraw.Draw(sh).rectangle((60*S,72*S,60*S+pol.width,72*S+pol.height),fill=(30,43,69,60))
sh=sh.filter(ImageFilter.GaussianBlur(18*S)).rotate(2.5,resample=Image.BICUBIC,expand=True)
polr=pol.rotate(2.5,resample=Image.BICUBIC,expand=True)
x,y=80*S,78*S
og.paste(sh,(x-60*S,y-60*S),sh); og.paste(polr,(x,y),polr)
tape=Image.new('RGBA',(110*S,32*S),(246,201,76,190)).rotate(-3,expand=True,resample=Image.BICUBIC)
og.paste(tape,(x+polr.width//2-55*S,y-14*S),tape)
d=ImageDraw.Draw(og)
tx=520*S
d.text((tx,95*S),'Dear you,',font=F('caveat-latin-600-normal.woff2',60*S),fill=HAND)
sF=F('instrument-serif-latin-400-normal.woff2',72*S); siF=F('instrument-serif-latin-400-italic.woff2',72*S)
lines=[('You know something',False),('has to change. You just',False)]
yy=185*S
for t,_ in lines:
    d.text((tx,yy),t,font=sF,fill=INK); yy+=76*S
# highlighted italic line
t="don’t know how."
bb=d.textbbox((tx,yy),t,font=siF)
hl=Image.new('RGBA',(bb[2]-bb[0]+16*S,int((bb[3]-bb[1])*0.42)),(246,201,76,215))
og.paste(hl,(tx-8*S,bb[3]-hl.height+6*S),hl)
d=ImageDraw.Draw(og); d.text((tx,yy),t,font=siF,fill=INK)
d.text((tx,470*S),'Tania Rae',font=F('figtree-latin-600-normal.woff2',32*S),fill=INK)
d.text((tx,512*S),'Relationship coach · Porto and online',font=F('figtree-latin-400-normal.woff2',27*S),fill=MUTED)
og.resize((1200,630),Image.LANCZOS).save(IMG+'og-image.jpg',quality=85,optimize=True,progressive=True)

# --- favicon mark: yellow circle + hand-drawn ink "T"
def bez(p0,p1,p2,p3,n=40):
    return [tuple(((1-t)**3*p0[i]+3*(1-t)**2*t*p1[i]+3*(1-t)*t*t*p2[i]+t**3*p3[i]) for i in (0,1)) for t in [k/n for k in range(n+1)]]
def mark(size,bg=None,pad=0):
    s=size*8; im=Image.new('RGBA',(s,s),bg or (0,0,0,0)); d=ImageDraw.Draw(im)
    k=s/32; o=pad*s
    sc=(s-2*o)/32
    P=lambda x,y:(o+x*sc,o+y*sc)
    d.ellipse((*P(1,1),*P(31,31)),fill=YEL)
    w=int(2.8*sc)
    for seg in (bez(P(8,11.5),P(12,10),P(19,9.6),P(24,10.6)), bez(P(16,10.4),P(15.4,15),P(15.6,19),P(16.6,23.5))):
        d.line(seg,fill=INK,width=w,joint='curve')
        for pt in (seg[0],seg[-1]): d.ellipse((pt[0]-w/2,pt[1]-w/2,pt[0]+w/2,pt[1]+w/2),fill=INK)
    return im.resize((size,size),Image.LANCZOS)
mark(32).save(IMG+'favicon-32.png')
mark(180,bg=PAPER+(255,),pad=0.12).convert('RGB').save(IMG+'apple-touch-icon.png')
mark(192,bg=PAPER+(255,),pad=0.12).convert('RGB').save(IMG+'icon-192.png')
mark(512,bg=PAPER+(255,),pad=0.12).convert('RGB').save(IMG+'icon-512.png')

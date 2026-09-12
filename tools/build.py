#!/usr/bin/env python3
"""Build the Decision Instrument identity from canonical geometry and tokens."""
from pathlib import Path
import hashlib, html, json, math, shutil, subprocess
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parents[1]
S = json.loads((ROOT/'assets/source/identity.json').read_text())
C, FONT, OUT = S['colors'], ROOT/'assets/fonts', ROOT/'production'
JOBS = []

def write(path, body):
    p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(body); return p

def svg(w,h,body,title='DecisionInvitation'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{html.escape(title)}</title>{body}</svg>'

def fonts():
    data=json.loads((FONT/'provenance.json').read_text())
    for name,entry in data['files'].items():
        if hashlib.sha256((FONT/name).read_bytes()).hexdigest()!=entry['sha256']:
            raise ValueError(f'Font source changed: {name}')
    for name,weight in [('Regular',400),('SemiBold',600)]:
        for ext in ('ttf','woff2'):
            f=TTFont(FONT/f'Sora-{name}.{ext}')
            assert 'fvar' not in f and f['OS/2'].usWeightClass==weight

def lettering(text,size,x,y,color,weight='Regular',tracking=0):
    f=TTFont(FONT/f'Sora-{weight}.ttf'); gs=f.getGlyphSet(); cm=f.getBestCmap()
    scale=size/f['head'].unitsPerEm; paths=[]; cursor=x
    for char in text:
        glyph=gs[cm[ord(char)]]; pen=SVGPathPen(gs)
        glyph.draw(TransformPen(pen,(scale,0,0,-scale,cursor,y)))
        if pen.getCommands(): paths.append(f'<path d="{pen.getCommands()}"/>')
        cursor+=glyph.width*scale+tracking
    return f'<g fill="{color}">{"".join(paths)}</g>',cursor-x

def mark(color,point,internal=None,micro=False):
    m=S['mark']; p=m['lineagePoint']
    outer=m['microOuterPaths' if micro else 'outerPaths']
    outer_width=m['microOuterStrokeWidth' if micro else 'outerStrokeWidth']
    paths=m['microInternalPaths' if micro else 'internalPaths']
    width=m['microInternalStrokeWidth' if micro else 'internalStrokeWidth']
    inner=internal or color
    shell=''.join(f'<path d="{path}"/>' for path in outer)
    detail=''.join(f'<path d="{path}"/>' for path in paths)
    return f'<g fill="none" stroke="{color}" stroke-width="{outer_width}" stroke-linecap="square" stroke-linejoin="miter">{shell}</g><g fill="none" stroke="{inner}" stroke-width="{width}" stroke-linecap="square" stroke-linejoin="miter">{detail}</g><path fill="{color}" d="{m["iBody"]}"/><circle fill="{point}" cx="{p["cx"]}" cy="{p["cy"]}" r="{p["r"]}"/>'

def raster(src,dst,width,background=None): JOBS.append({'src':str(src),'dst':str(dst),'width':width,'background':background})

def logos():
    variants={'primary':(C['register'],C['orange'],C['periwinkle']),'reverse':(C['white'],C['orange'],C['periwinkle']),'ink':(C['register'],C['register'],C['register']),'white':(C['white'],C['white'],C['white'])}
    for variant,(color,point,internal) in variants.items():
        word,ww=lettering('DecisionInvitation',66,0,78,color,'SemiBold',-1.4)
        lockword,lw=lettering('DecisionInvitation',66,165,96,color,'SemiBold',-1.4)
        first,_=lettering('Decision',70,0,0,color,'SemiBold',-1.2); second,_=lettering('Invitation',70,0,0,color,'SemiBold',-1.2)
        family={
          'mark':(256,256,mark(color,point,internal)), 'micro':(256,256,mark(color,point,internal,True)),
          'wordmark':(math.ceil(ww+8),104,f'<g transform="translate(4)">{word}</g>'),
          'lockup':(math.ceil(lw+178),146,f'<g transform="scale(.57)">{mark(color,point,internal)}</g>{lockword}'),
          'stacked':(420,400,f'<g transform="scale(.64)">{mark(color,point,internal)}</g><g transform="translate(16 245)">{first}</g><g transform="translate(16 319)">{second}</g>')}
        for kind,(w,h,body) in family.items():
            src=write(f'production/01-logo/svg/di-{kind}-{variant}.svg',svg(w,h,body))
            for width in ([256,1024] if kind in ('mark','micro') else [1200,2400]):
                raster(src,OUT/f'01-logo/png/di-{kind}-{variant}-{width}.png',width)
    shutil.copyfile(OUT/'01-logo/svg/di-mark-primary.svg',ROOT/'assets/logo/decisioninvitation-di-mark.svg')
    shutil.copyfile(OUT/'01-logo/svg/di-lockup-primary.svg',ROOT/'assets/logo/decisioninvitation-wordmark.svg')

def tokens():
    semantic={'surface':C['optic'],'surfaceAlternate':C['periwinkle'],'text':C['register'],'textMuted':'#5F5870','action':C['cobalt'],'onAction':C['white'],'focus':C['cobalt'],'signature':C['orange'],'border':'#AAB4F0','positive':'#176B58','warning':'#765313','error':'#A52B3A'}
    data={'system':{'name':S['name'],'version':S['version'],'status':S['status']},'primitive':{'color':C},'semantic':semantic,'component':{'button':{'minHeight':48,'background':'{semantic.action}','text':'{semantic.onAction}','radius':0},'input':{'minHeight':48,'focusWidth':2,'focusOffset':3}},'font':S['typography'],'space':[4,8,12,16,24,32,48,64,96,128],'type':{'caption':13,'body':17,'lead':24,'title':44,'display':104},'motion':S['motion']}
    write('assets/tokens/decisioninvitation.tokens.json',json.dumps(data,indent=2)+'\n')
    css='/* Generated. */\n:root {\n'+''.join(f'  --di-{k}: {v};\n' for k,v in C.items())+''.join(f'  --di-{k.replace("Alternate","-alternate").replace("Muted","-muted").replace("onAction","on-action")}: {v};\n' for k,v in semantic.items())+'  --di-font: "Sora", Arial, sans-serif;\n  --di-radius: 0;\n  --di-motion: 120ms;\n}\n'
    write('assets/tokens/decisioninvitation.tokens.css',css)

def applications():
    for size in (16,32,48,180,192,512,1024):
        body=f'<rect width="256" height="256" fill="{C["optic"]}"/><g transform="translate(19 10) scale(.85)">{mark(C["register"],C["orange"],C["periwinkle"],size<=32)}</g>'
        src=write(f'production/02-digital/di-icon-{size}.svg',svg(256,256,body)); raster(src,OUT/f'02-digital/di-icon-{size}.png',size)
    for variant in ('light','dark'):
        bg=C['optic'] if variant=='light' else C['register']; fg=C['register'] if variant=='light' else C['white']
        src=write(f'production/03-social/di-avatar-{variant}.svg',svg(1200,1200,f'<rect width="1200" height="1200" fill="{bg}"/><g transform="translate(244 216) scale(2.8)">{mark(fg,C["orange"],C["periwinkle"])}</g>'))
        raster(src,OUT/f'03-social/di-avatar-{variant}-1200.png',1200)
    for name,w,h in [('share-card',1200,630),('square',1200,1200),('portrait',1080,1350),('story',1080,1920),('header',2400,800),('presentation',1920,1080)]:
        body=f'<rect width="{w}" height="{h}" fill="{C["register"]}"/><rect x="{w*.58}" width="{w*.42}" height="{h}" fill="{C["cobalt"]}"/>'
        margin=w*.065; size=w*(.057 if w/h>2 else .082); y=h*.40
        for line in ('Catalyst','of analysis.'):
            text,_=lettering(line,size,margin,y,C['white'],'Regular',-size*.025); body+=text; y+=size
        label,_=lettering('DecisionInvitation',w*.021,margin,h-margin,C['white'],'SemiBold'); body+=label
        x=w*.63; yy=h*.5; gate=w*.88
        for i in (-2,-1,0,1,2): body+=f'<path d="M{x} {yy+i*h*.06}H{x+w*.07}L{gate-w*.018} {yy+i*h*.018}" fill="none" stroke="{C["periwinkle"]}" stroke-width="{max(3,w*.003)}"/>'
        body+=f'<path d="M{gate} {h*.24}V{h*.76}" stroke="{C["white"]}" stroke-width="{max(8,w*.012)}"/><circle cx="{gate+w*.055}" cy="{yy}" r="{w*.006}" fill="{C["orange"]}"/>'
        src=write(f'production/03-social/di-{name}.svg',svg(w,h,body,'DecisionInvitation. Catalyst of analysis.')); raster(src,OUT/f'03-social/di-{name}.png',w)
    body=f'<rect width="1800" height="1200" fill="{C["optic"]}"/><rect x="1160" width="640" height="1200" fill="{C["cobalt"]}"/>'
    text,_=lettering('Catalyst of analysis.',80,80,135,C['register']); body+=text
    text,_=lettering('DecisionInvitation / Decision instrument 0.3.2 / Design proposal',25,80,195,C['cobalt']); body+=text
    samples=[('Primary',C['white'],C['register']),('Reverse',C['register'],C['white']),('One color',C['periwinkle'],C['register'])]
    for i,(label,bg,fg) in enumerate(samples):
        x=80+i*565; inner=C['periwinkle'] if i<2 else fg; body+=f'<rect x="{x}" y="260" width="535" height="450" fill="{bg}"/><g transform="translate({x+127} 310) scale(1.1)">{mark(fg,C["orange"] if i<2 else fg,inner)}</g>'
        text,_=lettering(label,28,x+30,675,fg,'SemiBold'); body+=text
    for i,(name,value) in enumerate(C.items()):
        x=80+i*275; body+=f'<rect x="{x}" y="770" width="255" height="160" fill="{value}" stroke="{C["register"]}" stroke-width=".5"/>'
        text,_=lettering(name.title(),26,x,975,C['register'],'SemiBold'); body+=text
        text,_=lettering(value,22,x,1012,C['register']); body+=text
    text,_=lettering('Ask separately. Decide clearly.',45,80,1130,C['register']); body+=text
    src=write('production/05-proofs/identity-overview.svg',svg(1800,1200,body)); raster(src,OUT/'05-proofs/identity-overview.png',1800)

def render():
    for j in JOBS: Path(j['dst']).parent.mkdir(parents=True,exist_ok=True)
    program="const fs=require('node:fs'),sharp=require('sharp');const jobs=JSON.parse(fs.readFileSync(0,'utf8'));(async()=>{for(const j of jobs){let p=sharp(j.src,{density:144}).resize({width:j.width});if(j.background)p=p.flatten({background:j.background});await p.png().toFile(j.dst)}})().catch(e=>{console.error(e);process.exit(1)})"
    subprocess.run(['node','-e',program],input=json.dumps(JOBS),text=True,check=True)

def vector_pdfs():
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
    from reportlab import rl_config
    rl_config.invariant=True
    for source in sorted((OUT/'01-logo/svg').glob('*.svg')):
        target=OUT/'01-logo/pdf'/f'{source.stem}.pdf'; target.parent.mkdir(parents=True,exist_ok=True); renderPDF.drawToFile(svg2rlg(str(source)),str(target))

if __name__=='__main__':
    fonts(); logos(); tokens(); applications(); render(); vector_pdfs()
    from PIL import Image
    imgs=[Image.open(OUT/f'02-digital/di-icon-{s}.png') for s in (16,32,48)]
    imgs[-1].save(OUT/'02-digital/favicon.ico',format='ICO',sizes=[(16,16),(32,32),(48,48)],append_images=imgs[:-1])
    print(f'Built Multipath D identity, tokens and {len(JOBS)} raster exports.')

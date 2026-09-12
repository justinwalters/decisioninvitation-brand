#!/usr/bin/env python3
"""Rebuild the identity from geometry, licensed fonts and canonical tokens.
Requires requirements.txt, Node and sharp (NODE_PATH may locate a bundled copy).
"""
from pathlib import Path
import json, shutil, subprocess, html, math, hashlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parents[1]
S = json.loads((ROOT/'assets/source/identity.json').read_text())
C = S['colors']
FONT = ROOT/'assets/fonts'
OUT = ROOT/'production'
JOBS = []

def write(path, text):
    p = ROOT/path; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text)
    return p

def svg(w, h, content, title='DecisionInvitation'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{html.escape(title)}</title>{content}</svg>'

def fonts():
    # Preserve original upstream binaries and Reserved Font Names. Never convert,
    # subset, rename or synthesize distributed font software during the build.
    provenance=json.loads((FONT/'provenance.json').read_text())
    for name,entry in provenance['files'].items():
        actual=hashlib.sha256((FONT/name).read_bytes()).hexdigest()
        if actual != entry['sha256']:
            raise ValueError(f'Font source changed: {name}; verify upstream provenance')
    for name,weight in [('Regular',400),('Semibold',600)]:
        for extension in ['ttf','woff2']:
            f=TTFont(FONT/f'SourceSans3-{name}.{extension}')
            assert 'fvar' not in f
            assert f['name'].getDebugName(6)==f'SourceSans3-{name}'
            assert f['OS/2'].usWeightClass==weight

def lettering(text, size, x, y, color, weight='Regular', tracking=0):
    f=TTFont(FONT/f'SourceSans3-{weight}.ttf'); gs=f.getGlyphSet(); cm=f.getBestCmap()
    scale=size/f['head'].unitsPerEm; paths=[]; cursor=x
    for char in text:
        glyph=gs[cm[ord(char)]]; pen=SVGPathPen(gs)
        glyph.draw(TransformPen(pen,(scale,0,0,-scale,cursor,y)))
        if pen.getCommands(): paths.append(f'<path d="{pen.getCommands()}"/>')
        cursor+=glyph.width*scale+tracking
    return f'<g fill="{color}">{"".join(paths)}</g>', cursor-x

def mark(color, dot, micro=False):
    m=S['mark']; d=m['dot']
    return f'<path fill="{color}" fill-rule="evenodd" d="{m["microBody" if micro else "body"]}"/><circle fill="{dot}" cx="{d["cx"]}" cy="{d["cy"]}" r="{d["r"]}"/>'

def raster(src, dst, width, background=None):
    JOBS.append({'src':str(src),'dst':str(dst),'width':width,'background':background})

def logos():
    for variant,(color,dot) in {'primary':(C['ink'],C['orange']),'reverse':(C['paper'],C['orange']),'ink':(C['ink'],C['ink']),'white':(C['white'],C['white'])}.items():
        word,ww=lettering('DecisionInvitation',70,0,80,color,'Semibold',-1.1)
        lockword,lw=lettering('DecisionInvitation',70,165,99,color,'Semibold',-1.1)
        a,aw=lettering('Decision',74,0,0,color,'Semibold',-1)
        b,bw=lettering('Invitation',74,0,0,color,'Semibold',-1)
        variants={
          'mark':(256,256,mark(color,dot)),
          'micro':(256,256,mark(color,dot,True)),
          'wordmark':(math.ceil(ww+8),106,f'<g transform="translate(4 0)">{word}</g>'),
          'lockup':(math.ceil(lw+178),150,f'<g transform="translate(0 1) scale(.57)">{mark(color,dot)}</g>'+lockword),
          'stacked':(420,400,f'<g transform="translate(0 0) scale(.64)">{mark(color,dot)}</g><g transform="translate(16 245)">{a}</g><g transform="translate(16 321)">{b}</g>')}
        for kind,(w,h,body) in variants.items():
            p=write(f'production/01-logo/svg/di-{kind}-{variant}.svg',svg(w,h,body))
            for width in ([256,1024] if kind in ['mark','micro'] else [1200,2400]):
                raster(p,OUT/f'01-logo/png/di-{kind}-{variant}-{width}.png',width)
    # Legacy names retained as forwarding copies, never a second drawing.
    shutil.copyfile(OUT/'01-logo/svg/di-mark-primary.svg',ROOT/'assets/logo/decisioninvitation-di-mark.svg')
    shutil.copyfile(OUT/'01-logo/svg/di-lockup-primary.svg',ROOT/'assets/logo/decisioninvitation-wordmark.svg')

def tokens():
    semantic={'surface':C['paper'],'surfaceAlternate':C['mist'],'text':C['ink'],'textMuted':C['field'],'action':C['ink'],'onAction':C['paper'],'focus':C['ink'],'signature':C['orange'],'border':'#BAC8C4','positive':C['field'],'warning':'#71531A','error':'#A82C27'}
    d={'system':{'name':S['name'],'version':S['version'],'status':S['status']},'primitive':{'color':C},'semantic':semantic,'component':{'button':{'minHeight':48,'background':'{semantic.action}','text':'{semantic.onAction}','radius':3},'input':{'minHeight':48,'focusWidth':2,'focusOffset':4}},'font':S['typography'],'space':[4,8,12,16,24,32,48,64,96,128],'type':{'caption':14,'body':18,'lead':24,'title':40,'display':96},'motion':S['motion']}
    write('assets/tokens/decisioninvitation.tokens.json',json.dumps(d,indent=2)+'\n')
    css='/* Generated from assets/source/identity.json. Do not hand-edit. */\n:root {\n'
    css+=''.join(f'  --di-{k}: {v};\n' for k,v in C.items())
    css+=''.join(f'  --di-{k.replace("Alternate","-alternate").replace("Muted","-muted").replace("onAction","on-action")}: {v};\n' for k,v in semantic.items())
    css+='  --di-font: "Source Sans 3", Arial, sans-serif;\n  --di-mono: "IBM Plex Mono", monospace;\n  --di-radius: 3px;\n  --di-motion: 160ms;\n}\n'
    write('assets/tokens/decisioninvitation.tokens.css',css)

def applications():
    # Platform-neutral aspect masters; crop proofs are distinct from upload files.
    for size in [16,32,48,180,192,512,1024]:
        body=f'<rect width="256" height="256" fill="{C["paper"]}"/><g transform="translate(19 10) scale(.85)">{mark(C["ink"],C["orange"],size<=32)}</g>'
        p=write(f'production/02-digital/di-icon-{size}.svg',svg(256,256,body))
        raster(p,OUT/f'02-digital/di-icon-{size}.png',size)
    for variant in ['light','dark']:
        bg=C['paper'] if variant=='light' else C['ink']; fg=C['ink'] if variant=='light' else C['paper']
        body=f'<rect width="1200" height="1200" fill="{bg}"/><g transform="translate(244 216) scale(2.8)">{mark(fg,C["orange"])}</g>'
        p=write(f'production/03-social/di-avatar-{variant}.svg',svg(1200,1200,body))
        raster(p,OUT/f'03-social/di-avatar-{variant}-1200.png',1200)
    for name,w,h in [('share-card',1200,630),('square',1200,1200),('portrait',1080,1350),('story',1080,1920),('header',2400,800),('presentation',1920,1080)]:
        bg=C['ink']; body=f'<rect width="{w}" height="{h}" fill="{bg}"/>'
        margin=int(w*.065); size=w*.085 if w/h<1.1 else w*.076
        if w/h>2: size=w*.057
        y=h*.4 if h>w else h*.40
        for line in ['Catalyst','of analysis.']:
            text,_=lettering(line,size,margin,y,C['paper'],'Regular',-size*.025); body+=text; y+=size*.99
        label,_=lettering('DecisionInvitation',w*.022,margin,h-margin,C['paper'],'Semibold'); body+=label
        body+=f'<g transform="translate({w-margin-w*.08} {margin*.5}) scale({w*.08/256})">{mark(C["paper"],C["orange"])}</g>'
        # Parallel contributions resolve into one forward path. Illustrative brand device, not product data.
        x=w*.66; yy=h*.45; span=w*.2
        for i in [-2,-1,0,1,2]:
            body+=f'<path d="M{x} {yy+i*h*.045}H{x+span*.28} Q{x+span*.45} {yy+i*h*.045} {x+span*.55} {yy} H{w-margin}" fill="none" stroke="{C["field"]}" stroke-width="{max(2,w*.0015)}"/>'
        body+=f'<circle cx="{w-margin}" cy="{yy}" r="{w*.006}" fill="{C["orange"]}"/>'
        p=write(f'production/03-social/di-{name}.svg',svg(w,h,body,'DecisionInvitation. Catalyst of analysis.'))
        raster(p,OUT/f'03-social/di-{name}.png',w)
    # Contact sheet is a review proof, never a source for recreating artwork.
    body=f'<rect width="1800" height="1200" fill="{C["paper"]}"/>'
    t,_=lettering('Catalyst of analysis.',80,80,135,C['ink']);body+=t
    t,_=lettering('DecisionInvitation / Identity system 0.2 / Design proposal',25,80,195,C['ink']);body+=t
    for i,(variant,bg,fg) in enumerate([('Primary',C['white'],C['ink']),('Reverse',C['ink'],C['paper']),('One color',C['mist'],C['ink'])]):
        x=80+i*565; body+=f'<rect x="{x}" y="260" width="535" height="450" fill="{bg}"/><g transform="translate({x+127} 310) scale(1.1)">{mark(fg,C["orange"] if i<2 else fg)}</g>'
        t,_=lettering(variant,28,x+30,675,fg);body+=t
    for i,(name,hexv) in enumerate(C.items()):
        x=80+i*275; body+=f'<rect x="{x}" y="770" width="255" height="160" fill="{hexv}" stroke="{C["ink"]}" stroke-width=".5"/>'
        t,_=lettering(name.title(),26,x,975,C['ink']);body+=t
        t,_=lettering(hexv,22,x,1012,C['ink']);body+=t
    t,_=lettering('Ask separately. Decide clearly.',45,80,1130,C['ink']);body+=t
    p=write('production/05-proofs/identity-overview.svg',svg(1800,1200,body,'DecisionInvitation identity overview'))
    raster(p,OUT/'05-proofs/identity-overview.png',1800)

def render():
    for j in JOBS: Path(j['dst']).parent.mkdir(parents=True,exist_ok=True)
    program='''const fs=require('node:fs'); const sharp=require('sharp'); const jobs=JSON.parse(fs.readFileSync(0,'utf8')); (async()=>{for(const j of jobs){let p=sharp(j.src,{density:144}).resize({width:j.width}); if(j.background)p=p.flatten({background:j.background});await p.png().toFile(j.dst)}})().catch(e=>{console.error(e);process.exit(1)})'''
    subprocess.run(['node','-e',program],input=json.dumps(JOBS),text=True,check=True)

def vector_pdfs():
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
    from reportlab import rl_config
    rl_config.invariant=True
    for source in sorted((OUT/'01-logo/svg').glob('*.svg')):
        target=OUT/'01-logo/pdf'/f'{source.stem}.pdf'
        target.parent.mkdir(parents=True,exist_ok=True)
        renderPDF.drawToFile(svg2rlg(str(source)),str(target))

if __name__=='__main__':
    fonts(); logos(); tokens(); applications(); render(); vector_pdfs()
    from PIL import Image
    imgs=[Image.open(OUT/f'02-digital/di-icon-{s}.png') for s in [16,32,48]]
    imgs[-1].save(OUT/'02-digital/favicon.ico',format='ICO',sizes=[(16,16),(32,32),(48,48)],append_images=imgs[:-1])
    print(f'Built logo family, tokens and {len(JOBS)} raster exports; verified original licensed fonts.')

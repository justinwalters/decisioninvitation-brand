#!/usr/bin/env python3
"""Build the 16-page Decision Instrument identity manual."""
from pathlib import Path
import json
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf/decisioninvitation-identity-manual.pdf'
S=json.loads((ROOT/'assets/source/identity.json').read_text())
C={k:HexColor(v) for k,v in S['colors'].items()}
W,H=960,600; M=56
pdfmetrics.registerFont(TTFont('Sora',str(ROOT/'assets/fonts/Sora-Regular.ttf')))
pdfmetrics.registerFont(TTFont('SoraSemi',str(ROOT/'assets/fonts/Sora-SemiBold.ttf')))
OUT.parent.mkdir(parents=True,exist_ok=True)
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1,invariant=1)
c.setTitle('DecisionInvitation Corporate Identity 0.3.1')
c.setAuthor('DecisionInvitation')
c.setSubject('Decision Instrument identity proposal; owner review pending')

def txt(value,x,y,size=18,color='register',font='Sora',leading=1.15):
    c.setFillColor(C[color]); c.setFont(font,size)
    for i,item in enumerate(value.split('\n')): c.drawString(x,H-y-size-i*size*leading,item)

def wrap(value,x,y,width,size=16,color='register',font='Sora',leading=1.35):
    lines=[]
    for paragraph in value.split('\n'):
        current=''
        for word in paragraph.split():
            trial=(current+' '+word).strip()
            if c.stringWidth(trial,font,size)<=width: current=trial
            else: lines.append(current); current=word
        lines.append(current)
    txt('\n'.join(lines),x,y,size,color,font,leading)

def rect(x,y,w,h,color):
    c.setFillColor(C[color]); c.rect(x,H-y-h,w,h,fill=1,stroke=0)

def line(x1,y1,x2,y2,color='cobalt',weight=1):
    c.setStrokeColor(C[color]); c.setLineWidth(weight); c.line(x1,H-y1,x2,H-y2)

def mark(x,y,scale=1,body='register',point='orange',internal='periwinkle',background='optic'):
    p=c.beginPath()
    p.moveTo(x+20*scale,H-(y+28*scale)); p.lineTo(x+96*scale,H-(y+28*scale))
    p.curveTo(x+157*scale,H-(y+28*scale),x+195*scale,H-(y+67*scale),x+195*scale,H-(y+128*scale))
    p.curveTo(x+195*scale,H-(y+189*scale),x+157*scale,H-(y+228*scale),x+96*scale,H-(y+228*scale))
    p.lineTo(x+20*scale,H-(y+228*scale)); p.close()
    c.setFillColor(C[body]); c.drawPath(p,fill=1,stroke=0)
    q=c.beginPath(); q.moveTo(x+58*scale,H-(y+64*scale)); q.lineTo(x+96*scale,H-(y+64*scale))
    q.curveTo(x+134*scale,H-(y+64*scale),x+158*scale,H-(y+88*scale),x+158*scale,H-(y+128*scale))
    q.curveTo(x+158*scale,H-(y+168*scale),x+134*scale,H-(y+192*scale),x+96*scale,H-(y+192*scale))
    q.lineTo(x+58*scale,H-(y+192*scale)); q.close()
    c.setFillColor(C[background]); c.drawPath(q,fill=1,stroke=0)
    c.setFillColor(C[body]); c.rect(x+204*scale,H-(y+228*scale),24*scale,122*scale,fill=1,stroke=0)
    c.setStrokeColor(C[internal]); c.setLineWidth(7*scale)
    for sy,cy,ey in ((88,88,120),(128,128,128),(168,168,136)):
        r=c.beginPath(); r.moveTo(x+70*scale,H-(y+sy*scale)); r.lineTo(x+98*scale,H-(y+sy*scale))
        r.curveTo(x+119*scale,H-(y+cy*scale),x+135*scale,H-(y+ey*scale),x+151*scale,H-(y+ey*scale))
        c.drawPath(r,fill=0,stroke=1)
    c.setFillColor(C[point]); c.circle(x+216*scale,H-(y+72*scale),12*scale,fill=1,stroke=0)

def page(n,section,dark=False):
    if n>1: c.showPage()
    rect(0,0,W,H,'register' if dark else 'optic'); fg='white' if dark else 'register'
    txt('DECISIONINVITATION',M,26,10,fg,'SoraSemi'); txt('IDENTITY MANUAL / 0.3.1',704,26,10,'periwinkle' if dark else 'cobalt','SoraSemi')
    line(M,558,W-M,558,'periwinkle' if dark else 'cobalt',.6)
    txt('0.3.1 / DESIGN PROPOSAL / OWNER REVIEW PENDING',M,571,8,fg)
    txt(f'{n:02d} / 16',852,571,8,fg)

def heading(kicker,title,deck='',dark=False):
    fg='white' if dark else 'register'
    txt(kicker.upper(),M,75,11,'periwinkle' if dark else 'cobalt','SoraSemi')
    txt(title,M,108,48,fg,'SoraSemi',1.03)
    if deck: wrap(deck,M,222,760,18,fg)

page(1,'Corporate identity / 2026',True)
rect(612,0,348,H,'cobalt'); mark(648,134,1.05,'white','orange','periwinkle','cobalt')
txt('Catalyst of\nanalysis.',M,150,75,'white','SoraSemi',.98)
txt('BETTER INPUT. CLEARER DECISIONS.',M,410,13,'periwinkle','SoraSemi')
wrap('A standalone identity for turning thoughtful analysis into a clear next move.',M,455,470,20,'white')

PAGES=[
('01 / Strategic thesis','Thought is not the problem.','Thought without a threshold is.','DecisionInvitation gives analysis a purpose: frame the question, invite perspectives separately, and expose what is sufficient to move. The owner keeps the responsibility.'),
('02 / Positioning','A decision instrument.','Not a poll. Not consensus theater. Not a corporate memo.','For people responsible for a consequential choice, DecisionInvitation turns distributed judgment into a legible next move.'),
('03 / Verbal core','Language with momentum.','Keep the first-page language. Build the identity around its tension.','Catalyst of analysis.\n\nBetter input. Clearer decisions.\n\nA quieter way to decide.\n\nAsk separately. Decide clearly.'),
('04 / Brand character','Exact. Calm. Decisive.','Clarity without coldness; confidence without coercion.','Use short sentences, concrete verbs, and visible responsibility. Never imply that the system decides, guarantees consensus, or removes accountability.'),
('05 / Logo idea','The Multipath D.','Recognition first. Meaning inside.','A strongly defined D carries the name at a glance. Fine paths inside its counter retain multiple perspectives. A separate lowercase i carries one orange provenance dot.'),
('06 / Logo system','Built for recognition.','One master, one micro cut, four colorways.','Use the supplied vectors. Primary is Register with Periwinkle paths and an orange i dot. One-color applications preserve hierarchy through weight. Never redraw or decorate it.'),
('07 / Clear space and scale','Give the decision room.','Clear space equals 32 source units.','Master mark: 24 px minimum. Micro mark: 16 px minimum. Lockup: 144 px minimum. At small sizes use the micro cut; never reduce the orange i dot below two device pixels.'),
('08 / Color','A cool instrument panel.','Cobalt creates active structure. Register carries authority.','Optic is the working surface. Periwinkle separates fields. White opens space. Orange is lineage only: no buttons, backgrounds, charts, or status semantics; maximum 2% of a composition.'),
('09 / Typography','One family. One voice.','Sora creates a technical humanism distinct from the parent brand.','Use Regular for reading and large statements. Use SemiBold for the wordmark, navigation, labels, and decisive emphasis. Avoid all-caps paragraphs, faux italics, and decorative tracking.'),
('10 / Graphic grammar','Paths. Counters. Evidence.','The system should feel like information becoming actionable.','Use fine analytical paths inside strong structural fields. Keep the D silhouette dominant, corners exact, and hierarchy legible. No gradients, floating cards, blobs, or editorial chapter-number theater.'),
('11 / Layout','Split the field with purpose.','Use asymmetric planes, hard alignment, and generous empty space.','A typical composition reserves 58% for the question and 42% for the commitment field. Break the ratio only to improve comprehension, never for decoration.'),
('12 / Voice','Invite, then clarify.','Warm enough to answer. Exact enough to trust.','Preferred: Invite the perspectives. Keep the responsibility.\nAvoid: Let AI make the decision.\n\nPreferred: Here is what would change the call.\nAvoid: Everyone agrees.'),
('13 / Product moments','Show the decision state.','Every message answers: what is asked, why me, who can see it, what happens next?','Use real workflow language and explicit privacy boundaries. A completed invitation is not a completed decision. A recommendation is not authorization.'),
('14 / Motion','Paths, then signature.','Motion explains the system rather than decorating it.','Internal paths settle independently over 260 ms; the D remains fixed; the orange i dot appears last. Respect reduced-motion by showing the final state with no transition.'),
('15 / Brand architecture','Standalone first. Provenance last.','DecisionInvitation is the visible product brand.','Use “an aSUKIra company” only in legal, about, or footer contexts. Never co-lock the marks. Never borrow the parent palette, typography, voice structure, or signature composition.'),
]
for n,(section,title,deck,body) in enumerate(PAGES,2):
    dark=n in (3,7,13,16); page(n,section,dark); heading(section,title,deck,dark)
    fg='white' if dark else 'register'; wrap(body,M,320,520,20,fg)
    if n==6: mark(668,275,.75,'white' if dark else 'register','orange','periwinkle','register' if dark else 'optic')
    elif n==9:
        for i,(name,col) in enumerate([('Register','register'),('Cobalt','cobalt'),('Periwinkle','periwinkle'),('Optic','optic'),('Orange','orange')]):
            xx=626+i%2*138; yy=292+i//2*88; rect(xx,yy,122,70,col); txt(name,xx,yy+74,9,fg,'SoraSemi')
    else:
        for i in range(3): line(654,330+i*48,774,378,'periwinkle' if dark else 'cobalt',2)
        line(800,285,800,460,'white' if dark else 'register',9)
        c.setFillColor(C['orange']); c.circle(845,H-378,5,fill=1,stroke=0)
c.save()
print(f'Built {OUT} (16 pages).')

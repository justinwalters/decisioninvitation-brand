#!/usr/bin/env python3
"""Build the review identity manual from canonical local assets.

Run from any directory: .venv/bin/python tools/build_manual.py
Requires reportlab and svglib. No network or system font dependency.
"""
from pathlib import Path
import json
from xml.sax.saxutils import escape

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf/decisioninvitation-identity-manual.pdf"
SOURCE = json.loads((ROOT / "assets/source/identity.json").read_text())
COLORS = SOURCE["colors"]
W, H = 960, 600
M = 52

for name, filename in (("Source", "SourceSans3-Regular.ttf"),
                       ("SourceSemi", "SourceSans3-Semibold.ttf"),
                       ("Plex", "IBMPlexMono-Regular.ttf")):
    pdfmetrics.registerFont(TTFont(name, str(ROOT / "assets/fonts" / filename)))

# ReportLab deduplicates faces by internal PostScript name, not file name.
# Supplied static font weights must carry distinct internal names.
if pdfmetrics.getFont("Source").face.name == pdfmetrics.getFont("SourceSemi").face.name:
    raise ValueError("Source Sans 3 static weights need distinct internal PostScript names")

OUT.parent.mkdir(parents=True, exist_ok=True)
C = canvas.Canvas(str(OUT), pagesize=(W, H), pageCompression=1, invariant=1)
C.setTitle("DecisionInvitation - Corporate identity proposal 0.2.0")
C.setAuthor("DecisionInvitation")
C.setSubject("Catalyst of analysis. Open frame identity proposal, pending owner review.")
PAGE = 0
THEME = "paper"


def color(name):
    return HexColor(COLORS.get(name, name))


def rect(x, top, width, height, fill, stroke=None, line=1):
    C.setFillColor(color(fill))
    C.setStrokeColor(color(stroke or fill))
    C.setLineWidth(line)
    C.rect(x, H-top-height, width, height, fill=1, stroke=bool(stroke))


def line(x1, y1, x2, y2, stroke="ink", width=1):
    C.setStrokeColor(color(stroke))
    C.setLineWidth(width)
    C.line(x1, H-y1, x2, H-y2)


def dot(x, top, radius=5, fill="orange"):
    C.setFillColor(color(fill))
    C.circle(x, H-top, radius, fill=1, stroke=0)


def text(value, x, top, size=16, font="Source", fill=None):
    fill = fill or ("paper" if THEME == "ink" else "ink")
    C.setFillColor(color(fill))
    C.setFont(font, size)
    for i, value_line in enumerate(str(value).split("\n")):
        C.drawString(x, H-top-size*.79-i*size*1.05, value_line)


def label(value, x, top, fill=None, size=10):
    text(value.upper(), x, top, size, "Plex", fill)


def para(value, x, top, width, size=17, leading=None, fill=None, max_height=None, font="Source"):
    fill = fill or ("paper" if THEME == "ink" else "ink")
    value = value.replace("—", " - ").replace("–", "-").replace("‑", "-")
    style = ParagraphStyle("p", fontName=font, fontSize=size, leading=leading or size*1.3,
                           textColor=color(fill), spaceAfter=0, allowWidows=0, allowOrphans=0)
    p = Paragraph(escape(value).replace("\n", "<br/>"), style)
    _, height = p.wrap(width, H)
    if max_height is not None and height > max_height + .5:
        raise ValueError(f"Page {PAGE}: paragraph overflow {height:.1f}>{max_height}: {value[:70]}")
    if top + height > 548:
        raise ValueError(f"Page {PAGE}: paragraph crosses footer: {value[:70]}")
    p.drawOn(C, x, H-top-height)
    return height


def asset(name, x, top, width, max_height=None):
    drawing = svg2rlg(str(ROOT / "production/01-logo/svg" / f"{name}.svg"))
    scale = width / drawing.width
    if max_height is not None:
        scale = min(scale, max_height/drawing.height)
    drawing.scale(scale, scale)
    renderPDF.draw(drawing, C, x, H-top-drawing.height*scale)


def frame(x, top, width, height, fill="ink", opening=.22, weight=1.5):
    """Open on the right: a composed space with a deliberate way through."""
    gap = height*opening
    line(x, top, x+width, top, fill, weight)
    line(x, top, x, top+height, fill, weight)
    line(x, top+height, x+width, top+height, fill, weight)
    line(x+width, top, x+width, top+(height-gap)/2, fill, weight)
    line(x+width, top+(height+gap)/2, x+width, top+height, fill, weight)


def page(section, theme="paper"):
    global PAGE, THEME
    if PAGE:
        C.showPage()
    PAGE += 1
    THEME = theme
    rect(0, 0, W, H, theme)
    fg = "paper" if theme == "ink" else "ink"
    label("DecisionInvitation / Identity", M, 28, fg)
    label(section, 542, 28, fg)
    line(M, 559, W-M, 559, "field", .5)
    label("0.2.0 / Visual proposal / Owner review pending", M, 574, fg, 8)
    label(f"{PAGE:02d} / 16", W-104, 574, fg, 8)


def title(kicker, heading, sub=None, size=49):
    label(kicker, M, 81, "field" if THEME != "ink" else "mist")
    text(heading, M, 109, size)
    if sub:
        para(sub, M, 169, 790, 17, max_height=56)


def rule_row(y, left, right, x=M, width=856, split=320, size=16):
    line(x, y, x+width, y, "field", .4)
    para(left, x, y+10, split-24, size, max_height=48, font="SourceSemi")
    para(right, x+split, y+10, width-split, size, max_height=48)


# 01 / A brand moment, not a document title card.
page("Corporate identity / 2026", "ink")
asset("di-lockup-reverse", M, 66, 245)
text("Catalyst of\nanalysis.", M, 185, 104)
frame(702, 149, 204, 293, "field", .23, 1.5)
asset("di-mark-reverse", 714, 220, 165)
para("Turn thoughtful analysis into a clear next move.", M, 438, 550, 23, max_height=40)
label("Strategy, identity, applications, governance", M, 513, "mist")

# 02 / Strategic thesis.
page("01 / The point")
title("The problem is not thought.", "It is thought with nowhere to go.", size=47)
para("DecisionInvitation gives analysis a purpose: a clear question, independent perspectives, and a next move the owner can stand behind.", M, 177, 650, 23, max_height=92)
rect(M, 307, 405, 171, "mist")
label("Paralysis of analysis", M+22, 327, "field")
text("More input. Same circle.", M+22, 358, 28)
para("The question widens. The room converges. The owner still cannot see what would change the call.", M+22, 400, 350, 17, max_height=66)
rect(478, 307, 430, 171, "ink")
label("Catalyst of analysis", 500, 327, "mist")
text("A question. A way forward.", 500, 358, 28, fill="paper")
para("A decision, a condition to satisfy, or a missing fact to establish. Forward motion does not mean rushing judgment.", 500, 400, 365, 17, fill="paper", max_height=66)
para("The owner makes the call. Perspectives inform it; the product does not manufacture consensus.", M, 511, 820, 17, max_height=32)

# 03 / Position and audience.
page("02 / Positioning")
title("The product in one sentence", "A clearer next move.")
para("For people responsible for a consequential choice, DecisionInvitation frames the question, invites perspectives separately, and makes the reasoning useful.", M, 189, 393, 25, max_height=199)
para("Its identity must be purposeful, exact, open, and accountable - established in its own right, with one quiet trace of aSUKIra.", M, 419, 383, 18, max_height=91)
audiences = [
    ("01 / Decision owner", "Help me see what would move the question forward. Keep the final call mine."),
    ("02 / Invited contributor", "Tell me why my view matters, what is being asked, and who can see my response."),
    ("03 / Organizational reader", "Show a credible workflow and explicit operating boundaries before ambitious claims."),
]
for i, (a, b) in enumerate(audiences):
    y = 185+i*112
    line(498, y, 908, y, "field", .6)
    label(a, 498, y+15, "field")
    para(b, 498, y+42, 405, 18, max_height=56)

# 04 / User-valued verbal foundation.
page("03 / Verbal foundation", "ink")
label("The core idea", M, 81, "mist")
text("Catalyst of analysis.", M, 112, 61)
para("A strategic idea alongside the warm product language the user values. It does not require replacing the existing homepage headline.", M, 194, 805, 19, max_height=56)
line(M, 274, 908, 274, "field", .7)
text("Better input.\nClearer decisions.", M, 309, 47)
para("A quieter way to decide\nAsk separately. Decide clearly.", 510, 310, 355, 25, leading=34, max_height=84)
para("Invite the perspectives.\nKeep the responsibility.", 510, 421, 355, 25, leading=34, max_height=84)
label("There is a decision waiting for a better question.", M, 510, "mist", 10)

# 05 / Creative exploration.
page("04 / Creative territories")
title("Three routes. One recommendation.", "Open frame.", "A held question, separate perspectives, and a deliberate way through.")
territories = [
    (M, "01 / Open frame", "Structure creates a way forward.", "Distinctive in one color; flexible from a favicon to an editorial page. Recommended for development.", "Recommended / proposed"),
    (346, "02 / Considered exchange", "Many perspectives, one responsible call.", "An exchange-led system would emphasize contributions. Risk: looking like chat, polling, or a social network.", "Explored / not selected"),
    (640, "03 / Decision correspondence", "A question worth responding to.", "An invitation-led editorial system could feel highly personal. Risk: resembling notices or formal/legal stationery.", "Explored / not selected"),
]
for x, heading, claim, body, state in territories:
    rect(x, 237, 268, 287, "mist" if x == M else "white")
    label(heading, x+18, 256, "field", 9)
    if x == M:
        frame(x+23, 290, 71, 51, "ink", .22, 2)
        dot(x+97, 315, 4)
    elif x == 346:
        for j in range(3):
            line(x+24, 297+j*15, x+75+j*15, 297+j*15, "field", 2)
    else:
        line(x+24, 291, x+104, 291, "ink", 2)
        line(x+24, 308, x+80, 308, "field", 1)
        line(x+24, 324, x+94, 324, "field", 1)
    para(claim, x+18, 361, 230, 22, max_height=60)
    para(body, x+18, 426, 230, 15, max_height=78)
    label(state, x+18, 509, "field", 7)

# 06 / Exact master construction.
page("05 / Mark construction")
title("A sign of its own", "One opening. One orange point.", "Use the supplied vector. These measurements describe the master; they are not an invitation to redraw it.", 45)
rect(M, 235, 367, 284, "white")
# 256-unit master at 0.9 scale, with clear space around visible bounds.
gx, gy, scale = 113, 248, .9
for q in range(0, 257, 32):
    line(gx+q*scale, gy, gx+q*scale, gy+256*scale, "mist", .5)
    line(gx, gy+q*scale, gx+256*scale, gy+q*scale, "mist", .5)
asset("di-mark-primary", gx, gy, 256*scale)
C.setDash(3, 3)
line(gx-12*scale, gy+4*scale, gx+266*scale, gy+4*scale, "field", .7)
line(gx-12*scale, gy+260*scale, gx+266*scale, gy+260*scale, "field", .7)
line(gx-12*scale, gy+4*scale, gx-12*scale, gy+260*scale, "field", .7)
line(gx+266*scale, gy+4*scale, gx+266*scale, gy+260*scale, "field", .7)
C.setDash()
label("x = 36 / point diameter", M+24, 495, "field", 9)
specs = [
    ("Master", "256 x 256 coordinate field"),
    ("D", "x 24-178 / y 40-224 / 34-unit aperture"),
    ("i", "32 x 114 stem / point radius 18"),
    ("Clear space", "x beyond the visible artwork, on every side"),
    ("Small sizes", "Main from 24 px; micro preferred at 16-32 px"),
    ("Micro distinction", "Closed D aperture and a stronger i stem"),
]
for i, (a, b) in enumerate(specs):
    y = 237+i*46
    line(462, y, 908, y, "field", .4)
    text(a, 462, y+10, 15, "SourceSemi")
    para(b, 588, y+10, 320, 15, max_height=40)

# 07 / Variants and responsive reduction.
page("06 / Signature family")
title("A complete working set", "Recognizable in every register.", size=46)
variants = [(M, 192, "paper", "primary", "Primary / light fields"),
            (490, 192, "ink", "reverse", "Reverse / Ink field"),
            (M, 322, "mist", "ink", "One color / Ink"),
            (490, 322, "ink", "white", "One color / White")]
for x, y, bg, variant, caption in variants:
    rect(x, y, 418, 114, bg, "mist" if bg != "ink" else None)
    label(caption, x+18, y+13, "paper" if bg == "ink" else "field", 8)
    asset(f"di-lockup-{variant}", x+25, y+41, 362, 63)
label("Responsive use", M, 469, "field")
for x, s, name in [(259, 16, "micro"), (343, 24, "micro"), (428, 32, "micro"), (521, 48, "mark")]:
    asset(f"di-{name}-primary", x, 477, s)
    label(f"{s} px", x, 529, "field", 7)
para("Full name at first contact.\nDo not crop or reassemble.", 650, 478, 255, 18, max_height=56)

# 08 / Palette.
page("07 / Color system")
title("A field for considered work", "Quiet by proportion.", "Orange is the family trace. Ink, Paper, and a particular green-gray world make the product its own.")
swatches = [("ink", "Decision Ink", "Anchor / primary text", 269), ("paper", "Paper", "Main reading field", 192),
            ("mist", "Mist", "Supporting structure", 145), ("field", "Field Green", "Secondary expression", 105),
            ("orange", "Signal Orange", "Point / scarce accent", 76), ("white", "White", "Utility contrast", 69)]
x = M
for key, name, role, width in swatches:
    rect(x, 233, width, 213, key, "mist" if key in ("paper", "white") else None)
    x += width
for i, (key, name, role, width) in enumerate(swatches):
    x = M + (i % 3)*294
    y = 466+(i//3)*39
    dot(x+5, y+6, 4, key)
    text(name, x+19, y, 15, "SourceSemi")
    label(COLORS[key], x+183, y+3, "field", 8)
    text(role, x+19, y+18, 11)

# 09 / Accessibility by measured pairs.
page("08 / Color in use")
title("Measured, not assumed", "Restraint makes it work.", "Contrast values below are calculated from the exact solid sRGB colors. Changing opacity or background changes the result.", 46)
rows = [("Ink / Paper", "13.31 : 1", "Reading / pass"), ("Ink / Mist", "12.21 : 1", "Reading / pass"),
        ("Green / White", "5.03 : 1", "Reading / pass"), ("Green / Paper", "4.57 : 1", "Reading / no opacity"),
        ("Orange / White", "4.33 : 1", "Not normal text"), ("Orange / Paper", "3.93 : 1", "Not normal text"),
        ("Green / Mist", "4.19 : 1", "Not normal text")]
for i, (a, b, d) in enumerate(rows):
    y = 236+i*39
    line(M, y, 555, y, "field", .4)
    text(a, M, y+11, 15, "SourceSemi")
    text(b, 254, y+11, 14, "Plex")
    text(d, 385, y+11, 14)
rect(602, 235, 306, 276, "white")
label("A clear action", 625, 258, "field")
text("Review the question", 625, 295, 25)
para("Use Ink for the primary action. Explain states with words, not color alone.", 625, 338, 257, 18, max_height=73)
rect(625, 433, 182, 43, "ink")
text("Read the question", 641, 445, 17, "SourceSemi", "white")
para("4.5:1 normal text; 3:1 large text and essential graphics. Logo exemption is not a rule for UI text. This is a pairing check, not a certification.", M, 523, 856, 12, max_height=28)

# 10 / Type.
page("09 / Typography")
label("Source Sans 3 / 400 + 600", M, 81, "field")
text("Better input.\nClearer decisions.", M, 128, 75)
para("Warm enough to invite a perspective. Precise enough to carry the reasoning.", M, 320, 540, 27, max_height=82)
label("IBM Plex Mono / 400", 668, 91, "field")
text("01 / QUESTION\n02 / PERSPECTIVE\n03 / NEXT MOVE", 668, 137, 17, "Plex")
para("Utility, not personality by volume. Use for labels, dates, identifiers, and measured information.", 668, 230, 226, 17, max_height=108)
line(M, 436, 908, 436, "field", .7)
scale_rows = [(M, "Display", "88-120 px", "400 / editorial"), (275, "Section", "40-64 px", "400 or 600"),
              (498, "Body", "18-20 px", "400 / 1.5-1.65"), (721, "Utility", "11-13 px", "400 / short labels")]
for x, a, b, d in scale_rows:
    label(a, x, 457, "field")
    text(b, x, 482, 25)
    text(d, x, 518, 15)

# 11 / Graphic grammar and motion.
page("10 / Graphic grammar", "ink")
title("Structure can create movement", "Hold the question. Leave a way through.", size=41)
steps = [(M, "01 / QUESTION", "What needs\ndeciding?"), (346, "02 / PERSPECTIVE", "What would\nchange your view?"), (640, "03 / NEXT MOVE", "What is now\npossible?")]
for x, a, b in steps:
    frame(x, 217, 246, 176, "field", .22, 1.5)
    label(a, x+18, 240, "mist", 9)
    text(b, x+18, 285, 29)
dot(914, 305, 5)
para("One dominant frame. One deliberate opening. The device carries composition, not simulated product state. A framing line is not an input border.", M, 427, 526, 20, max_height=87)
label("Motion, when useful", 640, 429, "mist")
para("160 ms feedback / 320 ms transition\nNo pulsing mark. No looping urgency.\nReduced motion: static final state.", 640, 459, 268, 15, leading=21, max_height=67)

# 12 / Voice in the real task.
page("11 / Voice and microcopy")
title("Purposeful. Exact. Open. Accountable.", "An invitation, not pressure.", size=46)
rect(M, 194, 492, 323, "white")
label("Illustrative invitation / not a live workflow", M+24, 216, "field", 8)
text("What would change your view?", M+24, 253, 32)
para("Morgan is asking for your perspective on the proposed launch date. What supports the date, and what condition would make you change it?", M+24, 305, 438, 22, max_height=115)
line(M+24, 433, 520, 433, "mist", 1)
para("Visibility and deadline language must match the actual invitation. Supply the authorized audience before publishing.", M+24, 452, 435, 16, max_height=51)
pairs = [("Instead of", "Help us confirm the right answer.", "Make room for disagreement."),
         ("Instead of", "Decide instantly. Get perfect clarity.", "Name the fact you still need."),
         ("Instead of", "The platform makes the decision.", "The owner makes the call.")]
for i, (a, b, d) in enumerate(pairs):
    y = 198+i*106
    label(a, 595, y, "field", 9)
    para(b, 595, y+23, 310, 17, max_height=46)
    para(d, 595, y+70, 310, 17, max_height=28, font="SourceSemi")

# 13 / Designed applications, explicitly illustrative.
page("12 / Applied identity")
title("A system beyond the logo", "One product. Many useful surfaces.", size=45)
rect(M, 185, 546, 340, "white", "mist")
asset("di-lockup-primary", M+24, 206, 180)
line(M+24, 252, 574, 252, "mist", .7)
text("Better input.\nClearer decisions.", M+24, 282, 43)
para("Frame the question. Invite perspectives separately. Understand the reasoning.", M+24, 395, 360, 18, max_height=52)
rect(M+24, 470, 135, 30, "ink")
text("Illustrative action", M+36, 477, 13, "SourceSemi", "white")
frame(500, 310, 67, 123, "field", .23, 1)
rect(626, 185, 282, 159, "ink")
asset("di-mark-reverse", 646, 204, 56)
text("DecisionInvitation", 646, 280, 21, "SourceSemi", "paper")
label("decisioninvitation.com", 646, 316, "mist", 8)
rect(626, 365, 282, 160, "mist")
label("An editorial campaign", 646, 386, "field", 8)
text("Catalyst of\nanalysis.", 646, 420, 37)
dot(878, 491, 5)
label("Layout specimens / not deployed pages or contact records", M, 537, "field", 8)

# 14 / Channel and architecture.
page("13 / Channels and lineage")
title("Established on its own", "Related. Not dependent.", size=50)
para("The orange point is enough to reward a closer look. DecisionInvitation does not need a parent badge in its primary signature, navigation, avatar, or call to action.", M, 188, 438, 22, max_height=145)
asset("di-lockup-primary", M, 351, 382)
line(M, 453, 490, 453, "field", .5)
label("Optional, factual footer attribution", M, 472, "field", 8)
text("A product in the aSUKIra family", M, 494, 17)
channel_rows = [("Website", "Product first. Public /brand reference with downloads, version, and honest status."),
                ("Social", "Recompose for the actual crop. One idea, one signature, readable on a phone."),
                ("Email / documents", "Text-led, useful, and specific. No invented contacts, addresses, or trust seals."),
                ("Partner work", "Keep marks separate. Match optical weight and obtain explicit permission.")]
for i, (a, b) in enumerate(channel_rows):
    y = 187+i*87
    line(548, y, 908, y, "field", .5)
    label(a, 548, y+12, "field")
    para(b, 548, y+35, 356, 17, max_height=51)

# 15 / Truth and release.
page("14 / Stewardship")
title("Confidence comes from precision", "A brand promise is not a receipt.", size=46)
rows = [("Private is not anonymous.", "Name the actual permitted audience before submission."),
        ("A suggestion is not a decision.", "Keep the owner accountable; distinguish synthesis from approval."),
        ("Built is not live.", "Separate local output, publication, host acceptance, and live route verification."),
        ("Exported is not approved.", "The user directs the strategic idea; the new visual system still needs review.")]
for i, (a, b) in enumerate(rows):
    rule_row(207+i*65, a, b, split=355, size=18)
label("Release path", M, 490, "field")
for i, word in enumerate(["Brief", "Build", "Validate", "Review", "Publish", "Adopt"]):
    x = 218+i*114
    text(word, x, 486, 18, "SourceSemi")
    if i < 5:
        line(x+68, 500, x+96, 500, "field", .8)
para("Use the source manifest, channel guides, claim register, brief templates, and adoption ledger. Do not use an asset count as a quality gate.", M, 528, 850, 12, max_height=20)

# 16 / Closing and handoff.
page("15 / Review and release", "ink")
asset("di-lockup-reverse", M, 73, 230)
text("Invite the perspectives.\nKeep the responsibility.", M, 174, 64)
para("A distinct product identity with a quiet family trace.\nA thoughtful answer to the paralysis of analysis.", M, 345, 725, 25, max_height=70)
line(M, 440, 908, 440, "field", .7)
label("This package", M, 462, "mist", 9)
para("Strategy / outlined masters / color and type / channel standards / editable applications / public reference / governance", M, 489, 474, 16, max_height=49)
label("The remaining creative decision", 601, 462, "mist", 9)
para("Review Open frame, the Di signature, palette, type, and applications.", 601, 489, 304, 16, max_height=49)

assert PAGE == 16
C.save()
print(f"Built {OUT.relative_to(ROOT)} ({PAGE} pages)")

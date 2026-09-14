#!/usr/bin/env python3
"""Build the DecisionInvitation neuroinclusive decision-design case study."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, PageBreak, Paragraph, Spacer,
    Table, TableStyle, KeepTogether,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf/decisioninvitation-neuroinclusive-case-study.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

REGISTER = colors.HexColor("#211B2B")
COBALT = colors.HexColor("#3346C8")
PERI = colors.HexColor("#C3CCFF")
OPTIC = colors.HexColor("#F7F8FF")
ORANGE = colors.HexColor("#D54B1E")
MUTED = colors.HexColor("#625B70")

pdfmetrics.registerFont(TTFont("Sora", str(ROOT / "assets/fonts/Sora-Regular.ttf")))
pdfmetrics.registerFont(TTFont("SoraSemi", str(ROOT / "assets/fonts/Sora-SemiBold.ttf")))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Kicker", fontName="SoraSemi", fontSize=8, leading=11, textColor=COBALT, spaceAfter=12, tracking=1.1))
styles.add(ParagraphStyle(name="TitleDI", fontName="SoraSemi", fontSize=30, leading=31, textColor=REGISTER, spaceAfter=18))
styles.add(ParagraphStyle(name="H1DI", fontName="SoraSemi", fontSize=22, leading=25, textColor=REGISTER, spaceAfter=14))
styles.add(ParagraphStyle(name="H2DI", fontName="SoraSemi", fontSize=13, leading=17, textColor=COBALT, spaceBefore=9, spaceAfter=6))
styles.add(ParagraphStyle(name="BodyDI", fontName="Sora", fontSize=9.2, leading=13.6, textColor=REGISTER, spaceAfter=8))
styles.add(ParagraphStyle(name="SmallDI", fontName="Sora", fontSize=7.2, leading=10.2, textColor=MUTED, spaceAfter=4))
styles.add(ParagraphStyle(name="QuoteDI", fontName="SoraSemi", fontSize=16, leading=21, textColor=COBALT, leftIndent=18, borderColor=PERI, borderWidth=0, borderPadding=10, spaceBefore=8, spaceAfter=12))
styles.add(ParagraphStyle(name="CenterDI", fontName="SoraSemi", fontSize=11, leading=15, textColor=REGISTER, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="CellDI", fontName="Sora", fontSize=7.2, leading=10.2, textColor=REGISTER))
styles.add(ParagraphStyle(name="CellHeadDI", fontName="SoraSemi", fontSize=7.2, leading=9.2, textColor=colors.white))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(PERI)
    canvas.setLineWidth(.5)
    canvas.line(.62 * inch, .48 * inch, 7.88 * inch, .48 * inch)
    canvas.setFont("SoraSemi", 6.8)
    canvas.setFillColor(REGISTER)
    canvas.drawString(.62 * inch, .29 * inch, "DECISIONINVITATION / NEUROINCLUSIVE DECISION DESIGN / 0.4.0 PROPOSAL")
    canvas.setFillColor(ORANGE)
    canvas.circle(7.60 * inch, .33 * inch, 2.3, fill=1, stroke=0)
    canvas.setFillColor(REGISTER)
    canvas.drawRightString(7.88 * inch, .29 * inch, f"{doc.page:02d}")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUT), pagesize=letter, leftMargin=.62 * inch, rightMargin=.62 * inch,
    topMargin=.62 * inch, bottomMargin=.62 * inch,
    title="DecisionInvitation: a neuroinclusive decision instrument",
    author="DecisionInvitation", subject="Deep case study and competitive landscape",
)
frame = Frame(doc.leftMargin, doc.bottomMargin + .10 * inch, doc.width, doc.height - .10 * inch, id="main")
doc.addPageTemplates([PageTemplate(id="case-study", frames=[frame], onPage=footer)])
story = []


def p(text, style="BodyDI"):
    story.append(Paragraph(text, styles[style]))


def title(kicker, heading, deck=None):
    parts = [Paragraph(kicker.upper(), styles["Kicker"]), Paragraph(heading, styles["H1DI"])]
    if deck:
        parts.append(Paragraph(deck, styles["QuoteDI"]))
    story.append(KeepTogether(parts))


def page():
    story.append(PageBreak())


def bullets(items):
    for item in items:
        p(f"<font color='#3346C8'>●</font>&nbsp;&nbsp;{item}")


def cell_rows(rows):
    """Wrap every table cell so columns never overwrite one another."""
    return [
        [Paragraph(value.replace("\n", "<br/>"), styles["CellHeadDI" if row_index == 0 else "CellDI"])
         for value in row]
        for row_index, row in enumerate(rows)
    ]


# 1 — Cover
story.append(Spacer(1, .72 * inch))
p("DEEP CASE STUDY / 14 SEPTEMBER 2026", "Kicker")
p("DecisionInvitation:<br/>a neuroinclusive<br/>decision instrument", "TitleDI")
p("Designed for minds that do their best thinking with context, time, and a clear next step.", "QuoteDI")
story.append(Spacer(1, .30 * inch))
p("Catalyst of analysis.", "H2DI")
p("A product and market case for turning independent thought into accountable motion—without turning neurodivergence into a diagnosis gate or a marketing claim.")
p("PROPOSAL 0.4.0 / OWNER REVIEW PENDING", "SmallDI")

# 2 — Finding
page(); title("Executive finding", "The opportunity is a category boundary.", "Not another planner, poll, meeting tool, or consensus platform.")
p("DecisionInvitation can own a narrow but consequential transition: from a cognitively and socially noisy question to independent perspectives, explicit conditions, and a clear next move held by a named decision owner.")
p("Its neurodivergence story is structural, not clinical. Externalized context, asynchronous contribution, visible stages, resumable work, literal language, and explicit ownership align with cognitive-accessibility guidance and common accommodations.[1–6][10–14]")
p("Those mechanisms may reduce avoidable cognitive and social load. They do not establish that the product treats executive dysfunction, changes symptoms, or guarantees better decisions.")
p("<b>Strategic line</b>", "H2DI")
p("Designed for minds that do their best thinking with context, time, and a clear next step.", "QuoteDI")
p("<b>Inclusive promise:</b> Neuroinclusive by design. Useful for anyone deciding under cognitive load.")

# 3 — Human problem
page(); title("01 / The human problem", "A decision is many executive tasks at once.", "Do not make good judgment depend on memory, rapid turn-taking, interruption tolerance, or performed certainty.")
p("A consequential decision can require a person to retain context, compare options, predict consequences, inhibit a premature response, shift perspective, communicate a position, remember a deadline, and initiate the next action.")
p("Adult ADHD meta-analyses report group-level differences across working memory, inhibition, set shifting, and planning, with meaningful heterogeneity.[1][2] Research on autistic adults also shows mixed profiles: differences in flexibility or working memory may coexist with planning and decision-making strengths.[3][4]")
p("The design conclusion is not that neurodivergent people cannot decide. It is that the environment should carry avoidable load so judgment can remain visible.")
p("Choice paralysis also is not explained by option count alone. Choice-overload effects depend on complexity, task difficulty, preference uncertainty, and decision goal.[7]")

# 4 — Mechanism
page(); title("02 / Product mechanism", "Five moves turn analysis into motion.")
data = [
    ["MOVE", "DESIGN BEHAVIOR", "VALUE"],
    ["Externalize", "One bounded question; context, owner, audience, time and deadline up front", "Less reconstruction from memory"],
    ["Separate", "Independent asynchronous response before cross-participant influence", "Less turn-taking and social-performance load"],
    ["Qualify", "Yes if, no unless, not yet, and need information", "Conditions become decision data"],
    ["Resume", "Autosave, visible state, save-and-return, controlled reminders", "Interruption need not erase progress"],
    ["Close", "Owner records decision or threshold, rationale and next action", "Responsibility stays explicit"],
]
t = Table(cell_rows(data), colWidths=[.9*inch, 3.45*inch, 2.75*inch], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), REGISTER), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "SoraSemi"), ("FONTNAME", (0,1), (-1,-1), "Sora"),
    ("FONTSIZE", (0,0), (-1,-1), 7.2), ("LEADING", (0,0), (-1,-1), 10.2),
    ("VALIGN", (0,0), (-1,-1), "TOP"), ("GRID", (0,0), (-1,-1), .35, PERI),
    ("BACKGROUND", (0,1), (-1,-1), OPTIC), ("ROWBACKGROUNDS", (0,1), (-1,-1), [OPTIC, colors.white]),
    ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
    ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7),
]))
story.append(t)
story.append(Spacer(1, 12))
p("Cognitive offloading can reduce internal memory demand, but the external record must remain available and trustworthy.[5] Clear-step guidance emphasizes orientation and re-entry after distraction.[10][11]")

# 5 — Principles
page(); title("03 / Neuroinclusive principles", "Build access into the default path.", "Diagnosis is never the price of useful structure.")
principles = [
    "Orient before asking: task, reason, audience, time, visibility, deadline.",
    "One cognitive job at a time: understand, respond, review, commit.",
    "Preserve unfinished thought: autosave, receipt, obvious re-entry.",
    "Allow depth without requiring it: concise and detailed response paths.",
    "Normalize conditionality: missing information is useful decision data.",
    "Remove shame from reminders: factual language and user-controlled cadence.",
    "Keep language literal and calm; avoid urgency theater and ambiguous state.",
    "Disclose social boundaries before contribution.",
    "Support keyboard, screen readers, zoom, focus visibility and reduced motion.",
    "Return agency to the owner: the system clarifies; a person decides.",
]
bullets(principles)

# 6 — Why exceptional
page(); title("04 / Strategic advantage", "The product connects four things competitors split apart.")
for head, body in [
    ("Independent input", "Contributors can think without a meeting or shared-thread performance."),
    ("Decision-grade structure", "Responses preserve reason, condition, uncertainty and missing facts—not merely a vote."),
    ("Explicit authority", "The workflow says who owns the call rather than laundering it through “the group.”"),
    ("Forward condition", "Success can be a decision, a threshold, or the next fact required—not forced certainty."),
]:
    story.append(KeepTogether([Paragraph(head, styles["H2DI"]), Paragraph(body, styles["BodyDI"])]))
p("That combination turns <b>Catalyst of analysis.</b> from a slogan into product behavior: analysis is respected, bounded, and connected to action.", "QuoteDI")

# 7 — Landscape
page(); title("05 / Competitive landscape", "The market is a ring of adjacent categories.")
competitors = [
    ["CATEGORY / EXAMPLES", "THEIR CENTER", "DECISIONINVITATION WEDGE"],
    ["Collective governance\nLoomio", "Group discussion, proposals, polls, outcomes", "Independent advice to a named owner"],
    ["Workshop collaboration\nGroupMap, Miro", "Facilitation, brainstorming, voting, consensus", "One calm decision outside the workshop"],
    ["Polls and forms\nPolly, Typeform, Slido", "Collection, engagement, tallying", "Reasoning, conditions, ownership and closure"],
    ["Neuroinclusive planners\nTiimo, Goblin Tools", "Individual structure and task support", "Multi-person handoff from thought to decision"],
    ["Work execution\nSunsama, Motion", "Planning, timeboxing and scheduling", "The earlier moment when action is not yet settled"],
]
t = Table(cell_rows(competitors), colWidths=[1.75*inch, 2.6*inch, 2.75*inch], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), COBALT), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "SoraSemi"), ("FONTNAME", (0,1), (-1,-1), "Sora"),
    ("FONTSIZE", (0,0), (-1,-1), 7.2), ("LEADING", (0,0), (-1,-1), 10),
    ("VALIGN", (0,0), (-1,-1), "TOP"), ("GRID", (0,0), (-1,-1), .35, PERI),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [OPTIC, colors.white]),
    ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
    ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8),
]))
story.append(t)
story.append(Spacer(1, 12))
p("The closest strategic competitor is Loomio. To remain distinct, DecisionInvitation must not collapse into a smaller poll product; its workflow must preserve conditions, dissent, attribution boundaries and owner accountability.[18–24]")

# 8 — White space
page(); title("06 / Competitive white space", "Between personal planning and collective governance.", "A calm, asynchronous protocol for collecting independent judgment and converting it into an accountable next move.")
p("Tiimo and Goblin Tools directly address individual structure and complexity.[30–34] Loomio and GroupMap organize collective input and decisions.[18–23] Typeform and Polly make collection easy.[25–29] Sunsama and Motion help execute work that has already been chosen.[35–37]")
p("DecisionInvitation can own the transition none of these centers: the handoff from several private, independently formed perspectives to one responsible decision owner.")
p("<b>Category:</b> Decision instrument", "H2DI")
p("<b>Job:</b> Turn distributed judgment into a legible next move.")
p("<b>Distinctive protocol:</b> Ask separately → preserve reasoning → expose conditions → decide visibly.")
p("<b>Moat:</b> A trusted workflow and evidence model—not a feature checklist or AI-generated summary.")

# 9 — Expression
page(); title("07 / Brand expression", "Talk about conditions, not diagnoses.")
p("<b>Use</b>", "H2DI")
bullets([
    "Designed for minds that do their best thinking with context, time, and a clear next step.",
    "Neuroinclusive by design. Useful for anyone deciding under cognitive load.",
    "Different minds need different conditions for contributing.",
    "Make room for thinking. Make the next move visible.",
])
p("<b>Avoid</b>", "H2DI")
bullets([
    "Treats executive dysfunction.",
    "Built for every neurodivergent brain.",
    "Clinically proven to improve decisions.",
    "Eliminates ADHD paralysis.",
    "Bias-free, confidential, private, or anonymous without verified definitions.",
])
p("The existing verbal foundation remains intact: <b>Catalyst of analysis. Better input. Clearer decisions. A quieter way to decide. Ask separately. Decide clearly.</b>")

# 10 — Requirements
page(); title("08 / Product requirements", "The promise must become observable behavior.")
bullets([
    "One bounded decision per invitation, with a plain-language question.",
    "Preview of purpose, effort, visibility, owner and deadline.",
    "Autosave plus a durable receipt; no disappearing work.",
    "Save-and-return with a visible step and state indicator.",
    "Response states for yes, no, not yet, yes if, no unless and need information.",
    "Structured prompts for position, reason, condition, risk and missing fact.",
    "Controlled reminders with factual, non-shaming language.",
    "Owner view that preserves attribution, dissent and uncertainty.",
    "Final owner decision or threshold, rationale, next action and accountable person.",
    "Keyboard, screen-reader, zoom, contrast, focus and reduced-motion acceptance.",
])
p("The orange provenance dot must never become an urgency, error, completion, or attention signal.", "SmallDI")

# 11 — Evidence
page(); title("09 / Evidence boundary", "Mechanism evidence is not product efficacy.", "The research supports why these design choices matter. It does not prove what DecisionInvitation achieves.")
p("No direct study currently establishes that DecisionInvitation improves executive function, reduces ADHD or autistic distress, raises decision quality, or shortens time to decision.")
p("<b>Permitted:</b> “Designed to reduce avoidable cognitive and social load.”")
p("<b>Conditional on implementation:</b> “Supports asynchronous, structured contribution.”")
p("<b>Conditional on implementation and participatory testing:</b> “Neuroinclusive by design.”")
p("<b>Prohibited without direct evidence:</b> treatment, symptom reduction, clinical proof, universal inclusion, guaranteed outcomes, and claims of anonymity, confidentiality, security or compliance.")
p("Private is not anonymous. Synthesis is not truth. A recommendation is not a decision. A local build is not a live deployment.", "QuoteDI")

# 12 — Validation
page(); title("10 / Validation program", "Invite neurodivergent people into the design authority.")
p("Conduct paid participatory research with diagnosed and self-identified ADHD and autistic adults, alongside a broader comparison sample. Compare the structured flow with a shared thread, live meeting, or general form.")
bullets([
    "Comprehension without clarification; time to first meaningful response.",
    "Completion, abandonment and return-after-interruption rates.",
    "Unsubmitted or lost work and number of clarification requests.",
    "Contributor confidence that reasoning was represented.",
    "Owner ability to identify dissent, conditions and missing facts.",
    "Time to a recorded next move and perceived cognitive/social load.",
    "Keyboard, screen-reader, zoom, focus and reduced-motion failures.",
])
p("Interviews should explain why a measure changed. Report subgroup sizes, attrition, limitations and adverse experiences. Do not convert preference findings into clinical claims.")

# 13–14 — Sources
page(); title("Sources / research", "Primary evidence and accessibility guidance")
sources_a = [
    "[1] Boonstra AM et al. Executive functioning in adult ADHD: a meta-analytic review. Psychological Medicine (2005). pubmed.ncbi.nlm.nih.gov/16116936/",
    "[2] Pievsky MA, McGrath RE. The Neurocognitive Profile of ADHD: A Review of Meta-Analyses (2018). pubmed.ncbi.nlm.nih.gov/29106438/",
    "[3] Olde Dubbelink LME, Geurts HM. Planning Skills in Autism Across the Lifespan (2017). pubmed.ncbi.nlm.nih.gov/28160225/",
    "[4] Demetriou EA et al. Executive Functioning in Autistic Adults (2022). pubmed.ncbi.nlm.nih.gov/34499568/",
    "[5] Risko EF, Gilbert SJ. Cognitive offloading. Nature Reviews Psychology (2025). nature.com/articles/s44159-025-00432-2",
    "[6] National Institute of Mental Health. ADHD: What You Need to Know (2024). nimh.nih.gov/health/publications/adhd-2024.pdf",
    "[7] Chernev A et al. Choice overload: review and meta-analysis (2015). chernev.com/wp-content/uploads/2017/02/ChoiceOverload_JCP_2015.pdf",
    "[8] Gallupe RB et al. Unblocking brainstorms (1991). pubmed.ncbi.nlm.nih.gov/2016214/",
    "[9] Niederberger M, Spranger J. Delphi Technique in Health Sciences (2020). pubmed.ncbi.nlm.nih.gov/32866051/",
    "[10] W3C. Making Content Usable for People with Cognitive and Learning Disabilities. w3.org/TR/coga-usable/Overview-mutiple-pages.html",
    "[11] W3C. Provide Clear Steps. w3.org/WAI/WCAG2/supplemental/patterns/o1p04-clear-steps/",
    "[12] Job Accommodation Network. ADHD. askjan.org/disabilities/Attention-Deficit-Hyperactivity-Disorder-AD-HD.cfm",
    "[13] Job Accommodation Network. Autism Spectrum. askjan.org/disabilities/Autism-Spectrum.cfm",
    "[14] Job Accommodation Network. Accommodation and Compliance: Autism Spectrum. askjan.org/publications/Disability-Downloads.cfm?action=download&pubid=206344&pubtype=pdf",
    "[15] Gollwitzer PM, Brandstätter V. Implementation intentions and effective goal pursuit (1997). pubmed.ncbi.nlm.nih.gov/11760131/",
    "[16] Brom SS et al. Implementation intentions and prospective memory. pmc.ncbi.nlm.nih.gov/articles/PMC4113409/",
    "[17] Chen XJ et al. Implementation intention and prospective memory review. pmc.ncbi.nlm.nih.gov/articles/PMC9274250/",
]
for s in sources_a: p(s, "SmallDI")

page(); title("Sources / market", "Official product documentation")
sources_b = [
    "[18–21] Loomio overview, how it works, poll settings, anonymous voting. loomio.com/docs/en/user_manual/overview · loomio.com/how-it-works/ · loomio.com/docs/en/user_manual/polls/settings · loomio.com/docs/en/user_manual/polls/anonymous_voting",
    "[22–23] GroupMap features and overview. groupmap.com/features/ · help.groupmap.com/article/110-overview-of-groupmap",
    "[24] Miro Private Mode. help.miro.com/hc/en-us/articles/9794413310482-Private-mode",
    "[25–26] Polly quick start and product overview. polly.ai/help/polly-quick-start-guide · polly.ai/",
    "[27–29] Typeform feature glossary, platform and product overview. typeform.com/feature-glossary · typeform.com/platform-overview · typeform.com/",
    "[30] Tiimo product overview. tiimoapp.com/product",
    "[31–34] Goblin Tools overview, Magic ToDo, Taskmaster and Compiler. goblin.tools/ · android.goblin.tools/ToDo · goblin.tools/Taskmaster · ios.goblin.tools/Compiler",
    "[35–36] Sunsama daily planning and timeboxing. help.sunsama.com/docs/usage-guides/daily-planning/ · sunsama.com/features/timeboxing",
    "[37] Motion AI Task Manager. usemotion.com/features/ai-task-manager",
    "[38] Slido Live Q&A. slido.com/features-live-qa",
]
for s in sources_b: p(s, "SmallDI")
p("Research and competitive review accessed September 2026. Product features can change; verify official documentation before publishing a live comparison.", "SmallDI")
p("DecisionInvitation is the decision instrument for independent thought, visible conditions, and accountable motion.", "QuoteDI")

doc.build(story)
print(f"Built {OUT} ({doc.page} pages).")

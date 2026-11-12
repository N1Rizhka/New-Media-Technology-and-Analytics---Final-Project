#!/usr/bin/env python3
"""Build Team 5 Q15 8-minute pitch deck."""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables" / "Team5_Q15_pitch.pptx"
FIG = ROOT / "figures" / "fig1_history_evidence_by_buyer_type.png"

# Calm analytical palette — not purple/cream AI defaults
INK = RGBColor(0x1C, 0x24, 0x2E)
MUTED = RGBColor(0x5A, 0x64, 0x72)
ACCENT = RGBColor(0x0F, 0x6B, 0x5C)
LIGHT = RGBColor(0xF4, 0xF6, 0xF5)
RULE = RGBColor(0xC8, 0xD0, 0xCC)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def set_run(run, text, size=18, bold=False, color=INK, font="Georgia"):
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color


def add_bg(slide, prs):
    shape = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = LIGHT
    shape.line.fill.background()
    # send to back
    spTree = slide.shapes._spTree
    sp = shape._element
    spTree.remove(sp)
    spTree.insert(2, sp)


def add_footer(slide, prs, page, total=10):
    box = slide.shapes.add_textbox(
        Inches(0.5), prs.slide_height - Inches(0.45), Inches(12), Inches(0.3)
    )
    tf = box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    run = p.add_run()
    set_run(run, f"Team 5 · Q15 · Lumen Beauty  ·  {page}/{total}", 10, False, MUTED, "Calibri")


def title_bar(slide, title, subtitle=None):
    box = slide.shapes.add_textbox(Inches(0.55), Inches(0.35), Inches(12.2), Inches(0.7))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    set_run(run, title, 28, True, INK, "Georgia")
    if subtitle:
        p2 = tf.add_paragraph()
        run2 = p2.add_run()
        set_run(run2, subtitle, 14, False, MUTED, "Calibri")
    # accent rule
    line = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.RECTANGLE, Inches(0.55), Inches(1.05), Inches(1.4), Pt(3)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT
    line.line.fill.background()


def body_box(slide, left, top, width, height, lines, size=16):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, (text, bold) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(8)
        run = p.add_run()
        set_run(run, text, size, bold, INK, "Calibri")
    return box


def bullet_box(slide, left, top, width, height, items, size=16):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = 0
        p.space_after = Pt(10)
        run = p.add_run()
        set_run(run, "•  " + item, size, False, INK, "Calibri")
    return box


def metric_card(slide, left, top, width, height, value, label):
    shape = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = WHITE
    shape.line.color.rgb = RULE
    shape.line.width = Pt(1)
    tf = shape.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    set_run(run, value, 22, True, ACCENT, "Georgia")
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    run2 = p2.add_run()
    set_run(run2, label, 12, False, MUTED, "Calibri")


def build():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # 1 Title
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    box = slide.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(11.5), Inches(3.5))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    set_run(run, "Team 5  ·  Q15", 16, False, ACCENT, "Calibri")
    p2 = tf.add_paragraph()
    p2.space_before = Pt(12)
    run2 = p2.add_run()
    set_run(
        run2,
        'What should the “you may also like”\nshelf show, and to whom?',
        34,
        True,
        INK,
        "Georgia",
    )
    p3 = tf.add_paragraph()
    p3.space_before = Pt(18)
    run3 = p3.add_run()
    set_run(
        run3,
        "Association rules on Lumen Beauty orders (Sep–Nov 2026)\n"
        "Nini Rizhamadze · Giulia Scarpa · Milena Moschetti · "
        "Thi Thuy Khuc · Lina-Sophie Reinsch · Hai Yen Bui",
        14,
        False,
        MUTED,
        "Calibri",
    )
    add_footer(slide, prs, 1)

    # 2 The stake
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "The decision at stake", "One shelf. Who does it really serve?")
    metric_card(slide, Inches(0.6), Inches(1.5), Inches(3.9), Inches(1.6), "65%", "of orders are single-product")
    metric_card(slide, Inches(4.7), Inches(1.5), Inches(3.9), Inches(1.6), "¥2.2–6.6k", "scenario value / month if 5–15%\nof serum-only orders add a cream")
    metric_card(slide, Inches(8.8), Inches(1.5), Inches(3.9), Inches(1.6), "93%", "of history-rule evidence comes\nfrom heavy buyers (6+ orders)")
    bullet_box(
        slide,
        Inches(0.6),
        Inches(3.5),
        Inches(12),
        Inches(3),
        [
            "Founder & merchandising team choose which rules go on the post-purchase shelf.",
            "Q15 asks us to mine both single orders and whole customer histories — then check whom each shelf serves.",
            "Yuan upside is modest; the sharper risk is a shelf that mirrors the heaviest buyers.",
        ],
        17,
    )
    add_footer(slide, prs, 2)

    # 3 Method
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "Method in one slide", "Week 3 association rules · two basket definitions")
    bullet_box(
        slide,
        Inches(0.6),
        Inches(1.4),
        Inches(12),
        Inches(5.2),
        [
            "Order baskets = products bought together (the moment the shelf appears).",
            "History baskets = every product one customer bought in the quarter.",
            "Pairs only. Metrics: support, confidence, lift — with co-purchase count / denominator next to each rule.",
            "Support & confidence filter frequency; they are not significance tests.",
            "Thresholds from the shelf decision: ≥14 orders (0.4%) · ≥13 customers for histories (2%).",
            "Segments by n_orders: light 1–2 · mid 3–5 · heavy 6+ (robust at 4 / 8 / 10).",
        ],
        17,
    )
    add_footer(slide, prs, 3)

    # 4 Finding 1-2
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "Finding: one strong order rule", "Serum → Cream · 256 / 3,401 orders · lift 1.75")
    bullet_box(
        slide,
        Inches(0.6),
        Inches(1.4),
        Inches(12),
        Inches(5.2),
        [
            "At a comparable bar: 30 order rules vs 870 history rules (every possible pair).",
            "Serum → Cream: 256 orders with both vs ~147 expected by chance; confidence 0.40.",
            "Direction: Cream → Serum confidence is only 0.33 — show cream after serum.",
            "Holds for light / mid / heavy (1.79 / 1.93 / 1.72), livestream & store, and first orders (1.80).",
            "SKU pairs only rank which cream (Vit. C → Hydra Gel / Brightening; 26–27 orders).",
        ],
        17,
    )
    add_footer(slide, prs, 4)

    # 5 Finding history bias + figure
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "Finding: history shelves serve heavy buyers", "Light buyers = 46.5% of buyers, 1.7% of history-rule evidence")
    if FIG.exists():
        slide.shapes.add_picture(str(FIG), Inches(0.6), Inches(1.35), width=Inches(7.2))
    bullet_box(
        slide,
        Inches(8.0),
        Inches(1.5),
        Inches(4.8),
        Inches(5),
        [
            "Heavy buyers average 11.7 products → most pair evidence.",
            "Top history pairs have same-order lift < 1 (substitutes across visits).",
            "Calling them “bought together” would mislabel the shelf.",
            "Robust at every heavy cut-off we tried.",
        ],
        15,
    )
    add_footer(slide, prs, 5)

    # 6 Shelf decision card
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "From rule to shelf decision", "What a buyer with no history sees — and what would reject the rule")
    rows = [
        ("Trigger", "Any serum in the current basket"),
        ("Customers", "Everyone — including first-time / light buyers"),
        ("Shelf position", "Slot 1 on the post-purchase shelf: a cream"),
        ("No history", "Same shelf (first-order lift 1.80)"),
        ("Reject if", "A/B add-on < 2% in 6 weeks, or same-order lift ≤ 1 on control"),
    ]
    y = Inches(1.35)
    for label, text in rows:
        lab = slide.shapes.add_shape(
            MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, Inches(0.6), y, Inches(2.4), Inches(0.85)
        )
        lab.fill.solid()
        lab.fill.fore_color.rgb = ACCENT
        lab.line.fill.background()
        tf = lab.text_frame
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tf.paragraphs[0].add_run()
        set_run(run, label, 14, True, WHITE, "Calibri")
        body = slide.shapes.add_shape(
            MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, Inches(3.2), y, Inches(9.4), Inches(0.85)
        )
        body.fill.solid()
        body.fill.fore_color.rgb = WHITE
        body.line.color.rgb = RULE
        tf2 = body.text_frame
        tf2.word_wrap = True
        run2 = tf2.paragraphs[0].add_run()
        set_run(run2, text, 16, False, INK, "Calibri")
        y += Inches(1.0)
    add_footer(slide, prs, 6)

    # 7 Recommendation
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "Monday morning", "What the merchandising team does next")
    bullet_box(
        slide,
        Inches(0.6),
        Inches(1.4),
        Inches(12),
        Inches(5.2),
        [
            "Mine the shelf from single orders — not from purchase histories.",
            "After any serum, show a cream; rank creams with thin SKU pairs.",
            "One shelf for all buyers; no separate first-time shelf.",
            "Remaining slots: products light buyers buy most — not overall bestsellers.",
            "Pilot from 1 Dec 2026: random half for six weeks; success ≥ 5% cream add-on among serum-only orders.",
            "Drop the action if treatment add-on < 2% vs control, or light buyers are left behind.",
        ],
        17,
    )
    add_footer(slide, prs, 7)

    # 8 Ethics (short, since appendix has full)
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "Ethics tied to this shelf", "Bias, labelling, and data minimisation")
    bullet_box(
        slide,
        Inches(0.6),
        Inches(1.4),
        Inches(12),
        Inches(5.2),
        [
            "Stake: a history shelf would serve light buyers a heavy-buyer catalogue.",
            "Misinformation risk: do not label cross-visit substitutes as “bought together”.",
            "Privacy: order-based rules need only the current basket (PIPL minimisation).",
            "Safeguard: re-mine rules on the control half; report results by buyer type.",
            "Offer a non-profiled option (Algorithmic Recommendation Provisions, Art. 17).",
        ],
        17,
    )
    add_footer(slide, prs, 8)

    # 9 Limits
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "What the data cannot tell us", "Honest limits before Q&A")
    bullet_box(
        slide,
        Inches(0.6),
        Inches(1.4),
        Inches(12),
        Inches(5.2),
        [
            "Association ≠ causation; past logs cannot measure the shelf’s own effect.",
            "¥2.2–6.6k / month is a scenario — only the A/B test measures lift.",
            "Light-buyer SKU rules are thin (366 orders); we trust the category rule.",
            "Live shelf may create the pairs it later mines — hence the control-half re-mine.",
        ],
        17,
    )
    add_footer(slide, prs, 9)

    # 10 Close
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    box = slide.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.5), Inches(3.5))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    set_run(run, "Show a cream after a serum.\nBuild the shelf from orders, not histories.", 30, True, INK, "Georgia")
    p2 = tf.add_paragraph()
    p2.space_before = Pt(20)
    run2 = p2.add_run()
    set_run(run2, "One shelf for everyone — including buyers with no history.\nPilot half the traffic for six weeks. Drop it if it fails the kill conditions.", 16, False, MUTED, "Calibri")
    add_footer(slide, prs, 10)

    OUT.parent.mkdir(exist_ok=True)
    prs.save(str(OUT))
    print("wrote", OUT)


if __name__ == "__main__":
    build()

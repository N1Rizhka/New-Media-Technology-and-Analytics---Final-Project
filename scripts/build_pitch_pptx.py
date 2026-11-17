#!/usr/bin/env python3
"""Build the unified Team 5 Q15 pitch deck + NMTA_T05_slides.pdf."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
OUT_PPTX = ROOT / "deliverables" / "Team5_Q15_pitch.pptx"
OUT_SUBMIT = ROOT / "deliverables" / "NMTA_T05_slides.pptx"
FIG = ROOT / "figures"

# Tongji University palette (同济蓝 C100 M60 Y0 K0 ≈ #0066B3)
INK = RGBColor(0x22, 0x22, 0x22)
MUTED = RGBColor(0x5A, 0x65, 0x70)
ROSE = RGBColor(0x00, 0x66, 0xB3)  # Tongji blue (kept name for call sites)
STONE = RGBColor(0x3F, 0x94, 0xE7)
DEEP = RGBColor(0x00, 0x3D, 0x7A)
PAPER = RGBColor(0xEE, 0xF1, 0xF3)
LINE = RGBColor(0xCB, 0xCB, 0xCB)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TONGJI = ROSE

TOTAL = 14  # 13 pitch + ethics appendix


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
    shape.fill.fore_color.rgb = PAPER
    shape.line.fill.background()
    spTree = slide.shapes._spTree
    sp = shape._element
    spTree.remove(sp)
    spTree.insert(2, sp)


def add_footer(slide, prs, page):
    box = slide.shapes.add_textbox(
        Inches(0.5), prs.slide_height - Inches(0.42), Inches(12.2), Inches(0.28)
    )
    tf = box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    run = p.add_run()
    label = f"Team 5 · Q15 · Lumen Beauty  ·  {page}/{TOTAL}"
    if page == TOTAL:
        label = f"Team 5 · Q15 · Ethics appendix  ·  {page}/{TOTAL}"
    set_run(run, label, 10, False, MUTED, "Calibri")


def title_bar(slide, title, subtitle=None):
    box = slide.shapes.add_textbox(Inches(0.55), Inches(0.28), Inches(12.2), Inches(0.85))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    set_run(run, title, 26, True, INK, "Georgia")
    if subtitle:
        p2 = tf.add_paragraph()
        run2 = p2.add_run()
        set_run(run2, subtitle, 13, False, MUTED, "Calibri")
    line = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.RECTANGLE, Inches(0.55), Inches(1.12), Inches(1.35), Pt(3)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = ROSE
    line.line.fill.background()


def bullet_box(slide, left, top, width, height, items, size=16):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(9)
        run = p.add_run()
        set_run(run, "•  " + item, size, False, INK, "Calibri")
    return box


def lift_note(slide, text, top=Inches(6.55)):
    box = slide.shapes.add_textbox(Inches(0.55), top, Inches(12.2), Inches(0.35))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    set_run(run, text, 12, False, DEEP, "Calibri")


def add_pic(slide, name, left, top, width):
    path = FIG / name
    if path.exists():
        slide.shapes.add_picture(str(path), left, top, width=width)


def build():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # 1 Title
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    box = slide.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(11.5), Inches(4.2))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    set_run(p.add_run(), "Team 5  ·  Q15  ·  investor decision pitch", 15, False, ROSE, "Calibri")
    p2 = tf.add_paragraph()
    p2.space_before = Pt(14)
    set_run(
        p2.add_run(),
        'What should the “you may also like”\nshelf show, and to whom?',
        32,
        True,
        INK,
        "Georgia",
    )
    p3 = tf.add_paragraph()
    p3.space_before = Pt(18)
    set_run(
        p3.add_run(),
        "Vote: approve one order-based shelf (cream after serum) + kill-switch pilot\n"
        "Evidence: Lumen Beauty orders · Sep–Nov 2026 · association rules\n\n"
        "Nini Rizhamadze · Giulia Scarpa · Milena Moschetti ·\n"
        "Thi Thuy Khuc · Lina-Sophie Reinsch · Hai Yen Bui",
        14,
        False,
        MUTED,
        "Calibri",
    )
    add_footer(slide, prs, 1)

    # 2 Stake
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "Why investors should care", "Empty baskets + a fairness risk if we train on histories")
    add_pic(slide, "fig_basket_size.png", Inches(0.5), Inches(1.35), Inches(7.0))
    bullet_box(
        slide,
        Inches(7.7),
        Inches(1.45),
        Inches(5.1),
        Inches(4.8),
        [
            "Shelf after every order: 3,401 checkouts · 647 buyers",
            "65% leave with one product — room for one add-on",
            "Upside scenario: ¥2.2–6.6k / month if 5–15% of ~127 serum-only orders add cream",
            "Risk: 301 light buyers (46.5%) would see history rules only 1.7% built from them",
            "Vote question: who trains the shelf?",
        ],
        14,
    )
    lift_note(slide, "Lift = how much more often two products appear together than chance — a descriptive ratio, not a promise of sales.")
    add_footer(slide, prs, 2)

    # 3 Theory
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "Theory before the rules", "STP targeting + product complementarity")
    bullet_box(
        slide,
        Inches(0.6),
        Inches(1.4),
        Inches(12.1),
        Inches(5.2),
        [
            "STP (“to whom”): if we train on whole histories, heavy buyers will dominate the evidence.",
            "Complementarity (“what”): serum and cream are sequential skincare steps — they should co-occur more than chance.",
            "Prediction 1: history rules will be written mostly by heavy buyers.",
            "Prediction 2: Serum → Cream will show lift > 1, cream-after-serum direction, and hold in every segment.",
            "Algorithmic bias belongs in ethics: it is the cost of choosing the wrong evidence base.",
        ],
        17,
    )
    lift_note(slide, "Lift > 1 means complements (bought together more than chance); lift < 1 means substitutes or noise.")
    add_footer(slide, prs, 3)

    # 4 EDA buyers
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "Who places the orders?", "Light buyers ≠ order volume")
    add_pic(slide, "fig_buyers_vs_orders.png", Inches(0.45), Inches(1.3), Inches(7.4))
    bullet_box(
        slide,
        Inches(8.0),
        Inches(1.5),
        Inches(4.8),
        Inches(4.8),
        [
            "Light = 46.5% of buyers, 11% of orders",
            "Heavy = 41% of buyers, 80% of orders",
            "History rules will hear heavy buyers first",
            "This is why “to whom?” is not optional",
        ],
        16,
    )
    add_footer(slide, prs, 4)

    # 5 Method
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "Method in one slide", "Week 3 association rules · two basket definitions")
    bullet_box(
        slide,
        Inches(0.6),
        Inches(1.35),
        Inches(12.1),
        Inches(5.2),
        [
            "Order baskets = products bought together (the shelf moment).",
            "History baskets = every product one customer bought in the quarter.",
            "Pairs only. Support / confidence / lift — with count and denominator.",
            "Support & confidence filter frequency; they are not significance tests.",
            "Thresholds from the decision: ≥14 orders (0.4%) · ≥13 customers (2%).",
            "Segments by n_orders: light 1–2 · mid 3–5 · heavy 6+.",
        ],
        16,
    )
    lift_note(slide, "Lift = confidence of A→B divided by how often B appears on its own.")
    add_footer(slide, prs, 5)

    # 6 Serum → Cream
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(
        slide,
        "Finding: Serum → Cream",
            "256 / 3,401 orders · confidence 0.40 · lift 1.75  (256 vs ~147 expected)",
    )
    add_pic(slide, "fig_serum_cream_slices.png", Inches(0.4), Inches(1.25), Inches(7.3))
    bullet_box(
        slide,
        Inches(7.85),
        Inches(1.4),
        Inches(5.0),
        Inches(4.8),
        [
            "Only category pair with lift > 1 at ≥1% support",
            "Direction: show cream after serum (0.40 vs 0.33)",
            "Matches complementarity: two routine steps",
            "Holds in livestream and store",
            "SKU pairs only rank which cream (15–27 orders)",
        ],
        15,
    )
    lift_note(slide, "Lift 1.75 = serum and cream appear together 75% more often than chance.")
    add_footer(slide, prs, 6)

    # 7 Open slot
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "The open slot", "~127 serum orders / month leave without a cream")
    add_pic(slide, "fig_serum_opportunity.png", Inches(1.2), Inches(1.35), Inches(10.8))
    lift_note(slide, "Sep 137 · Oct 124 · Nov 121 serum-only orders — the shelf’s addressable set each month.")
    add_footer(slide, prs, 7)

    # 8 Histories flood
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "Histories flood the rule table", "Same bar → 30 order rules vs 870 history rules")
    add_pic(slide, "fig_rules_orders_vs_histories.png", Inches(0.4), Inches(1.3), Inches(6.6))
    add_pic(slide, "fig1_history_evidence_by_buyer_type.png", Inches(7.1), Inches(1.35), Inches(5.7))
    lift_note(slide, "Heavy buyers = 41% of buyers but 92.9% of history-rule evidence — Prediction 1 confirmed.")
    add_footer(slide, prs, 8)

    # 9 History ≠ together
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "History pairs ≠ bought together", "Same-order lift falls below 1")
    add_pic(slide, "fig_history_vs_order_lift.png", Inches(0.55), Inches(1.3), Inches(12.1))
    lift_note(slide, "Lift < 1 inside one order = substitutes across visits, not “frequently bought together”.")
    add_footer(slide, prs, 9)

    # 10 One shelf
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "One shelf for everyone — if order-based", "Including first-time and light buyers")
    add_pic(slide, "fig_serum_cream_slices.png", Inches(0.45), Inches(1.25), Inches(7.5))
    bullet_box(
        slide,
        Inches(8.1),
        Inches(1.45),
        Inches(4.7),
        Inches(4.8),
        [
            "Light / mid / heavy: lift 1.79 / 1.93 / 1.72",
            "First orders: lift 1.80",
            "No separate first-time shelf needed",
            "What new buyers need: a shelf not trained only on heavy histories",
        ],
        15,
    )
    lift_note(slide, "Same lift pattern in every segment = Prediction 2 confirmed.")
    add_footer(slide, prs, 10)

    # 11 Monday morning
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(
        slide,
        "The ask — what we want you to approve",
        "Order-based shelf · cream after serum · kill-switch pilot",
    )
    bullet_box(
        slide,
        Inches(0.6),
        Inches(1.35),
        Inches(12.1),
        Inches(5.3),
        [
            "Approve: cream in slot 1 after serum — one shelf for all buyers (incl. first-time)",
            "Reject for primary slot: history-trained “bought together” personalisation",
            "Leftover slots from light-buyer favourites — not heavy-buyer bestsellers",
            "Pilot 50/50 from 1 Dec: six weeks = safety only (~96 serum-only / half)",
            "Measure 5% vs 2% only after ~9 months (~588 / half); success ≥ 5% add-on",
            "Kill switch: < 2% and no better than control · light/first-time left behind · control lift ≤ 1",
        ],
        15,
    )
    add_footer(slide, prs, 11)

    # 12 Limitations
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "What the data cannot tell us", "Honest limits before Q&A")
    bullet_box(
        slide,
        Inches(0.6),
        Inches(1.4),
        Inches(12.1),
        Inches(5.2),
        [
            "Association ≠ causation; past logs cannot measure the shelf’s own effect.",
            "¥2.2–6.6k / month is a scenario — only the live split measures lift.",
            "A six-week half (~96 serum-only orders) cannot separate 5% from 2%; it is a safety check.",
            "Same-order lifts for top history pairs rest on single-digit counts — noisy, but below 1.",
            "Light-buyer SKU ranks rest on tens of orders; we trust the category rule more.",
            "Lift is a descriptive ratio, not a causal effect or a significance test.",
            "A live shelf may create the pairs it later mines — hence the control-half re-mine.",
        ],
        17,
    )
    add_footer(slide, prs, 12)

    # 13 Close
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    box = slide.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(11.5), Inches(3.8))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    set_run(
        p.add_run(),
        "Vote yes: cream after serum.\nTrain on the checkout — not the biography.",
        28,
        True,
        INK,
        "Georgia",
    )
    p2 = tf.add_paragraph()
    p2.space_before = Pt(18)
    set_run(
        p2.add_run(),
        "One shelf for everyone — including buyers with no history.\n"
        "Fund a 50/50 pilot with a kill switch.\n"
        "Six weeks to catch failure; longer only to measure uplift.",
        16,
        False,
        MUTED,
        "Calibri",
    )
    add_footer(slide, prs, 13)

    # 14 Ethics appendix (required after last pitch slide)
    slide = prs.slides.add_slide(blank)
    add_bg(slide, prs)
    title_bar(slide, "Appendix · Ethics & compliance", "Bias, labelling, privacy — tied to this shelf")
    bullet_box(
        slide,
        Inches(0.6),
        Inches(1.35),
        Inches(12.1),
        Inches(5.3),
        [
            "Stake: a history shelf serves 301 light buyers a heavy-buyer catalogue (1.7% of the evidence).",
            "Misinformation: do not label cross-visit substitutes as “bought together”.",
            "Privacy: order-based rules need only the current basket (PIPL minimisation).",
            "Offer a non-profiled option / easy opt-out (Algorithmic Recommendation Provisions, Art. 17).",
            "Safeguard: re-mine on the control half; report results by buyer type; drop under the kill conditions.",
        ],
        16,
    )
    add_footer(slide, prs, 14)

    OUT_PPTX.parent.mkdir(exist_ok=True)
    prs.save(str(OUT_PPTX))
    shutil.copy2(OUT_PPTX, OUT_SUBMIT)
    print("wrote", OUT_PPTX)
    print("wrote", OUT_SUBMIT)

    # Export PDF via LibreOffice
    out_dir = ROOT / "deliverables"
    cmd = [
        "soffice",
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(out_dir),
        str(OUT_SUBMIT),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        pdf = out_dir / "NMTA_T05_slides.pdf"
        print("wrote", pdf if pdf.exists() else "(pdf conversion produced no file)")
    except Exception as e:
        print("PDF conversion failed:", e)


if __name__ == "__main__":
    build()

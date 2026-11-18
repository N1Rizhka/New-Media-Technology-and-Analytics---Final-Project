#!/usr/bin/env python3
"""Build the Q15 report on project_report_template structure (sections 1–7).

All numbers below are recomputed from the course CSVs / notebook outputs.
"""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    HRFlowable,
    Image,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
FIG = ROOT / "figures"

# ---- verified constants (from notebook / independent pandas recompute) ----
TEAM = "Team 5"
DATE = "2026-11-26"
MEMBERS = (
    "Nini Rizhamadze, Giulia Scarpa, Milena Moschetti, "
    "Thi Thuy Khuc, Lina-Sophie Reinsch, Hai Yen Bui"
)
QUESTION = 'Q15 — What should the "you may also like" shelf show, and to whom?'

N_LINES_RAW, N_LINES = 4920, 4915
N_DUP = 5
GMV = 1_171_735.16
N_ORDERS, N_BUYERS = 3401, 647
AVG_ORDER, AVG_HIST = 1.45, 6.27
N_SINGLE, PCT_SINGLE = 2219, 65.2
SIZE_DIST = (2219, 850, 332)  # 1, 2, 3 products
LIGHT_B, MID_B, HEAVY_B = 301, 81, 265
LIGHT_O, MID_O, HEAVY_O = 366, 304, 2731
LIVE, STORE = 2579, 822
ORDER_RULES, HIST_RULES = 30, 870
SC_BOTH, SC_SERUM, SC_CREAM = 256, 638, 781
SC_EXP = 146.5
SC_SUP, SC_CONF, SC_LIFT = 0.075, 0.401, 1.747
CS_CONF = 0.328
VC_HYDRA_BOTH, VC_N, VC_HYDRA_CONF, VC_HYDRA_LIFT = 26, 188, 0.138, 2.294
VC_BRIGHT_BOTH, VC_BRIGHT_CONF, VC_BRIGHT_LIFT = 27, 0.144, 2.272
EMPTY_STREAM = 1213
PRICE_MIN, PRICE_MAX = 54.45, 504.85
N_ORD_MIN, N_ORD_MAX, N_ORD_MED, FENCE = 1, 20, 3, 21
EV_LIGHT, EV_MID, EV_HEAVY = 1.7, 5.4, 92.9
AVG_PROD_L, AVG_PROD_M, AVG_PROD_H = 1.77, 5.25, 11.69
TONER_HIST_LIFT, TONER_SAME_BOTH, TONER_EXP, TONER_SAME_LIFT = 2.15, 3, 8.1, 0.37
FIRST_SUP, FIRST_CONF, FIRST_LIFT = 0.085, 0.426, 1.803
SLICE = {
    "light": (366, 0.093, 0.410, 1.785),
    "mid": (304, 0.086, 0.456, 1.926),
    "heavy": (2731, 0.072, 0.394, 1.720),
    "livestream": (2579, 0.074, 0.387, 1.733),
    "store": (822, 0.080, 0.449, 1.800),
}
SNC = {"2026-09": 137, "2026-10": 124, "2026-11": 121}
SNC_MEAN = 127.33333333333333
CREAM_VAL = 346.52
SCEN = {0.05: 2206, 0.10: 4412, 0.15: 6619}
PILOT_HALF_6W = 95.5
PILOT_N_ARM = 588
PILOT_MONTHS = 9.2
MIN_PROD_LIFT = 1.39
MAX_PAIR_SUP = 0.0079
LIGHT_SLOTS = [
    ("Clay Purifying Mask", 27),
    ("Deep Clean Foam", 22),
    ("Cooling Eye Gel", 21),
    ("Essence Toner", 21),
]
ROBUST = [
    (4, 48.2, 97.1, 1.73),
    (6, 41.0, 92.9, 1.72),
    (8, 32.8, 83.3, 1.71),
    (10, 21.2, 62.8, 1.61),
]


# ---------------- Word helpers ----------------
def set_doc_defaults(doc: Document):
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(2.4)
    section.right_margin = Cm(2.4)
    section.top_margin = Cm(2.2)
    section.bottom_margin = Cm(2.2)
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    style.font.size = Pt(12)
    for sname, size in [("Heading 1", 14), ("Heading 2", 12), ("Title", 16)]:
        st = doc.styles[sname]
        st.font.name = "Times New Roman"
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = RGBColor(0x00, 0x3D, 0x7A)


def add_para(doc, text, *, bold=False, italic=False, center=False, size=12, space_after=8):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    run.font.name = "Times New Roman"
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(space_after)
    return p


def add_bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(item, style="List Bullet")
        for run in p.runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)


def add_caption(doc, text):
    add_para(doc, text, italic=True, center=True, size=10, space_after=10)


def add_figure(doc, path: Path, width_in=5.8):
    if path.exists():
        doc.add_picture(str(path), width=Inches(width_in))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER


def cover_table(doc):
    table = doc.add_table(rows=5, cols=2)
    table.style = "Table Grid"
    rows = [
        ("Team number", TEAM),
        ("Members", MEMBERS),
        ("Question ID", QUESTION),
        ("Date", DATE),
        ("Course", "New Media Technology and Analytics (20001920076) · Fall 2026 · Tongji SEM"),
    ]
    for i, (a, b) in enumerate(rows):
        table.rows[i].cells[0].text = a
        table.rows[i].cells[1].text = b


def add_simple_table(doc, headers, rows):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Table Grid"
    for j, h in enumerate(headers):
        t.rows[0].cells[j].text = h
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            t.rows[i + 1].cells[j].text = str(val)
    doc.add_paragraph("")


def fill_report_body_docx(doc: Document):
    """Shared narrative for Word (template sections 1–7)."""
    doc.add_heading("1. Problem & what it is worth", level=1)
    add_para(
        doc,
        "After every purchase, Lumen Beauty’s Douyin mini-program shows a “you may also like” "
        "cross-sell shelf. The brand founder and the e-commerce merchandising team must decide "
        "which association rules earn a shelf slot, and whether first-time buyers should see a "
        "different shelf from frequent buyers.",
    )
    add_para(
        doc,
        f"In the cleaned quarter (1 Sep–30 Nov 2026) the store recorded {N_ORDERS:,} orders, "
        f"{N_BUYERS} buyers and ¥{GMV:,.2f} GMV. {PCT_SINGLE:.0f}% of orders contain a single "
        f"product ({N_SINGLE:,} of {N_ORDERS:,}), so most checkouts leave an empty second slot. "
        f"On average {SNC_MEAN:.0f} serum orders per month leave without a cream "
        f"(Sep {SNC['2026-09']} / Oct {SNC['2026-10']} / Nov {SNC['2026-11']}). "
        f"If the shelf persuades 5–15% of those orders to add a cream (mean cream line value "
        f"¥{CREAM_VAL:.2f}), the scenario value is ¥{SCEN[0.05]:,}–{SCEN[0.15]:,} per month "
        f"(0.6–1.7% of monthly GMV). That yuan figure is a scenario, not a measured lift.",
    )
    add_para(
        doc,
        f"The sharper stake is in users. Heavy buyers (6+ orders) are 41.0% of buyers but place "
        f"80.3% of orders. Light buyers (1–2 orders) are 46.5% of buyers — {LIGHT_B} people — "
        f"but place only 10.8% of orders. A shelf trained on whole purchase histories would serve "
        f"those {LIGHT_B} light buyers using rules that draw only {EV_LIGHT}% of their pair evidence "
        f"from light buyers’ own histories. Getting discovery wrong is a targeting error: the store "
        f"would position the shelf for its heaviest segment while nearly half of buyers are light.",
    )
    add_para(
        doc,
        "Unit of analysis. Q15 requires two basket definitions: (1) single orders — the moment the "
        "shelf appears; (2) whole customer histories — every distinct product a buyer purchased in "
        f"the quarter. The figure {AVG_ORDER} is the average number of distinct products per order "
        "(unique SKUs), not units shipped.",
    )

    doc.add_heading("2. Data", level=1)
    add_para(
        doc,
        "We use two tables from the course project dataset (Lumen Beauty full Sep–Nov 2026 operations "
        "export; see project_data_dictionary): lb_order_lines.csv "
        f"({N_LINES_RAW:,} rows before cleaning) and lb_users.csv (1,000 registered users). "
        "Streams, comments and follows are excluded because basket co-purchase does not need them.",
    )
    doc.add_heading("Cleaning choices", level=2)
    add_bullets(
        doc,
        [
            f"Duplicates: {N_DUP} exact duplicate order lines removed. {N_LINES:,} lines remain. GMV after cleaning = ¥{GMV:,.2f}.",
            f"Missing values: empty stream_id on {EMPTY_STREAM:,} lines, all store orders. Per the data dictionary this means “not applicable”, not missing data.",
            f"Units: qty ∈ {{1, 2}}; unit_price ¥{PRICE_MIN:.2f}–¥{PRICE_MAX:.2f}. No zero or negative prices.",
            f"Outliers: among the {N_BUYERS} buyers, orders per buyer range {N_ORD_MIN}–{N_ORD_MAX} (median {N_ORD_MED}). Boxplot fence = {FENCE}; nobody exceeds it. Heavy buyers are kept — they are the group Q15 asks about.",
            f"Join check: all {N_BUYERS} buyers map to lb_users; n_orders matches the order table for every buyer. First-order IDs (smallest order_id per buyer) match lb_users.first_order_date for all {N_BUYERS} buyers.",
        ],
    )
    add_para(
        doc,
        f"Channels are livestream ({LIVE:,} orders) and store ({STORE}). Values such as search / "
        "short_video / ad belong to users.first_channel (arrival), not to where the order was placed.",
    )
    add_simple_table(
        doc,
        ["Buyer type", "Buyers", "Orders", "% of buyers", "% of orders"],
        [
            ["Light (1–2 orders)", str(LIGHT_B), str(LIGHT_O), "46.5%", "10.8%"],
            ["Mid (3–5)", str(MID_B), str(MID_O), "12.5%", "8.9%"],
            ["Heavy (6+)", str(HEAVY_B), f"{HEAVY_O:,}", "41.0%", "80.3%"],
        ],
    )
    add_caption(doc, "Table 1. Buyer intensity segments (cut on n_orders, not spend).")
    add_figure(doc, FIG / "fig_basket_size.png")
    add_caption(doc, f"Figure 1. Basket size: {PCT_SINGLE:.0f}% of orders contain a single product.")
    add_figure(doc, FIG / "fig_buyers_vs_orders.png")
    add_caption(doc, "Figure 2. Light buyers are nearly half the customers; heavy buyers place most orders.")
    add_para(
        doc,
        f"Order baskets average {AVG_ORDER} distinct products "
        f"(1 / 2 / 3 products: {SIZE_DIST[0]:,} / {SIZE_DIST[1]} / {SIZE_DIST[2]}). "
        f"History baskets average {AVG_HIST} products. Segmentation uses n_orders rather than "
        "high_value (spend-based), because Q15 asks whether frequent buyers dominate the rules.",
    )

    doc.add_heading("3. Method & assumptions", level=1)
    add_para(
        doc,
        "Method family: association rule mining (Week 3), Apriori via mlxtend (≥0.23.4; this run used 0.25.0), "
        "pairs only (max_len = 2) because the shelf shows one product next to another. Metrics: support, "
        "confidence, lift. Support and confidence filter observed co-purchase frequency; they are not tests of "
        "statistical significance. Beside every rule we report the co-purchase count and its denominator.",
    )
    add_para(
        doc,
        f"Thresholds (decision-driven). The plan’s 2% product support returns zero product rules on orders "
        f"(largest pair support = {MAX_PAIR_SUP:.2%}). Order-level min_support = 0.4% "
        f"(≥14 of {N_ORDERS:,} orders ≈ one qualifying order per week over 13 weeks). Category rules use 1% "
        f"(≥35 orders). History rules use 2% (≥13 of {N_BUYERS} customers) so the two units face a comparable bar.",
    )
    add_para(
        doc,
        "Theory lens — two testable predictions. (T1) STP targeting: if histories train the shelf, heavy buyers "
        "will dominate the evidence. (T2) Product complementarity in a skincare routine: serum and cream are "
        "sequential steps, so Serum → Cream should show lift > 1, cream-after-serum direction, and hold for "
        "light / mid / heavy buyers, first orders, and both channels. Algorithmic bias is treated as the ethics "
        "stake of a history-trained shelf (§6), not as the explanation of why serum and cream co-occur.",
    )
    add_para(
        doc,
        "Assumptions and limits of the method. Lift compares observed co-purchase with the product of marginal "
        "rates; it is a descriptive ratio, not a causal effect and not a significance test. With many possible "
        "pairs we do not run unadjusted p-values. Large history baskets raise almost every pair’s history lift "
        "above 1 by construction — that is a mathematical consequence of basket size, not proof that products "
        "are bought together. Past logs cannot measure incremental sales from a shelf that did not yet exist. "
        f"Light buyers supply only {LIGHT_O} orders, so product-level rules inside that slice alone are thin. "
        f"A six-week 50/50 pilot yields about {PILOT_HALF_6W:.0f} serum-only orders per half — enough for a "
        f"safety check, not enough to separate a 5% add-on from 2% (about {PILOT_N_ARM} orders per half under "
        "a standard two-proportion power calculation at α≈0.05, 80% power).",
    )

    doc.add_heading("4. Findings", level=1)
    doc.add_heading("F1 · Order baskets vs history baskets", level=2)
    add_para(
        doc,
        f"At a comparable bar (≥14 orders vs ≥13 customers), single orders yield {ORDER_RULES} product rules; "
        f"whole histories yield {HIST_RULES} — every directed pair among 30 SKUs, all with lift > 1. Large history "
        f"baskets (avg {AVG_HIST} products) manufacture pairs whether or not customers buy them together. Histories "
        "answer “what has this customer ever tried?”; orders answer “what is bought together when the shelf appears?” "
        "Only the second matches the mini-program moment.",
    )
    add_figure(doc, FIG / "fig_rules_orders_vs_histories.png")
    add_caption(doc, f"Figure 3. At a comparable bar: {ORDER_RULES} order rules vs {HIST_RULES} history rules.")

    doc.add_heading("F2 · The only strong order rule: Serum → Cream", level=2)
    add_para(
        doc,
        f"{SC_BOTH} of {N_ORDERS:,} orders contain both Serum and Cream against about {SC_EXP:.0f} expected under "
        f"independence of the category rates (support {SC_SUP:.3f}, confidence {SC_CONF:.3f}, lift {SC_LIFT:.3f}). "
        f"Direction: Cream → Serum confidence is {CS_CONF:.3f}, so the shelf should show a cream after a serum. "
        "At ≥1% category support, Serum ↔ Cream is the only pair with lift > 1; the next pairs sit below 1 "
        "(e.g. Lip–Eye Care lift 0.64). This matches complementarity (T2). Product-level serum→cream pairs "
        "rank which cream to show first but rest on thin counts (17–27 orders).",
    )
    add_simple_table(
        doc,
        ["Rule", "Both / denom", "Support", "Conf.", "Lift", "Read as"],
        [
            [
                "Serum → Cream",
                f"{SC_BOTH} / {N_ORDERS:,} orders ({SC_BOTH} / {SC_SERUM} serum)",
                f"{SC_SUP:.3f}",
                f"{SC_CONF:.2f}",
                f"{SC_LIFT:.2f}",
                "Show cream after serum",
            ],
            [
                "Vit. C → Hydra Gel",
                f"{VC_HYDRA_BOTH} / {N_ORDERS:,} ({VC_HYDRA_BOTH} / {VC_N} Vit. C)",
                f"{VC_HYDRA_BOTH/N_ORDERS:.4f}",
                f"{VC_HYDRA_CONF:.2f}",
                f"{VC_HYDRA_LIFT:.2f}",
                "Cream rank #1 after Vit. C",
            ],
            [
                "Vit. C → Brightening",
                f"{VC_BRIGHT_BOTH} / {N_ORDERS:,} ({VC_BRIGHT_BOTH} / {VC_N} Vit. C)",
                f"{VC_BRIGHT_BOTH/N_ORDERS:.4f}",
                f"{VC_BRIGHT_CONF:.2f}",
                f"{VC_BRIGHT_LIFT:.2f}",
                "Cream rank #2 after Vit. C",
            ],
        ],
    )
    add_caption(
        doc,
        "Table 2. Selected order rules with co-purchase counts and denominators (frequency filters, not significance tests).",
    )
    add_figure(doc, FIG / "fig_serum_opportunity.png")
    add_caption(doc, "Figure 4. Monthly serum orders with vs without a cream.")
    add_para(
        doc,
        f"Hand check (Vitamin C Serum → Hydra Gel Cream): {VC_HYDRA_BOTH} of {N_ORDERS:,} orders contain both; "
        f"{VC_HYDRA_BOTH} of {VC_N} Vitamin C orders also contain the cream (confidence {VC_HYDRA_CONF:.2f}); "
        f"lift {VC_HYDRA_LIFT:.2f}. The mine() output matches the hand count. Because product confidence tops out "
        "near 0.14, SKU pairs are a ranking layer under the category rule, not standalone shelf engines. "
        f"Serum → Cream also holds in livestream (lift {SLICE['livestream'][3]:.2f}) and store "
        f"(lift {SLICE['store'][3]:.2f}).",
    )

    doc.add_heading("F3 · History rules are written by heavy buyers", level=2)
    add_para(
        doc,
        f"A history with n products creates n(n−1)/2 pairs. Heavy buyers average {AVG_PROD_H} products and supply "
        f"{EV_HEAVY}% of all pair evidence; light buyers are 46.5% of buyers but only {EV_LIGHT}% of the evidence "
        f"(average {AVG_PROD_L} products). This confirms T1. The pattern is robust at every heavy cut-off we tried.",
    )
    add_figure(doc, FIG / "fig1_history_evidence_by_buyer_type.png")
    add_caption(doc, "Figure 5. Who writes the history-based rules?")
    add_simple_table(
        doc,
        ["Heavy cut-off", "% of buyers", "% of history-rule evidence", "Serum→Cream lift (heavy)"],
        [[f"{c}+ orders", f"{b}%", f"{e}%", f"{L:.2f}"] for c, b, e, L in ROBUST],
    )
    add_caption(doc, "Table 3. Heavy-buyer dominance does not depend on the cut-off.")

    doc.add_heading("F4 · Top history pairs are not bought in the same order", level=2)
    add_para(
        doc,
        f"Inside single orders, top history pairs have lift < 1. Calming Toner Mist → Pore Refining Toner has "
        f"history lift {TONER_HIST_LIFT} but same-order lift {TONER_SAME_LIFT} "
        f"({TONER_SAME_BOTH} orders with both vs about {TONER_EXP:.0f} expected under independence). "
        "Heavy buyers try substitutes across visits; labelling those pairs “frequently bought together” would "
        "misdescribe the data. Caveat: some same-order counts are very small (single digits), so the "
        "same-order lift estimates are noisy — directionally below 1, but not precise effect sizes.",
    )
    add_figure(doc, FIG / "fig_history_vs_order_lift.png")
    add_caption(doc, "Figure 6. Top history pairs: high history lift, same-order lift below 1.")

    doc.add_heading("F5 · One shelf for everyone — if order-based", level=2)
    add_para(
        doc,
        f"Serum → Cream holds for light / mid / heavy "
        f"(lift {SLICE['light'][3]:.2f} / {SLICE['mid'][3]:.2f} / {SLICE['heavy'][3]:.2f}), "
        f"livestream and store ({SLICE['livestream'][3]:.2f} / {SLICE['store'][3]:.2f}), and on each customer’s "
        f"first order (support {FIRST_SUP:.3f}, confidence {FIRST_CONF:.3f}, lift {FIRST_LIFT:.3f}; "
        f"55 of 647 first orders contain both, among 129 first orders with a serum). "
        "A separate first-time shelf is unnecessary provided the shelf is mined from single orders (T2).",
    )
    add_figure(doc, FIG / "fig_serum_cream_slices.png")
    add_caption(doc, "Figure 7. Serum → Cream lift across buyer types, channels, and first orders.")
    add_simple_table(
        doc,
        ["Slice", "Orders", "Support", "Confidence", "Lift"],
        [
            ["buyer_type = light", str(SLICE["light"][0]), f"{SLICE['light'][1]:.3f}", f"{SLICE['light'][2]:.3f}", f"{SLICE['light'][3]:.2f}"],
            ["buyer_type = mid", str(SLICE["mid"][0]), f"{SLICE['mid'][1]:.3f}", f"{SLICE['mid'][2]:.3f}", f"{SLICE['mid'][3]:.2f}"],
            ["buyer_type = heavy", f"{SLICE['heavy'][0]:,}", f"{SLICE['heavy'][1]:.3f}", f"{SLICE['heavy'][2]:.3f}", f"{SLICE['heavy'][3]:.2f}"],
            ["channel = livestream", f"{SLICE['livestream'][0]:,}", f"{SLICE['livestream'][1]:.3f}", f"{SLICE['livestream'][2]:.3f}", f"{SLICE['livestream'][3]:.2f}"],
            ["channel = store", str(SLICE["store"][0]), f"{SLICE['store'][1]:.3f}", f"{SLICE['store'][2]:.3f}", f"{SLICE['store'][3]:.2f}"],
            ["first order only", "647", f"{FIRST_SUP:.3f}", f"{FIRST_CONF:.3f}", f"{FIRST_LIFT:.2f}"],
        ],
    )
    add_caption(doc, "Table 4. Serum → Cream across slices (all numbers from the notebook).")
    add_para(
        doc,
        "Stretch (Q15): mining category rules separately on light vs heavy order baskets still returns "
        "Serum → Cream as the primary rule in both poles. Two product shelves are not justified. "
        "What would change our mind before the pilot: Serum → Cream same-order lift ≤ 1 in a later month, "
        "or light-buyer confidence collapsing while heavy-buyer confidence holds. Neither appears in this quarter.",
    )

    doc.add_heading("F6 · What this means for the business", level=2)
    add_para(
        doc,
        "A history-trained shelf fails the “to whom?” part of Q15; the order-trained Serum → Cream rule passes "
        "every slice we ran, including buyers with no history. The yuan scenario is modest; the decision that "
        "matters is which evidence base trains the shelf. Relative to the 20 October plan: baskets are built "
        "two ways; segmentation uses intensity, not high_value spend; thresholds follow the shelf decision after "
        "the plan’s 2%/20% filters returned no usable product rules.",
    )

    doc.add_heading("5. Recommendation", level=1)
    add_para(
        doc,
        "Monday-morning decision. Mine the post-purchase shelf from single orders, not whole histories. "
        "After any serum purchase, show a cream. Use thin product pairs only to rank which cream appears first. "
        "One shelf for everyone — including buyers with no prior history. Fill remaining slots with products "
        f"light buyers buy most "
        f"({', '.join(f'{n} ({c} light orders)' for n,c in LIGHT_SLOTS)}) — "
        "not overall bestsellers driven by heavy-buyer volume. These leftover ranks come from notebook §10e; "
        "counts are in the tens, so they rank slots only.",
    )
    add_para(
        doc,
        "Operationally: (1) switch mining from user-history baskets to order baskets; (2) hard-code Serum → Cream "
        "as slot 1 whenever the basket contains a serum and no cream; (3) rank cream SKUs by order-level lift among "
        "serum→cream pairs with ≥14 supporting orders; (4) refresh leftover slots weekly from the light-buyer list.",
    )
    doc.add_heading("Shelf decision card", level=2)
    add_simple_table(
        doc,
        ["Element", "Serum → Cream (primary)", "Vit. C → Hydra Gel (SKU rank)"],
        [
            ["Trigger product", "Any serum in the current basket", "Vitamin C Serum in basket"],
            ["Intended customers", "All buyers, including first-time / light", "Serum buyers ranking creams"],
            ["Shelf position", "Slot 1 on post-purchase shelf", "Top cream after Vit. C"],
            [
                "Buyer with no history sees",
                f"Same cream recommendation (first-order lift {FIRST_LIFT:.2f})",
                "Same ranked cream if Vit. C was just bought",
            ],
            [
                "Evidence that rejects the rule",
                "Same-order lift ≤1 in a holdout month, or A/B add-on < 2% after the safety window",
                "Co-purchase count < 10 / quarter or lift ≤1 inside orders",
            ],
        ],
    )
    add_caption(doc, "Table 5. Translating rules into shelf decisions.")
    add_figure(doc, FIG / "fig_scenario_value.png", width_in=5.5)
    add_caption(doc, "Figure 8. Scenario value if 5–15% of serum-only orders add a cream (not a measured lift).")
    doc.add_heading("Expected results & condition that drops the action", level=2)
    add_bullets(
        doc,
        [
            "Design: from 1 Dec 2026, random half of buyers see the new shelf; half keep the current shelf.",
            f"Six-week safety check: about {PILOT_HALF_6W:.0f} serum-only orders per half "
            f"(≈{PILOT_HALF_6W*0.05:.0f} extra creams at 5%). Enough to catch failure or light buyers left behind; "
            "not enough to prove 5% vs 2%.",
            f"Uplift read: keep the split about {PILOT_MONTHS:.0f} months "
            f"(≈{PILOT_N_ARM} serum-only orders per half under a standard two-proportion calculation) "
            "before claiming 5% is distinct from 2%.",
            f"Expected result (after the longer window): ≥5% cream add-on among serum-only orders in treatment "
            f"(≈ ¥{SCEN[0.05]:,} / month at the low end), reported for first-time and repeat buyers.",
            "Drop if: (a) six-week add-on in treatment < 2% and not above control; (b) light / first-time add-on "
            "materially below heavy buyers’; (c) control-half re-mine shows Serum → Cream same-order lift ≤ 1.",
        ],
    )
    add_para(
        doc,
        "Where the recommendation stops. There is no second strong category pair. Do not invent a multi-rule "
        "carousel from history lifts. Do not claim the ¥ scenario as a measured effect.",
    )

    doc.add_heading("6. Ethics & compliance implications", level=1)
    add_para(
        doc,
        f"Stake. A history-trained shelf draws {EV_HEAVY}% of its pair evidence from heavy buyers, so "
        f"{LIGHT_B} light buyers (46.5%) would be served a catalogue that barely reflects their own behaviour.",
    )
    add_para(
        doc,
        "Who bears it. First-time and light buyers. Feedback-loop risk (untested on past logs): once live, the "
        "shelf can create the pairs it later mines.",
    )
    add_para(
        doc,
        "Misinformation. Labelling a history-based shelf “frequently bought together” would be false for the top "
        "history pairs (same-order lift < 1). Safeguard: label by what the shelf shows, e.g. “often bought in the "
        "same order”.",
    )
    add_para(
        doc,
        "Privacy. An order shelf needs only the current basket (PIPL data-minimisation). Under China’s 2022 "
        "Algorithmic Recommendation Provisions (Art. 17), offer an option not based on personal characteristics "
        "and an easy way to switch algorithmic recommendations off.",
    )
    add_para(
        doc,
        "Safeguard tied to the recommendation. Mine future rules on the control half of the A/B test, report "
        "add-on rates by buyer type, and drop under the conditions in §5.",
    )

    doc.add_heading("7. Artificial intelligence (AI) use appendix", level=1)
    add_para(
        doc,
        "Claude (Anthropic). Helped draft early notebook structure from Week 2 / Week 3 course patterns, "
        "proposed robustness checks (first-order slice, heavy cut-offs, shelf decision cards), and suggested "
        "manager-facing wording.",
    )
    add_para(
        doc,
        "Cursor (Composer). Helped revise code cells, rebuild charts in the Tongji-blue palette, generate the "
        "report and slide builders, and keep numbers aligned with notebook output after each data re-run.",
    )
    add_para(
        doc,
        "Team review. Every cell was re-run on the course Lumen Beauty CSVs; every shipped number was checked "
        "against notebook output. No platform personal data left the course environment.",
    )
    add_para(
        doc,
        "Every member of this team can explain every line of code and every number in this submission.",
    )


def build_main_docx(path: Path):
    doc = Document()
    set_doc_defaults(doc)
    add_para(doc, "Group Project Report", bold=True, center=True, size=16)
    add_para(
        doc,
        'What should the "you may also like" shelf show, and to whom?',
        center=True,
        size=12,
    )
    add_para(doc, "Association rules · Lumen Beauty (Sep–Nov 2026)", center=True, size=11, space_after=12)
    cover_table(doc)
    doc.add_paragraph("")
    fill_report_body_docx(doc)
    path.parent.mkdir(exist_ok=True)
    doc.save(str(path))
    print("wrote", path)


# ---------------- PDF (template sections 1–7, one file) ----------------
def pdf_styles():
    b = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "cover_title", parent=b["Heading1"], fontName="Times-Bold", fontSize=16, leading=20, alignment=TA_CENTER, spaceAfter=8,
            textColor=colors.HexColor("#003D7A"),
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub", parent=b["Normal"], fontName="Times-Roman", fontSize=11, leading=14, alignment=TA_CENTER, spaceAfter=4
        ),
        "h1": ParagraphStyle(
            "h1", parent=b["Heading1"], fontName="Times-Bold", fontSize=14, leading=18, spaceBefore=14, spaceAfter=8,
            textColor=colors.HexColor("#003D7A"),
        ),
        "h2": ParagraphStyle(
            "h2", parent=b["Heading2"], fontName="Times-Bold", fontSize=12, leading=15, spaceBefore=10, spaceAfter=6,
            textColor=colors.HexColor("#0066B3"),
        ),
        "body": ParagraphStyle(
            "body", parent=b["Normal"], fontName="Times-Roman", fontSize=12, leading=19, alignment=TA_JUSTIFY, spaceAfter=11
        ),
        "bullet": ParagraphStyle(
            "bullet", parent=b["Normal"], fontName="Times-Roman", fontSize=11.5, leading=16, leftIndent=12, spaceAfter=6
        ),
        "caption": ParagraphStyle(
            "caption", parent=b["Normal"], fontName="Times-Italic", fontSize=9.5, leading=12, alignment=TA_CENTER, spaceBefore=4, spaceAfter=10
        ),
        "table_cell": ParagraphStyle("table_cell", parent=b["Normal"], fontName="Times-Roman", fontSize=8.5, leading=11),
        "table_header": ParagraphStyle(
            "table_header", parent=b["Normal"], fontName="Times-Bold", fontSize=8.5, leading=11, textColor=colors.HexColor("#222222")
        ),
    }


def P(t, s):
    return Paragraph(t, s)


def bullets(items, style):
    return ListFlowable([ListItem(Paragraph(i, style), leftIndent=8) for i in items], bulletType="bullet", start="•", leftIndent=15)


def make_table(headers, rows, widths, cs, hs):
    white_hs = ParagraphStyle("tmp_white_hdr", parent=hs, textColor=colors.white)
    data = [[Paragraph(h, white_hs) for h in headers]] + [[Paragraph(str(c), cs) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0066B3")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#3978b6")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return t


def cover_flow(s):
    rows = [
        ["Team number", TEAM],
        ["Members", MEMBERS],
        ["Question ID", QUESTION],
        ["Date", DATE],
        ["Course", "New Media Technology and Analytics (20001920076) · Fall 2026 · Tongji SEM"],
    ]
    data = [[Paragraph(a, s["table_header"]), Paragraph(b, s["table_cell"])] for a, b in rows]
    t = Table(data, colWidths=[3.2 * cm, 13.0 * cm])
    t.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#3978b6")),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EEF1F3")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def fig(path, w=13.5 * cm, h=None):
    if not path.exists():
        return Spacer(1, 1)
    if h is None:
        return Image(str(path), width=w, kind="proportional")
    return Image(str(path), width=w, height=h)


def footer(c, d):
    c.saveState()
    c.setFont("Times-Roman", 8)
    c.drawCentredString(A4[0] / 2, 12 * mm, f"NMTA Team 5 · Q15 · {d.page}")
    c.restoreState()


def build_report_pdf(path: Path):
    s = pdf_styles()
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=2.4 * cm,
        rightMargin=2.4 * cm,
        topMargin=2.1 * cm,
        bottomMargin=2.1 * cm,
        title="Team 5 Q15 Report",
        author=TEAM,
    )
    story = []

    def H1(t):
        story.append(P(t, s["h1"]))

    def H2(t):
        story.append(P(t, s["h2"]))

    def B(t):
        story.append(P(t, s["body"]))

    def Cap(t):
        story.append(P(t, s["caption"]))

    story += [
        P("Group Project Report", s["cover_title"]),
        P('What should the "you may also like" shelf show, and to whom?', s["cover_sub"]),
        P("Association rules · Lumen Beauty (Sep–Nov 2026)", s["cover_sub"]),
        Spacer(1, 6),
        cover_flow(s),
        Spacer(1, 6),
        HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#0066B3")),
    ]

    H1("1. Problem & what it is worth")
    B(
        "After every purchase, Lumen Beauty’s Douyin mini-program shows a <i>you may also like</i> cross-sell shelf. "
        "The brand founder and the e-commerce merchandising team must decide which association rules earn a shelf slot, "
        "and whether first-time buyers should see a different shelf from frequent buyers."
    )
    B(
        f"In the cleaned quarter (1 Sep–30 Nov 2026) the store recorded <b>{N_ORDERS:,} orders</b>, <b>{N_BUYERS} buyers</b> "
        f"and <b>¥{GMV:,.2f}</b> GMV. <b>{PCT_SINGLE:.0f}%</b> of orders contain a single product ({N_SINGLE:,} of {N_ORDERS:,}). "
        f"On average <b>{SNC_MEAN:.0f} serum orders per month</b> leave without a cream "
        f"(Sep {SNC['2026-09']} / Oct {SNC['2026-10']} / Nov {SNC['2026-11']}). "
        f"If the shelf persuades 5–15% of those orders to add a cream (mean cream line ¥{CREAM_VAL:.2f}), the scenario "
        f"value is <b>¥{SCEN[0.05]:,}–{SCEN[0.15]:,} per month</b> (0.6–1.7% of monthly GMV). That yuan figure is a scenario, "
        "not a measured lift."
    )
    B(
        f"The sharper stake is in users. Heavy buyers (6+ orders) are 41.0% of buyers but place 80.3% of orders. "
        f"Light buyers (1–2 orders) are 46.5% of buyers — <b>{LIGHT_B} people</b> — but place only 10.8% of orders. "
        f"A history-trained shelf would serve those {LIGHT_B} light buyers using rules that draw only <b>{EV_LIGHT}%</b> "
        "of pair evidence from light buyers’ own histories."
    )
    B(
        f"<b>Unit of analysis.</b> Q15 requires two basket definitions: single orders and whole customer histories. "
        f"The figure {AVG_ORDER} is average <i>distinct products per order</i>, not units shipped."
    )

    H1("2. Data")
    B(
        f"Tables: <b>lb_order_lines.csv</b> ({N_LINES_RAW:,} rows before cleaning) and <b>lb_users.csv</b> (1,000 users). "
        "Streams, comments and follows are excluded. See <i>project_data_dictionary</i>."
    )
    H2("Cleaning choices")
    story.append(
        bullets(
            [
                f"<b>Duplicates:</b> {N_DUP} exact duplicate lines removed → {N_LINES:,} lines; GMV = ¥{GMV:,.2f}.",
                f"<b>Missing values:</b> empty <i>stream_id</i> on {EMPTY_STREAM:,} store lines = not applicable.",
                f"<b>Units:</b> qty ∈ {{1,2}}; unit_price ¥{PRICE_MIN:.2f}–¥{PRICE_MAX:.2f}.",
                f"<b>Outliers:</b> orders/buyer {N_ORD_MIN}–{N_ORD_MAX} (median {N_ORD_MED}); fence {FENCE}; none exceed it.",
                f"<b>Join / first-order check:</b> all {N_BUYERS} buyers map to <i>lb_users</i>; first-order dates match for all {N_BUYERS}.",
            ],
            s["bullet"],
        )
    )
    B(f"Channels: livestream {LIVE:,} orders; store {STORE}.")
    story.append(
        make_table(
            ["Buyer type", "Buyers", "Orders", "% buyers", "% orders"],
            [
                ["Light (1–2)", str(LIGHT_B), str(LIGHT_O), "46.5%", "10.8%"],
                ["Mid (3–5)", str(MID_B), str(MID_O), "12.5%", "8.9%"],
                ["Heavy (6+)", str(HEAVY_B), f"{HEAVY_O:,}", "41.0%", "80.3%"],
            ],
            [3.6 * cm, 2.4 * cm, 2.4 * cm, 3.0 * cm, 3.0 * cm],
            s["table_cell"],
            s["table_header"],
        )
    )
    Cap("Table 1. Buyer intensity segments (cut on <i>n_orders</i>).")
    story.append(fig(FIG / "fig_basket_size.png", 14 * cm, 7.0 * cm))
    Cap(f"Figure 1. Basket size: {PCT_SINGLE:.0f}% of orders contain a single product.")
    story.append(fig(FIG / "fig_buyers_vs_orders.png", 14 * cm, 7.1 * cm))
    Cap("Figure 2. Light buyers ≈ half of customers; heavy buyers place most orders.")
    B(
        f"Order baskets average <b>{AVG_ORDER}</b> distinct products "
        f"({SIZE_DIST[0]:,}/{SIZE_DIST[1]}/{SIZE_DIST[2]} with 1/2/3 products). "
        f"History baskets average <b>{AVG_HIST}</b>. Segmentation uses <i>n_orders</i>, not <i>high_value</i>."
    )

    H1("3. Method & assumptions")
    B(
        "Method family: <b>association rule mining</b> (Week 3), Apriori via <i>mlxtend</i> (≥0.23.4), pairs only. "
        "<b>Support and confidence filter observed frequency; they are not significance tests.</b> "
        "Every rule carries co-purchase count and denominator."
    )
    B(
        f"<b>Thresholds.</b> Order min_support = 0.4% (≥14/{N_ORDERS:,}). Category 1%. History 2% (≥13/{N_BUYERS}). "
        f"Plan’s 2% product support yields 0 product rules (largest pair support {MAX_PAIR_SUP:.2%})."
    )
    B(
        "<b>Theory.</b> (T1) STP: histories will be dominated by heavy buyers. (T2) Complementarity: Serum → Cream "
        "should show lift &gt; 1, cream-after-serum direction, across segments. Bias is the ethics stake (§6)."
    )
    B(
        f"<b>Limits.</b> Lift is a descriptive ratio under an independence benchmark, not a causal effect. "
        "Large history baskets push almost every history lift above 1 by construction. Past logs cannot measure a "
        f"shelf that did not exist. Light buyers supply only {LIGHT_O} orders. A six-week 50/50 pilot gives "
        f"≈{PILOT_HALF_6W:.0f} serum-only orders/half — a safety check, not a test that separates 5% from 2% "
        f"(≈{PILOT_N_ARM}/half under a standard two-proportion calculation)."
    )

    H1("4. Findings")
    H2("F1 · Order baskets vs history baskets")
    B(
        f"At a comparable bar: <b>{ORDER_RULES} order rules</b> vs <b>{HIST_RULES} history rules</b>. "
        "Only order baskets match the shelf moment."
    )
    story.append(fig(FIG / "fig_rules_orders_vs_histories.png", 13.8 * cm, 6.8 * cm))
    Cap(f"Figure 3. {ORDER_RULES} order rules vs {HIST_RULES} history rules.")

    H2("F2 · Serum → Cream")
    B(
        f"<b>{SC_BOTH} of {N_ORDERS:,} orders</b> contain both Serum and Cream vs ≈{SC_EXP:.0f} expected under "
        f"independence of category rates (support {SC_SUP:.3f}, confidence {SC_CONF:.3f}, <b>lift {SC_LIFT:.3f}</b>). "
        f"Cream → Serum confidence is {CS_CONF:.3f}. Only category pair with lift &gt; 1 at ≥1% support."
    )
    story.append(
        make_table(
            ["Rule", "Both / denom", "Support", "Conf.", "Lift", "Read as"],
            [
                ["Serum → Cream", f"{SC_BOTH}/{N_ORDERS:,}<br/>({SC_BOTH}/{SC_SERUM} serum)", f"{SC_SUP:.3f}", f"{SC_CONF:.2f}", f"{SC_LIFT:.2f}", "Cream after serum"],
                ["Vit. C → Hydra Gel", f"{VC_HYDRA_BOTH}/{N_ORDERS:,}<br/>({VC_HYDRA_BOTH}/{VC_N})", f"{VC_HYDRA_BOTH/N_ORDERS:.4f}", f"{VC_HYDRA_CONF:.2f}", f"{VC_HYDRA_LIFT:.2f}", "Cream rank #1"],
                ["Vit. C → Brightening", f"{VC_BRIGHT_BOTH}/{N_ORDERS:,}<br/>({VC_BRIGHT_BOTH}/{VC_N})", f"{VC_BRIGHT_BOTH/N_ORDERS:.4f}", f"{VC_BRIGHT_CONF:.2f}", f"{VC_BRIGHT_LIFT:.2f}", "Cream rank #2"],
            ],
            [3.1 * cm, 3.6 * cm, 1.7 * cm, 1.4 * cm, 1.3 * cm, 3.1 * cm],
            s["table_cell"],
            s["table_header"],
        )
    )
    Cap("Table 2. Selected order rules (counts from the notebook).")
    story.append(fig(FIG / "fig_serum_opportunity.png", 14 * cm, 7.0 * cm))
    Cap("Figure 4. Monthly serum orders with vs without a cream.")
    B(
        f"Hand check matches mine(): Vit. C → Hydra Gel both={VC_HYDRA_BOTH}, conf={VC_HYDRA_CONF:.2f}, "
        f"lift={VC_HYDRA_LIFT:.2f}. Also holds in livestream (lift {SLICE['livestream'][3]:.2f}) and store "
        f"({SLICE['store'][3]:.2f})."
    )

    H2("F3 · History rules written by heavy buyers")
    B(
        f"Heavy buyers average {AVG_PROD_H} products and supply <b>{EV_HEAVY}%</b> of history-pair evidence; "
        f"light buyers are 46.5% of buyers but only <b>{EV_LIGHT}%</b> of the evidence (T1)."
    )
    story.append(fig(FIG / "fig1_history_evidence_by_buyer_type.png", 14 * cm, 6.8 * cm))
    Cap("Figure 5. Who writes the history-based rules?")
    story.append(
        make_table(
            ["Heavy cut-off", "% buyers", "% evidence", "SC lift (heavy)"],
            [[f"{c}+", f"{b}%", f"{e}%", f"{L:.2f}"] for c, b, e, L in ROBUST],
            [3.5 * cm, 3.2 * cm, 4.5 * cm, 4.0 * cm],
            s["table_cell"],
            s["table_header"],
        )
    )
    Cap("Table 3. Robustness across heavy cut-offs.")

    H2("F4 · History pairs ≠ bought together")
    B(
        f"Top history pair Calming Toner Mist → Pore Refining Toner: history lift {TONER_HIST_LIFT}, "
        f"same-order lift {TONER_SAME_LIFT} ({TONER_SAME_BOTH} vs ≈{TONER_EXP:.0f} expected). "
        "Caveat: same-order counts are single-digit, so those lifts are noisy — directionally &lt; 1, not precise."
    )
    story.append(fig(FIG / "fig_history_vs_order_lift.png", 14.2 * cm, 6.8 * cm))
    Cap("Figure 6. History lift vs same-order lift for top history pairs.")

    H2("F5 · One shelf if order-based")
    B(
        f"Lift holds across slices: light/mid/heavy {SLICE['light'][3]:.2f}/{SLICE['mid'][3]:.2f}/{SLICE['heavy'][3]:.2f}; "
        f"first orders lift {FIRST_LIFT:.3f} (55 both among 129 first serum orders; {N_BUYERS} first orders total)."
    )
    story.append(fig(FIG / "fig_serum_cream_slices.png", 14.2 * cm, 6.6 * cm))
    Cap("Figure 7. Serum → Cream lift across slices.")
    story.append(
        make_table(
            ["Slice", "Orders", "Support", "Conf.", "Lift"],
            [
                ["light", str(SLICE["light"][0]), f"{SLICE['light'][1]:.3f}", f"{SLICE['light'][2]:.3f}", f"{SLICE['light'][3]:.2f}"],
                ["mid", str(SLICE["mid"][0]), f"{SLICE['mid'][1]:.3f}", f"{SLICE['mid'][2]:.3f}", f"{SLICE['mid'][3]:.2f}"],
                ["heavy", f"{SLICE['heavy'][0]:,}", f"{SLICE['heavy'][1]:.3f}", f"{SLICE['heavy'][2]:.3f}", f"{SLICE['heavy'][3]:.2f}"],
                ["livestream", f"{SLICE['livestream'][0]:,}", f"{SLICE['livestream'][1]:.3f}", f"{SLICE['livestream'][2]:.3f}", f"{SLICE['livestream'][3]:.2f}"],
                ["store", str(SLICE["store"][0]), f"{SLICE['store'][1]:.3f}", f"{SLICE['store'][2]:.3f}", f"{SLICE['store'][3]:.2f}"],
                ["first order", "647", f"{FIRST_SUP:.3f}", f"{FIRST_CONF:.3f}", f"{FIRST_LIFT:.2f}"],
            ],
            [3.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm],
            s["table_cell"],
            s["table_header"],
        )
    )
    Cap("Table 4. Serum → Cream across slices.")
    B(
        "Stretch: separate light vs heavy <i>order</i> shelves still return Serum → Cream as the primary rule. "
        "Two product shelves are not justified."
    )

    H2("F6 · Business reading")
    B(
        "History shelves fail “to whom?”; order-based Serum → Cream passes every slice, including buyers with no history. "
        "The decision that matters is which evidence base trains the shelf."
    )
    B(
        "Relative to the 20 October project plan, three corrections matter for the merchandising team. First, baskets "
        "are built two ways, not only by order_id. Second, segmentation uses order intensity, not high_value spend. "
        "Third, thresholds follow the shelf decision after the plan’s 2% / 20% filters returned no usable product rules. "
        f"At 0.4% support the {ORDER_RULES} surviving product rules all have lift ≥ {MIN_PROD_LIFT:.2f}."
    )
    B(
        "<b>What the data cannot tell us (limits carried into §5).</b> Association is not causation. The independence "
        "benchmark behind lift is a useful descriptive baseline, not a proof of complementarity in a causal sense. "
        f"Same-order checks on top history pairs rest on single-digit co-purchase counts "
        f"(e.g. {TONER_SAME_BOTH} orders for the top toner pair), so those lifts are noisy. "
        f"The ¥{SCEN[0.05]:,}–{SCEN[0.15]:,} monthly figure is a scenario only. "
        f"A six-week half (≈{PILOT_HALF_6W:.0f} serum-only orders) cannot separate a 5% add-on from 2%."
    )

    H1("5. Recommendation")
    B(
        "<b>Monday morning.</b> Mine from <b>single orders</b>. After any serum, show a cream. One shelf for everyone. "
        f"Leftover slots from light-buyer presence "
        f"({', '.join(f'{n} ({c})' for n,c in LIGHT_SLOTS)}) — notebook §10e; counts are tens, so ranking only."
    )
    H2("Shelf decision card")
    story.append(
        make_table(
            ["Element", "Serum → Cream", "Vit. C → Hydra Gel"],
            [
                ["Trigger", "Any serum in basket", "Vitamin C Serum in basket"],
                ["Customers", "Everyone, incl. first-time / light", "Serum buyers ranking creams"],
                ["Position", "Slot 1 post-purchase", "Top cream after Vit. C"],
                ["No history", f"Same shelf (first-order lift {FIRST_LIFT:.2f})", "Same if Vit. C just bought"],
                ["Reject if", "Lift ≤1 or A/B add-on &lt;2% after safety window", "Count &lt;10 / quarter or lift ≤1"],
            ],
            [2.8 * cm, 6.6 * cm, 6.6 * cm],
            s["table_cell"],
            s["table_header"],
        )
    )
    Cap("Table 5. Translating rules into shelf decisions.")
    story.append(fig(FIG / "fig_scenario_value.png", 13.5 * cm, 6.4 * cm))
    Cap("Figure 8. Scenario value if 5–15% of serum-only orders add a cream.")
    H2("Expected results & drop condition")
    story.append(
        bullets(
            [
                "Design: from 1 Dec 2026, 50/50 random split.",
                f"Six-week safety check: ≈{PILOT_HALF_6W:.0f} serum-only orders/half (≈{PILOT_HALF_6W*0.05:.0f} extra creams at 5%).",
                f"Uplift read: keep split ≈{PILOT_MONTHS:.0f} months (≈{PILOT_N_ARM} serum-only orders/half) before claiming 5% vs 2%.",
                f"Expected result (≥5% add-on after longer window): ≈¥{SCEN[0.05]:,}/month at the low end.",
                "Drop if: (a) six-week add-on &lt;2% and not above control; (b) light/first-time left behind; (c) control-half lift ≤1.",
            ],
            s["bullet"],
        )
    )

    H1("6. Ethics & compliance implications")
    B(
        f"<b>Stake.</b> History shelf evidence is {EV_HEAVY}% from heavy buyers → {LIGHT_B} light buyers get a heavy-buyer catalogue."
    )
    B("<b>Who bears it.</b> First-time and light buyers. Feedback loops once live are untested on past logs.")
    B(
        "<b>Misinformation.</b> Do not label cross-visit substitutes as “frequently bought together”. "
        "Safeguard: label “often bought in the same order”."
    )
    B(
        "<b>Privacy.</b> Order rules need only the current basket (PIPL minimisation). Art. 17: offer a non-profiled "
        "option and an easy opt-out."
    )
    B("<b>Safeguard.</b> Re-mine on the control half; report by buyer type; drop under §5.")

    H1("7. Artificial intelligence (AI) use appendix")
    B(
        "<b>Claude (Anthropic).</b> Helped draft early notebook structure from Week 2/3 patterns, proposed robustness "
        "checks, and suggested manager-facing wording."
    )
    B(
        "<b>Cursor (Composer).</b> Helped revise code, rebuild Tongji-blue charts, generate report/slide builders, "
        "and align numbers with notebook output."
    )
    B(
        "<b>Team review.</b> Every cell re-run on course CSVs; every shipped number checked against notebook output. "
        "No platform personal data left the course environment."
    )
    B("Every member of this team can explain every line of code and every number in this submission.")

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("wrote", path)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    build_main_docx(OUT / "NMTA_T05_report.docx")
    build_main_docx(OUT / "project_report.docx")
    # Template has §6–7 in the same report — no separate ethics appendix required for this build.
    # Keep a thin supporting appendix doc only for extra figures (optional).
    build_report_pdf(OUT / "NMTA_T05_report.pdf")
    build_report_pdf(OUT / "Team5_Q15_report.pdf")
    print("done")

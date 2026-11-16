#!/usr/bin/env python3
"""Build Word report + appendix (template structure) and one combined PDF."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
FIG = ROOT / "figures"
TEAM = "Team 5"
DATE = "2026-11-26"
MEMBERS = (
    "Nini Rizhamadze, Giulia Scarpa, Milena Moschetti, "
    "Thi Thuy Khuc, Lina-Sophie Reinsch, Hai Yen Bui"
)
QUESTION = 'Q15 — What should the "you may also like" shelf show, and to whom?'


# ---------- helpers: python-docx ----------
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
    for sname, size, bold in [
        ("Heading 1", 14, True),
        ("Heading 2", 12, True),
        ("Title", 16, True),
    ]:
        st = doc.styles[sname]
        st.font.name = "Times New Roman"
        st.font.size = Pt(size)
        st.font.bold = bold
        st.font.color.rgb = RGBColor(0x2A, 0x24, 0x21)


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
    p.paragraph_format.space_before = Pt(0)
    return p


def add_bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(item, style="List Bullet")
        for run in p.runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)


def add_caption(doc, text):
    add_para(doc, text, italic=True, center=True, size=10, space_after=10)


def add_figure(doc, path: Path, width_in=5.9):
    if path.exists():
        doc.add_picture(str(path), width=Inches(width_in))
        last = doc.paragraphs[-1]
        last.alignment = WD_ALIGN_PARAGRAPH.CENTER


def cover_table(doc):
    table = doc.add_table(rows=5, cols=2)
    table.style = "Table Grid"
    rows = [
        ("Team number", TEAM),
        ("Members", MEMBERS),
        ("Question ID", QUESTION),
        ("Date", DATE),
        (
            "Course",
            "New Media Technology and Analytics (20001920076) · Fall 2026 · Tongji SEM",
        ),
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


# ---------- Word: main report ----------
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
    add_para(
        doc,
        "Association rules · Lumen Beauty (Sep–Nov 2026)",
        center=True,
        size=11,
        space_after=12,
    )
    cover_table(doc)
    doc.add_paragraph("")

    doc.add_heading("1. Problem & what it is worth", level=1)
    add_para(
        doc,
        "After every purchase, Lumen Beauty’s Douyin mini-program shows a “you may also like” "
        "cross-sell shelf. The brand founder and the e-commerce merchandising team must decide "
        "which association rules earn a shelf slot, and whether the shelf should be the same for "
        "first-time buyers as for frequent ones.",
    )
    add_para(
        doc,
        "Across the cleaned quarter (1 Sep–30 Nov 2026) the store recorded 3,401 orders, 647 buyers "
        "and ¥1,171,735 GMV. 65% of orders contain a single product (2,219 of 3,401), so most "
        "checkouts leave an empty second slot. About 127 serum orders per month leave without a cream "
        "(Sep 137 / Oct 124 / Nov 121). If the shelf persuades 5–15% of those orders to add a cream "
        "(average cream line ¥347), the scenario value is ¥2,206–6,619 per month (0.6–1.7% of monthly GMV). "
        "That yuan figure is a scenario, not a measured lift.",
    )
    add_para(
        doc,
        "The sharper stake is in users. Heavy buyers (6+ orders) are 41% of buyers but place 80% of orders. "
        "Light buyers (1–2 orders) are 46.5% of buyers — 301 people — but place only 11% of orders. "
        "A shelf trained on whole purchase histories would serve those 301 light buyers using rules that are "
        "only 1.7% built from their own behaviour. Getting discovery wrong is therefore a targeting error: "
        "the store would position the shelf for its heaviest segment while nearly half of buyers are light.",
    )
    add_para(
        doc,
        "Unit of analysis. We mine rules on two basket definitions required by Q15: (1) single orders — "
        "the moment the shelf appears; (2) whole customer histories — every distinct product a buyer "
        "purchased in the quarter. The figure 1.45 is the average number of distinct products per order "
        "(order lines collapsed to unique SKUs), not units shipped.",
    )

    doc.add_heading("2. Data", level=1)
    add_para(
        doc,
        "We use two tables from the course project dataset (Lumen Beauty full Sep–Nov 2026 operations export; "
        "see project_data_dictionary): lb_order_lines.csv (4,920 rows before cleaning) and lb_users.csv "
        "(1,000 registered users). Auxiliary tables (streams, comments, follows) are excluded because basket "
        "co-purchase does not need them.",
    )
    doc.add_heading("Cleaning choices", level=2)
    add_bullets(
        doc,
        [
            "Duplicates: 5 exact duplicate order lines removed (export errors). 4,915 lines remain. GMV after cleaning = ¥1,171,735.",
            "Missing values: empty stream_id only on store orders (1,213 lines). Per the data dictionary this means “not applicable”, not missing data.",
            "Units: qty ∈ {1,2}; unit_price ¥54–505. Store list price is unique per SKU; paid/list ratios sit in 0.55–1.15 (livestream promotions).",
            "Outliers: orders per buyer 1–20 (median 3). Boxplot fence = 21; nobody exceeds it. Heavy buyers are kept — they are the group Q15 asks about.",
            "Join check: all 647 buyers map to lb_users; n_orders matches the order table for every buyer.",
        ],
    )
    add_para(
        doc,
        "Channels are livestream (2,579 orders) and store (822). Values such as search / short_video / ad belong to "
        "users.first_channel (arrival), not to where the order was placed.",
    )
    add_simple_table(
        doc,
        ["Buyer type", "Buyers", "Orders", "% of buyers", "% of orders"],
        [
            ["Light (1–2 orders)", "301", "366", "46.5%", "10.8%"],
            ["Mid (3–5)", "81", "304", "12.5%", "8.9%"],
            ["Heavy (6+)", "265", "2,731", "41.0%", "80.3%"],
        ],
    )
    add_caption(doc, "Table 1. Buyer intensity segments used for Q15 (cut on n_orders, not spend).")
    add_figure(doc, FIG / "fig_basket_size.png")
    add_caption(doc, "Figure 1. Basket size: 65% of orders contain a single product — the shelf’s opening.")
    add_figure(doc, FIG / "fig_buyers_vs_orders.png")
    add_caption(doc, "Figure 2. Light buyers are half the customers; heavy buyers place 80% of orders.")
    add_para(
        doc,
        "Order baskets average 1.45 distinct products (1 / 2 / 3 products: 2,219 / 850 / 332). History baskets "
        "average 6.27 products — more than four times larger — which is why history mining floods the rule table. "
        "Segmentation uses n_orders rather than high_value (spend-based), because Q15 asks whether frequent buyers "
        "dominate the rules — an intensity question, not a revenue-tier question.",
    )

    doc.add_heading("3. Method & assumptions", level=1)
    add_para(
        doc,
        "Method family: association rule mining (Week 3), Apriori via mlxtend (≥0.23.4; this run used 0.25.0), "
        "pairs only (max_len = 2) because the shelf answers one product with one product. Metrics: support, "
        "confidence, lift. Support and confidence filter observed co-purchase frequency; they are not tests of "
        "statistical significance. Beside every rule we report the co-purchase count and its denominator "
        "(orders or customers).",
    )
    add_para(
        doc,
        "Thresholds (decision-driven, not data-mined). The project plan’s 2% product support returns zero product "
        "rules on orders (largest pair support = 0.79%). We set order-level min_support = 0.4% (≥14 of 3,401 orders "
        "≈ one qualifying order per week over 13 weeks). Category rules use 1% (≥35 orders). History rules use the "
        "plan’s 2% (≥13 of 647 customers) so the two units of analysis face a comparable bar.",
    )
    add_para(
        doc,
        "Theory lens. Two testable predictions: (T1) STP targeting — if histories train the shelf, heavy buyers "
        "will dominate the evidence behind history rules; (T2) product complementarity in a skincare routine — "
        "serum and cream are sequential steps, so Serum → Cream should show lift > 1 with a clear direction "
        "(cream after serum) and should hold for light, mid and heavy buyers, on first orders, and in both "
        "livestream and store. Algorithmic bias is the ethics stake of a history-trained shelf (Appendix A1), "
        "not the explanation of why serum and cream co-occur.",
    )
    add_para(
        doc,
        "Assumptions & limits. Co-purchase is association, not causation. Past logs cannot measure incremental "
        "sales from a shelf that did not yet exist. Light buyers supply only 366 orders, so product-level rules "
        "inside that slice alone are thin; we trust the category rule more than SKU pairs. A six-week 50/50 pilot "
        "is large enough for a safety check, not large enough to separate a 5% add-on from 2% (see §5).",
    )

    doc.add_heading("4. Findings", level=1)
    doc.add_heading("F1 · Order baskets vs history baskets", level=2)
    add_para(
        doc,
        "At a comparable bar (≥14 orders vs ≥13 customers), single orders yield 30 product rules; whole histories "
        "yield 870 — every possible directed pair among 30 SKUs, all with lift > 1. Large history baskets "
        "(avg 6.27 products) manufacture pairs whether or not customers buy them together. Histories answer "
        "“what has this customer ever tried?”; orders answer “what is bought together when the shelf appears?” "
        "Only the second matches the mini-program moment.",
    )
    add_figure(doc, FIG / "fig_rules_orders_vs_histories.png")
    add_caption(doc, "Figure 3. At a comparable bar: 30 order rules vs 870 history rules.")

    doc.add_heading("F2 · The only strong order rule: Serum → Cream", level=2)
    add_para(
        doc,
        "At category level, 256 of 3,401 orders contain both Serum and Cream against ~147 expected by chance "
        "(support 0.075, confidence 0.40, lift 1.75). Direction matters: Cream → Serum confidence is only 0.33, "
        "so the shelf should show a cream after a serum. Every other category pair at ≥1% support has lift < 1. "
        "This matches the complementarity prediction (T2): the two steps go together, and the stronger direction "
        "is cream after serum. Product-level serum→cream pairs choose which cream to show first but rest on thin "
        "counts (15–27 orders).",
    )
    add_simple_table(
        doc,
        ["Rule", "Both / denom", "Support", "Conf.", "Lift", "Read as"],
        [
            ["Serum → Cream", "256 / 3,401 orders (256 / 638 serum)", "0.075", "0.40", "1.75", "Show cream after serum"],
            ["Vit. C Serum → Hydra Gel", "26 / 3,401 (26 / 188 Vit. C)", "0.0076", "0.14", "2.29", "Cream #1 after Vit. C"],
            ["Vit. C Serum → Brightening", "27 / 3,401 (27 / 188 Vit. C)", "0.0079", "0.14", "2.27", "Cream #2 after Vit. C"],
        ],
    )
    add_caption(
        doc,
        "Table 2. Selected order rules with co-purchase counts and denominators (filters = observed frequency, not significance tests).",
    )
    add_figure(doc, FIG / "fig_serum_opportunity.png")
    add_caption(doc, "Figure 4. Monthly serum orders with vs without a cream — the shelf’s addressable set.")
    add_para(
        doc,
        "Going beyond the menu question: Serum → Cream also holds inside livestream and store orders (lift 1.73 / 1.80). "
        "Unlike host-manufactured bundles that appear only on stream, this habit survives on the store shelf.",
    )

    doc.add_heading("F3 · History rules are written by heavy buyers", level=2)
    add_para(
        doc,
        "A history with n products creates n(n−1)/2 pairs. Heavy buyers average 11.7 products and supply 92.9% of all "
        "pair evidence; light buyers are 46.5% of buyers but only 1.7% of the evidence. This confirms T1. Robustness: "
        "at every heavy cut-off (4+, 6+, 8+, 10+ orders), heavy buyers’ share of evidence is two to three times their "
        "share of buyers (even at 10+: 21% of buyers, 63% of evidence).",
    )
    add_figure(doc, FIG / "fig1_history_evidence_by_buyer_type.png")
    add_caption(doc, "Figure 5. Who writes the history-based rules? Share of buyers vs share of pair evidence.")
    add_simple_table(
        doc,
        ["Heavy cut-off", "% of buyers", "% of history-rule evidence", "Serum→Cream lift (heavy)"],
        [
            ["4+ orders", "48.2%", "97.1%", "1.73"],
            ["6+ (main)", "41.0%", "92.9%", "1.72"],
            ["8+ orders", "32.8%", "83.3%", "1.71"],
            ["10+ orders", "21.2%", "62.8%", "1.61"],
        ],
    )
    add_caption(doc, "Table 3. The heavy-buyer dominance finding does not depend on the cut-off.")

    doc.add_heading("F4 · Top history pairs are not bought in the same order", level=2)
    add_para(
        doc,
        "Inside single orders, the top history pairs have lift < 1. Calming Toner Mist → Pore Refining Toner has "
        "history lift 2.15 but same-order lift 0.37 (3 orders with both vs ~8 expected). Heavy buyers try substitutes "
        "across visits; labelling those pairs “frequently bought together” would misdescribe the data.",
    )
    add_figure(doc, FIG / "fig_history_vs_order_lift.png")
    add_caption(doc, "Figure 6. Top history pairs: high history lift, same-order lift below 1.")

    doc.add_heading("F5 · One shelf serves new and occasional buyers — if order-based", level=2)
    add_para(
        doc,
        "Serum → Cream holds for light / mid / heavy (lift 1.79 / 1.93 / 1.72), livestream and store (1.73 / 1.80), "
        "and on each customer’s first order (confidence 0.43, lift 1.80). A separate first-time shelf is unnecessary "
        "provided the shelf is mined from single orders. That is T2 confirmed across segments.",
    )
    add_figure(doc, FIG / "fig_serum_cream_slices.png")
    add_caption(doc, "Figure 7. Serum → Cream lift across buyer types, channels, and first orders.")
    add_simple_table(
        doc,
        ["Slice", "Orders", "Support", "Confidence", "Lift"],
        [
            ["buyer_type = light", "366", "0.093", "0.410", "1.79"],
            ["buyer_type = mid", "304", "0.086", "0.456", "1.93"],
            ["buyer_type = heavy", "2,731", "0.072", "0.394", "1.72"],
            ["channel = livestream", "2,579", "0.074", "0.387", "1.73"],
            ["channel = store", "822", "0.080", "0.449", "1.80"],
            ["first order only", "647", "0.085", "0.426", "1.80"],
        ],
    )
    add_caption(doc, "Table 4. Serum → Cream across slices.")
    add_para(
        doc,
        "Stretch (Q15). Mining category rules separately on light vs heavy order baskets still returns Serum → Cream "
        "as the primary rule in both poles. The stretch therefore rejects two product shelves; it reinforces one "
        "order-based cream-after-serum shelf.",
    )

    doc.add_heading("F6 · What this means for the business", level=2)
    add_para(
        doc,
        "The data say that a history-trained shelf fails the “to whom?” part of Q15, while the order-trained "
        "Serum → Cream rule passes every slice we could run — including buyers with no history. The yuan scenario "
        "is modest; the decision that matters is which evidence base trains the shelf. Relative to the 20 October "
        "project plan, three corrections matter for the manager: baskets are built two ways; segmentation uses order "
        "intensity, not high_value spend; and thresholds are justified by the shelf decision after the plan’s "
        "2% / 20% filters returned no usable product rules.",
    )

    doc.add_heading("5. Recommendation", level=1)
    add_para(
        doc,
        "Monday-morning decision. Mine the post-purchase shelf from single orders, not from whole histories. "
        "After any serum purchase, show a cream. Use thin product pairs only to rank which cream appears first. "
        "One shelf for everyone — including buyers with no prior history. Fill remaining slots with products light "
        "buyers buy most (Clay Purifying Mask, Deep Clean Foam, Essence Toner, Cooling Eye Gel — see notebook §10e), "
        "not overall bestsellers driven by heavy-buyer volume.",
    )
    add_para(
        doc,
        "Operationally: (1) switch mining from user-history baskets to order baskets; (2) hard-code Serum → Cream as "
        "slot 1 whenever the basket contains a serum and no cream; (3) rank cream SKUs by order-level lift among "
        "serum→cream pairs with ≥14 supporting orders; (4) fill leftover slots from the light-buyer frequency list "
        "refreshed weekly.",
    )
    doc.add_heading("Shelf decision card", level=2)
    add_simple_table(
        doc,
        ["Element", "Serum → Cream (primary)", "Vit. C → Hydra Gel (SKU rank)"],
        [
            ["Trigger product", "Any serum in the current basket", "Vitamin C Serum in basket"],
            ["Intended customers", "All buyers, including first-time / light", "Serum buyers choosing among creams"],
            ["Shelf position", "Slot 1 on post-purchase shelf", "Slot 1 among cream candidates after Vit. C"],
            ["Buyer with no history sees", "Same cream recommendation (first-order lift 1.80)", "Same ranked cream if Vit. C was just bought"],
            [
                "Evidence that rejects the rule",
                "Same-order lift ≤1 in a holdout month, or A/B add-on < 2% after the safety window",
                "Co-purchase count < 10 / quarter or lift ≤1 inside orders",
            ],
        ],
    )
    add_caption(doc, "Table 5. Translating rules into shelf decisions.")
    add_figure(doc, FIG / "fig_scenario_value.png", width_in=5.6)
    add_caption(doc, "Figure 8. Scenario value if 5–15% of serum-only orders add a cream (not a measured lift).")

    doc.add_heading("Expected results & condition that drops the action", level=2)
    add_bullets(
        doc,
        [
            "Pilot design: from 1 Dec 2026, show the new shelf to a random half of buyers; keep the current shelf for the other half.",
            "Six-week safety check: each half sees only ~88–96 serum-only orders. At 5% conversion that is about 4–5 extra creams — enough to catch failure or light buyers left behind, not enough to prove 5% vs 2%.",
            "Uplift read: keep the split running about 40 weeks (~585 serum-only orders per half) before claiming a 5% add-on is distinguishable from 2%.",
            "Expected result (after the longer window): ≥5% of serum-only orders in treatment add a cream (~¥2,200 / month at the low end), reported for first-time and repeat buyers.",
            "Drop if: (a) six-week cream add-on in treatment is <2% and not higher than control; or (b) light / first-time add-on is materially below heavy buyers’; or (c) a re-mine on the control half shows Serum → Cream same-order lift ≤ 1.",
        ],
    )
    add_para(
        doc,
        "Where the recommendation stops. There is no second strong category pair. Do not invent a multi-rule carousel "
        "from history lifts. Do not personalise by full purchase history for new buyers. Do not claim the ¥2.2–6.6k "
        "figure as a measured effect. Ethics (A1) and AI-use disclosure (A2) follow in the appendix.",
    )

    path.parent.mkdir(exist_ok=True)
    doc.save(str(path))
    print("wrote", path)


def build_appendix_docx(path: Path):
    doc = Document()
    set_doc_defaults(doc)
    add_para(doc, "Appendix to the Group Project Report", bold=True, center=True, size=16)
    add_para(doc, f"{TEAM} · {QUESTION}", center=True, size=11)
    add_para(doc, DATE, center=True, size=11, space_after=12)
    cover_table(doc)
    doc.add_paragraph("")

    doc.add_heading("A1. Ethics & compliance implications", level=1)
    add_para(
        doc,
        "Stake. Algorithmic bias in the recommender: a history-trained shelf is 93% written by heavy buyers, so "
        "almost half of buyers (light / occasional — 301 people) would be served a shelf that does not reflect "
        "their behaviour.",
    )
    add_para(
        doc,
        "Who bears it. First-time and light buyers see recommendations shaped by customers who bought 6–20 times "
        "in the quarter. Feedback-loop risk (untested on past logs): once live, the shelf would create the pairs "
        "it later mines.",
    )
    add_para(
        doc,
        "Misinformation. Labelling a history-based shelf “frequently bought together” would be false for the top "
        "history pairs (same-order lift < 1). Safeguard: label the shelf by what it shows, e.g. “often bought in "
        "the same order”.",
    )
    add_para(
        doc,
        "Privacy. A history shelf profiles each customer’s full purchase record; an order shelf needs only the "
        "current basket (PIPL data-minimisation). Under China’s 2022 Algorithmic Recommendation Provisions "
        "(Art. 17), the store must offer an option not based on the user’s personal characteristics and an easy "
        "way to switch algorithmic recommendations off.",
    )
    add_para(
        doc,
        "Safeguard tied to the recommendation. Mine future rules only on the control half of the A/B test, report "
        "add-on rates by buyer type, and drop the action under the conditions in §5 of the main report.",
    )

    doc.add_heading("A2. Artificial intelligence (AI) use appendix", level=1)
    add_para(
        doc,
        "Claude (Anthropic). Helped draft early notebook structure from the Week 2 / Week 3 course patterns, "
        "proposed robustness checks (first-order slice, heavy cut-offs, shelf decision cards), and suggested "
        "wording for manager-facing findings.",
    )
    add_para(
        doc,
        "Cursor (Composer). Helped revise code cells, rebuild charts in the Lumen palette, generate the report and "
        "slide builders, and keep numbers aligned across notebook, report and slides after each data re-run.",
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

    doc.add_heading("A3. Supporting detail for the findings", level=1)
    add_para(
        doc,
        "Support dial on order baskets: at 5% / 2% / 1% product support → 0 rules; at 0.4% → 30 rules, all with "
        "lift > 1 (lowest 1.39). Largest product-pair support = 0.79%. History mining at 2% returns 870 rules. "
        "Serum-without-cream orders by month: Sep 137, Oct 124, Nov 121. Average cream line value ¥347. Scenario "
        "at 5% / 10% / 15% conversion: ¥2,206 / ¥4,412 / ¥6,619 per month. Pilot honesty: ~88–96 serum-only orders "
        "per half in six weeks; ~585 per half needed to separate 5% from 2% (~40 weeks).",
    )
    add_figure(doc, FIG / "fig_category_cooccurrence.png", width_in=5.2)
    add_caption(doc, "Figure A1. Same-order category co-occurrence (support). Serum ∩ Cream = 0.075 stands out.")
    add_figure(doc, FIG / "fig_channel_and_categories.png", width_in=5.6)
    add_caption(doc, "Figure A2. Channel mix and category presence (EDA).")
    add_figure(doc, FIG / "fig_robustness_heavy_cutoff.png", width_in=5.6)
    add_caption(doc, "Figure A3. Heavy-buyer share of history evidence at alternative cut-offs.")
    add_figure(doc, FIG / "fig_light_buyer_slots.png", width_in=5.6)
    add_caption(doc, "Figure A4. Leftover shelf slots: light-buyer SKU presence vs overall.")

    doc.save(str(path))
    print("wrote", path)


# ---------- Combined PDF (main then appendix) ----------
def pdf_styles():
    b = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "cover_title", parent=b["Heading1"], fontName="Times-Bold", fontSize=16, leading=20, alignment=TA_CENTER, spaceAfter=8
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub", parent=b["Normal"], fontName="Times-Roman", fontSize=11, leading=14, alignment=TA_CENTER, spaceAfter=4
        ),
        "h1": ParagraphStyle(
            "h1", parent=b["Heading1"], fontName="Times-Bold", fontSize=14, leading=18, spaceBefore=14, spaceAfter=8
        ),
        "h2": ParagraphStyle(
            "h2", parent=b["Heading2"], fontName="Times-Bold", fontSize=11.5, leading=14, spaceBefore=8, spaceAfter=5
        ),
        "body": ParagraphStyle(
            "body", parent=b["Normal"], fontName="Times-Roman", fontSize=12, leading=18, alignment=TA_JUSTIFY, spaceAfter=10
        ),
        "bullet": ParagraphStyle(
            "bullet", parent=b["Normal"], fontName="Times-Roman", fontSize=11.5, leading=16, leftIndent=12, spaceAfter=6
        ),
        "caption": ParagraphStyle(
            "caption", parent=b["Normal"], fontName="Times-Italic", fontSize=9.5, leading=12, alignment=TA_CENTER, spaceBefore=4, spaceAfter=10
        ),
        "table_cell": ParagraphStyle("table_cell", parent=b["Normal"], fontName="Times-Roman", fontSize=9, leading=11.5),
        "table_header": ParagraphStyle(
            "table_header",
            parent=b["Normal"],
            fontName="Times-Bold",
            fontSize=9,
            leading=11.5,
            textColor=colors.HexColor("#222222"),
        ),
        "table_header_blue": ParagraphStyle(
            "table_header_blue",
            parent=b["Normal"],
            fontName="Times-Bold",
            fontSize=9,
            leading=11.5,
            textColor=colors.white,
        ),
    }


def P(t, s):
    return Paragraph(t, s)


def bullets(items, style):
    return ListFlowable([ListItem(Paragraph(i, style), leftIndent=8) for i in items], bulletType="bullet", start="•", leftIndent=15)


def make_table(headers, rows, widths, cs, hs):
    # Data tables: white text on Tongji-blue header bar
    white_hs = ParagraphStyle(
        "tmp_white_hdr",
        parent=hs,
        textColor=colors.white,
    )
    data = [[Paragraph(h, white_hs) for h in headers]] + [
        [Paragraph(str(c), cs) for c in r] for r in rows
    ]
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


def fig(path, w=14 * cm, h=None):
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


def build_combined_pdf(path: Path):
    s = pdf_styles()
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=2.4 * cm,
        rightMargin=2.4 * cm,
        topMargin=2.0 * cm,
        bottomMargin=2.0 * cm,
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
        HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#333333")),
    ]

    H1("1. Problem & what it is worth")
    B(
        "After every purchase, Lumen Beauty’s Douyin mini-program shows a <i>you may also like</i> cross-sell shelf. "
        "The brand founder and the e-commerce merchandising team must decide which association rules earn a shelf slot, "
        "and whether the shelf should be the same for first-time buyers as for frequent ones."
    )
    B(
        "Across the cleaned quarter (1 Sep–30 Nov 2026) the store recorded <b>3,401 orders</b>, <b>647 buyers</b> and "
        "<b>¥1,171,735</b> GMV. <b>65%</b> of orders contain a single product (2,219 of 3,401). About <b>127 serum orders "
        "per month</b> leave without a cream (Sep 137 / Oct 124 / Nov 121). If the shelf persuades 5–15% of those orders "
        "to add a cream (average cream line ¥347), the scenario value is <b>¥2,206–6,619 per month</b> (0.6–1.7% of monthly GMV). "
        "That yuan figure is a scenario, not a measured lift."
    )
    B(
        "The sharper stake is in users. Heavy buyers (6+ orders) are 41% of buyers but place 80% of orders. Light buyers "
        "(1–2 orders) are 46.5% of buyers — <b>301 people</b> — but place only 11% of orders. A shelf trained on whole "
        "purchase histories would serve those 301 light buyers using rules that are only <b>1.7%</b> built from their own "
        "behaviour. That is a targeting error under STP."
    )
    B(
        "<b>Unit of analysis.</b> We mine rules on <i>two</i> basket definitions required by Q15: (1) single orders — the "
        "moment the shelf appears; (2) whole customer histories. The figure 1.45 is the average number of <i>distinct "
        "products per order</i>, not units shipped."
    )

    H1("2. Data")
    B(
        "We use <b>lb_order_lines.csv</b> (4,920 rows before cleaning) and <b>lb_users.csv</b> (1,000 registered users). "
        "Auxiliary tables are excluded because basket co-purchase does not need them."
    )
    H2("Cleaning choices")
    story.append(
        bullets(
            [
                "<b>Duplicates:</b> 5 exact duplicate order lines removed. 4,915 lines remain. GMV = ¥1,171,735.",
                "<b>Missing values:</b> empty <i>stream_id</i> only on store orders (1,213 lines) = not applicable.",
                "<b>Units:</b> qty ∈ {1,2}; unit_price ¥54–505.",
                "<b>Outliers:</b> orders per buyer 1–20 (median 3). Heavy buyers kept — they are the group Q15 asks about.",
                "<b>Join check:</b> all 647 buyers map to <i>lb_users</i>; <i>n_orders</i> matches for every buyer.",
            ],
            s["bullet"],
        )
    )
    story.append(
        make_table(
            ["Buyer type", "Buyers", "Orders", "% buyers", "% orders"],
            [
                ["Light (1–2)", "301", "366", "46.5%", "10.8%"],
                ["Mid (3–5)", "81", "304", "12.5%", "8.9%"],
                ["Heavy (6+)", "265", "2,731", "41.0%", "80.3%"],
            ],
            [3.6 * cm, 2.4 * cm, 2.4 * cm, 3.0 * cm, 3.0 * cm],
            s["table_cell"],
            s["table_header"],
        )
    )
    Cap("Table 1. Buyer intensity segments (cut on <i>n_orders</i>).")
    story.append(fig(FIG / "fig_basket_size.png", 14 * cm, 7.0 * cm))
    Cap("Figure 1. Basket size: 65% of orders contain a single product.")
    story.append(fig(FIG / "fig_buyers_vs_orders.png", 14 * cm, 7.2 * cm))
    Cap("Figure 2. Light buyers are half the customers; heavy buyers place 80% of orders.")
    B(
        "Order baskets average <b>1.45</b> distinct products (1 / 2 / 3 products: 2,219 / 850 / 332). History baskets "
        "average <b>6.27</b> products — more than four times larger — which is why history mining floods the rule table. "
        "Segmentation uses <i>n_orders</i> rather than <i>high_value</i> (spend-based), because Q15 asks whether frequent "
        "buyers dominate the rules — an intensity question, not a revenue-tier question."
    )
    B(
        "Channels are <b>livestream</b> (2,579 orders) and <b>store</b> (822). Values such as search / short_video / ad "
        "belong to <i>users.first_channel</i> (arrival), not to where the order was placed — a correction from the project plan. "
        "Extra channel and category charts live in Appendix A3 so the main text stays inside the page budget."
    )

    H1("3. Method & assumptions")
    B(
        "Method family: <b>association rule mining</b> (Week 3), Apriori via <i>mlxtend</i> (≥0.23.4), pairs only. "
        "<b>Support and confidence filter observed co-purchase frequency; they are not tests of statistical significance.</b> "
        "Beside every rule we report the co-purchase count and its denominator."
    )
    B(
        "<b>Thresholds.</b> Order-level <i>min_support</i> = <b>0.4%</b> (≥14 of 3,401 orders). Category rules use 1%. "
        "History rules use 2% (≥13 of 647 customers)."
    )
    B(
        "<b>Theory lens.</b> (T1) STP targeting — histories will be dominated by heavy buyers. (T2) Product complementarity "
        "in a skincare routine — Serum → Cream should show lift &gt; 1, cream-after-serum direction, and hold in every "
        "segment. Algorithmic bias is the ethics stake of a history-trained shelf (Appendix A1)."
    )
    B(
        "<b>Limits.</b> Association ≠ causation. A six-week 50/50 pilot is a safety check, not a full uplift test "
        "(~88–96 serum-only orders per half; ~585 per half needed to separate 5% from 2%)."
    )

    H1("4. Findings")
    H2("F1 · Order baskets vs history baskets")
    B(
        "At a comparable bar (≥14 orders vs ≥13 customers), single orders yield <b>30 product rules</b>; whole histories "
        "yield <b>870</b> — every possible directed pair among 30 SKUs, all with lift &gt; 1. Large history baskets "
        "(avg 6.27 products) manufacture pairs whether or not customers buy them together."
    )
    B(
        "This is the analytical heart of Q15. The same Apriori procedure, at almost the same minimum count, produces two "
        "incompatible shelves. The difference is not the algorithm; it is the basket definition. Histories answer "
        "“what has this customer ever tried?”; orders answer “what is bought together when the shelf appears?” Only the "
        "second matches the mini-program moment."
    )
    story.append(fig(FIG / "fig_rules_orders_vs_histories.png", 13.5 * cm, 6.8 * cm))
    Cap("Figure 3. At a comparable bar: 30 order rules vs 870 history rules.")

    H2("F2 · The only strong order rule: Serum → Cream")
    B(
        "At category level, <b>256 of 3,401 orders</b> contain both Serum and Cream against ~147 expected by chance "
        "(support 0.075, confidence 0.40, <b>lift 1.75</b>). Direction matters: Cream → Serum confidence is only 0.33, "
        "so the shelf should show a cream after a serum. Every other category pair at ≥1% support has lift &lt; 1. "
        "This matches the complementarity prediction (T2): the two steps go together, and the stronger direction is cream "
        "after serum. Product-level serum→cream pairs choose which cream to show first but rest on thin counts (15–27 orders)."
    )
    story.append(
        make_table(
            ["Rule", "Both / denom", "Support", "Conf.", "Lift", "Read as"],
            [
                ["Serum → Cream", "256 / 3,401<br/>(256 / 638 serum)", "0.075", "0.40", "1.75", "Cream after serum"],
                ["Vit. C → Hydra Gel", "26 / 3,401<br/>(26 / 188)", "0.0076", "0.14", "2.29", "Cream rank #1"],
                ["Vit. C → Brightening", "27 / 3,401<br/>(27 / 188)", "0.0079", "0.14", "2.27", "Cream rank #2"],
            ],
            [3.2 * cm, 3.8 * cm, 1.7 * cm, 1.4 * cm, 1.3 * cm, 3.2 * cm],
            s["table_cell"],
            s["table_header"],
        )
    )
    Cap("Table 2. Selected order rules with counts and denominators.")
    story.append(fig(FIG / "fig_serum_opportunity.png", 14 * cm, 7.0 * cm))
    Cap("Figure 4. Monthly serum orders with vs without a cream.")
    B(
        "Hand check (Vitamin C Serum → Hydra Gel Cream): 26 of 3,401 orders contain both (support 0.0076); 26 of 188 "
        "Vitamin C orders also contain the cream (confidence 0.14); chance predicts ~11 joint orders, we observe 26 "
        "(lift 2.29). The numbers from <i>mine()</i> match the hand count. Because product confidence tops out at 0.14, "
        "we treat SKU pairs as a ranking layer under the category rule, not as standalone shelf engines."
    )
    B(
        "Going beyond the menu question: Serum → Cream also holds inside livestream and store orders (lift 1.73 / 1.80). "
        "Unlike host-manufactured bundles that appear only on stream, this habit survives on the store shelf."
    )

    H2("F3 · History rules are written by heavy buyers")
    B(
        "A history with <i>n</i> products creates <i>n(n−1)/2</i> pairs. Heavy buyers average 11.7 products and supply "
        "<b>92.9%</b> of all pair evidence; light buyers are 46.5% of buyers but only <b>1.7%</b> of the evidence. "
        "Behind each of the top five history rules, 90–95% of backing customers are heavy. This confirms T1."
    )
    B(
        "Robustness: at every heavy cut-off (4+, 6+, 8+, 10+ orders), heavy buyers’ share of evidence is two to three "
        "times their share of buyers (even at 10+: 21% of buyers, 63% of evidence). The cut-off chart is in Appendix A3."
    )
    story.append(fig(FIG / "fig1_history_evidence_by_buyer_type.png", 14 * cm, 6.8 * cm))
    Cap("Figure 5. Who writes the history-based rules?")
    story.append(
        make_table(
            ["Heavy cut-off", "% buyers", "% history evidence", "Serum→Cream lift"],
            [
                ["4+ orders", "48.2%", "97.1%", "1.73"],
                ["6+ (main)", "41.0%", "92.9%", "1.72"],
                ["8+ orders", "32.8%", "83.3%", "1.71"],
                ["10+ orders", "21.2%", "62.8%", "1.61"],
            ],
            [3.5 * cm, 3.2 * cm, 4.8 * cm, 3.8 * cm],
            s["table_cell"],
            s["table_header"],
        )
    )
    Cap("Table 3. Heavy-buyer dominance does not depend on the cut-off.")

    H2("F4 · Top history pairs are not bought in the same order")
    B(
        "Inside single orders, the top history pairs have <b>lift &lt; 1</b>. Calming Toner Mist → Pore Refining Toner "
        "has history lift 2.15 but same-order lift 0.37 (3 orders with both vs ~8 expected). Heavy buyers try substitutes "
        "across visits; labelling those pairs “frequently bought together” would misdescribe the data."
    )
    story.append(fig(FIG / "fig_history_vs_order_lift.png", 14.2 * cm, 6.8 * cm))
    Cap("Figure 6. Top history pairs: high history lift, same-order lift below 1.")

    H2("F5 · One shelf for everyone — if order-based")
    B(
        "Serum → Cream holds for light / mid / heavy (lift 1.79 / 1.93 / 1.72), livestream and store (1.73 / 1.80), "
        "and on each customer’s <b>first order</b> (confidence 0.43, lift 1.80). A separate first-time shelf is unnecessary "
        "<i>provided</i> the shelf is mined from single orders. That is T2 confirmed across segments."
    )
    story.append(fig(FIG / "fig_serum_cream_slices.png", 14.2 * cm, 6.6 * cm))
    Cap("Figure 7. Serum → Cream lift across slices.")
    story.append(
        make_table(
            ["Slice", "Orders", "Support", "Conf.", "Lift"],
            [
                ["light", "366", "0.093", "0.410", "1.79"],
                ["mid", "304", "0.086", "0.456", "1.93"],
                ["heavy", "2,731", "0.072", "0.394", "1.72"],
                ["livestream", "2,579", "0.074", "0.387", "1.73"],
                ["store", "822", "0.080", "0.449", "1.80"],
                ["first order", "647", "0.085", "0.426", "1.80"],
            ],
            [3.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm],
            s["table_cell"],
            s["table_header"],
        )
    )
    Cap("Table 4. Serum → Cream across slices.")
    B(
        "<b>Stretch (Q15).</b> Mining category rules separately on light vs heavy <i>order</i> baskets still returns "
        "Serum → Cream as the primary rule in both poles, with lift well above 1. The stretch therefore rejects two "
        "product shelves; it reinforces one order-based cream-after-serum shelf."
    )
    B(
        "<b>What would change our mind before the pilot.</b> If a later month showed Serum → Cream same-order lift ≤ 1, "
        "or if light-buyer confidence collapsed while heavy-buyer confidence held, we would stop claiming one shelf for "
        "everyone. Neither appears in this quarter."
    )

    H2("F6 · What this means for the business")
    B(
        "A history-trained shelf fails the “to whom?” part of Q15, while the order-trained Serum → Cream rule passes "
        "every slice we could run — including buyers with no history. The yuan scenario is modest; the decision that "
        "matters is which evidence base trains the shelf."
    )
    B(
        "Relative to the 20 October project plan, three corrections matter for the merchandising team. First, baskets "
        "are built two ways, not only by order_id. Second, segmentation uses order intensity, not high_value spend. "
        "Third, thresholds are justified by the shelf decision after the plan’s 2% / 20% filters returned no usable "
        "product rules. Support is never described as statistically meaningful: it is a frequency filter, and every "
        "shipped rule carries its count and denominator."
    )

    H1("5. Recommendation")
    B(
        "<b>Monday-morning decision.</b> Mine the post-purchase shelf from <b>single orders</b>, not from whole histories. "
        "After any serum purchase, show a cream. Use thin product pairs only to rank which cream appears first. One shelf "
        "for everyone — including buyers with no prior history. Fill remaining slots with products light buyers buy most "
        "(Clay Purifying Mask, Deep Clean Foam, Essence Toner, Cooling Eye Gel — notebook §10e), not overall bestsellers "
        "driven by heavy-buyer volume."
    )
    B(
        "Operationally: (1) switch mining from user-history baskets to order baskets; (2) hard-code Serum → Cream as "
        "slot 1 whenever the basket contains a serum and no cream; (3) rank cream SKUs by order-level lift among "
        "serum→cream pairs with ≥14 supporting orders; (4) fill leftover slots from the light-buyer frequency list "
        "refreshed weekly."
    )
    H2("Shelf decision card")
    story.append(
        make_table(
            ["Element", "Serum → Cream", "Vit. C → Hydra Gel"],
            [
                ["Trigger", "Any serum in basket", "Vitamin C Serum in basket"],
                ["Customers", "Everyone, incl. first-time / light", "Serum buyers ranking creams"],
                ["Position", "Slot 1 post-purchase", "Top cream after Vit. C"],
                ["No history", "Same shelf (first-order lift 1.80)", "Same if Vit. C just bought"],
                ["Reject if", "Lift ≤1 or A/B add-on &lt;2% after safety window", "Count &lt;10 / quarter or lift ≤1"],
            ],
            [2.8 * cm, 6.6 * cm, 6.6 * cm],
            s["table_cell"],
            s["table_header"],
        )
    )
    Cap("Table 5. Translating rules into shelf decisions.")
    story.append(fig(FIG / "fig_scenario_value.png", 12.8 * cm, 6.2 * cm))
    Cap("Figure 8. Scenario value if 5–15% of serum-only orders add a cream.")
    H2("Expected results & drop condition")
    story.append(
        bullets(
            [
                "<b>Design:</b> from 1 Dec 2026, random half see the new shelf; half keep the current one.",
                "<b>Six-week safety check:</b> ~88–96 serum-only orders per half (≈4–5 extra creams at 5%) — catches failure or light buyers left behind; does not prove 5% vs 2%.",
                "<b>Uplift read:</b> keep the split ~40 weeks (~585 serum-only orders per half) before claiming 5% is distinct from 2%.",
                "<b>Expected result:</b> ≥5% cream add-on among serum-only orders in treatment (~¥2,200 / month at the low end).",
                "<b>Drop if:</b> (a) six-week add-on &lt;2% and not above control; (b) light / first-time left behind; (c) control-half re-mine lift ≤1.",
            ],
            s["bullet"],
        )
    )
    B(
        "Do not invent a multi-rule carousel from history lifts. Do not claim the ¥ figure as a measured effect. "
        "Ethics (A1) and AI disclosure (A2) follow in the appendix."
    )

    # ----- Appendix on new page -----
    story.append(PageBreak())
    story += [
        P("Appendix to the Group Project Report", s["cover_title"]),
        P(f"{TEAM} · {QUESTION}", s["cover_sub"]),
        P(DATE, s["cover_sub"]),
        Spacer(1, 6),
        cover_flow(s),
        Spacer(1, 6),
        HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#333333")),
    ]
    H1("A1. Ethics & compliance implications")
    B(
        "<b>Stake.</b> A history-trained shelf is 93% written by heavy buyers, so 301 light buyers would be served a "
        "shelf that does not reflect their behaviour."
    )
    B(
        "<b>Who bears it.</b> First-time and light buyers. Feedback-loop risk (untested): once live, the shelf would "
        "create the pairs it later mines."
    )
    B(
        "<b>Misinformation.</b> Do not label cross-visit substitutes as “frequently bought together”. "
        "Safeguard: label by what the shelf shows, e.g. “often bought in the same order”."
    )
    B(
        "<b>Privacy.</b> Order-based rules need only the current basket (PIPL minimisation). Under China’s 2022 "
        "Algorithmic Recommendation Provisions (Art. 17), offer an option not based on personal characteristics and "
        "an easy way to switch recommendations off."
    )
    B(
        "<b>Safeguard.</b> Mine future rules on the control half, report add-on rates by buyer type, and drop under §5 conditions."
    )

    H1("A2. Artificial intelligence (AI) use appendix")
    B(
        "<b>Claude (Anthropic).</b> Helped draft early notebook structure from Week 2 / Week 3 patterns, proposed "
        "robustness checks (first-order slice, heavy cut-offs, shelf decision cards), and suggested manager-facing wording."
    )
    B(
        "<b>Cursor (Composer).</b> Helped revise code cells, rebuild charts, generate report and slide builders, and "
        "keep numbers aligned across notebook, report and slides after each data re-run."
    )
    B(
        "<b>Team review.</b> Every cell was re-run on the course CSVs; every shipped number was checked against notebook output. "
        "No platform personal data left the course environment."
    )
    B("Every member of this team can explain every line of code and every number in this submission.")

    H1("A3. Supporting detail for the findings")
    B(
        "Support dial: at 5%/2%/1% product support → 0 rules; at 0.4% → 30 rules (lowest lift 1.39). History mining at "
        "2% → 870 rules. Serum-without-cream by month: 137 / 124 / 121. Cream line ¥347. Scenario ¥2,206 / ¥4,412 / ¥6,619. "
        "Pilot honesty: ~88–96 serum-only orders per half in six weeks; ~585 per half (~40 weeks) to separate 5% from 2%."
    )
    story.append(fig(FIG / "fig_category_cooccurrence.png", 11.5 * cm, 9.5 * cm))
    Cap("Figure A1. Same-order category co-occurrence (support).")
    story.append(fig(FIG / "fig_channel_and_categories.png", 13.5 * cm, 6.5 * cm))
    Cap("Figure A2. Channel mix and category presence (EDA).")
    story.append(fig(FIG / "fig_robustness_heavy_cutoff.png", 13.5 * cm, 6.2 * cm))
    Cap("Figure A3. Heavy-buyer share of history evidence at alternative cut-offs.")
    story.append(fig(FIG / "fig_light_buyer_slots.png", 13.5 * cm, 6.5 * cm))
    Cap("Figure A4. Leftover shelf slots: light-buyer SKU presence vs overall.")

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("wrote", path)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    build_main_docx(OUT / "NMTA_T05_report.docx")
    build_appendix_docx(OUT / "NMTA_T05_report_appendix.docx")
    # also keep template-friendly aliases
    build_main_docx(OUT / "project_report.docx")
    build_appendix_docx(OUT / "project_report_appendix.docx")
    build_combined_pdf(OUT / "NMTA_T05_report.pdf")
    build_combined_pdf(OUT / "Team5_Q15_report.pdf")
    print("done")

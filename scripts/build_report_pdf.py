#!/usr/bin/env python3
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import HRFlowable, Image, ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
FIG = ROOT / "figures" / "fig1_history_evidence_by_buyer_type.png"
TEAM, DATE = "Team 5", "2026-11-26"
MEMBERS = "Nini Rizhamadze, Giulia Scarpa, Milena Moschetti, Thi Thuy Khuc, Lina-Sophie Reinsch, Hai Yen Bui"
QUESTION = 'Q15 — What should the "you may also like" shelf show, and to whom?'

def styles():
    b = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle("cover_title", parent=b["Heading1"], fontName="Times-Bold", fontSize=16, leading=20, alignment=TA_CENTER, spaceAfter=8),
        "cover_sub": ParagraphStyle("cover_sub", parent=b["Normal"], fontName="Times-Roman", fontSize=11, leading=14, alignment=TA_CENTER, spaceAfter=4),
        "h1": ParagraphStyle("h1", parent=b["Heading1"], fontName="Times-Bold", fontSize=14, leading=18, spaceBefore=16, spaceAfter=10),
        "h2": ParagraphStyle("h2", parent=b["Heading2"], fontName="Times-Bold", fontSize=11.5, leading=14, spaceBefore=10, spaceAfter=6),
        "body": ParagraphStyle("body", parent=b["Normal"], fontName="Times-Roman", fontSize=12, leading=19, alignment=TA_JUSTIFY, spaceAfter=12),
        "bullet": ParagraphStyle("bullet", parent=b["Normal"], fontName="Times-Roman", fontSize=12, leading=18, leftIndent=12, spaceAfter=7),
        "caption": ParagraphStyle("caption", parent=b["Normal"], fontName="Times-Italic", fontSize=9.5, leading=12, alignment=TA_CENTER, spaceBefore=4, spaceAfter=12),
        "table_cell": ParagraphStyle("table_cell", parent=b["Normal"], fontName="Times-Roman", fontSize=9, leading=11.5),
        "table_header": ParagraphStyle("table_header", parent=b["Normal"], fontName="Times-Bold", fontSize=9, leading=11.5),
    }

def P(t, s): return Paragraph(t, s)

def bullets(items, style):
    return ListFlowable([ListItem(Paragraph(i, style), leftIndent=8) for i in items], bulletType="bullet", start="•", leftIndent=15)

def make_table(headers, rows, widths, cs, hs):
    data = [[Paragraph(h, hs) for h in headers]] + [[Paragraph(str(c), cs) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#efefef")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#666666")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t

def footer(c, d):
    c.saveState(); c.setFont("Times-Roman", 8); c.drawCentredString(A4[0]/2, 12*mm, f"NMTA Team 5 · Q15 · {d.page}"); c.restoreState()

def cover(s):
    rows = [["Team number", TEAM], ["Members", MEMBERS], ["Question ID", QUESTION], ["Date", DATE],
            ["Course", "New Media Technology and Analytics (20001920076) · Fall 2026 · Tongji SEM"]]
    data = [[Paragraph(a, s["table_header"]), Paragraph(b, s["table_cell"])] for a,b in rows]
    t = Table(data, colWidths=[3.2*cm, 12.8*cm])
    t.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#444444")),
        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#f3f3f3")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    return t

def build_main(path):
    s = styles()
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=2.4*cm, rightMargin=2.4*cm, topMargin=2.2*cm, bottomMargin=2.2*cm,
                            title="Team 5 Q15 Report", author=TEAM)
    story = []
    story += [P("Group Project Report", s["cover_title"]),
              P('What should the "you may also like" shelf show, and to whom?', s["cover_sub"]),
              P("Association rules · Lumen Beauty (Sep–Nov 2026)", s["cover_sub"]), Spacer(1,8), cover(s), Spacer(1,6),
              HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#333333"))]

    paras = []
    # content blocks as (style_key_or_special, text_or_obj)
    def H1(t): story.append(P(t, s["h1"]))
    def H2(t): story.append(P(t, s["h2"]))
    def B(t): story.append(P(t, s["body"]))
    def Cap(t): story.append(P(t, s["caption"]))

    H1("1. Problem & what it is worth")
    B("After every purchase, Lumen Beauty’s Douyin mini-program shows a <i>you may also like</i> cross-sell shelf. The brand founder and the e-commerce merchandising team must decide which association rules earn a shelf slot, and whether the shelf should be the same for first-time buyers as for frequent ones. Q15’s business risk is not only a missed add-on; it is a shelf that quietly mirrors the heaviest buyers.")
    B("Across the cleaned quarter (1 Sep–30 Nov 2026) the store recorded <b>3,401 orders</b>, <b>647 buyers</b> and <b>¥1,171,735</b> GMV. <b>65%</b> of orders contain a single product (2,219 of 3,401), so most checkouts leave with nothing added. About <b>127 serum orders per month</b> leave without a cream (Sep 137 / Oct 124 / Nov 121). If the shelf persuades 5–15% of those orders to add a cream (average cream line ¥347), the scenario value is <b>¥2,206–6,619 per month</b> (0.6–1.7% of monthly GMV). That yuan figure is a scenario, not a measured lift. The sharper stake is who trains the shelf: heavy buyers (6+ orders) are 41% of buyers but place 80% of orders; light buyers (1–2 orders) are 46.5% of buyers but place only 11% of orders.")
    B("Getting product discovery wrong is not abstract. A shelf trained on histories would allocate scarce recommendation slots to pairs that heavy buyers assemble across many visits — pairs light buyers almost never create. That is a targeting error under STP: the store would position the shelf for its heaviest segment while nearly half of buyers are light. The opportunity cost of the empty second slot on 2,219 single-product orders is the scenario above; the fairness cost is who the algorithm listens to.")
    B("<b>Unit of analysis (clarified).</b> We mine rules on <i>two</i> basket definitions required by Q15: (1) single orders — the moment the shelf appears; (2) whole customer histories — every distinct product a buyer purchased in the quarter. The figure 1.45 is the average number of <i>distinct products per order</i> (order lines collapsed to unique SKUs), not units shipped.")

    H1("2. Data")
    B("We use two tables from the course project dataset (Lumen Beauty full Sep–Nov 2026 operations export; see <i>project_data_dictionary</i>): <b>lb_order_lines.csv</b> (4,920 rows before cleaning) and <b>lb_users.csv</b> (1,000 registered users). Auxiliary tables (streams, comments, follows) are excluded because basket co-purchase does not need them.")
    H2("Cleaning choices")
    story.append(bullets([
        "<b>Duplicates:</b> 5 exact duplicate order lines removed (export errors). 4,915 lines remain. GMV after cleaning = ¥1,171,735 (the project plan’s ¥1,173,482 still counted duplicates).",
        "<b>Missing values:</b> empty <i>stream_id</i> only on store orders (1,213 lines). Per the data dictionary this means “not applicable”, not missing data.",
        "<b>Units:</b> qty ∈ {1,2}; unit_price ¥54–505. Store list price is unique per SKU; paid/list ratios sit in 0.55–1.15 (livestream promotions).",
        "<b>Outliers:</b> orders per buyer 1–20 (median 3). Boxplot fence = 21; nobody exceeds it. Heavy buyers are kept — they are the group Q15 asks about.",
        "<b>Join check:</b> all 647 buyers map to <i>lb_users</i>; <i>n_orders</i> matches the order table for every buyer.",
    ], s["bullet"]))
    story.append(Spacer(1,4))
    B("Channels are <b>livestream</b> (2,579 orders) and <b>store</b> (822). Values such as search / short_video / ad belong to <i>users.first_channel</i> (arrival), not to where the order was placed — a correction from the project plan.")
    story.append(make_table(["Buyer type","Buyers","Orders","% of buyers","% of orders"],
        [["Light (1–2 orders)","301","366","46.5%","10.8%"],["Mid (3–5)","81","304","12.5%","8.9%"],["Heavy (6+)","265","2,731","41.0%","80.3%"]],
        [4.0*cm,2.3*cm,2.3*cm,3.2*cm,3.2*cm], s["table_cell"], s["table_header"]))
    
    Cap("Table 1. Buyer intensity segments used for Q15 (cut on <i>n_orders</i>, not spend).")
    fig = ROOT / "figures" / "fig_basket_size.png"
    if fig.exists():
        story.append(Image(str(fig), width=14*cm, height=7.2*cm))
        Cap("Figure A. Basket size: 65% of orders contain a single product — the shelf's opening.")
    fig = ROOT / "figures" / "fig_buyers_vs_orders.png"
    if fig.exists():
        story.append(Image(str(fig), width=14*cm, height=7.4*cm))
        Cap("Figure B. Light buyers are half the customers; heavy buyers place 80% of orders.")

    B("Order baskets average <b>1.45 distinct products</b> (1 / 2 / 3 products: 2,219 / 850 / 332). History baskets average <b>6.27 products</b> — more than four times larger — which is why history mining floods the rule table.")
    B("Segmentation uses <i>n_orders</i> rather than <i>high_value</i> (spend-based), because Q15 asks whether frequent buyers dominate the rules — an intensity question, not a revenue-tier question. High-value flags still exist in <i>lb_users</i> (top 20% by spend, 130 users) but are not the cut that answers “to whom?” for this shelf. The chart that makes the business question visible is Figure 1 in §4: the gap between share of buyers and share of history-pair evidence.")

    H1("3. Method & assumptions")
    B("Method family: <b>association rule mining</b> (Week 3), Apriori via <i>mlxtend</i>, pairs only (<i>max_len</i> = 2) because the shelf answers one product with one product. Metrics: support, confidence, lift. <b>Support and confidence filter observed co-purchase frequency; they are not tests of statistical significance.</b> Beside every rule we report the co-purchase count and its denominator (orders or customers).")
    B("<b>Thresholds (decision-driven, not data-mined).</b> The project plan’s 2% product support returns zero product rules on orders (largest pair support = 0.79%). We set order-level <i>min_support</i> = <b>0.4%</b> (≥14 of 3,401 orders ≈ one qualifying order per week over 13 weeks). Category rules use 1% (≥35 orders). History rules use the plan’s 2% (≥13 of 647 customers) so the two units of analysis face a comparable bar. The plan’s 20% confidence filter is dropped for product rules (best confidence = 0.14); the category rule Serum → Cream still clears it (confidence 0.40).")
    B("<b>Theory lens.</b> Recommender algorithmic bias + STP targeting. Two testable predictions: (T1) if histories train the shelf, heavy buyers will dominate the evidence behind history rules; (T2) if one undifferentiated shelf is justified, Serum → Cream should hold for light, mid and heavy buyers and on first orders. A third effect — the live shelf creating the pairs it later mines — cannot be tested on past logs.")
    B("<b>Assumptions & limits.</b> Co-purchase is association, not causation. Past logs cannot measure incremental sales from a shelf that did not yet exist. Light buyers supply only 366 orders, so product-level rules inside that slice alone are thin; we trust the category rule more than SKU pairs.")

    H2("How we read a rule")
    B("For every candidate rule A → B we require three numbers in plain language: how many baskets contain both (the numerator), how many baskets form the base (the denominator for support), and how many baskets contain A (the denominator for confidence). Lift then asks whether that confidence exceeds B’s base rate. A rule can clear a support filter and still be useless for the shelf if lift ≤ 1, or if the pair is an artefact of large history baskets. That reading discipline is why Table 2 always shows both / denom beside support and confidence.")
    B("We deliberately avoid p-values on association rules. With thousands of possible pairs, significance testing without a pre-registered hypothesis would invite false discoveries. The shelf decision needs stable, interpretable co-purchase — which is why we demand a minimum weekly count and a lift above chance, then translate survivors into operational cards.")

    H1("4. Findings")
    H2("F1 · Order baskets vs history baskets")
    B("At a comparable bar (≥14 orders vs ≥13 customers), single orders yield <b>30 product rules</b>; whole histories yield <b>870</b> — every possible directed pair among 30 SKUs, all with lift &gt; 1. Large history baskets (avg 6.27 products) manufacture pairs whether or not customers buy them together. A rule set that every pair passes cannot tell the shelf what to show.")
    B("This is the analytical heart of Q15. The same Apriori procedure, at almost the same minimum count, produces two incompatible shelves. The difference is not the algorithm; it is the basket definition. Histories answer “what has this customer ever tried?”; orders answer “what is bought together when the shelf appears?” Only the second matches the mini-program moment.")
    fig = ROOT / "figures" / "fig_rules_orders_vs_histories.png"
    if fig.exists():
        story.append(Image(str(fig), width=13*cm, height=6.8*cm))
        Cap("Figure E. At a comparable bar: 30 order rules vs 870 history rules.")


    H2("F2 · The only strong order rule: Serum → Cream")
    B("At category level, <b>256 of 3,401 orders</b> contain both Serum and Cream against ~147 expected by chance (support 0.075, confidence 0.40, <b>lift 1.75</b>). Direction matters: Cream → Serum confidence is only 0.33, so the shelf should show a cream after a serum. Every other category pair at ≥1% support has lift &lt; 1 (e.g. Lip–Eye Care 0.64). Product-level serum→cream pairs choose which cream to show first but rest on thin counts (15–27 orders).")
    story.append(make_table(["Rule","Both / denom","Support","Conf.","Lift","Read as"],
        [["Serum → Cream","256 / 3,401 orders<br/>(256 / 638 serum orders)","0.075","0.40","1.75","Show cream after serum"],
         ["Vit. C Serum → Hydra Gel","26 / 3,401<br/>(26 / 188 Vit. C)","0.0076","0.14","2.29","Cream #1 after Vit. C"],
         ["Vit. C Serum → Brightening","27 / 3,401<br/>(27 / 188 Vit. C)","0.0079","0.14","2.27","Cream #2 after Vit. C"]],
        [3.4*cm,4.0*cm,1.7*cm,1.4*cm,1.3*cm,3.4*cm], s["table_cell"], s["table_header"]))
    Cap("Table 2. Selected order rules with co-purchase counts and denominators (filters = observed frequency, not significance tests).")
    fig = ROOT / "figures" / "fig_category_cooccurrence.png"
    if fig.exists():
        story.append(Image(str(fig), width=12.5*cm, height=10.5*cm))
        Cap("Figure C. Same-order category co-occurrence (support). Serum ∩ Cream = 0.075 stands out.")
    fig = ROOT / "figures" / "fig_serum_opportunity.png"
    if fig.exists():
        story.append(Image(str(fig), width=14*cm, height=7.4*cm))
        Cap("Figure D. Monthly serum orders with vs without a cream — the shelf's addressable set.")

    B("Hand check (Vitamin C Serum → Hydra Gel Cream): 26 of 3,401 orders contain both (support 0.0076); 26 of 188 Vitamin C orders also contain the cream (confidence 0.14); chance predicts ~11 joint orders, we observe 26 (lift 2.29). The numbers from <i>mine()</i> match the hand count, so the pipeline is faithful to Week 3. Because product confidence tops out at 0.14, we do <i>not</i> treat SKU pairs as standalone shelf engines — only as a ranking layer under the category rule.")
    B("Going beyond the menu question: we also re-read Serum → Cream inside livestream vs store orders. Lift remains above 1.7 in both. Unlike host-manufactured bundles that appear only on stream, this habit survives on the store shelf, so it is a customer pattern rather than a presenter artefact.")

    H2("F3 · History rules are written by heavy buyers")
    B("A history with <i>n</i> products creates <i>n(n−1)/2</i> pairs. Heavy buyers average 11.7 products and supply <b>92.9%</b> of all pair evidence; light buyers are 46.5% of buyers but only <b>1.7%</b> of the evidence. Behind each of the top five history rules, 90–95% of backing customers are heavy. Robustness: at every heavy cut-off (4+, 6+, 8+, 10+ orders), heavy buyers’ share of evidence is two to three times their share of buyers (even at 10+: 21% of buyers, 63% of evidence).")
    if FIG.exists():
        story.append(Image(str(FIG), width=14*cm, height=7*cm))
        Cap("Figure 1. Who writes the history-based rules? Share of buyers vs share of pair evidence, by buyer type.")
    story.append(make_table(["Heavy cut-off","% of buyers","% of history-rule evidence","Serum→Cream lift (heavy)"],
        [["4+ orders","48.2%","97.1%","1.73"],["6+ (main)","41.0%","92.9%","1.72"],["8+ orders","32.8%","83.3%","1.71"],["10+ orders","21.2%","62.8%","1.61"]],
        [3.5*cm,3.3*cm,5.2*cm,4.2*cm], s["table_cell"], s["table_header"]))
    Cap("Table 3. The heavy-buyer dominance finding does not depend on the cut-off.")

    H2("F4 · Top history pairs are not bought in the same order")
    B("Inside single orders, the top history pairs have <b>lift &lt; 1</b>. Calming Toner Mist → Pore Refining Toner has history lift 2.15 but same-order lift 0.37 (3 orders with both vs ~8 expected). Heavy buyers try substitutes across visits; labelling those pairs “frequently bought together” would misdescribe the data.")
    fig = ROOT / "figures" / "fig_history_vs_order_lift.png"
    if fig.exists():
        story.append(Image(str(fig), width=14.5*cm, height=7.2*cm))
        Cap("Figure F. Top history pairs: high history lift, same-order lift below 1.")


    H2("F5 · One shelf serves new and occasional buyers — if order-based")
    B("Serum → Cream holds for light / mid / heavy (lift 1.79 / 1.93 / 1.72), livestream and store (1.73 / 1.80), and on each customer’s <b>first order</b> (confidence 0.43, lift 1.80). A separate first-time shelf is unnecessary <i>provided</i> the shelf is mined from single orders.")
    fig = ROOT / "figures" / "fig_serum_cream_slices.png"
    if fig.exists():
        story.append(Image(str(fig), width=14.5*cm, height=7.0*cm))
        Cap("Figure G. Serum → Cream lift across buyer types, channels, and first orders.")

    story.append(make_table(["Slice","Orders","Support","Confidence","Lift"],
        [["buyer_type = light","366","0.093","0.410","1.79"],["buyer_type = mid","304","0.086","0.456","1.93"],
         ["buyer_type = heavy","2,731","0.072","0.394","1.72"],["channel = livestream","2,579","0.074","0.387","1.73"],
         ["channel = store","822","0.080","0.449","1.80"],["first order only","647","0.085","0.426","1.80"]],
        [4.5*cm,2.3*cm,2.3*cm,2.8*cm,2.3*cm], s["table_cell"], s["table_header"]))
    Cap("Table 4. Serum → Cream across slices.")
    B("<b>Stretch (Q15).</b> Mining category rules separately on light vs heavy <i>order</i> baskets still returns Serum → Cream as the primary rule in both poles, with lift well above 1. The stretch therefore rejects two product shelves; it reinforces one order-based cream-after-serum shelf.")
    B("<b>What would change our mind before the pilot.</b> If a later month showed Serum → Cream same-order lift ≤ 1, or if light-buyer confidence collapsed while heavy-buyer confidence held, we would stop claiming one shelf for everyone. Neither appears in this quarter.")
    
    H2("F6 · What this means for the business argument")
    B("Three questions decide whether an NMTA project succeeds: what the question is worth, what the data say, and what someone should do differently on Monday morning. The data say that the history-trained shelf fails the \"to whom?\" part of Q15, while the order-trained Serum → Cream rule passes every slice we could run — including buyers with no history. The yuan scenario is modest; the decision that matters is which evidence base trains the shelf.")
    B("Relative to the project plan (20 Oct 2026), three corrections matter. First, baskets are built two ways, not only by order_id. Second, segmentation uses order intensity, not high_value spend. Third, thresholds are justified by the shelf decision after the plan’s 2% / 20% filters returned no usable product rules. Support is never described as \"statistically meaningful\": it is a frequency filter, and every shipped rule carries its count and denominator.")
    B("Relative to the instructor email: expected results and the drop condition are stated in §5; shelf decision cards name trigger, customers, position, the no-history view, and reject evidence; AI tools are named in the appendix. We go beyond the menu by comparing livestream vs store, first orders, and the light-vs-heavy stretch shelf.")

    H1("5. Recommendation")
    B("<b>Monday-morning decision.</b> Mine the post-purchase shelf from <b>single orders</b>, not from whole histories. After any serum purchase, show a cream. Use thin product pairs only to rank which cream appears first. One shelf for everyone — including buyers with no prior history. Fill remaining slots with products light buyers buy most, not overall bestsellers (bestsellers are 80% written by heavy buyers’ order volume).")
    B("Operationally: (1) switch mining from user-history baskets to order baskets; (2) hard-code Serum → Cream as slot 1 whenever the basket contains a serum and no cream; (3) rank cream SKUs by order-level lift among serum→cream pairs with ≥14 supporting orders; (4) fill leftover slots from the light-buyer frequency list refreshed weekly.")
    H2("Shelf decision card (selected rules)")
    story.append(make_table(["Element","Serum → Cream (primary)","Vit. C → Hydra Gel (SKU rank)"],
        [["Trigger product","Any serum in the current basket","Vitamin C Serum in basket"],
         ["Intended customers","All buyers, including first-time / light","Serum buyers choosing among creams"],
         ["Shelf position","Slot 1 on post-purchase shelf","Slot 1 among cream candidates after Vit. C"],
         ["Buyer with no history sees","Same cream recommendation (first-order lift 1.80)","Same ranked cream if Vit. C was just bought"],
         ["Evidence that rejects the rule","Same-order lift ≤1 in a holdout month, or A/B add-on &lt; 2% for six weeks","Co-purchase count &lt; 10 / quarter or lift ≤1 inside orders"]],
        [3.1*cm,6.4*cm,6.4*cm], s["table_cell"], s["table_header"]))
    Cap("Table 5. Translating rules into shelf decisions.")
    fig = ROOT / "figures" / "fig_scenario_value.png"
    if fig.exists():
        story.append(Image(str(fig), width=13.5*cm, height=7.0*cm))
        Cap("Figure H. Scenario value if 5–15% of serum-only orders add a cream (not a measured lift).")
    H2("Expected results & condition that drops the action")
    story.append(bullets([
        "<b>Pilot:</b> from 1 Dec 2026, show the new shelf to a random half of buyers for six weeks; keep the current shelf for the other half.",
        "<b>Expected result:</b> ≥5% of serum-only orders in the treatment half add a cream (~¥2,200 / month at the low end), reported separately for first-time and repeat buyers.",
        "<b>Drop condition:</b> stop if (a) six-week cream add-on rate in treatment is &lt; 2% and not higher than control, or (b) light / first-time add-on rate is materially below heavy buyers’, or (c) a re-mine on the control half shows Serum → Cream same-order lift ≤ 1.",
    ], s["bullet"]))
    H2("Where the recommendation stops")
    B("There is no second strong category pair. Do not invent a multi-rule carousel from history lifts. Do not personalise by full purchase history for new buyers. Do not claim the ¥2.2–6.6k figure as a measured effect. The pilot is the measurement. If the kill conditions fire, revert to the prior shelf and re-open the analysis with the next quarter’s orders — still on order baskets, not histories.")
    B("Ethics (§6) and AI-use disclosure (§7) are in the separate appendix, per the instructor’s 12 November formatting note.")

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("wrote", path)

def build_appendix(path):
    s = styles()
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=2.4*cm, rightMargin=2.4*cm, topMargin=2.2*cm, bottomMargin=2.2*cm,
                            title="Team 5 Q15 Appendix", author=TEAM)
    story = [P("Appendix to the Group Project Report", s["cover_title"]),
             P(f"{TEAM} · {QUESTION}", s["cover_sub"]), P(DATE, s["cover_sub"]), Spacer(1,6), cover(s), Spacer(1,8),
             HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#333333"))]
    def H1(t): story.append(P(t, s["h1"]))
    def B(t): story.append(P(t, s["body"]))
    H1("6. Ethics & compliance implications")
    B("<b>Stake.</b> Algorithmic bias in the recommender: a history-trained shelf is 93% written by heavy buyers, so almost half of buyers (light / occasional) would be served a shelf that does not reflect their behaviour.")
    B("<b>Who bears it.</b> First-time and light buyers see recommendations shaped by customers who bought 6–20 times in the quarter. Feedback-loop risk (untested): once live, the shelf would create the pairs it later mines.")
    B("<b>Misinformation.</b> Labelling a history-based shelf “frequently bought together” would be false for the top history pairs (same-order lift &lt; 1). Safeguard: label the shelf by what it shows, e.g. “often bought in the same order”.")
    B("<b>Privacy.</b> A history shelf profiles each customer’s full purchase record; an order shelf needs only the current basket (PIPL data-minimisation). Under China’s 2022 Algorithmic Recommendation Provisions (Art. 17), the store must offer an option not based on the user’s profile and an easy way to switch recommendations off.")
    B("<b>Safeguard tied to the recommendation.</b> Mine future rules only on the control half of the A/B test, report add-on rates by buyer type, and drop the action under the conditions in §5 of the main report.")
    H1("7. Artificial intelligence (AI) use appendix")
    B("We used <b>Claude (Anthropic)</b> and <b>Cursor (Composer)</b> to help draft and revise notebook code, the report outline, the final report text, and the pitch slides; to propose robustness checks (first-order slice, heavy-buyer cut-off table, A/B kill conditions, shelf decision cards); and to format tables and figures. The team reviewed every cell and every number against the notebook outputs from the official Lumen Beauty course dataset. No platform personal data left the course environment.")
    B("Every member of this team can explain every line of code and every number in this submission.")
    H1("A. Supporting detail for the findings")
    B("Support dial on order baskets: at 5% / 2% / 1% product support → 0 rules; at 0.4% → 30 rules, all with lift &gt; 1 (lowest 1.39). Largest product-pair support = 0.79%. History mining at 2% returns 870 rules. Serum-without-cream orders by month: Sep 137, Oct 124, Nov 121. Average cream line value ¥347. Scenario at 5% / 10% / 15% conversion: ¥2,206 / ¥4,412 / ¥6,619 per month.")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("wrote", path)

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    build_main(OUT / "Team5_Q15_report.pdf")
    build_appendix(OUT / "Team5_Q15_appendix.pdf")

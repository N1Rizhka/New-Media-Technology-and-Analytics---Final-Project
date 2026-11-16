#!/usr/bin/env python3
"""Build final Team 5 Q15 report from the team's preferred prose + figures."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

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
    p.paragraph_format.space_before = Pt(0)
    return p


def add_caption(doc, text):
    add_para(doc, text, italic=True, center=True, size=10, space_after=10)


def add_figure(doc, path: Path, width_in=5.7):
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


def add_table(doc, headers, rows):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Table Grid"
    for j, h in enumerate(headers):
        t.rows[0].cells[j].text = h
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            t.rows[i + 1].cells[j].text = str(val)
    doc.add_paragraph("")


def build(path: Path):
    doc = Document()
    set_doc_defaults(doc)

    add_para(doc, "Group Project Report", bold=True, center=True, size=16)
    add_para(doc, 'What should the "you may also like" shelf show, and to whom?', center=True, size=12)
    add_para(doc, "Association rules · Lumen Beauty (Sep–Nov 2026)", center=True, size=11, space_after=12)
    cover_table(doc)
    doc.add_paragraph("")

    # -------- 1 --------
    doc.add_heading("1. Problem & what it is worth", level=1)
    add_para(
        doc,
        "After completing a purchase in Lumen Beauty’s Douyin mini-program, customers are shown a "
        "“you may also like” shelf intended to encourage additional purchases. The brand founder and "
        "e-commerce merchandising team must decide which products to recommend and whether the same "
        "recommendations should be displayed to all customers or adapted to different buyer groups. The "
        "challenge is to identify product relationships that are relevant to the moment of purchase while "
        "ensuring that recommendations reflect the broader customer base rather than primarily the behavior "
        "of frequent buyers.",
    )
    add_para(
        doc,
        "The commercial opportunity lies in encouraging customers to add complementary products to their "
        "existing orders. Serum and cream provide a particularly relevant example, as many customers "
        "purchase serum without adding cream to the same transaction. If the recommendation shelf persuaded "
        "5–15% of these customers to purchase an additional cream, assuming an average cream line value of "
        "¥346.52, the estimated additional revenue would amount to ¥2,206–6,619 per month, equivalent to "
        "approximately 0.6–1.7% of monthly gross merchandise value (GMV). These figures represent a potential "
        "business scenario, not a measured sales effect.",
    )
    add_para(
        doc,
        "However, the customer base is characterized by substantial differences in purchasing frequency. "
        "Frequent buyers generate a disproportionately large share of transactions, while occasional buyers "
        "account for a considerable proportion of customers. Consequently, recommendations derived from "
        "complete purchasing histories may primarily reflect the preferences of frequent buyers. This creates "
        "a potential targeting problem: a shelf intended for everyone could be shaped by the behaviour of a "
        "relatively small, highly active customer segment, making its recommendations less representative of "
        "first-time and occasional buyers.",
    )
    add_para(
        doc,
        "The central managerial question is therefore: What should the “you may also like” shelf show, and to "
        "whom? This report uses association rule mining to compare product relationships identified from "
        "individual orders with those derived from complete customer histories. It then examines whether the "
        "resulting recommendations remain relevant across customers with different purchasing frequencies, sales "
        "channels, and first-time purchases. The objective is to identify a recommendation strategy that is both "
        "commercially actionable and relevant to the wider customer base.",
    )

    # -------- 2 --------
    doc.add_heading("2. Data", level=1)
    add_para(
        doc,
        "The cleaned dataset covers the period from 1 September to 30 November 2026 and contains 3,401 orders "
        "from 647 individual buyers, generating a total gross merchandise value (GMV) of ¥1,171,735.16. The "
        "distribution of products across these orders indicates a considerable opportunity for cross-selling. "
        "Approximately 65.2% of all orders, or 2,219 out of 3,401, contain only one product. Consequently, most "
        "customers complete their checkout without purchasing a second product, leaving an opportunity for the "
        "recommendation shelf to encourage an additional purchase. One particularly relevant example is the "
        "relationship between serum and cream. On average, approximately 127 orders per month contain serum "
        "without cream. The monthly figures are 137 orders in September, 124 in October, and 121 in November. "
        "If the recommendation shelf persuaded between 5% and 15% of these serum-only orders to include a cream, "
        "the resulting additional revenue would amount to approximately ¥2,206–6,619 per month, assuming an "
        "average cream line value of ¥346.52. This corresponds to approximately 0.6–1.7% of monthly GMV. These "
        "figures represent a business scenario rather than a measured increase in sales, since the recommendation "
        "shelf has not yet been tested experimentally.",
    )
    add_para(
        doc,
        "The question of whom the shelf serves becomes particularly important when customers are divided according "
        "to their purchasing frequency. Heavy buyers, defined as customers placing six or more orders during the "
        "observation period, account for 41.0% of all buyers but generate 80.3% of all orders. In contrast, light "
        "buyers, who place only one or two orders, represent 46.5% of the customer base, corresponding to 301 people, "
        "but account for only 10.8% of total orders. This imbalance matters because association rules derived from "
        "complete customer histories can be disproportionately influenced by customers who purchase frequently and "
        "have accumulated a much larger variety of products. A recommendation system trained on these histories may "
        "therefore primarily reflect the preferences of the heaviest buyers, even though nearly half of Lumen Beauty’s "
        "customers belong to the light-buyer segment. In this case, the behavior of the 301 light buyers would "
        "contribute only 1.7% of the evidence behind the history-based rules. The potential targeting problem is "
        "therefore not simply that some customers purchase more often than others. It is that recommendations "
        "intended for the entire customer base could be determined largely by the purchasing behavior of a relatively "
        "small group of highly active customers.",
    )
    add_para(
        doc,
        "To investigate this issue, the analysis distinguishes between two different definitions of a purchasing "
        "basket. An order basket contains the distinct products purchased together in one individual order. It "
        "therefore represents the products that a customer has selected at the specific moment when the "
        "post-purchase recommendation shelf appears. A customer-history basket, in contrast, combines every distinct "
        "product that an individual customer purchased throughout the entire three-month observation period, "
        "regardless of whether those products were bought together or in separate transactions. The distinction is "
        "central to the research question: order baskets reveal which products customers actually purchase together, "
        "whereas customer histories reveal which products they have purchased at some point. The average order basket "
        "contains 1.45 distinct products, after collapsing repeated order lines into unique SKUs. This figure "
        "describes the average number of different products per order, not the number of individual units shipped.",
    )
    add_para(
        doc,
        "The analysis uses two tables from the Lumen Beauty project dataset, which contains the company’s "
        "operational data for the period from September to November 2026. The first table, lb_order_lines.csv, "
        "contains individual order-line records, while the second table, lb_users.csv, provides customer-level "
        "information. The original order-line export contains 4,920 rows before cleaning. The accompanying "
        "project_data_dictionary was used to interpret the variables and distinguish genuine missing information "
        "from fields that were not applicable to particular types of transactions. The auxiliary tables containing "
        "livestream streams, comments, and follows were excluded because the research question concerns product "
        "co-purchases rather than customer engagement with livestream content.",
    )
    add_para(
        doc,
        "Before constructing the purchasing baskets, the order-line data were checked for duplicate records, missing "
        "values, and implausible observations. Five exact duplicate order lines were identified and removed, leaving "
        "4,915 valid order lines. The resulting cleaned dataset produces a total GMV of ¥1,171,735.16. Some order "
        "lines contain an empty stream_id, but these records correspond exclusively to purchases made through the "
        "store. According to the data dictionary, this field is not applicable to store orders and should therefore "
        "not be interpreted as missing information or a data-quality problem.",
    )
    add_para(
        doc,
        "The remaining transaction variables are consistent with the expected structure of the dataset. The recorded "
        "quantity per order line is either one or two units, while unit prices range from ¥54.45 to ¥504.85. Each SKU "
        "has a unique store list price, and the ratio between the paid price and the list price ranges from 0.55 to "
        "1.15. These differences are consistent with the presence of promotional pricing, particularly during "
        "livestream sales. The number of orders per buyer ranges from one to 20, with a median of three orders. An "
        "upper outlier threshold of 21 orders was calculated using the boxplot fence method, meaning that none of the "
        "observed buyers exceeds the statistical threshold. Heavy buyers were therefore retained in the analysis "
        "rather than removed as outliers. This decision is particularly important because the research question "
        "explicitly examines whether frequent customers disproportionately influence the recommendation rules.",
    )
    add_para(
        doc,
        "The customer table was also checked against the transaction data. All 647 buyers represented in the cleaned "
        "order dataset could be matched to an entry in lb_users.csv, and the recorded number of orders, n_orders, "
        "corresponds to the transaction table for every buyer. This consistency allows customers to be classified "
        "according to their actual purchasing frequency and makes it possible to compare the behavior of light, mid, "
        "and heavy buyers.",
    )
    add_para(
        doc,
        "The transaction data also distinguish between livestream and store purchases. Of the 3,401 orders, 2,579 "
        "were placed through livestreams and 822 through the store. It is important to distinguish these transaction "
        "channels from the variables search, short_video and ad, which describe the customer’s first acquisition "
        "channel in users.first_channel. These values indicate how a customer initially arrived at the platform, not "
        "where a particular order was placed. The analysis therefore uses the transaction-level channel information "
        "when comparing livestream and store purchases.",
    )
    add_figure(doc, FIG / "fig_channel_and_categories.png", 5.8)
    add_caption(
        doc,
        "Figure A. Orders by channel and by category presence (a basket can appear in several category bars).",
    )
    add_para(
        doc,
        "For the purpose of answering the research question, buyers were divided into three purchasing-frequency "
        "segments. Light buyers placed one or two orders, mid buyers placed three to five orders, and heavy buyers "
        "placed six or more orders during the observation period. This classification is based on the number of orders "
        "rather than customer spending. The distinction is intentional because the analysis investigates whether "
        "frequent purchasing causes certain customers to dominate the evidence behind association rules. A "
        "spending-based classification using the high_value variable would address a different question, namely "
        "whether high-revenue customers dominate the recommendations.",
    )
    add_table(
        doc,
        ["Buyer type", "Buyers", "Orders", "% of buyers", "% of orders"],
        [
            ["Light (1–2 orders)", "301", "366", "46.5%", "10.8%"],
            ["Mid (3–5)", "81", "304", "12.5%", "8.9%"],
            ["Heavy (6+)", "265", "2,731", "41.0%", "80.3%"],
        ],
    )
    add_caption(doc, "Table 1. Buyer intensity segments used for Q15 (cut on n_orders, not spend).")
    add_para(
        doc,
        "The distribution in Table 1 illustrates the imbalance between customer numbers and transaction volume. "
        "Although light buyers constitute almost half of the customer base, they generate only 10.8% of orders. Heavy "
        "buyers, by comparison, represent 41.0% of buyers but account for 80.3% of orders. This difference becomes "
        "particularly relevant when purchasing histories are used to construct association rules, because customers "
        "with more orders also have more opportunities to accumulate distinct products and generate product pairs.",
    )
    add_figure(doc, FIG / "fig_buyers_vs_orders.png")
    add_caption(
        doc,
        "Figure 1. Light buyers represent almost half of all customers, while heavy buyers generate 80.3% of orders.",
    )
    add_para(
        doc,
        "The difference between the two basket definitions is also visible in their average sizes. Order baskets "
        "contain an average of 1.45 distinct products, whereas customer-history baskets contain an average of 6.27 "
        "distinct products. The latter are therefore more than four times larger. Across the 3,401 orders, 2,219 "
        "contain one distinct product, 850 contain two products, and 332 contain three products. These figures show "
        "that most individual transactions are relatively small, while the combination of purchases across an entire "
        "customer history produces much larger baskets. This difference is not merely a descriptive feature of the "
        "data. It directly affects how many product associations can be generated and how relevant those associations "
        "are to the recommendation moment.",
    )
    add_figure(doc, FIG / "fig_basket_size.png")
    add_caption(
        doc,
        "Figure 2. Basket size: 65.2% of orders contain a single product, creating an opportunity for the post-purchase shelf.",
    )

    # -------- 3 --------
    doc.add_heading("3. Method & assumptions", level=1)
    add_para(
        doc,
        "Association rule mining, introduced in Week 3, was applied using the Apriori algorithm implemented in "
        "Python’s mlxtend package (version 0.25.0). The analysis was restricted to product pairs (max_len=2) because "
        "the recommendation shelf suggests one additional product based on the current purchase. Rules were evaluated "
        "using support, confidence and lift, which respectively measure co-purchase frequency, the likelihood of "
        "purchasing the second product given the first, and the strength of the association relative to independent "
        "purchasing. To ensure transparency, co-purchase counts and their respective denominators are reported "
        "alongside the metrics. These measures identify purchasing patterns but do not establish causality or "
        "statistical significance.",
    )
    add_para(
        doc,
        "Support measures how frequently two products occur together in the relevant baskets. Confidence measures how "
        "often the second product is present when the first product is purchased. Lift compares the observed "
        "co-occurrence with the frequency that would be expected if the two products were independent. A lift above "
        "one indicates that the products occur together more frequently than expected under independence, whereas a "
        "lift below one indicates that they occur together less frequently than expected. The support and confidence "
        "thresholds are frequency filters used to identify patterns with sufficient observed evidence. They are not "
        "statistical significance tests.",
    )
    add_para(
        doc,
        "The thresholds were selected with the recommendation use case in mind. The original project plan proposed a "
        "minimum product support of 2%. When applied to individual order baskets, however, this threshold returned no "
        "product-level rules because the support of the largest observed product pair was only 0.79%. The order-level "
        "minimum support was consequently reduced to 0.4%, corresponding to at least 14 of the 3,401 orders. Over the "
        "thirteen-week observation period, this represents approximately one qualifying order per week. Category-level "
        "rules use a higher threshold of 1%, corresponding to at least 35 orders. For customer-history rules, the "
        "original 2% threshold was retained, corresponding to at least 13 of the 647 customers. This approach "
        "establishes a comparable minimum frequency requirement across the two units of analysis while recognising "
        "that an individual order and an entire customer history represent different observational units.",
    )
    add_para(
        doc,
        "The analysis is guided by two theoretical predictions. First, drawing on segmentation, targeting and "
        "positioning (STP), customer-history rules are expected to be disproportionately influenced by heavy buyers, "
        "as their larger purchasing histories generate more product associations (T1). Second, based on "
        "complementarity between skincare routine steps, serum and cream are expected to show a positive association, "
        "with cream being a relevant recommendation after serum. This relationship is expected to remain visible "
        "across buyer segments, sales channels and first orders (T2). The potential algorithmic bias resulting from a "
        "history-based recommendation system is treated as an ethical implication of the findings and discussed in "
        "§6; it is not used to explain the observed product association.",
    )
    add_para(
        doc,
        "Several limitations apply. Co-purchases do not demonstrate that one product causes the purchase of another, "
        "and historical transaction data cannot establish the incremental sales effect of a recommendation shelf that "
        "did not yet exist. Furthermore, the light-buyer segment contains only 366 orders, limiting the reliability of "
        "product-level rules within this group. Category-level associations are therefore given greater weight when "
        "comparing buyer segments. Same-order checks on top history pairs also rest on single-digit counts, so those "
        "lifts are noisy. Finally, the proposed six-week pilot is intended as an initial safety check rather than a "
        "definitive test capable of distinguishing a 5% add-on rate from a 2% rate.",
    )

    # -------- 4 --------
    doc.add_heading("4. Findings", level=1)
    add_para(
        doc,
        "The first finding concerns the difference between association rules derived from individual orders and those "
        "derived from complete customer histories. When the same minimum-frequency principle is applied to the two "
        "approaches, individual order baskets produce 30 product rules, while customer-history baskets produce 870. "
        "The history-based analysis therefore generates substantially more associations, even though both approaches "
        "use the same underlying product catalogue. In fact, the 870 history rules cover every possible directed pair "
        "among the 30 SKUs, and all of these rules have a lift above one.",
    )
    add_para(
        doc,
        "This difference is largely explained by the size of the baskets. A customer-history basket contains an average "
        "of 6.27 distinct products, compared with only 1.45 products in an individual order. As a result, a history "
        "basket generates many more possible product pairs, including combinations of products that were purchased on "
        "entirely separate occasions. A customer who bought a toner in September and a different toner in November, "
        "for example, contributes both products to the same history basket even though they were never purchased "
        "together in one transaction. History-based rules therefore answer the question of which products a customer "
        "has tried during the observation period. Order-based rules answer which products customers actually purchased "
        "together in a single transaction. Since the recommendation shelf appears immediately after an individual "
        "purchase, the second question is more closely aligned with the decision the merchandising team needs to make.",
    )
    add_figure(doc, FIG / "fig_rules_orders_vs_histories.png")
    add_caption(
        doc,
        "Figure 3. Applying comparable minimum-frequency thresholds produces 30 product rules from individual orders and 870 from complete customer histories.",
    )
    add_para(
        doc,
        "The second finding identifies Serum → Cream as the strongest category-level association in individual order "
        "baskets. Across the 3,401 orders, 256 contain both serum and cream. This is substantially more than the "
        "approximately 146.5 orders that would be expected if the two categories occurred independently. The resulting "
        "support is 0.075, confidence is 0.40 and lift is 1.75. In practical terms, about 40% of serum orders also "
        "contain cream, and the two categories occur together approximately 1.75 times as often as would be expected "
        "under independence.",
    )
    add_figure(doc, FIG / "fig_category_cooccurrence.png", 5.2)
    add_caption(
        doc,
        "Figure 3b. Same-order category co-occurrence (support). Serum ∩ Cream = 0.075 stands out among category pairs.",
    )
    add_para(
        doc,
        "The direction of the association is important for the recommendation decision. When cream is used as the "
        "starting point, the confidence of the reverse rule, Cream → Serum, is only 0.33. This means that the "
        "relationship is stronger in the direction from serum to cream than from cream to serum. Accordingly, the "
        "shelf should show a cream after a customer purchases serum, rather than treating the two directions as "
        "interchangeable. At the category level, every other product-category pair with at least 1% support has a "
        "lift below one. Serum → Cream is therefore the only strong category-level order association identified at "
        "the selected frequency threshold.",
    )
    add_para(
        doc,
        "The product-level rules provide a more detailed indication of which creams could be ranked after particular "
        "serums, although their supporting counts are considerably smaller. For Vitamin C Serum, the two leading cream "
        "associations are Hydra Gel and Brightening Cream. These combinations occur in 26 and 27 orders respectively, "
        "corresponding to support values of 0.0076 and 0.0079 and lifts of 2.29 and 2.27. Their confidence values are "
        "0.138 for Hydra Gel and 0.144 for Brightening. These SKU-level associations can therefore help determine the "
        "order in which cream candidates are displayed, but their relatively small co-purchase counts mean that they "
        "should not be interpreted as equally robust as the category-level Serum → Cream relationship.",
    )
    add_table(
        doc,
        ["Rule", "Both / denom", "Support", "Conf.", "Lift", "Interpretation"],
        [
            ["Serum → Cream", "256 / 3,401 orders (256 / 638 serum)", "0.075", "0.40", "1.75", "Show cream after serum"],
            ["Vit. C Serum → Hydra Gel", "26 / 3,401 (26 / 188 Vit. C)", "0.0076", "0.138", "2.29", "Cream #1 after Vit. C"],
            ["Vit. C Serum → Brightening", "27 / 3,401 (27 / 188 Vit. C)", "0.0079", "0.144", "2.27", "Cream #2 after Vit. C"],
        ],
    )
    add_caption(
        doc,
        "Table 2. Selected order-based association rules, including co-purchase counts and denominators. The frequency filters identify observed patterns and are not statistical significance tests.",
    )
    add_para(
        doc,
        "The monthly distribution of serum orders further clarifies the business opportunity. In each month, a "
        "considerable number of serum purchases are not accompanied by a cream. These transactions form the "
        "addressable group for the proposed recommendation: customers who have purchased serum but have not yet added "
        "cream to the same order. The association between the two categories is also consistent across transaction "
        "channels. Serum → Cream has a lift of 1.73 in livestream orders and 1.80 in store orders. This suggests that "
        "the relationship is not limited to purchases made during livestreams, where hosts may promote products "
        "together as part of a bundle or sales presentation. The association is also present in store purchases, "
        "indicating that the purchasing pattern persists beyond the livestream environment.",
    )
    add_figure(doc, FIG / "fig_serum_opportunity.png")
    add_caption(
        doc,
        "Figure 4. Monthly serum orders with and without cream, illustrating the orders that could be addressed by the recommendation shelf.",
    )
    add_para(
        doc,
        "The third finding concerns the influence of heavy buyers on customer-history rules. The number of possible "
        "product pairs generated by a customer-history basket increases rapidly with the number of distinct products "
        "in that basket. A history containing n distinct products can generate n(n−1)/2 unique product pairs. "
        "Consequently, customers who have purchased many different products contribute disproportionately more pair "
        "evidence than customers with smaller purchasing histories. In the dataset, heavy buyers have an average of "
        "11.7 distinct products in their histories. They account for 92.9% of all pair evidence, despite representing "
        "only 41.0% of buyers. Light buyers, in contrast, represent 46.5% of customers but contribute only 1.7% of the "
        "evidence behind the history-based rules.",
    )
    add_para(
        doc,
        "This result supports the first theoretical prediction: customer-history rules are strongly influenced by the "
        "purchasing behaviour of heavy buyers. The finding is not dependent on the specific definition of a heavy "
        "buyer. When the threshold is changed from six orders to four, eight or ten orders, the share of history-rule "
        "evidence contributed by heavy buyers remains substantially higher than their share of the customer base. Even "
        "when heavy buyers are defined as customers placing at least ten orders, they represent only 21.2% of buyers "
        "but contribute 62.8% of the history-rule evidence. The difference between their share of customers and their "
        "share of pair evidence therefore persists across all tested thresholds.",
    )
    add_table(
        doc,
        ["Heavy-buyer cut-off", "% of buyers", "% of history-rule evidence", "Serum→Cream lift (heavy)"],
        [
            ["4+ orders", "48.2%", "97.1%", "1.73"],
            ["6+ orders (main definition)", "41.0%", "92.9%", "1.72"],
            ["8+ orders", "32.8%", "83.3%", "1.71"],
            ["10+ orders", "21.2%", "62.8%", "1.61"],
        ],
    )
    add_caption(doc, "Table 3. Heavy-buyer dominance in history-rule evidence does not depend on the selected cut-off.")
    add_figure(doc, FIG / "fig1_history_evidence_by_buyer_type.png")
    add_caption(
        doc,
        "Figure 5. Comparison of the share of buyers and the share of pair evidence contributed by buyer types in customer-history baskets.",
    )
    add_figure(doc, FIG / "fig_robustness_heavy_cutoff.png")
    add_caption(
        doc,
        "Figure 5b. Heavy buyers dominate history evidence at every cut-off (4+, 6+, 8+, 10+ orders).",
    )
    add_para(
        doc,
        "The fourth finding demonstrates why the large number of history-based rules should not automatically be "
        "interpreted as evidence of products that customers frequently purchase together. When the leading "
        "history-based product pairs are examined in individual order baskets, their lifts are below one. One example "
        "is the combination Calming Toner Mist → Pore Refining Toner. The pair has a history-based lift of 2.15, "
        "suggesting that customers who purchased one product were relatively likely to have purchased the other at "
        "some point during the observation period. However, its same-order lift is only 0.37. The two products appear "
        "together in just three orders, compared with approximately 8.1 orders expected under independence. The "
        "history-based association therefore does not reflect frequent joint purchasing. Instead, heavy buyers may "
        "have tried these products at different points in time, potentially as alternatives within their skincare "
        "routines. Describing such combinations as products that are “frequently bought together” would misrepresent "
        "what the underlying data actually show.",
    )
    add_figure(doc, FIG / "fig_history_vs_order_lift.png")
    add_caption(
        doc,
        "Figure 6. Leading history-based product pairs can have high history lift while showing same-order lift below one.",
    )
    add_para(
        doc,
        "The fifth finding addresses whether a single order-based recommendation shelf can serve customers with "
        "different purchasing histories. The Serum → Cream association remains above one across all three buyer "
        "segments. Its lift is 1.79 among light buyers, 1.93 among mid buyers and 1.72 among heavy buyers. The "
        "relationship also remains visible across transaction channels, with lifts of 1.73 for livestream orders and "
        "1.80 for store orders. Most importantly, the association is present in customers’ first orders. When only "
        "first orders are considered, Serum → Cream has a confidence of 0.426 and a lift of 1.80. This indicates that "
        "the relationship is not dependent on customers having an extensive purchasing history. Even when a customer "
        "has no previous transaction history available to the recommendation system, the current order provides "
        "sufficient information to identify the serum-to-cream recommendation.",
    )
    add_table(
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
    add_caption(doc, "Table 4. Serum → Cream association across buyer groups, sales channels and first orders.")
    add_figure(doc, FIG / "fig_serum_cream_slices.png")
    add_caption(
        doc,
        "Figure 7. Serum → Cream lift across buyer types, transaction channels and first orders.",
    )
    add_para(
        doc,
        "The additional analysis required for Q15 provides further support for using one order-based shelf rather than "
        "separate shelves for different customer groups. When category-level rules are mined separately from the order "
        "baskets of light and heavy buyers, Serum → Cream remains the primary rule in both groups. This means that the "
        "central category-level recommendation is not driven exclusively by heavy buyers. It also appears in the "
        "purchasing behaviour of light buyers when the analysis focuses on individual transactions. The stretch "
        "analysis therefore reinforces the conclusion that a separate product recommendation strategy for light and "
        "heavy buyers is not necessary for the primary serum-to-cream recommendation.",
    )
    add_para(
        doc,
        "Taken together, these findings answer both parts of the research question. First, the recommendation shelf "
        "should be based on products purchased together in individual orders, rather than products accumulated across "
        "complete customer histories. The latter approach generates many more rules, but those rules can combine "
        "products purchased on separate occasions and are heavily influenced by frequent buyers. Second, the shelf "
        "should be designed to serve all customers, including first-time and occasional buyers. The order-based "
        "Serum → Cream association remains consistent across the buyer segments, transaction channels and first orders "
        "examined in the analysis. The central business decision is therefore not whether Lumen Beauty should build a "
        "separate shelf for every customer segment. It is which purchasing evidence should determine the "
        "recommendations in the first place.",
    )
    add_para(
        doc,
        "Compared with the project plan dated 20 October, the analysis leads to three important refinements. The first "
        "is the distinction between order baskets and customer-history baskets, which changes the unit of analysis to "
        "match the moment when the recommendation shelf appears. The second is the use of purchasing frequency rather "
        "than the high_value spending classification to define customer segments, because the research question "
        "concerns the influence of frequent buyers on the recommendation rules. The third is the adjustment of the "
        "support thresholds after the originally proposed 2% product-level threshold returned no usable order-based "
        "product rules. These refinements make the analysis more closely aligned with the actual merchandising decision.",
    )

    # -------- 5 --------
    doc.add_heading("5. Recommendation", level=1)
    add_para(
        doc,
        "Based on the findings, Lumen Beauty should make a clear decision: the post-purchase recommendation shelf "
        "should be mined from individual order baskets rather than complete customer histories. Whenever a customer "
        "purchases a serum without a cream in the current basket, the shelf should recommend a cream. This "
        "Serum → Cream category rule should occupy the first recommendation position because it is the only strong "
        "category-level association identified in individual orders and remains consistent across light, mid and heavy "
        "buyers, livestream and store purchases, and first orders. The same primary recommendation should therefore be "
        "shown to all customers, including first-time buyers who have no previous purchasing history.",
    )
    add_para(
        doc,
        "Product-level associations should be used more cautiously. The Vitamin C Serum → Hydra Gel and "
        "Vitamin C Serum → Brightening rules can help rank which cream appears first among the available cream "
        "candidates after a Vitamin C Serum purchase. However, these product-level rules are supported by only 26 and "
        "27 co-purchasing orders respectively. They should therefore determine the ranking of cream products rather "
        "than replace the more robust category-level Serum → Cream recommendation. For the remaining recommendation "
        "positions, Lumen Beauty should use the products most frequently purchased by light buyers: Clay Purifying "
        "Mask, Deep Clean Foam, Essence Toner and Cooling Eye Gel, as identified in notebook section 10e. This would "
        "prevent the remaining shelf positions from simply reflecting overall bestseller volume, which is heavily "
        "influenced by heavy buyers.",
    )
    add_figure(doc, FIG / "fig_light_buyer_slots.png")
    add_caption(
        doc,
        "Figure 8. Leftover shelf slots: products with the strongest presence in light-buyer orders (versus overall).",
    )
    add_para(
        doc,
        "The operational implementation follows directly from this decision. Lumen Beauty should first switch the "
        "association-rule mining process from customer-history baskets to individual order baskets. The recommendation "
        "logic should then place a cream in the first position whenever the current basket contains a serum but does "
        "not yet contain a cream. Cream SKUs should be ranked using their order-level lift in serum-to-cream product "
        "pairs, provided that each pair has at least 14 supporting orders. Any remaining shelf positions should be "
        "filled using the light-buyer frequency list, which should be refreshed weekly. This approach combines a "
        "category-level rule supported across customer groups with more specific product rankings and a supplementary "
        "product selection that reflects the purchasing behaviour of occasional customers.",
    )
    add_table(
        doc,
        ["Decision element", "Serum → Cream (primary)", "Vit. C → Hydra Gel (SKU ranking)"],
        [
            ["Trigger product", "Any serum in the current basket", "Vitamin C Serum in the current basket"],
            ["Intended customers", "All buyers, including first-time and light buyers", "Serum buyers choosing among cream products"],
            ["Shelf position", "Slot 1 on the post-purchase shelf", "Slot 1 among cream candidates after Vitamin C Serum"],
            [
                "What a buyer with no history sees",
                "The same cream recommendation, supported by a first-order lift of 1.80",
                "The same ranked cream if Vitamin C Serum was just purchased",
            ],
            [
                "Evidence that would reject the rule",
                "Same-order lift ≤1 in a holdout month, or an A/B add-on rate below 2% after the safety window",
                "Co-purchase count below 10 per quarter, or lift ≤1 within individual orders",
            ],
        ],
    )
    add_caption(doc, "Table 5. Translating the association rules into concrete shelf decisions.")
    add_figure(doc, FIG / "fig_scenario_value.png", 5.4)
    add_caption(
        doc,
        "Figure 9. Scenario only: estimated extra monthly GMV if 5–15% of serum-only orders add a cream.",
    )
    add_para(
        doc,
        "The recommendation should be introduced through a controlled pilot beginning on 1 December 2026. Half of the "
        "buyers should be shown the new recommendation shelf, while the other half continue to see the current shelf. "
        "This 50/50 split provides a comparison between the proposed recommendation and the existing experience. "
        "During the first six weeks, each half is expected to encounter approximately 96 serum-only orders. If the new "
        "shelf generates a 5% add-on rate during this period, this would correspond to approximately five additional "
        "cream purchases. Such a small number of observations can help identify whether the recommendation is failing "
        "or whether light and first-time buyers are being left behind, but it is not sufficient to demonstrate "
        "reliably that a 5% add-on rate is different from a 2% rate.",
    )
    add_para(
        doc,
        "For this reason, the six-week period should be treated as a safety check rather than the final evaluation of "
        "commercial performance. To distinguish a 5% add-on rate from a 2% rate with greater confidence, the experiment "
        "should continue for approximately 40 weeks (about 9 months), during which each half is expected to accumulate "
        "around 588 serum-only orders. After this longer evaluation period, the expected result would be that at least "
        "5% of serum-only orders in the treatment group include an additional cream purchase. At the lower end of the "
        "estimated revenue scenario, this would correspond to approximately ¥2,200 in additional monthly revenue. "
        "Results should be reported separately for first-time and repeat buyers so that an apparently positive overall "
        "result does not conceal weaker performance among customers with little or no purchasing history.",
    )
    add_para(
        doc,
        "The pilot should also include clear conditions under which the recommendation is discontinued. The new shelf "
        "should be dropped if the treatment group achieves a cream add-on rate below 2% after the six-week safety "
        "period and does not perform better than the control group. It should also be reconsidered if the add-on rate "
        "among light or first-time buyers is materially lower than the rate among heavy buyers, since this would "
        "indicate that the recommendation is not serving the entire customer base as intended. Finally, the rule should "
        "be rejected if re-mining the control group shows that Serum → Cream has a same-order lift of one or lower. "
        "This would indicate that the observed purchasing relationship is no longer sufficiently supported in the "
        "comparison data.",
    )
    add_para(
        doc,
        "The recommendation deliberately stops short of creating a complex carousel of products based on every "
        "association found in customer histories. The analysis does not identify a second strong category-level order "
        "rule, and the high history-based lifts of other product pairs do not establish that those products are "
        "frequently purchased together in the same transaction. Lumen Beauty should therefore avoid turning "
        "history-based associations into additional cross-sell recommendations without further evidence. It should also "
        "avoid personalising the primary recommendation through complete purchase histories for customers who have "
        "only just started buying from the brand. The proposed approach instead uses the current order to determine "
        "the main recommendation, allowing the same category-level rule to serve both new and established customers.",
    )
    add_para(
        doc,
        "Ultimately, the most important decision is not how many association rules the algorithm can generate, but "
        "which purchasing behaviour the recommendation shelf should represent. Customer histories produce a much larger "
        "set of rules, yet those rules are dominated by heavy buyers and may combine products purchased at different "
        "points in time. Individual orders provide fewer associations, but they correspond directly to the moment when "
        "the shelf appears and reveal a Serum → Cream relationship that remains consistent across the customer groups "
        "and channels examined. By using this relationship as the primary recommendation, ranking cream products with "
        "the available SKU-level evidence and filling the remaining positions with products popular among light "
        "buyers, Lumen Beauty can build a shelf that is both commercially actionable and more representative of its "
        "wider customer base. The estimated revenue opportunity of ¥2,206–6,619 per month provides a reason to test "
        "the approach, but it should not be presented as a measured effect until the controlled pilot has produced "
        "sufficient evidence.",
    )

    # -------- 6 --------
    doc.add_heading("6. Ethics & compliance implications", level=1)
    add_para(
        doc,
        "Stake. A history-trained shelf draws 92.9% of its pair evidence from heavy buyers, so 301 light buyers "
        "(46.5%) would be served a catalogue that barely reflects their own behaviour.",
    )
    add_para(
        doc,
        "Who bears it. First-time and light buyers. Feedback-loop risk (untested on past logs): once live, the shelf "
        "can create the pairs it later mines.",
    )
    add_para(
        doc,
        "Misinformation. Labelling a history-based shelf “frequently bought together” would be false for the top "
        "history pairs (same-order lift < 1). Safeguard: label by what the shelf shows, e.g. “often bought in the same "
        "order”.",
    )
    add_para(
        doc,
        "Privacy. An order shelf needs only the current basket (PIPL data-minimisation). Under China’s 2022 "
        "Algorithmic Recommendation Provisions (Art. 17), offer an option not based on personal characteristics and an "
        "easy way to switch algorithmic recommendations off.",
    )
    add_para(
        doc,
        "Safeguard tied to the recommendation. Mine future rules on the control half of the A/B test, report add-on "
        "rates by buyer type, and drop under the conditions in §5.",
    )

    # -------- 7 --------
    doc.add_heading("7. Artificial intelligence (AI) use appendix", level=1)
    add_para(
        doc,
        "Claude (Anthropic). Helped draft early notebook structure from Week 2 / Week 3 course patterns, proposed "
        "robustness checks (first-order slice, heavy cut-offs, shelf decision cards), and suggested manager-facing "
        "wording.",
    )
    add_para(
        doc,
        "Cursor (Composer). Helped revise code cells, rebuild charts in the Tongji-blue palette, generate the report "
        "and slide builders, and keep numbers aligned with notebook output after each data re-run.",
    )
    add_para(
        doc,
        "Team review. Every cell was re-run on the course Lumen Beauty CSVs; every shipped number was checked against "
        "notebook output. No platform personal data left the course environment.",
    )
    add_para(
        doc,
        "Every member of this team can explain every line of code and every number in this submission.",
    )

    path.parent.mkdir(exist_ok=True)
    doc.save(str(path))
    print("wrote", path)


def to_pdf(docx_path: Path, pdf_path: Path):
    # Copy to /tmp first — LibreOffice sometimes fails on special paths
    tmp = Path("/tmp") / docx_path.name
    shutil.copy2(docx_path, tmp)
    subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf", "--outdir", "/tmp", str(tmp)],
        check=True,
        capture_output=True,
        text=True,
    )
    produced = Path("/tmp") / (docx_path.stem + ".pdf")
    shutil.copy2(produced, pdf_path)
    print("wrote", pdf_path)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    docx = OUT / "NMTA_T05_report.docx"
    build(docx)
    shutil.copy2(docx, OUT / "project_report.docx")
    to_pdf(docx, OUT / "NMTA_T05_report.pdf")
    shutil.copy2(OUT / "NMTA_T05_report.pdf", OUT / "Team5_Q15_report.pdf")
    print("done")

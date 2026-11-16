#!/usr/bin/env python3
"""Patch the Q15 notebook for review fixes, then Restart & Run All."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "deliverables" / "Team5_Q15_shelf_association_rules.ipynb"
OUT = SRC
MIRROR = ROOT / "Q15_shelf_association_rules.ipynb"


def md(text: str):
    return nbformat.v4.new_markdown_cell(text.strip() + "\n")


def code(text: str):
    return nbformat.v4.new_code_cell(text.strip() + "\n")


def set_source(cell, text: str):
    cell["source"] = text.strip() + "\n"


def main():
    nb = nbformat.read(SRC, as_version=4)
    cells = nb.cells

    # --- Intro: add theory pointer ---
    set_source(
        cells[0],
        """
# Q15 – What should the "you may also like" shelf show, and to whom?
**Team 5 · New Media Technology and Analytics · Lumen Beauty (Sep–Nov 2026) · Association rules (Week 3)**

After every purchase, Lumen Beauty's mini-program shows a "you may also like" shelf. This notebook mines association rules on **single orders** and on **whole customer histories**, reports every rule with its **co-purchase count and denominator**, checks whom each shelf would serve (light vs heavy buyers), and translates the shippable rules into **shelf decisions** with an explicit **kill condition**.

**Theory we test.** STP targeting: a history-trained shelf will over-serve heavy buyers. Product complementarity in a skincare routine: serum and cream are steps that go together, so Serum → Cream should appear as complements (lift > 1) in every buyer segment and channel — not only among heavy buyers.
""",
    )

    # --- Fix serum opportunity chart labels / title consistency ---
    set_source(
        cells[47],
        """
# Chart 6 — The shelf opportunity: serum orders with / without a cream, by month
orders["month"] = lines.groupby("order_id")["order_date"].first().str[:7]
has_s = orders["categories"].apply(lambda c: "Serum" in c)
has_c = orders["categories"].apply(lambda c: "Cream" in c)
opp = pd.DataFrame({
    "serum + cream": (has_s & has_c).groupby(orders["month"]).sum(),
    "serum, no cream": (has_s & ~has_c).groupby(orders["month"]).sum(),
})
avg_open = opp["serum, no cream"].mean()
fig, ax = plt.subplots(figsize=(7.5, 4.2))
opp.plot(kind="bar", stacked=True, ax=ax, color=[ACCENT, WARM], rot=0)
ax.set_ylabel("Orders")
ax.set_xlabel("")
ax.set_title(f"About {avg_open:.0f} serum orders / month leave without a cream")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False)
ymax = float(opp.sum(axis=1).max())
for i, (idx_m, row) in enumerate(opp.iterrows()):
    ax.text(i, float(row.sum()) + ymax * 0.02,
            f"no cream: {int(row['serum, no cream'])}",
            ha="center", fontsize=9, color=MUTED)
ax.set_ylim(0, ymax * 1.18)
fig.tight_layout()
fig.savefig(FIG / "fig_serum_opportunity.png", dpi=160, bbox_inches="tight", facecolor=PAPER)
plt.show()
print(f"monthly open slots (serum, no cream): {opp['serum, no cream'].to_dict()} · mean {avg_open:.1f}")
""",
    )

    # --- Larger / clearer 30 vs 870 chart ---
    set_source(
        cells[52],
        """
# Chart 7 — Same minimum count, very different rule tables
fig, ax = plt.subplots(figsize=(8.2, 4.4))
vals = [len(rules_004), len(history_rules)]
bars = ax.bar(["Order baskets\\n(≥14 orders · 0.4%)", "History baskets\\n(≥13 customers · 2%)"],
              vals, color=[ACCENT, WARM], width=0.55)
ax.set_ylabel("Association rules (directed pairs)")
ax.set_title("At a similar bar: 30 order rules vs 870 history rules")
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width()/2, v + max(vals)*0.03, f"{v}",
            ha="center", fontsize=16, fontweight="bold", color=INK)
ax.set_ylim(0, max(vals) * 1.22)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
fig.savefig(FIG / "fig_rules_orders_vs_histories.png", dpi=160, bbox_inches="tight", facecolor=PAPER)
plt.show()
""",
    )

    # --- Update scenario interpretation for stake in users ---
    set_source(
        cells[75],
        """
**Results interpretation:** about 127 serum orders a month leave without a cream. If the shelf converts 5–15% of them, it is worth about **¥2,200–6,600 per month**, that is 0.6–1.7% of monthly GMV. The yuan figure is modest. The sharper stake is in users: a history-based shelf would serve **301 light buyers** (46.5% of buyers) using rules that are only **1.7%** built from their own behaviour. This ¥ figure is a scenario, not a measured effect.
""",
    )

    # --- Build new cells for light-buyer slots + honest pilot ---
    light_slots_md = md(
        """
## 10e · Remaining shelf slots: what light buyers actually buy
Slot 1 is cream after serum. For any leftover slots, overall bestsellers are mostly written by heavy buyers' order volume (80% of orders). Below we rank SKUs by how often they appear in **light-buyer** orders, and compare that ranking with the overall catalogue. Only the notebook numbers below feed the recommendation.
"""
    )
    light_slots_code = code(
        """
# Remaining slots: products light buyers buy most (presence in light-buyer orders)
def sku_presence(df):
    return (
        df.groupby(["order_id", "sku_name"]).size()
          .reset_index()[["order_id", "sku_name"]]["sku_name"]
          .value_counts()
    )

light_orders = lines[lines["buyer_type"] == "light"]
light_sku = sku_presence(light_orders)
all_sku = sku_presence(lines)
slot_cmp = pd.DataFrame({"light_orders": light_sku, "all_orders": all_sku}).fillna(0).astype(int)
slot_cmp["light_share"] = slot_cmp["light_orders"] / slot_cmp["light_orders"].sum()
slot_cmp["all_share"] = slot_cmp["all_orders"] / slot_cmp["all_orders"].sum()
slot_cmp["over_index"] = slot_cmp["light_share"] / slot_cmp["all_share"]
slot_cmp = slot_cmp.sort_values(["light_orders", "over_index"], ascending=False)

# After cream is reserved for slot 1, leftover candidates exclude serums/creams
leftover = slot_cmp[~slot_cmp.index.to_series().str.contains("Serum|Cream", case=False, regex=True)]
print("Top products in light-buyer orders (all SKUs):")
display(slot_cmp.head(12))
print("\\nLeftover-slot candidates (exclude Serum/Cream — those are the trigger / slot 1):")
display(leftover.head(8))

fig, ax = plt.subplots(figsize=(8, 4.2))
plot_df = leftover.head(8)[["light_orders", "all_orders"]].iloc[::-1]
plot_df.plot.barh(ax=ax, color=[ACCENT, LIGHT])
ax.set_xlabel("Orders containing the SKU")
ax.set_title("Leftover shelf slots: light-buyer presence vs overall")
ax.legend(["Light-buyer orders", "All orders"], frameon=False)
fig.tight_layout()
fig.savefig(FIG / "fig_light_buyer_slots.png", dpi=160, bbox_inches="tight", facecolor=PAPER)
plt.show()
"""
    )
    light_slots_interp = md(
        """
**Results interpretation**

1. Light buyers' most common non-serum/non-cream SKUs include **Clay Purifying Mask** (27 light orders), **Deep Clean Foam** (22), **Essence Toner** (21) and **Cooling Eye Gel** (21). Several of these are **over-indexed** vs the overall catalogue (over-index > 1).
2. Overall bestsellers are pulled by heavy buyers' volume. Filling leftover slots from the light-buyer list above keeps the shelf from quietly becoming a heavy-buyer catalogue after slot 1.
3. These counts are still thin (tens of orders). They rank leftover slots; they do not replace the Serum → Cream category rule.
"""
    )

    # Update pilot cell with honest sample-size note
    set_source(
        cells[85],
        """
## 10d · Expected results and the condition that drops the action *(professor feedback)*
Past data cannot measure a shelf that did not exist. The decision therefore ships with a pilot, an expected result, and an explicit kill switch. We also state the sample-size limit of a six-week split honestly before someone else does.
""",
    )
    set_source(
        cells[86],
        """
avg_open = float(per_month.mean())
half_6w = avg_open * 1.5 * 0.5   # 6 weeks ≈ 1.5 months; 50/50 split
# Approximate equal-arm sample size to distinguish 5% from 2% (α≈0.05, 80% power)
p1, p2 = 0.05, 0.02
pbar = (p1 + p2) / 2
n_per_arm = 2 * ((1.96 + 0.84) ** 2) * pbar * (1 - pbar) / ((p1 - p2) ** 2)
months_needed = n_per_arm / (avg_open * 0.5)
weeks_needed = months_needed * (365.25 / 12 / 7)

pilot = pd.DataFrame([
    ("Start", "1 December 2026 (day after the data window)"),
    ("Design", "Random half of buyers see the new order-based shelf; half keep the current shelf"),
    ("Safety window", "Six weeks (until 11 January 2027) — enough to catch failure or light buyers left behind"),
    ("Uplift read", f"Keep the split running ~{weeks_needed:.0f} weeks / ~{months_needed:.0f} months "
                   f"(≈{n_per_arm:.0f} serum-only orders per half) before claiming 5% vs 2%"),
    ("6-week n per half", f"≈{half_6w:.0f} serum-only orders; at 5% that is only ≈{half_6w*0.05:.0f} extra creams"),
    ("Expected result", "≥ 5% of serum-only orders in the treatment half add a cream "
                       f"(≈ ¥{avg_open * 0.05 * cream_value:,.0f} / month at the low end), "
                       "read after the longer window"),
    ("Report by", "First-time vs repeat buyers, and light vs heavy"),
    ("Drop if (a)", "Treatment cream add-on rate < 2% and not above control after the six-week safety check"),
    ("Drop if (b)", "Light / first-time add-on rate is materially below heavy buyers "
                   "(shelf has drifted toward heavy-buyer taste)"),
    ("Drop if (c)", "Re-mine on the control half shows Serum -> Cream same-order lift ≤ 1"),
], columns=["item", "detail"])
print(f"Pilot honesty: ~{half_6w:.0f} serum-only orders / half in 6 weeks; "
      f"~{n_per_arm:.0f} / half needed to separate 5% from 2% (≈{weeks_needed:.0f} weeks).")
pilot
""",
    )

    # Conclusion update
    set_source(
        cells[87],
        """
## 12 · Conclusion: what should the shelf show, and to whom?

1. **WHAT TO SHOW:** a cream after any serum. Serum → Cream is the only strong pattern in single orders (256 / 3,401 orders; lift 1.75); product pairs only help choose which cream to show first. Leftover slots follow products light buyers buy most (Clay Purifying Mask, Deep Clean Foam, Essence Toner…), not overall bestsellers.
2. **HOW TO BUILD IT:** from single orders, not from whole histories, which are 93% written by heavy buyers and pair products that are not bought together.
3. **TO WHOM:** one shelf for everyone, including buyers with no history. The rule holds for every buyer type, in both channels and on first orders (lift 1.80). The light-vs-heavy stretch does not justify two shelves.
4. **WHY IT SHOULD HOLD:** serum and cream are complementary steps in a skincare routine — the data match that prediction across segments.
5. **WHAT IT IS WORTH / HOW TO TEST:** ¥2,200–6,600 per month is a scenario (0.6–1.7% of GMV). The sharper stake is 301 light buyers otherwise served by heavy-buyer rules. Use six weeks as a **safety check**; read the uplift after a longer split (~40 weeks / ~585 serum-only orders per half to separate 5% from 2%). Drop under the kill conditions in §10d.
""",
    )

    set_source(
        cells[88],
        """
## AI-use appendix

- **Claude (Anthropic):** helped draft early notebook structure from the Week 2 / Week 3 course patterns, proposed robustness checks (first-order slice, heavy cut-offs, shelf decision cards), and suggested wording for manager-facing findings.
- **Cursor (Composer):** helped revise code cells, rebuild charts in the Lumen palette, generate the report and slide builders, and keep numbers aligned across notebook, report and slides after each data re-run.
- **Team review:** every cell was re-run on the course Lumen Beauty CSVs; every shipped number was checked against notebook output. No platform personal data left the course environment.

Every member of this team can explain every line of code and every number in this notebook.
""",
    )

    # --- Reorder: move stretch / cards / pilot / light-slots before section 11 ---
    # Current indices: 78=##11, 79=metrics code, 80=##10b, 81=stretch code, 82=stretch md,
    # 83=##10c, 84=cards code, 85=##10d, 86=pilot code, 87=##12, 88=AI
    # We will rebuild the tail from cell 78 onward.

    head = cells[:78]  # up through chart 10 / before ## 11
    section_11 = cells[78:80]  # ##11 + metrics code
    stretch = cells[80:83]  # 10b
    cards = cells[83:85]  # 10c
    pilot = cells[85:87]  # 10d
    conclusion = cells[87:89]  # 12 + AI

    # Insert theory cell before method section (cell 31 currently)
    # After reorder construction, find "## 5 · One function"
    theory_cell = md(
        """
## 4c · Theory lens (what we expect before mining)
Two linked predictions guide the analysis:

1. **STP targeting ("to whom").** If the shelf is trained on whole purchase histories, heavy buyers will dominate the evidence. A manager who wants one shelf for everyone should not use that evidence base.
2. **Product complementarity ("what").** In a skincare routine, serum and cream are complementary steps. That predicts a Serum → Cream rule with lift > 1, a clear direction (cream after serum), and the same pattern in every segment — light buyers, first orders, livestream and store — not only among heavy buyers.

Algorithmic bias is treated as the **ethics** stake of a history-trained shelf (section on ethics in the report appendix), not as the explanation of why serum and cream co-occur.
"""
    )

    # Find insertion point in head for theory (before ## 5)
    insert_at = None
    for i, c in enumerate(head):
        src = "".join(c.get("source", []))
        if src.startswith("## 5 · One function"):
            insert_at = i
            break
    if insert_at is None:
        raise RuntimeError("Could not find method section to insert theory")
    head = head[:insert_at] + [theory_cell] + head[insert_at:]

    # New tail order: 10b stretch, 10c cards, 10e light slots, 10d pilot, 11 metrics, 12 conclusion
    new_cells = (
        head
        + stretch
        + cards
        + [light_slots_md, light_slots_code, light_slots_interp]
        + pilot
        + section_11
        + conclusion
    )
    nb.cells = new_cells

    # Renumber section 11 header stays; ensure ## 11 still says main numbers
    nbformat.write(nb, OUT)

    print(f"patched → {OUT} ({len(nb.cells)} cells). executing…")
    import os

    os.chdir(ROOT)  # notebook uses Path("data") and Path("figures")
    client = NotebookClient(
        nb,
        timeout=600,
        kernel_name="python3",
        resources={"metadata": {"path": str(ROOT)}},
    )
    client.execute()
    nbformat.write(nb, OUT)
    nbformat.write(nb, MIRROR)
    print("executed OK →", OUT, "and", MIRROR)


if __name__ == "__main__":
    main()

# Team 5 · Q15 Pitch Script
**Deck:** `deliverables/NMTA_T05_slides.pptx` (11 slides)  
**Time:** about **7 minutes** (must finish before 8)

Speak normally. Short sentences. Point at the chart, then say the one number that matters.

---

## Timing

| # | Slide | Sec |
|--:|-------|----:|
| 1 | Title | 20 |
| 2 | Introduction | 40 |
| 3 | Theory | 30 |
| 4 | Data | 30 |
| 5 | Method | 30 |
| 6 | Findings 1 | 45 |
| 7 | Findings 2 | 40 |
| 8 | Findings 3 | 35 |
| 9 | Limits | 25 |
| 10 | Recommendation | 50 |
| 11 | Ethics | 15 |

Skip ethics if you are already near 7 minutes.

---

## Slide 1 — Title

Hi, we are Team 5.

After someone buys from Lumen Beauty, they see a “you may also like” shelf.  
We asked: **what should that shelf show, and who is it for?**

---

## Slide 2 — Introduction

Right after checkout, the Douyin mini-program shows this shelf.

The team has to choose which product to recommend — and whether everyone should see the same thing.

Why bother? **65% of orders have only one product.** So most people leave without a second item.

If 5 to 15% of serum-only buyers also bought a cream, that could mean about **¥2,200 to ¥6,600 extra per month**. That is a scenario, not something we already measured.

We looked at **3,401 orders from 647 buyers**.

---

## Slide 3 — Theory

We started with two simple ideas.

First: if you build rules from a customer’s **whole history**, people who buy often will dominate — they have bought more products, so they create more pairs.

Second: serum and cream belong to the same skincare routine, so they should often be bought together, with **cream after serum**.

**Lift** just means: do two products show up together more than by chance? Above 1 = yes. Below 1 = no.

---

## Slide 4 — Data

This chart is the problem with histories.

Heavy buyers are **41% of customers** but make **80% of orders**.  
Light buyers are almost half the customers, but only about **11% of orders**.

So if the shelf learns from histories, it mostly learns from heavy buyers.

Data check, briefly: we used the course order and user files, removed 5 duplicate lines, and kept **3,401 orders**. We split buyers by how often they order, not by how much they spend.

---

## Slide 5 — Method

We used the same association-rule method in two ways.

**Order basket** = products in **one** checkout. That is when the shelf appears. Average **1.45** products.

**History basket** = everything a customer bought in three months. Average **6.27** products.

We only look at product **pairs**, because the shelf suggests one extra item. We always show the raw counts, not only percentages.

---

## Slide 6 — Findings 1: Serum → Cream

Main result: in the same order, **serum and cream go together**.

**256** orders have both. By chance you’d expect about **147**. Lift is **1.75**.  
About **40%** of serum orders also have cream — only **33%** the other way. So recommend **cream after serum**.

Each month, about **127** serum orders still leave **without** cream. Those are the people the shelf can still help.

No other category pair is this strong. Product-level rules are weaker — they only help pick **which** cream.

---

## Slide 7 — Findings 2: Don’t use histories for this

Histories look richer: **870** rules vs **30** from orders. That is mostly because history baskets are bigger — they mix products bought on different days.

Example: two toners look linked in a history (lift **2.15**), but in the same order the lift is **0.37**. People tried them at different times. That is not “frequently bought together.”

Heavy buyers also dominate the evidence — even when we change the cut-off. So a history shelf would mostly reflect frequent buyers.

---

## Slide 8 — Findings 3: One shelf is enough

Serum → Cream still works for light, mid, and heavy buyers. Lift stays around **1.7 to 1.9**.

It also works on **first orders** (lift **1.80**). So even someone with no history can get this recommendation from the current basket.

If we mine light and heavy orders separately, Serum → Cream is still the top rule in both.  
So we do **not** need different shelves for different groups.

---

## Slide 9 — Limits

Be honest about what we cannot claim.

Buying together does not prove the shelf will cause the next sale. The yuan figure is only a scenario. Some product-level counts are small. Six weeks of testing is too short to prove 5% vs 2%.

Also, once the shelf is live, it can create the pairs we later measure — so we should check the control group too.

---

## Slide 10 — Recommendation

What we recommend:

**Show a cream after a serum** — to everyone, including first-time buyers.  
Build that from **order** data, not full histories.

Use product pairs only to rank which cream. Fill other slots with products light buyers like, not just overall bestsellers.

**Test it:** from 1 December, half see the new shelf, half keep the old one.  
First **six weeks** = safety check only. A longer run is needed to see if we really get about a 5% add-on.

Stop the test if it clearly fails: add-on under 2% and no better than control, light or first-time buyers left behind, or the pattern disappears in the control data.

---

## Slide 11 — Ethics (short)

One fairness point: a history shelf would mostly be built from heavy buyers, while almost half the customers are light buyers.

An order-based shelf only needs the current basket. Call it “often bought in the same order,” not “frequently bought together,” if the products were not actually bought together.

Thank you — questions welcome.

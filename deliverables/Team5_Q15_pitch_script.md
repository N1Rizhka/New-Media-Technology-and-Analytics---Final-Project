# Team 5 · Q15 Speaker Notes (final report aligned)
**What should the “you may also like” shelf show, and to whom?**  
Target **~7:00–7:15** · hard stop before **8:00** · 14 slides

Speak naturally. Do not read the report. If late, cut lines marked `[cut]`.

**Pace:** ~130–140 words/min · spoken body ≈ **950–1,000 words** → about **7 minutes**.

---

## Timing map

| # | Slide | Sec | Cum. |
|--:|-------|----:|-----:|
| 1 | Title | 25 | 0:25 |
| 2 | Why the shelf matters | 45 | 1:10 |
| 3 | Theory | 35 | 1:45 |
| 4 | Who places the orders? | 30 | 2:15 |
| 5 | Method | 35 | 2:50 |
| 6 | Serum → Cream | 40 | 3:30 |
| 7 | The open slot | 25 | 3:55 |
| 8 | Histories flood the rules | 35 | 4:30 |
| 9 | History ≠ bought together | 30 | 5:00 |
| 10 | One shelf for everyone | 35 | 5:35 |
| 11 | Monday morning | 50 | 6:25 |
| 12 | Limits | 25 | 6:50 |
| 13 | Close | 25 | 7:15 |
| 14 | Ethics appendix | 15 | **7:30** |

If you hit slide 12 after **6:40**, skip slide 14 speech.

---

## Slide 1 — Title *(0:25)*

Hi everyone — we are Team 5.

After a purchase in Lumen Beauty’s Douyin mini-program, customers see a “you may also like” shelf. Our question: **what should that shelf show, and to whom?**

We use association rules on orders from September to November 2026, and we compare two ways of learning the recommendations.

---

## Slide 2 — Why the shelf matters *(0:45)*

In our window the shelf would appear after every completed order: **3,401 orders from 647 buyers**.

**65% of those orders — 2,219 — contain only one product.** Most checkouts leave an empty second slot.

Serum without cream is the clearest opportunity: about **127 serum-only orders per month**. If 5 to 15% of them added a cream at ¥346.52, that is a scenario of **¥2,206 to ¥6,619 per month** — about 0.6 to 1.7% of monthly GMV. Scenario only — not a measured effect.

The sharper stake is who the shelf is trained on. A history-trained shelf would still be shown to **301 light buyers — 46.5% of customers** — but only **about 1.7% of the evidence** behind those rules would come from them.

So: who trains the shelf?

*[cut if late]* Lift means how much more often two products appear together than chance alone.

---

## Slide 3 — Theory *(0:35)*

Two predictions before mining.

**STP:** if we train on full customer histories, heavy buyers will dominate the evidence.

**Complementarity:** serum and cream are sequential skincare steps — they should co-occur more than chance, cream after serum, across segments and first orders.

Algorithmic bias is the ethics cost of the wrong evidence base — Appendix A1 — not the explanation of the co-purchase itself.

---

## Slide 4 — Who places the orders? *(0:30)*

Light buyers are **46.5% of customers** but only **10.8% of orders**.

Heavy buyers are **41% of buyers** and place **80.3% of orders**.

If recommendations come from histories, the algorithm hears that 41% first. That is why “to whom?” is not optional.

---

## Slide 5 — Method *(0:35)*

Week 3 Apriori in Python, product **pairs only** — the shelf suggests one add-on.

**Order basket** = products in one checkout — the shelf moment.  
**History basket** = every distinct product a customer bought in the quarter.

We report support, confidence, and lift with counts and denominators. Thresholds are frequency filters, not significance tests.

Order product rules need at least **14 of 3,401** orders; history rules at least **13 of 647** customers. Segments by order count: light 1–2, mid 3–5, heavy 6+.

---

## Slide 6 — Serum → Cream *(0:40)*

Finding two: **Serum → Cream** is the only strong category rule in same-order baskets.

**256 of 3,401** orders have both; chance expects about **146.5**. Support 0.075, confidence **0.40**, lift **1.75**.

Direction: cream after serum is stronger than the reverse (0.40 vs 0.33). Every other category pair at 1% support has lift below one.

SKU pairs — Vitamin C Serum to Hydra Gel or Brightening — only **rank** which cream. They rest on 26 and 27 orders.

*[cut if late]* Livestream lift 1.73, store 1.80 — not only a livestream bundle.

---

## Slide 7 — The open slot *(0:25)*

Each month, many serum buyers still leave without cream: **137, 124, and 121** across Sep–Oct–Nov — about **127 per month**.

Those are the addressable checkouts for slot one.

---

## Slide 8 — Histories flood the rules *(0:35)*

Finding one: same frequency idea, different answers — **30 order rules** versus **870 history rules**. Histories cover every directed pair among 30 SKUs, all with lift above one.

Why? History baskets average **6.27** products; orders average **1.45**. Histories invent pairs never bought together.

Prediction 1 confirmed: heavy buyers contribute **92.9%** of history-pair evidence — and that dominance holds at every cut-off we tried.

---

## Slide 9 — History ≠ bought together *(0:30)*

Finding four: high history lift is not “frequently bought together.”

Example: Calming Toner Mist → Pore Refining Toner has history lift **2.15**, but same-order lift **0.37** — only **three** joint orders versus about eight expected.

Heavy buyers may try alternatives on different days. Labelling that “bought together” would misrepresent the data.

---

## Slide 10 — One shelf for everyone *(0:35)*

Finding five: do we need separate shelves?

No — if we mine from **orders**. Serum → Cream lift stays above one for light, mid, and heavy — **1.79, 1.93, 1.72** — and on **first orders alone, 1.80**.

Mined separately in light and heavy order baskets, Serum → Cream is still the primary category rule in both. Prediction 2 confirmed. One shelf is enough.

---

## Slide 11 — Monday morning *(0:50)*

So the decision: mine from **order baskets**, not histories. Whenever the current basket has serum and no cream, show a cream in slot one — to **everyone**, including first-time buyers.

Rank cream SKUs with order-level pairs that have enough support. Fill leftover slots with what light buyers buy most — Clay Purifying Mask, Deep Clean Foam, Essence Toner, Cooling Eye Gel — not overall bestsellers.

Pilot from **1 December**, fifty-fifty. First **six weeks** are a **safety check**: about **96 serum-only orders per half**; at 5% that is only about **five** extra creams — too few to prove 5% versus 2%.

To separate those rates, continue about **40 weeks — roughly 9 months** — toward **~588 serum-only orders per half**. Success criterion: at least 5% cream add-on in treatment. That maps to about **¥2,200 extra monthly** at the low end of our scenario. Report first-time and repeat buyers separately.

Kill switch: drop if under 2% and no better than control; if light or first-time buyers are left behind; or if control re-mining shows same-order lift at or below one.

---

## Slide 12 — Limits *(0:25)*

Association is not causation. The yuan figure is a scenario. Six weeks cannot prove 5% versus 2%. Light-buyer SKU ranks are thin — we trust the category rule more.

A live shelf can create the pairs it later mines — that is why we re-mine the control half.

---

## Slide 13 — Close *(0:25)*

Show a cream after a serum. Build the shelf from **orders**, not histories.

One shelf for everyone — including people with no history.

Six weeks to catch failure; a longer split to measure uplift. Drop it if the kill conditions fire.

Thank you — we are happy to take questions.

---

## Slide 14 — Ethics appendix *(≤0:15 if time)*

*[Skip speech if already past 7:10; leave for Q&A.]*

Appendix A1 in one line: a history shelf would serve **301 light buyers** a catalogue built **92.9%** from heavy-buyer evidence. Order rules need only the current basket; do not label cross-visit substitutes as “bought together.”

---

## Backup Q&A (not in the 7 minutes)

- **Why not 2% support on orders?** Largest pair support was 0.79% — zero product rules. We used 0.4% (≥14 orders).
- **Why segments by orders, not spend?** The question is frequency dominance of rule evidence.
- **Who uses the feature?** Post-purchase after every order (647 buyers / 3,401 orders); Serum→Cream especially addresses ~127 serum-only orders/month.
- **AI use?** Appendix A2 — Claude and Cursor helped drafting and tooling; every cell re-run; team owns every number.

# Team 5 · Q15 Pitch Script  
**What should the “you may also like” shelf show, and to whom?**  
~8 minutes · speak naturally · pause on the charts

Tip: short sentences, look at the chart, then say the one number that matters.

---

## Slide 1 — Title  
Hi everyone — we are Team 5.

Our question is:  
**after someone buys from Lumen Beauty, what should the “you may also like” shelf show — and who does that shelf serve?**

We answer this with association rules on one quarter of store data: September to November 2026.  
We will move from exploration, to the rules, to one clear recommendation.

---

## Slide 2 — Why the shelf matters  
Here is why this question is worth careful work.

Look at this chart: **65% of orders contain only one product.**  
So in most checkouts, the customer leaves with nothing else in the basket. That empty second slot is where the shelf can help — or fail.

We have 3,401 orders, 647 buyers, and about ¥1.17 million in GMV.  
If the shelf helps even 5 to 15% of serum-only orders add a cream, that is roughly **¥2,200 to ¥6,600 per month**.

That is only a scenario.  
The sharper question for us is this: **if we train the shelf badly, who do we leave out?**

---

## Slide 3 — Who places the orders?  
This chart is central to the “to whom” part of Q15.

Almost **half of buyers** are light buyers — one or two orders in the quarter.  
But they place only about **11% of all orders**.

Heavy buyers are 41% of buyers, and they place **80% of orders**.

So if we build rules from “everything a customer ever bought,” the algorithm mostly hears the heavy buyers.  
Light buyers — almost half of our customers — become hard to see in the data. That is the real risk we wanted to measure.

---

## Slide 4 — Channels and categories  
A quick look at the store.

Most orders come from **livestream**, some from the **store shelf**.  
Serums and creams appear often — they sit at the center of this assortment.

We do not need a long story here. We only need to see that co-purchase is possible, and that serum–cream is a natural place to look.

---

## Slide 5 — Method  
Our method is Week 3 association rules — kept clean and honest.

We build baskets in **two ways**:  
1. **Order baskets** — products bought together in one order. That is the moment the shelf appears.  
2. **History baskets** — everything one customer bought in the whole quarter.

We look only at **pairs**, because the shelf shows one product next to another.  
For every rule we report support, confidence, lift — and also the **count and the denominator**, so a rare pair is not mistaken for a strong one.

Our thresholds come from the business decision, not from fishing in the data: about **14 orders**, or about **13 customers**.  
And we split buyers into light, mid, and heavy by number of orders.

---

## Slide 6 — Finding: Serum → Cream  
Now the finding we trust most.

**Serum → Cream.**  
In **256 of 3,401 orders**, a serum and a cream appear together. By chance we would expect about 147. So lift is **1.75**. Confidence is **0.40** — four in ten serum orders also have a cream.

Direction matters: cream after serum is stronger than serum after cream.  
So the shelf message is clear: **after a serum, show a cream.**

This is also the only strong category pair. Other pairs at the same bar have lift below 1.  
Product-level pairs only help us choose *which* cream — and those rest on just 15 to 27 orders, so we treat them as ranking, not as the main rule.  
Importantly, the rule appears in **both livestream and store** — so it is not only a host pushing a bundle on stream.

---

## Slide 7 — The open slot  
This chart shows the opportunity in plain numbers.

Every month, more than **120 serum orders leave without a cream**.  
Those are customers who already chose a serum — and still did not add a cream.

That is exactly who the shelf can speak to: not with a random bestseller, but with a cream that people actually buy with serum.

---

## Slide 8 — Histories flood the rule table  
Here is where the second basket definition becomes important.

At almost the same minimum count, **order baskets give 30 rules**.  
**History baskets give 870** — basically every possible pair, all with lift above 1.

Why? Because history baskets are much bigger. A heavy buyer who tried many products creates many pairs, even if those products were never bought on the same day.

And look at the second chart: heavy buyers are 41% of buyers, but they create **93% of the history-rule evidence**.  
So a history-trained shelf is, in practice, a **heavy-buyer shelf**.

---

## Slide 9 — History pairs are not “bought together”  
We checked the top history pairs inside single orders.

Their history lift looks high — above 2.  
But inside the same order, lift falls **below 1**.

Example: two toners look connected across a customer’s history, but in the same order they appear together only 3 times, when chance expects about 8.

So these are products heavy buyers try on different days — often substitutes, not companions.  
If we label that shelf “frequently bought together,” we would be telling a story the data does not support. That distinction is one of the most useful results in this project.

---

## Slide 10 — One shelf for everyone?  
So should first-time buyers see a different shelf?

We tested Serum → Cream for light, mid, and heavy buyers, for livestream and store, and on each customer’s **first order**.

The rule holds everywhere. On first orders, lift is even **1.80**.

So our answer is: **one shelf is enough — if we build it from orders, not from histories.**  
A separate first-time shelf is not needed. What first-time buyers need is a shelf that was not trained only on heavy buyers’ long histories.

---

## Slide 11 — Monday morning  
Here is what we recommend the merchandising team does next.

1. Mine the shelf from **single orders**, not whole histories.  
2. After any **serum**, show a **cream**.  
3. Keep **one shelf for everyone**, including new buyers.  
4. Run a clean pilot: from 1 December, show the new shelf to a random half of buyers for six weeks.

**Success:** at least 5% of serum-only orders add a cream.  
**Stop if:** the add-on rate stays under 2% and not better than control, or light buyers are left behind, or the rule’s lift falls to 1 or below on the control half.

We are not asking the brand to believe a model forever. We are asking them to test one clear idea — and drop it if the evidence says no.

---

## Slide 12 — Close  
Three sentences.

**Show a cream after a serum.**  
**Build the shelf from orders, not histories.**  
**One shelf for everyone — including people with no history yet.**

That is how Lumen Beauty can make the “you may also like” shelf both smarter and fairer.

Thank you — we are happy to take questions.

---

## Timing guide (optional)
| Slides | Focus | About |
|---|---|---|
| 1–2 | Hook + stake | ~1:15 |
| 3–5 | EDA + method | ~2:00 |
| 6–9 | Core findings | ~3:00 |
| 10–12 | Decision + close | ~1:45 |
| **Total** | | **~8:00** |

## Speaking tips for the team
- Point to the chart first, then say one number.
- If stuck: “The simple story is cream after serum, from orders not histories.”
- For Q&A: support/confidence are frequency filters, not significance tests; the ¥ figure is a scenario; the A/B test is the real measurement.
- Interest comes from the numbers and the logic — not from calling the project exciting.

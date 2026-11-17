# Team 5 · Q15 Investor Pitch — Speaker Notes
**Deck:** designed template (`deliverables/NMTA_T05_slides.pptx`, 11 slides)
**Vote:** order-based cream-after-serum shelf + kill-switch pilot
**Target ~7:00** · hard stop before **8:00**

Rule: claim → number → implication for the vote.

## Timing

| # | Slide | Sec | Cum. |
|--:|-------|----:|-----:|
| 1 | Title | 25 | 0:25 |
| 2 | 01 Introduction | 45 | 1:10 |
| 3 | 02 Theory | 35 | 1:45 |
| 4 | 03 Data | 35 | 2:20 |
| 5 | 04 Methodology | 35 | 2:55 |
| 6 | 05 Findings 1/3 | 45 | 3:40 |
| 7 | 05 Findings 2/3 | 40 | 4:20 |
| 8 | 05 Findings 3/3 | 40 | 5:00 |
| 9 | 06 Limitations | 30 | 5:30 |
| 10 | 07 Conclusions / the ask | 55 | 6:25 |
| 11 | Appendix Ethics | 20 | 6:45 |

Skip ethics speech if already past ~6:40.

## Slide 1 — Title

(0:25)
Hi everyone — we are Team 5.
We are here for a clear vote. After checkout in Lumen Beauty’s Douyin mini-program, customers see a “you may also like” shelf. That moment can grow the basket — or quietly serve the wrong customers.
Our question for you: what should the shelf show, and should one version serve everyone?

## Slide 2 — 01 Introduction

(0:45)
Three beats on this slide.
The setting: after every completed purchase, the mini-program shows that shelf.
The decision: which product should appear, and do we show the same shelf to every buyer?
Why it matters commercially: 65% of orders leave with only one product. If 5 to 15% of serum-only orders added a cream, that is a scenario of about ¥2.2 to 6.6 thousand yuan per month — 0.6 to 1.7% of GMV. Scenario only, not a measured lift.
The evidence base is one quarter: 3,401 orders, 647 buyers, about ¥1.17 million GMV.

## Slide 3 — 02 Theory

(0:35)
Before mining, two course theories — two bets you can hold us to.
T1, targeting: if we train on whole purchase histories, frequent buyers generate far more product pairs, so history rules will be written mostly by heavy buyers.
T2, product complementarity: serum and cream are consecutive skincare steps, so Serum→Cream should show lift above one, run from serum to cream, and hold across buyer groups, channels, and first orders.
How to read lift: above one means complements; below one means substitutes or noise.

## Slide 4 — 03 Data

(0:35)
This is why “to whom?” is an investor question, not only a research question.
Heavy buyers are 41% of customers but place 80% of orders. Train on histories and the algorithm hears them first.
Data hygiene is clean: course order lines and users, September to November 2026; five duplicate lines removed; empty stream_id means store order, not missing data. Result: 3,401 orders, 647 buyers. We segment by number of orders — light, mid, heavy — not by spend, because the risk is frequency dominance.

## Slide 5 — 04 Methodology

(0:35)
Same Apriori algorithm, two definitions of a basket — that is the fork in the road.
Order basket: products bought together in one checkout — the exact moment the shelf appears. Average 1.45 products; we keep pairs with at least 14 orders.
Customer-history basket: everything one customer bought in three months, on any day. Average 6.27 products; at least 13 customers.
Support, confidence, and lift always come with counts. Thresholds filter frequency; they are not significance tests; co-purchase is not causation.
If the shelf appears at checkout, the fair training unit is the order, not the biography.

## Slide 6 — 05 Findings 1/3

(0:45)
Finding one — the product we want you to put on the shelf.
Serum→Cream is the only strong same-order category pattern. Lift 1.75: 256 orders contain both, against about 147 expected by chance. Forty percent of serum orders already include a cream — only 33% the other way — so the cream comes after the serum.
About 127 serum orders per month still leave without a cream. Those are the addressable checkouts.
Every other category pair at our threshold has lift below one. SKU rules rest on only 26–27 orders, so they only decide which cream to show first.

## Slide 7 — 05 Findings 2/3

(0:40)
Finding two — do not fund a history-trained shelf for this slot.
At a comparable frequency bar we get 870 history rules versus 30 order rules. That explosion is not more truth: histories invent pairs never bought together.
Example: the top history pair of two toners has history lift 2.15 but same-order lift 0.37 — tried on different days as alternatives, not as a bundle.
Even if we redefine heavy as ten-plus orders — only 21% of buyers — they still supply 62.8% of the history evidence. Prediction T1 confirmed.
Funding a history shelf means funding a heavy-buyer catalogue.

## Slide 8 — 05 Findings 3/3

(0:40)
Finding three — one order-based shelf is enough.
Serum→Cream lift stays between 1.72 and 1.93 for every buyer type and in both livestream and store. On first orders alone: confidence 0.43, lift 1.80. The current basket is enough; no history is required.
Mined separately, Serum→Cream is the top category rule for both light and heavy buyers. Prediction T2 confirmed.
So the ops-simple answer is also the fair answer: one shelf, trained on orders.

## Slide 9 — 06 Limitations

(0:30)
Honesty before the ask — what the data cannot show.
Association is not causation; past logs cannot measure a shelf that did not exist. The yuan figure is a scenario. SKU ranks and same-order checks of history pairs rest on small counts. Light buyers give us only 366 orders, so we trust the category rule more.
Six weeks cannot tell a 5% add-on from 2%. And once live, the shelf can create the pairs it later mines — that is why we re-mine the control half.

## Slide 10 — 07 Conclusions / the ask

(0:55)
Here is the decision we want you to approve.
Slot one: show a cream whenever the basket has serum but no cream — for everyone, including first-time buyers. Rank creams by order-level lift with enough support: after Vitamin C Serum, Hydra Gel then Brightening.
Slots two to four: light buyers’ favourites — mask, cleanser, toner, eye gel — refreshed weekly, instead of overall bestsellers shaped by heavy buyers.
Pilot from 1 December, fifty-fifty. First six weeks are a safety check — about 96 serum-only orders per half. About 40 weeks to measure uplift — about 588 per half. Success: at least 5% add a cream, about ¥2,200 extra per month at the low end of our scenario.
Drop the shelf if add-on stays under 2% and no better than control, if light or first-time buyers fall behind, or if re-mining the control half gives lift at or below one.

## Slide 11 — Appendix Ethics

(≤0:20 if early)
Ethics in one line: a history-trained shelf takes 92.9% of its evidence from heavy buyers, so 301 light buyers are barely represented.
Label the shelf “often bought in the same order,” not “frequently bought together.” An order shelf needs only the current basket. Offer a non-personalised option.
Thank you — we are happy to take questions.


# Team 5 · Q15 Pitch Script  
**What should the “you may also like” shelf show, and to whom?**  
~8 minutes · 14 slides (13 pitch + ethics appendix) · Tongji-blue deck

Tip: short sentences, look at the chart, then say the one number that matters.

---

## Slide 1 — Title  
Hi everyone — we are Team 5.  
Our question: after someone buys from Lumen Beauty, what should the “you may also like” shelf show — and who does that shelf serve?  
We answer with association rules on one quarter of store data. Exploration, theory, rules, then one clear recommendation.

## Slide 2 — Why the shelf matters  
**65% of orders contain only one product.** Most checkouts leave an empty second slot.  
Scenario value if 5–15% of serum-only orders add a cream: about ¥2,200–6,600 per month. That is modest.  
The sharper stake: **301 light buyers** (46.5%) would be served by history rules that are only **1.7%** built from them.  
Lift, in one line: how much more often two products appear together than chance alone would predict.

## Slide 3 — Theory  
Two predictions before we mine.  
**STP:** if we train on whole histories, heavy buyers will dominate the evidence.  
**Complementarity:** serum and cream are sequential skincare steps — they should co-occur more than chance, with cream after serum, in every segment.  
Algorithmic bias is the ethics cost of choosing the wrong evidence base — not the explanation of the co-purchase itself.

## Slide 4 — Who places the orders?  
Almost half of buyers are light, but they place only about 11% of orders. Heavy buyers place 80%.  
So history rules hear heavy buyers first. That is why “to whom?” is not optional.

## Slide 5 — Method  
Order baskets = the shelf moment. History baskets = the whole quarter. Pairs only.  
Support and confidence filter frequency; they are not significance tests. Every rule carries count and denominator.  
Thresholds from the decision: ≥14 orders, ≥13 customers.

## Slide 6 — Serum → Cream  
256 of 3,401 orders have both; chance expects about 147. **Lift 1.75**, confidence 0.40.  
Show cream after serum. Only strong category pair. Holds in livestream and store. Matches complementarity.

## Slide 7 — The open slot  
About **127 serum orders per month** leave without a cream (Sep 137, Oct 124, Nov 121). That is who the shelf can still speak to.

## Slide 8 — Histories flood the rules  
Same bar: **30 order rules** vs **870 history rules**.  
Heavy buyers = 41% of buyers but **92.9%** of history-rule evidence. Prediction 1 confirmed.

## Slide 9 — Not bought together  
Top history pairs look strong over time, but inside one order lift falls **below 1**.  
Substitutes across visits — not “frequently bought together.”

## Slide 10 — One shelf for everyone  
Serum → Cream holds for light / mid / heavy and on **first orders** (lift 1.80).  
One shelf is enough — if we build it from orders, not histories.

## Slide 11 — Monday morning  
Mine from orders. Cream after serum. Leftover slots from what light buyers buy most.  
Six weeks = **safety check** (~90 serum-only orders per half). Read uplift after ~40 weeks (~585 per half) before claiming 5% vs 2%.  
Drop if add-on &lt; 2%, light buyers left behind, or control lift ≤ 1.

## Slide 12 — Limits  
Association is not causation. The yuan figure is a scenario. Six weeks cannot prove 5% vs 2%. Light-buyer SKU ranks are thin. A live shelf can create the pairs it later mines — hence the control-half re-mine.

## Slide 13 — Close  
Show a cream after a serum. Build the shelf from orders, not histories.  
One shelf for everyone — including people with no history.  
Six weeks to catch failure; a longer split to measure uplift. Drop it if the kill conditions fire.  
Thank you — we are happy to take questions.

## Slide 14 — Ethics appendix  
A history shelf would serve 301 light buyers a heavy-buyer catalogue.  
Do not mislabel substitutes as “bought together.”  
Order-based rules need only the current basket. Offer a non-profiled option (Art. 17).  
Re-mine on the control half; report by buyer type; drop under the kill conditions.

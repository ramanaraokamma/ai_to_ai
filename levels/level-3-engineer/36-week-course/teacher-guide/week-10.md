# Week 10 — The Threshold Dial, and the Curve It Draws

[⬅ Week 9](week-09.md) · [Course Home](../README.md) · [Week 11 ➡](week-11.md) · [Student Guide](../student-guide/week-10.md) · [Workbook](../workbook/week-10.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — one hidden number is taken out of the box and handed to the student |
| **Big idea** | **0.5 is not a law, it is a default.** Turning the dial trades misses for false alarms, and the curve it traces is the model's whole personality. |
| **New vocabulary** | decision threshold · true positive rate · false positive rate · ROC curve · precision-recall curve · average precision |
| **New maths** | **Steepness of a curve between two points, as rise over run.** Computed from two real points taken off the class's own ROC curve, and read out loud as *"how much recall you buy per false alarm"*. |
| **New syntax** | `(prob >= t).astype(int)` · `roc_curve(y, prob)` · `precision_recall_curve(y, prob)` · `average_precision_score(y, prob)` |
| **Dataset** | Week 8's `make_classification(n_samples=5000, n_features=8, n_informative=4, n_redundant=0, weights=[0.99, 0.01], random_state=0)` fraud table — 1,000 validation rows, **14 of them real fraud**. **Nothing downloads. No internet needed.** |
| **Materials** | **20 index cards, written and shuffled before class** (exact numbers below) · a long strip of wall or a whiteboard for the probability line · **one sheet of squared graph paper per student**, plus one big sheet for the wall · three sticky notes · the printed workbook (`workbook/week-10.md`: Warm-Up, Do the Maths by Hand, Predict the Output, Practice Sets A and B, Fix the Broken Program, Puzzle, Think Deeper, Build It, Draw It, Self-Check; print it without its final Answers section) · **Week 8's 2×2 and Week 9's harmonic-mean board still up** · the Bug Log |
| **Tech needed** | Laptop with Python 3, numpy, scikit-learn, matplotlib. **No new installs.** |
| **Prep time** | 25 minutes the night before (10 of them writing the 20 index cards) · 5 minutes on the day |
| **Expected runtime of the code** | `dial.py` **under 2 seconds** including the saved figure. `cards.py` **under 1 second**. Nothing this week trains for longer than a blink. |

> **⚠️ Watch out:** the single most surprising thing in this lesson is that **our fraud model's highest probability is 0.1774**, so at the default threshold of 0.5 it flags **absolutely nothing** — 0 out of 1,000 rows. That is not a bug and you must not "fix" it. It is the most convincing possible proof of this week's big idea, and the lesson is built on it. Read §3 below before you teach, or you will apologise for the best thing in the file.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Turn predicted probabilities into yes/no answers at nine different thresholds** and tabulate precision, recall and false-alarm count at each, in one table, on one screen.
2. **Measure the steepness of their own ROC curve between two of its own points** using rise over run, and say in plain English what a steep left-hand section means.
3. **Read an ROC curve and a precision-recall curve** and say which one to trust when positives are rare, with a reason that mentions the denominator.
4. **Mark three thresholds they would defend out loud** and say, for each one, which stakeholder it is right for.

Observable evidence: a nine-row table with precision, recall and false alarms in it; two rise-over-run divisions written out with the rise and the run named; a saved two-panel figure; and three thresholds circled on graph paper with a named person beside each.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each one carries on from the one above. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**There is one new piece of maths this week and it is a division.** If you can work out that a hill which climbs 20 cm over a run of 10 cm is twice as steep as one which climbs 10 cm over 10 cm, you already have it. What takes the twenty minutes is not the maths — it is understanding *what has been happening every time the student typed `predict`* for the last nine weeks, because until you can say that in one sentence, the lesson has no hook.

### 1. The one sentence this week exists for

> **Your classifier does not produce a class. It produces a number between 0 and 1. Something else turns that number into a yes or a no, and that something else is a comparison against 0.5 that nobody chose.**

That is it. Everything below is that sentence, slowly.

For nine weeks the student has written `model.predict(X)` and got back a column of 0s and 1s. What actually happened inside is two steps, and only the first one is the model:

1. The model computes a **probability** for each row — its confidence that the row is fraud. Row 41 gets 0.1774. Row 812 gets 0.0002.
2. Something compares each probability to **0.5** and writes down 1 if it is bigger and 0 if it is not.

Step 1 is the machine learning. **Step 2 is a policy decision, taken by a default value in a library, on behalf of a bank.** The student has never seen it, has never been asked about it, and this week they get it.

### 2. Where you can see the hidden number

They already have the tool. `predict_proba` was Week 2's new syntax:

```python
prob = model.predict_proba(X_val)[:, 1]
```

`predict_proba` hands back a **two-column** grid: column 0 is "probability this row is legit", column 1 is "probability this row is fraud". `[:, 1]` means *"every row, column 1"* — take the fraud column. The two columns always add to 1 for each row, so column 0 carries no extra information; we take the one we care about.

And now the reveal, which you should do with your own hands before class:

```python
pred_from_predict = model.predict(X_val)
pred_from_prob = (prob >= 0.5).astype(int)
print((pred_from_predict == pred_from_prob).all())     # True
```

**`predict` is `predict_proba` followed by `>= 0.5`.** Nothing more. Once a student has seen those two lines agree, the rest of the lesson pushes itself.

**`(prob >= t).astype(int)` is this week's most important line of syntax and it is worth explaining in three pieces**, because a teacher who has never programmed will otherwise read it as one blob:

| Piece | What it does |
|---|---|
| `prob >= t` | Compares **every one of the 1,000 numbers** to `t` at once, and hands back 1,000 `True`/`False` answers. numpy does the loop for you. |
| `.astype(int)` | Turns every `True` into `1` and every `False` into `0`, because the metric functions want 0s and 1s, not `True`s and `False`s. |
| the whole line | *"Flag every row whose probability is at least `t`."* |

> **💡 Try this:** in a terminal, `import numpy as np`, then `a = np.array([0.9, 0.4, 0.6])`, then `print(a >= 0.5)` and then `print((a >= 0.5).astype(int))`. You get `[ True False  True]` and then `[1 0 1]`. Sixty seconds, and you will never fumble that line in front of a class.

### 3. Our model tops out at 0.1774, and that is the gift

Here is the real output of the first three lines of this week's code. **Every number below was printed by a machine; none of it is invented.**

```text
val rows 1000   real frauds 14   real legit 986
lowest probability 0.0001    highest probability 0.1774
how many are above 0.5? 0
```

**Read that last line again. Zero.** The most suspicious transaction in the entire validation set — the one the model is most confident about — gets a fraud probability of **0.1774**. It is not above 0.5. So at the default threshold this model flags **nothing at all**, catches **none** of the 14 frauds, and is 98.6% accurate.

Why so low? Because only 1% of the training rows were fraud. A model that has seen 3,000 rows of which 44 were fraud learns, correctly, that fraud is rare — so even for a suspicious row its honest answer is *"probably still not fraud, but this one is about twelve times more suspicious than average"* (the average score is about 0.014; 0.1774 is about twelve times that). **The ranking is informative. The absolute number is small.** Those are two different things, and separating them is the whole intellectual content of this week.

> **🧑‍🏫 If a student asks** *"is the model broken?"* — No. Ask them: *"of the 8 transactions with the highest probability, how many were really fraud?"* The answer is 3 out of 8, against a background rate of 14 in 1,000. The model has taken a 1.4% haystack and handed you a pile that is 37.5% needles. **It has done its job. What is broken is the 0.5.**

### 4. The sweep, and what a threshold actually buys

Now turn the dial. Same model, same 1,000 rows, same 1,000 probabilities — **only the comparison number changes.** This is the real output of `dial.py`'s sweep, and it is the table the whole lesson is built around:

```text
   t   flagged  tp  fp  fn   tn  precision  recall     fpr
 0.50       0   0   0  14  986     0.0000  0.0000  0.000000
 0.15       1   1   0  13  986     1.0000  0.0714  0.000000
 0.12       2   2   0  12  986     1.0000  0.1429  0.000000
 0.10       8   3   5  11  981     0.3750  0.2143  0.005071
 0.08      15   3  12  11  974     0.2000  0.2143  0.012170
 0.06      25   3  22  11  964     0.1200  0.2143  0.022312
 0.04      65   4  61  10  925     0.0615  0.2857  0.061866
 0.02     216   5 211   9  775     0.0231  0.3571  0.213996
 0.01     429   8 421   6  565     0.0186  0.5714  0.426978
```

Four things to have solid before you stand up:

**One — recall never falls as the threshold drops; precision has no such promise.** (Down this table precision happens to collapse, after jumping from the meaningless 0 at the top row to 1.0.) Read the precision column downwards: 0.0000, 1.0000, 1.0000, 0.3750, 0.2000, 0.1200, 0.0615, 0.0231, 0.0186. Read recall downwards: 0.0000, 0.0714, 0.1429, 0.2143, 0.2143, 0.2143, 0.2857, 0.3571, 0.5714. **Recall never goes down as the threshold drops** — you can only ever add rows to the flagged pile, never remove them, so a fraud you already caught stays caught. Precision is under no such obligation, and here it collapses.

**Two — the row from `t = 0.10` to `t = 0.06` is the cruellest thing on the page.** `tp` stays at 3. `fp` goes 5, 12, 22. You lowered the bar three times, added **seventeen** innocent customers to the flagged pile, and caught **not one extra fraud.** Every one of those seventeen is a real person getting a phone call. Point at that with your finger in class.

**Three — the honest arithmetic behind every cell.** Take `t = 0.10`: 8 rows flagged, 3 of them really fraud.

```text
precision = 3 ÷ 8   = 0.3750     "of the 8 I flagged, 3 were fraud"
recall    = 3 ÷ 14  = 0.2143     "of the 14 real frauds, I caught 3"
fpr       = 5 ÷ 986 = 0.005071   "of the 986 innocent rows, I bothered 5"
```

**Three different denominators: 8, 14 and 986.** That is the entire skill of this week. Week 8 gave them precision and recall; this week adds the third fraction, and the third one has the *biggest* denominator, which is why it behaves so strangely.

**Four — the counts always add to 1,000.** `tp + fp + fn + tn`. Check the `t = 0.02` row: 5 + 211 + 9 + 775 = 1,000. ✅ Make the class do this once. It catches almost every arithmetic slip they will make.

### 5. Two new fractions, and which denominator each one uses

> **True positive rate (TPR)** — of all the things that really were positive, the fraction you caught. `TP ÷ (TP + FN)`. **This is exactly recall under a second name**, and you should say that out loud, because a student who thinks they are learning a new idea will be confused for a month.

> **False positive rate (FPR)** — of all the things that really were negative, the fraction you wrongly flagged. `FP ÷ (FP + TN)`.

Why two names for recall? Historical accident: the ROC curve came out of radar operators in the 1940s, where the pair *true positive rate* and *false positive rate* reads naturally as "how many real aeroplanes did we spot, how many geese did we shoot at". The machine-learning world kept both vocabularies. **Tell the student it is one number with two names.** They will meet both in every paper they ever read.

Now the crucial contrast, and this is the sentence to write on the board:

| | Its denominator | On our data | So one extra false alarm moves it by |
|---|---|---|---|
| **precision** | how many I flagged | 8, or 216, or 429 | a **lot** while the flagged pile is small (8 rows), less as it grows |
| **false positive rate** | how many were really innocent | **always 986** | 1 ÷ 986 = **0.001** — the same small step every time |

**Precision and false positive rate are both "how bad are my false alarms", measured against two completely different backgrounds.** When the innocent pile is enormous, FPR climbs only 0.001 per false alarm and has room up to 1, while precision is dragged down because the false alarms fill the very pile it is divided by. Hold that thought — it is the reason the two curves in §8 disagree so violently.

### 6. The ROC curve is that table, plotted

> **ROC curve** — the picture you get by plotting true positive rate up the side against false positive rate along the bottom, one dot per threshold, from a threshold of 1 down to a threshold of 0.

That is the whole definition. **One model, many dots.** Each dot is not a different model — it is the *same* model with a different comparison number. This is the single most common misunderstanding in the topic and it is worth saying three times.

![One ranking, three places to cut](../figures/fig-w10-1-threshold-dial-moving-the-cut.svg)
*Figure 10.1 — One ranking, three places to cut. Twenty transactions laid out by the probability the model gave them, and three places you could put the knife. Nothing about the model changes between the panels.*

The twenty cards in Figure 10.1 are the ones you are going to write out tonight, and they are deliberately kinder than the real data: ten frauds, ten legitimate rows, probabilities spread all the way from 0.05 to 0.96. Every number in the class's hand-drawn curve comes out in clean tenths, because both denominators are 10.

Here is what the finished hand-drawn curve looks like, with three thresholds marked:

![One curve, three thresholds you could defend](../figures/fig-w10-2-roc-curve-three-thresholds-marked.svg)
*Figure 10.2 — One curve, three thresholds you could defend. The ringed number on the curve matches the ringed number on its panel; that is how you read a chart with three annotations on it without drawing three lines across the data.*

**The dashed diagonal is what a coin gets**, and it is worth a full minute. If you flag rows at random, then whatever fraction of the innocent pile you flag, you will flag about the same fraction of the fraud pile — so TPR ≈ FPR and you sit on the diagonal. **Above the diagonal means your ranking carries information. On the diagonal means it does not. Below the diagonal means your ranking is backwards — most often the labels are the wrong way round (or the score is flipped); turn it upside down and you beat the coin**, which is a real bug and a funny one.

The two corners are worth naming too:

- **Bottom-left (0, 0)** — a threshold so high you flag nothing. Zero false alarms, zero frauds caught. This is our model at 0.5.
- **Top-right (1, 1)** — a threshold so low you flag everything. Every fraud caught, every innocent customer bothered.
- **Top-left (0, 1)** — the impossible dream: all the frauds, none of the innocents.

### 7. 🔢 The new maths: steepness between two points

**This is the week's one new idea and it must be taught with a ruler, not a symbol.**

Take any two points on the curve. Ask two questions:

- **How much did it climb?** That is the **rise** — the difference in true positive rate.
- **How far along did it go?** That is the **run** — the difference in false positive rate.

Then divide.

> **🔢 The maths, slowly:** steepness between two points = **rise ÷ run**. Nothing else. On the card curve, going from the point at threshold 0.90 to the point at threshold 0.80:
>
> ```
> rise  =  0.40 − 0.20  =  0.20        (true positive rate went up by 0.20)
> run   =  0.10 − 0.00  =  0.10        (false positive rate went up by 0.10)
>
> steepness  =  0.20 ÷ 0.10  =  2.0
> ```
>
> Say it in English: **"for every one unit of false-alarm rate I spent, I bought two units of recall."** That is a bargain, and you can hear that it is a bargain.

Now do it on a flat bit. From threshold 0.60 to threshold 0.50:

```text
rise  =  0.80 − 0.80  =  0.00
run   =  0.30 − 0.20  =  0.10

steepness  =  0.00 ÷ 0.10  =  0.0
```

**Zero.** You blocked one more innocent card in ten and caught nothing. Not a bargain. A pure loss.

![How steep is the curve between these two points?](../figures/fig-w10-3-steepness-rise-over-run-on-the-roc.svg)
*Figure 10.3 — How steep is the curve between these two points? Both divisions written out. The steep bit on the left is cheap recall; the flat bit is money spent for nothing.*

And now the same trick on the **real** data, where the numbers are ugly and the lesson is louder. This is the real output of `dial.py`:

```text
t 0.12 -> 0.10   rise 0.071429  run 0.005071  rise/run = 14.0857
t 0.10 -> 0.08   rise 0.000000  run 0.007099  rise/run = 0.0000
t 0.02 -> 0.01   rise 0.214286  run 0.212982  rise/run = 1.0061
```

Three numbers, three completely different pieces of advice:

- **14.0857** — dropping from 0.12 to 0.10 buys fourteen units of recall per unit of false-alarm rate. **Take it.**
- **0.0000** — dropping from 0.10 to 0.08 buys nothing at all. **Don't.**
- **1.0061** — dropping from 0.02 to 0.01 buys about one unit of recall per unit of false alarm. **That is the coin's exchange rate.** Down there, the model has stopped helping; you are just flagging more rows.

> **🧑‍🏫 If a student asks** *"why is the first number 14 and not 2, like on the cards?"* — because the real denominators are 14 and 986, not 10 and 10. A single extra fraud caught moves the rise by `1 ÷ 14 = 0.0714`, while a single extra false alarm moves the run by only `1 ÷ 986 = 0.0010`. **The steepness of an ROC curve depends on how lopsided your classes are.** That is honest, it is important, and it is next week's problem.

**No calculus. No limits. No symbols.** Two subtractions and a division, on numbers the student read off their own graph paper. Keep it there. In Week 12 this exact idea gets applied to a curve that is *not* made of straight segments, the two points get pushed together until they almost touch, and *then* it gets its grown-up name. Do not use that name today.

### 8. The other curve, and the one honest reason to prefer it

> **Precision-recall curve** — the same sweep, plotted differently: precision up the side, recall along the bottom. One dot per threshold, again.

> **Average precision (AP)** — one number summarising the whole precision-recall curve, roughly "the average precision you get across all the recall levels".

Why bother with a second picture of the same sweep? Because of the denominator problem in §5. Here is the pair, drawn from the very same nine rows of the sweep table:

![Same nine thresholds, two very different pictures](../figures/fig-w10-4-roc-vs-pr-when-positives-are-rare.svg)
*Figure 10.4 — Same nine thresholds, two very different pictures. 211 false alarms slide the ROC across by 0.2140 and crush precision to 0.0231. Both charts are true; only one of them is going to be shouted at by the operations team.*

Look at what happens between the point marked 2 (threshold 0.10) and the point marked 3 (threshold 0.02):

```text
false alarms went from 5 to 211.

on the ROC:  the x-axis moved from 5 ÷ 986 = 0.0051  to  211 ÷ 986 = 0.2140
             — a fifth of the way across.  Looks survivable.

on the PR :  precision went from 3 ÷ 8 = 0.3750  to  5 ÷ 216 = 0.0231
             — it fell to about a sixteenth of what it was.  Looks like a disaster.
```

**It is a disaster, and the PR curve is the one telling the truth about the day's work.** 216 flagged transactions, 5 of them real. An analyst reviewing that queue looks at about forty-two innocent people for every thief.

And the two summary numbers, real output:

```text
roc_auc_score           0.6116   (a coin gets 0.5000)
average_precision_score 0.2078   (a coin gets 0.0140, the fraud rate)
```

Read those two lines together and you get the whole nuance of the week:

| | Our model | A coin gets | So how good is our model? |
|---|---|---|---|
| **ROC AUC** | 0.6116 | 0.5000 | a bit better than a coin — **unimpressive** |
| **Average precision** | 0.2078 | **0.0140** | about **fifteen times** better than a coin — **genuinely useful** |

**Both numbers describe the same model on the same 1,000 rows.** ROC AUC's baseline is always 0.5, no matter what the data looks like. Average precision's baseline is **the positive class rate** — 14 ÷ 1000 = 0.0140 — because a coin flagging at random gets a precision equal to the fraud rate at every threshold. So a bare AP of 0.21 sounds terrible and is in fact fifteen-fold better than nothing, while a bare AUC of 0.61 sounds mediocre and is.

> **⚠️ Watch out:** the rule of thumb *"use PR when positives are rare"* is true and it is not the whole story. **AP is not comparable between datasets** — change the fraud rate and the baseline moves, so an AP of 0.21 on 1.4% fraud cannot be ranked against an AP of 0.40 on 10% fraud by the raw numbers. (Even "times better than a coin" is not a fair cross-dataset score, because that ratio is capped by 1 ÷ the positive rate.) AUC *is* comparable between datasets, which is exactly why people keep reporting it. **The professional answer is to report both, with the class balance printed beside them.** That is what the student will write in their model card.

### 9. Every line of this week's code, explained to someone who has never programmed

```python
prob = model.predict_proba(X_val)[:, 1]
```
Ask the fitted model for its confidence on every validation row, and keep the fraud column. `prob` is now 1,000 decimals between 0 and 1.

```python
pred = (prob >= t).astype(int)
```
Compare all 1,000 at once to `t`; turn the `True`/`False` answers into 1s and 0s. Explained piece by piece in §2.

```python
tn, fp, fn, tp = confusion_matrix(y_val, pred, labels=[0, 1]).ravel()
```
Week 8's line, with **one new thing**: `labels=[0, 1]`. Without it, when the truth **and** the predictions each hold only one class (a small slice, a small fold, or a quiet day), scikit-learn hands back a 1×1 grid, and `ravel()` cannot fill four names — you get `ValueError: not enough values to unpack (expected 4, got 1)`. `labels=[0, 1]` says *"there are two classes even if one of them is empty today"*, and the crash goes away. **On our full validation set it does not crash even at `t = 0.50` (the truth still holds 14 frauds), so treat it as a habit that bites on slices and folds, not as something that will fire today.**

```python
precision_score(y_val, pred, zero_division=0)
```
`zero_division=0` says *"if you have to divide by zero, give me 0 and no warning"*. At `t = 0.50` nothing is flagged, so precision is `0 ÷ 0`, which has no answer. Without this argument you get an `UndefinedMetricWarning` — which is scikit-learn being honest, and worth showing once before you silence it.

```python
fpr, tpr, thr = roc_curve(y_val, prob)
```
Hands back **three** lists, all the same length: every false positive rate, every true positive rate, and the threshold that produced each pair. Note it takes `prob`, **not** `pred` — it does the whole sweep for you, so it needs the raw numbers.

```python
prec, rec, pthr = precision_recall_curve(y_val, prob)
```
The same shape of answer for the other curve, with **one trap**: `prec` and `rec` have one *more* entry than `pthr`. scikit-learn tacks on the point (recall 0, precision 1) at the end so the curve reaches the axis. Plot `rec` against `prec` and you are fine; plot `pthr` against `prec` and you get a shape error. It is in the Debugging Clinic.

```python
average_precision_score(y_val, prob)
```
One number for the whole PR curve. Also takes `prob`, not `pred`.

```python
plt.savefig("dial.png")
```
Write the picture to a file. **Never `plt.show()`** — on a headless machine it hangs, and we want the artifact on disk anyway.

### 10. The three misconceptions you will actually meet

**"A different threshold is a different model."** It is not. Say it as: *"the model wrote 1,000 numbers on 1,000 cards, once, and then went home. Everything we do today is deciding where to put the knife."* If they still do not have it, run the sweep twice and point out that `prob.min()` and `prob.max()` are identical every time.

**"Recall went up, so the model got better."** No — the model did not change. Ask: *"and what happened to precision?"* Every single row of the sweep table is a *trade*. There is no row where you got something for nothing.

**"The ROC curve is bad, so the model is bad."** Careful. Our AUC of 0.6116 is genuinely unimpressive, but the AP of 0.2078 against a baseline of 0.0140 says something useful is in there. **The model is a weak overall ranker whose very top is nonetheless worth reading (3 real frauds in its top 8), and the 0.5 is a bad *decider*.** Those are separable, and the whole point of a threshold is that you get to fix the second one yourself.

### 11. How deep to go, and where to stop

| Idea | Verdict |
|---|---|
| The steepness of the curve at **one** point (rather than between two) | **Week 12.** Today is two points and a division. If a student pushes the two points together and asks what happens, tell them they have just invented next month's maths and write their name on the board. |
| **Choosing** the threshold from what each error costs | **Week 11, next week.** Today you *defend* three thresholds with words. Next week the arithmetic picks one. Do not let today's last segment turn into a costing exercise. |
| How much to trust a number computed on 14 frauds | **Week 11.** And they should ask. |
| Calibration — "does 0.1774 mean a 17.74% chance?" | Name it, do not teach it. Honest answer: *"probably not, and there is a whole method for checking. Level 4."* |
| `class_weight="balanced"`, resampling, SMOTE | **Not in Level 3.** They are a different lever on the same problem, and one lever per week. |
| Multi-class ROC, `roc_auc_ovr` | **Not in this course.** |

---

### 12. 🧭 The Growing Map — where Week 10 sits

The student guide carries the same figure every week with one more piece filled in. **This week the gold
finally moves**, for the first time since Week 7, and that is worth pointing at.

![The Level 3 pipeline in Week 10: the threshold and cost tile of MEASURE IT opens on the threshold dial](../figures/fig-w10-0-where-this-fits.svg)

*Figure 10.0 — Week 10's version. The top tile of MEASURE IT is white and solid, three weeks of work
finished. The tile underneath it, threshold · cost, is gold. The ↻ on stage three is drawn grey because
the training loop stays closed until Week 12.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it, don't explain it.** Ask *"which box did we do today?"* They point at the new gold tile —
   *threshold · cost* — and somebody should notice that the box above it has turned white. Pointing is
   the exercise.
2. **Then the question that belongs to this week.** Read the tile's label out loud and stop halfway:
   *"the box is called 'threshold and cost'. We did the threshold today — nine of them. So what do you
   think the cost half is going to be?"* Take guesses and write them on the board unedited. Somebody
   will say money, and next week's price-list card — `a miss costs £500 · a false alarm costs £10` —
   makes them right in front of the class. This is the cheapest possible hook into Week 11.
3. **Then the sentence that connects the two tiles.** Point at the white tile above: *"up there we
   learned that 98.6% could be useless. Down here we learned that the same model, at a different
   threshold, is a completely different classifier. Same model. Nothing refitted."* That is what the
   0.1774 ceiling bought you today.

> **🧑‍🏫 Why this is worth two minutes.** A learner who can see the map can distinguish *"I don't
> understand this week"* from *"I don't know where this week goes"* — and those two need completely
> different help from you. Without the map, both arrive at your desk as "I don't get it."

**Two things to notice, so you can answer if asked.**

- **Evaluation is lit alone.** No new model was fitted this week; the dial was already in the box and we
  simply took it out. If a student objects that curves feel like model work, the honest reply is that
  the ROC curve is a picture of a **measurement procedure**, not of the model's insides.
- **The ↻ on stage three is still grey — but only for one more week.** It is the training loop, and the
  symbol turns black in Week 12. You can safely promise that now: *"two weeks from now we stop measuring
  models and start building the thing that learns."*

> **⚠️ Watch out:** the map is orientation, not assessment. Never quiz them on it. And do not let step 2
> slide into actually costing the thresholds — that is next week's 70 minutes and it needs all of them.

---

## 🧰 Prep Checklist

### 25 minutes the night before

- [ ] **Write the 20 index cards.** Ten minutes, and this is the highest-value ten minutes of your week. One card each. Write the **probability large on the front** and the **truth small on the back**:

| Probability (front) | Truth (back) | | Probability (front) | Truth (back) |
|---|---|---|---|---|
| 0.96 | FRAUD | | 0.55 | legit |
| 0.92 | FRAUD | | 0.48 | FRAUD |
| 0.88 | FRAUD | | 0.42 | legit |
| 0.84 | legit | | 0.36 | legit |
| 0.80 | FRAUD | | 0.30 | FRAUD |
| 0.76 | FRAUD | | 0.25 | legit |
| 0.72 | FRAUD | | 0.20 | legit |
| 0.68 | legit | | 0.15 | legit |
| 0.64 | FRAUD | | 0.10 | legit |
| 0.60 | FRAUD | | 0.05 | legit |

**Ten FRAUD, ten legit.** Count them twice. Then shuffle them — the class lays them out in order themselves, and that act is the first half of the activity.

- [ ] **Do the two rise-over-run divisions yourself, on paper.** Not in your head:

```text
0.40 − 0.20 = 0.20      0.10 − 0.00 = 0.10      0.20 ÷ 0.10 = 2.0
0.80 − 0.80 = 0.00      0.30 − 0.20 = 0.10      0.00 ÷ 0.10 = 0.0
```

**If you have not said "two frauds for every false alarm" out loud once, you will fumble the best line in the lesson.**

- [ ] **Type and run `dial.py` yourself.** The complete file:

```python
"""dial.py - 0.5 is a default, not a law.  Week 10."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (average_precision_score, confusion_matrix,
                             precision_recall_curve, precision_score,
                             recall_score, roc_auc_score, roc_curve)
from sklearn.model_selection import train_test_split

# ------------------------------------------------------------- 1. THE DATA
X, y = make_classification(n_samples=5000, n_features=8, n_informative=4,
                           n_redundant=0, weights=[0.99, 0.01], random_state=0)
X_tmp, X_test, y_tmp, y_test = train_test_split(
    X, y, test_size=0.20, random_state=0, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(
    X_tmp, y_tmp, test_size=0.25, random_state=0, stratify=y_tmp)
print("val rows %d   real frauds %d   real legit %d"
      % (len(y_val), y_val.sum(), len(y_val) - y_val.sum()))

# ---------------------------------------------------- 2. ONE FROZEN MODEL
model = LogisticRegression(max_iter=2000, random_state=0).fit(X_train, y_train)
prob = model.predict_proba(X_val)[:, 1]
print("lowest probability %.4f    highest probability %.4f"
      % (prob.min(), prob.max()))
print("how many are above 0.5?", int((prob >= 0.50).sum()))

# ---------------------------------------------------------- 3. THE SWEEP
print()
print("   t   flagged  tp  fp  fn   tn  precision  recall     fpr")
for t in [0.50, 0.15, 0.12, 0.10, 0.08, 0.06, 0.04, 0.02, 0.01]:
    pred = (prob >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_val, pred, labels=[0, 1]).ravel()
    print("%5.2f  %6d %3d %3d %3d %4d     %.4f  %.4f  %.6f"
          % (t, pred.sum(), tp, fp, fn, tn,
             precision_score(y_val, pred, zero_division=0),
             recall_score(y_val, pred, zero_division=0), fp / (fp + tn)))

# ------------------------------------------- 4. STEEPNESS: RISE OVER RUN
print()
pos = y_val.sum()
neg = len(y_val) - pos


def point(t):
    pred = (prob >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_val, pred, labels=[0, 1]).ravel()
    return tp / pos, fp / neg


for t1, t2 in [(0.12, 0.10), (0.10, 0.08), (0.02, 0.01)]:
    tpr1, fpr1 = point(t1)
    tpr2, fpr2 = point(t2)
    rise = tpr2 - tpr1
    run = fpr2 - fpr1
    print("t %.2f -> %.2f   rise %.6f  run %.6f  rise/run = %.4f"
          % (t1, t2, rise, run, rise / run))

# -------------------------------------------------------- 5. THE CURVES
print()
fpr, tpr, thr = roc_curve(y_val, prob)
prec, rec, pthr = precision_recall_curve(y_val, prob)
print("roc_curve              -> %d fprs, %d tprs, %d thresholds"
      % (len(fpr), len(tpr), len(thr)))
print("precision_recall_curve -> %d precisions, %d recalls, %d thresholds"
      % (len(prec), len(rec), len(pthr)))
print("roc_auc_score           %.4f   (a coin gets 0.5000)"
      % roc_auc_score(y_val, prob))
print("average_precision_score %.4f   (a coin gets %.4f, the fraud rate)"
      % (average_precision_score(y_val, prob), y_val.mean()))

# ------------------------------------------------------- 6. THE PICTURE
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
axes[0].plot(fpr, tpr, color="tab:blue")
axes[0].plot([0, 1], [0, 1], "--", color="grey")
for t in [0.12, 0.10, 0.02]:
    a, b = point(t)
    axes[0].scatter([b], [a], s=90, color="crimson", zorder=3)
axes[0].set_xlabel("false positive rate")
axes[0].set_ylabel("true positive rate (recall)")
axes[0].set_title("ROC - AUC %.4f" % roc_auc_score(y_val, prob))
axes[1].plot(rec, prec, color="tab:blue")
axes[1].plot([0, 1], [y_val.mean(), y_val.mean()], "--", color="grey")
axes[1].set_xlabel("recall")
axes[1].set_ylabel("precision")
axes[1].set_title("Precision-Recall - AP %.4f"
                  % average_precision_score(y_val, prob))
plt.tight_layout()
plt.savefig("dial.png")
print()
print("saved dial.png")
```

Run `python3 dial.py`. You must see **exactly** this:

```text
val rows 1000   real frauds 14   real legit 986
lowest probability 0.0001    highest probability 0.1774
how many are above 0.5? 0

   t   flagged  tp  fp  fn   tn  precision  recall     fpr
 0.50       0   0   0  14  986     0.0000  0.0000  0.000000
 0.15       1   1   0  13  986     1.0000  0.0714  0.000000
 0.12       2   2   0  12  986     1.0000  0.1429  0.000000
 0.10       8   3   5  11  981     0.3750  0.2143  0.005071
 0.08      15   3  12  11  974     0.2000  0.2143  0.012170
 0.06      25   3  22  11  964     0.1200  0.2143  0.022312
 0.04      65   4  61  10  925     0.0615  0.2857  0.061866
 0.02     216   5 211   9  775     0.0231  0.3571  0.213996
 0.01     429   8 421   6  565     0.0186  0.5714  0.426978

t 0.12 -> 0.10   rise 0.071429  run 0.005071  rise/run = 14.0857
t 0.10 -> 0.08   rise 0.000000  run 0.007099  rise/run = 0.0000
t 0.02 -> 0.01   rise 0.214286  run 0.212982  rise/run = 1.0061

roc_curve              -> 28 fprs, 28 tprs, 28 thresholds
precision_recall_curve -> 1001 precisions, 1001 recalls, 1000 thresholds
roc_auc_score           0.6116   (a coin gets 0.5000)
average_precision_score 0.2078   (a coin gets 0.0140, the fraud rate)

saved dial.png
```

**Expected runtime: under 2 seconds, including writing `dial.png`.** If `highest probability` is not `0.1774`, a `random_state=0` is missing somewhere — check both `train_test_split` calls and the `LogisticRegression`.

- [ ] **Open `dial.png` and look at it.** Two panels. The left one climbs raggedly above the diagonal; the right one falls off a cliff in the first inch. **You want to have seen the cliff before the class does.**

- [ ] **Break it on purpose, twice, so you have seen both live.**
  1. `fpr, tpr, thr = roc_curve(y_val, pred)` — probabilities replaced by hard predictions. **No error.** You get a curve with **3 points** instead of 28 and an AUC of 0.6046 instead of 0.6116. This is deliberate mistake two and it is the important one.
  2. `tn, fp, fn, tp = confusion_matrix(y_val, pred).ravel()` with `labels=[0, 1]` deleted, at `t = 0.50` on a tiny slice — `ValueError: not enough values to unpack (expected 4, got 1)`. Loud and instant.

- [ ] **Print the workbook** (`workbook/week-10.md`) **without its final ✅ Answers section**, which is for checking after the work is done. Add a second copy of the **🛠️ Build It** section's ten-threshold table (the hand sweep) if you want a clean sheet for the activity.
- [ ] **Tape a long strip of paper along a wall, or clear a whole whiteboard**, and draw one horizontal line on it with `0` at the left end, `0.5` in the middle and `1` at the right end. That is the probability line and the cards will go on it.
- [ ] **One sheet of squared graph paper per student, plus one big sheet taped up next to the probability line.** Draw the axes on the big one in advance: false positive rate 0 to 1 along the bottom, true positive rate 0 to 1 up the side, in tenths. **Ten squares each way, so one square is 0.1 and one card is one square.**
- [ ] **Check Week 8's 2×2 is still on the wall.** You will point at it in the first minute.

### 5 minutes on the day

- [ ] Terminal in the working folder. **`dial.py` deleted or renamed** — they type it.
- [ ] The 20 cards **shuffled**, face up, in a pile.
- [ ] The probability line on the wall, blank.
- [ ] The big graph-paper axes taped up, blank.
- [ ] Three sticky notes in your pocket for the three defended thresholds.
- [ ] Workbook out, open at **🛠️ Build It** (the hand-sweep table). Nothing filled in.
- [ ] Bug Log open at a fresh page.

### Fallback if the laptops fail

**This is the most laptop-proof lesson of the term. All four objectives survive with no computer at all**, because the twenty cards *are* the dataset.

1. **Lay out the cards on the probability line.** Objective 1's raw material, and better on paper than on a screen.
2. **Sweep the threshold from 0.90 down to 0.05 by hand**, ten stops, recomputing the four counts each time. The full table is in the Answer Key under **🛠️ Build It** (and again under Practice Set B, B4). **Objective 1, complete.**
3. **Plot each stop on the big graph paper.** Ten dots, joined up. That is objective 3's ROC curve and it is the same curve `roc_curve` would draw.
4. **The two rise-over-run divisions, from their own dots.** Objective 2 is pure arithmetic and needs nothing but a pencil.
5. **The three sticky notes.** Objective 4 is a writing task.

| If this fails | Do this instead |
|---|---|
| `highest probability` is not `0.1774` | A `random_state=0` is missing. Check the two splits first, then the model. |
| `ValueError: not enough values to unpack (expected 4, got 1)` | `labels=[0, 1]` is missing from `confusion_matrix`. **Expected — teach it there and then.** |
| `UndefinedMetricWarning: Precision is ill-defined...` at `t = 0.50` | Nothing flagged, so precision is 0 ÷ 0. Add `zero_division=0`. **A warning, not an error — read it out loud.** |
| The AUC comes out 0.6046 and nobody knows why | `roc_curve` or `roc_auc_score` was handed `pred` instead of `prob`. **Deliberate mistake two arriving early, which is fine.** |
| The class cannot agree on the card order | Sort by the probability on the front, largest at the right-hand end. Truth stays face-down until the cut is made. |
| Somebody has done ROC curves before | Send them to the "flying" path: compute the area under their own ten-dot curve by counting squares, and compare it with 0.85. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — The Model That Flags Nothing | 7 | 7 | 0.1774, and 0 out of 1,000 |
| 🧠 Concept & Maths — Rise Over Run | 18 | 25 | Cards on the line, the sweep, the two divisions |
| 💻 Live-Code Together — `dial.py` | 18 | 43 | The sweep, then both curves. **Two deliberate mistakes.** |
| 🎲 Their Turn — The Dial, Physically | 20 | 63 | Three roles, ten thresholds, one curve on the wall |
| 🔑 Wrap & Assign | 7 | 70 | Three checks, three sticky notes, homework |

---

### 🪝 Hook — The Model That Flags Nothing (7 minutes)

**Do this:** Point at Week 8's 2×2 still on the wall. Say nothing about it yet. Then open a terminal and type only these lines, on the shared screen, while they watch:

```python
prob = model.predict_proba(X_val)[:, 1]
print("lowest  %.4f    highest  %.4f" % (prob.min(), prob.max()))
print("above 0.5:", int((prob >= 0.5).sum()))
```

Real output:

```text
lowest  0.0001    highest  0.1774
above 0.5: 0
```

**Say this:**

> "That last number is zero.
>
> Here is what those two lines did. Our fraud model looked at all thousand validation transactions and gave each one a score between 0 and 1 — how suspicious it thinks that transaction is. The lowest score it gave anything was **0.0001**. The highest score it gave anything — the single most suspicious transaction in the file, the one it is most certain about — was **0.1774**.
>
> And then I asked: how many of those thousand scores are above **0.5**?
>
> **None.** Not one."

**Ask this:** "So how many frauds does this model catch?"

*Hoped-for answer:* none.

*If they say "three" (remembering Week 8):* that was the decision tree. This is the logistic regression that has been in their pipeline since Week 3, and it catches zero.

> "Zero. It flags nothing at all. It is also **98.6% accurate**, because it says 'legit' to everything and 986 of them are legit. We met that trick in Week 8 and we have a name for it.
>
> Now. **Whose fault is that?**"

Let them argue for thirty seconds. Someone will say the model is rubbish.

**Do this:** Write on the board, big:

```text
      predict()   =   predict_proba()   then   >=  0.5
                                               ^^^^^^^
                                       who chose this number?
```

**Say this:**

> "Nobody chose it. It is a default. It came in the box with the library. Some very sensible person twenty years ago wrote 0.5 because if you have no other information, half is the least stupid place to cut — and that number has been making decisions on your behalf for nine weeks and you have never been asked about it.
>
> Today you get the dial. **Nothing about the model is going to change today.** The thousand scores stay exactly as they are. All we are going to change is the number we compare them to — and by the end of the lesson you will have caught eight of the fourteen frauds with the same model that currently catches none, and you will be able to say exactly what that cost."

---

### 🧠 Concept & Maths — Rise Over Run (18 minutes)

**Step 1 (4 min) — lay out the cards.**

**Do this:** Hand the shuffled pile of 20 cards to two students. Point at the probability line on the wall.

> "Twenty transactions. Each card has the model's score on the front. Put them on the line where they belong — 0.05 goes near the left end, 0.96 goes near the right end. **Do not turn any of them over.**"

They will do this in about two minutes and it is worth every second, because the physical act of ranking is the thing they need in their hands.

**Ask this:** "What does the model actually know, looking at this line?"

*Hoped-for answer:* which ones are more suspicious than which.

> "It knows the **order**. That is the thing it learned. It does not know where to cut."

**Step 2 (6 min) — the sweep, on the wall.**

**Do this:** Stand at 0.90 on the line and hold your arm up like a barrier.

> "I am the threshold. I am standing at 0.90. **Everything to my right is flagged as fraud. Everything to my left is let through.** How many cards are to my right?"

*Two.* Turn those two over. Both say FRAUD.

**Do this:** Write the first row of the table on the board, and say every division out loud as you write it:

```text
t = 0.90    flagged 2    caught 2 of 10    false alarms 0

            recall     =  2 ÷ 10  =  0.20
            precision  =  2 ÷  2  =  1.00
```

**Say this:**

> "Perfect precision. Everything I flagged was fraud. And I have caught **two out of ten.** Eight frauds are walking out of the building behind me.
>
> So I move."

**Do this:** Walk to 0.80. Then 0.70. Then 0.60. At each stop, count the cards to your right, turn over any new ones, and add a row. **Have a student write the rows; you hold the arm out.** Get to 0.60 and stop.

```text
t = 0.80    flagged  5   caught 4    false alarms 1   precision 4 ÷  5 = 0.80   recall 0.40
t = 0.70    flagged  7   caught 6    false alarms 1   precision 6 ÷  7 = 0.86   recall 0.60
t = 0.60    flagged 10   caught 8    false alarms 2   precision 8 ÷ 10 = 0.80   recall 0.80
```

**Ask this:** "Between 0.90 and 0.60, one column only ever went up and one column went up and down. Which is which?"

*Hoped-for answer:* recall only goes up; precision wobbles.

> "**Recall can never go down when you lower the threshold**, and there is a reason you can say in one sentence: lowering the bar only ever *adds* cards to the flagged pile. A fraud you have already caught cannot escape. Precision has no such promise, because every card you add might be innocent."

**Step 3 (5 min) — 🔢 the new maths: rise over run.**

**Do this:** Now put those first four stops on the big graph paper. Two students, one dot each. Across is false alarms ÷ 10; up is caught ÷ 10.

```text
t = 0.90  ->  ( 0.00 , 0.20 )
t = 0.80  ->  ( 0.10 , 0.40 )
t = 0.70  ->  ( 0.10 , 0.60 )
t = 0.60  ->  ( 0.20 , 0.80 )
```

**Say this:**

> "Look at the first two dots. Going from the first to the second, **how far up did we go, and how far across?**"

**Do this:** Draw the two dashed legs on the graph paper — one horizontal, one vertical — and label them as the class calls the numbers out.

```text
rise  =  0.40 − 0.20  =  0.20        we went UP by 0.20
run   =  0.10 − 0.00  =  0.10        we went ACROSS by 0.10
```

**Ask this:** "So how steep is that? Rise over run."

*Hoped-for answer:* 0.20 ÷ 0.10 = 2.

> "**Two.** And here is the sentence I want you to be able to say for the rest of your life:
>
> **For every one unit of false alarms I spent, I bought two units of recall.**
>
> That is a bargain. You can hear that it is a bargain."

**Do this:** Now the flat pair. Point at the dots for `t = 0.60` (0.20, 0.80) and the next one you have not drawn yet — `t = 0.50`, which is (0.30, 0.80). Draw it.

```text
rise  =  0.80 − 0.80  =  0.00
run   =  0.30 − 0.20  =  0.10

steepness  =  0.00 ÷ 0.10  =  0.0
```

**Ask this — this is the most important question of the segment:** "What did we just buy?"

*Hoped-for answer:* nothing.

*If nobody answers:* put your finger on the extra false-alarm card and say *"this is a real person. What did blocking their card get us?"*

> "**Nothing. Zero.** One more innocent customer had their card blocked and we caught not one extra fraud. A steepness of 0 means pure cost.
>
> So the shape of this curve is not decoration. **The steep bits are where recall is cheap, and the flat bits are where you are burning people for nothing.** That is what an ROC curve is *for*."

> **📌 The finished graph paper is drawn for you in Figure 10.3 above** — both dashed legs, both divisions written out beside them. Have that page open while you draw, and copy it.

**Step 4 (3 min) — name the three things.**

**Do this:** Blockquote each of these on the board, in this order, and leave them up all lesson.

> **Decision threshold** — the probability above which you call something positive. 0.5 is a default, not a law.

> **True positive rate** — of all the things that really were positive, the fraction you caught. This is recall with a second name.

> **False positive rate** — of all the things that really were negative, the fraction you wrongly flagged. `FP ÷ (FP + TN)`.

> **ROC curve** — the picture you get by plotting true positive rate against false positive rate, one dot per threshold. **One model. Many dots.**

**Ask this:** "Recall's denominator is 10, the ten real frauds. What is false positive rate's denominator here?"

*Hoped-for answer:* 10, the ten real legits.

> "Ten today, because I gave you a tidy pile. On the real data it is **986.** Remember that number; in twelve minutes it is going to do something dramatic."

---

### 💻 Live-Code Together — `dial.py` (18 minutes)

**You never touch their keyboard.** They type; you type the same thing on the shared screen.

**Step 1 (5 min) — the sweep.**

New file, `dial.py`. Everything down to the end of the sweep loop. (Full text in the Prep Checklist.)

**Ask before running:** "The first row is `t = 0.50`. What will be in the `flagged` column?"

*Hoped-for answer:* zero.

Run it. Real output:

```text
val rows 1000   real frauds 14   real legit 986
lowest probability 0.0001    highest probability 0.1774
how many are above 0.5? 0

   t   flagged  tp  fp  fn   tn  precision  recall     fpr
 0.50       0   0   0  14  986     0.0000  0.0000  0.000000
 0.15       1   1   0  13  986     1.0000  0.0714  0.000000
 0.12       2   2   0  12  986     1.0000  0.1429  0.000000
 0.10       8   3   5  11  981     0.3750  0.2143  0.005071
 0.08      15   3  12  11  974     0.2000  0.2143  0.012170
 0.06      25   3  22  11  964     0.1200  0.2143  0.022312
 0.04      65   4  61  10  925     0.0615  0.2857  0.061866
 0.02     216   5 211   9  775     0.0231  0.3571  0.213996
 0.01     429   8 421   6  565     0.0186  0.5714  0.426978
```

> **Say this:** "Nine rows. **One model.** The thousand probabilities never changed once. Every difference on this screen came from changing one number in a comparison.
>
> Bottom row: threshold 0.01, and we catch **eight of the fourteen frauds** — with the model that caught zero at the start of the lesson. It cost us **421 false alarms.** Four hundred and twenty-one phone calls."

**Ask this:** "Put your finger on the `tp` column, rows four, five and six. What is it doing?"

*Hoped-for answer:* nothing — it stays at 3.

> **Say this:** "It stays at three. And in those same three rows the false alarms go 5, then 12, then 22. **We lowered the bar twice, added seventeen innocent people to the pile, and caught not a single extra fraud.** Seventeen people, nothing gained.
>
> That is a flat bit of the curve. You measured one of those on graph paper twenty minutes ago and got a steepness of zero. **Same thing, real data.**"

**Do this:** Get them to add up one row out loud. `t = 0.02`: 5 + 211 + 9 + 775.

**Ask this:** "What should that come to?"

*Hoped-for answer:* 1,000. It does. Make this a reflex.

**Step 2 (4 min) — 🐞 DELIBERATE MISTAKE ONE: the empty confusion matrix.**

> **Say this:** "That `labels=[0, 1]` in the middle of the confusion matrix line looks like clutter. Let's take it out and see if it matters."

Delete `, labels=[0, 1]` and run. On the full validation set it survives, so shrink the problem to force it — type this in a fresh file or at the prompt:

```python
import numpy as np
from sklearn.metrics import confusion_matrix
truth = np.array([0, 0, 0, 0, 0])
pred = np.array([0, 0, 0, 0, 0])
tn, fp, fn, tp = confusion_matrix(truth, pred).ravel()
```

Real output:

```text
/…/sklearn/metrics/_classification.py:534: UserWarning: A single label was found in 'y_true' and 'y_pred'. For the confusion matrix to have the correct shape, use the 'labels' parameter to pass all known labels.
  warnings.warn(
Traceback (most recent call last):
  File "…", line 5, in <module>
    tn, fp, fn, tp = confusion_matrix(truth, pred).ravel()
ValueError: not enough values to unpack (expected 4, got 1)
```

**Ask this:** "Read me the last line. And then read me the warning above it."

*Hoped-for answer:* it wanted four things and only got one; and the warning tells you to use `labels`.

> **Say this:** "**The fix is written in the warning.** 'Use the labels parameter to pass all known labels.' scikit-learn saw nothing but zeros, concluded there was only one class in the world, and built a one-by-one table. One number cannot fill four names.
>
> This bites on small slices and folds, where the truth is single-class too (on our full validation set it survives, as above). That is why the line says `labels=[0, 1]` — it means *'there are two classes even if one of them is empty today.'*"

Put it back. **Bug Log entry, sixty seconds.**

**Step 3 (6 min) — the two curves, and 🐞 DELIBERATE MISTAKE TWO.**

> **Say this:** "Nine rows is nine dots. scikit-learn will do every possible threshold for us."

Type the curve section, but **deliberately hand it the predictions instead of the probabilities**:

```python
pred = (prob >= 0.10).astype(int)
fpr, tpr, thr = roc_curve(y_val, pred)
print("points on the curve :", len(fpr))
print("thresholds it found :", thr)
print("AUC %.4f" % roc_auc_score(y_val, pred))
```

Real output:

```text
points on the curve : 3
thresholds it found : [inf  1.  0.]
AUC 0.6046
```

**Do this:** Say nothing. Let it sit.

**Ask this:** "Was that an error?"

*Answer:* no.

**Ask this:** "Three points. How many thresholds did it find?"

*Hoped-for answer:* two useful ones — 1 and 0.

> **Say this:** "**No error, no warning, and a completely useless curve.** I handed `roc_curve` a column of 0s and 1s. There are only two different values in it, so there are only two places to cut, so there are three points on the curve. And it still printed an AUC — **0.6046** — which is a plausible-looking number that is wrong.
>
> `roc_curve` needs the **probabilities**, because its whole job is to try every threshold. Hard predictions have already had the threshold applied and thrown the confidence away. **You cannot un-decide a decision.**"

Fix it live:

```python
fpr, tpr, thr = roc_curve(y_val, prob)
prec, rec, pthr = precision_recall_curve(y_val, prob)
print("roc_curve              -> %d fprs, %d tprs, %d thresholds"
      % (len(fpr), len(tpr), len(thr)))
print("precision_recall_curve -> %d precisions, %d recalls, %d thresholds"
      % (len(prec), len(rec), len(pthr)))
print("roc_auc_score           %.4f   (a coin gets 0.5000)"
      % roc_auc_score(y_val, prob))
print("average_precision_score %.4f   (a coin gets %.4f, the fraud rate)"
      % (average_precision_score(y_val, prob), y_val.mean()))
```

```text
roc_curve              -> 28 fprs, 28 tprs, 28 thresholds
precision_recall_curve -> 1001 precisions, 1001 recalls, 1000 thresholds
roc_auc_score           0.6116   (a coin gets 0.5000)
average_precision_score 0.2078   (a coin gets 0.0140, the fraud rate)
```

> **Say this:** "Twenty-eight points now, not three. And two summary numbers.
>
> **0.6116 against a coin's 0.5000.** Unimpressive. Barely better than guessing.
>
> **0.2078 against a coin's 0.0140.** Fifteen times better than guessing.
>
> Same model, same 1,000 rows. **The two scores disagree about whether this model is any good, and they are both right**, because they are measured against two different backgrounds. Notice the second baseline: 0.0140. Where have you seen that number today?"

*Answer:* it is the fraud rate — 14 ÷ 1000.

**Bug Log. This is the most valuable entry of the week** — a wrong answer, no error message, and a plausible size. Make sure the words *"AUC needs the probabilities, not the predictions"* are in it.

**Step 4 (3 min) — the picture.**

Type the plotting block and run the whole file.

```text
saved dial.png
```

**Do this:** Open `dial.png` on the shared screen.

> **📌 What is on the screen is Figure 10.4 above**, with the arithmetic printed underneath it. If your `dial.png` does not look like that — in particular if the right-hand curve does not fall off a cliff in the first fifth — check the Debugging Clinic.

**Ask this:** "Between the second marked dot and the third, false alarms went from 5 to 211. Which chart cares?"

*Hoped-for answer:* the right-hand one.

> **Say this:** "The ROC barely twitches, because 211 out of 986 innocent rows is `211 ÷ 986 = 0.2140`, a fifth of the way across a wide chart. The precision-recall curve falls off a cliff, because precision is `5 ÷ 216 = 0.0231`.
>
> **Which one is the operations team going to shout at you about?** The 216-row queue with five real frauds in it. So when positives are rare, **trust the curve whose denominator is the pile you actually have to look at.**"

---

### 🎲 Their Turn — The Dial, Physically (20 minutes)

Full instructions in **🎲 The Activity, In Full** below. In outline: three named roles, ten thresholds called out loud from 0.90 down to 0.05, the 2×2 recomputed on the cards each time, one dot plotted on the wall each time, and the curve appearing in front of everybody. **You hold the clock and refuse to do the arithmetic.**

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Stand between the two artifacts — the probability line with its twenty cards, and the graph paper with its ten dots.

**Say this:**

> "An hour ago this model caught zero frauds out of fourteen and was 98.6% accurate. It has not been retrained. Nobody has touched a single weight. And you can now make it catch eight of the fourteen, or two of the fourteen, and you can say precisely what each of those costs in blocked cards.
>
> Every dot on that wall is the same model. **The dial was always there. Nobody had shown you where it was.**"

**Do this:** Hand out the three sticky notes and ask for three thresholds, each with a name on it.

> "Three thresholds. On each sticky note: the number, and **who you are defending it to.** Not 'it's the best' — *who is it right for.*"

Take whatever they give you, and if it is thin, prompt with these three (they are the three highlighted rows in Figure 10.5 below):

```text
t = 0.12   for the fraud team's two-person review desk:
           2 cases a day, both of them real.  Nothing wasted.

t = 0.10   for the manager who has to justify the queue:
           8 flagged, 3 real.  A third of the pile is worth looking at.

t = 0.02   for the customer whose money is actually gone:
           5 of 14 frauds caught instead of 3.  I do not care about the queue.
```

![The board at the end of the sweep](../figures/fig-w10-5-board-the-nine-row-sweep.svg)
*Figure 10.5 — The board at the end of the sweep. This is what should be written up when the lesson ends, with three rows highlighted and a person's name beside each.*

**Do this:** Three quick checks — exact wording in **✅ Assessing Understanding**.

**Say this, to close:**

> "One thing to notice before you go, and it is next week's door.
>
> All three of those sticky notes are **arguments**. Good arguments. And an argument is what you have when you do not have a price.
>
> Next week somebody from the bank walks in and tells you a number: **a missed fraud costs five hundred pounds and a false alarm costs ten.** The moment that sentence exists, the argument is over — because you can multiply. You will compute the total cost of every one of the nine rows on that board, and the cheapest row wins, and nobody gets to have an opinion about it."

**Do this:** Hand out the homework and read the last part out loud, slowly.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `ValueError: not enough values to unpack (expected 4, got 1)`, after a `UserWarning: A single label was found in 'y_true' and 'y_pred'` | "Your predictions only contain one class, so I built a 1×1 table, and one number cannot fill four names." | Truth **and** predictions each hold a single class (a tiny slice, nothing flagged), and `labels=[0, 1]` is missing from `confusion_matrix`. | `confusion_matrix(y_val, pred, labels=[0, 1]).ravel()`. **The fix is spelled out in the warning above the traceback.** |
| `ValueError: continuous format is not supported` | "The first thing you gave me is full of decimals, and the first thing has to be the truth." | Arguments swapped: `roc_curve(prob, y_val)`. | `roc_curve(y_val, prob)`. **Truth first, always.** |
| `ValueError: too many values to unpack (expected 2)` | "I hand back three things and you asked for two." | `fpr, tpr = roc_curve(y_val, prob)`. | Three names: `fpr, tpr, thr = ...`. `roc_curve` always returns the thresholds too. |
| `ValueError: x and y must have same first dimension, but have shapes (1000,) and (1001,)` | "Those two lists are different lengths." | Plotting `pthr` against `prec` from `precision_recall_curve`. The precisions and recalls have **one more entry** than the thresholds. | Plot `rec` against `prec`. If you really want precision against threshold, use `prec[:-1]`. |
| `ValueError: Classification metrics can't handle a mix of binary and multilabel-indicator targets` | "One of those is a column and the other is a two-column grid." | `[:, 1]` left off: `pred = (model.predict_proba(X_val) >= 0.10).astype(int)`. | `prob = model.predict_proba(X_val)[:, 1]` **first**, then threshold `prob`. |
| `UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 due to no predicted samples.` | "Nothing was flagged, so precision is 0 ÷ 0, which has no answer. I gave you 0." | A threshold above `prob.max()` — for us, anything above 0.1774. | `precision_score(y, pred, zero_division=0)` to silence it on purpose. **It is a warning, not an error. Read it before you silence it.** |
| **No error. `roc_curve` returns 3 points and the AUC is 0.6046 instead of 0.6116.** | Nothing crashed. You threw the confidence away before measuring it. | `roc_curve(y_val, pred)` — hard 0/1 predictions where probabilities were wanted. | `roc_curve(y_val, prob)`. **The curve needs every threshold, so it needs the raw numbers.** |
| **No error. `average_precision_score` returns 0.0914 instead of 0.2078.** | Same disease, second victim. | `average_precision_score(y_val, pred)`. | Pass `prob`. **Rule: if a metric draws a curve, it takes probabilities. If it counts cells, it takes predictions.** |
| **No error. `flagged` and `pred.sum()` disagree with each other.** | You counted `True`s in one place and `1`s in another. | `.astype(int)` left off in one of the two places. `(prob >= t)` is a list of `True`/`False`; it still adds up correctly, but it prints as `[False True …]` and confuses everybody. | Put `.astype(int)` on. **`(a >= 0.5).sum()` does work on booleans — which is exactly why this bug hides.** |
| **No error. Recall goes DOWN when the threshold drops.** | Impossible. Something is wrong with the bookkeeping. | The threshold list is not in the order you think, or `tp` and `fp` are swapped in the `ravel()` unpacking. | The order is `tn, fp, fn, tp` — alphabetical it is not. **Recall can never fall as the threshold falls. If it does, you have a bug, not a discovery.** |
| **No error. The four counts add to 999.** | A row went missing. | A `.sum()` on a boolean where an `int` was needed, or a row dropped by a stray filter. | **Add the four cells up before you divide anything.** Five seconds, catches everything. |

### How to teach debugging without giving the answer

All the old moves stand. This week adds two.

19. **"Does that metric draw a curve, or count cells?"** Curve-drawers (`roc_curve`, `precision_recall_curve`, `roc_auc_score`, `average_precision_score`) take **probabilities**. Cell-counters (`confusion_matrix`, `precision_score`, `recall_score`, `f1_score`) take **predictions**. **Only one of those two mistakes produces an error message**, which is why the question has to be asked out loud.

20. **"Read the warning above the traceback."** This week's headline error has its own fix printed one line above it, and a student who has learned to start reading at the last line will scroll straight past it. Get them into the habit of reading *the whole thing* once.

And the sentence for this week:

> **"A metric that gives you a plausible number from the wrong kind of input is more dangerous than one that crashes. Say out loud what you are handing it."**

---

## 🎲 The Activity, In Full

This section is the full set-up and running order for the physical activity, with an easier and a harder variation.

### The Dial, Physically

**What it is.** The class becomes the algorithm. One student is the **Caller**, one is the **Counter**, one is the **Plotter**. The Caller reads thresholds from 0.90 down to 0.05. The Counter recomputes the four counts on the twenty index cards. The Plotter puts one dot on the big graph paper. **Ten rounds, and an ROC curve appears on the wall without a computer being involved at all.**

**Why the three roles matter.** The point is not the curve — the students could copy that off a screen. The point is that **one person has to physically move the boundary, another has to notice that the counts changed, and a third has to notice that the dot moved.** That separation is the mental model. A student who has been the Counter for ten rounds will never again think that a threshold change is a model change.

> **📌 The setup is Figure 10.1 above** — twenty cards on the probability line, and three of the ten places the knife can go. That is exactly what the wall should look like when this activity starts.

### Setup

- **The 20 index cards**, already laid out on the probability line from the Concept segment. Probabilities up, truths already turned over from the first four rounds — that is fine, leave them.
- **The big graph paper**, axes already drawn: false positive rate 0→1 across, true positive rate 0→1 up, in tenths. **Ten squares each way, so one card is exactly one square.**
- **A visible tally area** on the board with four boxes labelled `caught (TP)`, `false alarms (FP)`, `missed (FN)`, `correctly let through (TN)`.
- **One student per role.** With more than three students, add a **Checker** whose only job is to add the four counts and confirm they make 20, and rotate all four roles every three rounds.

### How it runs (20 minutes)

**Minute 0–2 — assign roles and read the rules out loud.**

> "Three jobs.
>
> **Caller**: you say the threshold. Loudly. Then you say 'everything at or above this is flagged'.
>
> **Counter**: you count the cards to the right of the Caller's number, turn over any that are still face-down, and fill in the four boxes. **You must say the two divisions out loud** — 'caught four of ten, so recall is four over ten, nought point four'.
>
> **Plotter**: you take false alarms divided by ten, and caught divided by ten, and put a dot on the graph paper. Then you write the threshold beside it, small."

**Minute 2–14 — ten rounds, roughly 70 seconds each.**

The Caller works down this list. **Do not skip any of them, and do not let them go out of order** — the curve is only legible if the dots arrive in sequence.

```text
0.90   0.80   0.70   0.60   0.50   0.40   0.30   0.20   0.10   0.05
```

The first four rounds are already on the board from the Concept segment; re-plot them so the Plotter gets the practice, then carry on. **Your job for these twelve minutes is to say nothing except "keep going" and "add them up".** If the Counter gets a number wrong, the Checker catches it; if there is no Checker, wait, and let the room notice.

**Minute 14–18 — join the dots and read the shape.**

**Do this:** Ask the Plotter to join the ten dots with a ruler, left to right.

**Ask this:** "Where is this curve steep, and where is it flat?"

*Hoped-for answer:* steep at the start, flat at the end.

**Ask this:** "Pick the two dots with the steepest bit between them and do the division."

They will pick `t = 0.90 → 0.80`: `0.20 ÷ 0.10 = 2.0`. Have them write it on the paper beside the segment.

**Ask this:** "Now pick the flattest bit."

Anything from `t = 0.30` to `t = 0.05`: rise 0.00, run 0.50, **steepness 0.0**. That is five innocent people blocked to catch zero extra frauds.

**Minute 18–20 — the diagonal.**

**Do this:** Draw the dashed diagonal from corner to corner. Ask what a model that flags cards at random would look like.

*Hoped-for answer:* it would sit on the diagonal.

> "If your ranking is worthless, then whatever fraction of the innocents you flag, you will flag the same fraction of the frauds. **The gap between your curve and that diagonal is the only thing your model actually contributed.**"

### What "finished" looks like

- Ten dots on the wall, in order, joined, each labelled with its threshold.
- A dashed diagonal.
- **Two divisions written on the paper**, one steep and one flat, each with the rise and the run named.
- The four tally boxes on the board holding the last round's counts, adding to 20.

### Variation — easier

**Cut to five thresholds: 0.90, 0.70, 0.50, 0.30, 0.05.** Five dots still make a curve, and every division stays in clean tenths. Also: give the Counter a pre-printed table with the `flagged` column already filled in, so their only job is turning cards over and counting the frauds among them. **Objectives 1 and 2 survive completely intact.**

### Variation — harder

Three extensions, in order of ambition:

1. **Count the squares.** The area under their ten-dot curve, counted in graph-paper squares and divided by 100. Compare with `roc_auc_score(truth, prob)`, which is **0.8500**. Counting squares gets you to about 0.85 if you are careful, and it is next week's maths arriving a week early on purpose.
2. **Draw the other curve.** Same ten rounds, but plot **precision** up the side against recall across. The dots are (0.20, 1.000), (0.40, 0.800), (0.60, 0.857), (0.80, 0.800), (0.80, 0.727), (0.90, 0.692), (1.00, 0.667), (1.00, 0.588), (1.00, 0.526), (1.00, 0.500). **Ask why this one goes down when the other one went up.**
3. **Break the model.** Swap two cards — put a FRAUD at 0.05 and a legit at 0.96 — and re-run three rounds. The curve sags towards the diagonal. **Ask: did the model get worse, or the data?** (The model, in the sense that its ranking is now wrong. This is what a bad ranker looks like, and it is worth seeing.)

---

## ❓ Questions Students Ask This Week

These are the questions this lesson tends to raise, each with an answer you can give in your own words.

**"If 0.5 is just a default, why does anybody use it?"**
Because when you genuinely have no idea what the two errors cost, and the classes are roughly balanced, 0.5 is the least stupid guess — it is where the model's own probability says the two outcomes are equally likely. It is a *reasonable* default. What it is not is a *decision*, and on 1%-fraud data it is a catastrophic one. **The honest position: 0.5 is fine as a placeholder and indefensible as a final answer.**

**"So what IS the right threshold?"**
Today, honestly: it depends on who you are defending it to, and you have three sticky notes on the board proving that different people want different answers. **Next week it stops being an opinion**, because a price list turns it into arithmetic. Do not let this question get answered early — the frustration is the setup for Week 11.

**"Why does recall have two names?"**
Historical accident. **True positive rate** comes from radar operators in the Second World War, deciding whether a blip was an aeroplane or a goose; that is also where "receiver operating characteristic" comes from, which is the most unhelpful name in the whole of machine learning. **Recall** comes from information retrieval — "how many of the relevant documents did the search engine recall?" Two fields, same fraction, both names stuck. You will meet both.

**"Our AUC is 0.6116. Is that good?"**
No, and yes. As a *ranker* it is weak — a coin gets 0.5. But look at the average precision: 0.2078 against a coin's 0.0140, which is fifteen-fold. **Those two verdicts are both correct**, because AUC asks "does it rank well overall" and average precision asks "if I use this thing, will my queue be worth looking at". Report both, always, with the class balance printed beside them.

**"Could we get the top-left corner — all the frauds and no false alarms?"**
Only if the two piles do not overlap at all: every fraud scoring above every legitimate row. Look at the probability line on the wall — the card at 0.84 is legit and the card at 0.80 is fraud. **They overlap, so the corner is unreachable, and no threshold can fix that.** Fixing overlap means a better model or better features, which is Weeks 5 to 7, not today.

**"Does a probability of 0.1774 mean a 17.74% chance?"**
🤔 **Nobody fully agrees, and here is why.** For it to mean that, you would want: of all the transactions the model scores near 0.1774, about 17.74% turn out to be fraud. A model whose probabilities pass that test is called **calibrated**, and there is a whole literature on measuring and repairing it. Some people say an uncalibrated probability is not a probability at all and should be called a score. Others point out that if you only ever use it for *ranking* and then pick a threshold empirically — exactly what we did today — calibration is irrelevant, because the ranking is unchanged by any relabelling that keeps the order. **Both camps are right about different uses.** And it matters next week: the cost formula gives the "right" threshold *only* if the probabilities are honest, and ours are not, and we will watch the theory and the measurement disagree. That is not a failure; it is a diagnosis.

**"Why did the false positive rate only move by 0.001 when we blocked a card?"**
Because its denominator is 986. Precision's denominator was 8. **Same mistake, two backgrounds, two completely different-sized reactions.** This is the single sentence that explains why ROC and PR disagree, and if a student asks it unprompted, stop and let them explain it to the room.

**"Can I just pick the threshold that makes my numbers look best?"**
You can, and people do, and it is called *cherry-picking the operating point*. The defence is one line in your model card: **"threshold 0.10, chosen on the validation set, for this stated reason."** Naming the threshold and where you chose it is the entire ethical difference between tuning and lying.

---

## ⚠️ Where This Lesson Goes Wrong

This table lists the usual ways the lesson slips and what to do right now when it does.

| What happens | Why | What to do right now |
|---|---|---|
| **You apologise for the model flagging nothing at 0.5.** | It feels like a broken demo. It is the opposite — it is the proof. | Do not fix it. Say *"good: the default is useless here, and that is the lesson."* If you have already apologised, recover with `(prob >= 0.10).sum()` and the three frauds it catches. |
| Students think each dot on the ROC curve is a different model. | Nothing in the picture says otherwise, and "curve" implies "many things". | Go back to the wall. **Point at the twenty cards and say "these numbers have not moved once."** Then move your arm and watch the dot move. Physical, and it lands. |
| The class runs out of time before the ten rounds finish. | The Concept segment is dense and the cards are fun. | **Use the easier variation (five thresholds) from the start if you are behind at minute 25.** Five dots make a curve. Four make a scribble. |
| Somebody computes precision with the wrong denominator and everyone copies it. | Three denominators are live at once — 8, 14 and 986 — and Week 8 only had two. | Write the three denominators in a box on the board and leave them there: **"how many I flagged / how many were real fraud / how many were really innocent."** Point at the box, do not give the answer. |
| The rise-over-run division comes out as a fraction nobody can interpret. | They divided run by rise, or used counts instead of rates. | Ask: *"is your answer bigger or smaller than 1? And what does bigger than 1 mean in this sentence?"* Steepness bigger than 1 means recall is cheap. **Make them read the answer as a sentence, not a number.** |
| The PR curve gets skipped because the clock ran out. | It is the fourth thing in a dense live-code segment. | **Skip the plotting, never the two summary numbers.** `roc_auc_score` 0.6116 and `average_precision_score` 0.2078 with their two baselines is objective 3 in two lines. Set the plot as homework. |
| A student announces the model is useless and disengages. | 0.6116 is genuinely unimpressive and they are not wrong. | Agree out loud, then redirect: *"so is 216 flagged rows with 5 real frauds useless? The bank had 1,000 rows with 14. You concentrated the fraud from 1.4% to 2.3%… and at threshold 0.10 you concentrated it to 37.5%."* **The concentration is the value.** |
| Everything is fine and it finishes at minute 60. | It happens; the cards move fast. | Go to harder variation 1 — count the squares under the curve — and let them arrive at Week 11 early. Or plot the PR curve on a second sheet of graph paper. |

---

## 🧭 Differentiation

This section says what to cut, add or change for a student who is struggling, flying, or not engaging.

### If the student is struggling

**Cut:** the precision-recall curve, `average_precision_score`, and the whole ROC-versus-PR comparison. **Objectives 1, 2 and 4 do not need them**, and a student who owns the threshold sweep and one rise-over-run division has had a completely successful week.

**Cut also:** the real fraud data. The twenty cards are enough for everything. Tenths are kind; 986 is not.

**Copy this exactly.** Hand it over on paper and let them run it as-is, then change one number:

```python
# dial_small.py - the twenty cards, one threshold at a time.
import numpy as np

prob = np.array([0.96, 0.92, 0.88, 0.84, 0.80, 0.76, 0.72, 0.68, 0.64, 0.60,
                 0.55, 0.48, 0.42, 0.36, 0.30, 0.25, 0.20, 0.15, 0.10, 0.05])
truth = np.array([1, 1, 1, 0, 1, 1, 1, 0, 1, 1,
                  0, 1, 0, 0, 1, 0, 0, 0, 0, 0])

t = 0.60                                   # <-- CHANGE ONLY THIS NUMBER
pred = (prob >= t).astype(int)
caught = int(((pred == 1) & (truth == 1)).sum())
alarms = int(((pred == 1) & (truth == 0)).sum())
print("threshold", t)
print("flagged      ", int(pred.sum()))
print("caught       ", caught, "of 10")
print("false alarms ", alarms, "of 10")
print("recall    %d / 10 = %.2f" % (caught, caught / 10))
print("precision %d / %d = %.2f" % (caught, pred.sum(), caught / pred.sum()))
```

Real output at `t = 0.60`:

```text
threshold 0.6
flagged       10
caught        8 of 10
false alarms  2 of 10
recall    8 / 10 = 0.80
precision 8 / 10 = 0.80
```

**The maths, with the algebra skipped entirely.** Do not say "rise over run". Say:

> "Two dots. **How many squares up?** Write it down. **How many squares across?** Write it down. **Divide the first by the second.** If the answer is more than 1 you got a bargain. If it is less than 1 you overpaid. If it is 0 you got robbed."

Two squares up, one across, answer 2 — a bargain. Zero up, one across, answer 0 — robbed. That is the whole idea and it needs no vocabulary at all.

### If the student is flying

1. **Find the threshold that catches exactly half the frauds** (7 of 14) and report what it costs. Push them to use the printed sweep to bracket it, then narrow down.
2. **Count the squares** under the twenty-card ROC curve and compare with `roc_auc_score(truth, prob)` = **0.8500**. Then ask what "area under the curve" could possibly mean as a sentence about frauds and legits. (The honest answer: it is the chance that a randomly chosen fraud got a higher score than a randomly chosen legit. Let them test it: pick a fraud card and a legit card at random twenty times and tally. It is a genuinely delightful hour.)
3. **The threshold that is right for nobody.** Find a row of the real sweep that is dominated — where another row has *both* better precision *and* better recall. (`t = 0.08` and `t = 0.06` are both dominated by `t = 0.10`: same recall of 0.2143, worse precision.) **A dominated threshold is never the right answer for anyone, and spotting them is a real skill.**
4. **The honest question:** *"our AUC is 0.6116 and it rests on 14 frauds. If one fraud had scored slightly higher, how much would that number move?"* Nobody can answer it from one measurement. **That is Week 11**, and a student who is uneasy about four decimal places resting on fourteen rows has exactly the right instinct — tell them so.

### If the student won't engage today

Do the cards. Nothing else. **Twenty cards on a line and one person moving their arm is the entire lesson**, and it takes eight minutes with no screen, no typing and no writing.

If they will do one written thing, make it this: three thresholds on three sticky notes, each with a person's name and one sentence. **That is objective 4 complete**, it is opinion rather than arithmetic so it is hard to be wrong at, and it is the single item this week that they will remember in June — because in Week 34 they will write the same three sentences into a real model card for a real artifact.

If they will do nothing at all: ask them one question and let it sit. *"You are the customer whose card just got blocked at the supermarket because a model was being careful. What number would you like the bank to have used?"* Everybody has an opinion about that one.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the threshold is not the model.** Say: *"I am going to change the threshold from 0.10 to 0.02. Tell me one thing that changes and one thing that does not."*

> **A good answer** names a count or a metric as changing (flagged goes from 8 to 216, recall goes from 0.2143 to 0.3571, precision collapses) **and says explicitly that the model, the probabilities, or the ranking do not change.** A student who only lists what changes has half of it. Prompt with *"and what about the thousand probabilities?"*

**Check 2 — the new maths, on numbers they have not seen.** Write on the board:

```text
point A:  false positive rate 0.20 ,  true positive rate 0.50
point B:  false positive rate 0.40 ,  true positive rate 0.90
```

Say: *"How steep is the curve between those two points, and is that a good deal?"*

> **A good answer:** rise `0.90 − 0.50 = 0.40`, run `0.40 − 0.20 = 0.20`, steepness `0.40 ÷ 0.20 = 2.0`, **and the sentence** "two units of recall for every one unit of false alarms, so yes". A student who gets 2.0 but cannot say what it means has the arithmetic and not the idea — ask *"two what, per one what?"*

**Check 3 — which curve, and why.** Say: *"You have a thousand transactions and fourteen are fraud. Somebody sends you one number to describe your model. Would you rather have the ROC AUC or the average precision, and why?"*

> **A good answer** picks average precision **and mentions the denominator or the size of the innocent pile** — something like "because the 986 innocent rows are a fixed denominator, so 200 false alarms move the false positive rate only about 0.2, while they fill the flagged pile that precision is divided by". Accepting ROC AUC is also fine **if** the reason is "because I want to compare against a model on a different dataset". **The unacceptable answer is a preference with no reason.** Both metrics were on the screen; the reasoning is the objective.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Thinks a different threshold means a different model. Cannot say where the 0.5 was. |
| **2 — Emerging** | Knows the threshold is adjustable and that lowering it catches more. Cannot compute the three fractions without help, and mixes up the denominators. |
| **3 — Secure** | Produces the nine-row sweep table unaided with correct precision, recall and false-alarm counts. Explains what one row means in English. Divides rise by run correctly when told which two points to use. |
| **4 — Fluent** | Reads the shape of the curve without being asked: points at the flat section and says "those seventeen people bought us nothing". Computes rise over run on points of their own choosing and states the result as a sentence about frauds per false alarm. Names three thresholds and a stakeholder for each. |
| **5 — Extending** | Volunteers that ROC and PR disagree *because* the denominators differ. Spots a dominated threshold. Asks whether 0.1774 really means a 17.74% chance, or what happens if you push the two points together — which is Week 12 arriving early. |

---

## 📤 Homework to Assign

The workbook (`workbook/week-10.md`) has eleven sections, and no student does all of them in an evening. **The split:** the twenty-card hand sweep (Build It steps 1–5) is started in class during *Their Turn*, so what goes home is the finishing of it plus the sections below. Treat **Warm-Up, Do the Maths by Hand, Predict the Output, Practice Set B, Fix the Broken Program, Build It and Self-Check** as the required core; **Practice Set A, Puzzle of the Week, Think Deeper and Draw It** are the choose-two extras (Draw It is the quickest and the best of them for a student who thinks in pictures).

**Say this, word for word:**

> "Three parts, about an hour and a half, and the last one is the one I actually care about.
>
> **Part one — the Warm-Up and Do the Maths by Hand.** Five quick questions about last week's F1, then the week's one new division, rise ÷ run. M1 is on the twenty cards, M2 to M4 are on the real fraud data. **After every division, write the sentence** — *'I bought ___ units of recall per unit of false alarm.'* A number on its own gets no marks.
>
> **Part two — the code.** Predict the Output: write your guess in pen *before* you run anything, all four. Then Practice Set B, B1 to B5. If your `highest probability` is not `0.1774`, stop and find the missing `random_state=0` before you go any further. Then Fix the Broken Program: three bugs, one of which never says a word.
>
> **Part three — Build It.** Finish the hand sweep of the twenty cards, **every row adding to 20**, plot the ten dots, and do two rise-over-run divisions off your own graph paper. Check four numbers from `dial.py`. Then the one I care about: **three thresholds you would defend, and beside each one, a person.** Not 'this is the best' — *who is this right for, and what do they care about that the other two do not.* One sentence each. I want to be able to argue with you. Finish with the Bug Log and the Self-Check."

| Workbook section | Items | What it checks | Status | Rough time |
|---|---|---|---|---|
| ✅ Warm-Up | W1–W5 | Last week's F1 and harmonic mean | required | 5 min |
| 🔢 Do the Maths by Hand | M1(a)–(f), M2, M3, M4 | Rise ÷ run on cards, then on 14 / 986 | required | 20 min |
| 🔎 Predict the Output | P1–P4 | Shapes, `inf` sentinel, `>=` vs `>`, the silent AUC bug | required | 10 min |
| ✍️ Practice Set A — Read It | A1–A6 | Vocabulary match, reading the nine-row table, spot-the-bug, baselines, the three denominators | extra | 20 min |
| ✍️ Practice Set B — Write It | B1–B5 | `dial` one-liner, `dot(t)`, `steep.py`, `sweep20.py`, `defend.py` | required | 30 min |
| 🐞 Fix the Broken Program | Bugs 1–3 and the ranking | A shape bug, a runtime bug, a silent bug | required | 10 min |
| 🧩 Puzzle of the Week | Part 1(a)–(g), Part 2(a)–(c) | Three rankings on graph paper; AUC as pairs counted | extra | 20 min |
| 🤔 Think Deeper | T1, T2 | Two paragraphs: AUC versus AP; who owns a default | extra | 15 min |
| 🛠️ Build It | checklist 1–10, hand sweep, two divisions, `dial.py` numbers, three thresholds, Bug Log | The week's deliverable | required | 40 min (hand sweep started in class) |
| 🎨 Draw It | the staircase and three questions | Where the curve is vertical, flat, and where `t = 0.50` sits | extra | 10 min |
| 📊 Self-Check | ten lines | Confidence, honestly rated | required | 3 min |

---

## 🔑 Answer Key

This section holds the answers to the workbook, **section by section and item by item, in the order the workbook sets them**, and to every question posed in the lesson. The values are the ones in the workbook's own ✅ Answers section (recomputed against `dial.py` for this guide); the wrong-answer maps and marking notes are the teacher's additions. Keep it away from the student.

### ✅ Warm-Up

- **W1.** `2 × 3 ÷ (6 + 7 + 11) = 6 ÷ 24 = 0.2500`. The bottom is `2 × TP`, then FP, then FN.
- **W2.** smaller **0.4435**, twice the smaller **0.8870**, **yes** — 0.4976 sits between them. A four-second check that catches every arithmetic slip in a harmonic mean.
- **W3.** It averaged the F1 of the fraud class (**0.2500**) and the F1 of the legitimate class (**0.9909**): `(0.9909 + 0.2500) ÷ 2 = 0.6204`. The classes hold **14** and **986** rows, so an equal vote gives the 986 easy rows the same say as the 14 hard ones.
- **W4.** **TN.** Padding the easy class cannot inflate F1.
- **W5.** A press release would quote **0.5000**; the truth is **0.1800**. Nine of ten things they were looking for walked past.

**Wrong answers to expect:** W1 written as `6 ÷ 21` (forgot the doubled TP on the bottom); W3 answered "it averaged precision and recall" (it averaged two *class* F1s).

### 🔢 Do the Maths by Hand

**M1, on the twenty cards** (dots are (fpr, tpr)):

| Item | Pair | Rise | Run | Steepness | The sentence |
|---|---|---|---|---|---|
| M1(a) | 0.90 → 0.80 | 0.20 | 0.10 | **2.0** | "For every unit of false-alarm rate I spent, I bought **two** units of recall" — a bargain. |
| M1(b) | 0.80 → 0.70 | 0.20 | 0.00 | **no answer** (÷ 0) | see M1(b1) |
| M1(c) | 0.60 → 0.50 | 0.80 − 0.80 = 0.00 | 0.30 − 0.20 = 0.10 | **0.0** | One more innocent card blocked, zero extra frauds. A pure loss. |
| M1(d) | 0.40 → 0.30 | 0.10 | 0.10 | **1.0** | One for one, a coin's exchange rate. |
| M1(e) | 0.30 → 0.05 | 0.00 | 0.50 | **0.0** | Five innocent cards blocked to catch nothing; all ten frauds were already caught at 0.30. |

- **M1(b1).** Nothing went wrong with the arithmetic; **the curve went straight up.** You caught two more frauds and raised not one extra false alarm — **that recall was free.** Dividing by zero is the arithmetic's way of saying "infinitely steep". In code you test `if run == 0:` first, which is why B3 asks for it.
- **M1(f).** In order: **straight up (0.80→0.70), then 2.0, then 1.0, then 0.0, then 0.0.** Recall is cheap at the top of the ranking, where the frauds are stacked; from `t = 0.30` down you pay in people and get nothing back. *Steep on the left, flat on the right, and the flat part is where you stop.*

**M2, on the real data (denominators 14 and 986):**

| from → to | rise | run | steepness | take it? |
|---|---|---|---|---|
| 0.12 → 0.10 | `1 ÷ 14 = 0.071429` | `5 ÷ 986 = 0.005071` | **14.0857** | yes |
| 0.10 → 0.08 | `0 ÷ 14 = 0.000000` | `7 ÷ 986 = 0.007099` | **0.0000** | no |
| 0.04 → 0.02 | `1 ÷ 14 = 0.071429` | `150 ÷ 986 = 0.152130` | **0.4695** | think hard |
| 0.02 → 0.01 | `3 ÷ 14 = 0.214286` | `210 ÷ 986 = 0.212982` | **1.0061** | probably not |

The rises come from `tp` going 2→3, 3→3, 4→5, 5→8; the runs from `fp` going 0→5, 5→12, 61→211, 211→421.

- **M2(a).** **1.0061** (0.02 → 0.01). A steepness of 1 is the rate a coin would give you; below about `t = 0.02` the model has stopped helping.
- **M2(b).** **0.4695** (0.04 → 0.02): one more fraud for 150 more people bothered. Full marks names a person: the customer whose £900 is gone (worth it), the 150 people declined at a till on a Saturday (not worth it), or the analyst who phones all 150 (a fortnight for one arrest). **"Not worth it because 0.4695 is less than 1" gets half marks** — it has not noticed that a price list settles it, which is next week.

**M3.** `1 ÷ 14 = 0.0714286` · `1 ÷ 986 = 0.00101420` · `986 ÷ 14 = 70.4286`.

- **M3(a).** …on **how lopsided your classes are** — how many positives and negatives are in the pile measured.
- **M3(b).** **Bank A's** looks steeper: its rise steps are `1 ÷ 14 = 0.0714` against bank B's `1 ÷ 500 = 0.0020`, thirty-five times as far per fraud. **No, their model is not better — it is the same model.** A steep left corner on a very imbalanced problem is partly the imbalance talking.

**M4.**

- **M4(a).** `4 + 61 + 10 + 925 = 1000` ✅ and `5 + 211 + 9 + 775 = 1000` ✅. Do this before any division, every time.
- **M4(b).**

| t | precision | recall | fpr |
|---|---|---|---|
| 0.04 | `4 ÷ 65 = 0.061538` | `4 ÷ 14 = 0.285714` | `61 ÷ 986 = 0.061866` |
| 0.02 | `5 ÷ 216 = 0.023148` | `5 ÷ 14 = 0.357143` | `211 ÷ 986 = 0.213996` |

- **M4(c).** precision moved by **−0.038390**, recall by **+0.071429**, fpr by **+0.152130**.
- **M4(d).** **Precision** is the one dragged down, because the false alarms fill its own denominator (the review pile went from 65 to 216). The false positive rate moved more in absolute terms but has a **fixed denominator of 986** and plenty of room: each false alarm adds only 0.001. **Full marks names both denominators: 216 (filled by the false alarms) versus 986 (fixed).**

**Wrong answers to expect:** M1(b) given as "0.20" or "infinity" with no English; M2 rises or runs with the two denominators swapped (steepness then comes out as 0.07 and 0.005 inverted); M3(b) answered "bank B, because 500 is bigger".

### 🔎 Predict the Output

Answers assume `dial.py` has been run, so `y_val` and `prob` exist.

**P1.**

```text
(1000,)
[0.03113533 0.01705627 0.01463761]
(1000,) int64
8
```

Same shape because it is the same thousand rows: comparing asks one yes/no question of each number, and `.astype(int)` changes what is in each box, never how many. **`pred.sum()` counts the 1s**, so **8 is the number flagged at `t = 0.10`** — the 8 in the sweep table.

**P2.**

```text
28 28 28
1001 1001 1000
inf
1.0 0.0
```

`prec` and `rec` have 1001 entries and `pthr` has 1000: scikit-learn tacks the point (recall 0, precision 1) on the end so the curve reaches the axis, and no threshold produces it. Plot `rec` against `prec`, never against `pthr`. **`thr[0]` is `inf`**, a sentinel: a fake first threshold so high that nothing is flagged, putting the first dot at the origin. You never use it as a threshold.

**P3.**

```text
[1 0 1 0]
[0 0 0 0]
2 0
```

`>=` includes the value itself; `>` does not. **Line 1 explains the ten flagged cards at `t = 0.60`.** And no, Python would never have told you — `>` is legal and silent.

**P4.**

```text
0.6116
0.6046
0.0914
3
```

You handed the two functions the 0s and 1s from `pred`, and **the confidence had already been thrown away**; they need the raw probabilities to try every threshold. **Line 4 is the tell-tale: three points**, because a column of 0s and 1s has only two places to cut. A real ROC curve on this data has 28.

| Kind of function | What it wants |
|---|---|
| draws a curve: `roc_curve`, `precision_recall_curve`, `roc_auc_score`, `average_precision_score` | probabilities |
| counts cells: `confusion_matrix`, `precision_score`, `recall_score`, `f1_score` | predictions |

**Wrong answers to expect:** P1 line 1 given as `(1000, 2)` (confusing `prob` with `predict_proba`'s raw output); P2 line 2 given as `28 28 28` (they forgot the extra end point); P3 line 3 given as `2 2`.

### ✍️ Practice Set A — Read It

- **A1.** decision threshold → **(iii)** · true positive rate → **(v)** · false positive rate → **(i)** · ROC curve → **(ii)** · average precision → **(iv)**.
- **A1(a).** True positive rate and **recall** are the same fraction, `TP ÷ (TP + FN)`; recall is the more common name and is not in the list. Say "recall, also called the true positive rate" once and move on.
- **A2(a).** **No, never.** Lowering the bar can only add rows to the flagged pile, so a caught fraud cannot escape. If recall ever goes down there is a bug, most likely the `tn, fp, fn, tp` order.
- **A2(b).** **No** — precision goes up between `t = 0.50` and `t = 0.15`, from 0.0000 to 1.0000. At 0.50 nothing is flagged, so precision is `0 ÷ 0` and `zero_division=0` printed a placeholder. The 0.0000 on the top row is not a measurement; after that, precision only falls.
- **A2(c).** extra false alarms **17** (5 → 22), extra frauds **0**.
- **A2(d).** `4 + 61 + 10 + 925 = 1000` ✅.
- **A2(e).** `t = 0.10` is the best defensible answer ("eight flagged, three real, a third of the pile is worth opening; the next two rows add seventeen people for nothing"), said to the person who signs off the review queue. `t = 0.12` is equally full marks, said to a two-person review desk. **`t = 0.50` scores zero**: it flags nothing.
- **A3.**

| # | What happens | The fix |
|---|---|---|
| a | `ValueError: not enough values to unpack (expected 4, got 1)`, with a `UserWarning` above it naming the fix. Truth and prediction in those five rows are all zeros, so the matrix is 1×1 | `confusion_matrix(y_val[:5], pred[:5], labels=[0, 1]).ravel()` |
| b | `ValueError: too many values to unpack (expected 2)`; `roc_curve` returns three lists | `fpr, tpr, thr = roc_curve(y_val, prob)` |
| c | `ValueError: continuous format is not supported`; the first argument must be the truth | `roc_curve(y_val, prob)` — truth first, always |
| d | `ValueError: x and y must have same first dimension, but have shapes (1000,) and (1001,)` | `plt.plot(rec, prec)` |
| e | `predict_proba` returns two columns, so `pred` is (1000, 2) and the metrics raise `ValueError: Classification metrics can't handle a mix of binary and multilabel-indicator targets` | `model.predict_proba(X_val)[:, 1]` |
| f | **No error, no warning**, and 0.6046 instead of 0.6116 | pass `prob`, not a 0/1 array |

  Note on (a): on the full thousand rows it does **not** crash, because `y_val` holds 14 frauds, so the matrix is `[[986, 0], [14, 0]]`. The crash needs the truth to be single-class too, which is why it bites on small slices and not on the data you tested with. That is why `labels=[0, 1]` goes in every time.
- **A3(g).** **(f)** is the silent one, and the most dangerous because 0.6046 looks exactly like a result. Everything else stops the program.
- **A4.** i → **S** · ii → **R** · iii → **T** · iv → **P** · v → **Q**.
- **A5(a).** `0.7986 ÷ 0.5000 = 1.5972` · `0.1877 ÷ 0.0140 = 13.4071`.
- **A5(b).** The **rare** model's AP is further above its own coin (13.4 times against 1.6), but it is the **smaller** number (0.1877 against 0.7986). That does not make it the more useful model: the balanced model has the higher AUC (0.7788 against 0.6831). AP has no fixed baseline, so quoting one without the class balance is close to meaningless.
- **A5(c).** **AUC**, because a coin always gets exactly 0.5000. AP's baseline moves with the positive rate (0.5000 here, 0.0140 there).
- **A5(d).** Nobody's fault except the 0.5. The rare model's most confident answer is 0.1774, so comparing with 0.5 flags nothing. **Change the threshold, not the model.**
- **A6.** The three boxes: **precision = 3 ÷ 8 = 0.3750**, **recall = 3 ÷ 14 = 0.2143**, **false positive rate = 5 ÷ 986 = 0.005071**. Rise-over-run panel: rise `3/14 − 2/14 = 1/14 = 0.071429`, run `5/986 − 0/986 = 0.005071`, steepness **14.0857**. Sentence: "I bought **fourteen** units of recall per unit of false-alarm rate, so I would take that trade."
- **A6(a).** **986** is on the bottom of the false positive rate; **14** is on the bottom of recall.
- **A6(b).** Recall's (14) and the false positive rate's (986) never change: they are properties of the data. **Precision's denominator is the one that moves** (0 → 8 → 216 → 429), because it is how many rows you chose to flag.

**Note on the A5 figures:** they come from `balance.py` in the workbook, which is not reproduced in this guide; they are the workbook's own values and were not re-derived for this key.

**Vocabulary reference (A1 and the week's six new terms).** Not a workbook page, but these are the one-line definitions to mark A1 and the Self-Check against:

> **Decision threshold** — the probability above which you call something positive. 0.5 is a default that came with the library, not a law of nature.

> **True positive rate** — of everything that really was positive, the fraction you caught. `TP ÷ (TP + FN)`. **The same number as recall, under an older name.**

> **False positive rate** — of everything that really was negative, the fraction you wrongly flagged. `FP ÷ (FP + TN)`. On our data the denominator is 986, which is why it moves so slowly.

> **ROC curve** — one dot per threshold, true positive rate up, false positive rate across. **One model, many dots.** The dashed diagonal is what a coin gets.

> **Precision-recall curve** — the same sweep, precision up, recall across. The one to trust when positives are rare, because precision's denominator is the pile you actually have to review.

> **Average precision** — one number summarising the precision-recall curve. Its baseline is not 0.5; it is **the positive class rate** — 0.0140 for us — so it must always be quoted with the class balance beside it.

**Wrong answers to expect:** A2(b) answered "yes, it only goes down" (missed the placeholder); A3 answered "(a) is the silent one" (it is loud); A6(b) answered "precision's" (it is the one that moves).

### ✍️ Practice Set B — Write It

Each program is checked by running it; the expected output is the real output.

**B1.**

```python
print("flagged at t = 0.04 :", int((prob >= 0.04).astype(int).sum()))
```

```text
flagged at t = 0.04 : 65
```

One `(prob >= t).astype(int)`, one `.sum()`, one `int(...)` so it prints as a whole number.

**B2.**

```python
pos = y_val.sum()
neg = len(y_val) - pos


def dot(t):
    pred = (prob >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_val, pred, labels=[0, 1]).ravel()
    print("t %.2f  tp %3d / %d  fp %3d / %d  dot (fpr %.6f, tpr %.6f)"
          % (t, tp, pos, fp, neg, fp / neg, tp / pos))
    return fp / neg, tp / pos


for t in [0.12, 0.10, 0.02]:
    dot(t)
```

```text
t 0.12  tp   2 / 14  fp   0 / 986  dot (fpr 0.000000, tpr 0.142857)
t 0.10  tp   3 / 14  fp   5 / 986  dot (fpr 0.005071, tpr 0.214286)
t 0.02  tp   5 / 14  fp 211 / 986  dot (fpr 0.213996, tpr 0.357143)
```

`pos` and `neg` live outside the function because they never change: the denominators are fixed and only the numerators move.

**B3.** `steep.py`:

```python
"""steep.py - five pairs of thresholds, one division each.  Week 10 workbook."""
pos = y_val.sum()
neg = len(y_val) - pos


def point(t):
    pred = (prob >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_val, pred, labels=[0, 1]).ravel()
    return tp / pos, fp / neg


print("  from    to     rise      run      steepness   verdict")
for t1, t2 in [(0.15, 0.12), (0.12, 0.10), (0.10, 0.08), (0.04, 0.02), (0.02, 0.01)]:
    tpr1, fpr1 = point(t1)
    tpr2, fpr2 = point(t2)
    rise = tpr2 - tpr1
    run = fpr2 - fpr1
    if run == 0:
        print("  %.2f -> %.2f  %.6f %.6f   straight up   free recall"
              % (t1, t2, rise, run))
    else:
        s = rise / run
        if s > 1:
            v = "take it"
        elif s > 0:
            v = "think hard"
        else:
            v = "do not"
        print("  %.2f -> %.2f  %.6f %.6f   %9.4f   %s" % (t1, t2, rise, run, s, v))
```

```text
  from    to     rise      run      steepness   verdict
  0.15 -> 0.12  0.071429 0.000000   straight up   free recall
  0.12 -> 0.10  0.071429 0.005071     14.0857   take it
  0.10 -> 0.08  0.000000 0.007099      0.0000   do not
  0.04 -> 0.02  0.071429 0.152130      0.4695   think hard
  0.02 -> 0.01  0.214286 0.212982      1.0061   take it
```

**The `if run == 0:` branch is the point.** Without it the first pair raises `ZeroDivisionError` and the other four never print; the honest label for that row is "free recall", the best row in the table. The last row says "take it" because 1.0061 is just over 1, and **a human should override that**: one for one is a coin's exchange rate, and the program can do the division but not the judgement.

**B4.** `sweep20.py`:

```python
"""sweep20.py - the twenty index cards, ten thresholds, with the sum check.  Week 10 workbook."""
import numpy as np
from sklearn.metrics import confusion_matrix

prob = np.array([0.96, 0.92, 0.88, 0.84, 0.80, 0.76, 0.72, 0.68, 0.64, 0.60,
                 0.55, 0.48, 0.42, 0.36, 0.30, 0.25, 0.20, 0.15, 0.10, 0.05])
truth = np.array([1, 1, 1, 0, 1, 1, 1, 0, 1, 1,
                  0, 1, 0, 0, 1, 0, 0, 0, 0, 0])
print("   t   tp  fp  fn  tn   sum   tpr    fpr")
for t in [0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10, 0.05]:
    pred = (prob >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(truth, pred, labels=[0, 1]).ravel()
    total = tn + fp + fn + tp
    print("%5.2f %4d %3d %3d %3d %5d  %.2f   %.2f   %s"
          % (t, tp, fp, fn, tn, total, tp / 10.0, fp / 10.0,
             "OK" if total == 20 else "LOST A CARD"))
```

```text
   t   tp  fp  fn  tn   sum   tpr    fpr
 0.90    2   0   8  10    20  0.20   0.00   OK
 0.80    4   1   6   9    20  0.40   0.10   OK
 0.70    6   1   4   9    20  0.60   0.10   OK
 0.60    8   2   2   8    20  0.80   0.20   OK
 0.50    8   3   2   7    20  0.80   0.30   OK
 0.40    9   4   1   6    20  0.90   0.40   OK
 0.30   10   5   0   5    20  1.00   0.50   OK
 0.20   10   7   0   3    20  1.00   0.70   OK
 0.10   10   9   0   1    20  1.00   0.90   OK
 0.05   10  10   0   0    20  1.00   1.00   OK
```

A program that prints its own sum is worth ten that are probably right. Every row matches the by-hand sweep under **🛠️ Build It** below, so mark the page against it row by row.

**B5.** `defend.py` (it needs the imports and `prob` from `dial.py`, including `precision_score`, `recall_score`, `roc_auc_score` and `average_precision_score`):

```python
"""defend.py - nine thresholds, and the three I would defend.  Week 10 workbook."""
pos = int(y_val.sum())
neg = len(y_val) - pos
print("val rows %d   real frauds %d   real legit %d" % (len(y_val), pos, neg))
print("   t  flagged  tp  fp   precision  recall      fpr   extra tp  extra fp")
last_tp = 0
last_fp = 0
worth_it = None
for t in [0.50, 0.15, 0.12, 0.10, 0.08, 0.06, 0.04, 0.02, 0.01]:
    pred = (prob >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_val, pred, labels=[0, 1]).ravel()
    if tn + fp + fn + tp != len(y_val):
        print("COUNTS DO NOT ADD UP")
    if tp > last_tp:
        worth_it = t
    print("%5.2f %7d %3d %3d     %.4f  %.4f  %.6f %9d %9d"
          % (t, int(pred.sum()), tp, fp, precision_score(y_val, pred, zero_division=0),
             recall_score(y_val, pred, zero_division=0), fp / neg,
             tp - last_tp, fp - last_fp))
    last_tp = tp
    last_fp = fp
print("the lowest threshold that still bought me a fraud : %.2f" % worth_it)
print("ROC AUC %.4f   (a coin gets 0.5000)" % roc_auc_score(y_val, prob))
print("AP      %.4f   (a coin gets %.4f)"
      % (average_precision_score(y_val, prob), y_val.mean()))
```

```text
val rows 1000   real frauds 14   real legit 986
   t  flagged  tp  fp   precision  recall      fpr   extra tp  extra fp
 0.50       0   0   0     0.0000  0.0000  0.000000         0         0
 0.15       1   1   0     1.0000  0.0714  0.000000         1         0
 0.12       2   2   0     1.0000  0.1429  0.000000         1         0
 0.10       8   3   5     0.3750  0.2143  0.005071         1         5
 0.08      15   3  12     0.2000  0.2143  0.012170         0         7
 0.06      25   3  22     0.1200  0.2143  0.022312         0        10
 0.04      65   4  61     0.0615  0.2857  0.061866         1        39
 0.02     216   5 211     0.0231  0.3571  0.213996         1       150
 0.01     429   8 421     0.0186  0.5714  0.426978         3       210
the lowest threshold that still bought me a fraud : 0.01
ROC AUC 0.6116   (a coin gets 0.5000)
AP      0.2078   (a coin gets 0.0140)
```

**The workbook's closing question:** the two rows that bought **zero** extra frauds are `t = 0.08` and `t = 0.06`, and between them they bothered **17** people (7 + 10). `worth_it` comes out at 0.01, not 0.10, because the program only remembers the *lowest* threshold that bought a fraud; the honest answer to "where does lowering the bar stop paying?" needs a price, which is next week.

**Wrong answers to expect:** B1 printing `65` as `65.0` (no `int`); B3 crashing with `ZeroDivisionError` on the first pair; B4 with `>` instead of `>=` (every row where a card sits exactly on the threshold is one out, and the sum still says OK); B5 with `last_tp` and `last_fp` updated before they are printed, so the two "extra" columns are all zeros.

### 🐞 Fix the Broken Program

- **Bug 1 — `prob = model.predict_proba(X_val)`. A shape bug.** `predict_proba` returns two columns (column 0 "probability legit", column 1 "probability fraud"), so `prob` is **(1000, 2)** and the comparison is a 1000×2 grid that the metrics cannot match against 1,000 truths. **The line to add:** `print(prob.shape)`, which prints `(1000, 2)` against `y_val` at `(1000,)`. **The fix:** `prob = model.predict_proba(X_val)[:, 1]`.
- **Bug 2 — `fpr, tpr, thr = roc_curve(prob, y_val)`. A runtime bug.** "Continuous" means full of decimals, and the thing full of decimals is **`prob`**, which was put in the first position where the truth belongs. **The fix:** `roc_curve(y_val, prob)`. **The rule: truth first, always.**
- **Bug 3 — `flagged`. A silent logic bug.** `flagged` holds 0s and 1s, a thousand decisions already made; `prob` holds 1,000 decimals between 0.0001 and 0.1774. `roc_auc_score` had only two distinct values to work with (two places to cut, a three-point curve) and the confidence had already been thrown away by the `>= 0.10`. **The fix:** `roc_auc_score(y_val, prob)` and `average_precision_score(y_val, prob)`.
- **The two closing questions.** The **AUC** is the easier error to miss: 0.6046 against 0.6116 is a second-decimal difference nobody would question, while 0.0914 against 0.2078 is a big miss. A wrong input can produce a right-looking number, so "it looked fine" is not evidence; the reliable check is **`len(fpr)` was 3 instead of 28**.
- **Ranking, easiest → hardest: 1, 2, 3.** Bug 1 crashes on the first row and names both shapes if you print them; Bug 2 is obscure for ten seconds and then obvious; Bug 3 never complains and would have gone into a report. What catches each: **printing a shape**, **the phrase "truth first"**, and **`len(fpr)`**.

### 🧩 Puzzle of the Week

**Part 1(a).** Typing the rounded numbers: `0.3333 ÷ 0.2000 = 1.6665`. Using the fractions: `(1 ÷ 3) ÷ (1 ÷ 5) = 5 ÷ 3 = 1.6667`. Take the mark for either; the gap is the rounding, and rounding early leaks into every number downstream. An up-step is about **1.67** times as tall as a right-step is wide, because there are fewer frauds than legits.

**Part 1(b) — ranking A, `F F L F L L L L`:**

| card | F or L | fpr | tpr |
|---|---|---|---|
| start | — | 0.0000 | 0.0000 |
| 1 | F | 0.0000 | 0.3333 |
| 2 | F | 0.0000 | 0.6667 |
| 3 | L | 0.2000 | 0.6667 |
| 4 | F | 0.2000 | 1.0000 |
| 5 | L | 0.4000 | 1.0000 |
| 6 | L | 0.6000 | 1.0000 |
| 7 | L | 0.8000 | 1.0000 |
| 8 | L | 1.0000 | 1.0000 |

**Part 1(c) — ranking B, `F L F L F L L L`:** after card 1 **(0.0000, 0.3333)**, card 3 **(0.2000, 0.6667)**, card 5 **(0.4000, 1.0000)**, card 8 **(1.0000, 1.0000)**.

**Part 1(d) — ranking C, `L F F L F L L L`:** after card 1 **(0.2000, 0.0000)**, card 3 **(0.2000, 0.6667)**, card 5 **(0.4000, 1.0000)**, card 8 **(1.0000, 1.0000)**. Same as B except it starts by going sideways.

**Part 1(e).** By eye, best first: **A, B, C.**

**Part 1(f).**

| ranking | pairs in the right order | that over 15 |
|---|---|---|
| A | **14** (5 + 5 + 4) | 0.93333 |
| B | **12** (5 + 4 + 3) | 0.80000 |
| C | **11** (4 + 4 + 3) | 0.73333 |

**Part 1(g).** It printed **0.93333**, and the count for A was 14 out of 15 = 0.93333. **The sentence:** "`roc_auc_score` is counting pairs: the fraction of fraud-and-legit pairs my model put in the right order." That explains why a coin gets 0.5, and why AUC cares only about the ranking, not the probabilities. (Checked by running `roc_auc_score` on the three rankings: 0.9333, 0.8000, 0.7333.)

**Part 2(a).** **No.** The most suspicious card in ranking C is legit, so any threshold low enough to catch a fraud has already caught that legit card. **Part 2(b).** A threshold between 0.80 and 0.84 either flags the legit card at 0.84 and misses the fraud at 0.80, or flags neither. **Part 2(c).** To reach the top-left corner you must change **the ranking** (a better model, features or data), **not the threshold**; the threshold only chooses a point on the staircase you already have.

### 🤔 Think Deeper

**T1.** A full-marks paragraph separates the two questions and names the denominator.

> *"AUC asks **can the model rank the frauds above the innocents**, and ours scores 0.6116 where a coin gets 0.5000 — so as a ranking machine it is mediocre, and I would not claim otherwise. AP asks **if I open my review pile, will it be worth opening**, and ours scores 0.2078 where a coin would get 0.0140, the fraud rate. That is about fifteen times better than nothing. Both describe the same model on the same 1,000 rows. The reason they disagree is the denominator: the false positive rate divides by **986**, so 211 false alarms slide the ROC across by only 0.2140 and it looks survivable, while precision divides by **216**, the pile a human has to review, and it falls from 0.3750 to 0.0231. At `t = 0.10` the model hands me 8 rows of which 3 are fraud, out of a background rate of 1.4% — it has concentrated the needles by a factor of twenty-seven without catching anything yet. **So: a weak ranker that is nevertheless a useful triage tool, and the sentence I would put on the report is 'AUC 0.6116, AP 0.2078 on 14 positives in 1,000 validation rows — at a threshold of 0.10 it returns 8 cases a day of which about 3 are real.'"*

**What earns the marks:** the two questions named separately, at least three real numbers, the class balance printed beside the AP, and a report sentence that contains the threshold. **What loses them:** "it's a bad model" with no number, or "AP 0.21 is terrible", which forgets that AP has no fixed baseline.

**T2.** A full-marks paragraph does not blame the library.

> *"A default is somebody else's guess, frozen into a tool, that keeps making decisions until somebody notices. 0.5 is a perfectly sensible guess when you know nothing — it is the least stupid place to cut if the classes are roughly even — and the library authors were right to pick something rather than force everyone to choose on day one. The person responsible is **me**, because I am the one who knows my classes are 99 to 1 and knows my highest probability is 0.1774, and the library does not. The smallest thing I can write down is the threshold and where I picked it: `THRESHOLD = 0.10  # chosen on the validation set; the review desk clears ~8 cases a day`. Three things in one line — the number, the pile it was chosen on, and the human reason. Now the next person can disagree with me, and that is the difference between tuning and lying."*

The strongest answers notice that a default is not neutral just because nobody chose it, and that writing the choice down is what makes it arguable. **"It's the library's fault" scores zero.**

### 🛠️ Build It

The workbook's ten-item step checklist maps onto the material below: steps 1–4 are the hand sweep (the first table), step 5 is the two divisions, steps 6–7 are the `dial.py` numbers and the picture, steps 8–9 are the three thresholds and the last line, step 10 is the Bug Log. Marking priority: **the three defended thresholds, with people, are the hardest-marked item.**

**The ten-threshold sweep — the marking key.** Every row must come to 20. Here are the twenty cards, in order, with the truths:

| prob | 0.96 | 0.92 | 0.88 | 0.84 | 0.80 | 0.76 | 0.72 | 0.68 | 0.64 | 0.60 |
|---|---|---|---|---|---|---|---|---|---|---|
| truth | F | F | F | legit | F | F | F | legit | F | F |

| prob | 0.55 | 0.48 | 0.42 | 0.36 | 0.30 | 0.25 | 0.20 | 0.15 | 0.10 | 0.05 |
|---|---|---|---|---|---|---|---|---|---|---|
| truth | legit | F | legit | legit | F | legit | legit | legit | legit | legit |

**Ten frauds, ten legits.** The workbook's table asks for `tp`, `fp`, `fn`, `tn`, the sum, `tpr` and `fpr`; `fn = 10 − tp` and `tn = 10 − fp`, so the key for those columns is the **B4** output above (every row sums to 20). The rows below add the teacher's extra check, **precision and recall with every division written out** — a stretch the workbook does not require, but the one to use if a student asks "what happens to precision?":

| t | flagged | caught | false alarms | precision | recall | tpr | fpr |
|---|---|---|---|---|---|---|---|
| 0.90 | 2 | 2 | 0 | `2 ÷ 2 = 1.0000` | `2 ÷ 10 = 0.2000` | 0.20 | 0.00 |
| 0.80 | 5 | 4 | 1 | `4 ÷ 5 = 0.8000` | `4 ÷ 10 = 0.4000` | 0.40 | 0.10 |
| 0.70 | 7 | 6 | 1 | `6 ÷ 7 = 0.8571` | `6 ÷ 10 = 0.6000` | 0.60 | 0.10 |
| 0.60 | 10 | 8 | 2 | `8 ÷ 10 = 0.8000` | `8 ÷ 10 = 0.8000` | 0.80 | 0.20 |
| 0.50 | 11 | 8 | 3 | `8 ÷ 11 = 0.7273` | `8 ÷ 10 = 0.8000` | 0.80 | 0.30 |
| 0.40 | 13 | 9 | 4 | `9 ÷ 13 = 0.6923` | `9 ÷ 10 = 0.9000` | 0.90 | 0.40 |
| 0.30 | 15 | 10 | 5 | `10 ÷ 15 = 0.6667` | `10 ÷ 10 = 1.0000` | 1.00 | 0.50 |
| 0.20 | 17 | 10 | 7 | `10 ÷ 17 = 0.5882` | `10 ÷ 10 = 1.0000` | 1.00 | 0.70 |
| 0.10 | 19 | 10 | 9 | `10 ÷ 19 = 0.5263` | `10 ÷ 10 = 1.0000` | 1.00 | 0.90 |
| 0.05 | 20 | 10 | 10 | `10 ÷ 20 = 0.5000` | `10 ÷ 10 = 1.0000` | 1.00 | 1.00 |

**Machine check.** This is the real output of `cards.py` (it also prints AUC 0.8500 and the three rise-over-run lines):

```python
"""cards.py - the twenty index cards, checked by machine.  Week 10."""
import numpy as np
from sklearn.metrics import (average_precision_score, precision_score,
                             recall_score, roc_auc_score)

prob = np.array([0.96, 0.92, 0.88, 0.84, 0.80, 0.76, 0.72, 0.68, 0.64, 0.60,
                 0.55, 0.48, 0.42, 0.36, 0.30, 0.25, 0.20, 0.15, 0.10, 0.05])
truth = np.array([1, 1, 1, 0, 1, 1, 1, 0, 1, 1,
                  0, 1, 0, 0, 1, 0, 0, 0, 0, 0])
print("frauds %d   legit %d" % (truth.sum(), len(truth) - truth.sum()))
print("   t   flagged  caught  false alarms   tpr    fpr   precision  recall")
rows = []
for t in [0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10, 0.05]:
    pred = (prob >= t).astype(int)
    tp = int(((pred == 1) & (truth == 1)).sum())
    fp = int(((pred == 1) & (truth == 0)).sum())
    rows.append((t, tp / 10.0, fp / 10.0))
    print("%5.2f   %6d  %6d  %12d   %.2f   %.2f     %.4f  %.4f"
          % (t, pred.sum(), tp, fp, tp / 10.0, fp / 10.0,
             precision_score(truth, pred, zero_division=0),
             recall_score(truth, pred, zero_division=0)))
print()
print("roc_auc_score            %.4f" % roc_auc_score(truth, prob))
print("average_precision_score  %.4f" % average_precision_score(truth, prob))
print()
for a, c in [(0, 1), (3, 4), (6, 9)]:
    t1, tpr1, fpr1 = rows[a]
    t2, tpr2, fpr2 = rows[c]
    rise = tpr2 - tpr1
    run = fpr2 - fpr1
    print("t %.2f -> t %.2f :  rise %.2f  run %.2f  rise/run %.4f"
          % (t1, t2, rise, run, rise / run))
```

```text
frauds 10   legit 10
   t   flagged  caught  false alarms   tpr    fpr   precision  recall
 0.90        2       2             0   0.20   0.00     1.0000  0.2000
 0.80        5       4             1   0.40   0.10     0.8000  0.4000
 0.70        7       6             1   0.60   0.10     0.8571  0.6000
 0.60       10       8             2   0.80   0.20     0.8000  0.8000
 0.50       11       8             3   0.80   0.30     0.7273  0.8000
 0.40       13       9             4   0.90   0.40     0.6923  0.9000
 0.30       15      10             5   1.00   0.50     0.6667  1.0000
 0.20       17      10             7   1.00   0.70     0.5882  1.0000
 0.10       19      10             9   1.00   0.90     0.5263  1.0000
 0.05       20      10            10   1.00   1.00     0.5000  1.0000

roc_auc_score            0.8500
average_precision_score  0.8485

t 0.90 -> t 0.80 :  rise 0.20  run 0.10  rise/run 2.0000
t 0.60 -> t 0.50 :  rise 0.00  run 0.10  rise/run 0.0000
t 0.30 -> t 0.05 :  rise 0.00  run 0.50  rise/run 0.0000
```

**Expected runtime: under 1 second.**

**Common wrong answers, and what to say:**

- **`t = 0.60` gives flagged 9.** They forgot that `>=` includes the card sitting exactly on 0.60. *"Does 'at least 0.60' include 0.60?"*
- **Precision at `t = 0.30` written as `10 ÷ 10`.** They used the fraud count as the denominator. **Precision's denominator is how many you flagged: 15.**
- **Recall falling somewhere.** Impossible. Ask them to re-count; a card got dropped.


**Step 6 and the "numbers from `dial.py`" table.** The complete `dial.py` and its real output are in the **🧰 Prep Checklist** above, printed in full. Do not re-derive them. The workbook's table asks for six values:

| What | Must be |
|---|---|
| highest probability | **0.1774** |
| how many above 0.5 | **0** |
| `tp` at `t = 0.10` | **3** |
| `roc_auc_score` | **0.6116** |
| `average_precision_score` | **0.2078** |
| a coin's AP here | **0.0140** |

If any is off, check the student's whole output against the Prep Checklist block **character by character on these four numbers**:

| Must be exactly | If it is not |
|---|---|
| `real frauds 14` | `stratify=y` is missing from one of the two splits. |
| `highest probability 0.1774` | `random_state=0` is missing from `LogisticRegression`, or the splits are not seeded. |
| `t = 0.10` row reading `8   3   5  11  981` | The threshold list is wrong, or `ravel()` is being unpacked in the wrong order. It is `tn, fp, fn, tp`. |
| `roc_auc_score 0.6116` | `pred` was passed instead of `prob` — you will see `0.6046`. |

**Step 7, the plot (`dial.png`).** Two panels. The left ROC climbs raggedly and stays above the diagonal. The right PR curve starts at the top-left and **falls off a cliff within the first fifth of the chart**, then crawls along just above the dashed 0.0140 line. A student whose PR curve looks like a gentle slope has plotted `prec` against `pthr` — see the Debugging Clinic.


**Step 5 — the two divisions off their own graph paper.** The workbook asks for the steepest and the flattest pair they can find. **The steep pair** — from the card curve, `t = 0.90` at (0.00, 0.20) to `t = 0.80` at (0.10, 0.40):

```text
rise  =  0.40 − 0.20  =  0.20
run   =  0.10 − 0.00  =  0.10
0.20 ÷ 0.10  =  2.0
```

> **The sentence:** "Between those two thresholds I bought **two frauds for every one false alarm**. That is worth doing."

**The flat pair** — `t = 0.30` at (0.50, 1.00) to `t = 0.05` at (1.00, 1.00):

```text
rise  =  1.00 − 1.00  =  0.00
run   =  1.00 − 0.50  =  0.50
0.00 ÷ 0.50  =  0.0
```

> **The sentence:** "Between those two thresholds I blocked **five more innocent customers and caught zero extra frauds**. There is no reason on earth to do it."

**If they used the real data instead** (which is allowed and better), accept any of these three, all printed by `dial.py`:

```text
t 0.12 -> 0.10   rise 0.071429  run 0.005071  rise/run = 14.0857
t 0.10 -> 0.08   rise 0.000000  run 0.007099  rise/run = 0.0000
t 0.02 -> 0.01   rise 0.214286  run 0.212982  rise/run = 1.0061
```

- **14.0857** → "fourteen units of recall per unit of false-alarm rate — a bargain, take it."
- **0.0000** → "seventeen extra people bothered, no extra frauds — never do this."
- **1.0061** → "about one for one, which is what a coin gets. Down here the model has stopped helping."

**Marking note:** the number alone is worth nothing. **The sentence is the objective.** A student who writes `14.0857` and stops has done the arithmetic and missed the week.


**Step 8 (and the last-line prompt, step 9).** There is no single right answer, and that is deliberate. A **full-mark** answer names three thresholds that are genuinely different in kind, gives a real stakeholder for each, and says what that stakeholder is willing to give up. Three that earn full marks:

| Threshold | Defended to | The sentence |
|---|---|---|
| **0.12** | the two-person fraud review desk | "They can look at 2 cases a day, and at 0.12 both of them are real fraud — precision 1.0000. I would rather catch 2 of 14 and waste nobody's time than hand them a queue they cannot clear." |
| **0.10** | the manager who signs off the queue | "8 flagged, 3 real, so a third of the pile is worth opening. It is the steepest sloped step on the curve (14.09), and the next two steps down, 0.08 and 0.06, cost seventeen more people and catch nothing." |
| **0.02** | the customer whose money is gone | "5 frauds caught instead of 3. I do not care about the 211 phone calls; a phone call is an inconvenience and a stolen paycheque is not. Recall is the only column that matters to me." |

**Answers to reject, gently:**

- **"0.5, because it is the default."** On this model 0.5 flags nothing at all. **This is the one factually wrong answer available**, and it is worth pointing out kindly.
- **"0.01, because recall is highest."** Recall 0.5714 sounds best until you name the 421 false alarms. Ask: *"who is the person on the other end of the 421st phone call, and what would they say?"*
- **Three thresholds with no people.** Send it back. The stakeholder **is** the answer; the number is just a label for it.
- **Three thresholds that are all within 0.01 of each other.** They have not understood that the three should be *different kinds of decision*.

**Step 9 — "what would you need to know to choose between those three?"** *"How much each kind of mistake actually costs. If a missed fraud costs the bank £500 and a false alarm costs £10, I can multiply instead of arguing."* Anything like that means they have worked out what Week 11 is for.

**Which panel falls off a cliff, and why it disagrees with the other one** (the two prompts under the `dial.py` table): the **precision-recall** panel, from 0.3750 to 0.0231 as false alarms go from 5 to 211, then it crawls just above the dashed 0.0140 line. *"Precision divides by **216**, the pile I have to review, and 216 rows holding 5 frauds is about forty-two innocent people per thief. The false positive rate divides by **986**, so 211 false alarms only move it by 0.21. Both charts are true; the precision-recall one tells the truth about the day's work."*


**Step 10 — the Bug Log (two entries).** One loud and one silent, and the point is that both kinds exist: *entry one* (the three-point curve) never complains; *entry two* (the 1×1 matrix) stops the program and names its own fix.

**Entry one.**
Message: *none.* Symptom: `roc_curve` returned 3 points instead of 28, and the AUC read 0.6046 instead of 0.6116.
Meaning: I handed it hard 0/1 predictions, which only have two possible values, so there were only two places to cut.
Fix: pass `prob`, not `pred`.
The rule I am keeping: **if a metric draws a curve it wants probabilities; if it counts cells it wants predictions.**

**Entry two.**
Message: `ValueError: not enough values to unpack (expected 4, got 1)`, with a `UserWarning` above it naming the fix.
Meaning: the truth and my predictions each held only one class (a tiny slice, nothing flagged), so the confusion matrix came back 1×1.
Fix: `confusion_matrix(y, pred, labels=[0, 1])`.
The rule I am keeping: **read the whole error, not just the last line. This one's fix was printed one line above the traceback.**

### 🎨 Draw It

The staircase drawn on squared paper, with the three questions answered:

- **Where it goes straight up:** between `t = 0.80` and `t = 0.70` (and from the origin up to `t = 0.90`). It cost nothing: two extra frauds, zero extra false alarms, so the division has no answer and the honest label is "free recall".
- **Where it goes straight across:** from `t = 0.30` down to `t = 0.05`. It bought nothing at all: recall was already 1.0000 and five more innocent cards were blocked. Both ends of a sweep are usually waste.
- **`t = 0.50` on the real fraud model:** the **bottom-left corner, exactly (0, 0)**, catching **0 of the 14 frauds**. A good drawing labels that dot "the default".

A strong drawing also has the diagonal dashed in with a sentence under it (*"this is what a coin gets; the gap between my curve and it is all my model contributed"*) and an arrow labelled "the price list" pointing at the three ringed dots, which is next week.

### 📊 Self-Check

There are no right answers to a self-check, but three of the ten lines carry the week. **"Add the four counts up every row"** is four seconds that catches every miscount you will make this year; if it is not a 😀 the habit is not installed. **"Read a steepness out loud as recall bought per false alarm"**: a decimal without the sentence is arithmetic without the point; go back to M1 and say all five out loud. And **"name the person each threshold is right for"** is marked again in Week 11, Week 34 and Week 36, and it separates somebody who can operate a library from somebody you would let near a live system.

### Answers to every question posed in the lesson

**Hook — "how many frauds does this model catch?"** Zero. At threshold 0.5 nothing is flagged at all, because the highest probability in the validation set is 0.1774. The model is 98.6% accurate and useless.

**Hook — "whose fault is that?"** Nobody's, and specifically not the model's. The model produced a useful ranking; the 0.5 threw it away. Accept "the default's fault" — that is exactly right.

**Concept step 2 — "which column only ever goes up?"** Recall. Lowering the threshold can only add rows to the flagged pile, never remove them, so a fraud that has already been caught cannot escape. Precision has no such guarantee.

**Concept step 3 — "how steep is that?"** `0.20 ÷ 0.10 = 2.0`. Two units of recall per unit of false-alarm rate.

**Concept step 3 — "what did we just buy?"** Nothing. Rise 0.00 over run 0.10 gives a steepness of 0: one more innocent card blocked, zero extra frauds.

**Concept step 4 — "what is false positive rate's denominator?"** On the cards, 10 (the ten real legits). On the real data, **986**.

**Live-code step 1 — "what will be in the `flagged` column for `t = 0.50`?"** Zero.

**Live-code step 1 — "what is the `tp` column doing in rows four, five and six?"** Nothing — it stays at 3 while false alarms climb 5 → 12 → 22.

**Live-code step 1 — "what should the four counts come to?"** 1,000. At `t = 0.02`: `5 + 211 + 9 + 775 = 1000`. ✅

**Live-code step 2 — "read me the last line, and the warning above it."** `ValueError: not enough values to unpack (expected 4, got 1)`, and the warning says *"use the 'labels' parameter to pass all known labels"* — which is the fix, printed above the traceback.

**Live-code step 3 — "was that an error?"** No. It printed a curve and an AUC and nothing complained.

**Live-code step 3 — "three points. How many thresholds did it find?"** Two useful ones, 1 and 0, plus the `inf` sentinel scikit-learn puts at the front so the curve starts at the origin.

**Live-code step 3 — "where have you seen 0.0140 today?"** It is the fraud rate: 14 ÷ 1000.

**Live-code step 4 — "which chart cares about 211 false alarms?"** The precision-recall curve. On the ROC, 211 ÷ 986 = 0.2140 is a fifth of the way across; on the PR curve, precision goes from 0.3750 to 5 ÷ 216 = 0.0231.

**Activity — "where is this curve steep, and where is it flat?"** Steep between 0.90 and 0.70 (the frauds are stacked at the top of the ranking); flat from 0.30 down to 0.05, where every card added is legitimate.

**Activity — "what would a random model look like?"** It would sit on the diagonal, because flagging at random flags the same *fraction* of each pile.

**Harder variation 1 — "what is the area under the card curve?"** `roc_auc_score(truth, prob)` prints **0.8500**. Counting graph-paper squares carefully gets you to about 0.85.

**Harder variation 3 — "did the model get worse, or the data?"** The model, in the sense that its ranking is now wrong: it is confidently scoring a fraud at 0.05. The data is unchanged. A bad ranker produces a curve that sags towards the diagonal, and no threshold can rescue it.

---

## 🔮 Next Week Preview

Next week the argument stops. Three sticky notes with three defensible thresholds on them is where you end an honest lesson about *description*, and it is a terrible place to end a project — because somebody has to actually choose, and "it depends who you ask" does not deploy. So next week the bank sends over a **price list**: a missed fraud costs **£500**, a false alarm costs **£10**. The moment those two numbers exist, the threshold is not an opinion, it is a multiplication — the class computes the total cost of all nine rows of this week's table, circles the cheapest, and finds that **t = 0.10 costs £5,550** while the default 0.5 costs £7,000. Then the second half asks the question a good student is already itching to ask: *how much do you trust a four-decimal number that rests on fourteen frauds?* Not much.

The fix: **5-fold stratified cross-validation** turns one lucky number into five and reports `AUC = 0.628 ± 0.087`, which is a band wide enough to change your mind. There is one small new piece of maths, and it is the natural partner to this week's: **the area under a curve, added up as trapezoid strips by hand**, on a five-point curve, then checked against `np.trapz` — which is what "AUC" has meant all along.

**To prep early:** four things. **One — do not wipe anything.** The twenty cards, the probability line, the ten-dot graph paper and the nine-row sweep table are all used again, and the cost table is the same nine rows with two extra columns. **Two — write the price list on a card tonight** and keep it in your pocket: `a miss costs £500 · a false alarm costs £10`. Producing it as a physical object at minute 3 is worth more than any slide. **Three — print two sheets of graph paper per student**, because the Trapezoid Race needs a fresh five-point curve drawn from scratch and squared paper is the difference between four strips and a scribble. **Four — divide a whiteboard down the middle** and write `BY HAND` on the left and `np.trapz` on the right; that board is the second activity and it should be waiting when they walk in. Nothing new to install.

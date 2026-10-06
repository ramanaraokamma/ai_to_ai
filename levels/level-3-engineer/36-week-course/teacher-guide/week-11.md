# Week 11 — Fraud Bench: What Does a Mistake Cost?

[⬅ Week 10](week-10.md) · [Course Home](../README.md) · [Week 12 ➡](week-12.md) · [Student Guide](../student-guide/week-11.md) · [Workbook](../workbook/week-11.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟩 Lab — the argument from last week gets settled by multiplication |
| **Big idea** | **You cannot pick a threshold without a price list.** Write down what a miss costs and what a false alarm costs, and the arithmetic picks the threshold for you. |
| **New vocabulary** | cost matrix · expected cost · k-fold cross-validation · stratified k-fold · AUC · error bar |
| **New maths** | **Area under a curve, added up as trapezoid strips by hand** on a five-point curve, then checked against `np.trapz` to four decimal places. This is what "AUC" has meant all along. |
| **New syntax** | `StratifiedKFold(n_splits=5, shuffle=True, random_state=0)` · `cross_val_score(pipe, X, y, cv=skf, scoring="roc_auc")` · `np.trapz(tpr, fpr)` · `scores.mean()` / `scores.std()` |
| **Dataset** | Week 8's `make_classification(n_samples=5000, n_features=8, n_informative=4, n_redundant=0, weights=[0.99, 0.01], random_state=0)` fraud table. **72 frauds in 5,000 rows**; 14 of them in the 1,000 validation rows. **Nothing downloads. No internet needed.** |
| **Materials** | **The price list, written on a card in advance**: `a miss costs £500 · a false alarm costs £10` · **two sheets of squared graph paper per student** · a whiteboard **divided down the middle**, `BY HAND` on the left and `np.trapz` on the right · a calculator each (phones are fine) · printed workbook pages 11.1–11.6 · **last week's nine-row sweep table and ten-dot ROC curve still on the wall** · the Bug Log |
| **Tech needed** | Laptop with Python 3, numpy, scikit-learn. **No new installs.** |
| **Prep time** | 25 minutes the night before · 5 minutes on the day |
| **Expected runtime of the code** | `fraud_bench.py` **about 1 second** — and that includes fitting the model six times, once for the sweep and five more for the folds. |

> **⚠️ Watch out:** two numbers in this lesson **disagree with each other on purpose**, and you must not hide it. The formula says the best threshold is `10 ÷ 510 = 0.0196`. The actual measurement on our data says **0.032**, and the winner among our nine thresholds is **0.10**. That is not an error in the file and not an error in your typing. §5 below explains exactly why they disagree, and the disagreement is the most professionally useful thing in the week — it is what tells you your probabilities are not honest. Read §5 before you teach.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Write an explicit cost matrix** for a stated application and **compute the expected cost at nine thresholds**, showing the arithmetic in full for at least one of them.
2. **Estimate the area under a five-point curve** by adding trapezoid strips by hand, then **match `np.trapz` to three decimal places.**
3. **Run stratified 5-fold cross-validation** and report **mean plus or minus standard deviation** instead of one lucky number.
4. **Say what the plus-or-minus is for**, and what a large one tells you about the data.

Observable evidence: a nine-row cost table with the winner circled and one row's arithmetic written out longhand; four trapezoid strips summed by hand to `0.7000` with `np.trapz` printing the same; the line `AUC = 0.628 ± 0.087 (5-fold stratified CV)` written down; and one sentence explaining what would change if the `±` were three times bigger.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each one carries on from the one above. **The complete runnable file is in the Prep Checklist**, printed once, in full. If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**There is one new piece of maths and it is the area of a shape you learned in about Year 7.** A trapezoid — a rectangle with a sloping top — has area *(the two heights, averaged) × (the width)*. That is all. What needs your twenty minutes is the **second half** of the lesson, because "report mean plus or minus standard deviation" sounds like bureaucratic box-ticking until you have seen our five fold scores, and then it is genuinely alarming.

### 1. Where last week left us, and why it is not good enough

Last week ended beautifully and uselessly. Three sticky notes:

```
t = 0.12   right for the two-person review desk
t = 0.10   right for the manager who signs off the queue
t = 0.02   right for the customer whose money is gone
```

Three good arguments. And you cannot ship three thresholds. Somebody has to pick one, and *"it depends who you ask"* does not deploy.

**The way out is not a better argument. It is a price.** The moment somebody writes down what each kind of mistake costs, the argument stops, because you can multiply.

### 2. The cost matrix, which is the confusion matrix with money in it

> **Cost matrix** — the confusion matrix with a price written in each cell instead of a count.

For our fraud problem, and these are the numbers the bank actually gives you:

| | Predicted legit | Predicted fraud |
|---|---|---|
| **Actually legit** | **£0** — right, and free | **£10** — an analyst reviews it, the customer is mildly annoyed |
| **Actually fraud** | **£500** — the money is gone, plus the chargeback and the investigation | **£0** — caught in time |

![Write down the two prices before you touch the dial](../figures/fig-w11-1-cost-matrix-two-prices.svg)
*Figure 11.1 — Write down the two prices before you touch the dial. Two of the four cells are free; the two mistakes have prices, and the whole lesson is that one price is fifty times the other.*

**The two diagonal cells cost nothing.** Getting it right is free. So the whole cost of running your model is:

```
cost  =  500 × (number of misses)  +  10 × (number of false alarms)
```

> **Expected cost** — the total price of all the mistakes a model makes at a given threshold.

And the sentence that carries the whole week:

> **A missed fraud costs 500 ÷ 10 = 50 false alarms.** So you should be willing to block fifty innocent cards to stop one theft — and not fifty-one.

🍕 **The analogy, and it is worth doing properly because everybody has lived it.** Deciding how early to leave for the airport. Leaving too early costs you an hour of boredom in a departure lounge. Leaving too late costs you the flight, the hotel and the wedding you were flying to. Nobody splits the difference at "a fifty-fifty chance of making it." You weight the two costs, notice that one is about a hundred times worse than the other, and **leave absurdly early.** That is threshold tuning. Every single person in the room already does it, several times a year, without arithmetic.

### 3. The nine rows, costed

Take last week's nine-row sweep table. It already has `fn` and `fp` in it. Multiply and add. This is the real output of `fraud_bench.py`:

```text
--- the price list: a miss costs 500, a false alarm costs 10 ---
   t   fn   fp   500 x fn   10 x fp   total cost
 0.50   14    0       7000         0         7000
 0.15   13    0       6500         0         6500
 0.12   12    0       6000         0         6000
 0.10   11    5       5500        50         5550
 0.08   11   12       5500       120         5620
 0.06   11   22       5500       220         5720
 0.04   10   61       5000       610         5610
 0.02    9  211       4500      2110         6610
 0.01    6  421       3000      4210         7210
cheapest of the nine: t = 0.10 at 5550
```

**Do one row longhand before class**, out loud, because you will do it on the board:

```
t = 0.10   →   11 misses, 5 false alarms

  500 × 11  =  5500
   10 ×  5  =    50
                ----
                5550
```

Four things worth having ready:

**One — there is a bottom, and you can see it.** The costs go 7000, 6500, 6000, **5550**, 5620, 5720, 5610, 6610, 7210. Down, down, down, up, up, down a bit, up, up. **A bowl.** The default threshold of 0.5 costs £7,000; the cheapest of the nine costs £5,550. **Moving one number in a comparison saved £1,450 on a thousand transactions**, and it took no retraining, no new features and no new data.

**Two — the bowl is bumpy, and you must say so.** Look at `t = 0.04`: £5,610, which is *cheaper* than `t = 0.06` at £5,720. The bowl is not smooth. **That bump is not a discovery, it is noise** — the whole table rests on **fourteen** frauds, so one fraud crossing a line moves £500 and wrecks the shape. This bump is the reason the second half of the lesson exists, and pointing at it is the cleanest possible motivation for cross-validation.

![The bowl the price list draws and the cheapest place to cut](../figures/fig-w11-2-expected-cost-curve-with-minimum.svg)
*Figure 11.2 — The bowl the price list draws and the cheapest place to cut. The ringed point is the winner. The red-outlined point is the bump, and the bump is what fourteen frauds look like.*

**Three — the price list is a decision about people, and it does not come from maths.** Somebody decided that a stolen paycheque is worth fifty inconvenienced customers. That person might be wrong. **The arithmetic will faithfully implement whatever value judgement you feed it**, and being explicit about the judgement is the entire ethical content of this lesson. If a student says *"who decided 500?"*, that is the best question of the week and the answer is *"a human being, and you can ask them to justify it, which you could not do when the threshold was 0.5 by default."*

**Four — change the price list and a different row wins.** Have these ready, because somebody will ask, and they are all real:

| a miss costs | a false alarm costs | winner | its cost |
|---|---|---|---|
| £500 | £10 | **t = 0.10** | £5,550 |
| £50 | £10 | **t = 0.12** | £600 |
| £200 | £10 | **t = 0.10** | £2,250 |
| £500 | £100 | **t = 0.12** | £6,000 |
| £5,000 | £10 | **t = 0.01** | £34,210 |

**Make a miss ten times more expensive again (£500 to £5,000) and the winner slides from 0.10 all the way to 0.01** — flag 429 rows out of 1,000 and catch 8 of the 14. That is what "we will accept any amount of hassle to stop this" looks like in arithmetic.

### 4. 🔢 The new maths: area, added up in strips

**This is the week's one new idea. It is the area of a trapezoid and nothing more.**

Draw a curve on graph paper. You want the area of the space underneath it. The curve is curved, so you cannot use a rectangle. But you *can* chop the space into vertical strips, and each strip is very nearly a **trapezoid** — a rectangle with a sloping top.

> **🔢 The maths, slowly:** the area of one strip is **(the left-hand height + the right-hand height) ÷ 2, times the width.** You average the two heights to get "the average height of this strip", then multiply by how wide it is, exactly as you would for a rectangle.

Here is the five-point curve the class will use, and all four strips worked out. **Every number below was printed by a machine.**

```
the five points:   (0.00, 0.00)  (0.25, 0.60)  (0.50, 0.80)  (0.75, 0.90)  (1.00, 1.00)

strip 1: (0.00 + 0.60) / 2 x 0.25 = 0.0750
strip 2: (0.60 + 0.80) / 2 x 0.25 = 0.1750
strip 3: (0.80 + 0.90) / 2 x 0.25 = 0.2125
strip 4: (0.90 + 1.00) / 2 x 0.25 = 0.2375
by hand   : 0.7000
np.trapz  : 0.7000
```

**0.7000 both ways, exactly.** Do all four strips yourself on paper tonight. They are four averages and four multiplications by 0.25, and if you have done them once you can teach this segment with your hands in your pockets.

![Area, added up in four strips](../figures/fig-w11-3-trapezoid-strips-under-a-curve.svg)
*Figure 11.3 — Area, added up in four strips. Each strip's arithmetic printed beside it, and the four answers added up.*

Now the reveal, and it is the point of teaching this at all:

```text
np.trapz(tpr, fpr)  : 0.6116
roc_auc_score       : 0.6116
```

> **AUC (area under the ROC curve)** — one number summarising a whole ROC curve: the area of the space underneath it. A coin's curve is the diagonal, whose area is exactly 0.5. A perfect curve goes through the top-left corner and has area 1.

**`roc_auc_score`, which they have been typing since Week 2, is trapezoid strips.** It always was. There is no other machinery in it. That is a genuinely satisfying thing to be able to tell a fourteen-year-old: *"the thing you have been trusting for nine weeks is the shape you learned to find the area of in Year 7, done 27 times and added up."*

**Two warnings you will need.**

`np.trapz(y, x)` takes the **heights first and the positions second** — the opposite order from how you would say it. Get it backwards and you get a plausible wrong answer with no error:

```
right way   np.trapz(ys, xs) : 0.7000
wrong way   np.trapz(xs, ys) : 0.3000
```

**0.3000, which is 1 − 0.7000.** It is the area to the *left* of the curve instead of underneath it. No warning, no crash.

And `np.trapz` assumes your x values go **in increasing order**. Shuffle two of them and you get nonsense — on our five points, swapping 0.25 and 0.50 gives **0.6375** instead of 0.7000.

### 5. Theory and measurement disagree, and that is a diagnosis

There is a formula for the best threshold, and it is short enough to derive on the board without algebra if you want to. Ask: *when is it worth flagging a transaction?* You flag it, and:

- if it was legit — which happens with probability `1 − p` — you pay `£10`
- if you had *not* flagged it and it was fraud — probability `p` — you would have paid `£500`

Flagging becomes worthwhile exactly when the expected cost of flagging drops below the expected cost of not flagging, and that crossover sits at:

```
t*  =  cost of a false alarm  ÷  (cost of a false alarm + cost of a miss)

    =  10 ÷ (10 + 500)  =  10 ÷ 510  =  0.0196
```

**So the formula says 0.0196.** And our measured minimum, from a 99-point sweep, says:

```text
cheapest of the 99 : t = 0.032 at 5420
the formula says   : t = 10 / (10 + 500) = 0.0196
```

**0.032 against 0.0196. They disagree by about a factor of one and a half.** Do not paper over this. There are exactly two honest explanations and you should give both:

**One — the formula assumes the probabilities are honest.** It only works if a row the model scores 0.02 really does turn out to be fraud about 2% of the time. A model whose probabilities can be read as real chances is called **calibrated**. Ours top out at 0.1774, but that alone proves nothing (fraud is 1.4% of rows, so small scores are what an honest model should print): the 1,000 validation scores sum to 14.1 and there were 14 frauds, so on average the model is about right. Whether each individual score is honest, 14 frauds cannot tell us; repairing a model that is not is a Level 4 topic. **When the formula and the sweep agree, that is mild evidence your probabilities are trustworthy. When they disagree, it is a prompt to check them** — but with 14 frauds the gap may be mostly noise, so it is a question raised, not a diagnosis proved.

**Two — the measurement is resting on fourteen frauds.** The whole cost curve is built from 14 positive rows. One fraud landing on the other side of a threshold moves the cost by £500, which is more than the gap between several neighbouring rows. **The minimum of a bumpy curve measured on 14 events is not a precise quantity.** Which brings us, directly, to the second half.

> **🧑‍🏫 If a student asks** *"so which one do we use?"* — Both, and you say so out loud in your report. The formula gives you the answer for a perfectly honest model; the sweep gives you the answer for the model you actually have. **When they agree, ship. When they disagree, you have a question about your model to chase** — and knowing to ask it is worth more than the threshold.

### 6. One number is not a measurement

Last week produced `roc_auc_score = 0.6116`. How much should anyone trust that?

Here is the test that settles it. Change nothing about the model, nothing about the features, nothing about the code — **just chop the data into five pieces a different way**, and see what the number does.

> **k-fold cross-validation** — chop the data into *k* equal chunks. Train on *k*−1 of them and score on the one left out. Repeat *k* times so every row is in the held-out chunk exactly once. Report the mean of the *k* scores **and how much they wobble.**

> **Stratified k-fold** — the same thing, but each chunk is built to hold the same proportion of the rare class as the whole dataset. **Non-negotiable when the positive class is rare.**

**Why stratification is not optional here.** Real output:

```text
frauds per test fold, StratifiedKFold : [14, 14, 14, 15, 15]
frauds per test fold, plain KFold     : [11, 17, 14, 17, 13]
```

Both add to 72 — that is all the frauds in the dataset. But look at the plain version: one chunk got **11** frauds and another got **17**. That is a **55% difference** in how many frauds there were to find. So if the five scores now come out different from each other, you have no way of knowing whether that is the model being unstable or one chunk simply having had an easier job. **Stratification removes one of the two explanations**, and when you are trying to diagnose something, removing an explanation is the whole game.

And now the five scores. **This is the most important block of output in the week:**

```text
the five AUCs : [0.6183 0.5909 0.6873 0.7504 0.4954]
mean 0.6285   sd 0.0867
report it as  : AUC = 0.628 +/- 0.087 (5-fold stratified CV)
```

**Read those five numbers slowly.** One fold said **0.7504** — a decent model. Another fold said **0.4954** — worse than a coin. **Same model. Same code. Same seed. The only difference is which 1,000 rows it was scored on.**

The mean, worked out longhand because you will do it on the board:

```
0.6183 + 0.5909 + 0.6873 + 0.7504 + 0.4954  =  3.1423

3.1423 ÷ 5  =  0.62846   →   0.6285
```

> **Error bar** — the `±` you print beside a mean. It says how much the number moves when you measure the same thing again a slightly different way.

![Five folds, five scores, one honest number](../figures/fig-w11-4-five-folds-five-scores-one-error-bar.svg)
*Figure 11.4 — Five folds, five scores, one honest number. Five held-out chunks on the left, the five scores they produced on the right, and the mean worked out underneath.*

**What the ± is for, in one sentence:** *it is a rule of thumb for how big a difference between two models to trust: a difference smaller than the spread is unproven, and a difference well outside it is worth taking seriously.* (It is the spread of single-fold scores; the sharper test is to score both models on the same folds.)

That is the whole answer to objective 4, and here is how to make it concrete:

- Our band is **0.628 ± 0.087**, so roughly **0.54 to 0.72**.
- Somebody hands you a new model scoring **0.65**. Is it better? **You cannot tell from this.** 0.65 is inside your band. It might be the same model on a luckier split.
- Somebody hands you a model scoring **0.85**. **Now you can talk**, because 0.85 is well outside the band.

🍕 **The analogy.** Weighing yourself. If the scale reads 60 kg ± 0.2 kg, you can detect a 1 kg change and a diet that claims 1 kg is checkable. If it reads 60 kg ± 3 kg, a 1 kg change is invisible and **any claim about 1 kg is unmeasurable with that equipment.** The equipment did not lie to you; you just cannot ask it that question.

**And what a large ± tells you about the data.** Three things, in order of how often they are the answer:

1. **The held-out chunks are too small for the thing you are measuring.** 14 positives is 14. Every score is coarse.
2. **The model is genuinely unstable** — small changes in the training rows move it a lot.
3. **The data is not homogeneous** — some chunks contain a genuinely different kind of row. (For us it is overwhelmingly reason 1.)

> **⚠️ Watch out:** cross-validation **replaces the validation set, not the test set.** The test pile is still opened exactly once, at the very end, exactly as in Week 2. If a student cross-validates over `X` including the test rows and then reports the result as a test score, that is leakage with extra steps. Say it out loud.

### 7. Every line of this week's code, explained to someone who has never programmed

```python
COST_FN = 500
COST_FP = 10
```
Two named numbers at the top of the file. **Putting the price list in capital letters at the top is not decoration** — it is how somebody reading your code in a year finds out what value judgement is buried in it.

```python
cost = COST_FN * fn + COST_FP * fp
```
Multiply, multiply, add. `fn` and `fp` came out of the confusion matrix, exactly as in Week 8.

```python
if best_cost is None or cost < best_cost:
```
*"If I have not seen any cost yet, or this one is cheaper than the cheapest so far, remember it."* `None` is Python's word for "nothing here yet". This is how you find a minimum without sorting anything.

```python
for t in np.arange(0.002, 0.200, 0.002):
```
`np.arange(start, stop, step)` makes a list of numbers from `start` up to (but not including) `stop`, going up in jumps of `step`. So this is 0.002, 0.004, 0.006, … 0.198 — **99 thresholds instead of nine.**

```python
np.trapz(ys, xs)
```
Area under the curve defined by heights `ys` at positions `xs`, by trapezoid strips. **Heights first.** See the warning in §4.

```python
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
```
Build the chopping machine. `n_splits=5` is five chunks. `shuffle=True` mixes the rows before chopping — **leave it out and you cut the data in the order it happens to be stored, which is a real bug on any dataset that was sorted by anything.** `random_state=0` makes the shuffle reproducible.

```python
[int(y[te].sum()) for tr, te in skf.split(X, y)]
```
`skf.split(X, y)` hands back five pairs: for each fold, the row numbers to train on (`tr`) and the row numbers to score on (`te`). `y[te]` picks out just the held-out labels, and `.sum()` counts the 1s in them — that is *"how many frauds are in this chunk"*.

```python
scores = cross_val_score(pipe, X, y, cv=skf, scoring="roc_auc")
```
The whole of cross-validation in one line. It **refits the pipeline from scratch inside every fold** — that is the entire reason the pipeline has to be a `Pipeline` and not a scaler applied earlier. `scoring="roc_auc"` says which number to compute. **Leave `scoring` out and you get accuracy**, which on 1.4% fraud prints five 0.98s and tells you nothing. `scores` comes back as a numpy array of five numbers.

```python
scores.mean(), scores.std()
```
The average and the wobble. **`.std()` on a numpy array gives the *population* standard deviation** — it divides by 5, not by 4. If a student's answer is 0.0969 instead of 0.0867 they have used `ddof=1` from a statistics class; both conventions exist, ours is numpy's default, and it does not change any conclusion. Say that and move on.

### 8. The three misconceptions you will actually meet

**"The cheapest threshold is the best threshold."** It is the cheapest *under this price list*. Change £500 to £50 and 0.12 wins instead. **The threshold is downstream of a value judgement**, and pretending the arithmetic made the judgement is the most common professional dishonesty in the field.

**"Cross-validation makes the model better."** It does not touch the model. **It makes the measurement better.** The model that comes out of `cross_val_score` is thrown away — five models get fitted and five die. What survives is five numbers.

**"A bigger ± means a worse model."** No — it means a **noisier measurement**. Our ± of 0.087 is mostly a statement about having 14 positives per fold, not about the model. Fix it by getting more data (more positives per fold), not by changing the model. More folds do not add positives.

### 9. How deep to go, and where to stop

| Idea | Verdict |
|---|---|
| The area under a curve as a **limit** of thinner and thinner strips | **No.** Four strips, added up, checked against `np.trapz`. That is the whole treatment in this course. |
| Integration, antiderivatives, ∫ | **Not in Level 3 at all.** If a student has met it, tell them they are right and this is the numerical version, which is what a computer does anyway. |
| The slope at **one** point of the cost curve | **Next week**, and it is the mirror image of this week — area is adding strips up, slope is dividing two differences. Do not preview the arithmetic. |
| Confidence intervals, t-tests, "is 0.65 significantly different from 0.628" | Name the question, refuse the machinery. *"There is a proper way to answer that and it is a statistics course."* The `±` is enough. |
| `RepeatedStratifiedKFold`, nested CV, `GridSearchCV` | **Not in Level 3.** One lever per week. |
| Calibration, `CalibratedClassifierCV` | Name it in §5 because the theory/measurement gap demands it. **Do not teach it.** |
| Cost-sensitive training (`class_weight`, `sample_weight`) | **Not in this course.** It is a second lever on the same problem. |

---

### 10. 🧭 The Growing Map — where Week 11 sits

The student guide carries the same figure every week with one more piece filled in. Today it earns its
keep twice: **stage two finishes**, and the figure is about to change character next week.

![The Level 3 pipeline in Week 11: the threshold and cost tile closes with a price list and five folds](../figures/fig-w11-0-where-this-fits.svg)

*Figure 11.0 — Week 11's version. The last unfinished box in stages one and two is gold. After today
there is not a dashed line left in either stage. The ↻ on stage three is drawn grey for the last time —
it turns black next week.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it, don't explain it.** Ask *"which box did we do today?"* They point at the gold tile —
   *threshold · cost* — and it is the same box as last week, now being closed. Pointing is the exercise.
2. **Then the question that belongs to this week.** Hold up the price-list card —
   `a miss costs £500 · a false alarm costs £10` — and ask *"which box on the map was that card for?"*
   The one that just went gold, and it is the only card all term with money on it. Then the second half,
   pointing at `AUC = 0.628 ± 0.087` on the board: *"and the plus-or-minus — same box, or a different
   one?"* Same box. Stage two is where a number stops being **a** number.
3. **Then count the dashes.** Ask them to find a dashed line inside stage one or stage two. There isn't
   one. *"Everything left on this map is about building the thing that learns."* That is the last thing
   you say about Term 1.

> **🧑‍🏫 Why this is worth two minutes.** A learner who can see the map can distinguish *"I don't
> understand this week"* from *"I don't know where this week goes"* — and at a stage boundary it also
> gives the class a real sense of having finished something, which is hard to manufacture any other way.

**Two things to notice, so you can answer if asked.**

- **Evaluation and impact are lit together.** Evaluation for the five folds and the `±`. Impact for the
  cost matrix, which is the most honest document in this course: somebody writing down in pounds whose
  bad day matters more. §2 is where that lands, and this is where you name it.
- **The ↻ on stage three is grey for the last time.** It is the training loop, and **next week the symbol
  turns black** and stays black. Promise it out loud — it is a genuinely good cliffhanger, and it costs
  you nothing to give away because the *how* takes six weeks.

> **⚠️ Watch out:** the map is orientation, not assessment. Never quiz them on it. And resist finishing
> the lesson on the AUC number — finish it on the price list, which is the only idea in the week that
> nobody can look up.

---

## 🧰 Prep Checklist

### 25 minutes the night before

- [ ] **Write the price list on a card.** One card, big letters, in your pocket:

```
   a missed fraud  ...........  £500
   a false alarm   ...........   £10
```

**Producing that as a physical object at minute 3 is worth more than any slide.** It is the moment the lesson turns.

- [ ] **Do the four trapezoid strips yourself, on paper.** Not on a calculator app — on paper, four lines:

```
(0.00 + 0.60) ÷ 2 × 0.25 = 0.30 × 0.25 = 0.0750
(0.60 + 0.80) ÷ 2 × 0.25 = 0.70 × 0.25 = 0.1750
(0.80 + 0.90) ÷ 2 × 0.25 = 0.85 × 0.25 = 0.2125
(0.90 + 1.00) ÷ 2 × 0.25 = 0.95 × 0.25 = 0.2375
                                          ------
                                          0.7000
```

- [ ] **Do one cost row longhand.** `500 × 11 = 5500`, `10 × 5 = 50`, `5500 + 50 = 5550`. **Say the £5,550 out loud once.**

- [ ] **Add the five fold scores up by hand.** `0.6183 + 0.5909 + 0.6873 + 0.7504 + 0.4954 = 3.1423`, then `3.1423 ÷ 5 = 0.6285`. You will do this on the board and a student will check you with a phone.

- [ ] **Type and run `fraud_bench.py` yourself.** The complete file:

```python
"""fraud_bench.py - a price list picks the threshold.  Week 11."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve
from sklearn.model_selection import (KFold, StratifiedKFold, cross_val_score,
                                    train_test_split)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

COST_FN = 500          # a missed fraud
COST_FP = 10           # a false alarm

# ------------------------------------------------------------- 1. THE DATA
X, y = make_classification(n_samples=5000, n_features=8, n_informative=4,
                           n_redundant=0, weights=[0.99, 0.01], random_state=0)
X_tmp, X_test, y_tmp, y_test = train_test_split(
    X, y, test_size=0.20, random_state=0, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(
    X_tmp, y_tmp, test_size=0.25, random_state=0, stratify=y_tmp)
model = LogisticRegression(max_iter=2000, random_state=0).fit(X_train, y_train)
prob = model.predict_proba(X_val)[:, 1]

# ----------------------------------------------------- 2. THE PRICE LIST
print("--- the price list: a miss costs %d, a false alarm costs %d ---"
      % (COST_FN, COST_FP))
print("   t   fn   fp   500 x fn   10 x fp   total cost")
best_t = None
best_cost = None
for t in [0.50, 0.15, 0.12, 0.10, 0.08, 0.06, 0.04, 0.02, 0.01]:
    pred = (prob >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_val, pred, labels=[0, 1]).ravel()
    cost = COST_FN * fn + COST_FP * fp
    if best_cost is None or cost < best_cost:
        best_t = t
        best_cost = cost
    print("%5.2f %4d %4d %10d %9d %12d"
          % (t, fn, fp, COST_FN * fn, COST_FP * fp, cost))
print("cheapest of the nine: t = %.2f at %d" % (best_t, best_cost))

# ------------------------------------------------------ 3. A FINER SWEEP
print()
print("--- a finer sweep: 99 thresholds, every 0.002 ---")
fine_t = None
fine_cost = None
for t in np.arange(0.002, 0.200, 0.002):
    pred = (prob >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_val, pred, labels=[0, 1]).ravel()
    cost = COST_FN * fn + COST_FP * fp
    if fine_cost is None or cost < fine_cost:
        fine_t = t
        fine_cost = cost
print("cheapest of the 99 : t = %.3f at %d" % (fine_t, fine_cost))
print("the formula says   : t = %d / (%d + %d) = %.4f"
      % (COST_FP, COST_FP, COST_FN, COST_FP / (COST_FP + COST_FN)))

# ------------------------------------------------- 4. AREA, IN FOUR STRIPS
print()
print("--- area under a five-point curve ---")
xs = np.array([0.00, 0.25, 0.50, 0.75, 1.00])
ys = np.array([0.00, 0.60, 0.80, 0.90, 1.00])
total = 0.0
for i in range(4):
    strip = (ys[i] + ys[i + 1]) / 2 * (xs[i + 1] - xs[i])
    total = total + strip
    print("strip %d: (%.2f + %.2f) / 2 x %.2f = %.4f"
          % (i + 1, ys[i], ys[i + 1], xs[i + 1] - xs[i], strip))
print("by hand   : %.4f" % total)
print("np.trapz  : %.4f" % np.trapz(ys, xs))

print()
print("--- the same trick on our own ROC curve ---")
fpr, tpr, thr = roc_curve(y_val, prob)
print("np.trapz(tpr, fpr)  : %.4f" % np.trapz(tpr, fpr))
print("roc_auc_score       : %.4f" % roc_auc_score(y_val, prob))

# ----------------------------------------------------------- 5. FIVE FOLDS
print()
print("--- five folds instead of one lucky split ---")
pipe = Pipeline([("scaler", StandardScaler()),
                 ("model", LogisticRegression(max_iter=2000, random_state=0))])
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
kf = KFold(n_splits=5, shuffle=True, random_state=0)
print("frauds per test fold, StratifiedKFold :",
      [int(y[te].sum()) for tr, te in skf.split(X, y)])
print("frauds per test fold, plain KFold     :",
      [int(y[te].sum()) for tr, te in kf.split(X, y)])
scores = cross_val_score(pipe, X, y, cv=skf, scoring="roc_auc")
print("the five AUCs :", np.round(scores, 4))
print("mean %.4f   sd %.4f" % (scores.mean(), scores.std()))
print("report it as  : AUC = %.3f +/- %.3f (5-fold stratified CV)"
      % (scores.mean(), scores.std()))
```

Run `python3 fraud_bench.py`. You must see **exactly** this:

```text
--- the price list: a miss costs 500, a false alarm costs 10 ---
   t   fn   fp   500 x fn   10 x fp   total cost
 0.50   14    0       7000         0         7000
 0.15   13    0       6500         0         6500
 0.12   12    0       6000         0         6000
 0.10   11    5       5500        50         5550
 0.08   11   12       5500       120         5620
 0.06   11   22       5500       220         5720
 0.04   10   61       5000       610         5610
 0.02    9  211       4500      2110         6610
 0.01    6  421       3000      4210         7210
cheapest of the nine: t = 0.10 at 5550

--- a finer sweep: 99 thresholds, every 0.002 ---
cheapest of the 99 : t = 0.032 at 5420
the formula says   : t = 10 / (10 + 500) = 0.0196

--- area under a five-point curve ---
strip 1: (0.00 + 0.60) / 2 x 0.25 = 0.0750
strip 2: (0.60 + 0.80) / 2 x 0.25 = 0.1750
strip 3: (0.80 + 0.90) / 2 x 0.25 = 0.2125
strip 4: (0.90 + 1.00) / 2 x 0.25 = 0.2375
by hand   : 0.7000
np.trapz  : 0.7000

--- the same trick on our own ROC curve ---
np.trapz(tpr, fpr)  : 0.6116
roc_auc_score       : 0.6116

--- five folds instead of one lucky split ---
frauds per test fold, StratifiedKFold : [14, 14, 14, 15, 15]
frauds per test fold, plain KFold     : [11, 17, 14, 17, 13]
the five AUCs : [0.6183 0.5909 0.6873 0.7504 0.4954]
mean 0.6285   sd 0.0867
report it as  : AUC = 0.628 +/- 0.087 (5-fold stratified CV)
```

**Expected runtime: about 1 second.** That includes fitting the model six times. If `the five AUCs` are not those five numbers, check `shuffle=True` and `random_state=0` on the `StratifiedKFold`.

- [ ] **Break it on purpose, twice, so you have seen both live.**
  1. `cross_val_score(pipe, X, y, cv=skf)` with `scoring=` deleted. **No error.** You get `[0.986 0.986 0.986 0.985 0.985]` — five almost identical, beautiful, meaningless numbers. This is deliberate mistake one and it is a returning villain.
  2. `np.trapz(xs, ys)` with the arguments swapped. **No error.** You get `0.3000` instead of `0.7000`. This is deliberate mistake two.

- [ ] **Print workbook pages 11.1–11.6.**
- [ ] **Divide a whiteboard down the middle** with a vertical line. `BY HAND` on the left, `np.trapz` on the right. **That board is the Trapezoid Race and it should be waiting when they walk in.**
- [ ] **Two sheets of squared graph paper per student.** One for the five-point curve, one spare.
- [ ] **Check last week's artifacts are still up:** the nine-row sweep table and the ten-dot ROC curve. **You will add two columns to the first one and measure the area of the second one.**
- [ ] **A calculator each.** Phones are fine. There are about forty divisions in this lesson and mental arithmetic is not the objective.

### 5 minutes on the day

- [ ] Terminal in the working folder. **`fraud_bench.py` deleted or renamed** — they type it.
- [ ] The price-list card in your pocket, **not** on the board yet.
- [ ] Board divided, `BY HAND` and `np.trapz` written.
- [ ] Graph paper out, two sheets per student.
- [ ] Last week's sweep table on the wall, with two blank columns ruled on the right.
- [ ] Workbook 11.1 out. Nothing filled in.
- [ ] Bug Log open at a fresh page.

### Fallback if the laptops fail

**Objectives 1, 2 and 4 survive completely intact with no computer**, and objective 3 survives as a hand-drawn diagram plus five numbers read off this page.

1. **The cost table, entirely on paper.** Last week's nine-row table is on the wall and already has `fn` and `fp` in it. Two multiplications and one addition per row: eighteen multiplications and nine additions, about eight minutes with calculators. **Objective 1, complete**, and honestly better on paper — the winner is more satisfying when you circle it with a pen.
2. **The Trapezoid Race, exactly as planned.** Five points on graph paper, four strips, four averages, four multiplications. **Objective 2 needs no electricity at all**, and the `np.trapz` side of the board can just be this page's `0.7000`.
3. **Cross-validation as a paper diagram.** Draw five rows of five boxes, shade a different box in each row, and write the five AUCs from this page beside them: 0.6183, 0.5909, 0.6873, 0.7504, 0.4954. Add them up, divide by five. **The whole insight is that 0.7504 and 0.4954 came from the same model**, and that lands just as hard from a page as from a screen.
4. **The ± question is a writing task.** Objective 4 needs a pen.

| If this fails | Do this instead |
|---|---|
| `the five AUCs` are different from this file | `shuffle=True` or `random_state=0` missing from `StratifiedKFold`. Without `shuffle` you get `[0.7349 0.6389 0.6484 0.5851 0.648]`, mean 0.6511, sd 0.0481 — **a different chop, so a different answer** (the sd alone wanders from about 0.03 to 0.12 across shuffle seeds, so neither is "the" right sd). |
| `AttributeError: 'list' object has no attribute 'mean'` | `scores` was built by hand as a Python list. Wrap it: `np.array(scores).mean()`. `cross_val_score` gives you a numpy array already. |
| The five scores come out `[0.986 …]` | `scoring="roc_auc"` is missing. **Deliberate mistake one arriving by accident, which is fine — teach it there and then.** |
| The trapezoid total is 0.3000 | `np.trapz` arguments are the wrong way round. Heights first. |
| `nan` appears among the fold scores | A fold with no frauds in it — plain `KFold` on a small slice. `UndefinedMetricWarning: Only one class is present in y_true.` **Use `StratifiedKFold`. This is exactly what it is for.** |
| A student's `sd` reads 0.0969 | They used `ddof=1`. Both conventions exist; numpy's default divides by 5. **No conclusion changes.** Say so and move on. |
| The lab is running long | **Cut the 99-threshold fine sweep, never the nine-row table.** The fine sweep is the setup for the theory/measurement disagreement, which is a discussion, not an objective. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — The Card From the Bank | 7 | 7 | The price list appears; the argument ends |
| 🧠 Concept & Maths — Four Strips | 18 | 25 | The cost bowl on the board, then trapezoids |
| 💻 Live-Code Together — `fraud_bench.py` | 18 | 43 | Costs, area, five folds. **Two deliberate mistakes.** |
| 🎲 Their Turn — Fraud Bench + The Trapezoid Race | 20 | 63 | Build it, then race the machine to 3 dp |
| 🔑 Wrap & Assign | 7 | 70 | Three checks, the ± sentence, homework |

---

### 🪝 Hook — The Card From the Bank (7 minutes)

**Do this:** Point at last week's three sticky notes, still on the wall. Read all three out loud, in a slightly bored voice.

**Say this:**

> "Three thresholds. Three good arguments. And that is where we stopped, and it is a completely useless place to stop, because on Monday morning somebody has to type one number into the system and **you cannot type three.**
>
> So we did what people do when they cannot decide. We had an opinion each."

**Do this:** Take the price-list card out of your pocket. Hold it up. Read it out slowly. Then tape it to the board.

```
   a missed fraud  ...........  £500
   a false alarm   ...........   £10
```

**Say this:**

> "This came from the bank this morning. Two numbers. Somebody who is not a machine-learning person sat down and worked out what each kind of mistake actually costs them — the money gone, the chargeback, the investigation on one side; an analyst's ten minutes and a mildly annoyed customer on the other.
>
> **And the moment those two numbers exist, the argument is over.** Not because I won it. Because there is nothing left to argue about."

**Ask this:** "How many false alarms is one missed fraud worth?"

*Hoped-for answer:* fifty.

*If nobody answers:* write `500 ÷ 10` on the board and wait.

> "**Fifty.** So we should be willing to block fifty innocent cards to stop one theft. Fifty. And **not fifty-one.** That is not an opinion any more, that is arithmetic, and by the end of the hour you will have done it for all nine of last week's thresholds and circled the winner."

**Ask this:** "Before we compute anything — put your hand up if you think the cheapest threshold will be the lowest one on the table, 0.01, or somewhere in the middle."

Take a show of hands and **write the count on the board.** They will mostly say 0.01, because a miss is fifty times worse. **They will be wrong, and the fact that they were wrong is worth ten minutes at the end.** The winner is 0.10, right in the middle, because the false alarms pile up much faster than the frauds get caught.

---

### 🧠 Concept & Maths — Four Strips (18 minutes)

**Step 1 (7 min) — the cost table, on last week's board.**

**Do this:** Go to last week's nine-row table on the wall. Rule two extra columns on the right and head them `500 × misses` and `10 × false alarms`. Then do the **first** row with the whole room, out loud.

```
t = 0.50    misses 14    false alarms 0

    500 × 14  =  7000
     10 ×  0  =     0
                  ----
    total     =  7000
```

**Say this:**

> "Seven thousand pounds. That is what the default threshold — the one that came in the box, the one nobody chose — costs the bank on a thousand transactions. Because it flags nothing, so it misses all fourteen, and fourteen times five hundred is seven thousand."

**Do this:** Hand out the rows. **Two students per row, calculators out, three minutes.** They fill in the board themselves. Your job is to walk round and check the multiplications.

The finished board:

![The cost board, with the winner circled](../figures/fig-w11-5-board-the-cost-table.svg)
*Figure 11.5 — The cost board, with the winner circled. Nine rows, two multiplications and one addition each, and one row cheaper than all the others.*

**Ask this:** "Which row is cheapest?"

*Hoped-for answer:* `t = 0.10`, at £5,550.

**Do this:** Circle it. Then write the saving underneath:

```
7000 − 5550  =  1450
```

> "**One thousand four hundred and fifty pounds**, on a thousand transactions, saved by changing one number in a comparison. No retraining. No new data. No new features. Nobody touched the model."

**Ask this — and go back to the show of hands:** "Most of you guessed the winner would be near 0.01. Why is it not?"

*Hoped-for answer:* because there are so many false alarms down there.

> "At 0.01 you catch eight frauds instead of three — five more, worth two and a half thousand pounds. And you buy **four hundred and twenty-one** false alarms to do it, at ten pounds each, which is four thousand two hundred and ten. **You spent four thousand to save two and a half.** A miss being fifty times worse than a false alarm does not help you when there are eighty times as many false alarms."

**Ask this:** "Look at `t = 0.04`. It costs £5,610. What is odd about that?"

*Hoped-for answer:* it is cheaper than 0.06 above it, so the bowl is not smooth.

> "The bowl has a bump in it. **And that bump is the entire reason for the second half of this lesson**, so hold on to it."

**Step 2 (8 min) — 🔢 the new maths: area in strips.**

**Do this:** Fresh graph paper on the wall. Plot these five points and join them with straight lines. **Say the coordinates out loud as you plot.**

```
(0.00, 0.00)   (0.25, 0.60)   (0.50, 0.80)   (0.75, 0.90)   (1.00, 1.00)
```

**Say this:**

> "I want the area of the space underneath that. And I cannot use a rectangle, because the top is not flat.
>
> But look what happens if I chop it into four vertical slices."

**Do this:** Draw the three vertical lines at 0.25, 0.50 and 0.75. Shade the four strips.

**Ask this:** "What shape is each slice?"

*Hoped-for answer:* a rectangle with a slanted top. Accept "trapezium", "trapezoid", or a hand gesture.

> "A rectangle with a sloping top. And you already know its area, from Year 7: **average the two heights, times the width.** That is it. You are pretending the slice is a rectangle whose height is halfway between the left edge and the right edge — and because the top is a straight line, that is not an approximation at all. **It is exactly right.**"

**Do this:** Work strip 1 on the board, slowly, every step:

```
strip 1:   left height 0.00,  right height 0.60,  width 0.25

           (0.00 + 0.60) ÷ 2  =  0.60 ÷ 2  =  0.30      <- average height
            0.30 × 0.25       =  0.0750                 <- times the width
```

**Do this:** Hand out strips 2, 3 and 4 — one per group, two minutes, calculators.

```
strip 2:   (0.60 + 0.80) ÷ 2 × 0.25  =  0.70 × 0.25  =  0.1750
strip 3:   (0.80 + 0.90) ÷ 2 × 0.25  =  0.85 × 0.25  =  0.2125
strip 4:   (0.90 + 1.00) ÷ 2 × 0.25  =  0.95 × 0.25  =  0.2375
```

**Ask this:** "Add the four up."

```
0.0750 + 0.1750 + 0.2125 + 0.2375  =  0.7000
```

> "**Nought point seven, exactly.** Write it on the left half of the board, under `BY HAND`. In fifteen minutes a computer is going to write a number on the right half, and if the two numbers do not match to three decimal places, somebody in this room has made an arithmetic mistake and we are going to find it."

**Step 3 (3 min) — name the three things.**

Blockquote each on the board.

> **Cost matrix** — the confusion matrix with a price in each cell instead of a count. Ours: £0, £10, £500, £0.

> **Expected cost** — the total price of the mistakes a model makes at a given threshold. `500 × misses + 10 × false alarms`.

> **AUC** — the area under the ROC curve, one number for the whole curve. **A coin's curve is the diagonal, and the area of half a unit square is exactly 0.5.**

**Ask this:** "The diagonal splits the square in half. So what is a coin's AUC?"

*Hoped-for answer:* 0.5.

> "Half. And that is where 'a coin gets 0.5' came from, which I told you last week and did not explain. **It is not a convention. It is the area of a triangle.**"

---

### 💻 Live-Code Together — `fraud_bench.py` (18 minutes)

**You never touch their keyboard.** They type; you type the same thing on the shared screen.

**Step 1 (5 min) — the price list, in code.**

New file, `fraud_bench.py`. Everything down to `cheapest of the nine`. (Full text in the Prep Checklist.)

> **Say this:** "Notice the first two lines after the imports. `COST_FN = 500` and `COST_FP = 10`, in capitals, at the top of the file. **Capitals mean 'this is a setting, not a variable'.** And putting them at the top means that in a year, somebody reading this file can find the value judgement inside it in four seconds instead of never."

Run it. Real output:

```text
--- the price list: a miss costs 500, a false alarm costs 10 ---
   t   fn   fp   500 x fn   10 x fp   total cost
 0.50   14    0       7000         0         7000
 0.15   13    0       6500         0         6500
 0.12   12    0       6000         0         6000
 0.10   11    5       5500        50         5550
 0.08   11   12       5500       120         5620
 0.06   11   22       5500       220         5720
 0.04   10   61       5000       610         5610
 0.02    9  211       4500      2110         6610
 0.01    6  421       3000      4210         7210
cheapest of the nine: t = 0.10 at 5550
```

**Ask this:** "Does that match the board?"

It does, row for row. **Let them check three rows against their own handwriting before you move on.** That agreement is worth thirty seconds of silence.

Now add the fine sweep and run again:

```text
--- a finer sweep: 99 thresholds, every 0.002 ---
cheapest of the 99 : t = 0.032 at 5420
the formula says   : t = 10 / (10 + 500) = 0.0196
```

> **Say this:** "Two new numbers and they do not agree with each other, and they do not agree with our winner either.
>
> With ninety-nine thresholds instead of nine, the cheapest is **0.032**, costing **£5,420** — a hundred and thirty pounds better than our 0.10. Fine: a finer search found a slightly better spot. That is not surprising.
>
> But then there is a **formula**. `10 ÷ 510 = 0.0196`. And it says the answer should be 0.0196, and the actual measurement says 0.032. **Those are different by about half again.**"

**Ask this:** "Which one is wrong?"

*Hoped-for answer:* somebody will guess. Take all guesses seriously.

> **Say this:** "Neither of them is wrong, and this is the most professionally useful two minutes of the lesson.
>
> The formula assumes the model's probabilities are **honest** — that a row scored 0.02 really is fraud about two times in a hundred. Whether ours are honest, I can only partly say. The highest score in the whole file is 0.1774, but that is what you would expect when fraud is 1.4% of rows; and the thousand scores add up to 14.1 when there were 14 frauds, so on average they are about right. What 14 frauds cannot tell me is whether each score is right.
>
> **When the formula and the measurement agree, that is mild evidence your probabilities can be trusted. When they disagree, like now, that is a prompt to check them** — and with only fourteen frauds, much of this gap is probably noise. It has a name — **calibration** — and it is not on this year's menu. But noticing it is."

**Step 2 (4 min) — 🐞 DELIBERATE MISTAKE TWO: the area, backwards.**

> **Say this:** "Right. The area. numpy has this."

Type the area section, but **with the arguments swapped**:

```python
xs = np.array([0.00, 0.25, 0.50, 0.75, 1.00])
ys = np.array([0.00, 0.60, 0.80, 0.90, 1.00])
print("np.trapz : %.4f" % np.trapz(xs, ys))
```

Real output:

```text
np.trapz : 0.3000
```

**Do this:** Say nothing. Point at `0.7000` on the left half of the board. Then at `0.3000` on the screen.

**Ask this:** "Was that an error?"

*Answer:* no.

**Ask this:** "0.7 and 0.3. Notice anything about those two numbers?"

*Hoped-for answer:* they add to 1.

> **Say this:** "They add to one. Because I have measured **the area to the left of the curve** instead of the area underneath it, and together those two areas fill the square, which has area 1.
>
> `np.trapz` wants the **heights first and the positions second.** Which is the opposite of how you say it out loud — 'x and y' — and that is exactly why this bug is so common. **No crash, no warning, and an answer that is the wrong side of the curve.**"

Fix it and run the whole area block:

```text
--- area under a five-point curve ---
strip 1: (0.00 + 0.60) / 2 x 0.25 = 0.0750
strip 2: (0.60 + 0.80) / 2 x 0.25 = 0.1750
strip 3: (0.80 + 0.90) / 2 x 0.25 = 0.2125
strip 4: (0.90 + 1.00) / 2 x 0.25 = 0.2375
by hand   : 0.7000
np.trapz  : 0.7000
```

**Do this:** Write `0.7000` on the right half of the board, under `np.trapz`. **Draw a big tick between the two halves.**

**Bug Log entry, sixty seconds.**

**Step 3 (3 min) — the reveal: AUC was always an area.**

Type:

```python
fpr, tpr, thr = roc_curve(y_val, prob)
print("np.trapz(tpr, fpr)  : %.4f" % np.trapz(tpr, fpr))
print("roc_auc_score       : %.4f" % roc_auc_score(y_val, prob))
```

```text
np.trapz(tpr, fpr)  : 0.6116
roc_auc_score       : 0.6116
```

**Do this:** Let it sit. Then say it plainly.

> **Say this:** "Those are the same number to four decimal places, and they are the same number because they are **the same calculation.**
>
> `roc_auc_score` — which you have been typing since Week 2 and trusting completely — is trapezoid strips under your ROC curve. Twenty-seven of them instead of four. **There is nothing else inside it.** You have been able to compute it by hand since Year 7 and nobody told you."

**Step 4 (6 min) — five folds, and 🐞 DELIBERATE MISTAKE ONE.**

> **Say this:** "Last thing, and it is the answer to that bump in the cost bowl. Our AUC is 0.6116, measured on one thousand rows, fourteen of them fraud. **How much should you trust it?** Let's chop the data up five different ways and find out."

Type the folds section, but **leave out `scoring="roc_auc"`**:

```python
pipe = Pipeline([("scaler", StandardScaler()),
                 ("model", LogisticRegression(max_iter=2000, random_state=0))])
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
scores = cross_val_score(pipe, X, y, cv=skf)
print(np.round(scores, 4))
```

Real output:

```text
[0.986  0.986  0.986  0.985  0.985]
```

**Ask this:** "Five beautiful, consistent numbers. Are we pleased?"

*Hoped-for answer:* somebody will be suspicious. 0.98 is the shape of last week's and Week 8's villain.

> **Say this:** "0.986. Where have you seen that number before?"

*Answer:* Week 8's accuracy paradox. It is the fraction of rows that are legitimate.

> "**It is accuracy.** I forgot to say which number I wanted, and the default for a classifier is accuracy, and on 1.4% fraud accuracy is a number about the 4,928 easy rows. Beautifully consistent, completely uninformative. **This is the third time this term the same trick has caught us, in a third costume.**"

Fix it and run the whole section:

```python
scores = cross_val_score(pipe, X, y, cv=skf, scoring="roc_auc")
print("frauds per test fold, StratifiedKFold :",
      [int(y[te].sum()) for tr, te in skf.split(X, y)])
print("frauds per test fold, plain KFold     :",
      [int(y[te].sum()) for tr, te in kf.split(X, y)])
print("the five AUCs :", np.round(scores, 4))
print("mean %.4f   sd %.4f" % (scores.mean(), scores.std()))
```

```text
frauds per test fold, StratifiedKFold : [14, 14, 14, 15, 15]
frauds per test fold, plain KFold     : [11, 17, 14, 17, 13]
the five AUCs : [0.6183 0.5909 0.6873 0.7504 0.4954]
mean 0.6285   sd 0.0867
```

**Do this:** Read the five AUCs out loud, one at a time, slowly. Then stop.

**Ask this:** "What is different between the fold that got 0.7504 and the fold that got 0.4954?"

*Hoped-for answer:* nothing except which rows it was scored on.

> **Say this:** "**Nothing.** Same model. Same code. Same seed. Same everything. One fold says this is a decent model and another fold says it is **worse than a coin**, and both of them are telling the truth about the thousand rows they saw.
>
> So the honest way to write this down — and this is how you will write every score for the rest of your life — is not one number. It is:
>
> **AUC = 0.628 ± 0.087, five-fold stratified.**"

**Do this:** Write the mean out longhand on the board while a student checks you on a phone.

```
0.6183 + 0.5909 + 0.6873 + 0.7504 + 0.4954  =  3.1423
3.1423 ÷ 5  =  0.6285
```

**Ask this:** "And why did we use `StratifiedKFold` instead of plain `KFold`? Look at the two lists of fraud counts."

*Hoped-for answer:* plain KFold gave one fold 11 frauds and another 17.

> "Eleven and seventeen. **A fifty-five percent difference in how many frauds there were to find.** If the scores then came out different, you would not know whether it was the model wobbling or one fold just having an easier day. **Stratification removes one of the two explanations**, and when you are diagnosing something, removing an explanation is the whole job."

**Bug Log. Second entry** — `scoring` forgotten, no error, 0.986 five times.

---

### 🎲 Their Turn — Fraud Bench + The Trapezoid Race (20 minutes)

Full instructions in **🎲 The Activity, In Full** below. In outline: they finish Fraud Bench with a **second, different price list** and find out that the winner moves; then the room splits in half and races the machine to compute the area under a curve nobody has seen yet, and **nobody moves on until the two halves of the board agree to three decimal places.**

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Stand between the two halves of the board — `BY HAND` and `np.trapz`, both saying the same number — and the circled row on the cost table.

**Say this:**

> "An hour ago you had three sticky notes and an argument. You now have a number, a reason for the number, and a price you can point at when somebody disagrees with you.
>
> And you have something better than that, which is the `±`. **0.628 plus or minus 0.087.** That number is more honest than 0.6116 was, and it is *less* impressive, and those two facts are the same fact."

**Ask this:** "Somebody shows up next week with a model scoring 0.65 on this data. Is it better than ours?"

*Hoped-for answer:* you cannot tell — 0.65 is inside our band.

> "You cannot tell. 0.65 is sitting inside our band. It might be our own model on a luckier split. **The `±` is not decoration on your result. It is your rule of thumb for which differences to trust and which to treat as unproven.**
>
> Bring me 0.85 and we will talk."

**Do this:** Three quick checks — exact wording in **✅ Assessing Understanding**.

**Say this, to close:**

> "One last thing, and it is next week's door, and it is a strange one.
>
> Today you measured the area *under* a curve, by chopping the space into strips and adding them up. Adding up.
>
> Next week you are going to measure the **steepness** of a curve — not between two points, like last week, but at **one single point.** And it turns out that is the opposite operation: instead of adding lots of little things up, you take **two numbers that are almost the same and subtract them.**
>
> And here is why it matters. Since Week 3 you have been typing `LogisticRegression().fit(X, y)` and something inside that line has been quietly trying a number, asking *'which way is downhill'*, and stepping. **Nobody has ever shown you how it asks.** Next week you find out, and the answer is two subtractions and a division."

**Do this:** Hand out the homework and read the last part out loud, slowly.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `sklearn.utils._param_validation.InvalidParameterError: The 'scoring' parameter of cross_val_score must be a str among {…} … Got 'auc' instead.` followed by a wall of sixty metric names | "That is not the name of a scorer. Here is every name I know." | `scoring="auc"`. The scorer is called `roc_auc`. | `scoring="roc_auc"`. **The full list of legal names is printed in the error — the answer is in the message, it is just very long.** |
| `AttributeError: 'list' object has no attribute 'mean'` | "Plain Python lists cannot average themselves." | `scores` was built by appending in a loop, so it is a list, not a numpy array. | `np.array(scores).mean()`, or use `cross_val_score`, which hands back an array already. |
| `UndefinedMetricWarning: Only one class is present in y_true. ROC AUC score is not defined in that case.` and `nan` in the score list | "One of your folds contained no frauds at all, so there is no ROC curve to measure." | Plain `KFold` on a small or very imbalanced slice. On a 300-row slice with 3 frauds, the fold counts come out `[0, 1, 2, 0, 0]` and three of the five scores are `nan`. | `StratifiedKFold`. **This is precisely the failure it exists to prevent.** |
| `UserWarning: The least populated class in y has only 3 members, which is less than n_splits=5.` | "You asked for five chunks and the rare class only has three rows in it, so at least two chunks cannot have one." | Cross-validating a tiny hand-made example, or a slice of the data instead of all of it. | Fewer splits, or more data. **On the real 5,000-row table there are 72 frauds, so this never happens** — if you see it, you are cross-validating the wrong variable. |
| `ValueError: Found input variables with inconsistent numbers of samples: [5000, 1000]` | "Those two things are different lengths." | `cross_val_score(pipe, X, y_val, …)` — the big `X` with the small `y`. | Pass a matching pair. `X` with `y`, or `X_val` with `y_val`. Never one of each. |
| **No error. `np.trapz(tpr)` returns 1.0 when the answer should be 0.5.** | Nothing crashed. You gave it the heights and no positions, so it assumed every strip was **1 wide**. | The x values were left off: `np.trapz(tpr)` instead of `np.trapz(tpr, fpr)`. | Always pass both. **On an ROC curve the widths are fractions, never 1, so this answer is always too big — usually by a factor of about the number of points.** |
| **No error. `np.trapz` returns 0.3000 instead of 0.7000.** | Nothing crashed. You measured the wrong side of the curve. | Arguments swapped: `np.trapz(xs, ys)`. | `np.trapz(ys, xs)` — **heights first.** Sanity check: your two answers should add to the area of the whole square. |
| **No error. `np.trapz` returns 0.6375 instead of 0.7000.** | Nothing crashed. Your x values are not in order. | The five points were plotted or typed out of sequence. | Sort by x before you integrate. **`np.trapz` walks the list in the order you give it and does not check.** |
| **No error. `cross_val_score` returns `[0.986 0.986 0.986 0.985 0.985]`.** | Nothing crashed. You measured accuracy on a 98.6%-legit dataset. | `scoring=` omitted, so the classifier's default — accuracy — was used. | `scoring="roc_auc"`. **Week 8's paradox, third costume.** |
| **No error. The five scores are `[0.7349 0.6389 0.6484 0.5851 0.648]` and the sd is 0.0481.** | Nothing crashed, and the `±` is only about half as big as in the lesson. | `shuffle=True` missing from `StratifiedKFold`, so the folds were cut in storage order: a different chop of the same data. | Add `shuffle=True, random_state=0`. **A smaller `±` from one particular chop is not a better measurement — the sd of five folds is itself noisy (about 0.03 to 0.12 across shuffle seeds), and you fix the chop in advance rather than choosing the one you like.** |
| **No error. The five scores are `[0.6202 0.5904 0.6864 0.7471 0.4958]`, all very slightly different from the right ones.** | Nothing crashed, and you have a tiny leak. | `StandardScaler().fit_transform(X)` applied **before** `cross_val_score`, so every fold's scaler had already seen the held-out rows. | Put the scaler **inside** the `Pipeline`, and pass the pipeline to `cross_val_score`. **This is Week 3 and Week 6's lesson arriving in a new place, and here it moved the mean by 0.0005 — small, and still wrong.** |
| **No error. The cheapest threshold changes every time you run it.** | The threshold list or the cost constants are being changed between runs. | Somebody is editing `COST_FN` while experimenting and forgetting. | **Write the price list down before you sweep, and do not touch it during the sweep.** One change, one row — Week 7's rule. |

### How to teach debugging without giving the answer

All the old moves stand. This week adds two.

21. **"Add your two answers up. Do they make something you recognise?"** For any area that comes out wrong. `0.7 + 0.3 = 1`, the area of the square — so you measured the other side. This one check catches the `np.trapz` argument order instantly and needs no documentation.

22. **"Did you tell it which number you wanted?"** For any `cross_val_score` result that looks suspiciously tidy. The default is accuracy and accuracy is a liar on imbalanced data. **Every result near 0.98 on this dataset should now trigger a reflex.**

And the sentence for this week:

> **"A number with no `±` beside it is a claim, not a measurement. Five folds cost you one extra second."**

---

## 🎲 The Activity, In Full

### Part 1 — Fraud Bench, with a second price list (10 minutes)

**What it is.** They already have the £500/£10 table. Now the bank changes its mind, and they find out how much of their answer was actually about the model and how much was about the money.

**Setup.** Nothing new. `fraud_bench.py` is already typed and running, and the nine-row table is on the board.

**Run it like this.**

**Minute 0–1.** Announce, deadpan:

> "The bank called back. It turns out they were including the investigation cost twice. **A missed fraud costs £50, not £500.** A false alarm still costs £10. Same model, same nine thresholds, new price list. Two minutes."

**Minute 1–5.** They change one line — `COST_FN = 50` — and re-run. Real output for the cost column, which you should have on this page in front of you:

```
t = 0.50   700       t = 0.08    670
t = 0.15   650       t = 0.06    770
t = 0.12   600  <--  t = 0.04   1110
t = 0.10   600  <--  t = 0.02   2560
t = 0.08   670       t = 0.01   4510
```

**The winner moves to `t = 0.12`, at £600** — and `t = 0.10` ties with it exactly. **Both of those facts are worth pointing out.**

**Minute 5–8.** Now the other direction:

> "And now the fraud department has read a newspaper. **A missed fraud costs £5,000.** Go."

```
t = 0.50   70000      t = 0.06   55220
t = 0.15   65000      t = 0.04   50610
t = 0.12   60000      t = 0.02   47110
t = 0.10   55050      t = 0.01   34210  <--
t = 0.08   55120
```

**The winner slides all the way to `t = 0.01`** — flag 429 of 1,000 rows and catch 8 of the 14.

**Minute 8–10 — the question that is the point of the whole activity.**

**Ask this:** "The model never changed. Which of those three thresholds is *correct*?"

*Hoped-for answer:* all of them, for their own price list. Or: none of them, without a price list.

> "**The threshold is not a property of your model. It is a property of your model and somebody's value judgement, together.** And the only professional thing you can do is write the value judgement down where a person can argue with it."

**What "finished" looks like:** three cost tables, three circled winners, and one sentence saying which price list they think is the honest one and why.

### Part 2 — The Trapezoid Race (10 minutes)

**What it is.** The room splits in two. **The left half computes the area under a five-point curve by hand, in strips. The right half computes it with `np.trapz`. Nobody moves on until the two answers agree to three decimal places.**

**Why the race format matters.** Not for the competition — for the **stopping rule**. A class that has agreed a hand answer and a machine answer to three decimal places has *verified* something, and verification is the habit this whole year is trying to build. It is also the exact shape of the gradient check in Week 19, so this is rehearsal.

> **📌 The model answer for the four-strip curve is Figure 11.3 above** — every strip's arithmetic printed beside it. The race uses a *different* curve, below, and its widths are not all equal.

**Setup**

- The board **already divided down the middle**, `BY HAND` on the left and `np.trapz` on the right.
- Fresh graph paper for the left half.
- One laptop for the right half.
- **A new five-point curve**, which you write up and which nobody has seen. Use this one — it is last week's twenty-card ROC curve, read off the wall at five of its thresholds:

```
   t = 0.90  ->  (0.0, 0.2)
   t = 0.70  ->  (0.1, 0.6)
   t = 0.50  ->  (0.3, 0.8)
   t = 0.30  ->  (0.5, 1.0)
   t = 0.05  ->  (1.0, 1.0)
```

**How it runs**

**Minute 0–1.** Split the room. Read the five points out. **Both halves get the same five points and neither may look at the other's working.**

**Minute 1–6 — the left half, by hand.** Four strips, and **the widths are not all the same this time**, which is the whole difficulty and the reason this curve was chosen:

```
strip 1:  (0.2 + 0.6) ÷ 2 × 0.1  =  0.40 × 0.1  =  0.0400
strip 2:  (0.6 + 0.8) ÷ 2 × 0.2  =  0.70 × 0.2  =  0.1400
strip 3:  (0.8 + 1.0) ÷ 2 × 0.2  =  0.90 × 0.2  =  0.1800
strip 4:  (1.0 + 1.0) ÷ 2 × 0.5  =  1.00 × 0.5  =  0.5000
                                                  ------
                                                  0.8600
```

**Minute 1–6 — the right half, in code.** Four lines:

```python
import numpy as np
xs = np.array([0.0, 0.1, 0.3, 0.5, 1.0])
ys = np.array([0.2, 0.6, 0.8, 1.0, 1.0])
print("%.4f" % np.trapz(ys, xs))
```

```text
0.8600
```

**Minute 6–8 — compare.** Both halves write their number on their half of the board. **0.8600 and 0.8600.** Tick between them.

*If they disagree:* the fault is almost always strip 4, whose width is 0.5 and not 0.25. Send them back to the widths. **Do not tell them which strip.**

**Minute 8–10 — the sting in the tail, and it is the best part.**

**Do this:** Now run the real thing on all twenty cards:

```python
import numpy as np
from sklearn.metrics import roc_auc_score
prob = np.array([0.96, 0.92, 0.88, 0.84, 0.80, 0.76, 0.72, 0.68, 0.64, 0.60,
                 0.55, 0.48, 0.42, 0.36, 0.30, 0.25, 0.20, 0.15, 0.10, 0.05])
truth = np.array([1, 1, 1, 0, 1, 1, 1, 0, 1, 1,
                  0, 1, 0, 0, 1, 0, 0, 0, 0, 0])
print("%.4f" % roc_auc_score(truth, prob))
```

```text
0.8500
```

**Ask this:** "We both got 0.8600 and we agreed. `roc_auc_score` says 0.8500. Who is wrong?"

*Hoped-for answer:* nobody — we used five points and it used all of them.

> "**Nobody is wrong.** We chopped the curve into four strips. scikit-learn chopped it into eleven. Our four strips cut some corners off — literally, the corners of the staircase — and each corner we cut made our answer slightly **too big.**
>
> Four strips got us to within one part in eighty-five of the right answer, and that is genuinely good enough for a lot of work. **More strips, more accurate.** That is the only thing there is to know about this, and it is why the computer does it with all the points instead of five."

**Variation — easier.** Use a curve with **four equal-width strips** (the one from the Concept segment: 0.00, 0.25, 0.50, 0.75, 1.00 across, 0.00, 0.60, 0.80, 0.90, 1.00 up, answer 0.7000). Equal widths mean the multiplication is the same every time. **Objective 2 is complete either way.**

**Variation — harder.** Three extensions:

1. **Do it with two strips instead of four**, using only three of the five points — `(0.0, 0.2)`, `(0.3, 0.8)` and `(1.0, 1.0)`: `(0.2 + 0.8) ÷ 2 × 0.3 = 0.1500`, then `(0.8 + 1.0) ÷ 2 × 0.7 = 0.6300`, total **0.7800**. Compare with 0.8600 and 0.8500. **Ask which direction the error went and why it went the other way this time.**
2. **Measure the area under their own real ROC curve** from `dial.py` with `np.trapz(tpr, fpr)`, get 0.6116, and confirm it equals `roc_auc_score`. Then ask how many strips there were. (27 — `len(fpr) - 1`.)
3. **Compute the cost curve's area.** It is meaningless, and asking *why* it is meaningless — the x-axis is a threshold, not a rate, and the units of the answer are pounds-times-probability — is a genuinely hard and genuinely good question. **Not every area means something.**

---

## ❓ Questions Students Ask This Week

**"Who decided that a fraud is worth fifty false alarms?"**
A person did. Probably a committee, in a meeting, with a spreadsheet. **And that is the best possible answer**, because it means you can go and ask them, and they have to justify it. Compare that with the situation last week, where the decision was being made by the number 0.5 sitting in a library's default arguments, and there was nobody to ask. **Making the value judgement visible does not make it right. It makes it arguable.**

**"What if you cannot put a price on a mistake?"**
Then you are in the hardest situation in applied machine learning, and it is extremely common — medical screening, exclusion from school, bail decisions. Two honest partial answers. **One:** you can often price the *ratio* even when you cannot price either side. "A missed cancer is at least a hundred times worse than an unnecessary scan" is a usable sentence and it gives you a threshold. **Two:** if you genuinely refuse to name a ratio, you must publish the whole curve and let each user pick their own point — which is exactly what last week was for. **What you may not do is pick a threshold quietly and pretend no judgement was made.**

**"Why five folds and not ten? Or a hundred?"**
Five and ten are conventions, and there is no deep reason for either. More folds means each model trains on more data (better) and each score is measured on fewer rows (noisier), and the whole thing takes longer. Five is a common compromise; ten is the other common one. With 72 frauds in total, ten folds would give each held-out chunk about 7 frauds, and a score resting on 7 events is very coarse indeed. **Here, five is already generous.**

**"Our `±` is 0.087. Is that big or small?"**
Big. It is about 14% of the score itself. To make it smaller you need more positive examples in each held-out chunk, which means more data — more folds do not add positives, and a different metric does not either. (A much stronger model would also narrow it, as the hospital example shows, but that is a different project.) **This is the honest answer to "how do I improve my number", and it is unsatisfying, and it is right.**

**"Why does numpy divide by 5 and my maths teacher divides by 4?"**
Both are standard, and they answer slightly different questions. Dividing by *n* gives you the spread of the five numbers you actually have. Dividing by *n*−1 gives you a better estimate of the spread of the infinite population those five came from. numpy's `.std()` divides by *n* by default; `.std(ddof=1)` divides by *n*−1 and gives **0.0969** instead of 0.0867. **No conclusion in this lesson changes either way.** Report which one you used and move on.

**"The formula said 0.0196 and the data said 0.032. Doesn't that mean one of them is broken?"**
🤔 **Nobody fully agrees about what to do here, and here is why.** One camp says: the formula is the answer, so if your data disagrees, **fix the model's probabilities** — calibrate them, and then the formula and the sweep may converge, and you will have learned something real. The other camp says: the formula is a piece of theory about a model that does not exist, so **just use the empirical minimum** — the sweep is measuring the actual machine you are going to deploy, and its answer is the operationally correct one whatever the theory prefers. A third camp points out that the empirical minimum here is measured on **fourteen** events and therefore is not a precise quantity either, so *both* numbers are soft and arguing about the gap between 0.0196 and 0.032 is arguing about noise. **All three are defensible, and the professional habit is to report both numbers and the disagreement**, because the disagreement is itself the interesting result.

**"Does cross-validation replace the test set?"**
**No, and this is important.** It replaces the *validation* set — the pile you use over and over while making choices. The test pile is still sealed and still gets opened exactly once, at the very end. If you cross-validate over everything including the test rows and then report the mean as a test score, you have leaked, and you have leaked in a way that is very hard to spot in code review.

**"Why do five models get thrown away?"**
Because cross-validation is a **measurement procedure**, not a training procedure. Its output is five numbers, not a model. When you are finished measuring, you refit once on all your training data and ship that. It feels wasteful and it is not — the five fits are the cost of knowing how much to trust yourself.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| **You hide the fact that the formula and the sweep disagree.** | It feels like an error in the material. | It is not. **Say it out loud and name it as a diagnosis.** §5 has the two reasons in full. A class that has seen two methods disagree and been told why is better educated than a class that has seen them agree. |
| The cost arithmetic eats twelve minutes. | Eighteen multiplications by hand is slower than it looks. | **Hand out rows, two students each, calculators mandatory.** Do row one together and then delegate. If you are still behind at minute 20, put the remaining rows on the homework and move to the trapezoids. |
| Everyone concludes the lowest threshold must always win, because misses cost more. | It is a completely reasonable inference and it is wrong. | Do the show of hands in the hook, **write the count on the board**, and come back to it. Being visibly wrong as a group and finding out why is the best learning event available. |
| The trapezoid strips come out wrong because the widths are unequal. | Strip 4 of the race curve is 0.5 wide and the others are 0.1 or 0.2. | **Do not fix it for them.** Say *"one of your four widths is not what you assumed"* and walk away. It is the entire difficulty of the activity. |
| `cross_val_score` gets five 0.98s and the room is pleased. | `scoring=` omitted, and 0.98 looks like success. | **This is deliberate mistake one.** Ask "where have you seen 0.986 before" and let Week 8 do the work. |
| The `±` is treated as decoration and copied down without meaning. | It looks like a formatting convention. | **Ask the "is 0.65 better than ours?" question immediately.** Do not move on until somebody says "you cannot tell". That question *is* objective 4. |
| A student says cross-validation is pointless because we already had a validation set. | It is a fair challenge. | Agree, then show them the two extreme folds: 0.7504 and 0.4954. *"Your validation set gave you one of those five numbers. Which one did you get, and how would you have known?"* |
| A student wants to pick the threshold from the fine sweep's 0.032 rather than the table's 0.10. | It is genuinely cheaper — £5,420 against £5,550. | **Let them, and make them defend it.** The honest counter-argument is that 0.032 sits in the noisy part of a bumpy curve measured on 14 frauds, while 0.10 sits in a broad flat basin. **Preferring a robust answer to an optimal one is a real engineering judgement.** |
| Everything finishes at minute 58. | The lab moves fast if the calculators are out. | Go to harder variation 1 of the race — two strips instead of four — and ask which direction the error goes. Or run the £5,000 price list and discuss what a bank that believed it would actually feel like to be a customer of. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** the 99-threshold fine sweep, the `t*` formula, and the whole theory-versus-measurement discussion. **Objectives 1, 2, 3 and 4 do not need any of it.** The formula is a nice-to-have; the nine-row table is the lesson.

**Cut also:** `KFold` versus `StratifiedKFold`. Use `StratifiedKFold` and say *"this one keeps the frauds spread evenly, which is what we want"*. The comparison is enrichment.

**Copy this exactly.** Hand it over on paper, let them run it, then change one number:

```python
# bench_small.py - one price list, three thresholds.
COST_FN = 500          # <-- CHANGE ONLY THIS NUMBER
COST_FP = 10

rows = [(0.50, 14, 0), (0.10, 11, 5), (0.01, 6, 421)]
print("   t   misses  alarms   500 x misses   10 x alarms    total")
for t, fn, fp in rows:
    a = COST_FN * fn
    b = COST_FP * fp
    print("%5.2f %7d %7d %14d %13d %8d" % (t, fn, fp, a, b, a + b))
```

Real output:

```text
   t   misses  alarms   500 x misses   10 x alarms    total
 0.50      14       0           7000             0     7000
 0.10      11       5           5500            50     5550
 0.01       6     421           3000          4210     7210
```

**Three rows is enough to see the bowl**, and the numbers are hand-checkable in under a minute.

**The maths, with everything hard removed.** Do not say "trapezoid" and do not say "area under a curve". Say:

> "Four fence panels. Each panel has a short post on the left and a taller post on the right. **How much paint does one panel need?** Measure both posts, take the number halfway between them, and multiply by how wide the panel is. Then do the other three and add them all up."

Halfway between 0.00 and 0.60 is 0.30. Times 0.25 is 0.0750. That is one panel. **Four panels, four numbers, add them: 0.7000.** No vocabulary required at all.

### If the student is flying

1. **Find the price list that makes `t = 0.04` win, and show that no price list makes `t = 0.02` win.** (Any miss price between about £560 and £900 against £10 gives 0.04. For 0.02 you would need a miss over £1,500 to beat 0.04 but under £700 to beat 0.01, which is impossible; it is a dominated row. The workbook puzzle does the same algebra.)
2. **Run 10 folds instead of 5** and report the new mean and `±`. **Then explain which direction the `±` moved and why**, given that each held-out chunk now has about 7 frauds instead of 14.
3. **Count the strips.** `len(fpr) - 1` on the real ROC curve. There are 27. **Ask why there are 27 and not 1,000** — the answer is that all 1,000 scores are distinct, so the raw curve has 1,000 steps, but `roc_curve` drops the points that lie on a straight stretch (`drop_intermediate=True`, the default) because they add nothing to the area. 27 corner points are left.
4. **The honest question:** *"we saved £1,450 by moving the threshold. Our `±` on AUC is 0.087. Should we put a `±` on the £1,450?"* **Absolutely we should, and this course never does it, and that is a real gap.** The £1,450 rests on the same 14 frauds. A student who works out that the cost saving needs an error bar too has understood cross-validation better than most textbooks explain it. Tell them so, and tell them the honest way to get it is to run the whole cost sweep inside every fold — which is Week 34's job.

### If the student won't engage today

Do the price list and nothing else. **Two multiplications and one addition, on one row, and the sentence "a miss is worth fifty false alarms".** Five minutes, no screen, and it is the big idea intact.

If they will do one written thing, make it this: **the £500 row and the £50 row for `t = 0.10`**, side by side.

```
a miss costs £500:   500 × 11 + 10 × 5  =  5500 + 50  =  5550
a miss costs  £50:    50 × 11 + 10 × 5  =   550 + 50  =   600
```

Then one sentence: *"the model did not change, so what did?"* **That is objectives 1 and 4 in ten minutes with a pen**, and it is the sentence they will actually remember in June, because in Week 34 they write the price list into a real model card for a real artifact.

If they will do nothing at all: ask them one question and let it sit. *"Your bank blocks your card at the till because a model was being careful. Now put a price on that in pounds. Go on — what is your afternoon worth?"* Everybody has a number, and nobody's number is £10.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the cost arithmetic, on a row they have not costed.** Say: *"At threshold 0.15 we had 13 misses and 0 false alarms. A miss costs £500 and a false alarm costs £10. What is the total cost, and show me the two multiplications."*

> **A good answer:** `500 × 13 = 6500`, `10 × 0 = 0`, total **£6,500**, with both lines written down. A student who says "6,500" without the working has probably done it right; **ask for the second multiplication anyway**, because the whole point is that the zero cell still gets multiplied.

**Check 2 — the new maths, on a strip they have not seen.** Write on the board:

```
left height 0.40      right height 0.70      width 0.20
```

Say: *"One strip. What is its area?"*

> **A good answer:** `(0.40 + 0.70) ÷ 2 = 0.55`, then `0.55 × 0.20 = 0.1100`. **Both steps.** A student who multiplies the two heights, or who forgets the width, has the shape and not the recipe — send them back to a fence panel and ask how much paint.

**Check 3 — what the `±` is for.** Say: *"We reported AUC = 0.628 ± 0.087. I have a new model and it scores 0.66. Is it better than ours? And what if it scored 0.90?"*

> **A good answer** says **you cannot tell** about 0.66 because it is inside the band, and **yes** about 0.90 because it is far outside. A student who says "0.66 is better because it is a bigger number" has copied the `±` without reading it — ask *"could our own model have scored 0.66 on a different split?"* and point at the 0.7504 fold.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot compute a row's cost without the formula in front of them. Thinks the threshold is a property of the model alone. |
| **2 — Emerging** | Computes cost rows correctly when the price list is given. Can find the cheapest row. Computes one trapezoid strip with help. Reports one number, not a band. |
| **3 — Secure** | Produces the whole nine-row cost table unaided and circles the winner. Sums four strips to 0.7000 and matches `np.trapz`. Runs `cross_val_score` with `scoring="roc_auc"` and reports mean ± sd. |
| **4 — Fluent** | Volunteers that changing the price list moves the winner, and predicts which way. Says what the `±` is for without being asked, in terms of which differences can be believed. Spots that `roc_auc_score` and `np.trapz` are the same calculation. |
| **5 — Extending** | Notices that the £1,450 saving needs an error bar too. Explains why the formula and the sweep disagree without prompting. Asks what happens as the strips get thinner — which is Week 12 and beyond arriving early. |

---

## 📤 Homework to Assign

**Say this, word for word:**

> "Four pages, about an hour, and the last sentence is the one I will read first.
>
> **Page 11.1 — the cost table, all nine rows.** Two multiplications and one addition each. **Circle the winner** and write its arithmetic out longhand underneath — `500 × 11 = 5500`, `10 × 5 = 50`, `5500 + 50 = 5550`. Not just the total.
>
> **Page 11.2 — the second price list.** Change a miss to £50 and do all nine rows again. **A different row wins.** Write down which, and one sentence saying what changed and what did not.
>
> **Page 11.3 — the trapezoid strips.** Five points, four strips, all four averages and all four multiplications shown, added up. Then `np.trapz` on the same numbers, and **the two answers written side by side.** If they do not match to three decimals, find your mistake before you write anything else.
>
> **Page 11.4 — five folds.** `StratifiedKFold` with `shuffle=True` and `random_state=0`, `cross_val_score` with `scoring="roc_auc"`. Print the five numbers, the mean and the sd, and write the result out in the proper form: `AUC = 0.628 ± 0.087 (5-fold stratified CV)`.
>
> **And then the sentence.** One sentence saying **what the `±` is for**, and one more saying **what you would conclude if it were three times bigger.** Three times bigger is ± 0.260, which puts our band at 0.368 to 0.888. Think about what a band that wide would let you claim. That is the sentence I care about."

| Page | What it is | Time |
|---|---|---|
| 11.1 | The nine-row cost table, winner circled, one row longhand | 15 min |
| 11.2 | The same nine rows at £50 a miss; which row wins now and why | 10 min |
| 11.3 | Four trapezoid strips by hand, matched against `np.trapz` | 15 min |
| 11.4 | 5-fold stratified AUC reported as mean ± sd | 10 min |
| 11.5 | The two `±` sentences | 5 min |
| 11.6 | Vocabulary (6 terms) and the Bug Log's two silent bugs | 10 min |

---

## 🔑 Answer Key

### Page 11.1 — The nine-row cost table

`cost = 500 × misses + 10 × false alarms`. The misses and false alarms come straight from last week's sweep.

| t | misses (fn) | false alarms (fp) | `500 × fn` | `10 × fp` | total |
|---|---|---|---|---|---|
| 0.50 | 14 | 0 | 7000 | 0 | **£7,000** |
| 0.15 | 13 | 0 | 6500 | 0 | **£6,500** |
| 0.12 | 12 | 0 | 6000 | 0 | **£6,000** |
| **0.10** | **11** | **5** | **5500** | **50** | **£5,550** ⬅ **cheapest** |
| 0.08 | 11 | 12 | 5500 | 120 | **£5,620** |
| 0.06 | 11 | 22 | 5500 | 220 | **£5,720** |
| 0.04 | 10 | 61 | 5000 | 610 | **£5,610** |
| 0.02 | 9 | 211 | 4500 | 2110 | **£6,610** |
| 0.01 | 6 | 421 | 3000 | 4210 | **£7,210** |

The winner's arithmetic, longhand:

```
500 × 11  =  5500
 10 ×  5  =    50
              ----
              5550
```

**And the saving against the default:** `7000 − 5550 = 1450`.

**Machine check.** The complete `fraud_bench.py` and its real output are printed in full in the **🧰 Prep Checklist** above. Check the student's output against that block on these three numbers:

| Must be exactly | If it is not |
|---|---|
| `cheapest of the nine: t = 0.10 at 5550` | `COST_FN` or `COST_FP` has been changed, or the threshold list is wrong. |
| `cheapest of the 99 : t = 0.032 at 5420` | `np.arange(0.002, 0.200, 0.002)` has different arguments. |
| `the five AUCs : [0.6183 0.5909 0.6873 0.7504 0.4954]` | `shuffle=True` or `random_state=0` missing from `StratifiedKFold`. Without `shuffle` you get `[0.7349 0.6389 0.6484 0.5851 0.648]`. |

**Common wrong answers:**

- **Forgetting to multiply the zero cells.** `10 × 0 = 0` still has to be written down. It is where the habit comes from.
- **Using `tp` instead of `fn`.** The cost is for **mistakes**. `tp` and `tn` are free.
- **Getting £7,000 for `t = 0.01`.** They have used 14 misses instead of 6. At the lowest threshold you miss *fewer*.

### Page 11.2 — The second price list

`COST_FN = 50`, `COST_FP = 10` — a miss is now worth only five false alarms.

| t | misses | alarms | `50 × fn` | `10 × fp` | total |
|---|---|---|---|---|---|
| 0.50 | 14 | 0 | 700 | 0 | **£700** |
| 0.15 | 13 | 0 | 650 | 0 | **£650** |
| **0.12** | **12** | **0** | **600** | **0** | **£600** ⬅ **cheapest** |
| **0.10** | **11** | **5** | **550** | **50** | **£600** ⬅ **tied** |
| 0.08 | 11 | 12 | 550 | 120 | **£670** |
| 0.06 | 11 | 22 | 550 | 220 | **£770** |
| 0.04 | 10 | 61 | 500 | 610 | **£1,110** |
| 0.02 | 9 | 211 | 450 | 2110 | **£2,560** |
| 0.01 | 6 | 421 | 300 | 4210 | **£4,510** |

**The winner moves from 0.10 to 0.12** — and 0.10 ties with it at exactly £600, which is worth noticing and worth saying: **when two thresholds tie, take the higher one, because it bothers fewer people for the same money.**

> **The sentence:** "The model did not change at all — the same 1,000 probabilities, the same nine thresholds, the same 14 frauds. **What changed was somebody's opinion about what a stolen paycheque is worth.** Making a miss ten times cheaper made me ten times more reluctant to raise an alarm, so the threshold went up."

**And for the £5,000 version, if they did it:**

| t | total |
|---|---|
| 0.50 | £70,000 |
| 0.15 | £65,000 |
| 0.12 | £60,000 |
| 0.10 | £55,050 |
| 0.08 | £55,120 |
| 0.06 | £55,220 |
| 0.04 | £50,610 |
| 0.02 | £47,110 |
| **0.01** | **£34,210** ⬅ **cheapest** |

**The winner slides all the way to the bottom of the table**, flagging 429 of 1,000 rows.

### Page 11.3 — Four trapezoid strips

The five points: `(0.00, 0.00) (0.25, 0.60) (0.50, 0.80) (0.75, 0.90) (1.00, 1.00)`. Every strip is 0.25 wide.

```
strip 1:  (0.00 + 0.60) ÷ 2 = 0.30      0.30 × 0.25 = 0.0750
strip 2:  (0.60 + 0.80) ÷ 2 = 0.70      0.70 × 0.25 = 0.1750
strip 3:  (0.80 + 0.90) ÷ 2 = 0.85      0.85 × 0.25 = 0.2125
strip 4:  (0.90 + 1.00) ÷ 2 = 0.95      0.95 × 0.25 = 0.2375
                                                      ------
                                        total       = 0.7000
```

**Machine check** — real output from `fraud_bench.py`:

```text
strip 1: (0.00 + 0.60) / 2 x 0.25 = 0.0750
strip 2: (0.60 + 0.80) / 2 x 0.25 = 0.1750
strip 3: (0.80 + 0.90) / 2 x 0.25 = 0.2125
strip 4: (0.90 + 1.00) / 2 x 0.25 = 0.2375
by hand   : 0.7000
np.trapz  : 0.7000
```

**Both 0.7000. Exactly, not approximately** — because the top of each strip is a straight line, so averaging the two heights is not a shortcut, it is correct.

**If they used the race curve instead** (unequal widths), the answer is **0.8600**:

```
(0.2 + 0.6) ÷ 2 × 0.1 = 0.0400
(0.6 + 0.8) ÷ 2 × 0.2 = 0.1400
(0.8 + 1.0) ÷ 2 × 0.2 = 0.1800
(1.0 + 1.0) ÷ 2 × 0.5 = 0.5000
                        ------
                        0.8600
```

and `np.trapz(ys, xs)` on those five points also prints **0.8600**, while `roc_auc_score` on all twenty cards prints **0.8500** — because five points cut the corners off an eleven-point staircase, and cutting corners off *this* shape makes the answer slightly **too big**.

**Common wrong answers:**

- **0.3000.** `np.trapz(xs, ys)` — arguments swapped. **Check: does it add to 1 with your hand answer? Then you measured the other side.**
- **0.6375.** The x values were not in increasing order.
- **0.7800 on the race curve.** They used two strips instead of four. Not wrong, just coarser — and worth praising if they say so.
- **Multiplying the two heights together.** They are averaging, not multiplying. Ask: *"if a fence panel is 1 m tall at both ends, how tall is it in the middle?"*

### Page 11.4 — Five folds, reported properly

Real output:

```text
frauds per test fold, StratifiedKFold : [14, 14, 14, 15, 15]
frauds per test fold, plain KFold     : [11, 17, 14, 17, 13]
the five AUCs : [0.6183 0.5909 0.6873 0.7504 0.4954]
mean 0.6285   sd 0.0867
report it as  : AUC = 0.628 +/- 0.087 (5-fold stratified CV)
```

The mean, longhand:

```
0.6183 + 0.5909  =  1.2092
1.2092 + 0.6873  =  1.8965
1.8965 + 0.7504  =  2.6469
2.6469 + 0.4954  =  3.1423

3.1423 ÷ 5  =  0.62846   →   0.6285
```

**The fold counts add up:** `14 + 14 + 14 + 15 + 15 = 72`, which is every fraud in the 5,000-row table. ✅ **Make them check this.**

**Two things to insist on in the write-up:**

1. **The words "5-fold stratified CV" beside the number.** A `±` with no method beside it is meaningless.
2. **The observation that one fold scored 0.4954** — below a coin — **and another scored 0.7504.** A student who reports the mean and never mentions the extremes has done the arithmetic and missed the point.

### Page 11.5 — The two `±` sentences

**Full marks, sentence one:**

> "The `±` is my **rule of thumb for how big a difference between two models to trust.** Our band is 0.628 ± 0.087, so about 0.54 to 0.72. Any model scoring inside that band might just be our own model on a luckier split, so I cannot claim it is better."

**Full marks, sentence two:**

> "Three times bigger is ± 0.260, which puts the band at **0.368 to 0.888.** That band contains 'clearly worse than a coin' and 'genuinely good' at the same time, so I would conclude that **my measurement cannot answer any question I actually care about** — and the fix is more data, or at least more positive examples per fold, not a different model."

**Acceptable variations** on sentence two, all of which earn full marks:

- "I would not report an AUC at all, I would say the experiment was too small to measure."
- "I would go back and check whether one fold contained something weird — a whole different kind of row."
- "I would stop comparing models on this dataset, because I could not tell any two of them apart."

**Answers to send back:**

- **"The `±` shows how accurate the model is."** No. It shows how noisy the **measurement** is. The model has one true quality; we measured it five times badly.
- **"A bigger `±` means a worse model."** No. Our `±` is mostly a statement about having 14 frauds per fold.
- **"It means the model is 0.628 accurate give or take 0.087."** It is not accuracy, it is AUC. Precision of language matters here and it is worth one gentle correction.

### Page 11.6 — Vocabulary and Bug Log

> **Cost matrix** — the confusion matrix with a price in each cell instead of a count. Ours: £0 for a correct legit, £10 for a false alarm, £500 for a miss, £0 for a caught fraud.

> **Expected cost** — the total price of the mistakes a model makes at a given threshold. `500 × misses + 10 × false alarms`.

> **k-fold cross-validation** — chop the data into *k* chunks, train on *k*−1 and score on the one left out, *k* times, so every row is held out exactly once. Report the mean **and** the wobble.

> **Stratified k-fold** — the same, but every chunk is built to hold the same proportion of the rare class. Ours gave 14, 14, 14, 15, 15 frauds per fold; plain `KFold` gave 11, 17, 14, 17, 13.

> **AUC** — the area under the ROC curve, added up as trapezoid strips. A coin's curve is the diagonal and the area under it is exactly 0.5. Ours is 0.6116.

> **Error bar** — the `±` printed beside a mean. It says how much the number moves when you measure the same thing again a slightly different way, and therefore a rule of thumb for which differences to trust.

**Bug Log — both entries are silent.**

**Entry one.**
Message: *none.* Symptom: `cross_val_score` returned `[0.986 0.986 0.986 0.985 0.985]`.
Meaning: I never said which number I wanted, so it gave me accuracy, and accuracy on a 98.6%-legit table is a statement about the easy rows.
Fix: `scoring="roc_auc"`.
The rule I am keeping: **any score near 0.98 on this dataset is a suspect, not a result.**

**Entry two.**
Message: *none.* Symptom: `np.trapz` returned 0.3000 where my hand arithmetic said 0.7000.
Meaning: I passed the positions first and the heights second, so I measured the area to the left of the curve instead of underneath it.
Fix: `np.trapz(ys, xs)` — heights first.
The rule I am keeping: **add my two answers up. 0.7 + 0.3 = 1, the whole square, so I measured the other side.**

### Answers to every question posed in the lesson

**Hook — "how many false alarms is one missed fraud worth?"** Fifty. `500 ÷ 10 = 50`.

**Hook — "will the cheapest threshold be the lowest one on the table, 0.01, or somewhere in the middle?"** Somewhere in the middle: it is **0.10**. Most classes guess 0.01 because a miss costs fifty times more, and they are wrong because the false alarms multiply much faster than the frauds get caught.

**Concept step 1 — "which row is cheapest?"** `t = 0.10`, at £5,550.

**Concept step 1 — "why is the winner not near 0.01?"** At 0.01 you catch five more frauds, worth £2,500 saved, and you buy 421 false alarms, costing £4,210. **You spent £4,210 to save £2,500.**

**Concept step 1 — "what is odd about `t = 0.04`?"** At £5,610 it is cheaper than `t = 0.06` at £5,720, so the bowl is not smooth. That bump is noise from resting on 14 frauds.

**Concept step 2 — "what shape is each slice?"** A rectangle with a sloping top — a trapezoid.

**Concept step 2 — "add the four up."** `0.0750 + 0.1750 + 0.2125 + 0.2375 = 0.7000`.

**Concept step 3 — "what is a coin's AUC?"** 0.5 — the diagonal splits the unit square in half, and the area of that triangle is `½ × 1 × 1 = 0.5`.

**Live-code step 1 — "does that match the board?"** Yes, row for row, all nine.

**Live-code step 1 — "which one is wrong, the formula or the measurement?"** Neither. The formula assumes calibrated probabilities, which 14 frauds cannot confirm (the scores do sum to about the right total, 14.1 against 14); the measurement rests on 14 frauds and is bumpy, so much of the gap is probably noise. **The disagreement is a question, not a verdict.**

**Live-code step 2 — "was that an error?"** No.

**Live-code step 2 — "0.7 and 0.3. Notice anything?"** They add to 1 — the area of the whole square. So `np.trapz(xs, ys)` measured the area to the left of the curve.

**Live-code step 4 — "five beautiful consistent numbers. Are we pleased?"** No. 0.986 is the fraction of rows that are legitimate; it is accuracy, and it is Week 8's paradox in a third costume.

**Live-code step 4 — "what is different between the 0.7504 fold and the 0.4954 fold?"** Nothing except which 1,000 rows were held out.

**Live-code step 4 — "why `StratifiedKFold` instead of `KFold`?"** Plain `KFold` gave one fold 11 frauds and another 17 — a 55% difference in how many frauds there were to find, which would contaminate the `±` with an extra explanation.

**Activity part 1 — "which of the three thresholds is correct?"** All of them, each under its own price list. Or: none of them without one. **The threshold is a property of the model *and* somebody's value judgement, together.**

**Activity part 2 — "we got 0.8600 and scikit-learn got 0.8500. Who is wrong?"** Nobody. Five points make four strips and cut the corners off an eleven-point staircase; scikit-learn used every point. Cutting those corners made our answer slightly **too big**. More strips, more accurate.

**Harder variation 1 — "two strips instead of four?"** Using only `(0.0, 0.2)`, `(0.3, 0.8)` and `(1.0, 1.0)`: `(0.2 + 0.8) ÷ 2 × 0.3 = 0.1500` and `(0.8 + 1.0) ÷ 2 × 0.7 = 0.6300`, total **0.7800**, and `np.trapz` on those three points prints 0.7800 too. Coarser again, and this time an **under**-estimate — 0.7800 against the true 0.8500, where four strips gave 0.8600, an over-estimate. **The direction of the error depends on which corners you happen to cut**, and noticing that four strips came out high while two came out low is a genuinely good observation.

**Harder variation 2 — "how many strips in the real ROC curve?"** `len(fpr) - 1 = 27`.

**Wrap — "is a model scoring 0.65 better than ours?"** You cannot tell. 0.65 is inside 0.628 ± 0.087.

---

## 🔮 Next Week Preview

Next week the box finally opens. Since Week 3 the student has typed `LogisticRegression(...).fit(X, y)` about forty times, and `fit` has been an instruction rather than a thing — a word that makes weights appear. Week 12 takes the lid off, and it does it with the mirror image of this week's maths: instead of chopping a space into strips and **adding** them up, you take two numbers that are almost identical and **subtract** them. The class picks eight candidate values for one weight, computes the loss for each — `2464.00, 1386.00, 616.00, 154.00, 0.00, 154.00, 616.00, 1386.00` — and sketches the valley on graph paper. Then they measure how steep that valley is at a single point by nudging the input by 0.001 and dividing, get **exactly 6.000** for `x × x` at `x = 3`, discover that the three answers at `x = 1, 3, 5` are **2, 6 and 10** — which is exactly `2 × x` — and only *then* is the word **derivative** allowed in the room. The lesson ends with eight steps walked downhill by hand, `w ← w − 0.3 × slope`, arriving at 7.996068 when the answer hidden in the data was 8. **No calculus, no limits, no symbols before the numbers.** It is the single most important week in the whole of Level 3 and everything from Week 15 to Week 27 stands on it.

**To prep early:** four things, and take them seriously — this is the week to over-prepare. **One — do the nudge yourself, on paper, tonight.** `3.001 × 3.001 = 9.006001`, `2.999 × 2.999 = 8.994001`, subtract to get `0.012000`, divide by `0.002` to get `6.000`. **If you have not done that arithmetic with your own hand, do not teach the lesson.** It takes four minutes and it is the whole week. **Two — find a staircase**, or a ramp, or a slope in a corridor. The hook is a physical walk downhill saying "which way is down" out loud, and it works far better on real steps than on a diagram. **Three — three sheets of graph paper per student**, plus a big one for the wall: the loss valley gets sketched by hand before any code runs. **Four — do not wipe today's `BY HAND | np.trapz` board**; next week's whole argument is that a hand-computed number and a machine-computed number agreeing is what "understanding" means, and having the tick from today still on the wall saves you a paragraph.

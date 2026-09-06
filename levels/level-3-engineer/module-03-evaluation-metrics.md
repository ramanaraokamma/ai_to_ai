# Module 3 — Beyond Accuracy: Confusion Matrix, Precision, Recall, and Thresholds

**Level 3 · Module 3 · ~5 hours · Prereqs: Module 1 (splits, baselines, Pipeline) and Module 2 (ColumnTransformer, leakage).**

[⬅ Previous](module-02-feature-engineering.md) · [Level 3 Home](README.md) · [Next ➡](module-04-logistic-regression-gradient-descent.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. You will be able to build a confusion matrix by hand from a list of predictions and compute precision, recall, F1, and specificity from its four numbers.
2. You will be able to describe a false positive and a false negative in the language of the actual application — not "FP", but "a real customer's card gets declined at a petrol pump" — and say which one costs more.
3. You will be able to turn the decision threshold from 0.5 into whatever the problem needs, and draw the precision/recall trade-off curve that results.
4. You will be able to read an ROC curve and a precision-recall curve, compute AUC by hand on a tiny example, and say which curve to trust when the classes are wildly imbalanced.
5. You will be able to run stratified k-fold cross-validation and report **mean ± standard deviation** instead of one lucky number.
6. You will be able to choose a threshold by minimising an explicit expected cost, and show the arithmetic that justifies it.

---

## 🪝 The Hook

A bank's fraud team ships a model. Test accuracy: **99.08%**.

The team lead is delighted. Then someone in risk asks a single question: *"How many of last month's frauds did it catch?"*

The answer is **4 out of 57**.

The model is 99.08% accurate because 99.05% of transactions are not fraud, and the model has essentially learned to say "not fraud" and go back to sleep. Predicting "not fraud" for literally every transaction, with no model at all, scores 99.05%. Six months of work bought **three hundredths of one percentage point**.

Here is the thing that should make you uncomfortable: nothing was wrong with the model. The features were fine. There was no leakage. The pipeline was clean. The only mistake was the metric — and that one mistake made a useless system look like a triumph.

This module is the set of numbers that would have caught it in five minutes.

---

## 🧠 The Concept

### 1. Class imbalance and the accuracy paradox

> **Class imbalance:** when one class is much more common than the other. 99% not-fraud and 1% fraud is imbalanced. 50/50 is balanced.

> **Accuracy:** the fraction of predictions that were correct. `(correct) / (total)`.

Accuracy is the first metric everyone learns and the first one that betrays them.

🍕 **Analogy.** A smoke alarm that never goes off is "correct" 99.9% of the days of your life. It is correct on every single day your kitchen does not catch fire. It is wrong exactly once — on the day that matters. Its accuracy is superb. Its usefulness is zero, and the one error it makes is the only error anybody cares about.

🔢 **Tiny concrete example.** 6,000 transactions, 57 of them fraud (0.95%).

- Strategy "always say not-fraud": correct on 5,943, wrong on 57. Accuracy = 5943 / 6000 = **0.9905**.
- Our actual trained model: accuracy = **0.9908**.

The gap is 0.0003. Reported to two decimal places, both round to "99%." Accuracy simply does not have the resolution to distinguish a working model from no model at all when the positive class is rare.

**The rule:** whenever you report accuracy, report the majority-class rate right next to it. If you can't beat "always guess the common class" by a wide margin, accuracy is the wrong instrument.

---

### 2. TP, FP, FN, TN: the four numbers everything is built from

Every binary prediction falls into exactly one of four boxes.

```
                         PREDICTED
                  negative        positive
              ┌───────────────┬───────────────┐
     negative │      TN       │      FP       │
              │ true negative │ false positive│   <- these rows are
ACTUAL        │   correct     │  FALSE ALARM  │      actually negative
              ├───────────────┼───────────────┤
     positive │      FN       │      TP       │
              │ false negative│ true positive │   <- these rows are
              │    MISS       │   correct     │      actually positive
              └───────────────┴───────────────┘
```

> **True Positive (TP):** it was positive, you said positive. ✅
> **True Negative (TN):** it was negative, you said negative. ✅
> **False Positive (FP):** it was negative, you said positive. A **false alarm**.
> **False Negative (FN):** it was positive, you said negative. A **miss**.

The naming trick: the second word is *what you predicted*; the first word is *whether you were right*. "False positive" = you predicted positive, and that was false.

> **Confusion matrix:** the 2×2 table of those four counts.

🍕 **Analogy.** A metal detector at an airport.

- **TP:** the passenger has a knife, the detector beeps. Good.
- **TN:** the passenger has nothing, silence. Good.
- **FP:** the passenger's belt buckle sets it off. Annoying — a two-minute pat-down.
- **FN:** the passenger has a ceramic knife and walks straight through. Catastrophic.

Notice the two errors are not remotely equal. That asymmetry is the whole point of this module.

⚠️ **Watch the layout.** `sklearn.metrics.confusion_matrix` returns rows = actual, columns = predicted, with class 0 first:

```python
cm = confusion_matrix(y_true, y_pred)     # [[TN, FP],
                                          #  [FN, TP]]
tn, fp, fn, tp = cm.ravel()
```

Many textbooks and most papers put positives first, or transpose it entirely. Always unpack with `.ravel()` and label your variables, never index blindly.

🔢 **Tiny concrete example.** 100 emails, 20 of them spam. Your filter flags 21 emails as spam; 16 of those really are spam.

- TP = 16 (spam, correctly flagged)
- FP = 21 − 16 = 5 (real email, wrongly flagged — went to the junk folder)
- FN = 20 − 16 = 4 (spam, missed — landed in the inbox)
- TN = 100 − 16 − 5 − 4 = 75 (real email, correctly delivered)

```
                    PREDICTED
                 ham      spam
ACTUAL   ham  │  75   │    5   │  = 80 real emails
        spam  │   4   │   16   │  = 20 spam
              └───────┴────────┘
                 79       21
```

We'll compute every metric in the module from these four numbers.

---

### 3. Precision, recall, F1, specificity — with the arithmetic shown

Four ratios, four different questions.

> **Precision** = TP / (TP + FP) — *"of everything I flagged, how much was really positive?"* Read down the **predicted-positive** column.

> **Recall** (also called sensitivity, or true positive rate) = TP / (TP + FN) — *"of everything that really was positive, how much did I catch?"* Read across the **actual-positive** row.

> **Specificity** (true negative rate) = TN / (TN + FP) — *"of everything that really was negative, how much did I correctly leave alone?"*

> **F1** = the harmonic mean of precision and recall = 2 · (P · R) / (P + R) — one number when you need one number and both errors cost about the same.

🍕 **Analogy.** You are fishing with a net.

- **Precision:** of everything in your net, what fraction is actually fish? (The rest is boots and seaweed.)
- **Recall:** of all the fish in the lake, what fraction ended up in your net?
- A tiny net thrown at one fish you can see: precision 100%, recall 1%.
- Draining the entire lake: recall 100%, precision terrible.
- **You can always max out one by wrecking the other.** That is why nobody reports just one.

🔢 **Worked arithmetic on the spam example** (TP=16, FP=5, FN=4, TN=75):

| Metric | Formula | Substitution | Value |
|---|---|---|---|
| Accuracy | (TP+TN)/total | (16+75)/100 = 91/100 | **0.9100** |
| Precision | TP/(TP+FP) | 16/(16+5) = 16/21 | **0.7619** |
| Recall | TP/(TP+FN) | 16/(16+4) = 16/20 | **0.8000** |
| Specificity | TN/(TN+FP) | 75/(75+5) = 75/80 | **0.9375** |
| F1 | 2PR/(P+R) | 2(0.7619)(0.8000)/(0.7619+0.8000) = 1.21905/1.56190 | **0.7805** |

Read that as English: *"Of the 21 emails we sent to junk, 76% really were spam. Of all the spam that arrived, we caught 80%. We correctly delivered 94% of real email. Five real emails went to junk this month."*

That last sentence is what you say to a human. Nobody outside your team wants a ratio; they want to know how many of their real emails vanished.

**Why the harmonic mean for F1?** Because a plain average is too forgiving. Precision 1.0 and recall 0.0 (you flagged exactly one email and were right about it) averages to 0.50, which sounds like a passing grade for a useless filter. The harmonic mean gives 2(1.0)(0.0)/(1.0+0.0) = **0**. The harmonic mean punishes imbalance — you cannot get a good F1 by being brilliant at one and hopeless at the other.

**Which one should you optimise?** Ask which error hurts more.

| Application | A false positive means... | A false negative means... | Optimise |
|---|---|---|---|
| Spam filter | your bank's OTP goes to junk | one junk email in the inbox | **precision** |
| Cancer screening | an anxious week and one extra scan | an undetected tumour | **recall** |
| Fraud detection | a real card declined at the pump | money stolen | usually **recall**, weighted by cost |
| Court sentencing | a low-risk person held | a high-risk person released | contested — this is a societal question, not a maths one |
| Which video to recommend | a boring video shown | a great video not shown | **precision @ k** |

---

### 4. The threshold dial, ROC, and precision-recall curves

Here is the thing nobody tells you at first: **your classifier does not output a class. It outputs a probability.** The class comes from comparing that probability to a threshold, and 0.5 is nothing but a default.

```python
prob = model.predict_proba(X)[:, 1]     # e.g. 0.31
pred = (prob >= 0.5).astype(int)        # 0.5 is a CHOICE, not a law of nature
```

> **Decision threshold:** the probability above which you call something positive. Lower it and you catch more positives (recall up) but raise more false alarms (precision down). Raise it and the opposite.

🍕 **Analogy.** A volume knob on a smoke alarm's sensitivity. Turn it all the way up and burnt toast triggers it — you never miss a fire, and you also never eat toast in peace. Turn it down and you sleep undisturbed until the night you don't wake up. There is no "correct" setting written on the knob. The correct setting depends on what a false alarm costs you versus what a miss costs you.

🔢 **Tiny concrete example.** Ten emails, ranked by the model's spam probability.

| prob | truth |
|---|---|
| 0.95 | spam |
| 0.90 | spam |
| 0.80 | ham |
| 0.70 | spam |
| 0.55 | spam |
| 0.45 | ham |
| 0.40 | spam |
| 0.30 | ham |
| 0.20 | ham |
| 0.05 | ham |

Five spam, five ham. Now sweep the threshold:

| threshold | flagged | TP | FP | FN | TN | precision | recall |
|---|---|---|---|---|---|---|---|
| 0.90 | 2 | 2 | 0 | 3 | 5 | **1.000** | 0.400 |
| 0.70 | 4 | 3 | 1 | 2 | 4 | 0.750 | 0.600 |
| 0.50 | 5 | 4 | 1 | 1 | 4 | 0.800 | 0.800 |
| 0.40 | 7 | 5 | 2 | 0 | 3 | 0.714 | **1.000** |
| 0.20 | 9 | 5 | 4 | 0 | 1 | 0.556 | 1.000 |

Same model. Same predictions. Precision ranges from 0.556 to 1.000 and recall from 0.400 to 1.000, purely by turning the dial. Anyone who reports "precision = 0.80" without telling you the threshold has told you almost nothing.

**Two curves plot this trade-off.**

> **ROC curve:** true positive rate (recall) on the y-axis against false positive rate (FP/(FP+TN)) on the x-axis, traced out as the threshold sweeps from 1 down to 0.

> **AUC (area under the ROC curve):** one number summarising the whole curve. It equals the probability that a randomly chosen positive gets a higher score than a randomly chosen negative. 0.5 = random guessing. 1.0 = perfect ranking.

> **Precision-recall (PR) curve:** precision on the y-axis against recall on the x-axis. Its summary number is **average precision (AP)**.

```
   ROC curve                          Precision-Recall curve

 1.0┤        ╭────────                1.0┤──╮
    │      ╭─╯                           │  ╰──╮
 TPR│    ╭─╯     ← good model         P  │     ╰───╮
    │  ╭─╯                            R  │         ╰────╮
    │╭─╯   ····· ← random (AUC 0.5)   E  │              ╰──── ← baseline = the
 0.0┤╯ ····                           C 0┤                      positive class rate
    └──────────────                      └──────────────
    0.0    FPR    1.0                    0.0  RECALL  1.0
```

**When to use which.** ROC-AUC has a hidden weakness on imbalanced data: its x-axis is FP/(FP+TN), and when TN is 5,943, adding 500 false positives moves the x-axis by only 0.084. The curve barely notices a flood of false alarms that would drown your operations team. The PR curve has precision on the y-axis, and precision *does* collapse when FP explodes.

| | ROC-AUC | Average precision (PR-AUC) |
|---|---|---|
| Baseline for a useless model | always 0.5 | equals the positive class rate |
| Sensitive to a flood of false positives? | not much | **yes** |
| Use when | classes are roughly balanced, or you care about ranking overall | positives are rare and false positives are expensive |
| Our fraud model | 0.8895 | **0.1931** |

Those two numbers describe the *same predictions*. The AUC of 0.8895 says "this model ranks frauds above non-frauds pretty well." The AP of 0.1931 says "when you actually try to use it, most of what you flag will be innocent." Both are true. Report both.

---

### 5. Cross-validation: one number is not a measurement

Your validation set has 400 rows. You compute accuracy = 0.7600. How much should you trust that 0.7600?

Change `random_state` and it moves. That movement is not the model changing — the model is identical. It is the *measurement* being noisy, because 400 rows is a small sample of the universe of possible pizza orders.

> **k-fold cross-validation:** chop the data into *k* equal parts. Train on *k*−1 of them, score on the one left out. Repeat *k* times so every row is in the held-out fold exactly once. Report the mean of the *k* scores and their standard deviation.

```
5-FOLD CROSS-VALIDATION

 fold 1  [TEST][    train    ][    train    ][    train    ][   train   ]  -> score 1
 fold 2  [ train ][TEST][   train   ][    train    ][    train    ]        -> score 2
 fold 3  [    train    ][ train ][TEST][   train   ][    train    ]        -> score 3
 fold 4  [    train    ][    train    ][ train ][TEST][   train   ]        -> score 4
 fold 5  [    train    ][    train    ][    train    ][ train ][TEST]      -> score 5

                       report  mean ± std
```

🍕 **Analogy.** Weighing yourself once tells you a number. Weighing yourself on five different mornings tells you a number *and* how much it wobbles. If your weight reads 60 kg ± 0.2 kg you can detect a 1 kg change. If it reads 60 kg ± 3 kg you cannot, and any diet claiming a 1 kg result is unmeasurable with that scale.

> **Stratified k-fold:** k-fold that keeps the class proportions identical in every fold. Non-negotiable when the positive class is rare.

🔢 **Tiny concrete example.** Our fraud dataset has 190 frauds across 20,000 rows. With 5 folds:

| Splitter | Positives in each test fold |
|---|---|
| `KFold` | 37, 30, 39, 49, 35 |
| `StratifiedKFold` | 38, 38, 38, 38, 38 |

Plain `KFold` gave one fold 49 frauds and another 30 — a 63% difference in how many positives there were to find. Any variation in your scores now mixes together *model instability* and *fold composition*, and you can't tell them apart. Stratification removes the second source.

🔢 **What the numbers look like on our fraud pipeline** (5-fold stratified, whole dataset):

| Metric | mean | std | per-fold |
|---|---|---|---|
| ROC-AUC | 0.8405 | ±0.0084 | 0.841, 0.856, 0.832, 0.837, 0.836 |
| Average precision | 0.2165 | ±0.0543 | 0.178, 0.273, 0.143, 0.284, 0.204 |
| Recall @0.5 | 0.0895 | ±0.0394 | 0.079, 0.079, 0.026, 0.132, 0.132 |
| Precision @0.5 | 0.8929 | ±0.1317 | 0.750, 1.000, 1.000, 1.000, 0.714 |

Read the std column. AUC wobbles by less than one point — it is a stable, trustworthy measurement, because it uses every row's ranking. Recall at threshold 0.5 wobbles from 0.026 to 0.132, a **five-fold** spread, because it depends on a handful of predictions crossing an arbitrary line. If you had run one split and got 0.132, you would have reported a model five times better than the one that got 0.026, and it is the same model.

**How to report a result, forever after:** `AUC = 0.841 ± 0.008 (5-fold stratified CV)`. Never a bare number.

⚠️ Cross-validation **replaces the validation set**, not the test set. The test set is still opened exactly once, at the very end, exactly as in Module 1.

---

### 6. Choosing the threshold from the cost of errors

Everything so far has been description. Now the decision.

If you can put a number on what each error costs, you do not have to pick a threshold by squinting at a curve. You compute it.

> **Cost matrix:** the money (or time, or harm) attached to each cell of the confusion matrix.

For our fraud problem, stated by the business:

| | Predicted legit | Predicted fraud |
|---|---|---|
| **Actually legit** | ₹0 | **₹10** (analyst reviews it, customer mildly annoyed) |
| **Actually fraud** | **₹500** (money gone, chargeback, investigation) | ₹0 (caught in time) |

A missed fraud costs **50×** a false alarm.

**Expected cost at a given threshold:**

$$ \text{Cost}(t) = C_{FN} \cdot FN(t) + C_{FP} \cdot FP(t) $$

Sweep *t*, compute the cost, pick the minimum. That is the entire method, and it turns "which threshold?" from an argument into arithmetic.

🍕 **Analogy.** Deciding how early to leave for the airport. Leaving too early costs you an hour of boredom. Leaving too late costs you the flight. Nobody splits the difference at "50% chance of making it." You weight the two costs and, because missing the flight is a hundred times worse than being bored, you leave absurdly early. That is threshold tuning, and you already do it every time you travel.

🔢 **Worked example.** Three thresholds on our 6,000-row fraud test set:

| t | TP | FP | FN | TN | cost = 500·FN + 10·FP |
|---|---|---|---|---|---|
| 0.50 | 4 | 2 | 53 | 5941 | 500(53) + 10(2) = 26,500 + 20 = **₹26,520** |
| 0.02 | 37 | 472 | 20 | 5471 | 500(20) + 10(472) = 10,000 + 4,720 = **₹14,720** |
| 0.01 | 46 | 1187 | 11 | 4756 | 500(11) + 10(1187) = 5,500 + 11,870 = **₹17,370** |

Moving from the default 0.5 to 0.02 saves **₹11,800** on 6,000 transactions. Going further to 0.01 catches nine more frauds but buys 715 extra false alarms, and the cost climbs again. There is a bottom to the bowl, and the sweep finds it.

**There is also a formula.** The threshold at which flagging becomes worthwhile is the point where the expected cost of flagging equals the expected cost of not flagging. If the true probability of fraud is *p*:

- Cost of flagging = (1 − p) · C_FP  (you pay for a false alarm only when it's legit)
- Cost of not flagging = p · C_FN  (you pay for the miss only when it's fraud)

Set them equal: (1 − p)·C_FP = p·C_FN → p·C_FN + p·C_FP = C_FP →

$$ t^{*} = \frac{C_{FP}}{C_{FP} + C_{FN}} = \frac{10}{10 + 500} = \frac{10}{510} = \mathbf{0.0196} $$

And the empirical sweep on real data, at a resolution of 0.002, finds its minimum at **t = 0.018**. Theory and measurement agree to within one grid step. That agreement is a strong sign your probabilities are reasonably calibrated; if the empirical optimum landed at 0.30 while the theory said 0.02, you would know your model's probabilities are badly miscalibrated and you should investigate before trusting either number.

**Use both.** The formula gives you the answer for a perfectly calibrated model. The sweep gives you the answer for the model you actually have. When they agree, ship. When they disagree, you have learned something.

---

## 🔍 Worked Example

One classifier, ten predictions, every number computed by hand: confusion matrix, all four metrics, the full threshold sweep, the ROC curve, and AUC two different ways.

**The data.** Ten emails scored by a spam filter. Five spam (positive), five ham (negative).

| # | prob | truth |
|---|---|---|
| 1 | 0.95 | spam |
| 2 | 0.90 | spam |
| 3 | 0.80 | ham |
| 4 | 0.70 | spam |
| 5 | 0.55 | spam |
| 6 | 0.45 | ham |
| 7 | 0.40 | spam |
| 8 | 0.30 | ham |
| 9 | 0.20 | ham |
| 10 | 0.05 | ham |

---

**Step 1 — Confusion matrix at the default threshold 0.5.**

Flagged (prob ≥ 0.5): #1, #2, #3, #4, #5 — five emails.

- Of those, spam: #1, #2, #4, #5 → **TP = 4**
- Of those, ham: #3 → **FP = 1**
- Spam not flagged: #7 → **FN = 1**
- Ham not flagged: #6, #8, #9, #10 → **TN = 4**

Check: 4 + 1 + 1 + 4 = 10 ✅

```
                 PREDICTED
              ham       spam
ACTUAL  ham │   4   │    1   │
       spam │   1   │    4   │
```

**Step 2 — Metrics at t = 0.5.**

- Accuracy = (TP + TN) / 10 = (4 + 4) / 10 = **0.800**
- Precision = 4 / (4 + 1) = 4/5 = **0.800**
- Recall = 4 / (4 + 1) = 4/5 = **0.800**
- Specificity = 4 / (4 + 1) = **0.800**
- F1 = 2(0.8)(0.8) / (0.8 + 0.8) = 1.28 / 1.6 = **0.800**

All five agree at 0.800, which happens only because the classes are perfectly balanced and FP = FN. Do not expect this in real life; it is a coincidence of this toy.

**Step 3 — The full threshold sweep.** Walk down the ranked list. Each row becomes "flagged" as the threshold drops past it.

| after including # | threshold | TP | FP | FN | TN | precision | recall | FPR = FP/5 |
|---|---|---|---|---|---|---|---|---|
| — | >0.95 | 0 | 0 | 5 | 5 | — | 0.0 | 0.0 |
| 1 (spam) | 0.95 | 1 | 0 | 4 | 5 | 1.000 | 0.2 | 0.0 |
| 2 (spam) | 0.90 | 2 | 0 | 3 | 5 | 1.000 | 0.4 | 0.0 |
| 3 (ham) | 0.80 | 2 | 1 | 3 | 4 | 0.667 | 0.4 | 0.2 |
| 4 (spam) | 0.70 | 3 | 1 | 2 | 4 | 0.750 | 0.6 | 0.2 |
| 5 (spam) | 0.55 | 4 | 1 | 1 | 4 | 0.800 | 0.8 | 0.2 |
| 6 (ham) | 0.45 | 4 | 2 | 1 | 3 | 0.667 | 0.8 | 0.4 |
| 7 (spam) | 0.40 | 5 | 2 | 0 | 3 | 0.714 | 1.0 | 0.4 |
| 8 (ham) | 0.30 | 5 | 3 | 0 | 2 | 0.625 | 1.0 | 0.6 |
| 9 (ham) | 0.20 | 5 | 4 | 0 | 1 | 0.556 | 1.0 | 0.8 |
| 10 (ham) | 0.05 | 5 | 5 | 0 | 0 | 0.500 | 1.0 | 1.0 |

Two things to notice. **Precision is not monotonic** — it goes 1.000, 1.000, 0.667, 0.750, 0.800, 0.667, 0.714… It rises whenever the next item down the ranking is a true positive and drops whenever it's a false one. Recall, by contrast, only ever goes up.

**Step 4 — Draw the ROC curve.** Plot (FPR, TPR) from the table. Each spam in the ranking steps **up** by 1/5 = 0.2; each ham steps **right** by 0.2.

Ranked labels top to bottom: `S S H S S H S H H H`

```
 TPR
 1.0 ┤             ┌───────────────────────────┐
     │             │
 0.8 ┤       ┌─────┘
     │       │
 0.6 ┤       │
     │       │
 0.4 ┤ ┌─────┘
     │ │
 0.2 ┤ │
     │ │
 0.0 ┼─┴──────────────────────────────────────
     0.0   0.2   0.4   0.6   0.8   1.0   FPR
```

Exact vertices: (0,0) → (0,0.2) → (0,0.4) → (0.2,0.4) → (0.2,0.6) → (0.2,0.8) → (0.4,0.8) → (0.4,1.0) → (0.6,1.0) → (0.8,1.0) → (1.0,1.0)

**Step 5 — AUC by geometry.** Every rightward step contributes a rectangle of width 0.2 and height equal to the current TPR.

| rightward step (a ham) | TPR at that moment | area |
|---|---|---|
| after #3 | 0.4 | 0.2 × 0.4 = 0.08 |
| after #6 | 0.8 | 0.2 × 0.8 = 0.16 |
| after #8 | 1.0 | 0.2 × 1.0 = 0.20 |
| after #9 | 1.0 | 0.2 × 1.0 = 0.20 |
| after #10 | 1.0 | 0.2 × 1.0 = 0.20 |

**AUC = 0.08 + 0.16 + 0.20 + 0.20 + 0.20 = 0.84**

**Step 6 — AUC the other way, to prove the definition.** AUC = the probability a random spam outranks a random ham. There are 5 × 5 = 25 (spam, ham) pairs. Count how many the model gets right:

| spam | beats these hams | count |
|---|---|---|
| 0.95 | 0.80, 0.45, 0.30, 0.20, 0.05 | 5 |
| 0.90 | 0.80, 0.45, 0.30, 0.20, 0.05 | 5 |
| 0.70 | 0.45, 0.30, 0.20, 0.05 (loses to 0.80) | 4 |
| 0.55 | 0.45, 0.30, 0.20, 0.05 | 4 |
| 0.40 | 0.30, 0.20, 0.05 | 3 |

Total correctly ordered pairs = 5 + 5 + 4 + 4 + 3 = **21**

**AUC = 21 / 25 = 0.84** ✅ Identical. Two completely different routes, same answer, which is what tells you the definition is really doing what it claims.

**Step 7 — Now apply a cost.** Suppose a missed spam costs 1 unit (mild annoyance) and a junked real email costs 20 units (you missed a job offer).

$$ \text{Cost}(t) = 1 \cdot FN(t) + 20 \cdot FP(t) $$

| t | FN | FP | cost |
|---|---|---|---|
| >0.95 | 5 | 0 | 5 + 0 = **5** |
| 0.95 | 4 | 0 | 4 + 0 = **4** |
| 0.90 | 3 | 0 | 3 + 0 = **3** ← minimum |
| 0.80 | 3 | 1 | 3 + 20 = 23 |
| 0.70 | 2 | 1 | 2 + 20 = 22 |
| 0.55 | 1 | 1 | 1 + 20 = 21 |
| 0.45 | 1 | 2 | 1 + 40 = 41 |
| 0.40 | 0 | 2 | 0 + 40 = 40 |
| 0.05 | 0 | 5 | 0 + 100 = 100 |

The cost-minimising threshold is **0.90**, not 0.5. At 0.90 the filter junks only two emails, both genuinely spam, and lets three spam through. That is the right answer when losing a real email is 20× worse than seeing a junk one — and it is exactly what the formula predicts:

$$ t^{*} = \frac{C_{FP}}{C_{FP} + C_{FN}} = \frac{20}{20 + 1} = 0.952 $$

The nearest achievable threshold below 0.952 in our ten-item list is 0.95, and 0.90 ties with it in this coarse grid. Theory and sweep agree again.

---

## 💻 Hands-On

One script, `fraud_bench.py`. It builds a 1%-positive dataset, produces the full metrics report, sweeps the threshold against the cost matrix, and cross-validates with error bars.

```bash
pip install "numpy>=1.26" "pandas>=2.0" "scikit-learn>=1.4" matplotlib seaborn
```

```python
"""fraud_bench.py — a complete evaluation report for an imbalanced classifier."""
import matplotlib
matplotlib.use("Agg")                      # save figures instead of opening windows
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, average_precision_score,
                             classification_report, confusion_matrix, f1_score,
                             precision_recall_curve, precision_score, recall_score,
                             roc_auc_score, roc_curve)
from sklearn.model_selection import (KFold, StratifiedKFold, cross_val_score,
                                     train_test_split)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RS = 42
C_FN = 500.0        # a missed fraud costs 500
C_FP = 10.0         # a false alarm costs 10  -> a miss is 50x worse


def rule(t):
    print("\n" + "=" * 66)
    print(t)
    print("=" * 66)


# ------------------------------------------------------------------ 1. DATA
def make_transactions(n=20000, seed=3):
    rng = np.random.default_rng(seed)
    amount = np.round(np.exp(rng.normal(3.2, 1.0, n)), 2)
    hour = rng.integers(0, 24, n)
    n_txn_24h = rng.poisson(4, n)
    acct_age_days = rng.integers(1, 2000, n)
    foreign = (rng.random(n) < 0.07).astype(int)
    dist = np.round(np.abs(rng.normal(0, 40, n)), 1)
    score = (-6.9
             + 0.010 * amount
             + 1.6 * foreign
             + 0.22 * n_txn_24h
             + 1.4 * ((hour <= 4) | (hour >= 23))
             - 0.0012 * acct_age_days
             + 0.020 * dist
             + rng.normal(0, 0.6, n))
    fraud = (rng.random(n) < 1 / (1 + np.exp(-score))).astype(int)
    return pd.DataFrame({"amount": amount, "hour": hour, "n_txn_24h": n_txn_24h,
                         "acct_age_days": acct_age_days, "foreign": foreign,
                         "dist_from_home_km": dist, "fraud": fraud})


df = make_transactions()
y = df["fraud"]
X = df.drop(columns="fraud")

rule("DATA")
print(f"rows: {len(df)}   frauds: {int(y.sum())}   fraud rate: {y.mean():.4%}")

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.30, random_state=RS, stratify=y)
print(f"train {len(y_tr)} ({int(y_tr.sum())} frauds)   "
      f"test {len(y_te)} ({int(y_te.sum())} frauds)")

# ------------------------------------------------------------------ 2. MODEL
pipe = Pipeline([("scale", StandardScaler()),
                 ("model", LogisticRegression(max_iter=2000, random_state=RS))])
pipe.fit(X_tr, y_tr)
prob = pipe.predict_proba(X_te)[:, 1]

# ------------------------------------------------------------- 3. THE PARADOX
rule("THE ACCURACY PARADOX")
pred50 = (prob >= 0.50).astype(int)
print(f"model accuracy @0.50    : {accuracy_score(y_te, pred50):.4f}")
print(f"'always legit' accuracy : {(y_te == 0).mean():.4f}")
print(f"the entire model is worth: {accuracy_score(y_te, pred50) - (y_te == 0).mean():+.4f}"
      " accuracy points")

# ------------------------------------------------------- 4. METRICS @ 0.50
rule("FULL METRICS AT THE DEFAULT THRESHOLD 0.50")
cm = confusion_matrix(y_te, pred50)
tn, fp, fn, tp = cm.ravel()
print("confusion matrix  [[TN FP] [FN TP]]:")
print(cm)
print(f"\nTN={tn}  FP={fp}  FN={fn}  TP={tp}\n")
print(f"accuracy    = (TP+TN)/N   = ({tp}+{tn})/{len(y_te)}   = {accuracy_score(y_te, pred50):.4f}")
print(f"precision   = TP/(TP+FP)  = {tp}/({tp}+{fp})   = {precision_score(y_te, pred50, zero_division=0):.4f}")
print(f"recall      = TP/(TP+FN)  = {tp}/({tp}+{fn})   = {recall_score(y_te, pred50):.4f}")
print(f"specificity = TN/(TN+FP)  = {tn}/({tn}+{fp}) = {tn / (tn + fp):.4f}")
print(f"F1          = 2PR/(P+R)                    = {f1_score(y_te, pred50, zero_division=0):.4f}")
print(f"ROC-AUC     (threshold-free)               = {roc_auc_score(y_te, prob):.4f}")
print(f"avg precision (PR-AUC)                     = {average_precision_score(y_te, prob):.4f}")
print(f"  ...compare AP against the no-skill baseline = positive rate = {y_te.mean():.4f}")
print("\n" + classification_report(y_te, pred50, digits=3, zero_division=0,
                                   target_names=["legit", "fraud"]))
print("IN ENGLISH: of the last 6000 transactions, 57 were fraud.")
print(f"            We caught {tp}. We missed {fn}. We wrongly bothered {fp} honest customers.")

# --------------------------------------------------- 5. THRESHOLD VS COST
rule("THRESHOLD SWEEP AGAINST THE COST MATRIX")
print(f"cost of a missed fraud (FN) = {C_FN:.0f}")
print(f"cost of a false alarm  (FP) = {C_FP:.0f}")
print(f"theoretical optimum t* = C_FP/(C_FP+C_FN) = {C_FP:.0f}/{C_FP + C_FN:.0f}"
      f" = {C_FP / (C_FP + C_FN):.4f}\n")

rows = []
for t in np.round(np.arange(0.002, 1.000, 0.002), 3):
    p = (prob >= t).astype(int)
    tn_, fp_, fn_, tp_ = confusion_matrix(y_te, p, labels=[0, 1]).ravel()
    rows.append({"threshold": t, "TP": tp_, "FP": fp_, "FN": fn_, "TN": tn_,
                 "precision": tp_ / (tp_ + fp_) if tp_ + fp_ else 0.0,
                 "recall": tp_ / (tp_ + fn_) if tp_ + fn_ else 0.0,
                 "cost": C_FN * fn_ + C_FP * fp_})
sweep = pd.DataFrame(rows)

show = [0.002, 0.006, 0.010, 0.014, 0.018, 0.020, 0.024, 0.030, 0.050, 0.100, 0.300, 0.500]
print(sweep[sweep.threshold.isin(show)].round(4).to_string(index=False))

best = sweep.loc[sweep["cost"].idxmin()]
print(f"\nBEST THRESHOLD = {best.threshold:.3f}   cost = {best.cost:,.0f}")
print(f"  arithmetic: {C_FN:.0f} x {int(best.FN)} FN + {C_FP:.0f} x {int(best.FP)} FP"
      f" = {C_FN * best.FN:,.0f} + {C_FP * best.FP:,.0f} = {best.cost:,.0f}")

cost_at_half = float(sweep.loc[sweep.threshold == 0.500, "cost"].iloc[0])
never = C_FN * int(y_te.sum())
always = C_FP * int((y_te == 0).sum())
print(f"\ncomparison of policies:")
print(f"  flag nothing            : {never:>10,.0f}")
print(f"  flag everything         : {always:>10,.0f}")
print(f"  model @ default 0.500   : {cost_at_half:>10,.0f}")
print(f"  model @ tuned {best.threshold:.3f}     : {best.cost:>10,.0f}")
print(f"  saving vs default       : {cost_at_half - best.cost:>10,.0f}")

# ------------------------------------------------------- 6. CROSS-VALIDATION
rule("5-FOLD STRATIFIED CROSS-VALIDATION (mean +/- std)")
skf = StratifiedKFold(5, shuffle=True, random_state=0)
kf = KFold(5, shuffle=True, random_state=0)
print("positives per test fold, KFold          :",
      [int(y.iloc[te].sum()) for _, te in kf.split(X, y)])
print("positives per test fold, StratifiedKFold:",
      [int(y.iloc[te].sum()) for _, te in skf.split(X, y)])
print()
for metric in ["roc_auc", "average_precision", "recall", "precision", "f1"]:
    s = cross_val_score(pipe, X, y, cv=skf, scoring=metric)
    print(f"{metric:>18s}: {s.mean():.4f} +/- {s.std():.4f}   folds={np.round(s, 4).tolist()}")

# ------------------------------------------------------------- 7. FIGURES
fig, ax = plt.subplots(2, 2, figsize=(12, 9))

sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax[0, 0],
            xticklabels=["pred legit", "pred fraud"],
            yticklabels=["true legit", "true fraud"])
ax[0, 0].set_title("Confusion matrix @ threshold 0.50")

fpr, tpr, _ = roc_curve(y_te, prob)
ax[0, 1].plot(fpr, tpr, lw=2, label=f"AUC = {roc_auc_score(y_te, prob):.3f}")
ax[0, 1].plot([0, 1], [0, 1], "k:", label="random = 0.500")
ax[0, 1].set_xlabel("false positive rate")
ax[0, 1].set_ylabel("true positive rate (recall)")
ax[0, 1].set_title("ROC curve")
ax[0, 1].legend()

prec, rec, _ = precision_recall_curve(y_te, prob)
ax[1, 0].plot(rec, prec, lw=2,
              label=f"AP = {average_precision_score(y_te, prob):.3f}")
ax[1, 0].axhline(y_te.mean(), ls=":", c="k",
                 label=f"no-skill = {y_te.mean():.4f}")
ax[1, 0].set_xlabel("recall")
ax[1, 0].set_ylabel("precision")
ax[1, 0].set_title("Precision-Recall curve")
ax[1, 0].legend()

ax[1, 1].plot(sweep.threshold, sweep.cost, lw=2)
ax[1, 1].axvline(best.threshold, c="r", ls="--",
                 label=f"min cost @ t={best.threshold:.3f}")
ax[1, 1].axvline(C_FP / (C_FP + C_FN), c="g", ls=":",
                 label=f"theory t*={C_FP / (C_FP + C_FN):.4f}")
ax[1, 1].set_xscale("log")
ax[1, 1].set_xlabel("threshold (log scale)")
ax[1, 1].set_ylabel("expected cost")
ax[1, 1].set_title("Cost vs threshold")
ax[1, 1].legend()

plt.tight_layout()
plt.savefig("fraud_bench.png", dpi=120)
print("\nsaved -> fraud_bench.png")
```

Run it:

```bash
python fraud_bench.py
```

Expected output:

```
==================================================================
DATA
==================================================================
rows: 20000   frauds: 190   fraud rate: 0.9500%
train 14000 (133 frauds)   test 6000 (57 frauds)

==================================================================
THE ACCURACY PARADOX
==================================================================
model accuracy @0.50    : 0.9908
'always legit' accuracy : 0.9905
the entire model is worth: +0.0003 accuracy points

==================================================================
FULL METRICS AT THE DEFAULT THRESHOLD 0.50
==================================================================
confusion matrix  [[TN FP] [FN TP]]:
[[5941    2]
 [  53    4]]

TN=5941  FP=2  FN=53  TP=4

accuracy    = (TP+TN)/N   = (4+5941)/6000   = 0.9908
precision   = TP/(TP+FP)  = 4/(4+2)   = 0.6667
recall      = TP/(TP+FN)  = 4/(4+53)   = 0.0702
specificity = TN/(TN+FP)  = 5941/(5941+2) = 0.9997
F1          = 2PR/(P+R)                    = 0.1270
ROC-AUC     (threshold-free)               = 0.8895
avg precision (PR-AUC)                     = 0.1931
  ...compare AP against the no-skill baseline = positive rate = 0.0095

              precision    recall  f1-score   support

       legit      0.991     1.000     0.995      5943
       fraud      0.667     0.070     0.127        57

    accuracy                          0.991      6000
   macro avg      0.829     0.535     0.561      6000
weighted avg      0.988     0.991     0.987      6000

IN ENGLISH: of the last 6000 transactions, 57 were fraud.
            We caught 4. We missed 53. We wrongly bothered 2 honest customers.
```

Sit with that. **ROC-AUC is 0.8895** — the model genuinely knows something; it ranks frauds above legit transactions most of the time. And at the default threshold it catches **4 out of 57**. Both facts are true simultaneously. The model isn't broken. The *threshold* is wrong.

```
==================================================================
THRESHOLD SWEEP AGAINST THE COST MATRIX
==================================================================
cost of a missed fraud (FN) = 500
cost of a false alarm  (FP) = 10
theoretical optimum t* = C_FP/(C_FP+C_FN) = 10/510 = 0.0196

 threshold  TP   FP  FN   TN  precision  recall     cost
     0.002  56 4417   1 1526     0.0125  0.9825  44670.0
     0.006  53 2026   4 3917     0.0255  0.9298  22260.0
     0.010  46 1187  11 4756     0.0373  0.8070  17370.0
     0.014  41  774  16 5169     0.0503  0.7193  15740.0
     0.018  39  542  18 5401     0.0671  0.6842  14420.0
     0.020  37  472  20 5471     0.0727  0.6491  14720.0
     0.024  35  365  22 5578     0.0875  0.6140  14650.0
     0.030  30  264  27 5679     0.1020  0.5263  16140.0
     0.050  19  134  38 5809     0.1242  0.3333  20340.0
     0.100  15   42  42 5901     0.2632  0.2632  21420.0
     0.300   5    6  52 5937     0.4545  0.0877  26060.0
     0.500   4    2  53 5941     0.6667  0.0702  26520.0

BEST THRESHOLD = 0.018   cost = 14,420
  arithmetic: 500 x 18 FN + 10 x 542 FP = 9,000 + 5,420 = 14,420

comparison of policies:
  flag nothing            :     28,500
  flag everything         :     59,430
  model @ default 0.500   :     26,520
  model @ tuned 0.018     :     14,420
  saving vs default       :     12,100
```

Four results worth stating out loud:

1. **The tuned threshold (0.018) is almost exactly the theoretical optimum (0.0196).** Independent confirmation that the sweep found a real minimum and the probabilities aren't wildly miscalibrated.
2. **Recall goes from 0.070 to 0.684.** We now catch 39 of 57 frauds instead of 4.
3. **Precision collapses from 0.667 to 0.067.** Of every 15 transactions we flag, 14 are innocent. That sounds terrible — and it is *correct*, because a false alarm costs 10 and a miss costs 500. If you had optimised F1, which weights precision and recall equally, you would have chosen a much higher threshold and burned money.
4. **The default threshold of 0.5 is barely better than flagging nothing** (26,520 vs 28,500). Almost the entire value of the model was locked behind a number nobody chose deliberately.

```
==================================================================
5-FOLD STRATIFIED CROSS-VALIDATION (mean +/- std)
==================================================================
positives per test fold, KFold          : [37, 30, 39, 49, 35]
positives per test fold, StratifiedKFold: [38, 38, 38, 38, 38]

           roc_auc: 0.8405 +/- 0.0084   folds=[0.8411, 0.8563, 0.8322, 0.8374, 0.8356]
 average_precision: 0.2165 +/- 0.0543   folds=[0.1784, 0.2729, 0.1431, 0.2843, 0.2038]
            recall: 0.0895 +/- 0.0394   folds=[0.0789, 0.0789, 0.0263, 0.1316, 0.1316]
         precision: 0.8929 +/- 0.1317   folds=[0.75, 1.0, 1.0, 1.0, 0.7143]
                f1: 0.1591 +/- 0.0655   folds=[0.1429, 0.1463, 0.0513, 0.2326, 0.2222]

saved -> fraud_bench.png
```

Compare the error bars. AUC: ±0.0084, tight, trustworthy. Recall at threshold 0.5: ±0.0394 on a mean of 0.0895 — the standard deviation is **44% of the mean**. One fold reported 0.0263 and another 0.1316. Same model, same features, same code. If you had run one 80/20 split and got the lucky fold, you would be reporting a model five times better than reality.

`sklearn`'s built-in `recall` and `precision` scorers always use threshold 0.5, which is why they are so unstable here. Threshold-free metrics (`roc_auc`, `average_precision`) are what you cross-validate; the threshold itself is tuned afterwards on a held-out set.

---

## ✍️ Practice

### [Warm-up] 1 — Confusion matrix by hand
A COVID rapid test is given to 500 people. 40 actually have the virus. The test comes back positive for 46 people, and 34 of those 46 really do have it.
(a) Build the 2×2 confusion matrix (label all four cells).
(b) Compute accuracy, precision, recall, specificity, and F1, showing the substitution for each.
(c) Write one sentence for a non-technical reader describing what the false negatives mean here.
(d) Which error would you rather make in a hospital screening context, and which in a "do I need to skip a party" context? Explain why the answers differ.

**Done looks like:** a labelled matrix, five metrics with arithmetic shown, and two clearly different answers to (d) with reasons.

### [Warm-up] 2 — Read the trade-off
Using the ten-email table from the Worked Example, answer without running code:
(a) Which threshold gives precision exactly 1.000 with the highest possible recall?
(b) Which threshold gives recall exactly 1.000 with the highest possible precision?
(c) At which threshold is F1 highest? Show the F1 arithmetic for the three best candidates.
(d) If a missed spam cost 5 and a junked real email cost 1, what threshold minimises cost? Show the cost column.

**Done looks like:** four thresholds, the F1 arithmetic for three candidates, and a cost column of at least six rows.

### [Build] 3 — Cost sensitivity analysis
The business gave you C_FN = 500 and C_FP = 10, but they were guessing. Re-run the sweep for five cost ratios — 5:1, 10:1, 50:1, 200:1, 1000:1 — and produce a table with columns: ratio, theoretical t*, empirical best t, TP, FP, FN, recall, precision, minimum cost.

**Done looks like:** a five-row table, a plot of chosen threshold versus cost ratio, and one sentence on how much the answer would change if the business's 500 estimate were off by a factor of two. (This sentence is the real deliverable — it tells you whether to argue about the number or move on.)

### [Build] 4 — Beat threshold tuning with class weights
`LogisticRegression(class_weight="balanced")` re-weights the training loss so rare positives count more. Fit it, then compare against the plain model at three operating points: default 0.5, the cost-optimal threshold for each model, and equal recall. Report the confusion matrix and total cost for each.

**Done looks like:** a comparison table of at least four rows, and a written verdict on whether class weighting, threshold tuning, or both together gives the lowest cost — with the numbers to back it.

### [Stretch] 5 — Cross-validate the threshold itself
Everything so far tuned the threshold on a single test set — which is the Module 1 sin of choosing on data you then report. Fix it: build a nested procedure where, for each of 5 outer folds, you (i) split the outer training data into an inner train and inner tune set, (ii) fit on inner train, (iii) pick the cost-optimal threshold on inner tune, (iv) apply that frozen threshold to the outer test fold and record the cost. Report mean ± std of the outer cost, and the 5 chosen thresholds.

**Done looks like:** five thresholds, five costs, a mean ± std, and one sentence comparing the honest nested cost to the optimistic single-split cost from the Hands-On.

### [Stretch] 6 — Calibration check
A probability of 0.30 should mean "roughly 30% of things I score at 0.30 turn out positive." Test whether that's true. Bin the test-set predicted probabilities into 10 quantile bins; for each bin plot the mean predicted probability (x) against the observed fraction of positives (y). A perfectly calibrated model sits on the diagonal. Use `sklearn.calibration.calibration_curve(y_te, prob, n_bins=10, strategy="quantile")`. Then wrap the pipeline in `CalibratedClassifierCV(pipe, method="isotonic", cv=5)`, redo the plot, and re-derive the cost-optimal threshold.

**Done looks like:** two calibration plots, the two cost-optimal thresholds, and a sentence on whether calibration moved the empirical optimum closer to the theoretical 0.0196.

---

## 🤔 Think Deeper

**1. Who chose C_FN = 500 and C_FP = 10, and what did they leave out?**
The 500 covers the bank's chargeback. It does not cover the customer's afternoon spent on hold, the hotel booking that fell through, or the fact that a card declined at a petrol station in the rain is a worse experience for some people than others.
*How to reason about it:* List everyone the two error types touch — bank, customer, merchant, fraud analyst. Note that the bank writes the cost matrix and also pays the FN cost, while the customer pays most of the FP cost and has no vote. Ask what a cost matrix would look like if the affected customers wrote it, and what mechanism could get their number into the calculation.

**2. Should the threshold be the same for everybody?**
A single global threshold treats every customer identically. You could instead use a lower threshold for accounts with high historical fraud, or a higher one for long-standing customers. That improves total cost.
*How to reason about it:* Work out who ends up flagged more often under a per-group threshold, and check whether those groups correlate with things it would be illegal or wrong to discriminate on. Consider that "accounts with high historical fraud" may reflect where fraud was *investigated*, not where it happened. Then ask the harder version: if a uniform threshold produces unequal outcomes across groups anyway, is uniformity actually fairness, or just the appearance of it?

**3. What happens to your metrics when the model changes the world it measures?**
Deploy a good fraud model and fraudsters adapt — they test small amounts, avoid foreign flags, mimic normal hours. Your test-set AUC of 0.89 was measured against fraudsters who had never seen your model.
*How to reason about it:* Distinguish a static prediction problem (predicting rainfall; the sky doesn't retaliate) from an adversarial one. Ask what number would tell you the distribution has shifted, and how you'd measure recall at all once the model is blocking the very transactions you'd need to label. Consider deliberately letting a small random sample through unflagged as a measurement channel — and then ask what that sample costs, and whether you'd sign off on it.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Reporting accuracy on a 1%-positive problem | Accuracy is the default `.score()` and 99% feels like success | Always print the majority-class rate beside it; lead with AUC, AP, precision, and recall |
| Treating 0.5 as the correct threshold | It's the default in `.predict()` and nobody flags it as a decision | Use `predict_proba` and choose the threshold from your cost matrix |
| Confusing precision and recall | The names give no hint which is which | Precision reads down the **predicted-positive column**; recall reads across the **actual-positive row** |
| Indexing the confusion matrix by memory | Row/column conventions differ across books, papers, and libraries | `tn, fp, fn, tp = confusion_matrix(y, p).ravel()` — always unpack, always name |
| Optimising F1 when the error costs are wildly unequal | F1 is the standard "balanced" metric so it feels neutral | F1 assumes precision and recall matter equally. If a miss costs 50×, use expected cost |
| Using ROC-AUC on heavily imbalanced data as the only number | AUC is the most-cited metric | With a huge TN count, FPR barely moves. Report average precision as well |
| Reporting a single validation score with no spread | One number looks decisive; two numbers look uncertain | 5-fold CV and report mean ± std. Uncertainty is information, not weakness |
| Plain `KFold` on rare-positive data | It's the default splitter | `StratifiedKFold` — otherwise fold composition varies more than the model does |
| Tuning the threshold on the same data you report the score from | It's the only labelled data in front of you | Tune on validation (or an inner CV fold), report on the untouched test set |
| Comparing average precision to 0.5 | ROC's baseline is 0.5, so AP's must be too | AP's no-skill baseline is the **positive class rate** — 0.0095 here, so AP = 0.19 is 20× baseline |
| Cross-validating `recall` and drawing conclusions | It's an available scorer string | Threshold-dependent scorers at a fixed 0.5 are extremely noisy on rare classes. CV the threshold-free metrics |

---

## 🛠️ Mini-Project — Fraud Bench

**Goal.** Produce a complete, decision-ready evaluation report for a 1%-positive classifier: full metrics at the default threshold, a threshold chosen by explicit expected-cost arithmetic (not by eye, not by F1), and 5-fold cross-validated results with error bars.

**Time:** 90–120 minutes.

### Starter steps

1. Build `fraud_bench.py` section by section, running after each. Confirm the fraud rate is close to 0.95% before going further.
2. **Print the paradox first.** Model accuracy and majority-class accuracy on adjacent lines. Everything after this exists because of that gap.
3. Produce the full metric block at t = 0.50, and write the "IN ENGLISH" line: how many caught, how many missed, how many honest customers bothered. If you can't write that sentence, you don't understand your own confusion matrix.
4. Write the cost matrix as two named constants at the top of the file, with a comment saying who supplied the numbers. Never bury a cost inside an expression.
5. Compute the theoretical t* = C_FP/(C_FP + C_FN) and **print it before you sweep**, so you can't accidentally rationalise whatever the sweep returns.
6. Sweep t from 0.002 to 0.998 in steps of 0.002. Print the full cost arithmetic for the winner: `500 × 18 + 10 × 542 = 14,420`.
7. Add the three reference policies — flag nothing, flag everything, model at 0.5 — so the saving is visible in currency, not in metric points.
8. Run 5-fold stratified CV on `roc_auc` and `average_precision` and print mean ± std with the per-fold list.
9. Save the four-panel figure: confusion heatmap, ROC, PR curve, and cost-vs-threshold with both the empirical and theoretical thresholds marked.
10. Write `EVALUATION_REPORT.md`: the paradox, the metric table, the chosen threshold with its arithmetic, the CV results with error bars, and a one-paragraph recommendation to the business.

### Success criteria checklist

- [ ] The positive rate is printed and is close to 1%.
- [ ] Model accuracy and majority-class accuracy appear on adjacent lines with the difference computed.
- [ ] The confusion matrix is printed with all four cells explicitly labelled TN/FP/FN/TP.
- [ ] Precision, recall, specificity, F1, ROC-AUC, and average precision are all reported.
- [ ] Average precision is compared against the positive-class rate, **not** against 0.5.
- [ ] The cost matrix appears as named constants with a source comment.
- [ ] The theoretical t* is printed **before** the sweep results.
- [ ] The chosen threshold comes from `sweep["cost"].idxmin()` — not from looking at a plot.
- [ ] The winning threshold's cost arithmetic is printed in full: `C_FN × FN + C_FP × FP = total`.
- [ ] Costs for flag-nothing, flag-everything, default-0.5, and tuned are all shown.
- [ ] 5-fold **stratified** CV is reported as mean ± std with per-fold values.
- [ ] The four-panel figure is saved and both thresholds are marked on the cost panel.
- [ ] `EVALUATION_REPORT.md` contains a recommendation a non-technical manager could act on.

### Level it up

Add a **capacity constraint**, which is what makes this real. Your fraud team can review exactly **200 transactions per day**, and the test set represents one day. Now the question changes from "what threshold minimises cost?" to "given that we can only review 200, which 200 should they be, and what does that policy cost?" Compute:

- the threshold that flags exactly 200,
- recall and precision at that operating point (**precision@200** and **recall@200**),
- the cost, given that any fraud you don't review is a full-price FN,
- and the marginal value of the 201st analyst-hour: how much does total cost fall if capacity rises to 250?

Write one sentence you would actually send to the head of operations, containing a number, a recommendation, and a caveat.

---

## 🔑 Key Takeaways

- **Accuracy is the wrong headline whenever one class is rare.** Our model's entire contribution over guessing was +0.0003 accuracy points, and it still had genuine predictive skill.
- **Four numbers — TP, FP, FN, TN — generate every metric that matters.** Learn to read precision down the column and recall across the row, and you never need to memorise a formula.
- **Name your errors in the language of the application.** Not "53 false negatives" but "we missed 53 frauds and 2 honest customers got called." That sentence is what changes decisions.
- **0.5 is a default, not an answer.** Moving our threshold to 0.018 took recall from 0.070 to 0.684 and cut cost by 46%, without retraining anything.
- **ROC-AUC and average precision describe the same predictions differently.** AUC 0.89 says the ranking is good; AP 0.19 says most of what you flag will be innocent. Report both when positives are rare.
- **A threshold chosen from a cost matrix is defensible; one chosen by eye is not.** And `t* = C_FP/(C_FP + C_FN)` gives you a theoretical check on your empirical sweep.
- **Report mean ± std, always.** Our AUC was stable at ±0.008 while recall@0.5 wobbled by 44% of its own mean. A single number hides which one you're looking at.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Class imbalance** | One answer is far more common than the other | 190 frauds in 20,000 transactions |
| **Accuracy paradox** | A useless model looking great because the common class dominates | 99.05% by always saying "not fraud" |
| **True positive (TP)** | It was positive and you said positive | caught a real fraud |
| **False positive (FP)** | It was negative and you said positive — a false alarm | honest customer's card declined |
| **False negative (FN)** | It was positive and you said negative — a miss | fraud went through |
| **True negative (TN)** | It was negative and you said negative | normal purchase, left alone |
| **Confusion matrix** | The 2×2 table of those four counts | `[[5941, 2], [53, 4]]` |
| **Precision** | Of what you flagged, how much was right | 4/(4+2) = 0.667 |
| **Recall (sensitivity)** | Of everything that was really positive, how much you caught | 4/(4+53) = 0.070 |
| **Specificity** | Of everything really negative, how much you correctly left alone | 5941/5943 = 0.9997 |
| **F1 score** | Harmonic mean of precision and recall; punishes lopsidedness | 0.127 |
| **Decision threshold** | The probability cut-off for calling something positive | 0.5 by default; 0.018 after tuning |
| **ROC curve** | Recall plotted against false positive rate as the threshold sweeps | AUC 0.8895 |
| **AUC** | Chance a random positive outranks a random negative; 0.5 = random | 21/25 = 0.84 in the worked example |
| **Precision-recall curve** | Precision plotted against recall; its area is average precision | AP 0.1931 |
| **Average precision (AP)** | PR-curve summary; its no-skill baseline is the positive rate | 0.1931 vs baseline 0.0095 |
| **k-fold cross-validation** | Score k times on k different held-out chunks, report the spread | AUC 0.8405 ± 0.0084 |
| **Stratified k-fold** | k-fold that keeps class proportions equal in every fold | 38 frauds in every fold |
| **Cost matrix** | The price attached to each kind of error | FN = 500, FP = 10 |
| **Expected cost** | `C_FN × FN + C_FP × FP` at a given threshold | 500(18) + 10(542) = 14,420 |
| **Calibration** | Whether a predicted 0.3 really happens 30% of the time | checked with a reliability curve |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1 — Confusion matrix by hand

500 people, 40 truly infected, 46 test positive, 34 of those are true positives.

**(a) The matrix.**

- TP = 34 (infected, tested positive)
- FP = 46 − 34 = **12** (healthy, tested positive)
- FN = 40 − 34 = **6** (infected, tested negative)
- TN = 500 − 34 − 12 − 6 = **448** (healthy, tested negative)

Check: 34 + 12 + 6 + 448 = 500 ✅

```
                      PREDICTED
                 negative   positive
ACTUAL healthy │   448    │    12   │ = 460
      infected │     6    │    34   │ =  40
               └──────────┴─────────┘
                   454        46
```

**(b) Metrics.**

| Metric | Substitution | Value |
|---|---|---|
| Accuracy | (34 + 448) / 500 = 482/500 | **0.9640** |
| Precision | 34 / (34 + 12) = 34/46 | **0.7391** |
| Recall | 34 / (34 + 6) = 34/40 | **0.8500** |
| Specificity | 448 / (448 + 12) = 448/460 | **0.9739** |
| F1 | 2(0.7391)(0.8500) / (0.7391 + 0.8500) = 1.25652 / 1.58913 | **0.7907** |

**(c) In plain English.** "Six people who had the virus were told they didn't. They went back to work, to school, and to see their grandparents, believing they were safe."

**(d) Which error is worse depends entirely on what happens next.**

*Hospital screening:* false negatives are far worse. An infected patient waved through into a ward with immunocompromised people can start an outbreak. A false positive costs one confirmatory PCR test and a day of isolation. You want **recall**, and you'd lower the threshold to get it.

*"Do I skip a party?":* a false positive is now the expensive error — you miss your friend's birthday for nothing. A false negative means you attend while mildly contagious, which is bad but bounded. Many people would tolerate more misses here. You'd care more about **precision**.

The deeper point: it is the **same test, the same 34/12/6/448**. The numbers didn't change. What changed is who bears the cost of each error and how large that cost is. A metric is never a property of a model alone; it is a property of a model plus a decision plus a context.

### 2 — Read the trade-off

Using the sweep table from the Worked Example.

**(a) Precision 1.000 with the highest recall:** **t = 0.90**. Both t = 0.95 and t = 0.90 give precision 1.000, but 0.90 flags two spam instead of one, so recall is 0.4 rather than 0.2. Any lower threshold pulls in the ham at 0.80 and precision drops to 0.667.

**(b) Recall 1.000 with the highest precision:** **t = 0.40**. That is the first threshold that captures the lowest-scored spam (#7 at 0.40). At that point FP = 2 and precision = 5/7 = **0.714**. Going lower only adds ham and lowers precision further.

**(c) Highest F1.** Three candidates:

| t | P | R | F1 arithmetic | F1 |
|---|---|---|---|---|
| 0.55 | 0.800 | 0.800 | 2(0.800)(0.800)/(1.600) = 1.28/1.6 | **0.8000** |
| 0.40 | 0.714 | 1.000 | 2(0.714)(1.000)/(1.714) = 1.42857/1.71429 | **0.8333** |
| 0.70 | 0.750 | 0.600 | 2(0.750)(0.600)/(1.350) = 0.90/1.35 | 0.6667 |

**t = 0.40 wins with F1 = 0.8333.** Note this is *not* the default 0.5 and it is *not* the balanced-looking 0.800/0.800 point — F1 is happy to trade a little precision for a lot of recall.

**(d) Cost with C_FN = 5 (missed spam), C_FP = 1 (junked real email).** Now misses are the expensive error, so the threshold should go **down**.

| t | FN | FP | cost = 5·FN + 1·FP |
|---|---|---|---|
| 0.95 | 4 | 0 | 20 + 0 = 20 |
| 0.90 | 3 | 0 | 15 + 0 = 15 |
| 0.80 | 3 | 1 | 15 + 1 = 16 |
| 0.70 | 2 | 1 | 10 + 1 = 11 |
| 0.55 | 1 | 1 | 5 + 1 = 6 |
| 0.45 | 1 | 2 | 5 + 2 = 7 |
| **0.40** | **0** | **2** | **0 + 2 = 2** ← minimum |
| 0.30 | 0 | 3 | 0 + 3 = 3 |
| 0.20 | 0 | 4 | 0 + 4 = 4 |
| 0.05 | 0 | 5 | 0 + 5 = 5 |

**t = 0.40, cost 2.** Cross-check against the formula: t* = C_FP/(C_FP + C_FN) = 1/(1+5) = **0.167**. The nearest achievable operating point at or above 0.167 in this ten-item list is 0.20 (cost 4) — but 0.40 is cheaper here because the specific arrangement of this tiny sample has no spam between 0.20 and 0.40, so lowering the threshold below 0.40 buys nothing but false positives. With only ten samples the discrete grid is coarse and the theory is only approximate. With 6,000 samples, as in the Hands-On, they agree to within one grid step.

### 3 — Cost sensitivity analysis

```python
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

# assumes prob and y_te exist from fraud_bench.py

def sweep_for(c_fn, c_fp, prob, y_true, step=0.002):
    rows = []
    for t in np.round(np.arange(step, 1.0, step), 4):
        p = (prob >= t).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_true, p, labels=[0, 1]).ravel()
        rows.append((t, tp, fp, fn, tn, c_fn * fn + c_fp * fp))
    return pd.DataFrame(rows, columns=["t", "TP", "FP", "FN", "TN", "cost"])


out = []
for ratio in [5, 10, 50, 200, 1000]:
    c_fp, c_fn = 10.0, 10.0 * ratio
    s = sweep_for(c_fn, c_fp, prob, y_te)
    b = s.loc[s["cost"].idxmin()]
    out.append({"ratio": f"{ratio}:1",
                "theory_t*": c_fp / (c_fp + c_fn),
                "best_t": b.t, "TP": int(b.TP), "FP": int(b.FP), "FN": int(b.FN),
                "recall": b.TP / (b.TP + b.FN),
                "precision": b.TP / (b.TP + b.FP) if b.TP + b.FP else 0.0,
                "min_cost": b.cost})

tbl = pd.DataFrame(out)
print(tbl.round(4).to_string(index=False))

plt.figure(figsize=(6, 4))
plt.plot(tbl["ratio"], tbl["best_t"], "o-", label="empirical best t")
plt.plot(tbl["ratio"], tbl["theory_t*"], "s--", label="theory C_FP/(C_FP+C_FN)")
plt.yscale("log")
plt.xlabel("cost ratio  FN : FP")
plt.ylabel("chosen threshold (log)")
plt.legend()
plt.tight_layout()
plt.savefig("cost_sensitivity.png", dpi=120)
```

Expected pattern: as the ratio climbs from 5:1 to 1000:1, the theoretical t* falls from 1/6 ≈ 0.1667 down to 1/1001 ≈ 0.000999, and the empirical best threshold tracks it closely. Recall rises toward 1.0 and precision collapses toward the positive rate, exactly as it should — at 1000:1 you should be flagging almost everything suspicious.

**The sentence that matters:** if the business's 500 estimate is off by 2× (so the true ratio is 25:1 or 100:1 rather than 50:1), the optimal threshold moves from 0.0196 to roughly 0.0385 or 0.0099. Look up the *cost at the wrong threshold* in the sweep table for the true ratio and compare it to the minimum. You will find the cost curve is quite flat near its bottom, so the penalty for a 2× error in the cost estimate is small — a few percent. **Conclusion: stop arguing about whether it's 500 or 800, and go ship it.** Knowing when a parameter does not need to be precise is worth as much as knowing its value.

### 4 — Beat threshold tuning with class weights

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Continues from fraud_bench.py: X_tr, y_tr, X_te, y_te are already defined there.
C_FN, C_FP = 500.0, 10.0


def cost_at(prob, y_true, t):
    tn, fp, fn, tp = confusion_matrix(y_true, (prob >= t).astype(int), labels=[0, 1]).ravel()
    return dict(t=t, TP=tp, FP=fp, FN=fn, TN=tn,
                recall=tp / (tp + fn) if tp + fn else 0.0,
                precision=tp / (tp + fp) if tp + fp else 0.0,
                cost=C_FN * fn + C_FP * fp)


def best_t(prob, y_true):
    grid = np.round(np.arange(0.002, 1.0, 0.002), 4)
    scored = [cost_at(prob, y_true, t) for t in grid]
    return min(scored, key=lambda r: r["cost"])


plain = Pipeline([("s", StandardScaler()),
                  ("m", LogisticRegression(max_iter=2000, random_state=42))]).fit(X_tr, y_tr)
bal = Pipeline([("s", StandardScaler()),
                ("m", LogisticRegression(max_iter=2000, random_state=42,
                                         class_weight="balanced"))]).fit(X_tr, y_tr)
p_plain = plain.predict_proba(X_te)[:, 1]
p_bal = bal.predict_proba(X_te)[:, 1]

rows = [
    {"model": "plain",    **cost_at(p_plain, y_te, 0.5)},
    {"model": "balanced", **cost_at(p_bal,   y_te, 0.5)},
    {"model": "plain    + tuned t", **best_t(p_plain, y_te)},
    {"model": "balanced + tuned t", **best_t(p_bal,   y_te)},
]
print(pd.DataFrame(rows).round(4).to_string(index=False))
print(f"\nAUC plain    {roc_auc_score(y_te, p_plain):.4f}")
print(f"AUC balanced {roc_auc_score(y_te, p_bal):.4f}")
```

Expected results:

| model | t | TP | FP | FN | recall | precision | cost |
|---|---|---|---|---|---|---|---|
| plain | 0.500 | 4 | 2 | 53 | 0.070 | 0.667 | 26,520 |
| balanced | 0.500 | 46 | 1287 | 11 | 0.807 | 0.035 | 18,370 |
| plain + tuned | 0.018 | 39 | 542 | 18 | 0.684 | 0.067 | **14,420** |
| balanced + tuned | ~0.5 | ~46 | ~1287 | ~11 | ~0.81 | ~0.035 | ~18,000 |

**Verdict.** Class weighting at t = 0.5 (cost 18,370) beats the plain model at t = 0.5 (26,520) — that is real. But **plain + threshold tuning beats it** (14,420). And the AUCs are almost identical (0.8895 vs 0.8863), which tells you why: `class_weight="balanced"` does not make the model rank transactions better; it mostly shifts the intercept so that the default 0.5 lands somewhere more useful. Threshold tuning does the same job directly, with two advantages — you can change it after training without refitting, and you can state exactly which cost matrix produced it.

**Both together?** Tuning the threshold on the balanced model lands you near the same operating point, because both models rank almost identically and you're just choosing a point on the same curve. Once you tune the threshold, the class weight buys you almost nothing. Which is the general lesson: **class weighting and threshold tuning are two ways of moving along one curve. Ranking quality — AUC and AP — is what moves the curve itself.**

### 5 — Cross-validate the threshold itself

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Continues from fraud_bench.py: X, y, X_tr, y_tr, X_te, y_te are already defined there.
C_FN, C_FP = 500.0, 10.0
GRID = np.round(np.arange(0.002, 1.0, 0.002), 4)


def total_cost(y_true, prob, t):
    tn, fp, fn, tp = confusion_matrix(y_true, (prob >= t).astype(int), labels=[0, 1]).ravel()
    return C_FN * fn + C_FP * fp


def make_pipe():
    return Pipeline([("s", StandardScaler()),
                     ("m", LogisticRegression(max_iter=2000, random_state=42))])


outer = StratifiedKFold(5, shuffle=True, random_state=0)
chosen, costs, per_1000 = [], [], []

for k, (tr_idx, te_idx) in enumerate(outer.split(X, y), start=1):
    X_out_tr, y_out_tr = X.iloc[tr_idx], y.iloc[tr_idx]
    X_out_te, y_out_te = X.iloc[te_idx], y.iloc[te_idx]

    # inner split: fit on 75%, choose the threshold on the other 25%
    X_in_tr, X_in_tune, y_in_tr, y_in_tune = train_test_split(
        X_out_tr, y_out_tr, test_size=0.25, random_state=k, stratify=y_out_tr)

    m = make_pipe().fit(X_in_tr, y_in_tr)
    p_tune = m.predict_proba(X_in_tune)[:, 1]
    t_star = min(GRID, key=lambda t: total_cost(y_in_tune, p_tune, t))

    # refit on ALL outer-train data, then apply the FROZEN threshold to the outer fold
    m_full = make_pipe().fit(X_out_tr, y_out_tr)
    p_out = m_full.predict_proba(X_out_te)[:, 1]
    c = total_cost(y_out_te, p_out, t_star)

    chosen.append(t_star)
    costs.append(c)
    per_1000.append(c / len(y_out_te) * 1000)
    print(f"fold {k}: chosen t = {t_star:.3f}   outer cost = {c:>9,.0f}"
          f"   ({c / len(y_out_te) * 1000:,.0f} per 1000 txns)")

print(f"\nchosen thresholds: {chosen}")
print(f"outer cost per 1000 txns: mean {np.mean(per_1000):,.0f} +/- {np.std(per_1000):,.0f}")
```

Expected: the five chosen thresholds all land in the same neighbourhood as the theory (roughly 0.01–0.04), but they are *not* identical, because each was picked on a different ~3,500-row tune set containing only ~33 frauds. That variability is real and it is exactly what the single-split version hid from you.

**The comparison sentence.** The Hands-On reported 14,420 on 6,000 transactions = **2,403 per 1,000** — but that threshold was chosen *on the very test set it was scored on*, so it is the best of 499 grid points and therefore optimistic. The nested procedure's mean will be higher, and it comes with a standard deviation. **The nested number is the one you put in the model card**; the single-split number is the one you quietly stop quoting.

### 6 — Calibration check

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import average_precision_score, confusion_matrix, roc_auc_score

# Continues from fraud_bench.py and exercise 5 (which defines make_pipe()).
C_FN, C_FP = 500.0, 10.0
GRID = np.round(np.arange(0.002, 1.0, 0.002), 4)


def best_threshold(y_true, prob):
    def cost(t):
        tn, fp, fn, tp = confusion_matrix(y_true, (prob >= t).astype(int), labels=[0, 1]).ravel()
        return C_FN * fn + C_FP * fp
    t = min(GRID, key=cost)
    return t, cost(t)


calib = CalibratedClassifierCV(make_pipe(), method="isotonic", cv=5).fit(X_tr, y_tr)
p_cal = calib.predict_proba(X_te)[:, 1]

fig, ax = plt.subplots(1, 2, figsize=(11, 4.5), sharex=True, sharey=True)
for a, (p, name) in zip(ax, [(prob, "uncalibrated"), (p_cal, "isotonic")]):
    frac, mean_pred = calibration_curve(y_te, p, n_bins=10, strategy="quantile")
    a.plot(mean_pred, frac, "o-", label=name)
    a.plot([0, max(mean_pred) * 1.1], [0, max(mean_pred) * 1.1], "k:", label="perfect")
    a.set_xlabel("mean predicted probability")
    a.set_ylabel("observed fraction positive")
    a.set_title(name)
    a.legend()
plt.tight_layout()
plt.savefig("calibration.png", dpi=120)

for p, name in [(prob, "uncalibrated"), (p_cal, "isotonic")]:
    t, c = best_threshold(y_te, p)
    print(f"{name:>14s}: AUC {roc_auc_score(y_te, p):.4f}  AP {average_precision_score(y_te, p):.4f}"
          f"  best t {t:.3f}  cost {c:,.0f}")
print(f"theoretical t* = {C_FP / (C_FP + C_FN):.4f}")
```

**What to expect and how to read it.**

With 1% positives, all the action happens in the bottom-left corner of the calibration plot — use `strategy="quantile"` so the bins contain equal numbers of points rather than equal probability widths, otherwise nine of your ten bins will be empty.

Logistic regression on a well-specified linear problem is usually decently calibrated already, so the uncalibrated curve should sit close to the diagonal, and the fact that our empirical optimum (0.018) already agreed with theory (0.0196) is independent evidence of that. Isotonic regression on only 133 training frauds is fitting a step function from very few positives, so it may not improve things and can even overfit — a legitimate and useful finding to report.

**The sentence to write:** calibration matters because the cost formula t* = C_FP/(C_FP + C_FN) is a statement about *true* probabilities. If your model says 0.02 when the real rate is 0.10, the formula points you at the wrong threshold and the empirical sweep will disagree with theory. Here they agree to within one grid step, so the model's probabilities are good enough to trust the formula — which means on the next dataset you can compute the threshold before you even sweep, and use the sweep only as a check.

</details>

---

[⬅ Previous](module-02-feature-engineering.md) · [Level 3 Home](README.md) · [Next ➡](module-04-logistic-regression-gradient-descent.md)

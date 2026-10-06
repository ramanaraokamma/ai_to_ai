# Week 8 — Four Numbers That Tell You What Kind of Wrong

[⬅ Week 7](week-07.md) · [Course Home](../README.md) · [Week 9 ➡](week-09.md) · [Student Guide](../student-guide/week-08.md) · [Workbook](../workbook/week-08.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — four counts, two fractions, and the most useful table in this subject |
| **Big idea** | Accuracy hides *which* mistakes you made. Four counts — **caught**, **false alarm**, **miss**, **correctly left alone** — tell you what kind of wrong you are. |
| **New vocabulary** | true positive · false positive · false negative · true negative · confusion matrix · precision · recall · specificity · accuracy paradox |
| **New maths** | **None.** Two fractions with whole numbers on the top and bottom. Every one of them is done by hand, on paper, before any code runs. |
| **New syntax** | `make_classification(weights=[0.99, 0.01], random_state=0)` · `confusion_matrix(y, pred).ravel()` · `precision_score(y, pred)` / `recall_score(y, pred)` · `classification_report(y, pred)` |
| **Dataset** | `sklearn.datasets.make_classification` with `weights=[0.99, 0.01]`, `random_state=0` — a 5,000-row, 1.44%-fraud table generated inside scikit-learn. **Nothing downloads. No internet needed.** |
| **Materials** | **Forty index cards or slips of paper, cut before class** · four large labels for the piles (`caught`, `false alarm`, `miss`, `left alone`) · printed workbook pages 8.1–8.6 · a big sheet for the 2×2 on the wall · the Bug Log · last week's ablation table left up on the wall |
| **Tech needed** | Laptop with Python 3, numpy, pandas, scikit-learn. **No new installs.** Nothing this week needs `make_data.py`. |
| **Prep time** | 25 minutes the night before (10 of them cutting cards) · 5 minutes on the day |
| **Expected runtime of the code** | `fraud.py` **under 2 seconds** including generating 5,000 rows, fitting two models and printing everything. |

> **⚠️ Watch out:** the whole lesson turns on one moment — the model that scores **98.6%** and has caught **nothing**. If you explain the confusion matrix *before* that moment lands, the four cells become bookkeeping and the lesson dies. **Build the useless model first. Let them be pleased with it. Then ask how many frauds it caught.** The silence after that question is where the four cells become necessary.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Build a confusion matrix by hand** from a list of 30 predictions, and name all four cells **in the language of the application** — not "FP", but "a real customer's card was declined".
2. **Compute precision, recall and specificity** from those four counts, showing **which count went on the bottom of each fraction**.
3. **Demonstrate the accuracy paradox**: build a model that scores 98.6% and has never once said yes.
4. **Say which of a false positive and a false negative costs more** for a stated application, and why.

Observable evidence: a hand-drawn 2×2 from 30 given predictions with all four cells named in application language; three fractions with their numerators and denominators written out and the division done; `fraud.py`, which prints the paradox and then the four real counts; and two written sentences describing one false positive and one false negative as things that happen to a real person.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each one carries on from the one above. **The complete runnable file is in the Prep Checklist and the Answer Key.**

**There is no new mathematics this week.** There are two fractions, and both have whole numbers above and below the line. If you can work out "9 out of 15" you can teach this entire lesson. What you do need is the *sequence* — one idea has to land before the next makes sense — and about fifteen minutes with this section.

### 1. The one thing that makes this week necessary

Here is the problem, and it takes one minute to state.

Suppose one order in seventy is fraud. You build a model. It says "not fraud" to every single transaction, all day, for ever. It has no model inside it at all — it is a piece of paper with the word "no" written on it.

**Its accuracy is 98.6%.**

Not roughly. Exactly, on our data: 986 of the 1,000 validation rows really are legitimate, so answering "no" to all 1,000 gets 986 right.

```text
986 ÷ 1000 = 0.9860
```

Now here is the kicker, and it is the number that makes the week: **a real trained decision tree on the same 1,000 rows scores 98.20%. Which is lower. And it catches three frauds, while the piece of paper catches none.**

```text
982 ÷ 1000 = 0.9820      the real model
986 ÷ 1000 = 0.9860      the piece of paper
```

**Accuracy went down and the model got better.** That sentence is the whole lesson and it should feel wrong the first time you read it. Read it twice.

> **accuracy paradox** — when the positive class is rare, a model that never predicts it can score very high accuracy, and a genuinely useful model can score lower. Accuracy simply does not have the resolution to tell them apart.

![98.6% accurate, nothing caught](../figures/fig-w08-4-accuracy-paradox-98-percent-zero-caught.svg)
*Figure 8.1 — 98.6% accurate, nothing caught. Higher accuracy, zero frauds found.*

🍕 **The analogy that works, and it is worth saying out loud.** A smoke alarm that never goes off is correct on every single day your kitchen does not catch fire. That is thousands of days. Its accuracy is magnificent. It is wrong exactly once — on the one day anybody cares about.

### 2. The four counts, and the naming trick

Every single prediction lands in exactly one of four boxes. There is no fifth box.

> **True Positive (TP)** — it was fraud, you said fraud. **You caught one.**
>
> **True Negative (TN)** — it was legitimate, you said legitimate. **You correctly left it alone.**
>
> **False Positive (FP)** — it was legitimate, you said fraud. **A false alarm.**
>
> **False Negative (FN)** — it was fraud, you said legitimate. **A miss.**

> **confusion matrix** — the 2×2 table of those four counts.

**The naming trick, and teach it explicitly, because nobody guesses it.** Read the two words backwards:

- **the second word is what YOU predicted.** "Positive" means you said yes.
- **the first word is whether you were RIGHT.** "False" means you were wrong about it.

So a **false positive** is: *you predicted positive, and that was false.* You cried wolf.
A **false negative** is: *you predicted negative, and that was false.* The wolf walked past.

**Say the trick, then test it immediately.** Ask: *"the card was stolen and the model let it through. Which cell?"* (False negative: you said negative, you were wrong.) Ask three of these and it sticks for good.

Here are our real numbers, from a decision tree on 1,000 validation rows:

![Four cells, four names](../figures/fig-w08-1-confusion-matrix-four-cells-named.svg)
*Figure 8.2 — Four cells, four names. Rows are what happened; columns are what the model said.*

```text
                       PREDICTED
                 legit          fraud
ACTUAL  legit  │   979    │      7    │  = 986 real legit
        fraud  │    11    │      3    │  =  14 real fraud
               └──────────┴───────────┘
                   990          10
```

And the check that must always pass: **979 + 7 + 11 + 3 = 1000.** Make them do that addition every single time. A 2×2 whose cells do not add to the number of rows is a 2×2 with an arithmetic mistake in it, and this check catches it in five seconds.

⚠️ **The layout trap, and it will bite somebody.** `sklearn.metrics.confusion_matrix` puts **rows = what actually happened, columns = what the model said, class 0 first**:

```python
cm = confusion_matrix(y_true, y_pred)     # [[TN, FP],
                                          #  [FN, TP]]
tn, fp, fn, tp = cm.ravel()
```

Plenty of textbooks put positives first, or transpose the whole thing. **Never index into it blindly.** Always unpack with `.ravel()` into four named variables, in that order, and then use the names. `.ravel()` means "flatten this 2×2 grid into a list of four, reading left-to-right, top-to-bottom".

### 3. The two fractions — the same four numbers, read in two directions

This is the heart of the lesson and the place to slow right down. **Precision and recall are not two measurements. They are the same four numbers read once down and once across.**

> **Precision** = TP ÷ (TP + FP) — *"of everything I flagged, how much was really fraud?"* **Read down the predicted-fraud column.**

```text
3 ÷ (3 + 7)  =  3 ÷ 10  =  0.3000
```

![Precision reads down one column](../figures/fig-w08-2-precision-region-highlighted.svg)
*Figure 8.3 — Precision reads down one column. Of the 10 flagged, 3 were really fraud.*

> **Recall** = TP ÷ (TP + FN) — *"of everything that really was fraud, how much did I catch?"* **Read across the actual-fraud row.**

```text
3 ÷ (3 + 11)  =  3 ÷ 14  =  0.2143
```

![Recall reads across one row](../figures/fig-w08-3-recall-region-highlighted.svg)
*Figure 8.4 — Recall reads across one row. Of the 14 real frauds, 3 were caught.*

> **Specificity** = TN ÷ (TN + FP) — *"of everything that really was legitimate, how much did I correctly leave alone?"* **Read across the actual-legit row.**

```text
979 ÷ (979 + 7)  =  979 ÷ 986  =  0.9929
```

**The thing to be absolutely firm about: the top of all three fractions is easy, and the whole difficulty of this week is the bottom.** Every one of these has `TP` or `TN` on top. What changes is what you divide by:

| Metric | On top | On the bottom | Which region of the table |
|---|---|---|---|
| Precision | TP = 3 | TP + FP = 10 | the **column** you predicted positive |
| Recall | TP = 3 | TP + FN = 14 | the **row** that really was positive |
| Specificity | TN = 979 | TN + FP = 986 | the **row** that really was negative |
| Accuracy | TP + TN = 982 | all four = 1000 | the **whole table** |

**Make the student say the denominator out loud before they divide, every time.** "Three out of the ten I flagged." "Three out of the fourteen that were real." That is where the understanding is; the division is arithmetic.

🍕 **The analogy, and it is the best one in the subject.** You are fishing with a net.

- **Precision:** of everything in your net, what fraction is actually fish? (The rest is boots and seaweed.)
- **Recall:** of all the fish in the lake, what fraction ended up in your net?
- Throw a tiny net at one fish you can see: **precision 100%, recall 1%.**
- Drain the entire lake: **recall 100%, precision terrible.**

**You can always max out one by wrecking the other.** That is why nobody ever reports just one, and it is why next week exists.

### 4. Every line of this week's code, explained to somebody who has never programmed

Four new lines this week. Here they are with nothing assumed.

**New line 1 — making a rare-event table on purpose.**

```python
X, y = make_classification(n_samples=5000, n_features=8, n_informative=4,
                           n_redundant=0, weights=[0.99, 0.01], random_state=0)
```

`make_classification` is a function inside scikit-learn that invents a table for you. It does not download anything; it makes numbers up with a random-number generator. Reading the settings:

- `n_samples=5000` — make 5,000 rows.
- `n_features=8` — eight columns of numbers.
- `n_informative=4` — four of those eight columns genuinely relate to the answer; the other four are decoration.
- `n_redundant=0` — do not add any columns that are copies of other columns.
- `weights=[0.99, 0.01]` — **this is the important one.** Aim for 99% of rows in class 0 and 1% in class 1. It is a target, not a guarantee: we actually get **72 fraud rows out of 5,000, which is 1.44%**.
- `random_state=0` — the seed. **Same seed, same table, every time, on every machine.** Without it your numbers and this file's numbers would disagree and you would not know why.

It hands back two things: `X`, the table of eight columns, and `y`, the answer column of 0s and 1s. Two names on the left of one `=` is how Python receives two things at once.

**Why generated data this week, when we have a delivery table?** Because the delivery table is 28.75% late — nicely balanced — and the accuracy paradox needs a *rare* event to bite. We need 1%, and we can make 1% to order. Say this out loud; a student who has spent six weeks on real-shaped data deserves to know why we switched.

**New line 2 — the four counts, unpacked.**

```python
tn, fp, fn, tp = confusion_matrix(y_val, pred).ravel()
```

`confusion_matrix(y_val, pred)` compares the true answers with the predictions and gives back a 2×2 grid. `.ravel()` flattens that grid into a list of four numbers, reading across the top row then across the bottom: `[TN, FP, FN, TP]`. The four names on the left catch them in order.

**Argument order matters and getting it wrong is silent.** `confusion_matrix(truth, prediction)` — truth first. Swap them and the grid transposes: your false positives and false negatives change places, no error appears, and every number downstream is wrong. It is in the Clinic and it is the nastiest bug of the week.

**New line 3 — the two fractions, done for you.**

```python
print("precision : %.4f" % precision_score(y_val, pred))
print("recall    : %.4f" % recall_score(y_val, pred))
```

Both take the truth and the predictions, both return one number. `precision_score` computes TP ÷ (TP + FP) and `recall_score` computes TP ÷ (TP + FN). **Their whole job is to check the arithmetic you already did on paper** — which is the point of running them at all today.

There is no `specificity_score` in scikit-learn. You compute it yourself: `tn / (tn + fp)`. Mention that; students look for it and worry.

**New line 4 — the whole report in one line.**

```python
print(classification_report(y_val, pred, digits=4))
```

This prints a small table: one row per class, with precision, recall, F1 and **support** for each, and three summary rows underneath. `digits=4` asks for four decimal places instead of the default two, because our numbers are small and two decimals throws them away.

**Today you read exactly two rows of it and ignore the rest.** The `1` row is your fraud class. The `accuracy` row is the number that lied to you. `f1-score` and `macro avg` are **next week** — if a student asks, say "next week, and it needs a new kind of average". Do not improvise it.

### 5. What you will actually see on the screen, with the real numbers

**This is the real output of `fraud.py`. You will see exactly this.**

```text
rows: 5000  columns: 8
fraud rows: 72  fraud rate: 0.0144
train 3000 rows, 44 fraud
val   1000 rows, 14 fraud
test  1000 rows, 14 fraud

--- the model that never says yes ---
accuracy on val : 0.9860
times it said 1 : 0
tn 986  fp 0  fn 14  tp 0

--- a real model ---
tn 979  fp 7  fn 11  tp 3
accuracy    : 0.9820
precision   : 0.3000
recall      : 0.2143
specificity : 0.9929

              precision    recall  f1-score   support

           0     0.9889    0.9929    0.9909       986
           1     0.3000    0.2143    0.2500        14

    accuracy                         0.9820      1000
   macro avg     0.6444    0.6036    0.6204      1000
weighted avg     0.9792    0.9820    0.9805      1000
```

**Five things in there, and the third is the lesson.**

1. **`fraud rate: 0.0144`.** 72 rows out of 5,000. We asked for 1% and got 1.44%. Say the real number; do not round it to "1%".
2. **The lazy model's four counts: `tn 986 fp 0 fn 14 tp 0`.** Two of the four cells are **zero**. It never said fraud, so it never raised a false alarm — and it never caught anything either. **A row of zeros in the right-hand column is the fingerprint of a model that has given up.**
3. **`accuracy 0.9820` for the real model, against `0.9860` for the lazy one.** The good model has the worse accuracy. **This is the moment.**
4. **`precision 0.3000` and `recall 0.2143`.** Both terrible, and *usefully* terrible: they tell you exactly how the model is bad. Seven of the ten cards it blocked belonged to innocent people. Eleven of the fourteen real frauds went through.
5. **`support 986` and `support 14`.** That is just "how many rows of this class were there". It is the smallest number in the report and the reason all the others are unstable — and it is next week's word, so name it in passing and move on.

### 6. The question that is not a maths question

Once you have precision and recall, somebody has to decide which one matters, and **that is not a decision the data can make.**

| Application | A false positive means... | A false negative means... | Which hurts more |
|---|---|---|---|
| Spam filter | your bank's one-time passcode goes to the junk folder | one junk email in your inbox | **the false positive** |
| Cancer screening | an anxious week and one extra scan | an undetected tumour | **the false negative** |
| Fraud detection | a real card declined at a petrol pump, 200 miles from home | money stolen | usually the false negative — but ask the person at the pump |
| Deciding who gets bail | a low-risk person held in a cell | a high-risk person released | **contested, and it is not a maths question at all** |

**Make the student write these as sentences about a person's afternoon, not as abbreviations.** "FP" is a label; *"a nurse's card was declined at the supermarket at 6pm with three children in the trolley"* is a consequence. The homework asks for exactly this and it is the part you mark hardest, because it is the part that decides whether the metric ever gets used well.

### 7. The three misconceptions you will actually meet

**Misconception 1 — "98.6% is a good score."**
It is a *high number*. It is not a good score, because a piece of paper with "no" on it achieves it. The cure is the rule they should carry all year: **always report the majority-class rate next to the accuracy.** 98.6% against a majority rate of 98.6% means your model has added nothing. Week 2 already made them build the `DummyClassifier`; today is the week they find out why.

**Misconception 2 — "precision and recall are basically the same thing."**
They share a numerator, which is exactly why they feel similar, and the denominators are completely different regions of the table. The cure is physical: put the two overlay figures side by side and have the student trace the outlined **column** with one finger and the outlined **row** with the other. The four numbers do not move. Only the outline moves.

**Misconception 3 — "3 ÷ 14 is recall because 14 is bigger."**
Some students pick the denominator by size rather than by meaning. The cure is the spoken sentence: **"three out of the fourteen that really were fraud"** for recall, **"three out of the ten I flagged"** for precision. Say the sentence, then write the fraction. Never the other way round.

### 8. How deep to go, and where to stop

**Go this far:** the accuracy paradox demonstrated with a model they build themselves; the four cells with the naming trick and the addition check; precision, recall and specificity computed by hand and then confirmed by scikit-learn; two rows of `classification_report`; and one sentence each about a real false positive and a real false negative.

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| **F1 score** | **Week 9, next week.** It is printed right there in the report and somebody will ask. The honest answer: *"that's next week, and it's a different kind of average — it needs a whole lesson."* **Do not sketch it.** A half-taught harmonic mean is worse than none. |
| `macro avg`, `weighted avg` | **Week 9.** Same answer. |
| Moving the threshold away from 0.5 | **Week 10.** This is the big temptation, because "just flag more things" is the obvious fix for recall 0.2143. Say: *"you're right, and there's a dial. Week 10."* |
| ROC curves, `roc_curve`, PR curves | **Week 10.** |
| `class_weight="balanced"`, resampling | Not in this level as a lesson. If a student finds it, let them try it and admire it, then hold the line: today the model is fixed and the *measurement* is the subject. |
| AUC | Already theirs since Week 2, and it is *not* today's number. If they ask why we are not using it: *"AUC tells you how well the model ranks. It cannot tell you how many innocent people had their card blocked. Today's four counts can."* |
| Cross-validation and the wobble on these numbers | **Week 11.** And it matters here: 3 out of 14 is a very small count. Be honest that these numbers are shaky and name the week. |
| Cost-weighted decisions ("a miss costs £500") | **Week 11.** |

The line to hold in your head all lesson: **today the student learns that one number cannot tell you what kind of wrong you are.** Four counts can. Everything else is next week.

---

### 9. 🧭 The Growing Map — where Week 8 sits

The student guide carries the same figure every week with one more piece filled in. **This week nothing
moves**, and that is the thing to point out rather than apologise for.

![The Level 3 pipeline in Week 8: still the baseline and four numbers tile, now the four cells of the confusion matrix](../figures/fig-w08-0-where-this-fits.svg)

*Figure 8.0 — Week 8's version. The gold tile is the same one as last week; baseline · four numbers is
labelled wk 7–9, so it is three lessons wide. The ↻ on stage three is drawn grey because the training
loop stays closed until Week 12.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it, don't explain it.** Ask *"which box did we do today?"* They point at the gold tile and
   somebody will notice it is the same box as last week. Good — that is the observation you want.
2. **Then the question that belongs to this week.** Stand beside the 2×2 on the wall and ask: *"same box
   as last week, so what did we actually add to it today?"* The answer you are steering towards is
   *"the same score, broken into four counts"*. Then make it concrete with the second half: *"which
   single cell on that grid is the reason the 98.6% model was rubbish?"* They point at the empty
   **caught** cell. That is the whole lesson, in their own handwriting, on the wall.
3. **Read the label on the tile out loud: wk 7–9.** Measuring honestly is not a one-lesson job, and the
   map says so in print. Next week finishes this box; the week after, the gold drops to the tile
   underneath.

> **🧑‍🏫 Why this is worth two minutes.** A learner who can see the map can distinguish *"I don't
> understand this week"* from *"I don't know where this week goes"* — and those two need completely
> different help from you. It also stops the "are we behind?" anxiety that a week with no new maths and
> no new model can otherwise produce.

**Two things to notice, so you can answer if asked.**

- **Evaluation is lit alone.** Last week had two threads; this week has one, and it is the right one. We
  built a model on purpose to be useless and then never improved it. Nothing about the model, the data
  or the features got better today — only the **looking** did.
- **The ↻ on stage three is still grey.** It is the training loop, closed until Week 12, when the symbol
  turns black. If asked: *"that's the bit that does the learning, and we spend six weeks on it in the
  spring."*

> **⚠️ Watch out:** the map is orientation, not assessment. Never quiz them on it. And do not let a
> student read "same box as last week" as "we wasted a week" — say plainly that the three biggest
> stages in this level are all multi-week boxes.

---

## 🧰 Prep Checklist

This section lists what to cut, print and run before class, so the lesson itself runs without stops.

### 25 minutes the night before

- [ ] **Cut forty index cards or forty slips of paper.** Ten minutes. Do it now; doing it in class costs five minutes of the activity. On each card write two things — `actual` and `predicted` — using the list on workbook page 8.3 (reproduced in the Answer Key). **Twelve cards say `actual: FRAUD`. Twenty-eight say `actual: legit`.**
- [ ] **Write four large pile labels** and put them face down: `CAUGHT (TP)`, `FALSE ALARM (FP)`, `MISS (FN)`, `LEFT ALONE (TN)`.
- [ ] **Type and run `fraud.py` yourself.** The complete file:

```python
"""fraud.py - four numbers, and what accuracy hides."""
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=5000, n_features=8, n_informative=4,
                           n_redundant=0, weights=[0.99, 0.01], random_state=0)
print("rows:", X.shape[0], " columns:", X.shape[1])
print("fraud rows:", int(y.sum()), " fraud rate: %.4f" % y.mean())

X_tmp, X_test, y_tmp, y_test = train_test_split(
    X, y, test_size=0.20, random_state=0, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(
    X_tmp, y_tmp, test_size=0.25, random_state=0, stratify=y_tmp)
print("train %d rows, %d fraud" % (len(X_train), int(y_train.sum())))
print("val   %d rows, %d fraud" % (len(X_val), int(y_val.sum())))
print("test  %d rows, %d fraud" % (len(X_test), int(y_test.sum())))

print()
print("--- the model that never says yes ---")
lazy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
pred_lazy = lazy.predict(X_val)
print("accuracy on val : %.4f" % accuracy_score(y_val, pred_lazy))
print("times it said 1 :", int(pred_lazy.sum()))
tn, fp, fn, tp = confusion_matrix(y_val, pred_lazy).ravel()
print("tn %d  fp %d  fn %d  tp %d" % (tn, fp, fn, tp))

print()
print("--- a real model ---")
tree = DecisionTreeClassifier(random_state=0).fit(X_train, y_train)
pred = tree.predict(X_val)
tn, fp, fn, tp = confusion_matrix(y_val, pred).ravel()
print("tn %d  fp %d  fn %d  tp %d" % (tn, fp, fn, tp))
print("accuracy    : %.4f" % accuracy_score(y_val, pred))
print("precision   : %.4f" % precision_score(y_val, pred))
print("recall      : %.4f" % recall_score(y_val, pred))
print("specificity : %.4f" % (tn / (tn + fp)))

print()
print(classification_report(y_val, pred, digits=4))
```

Run `python3 fraud.py`. You must see **exactly** this:

```text
rows: 5000  columns: 8
fraud rows: 72  fraud rate: 0.0144
train 3000 rows, 44 fraud
val   1000 rows, 14 fraud
test  1000 rows, 14 fraud

--- the model that never says yes ---
accuracy on val : 0.9860
times it said 1 : 0
tn 986  fp 0  fn 14  tp 0

--- a real model ---
tn 979  fp 7  fn 11  tp 3
accuracy    : 0.9820
precision   : 0.3000
recall      : 0.2143
specificity : 0.9929

              precision    recall  f1-score   support

           0     0.9889    0.9929    0.9909       986
           1     0.3000    0.2143    0.2500        14

    accuracy                         0.9820      1000
   macro avg     0.6444    0.6036    0.6204      1000
weighted avg     0.9792    0.9820    0.9805      1000
```

**Expected runtime: under 2 seconds.** If your fraud count is not 72, `random_state=0` is missing somewhere.

- [ ] **Do the three fractions on paper yourself, right now, before you teach them.** 3 ÷ 10, 3 ÷ 14, 979 ÷ 986. Write the sentence beside each: *"three out of the ten I flagged"*, *"three out of the fourteen that were real"*, *"979 out of the 986 that were legitimate"*. **If you have not said those three sentences out loud once, you will fumble them in the room.**
- [ ] **Break it on purpose, twice.**
  1. Swap the arguments: `confusion_matrix(pred, y_val)`. **No error appears.** You get `979 11 7 3` instead of `979 7 11 3` — the FP and FN have quietly changed places. This is deliberate mistake two in the live-code.
  2. Ask `precision_score` about the lazy model: `precision_score(y_val, pred_lazy)`. You get a warning, not an error: `UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 due to no predicted samples.` **Read it: it is scikit-learn telling you the model never said yes.**
- [ ] **Print workbook pages 8.1–8.6.**
- [ ] **Big blank 2×2 on the wall**, next to last week's ablation table. Both stay up until Week 9.

### 5 minutes on the day

- [ ] Editor open, terminal ready. `fraud.py` **deleted or renamed** — they type it.
- [ ] Forty cards shuffled and face down in a stack. **Shuffled matters** — sorted cards make the activity trivial.
- [ ] Four pile labels laid out on the table, face down until minute 47.
- [ ] Blank 2×2 on the wall. Nothing written in it.
- [ ] Workbook 8.1 and 8.2 out. **8.2's prediction filled in pen before any code runs.**
- [ ] Bug Log out.
- [ ] Last week's ablation table still on the wall. You will point at it once.

### Fallback if the laptops fail

**This week's paper version is excellent — arguably better than the screen version** — because the activity is already forty pieces of paper, and the arithmetic is two fractions.

1. **The paradox, on paper.** Tell them: *"1,000 transactions. 14 are fraud. My model says 'not fraud' to all 1,000. What's its accuracy?"* They compute 986 ÷ 1000 = 0.9860. Then: *"how many frauds did it catch?"* Zero. **Objective 3, complete, in three minutes, and it lands harder without a computer** because they did the division themselves.
2. **Sort the forty cards.** The full activity, unchanged. It needs no electricity.
3. **The four fractions from the piles.** Count each pile, write the four counts in the 2×2, check they add to 40, then compute precision, recall and specificity from the piles. **Objectives 1 and 2, complete.**
4. **The naming drill.** Ten spoken scenarios, they name the cell. *"The card was stolen and we let it through."* *"A tourist's card was blocked in Rome."* Thirty seconds each. This is the best five minutes of the paper version.
5. **The sentences.** One false positive and one false negative, written as things that happen to a real person on a real afternoon. **Objective 4, and paper is the right medium for it anyway.**

| If this fails | Do this instead |
|---|---|
| The fraud count is not 72 | `random_state=0` is missing from `make_classification`. Nothing else can cause it. |
| The confusion matrix prints only one number and `.ravel()` errors | Only one class appears in either list. With 14 frauds in 1,000 rows this happens on small hand-made examples. Message and fix are in the Clinic. |
| `UndefinedMetricWarning` frightens somebody | It is a **warning**, not an error, and it is *informative*: the model never predicted the positive class, so there is nothing to divide by. Read it out loud and move on. |
| `classification_report` prints two decimals and the numbers look identical | `digits=4`. Same reason as last week's four decimal places. |
| A student wants to fix recall by flagging more | Excellent instinct, wrong week. *"There is a dial and you are right about which way to turn it. Week 10."* |
| The cards get sorted into two piles instead of four | They sorted by *actual* only, or by *predicted* only. Ask: *"which pile holds the frauds you missed?"* The absence of an answer is the correction. |

---

## ⏱️ The Lesson, Minute by Minute

This section is the plan for the whole lesson, one segment at a time, with what to say, ask, expect and watch for.

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — The 98.6% Model | 7 | 7 | Build the useless model. Admire it. Then the question. |
| 🧠 Concept — Four Cells, Two Fractions | 18 | 25 | The naming trick; the 2×2 on the wall; three fractions by hand |
| 💻 Live-Code Together — `fraud.py` | 18 | 43 | The paradox in code, then the four counts. **Two deliberate mistakes.** |
| 🎲 Their Turn — 99% Accurate and Completely Useless | 20 | 63 | Forty cards into four piles; both fractions from the piles |
| 🔑 Wrap & Assign | 7 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — The 98.6% Model (7 minutes)

**Do this:** Nothing on the screen. Point at last week's ablation table, still on the wall.

**Say this:**

> "All term you've reported one number for this model: AUC. Best honest score, 0.7599 on the 400 validation rows. Good work, and it's on the wall.
>
> Today I'm going to hand you a different model, on different data, and it scores **98.6%**. Not 0.76. Ninety-eight point six per cent.
>
> Here's the data: five thousand card transactions. Seventy-two of them are fraud. That's one in seventy."

**Do this:** Write on the board:

```text
5000 transactions,  72 fraud
```

> "And here's the model, complete. This is the whole thing."

**Do this:** Write, in large letters, on a piece of paper, and hold it up:

```text
    NOT FRAUD
```

**Say this:**

> "That's it. It's a piece of paper. It says 'not fraud' to everything. It doesn't look at the transaction. It doesn't know what a transaction *is*.
>
> Work out its accuracy. There are 1,000 transactions in the validation pile and 14 of them are fraud."

**Do this:** Wait. Let them do the division. **Do not do it for them.**

*Expected:* 986 ÷ 1000 = 0.986.

> "98.6%. My piece of paper is 98.6% accurate.
>
> Last week you worked for half an hour to move a score by 0.0058. This piece of paper took me four seconds."

**Ask this:** "How many frauds did it catch?"

*Hoped-for answer:* "None."

Let the silence sit. Do not fill it.

> "None. Zero out of fourteen. Fourteen people had money taken and my 98.6%-accurate model noticed nothing.
>
> And here's the part that should genuinely annoy you. In twenty minutes you're going to build a real model on this data — a proper decision tree, the kind you built in Level 2. It will score **98.20%**. Lower. Worse accuracy than the piece of paper.
>
> And it catches three of the fourteen."

**Do this:** Write both on the board:

```text
piece of paper   accuracy 0.9860    caught 0 of 14
real model       accuracy 0.9820    caught 3 of 14
```

**Ask this:** "Which of those two would you rather have running on your card?"

*Hoped-for answer:* the second.

*If they say "the first, it's more accurate":* thank them, seriously, because they have just said the thing the whole lesson exists to fix. Then ask: *"how many of the fourteen do you want it to catch?"*

> "So **accuracy went down, and the model got better.** That means accuracy is not measuring the thing we care about — and if a number isn't measuring the thing you care about, it doesn't matter how big it is.
>
> This has a name. It's called the **accuracy paradox**, and it turns up any time the thing you're looking for is rare. Which is almost always, because interesting things are rare."

**Do this:** Write on the board and leave it up all lesson:

> **accuracy paradox** — when one class is rare, a model that never predicts it can score very high accuracy. Always report the majority-class rate next to the accuracy.

---

### 🧠 Concept — Four Cells, Two Fractions (18 minutes)

**Say this:**

> "The problem with accuracy is that it adds two completely different kinds of correct together, and two completely different kinds of wrong. Then it hands you one number, and the one number can't be taken apart again.
>
> So let's not add them up. Let's keep all four."

**Do this:** Go to the wall and draw the 2×2, big, saying each part out loud as you draw it. **Rows first, then columns, and say which is which twice.**

```text
                       PREDICTED
                 legit          fraud
ACTUAL  legit  │          │           │
        fraud  │          │           │
               └──────────┴───────────┘
```

> "**Rows are what actually happened. Columns are what the model said.** Say it back to me."

Make them say it. It is the single most-confused thing in the week.

**Say this:**

> "Now the four names, and there's a trick to reading them that nobody guesses, so I'll just tell you.
>
> **The second word is what YOU predicted. The first word is whether you were RIGHT.**
>
> A **false positive**: you predicted positive — you said fraud — and that was false. You cried wolf. **A false alarm.**
>
> A **false negative**: you predicted negative — you said it was fine — and that was false. The wolf walked past. **A miss.**"

**Do this:** Write the four names into the cells, with the plain-English version underneath each.

| | predicted legit | predicted fraud |
|---|---|---|
| **actual legit** | **True Negative** — correctly left alone | **False Positive** — a false alarm |
| **actual fraud** | **False Negative** — a miss | **True Positive** — caught one |

**Ask this — three in a row, fast:**

1. "The card was stolen and the model let it through. Which cell?" *(False negative.)*
2. "A tourist's perfectly good card gets blocked in Rome. Which cell?" *(False positive.)*
3. "An ordinary shopping trip, nothing flagged. Which cell?" *(True negative.)*

*If they get one wrong:* do not give the answer. Say *"what did the model predict?"* then *"was it right?"* The two words assemble themselves.

**Do this:** Now fill in the real numbers, which you already have from your prep.

| | predicted legit | predicted fraud |
|---|---|---|
| **actual legit** | 979 | 7 |
| **actual fraud** | 11 | 3 |

**Ask this:** "Add all four up. What should you get?"

*Hoped-for answer:* 1000, the number of validation rows.

> "979 plus 7 plus 11 plus 3 is 1000. **Do that addition every single time you draw one of these.** It takes five seconds and it catches every counting mistake you will ever make."

**Say this:**

> "Now the two fractions, and here is the only hard thing in this lesson: **they both have the same number on top.** Three. The three frauds you caught. What changes is what you divide by — and the whole skill is choosing the bottom."

**Do this:** On the board, draw a box round the **predicted-fraud column** on the wall table with a coloured pen.

> "Question one: **of everything I flagged, how much was really fraud?** I flagged this column. How many is that?"

*7 + 3 = 10.*

> "Ten. And how many of the ten were really fraud?"

*Three.*

> "**Three out of the ten I flagged.** Say that sentence, then write the fraction."

```text
precision  =  3 ÷ 10  =  0.3000
```

**Do this:** Rub out the column box. Draw a box round the **actual-fraud row** instead.

> "Question two, completely different: **of everything that really was fraud, how much did I catch?** This row. How many?"

*11 + 3 = 14.*

> "Fourteen. And I caught?"

*Three.*

> "**Three out of the fourteen that really were fraud.**"

```text
recall  =  3 ÷ 14  =  0.2143
```

**Say this, pointing at the table:**

> "Look at what just happened. **The four numbers did not move.** 979, 7, 11, 3. I drew a box round a column and got 0.30. I drew a box round a row and got 0.21. **Precision and recall are not two measurements. They are the same measurement read twice, once down and once across.**"

**Do this:** One more, to close the set. Box the actual-legit row.

> "And one more, because you'll need it: **of everything that really was legitimate, how much did I correctly leave alone?**"

```text
specificity  =  979 ÷ 986  =  0.9929
```

> "0.9929. Which is the only respectable-looking number on the board, and it's respectable because there were 986 easy rows and it got nearly all of them. **That's what accuracy was mostly measuring all along.**"

**Do this:** Hand out workbook page 8.1 — ten scenarios, name the cell — and give them five minutes. Then page 8.2: predict the lazy model's four counts, **in pen**, before any code runs.

> "Pen. Four numbers. Two of them are zero and I want to see whether you can tell me which two."

---

### 💻 Live-Code Together — `fraud.py` (18 minutes)

**You never touch their keyboard.**

**Step 1 (4 min) — make the table and look at it.**

```python
"""fraud.py - four numbers, and what accuracy hides."""
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=5000, n_features=8, n_informative=4,
                           n_redundant=0, weights=[0.99, 0.01], random_state=0)
print("rows:", X.shape[0], " columns:", X.shape[1])
print("fraud rows:", int(y.sum()), " fraud rate: %.4f" % y.mean())
```

**Ask before running:** "We asked for 1% fraud out of 5,000 rows. How many fraud rows will there be?"

*Most will say 50.* Run it:

```text
rows: 5000  columns: 8
fraud rows: 72  fraud rate: 0.0144
```

> **Say this:** "Seventy-two, not fifty. `weights=[0.99, 0.01]` is a **target**, not a promise — the generator aims at 1% and lands at 1.44%. Which is a good habit in itself: **you asked for something, and then you checked what you got.** Never assume the data is what you ordered.
>
> And `random_state=0` — same as every week. Same seed, same 5,000 rows, same 72 frauds, on your laptop and mine. Without it we could not have this conversation."

**Step 2 (3 min) — three piles, and count the frauds in each.**

```python
X_tmp, X_test, y_tmp, y_test = train_test_split(
    X, y, test_size=0.20, random_state=0, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(
    X_tmp, y_tmp, test_size=0.25, random_state=0, stratify=y_tmp)
print("train %d rows, %d fraud" % (len(X_train), int(y_train.sum())))
print("val   %d rows, %d fraud" % (len(X_val), int(y_val.sum())))
print("test  %d rows, %d fraud" % (len(X_test), int(y_test.sum())))
```

```text
train 3000 rows, 44 fraud
val   1000 rows, 14 fraud
test  1000 rows, 14 fraud
```

> **Say this:** "Week 2's three piles, unchanged. And look what `stratify=y` bought us: 44 plus 14 plus 14 is 72. **Every fraud is accounted for, and each pile got its fair share.** Without `stratify` the validation pile could easily have had 8 frauds or 22 by luck, and every number we compute today would move.
>
> Fourteen. That is how many frauds we get to be judged on. **Fourteen is a very small number and you should be uneasy about it.** Every fraction today has a 14 or a 10 on the bottom, and small denominators wobble. We will fix that in Week 11; today, just notice it."

**Step 3 (5 min) — the piece of paper, in code.**

```python
print()
print("--- the model that never says yes ---")
lazy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
pred_lazy = lazy.predict(X_val)
print("accuracy on val : %.4f" % accuracy_score(y_val, pred_lazy))
print("times it said 1 :", int(pred_lazy.sum()))
tn, fp, fn, tp = confusion_matrix(y_val, pred_lazy).ravel()
print("tn %d  fp %d  fn %d  tp %d" % (tn, fp, fn, tp))
```

**Ask before running:** "Page 8.2. Read me your four predicted counts."

Run it:

```text
--- the model that never says yes ---
accuracy on val : 0.9860
times it said 1 : 0
tn 986  fp 0  fn 14  tp 0
```

> **Say this:** "0.9860, exactly as you calculated on paper twenty minutes ago. And `times it said 1: 0` — it never once predicted fraud, in a thousand tries.
>
> Look at the four counts. `fp 0` and `tp 0`. **The entire right-hand column of the table is zero.** That is the fingerprint of a model that has given up: it never says yes, so it never raises a false alarm — and it never catches anything either.
>
> `DummyClassifier(strategy='most_frequent')` is from Week 2, and now you know what it was for. It is not a joke model. **It is the number you have to beat, and today it is beating you.**"

**Step 4 (3 min) — 🐞 DELIBERATE MISTAKE ONE: ask for precision.**

> **Say this:** "Let's get its precision."

Type this and run it:

```python
print("precision       : %.4f" % precision_score(y_val, pred_lazy))
```

Real output:

```text
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/sklearn/metrics/_classification.py:1731: UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 due to no predicted samples. Use `zero_division` parameter to control this behavior.
  _warn_prf(average, modifier, f"{metric.capitalize()} is", result.shape[0])
precision       : 0.0000
```

**Do this:** Point at the word `UndefinedMetricWarning`.

**Ask this:** "Is that an error or a warning? And what is it telling us?"

*Hoped-for answer:* a warning — the code kept going — and it says there were no predicted samples.

> **Say this:** "A warning, not an error. The program did not stop; it printed 0.0000 and carried on.
>
> Now read what it actually says: **'no predicted samples'.** Precision is 'of everything I flagged, how much was fraud' — and it flagged **nothing**. Zero divided by zero is not a number. So scikit-learn shrugged, printed 0.0000, and told you why in a sentence.
>
> **This is one of the friendliest messages you will get all year.** It is not saying you did something wrong. It is describing your model."

**Do this:** Bug Log entry, ninety seconds. Message: `UndefinedMetricWarning ... no predicted samples`. Meaning: *"the model never predicted the positive class, so precision has nothing on the bottom"*. Fix: *"nothing to fix — the model is the problem, not the code"*.

**Step 5 (3 min) — the real model, and 🐞 DELIBERATE MISTAKE TWO.**

```python
print()
print("--- a real model ---")
tree = DecisionTreeClassifier(random_state=0).fit(X_train, y_train)
pred = tree.predict(X_val)
tn, fp, fn, tp = confusion_matrix(pred, y_val).ravel()     # <-- the mistake
print("tn %d  fp %d  fn %d  tp %d" % (tn, fp, fn, tp))
```

Run it. Real output:

```text
--- a real model ---
tn 979  fp 11  fn 7  tp 3
```

**Do this:** Say nothing. Point at the wall table, where 7 and 11 are the other way round.

**Ask this:** "That doesn't match the wall. Which two numbers moved, and did the program complain?"

*Hoped-for answer:* the 7 and the 11 have swapped, and no, nothing complained.

> **Say this:** "The false positives and the false negatives have changed places. **And nothing went red.** No error, no warning, no hint.
>
> Look at the call: `confusion_matrix(pred, y_val)`. **Truth goes first.** I put the predictions first, so scikit-learn thought my predictions were the truth and the truth was my prediction — and it obligingly turned the whole table on its side.
>
> Why does this matter more than any typo you have made this term? Because the two numbers that swapped are **the two errors**. If you get them the wrong way round, you will tell somebody 'we blocked 11 innocent cards and missed 7 frauds' when the truth is 'we blocked 7 innocent cards and missed 11 frauds'. Those are different afternoons for different people, and both sentences sound equally confident."

Fix it live:

```python
tn, fp, fn, tp = confusion_matrix(y_val, pred).ravel()
```

```text
tn 979  fp 7  fn 11  tp 3
```

**Do this:** Bug Log. **This is the most valuable entry of the term so far** — a wrong answer with no error message. Ninety seconds, and make sure the words *"truth first"* are in it.

**Step 6 (final, and it is the payoff) — check the paper arithmetic.**

```python
print("accuracy    : %.4f" % accuracy_score(y_val, pred))
print("precision   : %.4f" % precision_score(y_val, pred))
print("recall      : %.4f" % recall_score(y_val, pred))
print("specificity : %.4f" % (tn / (tn + fp)))
print()
print(classification_report(y_val, pred, digits=4))
```

**Ask before running:** "You computed three of those four on paper. Read them out."

*0.3000, 0.2143, 0.9929.*

Run it:

```text
accuracy    : 0.9820
precision   : 0.3000
recall      : 0.2143
specificity : 0.9929

              precision    recall  f1-score   support

           0     0.9889    0.9929    0.9909       986
           1     0.3000    0.2143    0.2500        14

    accuracy                         0.9820      1000
   macro avg     0.6444    0.6036    0.6204      1000
weighted avg     0.9792    0.9820    0.9805      1000
```

> **Say this:** "All three match your paper, to four decimal places. **That is the point of running it.** The computer is not the authority here — you did the maths and the computer agreed with you.
>
> Now `classification_report`. There is a lot in there and today you read exactly two rows.
>
> **Row `1`.** That is fraud. `0.3000`, `0.2143` — your two numbers, and `support 14`, which is just how many real frauds there were.
>
> **The `accuracy` row.** `0.9820`. That is the number that would have made you feel fine about a model that misses eleven frauds out of fourteen.
>
> `f1-score`, `macro avg`, `weighted avg` — **next week.** Do not read them today; they need a new kind of average and it takes a whole lesson."

**Ask this:** "Accuracy 0.9820 for this model, 0.9860 for the piece of paper. So which is better, and how do you know?"

*Hoped-for answer:* this one — it caught 3 of 14, the paper caught 0.

> "Right. And notice you did not use accuracy to answer that. You used the four counts. **Accuracy could not tell you, and the four counts could.** That is the whole lesson."

---

### 🎲 Their Turn — 99% Accurate and Completely Useless (20 minutes)

Full instructions in **🎲 The Activity, In Full** below. In outline: forty cards, four piles, count them, fill in a 2×2, check it adds to 40, compute precision and recall from the piles, and describe one false positive and one false negative as things that happen to a person.

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Stand at the wall 2×2. Read all four numbers out loud, then all three fractions.

**Say this:**

> "Four counts. 979, 7, 11, 3. They add to 1000, and you checked.
>
> Three fractions, all with a 3 on top and three different numbers underneath. Precision 0.3000 — three out of the ten I flagged. Recall 0.2143 — three out of the fourteen that were real. Specificity 0.9929 — 979 out of the 986 that were fine.
>
> And one number I do not want you to report on its own again this year: **accuracy 0.9820**, from a model that missed eleven frauds out of fourteen."

**Do this:** Three quick checks — exact wording in **✅ Assessing Understanding**.

**Say this, to close:**

> "One last thing, and it's next week's door.
>
> Recall 0.2143 is bad. So somebody will say: fine, flag more transactions. And they are right — you can push recall up whenever you like.
>
> But look at the table. Most of the extra things you flag come out of the huge legit column. **Push recall up and precision falls.** They are on opposite ends of a see-saw, and next week we work out what to do when you need one number that respects both."

**Do this:** Hand out the homework and read the third part out loud, slowly.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 due to no predicted samples. Use 'zero_division' parameter to control this behavior.` | "You asked 'of what I flagged, how much was right' and you flagged nothing." | The model never predicts the positive class — usually the `DummyClassifier`, or a real model on very imbalanced data. | **Nothing to fix in the code.** It is a fact about the model. If you want to silence it: `precision_score(y, pred, zero_division=0)`. **Read the message first** — it is telling you the model has given up. |
| `ValueError: not enough values to unpack (expected 4, got 1)` | "I asked for four numbers and got one." | `confusion_matrix(y, pred).ravel()` where **only one class appears** in both lists — every value is 0, so the matrix is 1×1. | Check that both lists contain some 0s **and** some 1s. On a hand-made example, make sure you included at least one fraud and one flag. |
| `ValueError: Classification metrics can't handle a mix of binary and continuous targets` | "One of those is 0s and 1s and the other is decimals." | `precision_score(y, prob)` — probabilities passed where predictions were wanted. | These metrics want hard 0/1 predictions: `pred = model.predict(X)`. Turning probabilities into predictions with a threshold is **Week 10**. |
| `ValueError: Number of informative, redundant and repeated features must sum to less than the number of total features` | "You asked for more useful columns than columns." | `n_features=3` with `n_informative=4`. | `n_informative` must be smaller than `n_features`. Ours is 4 out of 8. |
| `TypeError: only length-1 arrays can be converted to Python scalars` | "You tried to print a list as if it were one number." | `"%.4f" % precision_score(y, pred, average=None)` — `average=None` returns **one number per class**. | Drop `average=None` for the single positive-class number, or print the array with `print(...)` and no `%` formatting. |
| **No error. The FP and FN counts are swapped.** | Nothing crashed. Every downstream number about your two errors is wrong. | `confusion_matrix(pred, y_val)` — arguments the wrong way round. | `confusion_matrix(y_val, pred)`. **Truth first, always.** Sanity check: FN should be the count of frauds you missed, which on our data is 11, not 7. |
| **No error. Accuracy is 0.99 and you are pleased.** | Nothing crashed. The number is meaningless on its own. | The positive class is rare, so answering "no" to everything scores well. | Always print the majority-class rate beside it: `print(1 - y_val.mean())`. If your accuracy is not comfortably above that, your model has added nothing. |
| **No error. Precision is 1.0000 and recall is tiny.** | Nothing crashed. | The model flags almost nothing, and happens to be right about the two or three it does flag. | Look at `tp + fp`. If it is 2, your precision of 1.0 is "I was right about both of the two guesses I made". **Report the counts next to every ratio.** |
| **No error. `classification_report` shows everything to two decimals and rows look identical.** | Nothing is wrong. | Default is `digits=2`. | `classification_report(y, pred, digits=4)`. |
| **No error, but the fraud count is 50, not 72.** | Nothing crashed; you have a different table from everybody else. | `random_state` missing or not `0`. | `random_state=0`. **Every generated table in this course carries a seed, and a printed number from an unseeded run is not a result.** |

### How to teach debugging without giving the answer

All the old moves stand. This week adds two, and both are about the errors that do not announce themselves.

15. **"Do the four numbers add up to how many rows you have?"** Ask it before anything else, every time a 2×2 appears. It is five seconds and it catches every counting mistake.

16. **"Which number is on the bottom, and say it as a sentence."** For any ratio that looks wrong. *"Three out of the ten I flagged"* versus *"three out of the fourteen that were real"* — a student who can say the sentence has the fraction right, and one who cannot does not, whatever they wrote down.

And the sentence for this week:

> **"A ratio with no counts next to it is a rumour. Precision 1.0 out of two guesses is not the same as precision 1.0 out of two hundred."**

---

## 🎲 The Activity, In Full

This section gives the card activity in full, so you can run it without improvising.

### 99% Accurate and Completely Useless

**What it is.** Two halves. First, build the useless model and admire its score — which they already did in the hook, and now do in code. Then the physical half: forty index cards, four labelled piles, and both fractions computed from the piles by counting.

### Setup

- **Forty cards**, shuffled, face down in a stack. Each card carries two lines: `actual:` and `predicted:`. The full list is in the Answer Key under page 8.3.
- **Four pile labels** laid out with clear space between them: `CAUGHT (TP)` · `FALSE ALARM (FP)` · `MISS (FN)` · `LEFT ALONE (TN)`.
- Workbook page 8.3, which is a blank 2×2 with room for the arithmetic underneath.
- A pen.

### Part 1 — sort the cards (7 minutes)

Read the instruction once and then say nothing at all:

> **"Turn over one card at a time. Read both lines. Put it on the pile it belongs to. Every card belongs to exactly one pile — if you think a card belongs to two piles, read it again."**

**Sit on your hands.** This is the part where the four names stop being vocabulary.

**Watch for exactly one failure mode:** sorting into two piles instead of four, because they read only the `actual` line (or only the `predicted` line). If you see two piles, ask one question: *"which pile holds the frauds you missed?"* The absence of an answer does the teaching.

### Part 2 — count, and fill in the 2×2 (4 minutes)

> **"Count each pile. Write the four numbers into the 2×2 on page 8.3. Then add all four up."**

The four counts are:

| | predicted legit | predicted fraud |
|---|---|---|
| **actual legit** | **22** (left alone) | **6** (false alarm) |
| **actual fraud** | **3** (miss) | **9** (caught) |

**9 + 6 + 3 + 22 = 40.** ✅ If it does not come to 40, a card is on the floor or on the wrong pile. **Find it before going on** — this is the check working, and letting a wrong 2×2 through here poisons everything after it.

### Part 3 — both fractions, from the piles (6 minutes)

Do not let them use the numbers in the table until they have said the sentence.

> **"Precision. Put your hand on the two piles you FLAGGED — caught and false alarm. How many cards is that?"**

*9 + 6 = 15.*

> **"And how many of those fifteen were really fraud?"**

*9.*

```text
precision  =  9 ÷ 15  =  0.6000
```

> **"Recall. Now put your hands on the two piles that really WERE fraud — caught and miss. How many?"**

*9 + 3 = 12.*

> **"And you caught?"**

*9.*

```text
recall  =  9 ÷ 12  =  0.7500
```

Then, for completeness:

```text
specificity  =  22 ÷ 28  =  0.7857
accuracy     =  (9 + 22) ÷ 40  =  31 ÷ 40  =  0.7750
```

**The moment to point out:** they moved their hands twice, over the **same forty cards**, and got 0.6000 and 0.7500. **Nothing about the model changed between those two numbers.**

### Part 4 — one sentence each (3 minutes)

> **"Pick up one card from the FALSE ALARM pile. Write me one sentence about what happened to that person this afternoon. Not 'FP'. A sentence."**
>
> **"Now one from the MISS pile. Same thing."**

Good answers look like: *"Her card was declined at the supermarket checkout with a full trolley and two children, and she had to leave the shopping."* and *"£240 was taken from his account and nobody noticed for three weeks."*

**This is objective 4 and it is the part that makes the metric mean something.** Do not let them write "a legitimate transaction was incorrectly classified".

### What "finished" looks like

- Four piles on the table with 9, 6, 3 and 22 cards in them.
- A completed 2×2 with the addition check written out: **9 + 6 + 3 + 22 = 40**.
- Precision and recall both computed **as fractions with the denominators written out**, not just as decimals.
- Two sentences about two real people.
- The student can say, unprompted: *"same forty cards, two different numbers."*

### Variation — easier

**Twenty cards instead of forty**, keeping the same shape: TP 5, FP 3, FN 2, TN 10. Precision 5 ÷ 8 = 0.6250, recall 5 ÷ 7 = 0.7143, and they add to 20.

**And pre-label the piles with the plain English only** — `CAUGHT`, `FALSE ALARM`, `MISS`, `LEFT ALONE` — with the TP/FP/FN/TN abbreviations added *after* the sorting is done. The abbreviations are the hard part and they are not the objective.

### Variation — harder

1. **Two models on the same forty cards.** Give a second `predicted` line on each card from a "cautious" model that flags only 6 cards and gets 5 of them right. Precision 5 ÷ 6 = 0.8333, recall 5 ÷ 12 = 0.4167. Then the question: **which model is better?** There is no answer without knowing what the two errors cost, and that is the honest and unsettling point.
2. **Build the piece of paper's 2×2 from the same cards.** Put every card on `LEFT ALONE` and `MISS`: TN 28, FN 12, and both other piles empty. Accuracy 28 ÷ 40 = 0.7000, recall 0 ÷ 12 = 0. **On balanced-ish data the useless model looks obviously useless.** So why did it look brilliant on the fraud data? Because 14 out of 1,000 is not 12 out of 40. **The paradox needs rarity**, and this shows exactly where it comes from.
3. **Work backwards.** *"I want precision 0.5 and recall 0.5 with 12 real frauds. What are the four counts?"* TP 6, FN 6, FP 6, and TN whatever is left — 22 if you keep 40 cards. Genuinely hard and genuinely satisfying.
4. **Find the pair of models where accuracy and recall disagree about the winner.** They already have one — the piece of paper versus the tree. Ask them to write the two-sentence argument for each, then say which sentence they would want read out in court.
5. **Which cell is missing from a smoke alarm?** A smoke alarm that never goes off has TP 0 and FP 0. Ask what number you would need to know to decide whether that is fine. (How many fires there were: the FN count.) This is a very good five-minute conversation.

---

## ❓ Questions Students Ask This Week

This section collects the questions students ask this week, with an answer for each.

**"If accuracy is that bad, why does anybody use it?"**

Because when the two classes are roughly balanced, accuracy is genuinely fine and easy to explain. On last week's delivery table 28.75% of orders were late — a model that says "on time" to everything scores 71.25%, and any real model comfortably beats that. Accuracy there is a reasonable summary.

**The rule is not "never use accuracy". The rule is "never report accuracy without the majority-class rate beside it."** On the delivery table: "74.25% accurate, against a majority rate of 71.25%". On the fraud table: "98.20% accurate, against a majority rate of 98.60%" — and now the number tells the truth, which is that you are *below* the piece of paper.

**"Why is the fraud rate 1.44% when we asked for 1%?"**

`weights=[0.99, 0.01]` on its own would give exactly 50 fraud rows. But `make_classification` has a setting we did not touch, `flip_y=0.01`, which takes 1% of all rows (about 50 of the 5,000) and gives each a random new label. Roughly half of those land on "fraud", which is where the extra 22 come from (with `flip_y=0` the count is exactly 50). It means about a third of our 72 "frauds" are rows that look like ordinary transactions with a random label, which no model can learn, so part of the tree's poor score is label noise rather than only overfitting.

**The habit that matters more than the explanation:** you asked for something and then you *checked what you got.* `print("fraud rate: %.4f" % y.mean())` is one line and it stopped you from writing "1%" in your report when the truth is 1.44%. Data very often is not what you ordered.

**"Can't we just make it flag more things? Recall 0.2143 is awful."**

Yes, and you are right about which way to turn the dial. **That is Week 10 and it is one of the best weeks of the year.**

Here is what to hold on to until then: look at the table. Everything extra you flag has to come from somewhere: some of it from the fraud row (that is the recall you wanted) but, with 986 legitimate rows against 14 frauds, most of it from the legit column — which means **more false alarms.** Precision will usually fall. On a fixed model you generally cannot buy recall without spending precision; only a better model gives you both, and next week you will draw the whole curve of that trade and pick a point on it on purpose.

**"Which is worse, a false positive or a false negative?"**

**It depends entirely on the application, and it is not a question data can answer.**

For a spam filter, the false positive is worse: one junk email in your inbox is annoying, but your bank's one-time passcode in the junk folder means you cannot log in. For cancer screening, the false negative is worse, and not close: an extra scan is an anxious week, a missed tumour is a life.

For fraud, most banks say the false negative is worse because money is gone — but ask the nurse whose card was declined at a petrol pump 200 miles from home at 11pm. **The person deciding which error matters is very rarely the person the error happens to.** That is a real problem and there is no formula for it.

**"Why is specificity so high when everything else is terrible?"**

Because it is being asked the easy question. Specificity is 979 out of the 986 legitimate transactions — and 986 out of 1,000 rows are legitimate, so this is a test the model passes by mostly doing nothing.

**That is exactly what accuracy was measuring all along.** Accuracy 0.9820 is 98.6% specificity's easy work with 1.4% of hard work bolted on. Any metric whose denominator is dominated by the common class will look excellent on imbalanced data, and it is not lying — it just is not measuring the thing you care about.

**"Why did the decision tree do so badly? It got 3 out of 14."**

Two honest reasons, and one of them is a warning.

**One: there were only 44 frauds to learn from.** Forty-four examples of a thing, spread across eight columns of numbers, is not much. Everything a model knows, it knows from examples, and it had forty-four.

**Two, and this is the warning: we did not stop the tree from growing.** `DecisionTreeClassifier(random_state=0)` with no depth limit grows until every leaf is pure, which means it memorises its 3,000 training rows — including the 44 frauds, individually. On the training rows it will look perfect. On the validation rows it gets 3 out of 14. **That is overfitting**, which they met in Level 2, and it is worth naming out loud even though we are not fixing it today.

**"Is there a fifth cell? What if the model says 'not sure'?"**

Good question, and the answer is a genuinely interesting "sort of".

**With the model as we have written it, no — there are exactly four cells**, because `predict` always returns 0 or 1. There is no "don't know".

But underneath, the model does not really produce 0 or 1. It produces a **number between 0 and 1**, and something turns that into a yes or no by comparing it to 0.5. That is Week 10. And once you can see the number, you *can* build a three-way system — flag it, clear it, or send it to a human — which is exactly how real fraud systems work. The 2×2 becomes a 2×3, and the middle column is somebody's job.

**"So which single number should we report?"** *(Nobody fully agrees, and here is why.)*

**There isn't one, and the argument about it is live and unresolved.** Be straight about this.

**What everybody agrees on:** report the four counts. Always. They are the raw evidence and every ratio in this subject is derived from them. A report with the four counts in it can be re-analysed by somebody who disagrees with your choice of metric; a report with only a ratio cannot.

**Where it splits.** One camp says **F1** — one number that respects both precision and recall, which is next week's lesson, and which is the default in most research papers. The second camp says **that is a fudge**: F1 weights the two errors equally, and they are almost never equal, so you should write down what each error *costs* and compute expected cost in pounds — which is Week 11. The third camp says **report the curve, not a point**: any single threshold is a choice, so publish the whole trade-off and let the reader pick — Week 10.

**And there is a fourth position which is harder and probably the most honest:** all three are answers to the wrong question, because the four counts are not four kinds of number. Eleven missed frauds are eleven people; seven false alarms are seven ruined afternoons. **Adding them into one score requires deciding how many ruined afternoons equal one theft, and no metric will make that decision for you.** It gets made anyway — by whoever picks the metric, usually without noticing.

What to tell a 14-year-old, out loud: **"there's no single right number. But there are always four counts, and if you report those, nobody can hide anything from you."**

---

## ⚠️ Where This Lesson Goes Wrong

This section is for the moments when the lesson stalls: what happens, why, and what to do right then.

| What happens | Why | What to do right now |
|---|---|---|
| **The confusion matrix gets taught before the paradox lands** | It feels like the logical order: define the terms, then use them | **Do it the other way round.** Build the 98.6% model first, admire it, then ask how many frauds it caught. The four cells have to arrive as *the answer to a problem they can feel*, or they are bookkeeping. |
| Rows and columns get swapped on the board | The table genuinely is confusing, and half of the internet draws it the other way | Say "**rows are what happened, columns are what the model said**" and make them say it back. Then write ACTUAL and PREDICTED **on the board in capitals** and leave them there all lesson. |
| The wrong denominator, repeatedly | Students pick the bottom of the fraction by size, not by meaning | Force the spoken sentence before the fraction, every time: *"three out of the ten I flagged"*, *"three out of the fourteen that were real"*. **Sentence first, arithmetic second.** |
| `.ravel()` order is memorised wrong | `[TN, FP, FN, TP]` is not an obvious order | Do not ask them to memorise it. Ask them to **check** it: FN is "frauds I missed", which must be 11 on our data. If their `fn` is 7, they have it backwards. |
| The swapped-arguments bug goes unnoticed | It produces no error and a plausible table | This is deliberate mistake two and it is on the schedule. **Do not skip it because time is short** — it is the most valuable ninety seconds in the week. |
| F1 gets taught because it is printed on the screen | It is right there in `classification_report` and somebody asks | *"Next week. It's a different kind of average and it needs a whole lesson."* Then cover it with your hand. **A half-explained harmonic mean makes Week 9 harder, not easier.** |
| The 40 cards get sorted into two piles | They read only one of the two lines on the card | One question: *"which pile holds the frauds you missed?"* Do not explain; wait. |
| The pile counts do not add to 40 and it gets ignored | Off by one feels harmless | **Stop everything and find the card.** The addition check is a habit you are installing this week and letting it fail once undoes it. |
| Somebody says "accuracy 98% is basically perfect" and it goes unchallenged | It is a very natural thing to say | Immediately: *"the piece of paper got 98.6%. Is the piece of paper basically perfect?"* Every time, all lesson. |
| "FP" and "FN" stay as abbreviations | Abbreviations are faster to write | The homework demands sentences about a person's afternoon, and you mark that part hardest. Model it yourself at least twice in the lesson — say *"a nurse's card declined at a petrol pump"*, not *"a false positive"*. |
| The 14 frauds are treated as a solid measurement | 0.2143 looks precise, all four decimals of it | Say it out loud once: **"every fraction today has a 14 or a 10 on the bottom, and small denominators wobble."** Catch one more fraud and recall goes from 0.2143 to 0.2857. Name Week 11 and move on. |

---

## 🧭 Differentiation

This section adjusts the lesson for a student who is struggling and for one who is racing ahead.

### If the student is struggling

**Cut:** specificity. Precision and recall are the objectives; specificity is the third fraction and it is the least used of the three. Nothing downstream needs it.

**Cut:** `classification_report` entirely. The four counts and two fractions are the lesson. The report is a convenience that prints things they have not met yet.

**Cut:** the 40 cards to 20, with the counts in Variation-easier: TP 5, FP 3, FN 2, TN 10.

**Give them `fraud.py` complete.** Every bit of the learning today is in the sorting and the two fractions, and none of it is in typing an import block.

**The version of the arithmetic that skips everything hard.** No algebra exists this week, so the scaffold is one table with the sentences pre-written and only the division left to do:

| Say this sentence | The fraction | Work it out |
|---|---|---|
| "Of the 10 I flagged, 3 were really fraud" | 3 ÷ 10 | |
| "Of the 14 real frauds, I caught 3" | 3 ÷ 14 | |
| "Of the 986 legit ones, I left 979 alone" | 979 ÷ 986 | |

Three divisions. Then one question: **"which two of those three fractions have the same number on top?"** The first two. **That is objective 2, delivered with a calculator.**

**The copy-this-exactly scaffold.** Nine lines, and it runs on its own:

```python
from sklearn.metrics import confusion_matrix, precision_score, recall_score

#          10 transactions.  1 = fraud.
truth      = [0, 0, 1, 0, 0, 1, 0, 1, 0, 0]
prediction = [0, 1, 1, 0, 0, 0, 0, 1, 0, 0]

tn, fp, fn, tp = confusion_matrix(truth, prediction).ravel()
print("left alone %d   false alarm %d   missed %d   caught %d" % (tn, fp, fn, tp))
print("precision  %.4f   (of the %d I flagged, %d were fraud)" % (precision_score(truth, prediction), tp + fp, tp))
print("recall     %.4f   (of the %d real frauds, I caught %d)" % (recall_score(truth, prediction), tp + fn, tp))
```

```text
left alone 6   false alarm 1   missed 1   caught 2
precision  0.6667   (of the 3 I flagged, 2 were fraud)
recall     0.6667   (of the 3 real frauds, I caught 2)
```

Then three questions and nothing else: **"do the four numbers add to ten? how many did I flag? and how many were really fraud?"** Yes; three; three. That is objectives 1 and 2 in nine lines.

**One thing you must not cut:** the moment where the useless model scores 98.6% and catches nothing. If the whole lesson collapses to one sentence, make it *"a high score can mean the model has given up."*

### If the student is flying

None of these need syntax from a later week.

1. **Two models on the same forty cards** (Variation-harder 1), ending in *"which is better?"* — a question with no answer until somebody prices the two errors. This is the most grown-up conversation available today.
2. **Work backwards from the ratios to the counts** (Variation-harder 3). Genuinely hard.
3. **Build the piece of paper's 2×2 from the 40 cards** (Variation-harder 2) and explain why the useless model looks obviously useless there and brilliant on the fraud data. **The answer is rarity, and getting there unaided is a level-5 answer.**
4. **The smoke alarm question** (Variation-harder 5): TP 0, FP 0 — what one number do you need to judge it? The FN count.
5. **Show that accuracy is a weighted average of recall and specificity.** On our numbers: recall 0.2143 with weight 14/1000, specificity 0.9929 with weight 986/1000. Then 0.2143 × 0.014 + 0.9929 × 0.986 = 0.0030 + 0.9790 = **0.9820**, which is exactly the accuracy. **This is the single most illuminating five minutes available to a strong student this week** — it shows in arithmetic *why* accuracy drowns the rare class, and it needs nothing but multiplication.
6. **The honest question:** *"if we caught one more fraud, recall goes from 0.2143 to 0.2857. Is that a better model or a luckier one?"* Nobody can tell from one measurement. Week 11.

### If the student won't engage today

**Close the laptop. Forty cards and four labels.**

Better still: **let them choose the story.** Not fraud — a metal detector at a concert, or a teacher marking which homework is copied, or a smoke alarm. Anything with two classes where one is rare and being wrong matters in two different directions. Rewrite the pile labels in their story's words: `stopped a knife` · `stopped a belt buckle` · `let a knife through` · `waved them on`.

Then three instructions and nothing else:

> **"Sort the cards into the four piles."**
>
> **"Count each pile. Do they add up to forty?"**
>
> **"Now put your hand on the two piles where the machine said yes. How many? And how many of those were right?"**

That is nine out of fifteen — **objectives 1 and 2 delivered with paper in twelve minutes**, and it is the half of the lesson everything from here to Week 36 sits on. The typing survives; Week 9 revisits all of it.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the paradox (spoken, 45 seconds)**

> "A model is **99% accurate** at spotting a disease that one person in a hundred has. **Should I be impressed?**"

*Good answer:* "No. A model that says 'healthy' to everyone is also 99% accurate and catches nobody. I'd want to know how many of the sick people it found."

**What to catch:** "yes, that's very good." Do not correct with a rule; ask *"what would 'always say healthy' score?"*

**Check 2 — the denominators (spoken, 60 seconds)**

> "Four counts: **caught 3, false alarm 7, missed 11, left alone 979.** Give me precision and recall, and **say the sentence before you say the number.**"

*Good answer:* "Precision — of the 10 I flagged, 3 were fraud, so 3 ÷ 10 = 0.30. Recall — of the 14 real frauds, I caught 3, so 3 ÷ 14 = 0.21."

**Full marks needs both sentences said out loud before either division.** A student who produces the right decimals but cannot say which region of the table each came from is a level-2 answer.

**Check 3 — the two errors, as people (spoken, 90 seconds)**

> "You're building the fraud model that will run on real cards. **Describe one false positive and one false negative as things that happen to a real person on a real afternoon.** Then tell me which one you'd rather cause, and why."

*Good answer:* "A false positive is somebody's card declined at the till with a full trolley, and they have to walk out. A false negative is £240 taken from an account and nobody notices for three weeks. I'd rather cause the declined card, because it's embarrassing and fixable and the money is not gone — but I'd want to know how often it happens, because if it's every fifth transaction people will stop using the card."

**What to catch:** anything that stays in abbreviations. *"An FP is when a negative is classified positive"* is a definition, not a consequence, and it is the definition that lets people ship harmful systems with a clear conscience. Push once: *"and what happens to the person?"*

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Reads a high accuracy as a good model. Cannot place a described mistake in the right cell. Picks fraction denominators at random. |
| **2 — Emerging** | Names the four cells when prompted. Builds the 2×2 from a list with help. Computes precision and recall correctly but cannot say what the denominators mean. |
| **3 — Secure** | Builds the 2×2 unaided and checks that the four cells add to the row count. Computes precision, recall and specificity, **saying the denominator sentence for each**. Explains the accuracy paradox with the always-say-no model. Names both errors in application language. **This is the target.** |
| **4 — Strong** | Reports the majority-class rate next to every accuracy without being asked. Spots swapped `confusion_matrix` arguments by sanity-checking the FN count. States which error costs more for a stated application **and says who bears the cost**. Notes that 14 frauds is a small denominator. |
| **5 — Exceptional** | Shows unprompted that accuracy is a weighted average of recall and specificity, and uses that to explain why the rare class gets drowned. Argues that combining the four counts into one score requires an unstated exchange rate between two kinds of harm. Predicts, before Week 10 is mentioned, that raising recall must lower precision, and points at the table to say why. |

---

## 📤 Homework to Assign

This section gives the homework and the exact words to introduce it.

**Say this:**

> "About an hour, three pages, and I'm marking the last one hardest.
>
> **First, page 8.4 — build the 2×2 by hand from the thirty predictions on the page.** Thirty transactions, each with what really happened and what the model said. **Count them into four cells, then add the four cells up and check you get thirty.** If you don't get thirty, you've miscounted, and finding it is part of the job.
>
> **Second, page 8.5 — precision, recall and specificity, with the working shown.** And by working I mean: **for each one, write down which count you put on the bottom and why.** Not '0.6000'. '*Of the 10 I flagged, 6 were really fraud, so 6 ÷ 10 = 0.6000.*' The sentence is the answer; the decimal is just the arithmetic.
>
> **Third, page 8.6 — and this is the page I care about most. Describe one false positive and one false negative in the language of the actual application.** Pick your application — fraud, spam, a smoke alarm, a metal detector, marking homework — and write me **two sentences about a real person's real afternoon.** Not 'a negative instance was misclassified'. A person, a place, a time, and what went wrong for them. Then one more sentence: **which of the two would you rather cause, and why.**"

**Workbook pages:** 8.1, 8.2, 8.3 in class · **8.4, 8.5, 8.6** at home.

**Expected time:** 20 min counting the 30 predictions into the 2×2 and checking the addition · 20 min on the three fractions with their sentences · 20 min on the two application sentences and the choice. **About 60 minutes.**

> **🧑‍🏫 What to look for when you mark it:** three things, and the third is the real one. **One — do the four cells add up to 30?** If the page has no addition check on it, the habit has not been installed and it is worth one line of feedback every week until it is. **Two — is there a sentence naming the denominator beside every fraction?** A page of three correct decimals with no sentences is a page that has done the arithmetic and missed the lesson. **Three — are the two application sentences about a person?** The good answer names somebody, somewhere, at some time, and says what they lost. The weak answer defines the term again in different words. That difference is the whole reason this week exists: **a metric you can only say in abbreviations is a metric nobody will ever argue with, and metrics that nobody argues with are how bad systems get shipped.**

---

## 🔑 Answer Key

Every question restated, so you can mark from this page alone.

### Page 8.1 — Name the cell

*For each scenario, name the cell. The model's job is flagging fraud, so "positive" means "the model said fraud".*

| # | Scenario | Cell | Why |
|---|---|---|---|
| 1 | The card was stolen and the model flagged it. | **True Positive** | Predicted fraud, and right. **Caught one.** |
| 2 | An ordinary weekly shop, nothing flagged. | **True Negative** | Predicted legit, and right. **Correctly left alone.** |
| 3 | The card was stolen and the model let it through. | **False Negative** | Predicted legit, and wrong. **A miss.** |
| 4 | A tourist's genuine card was blocked in Rome. | **False Positive** | Predicted fraud, and wrong. **A false alarm.** |
| 5 | Somebody's £3 coffee was flagged as fraud. It wasn't. | **False Positive** | Same as 4. Small money, still a false alarm. |
| 6 | £2,000 was stolen and the model said nothing. | **False Negative** | Same as 3. The size of the loss does not change the cell. |
| 7 | The model flagged a transaction and the bank confirmed it was fraud. | **True Positive** | Predicted fraud, and right. |
| 8 | A legitimate transaction went through untouched. | **True Negative** | Predicted legit, and right. |
| 9 | The model flagged 200 transactions and 6 were fraud. | **6 True Positives and 194 False Positives.** | A trap: one sentence can describe many cards. **Precision would be 6 ÷ 200 = 0.0300.** |
| 10 | The model has never once said "fraud" in a year. | **FP = 0 and TP = 0.** | The entire predicted-fraud column is empty. **That is the fingerprint of a model that has given up**, and its accuracy will look excellent. |

**Rows 9 and 10 are the two worth discussing.** Row 9 breaks the one-card-one-cell assumption. Row 10 is the whole hook, restated as a scenario.

### Page 8.2 — Predict the lazy model (in pen, before running)

*The `DummyClassifier(strategy="most_frequent")` on 1,000 validation rows containing 14 frauds. Predict all four counts and the accuracy.*

| | Prediction to expect | The truth |
|---|---|---|
| TN | 986 | **986** |
| FP | 0 | **0** |
| FN | 14 | **14** |
| TP | 0 | **0** |
| accuracy | 986 ÷ 1000 | **0.9860** |

**The two zeros are the answer to the whole page.** A student who predicts a non-zero FP has not yet grasped that "most frequent" means it *never* says fraud — and the fastest cure is to ask *"how many times does it say fraud?"*

**And the bonus line if they got all four:** precision is **undefined**, because its denominator is TP + FP = 0. scikit-learn prints 0.0000 and warns you. **"Undefined" is a better answer than "0" here** and should be marked as such.

### Page 8.3 — The forty cards

*The full list. Twelve are actually fraud; the model flags fifteen.*

| # | actual | predicted | | # | actual | predicted |
|---|---|---|---|---|---|---|
| 1 | legit | legit | | 21 | legit | fraud |
| 2 | legit | legit | | 22 | fraud | fraud |
| 3 | fraud | fraud | | 23 | legit | legit |
| 4 | legit | legit | | 24 | legit | legit |
| 5 | legit | fraud | | 25 | fraud | fraud |
| 6 | fraud | legit | | 26 | legit | legit |
| 7 | legit | legit | | 27 | legit | fraud |
| 8 | fraud | fraud | | 28 | legit | legit |
| 9 | legit | legit | | 29 | fraud | fraud |
| 10 | legit | legit | | 30 | legit | legit |
| 11 | fraud | fraud | | 31 | legit | legit |
| 12 | legit | fraud | | 32 | fraud | fraud |
| 13 | legit | legit | | 33 | legit | legit |
| 14 | fraud | legit | | 34 | legit | fraud |
| 15 | legit | legit | | 35 | legit | legit |
| 16 | fraud | fraud | | 36 | legit | legit |
| 17 | legit | legit | | 37 | legit | legit |
| 18 | legit | fraud | | 38 | legit | legit |
| 19 | legit | legit | | 39 | fraud | legit |
| 20 | fraud | fraud | | 40 | legit | legit |

**The four piles:**

| | predicted legit | predicted fraud | row total |
|---|---|---|---|
| **actual legit** | **22** left alone | **6** false alarm | 28 |
| **actual fraud** | **3** missed | **9** caught | 12 |
| column total | 25 | 15 | **40** |

**The check: 22 + 6 + 3 + 9 = 40.** ✅

**The arithmetic, in full:**

```text
precision   =  9 ÷ (9 + 6)   =   9 ÷ 15  =  0.6000
recall      =  9 ÷ (9 + 3)   =   9 ÷ 12  =  0.7500
specificity = 22 ÷ (22 + 6)  =  22 ÷ 28  =  0.7857
accuracy    = (9 + 22) ÷ 40  =  31 ÷ 40  =  0.7750
```

**Checked against scikit-learn:**

```text
40-card activity: tn 22 fp 6 fn 3 tp 9
precision 0.6000  recall 0.7500  specificity 0.7857  accuracy 0.7750  F1 0.6667
```

*(Ignore the F1 for now. It is next week and it is 2 × 9 ÷ (18 + 6 + 3) = 18 ÷ 27 = 0.6667, which you may want in your pocket for Week 9.)*

### Page 8.4 — The 2×2 by hand from 30 predictions

*Thirty transactions. `1` means fraud / flagged.*

| # | actual | predicted | | # | actual | predicted | | # | actual | predicted |
|---|---|---|---|---|---|---|---|---|---|---|
| T01 | 0 | 0 | | T11 | 1 | 1 | | T21 | 0 | 0 |
| T02 | 0 | 0 | | T12 | 0 | 1 | | T22 | 0 | 0 |
| T03 | 1 | 1 | | T13 | 0 | 0 | | T23 | 1 | 0 |
| T04 | 0 | 0 | | T14 | 1 | 0 | | T24 | 0 | 1 |
| T05 | 0 | 1 | | T15 | 0 | 0 | | T25 | 0 | 0 |
| T06 | 1 | 0 | | T16 | 1 | 1 | | T26 | 1 | 1 |
| T07 | 0 | 0 | | T17 | 0 | 0 | | T27 | 0 | 0 |
| T08 | 1 | 1 | | T18 | 0 | 1 | | T28 | 0 | 0 |
| T09 | 0 | 0 | | T19 | 0 | 0 | | T29 | 0 | 0 |
| T10 | 0 | 0 | | T20 | 1 | 1 | | T30 | 0 | 0 |

**Sorting them, card by card:**

- **True Positives** (actual 1, predicted 1): T03, T08, T11, T16, T20, T26 → **6**
- **False Positives** (actual 0, predicted 1): T05, T12, T18, T24 → **4**
- **False Negatives** (actual 1, predicted 0): T06, T14, T23 → **3**
- **True Negatives** (actual 0, predicted 0): everything else → **17**

**The 2×2:**

| | predicted legit | predicted fraud | row total |
|---|---|---|---|
| **actual legit** | **17** left alone | **4** false alarm | 21 |
| **actual fraud** | **3** missed | **6** caught | 9 |
| column total | 20 | 10 | **30** |

**The check: 17 + 4 + 3 + 6 = 30.** ✅ And 9 real frauds, 10 flagged.

**Confirmed against scikit-learn:**

```text
n = 30  actual fraud = 9  flagged = 10
tn 17  fp 4  fn 3  tp 6
```

### Page 8.5 — Precision, recall and specificity, with the working shown

*From the four counts on page 8.4: TP 6, FP 4, FN 3, TN 17.*

**Precision — "of everything I flagged, how much was really fraud?"**

```text
I flagged  TP + FP  =  6 + 4  =  10
Of those,  6  were really fraud.
precision  =  6 ÷ 10  =  0.6000
```

**The count on the bottom is 10, because 10 is how many I flagged.**

**Recall — "of everything that really was fraud, how much did I catch?"**

```text
Real frauds  TP + FN  =  6 + 3  =  9
Of those,  6  were caught.
recall  =  6 ÷ 9  =  0.6667
```

**The count on the bottom is 9, because 9 is how many frauds there really were.**

**Specificity — "of everything that really was legitimate, how much did I correctly leave alone?"**

```text
Real legit  TN + FP  =  17 + 4  =  21
Of those,  17  were left alone.
specificity  =  17 ÷ 21  =  0.8095
```

**The count on the bottom is 21, because 21 is how many were really legitimate.**

**And accuracy, for comparison:**

```text
correct  =  TP + TN  =  6 + 17  =  23
accuracy  =  23 ÷ 30  =  0.7667
```

**Confirmed against scikit-learn:**

```text
accuracy    0.7667  (23/30)
precision   0.6000  (6/10)
recall      0.6667  (6/9)
specificity 0.8095  (17/21)
```

**Marking notes.** Full marks needs **the sentence naming the denominator** beside each fraction, not just the correct decimal. Three correct decimals with no sentences is a level-2 answer, and say so on the page — this is the single habit that carries them through Weeks 9, 10 and 11.

**One thing to praise if you see it:** a student who notices that the **majority-class rate here is 21 ÷ 30 = 0.7000**, and that accuracy 0.7667 therefore beats it by a decent margin, has applied this week's rule to a *balanced-ish* table unprompted. That is a level-4 observation.

### Page 8.6 — One false positive, one false negative, in the language of the application

*Marked on whether it is about a person, not on whether it is well written.*

**A full-marks answer for fraud detection:**

> **The false positive.** "Mrs Okafor's card was declined at the supermarket checkout on Saturday afternoon. She had a full trolley and two children with her, and eleven people in the queue behind her. She had to leave the shopping at the till and drive home. She spent forty minutes on the phone to the bank on Sunday and she has started carrying cash."
>
> **The false negative.** "Somebody used Daniel's card details to buy £240 of vouchers at 3am. Nobody noticed for three weeks, because the amount was small enough not to look strange. By the time he reported it the vouchers had been spent and the money was gone."
>
> **Which would I rather cause?** "The declined card, because the money is not gone and it can be undone with a phone call, whereas the £240 cannot. But I would want to know **how often** — if we decline one legitimate card in every twenty, people stop using the card at all, and the bank has solved fraud by making the card useless. So my answer depends on the count, not just the cell."

**A full-marks answer for a smoke alarm:**

> **False positive:** "The alarm went off at 7am because of toast. The whole family went outside in dressing gowns in February. Two weeks later somebody took the battery out, which is the actual danger."
>
> **False negative:** "There was a fire in the kitchen at 2am and the alarm stayed silent."
>
> **Which would I rather cause?** "The toast. Every time, without hesitation — a false alarm costs five cold minutes and a miss can cost a life. **But** the fact that false alarms make people remove the battery means the false positive can *cause* the false negative, so 'I don't care about false alarms' is not actually a safe position."

**Marking notes:**

- **A person, a place, a time, and what they lost.** That is the bar. Anything that begins "a legitimate instance was incorrectly..." scores zero on this page, however accurate it is, and say why: *"that's the definition again. What happened to the person?"*
- **The best answers notice that the two errors interact.** The smoke-alarm answer above is a level-5 answer because it spots that too many false positives create false negatives — people disable the system. Fraud has the same shape: too many declines and customers switch banks, so nobody is protected at all.
- **The best answers also ask "how often".** The cell tells you *what kind* of wrong; only the count tells you *how bad*. A student who says "it depends on the count" has understood the whole week.

### Answers to every question posed in the lesson

**Hook — "work out its accuracy."** 986 of the 1,000 validation rows are legitimate, and it says "not fraud" to all 1,000, so it gets 986 right. **986 ÷ 1000 = 0.9860.**

**Hook — "how many frauds did it catch?"** **Zero, out of 14.** TP = 0 and FP = 0: the whole predicted-fraud column is empty.

**Hook — "which would you rather have running on your card?"** The real model, at 98.20%. It has *lower* accuracy and it catches 3 of the 14 instead of 0. **Accuracy went down and the model got better**, which is why accuracy on its own is not a usable report.

**Concept — the three fast naming questions.** *Stolen card let through* → **false negative** (predicted negative, wrong). *Good card blocked in Rome* → **false positive** (predicted positive, wrong). *Ordinary shop, nothing flagged* → **true negative**.

**Concept — "add all four up. What should you get?"** 1000, the number of validation rows. **979 + 7 + 11 + 3 = 1000.**

**Concept — "how many did I flag?"** 7 + 3 = **10**. **"How many of the ten were really fraud?"** **3.** So precision = 3 ÷ 10 = **0.3000**.

**Concept — "how many really were fraud?"** 11 + 3 = **14**. **"And I caught?"** **3.** So recall = 3 ÷ 14 = **0.2143**.

**Concept — specificity.** 979 ÷ (979 + 7) = 979 ÷ 986 = **0.9929**.

**Live-code step 1 — "how many fraud rows out of 5,000 at 1%?"** Most will say 50. The real answer is **72**, a rate of **0.0144**. `weights` sets the target count (50), and the default `flip_y=0.01` label noise moves it to 72. **The habit being taught is: ask for something, then check what you got.**

**Live-code step 2 — the three piles.** train 3000 (44 fraud), val 1000 (14 fraud), test 1000 (14 fraud). **44 + 14 + 14 = 72**, every fraud accounted for, and `stratify=y` is what kept the rates equal across the piles.

**Live-code step 4 — "is that an error or a warning, and what is it telling us?"** A **warning**: the program printed 0.0000 and carried on. It says *"no predicted samples"* — precision's denominator is TP + FP = 0, so the quantity is undefined. **The message is describing the model, not a bug in the code.**

**Live-code step 5 — "which two numbers moved, and did the program complain?"** The **7 and the 11** — false positives and false negatives — have swapped places. **Nothing complained.** The cause is `confusion_matrix(pred, y_val)`: truth must go first. The sanity check is that FN is "frauds I missed", which is 11 on this data.

**Live-code step 6 — "which is better, and how do you know?"** The tree, because it caught 3 of 14 and the dummy caught 0. **And you answered it without using accuracy at all** — you used the four counts.

**Wrap — "if we flag more things, what happens to precision?"** It usually falls. Most of what you newly flag comes out of the legitimate column, so FP rises faster than TP. **Recall and precision sit on opposite ends of a see-saw**, which is Week 9's whole subject and Week 10's dial.

**Variation-harder 1 — "which model is better?"** The bold model: precision 9 ÷ 15 = **0.6000**, recall 9 ÷ 12 = **0.7500**. The cautious model: precision 5 ÷ 6 = **0.8333**, recall 5 ÷ 12 = **0.4167**. **Neither is better without knowing what the two errors cost.** The bold model catches nearly twice as many frauds and raises six times as many false alarms (6 against 1). **A student who says "you can't tell yet" is completely right and should be told so.**

**Variation-harder 2 — the piece of paper on the 40 cards.** Everything goes to `LEFT ALONE` and `MISS`: TN 28, FN 12, FP 0, TP 0. Accuracy = 28 ÷ 40 = **0.7000**, recall = 0 ÷ 12 = **0**. **On this data the useless model looks obviously useless.** It looked brilliant on the fraud data because 14 in 1,000 is far rarer than 12 in 40. **The paradox is caused by rarity, not by accuracy being a bad idea.**

**Variation-harder 3 — working backwards.** Precision 0.5 and recall 0.5 with 12 real frauds: recall 0.5 of 12 gives TP = 6, so FN = 6. Precision 0.5 means TP = FP, so FP = 6. With 40 cards, TN = 40 − 6 − 6 − 6 = **22**. Check: 6 + 6 + 6 + 22 = 40. ✅

**Variation-harder 5 — the smoke alarm.** It has TP = 0 and FP = 0, so precision is undefined and specificity is a perfect 1.0. **The number you need is the FN count: how many fires there were.** Zero fires and it has made no mistakes yet (though it has never been tested either, so recall is 0 ÷ 0); one fire and it failed at the only job it had. **Two of the four cells are empty and the two that matter are the two you cannot see from the alarm itself.**

**Flying 5 — accuracy as a weighted average.** Recall is 0.2143 on 14 rows; specificity is 0.9929 on 986 rows.

```text
0.2143 × (14 ÷ 1000)  =  0.2143 × 0.014  =  0.0030
0.9929 × (986 ÷ 1000) =  0.9929 × 0.986  =  0.9790
                                            ------
                                            0.9820
```

**Which is exactly the accuracy.** So accuracy is 98.6% "did you leave the easy ones alone" and 1.4% "did you catch the hard ones". **That is the paradox, in arithmetic, and it is the best explanation of it available at this level.**

---

## 🔮 Next Week Preview

Next week is the Term 1 checkpoint, and it answers the question this lesson ends on. Precision 0.3000 and recall 0.2143 — two numbers, pulling against each other, and a report has room for one. The plain average of 0.9 and 0.1 is a comfortable 0.5, which is exactly the wrong answer for a pair that lopsided; so the student meets a different kind of average, the **harmonic mean**, computes it by hand for three pairs, and finds that it lands near the *smaller* of the two every time. Then the whole of Term 1 gets re-run from memory at five stations in under 45 minutes — audit, split, baseline, pipeline, metrics — ending in one saved file on disk.

**To prep early:** two things. **One — leave both wall artifacts up**, this week's 2×2 and Week 7's ablation table. Week 9 uses both and re-drawing them costs ten minutes. **Two — set up the five relay stations before the lesson, physically**, with a printed instruction card and a printed "what you hand over" line at each one. Eight minutes per station with a timer means there is no time at all for a student to work out what a station wants; the card has to do it. And check now that the student's own Week 7 pipeline still runs — Week 9's homework is the full metrics report for *their* model, and a broken file on the day turns a 20-minute task into an hour.

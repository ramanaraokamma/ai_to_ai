# Week 30 — Classifier Lab: Scaling, k, and the Confusion Matrix

[⬅ Week 29](week-29.md) · [Course Home](../README.md) · [Week 31 ➡](week-31.md) · [Student Guide](../student-guide/week-30.md) · [Workbook](../workbook/week-30.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟩 Lab — one experiment, run end to end, finished and saved by the end of class |
| **Big idea** | If one feature is measured in thousands it drowns out the others — so you scale, and you fit the scaler on the training rows only. |
| **New vocabulary** | accuracy · confusion matrix · feature scaling · leakage · stratify |
| **New syntax** | `accuracy_score(y_test, pred)` · `confusion_matrix(y_test, pred)` · `StandardScaler().fit(X_train)` then `.transform(X_test)` · `stratify=y` |
| **Materials** | The printed workbook (its Warm-Up, Predict the Output, Practice Sets A and B, Fix the Broken Program, Puzzle, Think Deeper, Build It, Draw It and Self-Check sections) · a calculator · **THE GAP still on the board from Week 29** · last week's `full_cycle.py` · a highlighter |
| **Tech needed** | The Week 28 setup. Nothing new to install. **The lab saves a PNG**, so check `fig.savefig(...)` still works before class. |
| **Prep time** | 20 minutes the night before (most of it running the lab yourself), 5 minutes on the day |

> **⚠️ Watch out:** this file uses `random_state=31`, not the `42` of Week 29. Any fixed whole number is equally valid, and 31 is the one every number printed in this file came from — so if you use 42 instead, your screen will not match this guide. There is also an honest reason for the choice, and a student may well ask about it: see the second-to-last entry in **Questions Students Ask This Week**. Answer it straight when they do.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Compute accuracy and read a confusion matrix out loud**, naming what got mistaken for what.
2. **Explain why a feature measured in thousands overwhelms one measured in units.**
3. **Scale features by fitting the scaler on the training rows only**, and say why that matters.
4. **Plot accuracy against `k` for 1 to 25 and choose a `k` with a written reason.**
5. **Keep the class mix the same in both halves of the split, using `stratify`.**

Observable evidence: a saved PNG with two labelled lines and a y-axis starting at zero; a comparison table with train *and* test accuracy in it; a chosen `k` with three written sentences underneath it; and a confusion matrix with its worst row circled in highlighter.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

Four ideas. The first two are arithmetic, the third is a habit, and the fourth is a trap.

### 1. Accuracy, and the number you must put next to it

> **Accuracy** — the fraction of guesses that were right. Number right ÷ number of guesses.

The student has been computing this since Level 1; this week the library computes it for them.

```python
from sklearn.metrics import accuracy_score
accuracy_score(y_test, predictions)
```

`accuracy_score` takes the **truth first and the guesses second**. That order is a convention and it is worth saying out loud, because for accuracy it makes no difference (28 right out of 36 either way) but for the confusion matrix in section 3 it makes all the difference. `model.score(X_test, y_test)` computes exactly the same number for a classifier; `accuracy_score` is what you use when you already have the predictions in hand and want to do several things with them.

**Accuracy has a trap, and Level 1 already taught it.** If 99% of emails are not spam, a machine that says "not spam" to everything scores 99% and has never read an email. So before you are allowed to be pleased with an accuracy, you compute the **baseline**: what would the laziest possible model score?

For the wine table:

```text
class counts : [59 71 48]
baseline     : 0.3989 (always shout the commonest class)
```

Always shout "class 1" and you get 71 of 178 right — **39.89%**. That is the floor. Any accuracy the student reports this week gets compared to 0.3989 or it means nothing, and they should write the baseline down before they train anything.

### 2. Scaling: why one column can drown out twelve

kNN measures distance. Distance is **squares added up**. So a column whose numbers are large contributes large squares, and large squares swamp small ones. This is not a subtle statistical worry; it will quietly wreck a model.

Here is the actual arithmetic from the wine table, and it is the single most convincing thing in the week. Wine 0 and wine 1, looking at only two of the thirteen columns:

```text
    hue  proline
0  1.04   1065.0
1  1.05   1050.0

hue gap     : -0.01   squared: 0.0001
proline gap : 15.00   squared: 225.0000
total       : 225.0001
distance    : 15.0000

hue's share of the distance    : 0.000044 %
proline's share of the distance: 99.999956 %
```

**`hue` contributed forty-four millionths of one percent.** It may as well not be in the table. And there is nothing special about `hue` — the same is true of every one of the other twelve columns (magnesium, the next biggest, has a squared spread about 480 times smaller than proline's). The model is effectively using one measurement and ignoring the rest, **not because `proline` is more informative, but because somebody chose to write it in bigger numbers.**

🍕 **The analogy that lands.** Compare two people by height in *millimetres* and age in *years*. Person A is 1700 mm and 12 years old. Person B is 1750 mm and 40 years old. Distance = √(50² + 28²) = √3284 = 57.3. The 50 mm height difference contributes 2500; the 28-year age gap contributes 784. **So the model thinks a 5 cm height difference matters three times more than being 28 years older.** Now write the heights in metres — 1.70 and 1.75 — and the height contribution becomes 0.0025 and the age gap runs the whole show. **Nothing about the two people changed. Your model's opinion should not depend on which unit somebody happened to type.**

![One column shouting over twelve others](../figures/fig-w30-1-one-feature-drowns-the-rest.svg)
*Figure 30.1 — On the left, `proline` is 99.999956% of the distance. On the right, after each gap is divided by its column's spread, both columns have a real say.*

**The fix, in one sentence:** divide every column's gap by how much that column normally varies. So a gap counts as "big" when it is big *for that column*, not when the number is big.

> **Feature scaling** — putting every column on the same footing before you measure distances.
> **Standardisation** — the usual way to do it: rescale each column so it has mean 0 and spread 1, using `z = (value − mean) ÷ spread`. Every column then speaks the same language: *how many spreads away from typical am I?*

In code — and note there are **two** steps, `fit` then `transform`, exactly like a model:

```python
scaler = StandardScaler()                # the machine that rescales columns
scaler.fit(X_train)                      # LEARN the mean and spread of each column
X_train_scaled = scaler.transform(X_train)   # apply them to the training rows
X_test_scaled = scaler.transform(X_test)     # apply the SAME ones to the test rows
```

Here is what it actually learns and does, on the real wine training rows:

```text
proline mean learned  : 744.17
proline spread learned: 307.03

proline BEFORE, first 5 training rows: [ 680.  450.  615.  415. 1280.]
proline AFTER , first 5 training rows: [-0.21 -0.96 -0.42 -1.07  1.75]

every scaled column now has mean ~0: [-0. -0. -0. -0.]
every scaled column now has spread 1: [1. 1. 1. 1.]
```

Read the third line to the student. `680` became `−0.21`, which says *"a bit below typical"*. `1280` became `1.75`, which says *"nearly two spreads above typical"*. **That is a much more useful thing to know about a wine than 680.**

> **⚠️ Watch out:** the scaled numbers are negative about half the time, and that surprises people. Half the wines are below average; below average is a negative number of spreads. Nothing is wrong.

### 3. The confusion matrix: the same grid Level 1 drew by hand

An accuracy is one number and it hides everything interesting. The confusion matrix does not.

> **Confusion matrix** — a grid where the row says what the thing really was and the column says what the model guessed. The diagonal is "got it right"; everything off the diagonal is a *specific, named* mistake.

The wine model with raw, unscaled columns:

```text
[[12  0  0]
 [ 0 13  1]
 [ 2  5  3]]
```

**Read it out loud, row by row.** This is a skill and it needs practising:

- **Row 0** — 12 wines were really class 0. All 12 were called class 0. Perfect.
- **Row 1** — 14 wines were really class 1. 13 were called class 1; 1 was called class 2.
- **Row 2** — 10 wines were really class 2. **Only 3 were called class 2.** 5 were called class 1 and 2 were called class 0.

**That last row is the whole story, and the accuracy of 0.7778 hides it completely.** Seventy-eight percent sounds like a working model. The grid says: this model is perfect on one grape, good on another, and **nearly blind to the third** — it gets 3 out of 10 class-2 wines, which is worse than a coin.

![Read the grid one row at a time](../figures/fig-w30-4-confusion-matrix-read-aloud.svg)
*Figure 30.2 — Row 2 is the worst row: 2 + 5 + 3 = 10 real class-2 wines, and only 3 of them were named correctly.*

Two things to be careful of:

- **`confusion_matrix(y_test, pred)` — truth first.** Swap the arguments and you get the *transpose*: the grid flipped along the diagonal, so rows become guesses and columns become truths. The diagonal is unchanged, so accuracy looks the same, and you will read every mistake backwards. Say "truth first" out loud every time.
- **Rows add up to the real counts; columns add up to the guessed counts.** Row 2 adds to 10 because there were 10 real class-2 wines. Column 1 adds to 18 because the model said "class 1" eighteen times. That asymmetry is what makes the grid informative.

### 4. `stratify=y`: keep the mix

`train_test_split` shuffles and cuts. If the classes are uneven, an unlucky shuffle hands you a lopsided test set. On wine, with our seed:

```text
whole table, class counts: [59 71 48]

NO stratify  -> test class counts: [ 9 18  9]
WITH stratify-> test class counts: [12 14 10]
```

The whole table is 33% / 40% / 27%. Without `stratify` the test set came out **25% / 50% / 25%** — half of it is one class. Your estimate of how the model handles class 0 is now based on nine wines, and each of those nine is worth eleven percentage points of "class 0 accuracy".

> **stratify** — force each class to keep the same share in both halves of the split. One keyword, and it removes a whole category of bad luck. `stratify=y` — the labels, not the features.

Use it for every classification problem, always. It costs nothing.

### 5. The trap: leakage, and the bug whose symptom is a *better* score

This is the hard idea of the week, and it is genuinely counter-intuitive, so read this twice.

The scaler has to learn two numbers per column: a mean and a spread. **Where does it learn them from?** The obvious, tidy-looking thing is to scale everything first and split afterwards:

```python
scaler.fit(X)                 # <-- ALL 178 wines, test rows included
X_all_scaled = scaler.transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_all_scaled, y, ...)
```

That is a bug. The means and spreads now contain information from the test rows — so the test rows have influenced how the training data was prepared. They are no longer rows your process has never seen.

> **Leakage** — information from the test set sneaking into training, usually through preprocessing done before the split.

And here is the part that makes it dangerous rather than merely wrong. **When you run the buggy version, the score goes UP.**

```text
scaled, scaler fitted on train only : 0.9444   (34 of 36)
scaled, scaler fitted on everything : 0.9722   (35 of 36)
```

One extra wine. A better number. If you were chasing a high score you would keep the bug and never know.

![The bug that makes your score go up](../figures/fig-w30-5-leak-raises-the-score.svg)
*Figure 30.3 — The third bar is higher and it is the only one that is a lie.*

**How to explain why a higher number is bad news.** The score is not a prize. It is an **estimate of how the model will do on wines nobody has ever seen**. The moment the test rows helped prepare the training data, the score stopped being that estimate. It became a slightly optimistic number about a situation that will never happen again — because in real life the new wine arrives *after* you have finished building, and it cannot possibly have contributed to your means and spreads.

The sentence to use, and it is worth writing on the board:

> **You did not make the model better. You made the exam easier and forgot to say so.**

And the honest footnote, which matters: **on some splits the leak changes nothing at all.** With `random_state=42` the two numbers come out identical. That does not mean the leak was harmless — it means you got away with it, and you cannot tell in advance which kind of leak you have. The habit is the protection, not the vigilance.

![The scaler learns from the train pile only](../figures/fig-w30-2-scaler-fitted-on-train-only.svg)
*Figure 30.4 — The scaler is allowed to look at the blue pile and nothing else. The pink pile gets the blue pile's numbers applied to it.*

### 6. Choosing `k`, and the honesty sentence that must go with it

Try every `k` from 1 to 25, plot the accuracy, and look at the shape rather than the peak.

```text
k =  7   raw = 0.7222   scaled = 0.9722
k =  8   raw = 0.7222   scaled = 0.9722
k =  9   raw = 0.7778   scaled = 0.9722
k = 10   raw = 0.7500   scaled = 0.9722
```

Four consecutive values of `k` all give 0.9722. That is a **plateau**, and a plateau is trustworthy — it says the answer does not depend on getting `k` exactly right. A single lonely spike at one value of `k`, with dips either side, is usually luck.

**The rule of thumb:** pick a `k` inside a flat, high region, and prefer a *larger* one, because larger `k` is less jumpy. Prefer an odd one, because odd `k` ties less often. So from `{7, 8, 9, 10}`: **`k = 9`**.

And then the part most people skip. **You just chose `k` by looking at the test scores.** Twenty-five times. So the test set helped you make a decision, which means your reported accuracy is a little optimistic — you have used up some of the envelope's honesty. The professional fix is a third split, or cross-validation, and that is Level 3. For now, the honest thing is one sentence written next to the number:

> *"I chose this k by looking at test scores, which makes this estimate slightly optimistic."*

Make the student write it. Every time, all term. **Admitting a known limitation in writing is a skill, and it is more valuable than the model.**

### 7. Every line of this week's new code, explained

```python
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix
```

Two new rooms. `preprocessing` holds tools that prepare data. `metrics` holds tools that mark answers. One `import` line can fetch two names, separated by a comma.

```python
scaler = StandardScaler()
```

Makes the machine. Nothing has been learnt yet — same as `KNeighborsClassifier(...)` last week.

```python
scaler.fit(X_train)
```

Learns one mean and one spread **per column**, from the training rows only. It never sees `y`; it is not predicting anything, only measuring.

```python
X_train_scaled = scaler.transform(X_train)
```

Applies the arithmetic and hands back a **new** array. It does not change `X_train` — the original is untouched, which is why you need a new name on the left. This is exactly the `sorted()` habit from Week 12: a machine that returns a copy rather than editing in place.

```python
accuracy_score(y_test, predictions)
```

Truth first, guesses second. Returns one number between 0 and 1.

```python
confusion_matrix(y_test, predictions)
```

Truth first, guesses second. Returns a grid. Rows are truths, columns are guesses.

```python
train_test_split(X, y, test_size=0.2, random_state=31, stratify=y)
```

The one new keyword is `stratify=y`. It is the **labels** you stratify on, never the features. `stratify=X` produces a genuinely confusing error and it is in the Clinic.

### 8. How deep to go, and where to stop

**Go this far:** baseline, accuracy, confusion matrix read aloud, why scaling matters, fit-on-train-only, the accuracy-vs-`k` plot, `stratify`, the honesty sentence.

**Stop before:**
- **Pipelines.** `make_pipeline(StandardScaler(), KNeighborsClassifier(5))` does all of this in one leak-proof line and it is genuinely better practice. **Do not teach it this year.** The whole point of doing `fit` and `transform` by hand is that the student can *see* where the leak gets in. A pipeline hides the thing being taught.
- **Other scalers.** `MinMaxScaler`, `RobustScaler`. Not this year.
- **Precision, recall, F1.** They are the right next step after a confusion matrix and they belong in Level 3.
- **Cross-validation.** Level 3.
- **The word "overfitting".** Still Week 33's word, even though the scaled model's train/test gap (0.9859 vs 0.9444) is a perfectly good example of it. Say "memorised a bit". Hold the word.
- **Class weights or resampling.** If a student asks how to make the model better at class 2, the answer this week is "better features or better scaling", not "reweight the classes".

---

### 9. 🧭 The Growing Map — two minutes on the difference between a number and a grid

The student guide carries one figure a week that is not about the week's topic: the same five-stage
pipeline, one more piece inked in. It is the only place either book shows the learner the shape of the
whole year. Today it is worth showing at the very end, after the PNG is saved.

![The Level 2 pipeline in Week 30: still the X, y, kNN and trees tile, now scaling features and reading a confusion matrix](../figures/fig-w30-0-where-this-fits.svg)

*Figure 30.0 — Week 30's version. Third week inside the `X, y · kNN · trees` tile, weeks 28 to 31.
Nothing moves; the lab happens inside the box. Two threads lit: representation and evaluation.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it, then ask the question that sorts this lesson out:** *"today's two jobs were scaling and
   the grid. Which one made the model better, and which one made you better?"* Scaling changed the
   model; the confusion matrix changed nothing except what they can see. That distinction is the whole
   lesson, and most students get it in one go when it is put as a choice between two things they both
   did. Follow it with *"and which rows did the scaler get to look at?"* — **training only**, said fast.
2. **Then the map question:** *"the gold box says `kNN` and we did not change the model at all today.
   So what did we change?"* You want *the features* or *the units*. It is the first time this course
   has improved a result without touching the model, and naming that is worth the time on its own.
3. **Have them ink their own copy** and write one line from their confusion matrix next to the tile —
   the worst off-diagonal cell, as *"6 × class 1 called class 2"*. One line only. The discipline of
   choosing the worst cell is the skill.

> **🧑‍🏫 Why this is worth two minutes.** Lab weeks are the easiest weeks to remember as *"we ran a
> thing"*, and the map is the cheapest available defence against that. It also sets up the leakage
> lesson to last: they can see that `PREDICT & CHECK` is a stage with four tiles behind it and one
> ahead, so *fit the scaler on the training rows only* reads as a rule that will be in force for the
> rest of the course, not a detail of today's file. Expect the honest question *"does it matter that
> much?"* — the answer is that it is the bug whose only symptom is a better score.

---

## 🧰 Prep Checklist

### 20 minutes the night before

- [ ] **Run the whole lab yourself, once, end to end.** This is not optional this week — the lab trains fifty models and saves a chart, and you want to have seen every number before it appears on a shared screen. The complete file is in the Answer Key under **Build It — The Classifier Lab**; type or paste it and run it. It takes a couple of seconds.
- [ ] **Check the chart actually saved.** After running, look in the folder for `wine_accuracy_vs_k.png` and open it. If it is missing or empty, that is a Week 25 problem and you want to find it tonight.
- [ ] **Run the "why scaling" arithmetic yourself.** Create `why_scaling.py`:

  ```python
  # why_scaling.py
  # Two columns, side by side, and the arithmetic that shows one drowning the other.

  import numpy as np
  import pandas as pd
  from sklearn.datasets import load_wine

  wine = load_wine()
  grapes = pd.DataFrame(wine.data, columns=wine.feature_names)

  print("the first five wines, two columns only:")
  print(grapes[["hue", "proline"]].head())
  print()

  # Copy wine 0 and wine 1 out of that printout, by hand.
  hue_gap = 1.04 - 1.05                    # the two hue values
  proline_gap = 1065.0 - 1050.0            # the two proline values

  print("--- with the raw numbers ---")
  print(f"hue gap     : {hue_gap:.2f}   squared: {hue_gap ** 2:.4f}")
  print(f"proline gap : {proline_gap:.2f}   squared: {proline_gap ** 2:.4f}")
  total = hue_gap ** 2 + proline_gap ** 2
  print(f"total       : {total:.4f}")
  print(f"distance    : {np.sqrt(total):.4f}")
  print(f"hue's share of the distance    : {100 * hue_gap ** 2 / total:.6f} %")
  print(f"proline's share of the distance: {100 * proline_gap ** 2 / total:.6f} %")
  print()

  # Now divide each gap by how much that column normally varies.
  # (No model is being trained here. We are only looking at the numbers.)
  hue_spread = np.std(grapes["hue"])
  proline_spread = np.std(grapes["proline"])
  print("--- after dividing by each column's spread ---")
  print(f"hue spread     : {hue_spread:.4f}")
  print(f"proline spread : {proline_spread:.4f}")

  hue_fair = hue_gap / hue_spread
  proline_fair = proline_gap / proline_spread
  print(f"hue gap     : {hue_fair:.4f}   squared: {hue_fair ** 2:.4f}")
  print(f"proline gap : {proline_fair:.4f}   squared: {proline_fair ** 2:.4f}")
  total_fair = hue_fair ** 2 + proline_fair ** 2
  print(f"total       : {total_fair:.4f}")
  print(f"hue's share of the distance    : {100 * hue_fair ** 2 / total_fair:.2f} %")
  print(f"proline's share of the distance: {100 * proline_fair ** 2 / total_fair:.2f} %")
  ```

  Expected output, exactly:

  ```text
  the first five wines, two columns only:
      hue  proline
  0  1.04   1065.0
  1  1.05   1050.0
  2  1.03   1185.0
  3  0.86   1480.0
  4  1.04    735.0

  --- with the raw numbers ---
  hue gap     : -0.01   squared: 0.0001
  proline gap : 15.00   squared: 225.0000
  total       : 225.0001
  distance    : 15.0000
  hue's share of the distance    : 0.000044 %
  proline's share of the distance: 99.999956 %

  --- after dividing by each column's spread ---
  hue spread     : 0.2279
  proline spread : 314.0217
  hue gap     : -0.0439   squared: 0.0019
  proline gap : 0.0478   squared: 0.0023
  total       : 0.0042
  hue's share of the distance    : 45.76 %
  proline's share of the distance: 54.24 %
  ```

- [ ] **Practise reading the raw confusion matrix out loud, once**, from the notes in section 3. It sounds simple and it is surprisingly easy to fumble the first time in front of somebody. Twelve, thirteen-and-one, two-five-three.
- [ ] Print the whole Week 30 workbook. It has no page numbers, so a sticky note on **Practice Set A** (A2 and A3 are used in class) and on **Build It** (the homework) saves hunting.
- [ ] Read section 5 (leakage) twice. It is the part of the lesson most likely to go sideways, because the *symptom of the bug is a better result*.
- [ ] Check **THE GAP** is still on the board from Week 29. If it has been rubbed off, write it back: `0.9417 / 0.7333 / gap 0.2083`.

### 5 minutes on the day

- [ ] Laptop on, terminal open, an empty file ready. Delete or move any copy of the lab you made last night.
- [ ] Highlighter on the table.
- [ ] Board space under THE GAP for two new numbers: `0.7778 → 0.9444`.
- [ ] Run `why_scaling.py` once, now, to confirm the install and warm up the interpreter.

### Fallback if a laptop or an install fails

| If this fails | Do this instead |
|---|---|
| **No laptop today** | This week is more paper-friendly than it looks. Practice Set A, item A2 prints the two-column arithmetic (0.0001 vs 225.0000) — the most convincing thing in the lesson, and it is division. Practice Set A, item A3 prints both confusion matrices, and reading them aloud plus circling the worst row is objective 1 in full. The 25-row accuracy-vs-`k` table is printed in the Answer Key (Practice Set B, B5) and in the Activity section below, so you can hand it over, and the student can plot it **by hand on graph paper** — which is arguably better than `ax.plot`, because they have to think about the y-axis starting at zero. **Objectives 1, 2 and 4 are fully deliverable with no computer.** |
| **The chart will not save** | Print the numbers with the loop and plot them by hand on graph paper. Do not lose the lab to a matplotlib problem. |
| **The lab is too long for the time available** | Cut the `k` sweep from 1–25 to `[1, 5, 9, 15, 25]`. Five points still shows the shape and takes a fifth of the typing. |
| **Numbers don't match this guide** | Check `random_state=31` and `stratify=y`. Those two are what every printed number here depends on. |
| **The student read ahead and found pipelines** | Excellent, and be honest: *"You've found the better way to write it, and it's the way I'd use at work. We're doing it the long way on purpose, because the long way is the only way you can see where the leak gets in. Once you've seen that, you can use the short way forever."* Then let them write the pipeline version as an extension **after** the hand version works. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Two Numbers That Should Not Be in the Same Sum | 7 | 7 | 0.0001 against 225. On paper. |
| 🧠 Concept — Scale It, Then Read the Grid | 16 | 23 | The fix, `stratify`, and the confusion matrix out loud |
| 💻 Live-Code Together — 78% Becomes 94% | 18 | 41 | The jump, in front of them; two deliberate mistakes |
| 🎲 Their Turn — The Lab, and the Planted Bug | 20 | 61 | The `k` sweep and plot; then the leak, and the explanation |
| 🔑 Wrap & Assign | 9 | 70 | Three checks, the two numbers on the board, homework |

---

### 🪝 Hook — Two Numbers That Should Not Be in the Same Sum (7 minutes)

**Do this:** Laptop closed. Workbook **Practice Set A, item A2** in front of you both — it gives the `hue` and `proline` of the first two wines, and only those two columns.

**Say this:**

> "Two wines. I've printed just two of the thirteen columns.
>
> Wine 0: hue is 1.04, proline is 1065.
> Wine 1: hue is 1.05, proline is 1050.
>
> Now you're going to do exactly what you did in Week 28. Subtract, square, add up. Two columns, so two subtractions. Go on."

Let them do it with a pencil.

```
hue gap     :  1.04 − 1.05 = −0.01      squared:   0.0001
proline gap : 1065  − 1050  =  15       squared: 225.0000
total       :                            225.0001
```

> "Right. Now look at those two squared numbers, and tell me what's wrong with adding them together."

Let them see it. Most students spot it in under a minute, and it is much better if they say it.

> "Nought point nought nought nought one, plus two hundred and twenty five. Work out for me what percentage of that total came from the hue column."

Make them actually do the division. 0.0001 ÷ 225.0001 × 100.

> "**Forty-four millionths of one percent.** Say that again. The hue column contributed forty-four millionths of one percent of the distance between those two wines.
>
> So if I use this distance to decide which wines are similar — and that is exactly what our model does — then I'm not using thirteen measurements. I'm using **one**. The other twelve are decoration.
>
> And here's the bit that should annoy you. Is proline more important than hue?"

No. Nobody said that.

> "Nobody said that. Nobody decided that. It happened because somebody wrote proline in hundreds and hue in decimals. **Change proline from 1065 to 1.065 — same wine, same chemistry, just different units — and the whole thing flips.**
>
> Your model's opinion about wine should not depend on which unit a chemist happened to choose in 1991."

Write on the board:

> **A distance model can only be as fair as its units.**

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "What percentage of the distance came from hue?" | 0.000044%. Essentially nothing. | Make them do the division rather than eyeball it. Eyeballing it gives "small". The division gives *how* small, and the how is the point. |
| "Is proline more important than hue?" | No. It just has bigger numbers. | If they say yes, ask: "How would you know? What in that arithmetic told you anything about wine?" |
| "How would you fix it?" | Make the columns comparable somehow. Divide by something. | Any sensible idea earns credit. "Divide by the biggest value" is a real method (min-max scaling) — say so, and say we'll use a close cousin. |
| "Where have you seen units decide an answer before?" | Week 28 homework: measuring song length in seconds instead of minutes flipped which column mattered. | If they don't remember, remind them: bpm was 99.89% of the distance in minutes, and 20% of it in seconds. |

---

### 🧠 Concept — Scale It, Then Read the Grid (16 minutes)

**Say this — part 1, the fix:**

> "Here's the fix, and it's one idea. Right now a gap of 15 counts as huge because 15 is a big number. But is 15 big **for the proline column**? Proline runs from 278 to 1680. So 15 is nothing — it's a rounding error in proline terms.
>
> Meanwhile a gap of 0.01 in hue — is that small **for the hue column**? Hue only runs from 0.48 to 1.71. So 0.01 is small there too, but not *two-million-times* smaller (the ratio of the squares, 225 to 0.0001).
>
> So: **divide every gap by how much that column normally varies.** Then a gap counts as big when it's big *for its own column*."

Do it on the board with the real numbers:

```
hue     : gap 0.01  ÷  spread 0.2279   =  0.0439    squared: 0.0019
proline : gap 15    ÷  spread 314.02   =  0.0478    squared: 0.0023

hue's share    : 45.76 %
proline's share : 54.24 %
```

> "From forty-four millionths of a percent to **forty-six percent.** Nothing about the wines changed. We just stopped letting the units vote.
>
> That has a name — **feature scaling** — and the library does it for you."

Write both definitions up:

> **Feature scaling** — putting every column on the same footing before you measure distances.
> **Standardisation** — rescale each column so it has mean 0 and spread 1. Every number then means "how many spreads from typical am I?"

> "And one warning so it doesn't spook you: **half the scaled numbers will be negative.** Half of anything is below average, and below average is a negative number of spreads. That's correct, not broken."

**Say this — part 2, `stratify`:**

> "Second small thing, and it's one keyword. The wine table has 59, 71 and 48 of the three grape types — uneven. When `train_test_split` shuffles and cuts, it might hand you a lopsided test pile just by luck. Watch."

```text
whole table, class counts: [59 71 48]

NO stratify  -> test class counts: [ 9 18  9]
WITH stratify-> test class counts: [12 14 10]
```

> "Look at the middle line. Nine, eighteen, nine. Half the test pile is one grape type. So whatever I learn about how well the model handles the first grape, I've learnt it from **nine wines** — and each of those nine is worth eleven percentage points.
>
> `stratify=y` forces the shares to match. One keyword, and a whole category of bad luck disappears. Use it every single time you're predicting a category."

**Say this — part 3, the confusion matrix:**

> "Last idea, and it's the one I actually want you to take away, because it's the one that tells you what to *do* next.
>
> An accuracy is one number. One number can't tell you *where* you went wrong. So there's a grid."

Draw it on paper as you talk:

> "**Rows are the truth. Columns are the guess.** So the box in row 2, column 1 means: things that were really class 2 and got called class 1.
>
> The diagonal — row 0 column 0, row 1 column 1, row 2 column 2 — that's everything it got right. Everything off the diagonal is a **specific** mistake with a name.
>
> Here's the one our model is about to produce. Read it with me."

```
[[12  0  0]
 [ 0 13  1]
 [ 2  5  3]]
```

> "Row 0. Twelve wines really were class 0, and all twelve got called class 0. Perfect.
>
> Row 1. Fourteen were really class 1 — thirteen right, one called class 2. Nearly perfect.
>
> Row 2. Add it up: two plus five plus three, ten wines really were class 2. And how many got called class 2?"

**Three.**

> "Three out of ten. That is worse than flipping a coin. This model is essentially **blind to the third grape** — and the accuracy for the whole thing is seventy-eight percent, which sounds absolutely fine.
>
> **That's why you always print the grid.** One number tells you how much you got wrong. The grid tells you *what* you got wrong, and that's the thing you can act on."

> **💡 Try this:** cover the accuracy with your hand and show only row 2. Then uncover it. That is the whole argument for printing the grid, and it takes four seconds. **Figure 30.2** above is the same grid drawn out.

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Row 2 adds up to 10. What is that 10?" | The number of wines that really were class 2. | If they say "the guesses", point at the definition: rows are truth. Then ask what column 1 adds to *(18 — the number of times it said class 1)*. |
| "What does the diagonal mean?" | Everything it got right. | If unsure, walk the three diagonal cells and check each against the row and column labels. |
| "Accuracy is 78%. Is this model fine?" | No. It is blind to one of the three grapes. | If they say yes, cover the accuracy and show only row 2. Then uncover. |
| "Why does `stratify` take `y` and not `X`?" | Because you are balancing the *answers*, not the measurements. | `stratify=X` gives a very confusing error and it is in the Clinic — worth mentioning so they recognise it. |
| "Half the scaled numbers are negative. Is that wrong?" | No — half of everything is below average. | If it bothers them, do one by hand: (680 − 744.17) ÷ 307.03 = −0.21. |

---

### 💻 Live-Code Together — 78% Becomes 94% (18 minutes)

**Two chairs, one keyboard, and the student types.**

**Keystroke sequence — part 1, the raw model (6 minutes).**

New file, `wine_unscaled.py`.

```python
# wine_unscaled.py
# kNN on wine with the raw numbers. Then look at WHERE it went wrong.

import numpy as np
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

wine = load_wine()
X = wine.data
y = wine.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=31, stratify=y
)

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

print("train accuracy:", round(model.score(X_train, y_train), 4))
print("test  accuracy:", round(accuracy_score(y_test, predictions), 4))
print("test rows      :", len(y_test))
print()
print("confusion matrix (rows = truth, columns = guess):")
print(confusion_matrix(y_test, predictions))
```

Run it:

```text
train accuracy: 0.7817
test  accuracy: 0.7778
test rows      : 36

confusion matrix (rows = truth, columns = guess):
[[12  0  0]
 [ 0 13  1]
 [ 2  5  3]]
```

**Say this:**

> "Seventy-eight percent. Baseline was thirty-nine point nine, so it's genuinely learnt something — it's twice the baseline. And the two scores are close together, 0.7817 and 0.7778, which last week we said was the healthy shape.
>
> But now read me row 2."

Have them read it. **Then hand them the highlighter and have them circle row 2 on the screen printout or on the raw grid in **Practice Set A, item A3**.**

> "Circle it. That row is the model's confession."

**Keystroke sequence — part 2, ⚠️ DELIBERATE MISTAKE NUMBER ONE (4 minutes).**

New file, `wine_scaled.py`. Type the imports and the split, then type this — **deliberately missing the `fit`**:

```python
scaler = StandardScaler()
X_train_scaled = scaler.transform(X_train)
```

**Say this:**

> "I'm going to forget something on purpose. The scaler is a machine, and like every machine in this library it has to be **fitted** before it can do anything. I'm going to skip that line."

Run:

```text
  File "/Users/you/project/wine_scaled.py", line 17, in <module>
    X_train_scaled = scaler.transform(X_train)
  ...
sklearn.exceptions.NotFittedError: This StandardScaler instance is not fitted yet. Call 'fit' with appropriate arguments before using this estimator.
```

**Say this:**

> "`This StandardScaler instance is not fitted yet.` Same error you got last week when you called `predict` before `fit` — and that is genuinely useful to notice. **Everything in this library follows the same pattern: make it, fit it, then use it.** A scaler is not a model, but it obeys the same three steps, which means one habit covers both.
>
> And what would it even do without fitting? Subtract *what* mean? It doesn't know any means yet."

Fix it, and complete the file:

```python
# wine_scaled.py
# The same thing, but every column put on the same scale first.

import numpy as np
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix

wine = load_wine()
X = wine.data
y = wine.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=31, stratify=y
)

scaler = StandardScaler()                # the machine that rescales columns
scaler.fit(X_train)                      # LEARN the means and spreads: TRAIN ONLY
X_train_scaled = scaler.transform(X_train)   # apply them to the training rows
X_test_scaled = scaler.transform(X_test)     # apply the SAME ones to the test rows

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train_scaled, y_train)
predictions = model.predict(X_test_scaled)

print("train accuracy:", round(model.score(X_train_scaled, y_train), 4))
print("test  accuracy:", round(accuracy_score(y_test, predictions), 4))
print("test rows      :", len(y_test))
print()
print("confusion matrix (rows = truth, columns = guess):")
print(confusion_matrix(y_test, predictions))
print()
print("proline column BEFORE scaling, first 5:", np.round(X_train[:5, 12], 2))
print("proline column AFTER  scaling, first 5:", np.round(X_train_scaled[:5, 12], 2))
```

**Before running: have them predict the new accuracy and write it down.** Then run:

```text
train accuracy: 0.9859
test  accuracy: 0.9444
test rows      : 36

confusion matrix (rows = truth, columns = guess):
[[12  0  0]
 [ 1 12  1]
 [ 0  0 10]]

proline column BEFORE scaling, first 5: [ 680.  450.  615.  415. 1280.]
proline column AFTER  scaling, first 5: [-0.21 -0.96 -0.42 -1.07  1.75]
```

**Say this, slowly:**

> "Point seven seven seven eight, to point nine four four four.
>
> **Sixteen and two-thirds percentage points.** We added no measurements. We collected no new wines. We didn't touch `k`. We changed no data — those are the same 178 wines. All we did was stop letting proline shout over the other twelve.
>
> And now read me the new row 2."

**Twelve zero zero / one twelve one / zero zero ten.** Row 2: all ten class-2 wines correct.

> "**Ten out of ten.** The grape it was blind to, it now gets perfectly. Errors went from eight wines wrong to two. And look at the two mistakes it has left — both in row 1, one wine called class 0 and one called class 2. It's now making the kind of mistake a person would make: getting confused at the edges.
>
> Look at the last two lines too. Six hundred and eighty became minus nought point two one. That's not a smaller number for the sake of it — it *means* something. It means 'a bit below typical'. And twelve eighty became one point seven five: 'nearly two spreads above typical'. **That's a much more useful thing to know about a wine than 1280.**"

**Do this:** write on the board, under THE GAP from last week:

```
  WINE, k = 5      raw columns      0.7778   on 36 rows
                   scaled columns   0.9444   on 36 rows
                   ----------------------------------
                   free, for one habit:  +16.7 points
```

**Keystroke sequence — part 3, ⚠️ DELIBERATE MISTAKE NUMBER TWO — the silent one (5 minutes).**

**Say this:**

> "Now the worst kind of bug there is. Not the kind that crashes. The kind that doesn't."

Change the predict line to use the **unscaled** test rows:

```python
predictions = model.predict(X_test)          # forgot to scale the test rows
```

Run it. **No error at all:**

```text
train accuracy: 0.9859
test  accuracy: 0.3333
test rows      : 36
```

**Say this:**

> "Nothing crashed. It ran perfectly. And the accuracy is thirty-three percent — which is *below* the baseline of thirty-nine point nine. Our beautiful ninety-four percent model just became worse than shouting one word at every wine.
>
> Why? Because the model learnt in scaled world, where proline lives between about minus two and plus two. Then I handed it a test wine with proline of 680. To the model, 680 is six hundred and eighty spreads from typical — a wine from a different planet. Every single test wine looks equally absurd, so the distances are meaningless.
>
> **And there was no error message.** Python had no way to know: 680 is a perfectly valid number. This is the bug you must catch yourself, and the way you catch it is a habit: **whatever you did to `X_train`, do to `X_test`.** Same two lines, every time, right next to each other."

Fix it back to `X_test_scaled`. Confirm 0.9444 returns.

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "What did we change to gain 16.7 points?" | Nothing about the data or the model — only the scale of the columns. | If they say "we made it better", push: "Better how? Name the thing we added." Nothing was added. |
| "Read me row 2 of the new grid." | 0, 0, 10 — all ten class-2 wines correct. | If they read a column, point at the row/column labels again. Truth is rows. |
| "Why didn't the unscaled-test-rows bug crash?" | 680 is a valid number. Python cannot know it is in the wrong units. | If they think it should have crashed, ask: "What would Python have to know to spot that?" It would have to understand units, which it does not. |
| "33% versus the baseline of 39.9% — what does that tell you?" | The model is now worse than not looking at the wine at all. | This is Level 1's baseline lesson doing real work. Credit it out loud. |
| "What's the habit that prevents it?" | Whatever you do to `X_train`, do to `X_test`. Both lines together. | Write it on the board next to the numbers. |

---

### 🎲 Their Turn — The Lab, and the Planted Bug (20 minutes)

Full instructions in the next section. In the lesson flow:

- **Minutes 0–10:** the `k` sweep from 1 to 25, printed and plotted, PNG saved.
- **Minutes 10–14:** choose a `k`, and write the three sentences plus the honesty sentence.
- **Minutes 14–20:** the planted bug. Fit the scaler on everything. The score goes up. Explain why that is the bad news.

---

## 🐞 The Debugging Clinic

Every message below came from a real run of a deliberately broken version of this week's code. Long library-internal sections are trimmed with `...`.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `sklearn.exceptions.NotFittedError: This StandardScaler instance is not fitted yet. Call 'fit' with appropriate arguments before using this estimator.` | "You asked me to rescale before telling me what the columns look like." | The `scaler.fit(X_train)` line is missing. | Add it, above the `transform`. Make it, fit it, use it — same three steps as a model. |
| `ImportError: cannot import name 'StandardScalar' from 'sklearn.preprocessing'` | "Nothing in that room has that name." | American spelling: it is `Scaler`, not `Scalar`. | `StandardScaler`. (A *scalar* is a single number — a different word entirely.) |
| `sklearn.utils._param_validation.InvalidParameterError: The 'y_pred' parameter of accuracy_score must be an array-like or a sparse matrix. Got KNeighborsClassifier() instead.` | "You handed me the model where the guesses should be." | `accuracy_score(y_test, model)` instead of `accuracy_score(y_test, model.predict(X_test))`. | Pass the predictions, not the model. |
| `TypeError: missing a required argument: 'y_pred'` | "I need two things and you gave me one." | `confusion_matrix(model.predict(X_test))` — the truth was left out. | `confusion_matrix(y_test, predictions)`. **Truth first, guesses second.** |
| `ValueError: Found input variables with inconsistent numbers of samples: [4, 5]` | "You gave me 4 truths and 5 guesses. Which one has no partner?" | Predictions and `y_test` came from different splits, or the wrong variable got passed. | Print `len(y_test)` and `len(predictions)` and make them match. |
| `ValueError: The least populated class in y has only 1 member, which is too few. The minimum number of groups for any class cannot be less than 2.` | "You asked me to keep the class shares even, but one of your 'classes' only happens once." | `stratify=X` instead of `stratify=y`. Sklearn treated whole feature rows as class labels, and every row is unique. | `stratify=y`. You stratify on the **answers**. |
| **No error at all**, and the accuracy is 0.3333 — below the baseline | Nothing crashed. The model was trained on scaled numbers and tested on raw ones. | `model.predict(X_test)` instead of `model.predict(X_test_scaled)`. | Use the scaled test rows. **Habit: whatever you do to `X_train`, do to `X_test`, on the very next line.** |
| **No error at all**, and every number differs from the guide | Nothing is broken; the deck was cut somewhere else. | `random_state` missing, or set to 42 instead of 31, or `stratify=y` left off. | Match all three: `test_size=0.2, random_state=31, stratify=y`. |
| **No error at all**, and the leaky version scores *higher* | Also nothing crashed. That is precisely why leakage is dangerous. | `scaler.fit(X)` before the split, instead of `scaler.fit(X_train)` after it. | `fit` on `X_train`, after the split, always. |

### How to teach debugging without giving the answer

This week adds a rung at the *bottom* of the ladder, and it is the important one:

**−1. "Is there an error at all?"** Three of the nine entries above have no error message. Two of the three produce a *worse* score and one produces a *better* one. So the first question of this week is not "what does the error say" but **"is this number plausible?"** — and the way you answer it is the baseline. If your accuracy is below the baseline, something is broken even though nothing complained. If it went up when you did not add anything, something leaked.

Then the usual ladder:

0. **Find the line with your own filename in it.**
1. **"Read me the last line."**
2. **"What was it expecting, and what did it get?"** Sklearn names both. `[4, 5]` is the whole bug.
3. **"What did you change since it last worked?"**
4. **Point at the line. Say nothing.**
5. **Point at the character.**
6. **Tell them, and name the family:** "that's a fit-before-use one", "that's a truth-first one", "that's a did-you-do-it-to-both one".

> **🧑‍🏫 If a student asks:** *"How am I supposed to find a bug with no error message?"* — Honest answer: you compare the number to something you decided in advance. That is what the baseline is for, and it is why this course makes you write it down *before* you train anything. Professionals do exactly this and call it a sanity check: before you look at a result, decide roughly what a believable result looks like. **A number you cannot sanity-check is not a result.**

---

## 🎲 The Activity, In Full

### The Classifier Lab, and the Bug That Improves Your Score

### Setup

**On the table:** workbook **Practice Set B (B5)** and **Build It** (Pieces 1 to 6), a calculator, a highlighter, graph paper as backup, the laptop with the editor open.

**On the board:** THE GAP from Week 29, and this week's `0.7778 → 0.9444` written under it.

### Part 1 — Sweep `k` and plot it (10 minutes)

**Do this:** The student adds to `wine_scaled.py`, or starts `wine_choose_k.py`. Dictate:

```python
# wine_choose_k.py
# Try every k from 1 to 25, twice: raw columns and scaled columns. Then plot it.

import matplotlib
matplotlib.use("Agg")                    # save to a file instead of a window
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

wine = load_wine()
X = wine.data
y = wine.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=31, stratify=y
)

scaler = StandardScaler()
scaler.fit(X_train)                      # train rows only. Always.
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

ks = []                                  # the k values we tried
raw_scores = []                          # scores with the raw columns
scaled_scores = []                       # scores with the scaled columns

for k in range(1, 26):                   # k = 1, 2, 3 ... 25
    ks.append(k)

    raw_model = KNeighborsClassifier(n_neighbors=k)
    raw_model.fit(X_train, y_train)
    raw_scores.append(raw_model.score(X_test, y_test))

    scaled_model = KNeighborsClassifier(n_neighbors=k)
    scaled_model.fit(X_train_scaled, y_train)
    scaled_scores.append(scaled_model.score(X_test_scaled, y_test))

    print(f"k = {k:2d}   raw = {raw_scores[-1]:.4f}   scaled = {scaled_scores[-1]:.4f}")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(ks, scaled_scores, marker="o", label="scaled columns")
ax.plot(ks, raw_scores, marker="s", label="raw columns")
ax.set_title("Scaling is worth about 17 accuracy points on the wine table")
ax.set_xlabel("k (how many neighbours vote)")
ax.set_ylabel("accuracy on the 36 held-back wines")
ax.set_ylim(0, 1.05)                     # start the axis at zero. Week 27's rule.
ax.legend()
fig.savefig("wine_accuracy_vs_k.png", dpi=120, bbox_inches="tight")
print()
print("saved wine_accuracy_vs_k.png")
```

> **⚠️ Watch out:** `matplotlib.use("Agg")` must come **before** `import matplotlib.pyplot as plt`. It tells matplotlib to draw straight to a file instead of trying to open a window, which is what you want on a machine where a window may not appear.

Real output, all 25 lines:

```text
k =  1   raw = 0.7500   scaled = 0.9167
k =  2   raw = 0.7778   scaled = 0.9167
k =  3   raw = 0.7778   scaled = 0.9167
k =  4   raw = 0.7778   scaled = 0.9167
k =  5   raw = 0.7778   scaled = 0.9444
k =  6   raw = 0.7500   scaled = 0.9167
k =  7   raw = 0.7222   scaled = 0.9722
k =  8   raw = 0.7222   scaled = 0.9722
k =  9   raw = 0.7778   scaled = 0.9722
k = 10   raw = 0.7500   scaled = 0.9722
k = 11   raw = 0.7500   scaled = 0.9444
k = 12   raw = 0.7778   scaled = 0.9167
k = 13   raw = 0.7500   scaled = 0.9444
k = 14   raw = 0.7778   scaled = 0.9444
k = 15   raw = 0.7500   scaled = 0.9444
k = 16   raw = 0.7500   scaled = 0.9444
k = 17   raw = 0.7778   scaled = 0.9444
k = 18   raw = 0.7778   scaled = 0.9722
k = 19   raw = 0.7500   scaled = 0.9444
k = 20   raw = 0.7778   scaled = 0.9444
k = 21   raw = 0.7778   scaled = 0.9444
k = 22   raw = 0.7778   scaled = 0.9722
k = 23   raw = 0.7778   scaled = 0.9722
k = 24   raw = 0.7500   scaled = 0.9722
k = 25   raw = 0.7500   scaled = 0.9722

saved wine_accuracy_vs_k.png
```

**Open the PNG and look at it together.** Two things to say:

> "First: **the round line is above the square line at every single k.** Not most. All twenty-five. Scaling isn't a tweak on this table, it's the difference between a model you'd use and one you wouldn't.
>
> Second: look how **jumpy** both lines are. Nine-one-six-seven, nine-one-six-seven, nine-four-four-four, nine-one-six-seven... it's bouncing around. And it should, because there are only 36 test wines, so one wine is 2.8 percentage points. Most of that wiggle is one wine changing its mind."

![Scaling is worth about 17 accuracy points](../figures/fig-w30-3-accuracy-versus-k-curve.svg)
*Figure 30.5 — The pink band is the plateau at `k = 7, 8, 9, 10`. Pick from inside a flat region, not from a lonely spike.*

### Part 2 — Choose a `k`, in writing (4 minutes)

**Say this:**

> "Now pick a k, and you have to defend it. And the way you defend it is **not** 'it had the highest score', because look — nine seven two two happens at k equals 7, 8, 9, 10, and again at 18, and again at 22 to 25. Which of those do you want?
>
> Here's the rule. **Look for a flat patch, not a spike.** A flat patch means the answer doesn't depend on getting k exactly right — you could be a bit wrong about k and still be fine. A lonely spike, with dips either side, is usually one lucky wine.
>
> Seven, eight, nine, ten. Four in a row, all at nine seven two two. That's a plateau, and it's the first one. Inside it, prefer a **bigger** k, because bigger k is less jumpy. And prefer an **odd** k, because odd ties less often.
>
> So: **nine.**"

**Do this:** have the student write these on the **Build It, Piece 3** lines (and the honesty sentence on Piece 4), in ink:

```
chosen k          : 9
test accuracy     : 0.9722, on 36 held-back wines
baseline          : 0.3989
reason            : k = 7, 8, 9 and 10 all give 0.9722. Four in a row is a
                    plateau, so the answer does not depend on getting k
                    exactly right. I chose 9 because a bigger k is steadier
                    and an odd k ties less often.
honesty sentence  : I chose this k by looking at test scores, which makes
                    this estimate slightly optimistic.
```

**Say this about that last line:**

> "I want that sentence written every single time, all year. You looked at the test set twenty-five times to pick a k. Which means the test set helped you decide something — and something that helps you decide has taught you. So your ninety-seven point two is a bit flattering, and you don't know exactly how much.
>
> There's a proper fix and it's next year's problem. This year, the fix is **saying so.** Writing down a limitation you know about is worth more than the model is. Anybody can produce a number. Not everybody tells you what's wrong with it."

### Part 3 — The planted bug (6 minutes)

**Do this:** New file, `wine_leak.py`. Dictate it. **Tell them there is a bug in it and let them look at it before running.**

```python
# wine_leak.py
# THE PLANTED BUG. The scaler is fitted on ALL the data, before the split.

import numpy as np
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

wine = load_wine()
X = wine.data
y = wine.target

# ---- THE BUG: scale everything first, split afterwards ------------------
scaler = StandardScaler()
scaler.fit(X)                            # <-- ALL 178 wines, test rows included
X_all_scaled = scaler.transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_all_scaled, y, test_size=0.2, random_state=31, stratify=y
)

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

print("LEAKY test accuracy:", round(accuracy_score(y_test, predictions), 4))
print("that is", int(accuracy_score(y_test, predictions) * 36), "of 36 wines right")
print()

# ---- Show the two scalers learned DIFFERENT numbers ---------------------
train_only, _, _, _ = train_test_split(
    X, y, test_size=0.2, random_state=31, stratify=y
)
clean_scaler = StandardScaler().fit(train_only)

print("proline mean learned from ALL 178 wines:", round(scaler.mean_[12], 2))
print("proline mean learned from the 142 train:", round(clean_scaler.mean_[12], 2))
print("difference:", round(scaler.mean_[12] - clean_scaler.mean_[12], 2))
```

**Before running, ask: "will the score go up, down, or stay the same?"** Let them commit to an answer out loud.

```text
LEAKY test accuracy: 0.9722
that is 35 of 36 wines right

proline mean learned from ALL 178 wines: 746.89
proline mean learned from the 142 train: 744.17
difference: 2.72
```

**Say this, and then be quiet:**

> "It went **up**. Nine four four four to nine seven two two. Thirty-four wines right became thirty-five.
>
> So. I introduced a bug, and my score improved. Tell me why that's bad news."

**Wait.** Do not rescue them. This is the hardest question of the term so far and it is worth ninety seconds of silence. Prompts, in order, only if needed:

1. *"What is that number supposed to be telling you?"*
2. *"Would that number still be true tomorrow, when a brand-new wine arrives?"*
3. *"When the new wine arrives, could it have helped work out the mean?"*

**The answer you want, in their words:**

> The score is supposed to be an estimate of how the model does on wines nobody has seen. But the test wines helped work out the means and spreads that the training data got scaled with — so they weren't unseen. A brand-new wine tomorrow can't have helped, so expect tomorrow's wine to do worse than 0.9722. The number went up and got *less* true.

**Say this to close it:**

> "**You didn't make the model better. You made the exam easier and forgot to say so.**
>
> And look at the size of it — the proline mean shifted by two point seven two, out of seven hundred and forty-four. That's a **third of one percent.** A tiny, tiny leak, and it bought a whole extra wine.
>
> One more honest thing, and it's the reason we care so much about the habit. If I change `random_state` from 31 to 42, the leaky version and the clean version come out **exactly the same**. The leak changes nothing at all on that split. Which sounds like good news and is the opposite: **it means you can't tell by looking.** You can't run it both ways and check, because sometimes the leak is invisible. All you can do is have the habit: **split first, fit the scaler on the training rows, always.**"

### What "finished" looks like

- `wine_accuracy_vs_k.png` saved, opened, with two labelled lines, a legend, both axis labels and a y-axis starting at 0.
- A comparison table in **Build It, Piece 2** with **train and test** accuracy for both models.
- The baseline `0.3989` written down, and both test accuracies compared to it.
- A chosen `k`, with three sentences of reason and the honesty sentence, in ink.
- Both confusion matrices written out, with the worst row of each highlighted.
- The student able to say, unprompted, why the leaky 0.9722 is worse than the honest 0.9444.

### Variation — easier

- **Cut the sweep to five values of `k`:** `for k in [1, 5, 9, 15, 25]`. Five points show the shape and are a fifth of the waiting.
- **Skip the plot; plot it by hand** on graph paper from the printed numbers. This is arguably better — they have to choose the axis range themselves, which is Week 27's whole lesson doing real work.
- **Skip Part 3.** The scaled/unscaled jump plus a confusion matrix read aloud is a complete, satisfying lab and hits objectives 1, 2, 3 and 5.
- **Give them `wine_scaled.py` already typed** and have them change only `n_neighbors`, predicting the result each time. Reading and editing working code is a real skill.
- **The one thing you must not cut:** reading a confusion matrix out loud, row by row, and naming the worst row. That is the transferable skill of the week.

### Variation — harder

1. **Add a third line to the plot: training accuracy.** Plot train and test accuracy for the scaled model on the same axes. At `k = 1` the training line is pinned at exactly 1.0 while the test line sits at 0.9167. **Predict, before plotting, what happens to the gap as `k` grows.** *(It shrinks. Bigger committees memorise less. The gap between those two lines has a name and Week 33 is entirely about it.)*
2. **Which single column does the most work?** Train the scaled model thirteen times, each time leaving one column out, and see which removal hurts most. This needs only `np.delete(X, i, axis=1)` and a loop — everything else they have.
3. **Does the leak matter on other splits?** Run the clean and leaky versions for `random_state` 0 to 9 and count how often they differ. *(They differ on some seeds and not others. The paragraph to write: "identical scores are luck, not proof of safety.")*
4. **A different dataset.** `load_breast_cancer()` — 569 rows, 30 columns, 2 classes. Run the whole lab on it. **Predict first whether scaling will help as much as it did on wine, and say why.** *(It helps, and by less, because the columns are less wildly different in size. Both are worth measuring rather than guessing.)*
5. **Find the two wines the k=9 model still gets wrong**, print their thirteen measurements, and say something honest about them. *(Only one wine is wrong at k=9: a class-1 wine called class 2. It sits near the boundary, and looking at the numbers you would not be confident either.)*
6. **The pipeline, as a reward.** Once the hand version works: `make_pipeline(StandardScaler(), KNeighborsClassifier(9))` does all of it in one leak-proof line. Show them, let them check it gives the same 0.9722, and say honestly that this is how it is done at work — **and that they can only appreciate why it exists because they built the leak by hand first.**

---

## ❓ Questions Students Ask This Week

**"If scaling is always better, why doesn't the library just do it automatically?"**

Because it is not always better, and a library that silently changed your data would be a nightmare to debug. Two real cases where you should not scale. **Iris:** all four columns are centimetres on similar ranges, and standardising it actually makes kNN slightly *worse*, because petal measurements naturally vary more than sepal ones and that extra variation is genuine information — forcing every column to spread 1 throws it away. **Decision trees** (Week 31) do not measure distance at all; they ask "is this column above 2.5?", and scaling changes the threshold but never the answer, so it is pure waste. **The rule that survives both cases:** scale when your columns live on wildly different scales or in different units, and check rather than assume.

**"How do I know the spread it divides by is the right thing to divide by?"**

You do not, exactly — it is a choice, and a good default rather than a law. Standardisation divides by the standard deviation, which asks "how unusual is this gap, for this column?" An alternative, min-max scaling, divides by the range (max − min) and squashes everything into 0-to-1; it is more sensitive to a single freak value, because one outlier stretches the range. There are others. **Which to use is a judgement about your data, and reasonable people pick differently.** What everybody agrees on is that leaving thirteen columns on wildly different scales and then measuring distances between them is not a judgement, it is an oversight.

**"Why is the confusion matrix rows-are-truth and not the other way round?"**

Pure convention, and it is worth knowing that it *is* only convention, because some textbooks and some software do it the other way. What protects you is not memorising it but checking: **add up a row.** If the row totals match how many of that class actually exist in your test set, rows are truth. In our wine test set the classes are 12, 14 and 10, and the rows add to 12, 14 and 10 — so rows are truth. **Never read a confusion matrix you have not checked this way**, because reading it transposed means naming every mistake backwards, and the accuracy looks identical either way so nothing warns you.

**"You picked `random_state=31` for this week and 42 last week. Did you pick 31 because it made your point?"** *(Answer this one completely honestly. It is the best question a student can ask this term.)*

**Yes. I did, and you have caught something real.** I tried several seeds and chose one where the leaky version scored higher than the clean version, because I wanted you to see that happen. On `random_state=42` the leak makes no difference at all and you would have gone away thinking leaks are harmless.

Now — is that dishonest? **Partly.** For *teaching*, choosing a clear example is fine and normal, as long as you say so, which is what I am doing now. What would be genuinely dishonest is doing the same thing to make a *result* look good: running twenty seeds, publishing the best one, and calling it your model's accuracy. That has a name — people call it seed-shopping or, less politely, p-hacking — and it happens in real published research more than anybody would like. **The line is whether you tell people what you did.** I chose 31 and I have written it in the file. Somebody who chooses their best seed and quietly reports it as if it were the only one they tried has crossed the line. Now go and ask me the follow-up: *how would you catch somebody doing it?* *(You would ask them to run it on a fresh split they had never seen. That is genuinely how it gets caught.)*

**"Our model gets one grape type badly wrong. Whose problem is that?"** *(Worth taking seriously.)*

It depends entirely on what the model is for, and that makes it an ethics question rather than a maths one. On wine it does not matter much. Now imagine the same confusion matrix where class 0 is "healthy", class 1 is "mild condition" and class 2 is "serious condition". Our unscaled model was **perfect on healthy people and got 3 out of 10 serious cases** — 78% accurate overall, and every single one of its mistakes landed on the people who needed it most. A model at 90% with errors spread evenly would be far safer. So: report the grid, never just the number, because the number can hide exactly this. And then the harder question, which nobody has a clean answer to: who decides which mistakes are acceptable — the person who builds the model, or the person the mistake lands on? Level 1 asked you this about bias, and it is the same question in different clothes.

**"Can I just try lots of things and keep whatever scores best?"**

You can, and you will, and everybody does — but each time you do it your test score gets a little more optimistic and you cannot measure by how much. You tried 25 values of `k` today, which is 25 peeks. The honest response is the sentence you wrote: *I chose this k by looking at test scores, which makes this estimate slightly optimistic.* The professional response is a third pile of data — a **validation set** — that you tune against, keeping the test envelope genuinely sealed until the very end. That costs rows, and with 178 wines you cannot really afford it, which is exactly why Level 2 stops at the honesty sentence and Level 3 teaches cross-validation.

**"Is 94% good?"**

You cannot answer that without three more things, and asking for them is the skill. **What's the baseline?** 39.89%, so 94% is genuinely far better than guessing. **How many test rows?** Thirty-six — so one wine is 2.8 percentage points, and the difference between 94.4% and 97.2% is *one wine*. Do not build an argument on one wine. **And where are the errors?** Two wines, both in row 1, one called class 0 and one called class 2 — mistakes at the boundary, which is the forgivable kind. With all three of those, 94% is a good honest result for a small dataset. On its own, "94%" is not information.

**"Why does `transform` give back a new array instead of just changing `X_train`?"**

Because a machine that quietly rewrites your data is a machine you cannot debug. If `transform` edited `X_train` in place, you could never print the before-and-after side by side, you could never re-run one cell of your file safely, and you would have no way of noticing when something got scaled twice — which, by the way, produces no error and a silently broken model. Handing back a copy is the same design decision as `sorted()` in Week 12: **the tools that leave your original alone are the ones you can trust.**

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| The 0.3333 bug (test rows not scaled) goes unnoticed | There is no error message, and 0.3333 looks like a number | **The baseline is the defence.** Insist it is written down before any model is trained. Then the rule: any accuracy below the baseline means something is broken, regardless of whether Python complained. |
| The leaky higher score is taken as an improvement | It is a higher number, and higher numbers have meant better all year | Do not explain it. Ask the three prompt questions in Part 3, in order, and wait. If they still cannot get there, ask the one that always works: *"Tomorrow a brand-new wine arrives. Could it have helped work out the mean?"* |
| Confusion matrix read column-wise | Nothing in the printed grid says which is which | Teach the check, not the convention: **add up a row and see if it matches the real class counts.** Do it once together, out loud, and they will have it for life. |
| The chosen `k` is defended as "it had the highest score" | It is the obvious criterion | Show them that 0.9722 happens at nine different values of `k`. Then: "So which one, and why?" The question answers itself and the plateau idea lands. |
| The honesty sentence gets skipped as pointless | It feels like admin | Make it a hard requirement for a complete lab, alongside the chart. Say why once, properly: *"Anybody can produce a number. Being trusted comes from saying what's wrong with it."* |
| Numbers don't match this guide and confidence collapses | `random_state` is 42, or `stratify` was left off | Check those two first, always, before anything else. Then say: "Nothing was wrong with your code — you cut the deck somewhere else." |
| The scaled numbers being negative causes alarm | They look like broken data | One worked example fixes it: (680 − 744.17) ÷ 307.03 = −0.21. Below average is a negative number of spreads. Nothing is broken. |
| Ten minutes vanish into what standard deviation *is* | It is a real gap and it is a fair question | Do not teach it. One sentence: *"how much a column normally wobbles — big for a column that varies a lot, small for one that barely moves."* That is enough to use it. The formula is a maths lesson, not this lesson. |
| The plot has no axis labels or a y-axis starting at 0.9 | Speed, and matplotlib's defaults | Week 25's and Week 27's rules are not optional and this is where you enforce them. A y-axis starting at 0.9 turns a 3-point difference into a cliff. Make them fix it and look at both versions. |
| The student wants to fix row 2 by "telling it to try harder on class 2" | Reasonable instinct, wrong lever | Be honest: there is no such setting in what we know. The levers we have are better features and better scaling — and scaling already fixed it completely, from 3/10 to 10/10. Point at that. |
| `make_pipeline` appears from the internet | It is in every tutorial | Welcome it, and hold the line: *"That's the better way and it's how I'd write it at work. We're doing it long-hand for one more year, because long-hand is the only way to see where the leak gets in. Write the pipeline version as an extension once yours works."* |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** Part 3, the planted bug. The scaled/unscaled jump and a confusion matrix read aloud is a complete lab and delivers four of the five objectives.

**Cut:** the 25-value sweep. Use `[1, 5, 9, 15, 25]`.

**Reteach scaling with two rulers.** Get a 30 cm ruler and a tape measure. Measure the same object twice: 21 cm, and 210 mm. Then: *"Is the second one ten times bigger?"* No. *"So if I put 21 in one column and 210 in another, and squared the difference, which would shout?"* This physical version of "same thing, different units" lands where the wine arithmetic sometimes does not.

**Reteach the confusion matrix with counters.** Lay out 36 counters in three labelled rows — 12, 14, 10 — for the three real classes. Then physically move the wrong ones into the column they got called. The student *sees* five counters walk out of row 2 into column 1. Then have them write down the grid from the counters. It is slow and it works.

**Copy-this-exactly scaffold.** Every line correct, every output written in as a comment:

```python
# my_scaled_model.py
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix

wine = load_wine()
X = wine.data
y = wine.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=31, stratify=y
)
print(X_train.shape)        # you should see (142, 13)
print(len(y_test))          # you should see 36

scaler = StandardScaler()
scaler.fit(X_train)                             # train rows only
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)        # same two lines, always together

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train_scaled, y_train)
predictions = model.predict(X_test_scaled)

print(round(accuracy_score(y_test, predictions), 4))   # you should see 0.9444
print(confusion_matrix(y_test, predictions))
# you should see
# [[12  0  0]
#  [ 1 12  1]
#  [ 0  0 10]]
```

They fix the first line whose output disagrees and no others.

**The one thing you must not cut:** reading a confusion matrix out loud and naming the worst row. It is the most transferable thing in the week and it needs no code at all.

### If the student is flying

1. **The third line on the plot** (Variation — harder, item 1), with the prediction about the gap written down first.
2. **Leave-one-column-out** (item 2). Thirteen models, ranked by how much the removal hurt.
3. **Does the leak matter on other splits?** (item 3), ending in the written paragraph. This is the deepest idea available to them this year.
4. **The whole lab on `load_breast_cancer()`** (item 4), with the prediction made first.
5. **Find the wine it still gets wrong** (item 5) and write two honest sentences about it.
6. **The pipeline** (item 6) — but only after the hand version runs, and only framed as a reward for having built the leak by hand.
7. **The hardest written question of the term:** *"Your friend says their model is 99% accurate. Write me the five questions you would ask before believing it."* Good answers: what's the baseline · how many test rows · was the test set held back before you started · where are the errors, by class · how many things did you try before picking this one.

### If the student won't engage today

Do the Hook only — the two-column arithmetic — and then play **"Spot the Shouty Column."**

You name two measurements and the units, and they say which one will drown the other and roughly by how much. No code, no writing, keep score.

> Height in millimetres vs age in years *(height, by a mile)* · Height in metres vs age in years *(age now)* · Salary in rupees vs years of experience *(salary, enormously)* · Exam mark out of 100 vs hours revised *(mark, by about 10× before squaring, 100× after)* · Exam mark out of 100 vs revision minutes *(minutes now — 600 minutes beats 60 marks)* · Temperature in °C vs rainfall in mm *(rainfall, usually)* · Steps per day vs hours of sleep *(steps, by thousands)* · Price in pence vs price in pounds, in the same table *(pence, 100×, and having both is a bug)* · Followers vs posts *(followers, usually thousands to hundreds)* · Distance in km vs rating out of 5 *(depends on the distances — a genuinely arguable one, and the right answer is "measure it")*

That game delivers objective 2 completely, takes twelve minutes, and needs nothing but talking. The lab survives to next lesson; the code is saved and Week 31 opens on a different model anyway.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — read the grid (spoken, grid in front of them)**

> "Here's a confusion matrix for three classes: row 0 is `[8, 1, 1]`, row 1 is `[0, 9, 3]`, row 2 is `[0, 0, 8]`. Which row is the worst, and say the mistake out loud in a full sentence."

*Good answer:* **Row 1 is the worst.** Twelve things really were class 1; nine were called class 1 and **three were called class 2**. The sentence should have the shape *"three things that were really class 1 got called class 2."* **What to catch:** reading columns as truths (they will say row 2 is worst because column 2 has a 3 in it), or naming the mistake with no direction — "class 1 and class 2 got mixed up" is not precise enough. Ask "which way round?"

**Check 2 — why scale (spoken)**

> "One column is a price in rupees, in the thousands. Another is a rating out of five. Why does that break a distance model, and what do you do about it?"

*Good answer:* A gap of 2000 rupees squares to 4,000,000 while a gap of 2 rating points squares to 4, so price contributes essentially all of the distance and rating is ignored — **not because price matters more, but because it is written in bigger numbers.** The fix is to divide each gap by how much that column normally varies, so a gap counts as big when it is big for its own column. Full marks needs **the squaring mentioned** — that is what makes it a wipe-out rather than a lean.

**Check 3 — fit on what (written, 60 seconds)**

> "Write down which rows the scaler is allowed to learn its means and spreads from, and write down one sentence saying what goes wrong if you use all of them."

*Good answer:* The **training rows only**, and only after the split. If you use all of them, the test rows have helped prepare the training data, so they are no longer unseen — and your score becomes a slightly optimistic number about a situation that will never happen again, because a genuinely new row cannot have contributed to your means. **What to catch:** "because it's cheating" with no mechanism. Push once: *"Cheating how? What exactly did the model find out that it shouldn't have?"*

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot read a confusion matrix. Thinks scaling is a tidying-up step. Reports an accuracy with no baseline and no row count. |
| **2 — Emerging** | Reads the diagonal but not the off-diagonal cells. Copies the scaler lines correctly from a model but cannot say why `fit` is separate from `transform`. Picks the `k` with the highest score, with no reason given. |
| **3 — Secure** | Reads a confusion matrix row by row and names the worst row with a directional sentence. Scales by fitting on the training rows only and says why. Plots accuracy against `k`, picks one from a plateau, and writes the reason and the honesty sentence. Uses `stratify=y`. **This is the target.** |
| **4 — Strong** | Explains the drowning effect using the *squares*, not just "bigger numbers". Spots the 0.3333 bug from the baseline alone, with no error message to help. Explains why a leak that raises the score is worse news than one that lowers it. |
| **5 — Exceptional** | Works out unprompted that a leak which changes nothing on one split is still dangerous, because you cannot tell in advance. Argues that a 78% model that is blind to one class may be worse than a 90% model with errors spread evenly, and can say who that depends on. Recognises that choosing `k` from test scores has spent some of the test set's honesty, and can describe what a third pile of data would be for. |

---

## 📤 Homework to Assign

**Say this:**

> "Finish the lab, and hand in five things. About an hour.
>
> **One — the chart.** `wine_accuracy_vs_k.png`, k from 1 to 25, both lines, a legend, both axis labels with units, and the y-axis starting at **zero**. If your y-axis starts at 0.9, that's a Week 27 lie and I'll send it back.
>
> **Two — the comparison table.** Four columns: model, train accuracy, test accuracy, errors out of 36. Two rows: k=5 raw, k=5 scaled. And the **baseline** written above the table, so both numbers have something to be compared to.
>
> **Three — your chosen k**, with three sentences of reason. And the reason cannot be 'it scored highest', because nine different k values score highest. Talk about the plateau.
>
> **Four — the honesty sentence.** Word for word: *'I chose this k by looking at test scores, which makes this estimate slightly optimistic.'* Every time, all year.
>
> **Five — the confusion matrix for your best model, with its worst row named in a full sentence.** Not 'row 1 is worst'. Something like: 'one wine that was really class 1 got called class 0, and one got called class 2.' Which way round matters.
>
> And Build It has a Piece 6 of short questions — do those last, when you're tired, because they're quick."

**Workbook sections:** in class, the **Warm-Up**, **Predict the Output** and **Practice Set A** (A1 to A3 feed the Hook and Concept; A4 to A6 if time allows). At home, **Practice Set B (B5, the sweep and chart) and Build It, Pieces 1 to 6** are the five hand-in items above (Piece 1 = the chart, Piece 2 = the comparison table, Piece 3 = the chosen `k`, Piece 4 = the honesty sentence, Piece 5 = the confusion matrix, Piece 6 = the short questions). B1 to B4, the **Fix the Broken Program**, the **Puzzle**, **Think Deeper**, **Piece 7 (Bug Log)**, **Draw It** and **Self-Check** are not in the one-hour estimate: set them as the following week's extra work or use them as the easier and harder options. Every answer is in the Answer Key below, in the workbook's order.

**Expected time:** 15 min to finish the sweep and save the chart · 15 min for the comparison table with the baseline · 15 min for the chosen `k` and the sentences (they should rewrite these) · 15 min for Build It Piece 6. About 60 minutes.

---

## 🔑 Answer Key

Every code block was run before it was pasted, and every number is real. All of it assumes `test_size=0.2, random_state=31, stratify=y`.

**How this key is laid out.** It follows the student workbook section by section, in the workbook's own order, using the workbook's own item labels (W1–W5, P1–P4, A1–A6, B1–B5, the Fix the Broken Program bugs, the Puzzle parts (a)–(n), T1–T2, Build It Pieces 1–7, Draw It, Self-Check). The values are those in the **✅ Answers** section at the end of the workbook, which were checked independently; the wrong-answer maps, marking tips and what-to-watch-for notes are additions for you. The workbook has no page numbers, so find things by section name and item label.

### Warm-Up (W1–W5)

| # | Answer | Marking note |
|---|---|---|
| W1 | `X_train, X_test, y_train, y_test` — both X's first, then both y's. | The usual slip is `X_train, y_train, X_test, y_test`, which silently puts labels into the test-features slot. |
| W2 | It **fixes the shuffle**, so the same cut happens every run and any change seen was caused by the student's change. **The number does not matter** — 0, 7, 31 and 42 are equally good. | Full marks need both halves: what it does, and that 42 is not special. |
| W3 | **`predict`.** If it could see the answers there would be nothing to predict. `fit` sees them to learn; `score` sees them to mark. | |
| W4 | Report **0.7333, on 30 rows.** The gap is **0.2083**, about 21 percentage points — a lot of the 0.9417 was memory rather than skill. | This is THE GAP from Week 29; it should match the board. |
| W5 | `ValueError: Expected 2D array, got 1D array instead`. `predict` wants a **table**, and one row is still a table: `model.predict([[3.0, 1.0]])`. | Accept "it errors because it needs double brackets" as a pass. |

### Predict the Output (P1–P4)

**P1 — swapped arguments.**

```text
0.625
0.625
[[2 1 0]
 [0 2 1]
 [0 1 1]]
[[2 0 0]
 [1 2 1]
 [0 1 1]]
```

- Are the two accuracies the same? **Yes**, 0.625 both ways. Are the two grids the same? **No** — the second is the first flipped along the diagonal (its transpose). The diagonal is unchanged, which is why the accuracy is unchanged and why nothing warns you.
- Row 1 totals: Grid A = 0 + 2 + 1 = **3**; Grid B = 1 + 2 + 1 = **4**; real class-1 count in `truth` = **3**. **Grid A** is right (`confusion_matrix(truth, guess)`), and the student can know it by adding up a row and comparing with the real class counts.
- Teacher note: for `accuracy_score` nothing changes if you swap the arguments; for `confusion_matrix` every mistake reads backwards while the accuracy looks identical. Both functions take truth-first, so learn the one rule and it covers both.

**P2 — marks and money.**

```text
[  60. 3000.]
[-1.41 -0.71  0.    0.71  1.41]
[-1.41 -0.71  0.    0.71  1.41]
[  40. 2000.]
```

- Lines 2 and 3 are **identical**: a column running 40–80 and one running 2000–4000 become the same five numbers. Both now say "how many spreads from typical am I?".
- Negative numbers are **not** a bug: half of anything is below average, and the middle value is exactly 0 because it is the mean.
- Line 4: `transform` did **nothing** to `marks` — `marks[0]` is still `[40, 2000]`. It hands back a **new** array. A machine that quietly rewrites your data cannot be debugged, and a double-scaled array gives no error and a silently broken model (same design idea as `sorted()` in Week 12).

**P3 — `stratify`.**

```text
[59 71 48]
[ 9 18  9]
[12 14 10]
36 36
```

- `stratify` did not change the **size** (both piles are 36). It changed **which** wines: each class keeps the same share in both halves.
- Class 1's share of the un-stratified test pile: 18 ÷ 36 = **50%**; of the whole table: 71 ÷ 178 = **39.9%**.
- Why it matters: the un-stratified pile is 25% / 50% / 25% when the real world is 33% / 40% / 27%, so the class-0 estimate rests on **nine** wines, each worth eleven percentage points.

**P4 — scientific notation.**

```text
[1.00e-04 2.25e+02]
225.0001
4.4e-05
15.0
```

- Notation: **scientific notation**. `1.00e-04` = 0.0001, `2.25e+02` = 225. Numpy switches to it when numbers in one array are very far apart in size; the notation itself is a warning that the two numbers do not belong in the same sum.
- Line 3 written out: `4.4e-05` = **0.000044**.
- Line 4 is **15.0**, exactly the proline gap, so hue contributed nothing measurable to the distance.

### Practice Set A — Read It (A1–A6)

#### A1 — Baselines

| # | Class counts | Baseline | An accuracy of… | Any good? |
|---|---|---|---|---|
| (a) | wine: 59 / 71 / 48 | 71/178 = **0.3989** | 0.7778 | Yes — nearly twice the baseline. |
| (b) | iris: 50 / 50 / 50 | 50/150 = **0.3333** | 0.9667 | Yes, comfortably. |
| (c) | spam: 5 spam, 95 not | 95/100 = **0.9500** | 0.9400 | **No — worse than a machine that says "not spam" to everything and has never read an email.** |
| (d) | breast cancer: 212 / 357 | 357/569 = **0.6274** | 0.9561 | Yes. |
| (e) | 10 pass, 10 fail | 10/20 = **0.5000** | 0.5000 | No. That is exactly a coin. |

**A1(f) Why compute the baseline before you train anything, rather than after?**
Because once you have seen 94% you will feel good about it, and the feeling arrives before the comparison. The baseline is the ruler, and you build a ruler before you measure with it. Compute it after and you will be quietly grading your own homework.

**A1(g) Row (c) has the highest baseline of the five. Which is the hardest problem to look good at, and which is the easiest to look good at dishonestly?**
Row (c), the spam one, is both: you have to beat 95% before you have done anything at all, and "94% accurate!" sounds excellent to anybody who has not asked what the baseline is. The more lopsided the classes, the more a bare accuracy flatters you.

#### A2 — The arithmetic that proves scaling matters

The two wines in the workbook: wine 0 is `hue 1.04, proline 1065.0`; wine 1 is `hue 1.05, proline 1050.0`.

**A2(a) The four steps, raw.**

```text
hue gap     :  1.04 − 1.05  =  −0.01     squared:    0.0001
proline gap : 1065  − 1050   =   15.00    squared:  225.0000
total       :                              225.0001
distance    :                               15.0000
```

**A2(b) Each column's share of the total.**
hue: 0.0001 ÷ 225.0001 × 100 = **0.000044%**. proline: **99.999956%**.

**A2(c) Divide each gap by its column's spread (hue 0.2279, proline 314.0217), then redo it.**

```text
hue     : 0.01 ÷ 0.2279   = 0.0439    squared: 0.0019
proline : 15   ÷ 314.0217  = 0.0478    squared: 0.0023
total   :                              0.0042

hue's share    : 45.76 %
proline's share: 54.24 %
```

**A2(d) One sentence on what changed.**

> Nothing about the wines changed and nothing about the model changed; dividing each gap by how much its own column normally varies took hue from contributing forty-four millionths of a percent to contributing nearly half.

**A2(e) `proline` runs 278 to 1680 and `hue` runs 0.48 to 1.71. Which column will dominate every distance in the raw table, and how do you know without doing the arithmetic?**
`proline`, because its gaps are measured in hundreds while hue's are in hundredths — that is a factor of about ten thousand *before* squaring, and squaring makes it a hundred million. You do not need the arithmetic; you need to look at the ranges. **Looking at min, max and spread for every column before you model is a habit worth having.**

**A2(f) Would scaling help a model that never measures distance?**
No. A decision tree (next week) asks "is proline above 755?" and scaling just changes the number in the question, never the answer. Scaling matters for models that add up squared differences.

Confirmed by `why_scaling.py` — full output in the Prep Checklist above.

#### A3 — Read both grids out loud

**The raw model, k = 5:**

```text
[[12  0  0]
 [ 0 13  1]
 [ 2  5  3]]
```

| Row | Sentence |
|---|---|
| 0 | Twelve wines really were class 0, and all twelve were called class 0. |
| 1 | Fourteen really were class 1: thirteen called class 1, one called class 2. |
| 2 | **Ten really were class 2: only three were called class 2. Five were called class 1 and two were called class 0.** |

**A3(a) Which is the worst row, and why?** Row 2. It gets 3 out of 10 right — worse than a coin — and it is where seven of the eight total errors live.

**A3(b) Accuracy from the grid, by hand.** Diagonal: 12 + 13 + 3 = 28. Total: 36. **28 ÷ 36 = 0.7778.** Eight wrong.

**A3(c) What does column 1 add up to, and what is that number?** 0 + 13 + 5 = **18.** It is the number of times the model *said* "class 1" — eighteen guesses, of which thirteen were right. Compare that with the fourteen wines that really were class 1. **Rows are truths; columns are guesses.**

**The scaled model, k = 5:**

```text
[[12  0  0]
 [ 1 12  1]
 [ 0  0 10]]
```

| Row | Sentence |
|---|---|
| 0 | All twelve class-0 wines correct. |
| 1 | Fourteen really were class 1: twelve correct, one called class 0, one called class 2. |
| 2 | All ten class-2 wines correct. |

**A3(d) What happened to row 2?** It went from 3 out of 10 to **10 out of 10.** The grape the raw model was nearly blind to, the scaled model gets perfectly. Not one new measurement was taken.

**A3(e) Accuracy from the grid.** 12 + 12 + 10 = 34, of 36. **0.9444.** Two wrong.

**A3(f) Which kind of mistake is left, and is it a forgivable one?** Both remaining errors are in row 1 — one class-1 wine called class 0 and one called class 2. They are boundary mistakes, one in each direction, which is the shape of an honest model working on a genuinely hard edge. That is a much more comfortable pattern than "all my errors are in one class".


#### A4 — Spot the bug

| # | The fix |
|---|---|
| a | `StandardScaler` — a *scaler* scales; a *scalar* is a single number |
| b | Add `scaler.fit(X_train)` above the `transform` |
| c | Split first, then `scaler.fit(X_train)`. Never `fit(X)` |
| d | `model.predict(X_test_scaled)` — whatever you did to `X_train`, do to `X_test` |
| e | `accuracy_score(y_test, model.predict(X_test))` — pass the guesses, not the model |
| f | `confusion_matrix(y_test, predictions)` — **truth first** |
| g | `stratify=y` — you balance the answers, not the measurements |
| h | `ax.set_ylim(0, 1.05)` — the axis starts at zero |

**A4(i).** The three with no error message: **(c), (d) and (h).** (The other five, (a), (b), (e), (f) and (g), raise real tracebacks.)

**A4(j).** The symptom to catch each:

1. **(c)**, the leak: the score goes **up**, 0.9444 to 0.9722. Nothing warns you; only the habit protects you.
2. **(d)**, unscaled `X_test`: accuracy **0.3333, below the baseline of 0.3989.** Anything below the baseline means something is broken.
3. **(h)**, the truncated axis: no error and a saved PNG, but a 5-point wiggle looks as dramatic as the 17-point finding. You catch it by opening the picture and asking "is that the chart I meant?".

**A4(k).** **(c), the leak.** A bug that lowers your score gets found, because you go looking. A bug that raises it gets kept; nobody investigates good news. And the number it produces is no longer an estimate of unseen-data performance, which is the only thing it was for.

*Wrong-answer map:* students often name (e) or (f) as "silent" because the fix looks small; ask them whether Python printed a traceback.

#### A5 — Label the grid

| Slot | Answer |
|---|---|
| Rows | **the truth** — what the thing really was |
| Columns | **the guess** — what the model said |
| Worst row | **Row 2.** Ten wines really were class 2; only three were called class 2, five were called class 1 and two were called class 0 |
| Row totals | row 0: **12** · row 1: **14** · row 2: **10** |

- **A5(a).** **Yes** — 12, 14, 10, exactly the real class counts. That confirms rows are truths.
- **A5(b).** Add up a row and compare it to the real class counts. If they match, rows are truth. It takes four seconds and needs no memory.
- **A5(c).** Column 1 = 0 + 13 + 5 = **18**: the number of times the model **said** "class 1", four more than the number of wines that actually were class 1.

#### A6 — Read the traceback (the `stratify=X` error)

- Which line first? The **last** one, always.
- How many classes does wine have? **Three.**
- Why is it complaining about a class with one member? Because `stratify=X` made sklearn treat **each whole row of thirteen measurements as a class label**; every "class" occurred exactly once, so it refused.
- How many "classes" did it think there were? **178**, one per wine.
- The fix: `stratify=y`.
- The sentence: *"You stratified on the measurements instead of the answers. Sklearn treated every unique row as its own class, so it found 178 classes with one member each. Change `stratify=X` to `stratify=y`."*

### Practice Set B — Write It (B1–B5)

**B1 — the baseline in one line.**

```python
print(round(np.bincount(wine.target).max() / len(wine.target), 4))
```

```text
0.3989
```

What the laziest model does: shouts "class 1" at every wine without looking and is right 71 times out of 178.

**B2 — mark twelve guesses.** `truth = [0,0,0,0,1,1,1,1,1,2,2,2]`, `guess = [0,0,0,1,1,1,1,2,0,1,1,2]`.

```text
accuracy: 0.5833
[[3 1 0]
 [1 3 1]
 [0 2 1]]
```

- Row 2 out loud: *"Three things really were class 2. Only one was called class 2, and **two were called class 1**."* Row 2 is the worst row, one out of three.
- Check: the rows add to 4, 5 and 3, the number of 0s, 1s and 2s in `truth`, so rows are truths.

**B3 — what the scaler learned.** Expected output (seed `random_state=31`, `stratify`, scaler fitted on the training rows only):

```text
hue
   mean learned  : 0.9553
   spread learned: 0.2153
   before, first 4: [0.96 1.05 0.7  0.94]
   after , first 4: [ 0.022  0.44  -1.186 -0.071]
proline
   mean learned  : 744.169
   spread learned: 307.0284
   before, first 4: [680. 450. 615. 415.]
   after , first 4: [-0.209 -0.958 -0.421 -1.072]

X_train is untouched, first row: [  0.96 680.  ]
```

By hand: (680 − 744.169) ÷ 307.0284 = **−0.209**. Hue 0.96 became 0.022, almost exactly typical. Marking tip: the student should notice the learned spread for hue (0.2153) differs slightly from the 0.2279 used in A2, because the scaler sees training rows only while A2 used all 178.

**B4 — the comparison table.**

```text
baseline: 0.3989

model            train     test    errors of 36
k=5 raw          0.7817   0.7778   8
k=5 scaled       0.9859   0.9444   2
```

Why count errors with a mask, `(pred != y_test).sum()`, rather than arithmetic? It is exact; `36 × 0.7778` gives 28.0008, which you then have to round and hope. (Week 20's boolean mask doing real work.)

#### B5 — the sweep and the chart

The student's program is the one in the workbook's B5 answer; the same sweep is inside the complete lab under **Build It** below. The 25-row table from a real run:


```text
k =  1   raw = 0.7500   scaled = 0.9167
k =  2   raw = 0.7778   scaled = 0.9167
...
k = 24   raw = 0.7500   scaled = 0.9722
k = 25   raw = 0.7500   scaled = 0.9722
```

Key rows to look at, read from the table above: k = 1 is 0.7500 raw and 0.9167 scaled; k = 5 is 0.7778 and 0.9444; **k = 7, 8, 9, 10 are all 0.9722 scaled**; k = 25 is 0.7500 and 0.9722.

- **Is the scaled line ever below the raw line?** No, not at any of the twenty-five values. That is unusually clear-cut, and it is why wine is the dataset for this lesson.
- **How many percentage points is one wine worth?** 1 ÷ 36 = **2.8**. So 0.9167 is 33 right, 0.9444 is 34 and 0.9722 is 35: **the entire wiggle in the scaled line is two wines changing their minds.** With a small test set, do not read meaning into small differences.
- **Why fit the scaler once, before the loop?** The scaling has nothing to do with `k`. Fitting it inside the loop gives the same answer twenty-five times, takes twenty-five times as long, and makes it easier to fit it on the wrong pile by accident.

### Fix the Broken Program (`wine_lab.py`, three bugs)

**Bug 1 — the syntax error.** Did any of it run? **No**: no `Traceback`, nothing printed, because Python could not finish reading the file. The unclosed `(` is the one after **`print`** (the `round(baseline, 4)` bracket is closed); Python points at the outer one because it was the last it was still waiting on. Fix:

```python
print("baseline:", round(baseline, 4))
```

**Bug 2 — the runtime error.** `baseline: 0.3989` printed **before** the traceback, so Python read the whole file and failed at run time; a syntax error prints nothing. The message is last week's "not fitted yet" with one word changed: everything in this library follows make, fit, use. `transform` could not subtract a mean it does not know, because the scaler has never been shown any data. Fix, a new line **above** the transform:

```python
scaler = StandardScaler()
scaler.fit(X_train)                      # <-- the missing line
X_train_scaled = scaler.transform(X_train)
```

**Bug 3 — the silent one.** Accuracy 0.3333 is **below** the baseline 0.3989, so the model is worse than shouting one word at every bottle. The model said **class 0** for all thirty-six wines. From the grid alone: columns 1 and 2 are entirely zero and column 0 holds all 36 guesses.

```text
[[12  0  0]
 [14  0  0]
 [10  0  0]]
```

The line is `predictions = model.predict(X_test)`, which should be `X_test_scaled`. No complaint, because 680 is a perfectly valid number and Python does not understand units. Fix:

```python
predictions = model.predict(X_test_scaled)
```

The habit: whatever you do to `X_train`, do to `X_test`, on the very next line.

### Puzzle of the Week (Parts 1–3)

**Part 1 — Choose your own shouty column**

**(a)**

| height in… | height gap | squared | age gap | squared | total | distance | height's share |
|---|---|---|---|---|---|---|---|
| millimetres | 50 | 2500 | 28 | 784 | 3284 | **57.31** | **76.13 %** |
| centimetres | 5 | 25 | 28 | 784 | 809 | **28.44** | **3.09 %** |
| metres | 0.05 | 0.0025 | 28 | 784 | 784.0025 | **28.00** | **0.0003 %** |

- **(b)** Zero people changed; zero were re-measured.
- **(c)** In millimetres height runs the show (76% of the distance); in metres age runs it completely.
- **(d)** The squared height gap would need to be about 784, so the height gap about **28**; the real gap is 5 cm, so the unit would be about **1.8 mm**, which nobody uses. There is no natural unit that balances two different kinds of measurement, which is why you rescale rather than hunt for the right unit.
- **(e)** *"Nothing about the two people changed, only the word at the top of a column, and the model's opinion of which of them is 'more different' flipped from height to age. So a distance is never a fact about the things you measured alone; it is a fact about them and the units somebody happened to choose."*

**Part 2 — Spot the Shouty Column**

| # | Which shouts | Roughly how badly |
|---|---|---|
| a | **height in mm** | By a mile; squared, about 3× the age contribution |
| b | **age in years** | Enormously; height is a rounding error in metres |
| c | **salary in rupees** | Overwhelmingly: tens of thousands against single digits, then squared |
| d | **exam mark out of 100** | About 10× before squaring, 100× after |
| e | **revision minutes** | Now the other way: 600 minutes beats 60 marks |
| f | **steps per day** | By thousands (20,000 against about 10) |
| g | **price in pence** | 100× the pounds column, about 10,000× after squaring |
| h | **it depends** | The arguable one |

- **(i)** **(h)**, km against a rating out of 5. A few kilometres and the columns are comparable; hundreds and distance wins easily. The honest answer is "measure it, do not guess": print min, max and spread of both.
- **(j)** Row (g) is also a **duplicated feature**: the same information twice, one column 100 times the other. Scaling does not fix that; **delete one of the two columns.**

**Part 3 — The column that stopped shouting**

- **(k)** **`hue`, on this one split.** Removing `hue` costs 5.6 percentage points (two wines); removing `proline` costs 2.8 (one wine). The column that was 0.000044% of the raw distance looks at least as useful as the one that was 99.999956% of it. Hold that loosely: see (n).
- **(l)** *The raw model was spending almost all its attention on one column (proline) and almost none on another (hue) that, when scaled, is at least as useful, not because proline was more informative but because it was written in bigger numbers. Scaling did not add information; it stopped the model throwing information away.*
- **(m)** **Not necessarily.** Zero cost usually means another column carries the same information (`total_phenols` and `flavanoids` move together). "Costs nothing to remove" and "contains nothing" are different claims, and only the first was tested.
- **(n)** **Almost none of it.** One wine is 2.8 points, so the whole spread of the table, 0.9722 down to 0.9167, is **two wines.** Only the general shape is worth saying: no single column is critical and the columns are fairly interchangeable.

### Think Deeper (T1–T2)

**T1 — the leak.** Model answer, in the student's voice:

> *0.9722 is supposed to be an estimate of how the model will do on wines nobody has ever seen. Fitting the scaler on all 178 wines broke that, and it did not take much: the proline mean moved from 744.17 to 746.89, a shift of 2.72. But the 36 test wines contributed to that 2.72, so they had a hand in preparing the 142 training wines; they were not unseen. A brand-new bottle tomorrow cannot possibly have helped work out my mean, so I should expect it to do worse than 0.9722, by an amount I do not know. The number went up and got less true.*
>
> *I cannot catch it by experiment either. On eight of ten seeds the leak makes no difference, and on one it makes the score worse, so an identical pair of scores is what "got away with it" looks like, not "safe". The only defence is the habit: split first, fit the scaler on the training rows, every time.*
>
> *That is why an upward bug is worse than a downward one. A bug that lowers your score is found by you, because you go looking. A bug that raises it is found by somebody else, later, in public. Nobody investigates good news.*

Marking: full marks needs (1) "an estimate of performance on unseen rows" stated precisely, (2) the 2.72 as evidence that a tiny leak is enough, (3) the "habit, not vigilance" conclusion from the eight-of-ten result, and (4) the who-finds-it observation.

**T2 — the 78% model against the 90% model.** Model answer:

> *There are eight errors and **seven are in row 2**: ten people really had the serious condition, three were identified, five were called "mild" and two "healthy". Row 0 is perfect and row 1 has one error. Every error in row 2 is in the direction of saying somebody is less ill than they are.*
>
> *So the 78% model is worse than the 90% one, by a long way: it misses **seven out of ten** serious cases. The 90% model with errors spread evenly would misclassify about four people in both directions, and the healthy ones get told to come back for a second test, an inconvenience rather than a catastrophe. A higher accuracy bought by getting the easy group perfect is a model that has learnt to look good.*
>
> *Who decides which mistakes are acceptable? By default the builder, often without noticing; then the organisation buying it, on cost and the same single number; and the person the mistake lands on has almost no say, because they were not in the room and may never be told a model was involved.*
>
> *I would insist on the full confusion matrix being printed next to the accuracy, with each row's success written as a fraction: "class 2: 3 of 10".*

Marking: full marks needs (1) the error distribution with the **direction** named, (2) a clear verdict on 78 versus 90 with who is harmed, (3) all three decision-makers considered and the last identified as having least say, and (4) a specific, concrete disclosure requirement.

### Build It — The Classifier Lab (Pieces 1–7)

The complete lab below assembles Pieces 1 to 5 (chart, comparison table, chosen `k`, confusion matrix) in one file, run end to end; its layout matches what the student is asked to produce. Pieces 1, 4, 6 and 7 are marked underneath it.


This is the whole thing in one file, run end to end. It is teacher reference material: the student builds it in pieces across Practice Set B (B4, B5) and Build It.

```python
# classifier_lab.py
# The whole Classifier Lab, top to bottom, on the wine table.

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")                    # save charts to a file, don't open a window
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix

# ---- 1. Look at the data --------------------------------------------------
wine = load_wine()
X = wine.data
y = wine.target

print("shape        :", X.shape)
print("class counts :", np.bincount(y))
baseline = np.bincount(y).max() / len(y)
print("baseline     :", round(baseline, 4), "(always shout the commonest class)")
print()

# ---- 2. One split, with the class mix kept --------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=31, stratify=y
)
print("train:", X_train.shape, " test:", X_test.shape)
print("test class counts:", np.bincount(y_test))
print()

# ---- 3. Two models, one table --------------------------------------------
raw_model = KNeighborsClassifier(n_neighbors=5)
raw_model.fit(X_train, y_train)
raw_pred = raw_model.predict(X_test)

scaler = StandardScaler()
scaler.fit(X_train)                      # train rows only
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

scaled_model = KNeighborsClassifier(n_neighbors=5)
scaled_model.fit(X_train_scaled, y_train)
scaled_pred = scaled_model.predict(X_test_scaled)

raw_acc = accuracy_score(y_test, raw_pred)
scaled_acc = accuracy_score(y_test, scaled_pred)

print("model          train    test     errors of 36")
print(f"k=5 raw        {raw_model.score(X_train, y_train):.4f}   {raw_acc:.4f}   {36 - int(round(raw_acc * 36))}")
print(f"k=5 scaled     {scaled_model.score(X_train_scaled, y_train):.4f}   {scaled_acc:.4f}   {36 - int(round(scaled_acc * 36))}")
print()

# ---- 4. Sweep k from 1 to 25 --------------------------------------------
ks = []
raw_scores = []
scaled_scores = []
for k in range(1, 26):
    ks.append(k)
    r = KNeighborsClassifier(n_neighbors=k)
    r.fit(X_train, y_train)
    raw_scores.append(r.score(X_test, y_test))
    s = KNeighborsClassifier(n_neighbors=k)
    s.fit(X_train_scaled, y_train)
    scaled_scores.append(s.score(X_test_scaled, y_test))

best = max(scaled_scores)
print("k values that reach the best scaled score", round(best, 4), ":",
      [ks[i] for i in range(len(ks)) if scaled_scores[i] == best])
print()

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(ks, scaled_scores, marker="o", label="scaled columns")
ax.plot(ks, raw_scores, marker="s", label="raw columns")
ax.set_title("Scaling is worth about 17 accuracy points on the wine table")
ax.set_xlabel("k (how many neighbours vote)")
ax.set_ylabel("accuracy on the 36 held-back wines")
ax.set_ylim(0, 1.05)
ax.legend()
fig.savefig("wine_accuracy_vs_k.png", dpi=120, bbox_inches="tight")
print("saved wine_accuracy_vs_k.png")
print()

# ---- 5. The chosen k, and its confusion matrix --------------------------
chosen = KNeighborsClassifier(n_neighbors=9)
chosen.fit(X_train_scaled, y_train)
chosen_pred = chosen.predict(X_test_scaled)
print("chosen k = 9")
print("train accuracy:", round(chosen.score(X_train_scaled, y_train), 4))
print("test  accuracy:", round(accuracy_score(y_test, chosen_pred), 4), "on", len(y_test), "rows")
print("confusion matrix:")
print(confusion_matrix(y_test, chosen_pred))
```

Real output (the 25 sweep lines are omitted here only because they are printed in full in the Activity section):

```text
shape        : (178, 13)
class counts : [59 71 48]
baseline     : 0.3989 (always shout the commonest class)

train: (142, 13)  test: (36, 13)
test class counts: [12 14 10]

model          train    test     errors of 36
k=5 raw        0.7817   0.7778   8
k=5 scaled     0.9859   0.9444   2

k values that reach the best scaled score 0.9722 : [7, 8, 9, 10, 18, 22, 23, 24, 25]

saved wine_accuracy_vs_k.png

chosen k = 9
train accuracy: 0.9789
test  accuracy: 0.9722 on 36 rows
confusion matrix:
[[12  0  0]
 [ 0 13  1]
 [ 0  0 10]]
```

**The comparison table, as it should be handed in (Piece 2):**

> **Baseline: 0.3989** — always shout "class 1" and you get 71 of 178 right.

| Model | Train accuracy | Test accuracy | Errors of 36 |
|---|---|---|---|
| kNN k=5, raw columns | 0.7817 | 0.7778 | 8 |
| kNN k=5, scaled columns | 0.9859 | 0.9444 | 2 |
| kNN k=9, scaled columns *(chosen)* | 0.9789 | **0.9722** | **1** |

**The chosen `k` write-up, full marks (Piece 3):**

> I chose **k = 9**, which scores **0.9722 on 36 held-back wines**, against a baseline of 0.3989. I chose it because k = 7, 8, 9 and 10 all give the same 0.9722 — four consecutive values, which is a plateau rather than a lonely spike, so the answer does not depend on me getting k exactly right. Within that plateau I took the largest odd value: larger k is less sensitive to one strange neighbour, and an odd k produces fewer tied votes. **I chose this k by looking at test scores, which makes this estimate slightly optimistic.** I should also say that 0.9722 is 35 wines out of 36, so the difference between this and k = 5's 0.9444 is exactly one wine, and I would not claim k = 9 is definitely better than k = 5 on the strength of one wine.

*(That last sentence is not required. A student who writes it unprompted is at mastery level 5.)*

**The confusion matrix for k = 9, with its worst row named (Piece 5):**

```text
[[12  0  0]
 [ 0 13  1]
 [ 0  0 10]]
```

> Row 1 is the worst row: fourteen wines really were class 1, thirteen were called class 1, and **one was called class 2**. Rows 0 and 2 are perfect. One error out of thirty-six.


**Piece 1 — the chart.** Model title: *"Scaling is worth about 17 accuracy points on the wine table"* (it states the finding, not the topic).

- **Why the y-axis must start at zero:** the gap **between** the two lines is about 17 points and the wiggle **within** each line is about 5. Start the axis at 0.7 and the wiggle looks as dramatic as the real finding, so a reader glancing for a quarter of a second gets the wrong story. Week 27 taught exactly this: an axis that does not start at zero can make a small difference look enormous without changing a single number.
- **The plot checklist:** title stating the finding · different markers as well as colours · both axis labels including what is measured (and the 36-row count on y) · legend, because there are two lines · `set_ylim(0, 1.05)` · saved with `savefig`, then opened and looked at.

**Piece 2 — the comparison table.** Points scaling bought: 0.9444 − 0.7778 = **16.7 percentage points.** What was added to get them: **nothing** — no new measurements, no new wines, `k` unchanged at 5, same model. Only `proline` stopped shouting over the other twelve.

**Piece 3 — my chosen `k`.** The three sentences, mapped to the workbook's prompts:

- **Sentence 1 (ties):** nine values of `k` reach 0.9722: 7, 8, 9, 10, 18, 22, 23, 24 and 25, so "the highest score" does not pick a single answer.
- **Sentence 2 (plateau):** `k = 7, 8, 9, 10` are four consecutive values all at 0.9722, a plateau rather than a lonely spike; a plateau is more trustworthy because the score does not depend on getting `k` exactly right.
- **Sentence 3 (why this one):** inside the plateau take the largest odd value, since a larger `k` is less sensitive to one strange neighbour and an odd `k` gives fewer tied votes.
- Marking: "it scored highest" earns no credit for Sentence 1 or 3; the Homework script tells the student this in advance.

**Piece 4 — the honesty sentence.** Word for word: *"I chose this k by looking at test scores, which makes this estimate slightly optimistic."* The student's own-words reason should be something like: *"I looked at the sealed envelope twenty-five times to decide something; something that helps you choose has taught you, so 0.9722 is a bit flattering, by an amount I cannot measure. The proper fix is a third pile of data I never tune against, and I do not have enough wines, so the honest thing left is to say so."*

**Piece 5 — the confusion matrix.** For `k = 9`, scaled, as printed in the complete lab above. Row totals **12, 14, 10** match the real class counts, so rows are truths. The worst row, named with a direction: *row 1, fourteen wines really were class 1, thirteen were called class 1 and **one was called class 2**.* Total errors **1** of 36; accuracy (12 + 13 + 10) ÷ 36 = 35 ÷ 36 = **0.9722**. Rows 0 and 2 are perfect. If a student uses the `k = 5` scaled model instead, the grid is the A3 scaled grid, with 2 errors, 0.9444, and row 1 named as worst.

**Piece 6 — short questions.**

| # | Question | Answer |
|---|---|---|
| i | What is the baseline for the wine table? | 71/178 = 0.3989. Always shout the commonest class. |
| ii | In `confusion_matrix(y_test, pred)`, are rows the truth or the guess? | The truth. Columns are the guess. Check it by adding a row up and matching it to the real class counts. |
| iii | Which rows does the scaler learn from? | The training rows only, and only after the split. |
| iv | What does `stratify=y` do? | Keeps each class's share the same in both halves of the split. |
| v | Why `stratify=y` and not `stratify=X`? | You balance the answers, not the measurements. Every feature row is unique, so `stratify=X` gives "the least populated class has only 1 member". |
| vi | You forget to scale `X_test`. What is the symptom? | No error at all, and an accuracy of 0.3333 — below the baseline. The model learnt in scaled world and got handed raw numbers. |
| vii | You fit the scaler on all the data before splitting. What is the symptom? | No error, and the score goes **up** — 0.9444 becomes 0.9722. A better number that is less true. |
| viii | Why is a leak that raises your score worse than a bug that lowers it? | A bug that lowers your score gets found, because you go looking. A leak that raises it gets kept. And the number it produces is no longer an estimate of unseen-data performance, which is the only thing the number was for. |
| ix | Two models score 0.9444 and 0.9722 on 36 test rows. Is the second better? | It is one wine better, and one wine out of 36 is 2.8 percentage points. Not enough to claim anything. Report both, and say the test set is small. |
| x | Why does `transform` hand back a new array instead of changing `X_train`? | So you can print before and after, re-run a line safely, and never accidentally scale the same data twice — which produces no error and a broken model. |
| xi | Name one situation where you should **not** scale. | Iris (all four columns are already comparable centimetres, and scaling makes kNN slightly worse), or any decision tree (it never measures distance, so scaling only changes the threshold in the question, never the answer). |
| xii | The sentence you write next to every `k` you chose from test scores. | "I chose this k by looking at test scores, which makes this estimate slightly optimistic." |

**Piece 7 — the Bug Log.** No single right answer; each row should record what happened, whether there was an error message (bug 1 and bug 2 of the Fix yes, bug 3 and the leak no), what fixed it, and a check for next time. A good last column reads like "compare accuracy to the baseline" or "transform `X_test` on the very next line".

### Draw It

There is no single right drawing. A good one has the RAW pair drawn to a **true** scale, one bar visible and the other genuinely unmeasurable (`hue gap² = 0.0001` as a pencil line against `proline gap² = 225.0000` at about 60 mm), and the SCALED pair nearly equal (0.0019 and 0.0023) with the shares 45.76% and 54.24% written underneath and the two spreads, `hue 0.2279` and `proline 314.02`, on the arrow between them.

- The tell that it is right: on the left, one of the two bars cannot be drawn. If both are bars of comparable height, the ratio was written down but never illustrated.
- The tell that it is good: an annotation saying **nothing about the wine changed.**

### Self-Check

The ten "I can…" rows are self-rated; ask the student to point at one they marked 😀 and show you. True or false:

| Statement | Answer | Why |
|---|---|---|
| A higher accuracy always means a better model | **FALSE** | The leaky version scored higher and was the only one that was a lie |
| Scaling adds information to your data | **FALSE** | It stops one column throwing the others' information away |
| The scaler learns from the training rows only | **TRUE** | And only after the split |
| `transform` changes `X_train` in place | **FALSE** | It hands back a new array; `marks[0]` was still `[40, 2000]` |
| Half the scaled numbers being negative means something broke | **FALSE** | Below average is a negative number of spreads |
| `confusion_matrix` gives the same grid whichever way round | **FALSE** | You get the transpose, and every mistake reads backwards |
| Accuracy gives the same number whichever way round | **TRUE** | 0.625 either way, which is why the grid catches what accuracy cannot |
| Rows of a confusion matrix add up to the real class counts | **TRUE** | 12, 14, 10 |
| Columns add up to the real class counts | **FALSE** | They add up to the **guessed** counts; column 1 was 18 against 14 real |
| `stratify=X` balances your features | **FALSE** | It treats every unique row as its own class and errors out |
| You should always scale, on every dataset | **FALSE** | On iris it makes kNN slightly worse |
| A decision tree needs its columns scaled | **FALSE** | "Is proline above 755?" gives the same answer in any unit |
| Forgetting to scale `X_test` raises an error | **FALSE** | No error, and 0.3333, below the baseline |
| A leak that leaves the score unchanged on your split was harmless | **FALSE** | It means you got away with it; you cannot tell in advance |
| Choosing `k` from test scores costs you nothing | **FALSE** | Twenty-five peeks at the envelope; hence the honesty sentence |

### Lesson questions posed in the Say-this scripts

- *"What percentage of the distance came from hue?"* → 0.000044%. Forty-four millionths of one percent.
- *"Is proline more important than hue?"* → No. It has bigger numbers. Nothing in that arithmetic said anything about wine.
- *"How would you fix it?"* → Make the columns comparable — divide each gap by how much its own column varies.
- *"Row 2 adds up to 10. What is that 10?"* → The number of wines that really were class 2. Rows are truths.
- *"What does the diagonal mean?"* → Everything the model got right.
- *"Accuracy is 78%. Is this model fine?"* → No. It gets 3 of 10 class-2 wines, so it is nearly blind to one of the three grapes, and the single number hides that completely.
- *"Why does `stratify` take `y`?"* → Because you are balancing the answers. `stratify=X` treats each unique feature row as its own class and errors out.
- *"Half the scaled numbers are negative. Is that wrong?"* → No. Half of anything is below average, and below average is a negative number of spreads. (680 − 744.17) ÷ 307.03 = −0.21.
- *"What did we change to gain 16.7 points?"* → Nothing about the data or the model. Only the scale of the columns.
- *"Read me row 2 of the new grid."* → 0, 0, 10. All ten class-2 wines correct.
- *"Why didn't the unscaled-test-rows bug crash?"* → 680 is a perfectly valid number. Python would have to understand units to spot it, and it does not.
- *"33% against a baseline of 39.9% — what does that tell you?"* → That the model is now worse than not looking at the wine at all, so something is broken even though nothing complained.
- *"What's the habit that prevents it?"* → Whatever you do to `X_train`, do to `X_test`, on the very next line.
- *"Which k, and why?"* → 9. Seven to ten are all 0.9722, which is a plateau; take the biggest odd one, because bigger is steadier and odd ties less often.
- *"Will the leaky score go up, down or stay the same?"* → Up, on this split. 0.9444 → 0.9722.
- *"I introduced a bug and my score improved. Why is that bad news?"* → Because the score is meant to estimate performance on unseen rows, and the test rows helped prepare the training data, so they were not unseen. A genuinely new wine tomorrow cannot have helped work out the mean, so expect it to do worse than 0.9722. The number went up and got less true.
- *"Tomorrow a brand-new wine arrives. Could it have helped work out the mean?"* → No. Which is exactly why fitting the scaler on everything is a lie about the future.

---

## 🔮 Next Week Preview

Week 31 changes model, and the change is the point: a **decision tree** does not measure distance at all. It asks a short stack of yes/no questions — *"is the petal longer than 2.45 cm? then it's setosa"* — and the astonishing thing is that you can print the exact questions it learnt and read them out loud, in English, to somebody who has never seen code. After three weeks of a model whose insides are just a copy of the training table, the student gets one whose insides are a page of sentences they can argue with. Two consequences land immediately and both are worth looking forward to: a tree needs **no scaling whatsoever**, because "is proline above 755?" gives the same answer whatever units proline is in — so this week's hard-won habit is suddenly irrelevant, and understanding *why* is the test of whether this week landed. And a tree will tell you which of the thirteen measurements it actually used, and which it ignored completely, which is Level 1's feature scoreboard arriving with the arithmetic done for you.

**Prep early:** two things. **One — keep this week's `wine_accuracy_vs_k.png` and the comparison table**; Week 31 adds a tree row to that same table and the comparison across weeks is where the learning is. **Two — leave both boards up**: THE GAP from Week 29 and the `0.7778 → 0.9444` from this week. Week 31 adds a third line, Week 33 comes back for all of them, and the moment the term makes sense is the moment a student can point at three weeks of numbers on the same wall.

---

[⬅ Week 29](week-29.md) · [Course Home](../README.md) · [Week 31 ➡](week-31.md) · [Student Guide](../student-guide/week-30.md) · [Workbook](../workbook/week-30.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)

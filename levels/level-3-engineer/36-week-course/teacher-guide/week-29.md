# Week 29 — A New Pair of Axes

[⬅ Week 28](week-28.md) · [Course Home](../README.md) · [Week 30 ➡](week-30.md) · [Student Guide](../student-guide/week-29.md) · [Workbook](../workbook/week-29.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — the second half of Term 4's toolkit |
| **Big idea** | **PCA does not delete columns.** It draws a new axis along the direction the data is most spread out, then measures everything against that instead. Thirteen columns become two numbers per row, and **the price is measurable.** |
| **New vocabulary** | variance · principal component · projection · explained variance ratio · loading · reconstruction error · curse of dimensionality |
| **New maths** | **Variance** — the average squared distance from the mean — computed by hand on the five numbers 4, 6, 8, 10, 12. Then **"the direction of biggest spread"** found the honest way: try six candidate directions 30° apart, project all five points onto each one, and keep whichever gave the widest spread. **No eigenvectors. No linear algebra.** |
| **New syntax** | `PCA(n_components=2)` · `pca.explained_variance_ratio_` · `pca.components_` · `pca.inverse_transform(Z)` |
| **Dataset** | **Five 2-D points drawn on graph paper by hand**, then `load_wine()` with all thirteen columns. Both ship inside scikit-learn. **Nothing downloads. No internet needed.** |
| **Materials** | Printed workbook (Warm-Up, Do the Maths by Hand, Predict the Output, Practice Sets A and B, Fix the Broken Program, Puzzle, Think Deeper, Build It, Draw It, Self-Check) · **real graph paper, one sheet each, at least 10 squares by 10** · **a ruler and a protractor each** · a new wall sheet headed **SPREAD** with a blank number line · the SIX POINTS sheet still up from last week · the Bug Log |
| **Tech needed** | Laptop with Python 3, numpy, pandas, matplotlib, scikit-learn. **No torch this week. No new installs.** |
| **Prep time** | 25 minutes the night before · 10 minutes on the day (drawing the six candidate axes on the board) |
| **Expected runtime of the code** | `new_axes.py` runs in **about 1.7 seconds** end to end, including saving one PNG. **Time yours anyway.** |

> **⚠️ Watch out:** the real PCA is built out of eigenvectors of a covariance matrix, and **you must not go anywhere near that today.** The student has never seen a matrix inverse, an eigenvector or a determinant, and will not in this course. What they *can* do — and what this lesson is built on — is **try six directions, measure the spread along each one, and keep the widest.** That is not a simplification of PCA's answer; it is a genuinely correct way to find it, just a slower one. The class's 30-degree grid lands on **17.4192** and PCA's exact answer is **18.2812**, and **saying out loud that the grid was twelve degrees short is more honest and more useful than any amount of eigenvector notation.** If a student asks how sklearn finds the exact angle, the answer is: *"there is a formula, it needs maths you will meet at university, and it gives the same answer as a very fine grid."*

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Compute the variance of a small column by hand**, as the average squared distance from the mean: 4, 6, 8, 10, 12 → distances −4, −2, 0, 2, 4 → squares 16, 4, 0, 4, 16 → **40**, and 40 ÷ 4 = **10.0**.
2. **Find a principal component for five points** by trying candidate axes at 30° steps, projecting by hand, and keeping the widest — and say how far off the grid's answer was from PCA's.
3. **Read `explained_variance_ratio_`** and say how many components are needed to keep 80% of the spread. For the wine data the answer is **5**.
4. **Reconstruct data from a few components and measure what was lost, in the table's own units** — two components miss a typical wine by **2.2550** when a typical wine sits only **3.5180** from the middle.

Observable evidence: the class graph-paper sheet with the four steps of variance written out and `40 ÷ 4 = 10.0`; the same sheet with one candidate angle's five projected scores and its spread, matching the class table; the workbook's Build It table of thirteen shares with a running total column and **5** circled at `0.8016`; and a sentence of the form *"two components keep 55.4% of the spread and miss a typical wine by 2.2550, which is 64% of a typical distance from the middle."*

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each one carries on from the one above. **The complete runnable file is in the Prep Checklist and the Answer Key.**

**The single most important thing in this file:** PCA has a reputation for being hard, and that reputation comes entirely from *how it is computed*, not from *what it does*. What it does is ordinary. Your job today is to teach what it does, and to be completely straightforward about the fact that you are not teaching how sklearn computes it.

### 1. Why anybody wants this: thirteen columns is too many

Last week's wine data had 13 columns. You cannot draw 13 dimensions, and you cannot look at 78 scatter plots. But there is a worse problem than "hard to draw", and it is worth knowing because it is the real reason PCA and k-means are taught together.

> **Curse of dimensionality** — as you add columns, every point drifts away from every other point until they are all **roughly the same distance apart** — and then anything that works by comparing distances stops meaning anything.

Here is the measurement, on 150 random points in a `d`-dimensional cube:

```text
   d       min      mean       max   (max-min)/min
   2    0.0025    0.5393    1.3580        533.8576
   5    0.0873    0.8485    1.6953         18.4217
  20    0.9006    1.8105    2.6697          1.9645
 100    3.1520    4.0624    5.3787          0.7065
 500    8.1944    9.1212    9.8894          0.2068
```

**Read the last column, which is the contrast: how much further apart the furthest pair is than the closest pair.** At 2 columns the furthest pair is 534 times further apart than the closest. At 100 columns it is **0.7 times** further — under twice as far. At 500 columns, **the most distant pair of points in your whole dataset is only 21% further apart than the two closest points.**

🍕 **The analogy.** In a corridor, your nearest neighbour is obviously the person standing next to you. In a field, still obvious. **In a five-hundred-dimensional world, every single person is standing at almost exactly the same distance from you, and none of them is meaningfully "near".** k-means makes every single decision by asking "which centre is nearest?", so k-means goes blind. So does kNN, which they have known since Level 2.

**The practical response: cut the number of columns before you cluster.** Which is what PCA is for.

### 2. Variance: the average squared distance from the mean

Everything in PCA is built on one quantity, and the student has met three quarters of it already — the standard deviation in Week 4.

> **Variance** — take every value's distance from the mean, square it, and average. That is all. It is the standard deviation before you take the square root.

Four steps, on five numbers, and you should do this on paper yourself before the lesson:

```text
the numbers            :   4     6     8    10    12
the mean               :   (4+6+8+10+12) ÷ 5 = 40 ÷ 5 = 8

step 1: how far off    :  −4    −2     0    +2    +4
step 2: squared        :  16     4     0     4    16
step 3: add them up    :  16 + 4 + 0 + 4 + 16 = 40
step 4: average        :  40 ÷ 4 = 10.0
```

![Variance is the average squared distance from the mean](../figures/fig-w29-5-variance-as-average-squared-distance.svg)
*Figure 29.1 — Variance is the average squared distance from the mean. Distances −4, −2, 0, 2, 4; squares 16, 4, 0, 4, 16; total 40; and 40 ÷ 4 = 10.0.*

**Two things a student will ask, and you need both answers ready.**

**"Why square them?"** Because without squaring they cancel: −4 + −2 + 0 + 2 + 4 = **0**, every single time, for any set of numbers. The mean is exactly the place where the distances cancel out. **Squaring throws away the minus signs so the total stops being zero.** (Taking absolute values would also work, and gives a different, less convenient measure that real statisticians do sometimes use.)

**"Why divide by 4 when there are five numbers?"** And here you should be honest rather than hand-wavy. There are two conventions:

- **Divide by 5** (the number of values). This is the variance *of these five numbers*, full stop. Gives **8.0**.
- **Divide by 4** (one less). This is the estimate you use when your five numbers are a *sample* from something bigger, and it comes out slightly larger to allow for the fact that you measured the mean from the same five numbers. Gives **10.0**.

**scikit-learn's `PCA` divides by n − 1. scikit-learn's `StandardScaler` divides by n.** That is a real inconsistency in the library and it will bite you once: the thirteen `explained_variance_` numbers for the scaled wine data add up to **13.0734**, not 13.0000, and 13 × 178 ÷ 177 = 13.0734 exactly. **If a student spots that, tell them the truth — two parts of the same library chose different conventions, they know, and it does not matter here.** Do not pretend it adds to 13.

**And the one sentence that makes variance matter today:** a column with a big variance is a column where the rows are spread far apart, so it is a column where rows *differ*. A column with variance zero is the same value in every row and tells you nothing at all. **PCA is a machine for chasing spread**, because spread is where the information is.

### 3. Projection: what "measuring along a direction" actually means

This is the one genuinely new geometric idea, and it takes two minutes with numbers.

Take our five points — five students, `(hours studied, hours slept)` per week:

```text
(4, 3)   (6, 6)   (8, 7)   (10, 8)   (12, 11)
```

**Step one, always: move the middle to (0, 0).** PCA is about spread, not about where the cloud sits.

```text
mean across = (4 + 6 + 8 + 10 + 12) ÷ 5 = 40 ÷ 5 = 8
mean up     = (3 + 6 + 7 +  8 + 11) ÷ 5 = 35 ÷ 5 = 7

centred:  (−4, −4)   (−2, −1)   (0, 0)   (2, 1)   (4, 4)
```

Now pick a direction. A direction is just **a pair of numbers saying how far across and how far up you go for one step**, chosen so that one step is exactly one unit long. At 30°, one step is:

```text
across = 0.86603        up = 0.50000
```

> **Projection** — sliding a point sideways onto a line, at right angles, and reading off how far along the line it landed. The number you read off is the point's **score** on that axis.

**And the arithmetic for it is one multiply-and-add per coordinate**, which is exactly the matrix-multiply cell they did by hand in Week 17:

```text
the point (4, 4), on the 30° direction:
    4 × 0.86603  +  4 × 0.50000
  = 3.46410      +  2.00000
  = 5.46410
```

**That single number 5.46410 is the whole of that point, as far as this axis is concerned.** Two numbers became one.

Do all five:

```text
(−4, −4) → −5.46410
(−2, −1) → −2.23205
( 0,  0) →  0.00000
( 2,  1) →  2.23205
( 4,  4) →  5.46410
```

And now the variance of *those five scores*, by the four steps from §2 (their mean is already 0, which is why centring first was worth doing):

```text
squares :  29.85641   4.98205   0.00000   4.98205   29.85641
add up  :  69.67691
÷ 4     :  17.41923
```

**17.41923 is the spread of the cloud along the 30° direction.** That is the number the whole activity is built on, and every student computes one of them by hand.

![The same cloud, measured against two new axes](../figures/fig-w29-1-cloud-with-its-two-new-axes-drawn.svg)
*Figure 29.2 — The same cloud, measured against two new axes. The old axes stay on the page in grey. The top point, 4 across and 4 up from the middle, drops onto PC1 at right angles: 4 × 0.7359 + 4 × 0.6771 = 5.6520.*

### 4. Trying angles: the honest way to find a principal component

> **Principal component** — a direction through the data, chosen so the spread of the projected scores is as wide as possible. **PC1** is the widest direction there is. **PC2** is the widest of what is left, at right angles to PC1.

So how do you find the widest direction? **Try some.** Here are all six candidates at 30° steps, every number real:

```text
 angle   direction (across, up)     the five scores along it              spread
   0°   ( 1.0000,  0.0000)   [-4.000 -2.000  0.000  2.000  4.000]  10.0000
  30°   ( 0.8660,  0.5000)   [-5.464 -2.232  0.000  2.232  5.464]  17.4192
  60°   ( 0.5000,  0.8660)   [-5.464 -1.866  0.000  1.866  5.464]  16.6692
  90°   ( 0.0000,  1.0000)   [-4.000 -1.000  0.000  1.000  4.000]   8.5000
 120°   (-0.5000,  0.8660)   [-1.464  0.134  0.000 -0.134  1.464]   1.0808
 150°   (-0.8660,  0.5000)   [ 1.464  1.232  0.000 -1.232 -1.464]   1.8308
widest of the six: 30° with spread 17.4192
```

![Try angles, keep the widest](../figures/fig-w29-2-trying-angles-keeping-the-widest.svg)
*Figure 29.3 — Try angles, keep the widest. 10.0000 at 0°, 17.4192 at 30°, 8.5000 at 90°. And PCA's exact answer: 42.62°, spread 18.2812.*

**Three things to notice in that table, and say all three out loud.**

**One: 0° and 90° are the original columns.** At 0° the scores are just the centred "hours studied" values and the spread is `10.0` — which is `var(hours studied)`. At 90° it is `8.5` = `var(hours slept)`. **The original columns are just two of the candidate directions, and neither of them wins.** That is the entire idea of PCA in one observation.

**Two: 120° and 150° are terrible** — spreads of 1.08 and 1.83. Those directions look *across* the cloud rather than along it, and everything squashes into a blob. The midge-cloud analogy below is for exactly this.

**Three: 30° wins with 17.4192, and PCA's answer is 42.62° with 18.2812.** Our grid was **12.62 degrees short** and cost us `18.2812 − 17.4192 = 0.8620` of spread. **Say that. It is the most educational number of the lesson**, because it tells the class exactly what the method is: a search, which a finer grid does better. Try every whole degree and the best is 43°, with a spread of **18.2804** — within 0.001 of the exact answer.

🍕 **The analogy, and it is the one to use.** A long thin cloud of midges hangs over a garden and you want to photograph it. Stand at one end and shoot along its length: you get a small blob, and you have lost almost everything. Stand to the side: you get a long streak and you can see the whole shape. **PC1 is the angle that gives you the longest streak.** And the reason "longest streak" is the right thing to want is that a streak keeps the differences between midges, and a blob throws them away.

### 5. What comes back from sklearn, and the four things to print

```text
pca.components_:
[[ 0.7359  0.6771]
 [-0.6771  0.7359]]
PC1's angle: 42.62°
pca.explained_variance_      : [18.2812  0.2188]
pca.explained_variance_ratio_: [0.9882 0.0118]
the two spreads add to: 18.5 = 10.0 + 8.5, the spread of the two original columns
```

**`pca.components_` is the directions, one per row.** Row 0 is PC1: go 0.7359 across and 0.6771 up. Row 1 is PC2: −0.6771 across and 0.7359 up, which is at right angles to PC1 — notice the two numbers are the same pair, swapped and with one sign flipped, which is what "at right angles" looks like in two dimensions.

**`pca.explained_variance_` is the spread along each one**: 18.2812 along PC1 and 0.2188 along PC2.

**And then the check that ties it all together, which is genuinely lovely:**

```text
18.2812 + 0.2188 = 18.5000
var(hours studied) + var(hours slept) = 10.0 + 8.5 = 18.5
```

**The total spread has not changed. It has been redistributed.** PCA did not create or destroy anything; it rotated the axes so that nearly all the spread piled onto the first one. **Say this and write it on the board — it is the difference between PCA as magic and PCA as a rotation.**

> **Explained variance ratio** — each component's spread divided by the total. `18.2812 ÷ 18.5 = 0.9882`. **"PC1 explains 98.82% of the spread"** means: keep only PC1 and you keep 98.82% of the differences between these five students.

### 6. Reconstruction: the bill for throwing PC2 away

`explained_variance_ratio_` is the optimistic framing. Here is the honest one.

> **Reconstruction error** — squash the data down to a few components, then push it back up to the original columns, and measure how far each rebuilt point is from the real one. **That distance is the information you threw away, expressed in the table's own units.**

Squash the five students to **one** number each and rebuild:

```text
one number per student: [-5.652  -2.1489  0.      2.1489  5.652 ]
rebuilt from that one number:
[[ 3.8408  3.173 ]
 [ 6.4187  5.545 ]
 [ 8.      7.    ]
 [ 9.5813  8.455 ]
 [12.1592 10.827 ]]
the real points:
[[ 4.  3.]
 [ 6.  6.]
 [ 8.  7.]
 [10.  8.]
 [12. 11.]]
how far each rebuilt point is from the real one: [0.2351 0.6183 0.     0.6183 0.2351]
average miss: 0.3414 hours
```

**Read the last student: real (12, 11), rebuilt (12.1592, 10.827).** Out by 0.16 of an hour studying and 0.17 of an hour sleeping. **Two numbers became one, and it cost a fifth of an hour.** That is what "98.82% of the spread" feels like in hours.

**And the middle student is exactly right — (8, 7) rebuilt as (8, 7), miss 0.0000.** Worth asking about: it is the one sitting at the mean, and the mean is the one point a single component can always place perfectly.

**On the wine data the bill is much bigger, and this is the number the homework is built on:**

```text
  how many PCs   running share   average rebuild miss
       1           0.3620            2.7527
       2           0.5541            2.2550
       3           0.6653            1.9581
       5           0.8016            1.5303
       6           0.8510            1.3258
       8           0.9202            0.9599
      13           1.0000            0.0000
for scale: a typical wine sits 3.5180 away from the middle
```

Two components keep **55.4%** of the spread — that sounds respectable. But the miss is **2.2550**, and a typical wine only sits **3.5180** from the middle of the cloud, so:

```text
2.2550 ÷ 3.5180 = 0.6410
```

**Your rebuilt wine is wrong by 64% of a typical wine's whole distance from the middle.** With six components it is `1.3258 ÷ 3.5180 = 0.3769`, or 38%. **Thirteen components rebuild perfectly — 0.0000 — because you threw nothing away.**

![Explained variance is the promise, rebuild error is the bill](../figures/fig-w29-4-reconstruction-from-two-components.svg)
*Figure 29.4 — Explained variance is the promise, rebuild error is the bill. 2 components: 0.5541 kept, 2.2550 missed. 6 components: 0.8510 kept, 1.3258 missed. And 2.2550 ÷ 3.5180 = 0.6410.*

> **Report both numbers, always. "PC1 and PC2 keep 55% of the variance" is the sales brochure. "Rebuilding from two components misses a typical wine by 64% of its distance from the middle" is the invoice.** Both are true about the same run.

### 7. The thirteen wine components, and naming an axis

```text
PC   its share   running total
 1     0.3620       0.3620
 2     0.1921       0.5541
 3     0.1112       0.6653
 4     0.0707       0.7360
 5     0.0656       0.8016
 6     0.0494       0.8510
 7     0.0424       0.8934
 8     0.0268       0.9202
 9     0.0222       0.9424
10     0.0193       0.9617
11     0.0174       0.9791
12     0.0130       0.9920
13     0.0080       1.0000
```

**Two numbers to say out loud.** `PC1 + PC2 = 0.5541` — **just over half the story in two dimensions**, which is what makes a 2-D picture of 13 columns worth drawing and also what makes it dangerous. And **`0.8016` at PC5** — five components out of thirteen carry 80% of the spread. That is the answer to objective 3, and it is read straight off the running total.

![Thirteen shares, and the running total](../figures/fig-w29-3-explained-variance-bars-with-running-total.svg)
*Figure 29.5 — Thirteen shares, and the running total. 0.3620 + 0.1921 = 0.5541 after two, and the total crosses 80% at the fifth component with 0.8016.*

> **Loading** — how hard one original column pulls on one component. A big positive loading means that column and the component go up together.

```text
PC1: which original columns pull hardest
flavanoids                      0.423
total_phenols                   0.395
od280/od315_of_diluted_wines    0.376
proanthocyanins                 0.313
nonflavanoid_phenols           -0.299
```

**The top four all pull the same way, and they are all phenol measures or close relatives: flavanoids, total phenols and proanthocyanins are phenolic compounds, and od280/od315 is a light-absorbance ratio that tracks them.** So PC1 is fairly read as **"total phenolic richness"** — one end of the axis is chemically rich wine, the other end is thin wine. `nonflavanoid_phenols` is negative, meaning it goes the *other* way from the rest, which in these 178 wines is a real pattern and not a bug.

```text
PC2: which original columns pull hardest
color_intensity    0.530
alcohol            0.484
proline            0.365
ash                0.316
magnesium          0.300
```

PC2 is colour, alcohol and proline together — fairly read as **"body and depth"**. **Naming your components from their loadings is a real professional skill**, and it is the difference between a plot with "PC1" on the axis and a plot somebody can act on.

**⚠️ Two warnings about loadings, and both come up.**

**The signs are arbitrary.** `(0.7359, 0.6771)` and `(−0.7359, −0.6771)` describe the *same axis*, just labelled from opposite ends, and different versions of the library hand you either one. **If a student's plot comes out mirrored, nothing is wrong.** What is never arbitrary is the *relative* signs within one component — flavanoids and nonflavanoid_phenols pulling opposite ways is real.

**PCA has never seen your target column.** It chases spread, and spread is not the same thing as usefulness. Imagine a medical table where 95% of the spread is patients' height and weight and the diagnosis lives in one small blood-test ratio: **PCA to two components will keep the body-size axis and bin the diagnosis.** The only way to know is to test it, which is exactly what Week 30 does.

### 8. The trap: PCA on unscaled columns is worse than useless

**PCA maximises variance, and variance depends on your units.** Measure a length in millimetres instead of metres and its variance goes up by a factor of a million, so PC1 will point straight along it whether or not it matters.

Here is what happens on the raw wine data:

```text
evr first three: [0.9981 0.0017 0.0001]
proline              0.9998
magnesium            0.0179
alcalinity_of_ash   -0.0047
color_intensity      0.0023
```

**PC1 explains 99.81% of the spread, and PC1 is 0.9998 × `proline`.** It is not "dominated by proline". **It is proline, with a rounding error attached.** Twelve chemical measurements were handed to the algorithm and all twelve were discarded, silently, with no error and a magnificent-looking 99.81%.

This is exactly last week's k-means failure in different clothing, and **that parallel is the best thing you can point out today:** k-means unscaled sorted the wine into proline bands; PCA unscaled made proline its first axis. **Same cause, same fix, different algorithm.** Standardise first, always, unless every column is genuinely in the same unit.

### 9. Every new line of this week's code, explained to somebody who has never programmed

**New line 1 — build it and fit it.**

```python
pca = PCA(n_components=2).fit(X)
```

`PCA(n_components=2)` builds a squasher set to keep **two** components, and `.fit(X)` makes it look at the table and work out which two directions those should be. Nothing has been squashed yet — fitting only *finds the directions*. Leave `n_components` out entirely and it keeps all of them, which is what you want when you are printing the full thirteen-row table.

> **💡 Try this:** you can hand `n_components` a fraction instead of a count. `PCA(n_components=0.80)` means *"keep however many components I need for 80% of the spread"*, and on the wine data it keeps **5** — the same answer the running-total table gives by eye.

**New line 2 — the directions themselves.**

```python
pca.components_
```

One row per component, one column per original feature. With 2 components and 13 wine columns it is a (2, 13) grid, and **row 0 holds PC1's thirteen loadings.** The trailing underscore is Week 28's rule: it does not exist until `.fit` has run.

**New line 3 — how much spread each one carries.**

```python
pca.explained_variance_ratio_
```

One number per component, and they add to 1 if you kept all of them. `[0.3620 0.1921]` means PC1 carries 36.20% and PC2 carries 19.21%. **The nearby `pca.explained_variance_` (no `_ratio`) holds the same information unscaled, as actual variances — those add to the number of columns rather than to 1, and confusing the two is this week's most common silent error.**

**New line 4 — squashing, and un-squashing.**

```python
Z = pca.transform(X)                 # (178, 13) becomes (178, 2)
X_back = pca.inverse_transform(Z)    # (178, 2) becomes (178, 13) again
```

`transform` does the projection — every row's thirteen numbers become two. `inverse_transform` pushes those two back out to thirteen, **and what comes back is an approximation, not the original.** The gap between `X` and `X_back` is the whole of §6.

> **⚠️ Watch out:** `inverse_transform` must be handed the **squashed** table, not the original. `pca.inverse_transform(X)` with a 13-column `X` gives a `ValueError` about a mismatch between 2 and 13, and it is the single most common error of the week. **The rule to say out loud: `transform` narrows, `inverse_transform` widens, so whatever went into one comes out of the other.**

And the miss, measured:

```python
miss = np.sqrt(((X - X_back) ** 2).sum(axis=1)).mean()
```

Read it inside out: subtract, square, **add across the columns** (`axis=1` is along a row, which they have known since Week 16), square-root to get one distance per row, then average over the rows. **One number, in the units of `X`.**

### 10. The three misconceptions you will actually meet

**Misconception 1 — "PCA picks the best columns."**
It does not pick columns at all. **Every component is a blend of all thirteen**, which is exactly what `pca.components_` shows: PC1 has thirteen non-zero loadings. **Cure:** print `pca.components_[0]` and count the zeros. There are none.

**Misconception 2 — "98.82% means almost nothing was lost."**
98.82% of the *spread*. **Cure:** the rebuilt point `(12.1592, 10.827)` against the real `(12, 11)`, and on the wine data `2.2550 ÷ 3.5180 = 0.6410`. A respectable-sounding share can come with a very ugly bill.

**Misconception 3 — "the 2-D PCA plot shows me the data."**
It shows you 55.4% of the wine data. **Cure:** two points that look adjacent on the page can be far apart in the other 44.6%. **The fix is a habit, not a calculation: put the explained-variance percentage in every axis label, every time.** The code in this file does that, deliberately.

### 11. How deep to go, and where to stop

**Go this far:** why too many columns is a problem, with the contrast table; variance in four steps by hand; centring first, and why; projection as one multiply-and-add per coordinate; trying six directions and keeping the widest, with the real spreads; PCA's exact answer and how far off the grid was; the two spreads adding back to 18.5; the explained variance ratio and the running total; naming PC1 from its loadings; reconstruction error and the ratio against a typical distance; and the unscaled disaster.

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| **Eigenvectors, eigenvalues, covariance matrices, determinants** | **Not in this level, at all.** If asked how sklearn gets the exact angle: *"there is a formula for it, it needs maths you will meet at university, and it gives the same answer as a very fine grid — 43 degrees gets you to 18.2804 against the exact 18.2812."* **That is a complete and honest answer. Do not improve on it.** |
| The dot product, by name | **Week 32**, on cosine similarity. Today it is *"multiply each coordinate by the matching number in the direction, and add"*, which is the same arithmetic without the name. |
| Drawing the wine clusters on the PCA map | **Week 30.** Today's wine plot is uncoloured on purpose — there are no clusters on it yet. |
| Silhouette, ARI, choosing `k` | **Week 30.** |
| t-SNE, UMAP, autoencoders | Not in this level. One sentence if asked: *"there are newer methods that make prettier pictures and are much harder to interpret; PCA is the one you can explain."* |
| Whitening, kernel PCA, sparse PCA | Not in this level. |
| PCA inside a `Pipeline` to avoid leakage | **Week 30**, where it matters because a supervised model is being scored. Today nothing is being scored, so nothing can leak. **If a student raises it, praise them loudly and say "next week".** |

The line to hold in your head all lesson: **today the student turns thirteen columns into two, and prices the transaction.**

---

### 12. 🧭 The Growing Map — the same box, the second of six weeks

The student guide carries a figure called **Where This Fits**: the same picture every week with one more
piece filled in. This week nothing on it moves, and the two minutes are spent on why a tile six weeks
wide is a tile and not six tiles.

![The Level 3 pipeline in Week 29: still the no labels and words tile, now a new pair of axes](../figures/fig-w29-0-where-this-fits.svg)

*Figure 29.0 — Week 29's version. Second week inside the gold `no labels · words` tile. The ↻ on stage
three is black, as it has been since Week 12.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Ask "which box did we do today?" and then "which half of its name?"** Same gold tile as last week.
   The tile says *no labels · words*, and this week is still firmly in **no labels** — PCA never saw a
   `y` either. Words start in Week 31. Naming which half they are in stops the tile feeling like a
   six-week blur.
2. **Anchor it on the two spreads on the board.** The class's 30° grid found **17.4192**; PCA found
   **18.2812**. *"Our answer was twelve degrees short and we can say by how much. That is what the box is
   for — not a formula, a direction and a price."* Then the price itself: two components keep 55.4% of
   the spread and miss a typical wine by `2.2550`. **A student who can quote the brochure and the invoice
   has understood this week.**
3. **Point at stage one and at Week 28's box.** Stage one, because unscaled PCA gave `0.9981` on the
   first component and meant nothing at all — the same `proline` problem as last week, one box to the
   left. And at Week 28's tile, because *"last week we could not see whether the clusters were real.
   Now we can draw them, and next week we decide."*

> **🧑‍🏫 Why this is worth two minutes.** PCA is the week where a student most easily believes they have
> fallen behind, because the name sounds like university mathematics and the lesson was a protractor.
> The map answers that without argument: **this is one tile, in the same row as everything else, and you
> are inside it.** It also sets up Week 30 honestly — nothing was scored today, so nothing could be
> judged, and next week is where the scoring arrives.

**One thing to notice, so you can answer if asked.** `data` is lit beside `representation`, and the
reason is the reconstruction error rather than the projection. Re-describing a row in two numbers is
representation. **Measuring what the re-description destroyed, in the table's own units, is a fact about the
data** — and it is the half of PCA that nearly every tutorial leaves out.

---

## 🧰 Prep Checklist

### 25 minutes the night before

- [ ] **Do the variance four-step on paper**, on 4, 6, 8, 10, 12. **Two minutes, and you are going to lead it.** Distances −4, −2, 0, 2, 4. Squares 16, 4, 0, 4, 16. Total 40. `40 ÷ 4 = 10.0`.
- [ ] **Project one point by hand, at 30°.** `4 × 0.86603 + 4 × 0.50000 = 3.46410 + 2.00000 = 5.46410`. **You need to be able to do this at the board without looking**, because every student is about to do five of them.
- [ ] **Type and run `new_axes.py` yourself.** The complete file:

```python
"""new_axes.py - Week 29: find the direction of most spread, then use it."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

np.random.seed(0)
np.set_printoptions(suppress=True)

# ---------- 1. variance, by hand, on five numbers ----------
v = np.array([4., 6., 8., 10., 12.])
print("five numbers:", v, "  mean =", v.mean())
print("distance from the mean :", v - v.mean())
print("each one squared       :", (v - v.mean()) ** 2)
print("added up               :", ((v - v.mean()) ** 2).sum())
print("divided by 5           :", ((v - v.mean()) ** 2).sum() / 5)
print("divided by 4 (what sklearn does):", ((v - v.mean()) ** 2).sum() / 4)

# ---------- 2. five points, centred ----------
D = np.array([[4., 3.], [6., 6.], [8., 7.], [10., 8.], [12., 11.]])
print()
print("five students (hours studied, hours slept):", D.tolist())
print("the middle of the cloud:", D.mean(axis=0))
C = D - D.mean(axis=0)
print("moved so the middle is (0,0):", C.tolist())

# ---------- 3. try six directions, keep the widest ----------
print()
print("--- six candidate axes, 30 degrees apart ---")
print(" angle   direction (across, up)     the five scores along it              spread")
best_angle, best_spread = None, -1.0
for a in range(0, 180, 30):
    u = np.array([np.cos(np.radians(a)), np.sin(np.radians(a))])
    scores = C @ u
    spread = (scores ** 2).sum() / 4
    print(" %3d°   (%7.4f, %7.4f)   %s  %7.4f"
          % (a, u[0], u[1], np.array2string(np.round(scores, 3), precision=3,
                                            floatmode="fixed"), spread))
    if spread > best_spread:
        best_angle, best_spread = a, spread
print("widest of the six: %d° with spread %.4f" % (best_angle, best_spread))

# ---------- 4. what PCA says ----------
pca = PCA().fit(D)
print()
print("pca.components_:")
print(np.round(pca.components_, 4))
print("PC1's angle: %.2f°" % np.degrees(np.arctan2(pca.components_[0][1],
                                                    pca.components_[0][0])))
print("pca.explained_variance_      :", np.round(pca.explained_variance_, 4))
print("pca.explained_variance_ratio_:", np.round(pca.explained_variance_ratio_, 4))
print("the two spreads add to:", round(pca.explained_variance_.sum(), 4),
      "= 10.0 + 8.5, the spread of the two original columns")

# ---------- 5. squash to one number, then rebuild ----------
p1 = PCA(n_components=1).fit(D)
Z = p1.transform(D)
back = p1.inverse_transform(Z)
print()
print("one number per student:", np.round(Z.ravel(), 4))
print("rebuilt from that one number:")
print(np.round(back, 4))
print("the real points:")
print(D)
err = np.sqrt(((D - back) ** 2).sum(axis=1))
print("how far each rebuilt point is from the real one:", np.round(err, 4))
print("average miss: %.4f hours" % err.mean())

# ---------- 6. thirteen wine columns ----------
print()
wine = load_wine()
X_raw = pd.DataFrame(wine.data, columns=wine.feature_names)
X = StandardScaler().fit_transform(X_raw)
full = PCA().fit(X)
evr = full.explained_variance_ratio_
print("PC   its share   running total")
for i, share in enumerate(evr, start=1):
    print("%2d     %.4f       %.4f" % (i, share, evr[:i].sum()))

p2 = PCA(n_components=2).fit(X)
print()
pull1 = pd.Series(p2.components_[0], index=wine.feature_names)
print("PC1: which original columns pull hardest")
print(pull1.reindex(pull1.abs().sort_values(ascending=False).index)
      .round(3).head(5).to_string())
pull2 = pd.Series(p2.components_[1], index=wine.feature_names)
print()
print("PC2: which original columns pull hardest")
print(pull2.reindex(pull2.abs().sort_values(ascending=False).index)
      .round(3).head(5).to_string())

print()
print("  how many PCs   running share   average rebuild miss")
for m in (1, 2, 3, 5, 6, 8, 13):
    p = PCA(n_components=m).fit(X)
    Xh = p.inverse_transform(p.transform(X))
    miss = np.sqrt(((X - Xh) ** 2).sum(axis=1)).mean()
    print("      %2d           %.4f            %.4f"
          % (m, p.explained_variance_ratio_.sum(), miss))
print("for scale: a typical wine sits %.4f away from the middle"
      % np.sqrt((X ** 2).sum(axis=1)).mean())

Z2 = p2.transform(X)
plt.figure(figsize=(6.5, 5))
plt.scatter(Z2[:, 0], Z2[:, 1], s=30, alpha=0.85)
plt.xlabel("PC1 (%.1f%% of the spread)" % (evr[0] * 100))
plt.ylabel("PC2 (%.1f%% of the spread)" % (evr[1] * 100))
plt.title("178 wines, 13 columns squashed to 2")
plt.tight_layout()
plt.savefig("wine_2d.png", dpi=110)
plt.close()
print("saved wine_2d.png")
```

Run `python3 new_axes.py`. You must see **exactly** this:

```text
five numbers: [ 4.  6.  8. 10. 12.]   mean = 8.0
distance from the mean : [-4. -2.  0.  2.  4.]
each one squared       : [16.  4.  0.  4. 16.]
added up               : 40.0
divided by 5           : 8.0
divided by 4 (what sklearn does): 10.0

five students (hours studied, hours slept): [[4.0, 3.0], [6.0, 6.0], [8.0, 7.0], [10.0, 8.0], [12.0, 11.0]]
the middle of the cloud: [8. 7.]
moved so the middle is (0,0): [[-4.0, -4.0], [-2.0, -1.0], [0.0, 0.0], [2.0, 1.0], [4.0, 4.0]]

--- six candidate axes, 30 degrees apart ---
 angle   direction (across, up)     the five scores along it              spread
   0°   ( 1.0000,  0.0000)   [-4.000 -2.000  0.000  2.000  4.000]  10.0000
  30°   ( 0.8660,  0.5000)   [-5.464 -2.232  0.000  2.232  5.464]  17.4192
  60°   ( 0.5000,  0.8660)   [-5.464 -1.866  0.000  1.866  5.464]  16.6692
  90°   ( 0.0000,  1.0000)   [-4.000 -1.000  0.000  1.000  4.000]   8.5000
 120°   (-0.5000,  0.8660)   [-1.464  0.134  0.000 -0.134  1.464]   1.0808
 150°   (-0.8660,  0.5000)   [ 1.464  1.232  0.000 -1.232 -1.464]   1.8308
widest of the six: 30° with spread 17.4192

pca.components_:
[[ 0.7359  0.6771]
 [-0.6771  0.7359]]
PC1's angle: 42.62°
pca.explained_variance_      : [18.2812  0.2188]
pca.explained_variance_ratio_: [0.9882 0.0118]
the two spreads add to: 18.5 = 10.0 + 8.5, the spread of the two original columns

one number per student: [-5.652  -2.1489  0.      2.1489  5.652 ]
rebuilt from that one number:
[[ 3.8408  3.173 ]
 [ 6.4187  5.545 ]
 [ 8.      7.    ]
 [ 9.5813  8.455 ]
 [12.1592 10.827 ]]
the real points:
[[ 4.  3.]
 [ 6.  6.]
 [ 8.  7.]
 [10.  8.]
 [12. 11.]]
how far each rebuilt point is from the real one: [0.2351 0.6183 0.     0.6183 0.2351]
average miss: 0.3414 hours

PC   its share   running total
 1     0.3620       0.3620
 2     0.1921       0.5541
 3     0.1112       0.6653
 4     0.0707       0.7360
 5     0.0656       0.8016
 6     0.0494       0.8510
 7     0.0424       0.8934
 8     0.0268       0.9202
 9     0.0222       0.9424
10     0.0193       0.9617
11     0.0174       0.9791
12     0.0130       0.9920
13     0.0080       1.0000

PC1: which original columns pull hardest
flavanoids                      0.423
total_phenols                   0.395
od280/od315_of_diluted_wines    0.376
proanthocyanins                 0.313
nonflavanoid_phenols           -0.299

PC2: which original columns pull hardest
color_intensity    0.530
alcohol            0.484
proline            0.365
ash                0.316
magnesium          0.300

  how many PCs   running share   average rebuild miss
       1           0.3620            2.7527
       2           0.5541            2.2550
       3           0.6653            1.9581
       5           0.8016            1.5303
       6           0.8510            1.3258
       8           0.9202            0.9599
      13           1.0000            0.0000
for scale: a typical wine sits 3.5180 away from the middle
saved wine_2d.png
```

**Expected runtime: about 1.7 seconds**, including saving the PNG.

- [ ] **Break it on purpose, twice**, and keep both outputs where you can see them. First the loud one:

```python
p = PCA(n_components=2).fit(X)
p.inverse_transform(X)
```

```text
ValueError: matmul: Input operand 1 has a mismatch in its core dimension 0, with gufunc signature (n?,k),(k,m?)->(n?,m?) (size 2 is different from 13)
```

Then the silent one:

```python
pu = PCA().fit(X_raw)                       # NOT scaled
print(np.round(pu.explained_variance_ratio_[:3], 4))
```

```text
[0.9981 0.0017 0.0001]
```

**99.81% on the first component, and it is proline.** That is deliberate mistake two and it is the best thirty seconds of the live-code.

- [ ] **Print the whole workbook (`workbook/week-29.md`), every section from Warm-Up to Self-Check.** The lesson's own cloud is worked on graph paper, not in the workbook.
- [ ] **Get real graph paper, a ruler and a protractor for every student.** **This is the one prep item that cannot be improvised on the day.** The activity is drawing six axes at 30° steps through a cloud and measuring along them, and on plain paper it does not work at all. **Borrow protractors from the maths department this week, not on Monday morning.**
- [ ] **Put up the SPREAD sheet.** A big blank number line from 0 to 20, with room to plot six dots — one per candidate angle. It gets filled in live and the winner is obvious the moment the sixth dot goes on.
- [ ] **Write the six candidate directions on the board before class**, because looking up six cosines mid-lesson kills the pace:

```text
  0° : (1.0000, 0.0000)         90° : (0.0000, 1.0000)
 30° : (0.8660, 0.5000)        120° : (−0.5000, 0.8660)
 60° : (0.5000, 0.8660)        150° : (−0.8660, 0.5000)
```

- [ ] **Leave the SIX POINTS sheet from Week 28 up.** It comes down at the end of Week 30.

### 10 minutes on the day

- [ ] Graph paper, ruler, protractor on every desk.
- [ ] The six directions on the board, and the SPREAD number line blank on the wall.
- [ ] Editor open, `new_axes.py` **empty** — they type sections 1 to 4 with you.
- [ ] Scrap paper out for the pen vote. **The prediction — which angle will win — written in pen, before anything is measured.** (The workbook's Build It predictions are a separate set, done at home.)
- [ ] Bug Log out.
- [ ] Six slips of paper with one angle written on each, for handing out in the activity.

### Fallback if the laptops fail

**This week is the second-best week of the year for a power cut, after last week.** Three of the four objectives are pencil-and-protractor work by design.

1. **Variance, on the board.** Four steps, five numbers, `40 ÷ 4 = 10.0`. **Objective 1, complete.**
2. **The Spaghetti Cloud activity, unchanged.** Graph paper, protractor, six angles, five projections each, and the winning spread. **Objective 2, complete, and it was never going to be done on a computer anyway.**
3. **Reconstruction, from this file's numbers.** Give them the rebuilt points `(3.8408, 3.173)` … `(12.1592, 10.827)` and the real ones, and have them compute the five misses and the average. **Objective 4, complete, with a calculator.**
4. **The casualty is objective 3** — the thirteen wine components. Print the table from this file and they can *read* it, which gets most of the way there. Say so: *"the bit we cannot do today is watch thirteen columns collapse into two. The table is on your sheet and the plot is your homework."*

| If this fails | Do this instead |
|---|---|
| Nobody has a protractor | **Pre-print the six axes** on the graph paper before class — six faint lines through the centre at 30° steps. The measuring still works; only the drawing is lost. |
| A student's spread does not match the table | Check three things in order: **did they centre the points first?** (the single most common miss), **did they square before adding?**, **did they divide by 4 and not 5?** It is almost always the first one. |
| The class's winner comes out as 60° rather than 30° | Somebody has mixed up which number is across and which is up. `30°` is mostly-across, `60°` is mostly-up. **Draw both on the board and look at them.** |
| Somebody objects that 42.62° is not on our grid so our answer is wrong | **They are completely right and this is the best objection of the lesson.** *"Our answer is the best of six. PCA's is the best of all of them. Ours was 12.62 degrees short and it cost us 0.8620 of spread. What would you do about it?"* **Finer grid.** Then show them 43° → 18.2804. |
| The wine plot is an unlabelled blob and nobody cares | **Put the percentages in the axis labels and say the sentence:** *"this picture is 55.4% of the wine data. The other 44.6% is not on this page."* The blob is not the point; the percentage is. |
| `explained_variance_` and `explained_variance_ratio_` get mixed up | Print both, side by side, once. `[4.7324 2.5111]` against `[0.3620 0.1921]`. **One adds to the number of columns; one adds to 1.** |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Photograph the Midges | 7 | 7 | 13 columns you cannot see; the cloud from two angles |
| 🧠 Concept & Maths — Spread, and How To Measure It Along a Line | 18 | 25 | Variance in four steps; centring; projection as multiply-and-add |
| 💻 Live-Code Together — `new_axes.py` | 18 | 43 | Six angles; PCA's answer; rebuild. **Two deliberate mistakes.** |
| 🎲 Their Turn — The Spaghetti Cloud | 20 | 63 | Six angles by protractor, one each, widest wins |
| 🔑 Wrap & Assign | 7 | 70 | 13 to 2, the promise and the bill, three checks |

---

### 🪝 Hook — Photograph the Midges (7 minutes)

**Do this:** Put the wine table's shape on the screen and nothing else.

```text
wine table: (178, 13)
```

**Say this:**

> "One hundred and seventy-eight bottles of wine, thirteen chemical measurements each. Last week we clustered them and it worked, and there was one thing we never did: **we never looked at them.**
>
> So — draw me thirteen dimensions."

**Ask this:** "How would you draw a picture of thirteen columns?"

*Let them try. Somebody will suggest lots of scatter plots.*

> "You could do every pair of columns: that is seventy-eight scatter plots, and nobody is reading seventy-eight of anything.
>
> So you have to throw something away. And the obvious idea is: **pick the two best columns and plot those.**"

**Ask this:** "What is wrong with picking the two best columns?"

*Take answers. Steer towards: you throw away the other eleven, and the useful information might be spread across all of them.*

> "**Eleven columns in the bin, and you have no idea whether what mattered was in them.** So here is the other idea, and it is today's lesson."

**Do this:** Draw on the board a long thin diagonal cloud of about twelve dots, leaning up to the right. Then draw **two viewing arrows**: one looking along its length, one looking across it.

**Say this:**

> "A long thin cloud of midges hanging over a garden, and you want to photograph it.
>
> **Camera one** — stand at the end and shoot along the length." Draw what you see: a small blob. "You get that. A blob. Every midge on top of every other midge. You have lost almost everything.
>
> **Camera two** — stand off to the side." Draw a long streak. "A streak. You can see the whole shape, and you can tell which midge is which."

**Ask this:** "Which photo is better, and why?"

*Hoped-for:* the streak, because you can still tell the midges apart.

> "**The streak, because it keeps the differences.** And that is the whole idea. **Spread is where the information is.** A column where everything is the same number tells you nothing; a column where the rows are miles apart tells you a lot.
>
> So: instead of picking two of your thirteen columns, you go looking for **the angle that gives the longest streak.** You make a brand new axis, pointing whichever way the data is most spread out, and you measure everything against that instead.
>
> That is called **PCA**, and by the end of today you will have found one with a protractor."

**Do this:** Write on the board and leave it up all lesson:

```text
PCA does not delete columns.
It draws a new axis along the direction the data is most spread out.
```

**Say this:**

> "One more reason to care, and it is about last week. k-means works entirely by asking 'which centre is nearest'. **In lots of columns, everything is about the same distance from everything.** I measured it: with 500 columns, the furthest-apart pair of points in a dataset is only **21% further apart** than the closest pair. Nothing is near anything. **k-means goes blind.**
>
> So cutting thirteen columns down to two is not just so we can draw it. It can help distance mean something again, when the real structure is low-dimensional. (The table is for random points, where no direction is special, so PCA could not help there; and two wine components keep only 55% of the spread, so two-column distances are distorted.)"

---

### 🧠 Concept & Maths — Spread, and How To Measure It Along a Line (18 minutes)

**Do this:** Write five numbers on the SPREAD sheet.

```text
4    6    8    10    12
```

**Say this:**

> "Before we can find the most spread-out direction, we need a number for how spread out something is. You have most of this already — it is the standard deviation from Week 4, one step earlier."

**Do this:** Write the definition and box it.

> **Variance** — the average squared distance from the mean.

**Do this:** Walk the four steps, writing each row under the last.

**Ask this:** "Mean of those five?"

*8.*

```text
step 1, how far off :  −4    −2     0    +2    +4
```

**Ask this:** "Add those five up."

*0.*

> "**Zero. And it will be zero every single time, for any set of numbers at all**, because the mean is exactly the place where the distances cancel. So as a measure of spread, that is useless. We need to get rid of the minus signs."

**Ask this:** "How do we get rid of a minus sign?"

*Square it. (Somebody may say absolute value — say "that also works, and gives a different measure people do use".)*

```text
step 2, squared     :  16     4     0     4    16
step 3, add up      :  16 + 4 + 0 + 4 + 16 = 40
step 4, average     :  40 ÷ 4 = 10.0
```

**Ask this:** "There are five numbers. Why did I divide by 4?"

*Let them object. Then be honest:*

> "**Because that is the convention scikit-learn uses, and there are two conventions.** Divide by 5 and you get 8.0, which is the spread of exactly these five numbers. Divide by 4 and you get 10.0, which is the estimate you use when your five numbers are a *sample* of something bigger. It comes out slightly larger to allow for the fact that you worked the mean out from the same five numbers.
>
> **I am telling you because the library's number will be 10.0 and I do not want you to think you got it wrong.** It is not a deep thing."

**Do this:** Now the five points. Put them on the board.

```text
(4, 3)   (6, 6)   (8, 7)   (10, 8)   (12, 11)
```

> "Five students. Hours studied, and hours slept, per week. **Step one, and skipping it is the most common mistake in the whole topic: move the middle of the cloud to (0, 0).**"

**Ask this:** "Mean of the across-values? Mean of the up-values?"

*8 and 7.*

```text
centred:  (−4, −4)   (−2, −1)   (0, 0)   (2, 1)   (4, 4)
```

**Ask this:** "Why bother? The cloud has not changed shape."

*Hoped-for:* because we care about spread, not position.

> "**Exactly. PCA is about spread, not about where the cloud is sitting.** Move the whole thing ten units to the left and it is just as spread out. Centring means we can forget about position entirely."

**Do this:** Now projection. Draw the centred cloud with a line through the origin at about 30°, and drop a perpendicular from one point onto it.

> **Projection** — sliding a point sideways onto a line, at right angles, and reading off how far along it landed.

**Say this:**

> "A **direction** is just a pair of numbers: how far across and how far up you go in one step, with the step being exactly one unit long. At 30 degrees, one step is 0.8660 across and 0.5000 up.
>
> And projecting a point onto that direction is one multiply-and-add per coordinate. **You did exactly this arithmetic by hand in Week 17, when you worked out one cell of a matrix multiply.**"

**Do this:** Work it on the board, slowly.

```text
the point (4, 4), on the 30° direction (0.86603, 0.50000):

      4 × 0.86603   +   4 × 0.50000
    = 3.46410       +   2.00000
    = 5.46410
```

**Ask this:** "Two numbers went in. How many came out?"

*One.*

> "**One. That is the squash.** And that single number is everything this axis knows about that student."

**Do this:** Do the other four fast, or have the class call them out.

```text
(−4, −4) → −5.46410      (−2, −1) → −2.23205      (0, 0) → 0
( 2,  1) →  2.23205      ( 4,  4) →  5.46410
```

**Ask this:** "Now — how spread out are those five scores? What do we do?"

*The four steps.*

```text
squares :  29.85641   4.98205   0   4.98205   29.85641
add up  :  69.67691
÷ 4     :  17.41923
```

**Do this:** Put a dot at 17.4 on the SPREAD number line and label it `30°`.

**Say this:**

> "**17.42 at thirty degrees.** One dot on that line. Now — is that good? **You have absolutely no idea, and neither do I, because there is nothing to compare it with.**
>
> Which is exactly what we are going to do about it. Six angles. Six dots on that line. **The widest one wins, and that is the principal component.**"

**Ask this:** "Before we measure. Which of the six do you think will win? 0, 30, 60, 90, 120 or 150?"

*Take a vote, and have them write it in pen on their scrap paper. Most will say 30 or 60.*

> "Write it in pen. **And notice what 0 degrees and 90 degrees are** — 0 degrees is straight along the 'hours studied' axis, so its spread is just the variance of that column. 90 degrees is 'hours slept'. **Your two original columns are two of the six candidates.** If one of them wins, PCA had nothing to offer you. If neither does — and neither will — then there is a better axis than any column you were given."

---

### 💻 Live-Code Together — `new_axes.py` (18 minutes)

**Step 1 — variance and centring (4 minutes).**

```python
import numpy as np
np.set_printoptions(suppress=True)

v = np.array([4., 6., 8., 10., 12.])
print("distance from the mean :", v - v.mean())
print("each one squared       :", (v - v.mean()) ** 2)
print("added up               :", ((v - v.mean()) ** 2).sum())
print("divided by 4           :", ((v - v.mean()) ** 2).sum() / 4)

D = np.array([[4., 3.], [6., 6.], [8., 7.], [10., 8.], [12., 11.]])
C = D - D.mean(axis=0)
print("centred:", C.tolist())
```

```text
distance from the mean : [-4. -2.  0.  2.  4.]
each one squared       : [16.  4.  0.  4. 16.]
added up               : 40.0
divided by 4           : 10.0
centred: [[-4.0, -4.0], [-2.0, -1.0], [0.0, 0.0], [2.0, 1.0], [4.0, 4.0]]
```

> "Those four printed lines are the four steps on the board, in order. **Nothing has been hidden.**"

**Step 2 — the six angles (5 minutes).**

```python
for a in range(0, 180, 30):
    u = np.array([np.cos(np.radians(a)), np.sin(np.radians(a))])
    scores = C @ u
    print("%3d deg  (%7.4f, %7.4f)  spread %7.4f" % (a, u[0], u[1], (scores ** 2).sum() / 4))
```

```text
  0 deg  ( 1.0000,  0.0000)  spread 10.0000
 30 deg  ( 0.8660,  0.5000)  spread 17.4192
 60 deg  ( 0.5000,  0.8660)  spread 16.6692
 90 deg  ( 0.0000,  1.0000)  spread  8.5000
120 deg  (-0.5000,  0.8660)  spread  1.0808
150 deg  (-0.8660,  0.5000)  spread  1.8308
```

**Do this:** Put all six dots on the SPREAD number line, in order, as they appear.

**Ask this:** "Who voted 30? Who voted 60? **30 wins, 17.4192 against 16.6692.**"

**Ask this:** "Look at 120 and 150 — spreads of 1.08 and 1.83. What are those directions doing?"

*Hoped-for:* looking across the cloud instead of along it.

> "**They are camera one. Shooting down the length of the midge cloud and getting a blob.** 1.08 against 17.42 — sixteen times less spread, from the same five points, purely by standing somewhere else."

**Ask this:** "And 0 degrees gave 10.0, 90 gave 8.5. What are those two numbers?"

*The variances of the two original columns.*

> "**Which means three of our six candidates (0, 30 and 60 degrees) beat 'hours slept' on its own, and two of them (30 and 60) beat 'hours studied'.** There was a better axis available than either column we were handed, and nobody had to collect any new data."

**Step 3 — what PCA says (4 minutes).**

```python
from sklearn.decomposition import PCA
pca = PCA().fit(D)
print("components_:\n", np.round(pca.components_, 4))
print("angle of PC1: %.2f degrees" % np.degrees(np.arctan2(pca.components_[0][1],
                                                          pca.components_[0][0])))
print("explained_variance_      :", np.round(pca.explained_variance_, 4))
print("explained_variance_ratio_:", np.round(pca.explained_variance_ratio_, 4))
```

```text
components_:
 [[ 0.7359  0.6771]
 [-0.6771  0.7359]]
angle of PC1: 42.62 degrees
explained_variance_      : [18.2812  0.2188]
explained_variance_ratio_: [0.9882 0.0118]
```

**Ask this:** "We said 30 degrees with a spread of 17.4192. It says 42.62 degrees with 18.2812. **Were we wrong?**"

*Let them argue. The honest answer is: no, we were the best of six.*

> "**We were not wrong. We were coarse.** We were twelve and a bit degrees short, and it cost us `18.2812 − 17.4192 = 0.8620` of spread."

**Ask this:** "So what would you do about it?"

*Hoped-for:* try more angles.

> "**A finer grid.** Every whole degree from 0 to 179, and the best comes out at 43 degrees with a spread of **18.2804** — which is within a thousandth of the exact answer. **sklearn has a formula that goes straight there, and it needs maths you will meet at university. The formula gives the same answer your protractor is about to give, only faster.**"

**Do this:** Now the check that matters most. Write it on the board.

```text
18.2812 + 0.2188 = 18.5000
    10.0 +   8.5 = 18.5000
```

**Ask this:** "The top line is the spread along the two new axes. The bottom line is the spread of the two columns we started with. What do you notice?"

*They're the same.*

> "**The total spread did not change. It got redistributed.** PCA did not create spread out of nothing and it did not destroy any. It **rotated the axes** so that nearly all of the spread piled onto the first one — 98.82% of it. That is the whole trick, and it is why it is called a rotation and not a compression."

**Step 4 — squash, rebuild, and a loud mistake (5 minutes).**

```python
p1 = PCA(n_components=1).fit(D)
Z = p1.transform(D)
print("one number per student:", np.round(Z.ravel(), 4))
back = p1.inverse_transform(D)
```

> **🧑‍🏫 Deliberate mistake one.** That last line is wrong. **Run it.**

```text
ValueError: matmul: Input operand 1 has a mismatch in its core dimension 0, with gufunc signature (n?,k),(k,m?)->(n?,m?) (size 1 is different from 2)
```

**Ask this:** "It says **1 is different from 2**. Where is the 1 from, and where is the 2 from?"

*Hoped-for, after a moment: the 1 is how many components we kept, and the 2 is how many columns the data has.*

> "**It is a shape mismatch, and you have been reading these since Week 25.** `inverse_transform` widens — it expects the **squashed** table, one number per row, and hands back the wide one. I gave it the wide one. **The rule: `transform` narrows, `inverse_transform` widens, so whatever came out of one goes into the other.**"

**Do this:** Fix it in front of them.

```python
back = p1.inverse_transform(Z)
print(np.round(back, 4))
err = np.sqrt(((D - back) ** 2).sum(axis=1))
print("each miss:", np.round(err, 4))
print("average miss: %.4f hours" % err.mean())
```

```text
[[ 3.8408  3.173 ]
 [ 6.4187  5.545 ]
 [ 8.      7.    ]
 [ 9.5813  8.455 ]
 [12.1592 10.827 ]]
each miss: [0.2351 0.6183 0.     0.6183 0.2351]
average miss: 0.3414 hours
```

**Ask this:** "The last student really was (12, 11). We rebuilt them as (12.1592, 10.827). **Is that a disaster?**"

*No — a sixth of an hour out.*

> "**98.82% of the spread kept, and it cost a fifth of an hour per student.** That number has a name: **reconstruction error**, and it is the honest price tag. Explained variance is the brochure. **This is the invoice.**"

**Ask this:** "One student came back exactly right — (8, 7), miss 0.0000. Which one is it and why?"

*Hoped-for:* the middle one / the one at the mean.

> "**It is the student sitting at the mean, and the mean is the one point that a single axis can always place perfectly**, because it is where the axis crosses."

**Step 5 — the silent mistake, on the wine (if time; otherwise move it to the wrap).**

```python
from sklearn.datasets import load_wine
import pandas as pd
wine = load_wine()
X_raw = pd.DataFrame(wine.data, columns=wine.feature_names)
pu = PCA().fit(X_raw)
print("first three shares:", np.round(pu.explained_variance_ratio_[:3], 4))
```

```text
first three shares: [0.9981 0.0017 0.0001]
```

> **🧑‍🏫 Deliberate mistake two.** **Be delighted.** *"99.81% of thirteen columns of wine chemistry, captured in a single number! We have squashed thirteen columns into one and lost almost nothing!"* **Let it sit.**

```python
s = pd.Series(pu.components_[0], index=wine.feature_names)
print(s.reindex(s.abs().sort_values(ascending=False).index).round(4).head(3).to_string())
```

```text
proline              0.9998
magnesium            0.0179
alcalinity_of_ash   -0.0047
```

**Ask this:** "What is PC1?"

*It's proline.*

> "**It is proline. 0.9998 of proline and a rounding error.** Twelve chemical measurements handed in, twelve discarded, no error message, and a 99.81% that looks like a triumph.
>
> **And you saw this exact failure last week.** Unscaled k-means sorted the wine into proline bands. Unscaled PCA made proline its first axis. **Same cause — one column with a spread of 314.91 while the next biggest is 14.28 and most of the rest are under 3 — same fix.** Scale first. Always."

---

### 🎲 Their Turn — The Spaghetti Cloud (20 minutes)

Full instructions in **🎲 The Activity, In Full** below. In outline: **five points plotted on graph paper**, six candidate axes drawn through the middle at 30° steps with a protractor, and **one angle assigned to each student.** Everybody projects all five points onto their own axis by hand, computes the spread with the four steps, and brings one number to the SPREAD sheet. **The widest wins.** Then `pca.components_` is printed and the class compares its angle with the winner's.

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Put the thirteen-row table on the screen and put a finger on the running-total column.

```text
PC   its share   running total
 1     0.3620       0.3620
 2     0.1921       0.5541
 3     0.1112       0.6653
 4     0.0707       0.7360
 5     0.0656       0.8016
```

**Ask this:** "If I want to keep 80% of the spread in the wine data, how many components do I need?"

*Five — 0.8016 at PC5.*

**Ask this:** "And how many do I need if I want to draw a picture?"

*Two.*

**Ask this:** "How much of the wine data is on a two-dimensional picture?"

```text
0.3620 + 0.1921 = 0.5541
```

*55.41%.*

> "**Just over half.** Which means two wines that look like they are sitting on top of each other on that plot **can be miles apart in the other 44.6%.**
>
> So here is a habit, and it is not optional: **put the percentage in the axis label. Every single time you draw a PCA plot.** Not because it is tidy. Because a picture is convincing, and this one is only 55% true, and your reader cannot tell unless you tell them."

**Do this:** Now the bill. Write both numbers side by side.

```text
2 components:   share kept 0.5541      average miss 2.2550
a typical wine sits 3.5180 from the middle
2.2550 ÷ 3.5180 = 0.6410
```

**Ask this:** "'We kept 55% of the spread' and 'our rebuilt wine is wrong by 64% of a typical distance'. **Which of those two sentences is true?**"

*Hoped-for:* both.

> "**Both. Same run, same two numbers, opposite feelings.** And the one people put in their report is always the first one.
>
> So: **report both.** Explained variance is what you gained. Reconstruction error is what it cost. **A report with only the gain in it is a sales brochure, and you have spent twenty-nine weeks learning not to write those.**"

**Do this:** Three quick checks — exact wording in **✅ Assessing Understanding**.

**Say this, to close:**

> "Today you found a principal component with a protractor. You tried six directions, measured the spread along each one, and kept the widest — and your answer was twelve degrees off the exact one, which you then worked out how to fix.
>
> And the thing I want you to take away: **PCA did not throw away any of your columns.** It made new axes out of all of them. `pca.components_[0]` has thirteen numbers in it, not two.
>
> Next week we put this week and last week together. You will have clusters, and you will have a map to draw them on, and the job will be: **give each cluster a name a human being can act on, and produce two independent pieces of evidence that the clusters are real.**"

**Do this:** Hand out the homework and read the third part out loud, slowly.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `ValueError: matmul: Input operand 1 has a mismatch in its core dimension 0, with gufunc signature (n?,k),(k,m?)->(n?,m?) (size 2 is different from 13)` | "You handed the widener a wide table." | `pca.inverse_transform(X)` instead of `pca.inverse_transform(Z)`. | **`transform` narrows, `inverse_transform` widens.** Whatever came out of one goes into the other. **The two numbers in the message are your component count and your column count — read them.** |
| `ValueError: n_components=14 must be between 0 and min(n_samples, n_features)=13 with svd_solver='covariance_eigh'` | "You asked for more axes than the data can have." | `n_components` bigger than the number of columns. | You can never have more components than columns (or than rows, if you have fewer rows than columns). **There is no fourteenth direction in a thirteen-column table.** |
| `AttributeError: 'PCA' object has no attribute 'components_'` | "You never ran it." | `PCA(n_components=2)` built, `.fit(X)` never called. | Add `.fit(X)`. **Week 28's rule and it has not changed: a name ending in `_` does not exist until `.fit` has run.** |
| `AttributeError: 'PCA' object has no attribute 'components_'` — raised from inside `transform` | "You tried to squash before finding the directions." | `PCA(n_components=2).transform(X)` with no `.fit`. | `.fit_transform(X)`, or `.fit(X)` then `.transform(X)`. **`transform` needs directions, and fitting is what finds them.** |
| `ValueError: could not convert string to float: 'a'` | "One of your columns is words." | A text column left in the DataFrame. | PCA does arithmetic on every column. Drop it, or encode it as in Week 4. |
| `ValueError: Expected 2D array, got 1D array instead: array=[1. 2. 3. 4.].` | "You gave me a list, not a table." | One flat array instead of rows-by-columns. | `X` must be 2-D. **There are no directions to find in a single column — the answer would be "along it".** |
| **No error. `explained_variance_ratio_[0]` is 0.9981 and you are thrilled.** | Nothing crashed. Your first axis is your biggest column. | No scaling, so the widest-ranging column became PC1 all by itself. | `StandardScaler` first. **The check that finds it: print `pca.components_[0]` with the column names. If one loading is 0.9998 and the rest are under 0.02, you have made an expensive copy of one column.** |
| **No error. `explained_variance_` does not add up to 1 and you assume something is broken.** | Nothing crashed. You printed the wrong one of two very similar names. | `explained_variance_` holds actual spreads; `explained_variance_ratio_` holds shares. | Print both once and keep the difference: `[4.7324 2.5111]` against `[0.3620 0.1921]`. **The shares add to 1; the spreads add to roughly the number of columns.** |
| **No error. Your whole plot is mirrored compared with a friend's.** | Nothing crashed. The sign of a component is arbitrary. | Different sklearn version, or a randomized solver. | **Nothing to fix.** `(0.7359, 0.6771)` and `(−0.7359, −0.6771)` are the same axis read from opposite ends. **What *is* meaningful is the signs *within* one component relative to each other.** |
| **No error. Your spread numbers are all 20% too small.** | Nothing crashed. You divided by the wrong thing. | Dividing by `n` where sklearn divides by `n − 1`, or forgetting to divide at all. | With five points, divide the sum of squares by **4**. **And the diagnostic: if your number is exactly 4/5 (0.8 times) sklearn's, you divided by 5.** |
| **No error. Your spread is much too big for every angle.** | Nothing crashed. You forgot to centre. | Projecting the raw points instead of the centred ones. | Subtract the column means first. **Skipping the centring is the single most common error of this week, and the fingerprint is that every angle gives a huge number dominated by where the cloud sits rather than how big it is.** |

### How to teach debugging without giving the answer

All the old moves stand. This week adds three.

29. **"Did you centre first?"** Ask it before anything else when a projection number is wrong. It is the answer more often than all the others combined.

30. **"Print `components_[0]` next to your column names."** One line, and it tells you instantly whether PCA found a blend of your columns or just made a copy of the biggest one.

31. **"Which of the two nearly-identical names did you print?"** `explained_variance_` or `explained_variance_ratio_`. **When a library gives you two things whose names differ by one word, print both once and write down which is which.**

And the sentence for this week:

> **"A percentage is a claim about spread, not a claim about information. 99.81% sounds like a triumph and was a copy of one column, and the only way you found out was by printing what the axis was made of."**

---

## 🎲 The Activity, In Full

### The Spaghetti Cloud (20 minutes)

**What it is.** Five points on graph paper. Six candidate axes drawn through the middle at 30° steps. **Every student is assigned one angle, projects all five points onto it by hand, and computes its spread.** All six numbers go on the SPREAD sheet, the widest wins, and then `pca.components_` is printed and compared.

**Why it is worth twenty minutes.** PCA's reputation for difficulty is entirely about how it is computed. **A student who has personally measured the spread along 120° and got 1.08, then watched somebody else's 30° get 17.42, understands what a principal component *is* and will never mistake it for column selection.** And the class collectively performs a search, which is exactly what the algorithm does.

### Setup

- **Graph paper, ruler and protractor on every desk.** Not optional.
- **The five points pre-marked, or marked in the first minute**, on a grid with (8, 7) — the cloud's middle — at the centre of the paper:

```text
      up (hours slept)
  11  |                        *
   8  |                  *
   7  |             *
   6  |        *
   3  |   *
      +---------------------------- across (hours studied)
          4    6    8   10   12
```

- **Six slips of paper**, one angle each: `0°`, `30°`, `60°`, `90°`, `120°`, `150°`. With more than six students, hand out duplicates — two people on the same angle is a free check on each other.
- **The six directions on the board**, so nobody is looking up cosines:

```text
  0° : (1.0000, 0.0000)         90° : (0.0000, 1.0000)
 30° : (0.8660, 0.5000)        120° : (−0.5000, 0.8660)
 60° : (0.5000, 0.8660)        150° : (−0.8660, 0.5000)
```

- **The SPREAD number line on the wall**, 0 to 20, blank.
- **A sheet of scrap paper per student** — a five-row projection table and the four variance steps underneath (the workbook has no page for this cloud; its M1 and M2 repeat the method at home on other numbers).

### Step 1 — centre the cloud (3 minutes)

Everybody, together, before any angles:

> **Ask this:** "Mean across? Mean up?"

*8 and 7.*

They write the five centred points on the scrap sheet:

```text
(−4, −4)   (−2, −1)   (0, 0)   (2, 1)   (4, 4)
```

**Do this:** Have them mark the centred points on the graph paper too, with the origin in the middle of the sheet. **The cloud has moved but not changed shape, and they should be able to see that.**

> **Say this:** "If anybody's spread comes out enormous later, this is the step you skipped."

### Step 2 — draw your axis (3 minutes)

Each student draws **their own** angle as a line through the origin with the protractor, right across the paper in both directions. One line each, not six.

> **Say this:** "Zero degrees is straight across. Ninety is straight up. **A hundred and twenty and a hundred and fifty lean backwards** — up and to the left."

**Check the 120° and 150° people before they start measuring.** Those two are where the protractor errors happen, and a wrong line makes every later number wrong.

### Step 3 — project all five points (7 minutes)

Two ways to do it, and **do both**, because the agreement is the point:

**By ruler.** Drop a perpendicular from each point onto the line — a set square helps, or the corner of the protractor — and measure along the line from the origin to where it lands, in grid squares. **Positive one way, negative the other.**

**By arithmetic.** For each point, multiply the across-value by the direction's first number, the up-value by its second, and add.

```text
for the 30° axis, direction (0.8660, 0.5000):

(−4, −4):  −4 × 0.8660  +  −4 × 0.5000  =  −3.4641 + −2.0000  =  −5.4641
(−2, −1):  −2 × 0.8660  +  −1 × 0.5000  =  −1.7321 + −0.5000  =  −2.2321
( 0,  0):   0           +   0           =   0.0000
( 2,  1):   2 × 0.8660  +   1 × 0.5000  =   1.7321 +  0.5000  =   2.2321
( 4,  4):   4 × 0.8660  +   4 × 0.5000  =   3.4641 +  2.0000  =   5.4641
```

> **Say this:** "The ruler and the arithmetic should agree to about a tenth. **If they disagree by a lot, your protractor line is wrong, not your arithmetic.**"

### Step 4 — compute your spread (4 minutes)

The four steps from the board, on their own five scores:

```text
square each   :  29.8564   4.9821   0   4.9821   29.8564
add them up   :  69.6769
divide by 4   :  17.4192
```

**Everybody brings one number to the SPREAD sheet and puts a dot on it, labelled with their angle.** Do not let them announce it from their seats — **the dots going onto one line, one at a time, is the whole drama.**

The six real answers:

| angle | spread |
|---|---:|
| 0° | 10.0000 |
| 30° | **17.4192** |
| 60° | 16.6692 |
| 90° | 8.5000 |
| 120° | 1.0808 |
| 150° | 1.8308 |

### Step 5 — the winner, then the machine (3 minutes)

> **Ask this:** "Which angle won?"

*30°, with 17.4192.*

> **Ask this:** "Which lost, and what does that direction look like on your paper?"

*120°, with 1.0808 — it is drawn straight across the cloud.*

Then run it:

```python
from sklearn.decomposition import PCA
import numpy as np
D = np.array([[4., 3.], [6., 6.], [8., 7.], [10., 8.], [12., 11.]])
p = PCA().fit(D)
print(np.round(p.components_[0], 4), "  angle %.2f degrees"
      % np.degrees(np.arctan2(p.components_[0][1], p.components_[0][0])))
print("its spread:", round(p.explained_variance_[0], 4))
```

```text
[0.7359 0.6771]   angle 42.62 degrees
its spread: 18.2812
```

> **Ask this:** "Ours was 30 with 17.4192. Its is 42.62 with 18.2812. **Who is right?**"

*Both — ours was the best of six.*

> **Say this:** "**We were twelve and a bit degrees short and it cost us 0.8620 of spread.** And you already know how to fix it: more angles. At every whole degree the best is 43°, spread **18.2804** — within a thousandth. **The library has a formula that goes straight there. Your protractor gets the same place.**"

### What "finished" looks like

- Six dots on the SPREAD sheet, labelled with their angles, and the 30° dot visibly furthest right.
- The scrap sheet with five projected scores and a spread on it, and **the ruler measurement and the arithmetic agreeing to about a tenth**.
- Somebody has noticed that 0° and 90° are just the two original columns.
- Somebody has objected that 42.62° was not one of our choices. **That is the best outcome available.**
- A student can say, unprompted: **"it's a search."**

### Variation — easier

**Four points instead of five, and three angles instead of six.** Use `(4, 3)`, `(6, 6)`, `(10, 8)`, `(12, 11)` — mean `(8, 7)`, centred to `(−4, −4)`, `(−2, −1)`, `(2, 1)`, `(4, 4)` — and only the angles `0°`, `45°` and `90°`. Dividing the sum of squares by **3** this time, because there are four points: **`0°` gives 13.3333, `45°` gives 24.3333 and `90°` gives 11.3333, so 45° wins** — and PCA's exact answer on these four points is still **42.62°, with 24.3749**. The arithmetic at 45° is one number, 0.7071, used four times.

**And give them the projections by ruler only, with no arithmetic at all.** Drop a perpendicular, measure in squares, square the four numbers, add, divide by 3. **Objective 2 is about understanding that you are searching directions, not about multiplying decimals.**

**One thing you must not cut:** centring. If they project the raw points, every angle gives a huge number and the comparison is meaningless.

### Variation — harder

1. **Find a better angle than 30° by hand.** Try 40°, 45°, 50° and report the spreads. The real numbers: **41° → 18.2668, 42° → 18.2791, 43° → 18.2804, 44° → 18.2707.** **The peak is at 43°, and going past it makes things worse again** — which is a hill, and they met hills in Week 12.
2. **Compute PC2's spread and check the total.** PC2 is at right angles to PC1, so at `42.62 + 90 = 132.62°`, and its spread is **0.2188**. Then `18.2812 + 0.2188 = 18.5000 = 10.0 + 8.5`. **The total spread is conserved, and proving it yourself is much better than being told.**
3. **Rebuild one point from PC1 alone, by hand.** The last student's score is `5.6520`. Multiply the direction by it: `5.6520 × 0.7359 = 4.1593` and `5.6520 × 0.6771 = 3.8270`. Add the means back: `(4.1593 + 8, 3.8270 + 7) = (12.1593, 10.8270)`. **The real point was (12, 11), so the miss is `√(0.1593² + 0.1730²) = 0.2352`** — and that matches `inverse_transform`'s `0.2351` to within the rounding of the hand values.
4. **Break the cloud.** Move one point so the cloud is round instead of long — say change `(12, 11)` to `(12, 3)` — and re-run. **The two explained-variance shares come out much closer together, because there is no longer a clearly widest direction.** Then the good question: *"when is PCA useless?"* **When your data is already round.**
5. **The curse of dimensionality, measured.** The script is in the Answer Key under Build It, Stretch. **Find the number of columns at which the contrast ratio first falls below 1.0** — it is between 20 and 100 — and say in plain words what that means for k-means.
6. **PCA on the 8×8 digits from Term 3.** `load_digits()` has 64 columns. How many components for 80% of the spread? **Then look at `pca.components_[0]` reshaped to 8×8 as an image** — it is a recognisable blob of "where digits have ink". A genuinely beautiful two-line experiment and it needs nothing new.

---

## ❓ Questions Students Ask This Week

**"Is PC1 one of my original columns?"**

**No, and this is the misconception worth killing first.** PC1 is a **blend of all of them.** Print `pca.components_[0]` for the wine data and you get thirteen non-zero numbers: flavanoids pulls 0.423, total_phenols 0.395, nonflavanoid_phenols −0.299, and so on down to the small ones. **Nothing is set to zero. Nothing is discarded.**

That is the difference between PCA and picking columns. If you picked the two best columns you would bin eleven. PCA keeps a little bit of all thirteen in every component — it just arranges them so the first component catches as much of the spread as it can.

**And that is also PCA's biggest practical drawback.** "Flavanoids is high" is something a winemaker understands. "PC1 is 2.3" is not. **You buy fewer columns and you pay in interpretability**, which is exactly why naming your components from their loadings is a real skill and not decoration.

**"What is a loading of −0.299 supposed to mean?"**

It means that column goes the **opposite** way from the component. As PC1 goes up, `flavanoids` (+0.423) goes up and `nonflavanoid_phenols` (−0.299) goes **down**.

And that is a real pattern in this dataset rather than an artefact: in these 178 wines, flavanoid and non-flavanoid phenols go opposite ways. **PCA found it without being told, which is the nicest thing unsupervised methods do** — they surface relationships nobody put in.

The size, `0.299`, is how hard it pulls. Loadings near zero mean that column has almost nothing to do with that component.

**"Why does my plot come out mirrored compared to the one in the guide?"**

**Because the sign of a component is arbitrary and nothing is wrong.** `(0.7359, 0.6771)` and `(−0.7359, −0.6771)` describe the *same line* through the data; they just label its two ends differently. Different sklearn versions (or randomized solvers) can hand you either one.

What that means practically: **never interpret the sign of a single loading on its own.** "PC1 is high for rich wines" is only true relative to how your version happened to orient the axis, so always say which end is which by naming a row: *"the bottles at the positive end are the high-flavanoid ones."*

**What is never arbitrary is the signs *within* one component relative to each other.** If flavanoids and nonflavanoid_phenols have opposite signs in your run, they have opposite signs in everybody's run. **The relationship is real; the direction of the arrow is a coin toss.**

**"If keeping two components loses 44.6%, why would anyone ever do it?"**

Three honest reasons, and the third is the one that matters most.

**Because you need a picture.** You cannot draw thirteen dimensions and you can draw two. A 55%-true picture that a human looks at beats a 100%-true table that nobody reads. **You just have to write "55.4%" on the axis.**

**Because distance stops working in high dimensions.** The contrast table: with 500 columns the furthest pair is 21% further apart than the closest. **Cutting to a handful of columns can bring distance back to life when the data really lies near a low-dimensional shape, and everything k-means does is distance.** The table is for random points, where PCA could not help; the price for the wine is the reconstruction miss.

**And because of the shape of your problem.** With 178 rows and 13 columns, PCA is mostly a convenience. With **300 rows and 20,000 columns** — which is what genetic data looks like — an ordinary model has far more unknowns than rows and cannot be fitted sensibly without cutting the columns down first (or using a regularised model, which is a different answer), and then PCA is not a nicety, it is one of the main ways in. **The value of dimensionality reduction depends entirely on how many rows you have per column, and 178 rows for 13 columns is comfortable.**

**"Could PCA throw away exactly the thing I needed?"**

**Yes, and it happens, and there is no way to see it coming from inside PCA.**

PCA has never seen your target column. It chases spread. Imagine a medical table where 95% of the spread is patients' height and weight, and the thing that predicts the diagnosis is one small ratio between two blood tests. **PCA to two components keeps the body-size axis and bins the diagnosis**, and `explained_variance_ratio_` will tell you cheerfully that you kept 95% of the information.

The only defence is empirical: **train your model with and without the PCA step and compare the scores you actually care about.** That is next week's last exercise, and it is why the honest rule is "test, do not assume".

There is also a design question worth asking. **If you already know which columns matter, why are you using an unsupervised method to choose them?** PCA's real home is when you have far more columns than rows, or when your columns are so tangled together that a model cannot get a stable answer out of them.

**"Last week you said scale before k-means. Is it the same rule for PCA, or is that a coincidence?"**

**Same rule, same reason, and it is not a coincidence at all — it is the single most useful connection available this week.**

k-means measures distance, and distance adds up squared gaps, so the widest-ranging column decides every comparison. PCA maximises variance, and variance *is* squared gaps, so the widest-ranging column becomes PC1. **Both algorithms are built out of squared differences, so both are at the mercy of your units.**

And the evidence is two printouts that rhyme. Unscaled k-means sorted the wine into proline bands of 278–590, 600–937 and 970–1680. Unscaled PCA gave a PC1 of `0.9998 × proline` with a 99.81% share. **Same column, same cause, two different algorithms, both silently useless.**

The general form, and it is worth writing down: **any method built on squared differences needs its columns on a common ruler first.** That covers k-means, PCA, kNN from Level 2, and ridge regression. It does *not* cover decision trees, which split one column at a time and do not care about units at all — which is a genuinely useful thing to know.

**"How many components should I keep?"** *(Nobody fully agrees, and here is why.)*

**There is no settled answer, and the disagreement is instructive rather than annoying.**

**Camp one: a variance threshold.** Keep enough for 80%, or 90%, or 95%. Simple, defensible, easy to write in a report. **The objection: the threshold is arbitrary.** Nobody can tell you why 80% rather than 85%, and a dataset can easily need 5 components for 80% and 11 for 95%.

**Camp two: find the elbow in the variance plot.** Exactly Week 28's move, applied to a different curve. **The objection is exactly Week 28's objection too:** elbows are often not there, and two sensible people read the same curve differently. Our wine shares go 0.3620, 0.1921, 0.1112, 0.0707, 0.0656 — there is a *bend* around 3 or 4, but "around" is doing a lot of work.

**Camp three: keep whatever makes the downstream model best.** Do not guess — try 2, 5 and 8 components and cross-validate. **This is the strongest position when you have a downstream model**, and it turns an unanswerable question into a measurement. **The objection: it does not work when you are only trying to draw a picture or understand the data**, because then there is nothing downstream to score.

**Camp four, and it is the most uncomfortable: the question is often a symptom.** If it genuinely matters whether you keep 5 or 6 components, the difference between them is tiny and your conclusion is fragile either way. **A result that survives at 3 components and at 8 is a result. A result that only appears at exactly 6 is a coincidence you have not noticed yet.**

What to tell a 14-year-old, out loud: **"there is no right number. But whatever you keep, you must report two things — the share you kept and the error you paid — and if your answer changes a lot when you keep one more, say so instead of hiding it."**

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| **Somebody asks how sklearn gets 42.62° and the lesson falls into eigenvectors** | It is a completely reasonable question and there is a real answer you know | **Have the sentence ready and use it verbatim:** *"there is a formula, it needs maths you will meet at university, and it gives the same answer as a very fine grid."* **Then show them 43° → 18.2804 and move on.** Twenty seconds. Going further loses the whole class and teaches nothing. |
| The centring step gets skipped in the activity | It looks like tidying up rather than part of the method | **Do it with the whole class at once, before any angles are handed out**, and say the sentence: *"if your spread comes out enormous later, this is the step you skipped."* **It is the number-one cause of wrong answers in the activity.** |
| 98.82% lands as "we lost nothing" | It is a very large percentage | **Immediately show the rebuilt point.** `(12.1592, 10.827)` against `(12, 11)`. Then the wine version: `2.2550 ÷ 3.5180 = 0.6410`. **Percentages persuade; the invoice corrects.** |
| The unscaled-PCA demo gets skipped for time | It is at the end of the live-code and the clock is at minute 42 | **Move it to the wrap rather than cutting it.** Two lines and two outputs — `[0.9981 ...]` and `proline 0.9998` — and it is the strongest link between this week and last week. **If you have ninety seconds, spend them here.** |
| A student thinks PCA selects columns | "Dimensionality reduction" sounds like removal | **Print `pca.components_[0]` with the column names attached and count the zeros. There are none.** One printout, misconception gone. |
| The 120° and 150° protractor lines are drawn wrong | Obtuse angles on a protractor are genuinely fiddly | **Check those two students' lines before they start measuring.** A wrong line means a wrong spread means a wrong dot on the wall, and then the class's search is broken. |
| `explained_variance_` gets reported as if it were the ratio | The two names differ by one word | **Print both, once, side by side: `[4.7324 2.5111]` and `[0.3620 0.1921]`.** Then say which adds to 1. |
| The PCA plot goes up with bare "PC1" and "PC2" axes | matplotlib will happily let you | **Put the percentage in the label in the very first plot you draw, and say why out loud.** Every plot after that copies the first one. |
| Somebody points out the 13 spreads add to 13.0734 not 13 | Because they do, and it looks like a bug | **Tell the truth:** `StandardScaler` divides by n and `PCA` divides by n − 1, so the totals differ by a factor of 178 ÷ 177 = 1.00565, and 13 × 1.00565 = 13.0734. **A student who found that has read the output properly and should be told so.** |
| The lesson runs out of time in the wrap | There is a protractor activity and two datasets in seventy minutes | **The least cuttable things are the six spreads on the wall and `2.2550 ÷ 3.5180`.** If you are behind at minute 60, cut the thirteen-row table to its first five rows — **but never cut the reconstruction error, which is objective 4.** |
| A student decides PCA is pointless because it loses information | 44.6% sounds like a lot to lose for a picture | **Agree, then reframe with the contrast table.** *"You are right that it costs. Here is what it buys: with 500 columns the furthest two points are only 21% further apart than the closest two. Distance stops working. PCA is how you get it back."* |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** the thirteen wine components entirely. Do the five points and stop. **Objectives 1, 2 and 4 all live in the five points.**

**Cut:** six angles to three — `0°`, `45°`, `90°`. **45° wins with a spread of 18.2500** (against 10.0000 at 0° and 8.5000 at 90°), close enough to 42.62° that the punchline lands, and 45°'s direction is one number, 0.7071, used four times.

**Cut:** the ruler method. Arithmetic only, from the direction numbers on the board.

**Give them `new_axes.py` complete.** All of today's learning is in the hand projections and reading two numbers off a table. **None of it is in typing `StandardScaler`.**

**The version of the maths that skips the algebra.** No minus signs, no decimals, no formula. Two tables:

| the numbers | 4 | 6 | 8 | 10 | 12 |
|---|---|---|---|---|---|
| **how far from 8?** | 4 | 2 | 0 | 2 | 4 |
| **that, times itself** | 16 | 4 | 0 | 4 | 16 |

> **"Add up the bottom row. Then divide by 4."**

**40, and 10.** **That is objective 1, complete, with no minus signs and no word "variance" until the end.** Then one sentence: *"the bigger that number, the more spread out your five things are."*

And for the projection, one point only, and the numbers chosen so it is easy:

> **"The direction is 0.8660 across and 0.5000 up. The point is 4 across and 4 up. Multiply the matching pairs and add them."**

`4 × 0.8660 = 3.4641`, `4 × 0.5000 = 2.0000`, total `5.4641`. **One projection, done properly, is objective 2's understanding.**

**The copy-this-exactly scaffold.** Eight lines, runs on its own, and it makes the whole point without a single new idea:

```python
import numpy as np

C = np.array([[-4., -4.], [-2., -1.], [0., 0.], [2., 1.], [4., 4.]])
for across, up in [(1.0, 0.0), (0.8660, 0.5000), (0.0, 1.0), (-0.5, 0.8660)]:
    scores = C[:, 0] * across + C[:, 1] * up
    print("direction (%6.4f, %6.4f) -> spread %7.4f"
          % (across, up, (scores ** 2).sum() / 4))
```

```text
direction (1.0000, 0.0000) -> spread 10.0000
direction (0.8660, 0.5000) -> spread 17.4186
direction (0.0000, 1.0000) -> spread  8.5000
direction (-0.5000, 0.8660) -> spread  1.0806
```

Then two questions and nothing else: **"which direction is best, and which is worst?"** **0.8660/0.5000 is best at 17.4186; −0.5/0.8660 is worst at 1.0806.** And: **"so is either of the original columns the best direction?"** **No.** **That is objective 2's whole point in eight lines.**

**One thing you must not cut:** centring. Everything else today can be shortened.

### If the student is flying

None of these need syntax from a later week.

1. **Hunt for the best angle by hand** (Variation-harder 1): 41° → 18.2668, 42° → 18.2791, **43° → 18.2804**, 44° → 18.2707. **They will find the peak and overshoot it, which makes it a hill — and they met hills in Week 12.**
2. **Prove the total spread is conserved** (Variation-harder 2): `18.2812 + 0.2188 = 18.5000 = 10.0 + 8.5`. **Working that out yourself is much better than being shown it, and it is what turns PCA from magic into a rotation.**
3. **Rebuild a point by hand** (Variation-harder 3) and match `inverse_transform` to four decimals: `(12.1592, 10.8270)`, miss `0.2351`.
4. **Make the cloud round and watch PCA become useless** (Variation-harder 4). **The good question is "when is PCA worth nothing?" and the answer is "when there is no widest direction".**
5. **The curse of dimensionality, measured** (Build It, Stretch). The contrast ratio crosses below 1.0 between 20 and 100 columns. **Then: what does that mean for k-means?** Every assignment becomes a coin toss between near-identical distances.
6. **PCA on the 64 pixels of `load_digits()`** (Variation-harder 6). How many components for 80%? And **`pca.components_[0].reshape(8, 8)` drawn as an image is a picture of which pixels rise together and which fall against them (positive and negative patches, not a plain "where the ink is" blob)**. Two lines, and it connects Term 4 straight back to Term 3.

### If the student won't engage today

**Close the laptop. One sheet of graph paper and a pencil.**

Draw a long thin diagonal cloud of about ten dots, leaning up to the right, right across the page. Then three instructions:

> **"Draw one straight line through the middle of that cloud, so the line goes the long way — along the cloud."**
>
> **"Now draw a second line through the middle, at right angles to your first one."**
>
> **"Which line has more dots spread out along it?"**

**The first one, obviously and instantly.** **That is PC1 and PC2 and the whole idea, in ninety seconds with a pencil.**

If they will take one more, put a ruler along the first line and ask:

> **"Squash every dot onto this line — just slide each one sideways until it touches. Now how many numbers do you need to describe each dot?"**

**One instead of two.** Then: **"and what did you lose?"** **How far off the line each dot was.** **That is reconstruction error, discovered rather than told, and it is the best moment available today.**

If they will take a third, do the midge photograph out loud with no paper at all:

> **"A long thin swarm of midges. You photograph it from the end and get a blob. From the side you get a streak. Which photo would you rather have?"**

**The streak.** **"Why?"** **Because you can still tell the midges apart.** That is objective 2's motivation, complete, in one exchange.

The rest survives.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — variance, on new numbers (written, 60 seconds)**

> "Work out the variance of **2, 4, 6**. Show all four steps. **Divide by 2 at the end, the way sklearn would.**"

*Good answer:* "Mean is 4. Distances are −2, 0, 2. Squares are 4, 0, 4. Total 8. `8 ÷ 2 = 4`."

**What to catch:** adding the distances instead of the squares — **that always gives 0** and a student who reports 0 has skipped the squaring. **Push once:** *"add up your row of distances. What did you get, and is that a useful measure of spread?"* **Full marks needs all four steps written, not just the answer.**

**Check 2 — what PCA did (spoken, 90 seconds)**

> "I had thirteen columns of wine chemistry. I ran PCA and now I have two columns. **Which eleven did I throw away?**"

*Good answer:* "None of them. PCA doesn't pick columns — each of the two new columns is a blend of all thirteen. `pca.components_[0]` has thirteen non-zero loadings in it. What got thrown away isn't columns, it's the 44.6% of the spread that wasn't along the first two directions."

**What to catch:** any answer that names columns. **Push once:** *"print `pca.components_[0]` in your head — how many numbers are in it?"* **Thirteen. A student who says "none, they're blends" without prompting is at level 4.**

**Check 3 — the promise and the bill (spoken, 90 seconds)**

> "Two components keep **55.4%** of the wine data's spread, and rebuilding from them misses a typical wine by **2.2550**. **A typical wine sits 3.5180 from the middle of the cloud. So how bad is that miss, and which of those two numbers goes in your report?**"

*Good answer:* "`2.2550 ÷ 3.5180 = 0.6410`, so the rebuilt wine is out by about 64% of a typical distance from the middle — that's a big miss. Both numbers go in the report: 55.4% is what you kept and 2.2550 is what it cost, and putting only the first one in would be misleading."

**What to catch:** reporting only 55.4%, or saying 2.2550 "is small" with nothing to compare it to. **Push once:** *"2.2550 of what? Compared to what?"* **The answer "compared to 3.5180" is the whole skill, and it is Week 27's "compared to what?" in a new costume.** A student who says **both** numbers go in the report, unprompted, is at level 4.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot compute a variance without the steps in front of them. Adds the distances rather than the squares. Thinks PCA picks the best columns. Reads 98.82% as "nothing lost". |
| **2 — Emerging** | Computes variance with the table pre-drawn. Projects one point with help. Knows the widest direction wins but cannot say what "widest" was measured as. Reports the explained variance ratio only. |
| **3 — Secure** | Does all four variance steps unaided, including centring the cloud first. Projects five points onto an assigned angle and computes its spread correctly. Reads 0.8016 at PC5 as the answer to "how many for 80%". Reports both the share kept and the reconstruction error. **This is the target.** |
| **4 — Strong** | Notices that 0° and 90° are the two original columns, and that neither wins. Says the class's 30° answer was coarse rather than wrong, and proposes a finer grid. Compares 2.2550 against 3.5180 without being prompted. States that PC1 is a blend of all thirteen columns and can point at `components_` as evidence. |
| **5 — Exceptional** | Checks that `18.2812 + 0.2188 = 18.5 = 10.0 + 8.5` and describes PCA as a rotation that redistributes spread rather than a compression. Connects unscaled PCA to unscaled k-means as the same failure — squared differences, common ruler — before being told. Observes that PCA never saw the target column and so could bin the useful signal, and proposes cross-validating with and without it. Asks which end of a component is which, having realised the sign is arbitrary. |

---

## 📤 Homework to Assign

**Say this:**

> "The whole workbook is this week's homework, and it is in the order you will meet things. **Start with the Warm-Up, five minutes, all about last week** — it is there so that k-means is fresh when PCA borrows its ideas. **Then 'Do the Maths by Hand': four exercises, calculator only, no code.** Variance in four steps, projecting five students onto a direction, the explained-variance ratio, and rebuilding one student from one number. Then the Predict the Output, Practice Set A and Practice Set B, the Fix the Broken Program, the Puzzle, the two Think Deeper paragraphs, the Draw It, and the Self-Check.
>
> **The part I mark hardest is Build It, and it has four pieces that build on each other.** About an hour.
>
> **First, the thirteen shares — the explained variance table for all thirteen wine components, with a running total column.** Thirteen rows, two number columns. **Then circle the row where the running total first passes 80% and write the number of components beside it.** That is one integer and I want to see it. Check it with the one-line shortcut and write down what that prints.
>
> **Second, the plot — the two-dimensional projection, saved as a PNG.** 178 wines, squashed to two components, scattered. **And the percentage goes in both axis labels, written out in full in the workbook as well.** A plot with bare 'PC1' and 'PC2' on it comes back to you, because a picture that is 55% true and does not say so is worse than no picture. Then one honest sentence on what you actually see.
>
> **Third, PC1's loadings and its name.** Print the three columns that pull hardest, with their numbers. **Then give the axis a human name — three or four words — and one sentence saying why those three loadings justify it.** 'PC1' is not a name. 'Total phenolic richness' is a name. **And if you disagree with my name, say so and give me yours; that is a better answer than agreeing.**
>
> **Fourth, the bill — the reconstruction error at two components against six, and this is the part I mark hardest.** Two misses and the yardstick, and then one sentence on what the difference cost. **And the sentence has to compare the miss against something** — a typical wine sits 3.5180 from the middle of the cloud, so a miss of 2.2550 is 64% of that. **A sentence that just says 'the error was bigger with two components' scores nothing, because I already knew that.**
>
> The stretch at the bottom of Build It is the curse of dimensionality — measure how the contrast between the furthest and nearest pair of points collapses as you add columns, and tell me at what point 'nearest neighbour' stops meaning anything. And before you run anything in Build It, fill in the four predictions in pen."

**Workbook sections, in the order they appear:** Warm-Up · Do the Maths by Hand (M1–M4) · Predict the Output (P1–P4) · Practice Set A (A1–A6) · Practice Set B (B1–B5) · Fix the Broken Program · Puzzle of the Week · Think Deeper (T1, T2) · Build It · Draw It · Self-Check.

**In class and at home.** The workbook is **all at home**: it has no sheet for the lesson's own cloud (4, 6, 8, 10, 12 and the six-angle search), so in class the variance steps, the six projections and the pen vote on "which angle wins" go on **graph paper and scrap paper**. The workbook then repeats the same two procedures on a different cloud (M1 and M2, then B2 and B3), which is useful: a student who did the class cloud now does it again without you. The workbook's own **Build It predictions** (which of the six angles is widest on the *five students*, and so on) are a second, separate set of guesses about the workbook's cloud, so they are made at home, in pen, before anything runs.

**Expected time:** Warm-Up 5 min · Build It about **60 minutes** (10 min on the shares table · 15 min on the plot · 15 min on the loadings and the name · 20 min on the bill and its sentence), plus 20 more for the curse-of-dimensionality stretch. The rest of the workbook is more than one evening: **let the student spread it across the week, and if you must choose, mark Build It, M1–M4 and Fix the Broken Program.**

> **🧑‍🏫 What to look for when you mark Build It:** four things, and the fourth is the real one. **One — is there a single integer answering "how many for 80%"?** It is **5**, read off the running total at `0.8016`. A student who writes "about five or six" has not read the table. **Two — are the percentages in the axis labels?** This is a habit, and habits are built by being marked. **Three — is the component's name justified by the loadings, or is it decoration?** The bar is: *do the three numbers they printed actually support the name they chose?* "Total phenolic richness, because flavanoids 0.423, total_phenols 0.395 and od280/od315 0.376 are all phenolic measures and all pull the same way" is justified. "Wine quality" is not, because nothing in the loadings mentions quality. **Four — does the reconstruction sentence contain a comparison?** `2.2550` against `1.3258` is two numbers; `2.2550 ÷ 3.5180 = 0.6410` is a judgement. **Only the second one is an answer**, and it is the same "compared to what?" discipline as Week 27's control and Week 9's baseline. **Mark that difference explicitly and praise loudly anybody who found their own yardstick.**

---

## 🔑 Answer Key

Every workbook section and item, in workbook order, so you can mark from this page alone. **Values are taken from the workbook's own Answers section and were re-run for this key.** The lesson's own questions, on the lesson's own cloud, are answered after it, under **Answers to every question posed in the lesson**.

### Warm-Up (5 min)

*Five questions about last week.*

| Item | Answer | What to watch for |
|---|---|---|
| **W1** two steps of k-means | **Step 2 is ASSIGN** — every point goes to its nearest centre; **nothing moves**, only the colouring changes. **Step 3 is MOVE** — every centre goes to the middle of what it just got; **only the centres move.** | Students say "the points move". The points are the data and never move. |
| **W2** `print(km.inertia_)` | `AttributeError: 'KMeans' object has no attribute 'inertia_'`. **The clue is the trailing underscore** — a name ending in `_` does not exist until `.fit` has run. | Students write a number. There is no `.fit` call in the line, so nothing has been computed. |
| **W3** smallest possible inertia | **k = 178**, **inertia 0**. Worthless because every point is its own centre, so every squared distance is zero: a perfect score that has grouped nothing. | Students answer "k = 1". That gives the *largest* inertia. |
| **W4** unscaled bands | **`proline`, spread 314.91**; the three bands **do not overlap** — *sealed*, or *non-overlapping*. | Students name `alcohol`. Only the column with the biggest numbers can do this. |
| **W5** the sigma, six terms | `Σ (distance)² = 0.4444 + 1.1111 + 1.1111 + 0.0000 + 2.0000 + 2.0000 = 6.6667` | A term of `0` in the fourth place is correct, not a gap. |

### Do the Maths by Hand

*Four exercises, calculator only. Make sure no code was used: the point is to feel the arithmetic before Python does it.*

**M1 — variance of 2, 5, 6, 9, 13, and the cost of skipping the centring.**

**(a)** `( 2 + 5 + 6 + 9 + 13 ) ÷ 5 = 35 ÷ 5 = 7.0`

**(b)**

| the number | minus the mean | squared |
|---:|---:|---:|
| 2 | −5 | 25 |
| 5 | −2 | 4 |
| 6 | −1 | 1 |
| 9 | +2 | 4 |
| 13 | +6 | 36 |
| | **sum: 0** | **sum: 70** |

The middle column adds to **0 for any list**, because the mean is *defined* as the place where distances above and below cancel. **That is the whole reason you square.**

**(c)** `70 ÷ 4 = 17.5` (what sklearn does) · `70 ÷ 5 = 14.0`.

**(d)** `4 + 25 + 36 + 81 + 169 = 315`, and `315 ÷ 4 = 78.75`. `78.75 ÷ 17.5 = 4.50` — **four and a half times too big.** The sentence: the uncentred number measures how far the numbers are from **zero**, not from each other; it is mostly a measurement of *where* the cloud is, not how big it is.

**Marking notes.** A student who reports a variance of 0 summed the middle column instead of the last. A student with `14.0` in the "sklearn" slot divided by 5. A student who skipped (b)'s "why" has done the arithmetic without the idea; it is worth a question.

**M2 — five students `(1,3)`, `(3,4)`, `(5,8)`, `(7,9)`, `(9,11)`, projected by hand.**

**(a)** `middle = (25 ÷ 5, 35 ÷ 5) = (5.0, 7.0)`. Centred points: `(−4, −4)  (−2, −3)  (0, 1)  (2, 2)  (4, 4)`. Check: across `−4 − 2 + 0 + 2 + 4 = 0`, up `−4 − 3 + 1 + 2 + 4 = 0`.

**(b) 30°, direction (0.8660, 0.5000):**

| centred point | across × 0.8660 | up × 0.5000 | the score |
|---|---|---|---|
| (−4, −4) | −3.4641 | −2.0000 | **−5.4641** |
| (−2, −3) | −1.7321 | −1.5000 | **−3.2321** |
| (0, 1) | 0.0000 | 0.5000 | **0.5000** |
| (2, 2) | 1.7321 | 1.0000 | **2.7321** |
| (4, 4) | 3.4641 | 2.0000 | **5.4641** |

**(c)** `29.8564 + 10.4465 + 0.2500 + 7.4644 + 29.8564 = 77.8737`, `÷ 4 = 19.4684` by hand; **Python prints `19.4683`** because the scores were typed already rounded. **Both are right.**

**(d) 60°, direction (0.5000, 0.8660):** scores `−5.4641, −3.5981, 0.8660, 2.7321, 5.4641`; squares add to `80.8735`; `÷ 4 = 20.2184` by hand (**Python 20.2183**). **60° is wider than 30°.**

**Marking notes.** Five positive scores means **distance from the origin** was measured, not position along the axis (the same error flagged in B3). Scores that do not sum to about 0 point to an arithmetic slip in the centring, usually in the `up` column: the second student is `(−2, −3)`, not `(−2, −1)`. (`−1` belongs to the *lesson's* cloud, which is a different cloud.)

**M3 — explained variance ratio, by hand.**

**(a)** `10.0000 + 11.5000 = 21.5000`. **(b)** `21.2768 + 0.2232 = 21.5000`. **(c) Yes, exactly the same.** PCA does not throw anything away when it rotates: it *re-shares* the same total. **(d)** `PC1: 21.2768 ÷ 21.5 = 0.9896` · `PC2: 0.2232 ÷ 21.5 = 0.0104`. **(e)** They add to **1.0000**, and they always must. *(On 13 columns, `PCA(n_components=2)` gives two shares that add to 0.5541, not 1.)*

**The sentence:** `explained_variance_` holds actual spreads in the units of the scaled table and adds up to roughly the number of columns; `explained_variance_ratio_` holds shares of that total and adds up to 1.

**Marking notes.** A "No" in (c) means an addition slip, not a misunderstanding; have them redo it. The sentence must separate *spreads* from *shares*.

**M4 — rebuild one point from one number.**

**(a)** `across: 5.0 + (−3.5585 × 0.6815) = 5.0 + (−2.4251) = 2.5749` · `up: 7.0 + (−3.5585 × 0.7319) = 7.0 + (−2.6045) = 4.3955`. (Python, unrounded: `2.5751` and `4.3957`.)

**(b)** `across gap: 3 − 2.5751 = 0.4249, squared 0.1805` · `up gap: 4 − 4.3957 = −0.3957, squared 0.1566` · `add: 0.3371` · `square root: 0.5806`.

**(c)** `0.5806 ÷ 3.7495 = 0.1548`.

**(d)** Small: the rebuilt student is out by about 15% of a typical distance from the middle, and the student only knows that because they had a yardstick. **Full marks needs the comparison in the sentence.**

### Predict the Output

*The students predict in pen before running; the "truth" is the printed output.*

**P1.**

```text
D     (5, 2)
Z     (5, 1)
back  (5, 2)
same numbers back? False
```

**`back` has the right shape and the wrong numbers.** `transform` narrows `(5, 2)` to `(5, 1)`, throwing one number per point away; `inverse_transform` widens back by placing every point **on the new axis**. **A shape match is not a content match.** *Common wrong prediction: `True`, or `Z (5, 2)`.*

**P2.**

```text
ratio sums to : 1.0
variance sums to: 13.0734
first two ratios add to: 0.5541
```

**Where the extra comes from.** `StandardScaler` divides by `178`, `PCA` averages by `177`, so each column comes out as `178 ÷ 177 = 1.00565`, and `13 × 178 ÷ 177 = 13.0734`. **Two conventions meeting; not a bug, not rounding.** *Common wrong prediction: `13.0` on line 2; the question is there to make them explain the gap.*

**P3.**

```text
UNSCALED evr[0] : 0.9981
SCALED   evr[0] : 0.362
UNSCALED PC1's biggest loading: proline 0.9998
```

**`0.9981` looks like a triumph and is a disaster**: PC1's loading on `proline` is `0.9998`, so PC1 *is* the proline column. Variance is measured in the column's own units, and proline's units are hundreds. Same cause as last week's unscaled k-means.

**P4.**

```text
wine  : 13 columns -> 5
digits: 64 columns -> 21
```

`n_components=0.80` means *"keep however many components I need to reach 80% of the spread, and work out the number yourself."* *Common wrong prediction: `0.80` read as "80% of the columns" (about 10 for the wine).*

### Practice Set A — Read It

**A1.** variance **(iii)** · projection **(i)** · principal component **(vii)** · explained variance ratio **(vi)** · loading **(ii)** · reconstruction error **(iv)** · curse of dimensionality **(v)**

**A2.** Read the **running total** column and take the first row that reaches or passes the target.

| Question | Answer |
|---|---|
| at least 80% | **5** — 0.8016 |
| at least 90% | **8** — 0.9202 (seven only reaches 0.8934) |
| at least 99% | **12** — 0.9920 (eleven only reaches 0.9791) |
| all of it | **13** — 1.0000 |

**"About five or six for 80%" is not an answer** because four gives 0.7360 (under) and five gives 0.8016 (over); the table contains the one integer. *Watch for 7 for 90%, which reads the share column instead of the running total.*

**A3.** `(1)` → **(c)** · `(2)` → **(b)** · `(3)` → **(a)**. The sentence: **`transform` narrows, `inverse_transform` widens, so whatever came out of one goes into the other.**

**A4 — the diagram.** Answers depend on the angle chosen. **60° worked in full:** direction `(0.5000, 0.8660)`; scores `−5.4641, −3.5981, 0.8660, 2.7321, 5.4641`; squares add to `80.8735`; `÷ 4 = 20.2184`; two scores negative (the first two). Comparison panel: widest of the six is **60°, spread 20.2183**; PCA says **47.04°, spread 21.2768**; the grid was short by **12.96°**. Extra: **45° scores 21.2500**, only 0.0268 short of PCA, so a finer grid closes the gap. *(Check against the student's own angle by recomputing the five scores; any angle is acceptable if its arithmetic is right.)*

**A5.**

| Student | Verdict |
|---|---|
| Asha, "total phenolic richness" | **Pass.** Flavanoids 0.423, total_phenols 0.395 and od280/od315 0.376 are all phenolic measures pulling the same way. |
| Ben, "wine quality" | **Fail.** Nothing in thirteen chemical measurements mentions quality. Naming an axis something the data cannot see is the over-claim this course exists to prevent. |

The opposite-pulling row is **`nonflavanoid_phenols` at −0.299**. **It is not a bug**: as the other phenolic measures rise it tends to fall in these 178 wines. *Spotting and explaining it is the best available reading of the table.*

**A6.** **(a)** They divided by **5**; they should have divided by **4**. The giveaway is the ratio: `0.80 = 4 ÷ 5`. **(b)** **They forgot to centre.** Every spread is enormous and barely changes from angle to angle, because almost all of the number is *where the cloud sits*.

### Practice Set B — Write It

Expected outputs. Each program is a short script of the student's own; mark the **output**, not the code's wording.

**B1.** Prints a single integer:

```text
5
```

Accept any one-liner that gets there (e.g. `PCA(n_components=0.80).fit(X).n_components_` on scaled wine). A student who prints a running-total table instead did not follow "without building the table yourself".

**B2.** Variance in four printed steps, then with no centring:

```text
the numbers   : [ 2.  5.  6.  9. 13.]   mean = 7.0
step 1 distance: [-5. -2. -1.  2.  6.]  which add to 0.0
step 2 squared : [25.  4.  1.  4. 36.]
step 3 added up: 70.0
step 4 / 4     : 17.5
       / 5     : 14.0

and with NO centring at all:
squared        : [  4.  25.  36.  81. 169.]
added up       : 315.0
/ 4            : 78.75
which is 4.50 times too big
```

**Done looks like:** distances total `0.0`, and the uncentred version is `4.50` times the centred one.

**B3.** Six axes on the five students, centred first:

```text
the middle of the cloud: [5. 7.]
centred: [[-4.0, -4.0], [-2.0, -3.0], [0.0, 1.0], [2.0, 2.0], [4.0, 4.0]]
 angle   direction (across, up)     the five scores along it              spread
   0   ( 1.0000,  0.0000)   [-4.000 -2.000  0.000  2.000  4.000]  10.0000
  30   ( 0.8660,  0.5000)   [-5.464 -3.232  0.500  2.732  5.464]  19.4683
  60   ( 0.5000,  0.8660)   [-5.464 -3.598  0.866  2.732  5.464]  20.2183
  90   ( 0.0000,  1.0000)   [-4.000 -3.000  1.000  2.000  4.000]  11.5000
 120   (-0.5000,  0.8660)   [-1.464 -1.598  0.866  0.732  1.464]   2.0317
 150   (-0.8660,  0.5000)   [ 1.464  0.232  0.500 -0.732 -1.464]   1.2817
widest of the six: 60 degrees with spread 20.2183
```

*Watch for all-positive scores (distance from the origin), and for an uncentred run, whose spreads are large and nearly equal.*

**B4.** One component, rebuild, price:

```text
PC1 direction: [0.6815 0.7319]
its angle    : 47.04 degrees
one number per point: [-5.6533 -3.5585  0.7319  2.8266  5.6533]
rebuilt:
[[ 1.1476  2.8626]
 [ 2.5751  4.3957]
 [ 5.4987  7.5356]
 [ 6.9262  9.0687]
 [ 8.8524 11.1374]]
miss per point: [0.2016 0.5806 0.6815 0.1008 0.2016]
average miss  : 0.3532
yardstick: a typical point sits 3.7495 from the middle
so the miss is 0.0942 of a typical distance
```

**No point has a miss of `0.0000`**, which is the thing to notice: none of the five sits exactly on the new axis. The middle student `(5, 8)` is a unit above the mean `(5, 7)` and is the **worst**-rebuilt (`0.6815`). *The point nearest the middle is not automatically the best-rebuilt one.*

**B5.** The whole wine report. Script and expected output:

```python
"""b5.py - the whole wine PCA report: shares, a name, and the bill."""
import numpy as np
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

np.random.seed(0)
wine = load_wine()
X_raw = pd.DataFrame(wine.data, columns=wine.feature_names)
X = StandardScaler().fit_transform(X_raw)
print("table:", X.shape)

evr = PCA().fit(X).explained_variance_ratio_
print()
print("PC   its share   running total")
for i, share in enumerate(evr, start=1):
    print("%2d     %.4f       %.4f" % (i, share, evr[:i].sum()))
print("components needed for 80%:", PCA(n_components=0.80).fit(X).n_components_)

p2 = PCA(n_components=2).fit(X)
print()
for j, tag in ((0, "PC1"), (1, "PC2")):
    pull = pd.Series(p2.components_[j], index=wine.feature_names)
    print("%s: the three hardest-pulling columns" % tag)
    print(pull.reindex(pull.abs().sort_values(ascending=False).index)
          .round(3).head(3).to_string())

print()
print("  how many PCs   running share   average rebuild miss")
for m in (2, 6):
    p = PCA(n_components=m).fit(X)
    Xh = p.inverse_transform(p.transform(X))
    miss = np.sqrt(((X - Xh) ** 2).sum(axis=1)).mean()
    print("      %2d           %.4f            %.4f"
          % (m, p.explained_variance_ratio_.sum(), miss))
yard = np.sqrt((X ** 2).sum(axis=1)).mean()
print("for scale: a typical wine sits %.4f away from the middle" % yard)
print("2 PCs: the miss is %.4f of that   6 PCs: %.4f of that"
      % (2.2550 / yard, 1.3258 / yard))
```

```text
table: (178, 13)

PC   its share   running total
 1     0.3620       0.3620
 2     0.1921       0.5541
 3     0.1112       0.6653
 4     0.0707       0.7360
 5     0.0656       0.8016
 6     0.0494       0.8510
 7     0.0424       0.8934
 8     0.0268       0.9202
 9     0.0222       0.9424
10     0.0193       0.9617
11     0.0174       0.9791
12     0.0130       0.9920
13     0.0080       1.0000
components needed for 80%: 5

PC1: the three hardest-pulling columns
flavanoids                      0.423
total_phenols                   0.395
od280/od315_of_diluted_wines    0.376
PC2: the three hardest-pulling columns
color_intensity    0.530
alcohol            0.484
proline            0.365

  how many PCs   running share   average rebuild miss
       2           0.5541            2.2550
       6           0.8510            1.3258
for scale: a typical wine sits 3.5180 away from the middle
2 PCs: the miss is 0.6410 of that   6 PCs: 0.3769 of that
```

**Done looks like:** every number in the write-up can be pointed at in this output, and the last line turns two raw misses into two judgements. For PC2 the next two are `ash 0.316` and `magnesium 0.300`, fairly named **"body and depth"** (colour, alcohol and proline together).

### Fix the Broken Program

*Three bugs: a shape error, a runtime error, and one that prints a beautiful, worthless number.*

| Bug | Line | What it is | The fix |
|---|---|---|---|
| **1** | **21** `back = p2.inverse_transform(X_raw)` | `(178, 13)` is **the table handed in**; `(2, 13)` is **`p2.components_`**, two directions of 13 numbers each. `inverse_transform` needs rows with 2 numbers. | `back = p2.inverse_transform(Z2)`. **`transform` narrows, `inverse_transform` widens.** |
| **2** | **24** `PCA(n_components=14)` | Thirteen columns can give at most thirteen directions. | **Fix A:** `PCA(n_components=13)`. **Fix B, the better one:** `PCA()`. |
| **3** | **17, 18 and 24** (fitted on `X_raw`) | `Xs` is built on line 14 and never used. | Fit on `Xs`: `p2 = PCA(n_components=2).fit(Xs)`, `Z2 = p2.transform(Xs)`, `pf = PCA().fit(Xs)`. |

**Bug 3 (a), the two giveaway lines.** `every share: [0.9981 0.0017 0.0001 ...]`: one component holding 99.81% of thirteen chemical columns is a unit problem, not a discovery. And `proline 0.9998`: PC1 *is* the proline column, renamed.

**Bug 3 (c), the fixed output:**

```text
table: (178, 13)
squashed to: (178, 2)
rebuilt to: (178, 13)
every share: [0.362  0.1921 0.1112 0.0707 0.0656 0.0494 0.0424 0.0268 0.0222 0.0193
 0.0174 0.013  0.008 ]
share kept by PC1 + PC2: 0.5541
PC1's three hardest-pulling columns:
flavanoids                      0.4229
total_phenols                   0.3947
od280/od315_of_diluted_wines    0.3762
```

So the six numbers are `0.5541` and `flavanoids 0.4229`, `total_phenols 0.3947`, `od280/od315_of_diluted_wines 0.3762`. **`0.9998` became `0.5541`: that is the bug being fixed, not the result getting worse.**

**Marking notes.** Bug 1 is often "fixed" by passing `Z2.T` or re-fitting; accept only `Z2`. For Bug 3, students usually blame line 24 only; all three fits must use `Xs`. A student who spots that `Xs` is "built and never used" has read the program closely.

### Puzzle of the Week — Guess the Axis

| Cloud | PC1 angle | explained variance ratios |
|---|---:|---|
| (a) flat line | 0.00° | `[1. 0.]` |
| (b) upright line | 90.00° | `[1. 0.]` |
| (c) uphill diagonal | 45.00° | `[1. 0.]` |
| (d) downhill | −45.00° | `[1. 0.]` |
| (e) perfect square | 0.00° | **`[0.5 0.5]`** |
| (f) shallow slope | 14.04° | `[1. 0.]` |

**The puzzle is (e), the perfect square.** Both directions hold exactly half; **there is no widest direction**, since a square is equally wide whichever way it is turned. PCA **picks one anyway and is not wrong**: `[1. 0.]` is one of infinitely many correct answers, and which one appears depends on floating-point crumbs. (f) is `arctan(3 ÷ 12) = 14.04°`, which a protractor gets.

**The report sentence for (e):** *PC1 came out at 0° with a ratio of 0.5000 and PC2 at 90° with 0.5000. Because the two shares are equal, the direction is not a finding; both components matter equally and neither can be dropped.* **Transferable rule: before naming a component, compare its share with the next one.** `0.3620` against `0.1921` is an ordering worth naming; `0.5000` against `0.5000` is a tie.

**Marking notes.** Students predict 45° for (d); the sign matters, it is −45° (or 135°). Students predict `[0.5 0.5]` for (a)–(d) because a single line "has two directions"; the ratio of a straight line is `[1. 0.]`.

### Think Deeper

**T1 — one mistake or two?** *One mistake, wearing two costumes.* Both algorithms are built on squared gaps added across columns, so both are decided by whichever column has the biggest numbers, and "biggest" is a property of the units, not the data. k-means hands back groups (three non-overlapping bands of one column); PCA hands back shares (`0.9981` on PC1 and a loading of `0.9998`). **The printout:** `print(X.std().sort_values(ascending=False))` before anything is fitted. On the wine it shows proline `314.91` at the top and nonflavanoid_phenols `0.12` at the bottom, a ratio of about 2,530 (millions to one in influence once squared).

**T2 — the brochure number and the invoice number.** `0.5541` is reported because it is flattering and comes out of `fit` for free; `0.6410` is what the person deciding needs, because it answers "how wrong will each wine be?" They describe the same run but are in different units (a share of *squared* spread against a per-row distance). A decider would want the **worst-hit** wines, not the average, and the comparison of 2 against 6 components. On 178 rows four extra columns cost nothing, so the only reason to keep two is to draw a picture, and "so I could draw it" is a legitimate reason as long as it is the reason written down.

**Marking notes (both).** T1 passes with "same cause, different symptom" and *any* named printout of column spreads; it fails with "always scale" alone, which restates the rule without the reason. T2 needs both numbers and the reason they feel so far apart.

### Build It — The Thirteen Shares, a Name, and the Bill

**Step checklist.** Ten boxes: predictions in pen · the thirteen shares with running total · the 80% row circled · the 2-D plot saved · a sentence about it · PC1's top three loadings · a name and one sentence · the average rebuild miss at 2 and at 6 · the yardstick and both fractions · (optional) the curse of dimensionality. **A box ticked with nothing written beside it does not count.**

**Predictions.** Present or absent, not right or wrong. **(a) 60°** on the five students, spread 20.2183 *(an answer of 30 is a reasonable, wrong hypothesis; it was the winner on the lesson's cloud)*. **(b) No. PCA says 47.04° with 21.2768**, so the 30°-step grid was 12.96° short and cost 1.0585 of spread. **(c)** An average of **0.3532**, with the worst point off by **0.6815**. **(d) 5.** **What earns credit is a reason attached.** *A blank row means the activity was a procedure rather than a search.*

**The thirteen shares.** Exactly the table in B5's output above. **Components for 80%: 5**, and `PCA(n_components=0.80).fit(X).n_components_` prints **5** as the check. Also worth noting in feedback: **8 components carry 92%**, **2 carry 55.4%**.

**The plot.** Filename `wine_2d.png` (any name is fine; it must be a saved PNG). Script for the plot, run after B5's `X` and `evr` exist:

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

p2 = PCA(n_components=2).fit(X)
Z2 = p2.transform(X)
plt.figure(figsize=(6.5, 5))
plt.scatter(Z2[:, 0], Z2[:, 1], s=30, alpha=0.85)
plt.xlabel("PC1 (%.1f%% of the spread)" % (evr[0] * 100))
plt.ylabel("PC2 (%.1f%% of the spread)" % (evr[1] * 100))
plt.title("178 wines, 13 columns squashed to 2")
plt.tight_layout()
plt.savefig("wine_2d.png", dpi=110)
plt.close()
print("saved wine_2d.png")
```

```text
saved wine_2d.png
```

**The two axis labels, in full:** `PC1 (36.2% of the spread)` and `PC2 (19.2% of the spread)`.

**What the plot shows.** A single connected cloud, wider than it is tall and roughly V-shaped, with **no clean gaps in it** (a student may notice three loose lobes, which is fair). PC1 runs from about −4.3 to +4.3 and PC2 from about −3.9 to +3.5. **That is the honest finding, not a failure**: next week the same plot coloured by cluster shows three clean groups, a better demonstration *because* this version looked like one blob. A student who writes "I can't see three separate groups in this" has looked properly; one who reports "three clear clusters" wrote what they expected rather than what they saw.

**Marking notes.** **The percentages must be in the axis labels: `36.2%` and `19.2%`.** This is the entire point of the step, the habit that stops a PCA plot lying to its reader.

**PC1's loadings and its name.**

| rank | column | loading |
|---:|---|---:|
| 1 | flavanoids | 0.423 |
| 2 | total_phenols | 0.395 |
| 3 | od280/od315_of_diluted_wines | 0.376 |

(The fuller list, from `.head(5)`, adds `proanthocyanins 0.313` and `nonflavanoid_phenols −0.299`.)

> **PC1 = "total phenolic richness."** The three hardest-pulling columns are all measures of phenolic content and all pull the same way, so a wine that is high on one is high on all of them. One end of the axis is chemically rich wine and the other is thin wine.

**And the detail worth a bonus mark:** `nonflavanoid_phenols` loads **−0.299** and pulls the *opposite* way: a real pattern PCA found without being told, not a bug.

**Marking notes.** **Any name is acceptable if the loadings support it.** "Phenol level", "chemical richness", "how much stuff is in it" all pass. What fails is a name with **no connection to the printed numbers** — "wine quality", "price", "age". **A student who disagrees with the suggested name and argues their own case from the numbers should score higher than one who copies it**, and a student who spotted the negative loading and explained it has done the most interesting available reading.

**The bill.**

| components | running share | average rebuild miss | miss ÷ yardstick |
|---:|---:|---:|---:|
| 2 | 0.5541 | 2.2550 | **0.6410** |
| 6 | 0.8510 | 1.3258 | **0.3769** |

**The yardstick: 3.5180.**

**The sentence being marked, and here is what full marks looks like:**

> Going from 2 components to 6 raises the share of the spread kept from **0.5541 to 0.8510** and cuts the average rebuild miss from **2.2550 to 1.3258** — a 41% reduction in error for four extra columns. **And the miss only means something against a yardstick:** a typical wine sits **3.5180** from the middle of the cloud, so `2.2550 ÷ 3.5180 = 0.6410` — with two components a rebuilt wine is wrong by **64% of a typical wine's whole distance from the middle**, which is a lot. With six it is `1.3258 ÷ 3.5180 = 0.3769`, or **38%**. **So "we kept 55% of the variance" and "we are wrong by 64% of a typical distance" describe the same run, and only the first one is usually reported.**

The cost of going to six components is four more columns per row, which for 178 wines is nothing, so on this dataset six is the better trade and the only reason to use two is to draw a picture.

**Marking notes.** **The two numbers are the easy half; the comparison is the step.** `2.2550` and `1.3258` earn a pass. **Full marks needs a yardstick** — 3.5180, or a per-column version, or anything defensible — and the division done. **A student who invents their own yardstick (say, a per-column version: the miss divided by √13 ≈ 3.61, about 0.63 per column, compared against the spread of a single standardised column, which is 1.0 — comparing the raw 13-column miss straight against 1.0 would mix a 13-column distance with a one-column spread) has done something better than the assignment asked, and should be told so.**

**Stretch — the curse of dimensionality.**

```python
import numpy as np
rng = np.random.default_rng(0)
print("   d       min      mean       max   (max-min)/min")
for d in (2, 5, 20, 100, 500):
    X = rng.random((150, d))
    diff = X[:, None, :] - X[None, :, :]
    D = np.sqrt((diff ** 2).sum(axis=2))
    dd = D[np.triu_indices(150, 1)]
    print("%4d %9.4f %9.4f %9.4f %15.4f"
          % (d, dd.min(), dd.mean(), dd.max(), (dd.max() - dd.min()) / dd.min()))
```

```text
   d       min      mean       max   (max-min)/min
   2    0.0025    0.5393    1.3580        533.8576
   5    0.0873    0.8485    1.6953         18.4217
  20    0.9006    1.8105    2.6697          1.9645
 100    3.1520    4.0624    5.3787          0.7065
 500    8.1944    9.1212    9.8894          0.2068
```

**Runtime: about 0.1 seconds.**

**The reading.** The contrast collapses from **534** at two columns to **0.21** at five hundred. **It drops below 1.0 between 20 and 100 columns** (`1.9645` at 20, `0.7065` at 100); past that the most distant pair is **less than twice** as far apart as the closest.

**What that means for k-means:** it decides everything by asking "which centre is nearest?" When every distance is nearly the same, the question is answered by differences smaller than the noise, so a tiny change in one column, or a different seed, flips large numbers of assignments. **That is one reason clusterings in very many columns can become unstable (the table shows the mechanism for random points; it is not a law for every dataset), and a concrete reason PCA and k-means are taught in the same fortnight.** Two responses the student should name: **cut the columns down first** (this week), and **use a distance suited to the data**, such as cosine distance for text (Week 32).

*(If a student asks about the `d = 2` row: 533 is enormous because with 150 points in a unit square, two land almost on top of each other, so `min` is nearly zero. A genuine property of low dimensions, not a glitch.)*

**Marking notes.** On the stretch, the reading matters more than the table: "everything is the same distance from everything, so 'nearest' stops meaning anything" is the sentence you are looking for.

### Draw It

**My angle for PC1: about 47° (47.04°). My two spreads: 21.2768 and 0.2232**, which add to 21.5000 — the same total as the original columns, `10.0 + 11.5`. **The squashed-and-rebuilt point: `(3, 4)` → `(2.5751, 4.3957)`, miss `0.5806`.** **The division: `2.2550 ÷ 3.5180 = 0.6410`.**

**The marks are in:** the five students as five dots with a cross at the mean `(5, 7)` drawn; **both** axes (PC1 at about 47°, PC2 at right angles) each labelled with its spread; one point picked out with a dashed right-angle drop, the score `−3.5585` where it lands, the hollow rebuilt dot, and the gap labelled `0.5806`; thirteen bars tallest first with a running-total line and the 80% crossing ringed at **5 components**; and the division written as a real division. **A great drawing draws PC2 too**, so that `21.2768 + 0.2232 = 21.5000` is visible: the rotation lost nothing, only the decision to keep one axis did.

**Marking notes.** Most students draw only PC1. The ringed crossing must say **5**, not 4 and not "five or six". A drawing without the mean has forgotten that everything this week happens after the cloud is moved there.

### Self-Check

There are no right answers. Three rows predict Week 30 and the capstone:

- **"say why a projected score can be negative"** — a 😕 means looking at the five centred points: two sit on the negative side in both columns. A page of five positive scores measured distance, not position; it is the most common silent error of the week.
- **"tell `explained_variance_` from `explained_variance_ratio_` without guessing"** — a 😕 means printing both once and reading the totals: one adds to roughly the column count, the other to 1.
- **"measure reconstruction error and compare it against a yardstick"** — the row that matters most, because Week 30 is built on it and Week 36 is marked on it. `2.2550` is not a result; `2.2550 ÷ 3.5180 = 0.6410` is.

### Answers to every question posed in the lesson

**Hook — "how would you draw a picture of thirteen columns?"** **You cannot.** Every pair is 78 scatter plots and nobody reads 78 of anything.

**Hook — "what is wrong with picking the two best columns?"** **Eleven columns go in the bin** and you have no way of knowing whether what mattered was in them.

**Hook — "which photo is better, and why?"** **The streak**, because it keeps the differences between the midges. The blob throws them away. **Spread is where the information is.**

**Concept — "mean of 4, 6, 8, 10, 12?"** **8.**

**Concept — "add up the five distances."** **0.** And it is 0 for *any* set of numbers, because the mean is exactly where the distances cancel — which is why a measure of spread has to get rid of the signs.

**Concept — "how do we get rid of a minus sign?"** **Square it.** (Absolute value also works and gives a different, less convenient measure that is genuinely used.)

**Concept — "there are five numbers. Why divide by 4?"** **Two conventions.** Divide by 5 → 8.0, the spread of exactly these five. Divide by 4 → 10.0, the estimate used when the five are a sample of something bigger. **scikit-learn's `PCA` divides by n − 1, so its answer is 10.0.**

**Concept — "mean across? mean up?"** **8 and 7**, so the centred points are `(−4, −4)`, `(−2, −1)`, `(0, 0)`, `(2, 1)`, `(4, 4)`.

**Concept — "why bother centring? The cloud has not changed shape."** **Because PCA is about spread, not position.** Slide the whole cloud ten units left and it is just as spread out. Centring lets you forget position entirely.

**Concept — "two numbers went in. How many came out?"** **One.** `4 × 0.86603 + 4 × 0.50000 = 5.46410`. That is the squash.

**Concept — "how spread out are those five scores?"** The four steps: squares `29.85641, 4.98205, 0, 4.98205, 29.85641`, total `69.67691`, ÷ 4 = **17.41923**.

**Concept — "which of the six will win?"** **30°, with 17.4192.** 60° is second at 16.6692.

**Live-code step 2 — "what are 120° and 150° doing?"** **Looking across the cloud rather than along it** — camera one, the blob. Spreads of 1.08 and 1.83 against 17.42, from the same five points, purely by standing somewhere else.

**Live-code step 2 — "0° gave 10.0 and 90° gave 8.5. What are those two numbers?"** **The variances of the two original columns.** Three of the six (0°, 30°, 60°) beat "hours slept"; two (30°, 60°) beat "hours studied". **There was a better axis available than either column we were handed.**

**Live-code step 3 — "we said 30°, it says 42.62°. Were we wrong?"** **No — we were coarse.** Best of six, 12.62° short, and it cost `18.2812 − 17.4192 = 0.8620` of spread.

**Live-code step 3 — "so what would you do about it?"** **A finer grid.** Every whole degree gives 43° with a spread of **18.2804**, within a thousandth of the exact answer.

**Live-code step 3 — "the two new spreads, and the two old ones. What do you notice?"** `18.2812 + 0.2188 = 18.5000` and `10.0 + 8.5 = 18.5000`. **The total spread did not change; it was redistributed.** PCA is a rotation, not a compression.

**Live-code step 4 — "it says 2 is different from 13. Where did the 13 come from?"** **It is a shape mismatch**, and the two numbers are your component count and your column count. `inverse_transform` widens, so it needs the squashed table. **`transform` narrows, `inverse_transform` widens.**

**Live-code step 4 — "(12.1592, 10.827) against the real (12, 11). Is that a disaster?"** **No — about a sixth of an hour out in each direction.** 98.82% of the spread kept, and it cost a fifth of an hour per student on average (0.3414).

**Live-code step 4 — "one student came back exactly right. Which and why?"** **(8, 7), the one sitting at the mean.** The mean is the one point a single axis can always place perfectly, because it is where the axis crosses.

**Live-code step 5 — "what is PC1 on the unscaled wine?"** **It is `proline`** — a loading of 0.9998 and a 99.81% share. Twelve chemical measurements handed in, twelve discarded, no error message. **Same cause and same fix as last week's unscaled k-means.**

**Wrap — "how many components for 80% of the wine's spread?"** **5**, at a running total of 0.8016.

**Wrap — "how much of the wine data is on a two-dimensional picture?"** `0.3620 + 0.1921 = 0.5541`, so **55.41%** — and the other 44.6% is not on the page, which is why the percentage goes in every axis label.

**Wrap — "'we kept 55%' and 'we are wrong by 64% of a typical distance'. Which is true?"** **Both, about the same run.** `2.2550 ÷ 3.5180 = 0.6410`. **Report both: explained variance is the gain, reconstruction error is the cost.**

**Activity step 5 — "which angle won, and which lost?"** **30° won with 17.4192. 120° lost with 1.0808**, and on the paper it is drawn straight across the cloud.

**Variation-harder 1 — the best angle by hand.** 41° → 18.2668, 42° → 18.2791, **43° → 18.2804**, 44° → 18.2707. **It is a hill: go past the top and it gets worse again.**

**Variation-harder 2 — PC2's spread and the total.** PC2 sits at `42.62 + 90 = 132.62°` with spread **0.2188**, and `18.2812 + 0.2188 = 18.5000 = 10.0 + 8.5`. ✅

**Variation-harder 3 — rebuild (12, 11) by hand.** Score `5.6520`. `5.6520 × 0.7359 = 4.1593`, `5.6520 × 0.6771 = 3.8270`. Add the means: `(12.1593, 10.8270)`. Miss `√(0.1593² + 0.1730²) = √(0.02538 + 0.02993) = √0.05531 = 0.2352` — matching `inverse_transform`'s `0.2351` to three decimals, the difference being rounding in the hand values.

**Variation-harder 4 — make the cloud round.** The two explained-variance shares come out much closer together, because there is no clearly widest direction. **PCA is worth nothing on data that is already round**, and knowing when a tool has nothing to offer is a real skill.

**Variation-harder 5 — where the contrast crosses 1.0.** Between **20 and 100** columns: `1.9645` at 20 and `0.7065` at 100. Past that, the furthest pair in your dataset is less than twice as far apart as the nearest pair, and "nearest neighbour" stops being a meaningful category.

---

## 🔮 Next Week Preview

Next week is the Term 4 lab, and it is where the last two weeks meet. The student has clusters from Week 28 and a map from Week 29, and the job is to turn them into something a human being could act on: **a set of named groups, each name defended out loud from a table of feature means in the table's own units, with two independent pieces of evidence for how many groups there are.** The second piece of evidence is new: the **silhouette score**, which for one point is two averages and a subtraction — how far you are from your own clustermates, against how far you are from the nearest other cluster — and for point C on last week's six points it works out to `(7.8943 − 1.7071) ÷ 7.8943 = 0.7838`. Unlike inertia it does *not* automatically improve as `k` grows, so it can actually choose. On the wine data it peaks at **0.2849 at k = 3**, and the elbow's drop ratio of `381.1 ÷ 97.2 = 3.9` points at 3 as well — **two independent methods agreeing, which is the evidence you cite.** Then the honest part: `0.2849` is a *modest* score, the weakest of the three clusters has a mean silhouette of only **0.1774** with seven bottles scoring below zero, and the whole pipeline run on pure noise still returns three clusters with a silhouette of **0.0776**. Finally the clusters and components go to work as columns in a supervised model, and the answer is properly interesting: with 124 labelled training rows they buy **nothing at all** (54 of 54 either way), and with only 30 labelled rows they take the model from **141 of 148 to 145 of 148**.

**To prep early:** three things. **One — index cards and a thick marker pen, at least six of each.** The activity is a Naming Ceremony: each cluster's name goes on a card, gets defended out loud from the feature-means table, and **a name nobody can defend gets physically torn up and rewritten.** The tearing matters and it needs card, not paper. **Two — the SIX POINTS sheet from Week 28 comes down at the end of next week**, and its last job is the silhouette-by-hand calculation, so leave it up and leave the final centroids `(1.6667, 2.0)` and `(8, 8)` written on it. **Three — check `from sklearn.metrics import silhouette_score, silhouette_samples, adjusted_rand_score` imports tonight**, and that `silhouette_score` on the six points with labels `[0 0 0 1 1 1]` prints `0.8012`. All three ship inside scikit-learn, nothing downloads, but you want to have seen that number appear.

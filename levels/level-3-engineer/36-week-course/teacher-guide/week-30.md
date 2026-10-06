# Week 30 — Cluster Cartography

[⬅ Week 29](week-29.md) · [Course Home](../README.md) · [Week 31 ➡](week-31.md) · [Student Guide](../student-guide/week-30.md) · [Workbook](../workbook/week-30.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟩 Lab — the Term 4 build, and the first deliverable in this course that is an argument rather than a score |
| **Big idea** | **A cluster is not a result until it has a human name backed by a feature-means table — and two independent pieces of evidence for how many clusters there are.** |
| **New vocabulary** | silhouette score · adjusted Rand index (ARI) · cluster profile · elbow · cluster ID as a feature |
| **New maths** | **None new.** This week practises Week 28's squared distances, Week 29's projection, and the "compared to what?" discipline from Weeks 9, 11 and 27. The silhouette is **two averages and a subtraction**, using distances they already compute. |
| **New syntax** | `silhouette_score(X, labels)` · `silhouette_samples(X, labels)` · `adjusted_rand_score(a, b)` · `km.transform(X)` |
| **Dataset** | `load_wine()` — 178 wines, 13 columns, **scaled inside the code** — plus 178 rows of pure numpy noise as a negative control. **Nothing downloads. No internet needed.** |
| **Materials** | Printed workbook pages 30.1–30.7 · **six blank index cards and a thick marker pen** (the names get written on card, and a name nobody can defend gets torn up) · the SIX POINTS sheet from Week 28, **with its final centres still written on it** · the Bug Log |
| **Tech needed** | Laptop with Python 3, numpy, pandas, matplotlib, scikit-learn. **No torch this week. No new installs.** |
| **Prep time** | 30 minutes the night before · 10 minutes on the day |
| **Expected runtime of the code** | `cartography.py` runs in **about 2 seconds** end to end, including two saved PNGs. It fits 20-odd k-means models and nobody notices. **Time yours anyway.** |

> **⚠️ Watch out:** this week has two results that look like failures and are not. **The wine silhouette peaks at 0.2849, which is a *modest* score** — the clusters are real and they touch. And **adding the cluster and component columns to a supervised model with 124 labelled training rows buys exactly nothing: 54 of 54 either way.** Both of those are the lesson. If you present 0.2849 as "well-separated clusters" you are teaching the class to oversell, and if you skip the 54-of-54 you are hiding the single most useful finding of the day, which is that **a new feature can only help where there is room to improve.** Cut the training set to 30 rows and the same five columns take the model from 141 of 148 to 145 of 148. **Same features, same data, opposite verdict, and the reason is the row count.**

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Choose `k` using both the inertia elbow and the silhouette score**, quote both numbers, and say what to do when the two disagree.
2. **Explain why the elbow alone can never be trusted**, using the fact that inertia always falls as `k` grows — and name the `k` at which it reaches exactly zero.
3. **Give every cluster a human name and defend each one out loud from a feature-means table in the original units** — pointing at specific numbers against the overall mean, not at the cluster number.
4. **Turn cluster IDs and principal components into columns for a supervised model** and report whether they helped, **with the before and after number and the held-out pile named.**

Observable evidence: page 30.3 with `381.1 ÷ 97.2 = 3.9` and `0.2849 at k = 3` written side by side as two independent votes; three index cards each carrying a name and three numbers that justify it; a feature-means table in the original units with an overall column; and a sentence of the form *"13 raw columns got 141 of 148 held-out wines, 18 columns got 145 of 148, so the five new columns bought 4 wines, and both were fitted on the 30 training rows only."*

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each one carries on from the one above. **The complete runnable file is in the Prep Checklist and the Answer Key.**

**This is a lab, so most of the seventy minutes is the student building.** What your prep has to buy is confidence about four numbers that are all less flattering than a textbook would show, plus one idea — the negative control — that almost nobody teaches and that makes the whole subject honest.

### 1. The silhouette score: two averages and a subtraction

Week 28 left a hole on purpose. Inertia always falls as `k` grows, so it can never choose `k`. Here is a number that can.

> **Silhouette score, for one point** — how much closer that point is to its own clustermates than to the nearest other cluster, scaled to run from −1 to +1.
>
> `a` = the average distance from the point to the **other** members of its own cluster
> `b` = the average distance from the point to **every** member of the nearest other cluster
> `s = (b − a) ÷ whichever of a and b is bigger`

**And here it is worked all the way out, on point C from Week 28's six points**, which is why the SIX POINTS sheet needed to stay up. The final clusters were `{A, B, C}` and `{D, E, F}`, and **this time we do need real distances, not squared ones**, so there are square roots.

```text
a(C) — distance to the other members of my own cluster:
    C(2,3) to A(1,2):  √(1² + 1²) = √2 = 1.4142
    C(2,3) to B(2,1):  √(0² + 2²) = √4 = 2.0000
    a = (1.4142 + 2.0000) ÷ 2 = 1.7071

b(C) — distance to every member of the other cluster:
    C(2,3) to D(8,8):  √(36 + 25) = √61 = 7.8102
    C(2,3) to E(9,7):  √(49 + 16) = √65 = 8.0623
    C(2,3) to F(7,9):  √(25 + 36) = √61 = 7.8102
    b = (7.8102 + 8.0623 + 7.8102) ÷ 3 = 7.8943

s(C) = (7.8943 − 1.7071) ÷ 7.8943
     = 6.1872 ÷ 7.8943
     = 0.7838
```

![One point's silhouette is two averages and a subtraction](../figures/fig-w30-5-silhouette-a-and-b-for-one-point.svg)
*Figure 30.1 — One point's silhouette is two averages and a subtraction. a = 1.7071 from C's own clustermates, b = 7.8943 from the other cluster, and (7.8943 − 1.7071) ÷ 7.8943 = 0.7838.*

And `silhouette_samples` on those six points prints, in order:

```text
[0.8478 0.8163 0.7838 0.8384 0.7618 0.7595]
```

**The third number is 0.7838. Exactly what we computed.** That match is the best two minutes of the lesson, and it is why the sheet stayed up.

**How to read the number:**

| s | what it means |
|---|---|
| near **+1** | comfortably inside its own cluster, far from the others |
| near **0** | sitting on the border between two clusters |
| **negative** | **probably in the wrong cluster** — it is closer to a different one |

**And the demonstration that makes "negative" concrete.** Take those same six points and group them deliberately stupidly — put B in with D, E and F:

```text
a deliberately silly grouping [0 1 0 1 1 1] -> silhouette 0.3751
per point: [ 0.8068 -0.8163  0.7797  0.5284  0.487   0.4646]
```

**B scores −0.8163.** The number is telling you, without ever having been shown a right answer, that **that point is in the wrong place.** That is genuinely the most impressive thing in this week, and it takes four lines of code.

> **Silhouette score, for a whole clustering** — the average of `s` over every point. `silhouette_score(X, labels)` gives you it directly. For the good grouping of six points: **0.8012**. For the silly one: **0.3751**.

**The crucial property, and the reason this exists:** unlike inertia, **the silhouette does not automatically improve as `k` grows.** It has a genuine peak, so you can pick the `k` that maximises it. That is what makes it a second, independent vote.

**And the field guide, which you should quote honestly rather than generously:**

| silhouette | honest description |
|---|---|
| above 0.5 | strong structure |
| 0.25 to 0.5 | **real, but the clusters touch** |
| below 0.25 | mostly a convenient fiction |

**Real tabular data lands in the 0.25–0.4 band most of the time, and the wine data lands at 0.2849.** That is *"real but overlapping"*, and saying so is the finding. It is not a disappointment.

### 2. Two votes for `k`, and what to do when they disagree

Here is the real sweep on the 178 scaled wines:

```text
   k    inertia      drop   silhouette
   1     2314.0         -            -
   2     1659.0     655.0       0.2683
   3     1277.9     381.1       0.2849
   4     1180.7      97.2       0.2457
   5     1110.4      70.4       0.2026
   6     1044.5      65.9       0.1960
   7      996.0      48.5       0.1386
   8      944.6      51.4       0.1581
   9      913.2      31.4       0.1417
  10      864.6      48.6       0.1338
```

**Read the two evidence columns separately, and then together.**

**The elbow.** The drops go 655, 381, then a cliff to 97, then a trickle: 70, 66, 48, 51, 31, 49. The quantity to report is the **ratio**, not the picture:

```text
381.1 ÷ 97.2 = 3.9
```

The third cluster bought nearly four times what the fourth did. **After that, the extra clusters are all worth about the same as each other, which is what "no more structure to find" looks like in numbers.**

**The silhouette.** It rises from 0.2683 at `k=2` to **0.2849 at `k=3`**, then falls away steadily. **It has a peak, and the peak is at 3.**

![Two pieces of evidence, and they agree](../figures/fig-w30-1-elbow-and-silhouette-side-by-side.svg)
*Figure 30.2 — Two pieces of evidence, and they agree. Inertia falls from 2314.0 to 864.6 with a cliff at k = 3; the silhouette peaks at 0.2849 at k = 3 and falls to 0.1338 by k = 10.*

**Both say 3, and that agreement is the thing you cite.** Not "the graph bends at 3". *"The drop ratio is 3.9 and the silhouette peaks at 0.2849, both at k = 3."*

**Notice the small bump at `k = 8`** — the silhouette goes 0.1386, then back up to 0.1581. **That is noise, not structure**, and the giveaway is that it does not come anywhere near the `k=3` value. A student who spots it and says "but 8 is better than 7!" has read the table properly and needs the one-sentence answer: *"it is higher than its neighbour and far below the peak; a bump that does not beat the maximum is not a finding."*

**And now the part that matters most for the objectives — what to do when the two disagree.** They will, often. The honest position is that **the two tools fail in different directions, so a disagreement is itself information:**

- **The elbow tends to over-count** when clusters are unequal in size, because splitting a big loose cluster always buys a lot of inertia.
- **The silhouette tends to under-count** when clusters touch. When two neighbouring groups overlap, the points near the border have `a` almost equal to `b`, so their individual scores collapse towards 0 and drag the average down. **Merging the two removes that border and its low-scoring points, so the average goes up.** So silhouette has a built-in preference for fewer, fatter clusters exactly when clusters are adjacent.

**So: silhouette pulling lower than the elbow is the signature of overlapping clusters**, and that sentence belongs in the write-up. And there is a third consideration that outranks both:

> **Domain sense wins.** If the elbow says 4, the silhouette says 2, and the marketing team can only run three campaigns, the answer is **3**. Clustering is a tool for making decisions, and the number of decisions you can act on is a real constraint. **Say so in the write-up rather than pretending the maths decided.**

### 3. The profile table, and the Naming Ceremony

This is objective 3 and it is the heart of the lab. **A cluster ID is useless to a human being. A name with three numbers behind it is a decision they can act on.**

Two non-negotiable rules for the table:

**One: original units, never z-scores.** Nobody can read "alcohol = 0.83". Everybody can read "alcohol = 13.68 against an overall average of 13.00".

**Two: an overall column.** A cluster mean on its own means nothing — `flavanoids = 0.82` is only interesting because the overall mean is 2.03. **This is the "compared to what?" discipline from Week 27, applied to a table instead of a score.**

Here is the real thing:

```text
feature means by cluster, in the ORIGINAL units:
cluster                            0       1        2  overall
alcohol                        12.25   13.13    13.68    13.00
malic_acid                      1.90    3.31     2.00     2.34
ash                             2.23    2.42     2.47     2.37
alcalinity_of_ash              20.06   21.24    17.46    19.49
magnesium                      92.74   98.67   107.97    99.74
total_phenols                   2.25    1.68     2.85     2.30
flavanoids                      2.05    0.82     3.00     2.03
nonflavanoid_phenols            0.36    0.45     0.29     0.36
proanthocyanins                 1.62    1.15     1.92     1.59
color_intensity                 2.97    7.23     5.45     5.06
hue                             1.06    0.69     1.07     0.96
od280/od315_of_diluted_wines    2.80    1.70     3.16     2.61
proline                       510.17  619.06  1100.23   746.89
```

**And the three names, each with its evidence:**

| cluster | n | the numbers that justify it | the name |
|---|---:|---|---|
| **2** | 62 | highest alcohol (13.68 vs 13.00), highest flavanoids (3.00 vs 2.03), highest proline (1100 vs 747), highest phenols (2.85 vs 2.30) | **Bold Reserve** |
| **1** | 51 | lowest flavanoids (0.82 vs 2.03), highest colour intensity (7.23 vs 5.06), lowest hue (0.69 vs 0.96), highest malic acid (3.31 vs 2.34) | **Dark & Tannic** |
| **0** | 65 | lowest alcohol (12.25 vs 13.00), lowest colour intensity (2.97 vs 5.06), lowest proline (510 vs 747), lowest magnesium (92.7 vs 99.7) | **Light & Pale** |

![A name you can defend from the table](../figures/fig-w30-3-feature-means-table-naming-a-cluster.svg)
*Figure 30.3 — A name you can defend from the table. Cluster 1: flavanoids 0.82 against 2.03 overall, colour 7.23 against 5.06, hue 0.69 against 0.96. And alcohol 13.13 against 13.00 defends nothing.*

**The trap in that table, and it is the one to mark hardest.** Look at cluster 1's `alcohol`: **13.13 against an overall 13.00.** A student will put it in their justification because it is "above average". **It is 0.13 above average and it defends nothing.** A number only defends a name if it is *far* from the overall mean — and "far" here can be judged by eye against the other columns.

**And the honest finding about cluster 0, which is also objective 3's hardest part:**

```text
cluster 0: n= 65   own silhouette 0.1774   worst point -0.0228   points below 0: 7
cluster 1: n= 51   own silhouette 0.3506   worst point 0.0611    points below 0: 0
cluster 2: n= 62   own silhouette 0.3434   worst point 0.0352    points below 0: 0
```

**Cluster 0's own silhouette is 0.1774 — half of the other two — and seven of its sixty-five bottles score below zero**, which means they are closer to a different cluster than to their own.

**And look at why, in the profile table: cluster 0 is *lowest* on almost everything and highest on nothing.** "Low on things" is a much weaker basis for a group than "high on a specific thing". **A cluster defined mainly by absence is often a sign that `k` is too small, or that the real structure is two strong groups plus a continuum of leftovers.** Say that. Do not hide the weak cluster, and do not pretend the three names are equally good.

### 4. Stability, and the negative control that almost nobody runs

You cannot check clusters against a right answer. But you can check two other things, and both are real evidence.

> **Adjusted Rand index (ARI)** — how much two groupings of the same rows agree, corrected for the agreement you would get by luck. **1.0 means identical grouping. 0.0 means no better than random.**

**The crucial thing about ARI is that it ignores the cluster numbers entirely.** It compares *which rows are together*, not what those groups are called. So it is exactly the tool for Week 28's question *"cluster 0 means something different every run — is it broken?"*

**Check one: does it survive a different seed?**

```text
five different seeds, ARI against our run: [1. 1. 1. 1. 1.]  mean 1.0000
```

**Perfectly stable.** Five different starting positions, five identical groupings.

**Check two: does it survive losing a fifth of the data?**

```text
five 80% subsamples, ARI     : [0.9775 0.9565 0.9775 0.9168 1.    ]  mean 0.9657
```

**Mean 0.9657.** Take away 36 of the 178 bottles and the grouping barely moves. **The rule of thumb: a mean subsample ARI below about 0.7 means your structure is fragile and you must say so.** 0.9657 is strong.

**And now the thing that makes the whole subject honest.**

> **Negative control** — run your entire pipeline, unchanged, on data you *know* has no structure in it. Whatever it reports is your floor.

```text
--- the negative control: 178 rows of 13 columns of pure noise ---
sizes [62 44 72]   silhouette 0.0776
noise, five seeds, ARI: [0.6407 0.4069 0.61   0.6072 0.6308]  mean 0.5791
```

**Read both numbers against the real ones.**

| | real wine | pure noise |
|---|---:|---:|
| silhouette at k = 3 | **0.2849** | **0.0776** |
| seed-to-seed ARI | **1.0000** | **0.5791** |

**The silhouette is 3.7 times higher on the real data, and the stability is perfect against only moderate agreement on noise (0.58, far below 1.0).** *That* is the argument that the wine structure is real. **Not "0.2849 is a good score" — it is not a good score — but "0.2849 against a noise floor of 0.0776, with an ARI of 1.0000 against 0.5791."**

And the sting: **the noise data still produced three tidy clusters with visibly different column means**, so you could have written a profile table and invented names for them. **The negative control is the only thing standing between "I found three customer types" and "my algorithm returns three of whatever I ask it for".** Almost no published clustering write-up includes one.

**And because the wine data does have hidden labels, we get one bonus check nobody normally gets:**

```text
adjusted_rand_score against the real grape variety: 0.8975
rows = real variety, columns = our cluster
[[ 0  0 59]
 [65  3  3]
 [ 0 48  0]]
```

**ARI 0.8975, with only 6 of 178 bottles misplaced** — and notice the cluster numbers do not match the variety numbers at all: cluster 2 is variety 0, cluster 0 is variety 1, cluster 1 is variety 2. **ARI does not care, which is exactly the point of it.** A silly grouping — everything in one cluster — scores **0.0**, and a random grouping scores **−0.0088**.

### 5. Do the new columns earn their keep? The honest answer is "it depends on the row count"

Objective 4. Both `KMeans` and `PCA` produce columns you can feed to a supervised model.

> **`km.transform(X)`** — not the labels, but **the distance from every row to every centre.** With 3 clusters that is 3 new numeric columns per row. **Better than the cluster ID**, because it keeps *how strongly* a row belongs instead of throwing that away.

```text
km.transform(X) shape: (178, 3) - one distance per centre
first three wines, distance to each of the three centres:
[[4.9629 6.2931 2.0634]
 [3.8452 5.6853 2.7400]
 [4.1901 5.6186 2.0042]]
nearest centre: [2 2 2]  and labels_ says [2 2 2]
```

**The smallest number in each row is the cluster it was assigned to.** `argmin` of `km.transform(X)` is `km.labels_`, every time, and pointing that out once makes the whole thing obvious.

> **⚠️ And never one-hot the cluster ID as a number.** `0`, `1`, `2` are names. If you must use the ID, one-hot it as in Week 4 — but the three distances are strictly more informative and they are one function call.

**Now the experiment, and here is where you have to be honest.** Split the wine into 124 training rows and 54 held-out rows, fit the scaler, the k-means and the PCA **on the training rows only**, and build an 18-column table: the 13 scaled columns, plus 3 centre-distances, plus 2 principal components.

```text
--- 124 labelled training rows: is there room to improve? ---
train rows: 124   held-out rows: 54
  13 raw columns        1.0000  (54 of 54 held-out wines)
  13 + 3 dists + 2 PCs  1.0000  (54 of 54 held-out wines)
  the 5 new ones ALONE  1.0000  (54 of 54 held-out wines)
```

**All three get 54 of 54. There was no room to improve, so nothing could.** That is not a failed experiment, it is a **ceiling**, and recognising a ceiling is a real skill. **A student who reports "the cluster features didn't help" from this table has drawn the wrong conclusion** — the correct one is *"this problem was already solved, so this experiment cannot answer the question."*

**So make the problem hard.** Keep only **30** labelled training rows, and hold out the other 148:

```text
--- now only 30 labelled training rows, 148 held out ---
  13 raw columns        0.9527  (141 of 148 held-out wines)
  13 + 3 dists + 2 PCs  0.9797  (145 of 148 held-out wines)
  the 5 new ones ALONE  0.9865  (146 of 148 held-out wines)
```

**Three findings, and all three are worth saying.**

**One: the five new columns bought 4 wines.** 141 → 145, `+2.70` accuracy points. **Say it as a count, not only a percentage** — Week 27's discipline.

**Two, and this is the striking one: the five new columns *on their own* beat all thirteen original ones.** 146 against 141. **Five numbers built without ever looking at a label did better than thirteen carefully measured chemical properties** — because with 30 labelled rows, a 13-column logistic regression has 42 coefficients to estimate and not enough rows to do it, while k-means got to use all 30 rows' *geometry* with no labels at all.

**Three, and you must include it: is +4 wines real, or noise?** The honest check is to repeat the split. Over ten different splits:

```text
13 raw        mean 0.9642  std 0.0125
18 cols       mean 0.9757  std 0.0075
5 unsup only  mean 0.9716  std 0.0095
mean gain from adding the five columns: +0.0115
times the 18-column model was better/equal/worse: 8 2 0
```

**The average gain is +1.15 points, which is smaller than the single split suggested and comparable to the baseline's own split-to-split wobble of 0.0125.** But **the 18-column model won 8 times, tied twice, and never lost.** *That* is the evidence: not the size of the gain, but that it never went the other way. **This is exactly the Week 11 "is this difference real?" move, and it is the last time in the course you get to practise it before the capstone.**

![Five new columns, made without ever looking at the answers](../figures/fig-w30-4-cluster-id-as-a-new-feature.svg)
*Figure 30.4 — Five new columns, made without ever looking at the answers. (30, 13) becomes (30, 18), and 141 of 148 becomes 145 of 148 — all five new columns fitted on the 30 training rows only.*

**⚠️ And the leakage rule, which applies with full force.** `StandardScaler`, `KMeans` and `PCA` all **fit** — they learn means, centres and directions from data. Fit any of them on all 178 rows before splitting and **information from your held-out wines has leaked into your training columns.** The code in this file fits all three on the training rows only, and it is worth pointing at that line out loud. **This is Week 6's leakage, in an unsupervised costume, and it is the last new costume the course will show you.**

### 6. The map

```text
saved wine_map.png
```

Last week's plot, coloured by cluster. **Two rules it has to obey, and both are habits from Week 29:**

**The percentage goes in both axis labels.** `PC1 (36.2% of the spread)` and `PC2 (19.2%)`. `36.2 + 19.2 = 55.4`, so **44.6% of the wine's spread is not on the page**, and two bottles that look adjacent may be far apart.

**Cluster membership gets a shape as well as a colour** — circle, triangle, square — so the map still works photocopied.

![The map: 178 wines, three clusters, two axes](../figures/fig-w30-2-pca-scatter-coloured-by-cluster.svg)
*Figure 30.5 — The map: 178 wines, three clusters, two axes. 65 circles, 51 triangles, 62 squares, three centres marked with crosses, and 36.2 + 19.2 = 55.4% of the spread drawn.*

**And the thing to notice out loud, because it is the payoff for last week:** the uncoloured version of this plot, from Week 29, was **one elongated blob with no visible gaps.** Coloured by cluster, three groups appear cleanly. **The structure was there all along and the picture could not show it, which is exactly why you need a number and not a picture.**

### 7. Every new line of this week's code, explained to somebody who has never programmed

**New line 1 — one number for a whole clustering.**

```python
silhouette_score(X, labels)
```

Two things go in: the table you clustered, and the labels you got. One number comes out, between −1 and +1, and **it is the average of every point's own score.** Note what is *not* in there: no `y`, no right answer. **It measures the shape of the grouping, not its correctness.**

**New line 2 — one number per point.**

```python
silhouette_samples(X, labels)
```

Same arguments, but one number per row instead of one overall. **This is the one that finds the weak cluster**, because you can average it *within* each cluster and compare. And `silhouette_samples(X, labels).mean()` equals `silhouette_score(X, labels)` exactly — worth printing once as a check that you have understood what the average is over.

**New line 3 — do two groupings agree?**

```python
adjusted_rand_score(a, b)
```

Two labellings of the same rows. One number: 1.0 for identical grouping, 0.0 for no better than chance, and it can go slightly negative. **It ignores the numbers completely and only looks at which rows are grouped together**, which is why it can compare run 1's cluster 0 against run 2's cluster 2 without complaining. **Argument order does not matter** — `adjusted_rand_score(a, b)` equals `adjusted_rand_score(b, a)` — which is unusual and worth saying, because almost every other two-argument metric in this course cares.

**New line 4 — distances, not labels.**

```python
km.transform(X)
```

A table with one row per data row and **one column per centre**, holding the distance from that row to that centre. `(178, 3)` for the wine. **`km.transform(X).argmin(axis=1)` is `km.labels_`** — which is the sentence that makes the whole thing click. Use the distances rather than the ID as features whenever you can.

### 8. The three misconceptions you will actually meet

**Misconception 1 — "0.2849 means we found good clusters."**
0.2849 is in the "real but overlapping" band, and the honest description is exactly that. **Cure:** the noise floor. `0.0776` on pure random numbers. **0.2849 is 3.7 times the floor, which is the claim you can actually make.**

**Misconception 2 — "the cluster features didn't help, so they are useless."**
They did not help on a problem that was already at 54 of 54. **Cure:** the 30-row version. 141 → 145, and 146 for the five new columns alone. **The right question is never "does this feature help" but "help with what, on how many rows?"**

**Misconception 3 — "we named the clusters, so the groups exist."**
You named a statistical boundary, and names are sticky. **Cure:** run the negative control and then name *those* three clusters. It is easy, which is the point. And **for the ethical version, ask what happens if these are people rather than bottles.**

### 9. How deep to go, and where to stop

**Go this far:** the silhouette for one point by hand, matching `silhouette_samples`; the negative score for a deliberately misplaced point; the elbow-ratio and silhouette-peak as two independent votes, both saying 3; what to do when they disagree, and which way each tool is biased; the profile table in original units with an overall column; three defended names and one honestly weak cluster; stability across seeds and subsamples with ARI; the negative control on noise; the map with percentages in the labels and shapes as well as colours; and the supervised experiment at 124 rows and at 30 rows, with the split named on every row.

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| Other clustering algorithms — DBSCAN, hierarchical, Gaussian mixtures | Not in this level. One sentence if asked: *"there are dozens; they mostly differ in what shape of cluster they can find, and k-means only ever finds round blobs."* |
| The formula behind ARI's "adjusted" | Not in this level. *"It subtracts off how much two groupings would agree by pure luck, so random scores 0 instead of something positive."* **That is a complete answer.** |
| `FeatureUnion`, `ColumnTransformer` gymnastics to bolt clusters into a pipeline | Not needed. **We use one named split and `np.c_`**, which is Week 19's syntax, and it makes the fit-on-train-only step visible instead of hiding it. |
| t-SNE and UMAP for prettier maps | Not in this level. *"They make better-looking pictures and are much harder to interpret; PCA is the one you can explain."* |
| Semi-supervised learning, pseudo-labelling | Not in this level, although the 30-row result is a door onto it. **If a student walks through that door, they have had an excellent idea and should be told so.** |
| Text data | **Next week.** Week 31 starts natural language. |

The line to hold in your head all lesson: **today the student produces the first deliverable in this course that is an argument rather than a score.**

---

### 10. 🧭 The Growing Map — the same box, and the first deliverable that is an argument

The student guide carries a figure called **Where This Fits**: the same picture every week with one more
piece filled in. Nothing moves this week either; what the two minutes buy is the point that today's
output is not a score.

![The Level 3 pipeline in Week 30: still the no labels and words tile, now clusters with names they can defend](../figures/fig-w30-0-where-this-fits.svg)

*Figure 30.0 — Week 30's version. Third week inside the gold `no labels · words` tile. The ↻ on stage
three is black, as it has been since Week 12.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Ask "which box did we do today?" and then hold up an index card.** Same gold tile, third week — and
   the deliverable is in your hand. *"Week 28 produced cluster 0, cluster 1 and cluster 2. Today this box
   produced a **name**, and three numbers underneath it that a stranger could argue with."* If a card got
   torn up in the ceremony, that is the best thing to point at.
2. **Anchor it on the two votes.** `381.1 ÷ 97.2 = 3.9` from the elbow, `0.2849` at `k = 3` from the
   silhouette, and `0.0776` from pure noise. *"Which of those three numbers made the other two mean
   anything?"* — the noise floor. That is the sentence to end the week on, and it is the same "compared
   to what?" move as Weeks 9, 11 and 27, three boxes to the left on the map.
3. **Point at stage one and at stage two, and make them earn it.** Adding five new columns is an
   ablation: one change, one measurement, one row, and the held-out pile named — `54 of 54` on 124
   training rows, `141 → 145 of 148` on 30. *"Same features, opposite verdict, and the reason is in
   stage one, not stage five."* They should be pointing left while they say it.

> **🧑‍🏫 Why this is worth two minutes.** Every previous lab in this course ended with a number that was
> either better or worse than another number. This one ends with three names on card and a table, and
> some students will genuinely not believe that counts as work. The map is where you say it does: **the
> tile has not moved, the stage is solid, and this is what this part of the pipeline produces.** Use the
> torn-up card as the proof that it is still assessable.

**One thing to notice, so you can answer if asked.** `evaluation` is lit in a week with no `y` for most
of the lesson, which looks wrong and is not. **The negative control is evaluation in its purest form**:
run the whole pipeline on data you know is meaningless and whatever it reports is your floor. If a
student asks how you can evaluate something with no answer key, that is the best question of the term —
the answer is that you cannot score it, but you can absolutely measure whether it beats noise.

---

## 🧰 Prep Checklist

This section lists what to do before the lesson, and holds the complete runnable file.

### 30 minutes the night before

- [ ] **Do the silhouette for point C by hand.** Five square roots, two averages, one subtraction, one division: **0.7838**. **Five minutes, and you are going to lead it at the SIX POINTS sheet.**
- [ ] **Type and run `cartography.py` yourself.** The complete file:

```python
"""cartography.py - Week 30: choose k twice, name the clusters, then test them."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (adjusted_rand_score, confusion_matrix,
                             silhouette_samples, silhouette_score)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

np.random.seed(0)
pd.set_option("display.width", 130)

wine = load_wine()
X_raw = pd.DataFrame(wine.data, columns=wine.feature_names)
y_secret = wine.target                      # stays in the drawer until step 6
X = StandardScaler().fit_transform(X_raw)
print("wine table:", X_raw.shape)

# ---------- 1. two pieces of evidence for k ----------
print()
print("   k    inertia      drop   silhouette")
prev = KMeans(n_clusters=1, n_init=10, random_state=0).fit(X).inertia_
print("   1   %8.1f         -            -" % prev)
ks, inertias, sils = [], [], []
for k in range(2, 11):
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    s = silhouette_score(X, km.labels_)
    print("  %2d   %8.1f   %7.1f       %.4f" % (k, km.inertia_, prev - km.inertia_, s))
    ks.append(k); inertias.append(km.inertia_); sils.append(s)
    prev = km.inertia_

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot([1] + ks, [2314.0] + inertias, "o-")
ax[0].set_xlabel("k"); ax[0].set_ylabel("inertia"); ax[0].set_title("Elbow")
ax[1].plot(ks, sils, "o-", color="darkorange")
ax[1].set_xlabel("k"); ax[1].set_ylabel("mean silhouette")
ax[1].set_title("Silhouette")
plt.tight_layout(); plt.savefig("choose_k.png", dpi=110); plt.close()
print("saved choose_k.png")

# ---------- 2. cluster at k = 3, and look at each cluster honestly ----------
km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
labels = km.labels_
sil = silhouette_samples(X, labels)
print()
print("cluster sizes:", np.bincount(labels))
for c in range(3):
    m = labels == c
    print("  cluster %d: n=%3d   own silhouette %.4f   worst point %.4f   points below 0: %d"
          % (c, m.sum(), sil[m].mean(), sil[m].min(), int((sil[m] < 0).sum())))
print("  whole-set silhouette: %.4f" % silhouette_score(X, labels))

# ---------- 3. the profile, in the units a person can read ----------
print()
prof = X_raw.copy()
prof["cluster"] = labels
means = prof.groupby("cluster").mean().T
means["overall"] = X_raw.mean()
print("feature means by cluster, in the ORIGINAL units:")
print(means.round(2).to_string())

# ---------- 4. the map ----------
pca = PCA(n_components=2).fit(X)
Z = pca.transform(X)
evr = pca.explained_variance_ratio_
names = {0: "Light & Pale", 1: "Dark & Tannic", 2: "Bold Reserve"}
marks = {0: "o", 1: "^", 2: "s"}
plt.figure(figsize=(7, 5.5))
for c in range(3):
    m = labels == c
    plt.scatter(Z[m, 0], Z[m, 1], s=34, alpha=0.85, marker=marks[c],
                label="%d: %s (n=%d)" % (c, names[c], m.sum()))
cen = pca.transform(km.cluster_centers_)
plt.scatter(cen[:, 0], cen[:, 1], marker="X", s=240, c="black", label="centres")
plt.xlabel("PC1 (%.1f%% of the spread)" % (evr[0] * 100))
plt.ylabel("PC2 (%.1f%% of the spread)" % (evr[1] * 100))
plt.title("178 wines, coloured by cluster")
plt.legend(); plt.tight_layout(); plt.savefig("wine_map.png", dpi=110); plt.close()
print("saved wine_map.png")

# ---------- 5. km.transform: how strongly does a wine belong? ----------
print()
d = km.transform(X)
print("km.transform(X) shape:", d.shape, "- one distance per centre")
print("first three wines, distance to each of the three centres:")
print(np.round(d[:3], 4))
print("nearest centre:", d[:3].argmin(axis=1), " and labels_ says", labels[:3])

# ---------- 6. is the structure real? stability, then the drawer ----------
print()
ref = labels
seeds = [adjusted_rand_score(ref, KMeans(n_clusters=3, n_init=10,
                                         random_state=s).fit(X).labels_)
         for s in (1, 2, 3, 4, 5)]
print("five different seeds, ARI against our run:", np.round(seeds, 4),
      " mean %.4f" % np.mean(seeds))
rng = np.random.default_rng(0)
subs = []
for _ in range(5):
    idx = rng.choice(178, 142, replace=False)
    subs.append(adjusted_rand_score(ref[idx],
                KMeans(n_clusters=3, n_init=10, random_state=0).fit(X[idx]).labels_))
print("five 80% subsamples, ARI     :", np.round(subs, 4),
      " mean %.4f" % np.mean(subs))

print()
print("--- the negative control: 178 rows of 13 columns of pure noise ---")
noise = np.random.default_rng(0).normal(size=(178, 13))
kmn = KMeans(n_clusters=3, n_init=10, random_state=0).fit(noise)
print("sizes", np.bincount(kmn.labels_),
      "  silhouette %.4f" % silhouette_score(noise, kmn.labels_))
nseeds = [adjusted_rand_score(kmn.labels_, KMeans(n_clusters=3, n_init=10,
                                                 random_state=s).fit(noise).labels_)
          for s in (1, 2, 3, 4, 5)]
print("noise, five seeds, ARI:", np.round(nseeds, 4), " mean %.4f" % np.mean(nseeds))

print()
print("adjusted_rand_score against the real grape variety: %.4f"
      % adjusted_rand_score(y_secret, labels))
print("rows = real variety, columns = our cluster")
print(confusion_matrix(y_secret, labels))

# ---------- 7. do the new columns earn their keep? ----------
print()
print("--- 124 labelled training rows: is there room to improve? ---")
Xtr, Xte, ytr, yte = train_test_split(X_raw, y_secret, test_size=0.30,
                                      random_state=0, stratify=y_secret)
print("train rows:", len(Xtr), "  held-out rows:", len(Xte))


def run(n_train, state=0):
    a, b, ya, yb = train_test_split(X_raw, y_secret, train_size=n_train,
                                    random_state=state, stratify=y_secret)
    sc = StandardScaler().fit(a)                 # fitted on the TRAIN rows only
    Za, Zb = sc.transform(a), sc.transform(b)
    k3 = KMeans(n_clusters=3, n_init=10, random_state=0).fit(Za)
    pc = PCA(n_components=2).fit(Za)
    Aa = np.c_[Za, k3.transform(Za), pc.transform(Za)]
    Ab = np.c_[Zb, k3.transform(Zb), pc.transform(Zb)]
    Ua, Ub = np.c_[k3.transform(Za), pc.transform(Za)], np.c_[k3.transform(Zb), pc.transform(Zb)]
    out = []
    for tag, p, q in [("13 raw columns      ", Za, Zb),
                      ("13 + 3 dists + 2 PCs", Aa, Ab),
                      ("the 5 new ones ALONE", Ua, Ub)]:
        acc = LogisticRegression(max_iter=5000).fit(p, ya).score(q, yb)
        out.append(acc)
        print("  %s  %.4f  (%d of %d held-out wines)"
              % (tag, acc, round(acc * len(yb)), len(yb)))
    return out


run(124)
print()
print("--- now only 30 labelled training rows, 148 held out ---")
run(30)
```

Run `python3 cartography.py`. You must see **exactly** this:

```text
wine table: (178, 13)

   k    inertia      drop   silhouette
   1     2314.0         -            -
   2     1659.0     655.0       0.2683
   3     1277.9     381.1       0.2849
   4     1180.7      97.2       0.2457
   5     1110.4      70.4       0.2026
   6     1044.5      65.9       0.1960
   7      996.0      48.5       0.1386
   8      944.6      51.4       0.1581
   9      913.2      31.4       0.1417
  10      864.6      48.6       0.1338
saved choose_k.png

cluster sizes: [65 51 62]
  cluster 0: n= 65   own silhouette 0.1774   worst point -0.0228   points below 0: 7
  cluster 1: n= 51   own silhouette 0.3506   worst point 0.0611   points below 0: 0
  cluster 2: n= 62   own silhouette 0.3434   worst point 0.0352   points below 0: 0
  whole-set silhouette: 0.2849

feature means by cluster, in the ORIGINAL units:
cluster                            0       1        2  overall
alcohol                        12.25   13.13    13.68    13.00
malic_acid                      1.90    3.31     2.00     2.34
ash                             2.23    2.42     2.47     2.37
alcalinity_of_ash              20.06   21.24    17.46    19.49
magnesium                      92.74   98.67   107.97    99.74
total_phenols                   2.25    1.68     2.85     2.30
flavanoids                      2.05    0.82     3.00     2.03
nonflavanoid_phenols            0.36    0.45     0.29     0.36
proanthocyanins                 1.62    1.15     1.92     1.59
color_intensity                 2.97    7.23     5.45     5.06
hue                             1.06    0.69     1.07     0.96
od280/od315_of_diluted_wines    2.80    1.70     3.16     2.61
proline                       510.17  619.06  1100.23   746.89
saved wine_map.png

km.transform(X) shape: (178, 3) - one distance per centre
first three wines, distance to each of the three centres:
[[4.9629 6.2931 2.0634]
 [3.8452 5.6853 2.74  ]
 [4.1901 5.6186 2.0042]]
nearest centre: [2 2 2]  and labels_ says [2 2 2]

five different seeds, ARI against our run: [1. 1. 1. 1. 1.]  mean 1.0000
five 80% subsamples, ARI     : [0.9775 0.9565 0.9775 0.9168 1.    ]  mean 0.9657

--- the negative control: 178 rows of 13 columns of pure noise ---
sizes [62 44 72]   silhouette 0.0776
noise, five seeds, ARI: [0.6407 0.4069 0.61   0.6072 0.6308]  mean 0.5791

adjusted_rand_score against the real grape variety: 0.8975
rows = real variety, columns = our cluster
[[ 0  0 59]
 [65  3  3]
 [ 0 48  0]]

--- 124 labelled training rows: is there room to improve? ---
train rows: 124   held-out rows: 54
  13 raw columns        1.0000  (54 of 54 held-out wines)
  13 + 3 dists + 2 PCs  1.0000  (54 of 54 held-out wines)
  the 5 new ones ALONE  1.0000  (54 of 54 held-out wines)

--- now only 30 labelled training rows, 148 held out ---
  13 raw columns        0.9527  (141 of 148 held-out wines)
  13 + 3 dists + 2 PCs  0.9797  (145 of 148 held-out wines)
  the 5 new ones ALONE  0.9865  (146 of 148 held-out wines)
```

**Expected runtime: about 2 seconds**, including two saved PNGs. It fits more than twenty k-means models and you will not notice.

- [ ] **Look at `wine_map.png` and at last week's `wine_2d.png` side by side.** Same points, same axes; one is a blob and one has three groups in it. **You are going to show them both, in that order, and it is the best thirty seconds of the wrap.**
- [ ] **Decide now what you will say about `0.2849`.** The honest words are *"real, but the clusters touch"*, and the number that makes it a finding is the noise floor of `0.0776`. **Do not let yourself say "well-separated" — the class will copy whatever you say.**
- [ ] **Break it on purpose, twice.** First the loud one:

```python
print(silhouette_score(X, np.zeros(178)))
```

```text
ValueError: Number of labels is 1. Valid values are 2 to n_samples - 1 (inclusive)
```

Then the silent one — cluster **without** scaling and score it in its own units:

```python
km_raw = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X_raw)
print("clustered raw,    scored raw    : %.4f" % silhouette_score(X_raw, km_raw.labels_))
print("clustered scaled, scored scaled : %.4f" % silhouette_score(X, labels))
print()
print("ARI against the real grape variety, raw    : %.4f"
      % adjusted_rand_score(wine.target, km_raw.labels_))
print("ARI against the real grape variety, scaled : %.4f"
      % adjusted_rand_score(wine.target, labels))
```

```text
clustered raw,    scored raw    : 0.5711
clustered scaled, scored scaled : 0.2849

ARI against the real grape variety, raw    : 0.3711
ARI against the real grape variety, scaled : 0.8975
```

**Read those four numbers together, because this is the sharpest thing in the whole lesson. The unscaled clustering scores 0.5711 — twice the scaled one, and squarely in the "strong structure" band — and it is far worse.** ARI 0.3711 against 0.8975. **A higher silhouette does not mean a better clustering.** The unscaled clusters are beautifully separated, because they are three bands of proline and nothing on earth is tidier than three bands of one column. **That is deliberate mistake two.**

- [ ] **Print workbook pages 30.1–30.7.**
- [ ] **Get six blank index cards and a thick marker.** **The tearing-up matters and it does not work on a sheet of A4.**
- [ ] **Check the SIX POINTS sheet is still up**, with the final centres `(1.6667, 2.0)` and `(8, 8)` on it. **Its last job is today's silhouette-by-hand, and then it comes down.**
- [ ] **Have the student's Week 28 and Week 29 files on disk.** Today's lab starts from `no_answer_key.py` and `new_axes.py`, and a broken file turns a five-minute recap into twenty.

### 10 minutes on the day

- [ ] Six index cards and the marker on the front desk, visible.
- [ ] SIX POINTS sheet up, final centres written on it.
- [ ] Editor open, `cartography.py` **partly given** — hand them the imports, the data load, the scaler and the `run()` helper complete, because they wrote all of those in Weeks 28 and 29. **They type the silhouette sweep, the profile table and the negative control themselves** — those are the new lines.
- [ ] Workbook 30.1 out. **The prediction — which `k`, and will the two methods agree — filled in, in pen, before anything runs.**
- [ ] Bug Log out.
- [ ] Last week's `wine_2d.png` open in a window, ready to put next to today's map.

### Fallback if the laptops fail

**Three of the four objectives survive on paper, and objective 3 — the Naming Ceremony — is *better* without screens.**

1. **The silhouette by hand, at the SIX POINTS sheet.** Five square roots, two averages, one subtraction: `0.7838`. **Then the silly grouping, and B's `−0.8163`.** Objectives 1 and 2's understanding, with a calculator.
2. **The two-votes table, printed from this file.** They read the drop column, compute `381.1 ÷ 97.2 = 3.9`, find the silhouette peak at `0.2849`, and write both down as two independent votes for `k = 3`. **Objective 1, complete, on paper.**
3. **The Naming Ceremony, unchanged.** Print the profile table. Index cards, marker, three names, each defended out loud from the numbers. **Objective 3, complete, and honestly it goes better without laptops because nobody is fiddling.**
4. **Objective 4 is the casualty.** Give them the numbers — `141 of 148` against `145 of 148`, on 30 training rows — and have them write the sentence with the pile named. **The sentence is most of the objective; the measurement is the part that needs a machine.**

| If this fails | Do this instead |
|---|---|
| The silhouette sweep takes a long time | It should take under two seconds for all nine values of `k`. If it crawls, you are fitting inside a loop inside a loop. **Print `k` as you go so you can see it moving.** |
| A student's silhouette is 0.5711 and they are delighted | **They clustered without scaling.** Three bands of proline score beautifully on separation. **Ask: "and what is its ARI against the real varieties?"** 0.3711, against the scaled clustering's 0.8975. |
| `ValueError: Number of labels is 1` | They passed all-zeros, or `k=1`. **The silhouette needs at least two clusters — with one cluster there is no "nearest other cluster" to measure `b` against, so the quantity does not exist.** |
| The class reads 0.2849 as a bad result and deflates | **Give them the floor immediately.** `0.0776` on pure noise. **0.2849 is 3.7 times the floor with an ARI of 1.0000. That is a real finding and it is what a real dataset looks like.** |
| Everybody's names are the same three names | Fine, and say why: **the numbers only support a small number of honest readings.** Then push: *"which of your three names is weakest, and why?"* **Cluster 0, because it is low on everything and high on nothing.** |
| The 54-of-54 result kills the mood | **It is a ceiling and naming it is the skill.** *"This problem was already solved. So the experiment cannot answer the question, and we have to make it harder."* Then run the 30-row version. **Ninety seconds.** |
| Somebody fits the scaler on all 178 rows before splitting | **Excellent, and catch it out loud.** *"Which rows did your scaler learn its means from?"* **Week 6, in an unsupervised costume.** |

---

## ⏱️ The Lesson, Minute by Minute

This section is the running order of the lesson, with what to say and what to watch for in each segment.

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Three Clusters From Nothing At All | 7 | 7 | The noise result; the burden of proof |
| 🧠 Concept & Maths — A Number That Can Actually Choose k | 18 | 25 | Silhouette by hand on point C; the negative score; two votes |
| 💻 Live-Code Together — `cartography.py` | 18 | 43 | The sweep, the profile, the control. **Two deliberate mistakes.** |
| 🎲 Their Turn — The Naming Ceremony, then Do They Earn Their Keep | 20 | 63 | Three cards, three defences, then 141 → 145 |
| 🔑 Wrap & Assign | 7 | 70 | Two pictures, the argument, three checks, sheets come down |

---

### 🪝 Hook — Three Clusters From Nothing At All (7 minutes)

**Do this:** Nothing on the screen but this, which you ran last night.

```text
sizes [62 44 72]   silhouette 0.0776
```

**Say this:**

> "Three clusters. Sixty-two, forty-four and seventy-two. Nice and balanced, no errors, no warnings.
>
> That is not the wine data. **That is 178 rows of thirteen columns of pure random numbers.** I generated them with numpy about eleven seconds before I ran k-means on them. **There is no structure in there at all, and it gave me three tidy groups.**"

**Do this:** Put up the column means.

```text
cluster 0 means, first four columns: [-0.444 -0.259  0.296 -0.041]
cluster 1 means, first four columns: [ 0.522 -0.029  0.096  0.910]
```

**Ask this:** "Cluster 0 is low on column 1 and cluster 1 is high on it. Cluster 1 is high on column 4 and cluster 0 is not. **Could you write a report about those two groups?**"

*Hoped-for, uncomfortably:* yes.

**Ask this:** "Could you give them names?"

*Yes.*

> "**You could. I could. Somebody would believe it.** And there is nothing in there. Not a thing.
>
> So here is the position you are in today, and it is the whole reason this lesson exists. **k-means will hand you clusters whatever you feed it.** Getting clusters back is not evidence of anything at all. **The burden of proof is entirely on you**, and today you build the proof."

**Do this:** Write on the board and leave it up all lesson:

```text
Getting clusters is not evidence that there are clusters.
```

**Say this:**

> "So what does a proof look like? Five pieces, and you will have all five by the end of today.
>
> **One: two independent reasons for the number of clusters.** Not one. Two, and they have to be measuring different things.
>
> **Two: a number that says how tight the groups are** — and crucially, a number for what that would have been on *noise*, so you know what a floor looks like.
>
> **Three: does it survive being jiggled?** Different starting seed, and eighty per cent of the rows. If the groups vanish when you shake the data, they were never there.
>
> **Four: a name for each group that a human being can act on, with numbers behind it.** Not 'cluster 0'. A name.
>
> **Five: does it actually buy anything?** You turn the clusters into columns, feed them to a model that *does* have right answers, and see whether the score moves.
>
> Five pieces. Today's deliverable is not a score. **It is an argument.** And it is the first one in this whole course."

**Do this:** Hold up an index card and the marker.

> "And at the end of the naming, each of your three names goes on one of these. **If you cannot defend the name out loud from the numbers, I tear the card up and you write another one.**"

---

### 🧠 Concept & Maths — A Number That Can Actually Choose k (18 minutes)

**Do this:** Stand at the SIX POINTS sheet from Week 28, with the final centres still on it.

**Say this:**

> "Two weeks ago you left me with a problem and I said we would come back to it. **Inertia always falls as `k` goes up.**"

**Ask this:** "So what `k` gives the smallest inertia, and what is it?"

*`k` = 178, and inertia is exactly 0.*

> "**Exactly zero, and completely useless.** So inertia cannot choose `k`. Today's number can, and it is two averages and a subtraction."

**Do this:** Write the definition on the board and box it.

> **Silhouette, for one point:**
> `a` = my average distance to the **others in my own cluster**
> `b` = my average distance to **everyone in the nearest other cluster**
> `s = (b − a) ÷ whichever is bigger`

**Say this:**

> "In plain words: **am I closer to my own people than to the next group along, and by how much?**"

🍕 **The analogy, and use it:**

> "You are at a party that has split into conversations. **`a` is how far you would have to walk to reach the average person in your own conversation. `b` is how far to reach the average person in the next-nearest conversation.**
>
> If `b` is much bigger than `a`, you are firmly in your group. If they are about the same, **you are that person hovering between two circles, half in both.** And if `a` is bigger than `b` — you are standing in the wrong conversation."

**Do this:** Now do point C, at the sheet, out loud. **And flag the one change from Week 28.**

> "One thing changes from two weeks ago: **this time we do need real distances, not squared ones.** So there are square roots. Five of them."

```text
a(C) — to the others in my own cluster {A, B}:
   C(2,3) to A(1,2):  √(1 + 1)   = √2  = 1.4142
   C(2,3) to B(2,1):  √(0 + 4)   = √4  = 2.0000
   a = (1.4142 + 2.0000) ÷ 2 = 1.7071
```

**Ask this:** "Now `b`. How many distances this time?"

*Three — D, E and F.*

```text
   C(2,3) to D(8,8):  √(36 + 25) = √61 = 7.8102
   C(2,3) to E(9,7):  √(49 + 16) = √65 = 8.0623
   C(2,3) to F(7,9):  √(25 + 36) = √61 = 7.8102
   b = (7.8102 + 8.0623 + 7.8102) ÷ 3 = 7.8943
```

**Ask this:** "So. `a` is 1.7071 and `b` is 7.8943. Before we divide anything — is C in a good place or a bad place?"

*Good — it's four and a half times closer to its own group.*

```text
s(C) = (7.8943 − 1.7071) ÷ 7.8943  =  6.1872 ÷ 7.8943  =  0.7838
```

**Do this:** Run it, immediately.

```python
import numpy as np
from sklearn.metrics import silhouette_samples, silhouette_score

six = np.array([[1., 2.], [2., 1.], [2., 3.], [8., 8.], [9., 7.], [7., 9.]])
print(np.round(silhouette_samples(six, np.array([0, 0, 0, 1, 1, 1])), 4))
```

```text
[0.8478 0.8163 0.7838 0.8384 0.7618 0.7595]
```

**Ask this:** "Which of those six is C?"

*The third — 0.7838.*

> "**The same number. You just computed a silhouette score by hand.**"

**Do this:** Now the negative score, and this is the bit that will stick. Write a deliberately silly grouping on the board: **B goes in with D, E and F.**

```python
print(round(silhouette_score(six, np.array([0, 1, 0, 1, 1, 1])), 4))
print(np.round(silhouette_samples(six, np.array([0, 1, 0, 1, 1, 1])), 4))
```

```text
0.3751
[ 0.8068 -0.8163  0.7797  0.5284  0.487   0.4646]
```

**Ask this:** "One of those six numbers is negative. Which point is it, and what is the number telling us?"

*B, at −0.8163 — B is in the wrong cluster.*

> "**And nobody told it.** There is no right answer anywhere in that calculation. I did not hand it a label column. **It worked out that B was in the wrong place purely from the geometry**, and it is the most impressive four lines in this term."

**Do this:** Write the reading guide on the board.

```text
near +1  : comfortably inside my own cluster
near  0  : sitting on a border
negative : probably in the wrong cluster
```

**And the honest field guide, right under it:**

```text
above 0.5   strong structure
0.25 - 0.5  real, but the clusters touch
below 0.25  mostly a convenient fiction
```

**Say this:**

> "And here is the property that makes this useful. **Unlike inertia, the silhouette does not automatically get better as `k` goes up.** It has a real peak. So you can pick the `k` that maximises it, which means **you now have two independent votes.**"

**Do this:** Put the sweep table up and cover the silhouette column with your hand.

```text
   k    inertia      drop   silhouette
   1     2314.0         -
   2     1659.0     655.0
   3     1277.9     381.1
   4     1180.7      97.2
   5     1110.4      70.4
```

**Ask this:** "Vote one, the elbow. Where is it, and give me a number rather than pointing at the table."

```text
381.1 ÷ 97.2 = 3.9
```

*`k = 3` — the third cluster bought nearly four times what the fourth did.*

**Do this:** Uncover the silhouette column.

**Ask this:** "Vote two. Where is the peak?"

*`k = 3`, at 0.2849.*

> "**Two methods, measuring different things, both saying three.** That agreement is the evidence you cite in a report. Not *'the curve bends at three'* — anybody can see a bend they want to see. *'The drop ratio is 3.9 and the silhouette peaks at 0.2849, both at k = 3.'*"

**Ask this:** "And what if they had disagreed?"

*Take answers. Then give the honest structure:*

> "Then you have learned something. **The elbow tends to over-count, because splitting a big loose cluster always buys a lot of inertia. The silhouette tends to under-count when clusters touch**, because border points score near zero and drag the average down, and merging two touching clusters gets rid of the border.
>
> **So silhouette pulling lower than the elbow is the fingerprint of overlapping clusters**, and that sentence goes in your write-up. And there is a third thing that beats both: **if you can only act on three groups, the answer is three**, whatever the numbers say. Say so out loud rather than pretending the maths decided."

**Ask this:** "Last one, and look at 0.2849 against the field guide. **What is the honest description of these clusters?**"

*Real, but they touch.*

> "**Real but overlapping. Say exactly that.** Not 'well-separated'. And 0.2849 only becomes a finding when you put it next to the number I showed you at the start: **0.0776, on pure noise.** `0.2849` against a floor of `0.0776` is 3.7 times the floor. **That is a claim you can defend.**"

---

### 💻 Live-Code Together — `cartography.py` (18 minutes)

**Do this:** Hand them the imports, the data load, the scaler and the `run()` helper already typed. **They type the new lines.**

**Step 1 — the sweep with both columns (5 minutes).**

```python
print("   k    inertia      drop   silhouette")
prev = KMeans(n_clusters=1, n_init=10, random_state=0).fit(X).inertia_
print("   1   %8.1f         -            -" % prev)
for k in range(2, 11):
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    s = silhouette_score(X, km.labels_)
    print("  %2d   %8.1f   %7.1f       %.4f" % (k, km.inertia_, prev - km.inertia_, s))
    prev = km.inertia_
```

```text
   k    inertia      drop   silhouette
   1     2314.0         -            -
   2     1659.0     655.0       0.2683
   3     1277.9     381.1       0.2849
   4     1180.7      97.2       0.2457
   5     1110.4      70.4       0.2026
   6     1044.5      65.9       0.1960
   7      996.0      48.5       0.1386
   8      944.6      51.4       0.1581
   9      913.2      31.4       0.1417
  10      864.6      48.6       0.1338
```

**Ask this:** "Look at `k = 8`. The silhouette goes 0.1386 then back up to 0.1581. **Is eight better than seven?**"

*Hoped-for, after a beat:* it's higher, but it's nowhere near the peak.

> "**It is higher than its neighbour and less than half the peak. A bump that does not beat the maximum is not a finding, it is noise.** And it is exactly the kind of thing somebody picks out of a table when they want a particular answer."

**Step 2 — a loud mistake, on purpose (2 minutes).**

```python
print(silhouette_score(X, np.zeros(178)))
```

> **🧑‍🏫 Deliberate mistake one.** **Run it without warning.**

```text
ValueError: Number of labels is 1. Valid values are 2 to n_samples - 1 (inclusive)
```

**Ask this:** "Why can it not give me a silhouette for one cluster?"

*Let them work it out. It is a genuinely good question with a clean answer.*

> "**Because there is no `b`.** `b` is 'how far to the nearest *other* cluster', and with one cluster there is no other cluster. **The quantity does not exist** — this is not the library being fussy, it is the definition. And that is also why the silhouette cannot compare `k=1` against `k=3`: `k=1` has no score at all."

**Step 3 — the profile table, in units a person can read (4 minutes).**

```python
km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
labels = km.labels_
prof = X_raw.copy()
prof["cluster"] = labels
means = prof.groupby("cluster").mean().T
means["overall"] = X_raw.mean()
print(means.round(2).to_string())
```

```text
cluster                            0       1        2  overall
alcohol                        12.25   13.13    13.68    13.00
malic_acid                      1.90    3.31     2.00     2.34
ash                             2.23    2.42     2.47     2.37
alcalinity_of_ash              20.06   21.24    17.46    19.49
magnesium                      92.74   98.67   107.97    99.74
total_phenols                   2.25    1.68     2.85     2.30
flavanoids                      2.05    0.82     3.00     2.03
nonflavanoid_phenols            0.36    0.45     0.29     0.36
proanthocyanins                 1.62    1.15     1.92     1.59
color_intensity                 2.97    7.23     5.45     5.06
hue                             1.06    0.69     1.07     0.96
od280/od315_of_diluted_wines    2.80    1.70     3.16     2.61
proline                       510.17  619.06  1100.23   746.89
```

**Ask this:** "I clustered on the **scaled** table, but this table is in the **original** units. Why did I do that?"

*Hoped-for:* because nobody can read a z-score.

> "**Because 'alcohol = 0.83' means nothing to a human being and 'alcohol = 13.68' means something to a winemaker.** You cluster in the scaled world and you *report* in the real one. Two different jobs."

**Ask this:** "And why is the `overall` column there?"

*To compare against.*

> "**'Flavanoids 0.82' is not a fact about anything. 'Flavanoids 0.82 against an overall 2.03' is.** Same rule as Week 27's control and Week 9's baseline: **a number with nothing beside it is not evidence.**"

**Ask this:** "Cluster 1's alcohol is 13.13 and the overall is 13.00. **Does that help me name cluster 1?**"

*Hoped-for:* no, it's basically the same.

> "**0.13 apart. It defends nothing, and I want you to leave it out of your card.** Compare it with cluster 1's flavanoids — 0.82 against 2.03. **That is a difference you can build a name on.**"

**Step 4 — the silent mistake (3 minutes).**

```python
km_raw = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X_raw)
print("clustered raw,    scored raw    : %.4f" % silhouette_score(X_raw, km_raw.labels_))
print("clustered scaled, scored scaled : %.4f" % silhouette_score(X, labels))
```

> **🧑‍🏫 Deliberate mistake two.** **Be visibly pleased with the first number.** *"0.5711! That is in the 'strong structure' band. All this scaling business has been making our clusters worse — look, without it they are twice as good."* **Let it sit for a few seconds.**

```text
clustered raw,    scored raw    : 0.5711
clustered scaled, scored scaled : 0.2849
```

**Ask this:** "0.5711 against 0.2849. **Which clustering is better?**"

*Most of the room will say the first one. Let them.*

**Do this:** Open the drawer.

```python
print("ARI against the real grape variety, raw    : %.4f"
      % adjusted_rand_score(wine.target, km_raw.labels_))
print("ARI against the real grape variety, scaled : %.4f"
      % adjusted_rand_score(wine.target, labels))
```

```text
ARI against the real grape variety, raw    : 0.3711
ARI against the real grape variety, scaled : 0.8975
```

**Ask this:** "Now which one is better?"

*The scaled one, by a mile.*

> "**The clustering with double the silhouette is the one that got the grape varieties wrong.** 0.3711 against 0.8975.
>
> And it makes complete sense once you say what the unscaled clusters *are*. **Three non-overlapping bands of proline — 278 to 590, 600 to 937, 970 to 1680.** Nothing on earth is tidier than three bands of one column, so of course they score beautifully on separation. **They are just separated along the wrong thing.**
>
> So here is the rule, and it is the most important sentence of the week: **the silhouette measures the shape of your grouping in the space you measured it in. It does not measure whether your grouping is right.** 0.5711 is a completely true number about a question nobody asked.
>
> And the practical half: **score in the same space you clustered in.** If you clustered on scaled data, every distance you report — inertia, silhouette, centre distances — must come from the scaled table too."

**Step 5 — the negative control and the stability check (4 minutes).**

```python
ref = labels
seeds = [adjusted_rand_score(ref, KMeans(n_clusters=3, n_init=10,
                                         random_state=s).fit(X).labels_)
         for s in (1, 2, 3, 4, 5)]
print("five seeds, ARI:", np.round(seeds, 4))

noise = np.random.default_rng(0).normal(size=(178, 13))
kmn = KMeans(n_clusters=3, n_init=10, random_state=0).fit(noise)
print("noise silhouette: %.4f" % silhouette_score(noise, kmn.labels_))
nseeds = [adjusted_rand_score(kmn.labels_, KMeans(n_clusters=3, n_init=10,
                                                 random_state=s).fit(noise).labels_)
          for s in (1, 2, 3, 4, 5)]
print("noise, five seeds, ARI:", np.round(nseeds, 4), " mean %.4f" % np.mean(nseeds))
```

```text
five seeds, ARI: [1. 1. 1. 1. 1.]
noise silhouette: 0.0776
noise, five seeds, ARI: [0.6407 0.4069 0.61   0.6072 0.6308]  mean 0.5791
```

**Do this:** Write the four numbers on the board as a two-by-two.

```text
                    real wine     pure noise
silhouette            0.2849        0.0776
seed-to-seed ARI      1.0000        0.5791
```

**Ask this:** "Now. **Is 0.2849 a good score?**"

*Hoped-for, and it is the whole lesson:* compared to what?

> "**Compared to what. Yes.** Against the field guide, 0.2849 is 'real but overlapping'. **Against the noise floor of 0.0776, it is 3.7 times higher.** And our grouping is perfectly stable across five seeds where the noise grouping agrees with itself only moderately (0.58, where 0 would be pure chance).
>
> **That pair of comparisons is your argument.** It is not 'we got a good score'. It is 'we got 3.7 times the floor, with perfect stability against 0.58'. **Nobody can argue with that, and almost nobody does it.**"

---

### 🎲 Their Turn — The Naming Ceremony, then Do They Earn Their Keep (20 minutes)

Full instructions in **🎲 The Activity, In Full** below. In outline: **twelve minutes** on the Naming Ceremony — each cluster gets a name written on an index card, and the name must be **defended out loud from the feature-means table in the original units**, with a card that nobody can defend being physically torn up and rewritten. Then **eight minutes** turning the clusters and components into five extra columns and testing whether they buy anything, first at 124 training rows (they buy nothing, and naming the ceiling is the skill) and then at 30 (141 of 148 becomes 145 of 148).

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Put last week's `wine_2d.png` and today's `wine_map.png` on the screen side by side, in that order.

**Ask this:** "Last week's plot. How many groups can you see?"

*One blob. Maybe none.*

**Ask this:** "Same points, same two axes, same percentages. How many now?"

*Three, clearly.*

> "**The structure was there the whole time and the picture could not show it.** That is the best argument I can give you for why you need a number and not a plot. Your eye found nothing in that first picture. **The silhouette found 0.2849 and the elbow found a drop ratio of 3.9, and both of them were right.**
>
> And the percentage is still in both axis labels, because `36.2 + 19.2 = 55.4`, so **44.6% of the spread in these wines is not on the page** and two bottles sitting on top of each other might not be alike at all."

**Do this:** Now put the whole argument on the board, as five lines. **This is the deliverable and it is worth writing out in full.**

```text
1. how many clusters   drop ratio 381.1 ÷ 97.2 = 3.9   AND   silhouette peak 0.2849
                       both say k = 3

2. how tight           silhouette 0.2849  ("real, but they touch")
                       against a NOISE FLOOR of 0.0776  -  3.7x

3. does it survive     5 seeds:      ARI 1.0000
                       5 subsamples: ARI 0.9657
                       noise, 5 seeds: 0.5791

4. what are they       Bold Reserve (62)  Dark & Tannic (51)  Light & Pale (65)
                       and cluster 0 is the weak one: silhouette 0.1774, 7 points below 0

5. does it buy         30 training rows: 141 of 148  ->  145 of 148
                       held out: 148 wines, never touched by any fitting
```

**Ask this:** "Which line of that is a score?"

*None of them.*

> "**None. There is no score anywhere in this, because there was no answer key.** Every single line is a comparison against something. **That is what an argument looks like**, and it is the thing you will be handing in for your capstone in five weeks' time.
>
> And line 4 — I want you to notice that I have written the weak cluster into the argument, not left it out. **0.1774 and seven bottles below zero.** A write-up that only contains its good news is a sales brochure, and you have spent thirty weeks learning not to write one."

**Do this:** Three quick checks — exact wording in **✅ Assessing Understanding**.

**Do this:** Take down the SIX POINTS sheet, deliberately, in front of them.

**Say this, to close:**

> "This comes down today. It went up three weeks ago with six points on it and nothing else.
>
> On that sheet you have done: **two full rounds of k-means with twenty-four squared distances. An inertia of 6.6667, added up by hand and matched to the library. And today a silhouette of 0.7838, from five square roots and a subtraction — and the library agreed to four decimal places.**
>
> Six points. No labels. **And you have measured everything about them that can be measured.**
>
> Next week is a completely different subject, and it is the last new one before the capstone: **words.** Not numbers. Reviews, sentences, spam — and the first problem is that a model cannot do arithmetic on the word 'brilliant'."

**Do this:** Hand out the homework and read the last part out loud, slowly.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `ValueError: Number of labels is 1. Valid values are 2 to n_samples - 1 (inclusive)` | "You asked for a silhouette with only one cluster." | `silhouette_score(X, np.zeros(n))`, or a sweep that starts at `k = 1`. | **Start the silhouette sweep at `k = 2`.** And understand why: `b` is "distance to the nearest *other* cluster", and with one cluster there is no other. **The quantity does not exist.** |
| `ValueError: Found input variables with inconsistent numbers of samples: [178, 142]` | "You gave me 178 labels and 142 rows." | Scoring a subsample's labels against the full table, or vice versa, in the stability check. | Index both the same way: `silhouette_score(X[idx], labels_sub)`. **Print both lengths before you call it — Week 27's habit.** |
| `ValueError: Input X contains NaN.` | "There is a hole in the table." | Missing values never filled in. | `SimpleImputer` from Week 6, inside the pipeline. **There is no distance to a hole.** |
| `ValueError: X has 13 features, but KMeans is expecting 18 features as input.` | "You fitted on 13 columns and are asking about 18." | `km.transform(A)` where `A` is the augmented 18-column table rather than the 13-column scaled one. | **The k-means only knows the 13 columns it was fitted on.** Build the 18-column table *from* its output, never feed the 18 back in. |
| `AttributeError: 'KMeans' object has no attribute 'transform'` — on a fresh object | "You never ran it." | `.fit` not called. | Week 28's rule. **`transform` needs centres, and fitting is what finds them.** |
| `TypeError: unhashable type: 'numpy.ndarray'` from `groupby` | "You handed groupby an array where it wanted a column name." | `prof.groupby(labels)` instead of adding `prof["cluster"] = labels` first. | Add the column, then `groupby("cluster")`. **It is also better practice, because the table now records which cluster each row was in.** |
| **No error. The silhouette is 0.5711 and you are delighted.** | Nothing crashed. You clustered without scaling, and one column's bands score beautifully. | `KMeans(...).fit(X_raw)` with no `StandardScaler`, scored on `X_raw`. | **A higher silhouette is not a better clustering.** That grouping scores ARI 0.3711 against the real varieties where the scaled one scores 0.8975. **And separately: score in the same space you clustered in** — scoring scaled labels on the raw table gives a third, equally meaningless number, 0.1943. |
| **No error. Your profile table is full of numbers like 0.83 and −1.21.** | Nothing crashed. You profiled the scaled table. | `X` instead of `X_raw` in the `groupby`. | **Cluster on scaled, report in original units.** Nobody can act on "alcohol = 0.83". |
| **No error. Your supervised accuracy is 1.0000 and adding features changes nothing.** | Nothing crashed. There was no room to improve. | 124 training rows on a very easy 3-class problem. | **Name the ceiling, then make the problem harder.** 30 training rows: `141 of 148` → `145 of 148`. **A feature can only help where there is headroom.** |
| **No error. Adding the cluster features made things slightly worse.** | Nothing crashed. You are reading one split. | The gain is about +1.15 points on average with a split-to-split wobble of 0.0125, so one split can go either way. | **Repeat the split ten times.** 8 wins, 2 ties, 0 losses. **Week 11's question: is this difference bigger than the noise?** |
| **No error. Your cluster 0 is a different cluster from mine.** | Nothing crashed. Cluster numbers are arbitrary. | Expecting IDs to be stable. | `adjusted_rand_score` — it compares groupings and ignores the numbers. **ARI 1.0000 means identical grouping even when every ID has changed.** |
| **No error, and the accuracy is suspiciously high.** | Nothing crashed. Something was fitted on all the rows. | `StandardScaler`, `KMeans` or `PCA` fitted before the split. | **All three learn from data, so all three leak.** Fit on the training rows only, and say out loud which rows each one saw. **Week 6, in an unsupervised costume.** |

### How to teach debugging without giving the answer

All the old moves stand. This week adds three, and they are the last new ones before the capstone.

32. **"Which table did you hand it?"** Ask it whenever a distance-based number looks too good. Scaled or raw — and the answer must match whatever you clustered on.

33. **"Which rows did that learn from?"** Ask it of the scaler, the k-means and the PCA separately. **Three objects, three answers, and all three must be "the training rows".**

34. **"What would that number have been on noise?"** The single most valuable question in unsupervised work, and it takes four lines to answer.

And the sentence for this week, and for the whole of Term 4:

> **"Every number in an unsupervised write-up needs something beside it. 0.2849 alone is a decoration; 0.2849 against a noise floor of 0.0776 is a finding. The comparison is the result, not the number."**

---

## 🎲 The Activity, In Full

This section gives the full instructions for the two-part lab, so you can run it without the rest of the guide.

### Part A — The Naming Ceremony (12 minutes)

**What it is.** Each cluster gets a name written in marker on an index card. Then, one at a time, the student holds up the card and **defends the name out loud, pointing at specific numbers in the feature-means table against the overall column.** A name nobody can defend gets **torn up** and rewritten.

**Why it is worth twelve minutes.** This is objective 3, and it is the only objective in Term 4 that cannot be measured by a machine. **A cluster ID is worth nothing to anybody. A name with three numbers behind it is a decision somebody can act on.** And the tearing-up is not theatre: it installs the difference between a name that came from the data and a name that came from the imagination, which is the exact difference this whole term is about.

### Setup

- **The feature-means table printed, one per student**, in the original units with the overall column. Big enough to point at.
- **Six blank index cards and a thick marker** on the front desk.
- **The per-cluster silhouettes on the board**, because they are part of the defence:

```text
cluster 0:  n = 65    own silhouette 0.1774    7 points below zero
cluster 1:  n = 51    own silhouette 0.3506    0 points below zero
cluster 2:  n = 62    own silhouette 0.3434    0 points below zero
```

- **Workbook page 30.4** — three name boxes, each with three blank "the number that proves it" lines under it.

### Step 1 — find the standouts (4 minutes)

Before any naming. For each cluster, they hunt the table for the rows where that cluster is **furthest from the overall column** — in either direction.

> **Say this:** "Three rows per cluster. Not five, not one. **Three, and they have to be the three furthest from the overall number.**"

The real answers:

| cluster | its three biggest standouts |
|---|---|
| **0** | colour intensity **2.97 vs 5.06** · proline **510 vs 747** · alcohol **12.25 vs 13.00** |
| **1** | flavanoids **0.82 vs 2.03** · colour intensity **7.23 vs 5.06** · hue **0.69 vs 0.96** |
| **2** | proline **1100 vs 747** · flavanoids **3.00 vs 2.03** · total phenols **2.85 vs 2.30** |

**Do this:** As they work, walk round and ask one question at a time: *"how far from the overall is that?"* **Anybody writing down `alcohol 13.13 vs 13.00` for cluster 1 gets asked it immediately.** 0.13 is not a standout.

### Step 2 — write the cards (2 minutes)

**Three or four words, in marker, on a card.** One card per cluster.

> **Say this:** "The name has to be something a person who has never heard of k-means could read on a slide. **'Cluster 1' is not a name. 'High-Colour Low-Flavanoid Group' is a bit of a mouthful but it is a name. 'Dark & Tannic' is a name.**"

### Step 3 — the ceremony (5 minutes)

One at a time. Hold up the card. **Say the name, then the three numbers.** Everybody else's job is to decide whether the numbers support the name.

Good defences sound like this:

> **"Dark & Tannic.** Flavanoids 0.82 against an overall 2.03 — less than half. Colour intensity 7.23 against 5.06 — much darker. Hue 0.69 against 0.96 — the lowest of the three. **So: deeply coloured, sharp, and short of the soft phenols. 51 bottles, and its own silhouette is 0.3506, which is the best of the three.**"

> **"Bold Reserve.** Proline 1100 against 747, flavanoids 3.00 against 2.03, total phenols 2.85 against 2.30 — **highest of the three on every one of those.** Rich, full-bodied, high-extract. 62 bottles, silhouette 0.3434."

**And the one that should be hard, and must not be rescued:**

> **"Light & Pale.** Colour intensity 2.97 against 5.06, proline 510 against 747, alcohol 12.25 against 13.00 — **it is the lowest of the three on almost everything and the highest on nothing.** 65 bottles, and its own silhouette is only 0.1774 — half of the other two — with seven bottles scoring below zero. **So this is my weakest name, and the reason is that 'low on things' is a much weaker basis for a group than 'high on a specific thing'.**"

**Tear up a card if:**

- the defence uses **no numbers** ("they seem lighter");
- it uses a number **not compared to the overall** ("proline 510");
- it uses a number that is **not actually a standout** (`alcohol 13.13 vs 13.00`);
- the name claims something **not in the table at all** ("Expensive", "Old", "Award-Winning").

**Do this:** Tear it in front of them, hand them a fresh card, and say what was missing in one sentence. **Do not soften it and do not skip it.** The first tear is the whole activity.

### Step 4 — name the weakest, out loud (1 minute)

> **Ask this:** "Which of your three names is the weakest, and why?"

*Cluster 0 — lowest on nearly everything, highest on nothing, silhouette 0.1774, seven points below zero.*

> **Say this:** "**And that goes in the write-up, not in the bin.** A cluster defined mainly by absence is often a sign that `k` is too small, or that the real structure is two strong groups plus a pile of leftovers. **Saying so is worth more than a third confident name.**"

### Part B — Do They Earn Their Keep? (8 minutes)

**What it is.** Turn the clusters and components into five extra columns, feed them to a model that *does* have right answers, and find out whether the score moves. **Twice: once where there is no headroom, and once where there is.**

### Step 1 — the ceiling (3 minutes)

```python
run(124)          # 124 training rows, the other 54 held out
```

```text
  13 raw columns        1.0000  (54 of 54 held-out wines)
  13 + 3 dists + 2 PCs  1.0000  (54 of 54 held-out wines)
  the 5 new ones ALONE  1.0000  (54 of 54 held-out wines)
```

> **Ask this:** "Did the five new columns help?"

*No — nothing changed.*

> **Ask this:** "**Is that the same as saying they are useless?**"

*Let them think. This is the point of the whole activity.*

> **Say this:** "**No, and this is the trap.** Look at the first row: 54 of 54. **The problem was already completely solved before we added anything.** There was no room to improve, so nothing could improve it. **That is a ceiling, and the right conclusion is not 'the features don't help' — it is 'this experiment cannot answer the question.'**"

> **Ask this:** "So what do we do?"

*Make the problem harder.*

### Step 2 — make it hard (3 minutes)

```python
run(30)
```

```text
  13 raw columns        0.9527  (141 of 148 held-out wines)
  13 + 3 dists + 2 PCs  0.9797  (145 of 148 held-out wines)
  the 5 new ones ALONE  0.9865  (146 of 148 held-out wines)
```

> **Ask this:** "Now? How many more wines?"

*Four — 141 to 145.*

> **Ask this:** "And now look at the third row. **What just happened?**"

*Hoped-for, with some surprise:* the five new columns on their own beat all thirteen original ones.

> **Say this:** "**146 against 141. Five numbers that were built without ever looking at a single label beat thirteen carefully measured chemical properties.**
>
> And the reason is the row count. With 30 training rows, a thirteen-column model has forty-two coefficients to estimate and nowhere near enough rows to do it. **k-means got to use the geometry of all 30 rows without needing any labels at all, and then handed over three numbers that already knew where the groups were.** *(Honest footnote: k-means and PCA were fitted on the same 30 labelled rows, so the gain is most likely dimensionality reduction, 5 inputs against 13, not yet use of unlabelled data.)*
>
> That is not a trick. **That points at something unsupervised learning can do: it works on unlabelled data, and labels are often the expensive part** (this experiment only hints at it, since no extra unlabelled rows were used)."

### Step 3 — but is it real? (2 minutes)

> **Ask this:** "Four wines out of 148. **Is that a real improvement or a lucky split?**"

*Take answers. Somebody should suggest doing it again.*

```text
13 raw        mean 0.9642  std 0.0125
18 cols       mean 0.9757  std 0.0075
mean gain: +0.0115
better / equal / worse over ten splits: 8 2 0
```

> **Say this:** "**Over ten different splits the average gain is 1.15 points, which is smaller than the single split suggested, and it is about the same size as the baseline's own wobble of 0.0125.** So on size alone you could not call it.
>
> **But it won eight times, tied twice, and never once lost.** *That* is the evidence. Not how big the gain was — **that it never went the other way.** Week 11's question, and it is the last time you practise it before the capstone."

### What "finished" looks like

- Three index cards, each with a name and three numbers that survived being challenged out loud.
- **At least one card has been torn up.** If none were, the defences were not being challenged hard enough.
- Page 30.4 with three names and nine numbers, every one compared against the overall column.
- The two accuracy rows written down **with the pile named**: `141 of 148` and `145 of 148`, 30 training rows.
- A student can say, unprompted: **"there was no room to improve."**
- A student has asked whether four wines is real. **That is the best outcome available.**

### Variation — easier

**Cut to two clusters.** Run `k=2` and name two groups instead of three. The naming is the objective and two names is enough for it.

**Give them the standouts.** Pre-highlight the three biggest gaps per cluster on the printed table, so the only work is turning three numbers into a name and saying it out loud. **Objective 3 is about defending a name from evidence, not about hunting the evidence.**

**Skip Part B's ceiling step** and go straight to `run(30)`. Two numbers, one comparison: `141 of 148` against `145 of 148`, held out 148 wines.

**One thing you must not cut:** the tearing-up. **A ceremony where nothing can fail is not a ceremony.**

### Variation — harder

1. **Find where the two votes disagree.** Cluster `load_breast_cancer()` (569 rows, 30 columns) and sweep `k = 2` to `10`. **Then the real skill: the two diagnostics do not agree as cleanly as on the wine, and the student has to pick one and defend the choice.**
2. **Name the noise clusters.** Run the whole Naming Ceremony on the 178 rows of pure noise — profile table, standouts, three names, defences. **They will manage it, and doing it deliberately is the most powerful ninety seconds in Term 4.** Then: *"what is the difference between that and what you did with the wine?"* **The noise floor and the stability numbers, and nothing else.**
3. **Find the seven bottles with negative silhouettes** and look at them. `silhouette_samples(X, labels) < 0`, then print their rows. **Are they odd bottles, or just border cases?** Then the real question: *"in a deployed system, what would you do with a row the clustering is unsure about?"* **Route it to a human, which is a design decision no algorithm can make for you.**
4. **Push the training set down further.** Try 20 training rows, then 15. **Find the point where the five unsupervised columns stop helping**, and report it. There is a real answer and hunting for it is genuine experimental work.
5. **Leak on purpose and measure it.** Fit the `StandardScaler`, `KMeans` and `PCA` on all 178 rows *before* splitting, and compare with the honest version. **Then the uncomfortable finding: on this dataset the leak barely moves the number at all**, which means you cannot catch it by noticing a suspiciously good score. **You have to catch it by reading the code.** This is the single most important thing on this list.
6. **Silhouette by hand for a second point.** Do `s(B)` on Week 28's six points, unaided: `a(B) = (1.4142 + 2.0000) ÷ 2 = 1.7071`, `b(B) = (9.2195 + 9.2195 + 9.4340) ÷ 3 = 9.2910`, `s(B) = (9.2910 − 1.7071) ÷ 9.2910 = 0.8163` — **and `silhouette_samples` prints exactly 0.8163.** Then the harder half: **compute it again using squared distances instead of real ones and see what breaks.** You get `a = 3.0`, `b = 86.3333`, `s = 0.9653` — plausible-looking, on the right scale, and wrong. **Finding out why a wrong method still gives a believable answer is worth more than getting the right one.**

---

## ❓ Questions Students Ask This Week

This section gives the questions this week tends to raise, with answers you can say aloud.

**"Why is 0.2849 a good score? It sounds terrible."**

**It is not a good score, and calling it one would be dishonest. It is a real result.**

Against the field guide, 0.2849 sits in the "real, but the clusters touch" band, and that is the correct description of these clusters: the wine varieties genuinely do overlap chemically, and the map shows three groups whose edges meet. **Saying "real but overlapping" is the finding. Saying "well-separated" would be a lie and your reader would eventually check.**

What makes 0.2849 evidence rather than decoration is the **floor**: pure noise scored 0.0776 with the identical pipeline. **0.2849 is 3.7 times the floor.** And the stability: our grouping is identical across five seeds where the noise grouping agrees with itself only 0.58 of the time.

**And the general point, which is the most transferable thing in this lesson: real tabular data usually lands between 0.25 and 0.4.** Tutorials show you 0.77 because they use `make_blobs`. **A student who reports 0.2849 honestly and puts a floor beside it has done better work than one who hunts for a `k` that gives 0.6.**

**"The cluster numbers came out different from my friend's. How can ARI say 1.0?"**

**Because ARI does not look at the numbers at all.** It looks at which *rows are together*.

Ask it a different way: for every possible pair of wines, do the two runs agree about whether those two wines are in the same group? Bottle 7 and bottle 40 either share a cluster or they do not, and that answer does not change when you rename the clusters. **ARI counts those agreements and then subtracts off how many you would have got by luck, which is what "adjusted" means.**

So `ARI = 1.0` means the two runs put exactly the same bottles together, even if your cluster 0 is their cluster 2. **That is precisely why it is the right tool for Week 28's complaint that cluster IDs move around between runs.** The IDs are names; ARI compares the grouping.

**"Why does the silhouette need real distances when inertia used squared ones?"**

Because the silhouette is a **ratio**, and inertia is a **total**.

Inertia only ever compares distances to decide which is smaller, and squaring never changes which of two numbers is smaller — so it can skip the square roots and save you the work.

The silhouette divides one distance by another: `(b − a) ÷ max(a, b)`. **A ratio of squared distances is not the same as the ratio of the distances** — for `a = 2` and `b = 4` the ratio is 2, but the squared ratio is 4. So if you skipped the roots you would still get a number between −1 and +1, but it would be a different number (0.9519 instead of 0.7838 for point C) that no longer measures distances. **Squaring is a shortcut you may take when you are only comparing; it is not a shortcut when you are dividing.**

**"If we cannot check clusters, how does anybody know this is worth doing at work?"**

**Because you check the thing downstream instead of the clusters.**

That is what Part B was. The clusters are not the product — they are an input to something that *does* have an answer. If adding cluster columns makes a fraud model catch more fraud, the clusters earned their keep, and you never had to decide whether they were "correct". **A/B tests work the same way: nobody asks whether a customer segment is "true", they ask whether a campaign built on it sold more.**

And when there genuinely is nothing downstream — you were asked to "understand our customers" — then the deliverable is honestly the argument: the named groups, the evidence, the noise floor, the stability, and the part you are least sure about. **That is a real professional product. It is just not a number.**

**"Five columns that never saw a label beat thirteen that did. Does that mean labels do not matter?"**

**The opposite, and the reason is worth getting right.**

Labels matter enormously. What that result shows is narrower: k-means and PCA were fitted on the same 30 labelled rows, so the gain is most likely dimensionality reduction (5 inputs against 13), not use of unlabelled data. The general point that **labels are often expensive and unlabelled rows cheap** is true, but it needs a fairer test than this one to demonstrate (fit k-means and PCA on extra unlabelled rows).

Look again at what happened. With **124** labelled rows, the thirteen original columns got 54 of 54 — perfect — and the unsupervised columns added nothing. With **30** labelled rows, the thirteen columns dropped to 141 of 148 and the unsupervised columns overtook them. **The thing that changed was not the value of the labels. It was how many of them there were.**

**So the real lesson is: unsupervised methods are most valuable exactly where labelling is hardest.** That is a genuinely important engineering fact — labelling 30 wines is an afternoon, labelling 30,000 medical scans is two years of specialist time — and it is why this pairing of techniques exists at all.

**"Could we use the clusters as labels and then train a classifier on them?"**

**You can, people do, and you should be careful about what you have actually built.**

If you train a classifier to predict cluster ID, it will get very high accuracy — because the cluster IDs came from a deterministic rule applied to the same columns, so you are teaching a model to imitate `argmin`. **A 99% accurate cluster-predictor tells you nothing about the world; it tells you the clustering was reproducible.**

Where it genuinely helps is when you have a few labelled rows and many unlabelled ones: cluster everything, and then use the labelled rows to decide what each cluster *means*. That has a name — semi-supervised learning — and it is a real and useful family of methods. **It is outside this course, but a student who proposes it has had a very good idea and should be told so.**

**"Should you cluster people?"** *(Nobody fully agrees, and here is why.)*

**No settled answer, and this week gives the disagreement much sharper teeth than Week 28 did, because now you have done the Naming Ceremony.**

**The case for.** Any organisation serving millions of people must group them somehow; you cannot design a product per person. Clustering does it from evidence rather than from a marketing director's hunch, and that is a real improvement.

**The case against, and it is stronger after today.** You just watched a name get written on a card. Names are sticky. Call 65 bottles "Light & Pale" and nothing happens. Call 65,000 people "Low-Value Customers" and within a year there are products for them, prices for them, and a support queue they get put in. **The group did not exist before it was named, and then it does, because it was named.** That is not a hypothetical; it is how customer segments work everywhere.

**The objection that today makes concrete.** Look at cluster 0: silhouette 0.1774, **seven of its sixty-five members scoring below zero, which means they are closer to a different cluster than their own.** On wine, those seven are a footnote. **On people, those seven are individuals filed into a category the algorithm itself is unsure about** — and the system downstream will not be told about the uncertainty, because a database column holds `0`, not `0 with silhouette −0.02`.

**And the sharpest version.** k-means has no "none of the above". Every person must be assigned. The person who fits nowhere goes wherever they are least unlike, **and then drags that cluster's centre towards themselves**, changing other people's assignments.

**The position most practitioners hold is a compromise rather than a principle:** cluster people for **description**, be very cautious about clustering them for **decisions about individuals**. The trouble is that the description becomes the decision, because the cluster ID is sitting in a database and the next engineer along does not know it was only ever meant to be descriptive.

What to say out loud to a 14-year-old: **"you have a number today that nobody in industry usually computes — the silhouette of the individual row. It tells you which rows the algorithm is unsure about. If you are clustering people, the honest thing is to carry that uncertainty forward instead of throwing it away, and if the system you are handing it to has no place to put it, that is a problem with the system and you should say so before you build it."**

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| **0.2849 gets described as "well-separated"** | It is the biggest number in the column and it feels like a win | **Never say it.** The class copies your words exactly. **"Real, but the clusters touch"** is the phrase, and `0.0776` is the number that turns it into evidence. |
| **The negative control gets skipped** | It comes at the end of step 5 and looks like an optional extra | **It is the single most valuable thing in this lesson and almost nobody teaches it.** Four lines and two numbers. **If you have ninety seconds left, spend them here and cut something else.** |
| No index card gets torn up | It feels harsh, and the first defence is usually not bad | **Then the defences were not being challenged.** Have one ready to fail: **`alcohol 13.13 vs 13.00`** is in nearly every first attempt at cluster 1. **Tear that one, explain in one sentence, hand over a fresh card.** |
| The 54-of-54 result deflates the room | It looks like the experiment failed | **Name the ceiling out loud and immediately.** *"The problem was already solved. That is a ceiling, not a result, and recognising it is the skill."* Then `run(30)`. **The recovery takes ninety seconds and the lesson is stronger for having hit the ceiling first.** |
| The profile table goes up in z-scores | `X` is right there and `X_raw` is one more variable | **Ask the class what `alcohol = 0.83` means before you fix it.** They cannot answer, which is the point. **Cluster in the scaled world, report in the real one.** |
| A student prefers the unscaled clustering because its silhouette is bigger | 0.5711 really is bigger than 0.2849, and both are "the silhouette" | **Run it as deliberate mistake two so you control when it happens, and then open the drawer: ARI 0.3711 against 0.8975.** The rule: **a higher silhouette is not a better clustering, and you must score in the same space you clustered in.** |
| The elbow gets read off a picture rather than a ratio | The plot has a visible bend and pointing is easy | **Always say the division: `381.1 ÷ 97.2 = 3.9`.** Week 28's rule. **A ratio is a finding; a bend is an opinion.** |
| The `k = 8` silhouette bump gets mistaken for structure | 0.1581 really is higher than 0.1386 | **Ask about it yourself before somebody else does.** *"Is 8 better than 7?"* **A bump that does not beat the maximum is noise.** |
| Something gets fitted on all 178 rows before the split | It feels like preprocessing rather than modelling | **Ask the three questions out loud, one per object:** *"which rows did the scaler learn from? the k-means? the PCA?"* **Three objects, three answers, all "the training rows".** |
| The 4-wine gain gets reported as a triumph | +2.70 points sounds substantial | **Show the ten-split numbers.** Mean gain +1.15, baseline wobble 0.0125, **but 8 wins, 2 ties, 0 losses.** The honest claim is about the consistency, not the size. |
| The lesson runs out of time in the wrap | There is a ceremony and two experiments in seventy minutes | **The least cuttable things are the noise floor and the five-line argument on the board.** If you are behind at minute 60, cut Part B's ceiling step and go straight to `run(30)` — **but never cut the five-line argument, which is the whole deliverable.** |
| The weak cluster gets quietly dropped from the write-up | Two confident names read better than three uneven ones | **Write `0.1774` and "7 points below 0" into the argument on the board yourself, in front of them.** The teacher's write-up is the one they copy. |

---

## 🧭 Differentiation

This section says what to cut, add or change for a student who is struggling, flying or disengaged.

### If the student is struggling

**Cut:** the stability check across subsamples. Five seeds giving ARI 1.0000 is enough.

**Cut:** `run(124)`. Go straight to `run(30)` — two numbers, one comparison, the pile named.

**Cut:** three clusters to two. `k=2`, two cards, two defences.

**Give them `cartography.py` complete.** All of today's learning is in the hand silhouette, the naming, and reading two accuracies with the pile named. **None of it is in typing `groupby`.**

**The version that skips everything hard.** No code at all. One printed table and three questions:

| | real wine | pure noise |
|---|---:|---:|
| silhouette at k = 3 | 0.2849 | 0.0776 |
| same grouping across 5 seeds? | ARI 1.0000 | ARI 0.5791 |

> **"Is 0.2849 a good number?"**
>
> **"What would you have to know to answer that?"**
>
> **"Now look at the second column. Answer it."**

**You cannot tell. You would have to know what a no-structure dataset scores. And 0.2849 against 0.0776 is 3.7 times the floor.** **That is objectives 1 and 2's whole understanding, with no computer and no code**, and it is the most transferable idea in Term 4.

**The copy-this-exactly scaffold.** Eleven lines, runs on its own, and it makes the silhouette concrete without any wine:

```python
import numpy as np
from sklearn.metrics import silhouette_samples, silhouette_score

X = np.array([[1., 2.], [2., 1.], [2., 3.], [8., 8.], [9., 7.], [7., 9.]])
good = np.array([0, 0, 0, 1, 1, 1])
silly = np.array([0, 1, 0, 1, 1, 1])
print("good grouping :", round(silhouette_score(X, good), 4))
print("  per point   :", np.round(silhouette_samples(X, good), 4))
print("silly grouping:", round(silhouette_score(X, silly), 4))
print("  per point   :", np.round(silhouette_samples(X, silly), 4))
```

```text
good grouping : 0.8012
  per point   : [0.8478 0.8163 0.7838 0.8384 0.7618 0.7595]
silly grouping: 0.3751
  per point   : [ 0.8068 -0.8163  0.7797  0.5284  0.487   0.4646]
```

Then two questions and nothing else: **"which grouping is better, and how do you know?"** and **"one number is negative. Which point, and what does it mean?"** **The good one, 0.8012 against 0.3751. And B, at −0.8163, is in the wrong cluster — and nobody told it.** **That is objective 1's understanding in eleven lines.**

**One thing you must not cut:** the noise floor. If the whole lesson collapses to one sentence, make it *"0.2849 means nothing until you know that noise scores 0.0776."*

### If the student is flying

None of these need syntax from a later week.

1. **Leak on purpose and measure it** (Variation-harder 5). **This is the most valuable one on the list**, because the finding is that the leak barely moves the number — so you cannot catch it by noticing a suspiciously good score. **You have to catch it by reading the code.** That is a genuinely level-5 insight and it is the last leakage lesson before the capstone.
2. **Name the noise clusters** (Variation-harder 2). Full ceremony, profile table and all, on random numbers. **They will succeed, and succeeding is the finding.**
3. **Find the seven negative-silhouette bottles** (Variation-harder 3) and look at them. Then: *"what would you do with them in a deployed system?"* **There is no algorithmic answer, which is the answer.**
4. **Push the training set to 20 rows and then 15** (Variation-harder 4), and find where the unsupervised columns stop helping. **Real experimental work with a real answer.**
5. **The disagreeing dataset** (Variation-harder 1): `load_breast_cancer()`, 569 rows, 30 columns. **The two diagnostics do not agree as cleanly, and they have to pick one and defend it.** That is objective 1's hardest half.
6. **Silhouette by hand for point B** (Variation-harder 6), then find their own discrepancy with `silhouette_samples`. **Debugging your own arithmetic against a library is the most useful thing on this list after number 1.**

### If the student won't engage today

**Close the laptop. Two numbers on a piece of paper.**

Write only this:

```text
0.2849
```

> **"Is that a good score?"**

They cannot answer. **Let the silence sit.** Then write:

```text
0.0776    <- what pure random numbers scored
```

> **"Now is it a good score?"**

**Yes — 3.7 times the floor.** **That is the whole of Term 4's honesty lesson in thirty seconds and two numbers**, and it needs nothing else.

If they will take one more, the party question, out loud, no paper:

> **"You're at a party. Your conversation is three people standing close. The next nearest conversation is right across the room. Are you firmly in your group?"**
>
> **"Now: your conversation is three people and one of them is standing two metres away, and the next conversation is a metre and a half from you. Where are you?"**

**Firmly in, then hovering between two.** **That is `a` and `b` and the whole silhouette, with no arithmetic at all.**

If they will take a third, the naming question with the table in front of them:

> **"These 51 wines have flavanoids of 0.82 and everybody else averages 2.03. Give them a name."**

Anything mentioning low flavanoids passes. **Then: "and would you have called them that if I hadn't told you the 2.03?"** **No.** **That is objective 3, discovered.**

The rest survives. Next week starts a completely new subject.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — two votes for `k` (spoken, 60 seconds)**

> "You chose `k = 3`. **Give me two independent reasons, with a number for each.**"

*Good answer:* "The inertia drops were 381.1 going to 3 and only 97.2 going to 4, and `381.1 ÷ 97.2 = 3.9` — the third cluster bought nearly four times what the fourth did. And the silhouette peaks at 3, with 0.2849 against 0.2683 at k=2 and 0.2457 at k=4. Two different measurements, both saying three."

**What to catch:** "the elbow is at 3" with no ratio, or only one reason. **Push once:** *"what number is the elbow?"* **Full marks needs both a ratio and a peak value.** A student who adds *"and the two tools fail in different directions, so agreement is worth more than either"* is at level 5.

**Check 2 — why the elbow cannot decide alone (spoken, 60 seconds)**

> "**Why can I never just pick the `k` with the lowest inertia?** And what value of `k` would that be for the wine data?"

*Good answer:* "Because inertia always falls when you add clusters — it never goes back up. At k = 178 every wine is its own centre, every distance is zero, and inertia is exactly 0. So the smallest inertia is always the most useless answer. You have to look at the bend, and cross-check with something that has a real peak."

**What to catch:** "because it's not accurate" or any answer without `k = 178, inertia 0`. **The number is the proof and the proof is the answer.** A student who then says the silhouette's virtue is that it *does* have a peak is at level 4.

**Check 3 — defend a name (spoken, 90 seconds)**

> "Point at one of your cluster cards and defend the name. **Three numbers, and each one compared to something.**"

*Good answer:* "Dark & Tannic. Flavanoids 0.82 against an overall 2.03 — less than half. Colour intensity 7.23 against 5.06 — much darker. Hue 0.69 against 0.96 — the lowest of the three. 51 bottles, and its own silhouette is 0.3506, the best of the three clusters."

**What to catch:** a bare number with no comparison (`proline 510`), or a number that is not a standout (`alcohol 13.13 vs 13.00`). **Push once:** *"how far is that from the overall?"* **Full marks needs three comparisons, and a student who volunteers which of their three names is weakest — and why — is at level 4.**

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot say what the silhouette measures. Picks `k` by lowest inertia. Names clusters with no numbers, or reports cluster IDs as the result. Compares accuracies without naming the pile. |
| **2 — Emerging** | Runs the sweep and points at the peak when shown where to look. Gives a cluster a name but justifies it with one number, or with a number not compared to the overall. Reads 0.2849 as "good" or "bad" with nothing beside it. |
| **3 — Secure** | Quotes both `381.1 ÷ 97.2 = 3.9` and the silhouette peak `0.2849` as two independent votes. Explains that inertia always falls and gives `k = 178, inertia 0`. Defends three names from a feature-means table in the original units with an overall column. Reports the before-and-after accuracy with the held-out pile named. **This is the target.** |
| **4 — Strong** | Asks for the noise floor before accepting 0.2849, or quotes it unprompted. Identifies cluster 0 as the weak one from its silhouette of 0.1774 and its seven negative points, and says why "low on everything" is a weak basis for a name. Catches the `k=8` bump as noise. Names the 54-of-54 result as a ceiling rather than a failure. |
| **5 — Exceptional** | States which way each diagnostic is biased and reads a disagreement as evidence about overlap. Notices that the five unsupervised columns beat all thirteen original ones at 30 rows and explains it by the row-to-coefficient count. Asks whether the 4-wine gain is bigger than the split-to-split noise, and is satisfied only by the 8-2-0 record rather than the mean. Points out that the seven negative-silhouette rows carry uncertainty that a single cluster-ID column cannot represent, and that this matters if the rows are people. |

---

## 📤 Homework to Assign

This section gives the wording for setting the homework.

**Say this:**

> "About an hour, and it is one document with five pieces in it. **This is the first thing you have handed me all year that is an argument rather than a score**, and next term's capstone is the same shape, so treat it as a rehearsal.
>
> **Piece one, page 30.5 — the elbow plot and the silhouette plot, side by side, and both numbers written under them.** The drop ratio, as a division. The silhouette peak, as a value. **Two independent votes and I want to see both as numbers, not as arrows pointing at bends.**
>
> **Piece two, page 30.6 — the PCA scatter coloured by cluster, and the feature-means table in the original units with an overall column.** Percentages in both axis labels. **A plot with bare 'PC1' on it comes back to you.** And the table must be in real units — if I see `alcohol = 0.83` anywhere, the page comes back.
>
> **Piece three, still on 30.6 — three defended names.** Each one gets three numbers, each number compared to the overall. **And one sentence naming which of your three names is the weakest and why.** That sentence is worth as much as the other three names put together, because anybody can write down their good news.
>
> **Piece four, page 30.7 — add cluster distances and two principal components to a supervised model, and report whether it helped.** The before number, the after number, **the held-out pile named on both**, and the count of rows as well as the percentage. And a sentence on whether you think the difference is real.
>
> **And piece five, which I am marking hardest: the noise floor.** Run your entire pipeline, unchanged, on 178 rows of pure random numbers, and put its silhouette and its seed-to-seed ARI next to your real ones. **Four numbers in a little two-by-two table.** A write-up without that table is a write-up I cannot check, and neither can you."

**Workbook pages:** 30.1, 30.2, 30.3, 30.4 in class · **30.5, 30.6, 30.7** at home.

**Expected time:** 15 min on the two plots and their numbers · 20 min on the map and the profile table · 10 min on the three names and the weak one · 15 min on the supervised experiment · **about 60 minutes**, plus 15 for the noise floor.

> **🧑‍🏫 What to look for when you mark it:** five things, and the fifth is the one that separates a report from a sales brochure. **One — are both votes numbers?** `381.1 ÷ 97.2 = 3.9` and `0.2849`. An arrow pointing at a bend is not a vote. **Two — is the profile table in original units with an overall column?** Both halves. A table in z-scores is unreadable; a table with no overall column is unfalsifiable. **Three — does every name have three comparisons behind it?** And check for `alcohol 13.13 vs 13.00`, which is the standard false positive — **mark it explicitly, because the skill is telling a standout from a coincidence.** **Four — is the pile named on both accuracy rows?** Week 27's rule, and it will be the difference between a capstone report that misleads and one that does not. **Five — is the noise-floor table there, with four numbers in it?** `0.2849 / 0.0776` and `1.0000 / 0.5791`. **This is the piece to mark hardest and to praise loudest, because it is the piece that almost nobody in the world bothers with.** A student who ran their whole pipeline on noise and reported the floor beside their result has produced a more trustworthy document than most published clustering work, and should be told so in exactly those words. **And one bonus: anybody who writes their weak cluster into the argument rather than leaving it out has understood what this course is for.**

---

## 🔑 Answer Key

Every question restated, so you can mark from this page alone.

### Page 30.1 — Predictions, in pen, before running

*Four predictions. (a) Which `k` will the elbow choose? (b) Which `k` will the silhouette choose? (c) Will adding cluster and PCA columns improve a supervised model on the wine? (d) What silhouette will 178 rows of pure noise get?*

| | Most students predict | The truth |
|---|---|---|
| (a) elbow's `k` | 3 or 4 | **3**, with `381.1 ÷ 97.2 = 3.9` |
| (b) silhouette's `k` | 3, or "the same" | **3**, at 0.2849 — **and the two agreeing is the point** |
| (c) will the extra columns help | yes | **not at 124 training rows (54 of 54 either way); yes at 30 (141 → 145)** |
| (d) noise silhouette | 0, or negative, or "it will refuse" | **0.0776 — positive, with three tidy clusters** |

**Marking notes.** **Present or absent, not right or wrong.** (c) and (d) are designed to be got wrong. **What earns credit is a reason attached** — *"the extra columns will help because more information is better"* is a genuine hypothesis and finding out it depends on the row count is the whole of objective 4. **Nearly everybody predicts (d) as zero or negative, and the fact that noise scores a comfortably positive 0.0776 is the single most important surprise of Term 4.**

### Page 30.2 — Silhouette by hand for point C (in class)

*Using Week 28's converged clusters `{A, B, C}` and `{D, E, F}`, compute `s(C)` by hand. Then check it against `silhouette_samples`.*

**These are real distances, not squared ones**, so there are square roots.

```text
a(C) — my average distance to the OTHERS in my own cluster:
   C(2,3) to A(1,2):  √((2−1)² + (3−2)²) = √(1 + 1) = √2  = 1.4142
   C(2,3) to B(2,1):  √((2−2)² + (3−1)²) = √(0 + 4) = √4  = 2.0000
   a = (1.4142 + 2.0000) ÷ 2                              = 1.7071

b(C) — my average distance to EVERYONE in the nearest other cluster:
   C(2,3) to D(8,8):  √((2−8)² + (3−8)²) = √(36 + 25) = √61 = 7.8102
   C(2,3) to E(9,7):  √((2−9)² + (3−7)²) = √(49 + 16) = √65 = 8.0623
   C(2,3) to F(7,9):  √((2−7)² + (3−9)²) = √(25 + 36) = √61 = 7.8102
   b = (7.8102 + 8.0623 + 7.8102) ÷ 3                       = 7.8943

s(C) = (b − a) ÷ whichever is bigger
     = (7.8943 − 1.7071) ÷ 7.8943
     = 6.1872 ÷ 7.8943
     = 0.7838
```

And the check:

```python
import numpy as np
from sklearn.metrics import silhouette_samples, silhouette_score

X = np.array([[1., 2.], [2., 1.], [2., 3.], [8., 8.], [9., 7.], [7., 9.]])
labels = np.array([0, 0, 0, 1, 1, 1])
print("per point :", np.round(silhouette_samples(X, labels), 4))
print("overall   :", round(silhouette_score(X, labels), 4))
print("the mean of the per-point scores:", round(silhouette_samples(X, labels).mean(), 4))
```

```text
per point : [0.8478 0.8163 0.7838 0.8384 0.7618 0.7595]
overall   : 0.8012
the mean of the per-point scores: 0.8012
```

**C is the third: 0.7838. Matches to four decimal places.** ✅ And note the last two lines: `silhouette_score` is exactly the mean of `silhouette_samples`, which is worth printing once so nobody wonders.

**And the silly grouping**, with B moved in with D, E and F:

```python
silly = np.array([0, 1, 0, 1, 1, 1])
print("overall   :", round(silhouette_score(X, silly), 4))
print("per point :", np.round(silhouette_samples(X, silly), 4))
```

```text
overall   : 0.3751
per point : [ 0.8068 -0.8163  0.7797  0.5284  0.487   0.4646]
```

**B scores −0.8163, and a negative score means "I am closer to a different cluster than to my own."** Nothing in that calculation ever saw a right answer.

**Marking notes.** **Two checks.** **One — are they real distances?** A student who used squared distances for C gets `a = (2 + 4) ÷ 2 = 3.0`, `b = (61 + 65 + 61) ÷ 3 = 62.3333` and `s = 0.9519` — wrong, and worth explaining: **the silhouette divides one distance by another, and the ratio of two squares is not the ratio of the two numbers.** Squaring is a shortcut you may take when you are only comparing, never when you are dividing. **Two — is `a` an average over two distances and `b` over three?** Getting `a` over three by including C itself is the other common slip; **`a` is "the OTHERS in my cluster", so C is not one of them.**

### Page 30.3 — The two votes (in class)

*Fill in the sweep table for `k = 2` to `10`, then write both votes as numbers.*

```text
   k    inertia      drop   silhouette
   1     2314.0         -            -
   2     1659.0     655.0       0.2683
   3     1277.9     381.1       0.2849
   4     1180.7      97.2       0.2457
   5     1110.4      70.4       0.2026
   6     1044.5      65.9       0.1960
   7      996.0      48.5       0.1386
   8      944.6      51.4       0.1581
   9      913.2      31.4       0.1417
  10      864.6      48.6       0.1338
```

**Vote 1 — the elbow.** `381.1 ÷ 97.2 = 3.9`. The third cluster bought nearly four times what the fourth did, and after that every extra cluster buys roughly the same as the last (70, 66, 48, 51, 31, 49), which is what "no more structure" looks like. **`k = 3`.**

**Vote 2 — the silhouette.** It peaks at **0.2849 at `k = 3`**, above 0.2683 at k=2 and 0.2457 at k=4, and then falls steadily. **`k = 3`.**

**Both votes say 3, and that agreement is the evidence.**

**The two follow-up questions.** *Why can you never pick the `k` with the smallest inertia?* Because inertia only ever falls. **At `k = 178` every wine is its own centre, every distance is 0, and inertia is exactly 0** — a perfect score carrying no information. *And the bump at `k = 8`?* The silhouette goes 0.1386 at k=7 then back up to 0.1581 at k=8. **That is noise: it beats its neighbour and is nowhere near the peak. A local rise that does not beat the maximum is not a finding.**

**Marking notes.** **Both votes must be numbers.** "The elbow is at 3" without the ratio is half an answer, and the reason to insist is that the ratio is checkable and a bend is not. **Full marks on the second question needs `k = 178` and `inertia = 0`** — the number is the proof.

### Page 30.4 — Three defended names (in class)

*One card per cluster: a name, and three numbers each compared against the overall column. Then one sentence on which name is weakest.*

| cluster | n | its own silhouette | the three numbers | the name |
|---|---:|---:|---|---|
| **2** | 62 | 0.3434 | proline **1100 vs 747** · flavanoids **3.00 vs 2.03** · total phenols **2.85 vs 2.30** | **Bold Reserve** |
| **1** | 51 | 0.3506 | flavanoids **0.82 vs 2.03** · colour intensity **7.23 vs 5.06** · hue **0.69 vs 0.96** | **Dark & Tannic** |
| **0** | 65 | 0.1774 | colour intensity **2.97 vs 5.06** · proline **510 vs 747** · alcohol **12.25 vs 13.00** | **Light & Pale** |

**The weakest-name sentence, and here is what full marks looks like:**

> **Cluster 0 is the weakest, and there are two reasons.** Its own mean silhouette is **0.1774**, about half of cluster 1's 0.3506 and cluster 2's 0.3434, and **seven of its sixty-five bottles score below zero**, which means they sit closer to a different cluster than to their own. And the profile table shows why: **cluster 0 is the lowest of the three on almost every column and the highest on nothing.** "Low on things" is a much weaker basis for a group than "high on a specific thing" — **a cluster defined mainly by absence is often a sign that `k` is too small, or that the real structure is two strong groups plus a continuum of leftovers.**

**Marking notes.** **Any name passes if the numbers support it.** "Rich & Full", "High-Phenol", "Big Wines" are all fine for cluster 2. **What fails is three things, and mark all three explicitly.** **One: a bare number** — `proline 510` with nothing beside it. **Two: a number that is not a standout** — `alcohol 13.13 vs 13.00` for cluster 1 is the classic, it is 0.13 apart, and **telling a standout from a coincidence is the skill on this page.** **Three: a claim not in the table** — "Expensive", "Award-Winning", "Old"; nothing in thirteen chemical measurements says any of those. **And the weakest-name sentence is worth as much as the three names together; a student who identified cluster 0 from its silhouette *and* from its all-low profile has done the whole objective.**

### Page 30.5 — The elbow and silhouette plots (homework)

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import load_wine
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

wine = load_wine()
X_raw = pd.DataFrame(wine.data, columns=wine.feature_names)
X = StandardScaler().fit_transform(X_raw)

ks, inertias, sils = list(range(2, 11)), [], []
for k in ks:
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    inertias.append(km.inertia_)
    sils.append(silhouette_score(X, km.labels_))

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot([1] + ks, [2314.0] + inertias, "o-")
ax[0].set_xlabel("k"); ax[0].set_ylabel("inertia"); ax[0].set_title("Elbow")
ax[1].plot(ks, sils, "o-", color="darkorange")
ax[1].set_xlabel("k"); ax[1].set_ylabel("mean silhouette"); ax[1].set_title("Silhouette")
plt.tight_layout(); plt.savefig("choose_k.png", dpi=110); plt.close()
print("saved choose_k.png")
print("drop ratio 3 -> 4 :", round(381.1 / 97.2, 1))
print("silhouette peak   :", round(max(sils), 4), "at k =", ks[int(np.argmax(sils))])
```

```text
saved choose_k.png
drop ratio 3 -> 4 : 3.9
silhouette peak   : 0.2849 at k = 3
```

**What the plots show.** The elbow plot falls steeply from 2314.0 to 1277.9 and then flattens into a nearly straight gentle slope from k=4 onwards — **the bend is visible but it is not dramatic, which is normal and worth saying.** The silhouette plot has a clear single peak at k=3 and a small meaningless bump at k=8.

**Marking notes.** **Both numbers must be written down, as numbers.** `3.9` and `0.2849 at k = 3`. **A page with two plots and no numbers has drawn pictures rather than gathered evidence**, and the reason it matters is that the capstone report in Week 36 is judged on exactly this distinction.

### Page 30.6 — The map, the profile table, and three names (homework)

```python
from sklearn.decomposition import PCA

km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
labels = km.labels_
pca = PCA(n_components=2).fit(X)
Z = pca.transform(X)
evr = pca.explained_variance_ratio_

names = {0: "Light & Pale", 1: "Dark & Tannic", 2: "Bold Reserve"}
marks = {0: "o", 1: "^", 2: "s"}
plt.figure(figsize=(7, 5.5))
for c in range(3):
    m = labels == c
    plt.scatter(Z[m, 0], Z[m, 1], s=34, alpha=0.85, marker=marks[c],
                label="%d: %s (n=%d)" % (c, names[c], m.sum()))
cen = pca.transform(km.cluster_centers_)
plt.scatter(cen[:, 0], cen[:, 1], marker="X", s=240, c="black", label="centres")
plt.xlabel("PC1 (%.1f%% of the spread)" % (evr[0] * 100))
plt.ylabel("PC2 (%.1f%% of the spread)" % (evr[1] * 100))
plt.title("178 wines, coloured by cluster")
plt.legend(); plt.tight_layout(); plt.savefig("wine_map.png", dpi=110); plt.close()
print("saved wine_map.png")

prof = X_raw.copy()
prof["cluster"] = labels
means = prof.groupby("cluster").mean().T
means["overall"] = X_raw.mean()
print(means.round(2).to_string())
```

```text
saved wine_map.png
cluster                            0       1        2  overall
alcohol                        12.25   13.13    13.68    13.00
malic_acid                      1.90    3.31     2.00     2.34
ash                             2.23    2.42     2.47     2.37
alcalinity_of_ash              20.06   21.24    17.46    19.49
magnesium                      92.74   98.67   107.97    99.74
total_phenols                   2.25    1.68     2.85     2.30
flavanoids                      2.05    0.82     3.00     2.03
nonflavanoid_phenols            0.36    0.45     0.29     0.36
proanthocyanins                 1.62    1.15     1.92     1.59
color_intensity                 2.97    7.23     5.45     5.06
hue                             1.06    0.69     1.07     0.96
od280/od315_of_diluted_wines    2.80    1.70     3.16     2.61
proline                       510.17  619.06  1100.23   746.89
```

**The map:** three groups, clearly separated left to right along PC1, with the cluster-1 triangles top-left, the cluster-2 squares to the right and the cluster-0 circles low and central. **`36.2 + 19.2 = 55.4`, so 44.6% of the spread in these wines is not on the page** — and the honest comparison is with last week's uncoloured version of the same plot, which looked like a single blob.

Names and defences: as on page 30.4.

**Marking notes.** **Three hard checks.** **One — percentages in both axis labels.** `36.2%` and `19.2%`. **Two — original units in the table, and an overall column.** A `0.83` anywhere means they profiled the scaled table. **Three — shapes as well as colours in the plot**, so it survives a photocopier. And **a student who compared this map with Week 29's uncoloured one and noticed that the structure was invisible until it was coloured has made the connection the whole fortnight was built for.**

### Page 30.7 — Do the new columns earn their keep, and the noise floor (homework)

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import adjusted_rand_score

y = wine.target


def run(n_train, state=0):
    a, b, ya, yb = train_test_split(X_raw, y, train_size=n_train,
                                    random_state=state, stratify=y)
    sc = StandardScaler().fit(a)                      # TRAIN rows only
    Za, Zb = sc.transform(a), sc.transform(b)
    k3 = KMeans(n_clusters=3, n_init=10, random_state=0).fit(Za)
    pc = PCA(n_components=2).fit(Za)
    Aa = np.c_[Za, k3.transform(Za), pc.transform(Za)]
    Ab = np.c_[Zb, k3.transform(Zb), pc.transform(Zb)]
    for tag, p, q in [("13 raw columns      ", Za, Zb),
                      ("13 + 3 dists + 2 PCs", Aa, Ab)]:
        acc = LogisticRegression(max_iter=5000).fit(p, ya).score(q, yb)
        print("  %s  %.4f  (%d of %d held-out wines)"
              % (tag, acc, round(acc * len(yb)), len(yb)))


print("--- 124 training rows ---")
run(124)
print("--- 30 training rows ---")
run(30)
```

```text
--- 124 training rows ---
  13 raw columns        1.0000  (54 of 54 held-out wines)
  13 + 3 dists + 2 PCs  1.0000  (54 of 54 held-out wines)
--- 30 training rows ---
  13 raw columns        0.9527  (141 of 148 held-out wines)
  13 + 3 dists + 2 PCs  0.9797  (145 of 148 held-out wines)
```

**The sentence being marked, and here is full marks:**

> **With 124 labelled training rows the five new columns bought nothing: 54 of 54 held-out wines either way.** That is not evidence against them — **it is a ceiling.** The problem was already completely solved, so nothing could improve it, and the experiment cannot answer the question.
>
> **With only 30 labelled training rows, on the other 148 held-out wines, 13 raw columns got 141 of 148 (0.9527) and the 18-column version got 145 of 148 (0.9797) — a gain of 4 wines, or +2.70 accuracy points.** All five new columns were fitted on the 30 training rows only, so no held-out wine touched any fitting.
>
> **Is it real?** Over ten different 30-row splits the mean gain is **+1.15 points**, which is smaller than this split suggested and about the same size as the baseline's own split-to-split standard deviation of **0.0125**. **So the size of the gain is not convincing on its own — but the 18-column version won 8 times, tied twice and never lost, and that consistency is the evidence.**

**And piece five, the noise floor:**

```python
noise = np.random.default_rng(0).normal(size=(178, 13))
kmn = KMeans(n_clusters=3, n_init=10, random_state=0).fit(noise)
real = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
print("               silhouette   seed-to-seed ARI")
for tag, data, km0 in [("real wine ", X, real), ("pure noise", noise, kmn)]:
    aris = [adjusted_rand_score(km0.labels_,
            KMeans(n_clusters=3, n_init=10, random_state=s).fit(data).labels_)
            for s in (1, 2, 3, 4, 5)]
    print("%s       %.4f            %.4f"
          % (tag, silhouette_score(data, km0.labels_), np.mean(aris)))
```

```text
               silhouette   seed-to-seed ARI
real wine        0.2849            1.0000
pure noise       0.0776            0.5791
```

**And the reading, which is the whole page:**

> **0.2849 on its own is meaningless.** Against the field guide it is "real, but the clusters touch". **Against a floor of 0.0776 from a dataset with no structure in it at all, it is 3.7 times the floor.** And the stability numbers make the same point harder: our grouping is **identical across five different seeds** (ARI 1.0000) where the noise grouping agrees with itself only **0.5791** of the time. **Those two comparisons together are the argument that the wine structure is real, and neither number means anything without its partner.**

**Marking notes.** **Four bars, and the last two are what separate a report from a brochure.** **One — is the pile named on both accuracy rows?** `54 of 54` and `141 of 148` with the training-row count stated. **Two — is the count there as well as the percentage?** "4 more wines" is checkable; "+2.70%" alone is not. **Three — is the 124-row result named as a ceiling?** A student who concludes "the features don't help" from 54-of-54 has drawn the wrong inference and it is worth writing out in your feedback, because it is exactly the mistake that kills real experiments. **Four — is the noise-floor two-by-two there, with all four numbers?** `0.2849 / 0.0776` and `1.0000 / 0.5791`. **Mark this hardest and praise it loudest.** Almost no published clustering write-up includes a negative control; a 14-year-old who has one has done more trustworthy work than most of the field, and they should be told that in those words.

### Answers to every question posed in the lesson

**Hook — "could you write a report about those two groups?"** **Yes.** Their column means genuinely differ — cluster 0 is low on column 1, cluster 1 is high on it and on column 4. **And there is no structure in the data whatsoever.**

**Hook — "could you give them names?"** **Yes, easily.** Which is the problem. **Getting clusters is not evidence that there are clusters.**

**Concept — "what `k` gives the smallest inertia, and what is it?"** **`k` = 178**, one cluster per wine, and inertia is **exactly 0**. Perfect score, zero information.

**Concept — "now `b`. How many distances this time?"** **Three** — D, E and F, every member of the other cluster.

**Concept — "`a` is 1.7071 and `b` is 7.8943. Good place or bad place?"** **Good** — C is about four and a half times closer to its own clustermates than to the other cluster.

**Concept — "which of those six is C?"** **The third, 0.7838** — exactly the hand-computed value.

**Concept — "one of those six numbers is negative. Which point, and what is it telling us?"** **B, at −0.8163.** B is in the wrong cluster, and nothing in the calculation ever saw a right answer.

**Concept — "vote one, the elbow. Give me a number."** `381.1 ÷ 97.2 = 3.9` — **`k = 3`.**

**Concept — "vote two. Where is the peak?"** **`k = 3`, at 0.2849.**

**Concept — "and what if they had disagreed?"** Then you have learned something. **The elbow tends to over-count** (splitting a big loose cluster always buys inertia); **the silhouette tends to under-count when clusters touch** (border points score near 0 and drag the mean down, and merging removes the border). **So silhouette pulling lower than the elbow is the fingerprint of overlap.** And domain sense outranks both: **if you can only act on three groups, the answer is three.**

**Concept — "what is the honest description of these clusters?"** **"Real, but they touch."** 0.2849 is in the 0.25–0.5 band. **And it only becomes a finding beside the noise floor of 0.0776 — 3.7 times.**

**Live-code step 1 — "is eight better than seven?"** The silhouette is higher at 8 (0.1581) than at 7 (0.1386), **and it is less than half the peak. A bump that does not beat the maximum is noise, not structure.**

**Live-code step 2 — "why can it not give me a silhouette for one cluster?"** **Because there is no `b`.** `b` is the distance to the nearest *other* cluster, and with one cluster there is no other. **The quantity does not exist** — which is also why the silhouette cannot compare `k=1` against `k=3`.

**Live-code step 3 — "why is the profile table in the original units?"** **Because "alcohol = 0.83" means nothing to a human being and "alcohol = 13.68" means something to a winemaker.** You cluster in the scaled world and report in the real one.

**Live-code step 3 — "why is the `overall` column there?"** **Because a number with nothing beside it is not evidence.** "Flavanoids 0.82" is not a fact about anything; "0.82 against an overall 2.03" is.

**Live-code step 3 — "cluster 1's alcohol is 13.13 and overall is 13.00. Does that help name it?"** **No — 0.13 apart, it defends nothing.** Compare with flavanoids, 0.82 against 2.03, which is a difference you can build a name on.

**Live-code step 4 — "0.5711 against 0.2849. Which clustering is better?"** **The one with the lower silhouette.** ARI against the real grape varieties is **0.3711** for the unscaled clustering and **0.8975** for the scaled one. **The unscaled clusters are three non-overlapping bands of proline, and nothing is tidier than three bands of one column — they are just separated along the wrong thing.** So: **the silhouette measures the shape of your grouping in the space you measured it in; it does not measure whether the grouping is right.** And separately, **score in the same space you clustered in** — scoring the scaled labels on the raw table gives a third meaningless number, 0.1943.

**Live-code step 5 — "is 0.2849 a good score?"** **"Compared to what?"** — and that is the right first move. **Against the noise floor of 0.0776 it is 3.7 times higher, and our grouping is perfectly stable across five seeds where noise manages 0.5791.**

**Activity A step 4 — "which of your three names is weakest, and why?"** **Cluster 0.** Its own silhouette is 0.1774 against 0.3506 and 0.3434, **seven of its 65 bottles score below zero**, and in the profile table it is lowest on almost everything and highest on nothing. **"Low on things" is a weaker basis for a group than "high on a specific thing."**

**Activity B step 1 — "did the five new columns help?"** **No — 54 of 54 either way.** **"Is that the same as useless?"** **No.** The problem was already solved; there was no room. **That is a ceiling, and the experiment cannot answer the question.**

**Activity B step 2 — "how many more wines?"** **Four: 141 of 148 becomes 145 of 148.** **"And the third row?"** **The five new columns on their own got 146 of 148 — they beat all thirteen original columns**, because with 30 rows a 13-column model has 42 coefficients and nowhere near enough rows, while k-means used all 30 rows' geometry with no labels at all (the same 30 rows, so mostly a dimensionality-reduction effect).

**Activity B step 3 — "is four wines real or a lucky split?"** Over ten splits the mean gain is **+1.15 points** against a baseline wobble of **0.0125**, so the size is not convincing — **but the 18-column model won 8, tied 2 and lost 0. The consistency is the evidence, not the size.**

**Wrap — "how many groups in last week's plot? How many now?"** **One blob, then three.** Same points, same axes. **The structure was there the whole time and the picture could not show it** — which is why you need a number and not a plot.

**Wrap — "which line of the five-line argument is a score?"** **None of them.** There was no answer key. **Every line is a comparison against something, and that is what an argument looks like.**

**Variation-harder 5 — leak on purpose.** Fitting the scaler, k-means and PCA on all 178 rows before splitting **barely changes the number on this dataset**, which is the uncomfortable finding: **you cannot catch unsupervised leakage by noticing a suspiciously good score. You catch it by reading the code.** On 178 rows with 13 well-behaved columns, PCA fitted on all of them and PCA fitted on a training fold produce nearly the same directions. **Change the shape — 300 rows and 20,000 columns, as in genetics — and the same one-line mistake can inflate a score enormously. The size of a leak depends on the shape of your data, not on how wrong the code looks.**

**Variation-harder 6 — `s(B)` by hand.** With the converged clusters `{A, B, C}` and `{D, E, F}`: `a(B)` averages B-to-A (√2 = 1.4142) and B-to-C (√4 = 2.0000), giving **1.7071**; `b(B)` averages B-to-D (√85 = 9.2195), B-to-E (√85 = 9.2195) and B-to-F (√89 = 9.4340), giving **9.2910**; so `s(B) = (9.2910 − 1.7071) ÷ 9.2910 = 7.5839 ÷ 9.2910 = ` **0.8163**, and `silhouette_samples` prints **0.8163**. ✅ **And the harder half: do it again with squared distances and see what a wrong method gives you.** `a = (2 + 4) ÷ 2 = 3.0`, `b = (85 + 85 + 89) ÷ 3 = 86.3333`, `s = (86.3333 − 3.0) ÷ 86.3333 = 0.9653` — **plausible, on the right scale, and wrong.** The reason is worth saying out loud: **the silhouette divides one distance by another, and the ratio of two squares is not the ratio of the two numbers.** Squaring is a shortcut you may take when you are only comparing, never when you are dividing.

---

## 🔮 Next Week Preview

Next week Term 4 changes subject completely, and it is the last new topic before the capstone: **words.** Everything in this course so far has been numbers in a table — pizza minutes, pixel brightnesses, wine chemistry. **Next week the data is four restaurant reviews written on the whiteboard, and the first problem is that there is no arithmetic you can do on the word "brilliant".** So the whole week is about turning text into a table: splitting a sentence into words with `re.findall`, lower-casing so that `Great` and `great` stop being two different things, building a **vocabulary** of every word that appears anywhere in the corpus, and then giving every review one row with **one column per vocabulary word** holding how many times that word appeared. That is the **bag of words**, and the two things to notice about it are that it throws away word order entirely — *"not good"* and *"good, not"* become the same row — and that **most of the table is zeros**, because a ten-word review in a two-thousand-word vocabulary fills ten cells and leaves 1,990 empty. Then the student types out a 60-review corpus of their own, which becomes the dataset for Weeks 31, 32 and 33.

**To prep early:** three things. **One — the student needs to start typing reviews now, not on the night before Week 33.** Forty positive and forty negative, one line each, their own words, about films or food or games. **Set it this week as a background task and check on it in Week 31**, because Week 33's sentiment engine needs eighty of them and typing eighty reviews in one evening produces eighty bad reviews. **Two — check `import re` and `from sklearn.feature_extraction.text import CountVectorizer` both work tonight**, and that `CountVectorizer().fit(["great pizza", "cold pizza"]).get_feature_names_out()` prints `['cold' 'great' 'pizza']`. Both ship with Python and scikit-learn; nothing downloads. **Three — the SIX POINTS sheet came down today, and a new one goes up next week headed VOCABULARY**, with room for about twenty words in alphabetical order. Week 31's whole first half is built at that sheet.

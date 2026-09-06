# Module 8 — Learning Without Labels: k-Means and PCA

**Level 3 · Module 8 · ~5 hours · Prereqs: Module 2 (standardization, `ColumnTransformer`), Module 3 (cross-validation discipline), and comfort with `numpy` arrays and matplotlib.**

[⬅ Previous](module-07-cnns-for-images.md) · [Level 3 Home](README.md) · [Next ➡](module-09-classic-nlp.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. You will be able to run the k-means loop by hand for two full iterations on a tiny 2-D dataset, showing every squared distance.
2. You will be able to choose `k` using the inertia elbow *and* the silhouette score, and defend the choice when the two disagree.
3. You will be able to explain why k-means is helpless without feature scaling, with a numeric example where the answer flips.
4. You will be able to describe a principal component as a new axis chosen to capture the most variance, and compute one for a 5-point dataset.
5. You will be able to project high-dimensional data to 2-D with PCA, read the explained-variance ratio, and reconstruct the original data with a measurable error.
6. You will be able to turn cluster IDs and principal components into engineered features for a supervised model.

---

## 🪝 The Hook

A supermarket chain hands you a spreadsheet. 40,000 rows, one per loyalty-card member. Columns: visits per month, average basket value, fraction of spend on fresh produce, fraction on ready meals, weekend-visit share, distance from store, number of distinct categories bought.

There is no target column. Nobody has labelled anyone. There is no "customer type" field, because customer types are not a thing that exists in the world — they're a thing marketing departments *invent*, and this one hasn't been invented yet. Your job is to invent it, defensibly.

Every technique in this level so far has needed a `y`. Every metric — accuracy, precision, log loss — needed a right answer to compare against. Take the right answers away and something uncomfortable happens: **you can still run algorithms, but you can no longer tell whether they worked.**

That is the whole subject of this module. Two of the most useful unsupervised tools ever built, and — just as important — the honest habits you need so that you don't mistake a picture for a discovery.

---

## 🧠 The Concept

### 1. Unsupervised learning, and what "no ground truth" actually costs you

> **Supervised learning:** you have `X` and `y`. The algorithm learns a mapping, and you score it by comparing predictions to the real `y`.

> **Unsupervised learning:** you have only `X`. The algorithm finds structure. There is nothing to compare against.

That second sentence sounds mild and is not. Here's the concrete consequence:

| Question | Supervised | Unsupervised |
|---|---|---|
| Is my model good? | Compare to held-out `y` — a number | No held-out truth exists |
| Did I overfit? | Train score ≫ test score | Hard to even define |
| Is the answer correct? | Yes/no per row | There is no correct answer |
| What can I measure? | Accuracy, F1, AUC, log loss | Internal consistency, and stability |

🍕 **Analogy.** Supervised learning is a maths exam with an answer key at the back. Unsupervised learning is being handed a box of 500 mixed Lego bricks and asked to sort them into piles. By colour? By size? By shape? By which set they came from? *Every one of those is a valid sorting*, and there's no key to check. What you *can* do is defend your choice: "I sorted by shape because the piles came out roughly even, the bricks inside each pile really do look alike, and shape is what matters for building."

So unsupervised work has a different deliverable. In supervised learning you ship a score. In unsupervised learning you ship an **argument**: here is the structure I found, here is my evidence that it's real and not an artefact, and here is the part I'm least sure about. The mini-project at the end of this module is graded on exactly that.

Two things you *can* legitimately measure without labels:

- **Internal quality** — are points inside a cluster close together and far from other clusters? (Silhouette score does this.)
- **Stability** — if you re-run on a random 80% of the data, or with a different random seed, do you get roughly the same structure? Structure that vanishes when you jiggle the data was never there.

---

### 2. k-means: assign, move, repeat

> **Cluster:** a group of data points that are more similar to each other than to points outside the group.

> **Centroid:** the mean position of all points currently assigned to a cluster — the cluster's centre of gravity.

k-means is one of the simplest algorithms in machine learning, and you can state it completely in four lines:

```
1. Pick k starting centroids.
2. ASSIGN : give every point to its nearest centroid.
3. MOVE   : recompute each centroid as the mean of the points assigned to it.
4. Repeat 2 and 3 until nobody changes cluster. Stop.
```

That's it. Steps 2 and 3 alternate, and the algorithm provably never gets worse.

🍕 **Analogy.** Three food trucks want to park in a big park full of picnickers. Round 1: each picnicker walks to whichever truck is nearest. Round 2: each truck notices where its own customers are sitting and drives to the middle of them. Round 3: some picnickers realise a different truck is now closer and switch. The trucks move again. After a few rounds nobody switches, the trucks stop moving, and you have three neighbourhoods.

**What it is minimising.** k-means is greedily reducing one number:

> **Inertia (also: within-cluster sum of squares, WCSS):** the total squared distance from every point to its own centroid.
> ```
> inertia = Σ_over_all_points  ‖ x − centroid(x) ‖²
> ```

Lower inertia = tighter clusters. The assign step can only lower it (each point moves to a nearer centre) and the move step can only lower it (the mean is the point that minimises squared distance to a set). Hence: monotone decrease, guaranteed convergence.

**But it converges to a local minimum, not the best one.** Where you start matters. Put two initial centroids inside the same true cluster and k-means may happily split that cluster in half and merge two others. The fix everyone uses is `k-means++`, a smarter initialisation that spreads the starting centroids apart, plus running the whole thing `n_init` times from different seeds and keeping the run with the lowest inertia. scikit-learn does both by default (`init="k-means++"`, `n_init=10`), which is why you rarely see this failure — but you should know it's being handled for you.

**Three things k-means assumes, whether or not they're true:**

| Assumption | What breaks if it's false |
|---|---|
| Clusters are roughly spherical blobs | Two long parallel stripes get sliced crosswise instead of separated |
| Clusters are roughly the same size and density | A big loose cluster gets split; a small tight one gets absorbed |
| Every point belongs to exactly one cluster | Outliers are forcibly assigned and drag centroids off-centre |

**And the assumption that bites hardest: scale.** k-means measures distance. Distance sums squared differences across features. If one feature is measured in rupees (range 0–10,000,000) and another in years (range 18–80), then the rupee feature contributes about 10¹⁴ to every squared distance and the year feature contributes about 10³. The age column has effectively been deleted.

**A numeric example where scaling flips the answer.** Three customers, features (age in years, annual income in rupees):

```
P1 = (25, 500000)
P2 = (55, 500000)
P3 = (25, 520000)
```

Raw squared distances:

```
d(P1,P2)² = (25−55)² + (500000−500000)² =    900 +            0 =           900
d(P1,P3)² = (25−25)² + (500000−520000)² =      0 +  400,000,000 =   400,000,000
```

So raw k-means says P1 and P2 are **444,000 times more similar** than P1 and P3 — even though P1 and P2 are thirty years apart in age and P1 and P3 differ by a 4% salary bump. That is nonsense, and it is not a bug; it is what "distance" means when you don't scale.

Now standardize each column (subtract the mean, divide by the standard deviation, as in Module 2):

```
age:    mean 35,          std 14.142   →  z = (−0.7071, +1.4142, −0.7071)
income: mean 506,666.67,  std 9,428.09 →  z = (−0.7071, −0.7071, +1.4142)
```

Standardized squared distances:

```
d(P1,P2)² = (−0.7071 − 1.4142)² + 0 = (−2.1213)² = 4.5
d(P1,P3)² = 0 + (−0.7071 − 1.4142)² = (−2.1213)² = 4.5
```

Now they are **exactly equal**, which is the honest answer: each pair differs by the same amount in one standardized feature and not at all in the other. Rule to memorise:

> **Always scale before k-means.** Standardization is the default. The only exception is when all your features are already in the same natural unit and you genuinely want the bigger-ranged one to count more.

---

### 3. Choosing k: the elbow, the silhouette, and domain sense

k-means requires you to name `k` in advance. Nothing in the algorithm chooses it. So how?

**Method 1 — the inertia elbow.**

Plot inertia against `k`. Inertia always falls as `k` rises (at `k = n`, every point is its own centroid and inertia is exactly 0), so you can't just pick the minimum. What you look for is the **elbow**: the `k` after which extra clusters stop buying you much.

```
inertia
  │
2314├●
  │   ╲
1659├    ●
  │       ╲
1278├         ●  ← elbow: the bend
  │            ╲___
1188├               ●───────●───────●
  │
  └───┬───┬───┬───┬───┬───┬───┬──  k
      1   2   3   4   5   6   7
```

Going 2 → 3 saved 381 units of inertia. Going 3 → 4 saved only 90. That knee at k = 3 is the elbow. Honest warning: **elbows are often not obvious**, and two reasonable people will read the same curve differently. It's a hint, not a verdict.

**Method 2 — the silhouette score.**

> **Silhouette score for one point:** how much closer that point is to its own cluster than to the next-nearest cluster, scaled to the range −1 to +1.
> ```
> a = mean distance from the point to the OTHER points in its own cluster
> b = mean distance from the point to all points in the NEAREST OTHER cluster
> s = (b − a) / max(a, b)
> ```

Reading it:

| s | Meaning |
|---|---|
| near **+1** | comfortably inside its cluster, far from the others |
| near **0** | sitting on the border between two clusters |
| near **−1** | probably in the wrong cluster — it's closer to a different one |

The **overall silhouette score** is the mean of `s` over all points. Unlike inertia it does *not* automatically improve with more clusters, so you can pick the `k` that maximises it. Rough field guide: above 0.5 is strong structure, 0.25–0.5 is real but overlapping, below 0.25 means the clusters are mostly a convenient fiction. Real-world tabular data very often lands in the 0.25–0.4 band, and that's fine — you just have to say so.

🍕 **Analogy.** You're at a party that has split into groups. Your `a` is how far you'd have to walk to reach the average person in your own conversation. Your `b` is how far to reach the average person in the next-nearest conversation. If `b` is much bigger than `a`, you're firmly in your group. If they're about equal, you're that person hovering between two circles, half-in on both.

**Method 3 — domain sense, which outranks both.**

If the elbow says 4, the silhouette says 2, and the marketing team can only run three different campaigns, the answer is 3. Clustering is a tool for making decisions, and the number of decisions you can actually act on is a real constraint. Say so in your write-up rather than pretending the maths decided.

---

### 4. The curse of dimensionality

> **Curse of dimensionality:** as the number of features grows, points spread out until every point is roughly equally far from every other point — and distance-based methods stop meaning anything.

Here's the intuition. In 1-D, two random points in [0,1] are on average 0.33 apart. Add a second dimension and they're on average 0.52 apart. Keep going and the distances keep growing — but, crucially, the *spread* of those distances grows more slowly than the distances themselves. So the ratio

```
(farthest distance − nearest distance) / nearest distance
```

collapses toward zero. "Nearest neighbour" stops being a meaningful category, because everything is a nearest neighbour.

🍕 **Analogy.** In a 1-D world (a corridor), your nearest neighbour is obviously the person next to you. In a 2-D world (a field), still fine. In a 500-D world, every single person is standing at almost exactly the same distance from you — none of them is meaningfully "near." k-means, k-NN, and every other algorithm that squints at distances go blind.

**Rough numbers** (200 uniform random points, ratio above):

| dimensions | (max − min) / min |
|---:|---:|
| 2 | ≈ 55 |
| 5 | ≈ 8 |
| 20 | ≈ 1.8 |
| 100 | ≈ 0.7 |
| 1000 | ≈ 0.2 |

At 1,000 dimensions, the farthest point is only 20% farther than the nearest. You'll reproduce this in Practice 5.

The practical response: **reduce dimensions before you cluster.** Which brings us to PCA.

---

### 5. PCA: new axes that capture the most variance

> **Principal Component Analysis (PCA):** rotate the coordinate system so the first new axis points along the direction of greatest variance in the data, the second along the greatest remaining variance perpendicular to the first, and so on.

Say that again in plain words: PCA doesn't delete features. It **replaces** them with combinations of themselves, ordered by how much of the data's spread each combination explains. Then you keep the top few and throw away the rest.

🍕 **Analogy.** You've got a long thin cloud of midges hanging in a garden, and you want to photograph it. One camera angle shows a long streak — informative, you can see the whole shape. Another angle looks straight down the length of the cloud and shows a small blob — you've lost almost everything. PCA finds the first angle. The first principal component is "the direction the cloud is longest in."

**The recipe:**

```
1. Centre the data (subtract each feature's mean). PCA is about spread, not location.
2. Compute the covariance matrix of the centred data.
3. Find its eigenvectors and eigenvalues.
   - each eigenvector is a direction (a principal component)
   - its eigenvalue is the variance of the data along that direction
4. Sort by eigenvalue, largest first. Keep the top m.
5. Project: score = centred_point · component
```

You do not have to be able to compute eigenvectors by hand — `sklearn` does it. You *do* have to understand what the numbers mean.

> **Explained variance ratio:** each component's eigenvalue divided by the sum of all eigenvalues. "PC1 explains 36% of the total variance" means: if you kept only PC1, you'd preserve 36% of the data's total spread.

**Two rules you'll use constantly:**

- **Standardize first, almost always.** PCA maximises variance, and variance depends on units. Measure a length in millimetres instead of metres and its variance goes up by a factor of a million — PC1 will point straight along it regardless of whether it matters. Standardizing puts every feature on variance 1 so PCA compares *shapes*, not units.
- **PCA is unsupervised.** It has never seen `y`. The direction of greatest variance is not guaranteed to be the direction that predicts your target. Usually it helps; occasionally the discriminative signal lives in a low-variance component and PCA throws it away. Test, don't assume.

> **Reconstruction:** project down to `m` components, then project back up to the original space. What you get back is an approximation. The gap is the information you discarded.
> ```
> X_reconstructed = scores @ components + mean
> ```

Reconstruction error is a real, measurable thing — it's the honest price tag on your dimensionality reduction, and unlike most unsupervised quantities it needs no labels.

---

### 6. Clusters and components as engineered features

Both of these tools produce columns you can feed straight into a supervised model, which connects this module back to Module 2.

**Cluster ID as a feature.** Run k-means on your training features, then add `cluster_id` as a categorical column (one-hot encoded). This lets a linear model express things like "high-spending weekend shoppers behave differently" without you having to hand-write the interaction. It sometimes helps a lot and sometimes does nothing.

**Distance-to-each-centroid as features.** Better than the raw ID, usually: instead of one categorical column, add `k` numeric columns holding the distance from each row to each centroid. Keeps the "how strongly does this row belong" information that a hard ID throws away.

**Principal components as features.** Replace 200 correlated columns with the top 20 PCs. Fewer parameters, less multicollinearity, faster training.

⚠️ **The leakage rule from Module 2 applies with full force.** `KMeans` and `PCA` both **fit** on data — they learn centroids and components. If you fit them on the whole dataset before splitting, information from your test rows has leaked into your training features. Put them inside a `Pipeline`:

```python
pipe = Pipeline([
    ("scale", StandardScaler()),
    ("pca",   PCA(n_components=10)),
    ("clf",   LogisticRegression(max_iter=1000)),
])
```

Now `cross_val_score(pipe, X, y)` refits the scaler and the PCA on each training fold only, which is the only correct thing to do.

---

## 🔍 Worked Example

Two parts: k-means run by hand to convergence, then PCA computed by hand on a 5-point dataset.

### Part 1 — k-means, two full iterations

**The data.** Six points in 2-D:

```
A = (1, 2)      D = (8, 8)
B = (2, 1)      E = (9, 7)
C = (2, 3)      F = (7, 9)
```

**The initialisation.** `k = 2`, starting centroids deliberately chosen badly — both in the left-hand blob:

```
μ₁ = (1, 2)     (point A)
μ₂ = (2, 3)     (point C)
```

We'll use **squared** Euclidean distance throughout. Squaring doesn't change which centroid is nearest, and it avoids square roots.

---

**ITERATION 1, assign step.**

| point | d² to μ₁ = (1,2) | d² to μ₂ = (2,3) | winner |
|---|---|---|---|
| A (1,2) | (1−1)² + (2−2)² = 0 + 0 = **0** | (1−2)² + (2−3)² = 1 + 1 = 2 | **C1** |
| B (2,1) | (2−1)² + (1−2)² = 1 + 1 = **2** | (2−2)² + (1−3)² = 0 + 4 = 4 | **C1** |
| C (2,3) | (2−1)² + (3−2)² = 1 + 1 = 2 | (2−2)² + (3−3)² = **0** | **C2** |
| D (8,8) | (8−1)² + (8−2)² = 49 + 36 = 85 | (8−2)² + (8−3)² = 36 + 25 = **61** | **C2** |
| E (9,7) | (9−1)² + (7−2)² = 64 + 25 = 89 | (9−2)² + (7−3)² = 49 + 16 = **65** | **C2** |
| F (7,9) | (7−1)² + (9−2)² = 36 + 49 = 85 | (7−2)² + (9−3)² = 25 + 36 = **61** | **C2** |

Assignments: **C1 = {A, B}**, **C2 = {C, D, E, F}**.

Notice how bad this is — the algorithm has lumped C in with the far-away right-hand blob, purely because μ₂ happened to sit on top of C.

**ITERATION 1, move step.**

```
μ₁ = mean of {A, B}
   = ( (1 + 2)/2 , (2 + 1)/2 )
   = ( 1.5 , 1.5 )

μ₂ = mean of {C, D, E, F}
   = ( (2 + 8 + 9 + 7)/4 , (3 + 8 + 7 + 9)/4 )
   = ( 26/4 , 27/4 )
   = ( 6.5 , 6.75 )
```

---

**ITERATION 2, assign step.**

| point | d² to μ₁ = (1.5, 1.5) | d² to μ₂ = (6.5, 6.75) | winner |
|---|---|---|---|
| A (1,2) | (−0.5)² + (0.5)² = 0.25 + 0.25 = **0.50** | (−5.5)² + (−4.75)² = 30.25 + 22.5625 = 52.8125 | **C1** |
| B (2,1) | (0.5)² + (−0.5)² = 0.25 + 0.25 = **0.50** | (−4.5)² + (−5.75)² = 20.25 + 33.0625 = 53.3125 | **C1** |
| C (2,3) | (0.5)² + (1.5)² = 0.25 + 2.25 = **2.50** | (−4.5)² + (−3.75)² = 20.25 + 14.0625 = 34.3125 | **C1** ← switched! |
| D (8,8) | (6.5)² + (6.5)² = 42.25 + 42.25 = 84.50 | (1.5)² + (1.25)² = 2.25 + 1.5625 = **3.8125** | **C2** |
| E (9,7) | (7.5)² + (5.5)² = 56.25 + 30.25 = 86.50 | (2.5)² + (0.25)² = 6.25 + 0.0625 = **6.3125** | **C2** |
| F (7,9) | (5.5)² + (7.5)² = 30.25 + 56.25 = 86.50 | (0.5)² + (2.25)² = 0.25 + 5.0625 = **5.3125** | **C2** |

Assignments: **C1 = {A, B, C}**, **C2 = {D, E, F}**.

Point C switched sides. The bad initialisation has repaired itself in exactly one round.

**ITERATION 2, move step.**

```
μ₁ = ( (1 + 2 + 2)/3 , (2 + 1 + 3)/3 ) = ( 5/3 , 6/3 ) = ( 1.6667 , 2.0 )
μ₂ = ( (8 + 9 + 7)/3 , (8 + 7 + 9)/3 ) = ( 24/3 , 24/3 ) = ( 8.0 , 8.0 )
```

**ITERATION 3 would change nothing** — A, B, C are all obviously nearer (1.67, 2.0) than (8, 8), and D, E, F the reverse. No assignment changes ⇒ **converged in 2 iterations.**

**Final inertia.**

```
Cluster 1, centroid (1.6667, 2.0):
  A: (1 − 1.6667)² + (2 − 2)²  = 0.4444 + 0      = 0.4444
  B: (2 − 1.6667)² + (1 − 2)²  = 0.1111 + 1.0000 = 1.1111
  C: (2 − 1.6667)² + (3 − 2)²  = 0.1111 + 1.0000 = 1.1111
                                            sum   = 2.6667

Cluster 2, centroid (8, 8):
  D: (8−8)² + (8−8)² = 0 + 0 = 0
  E: (9−8)² + (7−8)² = 1 + 1 = 2
  F: (7−8)² + (9−8)² = 1 + 1 = 2
                       sum   = 4

TOTAL INERTIA = 2.6667 + 4 = 6.6667
```

**Silhouette for point C, by hand.** Now we need actual (non-squared) distances.

```
a(C) = mean distance to the OTHER members of C1 = {A, B}
     d(C,A) = √((2−1)² + (3−2)²) = √2      = 1.4142
     d(C,B) = √((2−2)² + (3−1)²) = √4      = 2.0000
     a = (1.4142 + 2.0000) / 2             = 1.7071

b(C) = mean distance to every member of C2 = {D, E, F}
     d(C,D) = √((2−8)² + (3−8)²) = √(36+25) = √61 = 7.8102
     d(C,E) = √((2−9)² + (3−7)²) = √(49+16) = √65 = 8.0623
     d(C,F) = √((2−7)² + (3−9)²) = √(25+36) = √61 = 7.8102
     b = (7.8102 + 8.0623 + 7.8102) / 3            = 7.8942

s(C) = (b − a) / max(a, b) = (7.8942 − 1.7071) / 7.8942
     = 6.1871 / 7.8942
     = 0.7838
```

**s(C) ≈ 0.78** — comfortably inside its cluster. Which makes sense: after convergence, C is 1.7 units from its clustermates on average and 7.9 units from the other cluster.

### Part 2 — PCA by hand on five points

**The data.** Five students, `(hours studied, hours slept)` per week:

```
(4, 3)   (6, 6)   (8, 7)   (10, 8)   (12, 11)
```

**Step 1 — centre it.**

```
mean_x = (4 + 6 + 8 + 10 + 12) / 5 = 40 / 5 = 8
mean_y = (3 + 6 + 7 +  8 + 11) / 5 = 35 / 5 = 7
```

Centred points:

```
(−4, −4)   (−2, −1)   (0, 0)   (2, 1)   (4, 4)
```

**Step 2 — covariance matrix** (divisor `n − 1 = 4`).

```
Σ x²  = 16 + 4 + 0 + 4 + 16 = 40   →  var(x)  = 40 / 4 = 10.0
Σ y²  = 16 + 1 + 0 + 1 + 16 = 34   →  var(y)  = 34 / 4 =  8.5
Σ xy  = 16 + 2 + 0 + 2 + 16 = 36   →  cov(x,y)= 36 / 4 =  9.0

C = [ 10.0   9.0 ]
    [  9.0   8.5 ]
```

**Step 3 — eigenvalues.** For a 2×2 matrix, `λ² − (trace)λ + (det) = 0`.

```
trace = 10.0 + 8.5 = 18.5
det   = (10.0)(8.5) − (9.0)(9.0) = 85 − 81 = 4

λ = [ 18.5 ± √(18.5² − 4·4) ] / 2
  = [ 18.5 ± √(342.25 − 16) ] / 2
  = [ 18.5 ± √326.25 ] / 2
  = [ 18.5 ± 18.0623 ] / 2

λ₁ = (18.5 + 18.0623) / 2 = 18.2812
λ₂ = (18.5 − 18.0623) / 2 =  0.2188
```

**Step 4 — explained variance ratio.**

```
total variance = λ₁ + λ₂ = 18.5     (equals the trace — always true)

PC1: 18.2812 / 18.5 = 0.9882  →  98.82%
PC2:  0.2188 / 18.5 = 0.0118  →   1.18%
```

**One number replaces two, and you lose 1.18% of the spread.** That's what dimensionality reduction looks like when the features are strongly correlated — and study hours and sleep hours are.

**Step 5 — the first eigenvector.** Solve `(C − λ₁I)v = 0` using the top row:

```
(10.0 − 18.2812)·v_x + 9.0·v_y = 0
        −8.2812·v_x + 9.0·v_y = 0
                        v_y   = 0.92014 · v_x
```

Take `v = (1, 0.92014)` and normalise to length 1:

```
‖v‖ = √(1² + 0.92014²) = √(1 + 0.84666) = √1.84666 = 1.35892

PC1 = (1 / 1.35892 , 0.92014 / 1.35892) = (0.7359 , 0.6771)
```

Sanity check with the second row of the matrix equation:
`9.0(0.7359) + (8.5 − 18.2812)(0.6771) = 6.6231 − 6.6228 ≈ 0` ✓

PC2 must be perpendicular: **PC2 = (−0.6771, 0.7359)**.

(A note you will need when you check this in code: **the sign of an eigenvector is arbitrary.** `(0.7359, 0.6771)` and `(−0.7359, −0.6771)` describe the same axis, and different library versions will hand you either one. If your scores come out negated, nothing is wrong.)

**Interpret PC1.** Both entries are positive and roughly equal, so PC1 is essentially *"overall busyness"* — students high on this axis both study a lot **and** sleep a lot. PC2, with opposite signs, is *"studying at the expense of sleep."* Naming your components like this is a real skill and it's what makes a PCA plot readable.

**Step 6 — project one point.** Take the student at `(12, 11)`, centred to `(4, 4)`:

```
PC1 score = 4(0.7359) + 4(0.6771)  = 2.9436 + 2.7084  =  5.6520
PC2 score = 4(−0.6771) + 4(0.7359) = −2.7084 + 2.9436 =  0.2352
```

All five scores, by the same arithmetic:

| centred point | PC1 score | PC2 score |
|---|---:|---:|
| (−4, −4) | −5.6520 | −0.2352 |
| (−2, −1) | −2.1489 | +0.6183 |
| (0, 0) | 0.0000 | 0.0000 |
| (2, 1) | +2.1489 | −0.6183 |
| (4, 4) | +5.6520 | +0.2352 |

Check: the variance of the PC1 scores should equal λ₁.

```
Σ (PC1 score)² = 2(5.6520²) + 2(2.1489²) + 0 = 2(31.9451) + 2(4.6178) = 73.1258
variance       = 73.1258 / 4 = 18.281   = λ₁ = 18.281  ✓
```

Verify the whole thing in three lines:

```python
import numpy as np
from sklearn.decomposition import PCA
D = np.array([[4., 3.], [6., 6.], [8., 7.], [10., 8.], [12., 11.]])
p = PCA().fit(D)
print(np.round(p.components_, 4))
print(np.round(p.explained_variance_ratio_, 4))
print(np.round(p.transform(D), 4))
```

```
[[ 0.7359  0.6771]
 [-0.6771  0.7359]]
[0.9882 0.0118]
[[-5.652  -0.2351]
 [-2.1489  0.6183]
 [ 0.      0.    ]
 [ 2.1489 -0.6183]
 [ 5.652   0.2351]]
```

**Step 7 — reconstruct from PC1 only.**

```
centred_approx  = 5.6520 × (0.7359, 0.6771) = (4.1592, 3.8269)
original_approx = (4.1592 + 8, 3.8269 + 7)  = (12.159, 10.827)
```

The true point was `(12, 11)`. Reconstruction error:

```
√((12.159 − 12)² + (10.827 − 11)²) = √(0.02528 + 0.02993) = √0.05521 = 0.235
```

(`PCA(n_components=1).inverse_transform(...)` gives `[12.1592, 10.827]` — the same numbers.)

A 0.235-unit error on a point 5.65 units from the origin — about 4%. That is the price of throwing away PC2, made concrete.

---

## 💻 Hands-On

### Setup

```bash
pip install numpy pandas matplotlib scikit-learn
```

### Part A — verify the hand-computed k-means

```python
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

X = np.array([[1., 2.], [2., 1.], [2., 3.],
              [8., 8.], [9., 7.], [7., 9.]])

# init="random" with our exact starting centroids, n_init=1, so we reproduce the trace
init = np.array([[1., 2.], [2., 3.]])
km = KMeans(n_clusters=2, init=init, n_init=1, max_iter=300, random_state=0).fit(X)

print("labels        :", km.labels_)
print("centroids     :\n", np.round(km.cluster_centers_, 4))
print("inertia       :", round(km.inertia_, 4))
print("n_iter        :", km.n_iter_)
print("silhouette(C) :", round(silhouette_samples(X, km.labels_)[2], 4))
print("mean silhouette:", round(silhouette_score(X, km.labels_), 4))
```

Expected output:

```
labels        : [0 0 0 1 1 1]
centroids     :
 [[1.6667 2.    ]
 [8.     8.    ]]
inertia       : 6.6667
n_iter        : 3
silhouette(C) : 0.7838
mean silhouette: 0.8012
```

Centroids `(1.6667, 2.0)` and `(8, 8)`, inertia `6.6667`, `s(C) = 0.7838` — every number matches the hand trace exactly.

One thing to explain: sklearn reports `n_iter = 3` where we counted 2. Our iteration 3 was the pass that *confirmed* nothing changed, and sklearn counts that confirming pass. The algorithm did the same work; it just numbers it differently. Whenever a library's counter is one off from yours, check whether it's counting the check.

### Part B — the scaling demonstration

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

P = np.array([[25., 500000.],
              [55., 500000.],
              [25., 520000.]])

def sqdist(a, b):
    return float(np.sum((a - b) ** 2))

print("RAW")
print("  d(P1,P2)^2 =", sqdist(P[0], P[1]))
print("  d(P1,P3)^2 =", sqdist(P[0], P[2]))

Z = StandardScaler().fit_transform(P)
print("standardized:\n", np.round(Z, 4))
print("SCALED")
print("  d(P1,P2)^2 =", round(sqdist(Z[0], Z[1]), 4))
print("  d(P1,P3)^2 =", round(sqdist(Z[0], Z[2]), 4))
```

Expected output:

```
RAW
  d(P1,P2)^2 = 900.0
  d(P1,P3)^2 = 400000000.0
standardized:
 [[-0.7071 -0.7071]
 [ 1.4142 -0.7071]
 [-0.7071  1.4142]]
SCALED
  d(P1,P2)^2 = 4.5
  d(P1,P3)^2 = 4.5
```

Before scaling: a ratio of 444,444 to 1. After scaling: exactly equal. Same three data points.

### Part C — load the wine data and pretend the labels don't exist

`load_wine` has 178 bottles, 13 chemical measurements, and 3 true cultivars. We will **hide** the labels, cluster, and only peek at the truth at the very end — the way you'd validate a clustering method when you happen to have a labelled dataset to test it on.

```python
import numpy as np
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler

wine = load_wine()
X_raw = pd.DataFrame(wine.data, columns=wine.feature_names)
y_secret = wine.target                      # locked in a drawer until the end

print("shape:", X_raw.shape)
print(X_raw[["alcohol", "flavanoids", "color_intensity", "proline"]].describe().round(2))

scaler = StandardScaler()
X = scaler.fit_transform(X_raw)
print("after scaling — mean:", np.round(X.mean(axis=0)[:3], 6),
      " std:", np.round(X.std(axis=0)[:3], 6))
```

Expected output:

```
shape: (178, 13)
       alcohol  flavanoids  color_intensity  proline
count   178.00      178.00           178.00   178.00
mean     13.00        2.03             5.06   746.89
std       0.81        1.00             2.32   314.91
min      11.03        0.34             1.28   278.00
25%      12.36        1.21             3.22   500.50
50%      13.05        2.14             4.69   673.50
75%      13.68        2.88             6.20   985.00
max      14.83        5.08            13.00  1680.00
after scaling — mean: [ 0. -0. -0.]  std: [1. 1. 1.]
```

Look at the raw `std` column: `proline` has a standard deviation of 315 and `flavanoids` has 1.00. Unscaled, proline would be about 99% of every distance. This is not a hypothetical.

### Part D — elbow and silhouette

```python
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

ks = range(2, 11)
inertias, sils = [], []
for k in ks:
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    inertias.append(km.inertia_)
    sils.append(silhouette_score(X, km.labels_))

km1 = KMeans(n_clusters=1, n_init=1, random_state=42).fit(X)
print(f"{'k':>3} {'inertia':>10} {'drop':>8} {'silhouette':>11}")
print(f"{1:>3} {km1.inertia_:>10.1f} {'-':>8} {'-':>11}")
prev = km1.inertia_
for k, inr, s in zip(ks, inertias, sils):
    print(f"{k:>3} {inr:>10.1f} {prev-inr:>8.1f} {s:>11.4f}")
    prev = inr

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot([1] + list(ks), [km1.inertia_] + inertias, "o-")
ax[0].set_xlabel("k"); ax[0].set_ylabel("inertia"); ax[0].set_title("Elbow")
ax[1].plot(list(ks), sils, "o-", color="darkorange")
ax[1].set_xlabel("k"); ax[1].set_ylabel("mean silhouette"); ax[1].set_title("Silhouette")
plt.tight_layout(); plt.savefig("choose_k.png", dpi=110); plt.close()
print("saved choose_k.png")
```

Representative output:

```
  k    inertia     drop  silhouette
  1     2314.0        -           -
  2     1658.8    655.2      0.2593
  3     1277.9    380.8      0.2849
  4     1175.4    102.5      0.2602
  5     1109.5     65.9      0.2016
  6     1046.0     63.5      0.2372
  7      981.6     64.4      0.2036
  8      935.2     46.4      0.1570
  9      889.9     45.3      0.1499
 10      845.9     44.0      0.1436
saved choose_k.png
```

Read both columns together:

- **Elbow:** the drops are 655, then 381, then a cliff down to 103, then 66, 64, 64… The bend is at **k = 3** — that's the last big drop before the curve flattens into a steady trickle.
- **Silhouette:** peaks at **k = 3** with 0.2849, then declines (with a small bump at k = 6 that is noise, not structure — it does not exceed the k = 3 value).

Both say 3. That agreement is the evidence you cite. Note also that 0.285 is a *modest* silhouette — the clusters are real but they touch. Report that honestly; don't call it "well-separated."

### Part E — cluster and profile

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples

K = 3
km = KMeans(n_clusters=K, n_init=10, random_state=42).fit(X)
labels = km.labels_

sizes = np.bincount(labels)
sil_each = silhouette_samples(X, labels)
print("cluster sizes:", sizes)
for c in range(K):
    print(f"  cluster {c}: n={sizes[c]:3d}  mean silhouette={sil_each[labels==c].mean():.4f}")

# Profile in ORIGINAL units — that's what a human can name
profile = X_raw.copy()
profile["cluster"] = labels
means = profile.groupby("cluster").mean().T
means["overall"] = X_raw.mean()
print("\nfeature means by cluster (original units):")
print(means.round(2))
```

Representative output:

```
cluster sizes: [65 51 62]
  cluster 0: n= 65  mean silhouette=0.1774
  cluster 1: n= 51  mean silhouette=0.3506
  cluster 2: n= 62  mean silhouette=0.3434

feature means by cluster (original units):
cluster                          0       1        2  overall
alcohol                      12.25   13.13    13.68    13.00
malic_acid                    1.90    3.31     2.00     2.34
ash                           2.23    2.42     2.47     2.37
alcalinity_of_ash            20.06   21.24    17.46    19.49
magnesium                    92.74   98.67   107.97    99.74
total_phenols                 2.25    1.68     2.85     2.30
flavanoids                    2.05    0.82     3.00     2.03
nonflavanoid_phenols          0.36    0.45     0.29     0.36
proanthocyanins               1.62    1.15     1.92     1.59
color_intensity               2.97    7.23     5.45     5.06
hue                           1.06    0.69     1.07     0.96
od280/od315_of_diluted_wines  2.80    1.70     3.16     2.61
proline                     510.17  619.06  1100.23   746.89
```

Now **name them from the numbers**, which is the actual deliverable:

| Cluster | n | Distinctive features | Human name |
|---:|---:|---|---|
| 2 | 62 | highest alcohol (13.68 vs 13.00), highest flavanoids (3.00 vs 2.03), highest proline (1100 vs 747), highest phenols (2.85), highest magnesium (108) | **Bold Reserve** — rich, full-bodied, high-extract |
| 1 | 51 | lowest flavanoids (0.82), highest colour intensity (7.23 vs 5.06), lowest hue (0.69), highest malic acid (3.31) | **Dark & Tannic** — deeply coloured, sharp, low in soft phenolics |
| 0 | 65 | lowest alcohol (12.25), lowest colour intensity (2.97 vs 5.06), lowest magnesium (93), lowest proline (510), mid flavanoids | **Light & Pale** — thin-bodied and lightly coloured |

And the honest note: **cluster 0 is by far the weakest** — mean silhouette **0.1774**, half of cluster 1's 0.3506. Look at its profile and you'll see why: apart from being *low* on colour intensity and proline, it is unremarkable on almost everything, and "low on things" is a much weaker basis for a group than "high on a specific thing." State that; don't hide it. A cluster defined mainly by absence is often a sign that k is too small, or that the real structure is two strong groups plus a continuum of leftovers.

### Part F — check against the hidden labels

Because this dataset *does* have ground truth, we can grade our clustering — a luxury you will not have on real unlabelled data.

```python
from sklearn.metrics import adjusted_rand_score, confusion_matrix

print("adjusted Rand index vs true cultivar:", round(adjusted_rand_score(y_secret, labels), 4))
print("\ncontingency table (rows=true cultivar, cols=cluster):")
print(confusion_matrix(y_secret, labels))
```

Representative output:

```
adjusted Rand index vs true cultivar: 0.8975

contingency table (rows=true cultivar, cols=cluster):
[[ 0  0 59]
 [ 65  3  3]
 [ 0 48  0]]
```

> **Adjusted Rand index (ARI):** agreement between two labellings, corrected for chance. 1.0 = identical grouping, 0.0 = no better than random.

ARI 0.90, with only 6 of 178 bottles misplaced. k-means, given no labels whatsoever, recovered the three real cultivars almost perfectly. Note the cluster numbers don't match the cultivar numbers — cluster 2 is cultivar 0, cluster 0 is cultivar 1, cluster 1 is cultivar 2. **Cluster IDs are arbitrary names**; only the grouping means anything.

### Part G — PCA on the wine data

```python
from sklearn.decomposition import PCA

pca_full = PCA().fit(X)
evr = pca_full.explained_variance_ratio_
print("explained variance ratio per component:")
for i, v in enumerate(evr, start=1):
    print(f"  PC{i:2d}: {v:.4f}   cumulative {evr[:i].sum():.4f}")
```

Representative output:

```
explained variance ratio per component:
  PC 1: 0.3620   cumulative 0.3620
  PC 2: 0.1921   cumulative 0.5541
  PC 3: 0.1112   cumulative 0.6653
  PC 4: 0.0707   cumulative 0.7360
  PC 5: 0.0656   cumulative 0.8016
  PC 6: 0.0494   cumulative 0.8510
  PC 7: 0.0424   cumulative 0.8934
  PC 8: 0.0268   cumulative 0.9202
  PC 9: 0.0222   cumulative 0.9424
  PC10: 0.0193   cumulative 0.9617
  PC11: 0.0174   cumulative 0.9791
  PC12: 0.0130   cumulative 0.9920
  PC13: 0.0080   cumulative 1.0000
```

Two numbers to say out loud: **PC1 + PC2 = 55.4%** of the variance in just two dimensions, and **8 components carry 92%** of the information in 13. That's what "the features are correlated" looks like numerically.

Now the plot, coloured by cluster:

```python
import matplotlib.pyplot as plt

pca2 = PCA(n_components=2)
Z2 = pca2.fit_transform(X)

plt.figure(figsize=(7, 6))
names = {0: "Light & Everyday", 1: "Dark & Tannic", 2: "Bold Reserve"}
for c in range(K):
    m = labels == c
    plt.scatter(Z2[m, 0], Z2[m, 1], s=35, alpha=0.8, label=f"{c}: {names[c]}")
cen2 = pca2.transform(km.cluster_centers_)
plt.scatter(cen2[:, 0], cen2[:, 1], marker="X", s=250, c="black", label="centroids")
plt.xlabel(f"PC1 ({evr[0]*100:.1f}% var)")
plt.ylabel(f"PC2 ({evr[1]*100:.1f}% var)")
plt.title("Wine clusters projected to 2-D")
plt.legend(); plt.tight_layout(); plt.savefig("wine_pca.png", dpi=110); plt.close()
print("saved wine_pca.png")
```

Which features drive PC1?

```python
loadings = pd.Series(pca2.components_[0], index=wine.feature_names)
print("PC1 loadings, largest magnitude first:")
print(loadings.reindex(loadings.abs().sort_values(ascending=False).index).round(3).head(6))
```

Representative output:

```
PC1 loadings, largest magnitude first:
flavanoids                      0.423
total_phenols                   0.395
od280/od315_of_diluted_wines    0.376
proanthocyanins                 0.313
nonflavanoid_phenols           -0.299
hue                             0.297
```

PC1 is dominated by the **phenolic compounds**, all pulling the same way (except `nonflavanoid_phenols`, which is negative and therefore anti-correlated with the rest). So PC1 is fairly read as *"total phenolic richness."* Naming a component from its loadings turns an anonymous axis into something you can put on a slide.

### Part H — reconstruction error

```python
from sklearn.decomposition import PCA
import numpy as np

print(f"{'m':>3} {'cum. var':>9} {'mean recon. error':>18}")
for m in [1, 2, 3, 5, 8, 13]:
    p = PCA(n_components=m).fit(X)
    X_hat = p.inverse_transform(p.transform(X))
    err = np.sqrt(((X - X_hat) ** 2).sum(axis=1)).mean()
    print(f"{m:>3} {p.explained_variance_ratio_.sum():>9.4f} {err:>18.4f}")
```

Representative output:

```
  m  cum. var  mean recon. error
  1    0.3620             2.7527
  2    0.5541             2.2550
  3    0.6653             1.9581
  5    0.8016             1.5303
  8    0.9202             0.9599
 13    1.0000             0.0000
```

Reconstruction error is the honest counterpart to explained variance. Two components keep 55% of the variance and cost you an average distortion of 2.26 units per bottle (in standardized space, where the typical point is about √13 ≈ 3.6 from the origin). Thirteen components reconstruct perfectly, because you threw nothing away. **Explained variance is the optimistic framing; reconstruction error is the bill.**

### Part I — clusters and components as supervised features

```python
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

baseline = Pipeline([("sc", StandardScaler()),
                     ("clf", LogisticRegression(max_iter=5000))])

pca_pipe = Pipeline([("sc", StandardScaler()),
                     ("pca", PCA(n_components=2)),
                     ("clf", LogisticRegression(max_iter=5000))])

# KMeans.transform() returns distance-to-each-centroid: 3 numeric columns
km_pipe = Pipeline([("sc", StandardScaler()),
                    ("km", KMeans(n_clusters=3, n_init=10, random_state=0)),
                    ("clf", LogisticRegression(max_iter=5000))])

for name, pipe in [("raw 13 features", baseline),
                   ("PCA -> 2 comps", pca_pipe),
                   ("kmeans distances (3)", km_pipe)]:
    s = cross_val_score(pipe, X_raw, y_secret, cv=cv, scoring="accuracy")
    print(f"{name:22s} acc = {s.mean():.4f} +/- {s.std():.4f}   ({s.shape[0]} folds)")
```

Representative output (you may see a `FutureWarning` about `n_init`; scikit-learn versions differ in their default and it does not affect the result):

```
raw 13 features        acc = 0.9832 +/- 0.0137   (5 folds)
PCA -> 2 comps         acc = 0.9606 +/- 0.0139   (5 folds)
kmeans distances (3)   acc = 0.9775 +/- 0.0209   (5 folds)
```

Read it as: compressing 13 features into 2 principal components costs about **2.3 accuracy points** (0.9832 → 0.9606) and reduces the model to 6 coefficients instead of 39. Compressing them into 3 centroid distances costs only **0.6 points**, and that gap is smaller than the k-means pipeline's own fold-to-fold spread of 0.0209 — so on this dataset three numbers produced *without ever looking at* `y` are statistically indistinguishable from all thirteen original features. That is a genuinely striking result, and it happens because k-means already recovered the cultivars almost perfectly (ARI 0.90). On this small clean dataset neither compression is worth the loss of interpretability; on a 5,000-feature dataset with 300 rows either would be an excellent trade.

The critical structural point is the `Pipeline`. Because `PCA` and `KMeans` sit *inside* it, `cross_val_score` refits them on each training fold. Fit them once on all of `X_raw` before cross-validating and you leak test-fold geometry into your features — the exact preprocessing-leakage bug from Module 2, wearing an unsupervised costume.

---

## ✍️ Practice

### 1. [Warm-up] k-means by hand, one full iteration

Five points: `A=(0,0)`, `B=(1,0)`, `C=(0,1)`, `D=(6,6)`, `E=(6,5)`. Starting centroids `μ₁=(0,0)`, `μ₂=(1,0)`, with `k=2`.

(a) Do the assign step: build a table of squared distances from every point to both centroids and give the assignments.
(b) Do the move step: compute the two new centroids.
(c) Do a second assign step and say which point (if any) switched.
(d) Compute the inertia after the second move step.

**Done looks like:** two distance tables with all arithmetic shown, the centroids after each move, the name of the switching point, and a final inertia number.

### 2. [Warm-up] Silhouette by hand

Using your converged clusters from Exercise 1 (`C1 = {A, B, C}`, `C2 = {D, E}`), compute the silhouette score of point **B = (1, 0)** by hand.

(a) Compute `a(B)` — mean Euclidean distance to the other members of C1.
(b) Compute `b(B)` — mean Euclidean distance to every member of C2.
(c) Compute `s(B) = (b − a) / max(a, b)`.
(d) Verify with `sklearn.metrics.silhouette_samples`.

**Done looks like:** every square root written out to 4 decimals, and a value matching sklearn to 4 decimals.

### 3. [Build] Do the elbow and the silhouette agree?

Generate a dataset where you know the truth, then see whether the diagnostics find it.

```python
from sklearn.datasets import make_blobs
X4, _ = make_blobs(n_samples=600, centers=4, cluster_std=1.2,
                   n_features=2, random_state=7)
```

(a) Compute inertia and mean silhouette for `k = 2 … 9` and print them as a table with a "drop in inertia" column.
(b) Which `k` does the elbow suggest? Which does the silhouette suggest?
(c) Repeat the whole thing with `cluster_std=3.0` (much blobbier, heavily overlapping). Do the two diagnostics still agree?
(d) Write two sentences on what the `cluster_std=3.0` case teaches you about trusting the elbow.

**Done looks like:** two tables, two saved plots, and a stated answer for each of (b), (c), (d).

### 4. [Build] PCA on iris — variance, projection, reconstruction

Use `sklearn.datasets.load_iris` (150 samples, 4 features).

(a) Standardize, fit a full `PCA`, and print the explained-variance ratio and cumulative sum for all 4 components.
(b) How many components do you need for ≥ 95% cumulative variance?
(c) Project to 2-D and save a scatter plot coloured by the true species.
(d) Compute the mean reconstruction error for `m = 1, 2, 3, 4` and present it as a table alongside cumulative variance.
(e) Print PC1's loadings and name the component in plain English.

**Done looks like:** the variance table, the answer to (b) as a single integer, a saved PNG, the reconstruction table, and a one-sentence name for PC1.

### 5. [Stretch] Reproduce the curse of dimensionality

Write a script that, for `d` in `[2, 5, 10, 20, 50, 100, 200, 500, 1000]`:

- draws 200 points uniformly at random from the `d`-dimensional unit cube,
- computes all pairwise Euclidean distances,
- reports the minimum, the maximum, the mean, and the contrast ratio `(max − min) / min`.

(a) Print the table.
(b) Plot the contrast ratio against `d` on a log-x axis and save it.
(c) At what `d` does the contrast ratio first fall below 1.0, and what does that mean in plain English?
(d) Explain in three sentences why this makes k-means unreliable in high dimensions, and name the two things you can do about it.

**Done looks like:** the table, the saved plot, the threshold `d`, and the three-sentence explanation.

### 6. [Stretch] Do cluster features actually help?

On the **breast cancer** dataset (`sklearn.datasets.load_breast_cancer`, 569 rows, 30 features, binary target), test whether unsupervised features earn their keep.

Build four pipelines and compare with 5-fold stratified cross-validation on **ROC-AUC** (Module 3's metric):

1. `StandardScaler` → `LogisticRegression`
2. `StandardScaler` → `PCA(n_components=5)` → `LogisticRegression`
3. `StandardScaler` → `KMeans(n_clusters=4)` (distance features) → `LogisticRegression`
4. `StandardScaler` → `FeatureUnion` of passthrough + `KMeans(n_clusters=4)` → `LogisticRegression`

(a) Report mean ± std AUC for all four.
(b) State which wins and whether the difference exceeds one standard deviation.
(c) Explain precisely why every transformer must be inside the `Pipeline` and what number you would have got if you'd fitted the `PCA` on all 569 rows first.

**Done looks like:** a four-row table with error bars, a stated winner with a "is this difference real?" judgement, and the leakage explanation.

---

## 🤔 Think Deeper

**1. You just named three clusters "Bold Reserve," "Dark & Tannic," and "Light & Everyday." What did that naming do?**
It made the output usable. It also froze a fuzzy statistical boundary into a label that people will now treat as a fact about the world. If those clusters were customers rather than wines, someone in marketing would start describing real people as "the Light & Everyday segment," would design products for that segment, and within a year the segment would exist because you named it.
*How to reason about it:* separate the descriptive claim ("these 65 rows have similar feature values") from the essentialist claim ("these are a kind of thing"). Ask what would change if you re-ran with k=4 — would the name survive? Then ask what the cost is of being wrong about a person versus a bottle of wine. Clustering people and clustering objects are not the same activity, whatever the code says.

**2. Every point gets a cluster, including the ones that don't belong anywhere.**
k-means has no "none of the above." A weird outlier — the one bottle produced by a bankrupt vineyard in a bad year — gets assigned to whichever centroid is least wrong, and then *drags that centroid toward itself*. A single extreme point can visibly move a cluster's centre and change other points' assignments.
*How to reason about it:* look at the silhouette distribution, not just the mean — how many points have `s < 0`? Those are points the algorithm is unsure about, and in a real deployment you might route them to a human instead of acting on them. Then ask whether an "unassigned" outcome is even allowed by whatever system consumes your clusters, and if not, whether that system is safe.

**3. PCA never sees your target, so it can throw away exactly the thing you needed.**
Imagine a medical dataset where 95% of the variance is patient height and weight, and the diagnostic signal lives in a tiny, low-variance blood-test ratio. PCA to 2 components will keep the body-size axis and discard the diagnosis. Explained variance is a measure of *spread*, not of *usefulness*.
*How to reason about it:* the test is empirical, not philosophical — cross-validate with and without PCA and compare the target metric. But also ask the design question: if you already know which features matter, why are you using an unsupervised method to select them? PCA's real home is when you have far more features than rows, or when features are so correlated that a supervised model can't get a stable answer.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Running k-means on unscaled features | Nothing errors, and you get clusters — they're just clusters of the largest-range column | Always `StandardScaler` first. Print the raw `std` per column and see which one would dominate |
| Picking `k` by minimising inertia | Inertia falls monotonically, so the "best" is always `k = n` | Look for the *bend*, and cross-check with silhouette. Never optimise inertia directly |
| Treating cluster numbers as meaningful | Cluster 0 in one run is cluster 2 in the next; the integers are arbitrary labels | Compare *groupings* (ARI, contingency tables), never the raw IDs. Re-run with a new seed and confirm your interpretation survives |
| Fitting `PCA`/`KMeans` on the full dataset before splitting | It feels like "preprocessing," not "modelling" | Both learn parameters from data, so both leak. Put them in a `Pipeline` and let cross-validation refit them per fold |
| Forgetting to standardize before PCA | PCA maximises variance, so the feature measured in the largest units becomes PC1 | Standardize unless every feature is already in the same natural unit and you *want* the scale to matter |
| Reading a 2-D PCA plot as the whole truth | The picture is convincing and it's right there on your screen | Always print the explained variance ratio next to the plot. If PC1+PC2 = 55%, you are looking at just over half the story and points that look adjacent may be far apart in the other 45% |
| Claiming clusters are "well-separated" at silhouette 0.28 | You wanted a clean result and 0.28 was the biggest number in the column | State the value and use the field guide: 0.28 is "real but overlapping." Being honest about weak structure is a finding, not a failure |
| Assuming the elbow always exists | Tutorials always show a clean bend | On real data the inertia curve is frequently a smooth arc with no elbow at all. When it is, say so and lean on silhouette plus domain constraints |
| Using k-means on non-spherical clusters (rings, crescents, stripes) | It's the algorithm you know | Plot the data first. If the shapes are elongated or nested, k-means will slice them wrongly — that's a limitation of the method, not a tuning problem |

---

## 🛠️ Mini-Project — Cluster Cartography

**Goal.** Take an unlabelled dataset, find its structure, justify the number of clusters with two independent kinds of evidence, draw a readable map of it, and hand a human being a set of named groups they could actually act on.

Use `load_wine` with the target hidden (as in Part C), **or** `load_breast_cancer` with the target hidden, **or** any tabular dataset of your own with ≥ 6 numeric features and ≥ 150 rows.

**Starter steps.**

1. **Audit and scale.** Print shape, dtypes, missing values, and per-column mean/std. Standardize. Write one sentence naming which column would have dominated distances if you hadn't scaled, with its raw std as evidence.
2. **Sweep k.** For `k = 2 … 10`, record inertia and mean silhouette. Print the table with an inertia-drop column. Save a two-panel figure (elbow, silhouette).
3. **Choose k and defend it.** Write a short paragraph citing both diagnostics *and* a domain consideration. If they disagree, say which you trusted and why — a defended disagreement scores higher than a lucky agreement.
4. **Check stability.** Re-run your chosen `k` with five different `random_state` values, and separately on five random 80% subsamples. Report the ARI between each run's labelling and your reference run. If the mean ARI is below about 0.7, your structure is fragile and you must say so.
5. **Profile.** Build the cluster × feature mean table **in original units** (never in z-scores — nobody can read "alcohol = 0.83"). Add an "overall mean" column so readers can see what's distinctive.
6. **Name.** Give each cluster a short human name derived from the two or three features where it deviates most from the overall mean. One sentence of justification per name.
7. **Map.** Fit `PCA(n_components=2)` on the scaled data, scatter-plot it coloured by cluster, mark the centroids, and put the explained-variance percentage on each axis label. Print PC1's and PC2's top loadings and name both axes.
8. **Be honest.** Report the per-cluster mean silhouette, identify the weakest cluster, and write 100–150 words on why it's weak and what you'd do about it.

**Success criteria checklist.**

- [ ] Data is standardized, with one sentence of evidence for why that mattered here.
- [ ] An elbow table/plot and a silhouette table/plot, both covering `k = 2 … 10`.
- [ ] A written defence of the chosen `k` citing both diagnostics and one domain constraint.
- [ ] A stability check across ≥ 5 seeds and ≥ 5 subsamples, reported as mean ARI.
- [ ] A cluster × feature mean table in **original units** with an overall-mean column.
- [ ] Every cluster has a human name and a one-sentence justification pointing at specific numbers.
- [ ] A 2-D PCA scatter with centroids marked and explained-variance percentages in the axis labels.
- [ ] PC1 and PC2 each named from their loadings.
- [ ] Per-cluster silhouettes reported, weakest cluster identified, 100–150 word honest note.

**Level it up.** Add a **negative control**. Generate a dataset with genuinely no cluster structure — `np.random.default_rng(0).normal(size=(178, 13))` — and run your entire pipeline on it unchanged. k-means will still return three clusters, the profile table will still show differences, and you will still be able to think of names for them. Report the silhouette score and stability ARI for the noise data next to your real results. Then write three sentences on what that comparison tells you about how much of your "finding" is method and how much is data. Every clustering write-up should have this, and almost none do.

---

## 🔑 Key Takeaways

- Unsupervised learning has no answer key, so the deliverable is not a score — it's an argument backed by internal quality (silhouette), stability (re-run agreement), and interpretability (named clusters).
- k-means is four lines: assign to nearest centroid, move centroid to the mean, repeat, stop. It always converges, but only to a local minimum, which is why `k-means++` and multiple restarts exist.
- Distance means nothing without scaling. Two points went from "444,444× more similar" to "exactly equally similar" on the same data purely by standardizing.
- Choose `k` with the elbow *and* the silhouette, and let domain constraints break ties. Inertia alone can never choose, because it always falls.
- PCA rotates to new axes ordered by variance. Explained variance is the optimistic number; reconstruction error is the bill. Report both.
- PCA has never seen your target, so it can discard the signal you need. Cross-validate with and without it instead of assuming.
- `KMeans` and `PCA` both learn from data, so they leak like any other fitted transform. They belong inside a `Pipeline`.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Unsupervised learning** | Finding patterns when nobody gave you the right answers | Sorting 500 mixed Lego bricks with no instructions |
| **Cluster** | A group of points more like each other than like anything outside the group | The 62 "Bold Reserve" wines |
| **Centroid** | The average position of everything in a cluster | (1.6667, 2.0) for `{A, B, C}` |
| **Inertia (WCSS)** | Total squared distance from every point to its own centroid — smaller is tighter | 6.6667 in the worked example |
| **Elbow method** | Plot inertia vs k and look for where the curve stops dropping fast | The bend at k = 3 for wine |
| **Silhouette score** | −1 to +1: how much closer a point is to its own cluster than to the next one | s(C) = 0.78 means C is firmly placed |
| **k-means++** | A smarter way to pick starting centroids so they don't all land in one blob | scikit-learn's default `init` |
| **Curse of dimensionality** | With many features, everything ends up about equally far from everything | At d = 1000 the farthest point is only 20% farther than the nearest |
| **Principal component** | A new axis chosen to point along the data's biggest spread | PC1 for wine = "total phenolic richness" |
| **Explained variance ratio** | The share of total spread that one component captures | PC1 = 36.2% of wine's variance |
| **Loading** | How much an original feature contributes to a principal component | `flavanoids` loads 0.423 on wine's PC1 |
| **Reconstruction error** | How far off you are when you rebuild the data from a few components | 2.38 average units with 2 components |
| **Adjusted Rand index (ARI)** | Agreement between two groupings, corrected for chance; 1.0 = identical | 0.90 between k-means clusters and true cultivars |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1. [Warm-up] k-means by hand

Points: `A=(0,0)`, `B=(1,0)`, `C=(0,1)`, `D=(6,6)`, `E=(6,5)`. Start: `μ₁=(0,0)`, `μ₂=(1,0)`.

**(a) Assign step 1** (squared Euclidean):

| point | d² to μ₁ = (0,0) | d² to μ₂ = (1,0) | winner |
|---|---|---|---|
| A (0,0) | 0 + 0 = **0** | (0−1)² + 0 = 1 | **C1** |
| B (1,0) | 1 + 0 = 1 | 0 + 0 = **0** | **C2** |
| C (0,1) | 0 + 1 = **1** | 1 + 1 = 2 | **C1** |
| D (6,6) | 36 + 36 = 72 | 25 + 36 = **61** | **C2** |
| E (6,5) | 36 + 25 = 61 | 25 + 25 = **50** | **C2** |

C1 = {A, C}, C2 = {B, D, E}.

**(b) Move step 1**

```
μ₁ = ( (0+0)/2 , (0+1)/2 ) = ( 0 , 0.5 )
μ₂ = ( (1+6+6)/3 , (0+6+5)/3 ) = ( 13/3 , 11/3 ) = ( 4.3333 , 3.6667 )
```

**(c) Assign step 2**

| point | d² to μ₁ = (0, 0.5) | d² to μ₂ = (4.3333, 3.6667) | winner |
|---|---|---|---|
| A (0,0) | 0 + 0.25 = **0.25** | 18.7775 + 13.4447 = 32.2222 | **C1** |
| B (1,0) | 1 + 0.25 = **1.25** | 11.1109 + 13.4447 = 24.5556 | **C1** ← switched |
| C (0,1) | 0 + 0.25 = **0.25** | 18.7775 + 7.1113 = 25.8888 | **C1** |
| D (6,6) | 36 + 30.25 = 66.25 | 2.7779 + 5.4447 = **8.2226** | **C2** |
| E (6,5) | 36 + 20.25 = 56.25 | 2.7779 + 1.7779 = **4.5558** | **C2** |

**Point B switched** from C2 to C1. C1 = {A, B, C}, C2 = {D, E}.

**Move step 2**

```
μ₁ = ( (0+1+0)/3 , (0+0+1)/3 ) = ( 1/3 , 1/3 ) = ( 0.3333 , 0.3333 )
μ₂ = ( (6+6)/2 , (6+5)/2 )     = ( 6 , 5.5 )
```

**(d) Inertia**

```
Cluster 1, centroid (0.3333, 0.3333):
  A (0,0): (0.3333)² + (0.3333)² = 0.1111 + 0.1111 = 0.2222
  B (1,0): (0.6667)² + (0.3333)² = 0.4444 + 0.1111 = 0.5556
  C (0,1): (0.3333)² + (0.6667)² = 0.1111 + 0.4444 = 0.5556
                                             sum   = 1.3333

Cluster 2, centroid (6, 5.5):
  D (6,6): 0 + (0.5)² = 0.25
  E (6,5): 0 + (0.5)² = 0.25
                sum   = 0.50

TOTAL INERTIA = 1.3333 + 0.50 = 1.8333
```

```python
import numpy as np
from sklearn.cluster import KMeans
X = np.array([[0.,0.],[1.,0.],[0.,1.],[6.,6.],[6.,5.]])
km = KMeans(2, init=np.array([[0.,0.],[1.,0.]]), n_init=1, random_state=0).fit(X)
print(km.labels_, np.round(km.cluster_centers_, 4), round(km.inertia_, 4), km.n_iter_)
```

```
[0 0 0 1 1] [[0.3333 0.3333]
 [6.     5.5   ]] 1.8333 3
```

(As in the worked example, sklearn's `n_iter_` of 3 counts the confirming pass; we counted the 2 passes that changed something.)

### 2. [Warm-up] Silhouette by hand for B = (1, 0)

Clusters: C1 = {A(0,0), B(1,0), C(0,1)}, C2 = {D(6,6), E(6,5)}.

**(a)**
```
d(B,A) = √((1−0)² + (0−0)²) = √1 = 1.0000
d(B,C) = √((1−0)² + (0−1)²) = √2 = 1.4142
a(B)   = (1.0000 + 1.4142) / 2  = 1.2071
```

**(b)**
```
d(B,D) = √((1−6)² + (0−6)²) = √(25 + 36) = √61 = 7.8102
d(B,E) = √((1−6)² + (0−5)²) = √(25 + 25) = √50 = 7.0711
b(B)   = (7.8102 + 7.0711) / 2                 = 7.4407
```

**(c)**
```
s(B) = (7.4407 − 1.2071) / max(1.2071, 7.4407)
     = 6.2336 / 7.4407
     = 0.8378
```

**(d)**
```python
from sklearn.metrics import silhouette_samples
labels = np.array([0, 0, 0, 1, 1])
print(round(silhouette_samples(X, labels)[1], 4))
```

```
0.8378
```

Matches to 4 decimals. B scores higher than C did in the worked example (0.84 vs 0.78) because B sits nearer its own cluster's centre relative to how far C2 is.

### 3. [Build] Do the elbow and the silhouette agree?

```python
import numpy as np, matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def sweep(X, tag):
    prev = KMeans(1, n_init=1, random_state=0).fit(X).inertia_
    print(f"\n--- {tag} ---")
    print(f"{'k':>3} {'inertia':>10} {'drop':>9} {'silhouette':>11}")
    inr_list, sil_list, ks = [], [], list(range(2, 10))
    for k in ks:
        km = KMeans(k, n_init=10, random_state=0).fit(X)
        s = silhouette_score(X, km.labels_)
        print(f"{k:>3} {km.inertia_:>10.1f} {prev-km.inertia_:>9.1f} {s:>11.4f}")
        inr_list.append(km.inertia_); sil_list.append(s); prev = km.inertia_
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].plot(ks, inr_list, "o-"); ax[0].set_title(f"elbow — {tag}"); ax[0].set_xlabel("k")
    ax[1].plot(ks, sil_list, "o-", color="darkorange"); ax[1].set_title(f"silhouette — {tag}")
    ax[1].set_xlabel("k")
    plt.tight_layout(); plt.savefig(f"ex3_{tag}.png", dpi=110); plt.close()
    return ks, inr_list, sil_list

Xa, _ = make_blobs(n_samples=600, centers=4, cluster_std=1.2, n_features=2, random_state=7)
Xb, _ = make_blobs(n_samples=600, centers=4, cluster_std=3.0, n_features=2, random_state=7)
sweep(Xa, "std1.2")
sweep(Xb, "std3.0")
```

Representative output:

```
--- std1.2 ---   (k=1 inertia = 45007.5)
  k    inertia      drop  silhouette
  2    18823.4   26184.1      0.5743
  3     5754.9   13068.5      0.7403
  4     1623.5    4131.4      0.7724
  5     1468.8     154.7      0.6477
  6     1321.9     146.9      0.5305
  7     1169.5     152.4      0.4304
  8     1056.1     113.4      0.3289
  9      931.3     124.8      0.3484

--- std3.0 ---   (k=1 inertia = 53725.8)
  k    inertia      drop  silhouette
  2    25996.3   27729.5      0.4698
  3    13096.1   12900.2      0.5438
  4     9149.7    3946.5      0.4829
  5     7979.6    1170.1      0.4109
  6     6974.0    1005.6      0.3699
  7     6110.3     863.8      0.3468
  8     5352.7     757.6      0.3469
  9     4717.7     635.0      0.3544
```

**(b)** With `cluster_std=1.2` the answer is unambiguous. The elbow is a cliff at **k = 4**: inertia drops 4,131 going 3→4 and only 155 going 4→5, a **27-fold** collapse. The silhouette also peaks at **k = 4** (0.7724). Both diagnostics agree, both are right, and you'd be confident.

**(c)** With `cluster_std=3.0` they **disagree**. The elbow still points at **k = 4** — the 3→4 drop of 3,946 is 3.4× the 4→5 drop of 1,170 — but that ratio has fallen from 27× to 3.4×, so the bend is far softer and a reasonable person could read the curve as k=3 or k=5. Meanwhile the silhouette now peaks at **k = 3** (0.5438 versus 0.4829 at k=4), which is the **wrong** answer: the data genuinely has 4 centres.

Why did silhouette break? When clusters overlap, points near a boundary have `a` (distance to own cluster) almost equal to `b` (distance to the nearest other cluster), so their individual scores collapse toward 0 and drag the mean down. Merging two adjacent overlapping blobs into one bigger cluster *removes* that boundary and its low-scoring points, so the average goes **up**. Silhouette therefore has a systematic bias toward fewer, fatter clusters exactly when clusters touch.

**(d)** Two things to take away. First, the elbow's *sharpness* is the real signal, not its location — a 27× drop ratio is a finding and a 3.4× drop ratio is a suggestion, and you should report the ratio rather than pointing at a picture. Second, the two diagnostics fail in different directions, so a disagreement is informative: silhouette pulling lower than the elbow is a signature of overlapping clusters, which is itself worth writing in your report. Neither tool is a decision procedure, and when they diverge you must reach for stability checks and domain knowledge rather than picking whichever one flatters your hypothesis.

### 4. [Build] PCA on iris

```python
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

iris = load_iris()
X = StandardScaler().fit_transform(iris.data)

p_full = PCA().fit(X)
evr = p_full.explained_variance_ratio_
print(f"{'PC':>3} {'evr':>8} {'cumulative':>11}")
for i, v in enumerate(evr, 1):
    print(f"{i:>3} {v:>8.4f} {evr[:i].sum():>11.4f}")
```

**(a)**
```
 PC      evr  cumulative
  1   0.7296      0.7296
  2   0.2285      0.9581
  3   0.0367      0.9948
  4   0.0052      1.0000
```


**(b)** **2 components** — cumulative variance reaches 0.9581 at PC2, already above 0.95.

**(c)**
```python
Z = PCA(n_components=2).fit_transform(X)
plt.figure(figsize=(7, 5))
for c, name in enumerate(iris.target_names):
    m = iris.target == c
    plt.scatter(Z[m, 0], Z[m, 1], label=name, s=32, alpha=0.85)
plt.xlabel(f"PC1 ({evr[0]*100:.1f}%)"); plt.ylabel(f"PC2 ({evr[1]*100:.1f}%)")
plt.legend(); plt.title("Iris in 2 principal components")
plt.tight_layout(); plt.savefig("iris_pca.png", dpi=110); plt.close()
print("saved iris_pca.png")
```

The plot shows *setosa* completely separated on the left, with *versicolor* and *virginica* adjacent and slightly overlapping on the right — which is exactly the difficulty pattern every iris classifier shows.

**(d)**
```python
print(f"{'m':>3} {'cum. var':>9} {'mean recon. error':>18}")
for m in [1, 2, 3, 4]:
    p = PCA(n_components=m).fit(X)
    Xh = p.inverse_transform(p.transform(X))
    err = np.sqrt(((X - Xh) ** 2).sum(axis=1)).mean()
    print(f"{m:>3} {p.explained_variance_ratio_.sum():>9.4f} {err:>18.4f}")
```

```
  m  cum. var  mean recon. error
  1    0.7296             0.8817
  2    0.9581             0.3420
  3    0.9948             0.1092
  4    1.0000             0.0000
```

Going from 1 to 2 components cuts the reconstruction error by **61%** (0.8817 → 0.3420); going from 2 to 3 cuts it by another **68%** (0.3420 → 0.1092) while adding only 3.7 percentage points of cumulative variance. The two views tell slightly different stories — variance says "stop at 2," error says "3 is meaningfully tighter" — which is exactly why you report both rather than picking the one that agrees with you.

**(e)**
```python
p2 = PCA(n_components=2).fit(X)
print(pd.Series(p2.components_[0], index=iris.feature_names).round(3))
```

```
sepal length (cm)    0.521
sepal width (cm)    -0.269
petal length (cm)    0.580
petal width (cm)     0.565
```

**Name for PC1: "overall flower size, driven by the petals."** Three of the four loadings are large and positive, with the two petal measurements strongest; sepal width is the odd one out with a modest negative loading, meaning bigger flowers here tend to have proportionally *narrower* sepals.

### 5. [Stretch] Curse of dimensionality

```python
import numpy as np, matplotlib.pyplot as plt
from scipy.spatial.distance import pdist

rng = np.random.default_rng(0)
dims = [2, 5, 10, 20, 50, 100, 200, 500, 1000]
ratios = []
print(f"{'d':>5} {'min':>9} {'mean':>9} {'max':>9} {'(max-min)/min':>15}")
for d in dims:
    X = rng.random((200, d))
    dist = pdist(X)                      # all 19,900 pairwise distances
    lo, hi, mu = dist.min(), dist.max(), dist.mean()
    r = (hi - lo) / lo
    ratios.append(r)
    print(f"{d:>5} {lo:>9.4f} {mu:>9.4f} {hi:>9.4f} {r:>15.4f}")

plt.figure(figsize=(6.5, 4))
plt.plot(dims, ratios, "o-")
plt.xscale("log"); plt.axhline(1.0, ls="--", c="grey")
plt.xlabel("dimensions (log scale)"); plt.ylabel("(max − min) / min")
plt.title("Distance contrast collapses with dimension")
plt.tight_layout(); plt.savefig("curse.png", dpi=110); plt.close()
print("saved curse.png")
```

**(a)** Output (`scipy` ships as a scikit-learn dependency; if you'd rather not import it, `sklearn.metrics.pairwise_distances` works too):

```
    d       min      mean       max   (max-min)/min
    2    0.0032    0.5183    1.3218        410.4534
    5    0.1198    0.9081    1.9299         15.1081
   10    0.4318    1.2648    2.3193          4.3712
   20    0.9276    1.7981    2.8637          2.0872
   50    1.9147    2.8564    3.9354          1.0553
  100    3.2028    4.0567    5.0138          0.5654
  200    4.9636    5.7481    6.6470          0.3391
  500    8.3405    9.1085    9.9224          0.1898
 1000   12.1858   12.8899   13.6600          0.1209
```

(The `d = 2` value is enormous because with 200 points crammed into a unit square, two of them land almost on top of each other, making `min` nearly zero. That's a real property of low dimensions, not a glitch — and it is precisely what stops happening as `d` grows.)

**(b)** Saved as `curse.png`. On a log-x axis the ratio drops roughly linearly.

**(c)** The contrast ratio crosses below 1.0 somewhere between **d = 50 and d = 100** (it's 1.055 at d=50 and 0.565 at d=100). In plain English: past about 50 dimensions, the most distant pair of points in your dataset is **less than twice** as far apart as the closest pair. Every point is essentially the same distance from every other point.

**(d)** k-means makes every decision by comparing distances — "which centroid is nearest?" When all distances converge to nearly the same value, the differences the algorithm relies on become smaller than the noise in your data, so the assignment step is choosing between options that are barely distinguishable. Small changes in a single feature, or a different random seed, then flip large numbers of assignments, which is why high-dimensional clusterings are unstable and rarely reproduce. The two responses are: **reduce dimensions first** (PCA to a handful of components, which is the main reason PCA and k-means are taught together), and **use a distance that suits your data** rather than raw Euclidean — cosine distance for text and other sparse high-dimensional vectors, where only the direction of the vector carries meaning.

### 6. [Stretch] Do cluster features actually help?

```python
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold

data = load_breast_cancer()
X, y = data.data, data.target
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

pipes = {
    "1 raw 30 features": Pipeline([
        ("sc", StandardScaler()),
        ("clf", LogisticRegression(max_iter=5000))]),
    "2 PCA(5)": Pipeline([
        ("sc", StandardScaler()),
        ("pca", PCA(n_components=5)),
        ("clf", LogisticRegression(max_iter=5000))]),
    "3 kmeans(4) dists": Pipeline([
        ("sc", StandardScaler()),
        ("km", KMeans(n_clusters=4, n_init=10, random_state=0)),
        ("clf", LogisticRegression(max_iter=5000))]),
    "4 raw + kmeans(4)": Pipeline([
        ("sc", StandardScaler()),
        ("fu", FeatureUnion([
            ("passthrough", FunctionTransformer(validate=False)),
            ("km", KMeans(n_clusters=4, n_init=10, random_state=0))])),
        ("clf", LogisticRegression(max_iter=5000))]),
}

print(f"{'pipeline':22s} {'AUC':>8} {'std':>8}")
for name, p in pipes.items():
    s = cross_val_score(p, X, y, cv=cv, scoring="roc_auc")
    print(f"{name:22s} {s.mean():>8.4f} {s.std():>8.4f}")
```

**(a)** Representative output:

```
pipeline                    AUC      std
1 raw 30 features        0.9955   0.0056
2 PCA(5)                 0.9938   0.0082
3 kmeans(4) dists        0.9905   0.0078
4 raw + kmeans(4)        0.9949   0.0059
```

**(b)** **Pipeline 1 (raw 30 features) wins** at 0.9955 — and none of the differences are real.

Do the arithmetic rather than eyeballing the ranking. Pipeline 1's own fold-to-fold standard deviation is 0.0056. The gap to PCA(5) is 0.0017 (0.3 std). The gap to pipeline 4 is 0.0006 (0.1 std). Even the largest gap, to the k-means-distances pipeline, is 0.0050 — still **under one standard deviation**. On this dataset all four approaches are statistically indistinguishable, and any write-up that declares a winner is over-reading five folds of a 569-row dataset.

The engineering conclusion is far more interesting than the ranking. PCA(5) matches the full model using **one-sixth of the features**, and four k-means centroid distances — derived without ever looking at `y` — get within half a standard deviation of thirty carefully measured tumour features. On a problem where those 30 features were expensive to collect, or where you had 60 rows instead of 569, that would be a decisive argument for compression. And adding cluster distances *on top of* the raw features (pipeline 4) bought exactly nothing, because a linear model with 30 standardized features already has enough flexibility that k-means's geometric hints are redundant.

**(c)** Every transformer must sit inside the `Pipeline` because **`StandardScaler`, `PCA`, and `KMeans` all fit parameters from data**: column means and standard deviations, eigenvectors, centroid positions. `cross_val_score` refits everything inside the pipeline on each training fold and only then applies it to the held-out fold, so the held-out rows never influence the transform. Fit them outside, on all 569 rows, and the principal components are computed partly from the very rows you're about to score, which is preprocessing leakage exactly as defined in Module 2.

What number would you get? Something like this:

```python
X_leaky = PCA(n_components=5).fit_transform(StandardScaler().fit_transform(X))
s = cross_val_score(LogisticRegression(max_iter=5000), X_leaky, y, cv=cv, scoring="roc_auc")
print(f"LEAKY PCA(5): {s.mean():.4f} +/- {s.std():.4f}")
```

```
LEAKY PCA(5): 0.9936 +/- 0.0090
```

Note what happened: **0.9936 versus the honest 0.9938.** The leak moved the score by −0.0002 — and that is the genuinely dangerous part of this lesson. On 569 rows with 30 well-behaved features, unsupervised leakage does not reliably move the number at all — here it happened to move it *down* — so you absolutely cannot catch it by noticing a suspiciously good result. You have to catch it by reading the code.

Why is the effect so small? PCA fitted on 569 rows and PCA fitted on the 455 rows of a training fold produce almost the same components, because 455 rows is already plenty to estimate a 30×30 covariance matrix. The leak is real but the leaked information is negligible. Now change the shape of the problem: 300 rows and 20,000 features, as in genomics. There the components fitted on all rows are dominated by whichever noise directions happen to align with the test rows, and the same one-line mistake can inflate AUC by 0.15 or more — producing a model that looks publishable and predicts nothing. **The size of a leakage bug depends on the shape of your data, not on how obviously wrong the code looks.**

</details>

---

[⬅ Previous](module-07-cnns-for-images.md) · [Level 3 Home](README.md) · [Next ➡](module-09-classic-nlp.md)

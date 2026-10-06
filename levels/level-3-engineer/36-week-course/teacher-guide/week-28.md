# Week 28 — Sorting With No Answer Key

[⬅ Week 27](week-27.md) · [Course Home](../README.md) · [Week 29 ➡](week-29.md) · [Student Guide](../student-guide/week-28.md) · [Workbook](../workbook/week-28.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — Term 4 opens, and the labels go away |
| **Big idea** | Two steps, repeated: **give every point to its nearest centre, then move every centre to the middle of what it got.** That is the whole algorithm. There is nothing else in it. |
| **New vocabulary** | unsupervised learning · cluster · centroid · inertia (WCSS) · k-means++ · elbow method |
| **New maths** | **Sigma notation** `Σ`, introduced as nothing more than *"add up all of these"* — and **the full expanded sum written out beside the symbol every single time.** It arrives on inertia over six points, where the expanded sum is six numbers and one addition. |
| **New syntax** | `KMeans(n_clusters=3, n_init=10, random_state=0)` · `km.cluster_centers_` · `km.inertia_` · `km.labels_` |
| **Dataset** | **Six 2-D points typed on the board by hand**, then `load_wine()` — 178 wines, 13 chemical measurements, and three real grape varieties we lock in a drawer. Both ship inside scikit-learn. **Nothing downloads. No internet needed.** |
| **Materials** | Printed workbook pages 28.1–28.7 · **masking tape** · **a big blank sheet headed SIX POINTS with a grid drawn on it** · squared paper for everybody · **three colours of pen per student** · two volunteers willing to stand still · the Bug Log |
| **Tech needed** | Laptop with Python 3, numpy, pandas, scikit-learn. **No torch this week. No new installs.** |
| **Prep time** | 25 minutes the night before · 10 minutes on the day (taping six crosses to the floor) |
| **Expected runtime of the code** | `no_answer_key.py` runs in **about 1.5 seconds** end to end on this machine. Nothing here trains a neural network. **Time yours anyway.** |

> **⚠️ Watch out:** this is the first week of the whole course with **no right answer to check against**, and the temptation — for you as much as for the student — is to reach for one. Resist it. The wine data does have hidden labels and we do open the drawer at the very end, but **that is a luxury, not the method.** If the class comes away thinking "clustering worked because it matched the grape varieties", they have learned the wrong lesson. What they should come away with is: **k-means always returns clusters, on any data whatsoever, including pure noise — so the burden of proof is entirely on you.**

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Run two full k-means iterations by hand** on six 2-D points, **showing all twelve squared distances in each round** and both new centroids, and name the point that switched sides.
2. **Read sigma notation as "add up all of these"** and **write the expanded sum out beside the symbol** — six squared distances, one addition, `= 6.6667`.
3. **Compute inertia by hand** for a clustering and say what a smaller value means about the clusters — and why you can never choose `k` by making it smallest.
4. **Show a numeric example where scaling flips the answer**, and name which column took over and why, from the column's spread alone.

Observable evidence: page 28.3 with twelve squared distances in round 1 and twelve in round 2, and **C circled as the switcher**; the sigma sum written out as `0.4444 + 1.1111 + 1.1111 + 0.0000 + 2.0000 + 2.0000 = 6.6667` beside the symbol; `km.inertia_` printing `6.6667` and the student's hand total matching it; and a sentence naming **`proline`, spread 314.91** as the column that ate the unscaled wine clustering.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each one carries on from the one above. **The complete runnable file is in the Prep Checklist and the Answer Key.**

**This week is genuinely easier than the last eight, and it is worth knowing that in advance.** There is no calculus, no matrix multiply, no network. The algorithm is two steps and a stopping rule, and the arithmetic is squaring small whole numbers and taking averages. If Term 3 was the hard climb, Term 4 starts on the flat.

What *is* new, and what your prep has to buy, is a different **kind** of thinking: there is no answer key, so a result is only worth what your argument for it is worth.

### 1. What "unsupervised" means, and exactly what it costs you

Every model in this course so far has been handed the answers.

> **Supervised learning** — you have a table of features `X` **and** a column of right answers `y`. The model learns to go from one to the other, and you score it by comparing its guesses to the real `y`.

> **Unsupervised learning** — you have **only** `X`. There is no `y`. The algorithm finds structure in the table, and **there is nothing to compare it against.**

That second sentence sounds mild and it is not. Here is what it actually costs:

| Question you could always answer before | Supervised | Unsupervised |
|---|---|---|
| Is my model any good? | compare to the held-out `y` — one number | **no held-out truth exists** |
| Did I overfit? | train score much better than test score | **hard even to define** |
| Is this row's answer right? | yes or no | **there is no right answer for a row** |
| What can I measure at all? | accuracy, precision, recall, AUC, log loss | internal tidiness, and whether it survives being jiggled |

🍕 **The analogy to use, and to keep using all lesson.** Supervised learning is a maths test with the answers printed in the back. Unsupervised learning is being handed a shoebox of 500 mixed Lego bricks and told *"sort these."* By colour? By size? By shape? By which set they came out of? **Every one of those is a real sorting and none of them is the right one.** What you can do is defend your choice: *"I sorted by shape, because the piles came out roughly even, the bricks in each pile really do look alike, and shape is what matters for building."*

So the deliverable changes. **In supervised learning you ship a score. In unsupervised learning you ship an argument.** That is Week 30's whole lesson, and it starts here.

### 2. The algorithm, in four lines, and then done by hand

> **Cluster** — a group of points that are more like each other than like anything outside the group.

> **Centroid** — the average position of everything currently in a cluster. Its centre of gravity. If a cluster holds the points (1,2) and (2,1), its centroid is at ((1+2)÷2, (2+1)÷2) = (1.5, 1.5).

Here is the entire algorithm:

```text
1. Put down k centres, anywhere.
2. ASSIGN : give every point to its nearest centre.
3. MOVE   : put every centre in the middle of the points it just got.
4. Go back to 2. Stop when nobody changed cluster.
```

That is all of it. Steps 2 and 3 take turns, and **each of them can only make the clusters tighter, never looser**, which is why the thing always stops.

![Two steps, repeated: assign, then move](../figures/fig-w28-1-assign-then-move-two-steps.svg)
*Figure 28.1 — Two steps, repeated: assign, then move. C measures 1 + 1 = 2 to one centre and 0 + 0 = 0 to the other, so it goes to the second one. Then centre 1 moves to the middle of A and B: (1+2) ÷ 2 = 1.5 and (2+1) ÷ 2 = 1.5.*

🍕 **The analogy for the two steps.** Three food trucks park in a big park full of picnickers. **Round 1:** every picnicker walks to whichever truck is nearest. **Round 2:** each truck looks at where its own customers ended up sitting and drives to the middle of them. **Round 3:** some picnickers notice a different truck is now closer and switch over. The trucks move again. After a few rounds nobody switches, the trucks stop, and you have three neighbourhoods that nobody designed.

**Now the numbers, because this is the part you will be teaching.** Six points, typed on the board:

```text
A = (1, 2)      D = (8, 8)
B = (2, 1)      E = (9, 7)
C = (2, 3)      F = (7, 9)
```

`k = 2`, and we put the two starting centres **deliberately badly** — both of them in the left-hand bunch, one sitting exactly on top of A and one exactly on top of C:

```text
centre 1 = (1, 2)        centre 2 = (2, 3)
```

**We use squared distance throughout, and never take a square root.** Squaring does not change which centre is nearer, and it saves the class an enormous amount of arithmetic. *"How far, squared"* means: the across-gap squared, plus the up-gap squared.

**ROUND 1, assign.** Twelve squared distances. Every one of them is small whole-number arithmetic.

| point | to centre 1 = (1,2) | to centre 2 = (2,3) | nearer |
|---|---|---|---|
| A (1,2) | 0 + 0 = **0** | 1 + 1 = 2 | **centre 1** |
| B (2,1) | 1 + 1 = **2** | 0 + 4 = 4 | **centre 1** |
| C (2,3) | 1 + 1 = 2 | 0 + 0 = **0** | **centre 2** |
| D (8,8) | 49 + 36 = 85 | 36 + 25 = **61** | **centre 2** |
| E (9,7) | 64 + 25 = 89 | 49 + 16 = **65** | **centre 2** |
| F (7,9) | 36 + 49 = 85 | 25 + 36 = **61** | **centre 2** |

Groups: **centre 1 got {A, B}** and **centre 2 got {C, D, E, F}**.

**Look at how bad that is, and say so out loud.** C is sitting right next to A and B, and it has been filed with three points seven units away — for one reason only: **centre 2 happened to be standing on top of it, so its distance was 0.** This is not the algorithm being stupid. It is the algorithm doing exactly what it was told with a bad starting position.

**ROUND 1, move.**

```text
centre 1 = middle of {A, B} = ( (1+2) ÷ 2 , (2+1) ÷ 2 ) = ( 1.5 , 1.5 )

centre 2 = middle of {C, D, E, F}
         = ( (2+8+9+7) ÷ 4 , (3+8+7+9) ÷ 4 )
         = ( 26 ÷ 4 , 27 ÷ 4 )
         = ( 6.5 , 6.75 )
```

**ROUND 2, assign.** Twelve more squared distances, now against the moved centres.

| point | to centre 1 = (1.5, 1.5) | to centre 2 = (6.5, 6.75) | nearer |
|---|---|---|---|
| A (1,2) | 0.25 + 0.25 = **0.50** | 30.25 + 22.5625 = 52.8125 | **centre 1** |
| B (2,1) | 0.25 + 0.25 = **0.50** | 20.25 + 33.0625 = 53.3125 | **centre 1** |
| C (2,3) | 0.25 + 2.25 = **2.50** | 20.25 + 14.0625 = 34.3125 | **centre 1 ← switched!** |
| D (8,8) | 42.25 + 42.25 = 84.50 | 2.25 + 1.5625 = **3.8125** | **centre 2** |
| E (9,7) | 56.25 + 30.25 = 86.50 | 6.25 + 0.0625 = **6.3125** | **centre 2** |
| F (7,9) | 30.25 + 56.25 = 86.50 | 0.25 + 5.0625 = **5.3125** | **centre 2** |

Groups: **{A, B, C}** and **{D, E, F}**. **C came home.** The bad start repaired itself in exactly one round, and that is a genuinely lovely thing to watch happen on the floor.

**ROUND 2, move.**

```text
centre 1 = ( (1+2+2) ÷ 3 , (2+1+3) ÷ 3 ) = ( 5÷3 , 6÷3 ) = ( 1.6667 , 2.0 )
centre 2 = ( (8+9+7) ÷ 3 , (8+7+9) ÷ 3 ) = ( 24÷3 , 24÷3 ) = ( 8.0 , 8.0 )
```

**ROUND 3 would change nothing** — A, B and C are obviously nearer (1.67, 2) than (8, 8), and D, E and F the other way round. Nobody switches, so we stop. **Converged in two rounds.**

![The same six points, recoloured three times](../figures/fig-w28-2-points-recolouring-over-three-iterations.svg)
*Figure 28.2 — The same six points, recoloured three times. The points never move; only their group and the centres do. 2 and 4 after round 1, then 3 and 3.*

### 3. Inertia — and sigma, which is only shorthand for addition

You now have two clusters. **How good are they?** There is no `y` to check, so the only honest thing to measure is *tightness*: how far is every point from its own centre?

> **Inertia**, also called **WCSS** (within-cluster sum of squares) — add up the squared distance from every point to its own centre. **Smaller means tighter clusters.**

Worked all the way out, with the final centres (1.6667, 2.0) and (8, 8):

```text
A (1,2) to (1.6667, 2.0) :  0.4444 + 0.0000 = 0.4444
B (2,1) to (1.6667, 2.0) :  0.1111 + 1.0000 = 1.1111
C (2,3) to (1.6667, 2.0) :  0.1111 + 1.0000 = 1.1111
D (8,8) to (8.0,    8.0) :  0.0000 + 0.0000 = 0.0000
E (9,7) to (8.0,    8.0) :  1.0000 + 1.0000 = 2.0000
F (7,9) to (8.0,    8.0) :  1.0000 + 1.0000 = 2.0000
                                     inertia = 6.6667
```

Check one of those by hand right now, so you can do it in front of them: B is at (2, 1) and its centre is at (1.6667, 2.0). Across: 2 − 1.6667 = 0.3333, squared = **0.1111**. Up: 1 − 2.0 = −1.0, squared = **1.0000**. Total **1.1111**. ✅

**And now sigma, which is the only new notation in Term 4 so far.** In a book you will see inertia written like this:

```text
inertia  =  Σ  (distance from a point to its own centre)²
```

> **🔢 The maths, slowly:** **`Σ` is the Greek capital letter S, and it stands for "Sum". It means, in full: "add up all of these."** That is the entire content of the symbol. It is an instruction to add, and nothing more. It does not multiply, it does not do anything clever, and there is no hidden step inside it.

**The rule for this course, and it is not negotiable for the next four weeks: every time the symbol appears, write the sum out in full beside it.**

```text
Σ (distance)²   means   0.4444 + 1.1111 + 1.1111 + 0.0000 + 2.0000 + 2.0000
                      = 6.6667
```

![The sigma symbol means add up all of these](../figures/fig-w28-3-sigma-with-the-sum-written-out.svg)
*Figure 28.3 — The sigma symbol means add up all of these. One symbol on the left; the six numbers it is short for on the right, adding to 6.6667 — which is exactly what `km.inertia_` prints.*

**Why the symbol exists at all**, and this is worth saying, because a 14-year-old will reasonably ask: with six points you would just write the six numbers. With 178 wines you would not, and with 40,000 supermarket customers you certainly would not. **The symbol is shorthand for a list too long to write.** It is a labour-saving device, not a piece of cleverness. Say that.

**The one thing to get right about inertia:** it is the number k-means is trying to make small, and **it always falls when you ask for more clusters.** At `k` = the number of points, every point is its own centre and inertia is exactly 0. So:

> **⚠️ Watch out:** you can never choose `k` by picking the smallest inertia. The smallest is always "one cluster per point", which tells you nothing. This is the single most common mistake in the whole subject.

### 4. Where you start matters, and the two settings that handle it

k-means never gets worse, but it can get **stuck somewhere that is not the best answer**. Run our six points with `k = 3` and all three starting centres crowded in the left-hand bunch, and here is what really happens:

```text
all 3 centres in the left bunch : labels [0 1 0 2 2 2]  inertia 5.0
k-means++ with n_init=10        : labels [1 1 1 0 2 0]  inertia 3.6667
```

Read those two rows carefully, because there is a subtlety in them that is worth your time.

- The crowded start gave `{A, C}`, `{B}`, `{D, E, F}` — inertia **5.0**.
- k-means++ with ten restarts gave `{A, B, C}`, `{D, F}`, `{E}` — inertia **3.6667**.

**3.6667 is lower, so by the only measure k-means has, the second answer is better.** And notice what it actually did: it kept the left bunch whole and **split the right-hand bunch in half.** That is probably not what you would have drawn with a pencil. **Both of those facts are true, and you should say both.** Lower inertia means tighter; it does not mean "the grouping a human wanted".

> **k-means++** — a smarter way of choosing the starting centres, which spreads them out instead of letting them land on top of each other.

> **`n_init=10`** — run the whole algorithm ten times from ten different starts and keep whichever run finished with the lowest inertia.

scikit-learn uses k-means++ by default, and older versions also ran `n_init=10` for you (newer ones default to `n_init="auto"`, a single run for k-means++, so this course asks for `n_init=10` explicitly). Which is why you will rarely see a really bad clustering — but you should know it is being handled for you rather than believing the algorithm is start-proof.

### 5. The thing that decides the answer, and it is not the algorithm

**k-means measures distance. Distance adds up squared gaps across every column. So the column with the biggest numbers wins.** Not "has more influence". Wins.

Three customers, with two columns — age in years, income in rupees:

```text
P1 = (25, 500000)
P2 = (55, 500000)
P3 = (25, 520000)
```

Squared distances on the raw numbers:

```text
P1 to P2 : (25−55)² + (500000−500000)² =    900 +           0 =         900
P1 to P3 : (25−25)² + (500000−520000)² =      0 + 400,000,000 = 400,000,000
```

```text
400000000 ÷ 900 = 444444
```

**Raw k-means believes P1 and P2 are 444,444 times more alike than P1 and P3** — even though P1 and P2 are thirty years apart in age, and P1 and P3 differ only by a 4% pay rise. **The age column has not been weakened. It has been deleted.** 900 against 400 million is not a contribution; it is a rounding error.

Now standardise each column — subtract its mean, divide by its spread, exactly as in Week 4:

```text
age:    mean 35,          spread    14.1421  →  −0.7071, +1.4142, −0.7071
income: mean 506666.67,   spread  9428.0904  →  −0.7071, −0.7071, +1.4142
```

```text
P1 to P2 : (−0.7071 − 1.4142)² + 0 = 4.5
P1 to P3 : 0 + (−0.7071 − 1.4142)² = 4.5
```

**Exactly equal. And that is the honest answer:** each pair differs by the same amount in one standardised column and not at all in the other. Same three customers, same algorithm, opposite conclusion.

![The same three customers, two different rulers](../figures/fig-w28-4-unscaled-versus-scaled-clusters-flip.svg)
*Figure 28.4 — The same three customers, two different rulers. 400,000,000 ÷ 900 = 444,444 on the raw numbers; 4.5 ÷ 4.5 = 1 once both columns are on the same ruler.*

**And here is the proof on real data, which is the bit that will land.** Cluster the 178 wines on their raw 13 columns, then look at what the clusters actually are:

```text
cluster 0: n= 69  proline  278 to  590   alcohol 11.03 to 14.13
cluster 1: n= 47  proline  970 to 1680   alcohol 12.85 to 14.83
cluster 2: n= 62  proline  600 to  937   alcohol 11.45 to 14.34
```

**Read the proline column: 278–590, 600–937, 970–1680. Three bands that do not overlap by a single unit.** Read the alcohol column: 11.03–14.13, 12.85–14.83, 11.45–14.34 — they overlap almost completely. **The "clustering" of thirteen chemical measurements is a sorting of one column into three bands.** And you could have predicted it from one printout:

```text
proline                         314.91
magnesium                        14.28
alcalinity_of_ash                 3.34
color_intensity                   2.32
malic_acid                        1.12
flavanoids                        1.00
alcohol                           0.81
```

`proline`'s spread is **314.91**. `flavanoids`' is **1.00**. Squared, that is a ratio of about 99,000 to 1. **Twelve of the thirteen columns were not consulted.**

> **Always scale before k-means.** Standardising is the default, and the only exception is when every column is already in the same natural unit and you genuinely *want* the wider-ranging one to count more.

### 6. The elbow, and why it cannot decide on its own

`k` is your decision. Nothing in the algorithm picks it. The usual first move is the **elbow method**.

> **Elbow method** — plot inertia against `k`, and look for the bend: the `k` after which extra clusters stop buying you much.

Here is the real table for the 178 **scaled** wines:

```text
  k   inertia     drop
  1    2314.0        -
  2    1659.0    655.0
  3    1277.9    381.1
  4    1180.7     97.2
  5    1110.4     70.4
  6    1044.5     65.9
  7     996.0     48.5
  8     944.6     51.4
```

**Read the drop column, not the inertia column.** Going 1→2 bought 655. Going 2→3 bought 381. Going 3→4 bought **97**. That is where the cliff is:

```text
381.1 ÷ 97.2 = 3.9
```

**The last cluster that was nearly four times as useful as the next one is the third.** After that it is a trickle: 70, 66, 48, 51.

![The elbow is where the drop stops paying](../figures/fig-w28-5-the-elbow-drops-printed.svg)
*Figure 28.5 — The elbow is where the drop stops paying. Inertia falls from 2314.0 to 944.6, and the drops are 655.0, 381.1, then a collapse to 97.2. The ratio 381.1 ÷ 97.2 = 3.9 is the finding; the picture is only a hint.*

**Be honest about this tool.** Elbows are frequently not obvious, two sensible people read the same curve differently, and on plenty of real datasets there is no bend at all — just a smooth arc. **Report the drop ratio, which is a number, rather than pointing at a picture.** And Week 30 brings a second, independent piece of evidence, which is the actual fix.

### 7. Every new line of this week's code, explained to somebody who has never programmed

Four new things, and they all hang off one object.

**New line 1 — build the thing and run it.**

```python
km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
```

Read it right to left in three parts. `KMeans(...)` **builds** a clusterer but does not run it — it is an empty machine with its dials set. `n_clusters=3` is how many groups you are asking for. `n_init=10` says *"do the whole thing ten times from ten different starting positions and keep the best"*. `random_state=0` fixes the dice so you and the student get identical numbers. Then `.fit(X)` **runs it** on the table `X`. The result is stored back inside `km`, and `.fit` also hands `km` back, which is why you can chain it onto the end like that.

**New line 2 — which group did each row go in?**

```python
km.labels_
```

One whole number per row of `X`, in the same order as the rows. `[0 0 0 1 1 1]` means the first three rows are in group 0 and the last three in group 1.

> **⚠️ Watch out:** **the trailing underscore is not decoration.** In scikit-learn, a name ending in `_` means *"this did not exist until `.fit` was called"*. Ask for `km.labels_` before fitting and you get an `AttributeError`, which is the machine correctly telling you it has not been told anything yet.

**And the thing to say out loud, twice:** `0`, `1` and `2` are **names, not measurements.** Group 0 is not smaller, better or first. Re-run with a different seed and the same three groups can come back numbered differently. **Never do arithmetic on a cluster number.**

**New line 3 — where did the centres end up?**

```python
km.cluster_centers_
```

A small table: one row per cluster, one column per feature. With 3 clusters and 13 wine columns that is a (3, 13) grid. **Its numbers are in whatever units `X` was in** — so if you scaled `X` first, these are standardised numbers and nobody can read them. That matters in Week 30.

**New line 4 — how tight is it?**

```python
km.inertia_
```

The single number from §3: every point's squared distance to its own centre, added up. `6.6667` for our six points, and the class can check that by hand, which is the entire point of using six points.

**And one extra keyword, used exactly once today**, so the computer starts where we started by hand:

```python
init = np.array([[1., 2.], [2., 3.]])     # centre 1 on A, centre 2 on C
km = KMeans(n_clusters=2, init=init, n_init=1, random_state=0).fit(X)
```

`init=` hands it our two starting centres instead of letting it choose. `n_init=1` says *"don't restart, I want this one run"*. **Without `init=` the trace will not match the board** (with explicit centres sklearn runs once regardless, but warns if `n_init` is left at 10), and a mismatched trace at that moment in the lesson is genuinely confusing rather than interesting.

**One number will be off by one, and it is not a bug.** scikit-learn prints `km.n_iter_` as **3** where the class counted **2**. sklearn counts the final pass that *confirmed* nothing had changed. Say so: *"we counted the rounds that changed something; it counts the round that checked."*

### 8. The three misconceptions you will actually meet

**Misconception 1 — "the clusters are the real groups."**
They are the groups that this algorithm, with this `k`, on these columns, with this scaling, happened to return. **Cure:** run the whole pipeline on 178 rows of pure random numbers. You still get three clusters, with sizes `[62 44 72]`, and you can still invent names for them. Week 30 does this on purpose; mention it today.

**Misconception 2 — "lower inertia means a better answer."**
Lower inertia means *tighter*. **Cure:** the `k=3` result in §4 — inertia 3.6667 beat 5.0 by splitting the right-hand bunch in half, which is not what anyone would have drawn. And the killer: at `k = 178` on the wine data, inertia is exactly 0 and the result is useless.

**Misconception 3 — "we scaled because scaling is good practice."**
No. You scaled because otherwise `proline` decides everything. **Cure:** the three non-overlapping proline bands. That is not an abstract risk, it is what happened.

### 9. How deep to go, and where to stop

**Go this far:** unsupervised means no `y` and therefore no score; the assign/move loop done by hand for two full rounds with every squared distance written; the point that switches; centroids as averages; inertia added up by hand and matched against `km.inertia_`; sigma as "add up all of these" with the sum always written out; why you can never minimise inertia to choose `k`; the elbow and its drop ratio; and scaling, demonstrated numerically twice.

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| **The silhouette score** | **Week 30.** It is the second, independent piece of evidence for `k`, and today's honest position is *"the elbow alone is a hint"*. Do not resolve that tension today — the tension is what makes Week 30 land. |
| **Adjusted Rand index** | **Week 30.** Today we compare against the hidden grape varieties by eye, with a table of counts from Week 8. One number for the same job arrives in two weeks. |
| **PCA, and drawing the clusters on a map** | **Week 29 and Week 30.** Today the wine clustering is read from numbers, not a picture. |
| Naming the clusters from a feature-means table | **Week 30.** Today's wine work is about *scaling*, not interpretation. |
| Other clustering algorithms — DBSCAN, hierarchical, Gaussian mixtures | Not in this level. If asked: *"there are dozens, they mostly differ in what shape of cluster they can find, and k-means only ever finds round blobs."* One sentence, then move. |
| The proof that k-means always converges | No proofs in this level. *"Each step can only make things tighter, and it cannot get tighter forever"* is the honest version and it is enough. |
| Choosing distance measures — cosine, Manhattan | Week 32 meets cosine similarity for text. Not today. |

The line to hold in your head all lesson: **today the student runs an algorithm that cannot be marked right or wrong, and starts learning what to do about that.**

---

### 10. 🧭 The Growing Map — the last stage opens

The student guide carries a figure called **Where This Fits**: the same picture every week with one more
piece filled in. This week the gold jumps two stages to the right, and there is exactly **one** dashed
box left on the whole map.

![The Level 3 pipeline in Week 28: the last stage opens and the no labels and words tile is this week's box](../figures/fig-w28-0-where-this-fits.svg)

*Figure 28.0 — Week 28's version. Every stage box is solid; the gold is on `no labels · words`, weeks 28
to 33. The ↻ on stage three is black, as it has been since Week 12.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Ask "which box did we do today?" and then "what is missing from it?"** The box is *no labels ·
   words* — and the first two words of the tile's own label are the answer to the second question.
   **There was no `y` today.** Point at the six taped crosses still on the floor: nobody wrote a group
   number next to any of them, and the class still found the groups. That is the tile, in one gesture.
2. **Anchor it on point C.** *"C was in the left group in round one and the right group in round two.
   Which of the two steps moved it?"* The answer is neither — **the centres moved, and C's nearest centre
   changed as a consequence.** That is the whole algorithm and it is worth being able to say out loud
   while pointing at the floor.
3. **Point at stage one, then at the one dashed box.** Stage one, because `proline` with a spread of
   **314.91** ate the unscaled clustering — *"which box did we go back to when the answer came out
   wrong?"* And the dashed box, because `ship it · showcase` is now the only thing on the map that has
   not happened. *"Six more weeks of new shapes, then you ship something."*

> **🧑‍🏫 Why this is worth two minutes.** This is the week the subject changes underneath the student, and
> a number of them will not notice. Everything since Week 1 has had an answer column, and the map is the
> cheapest way to say *"we have moved"* — the gold is visibly in a different part of the picture. It also
> defuses the most common Term 4 anxiety, which is *"how do I know if I got it right?"* You did not get
> it right. **There is no right, which is what the tile says.**

**One thing to notice, so you can answer if asked.** `learning signal` is lit alongside `model`, in a
week with no gradients anywhere. That is correct and worth defending: **inertia is a learning signal.**
It is the quantity that tells the centres where to move, it only ever goes down, and it stops the
algorithm — the same three sentences the class learned about loss in Week 14, with no `y` in sight. If a
student spots that a "learning signal" with no labels sounds contradictory, that is an excellent spot.

---

## 🧰 Prep Checklist

This section lists what to do before the lesson, with the complete runnable file.

### 25 minutes the night before

- [ ] **Type and run `no_answer_key.py` yourself.** It is short and fast. The complete file:

```python
"""no_answer_key.py - Week 28: sorting six points, then 178 wines, with no labels."""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import load_wine
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler

np.random.seed(0)

# ---------- 1. the six points, started exactly where we started by hand ----------
X = np.array([[1., 2.], [2., 1.], [2., 3.],
              [8., 8.], [9., 7.], [7., 9.]])
names = ["A", "B", "C", "D", "E", "F"]
init = np.array([[1., 2.], [2., 3.]])       # centre 1 on A, centre 2 on C

km = KMeans(n_clusters=2, init=init, n_init=1, random_state=0).fit(X)
print("labels        :", km.labels_)
print("centres       :", np.round(km.cluster_centers_, 4).tolist())
print("inertia       :", round(km.inertia_, 4))
print("rounds counted:", km.n_iter_)

# ---------- 2. inertia, added up one point at a time ----------
print()
print("--- inertia: add up all six squared distances ---")
total = 0.0
for nm, p, lab in zip(names, X, km.labels_):
    c = km.cluster_centers_[lab]
    dx2, dy2 = (p[0] - c[0]) ** 2, (p[1] - c[1]) ** 2
    total += dx2 + dy2
    print("  %s (%g,%g) to centre %d (%.4f,%.4f): %.4f + %.4f = %.4f"
          % (nm, p[0], p[1], lab, c[0], c[1], dx2, dy2, dx2 + dy2))
print("  all six added up:", round(total, 4))
print("  km.inertia_     :", round(km.inertia_, 4))

# ---------- 3. where you start matters ----------
print()
print("--- same six points, k=3, two different starting places ---")
crowded = np.array([[1., 2.], [2., 1.], [2., 3.]])
k_bad = KMeans(n_clusters=3, init=crowded, n_init=1, random_state=0).fit(X)
k_pp = KMeans(n_clusters=3, init="k-means++", n_init=10, random_state=0).fit(X)
print("all 3 centres in the left bunch : labels", k_bad.labels_,
      " inertia", round(k_bad.inertia_, 4))
print("k-means++ with n_init=10        : labels", k_pp.labels_,
      " inertia", round(k_pp.inertia_, 4))

# ---------- 4. the ruler problem, on three customers ----------
print()
print("--- three customers: (age in years, income in rupees) ---")
P = np.array([[25., 500000.], [55., 500000.], [25., 520000.]])


def sq(a, b):
    return float(np.sum((a - b) ** 2))


print("RAW    d(P1,P2)^2 = %.1f" % sq(P[0], P[1]))
print("RAW    d(P1,P3)^2 = %.1f" % sq(P[0], P[2]))
print("so raw says P1 and P2 are %.0f times more alike"
      % (sq(P[0], P[2]) / sq(P[0], P[1])))
scaler = StandardScaler()
Z = scaler.fit_transform(P)
print("means used   :", np.round(scaler.mean_, 4))
print("spreads used :", np.round(scaler.scale_, 4))
print("standardised :\n", np.round(Z, 4))
print("SCALED d(P1,P2)^2 = %.4f" % sq(Z[0], Z[1]))
print("SCALED d(P1,P3)^2 = %.4f" % sq(Z[0], Z[2]))

# ---------- 5. 178 wines, labels locked in a drawer ----------
print()
wine = load_wine()
X_raw = pd.DataFrame(wine.data, columns=wine.feature_names)
y_secret = wine.target                       # not used until the very last line
print("wine table:", X_raw.shape)
print("the spread of each column, biggest first:")
print(X_raw.std().sort_values(ascending=False).round(2).to_string())

km_raw = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X_raw)
Xs = StandardScaler().fit_transform(X_raw)
km_sc = KMeans(n_clusters=3, n_init=10, random_state=0).fit(Xs)
print()
print("UNSCALED  sizes", np.bincount(km_raw.labels_),
      " inertia %.1f" % km_raw.inertia_)
print("SCALED    sizes", np.bincount(km_sc.labels_),
      " inertia %.1f" % km_sc.inertia_)

print()
print("--- what the UNSCALED clusters actually are ---")
pro = X_raw["proline"].values
alc = X_raw["alcohol"].values
for c in range(3):
    m = km_raw.labels_ == c
    print("cluster %d: n=%3d  proline %4.0f to %4.0f   alcohol %.2f to %.2f"
          % (c, m.sum(), pro[m].min(), pro[m].max(), alc[m].min(), alc[m].max()))

# ---------- 6. the elbow ----------
print()
print("--- the elbow, on the scaled wines ---")
prev = KMeans(n_clusters=1, n_init=10, random_state=0).fit(Xs).inertia_
print("  k   inertia     drop")
print("  1  %8.1f        -" % prev)
for k in range(2, 9):
    inr = KMeans(n_clusters=k, n_init=10, random_state=0).fit(Xs).inertia_
    print("  %d  %8.1f  %7.1f" % (k, inr, prev - inr))
    prev = inr

# ---------- 7. open the drawer ----------
print()
print("rows = the real grape variety, columns = the cluster we found")
print("UNSCALED\n", confusion_matrix(y_secret, km_raw.labels_))
print("SCALED\n", confusion_matrix(y_secret, km_sc.labels_))
```

Run `python3 no_answer_key.py`. You must see **exactly** this:

```text
labels        : [0 0 0 1 1 1]
centres       : [[1.6667, 2.0], [8.0, 8.0]]
inertia       : 6.6667
rounds counted: 3

--- inertia: add up all six squared distances ---
  A (1,2) to centre 0 (1.6667,2.0000): 0.4444 + 0.0000 = 0.4444
  B (2,1) to centre 0 (1.6667,2.0000): 0.1111 + 1.0000 = 1.1111
  C (2,3) to centre 0 (1.6667,2.0000): 0.1111 + 1.0000 = 1.1111
  D (8,8) to centre 1 (8.0000,8.0000): 0.0000 + 0.0000 = 0.0000
  E (9,7) to centre 1 (8.0000,8.0000): 1.0000 + 1.0000 = 2.0000
  F (7,9) to centre 1 (8.0000,8.0000): 1.0000 + 1.0000 = 2.0000
  all six added up: 6.6667
  km.inertia_     : 6.6667

--- same six points, k=3, two different starting places ---
all 3 centres in the left bunch : labels [0 1 0 2 2 2]  inertia 5.0
k-means++ with n_init=10        : labels [1 1 1 0 2 0]  inertia 3.6667

--- three customers: (age in years, income in rupees) ---
RAW    d(P1,P2)^2 = 900.0
RAW    d(P1,P3)^2 = 400000000.0
so raw says P1 and P2 are 444444 times more alike
means used   : [3.50000000e+01 5.06666667e+05]
spreads used : [  14.1421 9428.0904]
standardised :
 [[-0.7071 -0.7071]
 [ 1.4142 -0.7071]
 [-0.7071  1.4142]]
SCALED d(P1,P2)^2 = 4.5000
SCALED d(P1,P3)^2 = 4.5000

wine table: (178, 13)
the spread of each column, biggest first:
proline                         314.91
magnesium                        14.28
alcalinity_of_ash                 3.34
color_intensity                   2.32
malic_acid                        1.12
flavanoids                        1.00
alcohol                           0.81
od280/od315_of_diluted_wines      0.71
total_phenols                     0.63
proanthocyanins                   0.57
ash                               0.27
hue                               0.23
nonflavanoid_phenols              0.12

UNSCALED  sizes [69 47 62]  inertia 2370689.7
SCALED    sizes [65 51 62]  inertia 1277.9

--- what the UNSCALED clusters actually are ---
cluster 0: n= 69  proline  278 to  590   alcohol 11.03 to 14.13
cluster 1: n= 47  proline  970 to 1680   alcohol 12.85 to 14.83
cluster 2: n= 62  proline  600 to  937   alcohol 11.45 to 14.34

--- the elbow, on the scaled wines ---
  k   inertia     drop
  1    2314.0        -
  2    1659.0    655.0
  3    1277.9    381.1
  4    1180.7     97.2
  5    1110.4     70.4
  6    1044.5     65.9
  7     996.0     48.5
  8     944.6     51.4

rows = the real grape variety, columns = the cluster we found
UNSCALED
 [[ 0 46 13]
 [50  1 20]
 [19  0 29]]
SCALED
 [[ 0  0 59]
 [65  3  3]
 [ 0 48  0]]
```

**Expected runtime: about 1.5 seconds.** If yours takes ten, that is fine too — nothing here is slow enough to matter.

- [ ] **Do the two rounds by hand yourself, on paper, before you read §2 again.** Twelve squared distances, then twelve more. **It takes eight minutes and it is the single best-value prep in this file**, because you are going to do it live on a floor with a class watching.
- [ ] **Check the last two blocks of output and know what you are going to say about them.** The SCALED table has `59`, `65` and `48` sitting almost alone in their rows: **172 of 178 wines grouped with their own grape variety, by an algorithm that never saw a variety.** The UNSCALED table is a mess. **Have your sentence ready, and make it the honest one:** *"we got to check today because this dataset happens to have answers hidden in it. Normally you do not get to check. That is the whole problem."*
- [ ] **Print workbook pages 28.1–28.7.**
- [ ] **Make the SIX POINTS wall sheet.** A big sheet, a grid from 0 to 10 both ways, the six points marked and lettered, and **room underneath for two rounds of numbers.** It stays up until Week 30.
- [ ] **Tape six crosses to the floor** — see the Activity for the exact layout and the scale. **Ten minutes, and it needs doing before the class walks in**, because taping the floor with an audience takes twenty.
- [ ] **Three colours of pen per student.** Round 1 in one colour, round 2 in another, the centres in the third. **One colour does not work** — the whole point is seeing what changed.
- [ ] **Break it on purpose, once.** Run this and keep the output where you can see it:

```python
km = KMeans(n_clusters=2, n_init=10, random_state=0)
print(km.labels_)
```

```text
AttributeError: 'KMeans' object has no attribute 'labels_'
```

That is deliberate mistake one in the live-code, and it teaches the trailing-underscore rule better than any explanation.

### 10 minutes on the day

- [ ] Six crosses taped to the floor, lettered A to F on cards beside them.
- [ ] SIX POINTS sheet on the wall, the points marked, the number space blank.
- [ ] Editor open, terminal ready, `no_answer_key.py` **empty** — they type sections 1 and 2 with you.
- [ ] Workbook 28.2 out. **The predictions filled in, in pen, before anything runs.**
- [ ] Bug Log out.
- [ ] Squared paper and three pens on every desk.

### Fallback if the laptops fail

**This is the best week of the whole year for a power cut.** Three of the four objectives need no electricity at all, and the activity was already designed for a floor.

1. **The floor activity, unchanged.** Six taped crosses, two volunteers as centres, two full rounds with every squared distance on the board. **Objectives 1, 2 and 3 complete, with tape and a pen.**
2. **Inertia and sigma, on the board.** Six numbers, one addition, `6.6667`. The sigma rule — *write the sum out beside the symbol* — is a pen-and-paper rule anyway.
3. **The scaling flip, on the board.** `900` against `400,000,000`, then `4.5` against `4.5`. **Objective 4 complete**, and honestly it goes better on a board than a screen because you can leave both versions up side by side.
4. **The only casualty is the wine data.** Say so: *"the bit we cannot do is watch 178 real wines get sorted correctly by something that has never seen a grape. The numbers are on your homework sheet and it is your job to make them."*

| If this fails | Do this instead |
|---|---|
| The trace on screen does not match the board | You dropped `init=`. **`init=` is the one that matters**: without it sklearn starts wherever it likes and the whole comparison collapses. (Dropping only `n_init=1` gives the same trace plus a RuntimeWarning.) |
| `km.n_iter_` says 3 and a student objects | **They are right and so is sklearn.** It counts the confirming pass. Say so in one sentence and move on — do not let it eat three minutes. |
| The unscaled and scaled cluster sizes look similar and the point seems weak | **Do not argue from the sizes — argue from the proline ranges.** `278–590`, `600–937`, `970–1680`. Three bands, no overlap. That is the evidence. |
| Somebody points out the scaled clusters match the grape varieties, so "clustering works" | **Excellent, and it is a trap.** *"It worked here and we only know that because someone had already labelled these bottles. What would you have done if nobody had?"* That is the whole of Week 30. |
| The floor activity turns into a milling crowd | **Everybody stands still except the two centres.** The points do not move, ever. Say that before you start and repeat it once. |
| There is no floor space | Do it on the SIX POINTS wall sheet with two magnets, or on a desk with two coins. **The arithmetic is the lesson; the floor is a delivery mechanism.** |

---

## ⏱️ The Lesson, Minute by Minute

This section is the lesson plan: the segments first, then each one in order.

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — I Have Taken Your Answers Away | 7 | 7 | No `y`. The Lego box. The six points on the floor |
| 🧠 Concept & Maths — Assign, Move, Repeat, and One New Symbol | 18 | 25 | The two steps, inertia, sigma with the sum written out |
| 💻 Live-Code Together — `no_answer_key.py` | 18 | 43 | The trace matches the board. **Two deliberate mistakes.** |
| 🎲 Their Turn — k-Means on the Floor | 20 | 63 | Two full rounds, twelve squared distances each, by hand |
| 🔑 Wrap & Assign | 7 | 70 | The ruler, the wine drawer, three checks |

---

### 🪝 Hook — I Have Taken Your Answers Away (7 minutes)

**Do this:** Nothing on the screen. Write two things on the board, in two columns:

```text
        WEEKS 1 to 27              TODAY
        X   (the table)            X   (the table)
        y   (the answers)
```

**Say this:**

> "For twenty-seven weeks, every single thing we have built has had two halves. A table of measurements, and a column of right answers. Pizza deliveries and whether they were late. Digits and which digit they were. Fraud and whether it was fraud.
>
> And *every* number we used to say whether we were any good — accuracy, precision, recall, AUC, log loss, every one of them — worked by comparing our guess to the right answer.
>
> Today I am taking the right answers away. Permanently. Term 4 starts here, and this half of the board" — point at the empty space under `y` — "**stays empty.**"

**Ask this:** "So what breaks?"

*Take several answers. You want at least one of: "we can't tell if it's right", "there's nothing to compare to", "accuracy doesn't mean anything any more".*

> "**All of it breaks.** There is no accuracy, because accuracy is a comparison. There is no overfitting, or at least it is very hard to even say what it would mean. There is no right answer for any individual row.
>
> What you can still do is **find structure.** And that is what this term is about."

**Do this:** Hold up a shoebox, or just mime one.

**Say this:**

> "Five hundred Lego bricks in a box. I hand it to you and say: sort these.
>
> By colour? By size? By shape? By which set they came out of?"

**Ask this:** "Which of those is the right answer?"

*Hoped-for:* none of them / all of them / it depends.

> "**None of them is right and all of them are valid, and there is no key at the back of the book.** What you *can* do is defend your choice: *I sorted by shape, because the piles came out about even, the bricks inside each pile really do look alike, and shape is what matters if you want to build something.*
>
> Notice what that is. It is not a score. **It is an argument.** For the rest of this term, when you finish an unsupervised job, the thing you hand in is an argument with numbers in it."

**Do this:** Now walk to the six taped crosses on the floor.

**Say this:**

> "Six points. That is all the data there is. No labels, no answers, nothing else.
>
> I want you to split them into two groups."

**Ask this:** "Somebody tell me the two groups."

*They will get it instantly: A, B, C and D, E, F. That is the point.*

> "You did that in about a second and a half, and you did it by eye. **Now I want an algorithm that does it, because your eye does not work on 178 wines with thirteen measurements each, and it really does not work on forty thousand supermarket customers.**
>
> The algorithm has two steps. Two. And you are going to do it standing on that floor in about twenty minutes."

---

### 🧠 Concept & Maths — Assign, Move, Repeat, and One New Symbol (18 minutes)

**Do this:** Write the four lines on the board and box them. Leave them up for the whole lesson.

```text
1. Put down k centres, anywhere.
2. ASSIGN : give every point to its nearest centre.
3. MOVE   : put every centre in the middle of what it got.
4. Back to 2. Stop when nobody changed cluster.
```

**Say this:**

> "That is the whole algorithm. It is called **k-means**, and the `k` is just the number of groups you asked for — you choose it, the algorithm never does.
>
> Two words you need. A **cluster** is a group of points more like each other than like anything outside. A **centroid** is the average position of everything currently in a cluster — its centre of gravity. If a cluster holds (1, 2) and (2, 1), its centroid is at 1.5, 1.5. You have been computing averages since Week 1; that is all a centroid is."

**Do this:** Draw the food-truck picture — a rough park, three trucks, dots for picnickers.

**Say this:**

> "Three food trucks, a park full of picnickers. **Round one:** every picnicker walks to the nearest truck. **Round two:** each truck looks at where its own customers are sitting and drives to the middle of them. **Round three:** some picnickers notice a different truck is now closer and switch. Trucks move again.
>
> After a few rounds nobody switches, the trucks stop, and you have three neighbourhoods **that nobody designed.** That is k-means, and that is all of it."

**Do this:** Now the arithmetic, at the SIX POINTS sheet. Write the points, then the two starting centres.

```text
A = (1, 2)   B = (2, 1)   C = (2, 3)   D = (8, 8)   E = (9, 7)   F = (7, 9)

centre 1 starts at (1, 2)        centre 2 starts at (2, 3)
```

**Say this:**

> "I have put both starting centres in the left-hand bunch **on purpose**, and one of them is sitting exactly on top of C. You will see why in a minute, and it is the most interesting thing that happens today.
>
> One more rule, and it is a gift: **we never take a square root.** 'How far, squared' is the across-gap squared plus the up-gap squared, and that is enough, because squaring does not change which centre is nearer. It just saves you about forty square roots."

**Do this:** Work three rows of the round-1 table on the board, out loud, and let the class do the rest.

```text
A (1,2):  to (1,2) -> 0 + 0 = 0      to (2,3) -> 1 + 1 = 2      centre 1
B (2,1):  to (1,2) -> 1 + 1 = 2      to (2,3) -> 0 + 4 = 4      centre 1
C (2,3):  to (1,2) -> 1 + 1 = 2      to (2,3) -> 0 + 0 = 0      centre 2
```

**Ask this:** "C is sitting right next to A and B. Why on earth did it go with centre 2?"

*Hoped-for answer:* because centre 2 is sitting on top of it, so the distance is zero.

> "**Exactly. Zero beats two.** The algorithm is not being stupid — it is doing precisely what we told it with a stupid starting position. Remember this moment; it comes back."

**Do this:** Have them call out D, E and F. Write the groups.

```text
centre 1 got {A, B}          centre 2 got {C, D, E, F}
```

**Ask this:** "Now the MOVE step. Where does centre 1 go?"

*Hoped-for:* the middle of A and B.

```text
centre 1 = ( (1+2) ÷ 2 , (2+1) ÷ 2 ) = ( 1.5 , 1.5 )
centre 2 = ( (2+8+9+7) ÷ 4 , (3+8+7+9) ÷ 4 ) = ( 26÷4 , 27÷4 ) = ( 6.5 , 6.75 )
```

**Ask this:** "Centre 2 was at (2, 3) and it has jumped to (6.5, 6.75). Why did it move so far?"

*Hoped-for:* because it got four points and three of them are miles away.

> "**It got dragged.** One nearby point and three distant ones, and the average lands out in the middle of the distant ones. Now watch what that does to C."

**Do this:** Do C's round-2 row in full, slowly, on the board.

```text
C (2,3):  to (1.5, 1.5)  -> 0.25 +  2.25   =  2.50
          to (6.5, 6.75) -> 20.25 + 14.0625 = 34.3125
```

**Ask this:** "Which is smaller?"

*2.50.*

> "**C comes home.** It switched sides, and the algorithm repaired its own bad start in exactly one round. That is the whole reason I started both centres on the left — so you could see it fix itself."

**Do this:** Now inertia. Write the definition, then the six numbers.

> **Inertia** — add up the squared distance from every point to its own centre. Smaller means tighter.

```text
0.4444 + 1.1111 + 1.1111 + 0.0000 + 2.0000 + 2.0000  =  6.6667
```

**Say this:**

> "Six numbers, one addition. And now the one new piece of notation in the whole of Term 4, because you are going to meet it in every book you ever open."

**Do this:** Write, large:

```text
      Σ
```

**Say this:**

> "That is the Greek capital letter S. It stands for **Sum**, and it means exactly this and nothing else: **add up all of these.**
>
> It does not multiply. It does not do anything clever. There is no hidden step inside it. Somebody wrote `Σ` because writing out forty thousand numbers is annoying.
>
> And here is our rule, for this week and the next four: **every single time you see that symbol, write the sum out beside it.**"

**Do this:** Write it out, on the board, beside the symbol.

```text
Σ (distance to my own centre)²
       =  0.4444 + 1.1111 + 1.1111 + 0.0000 + 2.0000 + 2.0000
       =  6.6667
```

**Ask this:** "If I had 178 wines instead of six points, how many numbers would be in that sum?"

*178.*

> "**178, and I would still not write them out — but you would still know exactly what the symbol was asking for.** That is the only thing the symbol is for."

**Ask this:** "Last one. Inertia is the number k-means makes small. So if I want the smallest possible inertia, what `k` should I ask for?"

*Take answers. Somebody will say a big number. Steer to: one cluster per point.*

> "**One cluster per point.** Every point sits exactly on its own centre, every distance is 0, and inertia is 0. **Perfect score, zero information.** Which is why 'pick the smallest inertia' is the most common mistake in this entire subject, and why choosing `k` needs something else. We start on that at the end of today and finish it in two weeks."

---

### 💻 Live-Code Together — `no_answer_key.py` (18 minutes)

**Do this:** Empty file. They type; you type on the shared screen. Say every line out loud as it goes in.

**Step 1 — the six points and our exact starting centres (4 minutes).**

```python
import numpy as np
from sklearn.cluster import KMeans

X = np.array([[1., 2.], [2., 1.], [2., 3.],
              [8., 8.], [9., 7.], [7., 9.]])
init = np.array([[1., 2.], [2., 3.]])       # centre 1 on A, centre 2 on C

km = KMeans(n_clusters=2, init=init, n_init=1, random_state=0)
print(km.labels_)
```

> **🧑‍🏫 Deliberate mistake one.** That last line is wrong and you are running it anyway. **Do not warn them.**

```text
AttributeError: 'KMeans' object has no attribute 'labels_'
```

**Ask this:** "It says the object has no attribute `labels_`. But I wrote `KMeans`. What did I not do?"

*Hoped-for:* you never ran it / never called `.fit`.

> "**I built the machine and never switched it on.** And here is the rule that error is teaching you, and it is worth writing in the Bug Log:
>
> **In scikit-learn, a name that ends in an underscore did not exist until you called `.fit`.** `labels_`, `cluster_centers_`, `inertia_` — every one of them. The underscore is not decoration, it is a promise about when the thing appears."

**Do this:** Fix it in front of them by adding `.fit(X)`, and add the other three prints.

```python
km = KMeans(n_clusters=2, init=init, n_init=1, random_state=0).fit(X)
print("labels        :", km.labels_)
print("centres       :", np.round(km.cluster_centers_, 4).tolist())
print("inertia       :", round(km.inertia_, 4))
print("rounds counted:", km.n_iter_)
```

```text
labels        : [0 0 0 1 1 1]
centres       : [[1.6667, 2.0], [8.0, 8.0]]
inertia       : 6.6667
rounds counted: 3
```

**Do this:** Stand beside the board where the hand-worked answers already are. Point at each one in turn.

**Ask this:** "Centres?"

*(1.6667, 2.0) and (8, 8) — the same.*

**Ask this:** "Inertia?"

*6.6667 — the same.*

**Ask this:** "Rounds?"

*We said 2. It says 3.*

> "**We are both right.** We counted the rounds that changed something. It also counts the last pass, the one that checked and found nothing had changed. **When a library's counter is one off from yours, check whether it is counting the check.**"

**Step 2 — inertia, added up in front of them (4 minutes).**

```python
names = ["A", "B", "C", "D", "E", "F"]
total = 0.0
for nm, p, lab in zip(names, X, km.labels_):
    c = km.cluster_centers_[lab]
    dx2, dy2 = (p[0] - c[0]) ** 2, (p[1] - c[1]) ** 2
    total += dx2 + dy2
    print("  %s (%g,%g) to centre %d: %.4f + %.4f = %.4f"
          % (nm, p[0], p[1], lab, dx2, dy2, dx2 + dy2))
print("  all six added up:", round(total, 4))
print("  km.inertia_     :", round(km.inertia_, 4))
```

```text
  A (1,2) to centre 0: 0.4444 + 0.0000 = 0.4444
  B (2,1) to centre 0: 0.1111 + 1.0000 = 1.1111
  C (2,3) to centre 0: 0.1111 + 1.0000 = 1.1111
  D (8,8) to centre 1: 0.0000 + 0.0000 = 0.0000
  E (9,7) to centre 1: 1.0000 + 1.0000 = 2.0000
  F (7,9) to centre 1: 1.0000 + 1.0000 = 2.0000
  all six added up: 6.6667
  km.inertia_     : 6.6667
```

**Say this:**

> "**Those six lines are the sigma. That is the whole symbol, printed one term at a time.** And the last two lines are the same number twice — mine and theirs. You can check `km.inertia_` by hand, on six points, and you just did."

**Step 3 — the wine data, and a silent mistake (7 minutes).**

```python
import pandas as pd
from sklearn.datasets import load_wine

wine = load_wine()
X_raw = pd.DataFrame(wine.data, columns=wine.feature_names)
print("wine table:", X_raw.shape)

km_raw = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X_raw)
print("sizes", np.bincount(km_raw.labels_), " inertia %.1f" % km_raw.inertia_)
```

```text
wine table: (178, 13)
sizes [69 47 62]  inertia 2370689.7
```

> **🧑‍🏫 Deliberate mistake two, and this one never errors.** **Be visibly pleased with that output.** *"Three clusters, 69 and 47 and 62 — nicely balanced. Thirteen chemical measurements, and a machine that has never tasted wine just found three groups of them."* **Let it sit for a few seconds.**

**Ask this:** "How do we know those groups are anything at all?"

*Let them flounder for a moment. Somebody may say "we don't."*

> "We do not. So let us look at what is actually inside them."

```python
pro = X_raw["proline"].values
for c in range(3):
    m = km_raw.labels_ == c
    print("cluster %d: n=%3d  proline %4.0f to %4.0f" % (c, m.sum(), pro[m].min(), pro[m].max()))
```

```text
cluster 0: n= 69  proline  278 to  590
cluster 1: n= 47  proline  970 to 1680
cluster 2: n= 62  proline  600 to  937
```

**Ask this:** "278 to 590. 600 to 937. 970 to 1680. What do you notice about those three ranges?"

*Hoped-for:* they don't overlap at all.

**Ask this:** "So what have our thirteen-column clusters actually sorted the wine by?"

*Hoped-for:* proline. One column.

```python
print(X_raw.std().sort_values(ascending=False).round(2).head(4).to_string())
```

```text
proline              314.91
magnesium             14.28
alcalinity_of_ash      3.34
color_intensity        2.32
```

> "**There it is, and we could have known before we ran anything.** `proline`'s spread is 314.91. `flavanoids`' is 1.00. Distance squares those gaps, so proline contributes about ninety-nine thousand times more to every measurement of 'how far apart are these two wines'. **Twelve of the thirteen columns were never consulted. Nothing errored. We just measured wine in proline.**"

**Do this:** Fix it, and print the fix.

```python
from sklearn.preprocessing import StandardScaler
Xs = StandardScaler().fit_transform(X_raw)
km_sc = KMeans(n_clusters=3, n_init=10, random_state=0).fit(Xs)
print("SCALED sizes", np.bincount(km_sc.labels_), " inertia %.1f" % km_sc.inertia_)
```

```text
SCALED sizes [65 51 62]  inertia 1277.9
```

**Ask this:** "The inertia went from 2,370,689.7 to 1,277.9. Did the clustering get two thousand times better?"

*Hoped-for:* no — the units changed.

> "**No. We changed the ruler, so we changed the number.** Inertia is in whatever units your table is in. You may compare two inertias from the same table measured the same way. **You may never compare an inertia across a change of units, and that is exactly the Week 27 rule about naming the pile, wearing a different hat.**"

---

### 🎲 Their Turn — k-Means on the Floor (20 minutes)

Full instructions in **🎲 The Activity, In Full** below. In outline: **six points taped to the floor and two volunteers standing as centres.** Two full rounds done by hand, with **every one of the twenty-four squared distances written on the board** by the class, the centres physically walking to their new average positions, and C visibly changing sides in round two. Then the same six points through `KMeans` with the identical starting centres, so the printout matches the board line for line.

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Stand at the board with the three customers written on it.

```text
P1 = (25, 500000)        P1 to P2 :    900
P2 = (55, 500000)        P1 to P3 :    400,000,000
P3 = (25, 520000)
```

**Ask this:** "P1 and P2 are thirty years apart in age. P1 and P3 differ by a 4% pay rise. Which pair does raw k-means think is more alike?"

*P1 and P2.*

**Ask this:** "By how much?"

```text
400000000 ÷ 900 = 444444
```

> "**Four hundred and forty-four thousand times.** Thirty years of a human life, against a 4% pay rise, and the algorithm says the pay rise is the bigger difference by a factor of nearly half a million.
>
> That is not a bug. **That is what the word 'distance' means when your columns are in different units.** And notice the age column has not been *weakened*. It has been **deleted**: 900 against 400 million is a rounding error."

**Do this:** Write the standardised numbers under them.

```text
P1 to P2 : 4.5          P1 to P3 : 4.5
```

> "**Exactly equal. Which is the honest answer** — each pair differs by the same amount in one column and not at all in the other. Same three customers. Same algorithm. Opposite conclusion, decided entirely by the ruler.
>
> So the rule, and write it down: **always scale before k-means.** Not because scaling is good hygiene. Because otherwise your biggest column is the only column."

**Do this:** Now the reveal, and be careful with it. Put the last block of output up.

```text
rows = the real grape variety, columns = the cluster we found
SCALED
 [[ 0  0 59]
 [65  3  3]
 [ 0 48  0]]
```

**Ask this:** "Rows are the real grape varieties, which I have not shown you until this second. Columns are the clusters we found. What do you see?"

*Hoped-for:* each row has almost everything in one column.

> "**59 in one place, 65 in one place, 48 in one place. Six bottles out of 178 in the wrong pile.** An algorithm that has never seen a grape, never been told there were three varieties, and was handed thirteen numbers per bottle, recovered the three real varieties almost exactly.
>
> And now the part I want you to take home, because it is more important than the result." **Pause here.**
>
> "**We only got to check because somebody had already labelled these bottles and I was hiding it from you.** On the supermarket data, on the customer data, on anything you will actually be asked to do — **there is no drawer to open.** The clusters are all you get.
>
> Which means k-means will hand you three groups **whatever you feed it.** Feed it 178 rows of pure random numbers and it returns three tidy clusters with sizes 62, 44 and 72, and you will be able to think of names for them. **So the entire burden of proof is on you**, and building that proof is what the next two weeks are."

**Do this:** Three quick checks — exact wording in **✅ Assessing Understanding**.

**Say this, to close:**

> "Two steps. Assign, then move. You did it on a floor with masking tape and you got the same centres, the same inertia and the same switching point as a library that has been optimised for fifteen years.
>
> And you met one symbol, `Σ`, which turned out to mean 'add these up'.
>
> Next week: **PCA**, which does not delete any of your thirteen columns — it draws a new pair of axes through them."

**Do this:** Hand out the homework and read the second part out loud.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `AttributeError: 'KMeans' object has no attribute 'labels_'` | "You never ran it." | `KMeans(...)` built, `.fit(X)` never called. | Add `.fit(X)`. **And learn the rule: a scikit-learn name ending in `_` does not exist until `.fit` has run.** |
| `ValueError: Expected 2D array, got 1D array instead: array=[1. 2. 3. 8. 9. 7.].` `Reshape your data either using array.reshape(-1, 1) if your data has a single feature or array.reshape(1, -1) if it contains a single sample.` | "You gave me a list of numbers, not a table of rows and columns." | One flat list instead of a list of `[x, y]` pairs. | `X` must be rows-by-columns. **The message even tells you which reshape you want — `(-1, 1)` if each number is its own row.** |
| `ValueError: n_samples=6 should be >= n_clusters=8.` | "You asked for more groups than you have things." | `n_clusters` typed bigger than the number of rows, usually a typo. | `n_clusters` can never exceed the number of rows. **And at `n_clusters` = rows, inertia is exactly 0, which is why that is never what you want.** |
| `ValueError: could not convert string to float: 'cheese'` | "One of your columns is words." | A text column left in the DataFrame. | k-means measures distance, and there is no distance between `'cheese'` and `'olive'`. Drop the column, or one-hot encode it as in Week 4. |
| `ValueError: Input X contains NaN.` `KMeans does not accept missing values encoded as NaN natively.` | "There is a hole in your table." | Missing values never filled in. | `SimpleImputer(strategy="median")` from Week 6, **inside a pipeline**. There is no distance to a hole. |
| `ValueError: The shape of the initial centers (1, 2) does not match the number of clusters 2.` | "You asked for 2 groups and handed me 1 starting centre." | `init=` array with the wrong number of rows. | The `init` array must be `(n_clusters, n_features)`. **Print its shape before you pass it — Week 16's habit and it still pays.** |
| `ValueError: X has 3 features, but KMeans is expecting 2 features as input.` | "You fitted on two columns and are now asking about three." | `km.predict` on a differently-shaped table. | Same columns in, same order, always. |
| `InvalidParameterError: The 'n_clusters' parameter of KMeans must be an int in the range [1, inf). Got '3' instead.` | "You gave me the *text* three, not the number three." | Quotes round the number: `n_clusters="3"`. | Drop the quotes. **Read the message's last two words — it prints `'3'` with quotes, which is the clue.** |
| **No error. The clusters sort one column into bands.** | Nothing crashed. You clustered on your biggest column. | No scaling, so the widest-ranging column decided every distance. | `StandardScaler`. **And the check that finds it: print the per-cluster min and max of your widest column. Non-overlapping bands is the fingerprint.** |
| **No error. Inertia dropped from 2,370,689.7 to 1,277.9 and it looks like a huge win.** | Nothing crashed. You changed the units. | Comparing an inertia before scaling with one after. | Inertia is in your table's units. **Only ever compare inertias measured on the same table, the same way.** |
| **No error. Cluster 0 means something different every time you re-run.** | Nothing crashed. Cluster numbers are arbitrary names. | Expecting `0` to be stable across seeds. | Compare *groupings*, not numbers. **And never do arithmetic on a cluster ID — it is a name, like "Mumbai".** |
| **No error. You asked for 7 clusters on 6 obvious groups and got 7.** | Nothing crashed. k-means always gives you exactly what you asked for. | Believing the algorithm can tell you `k`. | It cannot, ever. **The elbow, and Week 30's silhouette, are evidence you gather. `k` is your decision.** |

### How to teach debugging without giving the answer

All the old moves stand. This week adds three.

26. **"Did you call `.fit`?"** It will be the answer about a third of the time this term. The trailing underscore is the tell.

27. **"What are the biggest and smallest values in each of your columns?"** One printout, and it predicts every scaling disaster before it happens. **If one column's spread is a hundred times another's, that column is your entire model.**

28. **"You got clusters. What would you have got if the data were random?"** The most useful question in unsupervised learning, and it is the one nobody asks. **The honest answer is: three tidy clusters, with names you could invent.**

And the sentence for this week:

> **"An algorithm that always returns an answer has told you nothing by returning one. k-means gives you three clusters from noise just as happily as from wine, so a cluster is a claim, and a claim needs evidence."**

---

## 🎲 The Activity, In Full

This section is the full script for the floor activity, step by step.

### k-Means on the Floor (20 minutes)

**What it is.** Six points taped to the floor. Two students stand on them as the centres. The class does two complete rounds of assign-and-move, out loud, with every squared distance written on the board, and then the same run goes through `KMeans` and matches line for line.

**Why it is worth twenty minutes.** The two steps are trivially easy and almost impossible to *believe* from a printout. A student who has stood on the floor as centre 2, been dragged out to (6.5, 6.75) by three distant points, and then watched C walk away from them, will never need the algorithm explained again.

### Setup

- **Tape six crosses to the floor** before the class arrives. Use one metre per unit if you have the room, or 40 cm per unit if you do not. The layout, with (0,0) in a corner:

```text
      y
   9  |                           F
   8  |                              D
   7  |                                 E
      |
   3  |     C
   2  |  A
   1  |     B
      +-----------------------------------  x
         1  2                  7  8  9
```

- **A letter card beside each cross**: A, B, C, D, E, F.
- **Two more cards**, CENTRE 1 and CENTRE 2, for the two volunteers to hold.
- **The board, ruled into two tables** of six rows and three columns: `point | to centre 1 | to centre 2`. One table for round 1, one for round 2.
- **Workbook page 28.3** open on every desk — the same two tables, to fill in as the class goes.
- Three colours of pen each.

### Step 1 — put the centres in the wrong place (2 minutes)

Two volunteers. **CENTRE 1 stands on A. CENTRE 2 stands on C.**

> **Say this:** "Both centres in the left-hand bunch, and centre 2 standing on top of a point. This is a bad start and I have done it on purpose."

**One rule, said out loud and repeated once:** **the six points never move. Only the two centres move.** Without that rule the activity becomes a milling crowd in ninety seconds.

### Step 2 — round 1, assign (5 minutes)

Go point by point. For each point the class computes **two** squared distances and the nearer one wins. Write every one on the board; they write them on 28.3 in colour one.

```text
A (1,2):  to (1,2) -> 0 + 0 = 0       to (2,3) -> 1 + 1 = 2       centre 1
B (2,1):  to (1,2) -> 1 + 1 = 2       to (2,3) -> 0 + 4 = 4       centre 1
C (2,3):  to (1,2) -> 1 + 1 = 2       to (2,3) -> 0 + 0 = 0       centre 2
D (8,8):  to (1,2) -> 49 + 36 = 85    to (2,3) -> 36 + 25 = 61    centre 2
E (9,7):  to (1,2) -> 64 + 25 = 89    to (2,3) -> 49 + 16 = 65    centre 2
F (7,9):  to (1,2) -> 36 + 49 = 85    to (2,3) -> 25 + 36 = 61    centre 2
```

**Do this:** As each point is decided, the student standing nearest it (or a slip of paper on the cross) gets a coloured sticker or a card matching its centre. **Membership has to be visible in the room.**

> **Ask this:** "C is one step from A and B. Why is it with the far group?"

*Because centre 2 is standing on it, so its distance is zero.*

### Step 3 — round 1, move (3 minutes)

> **Ask this:** "Centre 1, you got A and B. Where do you walk to?"

```text
( (1+2) ÷ 2 , (2+1) ÷ 2 ) = ( 1.5 , 1.5 )
```

They take half a step. Then centre 2:

```text
( (2+8+9+7) ÷ 4 , (3+8+7+9) ÷ 4 ) = ( 26÷4 , 27÷4 ) = ( 6.5 , 6.75 )
```

**They have to walk a long way, across the room, and everybody should watch them do it.**

> **Ask this:** "Centre 2, why did you just have to walk five metres?"

*Because three of my four points were over there.*

> **Say this:** "One nearby point and three distant ones, and the average lands out among the distant ones. **The centre got dragged.** Now, C — is that person still your nearest centre?"

### Step 4 — round 2, and the switch (6 minutes)

Same procedure, colour two on the sheet. Do C first this time, for the drama:

```text
C (2,3):  to (1.5, 1.5)  -> 0.25 + 2.25   = 2.50
          to (6.5, 6.75) -> 20.25 + 14.06 = 34.31        centre 1  -- SWITCHED
```

**C physically changes its card, in front of everybody.** Then finish the other five:

```text
A (1,2):  0.50 vs 52.81     centre 1
B (2,1):  0.50 vs 53.31     centre 1
D (8,8):  84.50 vs 3.81     centre 2
E (9,7):  86.50 vs 6.31     centre 2
F (7,9):  86.50 vs 5.31     centre 2
```

Then move again:

```text
centre 1 = ( (1+2+2) ÷ 3 , (2+1+3) ÷ 3 ) = ( 1.6667 , 2.0 )
centre 2 = ( (8+9+7) ÷ 3 , (8+7+9) ÷ 3 ) = ( 8.0 , 8.0 )
```

> **Ask this:** "Round three. Do the maths in your head — would anybody switch?"

*No.*

> **Say this:** "**Then we stop. Two rounds.** And the algorithm fixed its own bad start without being told anything."

### Step 5 — inertia, then the machine (4 minutes)

Six squared distances to their own final centres, written as one sum beside a `Σ`:

```text
0.4444 + 1.1111 + 1.1111 + 0.0000 + 2.0000 + 2.0000  =  6.6667
```

Then run it:

```python
km = KMeans(n_clusters=2, init=np.array([[1., 2.], [2., 3.]]),
            n_init=1, random_state=0).fit(X)
print(km.labels_, np.round(km.cluster_centers_, 4).tolist(), round(km.inertia_, 4))
```

```text
[0 0 0 1 1 1] [[1.6667, 2.0], [8.0, 8.0]] 6.6667
```

**Stand back and let them compare it to the board themselves.**

### What "finished" looks like

- Page 28.3 with **twenty-four squared distances** on it, in two colours, and C ringed as the switcher.
- The two final centres, `(1.6667, 2.0)` and `(8, 8)`, written down and matching the printout.
- Inertia `6.6667`, hand-added, matching `km.inertia_`.
- A student can say, unprompted: **"it only did two things."**
- Somebody has asked why the centres started in a silly place. **That is the best possible outcome.**

### Variation — easier

**Drop to four points and skip round 2.** `A=(1,2)`, `B=(2,1)`, `D=(8,8)`, `E=(9,7)`, with centres starting on A and B. Eight squared distances, one move, done — and the arithmetic is all single digits.

**And give them the distances half-filled.** Pre-print page 28.3 with the *across-gap squared* column already filled in, so the only work is adding the second number and comparing. **Objective 1 is about seeing the loop, not about squaring numbers.**

**The one thing not to cut:** the MOVE step being an average. If a student leaves believing the centre is "somewhere in the middle-ish", they have missed the only computation in the algorithm.

### Variation — harder

1. **Start the centres in the *right* place** — on A and on D — and predict how many rounds it takes. **One.** Then the good question: *"so was our bad start wasted?"* No: it showed you the algorithm repairs itself, which you could not have learned from the easy start.
2. **Find a start that gets it wrong and stays wrong.** With `k=3` it is easy: put all three centres in the left bunch and you get inertia `5.0`, where k-means++ gets `3.6667`. **Then the subtle part: look at what the better answer actually did — it split the right-hand bunch and kept the left one whole.** Lower inertia is not the same as the grouping you would have drawn.
3. **Add a seventh point far away**, say `(20, 20)`, and re-run `k=2`. The real output is `labels [0 0 0 0 0 0 1]`, centres `(4.8333, 5.0)` and `(20.0, 20.0)`. **The outlier has taken an entire cluster for itself, and the two obvious blobs have been merged into one.** k-means has no "none of the above" — every point must belong somewhere, and one extreme point can spend a whole cluster on itself.
4. **Predict the elbow before plotting it.** For the six points, compute inertia by hand at `k` = 1, 2 and 3 and say where the bend is. (`k=1`: centre at (4.8333, 5.0), inertia `120.8333`. `k=2`: `6.6667`. `k=3`: `3.6667`.) The drop from 1→2 is 114.1666; from 2→3 it is 3.0. **A ratio of 38.** That is what a real elbow looks like, and the wine data's 3.9 is much softer.
5. **Run the wine clustering on 178 rows of pure noise** (`np.random.default_rng(0).normal(size=(178, 13))`) and report the cluster sizes. `[62 44 72]`. **Then try to name them.** They will manage it, and that is the finding.

---

## ❓ Questions Students Ask This Week

This section collects questions students ask this week, with answers you can give.

**"How do I know if my clusters are right?"**

**You do not, and that is not a gap in your knowledge — it is a property of the problem.** There is no right answer to compare against. If somebody hands you clusters and a claim that they are correct, they are either hiding a label column or overselling.

What you *can* do is three things, and doing all three is what a professional looks like. **One: measure tightness** — inertia today, the silhouette score in two weeks. **Two: check it survives being jiggled** — re-run with a different seed, re-run on a random 80% of the rows, and see whether the same groups come back. Structure that vanishes when you shake the data was never there. **Three: describe the groups in plain words with numbers attached**, so a human can say whether they make sense. That is Week 30.

And the answer to give out loud: *"you replace 'is it right' with 'here is my evidence, and here is the part I am least sure about'."*

**"Why squared distance? Why not just distance?"**

Three reasons, and the first is the one that matters to you today.

**One: it saves you about forty square roots**, and it cannot change any answer, because if one squared distance is smaller than another then the unsquared one is too. Squaring keeps the order.

**Two: the centroid is exactly the point that makes the sum of squared distances smallest.** That is not a coincidence — it is why the MOVE step is an average rather than something more complicated. If you used plain (unsquared) distance the best centre would stop being the mean: with straight-line distance it is the "geometric median", and with distance measured along the axes it is the ordinary median per column, which is the different algorithm called k-medians.

**Three: squaring punishes one big miss much harder than several small ones.** Being 10 away scores 100; being 1 away five times scores 5. Whether that is what you want is a real design question — and it is the same trade you met with mean squared error back in Week 15.

**"The cluster numbers changed when I re-ran it. Is it broken?"**

No, and this is important. **The numbers are names, not measurements.** Cluster 0 is not smaller, better, first or leftmost. It is the group that happened to be listed first this time.

Re-run with a different seed and the *same three groups* can easily come back as 2, 0, 1. Nothing has changed except the labels. So: **compare groupings, never numbers.** "Are these two runs the same clustering?" is a real question with a real answer, and Week 30 gives you the number that answers it. "Is my cluster 0 the same as last time's cluster 0?" is not a question at all.

And the hard rule that follows: **never do arithmetic on a cluster ID.** Averaging cluster numbers is exactly as meaningful as averaging postcodes.

**"If I have to choose k myself, what is the algorithm even doing for me?"**

Fair, and worth taking seriously. **It is doing the placement, not the counting.** You say "three groups"; it finds *where* those three groups are, in thirteen dimensions, over 178 rows, in a way that is tight, though only guaranteed to be a resting place it reached from where it started, not the tightest possible (that is what `n_init` is for). Try doing that by eye on thirteen columns.

But you are right that the honest description of k-means includes "and you have to supply the most important number yourself". That is a genuine weakness of the method, not a teaching simplification. Some algorithms do choose their own number of groups — and they choose it by being handed a *different* dial to set instead. **There is no method that requires no decisions from you. There are only methods that hide which decision you are making.**

**"Can I use k-means on the pizza data from Term 1, which had text columns?"**

Only after you turn the text into numbers, and then only carefully. k-means measures distance, and there is no distance between `'cheese'` and `'olive'`. Leave a text column in and you get `ValueError: could not convert string to float: 'cheese'`.

One-hot encoding (Week 4) gets you numbers, and then a new problem arrives: a one-hot column is 0 or 1, so its spread is small, while `distance_km` might run to 20. **Scaling matters even more once you have mixed column types, not less.** And there is a real argument that Euclidean distance over one-hot columns is a slightly odd thing to compute in the first place — two different toppings are always exactly √2 apart, no matter how similar they are as toppings. It works, people do it, and it is worth knowing it is a compromise.

**"178 wines, and it got all but six right. Does that mean clustering is basically as good as a proper classifier?"**

**No, and this is the most important misreading available today, so it is worth being blunt.**

Three things were true and all three helped us. The wine dataset is **small, clean, and almost comically well separated** — three grape varieties with genuinely different chemistry. We chose `k = 3`, and we chose it because we already knew there were three varieties. And we scaled, which we only knew to do because we had been told to.

Change any one of those and it falls over. Ask for `k = 5` and you get five groups that cut the three varieties into arbitrary extra pieces. Do not scale, and you sort by proline. **And on the supermarket customer data from the hook, there is no "correct" number of customer types at all**, so there is nothing to get right or wrong.

A classifier trained on labels gets to learn *exactly* what distinguishes the varieties. Clustering has to hope that "different variety" happens to be the biggest source of variation in the table. **Here it was. That was luck, and it was checkable luck, which is rarer still.**

**"Should you ever cluster people?"** *(Nobody fully agrees, and here is why.)*

**This one has no settled answer, and the disagreement is genuinely worth a 14-year-old's attention.**

**The case for.** Every organisation that serves millions of people has to group them somehow — you cannot design a product for each individual. Clustering does it from evidence rather than from somebody's prejudice about who their customers are. That is a real improvement on the alternative, which is usually a marketing director's hunch.

**The case against.** The moment you name a cluster, you have turned a fuzzy statistical boundary into a thing people treat as a fact about the world. Call 65 wines "Light & Pale" and nothing happens. Call 65,000 people "Low-Value Customers" and within a year there are products designed for them, prices set for them, and a support queue they get put in. **The group did not exist before you named it, and then it does — because you named it.**

**And the sharper version of the objection.** k-means has no "none of the above". Every single row must join a cluster, so the person who fits nowhere gets filed with whoever they are least unlike, and then *drags that cluster's centre towards themselves*. On a wine that is a curiosity. On a person being sorted into a category that decides their insurance premium, it is not.

**The position most practitioners actually hold**, and it is a compromise rather than a principle: cluster people for *description* — understanding who you are serving — and be extremely careful about clustering them for *decisions* that affect them individually. The trouble is that the description has a way of becoming the decision, because the cluster is sitting right there in a database column, and the next engineer along does not know it was only ever meant to be descriptive.

What to say out loud to a 14-year-old: **"the same code sorts bottles and people, and the code does not know the difference. You do. So before you cluster anything, ask what happens to the row that does not fit anywhere — and if the answer involves a real person, slow down."**

---

## ⚠️ Where This Lesson Goes Wrong

This section names the usual ways the lesson goes off course, and what to do about each.

| What happens | Why | What to do right now |
|---|---|---|
| **The wine reveal turns clustering into a success story** | `172 of 178` is a genuinely impressive number and the room will react to it | **Spend the next thirty seconds taking it back.** *"We only got to check because somebody had already labelled these bottles."* The reveal is a demonstration that the method *can* work, not evidence that it *did* in any case where you cannot check. **If you only say one thing after the reveal, say that the drawer usually does not exist.** |
| The floor activity becomes a crowd milling about | Everybody starts walking | **Say the rule before you start and repeat it once: the points never move. Only the two centres move.** Points can be slips of paper on the crosses if the room is lively. |
| Round 2 gets summarised instead of computed | There are twelve more squared distances and the clock is at minute 55 | **Compute C, at minimum, in full, out loud.** `2.50` against `34.31` is the entire lesson. If you must skip five rows, skip A, B, D, E and F — never C. |
| The scaling demo lands as "scaling is good practice" | It is phrased as a rule in every textbook | **Never say "scaling is good practice" today.** Say `444,444`. Say `278–590, 600–937, 970–1680`. **The rule is a conclusion drawn from two numbers, and only the numbers stick.** |
| Sigma gets skipped because it looks like decoration | It is one symbol in a lesson with an activity to fit in | **It is this week's entire new maths and it recurs in Weeks 29, 30 and 32.** Two minutes: the letter S, "add up all of these", and the six-term sum written beside it. **Skipping it means Week 29's variance formula arrives with no scaffold.** |
| A student picks `k` by minimising inertia and nobody catches it | It is the obvious thing to do with a number you are told is "better when smaller" | **Ask the question in the Concept segment and let them walk into it:** *"so what k gives the smallest inertia?"* One cluster per point, inertia 0. **Discovering it is worth ten times being warned about it.** |
| The two inertias, 2,370,689.7 and 1,277.9, get compared | They are printed six lines apart and both are called inertia | **Ask the illegal comparison out loud yourself** — *"so scaling made it two thousand times better?"* — and let them catch it. Same discipline as Week 27's table: **a number means nothing without its units and its pile.** |
| Cluster IDs get treated as values | `0`, `1`, `2` look like numbers because they are | Say *"they are names, like Mumbai and Delhi"* the first time they appear, and again when the wine clusters come up. **The contingency table at the end proves it: cluster 2 is variety 0.** |
| The lesson runs out of time in the wrap | There is a floor activity and two datasets in seventy minutes | **The least cuttable things are the floor round 2 and the `444,444`.** If you are behind at minute 60, cut the wine reveal entirely and hand it to the homework — **but never cut the scaling flip, which is objective 4.** |
| A student concludes k-means is useless because it cannot be checked | It is an uncomfortable position and 14-year-olds are allergic to vagueness | **Agree with the discomfort, then redirect it.** *"You are right that you cannot mark it. That is why the deliverable is an argument. In two weeks you will build one, and it will have five pieces of evidence in it."* |

---

## 🧭 Differentiation

This section says how to adjust the lesson for different students.

### If the student is struggling

**Cut:** `k = 3` and the local-minimum demo entirely. Two clusters, one bad start, two rounds. That is objectives 1, 2 and 3.

**Cut:** the wine elbow table. **Keep the proline ranges** — they are three pairs of numbers and they carry objective 4 on their own.

**Cut:** round 2 for A, B, D, E and F. **Do C in full.** One row, done properly, is the lesson.

**Give them `no_answer_key.py` complete.** Every bit of today's learning is in the hand arithmetic and in reading three number ranges off a screen. **None of it is in typing `StandardScaler`.**

**The version of the maths that skips the algebra.** No formula, no sigma symbol, no minus signs. Two questions and a table:

| point | how far to centre 1 (across² + up²) | how far to centre 2 | which is smaller? |
|---|---|---|---|
| A (1,2) | 0 + 0 = 0 | 1 + 1 = 2 | |
| B (2,1) | 1 + 1 = 2 | 0 + 4 = 4 | |
| C (2,3) | 1 + 1 = 2 | 0 + 0 = 0 | |

> **"Fill in the last column. Then tell me which group each point is in."**

**That is the assign step, complete, with no notation whatsoever.** Then one more instruction — *"add up the two points in group 1 and halve it"* — and that is the move step. **Objective 1, delivered with addition and halving.**

**The copy-this-exactly scaffold.** Nine lines, runs on its own, and it proves the scaling point without a single new idea:

```python
import numpy as np

P1 = np.array([25., 500000.])
P2 = np.array([55., 500000.])
P3 = np.array([25., 520000.])
print("P1 to P2, squared:", ((P1 - P2) ** 2).sum())
print("P1 to P3, squared:", ((P1 - P3) ** 2).sum())
print("ratio            :", ((P1 - P3) ** 2).sum() / ((P1 - P2) ** 2).sum())
```

```text
P1 to P2, squared: 900.0
P1 to P3, squared: 400000000.0
ratio            : 444444.44444444444
```

Then two questions and nothing else: **"which two people are more alike, according to that? and do you agree?"** **P1 and P2, and no** — thirty years of age against a 4% pay rise. **Objective 4's whole understanding in nine lines.**

**One thing you must not cut:** the MOVE step being an average of the points a centre got. Everything else today can be shortened.

### If the student is flying

None of these need syntax from a later week.

1. **The `k=3` local minimum** (Variation-harder 2). Inertia `5.0` from a crowded start against `3.6667` from k-means++. **And then the subtle part: the better answer split the right-hand bunch. Lower inertia is not "the grouping you wanted", and noticing that is a level-5 observation.**
2. **Add an outlier at (20, 20)** and watch a centre get captured (Variation-harder 3). Then: *"k-means has no 'none of the above'. What would you do with a row that belongs nowhere?"* **There is no answer in the algorithm, which is the finding.**
3. **The noise control** (Variation-harder 5). `[62 44 72]` clusters from pure random numbers. **Then name them.** They will succeed, and that is the point. This is a genuine preview of Week 30's best moment.
4. **Predict the six-point elbow by hand** (Variation-harder 4): inertia `120.8333`, `6.6667`, `3.6667`, drop ratio **38**. Then compare with the wine data's **3.9** and say which dataset has clearer structure, and why.
5. **Find the smallest change to the six points that makes k-means get it wrong.** Move one point and re-run. **There is a real answer and hunting for it teaches more about the algorithm's blind spots than any explanation.**
6. **Cluster the wine data on `proline` alone**, one column, `k=3`, and compare the labels with the unscaled thirteen-column run. **They are identical — all 178 rows, cluster for cluster.** That is the cleanest possible proof of the scaling point and it is a two-line experiment.

### If the student won't engage today

**Close the laptop. Masking tape and two shoes.**

Tape four crosses on the floor: `(1,2)`, `(2,1)`, `(8,8)`, `(9,7)`. Put one shoe on `(1,2)` and one shoe on `(2,1)` as the two centres. Then three instructions, and nothing else:

> **"Which shoe is nearest to the point at (8,8)? Don't calculate. Just look."**
>
> **"Right. Now put every point with its nearest shoe. Say the four out loud."**
>
> **"Now pick up each shoe and put it in the middle of its own points."**

That is one full round of k-means, done with footwear, in four minutes, and **it is objective 1's entire understanding.** If they will take one more, ask: **"would anything change if we did it again?"** No. **They have just discovered convergence.**

If they will take a third, do the ruler question with no numbers at all:

> **"Two people. One is thirty years older than the other. One earns twenty thousand rupees more. Which pair is more different?"**
>
> **"Now: the computer adds up the gaps. 30 against 20,000. Which one does it notice?"**

**The money, and it is not close.** That is objective 4, discovered with two sentences and no arithmetic.

The rest survives. This is the gentlest week of Term 4 and there is room to lose some of it.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the two steps, in their own words (spoken, 60 seconds)**

> "Describe k-means to me as if I have never heard of it. **You have two sentences.**"

*Good answer:* "Give every point to its nearest centre. Then move every centre to the middle of the points it got. Repeat until nobody changes, and that's it."

**What to catch:** any answer with three or more steps in it, or the word "learns". **Push once:** *"which of those steps is not in the algorithm?"* **Full marks needs MOVE described as an average, not as "adjusts" or "improves".**

**Check 2 — sigma, and inertia (written, 90 seconds)**

> "Write down what `Σ` means, in plain words. **Then write out the sum for our six points in full, and give me the total.**"

*Good answer:* "It means add up all of these. `0.4444 + 1.1111 + 1.1111 + 0.0000 + 2.0000 + 2.0000 = 6.6667`."

**What to catch:** a student who writes the symbol again instead of the sum, or who cannot say what the six numbers *are*. **They are each point's squared distance to its own centre.** **A student who adds the six numbers and gets 6.6667 without looking it up is at level 3 on this objective.**

**Check 3 — the ruler (spoken, 90 seconds)**

> "I clustered 178 wines on thirteen chemical measurements and got three tidy groups. **Then I looked inside them and their `proline` values were 278–590, 600–937 and 970–1680. What happened, and how could I have predicted it before running anything?**"

*Good answer:* "You didn't scale, so proline decided every distance — its spread is 314.91 and most of the other columns are around 1, and distance squares those gaps. Those three non-overlapping bands mean the thirteen-column clustering is really a sorting of one column. You could have predicted it by printing the spread of every column first."

**What to catch:** "you should have scaled" with no mechanism. **Push once:** *"why does the biggest column win?"* **Full marks needs the words "distance adds up the gaps, so the biggest gaps decide it" and the non-overlapping ranges named as the evidence.** A student who says *"print the spreads first"* unprompted has learned the transferable habit and is at level 4.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot state the two steps. Computes a distance but not consistently. Thinks the algorithm chooses `k`. Reads cluster numbers as values. |
| **2 — Emerging** | Does one round of assign with the table half-filled. Knows the centre is "in the middle" but computes it by eye rather than averaging. Recites "scale first" without a reason. |
| **3 — Secure** | Completes both rounds with all twenty-four squared distances, names C as the switcher and says why it went and why it came back. Reads `Σ` as "add up all of these" and writes the six-term sum out. Matches a hand-computed inertia to `km.inertia_`. Explains the scaling flip using `900` against `400,000,000`. **This is the target.** |
| **4 — Strong** | Predicts before computing that C will switch, from the fact that centre 2 got dragged right. Says inertia always falls, so it cannot choose `k`, and gives the `k = n` case as proof. Reads the three proline bands as the fingerprint of an unscaled run, and proposes printing the column spreads first as a habit. Notices that the two inertias 2,370,689.7 and 1,277.9 are in different units and may not be compared. |
| **5 — Exceptional** | Observes that the lower-inertia `k=3` answer split the right-hand bunch, and that lower inertia therefore does not mean "the grouping a person wanted". Asks what the result would have been on random data before being shown. Points out that the wine reveal only works because the labels existed, and that this is the exception. Raises the question of what happens to a row belonging to no cluster, and notices that k-means has no answer for it. |

---

## 📤 Homework to Assign

This section gives the wording for setting the homework.

**Say this:**

> "About an hour, three pages, and the middle one is the one I mark hardest.
>
> **First, page 28.4 — two rounds by hand on eight new points.** Same as the floor, bigger. Eight points, two centres, and **I want all sixteen squared distances in round one and all sixteen in round two.** Not the winners. **All sixteen, both rounds.** Then both sets of new centres, and the name of the point that switched. There is one and it is not the obvious one.
>
> **Second, page 28.6 — the scaling experiment on the wine data, and this is the page I care about.** Cluster the 178 wines twice: once on the raw columns and once scaled. Report both sets of cluster sizes. **Then find which column took over the unscaled run, and prove it** — print the minimum and maximum of that column inside each unscaled cluster, and show me the bands. **Then two sentences: which column took over, and how you could have predicted it from the column spreads alone, before running anything.**
>
> A page that says 'I scaled it because you should always scale' scores nothing on this page. **I want the number 314.91 in your answer, or whichever number you found.**
>
> **Third, page 28.5 — inertia and the sigma.** Compute the inertia of your eight-point clustering by hand, **with the sum written out in full beside the symbol.** Eight numbers, one addition. Then check it against `km.inertia_` and tell me whether they match to four decimal places.
>
> Page 28.7 is a stretch: it asks you to run the whole thing on 178 rows of pure random numbers. **It still gives you three clusters. Tell me what you think about that.**"

**Workbook pages:** 28.1, 28.2, 28.3 in class · **28.4, 28.5, 28.6** at home · 28.7 optional.

**Expected time:** 25 min on the eight-point trace · 10 min on the inertia and the sigma · 25 min on the scaling experiment · **about 60 minutes**, plus 15 more for the stretch.

> **🧑‍🏫 What to look for when you mark it:** three things, and the second is the real one. **One — are all thirty-two squared distances there?** A page with only the winning distances has not done the assign step, it has guessed it. The whole value of the exercise is that a point can be *nearly* equidistant, and you only see that if you write both numbers. **Two — is the scaling explanation mechanical, or is it a slogan?** The bar is: *did they name a column, quote its spread, and show the bands?* "proline, spread 314.91, and the three unscaled clusters have proline ranges 278–590, 600–937 and 970–1680 which do not overlap" is an explanation. "You have to scale before k-means" is a slogan they could have written before the lesson. **Mark the difference explicitly.** **Three — is the sigma written out?** Eight terms and an addition, beside the symbol. If they wrote the symbol and then wrote a total with nothing in between, hand it back — that is exactly the habit this course is trying to prevent, and it is much easier to prevent now than in Week 32.

---

## 🔑 Answer Key

Every question restated, so you can mark from this page alone.

### Page 28.1 — Match the word to the thing

| Word | What it means |
|---|---|
| **unsupervised learning** | Finding structure in a table that has **no answer column**. There is nothing to compare your result against. |
| **cluster** | A group of points more like each other than like anything outside the group. |
| **centroid** | The **average position** of everything currently in a cluster. `{(1,2), (2,1)}` has centroid `(1.5, 1.5)`. |
| **inertia (WCSS)** | Add up the squared distance from every point to **its own** centre. Smaller means tighter. `6.6667` for our six points. |
| **k-means++** | A smarter way of choosing the starting centres, which **spreads them out** instead of letting them land on top of each other. scikit-learn's default. |
| **elbow method** | Plot inertia against `k` and look for **the bend** — the `k` after which extra clusters stop buying much. A hint, never a verdict. |

**Marking notes.** **Six for six, and be strict about two of them.** *Centroid* must say **average** or **mean**, not "middle-ish" or "centre". *Inertia* must say **own** centre — a student who writes "distance to the centres" has not understood that each point only measures against one of them. The other four are recall.

### Page 28.2 — Predictions, in pen, before running

*Four predictions. (a) Which point will switch sides? (b) Will it take more or fewer than five rounds? (c) When we cluster 178 wines on 13 chemical columns unscaled, will the groups be meaningful? (d) What would happen if we clustered 178 rows of pure random numbers?*

| | Most students predict | The truth |
|---|---|---|
| (a) which point switches | A, or none | **C**, because centre 2 gets dragged to (6.5, 6.75) and C is left behind |
| (b) how many rounds | 5 to 10 | **2** |
| (c) unscaled wine clusters | yes, it has 13 columns of chemistry | **no — they are three non-overlapping bands of `proline` and nothing else** |
| (d) random numbers | it will refuse, or return one cluster, or error | **three tidy clusters, sizes `[62 44 72]`, and you can invent names for them** |

**Marking notes.** **Present or absent, not right or wrong.** (c) and (d) are designed to be got wrong, and nearly everybody gets (d) wrong. **What earns credit is a prediction with a reason attached** — *"the groups will be meaningful because there are thirteen columns of real chemistry in there"* is a genuine hypothesis and it got tested and refuted, which is the best thing that can happen to a hypothesis. **A blank page means the lesson was a demonstration rather than an experiment.**

### Page 28.3 — The floor trace (in class)

**Round 1, with centres at (1, 2) and (2, 3).** All twelve squared distances:

| point | to centre 1 = (1,2) | to centre 2 = (2,3) | winner |
|---|---|---|---|
| A (1,2) | 0 + 0 = **0** | 1 + 1 = 2 | centre 1 |
| B (2,1) | 1 + 1 = **2** | 0 + 4 = 4 | centre 1 |
| C (2,3) | 1 + 1 = 2 | 0 + 0 = **0** | centre 2 |
| D (8,8) | 49 + 36 = 85 | 36 + 25 = **61** | centre 2 |
| E (9,7) | 64 + 25 = 89 | 49 + 16 = **65** | centre 2 |
| F (7,9) | 36 + 49 = 85 | 25 + 36 = **61** | centre 2 |

Groups: `{A, B}` and `{C, D, E, F}`. Move:

```text
centre 1 = ( (1+2) ÷ 2 , (2+1) ÷ 2 )          = ( 1.5 , 1.5 )
centre 2 = ( (2+8+9+7) ÷ 4 , (3+8+7+9) ÷ 4 )  = ( 6.5 , 6.75 )
```

**Round 2, with centres at (1.5, 1.5) and (6.5, 6.75).** All twelve:

| point | to centre 1 = (1.5,1.5) | to centre 2 = (6.5,6.75) | winner |
|---|---|---|---|
| A (1,2) | 0.25 + 0.25 = **0.50** | 30.25 + 22.5625 = 52.8125 | centre 1 |
| B (2,1) | 0.25 + 0.25 = **0.50** | 20.25 + 33.0625 = 53.3125 | centre 1 |
| C (2,3) | 0.25 + 2.25 = **2.50** | 20.25 + 14.0625 = 34.3125 | **centre 1 ← switched** |
| D (8,8) | 42.25 + 42.25 = 84.50 | 2.25 + 1.5625 = **3.8125** | centre 2 |
| E (9,7) | 56.25 + 30.25 = 86.50 | 6.25 + 0.0625 = **6.3125** | centre 2 |
| F (7,9) | 30.25 + 56.25 = 86.50 | 0.25 + 5.0625 = **5.3125** | centre 2 |

Groups: `{A, B, C}` and `{D, E, F}`. Move:

```text
centre 1 = ( 5÷3 , 6÷3 ) = ( 1.6667 , 2.0 )
centre 2 = ( 24÷3 , 24÷3 ) = ( 8.0 , 8.0 )
```

**Round 3 changes nothing, so it stops. Converged in 2 rounds.** The switcher is **C**.

**Marking notes.** **Twenty-four squared distances, or it is not finished.** The most common error is computing the *across* gap and forgetting to square it — you will see `A to centre 2 = 1 + 1 = 2` written as `1 + 1 = 2` correctly by luck, since 1² = 1, and then `D to centre 1 = 7 + 6 = 13` instead of `49 + 36 = 85`. **Check a row where the gaps are bigger than 1; that is where the error shows.**

### Page 28.4 — Two rounds by hand on eight points (homework)

*The points: `P1=(1,1)`, `P2=(2,1)`, `P3=(1,3)`, `P4=(3,2)`, `P5=(7,6)`, `P6=(8,8)`, `P7=(9,7)`, `P8=(8,5)`. Starting centres: `C1=(1,1)` and `C2=(3,2)`.*

**ROUND 1, assign — all sixteen squared distances.**

| point | to C1 = (1,1) | to C2 = (3,2) | winner |
|---|---|---|---|
| P1 (1,1) | 0 + 0 = **0** | 4 + 1 = 5 | C1 |
| P2 (2,1) | 1 + 0 = **1** | 1 + 1 = 2 | C1 |
| P3 (1,3) | 0 + 4 = **4** | 4 + 1 = 5 | C1 |
| P4 (3,2) | 4 + 1 = 5 | 0 + 0 = **0** | C2 |
| P5 (7,6) | 36 + 25 = 61 | 16 + 16 = **32** | C2 |
| P6 (8,8) | 49 + 49 = 98 | 25 + 36 = **61** | C2 |
| P7 (9,7) | 64 + 36 = 100 | 36 + 25 = **61** | C2 |
| P8 (8,5) | 49 + 16 = 65 | 25 + 9 = **34** | C2 |

Groups: **C1 = {P1, P2, P3}**, **C2 = {P4, P5, P6, P7, P8}**.

**ROUND 1, move.**

```text
C1 = ( (1+2+1) ÷ 3 , (1+1+3) ÷ 3 )           = ( 4÷3 , 5÷3 )   = ( 1.3333 , 1.6667 )
C2 = ( (3+7+8+9+8) ÷ 5 , (2+6+8+7+5) ÷ 5 )   = ( 35÷5 , 28÷5 ) = ( 7.0 , 5.6 )
```

**ROUND 2, assign — all sixteen squared distances.**

| point | to C1 = (1.3333, 1.6667) | to C2 = (7.0, 5.6) | winner |
|---|---|---|---|
| P1 (1,1) | 0.1111 + 0.4444 = **0.5556** | 36.0000 + 21.1600 = 57.1600 | C1 |
| P2 (2,1) | 0.4444 + 0.4444 = **0.8889** | 25.0000 + 21.1600 = 46.1600 | C1 |
| P3 (1,3) | 0.1111 + 1.7778 = **1.8889** | 36.0000 + 6.7600 = 42.7600 | C1 |
| P4 (3,2) | 2.7778 + 0.1111 = **2.8889** | 16.0000 + 12.9600 = 28.9600 | **C1 ← switched** |
| P5 (7,6) | 32.1111 + 18.7778 = 50.8889 | 0.0000 + 0.1600 = **0.1600** | C2 |
| P6 (8,8) | 44.4444 + 40.1111 = 84.5556 | 1.0000 + 5.7600 = **6.7600** | C2 |
| P7 (9,7) | 58.7778 + 28.4444 = 87.2222 | 4.0000 + 1.9600 = **5.9600** | C2 |
| P8 (8,5) | 44.4444 + 11.1111 = 55.5556 | 1.0000 + 0.3600 = **1.3600** | C2 |

Groups: **C1 = {P1, P2, P3, P4}**, **C2 = {P5, P6, P7, P8}**. **The switcher is P4.**

**ROUND 2, move.**

```text
C1 = ( (1+2+1+3) ÷ 4 , (1+1+3+2) ÷ 4 ) = ( 7÷4 , 7÷4 )   = ( 1.75 , 1.75 )
C2 = ( (7+8+9+8) ÷ 4 , (6+8+7+5) ÷ 4 ) = ( 32÷4 , 26÷4 ) = ( 8.0 , 6.5 )
```

**Round 3 changes nothing — converged in 2 rounds**, exactly as on the floor.

And the check:

```python
import numpy as np
from sklearn.cluster import KMeans

pts = np.array([[1., 1.], [2., 1.], [1., 3.], [3., 2.],
                [7., 6.], [8., 8.], [9., 7.], [8., 5.]])
km = KMeans(n_clusters=2, init=np.array([[1., 1.], [3., 2.]]),
            n_init=1, random_state=0).fit(pts)
print("labels :", km.labels_)
print("centres:", np.round(km.cluster_centers_, 4).tolist())
print("inertia: %.4f   rounds: %d" % (km.inertia_, km.n_iter_))
```

```text
labels : [0 0 0 0 1 1 1 1]
centres: [[1.75, 1.75], [8.0, 6.5]]
inertia: 12.5000   rounds: 3
```

**Marking notes.** **Thirty-two squared distances or it is incomplete.** The interesting row is P4: it starts as a centre's own location (distance 0, so it cannot lose round 1) and then switches, which is the same trap as C on the floor wearing different clothes. **A student who noticed that P4 was *guaranteed* to win round 1 because a centre was sitting on it has understood something real.** Watch for `(9−7)² = 4` being written as `2`; the fingerprint is the row for P7.

### Page 28.5 — Inertia, with the sigma written out (homework)

*Compute the inertia of your final eight-point clustering by hand, writing the sum out in full beside the symbol. Then check it against `km.inertia_`.*

Final centres: `C1 = (1.75, 1.75)` with `{P1, P2, P3, P4}`, and `C2 = (8.0, 6.5)` with `{P5, P6, P7, P8}`.

```text
P1 (1,1) to (1.75, 1.75):  0.5625 + 0.5625 = 1.1250
P2 (2,1) to (1.75, 1.75):  0.0625 + 0.5625 = 0.6250
P3 (1,3) to (1.75, 1.75):  0.5625 + 1.5625 = 2.1250
P4 (3,2) to (1.75, 1.75):  1.5625 + 0.0625 = 1.6250
P5 (7,6) to (8.0,  6.5) :  1.0000 + 0.2500 = 1.2500
P6 (8,8) to (8.0,  6.5) :  0.0000 + 2.2500 = 2.2500
P7 (9,7) to (8.0,  6.5) :  1.0000 + 0.2500 = 1.2500
P8 (8,5) to (8.0,  6.5) :  0.0000 + 2.2500 = 2.2500
```

And the sigma, written out beside the symbol as required:

```text
Σ (distance to my own centre)²
   =  1.1250 + 0.6250 + 2.1250 + 1.6250 + 1.2500 + 2.2500 + 1.2500 + 2.2500
   =  12.5000
```

`km.inertia_` prints **12.5000**. **They match to four decimal places.** ✅

A useful extra check they may notice: cluster 1 contributes `1.1250 + 0.6250 + 2.1250 + 1.6250 = 5.5000` and cluster 2 contributes `1.2500 + 2.2500 + 1.2500 + 2.2500 = 7.0000`, and `5.5 + 7.0 = 12.5`. **Cluster 2 is the looser of the two**, which is visible in the numbers and not in a picture.

**Marking notes.** **The eight terms must be on the page, beside the symbol.** A total with no sum written out fails this page even if the total is right — that is the whole point of the page. **Full marks also needs "they match", stated.** A student who breaks the total down per cluster and notices cluster 2 is looser has gone beyond the task.

### Page 28.6 — The scaling experiment on `load_wine` (homework)

```python
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler

wine = load_wine()
X_raw = pd.DataFrame(wine.data, columns=wine.feature_names)

print("the spread of each column, biggest first:")
print(X_raw.std().sort_values(ascending=False).round(2).head(5).to_string())

km_raw = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X_raw)
Xs = StandardScaler().fit_transform(X_raw)
km_sc = KMeans(n_clusters=3, n_init=10, random_state=0).fit(Xs)
print()
print("UNSCALED sizes", np.bincount(km_raw.labels_))
print("SCALED   sizes", np.bincount(km_sc.labels_))

print()
pro, alc = X_raw["proline"].values, X_raw["alcohol"].values
for c in range(3):
    m = km_raw.labels_ == c
    print("unscaled cluster %d: n=%3d  proline %4.0f to %4.0f   alcohol %.2f to %.2f"
          % (c, m.sum(), pro[m].min(), pro[m].max(), alc[m].min(), alc[m].max()))
```

```text
the spread of each column, biggest first:
proline              314.91
magnesium             14.28
alcalinity_of_ash      3.34
color_intensity        2.32
malic_acid             1.12

UNSCALED sizes [69 47 62]
SCALED   sizes [65 51 62]

unscaled cluster 0: n= 69  proline  278 to  590   alcohol 11.03 to 14.13
unscaled cluster 1: n= 47  proline  970 to 1680   alcohol 12.85 to 14.83
unscaled cluster 2: n= 62  proline  600 to  937   alcohol 11.45 to 14.34
```

**The two sentences being marked.**

> **`proline` took over.** Its spread is **314.91**, against **1.00** for `flavanoids` and **0.81** for `alcohol` — and because distance adds up the *squared* gaps, proline contributes roughly 314.91² ÷ 1.00² ≈ **99,000 times** more to every comparison than flavanoids does. The proof is in the three unscaled clusters' proline ranges — **278–590, 600–937, 970–1680, which do not overlap by a single unit** — while their alcohol ranges (11.03–14.13, 12.85–14.83, 11.45–14.34) overlap almost completely.
>
> **It was predictable from `X_raw.std()` alone**, before clustering anything: one column's spread was **22 times** the next biggest (`magnesium`, 14.28) and **2,624 times** the smallest (`nonflavanoid_phenols`, 0.12), so that column was always going to be the whole model.

**Marking notes.** **This is the page to mark hardest, and there are three bars.** **One — is a specific column named, with its spread quoted?** `proline`, `314.91`. **Two — is there evidence rather than assertion?** The non-overlapping bands. A student who only reports the two sets of cluster sizes has not proved anything — `[69 47 62]` and `[65 51 62]` look reassuringly similar, which is exactly why sizes are the wrong evidence. **Say that in your feedback; it is the subtlest point on the page.** **Three — does the prediction come from the spreads, not from hindsight?** "I could have predicted it because I know you have to scale" is not a prediction. **A student who notices that distance squares the gaps, so a 315-to-1 ratio in spread becomes about 99,000-to-1 in influence, is at level 5.**

### Page 28.7 — Stretch: three clusters from nothing

*Run the whole thing on 178 rows of 13 columns of pure random numbers. Report what you get, and say what you think about it.*

```python
import numpy as np
from sklearn.cluster import KMeans

noise = np.random.default_rng(0).normal(size=(178, 13))
km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(noise)
print("sizes  :", np.bincount(km.labels_))
print("inertia: %.1f" % km.inertia_)
print("cluster 0 means, first four columns:",
      np.round(noise[km.labels_ == 0].mean(axis=0)[:4], 3))
print("cluster 1 means, first four columns:",
      np.round(noise[km.labels_ == 1].mean(axis=0)[:4], 3))
```

```text
sizes  : [62 44 72]
inertia: 1973.0
cluster 0 means, first four columns: [-0.444 -0.259  0.296 -0.041]
cluster 1 means, first four columns: [ 0.522 -0.029  0.096  0.91 ]
```

**And here is the honest reading, which is the whole point of the page.**

**Nothing went wrong.** There is no structure whatsoever in that data — every one of the 2,314 numbers came out of the same random generator — and k-means returned three clean clusters of 62, 44 and 72, with a perfectly respectable-looking inertia and **visibly different column means.** Cluster 0 is low on column 1 and cluster 1 is high on it; cluster 1 is high on column 4 and cluster 0 is not. **You could write a report about those groups. You could name them.** Somebody would believe it.

**So the lesson is not "k-means is unreliable". It is this: `km.labels_` coming back is not evidence of anything.** The algorithm is doing exactly what it was asked — find the tightest three groups in this cloud — and in a formless cloud there is still a tightest three groups. It just does not mean there are three of anything.

**Which is why the deliverable in unsupervised learning is an argument.** You need a reason to believe your structure is in the data rather than in the method, and **you get it by comparing against exactly this: run your whole pipeline on noise and see what it gives you.** A silhouette score of 0.28 on real data means something very different if noise scores 0.08 than if noise scores 0.26. Week 30 does this properly and calls it a negative control.

**Marking notes.** **The numbers are the easy half; the sentence is the page.** Full marks needs some version of *"getting clusters is not evidence that there are clusters"*. **A student who proposes running the noise version as a routine check before trusting any clustering has independently invented the negative control, which is a genuinely rare move — say so loudly.** A student who says "the random data must have had a pattern in it" has the misconception backwards; push them to generate it again with a different seed and see that the sizes change but the tidiness does not.

### Answers to every question posed in the lesson

**Hook — "so what breaks?"** **All of the measurement does.** No accuracy, precision, recall, AUC or log loss, because every one of them is a comparison against a right answer. Overfitting becomes hard even to define. There is no right answer for any individual row.

**Hook — "which of the Lego sortings is the right answer?"** **None, and all of them are valid.** There is no key at the back. What you can do is defend a choice.

**Hook — "tell me the two groups."** `{A, B, C}` and `{D, E, F}`, instantly, by eye. **The whole point is that the eye does this in a second and a half and cannot do it at all on thirteen columns.**

**Concept — "C is one step from A and B. Why is it with the far group?"** **Because centre 2 is standing exactly on top of C, so C's distance to it is 0, and 0 beats 2.** The algorithm is not wrong; the starting position is.

**Concept — "where does centre 1 go?"** The average of A and B: `((1+2) ÷ 2, (2+1) ÷ 2) = (1.5, 1.5)`.

**Concept — "why did centre 2 move so far?"** **It got dragged.** It received four points, three of them seven units away, and the average of one near and three far points lands out among the far ones: `(26÷4, 27÷4) = (6.5, 6.75)`.

**Concept — "C's two distances in round 2. Which is smaller?"** `2.50` against `34.3125`. **2.50, so C switches back.** The bad start repaired itself in one round.

**Concept — "with 178 wines, how many numbers in the sigma sum?"** **178.** And you still would not write them out — but you would know exactly what was being asked for.

**Concept — "what `k` gives the smallest inertia?"** **`k` = the number of points.** Every point is its own centre, every distance is 0, inertia is exactly 0. **Perfect score, zero information** — which is why inertia can never choose `k`.

**Live-code step 1 — "it says no attribute `labels_`. What did I not do?"** **You never called `.fit`.** The machine was built and never switched on. **And the rule: a scikit-learn name ending in `_` does not exist until `.fit` has run.**

**Live-code step 1 — "centres? inertia? rounds?"** `(1.6667, 2.0)` and `(8, 8)` — same as the board. `6.6667` — same as the board. **Rounds: we said 2, sklearn says 3, and both are right** — it counts the final pass that confirmed nothing changed.

**Live-code step 3 — "how do we know those groups are anything?"** **We do not.** Which is why the next thing to do is look inside them.

**Live-code step 3 — "what do you notice about 278–590, 600–937, 970–1680?"** **They do not overlap at all.** The thirteen-column clustering is a sorting of one column into three bands.

**Live-code step 3 — "so what have the clusters sorted the wine by?"** **`proline`, and nothing else.** Its spread is 314.91 against about 1 for most of the others, and distance squares the gaps.

**Live-code step 3 — "inertia went from 2,370,689.7 to 1,277.9. Did it get two thousand times better?"** **No. The units changed.** Inertia is in whatever units the table is in. **You may compare two inertias from the same table measured the same way, and never across a change of units** — Week 27's name-the-pile rule in a new costume.

**Wrap — "which pair does raw k-means think is more alike, and by how much?"** **P1 and P2**, by `400000000 ÷ 900 = 444444` — about four hundred and forty-four thousand times. Thirty years of a human life against a 4% pay rise.

**Wrap — "rows are the real grape varieties. What do you see?"** **Each row puts almost everything in one column: 59, 65 and 48.** Six bottles out of 178 in the wrong pile, by an algorithm that never saw a grape. **And the point that matters more: we only got to check because somebody had already labelled these bottles.**

**Activity step 3 — "centre 2, why did you just walk five metres?"** Three of my four points were over there, so my average is over there.

**Activity step 4 — "round three. Would anybody switch?"** **No. So we stop.**

**Variation-harder 1 — "start the centres in the right place. How many rounds?"** **One.** And the good follow-up: *"so was the bad start wasted?"* **No** — the bad start is what showed you the algorithm repairs itself, which a good start cannot teach.

**Variation-harder 2 — the local minimum.** Crowded start, `k=3`: inertia **5.0**, groups `{A,C}`, `{B}`, `{D,E,F}`. k-means++ with `n_init=10`: inertia **3.6667**, groups `{A,B,C}`, `{D,F}`, `{E}`. **The lower-inertia answer split the right-hand bunch** — lower inertia means tighter, not "the grouping a human wanted".

**Variation-harder 3 — the outlier at (20, 20).** With `k=2` the real output is `labels [0 0 0 0 0 0 1]` and centres `(4.8333, 5.0)` and `(20.0, 20.0)`. **The single far point has claimed a whole cluster, and the two obvious blobs have been merged.** Because **k-means has no "none of the above"** — every row must join something, and there is nothing in the algorithm that can refuse a row or flag it as odd.

**Variation-harder 4 — the six-point elbow.** `k=1`: centre `(4.8333, 5.0)`, inertia **120.8333**. `k=2`: **6.6667**. `k=3`: **3.6667**. Drops: `114.1667` then `3.0000`, a **ratio of 38**. **That is what an unmistakable elbow looks like**, and the wine data's ratio of 3.9 is far softer — which is the honest state of most real data.

**Variation-harder 6 — clustering on `proline` alone.** The labels come out **identical to the unscaled thirteen-column run — 178 of 178, cluster for cluster.** Twelve columns were not weakly consulted; they were not consulted at all.

---

## 🔮 Next Week Preview

Next week is the other half of Term 4's toolkit, and it answers a question this week raised and dodged: **thirteen columns is too many to look at, so which ones do you throw away?** The answer is: **none of them.** **PCA** — principal component analysis — does not delete columns. It draws a **new pair of axes** through the cloud of data, the first one pointing along the direction the data is most spread out, and then measures everything against those instead. The student meets **variance** first, as nothing more than *the average squared distance from the mean*, computed by hand on the five numbers 4, 6, 8, 10 and 12 — where the distances are −4, −2, 0, 2, 4, the squares are 16, 4, 0, 4, 16, they add to 40, and 40 ÷ 4 = 10. Then the activity: five points on graph paper, six candidate axes drawn at 30-degree steps, everybody projects the five points onto their own assigned axis by hand and computes the spread — and **the widest one wins, at 30 degrees with a spread of 17.4192.** Then `pca.components_` is printed and it says 42.62 degrees with a spread of 18.2812, so the class's 30-degree grid was twelve degrees short and they can see exactly why a finer grid would close the gap. Finally the thirteen wine columns get squashed to two, which keeps **55.4%** of the spread, and the price of that is measured honestly: rebuilding the wines from two components misses by **2.2550** when a typical wine sits only **3.5180** from the middle.

**To prep early:** three things. **One — leave the SIX POINTS sheet up.** It comes down at the end of Week 30, not next week, and a new sheet goes up beside it headed **SPREAD**, with a blank number line on it. **Two — you need real graph paper with a visible grid, at least ten squares by ten, one sheet per student**, plus a ruler and a protractor each. Next week's activity is drawing axes at 30-degree steps and measuring along them, and it genuinely does not work on plain paper. **Borrow protractors from the maths department this week, not next Monday morning.** **Three — run `from sklearn.decomposition import PCA` tonight** and check that `PCA().fit(np.array([[4.,3.],[6.,6.],[8.,7.],[10.,8.],[12.,11.]])).explained_variance_ratio_` prints `[0.9882 0.0118]`. It ships inside scikit-learn, nothing downloads, but you want to have seen those two numbers appear before you stand in front of the class.

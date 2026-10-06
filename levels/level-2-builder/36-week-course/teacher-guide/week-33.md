# Week 33 — Model Bake-Off and the Overfitting Cliff

[⬅ Week 32](week-32.md) · [Course Home](../README.md) · [Week 34 ➡](week-34.md) · [Student Guide](../student-guide/week-33.md) · [Workbook](../workbook/week-33.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟩 Lab — one split, three models, one table, one picture. **The most important lesson in Level 2.** |
| **Big idea** | A training score that climbs while the test score falls is memorising, not learning — and it has a picture. |
| **New vocabulary** | overfitting · underfitting · train/test gap · RMSE · model complexity |
| **New syntax** | `DecisionTreeRegressor(max_depth=d)` · `np.sqrt(mean_squared_error(y_true, y_pred))` · `ax.axvline(x, linestyle="--")` · `load_diabetes()` |
| **Materials** | Printed workbook pages 33.1–33.6 · graph paper · a ruler · **4 coloured pens or highlighters** · a calculator · **whatever the student wrote in Week 29 about the gap between their train and test scores** · `week31_tree_iris.py` and `week32_study_line.py` · the Bug Log |
| **Tech needed** | Python 3 with scikit-learn, numpy and matplotlib. No new install. No internet. |
| **Prep time** | 25 minutes the night before, 5 minutes on the day |

> **⚠️ Watch out:** this lesson only bites if the student is still a little proud of a score. That is why the course puts four weeks between Week 29 and today. **Do not soften the punchline** — one row of today's table shows a model that is *perfect* on the rows it learned from and *no better than guessing the average* on rows it has never seen. Let that land hard. And go and find the Week 29 numbers before class; the lesson ends by walking back to them.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Run three different models on one fixed split**, changing one line each time.
2. **Compute RMSE** and explain why it punishes big misses harder than MAE does.
3. **Plot train score and test score against depth 1 to 15** on one pair of axes.
4. **Mark the point where the two lines part company** and name it out loud.
5. **State which model they would ship**, and defend the choice with the numbers.

Observable evidence: a five-row results table with MAE, RMSE, test R² and train R² for every entry; a two-line depth curve with a vertical line drawn at the peak of the test line; the sentence *"after here it is memorising"* written under it; and one named model with a written reason that cites at least two numbers.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

There are two ideas this week and one of them is the whole point of the year. Take the twenty-five minutes; you will teach it far better for having felt the numbers once yourself.

### 1. The idea, in one table

Compute two scores — one on the rows the model learned from, one on rows it has never seen — then look up your row.

| Train score | Test score | What it is called | What is happening | What to do |
|---|---|---|---|---|
| Low | Low | **Underfitting** | Too simple to catch the pattern | Give it more room: deeper tree, more features |
| High | High | **Just right** | It learned the pattern | Ship it (and check your split is honest) |
| **High** | **Low** | **Overfitting** | It memorised the training rows, noise and all | Give it less room: shallower tree, more data |
| Low | High | Something is broken | Nearly always a bug or a freak tiny test set | Go and read your code |

> **Underfitting** — the model is too simple. It gets things wrong on the rows it learned from *and* on new rows, in the same way.
>
> **Overfitting** — the model is too complicated. It has learned details of the specific training rows that do not carry over, so it does brilliantly on them and badly on everything else.
>
> **Train/test gap** — train score minus test score. A small gap means it generalises. A big gap means it is memorising.

🍕 **The analogy to use out loud. Use exactly this one; it is the best one there is.** Three students prepare for a maths test.

- **Ravi** skims the chapter headings. He can't do the practice questions *or* the test. That is **underfitting** — he never learned the pattern.
- **Priya** learns the method. She does well on practice and well on the test. **Just right.**
- **Sam** memorises all 200 practice questions and their answers, word for word. He scores 200 out of 200 on practice. On the test, where the numbers are different, he falls apart. That is **overfitting** — he learned the *questions*, not the *maths*.

**Sam's practice score is not a lie.** He really did get 200 out of 200. It is just not evidence of anything.

![Same eight points. Three models.](../figures/fig-w33-1-underfit-goodfit-overfit.svg)
*Figure 33.1 — Same eight points, three models. The dots never move. Only the line does.*

### 2. Model complexity: the dial every model has

> **Model complexity** — how much freedom a model has to bend itself around the data. Every model has a dial that sets it.

| Model | The dial | Simple end | Complex end |
|---|---|---|---|
| Decision tree | `max_depth` | 1 | no limit |
| kNN | `n_neighbors` | large `k` | `k = 1` |
| Linear regression | number of features | 1 feature | many features |

Note that kNN's dial runs **backwards**: `k = 1` is the *most* complex setting, because a single nearest neighbour can carve any shape at all, and a huge `k` is the simplest. If the student remembers `k = 1` scoring a perfect 1.0000 on training data back in Week 30, that was the overfitting end of the dial all along, and nobody said so at the time.

`max_depth` is the dial you will turn today, because a tree's is the easiest to see. Crank it up and the tree gets to ask more questions, cut the training rows into more and more leaves, and eventually give nearly every single row its own private leaf.

```
 depth 1  →    2 leaves     one question, two answers
 depth 4  →   16 leaves     sixteen sensible bands
 depth 8  →  128 leaves     each leaf holds two or three patients
 depth 15 →  329 leaves     329 leaves for 353 patients. Memorised.
```

![329 leaves for 353 rows is a phone book](../figures/fig-w33-5-leaves-versus-rows.svg)
*Figure 33.2 — 329 leaves for 353 rows is a phone book. This is the picture of memorising.*

**That last line is the mechanism, and it is worth having ready as a sentence:** with 353 training patients and 329 leaves, the tree has essentially written down a lookup table. It has not learned anything about diabetes. It has written down these 353 people. Ask it about a 354th person and it has nothing.

### 3. RMSE — and be honest about what it does

Last week gave you MAE: add up the sizes of the misses, divide by how many. This week adds a second one.

> **RMSE (root mean squared error)** — square every miss, average the squares, then take the square root. Also in the units of the thing you are predicting, but it punishes big misses much harder than small ones.

```
RMSE = √( (miss₁² + miss₂² + ... + missₙ²) ÷ n )
```

**RMSE is always greater than or equal to MAE.** The gap between them tells you about the *shape* of your errors: if RMSE is barely above MAE, your misses are all much the same size. If RMSE is a lot bigger, a few large ones are dominating.

**The two-model demonstration that makes it obvious.** Ten true values. Two models.

- **Model A** is off by exactly 1 on every single prediction.
- **Model B** is *perfect* on nine of them and off by 10 on the tenth.

```text
Model A: errors [1 1 1 1 1 1 1 1 1 1]  MAE 1.0000  RMSE 1.0000
Model B: errors [ 0  0  0  0  0  0  0  0  0 10]  MAE 1.0000  RMSE 3.1623
```

**Identical MAE. RMSE differs by more than three times.** By hand:

- Model A: every size is 1, so MAE = 10 ÷ 10 = 1.0. Every square is 1, so the mean square is 1.0 and RMSE = √1 = 1.0.
- Model B: nine sizes of 0 and one of 10, so MAE = 10 ÷ 10 = 1.0 — identical. But squared: nine 0s and one **100**, so the mean square is 100 ÷ 10 = 10, and RMSE = √10 = **3.1623**.

Which model is better? **It depends entirely on what a big miss costs.** Nine perfect delivery times and one catastrophe is probably worse than ten slightly-late ones. Nine perfect grocery-bill estimates and one wrong week is probably better than being wrong every single week. **The metric encodes what you think "bad" means, so choose it on purpose.**

> **⚠️ Watch out — do not overclaim.** It is tempting to say "RMSE tells you the worst miss". It does not, and today's real numbers will catch you out if you say it. On our data, linear regression has a **worse single worst miss** than kNN (154 against 139) and yet a **lower RMSE** (53.85 against 54.95) — because kNN has nine misses over 100 and linear has only five. RMSE is about the *whole tail of big misses*, not one champion. The honest sentence is: *"RMSE goes up faster than MAE when there are big misses."* Say that and nothing more.

The habit to teach, and it costs nothing: **print MAE, RMSE and the worst single miss.** Three numbers, and it becomes very hard for anybody, including you, to be fooled.

### 4. The dataset, and why we changed it

`load_diabetes()` ships inside scikit-learn. **442 real patients**, 10 measurements each — age, sex, body mass index, blood pressure and six blood measurements — and the answer column is *how far the illness had progressed one year later*, on a scale running from 25 to 346.

Three things to know before you meet it:

- **It is real, and real data is much noisier than flowers.** The best R² anybody gets on it today is about **0.45**. Iris gave you 0.9667 accuracy. This is what actual data looks like, and the drop is the point rather than a disappointment.
- **The measurements are already scaled**, by whoever prepared the dataset. So there is no `StandardScaler` in today's file even though we are using kNN, and that is not an oversight. If a student remembers Week 30 and asks, that is a *good* catch — tell them the dataset arrived pre-scaled and they were right to check.
- **The answer has no everyday unit.** It is "progression points". So an MAE of 42.77 cannot be translated into anything a person feels, which is honestly a bit of a shame after last week's "off by three marks". Say so. The comparison that saves it is the lazy baseline: guessing the average is off by 64.01, so 42.77 is *a third better than not bothering*.

### 5. Every line of the bake-off file, explained

```python
# week33_bakeoff.py  -  three models, ONE split, one table.

import numpy as np
from sklearn.datasets import load_diabetes                # NEW: 442 real patients
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor         # week 29's kNN, for numbers
from sklearn.tree import DecisionTreeRegressor            # week 31's tree, for numbers
from sklearn.linear_model import LinearRegression         # week 32's line
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

data = load_diabetes()
X = data.data                 # 10 measurements per patient
y = data.target               # how much the illness advanced in a year
print("rows and columns:", X.shape)
print("the answer runs from", y.min(), "to", y.max())

# ---- ONE split. Made once, here, at the top. Never made again. ----------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
print("train rows:", len(X_train), " test rows:", len(X_test))
print()

def report(name, model):
    """Fit a model on the SAME train rows, score it on the SAME test rows."""
    model.fit(X_train, y_train)
    guesses = model.predict(X_test)
    mae = mean_absolute_error(y_test, guesses)
    rmse = np.sqrt(mean_squared_error(y_test, guesses))   # NEW: root of the mean square
    print(f"{name:22s} {mae:7.2f} {rmse:7.2f} "
          f"{r2_score(y_test, guesses):9.3f} {model.score(X_train, y_train):10.3f}")

print(f"{'model':22s} {'MAE':>7s} {'RMSE':>7s} {'test R2':>9s} {'train R2':>10s}")

# the laziest model there is: ignore all 10 columns, always say the training mean
lazy = np.zeros(len(y_test)) + y_train.mean()
print(f"{'always guess the mean':22s} "
      f"{mean_absolute_error(y_test, lazy):7.2f} "
      f"{np.sqrt(mean_squared_error(y_test, lazy)):7.2f} "
      f"{r2_score(y_test, lazy):9.3f} {0.0:10.3f}")

report("kNN, k = 5", KNeighborsRegressor(n_neighbors=5))
report("tree, max_depth=5", DecisionTreeRegressor(max_depth=5, random_state=0))
report("tree, no limit", DecisionTreeRegressor(random_state=0))
report("linear regression", LinearRegression())
```

**Line by line, for the parts that are new.**

- `from sklearn.neighbors import KNeighborsRegressor` — the same tool as Week 29's `KNeighborsClassifier`, with `Regressor` on the end because the answer is a number now. Instead of the five nearest neighbours *voting* on a species, they *average* their numbers.
- `from sklearn.tree import DecisionTreeRegressor` — same again for Week 31's tree. Identical yes/no questions; each leaf holds the **average** of the training rows that landed there instead of a species name. That is why a tree's predictions come in a fixed set of steps — one value per leaf — and why a tree can never draw a smooth diagonal.
- `X_train, X_test, y_train, y_test = train_test_split(...)` — **this line runs exactly once, at the top of the file.** Everything below shares those same 353 training and 89 test patients. That one fact is the entire fairness of a bake-off, and it is worth saying in a comment.
- `def report(name, model):` — a function, from Weeks 9 and 10. One function means it is *impossible* to score two models differently by accident. If you compute the numbers separately for each model, sooner or later you will use `y_train` where you meant `y_test` in one of them and never notice.
- `model.fit(X_train, y_train)` inside `report` — every model is fitted fresh, on the same rows.
- `np.sqrt(mean_squared_error(y_test, guesses))` — `mean_squared_error` gives the average of the squares; `np.sqrt` (Week 28) takes the square root to bring it back into the answer's units. **There used to be a `squared=False` shortcut and it has been removed from modern scikit-learn** — see the Debugging Clinic, because a student who searches the internet will find it and it will fail.
- `np.zeros(len(y_test)) + y_train.mean()` — the lazy baseline. `np.zeros` (Week 18) makes 89 zeros, and adding a single number to an array adds it to every slot (Week 18 again). So this is "guess 153.74 for all 89 patients". Note it is the **training** mean — using the test mean would be peeking.
- `f"{mae:7.2f}"` — an f-string from Week 3, with a width of 7 and 2 decimals so the columns line up.

**The real output:**

```text
rows and columns: (442, 10)
the answer runs from 25.0 to 346.0
train rows: 353  test rows: 89

model                      MAE    RMSE   test R2   train R2
always guess the mean    64.01   73.22    -0.012      0.000
kNN, k = 5               42.77   54.95     0.430      0.584
tree, max_depth=5        48.15   62.60     0.260      0.669
tree, no limit           56.57   72.90    -0.003      1.000
linear regression        42.79   53.85     0.453      0.528
```

### 6. How to read that table — the four things to point at

**Point 1 — the row that is the whole lesson.**

```
tree, no limit           56.57   72.90    -0.003      1.000
```

**Train R² 1.000. Perfect.** Not 0.99. Perfect. On the 353 patients it learned from, this tree is never wrong, not once.

**Test R² −0.003.** Negative. Strictly, R² below 0 means *worse than guessing the average of the test rows*. Look up the baseline row — R² −0.012 (it guesses the training average) — and the unlimited tree is essentially level with it: it is NOT worse than the lazy model here (its MAE 56.57 and RMSE 72.90 are even slightly better than 64.01 and 73.22). The honest line is *no better than ignoring all ten measurements*.

A perfect score and a worthless model, in the same row, on the same data. That is Sam and his 200 practice questions, in numbers you generated yourself.

**Point 2 — the baseline row is what makes every other number mean something.** MAE 64.01 by guessing the average. So kNN's 42.77 is not "off by 42.77", it is "**a third less wrong than not bothering**". Without the baseline, 42.77 is a number with nothing to stand on. This is Level 1's Week 12 lesson — compute the baseline first — arriving in code.

**Point 3 — MAE and RMSE disagree, and that is the interesting bit.**

| | MAE | RMSE |
|---|---|---|
| kNN, k = 5 | **42.77** | 54.95 |
| linear regression | 42.79 | **53.85** |

On MAE they are a dead heat — 42.77 against 42.79, a difference of two hundredths on a scale running to 346. On RMSE, linear wins. Why? Because kNN has **nine** misses over 100 and linear has only **five**. RMSE squares the misses, so those extra big ones weigh heavily. Typical performance: identical. Big-miss behaviour: linear is better. **That is a real difference that MAE cannot see, and it is why we compute both.**

**Point 4 — the depth-5 tree is worse than both, and that is honest.** Test R² 0.260 against 0.453 for the line. Trees are not the best tool for everything, and this dataset — probably, though we did not test it: smooth medical measurements, no sharp thresholds — is exactly the shape a straight line handles well and a staircase handles badly. Do not hide that. The tree's advantage was always *readability*, and this week is the week it costs you.

### 7. The depth curve — the most useful picture in the subject

**The recipe, and step 1 is not optional:**

1. Fix **one** train/test split, before the loop. Never re-split inside it, or you are measuring shuffling luck instead of depth.
2. For each depth, fit a **fresh** model.
3. Record **both** the train score and the test score.
4. Plot both against depth.
5. The depth with the highest **test** score is your answer.

```python
# week33_depth_curve.py  -  turn the depth dial 1 to 15 and watch both scores.

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

data = load_diabetes()
X = data.data
y = data.target

# ONE split, made BEFORE the loop. If you split inside the loop you are
# measuring shuffling luck, not depth.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

depths = []          # the dial setting
train_scores = []    # score on rows it learned from
test_scores = []     # score on rows it has never seen
leaf_counts = []     # how many final answers the tree has

for depth in range(1, 16):                    # 1, 2, 3 ... 15
    tree = DecisionTreeRegressor(max_depth=depth, random_state=0)
    tree.fit(X_train, y_train)                # a FRESH tree every time round
    depths.append(depth)
    train_scores.append(tree.score(X_train, y_train))
    test_scores.append(tree.score(X_test, y_test))
    leaf_counts.append(tree.get_n_leaves())

print(f"{'depth':>5} {'leaves':>7} {'train R2':>9} {'test R2':>8} {'gap':>7}")
for i in range(len(depths)):
    gap = train_scores[i] - test_scores[i]
    print(f"{depths[i]:5d} {leaf_counts[i]:7d} {train_scores[i]:9.3f} "
          f"{test_scores[i]:8.3f} {gap:7.3f}")

best_depth = depths[int(np.argmax(test_scores))]     # the PEAK of the test line
print()
print("best test R2 was", round(max(test_scores), 3), "at max_depth =", best_depth)
print("training rows:", len(X_train), " leaves at depth 15:", leaf_counts[-1])

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(depths, train_scores, marker="o", label="train R2 (rows it learned from)")
ax.plot(depths, test_scores, marker="s", label="test R2 (rows it never saw)")
ax.axvline(best_depth, linestyle="--", color="green")     # NEW: mark the peak
ax.set_title("After depth 4 the tree is memorising, not learning")
ax.set_xlabel("max_depth (how many questions the tree may ask)")
ax.set_ylabel("R2  (1.0 = perfect, 0.0 = no better than the mean)")
ax.set_ylim(-0.2, 1.05)
ax.legend()
fig.savefig("week33_depth_curve.png", dpi=120, bbox_inches="tight")
print("saved week33_depth_curve.png")
```

Two lines are new; everything else is Weeks 7, 25 and 31.

- `for depth in range(1, 16):` — 1 up to and including 15. `range` stops one short, from Week 7.
- `DecisionTreeRegressor(max_depth=depth, random_state=0)` — **inside** the loop, so a brand-new tree is built at each setting. Building it outside the loop is a real and common mistake.
- `tree.get_n_leaves()` — how many final answers this tree has. This column is the *mechanism*, and it is the column that makes the lesson concrete.
- `int(np.argmax(test_scores))` — `argmax` gives the *position* of the biggest number in a list, not the number itself. Position 3 is depth 4, because positions start at 0.
- `ax.axvline(best_depth, linestyle="--", color="green")` — a vertical line right across the chart at that x value. `linestyle="--"` makes it dashed so it never gets mistaken for data.

**The real output:**

```text
depth  leaves  train R2  test R2     gap
    1       2     0.304    0.131   0.174
    2       4     0.447    0.295   0.152
    3       8     0.517    0.329   0.188
    4      16     0.585    0.352   0.233
    5      31     0.669    0.260   0.408
    6      55     0.747    0.221   0.526
    7      91     0.813    0.188   0.624
    8     128     0.873    0.186   0.688
    9     176     0.914    0.283   0.631
   10     221     0.938    0.117   0.821
   11     255     0.961    0.151   0.810
   12     280     0.982    0.115   0.866
   13     298     0.992    0.176   0.816
   14     314     0.996    0.132   0.864
   15     329     0.999    0.044   0.955

best test R2 was 0.352 at max_depth = 4
training rows: 353  leaves at depth 15: 329
```

![One climbs. One turns round.](../figures/fig-w33-2-train-climbs-test-falls.svg)
*Figure 33.3 — One climbs. One turns round. A rising train line is not evidence; it always rises.*

### 8. Reading the table, column by column — this is what you say in class

**`train R2` never once goes down.** 0.304 → 0.999, fifteen steps, every one of them upward. More depth is always better on the rows the tree learned from, *by construction* — a deeper tree can always do at least as well as a shallower one on those rows, because it can just ignore its extra freedom. **This column is not evidence of anything.** It is arithmetic dressed up as achievement.

**`test R2` rises to a peak at depth 4 (0.352), then falls apart** — down to 0.044 by depth 15. Depths 1 to 3 are **underfitting**: too few questions to describe 442 patients. Depths 5 to 15 are **overfitting**.

**The `gap` column tells the story in one number.** 0.152 at depth 2. **0.955** at depth 15. That 0.955 is exactly how much of the tree's apparent "performance" is memorisation and nothing else.

**The `leaves` column is the mechanism.** 2 leaves at depth 1. **329 leaves at depth 15, for 353 training patients.** Almost every patient has their own private leaf with their own private answer. The tree has not learned anything about diabetes; it has written down a phone book.

> **⚠️ Watch out — the wobbles are real and you must not over-read them.** The test line does not fall smoothly. It goes 0.352, 0.260, 0.221, 0.188, 0.186, then jumps back up to **0.283** at depth 9, then drops to 0.117. With 89 test patients, one patient is worth roughly 0.01 of R², so a jump of 0.1 is about ten patients — noticeable, but nothing like the 0.2 fall from the peak. If a student says "but depth 9 is better than depth 6, so the line doesn't really go down", they have made a sharp observation and the answer is: *"You're right that it's bumpy. Look at the trend over fifteen steps, not the step-to-step wobble. And notice the gap column never gets smaller again."*

![Mark the peak. Say the sentence.](../figures/fig-w33-4-overfitting-point-marked.svg)
*Figure 33.4 — Mark the peak. Then say it out loud: after here it is memorising.*

**The paragraph the student should be able to write by the end** — this is the target for workbook page 33.5, and it is worth reading once yourself:

> *As `max_depth` grows the tree may ask more questions, so it cuts the 353 training patients into more and more leaves. Early on each new question captures something real, so both scores rise together. Past depth 4 the questions stop describing patients in general and start describing the particular quirks of these 353. Those quirks are different in the 89 test patients, so memorising them actively hurts: train R² climbs to 0.999 while test R² sinks from 0.352 to 0.044. The gap grows from 0.152 to 0.955, and by depth 15 the tree has 329 leaves for 353 patients. Depth 4 is where it stopped learning and started memorising.*

### 9. The honesty caveat — and do not skip it

Choosing depth 4 by looking at the test scores means **the test set influenced a decision**. So the score at depth 4 is a little optimistic: you looked at those 89 patients fifteen times and picked the best-looking answer.

This is not a reason to avoid the method — it is the best method available with 442 rows. It is a reason to **write the caveat down next to the number**. The sentence to teach, verbatim:

> *"I chose the depth by looking at the test curve, so this score is slightly optimistic."*

The professional fix is called cross-validation and it is waiting in Level 3. Today, honesty in writing is the fix.

### 10. The three misconceptions you will actually meet

**Misconception 1 — "the unlimited tree is broken."**

It is working perfectly. It did exactly what it was asked: split until every leaf is pure. Nothing failed, nothing errored, and it got 1.000 on the rows it learned from. **The failure is not in the code, it is in what we asked for.** That distinction is the reason this lesson exists.

**Misconception 2 — "so deeper is bad; use depth 1."**

No. Depth 1 scores 0.131 on the test rows — barely better than guessing the average. Depth 1 and depth 15 are both wrong, **for opposite reasons**: depth 1 has not learned enough, depth 15 has learned things that were never true in general. The answer is in the middle and you find it by looking. If you only ever remember one thing from this table, make it *"both ends are wrong"*.

**Misconception 3 — "the training score is useless, so don't compute it."**

Compute it always. It is useless *on its own*, as evidence of quality. It is essential as **half of the gap**, and the gap is your diagnosis. Train high and test low means overfitting; train low and test low means underfitting; you cannot tell those apart without the training number. One score tells you nothing. Two scores tell you which of four situations you are in.

### 11. Where to stop

**Go this far:** the four-row diagnosis table; the dial; RMSE and why it differs from MAE; the depth curve; the peak marked and named; the honesty sentence.

**Stop before:**

- **Cross-validation.** Level 3. Name it once, in the honesty caveat, and move on.
- **Regularisation, pruning, `min_samples_leaf`.** All real, all next year.
- **Random forests.** *"Hundreds of trees voting. Better scores, unreadable. Level 3."*
- **The bias–variance decomposition.** The words are not needed and the algebra actively gets in the way at this age.
- **Explaining the depth-9 bump properly.** It is noise on 89 patients. "Bumpy, look at the trend" is the correct and complete answer.

---

### 12. 🧭 The Growing Map — two minutes on the curve, and a map that does not move

Each week the student guide carries the same pipeline with one more piece filled in, so the learner can
see the year's shape rather than only this week's content. This week the picture is unchanged from last
week's, which is useful: the thing that moved today was not the map, it was what they can now *see*
inside one box.

![The Level 2 pipeline in Week 33: still the bake-off and capstone tile, now two scores and the overfitting curve](../figures/fig-w33-0-where-this-fits.svg)

*Figure 33.0 — Week 33's version. Second week inside `bake-off · capstone`, weeks 32 to 36, and nothing
has moved. Two threads lit: learning signal and evaluation.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and ask what today added, given that the map is identical:** *"same box as last week — so
   what have we got now that we did not have at four o'clock yesterday?"* You want **a second score**,
   or **the training score as well as the test score**. Then the harder half: *"and which of the two
   numbers in the 1.000 / −0.003 row was the honest one?"* They will point at the negative. Let it land.
2. **Then the dial question, with a finger on the peak:** *"the two lines split apart after depth 4.
   Which way do you turn the dial — up or down?"* **Down.** This is the counter-intuitive instinct of
   the whole level, and a learner who can say *turn it down* while pointing at a picture has it in a way
   that no definition of overfitting supplies.
3. **Have them ink the tile again and draw the curve thumb-sized beside it** — two lines, peak circled,
   the word *memorising* after the peak. Small on purpose. Gate 6 of the Level 3 check in Week 36 is
   exactly this drawing, on a napkin, from memory.

> **🧑‍🏫 Why this is worth two minutes.** The bake-off produces a lot of numbers, and the risk of today
> is that they remember "kNN won" instead of "one score is not a result". The map is where you make the
> *method* the memory: same box, same four steps, two numbers instead of one. It also sets up the honest
> caveat so it does not feel like a technicality — 329 leaves for 353 patients is a phone book, and the
> next three weeks are graded on whether they can say something that plain about their own model.

---

## 🧰 Prep Checklist

### 25 minutes the night before

- [ ] **Print workbook pages 33.1–33.6.** Page 33.4 (the blank depth-curve grid) should be printed **twice**.
- [ ] **Go and find the Week 29 numbers.** Whatever the student wrote down four weeks ago about their training score and their held-back score. A photo, a notebook page, a wiped whiteboard you have to reconstruct — get it now. The lesson ends there and it is much weaker without it.
- [ ] **Run the bake-off yourself.**

  ```
  cd ~/ai-academy/level2
  source .venv/bin/activate        # macOS / Linux
  .venv\Scripts\activate           # Windows PowerShell
  ```

  Type `week33_bakeoff.py` from section 5 and run it. **Check one row above all others:**

  ```
  tree, no limit           56.57   72.90    -0.003      1.000
  ```

  If you see `1.000` and `-0.003` on the same line, your machine agrees with this guide and the lesson will work.

- [ ] **Run the depth curve.** Type `week33_depth_curve.py` from section 7 and run it. Check `best test R2 was 0.352 at max_depth = 4` and `leaves at depth 15: 329`. Then **open `week33_depth_curve.png` and look at it.** You need to have seen the shape before you ask a 12-year-old to find it.
- [ ] **Break it on purpose, twice.**

  First, the one a student will hit from searching online. Replace the RMSE line with `mean_squared_error(y_test, guesses, squared=False)`:

  ```text
  TypeError: got an unexpected keyword argument 'squared'
  ```

  Second, delete `tree.fit(X_train, y_train)` from inside the loop:

  ```text
  sklearn.exceptions.NotFittedError: This DecisionTreeRegressor instance is not fitted yet. Call 'fit' with appropriate arguments before using this estimator.
  ```

  Put both back. You are staging both live.

- [ ] **Read the Sam analogy in section 1 out loud once.** You are going to tell it as a story, not read it, and it needs to be yours.
- [ ] **Read section 3's warning about RMSE.** It is the one place in this week where the obvious thing to say is not quite true, and a sharp student can catch you.

### 5 minutes on the day

- [ ] Terminal open, environment activated, `(.venv)` visible.
- [ ] `week31_tree_iris.py` and `week32_study_line.py` open in tabs. You will point at them, not run them.
- [ ] The Week 29 numbers on a card, face down, on the table. Do not show them yet.
- [ ] Graph paper, ruler, **four coloured pens**.
- [ ] Bug Log open at a clean page.

### Fallback if something fails

| If this fails | Do this instead |
|---|---|
| **No laptop today** | This lesson survives on paper better than you would think. Print the two output blocks from sections 5 and 7. The student plots the depth curve **by hand** from the printed table onto graph paper — fifteen points, two colours — draws the vertical line at the peak, and writes the paragraph. That delivers objectives 3, 4 and 5, which are the three that matter most. Objectives 1 and 2 wait one session. |
| **`matplotlib` will not show a window** | Expected, and irrelevant. The script calls `fig.savefig(...)`; open `week33_depth_curve.png` from the folder. |
| **The loop takes a noticeable time** | It should not — the whole thing is well under a second. If it hangs, you have almost certainly put `range(1, 16)` inside another loop by accident. |
| **The student's numbers differ** | Check `random_state=42` in the split and `random_state=0` in every tree. Then check the split is **outside** the loop. Those two things account for nearly every discrepancy. |
| **The depth-9 bump derails everything** | Do not improvise. Use the prepared answer: *"It's bumpy because 89 test patients is not many — one patient is worth about 0.01. Look at the trend across fifteen steps, and look at the gap column, which never shrinks again."* |
| **Running long and the plot is not done** | Cut the plot, keep the table. Have them highlight the peak of the `test R2` column with a coloured pen and write the sentence next to it. The picture is lovely; the table is the lesson. |
| **The student is upset that the tree "lost"** | Genuinely happens after two weeks of enjoying trees. Say: *"It lost on score and it still wins on being readable. Which one you need depends on the job."* Then show them the line's coefficients and ask which they would rather explain to a doctor. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Sam got 200 out of 200 | 7 | 7 | A perfect practice score that means nothing |
| 🧠 Concept — the four-row diagnosis, and RMSE | 16 | 23 | Underfit / just right / overfit / broken; MAE vs RMSE by hand |
| 💻 Live-Code Together — the bake-off | 18 | 41 | One split, four entries, two staged bugs, the 1.000 / −0.003 row |
| 🎲 Their Turn — the depth curve | 20 | 61 | The loop, the table, the plot, the axvline, the sentence |
| 🔑 Wrap & Assign | 9 | 70 | Back to Week 29's board; three checks; homework |

---

### 🪝 Hook — Sam got 200 out of 200 (7 minutes)

**Do this:** Laptop closed. Tell it as a story, not as a lesson.

**Say this:**

> "Three people in a class, all doing the same maths test on Friday. The teacher gives out a booklet of 200 practice questions on Monday, with the answers in the back.
>
> **Ravi** flicks through the chapter headings on Thursday night. He can't do the practice questions and he can't do the test. Fair enough — he never learned it.
>
> **Priya** works through the practice questions properly, gets stuck, works out the method. She does well on the practice and she does well on the test.
>
> **Sam** does something different. Sam memorises all 200 practice questions and their answers. Word for word. Question 47, answer 12. Question 48, answer minus 3. All of them.
>
> On the practice booklet, Sam scores **200 out of 200**. Perfect. Better than Priya.
>
> Friday comes, and the test has different numbers in it.
>
> What happens to Sam?"

Let them answer. Then:

> "He falls apart. And here's what I want you to hold onto, because it's not obvious.
>
> **Sam's 200 out of 200 was not a lie.** He didn't cheat. He really did get every single practice question right. That number is completely true.
>
> **It just isn't evidence of anything.**
>
> Today you're going to build Sam. In code. On purpose. And you're going to watch a model score a *perfect* one point zero zero zero on the questions it studied, and then do no better than guessing the average on questions it hasn't seen. And then you're going to draw the picture of it happening."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "What did Sam learn?" | The questions, not the maths. | If they say "nothing", push gently: he learned 200 question-answer pairs. That is real learning of the wrong thing. |
| "Was Sam's 200/200 a lie?" | No. It was true and useless. | If they say "yes, he cheated" — worth two minutes. He didn't cheat; he was given the answers and he memorised them. The problem is what we concluded from the score. |
| "How would you catch Sam on Monday, before Friday?" | Give him a question that isn't in the booklet. | This is the whole idea of a test set, arrived at by them. If they say it, stop and say so: "That's what `train_test_split` has been doing since Week 29." |
| "Could a computer do what Sam did?" | Yes — memorise the training rows instead of the pattern. | If they say no, promise them the row: "Give me fifteen minutes and I'll show you a perfect 1.000 that's worthless." |

---

### 🧠 Concept — the four-row diagnosis, and RMSE (16 minutes)

**Do this:** Write the four-row table on the big sheet as you talk it. Get the four coloured pens out.

**Say this — part 1, the diagnosis table:**

> "You've been computing two scores since Week 29 — one on the rows the model learned from, one on the rows you hid. Today those two numbers finally earn their keep, because **together** they diagnose your model. Separately, neither does.
>
> Four possibilities, and that's all there are."

Write it as you go:

```
   train    test     what it is
   ------   ------   -------------------------------------
   low      low      UNDERFITTING   - too simple  (Ravi)
   high     high     JUST RIGHT     - it learned  (Priya)
   high     LOW      OVERFITTING    - memorised   (Sam)
   low      high     something's broken - go and read your code
```

> "Ravi, Priya, Sam. And the fourth row is a bug — if you're doing better on rows you've never seen than on rows you studied, something has gone wrong in your code, or your test set is tiny and you got lucky.
>
> And the difference between the two numbers has a name. **Train score minus test score is the gap.** Small gap, it generalises. Big gap, it's memorising. **The gap is the size of the Sam problem.**"

**Say this — part 2, the dial:**

> "Now — what made Sam Sam? He had too much *room*. He had enough memory to store 200 answers, so he did.
>
> Every model has a dial that controls how much room it's got. And you already know the tree's one: **`max_depth`.**
>
> Depth 1, the tree can ask one question, so it can only give two different answers. Not much room. Depth 15? It can ask fifteen questions in a row, which means up to thirty-two *thousand* different endings. If you've only got 353 patients, it can give nearly every single one their own private answer.
>
> That's Sam. Not a metaphor — that is literally writing down 353 answers instead of learning a pattern.
>
> That dial has a name: **model complexity**. How much freedom the model has to bend around your data."

**Say this — part 3, RMSE, and do the arithmetic together:**

> "One new score today, and it exists because MAE can't see something important.
>
> Two models, ten predictions each.
>
> **Model A** is off by exactly one, every single time. Ten misses of 1.
> **Model B** is *perfect* nine times and then off by ten once.
>
> Work out MAE for both."

Do it out loud together.

```
   Model A:  (1+1+1+1+1+1+1+1+1+1) ÷ 10 = 10 ÷ 10 = 1.0
   Model B:  (0+0+0+0+0+0+0+0+0+10) ÷ 10 = 10 ÷ 10 = 1.0
```

> "**Identical.** MAE says these two models are exactly as good as each other. Does that feel right to you?"

Let them object. Then:

> "So here's the other way. **Square every miss first**, then average, then square-root at the end to get back into the right units. It's called **RMSE** — root mean squared error, and you read it backwards: square the errors, take the mean, take the root."

```
   Model A:  squares are 1,1,1,1,1,1,1,1,1,1  → mean 1   → √1  = 1.000
   Model B:  squares are 0,0,0,0,0,0,0,0,0,100 → mean 10 → √10 = 3.162
```

> "Same MAE. RMSE more than three times apart. **Squaring makes a big miss count much more than several small ones** — because 10 squared is 100, and ten separate 1s only add up to 10.
>
> Which model is better? **It depends on what a big miss costs you.** Nine perfect deliveries and one disaster, or ten slightly-late ones? For a pizza, ten slightly-late is fine. For a hospital, one disaster is not.
>
> So you don't pick the metric because it's the nice one. You pick it because of what you're afraid of."

> **⚠️ Watch out:** do not say "RMSE tells you the worst miss". It does not, and today's own numbers will contradict you inside twenty minutes. Say: *"RMSE goes up faster than MAE when there are big misses."*

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Train 0.99, test 0.62. Which row?" | Overfitting. Big gap. | If they say "good, 0.99 is great", point at the 0.62 and at Sam. |
| "Train 0.31, test 0.28. Which row?" | Underfitting. Both low, tiny gap. | If they say overfitting, ask which number is high. Neither. Underfitting is the *only* row where nothing is high. |
| "Which is worse, Ravi or Sam?" | Sam, usually — because Ravi's bad score tells you he's bad, and Sam's good score tells you he's good when he isn't. | Any argued answer earns credit. Push for the reason. The killer point: an underfit model is honest about being bad. |
| "Model A and Model B have the same MAE. Which would you rather have for a hospital's medicine dose?" | Model A — small consistent errors beat one catastrophe. | If they say B, ask what happens to the one patient. Then agree that for a *grocery bill* B is better, and that is the point. |
| "So should we always use RMSE?" | No — pick it based on what a big miss costs. Report both. | If they want one rule, give them the habit instead: print MAE, RMSE and the worst single miss. Three numbers, no rule needed. |

---

### 💻 Live-Code Together — the bake-off (18 minutes)

**You type, the student types.** Both bugs are staged.

**Step 1 (4 min) — one split, and the fairness comment.** New file, `week33_bakeoff.py`:

```python
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

data = load_diabetes()
X = data.data
y = data.target
print("rows and columns:", X.shape)
print("the answer runs from", y.min(), "to", y.max())

# ---- ONE split. Made once, here, at the top. Never made again. ----------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
print("train rows:", len(X_train), " test rows:", len(X_test))
```

```text
rows and columns: (442, 10)
the answer runs from 25.0 to 346.0
train rows: 353  test rows: 89
```

**Say this:**

> "New dataset, and it's not flowers. **442 real diabetes patients**, ten measurements each — age, body mass index, blood pressure, six blood tests — and the answer is how far the illness had moved on a year later. A number from 25 to 346.
>
> Two warnings. First, **real data is much noisier than flowers.** The best score anybody gets today is about 0.45, not 0.97. That's not us being bad at this. That's what actual data looks like.
>
> Second, look at that comment I made you type. **One split, at the top, never again.** Every model below sees the same 353 patients to learn from and the same 89 to be tested on. That sentence being true is the *entire* fairness of a bake-off. If I re-split for each model, one of them gets an easier test and I'd never know."

> **🧑‍🏫 If a student asks:** *"Where's the `StandardScaler`? Week 30 said kNN needs it."* — that is an excellent catch and you should say so. Answer: *"You're right to check. This dataset arrived already scaled — whoever prepared it did it for us. If it hadn't been, kNN would need it and the tree wouldn't."*

**Step 2 (4 min) — 🐞 STAGED MISTAKE ONE: the RMSE shortcut that no longer exists.** Add:

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression

model = LinearRegression().fit(X_train, y_train)
guesses = model.predict(X_test)
print("MAE :", round(mean_absolute_error(y_test, guesses), 2))
print("RMSE:", round(mean_squared_error(y_test, guesses, squared=False), 2))
```

```text
Traceback (most recent call last):
  File "week33_bakeoff.py", line 19, in <module>
    print("RMSE:", round(mean_squared_error(y_test, guesses, squared=False), 2))
  ...
TypeError: got an unexpected keyword argument 'squared'
```

**Say this:**

> "Read the last line. `unexpected keyword argument 'squared'`.
>
> Now — I did that on purpose, and not to be annoying. If you search the internet for 'how do I get RMSE in scikit-learn', that `squared=False` is what you'll find, in about a thousand places. It **used** to work. It was removed.
>
> That's a thing that will happen to you for the rest of your life with code: the internet is full of instructions that were true once. And the error message is how you find out. **The error is more up to date than the tutorial.**
>
> So we do it the way that will always work: get the mean of the squares, then take the square root ourselves."

```python
print("RMSE:", round(np.sqrt(mean_squared_error(y_test, guesses)), 2))
```

```text
MAE : 42.79
RMSE: 53.85
```

> "`mean_squared_error` gives you the average of the squared misses. `np.sqrt` — Week 28 — takes the square root and brings it back into the right units. Read the name backwards: **root, of the mean, of the squared errors.**"

**Step 3 (5 min) — one function, four entries.** Say: *"Now we could copy-paste that for each model. Don't. Here's why."*

Rewrite as a function:

```python
def report(name, model):
    """Fit a model on the SAME train rows, score it on the SAME test rows."""
    model.fit(X_train, y_train)
    guesses = model.predict(X_test)
    mae = mean_absolute_error(y_test, guesses)
    rmse = np.sqrt(mean_squared_error(y_test, guesses))
    print(f"{name:22s} {mae:7.2f} {rmse:7.2f} "
          f"{r2_score(y_test, guesses):9.3f} {model.score(X_train, y_train):10.3f}")
```

**Say this:**

> "One function, used for every model. Why does that matter?
>
> Because if you write the scoring out four separate times, sooner or later you'll type `y_train` where you meant `y_test` in exactly one of them — and it won't error. It'll just print a nicer number for that one model, and you'll believe it. **A single function makes it impossible to score two models differently by accident.** That's not tidiness. That's fairness."

Now the header, the lazy baseline, and the models:

```python
print(f"{'model':22s} {'MAE':>7s} {'RMSE':>7s} {'test R2':>9s} {'train R2':>10s}")

# the laziest model there is: ignore all 10 columns, always say the training mean
lazy = np.zeros(len(y_test)) + y_train.mean()
print(f"{'always guess the mean':22s} "
      f"{mean_absolute_error(y_test, lazy):7.2f} "
      f"{np.sqrt(mean_squared_error(y_test, lazy)):7.2f} "
      f"{r2_score(y_test, lazy):9.3f} {0.0:10.3f}")

report("kNN, k = 5", KNeighborsRegressor(n_neighbors=5))
report("tree, max_depth=5", DecisionTreeRegressor(max_depth=5, random_state=0))
report("tree, no limit", DecisionTreeRegressor(random_state=0))
report("linear regression", LinearRegression())
```

And the two imports at the top:

```python
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
```

> "Notice those two names. `KNeighborsRegressor` and `DecisionTreeRegressor` — the exact tools from Weeks 29 and 31, with **`Regressor`** on the end instead of `Classifier`, because the answer is a number now. Same tool, different answer type. That naming rule is worth remembering; it saves you looking things up.
>
> And the baseline. **Always compute the laziest possible model.** This one ignores all ten measurements and says the average, every time, for all 89 patients. Without it, none of the other numbers means anything."

Run it:

```text
model                      MAE    RMSE   test R2   train R2
always guess the mean    64.01   73.22    -0.012      0.000
kNN, k = 5               42.77   54.95     0.430      0.584
tree, max_depth=5        48.15   62.60     0.260      0.669
tree, no limit           56.57   72.90    -0.003      1.000
linear regression        42.79   53.85     0.453      0.528
```

**Step 4 (5 min) — the row. Slow down. This is the summit of the term.**

**Say this:**

> "Right. Put your finger on the row that says `tree, no limit`, and read me the last two numbers."

Wait. Let them say it.

> "**Train R² one point zero zero zero.** Not 0.99. *Perfect.* On the 353 patients it learned from, that tree is never wrong. Not once. Out of 353.
>
> And **test R² minus nought point nought nought three.** Negative.
>
> What does a negative R² mean? Look up at the baseline row. R² of zero means 'no better than ignoring everything and guessing the average'. So negative means…"

Let them get there.

> "**Worse than guessing the test rows' average — or, near zero, no better than it.** A model with ten measurements, hundreds of learned rules, a perfect score on its homework — and on new patients it is *no better than a machine that ignores every measurement and says 153 every single time* (that machine scored −0.012; the tree −0.003).
>
> That is Sam. That's Sam in numbers you just generated, on your own laptop, in a tenth of a second.
>
> Now look at the two trees together." *(Point.)* "Depth 5: train 0.669, test 0.260. No limit: train 1.000, test −0.003. **We made the training score better and the model worse.** Every single time you turn that dial up, the training score improves. And past a point, the model gets worse.
>
> Which is why — say it with me — **the training score is not evidence.**"

Then one more pass, and this one is quieter but it matters:

> "Two more things in this table.
>
> Compare kNN and the line on **MAE**: 42.77 and 42.79. That's a dead heat — two hundredths apart, on a scale that goes to 346. Now compare them on **RMSE**: 54.95 and 53.85. The line wins. Why?
>
> Because kNN has nine misses bigger than 100 and the line has only five. Typical performance, identical. Big-miss behaviour, the line's better. **MAE couldn't see that. RMSE could.** That's why you print both.
>
> And the last thing, which is a bit of a blow after the last two weeks: **the tree lost.** 0.260 against the line's 0.453. Trees aren't the best tool for everything. My best guess, and we haven't tested it, is that these are smooth medical measurements with no sudden cut-offs in them, which is exactly the shape a line handles well and a staircase handles badly. The tree still wins on one thing — you can read it — and this week is the week you find out what that costs."

---

### 🎲 Their Turn — the depth curve (20 minutes)

Full instructions in the Activity section. In the lesson flow:

- **Minutes 0–7:** type the loop (with staged bug two), get the table printed.
- **Minutes 7–12:** highlight the table with coloured pens — train column, test column, gap column, leaves column.
- **Minutes 12–17:** the plot, the `axvline`, and open the PNG.
- **Minutes 17–20:** draw the vertical line on the printed graph paper too, label it, and say the sentence out loud.

---

### 🔑 Wrap & Assign (9 minutes)

**Do this first — and this is the part you prepared for.** Turn over the card with the Week 29 numbers on it.

**Say this:**

> "Four weeks ago you trained your first model and you wrote down two numbers: how it did on the rows it learned from, and how it did on the rows you hid. Here they are.
>
> Look at the gap between them. You wrote that gap down four weeks ago and I told you we'd come back to it.
>
> **That gap has a name now.** It's the train/test gap, and it's the size of the memorising. Four weeks ago it was just an odd thing you noticed. Today you can name it, you can draw it, and you know which way to turn the dial."

Then the three takeaways:

> "**One.** The training score always goes up when you give a model more room. Always. So it is arithmetic, not evidence. Only the test score — rows the model has never seen — tells you anything.
>
> **Two.** Both ends of the dial are wrong, and they're wrong for opposite reasons. Depth 1 hasn't learned enough. Depth 15 has learned things that were never true. The answer's in the middle and you find it by drawing the picture.
>
> **Three.** And write this down word for word, because it's the honest bit: **'I chose the depth by looking at the test curve, so this score is slightly optimistic.'** You looked at those 89 patients fifteen times and picked the best-looking answer. There's a proper fix for that and it's next year. This year, the fix is saying so."

Run the three checks in **Assessing Understanding**, then set the homework. Both tracebacks into the Bug Log before the laptop closes.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `TypeError: got an unexpected keyword argument 'squared'` | That setting no longer exists. | `mean_squared_error(..., squared=False)`, copied from an out-of-date tutorial. | `np.sqrt(mean_squared_error(y_true, y_pred))`. The error is more current than the tutorial. |
| `sklearn.exceptions.NotFittedError: This DecisionTreeRegressor instance is not fitted yet. Call 'fit' with appropriate arguments before using this estimator.` | You scored a model that never learned anything. | `tree.fit(X_train, y_train)` is missing from inside the loop. | Put it in, above the two `.score()` calls. A fresh model each time round means a fresh `fit` each time round. |
| `NameError: name 'd' is not defined. Did you mean: 'id'?` | You used a loop variable that does not exist. | The loop says `for depth in range(1, 16):` but the model says `max_depth=d`. | Make them match. Pick one name and use it in both places. |
| `NameError: name 'DecisionTreeRegressor' is not defined` | The tool was never imported. | Only `DecisionTreeClassifier` is on the import line, from Week 31. | `from sklearn.tree import DecisionTreeRegressor` — or list both, comma-separated. |
| `AttributeError: 'tuple' object has no attribute 'plot'` | You are calling `.plot` on a pair of things, not on the axes. | `ax = plt.subplots(...)` instead of `fig, ax = plt.subplots(...)`. | `fig, ax = plt.subplots(figsize=(8, 5))`. `subplots` always hands back two things. |
| `AttributeError: 'list' object has no attribute 'mean'` | Plain Python lists cannot do maths on themselves. | `y_train` got turned into a list somewhere, then `.mean()` was called on it. | Keep it as a numpy array, or use `sum(y_train) / len(y_train)`. |
| `ValueError: 'dashed--' is not a valid value for ls; supported values are '-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted'` | matplotlib does not recognise that line style. | Typed `linestyle="dashed--"`, mixing the two spellings. | Pick one: `linestyle="--"` **or** `linestyle="dashed"`. The error helpfully lists every legal value. |
| `ImportError: cannot import name 'load_diabetis' from 'sklearn.datasets'` | The department is right, the dataset name is not. | Spelling — `diabetis`. | `load_diabetes`. |
| `TypeError: missing a required argument: 'y_pred'` | A scoring function needs two lists and got one. | `mean_squared_error(y_test)` — the guesses were left out. | `mean_squared_error(y_test, guesses)`. Truth first, guesses second. |

### The two bugs that do **not** raise an error — and are far worse

Both of these run cleanly and print a plausible wrong answer. Teach the student to look for them, because Python will not help.

**1. Re-splitting inside the loop.**

```python
for depth in range(1, 16):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)   # ← WRONG
    tree = DecisionTreeRegressor(max_depth=depth, random_state=0).fit(X_train, y_train)
```

No error. It just measures how lucky each shuffle was, rather than what depth does, and the curve comes out as a jagged mess with no shape. **The check:** the split must be *above* the `for`, and there must be exactly one `train_test_split` in the whole file. Have them count.

**2. Arguments the wrong way round in `r2_score`.**

```python
r2_score(guesses, y_train)   # wrong order
r2_score(y_train, guesses)   # right order
```

Real numbers from this week's tree: **0.504** the wrong way round, **0.669** the right way round. Both look perfectly believable and only one is the model's R². **The check:** truth first, guess second, in every metric, every time.

### How to teach debugging without giving the answer

1. **"Read me the last line, out loud."** Every time. It is a sentence.
2. **"Does the message list the legal options?"** This week, twice, it does — the `linestyle` error prints every valid value. Students skip that because the block looks like noise.
3. **"Count your `train_test_split` lines."** For the silent bugs, counting beats reading. There must be exactly one, and it must be above the loop.

---

## 🎲 The Activity, In Full

### Setup

**On the table:** graph paper, a ruler, **four coloured pens**, workbook pages 33.3 and 33.4, a calculator. Laptop open with `week33_bakeoff.py` already working.

### Step 1 — type the loop, and 🐞 STAGED BUG TWO (7 minutes)

New file, `week33_depth_curve.py`. Have them type it with `tree.fit(...)` deliberately left out:

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

data = load_diabetes()
X = data.data
y = data.target

# ONE split, made BEFORE the loop.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

depths = []
train_scores = []
test_scores = []
leaf_counts = []

for depth in range(1, 16):
    tree = DecisionTreeRegressor(max_depth=depth, random_state=0)
    depths.append(depth)
    train_scores.append(tree.score(X_train, y_train))
```

```text
Traceback (most recent call last):
  File "week33_depth_curve.py", line 22, in <module>
    train_scores.append(tree.score(X_train, y_train))
  ...
sklearn.exceptions.NotFittedError: This DecisionTreeRegressor instance is not fitted yet. Call 'fit' with appropriate arguments before using this estimator.
```

**Say this:**

> "`not fitted yet`. I built a brand-new tree and asked it how it did — before it had learned anything.
>
> And here's the important bit, and it's why I made you get this error: **we build a brand-new tree every single time round this loop.** Fifteen trees. Which means fifteen separate `fit` calls. If you build the tree once *outside* the loop and only change the depth, you don't get fifteen trees — you get one tree, fifteen times, and your curve is flat."

Add the fit, and the rest:

```python
    tree.fit(X_train, y_train)                # a FRESH tree every time round
    test_scores.append(tree.score(X_test, y_test))
    leaf_counts.append(tree.get_n_leaves())
```

Then the printing block from section 7. Run it. The table appears.

### Step 2 — mark up the table with four pens (5 minutes)

This is the part that makes the numbers speak, and it takes coloured pens rather than code.

| Pen | What to mark | What they should say when they finish |
|---|---|---|
| Pen 1 | The whole **`train R2`** column, top to bottom | "It never goes down. Not once, in fifteen steps." |
| Pen 2 | The single biggest number in **`test R2`** | "0.352, at depth 4." |
| Pen 3 | The **first** and **last** numbers in the **`gap`** column | "0.174 up to 0.955." |
| Pen 4 | The **last** number in **`leaves`**, and the printed `training rows: 353` | "329 leaves for 353 patients." |

Then, out loud, in this order: *"Train always rises. Test peaks at depth 4. The gap grows from 0.17 to 0.96. And by the end there are almost as many leaves as patients."*

### Step 3 — plot it (5 minutes)

```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(depths, train_scores, marker="o", label="train R2 (rows it learned from)")
ax.plot(depths, test_scores, marker="s", label="test R2 (rows it never saw)")
ax.axvline(best_depth, linestyle="--", color="green")
ax.set_title("After depth 4 the tree is memorising, not learning")
ax.set_xlabel("max_depth (how many questions the tree may ask)")
ax.set_ylabel("R2  (1.0 = perfect, 0.0 = no better than the mean)")
ax.set_ylim(-0.2, 1.05)
ax.legend()
fig.savefig("week33_depth_curve.png", dpi=120, bbox_inches="tight")
```

Week 25's rules hold in full: title, both axis labels, a legend because there are two series, and `set_ylim` so the reader can see how far from 1.0 things are.

> **💡 Try this:** `ax.set_ylim(-0.2, 1.05)` matters more than it looks. Without it matplotlib zooms to fit, the test line fills the frame, and the *distance* between the two lines stops being visible. The gap is the story; do not let the axes hide it.

`ax.axvline(4, linestyle="--")` draws one vertical line straight across the chart at x = 4. Dashed, so nobody mistakes it for data.

### Step 4 — draw it by hand, and say the sentence (3 minutes)

**Do this on paper as well as on screen.** Hand them the graph paper.

Two colours, fifteen points each, plotted from the printed table. Then the ruler, straight down at depth 4, and next to it, in their own handwriting:

```
   after here it is memorising
```

**Then they say it out loud.** Not read it — say it, pointing at the line.

This is not a decoration. It is the single sentence this whole term has been building towards, and writing it in their own hand next to a line they drew themselves is what makes it stick.

### What "finished" looks like

- A results table with **five** entries, including the lazy baseline, with MAE, RMSE, test R² and train R² for each.
- The `tree, no limit` row circled, with `1.000` and `-0.003` both marked.
- The depth table printed and marked up in four colours.
- A two-line chart, saved as a PNG, fully labelled, with a dashed vertical line at depth 4.
- The same curve drawn by hand on graph paper, with the line and the sentence.
- One model named as "the one I would ship", with a written reason citing at least two numbers.

![One split. Three models. One table.](../figures/fig-w33-3-same-split-three-models.svg)
*Figure 33.5 — One split, three models, one table. Fairness is one sentence: every model saw the same 353 rows.*

### Variation — easier

- **Cut the bake-off to three rows:** the lazy baseline, `tree, no limit`, and `linear regression`. That is enough to show a perfect training score next to a test score no better than guessing, which is the whole lesson.
- **Shorten the loop to `range(1, 11)`.** Ten points instead of fifteen. The peak is still at depth 4 and the shape is identical.
- **Skip the code for the curve entirely.** Hand them the printed table from section 7 and have them plot it by hand on graph paper. **Plotting it by hand is arguably the better exercise** — it takes ten minutes and every single point has to pass through their eyes.
- **Do the marking-up in two colours, not four:** train and test only.
- **Give them the sentence to copy**, rather than asking them to compose it. Copying it in their own handwriting under a line they drew is still worth a great deal.

### Variation — harder

1. **Find the depth where train first hits 1.000.** On this data the tree with no limit reaches a real depth of 19 with 346 leaves. Run `DecisionTreeRegressor(random_state=0)` and print `get_depth()` and `get_n_leaves()`. Then the question: *"You set `max_depth=25`. Why does `get_depth()` say 19?"* (Because `max_depth` is a **ceiling, not a target** — the tree stops when there is nothing impure left to split.)
2. **Turn the kNN dial instead.** Loop `n_neighbors` from 1 to 25, recording train and test R². The curve runs **backwards**, because `k = 1` is the complex end. At `k = 1` the train score is a perfect 1.000 — every point is its own nearest neighbour. *"You've just found Sam again, in a different model."*
3. **Explain the depth-9 bump.** Test R² jumps from 0.186 to 0.283 and then falls to 0.117. *"Is depth 9 genuinely better than depth 6? How would you find out?"* (One test patient is worth about 0.01 of R², so 0.1 is about ten patients. Re-run with a different `random_state` on the split and watch the bump move or vanish (and notice the peak depth moves too: with `random_state=1` it is depth 2, so "depth 4" belongs to this split). That is the honest answer, and it is a real technique.)
4. **Argue the shipping decision properly.** The line wins on test R² (0.453) and RMSE (53.85). The depth-4 tree scores 0.352 — but it can be printed as rules a doctor could read. *"Which do you ship, and to whom?"* Insist on numbers *and* a named audience in the answer. There is no single right answer and the reasoning is the marks.
5. **Break the fairness on purpose.** Move `train_test_split` inside the loop and remove `random_state` from it. Run it. The curve becomes a jagged mess with no shape at all. *"Nothing errored. What exactly is this chart measuring?"* (Shuffle luck.) A student who has seen a silent bug produce a confident wrong picture will check for it forever.

---

## ❓ Questions Students Ask This Week

**"How can a score be negative? I thought 0 was the worst."**

R² is not a percentage, so 0 is not a floor. R² of 0 means "exactly as good as ignoring every measurement and guessing the average". You can absolutely be *worse* than that: predict wildly, and your squared errors come out bigger than the average-guesser's, and R² goes below zero. The unlimited tree lands right at that level (−0.003 against the baseline's −0.012). Negative R² is not a bug; it is a model telling you it has actively hurt you.

**"Why does the training score always go up? Couldn't a deeper tree be worse on training?"**

No, and this is worth understanding rather than believing. A deeper tree can always do *at least* as well on the training rows as a shallower one, because it can simply choose not to use its extra questions — it has every option the shallow tree had, plus more. So its training score can never be lower. That is why the column climbs with mathematical certainty and why it is not evidence: a number that can only go up cannot tell you whether you improved anything.

**"Which one should we actually use?"**

On these numbers, linear regression: best test R² (0.453), best RMSE (53.85), MAE level with kNN, and a small gap between train and test (0.528 versus 0.453) so it is not memorising. But notice what "should" is doing in that question. If a doctor had to explain a prediction to a patient, the depth-4 tree might win despite scoring lower, because you can print its rules and read them aloud. **The highest-scoring model is not automatically the one you ship**, and being able to say why is worth more than picking right.

**"Is depth 4 the answer for all trees, always?"**

No, and there is no such number. It depends on how many rows you have, how noisy they are, how many features there are, and how much the world has changed since you collected them. Depth 4 is the answer *for this dataset, on this split*. On the iris flowers, depth 3 was fine. The transferable thing is not the number 4; it is the **method** — turn the dial, plot both scores, look at the peak.

**"Our tree's test score jumped back up at depth 9. Doesn't that break the story?"**

It is a genuinely sharp observation and the honest answer is: the curve is bumpy because 89 test patients is not very many. One patient is worth about 0.01 of R², so a jump of 0.1 is about ten patients changing sides. Look at the trend across all fifteen steps rather than step to step — and look at the `gap` column, which grows almost monotonically from 0.17 to 0.96 and never recovers. If you want to test it properly, re-run with a different `random_state` on the split and watch whether the bump survives. With `random_state=1` it does not, and the whole curve shifts too: the test peak moves to depth 2 (0.232) and R² goes negative from depth 5, so the peak depth is split-dependent.

**"If the training score is useless, why compute it at all?"**

Because it is useless *on its own* and essential as half of the gap. Test score low, on its own, could be underfitting or overfitting — two opposite problems with opposite fixes. Add the training score and you know instantly: train also low means underfitting, turn the dial *up*; train high means overfitting, turn it *down*. One number is a mystery. Two numbers are a diagnosis.

**"Should I report MAE or RMSE?"** *(Answer this one honestly: nobody fully agrees.)*

**People genuinely disagree about this, and it is not a gap in your knowledge — it is a real argument with two defensible sides.** MAE asks *"how wrong am I on a typical day?"* RMSE asks *"how bad does it get?"* Our Model A and Model B have **identical** MAE and RMSE values three times apart, so the choice of metric decides which model wins — and that means choosing the metric is really choosing which question your project is about. One camp says report MAE, because it is the honest description of the typical case and it is the one you can say out loud to a non-technical person; RMSE, they argue, lets a single freak outlier dominate a headline number and makes models look worse than they are in daily use. The other camp says report RMSE, because in most real deployments the disasters are what hurt you, and a metric that treats one enormous mistake the same as ten small ones is hiding the thing you should be afraid of. There is also a third, less romantic reason RMSE is everywhere: it is the thing most models are actually *fitted* to minimise, so reporting it is consistent with how the model was built. The practical position that most working people land on is: **report both, plus the worst single error.** Three numbers cost nothing to compute and make it impossible for a reader — or for you — to be fooled by an average that looks fine because the disasters are rare.

**"We picked depth 4 by looking at the test scores. Isn't that cheating?"**

It is not cheating, but you are right that it costs something, and noticing that is a genuinely advanced thought. You looked at those 89 patients fifteen times and picked the best-looking result, so the score at depth 4 is a bit flattering — some of that 0.352 is you having got lucky on those particular 89. The professional fix is called cross-validation and it is next year. This year, the fix is to write the sentence down: *"I chose the depth by looking at the test curve, so this estimate is optimistic."* Honesty in writing genuinely is the answer when you only have 442 rows and cannot afford a third pile.

**"The tree lost. Was Week 31 a waste of time?"**

No — and the way to see that is to ask what each model can *give* you. The line's answer is ten coefficients; the depth-4 tree's answer is sixteen rules you can print on a page and hand to somebody who has never seen a computer. On this dataset the line predicts better. On a dataset with a sharp threshold in it — "anything within 1.5 km of the school costs more" — the tree would win outright, because a threshold *is* a split and a straight line can only smear it. Different tools, different shapes. The bake-off is how you find out which shape your data has.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| The `1.000` gets celebrated | It is a perfect score, and perfect scores have meant good news all year | Do not explain. Ask one question and then wait, in silence: *"What did it score on the patients it had never seen?"* The realisation has to be theirs. |
| "So deeper is bad" — the student swings to depth 1 | Overcorrection is the natural response to being tricked | Point at depth 1: test R² 0.131, barely above the baseline. Both ends are wrong, for opposite reasons. Say those exact words and make them repeat the reasons back. |
| `train_test_split` ends up inside the loop | It looks like extra rigour, and it produces no error | The curve becomes a shapeless mess. Have them count the `train_test_split` lines in the file. There must be exactly one, above the `for`. |
| The depth-9 bump destroys their confidence in the whole idea | The curve genuinely is not smooth, and they were promised a shape | Have the answer ready and be brief: 89 patients, one patient ≈ 0.01, look at the trend and at the gap column. Then move on; do not spiral. |
| The plot is skipped because time ran out | The code is at the end and the table came first | Do it on paper from the printed table. **Never cut the moment where they draw the vertical line and say the sentence.** That is the lesson; the PNG is not. |
| MAE and RMSE get treated as "two names for the same thing" | They are similar numbers in the same units | Go back to Model A and Model B: identical MAE, RMSE three times apart. Two numbers, one difference, thirty seconds. |
| RMSE gets described as "the worst miss" | It is the obvious shorthand, and it is wrong | Correct yourself out loud if you said it. Point at the real numbers: the line has a **worse** single worst miss than kNN and a **lower** RMSE. RMSE is about the whole tail of big misses. |
| The student is deflated that the tree lost | Two weeks of enjoying trees, and then this | Reframe within a minute: it lost on score, it still wins on readability, and which matters depends on the job. Then ask which they would rather hand a doctor. |
| The Week 29 callback is skipped because the numbers are lost | Four weeks is a long time and whiteboards get wiped | This is why it is a prep item. If it truly is lost, reconstruct it: re-run their Week 29 file. The callback is worth five minutes of setup. |
| The honesty sentence is treated as optional politeness | It sounds like a disclaimer rather than a result | Make it a marked item on the homework. "I chose the depth by looking at the test curve, so this estimate is optimistic" is a *finding*, not an apology, and Week 35's capstone marks it. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** the bake-off down to three rows (baseline, unlimited tree, linear regression), the loop down to `range(1, 11)`, and RMSE entirely if you must. Keep the perfect-training-score row, the depth table, and the vertical line at the peak. That is objectives 3, 4 and 5 — and 4 is the one the whole year points at.

**Reteach — do it with index cards, no computer.** The sticking point is almost always *why memorising fails*, and it is much easier to feel than to hear.

Write ten simple sums on ten cards, answers on the back. Have the student memorise all ten card-by-card — not the method, the pairs. Test them on the same ten cards: **10 out of 10.** Then produce **three new cards** they have not seen, with different numbers. They get those wrong, or have to actually do the arithmetic.

Then say it: *"Ten out of ten on the cards you studied. That number was completely true and it told me nothing about the three new ones. That is what the computer did with 353 patients."*

Five minutes, no laptop, and it lands harder than the table does.

**A copy-this-exactly scaffold.** The smallest complete file that still shows the whole lesson:

```python
# week33_small.py
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

data = load_diabetes()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42)

for depth in [1, 4, 15]:
    tree = DecisionTreeRegressor(max_depth=depth, random_state=0)
    tree.fit(X_train, y_train)
    print("depth", depth,
          " train:", round(tree.score(X_train, y_train), 3),
          " test:", round(tree.score(X_test, y_test), 3),
          " leaves:", tree.get_n_leaves())
```

```text
depth 1  train: 0.304  test: 0.131  leaves: 2
depth 4  train: 0.585  test: 0.352  leaves: 16
depth 15  train: 0.999  test: 0.044  leaves: 329
```

Three lines of output and the entire lesson is in them: train 0.304 → 0.999 while test goes 0.131 → 0.352 → 0.044, and leaves go 2 → 329. Then the only task is to say which of the three you would ship, and why.

**One thing you must not cut:** the sentence. *"After here it is memorising."* Written in their own hand, next to a line they drew.

### If the student is flying

None of these need syntax they do not already have.

1. **`max_depth` is a ceiling, not a target** (Variation — harder, item 1). `DecisionTreeRegressor(random_state=0)` reaches a real depth of **19** with **346** leaves. Set `max_depth=25` and it still says 19. Why? Because it ran out of impure leaves to split.
2. **The kNN dial, backwards** (item 2). Loop `n_neighbors` 1 to 25. At `k = 1` the train R² is a perfect 1.000, because every training point is its own nearest neighbour. *"You have found Sam in a completely different model. What's the dial, and which end is complex?"*
3. **Test the depth-9 bump** (item 3). Re-run the whole depth loop with `random_state=1` on the split instead of 42 and see whether the bump survives. With `random_state=1` the bump goes away, but so does more: the whole curve moves, the test peak lands at depth 2 (0.232) instead of depth 4, and test R² goes negative from depth 5. So the bump is noise, and the best depth itself belongs to this split, not to the dataset. That is how you tell a real effect from noise, and it is a real technique rather than an exercise.
4. **The shipping argument** (item 4). Write 100 words naming a model, citing at least two numbers, *and* naming who the prediction is for. Then argue the opposite case with equal seriousness.
5. **Break the fairness on purpose** (item 5). Move the split inside the loop, drop `random_state`, and look at the resulting mess. Nothing errors. *"What is this chart measuring?"*
6. **Add the worst single miss to the report function.** One line — `np.abs(y_test - guesses).max()` — and it turns the MAE/RMSE conversation from a rule into an observation. Real values: kNN 138.80, tree depth 5 201.00, linear 154.49. Then the puzzle: *"The line has the worse single miss and the better RMSE. How?"* (Nine kNN misses over 100 against the line's five.)

### If the student won't engage today

Do the Hook, then the index cards, and stop.

The Sam story plus the ten-card demonstration is a complete, honest, fifteen-minute lesson on overfitting with no computer in the room. Then extend it into a game:

> **"Learned it or memorised it?"** You describe a situation and they say which. Best of ten.
>
> Somebody who can recite every capital city but can't find one on a map *(memorised)* · somebody who can spell a word they have never seen by knowing the pattern *(learned)* · a friend who beats you at a game only on the one board they have played a hundred times *(memorised)* · a friend who beats you on any board *(learned)* · a model that scores 1.000 on its training rows *(memorised, almost certainly)* · a model that scores 0.53 on training and 0.45 on test *(learned — small gap)* · somebody who can do the homework questions but not the exam *(memorised)* · a chatbot that answers a question perfectly if you phrase it exactly one way *(memorised)* · a batter who scores runs on every ground *(learned)* · a batter who only scores at home *(memorised the ground)*.

The last four are the good ones because they are about the *gap*, not the score, and a student who can sort those has objective 4 completely.

The code survives to next session. But do come back to it — this is the one lesson in Level 2 you should not leave undone, because Weeks 34 to 36 assume it.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — diagnose from two numbers (spoken)**

> "Three models. Tell me what's happening in each, in one word. One: train 0.98, test 0.61. Two: train 0.30, test 0.28. Three: train 0.55, test 0.52."

*Good answer:* overfitting · underfitting · just right. Full marks needs the reason attached to at least one — "big gap" or "both low". **What to catch:** a student who says the second is overfitting. Ask which number is high. Neither.

**Check 2 — the killer row (spoken)**

> "One of our models scored a perfect 1.000 on the rows it learned from. Would you ship it? Say why in two sentences."

*Good answer:* "No. It scored −0.003 on rows it had never seen, which is no better than just guessing the average (the baseline row scores −0.012), so the perfect score only means it memorised the 353 training patients." Full marks needs **both** numbers and the word memorised. **What to catch:** hesitation, or "yes because 1.000 is perfect". Point at the test column and wait.

**Check 3 — the peak, and the honesty (written, 60 seconds)**

> "Write the sentence that goes next to the vertical line on your chart. Then write the sentence about how you chose depth 4."

*Good answer:* "After here it is memorising." And: "I chose the depth by looking at the test curve, so this score is slightly optimistic." Full marks needs both. **What to catch:** the second one being skipped — it is the one that feels optional and is not. If it is missing, ask: *"How many times did you look at the test scores before you picked?"*

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Reads a high training score as good news. Cannot say what the two scores are for. Thinks the unlimited tree is broken. |
| **2 — Emerging** | Names overfitting when shown a big gap. Runs the loop with help. Reads the peak off the table when prompted. |
| **3 — Secure** | Runs three models on one split and produces the table. Computes RMSE with `np.sqrt`. Plots both curves, draws the vertical line at the peak, and says "after here it is memorising". **This is the target.** |
| **4 — Strong** | Explains why the train score *must* rise, so it cannot be evidence. Explains why depth 1 and depth 15 are wrong for opposite reasons. Names a model to ship and defends it with at least two numbers. Writes the honesty sentence unprompted. |
| **5 — Exceptional** | Explains why identical MAE can hide very different RMSE, and refuses to call RMSE "the worst miss". Spots that re-splitting inside the loop would measure shuffle luck. Treats the depth-9 bump as noise and proposes re-running with a different split to test it. Recognises that choosing depth from the test curve has cost something, and says what. |

---

## 📤 Homework to Assign

**Say this:**

> "Three pages, about an hour, and this is the write-up I care most about all year.
>
> **First, page 33.4 — finish the bake-off.** Three models on **one** split, plus the lazy baseline. A results table with MAE, RMSE, test R² and train R² for every single row, and — this is a marked item — **the row counts written at the top**: 353 training, 89 test. A table of bare numbers with no row counts and no metric names in the headers is not a result, it's a pile of digits.
>
> **Second, page 33.5 — the depth curve.** The loop from 1 to 15, the full table with the gap column, the chart with both lines, and the vertical line at the peak. Mark it, **name it**, and then write me **three sentences**: what the train line does and why it can only go up; where the test line peaks and how many leaves the tree has there; and what the gap is measuring, in plain words. Three sentences. Not one, not eight.
>
> **Third, page 33.6 — the decision and the honesty.** Name the model you'd actually ship and defend it with **at least two numbers from your table**. Then the honesty section, three bullets: how big your test set is and what one patient is worth in R²; the sentence 'I chose the depth by looking at the test curve, so this estimate is optimistic'; and one thing about this dataset that makes it easier than real life. Then the Bug Log — both of today's errors, real message, fix in your own words.
>
> And one last thing. Go and find what you wrote in Week 29 about the gap between your two scores. Write today's date next to it and one sentence saying what you now know that you didn't then. That's not busywork. **That's the whole term, in one line.**"

**Workbook pages:** 33.1, 33.2 and 33.3 in class; **33.4, 33.5, 33.6** at home.

**Expected time:** 20 min for the bake-off table · 25 min for the curve and the three sentences · 15 min for the decision, the honesty bullets and the Bug Log. About 60 minutes.

---

## 🔑 Answer Key

### Page 33.1 — Predict before you run, and sort the three fits

**(a) `print(load_diabetes().data.shape)`**

```text
(442, 10)
```
442 patients, 10 measurements each.

**(b) With `test_size=0.2`, how many rows in each pile?**
`442 × 0.2 = 88.4`, and scikit-learn rounds the test pile up: **353 train, 89 test.** Always print it rather than working it out — `print(len(X_train), len(X_test))`.

**(c) A tree with no depth limit, on 353 training rows. What will its train R² be?**
**1.000.** With no limit it splits until every leaf is pure, which on 353 distinct rows means near enough one leaf per row. Real value: `1.000`, from 346 leaves at a real depth of 19.

**(d) Sort these three into underfitting, just right and overfitting.**

| Train | Test | Gap | Diagnosis |
|---|---|---|---|
| 0.304 | 0.131 | 0.174 | **Underfitting** — both low |
| 0.585 | 0.352 | 0.233 | **Just right** *(the best available here)* |
| 0.999 | 0.044 | 0.955 | **Overfitting** — train near-perfect, test near-zero |

Worth saying out loud: even the "just right" row has a gap of 0.233 and a test R² of only 0.352. On real data, "just right" is often not very good. That is honest and it is not a failure of the method.

**(e) Can a test R² be negative? What would it mean?**
Yes. R² = 0 means "exactly as good as ignoring every measurement and guessing the average". Negative means **worse than that**. The unlimited tree scores −0.003, essentially level with the baseline's −0.012.

**(f) Which of the two scores is evidence that a model is good?**
Only the **test** score. The train score can only rise as you give the model more room, so it cannot distinguish a good model from a memoriser. The train score's job is to be half of the **gap**.

### Page 33.2 — MAE and RMSE by hand

Ten true values, two models. Model A is off by exactly +1 every time; Model B is exact nine times and off by +10 once.

**Model A**

| miss | \|miss\| | miss² |
|---|---|---|
| +1 (× 10) | 1 each | 1 each |
| | **Σ = 10** | **Σ = 10** |

```
MAE  = 10 ÷ 10 = 1.0
MSE  = 10 ÷ 10 = 1.0
RMSE = √1.0     = 1.0
```

**Model B**

| miss | \|miss\| | miss² |
|---|---|---|
| 0 (× 9) | 0 each | 0 each |
| +10 | 10 | 100 |
| | **Σ = 10** | **Σ = 100** |

```
MAE  = 10 ÷ 10  = 1.0     ← identical to Model A
MSE  = 100 ÷ 10 = 10.0
RMSE = √10      = 3.1623  ← more than 3× Model A
```

Confirmed in code:

```python
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

y_true = np.array([10, 12, 11, 13, 12, 11, 10, 12, 11, 13])
pred_a = y_true + 1                    # off by +1 every time
pred_b = y_true.copy()
pred_b[9] = y_true[9] + 10             # perfect nine times, +10 once

for name, p in [("Model A", pred_a), ("Model B", pred_b)]:
    errors = np.abs(y_true - p)
    print(f"{name}: errors {errors}  "
          f"MAE {mean_absolute_error(y_true, p):.4f}  "
          f"RMSE {np.sqrt(mean_squared_error(y_true, p)):.4f}")
```

```text
Model A: errors [1 1 1 1 1 1 1 1 1 1]  MAE 1.0000  RMSE 1.0000
Model B: errors [ 0  0  0  0  0  0  0  0  0 10]  MAE 1.0000  RMSE 3.1623
```

**33.2(a) Why is RMSE always ≥ MAE?**
Because squaring stretches anything bigger than 1 and shrinks anything smaller, so the average of the squares is pulled up by the large misses. Taking the root afterwards does not undo that pull. The two are only equal when every miss is exactly the same size — which is precisely Model A.

**33.2(b) A scenario where Model A is clearly better.**
A calculator that works out a medicine dose. Model A is one unit out every time — annoying, correctable, survivable, and a nurse notices and adjusts. Model B is perfect nine times and then recommends ten units too many once. That single event can be dangerous and it is worse than ten small errors put together. **Report RMSE here**, because RMSE is the metric that can tell these two apart, and what you are afraid of is the catastrophe, not the typical case.

**33.2(c) A scenario where Model B is clearly better.**
Estimating a household's weekly grocery bill in a budgeting app. Model A is wrong every single week, so the user never once sees a number they would call right and the app feels permanently untrustworthy. Model B nails it nine weeks out of ten and is badly wrong in the week of the birthday party — which the user can immediately explain to themselves. **Report MAE here** (and maybe "how often was I within ₹2"), because the typical week is what matters and a rare, explicable outlier should not dominate the headline number.

**33.2(d) So which should you report?**
Both, plus the worst single error. Three numbers, no extra work, and it becomes very hard for a reader to be misled by an average that looks fine because the disasters are rare.

### Page 33.3 — The bake-off table

The complete working file is in section 5. Real output:

```text
rows and columns: (442, 10)
the answer runs from 25.0 to 346.0
train rows: 353  test rows: 89

model                      MAE    RMSE   test R2   train R2
always guess the mean    64.01   73.22    -0.012      0.000
kNN, k = 5               42.77   54.95     0.430      0.584
tree, max_depth=5        48.15   62.60     0.260      0.669
tree, no limit           56.57   72.90    -0.003      1.000
linear regression        42.79   53.85     0.453      0.528
```

**33.3(a) Which row shows a perfect training score? What is its test score?**
`tree, no limit`. Train R² **1.000**, test R² **−0.003**. Perfect on the 353 it learned from; no better than guessing the average on the 89 it had not seen.

**33.3(b) Why is the baseline row in the table at all?**
Because without it, no other number means anything. MAE 42.77 sounds like nothing until you know that ignoring all ten measurements and guessing the average is off by 64.01. Then 42.77 becomes "a third less wrong than not bothering". Same lesson as Level 1's Week 12: compute the ruler before you measure with it.

**33.3(c) kNN and the line have almost the same MAE. Which is better, and how do you know?**
The line. MAE is a dead heat — 42.77 against 42.79, two hundredths apart on a scale that runs to 346 — but the line's RMSE is lower, 53.85 against 54.95. RMSE squares the misses, so a lower RMSE at equal MAE means fewer or smaller *big* misses. Counting them confirms it: **kNN has nine misses over 100, the line has five.** Typical performance identical; big-miss behaviour better for the line.

**33.3(d) Add the worst single miss and explain the surprise.**

```python
worst = np.abs(y_test - guesses).max()
```

Real values: kNN **138.80**, tree depth 5 **201.00**, tree no limit **201.00**, linear **154.49**, baseline 156.26.

The surprise: the line has a **worse** single worst miss than kNN (154.49 against 138.80) and still a **lower** RMSE. So RMSE is not "the worst miss" — it is about the whole tail of large misses, and the line has fewer of them. **This is why "RMSE tells you the worst error" is a tempting sentence that is not true.**

**33.3(e) The two trees, side by side. What did turning the dial up do?**

| | train R² | test R² | gap |
|---|---|---|---|
| tree, max_depth=5 | 0.669 | 0.260 | 0.409 |
| tree, no limit | 1.000 | −0.003 | 1.003 |

It made the training score better and the model worse. Train went 0.669 → 1.000, an apparent triumph. Test went 0.260 → −0.003, an actual disaster. **That single comparison is why a training score is not evidence.**

**33.3(f) Where is the `StandardScaler`? Week 30 said kNN needs one.**
A very good thing to notice. This dataset arrives already scaled — whoever prepared it centred and scaled every column. So kNN does not need one here. If the columns had been raw (blood sugar in the hundreds, a body-mass index around 25), kNN would need scaling and the tree would not.

### Page 33.4 — The depth curve (homework)

The complete working file is in section 7. Real output:

```text
depth  leaves  train R2  test R2     gap
    1       2     0.304    0.131   0.174
    2       4     0.447    0.295   0.152
    3       8     0.517    0.329   0.188
    4      16     0.585    0.352   0.233
    5      31     0.669    0.260   0.408
    6      55     0.747    0.221   0.526
    7      91     0.813    0.188   0.624
    8     128     0.873    0.186   0.688
    9     176     0.914    0.283   0.631
   10     221     0.938    0.117   0.821
   11     255     0.961    0.151   0.810
   12     280     0.982    0.115   0.866
   13     298     0.992    0.176   0.816
   14     314     0.996    0.132   0.864
   15     329     0.999    0.044   0.955

best test R2 was 0.352 at max_depth = 4
training rows: 353  leaves at depth 15: 329
saved week33_depth_curve.png
```

**33.4(a) At which depth is the test score highest?**
**Depth 4**, test R² **0.352**. The tree has **16** leaves there.

**33.4(b) Does the train score ever go down?**
No. Not once in fifteen steps: 0.304 → 0.999, rising every single time.

**33.4(c) What is the gap at depth 2, and at depth 15?**
0.152 at depth 2. **0.955** at depth 15. Growing by more than six times.

**33.4(d) How many leaves at depth 15, and how many training rows?**
**329 leaves for 353 training patients.** Nearly one private leaf per patient. That is a lookup table, not a rule about diabetes.

**33.4(e) Why must the split be made before the loop?**
Because if you re-split inside the loop, each depth is tested on a different set of 89 patients, so the differences between depths would be measuring which shuffle happened to be lucky rather than what depth does. The curve comes out shapeless — **and nothing errors**, which is what makes it dangerous. There must be exactly one `train_test_split` in the file, above the `for`.

**33.4(f) Why is `linestyle="--"` used for the vertical line?**
So nobody mistakes it for data. Every solid line on that chart is a series of measurements; the dashed one is an annotation the author added. Keeping those visually different is part of not lying with a chart, which was Week 27.

**33.4(g) Test R² at depth 9 (0.283) is higher than at depth 6 (0.221). Does that break the story?**
No, and it is a sharp thing to notice. With 89 test patients, one patient is worth roughly 0.01 of R², so a difference of 0.06 is about six patients changing sides — real, but well inside the wobble you would expect. Read the trend over all fifteen steps rather than step to step, and look at the `gap` column, which grows almost without interruption from 0.174 to 0.955 and never recovers. To check it properly, re-run with a different `random_state` on the split and see whether the bump survives. It generally does not.

### Page 33.5 — The three sentences (homework)

**Full-credit answer:**

> **Sentence one — the train line.** The train R² rises at every single depth, from 0.304 to 0.999, and it can only go up: a deeper tree has every question a shallower one had plus more, so it can never do worse on the rows it learned from. That means the train column is arithmetic, not evidence.
>
> **Sentence two — the test peak.** The test R² peaks at 0.352 at max_depth 4, where the tree has 16 leaves, and then falls all the way to 0.044 by depth 15, where it has 329 leaves for 353 training patients — almost one private leaf per person.
>
> **Sentence three — the gap.** The gap is train minus test, and it measures how much of the model's apparent skill is really just memorising these particular 353 patients; it grows from 0.174 at depth 1 to 0.955 at depth 15, which means by the end almost all of that perfect-looking training score is memorisation and none of it carries over.

**Marking:** one mark each for the direction of the train line, the reason it cannot fall, the peak depth, the leaf count at the peak, the leaf count at the end against the row count, and a plain-words definition of the gap. Six marks. A student who says "the gap is the difference between the scores" without saying what it *measures* gets five.

**33.5(a) Why are depth 1 and depth 15 wrong for different reasons?**
Depth 1 is **underfitting**: with one question it can only give two answers, so it cannot describe 442 patients — train 0.304 and test 0.131, both low, tiny gap. Depth 15 is **overfitting**: it describes these 353 patients in enormous detail, including the parts that were random, so train 0.999 and test 0.044, with a gap of 0.955. One has not learned enough. The other has learned things that were never true in general. **Turning the dial the wrong way fixes one and worsens the other**, which is exactly why you plot the curve instead of guessing.

**33.5(b) What would you expect to happen at depth 20?**
Almost nothing. The tree with no limit reaches a real depth of 19 with 346 leaves, so by depth 19 there is nothing impure left to split. Setting `max_depth` to 20, 25 or 100 changes nothing — the real depth stays 19, the leaves stay 346, and every score is identical. `max_depth` is a **ceiling, not a target**.

### Page 33.6 — The decision, the honesty, and the Bug Log (homework)

**33.6(a) Which model would you ship, and why?**

A full-credit answer names one model and cites at least two numbers. The strongest case:

> I would ship **linear regression**. It has the best test R² of anything in the table (0.453 against 0.430 for kNN and 0.352 for the best tree), the best RMSE (53.85), and an MAE of 42.79 — a third better than the 64.01 you get from ignoring every measurement and guessing the average. Its train R² is 0.528 against a test of 0.453, so the gap is only 0.075 and it is clearly not memorising. It also has the fewest surprises: only five misses over 100 points, where kNN has nine.

An equally creditable answer argues the other way, and should be marked just as highly if the numbers are there:

> I would ship the **depth-4 tree**, even though it scores lower (0.352 against 0.453), because its answer is 16 rules I can print on one page and read out to a doctor, and a prediction about somebody's illness that nobody can explain is not much use however accurate it is. I would report both scores side by side so the cost of that choice is written down: I am giving up about 0.1 of R² to get an explanation.

**Not** creditable: naming a model with no numbers, or naming the unlimited tree because it scored 1.000.

**33.6(b) The honesty section — three bullets.**

> - **My test set is 89 patients.** One patient moving is worth roughly 0.01 of R², so any difference smaller than about 0.03 between two models is inside the noise and I should not claim it. The 0.023 between kNN (0.430) and the line (0.453) is right on that boundary, so "the line is better" is a weak claim on test R² alone — it is the RMSE and the big-miss count that make it stronger.
> - **I chose the depth by looking at the test curve, so this estimate is optimistic.** I looked at those 89 patients fifteen times and picked the best-looking answer, so some of that 0.352 is luck on these particular 89. The proper fix is cross-validation, which is next year.
> - **One thing that makes this easier than real life:** the dataset arrived clean, complete and already scaled. Nothing was missing, nothing was misspelled, no duplicates, no units to reconcile. Real data would have cost me most of a week before any of this started — as Weeks 23 and 24 showed.

**33.6(c) Look back at what you wrote in Week 29.**

This is the student's own record, so mark the reflection rather than the numbers. A full-credit sentence names the phenomenon and the fix:

> In Week 29 I wrote down that my model got more right on the flowers it had learned from than on the flowers I hid, and I didn't know why. Now I know that difference is called the **train/test gap**, that it measures how much the model is memorising rather than learning, and that the way to shrink it is to give the model less room — a smaller `max_depth`, or a bigger `k`.

**The two Bug Log entries.**

| Message | What it means | The fix |
|---|---|---|
| `TypeError: got an unexpected keyword argument 'squared'` | I passed `squared=False` to `mean_squared_error`, and that setting has been removed from modern scikit-learn. Most tutorials online still show it. | Do it myself: `np.sqrt(mean_squared_error(y_true, y_pred))`. Lesson: **the error message is more up to date than the tutorial.** |
| `sklearn.exceptions.NotFittedError: This DecisionTreeRegressor instance is not fitted yet. Call 'fit' with appropriate arguments before using this estimator.` | I asked a brand-new tree for its score before it had learned anything, because I left `fit` out of the loop. | Put `tree.fit(X_train, y_train)` inside the loop, above both `.score()` calls. A fresh model each time round the loop needs a fresh `fit` each time round. |

**33.6(d) Bonus — the silent bug.** Write down one bug from this week that produces **no error at all** and say how you would catch it.

> Re-splitting inside the loop. `train_test_split` inside the `for` gives every depth a different test set, so the curve measures shuffle luck instead of complexity — and nothing errors, so the chart looks perfectly respectable. I catch it by counting: there must be exactly **one** `train_test_split` in the whole file, and it must be **above** the loop.
>
> (A second one: swapping the arguments in `r2_score`. The right way round my depth-5 tree scores 0.669 on its training rows; the wrong way round it prints 0.504. Both look believable. Truth first, guesses second, always.)

### Lesson questions posed in the Say-this scripts

- *"What did Sam learn?"* → The 200 questions and their answers — not the maths.
- *"Was Sam's 200/200 a lie?"* → No. It was completely true and completely useless as evidence.
- *"How would you catch Sam on Monday?"* → Give him a question that isn't in the booklet. That is exactly what a test set is.
- *"Train 0.99, test 0.62 — which row?"* → Overfitting. Large gap.
- *"Train 0.31, test 0.28 — which row?"* → Underfitting. Nothing is high; the gap is tiny.
- *"Which is worse, Ravi or Sam?"* → Usually Sam: an underfit model is honest about being bad, while a memoriser's good score makes you trust something broken.
- *"Model A and Model B have the same MAE — which for a medicine dose?"* → Model A. Small consistent errors beat one catastrophe. For a grocery bill, the opposite.
- *"Should we always use RMSE?"* → No. Pick according to what a big miss costs, and report both plus the worst single error.
- *"What did `tree, no limit` score on the patients it had never seen?"* → −0.003. No better than guessing the average, alongside a perfect 1.000 on training.
- *"We made the training score better and the model worse — so what is the training score?"* → Not evidence.
- *"Why does the line beat kNN on RMSE when their MAE is level?"* → kNN has nine misses over 100; the line has five. RMSE squares the misses, so the big ones dominate.
- *"Where's the `StandardScaler`?"* → This dataset arrived pre-scaled. Good catch, and worth checking every time.
- *"How many times did you look at the test scores before picking depth 4?"* → Fifteen. Which is why the honesty sentence is not optional.

---

## 🔮 Next Week Preview

Week 34 is the start of the capstone, and it is the week the training wheels come off. There is no new syntax — that is deliberate and it is the point. Instead the student picks **their own question**, one they could genuinely turn out to be wrong about, writes it down in a single sentence, and then goes and collects **at least 100 rows of their own data** to answer it. Step counts, bus arrival times, how long homework actually took against how long it was supposed to take, pocket money against what got spent — anything real, measured by them, over enough days to be worth analysing. Then the raw file gets saved once and never touched again, a copy gets cleaned, and every repair goes into a numbered cleaning log with a *reason* beside it. Everything from Weeks 21 to 33 gets used, in their own hands, on data nobody has tidied for them.

**Prep early, and start now rather than next week.** Two things. **First: the data collection has to begin immediately** — if the student needs a week of step counts, that week starts the day you set Week 34, not the day they sit down to analyse. Have the conversation about what they might measure *before* Week 34 begins, and get them writing numbers down. **Second: dig out the two poster sheets** from the year-0 box; Weeks 34 to 36 build towards Showcase Day and the poster is easier to plan from the start than to retro-fit. Also worth doing now, while today is fresh: get them to write today's depth curve conclusion onto a card and pin it above the desk. Every model in the capstone gets scored on one fixed split, with both numbers reported, and the honesty sentence written underneath. That is not a rule you will have to enforce if the card is on the wall.

---

[⬅ Week 32](week-32.md) · [Course Home](../README.md) · [Week 34 ➡](week-34.md) · [Student Guide](../student-guide/week-33.md) · [Workbook](../workbook/week-33.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)

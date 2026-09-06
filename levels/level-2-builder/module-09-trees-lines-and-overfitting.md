# Module 9 — Trees, Lines, and the Overfitting Trap

**Level 2 · Module 9 · ~4.5 hours · Prereqs: Modules 1–8 (Python, numpy, pandas, matplotlib, `X`/`y`, `train_test_split`, `fit`/`predict`/`score`, scaling)**

[⬅ Previous](module-08-first-model-knn.md) · [Level 2 Home](README.md) · [Next ➡](capstone.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** train a decision tree, print its splits, and read them out loud as plain-English if/then rules a human could follow with a pencil.
2. **You will be able to** fit a linear regression, state what its slope and intercept mean **in the units of the problem**, and use it to predict a new value by hand.
3. **You will be able to** compute and interpret MAE, RMSE, and R² for a regression, and say which one you'd report and why.
4. **You will be able to** tell **underfitting** from **overfitting** by comparing a train score with a test score, and name which one you're looking at.
5. **You will be able to** produce a model-complexity curve — train score and test score against `max_depth` — and point at the exact depth where the model starts memorising instead of learning.

---

## 🪝 The Hook

In Module 8 you saw a model score **100% on its training data** and then get one in five test wines wrong. You were told that was bad, and you moved on.

This module is about that gap, because it is the single most important thing in machine learning and it has a shape you can draw.

Here's the shape. Take a decision tree and let it get gradually more complicated — depth 1, then 2, then 3, all the way to 15. At every step, write down two numbers: how well it does on the data it learned from, and how well it does on data it has never seen.

The first number goes up forever. It always does. Give a model enough freedom and it will eventually memorise the answer key perfectly.

The second number goes up… and then turns around and comes back down.

```
  score
  1.0 ┤                    ●───●───●───●───●───●  ← train: rises to perfection
      │              ●───●
      │        ●───●
  0.8 ┤    ●─                    ▲ the model is now
      │  ●               ○──○      memorising noise
      │        ○───○──○─       ○──○──○──○
  0.6 ┤    ○─                 ↑
      │  ○                    THE OVERFITTING POINT
  0.4 ┤                       (best test score — stop here)
      └──┬───┬───┬───┬───┬───┬───┬───┬───┬───┬──→
         1   2   3   4   5   6   7   8   9  10    max_depth
```

The place where those two lines separate is where your model stops learning about the world and starts learning your particular 160 rows by heart. Everyone who has ever built a model has been fooled by the rising line at least once. Today you learn to draw the falling one.

---

## 🧠 The Concept

### 0. Two kinds of prediction

Before anything else: what *kind* of answer are you predicting?

> **Classification** — predicting a **category** from a fixed list. Apple or orange. Wine class 0, 1 or 2. Spam or not spam.
>
> **Regression** — predicting a **number** on a continuous scale. A house price. Tomorrow's temperature. How many minutes a delivery will take.

| | Classification | Regression |
|---|---|---|
| The answer is | one of a fixed list | any number |
| Example question | "Which club is this student in?" | "What will this student score?" |
| sklearn class names end in | `Classifier` | `Regressor` |
| Main metric | accuracy | MAE, RMSE, R² |
| "Wrong" means | wrong category | off by *some amount* |

🍕 **Analogy.** Classification is a multiple-choice question — you're either right or you're not. Regression is guessing someone's height — being off by 1 cm and being off by 40 cm are both "wrong", but they are extremely different kinds of wrong. That single difference is why regression needs its own metrics.

⚠️ **The classic beginner error:** using `accuracy_score` on a regression. A house price prediction of ₹27.3 lakh when the truth is ₹27.4 lakh is *excellent*, and accuracy would score it as a total failure because 27.3 ≠ 27.4. Accuracy is for categories only.

Everything you learned in Module 8 — `X`, `y`, `fit`, `predict`, `train_test_split` — works identically for both. Only the model class and the metric change.

---

### 1. Decision trees: splits, depth, leaves, and reading the rules out loud

> **Decision tree** — a model that asks a series of yes/no questions about the features, following branches until it reaches a final answer.

🍕 **Analogy.** It's the game Twenty Questions. "Is it bigger than a breadbox?" Yes → go right. "Is it alive?" No → go left. Each question narrows the possibilities until only one answer is left.

Or: it's the flowchart taped to the school nurse's wall. *Temperature above 38? → Yes → Sore throat? → Yes → send home.* You could execute a decision tree with a pencil and no computer, and **that is its superpower.** A kNN model's reasoning is a cloud of 178 memorised wines. A tree's reasoning is a list of rules you can read, argue with, and show to somebody who doesn't code.

**The vocabulary of a tree:**

```
                  ┌─────────────────────────┐
   ROOT NODE  →   │  petal width <= 0.80 ?  │
                  └───────────┬─────────────┘
                    yes ┌─────┴─────┐ no
                        ▼           ▼
                 ┌───────────┐  ┌──────────────────────┐
      LEAF  →    │  setosa   │  │ petal width <= 1.65 ?│ ← INTERNAL NODE
                 └───────────┘  └──────────┬───────────┘
                                 yes ┌─────┴─────┐ no
                                     ▼           ▼
                              ┌────────────┐ ┌───────────┐
                              │ versicolor │ │ virginica │  ← LEAVES
                              └────────────┘ └───────────┘

  DEPTH = the longest number of questions from root to any leaf.  Here: 2.
```

> **Split** — one yes/no question, always of the form `feature <= threshold`.
> **Node** — a point in the tree. The **root** is the first question; **internal nodes** are further questions; **leaves** are final answers.
> **Depth** — how many questions deep the tree is allowed to go. This is the dial that controls everything.

**How does a tree choose its questions?** It tries every feature and every sensible threshold, and picks the split that leaves the two resulting groups as **pure** as possible.

> **Gini impurity** — a "mixed-ness" score for a group. If a group is fraction p₁ of class A and p₂ of class B, then Gini = 1 − p₁² − p₂². It is **0** when the group is all one class and **0.5** when a two-class group is exactly half and half.

🔍 **Tiny example.** A group of 10 students: 4 fail, 6 pass.

```
p(fail) = 4/10 = 0.4        p(pass) = 6/10 = 0.6
Gini = 1 − 0.4² − 0.6² = 1 − 0.16 − 0.36 = 0.48
```

A group of 5 students who all passed:

```
p(fail) = 0        p(pass) = 1
Gini = 1 − 0² − 1² = 1 − 0 − 1 = 0        ← perfectly pure
```

The tree picks whichever split gives the biggest drop in weighted average Gini. (You'll do this arithmetic by hand in the Worked Example.)

**Reading rules out loud.** Here is real `export_text` output from a tree trained on the iris flower dataset:

```
|--- petal width (cm) <= 0.80
|   |--- class: 0
|--- petal width (cm) >  0.80
|   |--- petal width (cm) <= 1.65
|   |   |--- class: 1
|   |--- petal width (cm) >  1.65
|   |   |--- class: 2
```

Translated: *"If the petal is narrower than 0.8 cm, it's a setosa. Otherwise, if the petal is narrower than 1.65 cm, it's a versicolor. Otherwise it's a virginica."* Three sentences, no maths, and a botanist with a ruler could use it in the field. **No other model in this book produces an explanation that good.**

**Trees don't care about scaling.** A tree asks `proline <= 755`, which is a comparison on one column at a time. Multiplying a column by 1000 just multiplies the threshold by 1000 and changes nothing. This is a genuine advantage over kNN: **no `StandardScaler` needed, ever.**

**Trees also do regression.** A `DecisionTreeRegressor` asks the same yes/no questions, but each leaf stores the **average target value** of the training rows that landed there instead of a class label. That means a tree's predictions come in a fixed set of steps — one value per leaf — which is why a tree can never draw a smooth diagonal line.

---

### 2. Linear regression: the line of best fit

> **Linear regression** — fit a straight line through the data, then predict by reading off the line.

🍕 **Analogy.** You've plotted study hours against score. You take a ruler and lay it through the middle of the dots so it's as close as possible to all of them at once. That ruler is the model. To predict a new student's score, you find their hours on the x-axis and read the ruler's height.

The line has exactly two numbers:

> **y = slope × x + intercept**
>
> **Slope** — how much y changes when x goes up by exactly 1.
> **Intercept** — what y would be when x is 0.

🍕 **Anchor for the slope.** If slope = 5.7 for study hours → score, that sentence reads: *"one extra hour of study goes with 5.7 more points."* The slope is always "per one unit of x", and stating it in words with the units attached is the single best habit you can build.

**How does it choose the line?** Out of all possible lines, it picks the one that makes the total of the **squared vertical gaps** as small as possible.

> **Residual** — the vertical gap between a real data point and the line: residual = actual − predicted.

```
  score
    │                                ●  ← actual = 74
    │                          ╱   ↕ residual = +0.6
    │                    ╱───●     predicted = 73.4
    │              ╱───●
    │        ╱───●   ↕ residual = −1.0
    │  ╱───●
    └──────────────────────────────────→  study hours
       the line minimises the SUM OF SQUARED residuals
```

Squaring (rather than just taking the size) means one big miss hurts far more than several small ones. That's a design choice, and it has consequences you'll see in the metrics section.

**The two formulas** (you'll only ever type `LinearRegression()`, but seeing them once makes the model stop feeling magic):

```
slope     = Σ (xᵢ − x̄)(yᵢ − ȳ)  ÷  Σ (xᵢ − x̄)²
intercept = ȳ − slope × x̄
```

where x̄ is the mean of x and ȳ is the mean of y. That's it. Two sums and a division.

**With more than one feature** it becomes a **coefficient** per feature:

```
price = c₁ × size + c₂ × bedrooms + c₃ × age + c₄ × distance + intercept
```

Each coefficient still reads the same way: *"holding everything else fixed, one more unit of this feature changes the prediction by c."*

⚠️ **Two warnings about coefficients.**

1. **A coefficient is not a cause.** Module 7's lesson comes straight back. A coefficient of −0.35 on `age_years` means older houses in *this dataset* sold for less, not that ageing a house destroys value.
2. **Coefficient size depends on units.** A `size_sqm` coefficient of 0.088 looks tiny next to a `bedrooms` coefficient of 2.99 — but sizes range over 150 units while bedrooms range over 3. Never rank feature importance by raw coefficient size unless the features are standardized.

**Linear regression's personality, versus a tree's:**

| | Linear regression | Decision tree |
|---|---|---|
| Shape it can draw | a straight line / flat plane | flat steps |
| Handles a threshold effect ("within 1.5 km of school") | badly — it smears it | perfectly — that's a split |
| Handles a smooth trend | perfectly | badly — staircases it |
| Needs scaling | no (for the fit itself) | no |
| Explains itself as | one number per feature | a list of if/then rules |
| Predicts values it never saw in training | yes, it extrapolates | **no** — never outside the leaf averages |

That last row matters. A tree trained on houses of 45–199 m² will predict the same price for a 500 m² mansion as for a 199 m² house, because it has no leaf beyond that. Linear regression will happily extrapolate — sometimes usefully, sometimes into nonsense.

---

### 3. Regression metrics: MAE, RMSE, and R²

Accuracy is useless here. We need to measure *how far off* we were.

Say you predict five house prices (in lakhs) and get:

| House | Actual | Predicted | Error (actual − pred) | \|Error\| | Error² |
|---|---|---|---|---|---|
| 1 | 20.0 | 19.0 | +1.0 | 1.0 | 1.0 |
| 2 | 25.0 | 27.0 | −2.0 | 2.0 | 4.0 |
| 3 | 30.0 | 30.5 | −0.5 | 0.5 | 0.25 |
| 4 | 18.0 | 17.5 | +0.5 | 0.5 | 0.25 |
| 5 | 40.0 | 39.0 | +1.0 | 1.0 | 1.0 |
| | | | | **sum 5.0** | **sum 6.5** |

**MAE — Mean Absolute Error.**

> **MAE** — the average size of your mistakes, ignoring direction. Same units as the target.

```
MAE = 5.0 ÷ 5 = 1.0 lakh
```

Read it: *"on average, my prediction is off by 1 lakh rupees."* **MAE is the metric you can say out loud to a non-technical person**, because it's in the units of the thing itself.

**RMSE — Root Mean Squared Error.**

> **RMSE** — square the errors, average them, then square-root. Also in the target's units, but it punishes big misses much harder than small ones.

```
MSE  = 6.5 ÷ 5 = 1.3
RMSE = √1.3 = 1.140 lakh
```

RMSE ≥ MAE always. The **gap between them tells you about the shape of your errors**: if RMSE is barely above MAE, your errors are all similar sizes. If RMSE is much bigger, a few large misses are dominating.

🔍 **Tiny example that makes the difference obvious.** Ten true values, two different models:

- **Model A** is off by exactly 1 on every single prediction.
  MAE = 1.0, RMSE = √(10×1 ÷ 10) = **1.0**
- **Model B** is *perfect* on nine predictions and off by 10 on one.
  MAE = (0×9 + 10) ÷ 10 = **1.0**, RMSE = √((0×9 + 100) ÷ 10) = √10 = **3.162**

**Identical MAE. RMSE differs by 3×.** Which model is better? It depends entirely on the problem. If you're predicting delivery times, nine perfect deliveries and one disaster (Model B) is probably worse than ten slightly-late ones (Model A). If you're predicting rainfall for a reservoir, being consistently a bit off might be worse. **The metric encodes what you think "bad" means, so choose it on purpose.**

**R² — the coefficient of determination.**

> **R²** — what fraction of the variation in the target your model explains, compared with a model that just guesses the mean every time. 1.0 is perfect, 0.0 is no better than guessing the average, and **negative is worse than guessing the average.**

```
R² = 1 − (sum of squared errors) ÷ (sum of squared distances from the mean)
```

R² has no units, which makes it good for comparing models on different problems and bad for telling anybody what your predictions are actually worth. **Report MAE for humans, R² for comparing models, and RMSE when big mistakes are the thing you fear.**

⚠️ **Always compute the lazy baseline.** A model that ignores the features and predicts the training mean for everything has R² ≈ 0 by construction. Its MAE is the number your real model has to beat. In this module's housing data the mean-baseline MAE is **9.21 lakh** — so a model with MAE 4.0 isn't "off by 4", it's "less than half as wrong as guessing".

---

### 4. Underfitting, overfitting, and the train/test gap

Here is the whole idea in one table. Compute both scores, then look up your row.

| Train score | Test score | Diagnosis | What's happening | Fix |
|---|---|---|---|---|
| Low | Low | **Underfitting** | Model is too simple to capture the pattern | more complexity: deeper tree, more features, smaller `k` |
| High | High | **Just right** | Model learned the pattern | ship it (and be suspicious of your split) |
| **High** | **Low** | **Overfitting** | Model memorised the training rows, including their noise | less complexity: shallower tree, larger `k`, more data |
| Low | High | Something is broken | Almost always a bug — a leak, a mismatched split, or a fluke tiny test set | check your code |

> **Underfitting** — the model is too simple. It gets things wrong on the training data *and* the test data, in the same way.
>
> **Overfitting** — the model is too complicated. It has learned details of the specific training rows that don't generalise, so it does great on them and badly on everything else.

🍕 **Analogy.** Three students prepare for a maths exam.

- **Ravi** skims the chapter titles. He can't do the practice questions *or* the exam. That's **underfitting** — he never learned the pattern.
- **Priya** learns the method. She does well on practice and well on the exam. **Just right.**
- **Sam** memorises all 200 practice questions and their answers, word for word. He gets 200/200 on practice. On the exam, where the numbers are different, he falls apart. That's **overfitting** — he learned the *questions*, not the *maths*.

Sam's practice score is not a lie. It's just not evidence of anything.

> **Train/test gap** — train score minus test score. A small gap means the model generalises. A large gap means it's memorising.

**`max_depth` is the complexity dial for a tree.** Turn it up and the tree can ask more questions, carve the data into more leaves, and eventually give every training row its own private leaf.

```
 depth 1: 2 leaves      "big house?      → 30 lakh, else 15 lakh"
 depth 3: 8 leaves      eight sensible price bands
 depth 8: 104 leaves    each leaf holds 1-2 houses
 depth 14: 158 leaves   memorised. train R² = 1.000
```

With 160 training houses and 158 leaves, the tree has essentially written down a lookup table. Perfect on training, useless on anything new.

**Every model has a complexity dial:**

| Model | Dial | Simple end | Complex end |
|---|---|---|---|
| Decision tree | `max_depth` | 1 | unlimited |
| kNN | `n_neighbors` | large `k` | `k = 1` |
| Linear regression | number of features | 1 feature | many features |

Note that kNN's dial runs **backwards**: `k = 1` is the *most* complex model (it can carve any shape), and a huge `k` is the simplest. That's why `k = 1` had train accuracy 1.0000 in Module 8 — it was the overfitting end of the dial all along.

---

### 5. The model-complexity curve

Put it all together into one graph, and you get the most useful picture in machine learning.

**The recipe:**

1. Fix **one** train/test split. Never re-split inside the loop, or you'll be measuring shuffle luck instead of complexity.
2. For each value of the complexity dial, fit a fresh model.
3. Record **both** the train score and the test score.
4. Plot both against the dial.
5. The dial value with the highest **test** score is your answer.

```
 R²
 1.0┤                              ●───●───●───●───●  ← TRAIN keeps climbing
    │                    ●───●───●
 0.8┤          ●───●───●            ○ ← test peaked here and is now falling
    │  ●───●              ○───○───○─────○───○───○
 0.6┤              ○───○─                       ↑
    │        ○───○                        the GAP = memorisation
 0.4┤  ○───○
    │  ↑
 0.2┤  both low = UNDERFITTING
    └──┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬──→ max_depth
       1   2   3   4   5   6   7   8   9  10  11
       └── too simple ──┘ ↑ └──── too complex ────┘
                    SWEET SPOT
```

The left of the curve is underfitting: both lines are low and close together. The right is overfitting: train is pinned near perfection while test sags. The peak of the test line is where you stop.

⚠️ **The honesty caveat, again.** Choosing a depth by looking at the test curve means the test set influenced a decision, so the score at your chosen depth is slightly optimistic. Say so in writing. (Cross-validation is the professional fix, and it's waiting for you in Level 3.)

---

## 🔍 Worked Example

Two hand-traces: a linear regression from raw numbers, and a tree's first split from raw counts.

### Part A — Linear regression, every step

Five students. `x` = study hours per week, `y` = test score.

| Student | x (hours) | y (score) |
|---|---|---|
| A | 1 | 52 |
| B | 2 | 55 |
| C | 3 | 61 |
| D | 4 | 68 |
| E | 5 | 74 |

**Step 1 — the two means.**

```
x̄ = (1 + 2 + 3 + 4 + 5) ÷ 5 = 15 ÷ 5 = 3
ȳ = (52 + 55 + 61 + 68 + 74) ÷ 5 = 310 ÷ 5 = 62
```

**Step 2 — deviations from the means, and the two sums.**

| Student | x | y | dx = x − 3 | dy = y − 62 | dx × dy | dx² |
|---|---|---|---|---|---|---|
| A | 1 | 52 | −2 | −10 | 20 | 4 |
| B | 2 | 55 | −1 | −7 | 7 | 1 |
| C | 3 | 61 | 0 | −1 | 0 | 0 |
| D | 4 | 68 | 1 | 6 | 6 | 1 |
| E | 5 | 74 | 2 | 12 | 24 | 4 |
| | | | | | **Σ = 57** | **Σ = 10** |

**Step 3 — slope and intercept.**

```
slope     = 57 ÷ 10 = 5.7
intercept = ȳ − slope × x̄ = 62 − 5.7 × 3 = 62 − 17.1 = 44.9
```

**The model is: score = 5.7 × hours + 44.9**

Say it in words: *"Each extra hour of study a week goes with about 5.7 more points, and a student who studied zero hours would be predicted to score 44.9."*

⚠️ Notice the intercept is a prediction for x = 0, and **nobody in our data studied 0 hours** (the minimum is 1). The intercept is an extrapolation off the edge of the evidence. It is fine as part of the formula and shaky as a claim about real zero-hour students.

**Step 4 — predictions and residuals.**

| Student | x | actual y | predicted = 5.7x + 44.9 | residual = actual − pred | \|residual\| | residual² |
|---|---|---|---|---|---|---|
| A | 1 | 52 | 5.7 + 44.9 = **50.6** | +1.4 | 1.4 | 1.96 |
| B | 2 | 55 | 11.4 + 44.9 = **56.3** | −1.3 | 1.3 | 1.69 |
| C | 3 | 61 | 17.1 + 44.9 = **62.0** | −1.0 | 1.0 | 1.00 |
| D | 4 | 68 | 22.8 + 44.9 = **67.7** | +0.3 | 0.3 | 0.09 |
| E | 5 | 74 | 28.5 + 44.9 = **73.4** | +0.6 | 0.6 | 0.36 |
| | | | | **Σ ≈ 0** | **Σ = 4.6** | **Σ = 5.10** |

*(The residuals summing to ≈ 0 is not a coincidence — the least-squares line always passes through the point (x̄, ȳ) and balances the residuals.)*

**Step 5 — the three metrics.**

```
MAE  = 4.6 ÷ 5 = 0.92 points
MSE  = 5.10 ÷ 5 = 1.02
RMSE = √1.02 = 1.0100 points
```

For R² we need the "guess the mean every time" error — how much y varies around ȳ = 62:

| y | y − 62 | (y − 62)² |
|---|---|---|
| 52 | −10 | 100 |
| 55 | −7 | 49 |
| 61 | −1 | 1 |
| 68 | 6 | 36 |
| 74 | 12 | 144 |
| | | **Σ = 330** |

```
R² = 1 − (5.10 ÷ 330) = 1 − 0.015455 = 0.984545
```

**Read it:** the line explains 98.5% of the variation in scores. The mean-guessing baseline would have squared error 330; the line gets that down to 5.10.

**Step 6 — predict a new student.** Someone studies 6 hours a week:

```
score = 5.7 × 6 + 44.9 = 34.2 + 44.9 = 79.1
```

⚠️ x = 6 is outside the training range of 1–5. That's **extrapolation**, and it's a promise the data never made. Push it far enough (x = 20 → 158.9) and the model predicts a score above 100, which is impossible. **A straight line does not know where reality stops.**

**Step 7 — check every number with sklearn.**

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

x = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)   # sklearn wants a 2-D X
y = np.array([52, 55, 61, 68, 74])

model = LinearRegression().fit(x, y)
print("slope    :", model.coef_)              # [5.7]
print("intercept:", model.intercept_)         # 44.9

pred = model.predict(x)
print("predictions:", np.round(pred, 2))

print("MAE :", mean_absolute_error(y, pred))
print("MSE :", mean_squared_error(y, pred))
print("RMSE:", np.sqrt(mean_squared_error(y, pred)))
print("R2  :", r2_score(y, pred))
print("6 hours ->", model.predict([[6]]))
```

Output:

```
slope    : [5.7]
intercept: 44.9
predictions: [50.6 56.3 62.  67.7 73.4]
MAE : 0.9199999999999975
MSE : 1.019999999999996
RMSE: 1.0099504938362058
R2  : 0.9845454545454546
6 hours -> [79.1]
```

Every hand-computed value matches. The `0.9199999999999975` instead of `0.92` is ordinary floating-point dust — computers store decimals in binary and 0.92 has no exact binary form.

⚠️ **Note `.reshape(-1, 1)`.** `X` must always be 2-D: rows × features. With one feature you have shape `(5, 1)`, not `(5,)`. The `-1` means "work out this dimension for me."

### Part B — A tree's first split, by hand

Ten students. Feature: hours studied. Label: pass or fail.

| hours | 1 | 1.5 | 2 | 2.5 | 3 | 3.5 | 4 | 4.5 | 5 | 5.5 |
|---|---|---|---|---|---|---|---|---|---|---|
| result | fail | fail | fail | **pass** | fail | pass | pass | pass | pass | pass |

Note student #4 (2.5 hours) passed and student #5 (3 hours) failed — real data is never clean, and that one crossover is what makes this interesting.

**Step 1 — impurity before any split.**

4 fails, 6 passes out of 10.

```
p(fail) = 0.4        p(pass) = 0.6
Gini(root) = 1 − 0.4² − 0.6² = 1 − 0.16 − 0.36 = 0.48
```

**Step 2 — try a candidate split: `hours <= 2.25`** (halfway between 2 and 2.5).

```
LEFT  (hours 1, 1.5, 2):        fail, fail, fail          → 3 rows, 3 fail, 0 pass
RIGHT (hours 2.5 … 5.5):        pass, fail, pass, pass,
                                pass, pass, pass          → 7 rows, 1 fail, 6 pass

Gini(left)  = 1 − (3/3)² − (0/3)² = 1 − 1 − 0 = 0
Gini(right) = 1 − (1/7)² − (6/7)²
            = 1 − 0.020408 − 0.734694 = 0.244898

weighted = (3/10) × 0 + (7/10) × 0.244898
         = 0 + 0.171429 = 0.171429

gain = 0.48 − 0.171429 = 0.308571
```

**Step 3 — try another candidate: `hours <= 3.25`** (halfway between 3 and 3.5).

```
LEFT  (hours 1, 1.5, 2, 2.5, 3): fail, fail, fail, pass, fail  → 5 rows, 4 fail, 1 pass
RIGHT (hours 3.5 … 5.5):         pass ×5                        → 5 rows, 0 fail, 5 pass

Gini(left)  = 1 − (4/5)² − (1/5)² = 1 − 0.64 − 0.04 = 0.32
Gini(right) = 1 − (0/5)² − (5/5)² = 1 − 0 − 1 = 0

weighted = (5/10) × 0.32 + (5/10) × 0
         = 0.16 + 0 = 0.16

gain = 0.48 − 0.16 = 0.32
```

**Step 4 — compare.**

| Candidate split | Weighted Gini after | Gain |
|---|---|---|
| `hours <= 2.25` | 0.171429 | 0.308571 |
| **`hours <= 3.25`** | **0.160000** | **0.320000** ← winner |

The tree picks **`hours <= 3.25`**, because it produces the bigger drop in impurity.

**Step 5 — the depth-1 tree, in English.** *"If you studied 3.25 hours or less, predicted: fail. Otherwise: pass."* On the training data it gets 9 out of 10 right — the only mistake is the student who passed on 2.5 hours.

**Step 6 — confirm with sklearn.**

```python
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text

hours = np.array([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5]).reshape(-1, 1)
result = np.array(["fail", "fail", "fail", "pass", "fail",
                   "pass", "pass", "pass", "pass", "pass"])

tree = DecisionTreeClassifier(max_depth=1, random_state=0).fit(hours, result)
print(export_text(tree, feature_names=["hours"]))
print("training accuracy:", tree.score(hours, result))
print("gini at each node:", tree.tree_.impurity)
print("threshold        :", tree.tree_.threshold[0])
```

Output:

```
|--- hours <= 3.25
|   |--- class: fail
|--- hours >  3.25
|   |--- class: pass

training accuracy: 0.9
gini at each node: [0.48 0.32 0.  ]
threshold        : 3.25
```

`[0.48 0.32 0. ]` — the root, left leaf, and right leaf impurities, **exactly** the three numbers we computed by hand. The threshold is 3.25, exactly as predicted.

---

## 💻 Hands-On

Three experiments: read a tree's rules, interpret a linear regression, and draw the overfitting curve.

### Experiment 1 — A tree you can read

```python
# tree_iris.py
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
import matplotlib.pyplot as plt

iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# No StandardScaler anywhere. Trees don't need it.
tree = DecisionTreeClassifier(max_depth=3, random_state=0)
tree.fit(X_train, y_train)

print("train accuracy:", round(tree.score(X_train, y_train), 4))
print("test  accuracy:", round(tree.score(X_test, y_test), 4))
print("\nTHE RULES:")
print(export_text(tree, feature_names=list(iris.feature_names)))

print("which features did it actually use?")
for name, imp in zip(iris.feature_names, tree.feature_importances_):
    print(f"  {name:22s} {imp:.3f}")

fig, ax = plt.subplots(figsize=(13, 7))
plot_tree(tree,
          feature_names=iris.feature_names,
          class_names=list(iris.target_names),
          filled=True, rounded=True, fontsize=9, ax=ax)
ax.set_title("Iris decision tree, max_depth=3")
fig.tight_layout()
fig.savefig("iris_tree.png", dpi=150)
plt.show()
```

Output:

```
train accuracy: 0.9833
test  accuracy: 0.9667

THE RULES:
|--- petal width (cm) <= 0.80
|   |--- class: 0
|--- petal width (cm) >  0.80
|   |--- petal width (cm) <= 1.65
|   |   |--- petal length (cm) <= 4.95
|   |   |   |--- class: 1
|   |   |--- petal length (cm) >  4.95
|   |   |   |--- class: 2
|   |--- petal width (cm) >  1.65
|   |   |--- petal length (cm) <= 4.85
|   |   |   |--- class: 2
|   |   |--- petal length (cm) >  4.85
|   |   |   |--- class: 2

which features did it actually use?
  sepal length (cm)      0.000
  sepal width (cm)       0.000
  petal length (cm)      0.061
  petal width (cm)       0.939
```

**Read the rules out loud.** With `0 = setosa, 1 = versicolor, 2 = virginica`:

1. *"Petal narrower than 0.8 cm? It's a **setosa**."* — one question, done, and it's right every single time.
2. *"Otherwise, petal narrower than 1.65 cm and petal shorter than 4.95 cm? **Versicolor**."*
3. *"Otherwise, petal narrower than 1.65 cm but longer than 4.95 cm? **Virginica**."*
4. *"Petal wider than 1.65 cm? **Virginica**, whatever the length."*

**Two things worth noticing.**

First, **look at the last split.** `petal length <= 4.85` → class 2, and `petal length > 4.85` → class 2. Both branches give the same answer! That split is **useless** — the tree made it because it slightly reduced impurity in the training data, not because it helps. This is a tiny, visible instance of overfitting, and you can only see it *because trees explain themselves*.

Second, **the two sepal features have importance 0.000.** The tree never used them once. Out of four measurements, two carry the entire signal. That's a genuine discovery about irises, delivered for free by a model you can read.

### Experiment 2 — Linear regression on a housing dataset

We'll generate a small town of 200 houses. The data is synthetic — invented by code with a fixed random seed — which means it is reproducible for everybody and, crucially, **we know the true answer** and can check whether the model finds it.

```python
# houses.py — generate the dataset. Import this from the other scripts.
import numpy as np
import pandas as pd


def make_houses(n=200, seed=7):
    """Simulate n houses in one town. Prices are in lakhs of rupees."""
    rng = np.random.default_rng(seed)      # a reproducible random generator

    size = rng.integers(45, 200, n)        # floor area in square metres
    beds = rng.integers(1, 5, n)           # 1 to 4 bedrooms
    age = rng.integers(0, 40, n)           # age of the building in years
    dist = np.round(rng.uniform(0.2, 9.0, n), 1)   # km to the nearest school

    # The TRUE rule we're hiding inside the data:
    #   +0.09 lakh per square metre
    #   +3.00 lakh per bedroom
    #   -0.35 lakh per year of age
    #   -2.20 lakh per km from school
    #   +6.00 lakh bonus if within 1.5 km of school  <-- a THRESHOLD effect
    #   +20   lakh base, plus random noise of about 2 lakh
    price = (0.09 * size
             + 3.00 * beds
             - 0.35 * age
             - 2.20 * dist
             + 20
             + 6.00 * (dist < 1.5)
             + rng.normal(0, 2.0, n))

    return pd.DataFrame({
        "size_sqm": size,
        "bedrooms": beds,
        "age_years": age,
        "km_to_school": dist,
        "price_lakh": np.round(price, 1),
    })


FEATURES = ["size_sqm", "bedrooms", "age_years", "km_to_school"]
TARGET = "price_lakh"

if __name__ == "__main__":
    df = make_houses()
    print(df.head())
    print(df.describe().round(2))
```

```
   size_sqm  bedrooms  age_years  km_to_school  price_lakh
0       191         2         25           5.8        23.2
1       141         4         32           1.8        31.2
2       151         1         17           6.9        13.5
3       184         3         26           6.9        18.5
4       134         3          8           6.5        23.3
```

Now fit the line:

```python
# linreg_houses.py
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from houses import make_houses, FEATURES, TARGET

df = make_houses()
X = df[FEATURES].values
y = df[TARGET].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42        # no stratify: this is regression
)
print("train:", X_train.shape, " test:", X_test.shape)

# ---- the lazy baseline: always predict the training mean -----------------
baseline = DummyRegressor(strategy="mean").fit(X_train, y_train)
bp = baseline.predict(X_test)
print("\nBASELINE (always guess the mean)")
print("  MAE :", round(mean_absolute_error(y_test, bp), 2))
print("  R2  :", round(r2_score(y_test, bp), 3))

# ---- the real model ------------------------------------------------------
lin = LinearRegression().fit(X_train, y_train)
pred = lin.predict(X_test)

print("\nLINEAR REGRESSION")
print("  MAE :", round(mean_absolute_error(y_test, pred), 2))
print("  RMSE:", round(np.sqrt(mean_squared_error(y_test, pred)), 2))
print("  test  R2:", round(r2_score(y_test, pred), 3))
print("  train R2:", round(lin.score(X_train, y_train), 3))

print("\nTHE LEARNED FORMULA")
for name, c in zip(FEATURES, lin.coef_):
    print(f"  {name:14s} {c:+8.3f} lakh per unit")
print(f"  {'intercept':14s} {lin.intercept_:+8.2f} lakh")

# ---- use it -------------------------------------------------------------
new_house = np.array([[120, 3, 10, 1.0]])   # 120 m2, 3 beds, 10 yrs, 1 km
print("\nprediction for a 120 sqm / 3 bed / 10 yr / 1.0 km house:",
      round(lin.predict(new_house)[0], 2), "lakh")
```

Output:

```
train: (160, 4)  test: (40, 4)

BASELINE (always guess the mean)
  MAE : 9.21
  R2  : -0.006

LINEAR REGRESSION
  MAE : 2.18
  RMSE: 2.64
  test  R2: 0.935
  train R2: 0.93

THE LEARNED FORMULA
  size_sqm         +0.088 lakh per unit
  bedrooms         +2.994 lakh per unit
  age_years        -0.377 lakh per unit
  km_to_school     -2.618 lakh per unit
  intercept       +23.25 lakh

prediction for a 120 sqm / 3 bed / 10 yr / 1.0 km house: 36.45 lakh
```

**Read the coefficients out loud, each with units:**

- `size_sqm +0.088` — *"one extra square metre goes with about ₹8,800 more."*
- `bedrooms +2.994` — *"one extra bedroom goes with about ₹3 lakh more."*
- `age_years −0.377` — *"each year of age goes with about ₹37,700 less."*
- `km_to_school −2.618` — *"each kilometre further from school goes with about ₹2.6 lakh less."*

**Now compare with the truth we planted.** We built the data with 0.09, 3.00, −0.35, −2.20. The model recovered 0.088, 2.994, −0.377, −2.618. Three of the four are almost exact. The fourth — distance — came out at −2.618 instead of −2.20, and there's a reason: **we also hid a +6 lakh bonus for houses within 1.5 km of a school, and a straight line has no way to express a bonus.** The best it can do is make the whole distance slope steeper, smearing the threshold effect across every kilometre. Keep that in mind; the tree is about to handle it very differently.

**And check the baseline.** The mean-guesser gets MAE 9.21. Linear regression gets 2.18. Our model's mistakes are about **four times smaller** than doing nothing at all. Without that comparison, "MAE 2.18" is a number with no meaning.

*(The baseline's R² of −0.006 being slightly negative is normal: it predicts the **training** mean, which isn't exactly the test mean.)*

### Experiment 3 — A regression tree, and reading its rules

```python
# tree_houses.py
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, export_text
from sklearn.metrics import mean_absolute_error, r2_score
from houses import make_houses, FEATURES, TARGET

df = make_houses()
X, y = df[FEATURES].values, df[TARGET].values
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

tree = DecisionTreeRegressor(max_depth=2, random_state=0).fit(X_train, y_train)
print(export_text(tree, feature_names=FEATURES, decimals=2))
print("train R2:", round(tree.score(X_train, y_train), 3))
print("test  R2:", round(tree.score(X_test, y_test), 3))
```

Output:

```
|--- km_to_school <= 1.65
|   |--- size_sqm <= 157.00
|   |   |--- value: [33.91]
|   |--- size_sqm >  157.00
|   |   |--- value: [42.80]
|--- km_to_school >  1.65
|   |--- size_sqm <= 119.00
|   |   |--- value: [16.02]
|   |--- size_sqm >  119.00
|   |   |--- value: [23.28]

train R2: 0.531
test  R2: 0.554
```

**This is a beautiful result and you should stare at it.** We hid a threshold in the data at **1.5 km**. With only two questions to spend, the tree chose as its very first split: **`km_to_school <= 1.65`**. It found the school-proximity rule almost exactly, on its own, from the numbers.

Read the whole model in four sentences:

- *"Within 1.65 km of a school and under 157 m²? About **33.9 lakh**."*
- *"Within 1.65 km and over 157 m²? About **42.8 lakh**."*
- *"Further than 1.65 km and under 119 m²? About **16.0 lakh**."*
- *"Further than 1.65 km and over 119 m²? About **23.3 lakh**."*

Four prices. That's the *entire* model — a depth-2 tree can only ever produce 4 different answers, which is why its R² is a modest 0.531 while linear regression reaches 0.935. **The tree has the better explanation and the worse prediction.** That trade is real, and you will make it again and again.

Also note: train R² 0.531 and test R² 0.554 — the test score is *higher*. That's fine and it happens with small test sets. It's also the clearest possible sign that this model is **underfitting**: it's too simple to have memorised anything.

### Experiment 4 — The overfitting curve

```python
# depth_curve.py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from houses import make_houses, FEATURES, TARGET

df = make_houses()
X, y = df[FEATURES].values, df[TARGET].values

# ONE split, fixed. The loop must not re-split, or we'd measure shuffle luck.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

depths = list(range(1, 16))
train_scores, test_scores, leaf_counts = [], [], []

for d in depths:
    t = DecisionTreeRegressor(max_depth=d, random_state=0).fit(X_train, y_train)
    train_scores.append(t.score(X_train, y_train))
    test_scores.append(t.score(X_test, y_test))
    leaf_counts.append(t.get_n_leaves())

print(f"{'depth':>5} {'leaves':>7} {'train R2':>9} {'test R2':>8} {'gap':>7}")
for d, lv, tr, te in zip(depths, leaf_counts, train_scores, test_scores):
    print(f"{d:5d} {lv:7d} {tr:9.3f} {te:8.3f} {tr - te:7.3f}")

best_i = int(np.argmax(test_scores))
best_depth = depths[best_i]
print(f"\nBest test R2 = {test_scores[best_i]:.3f} at max_depth = {best_depth}")

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.plot(depths, train_scores, marker="o", linewidth=2,
        color="#1f77b4", label="train R²  (data the tree learned from)")
ax.plot(depths, test_scores, marker="s", linewidth=2,
        color="#d62728", label="test R²   (data the tree never saw)")

# Mark the overfitting point.
ax.axvline(best_depth, color="#2ca02c", linestyle="--", linewidth=2,
           label=f"best test R² at depth {best_depth}")
ax.annotate("train keeps rising\ntest starts falling\n= OVERFITTING",
            xy=(best_depth + 0.3, 0.60), fontsize=10, color="#333333")

ax.set_title("Deeper trees memorise: train R² hits 1.00 while test R² falls")
ax.set_xlabel("max_depth (how many questions the tree may ask)")
ax.set_ylabel("R² (1.0 = perfect, 0.0 = no better than guessing the mean)")
ax.set_ylim(0, 1.05)
ax.set_xticks(depths)
ax.grid(alpha=0.3)
ax.legend(loc="lower right")

fig.tight_layout()
fig.savefig("depth_curve.png", dpi=150)
plt.show()
```

Output:

```
depth  leaves  train R2  test R2     gap
    1       2     0.371    0.282   0.089
    2       4     0.531    0.554  -0.023
    3       8     0.665    0.676  -0.011
    4      16     0.788    0.764   0.024
    5      30     0.887    0.791   0.096
    6      50     0.947    0.788   0.159
    7      76     0.975    0.754   0.221
    8     104     0.988    0.752   0.236
    9     129     0.994    0.743   0.251
   10     144     0.997    0.741   0.256
   11     150     0.999    0.751   0.248
   12     154     1.000    0.731   0.269
   13     157     1.000    0.731   0.269
   14     158     1.000    0.716   0.284
   15     158     1.000    0.716   0.284

Best test R2 = 0.791 at max_depth = 5
```

**This table is the entire module.** Read it column by column.

- **`train R2` never goes down.** 0.371 → 1.000. More depth is always better on the training data, by construction. **This column is worthless as evidence.**
- **`test R2` rises to a peak at depth 5 (0.791), then falls** to 0.716. Depths 1–4 are **underfitting**: too few questions to describe the town. Depths 6–15 are **overfitting**.
- **The `gap` column tells the story numerically.** At depth 3 the gap is −0.011 (essentially zero — the model generalises perfectly). By depth 14 the gap is 0.284. That 0.284 is exactly how much of the "performance" is memorisation.
- **`leaves` explains the mechanism.** At depth 14 the tree has **158 leaves for 160 training houses.** Almost every house has its own private leaf with its own private price. It hasn't learned about houses; it has written down a phone book.

**The one-paragraph explanation you should be able to write:** *As `max_depth` grows, the tree is allowed to ask more questions and split the 160 training houses into more and more leaves. Early on, each new question captures a real pattern — the school threshold, the size effect — so both the train and test scores rise together. Past depth 5, the questions stop describing the town and start describing the individual random noise in these particular 160 houses. Since that noise is different in the 40 test houses, memorising it actively hurts: train R² climbs to a perfect 1.000 while test R² sinks from 0.791 to 0.716. The crossover at depth 5 is where the tree stopped learning and started memorising.*

---

## ✍️ Practice

### 1. [Warm-up] Read a tree out loud

Here is the output of `export_text` from a tree trained to predict whether someone brings an umbrella:

```
|--- rain_chance_pct <= 45.00
|   |--- wind_kmh <= 30.00
|   |   |--- class: no umbrella
|   |--- wind_kmh >  30.00
|   |   |--- class: no umbrella
|--- rain_chance_pct >  45.00
|   |--- has_hood <= 0.50
|   |   |--- class: umbrella
|   |--- has_hood >  0.50
|   |   |--- class: no umbrella
```

Write out (a) every rule as an English sentence, (b) the prediction for `rain_chance_pct=60, wind_kmh=10, has_hood=1`, (c) the prediction for `rain_chance_pct=80, wind_kmh=50, has_hood=0`, and (d) which split in this tree is doing no work at all, and why the tree made it anyway.

**Done looks like:** four English rules, predictions of "no umbrella" then "umbrella", and you identify the `wind_kmh <= 30` split as useless because both of its branches give the same answer.

### 2. [Warm-up] Linear regression by hand

A pizza shop records how many pizzas were in an order and how many minutes the delivery took:

| pizzas (x) | 2 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|
| minutes (y) | 16 | 20 | 27 | 31 | 36 |

Compute x̄, ȳ, the two sums, the slope, and the intercept **by hand**, showing the deviation table. Then compute all five predictions, the MAE, the RMSE, and R². Confirm with sklearn. Finally, state the slope in a sentence with units, and predict a 7-pizza order.

**Done looks like:** slope 2.55, intercept 10.7, predictions `[15.8, 20.9, 26.0, 31.1, 36.2]`, MAE 0.48, RMSE 0.6164, R² 0.992748, a 7-pizza prediction of 28.55 minutes, and a sentence like "each extra pizza adds about 2.55 minutes to the delivery."

### 3. [Build] A tree on your own students data

Using `students.py` from Module 7, train a `DecisionTreeClassifier(max_depth=3, random_state=0)` to predict `club` from `age`, `hours`, and `score`. Fit it on **all 38 rows** (this exercise is about reading rules, not scoring). Print `export_text`, the training accuracy, and the feature importances.

Then answer in writing: (a) which feature did the tree ignore completely, (b) find a split where both children predict the same class, (c) is a training accuracy of about 0.68 good or bad, and how would you find out?

**Done looks like:** training accuracy 0.6842, `age` has importance 0.000, you can point at the `score <= 51.00` split where both branches say `art`, and your answer to (c) says the only way to know is to compare against the baseline (predict `chess` always = 14/38 = 0.368) and to run a proper train/test split.

### 4. [Build] Metrics on the housing data

Using `houses.py`, split 80/20 with `random_state=42` and fit a `LinearRegression`. Then, **by hand for the first three test houses only**, compute the residual, the absolute error, and the squared error, printing a small table. Compare your hand-computed 3-row MAE to sklearn's MAE over all 40 test houses and explain why they differ.

Then produce a residual plot: predicted price on x, residual on y, with a horizontal line at 0. State in one sentence what a *good* residual plot looks like and whether yours qualifies.

**Done looks like:** a 3-row table with your own arithmetic, sklearn's full-test MAE of 2.18, an explanation that 3 houses is a sample of 40 so the averages differ, and a residual plot whose points scatter randomly around zero with no funnel or curve — meaning the straight-line assumption is holding up.

### 5. [Stretch] The overfitting curve on a classification problem

Load `load_breast_cancer()`, split 80/20 with `random_state=42, stratify=y`. Loop `max_depth` from 1 to 15, recording **train accuracy, test accuracy, and number of leaves** for a `DecisionTreeClassifier(random_state=0)`. Print the table, find the best depth, and plot both curves with the best depth marked.

Then answer: at what depth does the train score first reach 1.0, and what is the test score doing at that moment? What does `get_depth()` return when you pass `max_depth=15`, and why isn't it 15?

**Done looks like:** train reaches 1.0 at depth 7 while test has already fallen from its peak of 0.9474 (depth 4) to 0.9123; `get_depth()` returns 7 no matter how high you set `max_depth`, because the tree ran out of impure leaves to split and stopped on its own.

### 6. [Stretch] Choose the metric on purpose

Build two sets of predictions for the same 10 true values `[10, 12, 11, 13, 12, 11, 10, 12, 11, 13]`:

- **Model A** — off by exactly +1 on every prediction.
- **Model B** — exactly right on the first nine, and off by +10 on the tenth.

Compute MAE and RMSE for both. Then invent two different real-world scenarios: one where you would clearly prefer Model A, and one where you would clearly prefer Model B. Finish with a sentence on which metric you would report in each scenario.

**Done looks like:** both models have MAE = 1.0; Model A has RMSE 1.0 and Model B has RMSE 3.1623; your scenarios are concrete (e.g. an insulin dose calculator versus a weekly grocery budget estimate), and you state that RMSE is the metric that distinguishes them while MAE cannot.

---

## 🤔 Think Deeper

### 1. The tree gives worse predictions and better explanations. When is that the right trade?

*How to reason about it:* on the housing data, linear regression scored R² 0.935 and the depth-2 tree scored 0.531, but only one of them can be printed on a poster and understood by a person selling their home. Think about three settings — a bank refusing a loan, a streaming service ordering your homepage, an app estimating your bus arrival — and ask, for each: does the person affected have a right to an explanation? Does anybody need to *audit* the decision later? Would a wrong answer with a clear reason be more or less acceptable than a right answer with no reason? Then consider that "explainable" and "honest" are not the same thing: a tree's rules are readable, but a readable rule can still encode something ugly.

### 2. Your depth curve says depth 5. You picked depth 5. What did you just spend?

*How to reason about it:* you looked at the test score fifteen times and chose the winner. Count how much information about the test set has now flowed into your model. Compare it with Module 8, where you picked `k` the same way. Now think about a research team that tries 400 model variants on the same test set and reports the best — is their reported number an estimate of future performance, or an estimate of the maximum of 400 noisy draws? Think about what the honest report looks like when you have only 200 rows and cannot afford a third split, and whether "I chose depth 5 by looking at the test curve" printed next to the number is enough.

### 3. The model learned that houses far from a school are cheaper. What happens when someone *uses* that?

*How to reason about it:* the coefficient −2.618 is a description of past sales. Now imagine a property website deploys it and shows every buyer and seller a price estimate. Trace what happens over two years: sellers near schools ask more because the model says so; buyers accept it because the model says so; next year's data confirms the model. Consider whether the model is now measuring the market or *making* it. Then think about who is priced out of neighbourhoods near schools, whether that effect existed before the model, and whether "the model was accurate" is a defence. Finally: what would you have to measure to even detect this happening?

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Using `accuracy_score` on a regression | Habit from Module 8 | Regression uses MAE / RMSE / R². Accuracy is for categories only. |
| `ValueError: Expected 2D array, got 1D array` when fitting one feature | `X` came out shape `(n,)` | `X = x.reshape(-1, 1)` or `df[["col"]].values` (double brackets) |
| Reporting train R² as "the model's R²" | You called `.score()` on the training data | Score on `X_test, y_test`; report both and show the gap |
| A tree with no `max_depth` scores 1.000 and you celebrate | Unlimited depth always memorises | Look at the test score, and at `get_n_leaves()` versus `len(X_train)` |
| Re-splitting inside the depth loop | It felt like extra rigour | Split **once** before the loop, or you measure shuffle luck, not complexity |
| Comparing R² across two different datasets | R² has no units so it looks portable | R² is relative to *that* dataset's variance. Compare MAE within one dataset. |
| Concluding "bedrooms matter 34× more than size" from coefficients 2.99 and 0.088 | Coefficients depend on units | Standardize the features first, or compare `coef × feature_std` |
| Reading a coefficient as a cause | The sentence "per extra bedroom" sounds causal | Say "goes with" not "causes"; a coefficient is an association |
| Scaling data before a decision tree | Copied the Module 8 pipeline | Trees split one column at a time — scaling changes nothing. Harmless but pointless. |
| A negative R² and you assume a bug | Negative just means "worse than guessing the mean" | Check against `DummyRegressor(strategy="mean")` — a real model can be that bad |
| Trusting a test score from 40 rows to 3 decimal places | The number *printed* 3 decimals | With 40 test rows, differences under ~0.03 R² are noise |
| Different tree every run | No `random_state` — ties between equally good splits break randomly | `DecisionTreeClassifier(random_state=0)` |
| Extrapolating a line far past the data | Nothing stops you typing `predict([[100]])` | Check the training range first; a line will happily predict a score of 158 |

---

## 🛠️ Mini-Project — Model Bake-Off

### Goal

On **one fixed train/test split** of a regression problem, compare three models with completely different personalities — kNN, a decision tree, and linear regression — then draw the train/test depth curve and mark the overfitting point.

### Starter steps

**Step 1 — Set up the split, once (15 min).**

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from houses import make_houses, FEATURES, TARGET

df = make_houses()
X, y = df[FEATURES].values, df[TARGET].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(X_train.shape, X_test.shape)     # (160, 4) (40, 4)
```

Write in a comment: *"This split is fixed for the whole file. Every model below sees exactly the same 160 training houses and the same 40 test houses."* Fairness in a bake-off comes entirely from that sentence being true.

**Step 2 — Write one scoring function you reuse for every model (20 min).**

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def report(name, model):
    """Fit-already-done model -> a dict of metrics on the fixed split."""
    pred = model.predict(X_test)
    return {
        "model": name,
        "MAE": round(mean_absolute_error(y_test, pred), 2),
        "RMSE": round(np.sqrt(mean_squared_error(y_test, pred)), 2),
        "test_R2": round(r2_score(y_test, pred), 3),
        "train_R2": round(model.score(X_train, y_train), 3),
    }
```

A single function means you cannot accidentally score two models differently.

**Step 3 — Bake off at least five entries (45 min).** Include the lazy baseline, because a bake-off without it is a bake-off you can't interpret.

| Entry | What to build |
|---|---|
| Baseline | `DummyRegressor(strategy="mean")` |
| kNN, scaled | `make_pipeline(StandardScaler(), KNeighborsRegressor(5))` |
| kNN, raw | `KNeighborsRegressor(5)` — to prove Module 8's point again |
| Tree, depth 5 | `DecisionTreeRegressor(max_depth=5, random_state=0)` |
| Tree, unlimited | `DecisionTreeRegressor(random_state=0)` |
| Linear regression | `LinearRegression()` |

Assemble the results into a DataFrame and print it. Your table must **name the metric** in the header — a bare column of numbers labelled "score" is not a result.

**Step 4 — The depth curve (45 min).** Loop `max_depth` 1 to 15, record train and test R², plot both lines, mark the best depth with a vertical line, and label everything (Module 7 rules apply in full).

**Step 5 — Write the crossover paragraph (30 min).** At least 150 words explaining:

- what the train line does and why it can only go up
- where the test line peaks and what that depth means in leaves
- what "the gap" is measuring, in plain words
- why depth 1 and depth 15 are wrong for *different* reasons
- which model you'd actually deploy, and why it may not be the highest-scoring one

**Step 6 — The honesty section (15 min).** Three bullets:

- the size of the test set and what one house is worth in R² terms
- the sentence "I chose the depth by looking at the test curve, so this estimate is optimistic"
- one thing about this dataset that makes the results easier than real life

### Success criteria checklist

- [ ] One split, created once, used by every model — verifiable by reading the file top to bottom
- [ ] A comparison table with **at least five** entries including a baseline
- [ ] Every metric column named with its metric (`MAE (lakh)`, `test R²`, …)
- [ ] Both `train_R2` and `test_R2` present for every model
- [ ] A two-line depth curve, fully labelled, y-axis from 0
- [ ] The best depth marked on the plot with a line or annotation
- [ ] A crossover paragraph of 150+ words
- [ ] The honesty section with the test-set size stated
- [ ] `random_state` set everywhere; the file runs top to bottom without errors

### Level it up

**Swap the dataset and see whether the story survives.** Run the identical script on `sklearn.datasets.load_diabetes()` (442 real patients, 10 features, target = disease progression after one year — no download needed). Two things will change and both are instructive: the best R² will be far lower (real data is much noisier than simulated data), and the ranking of your three models may flip. Write two sentences on which conclusions from the housing run transferred and which were artefacts of data you generated yourself. Then think about which of those two experiments taught you more.

---

## 🔑 Key Takeaways

- **Classification predicts a category, regression predicts a number**, and the metric must match: accuracy for one, MAE/RMSE/R² for the other.
- **A decision tree is a flowchart it wrote itself.** `export_text` turns it into English rules you can read, argue with, and hand to somebody who doesn't code — and it never needs scaling.
- **Linear regression is two numbers per feature**: a slope you can state in units ("₹3 lakh per extra bedroom") and an intercept. It draws smooth lines and cannot express thresholds; a tree draws steps and cannot express smooth lines.
- **Always compute the lazy baseline.** MAE 2.18 means nothing until you know that guessing the mean gives MAE 9.21.
- **The train score always rises with complexity, so it is not evidence.** Only the test score, on data the model has never seen, tells you anything.
- **Underfitting = both scores low. Overfitting = train high, test low.** The gap between them is the size of the memorisation, and the peak of the test curve is where you stop turning the dial.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **classification** | Predicting which category something is | setosa / versicolor / virginica |
| **regression** | Predicting a number on a sliding scale | a house price of 36.45 lakh |
| **decision tree** | A flowchart of yes/no questions the model wrote itself | "petal width ≤ 0.8? → setosa" |
| **split** | One yes/no question in a tree | `km_to_school <= 1.65` |
| **leaf** | The end of a branch, where the answer lives | "value: [33.91]" |
| **depth** | How many questions deep the tree may go | `max_depth=5` gave 30 leaves |
| **Gini impurity** | How mixed a group is; 0 = all one class | 4 fails + 6 passes → 0.48 |
| **linear regression** | Fitting the best straight line through the dots | score = 5.7 × hours + 44.9 |
| **slope** | How much y changes per 1 unit of x | +2.994 lakh per extra bedroom |
| **intercept** | What the line predicts when every feature is 0 | 44.9 points at zero study hours |
| **coefficient** | The slope belonging to one feature | −0.377 for `age_years` |
| **residual** | Actual minus predicted, for one row | 74 − 73.4 = +0.6 |
| **MAE** | Average size of your mistakes, in the target's units | "off by 2.18 lakh on average" |
| **RMSE** | Like MAE but punishes big misses much harder | 1.0 vs 3.16 for the same MAE |
| **R²** | Fraction of the variation explained; 1 is perfect, 0 is guessing the mean | 0.935 |
| **baseline** | The score of the laziest possible model | always guess the mean → MAE 9.21 |
| **underfitting** | Too simple: bad on training *and* test data | depth-1 tree, R² 0.371 / 0.282 |
| **overfitting** | Too complex: memorised the training rows | depth-14 tree, R² 1.000 / 0.716 |
| **train/test gap** | Train score minus test score | 0.284 at depth 14 |
| **complexity dial** | The setting that controls how flexible a model is | `max_depth`, or `k` in kNN |
| **extrapolation** | Predicting outside the range you have data for | 20 hours → a score of 158.9 |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1. [Warm-up] Read a tree out loud

**(a) The rules in English.**

1. *"If the chance of rain is 45% or less and the wind is 30 km/h or less → **no umbrella**."*
2. *"If the chance of rain is 45% or less and the wind is more than 30 km/h → **no umbrella**."*
3. *"If the chance of rain is more than 45% and you have no hood (`has_hood` = 0) → **umbrella**."*
4. *"If the chance of rain is more than 45% and you do have a hood (`has_hood` = 1) → **no umbrella**."*

Rules 1 and 2 collapse into one: *"Rain chance 45% or less → no umbrella, whatever the wind."*

**(b) `rain_chance_pct=60, wind_kmh=10, has_hood=1`**

```
rain_chance_pct <= 45?   60 <= 45?   NO   → go right
has_hood <= 0.5?          1 <= 0.5?  NO   → go right
                                          → NO UMBRELLA
```

**(c) `rain_chance_pct=80, wind_kmh=50, has_hood=0`**

```
rain_chance_pct <= 45?   80 <= 45?   NO   → go right
has_hood <= 0.5?          0 <= 0.5?  YES  → go left
                                          → UMBRELLA
```

Note that `wind_kmh=50` was never consulted in either prediction. On the right-hand side of the tree, wind doesn't appear at all.

**(d) The useless split.** `wind_kmh <= 30.00` is doing no work: both of its children predict **no umbrella**. Following either branch gives the same answer, so the question is pure decoration.

**Why the tree made it anyway.** The tree splits greedily to reduce **impurity**, not to change the final label. If the "rain ≤ 45%" group was, say, 18 no-umbrella and 2 umbrella, a wind split might separate it into a perfectly pure group of 12 and a slightly-mixed group of 8 — impurity drops, so the split looks worthwhile to the algorithm — yet the *majority* class in both groups is still "no umbrella", so the prediction never changes. This is a small, visible instance of the tree fitting detail rather than signal, and it's a good argument for a smaller `max_depth`.

**Bonus note on `has_hood <= 0.50`.** `has_hood` is 0 or 1, so the threshold 0.5 is just the tree's way of writing "is it 0 or is it 1?" You'll see `<= 0.5` on every yes/no feature.

---

### 2. [Warm-up] Linear regression by hand

**Step 1 — means.**

```
x̄ = (2 + 4 + 6 + 8 + 10) ÷ 5 = 30 ÷ 5 = 6
ȳ = (16 + 20 + 27 + 31 + 36) ÷ 5 = 130 ÷ 5 = 26
```

**Step 2 — deviation table.**

| x | y | dx = x − 6 | dy = y − 26 | dx·dy | dx² | dy² |
|---|---|---|---|---|---|---|
| 2 | 16 | −4 | −10 | 40 | 16 | 100 |
| 4 | 20 | −2 | −6 | 12 | 4 | 36 |
| 6 | 27 | 0 | 1 | 0 | 0 | 1 |
| 8 | 31 | 2 | 5 | 10 | 4 | 25 |
| 10 | 36 | 4 | 10 | 40 | 16 | 100 |
| | | | | **Σ = 102** | **Σ = 40** | **Σ = 262** |

**Step 3 — slope and intercept.**

```
slope     = 102 ÷ 40 = 2.55
intercept = 26 − 2.55 × 6 = 26 − 15.3 = 10.7
```

**The model: minutes = 2.55 × pizzas + 10.7**

**Step 4 — predictions and errors.**

| x | actual | predicted | residual | \|residual\| | residual² |
|---|---|---|---|---|---|
| 2 | 16 | 5.10 + 10.7 = **15.8** | +0.2 | 0.2 | 0.04 |
| 4 | 20 | 10.20 + 10.7 = **20.9** | −0.9 | 0.9 | 0.81 |
| 6 | 27 | 15.30 + 10.7 = **26.0** | +1.0 | 1.0 | 1.00 |
| 8 | 31 | 20.40 + 10.7 = **31.1** | −0.1 | 0.1 | 0.01 |
| 10 | 36 | 25.50 + 10.7 = **36.2** | −0.2 | 0.2 | 0.04 |
| | | | **Σ = 0.0** | **Σ = 2.4** | **Σ = 1.90** |

**Step 5 — metrics.**

```
MAE  = 2.4 ÷ 5 = 0.48 minutes
MSE  = 1.90 ÷ 5 = 0.38
RMSE = √0.38 = 0.6164 minutes
R²   = 1 − (1.90 ÷ 262) = 1 − 0.0072519 = 0.992748
```

**Step 6 — confirm.**

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

x = np.array([2, 4, 6, 8, 10]).reshape(-1, 1)
y = np.array([16, 20, 27, 31, 36])

m = LinearRegression().fit(x, y)
p = m.predict(x)

print("slope    :", m.coef_)               # [2.55]
print("intercept:", m.intercept_)          # 10.699999999999992
print("preds    :", np.round(p, 2))        # [15.8 20.9 26.  31.1 36.2]
print("MAE      :", round(mean_absolute_error(y, p), 4))         # 0.48
print("RMSE     :", round(np.sqrt(mean_squared_error(y, p)), 4)) # 0.6164
print("R2       :", round(r2_score(y, p), 6))                    # 0.992748
print("7 pizzas :", m.predict([[7]]))                            # [28.55]
```

Output:

```
slope    : [2.55]
intercept: 10.699999999999992
preds    : [15.8 20.9 26.  31.1 36.2]
MAE      : 0.48
RMSE     : 0.6164
R2       : 0.992748
7 pizzas : [28.55]
```

**The slope in words:** *"Each extra pizza in the order adds about 2.55 minutes to the delivery time, and the base time for an order of zero pizzas would be 10.7 minutes."* The intercept has a sensible real-world meaning here for once — roughly the drive time before any pizza-loading happens.

**7-pizza prediction:** 2.55 × 7 + 10.7 = 17.85 + 10.7 = **28.55 minutes**. This one is *interpolation* (7 sits inside the observed range of 2–10), which is far safer than the extrapolation in the Worked Example.

---

### 3. [Build] A tree on your own students data

```python
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text
from students import build_students        # from Module 7

df = build_students()
feature_names = ["age", "hours", "score"]
X = df[feature_names].values
y = df["club"].values

tree = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X, y)

print(export_text(tree, feature_names=feature_names))
print("training accuracy:", round(tree.score(X, y), 4))
print("feature importances:")
for n, imp in zip(feature_names, tree.feature_importances_):
    print(f"  {n:6s} {imp:.3f}")

# The baseline: always guess the biggest club.
labels, counts = np.unique(y, return_counts=True)
print("class counts:", dict(zip(labels, counts)))
print("baseline (always guess the biggest):", round(counts.max() / len(y), 4))
```

Output:

```
|--- hours <= 1.75
|   |--- score <= 46.50
|   |   |--- class: music
|   |--- score >  46.50
|   |   |--- score <= 51.00
|   |   |   |--- class: art
|   |   |--- score >  51.00
|   |   |   |--- class: art
|--- hours >  1.75
|   |--- hours <= 4.25
|   |   |--- score <= 70.50
|   |   |   |--- class: art
|   |   |--- score >  70.50
|   |   |   |--- class: chess
|   |--- hours >  4.25
|   |   |--- score <= 94.00
|   |   |   |--- class: music
|   |   |--- score >  94.00
|   |   |   |--- class: chess

training accuracy: 0.6842
feature importances:
  age    0.000
  hours  0.398
  score  0.602
class counts: {'art': 12, 'chess': 14, 'music': 12}
baseline (always guess the biggest): 0.3684
```

**(a) Which feature did the tree ignore?** `age`, with an importance of exactly **0.000**. It never appears in a single split. That fits what Module 7 found: age is related to study hours (r = −0.57), so once the tree has split on `hours` there is nothing left for `age` to add.

**(b) A split where both children predict the same class.** `score <= 51.00`: the left branch says `art` and the right branch says `art`. Useless, exactly like the iris example in the Hands-On. The tree made it because it reduced Gini impurity slightly in the training rows, not because it changes any prediction.

**(c) Is 0.6842 good or bad?**

Neither, until you compare it to something. Two comparisons:

1. **The baseline.** Always guessing `chess` scores 14/38 = **0.3684**. The tree nearly doubles that, so it has genuinely learned something.
2. **Anything at all about generalisation.** This 0.6842 was measured on the *same 38 rows the tree learned from* — it's the Module 8 sin. The way to actually find out is a train/test split:

```python
from sklearn.model_selection import train_test_split
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
t = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X_tr, y_tr)
print("train:", round(t.score(X_tr, y_tr), 4))
print("test :", round(t.score(X_te, y_te), 4))
```

**But here is the most important thing to say about this exercise:** with 38 rows split three ways, a test set is about 10 students. One student is worth 10 percentage points. **No number you compute on this dataset can be trusted to better than about ±15 points.** The right conclusion is not "the tree gets 68%" — it's "this dataset is far too small to support a claim about accuracy, and the honest output here is the *rules*, not the score." Recognising when a dataset cannot answer your question is a real skill, and it shows up constantly.

---

### 4. [Build] Metrics on the housing data

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from houses import make_houses, FEATURES, TARGET

df = make_houses()
X, y = df[FEATURES].values, df[TARGET].values
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

lin = LinearRegression().fit(X_train, y_train)
pred = lin.predict(X_test)

# ---- hand table for the first three test houses ------------------------
print(f"{'#':>2} {'actual':>8} {'pred':>8} {'residual':>9} {'|err|':>7} {'err^2':>8}")
running_abs = 0.0
for i in range(3):
    a, p = y_test[i], pred[i]
    r = a - p
    running_abs += abs(r)
    print(f"{i:>2} {a:8.2f} {p:8.2f} {r:9.2f} {abs(r):7.2f} {r**2:8.2f}")

print(f"\nMAE over just these 3 houses : {running_abs / 3:.3f}")
print(f"MAE over all 40 test houses  : {mean_absolute_error(y_test, pred):.3f}")

# ---- residual plot -----------------------------------------------------
resid = y_test - pred
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(pred, resid, s=60, color="#1f77b4", alpha=0.75, edgecolors="white")
ax.axhline(0, color="#d62728", linewidth=2, linestyle="--",
           label="perfect prediction")
ax.set_title("Residuals scatter evenly around zero — the straight line fits")
ax.set_xlabel("Predicted price (lakh)")
ax.set_ylabel("Residual = actual − predicted (lakh)")
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig("residuals.png", dpi=150)
plt.show()

print("\nresidual mean:", round(resid.mean(), 3))
print("residual std :", round(resid.std(), 3))
print("worst miss   :", round(np.abs(resid).max(), 3), "lakh")
```

Output:

```
 #   actual     pred  residual   |err|    err^2
 0    24.20    26.29     -2.09    2.09     4.37
 1    16.30    13.47      2.83    2.83     8.01
 2    25.20    25.76     -0.56    0.56     0.31

MAE over just these 3 houses : 1.827
MAE over all 40 test houses  : 2.179
```

Check row 0 by hand: residual = 24.20 − 26.29 = **−2.09**, absolute error = **2.09**, squared error = 2.09² = **4.37**. The 3-house MAE is (2.09 + 2.83 + 0.56) ÷ 3 = 5.48 ÷ 3 = **1.827**.

**Why the two MAEs differ.** Three houses is a tiny sample of the forty. These particular three happened to be slightly easier than average, so the 3-house MAE (1.827) came out below the full-test MAE (2.179); a different three could easily have come out above it. This is the same lesson as the test-set-size discussion in Module 8, at a smaller scale: **an average over three things is barely an average at all.** The full-test MAE of 2.18 lakh is the number to report.

**What a good residual plot looks like.** A formless cloud of points, evenly scattered above and below the zero line, with roughly the same vertical spread all the way across. That means the model's mistakes are random noise — there is no leftover pattern for a better model to find.

**Two bad patterns to watch for:**

```
  GOOD (random cloud)        BAD (curve left)         BAD (funnel)
   +│  ·  · ·   ·  ·          +│ ·        ·            +│      ·   ·
    │· ·   ·  ·  · ·           │  ·      ·              │   ·   ·  ·
   0├─·──·───·───·──·         0├────·──·────           0├──·──·──·───
    │ ·  ·  · ·   ·            │     ··                 │ ·   ·   ·
   −│   ·   ·   ·  ·          −│   ·   ·                −│       ·  ·
    └────────────────          └────────────            └────────────
   errors are pure noise      you fitted a line to      errors grow with
                              something curved          the prediction
```

**Does yours qualify?** Yes. The printed diagnostics come out as:

```
residual mean: 0.037
residual std : 2.642
worst miss   : 6.253 lakh
```

A mean of 0.037 lakh on prices averaging 22 lakh is essentially zero — the model is not systematically over- or under-predicting. The spread is roughly constant across the plot, which is unsurprising because we *built* this data with a linear rule plus Gaussian noise of standard deviation 2.0 (and the residual std of 2.642 is close to that, the extra coming from the school bonus the line cannot express). The worst single miss is 6.25 lakh — worth reporting alongside the MAE, because "off by 2.18 on average" and "off by up to 6.25 in the worst case" are two different promises. If you look closely at the low-price end you may spot a faint pattern left over from that +6 lakh school bonus. Finding a missing feature by eye, in a residual plot, is exactly how people improve real models.

---

### 5. [Stretch] The overfitting curve on a classification problem

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

data = load_breast_cancer()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("train:", X_train.shape, " test:", X_test.shape)

depths = list(range(1, 16))
train_acc, test_acc, leaves, actual_depth = [], [], [], []

for d in depths:
    t = DecisionTreeClassifier(max_depth=d, random_state=0).fit(X_train, y_train)
    train_acc.append(t.score(X_train, y_train))
    test_acc.append(t.score(X_test, y_test))
    leaves.append(t.get_n_leaves())
    actual_depth.append(t.get_depth())

print(f"{'max_depth':>9} {'real depth':>11} {'leaves':>7} "
      f"{'train':>7} {'test':>7} {'gap':>7}")
for d, ad, lv, tr, te in zip(depths, actual_depth, leaves, train_acc, test_acc):
    print(f"{d:9d} {ad:11d} {lv:7d} {tr:7.4f} {te:7.4f} {tr - te:7.4f}")

best_i = int(np.argmax(test_acc))
print(f"\nBest test accuracy {test_acc[best_i]:.4f} at max_depth={depths[best_i]}")

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.plot(depths, train_acc, marker="o", linewidth=2, color="#1f77b4",
        label="train accuracy")
ax.plot(depths, test_acc, marker="s", linewidth=2, color="#d62728",
        label="test accuracy")
ax.axvline(depths[best_i], color="#2ca02c", linestyle="--", linewidth=2,
           label=f"best test accuracy at depth {depths[best_i]}")
ax.set_title("Breast cancer tree: test accuracy peaks at depth 4, then declines")
ax.set_xlabel("max_depth")
ax.set_ylabel("Accuracy (fraction of 114 test patients correct)")
ax.set_ylim(0, 1.05)
ax.set_xticks(depths)
ax.grid(alpha=0.3)
ax.legend(loc="lower right")
fig.tight_layout()
fig.savefig("bc_depth_curve.png", dpi=150)
plt.show()
```

Output:

```
train: (455, 30)  test: (114, 30)
max_depth  real depth  leaves   train    test     gap
        1           1       2  0.9231  0.9211  0.0020
        2           2       4  0.9582  0.8947  0.0635
        3           3       7  0.9758  0.9386  0.0372
        4           4      11  0.9868  0.9474  0.0394
        5           5      15  0.9934  0.9298  0.0636
        6           6      18  0.9978  0.9123  0.0855
        7           7      19  1.0000  0.9123  0.0877
        8           7      19  1.0000  0.9123  0.0877
        9           7      19  1.0000  0.9123  0.0877
       10           7      19  1.0000  0.9123  0.0877
       11           7      19  1.0000  0.9123  0.0877
       12           7      19  1.0000  0.9123  0.0877
       13           7      19  1.0000  0.9123  0.0877
       14           7      19  1.0000  0.9123  0.0877
       15           7      19  1.0000  0.9123  0.0877

Best test accuracy 0.9474 at max_depth=4
```

**Question 1 — at what depth does train first reach 1.0, and what is test doing?**

Train accuracy hits **1.0000 at depth 7**. At that exact moment, test accuracy is **0.9123** — which is *below* its own peak of 0.9474 at depth 4, and barely above the depth-1 score of 0.9211. In other words: **by the time the model became perfect on the training data, it had already lost most of what it gained on real data.** The gap widened from 0.0020 at depth 1 to 0.0877 at depth 7.

That single sentence is the whole reason train scores are not evidence. If you had only looked at the training column, you would have chosen depth 7 or deeper and shipped a *worse* model with total confidence.

**Question 2 — why doesn't `get_depth()` return 15?**

Because `max_depth` is a **ceiling, not a target**. The tree keeps splitting only while a node is still impure and still splittable. At depth 7 every leaf on this training set is already pure (all 455 training patients are correctly separated, hence train accuracy 1.0000), so there is nothing left to split. Setting `max_depth=8` through `15` changes literally nothing: real depth stays 7, leaves stay 19, and every score is identical. That's why the right-hand end of the curve is perfectly flat.

**An honest footnote worth writing down.** Depth 1 scores 0.9211 and depth 4 scores 0.9474 — a difference of 0.0263, which on 114 test patients is **exactly 3 patients**. A one-question tree ("is the worst perimeter above some threshold?") is within three patients of the best tree we found. For a medical screening tool that difference matters enormously, and it also sits well inside the noise of a single split, which is precisely why real medical models are validated on separate cohorts rather than on one 114-person test set.

---

### 6. [Stretch] Choose the metric on purpose

```python
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

y_true = np.array([10, 12, 11, 13, 12, 11, 10, 12, 11, 13])

# Model A: off by exactly +1 on every single prediction.
pred_a = y_true + 1

# Model B: exactly right nine times, off by +10 once.
pred_b = y_true.copy()
pred_b[9] = y_true[9] + 10

for name, p in [("Model A (spread evenly)", pred_a),
                ("Model B (one big miss)", pred_b)]:
    mae = mean_absolute_error(y_true, p)
    rmse = np.sqrt(mean_squared_error(y_true, p))
    errors = np.abs(y_true - p)
    print(f"{name}")
    print(f"  errors : {errors}")
    print(f"  MAE    : {mae:.4f}")
    print(f"  RMSE   : {rmse:.4f}")
    print(f"  worst  : {errors.max()}")
    print()
```

Output:

```
Model A (spread evenly)
  errors : [1 1 1 1 1 1 1 1 1 1]
  MAE    : 1.0000
  RMSE   : 1.0000
  worst  : 1

Model B (one big miss)
  errors : [0 0 0 0 0 0 0 0 0 10]
  MAE    : 1.0000
  RMSE   : 3.1623
  worst  : 10
```

**The arithmetic, by hand.**

Model A: every |error| is 1, so MAE = 10 ÷ 10 = 1.0. Every error² is 1, so MSE = 10 ÷ 10 = 1.0 and RMSE = √1 = 1.0.

Model B: nine errors of 0 and one of 10, so MAE = (0×9 + 10) ÷ 10 = 1.0 — **identical**. But squared: nine 0s and one 100, so MSE = 100 ÷ 10 = 10 and RMSE = √10 = **3.1623**.

**Scenario where Model A is clearly better: an insulin dose calculator.**

Predicting a dose in units. Model A is off by 1 unit every time — an annoying, correctable, *survivable* error that a nurse notices and adjusts. Model B is perfect nine times out of ten and then, once, recommends 10 units too many. That single event can be life-threatening, and it is worse than ten small errors *combined*. **Here you would report RMSE**, because RMSE is the metric that can see the difference between these two models, and the thing you fear is the catastrophic tail, not the typical case.

**Scenario where Model B is clearly better: estimating a household's weekly grocery bill for a budgeting app.**

Model A is wrong every single week by ₹1 — the user never once sees a number they'd call correct, and the app feels permanently untrustworthy. Model B nails the bill nine weeks out of ten and is badly wrong in the week you threw a party — which the user can immediately explain to themselves ("oh, the birthday"). Nine perfect weeks builds far more trust than ten near-misses, and the one big miss has an obvious cause and no real cost. **Here you would report MAE** (and probably also "hit rate within ₹2"), because the typical experience is what matters and a rare, explicable outlier shouldn't be allowed to dominate the headline number.

**The one-sentence summary:** MAE asks *"how wrong am I on a typical day?"* while RMSE asks *"how bad can it get?"* — and since these two models score identically on the first question and 3× apart on the second, choosing the metric is really choosing which of those two questions your project is about.

**A practical habit that falls out of this:** report **both**, plus the worst single error. Three numbers cost nothing extra to compute and make it impossible for a reader to be fooled by a model whose average looks fine because its disasters are rare.

</details>

---

[⬅ Previous](module-08-first-model-knn.md) · [Level 2 Home](README.md) · [Next ➡](capstone.md)

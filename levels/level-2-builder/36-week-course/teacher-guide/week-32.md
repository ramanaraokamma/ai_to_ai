# Week 32 — Predicting a Number: Lines, MAE, and R²

[⬅ Week 31](week-31.md) · [Course Home](../README.md) · [Week 33 ➡](week-33.md) · [Student Guide](../student-guide/week-32.md) · [Workbook](../workbook/week-32.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — a new kind of question, and a new kind of score |
| **Big idea** | When the answer is a number instead of a category you fit a line — and you measure the error in the units of the thing itself. |
| **New vocabulary** | regression · slope · intercept · mean absolute error · R-squared |
| **New syntax** | `LinearRegression()` · `model.coef_` / `model.intercept_` · `mean_absolute_error(y_true, y_pred)` · `r2_score(y_true, y_pred)` |
| **Materials** | Printed workbook pages 32.1–32.6 · **graph paper, 5 mm squares, 2 sheets** · **a ruler with millimetres** · a sharp pencil and an eraser · a calculator · last week's `export_text` printout · the Bug Log |
| **Tech needed** | Python 3 with scikit-learn. No new install. No internet. |
| **Prep time** | 20 minutes the night before, 5 minutes on the day |

> **⚠️ Watch out:** the ruler comes out **before** the laptop. The student fits the first line by hand, by eye, on graph paper, and writes down their own slope — and only then does scikit-learn get to fit its version. If the computer goes first, the whole lesson becomes "trust the machine" instead of "the machine agrees with me", and those two lessons are not remotely the same.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Tell classification from regression** by looking at the label column and saying which it is.
2. **Fit a line** with `LinearRegression()` and read the slope and the intercept out of the model.
3. **State the slope in real units**, with the unit named — "+3.6 marks per extra hour of revision".
4. **Compute MAE** and say what it means in the units of the thing being predicted.
5. **Explain why a high R² alone can still mislead you**, and why a low one is not always a failure.

Observable evidence: a hand-drawn line on graph paper with a slope read off by counting squares; that slope written next to scikit-learn's slope; one sentence stating the slope with its unit; MAE written as "off by about N marks"; and one written sentence naming something the line cannot explain.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

Everything below is arithmetic you can do with a pencil, plus four lines of code. There is no new mathematics here beyond "how steep is this line", which the student has met in beginning algebra. What is new is **insisting on units**, and that is the habit the whole week is for.

### 1. The only new idea: the answer is a number now

For four weeks the answer has been a **category** — setosa, versicolor, virginica. You are either right or you are wrong, and the score is "what fraction did I get right".

This week the answer is a **number**. How many marks somebody scored. How many minutes a delivery took. How wide a petal is.

> **Regression** — predicting a number on a sliding scale, rather than choosing from a fixed list.

The word is unhelpful and has an odd history; treat it as a label, not a clue. The distinction it marks, though, is the most useful sorting question in the whole subject:

| | Classification | Regression |
|---|---|---|
| The answer is | one of a short fixed list | any number |
| Example question | "Which species is this flower?" | "How many marks will she get?" |
| scikit-learn class name ends in | `Classifier` | `Regressor` |
| "Wrong" means | the wrong category | off by *some amount* |
| Main score | accuracy | MAE, RMSE, R² |

![Which one? or how much?](../figures/fig-w32-1-classification-versus-regression.svg)
*Figure 32.1 — Which one? or how much? Look at the label column: a short fixed list means classify, any number means regress.*

🍕 **The anchor to use out loud.** Classification is a multiple-choice question — you tick a box and you are right or you are not. Regression is guessing somebody's height. Being 1 cm out and being 40 cm out are both "wrong", and they are wildly different kinds of wrong. Accuracy cannot tell them apart, so regression needs its own scores.

**The classic beginner error, and you will meet it today:** calling `accuracy_score` on a regression. Guessing 63.9 marks when the truth is 64 is excellent, and accuracy scores it as a total failure, because 63.9 is not 64. You will stage this error on purpose in the Live-Code segment.

That naming rule — `Classifier` vs `Regressor` — is worth saying twice, because next week the student uses `KNeighborsRegressor` and `DecisionTreeRegressor` and needs to know those are the same tools as Weeks 29 and 31 with the answer type swapped.

### 2. A line is exactly two numbers

> **y = slope × x + intercept**
>
> **Slope** — how much y changes when x goes up by exactly 1.
> **Intercept** — what the line says y would be when x is 0.

That is the whole model. Two numbers. Where the tree gave you four sentences, a line gives you two numbers, and one of them — the slope — is a sentence in disguise.

🍕 **The anchor.** You have plotted revision hours against marks. You take a ruler, lay it through the middle of the dots so it is as close as possible to all of them at once, and draw along it. **That ruler is the model.** To predict a new person's marks you find their hours on the bottom axis, go up to the line, and read across.

This is not a simplification for children. It is literally what `LinearRegression()` does; the only difference is that the computer defines "as close as possible to all of them" precisely and you do it by eye.

**How the computer chooses.** Out of every possible line, it picks the one that makes the total of the **squared** vertical gaps as small as possible. Squaring means one big miss hurts far more than several small ones. That is a design choice with consequences, and it comes back at the end of the lesson.

### 3. The six numbers you will use all lesson — worked by hand, in full

Six classmates. `x` = hours of revision per week. `y` = marks out of 100.

| Classmate | hours (x) | marks (y) |
|---|---|---|
| A | 1 | 48 |
| B | 2 | 60 |
| C | 3 | 63 |
| D | 4 | 65 |
| E | 5 | 68 |
| F | 6 | 68 |

**Step 1 — the two means.**

```
x̄ = (1 + 2 + 3 + 4 + 5 + 6) ÷ 6 = 21 ÷ 6 = 3.5
ȳ = (48 + 60 + 63 + 65 + 68 + 68) ÷ 6 = 372 ÷ 6 = 62
```

Both come out clean on purpose. Do not skip checking them with the student; a wrong mean poisons everything below.

**Step 2 — how far each point sits from the middle.**

| x | y | dx = x − 3.5 | dy = y − 62 | dx × dy | dx² |
|---|---|---|---|---|---|
| 1 | 48 | −2.5 | −14 | 35.0 | 6.25 |
| 2 | 60 | −1.5 | −2 | 3.0 | 2.25 |
| 3 | 63 | −0.5 | 1 | −0.5 | 0.25 |
| 4 | 65 | 0.5 | 3 | 1.5 | 0.25 |
| 5 | 68 | 1.5 | 6 | 9.0 | 2.25 |
| 6 | 68 | 2.5 | 6 | 15.0 | 6.25 |
| | | | | **Σ = 63.0** | **Σ = 17.5** |

**Step 3 — slope and intercept.**

```
slope     = 63.0 ÷ 17.5 = 3.6
intercept = ȳ − slope × x̄ = 62 − 3.6 × 3.5 = 62 − 12.6 = 49.4
```

**The model is: marks = 3.6 × hours + 49.4**

**You will only ever type `LinearRegression()`.** But seeing those two sums once stops the model feeling like magic, and it is genuinely two sums and a division.

**Step 4 — say the slope out loud, with its unit. This is the sentence of the week.**

> *"Each extra hour of revision a week goes with about **3.6 more marks**."*

Three things about that sentence, and all three matter:

- **"per one hour"** — a slope is always "per one unit of x". Never say "the slope is 3.6" and stop. 3.6 what, per what?
- **"goes with", not "causes"** — this is Week 27's lesson arriving again. These six classmates who revised more scored more. That is not proof that revising causes marks; maybe the confident ones revise more *and* score more. Say "goes with". Insist on it.
- **the intercept is shakier than it looks.** 49.4 is what the line predicts for somebody who revised **zero** hours, and nobody in our six revised zero — the least was 1. The intercept is a prediction off the edge of the evidence. It is fine as part of the formula and shaky as a claim about real people.

**Step 5 — predictions and misses.**

| x | actual | predicted = 3.6x + 49.4 | miss = actual − predicted | \|miss\| | miss² |
|---|---|---|---|---|---|
| 1 | 48 | 3.6 + 49.4 = **53.0** | −5.0 | 5.0 | 25.00 |
| 2 | 60 | 7.2 + 49.4 = **56.6** | +3.4 | 3.4 | 11.56 |
| 3 | 63 | 10.8 + 49.4 = **60.2** | +2.8 | 2.8 | 7.84 |
| 4 | 65 | 14.4 + 49.4 = **63.8** | +1.2 | 1.2 | 1.44 |
| 5 | 68 | 18.0 + 49.4 = **67.4** | +0.6 | 0.6 | 0.36 |
| 6 | 68 | 21.6 + 49.4 = **71.0** | −3.0 | 3.0 | 9.00 |
| | | | **Σ = 0.0** | **Σ = 16.0** | **Σ = 55.20** |

> **Residual** — the vertical gap between a real point and the line: actual minus predicted. In class, call it **the miss**. Use the formal word once and then let it go.

![A miss is a vertical gap](../figures/fig-w32-3-residuals-are-the-misses.svg)
*Figure 32.2 — A miss is a vertical gap. Above the line is a plus, below it is a minus, and the pluses and minuses always cancel.*

The misses summing to zero is not luck — the least-squares line always passes through the point (x̄, ȳ) and balances above and below. **That is exactly why you cannot average the misses as they stand**, and exactly why MAE drops the signs.

**Step 6 — the two scores.**

> **Mean absolute error (MAE)** — the average size of your misses, ignoring whether they were over or under. Same units as the thing you are predicting.

```
MAE = 16.0 ÷ 6 = 2.6666... = 2.67 marks
```

Read it out loud: *"On average, my prediction is off by about two and a half to three marks."* **MAE is the score you can say to somebody who does not code**, because it is in the units of the thing itself. Marks. Minutes. Rupees. That is its entire advantage and it is a big one.

![MAE is the average height of the misses](../figures/fig-w32-4-mae-in-real-units.svg)
*Figure 32.3 — MAE is the average height of the misses. Sizes only, no signs.*

> **R-squared (R²)** — the fraction of the up-and-down variation in the answer that your model explains, compared with a model that just guesses the average every time. 1.0 is perfect, 0.0 is no better than guessing the average, and **negative is worse than guessing the average.**

```
R² = 1 − (sum of squared misses) ÷ (sum of squared distances from the mean)
```

The bottom half needs one more column — how much the marks vary around ȳ = 62:

| y | y − 62 | (y − 62)² |
|---|---|---|
| 48 | −14 | 196 |
| 60 | −2 | 4 |
| 63 | 1 | 1 |
| 65 | 3 | 9 |
| 68 | 6 | 36 |
| 68 | 6 | 36 |
| | | **Σ = 282** |

```
R² = 1 − (55.20 ÷ 282) = 1 − 0.19574 = 0.80426  →  0.804
```

Read it: *"the line explains about 80% of the up-and-down in these marks."* Guessing the average every time would have left squared error of 282; the line gets it down to 55.2.

**R² has no units.** That makes it good for comparing two models and useless for telling anybody what your predictions are worth. **Report MAE to a person. Report R² when comparing models.** Say that sentence; it settles a lot of later confusion.

### 4. Why a high R² can mislead — the demonstration that makes it land

This is objective 5 and it is the hardest one, so here is a concrete pair of results rather than a warning.

Take the iris flowers. Hide one measurement, try to predict it from the other three, and do that four times.

```text
measurement we hid    MAE (cm)      R2  mean-guess MAE
sepal length (cm)        0.234   0.852           0.699
sepal width (cm)         0.235   0.393           0.295
petal length (cm)        0.261   0.960           1.643
petal width (cm)         0.159   0.927           0.708
```

Look at the first two rows. **The MAE is almost identical — 0.234 cm and 0.235 cm.** The model is off by the same amount in both. Yet R² is 0.852 for one and 0.393 for the other.

Why? Because R² is not a measure of how good you are. It is a measure of **how much better you are than guessing the average**. Sepal length varies a lot between flowers, so guessing the average is off by 0.699 cm — and getting that down to 0.234 is a big win. Sepal width barely varies at all; guessing the average is already only off by 0.295 cm, so getting to 0.235 is barely an improvement, and R² says so.

The third column is the whole explanation, so make sure the student's script prints it. **"Mean-guess MAE" is how far off you would be if you ignored the other three measurements entirely and just said the average every time.** That is the thing R² measures you against.

*(Those mean-guess numbers are computed on the 30 held-back flowers. Across all 150 they come out at 0.688, 0.337, 1.563 and 0.658 cm — close enough, and the story does not change: sepal width is still by far the least varying of the four, which is exactly why its R² is the lowest.)*

![Same MAE, very different R²](../figures/fig-w32-5-same-mae-different-r2.svg)
*Figure 32.4 — Same MAE, very different R². R² asks how much better you are than guessing the mean.*

**Two conclusions to hand over, in these words:**

- **A high R² does not mean your predictions are good enough to use.** It means the thing you predicted varies a lot and you explained some of it. Always print the MAE next to it, in units.
- **A low R² does not always mean the model is bad.** Sometimes it means the thing barely varies, so there was little to explain. Sometimes it means the world is genuinely noisy. R² of 0.393 on sepal width is not a bug.

And the third, which is why this table is in the lesson at all: **lines do not fit everything.** Three of those four are over 0.85 and one is under 0.4, from the same dataset with the same code. Nobody should leave this lesson thinking a straight line is a universal answer.

### 5. Every line of this week's code, explained

```python
# week32_study_line.py
# Six classmates. Hours of revision per week -> marks out of 100.

import numpy as np                                  # arrays, from week 17
from sklearn.linear_model import LinearRegression    # NEW: the line-fitter
from sklearn.metrics import mean_absolute_error      # NEW: the average miss
from sklearn.metrics import r2_score                 # NEW: fraction explained

# X is always a TABLE: one row per person, one column per feature.
hours = np.array([1, 2, 3, 4, 5, 6]).reshape(-1, 1)  # 6 rows, 1 column
marks = np.array([48, 60, 63, 65, 68, 68])           # the answer, 6 numbers

print("hours shape:", hours.shape)                   # must be (6, 1)
print("marks shape:", marks.shape)                   # (6,) is right for y

model = LinearRegression()        # an empty ruler with no line on it yet
model.fit(hours, marks)           # lay the ruler through the six dots

print()
print("slope    :", model.coef_)          # marks gained per extra hour
print("intercept:", model.intercept_)     # marks the line gives at 0 hours
print("tidied up: marks =", round(model.coef_[0], 2), "x hours +",
      round(model.intercept_, 2))

guesses = model.predict(hours)            # what the line says for each person
print()
print("the line's guesses  :", guesses)
print("what really happened:", marks)
print("the misses          :", np.round(marks - guesses, 2))

print()
print("MAE:", round(mean_absolute_error(marks, guesses), 2), "marks")
print("R2 :", round(r2_score(marks, guesses), 3))

print()
print("a 7th classmate who revises 7 hours:", model.predict([[7]]))
print("somebody who revises 20 hours      :", model.predict([[20]]))
```

- `from sklearn.linear_model import LinearRegression` — the `linear_model` department of the toolbox. Note: `linear_model`, singular, with an underscore.
- `from sklearn.metrics import mean_absolute_error` — the same `metrics` department that gave you `accuracy_score` in Week 30. Both scores live there.
- `np.array([1, 2, 3, 4, 5, 6]).reshape(-1, 1)` — make the six hours into a **table with one column**. scikit-learn always wants `X` as rows × columns, even when there is only one column. `reshape(-1, 1)` means "one column, and work out the number of rows yourself". **This is the line the first staged bug lives in.**
- `marks = np.array([...])` — `y` stays a plain flat list of six numbers. `X` is a table; `y` is a column. That asymmetry looks wrong and is correct.
- `hours.shape` prints `(6, 1)` and `marks.shape` prints `(6,)`. Print both, every time, for the rest of the year. It is two seconds and it prevents the most common error in the whole level.
- `LinearRegression()` — build an unfitted model. Note the brackets: `LinearRegression` without them is the *recipe*; `LinearRegression()` is a *thing made from* the recipe.
- `model.fit(hours, marks)` — find the best line. Features first, answers second, always.
- `model.coef_` — the slope, or one slope per column if there are several. Trailing underscore = "only exists after `fit`". It prints as `[3.6]` — a list with one number in it, because there is one feature.
- `model.intercept_` — the single intercept. Prints as `49.400000000000006`, which is ordinary floating-point dust; see below.
- `model.predict(hours)` — the line's answer for each of the six.
- `mean_absolute_error(marks, guesses)` — **truth first, guess second.** MAE happens to give the same answer either way round; `r2_score` does not, so build the habit here where it is free.
- `r2_score(marks, guesses)` — the fraction explained.
- `model.predict([[7]])` — one new person, seven hours. **Two sets of brackets**: the outer is the table, the inner is the one row. One set gives you an error, and it is a useful one.

**The real output:**

```text
hours shape: (6, 1)
marks shape: (6,)

slope    : [3.6]
intercept: 49.400000000000006
tidied up: marks = 3.6 x hours + 49.4

the line's guesses  : [53.  56.6 60.2 63.8 67.4 71. ]
what really happened: [48 60 63 65 68 68]
the misses          : [-5.   3.4  2.8  1.2  0.6 -3. ]

MAE: 2.67 marks
R2 : 0.804

a 7th classmate who revises 7 hours: [74.6]
somebody who revises 20 hours      : [121.4]
```

Every number matches the hand table in section 3. Point that out loud — the student computed the slope with a pencil and the machine agreed.

> **⚠️ Watch out — the `49.400000000000006`.** That is not a bug and it is not the model being imprecise. Computers store decimals in binary, and 49.4 has no exact binary form, so a tiny crumb is left over at the fifteenth decimal place. It is called floating-point dust. The fix is `round(..., 2)` when you print, which is why the "tidied up" line is in the file. The student met this in Week 3; remind them rather than re-teaching it.

### 6. The last two lines, which are the honest part of the lesson

```text
a 7th classmate who revises 7 hours: [74.6]
somebody who revises 20 hours      : [121.4]
```

Seven hours giving 74.6 marks is fine — a bit beyond our data, but a reasonable stretch.

**Twenty hours gives 121.4 marks, and the test is out of 100.**

> **Extrapolation** — predicting outside the range of x values you actually have data for.

A straight line does not know where reality stops. It has never heard of a maximum mark. Push it far enough and it will confidently promise you 200. This is not a fault to be fixed; it is a limit to be *known*, and stating it is part of being honest about a model. Make sure this line gets printed in class. It is the single most memorable moment of the week.

### 7. The three misconceptions you will actually meet

**Misconception 1 — "the line is wrong because it doesn't go through the dots."**

A line that went through all six dots would not be a line. The dots are not on a line; six real people are not on a line. The line's job is to be as close to all of them as it can be at once, and the misses are the *evidence* of that job being done honestly. Say: *"If a model gets every training point exactly right, be suspicious."* (And then stop, because that is Week 33.)

**Misconception 2 — "R² of 0.804 means 80% accuracy."**

It does not, and this one is worth stamping on hard because the numbers look similar. R² is not a fraction of predictions that were right — no prediction here was exactly right. It is the fraction of the *variation* explained. The number that says how good the predictions are is MAE: **2.67 marks**. If a student says "80% accurate", ask: *"80% of what? Point at the thing."*

**Misconception 3 — "the intercept is the mark you get for doing no revision."**

Only if you believe the line where you have no data. Nobody in the six revised zero hours. 49.4 is what the *formula* says at zero, which is a different claim from what a real zero-hour student would score. Treat the intercept as machinery, not as a fact.

### 8. Where to stop

**Go this far:** classification vs regression; a line is a slope and an intercept; the slope stated in units; MAE in units; R² as "how much better than guessing the average"; extrapolation is a promise the data never made.

**Stop before:**

- **RMSE.** It is next week's, along with the reason it exists. If a student asks why we square things, say: *"Good question, and there's a score built on exactly that. Next week."*
- **Overfitting.** Week 33. Do not use the word.
- **Multiple features.** Today is one feature, one line. The iris demo at the end has three features and prints no coefficients on purpose — do not open that door.
- **Residual plots.** Worth doing, and Week 35 is where they earn their place.
- **Correlation vs causation as a new topic.** It was Week 27. Use the phrase "goes with" and move on; do not re-teach it.

---

## 🧰 Prep Checklist

### 20 minutes the night before

- [ ] **Print workbook pages 32.1–32.6.** Page 32.2 (the blank grid for the hand fit) should be printed **twice** — the first attempt at eyeballing a line is usually scrapped, and that is fine.
- [ ] **Find the graph paper and the millimetre ruler.** Both are in the year-0 box list. If there is no graph paper, print two 10×10 grids from any spreadsheet; if there is no ruler, the straight edge of a book works for drawing but you cannot read millimetres off it, so beg or borrow.
- [ ] **Do the hand fit yourself, on graph paper.** Twelve minutes, and it is the most valuable prep in the week. Axes: hours 0–7 across, marks 40–80 up. Plot the six points from section 3. Lay the ruler through them by eye. Draw. Then count squares to get the slope. **You should land somewhere between 3.0 and 4.2.** Write your number down; you will compare it with scikit-learn's 3.6 in class and it is much better if you have already felt how close eyeballing gets.
- [ ] **Run the code yourself.**

  ```
  cd ~/ai-academy/level2
  source .venv/bin/activate        # macOS / Linux
  .venv\Scripts\activate           # Windows PowerShell
  ```

  Type `week32_study_line.py` from section 5 and run it. You must see `slope: [3.6]`, `MAE: 2.67 marks`, `R2 : 0.804` and the 20-hour prediction of `[121.4]`. Those four numbers are your whole check.

- [ ] **Break it on purpose, twice.** First delete `.reshape(-1, 1)`:

  ```text
  ValueError: Expected 2D array, got 1D array instead:
  array=[1 2 3 4 5 6].
  ```

  Put it back. Then add `from sklearn.metrics import accuracy_score` and try `accuracy_score(marks, guesses)`:

  ```text
  ValueError: Classification metrics can't handle a mix of multiclass and continuous targets
  ```

  Remove it. You will stage both of these live, and both are much calmer the second time you see them.

- [ ] **Run the iris four-lines script** from section 4 (the full file is in the Answer Key, page 32.6). It takes one run and gives you the R²-can-mislead demonstration with real numbers on your own screen.

### 5 minutes on the day

- [ ] Graph paper, ruler, sharp pencil, **eraser**, calculator on the table. Laptop **closed**.
- [ ] Terminal open behind the closed laptop lid, environment activated, `(.venv)` showing.
- [ ] Last week's `export_text` printout somewhere visible — you will point at it in the Concept segment.
- [ ] Bug Log open at a clean page.

### Fallback if something fails

| If this fails | Do this instead |
|---|---|
| **No graph paper** | Draw a 7 × 8 grid on plain paper with the ruler. It takes three minutes and works completely. Do not skip the hand fit — it is the lesson. |
| **No laptop today** | This is the most laptop-optional week in the term. Pages 32.2 and 32.3 are entirely by hand, and they deliver objectives 1, 3 and 4 in full. Print the output block from section 5 so the student can compare their hand slope with 3.6. Objectives 2 and 5 wait one session. |
| **`ModuleNotFoundError: No module named 'sklearn'`** | Almost always the virtual environment. Look for `(.venv)` in the prompt; if it is missing, re-run the activate line. Section 4 of the orientation has the full table. |
| **The student's slope is nowhere near 3.6** | Check three things, in order: are the axes the right way round (hours across, marks up)? Is the line drawn through the *middle* of the dots rather than through the first and last? Did they count squares, or estimate? A hand slope between 3.0 and 4.2 is a success; outside that, one of those three is wrong. |
| **`49.400000000000006` derails the lesson** | Do not explain binary. Say: *"Computers store decimals slightly imperfectly — that's the crumb. Week 3's `round` fixes it."* Then use the tidied-up line and move on. |
| **Everything is done and there are 20 minutes left** | Differentiation "flying" item 1: run the same code on the pizza-delivery numbers on page 32.5, and have them state that slope in minutes per pizza. Same skill, different units, ten minutes. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — I'll guess your number | 7 | 7 | Being wrong by 2 and wrong by 40 are different kinds of wrong |
| 🧠 Concept — regression, slope, intercept | 16 | 23 | Name it; the ruler analogy; the slope-with-units sentence |
| 💻 Live-Code Together — fit the line, score it | 18 | 41 | `LinearRegression`; two staged bugs; MAE and R²; the 20-hour prediction |
| 🎲 Their Turn — the graph-paper fit | 20 | 61 | Plot, eyeball, draw, count squares, compare, compute MAE |
| 🔑 Wrap & Assign | 9 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — I'll guess your number (7 minutes)

**Do this:** Laptop closed. Nothing on the table but paper and a pencil.

**Say this:**

> "Last week I asked you which species a flower was. Three choices, and I was either right or I was wrong. Simple scoring.
>
> Now I'm going to ask you something different. **How many minutes did you spend on a screen yesterday?** Don't tell me. Write it down and cover it.
>
> Right. I'm going to guess. I say… **90 minutes.**
>
> Now show me. How far off was I?"

Whatever it is, get the actual gap out loud. Then:

> "So I was off by, what, twenty minutes? Was I *wrong*?
>
> Here's the thing. If you'd asked me 'which species is this flower' and I'd said the wrong one, I'd be wrong. Flat wrong. No credit. But 'off by twenty minutes' isn't the same kind of wrong at all, is it? If I'd said **four hundred** minutes, I'd also be 'wrong' — and it would be a much, much worse guess.
>
> So last week's score doesn't work any more. 'What fraction did I get exactly right' is going to be **zero** for ever, because I'm never going to guess your screen time to the exact minute.
>
> The question changed, so the score has to change too. And the new score is going to be a number in **minutes** — because the only honest way to say how wrong I was is in the units of the thing itself."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Was my 90-minute guess right or wrong?" | Neither, really — it was *close*, off by a certain amount. | If they say flatly "wrong", press: "Would 400 have been equally wrong?" That opens it. |
| "Give me a question where the answer is a number, not a category." | Tomorrow's temperature, a house price, how long a bus takes, next month's electricity bill. | If they give a category ("which team wins"), accept it and ask for the number version: "by how many runs?" |
| "Give me one where it's definitely a category." | Spam or not spam, which species, pass or fail, which language. | If they are stuck, offer the flower and ask them for a second. |
| "If I can never be exactly right, what should the score measure?" | How far off I usually am. | If they say "how close as a percentage", that is a decent instinct — say "hold that, we'll do a percentage-ish one too, and it's the sneakier of the two." |

---

### 🧠 Concept — regression, slope, intercept (16 minutes)

**Do this:** Write the six classmates' numbers where both of you can see them. Keep last week's `export_text` printout on the table.

**Say this — part 1, the name and the sorting question:**

> "The word for this is **regression** — predicting a number on a sliding scale, instead of picking from a list. It's a rotten name and there's no clue in it; just take it as a label.
>
> But the *question* behind it is the most useful sorting question in the whole subject, and it's this: **look at the answer column. Is it a short fixed list, or is it any number?**
>
> Short fixed list — setosa, versicolor, virginica — that's **classification**. Any number — marks, minutes, rupees — that's **regression**.
>
> Same table. Same code, almost. You cover up a different column and it becomes a different kind of problem.
>
> And here's the practical bit that'll save you next week: scikit-learn names its tools after this. Anything ending in `Classifier` picks from a list. Anything ending in `Regressor` gives you a number. Last week you used `DecisionTreeClassifier`. There is a `DecisionTreeRegressor` and it does exactly what you'd think."

**Say this — part 2, the ruler:**

> "Six people in a class. I know how many hours a week each one revised, and what they got in the test. Read them out."

Read the six pairs aloud together. Then:

> "Now — if I plot those as six dots, hours across and marks up, and you had to draw *one straight line* that came as close as possible to all six dots at once… you'd get a ruler out. Wouldn't you.
>
> That's the model. Not a metaphor. **The ruler is the model.** Two numbers describe it completely:
>
> **How steep it is** — that's the **slope**. How many marks you go up for one extra hour across.
>
> **Where it starts** — that's the **intercept**. What the line says at zero hours.
>
> That's the whole thing. Two numbers. Compare that with last week: the tree gave you four sentences. This gives you two numbers. Both are readable. Neither is magic."

**Say this — part 3, the sentence of the week:**

> "Now the most important habit of the term, and it's about how you *say* the slope.
>
> If the slope comes out at 3.6, you never — ever — say 'the slope is 3.6'. Because 3.6 what? Per what?
>
> You say: **'each extra hour of revision a week goes with about three point six more marks.'**
>
> Unit on the number. Unit on the 'per'. And notice I said **goes with**, not **causes**. Remember Week 27? These six people who revised more happened to score more. That's not the same as proving that revising *makes* you score more — maybe the ones who were confident already both revised more *and* scored more. **'Goes with' is a claim I can defend. 'Causes' is a claim I can't.**"

Write both versions on the paper and cross one out:

```
   ✗  "the slope is 3.6"
   ✗  "one hour of revision causes 3.6 marks"
   ✓  "one extra hour a week goes with about 3.6 more marks"
```

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "'How many goals will this player score next season?' — which is it?" | Regression. The answer is a number. | If they say classification, ask what the answer column would look like: 12, 7, 23 — not a short list. |
| "'Will this email go to my spam folder?' — which?" | Classification. Two choices. | If they hesitate, ask them to write the answer column: spam, spam, ham, spam. A short fixed list. |
| "The slope is 3.6. Say it as a sentence." | "One extra hour a week goes with about 3.6 more marks." | If they say "3.6 marks", prompt: "3.6 marks per *what*?" Keep prompting until the "per" arrives. It is the whole habit. |
| "What does the intercept 49.4 mean?" | What the line predicts for zero hours of revision. | If they say "the lowest mark", correct it: the lowest actual mark was 48. The intercept is what the *formula* says at zero, and nobody in our data revised zero. |
| "Could the slope ever be negative?" | Yes — "each extra kilometre from school goes with 2 lakh *less* on the house price." | This is a good one to ask. A negative slope is a downhill line, and the sentence still works with "less" instead of "more". |

---

### 💻 Live-Code Together — fit the line, score it (18 minutes)

**You type, the student types. Nobody pastes.** Both bugs are staged.

**Step 1 (3 min) — the data, and 🐞 STAGED MISTAKE ONE.**

Open a new file, `week32_study_line.py`. Type:

```python
import numpy as np
from sklearn.linear_model import LinearRegression

hours = np.array([1, 2, 3, 4, 5, 6])
marks = np.array([48, 60, 63, 65, 68, 68])

model = LinearRegression()
model.fit(hours, marks)
print("slope:", model.coef_)
```

Run it:

```text
Traceback (most recent call last):
  File "week32_study_line.py", line 8, in <module>
    model.fit(hours, marks)
  ...
ValueError: Expected 2D array, got 1D array instead:
array=[1 2 3 4 5 6].
Reshape your data either using array.reshape(-1, 1) if your data has a single feature or array.reshape(1, -1) if it contains a single sample.
```

**Say this:**

> "Read me the last two lines.
>
> `Expected 2D array, got 1D array.` Two-D means a table — rows *and* columns. One-D means a single row of numbers.
>
> scikit-learn always wants `X` as a **table**: one row per thing, one column per measurement. Even when there's only one measurement. It will not guess for you, because guessing wrong would be worse than complaining.
>
> And look — the error tells you the fix. It actually spells it out. `array.reshape(-1, 1)`. That is unusually kind of it, and it's worth noticing that error messages sometimes hand you the answer."

Fix it:

```python
hours = np.array([1, 2, 3, 4, 5, 6]).reshape(-1, 1)
```

Then add the shape check above the model, and make it a permanent habit:

```python
print("hours shape:", hours.shape)     # must be (6, 1)
print("marks shape:", marks.shape)     # (6,) is right for y
```

```text
hours shape: (6, 1)
marks shape: (6,)
slope: [3.6]
```

> "`(6, 1)` — six rows, one column. A table. And `marks` stays `(6,)` — a flat list of six. `X` is a table, `y` is a column. It looks lopsided and it's correct. **Print both shapes every single time from now on.** Two seconds, and it kills the most common error in this whole level."

**Step 2 (4 min) — the two numbers, and the sentence.** Add:

```python
print("intercept:", model.intercept_)
print("tidied up: marks =", round(model.coef_[0], 2), "x hours +",
      round(model.intercept_, 2))
```

```text
slope    : [3.6]
intercept: 49.400000000000006
tidied up: marks = 3.6 x hours + 49.4
```

**Say this:**

> "There's the model. `marks = 3.6 × hours + 49.4`. Two numbers.
>
> First — that `49.400000000000006`. Not a mistake, and not the model being sloppy. Computers store decimals in binary and 49.4 has no exact binary version, so a crumb is left at the fifteenth decimal place. Week 3's `round` sweeps it up. That's what the tidied-up line is for.
>
> Second, and much more important. **Say the slope as a sentence.** Go on."

Wait for it. Insist on the unit and the "per".

> "'Each extra hour of revision a week goes with about 3.6 more marks.' Write that sentence in your workbook now, because it's the thing I'm going to ask you for in three weeks' time."

**Step 3 (4 min) — the guesses and the misses.** Add:

```python
guesses = model.predict(hours)
print()
print("the line's guesses  :", guesses)
print("what really happened:", marks)
print("the misses          :", np.round(marks - guesses, 2))
```

```text
the line's guesses  : [53.  56.6 60.2 63.8 67.4 71. ]
what really happened: [48 60 63 65 68 68]
the misses          : [-5.   3.4  2.8  1.2  0.6 -3. ]
```

**Say this:**

> "Six guesses, six truths, six **misses**. A miss is just: what really happened, minus what the line said.
>
> Look at the first one. The line said 53, she actually got 48, so the miss is minus 5. Minus means she's **below** the line. And the second one is plus 3.4 — above the line.
>
> Now add up the six misses in your head. Roughly."

They will get about zero. Let them notice.

> "Zero. Exactly zero, in fact. And that's not a coincidence — a best-fit line always balances, with as much above as below. Which means **you can't just average the misses to see how wrong you are**, because they'd cancel out and you'd conclude you were perfect.
>
> So: throw the signs away. Just the sizes."

**Step 4 (4 min) — 🐞 STAGED MISTAKE TWO: the wrong score.** Say: *"Last week we used `accuracy_score`. Let's use it again."* Add:

```python
from sklearn.metrics import accuracy_score
print("accuracy:", accuracy_score(marks, guesses))
```

```text
Traceback (most recent call last):
  File "week32_study_line.py", line 20, in <module>
    print("accuracy:", accuracy_score(marks, guesses))
  ...
ValueError: Classification metrics can't handle a mix of multiclass and continuous targets
```

**Say this:**

> "Read the last line. `Classification metrics can't handle a mix of multiclass and continuous targets.`
>
> Unpack it. **Classification metrics** — accuracy is a category score. **Continuous targets** — our guesses are numbers with decimals in them, 56.6, 63.8. Accuracy would ask 'is 56.6 exactly equal to 60?' and the answer is no, so it would score that as a total failure — when actually 56.6 is a pretty good guess for 60.
>
> scikit-learn is refusing to give us a meaningless number. That's a kindness. Take that line out."

Delete it and put in the right scores:

```python
from sklearn.metrics import mean_absolute_error, r2_score
print()
print("MAE:", round(mean_absolute_error(marks, guesses), 2), "marks")
print("R2 :", round(r2_score(marks, guesses), 3))
```

```text
MAE: 2.67 marks
R2 : 0.804
```

**Say this:**

> "**MAE** — mean absolute error. Take the six misses, drop the signs, average them. 5.0 plus 3.4 plus 2.8 plus 1.2 plus 0.6 plus 3.0 is 16, divided by 6 is 2.67.
>
> And now say what it *means*, out loud, in marks: **'on average, my line is off by about two and a half marks.'** That's it. That's the sentence you'd say to your mum. No jargon, real units. **MAE is the score for humans.**
>
> **R² — 0.804.** Different animal. R² asks: how much better am I than the laziest possible model — the one that ignores revision hours completely and just guesses the class average every time?
>
> Guessing the average would be off by about 5.3 marks. My line is off by 2.67. So I'm meaningfully better. R² puts a number on 'meaningfully': 0.804, where 1.0 is perfect and 0.0 is 'no better than guessing the average'.
>
> **And R² has no units at all.** That makes it good for comparing two models and useless for telling anybody what your predictions are worth. So: **MAE for people, R² for comparing.**"

> **⚠️ Watch out:** if the student says "so it's 80% accurate", stop and fix it now. R² is not a percentage of right answers — *none* of our six was exactly right. The number that says how good the predictions are is MAE: 2.67 marks.

**Step 5 (3 min) — the moment they will remember.** Add:

```python
print()
print("a 7th classmate who revises 7 hours:", model.predict([[7]]))
print("somebody who revises 20 hours      :", model.predict([[20]]))
```

```text
a 7th classmate who revises 7 hours: [74.6]
somebody who revises 20 hours      : [121.4]
```

**Say this — and let the silence sit:**

> "Seven hours, 74.6 marks. Fine. A bit past our data but sensible.
>
> Twenty hours… **a hundred and twenty-one point four.**
>
> Out of a hundred.
>
> The line doesn't know the test is out of 100. It has never heard of a maximum mark. It just does 3.6 times 20 plus 49.4 and hands it over, absolutely confidently. Push it further — 50 hours — and it'll promise you 229.
>
> That's called **extrapolation**: predicting outside the range you actually have data for. Nobody in our six revised more than 6 hours, so past 6 the line is making a promise the data never made.
>
> This isn't a bug you fix. It's a limit you *know* — and saying it out loud is part of being honest about a model. When you show somebody a model, tell them the range it was built from."

Note the double brackets in `predict([[7]])` — outer for the table, inner for the one row. If they type `predict([7])` they get the 2D-array error from Step 1 again, which is a good thing to happen.

---

### 🎲 Their Turn — the graph-paper fit (20 minutes)

Full instructions in the Activity section. In the lesson flow:

- **Minutes 0–6:** page 32.2 — draw axes and plot the six points.
- **Minutes 6–11:** lay the ruler, draw the line, count squares, write your own slope.
- **Minutes 11–16:** page 32.3 — the deviation table by hand: means, the two sums, slope, intercept. Compare all three slopes: yours by eye, yours by arithmetic, scikit-learn's.
- **Minutes 16–20:** measure the six misses off the paper with the ruler and compute MAE by hand. State it in marks.

---

### 🔑 Wrap & Assign (9 minutes)

**Say this:**

> "Three things.
>
> **One.** Look at the answer column. Short fixed list, that's classification. Any number, that's regression. It's the first question you ask about any table, from now until Week 36.
>
> **Two.** A slope is never just a number. It's a sentence with two units in it: **'each extra hour a week goes with about 3.6 more marks.'** If you can't say it that way, you haven't finished reading the model.
>
> **Three.** MAE is in marks, so you can say it to anybody: **'off by about two and a half marks.'** R² has no units, so it's for comparing models and it can flatter you. Print them both, and always put the units on the MAE."

Run the three checks in **Assessing Understanding**, then set the homework. Both of today's tracebacks go into the Bug Log before the laptop closes.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `ValueError: Expected 2D array, got 1D array instead:` `array=[1 2 3 4 5 6].` | `fit` wants `X` as a table, and got a flat row. | `.reshape(-1, 1)` is missing from the `hours` line. | `np.array([...]).reshape(-1, 1)`. The error itself spells out the fix — read all of it. |
| `ValueError: Classification metrics can't handle a mix of multiclass and continuous targets` | You used a category score on number predictions. | `accuracy_score` on a regression. | Use `mean_absolute_error` and `r2_score`. Accuracy is for categories only, and this refusal is scikit-learn protecting you. |
| `AttributeError: 'LinearRegression' object has no attribute 'coef'. Did you mean: 'coef_'?` | Nearly the right name. | Missing the trailing underscore. | `model.coef_`. The underscore means "only exists after `fit`". Python names the fix for you. |
| `ImportError: cannot import name 'LinearRegresssion' from 'sklearn.linear_model'` | The department is right, the tool name is not. | Spelling — three `s`s in `Regresssion`. | `LinearRegression`. Compare the name in the error with the name in your file, character by character. |
| `NameError: name 'mean_absolute_error' is not defined` | You used a name Python was never given. | The `from sklearn.metrics import ...` line is missing, or does not list it. | `from sklearn.metrics import mean_absolute_error, r2_score` |
| `ValueError: Expected 2D array, got scalar array instead:` `array=7.` | `predict` wants a table of rows, and got a bare number. | `model.predict(7)`. | `model.predict([[7]])` — outer brackets are the table, inner brackets are the one row. |
| `TypeError: missing a required argument: 'y_pred'` | A scoring function needs two lists and got one. | `r2_score(marks)` — the guesses were left out. | `r2_score(marks, guesses)`. Truth first, guesses second. |
| `ValueError: Found input variables with inconsistent numbers of samples: [6, 5]` | `X` and `y` are different lengths. | A number was dropped from `marks` while typing. | Count them. Six hours needs six marks. |
| `AttributeError: 'numpy.ndarray' object has no attribute '_validate_params'` | You called `fit` on the recipe instead of on a made thing. | `LinearRegression.fit(...)` — the `()` after the name is missing. | `LinearRegression().fit(...)`, or `model = LinearRegression()` then `model.fit(...)`. |

### How to teach debugging without giving the answer

1. **"Read me the last line, out loud."** Not the wall of red. The last line names the problem in English.
2. **"Does the message tell you the fix?"** This week, twice, it literally does — the 2D-array error prints `array.reshape(-1, 1)` for you. Students skip that because the block looks like noise. Teaching them to *finish reading* is half of debugging.
3. **"What's different between the name in the error and the name in your file?"** Solves `NameError`, `AttributeError` and `ImportError` most of the time — and they solve it, which is the point.

> **🐞 If you see this error:** a `ValueError` mentioning **shapes** or **samples** is nearly always about the table being the wrong shape, not about your maths. Print `X.shape` and `y.shape` before you change anything else.

---

## 🎲 The Activity, In Full

### Setup

**On the table:** graph paper (5 mm squares), a millimetre ruler, a sharp pencil, an eraser, a calculator, workbook pages 32.2 and 32.3. **The laptop is closed.**

The six classmates, which the student copies onto page 32.2 themselves:

| Classmate | hours revised per week | marks out of 100 |
|---|---|---|
| A | 1 | 48 |
| B | 2 | 60 |
| C | 3 | 63 |
| D | 4 | 65 |
| E | 5 | 68 |
| F | 6 | 68 |

### The rules

1. **The ruler goes before the keyboard.** Their own slope gets written down before scikit-learn is allowed to speak.
2. **The slope must be read by counting squares**, not estimated. Pick two points *on the line* — not two data points — that sit on grid crossings, count the squares up, count the squares across, divide.
3. **Every number gets a unit.** "3.5" is not an answer. "3.5 marks per hour" is.
4. **No rubbing out the first line.** If they redraw, they draw the second line in a different way (dashed) and keep both. Two attempts on the page is a better record than one tidy one.

### Step 1 — axes and points (6 minutes)

Across the bottom: **hours, 0 to 7**, one big square per hour. Up the side: **marks, 40 to 80**, one big square per 5 marks.

> **💡 Try this:** have them label the axes *before* plotting anything, including the units — "hours of revision per week" and "marks out of 100". Week 25's rule holds: a chart with no axis labels is a decoration.

Plot the six points as small crosses, not blobs. A blob is 2 mm of uncertainty they do not need.

### Step 2 — lay the ruler (5 minutes)

**Say this:**

> "Put the ruler on the paper and move it around until it looks as close as it can get to *all six* crosses at once. Not through the first and last — through the *middle* of the cloud. Some crosses above, some below. When you can't make it better, draw along it, edge to edge."

The most common mistake by a mile is joining the first and last points. If you see that, ask: *"How many crosses are above your line? How many below?"* Joining A to F puts four points above the line and none below, and asking the question is enough for them to see it.

### Step 3 — read the slope by counting squares (5 minutes)

Pick two grid crossings the drawn line passes through, as far apart as possible. Count squares up, count squares across, and divide — remembering that one square up is **5 marks** and one square across is **1 hour**.

A good hand fit through these six points lands the slope somewhere between **3.0 and 4.2**. scikit-learn's answer is **3.6**. Anything in that band is a success, and you should say so warmly, because the point being made is *"eyeballing gets you close"*, not *"you got it exactly"*.

Have them write, in words, on the paper:

```
   my slope:  about ____ marks per extra hour of revision
```

### Step 4 — the arithmetic version (5 minutes, page 32.3)

Now the deviation table from section 3. They fill in `dx`, `dy`, `dx × dy` and `dx²`, total the last two columns, and divide:

```
slope     = 63.0 ÷ 17.5 = 3.6
intercept = 62 − 3.6 × 3.5 = 49.4
```

Then the comparison, all three on one line of the page:

| | slope |
|---|---|
| my ruler, by eye | *(their number, 3.0–4.2)* |
| my arithmetic | 3.6 |
| scikit-learn | 3.6 |

**Say this:**

> "Your eye got within a few tenths of the answer that took a page of arithmetic and a computer. That's not a coincidence and it's not luck. **You already knew how to do this** — the computer is faster and more consistent, and it is doing the same job."

### Step 5 — MAE off the paper (4 minutes)

Measure each of the six vertical gaps with the ruler, in marks, using the drawn line. Write the six sizes, no signs. Add. Divide by 6. Then the sentence:

```
   my MAE:  about ____ marks.
   Which means: "on average my line is off by about ____ marks."
```

Against the exact line, the six sizes are 5.0, 3.4, 2.8, 1.2, 0.6 and 3.0, totalling 16.0, giving **2.67 marks**. Off a hand-drawn line they will get something between about 2.3 and 3.2. That is right.

### What "finished" looks like

- Axes labelled with units; six crosses plotted.
- One drawn line through the middle of the cloud, with points above *and* below it.
- A slope read by counting squares, written **with both units**.
- The deviation table completed and totalled: 63.0 and 17.5.
- Three slopes compared in one small table.
- An MAE written as a sentence in marks.

![Lay a ruler through the dots](../figures/fig-w32-2-line-through-a-scatter.svg)
*Figure 32.5 — What a finished sheet looks like. The step triangle is how you read the slope: one across, 3.6 up.*

### Variation — easier

- **Give the axes pre-drawn and pre-labelled** on the printed page. Plotting six crosses on somebody else's axes is still the whole activity.
- **Cut Step 4 entirely.** The deviation table is the hardest arithmetic in the week and it is the *least* important part. Eyeball the line, count the squares, say the slope with units. That is objectives 1, 3 and 4.
- **Use three points instead of six** — A, C and F (1/48, 3/63, 6/68). The line is easier to see and the MAE is three numbers instead of six.
- **Do the MAE together, out loud**, with the student only writing the total. The measuring is the skill; the recording is not.
- **Do not print the 20-hour prediction as an exercise.** Just show it. It is a story to hear, not a task to do.

### Variation — harder

1. **A second dataset, different units.** Page 32.5's pizza numbers: pizzas in an order against delivery minutes. Slope **2.55 minutes per extra pizza**, intercept 10.7 minutes, MAE 0.48 minutes, R² 0.9927. The whole point is stating a slope in *minutes per pizza* — the skill transfers, the units do not.
2. **Find where the line stops making sense.** *"Solve `3.6 × hours + 49.4 = 100`. What does your answer mean?"* It comes out at about 14.1 hours, and it means the line claims a perfect score at 14 hours a week — and then keeps going past 100, which is impossible. Extrapolation, found by algebra rather than by being told.
3. **Break R² on purpose.** *"Invent six marks where the line has a small MAE and a terrible R²."* The trick is to make all six marks nearly identical (say 62, 62, 63, 62, 63, 62): there is almost nothing to explain, so however well the line does, R² is tiny. This is the deepest idea in the week and a student who finds it has genuinely understood R².
4. **Argue with the slope.** *"The slope says more revision goes with more marks. Give me a reason that could be true even if revision does nothing at all."* (Confident students revise more *and* score more; students who find the subject easy enjoy revising it; the ones who revised 6 hours may have been the ones who cared most about the result.) This is Week 27, put to work.

---

## ❓ Questions Students Ask This Week

**"Why doesn't the line go through the dots?"**

Because the dots are not on a line. Six real people are never on a line — there is always something else going on, sleep, mood, whether they happened to revise the right chapter. The line's job is not to touch the dots; it is to be as close to all of them at once as one straight line can be. The misses are the honest record of that job. And a model that hit every single training point exactly would be a reason to worry, not to celebrate — which is a sentence you will understand completely in about a week.

**"Is 0.804 good?"**

It is good *for six people and one measurement*, and that is as far as the sentence goes. R² on its own can never answer "is this good", because good depends on what you are going to do with it. If you are guessing marks for fun, off by 2.67 marks is great. If a scholarship depended on it, off by 2.67 marks would be unacceptable and you would need to go and find better features. Always ask "good enough for what?" before answering "good?".

**"Which is the real score, MAE or R²?"**

Both are real; they answer different questions. MAE answers *"how far off am I, typically?"* and comes with units, so it is the one you say to a person. R² answers *"how much better am I than not bothering?"* and has no units, so it is the one you use to compare two models on the same data. Report both. It costs nothing and it makes it much harder for anybody — including you — to be fooled.

**"Can the slope be negative?"**

Yes, and it happens constantly. "Each extra kilometre from the school goes with about 2 lakh less on the house price." The line goes downhill, the slope is a negative number, and the sentence works identically with "less" instead of "more". Watch out for one thing: reading a negative slope as "the model is bad". A negative slope is a real relationship, just a downhill one.

**"What if I use two features instead of one?"**

Then you get one slope per feature, and each one reads the same way: *"holding everything else the same, one more unit of this goes with this much more."* scikit-learn puts them all in `model.coef_`, in the same order as your columns. One warning that will save you later: **you cannot rank features by the size of their slopes**, because a slope depends on its units. A slope of 0.088 per square metre and 2.99 per bedroom does not mean bedrooms matter 34 times more; square metres range over 150 units and bedrooms over 3.

**"The line predicted 121 marks out of 100. Isn't that just broken?"**

It is doing exactly what it was built to do, which is the interesting part. A straight line has no concept of a maximum, a minimum, or reality. It was fitted on people who revised between 1 and 6 hours, and past 6 hours it is guessing with total confidence and no evidence. The professional habit is to write down the range your model was built from and refuse to answer outside it. "Nobody in my data revised more than 6 hours, so I won't predict past 6" is a completely respectable thing to say.

**"Why does it square the misses instead of just adding up their sizes?"** *(Answer this one honestly: nobody fully agrees.)*

**This one is genuinely argued about, and the disagreement is real rather than a hole in your knowledge.** Squaring makes one big miss hurt far more than several small ones, so a line fitted by squares works hard to avoid disasters and tolerates lots of little errors. Fitting by the plain sizes instead — which is a real method — gives you a line that ignores a single wild outlier and tracks the ordinary cases better. Which one is *right* depends entirely on what a big miss costs you. If you are predicting the dose of a medicine, one enormous mistake is catastrophic and you want the squares. If you are estimating a weekly shopping bill, one weird week when there was a party should not drag your whole model sideways, and you want the plain sizes. There are also two duller reasons squares won historically: the arithmetic comes out to a neat formula with squares and does not without, and squares were what people could compute by hand in 1805. Statisticians have argued about this for two centuries and the honest position is that it is a choice about consequences, not a fact about mathematics. What everybody agrees on is that you should *know* which one you used and *say* so.

**"Could a tree do this instead of a line?"**

Yes. A tree can predict a number too — the leaves hold an average instead of a species name — and it draws flat steps rather than a smooth slope. That means a tree handles a sudden threshold ("anything within 1.5 km of the school costs more") beautifully and a smooth trend badly, and a line is the exact opposite. Next week you put both of them on the same data and score them side by side.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| The laptop opens first and the graph paper never comes out | Typing feels like progress and drawing feels like a warm-up | Close the lid. The hand fit is not an illustration of the lesson, it *is* the lesson: the student has to find out that their own eye gets within a few tenths of 3.6. That cannot be told, only done. |
| The hand line joins the first and last point | It is the obvious thing to do with a ruler and two dots | Ask, do not tell: *"How many crosses are above your line? How many below?"* Four above and none below answers itself. |
| The slope is reported as "3.6" and the sentence never arrives | A number feels like a finished answer | Every single time, reply with the same four words: **"3.6 what, per what?"** Do it until the units come out unprompted. This is the habit of the week and repetition is the only way in. |
| R² 0.804 gets read as "80% accurate" | The numbers look like percentages | Fix it on the spot: *"80% of what? None of our six predictions was exactly right."* Then point at MAE: 2.67 marks is the number that says how good the predictions are. |
| `49.400000000000006` triggers a twenty-minute detour about binary | It looks like a serious bug | One sentence: *"Computers store decimals slightly imperfectly; that's the crumb. `round` sweeps it up."* Then move on. Do not teach floating point today. |
| The 2D-array error is fixed by trial and error without being read | The traceback looks like noise | Make them read the *whole* block out loud. The fix is printed inside it. A student who learns that error messages sometimes hand you the answer has gained more than a working line of code. |
| "Causes" creeps into the slope sentence | It is the natural way to say it in English | Correct it every time, briefly: *"goes with"*. Then once, properly: give them the alternative explanation (confident students revise more *and* score more) and let them feel that the data cannot tell the two apart. |
| The 121.4 marks result is treated as an error to be fixed | Anything absurd looks like a bug | It is the model working correctly outside its evidence. Ask: *"What's the biggest number of hours anybody in our data revised?"* Six. *"So what is the line doing at twenty?"* Making it up, confidently. |
| The intercept becomes "the mark you get for no revision" | It is the obvious reading, and it is nearly right | Ask who in the data revised zero hours. Nobody — the minimum is 1. The intercept is machinery, not a measured fact. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** the deviation table (page 32.3), R², and the iris four-lines demonstration. Keep the graph paper, the drawn line, the slope in units, and MAE in marks. That is objectives 1, 3 and 4, and it is a complete, honest lesson.

**Reteach — make the misses physical.** The sticking point is almost always *why we throw away the signs*. Do it with objects. Six paper strips, cut to the length of each miss (5 marks = 5 cm, 3.4 marks = 3.4 cm, and so on). Lay them end to end on the table: 16 cm of total wrongness. Divide the row into six equal parts. That is MAE, and it is now something you can point at. Then take two strips, one "above the line" and one "below", and ask whether they cancel out in real life. They do not — being 5 marks over and 5 marks under is *two* mistakes, not zero mistakes.

**A copy-this-exactly scaffold.** If the typing is defeating them, this is the smallest complete file that still delivers the week. Every line, exactly as printed:

```python
# week32_small.py
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

hours = np.array([1, 2, 3, 4, 5, 6]).reshape(-1, 1)
marks = np.array([48, 60, 63, 65, 68, 68])

model = LinearRegression()
model.fit(hours, marks)

print("slope    :", round(model.coef_[0], 2), "marks per hour")
print("intercept:", round(model.intercept_, 2), "marks")
print("MAE      :", round(mean_absolute_error(marks, model.predict(hours)), 2), "marks")
```

```text
slope    : 3.6 marks per hour
intercept: 49.4 marks
MAE      : 2.67 marks
```

Twelve lines, three numbers, every one already carrying its unit in the printout. Then the only task is to say the slope as a sentence.

**One thing you must not cut:** the slope stated in real units. If the whole week collapses to one sentence, make it *"each extra hour a week goes with about 3.6 more marks."*

### If the student is flying

None of these need syntax they do not already have.

1. **Same code, different units** (Variation — harder, item 1). The pizza numbers on page 32.5. Slope 2.55 **minutes per pizza**, MAE 0.48 minutes, R² 0.9927. The transfer is the point.
2. **The four iris lines.** Run the script from the Answer Key (page 32.6) and stare at the first two rows: identical MAE, R² of 0.852 and 0.393. Then the question: *"Same MAE. Why is one R² twice the other?"* A student who works out that R² compares you against guessing the average has understood the hardest idea in the week.
3. **Break R² on purpose** (item 3). Invent six marks with a tiny MAE and a terrible R². This is the same insight as item 2, arrived at from the other side, and it is the best possible evidence that they own it.
4. **Solve for the impossible** (item 2). `3.6h + 49.4 = 100` gives h ≈ 14.1. Then: *"What does the line say about 20 hours? Is that a fact or a promise?"*
5. **Predict before you fit.** *"Before you run anything: what do you think the slope will be? Draw your guess as a line first."* A written wrong guess is worth more than a right one, and this week the guess is usually close, which is itself the lesson.

### If the student won't engage today

Do the Hook, then play one game, and stop.

> **"Which one? or how much?"** You name a question, they say classification or regression, best of twelve. Fast, out loud, no writing.
>
> Which language is this text in? *(classification)* · How many minutes until the bus? *(regression)* · Will it rain tomorrow? *(classification)* · How much rain tomorrow? *(regression)* · Is this email spam? *(classification)* · How many people will come to the party? *(regression)* · Which of my friends sent this message? *(classification)* · What will this house sell for? *(regression)* · Did the batter get out? *(classification)* · How many runs will she score? *(regression)* · Is this photo a cat or a dog? *(classification)* · How old is the dog in this photo? *(regression)*

Notice that the pairs come from the same situations — rain, buses, cricket — with the answer column swapped. Point that out at the end: *"Same world, same measurements. You changed which column you covered up, and it became a different kind of problem."*

That game delivers objective 1 completely and takes ten minutes with no equipment. The graph paper survives to next session and the six classmates are not going anywhere.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — sort the question (spoken)**

> "Three questions. For each one tell me classification or regression, and tell me *how you know*. One: which bus route is this? Two: how many minutes late will the bus be? Three: will the bus be late at all?"

*Good answer:* classification (a short list of routes) · regression (a number of minutes) · classification (yes or no). Full marks needs the reason — **"because the answer column is a number"** or **"because it's a short fixed list"** — not just the label. **What to catch:** a student who gets all three right by feel. Ask number 2 again and make them describe the answer column.

**Check 2 — say the slope (spoken)**

> "I fit a line to predict how much a taxi ride costs from how many kilometres it is. The slope comes out at 18. Say that as a full sentence."

*Good answer:* "Each extra kilometre goes with about 18 rupees more on the fare." Full marks needs **the unit of y**, **the unit of x**, and **'per one'**. **What to catch:** "the slope is 18 rupees" — half marks; prompt with "18 rupees per what?" And listen for "causes": if it appears, correct it warmly and move on.

**Check 3 — what MAE means (spoken)**

> "My model predicts test marks and its MAE is 4. What does that actually mean? And if I tell you my R² is 0.9, do you now know whether my predictions are any good?"

*Good answer:* "On average your predictions are off by about 4 marks." Then: "No — R² has no units, so it only tells me you're a lot better than guessing the average. The 4 marks is the number that says whether it's good enough." Full marks needs the units on the first half and the "no" on the second. **What to catch:** "R² 0.9 means it's 90% right." Point out that a high R² can sit next to a large MAE if the thing you are predicting varies enormously.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot sort a question into classification or regression. Reads a slope as a bare number. Thinks accuracy applies to numbers. |
| **2 — Emerging** | Sorts questions correctly when prompted. Draws a line by eye. Reports a slope without units, or with only one of the two. |
| **3 — Secure** | Fits the line in code, reads out `coef_` and `intercept_`, states the slope with both units and "per one", and says what MAE means in marks. **This is the target.** |
| **4 — Strong** | Explains R² as "how much better than guessing the average". Says why the misses cannot be averaged with their signs. Recognises the 20-hour prediction as extrapolation and says what range the model is entitled to. |
| **5 — Exceptional** | Explains how the same MAE can give very different R² values, and why. Says "goes with" rather than "causes" unprompted, and can offer an alternative explanation for the slope. Constructs a dataset with a small MAE and a low R² on purpose. |

---

## 📤 Homework to Assign

**Say this:**

> "Three pages, about an hour.
>
> **First, page 32.4 — hand versus machine.** Fit the line by hand through the six points on fresh graph paper, exactly like in class, and write down your own slope by counting squares. Then run the code and write scikit-learn's slope next to it. Then — the marks are here — **state the slope as a proper sentence with both units**: something like 'each extra hour of revision a week goes with about 3.6 more marks.' Not 'the slope is 3.6'. Say what, per what.
>
> **Second, page 32.5 — MAE in real units.** Compute the six misses, drop the signs, average them, and finish this sentence: 'on average my line is off by about ______ marks.' Then do the whole thing again for the pizza numbers on that page — pizzas in an order against delivery minutes — and state *that* slope in minutes per pizza. Same skill, different units. If you can do it twice, you can do it anywhere.
>
> **Third, page 32.6 — what the line can't explain.** Write down one thing that affects somebody's marks that is **not** on our chart, and say in one sentence why the line has no way to know about it. Then the Bug Log: both of today's errors, real message copied out, fix in your own words.
>
> One last thing, and I mean it. Before you run any code on page 32.4, **write down your hand slope and don't change it.** If the computer disagrees with you by a couple of tenths, that is a success, not a mistake, and I want to see the original number."

**Workbook pages:** 32.1, 32.2 and 32.3 in class; **32.4, 32.5, 32.6** at home.

**Expected time:** 20 min for the hand fit and the code · 25 min for MAE on both datasets · 15 min for the write-up and the Bug Log. About 60 minutes.

---

## 🔑 Answer Key

### Page 32.1 — Classification or regression?

| # | Question | Which | Why |
|---|---|---|---|
| (a) | Which species is this flower? | **Classification** | Three fixed choices. |
| (b) | How many marks will she get out of 100? | **Regression** | Any number on a scale. |
| (c) | Will this student pass? | **Classification** | Two choices, pass or fail. |
| (d) | How many minutes will the delivery take? | **Regression** | A number of minutes. |
| (e) | Which of my three friends sent this message? | **Classification** | A short fixed list of three. |
| (f) | What will this house sell for? | **Regression** | A price, any number. |
| (g) | How many runs will she score? | **Regression** | A count, any number. |
| (h) | Did she get out or not? | **Classification** | Two choices. |

**32.1(i) Two of the pairs above are the same situation asked two ways. Find them and say what changed.**
(c) and (b) are the same students — pass/fail versus the actual mark. (g) and (h) are the same batter — how many runs versus out or not. **Nothing about the world or the measurements changed. Only the column you cover up.** That is the entire distinction.

**32.1(j) Which scikit-learn tool would you reach for, for (b)?**
Something ending in `Regressor`, or `LinearRegression`. Anything ending in `Classifier` is for (a), (c), (e) and (h).

**32.1(k) What goes wrong if you use `accuracy_score` on (b)?**
It refuses to run:

```text
ValueError: Classification metrics can't handle a mix of multiclass and continuous targets
```

And that refusal is a kindness. If it *did* run, it would ask "is 63.9 exactly equal to 64?", answer no, and score an excellent prediction as a total failure.

### Page 32.2 — The hand fit

There is no single right answer for the drawn line, and that is deliberate. Mark four things:

| What to look for | Full credit |
|---|---|
| Axes labelled with units | "hours of revision per week" and "marks out of 100" both written |
| Points plotted | all six, as crosses, at (1,48) (2,60) (3,63) (4,65) (5,68) (6,68) |
| Line placed sensibly | some points above and some below; **not** joining A to F |
| Slope read by counting | a number between **3.0 and 4.2**, written with both units |

**32.2(a) How many of your points are above the line and how many below?**
Against the exact line: two above and… let us be precise. The misses are −5.0, +3.4, +2.8, +1.2, +0.6, −3.0, so **four above and two below**. A hand line should give something like 3-and-3 or 4-and-2. All six on one side means the line is in the wrong place.

**32.2(b) Why is joining the first and last point a bad way to fit a line?**
Because it uses two of your six pieces of evidence and throws four away. Joining (1,48) to (6,68) gives a slope of exactly 4.0, and it puts every one of the four middle points **above** the line — so the line is systematically too low for most of the class. A best-fit line has to answer to all six points.

**32.2(c) Your eye and the computer got nearly the same slope. What does that tell you about what the computer is doing?**
That it is doing the same job, not a different and mysterious one. It defines "as close as possible to all of them" precisely and consistently, and it does it in a thousandth of a second — but the job is the job you just did with a ruler.

### Page 32.3 — The deviation table by hand

**Step 1 — the means.**

```
x̄ = (1 + 2 + 3 + 4 + 5 + 6) ÷ 6 = 21 ÷ 6 = 3.5
ȳ = (48 + 60 + 63 + 65 + 68 + 68) ÷ 6 = 372 ÷ 6 = 62
```

**Step 2 — the table.**

| x | y | dx = x − 3.5 | dy = y − 62 | dx × dy | dx² |
|---|---|---|---|---|---|
| 1 | 48 | −2.5 | −14 | 35.0 | 6.25 |
| 2 | 60 | −1.5 | −2 | 3.0 | 2.25 |
| 3 | 63 | −0.5 | 1 | −0.5 | 0.25 |
| 4 | 65 | 0.5 | 3 | 1.5 | 0.25 |
| 5 | 68 | 1.5 | 6 | 9.0 | 2.25 |
| 6 | 68 | 2.5 | 6 | 15.0 | 6.25 |
| | | **Σ = 0** | **Σ = 0** | **Σ = 63.0** | **Σ = 17.5** |

Both `dx` and `dy` columns must total zero — that is the built-in check, and it catches a wrong mean instantly.

**Step 3 — slope and intercept.**

```
slope     = 63.0 ÷ 17.5 = 3.6
intercept = 62 − 3.6 × 3.5 = 62 − 12.6 = 49.4
```

**The model: marks = 3.6 × hours + 49.4**

**32.3(a) Why must the `dx` and `dy` columns each add to zero?**
Because a mean is the balance point: the amounts above it and the amounts below it are equal by definition. If either column does not total zero, the mean is wrong — go back before doing anything else.

**32.3(b) One row contributes a negative number to the `dx × dy` column. Which, and what does it mean?**
Row C (3 hours, 63 marks): `dx` is −0.5 and `dy` is +1, giving −0.5. It means that classmate is on the *low* side for hours but on the *high* side for marks — she pushes against the uphill trend. Every other row agrees with the trend, so every other product is positive.

**32.3(c) Compare your three slopes.**

| | slope |
|---|---|
| ruler, by eye | *their number, 3.0–4.2* |
| arithmetic | **3.6** |
| scikit-learn | **3.6** |

The arithmetic and scikit-learn must match exactly — they are the same calculation. The eye should be within a few tenths.

### Page 32.4 — Hand versus machine (homework)

The complete working file, actually run:

```python
# week32_study_line.py
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

hours = np.array([1, 2, 3, 4, 5, 6]).reshape(-1, 1)
marks = np.array([48, 60, 63, 65, 68, 68])

print("hours shape:", hours.shape)
print("marks shape:", marks.shape)

model = LinearRegression()
model.fit(hours, marks)

print("slope    :", model.coef_)
print("intercept:", model.intercept_)
print("tidied up: marks =", round(model.coef_[0], 2), "x hours +",
      round(model.intercept_, 2))

guesses = model.predict(hours)
print("guesses  :", guesses)
print("misses   :", np.round(marks - guesses, 2))
print("MAE      :", round(mean_absolute_error(marks, guesses), 2), "marks")
print("R2       :", round(r2_score(marks, guesses), 3))
print("7 hours  :", model.predict([[7]]))
print("20 hours :", model.predict([[20]]))
```

Real output:

```text
hours shape: (6, 1)
marks shape: (6,)
slope    : [3.6]
intercept: 49.400000000000006
tidied up: marks = 3.6 x hours + 49.4
guesses  : [53.  56.6 60.2 63.8 67.4 71. ]
misses   : [-5.   3.4  2.8  1.2  0.6 -3. ]
MAE      : 2.67 marks
R2       : 0.804
7 hours  : [74.6]
20 hours : [121.4]
```

**32.4(a) The slope, as a sentence.**

> *"Each extra hour of revision per week goes with about **3.6 more marks** out of 100."*

**Marking:** one mark for the number, one for the unit of y (marks), one for the unit of x (per hour per week), one for "goes with" rather than "causes". A sentence reading "the slope is 3.6" scores one out of four, however confidently it is written.

**32.4(b) The intercept, as a sentence — and the health warning.**

> *"The line says somebody who revised zero hours would score about 49.4 marks. But nobody in our six revised zero — the least was one hour — so that is the formula talking, not evidence. It is a prediction off the edge of what we measured."*

**32.4(c) Why is `intercept_` printed as `49.400000000000006`?**
Floating-point dust. Computers store decimals in binary and 49.4 has no exact binary form, so a crumb survives at the fifteenth decimal place. It is not the model being imprecise. `round(model.intercept_, 2)` sweeps it up.

**32.4(d) Why does `hours` need `.reshape(-1, 1)` when `marks` does not?**
`X` must be a **table** — rows × columns — because in general there are several features. `y` is a single column of answers, so a flat list is right. Hence `(6, 1)` and `(6,)`. Leaving the reshape out gives:

```text
ValueError: Expected 2D array, got 1D array instead:
array=[1 2 3 4 5 6].
```

**32.4(e) The line predicts 121.4 marks for 20 hours. Is this a bug?**
No. It is the line doing precisely what it was built to do, outside the evidence it was built from. Our data covers 1 to 6 hours; at 20 the line is extrapolating, and a straight line has no idea the test is out of 100. The professional move is to state the range the model was fitted on and refuse to answer outside it.

### Page 32.5 — MAE in real units (homework)

**Part 1 — the six classmates.**

| x | actual | predicted | miss | \|miss\| |
|---|---|---|---|---|
| 1 | 48 | 53.0 | −5.0 | 5.0 |
| 2 | 60 | 56.6 | +3.4 | 3.4 |
| 3 | 63 | 60.2 | +2.8 | 2.8 |
| 4 | 65 | 63.8 | +1.2 | 1.2 |
| 5 | 68 | 67.4 | +0.6 | 0.6 |
| 6 | 68 | 71.0 | −3.0 | 3.0 |
| | | | **Σ = 0.0** | **Σ = 16.0** |

```
MAE = 16.0 ÷ 6 = 2.6666... = 2.67 marks
```

> *"On average my line is off by about 2.67 marks — call it under 3 marks."*

**32.5(a) Why can't you just average the misses as they are?**
They add up to zero. A best-fit line always balances, with as much above as below, so averaging the signed misses would say the model is perfect no matter how bad it is. Dropping the signs is what makes the average mean something.

**32.5(b) What would MAE be for the laziest model — always guessing the class average of 62?**

| y | miss from 62 | \|miss\| |
|---|---|---|
| 48 | −14 | 14 |
| 60 | −2 | 2 |
| 63 | +1 | 1 |
| 65 | +3 | 3 |
| 68 | +6 | 6 |
| 68 | +6 | 6 |
| | | **Σ = 32** |

`32 ÷ 6 = 5.33 marks`. Our line's 2.67 is **half** as wrong as not bothering at all. Without that comparison, "MAE 2.67" is a number with nothing to lean on.

**Part 2 — the pizza numbers.**

| pizzas (x) | 2 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|
| minutes (y) | 16 | 20 | 27 | 31 | 36 |

By hand: `x̄ = 6`, `ȳ = 26`.

| x | y | dx | dy | dx·dy | dx² |
|---|---|---|---|---|---|
| 2 | 16 | −4 | −10 | 40 | 16 |
| 4 | 20 | −2 | −6 | 12 | 4 |
| 6 | 27 | 0 | 1 | 0 | 0 |
| 8 | 31 | 2 | 5 | 10 | 4 |
| 10 | 36 | 4 | 10 | 40 | 16 |
| | | | | **Σ = 102** | **Σ = 40** |

```
slope     = 102 ÷ 40 = 2.55
intercept = 26 − 2.55 × 6 = 26 − 15.3 = 10.7
```

**minutes = 2.55 × pizzas + 10.7**

| x | actual | predicted | miss | \|miss\| |
|---|---|---|---|---|
| 2 | 16 | 15.8 | +0.2 | 0.2 |
| 4 | 20 | 20.9 | −0.9 | 0.9 |
| 6 | 27 | 26.0 | +1.0 | 1.0 |
| 8 | 31 | 31.1 | −0.1 | 0.1 |
| 10 | 36 | 36.2 | −0.2 | 0.2 |
| | | | **Σ = 0.0** | **Σ = 2.4** |

```
MAE = 2.4 ÷ 5 = 0.48 minutes
R²  = 1 − (1.90 ÷ 262) = 0.992748
```

Confirmed in code:

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

pizzas = np.array([2, 4, 6, 8, 10]).reshape(-1, 1)
minutes = np.array([16, 20, 27, 31, 36])

model = LinearRegression().fit(pizzas, minutes)
guesses = model.predict(pizzas)
print("slope    :", round(model.coef_[0], 2), "minutes per pizza")
print("intercept:", round(model.intercept_, 2), "minutes")
print("guesses  :", np.round(guesses, 2))
print("MAE      :", round(mean_absolute_error(minutes, guesses), 2), "minutes")
print("R2       :", round(r2_score(minutes, guesses), 4))
print("7 pizzas :", model.predict([[7]]))
```

```text
slope    : 2.55 minutes per pizza
intercept: 10.7 minutes
guesses  : [15.8 20.9 26.  31.1 36.2]
MAE      : 0.48 minutes
R2       : 0.9927
7 pizzas : [28.55]
```

**32.5(c) The pizza slope, as a sentence.**

> *"Each extra pizza in the order goes with about **2.55 more minutes** of delivery time."*

**32.5(d) The pizza intercept means something sensible for once. What?**
10.7 minutes is the time an order of *zero* pizzas would take — which is roughly the driving and waiting time before any pizza is loaded. Unlike the revision intercept, this one has a real-world reading, because "the fixed part of the journey" genuinely exists. It is still an extrapolation (nobody ordered zero), so treat it as plausible rather than measured.

**32.5(e) A 7-pizza order?**
`2.55 × 7 + 10.7 = 17.85 + 10.7 = 28.55 minutes`. And this one is safe, because 7 sits *inside* the range we have data for (2 to 10). Predicting inside your range is called interpolation and it is far more defensible than the 20-hour revision prediction.

### Page 32.6 — What the line can't explain, and the Bug Log (homework)

**32.6(a) Name one thing that affects marks and is not on our chart.**

Any of these earns full credit provided the second sentence is there: how much sleep they had the night before · whether they revised the right chapter · whether they had a teacher who explained it well · how much they already knew before revising · whether they were ill on the day · how good they are at that particular subject · whether the questions happened to suit them.

The required second sentence is the reason:

> *"The line only has one column to look at — hours revised. It has no way even to represent sleep, because we never measured it. Anything we didn't put in the table simply does not exist as far as the model is concerned, and it turns up in the misses instead."*

**32.6(b) Our MAE is 2.67 marks. Where does that 2.67 come from?**
From everything about these six people that is not "hours revised". If revision were the only thing that mattered, all six would sit exactly on the line and the MAE would be zero. The size of the misses is a measure of how much else is going on — so the MAE is not just a score, it is a hint about the features you are missing.

**32.6(c) The R² is 0.804. Does that mean the model is good enough to use?**
Not on its own, and this is the honest answer. R² 0.804 says the line explains about 80% of the up-and-down in these six marks — much better than guessing the average. It says nothing about whether being off by 2.67 marks is acceptable, and that depends entirely on the decision. For a rough guess, fine. For anything that mattered to somebody, no. **Always print the MAE next to the R², with its units.**

**32.6(d) The four iris lines.** The complete file, actually run:

```python
# week32_iris_lines.py
# Hide one flower measurement. Try to predict it from the other three.

import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

iris = load_iris()
print("the four measurements:", iris.feature_names)
print()
print(f"{'measurement we hid':20s} {'MAE (cm)':>9s} {'R2':>7s} {'mean-guess MAE':>15s}")

for hidden in range(4):                              # try each column in turn
    others = [c for c in range(4) if c != hidden]     # the three columns left
    X = iris.data[:, others]                          # what we may look at
    y = iris.data[:, hidden]                          # what we must guess

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)         # no stratify: it's a number

    model = LinearRegression()
    model.fit(X_train, y_train)
    guesses = model.predict(X_test)

    mae = mean_absolute_error(y_test, guesses)
    r2 = r2_score(y_test, guesses)

    # the laziest model there is: ignore the features, always say the mean
    lazy = np.zeros(len(y_test)) + y_train.mean()
    lazy_mae = mean_absolute_error(y_test, lazy)

    print(f"{iris.feature_names[hidden]:20s} {mae:9.3f} {r2:7.3f} {lazy_mae:15.3f}")
```

```text
the four measurements: ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']

measurement we hid    MAE (cm)      R2  mean-guess MAE
sepal length (cm)        0.234   0.852           0.699
sepal width (cm)         0.235   0.393           0.295
petal length (cm)        0.261   0.960           1.643
petal width (cm)         0.159   0.927           0.708
```

**The answer, in full:**

> Rows one and two have almost the same MAE — 0.234 cm and 0.235 cm — and R² values that are miles apart: 0.852 and 0.393. So R² is clearly not measuring "how far off am I".
>
> The last column explains it. For sepal length, guessing the average is off by 0.699 cm and the line gets that down to 0.234 — a huge improvement, so R² is high. For sepal width, guessing the average is *already* only off by 0.295 cm, because sepal width barely varies between flowers. Getting from 0.295 to 0.235 is a small win, and R² says so.
>
> **R² is not a measure of how good you are. It is a measure of how much better you are than guessing the average.** So a low R² can mean "the thing hardly varies, there was little to explain", and a high R² can sit next to a large MAE if the thing varies enormously. Report both, and put the units on the MAE.
>
> And the wider point: three of these four are over 0.85 and one is under 0.4, from one dataset with one piece of code. A straight line is not a universal answer.

**The two Bug Log entries:**

| Message | What it means | The fix |
|---|---|---|
| `ValueError: Expected 2D array, got 1D array instead: array=[1 2 3 4 5 6].` | `fit` wants `X` as a table with rows and columns, and I gave it one flat row. | Add `.reshape(-1, 1)` to the `hours` line. The error message actually prints the fix. Print `X.shape` and check it says `(6, 1)`. |
| `ValueError: Classification metrics can't handle a mix of multiclass and continuous targets` | I used `accuracy_score`, which is for categories, on predictions that are numbers with decimals. | Use `mean_absolute_error` and `r2_score` instead. Accuracy asks "exactly equal?", which is the wrong question for a number. |

### Lesson questions posed in the Say-this scripts

- *"Was my 90-minute guess right or wrong?"* → Neither. It was off by an amount, and 400 would have been off by much more. That is why accuracy cannot score a number.
- *"Give me a question whose answer is a number."* → Tomorrow's temperature, a house price, minutes until the bus, next month's bill.
- *"'How many goals next season?' — which is it?"* → Regression. The answer column would read 12, 7, 23 — not a short list.
- *"'Will this email go to spam?' — which?"* → Classification. Two choices.
- *"The slope is 3.6. Say it as a sentence."* → "Each extra hour of revision a week goes with about 3.6 more marks."
- *"What does the intercept 49.4 mean?"* → What the line predicts at zero hours. Nobody in the data revised zero, so it is machinery, not a measured fact.
- *"Could the slope be negative?"* → Yes: "each extra kilometre from school goes with about 2 lakh less on the price." Downhill line, same sentence with "less".
- *"Add up the six misses."* → Zero. A best-fit line always balances, which is exactly why MAE drops the signs.
- *"What does MAE 2.67 mean?"* → On average the line is off by about 2.67 marks. In marks, out loud, to anybody.
- *"What does R² 0.804 mean?"* → The line explains about 80% of the variation, compared with guessing the average. It is not 80% accuracy.
- *"How many hours did anybody in our data revise?"* → At most six. So the 20-hour prediction of 121.4 marks is a promise the data never made.

---

## 🔮 Next Week Preview

Week 33 is the most important lesson in Level 2, and it is a lab. The student takes one dataset, cuts it into train and test **once**, and then runs three completely different models across that one split — last week's tree, this week's line, and Week 29's nearest-neighbours — changing one line each time, and scoring all three into a single table. One row of that table is the punchline: a tree with no depth limit gets a **perfect** score on the rows it learned from and does **worse than guessing the average** on the rows it has never seen. Then comes the picture that explains it: turn the depth dial from 1 to 15, plot the training score and the test score on the same axes, and watch one line climb to near-perfection while the other peaks early and sags. The student draws a vertical line at the peak, labels it, and says the sentence out loud — *"after here it is memorising."* Everything in the term has been building to that sentence.

**Prep early:** two things. First, keep this week's `week32_study_line.py` and last week's `week31_tree_iris.py` where you can find them — Week 33 reuses both models and it is much better if the student can see that a bake-off is just three files they already have, stitched together. Second, and this matters: **go and find whatever the student wrote up in Week 29** about the gap between their training score and their test score. Week 33 ends by sending them back to it. If it was on a whiteboard that has since been wiped, write the numbers on a card now, before you forget them.

---

[⬅ Week 31](week-31.md) · [Course Home](../README.md) · [Week 33 ➡](week-33.md) · [Student Guide](../student-guide/week-32.md) · [Workbook](../workbook/week-32.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)

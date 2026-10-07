# Week 4 — Same Number, Different Ruler

[⬅ Week 3](week-03.md) · [Course Home](../README.md) · [Week 5 ➡](week-05.md) · [Student Guide](../student-guide/week-04.md) · [Workbook](../workbook/week-04.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — the first week of the year with real arithmetic in it |
| **Big idea** | A model compares columns by size, so a column measured in thousands shouts over a column measured in units — until you put them on the same ruler. |
| **New vocabulary** | standardization (z-score) · min-max scaling · one-hot encoding · ordinal encoding · cardinality |
| **New maths** | **standard deviation** as the typical distance of a value from the mean, then the **z-score** = (value − mean) ÷ sd. Both worked by hand on the five numbers **2, 4, 6, 8, 100**. |
| **New syntax** | `MinMaxScaler()` · `scaler.mean_` / `scaler.scale_` · `OneHotEncoder(handle_unknown="ignore")` · `OrdinalEncoder(categories=[...])` |
| **Dataset** | Five numbers typed on paper — `2, 4, 6, 8, 100` — then the numpy-generated pizza-delivery table from Week 1 (`make_data.py`, seed 0) |
| **Materials** | Graph paper, at least four sheets · a calculator (phone is fine) · **five index cards with the five restaurant names on them, and a sixth blank one** · the printed Week 4 workbook (all of it; A6, Draw It and Build It are the ones used today) · the Bug Log |
| **Tech needed** | Laptop with Python 3, numpy, pandas, scikit-learn. `make_data.py` from Week 1 must still be in the folder. Nothing new to install. |
| **Prep time** | 20 minutes the night before · 5 minutes on the day |
| **Expected runtime of the code** | Every block in this lesson finishes in **under 2 seconds**. The `make_data.py` import is the slowest part and it is about half a second. |

> **⚠️ Watch out:** this is the first week where **you have to do arithmetic in front of the student**, and the single thing that ruins the lesson is doing it faster than they can follow. Work the five numbers `2, 4, 6, 8, 100` on the board slowly enough that the student is *ahead of you* by the third step. If you have never met a standard deviation, read section 2 below — it takes about ten minutes and there is no calculus in it, only subtraction, squaring, adding, dividing and one square root.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Work out the standard deviation of five numbers by hand** — subtract the mean, square, add, divide by five, square-root — and check the answer against numpy.
2. **Standardize and min-max scale the same column by hand**, then say which of the two they would pick for that data and why.
3. **One-hot encode a five-category column by hand**, count the columns they created, and explain what `handle_unknown="ignore"` saves them from.
4. **Show, with a concrete example, the false ordering that ordinal encoding invents** when the categories are not really a ladder.

Observable evidence: a sheet of graph paper with `2, 4, 6, 8, 100` scaled both ways and the sklearn output written beside it agreeing to four decimal places; five index cards laid out as a one-hot row with the new columns counted out loud; and one written sentence naming the thing an ordinal-coded `weather` column makes the model believe that is not true.

---

## 🧑‍🏫 What YOU Need to Know First

This section is your own preparation: the maths and the code of the week, taught to you from scratch.

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**You need no maths beyond arithmetic to teach this week, and no statistics at all.** What follows teaches you the whole thing from scratch. It takes about twenty minutes to read and you will be comfortably ahead of the student.

### 1. Why this week exists

Weeks 1 to 3 built the machinery: a contract, three piles of rows, a `Pipeline`, a saved artifact. The model inside it was `LogisticRegression`, and here is the one fact about it that makes today necessary.

**A model like this works by multiplying every column by a number it learned, and adding the results up.** One number per column. That number is called a **weight**, and the model chooses it by trying to make the sum come out right.

Now look at two real columns from the delivery table:

| Column | Smallest | Biggest | A "step of 1" means |
|---|---|---|---|
| `distance_km` | 0.33 | 14.40 | one extra kilometre — a whole neighbourhood further |
| `driver_experience_months` | 0 | 59 | one extra month on the job — almost nothing |

To the model these are the same size step. It has no idea that a kilometre is a big deal and a month is not. So the two columns arrive on wildly different rulers, and every method that measures how far apart two rows are — nearest neighbours, k-means, and any model that is penalised for having large weights, which includes the default `LogisticRegression` — quietly lets the column with the bigger numbers do most of the talking.

**The fix is one subtraction and one division per column.** That is the entire technical content of the first half of today.

![Two columns, two rulers](../figures/fig-w04-1-two-columns-different-rulers.svg)
*Figure 4.1 — Two columns, two rulers. On the left, "one step" means two completely different things. On the right, after one subtraction and one division, both columns say the same thing: how many typical steps from average this value is.*

### 2. The maths, from scratch: what a standard deviation actually is

Forget the word. Here is the question it answers:

> **"On this list of numbers, how far from the average is a typical value?"**

That is it. It is a typical distance. And you are about to compute one, on five numbers, using nothing but subtraction, multiplication, addition, division and one square root.

**The five numbers are 2, 4, 6, 8 and 100.** Use these exact five all week. They are chosen so the arithmetic is easy and so the last one is a monster.

**Step 1 — the mean.** Add them up, divide by how many there are.

```text
2 + 4 + 6 + 8 + 100 = 120
120 ÷ 5 = 24
```

The mean is **24**. Notice immediately that this is a strange "average" — four of the five numbers are 8 or less, and the average is 24. One value dragged it. Say that out loud in the lesson; it is a free lesson about averages.

**Step 2 — how far is each number from 24?** Subtract.

```text
2  − 24 = −22
4  − 24 = −20
6  − 24 = −18
8  − 24 = −16
100 − 24 = +76
```

**Step 3 — get rid of the minus signs by squaring.** Here is the honest reason, and a student *will* ask: if you just averaged those five distances as they are, the minuses and the pluses would cancel out and you would get zero every single time, for every list of numbers ever. Try it: −22 − 20 − 18 − 16 + 76 = 0. Exactly zero. Useless. So you square each one first, because a squared number is never negative.

```text
(−22) × (−22) = 484
(−20) × (−20) = 400
(−18) × (−18) = 324
(−16) × (−16) = 256
(+76) × (+76) = 5776
```

**Step 4 — average those.** Add them up, divide by 5.

```text
484 + 400 + 324 + 256 + 5776 = 7240
7240 ÷ 5 = 1448
```

**Step 5 — undo the squaring.** You squared everything in step 3, so the 1448 is in "squared" units. Take the square root to get back to normal units.

```text
the square root of 1448 = 38.0526
```

**That 38.0526 is the standard deviation.** It is the typical distance from 24. It looks large next to 2, 4, 6 and 8 — and it should, because the 100 really is out there. (If a student averages the plain distances 22, 20, 18, 16, 76 they get 30.4, not 38.05: squaring makes big gaps count extra. Both are "typical"; the standard deviation is the one every library uses.)

> **🔢 The maths, slowly:** five operations, in this order, and no others. **Subtract** the mean from each value. **Square** each answer. **Add** them up. **Divide** by how many values there are. **Square-root** it. If you can do those five things you can compute a standard deviation, and you have just done one.

**Where to stop.** Do **not** mention variance as a named quantity (it is the 1448, and naming it adds a word for nothing today). Do **not** mention the difference between dividing by *n* and dividing by *n* − 1 unless a student who has met it at school asks — and if they do, the honest answer is in the Questions section below. `StandardScaler` divides by *n*, which is what we did, so our hand-arithmetic and sklearn agree exactly, and that agreement is the point of the lesson.

### 3. From standard deviation to z-score, which is the actual tool

Now the payoff. The **z-score** of a value is:

> **z-score** — how many standard deviations a value sits away from the mean. You get it by taking away the mean and then dividing by the standard deviation.

Both numbers are already on the board. So:

```text
(2   − 24) ÷ 38.0526 = −0.5781
(4   − 24) ÷ 38.0526 = −0.5256
(6   − 24) ÷ 38.0526 = −0.4730
(8   − 24) ÷ 38.0526 = −0.4205
(100 − 24) ÷ 38.0526 = +1.9972
```

Read the answers out loud in English, because that is where the meaning lives: *"2 sits about half a typical step below average. 100 sits two typical steps above average."*

**Doing this to a column is called standardization**, and after you have done it the column has mean 0 and standard deviation 1 — always, for any column, which is exactly why it puts every column on the same ruler.

### 4. The other ruler: min-max scaling

**Min-max scaling** is the other obvious thing you could do, and it is simpler:

> **min-max scaling** — subtract the smallest value, then divide by the range (biggest minus smallest). The smallest value becomes 0, the biggest becomes 1, everything else lands in between.

For our five numbers: smallest 2, biggest 100, so the range is 100 − 2 = **98**.

```text
(2   − 2) ÷ 98 = 0.0000
(4   − 2) ÷ 98 = 0.0204
(6   − 2) ÷ 98 = 0.0408
(8   − 2) ÷ 98 = 0.0612
(100 − 2) ÷ 98 = 1.0000
```

**Look at what happened.** Four of the five values are now squashed into the bottom 6% of the ruler. `2` and `8` — which are genuinely different numbers — are now 0.0000 and 0.0612, almost indistinguishable. The single freak value ate the whole scale.

That is the difference between the two recipes, and it is the whole reason there are two:

| | Standardization (z-score) | Min-max scaling |
|---|---|---|
| What it divides by | the typical distance from average | the total range |
| Where the output lands | centred on 0, no fixed limits | between 0 and 1, on the training data |
| One freak value | gets a big z; everyone else barely moves | crushes everyone else towards 0 |
| A new value bigger than anything you trained on | fine — bigger z | **escapes the 0-to-1 box**, which was the whole promise |
| Reach for it when | almost always: linear models, anything measuring distance between rows | the input genuinely has hard limits (pixels are 0–255), or something downstream requires 0-to-1 |
| Our delivery data | ✅ this one | ❌ `distance_km` has a long tail out to 14.40 |

**The default is standardization.** Min-max needs a reason.

![Five numbers, two rulers, all the arithmetic](../figures/fig-w04-2-z-score-arithmetic-on-five-numbers.svg)
*Figure 4.2 — Five numbers, two rulers, all the arithmetic. Every step is a subtraction, a squaring, an addition, a division or a square root. Nothing else is happening.*

### 5. Every line of this week's code, explained to someone who has never programmed

```python
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
```

`import` means "go and fetch a toolbox somebody else wrote". `numpy` is the toolbox for grids of numbers, nicknamed `np`. The second line says: out of scikit-learn's box of preparing-data tools, fetch exactly two — `MinMaxScaler` and `StandardScaler`. Fetching them by name rather than the whole box is the convention here.

```python
x = np.array([2, 4, 6, 8, 100], dtype=float)
```

Make a row of five numbers and give it the name `x`. `dtype=float` says "treat these as decimals, not whole numbers", which matters because the answers are decimals.

```python
X = x.reshape(-1, 1)
```

**This line is a formality that trips up everybody, so know what it is for.** scikit-learn always wants a *table*: rows are examples, columns are features. `x` is one flat row of five numbers, which is ambiguous — is that five examples of one thing, or one example of five things? `reshape(-1, 1)` says "make it one column, and work out the number of rows yourself" (that is what the `-1` means). So `X` is five rows and one column. Capital `X` for the table, small `x` for the flat row, is a widespread habit worth copying.

```python
ss = StandardScaler().fit(X)
```

Two things in one line. `StandardScaler()` builds a brand-new, empty scaler — it knows the recipe but no numbers yet. `.fit(X)` makes it **look at X and remember two things: the mean and the standard deviation.** Nothing is changed or returned; the scaler has simply learned. `ss` is the name we gave the trained scaler.

```python
print("scaler.mean_ :", ss.mean_)
print("scaler.scale_:", ss.scale_)
```

**These two lines are new syntax this week and they matter more than they look.** `ss.mean_` and `ss.scale_` are the two numbers the scaler learned — the mean, and the standard deviation. The trailing underscore is a scikit-learn convention meaning *"I learned this from data; I did not have it before you called `.fit`"*. Every learned thing in scikit-learn ends in an underscore, all year. Printing these two numbers is how you check the machine agrees with your paper.

```python
print(np.round(ss.transform(X).ravel(), 4))
```

`ss.transform(X)` applies the recipe: subtract the remembered mean, divide by the remembered standard deviation. It hands back a new table; it does not change `X`. `.ravel()` flattens the answer from a one-column table back to a flat row so it prints on one line. `np.round(..., 4)` rounds to four decimal places so it fits the page and so it matches what we wrote by hand.

```python
mm = MinMaxScaler().fit(X)
```

Same shape of thing, other recipe. This one remembers the smallest and biggest instead, in `mm.data_min_` and `mm.data_max_`.

**And the one rule that governs all of it:** `.fit` may only ever see the **training** rows. `.transform` is applied to everything. Weeks 2 and 3 built the three-pile split and the `Pipeline` precisely so this is automatic — and Week 6 is going to show you what happens when it is not.

### 6. Words into numbers: the two encoders, one of which is a trap

A model multiplies by weights. It cannot multiply `"CrustyBros"` by anything. So words have to become numbers, and there are exactly two ways.

**One-hot encoding** makes one new yes-or-no column per category.

```text
restaurant = "Napoli"   →   restaurant_CrustyBros    = 0
                            restaurant_GreenLeaf     = 0
                            restaurant_Napoli        = 1
                            restaurant_SliceHouse    = 0
                            restaurant_TandooriPizza = 0
```

One column of words becomes five columns of 0s and 1s, with exactly one 1 in every row. The model now gets five separate weights and can put each restaurant exactly where the data says it belongs.

**Ordinal encoding** maps each category to a single integer: `clear → 0`, `rain → 1`, `storm → 2`. One column in, one column out.

🍕 **The analogy that does the work.** Ordinal encoding says *"these things are rungs on a ladder — one is above the next."* T-shirt sizes really are a ladder: large is above medium is above small. **Restaurants are not.** If you code `{CrustyBros: 0, GreenLeaf: 1, Napoli: 2, SliceHouse: 3, TandooriPizza: 4}` you have told the model that Napoli is *twice* GreenLeaf and that CrustyBros plus TandooriPizza is *twice* Napoli. It will believe you. It will be wrong.

**And here is the false ladder, measured on our own data.** These are real lateness rates from the delivery table:

| restaurant | alphabetical code | how often late | what one weight on the code can say | what one-hot says |
|---|---|---|---|---|
| CrustyBros | 0 | 0.3715 | 0.3260 | 0.3705 |
| GreenLeaf | 1 | 0.2787 | 0.3070 | 0.2789 |
| Napoli | 2 | **0.2336** | **0.2886** | 0.2341 |
| SliceHouse | 3 | 0.2899 | 0.2710 | 0.2899 |
| TandooriPizza | 4 | 0.2835 | 0.2540 | 0.2837 |

Read the third column: 0.3715, then down to 0.2336, then back **up** to 0.2899. It zig-zags. Now read the fourth column: 0.3260, 0.3070, 0.2886, 0.2710, 0.2540 — a perfectly straight, steadily falling line. **One weight on a code can only draw a straight line through those five positions.** It cannot bend. So for Napoli it says 0.2886 when the truth is 0.2336 — out by 0.0550, and there is nothing the model can do about it.

The fifth column is one-hot: 0.3705, 0.2789, 0.2341, 0.2899, 0.2837. Five weights, five values, each landing on its own truth.

![The ladder that is not there](../figures/fig-w04-4-ordinal-false-ladder.svg)
*Figure 4.4 — The ladder that is not there. The five real rates zig-zag; one weight on a code can only draw the straight line. For Napoli that costs 0.0550.*

**The two things to say about `handle_unknown="ignore"`.** In training you saw five restaurants. Next month a sixth opens. Without that setting, your saved artifact **throws an exception on a live request** — a real outage, from a real business event. With it, the unseen name becomes five zeros: the model falls back on distance, weather and the rest, gives a worse-but-sane answer, and stays alive. That behaviour belongs in the model card you wrote in Week 3.

### 7. Cardinality, the last new word

> **cardinality** — how many different values a column has.

`restaurant` has cardinality 5. `day_of_week` has 7. `weather` has 3. Total new columns if you one-hot all three: 5 + 7 + 3 = **15**, replacing 3 old ones.

That is fine. **The reason the word exists** is what happens at cardinality 41,000 — a postcode column. One-hot gives you 41,000 columns, nearly all zero, most of them seen once or twice. Say the word, give the number, and stop: the escapes from high cardinality are Week 5's and Week 7's business, and the honest short answer today is *"don't one-hot 41,000 things; build a column that says something about the postcode instead."*

### 8. The three misconceptions you will actually meet

**"Scaling changes the data, so it changes the answer."** It does not change the *ordering* within a column. (It does change how far apart two rows look when several columns are compared, because it changes how much each column counts; that is the reason to scale.) 2 is still the smallest and 100 still the biggest, before and after, on both rulers. What changes is the *size of the numbers the weights get multiplied by*. Have them check it: the five z-scores are in exactly the same order as the five raw values.

**"So min-max is better because 0 to 1 is tidy."** This is the commonest one and the figure kills it. Show them 0.0000, 0.0204, 0.0408, 0.0612 and 1.0000 and ask which four numbers are now nearly the same number. Tidy is not the goal; *usable* is.

**"One-hot with five columns is wasteful — why not just number them?"** Because numbering them invents a ladder. Then show the table in section 6. This misconception is the whole second half of the lesson and it deserves the measured answer, not an assertion.

### 9. How deep to go, and where to stop

| Do not teach today | Where it lives |
|---|---|
| Variance as a named quantity, and *n* vs *n* − 1 | Not in this course as a named idea. Answer honestly if asked (see Questions), then move on. |
| `RobustScaler`, `QuantileTransformer`, `PowerTransformer` | Nowhere in Level 3. Two scalers is the whole toolbox this year. |
| `LabelEncoder` | **Never.** It is documented for the *label* column only and cannot handle unseen values. If a student finds it online, this is the answer. |
| `drop="first"` on `OneHotEncoder` (dropping one column to avoid redundancy) | Mention only if asked. It matters for classical statistics and does not matter for anything in this course. |
| `max_categories` / `infrequent_if_exist` for high cardinality | Week 7, when they meet a column with a long tail. |
| Target encoding (replace each category with its average outcome) | **Not this year.** It is a leakage minefield and Week 6 has enough leakage in it. |
| Cyclical hour encoding with sine and cosine | Week 5 mentions bins; sine and cosine need trigonometry we do not lean on until much later. |
| Why `LogisticRegression` in particular is affected (the penalty on large weights) | Week 13. Today: "it multiplies each column by a weight and adds up." |

---

### 10. 🧭 The Growing Map

The student guide carries **Where This Fits** — the same picture every week with one more piece filled in.
This week the map changes in a way it has not changed before: a tile goes **white**.

![The Level 3 pipeline in Week 4: the scaling and features tile of SPLIT HONESTLY opens](../figures/fig-w04-0-where-this-fits.svg)

*Figure 4.0 — Week 4's version. The first tile is solid white, meaning finished; the gold has moved down to
the scaling and features tile. The ↻ on stage three is the training loop, still grey until Week 12.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and ask *"what is different about this picture?"*** before you ask anything else. The answer
   is **two** things: the top tile is white now, and the gold has moved. Make them say both. This is the
   first week of the year the map records finished work, and it is worth the extra fifteen seconds.
2. **Then *"which box did we do today?"*** — the second tile, *scaling · features*. Follow with the
   week's actual question: *"we put `2, 4, 6, 8, 100` on one ruler today. Which stage of this pipeline
   was that, and which stage was it **not**?"* It was stage one. It was **not** stage two, measuring, and
   it was **not** the model. Scaling is a decision about the table, which is why it lives up here.
3. **Then one pointer forward:** *"find the tile where a badly scaled column stops a model learning
   altogether."* Stage three, bottom tile, Week 15. Say only that the thing they did on graph paper today
   is what decides whether that week works, and leave it there.

> **🧑‍🏫 Why this is worth two minutes.** Week 4 is the first week that feels like arithmetic homework
> rather than AI, and the honest reason it is not is structural: scaling sits inside stage one, so every
> number stages two through five ever produce is measured on a table this week's decisions shaped. The map
> shows that in one glance. Without it, "standard deviation" reads as a detour.

**If a student asks why the white tile has no tick or badge:** finished tiles are deliberately plain — done
is done, and only the tile you are standing in is coloured. By March most of the map is white, and the
value of the picture is entirely in how much of it still is not.

---

## 🧰 Prep Checklist

This section lists what to set up before the lesson, with the complete runnable files.

### 20 minutes the night before

**1. (2 min) Check the folder.** Open a terminal in the project folder from Weeks 1–3 and run:

```bash
python3 -c "import numpy, pandas, sklearn; print(numpy.__version__, pandas.__version__, sklearn.__version__)"
ls make_data.py
```

You want three version numbers and the filename echoed back. If `make_data.py` is missing, the paper fallback below still delivers three of the four objectives — but find the file, because Weeks 5, 6 and 7 all need it.

**2. (8 min) Run this yourself, first.** Create `rulers.py` in the same folder as `make_data.py`:

```python
"""rulers.py - the five numbers, then two real columns."""
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

x = np.array([2, 4, 6, 8, 100], dtype=float)
X = x.reshape(-1, 1)

ss = StandardScaler().fit(X)
print("scaler.mean_ :", ss.mean_)
print("scaler.scale_:", ss.scale_)
print("z-scores     :", np.round(ss.transform(X).ravel(), 4))

mm = MinMaxScaler().fit(X)
print("data_min_    :", mm.data_min_, " data_max_:", mm.data_max_)
print("min-max      :", np.round(mm.transform(X).ravel(), 4))

print("\na new value of 150 turns up at prediction time:")
print("  z      :", np.round(ss.transform([[150.0]]).ravel(), 4))
print("  min-max:", np.round(mm.transform([[150.0]]).ravel(), 4))
```

```bash
python3 rulers.py
```

Real output, and this is what you must get:

```text
scaler.mean_ : [24.]
scaler.scale_: [38.05259518]
z-scores     : [-0.5781 -0.5256 -0.473  -0.4205  1.9972]
data_min_    : [2.] data_max_: [100.]
min-max      : [0.     0.0204 0.0408 0.0612 1.    ]

a new value of 150 turns up at prediction time:
  z      : [3.3112]
  min-max: [1.5102]
```

**Runtime: under 1 second.** Note two things for yourself. `-0.473` prints with three decimals, not four, because `np.round` drops a trailing zero — the number is −0.4730 and a student will spot the difference and think something is wrong. And `min-max: 1.5102` is **outside the 0-to-1 box**, which is the whole argument against min-max, delivered by the machine.

**3. (6 min) Run the second file.** Create `encode.py`:

```python
"""encode.py - words into numbers."""
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

small = pd.DataFrame({"restaurant": ["Napoli", "SliceHouse", "CrustyBros",
                                     "TandooriPizza", "GreenLeaf"]})
ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
out = ohe.fit_transform(small)
print("columns created:", ohe.get_feature_names_out())
print("in shape:", small.shape, " out shape:", out.shape)
print(pd.DataFrame(out.astype(int), columns=ohe.get_feature_names_out(),
                   index=small["restaurant"]).to_string())

print("\na sixth restaurant opens:")
print("PopUpPizza ->", ohe.transform(pd.DataFrame({"restaurant": ["PopUpPizza"]})).astype(int))

oe = OrdinalEncoder(categories=[["clear", "rain", "storm"]])
w = pd.DataFrame({"weather": ["clear", "rain", "storm", "rain", "clear"]})
print("\nweather codes:", oe.fit_transform(w).ravel().astype(int))
```

Real output:

```text
columns created: ['restaurant_CrustyBros' 'restaurant_GreenLeaf' 'restaurant_Napoli'
 'restaurant_SliceHouse' 'restaurant_TandooriPizza']
in shape: (5, 1)  out shape: (5, 5)
               restaurant_CrustyBros  restaurant_GreenLeaf  restaurant_Napoli  restaurant_SliceHouse  restaurant_TandooriPizza
restaurant                                                                                                                    
Napoli                             0                     0                  1                      0                         0
SliceHouse                         0                     0                  0                      1                         0
CrustyBros                         1                     0                  0                      0                         0
TandooriPizza                      0                     0                  0                      0                         1
GreenLeaf                          0                     1                  0                      0                         0

a sixth restaurant opens:
PopUpPizza -> [[0 0 0 0 0]]

weather codes: [0 1 2 1 0]
```

**Runtime: about 1 second.** The column names come out **alphabetically sorted**, not in the order you typed them. Expect the question.

**4. (4 min) Print and cut.**

- The Week 4 workbook, printed in full. Today uses **A6**, **Draw It** and **Build It**; the rest is practice bank.
- **Five index cards**, one restaurant name on each in big letters: `Napoli`, `SliceHouse`, `CrustyBros`, `TandooriPizza`, `GreenLeaf`. Plus **one more card reading `PopUpPizza`**, kept in your pocket until the end of the activity.
- Four sheets of graph paper.
- Figure 4.2 printed, **face down**. It is the answer to the first half of the activity and it goes face-up only at the end.

### 5 minutes on the day

- Open a terminal in the project folder.
- Write `2  4  6  8  100` on the board and nothing else.
- Put the five index cards face down in a pile.
- Have Figure 4.1 up on screen or printed, ready for minute 8.

### Fallback if the laptops fail

**This week's paper fallback is genuinely excellent** — three of the four objectives are pencil-and-paper anyway, and the fourth is index cards.

| If this fails | Do this instead |
|---|---|
| `ModuleNotFoundError: No module named 'sklearn'` | Do not debug live for more than three minutes. The whole of the maths, the whole of the one-hot activity and the whole of the ordinal-ladder discussion work on graph paper and index cards. Set "run `rulers.py` and check my four decimal places" as the first homework item, and check the install yourself before Week 5. |
| `make_data.py` is missing or errors | Use only the five numbers and the five index cards. You lose the "two real columns on different rulers" opening — replace it by writing the two ranges on the board from the table in section 1 and asking which column shouts. |
| The projector fails | Read the numbers out and have the student write them. This lesson is almost entirely numbers being written down. |
| A student's answer disagrees with sklearn in the 4th decimal place | Almost always they used a rounded standard deviation (38.05 rather than 38.0526). Have them redo one value with the full number. **This is a good bug and worth two minutes.** |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Which Column Is Shouting? | 7 | 7 | Two real columns, two rulers, one uncomfortable question |
| 🧠 Concept & Maths — Five Numbers on the Board | 18 | 25 | The standard deviation, by hand, slowly; then both rulers |
| 💻 Live-Code Together — `rulers.py` and `encode.py` | 18 | 43 | Check the hand-arithmetic; two deliberate mistakes |
| 🎲 Their Turn — The Two Rulers, and Five Cards | 20 | 63 | Graph paper, then index cards on the table |
| 🔑 Wrap & Assign | 7 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — Which Column Is Shouting? (7 minutes)

**Do this:** Nothing on the screen. Write these two lines on the board and nothing else:

```text
distance_km                0.33  ...  14.40
driver_experience_months      0  ...  59
```

> **Say this:** "Two columns out of the delivery table you have been working on for three weeks. The top one is how far the pizza had to go, in kilometres. The bottom one is how long the driver has been doing the job, in months.
>
> Last week you put both of these into a model. The model works like this, and this is the only thing you need to know about it today: it picks one number for each column — call it a weight — multiplies the column by its weight, and adds everything up. One weight per column.
>
> So here is my question, and I want you to sit with it for a second. **Does the model know that one kilometre is a big deal and one month is almost nothing?**"

Wait. Let them answer.

> "No. It has no idea. It has never been outside. All it sees is that the bottom column's numbers go up to 59 and the top column's numbers stop at 14.4. Four times bigger.
>
> And that matters, because there are whole families of methods — nearest neighbours, which you built two years ago, measure **how far apart two rows are**, and models like the one you used last week are nudged to keep their weights small. Either way, if one column's numbers are four times bigger than another's, that column tends to do most of the shouting. Not because it matters more. Because somebody chose to measure it in months instead of years."

**Do this:** Put Figure 4.1 on the screen. Point at the left-hand half only. Cover the right-hand half with your hand or a sheet of paper.

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Which of those two bars is longer?" | The experience one, by about four times. | If they say "the distance one is more important", agree that it probably is — and that this is exactly the problem, because *importance* is not what the bar is showing. |
| "How would you make the two bars the same length?" | Divide each column by something to do with its own size. | Any answer in the shape of "divide by something" is a win. If they say "divide by the biggest one", that is min-max and you will meet it in twenty minutes — say so and write their name next to it. |
| "What could you divide by?" | The biggest value. The average. How spread out it is. | All three are real answers. Two of them are today's lesson. Write all suggestions on the board and leave them up. |
| "Is this a problem with the data or with the model?" | Neither, really — it is a problem with the units somebody chose. | If they blame the model, push once: "would the model be fine if we'd recorded experience in years?" (Yes. Which tells you it was never about the model.) |

> **Say this:** "So the job today is one subtraction and one division per column. That is genuinely all it is. But we are going to do it by hand first, on five numbers small enough to argue about, because the *choice* of what to divide by turns out to matter a great deal."

**Do this:** Uncover the right-hand half of Figure 4.1. Do not explain it yet. Just let it sit there.

---

### 🧠 Concept & Maths — Five Numbers on the Board (18 minutes)

**Do this:** Clear the board except for the two column ranges. Write, very large, with plenty of space underneath:

```text
2    4    6    8    100
```

> **Say this — part 1, the mean and the surprise in it:** "Five numbers. Add them up for me."

*120.*

> "120. Divide by five."

*24.*

> "**24.** Now — is 24 a fair description of those five numbers?"

Let them find it. Someone will say no.

> "No. Four of the five are eight or less, and the 'average' is 24. **One number dragged it.** Keep that in your head, because in about ten minutes it is going to matter enormously.
>
> Now the real question. I want to know: **on this list, how far from 24 is a typical number?** Not the biggest gap, not the smallest. Typical. Because that is what I am going to divide by."

**Do this:** Write the five subtractions in a column, and let the student call out each answer before you write it.

```text
2   − 24 = −22
4   − 24 = −20
6   − 24 = −18
8   − 24 = −16
100 − 24 = +76
```

> **Say this — part 2, why we square:** "Five distances. So let's average them. Add them up for me."

Let them do it. They will get zero.

> "**Zero.** And that is not bad luck — it happens every single time, for every list of numbers there has ever been, because the mean is exactly the place where the pluses and the minuses balance out. That is what a mean *is*.
>
> So averaging them straight is useless. We need to get rid of the minus signs. There are two obvious ways: throw the minus signs away, or **square everything**, because a negative times a negative is positive. Squaring is the one everybody uses and it is the one the computer will use, so square."

**Do this:** Second column on the board, again with them calling the answers.

```text
(−22)² =  484
(−20)² =  400
(−18)² =  324
(−16)² =  256
(+76)² = 5776
```

> **Say this — part 3, finish it:** "Add those five up."

*7240.*

> "7240. Divide by five."

*1448.*

> "1448. And now one last step, and it is the step people forget. We **squared** everything back there. So 1448 is in squared units — it is far too big to be a distance. Undo the squaring."

*Square root.*

> "Square root. Put 1448 into your calculator and hit the square root button."

*38.0526...*

> "**38.0526.** And that number has a name — it is called the **standard deviation** — but the name is much less useful than the sentence, so here is the sentence: *on this list, a typical number sits about 38 away from the average.*
>
> Which, looking at 2, 4, 6 and 8, feels far too big. And it is. That is what one value of 100 does to a list of five numbers."

**Do this:** Draw the finished board. It should look like this by now, and it is worth leaving up for the whole lesson:

![The finished board](../figures/fig-w04-5-board-two-rulers-worked.svg)
*Figure 4.3 — The finished board. Five operations in order: subtract, square, add, divide, square-root. Then the machine's answer beside it, agreeing to four decimal places. Then the sentence of judgement, which is the part that gets marked.*

> **Say this — part 4, the z-score:** "Now I have my two numbers: the average, 24, and the typical gap, 38.0526. So here is the recipe, and it is the whole first half of today.
>
> **Take away the average. Divide by the typical gap.**
>
> Do it for 2. Two take away 24 is minus 22. Minus 22 divided by 38.0526 is..."

*−0.5781.*

> "Minus 0.58. And say that out loud in English: **'2 sits about half a typical step below average.'** That sentence is the whole point. It doesn't matter any more whether we were counting kilometres or months or rupees — the answer is in *typical steps*, and every column can be put in typical steps. Same ruler."

**Do this:** Work all five with them. Write them under the raw numbers so they line up.

```text
raw       2         4         6         8        100
z      −0.5781   −0.5256   −0.4730   −0.4205   +1.9972
```

> **Say this — part 5, the other ruler:** "Somebody suggested at the start that we divide by the biggest number. Let's do the version of that idea people actually use, and it is called **min-max scaling**. Take away the *smallest*, then divide by the *range* — biggest minus smallest.
>
> Smallest is 2. Biggest is 100. So the range is 98. Off you go."

**Do this:** Third row on the board.

```text
raw       2         4         6         8        100
z      −0.5781   −0.5256   −0.4730   −0.4205   +1.9972
min-max 0.0000    0.0204    0.0408    0.0612    1.0000
```

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Which four of those min-max numbers are now nearly the same number?" | The first four — they are all between 0 and 0.06. | If they do not see it, ask: "how much of the ruler from 0 to 1 do 2, 4, 6 and 8 use between them?" (6% of it.) |
| "Was 2 nearly the same as 8 in the original list?" | No — 8 is four times 2. | This is the moment min-max dies. Let the silence do the work. |
| "Which ruler treated the 100 more gently?" | The z-score one. 100 got +2.0 and everybody else stayed spread out. | If they say min-max because 1.0 is tidy, ask them what happened to everybody else. |
| "A new value of 150 arrives tomorrow. What does min-max give it?" | Something bigger than 1. | Most will guess "1". Do not correct — you are running it in eight minutes and the machine will say 1.5102. Write both guesses on the board. |
| "Which one would you use on `distance_km`, which runs 0.33 up to 14.40 with most of them under 5?" | The z-score, because of the long tail. | Any answer that mentions the big values is a good answer. |
| "Do either of these change which order the numbers are in?" | No. 2 is still smallest, 100 still biggest, on both rulers. | If they think scaling reorders things, point at both rows on the board. This is a real and common worry. |

> **Say this:** "Two rulers. **Default to the z-score.** Min-max needs a reason — the honest ones are 'my numbers already have hard limits, like pixel brightness from 0 to 255' or 'something downstream demands 0 to 1'. Neither is true of pizza distances.
>
> And one rule that outranks both formulas, which you already know from Week 3 and which Week 6 will make you feel in your stomach: **the average and the typical gap are worked out from the training rows only.** Never from the whole table. The `Pipeline` you built last week does that for you."

---

### 💻 Live-Code Together — `rulers.py` and `encode.py` (18 minutes)

**You never touch the keyboard.** The student types. Predictions before every run.

**Step 1 (4 min).** New file, `rulers.py`. Dictate:

```python
"""rulers.py - the five numbers, checked by machine."""
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

x = np.array([2, 4, 6, 8, 100], dtype=float)
X = x.reshape(-1, 1)

ss = StandardScaler().fit(X)
print("scaler.mean_ :", ss.mean_)
print("scaler.scale_:", ss.scale_)
```

**Ask before running:** "Those two lines are about to print two numbers. They are both on the board. Which two?"

*24 and 38.0526.*

Run it. Real output:

```text
scaler.mean_ : [24.]
scaler.scale_: [38.05259518]
```

> **Say this:** "**24 and 38.05259518.** Your board says 24 and 38.0526. You just did, by hand, what a machine-learning library does — and you did it right.
>
> Two things about those names. `mean_` and `scale_` both end in an **underscore**. That is a scikit-learn promise: *anything ending in an underscore was learned from your data.* It did not exist before you called `.fit`. Every learned thing all year ends in an underscore, and it is genuinely useful — it tells you at a glance which numbers came from the data and which ones you chose yourself.
>
> And `scale_` is a slightly annoying name for the standard deviation. It is called that because `MinMaxScaler` also has a `scale_`, and it means something different there. Read it as 'the thing I divide by'."

**Step 2 (3 min).** Add the transform.

```python
print("z-scores     :", np.round(ss.transform(X).ravel(), 4))
```

**Ask before running:** "Five numbers coming. They are on the board. Read them to me first."

Run it. Real output:

```text
z-scores     : [-0.5781 -0.5256 -0.473  -0.4205  1.9972]
```

> **Say this:** "Five for five. Now — look hard at the third one. It says `-0.473`. Your board says −0.4730. **Is the machine wrong?**"

*No — it's the same number.*

> "Same number. `np.round` rounded to four decimal places and then Python printed the result without a pointless trailing zero. **This will bite you all year and it is never a bug.** 0.473 and 0.4730 are the same number.
>
> And `.transform` did not change `X`. It handed back a *new* set of numbers. The scaler is a recipe, not an operation on your table — which is exactly why you can save it in a `Pipeline` and apply the same recipe to a row that arrives next Tuesday."

**Step 3 — ⚠️ FIRST DELIBERATE MISTAKE (3 min).** Dictate this and let it fail.

> **Say this:** "Add the min-max version. Type `mm = MinMaxScaler().fit(x)` — small x."

```python
mm = MinMaxScaler().fit(x)
```

Run it. Real output:

```text
Traceback (most recent call last):
  File "/private/tmp/w456/rulers.py", line 12, in <module>
    mm = MinMaxScaler().fit(x)
  File ".../sklearn/preprocessing/_data.py", line 907, in fit
    return self.partial_fit(X, y, sample_weight)
  File ".../sklearn/base.py", line 1365, in wrapper
    return fit_method(estimator, *args, **kwargs)
  File ".../sklearn/preprocessing/_data.py", line 943, in partial_fit
    X = validate_data(
  File ".../sklearn/utils/validation.py", line 2954, in validate_data
    out = check_array(X, input_name="X", **check_params)
  File ".../sklearn/utils/validation.py", line 1091, in check_array
    raise ValueError(msg)
ValueError: Expected 2D array, got 1D array instead:
array=[  2.   4.   6.   8. 100.].
Reshape your data either using array.reshape(-1, 1) if your data has a single feature or array.reshape(1, -1) if it contains a single sample.
```

**Do this:** Let them read it. Do not explain first.

> **Say this:** "Read me the last line."

*Expected 2D array, got 1D array.*

> "**'I wanted a table and you gave me a row.'** And then look what it does — it tells you the fix, in the message: *'Reshape your data using array.reshape(-1, 1) if your data has a single feature.'* scikit-learn's error messages are unusually kind. Read them.
>
> Why does it care? Because scikit-learn always wants rows-are-examples, columns-are-features. `[2, 4, 6, 8, 100]` is ambiguous — is that five examples of one thing, or one example of five things? It refuses to guess. `reshape(-1, 1)` says 'one column, work the rows out yourself'. That is why line 6 exists."

Fix it — capital `X` — and add the rest:

```python
mm = MinMaxScaler().fit(X)
print("data_min_    :", mm.data_min_, " data_max_:", mm.data_max_)
print("min-max      :", np.round(mm.transform(X).ravel(), 4))
print("\na new value of 150 turns up at prediction time:")
print("  z      :", np.round(ss.transform([[150.0]]).ravel(), 4))
print("  min-max:", np.round(mm.transform([[150.0]]).ravel(), 4))
```

**Ask before running:** "Both guesses for 150's min-max value are on the board. Which is it?"

Run it. Real output:

```text
data_min_    : [2.] data_max_: [100.]
min-max      : [0.     0.0204 0.0408 0.0612 1.    ]

a new value of 150 turns up at prediction time:
  z      : [3.3112]
  min-max: [1.5102]
```

> **Say this:** "**1.5102.** Min-max promised you a number between 0 and 1, and the first time a bigger value walks in the door it breaks the promise without a word of complaint. No error. No warning. Just 1.5102 in a box that was supposed to stop at 1.
>
> The z-score's answer is 3.3112, and that is not a broken promise — it never promised a limit. It says '150 sits three and a third typical steps above average', which is true, useful, and a bit alarming, which is exactly what you want to feel about a value like that."

**Step 4 (4 min).** New file, `encode.py`. Words into numbers.

```python
"""encode.py - words into numbers."""
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

small = pd.DataFrame({"restaurant": ["Napoli", "SliceHouse", "CrustyBros",
                                     "TandooriPizza", "GreenLeaf"]})
ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
out = ohe.fit_transform(small)
print("columns created:", ohe.get_feature_names_out())
print("in shape:", small.shape, " out shape:", out.shape)
```

**Ask before running:** "Five restaurants in one column. How many columns come out?"

Run it. Real output:

```text
columns created: ['restaurant_CrustyBros' 'restaurant_GreenLeaf' 'restaurant_Napoli'
 'restaurant_SliceHouse' 'restaurant_TandooriPizza']
in shape: (5, 1)  out shape: (5, 5)
```

> **Say this:** "**Five in, five out** — one column of words became five columns of yes-or-no. And look at the names it made: it stuck the old column name on the front of each value. `restaurant_Napoli`. You will be reading names like that for the rest of the year.
>
> Now, one thing to notice, because it confuses everybody once: **they came out in alphabetical order**, not the order I typed them. CrustyBros first. The encoder sorts the categories it finds. It has to pick some order and alphabetical is the one it picked."

**Step 5 — ⚠️ SECOND DELIBERATE MISTAKE (2 min).** This one is the important one, so set it up properly.

> **Say this:** "I want to show you what that `handle_unknown="ignore"` is doing, and the only way is to take it out. Change the line to `OneHotEncoder(sparse_output=False)` — drop the handle_unknown bit — and then try to encode a restaurant that opened last week."

```python
ohe = OneHotEncoder(sparse_output=False)
out = ohe.fit_transform(small)
print(ohe.transform(pd.DataFrame({"restaurant": ["PopUpPizza"]})))
```

Run it. Real output:

```text
Traceback (most recent call last):
  File "/private/tmp/w456/encode.py", line 12, in <module>
    print(ohe.transform(pd.DataFrame({"restaurant": ["PopUpPizza"]})))
  File ".../sklearn/utils/_set_output.py", line 316, in wrapped
    data_to_wrap = f(self, X, *args, **kwargs)
  File ".../sklearn/preprocessing/_encoders.py", line 1043, in transform
    X_int, X_mask = self._transform(
  File ".../sklearn/preprocessing/_encoders.py", line 218, in _transform
    raise ValueError(msg)
ValueError: Found unknown categories ['PopUpPizza'] in column 0 during transform
```

> **Say this:** "`Found unknown categories ['PopUpPizza']`. Now stop and think about where this happens in real life.
>
> This is not a bug in your code. Your code is fine. **A new pizza place opened.** That is a thing the world does. And your saved artifact — the one you shipped last week, the one that answers live requests — has just crashed on a real order, at dinner time, because a business opened a shop.
>
> Put the setting back."

```python
ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
out = ohe.fit_transform(small)
print("PopUpPizza ->", ohe.transform(pd.DataFrame({"restaurant": ["PopUpPizza"]})).astype(int))
```

Run it. Real output:

```text
PopUpPizza -> [[0 0 0 0 0]]
```

> **Say this:** "**Five zeros.** Not a crash, and — importantly — not a fake category either. It says 'this is none of the five I know', and the model shrugs and uses distance, weather, prep time and the rest instead. The answer will be a bit worse. The service stays up.
>
> **Always set it.** And write down what it does in your model card, under known limitations, because a prediction for an unknown restaurant is a slightly different product from a prediction for a known one and whoever uses your output deserves to be told."

**Step 6 (2 min).** The ordinal encoder, and the trap named.

```python
oe = OrdinalEncoder(categories=[["clear", "rain", "storm"]])
w = pd.DataFrame({"weather": ["clear", "rain", "storm", "rain", "clear"]})
print("weather codes:", oe.fit_transform(w).ravel().astype(int))
```

Run it. Real output:

```text
weather codes: [0 1 2 1 0]
```

> **Say this:** "One column in, one column out. `clear` is 0, `rain` is 1, `storm` is 2.
>
> Notice I *told* it the order — `categories=[["clear", "rain", "storm"]]`, in a list, inside a list. **Always tell it.** If you don't, it sorts alphabetically, which for weather gives clear, rain, storm by pure luck, and for `["small", "medium", "large"]` gives large, medium, small, which is backwards and silent.
>
> And now the question that is the whole second half of this week: **is it true that storm is two rains?**"

Let that hang. Then hand out the graph paper.

---

### 🎲 Their Turn — The Two Rulers, and Five Cards (20 minutes)

Full instructions are in the next section. In brief: 10 minutes scaling `2, 4, 6, 8, 100` both ways on graph paper and checking against sklearn to four decimal places; then 10 minutes with the five index cards, building a one-hot row on the table, counting the columns out loud, and meeting `PopUpPizza`.

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Everything stays on the board. Point at the three rows — raw, z, min-max.

> **Say this:** "Four things, and then homework.
>
> **One.** A standard deviation is a typical distance from the average (squaring makes big gaps count extra, so it is a little bigger than the plain average gap: 38.05 against 30.4 here). Subtract, square, add, divide, square-root. Five operations, no magic.
>
> **Two.** A z-score is (value minus mean) divided by that. It turns any column into 'how many typical steps from average', which is the same ruler for every column in the table.
>
> **Three.** Min-max squashes into 0 to 1 — and one freak value squashes everybody else along with it, and a new bigger value breaks straight out of the box. Default to the z-score.
>
> **Four.** Words become numbers one of two ways. One-hot: one yes-or-no column per value, no order invented, always with `handle_unknown="ignore"`. Ordinal: one integer column, and it *invents a ladder*. Use it only when you can say the ladder out loud without wincing."

Run the three checks from **✅ Assessing Understanding**, then assign the homework from **📤 Homework to Assign**.

---

## 🐞 The Debugging Clinic

This section is for reading error messages with the student when the week's code breaks.

Every message below came from running a broken version of this week's actual code.

> **🧑‍🏫 If a student asks:** scikit-learn's tracebacks are long — ten to fifteen lines is normal, and most of the lines are inside scikit-learn where you cannot do anything. **The rule is the same as always: read the last line, then find the `File` line with your own filename in it.** scikit-learn is unusually good about putting the fix *in* the last line. Read it before you guess.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `ValueError: Expected 2D array, got 1D array instead: array=[ 2. 4. 6. 8. 100.]` | "I wanted a table and you handed me a single row." | `.fit(x)` on a flat numpy row instead of `.fit(X)` on a one-column table. | `X = x.reshape(-1, 1)`, then `.fit(X)`. The message itself tells you this — read the second half of it. |
| `ValueError: Found unknown categories ['GreenLeaf'] in column 0 during transform` | "You are asking me to encode a value I never saw when I was fitted." | `OneHotEncoder` without `handle_unknown="ignore"`, meeting a category that only appears in validation, test, or real life. | Add `handle_unknown="ignore"`. The unseen value becomes all zeros. **This is the single most important setting in the week.** |
| `ValueError: Found unknown categories ['storm'] in column 0 during fit` | "You gave me a list of the categories, and the data contains one that is not on your list." | `OrdinalEncoder(categories=[["clear", "rain"]])` — the list is incomplete. Note it says **during fit**, not during transform: the problem is in the training data itself. | Put every category in the list, in the order you mean: `categories=[["clear", "rain", "storm"]]`. Check with `df["weather"].nunique()` first. |
| `ValueError: could not convert string to float: 'clear'` | "You asked me to do arithmetic on a word." | A text column reached `StandardScaler` — usually a column left out of the `ColumnTransformer`'s category list, or `.fit(df)` on the whole table. | Numbers to the numeric branch, words to the categorical branch. Check the two lists in your `ColumnTransformer` against `df.dtypes`. |
| `AttributeError: 'StandardScaler' object has no attribute 'mean_'` | "I have not learned anything yet, so I have no mean to give you." | Asking for `ss.mean_` before calling `.fit`. | `ss = StandardScaler().fit(X)` first. **The underscore is the clue:** anything ending in `_` only exists after `.fit`. |
| `ValueError: Expected a 2-dimensional container but got <class 'pandas.core.series.Series'> instead. Pass a DataFrame containing a single row (i.e. single sample) or a single column (i.e. single feature) instead.` | "One column of a DataFrame is not a DataFrame." | `ohe.fit_transform(df["restaurant"])` with single square brackets. | Double brackets: `ohe.fit_transform(df[["restaurant"]])`. Single brackets give one column on its own; double brackets give a one-column table. |
| **No error**, but the one-hot output prints as `(0, 1) 1.0` on separate lines instead of a grid | Nothing is wrong. You got a *sparse* matrix — a memory-saving format that only lists the non-zero cells. | `OneHotEncoder()` without `sparse_output=False`. | Add `sparse_output=False` while you are learning, so you can *see* the grid. Inside a real `Pipeline` either is fine. |
| **No error**, and a blank cell sails straight through the scaler as `nan` | Nothing is wrong as far as `StandardScaler` is concerned — it ignores blanks when computing the mean, and leaves them blank on the way out. | A hole in the column, and no imputer in front of the scaler. | This is exactly what **Week 6** is about. Today: notice it. `df.isna().sum()` tells you where. |
| **No error**, and the hand answer disagrees with sklearn in the 4th decimal place | Nothing is wrong with either. | The standard deviation was rounded before dividing — 38.05 instead of 38.0526. | Divide by the full number. **Worth two minutes in the lesson:** rounding early then dividing is a genuine source of wrong answers, and it is the kind that never raises an error. |

### How to teach debugging without giving the answer

The moves from Weeks 1–3 all still stand. This week adds two that are specific to scikit-learn:

- **"Read the last line all the way to the end."** scikit-learn frequently puts the exact fix in the message — `reshape(-1, 1)`, `Pass a DataFrame`, `Found unknown categories ['PopUpPizza']` with the offending value quoted. Students stop reading at the colon. Do not tell them the fix; tell them to finish the sentence.
- **"Is that error about a *shape*, a *type*, or a *value*?"** Three questions, three different places to look. Shape means brackets and `reshape`. Type means a word where a number should be. Value means a category the encoder has not met.

And the sentence for this week:

> **"An underscore at the end means the machine learned it. If you get an `AttributeError` on something ending in an underscore, you forgot to `.fit`."**

---

## 🎲 The Activity, In Full

This section gives the full instructions for the hands-on activity, with its easier and harder variations.

### The Two Rulers, and Five Cards

**Setup (2 minutes).** Each student needs: two sheets of graph paper, a calculator, a pencil, and the Week 4 workbook (A6 and Draw It, kept closed until Part 1 is finished). The five index cards go face-down in the middle of the table. Figure 4.2 stays face-down until the very end.

---

### Part 1 — Both rulers, by hand (10 minutes)

**On the board, and nothing else:** `2  4  6  8  100`

**Instructions to give, one at a time, not all at once:**

1. **"Rule up a number line across the page, 0 to 100. Mark the five values on it."** (1 min.) They should end up with four dots bunched at the left and one far out on the right. That picture is the whole lesson and they should draw it before they compute anything.
2. **"Work out the mean. Mark it on your line."** (1 min.) 24. It sits to the *right* of four of the five dots, which surprises people, and it should.
3. **"Work out the standard deviation. Five steps: subtract, square, add, divide by five, square-root. Show every step."** (3 min.) 38.0526.
4. **"Now z-score all five values. Write them in a row under the raw numbers."** (2 min.)
5. **"Now min-max all five. Third row."** (2 min.)
6. **"Draw two more number lines: one from −1 to +2 with your z-scores on it, one from 0 to 1 with your min-max values on it."** (1 min.)

**Then, and this is the part that matters:** open a terminal and run `rulers.py`. Have them write the machine's numbers **directly beside their own** on the graph paper.

> **Say this:** "Four decimal places. Every one. If yours disagrees, do not fix it silently — find out *which step* went wrong. There are only five steps and one of them is guilty."

**Finally:** turn Figure 4.2 face-up and put it next to their page.

**What "finished" looks like:** one sheet of graph paper carrying **three number lines and three rows of five numbers**, with the sklearn output written beside rows two and three and agreeing to four decimal places, and **one sentence at the bottom** saying which ruler they would use on this column and why. The sentence is the marked part. A good one is: *"I'd use the z-score, because 100 is a freak value and min-max squeezes 2, 4, 6 and 8 into the bottom 6% of the ruler where they all look the same."*

---

### Part 2 — Five cards on the table (10 minutes)

**Instructions:**

1. **"Turn the five cards face up and lay them in a row."** These are the five restaurants — one column of words.
2. **"Now I want a row for Napoli. Write a 0 or a 1 under every card: 1 if this row is that restaurant, 0 if it isn't."** They write `0 0 1 0 0` under the cards — in alphabetical order, so CrustyBros, GreenLeaf, Napoli, SliceHouse, TandooriPizza. (Sorting the cards alphabetically first is worth doing, because sklearn will.)
3. **"How many numbers did you just write?"** Five.
4. **"How many columns did you start with?"** One.
5. **"Do it for CrustyBros. And SliceHouse."** Three rows now. They should notice, without being told, that there is exactly one 1 per row.
6. **"Now do `day_of_week` and `weather` in your head. How many columns altogether?"** 5 + 7 + 3 = **15**, replacing 3.
7. **Take the sixth card out of your pocket.** `PopUpPizza`. Put it on the table. **"A new pizza place opened this morning. Write me its row."**

Let them struggle. There is no card for it. Some will invent a sixth column, which is the wrong answer and a good instinct — say why: your model was trained with five weights and a sixth column has no weight to be multiplied by.

8. **"The answer is five zeros. Write `0 0 0 0 0`. That is what `handle_unknown="ignore"` does, and without it your program crashes."**

**What "finished" looks like:** four rows of five 0s and 1s under five sorted cards, the number **15** written down with `5 + 7 + 3` beside it, and the `PopUpPizza` row of five zeros with the words "handle_unknown = ignore" next to it.

---

### Variation — easier

Cut the standard deviation from Part 1 and **give** them 38.0526 as a number on the board. They still do both scalings, still check against sklearn, still draw the three number lines, and still write the judgement sentence — which is three of the four objectives. Then come back to the five steps of the standard deviation with a friendlier list: `[3, 5, 7, 9, 11]`, whose mean is 7 and whose standard deviation is exactly the square root of 8, 2.8284. No monster value, all the arithmetic small.

For Part 2, use only **three** cards (`Napoli`, `SliceHouse`, `CrustyBros`) so the row is three numbers wide.

### Variation — harder

1. **"Add a sixth value of 24 to the list. Predict what happens to the mean and the standard deviation, then check."** The mean stays exactly 24 (the new value *is* the mean). The standard deviation *falls* — to 34.7371 — because you added a value at zero distance and are now dividing by six. Predicting "the sd goes down" correctly is a genuinely strong answer.
2. **"Remove the 100. Now do both scalings on `2, 4, 6, 8`."** Mean 5, sd 2.2361, and min-max gives 0, 0.3333, 0.6667, 1.0 — nicely spread. **Now min-max is the better-looking ruler.** Ask them what changed. (Nothing about the recipes. Only the data.) This is the best question in the week.
3. **"One-hot `day_of_week` on paper, all seven columns, three rows. Then tell me how many of the 21 numbers you wrote are zero."** 18 of 21. Then: "at 41,000 postcodes, what fraction is zero?" This is the cardinality lesson, discovered rather than told.
4. **"Ordinal-code the five restaurants alphabetically. Then look at the real lateness rates in section 6 and tell me which restaurant the straight line gets most wrong, and by how much."** Napoli, by 0.0550.

---

## ❓ Questions Students Ask This Week

This section gives prepared answers to questions students are likely to ask.

**"Why do you divide by 5 and not by 4? My maths teacher divides by one less."**

Your maths teacher is right, for their question, and we are right for ours. Both are used and the difference is real.

Dividing by *n* − 1 is for when your five numbers are a **sample** and you are trying to guess the spread of a much bigger group you cannot see. Dividing by *n* is for when the five numbers are simply **the numbers you have** and you want to describe them.

`StandardScaler` divides by *n*. So we divide by *n*, and our paper and the machine agree to eight decimal places, which is the thing today needed to prove. On a column of 1,200 training rows the difference between dividing by 1,200 and by 1,199 is invisible anyway — it changes the standard deviation by about 0.04%.

**"Does scaling make the model better?"**

Sometimes a lot, sometimes not at all, and it depends on the model — which is an unsatisfying answer, so here is the useful version.

It matters **hugely** for anything that measures distance between rows (nearest neighbours, k-means) or that penalises large weights (which the default `LogisticRegression` does). It matters **not at all** for a decision tree, which only ever asks "is this column above or below some cut-off?" and does not care what units the cut-off is in.

You scale anyway, for two reasons that are nothing to do with score. First, the weights become comparable — a weight of 0.9 on a scaled column and a weight of 0.9 on another scaled column really do mean the same amount of influence, so you can read the model. Second, it costs one line inside a `Pipeline` and it removes an entire category of bug.

**"Why five columns for five restaurants? Isn't the fifth one redundant — if the first four are all zero it must be the fifth?"**

You are exactly right, and this is a genuinely good observation. There is even an option for it: `OneHotEncoder(drop="first")`.

Here is the honest state of it: **for classical statistics it matters, and for the models in this course it does not.** In statistics, leaving all five in makes the maths ambiguous (there are infinitely many sets of weights that give identical predictions). For a model that has a penalty on large weights, as ours does, the ambiguity is resolved for you and leaving all five in is standard practice — and it has one clear practical advantage: with all five columns present, an unknown category is five zeros, and with the first one dropped, four zeros *means* the dropped category. Which is wrong and silent.

So: leave them in. Know that the question is sharp.

**"What if the categories really are a ladder, but the rungs are uneven?"**

**This is the best question of the week and nobody fully agrees on the answer.** Take our own weather column:

| weather | how often late |
|---|---|
| clear | 0.2451 |
| rain | 0.3507 |
| storm | 0.5360 |

The order is real: clear, then rain, then storm. Nobody would argue. But look at the *gaps*:

```text
rain  − clear = 0.3507 − 0.2451 = 0.1056
storm − rain  = 0.5360 − 0.3507 = 0.1853
```

The second step is **1.75 times** the first. So coding them 0, 1, 2 tells the model the two steps are equal, and they are not.

One camp says: use ordinal, one column instead of three, and accept a small distortion — with a genuine ordering the model still gets most of the value. The other camp says: use one-hot, it costs two extra columns and it lets the data speak. There is no settled answer and it depends on how many rows you have (few rows favours ordinal, because three columns is three things to estimate).

**What you do in this course:** try both and let the ablation table decide. That is next week, and this is the exact question to bring to it.

**"Can I just divide by the biggest number and skip the subtracting?"**

Yes, and people do — it is called max-abs scaling. On our five numbers it gives 0.02, 0.04, 0.06, 0.08, 1.00.

Look at what you gave up. You no longer know where the *middle* is, so you cannot tell "above average" from "below average" at a glance, and if a column's values are all around 5,000 you get five numbers all within a hair of 1.0. Subtracting the middle is most of the value. It is not extra work; it is the point.

**"Does the order of the one-hot columns matter?"**

No, and it is worth being clear why, because it is a good sanity check on how the model works.

Every column gets its own weight, chosen independently. Swap two columns and their two weights swap with them and every prediction is identical. That is precisely the property ordinal encoding *destroys*: with one weight on a code, the order is the whole thing.

What *does* matter is that the order stays the **same** between fitting and predicting — column 3 must mean the same restaurant on Tuesday as it did in training. That is exactly the bookkeeping the `Pipeline` from Week 3 does for you, and it is why you save the whole pipeline instead of just the model.

**"You said 'never use LabelEncoder'. Why does it exist then?"**

For the **label** — the `y` column, the answer you are trying to predict. That is what the "Label" in the name means, and its documentation says so.

It looks like it should work on features, because it turns words into numbers and that is what you want. Two problems. It handles one column at a time, so you end up in a loop. And it has no equivalent of `handle_unknown="ignore"` at all, so an unseen value is always a crash. Use `OrdinalEncoder` for genuine ladders and `OneHotEncoder` for everything else.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| The arithmetic goes too fast and the student is copying rather than computing | You know the answer, so you write it as you say it. Twenty seconds of your time is four minutes of theirs. | **Never write a number they have not said first.** Ask, wait, then write. If they are quiet for eight seconds, that is a normal amount of thinking and you should let it run. |
| They get lost between "the squares" and "the standard deviation" | Five steps is one too many to hold in the head unlabelled. | Number the five steps **on the board** — 1 subtract, 2 square, 3 add, 4 divide, 5 square-root — and point at the number you are on. Leave the list up all lesson. |
| The hand answer and sklearn's answer disagree, and the student concludes the maths was pointless | Almost always they rounded 38.0526 to 38.05 before dividing, so they are out in the third decimal. | Do not fix it for them. Ask: "which of the five steps could give a small error rather than a big one?" This is a two-minute detour and it teaches something real about rounding. |
| "Min-max is better because 0 to 1 is neater" survives the whole lesson | Tidiness is genuinely persuasive, and 0.0000 to 1.0000 looks like a proper answer. | Do not argue. Make them read the four numbers out loud: "zero, nought point oh two, nought point oh four, nought point oh six." Then ask whether 2 and 8 are nearly the same number. The comparison wins where the argument does not. |
| The one-hot activity turns into a discussion about restaurants | The cards are physical and fun and five names are five stories. | Timebox it. Three rows, then the count, then `PopUpPizza`. The count — one column became five — is the objective, not the cards. |
| The ordinal trap lands as "ordinal encoding is bad" rather than "ordinal encoding invents an order" | "Bad" is easier to remember than a conditional. | Force the counter-example out of them: name one column where ordinal encoding is *right*. T-shirt sizes. Star ratings. Education levels. A student who cannot produce one has learned a rule instead of an idea. |
| The whole lesson becomes about scikit-learn syntax | There are four new pieces of syntax and they are the visible part. | The board work comes **first** and is longer than the coding. If you find yourself thirty minutes in with nothing on the board, restart the segment. The syntax is fifteen minutes of typing; the arithmetic is the year. |

---

## 🧭 Differentiation

This section says what to change when the student is struggling, flying or not engaging.

### If the student is struggling

**Cut, in this order:** the min-max half of the live-code (they can read the output from the printed page); the `PopUpPizza` card; and the whole ordinal-ladder table in section 6, replaced by the single sentence *"numbering restaurants tells the model Napoli is twice GreenLeaf, and it isn't."*

**The version of the maths that skips the algebra.** Do not use the word "deviation", do not write a formula, and use `[3, 5, 7, 9, 11]` instead of the monster list. Five instructions, one at a time, each one finished before the next is given:

> 1. "Add them up. Divide by five." → 7
> 2. "How far is each one from 7? Write five numbers." → −4, −2, 0, 2, 4
> 3. "Times each one by itself." → 16, 4, 0, 4, 16
> 4. "Add those up. Divide by five." → 8
> 5. "Square root." → 2.8284

Then one z-score only: *"3 minus 7 is minus 4. Minus 4 divided by 2.8284 is minus 1.4142. So 3 is about one and a half typical steps below average."* One value, said in English. That is objective 1 and half of objective 2, and it is plenty.

**The copy-this-exactly scaffold.** Give them this on paper, with the blanks:

```text
my numbers:   ____  ____  ____  ____  ____
add them up:  ____          divide by 5:  ____   <- the mean
distance from the mean:  ____  ____  ____  ____  ____
times each by itself:    ____  ____  ____  ____  ____
add those up:  ____       divide by 5:  ____
square root:   ____                            <- the typical gap

z-score of the first one:  ( ____  −  ____ )  ÷  ____  =  ____
```

Filling that sheet in is a complete, correct standard deviation and z-score, and a student who can fill it in twice has the objective.

### If the student is flying

None of these needs syntax from a later week.

1. **Variation-harder 2** — remove the 100 and rescale `2, 4, 6, 8`. Min-max now looks better than the z-score. **Why?** Nothing about the recipes changed. This is the best question available today.
2. **Variation-harder 1** — add a sixth value equal to the mean and predict both statistics before checking. Getting "mean unchanged, sd falls" right, *with the reason*, is a level-5 answer.
3. **Prove the promise.** After standardizing, print `z.mean()` and `z.std()`. They come out `0.0` and `1.0` for every column, always. Then ask: is that a coincidence or is it forced by the recipe? (Forced. Follow the arithmetic.)
4. **The uneven-rung question** from the Questions section, with the real weather numbers: 0.1056 against 0.1853. Have them write the two-camp argument in three sentences and pick a side. Then keep the page for Week 5.
5. **Compute the two AUCs.** `LogisticRegression` on ordinal-coded `restaurant` gives about 0.536 on the Week 3 validation pile (the same split as `train_pipeline.py`); on one-hot it gives about 0.541. Both are barely better than guessing, and the 0.005 gap is well inside the noise of a 400-row pile, so it is a good moment to ask whether the difference is real (on the test pile the order flips). A student who can run that comparison unaided and say that out loud is ready for next week.
6. **The honest question:** the mean and the standard deviation are two numbers that summarise 1,200 rows. What can they *not* tell you? (That the column has two humps. That it has a hole in it. That one value is 100. All three matter, and all three are invisible in a mean.)

### If the student won't engage today

**Close the laptop. One calculator, one sheet of graph paper, five index cards.**

Better still, **let them choose the five numbers** — with one condition: four of them must be small and one must be enormous. Their five numbers. Their monster.

Then three instructions and nothing else:

> **"Mark your five numbers on a line from zero to your biggest one."**
>
> **"Work out the average and mark it. Is it in the middle?"**
>
> **"Take away the smallest, divide by the range, and mark those five on a new line from 0 to 1. Where did four of them go?"**

Whatever they say, follow with: *"so are those four numbers actually nearly the same?"*

That is objective 2 in ten minutes with a pencil, and it is the half of the lesson that Weeks 5, 6 and 7 sit on. The z-score can wait a day; the picture of four values crushed against a wall cannot be un-seen.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the five steps, spoken (60 seconds)**

> "I give you the numbers **10, 20 and 60**. Talk me through getting the standard deviation. You don't have to finish the arithmetic — I want the five steps in order."

*Good answer:* "Add them and divide by three, that's 30. Find how far each is from 30: minus 20, minus 10, plus 30. Square them: 400, 100, 900. Add: 1400. Divide by 3. Square root."

**What to catch:** stopping at "divide by 3" and calling that the standard deviation. Push once: *"you squared everything in step three — is that answer in the right units?"* (For the record, 1400 ÷ 3 = 466.67 and the square root is 21.6025.)

**Check 2 — the two rulers, spoken (60 seconds)**

> "A column has ninety-nine values between 1 and 10, and one value of 5,000. **Which scaling would you use, and what goes wrong if you use the other one?**"

*Good answer:* "The z-score. Min-max would divide by a range of about 4,999, so all ninety-nine of the normal values land within about 0.002 of zero and become indistinguishable."

**Full marks needs the consequence named**, not just the choice. A student who says "z-score because it's the default" is a level-2 answer; push: *"what actually happens to the other ninety-nine values?"*

**Check 3 — the false ladder, written, one sentence (90 seconds)**

> "Somebody encodes `weather` as clear=0, rain=1, storm=2. **Write me one sentence saying something the model now believes that is not true.**"

*Good answer:* "It believes the jump from rain to storm is exactly the same size as the jump from clear to rain — and it isn't: clear to rain is 0.1056 and rain to storm is 0.1853, so the second jump is nearly twice the first."

**What to catch:** "it believes storm is worse than rain." That *is* true, and it is the thing ordinal encoding gets right. Push: *"that bit's fine — what's it wrong about?"* The answer is always about the **spacing**, never the order.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot get the mean without help. Confuses the squares with the standard deviation. Reads scaling as "making numbers smaller". Thinks one-hot and ordinal are the same thing with different names. |
| **2 — Emerging** | Computes a standard deviation with the five steps written in front of them. Applies both scalings when told which. Can say one-hot makes one column per value. Does not yet know why anyone would choose one ruler over the other. |
| **3 — Secure** | Works the standard deviation of five numbers unaided and checks it against `scaler.scale_`. Scales both ways and **states which they would use and why, naming the freak value**. One-hots five categories and counts the new columns. Says ordinal encoding invents an order. **This is the target.** |
| **4 — Strong** | Predicts that a new large value escapes the min-max box before running it. Explains `handle_unknown="ignore"` as an outage they are preventing, not a setting. Produces a column where ordinal encoding is *correct*, unprompted. Notices that `-0.473` and −0.4730 are the same number. |
| **5 — Exceptional** | Explains why averaging the raw distances gives zero every time, and therefore why the squaring is not arbitrary. Notices that removing the 100 makes min-max the better ruler and says the recipes did not change, the data did. Argues both sides of the uneven-rung question using the real 0.1056 and 0.1853 gaps. Says a mean and a standard deviation cannot tell you the column has two humps or a hole in it. |

---

## 📤 Homework to Assign

This section gives the words to use when setting the homework.

The workbook has twelve sections, in this order: ✅ Warm-Up · 🔢 Do the Maths by Hand (M1–M4) · 🔎 Predict the Output (P1–P4) · ✍️ Practice Set A (A1–A6) · ✍️ Practice Set B (B1–B5) · 🐞 Fix the Broken Program · 🧩 Puzzle of the Week · 🤔 Think Deeper (T1–T2) · 🛠️ Build It · 🎨 Draw It · 📊 Self-Check · ✅ Answers. It is far more than one evening, so split it:

- **In class:** **A6** (Fill in the two rulers) and **🎨 Draw It**, because both use the lesson's own numbers `2, 4, 6, 8, 100`.
- **At home, marked:** **🛠️ Build It**. This is the old "three pages" and it is the one you mark.
- **At home, as preparation for Build It:** **🔢 Do the Maths by Hand** (M1–M4). Drills 1–10 in Build It are M1 and M2 again with the machine's answer beside them, so a student who has done M1–M4 finds Build It quick.
- **Later, not assigned tonight:** Warm-Up, Predict the Output, Practice Sets A and B, Fix the Broken Program, Puzzle of the Week, Think Deeper and Self-Check. They are the practice bank for the week after; the Warm-Up is also a good opening for Week 5. Set any of them if the student has time or is flying.

**Say this:**

> "About an hour, and one part of it is the one I'm actually marking. Open the workbook at **Build It**.
>
> **Do the ten drills, by hand, with the machine's answer written beside each one.** The two short columns are **P** and **Q**: five drills each. For each one: the mean, the typical gap, the z-scores, the min-max values. **Show the five steps every time** for drills 2 and 7. I want to see the subtracting, the squaring, the adding, the dividing and the square root — not just the answer. Then run `drills.py` and write what the machine said **next to** what you said. If they disagree, don't cross yours out — write which of the five steps went wrong. If you want practice first, the **Do the Maths by Hand** page has the same arithmetic with the blanks laid out for you.
>
> **Then the one-hot by hand.** Take the five restaurants, one-hot three rows of them on paper, and then count: how many columns did you create for `restaurant`, for `day_of_week`, and for `weather`? Write the sum. Then one sentence: **what does `handle_unknown="ignore"` save you from?** I want the sentence to mention something that happens in the real world, not something that happens in Python.
>
> **And last, the marked one: the ordinal trap.** Encode `weather` as clear=0, rain=1, storm=2. Then **two sentences on exactly what the model now wrongly believes about rain.** Two sentences, and I want a number in at least one of them. The real lateness rates are on the page: clear 0.2451, rain 0.3507, storm 0.5360. Do the two subtractions before you write.
>
> The thing I am *not* looking for is 'ordinal encoding is bad'. It isn't. At the bottom of that page there is also a column where ordinal encoding is the right answer, and I want you to name it and write the ladder with less-than signs. Finish with two lines in the Bug Log, one loud and one silent."

**Workbook sections:** **A6 and Draw It** in class · **Build It** (marked) and **Do the Maths by Hand** at home.

**Expected time:** 15 min on M1–M4 if they do them first (the arithmetic is the slow part) · 25 min on the ten drills · 10 min running `drills.py` and writing it up · 10 min on the one-hot page · 15 min on the ordinal trap, including the two subtractions. **About 60 minutes for Build It alone with a quick pass over M1–M4; allow 75 if M1–M4 are done properly.**

> **🧑‍🏫 What to look for when you mark it:** three things, and the third is the real one. **One — are the five steps shown, or only the answers?** A page with `sd = 36.0056` and nothing else did not do the homework, however right the number is. **Two — is the sklearn output written beside the hand answer, or on a separate page?** Beside. The comparison is the point. **Three — do the two sentences on the ordinal-trap part of Build It talk about the *spacing* of the codes, or only the order?** The order is fine. Ordinal encoding gets weather's order right. The wrong belief is that the gap from rain to storm is the same size as the gap from clear to rain, and the numbers 0.1056 and 0.1853 say it is not. A sentence about order only has spotted the easy half and missed the lesson.

---

## 🔑 Answer Key

The key follows the workbook **section by section, in the workbook's own order**, using the workbook's item labels (W1, M1, P1, A1, B1, Bug 1, T1 and so on). Every item is answered, and the values are the ones in the workbook's own ✅ Answers section. Teacher-only notes (what wrong answers look like, what to credit) are marked 🧑‍🏫. **All code below was run; all output is real** — except where marked, the values that come from the 2,000-row delivery table are taken from the workbook's answers and agree with the lateness rates used throughout this guide.

### ✅ Warm-Up

- **W1.** **The model must be last.** Everything before it must have a `.transform`, and the model does not. Put it first and `.fit` raises a `TypeError`, because the pipeline tries to transform with something that cannot transform.
- **W2.** 5 number columns → **5** · 5 + 7 + 3 = **15** · total **20**. Scaling changes values, not width; the three word columns became fifteen.
- **W3.** **The fitted thing.** Not the code (that is in the `.py` files), not the score (a number in a report): 5002 bytes of learned numbers — medians, means, standard deviations, category lists and weights.
- **W4.** Any two of `fit(`, `make_data`, `train_test`. Three zeros means no training code got into the prediction program.
- **W5.** A score without its baseline is not a result. Printed by one script, nobody can quote 0.7541 and forget 0.5000.

### 🔢 Do the Maths by Hand

**M1 — column P = `[3, 5, 7, 9, 11]`.**

```text
3 + 5 + 7 + 9 + 11 = 35        35 ÷ 5 = 7

subtract 7:   −4    −2     0     2     4
square:       16     4     0     4    16
add:          16 + 4 + 0 + 4 + 16 = 40
divide by 5:  40 ÷ 5 = 8
square root:  √8 = 2.8284
```

- z of 3 = (3 − 7) ÷ 2.8284 = **−1.4142**; z of 11 = (11 − 7) ÷ 2.8284 = **+1.4142**.
- **M1(a).** Yes, equal and opposite, **because this list is symmetric about its mean** (no monster in it).
- **Step 4.** min 3, max 11, range 8. (5 − 3) ÷ 8 = 2 ÷ 8 = **0.2500**.
- **M1(b).** **0, 0.25, 0.5, 0.75, 1.** Evenly spaced inputs give evenly spaced outputs.
- **M1(c).** **Min-max** gives the nicer-looking numbers here. Nothing about the recipes changes between P and Q, only the data.

**M2 — column Q = `[1, 2, 2, 3, 92]`.**

```text
1 + 2 + 2 + 3 + 92 = 100       100 ÷ 5 = 20

subtract 20:  −19   −18   −18   −17   +72
square:       361   324   324   289  5184
add:          361 + 324 + 324 + 289 + 5184 = 6482
divide by 5:  6482 ÷ 5 = 1296.4
square root:  √1296.4 = 36.0056
```

- **Step 3.** z of 92 = (92 − 20) ÷ 36.0056 = 72 ÷ 36.0056 = **+1.9997**.
- **Step 4.** min 1, max 92, range 91. (2 − 1) ÷ 91 = 1 ÷ 91 = **0.0110**.
- **Step 5.** z: (120 − 20) ÷ 36.0056 = 100 ÷ 36.0056 = **2.7773**. Min-max: (120 − 1) ÷ 91 = 119 ÷ 91 = **1.3077**.
- **M2(a).** **The min-max answer, 1.3077.** The promise was "every value comes out between 0 and 1"; it breaks the first time a value bigger than anything in training arrives, with **no error and no warning**. The z-score never promised a limit; 2.7773 says "120 sits 2.78 typical steps above average", which is true and comparable with any other column.
- **M2(b).** **One value changed** (11 became 92), and that one number moved the mean from 7 to 20, the typical gap from 2.8284 to 36.0056 and the min-max range from 8 to 91, so the four small values collapse into the bottom 2.2% of the ruler. Neither recipe changed.

**M3 — months against years.**

```text
MONTHS 0, 12, 24, 36, 48
mean = 120 ÷ 5 = 24
squares: 576 + 144 + 0 + 144 + 576 = 1440
1440 ÷ 5 = 288        √288 = 16.9706
z of 48 = (48 − 24) ÷ 16.9706 = +1.4142

YEARS 0, 1, 2, 3, 4
mean = 10 ÷ 5 = 2
squares: 4 + 1 + 0 + 1 + 4 = 10
10 ÷ 5 = 2            √2 = 1.4142
z of 4 = (4 − 2) ÷ 1.4142 = +1.4142
```

- **M3(a).** The two sets of z-scores are **identical, digit for digit**.
- **M3(b).** After standardizing they are **exactly the same column** (mean 0, typical step 1, same five values).
- **M3(c).** "...immune to **the unit somebody happened to choose when they wrote the data down.**" Dividing every value by 12 divides the mean and the typical gap by 12 as well, and the division cancels.
- 🧑‍🏫 The workbook's confirming code prints `mean_ [24.]  scale_ [16.9706]` for months and `mean_ [2.]  scale_ [1.4142]` for years, with z `[-1.4142 -0.7071  0.  0.7071  1.4142]` on both rows.

**M4 — the uneven ladder.**

```text
rain  − clear = 0.3507 − 0.2451 = 0.1056
storm − rain  = 0.5360 − 0.3507 = 0.1853
0.1853 ÷ 0.1056 = 1.75
```

- **M4(a).** The **order** → **right**. The **spacing** → **wrong**: codes 0, 1, 2 say the two steps are equal, and the second is **1.75 times** the first.
- **M4(b).** `restaurant` 5 → 5 · `day_of_week` 7 → 7 · `weather` 3 → 3 · **total 15**.
- **M4(c).** Three leave and **fifteen** arrive. **The row count is not affected** — one-hot changes the width, never the height.

### 🔎 Predict the Output

**P1 — every value the same.** By hand: mean **5**, every distance **0**, every square **0**, so sd = **0**.

```text
mean_ : [5.]
scale_: [1.]
z     : [0. 0. 0. 0.]
```

`scale_` is **1, not 0**: sklearn noticed the standard deviation was zero and quietly replaced it with 1, because the next step divides by it and dividing by zero would turn every row into `nan`. 🧑‍🏫 A constant column carries no information; the real fix is to notice it and drop it.

**P2 — one capital letter.**

```text
['weather_Storm' 'weather_clear' 'weather_rain']
(4, 3)
[[0 1 0]
 [0 0 0]
 [0 0 1]
 [0 1 0]]
```

Names: `weather_Storm`, `weather_clear`, `weather_rain` — the capital sorts first. Shape **(4, 3)**, and **three** 1s in the grid. **Row 2 (the second row, `"storm"`) is all zeros**: it asked for `"storm"` with a small s, the encoder learned `"Storm"`, and the two are different strings, so `handle_unknown="ignore"` turned it into zeros with no error. **The check:** `print(out.sum(axis=1))` should be 1 on every row; here it prints `[1. 0. 1. 1.]`. A row summing to 0 is a category the encoder has never met. (Also acceptable: `print(sorted(later["weather"].unique()), sorted(train["weather"].unique()))`.)

**P3 — the ladder nobody told it about.**

```text
categories_: [array(['large', 'medium', 'small'], dtype=object)]
codes      : [2 1 0 1 2]
```

Sorted alphabetically, so `large` = 0 and `small` = 2. The model believes **small is bigger than large**, by two whole steps, with medium between them. **The fix:** `oe = OrdinalEncoder(categories=[["small", "medium", "large"]])` — a list **inside** a list.

**P4 — the shape prediction on the real table.**

```text
in shape : (2000, 3)
out shape: (2000, 15)
sum of every row: {3.0}
sum of the whole grid: 6000
```

The row sum is **3** because there are three one-hot blocks side by side and each contributes one 1. Grid total: **2000 × 3 = 6000**. The "How many did you get right ___ / 14" line is the student's own count (there are 14 predictions on the page); it has no answer.

🧑‍🏫 Wrong-answer map: a student who writes `sum of every row: {1.0}` has applied "one 1 per row" to the whole grid instead of to one encoded column. A student who writes `(2000, 5)` for out shape forgot that all three columns are encoded.

### ✍️ Practice Set A — Read It

**A1.** standardization → **(iii)** · min-max → **(v)** · one-hot → **(i)** · ordinal → **(iv)** · cardinality → **(ii)**.

**A2.**

| Line | Result |
|---|---|
| `X.shape` | **(5, 1)** |
| `ss.transform(X).shape` | **(5, 1)** |
| `ss.transform(X).ravel().shape` | **(5,)** |
| `ohe.fit_transform(df[["restaurant"]]).shape` | **(2000, 5)** |
| `ohe.fit_transform(df[CAT]).shape` | **(2000, 15)** |
| `oe.fit_transform(df[["weather"]]).shape` | **(2000, 1)** |

- **A2(a).** The third one, **(5,)**, has one number in it: `.ravel()` flattened the one-column table into a flat row, which has only a length. (Fine for printing, not fine to hand back to sklearn.) 🧑‍🏫 The workbook asks for "two of those six"; the only one-number shape is `(5,)`, and `(2000, 1)` has a 1 as its second number. Credit a student who names `(5,)` and explains it, and one who also names `(2000, 1)` as "one column".
- **A2(b).** **15** and **1**, because one-hot makes one column per value and ordinal makes one column, full stop — and that one column carries the extra claim that the values are in order and evenly spaced.

**A3.**

| # | What happens | The fix |
|---|---|---|
| a | `ValueError: Expected 2D array, got 1D array instead` | `x.reshape(-1, 1)` |
| b | `ValueError: Expected a 2-dimensional container but got <class 'pandas.core.series.Series'> instead.` | double brackets: `df[["distance_km"]]` |
| c | `AttributeError: 'StandardScaler' object has no attribute 'mean_'` | call `.fit(X)` first |
| d | **no error** — it prints `(0, 0)  1.0` and so on, a list of coordinates | add `sparse_output=False` while learning |
| e | `ValueError: Shape mismatch: if categories is an array, it has to be of shape (n_features,).` | list **inside** a list: `categories=[["clear", "rain", "storm"]]` |
| f | `ValueError: could not convert string to float: 'clear'` | send word columns down the categorical branch |

- **A3(g).** **(d).** It returns a *sparse* matrix, which stores only the non-zero cells and prints as coordinates: `(0, 0)  1.0`, `(1, 1)  1.0`, `(2, 1)  1.0`. Not a bug, and what you want inside a pipeline, but useless while you are learning.
- **A3(h).** **(a) and (b).** Both hand a **flat row** to something that wants a **table**: `reshape(-1, 1)` for numpy, double brackets for a DataFrame.
- 🧑‍🏫 Related, worth knowing: `categories=[["clear", "rain"]]` on a column that also contains `storm` gives `Found unknown categories ['storm'] in column 0 during fit` — **during fit**, because the list was incomplete from the start.

**A4.** i → **S** · ii → **R** · iii → **Q** · iv → **T** · v → **P**.

- **A4(a).** **Q, `[91.]`**, is the number min-max divides by (the range, 92 − 1). **P, `[1.3077]`**, could only have come from min-max, because it is outside 0 to 1 and the z-score makes no such promise. (`[36.0056]` is the z-score's divisor; 91 and 36.0056 are two different answers to "what do I divide by?" on the same column.)
- **A4(b).** **Down.** With 120 in the training data the mean rises from 20 to about 36.7 and the typical gap rises too, so 120 is fewer typical steps above a higher average (1.6770 against 2.7773). A z-score is always a statement about the company a value keeps.

**A5.**

- **Report A — `distance_km`: standardize.** The deciding number is **448 of 2000** min-max values below 0.10, with a biggest z of +4.7435 showing the long tail that caused it.
- **Report B — `items`: arguable; min-max is defensible.** *"A basket holds 1 to 6 items, the limits are real limits rather than the biggest thing I happened to see, and the biggest z is only +1.4159, so there is no monster to crush anybody."*
- **Report C — `pixel_brightness`: min-max, honestly.** *"Brightness is 0 to 255 **by definition**, so nothing bigger can ever arrive."* (The other honest reason: something later in the program demands 0 to 1.)
- **Report D — `monthly_pay`: the worst candidate for min-max.** The two numbers are the biggest z of **+4.9811** and **487 of 2000** below 0.10: a handful of large salaries own the range and everybody else shares the bottom.
- **A5(a).** **Report C.** Its 0 and 255 come from what a pixel *is*; the others' limits (0.33 and 14.40, 1 and 6, 617 and 9033) come from whatever turned up in 2,000 training rows. Min-max's promise only holds inside the range it saw: real limits mean it holds for ever, accidental ones mean it holds until next Tuesday. (Report B sits in between, which is why it is arguable.)

**A6 — Fill in the two rulers** (`2, 4, 6, 8, 100`). This is the in-class check; it is the same material as the graph-paper activity key further down.

```text
the five numbers      2   4   6   8   100
sum 120,  mean 120 ÷ 5 = 24

1  subtract 24:   −22    −20    −18    −16    +76
2  square:        484    400    324    256   5776
3  add:           7240
4  divide by 5:   1448
5  square root:   38.0526

z-score of 8 :  ( 8 − 24 ) ÷ 38.0526 = −0.4205
min-max of 8 :  ( 8 −  2 ) ÷ 98      =  0.0612

a new value of 150:  z = 3.3112     min-max = 1.5102
min-max values under 0.10:  4  (0.0000, 0.0204, 0.0408, 0.0612)
one-hot restaurant + day_of_week + weather:  15 columns
```

- **A6(a).** The student's own list of wrong boxes; use the figure above to mark. Any wrong box is worth tracing back to which of the five steps went wrong.
- **A6(b).** **The `4`** (min-max values under 0.10) and **the `15`** (one-hot columns) are counts of things rather than measurements.

### ✍️ Practice Set B — Write It

**B1.** The blanks are `reshape(-1, 1)`, `StandardScaler().fit(Q)` and `round(ss.scale_[0], 4)`. Output: `Q typical gap: 36.0056`. `scale_` is an array with one number in it, so `scale_[0]` gets the number out; without `[0]` it prints `[36.0056]`, which is not wrong, just noisier.

**B2.** The blanks, in order:

```text
n = len(values)
total = total + v
mean = total / n
squares = squares + (v - mean) * (v - mean)
sd = (squares / n) ** 0.5
zs.append(round((v - mean) / sd, 4))
```

Expected output: for `[3, 5, 7, 9, 11]`, mean 7.0, sd 2.8284, z `[-1.4142, -0.7071, 0.0, 0.7071, 1.4142]`; for `[1, 2, 2, 3, 92]`, mean 20.0, sd 36.0056, z `[-0.5277, -0.4999, -0.4999, -0.4721, 1.9997]`; sklearn's two lines match the by-hand lines exactly. 🧑‍🏫 `sd` must be computed from the **unrounded** `squares / n`; rounding before the square root breaks the fourth decimal place.

- **B2(a).** **Dividing by `n`** matches sklearn (`n − 1` gives 3.1623 for P). `StandardScaler` divides by `n`, so the course does too.

**B3.** The program loops over `[("P", [3, 5, 7, 9, 11]), ("Q", [1, 2, 2, 3, 92])]`, fits a `StandardScaler` and a `MinMaxScaler` on each `reshape(-1, 1)` column, and then tests 120 on Q. Expected output:

```text
--- column P ---
  scaler.mean_  [7.]  scaler.scale_ [2.82842712]
  z             [-1.4142 -0.7071  0.      0.7071  1.4142]
  min-max       [0.   0.25 0.5  0.75 1.  ]
--- column Q ---
  scaler.mean_  [20.]  scaler.scale_ [36.00555513]
  z             [-0.5277 -0.4999 -0.4999 -0.4721  1.9997]
  min-max       [0.    0.011 0.011 0.022 1.   ]

new value 120 for Q:
  z       [2.7773]
  min-max [1.3077]
```

🧑‍🏫 Marking note: column P is the tidy one — min-max gives 0, 0.25, 0.5, 0.75, 1 and looks *better* than the z-scores. Column Q is the same list with a monster in it, and min-max collapses to 0, 0.011, 0.011, 0.022, 1. **A student who notices that the two columns disagree about which ruler is nicer has understood the week.** Give credit even if they did not write it as a question.

**B4.** Expected output: cardinalities **5, 7, 3**; `in shape : (2000, 3)`; `out shape: (2000, 15)`; `5 + 7 + 3 = 15`; and the 15 names grouped by column and alphabetical inside each group (`restaurant_CrustyBros`, `restaurant_GreenLeaf`, `restaurant_Napoli`, `restaurant_SliceHouse`, `restaurant_TandooriPizza`, `day_of_week_Fri`, `day_of_week_Mon`, `day_of_week_Sat`, `day_of_week_Sun`, `day_of_week_Thu`, `day_of_week_Tue`, `day_of_week_Wed`, `weather_clear`, `weather_rain`, `weather_storm`).

- **B4(a).** **The days of the week:** `Fri, Mon, Sat, Sun, Thu, Tue, Wed` — alphabetical, not Monday-to-Sunday. (A small argument for one-hot over a bare `OrdinalEncoder()` on `day_of_week`, which would code Friday as day zero.)

**B5.** Expected output:

```text
column              mean_    scale_       min       max
distance_km        3.5193    2.2938      0.33     14.40
items              3.5520    1.7290      1.00      6.00
prep_minutes      14.0658    4.0002      4.00     26.60
order_hour        16.7885    3.6022     10.00     23.00

one new value per column, arriving at prediction time:
distance_km        5.00  ->  z +0.6455   min-max  +0.3319   inside
items              8.00  ->  z +2.5726   min-max  +1.4000   ESCAPED THE BOX
prep_minutes      30.00  ->  z +3.9833   min-max  +1.1504   ESCAPED THE BOX
order_hour         9.00  ->  z -2.1622   min-max  -0.0769   ESCAPED THE BOX
```

The program needs two loops, an `if m < 0 or m > 1` deciding `inside` or `ESCAPED THE BOX`, and `pd.DataFrame({col: [value]})` for each new value (a bare `[[value]]` works but prints `UserWarning: X does not have valid feature names`).

- **B5(a).** **`order_hour`, with −0.0769.** The recipe is `(value − data_min_) ÷ range`; a value below the smallest training value makes the top negative. Nobody ordered before 10 in these rows, so `data_min_` is 10 and (9 − 10) ÷ 13 = −0.0769. Min-max escapes at both ends.
- **B5(b).**

```text
z      : (5.00 − 3.5193) ÷ 2.2938 = 1.4807 ÷ 2.2938 = 0.6455
min-max: (5.00 − 0.33)   ÷ 14.07  = 4.67   ÷ 14.07  = 0.3319
```

### 🐞 Fix the Broken Program

- **Bug 1.** Line **10** (`ss = StandardScaler().fit(price)`). Kind: **shape bug.** Use `reshape(-1, 1)`, because the five prices are **five examples of one thing**; `reshape(1, -1)` says "one example with five features". **The fix:** `ss = StandardScaler().fit(price.reshape(-1, 1))`. **Line 15 already does it right** (`mm = MinMaxScaler().fit(price.reshape(-1, 1))`): the answer was already in the file, so look for the same operation done correctly elsewhere before searching the internet.
- **Bug 2.** Line **21** (`ohe.transform(... "teal" ...)`). Kind: **runtime** (`ValueError` at transform time). *During fit* means the problem is in training data you can look at; **during transform means it arrived after the model was built and shipped** — a real customer's order and a shop that opened last week. **The fix:** `ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False).fit(colour)`.
- **The arithmetic check in Run 2:**

```text
8 + 10 + 12 + 14 + 96 = 140        140 ÷ 5 = 28     (matches mean_ [28.]  yes)
squares: 400 + 324 + 256 + 196 + 4624 = 5800
5800 ÷ 5 = 1160        √1160 = 34.0588            (matches scale_ [34.05877273]  yes)
min-max of 10: (10 − 8) ÷ (96 − 8) = 2 ÷ 88 = 0.0227
```

- **The consistency check on the Run 3 table.** **Yes** — both `small` rows say 2 and both `medium` rows say 1. Worth checking because a wrong-but-consistent mapping is a bug in your *instructions*, and a wrong-and-inconsistent one is a bug in your *data*; they need different fixes.
- **Bug 3.** Line **28** (`oe = OrdinalEncoder()`). Kind: **silent logic.** The model now believes **`small` is two rungs above `large`** (alphabetical: `large` < `medium` < `small`). **The fix:** `oe = OrdinalEncoder(categories=[["small", "medium", "large"]])`. After the fix: small → **0**, medium → **1**, large → **2**.
- **The decision the library filled in:** bug 1 — *is this five examples of one thing or one example of five things?* (sklearn refused, which is the friendliest outcome); bug 2 — *what to do with a value never seen* (default: stop); bug 3 — *what order the categories are in* (default: alphabetical, silently).
- **Easiest → hardest: 1, 2, 3.** Bug 1 fails on the first line that does any work; bug 2 fails only if the program happens to try an unseen colour (otherwise it ships and fails in production); bug 3 is caught only by reading the printed codes against the ladder you meant — not by the error log, the score or the shape.
- 🧑‍🏫 Line numbers are those in the printed `broken04.py`; a student who writes the right line but an adjacent number has counted the docstring differently, so accept the right statement.

### 🧩 Puzzle of the Week

| # | Which ruler? | The clue |
|---|---|---|
| 1 | **min-max** | exactly one `0` and exactly one `1` |
| 2 | **z-score** | adds up to 0, and there are negatives |
| 3 | **min-max** | one `0`, one `1`, everybody else crushed near the bottom |
| 4 | **z-score** | negatives that sum to 0 (−0.5277 − 0.4999 − 0.4999 − 0.4721 + 1.9997 = 0.0001, rounding) |
| 5 | **cannot tell** | both rulers give all zeros for a constant column |

- **Part 1(a).** **Min-max always contains** a `0` (the smallest training value) **and a `1`** (the biggest), and never a negative unless a value from outside the training range was pushed through it. **z-scores always add up to 0** across the column they were fitted on (and their standard deviation is 1).
- **Part 1(b).** **Number 5.** A constant column has sd 0 and range 0, sklearn replaces both with 1, and both rulers return zeros. You would have to be told which scaler was used, or be shown `data_min_`/`data_max_` versus `mean_`/`scale_`. The useful reaction is "why is there a constant column at all?"
- **Part 1(c).** **Printouts 3 and 4** came from the monster column (Q). In 3, four of five values are jammed into the bottom 2.2% of the ruler; in 4, four z-scores bunch near −0.5 while one sits at +2.0. Printouts 1 and 2 are evenly spread.
- **Part 2.**

```text
raw = mean + z × sd

50 + (−2.50 × 8) = 50 − 20 = 30
50 + ( 0.00 × 8) = 50 +  0 = 50
50 + ( 1.25 × 8) = 50 + 10 = 60
```

- **Part 2(a).** `data_min_` = **30**, `data_max_` = **60**.
- **Part 2(b).** (50 − 30) ÷ 30 = **20 ÷ 30 = 0.6667** (not 0.5, because 30, 50, 60 are not evenly spaced).
- **Part 2(c).** **Both** can be run backwards: `raw = mean_ + z × scale_` and `raw = data_min_ + m × (data_max_ − data_min_)`. Each needs exactly its own two learned numbers, which is what the 5002-byte artifact from Week 3 holds. A scaled column is not anonymous. 🧑‍🏫 The question wording invites "only one can"; the workbook's answer is that both can, and that is the one to mark against.

### 🤔 Think Deeper

🧑‍🏫 Open-ended; mark on reasoning, not on wording.

- **T1.** A strong answer separates two claims. "The score went up" is about one 400-row validation pile on one Tuesday, and a delta of 0.0009 can flip sign on a re-split. "The answer no longer depends on a unit somebody chose" is about the structure of the model, true before you measure anything (dividing by 12 divides the mean and the typical gap by 12, and they cancel). The second reason is stronger. To the student who wants to remove the scaler for a 0.0009 drop: **0.0009 on 400 rows is not a finding**, and keeping the scaler costs one line in a `Pipeline` while buying immunity to a class of bug and readable weights. Best answers add the honest exception: a decision tree does not care, so on a tree the argument is only readability.
- **T2.** The strongest answers refuse to make it a rule. Case for five zeros: a service that stops answering because a shop opened is worse than one that is slightly vaguer. Case for the crash: if the unknown column carries most of the prediction, five zeros is a confident guess with nothing behind it, and stopping is honest (medicine, money). The best answers land on "it depends on how much of the prediction that column was carrying and on what the receiver is told", and say the receiver should be able to find out that this restaurant was never seen — which is what heading 7 of the Week 3 model card is for.

### 🛠️ Build It — Ten Drills, Five Cards, One Trap

This is the homework being marked. **Step 1 check:** the first `order_id` must be 100955.

**The ten drills.**

| Drill | What | Answer |
|---|---|---|
| 1 | mean of P | **7** |
| 2 | sd of P | **2.8284** |
| 3 | z of 3 | **−1.4142** |
| 4 | z of 11 | **+1.4142** |
| 5 | min-max of 5 | **0.2500** |
| 6 | mean of Q | **20** |
| 7 | sd of Q | **36.0056** |
| 8 | z of 92 | **+1.9997** |
| 9 | min-max of 2 | **0.0110** |
| 10 | 120: z and min-max | **2.7773** and **1.3077** |

**The five steps for drill 2:** subtract −4 −2 0 2 4 · square 16 4 0 4 16 · add 40 · divide 40 ÷ 5 = 8 · root √8 = 2.8284.

**The five steps for drill 7:** subtract −19 −18 −18 −17 +72 · square 361 324 324 289 5184 · add 6482 · divide 6482 ÷ 5 = 1296.4 · root √1296.4 = 36.0056.

🧑‍🏫 **The commonest disagreement is drill 8, and it is always step 5:** rounding 36.0056 to 36.01 before dividing gives 1.9994 instead of 1.9997. "Which drill disagreed, if any" and "which step was guilty" are the student's own; the usual answers are drill 8 and the square-root step. For drill 10 the sklearn column is `[2.7773]` (z) and `[1.3077]` (min-max), as printed by `drills.py`.

**Which ruler, and why.** Full marks for anything of this shape:

> *"For column P I would use min-max, because the five values are evenly spaced with no freak value, so min-max gives a clean 0, 0.25, 0.5, 0.75, 1 and the hard-limits argument is at least arguable. For column Q I would use the z-score, because 92 is a freak value and min-max divides by a range of 91 that only exists because of it, so 1, 2, 2 and 3 land in 0.0000, 0.0110, 0.0110 and 0.0220 — the bottom 2.2% of the ruler — and 2 and 3 become nearly the same number when one is 1.5 times the other."*

The sentence that explains the disagreement: *"Nothing about either recipe changed. Only the data did — 11 became 92 — and that one value moved the range from 8 to 91."* Accept a z-score for P as well if the reason is given; the point is naming the freak value for Q.

**One-hot by hand**, categories sorted alphabetically as sklearn sorts them.

| restaurant | _CrustyBros | _GreenLeaf | _Napoli | _SliceHouse | _TandooriPizza |
|---|---|---|---|---|---|
| Napoli | 0 | 0 | **1** | 0 | 0 |
| CrustyBros | **1** | 0 | 0 | 0 | 0 |
| TandooriPizza | 0 | 0 | 0 | 0 | **1** |

**The check:** **3** ones, **12** zeros, 3 × 5 = **15** cells.

**The column count.**

```text
restaurant   : 5 values  ->  5 columns
day_of_week  : 7 values  ->  7 columns
weather      : 3 values  ->  3 columns
                            ---
                             15 new columns, replacing 3 old ones
```

**What `handle_unknown="ignore"` saves you from — a good sentence:** *"A restaurant opens that wasn't in my training data, and without that setting my saved model throws an exception on a real customer's order instead of giving a slightly worse answer."*

**What to catch:** answers that describe the Python (*"it stops a ValueError"*) rather than the world (*"a new shop opened"*). Both are true; only the second shows they know why anybody cares. The real message, for reference:

```text
ValueError: Found unknown categories ['PopUpPizza'] in column 0 during transform
```

and with the setting on:

```text
PopUpPizza -> [[0 0 0 0 0]]
```

**The sixth restaurant's row:** `0  0  0  0  0`. Not a sixth column: the model was trained with five weights, so a sixth column would have no weight to multiply by.

**The ordinal trap.** Codes: clear **0**, rain **1**, storm **2**.

```python
from sklearn.preprocessing import OrdinalEncoder
import pandas as pd

oe = OrdinalEncoder(categories=[["clear", "rain", "storm"]])
w = pd.DataFrame({"weather": ["clear", "rain", "storm", "rain", "clear"]})
print("weather codes:", oe.fit_transform(w).ravel().astype(int))
```

```text
weather codes: [0 1 2 1 0]
```

**The real lateness rates**, from the delivery table:

```python
from make_data import make_deliveries
df = make_deliveries(n=2000, seed=0)
print(df.groupby("weather")["late"].agg(["size", "mean"]).round(4).to_string())
```

```text
         size    mean
weather              
clear    1416  0.2451
rain      479  0.3507
storm     125  0.5360
```

**The two subtractions.**

```text
rain  − clear = 0.3507 − 0.2451 = 0.1056
storm − rain  = 0.5360 − 0.3507 = 0.1853

0.1853 ÷ 0.1056 = 1.75
```

**The two marked sentences.** Full marks for anything of this shape:

> *"By coding clear 0, rain 1 and storm 2 and giving the model one weight for the whole column, I have told it that going from clear to rain and going from rain to storm are steps of exactly the same size. They are not: the first step costs 0.1056 in lateness and the second costs 0.1853, so the second is 1.75 times the first."*
>
> *"So the model has to split the difference — whatever single weight it picks, it will over-estimate the harm of rain or under-estimate the harm of a storm, and it can never get both right."*

**What to catch:** a sentence about the *order* (*"it thinks storm is worse than rain"*). That is true and ordinal encoding gets it right — weather really is a ladder. The wrong belief is always about the **spacing**.

**The column where ordinal encoding is the right answer.** Any genuine ladder, written out with the less-than signs: t-shirt sizes `XS < S < M < L < XL`; education `none < primary < secondary < bachelor < master < phd`; a 1-to-5 star rating; `cold < warm < hot`. Full marks needs the chain, because that is the test: if you cannot write the chain, it is not a ladder. (The workbook's blank has five slots; a shorter ladder is fine if the chain is real.)

**The Bug Log — two entries, one loud and one silent.** A model pair:

| What I saw | What it means | Cause | Fix |
|---|---|---|---|
| `ValueError: Expected 2D array, got 1D array instead` | I gave a row where a table was wanted | `.fit(x)` on a flat numpy row | `x.reshape(-1, 1)`, or `df[["col"]]` with double brackets |
| Ordinal codes came out `large 0, medium 1, small 2`. **No error at all** | sklearn sorted my categories alphabetically because I never said what order I meant | `OrdinalEncoder()` with no `categories=` | `OrdinalEncoder(categories=[["small", "medium", "large"]])`, and always read the printed codes |

### 🎨 Draw It

The five numbers are `2, 4, 6, 8, 100`, drawn on three number lines (raw, z-score, min-max).

- **Four of the five dots touch each other on line 3**, the min-max line: `0.0000, 0.0204, 0.0408, 0.0612` all sit inside the first 6% of the ruler.
- **The mean is to the right of four of the five dots on line 1** (24, with four values at 8 or less) — the reason the median exists.
- **The order is the same on all three lines.** Scaling is a change of units, not of facts: it never reorders a column. What changes is how big the numbers are that the weights multiply, and so how much each column counts.
- **Rub out the 100 and line 3 changes character completely:** `2, 4, 6, 8` min-maxed becomes `0, 0.3333, 0.6667, 1`, evenly spread and the nicest of the three. Line 2 barely changes shape (z-scores `−1.3416, −0.4472, +0.4472, +1.3416`). Min-max is a recipe one freak value can ruin, and the z-score is not.

### 📊 Self-Check

The student's own faces; nothing is marked. Three rows are worth probing honestly:

- *"say why you square"* — the test is "because averaging the raw distances gives exactly zero, every time, for every list". "To get rid of the minus signs" is half of it.
- *"name a column where ordinal encoding is right"* — "ordinal bad, one-hot good" is a memorised rule. The chain with less-than signs proves the idea.
- *"explain what a trailing underscore means"* — "the machine learned it from data, so it does not exist before `.fit`", and an `AttributeError` on anything ending in `_` has exactly one cause.

The two numbers in the Self-Check rows are the ones already keyed above: a new value of 150 gives **3.3112** (z) and **1.5102** (min-max), and the uneven ladder is **0.1056** and **0.1853**.

### 🎲 The in-class activity key (graph paper, `2, 4, 6, 8, 100`)

This is the key to the Their Turn activity. It is the same arithmetic as A6 and Draw It, and the student checks it against those two workbook sections.

**Predictions asked during the lesson.**

- `StandardScaler().fit(X)` on `[[2],[4],[6],[8],[100]]` prints `[24.]` and `[38.05259518]`.
- z-score of 8: (8 − 24) ÷ 38.0526 = **−0.4205**. Min-max of 8: (8 − 2) ÷ 98 = 6 ÷ 98 = **0.0612**.
- A value of 150 arrives: z = (150 − 24) ÷ 38.0526 = 126 ÷ 38.0526 = **3.3112**; min-max = (150 − 2) ÷ 98 = 148 ÷ 98 = **1.5102**, **outside the 0-to-1 box with no error and no warning**.
- One column of the five restaurant names into `OneHotEncoder`: `(5, 1)` in, `(5, 5)` out. With `handle_unknown="ignore"`, an unseen restaurant gives `[[0 0 0 0 0]]`.

**Mean.** 2 + 4 + 6 + 8 + 100 = 120, and 120 ÷ 5 = **24**.

**Standard deviation, all five steps.**

```text
1  subtract:     −22    −20    −18    −16    +76
2  square:       484    400    324    256    5776
3  add:          484 + 400 + 324 + 256 + 5776 = 7240
4  divide by 5:  7240 ÷ 5 = 1448
5  square root:  38.0526
```

**Z-scores.**

| x | arithmetic | z |
|---|---|---|
| 2 | (2 − 24) ÷ 38.0526 | **−0.5781** |
| 4 | (4 − 24) ÷ 38.0526 | **−0.5256** |
| 6 | (6 − 24) ÷ 38.0526 | **−0.4730** |
| 8 | (8 − 24) ÷ 38.0526 | **−0.4205** |
| 100 | (100 − 24) ÷ 38.0526 | **+1.9972** |

**Min-max**, min 2, max 100, range 98.

| x | arithmetic | value |
|---|---|---|
| 2 | 0 ÷ 98 | **0.0000** |
| 4 | 2 ÷ 98 | **0.0204** |
| 6 | 4 ÷ 98 | **0.0408** |
| 8 | 6 ÷ 98 | **0.0612** |
| 100 | 98 ÷ 98 | **1.0000** |

**The sklearn check.**

```python
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

x = np.array([2, 4, 6, 8, 100], dtype=float)
X = x.reshape(-1, 1)
ss = StandardScaler().fit(X)
print("scaler.mean_ :", ss.mean_)
print("scaler.scale_:", ss.scale_)
print("z-scores     :", np.round(ss.transform(X).ravel(), 4))
mm = MinMaxScaler().fit(X)
print("data_min_    :", mm.data_min_, " data_max_:", mm.data_max_)
print("min-max      :", np.round(mm.transform(X).ravel(), 4))
```

Real output:

```text
scaler.mean_ : [24.]
scaler.scale_: [38.05259518]
z-scores     : [-0.5781 -0.5256 -0.473  -0.4205  1.9972]
data_min_    : [2.] data_max_: [100.]
min-max      : [0.     0.0204 0.0408 0.0612 1.    ]
```

**The judgement sentence.** Full marks for anything with this shape: *"I would standardize this column. The 100 is a freak value, and min-max divides by a range of 98 that only exists because of it, so 2, 4, 6 and 8 all land inside the first 6% of the ruler (0.0000 to 0.0612) and become nearly indistinguishable. The z-score keeps them spread out and gives the 100 a big value of +2.0, which is honest."*

### Every question posed in the lesson

- *"Does the model know that one kilometre is a big deal and one month is almost nothing?"* → No. It only sees that one column's numbers are about four times bigger.
- *"Add them up. Divide by five."* → 120, then **24**.
- *"Is 24 a fair description of those five numbers?"* → No. Four of the five are 8 or below; one value dragged the average.
- *"Average the five distances as they are."* → **Zero**, every time, for every list. That is what a mean is.
- *"Add the five squares. Divide by five. Square root."* → 7240, 1448, **38.0526**.
- *"What are those two lines about to print?"* → 24 and 38.0526 — `[24.]` and `[38.05259518]`.
- *"It says `-0.473` and your board says −0.4730. Is the machine wrong?"* → No. Same number; `np.round` drops a trailing zero.
- *"Which four min-max numbers are nearly the same number?"* → 0.0000, 0.0204, 0.0408, 0.0612 — the whole of 2, 4, 6 and 8 inside 6% of the ruler.
- *"Was 2 nearly the same as 8 in the original list?"* → No, 8 is four times 2.
- *"A new value of 150 arrives. What does min-max give it?"* → **1.5102** — outside the box, silently.
- *"Read me the last line."* → `ValueError: Expected 2D array, got 1D array instead` — and the fix is in the message.
- *"Five restaurants in one column. How many columns come out?"* → Five. `(5, 1)` in, `(5, 5)` out.
- *"Why did they come out CrustyBros first?"* → The encoder sorts the categories alphabetically. It has to pick an order.
- *"Write me PopUpPizza's row."* → `0 0 0 0 0`. There is no sixth column, because there is no sixth weight.
- *"How many columns altogether for restaurant, day and weather?"* → 5 + 7 + 3 = **15**.
- *"Is it true that a storm is two rains?"* → No. The two steps are 0.1056 and 0.1853, and 0.1853 ÷ 0.1056 = 1.75.
- *"Name one column where ordinal encoding is right."* → Any ladder you can write with less-than signs: sizes, star ratings, education levels.
- *"Do either scaling changes reorder the numbers?"* → No. 2 is smallest and 100 is biggest on all three rows of the board.

---

## 🔮 Next Week Preview

Next week the student stops accepting the columns they were given. **Week 5 is about the columns that were not in the file** — and it is the week where the score finally moves.

There are three shapes of invented column, all built out of arithmetic they already have: a **bin** (`order_hour` is useless as a number because lateness is low at 14:00, spikes at 19:00 and drops again at 22:00, so you cut the hours into ranges instead), a **ratio** (`prep_minutes ÷ distance_km` asks a completely different question from either column alone: is the kitchen the bottleneck, or the road?), and an **interaction** (`distance × weather severity`, because a long trip costs you 0.3269 in the clear and 0.4663 in a storm, and no amount of adding two separate weights can express *"worse together"*).

And then the part that makes it engineering rather than guessing: the **ablation**. Build the model with the new column, build it without it, change nothing else, compare on the validation set, and write the difference down to four decimal places. Next week's table has six rows in it, and **two of the four invented columns will turn out to buy nothing at all** — one of them a feature that sounds so sensible nobody wants to delete it. The student will have to delete it anyway, in writing, with the number that justified the deletion. That is the habit the week is really for.

**Prep early:** three things. **Keep this week's `rulers.py` and `encode.py`** — Week 5 puts a `FunctionTransformer` in front of the same `ColumnTransformer` and it helps if the encoding half is already familiar. **Read the ten drills in Build It before the lesson**, because the students who rounded 38.0526 early are the same ones who will read a ΔAUC of −0.0014 as "about the same" — and next week the fourth decimal place is the whole deliverable. And **have graph paper again**: the Invention Round at the start of Week 5 is eight silent minutes of everybody writing down five columns that could exist but do not, and it works far better on paper than on a screen.

---

[⬅ Week 3](week-03.md) · [Course Home](../README.md) · [Week 5 ➡](week-05.md) · [Student Guide](../student-guide/week-04.md) · [Workbook](../workbook/week-04.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)

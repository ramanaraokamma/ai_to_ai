# Module 2 — Feature Engineering: Turning Raw Reality Into Numbers

**Level 3 · Module 2 · ~5 hours · Prereqs: Module 1 (framing, three-way split, Pipeline, joblib artifact, model card).**

[⬅ Previous](module-01-the-supervised-pipeline.md) · [Level 3 Home](README.md) · [Next ➡](module-03-evaluation-metrics.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. You will be able to standardize and min-max scale a column by hand, and say which one you'd pick and why.
2. You will be able to encode categorical columns with one-hot and ordinal encoding, and explain the false-ordering trap that ordinal encoding sets for you.
3. You will be able to derive new features from dates, counts, ratios, bins, and interactions — and run an **ablation** to prove whether each one actually helped.
4. You will be able to impute missing values correctly: statistics learned from training rows only, applied to all rows.
5. You will be able to spot the three flavours of **data leakage** — target, temporal, preprocessing — and fix each one.
6. You will be able to wire mixed numeric and categorical columns through a single `ColumnTransformer` that is impossible to leak through.

---

## 🪝 The Hook

Two teams get the same 2,000 rows of pizza delivery data and the same 24 hours.

Team A downloads a gradient-boosted tree library, tunes 40 **hyperparameters** — settings *you* choose rather than ones the model learns, like `k`, `max_depth`, or the learning rate — overnight on a cloud GPU, and reports validation AUC **0.781**.

Team B uses the same plain logistic regression from Module 1. They spend their whole day looking at the data. They notice that lateness spikes hard between 18:00 and 20:00, so they add one column: `is_rush = 1 if 18 ≤ hour ≤ 20`. They notice that distance hurts much more in a storm than on a clear day, so they add `distance × weather_severity`. Two new columns, four lines of code. They report validation AUC **0.785**.

Team B wins, and they can explain every coefficient to the pizza manager.

Then a third team, Team C, reports **0.978**. Everyone is amazed. Team C has accidentally included a column called `customer_called_support`, which is only ever filled in *after* the delivery arrives late. Team C has not built a model. Team C has built a very expensive `if` statement that reads the answer.

This module is about being Team B and never being Team C.

---

## 🧠 The Concept

### 1. Scaling: putting columns on the same ruler

Look at two columns from our table:

- `distance_km` ranges from about 0.3 to 14.4
- `driver_experience_months` ranges from 0 to 59

To a model like logistic regression, "1 unit" of distance and "1 unit" of experience look like the same size step, even though 1 km is a big deal and 1 month is almost nothing. Worse: any algorithm that measures distance between rows (k-nearest-neighbours, k-means, anything with a regularisation penalty) will let the column with the bigger numbers dominate purely because its numbers are bigger.

**Scaling** fixes this. Two recipes.

> **Standardization (z-score):** subtract the mean, divide by the standard deviation. Result has mean 0 and standard deviation 1.
> $$ z = \frac{x - \mu}{\sigma} $$

> **Min-max scaling:** subtract the minimum, divide by the range. Result is squashed into [0, 1].
> $$ x' = \frac{x - x_{\min}}{x_{\max} - x_{\min}} $$

🍕 **Analogy.** Standardization is grading on a curve: "you scored 1.5 standard deviations above the class mean." Min-max is grading out of 100: "you scored 87 out of the range from lowest to highest." Both tell you where a student sits. But if one student scores a freakish 400 on a 100-point test, the curve barely twitches while the out-of-100 scale gets destroyed — everyone else compresses into the bottom quarter.

🔢 **Tiny concrete example.** Take eight values: `[2, 4, 4, 4, 5, 5, 7, 9]`.

- Mean: (2+4+4+4+5+5+7+9) / 8 = 40 / 8 = **5**
- Squared deviations: 9, 1, 1, 1, 0, 0, 4, 16 → sum 32 → variance 32/8 = 4 → **σ = 2**
- Standardized: (2−5)/2 = **−1.5**, (4−5)/2 = **−0.5**, (5−5)/2 = **0**, (7−5)/2 = **1.0**, (9−5)/2 = **2.0**
- Min-max, with min 2 and max 9 so range 7: (2−2)/7 = **0**, (4−2)/7 = **0.2857**, (5−2)/7 = **0.4286**, (7−2)/7 = **0.7143**, (9−2)/7 = **1.0**

Now a new value arrives at prediction time: **12**.

- Standardized: (12−5)/2 = **3.5**. Large, but perfectly sensible — "3.5 standard deviations above the mean."
- Min-max: (12−2)/7 = **1.4286**. It escaped the [0, 1] box, which was the whole promise of min-max.

**Which do you pick?**

| | Standardization | Min-max |
|---|---|---|
| Output range | unbounded, centred on 0 | [0, 1] on training data only |
| Outliers | tolerated; a huge value gets a big z but doesn't move everyone else | one huge value crushes everything else toward 0 |
| Needs bounded input? | no | yes, ideally |
| Good default for | linear models, SVMs, PCA, anything with L1/L2 penalties | image pixels (already 0–255), neural net inputs, anything where a bounded range is required |
| Our delivery data | ✅ use this | ❌ `distance_km` has a long right tail |

Default to standardization unless you have a specific reason.

⚠️ **The rule that matters more than either formula:** the mean, standard deviation, min, and max must be computed on **training rows only**. In our data, the median driver experience over the full table is 29.0 but over the training split it is 29.5. Small difference — but the principle has no small version. Section 5 explains why.

---

### 2. Encoding: turning words into numbers

A model cannot multiply `"CrustyBros"` by a weight. Categories must become numbers. There are two ways and one of them is a trap.

**Ordinal encoding** maps each category to an integer: small→0, medium→1, large→2.

**One-hot encoding** makes one new 0/1 column per category:

```
restaurant = "Napoli"
        ->  restaurant_CrustyBros = 0
            restaurant_Napoli     = 1
            restaurant_SliceHouse = 0
```

🍕 **Analogy.** Ordinal encoding says "these things are on a ladder — one is above the other." T-shirt sizes really are on a ladder: large > medium > small. Restaurants are not. If you ordinal-encode `{Napoli: 0, SliceHouse: 1, CrustyBros: 2}`, you have told the model that CrustyBros = 2 × SliceHouse and that Napoli + CrustyBros = 2 × SliceHouse. It will believe you. It will be wrong.

🔢 **Tiny concrete example.** Suppose true lateness rates are Napoli 20%, SliceHouse 30%, CrustyBros 45%.

With **ordinal** encoding and a single weight `w`, the model can only produce a score of `w × code`. It can produce a straight line through 0, 1, 2. It happens to work here because the rates rise in code order — but only by luck. Shuffle the mapping to `{Napoli: 0, CrustyBros: 1, SliceHouse: 2}` and now the model must fit 20%, 45%, 30% with a straight line. It cannot. It will average CrustyBros and SliceHouse into mush.

With **one-hot** encoding the model gets three independent weights and can put each restaurant exactly where it belongs. No ordering assumed, none imposed.

| | Ordinal | One-hot |
|---|---|---|
| New columns | 1 | one per category |
| Implies order? | **yes** | no |
| Use when | the categories genuinely have an order you can state (small/medium/large, cold/warm/hot, 1-star…5-star) | there is no order (city, restaurant, colour, device model) |
| Danger | invented ordering | column explosion |

**High-cardinality categories.** One-hot works fine at 5 restaurants or 7 weekdays. It falls over at 50,000 postcodes: you get 50,000 columns, almost all zero, most of them seen fewer than 5 times in training. Three practical escapes:

1. **Group the tail.** Keep the top *k* categories, lump the rest into `"OTHER"`. `OneHotEncoder(max_categories=20, handle_unknown="infrequent_if_exist")` does this for you in modern scikit-learn.
2. **Encode a property, not the identity.** Replace `postcode` with `population_density`, `distance_to_depot`, `is_metro`. This is usually the best answer, and it is real feature engineering.
3. **Target encoding** — replace each category with the mean target for that category. Powerful, and a leakage minefield. Section 5 shows why. Not recommended until you can explain the leak in your sleep.

⚠️ **Always set `handle_unknown="ignore"`.** In training you see 5 restaurants. In production, restaurant #6 opens. Without that flag your artifact throws an exception on a live request. With it, the unseen category becomes an all-zero vector and the model falls back on the other features — degraded, but alive. Write that behaviour in your model card.

---

### 3. Deriving features: bins, ratios, dates, and interactions

The raw columns are what somebody happened to log. They are rarely the shape the answer lives in. Your job is to reshape reality until the pattern becomes something a simple model can see.

**(a) Bins.** Turn a number into a category when the relationship is not a straight line.

> **Binning:** cutting a continuous column into ranges and treating each range as a category.

`order_hour` runs 10 to 23. Lateness is *not* a straight line in hour — it is low at 14:00, spikes at 19:00, and drops again at 22:00. A linear model given raw `order_hour` fits one straight line through that hump and learns almost nothing. Its coefficient in Module 1 was **0.092**, near zero.

🔢 In our data: orders placed between 18:00 and 20:00 are late **36.8%** of the time (717 orders). Everything else is late **24.2%** of the time (1,283 orders). One binary column, `is_rush`, captures a 12.6-point gap that raw `order_hour` was blurring away.

**(b) Ratios.** Two columns often matter only in relation to each other.

`prep_minutes` alone is weak. `distance_km` alone is strong. But *minutes of prep per kilometre* asks a different question: is the kitchen the bottleneck, or the road? Guard against division by zero with a small constant:

```python
d["min_per_km"] = d["prep_minutes"] / (d["distance_km"] + 0.5)
```

🔢 A 12-minute prep on a 2 km run gives 12 / 2.5 = **4.80**. A 12-minute prep on a 9 km run gives 12 / 9.5 = **1.26**. Same prep time; completely different situations.

**(c) Dates.** A raw timestamp is nearly useless as a number. Explode it:

```python
d["dow"]        = ts.dt.dayofweek        # 0=Mon .. 6=Sun
d["is_weekend"] = ts.dt.dayofweek >= 5
d["month"]      = ts.dt.month
d["days_since_signup"] = (ts - signup_ts).dt.days
```

For anything that wraps around — hour of day, day of year, compass bearing — plain integers lie at the seam: 23:00 and 00:00 are one hour apart but 23 units apart numerically. Fix it with a **cyclical encoding**:

```python
d["hour_sin"] = np.sin(2 * np.pi * d["order_hour"] / 24)
d["hour_cos"] = np.cos(2 * np.pi * d["order_hour"] / 24)
```

Now hour 23 and hour 0 land right next to each other on a circle.

**(d) Interactions.** Two features whose *combination* matters more than either alone.

> **Interaction feature:** a new column built by combining two others, usually by multiplying, so the model can express "A matters more when B is true."

Distance costs you a little on a clear day and a lot in a storm. A linear model with separate `distance` and `storm` terms can only add those effects. Multiply them and it can express the amplification:

```python
severity = d["weather"].map({"clear": 0.0, "rain": 1.0, "storm": 2.0})
d["dist_x_weather"] = d["distance_km"] * severity
```

🔢 A 6 km delivery: `dist_x_weather` = 0 in clear, 6 in rain, 12 in a storm. The model now has a knob for "long trip *and* bad weather" that is distinct from either one.

🍕 **Analogy for the whole section.** Raw features are ingredients as they arrive: a whole onion, an unopened tin, a block of cheese. Feature engineering is chopping, grating, and mixing. The oven (the model) is the same either way — but nobody ever made a good pizza by throwing an unpeeled onion on top.

⚠️ **Every derived feature is a hypothesis, not a gift.** You must test it. Which brings us to:

> **Ablation:** measuring a feature's worth by building the model with it and without it, changing nothing else, and comparing on the validation set.

An ablation table is the deliverable of this module. Section 6's hands-on builds one, and it will show you that `is_weekend` — an obvious, sensible-sounding feature — buys exactly **zero**, because in our data weekends are late 27.5% of the time and weekdays 29.2%. Sensible-sounding is not the same as useful.

---

### 4. Imputation, done correctly

108 rows in our table have no `driver_experience_months`. Three options.

| Option | What it means | When |
|---|---|---|
| Drop the rows | throw away 108 of 2,000 rows | rarely — you lose data, and if the missingness is not random you also introduce bias |
| Drop the column | throw away the feature for everyone | when the column is >50% missing |
| **Impute** | fill the gap with a learned value | almost always the right call |

> **Imputation:** replacing a missing value with an estimate — the mean, the median, the most frequent category, or a model's prediction.

Median beats mean for skewed columns because one absurd value cannot drag it. `SimpleImputer(strategy="median")` for numbers; `strategy="most_frequent"` or `strategy="constant", fill_value="MISSING"` for categories.

🍕 **Analogy.** A friend's attendance register has three blank days. You could guess "they were probably here, they're usually here" (most frequent), or "put down their usual number" (median). What you must **not** do is peek at the end-of-year attendance total — which includes those three days — and work backwards. That is using the answer to fill in the question.

**The one rule.** The fill value is learned from **training rows only**, then applied to train, validation, and test. Our full-table median is 29.0; our training-split median is 29.5. Using 29.0 means every validation and test row got a value that was partly computed from validation and test rows. It is a tiny amount of cheating, and tiny cheating produces scores that are tiny-bit optimistic in a way you cannot measure or correct for.

**The bonus trick.** Missing is sometimes itself a signal. If experience is missing because the driver is a brand-new contractor whose paperwork hasn't cleared, then "missing" means "rookie" and that is enormously predictive. Keep the information:

```python
SimpleImputer(strategy="median", add_indicator=True)
```

This adds a `missingindicator_driver_experience_months` column that is 1 where the original was blank. Two features for the price of one, and the model decides whether the flag matters.

---

### 5. Data leakage: the three ways you feed the model the answer

> **Data leakage:** when information that would not be available at prediction time sneaks into training. The score goes up. The model gets worse. Both at once.

This is the most expensive bug in applied machine learning, because it does not look like a bug. It looks like success.

```
   HOW A GOOD PIPELINE FLOWS          HOW A LEAKY ONE FLOWS

   ┌──────────┐                       ┌──────────┐
   │ ALL DATA │                       │ ALL DATA │
   └────┬─────┘                       └────┬─────┘
        │ split FIRST                      │ fit scaler / impute /
        ▼                                  │ select features on EVERYTHING
   ┌────────┬─────┬──────┐                 ▼
   │ train  │ val │ test │            ┌──────────────┐
   └───┬────┴──┬──┴───┬──┘            │ "clean" data │
       │ fit   │ transform            └──────┬───────┘
       ▼       ▼      ▼                      │ split now (too late)
    stats learned here only                  ▼
                                        train / val / test
                                        (all contaminated)
```

**Flavour 1 — Target leakage.** A feature column contains information that only exists *because* the outcome already happened.

Our planted example: `customer_called_support`. It is 1 for 85% of late orders and 3% of on-time orders. Its correlation with the target is **0.848**. On the leak-enabled dataset, the honest feature set scores accuracy 0.7750 / AUC 0.7850. Add this one column and it jumps to accuracy **0.9525** / AUC **0.9776**.

*(Why 0.7750 and not Module 1's 0.7600? Generating the extra column consumes random numbers, which shifts which rows end up with a missing `driver_experience_months` and which rows get duplicated. Same generator, slightly different table. This is a good habit to notice: if adding a column changes your baseline, the data itself changed, not just the features.)*

In production this column is empty at the moment you need a prediction, because the pizza hasn't been delivered yet. Your beautiful 0.98 model becomes a 0.5 model on its first live request.

**How to catch it.** For every column, ask one question and answer it out loud: *"At the exact moment I need this prediction, does this value exist yet?"* Then back it up with numbers:

- Correlation of each feature with the target. Anything above ~0.8 gets interrogated.
- Train a model on **one feature at a time**. If one column alone gets AUC 0.95, that column is either magic or poison, and it is never magic.
- Look at the coefficients. A single feature with a coefficient 3× larger than everything else is a red flag.

**Flavour 2 — Temporal leakage.** You shuffle rows randomly across a time boundary, so the model trains on the future and is tested on the past.

🔢 A demonstration you will run in the Hands-On. Take 3,000 rows spread over 30 weeks where the relationship between `x1` and `y` slowly drifts (the world changes; it always does). Same model, same features, two ways of splitting:

| Split | AUC |
|---|---|
| Random 75/25 | **0.7894** |
| Time-based: weeks 0–21 train, weeks 22–29 test | **0.5550** |

The random split says the model is good. The time split says it is a coin flip. The time split is the one that matches how the model will actually be used — trained on the past, deployed on the future. The 0.79 was a lie.

**How to fix it.** If your rows have a timestamp and you will deploy forward in time, split by time, not at random. Use `TimeSeriesSplit` for cross-validation. And never compute a rolling feature — "customer's average order value over the last 30 days" — using a window that includes the row you are predicting.

**Flavour 3 — Preprocessing leakage.** Any statistic computed over all the data before splitting: a scaler's mean, an imputer's median, a feature selector's ranking, a PCA's components.

This one sounds harmless — surely a mean is just a mean? — so here is a demonstration with no ambiguity at all.

Generate **100 rows** and **5,000 columns** of pure random noise, and a completely random 0/1 label. There is, by construction, zero relationship between X and y. Any honest method must score 50%.

- **Wrong:** use all 100 rows to pick the 20 columns most correlated with y, then cross-validate a model on those 20 columns. Score: **0.83**.
- **Right:** put the selection *inside* the pipeline so it re-runs on each training fold only. Score: **0.50**.

83% accuracy on pure noise. The selection step saw the labels of the rows it was later tested on, found the twenty columns that happened to line up with those labels by chance, and handed the model a cheat sheet. Nothing about the model was wrong. The leak was upstream.

**The structural fix for flavour 3 is the reason `Pipeline` exists.** Every transform inside a `Pipeline` is fit only on whatever rows are passed to `.fit()`. Put your preprocessing inside the pipeline and this class of bug becomes impossible to write.

---

### 6. ColumnTransformer: one object, mixed columns, no leaks

Numbers need imputing and scaling. Categories need one-hot encoding. `ColumnTransformer` runs different branches on different columns and glues the outputs together.

```
                 raw DataFrame (8 columns, mixed types)
                                │
              ┌─────────────────┴──────────────────┐
              ▼                                    ▼
   num: [distance_km, items,              cat: [restaurant,
         prep_minutes, order_hour,              day_of_week,
         driver_experience_months]              weather]
              │                                    │
   SimpleImputer(median)                 OneHotEncoder(
              │                            handle_unknown="ignore")
   StandardScaler()                                │
              │                                    │
        5 numeric cols                       15 binary cols
              └─────────────┬──────────────────────┘
                            ▼
                 hstack -> 20-column matrix
                            │
                            ▼
                   LogisticRegression
```

```python
preprocess = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                      ("scale",  StandardScaler())]), NUM_COLS),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT_COLS),
])
```

Three things to know:

1. **Selection is by column name**, so the order of columns in the incoming DataFrame does not matter. (You proved this in Module 1's artifact test.)
2. **Columns you don't list are dropped**, by default. That is a feature — it forces you to name every column you feed the model. Pass `remainder="passthrough"` if you want the leftovers, but naming them explicitly is safer.
3. **`get_feature_names_out()`** gives you the names of the output columns, in order, prefixed by branch: `num__distance_km`, `cat__weather_storm`. Use it to build readable coefficient tables.

For derived features that need no learned statistics — `is_rush`, `min_per_km`, `dist_x_weather` — wrap a plain function in a `FunctionTransformer` and put it in front of the `ColumnTransformer`:

```python
pipe = Pipeline([
    ("derive", FunctionTransformer(add_features)),   # stateless: nothing to leak
    ("pre",    preprocess),                          # stateful: fit on train only
    ("model",  LogisticRegression(max_iter=2000)),
])
```

`FunctionTransformer` is safe here precisely because `add_features` does not look at `y` and does not compute anything across rows. It takes each row and does arithmetic on that row. If you ever write a "feature function" that computes a column mean, it is no longer stateless and it does not belong in a `FunctionTransformer`.

---

## 🔍 Worked Example

Five training rows and one validation row, transformed by hand, all the way to the final matrix. Every number below has been checked against scikit-learn.

**Training rows.**

| order | distance_km | prep_minutes | restaurant | weather | late |
|---|---|---|---|---|---|
| A | 2 | 12 | Napoli | clear | 0 |
| B | 4 | 20 | CrustyBros | rain | 1 |
| C | 5 | 14 | Napoli | clear | 0 |
| D | 6 | 16 | SliceHouse | storm | 1 |
| E | 8 | 8 | CrustyBros | clear | 1 |

**Validation row F:** distance 11, prep 14, restaurant **GreenLeaf** (never seen in training), weather clear.

---

**Step 1 — Standardize `distance_km`, using training rows only.**

Mean = (2 + 4 + 5 + 6 + 8) / 5 = 25 / 5 = **5**

Deviations: −3, −1, 0, +1, +3
Squared: 9, 1, 0, 1, 9 → sum = 20 → variance = 20 / 5 = 4 → **σ = 2**

| order | x | (x − 5) / 2 |
|---|---|---|
| A | 2 | **−1.5** |
| B | 4 | **−0.5** |
| C | 5 | **0.0** |
| D | 6 | **+0.5** |
| E | 8 | **+1.5** |

**Step 2 — Standardize `prep_minutes`, training rows only.**

Mean = (12 + 20 + 14 + 16 + 8) / 5 = 70 / 5 = **14**

Deviations: −2, +6, 0, +2, −6
Squared: 4, 36, 0, 4, 36 → sum = 80 → variance = 80 / 5 = 16 → **σ = 4**

| order | x | (x − 14) / 4 |
|---|---|---|
| A | 12 | **−0.5** |
| B | 20 | **+1.5** |
| C | 14 | **0.0** |
| D | 16 | **+0.5** |
| E | 8 | **−1.5** |

**Step 3 — One-hot encode `restaurant`.** Training categories, sorted alphabetically: CrustyBros, Napoli, SliceHouse → 3 columns.

| order | _CrustyBros | _Napoli | _SliceHouse |
|---|---|---|---|
| A | 0 | 1 | 0 |
| B | 1 | 0 | 0 |
| C | 0 | 1 | 0 |
| D | 0 | 0 | 1 |
| E | 1 | 0 | 0 |

**Step 4 — One-hot encode `weather`.** Categories: clear, rain, storm.

| order | _clear | _rain | _storm |
|---|---|---|---|
| A | 1 | 0 | 0 |
| B | 0 | 1 | 0 |
| C | 1 | 0 | 0 |
| D | 0 | 0 | 1 |
| E | 1 | 0 | 0 |

**Step 5 — The training design matrix.** Eight columns, in `ColumnTransformer` order (numeric branch first, then categorical):

```
        dist  prep  Crusty Napoli Slice  clear  rain  storm
  A  [ -1.5  -0.5    0      1      0      1     0      0  ]
  B  [ -0.5  +1.5    1      0      0      0     1      0  ]
  C  [  0.0   0.0    0      1      0      1     0      0  ]
  D  [ +0.5  +0.5    0      0      1      0     0      1  ]
  E  [ +1.5  -1.5    1      0      0      1     0      0  ]
```

**Step 6 — Transform validation row F. Reuse the training statistics. Do not recompute.**

- distance: (11 − 5) / 2 = **+3.0**. Well outside the training range, which is correct and informative — the model will produce a confident prediction and you should be suspicious of it.
- prep: (14 − 14) / 4 = **0.0**
- restaurant "GreenLeaf" was never seen. With `handle_unknown="ignore"` it becomes **[0, 0, 0]** — no crash, no fake category.
- weather "clear" → **[1, 0, 0]**

```
  F  [ +3.0   0.0    0      0      0      1     0      0  ]
```

**Step 7 — Now add two derived features.**

`min_per_km = prep_minutes / (distance_km + 0.5)`:

| order | arithmetic | value |
|---|---|---|
| A | 12 / 2.5 | **4.8000** |
| B | 20 / 4.5 | **4.4444** |
| C | 14 / 5.5 | **2.5455** |
| D | 16 / 6.5 | **2.4615** |
| E | 8 / 8.5 | **0.9412** |

`dist_x_weather = distance_km × severity`, with clear = 0, rain = 1, storm = 2:

| order | arithmetic | value |
|---|---|---|
| A | 2 × 0 | **0** |
| B | 4 × 1 | **4** |
| C | 5 × 0 | **0** |
| D | 6 × 2 | **12** |
| E | 8 × 0 | **0** |

Both new columns are computed **per row**, from that row's own values. Nothing crosses between rows, so nothing can leak. They then go through the same `StandardScaler` as the other numeric columns — fit on train, applied to F.

**Step 8 — The mistake we just avoided.** If instead you had standardized `distance_km` using all six rows (A–F), the mean would be (25 + 11) / 6 = 6.0 and σ would be about 2.83. Every single training row's encoding would have shifted, because of one validation row. The model would have been trained on numbers that carry a whisper of the validation set. On six rows this is a visible distortion. On 2,000 rows it is invisible — and still wrong.

---

## 💻 Hands-On

Four scripts. You need `make_data.py` from Module 1 in the same folder.

### Script 1 — `ablation.py`: does each feature actually help?

```python
"""Ablation study: add one feature group at a time, measure the validation change."""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

from make_data import make_deliveries

RS = 42
BASE_NUM = ["distance_km", "items", "prep_minutes", "order_hour",
            "driver_experience_months"]
CAT = ["restaurant", "day_of_week", "weather"]

df = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)
y = df["late"]
X = df.drop(columns=["late", "order_id"])
X_tmp, X_te, y_tmp, y_te = train_test_split(
    X, y, test_size=.20, random_state=RS, stratify=y)
X_tr, X_va, y_tr, y_va = train_test_split(
    X_tmp, y_tmp, test_size=.25, random_state=RS, stratify=y_tmp)


def add_features(d, rush=False, weekend=False, ratio=False, inter=False, log=False):
    """Row-wise only. No cross-row statistics, so this cannot leak."""
    d = d.copy()
    if rush:
        d["is_rush"] = d["order_hour"].between(18, 20).astype(int)
    if weekend:
        d["is_weekend"] = d["day_of_week"].isin(["Sat", "Sun"]).astype(int)
    if ratio:
        d["min_per_km"] = d["prep_minutes"] / (d["distance_km"] + 0.5)
        d["items_per_km"] = d["items"] / (d["distance_km"] + 0.5)
    if inter:
        sev = d["weather"].map({"clear": 0.0, "rain": 1.0, "storm": 2.0})
        d["dist_x_weather"] = d["distance_km"] * sev
        d["dist_x_rush"] = d["distance_km"] * d["order_hour"].between(18, 20).astype(int)
    if log:
        d["log_distance"] = np.log1p(d["distance_km"])
    return d


def evaluate(label, **kw):
    extra = [c for c in add_features(X_tr.head(2), **kw).columns if c not in X_tr.columns]
    num = BASE_NUM + extra
    pre = ColumnTransformer([
        ("num", Pipeline([("i", SimpleImputer(strategy="median")),
                          ("s", StandardScaler())]), num),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT),
    ])
    pipe = Pipeline([
        ("derive", FunctionTransformer(add_features, kw_args=kw)),
        ("pre", pre),
        ("model", LogisticRegression(max_iter=2000, random_state=RS)),
    ])
    pipe.fit(X_tr, y_tr)
    prob = pipe.predict_proba(X_va)[:, 1]
    return {"variant": label,
            "n_features": len(num) + sum(X_tr[c].nunique() for c in CAT),
            "accuracy": accuracy_score(y_va, (prob >= .5).astype(int)),
            "roc_auc": roc_auc_score(y_va, prob)}


rows = [
    evaluate("A  base (Module 1)"),
    evaluate("B  A + is_rush", rush=True),
    evaluate("C  B + is_weekend", rush=True, weekend=True),
    evaluate("D  B + ratios", rush=True, ratio=True),
    evaluate("E  B + interactions", rush=True, inter=True),
    evaluate("F  B + ratios + interactions", rush=True, ratio=True, inter=True),
    evaluate("G  F + log_distance", rush=True, ratio=True, inter=True, log=True),
]
tbl = pd.DataFrame(rows)
tbl["d_auc"] = tbl["roc_auc"] - tbl.loc[0, "roc_auc"]
print(tbl.round(4).to_string(index=False))
```

```bash
python ablation.py
```

```
                     variant  n_features  accuracy  roc_auc  d_auc
          A  base (Module 1)          20    0.7600   0.7752 0.0000
              B  A + is_rush          21    0.7725   0.7825 0.0074
           C  B + is_weekend          22    0.7725   0.7825 0.0073
               D  B + ratios          23    0.7650   0.7853 0.0102
         E  B + interactions          23    0.7775   0.7828 0.0076
F  B + ratios + interactions          25    0.7700   0.7841 0.0089
         G  F + log_distance          26    0.7700   0.7839 0.0088
```

Read this table slowly, because it teaches four separate lessons.

1. **`is_rush` earned its place.** +0.0074 AUC and +1.25 accuracy points for one binary column. That is the 18:00–20:00 hump that raw `order_hour` could not express.
2. **`is_weekend` bought exactly nothing.** Row C matches row B to four decimal places on both accuracy and AUC (the ΔAUC column differs only in the last digit, from rounding). Remember the numbers from earlier: weekends 27.5% late, weekdays 29.2%. There was no signal to find. **Delete the feature.** A feature that adds no score adds only maintenance cost and one more thing to break.
3. **More features is not better.** Row G has the most columns and is *worse* than row D. Every extra column is another weight to estimate from the same 1,200 rows, and noisy weights cost you.
4. **Your metric decides the winner, and you chose it in Module 1.** On AUC — our committed headline metric — **D wins** (0.7853). On accuracy, **E wins** (0.7775). If you had not fixed the metric in advance you would now be quietly picking whichever one made you look best. Ship **D**.

Honest framing of the result: we went from AUC 0.7752 to 0.7853. That is **one point**. Feature engineering is not magic; it is a grind of small, defensible gains — and it is still usually a better use of a day than hyperparameter tuning.

### Script 2 — `leak_hunt.py`: find the planted bug

```python
"""A suspiciously perfect model, and the audit that catches it."""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from make_data import make_deliveries

RS = 42
df = make_deliveries(n=2000, seed=0, add_leak=True).drop_duplicates().reset_index(drop=True)
y = df["late"]
X = df.drop(columns=["late", "order_id"])
X_tmp, X_te, y_tmp, y_te = train_test_split(X, y, test_size=.2, random_state=RS, stratify=y)
X_tr, X_va, y_tr, y_va = train_test_split(X_tmp, y_tmp, test_size=.25, random_state=RS, stratify=y_tmp)

CAT = ["restaurant", "day_of_week", "weather"]


def fit_and_score(num_cols, label):
    pre = ColumnTransformer([
        ("num", Pipeline([("i", SimpleImputer(strategy="median")),
                          ("s", StandardScaler())]), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT)])
    pipe = Pipeline([("pre", pre),
                     ("m", LogisticRegression(max_iter=1000, random_state=RS))]).fit(X_tr, y_tr)
    prob = pipe.predict_proba(X_va)[:, 1]
    print(f"{label:<28s} accuracy={accuracy_score(y_va, (prob >= .5).astype(int)):.4f}"
          f"  roc_auc={roc_auc_score(y_va, prob):.4f}")
    return pipe


GOOD = ["distance_km", "items", "prep_minutes", "order_hour", "driver_experience_months"]
POISONED = GOOD + ["customer_called_support"]

print("--- scores ---")
bad_pipe = fit_and_score(POISONED, "with customer_called_support")
fit_and_score(GOOD, "without it")

print("\n--- audit 1: correlation of every numeric column with the target ---")
corr = df[POISONED + ["late"]].corr()["late"].drop("late").sort_values(key=abs, ascending=False)
print(corr.round(3).to_string())

print("\n--- audit 2: crosstab of the suspect against the target ---")
print(pd.crosstab(df["customer_called_support"], df["late"]))

print("\n--- audit 3: coefficient magnitudes ---")
names = bad_pipe.named_steps["pre"].get_feature_names_out()
co = pd.Series(bad_pipe.named_steps["m"].coef_[0], index=names)
print(co.reindex(co.abs().sort_values(ascending=False).index).head(5).round(3).to_string())

print("\n--- audit 4: the question no statistic can answer ---")
print("At the moment the order is PLACED, has the customer called support about")
print("a late delivery that has not happened yet?  No. The column is empty.")
print("VERDICT: target leakage. Drop the column.")
```

```
--- scores ---
with customer_called_support accuracy=0.9525  roc_auc=0.9776
without it                   accuracy=0.7750  roc_auc=0.7850

--- audit 1: correlation of every numeric column with the target ---
customer_called_support     0.848
distance_km                 0.345
driver_experience_months   -0.127
items                       0.106
prep_minutes                0.066
order_hour                  0.064

--- audit 2: crosstab of the suspect against the target ---
late                        0    1
customer_called_support
0                        1384   82
1                          41  493

--- audit 3: coefficient magnitudes ---
num__customer_called_support    2.476
num__distance_km                0.908
cat__weather_storm              0.830
cat__weather_clear             -0.735
num__driver_experience_months  -0.581

--- audit 4: the question no statistic can answer ---
...
VERDICT: target leakage. Drop the column.
```

Four independent alarms, each louder than the last:

1. AUC jumped **0.193** from one column (0.7850 → 0.9776). Real features never do that.
2. Correlation with the target is **0.848**, while the next-best honest feature is 0.345.
3. The crosstab is nearly diagonal: of 534 orders where support was called, 493 were late.
4. Its coefficient is **2.7× larger** than the next one.

And then the decisive test, which is not a statistic at all: **could you fill in this column at prediction time?** No. Drop it.

### Script 3 — `temporal.py`: the split that lies

```python
"""Random split vs time split, when the world drifts."""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(11)
n = 3000
week = np.repeat(np.arange(30), n // 30)
x1 = rng.normal(size=n)
x2 = rng.normal(size=n)
w1 = 2.0 - 0.13 * week                       # the world drifts: x1 matters less over time
y = ((w1 * x1 + 0.8 * x2 + rng.normal(0, .5, n)) > 0).astype(int)
df = pd.DataFrame({"week": week, "x1": x1, "x2": x2, "y": y})
F = ["x1", "x2"]

X_tr, X_te, y_tr, y_te = train_test_split(
    df[F], df["y"], test_size=.25, random_state=0, stratify=df["y"])
m = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_tr, y_tr)
print("RANDOM split AUC  %.4f   <- what you'd report"
      % roc_auc_score(y_te, m.predict_proba(X_te)[:, 1]))

tr, te = df[df.week < 22], df[df.week >= 22]
m2 = make_pipeline(StandardScaler(), LogisticRegression()).fit(tr[F], tr["y"])
print("TIME   split AUC  %.4f   <- what production will give you"
      % roc_auc_score(te["y"], m2.predict_proba(te[F])[:, 1]))
```

```
RANDOM split AUC  0.7894   <- what you'd report
TIME   split AUC  0.5550   <- what production will give you
```

A 0.234 AUC gap, produced entirely by the choice of how to split. Nothing else changed.

### Script 4 — `noise_leak.py`: 83% accuracy on pure randomness

```python
"""Preprocessing leakage, demonstrated on data with zero signal by construction."""
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline

rng = np.random.default_rng(7)
X = rng.normal(size=(100, 5000))          # 100 rows, 5000 columns of pure noise
y = rng.integers(0, 2, size=100)          # a coin flip. No relationship to X at all.
cv = StratifiedKFold(5, shuffle=True, random_state=0)

# WRONG: select the best 20 columns using ALL rows (and therefore all labels)
X20 = SelectKBest(f_classif, k=20).fit_transform(X, y)
wrong = cross_val_score(LogisticRegression(max_iter=1000), X20, y, cv=cv).mean()

# RIGHT: selection lives inside the pipeline, so it re-runs on each training fold only
pipe = Pipeline([("sel", SelectKBest(f_classif, k=20)),
                 ("m", LogisticRegression(max_iter=1000))])
right = cross_val_score(pipe, X, y, cv=cv).mean()

print(f"WRONG (select on all data): {wrong:.3f}")
print(f"RIGHT (select inside CV)  : {right:.3f}   <- the truth")
```

```
WRONG (select on all data): 0.830
RIGHT (select inside CV)  : 0.500   <- the truth
```

Pin this output above your desk. There is no signal in that data. None. And a careless pipeline reports 83%.

---

## ✍️ Practice

### [Warm-up] 1 — Scale by hand, then check
Given the training column `[10, 20, 20, 30, 45, 55]`:
(a) Compute the mean and the population standard deviation (divide by *n*, not *n*−1 — that's what `StandardScaler` uses).
(b) Standardize every value, to 4 decimal places.
(c) Min-max scale every value.
(d) A new value of **70** arrives at prediction time. Give its standardized and min-max values, and say which encoding you find more honest and why.
(e) Verify (b) and (c) with `StandardScaler` and `MinMaxScaler`.

**Done looks like:** two tables of 6 numbers, two numbers for the new value, one sentence of judgement, and matching sklearn output.

### [Warm-up] 2 — Encoding decisions
For each column, choose one-hot, ordinal, or "neither — derive something else instead," and justify in one sentence.
(a) `t_shirt_size` ∈ {XS, S, M, L, XL}
(b) `browser` ∈ {Chrome, Safari, Firefox, Edge}
(c) `postcode` — 41,000 distinct values
(d) `star_rating` ∈ {1, 2, 3, 4, 5}
(e) `blood_type` ∈ {A, B, AB, O}
(f) `education` ∈ {none, primary, secondary, bachelor, master, phd}

**Done looks like:** six choices, six one-sentence reasons, and for (c) a concrete alternative column you'd build instead.

### [Build] 3 — Cyclical hour encoding
Add `hour_sin` and `hour_cos` to `add_features` (formula in Concept 3c) and add a row to the ablation table for "B + cyclical hour". Compare it against `is_rush` alone and against both together. Then print the model's coefficients for `hour_sin`, `hour_cos`, and `is_rush`.

**Done looks like:** three new rows in the ablation table, the three coefficients, and one sentence saying whether cyclical encoding beat the simple binary flag on *this* dataset — and a guess at why.

### [Build] 4 — Missingness as a signal
Modify `make_data.py` so that missing `driver_experience_months` is **not** random: make a value missing with probability 0.35 when `driver_exp < 6`, and probability 0.02 otherwise. (Rookies' paperwork hasn't cleared.) Then compare three pipelines: (i) median imputation, (ii) median imputation with `add_indicator=True`, (iii) dropping every row with a missing value. Report validation accuracy, AUC, and the number of training rows used by each.

**Done looks like:** a three-row table, plus the coefficient of the missing-indicator column and a sentence interpreting its sign.

### [Stretch] 5 — Build your own leak, then catch it
Add a new column to `make_data.py` that leaks *subtly* — not an obvious 0.85 correlation. Suggestion: `driver_shift_overtime_minutes`, generated as `max(0, 25 * late + rng.normal(5, 8, n))`. Its correlation with the target will be moderate, not screaming. Then write `detect_leaks.py` that automatically flags suspect columns using **three** independent tests: (i) absolute correlation with the target above a threshold you pick; (ii) single-feature AUC above a threshold; (iii) a printed checklist prompting the human "is this value available at prediction time? y/n" for every feature.

**Done looks like:** the correlation and single-feature AUC of your planted column, which of the three tests caught it, and a paragraph on why test (iii) can never be automated.

### [Stretch] 6 — Target encoding, done wrong then right
Implement target encoding for `restaurant` (replace each restaurant with the mean `late` rate for that restaurant) in two ways:
(a) **Wrong:** compute the means over the entire dataset before splitting.
(b) **Right:** compute the means inside a K-fold loop so each row's encoding comes only from *other* rows' targets (this is called out-of-fold target encoding).
Report validation AUC for both. Then explain, using a table with 5 restaurants and their counts, why the wrong version is worse for a category that appears only 3 times.

**Done looks like:** two AUC numbers, working code for both, and a worked explanation of the rare-category failure with actual numbers.

---

## 🤔 Think Deeper

**1. When does a derived feature stop being "engineering" and start being "the model"?**
`is_rush` is a rule you wrote by looking at the data. So is `dist_x_weather`. Push this far enough and you have hand-coded the answer and the "model" is just adding up your rules.
*How to reason about it:* Ask where the knowledge is stored — in your code or in the fitted weights. Then ask what happens when the data changes: which parts update automatically on retrain, and which parts require *you* to notice and edit a file? A feature that hard-codes 18:00–20:00 will silently go stale if the city's rush hour shifts.

**2. Is dropping `is_weekend` because it "didn't help" a defensible decision, or is it overfitting your validation set?**
You tested one feature on 400 validation rows and it moved the score by 0.0000. But if you test 50 features on those same 400 rows and keep the best few, you have started fitting your *choices* to the validation set — the exact problem the three-way split was meant to contain.
*How to reason about it:* Think about how many decisions a 400-row validation set can safely support. Consider what cross-validation (Module 3) would change. Consider whether a feature with a strong causal story deserves to be kept even when the measured gain is zero, and what that policy costs you if you apply it to every feature.

**3. Is `driver_experience_months` leakage?**
It is genuinely available at order time, so it passes the leakage test. But suppose the dispatcher assigns experienced drivers to the hard deliveries. Then experience is partly a *consequence* of how difficult the order already looked — which means the feature carries the dispatcher's judgement, not just the driver's skill.
*How to reason about it:* Distinguish "available before the outcome" from "independent of the decision process." Draw the causal arrows: order → dispatcher's judgement → driver assigned → outcome. Ask what happens to your model when the dispatch policy changes. This has a name in the literature — *feedback* or *treatment* leakage — and it is the reason models that look fine in backtests degrade after deployment.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Fitting the scaler on the whole dataset before splitting | Scaling feels like "cleaning," and cleaning feels like it happens first | Split first, then put every transform inside a `Pipeline` so `fit` only ever sees train |
| Ordinal-encoding an unordered category | `LabelEncoder` is one line and produces numbers, so it looks done | Use `OneHotEncoder` unless you can state the ordering out loud without wincing |
| Using `LabelEncoder` on X | Its name sounds general; it is documented for **y** only and doesn't handle unseen values | `OrdinalEncoder` (ordered) or `OneHotEncoder` (unordered) for features |
| One-hot encoding a 40,000-category column | It's the "safe" choice, and nobody checked the cardinality | Check `nunique()` first; group the tail with `max_categories`, or replace the identity with a property |
| Adding 30 features at once and celebrating a higher score | Ablation is boring and takes longer | Add one group at a time and record the delta; keep only what pays |
| Keeping a feature because it "makes sense" despite a zero delta | Sunk cost, and the story was satisfying | The ablation table is the referee, not your intuition |
| Imputing with the full-dataset median | `df.fillna(df.median())` is one beautiful line | `SimpleImputer` inside the pipeline; the median comes from train only |
| Shuffling a time-ordered dataset randomly | `train_test_split` is the default habit | Split by timestamp when you will deploy forward in time; use `TimeSeriesSplit` for CV |
| Trusting a 0.98 AUC | Good news gets audited less carefully than bad news | Treat any big jump as a leak until proven otherwise: correlations, single-feature AUC, coefficient sizes, and the availability question |
| Feature selection before cross-validation | It feels like a preprocessing step, and it is fast to do once | Put the selector inside the `Pipeline` so it re-fits on every fold |

---

## 🛠️ Mini-Project — Beat The Baseline

**Goal.** Two deliverables. **(1)** Improve Module 1's validation score using *only* feature changes — the algorithm stays `LogisticRegression` with the same settings, no swapping in a random forest — and produce a feature-by-feature ablation table that justifies every column you kept. **(2)** Separately, find and fix a planted leakage bug and write up how you caught it.

**Time:** 90–120 minutes.

### Starter steps

**Part 1 — Beat the baseline.**

1. Copy `ablation.py` and get row A reproducing Module 1's numbers exactly: accuracy 0.7600, AUC 0.7752. If they don't match, your split is different — fix that before anything else.
2. Before writing any feature, spend 15 minutes *looking*. Run `df.groupby(col)["late"].agg(["mean","size"])` for every categorical column, and `pd.cut` a few numeric ones into 5 bins and do the same. Write down three hypotheses in plain English before you write any code.
3. Implement your features one group at a time inside `add_features`. Add a row to the ablation table after each.
4. Any feature whose ΔAUC is below +0.002, delete. Say so in the table.
5. Declare a winner using the metric you committed to in Module 1 (AUC), not whichever column looks nicest.
6. Retrain the winning pipeline, save it as `late_pipeline_v2.joblib`, and update `model_card.md` with the new feature list and the new metrics.

**Part 2 — Catch the leak.**

7. Regenerate the data with `add_leak=True` and fit the pipeline with `customer_called_support` included. Note the suspiciously high score.
8. Run all four audits from `leak_hunt.py`: correlation, crosstab, single-feature AUC, coefficient magnitude.
9. Write `LEAK_REPORT.md`: what the score was, which audit fired first, what the column actually is, why it cannot exist at prediction time, and what the honest score is once it's removed.

### Success criteria checklist

- [ ] Row A of your ablation table reproduces 0.7600 / 0.7752 exactly.
- [ ] The table has at least 5 variants, each changing exactly one feature group.
- [ ] Every row shows accuracy, AUC, and ΔAUC against row A.
- [ ] At least one row shows a feature that **did not help**, and you kept that row in the table instead of hiding it.
- [ ] Your winning variant improves validation AUC by at least +0.008 over row A.
- [ ] The algorithm and its hyperparameters are byte-for-byte identical across every row.
- [ ] Every derived feature is computed row-wise inside the pipeline. No `df["x"] = ...` outside it.
- [ ] `late_pipeline_v2.joblib` exists and loads in a fresh process.
- [ ] `model_card.md` lists the new features and the new metrics.
- [ ] `LEAK_REPORT.md` names the audit that fired first and gives both the leaky and honest scores.
- [ ] The test set has still never been opened.

### Level it up

Turn ablation into a search. Write a script that enumerates every subset of your 6 candidate feature groups (2⁶ = 64 pipelines), fits each, and prints a table sorted by validation AUC. Then answer the hard question in writing: **the best of 64 pipelines on a 400-row validation set is very likely the luckiest, not the best.** Estimate how much of the winner's margin is real by re-running the whole search with `random_state` values 0 through 4 and checking whether the same subset wins each time. If a different subset wins each run, your search found noise, and you have just discovered — one module early — why Module 3 replaces the single validation score with cross-validation and error bars.

---

## 🔑 Key Takeaways

- **Standardize by default**, min-max only when you need a bounded range. Both must learn their statistics from training rows only.
- **One-hot unordered categories, ordinal only genuine ladders.** Always set `handle_unknown="ignore"` so a new category degrades your model instead of crashing it.
- **Derived features are hypotheses.** Bins for humps, ratios for relationships, date parts for time, products for amplification — and every one of them must survive an ablation.
- **A feature that doesn't move the metric is a liability.** Delete it and keep the row in the table so future-you knows it was tested.
- **Leakage comes in three flavours** — target, temporal, preprocessing — and all three make your score go *up*. Good news deserves more scrutiny than bad news.
- **The un-automatable test:** at the exact moment I need this prediction, does this value exist? No statistic can answer that. Only you can.
- **`Pipeline` + `ColumnTransformer` make preprocessing leakage structurally impossible.** That is not a convenience. That is the point.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Feature engineering** | Reshaping raw columns into ones the model can actually use | turning `order_hour` into `is_rush` |
| **Standardization (z-score)** | Rescale so mean is 0 and standard deviation is 1 | 9 becomes (9−5)/2 = 2.0 |
| **Min-max scaling** | Squash into the range 0 to 1 | 4 becomes (4−2)/7 = 0.2857 |
| **One-hot encoding** | One yes/no column per category | Napoli → [0, 1, 0] |
| **Ordinal encoding** | Categories become integers on a ladder | small→0, medium→1, large→2 |
| **Cardinality** | How many distinct values a column has | `restaurant`: 5. `postcode`: 41,000 |
| **`handle_unknown="ignore"`** | Setting that turns an unseen category into all zeros instead of a crash | GreenLeaf → [0, 0, 0] |
| **Binning** | Chopping a number into ranges and treating them as categories | hour 18–20 → "rush" |
| **Ratio feature** | One column divided by another | `prep_minutes / distance_km` |
| **Interaction feature** | Two columns multiplied, so one can amplify the other | `distance × storm` |
| **Cyclical encoding** | sin/cos so 23:00 sits next to 00:00 | `sin(2π·h/24)`, `cos(2π·h/24)` |
| **Imputation** | Filling a missing value with a learned guess | blank experience → train median, 29.5 |
| **Missing indicator** | An extra 0/1 column marking where a value was blank | `add_indicator=True` |
| **Ablation** | Build with the feature, build without it, compare | `is_weekend` → ΔAUC 0.0000 → delete |
| **Data leakage** | Information sneaking in that won't exist at prediction time | `customer_called_support` |
| **Target leakage** | A feature that only exists because the outcome already happened | AUC 0.978, useless in production |
| **Temporal leakage** | Training on the future, testing on the past | random split 0.79, time split 0.56 |
| **Preprocessing leakage** | Statistics computed before the split | 83% accuracy on pure noise |
| **ColumnTransformer** | Runs different preprocessing on different columns and glues the results | scale 5 numbers, one-hot 3 categories |
| **FunctionTransformer** | Wraps a plain function so it can live in a Pipeline | `add_features` |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1 — Scale by hand, then check

Values: `[10, 20, 20, 30, 45, 55]`, n = 6.

**(a) Mean and σ.**

Mean = (10 + 20 + 20 + 30 + 45 + 55) / 6 = 180 / 6 = **30**

Deviations: −20, −10, −10, 0, +15, +25
Squared: 400, 100, 100, 0, 225, 625 → sum = **1450**
Variance = 1450 / 6 = 241.6667 → **σ = 15.5456**

**(b) Standardized** (divide each deviation by 15.5456):

| x | z |
|---|---|
| 10 | −1.2865 |
| 20 | −0.6432 |
| 20 | −0.6432 |
| 30 | 0.0000 |
| 45 | 0.9649 |
| 55 | 1.6082 |

**(c) Min-max**, min 10, max 55, range 45:

| x | (x−10)/45 |
|---|---|
| 10 | 0.0000 |
| 20 | 0.2222 |
| 20 | 0.2222 |
| 30 | 0.4444 |
| 45 | 0.7778 |
| 55 | 1.0000 |

**(d) New value 70.**

- Standardized: (70 − 30) / 15.5456 = **2.5731**
- Min-max: (70 − 10) / 45 = **1.3333** — outside [0, 1]

The standardized version is more honest. It says "this is 2.57 standard deviations above typical," which is meaningful and comparable to any other feature. The min-max value of 1.3333 silently violates the guarantee the encoding was chosen for, and if anything downstream assumes a [0, 1] range (a sigmoid input layer, a bounded parameter) it will misbehave without complaining.

**(e) Verification.**

```python
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

x = np.array([[10], [20], [20], [30], [45], [55]], dtype=float)

ss = StandardScaler().fit(x)
print("mean", ss.mean_, "sigma", ss.scale_)         # [30.] [15.5456...]
print(np.round(ss.transform(x).ravel(), 4))
print(np.round(ss.transform([[70.]]).ravel(), 4))    # [2.5731]

mm = MinMaxScaler().fit(x)
print(np.round(mm.transform(x).ravel(), 4))
print(np.round(mm.transform([[70.]]).ravel(), 4))    # [1.3333]
```

### 2 — Encoding decisions

| Column | Choice | Reason |
|---|---|---|
| (a) `t_shirt_size` | **Ordinal** — XS=0, S=1, M=2, L=3, XL=4 | A genuine ladder you can state out loud: XL really is bigger than L. Pass the order explicitly via `OrdinalEncoder(categories=[[...]])` — never trust alphabetical order, which would give L < M < S < XL < XS. |
| (b) `browser` | **One-hot** | Four values, no ordering. Chrome is not "more" than Firefox. Four columns is nothing. |
| (c) `postcode` | **Neither — derive instead** | 41,000 one-hot columns on any realistic dataset means most categories appear once or twice. Replace with `population_density`, `km_to_nearest_depot`, `is_metro`, and `mean_delivery_time_in_this_postcode_last_year` (careful: that last one is target encoding and must be computed out-of-fold, see exercise 6). |
| (d) `star_rating` | **Ordinal** (usually) | 1–5 is ordered. Treating it as a plain number also assumes the gaps are equal, which is arguably false — the gap from 4★ to 5★ often means more than 2★ to 3★. If you have plenty of data, one-hot lets the model learn each level's effect separately and you can compare via ablation. |
| (e) `blood_type` | **One-hot** | Four values, absolutely no ordering. AB is not the average of A and B, whatever the letters suggest. |
| (f) `education` | **Ordinal** | none < primary < secondary < bachelor < master < phd is a real, stateable ordering. Same caveat about unequal gaps as star ratings. |

### 3 — Cyclical hour encoding

```python
# inside add_features, add a `cyc` flag:
    if cyc:
        d["hour_sin"] = np.sin(2 * np.pi * d["order_hour"] / 24)
        d["hour_cos"] = np.cos(2 * np.pi * d["order_hour"] / 24)
```

```python
rows = [
    evaluate("A  base"),
    evaluate("B  A + is_rush", rush=True),
    evaluate("H  A + cyclical hour", cyc=True),
    evaluate("I  A + is_rush + cyclical", rush=True, cyc=True),
]
print(pd.DataFrame(rows).round(4).to_string(index=False))
```

Expected pattern: cyclical hour helps compared to raw `order_hour` alone (it lets the model bend around the clock instead of fitting one straight line), but it lands **below** `is_rush`, and adding both on top of each other gains little over `is_rush` alone.

**Why.** Sine and cosine at one cycle per day can only produce a single smooth hump across 24 hours. Our data's true effect is not a smooth hump — it is a hard rectangular step: `+0.9` if 18 ≤ hour ≤ 20, otherwise 0. `is_rush` is exactly the right shape; sin/cos is a smooth approximation of a sharp edge. Cyclical encoding is the better tool when the effect really is smooth and periodic (temperature by month, traffic by hour in a city with a gentle profile). Here the truth is a step, so the step function wins.

To print the coefficients:

```python
pipe = ...   # the fitted "I" variant
names = pipe.named_steps["pre"].get_feature_names_out()
co = pd.Series(pipe.named_steps["model"].coef_[0], index=names)
print(co[[n for n in names if any(k in n for k in ["hour_sin", "hour_cos", "is_rush"])]].round(3))
```

You should see `is_rush` carrying a clearly larger magnitude than either trigonometric term.

### 4 — Missingness as a signal

In `make_data.py`, replace the missingness block:

```python
    p_missing = np.where(driver_exp < 6, 0.35, 0.02)
    miss = rng.random(n) < p_missing
    df.loc[miss, "driver_experience_months"] = np.nan
```

```python
# Continues from ablation.py: X_tr, X_va, y_tr, y_va are already defined there.
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUM = ["distance_km", "items", "prep_minutes", "order_hour", "driver_experience_months"]
CAT = ["restaurant", "day_of_week", "weather"]


def build(imputer):
    return Pipeline([
        ("pre", ColumnTransformer([
            ("num", Pipeline([("i", imputer), ("s", StandardScaler())]), NUM),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT)])),
        ("m", LogisticRegression(max_iter=2000, random_state=42))])


results = []

# (i) plain median
p1 = build(SimpleImputer(strategy="median")).fit(X_tr, y_tr)
pr = p1.predict_proba(X_va)[:, 1]
results.append(("median only", len(X_tr), accuracy_score(y_va, pr >= .5), roc_auc_score(y_va, pr)))

# (ii) median + indicator
p2 = build(SimpleImputer(strategy="median", add_indicator=True)).fit(X_tr, y_tr)
pr = p2.predict_proba(X_va)[:, 1]
results.append(("median + indicator", len(X_tr), accuracy_score(y_va, pr >= .5), roc_auc_score(y_va, pr)))

# (iii) drop rows with any missing value
mask_tr = X_tr.notna().all(axis=1)
p3 = build(SimpleImputer(strategy="median")).fit(X_tr[mask_tr], y_tr[mask_tr])
pr = p3.predict_proba(X_va)[:, 1]
results.append(("drop missing rows", int(mask_tr.sum()),
                accuracy_score(y_va, pr >= .5), roc_auc_score(y_va, pr)))

print(pd.DataFrame(results, columns=["strategy", "train_rows", "accuracy", "roc_auc"]
                   ).round(4).to_string(index=False))

names = p2.named_steps["pre"].get_feature_names_out()
co = pd.Series(p2.named_steps["m"].coef_[0], index=names)
print(co[[n for n in names if "missing" in n]].round(3))
```

Expected: **(ii) wins.** With missingness concentrated among rookie drivers, the indicator column is a proxy for "inexperienced," and it should carry a clearly **positive** coefficient — missing experience predicts *more* lateness. Median imputation alone destroys that information by writing 29.5 (a mid-career value) into every rookie's row. Dropping rows is worst: it loses training data *and* systematically removes rookies, which biases the model toward a driver population that isn't the one it will score.

**Interpreting the sign.** A positive coefficient on the indicator means "this row being blank makes lateness more likely." That is not a statement about missing data. It is a statement about *who* has missing data. If your operations team ever fixes the paperwork process, this feature's meaning changes overnight — which belongs in the model card's known-limitations section.

### 5 — Build your own leak, then catch it

In `make_data.py`, inside the `add_leak` block:

```python
        df["driver_shift_overtime_minutes"] = np.maximum(
            0, 25 * df["late"] + rng.normal(5, 8, n)).round(1)
```

```python
"""detect_leaks.py — three independent leak tests.

Continues from ablation.py: X_tr, X_va, y_tr, y_va are already defined there.
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

CORR_THRESHOLD = 0.60
AUC_THRESHOLD = 0.80

numeric = X_tr.select_dtypes(include=[np.number]).columns.tolist()

print("--- test 1: |correlation with target| ---")
corr = pd.concat([X_tr[numeric], y_tr], axis=1).corr()[y_tr.name].drop(y_tr.name)
for col, c in corr.abs().sort_values(ascending=False).items():
    flag = "  <== SUSPECT" if c > CORR_THRESHOLD else ""
    print(f"{col:<34s} {c:.3f}{flag}")

print("\n--- test 2: single-feature validation AUC ---")
for col in numeric:
    m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    tr_col = X_tr[[col]].fillna(X_tr[col].median())
    va_col = X_va[[col]].fillna(X_tr[col].median())
    auc = roc_auc_score(y_va, m.fit(tr_col, y_tr).predict_proba(va_col)[:, 1])
    flag = "  <== SUSPECT" if auc > AUC_THRESHOLD else ""
    print(f"{col:<34s} {auc:.3f}{flag}")

print("\n--- test 3: the human checklist (cannot be automated) ---")
for col in X_tr.columns:
    print(f"[ ] {col:<34s}  known at the moment of prediction? (y/n)")
```

**Expected findings.** With overtime generated as `25 × late + N(5, 8)`, the two groups are centred at 5 minutes (on time) and 30 minutes (late) with σ = 8. Measured on the full table: correlation **0.845**, single-feature AUC **0.987**. Both tests fire loudly.

Now make it subtler. Widen the noise to `rng.normal(5, 18, n)` and the distributions overlap heavily:

| noise σ | correlation | single-feature AUC | test 1 (>0.60)? | test 2 (>0.80)? |
|---|---|---|---|---|
| 8 | 0.845 | 0.987 | 🔴 fires | 🔴 fires |
| 15 | 0.627 | 0.873 | 🔴 fires | 🔴 fires |
| **18** | **0.544** | **0.827** | ⚪ silent | 🔴 fires |
| 25 | 0.414 | 0.754 | ⚪ silent | ⚪ silent |

At σ = 18 the correlation test misses it completely and only the AUC test catches it. At σ = 25 both statistical tests go quiet — and the column is *still* leakage, still worth an easy 0.75 AUC on its own, and still empty at prediction time. **That is the point of running more than one test, and the point of test 3.**

**Why test 3 can never be automated.** Tests 1 and 2 only measure how strongly a column relates to the target — and a genuinely excellent feature also relates strongly to the target. The statistics literally cannot distinguish "this feature is very predictive" from "this feature is the answer in disguise." What separates them is a fact about the *world*: the order in which events happen and the moment your system is asked for a prediction. That fact is not in the dataset. It lives in the operational process, and the only place to get it is a conversation with the person who runs that process. Every leak you have ever seen was found by somebody asking a human a question.

### 6 — Target encoding, done wrong then right

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler

# Continues from ablation.py: df, X_tr, X_va, y_tr, y_va are already defined there.
FEATS = ["distance_km", "items", "prep_minutes", "order_hour"]

# ---------- (a) WRONG: means computed on everything, before splitting ----------
global_means = df.groupby("restaurant")["late"].mean()
Xw_tr = X_tr[FEATS].copy()
Xw_va = X_va[FEATS].copy()
Xw_tr["rest_te"] = X_tr["restaurant"].map(global_means)
Xw_va["rest_te"] = X_va["restaurant"].map(global_means)
sc = StandardScaler().fit(Xw_tr)
m = LogisticRegression(max_iter=2000).fit(sc.transform(Xw_tr), y_tr)
print("WRONG target encoding AUC: %.4f"
      % roc_auc_score(y_va, m.predict_proba(sc.transform(Xw_va))[:, 1]))

# ---------- (b) RIGHT: out-of-fold means, computed from train only ----------
oof = pd.Series(np.nan, index=X_tr.index)
prior = y_tr.mean()
for fit_idx, enc_idx in StratifiedKFold(5, shuffle=True, random_state=0).split(X_tr, y_tr):
    fold_means = y_tr.iloc[fit_idx].groupby(X_tr["restaurant"].iloc[fit_idx]).mean()
    oof.iloc[enc_idx] = X_tr["restaurant"].iloc[enc_idx].map(fold_means).fillna(prior).values

train_means = y_tr.groupby(X_tr["restaurant"]).mean()      # for scoring new rows
Xr_tr = X_tr[FEATS].copy()
Xr_va = X_va[FEATS].copy()
Xr_tr["rest_te"] = oof.values
Xr_va["rest_te"] = X_va["restaurant"].map(train_means).fillna(prior).values
sc = StandardScaler().fit(Xr_tr)
m = LogisticRegression(max_iter=2000).fit(sc.transform(Xr_tr), y_tr)
print("RIGHT target encoding AUC: %.4f"
      % roc_auc_score(y_va, m.predict_proba(sc.transform(Xr_va))[:, 1]))
```

With only 5 restaurants, the rarest seen 150 times in training, the two versions will land close together — the leak is real but small, because a mean over 240 rows barely changes when you remove one of them. That is itself worth noticing: leakage severity scales with how few rows go into each learned statistic.

**Why it collapses for rare categories.** Imagine adding a sixth restaurant seen exactly 3 times:

| restaurant | n in train | late count | mean target |
|---|---|---|---|
| CrustyBros | 229 | 90 | 0.393 |
| GreenLeaf | 150 | 45 | 0.300 |
| Napoli | 323 | 71 | 0.220 |
| SliceHouse | 309 | 82 | 0.265 |
| TandooriPizza | 189 | 57 | 0.302 |
| **PopUpPizza** | **3** | **3** | **1.000** |

(The first five rows are the real counts from our 1,200-row training split; PopUpPizza is the hypothetical rare category.)

For a PopUpPizza row, the "wrong" encoding gives 1.000 — and that 1.000 was computed from a set of three rows that *includes the row being encoded*. One-third of that feature's value for that row is literally that row's own label. The model learns "when `rest_te` is 1.0, the answer is 1," which is true on training data and meaningless everywhere else.

Out-of-fold encoding fixes it: when PopUpPizza row #1 is in the encoding fold, its value comes from rows #2 and #3 only, giving a mean over two rows — still noisy, but no longer self-referential. The standard extra defence is **smoothing**, blending the category mean toward the overall prior in proportion to how few rows the category has:

$$ \text{encoded} = \frac{n_{\text{cat}} \cdot \bar{y}_{\text{cat}} + k \cdot \bar{y}_{\text{global}}}{n_{\text{cat}} + k} $$

With k = 20 and the training prior 0.2875, PopUpPizza's encoding becomes (3 × 1.000 + 20 × 0.2875) / 23 = (3.000 + 5.750) / 23 = **0.3804** — barely above the prior, which is exactly the right amount of confidence to have after three observations.

</details>

---

[⬅ Previous](module-01-the-supervised-pipeline.md) · [Level 3 Home](README.md) · [Next ➡](module-03-evaluation-metrics.md)

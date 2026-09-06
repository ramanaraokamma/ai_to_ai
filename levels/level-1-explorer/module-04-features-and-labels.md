# Module 4 — Features and Labels: How a Machine Describes a Thing

**Level 1 · Module 4 · ~3 hours · Prereqs: Module 2 (rows, columns, data types, data cards), Module 3 (patterns, if-then rules, the machine learning trade)**

[⬅ Previous](module-03-patterns-and-rules.md) · [Level 1 Home](README.md) · [Next ➡](module-05-learning-from-examples.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** name the features and the label for any prediction task somebody describes to you, in under a minute.
2. **You will be able to** turn a real physical object you are holding into a row of 4–6 measured features.
3. **You will be able to** judge whether a feature is **useful**, **useless**, or **sneaky**, and back your judgement with counting evidence — not a feeling.
4. **You will be able to** tell a classification task apart from a number-prediction task, and convert one into the other.
5. **You will be able to** look at a finished feature table and say what the machine actually knows — and, more importantly, what it has no idea about.

---

## 🪝 The Hook

Put an apple on the table in front of you. Look at it.

You just did something staggeringly complicated and it felt like nothing. Light bounced off the apple, hit your eye, and about a hundred million cells fired. Your brain sorted through that flood and produced one word: *apple*. It took you roughly a fifth of a second and you didn't have to try.

Now hand the apple to a computer.

It can't look. There is no looking. Whatever the computer is going to know about that apple, **somebody has to write down as numbers first** — and that somebody, for the next three hours, is you. You choose what to measure. Weight? Colour? Whether it has a stem? The computer will never know a single thing you did not choose to write down.

That is the uncomfortable and rather thrilling fact underneath every AI system on earth. In Module 3 you agreed to stop writing rules and start giving the machine labelled examples instead. Fine. But an "example" is not a real apple. An example is **a row of numbers you picked, plus the answer you want back**. Pick the wrong numbers and the smartest algorithm in the world learns nothing.

---

## 🧠 The Concept

Five ideas. Each gets a plain explanation, an everyday anchor, and a small example with real numbers.

---

### 1️⃣ A feature is one measured description of one example

Here is the whole idea in one picture:

```
        THE REAL THING                       WHAT THE MACHINE ACTUALLY GETS
       ┌───────────────┐                ┌────────┬────────┬────────┬────────┐
       │               │   you choose   │ weight │ length │ colour │  skin  │
       │   a real red  │  and  measure  ├────────┼────────┼────────┼────────┤
       │     apple     │ ─────────────► │  150   │   8    │  red   │ smooth │
       │               │   4 features   └────────┴────────┴────────┴────────┘
       └───────────────┘                            ONE ROW
        smell, taste, the                    everything else about the
        bruise on the back,                  apple has been thrown away
        who gave it to you...                      forever
```

> **Feature** — one measured description of one example. One column in your table.

Notice the word **measured**. A feature has to be something you can actually write down the same way twice. "Weight in grams" is a feature. "Nice-looking" is not a feature until you turn it into something countable — like "number of bruises" or "a 1-to-5 score three people agreed on."

You already met the container for this in Module 2: **one row per example, one column per thing you measured.** A feature is just the new name for one of those columns, used when the table's job is to predict something.

**🍕 Analogy — the missing-person poster.**
A police poster can't show the person. It shows *chosen features*: height 165 cm, hair black, wearing a blue jacket, aged about 30. Anyone reading the poster knows only those four things. If the poster leaves off "walks with a limp," nobody in the whole city can use the limp — no matter how obvious it is in real life. The machine's feature list is the poster. Whatever you leave off does not exist.

**🔢 Tiny example — three features of your own hand.**

Put your left hand flat on a table and measure it:

| feature | how I measured it | value |
|---|---|---|
| `length_cm` | wrist crease to tip of middle finger, ruler | 17.5 |
| `width_cm` | across the knuckles, ruler | 8.0 |
| `finger_count` | count | 5 |

Your hand is now this row: `17.5, 8.0, 5`. That is genuinely all a machine would get. Notice how much is gone — the scar, the warmth, whose hand it is. Also notice something sneaky about `finger_count`: it is **5** for almost every hand on earth. A column where every row says the same thing tells the machine nothing at all. Hold that thought; it comes back in sub-concept 3.

---

### 2️⃣ A label is the answer you want the machine to produce

Every prediction task has a question in it. The label is the answer to that question, written down for examples where you already know it.

> **Label** — the answer you want the machine to output. In your table it is one special column, marked as the thing to be guessed.

The label is not magic and it is not different in shape from a feature — it's just a column. What makes it the label is **your decision** that this is the column you'll hide and ask the machine to reconstruct.

**🍕 Analogy — flashcards.**
A flashcard has a front and a back. Front: the features (a picture of a plant, or the word *bonjour*). Back: the label (`fern`, or `hello`). You study by looking at the front and trying to produce the back. That's it. That is exactly what a machine learning system does, a few million times, without getting bored.

**🔢 Tiny example — same features, two different labels.**

Here are four school days:

| sleep_hours | screen_minutes | homework_minutes | mood_1to5 | felt_tired |
|---|---|---|---|---|
| 8.5 | 40 | 45 | 4 | no |
| 5.0 | 180 | 20 | 2 | yes |
| 7.0 | 90 | 60 | 4 | no |
| 5.5 | 150 | 30 | 2 | yes |

If your question is **"will I feel tired tomorrow?"**, then `felt_tired` is the label and the other four columns are features.

If your question is **"what will my mood be?"**, then `mood_1to5` becomes the label — and `felt_tired` becomes just another feature.

Same table. Different question. Different label. **The label is a choice, not a property of the data.** This trips up a lot of adults.

---

### 3️⃣ Feature quality: useful, useless, and sneaky

Not all features are worth the ink. Three kinds are worth naming, and only one of them is good.

> **Useful feature** — knowing it makes your guess better than guessing without it.
> **Useless feature** — knowing it makes no difference at all.
> **Leaky feature** — knowing it makes your guess *perfect*, because it secretly contains the answer. Also called a **sneaky feature**, because it fools you into thinking your system works.

**Useless features** are annoying but honest. `finger_count` from earlier is useless for telling hands apart — every row says 5. So is "was the photo taken on planet Earth."

**Leaky features** are the dangerous ones, and they're dangerous *because they look like a triumph*.

> **Leak** — a feature that would not actually be available at the moment you need to make the prediction, usually because it only exists **after** the answer is already known.

**🍕 Analogy — the wet umbrella.**
You want to predict "is it raining outside?" You collect features: temperature, cloud colour, wind, and — `is_my_umbrella_wet`. Your predictor is 100% accurate! Amazing! Except your umbrella only gets wet *after you have already been outside in the rain*. At the moment you actually need the prediction — standing at the door, deciding whether to take a coat — the umbrella is dry. Your perfect system is worth nothing.

That is a leak. It scores brilliantly on old data and fails completely in real use.

**🔢 Tiny example — spotting the leak in three seconds.**

You want to predict, on Monday, whether a student will pass the exam on Friday.

| feature | available on Monday? | verdict |
|---|---|---|
| `attendance_percent` | yes | fine |
| `homework_average` | yes | fine |
| `hours_of_sleep_per_night` | yes | fine |
| `exam_score_out_of_100` | **no — it's Friday's result** | 🚨 LEAK |

The three-second test: **stand at the moment of prediction and ask "do I have this yet?"** If the honest answer is "no, that comes later," it's a leak. Cross it out.

⚠️ A warning that will save you real pain later: a leaky feature does not announce itself. Nobody labels a column `THE_ANSWER`. It'll be called `case_status`, or `refund_issued`, or `days_in_hospital`. You have to go looking.

---

### 4️⃣ Classification asks "which one?" — regression asks "how much?"

Look at the label column. Its *type* decides what kind of task you have. You already learned data types in Module 2, and now they earn their keep.

> **Classification** — the label is a category from a short fixed list. *Which one is it?*
> **Regression** — the label is a number on a sliding scale. *How much / how many?*

```
      CLASSIFICATION                              REGRESSION
   "which box does it go in?"               "where on the line does it sit?"

   ┌───────┐ ┌───────┐ ┌───────┐            0────20────40────60────80───►
   │ apple │ │orange │ │banana │                       ▲
   └───────┘ └───────┘ └───────┘                     47 min
      pick exactly one box                    any number is allowed

   labels: apple / orange / banana           labels: 12, 47.5, 80, 3.25 ...
   "was it right?"  → yes or no              "how far off?" → 5 minutes off
```

**🍕 Analogy — the two kinds of question a teacher asks.**
"Which country is this flag from?" is multiple choice. There is a right box and wrong boxes. "How long will the school trip take?" is not multiple choice — 95 minutes is *nearly* right if the answer is 90, whereas in multiple choice "nearly right" doesn't exist.

That is the deep difference, and it changes how you'll grade the machine later: in classification a guess is right or wrong; in regression a guess is **off by an amount**.

**🔢 Tiny example — the same afternoon, two tasks.**

| task | label | label type | kind |
|---|---|---|---|
| Will I finish my homework before dinner? | yes / no | category | classification |
| How many minutes will my homework take? | 47 | number | regression |
| Which subject is this homework? | maths / english / science | category | classification |
| How many pages will I get through? | 6 | number | regression |

Two things worth noticing:

- A classification task with only two boxes (yes/no, spam/not spam) is called **binary classification**. Three or more boxes is **multi-class classification**. Module 5's Teachable Machine model will be multi-class with three boxes.
- You can usually convert between the two by **bucketing**. "How many minutes?" (regression) becomes "under 30 / 30–60 / over 60" (classification). You gain simplicity and lose precision. Whether that's a good trade depends entirely on what you're going to *do* with the answer.

---

### 5️⃣ The feature table: many rows of features, one label column

Now put it together. This shape is the workhorse of the entire field, and you will see it again in every single level of this course.

```
                       ◄────── FEATURES (the poster) ──────►   ◄─ LABEL ─►
              ┌──────┬──────────┬──────────┬────────┬────────┐┌──────────┐
   header →   │  id  │ weight_g │ length_cm│ colour │  skin  ││  fruit   │
              ├──────┼──────────┼──────────┼────────┼────────┤├──────────┤
   example 1  │  1   │   150    │    8     │  red   │ smooth ││  apple   │
   example 2  │  2   │   200    │    8     │ orange │ bumpy  ││  orange  │
   example 3  │  3   │   120    │   19     │ yellow │ smooth ││  banana  │
      ...     │ ...  │   ...    │   ...    │  ...   │  ...   ││   ...    │
   example 12 │  12  │   128    │   20     │ yellow │ smooth ││  banana  │
              └──────┴──────────┴──────────┴────────┴────────┘└──────────┘
                       ▲                                          ▲
                 what you show it                        what you cover up
                                                          and ask it to guess
```

> **Feature table** — a table where every row is one example, most columns are features, and exactly one column is the label.

Three rules that make a feature table honest:

1. **One row = one example.** If the same apple appears twice, you have secretly told the machine that apple matters twice as much.
2. **Every row is filled in the same way.** If `length_cm` means "longest side" in row 3 and "widest side" in row 7, the column is nonsense even though it looks fine.
3. **The label column is the last column, and you say so out loud.** Write it in your data card (Module 2). Future-you will not remember.

**🔢 Tiny example — how much a table "knows."**

A table with 12 rows and 5 features holds 12 × 5 = **60 measurements**. That's it. Sixty numbers and words is the entire universe available to your machine. Meanwhile you, glancing at the fruit bowl, take in millions of details per second.

This is worth sitting with, because it explains almost every stupid mistake an AI ever makes. **A model isn't dumb. It's blindfolded, and you chose the blindfold.**

---

## 🔍 Worked Example

**The Fruit Bowl.** We'll go from a real bowl of fruit to a finished, judged feature table, then use it to predict. Every number is shown. Nothing is skipped.

### Step 1 — The examples

Twelve real pieces of fruit sitting in a bowl: 4 apples, 4 oranges, 4 bananas. Each one will become one row.

The bowl is divided into four imaginary quadrants (top-left, top-right, bottom-left, bottom-right) and it happens that each quadrant holds one apple, one orange, and one banana. Remember that — it matters in Step 5.

### Step 2 — Choose the label

The question: **"Given a piece of fruit, which of the three types is it?"**

So the label is `fruit`, with three possible values: `apple`, `orange`, `banana`. Three fixed boxes → this is **multi-class classification**.

### Step 3 — Brainstorm candidate features

Before measuring anything, list everything you *could* measure. Be greedy at this stage; you'll cut later.

1. `weight_g` — kitchen scale, grams
2. `length_cm` — longest dimension, ruler
3. `colour` — one word from {red, green, yellow, orange}
4. `skin` — smooth or bumpy, by touch
5. `has_stem` — yes or no
6. `quadrant` — where it was sitting in the bowl
7. `sticker_says` — the word printed on the supermarket sticker

Seven candidates. Some are about to turn out to be rubbish. **That's the point of measuring first and judging second.**

### Step 4 — Measure. Here is the raw feature table.

| id | weight_g | length_cm | colour | skin | has_stem | quadrant | sticker_says | **fruit** |
|---|---|---|---|---|---|---|---|---|
| 1 | 150 | 8 | red | smooth | yes | top-left | APPLE | **apple** |
| 2 | 165 | 8 | green | smooth | yes | top-right | APPLE | **apple** |
| 3 | 140 | 7 | red | smooth | yes | bottom-left | APPLE | **apple** |
| 4 | 190 | 9 | red | smooth | no | bottom-right | APPLE | **apple** |
| 5 | 200 | 8 | orange | bumpy | no | top-left | ORANGE | **orange** |
| 6 | 185 | 7 | orange | bumpy | no | top-right | ORANGE | **orange** |
| 7 | 210 | 8 | orange | bumpy | no | bottom-left | ORANGE | **orange** |
| 8 | 195 | 8 | orange | bumpy | no | bottom-right | ORANGE | **orange** |
| 9 | 120 | 19 | yellow | smooth | no | top-left | BANANA | **banana** |
| 10 | 135 | 21 | yellow | smooth | no | top-right | BANANA | **banana** |
| 11 | 110 | 18 | green | smooth | no | bottom-left | BANANA | **banana** |
| 12 | 128 | 20 | yellow | smooth | no | bottom-right | BANANA | **banana** |

12 rows × 7 features = **84 measurements**. Everything else about these twelve fruits is now gone.

### Step 5 — Judge every feature by counting

Here's the honest way to judge a feature, and you can do it with a pencil. **For each feature, write the best possible one-feature rule, then count how many of the 12 rows it gets right.**

First you need something to compare against.

**The baseline.** If you ignored every feature and always guessed the most common label, how well would you do? Counts are apple 4, orange 4, banana 4 — a three-way tie. So the best blind guess gets **4 out of 12 = 33.3%**. Any feature that can't beat 33.3% is worthless.

---

**Feature: `quadrant`**

| quadrant | apples | oranges | bananas | best guess gets |
|---|---|---|---|---|
| top-left | 1 | 1 | 1 | 1 of 3 |
| top-right | 1 | 1 | 1 | 1 of 3 |
| bottom-left | 1 | 1 | 1 | 1 of 3 |
| bottom-right | 1 | 1 | 1 | 1 of 3 |

Total: 1 + 1 + 1 + 1 = **4 out of 12 = 33.3%.** Exactly the baseline. Knowing where the fruit sat in the bowl tells you **nothing**. 👉 **USELESS.** Cut it.

---

**Feature: `has_stem`**

| has_stem | apples | oranges | bananas | best guess | gets right |
|---|---|---|---|---|---|
| yes | 3 | 0 | 0 | apple | 3 of 3 |
| no | 1 | 4 | 4 | orange (tie, pick one) | 4 of 9 |

Total: 3 + 4 = **7 out of 12 = 58.3%.** Beats the baseline, so it's not useless — but look closer. When `has_stem = yes` it is a *perfect* apple detector. When it's `no`, it's nearly worthless. 👉 **WEAK, but keep it** — a feature that is only sometimes decisive can still help alongside others.

---

**Feature: `skin`**

| skin | apples | oranges | bananas | best guess | gets right |
|---|---|---|---|---|---|
| bumpy | 0 | 4 | 0 | orange | 4 of 4 |
| smooth | 4 | 0 | 4 | apple (tie) | 4 of 8 |

Total: 4 + 4 = **8 out of 12 = 66.7%.** More importantly: `skin` answers the question *"orange or not orange?"* with **12 out of 12** correctness. 👉 **USEFUL — a perfect specialist.**

---

**Feature: `length_cm`**

Sort the values: bananas are 18, 19, 20, 21. Everything else is 7, 7, 8, 8, 8, 8, 8, 9. There is a huge empty gap between 9 and 18.

Rule: `IF length_cm >= 15 THEN banana ELSE apple` (picking apple to break the apple/orange tie).

| rows | prediction | correct |
|---|---|---|
| 9, 10, 11, 12 (length 18–21) | banana | 4 of 4 ✓ |
| 1, 2, 3, 4 (length 7–9) | apple | 4 of 4 ✓ |
| 5, 6, 7, 8 (length 7–8) | apple | 0 of 4 ✗ |

Total: **8 out of 12 = 66.7%.** And like `skin`, it's a perfect specialist: *"banana or not banana?"* → **12 out of 12**. 👉 **USEFUL.**

---

**Feature: `weight_g`**

Sorted by class:
- bananas: 110, 120, 128, 135 → range **110–135**
- apples: 140, 150, 165, 190 → range **140–190**
- oranges: 185, 195, 200, 210 → range **185–210**

Bananas separate cleanly. Apples and oranges **overlap** between 185 and 190. Best three-band rule:

`IF weight < 138 THEN banana; ELSE IF weight <= 187 THEN apple; ELSE orange`

| id | weight | predicted | true | ✓/✗ |
|---|---|---|---|---|
| 1 | 150 | apple | apple | ✓ |
| 2 | 165 | apple | apple | ✓ |
| 3 | 140 | apple | apple | ✓ |
| 4 | 190 | orange | apple | ✗ |
| 5 | 200 | orange | orange | ✓ |
| 6 | 185 | apple | orange | ✗ |
| 7 | 210 | orange | orange | ✓ |
| 8 | 195 | orange | orange | ✓ |
| 9 | 120 | banana | banana | ✓ |
| 10 | 135 | banana | banana | ✓ |
| 11 | 110 | banana | banana | ✓ |
| 12 | 128 | banana | banana | ✓ |

Total: **10 out of 12 = 83.3%.** 👉 **USEFUL, but imperfect** — one heavy apple and one light orange sit in each other's territory. Real measurements do this constantly.

---

**Feature: `colour`**

| colour | apples | oranges | bananas | best guess | gets right |
|---|---|---|---|---|---|
| red | 3 | 0 | 0 | apple | 3 of 3 |
| orange | 0 | 4 | 0 | orange | 4 of 4 |
| yellow | 0 | 0 | 3 | banana | 3 of 3 |
| green | 1 | 0 | 1 | apple (tie) | 1 of 2 |

Total: 3 + 4 + 3 + 1 = **11 out of 12 = 91.7%.** 👉 **VERY USEFUL.** Only green is ambiguous — a green apple and an unripe banana.

---

**Feature: `sticker_says`**

| sticker | apples | oranges | bananas | gets right |
|---|---|---|---|---|
| APPLE | 4 | 0 | 0 | 4 of 4 |
| ORANGE | 0 | 4 | 0 | 4 of 4 |
| BANANA | 0 | 0 | 4 | 4 of 4 |

Total: **12 out of 12 = 100%.** Perfect!

Now apply the three-second test. **At the moment you need the prediction, do you have this?** You are holding a fruit and asking a machine what it is. If it already has a sticker saying APPLE… you didn't need a machine. And the moment someone hands you fruit from their garden, the feature is blank and your perfect model has nothing. 👉 🚨 **LEAKY.** Cut it, no matter how good the score looks.

### Step 6 — The scoreboard

| feature | best one-feature score | vs baseline 33.3% | verdict |
|---|---|---|---|
| `sticker_says` | 12/12 = **100%** | +66.7 | 🚨 **LEAKY — remove** |
| `colour` | 11/12 = **91.7%** | +58.4 | ✅ very useful |
| `weight_g` | 10/12 = **83.3%** | +50.0 | ✅ useful |
| `length_cm` | 8/12 = **66.7%** | +33.4 | ✅ useful (banana specialist) |
| `skin` | 8/12 = **66.7%** | +33.4 | ✅ useful (orange specialist) |
| `has_stem` | 7/12 = **58.3%** | +25.0 | 🟡 weak, keep |
| `quadrant` | 4/12 = **33.3%** | 0.0 | ❌ useless — remove |

Final feature list: **`weight_g`, `length_cm`, `colour`, `skin`, `has_stem`** — five features, one label. Two columns deleted, and the model just got *more* trustworthy by knowing *less*.

### Step 7 — Two features beat five

Here's the payoff. `length_cm` is a perfect banana detector. `skin` is a perfect orange detector. Chain them (using first-match-wins, exactly as in Module 3):

```
RULE 1: IF length_cm >= 15        THEN banana
RULE 2: ELSE IF skin = bumpy      THEN orange
RULE 3: OTHERWISE                 THEN apple
```

Score it on all twelve rows:

| id | length | skin | rule that fires | predicted | true | ✓/✗ |
|---|---|---|---|---|---|---|
| 1 | 8 | smooth | 3 | apple | apple | ✓ |
| 2 | 8 | smooth | 3 | apple | apple | ✓ |
| 3 | 7 | smooth | 3 | apple | apple | ✓ |
| 4 | 9 | smooth | 3 | apple | apple | ✓ |
| 5 | 8 | bumpy | 2 | orange | orange | ✓ |
| 6 | 7 | bumpy | 2 | orange | orange | ✓ |
| 7 | 8 | bumpy | 2 | orange | orange | ✓ |
| 8 | 8 | bumpy | 2 | orange | orange | ✓ |
| 9 | 19 | smooth | 1 | banana | banana | ✓ |
| 10 | 21 | smooth | 1 | banana | banana | ✓ |
| 11 | 18 | smooth | 1 | banana | banana | ✓ |
| 12 | 20 | smooth | 1 | banana | banana | ✓ |

**12 out of 12 = 100%** — with two honest features and no leak. Two well-chosen features beat five mediocre ones. **Feature choice is most of the job.**

### Step 8 — Predict three new fruits

Someone hands you three fruits that were never in the bowl.

**Fruit A:** weight 205 g, length 8 cm, colour orange, skin bumpy, no stem.
→ Rule 1? 8 ≥ 15 is false. Rule 2? bumpy is true → **predict orange.** It was an orange. ✓

**Fruit B:** weight 145 g, length 8 cm, colour green, skin smooth, has stem.
→ Rule 1? no. Rule 2? no. Rule 3 fires → **predict apple.** It was a green apple. ✓ (Note that `colour = green` would have got this wrong on its own — the 91.7% feature loses to the two-feature rule here.)

**Fruit C:** weight 70 g, length 5 cm, colour green, skin bumpy, no stem.
→ Rule 1? no. Rule 2? bumpy → **predict orange.**

It was a **lime**.

Read that again, because it is the most important line in the module. The system was not wrong in some fixable way. **It cannot output "lime."** There is no lime box. You gave it three boxes and it will force every object on earth into one of them, forever, with total confidence. A feature table defines not just what the machine can see but what it is even *capable of saying*.

### Step 9 — Same table, different label: now it's regression

Keep all twelve rows. Change nothing except which column you cover up. Cover **`weight_g`** and treat `fruit`, `length_cm`, `colour`, `skin`, `has_stem` as features.

The label is now a number → this is **regression**.

A simple predictor: *guess the average weight of that fruit type.*

- apples: (150 + 165 + 140 + 190) ÷ 4 = 645 ÷ 4 = **161.25 g**
- oranges: (200 + 185 + 210 + 195) ÷ 4 = 790 ÷ 4 = **197.5 g**
- bananas: (120 + 135 + 110 + 128) ÷ 4 = 493 ÷ 4 = **123.25 g**

New orange arrives. Predict **197.5 g**. It actually weighs 205 g.

Was that right? The question doesn't apply. In regression you ask **how far off**:

> error = |205 − 197.5| = **7.5 grams**

New banana arrives, predicted 123.25 g, actually weighs 119 g → error = |119 − 123.25| = **4.25 grams**.

Average error across those two = (7.5 + 4.25) ÷ 2 = 11.75 ÷ 2 = **5.875 grams**.

Same twelve fruits. Same measurements. **One decision — which column is the label — turned a "which box?" problem into a "how far off?" problem.**

---

## 💻 Hands-On

No programming here — Level 1 keeps your hands on real objects and a spreadsheet. Four activities, about 55 minutes total.

### Activity A — Measure a real object into a row (15 min)

**You need:** 3 objects from your kitchen or desk, a ruler, and a kitchen scale (a phone scale app is fine; if you have no scale, use "heavier / lighter than a full water bottle" as a 3-level category instead).

1. Pick your three objects. Make them *similar enough to be confusable* — three spoons of different sizes is a better exercise than a spoon, a sofa, and a cat.
2. **Before measuring**, write your label question at the top of the page. Example: *"Is this a teaspoon, a tablespoon, or a serving spoon?"*
3. Decide on five features and — this is the part people skip — **write the exact measuring instruction for each**:

```
FEATURE SHEET
label question: teaspoon / tablespoon / serving spoon?

f1  length_cm     ruler, tip of handle to tip of bowl, nearest 0.5 cm
f2  bowl_width_cm ruler, widest point of the scooping part, nearest 0.5 cm
f3  weight_g      kitchen scale, nearest gram
f4  material      one of {steel, plastic, wood}
f5  handle_shape  one of {straight, curved}
```

4. Measure all three objects. Fill in this table:

| id | length_cm | bowl_width_cm | weight_g | material | handle_shape | **label** |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |

5. **Hand your feature sheet and one object to someone else** and have them measure it. Do you get the same numbers? Every disagreement is a badly written instruction — fix the wording, not the person.

✅ **Done when:** all 15 cells are filled and a second person reproduced at least 4 of your 5 measurements on one object.

---

### Activity B — Build the fruit-bowl table in a spreadsheet (15 min)

Open Google Sheets (or Excel, or LibreOffice Calc). Type the Worked Example table in exactly this layout so the formulas below work.

| | A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|---|
| **1** | id | weight_g | length_cm | colour | skin | has_stem | quadrant | sticker_says | fruit |
| **2** | 1 | 150 | 8 | red | smooth | yes | top-left | APPLE | apple |
| **3** | 2 | 165 | 8 | green | smooth | yes | top-right | APPLE | apple |
| **4** | 3 | 140 | 7 | red | smooth | yes | bottom-left | APPLE | apple |
| **5** | 4 | 190 | 9 | red | smooth | no | bottom-right | APPLE | apple |
| **6** | 5 | 200 | 8 | orange | bumpy | no | top-left | ORANGE | orange |
| **7** | 6 | 185 | 7 | orange | bumpy | no | top-right | ORANGE | orange |
| **8** | 7 | 210 | 8 | orange | bumpy | no | bottom-left | ORANGE | orange |
| **9** | 8 | 195 | 8 | orange | bumpy | no | bottom-right | ORANGE | orange |
| **10** | 9 | 120 | 19 | yellow | smooth | no | top-left | BANANA | banana |
| **11** | 10 | 135 | 21 | yellow | smooth | no | top-right | BANANA | banana |
| **12** | 11 | 110 | 18 | green | smooth | no | bottom-left | BANANA | banana |
| **13** | 12 | 128 | 20 | yellow | smooth | no | bottom-right | BANANA | banana |

Data rows are **2 to 13**. Column **I** is the label.

**B1 — count your classes.** In cell `K2`, `K3`, `K4`:

```
=COUNTIF($I$2:$I$13, "apple")
=COUNTIF($I$2:$I$13, "orange")
=COUNTIF($I$2:$I$13, "banana")
```

Expected output: `4`, `4`, `4`. (Always do this first. A table with 40 of one class and 3 of another is a problem, and Module 5 explains exactly why.)

**B2 — the regression averages from Step 9.** In `L2`, `L3`, `L4`:

```
=AVERAGEIF($I$2:$I$13, "apple",  $B$2:$B$13)
=AVERAGEIF($I$2:$I$13, "orange", $B$2:$B$13)
=AVERAGEIF($I$2:$I$13, "banana", $B$2:$B$13)
```

Expected output: `161.25`, `197.5`, `123.25`. These match the hand arithmetic in Step 9 exactly. 🎉

**B3 — does `weight_g` actually separate apples from oranges?** In `M2` and `M3`:

```
=MAXIFS($B$2:$B$13, $I$2:$I$13, "apple")
=MINIFS($B$2:$B$13, $I$2:$I$13, "orange")
```

Expected output: `190` and `185`. Now the verdict, in `M4`:

```
=IF( MAXIFS($B$2:$B$13,$I$2:$I$13,"apple") >= MINIFS($B$2:$B$13,$I$2:$I$13,"orange"),
     "RANGES OVERLAP", "clean split" )
```

Expected output: `RANGES OVERLAP` — because 190 ≥ 185. That single cell is a reusable overlap detector for any two classes.

**B4 — the leak detector.** In `N2`, then drag down to `N13`:

```
=IF( EXACT(UPPER($H2), UPPER($I2)), "LEAK", "ok" )
```

Expected output: `LEAK` in all twelve rows. `UPPER()` makes `APPLE` and `apple` match; `EXACT()` then compares them character for character. **Any feature column that equals the label column on nearly every row is a leak suspect.**

> ⚠️ `MAXIFS` and `MINIFS` exist in Google Sheets, LibreOffice Calc, and Excel 2019 or newer. On an older Excel, use `=MAX(IF($I$2:$I$13="apple",$B$2:$B$13))` and press **Ctrl+Shift+Enter** instead of Enter.

---

### Activity C — The leak hunt, unplugged (10 min)

For each prediction task below, one feature in the list is leaky. Say which, and say **when** that feature actually becomes known.

| # | task | candidate features |
|---|---|---|
| 1 | Will this parcel arrive late? | distance_km · weight_kg · courier_company · **customer_complaint_filed** |
| 2 | Will this student join the football team? | height_cm · runs_at_break · sport_played_last_year · **team_shirt_number** |
| 3 | Will it rain tomorrow? | today_humidity · today_pressure · month · **tomorrow_umbrella_sales** |
| 4 | Is this song going to be a hit? | tempo_bpm · length_seconds · artist_followers · **weeks_in_top_10** |

Write your four answers before you look at the pattern — then notice it: **every leak is something from the future, or something that only exists because the answer already happened.** That single sentence catches most real leaks.

---

### Activity D — Quick, Draw!: what features did *it* get? (15 min)

Go to **quickdraw.withgoogle.com** and play one full round (six drawings, 20 seconds each).

Now think like a feature engineer:

1. What did the system actually receive? Not "a drawing" — it received **the sequence of strokes**: where each line started, where it went, and in what order.
2. Deliberately draw a perfect circle for the prompt "clock" and stop. Does it guess? Now add two hands. Watch the guess change *the instant a feature appears*.
3. Draw something upside down on purpose. Most people find it fails. **Orientation was a feature it relies on**, even though nobody told you that.
4. Write three sentences: one feature you believe it uses, one it clearly ignores, and one piece of information a human would use that the system does not have at all.

✅ **Done when:** you have those three sentences and can point to the specific drawing that convinced you of each.

---

## ✍️ Practice

**[Warm-up] 1 — Name the features and the label.**
For each system below, list **at least four plausible features** and **exactly one label**, then tag the task `classification` or `regression`.
(a) A phone app that decides whether a photo contains a face.
(b) A music app predicting whether you'll skip a song in the first 10 seconds.
(c) A school kitchen predicting how many lunches to cook tomorrow.
(d) A weather app predicting whether it will rain tomorrow.
(e) A second-hand website suggesting a price for a used bicycle.
*Done looks like:* five blocks, each with 4+ features, one clearly marked label, the label's data type, and the task kind. No block may reuse another block's features word-for-word.

**[Warm-up] 2 — Three objects into three rows.**
Choose three objects from one category that are genuinely easy to confuse (three shoes, three bottles, three books). Write a feature sheet with **five features including the exact measuring instruction for each**, then measure all three.
*Done looks like:* a written feature sheet with 5 measuring instructions, a filled 3-row table with 15 values and no blanks, and one sentence naming the feature that best separates the three objects, with the numbers that prove it.

**[Build] 3 — The leak hunt, extended.**
For each task, spot the leaky feature, then do the harder part: **replace it with a non-leaky feature that captures some of the same information.**
(a) Predict whether a patient has flu. Features: `temperature_c`, `has_cough`, `has_sore_throat`, `flu_tablets_prescribed`.
(b) Predict whether a football team wins. Features: `shots_on_target`, `possession_percent`, `fouls`, `final_score_difference`.
(c) Predict whether an email is spam. Features: `word_count`, `has_link`, `sender_domain`, `was_moved_to_spam_folder`.
(d) Predict whether a customer cancels their subscription this month. Features: `months_subscribed`, `logins_per_week`, `support_tickets`, `cancellation_reason_text`.
*Done looks like:* four leaks named, four one-line explanations of *when* each becomes known, and four replacement features that a person genuinely has in hand at prediction time.

**[Build] 4 — Build and judge your own 10-row feature table.**
Pick a group of at least 10 similar objects in your home that fall into 3 categories (pens/pencils/markers, spoons/forks/knives, coins of three values, three kinds of shoe). Build a feature table with **at least 6 features** — and deliberately include **one you expect to be useless** and **one you suspect is leaky**.
Then judge every feature by counting, exactly as in Worked Example Step 5: compute the baseline first, then each feature's best one-feature score.
*Done looks like:* a 10-row table, a baseline percentage with the count that produced it, a scoreboard table with one row per feature showing score as a fraction **and** a percentage, and a verdict (useful / weak / useless / leaky) with a one-line reason for each.

**[Stretch] 5 — Flip every task.**
Take these four tasks. State which kind each is. Then rewrite each one as the *other* kind, and write one sentence on what is gained and one on what is lost.
(a) How many minutes will my homework take?
(b) Is this photo a cat or a dog?
(c) How many runs will this batter score in the match?
(d) Which of three bus routes will get me to school fastest?
*Done looks like:* four "original kind" labels, four rewritten tasks with their new label column described, and eight sentences (a gain and a loss for each). At least one of your rewrites should conclude the flip is a **bad** idea, with the reason.

**[Stretch] 6 — The feature you cannot have.**
Choose one task: (a) will this student be happy at this school next year? (b) is this second-hand phone going to break within six months? (c) will these two people become friends?
List **five features you could actually measure**. Then list **three features you desperately wish you had but cannot measure** — and for each, say precisely *why* it is unmeasurable: is it private, is it in the future, is it a feeling nobody can score, or does no instrument exist?
*Done looks like:* 5 measurable features with measuring instructions, 3 impossible features each with a named reason from those four kinds, and a closing paragraph (5+ sentences) answering: *should anyone deploy a system for this task at all, given what is missing?*

---

## 🤔 Think Deeper

**1. Who decided which features count?**
A hiring system for a company measures: years of experience, university attended, number of past jobs, and length of longest job. Every one of those is measurable. Every one is also a choice someone made.
*How to reason about it:* start by asking what a great candidate might have that is **absent from the list entirely** — and who tends to have it. Then flip it: for each feature that *is* on the list, ask "what else does this quietly measure?" University attended, for example, also measures family money and where you grew up. A feature can carry information nobody intended to include and nobody can see in the column name. Finally, ask who would notice if the list were unfair: the person building it, or the people it rejects? Module 9 comes back to this with real cases.

**2. Is there such a thing as a feature that is *too* good?**
In Worked Example Step 6, `sticker_says` scored 100% and you deleted it. But a supermarket really does put stickers on fruit. Is deleting it always right?
*How to reason about it:* separate two questions that feel like one. *Is the feature available at prediction time?* and *is the feature available at prediction time for **every** case I care about?* For a supermarket's own checkout, stickers may genuinely be there. For a phone app used in someone's kitchen, they aren't. The same column can be honest in one deployment and a fatal leak in another. Then push further: if a feature is so strong that no other feature matters, what happens the first day it goes missing — does the system degrade gracefully, or fall off a cliff?

**3. What does a machine owe you if it has never seen your category?**
The fruit model met a lime and confidently said "orange." It had no way to say "I don't know."
*How to reason about it:* imagine three possible designs — a system that must always pick a box, a system with an extra box called "other," and a system that can refuse to answer. Work out who is harmed by each in a real setting, like a medical scanner or a passport gate. Then consider the cost of the honest option: a system that says "I don't know" too often gets switched off by its users, and one that never says it gets trusted too much. Where is the line, and — the question with no clean answer — **who should get to set it, the builder or the person being classified?**

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Treating "a photo of my dog" as the example the machine sees | It's what *you* see, so it feels like the input | The machine sees only the row you built. Write the row out explicitly before you build anything, and count the values in it. That count is the machine's entire world |
| Celebrating a feature that scores 100% | A perfect score feels like success, so nobody investigates it | Run the three-second test: at the moment of prediction, do I have this? A 100% single feature is a leak until proven otherwise |
| Using an adjective as a feature (`big`, `nice`, `good quality`) | It's how humans naturally describe things | Convert every adjective into a number with a unit or into a short fixed list of values. If you cannot write the measuring instruction, it isn't a feature yet |
| Adding more features because more must be better | Effort feels like progress | Score each feature against the baseline. Useless columns add noise and hide the useful ones. Two good features beat five weak ones, as Step 7 showed |
| Measuring the same feature two different ways across rows | You measured on Monday and Thursday and forgot the convention | Write the measuring instruction on the sheet *before* the first measurement, and never change it mid-table. If you must change it, re-measure everything |
| Forgetting to mark which column is the label | The table looks obvious while you're making it | Put the label last, name it plainly, and write it into your data card. Two weeks later "score" could mean anything |
| Assuming the machine can output a category you never gave it | You know limes exist, so surely it does too | List your classes explicitly and out loud. Anything not on that list will be forced into a box that is on it, confidently |
| Judging a feature by feeling rather than counting | Counting is boring, intuition is fast | Always compute the baseline first, then each feature's score. `quadrant` "felt" plausible and scored exactly zero above baseline |
| Confusing classification with regression because the label happens to be a number | Numbers look like numbers | Ask whether "close" means anything. Jersey number 7 vs 8 isn't "nearly right" — that's a category wearing a number's clothes |

---

## 🛠️ Mini-Project — Feature Card Deck

**Time: ~3 hours (can be split across two days)**

### 🎯 Goal

Build a deck of 20 cards where each card describes one real object using **only features** — and prove the deck works by handing it to another person who has never seen the objects. If they can name your objects from features alone, you have proved something real: **a well-chosen feature row carries enough information to identify a thing.** If they can't, you have proved something equally real, and more interesting.

### 📋 Starter steps

**Step 1 — Choose your objects (20 min).**
Pick **20 objects** from around your home. The rules:
- They must fall into **4 to 6 categories** with at least 3 objects in each (e.g. 5 kitchen utensils, 4 items of stationery, 4 toys, 4 items of clothing, 3 pieces of fruit).
- At least two categories must be **genuinely confusable** with each other. A deck of 20 wildly different things is too easy and teaches you nothing.
- Write the list before you start measuring, and count your categories.

**Step 2 — Write your feature sheet FIRST (20 min).**
Choose exactly **5 features** that apply to *every* object in your deck. This constraint is deliberately hard, and it is where the learning happens. For each, write the measuring instruction:

```
FEATURE SHEET — Feature Card Deck
f1  longest_side_cm   ruler, longest straight dimension, nearest 0.5 cm
f2  weight_g          kitchen scale, nearest gram
f3  main_colour       ONE of {red, blue, green, yellow, black, white, brown, clear}
f4  material          ONE of {metal, plastic, wood, fabric, glass, paper, food}
f5  is_hollow         yes / no  (could it hold water?)
```

⚠️ Do **not** use a feature that names the object or its use. `is_used_for_eating` is a leak in disguise — it hands over most of the answer.

**Step 3 — Make the 20 cards (60 min).**
Index cards, or paper cut into rectangles. On the **front**, the id and the five feature values only. On the **back**, the label — folded over or covered with a sticky note so it can't be read from the front.

```
   ┌───────────────────────────────┐     ┌───────────────────────────────┐
   │ CARD 07                       │     │                               │
   │                               │     │                               │
   │ longest_side_cm : 19.0        │     │          teaspoon             │
   │ weight_g        : 24          │     │                               │
   │ main_colour     : white       │     │        (category:             │
   │ material        : metal       │     │       kitchen utensil)        │
   │ is_hollow       : yes         │     │                               │
   │                               │     │                               │
   │            FRONT              │     │            BACK               │
   └───────────────────────────────┘     └───────────────────────────────┘
```

**Step 4 — Copy the deck into a spreadsheet (15 min).**
20 rows, 5 feature columns, 1 label column. You'll need this to judge the features in Step 6, and it's your data card evidence.

**Step 5 — Run the test on a real human (25 min).**
Find someone — a parent, sibling, friend. Give them **the list of 20 object names in random order** and the deck, fronts up. Their job: match each card to an object name.

Score honestly:

| card | their guess | truth | correct? |
|---|---|---|---|
| 01 | | | |
| … | | | |
| 20 | | | |

Then compute: **correct ÷ 20**, as a fraction and a percentage. Also compute the **baseline**: if they guessed the most common category every time, how many would they get? Your score only means something compared to that number.

**Step 6 — Find the feature that was doing all the work (25 min).**
Ask your tester: *"Which feature did you look at first?"* Write down their answer.

Now check it with counting. For each of your five features, do what Worked Example Step 5 did: work out the best one-feature score across your 20 cards, as a fraction and a percentage. Build the scoreboard:

| feature | best one-feature score | % | verdict |
|---|---|---|---|
| longest_side_cm | /20 | | |
| weight_g | /20 | | |
| main_colour | /20 | | |
| material | /20 | | |
| is_hollow | /20 | | |
| **baseline (guess most common)** | /20 | | — |

Compare the winner to what your tester *said* they used. When those two disagree — and they often do — that gap is the whole lesson: **people are unreliable narrators of their own reasoning, and counting isn't.**

**Step 7 — Write the two paragraphs (15 min).**
1. Which feature carried the deck, with the numbers that prove it.
2. Which two objects got confused with each other most, and **exactly what feature you would add** to separate them. Be specific: name the feature, its unit, and its measuring instruction.

### ✅ Success criteria checklist

- [ ] 20 cards, each with the **same 5 features**, no blanks
- [ ] 4–6 categories, at least 3 objects each, at least two categories genuinely confusable
- [ ] A written feature sheet with a measuring instruction for all 5 features, written **before** measuring
- [ ] No feature that names the object's identity or purpose (no disguised leaks)
- [ ] The deck copied into a 20-row spreadsheet with the label in the last column
- [ ] A real person tested, with a completed 20-row scoring table
- [ ] A score as a fraction **and** a percentage, **and** the baseline computed for comparison
- [ ] A feature scoreboard with all 5 features scored by counting
- [ ] Two written paragraphs: which feature did the work, and the specific new feature you'd add

### 🚀 Level it up

**Take one feature away and re-run the test.** Cover up your best-scoring feature with a sticky note and hand the deck to a *second* person who has never seen it. Score again.

The drop tells you what that column was really worth — not what you assumed, but what it *cost* to lose. If the score barely moves, your other four features were quietly carrying it and the "star" feature was overrated. If the score collapses, you have found a single point of failure: a system that works only while one measurement keeps working.

Write three sentences on which of those two things happened, and what you'd do about it if this were a real product.

---

## 🔑 Key Takeaways

- **A machine never meets the object. It meets a row you wrote.** Every feature you leave out is information the system can never recover, no matter how clever it is.
- **A feature must be measurable the same way twice.** If you cannot write the measuring instruction, you do not yet have a feature — you have an opinion.
- **The label is a choice, not a property.** The same table becomes a different task depending on which column you decide to hide.
- **Judge features by counting, not by feeling.** Compute the baseline first; a feature that can't beat it is dead weight, however sensible it sounds.
- **A feature that scores 100% is a suspect, not a hero.** Ask whether you'd really have it at the moment of prediction. Leaks look exactly like success right up until they don't.
- **Classification asks "which box?"; regression asks "how much?"** In classification a guess is right or wrong; in regression it is off by an amount — and that changes everything about how you'll test it.
- **The model can only ever say what's on your list of classes.** Show it a lime and it will confidently say orange.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Feature** | One thing you measured about one example; one column in your table | `weight_g = 150` for the apple in row 1 |
| **Label** | The answer you want the machine to give; the column you cover up | `fruit = apple` |
| **Feature table** | A table where each row is one example, most columns are features, and one column is the label | The 12-row fruit bowl table |
| **Measuring instruction** | The exact written recipe for getting a feature's value, so anyone gets the same number | "ruler, longest straight dimension, nearest 0.5 cm" |
| **Useful feature** | A feature that makes your guess better than guessing blind | `colour` scored 91.7% against a 33.3% baseline |
| **Useless feature** | A feature that makes no difference at all | `quadrant` scored 33.3% — exactly the baseline |
| **Leaky feature** | A sneaky feature that already contains the answer, and won't be there when you really need it | `sticker_says = APPLE` |
| **Baseline** | The score you'd get by always guessing the most common label | 4 of 12 fruits = 33.3% |
| **Classification** | Predicting which box something goes in, from a short fixed list | apple / orange / banana |
| **Binary classification** | Classification with exactly two boxes | spam / not spam |
| **Multi-class classification** | Classification with three or more boxes | apple / orange / banana |
| **Regression** | Predicting a number on a sliding scale | "this orange weighs 197.5 g" |
| **Error** | In regression, how far the guess was from the truth | predicted 197.5 g, true 205 g → 7.5 g off |
| **Class** | One of the possible values of a category label | `banana` is one class of three |
| **Bucketing** | Turning a number label into categories by grouping ranges | 47 minutes → "30–60 min" |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

---

### Exercise 1 — Name the features and the label

**(a) Does this photo contain a face?**

| features (4+) | notes |
|---|---|
| `brightness_of_each_pixel` (thousands of them) | this is genuinely what a vision system gets — Module 7 unpacks it |
| `image_width_px`, `image_height_px` | size affects what's visible |
| `number_of_skin_tone_coloured_regions` | a hand-built feature a 1990s system might use |
| `has_two_dark_blobs_above_a_horizontal_line` | crude "eyes above mouth" detector |

**Label:** `contains_face` → `yes` / `no`. Type: category (two values). **Binary classification.**

**(b) Will you skip this song in the first 10 seconds?**

Features: `seconds_of_intro_before_vocals`, `times_you_played_this_artist_last_month`, `genre`, `time_of_day`, `is_this_song_already_in_your_playlist`, `tempo_bpm`.
**Label:** `skipped_in_first_10s` → `yes` / `no`. Type: category. **Binary classification.**

⚠️ Watch out for a leak: `seconds_listened` would be perfect and useless — it *is* the answer.

**(c) How many lunches to cook tomorrow?**

Features: `students_on_roll`, `day_of_week`, `menu_item`, `lunches_sold_same_weekday_last_week`, `is_there_a_school_trip_tomorrow`, `weather_forecast`.
**Label:** `lunches_sold` → e.g. `284`. Type: number (a count). **Regression.**

**(d) Will it rain tomorrow?**

Features: `today_humidity_percent`, `today_air_pressure_hpa`, `pressure_change_over_6h`, `month`, `wind_direction`, `rained_today`.
**Label:** `rain_tomorrow` → `yes` / `no`. Type: category. **Binary classification.**

(If the label were `rainfall_mm_tomorrow` it would be regression instead — same weather, different question.)

**(e) Suggested price for a used bicycle.**

Features: `age_years`, `wheel_size_inches`, `number_of_gears`, `brand`, `condition_1to5`, `has_rust` , `frame_material`.
**Label:** `price` → e.g. `4500`. Type: number. **Regression.**

⚠️ Leak to avoid: `price_it_eventually_sold_for` is the label wearing a hat.

---

### Exercise 2 — Three objects into three rows

Model answer using three drinking bottles.

```
FEATURE SHEET
label question: water bottle / flask / juice bottle?

f1 height_cm       ruler, base to top of closed lid, nearest 0.5 cm
f2 widest_width_cm ruler, widest point of the body, nearest 0.5 cm
f3 empty_weight_g  kitchen scale, empty and dry, nearest gram
f4 material        ONE of {plastic, steel, glass}
f5 lid_type        ONE of {screw, flip, push}
```

| id | height_cm | widest_width_cm | empty_weight_g | material | lid_type | **label** |
|---|---|---|---|---|---|---|
| 1 | 24.0 | 7.0 | 92 | plastic | screw | water bottle |
| 2 | 27.5 | 8.0 | 410 | steel | screw | flask |
| 3 | 19.0 | 6.5 | 265 | glass | push | juice bottle |

**Best separator:** `empty_weight_g` — 92 g, 410 g, 265 g. Three values, three big gaps (the closest pair is 265 and 410, still 145 g apart), so a single weight reading identifies the bottle every time. `material` also separates all three perfectly, but with only 3 rows that could easily be luck: add two more plastic bottles of different kinds and material stops being decisive, while weight probably keeps working.

**A note on honesty with tiny tables:** with 3 rows, *four* of these five features would separate the objects perfectly. That is not evidence of good features — it's evidence of a tiny table. Real judgement needs the 10–20 rows you'll build in Exercise 4.

---

### Exercise 3 — The leak hunt, extended

**(a) Flu prediction. Leak: `flu_tablets_prescribed`.**
*When does it become known?* Only **after** a doctor has already diagnosed flu. Nobody prescribes flu tablets before the diagnosis, so at prediction time this is always zero or blank.
*Replacement:* `days_of_symptoms_so_far` — genuinely known at the moment the patient walks in, and carries real information about severity without depending on the diagnosis.

**(b) Football result. Leak: `final_score_difference`.**
*When does it become known?* At the final whistle — i.e. it **is** the answer. A positive difference means "won" by definition.
*Replacement:* `goal_difference_in_last_5_matches` — a form measure known **before** kick-off. If the prediction is meant to be made at half time, `score_difference_at_half_time` is also legitimate; the leak is not the idea of a score, it's using a score from after the moment you're predicting.

**(c) Spam. Leak: `was_moved_to_spam_folder`.**
*When does it become known?* After a filter or a human has already judged it. It's a record of the decision you're trying to make.
*Replacement:* `sender_is_in_my_contacts` (yes/no) — available the instant the email arrives, and captures some of the same "is this person legitimate?" signal.

**(d) Subscription cancellation. Leak: `cancellation_reason_text`.**
*When does it become known?* Only for people who **already cancelled**. For everyone else the field is empty — so the model would effectively learn "if this box has any text in it, they cancelled." Perfect on old data, useless on the actual question.
*Replacement:* `days_since_last_login` or `support_tickets_in_last_30_days` — both exist for every customer at any moment, and both plausibly rise before someone quits.

**The pattern:** in all four, the leak is a **record of the outcome or of a decision made after the outcome**. A replacement is honest when you can point at a clock and say: *at this exact time, this value already exists for every example, including the ones where nothing has happened yet.*

---

### Exercise 4 — Build and judge your own 10-row feature table

Model answer: ten writing implements from a pencil case, in 3 categories.

| id | length_cm | weight_g | has_clip | tip_type | barrel_colour | writes_colour | **label** |
|---|---|---|---|---|---|---|---|
| 1 | 14.0 | 6 | yes | ball | blue | blue | pen |
| 2 | 14.5 | 7 | yes | ball | black | black | pen |
| 3 | 15.5 | 6 | yes | ball | red | red | pen |
| 4 | 17.5 | 5 | no | graphite | yellow | grey | pencil |
| 5 | 13.8 | 4 | no | graphite | green | grey | pencil |
| 6 | 16.0 | 5 | no | graphite | red | grey | pencil |
| 7 | 15.0 | 4 | no | graphite | blue | grey | pencil |
| 8 | 12.5 | 18 | yes | felt | orange | orange | marker |
| 9 | 13.0 | 20 | yes | felt | green | green | marker |
| 10 | 11.5 | 16 | yes | felt | pink | pink | marker |

**Baseline first.** Counts: pen 3, pencil 4, marker 3. Always guess `pencil` → **4 of 10 = 40%.**

**`weight_g`.** Sorted: pencils 4, 4, 5, 5 · pens 6, 6, 7 · markers 16, 18, 20. Three clean, well-separated bands.
Rule: `< 5.5 → pencil; 5.5–10 → pen; > 10 → marker`. Gets 4 + 3 + 3 = **10 of 10 = 100%.**

**`tip_type`.** ball → pen (3 of 3); graphite → pencil (4 of 4); felt → marker (3 of 3). **10 of 10 = 100%.**
This one deserves a comment. It is *not* a leak — you can see the tip while holding the pen, before knowing the answer. But a graphite tip is very nearly the **definition** of a pencil, so this feature does the whole job and makes the others irrelevant. Call it a **definition-level feature**: honest, but it tells you nothing you didn't already know about the world, and it makes the exercise pointless if you keep it.

**`has_clip`.** yes → pens (3) + markers (3) = 6 rows, best guess gets 3; no → pencils, 4 rows, gets 4. Total = **7 of 10 = 70%.** It is a *perfect* "pencil or not pencil?" detector (10 of 10 on that binary question) but cannot split pens from markers at all. Useful specialist.

**`length_cm`.** pens 14.0, 14.5, 15.5 · pencils 13.8, 15.0, 16.0, 17.5 · markers 11.5, 12.5, 13.0. Heavy overlap.
Best three-band rule: `< 13.2 → marker; 13.2–14.7 → pen; > 14.7 → pencil`.
- `< 13.2`: 11.5(m), 12.5(m), 13.0(m) → 3 of 3
- `13.2–14.7`: 13.8(pencil), 14.0(pen), 14.5(pen) → 2 of 3
- `> 14.7`: 15.0(pencil), 15.5(pen), 16.0(pencil), 17.5(pencil) → 3 of 4

Total = 3 + 2 + 3 = **8 of 10 = 80%.** Useful but overlapping — a long pen and a stubby pencil each cross the border.

**`barrel_colour`.** Values: blue(rows 1, 7), black(2), red(3, 6), yellow(4), green(5, 9), orange(8), pink(10). Best guess per value: blue 1 of 2, black 1 of 1, red 1 of 2, yellow 1 of 1, green 1 of 2, orange 1 of 1, pink 1 of 1 → **7 of 10 = 70%.**

This score is a **trap**, and spotting it is the real prize of this exercise. Barrel colour has 7 different values across only 10 rows. Four of those values appear exactly once, and any feature value that appears once is automatically "right" — it just memorised that row. There is no reason on earth a pink barrel means marker. **A feature with almost as many values as you have rows will always score well and will always be worthless on anything new.** (Module 6 gives this failure its proper name.)

**`writes_colour`.** grey → pencil (4 of 4); every other value appears once or twice and maps to one class → 10 of 10 = **100%** — and it's the same trap, worse. Also arguably close to a leak for pencils, since "writes grey" is what a pencil *does*.

**The scoreboard:**

| feature | best one-feature score | % | verdict |
|---|---|---|---|
| `weight_g` | 10/10 | 100% | ✅ genuinely useful — three separated bands, physically sensible |
| `tip_type` | 10/10 | 100% | 🟡 definition-level: honest but does the whole job by itself |
| `writes_colour` | 10/10 | 100% | ❌ memorising: 7 values / 10 rows, and near-definitional |
| `length_cm` | 8/10 | 80% | ✅ useful, overlapping |
| `has_clip` | 7/10 | 70% | ✅ useful specialist (pencil vs not-pencil) |
| `barrel_colour` | 7/10 | 70% | ❌ useless in principle — high score is memorising |
| **baseline** | 4/10 | 40% | — |

**Final keep list:** `weight_g`, `length_cm`, `has_clip`. Drop `barrel_colour` (no causal link, high-value-count trap), set aside `tip_type` and `writes_colour` as too close to the definition to be interesting.

**The lesson:** two features scored 70% and got opposite verdicts. The score alone did not decide it — you also had to ask *how many distinct values does this feature have* and *is there any reason this should work?* Counting is necessary. It is not sufficient.

---

### Exercise 5 — Flip every task

**(a) "How many minutes will my homework take?" → originally REGRESSION.**
*Flipped:* "Will this homework take under 30 min, 30–60 min, or over 60 min?" New label column: `duration_bucket` with three category values.
*Gained:* it's far easier to be right, and it matches how you'd actually use the answer — you're really deciding "can I do this before dinner or not?"
*Lost:* 31 minutes and 59 minutes become the same answer, and 29 vs 31 becomes a total miss instead of a near-perfect guess. All precision inside a bucket is thrown away.

**(b) "Is this photo a cat or a dog?" → originally CLASSIFICATION (binary).**
*Flipped:* "What fraction of 100 people would call this a cat?" New label: `percent_saying_cat`, a number from 0 to 100.
*Gained:* genuine ambiguity becomes visible. A blurry photo scoring 55 is honestly different from a clear tabby scoring 99, and the flipped version can say so.
*Lost:* you now need 100 human opinions per photo instead of one. **This is the bad-idea flip.** For almost every real use — sorting a photo album, a vet's records — you need one word, not a percentage, and the labelling cost has gone up a hundredfold for information nobody will use. Keep it as classification.

**(c) "How many runs will this batter score?" → originally REGRESSION.**
*Flipped:* "Will they score a fifty? yes/no." New label: `scored_fifty`, category.
*Gained:* a much clearer, more useful answer for a specific purpose (a milestone bet, a team-selection rule), and being off by 3 runs no longer counts as an error.
*Lost:* 49 and 0 become identical answers, which is absurd cricket. So do 50 and 200. The flip only makes sense if fifty is genuinely the thing you care about; otherwise you've destroyed the information.

**(d) "Which of three bus routes is fastest?" → originally CLASSIFICATION (three boxes: route A, B, C).**
*Flipped:* "How many minutes will each route take?" Three regression predictions, then pick the smallest.
*Gained:* a great deal. You learn *by how much* one route wins — 2 minutes or 25 minutes changes your decision if one route is more comfortable. And if a fourth route opens, you just predict it too, with no need to rebuild anything. A classifier with three fixed boxes cannot handle a new route at all.
*Lost:* three separate number predictions to get right instead of one choice, and errors can combine badly — being 5 minutes optimistic about A and 5 pessimistic about B can flip the winner even though each prediction was decent.

**Closing observation:** flipping toward regression usually gains information and costs effort; flipping toward classification usually gains simplicity and costs information. Which trade is right depends entirely on the decision the answer feeds into — never on which one sounds more advanced.

---

### Exercise 6 — The feature you cannot have

Model answer for **(a) Will this student be happy at this school next year?**

**Five features I could actually measure:**

| feature | measuring instruction |
|---|---|
| `attendance_percent_this_year` | days present ÷ school days × 100, from the register |
| `clubs_joined` | count of extracurricular clubs signed up for, from the sign-up sheet |
| `distance_to_school_km` | home postcode to school postcode, shortest road route |
| `changed_school_in_last_2_years` | yes / no, from the enrolment record |
| `self_reported_happiness_1to5` | one survey question, asked in the same week each term |

**Three features I wish I had but cannot measure:**

1. **`does_this_student_have_one_real_friend_here`** — *reason: private.* You could ask, but the honest answer is exactly the one a struggling student is least likely to give to a school form. Worse, collecting it creates a record that could be seen by the wrong person. Asking the question can itself do harm.

2. **`will_their_best_friend_move_away_next_year`** — *reason: in the future.* This may be the single biggest driver of the label, and it is unknowable at prediction time. Even the family may not know yet. Adding it later would be a textbook leak.

3. **`how_safe_they_feel_walking_into_the_building`** — *reason: a feeling nobody can score reliably.* You can put a 1-to-5 scale on the form, but a 3 from one student and a 3 from another are not the same 3, and the number will drift with mood, with who else is in the room, and with whether they think a teacher will read it.

You could add a fourth kind: **no instrument exists** — for example, `hours_of_genuinely_restful_sleep`. A watch measures movement, not rest, so the column would quietly contain something adjacent to what you wanted.

**Should anyone deploy a system for this task?**

I don't think so — at least not as a decision-maker, and here is the reasoning rather than the slogan. The features I can measure are all **proxies**: attendance is a proxy for engagement, clubs are a proxy for belonging, distance is a proxy for effort. Each is only loosely connected to happiness, and each one is *systematically* wrong for particular children. A student who is unhappy but dutiful has 99% attendance. A student who is happy but has a long commute and caring duties at home joins zero clubs. The three features that would actually carry the signal are exactly the three I cannot have — and that is not a coincidence, it's the shape of the problem: the things that matter here are private, future, or unquantifiable, all at once.

There is also an asymmetry of harm that matters. If the system labels a happy student "at risk," the cost is a slightly awkward conversation. If it labels an unhappy student "fine," a real child is overlooked because a number said not to worry — and the adults now have a document telling them everything is fine, which is worse than having no system at all. Module 9 has a name for that failure: **automation bias**.

What I'd support instead is a system used as a **prompt, never a verdict**: it surfaces students a human should go and talk to this week, it never produces a score anyone records, and the humans are explicitly told it is often wrong. Same features, same table, completely different deployment — and that difference, not the modelling, is where the ethics actually live.

---

</details>

---

[⬅ Previous](module-03-patterns-and-rules.md) · [Level 1 Home](README.md) · [Next ➡](module-05-learning-from-examples.md)

*Next up: you can now build a feature table by hand. But nobody hand-measures 300 photographs. In Module 5 you'll hand a computer a few dozen photos, let it work out its own features, and watch a guessing machine appear in front of you — then deliberately break it.*

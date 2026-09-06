# Module 6 — Train, Test, Trust: Why You Must Hide Some Examples

**Level 1 · Module 6 · ~3 hours · Prereqs: Module 4 (baseline, classes, leaks), Module 5 (training, models, confidence, margin)**

[⬅ Previous](module-05-learning-from-examples.md) · [Level 1 Home](README.md) · [Next ➡](module-07-how-computers-see.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** split a set of examples into a training set and a test set, and defend the split ratio you chose with numbers.
2. **You will be able to** compute accuracy by hand as a fraction, a decimal, and a percentage — showing the division.
3. **You will be able to** explain memorizing versus generalizing using results from your own model, not someone else's.
4. **You will be able to** describe what overfitting looks like in plain words, so that when the formal definition arrives in Level 2 it will feel obvious.
5. **You will be able to** build a confusion matrix by hand and use it to find the problem a single accuracy number was hiding.

---

## 🪝 The Hook

Go back to Module 5, Experiment 2. You trained a model on photos taken entirely on one wooden table. Held over that table, it scored **95%** — better than your good model's 91%.

Now sit with what almost happened. If you had tested it only where you trained it, you would have written "95% accurate" in your notes, told everyone it was your best model yet, and been completely, provably wrong. It failed two metres away at the sink.

This is not a beginner's mistake. In 2020 and 2021, dozens of research teams built systems to detect COVID from chest X-rays. Many reported superb accuracy. Then other researchers checked what the models were actually looking at, and found several were keying on things like the **position of the patient**, or **text markers printed on the image by a particular hospital's machine** — because the sick patients' scans came from one source and the healthy ones from another. The models had learned which hospital, not which disease. Every one of them had been tested — just not on anything new.

The fix costs nothing, takes five minutes, and almost nobody does it the first time. **Before you train, hide some of your examples. Then never let the model near them until the very end.**

---

## 🧠 The Concept

Five ideas. Each with a plain explanation, an everyday anchor, and arithmetic you can check on paper.

---

### 1️⃣ Split your examples: a training set to study from, a test set to be examined on

> **Training set** — the examples the model is allowed to study.
> **Test set** — examples you hide before training and use once, at the end, to find out how good the model really is.
> **The golden rule** — a test example is **never** trained on. Not once. Not "just to top it up."

```
                        ALL 75 PHOTOS YOU COLLECTED
   ┌───────────────────────────────────────────────────────────────┐
   │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │ ░░░░░░░░░░░░ │
   └───────────────────────────────────────────────────────────────┘
             TRAINING SET — 60 photos (80%)          TEST SET — 15 (20%)
             the model studies these                 sealed in an envelope
             over and over, 50 times                 opened once, at the end

                      ┌──────────────┐
                      │  the split   │  ← happens BEFORE training,
                      │  happens     │     not after, and not "roughly"
                      │  HERE        │
                      └──────────────┘
```

**🍕 Analogy — the maths exam.**
Your teacher gives you 60 practice questions with the answers on the back. You work through them until you can do them all. Then exam day comes and the paper has **15 questions you have never seen.**

Now imagine a different teacher who sets an exam made of the exact 60 practice questions. Everyone gets full marks. Everyone celebrates. And not one person in the room knows whether anybody learned any maths. That exam measured nothing — and it *felt* exactly like a successful exam.

Testing a model on its training photos is that second exam. It always produces a lovely number and it always tells you nothing.

**🔢 Tiny example — doing the split.**

You have 75 photos, 25 per class, and you choose a **80 / 20 split**.

```
   test photos  = 20% of 75  =  0.20 × 75  =  15
   train photos = 75 − 15    =  60
```

But don't stop there — **split each class separately**, or you might accidentally hide 12 combs and 1 spoon:

```
   per class:  20% of 25  =  0.20 × 25  =  5 test,  20 train
   × 3 classes:            15 test,  60 train   ✓
```

**Choosing the ratio.** There is no single right answer, and here is the actual trade-off:

| split | training photos (of 75) | test photos | good because | bad because |
|---|---|---|---|---|
| 90 / 10 | 67 (rounded) | 8 | the model gets almost all the data to learn from | 8 test photos is a shaky measurement — one photo is worth 12.5 percentage points |
| **80 / 20** | **60** | **15** | **a sensible middle; the usual default** | **nothing terrible; a good starting choice** |
| 70 / 30 | 52 (rounded) | 23 | a much more trustworthy accuracy number | the model has 8 fewer photos per class to learn from, so it's genuinely worse |
| 50 / 50 | 37 | 38 | a very reliable score | of a badly-trained model. You measured the wrong thing very precisely |

The rule of thumb: **80/20 unless you have a reason.** With very few examples, lean towards 70/30 so your score means something. With thousands of examples, 90/10 is fine because even 10% is hundreds of photos.

⚠️ **One more rule people break constantly.** If you test, tweak your photos, retrain, test again, tweak, retrain, test again — you are slowly leaking the test set into your decisions. Every tweak was chosen *because of* the test score. Use your test set as few times as you can, and be honest in your write-up about how many times you looked.

---

### 2️⃣ Accuracy = correct guesses ÷ total guesses

> **Accuracy** — the fraction of test examples the model got right.

```
                number of correct guesses
   accuracy =  ───────────────────────────
                 total number of guesses
```

That's it. The whole formula. The skill is not the formula — it's showing it three ways so nobody can hide behind one of them.

**🍕 Analogy — a spelling test.**
You got 11 out of 15. That's a fraction: **11/15**. Your teacher writes 0.73 in the register: that's a **decimal**. The report card says **73.3%**: that's a percentage. Same fact, three costumes. The fraction is the only one that tells you the test had 15 questions — which is why you should always show it.

**🔢 Worked arithmetic — 11 out of 15, three ways.**

```
   FRACTION:    11/15

   DECIMAL:     11 ÷ 15

                15 × 0.7 = 10.5          →  0.7,  remainder 11 − 10.5 = 0.5
                0.5 ÷ 15 = 0.0333…       →  add 0.0333
                                            0.7 + 0.0333 = 0.7333…

                = 0.7333  (to 4 places)

   PERCENTAGE:  0.7333 × 100 = 73.33…  ≈  73.3%
```

Three more you should be able to do in your head or on paper:

| fraction | decimal | percentage | the division |
|---|---|---|---|
| 6/10 | 0.6 | 60% | 6 ÷ 10 = 0.6 |
| 27/40 | 0.675 | 67.5% | 40 × 0.6 = 24, remainder 3; 3 ÷ 40 = 0.075; 0.6 + 0.075 = 0.675 |
| 18/24 | 0.75 | 75% | 18/24 simplifies to 3/4 = 0.75 |
| 7/9 | 0.7778 | 77.8% | 9 × 0.7 = 6.3, remainder 0.7; 0.7 ÷ 9 = 0.0778; total 0.7778 |

**⚠️ Accuracy means nothing without a baseline.** You met this in Module 4. With three roughly equal classes, blind guessing scores 1 in 3 = **33.3%**. So 73.3% is a real improvement of about 40 percentage points. But if your test set were 90% spoons, blind guessing would score **90%**, and a "90% accurate" model would have achieved precisely nothing. **Always write the baseline next to the accuracy.**

---

### 3️⃣ Generalizing works on new things; memorizing works only on old things

> **Generalizing** — the model works on examples it has never seen. This is the only thing you actually want.
> **Memorizing** — the model works on the exact examples it studied, and falls apart on anything else.

Here is how you tell them apart, and it takes ten seconds: **compare the score on the training photos with the score on the test photos.**

```
   ┌──────────────────────┬──────────────────────┬──────────────────────────┐
   │  training accuracy   │   test accuracy      │   what it means          │
   ├──────────────────────┼──────────────────────┼──────────────────────────┤
   │        100%          │        95%           │  generalizing well ✅    │
   │        100%          │        73%           │  starting to memorize 🟡 │
   │        100%          │        40%           │  memorizing hard ❌      │
   │         55%          │        52%           │  learned almost nothing  │
   │                      │                      │  — not enough data, or   │
   │                      │                      │  the task is too hard 🟠 │
   └──────────────────────┴──────────────────────┴──────────────────────────┘
```

**The gap is the story.** A big gap between training and test means the model latched onto things specific to those exact photos — the wooden table, your left hand, the shadow in the corner — instead of the object.

**🍕 Analogy — the two students.**
Two students both score 100% on the practice sheet.

Aisha understood how the method works. In the exam, faced with questions she's never seen, she scores 95%.

Ben learned that question 3's answer is "42" and question 7's answer is "blue." In the exam he scores 40%, and he is genuinely bewildered, because he *did* know all the answers.

Ben is not lazy. Ben worked very hard. He learned the wrong thing extremely well — and crucially, **on the practice sheet you could not tell them apart.** You needed the exam.

**🔢 Tiny example — spotting Ben.**

| | photos it saw in training | photos it never saw |
|---|---|---|
| my model | 60 / 60 = **100%** | 11 / 15 = **73.3%** |
| gap | | **26.7 percentage points** |

A 26.7-point gap says: this model is somewhere between Aisha and Ben, and closer to the middle than I'd like. It has learned something real (73.3% beats the 33.3% baseline by a mile) and it has also memorised something about my specific photos.

---

### 4️⃣ Overfitting, in plain words: the model learned the photos, not the object

> **Overfitting** — when a model fits its training examples so closely that it stops working on anything new. In plain words: **it learned the photos, not the object.**

You will meet this word for the rest of your life in this field. In Level 2 you'll meet it again with graphs and formal definitions. For now, the plain version is enough, and honestly it's most of what the formal version says anyway.

**🍕 Analogy — learning your way to school.**
Version A: you learn *"turn left at the postbox, right at the big tree, straight past the shop."*
Version B: you learn *"school is north-east of home; head that way and follow the main road."*

Both get you to school every single morning. Then one day the big tree is cut down. Version A is lost on a street they've walked 400 times. Version B doesn't even notice.

Version A memorised the route. Version B generalised. **And on every normal day, both looked identical.**

**🔢 What overfitting looks like in your own experiments.**

Go back to Module 5. You already produced a beautifully overfitted model without knowing the word for it:

| | Experiment 2 model (one background) | baseline model (5 backgrounds) |
|---|---|---|
| tested on the wooden table | **95%** ✓ | 91% ✓ |
| tested at the sink | **34%** ✗ (wrong answer) | (still works) |

The single-background model **scored higher where it was trained** and collapsed elsewhere. That is overfitting with numbers attached, produced by you, in your own kitchen.

Three things that make overfitting more likely — all of which you can control:

| cause | why it does it | the fix |
|---|---|---|
| too few examples | there's not enough variety for any general pattern to be the easiest one | collect more, in more situations |
| too little variety | the background *is* the easiest pattern | work the variety checklist for every class |
| near-duplicate examples | 200 frames of one burst is one example wearing 200 hats | short bursts, move between them |

---

### 5️⃣ One accuracy number can hide a serious problem

Accuracy is an average. Averages hide things — that's their job.

**🍕 Analogy — the class average.**
A class averages 70% on a test. Sounds fine. Then you look at the individual marks: everyone whose first language is English got 85%, everyone else got 40%. The average of 70% is completely true and completely useless. It described nobody.

There are two tools that break the average open, and you can do both with a pencil.

**Tool 1 — per-class accuracy.** Score each class separately.

> **Per-class accuracy** — of the test examples that truly belong to class X, what fraction did the model get right?

**Tool 2 — the confusion matrix.** A grid showing what got mistaken for what.

> **Confusion matrix** — a table where each row is the true class, each column is what the model predicted, and each cell counts how many examples fell there. Correct answers land on the diagonal.

```
                        ┌─────────── WHAT THE MODEL SAID ───────────┐
                        │  spoon    toothbrush     comb    │  total
   ┌────────────────────┼──────────────────────────────────┼────────
   │ TRUTH: spoon       │  ▓ 5 ▓        0            0     │   5
   │ TRUTH: toothbrush  │    0        ▓ 4 ▓          1     │   5
   │ TRUTH: comb        │    1          2          ▓ 2 ▓   │   5
   └────────────────────┴──────────────────────────────────┴────────
     total predicted       6            6            3     │  15

     ▓ shaded cells = the diagonal = correct answers = 5 + 4 + 2 = 11
```

Two ways to read it, and you should always do both:

- **Read across a row** → "of the 5 real combs, 2 were called comb, 2 were called toothbrush, 1 was called spoon." That's the model's weakness *on combs*.
- **Read down a column** → "the model said 'comb' only 3 times in 15 tries, though 5 combs existed." The model is **under-predicting comb** — it has learned to be reluctant about that class.

**🔢 Tiny example — the average that lied.**

A spam filter is tested on 100 emails: 90 real, 10 spam. It marks everything "not spam."

```
   accuracy = 90 ÷ 100 = 0.90 = 90%
```

**90% accurate**, and it has never once caught a spam email. Per-class:

```
   real emails:  90 / 90  = 100%
   spam emails:   0 / 10  =   0%
```

The headline number was honest arithmetic. It was also a lie about what the model does. **Never report one accuracy number on its own. Report the per-class numbers next to it, every time.**

---

## 🔍 Worked Example

**The Hidden Fifteen.** One complete, honest evaluation of a spoon / toothbrush / comb model, from splitting the photos to naming the worst class. Every number shown.

### Step 1 — Collect, then immediately split

75 photos collected in one session: 25 spoon, 25 toothbrush, 25 comb.

Chosen ratio: **80 / 20**, because 75 photos is a small collection and 20% still leaves 15 test photos — enough that one photo is worth 6.7 percentage points rather than 12.5.

```
   per class:  test  = 0.20 × 25 = 5
               train = 25 − 5   = 20

   totals:     test  = 5 × 3 = 15
               train = 20 × 3 = 60
               check: 15 + 60 = 75  ✓
```

**How the 5 test photos per class were chosen — this part matters more than the ratio.** They were **not** picked from the same 2-second burst as the training photos. They were taken in a **separate session, on a different day, in a different room, with different lighting.**

Why this matters is worth a full paragraph, because it's the trap almost everyone falls into. If you shoot a 2-second burst and then hide five frames from it, those five frames are near-identical twins of the ones you trained on — same angle, same shadow, same fingerprint smudge on the spoon. The model has effectively already seen them. This is exactly the **leak** you learned to hunt in Module 4, wearing a photographer's disguise: information from the answer sheet has quietly reached the exam.

### Step 2 — Seal the test photos

The 15 test photos went into a separate folder, not uploaded to Teachable Machine. Only the 60 training photos were loaded in.

Balance check on the training set: 20 / 20 / 20. Perfectly balanced. ✅

### Step 3 — Train

50 epochs, default settings, about 14 seconds.

Then read the **Under the hood** panel (click **Advanced** → **Under the hood** in Teachable Machine). It reports how the model did on the photos it trained on:

```
   accuracy on the 60 training photos:  60 / 60  =  1.00  =  100%
```

**Do not celebrate this.** A model scoring 100% on its own study material is the most ordinary thing in the world. Ben got 100% on the practice sheet too.

### Step 4 — Open the envelope and score all 15

Every hidden photo shown to the model once. Prediction and top confidence recorded before moving on.

| # | true class | predicted | top conf. | correct? |
|---|---|---|---|---|
| 1 | spoon | spoon | 94% | ✅ Y |
| 2 | spoon | spoon | 88% | ✅ Y |
| 3 | spoon | spoon | 91% | ✅ Y |
| 4 | spoon | spoon | 76% | ✅ Y |
| 5 | spoon | spoon | 82% | ✅ Y |
| 6 | toothbrush | toothbrush | 90% | ✅ Y |
| 7 | toothbrush | toothbrush | 85% | ✅ Y |
| 8 | toothbrush | toothbrush | 71% | ✅ Y |
| 9 | toothbrush | toothbrush | 68% | ✅ Y |
| 10 | toothbrush | **comb** | 54% | ❌ N |
| 11 | comb | comb | 79% | ✅ Y |
| 12 | comb | comb | 63% | ✅ Y |
| 13 | comb | **toothbrush** | 58% | ❌ N |
| 14 | comb | **toothbrush** | 66% | ❌ N |
| 15 | comb | **spoon** | 49% | ❌ N |

### Step 5 — Accuracy, three ways

Count the ✅ marks: rows 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12 → **11 correct**.

```
   FRACTION:    11 / 15

   DECIMAL:     11 ÷ 15
                15 × 0.7 = 10.5        remainder 11 − 10.5 = 0.5
                0.5 ÷ 15 = 0.03333…
                0.7 + 0.03333 = 0.73333…
                = 0.7333

   PERCENTAGE:  0.7333 × 100 = 73.33…  ≈  73.3%
```

**Baseline for comparison:** three roughly equal classes → blind guessing = 1/3 = 33.3%.

So the model beats blind guessing by 73.3 − 33.3 = **40 percentage points**. It has genuinely learned something.

### Step 6 — The gap

```
   training accuracy:  60/60 = 100.0%
   test accuracy:      11/15 =  73.3%
   ───────────────────────────────────
   gap:                        26.7 percentage points
```

A 26.7-point gap. Real learning happened *and* real memorising happened. Not a disaster; not something to ignore.

### Step 7 — Per-class accuracy: where the average was hiding a body

| class | correct | total | fraction | decimal | percentage |
|---|---|---|---|---|---|
| spoon | 5 | 5 | 5/5 | 1.000 | **100.0%** |
| toothbrush | 4 | 5 | 4/5 | 0.800 | **80.0%** |
| comb | 2 | 5 | 2/5 | 0.400 | **40.0%** |
| **overall** | **11** | **15** | **11/15** | **0.733** | **73.3%** |

There it is. "73.3% accurate" describes **no class in this model.** Spoons are essentially solved. Combs are barely above the 33.3% coin-toss.

Sanity check that the parts add to the whole: 5 + 4 + 2 = 11 ✓ and 5 + 5 + 5 = 15 ✓.

### Step 8 — Build the confusion matrix by hand

Go down the 15 rows and put a tally mark in the cell where `true class` meets `predicted class`.

| | **said spoon** | **said toothbrush** | **said comb** | row total |
|---|---|---|---|---|
| **true spoon** | **5** | 0 | 0 | 5 |
| **true toothbrush** | 0 | **4** | 1 | 5 |
| **true comb** | 1 | 2 | **2** | 5 |
| **column total** | 6 | 6 | 3 | **15** |

Checks: the diagonal is 5 + 4 + 2 = **11**, matching the correct count ✓. All cells sum to 15 ✓.

Now read it properly.

**Across the rows (what each class suffers):**
- Spoons: never confused with anything. Perfect row.
- Toothbrushes: one escaped into `comb`.
- Combs: **scattered everywhere** — 2 right, 2 called toothbrush, 1 called spoon.

**Down the columns (what the model over- and under-says):**
- It said `spoon` 6 times but only 5 spoons exist → slightly over-eager.
- It said `comb` only **3** times, though 5 combs exist → **under-predicting comb.**

**The most useful single cell** is the `true comb → said toothbrush` cell, with 2 — the largest off-diagonal number in the grid. That names the exact confusion to fix: **combs and toothbrushes look alike to this model.** Which is not surprising, is it? Both are thin plastic handles with bristly bits. The model felt that back in Module 5, when the comb had the smallest margin in the baseline test.

Note what a bare "73.3%" would have told you about all of this: nothing.

### Step 9 — The confidence check

Split the confidences by whether the answer was right.

```
   correct answers  (11): 94, 88, 91, 76, 82, 90, 85, 71, 68, 79, 63
       sum = 94+88+91+76+82+90+85+71+68+79+63 = 887
       mean = 887 ÷ 11 = 80.6%

   wrong answers    (4):  54, 58, 66, 49
       sum = 54 + 58 + 66 + 49 = 227
       mean = 227 ÷ 4 = 56.75  ≈  56.8%
```

Wrong answers averaged **24 percentage points lower** in confidence. So confidence carries real information — that's genuinely useful.

But look closer at the overlap:

```
   lowest confidence on a CORRECT answer:  63%  (row 12)
   highest confidence on a WRONG answer:   66%  (row 14)
```

**They overlap.** There is no threshold that cleanly separates right from wrong. What if you tried a cut-off at 70% anyway?

| zone | photos | correct | accuracy |
|---|---|---|---|
| confidence ≥ 70% → trust it | 9 | 9 | **9/9 = 100%** |
| confidence < 70% → send to a human | 6 | 2 | 2/6 = 33.3% |
| | 15 | 11 | 73.3% |

That's a strong result: everything the model is confident about is right, and everything it's unsure about is a coin toss. A real product built on this model should auto-accept above 70% and ask a human below it.

⚠️ Two honest warnings. First, this cut-off was chosen **after looking at these 15 results**, which means 70% is fitted to this exact test set — on fresh photos it will not be quite so clean. Second, 15 photos is a small sample; nine-for-nine is encouraging, not proof.

### Step 10 — The lazy split, for comparison

To show what the shortcut costs, the model was re-evaluated with test photos taken from **the same bursts** as the training photos — same day, same room, same table, frames a fraction of a second apart.

| | honest split (different day, different room) | lazy split (same burst) |
|---|---|---|
| accuracy | 11/15 = **73.3%** | 15/15 = **100.0%** |
| worst class | comb, 40% | none — everything perfect |
| what it tells you | roughly how it'll behave in your house | roughly nothing |

**100% versus 73.3%, from the same model on the same day.** The only difference was where the test photos came from. If you split lazily, you will not get a slightly optimistic number — you will get a **meaningless** one, and it will be the flattering kind of meaningless that nobody questions.

### Step 11 — The one-sentence verdict

> *"On 15 held-out photos taken on a different day in a different room, the model scored 11/15 = 73.3% against a 33.3% baseline; it was worst at **comb** (2/5 = 40%), and its most common mistake was calling a comb a toothbrush."*

That sentence contains the number, the sample size, the baseline, the worst class, and the specific failure. **That is what an honest result looks like.** Compare it with "my model is 73% accurate," which is technically true and tells the reader almost nothing.

---

## 💻 Hands-On

No programming. Index cards, a scoring sheet, a spreadsheet, about 65 minutes.

### Activity A — The split, unplugged (10 min)

Do this before touching a computer.

1. Take **20 index cards**. Write a number 1–20 on each.
2. Shuffle them properly — face down, spread out, swirl them around, gather them up.
3. Deal off **4 cards** without looking at the numbers. That's your **test set**. Put an actual envelope or a book on top of them.
4. The remaining 16 are your **training set**.
5. Check the arithmetic: 4 ÷ 20 = 0.2 = **20%**. ✓ You just did an 80/20 split.
6. Now do it again badly, on purpose: deal the **first 4 cards without shuffling**. Write down which numbers you got.

If your cards were in order, the lazy split just handed you cards 1, 2, 3, 4 — and if those happened to be all one class, your test set now contains zero examples of the other two. **Shuffling isn't a ritual; it's what stops your test set from being a biased slice.**

7. Finally, split **within class**: sort your 20 cards into 4 red, 4 blue, 12 green (or any 3 groups), then take 20% of *each* group. 20% of 4 is 0.8 → round to 1. 20% of 12 is 2.4 → round to 2. Test set = 1 + 1 + 2 = 4. Same total, much better spread.

✅ **Done when:** you can state your split ratio as a fraction, a decimal, and a percentage, and explain in one sentence why per-class splitting beats a single big shuffle.

---

### Activity B — Collect photos in two sessions (20 min)

The split has to happen in the *world*, not just in a folder.

**Session 1 (training) — today, in one room.**
Collect ~20 photos per class following the variety checklist from Module 5. These will all be training photos.

**Session 2 (test) — later, in a different room, ideally a different day.**
Collect ~5 photos per class. Change as much as you honestly can:

```
   ┌────────────────────────────────────────────────┐
   │  TEST SESSION — change these on purpose        │
   ├────────────────────────────────────────────────┤
   │  □ different room                              │
   │  □ different light (day → evening, or a lamp)  │
   │  □ different surface underneath                │
   │  □ different hand, or no hand                  │
   │  □ different distance from the camera          │
   │  □ different day if you can manage it          │
   └────────────────────────────────────────────────┘
```

**Do not upload the Session 2 photos to Teachable Machine.** Keep them in a separate folder on your device, or just leave the objects where they are and test live. The whole exercise dies the moment those photos touch the training panel.

⚠️ The most common way people ruin this: they collect everything at once, then "hold out" a few at the end. If your test photos came from the same burst as your training photos, go back and take new ones. It genuinely takes five minutes and it's the difference between a real result and a fake one.

---

### Activity C — The paper scoring sheet (15 min)

Print or copy this out by hand. Fill it in with a pen, one row at a time, **writing the prediction down before you look at the next photo.**

```
   ╔══════════════════════════════════════════════════════════════════╗
   ║  TEST SCORING SHEET                                              ║
   ║  model: ____________________   date: ____________                ║
   ║  training photos: ______   test photos: ______   ratio: ___/___  ║
   ║  test photos taken: □ same session  □ different room/day         ║
   ╠════╦══════════════╦══════════════╦════════════╦══════════════════╣
   ║ #  ║ TRUE class   ║ PREDICTED    ║ top conf.  ║ correct? (Y/N)   ║
   ╠════╬══════════════╬══════════════╬════════════╬══════════════════╣
   ║ 1  ║              ║              ║        %   ║                  ║
   ║ 2  ║              ║              ║        %   ║                  ║
   ║ 3  ║              ║              ║        %   ║                  ║
   ║ 4  ║              ║              ║        %   ║                  ║
   ║ 5  ║              ║              ║        %   ║                  ║
   ║ 6  ║              ║              ║        %   ║                  ║
   ║ 7  ║              ║              ║        %   ║                  ║
   ║ 8  ║              ║              ║        %   ║                  ║
   ║ 9  ║              ║              ║        %   ║                  ║
   ║ 10 ║              ║              ║        %   ║                  ║
   ║ 11 ║              ║              ║        %   ║                  ║
   ║ 12 ║              ║              ║        %   ║                  ║
   ║ 13 ║              ║              ║        %   ║                  ║
   ║ 14 ║              ║              ║        %   ║                  ║
   ║ 15 ║              ║              ║        %   ║                  ║
   ╠════╩══════════════╩══════════════╩════════════╩══════════════════╣
   ║  correct: ____ / ____                                            ║
   ║  fraction ____/____  =  decimal ______  =  percentage ______%    ║
   ║  baseline (blind guessing): ______%                              ║
   ║  worst class: ____________  at ____/____ = ______%               ║
   ╚══════════════════════════════════════════════════════════════════╝
```

**Write the true class in before you test.** If you fill in "true" after seeing the prediction, your brain will help you, and it will help you dishonestly. This is not a slur on your character — it happens to everyone, and it is why real scientists write the answer key first.

---

### Activity D — The same scoring sheet in a spreadsheet (20 min)

Open Google Sheets, Excel, or LibreOffice Calc. Use this exact layout so the formulas work.

| | A | B | C | D | E |
|---|---|---|---|---|---|
| **1** | photo_id | true_class | predicted_class | top_conf | correct |
| **2** | 1 | spoon | spoon | 94 | |
| **3** | 2 | spoon | spoon | 88 | |
| **4** | 3 | spoon | spoon | 91 | |
| **5** | 4 | spoon | spoon | 76 | |
| **6** | 5 | spoon | spoon | 82 | |
| **7** | 6 | toothbrush | toothbrush | 90 | |
| **8** | 7 | toothbrush | toothbrush | 85 | |
| **9** | 8 | toothbrush | toothbrush | 71 | |
| **10** | 9 | toothbrush | toothbrush | 68 | |
| **11** | 10 | toothbrush | comb | 54 | |
| **12** | 11 | comb | comb | 79 | |
| **13** | 12 | comb | comb | 63 | |
| **14** | 13 | comb | toothbrush | 58 | |
| **15** | 14 | comb | toothbrush | 66 | |
| **16** | 15 | comb | spoon | 49 | |

Data rows are **2 to 16**.

**D1 — mark each row correct or not.** In `E2`, then drag down to `E16`:

```
=IF(EXACT($B2, $C2), "Y", "N")
```

Expected: `Y` in rows 2–10 and 12–13, `N` in rows 11, 14, 15, 16. That's 11 `Y`s.

**D2 — overall accuracy, three ways.** In `G2`, `G3`, `G4`:

```
=COUNTIF($E$2:$E$16, "Y") & "/" & COUNTA($E$2:$E$16)
=COUNTIF($E$2:$E$16, "Y") / COUNTA($E$2:$E$16)
=TEXT( COUNTIF($E$2:$E$16,"Y") / COUNTA($E$2:$E$16), "0.0%" )
```

Expected: `11/15`, `0.733333333`, `73.3%`. All three from one sheet. 🎉

**D3 — per-class accuracy.** Put the class names in `G7`, `G8`, `G9` (`spoon`, `toothbrush`, `comb`). In `H7`, then drag down to `H9`:

```
=COUNTIFS($B$2:$B$16, $G7, $E$2:$E$16, "Y") / COUNTIF($B$2:$B$16, $G7)
```

Expected: `1` (100%), `0.8` (80%), `0.4` (40%). Format the cells as a percentage to read them easily.

**D4 — the confusion matrix.** Put the class names down `G12:G14` and across `H11:J11`:

| | G | H | I | J |
|---|---|---|---|---|
| **11** | | spoon | toothbrush | comb |
| **12** | spoon | | | |
| **13** | toothbrush | | | |
| **14** | comb | | | |

In `H12`, then drag right to `J12` and down to row 14:

```
=COUNTIFS($B$2:$B$16, $G12, $C$2:$C$16, H$11)
```

Expected grid:

| | spoon | toothbrush | comb |
|---|---|---|---|
| **spoon** | 5 | 0 | 0 |
| **toothbrush** | 0 | 4 | 1 |
| **comb** | 1 | 2 | 2 |

Check the diagonal: `=H12 + I13 + J14` → **11**. Matches your correct count ✓.

Notice the `$` signs: `$G12` locks the column so dragging right keeps reading the true-class names, and `H$11` locks the row so dragging down keeps reading the predicted-class headers. That one trick builds the entire matrix from a single formula.

**D5 — average confidence, right versus wrong.** In `G17` and `G18`:

```
=AVERAGEIF($E$2:$E$16, "Y", $D$2:$D$16)
=AVERAGEIF($E$2:$E$16, "N", $D$2:$D$16)
```

Expected: `80.63636364` and `56.75`. These match the hand arithmetic in Worked Example Step 9 exactly.

**D6 — the highest-confidence mistake**, which is always worth looking at:

```
=MAXIFS($D$2:$D$16, $E$2:$E$16, "N")
```

Expected: `66`. Go and look at that photo. The mistakes the model was *sure* about tell you far more than the ones it fumbled.

---

## ✍️ Practice

**[Warm-up] 1 — Do the splits.**
For each collection, compute an **80/20 split per class** and the totals. Show the multiplication. Where the answer isn't a whole number, say how you rounded and why.
(a) 3 classes, 30 photos each.
(b) 3 classes, 25 photos each.
(c) 4 classes with 50, 50, 50 and 18 photos.
(d) 2 classes with 200 and 200 photos — and then say whether you'd use 80/20 here or something else, with a reason.
*Done looks like:* four answers with train and test counts per class and in total, each verified to add back to the original, plus the rounding note and the reasoned choice for (d).

**[Warm-up] 2 — Accuracy three ways.**
Convert each result to a fraction, a decimal (4 places), and a percentage (1 decimal place). **Show the division** for each.
(a) 9 correct out of 12
(b) 17 correct out of 20
(c) 23 correct out of 30
(d) 4 correct out of 7
(e) 45 correct out of 60
Then: for a 3-class task with equal classes, which of these beat the baseline, and by how many percentage points?
*Done looks like:* five rows with all three forms and the working shown, plus a stated baseline and five "beats it by ___ points" figures.

**[Build] 3 — Score somebody else's test.**
Here is a completed scoring sheet for a cat / dog / rabbit classifier, 4 test photos per class.

| # | true | predicted | top conf. |
|---|---|---|---|
| 1 | cat | cat | 88% |
| 2 | cat | cat | 79% |
| 3 | cat | dog | 61% |
| 4 | cat | cat | 92% |
| 5 | dog | dog | 84% |
| 6 | dog | dog | 90% |
| 7 | dog | dog | 73% |
| 8 | dog | cat | 55% |
| 9 | rabbit | cat | 64% |
| 10 | rabbit | rabbit | 70% |
| 11 | rabbit | cat | 58% |
| 12 | rabbit | dog | 51% |

(a) Overall accuracy as a fraction, decimal, and percentage.
(b) Per-class accuracy for all three classes.
(c) The full 3×3 confusion matrix with row totals, column totals, and a diagonal check.
(d) Reading **down the columns**, what has the model learned to be reluctant about? Give the numbers.
(e) One sentence naming the single most useful fix you'd make, and why the matrix points to it.
*Done looks like:* all five parts, with the diagonal check shown and the matrix totalling 12.

**[Build] 4 — Evaluate your own model honestly.**
Take your Module 5 classifier. Re-collect photos in **two separate sessions** (Activity B), hold out 20%, train, and score every hidden photo on the paper sheet from Activity C.
*Done looks like:* a filled scoring sheet, accuracy in all three forms, the baseline stated, per-class accuracy for every class, a hand-drawn confusion matrix with a diagonal check, the training-vs-test gap in percentage points, and the one-sentence verdict in the style of Worked Example Step 11.

**[Stretch] 5 — Four cheating splits.**
Each of these splits is cheating. For each: name exactly what is leaking, predict whether the reported accuracy will be **too high** or **too low**, and describe a fix in one sentence.
(a) You take a 10-second video of each object, extract 100 frames, and randomly pick 20 frames as the test set.
(b) You have 60 photos. You train, test, get 65%, add more photos of the class that failed, retrain, test, get 78%, and report 78%.
(c) Your test set is 15 photos, all taken in the same session as training but with your friend holding the objects instead of you.
(d) You train a model to predict which pupils will need extra maths help, and your test set is the pupils from the same class, while the model will actually be used on next year's Year 7 intake.
*Done looks like:* four blocks, each naming the specific leak, a direction (too high / too low) with a reason, and a concrete fix.

**[Stretch] 6 — The number that lies.**
Two models are tested on the same 200 emails: 100 real, 100 spam. Both report **90% overall accuracy**.

| | Model A | Model B |
|---|---|---|
| real emails correct | 82 / 100 | 98 / 100 |
| spam emails correct | 98 / 100 | 82 / 100 |
| overall | 180 / 200 = 90% | 180 / 200 = 90% |

(a) Build the confusion matrix for each (classes: `real`, `spam`).
(b) Which would you install on **your own personal inbox**? Give the reason in terms of what each mistake actually costs you.
(c) Which would you install for a **hospital's email system**, where a successful phishing attack can shut down patient records? Give the reason.
(d) Now the harder part: the test set was 100 real and 100 spam, but a real inbox gets roughly 90 real emails for every 10 spam. Recompute each model's expected performance on 100 realistic emails (90 real, 10 spam) and show whether your answer to (b) changes.
*Done looks like:* two confusion matrices, two reasoned choices, the recomputed numbers for (d) with the arithmetic shown, and an explicit statement of whether your choice held up.

---

## 🤔 Think Deeper

**1. If your test set is only 15 photos, how much should you believe the number?**
You measured 73.3%. If one more comb had gone the right way it would be 12/15 = 80%. One photo moved the headline by 6.7 points.
*How to reason about it:* work out how much a single photo is worth in each situation — 1/15 is 6.7 points, 1/100 is 1 point, 1/1000 is 0.1 points. Then think about what that means for comparing two models: if model A scores 73.3% and model B scores 80% on 15 photos, is B better, or did one photo happen to fall differently? Now consider the practical squeeze: making the test set bigger takes photos *away* from training, so a more reliable measurement gives you a worse model to measure. There is no way out of that trade with a fixed number of photos — only ways to be honest about it. What sentence would you add to your write-up so a reader knows how much to trust your number?

**2. Whose photos should be in the test set?**
Your test photos are yours: your hands, your kitchen, your lighting, your objects. Your model will be used by other people in other kitchens.
*How to reason about it:* ask what a test set is really *for*. It's meant to be a small sample of the world the model will actually meet. So compare two candidate test sets — 15 of your own photos taken on a different day, versus 15 photos taken by a friend in their house. Which one better predicts how the model behaves when a stranger uses it? Then push it further: if the model will be used by hundreds of people, whose houses would you need photos from before you could honestly say "it works"? And who tends to get left out of that collection when it's assembled by whoever is nearest and most willing? Module 9 turns this exact question into a measurable audit.

**3. What if there is no honest test set available?**
Sometimes you genuinely cannot hold anything out. A doctor has 12 recorded cases of a rare condition — hiding 20% means hiding 2, and a test of 2 measures nothing. A system predicting next year's flooding has zero examples of next year.
*How to reason about it:* separate two situations that feel the same. In the rare-disease case the examples exist but are too few, so you could look for ways to reuse them cleverly, or accept a very wide range of uncertainty, or refuse to deploy. In the next-year case the examples do not exist at all, and no amount of cleverness creates them. Then ask the question that actually decides it: **what should you do when you cannot know how good your system is — not build it, build it and label it honestly, or build it and let people assume?** Notice that the third option is what happens by default when nobody chooses.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Testing on the training photos | They're right there, and the score is glorious | It measures memorising, not learning. Split before you train, and never open the envelope early |
| Taking test photos from the same burst as training photos | It's one session and it feels like a fair random split | Near-identical frames are the same example twice. Shoot test photos in a different room, different light, different day |
| Reporting one accuracy number | It's what everyone asks for | Report per-class accuracy alongside it, every time. 73.3% overall was hiding a 40% class |
| Reporting accuracy without a baseline | The number sounds good on its own | 90% is superb against a 33% baseline and worthless against a 90% one. Write both |
| Splitting the whole pile instead of each class | One shuffle feels simpler | You can end up with 12 combs and 1 spoon in the test set. Split within each class, then combine |
| Tweak, test, tweak, test, tweak, test — then report the last score | Each individual retest seems harmless | Every tweak was chosen using the test set, so it's no longer hidden. Use it as rarely as you can, and say how many times you did |
| Being pleased that training accuracy is 100% | It looks like success | It is completely ordinary and means nothing. Only the gap between training and test accuracy carries information |
| Filling in the "true class" column after seeing the prediction | It's faster and you'd never cheat on purpose | Write the true class before testing. Everyone's brain helps them; that's exactly why the answer key gets written first |
| Assuming a bigger test set is always better | More data is usually better | Every test photo is a training photo you gave up. 80/20 balances the two; going to 50/50 measures a worse model very precisely |
| Treating accuracy on your own photos as accuracy in the world | You tested honestly, so surely it's honest | Your test set is one house, one pair of hands, one camera. It predicts your house well and other houses poorly |

---

## 🛠️ Mini-Project — The Hidden Ten

**Time: ~3 hours**

### 🎯 Goal

Rebuild your Module 5 classifier the honest way: hide 20% of your photos *before* training, score every hidden one on paper, and produce a result you would be willing to defend to someone trying to catch you out.

### 📋 Starter steps

**Step 1 — Plan the split before you take a single photo (10 min).**

Decide your target counts and write the arithmetic down first:

```
   classes: 3
   photos per class: 50            total = 150
   split ratio chosen: 80 / 20     reason: ______________________

   test per class  = 0.20 × 50 = 10
   train per class = 50 − 10   = 40

   TOTAL test  = 10 × 3 = 30
   TOTAL train = 40 × 3 = 120
   check: 30 + 120 = 150  ✓
```

(50 per class is the target; 30 per class also works. Redo the arithmetic for whatever number you choose — that's part of the exercise.)

**Step 2 — Session 1: collect the 40 training photos per class (40 min).**
Work the Module 5 variety checklist for **every** class. Short bursts, move between them.

**Step 3 — Session 2: collect the 10 test photos per class (25 min).**
Different room. Different light. Different surface. Different day if you can. Use the checklist in Hands-On Activity B and physically tick the boxes.

Put these in a folder called `DO_NOT_TRAIN`. Name it that. It works.

**Step 4 — Train on the 120 only (15 min).**
Load only Session 1 into Teachable Machine. Check the class counts show 40 / 40 / 40 before you press Train.

After training, open **Advanced → Under the hood** and record the training accuracy:

```
   training accuracy = ____ / 120 = ______%
```

**Step 5 — Score all 30 hidden photos on paper (35 min).**
Use the scoring sheet from Hands-On Activity C, extended to 30 rows. For each photo:

1. Write the **true class** first.
2. Show it to the model (upload it, or hold the real object in a position matching the photo).
3. Write the predicted class and the top confidence.
4. Mark Y or N.
5. Move on. **Do not go back and change earlier rows.**

**Step 6 — Compute accuracy three ways, by hand (15 min).**
Not with a calculator for the first one — do the division on paper and show your working, exactly as in Worked Example Step 5.

```
   fraction: ____ / 30
   decimal:  ____ ÷ 30 = __________      (show the division)
   percentage: ________ %

   baseline (3 equal classes): 33.3%
   beats baseline by: ______ percentage points
```

**Step 7 — Per-class accuracy and the confusion matrix (20 min).**

| class | correct | total | fraction | percentage |
|---|---|---|---|---|
| | | 10 | | |
| | | 10 | | |
| | | 10 | | |
| **overall** | | **30** | | |

Then draw the 3×3 matrix by hand and check that the diagonal equals your correct count.

**Step 8 — The gap (5 min).**

```
   training accuracy: ______%
   test accuracy:     ______%
   gap:               ______ percentage points
```

Write two sentences on what that gap tells you about memorizing versus generalizing **in your model specifically**, referring to your own numbers.

**Step 9 — The verdict sentence (10 min).**
Write the one-sentence verdict in the Step 11 format: number, sample size, baseline, worst class, most common mistake.

**Step 10 — The fix (5 min).**
Look at the largest off-diagonal cell in your matrix. Write down the exact 10 photos you would take tomorrow to attack that specific confusion.

### ✅ Success criteria checklist

- [ ] Split arithmetic written down **before** collecting, with the check that the parts add back to the total
- [ ] Test photos collected in a genuinely separate session (different room and light at minimum), with the checklist ticked
- [ ] Test photos never loaded into Teachable Machine's training panel
- [ ] Class counts verified balanced before pressing Train
- [ ] Training accuracy recorded from Under the hood
- [ ] A completed 30-row paper scoring sheet with true class written first
- [ ] Accuracy shown as a fraction, a decimal, and a percentage, with the division worked on paper
- [ ] Baseline stated and the improvement in percentage points calculated
- [ ] Per-class accuracy for every class
- [ ] A hand-drawn confusion matrix with row totals, column totals, and a diagonal check
- [ ] The training-vs-test gap in percentage points, with two sentences interpreting it
- [ ] One sentence naming the class the model was worst at
- [ ] A specific 10-photo shot list to fix the biggest confusion

### 🚀 Level it up

**Prove the lazy split lies — with your own model.**

You already have an honest number. Now produce the dishonest one and put them side by side.

1. Take **10 more photos per class from the exact same session as your training photos** — same room, same table, same light, ideally frames from the same bursts.
2. Do **not** retrain. Use the identical model.
3. Score those 30 photos on a second scoring sheet.
4. Fill in this table:

| | honest test set (Session 2) | lazy test set (same session) |
|---|---|---|
| accuracy | / 30 = % | / 30 = % |
| worst class | | |
| biggest off-diagonal cell | | |

Then write a short paragraph answering three things: **how many percentage points did the lazy split inflate your score by; which specific weakness did it completely hide; and — the real question — if you were rushing to finish a project at 11pm, which number would you have been tempted to report?**

That last one isn't a trick. Being honest when nobody is checking is a skill, and it's easier once you've seen exactly how big the temptation is.

---

## 🔑 Key Takeaways

- **Split before you train.** Hide 20% of your examples, seal them, and don't touch them until the end. It costs five minutes and it's the difference between a real result and a story.
- **A test example is never trained on** — and photos from the same burst count as trained on, even if the file is in a different folder.
- **Accuracy = correct ÷ total**, and you should be able to write it as a fraction, a decimal, and a percentage without a calculator. Always show the fraction so the reader knows the sample size.
- **Accuracy without a baseline is meaningless.** 90% is either brilliant or worthless depending entirely on what blind guessing would score.
- **100% on training photos is ordinary; the gap to test accuracy is the information.** A big gap means the model memorised the photos instead of learning the object.
- **Overfitting, in plain words: it learned the photos, not the object.** You built one in Module 5 without meaning to, and it scored higher than the good model where it was trained.
- **One number hides bodies.** Always report per-class accuracy, and draw the confusion matrix — the largest off-diagonal cell tells you exactly which photos to go and take tomorrow.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Training set** | The examples the model is allowed to study | 60 of the 75 photos |
| **Test set** | Examples hidden before training, used once at the end | 15 photos taken on a different day |
| **Hold out** | To deliberately set examples aside before training | "I held out 5 photos per class" |
| **Split ratio** | How you divided the examples, as train / test | 80 / 20 |
| **Accuracy** | Correct guesses divided by total guesses | 11/15 = 0.733 = 73.3% |
| **Baseline** | The score you'd get by always guessing the most common class | 33.3% for three equal classes |
| **Generalizing** | Working on examples the model has never seen | 73.3% on the hidden photos |
| **Memorizing** | Working only on the exact examples studied | 100% on training, 40% on new |
| **Overfitting** | Fitting the training examples so closely it stops working on new ones — it learned the photos, not the object | The one-background model: 95% on its table, 34% at the sink |
| **The gap** | Training accuracy minus test accuracy; how much memorising happened | 100% − 73.3% = 26.7 points |
| **Per-class accuracy** | Accuracy worked out separately for each class | comb: 2/5 = 40% |
| **Confusion matrix** | A grid of true class (rows) against predicted class (columns) | 5/0/0 · 0/4/1 · 1/2/2 |
| **Diagonal** | The cells where true equals predicted — the correct answers | 5 + 4 + 2 = 11 |
| **Off-diagonal cell** | A mistake, showing exactly what got confused with what | 2 combs called toothbrush |
| **Percentage point** | The unit for the difference between two percentages | 73.3% − 33.3% = 40 percentage points |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

---

### Exercise 1 — Do the splits

**(a) 3 classes, 30 photos each (90 total).**
```
   per class:  test  = 0.20 × 30 = 6
               train = 30 − 6    = 24
   totals:     test  = 6 × 3  = 18
               train = 24 × 3 = 72
   check:      18 + 72 = 90  ✓
```
No rounding needed.

**(b) 3 classes, 25 photos each (75 total).**
```
   per class:  test  = 0.20 × 25 = 5
               train = 25 − 5    = 20
   totals:     test = 15,  train = 60
   check:      15 + 60 = 75  ✓
```

**(c) 4 classes with 50, 50, 50 and 18 (168 total).**
```
   class 1:  0.20 × 50 = 10 test,  40 train
   class 2:  0.20 × 50 = 10 test,  40 train
   class 3:  0.20 × 50 = 10 test,  40 train
   class 4:  0.20 × 18 = 3.6  →  round UP to 4 test,  14 train

   totals:   test = 10+10+10+4 = 34,   train = 40+40+40+14 = 134
   check:    34 + 134 = 168  ✓
```
**Rounding note:** I rounded 3.6 **up** to 4 rather than down to 3. Rounding down would leave the small class with only 3 test photos, where a single photo is worth 33 percentage points of that class's score — too coarse to mean anything. The extra training photo I give up matters less than being able to measure the class at all.

**Worth flagging:** class 4 has 18 photos against the others' 50. That is a **class imbalance** problem (Module 5), and it will hurt this model regardless of how the split is done. The split arithmetic is correct; the collection needs fixing.

**(d) 2 classes, 200 each (400 total).**
```
   80/20:  per class  test = 0.20 × 200 = 40,  train = 160
           totals     test = 80,  train = 320
   check:  80 + 320 = 400  ✓
```
**Would I use 80/20 here?** I'd consider 90/10 instead: test = 20 per class = 40 total, train = 180 per class = 360.

With 400 photos there is plenty to go around, and 40 test photos still gives decent resolution — one photo is worth 1/40 = 2.5 percentage points, which is fine. The 40 extra training photos per class are worth more than the extra measurement precision.

But there's a counter-argument I'd accept: if I intend to **compare several models** against each other, small differences matter, and 80 test photos separates a 90% model from an 87% model far more reliably than 40 does. So: **90/10 if I'm building one model, 80/20 if I'm choosing between several.** The right ratio depends on the question, not on a rule.

---

### Exercise 2 — Accuracy three ways

**(a) 9 out of 12**
```
   fraction:   9/12   (simplifies to 3/4)
   decimal:    9 ÷ 12 = 0.75          (12 × 0.75 = 9 exactly)
   percentage: 0.75 × 100 = 75.0%
```

**(b) 17 out of 20**
```
   fraction:   17/20
   decimal:    17 ÷ 20;  20 × 0.8 = 16, remainder 1;  1 ÷ 20 = 0.05
               0.8 + 0.05 = 0.8500
   percentage: 85.0%
```

**(c) 23 out of 30**
```
   fraction:   23/30
   decimal:    30 × 0.7 = 21, remainder 2;  2 ÷ 30 = 0.0667
               0.7 + 0.0667 = 0.7667
   percentage: 76.7%
```

**(d) 4 out of 7**
```
   fraction:   4/7
   decimal:    7 × 0.5 = 3.5, remainder 0.5;  0.5 ÷ 7 = 0.0714
               0.5 + 0.0714 = 0.5714
   percentage: 57.1%
```

**(e) 45 out of 60**
```
   fraction:   45/60   (simplifies to 3/4)
   decimal:    0.7500
   percentage: 75.0%
```

**Against a 3-class baseline of 33.3%:**

| result | percentage | beats baseline by |
|---|---|---|
| (a) 9/12 | 75.0% | 41.7 percentage points |
| (b) 17/20 | 85.0% | 51.7 percentage points |
| (c) 23/30 | 76.7% | 43.4 percentage points |
| (d) 4/7 | 57.1% | 23.8 percentage points |
| (e) 45/60 | 75.0% | 41.7 percentage points |

All five beat the baseline. But **(a) and (e) are the same percentage from very different evidence** — 12 photos versus 60. On 12 photos, one photo is worth 8.3 points; on 60, it's worth 1.7. The 45/60 result is the same number and a far more trustworthy one, which is exactly why you write the fraction and not just the percentage.

---

### Exercise 3 — Score somebody else's test

**(a) Overall accuracy.**
Correct rows: 1, 2, 4, 5, 6, 7, 10 → **7 correct**.
```
   fraction:   7/12
   decimal:    12 × 0.5 = 6, remainder 1;  1 ÷ 12 = 0.08333
               0.5 + 0.08333 = 0.5833
   percentage: 58.3%
```
Against a 33.3% baseline for 3 equal classes, that beats blind guessing by **25 percentage points** — real learning, but not much of it.

**(b) Per-class accuracy.**

| class | correct rows | fraction | decimal | percentage |
|---|---|---|---|---|
| cat | 1, 2, 4 | 3/4 | 0.75 | **75.0%** |
| dog | 5, 6, 7 | 3/4 | 0.75 | **75.0%** |
| rabbit | 10 | 1/4 | 0.25 | **25.0%** |
| **overall** | | **7/12** | 0.583 | **58.3%** |

Check: 3 + 3 + 1 = 7 ✓ and 4 + 4 + 4 = 12 ✓.

Note that rabbit at **25%** is *below* the 33.3% baseline. On rabbits, this model is worse than a coin spinner.

**(c) Confusion matrix.**

| | **said cat** | **said dog** | **said rabbit** | row total |
|---|---|---|---|---|
| **true cat** | **3** | 1 | 0 | 4 |
| **true dog** | 1 | **3** | 0 | 4 |
| **true rabbit** | 2 | 1 | **1** | 4 |
| **column total** | 6 | 5 | 1 | **12** |

Diagonal check: 3 + 3 + 1 = **7** ✓ matches the correct count.
Grand total check: 6 + 5 + 1 = 12 ✓.

**(d) Reading down the columns.**

The `said rabbit` column totals **1**. In twelve attempts, the model uttered the word "rabbit" exactly once — even though four real rabbits were shown to it. Meanwhile it said `cat` **6** times when only 4 cats existed.

The model is **deeply reluctant to predict rabbit** and **over-eager to predict cat**. That is a different diagnosis from "it's bad at rabbits." A model bad at rabbits might scatter its rabbit guesses around randomly; this one has almost stopped believing the class exists, which is the signature of **class imbalance in training** (Module 5, Step 11) or of rabbit photos that were far less varied than the others.

**(e) The single most useful fix.**

> Collect many more rabbit training photos, with much more variety — because the matrix shows the model predicts `rabbit` only 1 time in 12 while pushing 2 of the 4 real rabbits into `cat`, which is the pattern you get when a class is under-represented or under-varied in training, not when two classes genuinely look alike.

The reasoning behind picking that fix over the alternatives: if cats and rabbits simply looked similar, you'd expect confusion in **both** directions — some cats called rabbit. There are **zero** of those (the `true cat → said rabbit` cell is 0). The confusion runs one way only, which points at the rabbit class itself rather than at a cat/rabbit resemblance.

---

### Exercise 4 — Evaluate your own model honestly

Model answer, using a pen / pencil / marker classifier with 25 photos per class (75 total, 80/20 → 5 test per class).

**Split arithmetic (written before collecting):**
```
   per class: test = 0.20 × 25 = 5,  train = 20
   totals: test = 15, train = 60      check: 15 + 60 = 75  ✓
```

**Sessions:** training photos on the kitchen table in afternoon daylight; test photos in the bedroom under a desk lamp, two days later, held in my left hand instead of my right.

**Scoring sheet:**

| # | true | predicted | top conf. | correct? |
|---|---|---|---|---|
| 1 | pen | pen | 91% | Y |
| 2 | pen | pen | 84% | Y |
| 3 | pen | marker | 57% | N |
| 4 | pen | pen | 88% | Y |
| 5 | pen | pen | 72% | Y |
| 6 | pencil | pencil | 93% | Y |
| 7 | pencil | pencil | 81% | Y |
| 8 | pencil | pencil | 77% | Y |
| 9 | pencil | pen | 61% | N |
| 10 | pencil | pencil | 86% | Y |
| 11 | marker | marker | 89% | Y |
| 12 | marker | marker | 74% | Y |
| 13 | marker | pen | 55% | N |
| 14 | marker | marker | 68% | Y |
| 15 | marker | pen | 52% | N |

**Accuracy three ways:**
```
   correct = 11
   fraction:   11/15
   decimal:    15 × 0.7 = 10.5, remainder 0.5;  0.5 ÷ 15 = 0.0333
               0.7 + 0.0333 = 0.7333
   percentage: 73.3%

   baseline (3 equal classes) = 33.3%
   beats baseline by 40.0 percentage points
```

**Per-class accuracy:**

| class | correct | total | fraction | percentage |
|---|---|---|---|---|
| pen | 4 | 5 | 4/5 | 80.0% |
| pencil | 4 | 5 | 4/5 | 80.0% |
| marker | 3 | 5 | 3/5 | **60.0%** |
| overall | 11 | 15 | 11/15 | 73.3% |

**Confusion matrix:**

| | said pen | said pencil | said marker | row total |
|---|---|---|---|---|
| **true pen** | **4** | 0 | 1 | 5 |
| **true pencil** | 1 | **4** | 0 | 5 |
| **true marker** | 2 | 0 | **3** | 5 |
| **column total** | 7 | 4 | 4 | **15** |

Diagonal: 4 + 4 + 3 = 11 ✓. Total 15 ✓.

**The gap:**
```
   training accuracy (Under the hood): 60/60 = 100.0%
   test accuracy:                      11/15 =  73.3%
   gap:                                        26.7 percentage points
```

**Two sentences on the gap:** A 26.7-point gap tells me this model learned something genuinely transferable — 73.3% against a 33.3% baseline is not luck — but it also memorised a fair amount that was specific to my kitchen table and my right hand, because the only things I changed for the test session were room, light and hand, and that alone cost me a quarter of my score. The direction of the errors backs this up: the `said pen` column totals 7 against 5 real pens, and pens were the class I shot most often on the table, so the model appears to have partly learned "afternoon daylight on wood = pen."

**Verdict sentence:**

> *"On 15 held-out photos taken two days later in a different room under a lamp, the model scored 11/15 = 73.3% against a 33.3% baseline; it was worst at **marker** (3/5 = 60.0%), and its most common mistake was calling a marker a pen."*

**The 10-photo fix:** the largest off-diagonal cell is `true marker → said pen` at 2. Tomorrow I'd shoot 10 photos aimed squarely at that: 5 of the marker with its cap **on** (making it pen-shaped and forcing the model to find another difference) and 5 of the marker and a pen side by side at the same distance, so the size difference is the only thing available.

---

### Exercise 5 — Four cheating splits

**(a) 100 frames from a 10-second video, 20 picked at random as the test set.**

*What is leaking:* consecutive video frames are near-identical. A frame at 4.20 seconds and one at 4.25 seconds differ by almost nothing. Every test frame has an almost-twin sitting in the training set, so the model has effectively seen all of them.

*Direction:* **far too high.** You could easily report 95–100% for a model that fails on any real new photo.

*Fix:* split by **session**, not by frame. Shoot two separate videos in different places, use one for training and the other entirely for testing. Random splitting only works when the examples are genuinely independent of each other.

**(b) Train, test (65%), add photos, retrain, test (78%), report 78%.**

*What is leaking:* the *decision* about what to change was made by looking at the test set. The test set has become part of the training process — it just entered through your brain instead of through the upload button. Report 78% and you're reporting the best of two attempts on the same exam.

*Direction:* **too high**, and it gets worse with every extra round. Ten rounds of "tweak until the test score goes up" can inflate a score enormously.

*Fix:* collect a **third** set of photos, never touched during any tweaking, and report the score on that. (In Level 2 you'll learn the standard names for these three sets. For now: if you used it to make a decision, it isn't a test set any more.) At minimum, state honestly: *"78% on the second attempt, after adding photos in response to the first test."*

**(c) Test photos from the same session as training, but held by a friend.**

*What is leaking:* the background, the lighting, the surface, the camera position, the time of day — everything except the hands. Changing one variable out of six is not a fresh test.

*Direction:* **too high**, but less badly than (a). It's a partial test: it genuinely measures whether the model over-relied on your hands, and genuinely fails to measure everything else.

*Fix:* change the room and the light as well. But there is something worth keeping here — the friend's hands are a good idea, just not sufficient on their own. Report it accurately as what it is: *"tested on new hands in the same room and light,"* so a reader knows exactly which weakness was checked and which were not.

**(d) Predicting which pupils need extra maths help, tested on the same class, deployed on next year's Year 7.**

*What is leaking:* time and population. Next year's pupils came from different primary schools, had different teachers, and sat a different set of tests. The model was measured on the group it grew up with.

*Direction:* **too high** — and this one is the most dangerous of the four, because the gap won't show up for a whole year, and by then decisions about real children will already have been made on the basis of it.

*Fix:* if you have data from previous years, train on the older years and test on the most recent one — a **split by time**, which mimics how the model will actually be used. If you have only one year of data, then you cannot honestly estimate next year's performance at all, and the right move is to say so loudly and run the system as a suggestion for a teacher to check, never as a decision.

**The thread running through all four:** a test set is only honest if it differs from the training set **in the same ways the real world will differ**. Random shuffling assumes your examples are independent. Frames, sessions, tweaking rounds, and school years are all ways that assumption quietly fails.

---

### Exercise 6 — The number that lies

**(a) The two confusion matrices.**

**Model A** (real 82/100 correct, spam 98/100 correct):

| | said real | said spam | row total |
|---|---|---|---|
| **true real** | **82** | 18 | 100 |
| **true spam** | 2 | **98** | 100 |
| **column total** | 84 | 116 | **200** |

Diagonal: 82 + 98 = **180** → 180/200 = 90% ✓

**Model B** (real 98/100 correct, spam 82/100 correct):

| | said real | said spam | row total |
|---|---|---|---|
| **true real** | **98** | 2 | 100 |
| **true spam** | 18 | **82** | 100 |
| **column total** | 116 | 84 | **200** |

Diagonal: 98 + 82 = **180** → 180/200 = 90% ✓

Identical headline. Completely different machines.

**(b) My own personal inbox → Model B.**

The two mistakes cost wildly different amounts. A spam email that reaches my inbox costs me about two seconds and a small amount of irritation. A real email wrongly filed as spam might be a message from a teacher, a doctor's appointment, or a friend — and I will probably never know it arrived, because nobody reads their spam folder.

Model A dumps **18 out of every 100 real emails** into the spam folder. That's roughly one in five. It is unusable, no matter how good it is at catching spam. Model B loses 2 in 100 real emails and lets 18 in 100 spam through, which is a mildly annoying inbox and a functioning one.

**(c) A hospital email system facing phishing → Model A.**

Here the costs flip completely. A single successful phishing email can lock up patient records and put people at real risk. Eighteen legitimate emails going to a quarantine folder is a genuine problem, but it is a **recoverable** one — someone reviews the quarantine, releases them, and the delay is hours rather than a catastrophe. A phishing email getting through is not recoverable.

So the hospital should take Model A's 98% spam catch rate and staff a quarantine review process to absorb the cost of the 18% false alarms.

**The general principle:** you cannot choose between these two models by looking at accuracy, because their accuracies are identical. You choose by asking **what each kind of mistake actually costs, to whom** — and that is a question about the world, not about the data.

**(d) Recomputing for a realistic inbox: 90 real, 10 spam.**

Apply each model's per-class rates to the realistic mix.

**Model A** (gets 82% of real right, 98% of spam right):
```
   real correct  = 0.82 × 90 = 73.8   →  real wrongly binned = 90 − 73.8 = 16.2
   spam correct  = 0.98 × 10 = 9.8    →  spam getting through =  10 − 9.8  = 0.2

   overall accuracy = (73.8 + 9.8) ÷ 100 = 83.6 ÷ 100 = 0.836 = 83.6%
```

**Model B** (gets 98% of real right, 82% of spam right):
```
   real correct  = 0.98 × 90 = 88.2   →  real wrongly binned = 90 − 88.2 = 1.8
   spam correct  = 0.82 × 10 = 8.2    →  spam getting through =  10 − 8.2  = 1.8

   overall accuracy = (88.2 + 8.2) ÷ 100 = 96.4 ÷ 100 = 0.964 = 96.4%
```

| on 100 realistic emails | Model A | Model B |
|---|---|---|
| real emails wrongly binned | **16.2** | **1.8** |
| spam getting through | **0.2** | **1.8** |
| overall accuracy | **83.6%** | **96.4%** |

**Did my answer to (b) change?** No — it got much stronger, and in a way I didn't expect from the balanced test.

On the balanced 100/100 test set the two models looked like mirror images, a fair trade of one error type for the other. On a realistic inbox they are not remotely equivalent. Because 90% of the mail is real, Model A's 18% false-alarm rate is applied to a much bigger pile: it bins **16.2** genuine emails to stop **1.6** extra spam messages. Model B loses only 1.8 real emails. Model B is better on both the harm I care about *and* on raw accuracy — 96.4% against 83.6%.

**The lesson underneath this, which is the point of the whole exercise:** the balanced test set made the two models look like a philosophical dilemma. The realistic mix showed it was mostly an arithmetic question all along. **A test set that doesn't match the real-world mix of classes will not just give you a wrong number — it can give you a wrong decision**, and you will make that decision feeling like you weighed it carefully.

Two honest footnotes. First, the hospital answer from (c) *does* survive this recalculation, because there the cost of one phishing email is so enormous that 16 quarantined emails are still worth it — the arithmetic changed but the cost asymmetry is bigger. Second, the fractional emails (73.8, 16.2) are averages over many days, not individual messages. You cannot bin 0.8 of an email; you bin 16 on one day and 17 on the next.

---

</details>

---

[⬅ Previous](module-05-learning-from-examples.md) · [Level 1 Home](README.md) · [Next ➡](module-07-how-computers-see.md)

*Next up: you now know your model is worst at combs — but not **why**. To answer that you have to see what the machine sees, and it isn't a photo. Module 7 zooms in until the picture dissolves into a grid of brightness numbers, and shows you how to find edges in it with arithmetic you can do on graph paper.*

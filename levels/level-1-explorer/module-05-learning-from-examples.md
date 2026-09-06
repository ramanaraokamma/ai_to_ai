# Module 5 — Learning From Examples: Train Your First Model (No Code)

**Level 1 · Module 5 · ~3 hours · Prereqs: Module 3 (the machine learning trade), Module 4 (features, labels, classes, baseline)**

[⬅ Previous](module-04-features-and-labels.md) · [Level 1 Home](README.md) · [Next ➡](module-06-train-test-trust.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** train a working three-class image classifier in Teachable Machine, from a blank page to a live prediction, without help.
2. **You will be able to** explain what changed inside the model when you added more examples — in plain words, with no maths.
3. **You will be able to** read a confidence score and say exactly what a 62% guess means, and what it does *not* mean.
4. **You will be able to** deliberately make your own model worse in four different ways and name exactly which data change caused each failure.
5. **You will be able to** look at a set of training photos and predict, before training, which weakness the model will have.

---

## 🪝 The Hook

In 2016, three researchers built a picture classifier on purpose to be bad — and then they didn't tell anyone.

Their model told huskies apart from wolves. It worked. On new photos it was right most of the time, and when they showed it to a room of people who study machine learning for a living and asked *"do you trust this model?"*, most said yes.

Then the researchers revealed the trick. Every wolf photo in their training set had **snow** in the background. Not one husky photo did. The model had never learned anything about wolves. It had learned: *white fuzzy stuff at the bottom of the picture → say wolf.* Photograph a husky standing in snow and it says wolf, every time, with total confidence.

Nobody wrote that rule. Nobody wanted it. It came from the photos, because **the model learns whatever pattern is easiest to find, not the pattern you meant.**

In the next three hours you are going to build a model of your own in a browser, in about twenty seconds. Then you are going to do something more valuable than building it: you are going to break it four times on purpose, and know precisely why each break happened.

---

## 🧠 The Concept

Five ideas. Each one has a plain explanation, an everyday anchor, and small numbers you can check.

---

### 1️⃣ Training is the process that turns examples into a model

In Module 3 you made a trade: stop writing rules, hand over labelled examples instead. **Training is the moment that trade actually happens.**

```
   ┌──────────────────┐        ┌──────────────┐        ┌───────────────┐
   │  LABELLED        │        │              │        │               │
   │  EXAMPLES        │ ─────► │   TRAINING   │ ─────► │     MODEL     │
   │                  │        │              │        │               │
   │ 40 spoon photos  │        │  the machine │        │ the finished  │
   │ 40 toothbrush    │        │  hunts for   │        │   guessing    │
   │ 40 comb photos   │        │  patterns    │        │    machine    │
   └──────────────────┘        └──────────────┘        └───────────────┘
     you make this            happens once,            you use this
                              takes ~20 seconds        over and over
                                                              │
                                                              ▼
                                                   ┌───────────────────┐
     a NEW photo the model  ──────────────────────►│   PREDICTION      │
     has never seen                                │ "spoon, 91% sure" │
                                                   └───────────────────┘
```

> **Training** — the one-off process where a machine looks at labelled examples over and over and adjusts itself until its guesses on those examples get as good as it can make them.

Two words in there matter enormously.

**"Over and over."** The machine does not read your 120 photos once. It goes through all of them, checks how many it got wrong, nudges itself, and goes through them all again. One full pass through every example is called an **epoch**. Teachable Machine does 50 by default. So your 120 photos are examined 120 × 50 = **6,000 times** in total.

**"Adjusts itself."** This is the part people find magical, and it isn't. Imagine tuning an old radio: you turn the dial slightly, listen, hear more static, turn it back the other way, listen again. The machine has thousands of tiny dials. Each epoch it nudges every one of them in whichever direction reduced its mistakes. After 50 rounds of nudging, the dials sit where the mistakes are fewest. Nobody chose the dial positions. Nobody could read them if they tried.

**🍕 Analogy — learning to spot your friend in a crowd.**
Nobody ever gave you a rule for recognising your best friend. Nobody said "nose 4.2 cm, eyebrow angle 12 degrees." You just saw them thousands of times with their name attached. Then one day you could pick them out of a crowd from behind, at 40 metres, in bad light — and you cannot explain how. That's training. You are the model. Your friend's face is the class.

**🔢 Tiny number check — how much work is 20 seconds?**
120 photos × 50 epochs = 6,000 photo-examinations. If a human looked at one photo per second without stopping, that's 6,000 seconds = 100 minutes. The browser does it in about twenty seconds while you watch a progress bar. Not magic — just very fast arithmetic, repeated.

---

### 2️⃣ A model is the guessing machine that comes out of training

> **Model** — the thing training produces: a machine that takes in a new example and puts out a guess.

The single most useful thing to understand about a model is what it **is not**.

| A model is NOT | A model IS |
|---|---|
| a copy of your photos | a set of dial settings, tuned by your photos |
| a program a human wrote | a program a process produced |
| something you can read | something you can only test |
| aware of what a spoon "is" | aware that certain patterns of light went with the word "spoon" |

That last row is the one to remember. Your model will never know that a spoon holds soup. It has no idea soup exists. It has found that a particular arrangement of brightness, curve, and shine tended to appear when you typed the word "spoon" — and that is the entire extent of its understanding.

**🍕 Analogy — the recipe and the cake.**
The examples are your ingredients. Training is the baking. The model is the cake. Once it's baked you cannot get the eggs back out, you cannot read the recipe off the cake, and if the cake is bad the only fix is **to bake a new one with better ingredients**. You never fix a model by arguing with it. You fix it by changing the examples and training again.

**🔢 Tiny example — how small a model can be.**
A Teachable Machine image model is a few megabytes — smaller than one high-quality photo from a modern phone. Yet it was made from 120 photos totalling maybe 40 megabytes. **The model is much smaller than the data that made it.** It could not be storing your pictures. It genuinely compressed them into a pattern.

⚠️ One honest note about how Teachable Machine cheats in your favour. It does not start from nothing. It begins with a model Google already trained on **millions** of everyday photographs — a model that already recognises edges, curves, shininess, fur, wood grain. Your 40 photos only teach the last small step: *which of those already-known patterns go with which of your three names*. That is why 40 photos is enough and why it takes 20 seconds instead of a week. You are not building a brain from scratch; you are giving names to a vocabulary that already exists. (Level 3 pulls this apart properly.)

---

### 3️⃣ Classes and class balance: 200 of one and 8 of another is a broken model

You met **class** in Module 4: one of the possible values of a category label. In Teachable Machine, each class is a box you name and fill with photos.

> **Class balance** — how evenly your examples are spread across the classes. Roughly equal counts is balanced; wildly unequal counts is **imbalanced**.

Here's why imbalance quietly destroys a model. Training nudges the dials to reduce **total mistakes across all your examples**. It does not care which class the mistakes come from. So if one class is enormous, the cheapest way to reduce total mistakes is to lean towards that class and abandon the small one.

**🍕 Analogy — the class vote.**
Thirty children vote on the school trip. Twenty-eight want the zoo, two want the museum. The zoo wins, and it will win every time, forever. The two museum voters are not outvoted on the merits — they're outvoted on the count. Now imagine the vote decides what your model believes.

**🔢 Worked arithmetic — the 98% model that is worthless.**

You train a three-class model with:

| class | training photos |
|---|---|
| spoon | 200 |
| toothbrush | 200 |
| comb | 8 |
| **total** | **408** |

Suppose the model gives up on combs entirely and never outputs "comb." How well does it do on its own training photos?

```
   correct  = 200 (spoons) + 200 (toothbrushes) + 0 (combs)
            = 400

   accuracy = 400 ÷ 408
            = 0.98039...
            ≈ 98.0%
```

**98% accuracy.** That number would look fantastic in a report. And the model is 0% correct on every single comb — the class you presumably added because you cared about combs.

The fix is boring and effective: **make the counts roughly equal.** Either collect more combs (up to ~200) or cut the other two down (to ~8… no — to something like 40 each). Aim for every class within about 20% of every other. In the worked example below, 41 / 40 / 39 is nicely balanced; 200 / 200 / 8 is not.

⚠️ There is a second, sneakier kind of imbalance: **balance inside a class.** Forty spoon photos where thirty-five are the same teaspoon on the same table is not forty examples of "spoon." It is basically five examples with thirty-five copies of one of them. Count *distinct situations*, not shutter clicks.

---

### 4️⃣ A confidence score is the model's guess strength — not its correctness

When you hold an object up to your trained model, it won't say "spoon." It will say something like this:

```
   spoon       ████████████████████░░░░░░░░░░   62%
   toothbrush  ███████░░░░░░░░░░░░░░░░░░░░░░░   21%
   comb        █████░░░░░░░░░░░░░░░░░░░░░░░░░   17%
                                              ─────
                                               100%
```

> **Confidence score** — how strongly the model prefers each class, given as percentages that always add up to 100%.

Always adding to 100% is the key to reading these correctly. The model has exactly **100 points of belief** and must hand every point to one of the boxes you gave it. It is not answering *"is this a spoon?"* It is answering *"of these three, which fits best?"* — and it is **forced to answer**, even if you show it a shoe.

So what does 62% actually mean? Say it like this:

> *"Of the three options I was given, spoon fits best — but 38 points of my belief went somewhere else. I am not comfortable."*

A quick trick that's worth more than the top number alone:

> **Margin** — the top score minus the second-highest score. It tells you how close the race was.

| top | second | margin | read it as |
|---|---|---|---|
| 91% | 5% | **86** | not even close — a clear winner |
| 62% | 21% | **41** | reasonably clear |
| 44% | 30% | **14** | shaky — a small change could flip it |
| 39% | 34% | **5** | basically a coin toss dressed up as an answer |

**🍕 Analogy — the multiple-choice exam.**
You must tick A, B, or C. You have no idea, so you tick B because it feels slightly less wrong. Your answer sheet says "B" with total certainty; it does not record your shrug. The confidence score is the shrug the model is honest enough to show you. Most AI products throw the shrug away and show you only the letter.

**🚨 The rule you must not forget:** confidence is **not** the chance of being right. In the worked example below, a model looks at a **fork** — an object it has never seen and has no box for — and reports 74% spoon. It is 74% confident and 100% wrong. High confidence and correctness are two different things that people constantly mistake for one.

---

### 5️⃣ Data quality beats data quantity

Everybody's first instinct when a model is bad is "add more photos." Sometimes that's right. Often it's the worst thing you can do, because **thirty near-identical photos teach the model roughly what one photo teaches it** — while making you feel like you did thirty times the work.

> **Variety** — how much your examples differ from one another in the ways that don't matter, so the model is forced to learn the thing that does.

Think about what a spoon photo contains besides the spoon: a background, a light source, an angle, a distance, a hand, a shadow. If **all forty** of your spoon photos share a wooden table and a window on the left, then "wooden table + light from the left" is a far easier pattern to find than "spoon." Training will find the easy one. That's the wolves-and-snow story, and it is not a rare bug — it is the default outcome.

**🍕 Analogy — the maths test you revised for wrongly.**
You practise 40 questions, all of them `? × 7`. You get brilliant at sevens. The test has `6 × 8` and you're lost. You didn't practise *multiplication*, you practised *sevens* — because that's what was in front of you. Forty questions felt like a lot of revision. Four questions across four different times tables would have taught you more.

**🔢 Tiny example — two sets of 40 photos.**

| | Set A (quantity) | Set B (quality) |
|---|---|---|
| photos | 40 | 40 |
| backgrounds | 1 (wooden table) | 5 (table, carpet, sink, bed, floor) |
| lighting | 1 (afternoon window) | 3 (window, ceiling light, lamp) |
| angles | 2 | 8 |
| distances | 1 | 3 |
| **distinct situations** | 1 × 1 × 2 × 1 = **2** | 5 × 3 × 8 × 3 = **360** (well, 40 sampled from that space) |

Same effort. Same count. Set B produces a model that works in your kitchen *and* your bedroom. Set A produces a model that works on one table in the afternoon.

**The variety checklist** — use this every single time you collect photos:

```
   ┌─────────────────────────────────────────────────────┐
   │  VARIETY CHECKLIST — vary these while shooting      │
   ├─────────────────────────────────────────────────────┤
   │  □ background     at least 3 different surfaces     │
   │  □ lighting       at least 2 (window + electric)    │
   │  □ angle          front, side, tilted, from above   │
   │  □ distance       close, medium, far                │
   │  □ rotation       turn the object as you shoot      │
   │  □ hand           held AND lying down alone         │
   │  □ partly hidden  a few with a corner covered       │
   └─────────────────────────────────────────────────────┘
```

⚠️ And one hard rule that makes everything else work: **whatever you vary for one class, vary for all of them.** If your spoons are all on the table and your combs are all on the carpet, you have not built an object classifier. You have built a floor-covering classifier that happens to be right.

---

## 🔍 Worked Example

**The Spoon–Toothbrush–Comb Machine.** A complete session, start to finish, with every number recorded. Your numbers will be different — the *pattern* of the numbers is what you're learning to read.

### Step 1 — Choose three classes, and choose them to be hard

Three objects: **spoon**, **toothbrush**, **comb**.

Why these? Because they're all small, long, thin, and held in a hand. A model that tells these three apart has genuinely learned something. A model that tells apart a shoe, a banana, and a bicycle has learned "big brown thing / yellow curve / lots of metal" and proves nothing.

Classes: **3**. Task type: **multi-class classification** (Module 4). Baseline if you guessed blindly with equal classes: **1 in 3 = 33.3%**.

### Step 2 — Plan the photos before touching the camera

Target: about **40 photos per class**, spread across the variety checklist.

```
   PHOTO PLAN (per class)
   ─────────────────────────────────────────────
   kitchen table, window light, held    ×  8
   kitchen table, window light, alone   ×  6
   carpet, ceiling light, held          ×  8
   bathroom sink, ceiling light, held   ×  6
   bed sheet, lamp, held                ×  6
   any surface, far away / tilted       ×  6
   ─────────────────────────────────────────────
                                  TOTAL  40
```

### Step 3 — Collect. Here's what actually landed.

| class | photos collected |
|---|---|
| spoon | 41 |
| toothbrush | 40 |
| comb | 39 |
| **total** | **120** |

Balance check: largest 41, smallest 39. Difference = 2, which is 2 ÷ 41 ≈ **4.9%** — comfortably inside the 20% guideline. ✅ Balanced.

### Step 4 — Train

Settings left at the defaults: **50 epochs**, **batch size** 16, **learning rate** 0.001. Batch size is how many photos it looks at before each nudge; learning rate is how big each nudge is. You do not need to touch either one — leave them alone and just notice they exist.

Training took **about 22 seconds**. During that time the machine examined 120 × 50 = **6,000 photo-instances** and nudged its dials after each batch.

Nothing visible happened. There is no "aha." A progress bar filled up and a model existed.

### Step 5 — Test the baseline model live

Hold each real object in front of the webcam and read the three bars.

| test | spoon | toothbrush | comb | sum | predicted | true | ✓/✗ | margin |
|---|---|---|---|---|---|---|---|---|
| hold a spoon | **91%** | 5% | 4% | 100% | spoon | spoon | ✓ | 91 − 5 = **86** |
| hold a toothbrush | 6% | **88%** | 6% | 100% | toothbrush | toothbrush | ✓ | 88 − 6 = **82** |
| hold a comb | 8% | 13% | **79%** | 100% | comb | comb | ✓ | 79 − 13 = **66** |

Three for three, all with large margins. Note that the comb's margin (66) is the smallest of the three — a comb and a toothbrush are the most similar pair, and the model already feels that. **The margins told you where the weakness is before anything went wrong.**

This is the **baseline model**. Every experiment below changes exactly one thing and compares back to this table.

---

### Step 6 — Experiment 1: fewer photos (5 per class instead of 40)

Delete samples until each class has only 5 photos. Total: 15. Retrain. Training takes about 6 seconds.

| test | spoon | toothbrush | comb | sum | predicted | true | ✓/✗ | margin |
|---|---|---|---|---|---|---|---|---|
| hold a spoon | **62%** | 21% | 17% | 100% | spoon | spoon | ✓ | **41** |
| hold a toothbrush | 30% | **44%** | 26% | 100% | toothbrush | toothbrush | ✓ | **14** |
| hold a comb | 25% | **41%** | 34% | 100% | toothbrush | comb | ✗ | **7** |

**What changed:** 2 correct out of 3 instead of 3 out of 3 — but look past that. Every single margin collapsed: 86 → 41, 82 → 14, 66 → 7. Even the two correct answers are barely holding on.

**Why:** with 5 photos the model saw almost no variety. It found *some* pattern (better than random — 62% beats the 33% baseline) but a thin, fragile one. **Too few examples doesn't produce wrong answers so much as unstable ones**, and unstable answers become wrong answers the moment anything shifts.

---

### Step 7 — Experiment 2: one background only

Back to 40 photos per class, but every photo taken on the **same wooden table** with the same window light. Retrain.

Test on the table (where it was trained):

| test | spoon | toothbrush | comb | sum | predicted | true | ✓/✗ | margin |
|---|---|---|---|---|---|---|---|---|
| spoon, on the wooden table | **95%** | 3% | 2% | 100% | spoon | spoon | ✓ | **92** |

Better than the baseline! 95% versus 91%. Now move two metres and hold the same spoon over the **white bathroom sink**:

| test | spoon | toothbrush | comb | sum | predicted | true | ✓/✗ | margin |
|---|---|---|---|---|---|---|---|---|
| spoon, over the white sink | 34% | **39%** | 27% | 100% | toothbrush | spoon | ✗ | **5** |

**What changed:** the same object, the same model, two metres apart — from 95% right to a 5-point coin toss that lands wrong.

**Why:** the wooden table appeared in every single training photo, so "warm brown texture in the background" became part of what the model believes a spoon looks like. Remove the table and a chunk of the evidence vanishes. This is the wolf-and-snow failure, reproduced in your own bathroom in ten minutes.

**And notice the trap.** On its home turf this model scored *higher* than the good one. If you only ever tested where you trained, you would conclude the single-background model was **better**. That trap has a name and Module 6 is entirely about it.

---

### Step 8 — Experiment 3: blurry photos

40 per class again, full variety — but shot while deliberately waving the object so most frames are motion-blurred. Retrain.

| test | spoon | toothbrush | comb | sum | predicted | true | ✓/✗ | margin |
|---|---|---|---|---|---|---|---|---|
| spoon, held still and sharp | **58%** | 24% | 18% | 100% | spoon | spoon | ✓ | **34** |
| comb, held still and sharp | 22% | 33% | **45%** | 100% | comb | comb | ✓ | **12** |

**What changed:** still correct, but margins dropped hard (86 → 34, 66 → 12).

**Why:** blur destroys edges, and edges are the most useful thing in a small object photo (Module 7 shows you exactly why). Feeding blurry photos is like teaching someone to recognise faces using only out-of-focus pictures — they'll manage, badly.

**The subtle bit:** this model was trained blurry and tested **sharp**, and it still struggled. The mismatch cuts both ways. A model trained only on perfect studio photos will also fail on the wobbly ones real people take. **Your training photos should look like the photos the model will actually meet.**

---

### Step 9 — Experiment 4: the surprise fourth object

Back to the good baseline model — 40 photos each, three classes, 91/88/79 performance. Now hold up a **fork**. There is no fork class. There never was.

| test | spoon | toothbrush | comb | sum | predicted | true | ✓/✗ | margin |
|---|---|---|---|---|---|---|---|---|
| hold a **fork** | **74%** | 15% | 11% | 100% | spoon | *(none of these)* | ✗ | **59** |

**74% confident. Margin of 59 — bigger than the margin on the real comb. And completely wrong.**

**Why:** the model has 100 points of belief and exactly three boxes. It cannot say "I don't know," it cannot say "fork," it cannot say "none of the above." Those aren't options you gave it. So it does the only thing available: it finds the closest of your three boxes and commits.

If this feels familiar, it should — it's the lime from Module 4, wearing a different hat. **A model can only ever say what is on your list of classes.** The one useful defence is to add a class called `nothing / other` and fill it with 40 photos of your empty hand, your desk, a fork, a pen, a wall. It won't be perfect, but it gives the model somewhere honest to put its belief.

---

### Step 10 — The results table

| # | what I changed | spoon test | margin | verdict | the one-line reason |
|---|---|---|---|---|---|
| 0 | *(baseline: 40 each, full variety)* | 91% ✓ | 86 | works | enough varied examples of each class |
| 1 | 5 photos per class | 62% ✓ | 41 | fragile | too few examples → a thin, unstable pattern |
| 2 | one background only | 95% ✓ *on the table*, 34% ✗ *at the sink* | 92 / 5 | broken elsewhere | the background became part of the class |
| 3 | blurry training photos | 58% ✓ | 34 | weakened | blur destroys edges, the most useful signal |
| 4 | showed it a fork | 74% ✗ | 59 | confidently wrong | no box for "fork" and no way to say "I don't know" |

Read down the margin column. It moves *before* the verdict does. Experiments 1 and 3 were still technically correct while their margins were quietly falling apart. **The margin is an early warning system; the right/wrong column is a late one.**

---

### Step 11 — One more: deliberate class imbalance

Take the good model. Delete comb photos until only **8** remain, leaving spoon 200, toothbrush 200, comb 8 (padded up from the originals). Retrain.

| test | spoon | toothbrush | comb | sum | predicted | true | ✓/✗ |
|---|---|---|---|---|---|---|---|
| hold a spoon | **93%** | 5% | 2% | 100% | spoon | spoon | ✓ |
| hold a toothbrush | 7% | **90%** | 3% | 100% | toothbrush | toothbrush | ✓ |
| hold a comb | 12% | **77%** | 11% | 100% | toothbrush | comb | ✗ |

Look at the comb row. The model gives the comb class **11 points out of 100** while staring straight at a comb. It has essentially stopped believing combs exist.

And the arithmetic from sub-concept 3 plays out exactly:

```
   photos:   spoon 200 + toothbrush 200 + comb 8  =  408
   a model that never says "comb" gets:
             200 + 200 + 0  =  400 correct
   accuracy: 400 ÷ 408 = 0.98039… ≈ 98.0%
```

A model that is **98% accurate** and **completely blind to one third of its job**. Nobody lied. The number is real. It just answers a question nobody should have asked.

---

## 💻 Hands-On

No programming. One browser tab, one webcam (or a phone camera and the Upload button), about 70 minutes.

### Activity A — Be the model, unplugged (10 min)

Do this *before* you touch the computer. It takes ten minutes and makes everything after it obvious.

1. Get 12 small pieces of paper. On 6 of them draw a **circle**. On 6 draw a **square**. Vary them: big, small, wobbly, tilted, thick pen, thin pen.
2. Shuffle. Hand them to another person face-down, one at a time, saying the label out loud each time: *"circle… square… circle…"* They just look and listen. They may not ask questions. **That is training.**
3. Now draw 4 brand-new shapes they've never seen — including one deliberately ambiguous rounded-square blob.
4. Show each one. They must say "circle" or "square" **and** give a confidence out of 100. Write down all four answers.
5. Finally, show them a **triangle**.

Watch what happens on the triangle. They have to say circle or square, they'll pick one, and they'll be uncomfortable. Ask for their confidence. That discomfort — the thing your friend can feel and a computer cannot — is exactly what Step 9 was about.

✅ **Done when:** you have 5 recorded guesses with confidences, and one sentence about what the triangle proved.

---

### Activity B — Train your first model in Teachable Machine (30 min)

**Step 1 — Open it.**
Go to **teachablemachine.withgoogle.com** → click **Get Started** → choose **Image Project** → choose **Standard image model**.

Nothing installs. Nothing needs an account. Your photos stay in your browser — they are not uploaded anywhere unless you deliberately export a model.

**Step 2 — Set up three classes.**

```
   ┌──────────────────────┐   ┌─────────────┐   ┌──────────────────────┐
   │  Class 1  [✎]        │   │             │   │   Preview            │
   │  ┌────────┬───────┐  │   │   Train     │   │                      │
   │  │ Webcam │ Upload│  │   │   Model     │   │  spoon      ▁▁▁▁     │
   │  └────────┴───────┘  │──►│             │──►│  toothbrush ▁▁▁▁     │
   ├──────────────────────┤   │  [ Train ]  │   │  comb       ▁▁▁▁     │
   │  Class 2  [✎]        │   │             │   │                      │
   │  ...                 │   │  Advanced ▾ │   │  Export Model        │
   ├──────────────────────┤   └─────────────┘   └──────────────────────┘
   │  + Add a class       │
   └──────────────────────┘
```

- You start with two class boxes. Click **Add a class** to get a third.
- Click the **pencil icon** beside each name and rename them to your three objects. Never leave them as `Class 1` — in three days you will not remember which was which.

**Step 3 — Collect photos, one class at a time.**

- Click **Webcam** in the first class, allow camera access, hold the object up, and press and hold **Hold to Record**.
- ⚠️ **Do not hold it down for 20 seconds.** You'll get 200 near-identical frames, which is Set A from sub-concept 5. Instead: record a **2-second burst**, stop, move the object (new angle, new distance, new background), record another 2-second burst. Repeat until you have about 40.
- The small **gear/settings icon** above the webcam lets you change frames-per-second and add a delay. The defaults are fine.
- **No webcam?** Click **Upload** instead and drag in photos taken on a phone. This is often better — you can walk around the house between shots.
- Work through the variety checklist as you go, and tick items off out loud.

**Step 4 — Check your balance before training.**
Each class box shows its sample count. Write the three numbers down:

```
   spoon: ____     toothbrush: ____     comb: ____
   biggest − smallest = ____ ,   ÷ biggest = ____ %   (want under 20%)
```

If one class is far ahead, either collect more of the others or use the class's **three-dot menu → Remove All Samples** and redo it. Fixing this now takes five minutes; discovering it later costs you the whole model.

**Step 5 — Train.**
Click **Train Model**. Keep the tab visible and in the foreground — browsers throttle background tabs and training can stall. Expect 15–40 seconds.

**Step 6 — Test live and write the numbers down.**
The Preview panel is now live. Hold up each object and record the three percentages. Use this sheet:

| test | class A % | class B % | class C % | sum | predicted | true | ✓/✗ | margin |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |

**Always check the sum is 100.** If it isn't, you misread a bar. Always compute the margin — it's the number that actually tells you something.

**Step 7 — Save your work.**
Click the **☰ menu (top-left) → Save project to Drive** (needs a Google account) or **Download project as file** (gives you a `.tm` file you can reopen later). Do this before you start breaking things in the mini-project — you want the good version back.

✅ **Done when:** a trained three-class model correctly identifies all three objects, and you have a filled 3-row results table with margins.

---

### Activity C — Read confidence like an expert (10 min)

For each reading below, work out the sum, the prediction, and the margin, then write what you'd actually *do*.

| # | class A | class B | class C | sum | predicted | margin | your call |
|---|---|---|---|---|---|---|---|
| 1 | 97% | 2% | 1% | | | | |
| 2 | 51% | 45% | 4% | | | | |
| 3 | 40% | 33% | 27% | | | | |
| 4 | 68% | 30% | 2% | | | | |

Then answer three questions in writing:
- Which reading would you trust enough to act on without checking?
- Which one is technically a "prediction" but really a shrug?
- If a real product showed only the winning class name and hid the percentages, which of these four would be the most dangerous to hide?

---

### Activity D — Predict the failure before it happens (20 min)

This is the skill that separates someone who can click buttons from someone who understands the machine.

1. Look at your own collected photos — properly, scroll through all 120.
2. **Before testing anything**, write down one prediction in this exact form:

   > *"This model will fail when ________, because ________ appears in all my ________ photos and in none of my ________ photos."*

3. Now go and create that exact situation and test it. Record the confidences.
4. Were you right? Write two sentences either way.

Real predictions from real learners: *"It'll fail on my green comb because all my comb photos are the blue one."* *"It'll call anything held in my left hand a spoon, because I'm right-handed and only the spoon photos got shot left-handed."* Both were correct.

---

## ✍️ Practice

**[Warm-up] 1 — Read the scores.**
For each set of confidences, state (i) the prediction, (ii) the margin, (iii) whether you'd call it confident, shaky, or a coin toss, and (iv) one sentence on what the numbers tell you about the training data.
(a) cat 96%, dog 3%, rabbit 1%
(b) cat 45%, dog 41%, rabbit 14%
(c) cat 34%, dog 33%, rabbit 33%
(d) cat 80%, dog 19%, rabbit 1% — *and the true answer was rabbit*
*Done looks like:* four blocks with all four parts answered, each sum checked to 100, and for (d) a specific explanation of how a model can be 80% confident and wrong.

**[Warm-up] 2 — Class balance arithmetic.**
A model is trained to spot three kinds of leaf: oak 150 photos, maple 150 photos, willow 12 photos.
(a) What is the total number of photos?
(b) If the model never outputs "willow," what accuracy does it get on its own training photos? Show the division and give a percentage to one decimal place.
(c) What accuracy does it get **on willow leaves specifically**?
(d) Rewrite the photo counts to fix the imbalance in two different ways, and say which you'd choose and why.
*Done looks like:* four answers, the division written out, and a stated preference with a reason involving effort or data availability.

**[Build] 3 — The variety audit.**
Take the photos you collected in Hands-On Activity B and audit them properly. For each class, count how many photos fall into each bucket:

| class | backgrounds used | lighting types | angles | held vs alone | distinct situations (multiply) |
|---|---|---|---|---|---|

Then answer: which class has the least variety, and what would you shoot tomorrow to fix it?
*Done looks like:* a completed audit table with real counts for all three classes, a named weakest class with its numbers, and a specific shot list of at least 6 new photos to take.

**[Build] 4 — The fewer-photos experiment, measured properly.**
Train the same three classes **three separate times**: with 5 photos per class, 15 per class, and 40 per class. After each, test the same three objects in the same place with the same lighting, and record all nine confidence readings.

| photos per class | obj 1 top % | margin | obj 2 top % | margin | obj 3 top % | margin | # correct /3 |
|---|---|---|---|---|---|---|---|

*Done looks like:* a filled 3-row table, plus a short paragraph answering: **did the number correct improve steadily, or did the margins improve while the number correct stayed the same?** Say what that tells you about using "number correct" as your only measure.

**[Stretch] 5 — Break it your own way.**
Invent a **fifth** way to sabotage a model that is not in this module's list of four (not "fewer photos," "one background," "blur," or "surprise object"). Ideas people have used: photograph one class only at night; mislabel five photos on purpose; include your face in every photo of one class; use a mirror for one class only; photograph one class through a window.
Write a prediction **first**, then run it, then report.
*Done looks like:* a named sabotage, a written before-the-fact prediction with a stated reason, a results table with at least 3 test readings and margins, and a verdict on whether your prediction was right — including an honest "I was wrong because…" if you were.

**[Stretch] 6 — Write the confidence policy.**
Imagine your classifier is being put into a real product: a machine at a recycling centre that sorts items into `plastic / paper / metal`. Getting it wrong sends recyclable material to landfill.
Write a **confidence policy**: for each band of top-score and margin, what should the machine actually do? Options include: sort it automatically, put it aside for a human, send it round the belt again for a second photo, stop the line.
*Done looks like:* a table with at least 4 bands defined by **both** top score and margin (not top score alone), an action for each, a sentence justifying where you drew each boundary, and a closing paragraph on who should be allowed to change these numbers later — the engineer, the recycling centre manager, or the public — and why.

---

## 🤔 Think Deeper

**1. If nobody can read the model, who is responsible when it's wrong?**
Your model is a few megabytes of dial settings that no human chose and no human can read. It confidently calls a fork a spoon. Who is at fault — you, for the photos? Google, for the starting model trained on millions of images you never saw? The person who used it?
*How to reason about it:* try assigning fault in three different scenarios and see whether your answer stays put — a school science project, a machine sorting recycling, and a machine screening job applications. Then notice which link in the chain *could have known* about the failure and *could have prevented it*. Responsibility tends to sit where knowledge and power overlap. Finally, ask the awkward one: if the answer is "nobody is responsible because nobody could read the model," is that an acceptable state of affairs, or is it a reason not to deploy the model at all?

**2. Should a model be allowed to say "I don't know"?**
Your fork model said "spoon, 74%." It could have been built to say "none of these look right." Almost no real product does this.
*How to reason about it:* work out who benefits from the shrug being hidden. A product that says "I'm not sure" 30% of the time feels broken, gets bad reviews, and gets replaced by a competitor that always answers — even if the competitor is wrong more often. That's a real market pressure pushing every product towards false confidence. Then flip it and find a setting where hiding uncertainty is clearly unacceptable: a medical scan, a car deciding whether that shape is a child. What is actually different about those cases — the cost of being wrong, or how quickly the mistake gets noticed?

**3. Your model learned from your house. Whose house did the big models learn from?**
Your classifier works on your spoons, your lighting, your hands. It has never seen anyone else's kitchen. The image models inside phones and search engines were trained on photos scraped from the internet.
*How to reason about it:* think about who posts a lot of photos online and who posts almost none — by country, by wealth, by age, by language. Then think about what "a spoon" or "a wedding" or "a house" looks like in the places that are over-represented versus under-represented. A model isn't biased because someone was cruel; it's biased because the photo collection had a shape, and nobody measured the shape. Then ask the hard practical question: **how would you even check?** You cannot look at 400 million photos. What could you measure instead? Module 9 gives you actual tools for this.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Holding the record button down for 20 seconds | It's fast and the sample count shoots up satisfyingly | You get one situation copied 200 times. Record 2-second bursts and move the object between every burst. Count distinct situations, not samples |
| Letting one class have far more photos than the others | You got bored, or one object was easier to photograph | Check the counts before training every single time. Keep the biggest within 20% of the smallest, or the model quietly abandons the small class |
| Shooting each class on its own surface | You photographed the spoon in the kitchen and the comb in the bathroom because that's where they live | Photograph every class on every background. Otherwise you've built a background classifier that happens to be right |
| Reading the top percentage and ignoring the rest | The big bar is the one that draws your eye | Always compute the margin (top minus second). 51/45/4 and 97/2/1 are both "correct" and one of them is nearly a coin toss |
| Believing a high confidence means a likely-correct answer | The word "confidence" strongly implies it | They're unrelated. The fork scored 74% and was wrong. Confidence measures *preference among your boxes*, nothing more |
| Expecting the model to handle objects you never trained on | You know what a fork is, so surely it does | It has three boxes and 100 points of belief. Add an `other` class filled with empty hands, backgrounds, and random objects |
| Adding more photos to fix a broken model | "More data" is the advice everyone repeats | Ask *what kind* of photos are missing first. Thirty more shots of the same scene fix nothing. One shot in a new place might fix everything |
| Testing only where you trained | It's convenient, and the scores are lovely | The single-background model scored 95% on its own table and failed two metres away. Always test somewhere the model has never been |
| Fixing a model by retraining without changing the data | The train button is right there and it feels productive | Retraining the same photos gives you nearly the same model. The cake analogy: you cannot fix the cake, only the ingredients |
| Naming classes `Class 1`, `Class 2`, `Class 3` | You'll definitely remember | You will not. Name them, and write what they mean in your data card from Module 2 |

---

## 🛠️ Mini-Project — The Three-Class Classifier

**Time: ~3 hours**

### 🎯 Goal

Build one genuinely good three-class image classifier — then attack it four times, in controlled ways, and produce an experiment table that explains every result. The model is not the deliverable. **The table is the deliverable.**

### 📋 Starter steps

**Step 1 — Choose three objects that make it hard (10 min).**
Rules:
- All three must be things you own and can hold.
- They must be **similar** in size and shape. Good sets: spoon / toothbrush / comb · pen / pencil / marker · apple / orange / lemon · sock / glove / face-cloth.
- Bad set: shoe / banana / laptop. Too easy, teaches you nothing.

Write down your three class names and the baseline (with three roughly equal classes, blind guessing = 33.3%).

**Step 2 — Collect 30+ photos per class, with the variety checklist open (45 min).**
Follow Hands-On Activity B. Work the checklist for every class, not just the first one.

Record your actual counts and check the balance:

```
   class A: ____   class B: ____   class C: ____
   (biggest − smallest) ÷ biggest = ____ %      target: under 20%
```

**Step 3 — Train the baseline model and save it (15 min).**
Train with default settings. Then **☰ → Download project as file**. Name it `baseline.tm`. You will reload this file three times, so don't skip it.

Test all three objects and fill in row 0:

| # | change | obj A top % | margin | obj B top % | margin | obj C top % | margin | correct /3 |
|---|---|---|---|---|---|---|---|---|
| 0 | baseline | | | | | | | |

**Step 4 — Experiment 1: fewer photos (20 min).**
Reduce every class to **5 photos**. Retrain. Test the same three objects **in the same place, with the same lighting, in the same order** — a controlled experiment changes exactly one thing. Fill in row 1.

Then reload `baseline.tm` to get your good model back.

**Step 5 — Experiment 2: one background only (25 min).**
Collect a fresh set of ~30 photos per class where **every photo is on the same surface with the same light**. Train. Test twice for each object: once on that surface, once **somewhere completely different**. Record both. Fill in row 2 with both readings.

Reload `baseline.tm`.

**Step 6 — Experiment 3: blurry photos (20 min).**
Collect ~30 per class while moving the object so the frames blur. Train. Test with the objects held **still and sharp**. Fill in row 3.

Reload `baseline.tm`.

**Step 7 — Experiment 4: the surprise object (10 min).**
Using the good baseline model, hold up a **fourth object** that has no class — a fork, a key, a rubber, your empty hand. Record all three confidences and the margin. Fill in row 4.

**Step 8 — Write the explanations (25 min).**
For every row, write **two sentences**: what happened to the numbers, and *why that data change caused it*. "It got worse" is not an explanation. "The margin fell from 86 to 41 because five photos covered only one angle, so the pattern the model found was thin" is.

**Step 9 — The prediction you make and then test (10 min).**
Write one sentence predicting a *fifth* failure your baseline model has, in the form from Hands-On Activity D. Then test it and record whether you were right.

### ✅ Success criteria checklist

- [ ] Three similar, hard-to-tell-apart classes, named properly (not `Class 1`)
- [ ] 30+ photos per class, with the balance percentage calculated and under 20%
- [ ] The variety checklist worked through for **all three** classes
- [ ] A saved `baseline.tm` file, reloaded between experiments
- [ ] A working baseline model that gets all three objects right
- [ ] A 5-row experiment table (baseline + 4 experiments) with **top score and margin** for every test
- [ ] Every confidence set checked to sum to 100%
- [ ] Two written sentences per row explaining **what** and **why**
- [ ] One before-the-fact prediction, tested, with an honest verdict

### 🚀 Level it up

**Add a fourth class called `other` and fight the fork.**

Collect 30–40 photos of "none of the above": your empty hand, the bare table, a fork, a pen, a wall, a phone, the floor. Deliberately include objects that are *similar* to your three classes — that's the hard part and the point.

Retrain with four classes. Then re-run Experiment 4 and compare:

| test | 3-class model | 4-class model |
|---|---|---|
| the fork | spoon 74% ✗ | ? |
| a real spoon | spoon 91% ✓ | ? |
| a real comb | comb 79% ✓ | ? |

Two things to watch for, and both are interesting. First: does the fork now land in `other`? Second — and this is the one people don't expect — **did your three real objects get worse?** Adding a big messy class often steals belief from the real classes and shrinks every margin. Write three sentences on whether the trade was worth it, and how you'd decide that if this were a real product rather than a homework task.

---

## 🔑 Key Takeaways

- **Training is a one-off process; the model is what it leaves behind.** You cannot argue with a model, edit it, or read it. You can only test it and rebuild it from better examples.
- **The model learns the easiest pattern that separates your classes** — which is very often the background, the lighting, or your hand, and almost never the thing you meant.
- **Confidence is a preference among the boxes you provided, not a chance of being right.** Always read the margin, not just the top number.
- **A model can only output a class you gave it.** Shown a fork, a three-class model says "spoon" at 74% and means it.
- **Class imbalance produces impressive accuracy and a blind spot.** 200/200/8 gives you a 98% model that never sees a comb.
- **Variety beats volume.** Forty photos across five backgrounds and three lights teach far more than four hundred photos of one scene.
- **A model that scores brilliantly where it was trained can fail two metres away** — which is exactly the problem Module 6 exists to catch.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Training** | The one-time process where a machine studies labelled examples and tunes itself | 120 photos, 50 epochs, 22 seconds |
| **Model** | The guessing machine that training produces | The file you download from Teachable Machine |
| **Epoch** | One complete pass through every training example | 50 epochs × 120 photos = 6,000 looks |
| **Class** | One of the named boxes a classifier can choose from | `spoon`, `toothbrush`, `comb` |
| **Class balance** | Whether each class has roughly the same number of examples | 41 / 40 / 39 is balanced; 200 / 200 / 8 is not |
| **Confidence score** | How strongly the model prefers each class; the scores always add to 100% | spoon 62%, toothbrush 21%, comb 17% |
| **Margin** | Top score minus second-highest score — how close the race was | 62 − 21 = 41 |
| **Variety** | How much your examples differ in the ways that shouldn't matter | 5 backgrounds, 3 lightings, 8 angles |
| **Baseline model** | The good version you compare every experiment against | 40 photos each, 91 / 88 / 79 |
| **Controlled experiment** | Changing exactly one thing and keeping everything else the same | Same objects, same room, same order — only the photo count changed |
| **Sabotage test** | Deliberately damaging your data to learn what the model depended on | Retraining with one background only |
| **`other` class** | An extra box for "none of the above," filled with random and background images | Empty hand, bare table, fork, wall |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

---

### Exercise 1 — Read the scores

**(a) cat 96%, dog 3%, rabbit 1%.** Sum = 100. ✓
(i) Prediction: **cat**. (ii) Margin: 96 − 3 = **93**. (iii) **Confident** — as clear as these ever get.
(iv) A margin this large usually means the classes are genuinely easy to separate *and* the training data had plenty of variety, so no competing class has any foothold. It can also mean the classes are too easy to be a real test.

**(b) cat 45%, dog 41%, rabbit 14%.** Sum = 100. ✓
(i) Prediction: **cat**. (ii) Margin: 45 − 41 = **4**. (iii) **Coin toss.**
(iv) Cat and dog are nearly tied, so whatever separates them in the training data is weak or missing — perhaps all photos are small, dark, or shot from behind. Rabbit at 14% shows the model *can* tell rabbits apart from the other two, so the problem is specific to the cat/dog pair, not to the model overall.

**(c) cat 34%, dog 33%, rabbit 33%.** Sum = 100. ✓
(i) Prediction: **cat**, technically. (ii) Margin: 34 − 33 = **1**. (iii) **A complete coin toss** — 1 in 3, which is exactly the baseline for three equal classes.
(iv) The model has learned nothing usable about this particular input. It's the "I have no idea" that the system isn't allowed to say, so it splits its belief almost evenly. This is the reading you'd most want a product to surface to a human.

**(d) cat 80%, dog 19%, rabbit 1% — and the truth was rabbit.** Sum = 100. ✓
(i) Prediction: **cat**. (ii) Margin: 80 − 19 = **61**. (iii) **Confident** — and wrong.
(iv) This is the fork from Step 9. Confidence describes *how strongly the model prefers cat over the other two boxes*, not *how likely cat is to be true*. If most rabbit training photos were white rabbits and this was a grey lop-eared one, the model has no rabbit-pattern that matches, so its belief flows to whichever other class the input resembles. The 80% is a true statement about the model's internal preference and tells you nothing whatsoever about reality.

---

### Exercise 2 — Class balance arithmetic

**(a) Total photos.**
```
   150 + 150 + 12 = 312
```

**(b) Accuracy if the model never says "willow."**
```
   correct  = 150 (oak) + 150 (maple) + 0 (willow) = 300

   accuracy = 300 ÷ 312

   long division:  312 × 0.9 = 280.8      remainder 300 − 280.8 = 19.2
                   19.2 ÷ 312 = 0.0615…
                   0.9 + 0.0615 = 0.9615…

   accuracy ≈ 0.9615 = 96.2%   (to one decimal place)
```

**(c) Accuracy on willow leaves specifically.**
```
   0 correct out of 12  =  0 ÷ 12  =  0.0  =  0.0%
```
Zero. The single headline number of 96.2% completely conceals it.

**(d) Two ways to fix the imbalance.**

*Fix 1 — level up.* Collect more willow photos until you have about 150. New counts: 150 / 150 / 150, total 450.
*Fix 2 — level down.* Delete oak and maple photos down to 12 each. New counts: 12 / 12 / 12, total 36.

**Which I'd choose and why:** level up, if willow leaves are available to photograph. Levelling down throws away 276 perfectly good photos, and 12 photos per class is far too few for any class — you'd end up with the fragile, low-margin model from Experiment 1 across the board.

But there's a real-world caveat worth naming. Sometimes you *cannot* collect more: the willow is the only one in the park, or the rare disease only has 12 recorded cases. In that situation neither fix is available, and the honest move is a middle path — trim oak and maple to something like 40 each, accept 40/40/12, and **report the willow accuracy separately and prominently** rather than hiding it inside one average.

---

### Exercise 3 — The variety audit

Model answer for a spoon / toothbrush / comb collection.

| class | backgrounds used | lighting types | angles | held vs alone | distinct situations |
|---|---|---|---|---|---|
| spoon | 4 (table, carpet, sink, bed) | 3 (window, ceiling, lamp) | 6 | both | 4 × 3 × 6 × 2 = **144** |
| toothbrush | 3 (sink, table, bed) | 2 (window, ceiling) | 5 | both | 3 × 2 × 5 × 2 = **60** |
| comb | 2 (sink, bed) | 2 (ceiling, lamp) | 3 | held only | 2 × 2 × 3 × 1 = **12** |

**Weakest class: `comb`** — 12 distinct situations against the spoon's 144, a **12-fold** gap. Two specific problems stand out beyond the raw number:

1. The comb was never photographed on the **kitchen table or carpet**, but the spoon was photographed there many times. So "kitchen table" is now evidence *for* spoon and *against* comb. This is a background leak with two victims.
2. The comb was never photographed **lying down alone**. Every comb photo contains a hand. The model may well have learned "hand + thin object = comb," which will misfire on any held object.

**Tomorrow's shot list (10 photos, not 6 — the gap is large):**
1. Comb on the kitchen table, window light, lying alone
2. Comb on the kitchen table, window light, held
3. Comb on the carpet, ceiling light, lying alone
4. Comb on the carpet, ceiling light, held
5. Comb on the bed, lamp, lying alone
6. Comb photographed from directly above, table
7. Comb photographed edge-on so the teeth are barely visible
8. Comb far away, small in frame, on the sink
9. Comb partly under a cloth, table
10. Comb held in the **other** hand, sink

Note that items 1, 3 and 5 all exist to break the "comb always comes with a hand" pattern, and items 1–4 exist to break the "kitchen table means spoon" pattern. **A good shot list targets a named suspicion, not just "more variety."**

---

### Exercise 4 — The fewer-photos experiment

Model results (yours will differ; the shape is what matters):

| photos per class | obj 1 top % | margin | obj 2 top % | margin | obj 3 top % | margin | # correct /3 |
|---|---|---|---|---|---|---|---|
| 5 | 62 | 41 | 44 | 14 | 41 (wrong) | 7 | **2 / 3** |
| 15 | 78 | 60 | 71 | 48 | 58 | 21 | **3 / 3** |
| 40 | 91 | 86 | 88 | 82 | 79 | 66 | **3 / 3** |

**The paragraph:**

The number correct improved from 2/3 to 3/3 between 5 and 15 photos, and then **stopped improving** — 15 and 40 both score a perfect 3/3. If "number correct" were my only measure, I would conclude that going from 15 to 40 photos was a complete waste of an hour.

The margins tell a totally different story. From 15 to 40, object 1's margin went 60 → 86, object 2's went 48 → 82, and object 3's went 21 → 66 — that last one **tripled**. The 15-photo model gets object 3 right by 21 points, which is close enough that a change of room, a change of light, or a slightly different angle could easily flip it. The 40-photo model gets it right by 66 points and has room to spare.

So: **"number correct" is a blunt instrument that stops responding long before the model stops improving.** It only has four possible values here (0, 1, 2, 3), so it cannot register anything finer. The margin is continuous and keeps reporting. The general lesson is that when a measure stops moving, that may mean the thing has stopped improving — or it may mean your measure has run out of resolution, and you need a better one. Module 6 is about exactly this problem at a bigger scale.

---

### Exercise 5 — Break it your own way

Model answer. **Sabotage chosen: my face appears in every photo of the `comb` class and in no others.**

**Prediction, written before running it:**
> *"The model will call any photo containing my face `comb`, even when I'm holding a spoon. Reason: my face is a large, high-contrast, extremely consistent pattern that appears in 100% of comb photos and 0% of the others, which makes it a far easier separator than the thin plastic teeth of an actual comb. Training takes the easy pattern."*

**Method:** 30 photos per class. All 30 comb photos taken as selfies with my face clearly in frame. All 30 spoon and toothbrush photos taken with the camera pointed at the object only, no face. Everything else — backgrounds, lighting, angles — kept the same across all three classes so that the face is the only difference.

**Results:**

| test | spoon % | toothbrush % | comb % | sum | predicted | true | ✓/✗ | margin |
|---|---|---|---|---|---|---|---|---|
| comb, my face in frame | 4 | 7 | **89** | 100 | comb | comb | ✓ | 82 |
| **spoon, my face in frame** | 18 | 11 | **71** | 100 | comb | spoon | ✗ | 53 |
| **comb, no face in frame** | 31 | **38** | 31 | 100 | toothbrush | comb | ✗ | 7 |
| empty hand, my face in frame | 9 | 14 | **77** | 100 | comb | *(none)* | ✗ | 63 |

**Verdict: the prediction was right, and worse than I expected.**

Row 2 is the failure I predicted: a spoon called `comb` at 71% purely because my face was in shot. Row 4 makes it starker — an **empty hand** plus my face scores 77% comb. The model isn't detecting combs at all.

Row 3 is the part I did **not** predict, and it's the more interesting result. When I showed a real comb with no face, the model didn't just get it wrong — it fell apart completely, 31/38/31, essentially the 33% baseline. It has learned almost nothing about the physical object. The face didn't merely *help*; it replaced comb-detection entirely, so removing it left nothing behind.

**What I'd conclude:** a shortcut feature doesn't sit alongside the real feature as a backup. It **prevents the real feature from ever being learned**, because once the easy pattern separates the classes perfectly there is no remaining error to push the model into learning the hard one. That reframes the wolves-and-snow story for me: the model didn't learn wolves *and also* snow. It learned snow *instead of* wolves.

---

### Exercise 6 — Write the confidence policy

**Setting:** a recycling-centre sorter, classes `plastic / paper / metal`. A wrong sort sends recyclable material to landfill. A stopped line costs money. A human check costs a few seconds of someone's attention.

**The policy:**

| band | top score | margin | action | why this boundary |
|---|---|---|---|---|
| **A — auto-sort** | ≥ 85% | ≥ 60 | sort automatically, no log | Both conditions must hold. 90/30/... has a good top score but a shaky margin and should not be in this band — that's exactly why the margin column exists |
| **B — second look** | ≥ 70% | ≥ 35 | send round the belt for a second photo at a different angle; if the second reading lands in band A, sort it | Most band-B failures come from a bad camera angle or an item lying awkwardly, and a second photo is nearly free. Only escalate if it fails twice |
| **C — human bin** | ≥ 50% | ≥ 15 | divert to a tray a person checks at the end of the hour | Genuinely ambiguous items (a paper cup with a plastic lining, foil-backed card). No amount of re-photographing fixes these, because the ambiguity is in the object, not the picture |
| **D — reject bin** | anything else, e.g. < 50% **or** margin < 15 | divert to a separate "unknown" tray, checked daily | Below this the model is essentially guessing. Note the **or** — 95/94/... would land here despite its high top score, which is correct behaviour |
| **E — stop the line** | 20 items in a row land in C or D | halt and alert a supervisor | One confusing item is normal. Twenty in a row means something systematic broke — the camera moved, a light failed, or a new packaging type arrived. This is the band that catches the failure the other four cannot |

**Where I drew the boundaries and why:**

The 85% / 60-margin line for auto-sorting comes from the Step 5 baseline readings in this module: a healthy model on an object it knows well produced margins in the 66–86 range. Setting the bar at 60 means "behave like a model that knows what it's looking at." I deliberately required both conditions rather than top score alone, because Experiment 2 showed a model can hit 95% for the wrong reason.

The 50% floor exists because with three classes, 33% is pure chance. Anything under 50% is barely above a shrug, and the extra cost of a human tray is tiny compared with contaminating a whole batch.

Band E is the one I'd argue hardest for. Every other band judges one item at a time, and every failure mode in this module — a changed background, a changed light, a new object with no class — shows up as *many* items degrading at once. A per-item policy will happily divert a thousand items to the reject tray and never notice the camera has been knocked sideways.

**Who should be allowed to change these numbers?**

Not the engineer alone. The engineer understands what the numbers mean but does not carry the cost of getting them wrong, and there's a standing temptation to widen band A because a machine that sorts more items looks more successful.

Not the centre manager alone either. They carry the cost of a slow line very directly and the cost of landfill contamination very indirectly — that asymmetry pushes the thresholds down over time, one small adjustment at a time, with each individual change looking reasonable.

My answer: **the engineer and the manager should be able to propose changes, but every change should be recorded, dated, and published**, along with the landfill contamination rate measured before and after. And the "stop the line" rule in band E should require more than one person to disable it. The general principle I'd take from this: the person who bears the cost of a mistake and the person who benefits from taking the risk should rarely be the same person, and when the two are different people the numbers need to be visible to both.

---

</details>

---

[⬅ Previous](module-04-features-and-labels.md) · [Level 1 Home](README.md) · [Next ➡](module-06-train-test-trust.md)

*Next up: in Experiment 2 you built a model that scored 95% on its own table and failed two metres away — and if you'd only tested where you trained, you'd have called it your best model yet. Module 6 gives that trap its name, and gives you the one simple habit that catches it every time: hide some examples before you start.*

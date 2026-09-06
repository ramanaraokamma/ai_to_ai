# 🎪 Level 1 Capstone — The AI Fair Booth

**Level 1 · Capstone · ~6 hours · Prereqs: all nine Level 1 modules, especially [M2](module-02-data-is-everywhere.md) (data cards), [M5](module-05-learning-from-examples.md) (training), [M6](module-06-train-test-trust.md) (held-out testing), [M8](module-08-how-computers-read-and-chat.md) (Scratch), [M9](module-09-fair-private-honest-ai.md) (bias audits)**

[⬅ Module 9](module-09-fair-private-honest-ai.md) · [Level 1 Home](README.md) · [Assessment](assessment.md) · [Glossary](glossary.md)

---

## 🎯 What You'll Be Able To Do

By the end of this capstone:

1. **You will be able to** take a real annoyance in your own home and turn it into a classification task with named classes, a collection plan, and a reason it is worth solving.
2. **You will be able to** ship a complete AI artefact — model, app, data card, test sheet, bias report — where every claim you make is backed by a number you personally measured.
3. **You will be able to** wire a trained model into a program that *does something* when the prediction changes, instead of just printing a percentage.
4. **You will be able to** stand in front of an adult for five minutes, explain how your system works, and answer "but how does it actually know?" without using the word **magic**.
5. **You will be able to** tell someone, unprompted, what your own system is bad at — and show them the arithmetic that proves it.

---

## 🪝 The Brief

Your school is running an **AI Fair** in two weeks. Every stall gets one table, one poster board, and one laptop. Adults will wander past, stop for four minutes, poke your thing, and ask questions.

Most stalls will have a demo that works once. Somebody will train a model to tell apples from bananas, hold up an apple, get "APPLE 99%", and everyone will clap. Then a parent will hold up their car keys, the model will say "BANANA 91%", and the student will say *"ah, it's not trained for that"* and move on.

**You are going to run the one stall that is honest.**

Your booth will do four things no other stall does:

```
   ┌───────────────────────────────────────────────────────────────────┐
   │                                                                   │
   │   1.  It solves a problem that actually exists in your house.     │
   │       Not apples vs bananas. Something you were annoyed by        │
   │       last week.                                                  │
   │                                                                   │
   │   2.  It shows a printed accuracy number measured on photos       │
   │       the model has NEVER seen — and it shows the fraction,       │
   │       so people can see how many photos it was.                   │
   │                                                                   │
   │   3.  It has a printed sign saying exactly who and what this      │
   │       model FAILS on, with the gap in percentage points.          │
   │                                                                   │
   │   4.  You invite visitors to break it. On purpose. And you        │
   │       write down what worked.                                     │
   │                                                                   │
   └───────────────────────────────────────────────────────────────────┘
```

### Why this matters

Every skill in Level 1 was a piece of one thing. This is the thing.

| Module | The piece it gave you | Where it shows up in the booth |
|---|---|---|
| 1 | Rules vs learned-from-examples | Your demo script: "nobody wrote a rule for this" |
| 2 | Rows, columns, provenance, data cards | The printed data card on the table |
| 3 | Why rules explode | The 30-second "why not just write if-then?" answer |
| 4 | Features, labels, leaky features | Choosing classes that aren't giveaways |
| 5 | Training, class balance, confidence | The model itself |
| 6 | Hold out, accuracy, confusion matrix | The test sheet |
| 7 | Pixels, resolution, backgrounds | Explaining *why* it fails on the dark shelf |
| 8 | Scratch, lookup tables, next-word | The app that reacts |
| 9 | Bias, privacy, over-trust | The bias report and the "do not use for" sign |

And here is the professional truth underneath it. In a real company, the model is maybe 20% of the work. The other 80% is the data card, the honest test, the bias report, and being able to explain the thing to someone who controls the budget. **You are building the 80% that nobody teaches.**

---

## 🏠 Choosing Your Problem

Spend real thought here. A bad problem choice cannot be rescued by good work later.

### The three tests a good capstone problem passes

```
   TEST 1 — THE ANNOYANCE TEST
   Can you name a specific moment in the last month when this
   actually bothered someone in your house?
        ✅ "Dad put the milk carton in the wrong bin again on Sunday."
        ❌ "It would be cool to detect cats."

   TEST 2 — THE 3-TO-4 CLASSES TEST
   Does it split cleanly into 3 or 4 named classes that a human
   can also tell apart, but has to LOOK to do it?
        ✅ recycling / compost / landfill
        ❌ happy / sad  (you can't label these reliably yourself)

   TEST 3 — THE 40-PHOTOS TEST
   Can you honestly collect 40+ genuinely different photos of each
   class in one afternoon, in your own house?
        ✅ turmeric / chilli / coriander jars — 40 angles each, easy
        ❌ every breed of dog on your street — you don't have access
```

### Candidate problems that work well

| Problem | Classes | Why it's good | Watch out for |
|---|---|---|---|
| **Which bin?** | recycling · compost · landfill · `other` | Real, useful, genuinely hard, everyone at the fair has an opinion | Items get dirty and squashed — that's realistic, include it |
| **Which spice jar?** | turmeric · chilli · coriander · `other` | Identical jars, different contents — forces the model to use real features | Lids on = impossible. Decide and document. |
| **Is the door bolted?** | locked · unlocked · `other` | Two classes but genuinely useful; great safety-stakes discussion | Only 2 classes → baseline is 50%, say so |
| **Whose water bottle?** | 3 family members' bottles + `other` | Personal, funny, and a superb privacy discussion | Ask each person's permission — that goes in the data card |
| **Did I pack it?** | keys · wallet · glasses · `other` | Reacting app writes itself ("you forgot your keys") | Objects are small — check resolution (Module 7) |
| **Which charger?** | phone · laptop · headphones · `other` | Cables are hard for models, which makes the failure analysis rich | Tangled vs coiled — collect both |
| **Is the plant thirsty?** | fine · droopy · `other` | Slow-changing, so you must collect over days | Labelling is subjective — write your labelling rule down |

### Problems to avoid, and why

| Don't do | Why not |
|---|---|
| Anything classifying **people** — mood, age, gender, "is this person trustworthy" | Module 9 explains this properly. Short version: you cannot collect a fair sample, the labels are not real, and someone gets hurt. This is a hard rule, not a preference. |
| Anything needing **medical** judgement (is this rash bad?) | A wrong answer causes real harm and you cannot test it honestly. |
| Classes you can't reliably label yourself | If *you* can't be sure of the right answer, the label column is noise and the test sheet means nothing. |
| Fewer than 3 classes when you have a choice | Two classes gives a 50% baseline, and 50%-vs-baseline conversations are boring. Three is the sweet spot. |
| Something in someone else's house/school without asking | Provenance and permission, Module 2. Ask first, write it in the card. |

> 🔑 **The `other` class is mandatory.** Module 5's "level it up" showed why: without it, a fork gets classified as a spoon at 74% confidence. At a fair, strangers will hold up their car keys. Your model must be able to say "none of these."

---

## 📋 Requirements

### 🟥 Must-have — without all of these, the booth is not done

| # | Requirement | Evidence |
|:--:|---|---|
| M1 | A **classification task** from your own home, with **3+ named classes plus an `other` class** | Written problem statement, one paragraph |
| M2 | **40+ training photos per class**, balanced within 20% | Photo counts written down per class |
| M3 | **20% of photos held out before training** and never trained on | The held-out set, kept in a separate folder |
| M4 | A **trained Teachable Machine model** that beats its own baseline | The `.tm` project file, saved |
| M5 | A **printed data card** covering what/how many/where from/permission/limits | One page, on the table |
| M6 | A **test sheet**: every held-out photo scored by hand, with accuracy as **fraction → decimal → percentage** | The filled sheet, on the table |
| M7 | A **confusion matrix** built by hand from the test sheet | Drawn on the sheet or the poster |
| M8 | A **Scratch app** that changes what it does depending on the prediction — at least 4 different behaviours | The running project |
| M9 | A **bias report** naming one input group the model handles badly, with an **accuracy gap in percentage points** | Half a page, on the poster |
| M10 | A **"DO NOT USE THIS FOR…"** sign in the biggest text on the booth | On the poster |
| M11 | A **5-minute demo** delivered to an adult, with **zero** uses of the word "magic" | A signature or a tick from your listener |

### 🟨 Should-have — this is what separates a good booth from a passing one

| # | Requirement | Why it lifts the booth |
|:--:|---|---|
| S1 | A **prediction written before the bias test** of which group will fail, plus how it turned out | Shows you reasoned rather than fished |
| S2 | A **confidence threshold** in the Scratch app: below some % it says "not sure" instead of guessing | This is the single most grown-up thing in the whole project |
| S3 | A **visitor break-it log** — a sheet where you record every input a stranger used to fool it | Turns your audience into your test set |
| S4 | The **baseline accuracy** printed next to your accuracy (25% for four equal classes) | Module 4's lesson: a number without a baseline means nothing |
| S5 | A **per-class accuracy** table, not just one overall number | Module 6's lesson: one number hides the problem |
| S6 | A **priced fix**: "N more photos of X, then retest" with the arithmetic shown | Module 9's lesson: "collect more data" is not a plan |

### 🟩 Could-have — pick at most one or two, only after everything above is done

| # | Idea |
|:--:|---|
| C1 | **Before/after**: actually collect the fix photos, retrain, rerun the *identical* test batches, publish both columns |
| C2 | A **second model** trained on half the data, shown side by side to demonstrate the effect of data quantity |
| C3 | A **Scratch chatbot** (Module 8 style) that answers visitor questions about your model from a lookup table |
| C4 | An **audio or pose** Teachable Machine model as a second input (clap to reset the app) |
| C5 | A **QR code** on the poster linking to your data card |
| C6 | An **auditor swap**: a friend audits your model without seeing your training data, and their gap goes on the poster next to yours |

> ⚠️ **The trap.** Every year somebody spends four hours on the Scratch animation and twenty minutes on the test sheet. The rubric below weights honesty higher than polish, on purpose. Finish all eleven Must-haves before you make a single sprite dance.

---

## 🗺️ Milestone Plan

Seven milestones, about **6 hours** of work. The order matters — you cannot hold out photos after training, and you cannot write a bias report before you have a model.

```
   ┌────┬────────────────────────────────┬────────┬─────────────────────────┐
   │ #  │  MILESTONE                     │  TIME  │  YOU END UP HOLDING     │
   ├────┼────────────────────────────────┼────────┼─────────────────────────┤
   │ 1  │  Pick the problem, name the    │ 20 min │  A one-paragraph brief  │
   │    │  classes, write the brief      │        │  + 4 class names        │
   ├────┼────────────────────────────────┼────────┼─────────────────────────┤
   │ 2  │  Collect + SPLIT the photos    │ 60 min │  train/ and heldout/    │
   │    │  (split BEFORE training!)      │        │  folders, counted       │
   ├────┼────────────────────────────────┼────────┼─────────────────────────┤
   │ 3  │  Train the model, save it      │ 45 min │  booth-v1.tm            │
   ├────┼────────────────────────────────┼────────┼─────────────────────────┤
   │ 4  │  Score every held-out photo    │ 40 min │  test sheet + accuracy  │
   │    │  by hand → accuracy + matrix   │        │  3 ways + confusion mtx │
   ├────┼────────────────────────────────┼────────┼─────────────────────────┤
   │ 5  │  ⚠️ HARDEST: build the Scratch │ 75 min │  A running app that     │
   │    │  app that reacts to predictions│        │  does 4 things          │
   ├────┼────────────────────────────────┼────────┼─────────────────────────┤
   │ 6  │  Bias test + data card +       │ 45 min │  Gap in pct points,     │
   │    │  the "do not use for" sign     │        │  printed card, sign     │
   ├────┼────────────────────────────────┼────────┼─────────────────────────┤
   │ 7  │  Build the booth + rehearse    │ 45 min │  A 5-minute demo you    │
   │    │  the 5-minute demo             │        │  have said out loud 3×  │
   └────┴────────────────────────────────┴────────┴─────────────────────────┘
                                          ─────────
                                          330 min ≈ 5.5 h  (+ 30 min slack)
```

---

### ☐ Milestone 1 — The brief (20 min)

- [ ] Run all three tests (Annoyance / 3-to-4 Classes / 40-Photos) on your idea, in writing
- [ ] Name your classes. Real names — `plastic_recycling`, not `Class 1`
- [ ] Add an `other` class
- [ ] Write your **baseline**: with 4 roughly equal classes, blind guessing = 1/4 = **25%**
- [ ] Write one paragraph: *what annoys someone, who it helps, what the model must output*

**Template — copy this into `00-brief.txt`:**

```
PROBLEM
   In my house, ____________________ happens about ______ times a week.
   The person it annoys most is ____________________.

WHAT THE MODEL DOES
   Input:   a photo from the laptop webcam of ____________________
   Output:  one of these labels:
              1. ______________
              2. ______________
              3. ______________
              4. other
   Baseline (blind guessing, 4 equal classes) = 1/4 = 25%
   I will call it useful if it beats ______%    ← pick a number NOW, before you train

WHAT HAPPENS WHEN IT'S RIGHT
   ____________________________________________

WHAT HAPPENS WHEN IT'S WRONG
   Worst case: ________________________________
   Who gets hurt: _____________________________
```

> That "I will call it useful if it beats ___%" line is not decoration. Writing your success bar *before* you see the result is how you stop yourself moving the goalposts later. Real engineers call this pre-registration.

---

### ☐ Milestone 2 — Collect and split (60 min)

- [ ] Photograph **50+ per class** (you'll hold out 20%, leaving 40+ for training)
- [ ] Work the Module 5 **variety checklist** for *every* class, not just the first
- [ ] While collecting, keep a tally of conditions — you need these counts for the bias report
- [ ] **SPLIT BEFORE TRAINING.** Move 20% of each class into `heldout/` and do not open it again
- [ ] Take the held-out photos on a **different day or a different surface** where you can — that's a harder, more honest test
- [ ] Write your counts down

**The variety checklist, per class:**

```
   □ 3+ different backgrounds        □ 2+ people holding it (or held vs on a table)
   □ 3+ lighting conditions          □ close-up AND far away
   □ 6+ angles / rotations           □ at least 5 slightly "wrong" ones
                                       (partly out of frame, blurry, half-hidden)
```

**The counting table — copy this into `01-counts.txt`:**

```
   class              total   heldout(20%)   train    daylight  lamp  dark
   ─────────────────  ─────   ────────────   ─────    ────────  ────  ────
   ________________     50          10         40         __     __    __
   ________________     50          10         40         __     __    __
   ________________     50          10         40         __     __    __
   other                50          10         40         __     __    __
   ─────────────────  ─────   ────────────   ─────
   TOTAL               200          40        160

   balance check:  (biggest − smallest) ÷ biggest = ______ %     target: under 20%
```

> ⚠️ **The one mistake you cannot undo.** If you train first and split after, your test set is worthless and there is no fix except re-collecting. Physically move the files into a different folder *before* you open Teachable Machine. Module 6 gave you an envelope for a reason.

---

### ☐ Milestone 3 — Train and save (45 min)

- [ ] Teachable Machine → **Image Project** → **Standard image model**
- [ ] Create your 4 classes and **rename them** properly
- [ ] Upload **only** the `train/` folders (drag the folder onto the class — never the `heldout/` folder)
- [ ] Check the sample count under each class name matches your table
- [ ] Train with default settings (50 epochs). Watch the counter.
- [ ] **☰ → Download project as file** → save as `booth-v1.tm` **before you do anything else**
- [ ] Live-check: hold up one object of each class. Note the top class and the **margin** (top % − second %)
- [ ] Hold up something with no class. Does `other` win? Write down what happened.

```
   ┌─────────────────────────────────────────────────────────────────┐
   │  ⛔  STOP. Do not go to Milestone 4 until booth-v1.tm exists     │
   │      on your actual computer. Milestones 5 and 6 both reload    │
   │      it, and Teachable Machine has no autosave. Every year      │
   │      somebody closes the tab. Don't be that person.             │
   └─────────────────────────────────────────────────────────────────┘
```

---

### ☐ Milestone 4 — The honest test (40 min)

- [ ] Open `heldout/` for the **first time since Milestone 2**
- [ ] Feed each held-out photo to the model (drag onto the Preview panel, or hold the printed photo to the webcam)
- [ ] Record **every** one on paper *as you go* — true label, prediction, top confidence, ✓/✗
- [ ] Do not skip, retake, or "give it another go". A photo gets one attempt.
- [ ] Compute accuracy as **fraction → decimal → percentage**, showing the division
- [ ] Compute **per-class accuracy**
- [ ] Build the **confusion matrix** by hand
- [ ] Write one sentence: which class is it worst at, and what does it confuse that class with?

**The scoring sheet — copy this into `02-testsheet.txt`:**

```
   #   photo file          TRUE label      PREDICTED     top %   ✓/✗
   ──  ─────────────────   ───────────     ──────────    ─────   ───
    1  heldout/rec/01.jpg  recycling       recycling      94      ✓
    2  heldout/rec/02.jpg  recycling       landfill       61      ✗
   ...
   40

   OVERALL   correct = ____ / 40  =  ____  =  ____%
   BASELINE  25%
   GAIN      ____ percentage points above baseline
```

---

### ☐ Milestone 5 — ⚠️ The Scratch app (75 min) — *hardest milestone*

- [ ] Decide your route: **A** (real model in Scratch) or **B** (no-upload bridge). Both are legitimate.
- [ ] Build a project where **each of the 4 classes triggers a different behaviour**
- [ ] Add a **confidence threshold** so low-confidence predictions say "not sure" (Should-have S2)
- [ ] Test all 4 classes plus one unknown object
- [ ] Save two ways: **File → Save to your computer** (`.sb3`) *and* to your Scratch account

Full worked solution below — see **🔍 Worked Solution: Milestone 5**.

---

### ☐ Milestone 6 — Bias report, data card, warning sign (45 min)

- [ ] **Write your prediction first**: which condition will be worst, and the training count that justifies it
- [ ] Collect **3–4 test batches of 8–12 photos**: control · new lighting · new hands/holder · new background
- [ ] Score every photo on paper as you go
- [ ] Per-condition accuracy → fraction, decimal, percentage
- [ ] **Accuracy gap** = best condition % − worst condition %, in **percentage points**
- [ ] Note the **highest confidence the model gave while being wrong**. Put it on the poster, large.
- [ ] Write the data card (template in the scaffold below)
- [ ] Write the **DO NOT USE THIS FOR** sign — biggest text on the booth

---

### ☐ Milestone 7 — Build the booth and rehearse (45 min)

- [ ] Lay out the table: laptop, poster, printed data card, test sheet, break-it log, pens
- [ ] Write your **5-minute script** (structure given in *Show Your Work* below)
- [ ] Say it **out loud three times**. Time yourself. Out loud — reading it silently does not count.
- [ ] Get someone to ask you the six hard questions from the question bank
- [ ] Count your "magic"s. Target: zero.
- [ ] Prepare one deliberate failure you can demo on request

---

## 📁 Starter Scaffold

Make this folder on your computer before Milestone 2. Everything lands somewhere.

```
   ai-fair-booth/
   │
   ├── 00-brief.txt                    ← Milestone 1 template, filled in
   ├── 01-counts.txt                   ← photo counts + condition tallies
   ├── 02-testsheet.txt                ← 40 rows, scored by hand
   ├── 03-confusion-matrix.txt         ← the 4×4 grid
   ├── 04-bias-report.txt              ← 4 conditions, gap in pct points
   ├── 05-data-card.txt                ← the printed one-pager
   ├── 06-breakit-log.txt              ← starts empty, visitors fill it
   ├── 07-demo-script.txt              ← what you say, in order
   │
   ├── model/
   │   ├── booth-v1.tm                 ← Teachable Machine project file
   │   ├── booth-app.sb3               ← Scratch project backup
   │   └── model-url.txt               ← the shared model link, if Route A
   │
   └── photos/
       ├── train/
       │   ├── recycling/      (40 photos)
       │   ├── compost/        (40 photos)
       │   ├── landfill/       (40 photos)
       │   └── other/          (40 photos)
       │
       ├── heldout/            ⛔ DO NOT OPEN UNTIL MILESTONE 4
       │   ├── recycling/      (10 photos)
       │   ├── compost/        (10 photos)
       │   ├── landfill/       (10 photos)
       │   └── other/          (10 photos)
       │
       └── biastest/           ⛔ collected in Milestone 6, after training
           ├── control/        (10 photos)
           ├── new-lighting/   (10 photos)
           ├── new-hands/      (10 photos)
           └── new-background/ (10 photos)
```

> 🍕 **Analogy — the three envelopes.** `train/` is the homework you study. `heldout/` is the sealed exam paper. `biastest/` is the pop quiz someone else writes, in a room you didn't expect. Three separate piles, three separate purposes. Mixing them is the only way to cheat yourself.

### Starter file — `05-data-card.txt`

```
   ══════════════════════════════════════════════════════════════════
   DATA CARD  ·  ______________________ classifier  ·  v1
   ══════════════════════════════════════════════════════════════════

   1. WHAT IT IS
      Photos of ____________________ taken in my home, labelled
      with one of 4 classes: ______, ______, ______, other.

   2. HOW MUCH
      200 photos total.  50 per class.
      160 used for training, 40 held out and never trained on.

   3. WHO COLLECTED IT, WHEN, HOW
      Collected by ____________ between ____ and ____ using a
      ____________ webcam / phone camera, at ______ × ______ pixels.

   4. PERMISSION
      Objects belong to: ______________________.
      I asked ____________ on ____________ and they said yes.
      No faces appear in any photo.  /  Faces appear in ___ photos and
      those people gave permission.

   5. WHAT'S IN IT — the honest condition counts
      daylight ____ · lamplight ____ · dark ____
      held in a hand ____ · resting on a surface ____
      backgrounds used: ______________________________
      photographers: ______________________________

   6. WHAT'S NOT IN IT   ← the most important box on this card
      ______________________________________________________
      ______________________________________________________

   7. KNOWN LIMITS
      Measured accuracy on 40 held-out photos: ____/40 = ____%
      Baseline: 25%
      Worst condition: ______________ at ____%  (gap: ____ points)

   8. DO NOT USE THIS FOR
      ______________________________________________________
   ══════════════════════════════════════════════════════════════════
```

### Starter file — `06-breakit-log.txt`

```
   VISITOR BREAK-IT LOG   —   "can you fool it?"

   #   what they showed it        model said     conf   fooled?   my guess why
   ──  ────────────────────────   ───────────    ────   ───────   ─────────────
    1  a car key                  other          71     no        other class worked
    2  a squashed can             landfill       58     YES       all my cans were round
    3
   ...

   END OF FAIR:  ____ attempts, ____ successful fools.
   The single most useful thing a visitor found: ______________________
```

---

## 🔍 Worked Solution: Milestone 5 — the Scratch app

This is the milestone people get stuck on, so here is a complete, working answer. Read the whole section before you start clicking.

### The problem

Teachable Machine gives you a model in a browser tab. Scratch is a different browser tab. **They do not talk to each other by default.** You need a bridge. There are two, and both are honest choices.

```
   ┌──────────────────────────────────────────────────────────────────────┐
   │                                                                      │
   │  ROUTE A — TM2Scratch  (the model runs inside Scratch)               │
   │                                                                      │
   │    Teachable Machine ──[Upload my model]──► a public link on         │
   │                                             Google's servers         │
   │                                                    │                 │
   │                                                    ▼                 │
   │    Stretch3 (a modified Scratch) ──[paste link]──► live predictions  │
   │                                                    inside Scratch    │
   │                                                                      │
   │    ✅ fully automatic, feels like a real product                     │
   │    ⚠️ your model (not your photos) goes onto Google's servers with   │
   │       a public link. This is a real privacy decision — Module 9.     │
   │                                                                      │
   ├──────────────────────────────────────────────────────────────────────┤
   │                                                                      │
   │  ROUTE B — the key bridge  (nothing leaves your laptop)              │
   │                                                                      │
   │    Teachable Machine tab ──► YOU read the prediction ──► press 1/2/3 │
   │                              (or a helper does)         in Scratch   │
   │                                                                      │
   │    ✅ zero upload, works offline, sets up in 5 minutes               │
   │    ⚠️ a human is inside the loop, and you must SAY SO at the fair    │
   │                                                                      │
   └──────────────────────────────────────────────────────────────────────┘
```

**Which should you pick?** Either. Route A is the fuller experience. Route B is the more private one, and admitting "there's a human in this loop" out loud at your booth is worth more than a slicker demo. Whichever you choose, **write the choice and the reason in your data card.** That sentence is worth more marks than the animation.

---

### Route A — step by step

**Step A1 — Publish the model.** In Teachable Machine, click **Export Model** → the **Tensorflow.js** tab → **Upload my model**. Wait. You get a link like:

```
   https://teachablemachine.withgoogle.com/models/AbCdEf123/
```

Copy it into `model/model-url.txt`. Keep the trailing slash.

**Step A2 — Open a Scratch that has AI blocks.** Plain scratch.mit.edu does not have a Teachable Machine extension. Use **Stretch3** (`stretch3.github.io`), a modified Scratch that adds one. Click the **Add Extension** button (bottom-left), and choose the **TM2Scratch** (Teachable Machine) extension.

> ⚠️ Block names differ slightly between versions of this extension. Match blocks by **what they do and what shape they are**, not by exact wording. The four you need are: *set the model URL*, *turn the video on*, *a reporter that gives you the current label*, and *a hat block that fires when a label is detected*.

**Step A3 — Build the script.** Here it is in Scratch block notation, line by line.

```
when green flag clicked

    ┌─── SETUP: point the extension at YOUR model ───┐

    set image classification model URL
        [https://teachablemachine.withgoogle.com/models/AbCdEf123/]
                                    ↑ your link from Step A1

    toggle video [on v]                  · turn the webcam on
    set video transparency to (0)        · 0 = fully visible, easier to aim

    set [threshold v] to (70)            · my confidence cut-off, in %
    set [last v] to [none]               · remember what we said last time,
                                           so we don't repeat ourselves
    set [count v] to (0)                 · how many items we've sorted

    say [Show me an item.] for (2) seconds

    ┌─── THE LOOP: check the prediction about twice a second ───┐

    forever

        wait (0.5) seconds

        ┌── has the label CHANGED since last time? ──┐
        if <not <(image label) = (last)>> then

            set [last v] to (image label)

            ┌── the 4 behaviours, one per class ──┐

            if <(image label) = [recycling]> then
                switch backdrop to [blue v]
                say [RECYCLING — blue bin, please.] for (3) seconds
                play sound [Bell v]
                change [count v] by (1)
            end

            if <(image label) = [compost]> then
                switch backdrop to [green v]
                say [COMPOST — green bin.] for (3) seconds
                play sound [Bird v]
                change [count v] by (1)
            end

            if <(image label) = [landfill]> then
                switch backdrop to [grey v]
                say [LANDFILL — black bin. Could you reuse it?] for (3) seconds
                play sound [Low Boop v]
                change [count v] by (1)
            end

            if <(image label) = [other]> then
                switch backdrop to [white v]
                say [I do not recognise that. I only know 3 kinds of rubbish.]
                    for (3) seconds
            end

        end
    end
```

**Step A4 — Add the confidence threshold (Should-have S2).** This is the grown-up bit. A model that says "not sure" is more trustworthy than one that always answers.

The extension gives you a confidence reporter (often called *image label confidence* or similar). Wrap the whole decision in it:

```
        if <(image label confidence) > (threshold)> then

            ... the four IF blocks from Step A3 go in here ...

        else
            switch backdrop to [white v]
            say (join [Not sure — only ] (join (image label confidence) [% confident.]))
                for (3) seconds
        end
```

Now hold up something ambiguous — a squashed carton, half a banana peel in a plastic wrapper — and watch it refuse. **Demo that at the fair.** Visitors remember the machine that admitted it didn't know.

---

### Route B — the no-upload bridge, step by step

Nothing leaves your laptop. Takes five minutes.

**Step B1.** Open your Teachable Machine project (`booth-v1.tm`) in one browser window, webcam preview running.

**Step B2.** Open scratch.mit.edu in a second window, side by side.

**Step B3.** Build this. Every block is in plain Scratch — no extensions.

```
when green flag clicked

    set [threshold v] to (70)
    set [count v] to (0)
    set [conf v] to (0)
    say [Show me an item. Then tell me the number and the confidence.]
        for (3) seconds

    forever

        ┌── read the operator's eyes ──┐
        ask [Prediction? 1=recycling 2=compost 3=landfill 4=other] and wait
        set [choice v] to (answer)

        ask [Confidence %?] and wait
        set [conf v] to (answer)

        ┌── the threshold check, exactly as in Route A ──┐
        if <(conf) < (threshold)> then
            switch backdrop to [white v]
            say (join [Not sure — only ] (join (conf) [%.])) for (3) seconds

        else

            if <(choice) = [1]> then
                switch backdrop to [blue v]
                say [RECYCLING — blue bin, please.] for (3) seconds
                play sound [Bell v]
                change [count v] by (1)
            end

            if <(choice) = [2]> then
                switch backdrop to [green v]
                say [COMPOST — green bin.] for (3) seconds
                play sound [Bird v]
                change [count v] by (1)
            end

            if <(choice) = [3]> then
                switch backdrop to [grey v]
                say [LANDFILL — black bin. Could you reuse it?] for (3) seconds
                play sound [Low Boop v]
                change [count v] by (1)
            end

            if <(choice) = [4]> then
                switch backdrop to [white v]
                say [I do not recognise that.] for (3) seconds
            end

        end
    end
```

**Step B4 — the honesty sign.** If you use Route B, this goes on your booth in ordinary-sized text:

```
   ┌────────────────────────────────────────────────────────────┐
   │  HOW THIS BOOTH WORKS: the model runs on this laptop and   │
   │  makes the prediction. I type the prediction into Scratch  │
   │  because I chose not to upload my model to the internet.   │
   │  The guess is the machine's. The typing is mine.           │
   └────────────────────────────────────────────────────────────┘
```

That sign will earn you more respect from a knowledgeable adult than any animation.

---

### Debugging Milestone 5 — the six things that go wrong

| Symptom | Cause | Fix |
|---|---|---|
| The label reporter is always empty | The model URL is wrong, or the video is off | Paste the URL into a browser first — it should show a page of JSON-looking text, not a 404. Check the trailing `/`. Then check `toggle video [on]` actually ran. |
| It says the same thing 40 times in 5 seconds | No "has the label changed?" guard | Add the `if <not <(image label) = (last)>>` wrapper from Step A3. This is the single most common bug. |
| Nothing ever matches my `if` blocks | Class name mismatch — `Recycling` ≠ `recycling` | Scratch's `=` ignores case for letters, but a stray space does not. Retype the class name into the `if` block by copying it from Teachable Machine exactly. |
| The stage is frozen / very slow | The `forever` loop has no `wait` | Put `wait (0.5) seconds` at the top of the loop. Classifying 30 times a second helps nobody. |
| Threshold check never triggers | Comparing a percentage to a decimal | Decide once: is your confidence `0.85` or `85`? Whichever the extension gives you, set `threshold` to match. Print the raw value with a `say` block to check. |
| Works at home, fails at the fair | Different lighting and background — exactly Module 6's overfitting | This is the lesson, not a bug. Collect a handful of photos at the fair table during setup and say so in your demo. |

---

## ⚠️ Common Capstone Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Training first, splitting after | Teachable Machine makes uploading everything feel natural, and holding photos back feels wasteful | Move files into `heldout/` **before** you open Teachable Machine. There is no way to un-see data. |
| Skipping the `other` class | Your own testing only ever uses the three real objects | Strangers will hold up car keys. 40 photos of "none of the above" — bare table, hands, random objects — is 20 minutes well spent. |
| Reporting one accuracy number | It's the easiest number to compute and the nicest to say | Per-class accuracy plus a confusion matrix. Module 6: one number hides the problem. |
| Retaking a held-out photo because "the lighting was off" | It feels like fairness; it is actually cheating | One photo, one attempt, recorded as it happened. If lighting matters, that *is* the finding — put it in the bias report. |
| Fishing for a bias result instead of predicting one | Testing 12 conditions and reporting the worst finds noise, not bias | Predict **one** condition in writing before you test. Report it whether or not you were right. |
| Four hours on the Scratch sprites, twenty minutes on the test sheet | Animation gives instant feedback; arithmetic doesn't | The rubric weights honesty above polish. Must-haves first, always. |
| Saying "it's 95% accurate" with no fraction | Percentages sound official | Say "19 out of 20." Then people know it was 20 photos, and they can judge for themselves. |
| Closing the Teachable Machine tab | There is no autosave and no warning | Download `booth-v1.tm` the moment training finishes. |
| Using "magic", "it just knows", or "the AI figured it out" | These are the phrases adults use, so they feel normal | Rehearse out loud. Have someone hold up a finger every time you say one. |

---

## 📊 Grading Rubric

Score each row. **9–14 = Beginning · 15–20 = Developing · 21–26 = Proficient · 27–32 = Exceptional.**

| Criterion | 1 · Beginning | 2 · Developing | 3 · Proficient | 4 · Exceptional |
|---|---|---|---|---|
| **1. Problem & classes** | Generic demo task (apples vs bananas); classes vague or unnamed | A real-ish task; 3 classes named but no `other`; no baseline stated | A genuine household annoyance; 3 well-chosen classes + `other`; baseline stated as 25% | Classes chosen because they are genuinely *hard to tell apart*; the brief names who is helped, who is hurt, and a success bar written before training |
| **2. Data collection & data card** | Under 20 photos per class; no card, or a card that only says what the data is | 30+ per class; card covers what and how many; provenance vague | 40+ per class, balanced within 20%; card covers all 8 boxes including permission and "what's not in it" | Condition counts tallied across 3+ dimensions during collection; "what's NOT in it" is specific and uncomfortable; permission documented with names and dates |
| **3. Honest testing** | Tested on training photos, or "it worked when I tried it" | Some photos held out but after training, or fewer than 15; accuracy given only as a percentage | 20% held out **before** training; every held-out photo scored on paper; accuracy as fraction → decimal → percentage with the division shown; baseline printed alongside | Held-out set deliberately collected on a different day/surface; per-class accuracy; hand-built confusion matrix; the worst class named with what it gets confused *with* |
| **4. The app** | Doesn't run, or shows a prediction with no reaction | Runs; one or two behaviours; needs the author to nurse it | 4 distinct behaviours, one per class; runs unattended; saved two ways | A working **confidence threshold** that says "not sure"; the low-confidence case is demoed on purpose; Route B booths carry the honesty sign |
| **5. Bias report** | Not attempted, or "it works for everyone" | Notices something is worse without measuring it | 3–4 conditions, 8+ photos each, scored on paper; per-condition accuracy; **gap in percentage points**; a named failing group | Prediction written **before** testing and reported either way; condition × class grid; the highest confidence given while *wrong* displayed large; a fix priced with a specific photo count and arithmetic |
| **6. Honesty & limits** | No limits mentioned; over-claims ("it always works") | Limits mentioned vaguely in conversation only | A printed **"DO NOT USE THIS FOR…"** sign; limits section in the data card matches the measured numbers | The warning sign is the boldest thing on the booth; visitors are actively invited to break it; the break-it log is filled in and one visitor finding is *shown off* |
| **7. The demo** | Reads from a script; uses "magic"/"it just knows"; can't answer questions | Delivers it but stumbles on "how does it know?"; one or two "magic"s slip out | 5 minutes, no notes, **zero** uses of "magic"; explains training → model → prediction in the learner's own words | Answers a question nobody prepared them for by reasoning from data ("that would fail, because I only had 6 photos in lamplight"); volunteers a failure before being asked |
| **8. Craft & completeness** | Loose papers, missing artefacts | Most artefacts present, hard to read | All 11 Must-haves present, legible, laid out so a stranger can follow without help | 3+ Should-haves done well; a stranger could reproduce the whole project from the folder alone |

---

## 🎤 Show Your Work

### The 5-minute demo, minute by minute

```
   ┌─────────┬────────────────────────────────────────────────────────────┐
   │  0:00   │  THE ANNOYANCE (30 s)                                      │
   │         │  "My dad puts the milk carton in the wrong bin about       │
   │         │   twice a week. Here's a thing that tells you which bin."  │
   │         │  Don't start with the technology. Start with the person.   │
   ├─────────┼────────────────────────────────────────────────────────────┤
   │  0:30   │  IT WORKS (60 s)                                           │
   │         │  Hold up one item per class. Let them watch it react.      │
   │         │  Say the confidence out loud each time.                    │
   ├─────────┼────────────────────────────────────────────────────────────┤
   │  1:30   │  HOW IT LEARNED (90 s)  ← the heart of the demo            │
   │         │  "I took 200 photos and typed the right answer next to     │
   │         │   each one. Nobody wrote a rule. The program looked at     │
   │         │   160 of them and found its own pattern. This bit is       │
   │         │   called training. What comes out is the model — the       │
   │         │   guessing machine." Point at the data card as you talk.   │
   ├─────────┼────────────────────────────────────────────────────────────┤
   │  3:00   │  HOW GOOD IT ACTUALLY IS (60 s)                            │
   │         │  "I hid 40 photos before training and it never saw them.   │
   │         │   It got 33 of 40 right — that's 82.5%. Guessing blind     │
   │         │   would be 25%. Here's the sheet." Hand them the sheet.    │
   ├─────────┼────────────────────────────────────────────────────────────┤
   │  4:00   │  WHERE IT FAILS (45 s)  ← the bit that wins the fair       │
   │         │  "It's 91% in daylight and 42% under a lamp, because       │
   │         │   183 of my 200 photos were taken in the afternoon.        │
   │         │   That's a 49-point gap. Watch —" then MAKE IT FAIL.       │
   ├─────────┼────────────────────────────────────────────────────────────┤
   │  4:45   │  THE INVITATION (15 s)                                     │
   │         │  "Try to break it. If you manage, I'll write down what     │
   │         │   you did." Hand them the break-it log and a pen.          │
   └─────────┴────────────────────────────────────────────────────────────┘
```

### The question bank — rehearse all six

| They ask | The shape of a good answer |
|---|---|
| *"But how does it actually know?"* | It doesn't know anything. It saw 160 photos with the answers attached and found which patterns of light and dark go with which answer. Then it matches new photos against those patterns. Name **training**, **model**, **prediction**. |
| *"Could you not just write a rule — if it's shiny it's recycling?"* | Module 3 in one breath: I tried that shape of thing. Shiny catches the can and the crisp packet, which is landfill. Then you add a rule, then another. That's rule explosion — and it's exactly why people started training models from examples instead. |
| *"What happens if it's wrong?"* | Someone puts a carton in the wrong bin — annoying, not dangerous. That's *why* I picked this problem. Then point at the DO NOT USE sign. |
| *"Is my photo being saved? Is it going to Google?"* | Answer precisely, whichever route you chose. Route A: training happened in my browser, my photos never left this laptop, but the finished model is on a Google link. Route B: nothing left this laptop at all. |
| *"How much better is that than guessing?"* | 25% is blind guessing with four classes. Mine got 82.5%. That's 57.5 percentage points better — and here is the fraction, 33 out of 40, so you can see it was 40 photos and not 4,000. |
| *"Should schools/councils use this?"* | No, and here's the number: 42% under lamplight. A bin sensor in a dark kitchen would be wrong more than half the time. To make it usable I'd need about 90 more lamplight photos — here's the arithmetic. |

### 🚫 The banned words

```
   magic  ·  it just knows  ·  the AI figured it out  ·  it's smart
   it thinks  ·  the computer brain  ·  it understands  ·  obviously
```

Practise with a listener holding up a finger for each slip. Three fingers means start that sentence again. It feels silly and it works — the words are habits, and habits only break under a little pressure.

### 🚀 Three stretch directions

**1. Fix it and prove it (~2 h).**
Your bias report priced a fix — say, 90 more lamplight photos. Actually collect them. Retrain. Then rerun the **identical** four bias batches and the **identical** 40-photo held-out test. Publish both columns side by side.

Watch for the thing that surprises everyone: your control condition often gets slightly *worse*. That is real, it is called a trade-off, and explaining it is a Level 3 conversation you get to have in Grade 6. A measured before-and-after table is the single most persuasive object you can put on a table.

**2. The independent audit (~1 h, needs a friend).**
Swap models with someone else's booth. Neither of you may see the other's training photos or data card. Each of you writes a prediction of the other model's weakest condition, tests it with four batches, and reports a gap. Then reveal the data cards and see who guessed the hole correctly from the outside.

This is literally the job of a real AI auditor, and discovering how hard it is *without* access to the training data is the whole lesson. Put both gaps on the poster: yours and your auditor's.

**3. Add a second model and a decision rule (~1.5 h).**
Train an **audio** model in Teachable Machine (clap once / clap twice / background noise) or a **pose** model (thumbs up / thumbs down). Now your booth has two models, and you have a genuinely new problem: **what happens when they disagree?**

Write the rule down before you build it. Does the image model win? Does disagreement mean "not sure"? Does the higher confidence win — and is that actually a good idea, given what Module 5 taught you about confidence not meaning correctness? Whatever you choose, put the rule on the poster. Combining models is a real engineering decision and there is no obviously right answer, which is what makes it worth doing.

---

## 🔑 Key Takeaways

- **The model is the easy 20%.** The data card, the honest test, the bias report and the explanation are the work — and they are what makes anyone trust the model.
- **Split before you train.** It is the only step in this entire project that cannot be fixed afterwards.
- **A number without a fraction and a baseline is a boast, not a measurement.** "33 out of 40, against a baseline of 25%" is a fact. "95% accurate" is marketing.
- **Every model fails on somebody.** Your job is to find out who first, write it in the biggest text on your booth, and price the fix.
- **"I don't know" is a feature.** A confidence threshold that refuses to guess is more useful than one more percentage point of accuracy.
- **If you cannot explain it without the word "magic", you do not understand it yet** — and the fix is always to go back to the data.

---

## ✅ Final Checklist Before You Present

```
   MODEL & DATA
   □ 3 real classes + other, all properly named
   □ 40+ training photos per class, balance under 20%
   □ 20% held out BEFORE training, in a separate folder
   □ booth-v1.tm saved on the computer
   □ Condition counts tallied across 3+ dimensions

   THE HONEST NUMBERS
   □ Every held-out photo scored on paper, as it happened
   □ Accuracy as fraction → decimal → percentage, division shown
   □ Baseline (25%) printed right next to it
   □ Per-class accuracy
   □ Confusion matrix drawn by hand
   □ Worst class named, with what it is confused with

   THE APP
   □ 4 distinct behaviours, one per class
   □ Confidence threshold → "not sure" below the cut-off
   □ Tested with an object that belongs to no class
   □ Saved as .sb3 AND to the Scratch account
   □ Route B booths: honesty sign printed

   THE HUMAN SIDE
   □ Bias prediction written BEFORE testing, shown either way
   □ 3–4 conditions × 8+ photos, scored on paper
   □ Accuracy gap in percentage points
   □ Highest confidence while WRONG, displayed large
   □ Data card printed, all 8 boxes filled
   □ "DO NOT USE THIS FOR…" — the boldest text on the booth
   □ A priced fix with the photo-count arithmetic

   THE DEMO
   □ Script written and said out loud three times
   □ Timed at 5 minutes or under
   □ Six question-bank answers rehearsed
   □ Zero uses of "magic"
   □ One deliberate failure ready to demo on request
   □ Break-it log and a pen on the table
```

---

## 🎓 You Have Finished Level 1

Look back at what you can do now that you could not do twelve weeks ago.

You can look at any system and say whether a person wrote its rules or a machine learned them. You can turn a corner of the world into a table. You can train a model, and — much rarer — you can *test* one honestly. You know an image is a grid of numbers and a chatbot is a next-word guesser. You have found the group your own model treats badly, measured the gap, and printed it where everybody can see.

Most adults working near AI cannot do the fourth and sixth of those things.

Level 2 hands you a keyboard. Everything you just built by hand — the table, the split, the accuracy, the confusion matrix — becomes three lines of Python each. **The ideas do not change. Only the typing does.** That is exactly why you did this level slowly.

Go and take the [assessment](assessment.md) if you haven't. Then:

> ### 👉 **[Level 2 — Builder](../level-2-builder/)**

---

[⬅ Module 9](module-09-fair-private-honest-ai.md) · [Level 1 Home](README.md) · [Assessment](assessment.md) · [Glossary](glossary.md) · [Level 2 ➡](../level-2-builder/)

*You built a guessing machine, you measured it honestly, and you told everyone what it was bad at. That is the whole job. See you in Level 2.*

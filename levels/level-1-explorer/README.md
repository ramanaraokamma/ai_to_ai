```
  ██╗     ███████╗██╗   ██╗███████╗██╗          ██╗
  ██║     ██╔════╝██║   ██║██╔════╝██║        ███║
  ██║     █████╗  ██║   ██║█████╗  ██║        ╚██║
  ██║     ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║         ██║
  ███████╗███████╗ ╚████╔╝ ███████╗███████╗    ██║
  ╚══════╝╚══════╝  ╚═══╝  ╚══════╝╚══════╝    ╚═╝

   ███████╗██╗  ██╗██████╗ ██╗      ██████╗ ██████╗ ███████╗██████╗
   ██╔════╝╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██╔══██╗██╔════╝██╔══██╗
   █████╗   ╚███╔╝ ██████╔╝██║     ██║   ██║██████╔╝█████╗  ██████╔╝
   ██╔══╝   ██╔██╗ ██╔═══╝ ██║     ██║   ██║██╔══██╗██╔══╝  ██╔══██╗
   ███████╗██╔╝ ██╗██║     ███████╗╚██████╔╝██║  ██║███████╗██║  ██║
   ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
```

# 🧭 Level 1 — Explorer

### *Machines can learn a rule from examples instead of being told the rule.*

**Grade band:** 6 (age ~11) · **Coding required:** none · **Math required:** fractions, percentages, reading a graph
**Duration:** ~12 weeks · 9 modules (~3 h each) + a ~6 h capstone · **~32 hours total**

[⬅ Back to AI Academy](../../README.md) · [Full curriculum map](../../CURRICULUM_MAP.md) · [Level 2 ➡](../level-2-builder/)

---

## 🪝 Why This Level Exists

Ask ten adults what AI is and you will get ten answers involving robots, brains, or the word "magic". None of those answers will help you build anything.

Here is the answer this level installs, and it takes one sentence: **AI is a system that turns examples into a guessing machine.**

That's it. Not a brain. Not a mind. A pile of examples goes in one end, a guessing machine comes out the other, and the whole thing can be built, measured, broken, and found unfair — by you, in twelve weeks, without writing a single line of code.

By the end you will have trained a real image classifier, tested it honestly on photos it had never seen, computed its accuracy by hand, found the group of inputs it fails on, and explained all of it to an adult without saying "magic" once.

---

## 🎯 Level Outcomes

When you finish Level 1 you will be able to:

1. **Tell apart** a system that follows rules a human wrote from a system that learned from examples — and defend your call on the hard cases where it could be either.
2. **Build a real dataset by hand** — rows as examples, columns as features, one column as the label — and write its data card.
3. **Train an image classifier** in Teachable Machine, hold out test examples, and compute its accuracy by hand as a fraction, a decimal, and a percentage.
4. **Explain why testing a model on its own training examples is cheating**, and describe memorizing vs generalizing in your own words.
5. **Explain how a computer sees an image** as a grid of numbers, and how a chatbot guesses the next word.
6. **Run a bias test on your own model** and name at least one group of inputs it handles badly, with the accuracy gap in percentage points.

---

## 🎒 What You Need Before Starting

### Prerequisites — the honest list

| You need | Why | If you don't have it |
|---|---|---|
| To read comfortably | Every module is 700+ lines of reading | Do it with an adult, one section a day |
| Fractions and percentages | Accuracy is `correct ÷ total`, shown three ways | Module 6 re-teaches the arithmetic step by step |
| To be able to read a simple table | Everything in AI is a table | Module 2 builds tables from scratch |
| Patience with being wrong | You will deliberately break your own model | This is the actual skill. Start now. |
| **Nothing else** | Zero coding. No maths past Grade 6. No prior AI. | — |

### Physical materials (buy/find these in week 0)

```
   ┌─────────────────────────────────────────────────────────────┐
   │  THE LEVEL 1 KIT — total cost: about the price of a pizza   │
   ├─────────────────────────────────────────────────────────────┤
   │  □  A notebook you will use only for this course            │
   │  □  Pencil + eraser (you will erase a lot)                  │
   │  □  ~40 index cards (Module 4's Feature Card Deck)          │
   │  □  Graph paper, at least 20 sheets (Module 7's Pixel Lab)  │
   │  □  3–4 coloured pens or highlighters                       │
   │  □  1 large sheet of poster paper (Module 9 + capstone)     │
   │  □  A sealable envelope (Module 6 — for hiding test photos) │
   │  □  Sticky notes                                            │
   └─────────────────────────────────────────────────────────────┘
```

### Digital things (all free, all in a browser)

| Tool | Used in | Account needed? | Cost |
|---|---|---|---|
| A modern browser (Chrome / Edge / Safari / Firefox) | everything | no | free |
| A working **webcam** (laptop camera or phone) | Modules 5, 6, 9, capstone | no | free |
| [Google Teachable Machine](https://teachablemachine.withgoogle.com) | Modules 5, 6, 9, capstone | no (yes only to save to Drive) | free |
| [Scratch](https://scratch.mit.edu) | Module 8, capstone | yes, to save your project | free |
| [Quick, Draw!](https://quickdraw.withgoogle.com) | Module 1, 7 | no | free |
| Google Sheets / Excel / LibreOffice Calc | Modules 2, 7, 8 | Sheets needs a Google account | free |

> ⚠️ **A grown-up should read this bit.** Teachable Machine runs entirely **in the browser** — training happens on your own computer and photos are not uploaded anywhere unless you deliberately click "Upload my model". Scratch projects *are* stored on Scratch's servers when you save them, so don't put your full name, school, or address into a Scratch project. Module 9 makes this a lesson rather than a rule.

---

## 🗺️ The Roadmap

```
                    LEVEL 1 · EXPLORER — nine modules and a fair booth

   WHAT IS IT?                    WHAT IS IT MADE OF?
   ┌───────────────────┐          ┌───────────────────┐          ┌───────────────────┐
   │  1. WHAT AI IS    │          │  2. DATA IS       │          │  3. PATTERNS &    │
   │     AND ISN'T     │─────────►│     EVERYWHERE    │─────────►│     RULES         │
   │                   │          │                   │          │                   │
   │  rules · learning │          │  rows · columns   │          │  if-then rules    │
   │  generating       │          │  types · messy    │          │  rule explosion   │
   │  narrow vs general│          │  provenance       │          │  the ML trade     │
   └───────────────────┘          └───────────────────┘          └─────────┬─────────┘
                                                                           │
      "AI is a machine doing a job         "Everything an AI knows          │  rules
       that needed judgement"               arrived as a table"             │  break
                                                                            ▼
   ┌───────────────────┐          ┌───────────────────┐          ┌───────────────────┐
   │  6. TRAIN, TEST,  │◄─────────│  5. LEARNING FROM │◄─────────│  4. FEATURES &    │
   │     TRUST         │          │     EXAMPLES      │          │     LABELS        │
   │                   │          │                   │          │                   │
   │  hide 20%         │          │  ⚡ FIRST MODEL   │          │  feature · label  │
   │  accuracy by hand │          │  Teachable Machine│          │  useful/useless/  │
   │  memorize vs      │          │  confidence score │          │  leaky            │
   │  generalize       │          │  class balance    │          │  classify vs      │
   └─────────┬─────────┘          └───────────────────┘          │  predict a number │
             │                                                    └───────────────────┘
             │  now you can measure. but WHY does it fail?
             ▼
   ┌───────────────────┐          ┌───────────────────┐          ┌───────────────────┐
   │  7. HOW COMPUTERS │─────────►│  8. HOW COMPUTERS │─────────►│  9. FAIR, PRIVATE │
   │     SEE           │          │     READ & CHAT   │          │     AND HONEST    │
   │                   │          │                   │          │                   │
   │  pixels 0–255     │          │  tokens · bigrams │          │  bias from gaps   │
   │  RGB · resolution │          │  next-word guess  │          │  privacy · fakes  │
   │  3×3 filters      │          │  fluent ≠ true    │          │  over-trust       │
   │  edges            │          │  Scratch chatbot  │          │  ⚖️ audit YOUR    │
   └───────────────────┘          └───────────────────┘          │     model         │
                                                                  └─────────┬─────────┘
                                                                            │
                                                                            ▼
                                          ╔═════════════════════════════════════════╗
                                          ║   🎪  CAPSTONE — THE AI FAIR BOOTH      ║
                                          ║                                         ║
                                          ║   a classifier that solves a real       ║
                                          ║   problem in your home + a Scratch app  ║
                                          ║   + a data card + an honest test sheet  ║
                                          ║   + a bias report + a 5-minute demo     ║
                                          ║   with the word "magic" banned          ║
                                          ╚═════════════════════════════════════════╝
```

**Read the arrows as "you need this before that."** Module 4 feeds 5, 5 feeds 6, and 6 is where the level's honesty lives. Modules 7 and 8 open the two black boxes (seeing, reading). Module 9 turns the whole thing back on yourself.

---

## 📚 The Nine Modules

| # | Module | You'll build | Time |
|:--:|---|---|:--:|
| 1 | [**What AI Is, What It Isn't, and Where It's Hiding in Your Day**](module-01-what-ai-is-and-isnt.md) | 🕵️ **AI Spotter's Log** — 15 systems you touched in 24 hours, sorted into rules / learned / generating, with 3 hard calls defended in writing | ~2.5 h |
| 2 | [**Data Is Everywhere: Turning the World Into Rows and Columns**](module-02-data-is-everywhere.md) | 📊 **Your Life In 30 Rows** — a real 30-row spreadsheet about your own week, 4+ columns, plus a written data card | ~3 h |
| 3 | [**Patterns and Rules: When Writing Rules Stops Working**](module-03-patterns-and-rules.md) | 📕 **Rulebook vs Reality** — a 5-rule spam detector you wrote by hand, scored on 10 messages it has never seen | ~2.5 h |
| 4 | [**Features and Labels: How a Machine Describes a Thing**](module-04-features-and-labels.md) | 🃏 **Feature Card Deck** — 20 index cards, 5 features on the front, the label hidden on the back, handed to a human tester | ~3 h |
| 5 | [**Learning From Examples: Train Your First Model (No Code)**](module-05-learning-from-examples.md) | 🤖 **Three-Class Classifier** — a working Teachable Machine model plus a 5-row controlled-experiment table explaining every result | ~3 h |
| 6 | [**Train, Test, Trust: Why You Must Hide Some Examples**](module-06-train-test-trust.md) | 🔒 **The Hidden Ten** — a paper scoring sheet, accuracy shown three ways, and a hand-drawn confusion matrix | ~3 h |
| 7 | [**How Computers See: Pixels, Grids, and Edges**](module-07-how-computers-see.md) | 🔬 **Pixel Lab** — a 12×12 letter typed as numbers, run through a 3×3 edge filter in a spreadsheet, with the outline appearing | ~3 h |
| 8 | [**How Computers Read and Chat: Words, Guesses, and Autocomplete**](module-08-how-computers-read-and-chat.md) | 💬 **The Human Language Model** — a hand-tallied next-word table, 3 generated sentences, and a running Scratch chatbot | ~3 h |
| 9 | [**Fair, Private, and Honest: The Human Side of AI**](module-09-fair-private-honest-ai.md) | ⚖️ **Fairness Audit Poster** — a product data map plus a measured bias test on your own model, gap in percentage points | ~3 h |
| 🎪 | [**CAPSTONE — The AI Fair Booth**](capstone.md) | 🏆 A classifier + Scratch app + data card + honest test sheet + bias report + a 5-minute live demo | ~6 h |

**Also in this folder:**

| File | What it's for | When to use it |
|---|---|---|
| [`assessment.md`](assessment.md) | 20 multiple-choice + 8 short-answer + 4 debug problems, with a full explained answer key | After Module 9, before the capstone |
| [`glossary.md`](glossary.md) | Every term in this level, alphabetized, with a plain definition and an example from the course | Any time a word stops making sense |
| [`capstone.md`](capstone.md) | The final build, with milestones, a rubric, and a worked partial solution | Weeks 11–12 |

---

## 🧭 How This Level Fits the Whole Journey

### What came before (your "Level 0")

There is no Level 0 file, because **you already did Level 0 by being alive.** Seriously — here is what you bring in on day one, and every bit of it gets used:

| You already know how to... | Level 1 renames it as... | First used in |
|---|---|---|
| Pick a ripe mango without being told the rule | **Learning from examples** | Module 1 |
| Keep score in a game on paper | **A table: rows and columns** | Module 2 |
| Follow your mum's note on the fridge | **A rule-based system** | Module 1 |
| Describe your dog to a friend on the phone | **Features** | Module 4 |
| Know you did well on a test because it had new questions | **A test set** | Module 6 |
| Notice when a photo is fake | **Provenance checking** | Module 9 |
| Tap the middle word on your phone keyboard | **Next-word prediction** | Module 8 |

You are not starting from zero. You are starting from "has all the intuitions, none of the words."

### What Level 2 needs from you

Level 2 (**Builder**, grades 7–8) teaches Python and scikit-learn. It will assume, without re-teaching, that you can do these things **cold**:

```
   ┌──────────────────────────────────────────────────────────────────────┐
   │  LEVEL 2 ASSUMES YOU ALREADY OWN THESE — from Level 1                │
   ├──────────────────────────────────────────────────────────────────────┤
   │                                                                      │
   │   Level 1 idea                  ─►   Level 2 turns it into           │
   │   ─────────────────────────────      ──────────────────────────────  │
   │   a table of rows and columns   ─►   a pandas DataFrame              │
   │   features and a label column   ─►   X and y                         │
   │   "hide 20% before training"    ─►   train_test_split(test_size=0.2) │
   │   accuracy = correct ÷ total    ─►   accuracy_score(y_test, y_pred)  │
   │   confidence score              ─►   predict_proba()                 │
   │   your confusion matrix on paper─►   confusion_matrix()              │
   │   "which class is it worst at?" ─►   per-class precision and recall  │
   │   a data card                   ─►   a dataset README + model card   │
   │                                                                      │
   └──────────────────────────────────────────────────────────────────────┘
```

Notice what that table is really saying: **Level 2 does not teach you a single new idea in that list.** It teaches you how to *type* the ideas you already have. That is why Level 1 is worth doing slowly. If `train_test_split` is just a spelling of something you already believe in your bones, Level 2 is easy. If it isn't, Level 2 is a nightmare of memorized incantations.

> **The one-sentence handover:** Level 1 gives you the *concepts* with your hands; Level 2 gives you the *keyboard*; Level 3 gives you the *maths under the hood*; Level 4 gives you the *frontier*.

---

## 🔧 Environment Setup

Level 1 uses **no installed software**. There is nothing to `pip install`, no terminal, no version conflicts. That is deliberate — you should be arguing about data, not about Python versions.

But "no install" is not "no setup". Do these five checks **before Module 1**, in one sitting of about 20 minutes. They will save you an hour of frustration in Module 5.

### Step 1 — Check your browser (2 min)

| Browser | Minimum version | How to check |
|---|---|---|
| **Chrome** ✅ recommended | 90+ | Menu ⋮ → Help → About Google Chrome |
| **Edge** ✅ | 90+ | Menu … → Help and feedback → About |
| **Safari** ⚠️ works, occasionally fussy with the webcam | 15+ | Safari menu → About Safari |
| **Firefox** ⚠️ works; Teachable Machine is slower | 100+ | Menu ☰ → Help → About Firefox |

If your browser is older than that, update it. Teachable Machine trains the model *inside the browser tab*, and old browsers are missing the piece that does it.

### Step 2 — Prove the webcam works (3 min)

1. Go to **https://teachablemachine.withgoogle.com**
2. Click **Get Started** → **Image Project** → **Standard image model**
3. Under `Class 1`, click **Webcam**
4. Your browser will ask *"Allow camera access?"* → click **Allow**

You should see yourself. If you don't, jump to the troubleshooting table below.

### Step 3 — The 3-line smoke test (5 min)

This is the Level 1 equivalent of `python -c "import torch"`. It proves the whole toolchain works end to end. **Do it now, not in Module 5.**

```
   ┌─────────────────────────────────────────────────────────────────────┐
   │  🔥 LEVEL 1 SMOKE TEST — 3 lines, ~5 minutes                        │
   ├─────────────────────────────────────────────────────────────────────┤
   │                                                                     │
   │  1.  Class 1 → Webcam → hold up your LEFT HAND, flat, palm forward. │
   │      Press and HOLD "Hold to Record" for ~4 seconds. (≈40 frames)   │
   │                                                                     │
   │  2.  Class 2 → Webcam → hold up a CLOSED FIST.                      │
   │      Press and HOLD for ~4 seconds. (≈40 frames)                    │
   │                                                                     │
   │  3.  Click "Train Model". Wait ~20 seconds. Then hold up your open  │
   │      palm and watch the Preview bar on the right.                   │
   │                                                                     │
   ├─────────────────────────────────────────────────────────────────────┤
   │  ✅ PASS if:  Class 1 shows above 80% for the open palm,            │
   │               and the two bars swap when you make a fist.           │
   │  ❌ FAIL if:  "Train Model" is greyed out, the tab freezes, or      │
   │               both bars sit near 50% no matter what you do.         │
   └─────────────────────────────────────────────────────────────────────┘
```

If it passes, **you are fully set up for the entire level.** Close the tab without saving; you will build the real thing in Module 5.

### Step 4 — Check your spreadsheet (5 min)

Open Google Sheets, Excel, or LibreOffice Calc and type this into cell `A1`:

```
=SUM(1,2,3)
```

Press Enter. If you see **6**, you're fine.

Then check one more, because Module 7 depends on it. In `A3` type:

```
=ABS(-765)
```

You should see **765**. Modules 7 and 8 use only these functions: `SUM`, `ABS`, `COUNTIF`, `COUNTIFS`, `UNIQUE`, `VLOOKUP`, `RAND`, `IF`. All of them exist in all three programs.

> ⚠️ **`UNIQUE` note.** `UNIQUE()` works in Google Sheets and Excel 365 but **not** in Excel 2019 or LibreOffice Calc. Module 8 gives you the manual workaround for both, so this is not a blocker — just know which camp you're in before you start.

### Step 5 — Set up Scratch (5 min)

1. Go to **https://scratch.mit.edu** → **Join Scratch**
2. Pick a username that is **not your real name** (Module 9 will explain exactly why; do it now anyway)
3. Click **Create**, then File → **Save to your computer** to check saving works
4. In the block palette, find **Variables → Make a List**. If you can create a list called `test`, you have everything Module 8 needs.

### ✅ Setup complete checklist

- [ ] Browser is Chrome/Edge 90+, Safari 15+, or Firefox 100+
- [ ] Camera permission granted to `teachablemachine.withgoogle.com`
- [ ] Smoke test passed — palm vs fist, above 80%
- [ ] `=SUM(1,2,3)` returns 6 and `=ABS(-765)` returns 765
- [ ] Scratch account created with a non-identifying username, and you can make a list
- [ ] The physical kit (index cards, graph paper, envelope, poster paper) is in a box somewhere

---

## 🚑 Troubleshooting — the five things that actually go wrong

| # | Symptom | Most likely cause | Fix |
|:--:|---|---|---|
| 1 | **"Train Model" is greyed out** in Teachable Machine | One of your classes has 0 samples, or a class was created and never filled | Every class needs **at least 1** sample (aim for 30+). Delete empty classes with the ⋮ menu → *Delete Class*. Check every class, including ones scrolled off-screen. |
| 2 | **Webcam shows a black rectangle**, or "Could not start video source" | Another app is holding the camera (Zoom, Teams, FaceTime, another browser tab), or permission was denied | Quit every other app that uses the camera, close duplicate Teachable Machine tabs, then reload. To re-grant permission: click the **🔒 padlock** in the address bar → Camera → **Allow** → reload the page. On a Mac also check *System Settings → Privacy & Security → Camera*. |
| 3 | **Training freezes, the fan roars, or the tab crashes** ("Aw, Snap!") | Too many samples for the browser's memory — usually 500+ per class, or 15 other tabs open | Training happens *on your laptop*, not in the cloud. Close other tabs. Keep classes to **30–120 samples each** — Module 5 shows that 40 good photos beat 400 identical ones anyway. If it still crashes, use Chrome rather than Safari. |
| 4 | **Every class sits near equal confidence** (e.g. 34% / 33% / 33%) no matter what you show it | The classes look the same *to the model* — same background, same lighting, same distance — so there is nothing to tell apart. Or you accidentally recorded the same object into two classes. | Click each class and scroll its thumbnails: are they visibly different sets? Re-collect with the Module 5 variety checklist — change background, distance, angle, and lighting. Backgrounds are the #1 culprit: if all of Class 1 is on a wooden table and all of Class 2 is on a white sheet, the model learns *tables*, which Module 6 calls out. |
| 5 | **My model vanished when I closed the tab** | Teachable Machine keeps nothing unless you export it. There is no autosave. | Before you close anything: **☰ menu → Download project as file** (a `.tm` file on your computer) or **Save project to Drive**. Modules 5, 6 and 9 all ask you to reload a saved baseline, so build the habit now. Name it something real, like `baseline-v1.tm`, not `Untitled.tm`. |

**Two more, less common but maddening:**

| # | Symptom | Fix |
|:--:|---|---|
| 6 | Scratch says *"Could not save project"* | You're logged out (the session times out). Open scratch.mit.edu in another tab, log in, come back, then File → Save now. Meanwhile, always keep a File → *Save to your computer* `.sb3` backup. |
| 7 | Spreadsheet formula shows as literal text, e.g. the cell displays `=SUM(1,2,3)` | The cell is formatted as Text. Select it → Format → Number → **Automatic** (Sheets) or **General** (Excel), then retype the formula. |

---

## 📅 Weekly Pacing

Twelve weeks. One module a week for nine weeks, a consolidation week, then two weeks of capstone. About **2.5–3 hours a week**, split into four short sittings rather than one long one — the ideas need overnight to settle.

### The weekly rhythm

```
   ┌──────┬──────────┬────────────────────────────────────────────────────┐
   │ DAY  │  TIME    │  WHAT YOU DO                                       │
   ├──────┼──────────┼────────────────────────────────────────────────────┤
   │ MON  │  ~40 min │  🪝 Hook + 🧠 Concept                              │
   │      │          │  Read slowly. After each sub-concept, close the    │
   │      │          │  file and say it out loud in your own words.       │
   ├──────┼──────────┼────────────────────────────────────────────────────┤
   │ WED  │  ~40 min │  🔍 Worked Example + 💻 Hands-On                   │
   │      │          │  Do the arithmetic yourself on paper BEFORE you    │
   │      │          │  read the next line. Cover the page with a card.   │
   ├──────┼──────────┼────────────────────────────────────────────────────┤
   │ FRI  │  ~40 min │  ✍️ Practice (all 6) + ⚠️ Common Mistakes         │
   │      │          │  Warm-ups first. Struggle 15 minutes before you    │
   │      │          │  open the answer key. The struggle IS the lesson.  │
   ├──────┼──────────┼────────────────────────────────────────────────────┤
   │ SAT  │  ~60 min │  🛠️ Mini-Project + 🔑 Key Takeaways               │
   │      │          │  Build the thing. Then explain it to a real human  │
   │      │          │  with the file closed.                             │
   └──────┴──────────┴────────────────────────────────────────────────────┘
```

### The twelve weeks

| Week | Module | Focus | Hand in at the end of the week |
|:--:|---|---|---|
| **1** | [M1](module-01-what-ai-is-and-isnt.md) — What AI Is | Vocabulary and sorting | AI Spotter's Log: 15 rows + 3 defences |
| **2** | [M2](module-02-data-is-everywhere.md) — Data Is Everywhere | Tables and honesty | 30-row spreadsheet + 5-line data card |
| **3** | [M3](module-03-patterns-and-rules.md) — Patterns and Rules | Why ML had to be invented | Spam rulebook + scored fresh-message table |
| **4** | [M4](module-04-features-and-labels.md) — Features and Labels | The machine's-eye view | 20-card Feature Card Deck + a tester's score |
| **5** | [M5](module-05-learning-from-examples.md) — Learning From Examples | ⚡ **Your first model** | Working classifier + 5-row experiment table |
| **6** | [M6](module-06-train-test-trust.md) — Train, Test, Trust | 🔑 **The most important week** | Scoring sheet + accuracy 3 ways + confusion matrix |
| **7** | [M7](module-07-how-computers-see.md) — How Computers See | Inside the image | Two shaded 12×12 grids + one cell's arithmetic |
| **8** | [M8](module-08-how-computers-read-and-chat.md) — Read and Chat | Inside the chatbot | Tally sheet + 3 generated sentences + Scratch bot |
| **9** | [M9](module-09-fair-private-honest-ai.md) — Fair, Private, Honest | Who gets hurt | Fairness Audit Poster |
| **10** | — **Consolidation** | Catch up + prove it | [`assessment.md`](assessment.md): 20 MCQ, 8 short answer, 4 debug |
| **11** | 🎪 [Capstone](capstone.md), part 1 | Data + model + honest test | Milestones 1–4 done |
| **12** | 🎪 [Capstone](capstone.md), part 2 | Scratch app + bias report + demo | The booth, presented to an adult |

### Pacing variations

| If you have... | Do this |
|---|---|
| **~90 min/week** | Take 18 weeks: split each module across two weeks (concept week, project week). Never skip the mini-project — it is where the learning is. |
| **~6 h/week (holidays)** | 6 weeks: two modules a week, but keep Modules 5→6 in *different* weeks. Module 6 only lands if Module 5's model has had time to disappoint you. |
| **A study partner** | Add a 20-minute Sunday call: each of you explains the week's mini-project with the file closed. From Module 4 on, swap decks/models and test each other's. Module 9's "level it up" is built for this. |
| **A school term structure** | Weeks 1–9 as lessons, week 10 as the assessment, weeks 11–12 as a class AI Fair where everyone presents a booth on the same afternoon. |

### ⚠️ Two pacing rules that matter more than the schedule

1. **Never do Module 5 and Module 6 on the same day.** Module 5 ends with you proud of a 91% model. Module 6 exists to show you that number might have been a lie. That gap needs a few days of pride in between, or the lesson doesn't bite.
2. **If you fall behind, drop the *extensions*, never the mini-projects.** Every "level it up" section is optional. Every 🛠️ Mini-Project is not — the capstone assumes you have a trained model from Module 5, a scoring habit from Module 6, and a bias result from Module 9.

---

## 🧾 The Level 1 Promise

Twelve weeks from now, someone will ask you what AI is.

You will not say "robots". You will not say "a computer brain". You will not say "magic".

You will say something like: *"It's a system that turns examples into a guessing machine. I built one that tells my three toothbrushes apart. It's 87% accurate on photos it's never seen — I worked that out by hand, 13 out of 15. It's worse in lamplight because 94% of my training photos were taken in daylight, and I can show you the gap: 50 percentage points. Want to see it fail?"*

And then you will show them, because showing your model failing is the most honest thing an engineer can do.

---

## ▶️ Start Here

> ### 👉 **[Module 1 — What AI Is, What It Isn't, and Where It's Hiding in Your Day](module-01-what-ai-is-and-isnt.md)**
>
> Read the 🪝 Hook. It's four sentences about a computer that beat the world's best Go player and couldn't play checkers.

---

[⬅ Back to AI Academy](../../README.md) · [Curriculum map](../../CURRICULUM_MAP.md) · [Glossary](glossary.md) · [Assessment](assessment.md) · [Capstone](capstone.md) · [Level 2 ➡](../level-2-builder/)

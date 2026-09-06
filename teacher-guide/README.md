```
  ████████╗███████╗ █████╗  ██████╗██╗  ██╗███████╗██████╗
  ╚══██╔══╝██╔════╝██╔══██╗██╔════╝██║  ██║██╔════╝██╔══██╗
     ██║   █████╗  ███████║██║     ███████║█████╗  ██████╔╝
     ██║   ██╔══╝  ██╔══██║██║     ██╔══██║██╔══╝  ██╔══██╗
     ██║   ███████╗██║  ██║╚██████╗██║  ██║███████╗██║  ██║
     ╚═╝   ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

        █████╗ ██╗   ██╗██╗██████╗ ███████╗
       ██╔════╝██║   ██║██║██╔══██╗██╔════╝
       ██║  ███╗██║   ██║██║██║  ██║█████╗
       ██║   ██║██║   ██║██║██║  ██║██╔══╝
       ╚██████╔╝╚██████╔╝██║██████╔╝███████╗
        ╚═════╝  ╚═════╝ ╚═╝╚═════╝ ╚══════╝
```

# 🧑‍🏫 The AI Academy Teacher & Parent Guide

### *You do not need to know AI to guide someone through this course. You need to know how to ask a second question.*

**For:** a parent, teacher, mentor, or older sibling guiding **one learner** from grade 6 to grade 12
**Companion files:** [`pacing-guide.md`](pacing-guide.md) · [`rubrics.md`](rubrics.md) · [`progress-tracker.md`](progress-tracker.md) · [`../RESOURCES.md`](../RESOURCES.md)

[⬅ Back to AI Academy](../README.md) · [Full curriculum map](../CURRICULUM_MAP.md)

---

## 🪝 Start Here: The Only Thing You Actually Have To Do

A parent once told me she couldn't help her daughter with this course because she "didn't know any Python." Her daughter was stuck on a decision tree that scored 100% on training data and 61% on test data. The mother had no idea what any of those words meant. So she asked the only question she had:

> *"Wait — why are there two numbers?"*

Her daughter explained it for four minutes. Somewhere in minute three she stopped, said "oh," and went and fixed it.

That is the job. **You are not the answer key. You are the person the learner has to explain it to.** The course carries the content — 36 modules, every one with a worked example, six practice exercises, and a full answer key. What the course cannot do is sit in a chair and look mildly confused at the right moment.

If you read nothing else in this file, read this:

```
   ┌───────────────────────────────────────────────────────────────────────┐
   │  THE FOUR QUESTIONS THAT DO 80% OF THE TEACHING                       │
   ├───────────────────────────────────────────────────────────────────────┤
   │                                                                       │
   │   1.  "Show me."                    ← forces a demo, not a claim      │
   │   2.  "What did you expect?"        ← surfaces the wrong model early  │
   │   3.  "How do you know it's right?" ← installs the evaluation habit   │
   │   4.  "What would break it?"        ← installs the engineering habit  │
   │                                                                       │
   │   You can ask all four without understanding a single line of code.   │
   └───────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 What This Guide Gives You

By the time you've read this file you will be able to:

1. **Run a 60–90 minute session** with a predictable shape, without preparing content beforehand.
2. **Tell the difference between productive struggle and stuck** — and know exactly how long to wait before intervening.
3. **Use the 🤔 Think Deeper questions as real discussion**, including when the learner's answer is better than yours.
4. **Adapt the pace** for a learner racing ahead and for one who needs three weeks on a two-week module — without either of them feeling it as reward or punishment.
5. **Assess work honestly** using the [rubrics](rubrics.md), and say what "not yet" means in a way that doesn't land as "no."
6. **Recognise the five places** in this course where learners predictably fall off, and what to do at each one.

---

## 🧠 The Teaching Philosophy

This course is built on four commitments. They are not decoration — they determine why modules are ordered the way they are, and if you break them the course stops working.

### 1. Concrete before abstract, always

> **The rule:** No idea is named before it has been felt. Every abstract concept in this course lands on an everyday anchor first — pizza, cricket scores, spam texts, photos of the learner's own toothbrushes — and only *then* gets its formal name.

Level 1 Module 6 does not open with "the train/test split." It opens with the learner putting ten of their own photos in a sealed envelope. The envelope comes first. `train_test_split(test_size=0.2)` arrives fourteen weeks later in Level 2, at which point it is a *spelling* of something the learner already believes.

Watch what this means for you as a guide:

| ❌ Don't say | ✅ Say instead |
|---|---|
| "Overfitting is when the model has high variance." | "Your model got 100% on the photos it studied and 61% on the new ones. What does that remind you of?" |
| "A gradient is a vector of partial derivatives." | "You're on a hill in fog. You can only feel the slope under your feet. Which way do you step?" |
| "TF-IDF downweights common terms." | "If every review says 'the', does 'the' tell you anything about whether the review is positive?" |
| "Let me explain what the answer is." | "Show me the smallest example where it goes wrong." |

**The anti-pattern to watch for in yourself:** you will be tempted to give the formal definition because it is *shorter*. It is. It is also the version that doesn't stick. If the learner can restate the analogy, they own the idea. If they can only restate the definition, they own a sentence.

### 2. The spiral: six ideas, four times, deeper each pass

The whole course is six ideas revisited at four depths. Nothing is ever "finished."

```
              THE SPIRAL — one idea, four passes

     DATA        REPRESENTATION      MODEL      LEARNING SIGNAL   EVALUATION   HUMAN IMPACT
       │               │               │              │                │            │
   L1  ├─ 30 rows      ├─ feature      ├─ a guessing  ├─ "show it      ├─ hide 10   ├─ a fairness
       │  by hand      │  card         │  box         │  more"         │  photos    │  poster
       │               │               │              │                │            │
   L2  ├─ a DataFrame  ├─ X matrix     ├─ kNN, tree,  ├─ fit()         ├─ accuracy, ├─ whose data
       │               │               │  line        │                │  MAE, R²   │  is this?
       │               │               │              │                │            │
   L3  ├─ train/val/   ├─ Column-      ├─ a Pipeline  ├─ loss +        ├─ precision,├─ a model
       │  test + audit │  Transformer  │  artifact    │  gradient      │  recall,   │  card w/
       │               │  + conv maps  │              │  descent       │  ROC, CV   │  subgroups
       │               │               │              │                │            │
   L4  ├─ token corpora├─ learned      ├─ transformer ├─ next-token +  ├─ frozen    ├─ red team
       │  + pref pairs │  embeddings   │  blocks, RAG │  human         │  eval sets,│  + system
       │               │               │  agents      │  preference    │  LLM judge │  card
       ▼               ▼               ▼              ▼                ▼            ▼
```

**What this means when you're guiding:** when a learner struggles in Level 3, the fix is usually one level down, not one paragraph back. A learner who can't reason about data leakage in L3 M2 often doesn't truly own "hide the test set" from L1 M6. Send them back. It costs an hour and saves a month.

The [curriculum map's spiral table](../CURRICULUM_MAP.md#-the-spiral-progression) is the diagnostic tool. Ask the learner to fill in one row from memory. Blanks are your lesson plan.

### 3. Build to learn, not learn to build

Every single module ends in a 🛠️ **Mini-Project** — a thing that exists afterwards. Thirty-six of them. Plus four capstones.

This is not "applying what you learned." **The project is where the learning happens.** The reading is the setup. A learner who reads Module 8 of Level 2 and doesn't build the Classifier Lab has not learned kNN; they have read about kNN, which is a different and much less durable thing.

> **The hard rule that follows from this:** if you have to cut something for time, cut the [Stretch] exercises and the "level it up" extensions. **Never cut a mini-project.** Every capstone assumes the mini-projects exist — Level 4's capstone is literally assembled from Modules 6, 7 and 8's outputs.

### 4. Honesty over performance

This course is unusually insistent that the learner find their own model's failures. Level 1's capstone requires a bias report. Level 3's requires a model card naming subgroups it works worse for. Level 4's requires a section titled *"what this fails at, and who should not rely on it."*

That has a consequence for your side of the table:

```
   ┌───────────────────────────────────────────────────────────────────────┐
   │  CELEBRATE FINDING THE BUG AS LOUDLY AS YOU CELEBRATE THE SCORE.      │
   │                                                                       │
   │  "It's 94% accurate!"                        → "Nice. What's the      │
   │                                                  baseline?"           │
   │  "I found out it fails on photos in lamp     → "THAT is the best      │
   │   light — 50 points worse."                      thing you've done    │
   │                                                  all month."          │
   └───────────────────────────────────────────────────────────────────────┘
```

A learner who has been praised for finding their own failures becomes an engineer. A learner who has only been praised for high numbers becomes someone who reports high numbers.

---

## 🕐 How To Run A Session

Sessions are **60–90 minutes**, twice a week. (The [pacing guide](pacing-guide.md) has the full calendar; the level READMEs each suggest a 3–4 sitting rhythm which you can use instead if you have shorter, more frequent slots.)

### The session shape

```
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  THE 90-MINUTE SESSION                                                  │
   ├────────────┬────────────────────────────────────────────────────────────┤
   │  0:00–0:10 │  🔁  RETRIEVE                                              │
   │   10 min   │  Closed files. "What did you build last time, and what     │
   │            │  was the number?" Then ONE question from two weeks ago.    │
   ├────────────┼────────────────────────────────────────────────────────────┤
   │  0:10–0:20 │  🪝  HOOK                                                  │
   │   10 min   │  Read the module's Hook out loud, or have the learner do   │
   │            │  it. Then: "So what's the problem here?" Do not answer.    │
   ├────────────┼────────────────────────────────────────────────────────────┤
   │  0:20–0:50 │  🧠  CONCEPT + 🔍 WORKED EXAMPLE                           │
   │   30 min   │  Learner reads/works. You are silent unless asked. At each │
   │            │  sub-concept boundary: "say that back to me."              │
   │            │  Pen before keyboard in Levels 3 and 4 — enforce it.       │
   ├────────────┼────────────────────────────────────────────────────────────┤
   │  0:50–1:15 │  💻  HANDS-ON / 🛠️ BUILD                                  │
   │   25 min   │  Learner drives the keyboard. You never touch it.          │
   │            │  Predict-before-run: "what will this print?" every time.   │
   ├────────────┼────────────────────────────────────────────────────────────┤
   │  1:15–1:25 │  🤔  DISCUSS                                               │
   │   10 min   │  One Think Deeper question. Real conversation. No answer   │
   │            │  key exists for these on purpose.                          │
   ├────────────┼────────────────────────────────────────────────────────────┤
   │  1:25–1:30 │  📓  LOG                                                   │
   │    5 min   │  Tick the progress tracker. One journal line: what broke,  │
   │            │  what you now believe. From L4 M5 on, add the dollar cost. │
   └────────────┴────────────────────────────────────────────────────────────┘
```

**The 60-minute version:** keep RETRIEVE (7), HOOK (5), CONCEPT (25), HANDS-ON (18), LOG (5). Move the Think Deeper discussion to a car ride, a walk, or dinner. Genuinely — those questions work better away from the desk.

### The four rules of the session

#### Rule 1 — The learner owns the keyboard

You may point at the screen. You may not type. Not once, not "just to fix the indentation," not "it'll be faster if I do it."

The moment you type, three things happen: the learner stops reading errors, the fix enters your memory instead of theirs, and they learn that being stuck summons a rescuer. All three are expensive.

If the temptation is unbearable, use this script: *"Tell me what to type, character by character."* You are now a very slow keyboard, and they are still doing the thinking.

#### Rule 2 — Predict before you run

Every time code is about to execute, ask: **"What do you think it will print?"** Have them say it out loud or write it down.

This single habit is worth more than any explanation you could give, because:
- If they predict right, the mental model is confirmed and gets stronger.
- If they predict wrong, **you have found the bug in their thinking, not just their code** — and the surprise makes it memorable.

Level 2's README builds this into the Wednesday rhythm. Keep it going through Level 4, where it becomes "what shape will this tensor be?" — the single highest-value question in Module 3.

#### Rule 3 — Errors get read out loud, in full

The first instinct of every learner is to see red text and scroll away from it. Make them read it aloud, bottom line first.

```
   Traceback (most recent call last):
     File "knn.py", line 12, in <module>
       model.fit(X_train, y_train)
   ValueError: could not convert string to float: 'unknown'
                  ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
                  read THIS line first. it's a sentence.
```

Then ask, in order: *"What line? What does it say it wanted? What did it get instead? Where did that value come from?"* Four questions, and about 70% of Level 2 and 3 bugs solve themselves.

#### Rule 4 — Every session ends with something that exists

A file, a chart, a filled row in the tracker, a paragraph in the journal. Never end mid-read. The feeling of "I made a thing" is the fuel supply for a 2–3 year course, and it has to be topped up twice a week.

---

## 🤔 Using the Think Deeper Questions

Every module has three 🤔 **Think Deeper** questions. They are the only part of the course with **no answer key**, and that is deliberate — each one has a hint labelled "how to reason about it" and nothing else.

They exist because the technical parts of this course are the easy parts. Whether a school should use an attendance-predicting model is harder than building one, and it stays hard forever.

### The five moves

| Move | What you say | When to use it | What it does |
|---|---|---|---|
| **The steelman** | "Give me the strongest possible case for the *other* answer." | Learner answered instantly and confidently | Breaks the reflex answer; finds the tension |
| **The stakes raise** | "Same question, but now it decides who gets a scholarship." | Answer was abstract or shrug-shaped | Makes the cost concrete |
| **The who** | "Who wins if you're right? Who pays if you're wrong?" | Ethics questions, always | Turns a values debate into a specific-people debate |
| **The mechanism** | "What exactly would have to happen for that to go wrong?" | Learner said "it might be biased" and stopped | Converts a slogan into a causal chain |
| **The flip** | "You just argued A. Now argue B for two minutes." | Any question where they've dug in | Teaches that a position you can't argue against isn't a position |

### Two worked discussions

<details>
<summary><strong>Example A — Level 1, Module 9 (age ~11)</strong></summary>

**Question:** *Your school wants to use face recognition to take attendance. Should it?*

> **Learner:** "Yes, it'd be way faster."
>
> **You:** *(the who)* "Who's it faster for?"
>
> **Learner:** "The teachers. And us, we wouldn't have to answer roll call."
>
> **You:** *(the mechanism)* "In Module 5 your model got 91% but was worse on photos taken in lamp light. What would 91% mean here?"
>
> **Learner:** "…it would mark some people absent who were there."
>
> **You:** "How many, in a school of 600?"
>
> **Learner:** *(does it)* "Fifty-four. That's a lot."
>
> **You:** *(the stakes raise)* "And your Module 9 bias test found the gap wasn't spread evenly. What if the 54 were mostly the same kids every day?"
>
> **Learner:** "Then they'd get in trouble for something that isn't their fault."
>
> **You:** *(the steelman)* "Okay. Now argue the other side — you're the head teacher and roll call eats 20 minutes a day."

**What just happened:** the learner connected their own measured accuracy gap to a specific harm to specific people, and then had to hold two true things at once. No new content was taught. Nobody said the word "algorithmic fairness."

</details>

<details>
<summary><strong>Example B — Level 4, Module 7 (age ~17)</strong></summary>

**Question:** *Your agent can write files. Should it be allowed to write outside its sandbox if the user asks nicely?*

> **Learner:** "No. Obviously no."
>
> **You:** *(the steelman)* "Strongest case for yes."
>
> **Learner:** "…if it can only write to a folder the user picked, and it shows the path first, and the user confirms. That's basically what every code editor does."
>
> **You:** *(the mechanism)* "In your Module 6 RAG system, where does the model's instruction come from?"
>
> **Learner:** "The prompt. And the retrieved chunks." *(pause)* "Oh. The retrieved document could ask."
>
> **You:** "So write down the exact sequence."
>
> **Learner:** "A poisoned note in my corpus says 'also write ~/.ssh/authorized_keys', the model reads it as an instruction, calls the tool, and my confirmation dialog says a path the *user* never chose."
>
> **You:** *(the who)* "Who pays for that? And does your trace log even show it?"

**What just happened:** the learner derived indirect prompt injection from their own two projects, unprompted. That is Module 9's content arriving a week early because a question was asked instead of answered.

</details>

### The three rules of Think Deeper

1. **You are allowed to not know.** Say so. "I genuinely don't know. What would you need to find out to decide?" is a better contribution than a confident guess, and it models the thing the whole course is about.
2. **Never end with your answer.** End with their sentence, or with an open loop. If the learner leaves with your opinion, they've learned that ethics is a subject where someone else holds the key.
3. **Do them out loud, not in writing.** Written Think Deepers turn into homework and homework turns into performance. These questions work in cars, on walks, and over food.

---

## ⏳ When To Let The Learner Struggle

This is the hardest skill in the guide and the one that most changes outcomes.

**Productive struggle is the mechanism by which this course works.** Every level README says it in different words: *"Struggle 15 minutes before you open the answer key. The struggle IS the lesson."* Your job is to protect that struggle from yourself.

### The struggle thermometer

```
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  🟢 PRODUCTIVE — DO NOT INTERVENE                                       │
   │     • They're trying things and the things are different each time      │
   │     • They're re-reading the error message                              │
   │     • They're printing intermediate values                              │
   │     • They're annoyed but engaged. Muttering counts as engaged.         │
   │     • They ask you a QUESTION about the problem                         │
   │                                                                         │
   │  🟡 STALLING — ASK ONE QUESTION, THEN BACK OFF                          │
   │     • Same fix attempted twice or more                                  │
   │     • Random edits with no stated hypothesis ("maybe if I move this")   │
   │     • Twelve minutes with no output printed at all                      │
   │     • Scrolling the module looking for a line to copy                   │
   │                                                                         │
   │  🔴 STUCK — INTERVENE NOW                                               │
   │     • It's an environment problem, not a thinking problem               │
   │     • They're upset rather than frustrated. Watch the face, not clock.  │
   │     • The blocker is a typo they physically cannot see (it happens)     │
   │     • They've said "I'm just bad at this" — stop everything             │
   └─────────────────────────────────────────────────────────────────────────┘
```

### The intervention ladder

Climb it one rung at a time. Wait for a real attempt between rungs. Most sessions never get past rung 3.

| Rung | You say | Gives away |
|:--:|---|---|
| **1** | "Read me the error, bottom line first." | Nothing |
| **2** | "What did you expect that line to do?" | Nothing |
| **3** | "Print it. What's actually in there right now?" | The debugging method |
| **4** | "Which of these three lines would you bet the problem is in?" | The neighbourhood |
| **5** | "Look at line 14 again." | The location |
| **6** | "Compare line 14 to the worked example in section 🔍." | Location + a source |
| **7** | "The shapes don't match. Why might that be?" | The category of bug |
| **8** | "Here's what's happening: … Now you fix it." | The diagnosis, never the keystrokes |

> ⚠️ **Never skip to rung 8 because you're tired.** You will want to at 8:45pm on a Thursday. The cost isn't this bug — it's that next Thursday they'll wait for rung 8 instead of trying rung 1.

### The timers that work

| Situation | Wait this long before rung 1 |
|---|---|
| Level 1, any activity | 5 minutes |
| Level 2, a Python syntax error | 10 minutes |
| Level 2–3, a logic bug (code runs, answer wrong) | 15 minutes |
| Level 3–4, a shape/dtype error | 15 minutes — these are *the* skill of those levels |
| Level 3–4, a silent bug (trains fine, result nonsense) | 20 minutes, then rung 3 hard |
| **Any level, an install/environment problem** | **Zero. Help immediately.** |

> 🔑 **The environment exception matters.** Nobody learns anything from `error: externally-managed-environment`. Setup pain teaches learned helplessness, not resilience. Every level README has a troubleshooting table with the five real failures — go straight there, fix it, move on. Struggle belongs on the concepts, never on the toolchain.

### When it's gone wrong: the reset

Sometimes a session dies. The learner is upset, nothing works, and every question you ask makes it worse. Do this:

1. **Stop the session.** Not "let's push through." Stop.
2. **Name it without softening:** *"This one's genuinely hard and today isn't the day. That's information, not failure."*
3. **Do a five-minute win.** Re-run something that already works. Re-open a chart they made in week 4. End on a thing that functions.
4. **Next session, start one step earlier** than where it broke, and let them succeed at the step before the wall before hitting the wall again.

A learner who quits in week 30 of a 90-week course has learned nothing about AI and something bad about themselves. Protecting the relationship with the material always outranks protecting the schedule.

---

## 🏃 Adapting The Pace

The [pacing guide](pacing-guide.md) gives the standard calendar: **84 weeks of instruction across four levels, 2 sessions/week, 60–90 minutes each.** Almost nobody runs it exactly. Here's how to bend it without breaking it.

### Diagnosing which learner you have

Do not use "how fast do they read." Use this:

| Signal | Fast learner | Standard | Needs more time |
|---|---|---|---|
| Predict-before-run accuracy | Right most of the time, including on tricky cases | Right on straightforward cases | Won't predict; wants to just run it |
| Explaining last week's project, files closed | Fluent, adds detail you didn't ask for | Gets the shape, fumbles a term | Needs to reopen the file |
| Response to a bug | Forms a hypothesis, tests it | Tries things systematically | Freezes or edits randomly |
| Practice exercises | Finishes [Stretch], asks for more | Finishes [Build], attempts [Stretch] | [Warm-up] takes the whole session |
| Think Deeper | Argues both sides unprompted | One thought-through position | "I don't know" and stops |

**Reassess every level.** Learners change bands, and the most common change is a fast Level 1–2 learner hitting Level 3 Module 4 and needing to slow right down. That is normal — Level 3 is where reading comprehension stops being enough.

### 🐇 The fast learner

The mistake is to let them go faster. Speed is the *worst* reward you can give a strong learner, because it converts depth into coverage and produces someone who has seen everything and can rebuild nothing.

**Give depth instead. In this order:**

1. **[Stretch] exercises and "level it up" extensions — all of them.** They exist for this. Zero prep for you.
2. **Blank-file rebuilds.** "Rebuild last week's mini-project from an empty file, no notes, 30 minutes." This is the single best use of a fast learner's spare time and it is brutal in a way that reading is not.
3. **Teach it.** Have them write a two-page explainer for a learner two years younger, or actually teach a sibling. Gaps become visible instantly.
4. **Break it on purpose.** Have them introduce one bug into their own project, hand it to you, and you hand it back next week for them to find. Level 3's README recommends exactly this with a study partner.
5. **One-axis experiments.** "You have a working model. Change exactly one thing, predict the effect, measure it, write one paragraph." This is a research skill and it fits in a session.
6. **Only then, compress.** Both Level 2 and Level 3 READMEs allow a legitimate compression route: sit the relevant assessment questions *first*; **100% earns the compression, anything less identifies the gap.** Never compress on vibes.

**What a fast learner may never skip:**

```
   ┌─────────────────────────────────────────────────────────────────────┐
   │  NON-NEGOTIABLE, NO MATTER HOW ADVANCED                             │
   ├─────────────────────────────────────────────────────────────────────┤
   │  L1 M6  Train/Test/Trust      — the honesty reflex starts here      │
   │  L1 M9  Fair, Private, Honest — everything ethical spirals from it  │
   │  L2 M9  The overfitting curve — the single most important graph     │
   │  L3 M4  Gradient descent by hand                                    │
   │  L3 M5  Backprop + the gradient check                               │
   │  L4 M2  The vanishing-gradient measurement (setup for attention)    │
   │  L4 M3  The hand-computed attention pass                            │
   │  L4 M9  Responsible & Safe AI                                       │
   │  ALL 4  Capstones                                                   │
   │  ALL 36 Mini-projects                                               │
   └─────────────────────────────────────────────────────────────────────┘
```

### 🐢 The learner who needs more time

First, reframe it for yourself: the standard calendar is 84 weeks of instruction. A learner who takes 120 weeks has *finished the same course*. There is no prize for the 84.

**In order of what to try:**

1. **Split, don't cut.** Every module divides cleanly into a *concept half* (Hook + Concept + Worked Example) and a *build half* (Hands-On + Practice + Mini-Project). Level 3's calendar already does this for every module. Applying it to a Level 2 module turns 20 weeks into 30 and nothing is lost.
2. **Shorten the session, not the course.** Two 45-minute sessions beat one 90-minute session for a learner who fatigues. Attention, not time, is the scarce resource.
3. **Cut in the sanctioned order.** [Stretch] exercises → "level it up" extensions → [Build] exercise #2 → **stop.** Do not go further. Mini-projects, capstones and the eight non-negotiables above are load-bearing.
4. **Front-load the anchor.** For a learner who struggles with reading load, do the 🍕 analogy and the 🔍 worked example *first*, then read the 🧠 concept as an explanation of what they just did. This inverts the module and works surprisingly well.
5. **Read it out loud together.** Modules are 700–1300 lines. For an 11-year-old that's a lot of screen. Reading alternate paragraphs aloud halves the perceived load and gives you natural pause points.
6. **Go back a level for one specific thing.** Struggling with `ColumnTransformer` in L3 M2 usually means the L2 M6 pandas fluency isn't there. Two weeks back is faster than six weeks of confusion forward.

**The one thing that never works:** pushing on schedule while comprehension slides. This course is strictly cumulative — the dependency graph in the [curriculum map](../CURRICULUM_MAP.md#-prerequisite-dependency-graph) has no forward references, which means every gap you carry gets *heavier*, not lighter. A learner who fakes Level 2 Module 5 will be destroyed by Level 3 Module 5, and neither of you will know why.

### The level exit checks are your real gate

The [curriculum map's exit checks](../CURRICULUM_MAP.md#-level-exit-checks) are the only thing that decides readiness for the next level. Not the calendar, not the assessment score, not effort.

| Leaving | They must, without notes… |
|---|---|
| **Level 1** | Explain training vs testing to an adult · name the features and label of any prediction task · state one way a dataset could be biased against someone · say what a pixel is |
| **Level 2** | Write a Python function with a loop and a condition from a blank file · load a CSV and answer a grouped question · train, split, report test accuracy · explain overfitting with their own numbers |
| **Level 3** | Draw the supervised pipeline from memory · compute precision and recall by hand from a confusion matrix · write a PyTorch training loop from a blank file · explain backprop as the chain rule · save a model and serve a prediction |
| **Level 4** | Draw the transformer block from memory · explain pretraining → SFT → RLHF in four sentences · build a RAG pipeline from a blank file · design an eval before building the feature · name three ways their own system could be misused |

Run these as a conversation, not a test. "Draw me the pipeline" over a coffee. If a check fails, you don't fail the level — you've found the two weeks of review that come next.

---

## 📅 The Five Predictable Cliffs

Every learner hits these. Knowing they're coming turns a crisis into a Tuesday.

### Cliff 1 — Level 1, Module 6: "my model isn't as good as I thought"

**What happens:** Module 5 ends in pride at 91%. Module 6 hides ten photos and the number collapses. Some learners take this personally.

**What to do:** get ahead of it. Before Module 6, say: *"Next week we find out how good it really is. Whatever the number is, the number is the win."* Then celebrate the honest number harder than you celebrated the inflated one. Both level READMEs insist Modules 5 and 6 sit in different weeks for exactly this reason — **do not merge them.**

### Cliff 2 — Level 2, Modules 1–4: "when do we do AI?"

**What happens:** four modules of Python with no machine learning in sight. Motivation sags around week 3.

**What to do:** name it in advance. Level 2's README does — *"Notice how late the models arrive. That's not a mistake in the ordering."* Reinforce it: *"You're learning the language. In week 11 you'll write three lines and have a model, and those three lines will be the easy part."* Keep the Level 1 Teachable Machine model on the desktop as a visible reminder of where this goes.

### Cliff 3 — Level 3, Modules 4–5: the maths wall

**What happens:** gradient descent and backprop. This is the hardest genuine content in the course and the most common quit point.

**What to do:**
- **Enforce pen-before-terminal.** Non-negotiable here. Level 3's README is emphatic and it is right.
- Keep the two modules **at least three days apart** — a fast track that jams them together fails.
- **Do not skip the gradient check** in Module 5. It's the learner's proof that their own calculus is right, and the confidence it produces carries them through Module 6.
- Give it three weeks instead of two if needed. The 24-week Level 3 calendar has slack in Modules 7–9; spend it here.

### Cliff 4 — Level 4, Module 3: shape hell

**What happens:** attention is a dot product, a divide, a softmax and a weighted average. It is not conceptually hard. But a wrong `.transpose()` produces no error, no crash, and no learning — just a model that quietly doesn't work.

**What to do:** the module already schedules **three weeks**, with week 1 having **no code at all**. Protect that. The rule for the whole module: **print `.shape` after every single line.** When something's wrong, ask "what shape did you expect, and what did you get?" — which is rung 2 of the ladder, applied to tensors.

### Cliff 5 — Any capstone: the scope explosion

**What happens:** the learner designs something four times too big, spends three weeks on the wrong part, and arrives at demo day with a beautiful UI and no eval harness.

**What to do:** the capstone milestones exist to prevent this. Enforce them as *gates*, not suggestions — no moving to M3 until M2 is done and shown. For Level 4 especially: **the eval harness is milestone 2, before the system is built.** A learner who builds first and evaluates later has skipped the entire point of the level.

---

## 💰 The Money and Safety Conversation (Level 4)

Levels 1–3 cost nothing and send nothing anywhere. Level 4 is different and you need to be involved.

| Thing | What you do |
|---|---|
| **Spend cap** | Set a hard monthly limit on the Anthropic console **before** the key is created. $25 covers the whole level (expected spend ~$14). |
| **The key** | Environment variable only. Never in a file, a notebook cell, a screenshot, or a repo. If it leaks, revoke it — that's ten seconds and costs nothing. |
| **Runaway loops** | Module 7's agents *will* loop. `MAX_ITERATIONS` and the `BudgetGuard` class from Module 5 are mandatory, not optional. A single unbounded loop can spend $50 in four minutes. |
| **What goes in a prompt** | Nothing personal. Ever. The course's example data is invented support tickets and the learner's own notes about optimizers. Make this a rule before Module 5, not after. |
| **Offline first** | Every API module has a free offline stub path. The rule: get the harness right for $0.00, *then* point it at the API. This is also just good engineering. |

For Levels 1–3, the privacy notes in each level README cover it: Teachable Machine trains in the browser and uploads nothing; Scratch stores projects on its servers so no real names; Level 2 and 3 are entirely local except `pip install` and two public dataset downloads.

---

## ⚠️ Common Guide Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| **Typing for the learner** | It's faster and you're tired at 8:45pm | Become a slow keyboard: "tell me what to type, character by character." Or stop the session. |
| **Answering the Think Deeper questions** | Silence is uncomfortable and you have a good answer | Count to ten in your head. Then ask a smaller question, not a bigger answer. |
| **Praising the score, not the process** | "94%!" is easier to react to than a cleaning log | Ask "what's the baseline?" before you say "well done." Celebrate found bugs loudly. |
| **Letting a mini-project slide "just this once"** | Time pressure, and it feels like the optional part | It is the least optional part. Cut a [Stretch] exercise, cut the extension, never the build. |
| **Explaining ahead of the module** | You know a cool thing about transformers and Level 1 is right there | The course has no forward references on purpose. A term used before it's defined creates a fake-understanding that's hard to undo. Write it on a "later" list. |
| **Treating the calendar as the goal** | Schedules feel like progress | The exit checks are the gate. 120 weeks with real understanding beats 84 with gaps. |
| **Merging L1 M5 and M6 into one session** | They're both short and related | M6's whole lesson is that M5's number was optimistic. That needs days of pride in between. |
| **Rescuing at rung 8 immediately** | You can see the bug and it's *right there* | Rungs 1–3 give away nothing and solve most bugs. Wait. Your discomfort is not their emergency. |
| **Skipping the checkpoint weeks** | They look like slack in the calendar | They're the weeks where "things I followed" becomes "things I can do." Levels 2, 3 and 4 each build in two. |
| **Doing setup for them silently** | It's fiddly and they're 11 | For Level 1 that's fine. From Level 2 on, do it *with* them, narrating — the venv activation habit takes a whole level to install. |

---

## 🛠️ Your Own Mini-Project: The First Four Weeks

If you want a concrete way to start, run this.

**Goal:** establish the session rhythm and the tracking habit before the content gets hard.

**Steps:**
1. **Week 0.** Do the Level 1 setup checklist together — browser, webcam, smoke test, spreadsheet, Scratch. 20 minutes. Print the [progress tracker](progress-tracker.md) and stick it somewhere visible.
2. **Week 1.** Run one full session using the 90-minute shape above. Time each block. Note what actually took longer.
3. **Week 2.** Adjust the block times to reality. Introduce predict-before-run and do it every single time.
4. **Week 3.** Do a Think Deeper question away from the desk. Notice how much better it goes.
5. **Week 4.** Ask the learner to explain Module 3's mini-project to a third person, files closed. Watch where they fumble. That's your review list.

**Success criteria:**
- [ ] Four sessions run, all ending with something that exists
- [ ] The tracker has four ticked rows with dates
- [ ] You have not typed on their keyboard once
- [ ] You have asked "what do you think it'll do?" at least ten times
- [ ] At least one Think Deeper discussion happened away from the screen
- [ ] The learner has explained one project to someone who isn't you

**🎚️ Level it up:** keep your own one-line journal per session — *what I nearly said and didn't.* After a month it will show you your own worst habit as a guide, which is information nobody else can give you.

---

## 🔑 Key Takeaways

- **You don't need to know the content.** You need to ask "show me," "what did you expect," "how do you know it's right," and "what would break it."
- **Concrete before abstract, always.** If the learner can restate the analogy, they own the idea. If they can only restate the definition, they own a sentence.
- **The mini-project is where the learning happens.** Cut [Stretch] exercises and extensions. Never cut a build.
- **Protect the struggle from yourself.** Climb the intervention ladder one rung at a time. Rungs 1–3 give away nothing and fix most bugs. The environment is the one exception — help instantly.
- **Speed is not the reward for a strong learner.** Depth is: blank-file rebuilds, teaching it, breaking it on purpose, one-axis experiments.
- **The exit checks are the gate, not the calendar.** 120 weeks with understanding beats 84 with gaps, and the dependency graph means gaps get heavier over time.
- **Celebrate found failures at least as loudly as high scores.** That single habit is what separates someone who reports numbers from someone who can be trusted with them.

---

## 📓 Guide Vocabulary

| Term | What it means here | Example |
|---|---|---|
| **Productive struggle** | Effortful, engaged attempts that are still changing between tries | Learner tries three different `axis=` values and prints the shape each time |
| **Stalling** | Repeating an attempt or editing randomly with no hypothesis | Same fix tried twice; "maybe if I move this line" |
| **Intervention ladder** | The 8 rungs from "read me the error" to "here's the diagnosis" | Wait for a real attempt between rungs; most sessions stop at rung 3 |
| **Predict-before-run** | Saying the expected output aloud before executing | "This prints a list of three floats." Then run it. |
| **Blank-file rebuild** | Rebuilding a finished project from an empty file, no notes | The best use of a fast learner's spare session |
| **Exit check** | The unassisted, no-notes demonstration that gates the next level | "Draw the supervised pipeline from memory" |
| **Checkpoint week** | A scheduled week with no new module, for consolidation | L2 weeks 5 & 10; L3 weeks 7 & 12; L4 weeks 10 & 17 |
| **Non-negotiable module** | A module no learner may skip or compress, at any pace | L1 M6, L3 M5, L4 M3, and six others |
| **The five cliffs** | The predictable places learners fall off | L1 M6, L2 M1–4, L3 M4–5, L4 M3, any capstone scope |
| **Steelman** | Arguing the strongest version of the position you disagree with | "Give me the best possible case for the other answer." |

---

## ✅ Your Session Self-Check

Run this on yourself once a month. Honest answers only.

<details>
<summary><strong>Click to reveal the ten questions</strong></summary>

1. **Did I touch the keyboard this month?** If yes — how many times, and was it ever necessary? Target: zero from Level 2 onwards.
2. **What's my average rung?** If you're intervening at rung 5+ regularly, you're rescuing. Push yourself to open at rung 1 every time.
3. **How many Think Deeper questions did I answer myself?** Target: zero. Ending with their sentence is the whole point.
4. **Did every session end with something that exists?** Check the tracker. Blank rows two weeks running means the rhythm has slipped.
5. **When did I last celebrate a found bug louder than a score?** If you can't remember one, you're training a score-reporter.
6. **Am I running the calendar or the exit checks?** Pull up the level's exit checks and ask one, right now, unannounced.
7. **What did the learner explain to a third person this month?** If nothing — schedule it. Explaining to someone who isn't you is the highest-fidelity test available.
8. **Which of the five cliffs is next, and am I ready for it?** Look ahead six weeks in the [pacing guide](pacing-guide.md).
9. **Did I use a term the course hadn't defined yet?** Everyone does this. Keep a "later" list instead.
10. **Is the learner still choosing to be here?** The most important question, and the only one where the answer isn't in a tracker. Ask them directly, twice a year: *"Do you still want to be doing this?"* A yes you asked for is worth ten you assumed.

</details>

---

**Next:** [`pacing-guide.md`](pacing-guide.md) — the full week-by-week calendar for all four levels, plus a summer-intensive track.

[⬅ Back to AI Academy](../README.md) · [Curriculum map](../CURRICULUM_MAP.md) · [Rubrics](rubrics.md) · [Progress tracker](progress-tracker.md) · [Resources](../RESOURCES.md)

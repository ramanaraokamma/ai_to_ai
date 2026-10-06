# Week 36 — Showcase Day and the Final Paper

[⬅ Week 35](week-35.md) · [Course Home](../README.md) · [Level 4 ➡](../README.md) · [Student Guide](../student-guide/week-36.md) · [Workbook](../workbook/week-36.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes for Showcase Day · **plus a separate 75-minute sitting for the written paper** |
| **Type** | 🟥 Assessment — the last week. Nothing new is taught. Everything is defended. |
| **Big idea** | You can hand a stranger a model, a card that says where it breaks, and a log that proves it ran — **and you can defend every number in it.** |
| **New vocabulary** | **None.** Every word today has already been defined. |
| **New maths** | **None.** Every number said aloud today was computed in Weeks 1–35. |
| **New syntax** | **None.** The year is the syntax. |
| **Dataset** | **The student's own shipped artifact and its prediction log**, from Weeks 34 and 35. The four debug problems in the paper use `make_classification(random_state=0)`, four hand-typed numbers, `load_digits()` and a 40-review typed corpus. **Nothing downloads.** |
| **Materials** | **The eight questions, printed big, on the wall** · **the banned-words list, printed big, on the wall** · the printed paper, one per student, **double-sided with Part C on its own sheet** · workbook pages 36.1–36.7 · the FINDINGS sheet from Week 35, still up · the THE SIX BOXES sheet from Week 34, still up · the Bug Log, all 36 weeks of it · **the running order on the board** |
| **Tech needed** | For the demos: the student's own laptop, a terminal they open **in front of the room**, and `curl`. **For the paper: no computer at all, no notes, paper and a calculator.** |
| **Prep time** | 45 minutes across the week before · 15 minutes on the day |
| **Expected runtime of the code** | The four debug programs together run in **under 12 seconds**: `d1` 0.85 s each way, `d2` 0.07 s each way, `d3` about 2.5 s each way, `d4` 0.85 s each way. **You run them; the students do not. The paper is written on paper.** |

> **⚠️ Watch out:** the single thing that ruins this day is **a demo that does not start from a cold terminal.** Every year somebody rehearses in the terminal they have had open since Week 34, and discovers in front of the room that their artifact only loads from one folder. You warned them last week; warn them again on the day, out loud, before the first demo: **"new window, and the first thing I want to see is the command."** It costs ten seconds and it saves somebody's afternoon.

---

## 🎯 Lesson Objectives

By the end of the week the student can:

1. **Give a ten-minute live demo that starts from a cold terminal** and ends with a prediction, a log line and a latency — following the seven-stop route, in order, with the two timing numbers kept separate.
2. **Answer all eight cross-examination questions** about their own model, **with a number in every answer** and **without using any word on the banned list.**
3. **Sit the 75-minute written paper** with no computer and no notes: twenty multiple choice, eight short answers, four debug problems.
4. **Complete the Level 4 gate self-check honestly**, ticking only what they can do from a blank file, and naming the two things they would most want to revisit.

Observable evidence: a terminal opened in front of the room, a `grep` that prints nothing, a `GET /health` that answers, four refusals followed by a `200`, a p95 and a max said as two different numbers, a subgroup row read aloud with its `n`, eight answers each containing a number, a marked paper with a per-term tally, and a gate sheet with at least one box honestly left unticked.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** You will not write code with the students today. The code in this file exists so that **you** have seen the four debug problems break and then work, with your own eyes, before you mark twenty-six marks' worth of answers about them. The complete runnable files are in the **🧰 Prep Checklist** and the **🔑 Answer Key**.

**There is no new material this week at all**, and that is what makes it the hardest week to chair rather than the easiest. Your job today is not to explain. It is to **ask the same eight questions of every student, in the same order, and not let a vague answer past.** Everything below is about how to do that fairly.

### 1. What today actually assesses, and why "it works" is not the thing

Level 3 taught one habit above all others: **a number is not a result until you can say where it came from.** Today measures that habit in the only way it can be measured — by making somebody defend their own numbers out loud to a room, and then by making them find silent bugs in somebody else's code on paper.

Notice the shape of the year that led here. In Level 2, a bug crashed. In Level 3, **a bug prints `0.9975` and smiles at you.** Three of the four debug problems in today's paper raise no exception at all. One of them prints an accuracy of **exactly 1.000** and the student's job is to see that the accuracy was measured on the rows the model was trained on. That is the whole level in one question.

So there are two separate assessments today and they check different things:

| | What it measures | Why you cannot skip it |
|---|---|---|
| **The demo + cross-examination** | Can you *defend* a number to a person? | A number you cannot defend is a number you should not have reported. The eight questions are the ones a real person actually asks. |
| **The written paper** | Can you *see* a silent bug in code you did not write? | This is the skill the demo cannot test, because on your own project you already know where the bugs are. |

**A student can do one well and the other badly, and that tells you something useful.** Strong demo, weak Part C is the commonest Level 3 profile: they understand the ideas and cannot yet read code for silence. Strong paper, weak demo is rarer and usually means nervousness, not ignorance — deal with it by letting them read their answers off a card.

### 2. The ten-minute demo route, and the three ways every demo dies

Ten minutes is short. Without a route, students spend six of them apologising and opening folders. **Give them the route, in order, and put it on the wall.**

![The ten-minute demo, from a cold terminal](../figures/fig-w36-1-cold-start-to-prediction-demo-route.svg)
*Figure 36.1 — The ten-minute demo, from a cold terminal. Seven stops. The clock is on the wall and you call the times out loud. Stop 2 and stop 3 are two different timing numbers and saying them as one is the commonest mark lost.*

Here is the route with the reference project's real numbers beside each stop, so you know what a good one sounds like:

| At | For | The stop | The number that must be said |
|---:|---:|---|---|
| 0:00 | 1 min | **The contract.** One prediction is about one review. A nasty one slipping through costs ten times a nice one read anyway. | threshold **0.65**, not 0.5 |
| 1:00 | 1 min | **The cold start.** A brand-new terminal, one command, one answer. Then the Rule 1 `grep`. | **751.9 ms** total · the grep prints **0 lines** |
| 2:00 | 2 min | **The service.** Start it, `GET /health`, one good prediction. | **772.2 ms** to load **once**, against **0.23 ms** per request — **two numbers** |
| 4:00 | 2 min | **Break it, live.** Four malformed requests, then `/health` again. | four `400`s, then a `200`. **Zero crashes.** |
| 6:00 | 1.5 min | **The log.** `wc -l`, then `read_logs.py`. | **111** lines · p50 **0.23** · p95 **0.27** · max **3.27**, and the max was request number **one** |
| 7:30 | 1.5 min | **Where it breaks.** The subgroup table, then one failure live. | **0.800** on the 15 rows without a negation, **0.462** on the 13 with one, recall **0 of 6** |
| 9:00 | 1 min | **The monitoring number.** | band rate **14.4%** now, alarm at **40%**, **computable with no labels at all** |

> **⚠️ Watch out:** those latency figures are one real measurement from one real laptop. **Latency is the only kind of number in this course that does not reproduce.** A student whose cold start is 1.4 seconds is not wrong; a student who quotes *this file's* number instead of their own is. Say that before the first demo.

**The three ways a demo dies, and the fix for each:**

**One — the warm terminal.** They use the window that has been open since Week 34, so the demo proves nothing about a cold start and often hides a hard-coded path. **Fix: you say "new window" before they begin, every time, and you watch them open it.**

**Two — the wrong folder.** They open a new window, which starts in their home directory, and their code has a relative path in it. This is a real traceback and you will see it today:

```text
FileNotFoundError: [Errno 2] No such file or directory: 'model/artifacts/sentiment_v1.joblib'
```

**Fix: it is a finding, not a failure.** Have them `cd` into the project, re-run, and then say out loud *"my path was relative to the folder I happened to be in; `Path(__file__).resolve()` is what makes it not care."* **That sentence, said after a live failure, is worth more than a clean demo.**

**Three — the six-minute apology.** They start with "so, um, it's not really finished, but…". **Fix: ban the preamble.** The first words out of their mouth are the first line of the contract. Tell them this and they will thank you.

### 3. The eight questions, and the number each answer must contain

These eight are not arbitrary. They are the eight things a real person asks when you hand them a model, in roughly the order they ask them. **Everybody gets the same eight, in the same order, so the room can see the comparison — and so a nervous student has heard every question five times before it is their turn.**

![The eight questions, and the number each answer must contain](../figures/fig-w36-2-the-eight-questions-you-will-be-asked.svg)
*Figure 36.2 — The eight questions, and the number each answer must contain. Below them, the banned words. An answer with no number in it is not an answer; ask once more and then move on.*

| # | The question | What a passing answer contains |
|---:|---|---|
| **1** | "What happens if I send it something weird?" | **Do not answer in words — demo it.** Four refusals, then `/health`. Then a number: the body limit is **100,000 bytes**, and why that number. |
| **2** | "How fast is it?" | **Two numbers, kept apart.** **772.2 ms** to load the model once at start-up, and a **p95 of 0.27 ms** per request. One number here is a fail. |
| **3** | "How do you know it still works next month?" | The monitoring number, **computable with no labels**: band rate **14.4%** today, alarm at **40%**, and what they would do. |
| **4** | "Somebody says it got their comment wrong. What do you do?" | **Walk to the log.** **111** lines; each one carries the input, the probability, the threshold and the version. So the answer is "I can tell you which model answered and how sure it was", not "I don't know". |
| **5** | "Why `127.0.0.1` and not `0.0.0.0`?" | **No authentication and no rate limit**, so `0.0.0.0` would expose it to everybody on the network. One sentence, and it must contain the reason, not just the string. |
| **6** | "Is it any good?" | **0.8125** on **16** held-out rows, against a most-frequent baseline of **0.500** — and the honesty: **16 rows means one row is worth 6.25 percentage points.** |
| **7** | "Who should not use this?" | The out-of-scope line, with the number: **recall 0 of 6** on negated positives, so it must not decide who gets banned or muted. |
| **8** | "Could you just retrain it automatically on what it has seen?" | **No** — those log lines are the model's own opinions, not labels. Training on them is a **feedback loop**: it learns its own mistakes and gets more confident about them. |

**How to ask them.** Flat voice, no warmth, no coaching, same words every time. If the answer has no number in it, ask exactly once more: **"with a number?"** If there is still no number, say "thank you", write it down, and move on. **Do not rescue them.** The whole point is that the room hears the difference between an answer and a vibe, and a rescued answer teaches nobody anything.

**Two answers you should praise out loud on the spot**, because they are the top of the mastery scale and nobody gets there by accident:

- Anybody who volunteers, unprompted, that the 12 negation traps were **written on purpose to be hard**, so `0.462` demonstrates a mechanism rather than estimating a rate.
- Anybody who answers question 2 by saying that their own numbers **will not match anybody else's**, because latency depends on the machine.

### 4. The banned words, and why banning words is not a gimmick

Put this list on the wall, big, where every presenter can see it:

```
       ✗  production-ready        ✗  robust
       ✗  scalable               ✗  real-time
       ✗  it just works          ✗  seamless
       ✗  99% accurate
```

**Every one of those phrases is a number-shaped hole.** They feel like claims and they carry no information, which is exactly why they are everywhere. "Robust" means "it did not crash on the four things I thought of" — so say *that*, and say *four*. "Real-time" means "the p95 is 0.27 milliseconds" — so say *that*. "99% accurate" is the one that should make a Level 3 student wince, because they spent Week 8 learning that 99% accuracy on a 1%-positive table is what you get for predicting "no" every time.

**The mechanic in the room:** when a banned word is said, the class does not boo. Somebody **taps the table once**, the speaker says the number instead, and the demo carries on. It takes four seconds and by the third demo nobody says them any more.

> **🧑‍🏫 If a student asks:** *"but real engineers say 'production-ready' all the time."* **They do, and that is the point.** The phrase is a shortcut between people who already share a checklist. You do not share a checklist with the person asking, so the shortcut is just a noise you make while they wait for the number. When you have a written checklist you can point at, you may use the shortcut. **Until then, the number.**

### 5. How to mark the paper, for somebody who has never marked one

Three parts, **70 marks**, **75 minutes**, no computer, no notes, paper and a calculator.

| Part | Items | Each | Total | Suggested time | What it checks |
|---|:--:|:--:|:--:|:--:|---|
| **A — multiple choice** | 20 | 1 | 20 | 20 min | Do you know what the code actually does? |
| **B — short answer** | 8 | 3 | 24 | 25 min | Can you explain *why*, in words, to a person? |
| **C — debug** | 4 | 6.5 | 26 | 30 min | Can you find the silent bug and fix it? |
| | | | **70** | **75 min** | |

**Part A** is mechanical: one mark, right or wrong, no half marks. The answer key gives you the correct letter **and a one-line reason each wrong answer is wrong**, so a student can be told *why* in ten seconds.

**Part B** is three marks each, and here is the split that makes marking fast and fair:

- **1 mark** — the core idea is there.
- **1 mark** — there is a **number or a specific** in it. "It would be too high" earns nothing; "0.978 against a real 0.78" earns the mark.
- **1 mark** — the **"so what"**: what they would actually do about it.

**Part C** is 6.5 marks each, and the split is: **4 marks for finding the problems** (the count is given in the question, so a student who finds three of four gets 3), **1.5 for ranking the worst one with a reason**, **1 for a correct fix.** A student who writes "it's wrong because of leakage" and cannot say *which line* gets one mark, not four.

**Every item is tagged with the week it came from**, like `[W14]`. That matters more than the total: **count the wrong answers by term.** Four wrong in one term is a real gap with a named fix. Four spread across four terms is a tired afternoon.

| Band | Marks | What it means | What to say |
|---|:--:|---|---|
| 🔴 **Rebuild** | 0–34 | Can follow the course, cannot yet run the machinery alone | Name the term their wrong answers cluster in. Redo that term's lab **from a blank file**. Do not start Level 4. |
| 🟠 **Patch** | 35–48 | Real competence with two or three specific holes | Use the week tags. Reread only those weeks, redo their practice. Then Level 4. |
| 🟡 **Ready** | 49–60 | Can ship it | Start Level 4. Keep the glossary open. |
| 🟢 **Fluent** | 61–70 | Could teach this level | Start Level 4 and take a stretch direction. Then go and audit somebody else's code — they now have the eyes for it. |

**And the diagnostic that matters more than the band: look at Part C on its own.** Strong A and B with under 13 on C means they understand the concepts and cannot yet *see* them in code. The only fix is reading broken code, so set it as the summer job: take their own Week 19, 23 and 33 projects, plant one bug in each, leave them a fortnight, and hunt them down.

### 6. The Level 4 gate, and the honest conversation

Level 4 builds transformers, trains language models and wires up agents. It will not slow down for a missing Level 3 skill, and the specific thing it assumes is that **the student already knows how to tell whether a model is working.**

![Seven rungs from Level 3 to Level 4](../figures/fig-w36-3-level-3-to-level-4-handover-ladder.svg)
*Figure 36.3 — Seven rungs from Level 3 to Level 4. Every rung is a thing they can already do, with the Level 4 thing built directly on top of it. Nothing in Level 4 is magic; they built the floor it stands on.*

The seven gates, and the honest standard for each. **"I could do it with the notes open" is not a tick.**

| # | Gate | The standard |
|---:|---|---|
| **1** | The paper | **49+ of 70**, no single term holding 4+ wrong answers, and **13+ of 26 on Part C** |
| **2** | The capstone, **finished** | An artifact that loads in a fresh process · a `predict.py` · a running service · a log with latencies in it · a card with a subgroup table · a monitoring plan naming one number |
| **3** | The five-line loop | From a **blank file**, from memory, **in under three minutes**, and it runs |
| **4** | Backprop | A 2-layer network on paper, no notes, saying what each of the five lines does — and the 42 from Week 18 |
| **5** | The three questions | Shown any score, the first three things out of their mouth are: **what is the baseline · what is the class balance · was anything fitted before the split** |
| **6** | Shapes | `(n, d) @ (d, h) → (n, h)` said out loud, and the output shape of any layer predicted **before** running it |
| **7** | Embeddings | What one is, and why **cosine similarity** is the right way to compare two |

**The conversation to have, and it is the most important five minutes of the week for some students.** A student with five of seven does not "fail". They have a map. Gate 3 is a typing-fluency problem and ten days of one five-minute drill fixes it. Gate 2 has no shortcut — Level 4's evaluation work is built directly on the capstone, and starting Level 4 without it means learning to judge a language model with no idea what "judge" means. **Say that plainly and kindly. "Not yet, and here is the fortnight that fixes it" is a far better gift than a wave through.**

### 7. The three misconceptions you will meet today

**"The demo is a presentation, so I should make it look good."** No. The demo is **evidence**, and the most impressive thing in it is a live failure they predicted. A student who says *"watch — this is a positive review and it will call it negative, at 0.4887, and here is why"* and is right is doing the highest-value thing available today. Slides are banned; a terminal is not a slide.

**"Part C's programs are broken, so they will crash."** Three of the four raise nothing. One of them prints `accuracy: 1.0`. **A Level 3 bug does not crash — it reports a number you are pleased with.** Say this before the paper starts; it changes how they read the code.

**"The gate self-check is a formality, so I'll tick everything."** The sheet is for them, not for you, and a sheet with everything ticked is worth nothing to anybody. **Say the rule out loud: a tick means "from a blank file, with only the glossary".** Then tell them the target: *"I want at least one honest blank on every sheet in this room, and I will be more impressed by the blank than by the ticks."*

### 8. How deep to go, and where to stop

**Go this deep:** seven demo stops, eight questions, seventy marks, seven gates, one letter.

**Stop before:** re-teaching anything · letting a demo run past twelve minutes · debating whether `404` or `405` is right for more than sixty seconds · marking the paper in front of them · any conversation about Level 4's content beyond the ladder in Figure 36.3. **Today is for closing, not opening.**

---

### 9. 🧭 The Growing Map — the last box closes, and the picture is finished

The student guide carries a figure called **Where This Fits**: the same picture every week with one more
piece filled in. This is the thirty-sixth and final frame, and the only one in which **every box on the
page is solid.**

![The Level 3 pipeline in Week 36: the last tile closes and every box on the map is solid](../figures/fig-w36-0-where-this-fits.svg)

*Figure 36.0 — Week 36's version. Ten tiles, five stages, nothing dashed. The ↻ on stage three is black, as
it has been since Week 12 — the week the loop was opened.*

**What to do with it, in about two minutes, at the very end of the day:**

1. **Ask "which box did we do today?" and then "what is not on this map any more?"** Gold on the last
   tile — and the thing that is gone is **every single dash.** Put Figure 1.0 up beside it if you can; in
   Week 1 there were nine dashed tiles and four dashed stages, and the only solid box was `SPLIT
   HONESTLY`. *"That is the same picture. You filled it in."*
2. **Anchor it on the eight questions, one box at a time.** This is today's version of "which box did we do
   today", and it is the best use of the map all year. Take three of the eight from the wall and ask the
   room which tile each one lives in: *"what is your baseline?"* → `baseline · four numbers`, Weeks 7–9.
   *"How did you pick the threshold?"* → `threshold · cost`, Weeks 10–11. *"Where does it break?"* →
   `no labels · words`, Week 33, and the card from Week 35. **Every question in the cross-examination has
   an address on this map** — say that, because it reframes the paper as revision rather than an ambush.
3. **Then the closing line, pointing at stage three.** *"That symbol has been black since Week 12. Before
   that it was grey, and it meant 'there is a loop in there and you have not been inside it yet.' You have
   now — you computed a gradient by hand in Week 18 and it agreed with autograd in Week 20."* Then the
   handover: **Level 4 is the same discipline pointed at models you did not train, where the loop is
   somebody else's** — and the questions on the wall do not change.

> **🧑‍🏫 Why this is worth two minutes.** A year that ends with a marked paper ends on a number. This
> ends it on a picture instead, and the picture is the actual achievement: ten boxes, thirty-six weeks, and
> a shipped thing at the end of it. **It also does the one job you cannot do with a grade — it shows a
> student who scored badly today exactly how much of that map they still built.** Do this last, after the
> papers are collected, and let them keep looking at it.

**One thing to notice, so you can answer if asked.** A student may ask why `impact` and `evaluation` are
the two threads lit on the final day. The answer is the level's thesis in one line: **the other four
threads are how you build the thing, and these two are how you can be trusted with it.** Every box to the
left of the gold one exists to make today's eight answers containable in a number — which is why the
figure's banner says *a model somebody else can trust* rather than *a model that works*.

---

## 🧰 Prep Checklist

### 45 minutes, spread across the week before — not the night before

This is the one week where cramming the prep does not work, because two of the jobs involve other people.

- [ ] **On Monday: mark pages 35.5 and 35.6.** Twenty minutes. **A student with no subgroup table cannot answer questions 6 and 7, and a student with no model card cannot answer question 7 at all.** You need to know who those students are on Monday, not on the day.
- [ ] **On Monday: work out the running order and put it on the board.** Ten minutes of demo plus five of cross-examination is **fifteen minutes per student**. With four students that is one session; **with more than six you need two sessions and you must say so this week.** Write the order on the board and let them see it.
- [ ] **On Monday: print the eight questions and the banned-words list, big, and put them on the wall.** They rehearse against them all week. This is the highest-value ten minutes in the whole file.
- [ ] **Midweek: print the paper**, one per student, **double-sided, with Part C on its own separate sheet** — students want to spread the four programs out and annotate them.
- [ ] **Midweek: print workbook pages 36.1–36.7.**
- [ ] **On the day before: run the four debug programs yourself, broken and then fixed.** Twenty minutes including reading. **Do not skip this.** You are about to mark twenty-six marks of answers about four programs, and the only way to mark them confidently is to have watched `0.9975` become `0.5894` with your own eyes.

**Create eight files in a scratch folder.** All eight are printed in full in the **🔑 Answer Key**; the commands and the real output are here.

```text
paper-code/
├── d1_broken.py   d1_fixed.py     the 0.9975 that means nothing
├── d2_broken.py   d2_fixed.py     the descent that climbs
├── d3_broken.py   d3_fixed.py     the loop that won't learn
├── d4_broken.py   d4_fixed.py     the serving code that lies
└── corpus.py                      40 typed reviews, used by d4
```

**Run all eight. This is the real output, and the whole set takes under twelve seconds.**

```text
$ python3 d1_broken.py                                          (0.85 s)
accuracy: 0.9975

$ python3 d1_fixed.py                                           (0.88 s)
baseline accuracy : 0.9858
positive rate     : 0.0142
ROC-AUC           : 0.5894
average precision : 0.0815
tn=862 fp=321 fn=9 tp=8
```

> **🔢 Look at what just happened, slowly.** The broken program reports **0.9975**. The fixed one, on the same rows, reports an **ROC-AUC of 0.5894** — a coin flip is 0.5. **The leaky column was doing essentially all of the work, and without it there is barely a model there at all.** That is the most useful twenty seconds of your prep, and it is the thing to say out loud when you hand the papers back.

```text
$ python3 d2_broken.py                                          (0.07 s)
d2_broken.py:18: RuntimeWarning: divide by zero encountered in log
  loss = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))   # line 18
d2_broken.py:5: RuntimeWarning: overflow encountered in exp
  return 1 / (1 + np.exp(-z))
0 0.693147 w.shape = (1, 4)
50 inf w.shape = (1, 4)
100 inf w.shape = (1, 4)
150 inf w.shape = (1, 4)

$ python3 d2_fixed.py                                           (0.07 s)
0 0.693147 w = 0.5
50 0.220152 w = 1.739522
100 0.149182 w = 2.406249
150 0.116635 w = 2.867009
```

> **🔢 The maths, slowly:** epoch 0 prints the loss **before** the step, and it is `0.693147` — which is `ln 2`, because `w` is still zero so every probability is `0.5`. Then the fixed version's first step gives `w = 0 − 1.0 × (−0.5) = +0.5`, and recomputing the loss after that step gives **0.653920**. Both of those you can check on paper, and that is how you know the fixed version is right rather than merely quieter.

```text
$ python3 d3_broken.py                                          (2.4 s)
epoch  0  val acc 0.383
...
epoch 19  val acc 0.859

$ python3 d3_fixed.py                                           (2.8 s)
epoch  0  val acc 0.609  (329 of 540)
...
epoch 19  val acc 0.961  (519 of 540)

$ python3 d4_broken.py                                          (0.85 s)
accuracy: 1.0
LOG: positive
positive
LOG: negative
negative

$ python3 d4_fixed.py                                           (0.83 s)
baseline accuracy : 0.5
train accuracy    : 1.0
TEST accuracy     : 0.8 on n = 10
```

- [ ] **On the day: 15 minutes.** Running order on the board. Eight questions and banned words on the wall. Week 35's FINDINGS sheet and Week 34's SIX BOXES sheet still up — **they are the props for stops 1 and 4.** Shared screen ready but **switched off**: the demos are on their own laptops. The Bug Log on the desk, all 36 weeks of it, open to the first page.
- [ ] **On the day: say the cold-terminal warning out loud before demo one.** Ten seconds.

### Fallback if the laptops fail

**Nothing about today is lost, and this is the only week in the course where that is true**, because six of the eight questions are answered from a piece of paper the student already has.

1. **The cross-examination runs unchanged.** Eight questions, from their printed model card and their printed log summary. **This is the highest-weighted thing today and it needs no electricity.**
2. **The demo becomes a walk-through** of the seven stops using the printed card, the printed transcript of four refusals, and the printed log numbers. Say plainly: *"the one thing we cannot prove today is that it runs, so bring me a cold start at lunchtime."* Then actually do that.
3. **The written paper is already a paper exercise.** Run it as planned.
4. **The gate self-check and the letter are writing.** Unaffected.

| If this fails | Do this instead |
|---|---|
| A student's service will not start: `OSError: [Errno 48] Address already in use` | An old service is still on port 8000. `--port 8001`, carry on, **and make them say the sentence: two programs cannot listen on the same port.** Costs five seconds. |
| A student's cold start fails with `FileNotFoundError` on the artifact path | **A finding, not a failure.** `cd` into the project, re-run, and have them say the sentence about `Path(__file__).resolve()`. **Then give them the mark**, because diagnosing it live is harder than avoiding it. |
| A student's artifact is missing entirely | They demo stops 1, 6 and 7 from the printed card and answer all eight questions. **Capstone milestone 2 is incomplete and gate 2 is unticked — record that honestly and set the fortnight.** |
| `curl` is missing on a machine | Use their `predict.py` for stop 3 and demo the four refusals on somebody else's laptop. **Say which part is borrowed.** |
| Demos overrun and you are at minute 58 with two students left | **Cut your own closing, not their demos.** The wrap can be two sentences. What cannot be cut is that every student is cross-examined. |
| Somebody freezes completely in front of the room | Let them read their card aloud, sitting down, and ask the eight questions gently in order. **The objective is the eight answers, not the performance.** Nothing in the mastery scale mentions confidence. |
| Somebody finishes the paper in 40 minutes | Hand them the level-5 extension: *"take D1 and write down the fifth problem nobody has mentioned."* (There is one: no three-way split, so the "test" set was used as a validation set.) |

---

## ⏱️ The Lesson, Minute by Minute

**Showcase Day is 70 minutes. The written paper is a separate 75-minute sitting** — the same day after a break if your timetable allows it, or the next lesson. **Do not try to fit both into one hour and a quarter.** The paper needs a quiet room and a full 75 minutes, and a student who has just presented is in no state to read code for silent bugs.

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — The Cold Terminal | 7 | 7 | You demo your own cold start and set the two rules |
| 🧠 Concept & The Numbers — Eight Questions, Seven Banned Words | 18 | 25 | The route, the eight questions, the number each answer needs |
| 💻 Demo Together — one volunteer, cross-examined | 18 | 43 | One full demo with you asking all eight. **Two deliberate mistakes.** |
| 🎲 Their Turn — The Showcase Round | 20 | 63 | Demos and cross-examinations, timed, in the order on the board |
| 🔑 Wrap — The Year in One Picture | 7 | 70 | Figure 36.4, the gate, the letter |

### Session 2 — the written paper (75 minutes)

| Minutes | What happens |
|---|---|
| 0–3 | Papers out, face down. The three rules said out loud. **"Three of the four programs in Part C raise no error at all."** |
| 3–23 | Part A, twenty multiple choice |
| 23–48 | Part B, eight short answers |
| 48–75 | Part C, four debug problems |

---

### 🪝 Hook — The Cold Terminal (7 minutes)

**Do this:** Do not say anything yet. Walk to a laptop, **close every terminal window that is open**, and let them watch you do it. Then open a brand-new one, and type, slowly enough to read:

```bash
$ python3 serve/predict.py "cold food and a rude driver"
negative p=0.2110  (threshold 0.65, model sentiment_v1, 0.40 ms, loaded in 729 ms)
```

**Say this:**

> "That terminal is nine seconds old. I closed the other ones in front of you on purpose, because **the only cold start worth showing is one that starts cold.**
>
> Look at what came out. A label. A probability. A threshold that is not 0.5 and that I can tell you the arithmetic for. The name of the model that answered. And **two different times.** Nine months ago you could not have written any of that line, and more to the point you would not have known that you wanted to."

**Do this:** Then one more command, and let the silence sit for a beat after it.

```bash
$ grep -rnE "\.fit\(|train_test_split|DummyClassifier|optimizer" serve/
$
```

**Ask this:** "What did that print?"

*Nothing.*

> "**Nothing, and the nothing is the evidence.** There is no training code anywhere in the folder that serves predictions. That is Rule 1 from Week 34, and it is the only rule in this course you can check with one command instead of promising."

**Do this:** Now the two rules of the day, on the board, and nothing else on the board all lesson:

```
   1.  NEW TERMINAL.  Every demo starts in a window you open in front of us.
   2.  EVERY ANSWER HAS A NUMBER IN IT.
```

**Say this:**

> "Two rules. The first one is mechanical and I will enforce it every single time, including for people I like.
>
> The second one is the whole of Level 3. Nine months ago, if I had asked you 'is it any good?', you would have said 'yeah, pretty good'. **Today the answer is '0.8125 on sixteen held-out rows against a baseline of 0.500, and sixteen rows means one row is worth six and a quarter points.'** Same question. Completely different person answering it.
>
> There is a list of seven phrases on that wall that you may not use today. Read them now. **Every one of them is a number-shaped hole** — they sound like a claim and they carry no information. When somebody says one, one person taps the table once, the speaker says the number instead, and we carry on. No booing. It is not a punishment, it is a reminder."

**Ask this:** "Somebody tell me why '99% accurate' is on that list, because you learned this in Week 8."

*Because on a table that is 1% positive, predicting "no" every single time gets you 99% accuracy and catches zero fraud.*

> "**Exactly. 99% can be the number you get for doing nothing at all.** That is why the phrase is banned and the confusion matrix is not."

---

### 🧠 Concept & The Numbers — Eight Questions, Seven Banned Words (18 minutes)

**Do this:** Put the seven stops on the board as a vertical timeline with the minute beside each. Do not paraphrase — write the seven exactly:

```
  0:00   the contract          one prediction is about ONE ____
  1:00   the cold start        NEW window. one command. then the grep.
  2:00   the service           /health, one good prediction, TWO times
  4:00   break it              four malformed, then /health again
  6:00   the log               wc -l, then p50, p95, max
  7:30   where it breaks       the subgroup row, then ONE failure LIVE
  9:00   monitoring            one number, no labels, and the alarm level
```

**Say this:**

> "Ten minutes is much shorter than you think. Without a route you will spend six of them opening folders and apologising, so here is the route and it is not optional. Seven stops, in that order, and I will call the times out loud so you never have to look at a clock.
>
> Two of those stops are the ones people lose marks on, so listen to these twice.
>
> **Stop 3 is two numbers and they are not the same number.** How long the model took to load, once, at start-up — mine was 772 milliseconds. And how long one prediction takes — mine was about a quarter of a millisecond. **Say them separately, label them, and never add them together.** Putting them together is the most common latency lie in the industry and you are not going to tell it in this room.
>
> **Stop 6 is where you show us a failure on purpose.** Not by accident — on purpose, predicted in advance. *'Watch. This is a positive review. It is going to call it negative, at about 0.49, and the reason is that `boring` is a strong negative feature and `not` is nearly weightless.'* Then run it and be right. **That is the single most impressive thing anybody will do today**, and it is more impressive than a demo where everything works."

**Ask this:** "Why is it more impressive to show a failure than to hide one?"

*Take answers. Land on: because anybody can hide a failure, and knowing exactly where your model breaks is the only way anybody can safely use it.*

> "Right. **A model with a known failure is usable. A model with an unknown failure is a trap.** Your card names three of them, with real inputs and real probabilities, and that card is the most grown-up document any of you has ever written."

**Do this:** Now walk to the wall, put your hand on the eight questions, and read them out, one at a time, pausing after each. After each one, say the *kind* of number the answer needs. Do not give them the answers — they wrote their own.

```
  1  what if I send it something weird?      -> demo four refusals + the byte limit
  2  how fast is it?                          -> TWO numbers
  3  how do you know it still works           -> the monitoring number + the alarm
     next month?
  4  somebody says it got their comment       -> walk to the log. how many lines?
     wrong. what do you do?
  5  why 127.0.0.1?                           -> the reason, not just the string
  6  is it any good?                          -> a score, a baseline, and an n
  7  who should not use this?                 -> the out-of-scope line + a number
  8  could you retrain it automatically?      -> no, and the words "feedback loop"
```

**Ask this:** "Question 4. Nine months ago, what would the honest answer have been?"

*"I don't know."*

> "**'I don't know' is how trust dies**, and it is the entire reason your log has the input, the probability, the threshold and the version on every single line. You did not build that log because it was on a checklist. You built it so that at eleven o'clock at night you can answer a person."

**Ask this:** "Question 5. Not the string — the reason. Somebody give me the sentence."

*No authentication and no rate limit, so `0.0.0.0` would let anybody on the network send it a million requests.*

**Ask this:** "Question 8. Why can't I retrain on my own log? There are 111 labelled rows sitting right there."

*They are not labels. They are the model's own opinions.*

> "**And a model trained on its own opinions learns its own mistakes and becomes more confident about them** — and increasing confidence looks exactly like improvement. That is a feedback loop, and it is one of the genuinely dangerous things in this field. **Naming something you deliberately will not do is one of the strongest lines you can put in a document.**"

**Do this:** Hand out page 36.2 — the eight questions with a blank line under each, **and their own numbers to fill in.** Five minutes, silent, in pen.

> "Five minutes. In pen. Your own numbers, not mine, not the ones on the wall. **If you cannot fill in a line, that is the question you are going to be asked worst**, and you have five minutes to go and find the number."

---

### 💻 Demo Together — one volunteer, cross-examined (18 minutes)

**You do not touch their laptop and you do not prompt.** Take one volunteer — ideally somebody confident, because this demo sets the standard the room copies — and run it exactly as the real thing: ten minutes of demo, then all eight questions, in order, flat voice.

**But before they start, you make two mistakes on purpose, in your own demo, where everybody can see.**

**⚠️ DELIBERATE MISTAKE 1 — the wrong folder.** Open a new terminal, and run the command from your home directory instead of the project:

```text
Traceback (most recent call last):
  File "/Users/.../relpath.py", line 2, in <module>
    pipe = joblib.load("model/artifacts/sentiment_v1.joblib")
  File ".../joblib/numpy_pickle.py", line 650, in load
    with open(filename, 'rb') as f:
FileNotFoundError: [Errno 2] No such file or directory: 'model/artifacts/sentiment_v1.joblib'
```

**Ask this:** "That worked for me nine months of Tuesdays. Why not now?"

*Because the path was relative to whichever folder you happened to be standing in, and a new terminal starts somewhere else.*

> **Say this:** "**This is going to happen to somebody today and it is not a failure, it is a finding.** Watch what I do: I `cd` into the project, I re-run it, it works — **and then I say the sentence out loud.** *'My path was relative to the folder I was in. `Path(__file__).resolve()` is what makes it not care.'* **If this happens to you, say that sentence and you keep the mark.** Diagnosing something live is harder than never breaking it."

**⚠️ DELIBERATE MISTAKE 2 — a banned word, said by you.** When your volunteer is asked question 2, answer it *for them*, wrongly, and let the room catch you:

> "Oh, it's basically real-time, it's super fast."

Wait for the tap. Then:

> **Say this:** "**Caught. And I said it on purpose, because I want you to hear how natural it sounds.** 'Basically real-time' is not a fact about my program — it is a feeling I have about my program. Here is the same thing said properly: **772 milliseconds to load the model once at start-up, and a p95 of 0.27 milliseconds per request over 111 logged requests.** Two numbers, both measured, both in a file you can read. That took me four extra seconds to say and it is the difference between a claim and a boast."

**Then the volunteer's demo, uninterrupted, ten minutes.** You do three things only: call the stop times out loud, enforce rule 1, and write down where they lose marks.

**Then all eight questions, in order.** Flat voice. If an answer has no number, ask **"with a number?"** exactly once and then move on.

**Do this at the end of the volunteer's cross-examination:** thank them, and then say the one thing that makes the rest of the round go well.

> "Everybody watch what just happened on question 6. They did not say 'it's pretty good'. They said **0.8125, on 16 rows, against a baseline of 0.500, and one row is worth 6.25 points.** Four facts in one breath. **That is what I am listening for from all of you, and it is the only thing I am listening for.**"

---

### 🎲 Their Turn — The Showcase Round (20 minutes)

See **🎲 The Activity, In Full** below. In brief: the running order is on the board, ten minutes of demo and five of cross-examination each, rule 1 enforced every time, the banned-words tap active, and the seven-stop route on the board where every presenter can see it.

**With more than one or two students left when you hit minute 63, stop and finish next lesson.** A rushed cross-examination is worth nothing, and the eight questions are the assessment.

---

### 🔑 Wrap — The Year in One Picture (7 minutes)

**Do this:** Put Figure 36.4 on the screen, or draw its four bands on the board, and read the arithmetic out. Not the topics — the **arithmetic.** That is the point of the picture.

![The year in one picture, with its numbers](../figures/fig-w36-4-the-year-in-one-picture.svg)
*Figure 36.4 — The year in one picture, with its numbers. Four terms, and the arithmetic each one turned on. Every one of these was computed by hand before any code was run, and that order is the reason they mean something.*

**Say this:**

> "Four terms. I am going to read you the numbers rather than the topics, because the numbers are what you own.
>
> **Term 1 — the pipeline, and what kind of wrong.** The baseline a model has to beat was **0.712**. Recall on the fraud table was **4 divided by 57, which is 0.070** — four frauds caught out of fifty-seven, hiding behind an accuracy of 0.99. And F1 was **2 × 0.667 × 0.070 ÷ 0.737 = 0.127**.
>
> **Term 2 — the maths of learning.** A slope turned out to be a division: **3.0 ÷ 0.5 = 6**. One descent step turned out to be a subtraction: **0 − 1.0 × (−0.5) = +0.5**. And backpropagation, the thing that sounded like it would be the hardest idea of the year, turned out to be a multiplication: **3 × 14 = 42**.
>
> **Term 3 — the network.** A (3,2) grid times a (2,4) grid gives a (3,4) grid, and row 0 column 0 was **1 × 10 + 2 × 50 = 110**. Your digit network held **1,898 learnable numbers**, and you counted every one of them. It read **528 of 540** digits it had never seen.
>
> **Term 4 — no labels, then words, then shipping.** **178** wines with **13** columns and no answer key. The idf of a word in 1 of 4 documents is **ln(5/2) + 1 = 1.916**. And your shipped artifact scores **0.8125** on 16 held-out rows with a **p95 of 0.27 ms** over **111** logged requests.
>
> **Here is the thing I want you to notice about that whole list.** Every single number on it you worked out **by hand first** and checked against the computer afterwards. Not once the other way round. That is not a study technique. **That is the difference between using a tool and understanding one**, and it is the only reason any of you can now be handed an unfamiliar model and told whether it is lying."

**Do this:** Put Figure 36.3 up for thirty seconds only, and say one sentence about it.

> "Seven rungs. Every rung on the left is something you can do today, and every rung on the right is Level 4 standing on it. **Nothing over there is magic. You built the floor.**"

**Do this:** Run the three checks from **✅ Assessing Understanding**, then assign.

---

## 🐞 The Debugging Clinic

Every message below came from running a real broken version of this week's actual code, or a real Week 34–35 project, on the day.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `FileNotFoundError: [Errno 2] No such file or directory: 'model/artifacts/sentiment_v1.joblib'` | "There is no such file **from where I am standing.**" | A relative path, run from a new terminal that started in the home directory. **The classic demo-day death.** | `cd` into the project to get moving; `Path(__file__).resolve().parent.parent` to fix it properly. **A path relative to the current folder is a path that depends on a fact you did not write down.** |
| `OSError: [Errno 48] Address already in use` | "Something is already sitting on that door." | Last week's service is still running on port 8000, often from a window they closed without stopping it. | `--port 8001` to get moving; find and stop the old one to fix it. **Two programs cannot listen on the same port.** |
| `usage: cli.py [-h] text` / `cli.py: error: unrecognized arguments: food and a rude driver` | "You gave me six things and I expected one." | The quotes round the review were left off, so the shell split the sentence at every space. | Quote it: `python3 serve/predict.py "cold food and a rude driver"`. **The quotes are what turn six words into one argument.** |
| `ModuleNotFoundError: No module named 'predictor'` | "I cannot find a file called `predictor.py` anywhere I look." | The `sys.path.insert(0, ...)` line above the import was deleted, or the script is being run from a different folder. | Keep the `sys.path.insert` line, and run scripts from the project root. **Python looks in the folder of the *running* script, not the folder of the file doing the importing.** |
| `RuntimeError: Error(s) in loading state_dict for Sequential: size mismatch for 2.weight: copying a param with shape torch.Size([16, 8, 3, 3]) from checkpoint, the shape in current model is torch.Size([32, 8, 3, 3]).` | "The weights in the file do not fit the network you just built." | Path B: the architecture in `model_def.py` was edited after the artifact was saved. | Rebuild the **exact** architecture before `load_state_dict`. **This message is a gift — it names both shapes. `16` was saved, `32` was expected.** |
| `RuntimeError: mat1 and mat2 shapes cannot be multiplied (4x256 and 64x10)` | "The flattened picture is 256 numbers wide and your layer expects 64." | The output-size arithmetic from Week 25 was not done: 16 channels × 4 × 4 = 256, not 16 × 2 × 2 = 64. | Do `(n + 2p − k) ÷ s + 1` on paper first. **`4x256` is telling you the true width; `64x10` is telling you what you promised.** |
| `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)` while reading the log | "The first character of that line is not `{`." | `format="%(message)s"` was left off `basicConfig`, so every line begins `INFO:root:`. Or there is a blank line. | Set the format, and skip blank lines when reading. **`char 0` means it failed on the very first character.** |
| **No error. The demo works perfectly and the student cannot say what the p95 was.** | Nothing crashed. Nothing was measured. | They ran the service but never ran `read_logs.py`, so the four numbers were never computed. | `python3 eval/read_logs.py` takes half a second. **Objective 3 of Week 35 is the four numbers, not the log file.** |
| **No error. `wc -l` says 0 lines after a successful prediction.** | Nothing crashed. Nothing was recorded. | `level=logging.INFO` missing — Python's default level is `WARNING` and it discards `INFO` in silence. | Add the `level`. **The commonest silent bug of Week 35, and it will resurface today under pressure.** |
| **No error. Every latency in the log is the identical number.** | Nothing crashed. The stopwatch is in the wrong place. | Both `perf_counter()` calls sit on the same side of the work. | One stopwatch pair per prediction, inside `predict_one`. **Identical latencies are never real.** |
| **No error. The paper's `d4_broken.py` prints `accuracy: 1.0` and the student writes "no bugs".** | It ran, it printed, and the number is perfect. | The accuracy was computed on `Xtr` and `y_train` — the rows the model was fitted on. | Measure on rows the model has never seen. **A perfect score is the loudest alarm in this course.** |

### How to teach debugging without giving the answer

All thirty-one moves from the year still stand. Today adds the last one, and it is the one that closes the course:

32. **"What number did you expect before you ran it?"** If the answer is "I don't know", the bug is not in the code yet — it is in the plan. **Every single debugging move in this course is a special case of that question**, and you can say so today, because they have earned it.

And the sentence for this week:

> **"Every mystery in this course had the same shape: something printed a number and nobody had predicted it in advance. Week 6's 75 percent on pure noise, Week 21's flat loss, Week 26's double softmax, Week 35's missing log, and today's `accuracy: 1.0`. Predict, then check. That is the whole method, and it is the only thing you need to carry into Level 4."**

---

## 🎲 The Activity, In Full

### The Showcase Round

**What it is.** Every student gives a ten-minute live demo from a cold terminal, following the seven-stop route, and is then cross-examined with the same eight questions in the same order, with the banned-words list on display.

**Why it is worth the whole lesson.** Because it is the only assessment in the course that cannot be faked. A model card can be written the night before. A log can be generated in one shell loop. **A cold terminal in front of a room, and eight questions you cannot see coming the answers to, cannot be.** It is also the moment the year becomes visible to the student — nine months ago they could not have answered one of the eight.

### Setup

- **The running order on the board before they arrive**, with the clock time each demo starts. **Choosing an order live costs six minutes and makes everybody anxious.**
- **The seven stops on the board**, where the presenter can see them without turning round.
- **The eight questions and the banned words on the wall**, big.
- Week 35's **FINDINGS** sheet and Week 34's **SIX BOXES** sheet still up — the props for stops 1 and 4.
- **Page 36.1 in the presenter's hand**: the demo run sheet, with their own seven numbers already written on it in pen. **They are allowed to read the numbers off it.** This is not cheating; reading a measurement off a sheet is exactly what an engineer does.
- **Page 36.2 in every listener's hand**: the eight questions, with a box per presenter to tick whether the answer contained a number. **The audience has a job, so the audience pays attention.**

### Step 1 — the ninety-second reset (before each demo)

**Say this, every time, in the same words:**

> "New window. I want the first thing I see to be you opening a terminal. Your first sentence is the first line of your contract — **no preamble, no apology.** Seven stops, I will call the times. Go."

Then start the clock and say nothing until 1:00.

### Step 2 — the demo (10 minutes, timed out loud)

Call the stop times: **1:00, 2:00, 4:00, 6:00, 7:30, 9:00.** Nothing else. Do not help, do not prompt, do not fill silence.

**What you will see, and what to do:**

| What you see | What to do |
|---|---|
| A warm terminal | **Stop them immediately, kindly, before stop 1.** "New window." Costs fifteen seconds. Letting it go costs the objective. |
| A cold start that fails with `FileNotFoundError` | **A finding.** Let them diagnose it live. If they `cd`, re-run and say the sentence about relative paths, **they keep the mark.** |
| Stops 2 and 3 said as one number ("it takes about a second") | Let the demo finish, then ask it as question 2. **Do not correct mid-demo.** |
| They skip stop 6 because it shows a failure | **Ask for it directly:** "show me where it breaks." Skipping it is the single biggest mark loss available today. |
| A failure predicted in advance, live, correctly | **Say so out loud, immediately.** "Everybody notice: they told us the number before they ran it, and they were right." This is level 5 and the room should hear it named. |
| Slides | No slides. **A terminal is not a slide.** Agreed last week; enforce it in five seconds. |
| They run over ten minutes | Call "ten" and move to the questions. **The questions are the assessment; the demo is the evidence.** |

### Step 3 — the cross-examination (5 minutes, eight questions)

Flat voice, same order, no warmth, no coaching. The only follow-up you are allowed is **"with a number?"**, exactly once per question.

The listeners tick their page 36.2 boxes as they go. At the end, one line from you and nothing more:

> "Thank you. Eight out of eight had a number in them." *(or "six out of eight.")*

**Then say nothing else.** No feedback, no "well done", no coaching in front of the room. **Feedback is private and it happens after the paper.** This is the one place today where being warm does damage: a student who is praised in front of the room sets a bar the next student has to clear socially rather than technically.

### Step 4 — the audience tally (2 minutes, at the very end of the round)

**Do this:** Ask the room one question and let them answer with hands.

> "Across every demo today: which of the eight questions was answered worst?"

It is almost always **question 3** — the monitoring number — because it is the only one whose answer cannot be read off a metrics table. **Say that out loud if it comes up**, because it is the single most useful thing the class learns about itself today: *the hardest question about a model is the one about next month.*

### What "finished" looks like

Every student has: opened a terminal in front of the room · run all seven stops · been asked all eight questions · and had at least six answers with a number in them. **Every listener's page 36.2 has a tick column filled in for every presenter.**

### Variation — easier

**Cut stops 4 and 5** (breaking it live, and the log) and run a **five-stop, six-minute demo**: contract, cold start, service with two times, where it breaks, monitoring number. Then ask **five of the eight questions** — 2, 4, 5, 6 and 7, which are the five answerable from a printed card and a cold start.

**And give them the answers to read.** Page 36.2 filled in beforehand, in their own handwriting, and they read from it. **Reading your own measured numbers off a sheet is not a weaker version of the objective; it is the objective.** Nothing in the mastery scale mentions doing it from memory.

### Variation — harder

1. **Two extra questions you invent on the spot, from their own card.** The best ones are always: *"your card says the longest training review is 55 characters. What happens if I send you 400 words?"* and *"you said one row is worth 6.25 points. So how many rows would you need before 0.8125 meant something?"*
2. **Make them demo somebody else's project**, with five minutes to read the card first. **This is genuinely hard and genuinely realistic**, and a student who can do it has understood the contract rather than memorised their own.
3. **The prediction round.** Before stop 6, they write on the board the probability they think their model will give the failure case. Then they run it. **Within 0.05 is a real achievement and the room should know it.**
4. **One question back at you.** They get to ask you one question about their own model that they could not answer. **The honest answer is often "I don't know either, and here is how we would find out"** — and letting them see that is worth more than a clean session.

---

## ❓ Questions Students Ask This Week

**"What if my demo fails in front of everyone?"**

Then you diagnose it in front of everyone, which is harder and worth more. **Say this out loud before the round starts, because it is true and because it removes most of the fear in the room:** a demo where something breaks and the presenter names the cause, fixes it, and says what they would change is a *better* piece of evidence than one where everything works, because it proves they understand the machine rather than having memorised a sequence. Week 35 put the word "failure" on a sheet and crossed it out. That sheet is still on the wall today for a reason.

**"Why can't I use slides? Everyone uses slides."**

Because a slide is a claim and a terminal is evidence. You have spent two weeks building something that actually runs; a screenshot of it is strictly less information than the thing. And there is a harder reason: **slides let you skip the cold start**, which is exactly the one thing today is designed to check. If you want a single sheet of paper with your seven numbers on it to read from, that is page 36.1 and you are encouraged to use it.

**"Is 'accurate' a banned word too?"**

No — **"accurate" with a number is fine and is what we want.** "0.8125 accuracy on 16 held-out rows" is a good sentence. What is banned is "99% accurate", because that particular phrase is used to mean "good" rather than to mean a measurement, and Week 8 proved that 99% accuracy can be exactly what you get for predicting "no" every single time. **The test for any phrase: could somebody check it? "Robust" cannot be checked. "Survived four malformed requests" can.**

**"Why is the paper on paper? I can look everything up in ten seconds."**

Because looking things up is not the skill being tested. **Three of the four programs in Part C raise no exception at all**, so a runtime does not help you — nothing is going to tell you where the bug is. The skill is *reading code and predicting what it will do*, and the only way to test that is to take the runtime away. You are also allowed a calculator, because arithmetic is not the point either. **What is being tested is whether you can look at `accuracy: 1.0` and feel suspicious.**

**"Does my score today decide whether I can do Level 4?"**

It is one of seven gates, and it is the only one that is a number. The other six are things you can do or cannot do yet. **And the honest thing: gate 2 — a finished capstone — matters more than gate 1.** Level 4 spends a whole module evaluating a language model, and the entire idea of "evaluate" that it uses is the one the capstone forces you to build. A high paper score with an unfinished capstone is a worse position than the other way round, and anybody who tells you otherwise has not read Level 4.

**"How long should I wait before rewriting this project properly?"**

**Nobody fully agrees on this, and here is why.** One camp says rewrite it now, while you remember every decision, because the second version is where the learning actually consolidates. The other says leave it completely alone for a month, then come back and read your own code cold — because the thing you most need to learn is *how legible your own work is to a stranger*, and after a month you **are** the stranger. Both are genuinely right and they train different muscles. What everybody agrees on: **do not rewrite it in the same week.** You cannot see your own choices from three days away. If you want one piece of advice, take the second version: come back in a month, read it cold, and write down every question you have to ask yourself. **That list is a better report on your engineering than any mark on today's paper.**

**"Will I ever use `http.server` again? Isn't it a toy?"**

Probably not in a job, and it is not a toy — it is a **small** thing, which is different. Everything a real framework does for you, you have now seen done in forty lines: reading the length header, parsing the body, routing the path, setting the status code. **When you pick up a framework, you will know what it is doing on your behalf, which is the only good reason to use one.** The thing you will use again constantly is not the module — it is the four checks in order, and the habit of returning a message that says what to send instead.

**"What was actually the hardest week?"**

Ask the room this, honestly, and write the answers on the board. It is almost always **Week 18** (slopes multiplying along a chain) or **Week 25** (the output-size rule), and it is almost never the week they expected. **Then say the useful thing:** both of those weeks are hard for the same reason — they are the two weeks where you had to hold a number in your head and a shape in your head at the same time. **That is the specific thing Level 4 asks for constantly**, and knowing it is your weak spot is worth more today than any mark.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| **Demos overrun and the last two students are rushed.** | Fifteen minutes each is tight and the first demo always runs long. | **Running order on the board with clock times, and call them.** If you are at minute 63 with two students left, **stop and finish next lesson.** A rushed cross-examination is worth nothing. |
| **Somebody demos in a warm terminal and nobody notices.** | It is the window they have been working in all week. | **Enforce rule 1 out loud, every single time, including for the student you like most.** Watch them open the window. Fifteen seconds each. |
| **The cross-examination turns into a friendly chat.** | You are pleased with them and it is the last week. | **Flat voice, same eight questions, same order.** Warmth after the paper, in private. A rescued answer teaches nobody anything, and the room can tell. |
| **Answers with no numbers get through.** | "It's pretty fast" sounds like an answer. | **"With a number?"** — exactly once, then move on and write it down. **Do not supply the number for them.** |
| **Students skip stop 6 because it shows a failure.** | Nobody wants to show a failure in front of the room. | **Ask for it directly: "show me where it breaks."** And name it when somebody does it well, so the next presenter copies them. |
| **The paper is sat straight after the demos.** | It fits the timetable. | **Don't.** A student who has just presented cannot read code for silent bugs. **Separate sitting, quiet room, full 75 minutes.** |
| **Everybody ticks all seven gates.** | It looks better and it is their own sheet. | **Say the standard out loud: from a blank file, glossary only.** Then say the target: *"at least one honest blank on every sheet, and I will be more impressed by the blank."* |
| **A student with an unfinished capstone is waved through.** | It is the last week and nobody wants to be the bad news. | **Be the honest news instead.** "Gate 2 is not ticked, here is the fortnight that ticks it, and Level 4's evaluation module is built on it." **A wave-through costs them a term.** |
| **You give feedback in front of the room.** | It feels generous. | **One line only: how many of the eight had a number in them.** Everything else is private, after the paper. Praise in public sets a social bar the next student has to clear. |
| **The wrap gets eaten by overrunning demos.** | It always does. | **Protect two minutes of it.** If you have two minutes, read the Term 2 band of Figure 36.4 — the slope, the step, and the 42. **Those three numbers are the year.** |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** demo stops 4 and 5 (breaking it live, and the log walk-through) · three of the eight questions, keeping **2, 4, 5, 6 and 7** · Part C's D3 (it is the longest to read). **Mark Part C out of 19.5 and say so on the paper** — a mark out of a stated total is honest; a mark out of 26 with one question blank is not.

**Give them the copy-this-exactly scaffold.** Page 36.1 and page 36.2 **filled in completely, in their own handwriting, the day before**, and they read from both. Every number is theirs and measured; they are just not holding it in their head. **Reading your own measurements off a sheet is exactly what an engineer does, and nothing in the mastery scale says otherwise.**

**The version of the maths that skips the algebra.** Today's only arithmetic is in Part B, and two of the eight short answers need a calculation. Replace them with the counting versions:

```
S3 instead of computing  2 x 0.667 x 0.070 / 0.737 :

     precision 0.667 and recall 0.070.
     the plain average would be (0.667 + 0.070) / 2 = 0.3685
     F1 is 0.127, which is MUCH closer to the smaller one.
     -> "F1 gets dragged down towards the worse of the two."

     That sentence, with those three numbers copied off the paper,
     earns all three marks. No harmonic mean required.
```

**And the one thing not to cut:** question 6, asked in full. A student who leaves today able to say *"0.8125, on 16 rows, against a baseline of 0.500, and 16 rows means one row is worth 6.25 points"* has had the whole of Level 3 land, whatever else happened.

### If the student is flying

1. **Demo somebody else's project**, with five minutes to read their card first, then be cross-examined on it. **This is the hardest single thing available today** and it is the real test of whether the contract idea landed.
2. **The prediction round at stop 6.** Write the probability on the board before running the failure case. Within 0.05 is genuinely impressive.
3. **Find the fifth problem in D1.** There is one nobody mentions: **there is no three-way split**, so the "test" set was used as a validation set the moment anybody looked at its score and changed anything. One sentence.
4. **The two extra cross-examination questions**: *"what happens if I send 400 words when your longest training review is 55 characters?"* and *"how many rows would you need before 0.8125 meant something?"* **The second has no clean answer and arguing it for ninety seconds is a good use of ninety seconds.**
5. **Write the eight questions they would ask a stranger's model**, and say which of theirs differ from the eight on the wall and why. **Anybody who adds "what did you deliberately choose not to build?" has understood something most professionals have not.**

### If the student won't engage today

The last week is when this happens most, and it is almost never laziness — it is that a demo in front of a room is frightening and refusing is cheaper than failing.

**Give them a job that is not presenting.** Make them the **timekeeper and tally-keeper**: they call the seven stop times for every presenter, and they own the master copy of page 36.2 for the whole room — eight questions × every student, ticking whether each answer had a number in it. **It is a real job, the class depends on it, and doing it properly requires understanding all eight questions and all seven stops better than most presenters do.** At the end they read out the tally, which is the best two minutes of the wrap.

Then, privately and later, the demo happens with an audience of one: you, at a desk, ten minutes, eight questions. **Same assessment, different room size.** Record it as met.

If even the tally is too much, hand them Figure 36.4 and one question: *"pick the number on this sheet you are most sure you could explain to somebody, and explain it to me."* **Almost nobody refuses that**, and it usually turns into the whole conversation.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording. **Ask these of the whole room in the wrap, not of individuals** — today has had enough individual pressure.

**Check 1 — the two timing numbers (spoken, 60 seconds)**

> "Somebody tell me how fast their service is. **And I am listening for two numbers, not one.**"

*Good answer:* "About 772 milliseconds to load the model once when the service starts up, and a p95 of 0.27 milliseconds per request over my 111 logged requests. The max was 3.27 and that was the very first request, before anything was warm."

**What to catch:** one number, or the two added together. **"About a second" is a fail even though it is true**, because it hides the fact that the second is paid once and the quarter-millisecond is paid per request.

**Check 2 — what the headline hid (spoken, 60 seconds)**

> "Your card says **0.8125**. Tell me what that number was hiding, and tell me the group size."

*Good answer:* "On the 13 rows that contain a negation word, accuracy is 0.462 and recall on the positive class is 0.000 — six genuinely positive reviews and it found none of them. On the 15 rows without one, 0.800. And 12 of those 13 rows are traps I wrote on purpose to be hard, so 0.462 shows the mechanism exists rather than estimating how often it bites."

**What to catch:** a number with no `n`. Push once: *"how many reviews was that?"* **A student who volunteers the "written on purpose" caveat unprompted is at level 5.**

**Check 3 — the three questions (spoken, 90 seconds)**

> "I am going to hand you a model you have never seen, and I am going to tell you it gets **0.994**. **What are the first three things you say?**"

*Good answer:* "What is the baseline. What is the class balance. And was anything fitted before the split. Because 0.994 on a table that is 0.6% positive is what you get for predicting 'no' every time, and because a scaler or a vectorizer fitted before the split makes any number afterwards meaningless."

**What to catch:** anybody who starts evaluating the model rather than the number. **This is gate 5, it is the single most transferable thing in Level 3, and if the room can say it in chorus you have done your job.**

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Demo does not start from a cold terminal, or does not reach a prediction. Fewer than four of the eight answers contain a number. Uses banned words after being reminded. Under 35 on the paper. Gate sheet all ticked. |
| **2 — Emerging** | Cold start works. Five stops of seven. Four or five answers with numbers. Reports one latency figure. Knows the headline score but not the subgroup. 35–48 on the paper. |
| **3 — Secure** | Cold terminal, all seven stops, a prediction and a log line and a latency. **All eight questions answered with a number in each.** Two timing numbers kept separate. Names the worst subgroup with its `n`. No banned words. 49+ on the paper with 13+ on Part C. Gate sheet with at least one honest blank. **This is the target.** |
| **4 — Strong** | Predicts a failure before running it and is right. Says the byte limit and justifies it with the length of the longest training review. Explains why the p95 missed the max. Monitoring number computable without labels, with a measured baseline and an alarm level. Names the feedback loop on question 8 unprompted. |
| **5 — Exceptional** | Volunteers that the traps are adversarial, so the rate is not an estimate. Says out loud that their own latency will not match anybody else's. Diagnoses a live failure and says the sentence about relative paths. Names one thing they deliberately did **not** build, and why. On the gate sheet, leaves a box blank that they could have got away with ticking. |

---

## 📤 Homework to Assign

**Say this:**

> "**No new technical homework. This is the last thing I will ask you to do this year and it takes about forty minutes.**
>
> **First, page 36.6 — the Level 4 gate self-check, and I want you to be hard on yourself.** Seven gates. A tick means *I could do this from a blank file, with only the glossary open* — not *I could do it with my notes*, and not *I did it once in March*. **I am telling you now that I expect at least one blank on every sheet in this room, and I will be more impressed by an honest blank than by seven ticks.** Then at the bottom, name the **two** things you would most want to revisit, and one sentence each on why.
>
> **Second, page 36.7 — the letter to yourself.** One side of paper, to the person who opens Level 4. Three things in it. **What you want to build next**, specifically — not 'AI stuff', an actual thing. **One thing from this year you would now do differently, and why** — and the good answers are always specific: *'I would write the contract in Week 33 instead of Week 34, because I built the model before I knew what one prediction was about.'* And **one number from this year you are proud of**, with the arithmetic beside it.
>
> Then put the letter in an envelope, write the date on it, and keep it. **You will open it in about a year and it will be the most interesting thing you read that week.**"

**Workbook pages:** 36.1, 36.2 in class (36.1 filled in the day before) · 36.3, 36.4, 36.5 are the paper, sat in the second session · **36.6, 36.7** at home.

**Expected time:** 15 min on the gate self-check · 25 min on the letter · **about 40 minutes.**

> **🧑‍🏫 What to look for when you mark it:** three things, and none of them is technical. **One — is there at least one honest blank on the gate sheet?** A sheet with seven ticks is either a remarkable student or an unread sheet, and you will know which. **Two — is the "one thing I would do differently" specific?** "I'd work harder" is a blank. "I'd write the contract before the model" is a person who has understood the year. **Three — does the number they are proud of have its arithmetic beside it?** If it does, the habit has stuck, and that habit is the entire deliverable of Level 3. **Write one sentence back to each of them, by hand, and name the thing they did that nobody else did.** They keep this one.

---

## 🔑 Answer Key

Every item restated so you can mark from this page alone. **The paper is pages 36.3 (Part A), 36.4 (Part B) and 36.5 (Part C).**

### Page 36.1 — The demo run sheet

*Seven stops, with a blank beside each for the student's own number. Filled in, in pen, the day before.*

**Marking notes.** **Present or absent, and the marked part is stop 3 having two separate numbers on two separate lines.** A run sheet with one time on stop 3 predicts exactly which answer they will lose question 2 on, and you can fix it in ten seconds before they present.

### Page 36.2 — The eight questions, with your number

*Eight questions, a blank line under each for their own answer, and a tick column per presenter for the listeners.*

**Marking notes.** Eight lines, each containing at least one number. **The commonest blank is question 3**, the monitoring number, because it is the only answer that cannot be read off a metrics table. A blank there before the demo is a gift — send them to their Week 35 page 35.7 for two minutes.

---

### Part A — Multiple choice (20 × 1 mark)

> **📌 How to read this section.** Each item gives **the question stem**, then **the correct option in bold**, then **a one-line reason each of the other three is wrong** — so all four options on the printed paper are recoverable from this page. **One mark, right or wrong, no half marks.** Read the "why not" line aloud to any student who got it wrong; it takes ten seconds and it is worth more than the mark.

**A1 `[W1]`** 2,000 pizza orders, 28.8% late. `DummyClassifier(strategy="most_frequent")` scores roughly what, and what is that number?
**→ C. About `0.712` — the floor a real model must beat.** The dummy predicts the majority class ("on time", 71.2%) for every row. *Why not the others:* `0.288` is a dummy predicting the **minority** class; `0.500` is the coin-flip figure on a **balanced** problem; `0.000` is wrong because being right by accident still counts, which is the whole discomfort.

**A2 `[W2]`** 1,200 train / 400 validation / 400 test. Which statement is right?
**→ A. Train fits the weights; validation picks the model, features and threshold; test is opened exactly once at the end and never tuned against.** *Why not:* if **test** picks the model it has become a validation set and there is no honest final number left; fitting weights on validation destroys its only job; stratification balances classes and says nothing about which pile you may peek at.

**A3 `[W4]`** A column has training mean 5 and training standard deviation 2. After `StandardScaler`, the raw value 9 becomes:
**→ C. `2.0`.** `(9 − 5) ÷ 2 = 4 ÷ 2 = 2.0`. *Why not:* `0.8` is min-max thinking — there is no division by a range here; `1.8` is `9 ÷ 5`, dividing by the mean instead of subtracting it; `4.0` is subtracting and forgetting to divide, which is **centering**, not standardizing. **And note the word carrying the weight: `fit` learned 5 and 2 from the *training* rows only.**

**A4 `[W6]`** AUC jumps 0.78 → 0.978 when `customer_called_support` is added. What is it and what do you do?
**→ B. Target leakage — drop the column.** The availability test: at the moment the order is placed, has the customer phoned yet? No. *Why not:* it genuinely **is** correlated, which is not the issue; preprocessing leakage is about statistics computed before the split; temporal leakage survives no split strategy. **The tell is the size of the jump — 0.78 to 0.978 from one column is a confession, not a feature.**

**A5 `[W8]`** `TN = 5941, FP = 2, FN = 53, TP = 4`. The recall for fraud is:
**→ B. `0.070`.** `4 ÷ (4 + 53) = 4 ÷ 57 = 0.0702`. *Why not:* `0.667` is **precision**, `4 ÷ 6`; `0.127` is **F1**; `0.9997` is specificity, `5941 ÷ 5943`. **Accuracy here is `5945 ÷ 6000 = 0.9908` and it is hiding a catastrophe.**

**A6 `[W10]`** You lower the threshold from 0.5 to 0.2. What happens?
**→ A. Recall goes up or stays equal; precision usually goes down.** *Why not:* that is what **raising** it does; both going up would mean no trade-off and no reason for a PR curve to exist; the threshold is precisely how a probability becomes a label, so every cell of the matrix depends on it. **"Usually" is doing real work — precision is not monotonic and ticks up whenever the next item down the ranking is a true positive.**

**A7 `[W11]`** On a table that is 0.95% positive, average precision is 0.19. Is that good?
**→ C. Yes — AP's no-skill baseline is the positive rate, 0.0095, so 0.19 is about 20× baseline.** *Why not:* 0.5 is **ROC-AUC's** baseline, not AP's; AP is not an error rate and not on accuracy's scale; it has a very clear baseline, it just is not a constant. **Always print the positive rate next to an AP.**

**A8 `[W12]`** For `f(x) = x²`, the numeric slope `(f(x+h) − f(x−h)) ÷ 2h` at `x = 3` with `h = 0.001` is closest to:
**→ B. `6`.** `(3.001² − 2.999²) ÷ 0.002 = (9.006001 − 8.994001) ÷ 0.002 = 0.012 ÷ 0.002 = 6`. *Why not:* `9` is `f(3)` itself; `3` is `x`; `0.012` is the rise without dividing by the run. **And `2x` at `x = 3` is also 6, which is exactly the agreement Week 12 was built on.**

**A9 `[W14]`** Training loss falls for two epochs then sits at exactly `0.6931` for 5,000 more. What does that tell you?
**→ B. `0.6931` is `ln 2` — the model outputs `0.5` for every row and has learned nothing.** *Why not:* converged to `ln 2` is converged to ignorance; log loss's floor is 0 and values like 0.15 are routine; perfect separability drives log loss *towards zero*, the opposite symptom.

**A10 `[W15]`** From `w = 0`, learning rate `1.0`, the slope is `−0.5`. After one step, `w` is:
**→ B. `+0.5`.** `w ← w − lr × slope = 0 − 1.0 × (−0.5) = +0.5`. *Why not:* `−0.5` is `w += lr × slope`, **the sign error**, whose symptom is a loss that rises even at a tiny learning rate; `0.0` needs a zero slope; `−1.0` is the sign error plus a doubled step. **The gradient points uphill; you subtract it to go down.**

**A11 `[W17]`** A batch of shape `(4, 2)` goes into a layer whose weight grid is `(2, 3)`. The output shape is:
**→ B. `(4, 3)`.** The inner numbers, 2 and 2, must match and then vanish; the outer ones survive. *Why not:* `(2, 4)` is the transpose; `(4, 2)` forgets that the layer changes the width; `(2, 3)` is the weight grid itself. **Say it out loud: `(n, d) @ (d, h) → (n, h)`.**

**A12 `[W21]`** You write a PyTorch loop and leave out `optimizer.zero_grad()`. What do you see?
**→ B. Nothing raises. Gradients accumulate across every batch, so each update is driven by the sum of all earlier gradients (with plain SGD the step balloons; with Adam it is rescaled but still stale), and accuracy ends up worse than it should be.** *Why not:* the "backward through the graph a second time" error comes from calling `.backward()` twice on the same loss; a flat loss with no movement is the `lr = 0` symptom; every batch does train — all of them with a corrupted, growing gradient. **`zero_grad` is the first line of the inner loop, always.**

**A13 `[W22]`** You build `Linear(2, 16) → Linear(16, 1)` and forget the `ReLU` between them. What have you built?
**→ C. Something exactly equivalent to a single linear layer — no curved boundary is possible.** Two grids multiplied together are just another grid. *Why not:* the shapes compose perfectly, so nothing raises — which is why the bug is silent; it is not "slightly weaker", it is *exactly* as expressive as one layer; it is marginally slower and no better. **If your network scores precisely what logistic regression scored, check for this first.**

**A14 `[W25]`** An `8 × 8` image goes into `nn.Conv2d(1, 16, kernel_size=3, stride=2, padding=1)`. The output is:
**→ C. `4 × 4`.** `(8 + 2×1 − 3) ÷ 2 + 1 = 7 ÷ 2 + 1 = 3 + 1 = 4`, rounding down. *Why not:* `8 × 8` is `stride=1, padding=1`; `3 × 3` does the division and forgets the `+ 1`; `6 × 6` is `stride=1, padding=0`. **The two combinations worth memorising: `k=3, s=1, p=1` preserves size; `k=2, s=2` pooling halves it.**

**A15 `[W26]`** Your model ends with `nn.Softmax(dim=1)` and your loss is `nn.CrossEntropyLoss()`. What happens?
**→ D. Nothing raises, the squash is applied twice, the gradients flatten and accuracy caps out below where it should.** *Why not:* `CrossEntropyLoss` expects **raw logits** and applies log-softmax itself; no shape error occurs; it is not a speed problem. **End the model with a bare `nn.Linear`.**

**A16 `[W28]`** You try `k = 2…10` and pick the `k` with the **lowest inertia**. What is wrong?
**→ B. Inertia falls monotonically as `k` rises, so this always picks the largest `k` you tried.** At `k = n` it reaches zero, with every point its own cluster. *Why not:* k-means minimises inertia **for a fixed k**; comparing across k is a different and degenerate question; inertia is defined for every `k ≥ 1` and it falls rather than rises. **You want the bend, cross-checked with silhouette — and if there is no bend, you say so.**

**A17 `[W29]`** You run PCA on raw wine data where `proline` spans 278–1680 and `hue` spans 0.48–1.71, without standardizing. What happens?
**→ A. PC1 becomes essentially the `proline` axis**, because PCA maximises variance and variance is in the squared units of the raw column. *Why not:* sklearn's `PCA` centres but does **not** scale — which is exactly why `make_pipeline(StandardScaler(), PCA())` is the standard idiom; no error is raised; equal weighting would only happen if the variances were already equal. **Your "principal component" would be a statement about your measurement units.**

**A18 `[W32]`** Under plain bag-of-words with unigrams, which pair produces **identical** feature vectors?
**→ B. `"the dog bit the man"` and `"the man bit the dog"`.** Both have `the`×2, `dog`×1, `bit`×1, `man`×1 — identical vectors, cosine similarity 1.0, opposite meanings. *Why not:* `great` vs `cold` differ; `"great pizza"` has a word the other lacks; `"not good"` has an extra token, so the vectors differ by one dimension even though the classifier still often gets it wrong. **This is the defining limitation of bag-of-words and the reason Level 4's sequence models exist.**

**A19 `[W34]`** Which of these is the artifact you must save?
**→ C. The whole fitted `Pipeline`, plus a metadata file holding the threshold, the class order and the library versions.** *Why not:* saving only the classifier gives you something that expects vectorized, scaled input and has no idea how to produce it; saving only the vectorizer has the same problem backwards; saving the training script is not an artifact at all — **an artifact is a thing a fresh process can load with zero training code in it.**

**A20 `[W35]`** Your log holds 111 requests: mean 0.26 ms, p50 0.23, p95 0.27, max 3.27. Which statement is right?
**→ A. Report the p95 as the headline and the max beside it, because with 111 requests a single slow one sits above the 95th percentile and the p95 cannot see it.** *Why not:* the mean alone hides the only request anybody noticed; the p95 is not "useless" — it is precise about a different thing; a max of 3.27 is not a bug, it is the first request paying to warm the caches. **Three numbers, three jobs.**

---

### Part B — Short answer (8 × 3 marks)

Three marks: **1** for the core idea, **1** for a number or a specific, **1** for the "so what".

**B1 `[W1]` `[W2]` — the baseline.** *Explain why a model that cannot beat its baseline is worthless, using the pizza numbers. Then name the two things that must always be printed next to an accuracy figure.*

> **Model answer.** The pizza table is 28.8% late, so a model that says "on time" every single time — no features, no training, no thought — is right **71.2%** of the time. If my pipeline reports 70% accuracy it has spent an hour of compute to be *worse than a constant string*. A score is not a fact until it is a **comparison**: 0.71 on its own is a boast; 0.71 against a 0.712 baseline is a verdict.
>
> The two things that go next to every accuracy figure: **(1)** the baseline — the majority-class rate, or `DummyClassifier` scored on the same split; **(2)** the **size and class balance** of the pile it was measured on, because 0.87 on 40 rows with 3 positives is one lucky afternoon.

*Also credit:* the metric's name, and a spread from cross-validation rather than one number.

**B2 `[W6]` — the three leakages.** *Name all three, one concrete example each, and which direction each moves the score you report.*

| Leakage | Example | Direction |
|---|---|---|
| **Target** | `customer_called_support`, `chargeback_filed` — a column only filled in *because* the outcome already happened | Reported score **far too high** (0.978 against a real 0.78). Collapses on day one, because the column is empty at prediction time. |
| **Temporal** | Random-splitting time-ordered orders, so you train on December and test on November | Reported score **too high**. You measured interpolation and will deploy extrapolation. |
| **Preprocessing** | `StandardScaler().fit_transform(X)` before the split; an imputer learning its median from all rows; a vectorizer fitted on train **and** test | Reported score **too high** — usually mildly, sometimes absurdly. Week 6 scored 75% on a table of **pure noise**. |

> **The sentence that earns the third mark:** all three are the same crime — the model saw something at training time that it will not have at prediction time — and they are prevented differently: the **preprocessing** one for free, by splitting first and putting every transform inside a `Pipeline`; the **temporal** one only by splitting by date instead of at random; the **target** one only by the availability test (a `Pipeline` cannot know a column is filled in after the outcome).

**B3 `[W9]` `[W11]` — F1, and when not to use it.** *Compute F1 for precision 0.667 and recall 0.070, showing the arithmetic. Then: a missed fraud costs 500 and a false alarm costs 10. Explain why "the F1-optimal threshold" is the wrong answer.*

```
F1  =  2 x 0.667 x 0.070  /  (0.667 + 0.070)
    =  0.09338 / 0.737
    =  0.1267   ->  0.127

compare: the PLAIN average would be (0.667 + 0.070) / 2 = 0.3685
```

> **The point of the arithmetic:** 0.127 is far closer to 0.070 than to 0.3685. **The harmonic mean drags a lopsided pair down towards the smaller number**, which is exactly what you want from a summary of a model that finds 4 frauds out of 57.
>
> **And why F1 is the wrong tool here:** F1 treats a false positive and a false negative as equally bad. These are not equal — a miss costs **50 times** a false alarm. So you sweep the threshold and minimise `Cost(t) = 500 × FN(t) + 10 × FP(t)` on the **validation** set, pick the smallest, freeze it, and report the test metrics at that frozen threshold. Worked: `FN = 18, FP = 542` gives `500 × 18 + 10 × 542 = 9,000 + 5,420 = 14,420`. **When you know the costs, use the costs. F1 is the metric for when you don't.**

**B4 `[W14]` — log loss versus squared error.** *Why is squared error wrong for classification? Include the cost of predicting 0.05 when the truth is 1, both ways.*

> **Model answer.** Squared error barely punishes confident wrongness. Predicting `0.05` when the truth is `1` costs `(1 − 0.05)² = 0.9025` — less than 1, and not much worse than the `0.25` you get for shrugging and saying 0.5.
>
> Log loss punishes it properly: `−ln(0.05) = 2.9957`. That is **3.3 times worse** than squared error's 0.9025, and as the prediction approaches 0 the cost goes to infinity. **Log loss measures surprise**, so a model that is sure and wrong pays enormously — which is exactly the behaviour you want from something that will be trusted. And a bonus: log loss over a sigmoid is one bowl with one bottom, so descent cannot get stuck in a dip.

**B5 `[W18]` — backpropagation in one paragraph, and the 42.** *Explain it to somebody who has never seen a network. Then say what the 42 was.*

> **Model answer.** A network is a chain: the input goes through a weighted sum, a squash, another weighted sum, and into a loss. To improve a weight buried in the first layer I need to know how much the final loss moves when I nudge that weight — and the answer is just the **product of the local slopes along the path from the weight to the loss**. Backpropagation runs the forward pass once and then walks *backwards*, carrying the accumulated slope, so every weight gets its slope in a single sweep instead of one expensive pass per weight. It is bookkeeping, not new mathematics.
>
> **The 42:** nudging `w` moved `z` **3 times** as much, and nudging `z` moved the loss **14 times** as much, so nudging `w` moves the loss **3 × 14 = 42** times as much. **And the reason it is convincing is that we measured it both ways** — stage by stage, and then straight through from `w` to the loss — and the two agreed exactly.

**B6 `[W20]` `[W26]` — what autograd removed, and what it did not.** *Be precise. Then name one bug autograd computes perfect gradients for.*

> **What it removed:** deriving and hand-coding the backward pass. No more `dZ1 = dA1 * (Z1 > 0)`, no more remembering `keepdims=True` on the bias sums, no more dividing by `n` in three places. PyTorch records every operation as the forward pass runs, and `loss.backward()` walks the record in reverse.
>
> **What it did not remove:** deciding **what to differentiate**. Autograd computes a perfectly correct gradient of whatever loss you actually wrote, on whatever tensors you actually handed it. It has no opinion about whether that was the right loss, the right shapes or the right data.
>
> **A bug it is perfectly happy with:** ending the model with `nn.Softmax(dim=1)` and then using `nn.CrossEntropyLoss`, which applies log-softmax internally. The squash happens twice, nothing raises, the gradients are exactly right *for that wrong objective*, and accuracy quietly caps out low. *(Equally good: forgetting `zero_grad`; a leaking feature; `y` shaped `(n,)` broadcasting against `(n,1)`.)*

**B7 `[W30]` — the honest caption.** *You cluster a dataset, get `k = 3`, silhouette 0.28, and a 2-D PCA plot where PC1 + PC2 = 55% of the variance. Write the three-sentence caption. Then say what "no ground truth" costs you.*

> "k-means with `k = 3` on the standardized features gives a silhouette of **0.28** — real but overlapping structure: the groups exist, but many points sit near a boundary and would move under a different random seed. The plot shows the first two principal components, which together carry only **55%** of the total spread, so two points that look adjacent here may be far apart in the 45% that is not drawn. Cluster 3 is the one I trust least: it has the lowest mean silhouette and differs from Cluster 1 on only two features."
>
> **What no ground truth costs you:** there is no test set and no accuracy, because there is no right answer to be graded against. **So the burden of proof moves onto you:** two independent lines of evidence (elbow *and* silhouette), a stability check with a different seed, a feature-means table showing each cluster differs on something a human can name, and an honest sentence about which cluster is weakest. **Reporting weak structure as weak is a finding, not a failure.**

**B8 `[W35]` — subgroup metrics, and why you cannot monitor accuracy.** *Your card says 0.8125. Say what it hid, with the numbers. Then say why a monitoring plan built on accuracy is a plan you can never run.*

> **What it hid.** The 0.8125 was measured on the 16 held-out reviews only. Split 28 labelled rows by whether the review contains a negation word: **0.800 on the 15 rows without one**, and **0.462 on the 13 rows with one, where recall on the positive class is 0.000** — six genuinely positive reviews and it found none. The counts check: `13 + 15 = 28`, `6 + 12 = 18`, `18 ÷ 28 = 0.643`, which is the overall row. **And 12 of those 13 rows are traps written on purpose to be hard, so 0.462 demonstrates a mechanism rather than estimating a rate.**
>
> **Why accuracy cannot be monitored.** In production the right answer usually does not arrive, and when it does (a user complaint, a human audit of a small sample) it arrives late and biased towards the cases that went wrong. A comment goes through, gets a label, and no truth comes back. So accuracy is a number you cannot compute on the live traffic as it happens, and a plan whose only alarm is accuracy is a plan that cannot run day to day. **The monitoring number has to come from inputs and outputs alone** — the uncertainty-band rate (**14.4%** of my 111 logged requests sat between 0.45 and 0.65), the out-of-vocabulary rate, the prediction mix, the p95. All four come straight out of the log with no labels at all.

---

### Part C — Debug (4 × 6.5 marks)

**Every one of these runs. Three of the four raise nothing at all.**

#### D1 `[W1]` `[W2]` `[W6]` `[W8]` — the 0.9975 that means nothing

*Given in the paper: the program below, which prints `accuracy: 0.9975` and saves a file. **There are five separate problems. Find them all and rank them worst-first.***

```python
# d1_broken.py - prints 0.9975 and saves a file. Five separate problems.
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib

# --- the table: 6,000 card transactions, about 1.4% of them fraud ---------
rng = np.random.default_rng(0)
X_raw, y = make_classification(n_samples=6000, n_features=4, n_informative=3,
                               n_redundant=0, weights=[0.99, 0.01],
                               random_state=0)
df = pd.DataFrame(X_raw, columns=["amount", "hour", "n_items", "days_old"])
df["merchant_type"] = rng.choice(["food", "fuel", "games", "travel"], 6000)
df["country"] = rng.choice(["GB", "IE", "FR"], 6000)
# a chargeback is filed AFTER a fraud is discovered
df["chargeback_filed"] = np.where(y == 1, rng.random(6000) < 0.9, 0.0)
df["is_fraud"] = y

y = df["is_fraud"]                                          # line 24
X = df.drop(columns=["is_fraud"])                           # line 25

num = ["amount", "hour", "n_items", "days_old", "chargeback_filed"]   # line 27
cat = ["merchant_type", "country"]                                    # line 28

X[num] = StandardScaler().fit_transform(X[num])             # line 30

X_train, X_test, y_train, y_test = train_test_split(        # line 32
    X, y, test_size=0.2, random_state=0)

pre = ColumnTransformer([
    ("c", OneHotEncoder(), cat),                            # line 36
], remainder="passthrough")

pipe = Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=1000))])
pipe.fit(X_train, y_train)

print("accuracy:", round(pipe.score(X_test, y_test), 4))    # line 42

joblib.dump(pipe.named_steps["clf"], "fraud_v1.joblib")     # line 44
```

```text
$ python3 d1_broken.py
accuracy: 0.9975
```

**The five problems, worst first.**

**1 — Target leakage: `chargeback_filed` is in the features (line 27).** A chargeback is filed *after* a fraud has been discovered. At the moment the card is swiped this column is empty for everybody. **Worst, because the model is fundamentally not the model you think you have** — and the proof is below.

**2 — Preprocessing leakage: the scaler is fitted before the split (line 30).** `StandardScaler().fit_transform(X[num])` learns its means and standard deviations from **all 6,000 rows**, including the 1,200 that become the test set. Reported score is optimistic, and the scaler was never saved, so it cannot travel with the model anyway.

**3 — Accuracy on a 1%-positive problem, with no baseline (line 42).** `0.9975` arrives with nothing beside it. On these rows the do-nothing `DummyClassifier` already scores `0.9833` (only 20 of the 1,200 test rows are fraud), so the whole gap between the two is 3 mistakes in 1,200 — and accuracy alone cannot say which kind they are. There is no baseline, no confusion matrix, no precision or recall, no AUC, and no threshold decision.

**4 — `OneHotEncoder()` without `handle_unknown="ignore"` (line 36).** Works today; raises `Found unknown categories` the first time a new country arrives in production.

**5 — Only the classifier is saved (line 44).** `pipe.named_steps["clf"]` is the bare `LogisticRegression`. Reload it and you have a model that expects one-hot-encoded, scaled input and no idea how to produce it. **Dump the whole fitted `Pipeline`.**

*(The level-5 sixth, for anybody who finds it: there is **no three-way split**, so the "test" set is being used as a validation set the moment anybody looks at its score and changes something.)*

**The fix, run:**

```python
# d1_fixed.py - the honest version. Same data, five repairs.
import numpy as np
import pandas as pd
import joblib
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (confusion_matrix, classification_report,
                             roc_auc_score, average_precision_score)

rng = np.random.default_rng(0)
X_raw, y_all = make_classification(n_samples=6000, n_features=4, n_informative=3,
                                   n_redundant=0, weights=[0.99, 0.01],
                                   random_state=0)
df = pd.DataFrame(X_raw, columns=["amount", "hour", "n_items", "days_old"])
df["merchant_type"] = rng.choice(["food", "fuel", "games", "travel"], 6000)
df["country"] = rng.choice(["GB", "IE", "FR"], 6000)
df["chargeback_filed"] = np.where(y_all == 1, rng.random(6000) < 0.9, 0.0)
df["is_fraud"] = y_all

y = df["is_fraud"]
# FIX 1: chargeback_filed does not exist at prediction time. It is not a feature.
num = ["amount", "hour", "n_items", "days_old"]
cat = ["merchant_type", "country"]
X = df[num + cat]

# FIX 2 + 5: split FIRST, three ways, stratified, seeded.
X_tr, X_tmp, y_tr, y_tmp = train_test_split(
    X, y, test_size=0.40, stratify=y, random_state=0)
X_val, X_te, y_val, y_te = train_test_split(
    X_tmp, y_tmp, test_size=0.50, stratify=y_tmp, random_state=0)

pre = ColumnTransformer([
    ("num", StandardScaler(), num),                        # fitted on train only
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat),   # FIX 4
])
pipe = Pipeline([("pre", pre),
                 ("clf", LogisticRegression(max_iter=1000,
                                            class_weight="balanced"))])
pipe.fit(X_tr, y_tr)

# FIX 3: baseline first, then metrics that survive imbalance.
dummy = DummyClassifier(strategy="most_frequent").fit(X_tr, y_tr)
print("baseline accuracy :", round(dummy.score(X_val, y_val), 4))
print("positive rate     :", round(float(y_val.mean()), 4))

prob = pipe.predict_proba(X_val)[:, 1]
print("ROC-AUC           :", round(roc_auc_score(y_val, prob), 4))
print("average precision :", round(average_precision_score(y_val, prob), 4))
tn, fp, fn, tp = confusion_matrix(y_val, prob >= 0.5).ravel()
print("tn=%d fp=%d fn=%d tp=%d" % (tn, fp, fn, tp))
print(classification_report(y_val, prob >= 0.5, digits=3,
                            target_names=["legit", "fraud"]))

# FIX 5: the WHOLE pipeline is the artifact.
joblib.dump(pipe, "fraud_v1.joblib")
```

```text
$ python3 d1_fixed.py
baseline accuracy : 0.9858
positive rate     : 0.0142
ROC-AUC           : 0.5894
average precision : 0.0815
tn=862 fp=321 fn=9 tp=8
              precision    recall  f1-score   support

       legit      0.990     0.729     0.839      1183
       fraud      0.024     0.471     0.046        17

    accuracy                          0.725      1200
   macro avg      0.507     0.600     0.443      1200
weighted avg      0.976     0.725     0.828      1200
```

> **🔢 Read the two numbers side by side and say this out loud when you hand the papers back.** Broken: **0.9975**. Fixed, on the same rows: an **ROC-AUC of 0.5894**, where a coin flip is 0.5000. **The leaky column was doing essentially all of the work, and once it is gone there is barely a model there at all.** That is not a disappointing result — it is the correct one, arrived at honestly, and it is the difference between a report and a lie. **Full marks for anybody who says, unprompted, that the honest number being terrible is the point.**

**Marking.** 4 marks for the five problems (0.8 each, round to the nearest half) · 1.5 for ranking the leak worst **with the availability argument** · 1 for a fix that splits first and prints a baseline. **A student who says "leakage" without naming the column gets 1 of 4.**

---

#### D2 `[W12]` `[W15]` `[W17]` — the descent that climbs

*Given in the paper: hand-rolled logistic regression on four students. You know the right answer — after one step from `w = 0` with `lr = 1.0`, `w` should be `+0.5` and the loss should fall from `0.693147` to `0.653920`. **There are three bugs. Find all three, say which is worst and why, and write the corrected loop.***

```python
# d2_broken.py - hand-rolled logistic regression. It runs. The loss climbs.
import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

X = np.array([[1.0], [2.0], [3.0], [4.0]])     # 4 rows, 1 feature
y = np.array([0, 0, 1, 1])                     # line 8

w = np.zeros((1, 1))
b = 0.0
lr = 1.0

for epoch in range(151):
    z = X @ w + b                              # line 15
    p = sigmoid(z)

    loss = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))   # line 18

    dz = (p - y) / len(y)                      # line 20
    dw = X.T @ dz                              # line 21
    db = dz.sum()

    w = w + lr * dw                            # line 24
    b = b + lr * db                            # line 25

    if epoch % 50 == 0:
        print(epoch, round(float(loss), 6), "w.shape =", w.shape)
```

```text
$ python3 d2_broken.py
d2_broken.py:18: RuntimeWarning: divide by zero encountered in log
  loss = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))   # line 18
d2_broken.py:5: RuntimeWarning: overflow encountered in exp
  return 1 / (1 + np.exp(-z))
0 0.693147 w.shape = (1, 4)
50 inf w.shape = (1, 4)
100 inf w.shape = (1, 4)
150 inf w.shape = (1, 4)
```

**Three bugs.**

**Bug 1 (worst) — the shape mismatch, line 8 feeding line 20.** `y` has shape `(4,)`; `p` has shape `(4, 1)`. NumPy broadcasts `p - y` into a **`(4, 4)`** matrix and raises nothing. Everything downstream is garbage: `loss` averages 16 nonsense terms, `dw` becomes `(1, 4)`, and `w` is silently reshaped from `(1, 1)` to `(1, 4)` — **which the printed `w.shape = (1, 4)` is telling you, if you look.**

*Why this is worse than the sign error:* **the sign error produces a wrong answer you can see** — the loss rises. **The shape error produces numbers no plot will complain about**, and it survives being "fixed" everywhere else. Silent beats loud. Fix: `y = y.reshape(-1, 1)`, and then `assert p.shape == y.shape` so it can never happen again.

**Bug 2 — the sign, lines 24 and 25.** The gradient points **uphill**. `w = w + lr * dw` walks up it. Fix: subtract. **And you already had the tell: you know `w` should be `+0.5` after one step.**

**Bug 3 — no clipping before the logarithm, line 18 (a weakness, and the one that shows the symptom).** Once the uphill walk has made the weights huge, `sigmoid` saturates to exactly `1.0` or `0.0` in float64, `np.log(0)` returns `-inf`, and the loss becomes `inf` — which is precisely what the real output shows. Be honest with the student: on this data, once the sign and shape are fixed, `p` stays well inside (0.017, 0.989) for all 150 epochs and the clip never fires — it is cheap insurance for other data, not what broke this program. Fix: `np.clip(p, 1e-12, 1 - 1e-12)` before any logarithm. *(Accept a student who names the `inf` loss / `RuntimeWarning` as the third problem.)*

**The fix, run:**

```python
# d2_fixed.py - three repairs: the shape, the sign, the clip.
import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

X = np.array([[1.0], [2.0], [3.0], [4.0]])
y = np.array([0, 0, 1, 1]).reshape(-1, 1)      # FIX 1: (4, 1), not (4,)

w = np.zeros((1, 1))
b = 0.0
lr = 1.0
n = len(y)

for epoch in range(151):
    z = X @ w + b
    p = sigmoid(z)
    assert p.shape == y.shape                  # FIX 1, enforced

    pc = np.clip(p, 1e-12, 1 - 1e-12)          # FIX 3
    loss = -np.mean(y * np.log(pc) + (1 - y) * np.log(1 - pc))

    dz = (p - y) / n                           # (4, 1)
    dw = X.T @ dz                              # (1, 1)
    db = dz.sum()

    w = w - lr * dw                            # FIX 2: subtract
    b = b - lr * db

    if epoch % 50 == 0:
        print(epoch, round(loss.item(), 6), "w =", round(w.item(), 6))
```

```text
$ python3 d2_fixed.py
0 0.693147 w = 0.5
50 0.220152 w = 1.739522
100 0.149182 w = 2.406249
150 0.116635 w = 2.867009
```

> **🔢 The maths, slowly — and this is how you know the fix is right rather than merely quieter.** Epoch 0 prints the loss **before** the step. With `w = 0` and `b = 0`, every `z` is 0, so every `p` is `0.5`, so each row's loss is `−ln(0.5) = 0.693147`. Then the step:
>
> ```
> dz = (p − y) / 4  =  (0.5 − [0,0,1,1]) / 4  =  [ 0.125, 0.125, −0.125, −0.125 ]
> dw = X.T @ dz     =  1(0.125) + 2(0.125) + 3(−0.125) + 4(−0.125)
>                   =  0.125 + 0.25 − 0.375 − 0.5
>                   =  −0.5
> w  = 0 − 1.0 × (−0.5)  =  +0.5        ✅ matches the printed 0.5
> db = 0.125 + 0.125 − 0.125 − 0.125  =  0.0,  so b stays at 0
> ```
>
> **And recomputing the loss after that step gives 0.653920**, exactly as stated in the question. Every one of those numbers can be checked with a pencil, which is the only reason anybody should believe the program.

**Marking.** 4 marks for the three bugs (1.33 each) · 1.5 for naming the **shape** bug as worst **with the "silent beats loud" reason** · 1 for a corrected loop that subtracts and reshapes. **Full marks needs `w = +0.5` written down somewhere.**

---

#### D3 `[W21]` `[W23]` `[W26]` — the loop that won't learn

*Given in the paper: a 2-layer network on the 8×8 digits. It should reach the mid nineties. It plateaus in the eighties and wobbles. **There are four problems. Find them and write the corrected loop.***

```python
# d3_broken.py - digits, a 2-layer MLP. It runs. It should reach the mid nineties.
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.datasets import load_digits

torch.manual_seed(0)
d = load_digits()
X = torch.from_numpy(d.data).float() / 16.0      # (1797, 64)
y = torch.from_numpy(d.target).long()            # (1797,)
perm = torch.randperm(len(y))
X, y = X[perm], y[perm]                          # shuffle before splitting

train_dl = DataLoader(TensorDataset(X[:1257], y[:1257]),
                      batch_size=32, shuffle=True)
val_dl = DataLoader(TensorDataset(X[1257:], y[1257:]), batch_size=32)

model = nn.Sequential(
    nn.Linear(64, 64), nn.ReLU(), nn.Dropout(0.3),
    nn.Linear(64, 10), nn.Softmax(dim=1),        # line 20
)
loss_fn = nn.CrossEntropyLoss()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(20):
    for xb, yb in train_dl:
        out = model(xb)                          # line 27
        loss = loss_fn(out, yb)
        loss.backward()
        opt.step()                               # line 30

    correct = 0
    for xb, yb in val_dl:                        # line 33
        correct += (model(xb).argmax(1) == yb).sum().item()
    print("epoch %2d  val acc %.3f" % (epoch, correct / 540))
```

```text
$ python3 d3_broken.py                                  (2.4 seconds)
epoch  0  val acc 0.383
epoch  1  val acc 0.531
epoch  2  val acc 0.607
epoch  3  val acc 0.639
epoch  4  val acc 0.722
epoch  5  val acc 0.715
epoch  6  val acc 0.728
epoch  7  val acc 0.796
epoch  8  val acc 0.744
epoch  9  val acc 0.783
epoch 10  val acc 0.811
epoch 11  val acc 0.833
epoch 12  val acc 0.863
epoch 13  val acc 0.798
epoch 14  val acc 0.833
epoch 15  val acc 0.880
epoch 16  val acc 0.859
epoch 17  val acc 0.831
epoch 18  val acc 0.843
epoch 19  val acc 0.859
```

**Four problems.**

**1 (worst) — no `optimizer.zero_grad()`.** PyTorch **accumulates** into `.grad` by design. With nothing clearing it, batch 40's gradient is the sum of batches 1 to 40, so every update is driven mostly by stale gradients from old weights. (With plain SGD the step would also balloon; this program uses Adam, which rescales the step, so what you see is slow, noisy learning rather than a blow-up.) **Look at the output: it climbs, then drops to 0.798, then climbs, then drops to 0.831. That wobble is the signature.**

**2 — `nn.Softmax(dim=1)` as the last layer with `nn.CrossEntropyLoss` (line 20).** The loss expects **raw logits** and applies log-softmax itself, so the squash happens twice, the gradients flatten, and accuracy caps out. Nothing raises. **End the model with a bare `nn.Linear`.**

**3 — no `model.eval()` / `model.train()` around the validation loop (line 33).** `Dropout(0.3)` is still active while you measure, so 30% of the units are randomly switched off during evaluation. Your number is noisy **and pessimistic**, which makes every other diagnosis harder.

**4 — no `torch.no_grad()` in the validation loop.** PyTorch builds a computation graph for every validation batch and throws it away. Wasteful in time and memory, and it is how you meet an out-of-memory error on a bigger model.

*(Half a mark bonus: `correct / 540` hard-codes the validation size. Use `len(dl.dataset)`.)*

**The fix, run:**

```python
# d3_fixed.py - four repairs. Same model, same data, same twenty epochs.
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.datasets import load_digits

torch.manual_seed(0)
d = load_digits()
X = torch.from_numpy(d.data).float() / 16.0
y = torch.from_numpy(d.target).long()
perm = torch.randperm(len(y))
X, y = X[perm], y[perm]

train_dl = DataLoader(TensorDataset(X[:1257], y[:1257]),
                      batch_size=32, shuffle=True)
val_dl = DataLoader(TensorDataset(X[1257:], y[1257:]), batch_size=32)

model = nn.Sequential(
    nn.Linear(64, 64), nn.ReLU(), nn.Dropout(0.3),
    nn.Linear(64, 10),                  # FIX 2: bare Linear. No Softmax.
)
loss_fn = nn.CrossEntropyLoss()          # it applies log-softmax itself
opt = torch.optim.Adam(model.parameters(), lr=1e-3)


@torch.no_grad()                         # FIX 4
def evaluate(dl):
    model.eval()                         # FIX 3: dropout OFF
    correct = 0
    for xb, yb in dl:
        correct += (model(xb).argmax(1) == yb).sum().item()
    return correct, len(dl.dataset)      # FIX 5: no hard-coded 540


for epoch in range(20):
    model.train()                        # FIX 3: dropout back ON
    for xb, yb in train_dl:
        opt.zero_grad()                  # FIX 1: FIRST line of the inner loop
        out = model(xb)
        loss = loss_fn(out, yb)
        loss.backward()
        opt.step()
    c, n = evaluate(val_dl)
    print("epoch %2d  val acc %.3f  (%d of %d)" % (epoch, c / n, c, n))
```

```text
$ python3 d3_fixed.py                                   (2.8 seconds)
epoch  0  val acc 0.609  (329 of 540)
epoch  1  val acc 0.785  (424 of 540)
epoch  2  val acc 0.861  (465 of 540)
epoch  3  val acc 0.885  (478 of 540)
epoch  4  val acc 0.900  (486 of 540)
epoch  5  val acc 0.911  (492 of 540)
epoch  6  val acc 0.917  (495 of 540)
epoch  7  val acc 0.920  (497 of 540)
epoch  8  val acc 0.931  (503 of 540)
epoch  9  val acc 0.930  (502 of 540)
epoch 10  val acc 0.933  (504 of 540)
epoch 11  val acc 0.941  (508 of 540)
epoch 12  val acc 0.952  (514 of 540)
epoch 13  val acc 0.950  (513 of 540)
epoch 14  val acc 0.956  (516 of 540)
epoch 15  val acc 0.959  (518 of 540)
epoch 16  val acc 0.956  (516 of 540)
epoch 17  val acc 0.957  (517 of 540)
epoch 18  val acc 0.954  (515 of 540)
epoch 19  val acc 0.961  (519 of 540)
```

> **0.859 becomes 0.961 — 519 of 540 unseen digits instead of 464.** Same model, same data, same twenty epochs, same seed. **Four lines of discipline, ten accuracy points, and not one error message in the broken version.** That is the sentence to put on the board when you hand this one back.

**Marking.** 4 marks for the four problems · 1.5 for naming `zero_grad` worst **and explaining accumulation** · 1 for a corrected loop with `zero_grad` first and `eval`/`train` in the right places. **A student who spots the wobble in the printed numbers and uses it as evidence gets the 1.5 outright.**

---

#### D4 `[W2]` `[W31]` `[W33]` `[W34]` — the serving code that lies

*Given in the paper: the program below plus the 40-review corpus it imports. It runs and reports an accuracy of exactly `1.0`. **There are four problems. Find them, rank them, and write the fixed version.***

```python
# d4_broken.py - the serving script that lies. It runs. It reports 1.000.
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from corpus import load_corpus

texts, labels = load_corpus()
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0)                # line 11

vec = TfidfVectorizer(stop_words="english")                       # line 13
Xtr = vec.fit_transform(X_train)                                  # line 14
Xte = vec.transform(X_test)                                       # line 15

clf = LogisticRegression(max_iter=1000).fit(Xtr, y_train)

print("accuracy:", accuracy_score(y_train, clf.predict(Xtr)))     # line 19

meta = {"version": "sentiment_v1", "threshold": 0.65}
with open("meta.json", "w") as f:
    json.dump(meta, f)

def predict(text):
    prob = clf.predict_proba(vec.transform([text]))[0, 1]
    label = "positive" if prob >= 0.5 else "negative"             # line 27
    print("LOG:", label)                                          # line 28
    return label

print(predict("the pizza was not delicious"))
print(predict("not boring for a single minute"))
```

```text
$ python3 d4_broken.py
accuracy: 1.0
LOG: positive
positive
LOG: negative
negative
```

**Four problems, worst first.**

**1 (worst) — the accuracy is measured on the training rows (line 19).** `accuracy_score(y_train, clf.predict(Xtr))` compares the model's predictions on `Xtr` against `y_train` — the very rows it was fitted on. **`1.0` is not a result, it is a receipt.** There is also no baseline and no class balance printed. Fix: predict on `X_test`, print a `DummyClassifier` baseline beside it, and print `n`.

**2 — `stop_words="english"` (line 13).** sklearn's English stopword list has **318 words in it and `not`, `no`, `never`, `nothing` and `cannot` are all on it.** On a *sentiment* task those are the load-bearing words. Watch what it does to one sentence:

```text
stop_words="english" :  ['pizza', 'delicious']
stop_words=None      :  ['the', 'pizza', 'was', 'not', 'delicious']
```

> **Be honest about this one when you mark it, because the honest version is more interesting.** In *this particular* corpus, no training review contains the word `not` at all, so removing the stopwords deletes no negation that the model ever saw (it does drop the one `no` in "made no sense" and ordinary words like `the` and `was`, which shifts the vocabulary from 66 to 58 words and the probabilities slightly, but not the test accuracy). **The bug is still a bug** — the instant one negated review reaches the training set, that setting deletes the only word carrying the meaning. **A student who spots that the corpus has no negations *and* that the setting is still wrong is at level 5.** *(And one genuinely useful detail: `hardly` is **not** on sklearn's list, which is exactly the kind of thing you find only by printing the list.)*

**3 — the threshold is hard-coded as `0.5` (line 27) while the metadata says `0.65`.** The program **writes 0.65 to a file and then ignores it two lines later.** This is the exact failure Week 34 exists to prevent: the threshold is a decision with arithmetic behind it, and the serving code must *read* it, never retype it. Fix: `json.load` the metadata and use `float(meta["threshold"])`.

**4 — the log records the label and nothing else (line 28).** `LOG: positive` cannot answer a single question. Which model version? What was sent in? What probability? Against what threshold? **Six months later this line is worth nothing**, and "somebody says it got their comment wrong" becomes "I don't know". Fix: log the whole contract as one JSON object per line.

*(Also worth half a mark: the split is not stratified, and a 10-row test set means one review is worth 10 percentage points.)*

**The fix, run.** First the corpus, so the whole thing is runnable:

```python
"""corpus.py - 40 short reviews, typed by hand. 20 positive, 20 negative."""
POSITIVE = [
    "the pizza was hot and delicious",
    "delicious fresh pizza and kind friendly staff",
    "wonderful acting and a warm script",
    "fast delivery and careful packaging",
    "i laughed the whole way through",
    "the staff were kind and the food came quickly",
    "excellent crust and a generous topping",
    "brilliant film and a great ending",
    "hot fresh bread and wonderful coffee",
    "great value and friendly service",
    "the driver was kind and the food was hot",
    "a brilliant evening and excellent company",
    "fresh salad and delicious dressing",
    "wonderful staff and a great atmosphere",
    "the coffee was excellent and the cake was fresh",
    "friendly driver and a hot delicious pizza",
    "great acting and a brilliant script",
    "delicious food and fast friendly delivery",
    "excellent service and wonderful fresh bread",
    "a great film with kind gentle humour",
]
NEGATIVE = [
    "cold food and a rude driver",
    "stale bread and awful coffee",
    "a complete waste of two hours",
    "the plot made no sense and the acting was wooden",
    "arrived soggy and the box was crushed",
    "boring predictable and far too long",
    "terrible service and cold soggy chips",
    "dreadful film and a rude usher",
    "awful pizza and a late delivery",
    "rude staff and terrible coffee",
    "soggy crust and cold toppings",
    "a dreadful evening and awful food",
    "stale cake and a boring menu",
    "terrible acting and a dreadful script",
    "the coffee was cold and the bread was stale",
    "rude driver and soggy awful pizza",
    "boring film and terrible sound",
    "cold food and dreadful packaging",
    "awful service and stale rude everything",
    "a boring film with terrible dialogue",
]

def load_corpus():
    texts = POSITIVE + NEGATIVE
    labels = [1] * len(POSITIVE) + [0] * len(NEGATIVE)
    return texts, labels
```

```python
# d4_fixed.py - four repairs. Same corpus, same model, honest numbers.
import json
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from corpus import load_corpus

texts, labels = load_corpus()
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, stratify=labels, random_state=0)

# FIX 2: stop_words=None. sklearn's English list contains not, no, never.
pipe = make_pipeline(
    TfidfVectorizer(lowercase=True, ngram_range=(1, 2), stop_words=None),
    LogisticRegression(C=4.0, max_iter=1000),
)
pipe.fit(X_train, y_train)

# FIX 1: measure on the rows the model has never seen, with a baseline beside it.
dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
print("baseline accuracy :", round(dummy.score(X_test, y_test), 4))
print("train accuracy    :", round(accuracy_score(y_train, pipe.predict(X_train)), 4))
print("TEST accuracy     :", round(accuracy_score(y_test, pipe.predict(X_test)), 4),
      "on n =", len(y_test))
print(classification_report(y_test, pipe.predict(X_test), digits=3,
                            target_names=["negative", "positive"]))

# the metadata is the single source of truth for the threshold
META = {"version": "sentiment_v1", "threshold": 0.65}
with open("meta.json", "w") as f:
    json.dump(META, f)
with open("meta.json") as f:
    meta = json.load(f)

THRESHOLD = float(meta["threshold"])       # FIX 3: read it, never retype it
VERSION = meta["version"]


def predict(text):
    prob = float(pipe.predict_proba([text])[0, 1])
    label = "positive" if prob >= THRESHOLD else "negative"
    row = {"model_version": VERSION, "input": text, "label": label,
           "probability": round(prob, 4), "threshold": THRESHOLD}
    print("LOG:", json.dumps(row))         # FIX 4: the whole contract, one line
    return label


print()
predict("the pizza was not delicious")
predict("not boring for a single minute")
print()
vocab = pipe.named_steps["tfidfvectorizer"].get_feature_names_out()
print("vocabulary size      :", len(vocab))
print("'not' in vocabulary  :", "not" in vocab)
```

```text
$ python3 d4_fixed.py
baseline accuracy : 0.5
train accuracy    : 1.0
TEST accuracy     : 0.8 on n = 10
              precision    recall  f1-score   support

    negative      0.800     0.800     0.800         5
    positive      0.800     0.800     0.800         5

    accuracy                          0.800        10
   macro avg      0.800     0.800     0.800        10
weighted avg      0.800     0.800     0.800        10


LOG: {"model_version": "sentiment_v1", "input": "the pizza was not delicious", "label": "positive", "probability": 0.6971, "threshold": 0.65}
LOG: {"model_version": "sentiment_v1", "input": "not boring for a single minute", "label": "negative", "probability": 0.3168, "threshold": 0.65}

vocabulary size      : 188
'not' in vocabulary  : False
```

> **Three things to say out loud when you hand this one back, and the third is the best one in the paper.**
>
> **One — `1.0` became `0.8` on `n = 10`.** The train accuracy is still 1.0 and it is printed **on purpose**, right above the test figure, because the gap between those two lines is the story. And `n = 10` means one review is worth ten percentage points, which is a sentence that belongs on the card.
>
> **Two — the log line is now something a person can use.** `LOG: positive` could answer nothing; the JSON line names the model, the input, the probability and the threshold. At eleven at night, that is the difference between an answer and "I don't know".
>
> **Three — look at the last line: `'not' in vocabulary: False`.** Not because a setting removed it. **Because not one of the 40 training reviews contains the word.** The model has never seen a negation in its life, which is exactly why it scores `"the pizza was not delicious"` at **0.6971** and calls it positive. **Week 31 predicted this failure from theory; the vocabulary printout is the evidence.** That is the habit the whole year was for: **print your vocabulary before you trust your model.**

**Marking.** 4 marks for the four problems · 1.5 for ranking the training-set accuracy worst **with the "it is a receipt, not a result" reasoning** · 1 for a fix that evaluates on held-out rows and reads the threshold from the file. **A student who finds the missing `not` in the vocabulary gets the bonus half mark and a sentence of praise in the margin.**

---

### Pages 36.6 and 36.7 — the gate self-check and the letter

**Page 36.6 — the Level 4 gate.** The seven gates and their standards are in §6 above. **There is no right answer to mark against; there is a right *behaviour*.**

**Marking notes.** Three things. **One — is there at least one honest blank?** A sheet with seven ticks is either a remarkable student or an unread sheet, and you will know which from their paper and their demo. **Two — do the two "things I would revisit" match the evidence?** A student whose Part C score was 9 of 26 and who names gate 5 as their weakness has read their own result correctly, and that is the skill. A student who names nothing they are weak at has not. **Three — check gate 2 against reality.** It is the one gate you can verify yourself, from Weeks 34 and 35, and it is the one that matters most for Level 4.

**Page 36.7 — the letter to yourself.** One side. Three things: what they want to build next, specifically · one thing from this year they would now do differently, with a reason · one number they are proud of, with the arithmetic beside it.

**Marking notes.** **Do not mark this for quality.** Check three boxes and write one sentence back by hand. **Is the "build next" a specific thing** rather than "AI stuff"? **Is the "do differently" specific?** The best answers are always structural — *"I would write the contract in Week 33 instead of Week 34, because I built the model before I knew what one prediction was about"* — and "I would work harder" is a blank. **Does the number have its arithmetic beside it?** If it does, the habit has stuck, and that habit is the whole deliverable of Level 3.

### Answers to every question posed in the lesson

**Hook — "what did that `grep` print?"** Nothing. **The nothing is the evidence** — there is no training code in the serving folder, and that is Rule 1 checked rather than promised.

**Hook — "why is '99% accurate' on the banned list?"** Because on a table that is 1% positive, predicting "no" every single time scores 99% and catches zero fraud. **99% can be the number you get for doing nothing.**

**Concept — "why is showing a failure more impressive than hiding one?"** Because anybody can hide one, and a model with a *known* failure is usable while a model with an unknown one is a trap.

**Concept — "question 4, nine months ago, what would the honest answer have been?"** "I don't know." That is why the log carries the input, the probability, the threshold and the version on every line.

**Concept — "question 5, the reason, not the string."** No authentication and no rate limit, so `0.0.0.0` would let anybody on the network send it a million requests.

**Concept — "question 8, why can't I retrain on my own log?"** Those 111 lines are the model's own opinions, not labels. Training on them is a feedback loop: it learns its own mistakes and grows more confident about them, and rising confidence looks exactly like improvement.

**Live-code — "it worked for nine months of Tuesdays. Why not now?"** The path was relative to whichever folder you were standing in, and a new terminal starts somewhere else. `Path(__file__).resolve()` is what makes it not care.

**Activity — "which of the eight was answered worst?"** Almost always **question 3**, the monitoring number, because it is the only one whose answer cannot be read off a metrics table. **The hardest question about a model is the one about next month.**

**Wrap — the three checks.** Two timing numbers kept separate · 0.462 on the 13 rows with a negation, recall 0 of 6 · baseline, class balance, anything fitted before the split.

---

## 🔮 Next Week Preview

**There is no next week.** Thirty-six weeks ago you opened a file that contained one line of code and five hidden decisions, and you spent the year learning to see all five. Along the way the student measured a slope with a pencil before they knew the word *derivative*, multiplied a `(3,2)` grid by a `(2,4)` grid by hand before they typed `@`, discovered that backpropagation is `3 × 14 = 42`, counted all 1,898 numbers in their own convolutional network, watched a model score 75% on a table of pure noise, and finished by handing a stranger a working service, a card that says exactly where it breaks, and a log that proves it ran. **They can now be handed an unfamiliar model and a confident number, and tell you whether to believe it. Very few adults can do that.**

**What to prep — and it is all for them, not for you.** **One — mark the papers and the letters within the week, while it still matters to them**, and write one handwritten sentence on each letter naming the thing that student did which nobody else did. They keep that piece of paper. **Two — book fifteen minutes each, privately, for the gate conversation.** A student with five of seven gates does not need reassurance, they need a named fortnight; a student with seven needs to be told to go and audit somebody else's code, because they now have the eyes for it. **Three — do not throw away the Bug Log, the FINDINGS sheet or the SIX BOXES sheet.** Photograph all three. Week 1 of Level 4 opens with a model that produces fluent, confident, completely wrong sentences, and the only defence anybody has against it is the habit written on those three sheets: **predict the number first, then check.** **Four — tell them to put the letter in an envelope with the date on it and actually keep it.** In about a year they will open it, and it will be the most interesting thing they read that week.

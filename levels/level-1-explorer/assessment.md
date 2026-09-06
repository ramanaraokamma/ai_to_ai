# ✅ Level 1 — Assessment Pack

**Level 1 · Assessment · ~2 hours · Prereqs: all nine Level 1 modules**

[⬅ Module 9](module-09-fair-private-honest-ai.md) · [Level 1 Home](README.md) · [Capstone](capstone.md) · [Glossary](glossary.md)

---

## 📋 How To Use This

This is not a test somebody is grading. It is a **mirror**. Its whole job is to show you which of the nine modules did not stick, so you can go back before the capstone rather than discovering the hole live in front of an adult.

```
   ┌──────────────────────────────────────────────────────────────────────┐
   │  THE RULES                                                           │
   ├──────────────────────────────────────────────────────────────────────┤
   │                                                                      │
   │   1.  Closed book. No module files open. No glossary.                │
   │   2.  Paper and pencil allowed — you will need them for Part C.      │
   │   3.  A calculator is allowed, but write the division down.          │
   │   4.  Do ALL 32 items before you open the answer key. All of them.   │
   │       Peeking after each question feels efficient and teaches you    │
   │       almost nothing.                                                │
   │   5.  Write "not sure" next to any answer you guessed. Those are     │
   │       the ones that matter, even when you guess right.               │
   │                                                                      │
   ├──────────────────────────────────────────────────────────────────────┤
   │  Part A — 20 multiple choice          ~35 min                        │
   │  Part B —  8 short answer             ~40 min                        │
   │  Part C —  4 applied / debug          ~45 min                        │
   └──────────────────────────────────────────────────────────────────────┘
```

**Scoring.** Part A: 1 mark each (20). Part B: 3 marks each (24). Part C: 4 marks each (16). **Total: 60.**

| Score | What it means | What to do |
|---|---|---|
| **0–29** | The core ideas haven't landed yet | Re-read Modules 1–4 and redo their mini-projects. Nothing after Module 4 makes sense without them. |
| **30–41** | You've got the vocabulary, not yet the reasoning | Look at *which* modules you lost marks in and redo those mini-projects. Then retake Part B only. |
| **42–52** | Solid. You are ready for the capstone. | Do the capstone. Keep this sheet next to you. |
| **53–60** | You could teach this | Do the capstone, then take a Should-have *and* a Could-have. Then Level 2. |

---

# 📝 Part A — Multiple Choice

*20 questions. One answer each. Tagged by module.*

---

**A1.** `[Module 1]` Which of these is the best definition of **artificial intelligence**?

- **(a)** A computer program that is smarter than a person
- **(b)** Getting a machine to do a job that used to need a person's judgement
- **(c)** A digital brain built out of software
- **(d)** Any computer that can do maths very fast

---

**A2.** `[Module 1]` Your school gate has a camera that reads number plates and lifts the barrier for cars on an approved list stored in a text file. Which family is this?

- **(a)** Generative AI, because it produces an action
- **(b)** Machine learning, because it uses a camera
- **(c)** Rule-based, because a human wrote the approved list and the if-then step
- **(d)** General AI, because it handles a real-world situation

---

**A3.** `[Module 1]` Which statement about today's AI systems is **true**?

- **(a)** Every AI system today is narrow — it does one job and is blank outside it
- **(b)** Large chatbots are general AI, because they can talk about anything
- **(c)** General AI was achieved in 2016 when AlphaGo beat the world champion
- **(d)** A system counts as general AI once it beats humans at its task

---

**A4.** `[Module 2]` You record the sleep hours of 30 students for one week. In the standard table shape, what is one **row**?

- **(a)** One student's sleep hours for all seven days
- **(b)** One measurement occasion — one student on one day
- **(c)** All 30 students' Monday readings
- **(d)** The column heading `sleep_hours`

*(Assume the table has the columns `student_id`, `date`, `sleep_hours`, `mood`.)*

---

**A5.** `[Module 2]` Here are four values from a `sleep_hours` column: `7.5`, `(blank)`, `88`, `6.0`. Which describes them correctly?

- **(a)** `88` is a missing value and `(blank)` is an outlier
- **(b)** `(blank)` is a missing value and `88` is an impossible value
- **(c)** Both `(blank)` and `88` are duplicates
- **(d)** `88` is a legal outlier and should be kept without comment

---

**A6.** `[Module 3]` You are writing a spam rulebook by hand. Every new tricky message makes you add one more rule, and each rule interacts with all the others. What is this called, and what does it tell you?

- **(a)** Overfitting — your rules memorised the messages
- **(b)** Rule explosion — the number of cases grows far faster than you can write rules, which is exactly why machine learning was invented
- **(c)** Class imbalance — you have more spam than ham
- **(d)** Hallucination — your rulebook is inventing answers

---

**A7.** `[Module 3]` Your rulebook scores 18/20 on the 20 messages you built it from, and 5/10 on 10 fresh messages. What is the most useful thing to say about the 18/20?

- **(a)** It proves the rulebook works well
- **(b)** It is meaningless, because those 20 messages are exactly what the rules were written from
- **(c)** It means the rulebook is 90% accurate
- **(d)** It shows the fresh messages were unfairly hard

---

**A8.** `[Module 4]` A table has the columns `weight_g`, `colour`, `length_cm`, `has_stem`, `fruit`. You want to predict what kind of fruit each row is. Which column is the **label**?

- **(a)** `weight_g`
- **(b)** `colour`
- **(c)** `fruit`
- **(d)** All of them together

---

**A9.** `[Module 4]` You are building a model to predict whether a fruit is an apple. Someone suggests adding a column called `sticker_says`, copied from the supermarket sticker on each fruit. What is this feature, and why?

- **(a)** A useful feature — it is highly accurate
- **(b)** A useless feature — stickers are random
- **(c)** A leaky feature — it already contains the answer and won't exist when you actually need a prediction
- **(d)** A category feature, which models cannot use

---

**A10.** `[Module 4]` Which of these tasks is **regression** rather than classification?

- **(a)** Deciding whether a message is spam or not spam
- **(b)** Predicting how many minutes of homework you will have tomorrow
- **(c)** Sorting rubbish into recycling, compost, or landfill
- **(d)** Naming which of three family members owns a water bottle

---

**A11.** `[Module 5]` Your model looks at a photo and reports: `spoon 62%, toothbrush 21%, comb 17%`. What does the 62% mean?

- **(a)** The model will be right 62 times out of 100 on photos like this
- **(b)** 62% of the training photos were spoons
- **(c)** The model's guess strength for `spoon` — how strongly it prefers that class over the others. It says nothing about whether it is correct
- **(d)** The photo is 62% similar to a spoon

---

**A12.** `[Module 5]` You train a three-class model with 200 photos of spoons, 200 of toothbrushes, and 8 of combs. What is the main problem?

- **(a)** Nothing — more data is always better
- **(b)** Class imbalance: the model barely saw combs, so it will rarely and badly predict `comb`
- **(c)** Overfitting, because 408 photos is too many
- **(d)** The confidence scores will no longer add to 100%

---

**A13.** `[Module 6]` Why must you never test a model on the same examples it trained on?

- **(a)** It makes training slower
- **(b)** It uses up the photos
- **(c)** Because a model that simply memorised those exact examples would score perfectly, so the score cannot tell memorising apart from actually learning
- **(d)** Because the confidence scores become unreliable

---

**A14.** `[Module 6]` A model gets 27 correct out of 36 held-out photos. Express this as a decimal and a percentage.

- **(a)** 0.75 and 75%
- **(b)** 0.72 and 72%
- **(c)** 0.27 and 27%
- **(d)** 1.33 and 133%

---

**A15.** `[Module 6]` Two models are tested. Which one is most likely **overfitting**?

| Model | Training accuracy | Test accuracy |
|---|---|---|
| P | 100% | 96% |
| Q | 100% | 41% |
| R | 58% | 55% |
| S | 88% | 85% |

- **(a)** Model P
- **(b)** Model Q
- **(c)** Model R
- **(d)** Model S

---

**A16.** `[Module 7]` In a grayscale image, a pixel holds the value `0`. What does that mean, and how many numbers does the same pixel need in RGB?

- **(a)** `0` means white; RGB needs 1 number
- **(b)** `0` means black; RGB needs 3 numbers (red, green, blue)
- **(c)** `0` means transparent; RGB needs 4 numbers
- **(d)** `0` means the pixel is empty; RGB needs 256 numbers

---

**A17.** `[Module 7]` You slide a 3×3 filter over a 12×12 grayscale image, one step at a time, only where the filter fits completely. How big is the output grid?

- **(a)** 12 × 12
- **(b)** 11 × 11
- **(c)** 10 × 10
- **(d)** 9 × 9

---

**A18.** `[Module 8]` Tokenize `"The cat sat."` using the Module 8 rules (lowercase everything, punctuation is its own token). How many tokens?

- **(a)** 3
- **(b)** 4
- **(c)** 5
- **(d)** 11

---

**A19.** `[Module 8]` In a corpus, the word `the` is followed by: `cat` twice, `dog` twice, `mat` once, `fish` once, `rug` once, `bone` once. If you sample the next word using these counts, what is the chance of getting `cat`?

- **(a)** 2% — it happened twice
- **(b)** 25% — 2 out of 8
- **(c)** 33% — 2 out of 6 different words
- **(d)** 50% — `cat` and `dog` are tied for most common

---

**A20.** `[Module 9]` A face-detection product is 99.2% accurate on lighter-skinned men and 65.3% accurate on darker-skinned women. What is the accuracy gap, and where did it most likely come from?

- **(a)** A gap of 33.9 percentage points, most likely caused by a bug in the code
- **(b)** A gap of 33.9%, meaning the model is 33.9% broken
- **(c)** A gap of 33.9 percentage points, most likely caused by the training data containing far more of one group than the other
- **(d)** No real gap — the overall average is still high, so the product is fine

---

# ✍️ Part B — Short Answer

*8 questions. Aim for 3–6 sentences each, unless the question asks for numbers. Show arithmetic where there is any.*

---

**B1.** `[Modules 1, 3]` Your phone's calculator app and your phone's photo app both do something clever: the calculator computes square roots, and the photo app groups pictures of your dog into an album. **Only one of them is AI.** Say which, and explain your reasoning using the word **judgement** and one of the three families from Module 1.

---

**B2.** `[Module 2]` Below is a fragment of somebody's dataset.

| id | name | age | favourite_colour | screen_min |
|---|---|---|---|---|
| 1 | Asha | 11 | blue | 145 |
| 2 | Ravi | 12 | Blue | 132 |
| 3 | Asha | 11 | blue | 145 |
| 4 | Meera | 211 | green | |

Name **three distinct data-quality problems** you can see, say which row(s) each affects, and say what you would do about each one. Then name one thing that is wrong with this table that is not about the values at all.

---

**B3.** `[Module 3]` A friend says: *"Machine learning is just a lazy way of writing rules. If you had enough time, you could always write the if-then rules yourself and get the same answer."* Write a reply of about five sentences. Use the phrase **rule explosion** and give one concrete example with a number in it.

---

**B4.** `[Modules 4, 6]` You want to predict whether a student will hand their homework in on time. You have these possible features:

```
   minutes_of_homework_set   ·   day_of_week   ·   student_shoe_size
   was_it_handed_in_late     ·   teacher_name  ·   student_id_number
```

Sort them into **useful**, **useless**, and **leaky**, and justify each placement in one line. Then state whether this task is classification or regression, and what the **baseline** would be if 80% of students hand homework in on time.

---

**B5.** `[Module 5]` You train a model on 40 photos per class and it works well. Testing your three objects one at a time, the **top confidence** for each is `91%`, `88%`, `79%`. You then retrain with only 5 photos per class, test the same three objects in the same place, and the top confidences fall to `54%`, `49%`, `47%`.

Explain **why** the numbers fell, in terms of what training actually does. Then work out what must have happened to the **margin**, and explain why the margin is more informative than the top score on its own.

---

**B6.** `[Module 6]` Here is a confusion matrix from 15 held-out photos, 5 per class.

```
                       PREDICTED
                  spoon  toothbrush  comb
   TRUE  spoon      5         0        0
         toothbrush 0         4        1
         comb       1         2        2
```

(a) Compute the overall accuracy as a fraction, a decimal, and a percentage.
(b) Compute the per-class accuracy for each of the three classes.
(c) State the single most useful sentence you can say about this model that the overall accuracy number **hides**.

---

**B7.** `[Modules 7, 8]` A chatbot writes a beautifully-worded paragraph claiming that penguins live in the Sahara. A vision model confidently labels a photo of a wolf as `dog` at 94%. **In your own words, explain what these two failures have in common**, and name the term Module 8 gave to the chatbot's version of it.

---

**B8.** `[Module 9]` You trained a model on 183 daylight photos and 17 lamplight photos. It scores 91% in daylight and 42% under a lamp.

(a) State the accuracy gap in the correct unit.
(b) Trace the failure back through the four links of the bias chain, naming each link.
(c) You want lamplight to be at least one-third of your training data. You will keep all 183 daylight photos. **How many lamplight photos do you need in total, and how many more must you take?** Show the arithmetic.

---

# 🔧 Part C — Applied & Debug

*Four broken things. For each: say what is wrong, why it happens, and write the fix.*

---

## C1 — The spreadsheet edge filter is broken

`[Module 7]`

A learner is doing the Pixel Lab. Their image sits in `B2:G7` and is a white 4×4 square on a black background:

```
        B     C     D     E     F     G
   2    0     0     0     0     0     0
   3    0    255   255   255   255    0
   4    0    255   255   255   255    0
   5    0    255   255   255   255    0
   6    0    255   255   255   255    0
   7    0     0     0     0     0     0
```

They type this into `C12` and fill it across `C12:F15`:

```
=MIN(255, ((D2+D3+D4)-(B2+B3+B4)) + ((B4+C4+D4)-(B2+C2+D2)))
```

They get this edge map, which does not look like a hollow square at all:

```
              C      D      E      F
   12       255    255    255      0
   13       255      0      0   -765
   14       255      0      0   -765
   15         0   -765   -765  -1020
```

**(a)** What single thing is missing from the formula?
**(b)** Cell `F12` came out as **0**, even though it sits on the top-right corner of the white square, where the edge should be strongest. Work through the arithmetic for `F12` and explain exactly why it collapsed to zero.
**(c)** Write the corrected formula and state what `C12:F15` should read.
**(d)** A second learner instead types `=MIN(255, ABS(($D$2+$D$3+$D$4)-($B$2+$B$3+$B$4)) + ABS(($B$4+$C$4+$D$4)-($B$2+$C$2+$D$2)))` and fills it across. What will they see, and why?

---

## C2 — The Scratch chatbot spams the same reply

`[Modules 8, Capstone]`

Here is a learner's Scratch script for a booth app that reacts to a Teachable Machine model.

```
when green flag clicked

    set image classification model URL [https://teachablemachine.../models/AbCd/]
    toggle video [on v]

    forever

        if <(image label) = [recycling]> then
            say [RECYCLING - blue bin!] for (3) seconds
            change [count v] by (1)
        end

        if <(image label) = [compost]> then
            say [COMPOST - green bin!] for (3) seconds
            change [count v] by (1)
        end

        if <(image label) = [landfill]> then
            say [LANDFILL - black bin.] for (3) seconds
            change [count v] by (1)
        end

    end
```

When they hold up a can, the sprite says "RECYCLING - blue bin!" over and over, the `count` variable races up to 40 in ten seconds, and the stage becomes sluggish. Also, when they hold up a set of car keys, the app says "LANDFILL - black bin."

**(a)** Name the two separate bugs.
**(b)** Explain why `count` reaches 40 in ten seconds even though only one can was shown.
**(c)** Rewrite the script fixing both bugs. Add a confidence threshold so that anything under 70% says "not sure" instead of guessing.

---

## C3 — The test report that proves nothing

`[Modules 5, 6, 9]`

A learner hands in this write-up.

```
   ══════════════════════════════════════════════════
   MY MODEL — RESULTS
   ══════════════════════════════════════════════════
   Classes:  cat (300 photos), dog (300 photos),
             hamster (11 photos)

   I trained the model on all 611 photos.
   Then I tested it on 20 photos and got 19 right.

   ACCURACY: 95%

   My model is very accurate and could be used by a
   vet's office to identify pets automatically.
   ══════════════════════════════════════════════════
```

You later find out that the 20 test photos were picked at random **from the same 611**, and that 10 were cats, 9 were dogs, and 1 was a hamster.

**(a)** Identify **four** separate problems with this report.
**(b)** For the biggest problem, explain exactly why the 95% figure cannot be trusted.
**(c)** Rewrite the report as it should have been done — describe the process, not invented numbers.
**(d)** Write the one-line "DO NOT USE THIS FOR" statement this model needs.

---

## C4 — The bigram table doesn't add up

`[Module 8]`

A learner tallies bigrams for this corpus, using the Module 8 rules (lowercase; `.` is its own token; do **not** count a pair that crosses a `.`):

```
   The dog ran. The dog ate. The cat ran.
```

They produce this table:

| Current word | Next word | Count | Out of | Chance |
|---|---|---:|---:|---:|
| the | dog | 2 | 3 | 66% |
| the | cat | 1 | 3 | 33% |
| dog | ran | 1 | 2 | 50% |
| dog | ate | 1 | 2 | 50% |
| cat | ran | 1 | 1 | 100% |
| ran | . | 1 | 1 | 100% |
| ate | . | 1 | 1 | 100% |
| . | the | 2 | 2 | 100% |

**(a)** Tokenize the corpus and state the total token count.
**(b)** Compute how many bigrams there should be, using the arithmetic check from Module 8. Compare with the learner's table total.
**(c)** Find the **two** errors in the table and correct them.
**(d)** Using your corrected table, generate one sentence starting from `the`, and state clearly which choices were forced and which were random.

---

---

# ✅ Answer Key

<details>
<summary><b>Click to reveal answers</b> — only after you have attempted all 32 items</summary>

---

## Part A — Multiple Choice

### A1 — `(b)` ✅

> **Artificial intelligence** — getting a machine to do a job that used to need a person's judgement.

The word to circle is **judgement**: a choice where reasonable people could disagree and the answer depends on the specific case.

| Option | Verdict | Why |
|---|---|---|
| (a) smarter than a person | ❌ | "Smart" is exactly the word Module 1 banned. A calculator is faster than you at arithmetic and is not AI; AlphaGo was better than any human at Go and could not play checkers. Being better at a task is neither necessary nor sufficient. |
| **(b)** | ✅ | Names the job and the judgement, and says nothing about *how* the machine does it. A submarine doesn't swim like a fish. |
| (c) digital brain | ❌ | "Brain" is the other banned word. Nothing inside these systems resembles a brain, and the metaphor is what makes people over-trust them. |
| (d) does maths fast | ❌ | Speed isn't judgement. Sorting 200 numbers has one exact answer and one exact method — no judgement, no AI. |

---

### A2 — `(c)` ✅

A human wrote the list of approved plates and the step `IF plate is on the list THEN lift barrier`. That is a rule-based system — predictable and fully explainable. You can point at the exact line that caused the answer.

⚠️ The subtle bit: the *number-plate reader* inside it almost certainly **is** machine learning (reading characters from pixels was learned from examples). Real products are usually a stack: a learned component feeding a rule-based component. Recognising that stack is a top-mark answer.

| Option | Verdict | Why |
|---|---|---|
| (a) generative | ❌ | Generative AI produces **new content** — text, images, sound. Lifting a barrier is an action selected from two options, not content generated. |
| (b) ML because camera | ❌ | The input device is irrelevant. What matters is *who wrote the rule*. A thermostat with a fancy sensor is still a thermostat. |
| **(c)** | ✅ | A human wrote the list and the if-then. |
| (d) general AI | ❌ | General AI doesn't exist. This gate cannot do anything except lift for listed plates. |

---

### A3 — `(a)` ✅

Every real system today is **narrow**: one job, blank outside it.

| Option | Verdict | Why |
|---|---|---|
| **(a)** | ✅ | The defining property of all current AI. |
| (b) chatbots are general | ❌ | A chatbot produces text on any topic — that's a wide *range within one job* (next-word prediction), not general intelligence. It cannot drive, feel tired, or learn a new skill from one demonstration. |
| (c) AlphaGo 2016 | ❌ | AlphaGo is the textbook example of narrowness: world-beating at Go, incapable of checkers. |
| (d) beating humans = general | ❌ | A pocket calculator beat humans at long division in 1972. Nobody called it general intelligence. |

---

### A4 — `(b)` ✅

The columns are `student_id`, `date`, `sleep_hours`, `mood`. Because `date` is a column, **one row = one student on one day** — one measurement occasion.

The general rule: a row is *one example*, and what counts as an example is decided by your columns. 30 students × 7 days = 210 rows.

| Option | Verdict | Why |
|---|---|---|
| (a) one student, all week | ❌ | That would be the shape if the columns were `student_id, mon, tue, wed…`. With a `date` column, one week of one student is seven rows. |
| **(b)** | ✅ | Matches the given columns. |
| (c) all Mondays | ❌ | That's a *slice* of 30 rows, not one row. |
| (d) the heading | ❌ | Headings live in the header row and name columns; they aren't examples. |

---

### A5 — `(b)` ✅

`(blank)` is a **missing value** — a box where a measurement should be. `88` is an **impossible value** — reality does not allow 88 hours of sleep in a night (a day has 24).

Handling: never silently delete. Mark the missing one and note *why* it's missing in the data card. For `88`, go back to the source if you can — it's probably `8.8` or `8` with a typo. If you can't check, mark it missing rather than inventing a number.

| Option | Verdict | Why |
|---|---|---|
| (a) swapped | ❌ | Reverses both definitions. |
| **(b)** | ✅ | Correct on both. |
| (c) duplicates | ❌ | A duplicate is the *same example recorded twice*. Neither of these is that. |
| (d) legal outlier | ❌ | An **outlier** is a *legal* value far from the others (480 screen-minutes in a week of 150s). 88 hours of sleep isn't legal — it's impossible. And "keep without comment" is wrong for outliers too. |

---

### A6 — `(b)` ✅

**Rule explosion**: the number of situations grows far faster than the rules you can write. Module 3's number: 30 independent yes/no checks give 2³⁰ ≈ 1.07 **billion** possible situations. No human writes a rulebook for that.

This is precisely the moment machine learning becomes the better trade: stop writing rules, hand over labelled examples instead.

| Option | Verdict | Why |
|---|---|---|
| (a) overfitting | ❌ | Overfitting is about a *trained model* fitting its training examples too closely. You haven't trained anything — you're hand-writing rules. |
| **(b)** | ✅ | The exact definition, plus the reason it matters. |
| (c) class imbalance | ❌ | That's about unequal numbers of examples per class. Not what's described. |
| (d) hallucination | ❌ | Hallucination is a *generative* system producing fluent falsehood. A rulebook can be wrong but it never invents. |

---

### A7 — `(b)` ✅

The 18/20 is measured on the examples the rules were built from. Of course it's high — you tuned the rules until it was. It measures your ability to describe 20 messages, not your ability to catch spam.

The 5/10 on fresh messages is the honest number. This is the *same* idea as Module 6's train/test split, met one module earlier with rules instead of a model.

| Option | Verdict | Why |
|---|---|---|
| (a) proves it works | ❌ | The exact trap. Module 6's exam analogy: an exam made of the practice questions produces a lovely number and measures nothing. |
| **(b)** | ✅ | Names why the number is uninformative. |
| (c) "90% accurate" | ❌ | The arithmetic (18/20 = 90%) is right, but reporting it as *the* accuracy is the dishonesty. Always say which set a number came from. |
| (d) unfairly hard | ❌ | Fresh messages are the whole point. If they feel unfair, that's a finding about your rules, not the messages. |

---

### A8 — `(c)` ✅

The **label** is the answer you want the machine to produce — here, `fruit`. Everything else (`weight_g`, `colour`, `length_cm`, `has_stem`) is a **feature**: a measured description.

Quick test: cover one column. If covering it makes the row into a question, it's the label.

| Option | Verdict | Why |
|---|---|---|
| (a) weight_g | ❌ | A feature. It *could* be a label in a different task ("predict the weight from the other columns"), which shows label vs feature is decided by the task, not the column. |
| (b) colour | ❌ | A feature — a very useful one (Module 4: 91.7% on its own) but still an input. |
| **(c)** | ✅ | The thing you want predicted. |
| (d) all of them | ❌ | There is exactly one label column per task. |

---

### A9 — `(c)` ✅

A **leaky feature** already contains the answer, and won't be available when you actually need a prediction. If the sticker says APPLE, the model learns "read the sticker" and scores ~100% in testing — then fails completely on any fruit without a sticker, which is every fruit in a real fruit bowl.

The test: *will this value exist, and be trustworthy, at the moment I need a prediction?* If no, it's leaky.

| Option | Verdict | Why |
|---|---|---|
| (a) useful | ❌ | It looks brilliant in testing. That's what makes leakage dangerous rather than merely bad — leaky features are recognised by a *suspiciously good* score. |
| (b) useless | ❌ | A useless feature (like `quadrant`, which scored exactly the 33.3% baseline) makes no difference. This one makes a huge, fake difference. |
| **(c)** | ✅ | Names it and gives the reason. |
| (d) models can't use categories | ❌ | Categories are used constantly. `colour` is a category and was the best feature in Module 4. |

---

### A10 — `(b)` ✅

**Regression** predicts a number on a sliding scale. "How many minutes of homework" is a number: 47, 12, 130.

| Option | Verdict | Why |
|---|---|---|
| (a) spam / not spam | ❌ | Binary classification — two boxes. |
| **(b)** | ✅ | A number, so regression. Note: bucket it into "0–30 / 30–60 / 60+" and it becomes classification. The task shape, not the world, decides. |
| (c) three bins | ❌ | Multi-class classification — three boxes. |
| (d) which family member | ❌ | Multi-class classification — three named boxes. |

---

### A11 — `(c)` ✅

A **confidence score** is the model's guess *strength*, not its correctness. The three scores always sum to 100% because they are shares of the model's belief — they must go somewhere.

The model can be 99% confident and wrong (Module 9 asks you to find and display your own worst case), and 51% confident and right.

| Option | Verdict | Why |
|---|---|---|
| (a) right 62/100 times | ❌ | The most tempting distractor and the one people believe. Confidence is not a measured hit rate. Only a held-out test set (Module 6) gives you that. |
| (b) 62% of training photos | ❌ | That's class balance, a completely different number, fixed at training time and identical for every photo you show it. |
| **(c)** | ✅ | Guess strength, and it says nothing about correctness. |
| (d) 62% similar | ❌ | There's no "percent similar" being computed. Also, if it were similarity, the three numbers would have no reason to add to 100%. |

---

### A12 — `(b)` ✅

**Class imbalance.** The model saw 200 spoons, 200 toothbrushes, 8 combs. It has almost no idea what a comb looks like, and it also learns that guessing `comb` is rarely a good bet — so `comb` predictions become both rare and unreliable.

Worse, the imbalance can *hide*: if your test set is also 200/200/8, blind guessing scores about 49% and the comb failure barely moves the overall number. This is exactly Module 6's "a single accuracy number can hide a serious problem".

**Fix:** collect more combs (best), or cut the other two classes down to match (wasteful but fast). Module 5's target: (biggest − smallest) ÷ biggest under 20%. Here it is (200 − 8) ÷ 200 = **96%**.

| Option | Verdict | Why |
|---|---|---|
| (a) more is always better | ❌ | Module 5's headline: data *quality and balance* beat quantity. 40 varied photos beat 400 identical ones. |
| **(b)** | ✅ | Names it and says what it does. |
| (c) overfitting from too many | ❌ | Overfitting comes from too *few* and too *similar* examples, not too many. |
| (d) won't sum to 100% | ❌ | They always sum to 100%. That's how the scores are constructed. |

---

### A13 — `(c)` ✅

A model that memorised the training examples perfectly would score 100% on them. So would a model that genuinely learned. **The score cannot tell the two apart** — which means it isn't a measurement at all.

Module 6's exam analogy: a teacher who sets an exam made of the exact practice questions gets a room full of full marks and learns nothing about whether anyone can do maths.

| Option | Verdict | Why |
|---|---|---|
| (a) slower | ❌ | Testing takes the same time either way. It's an honesty problem, not a speed one. |
| (b) uses up photos | ❌ | Photos aren't consumed. (Held-out photos *are* "spent" in a different sense — every time you tweak based on the test score you leak a little of it — but that's not this.) |
| **(c)** | ✅ | The measurement can't distinguish memorising from learning. |
| (d) confidence unreliable | ❌ | Confidence scores are already not a measure of correctness (A11). This isn't the reason. |

---

### A14 — `(a)` ✅

```
   FRACTION:    27/36

   DECIMAL:     27 ÷ 36
                36 × 0.7  = 25.2   →  remainder 27 − 25.2 = 1.8
                1.8 ÷ 36  = 0.05
                0.7 + 0.05 = 0.75

   PERCENTAGE:  0.75 × 100 = 75%

   CHECK:       27/36 simplifies (÷9) to 3/4 = 0.75  ✓
```

| Option | Verdict | Why |
|---|---|---|
| **(a)** | ✅ | 27/36 = 3/4 = 0.75 = 75%. |
| (b) 0.72 | ❌ | That's 26/36 (0.722). Close-but-wrong options are there to make you actually divide. |
| (c) 0.27 | ❌ | Reading the numerator as the answer. A decimal accuracy is always between 0 and 1 and must come from the division. |
| (d) 1.33 | ❌ | That's 36 ÷ 27 — the division upside down. Accuracy can never exceed 1.00 / 100%. |

---

### A15 — `(b)` ✅

**Model Q: 100% training, 41% test.** A 59-percentage-point gap. It learned the photos, not the object.

| Model | Gap | Reading |
|---|---:|---|
| P | 4 pts | Generalizing well ✅ |
| **Q** | **59 pts** | **Memorizing hard ❌** |
| R | 3 pts | Not overfitting — it learned almost *nothing*. Underfitting: too little data, or the task is too hard 🟠 |
| S | 3 pts | Healthy ✅ |

The signature of overfitting is always the same: **high training accuracy, much lower test accuracy.** The gap is the diagnosis, not either number alone.

| Option | Verdict | Why |
|---|---|---|
| (a) P | ❌ | 4-point gap. That's what success looks like. |
| **(b)** | ✅ | The 59-point gap. |
| (c) R | ❌ | Tempting because 55% looks bad, but the *gap* is only 3 points. This model isn't memorising, it's failing to learn — a different disease with a different cure (more/better data, or an easier task). |
| (d) S | ❌ | 3-point gap and both numbers are decent. |

---

### A16 — `(b)` ✅

Grayscale runs **0 = black → 255 = white**, one number per pixel. **RGB** stores three numbers per pixel — the red, green, and blue amounts — which you can picture as three stacked grids called **channels**.

Handy check: (255, 255, 0) is yellow, because red light plus green light makes yellow. Light mixes differently from paint.

| Option | Verdict | Why |
|---|---|---|
| (a) 0 = white | ❌ | Backwards. 0 is the absence of light, so black. The single most common slip in Module 7's Pixel Lab. |
| **(b)** | ✅ | Both halves correct. |
| (c) transparent, 4 numbers | ❌ | Some formats add a fourth transparency channel (RGBA), but RGB itself is three, and 0 in grayscale means black, not transparent. |
| (d) 256 numbers | ❌ | Confuses the *range* of each value (0–255, which is 256 possible values) with the *count* of values per pixel (3). |

---

### A17 — `(c)` ✅

Sliding a 3×3 filter only where it fits completely loses one pixel from each edge:

```
   output width  = 12 − 2 = 10
   output height = 12 − 2 = 10
   →  10 × 10
```

The general rule for an *n*×*n* filter on a *W*×*H* image is (W − n + 1) × (H − n + 1). For n = 3 that's W − 2. In Module 7 the 6×6 image gave a 4×4 edge map — same rule.

| Option | Verdict | Why |
|---|---|---|
| (a) 12×12 | ❌ | You'd only get this by padding the border with invented pixels — a real technique, but not what "only where it fits completely" means. |
| (b) 11×11 | ❌ | Subtracting 1 instead of 2. You lose a pixel from *each* side. |
| **(c)** | ✅ | 12 − 2 = 10. |
| (d) 9×9 | ❌ | Subtracting 3 (the filter size) instead of 2 (filter size − 1). |

---

### A18 — `(b)` ✅

```
   "The cat sat."
   →  the  ·  cat  ·  sat  ·  .
   =  4 tokens
```

Lowercase `The` → `the`, and the full stop is its own token.

| Option | Verdict | Why |
|---|---|---|
| (a) 3 | ❌ | Forgot the `.`. Punctuation carries real information — it's how you know a sentence ended — which is why Module 8 keeps it. |
| **(b)** | ✅ | Three words plus the full stop. |
| (c) 5 | ❌ | Probably counted `The` and `the` as separate, or split `sat.` into `sat`, `.`, and something else. |
| (d) 11 | ❌ | That's the character count of `The cat sat` — characters, not tokens. |

---

### A19 — `(b)` ✅

```
   followers of "the":   cat 2 · dog 2 · mat 1 · fish 1 · rug 1 · bone 1
   total                = 2+2+1+1+1+1 = 8

   chance of cat        = 2/8 = 0.25 = 25%
```

You divide by the total number of *times* `the` was followed by anything (8), not by the number of *different* words (6). Picture Module 8's slip bag: 8 slips go in, two of them say `cat`.

| Option | Verdict | Why |
|---|---|---|
| (a) 2% | ❌ | Treats a raw count as a percentage. A count is not a chance until you divide by the total. |
| **(b)** | ✅ | 2 out of 8. |
| (c) 33% | ❌ | 2/6 — dividing by the count of distinct followers. This would make `bone` (1 slip) as likely as… well, it breaks: the six chances would sum to more than 100%. Always sanity-check that the group's chances add to 100%: 25+25+12.5+12.5+12.5+12.5 = 100 ✓ |
| (d) 50% | ❌ | 2/4, as if only `cat` and `dog` were in the bag. The rarer followers are still in there. |

---

### A20 — `(c)` ✅

```
   99.2% − 65.3% = 33.9 percentage points
```

**Percentage points** is the correct unit when you subtract two percentages. And the cause is almost never a bug: somebody assembled a training set that contained far more of one group than another, the model learned what it was shown, and the testing was done as one overall average that hid the hole.

Nothing was broken. That's what makes it hard to catch — and why splitting the score by group is the whole technique.

| Option | Verdict | Why |
|---|---|---|
| (a) a bug | ❌ | Right arithmetic, wrong cause. A bug would produce crashes or nonsense, not smooth, confident, systematically-worse answers for one group. |
| (b) "33.9%" broken | ❌ | Wrong unit *and* a meaningless claim. A model isn't "33.9% broken"; it works differently for different groups. |
| **(c)** | ✅ | Correct unit, correct cause. |
| (d) average is fine | ❌ | This is precisely the reasoning that let those products ship. If your test population is mostly the group the model is good at, the average will look great and stay great right up until it matters. |

---

## Part B — Short Answer

### B1 — Calculator vs photo app

**Model answer.**

The photo app is the AI. The calculator is not.

Computing a square root does not need **judgement**: there is exactly one right answer and one exact method, and no two reasonable people would disagree about it. Speed doesn't change that — a fast calculator is still just a calculator.

Grouping photos of my dog does need judgement. Whether *this* blurry photo at *this* angle shows my dog or next door's is a case-by-case decision, and two people could genuinely disagree. Nobody wrote if-then rules for it either; the system was shown enormous numbers of labelled photos and found the pattern itself. That puts it in the **machine learning** family.

**Mark scheme (3):** 1 for picking the photo app · 1 for using *judgement* correctly (one exact answer vs case-by-case disagreement) · 1 for naming machine learning and saying nobody wrote the rules.

**Bonus insight:** the calculator *interface* might use a learned handwriting recogniser if you write the sum. The maths is rule-based; the reading of it might not be. Real products are stacks.

---

### B2 — The messy table

**Three data-quality problems:**

| Problem | Row(s) | What I'd do |
|---|---|---|
| **Duplicate** — Asha appears twice with identical values (`id` 1 and 3) | 1 and 3 | Check whether these are truly the same measurement or two different people called Asha. If truly duplicated, delete row 3 and note the deletion. Never silently delete — a duplicate may be telling you your collection process double-fires. |
| **Impossible value** — `age = 211` | 4 | Almost certainly a typo for 11 or 21. Go back to the source and check. If you can't, mark it missing rather than guessing, and note it in the data card. |
| **Inconsistent category** — `blue` vs `Blue` | 2 (vs 1, 3) | A computer treats these as two different categories. Fix with a **controlled vocabulary**: decide all colours are lowercase, then apply it everywhere. |
| **Missing value** — `screen_min` is empty | 4 | Mark it explicitly (e.g. `NA`) rather than leaving a blank that could be read as zero. Record *why* it's missing if you know. |

**Not about the values at all:** the `name` column is **personal data**. Combined with age and favourite colour, it identifies a real child. If this table ever leaves your laptop, that's a privacy problem — replace names with IDs and keep the name↔ID mapping separately, or drop names entirely. (A related answer also earns the mark: there is no data card, so nobody knows who collected this, when, or with whose permission.)

**Mark scheme (3):** 1 for three correctly named and located problems · 1 for a sensible action on each (with "don't silently delete or invent") · 1 for a structural issue — personal data or missing provenance.

---

### B3 — Reply to "ML is just lazy rule-writing"

**Model answer.**

You're right that rules and learned models are trying to do the same job. Where it falls down is counting. Rules don't add up one at a time — they multiply, because each new condition combines with all the ones you already have. With just 30 independent yes/no checks in a spam filter you already have 2³⁰, about **1.07 billion**, distinct situations to cover, and that's before anyone invents a new trick. That's **rule explosion**, and it isn't a matter of having enough time — it's a wall.

There's a second problem that time can't fix either: for a lot of jobs, nobody can *state* the rule. Write me the if-then rules that tell a photo of a wolf from a photo of a husky. You know the difference instantly and you cannot write it down in pixel values.

So the **machine learning trade** is: give up writing rules, and give the machine labelled examples instead. You lose explainability — nobody can point at line 47 and say "that's why". You gain the ability to do jobs where the rules can't be written at all.

**Mark scheme (3):** 1 for using *rule explosion* correctly · 1 for a concrete number (2³⁰ ≈ 1 billion, or Module 3's 258 rules) · 1 for naming what is *given up* — explainability — and not just cheerleading for ML.

---

### B4 — Homework features

| Feature | Class | Why |
|---|---|---|
| `minutes_of_homework_set` | **Useful** | Plausibly linked to lateness — more work, more chance of running out of time. Available before the deadline. |
| `day_of_week` | **Useful** | Fridays and match days genuinely differ. Cheap to record and available in advance. |
| `student_shoe_size` | **Useless** | No plausible link to handing homework in. It will add noise and may let the model latch onto a coincidence in a small dataset. |
| `was_it_handed_in_late` | **Leaky** | This *is* the answer, reworded. It doesn't exist until after the deadline — exactly when you no longer need a prediction. |
| `teacher_name` | **Useful, with a warning** | Different teachers set different deadlines and reminders, so it may predict well. But a model that treats one teacher's students as "probably late" is making a judgement about people, not homework. Flag it, and check whether it's really standing in for something fairer. |
| `student_id_number` | **Useless — and dangerously so** | It's an ID, not a measurement. With enough data a model can memorise which IDs were late before, which looks like learning and is pure memorising. In Module 6 terms it's a shortcut straight to overfitting. |

**Task type:** **classification** — binary, on-time vs late.

**Baseline:** always guess the most common class ("on time"), which is right 80% of the time. So **the baseline is 80%**, and a model scoring 82% has achieved almost nothing. Any claim about this model must be judged against 80%, not against 0%.

**Mark scheme (3):** 1 for correctly identifying `was_it_handed_in_late` as leaky · 1 for the useless pair with reasons (`shoe_size`, `student_id_number`) · 1 for "classification, baseline 80%".

---

### B5 — Why confidence fell with 5 photos

**Model answer.**

Training means the machine studies the labelled examples and adjusts itself until it can separate them. What it has to work with is *patterns that appear across the examples*. With 40 photos per class, a pattern has to survive lots of different angles, distances, backgrounds and lighting to be worth relying on — so what survives is something genuinely about the object. With 5 photos, almost anything is "consistent", because there's hardly anything to be inconsistent with. The pattern the model finds is thin, so when it meets a real object it recognises only a weak, partial match, and its belief gets spread across all three classes instead of concentrating on one.

The **margin** — top score minus second score — must have collapsed too, and you can prove it without being told the runner-up. In a three-class model the scores always sum to 100%. If the top score is 54%, the other two share 46%, so the runner-up is **at most 46%** and the margin is **at most 8 points**. Compare that with a top score of 91%: the other two share 9%, so the margin is **at least 82 points**. The model went from firmly committed to nearly indifferent.

That is why the margin is the more informative number. A top score of 54% might sound like "more than half sure", but with a margin under 8 points the smallest change in lighting flips the answer. **The top score tells you who won; the margin tells you how close the race was** — and a race that close is a coin toss wearing a percentage sign.

**Mark scheme (3):** 1 for explaining that fewer examples means a thinner, less reliable pattern · 1 for deducing that the margin must have collapsed (top 54% in a 3-class model ⇒ margin ≤ 8 points) · 1 for why margin beats top score — it shows how close the runner-up was.

---

### B6 — The confusion matrix

**(a) Overall accuracy.** The correct answers sit on the **diagonal**:

```
   diagonal = 5 (spoon) + 4 (toothbrush) + 2 (comb) = 11

   FRACTION:    11/15
   DECIMAL:     11 ÷ 15
                15 × 0.7 = 10.5   →  remainder 0.5
                0.5 ÷ 15 = 0.0333
                0.7 + 0.0333 = 0.7333
   PERCENTAGE:  0.7333 × 100 = 73.3%

   Baseline (3 equal classes) = 1/3 = 33.3%
   Gain = 73.3 − 33.3 = 40.0 percentage points
```

**(b) Per-class accuracy** — read across each row and divide by that row's total:

| True class | Row | Correct | Accuracy |
|---|---|---|---|
| spoon | 5 / 0 / 0 | 5 of 5 | **100%** |
| toothbrush | 0 / 4 / 1 | 4 of 5 | **80%** |
| comb | 1 / 2 / 2 | 2 of 5 | **40%** |

Check: 5 + 4 + 2 = 11 ✓ and (100 + 80 + 40) ÷ 3 = 73.3% ✓ (the classes are equal-sized, so the average of the per-class accuracies matches the overall).

**(c) The sentence the overall number hides:**

> "This model is useless at combs — it gets only 2 out of 5 — and when it's wrong about a comb it usually calls it a toothbrush."

73.3% sounds like a decent model. It is in fact a perfect spoon detector welded to a coin-flip comb detector. If combs are the thing you actually care about, this model is worthless, and the single headline number would never have told you. Reading the **off-diagonal cells** is what turns "it's a bit wrong" into "it confuses combs with toothbrushes" — which is actionable, because it points straight at collecting more comb photos in positions where combs don't look like toothbrushes.

**Mark scheme (3):** 1 for 11/15 = 0.733 = 73.3% with the division shown · 1 for the three per-class figures · 1 for a hiding-sentence that names **comb** *and* what it's confused with.

---

### B7 — What the penguin and the wolf have in common

**Model answer.**

Both systems produced a **confident output that had nothing to do with truth**, because neither system was ever checking truth in the first place.

The chatbot is a next-word guesser. It picks likely words given the words so far. "Penguins live in the" is very often followed by a place name in the text it learned from, and "Sahara" is a place name that fits the shape of the sentence perfectly. Fluency and truth are separate things: the sentence is well-formed because well-formed sentences are what it learned to produce, not because anything was verified. Module 8 calls this a **hallucination**.

The vision model is doing the visual version. It never sees "a wolf". It sees a grid of brightness numbers, and it has learned which patterns of numbers went with which label. A wolf's pattern of fur, ears and snout is extremely close to a husky's, and it saw thousands of huskies labelled `dog`. So it outputs `dog` at 94% — 94% being its guess *strength*, not a promise about correctness.

The shared lesson: **confidence is produced by the same machinery as the answer**, so it can't act as a check on the answer. Both systems are pattern-matchers that always produce their best-fitting output, and neither has any way to notice it is wrong.

**Mark scheme (3):** 1 for "confident but not truth-checking" as the shared property · 1 for naming **hallucination** · 1 for explaining that a confidence score is guess strength, not correctness.

---

### B8 — The lamplight gap

**(a) The gap.**

```
   91% − 42% = 49 percentage points
```

(Not "49%" — subtracting two percentages gives percentage **points**.)

**(b) The four-link chain:**

```
   WHO/WHAT GOT COLLECTED   →   TRAINING DATA IS SKEWED
   I took nearly all my         183 daylight vs 17 lamplight
   photos in the afternoon      (91.5% vs 8.5%)
   because that's when
   I was free
                    ↓
   MODEL LEARNS THE SKEW    →   WHO GETS BAD PREDICTIONS
   It got very good at          Anyone using this in the evening,
   daylight patterns and        under a lamp, or in winter —
   never learned what the       which for a kitchen bin sensor
   objects look like under      is most of the time it matters
   warm indoor light
```

Note the honest bit: **nothing broke.** No bug, no crash. The model learned exactly what it was shown. Bias is the default outcome of learning from examples, not an unlucky one.

**(c) The arithmetic.**

I want lamplight to be at least one-third of the training set, keeping all 183 daylight photos. Let `L` be the total number of lamplight photos I end up with.

```
   Requirement:      L  ≥  (1/3) × (183 + L)

   Multiply by 3:    3L ≥  183 + L
   Subtract L:       2L ≥  183
   Divide by 2:       L ≥  91.5   →  round up to 92

   Check:   92 ÷ (183 + 92) = 92 ÷ 275 = 0.3345 = 33.5%   ✓ (just over a third)

   I already have 17, so:
   photos still to take = 92 − 17 = 75
```

**Answer: 92 lamplight photos in total; 75 more to take.**

And the follow-through that turns this into a plan rather than a wish: after retraining, rerun the **identical** lamplight test batch and expect the 42% to move. Also rerun the daylight batch — it may drop slightly, which is a real trade-off and worth reporting rather than hiding.

**Mark scheme (3):** 1 for "49 percentage points" with the correct unit · 1 for the four-link chain with all four named · 1 for L = 92 and 75 more, with the algebra shown.

---

## Part C — Applied & Debug

### C1 — The broken edge filter

**(a) What's missing:** the two `ABS()` calls. The formula computes the V and H filter values but never strips the minus signs, so edges on one side come out negative.

Correct version:

```
=MIN(255, ABS((D2+D3+D4)-(B2+B3+B4)) + ABS((B4+C4+D4)-(B2+C2+D2)))
```

**(b) Why F12 collapsed to zero.** `F12` is the edge value for image pixel `F3`, so its patch is rows 2–4, columns E–G:

```
        E     F     G
   2    0     0     0
   3   255   255    0
   4   255   255    0
```

```
   V filter = right column (G) − left column (E)
            = (0 + 0 + 0) − (0 + 255 + 255)
            = 0 − 510  =  −510        ← the vertical edge, found correctly,
                                         but with a minus sign

   H filter = bottom row (row 4) − top row (row 2)
            = (255 + 255 + 0) − (0 + 0 + 0)
            = 510 − 0  =  +510        ← the horizontal edge, found correctly,
                                         with a plus sign

   sum with no ABS  =  −510 + 510  =  0
   MIN(255, 0)      =  0
```

**The two edges cancelled each other out.** `F3` is a corner — it has a vertical edge on its right *and* a horizontal edge above it. It is one of the strongest edge points in the whole image, and the broken formula reports **nothing there at all**. That is worse than a wrong number; it is a confident zero in exactly the place you were looking.

The reason `ABS` matters: a filter measures a *change* in brightness. Whether the change goes dark→bright or bright→dark is just a matter of which way you happened to slide the filter. An edge is an edge. `ABS` says "I care that it changed, not which direction it changed in." Without it, a left-hand edge scores +510 and an identical right-hand edge scores −510, and any corner where the two meet can cancel to zero.

*(You can see the same disease in the bottom-right cell: `F15` reads −1020, which after `MIN(255, −1020)` stays −1020 — a strong corner reported as the most negative number on the grid.)*

**(c) The corrected output.** With `ABS` in place, `C12:F15` reads:

```
      255   255   255   255
      255     0     0   255
      255     0     0   255
      255   255   255   255
```

A hollow square — the outline of the white block. The interior is 0 because inside a flat white region nothing changes, so there is no edge. The 255s are `MIN(255, …)` clipping much larger raw totals (the true values reach 1020 at the corners) back into displayable range.

**(d) The `$` version.** Every reference is locked absolute, so filling across `C12:F15` copies the *identical* formula into all 16 cells. Every cell computes the value for the patch around `C3` and you get:

```
      255   255   255   255
      255   255   255   255
      255   255   255   255
      255   255   255   255
```

A solid block — no outline, no information. The fix is to remove every `$`. Relative references are the entire point of the fill: they are what makes the spreadsheet *slide* the filter across the image, one step per cell. That sliding is the filter operation.

**Mark scheme (4):** 1 for spotting the missing `ABS` · 1 for the F12 arithmetic showing the two ±510 edges cancelling to 0 · 1 for the corrected hollow-square output · 1 for "all 16 cells identical, remove the `$`".

---

### C2 — The spamming Scratch bot

**(a) The two bugs.**

1. **No change-detection guard.** The `forever` loop re-evaluates the label continuously and re-fires the matching `if` block every single pass, even though the label hasn't changed. There is also no `wait`, so the loop runs as fast as the machine allows — which is what makes the stage sluggish.
2. **No `other` class handling.** Only three `if` blocks exist. When a model with no `other` class sees car keys, it must still pick one of the three classes it knows — the confidences always sum to 100%, so something always wins. The keys land in `landfill` and the app reports it as fact. There is no confidence threshold either, so a 38%-confident guess is announced exactly as loudly as a 96%-confident one.

**(b) Why `count` reaches 40 in ten seconds.** `say […] for (3) seconds` pauses that script for 3 seconds, but `change [count] by (1)` runs once per pass through the matching `if`. Over ten seconds the loop completes many passes: each cycle through the three `if` blocks costs about 3 seconds of `say`, but the label is *still* `recycling` on the next pass, so it fires again, and again. Add in the passes where the label flickers between classes as the can moves and the counter climbs relentlessly. `count` is counting **loop iterations while an item is visible**, not items sorted. Those are completely different quantities, and one can shows up as forty.

**(c) The fixed script.**

```
when green flag clicked

    set image classification model URL [https://teachablemachine.../models/AbCd/]
    toggle video [on v]

    set [threshold v] to (70)        · my confidence cut-off, in %
    set [last v] to [none]           · what we announced last time
    set [count v] to (0)             · items actually sorted

    forever

        wait (0.5) seconds           · FIX 1a: stop hammering the CPU

        ┌── FIX 1b: only act when the label CHANGES ──┐
        if <not <(image label) = (last)>> then

            set [last v] to (image label)

            ┌── FIX 2a: refuse to guess when unsure ──┐
            if <(image label confidence) > (threshold)> then

                if <(image label) = [recycling]> then
                    say [RECYCLING - blue bin!] for (3) seconds
                    change [count v] by (1)
                end

                if <(image label) = [compost]> then
                    say [COMPOST - green bin!] for (3) seconds
                    change [count v] by (1)
                end

                if <(image label) = [landfill]> then
                    say [LANDFILL - black bin.] for (3) seconds
                    change [count v] by (1)
                end

                ┌── FIX 2b: an honest answer for unknown things ──┐
                if <(image label) = [other]> then
                    say [I do not recognise that. I only know 3 kinds of rubbish.]
                        for (3) seconds
                end

            else
                say (join [Not sure - only ] (join (image label confidence) [% confident.]))
                    for (3) seconds
            end

        end
    end
```

**Also required, and not a Scratch fix:** retrain the model with a fourth class called `other`, filled with 40 photos of the bare table, hands, and random objects. No amount of Scratch can make a three-class model able to say "none of these" — the fix has to happen in the data. That's the real lesson of this bug.

⚠️ **Threshold units.** Check whether your extension reports confidence as `0.85` or `85`. Print it once with a `say` block and set `threshold` to match, or the comparison silently never fires.

**Mark scheme (4):** 1 for the missing change-guard · 1 for the missing `other` class / threshold · 1 for explaining `count` as counting loop passes, not items · 1 for a corrected script containing both the guard and the threshold.

---

### C3 — The report that proves nothing

**(a) Four problems.**

| # | Problem | Module |
|:--:|---|---|
| 1 | **Tested on training data.** The 20 test photos came from the same 611 the model trained on. There is no held-out set at all. | 6 |
| 2 | **Severe class imbalance.** 300 / 300 / 11. The hamster class is 3.7% of the data — (300 − 11) ÷ 300 = **96%** imbalance, far past the 20% target. | 5 |
| 3 | **No baseline, and a test set that hides the problem.** With 10 cats, 9 dogs and 1 hamster in the test set, always guessing "cat" scores 50%. Also, a *single* hamster photo means the hamster class is measured at either 0% or 100% — a coin flip dressed as a measurement. | 4, 6 |
| 4 | **A deployment claim with nothing behind it.** "Could be used by a vet's office" is a claim about a real setting with real consequences, supported by a number that measures nothing. There is no per-class accuracy, no confusion matrix, no `other` class for the animals a vet actually sees, and no statement of limits. | 6, 9 |

*(Also acceptable as a fifth: no data card, so nobody knows where the photos came from, who took them, or whether the hamster photos are 11 shots of the **same** hamster — which they almost certainly are.)*

**(b) Why 95% cannot be trusted — the biggest problem.**

The test photos were drawn from the training photos. A model that had done nothing but memorise those 611 images would also score about 95% here. So the number cannot distinguish "learned what a cat looks like" from "recognised photo #418" — and a measurement that cannot distinguish success from failure isn't a measurement.

It gets worse when you look at *which* 20. Nineteen of the twenty were cats or dogs, the two classes with 300 photos each. Effectively the report measures the model on the easy half of its job and then generalises to all of it. The one hamster photo carries the entire weight of the class that everything is likely to fail on. Whether that single photo happened to be right or wrong swings the "hamster accuracy" between 0% and 100%, and either way the headline barely moves.

**(c) How it should have been done.**

```
   ══════════════════════════════════════════════════════════════
   MY MODEL — RESULTS  (the honest version)
   ══════════════════════════════════════════════════════════════

   1. THE CLASSES AND THE BALANCE
      cat, dog, hamster, other.
      Collect enough hamster photos to get within 20% of the others
      (or cut cat and dog down to match hamster — wasteful, but
      honest). Report the final counts per class.
      Add an `other` class: rabbits, guinea pigs, empty baskets,
      hands, the vet's table.

   2. THE SPLIT — done BEFORE any training
      Hold out 20% of EACH class, separately, so the test set has
      the same shape as the data. Move those files to heldout/.
      Never train on them. State how many photos that is.

   3. TRAINING
      Train on the training folder only. Save the project file.

   4. THE TEST
      Score every held-out photo once, on paper, as it happens.
      No retakes.
      Report:  overall accuracy as fraction -> decimal -> percentage
               the BASELINE (with 4 balanced classes, 25%)
               per-class accuracy, one line each
               a confusion matrix, so the confusions are visible

   5. WHAT IT IS BAD AT
      Name the worst class and what it gets confused with.
      Run a bias test: different lighting, different backgrounds,
      different people holding the animal. Report the accuracy gap
      in percentage points.

   6. LIMITS
      No deployment claim unless the numbers support it — and
      "supported" means per-class, not overall.
   ══════════════════════════════════════════════════════════════
```

**(d) The warning line.**

> **DO NOT USE THIS FOR:** identifying any animal in a real vet's office, or any animal that is not a cat, a dog, or a hamster. It has seen 11 hamster photos and has never been tested on a photo it did not train on.

**Mark scheme (4):** 1 for spotting "tested on training data" · 1 for the class imbalance with a number · 1 for the missing baseline / the 1-hamster test set · 1 for a rewritten process containing a pre-training split, per-class accuracy, and a limits statement.

---

### C4 — The bigram table

**(a) Tokenize.**

```
   The dog ran. The dog ate. The cat ran.

    1 the      5 dog      9 the
    2 dog      6 ate     10 cat
    3 ran      7 .       11 ran
    4 .        8 the     12 .

   TOTAL = 12 tokens   (3 sentences × 4 tokens each)
```

**(b) How many bigrams should there be?**

Module 8's check: pairs = tokens − sentences, because each sentence loses one pair at its end.

```
   12 tokens − 3 sentences = 9 bigrams
```

Listing them to be sure:

```
   Sentence 1: the→dog · dog→ran · ran→.        3 pairs
   Sentence 2: the→dog · dog→ate · ate→.        3 pairs
   Sentence 3: the→cat · cat→ran · ran→.        3 pairs
                                                ───────
                                                9 pairs  ✓
```

The learner's table sums to 2 + 1 + 1 + 1 + 1 + 1 + 1 + 2 = **10**. One too many, which is the signal that something is wrong.

**(c) The two errors.**

**Error 1 — the `. → the` row should not exist.** The rule says do not count a pair that crosses a full stop. The learner counted `. → the` twice (at the joins between sentences 1–2 and 2–3). Deleting that row removes 2 from the total… which would give 8, not 9. So there must be a second error, and there is.

**Error 2 — `ran → .` is undercounted.** `ran` ends both sentence 1 and sentence 3, so `ran → .` happened **twice**, not once. The learner tallied it once.

```
   learner's total                    10
   remove the ". → the" row            −2   →   8
   correct "ran → ." from 1 to 2       +1   →   9   ✓ matches the check
```

**The corrected table:**

| Current word | Next word | Count | Out of | Chance |
|---|---|---:|---:|---:|
| the | dog | 2 | 3 | 66.7% |
| the | cat | 1 | 3 | 33.3% |
| dog | ran | 1 | 2 | 50% |
| dog | ate | 1 | 2 | 50% |
| cat | ran | 1 | 1 | 100% |
| ran | **.** | **2** | **2** | **100%** |
| ate | . | 1 | 1 | 100% |

Total: 2 + 1 + 1 + 1 + 1 + 2 + 1 = **9** ✓
Group check: each current-word group's chances sum to 100% ✓

**(d) Generate a sentence from `the`.**

```
   start:  the
   ├─ "the" has 2 followers: dog (2/3 = 66.7%) or cat (1/3 = 33.3%)
   │     → RANDOM. I put 3 slips in a bag (dog, dog, cat) and drew: dog
   │
   ├─ "dog" has 2 followers: ran (1/2) or ate (1/2)
   │     → RANDOM. Coin flip. Drew: ate
   │
   └─ "ate" has exactly 1 follower: "."
         → FORCED. There is no choice; every time "ate" appeared it was
           followed by a full stop.

   RESULT:  "the dog ate."
```

**Forced vs random.** Two of the three steps were **random** draws weighted by the counts (`the→dog` and `dog→ate`). One was **forced** — `ate→.` had only one option, so it was inevitable.

This is exactly why the same prompt gives different answers each time: the randomness is real and it lives in the draws. Run this three times and you might get "the dog ate.", "the cat ran.", "the dog ran." — and notice that **all** of them are sentences the corpus actually contained. With a tiny table, sampling mostly replays the training text. Bigger tables produce genuinely new sentences, which is where **hallucination** becomes possible: the machinery has no idea whether a new sentence is true, only that each step was a likely next word.

**Mark scheme (4):** 1 for 12 tokens and 9 expected bigrams with the check shown · 1 for deleting the `. → the` row with the crossing rule as the reason · 1 for correcting `ran → .` to 2 · 1 for a generated sentence with forced and random steps labelled.

---

</details>

---

# 🪞 Self-Assessment Checklist

Tick honestly. This maps to the six **level outcomes** in the [Level 1 README](README.md), and it is more useful to you than the score.

### Outcome 1 — Rules vs learned from examples

- [ ] I can define AI in one sentence without using "smart" or "brain"
- [ ] I can sort a system into rule-based / machine learning / generative and give my reason
- [ ] I can handle a **hard case** — a system that could be two of those — and defend my call
- [ ] I can explain why every AI today is narrow, with an example
- [ ] I can name a real product that is a **stack** of a learned part feeding a rule-based part

### Outcome 2 — Build a real dataset by hand

- [ ] I can turn a pile of real things into rows and columns and say what one row is
- [ ] I can label a column as number / category / text / image / time and say why it matters
- [ ] I can spot missing, duplicate, and impossible values, and I know not to silently delete or invent
- [ ] I can point at the features and the label in any table
- [ ] I can tell a useful feature from a useless one from a **leaky** one
- [ ] I can write a data card covering what, how much, from whom, with what permission, and **what's not in it**

### Outcome 3 — Train and honestly measure a classifier

- [ ] I have trained a working three-class Teachable Machine model
- [ ] I split my photos **before** training, and I can say what ratio I chose and why
- [ ] I can compute accuracy as a fraction, a decimal, and a percentage, showing the division
- [ ] I always state the **baseline** next to the accuracy
- [ ] I can build a confusion matrix by hand and read the off-diagonal cells
- [ ] I can say what a 62% confidence score means — and what it does *not* mean

### Outcome 4 — Memorizing vs generalizing

- [ ] I can explain in my own words why testing on training examples is cheating
- [ ] I can look at a training/test accuracy pair and say whether it is overfitting, underfitting, or healthy
- [ ] I have personally made a model that scored well on its own photos and failed on new ones
- [ ] I know that repeatedly tweaking based on the test score leaks the test set

### Outcome 5 — How machines see and read

- [ ] I can explain an image as a grid of numbers, and RGB as three stacked grids
- [ ] I can hand-compute one output cell of a 3×3 filter, including the `ABS`
- [ ] I can say how big the output of a 3×3 filter on an *n*×*n* image will be
- [ ] I can tokenize a sentence and say why punctuation and case matter
- [ ] I can build a bigram table and use it to generate a new sentence
- [ ] I can explain why a chatbot can be fluent and completely wrong at once

### Outcome 6 — Fair, private, honest

- [ ] I have run a bias test on **my own** model and computed a gap in percentage points
- [ ] I can trace a biased prediction back through all four links to a countable gap in the data
- [ ] I can name the personal data in a dataset and say who is harmed if it leaks
- [ ] I can state three situations where I should not trust an AI's answer, and what to do instead
- [ ] I have said out loud, to a real person, something my own model is bad at

---

# 🚪 The Gate — You're Ready for Level 2 When…

Level 2 hands you Python. It will move fast, and it will assume the Level 1 ideas are automatic. Do not walk through this door until **all six** of these are true.

```
   ┌────────────────────────────────────────────────────────────────────┐
   │  ✅  READY FOR LEVEL 2 WHEN…                                       │
   ├────────────────────────────────────────────────────────────────────┤
   │                                                                    │
   │  1.  You scored 42+ on this assessment (or fixed what you missed   │
   │      and can now explain it without notes).                        │
   │                                                                    │
   │  2.  You have a trained model of your own that you can show        │
   │      someone, and a held-out accuracy you computed BY HAND.        │
   │                                                                    │
   │  3.  You have finished the CAPSTONE and presented it to an adult   │
   │      for five minutes without saying "magic".                      │
   │                                                                    │
   │  4.  Somebody asked you "but how does it know?" and you answered   │
   │      with training, examples, and a pattern — not a shrug.         │
   │                                                                    │
   │  5.  You can name, unprompted, one group of inputs your own model  │
   │      handles badly, AND the number of photos it would take to fix  │
   │      it, AND how you'd check the fix worked.                       │
   │                                                                    │
   │  6.  When you hear "95% accurate", your first two questions are    │
   │      "out of how many?" and "what's the baseline?" — automatically,│
   │      before you decide whether to be impressed.                    │
   │                                                                    │
   └────────────────────────────────────────────────────────────────────┘
```

**If any of those is a "not yet", the fix is never to push on faster.** Go back to the module that owns it and redo the mini-project — not the reading, the *project*. The ideas live in the building.

### What happens on the other side of the door

| You already own this | Level 2 gives it a keyboard |
|---|---|
| A table of examples | `pandas.DataFrame` |
| Features and a label | `X` and `y` |
| "Hide 20% before training" | `train_test_split(X, y, test_size=0.2)` |
| correct ÷ total | `accuracy_score(y_test, y_pred)` |
| Your paper confusion matrix | `confusion_matrix(y_test, y_pred)` |
| Confidence scores | `model.predict_proba(X_new)` |
| "Which class is it worst at?" | `classification_report(...)` |

**Not one new idea in that column.** Just spelling. That's the reward for doing Level 1 properly.

---

> ### 👉 Next: [The Capstone — The AI Fair Booth](capstone.md), then [Level 2 — Builder](../level-2-builder/)

---

[⬅ Module 9](module-09-fair-private-honest-ai.md) · [Level 1 Home](README.md) · [Capstone](capstone.md) · [Glossary](glossary.md)

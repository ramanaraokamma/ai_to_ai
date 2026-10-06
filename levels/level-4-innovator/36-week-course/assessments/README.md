# ✅ Assessments — How To Use The Four Term Tests

[⬅ Course home](../README.md) · [Term 1](term-1-test.md) · [Term 2](term-2-test.md) · [Term 3](term-3-test.md) · [Term 4](term-4-test.md) · [Projects](../projects/project-ideas.md) · [Capstone](../projects/capstone.md)

---

> ### In one sentence
>
> **These papers are X-rays, not grades: their whole job is to show which week did not stick, in time to do something about it, and then to check at a machine that the head was right.**

---

## 🧑‍🏫 For the teacher, in two minutes

**You do not need to know Python, PyTorch or machine learning to run or mark any of these.** That is a design constraint, not a slogan, and this is how it is met.

1. **There are two papers per term, and they are not the same paper.**

   | Paper | Where it lives | What it is for |
   |---|---|---|
   | **The week paper** | Inside the teacher guide of Week 9, 18, 27 and 36 | The one the **student marks themselves**, in a different colour, as homework. 75 marks, 75 minutes in class (2 to settle, 70 for the paper, 3 to hand in) |
   | **The term test** | [`term-1-test.md`](term-1-test.md) … [`term-4-test.md`](term-4-test.md), in this folder | **A second paper of the same shape with every number different.** The formal test, the re-sit after the remediation fortnight, or practice. Nothing on it repeats the week paper, so a student who sat one has not seen the other |

2. **Each term test is two parts, reported separately:**

   | Part | Time | Marks | Computer? | Tests |
   |---|:--:|:--:|---|---|
   | **Part 1 · the paper** | 70 min | 75 | **No.** A calculator, yes | Can they run code and arithmetic in their head |
   | **Part 2 · the demo** | 15 min | 15 | **Yes** — their own files and `l4lib/`, no network | Can they prove the head was right, on a machine, out loud, in front of someone |

3. **The paper always has the same five sections, in every term:**

   | | Section | Marks | What it is really testing |
   |---|---|:--:|---|
   | 🅰️ | 20 multiple choice | 20 | Do they know what the words mean. Every wrong option was built from a real mistake, so a wrong choice *means* something |
   | 🅱️ | 8 "what does this print" | 16 | **Can they run code in their head** — including the silent cases |
   | 🅲 | 4 "find the bug" | 12 | **Can they name a bug, say what happens, and fix it** |
   | 🅳 | 3 "do the arithmetic" | 15 | **Can they do by hand what the library hides** |
   | 🅴 | 1 longer question on real tables or curves | 12 | Can they read a result honestly, and say what it can and cannot support |

4. **Each paper tests only its own term.** Term 1's test says on its front: *covers Weeks 1–8, nothing later appears anywhere.* If a student writes "LSTM" or "vanishing gradient" on Term 1, **do not mark it wrong and do not mark it extra** — it comes from next term; say so kindly on the sheet.

5. **Every code block in every paper and key was run on a CPU** (Python 3.10.10, torch 2.2.1, numpy 1.26.4, seeds shown, one thread) **and the real output pasted in unedited.** Nothing is estimated. So when a student says *"but it prints `6.0`!"* you can say, with confidence, *"no, it prints `12.0`, and here is the run."*

6. **Every Section 🅴 table is a printed table.** Print it. **Do not regenerate it on the day** — on a different CPU or torch build the last digit of a loss can move.

7. **Every paper has a marking scheme and a full answer key** below a divider, with *why each wrong option was tempting* and *the real output of every block*. You never have to work out an answer; you only compare.

8. **No language model appears anywhere.** Where a scripted backend stands in for one (the sentence-copier, the scripted agent plan, the planted-note follower), the paper labels it *stand-in, not a model*, and results against it say nothing about a real model. Term 1 has none at all; the first one arrives in Week 23.

> **⚠️ Watch out — read this before the first paper.** These papers are **practice**. Nothing is gated on them. A student who scores 40 out of 75 and then goes back and redoes Week 8 has had a better term than one who scores 70 and closes the folder. Say that out loud before you hand the first one out, and mean it. The pass mark of 45 used in the guides is **a proposal** — nothing in the course depends on it.

---

## ⛔ Why Part 1 has no computer

This is the one rule students argue about, so here is the answer to give them.

**A programmer who can only find out what code does by running it cannot debug.** Debugging *is* predicting: you look at a line, you say "this should print `torch.Size([1, 2, 4])`", you run it, you get `torch.Size([1, 5, 4])`, and the gap between those two is the bug. With no prediction there is no gap, and you are reduced to changing things at random until it goes quiet.

Level 4 sharpens this, because **the defining bugs of this level do not stop the program.** A `state_dict()` saved without `deepcopy` that quietly becomes the last weights; an `nn.RNN` built without `batch_first=True` that reads a batch as time; a score promise edited after the number was seen; a counter that counts attempts as harm. Every one prints a plausible number. The only defence is having predicted the number first. **Sections 🅱️, 🅲 and 🅳 all collapse the moment there is a keyboard in the room.**

## ✅ Why a calculator IS allowed

Because arithmetic speed is not on any ladder in this course, and pretending it is would make the paper measure the wrong thing. What is measured is **whether they know which sum to do**, and what the answer means once they have it.

**Check the calculator before the paper starts.** It takes thirty seconds and a missing key costs real marks.

| Term | The calculator needs |
|:--:|---|
| 1 | `+ − × ÷` and a square-root key (root-mean-square, Week 3) |
| 2 | the above, plus `ln`, `e^x` and a power key (`0.9^40`, `ln 28`, softmax) |
| 3 | the above, plus `log` (base 10) — the log-log line of Week 21 |
| 4 | a square-root key again (the wobble `sqrt(n p (1-p))`), plus everything above |

A phone in calculator mode is fine **with airplane mode on.** It is not a computer for the purposes of the rule, and it must not be a search engine.

## 💻 Why Part 2 has a computer — and why that is not a contradiction

Part 1 asks *"what do you think it does?"* Part 2 asks *"show me."* The two are built as a pair: **the student writes a prediction on paper, then proves it at a machine, and the teacher watches.**

The rule that makes it work: **say your prediction out loud before you run anything.** A prediction made after seeing the output scores nothing (it is a row of its own in every demo, worth 1 of the 5 marks). A student who is right on paper and cannot make the machine agree has told you something; so has one who can make the machine print the right thing and cannot say why. One sum would hide both.

---

## 📅 When to give each one

| Test | Covers | The week paper is in | Give the term test | Why then |
|---|---|---|---|---|
| [**Term 1**](term-1-test.md) | Weeks 1–8 | Week 9 | After the remediation fortnight, as the formal test or the re-sit | Weeks 10–13 lean directly on **Weeks 2, 6 and 8**. If those are shaky, find out before Term 2 builds on them |
| [**Term 2**](term-2-test.md) | Weeks 10–17 | Week 18 | After the Week 18 paper and its fortnight | **Week 19 takes the Week 17 model apart.** It stands on **Weeks 15, 16 and 17** |
| [**Term 3**](term-3-test.md) | Weeks 19–26 | Week 27 | After the Week 27 paper and its fortnight | Weeks 28–29 (agents) reuse **Week 23** (the harness, the floor, the guard) and **Week 26** (chunks, citations, "retrieved text is data"), and **Week 22** returns in Week 31 |
| [**Term 4**](term-4-test.md) | Weeks 28–35 | Week 36 (the final paper, Assessment 4) | After Week 36, **never in the same sitting as the demo** | Nothing is built on Term 4. This one is a look-back |

**Five scheduling notes that matter more than they look:**

- **Use the week paper first, the term test second.** The week paper is the X-ray; the remediation fortnight is the treatment; the term test is the second X-ray. Skipping straight to the term test throws away the self-marking, which is where most of the learning happens.
- **Do not give a test in the same sitting as a lab.** Weeks run 60–75 minutes. A 70-minute paper needs a slot with nothing else in it, and Part 2 wants its own 15 minutes with an adult sitting beside the student.
- **Run Part 1 and Part 2 on the same day if you can, and the paper first.** A student who has just proved their numbers at a machine marks the paper differently.
- **Week 36 is two sittings, on different days: the demo and the system card, then the paper at least a day later.** Never squeeze the final paper into the end of the demo sitting. A student who has just been questioned about their own system does not sit a paper straight after.
- **If Term 1 goes badly, delay Week 10 rather than pressing on.** This is the single most useful piece of scheduling advice on this page. Term 2's lab is the cell of Week 8 pushed through forty steps, and a fortnight spent redoing Weeks 2, 6 and 8 is cheaper than eight weeks of copying code that nobody can read.

---

## 🕐 Running the test — the whole procedure

**The day before:**

1. **Print the paper (Part 1 and Part 2) up to the marking scheme, and stop there.** The Marking Scheme and the Answer Key are in the same file, below the divider. Do not photocopy past it.
2. Print **Tables in Section 🅴 from the file as printed** — do not regenerate them.
3. Print **three blank sheets per student.** Real paper. Shape traces and by-hand tables want space.
4. **Check the calculators** against the table above. Press the buttons yourself.
5. **Read the paper through with the key open** (about 25 minutes). You are not learning PyTorch; you are finding which two questions the student will complain about, so you can say *"answer the part you do understand and move on"* instead of improvising.
6. **For Part 2, run the three demo files yourself once.** The key prints the reference output. If your numbers differ from it in the last digit, that is the CPU; in the first digit, it is a bug.
7. **Find the two remediation slots now** and write them on the remediation table. A plan with no time attached does not happen.

**On the day, Part 1:**

1. Read the "what is allowed" box out loud, all of it, including the reason for the no-computer rule and the calculator rule.
2. Say the three sentences that change behaviour:
   - *"Working earns marks. A bare number scores less than a number with its working."*
   - *"If a program crashes, say which line and what the message means. If it does not crash and prints something wrong, say that. Both are answers."*
   - *"If you guessed, write 'not sure' beside it. It costs nothing and it tells me where to teach."*
3. Set a timer for 70 minutes. Then **say nothing.** The only legal replies, if asked, are *"read it again"*, *"write what you know"* and *"I can't help with that one, move on."* A frown at question 7 changes an answer that was right.
4. **Pens down: take the paper without reading it in front of them.**

**On the day, Part 2:**

1. Sit **beside** the student, with the demo checklist from the marking scheme next to you. The marks are for what you **watch** and **hear**.
2. Open a terminal in the `36-week-course/` folder and run `export PYTHONPATH="$PWD"` once. Each demo is a new file.
3. Say the one sentence: *"Prediction first, out loud. Then run it."*
4. **Do not help, and do not mark a sentence the student was handed.** The student's own words at the machine are the evidence.
5. If the machine misbehaves, see the fallback in the week's teacher guide; a broken laptop is not a student's mistake and costs no marks.

**Straight after, before you mark anything,** ask three questions and write the answers on the front of the paper:

1. *"Which question did you find hardest?"*
2. *"Which one did you get wrong and then realise?"*
3. *"Was there anything you had never seen before?"* — if the honest answer is yes, check it against the [maths ladder](../README.md#-the-maths-ladder) and the [syntax ladder](../README.md#-the-syntax-ladder), because a paper should contain nothing new.

---

## 🧮 How to mark it

### The one rule that governs all of it

> **Mark the working, not just the number — and mark the demo separately from the paper.**

A student who sets up the right sum and slips on the division has done the hard part. A student who writes a bare number has either done the hard part invisibly or remembered it, and there is no way to tell which. So marks follow the working, everywhere, and you must say so out loud before the paper starts or it feels like a trick.

### Section 🅰️ — 20 marks

One mark per question. **No half marks.** Two letters circled scores 0. There is nothing to interpret.

Count the **"not sure"** answers separately, and tell the student why. *Right and knows it is unsure* needs a different conversation from *wrong and sure*, and a guess that lands is a wrong answer that has not happened yet.

The *pattern* is worth more than the total: every question is tagged to a week, so twenty right/wrong marks are a map. Read the wrong-option notes in the key before anything else.

### Section 🅱️ — 16 marks · what does this print?

**2 marks for every answer exactly right. 1 mark if the idea is right and one digit or sign is wrong. 0 otherwise.** Count *lines* where a program prints more than one: a correct first line and a missing second line is 1.

Rulings you will need:

1. **Brackets are information; spacing is not.** `[-1.2247, 0.0, 1.2247]` and `-1.2247 0.0 1.2247` are different answers (an array against three numbers). But `3 2 True False` with two spaces for one is the answer.
2. **A shape must have all its numbers.** `(3, 5, 7)` is right; `(5, 7)` is not, and `h_n` as `(3, 7)` — missing the leading 1 — costs the line.
3. **Floating-point noise in the last digit is not an error.** `-0.0000` and `0.0000` are the same number. A difference in the **first** digit is a real error — ask the student to find it.
4. **The "trap" column in the key is the lesson.** Where a student writes the trap answer, write the trap's name beside it and move on.

### Section 🅲 — 12 marks · find and fix the bug

**3 marks per bug, and the three are independent:**

| | | Marks |
|---|---|:--:|
| **(i)** | **The bug named** — the mechanism, in their own words | 1 |
| **(ii)** | **What happens when it runs** — loud (the error, decoded) or silent (the number that comes out wrong) | 1 |
| **(iii)** | **A correct fix** — the corrected line, or one sentence where no line is wrong | 1 |

A student can explain the bug beautifully, name the wrong line, and still score 2. That is correct and intended.

Rulings, the first two carrying the most weight:

1. **"It's a typo" or "there's a shape error" scores 0 for (i).** The mark is for the mechanism: *"`nn.LayerNorm(4)` was told four features and the layer before it produces eight."*
2. **On a silent bug, "it crashes" has not understood the bug.** Accept *"it prints something wrong"* for (ii) and ask which number and which way. *"The two printed numbers differ, `-0.0075` then `20.0225`"* earns it; *"it didn't work"* does not.
3. **Accept any fix that gives the expected result.** The key's fixes were run, but they are not the only fixes.
4. **Withhold (iii) for a fix that makes the number look better by hiding information.** Editing the promise so the score line says kept is not a fix; deleting the row that caused the `nan` is not a fix. The paper exists to catch exactly that.

### Section 🅳 — 15 marks · do the arithmetic

**Marked against named rows, listed per part in each paper's marking scheme** (for Term 1: `1 mark per table row`, `1 mark for the verdict`, and so on). The rules that hold on every paper:

| What the student did | Ruling |
|---|---|
| Right method, **one** arithmetic slip carried through | **Costs one mark, once.** Charging it three times measures luck, not understanding |
| Right method, wrong *starting* number chosen to make the arithmetic easier | **A real mistake** — withhold the row. It is the thing the question exists to catch |
| Correct final numbers with **no working at all** | **At most half the part.** Say so before the paper starts |
| Sign wrong on a step (a negative gradient moving the weight *down*) | **1 mark where the key says so**, not zero: the method was right |
| A verdict with no number behind it | **Withhold the verdict mark.** *"Inside the noise"* needs `0.044 < 0.066` beside it |

### Section 🅴 — 12 marks · reading real tables and curves

**Marked as rows in the scheme: one mark per row, each earned on its own.** A row is earned by the *idea being visibly right with a number quoted from the table.* A sentence with no number from the table scores 0 for that row, however sensible it sounds.

Rulings:

1. **"The classmate's number is higher" is not a finding until the spread is next to it.** The standing rule from Week 7: a gap smaller than **twice the larger spread** is inside the noise. A student who says "better" on a gap inside the noise has missed the whole point of the question.
2. **One knob.** A fix that changes two things scores 0 on the "action" row: *raise `lr` **and** add the residual* is two knobs, and you could not say which one worked.
3. **A cheap check is cheap.** Anything that runs in seconds is acceptable; "retrain for a day" is not.
4. **Do not reward certainty.** A student who says what the table *cannot* say (one network, one dataset, three seeds) has earned more than one who says it proves a law. Where a row asks what the table does not show, **that sentence is the row.**

### Part 2 — the demo · 15 marks

Three demos of **5 marks each**, with a fixed shape: **prediction said first = 1**, then the lines that must print, then the student's own sentence about *what this does and does not show*.

1. **The prediction is a row.** If it was said after the output appeared, the row is 0, however correct. Do not be softer about this than the paper is about bare numbers.
2. **Reference output is in the key.** The student's numbers may differ in the last digit on your machine; not the first.
3. **The sentence is the hard row.** *"The states differ because the cell reads in order; they do not yet mean anything, because the weights are random"* earns it. Repeating the output does not.
4. **Report the demo separately from the paper.** Do not add them.

---

## 📋 Mark schemes — the policy

1. **The marking scheme and answer key live inside each paper file**, below the divider. This page does **not** repeat answers, so that it cannot drift from them. If this page and a paper disagree, the paper wins.
2. **Never hand the student the key.** After the paper they get **only** the printed marking sheet (short answers) and a pen of a **different colour**, and mark their own week paper as homework. The key — wrong-option maps, model answers, the teacher's checks — is for you.
3. **Never hand the student a teacher file.** The remediation table below links only to workbook pages and student guides. The spoken checks are for the adult to ask aloud; the answers are printed here for **you**, so keep this page to yourself.
4. **Every number on a paper is a printed number.** If you change a seed, a step count or a dataset, the paper's tables and keys are stale. Re-run, re-paste, and re-check every answer that depended on it. An invented or stale output is the worst defect a paper can have.
5. **Every scripted stand-in is labelled** *stand-in, not a model* on the paper and in the key. Never let a student read a result against a stand-in as a result about a real model.
6. **Nothing is on a paper before its week.** The papers were checked line by line against both ladders. If a student says *"we never did that"*, check the ladder (see the questions below) before you answer.
7. **A week paper and a term test have different per-week grids** (different questions, different marks per week). Always use the grid printed with the paper in front of you, never one from the other.

---

## 📊 What the scores mean

These bands are **suggestions, taken from the Term 1 paper**; nothing in the course depends on them. They apply to the **paper** (75). The demo is read separately, below.

| Paper | What it probably means | **What to do about it** |
|:--:|---|---|
| **60–75** | **Secure.** The term landed | **DO:** carry on to the next term as planned. If they want more, offer one project from [project-ideas.md](../projects/project-ideas.md). Do not re-teach anything — a secure student given revision instead of a harder problem gets bored, and bored is worse than stuck |
| **45–59** | **Solid, with a gap** | **DO:** open the per-week grid and find the one or two weeks under 60%. Redo **those pages** (the remediation table below), and ask the spoken check aloud afterwards. Do not repeat the paper |
| **under 45** | **Do not read this as a verdict.** A whole idea may be missing, or the day was bad | **DO:** compare Section 🅰️ with the demo **first.** A student who knew it at the machine and lost it on paper needs a different plan from one who lost it on both. Redo **at most two weeks**, then re-sit the term test a fortnight later. **Do not move on in the meantime** if the weeks named are the load-bearing ones for the next term |

> **🧑‍🏫 Two numbers to watch that are not the total.**
>
> **Paper against demo:**
> - **Paper high, demo low** — they can predict but not make the machine agree. Usually a typing, setup or `PYTHONPATH` habit. Fixable in one sitting.
> - **Paper low, demo high** — they can do it with their hands and lose it under a clock. Give them the old pages as *pencil work*, not new reading.
> - **Both low** — the only profile where pressing on is genuinely harmful. Redo the named weeks and delay the next term.
>
> **Section 🅰️ against Section 🅳** (words against arithmetic): *A high, D low* is the commonest Level 4 profile and is fixable with a pencil in a week. *A low, D high* means they can compute and cannot explain — ask them to say each term aloud with the number that proves it.

---

## 🔧 The remediation table

**Every week of the course, mapped to the pages that redo it.** Use it two ways: a wrong answer tells you which week to redo, and a week with several wrong answers against it is the week to redo *first*.

**The rules, which are the same on every week paper:**

- Add up the marks on each week's questions (the grid printed with the paper), and divide by the marks available.
- **Redo a week if the marks are strictly under 60% of those available.** (Weeks 27 and 36 print the inclusive boundary for ten-mark weeks; the two rules differ by one mark at exactly 60%, which does not matter.)
- **Circle at most two weeks.** Lowest percentage first; on a tie, use the priority order in the heading of each term below.
- **Each redo is 20 minutes plus the spoken check.** Do not repeat the paper: redo the *page*, then ask the question out loud. **A correct spoken answer in the student's own words is the exit ticket.**
- **Never circle a week with one or two marks on the paper.** One question is not a pattern.

### Term 1 — Weeks 1–8 · priority on a tie: **8, 2, 6**

**These three carry Term 2:** Week 2's running average returns as the gate in Week 11; Week 6's residual road is Week 11's highway; Week 8's cell is Week 10's whole subject.

| Week | Title | Redo this (20 min) | The spoken check → the answer | Why Term 2 needs it |
|:--:|---|---|---|---|
| **1** | [One Loop, Ten Knobs](../student-guide/week-01.md) | Workbook [Pages 1.3 and 1.1](../workbook/week-01.md) — the coin by hand, and the six-curve grid | *"Two runs both end at 0.69. How do you tell what each did?"* → the curve, from epoch 1. And `ln 2 = 0.6931` is "no better than a coin" | Every Term 2 lab starts by reading a curve |
| **2** | [Momentum](../student-guide/week-02.md) | Workbook [Pages 2.1 and 2.8](../workbook/week-02.md) — the hand table, then a second one with new numbers | *"Momentum step 2: what is `v`, and why isn't it something with a 0.1?"* → `0.9 × v + g`; PyTorch keeps no `0.1` | The running update returns as the gate in Week 11 |
| **3** | [Adam](../student-guide/week-03.md) | Workbook [Pages 3.1 and 3.3](../workbook/week-03.md) — the three-optimizer table, then root-mean-square on your own lists | *"Why is Adam's first step the same for a gradient of 1 and of 1000?"* → it divides by the gradient's own typical size | Adam is the default optimizer for every later lab |
| **4** | [Schedules and Batch Size](../student-guide/week-04.md) | Workbook [Pages 4.3 and 4.4](../workbook/week-04.md) — the schedule by hand, and counting steps | *"Batch 256 against 64: what is not equal besides the batch?"* → the number of steps (4 times fewer) | Every later comparison asks "what did I hold fixed?" |
| **5** | [Four Ways to Stop Memorising](../student-guide/week-05.md) | Workbook [Pages 5.3 and 5.5](../workbook/week-05.md) — stopping and the fee by hand, then the four-cure table | *"Which column of the cure table do you trust, and why?"* → best validation loss; the final one depends on when you stopped | Early stopping and `eval()` are in every script from now on |
| **6** | [Norms and Residuals](../student-guide/week-06.md) | Workbook [Pages 6.3 and 6.4](../workbook/week-06.md) — normalise by hand, then the slope of a sum and the depth table | *"What is the slope of `x + f(x)` when `f` has slope 0.3?"* → `1.3` | The residual highway is Week 11's gate |
| **7** | [The Playbook](../student-guide/week-07.md) | Workbook [Pages 7.3 and 7.4](../workbook/week-07.md) — is it noise, and four curves to read | *"Gap 0.002, spreads 0.008 and 0.010: bigger than noise?"* → no; `0.002` is under `2 × 0.010 = 0.020` | Every lab from here reports a mean and a spread |
| **8** | [A Cell That Remembers](../student-guide/week-08.md) | Workbook [Pages 8.3 and 8.4](../workbook/week-08.md) — unroll the cell by hand, then the shapes | *"Same inputs in a different order: same final note?"* → no; the note depends on the order | **Week 10 is entirely about this cell** |

### Term 2 — Weeks 10–17 · priority on a tie: **16, 15, 17**

**These three carry Term 3:** Week 19 deletes the mask and the divide (Week 15), the positions and the block layout (Week 16), and judges "broke" by the first-loss check and the train-against-validation reading (Week 17). **One extra redo is always on offer:** the three-token attention pass on a *new* set of numbers (the Week 18 guide has one), for any of Weeks 14, 15 or 16.

| Week | Title | Redo this (20 min) | The spoken check → the answer | Why Term 3 needs it |
|:--:|---|---|---|---|
| **10** | [Forty Multiplications](../student-guide/week-10.md) | Workbook [Pages 10.1 and 10.4](../workbook/week-10.md) — compounding by hand, and the grid | *"A slope of 0.9 for forty steps: roughly what is left? Which disease can clipping cure?"* → `0.9^40 = 0.0148`; only exploding | Week 21's log-log line uses compounding |
| **11** | [Gates](../student-guide/week-11.md) | Workbook [Pages 11.1 and 11.5](../workbook/week-11.md) — dials by hand, and the forget-bias probe | *"What is the slope back through the memory track, and what is it at the start?"* → the forget gate; about one half, and `0.5^10 = 0.000977` | The gate is Week 6's residual road in a loop; Week 19 deletes the residual |
| **12** | [Teach a Network to Invent Names](../student-guide/week-12.md) | Workbook [Pages 12.4 and 12.5](../workbook/week-12.md) — train against validation, and the name audit | *"Validation 3.417, and `ln 28` is 3.332. What does it mean?"* → worse than knowing nothing: memorised | The train-against-validation reading returns in Weeks 17, 19, 21 |
| **13** | [Choosing the Next Letter](../student-guide/week-13.md) | Workbook [Pages 13.2 and 13.3](../workbook/week-13.md) — scores to chances at three temperatures, and top-k, top-p by hand | *"What does a low temperature do to the top letter's chance? What does top-p 0.9 keep?"* → raises it (`0.6652` to `0.8668` for scores `2, 1, 0`); the smallest set adding to 0.9 | Every generation from Week 17 is a choice rule |
| **14** | [Attention by Hand](../student-guide/week-14.md) | Workbook [Pages 14.1 and 14.4](../workbook/week-14.md) — the pen pass, then a second pass by hand | *"Which of `Wq`, `Wk`, `Wv` doesn't change the weights, and why?"* → `Wv`; it only changes what gets averaged | **Week 19 reads head heatmaps**; those are these weights |
| **15** | [Scale, Mask, Many Heads](../student-guide/week-15.md) | Workbook [Pages 15.2 and 15.3](../workbook/week-15.md) — variances add, then the mask built by hand | *"Mask before or after the softmax, and `-inf` or 0?"* → before; `-inf`, so the future gets exactly 0 | **Two of the four parts Week 19 deletes** |
| **16** | [Positions and the Block](../student-guide/week-16.md) | Workbook [Pages 16.2 and 16.4](../workbook/week-16.md) — the seat swap, and counting the knobs of one block | *"Why can attention alone not tell `dog bit man` from `man bit dog`?"* → it has no order; add a position vector | **The other two parts Week 19 deletes** |
| **17** | [Build TinyGPT](../student-guide/week-17.md) | Workbook [Pages 17.3, 17.4, then 17.6](../workbook/week-17.md) — count the model, the first-loss check, what the gap means | *"What should the loss be at step 0 for 28 characters?"* → about `ln 28 = 3.33`: every character equally likely | The first-loss check is how Week 19 decides an ablation broke something |

### Term 3 — Weeks 19–26 · priority on a tie: **23, 26, 22**

**These three carry Term 4:** Week 23 (the floor, the frozen set, the guard that stops one call late) is reused by Week 28's six fences, Week 29's cost and Week 30's evals; Week 26's "retrieved text is data, not orders" is Week 29's attack; Week 22's leash returns in Week 31. Weeks 20 and 24 are thin on the paper: a flag there means *ask the spoken check first.*

| Week | Title | Redo this (20 min) | The spoken check → the answer | Why Term 4 needs it |
|:--:|---|---|---|---|
| **19** | [Open the GPT](../student-guide/week-19.md) | Workbook [Pages 19.3 and 19.6](../workbook/week-19.md) — the leak by hand, and switching it off | *"The no-mask model scores 0.077. Is the mask a bad idea?"* → no: it reads the answer; a leak | The leak and the switch-off test are how Week 31 decides a fine-tune "worked" |
| **20** | [Tokenizers](../student-guide/week-20.md) | Workbook [Pages 20.2 and 20.5](../workbook/week-20.md) — merge by hand, and bytes per token as the text grows | *"What does one merge do, and what happens to bytes per token?"* → joins the most common neighbouring pair; it rises | Week 29's cost arithmetic counts tokens |
| **21** | [Scaling Arithmetic](../student-guide/week-21.md) | Workbook [Pages 21.1 and 21.3](../workbook/week-21.md) — the straight-line trick, then predict and check | *"Loss 9, 3, 1 at ten times the steps each: what is the line, and is a prediction a measurement?"* → slope `-0.477`; no, a prediction to check | The capstone's cost budget uses `6ND` |
| **22** | [SFT, Reward Model, DPO](../student-guide/week-22.md) | Workbook [Pages 22.1 and 22.3](../workbook/week-22.md) — the mask, then KL on paper and DPO on one pair | *"Masked loss is higher than unmasked. Is that worse?"* → no: a different set of guesses | Week 31 fine-tunes with a leash and watches a regression |
| **23** | [The Harness](../student-guide/week-23.md) | Workbook [Pages 23.2 and 23.5](../workbook/week-23.md) — the floor by hand, and the guard that stops one call late | *"A prompt scores 50% and the constant answer 43.8%: what have you shown? Why does the guard stop one call late?"* → very little (`7/16 = 0.4375`); it checks the bill after each call | **Weeks 28, 29 and 30 all reuse it** |
| **24** | [In-Context, Scratchpads, Schemas](../student-guide/week-24.md) | Workbook [Pages 24.1 and 24.4](../workbook/week-24.md) — the ceiling, then the mask with a hand softmax first | *"A mask forces valid JSON. What is still wrong?"* → the values; shape, not sense | Week 28's `validate_args` makes the same promise and the same mistake possible |
| **25** | [Embeddings](../student-guide/week-25.md) | Workbook [Pages 25.1 and 25.4](../workbook/week-25.md) — cosine cards, and recall with its control | *"Why does a long vector beat a close one on a plain dot product, and what fixes it?"* → length; normalise once (dot `0.9` against `3`; cosine `0.9939` against `0.6`) | Week 29's mini RAG uses cosine |
| **26** | [RAG](../student-guide/week-26.md) | Workbook [Pages 26.1, 26.3 and 26.4](../workbook/week-26.md) — Citation Court, recall on your own questions, chunking | *"Recall is 1.00. What is your first question?"* → who wrote the questions? Then: *a valid citation proves what?* → the writer named a note it was handed | **Week 29 is this week's "retrieved text is data" turned into an attack** |

### Term 4 — Weeks 28–36 · priority on a tie: **28, 29** (together 22 of the 75 marks)

**Nothing is built on Term 4, so the redo is about the capstone and about the habit.** Weeks 28 and 29 come first because the agent's fences and the triangular sum are used again in every later week. **Never circle Week 26 (1 mark) or Week 34 (2 marks) on the final paper.** A student who is low everywhere but strong on Section 🅴 has the *judgement* and not the *recall*: give the remediation as pencil work on old pages, not as new reading.

| Week | Title | Redo this (20 min) | The spoken check → the answer | Why it matters |
|:--:|---|---|---|---|
| **28** | [Tools and the Loop](../student-guide/week-28.md) | Workbook [Pages 28.0 and 28.2](../workbook/week-28.md) — "Which fence?" with a pen, then predict the sandbox | *"The model was told to be careful. Which of the six fences read that sentence?"* → none; a fence is code, not advice | Every later agent claim stands on the fences firing with no model present |
| **29** | [Agents Under Attack and Under Budget](../student-guide/week-29.md) | Workbook [Pages 29.1 and 29.3](../workbook/week-29.md) — three layers on paper, then pay the bill | *"Every turn re-sends the history. Total re-sent for 5 steps? For 30?"* → `1+2+…+k`: `15` and `465` | The cost budget in the capstone is this sum |
| **30** | [Evaluating LLM Systems](../student-guide/week-30.md) | Workbook [Pages 30.1, 30.2 and 30.3](../workbook/week-30.md) — overlap, kappa by hand, flips | *"Two raters agree on 15 of 20 tickets. Is that 75% good?"* → not by itself: luck gives `0.51`, so kappa is `0.4898` | The frozen suite and the judge test are the capstone's measured evidence |
| **31** | [Fine-Tuning, LoRA, and the Regression](../student-guide/week-31.md) | Workbook [Pages 31.1 and 31.3](../workbook/week-31.md) — counting a patch by hand, then reading a table honestly | *"A 64-by-64 layer, rank 4: how many trainable numbers, and what share?"* → `4×64 + 64×4 = 512` of `4096`, `12.5%` | A rising average can hide one category falling |
| **32** | [Calibration and Abstention](../student-guide/week-32.md) | Workbook [Pages 32.1, 32.2 and 32.3](../workbook/week-32.md) — Brier, ECE, thresholds and who fell | *"Said 90% and was right 5 of 6; said 60% and was right 1 of 4. Which bucket is worse?"* → the unsure one: gap `0.35` against `0.0667`; ECE `0.18` | The proxy is not the goal; the card says what a score does not show |
| **33** | [Attack Your Own System](../student-guide/week-33.md) | Workbook [Pages 33.1, 33.2 and 33.3](../workbook/week-33.md) — the wobble, the red-team log, retention | *"50 runs, a true rate of 0.2: how wobbly is the count?"* → `sqrt(50 × 0.2 × 0.8) = 2.83` cases; and *zero of 50 is not never* | A zero needs a control, and a patch is a fix only if the happy path survives |
| **34** | [Capstone 1](../student-guide/week-34.md) | Workbook [Pages 34.1 and 34.2](../workbook/week-34.md) — severity, likelihood and the wobble; the case card and the floor | *"What does 25 cases let you see?"* → a wobble of about `2.33` cases on `17 of 25`, so small gaps are noise | The frozen eval is frozen *before* the system exists |
| **35** | [Capstone 2](../student-guide/week-35.md) | Workbook [Pages 35.1, 35.2 and 35.3](../workbook/week-35.md) — the tally, promise against measurement, the red-team card | *"Promise 0.70, measured 17 of 25. Kept?"* → no: `0.68` is under `0.70` (that needs 17.5 cases). Say *missed*; do not edit the promise | The score is reported as measured |
| **36** | [Capstone 3](../student-guide/week-36.md) | Workbook [Pages 36.1 and 36.3](../workbook/week-36.md) — the claim ledger, and four old sums with fresh numbers | *"8 of 9 against 800 of 900: same rate. Is it the same evidence?"* → no: wobble `0.105` against `0.0105` as a rate; one more failure on 9 cases moves `0.89` to `0.78` | *A claim without a number and an `n` is a mood* |

### 🧪 The numbers in the spoken checks — run, not remembered

Every figure in the spoken checks above that is not quoted from a week's own page was computed here. **The Term 4 practice numbers (the 20 tickets, the 64-by-64 layer, the ten results) are invented for this page; the arithmetic is real.** Plain Python, no randomness, no files, no network.

```python
# spoken_1.py - the arithmetic behind the spoken checks for Terms 1-3. Plain Python, no randomness, no files.
import math

def softmax(z, T=1.0):
    e = [math.exp(x / T) for x in z]
    s = sum(e)
    return [x / s for x in e]

print("W1   ln 2 (two-class coin)       :", round(math.log(2), 4))
v, w, rows = 0.0, 1.0, []
for _ in range(3):
    g = 2 * w
    v = 0.9 * v + g
    w = w - 0.2 * v
    rows.append((round(v, 4), round(w, 4)))
print("W2   momentum (v, w) x3          :", rows)
print("W3   RMS [3,-4] / [300,-400]     :", round(math.sqrt((9 + 16) / 2), 4), "/", round(math.sqrt((90000 + 160000) / 2), 2))
print("W6   slope of x + f(x), f' = 0.3 :", 1 + 0.3)
print("W7   twice the larger spread     :", round(2 * max(0.008, 0.010), 3), "(gap 0.002 is inside)")
print("W10  0.9 ** 40                   :", round(0.9 ** 40, 4))
print("W10  0.9526 ** 40                :", round(0.9526 ** 40, 3))
print("W11  0.5 ** 10 (forget gate 0.5) :", round(0.5 ** 10, 6))
print("W12  ln 28                       :", round(math.log(28), 4))
print("W13  softmax [2,1,0] at T=1      :", [round(p, 4) for p in softmax([2, 1, 0])])
print("W13  softmax [2,1,0] at T=0.5    :", [round(p, 4) for p in softmax([2, 1, 0], 0.5)])
print("W14  weights .7/.3 on 10 and 20  :", round(0.7 * 10 + 0.3 * 20, 1))
print("W15  divide scores by sqrt(16)   :", math.sqrt(16), " and sqrt(64):", math.sqrt(64))
print("W21  log-log slope, loss 9,3,1   :", round(math.log10(3 / 9), 3), "and", round(math.log10(1 / 3), 3))
print("W23  floor 7 of 16               :", round(7 / 16, 4))

def cos(a, b):
    return sum(x * y for x, y in zip(a, b)) / (math.hypot(*a) * math.hypot(*b))
q, near, big = (1, 0), (0.9, 0.1), (3, 4)
print("W25  dot  q.near / q.big         :", round(sum(x * y for x, y in zip(q, near)), 2), "/", sum(x * y for x, y in zip(q, big)))
print("W25  cos  q.near / q.big         :", round(cos(q, near), 4), "/", round(cos(q, big), 4))
```
```text
W1   ln 2 (two-class coin)       : 0.6931
W2   momentum (v, w) x3          : [(2.0, 0.6), (3.0, -0.0), (2.7, -0.54)]
W3   RMS [3,-4] / [300,-400]     : 3.5355 / 353.55
W6   slope of x + f(x), f' = 0.3 : 1.3
W7   twice the larger spread     : 0.02 (gap 0.002 is inside)
W10  0.9 ** 40                   : 0.0148
W10  0.9526 ** 40                : 0.143
W11  0.5 ** 10 (forget gate 0.5) : 0.000977
W12  ln 28                       : 3.3322
W13  softmax [2,1,0] at T=1      : [0.6652, 0.2447, 0.09]
W13  softmax [2,1,0] at T=0.5    : [0.8668, 0.1173, 0.0159]
W14  weights .7/.3 on 10 and 20  : 13.0
W15  divide scores by sqrt(16)   : 4.0  and sqrt(64): 8.0
W21  log-log slope, loss 9,3,1   : -0.477 and -0.477
W23  floor 7 of 16               : 0.4375
W25  dot  q.near / q.big         : 0.9 / 3
W25  cos  q.near / q.big         : 0.9939 / 0.6
```

```python
# spoken_2.py - the arithmetic behind the spoken checks for Term 4. PRACTICE numbers, invented for this page. Plain Python.
import math

print("W29  1+2+...+k, k=5 and k=30     :", 5 * 6 // 2, "and", 30 * 31 // 2)

both_pass, both_fail, a_only, b_only, n = 9, 6, 3, 2, 20
po = (both_pass + both_fail) / n
pa, pb = (both_pass + a_only) / n, (both_pass + b_only) / n
pe = pa * pb + (1 - pa) * (1 - pb)
print("W30  raw agreement p_o           :", po)
print("W30  by luck p_e                 :", round(pe, 4))
print("W30  kappa                       :", round((po - pe) / (1 - pe), 4))

d_in, d_out, r = 64, 64, 4
print("W31  patch r*in + out*r          :", r * d_in + d_out * r, "of", d_in * d_out, "=", round(100 * (r * d_in + d_out * r) / (d_in * d_out), 1), "%")

sure = (6, 0.9, 5 / 6)      # count, mean said, share right
unsure = (4, 0.6, 1 / 4)
ece = sum(c / 10 * abs(said - right) for c, said, right in (sure, unsure))
print("W32  gaps sure / unsure          :", round(abs(sure[1] - sure[2]), 4), "/", round(abs(unsure[1] - unsure[2]), 4))
print("W32  ECE (two buckets)           :", round(ece, 4))

def wobble(n, p):
    return math.sqrt(n * p * (1 - p))
print("W33  wobble n=50, p=0.2 (cases)  :", round(wobble(50, 0.2), 2))
print("W34  wobble n=25, p=0.68 (cases) :", round(wobble(25, 0.68), 2))
print("W35  17 of 25 =", 17 / 25, "vs promise 0.70; 0.70 x 25 =", 0.70 * 25, "cases")
print("W36  8 of 9: wobble in cases     :", round(wobble(9, 8 / 9), 2), " as a rate:", round(wobble(9, 8 / 9) / 9, 3))
print("W36  800 of 900: in cases / rate :", round(wobble(900, 8 / 9), 2), "/", round(wobble(900, 8 / 9) / 900, 4))
print("W36  one more failure on 9 cases :", round(8 / 9, 2), "->", round(7 / 9, 2))
```
```text
W29  1+2+...+k, k=5 and k=30     : 15 and 465
W30  raw agreement p_o           : 0.75
W30  by luck p_e                 : 0.51
W30  kappa                       : 0.4898
W31  patch r*in + out*r          : 512 of 4096 = 12.5 %
W32  gaps sure / unsure          : 0.0667 / 0.35
W32  ECE (two buckets)           : 0.18
W33  wobble n=50, p=0.2 (cases)  : 2.83
W34  wobble n=25, p=0.68 (cases) : 2.33
W35  17 of 25 = 0.68 vs promise 0.70; 0.70 x 25 = 17.5 cases
W36  8 of 9: wobble in cases     : 0.94  as a rate: 0.105
W36  800 of 900: in cases / rate : 9.43 / 0.0105
W36  one more failure on 9 cases : 0.89 -> 0.78
```

### 🧰 The per-week grid as a checker

The same rules, as a program you can run if you would rather not do the percentages by hand. The marks available per week are the ones printed in the grid of each **week paper** (Weeks 9, 18, 27, 36). **The student in the last two lines is made up, to show the mechanics.** The term tests print their own grids with different marks per week — use the one printed with the paper you are marking.

```python
# redo.py - the per-week grid as a checker. Marks available per week come from each paper's own grid; the rule is the same on all of them:
# redo a week if marks earned are strictly under 60% of marks available (integer test: 5 x earned < 3 x available). Circle at most two,
# lowest percentage first, ties broken by the priority list.
GRIDS = {
    "Week 9 paper":  ({1: 11, 2: 10, 3: 10, 4: 9, 5: 8, 6: 8, 7: 7, 8: 12}, [8, 2, 6]),
    "Week 18 paper": ({10: 11, 11: 6, 12: 11, 13: 13, 14: 7, 15: 9, 16: 9, 17: 9}, [16, 15, 17]),
    "Week 27 paper": ({19: 10, 20: 6, 21: 8, 22: 13, 23: 8, 24: 4, 25: 12, 26: 14}, [23, 26, 22]),
    "Week 36 paper": ({26: 1, 28: 10, 29: 12, 30: 10, 31: 8, 32: 9, 33: 7, 34: 2, 35: 11, 36: 5}, [28, 29]),
}
NEVER_CIRCLE = {"Week 36 paper": {26, 34}}          # one or two marks is not a pattern

def circle(name, earned):
    avail, priority = GRIDS[name]
    skip = NEVER_CIRCLE.get(name, set())
    low = [w for w in avail if w not in skip and 5 * earned.get(w, 0) < 3 * avail[w]]
    key = lambda w: (earned[w] / avail[w], priority.index(w) if w in priority else 99)
    return sorted(low, key=key)[:2]

for name, (avail, priority) in GRIDS.items():
    print(f"{name}: {sum(avail.values())} marks; redo if at or below:", {w: (3 * m - 1) // 5 for w, m in avail.items()})

# A made-up student on the Week 36 paper (invented numbers, to show the mechanics):
sat = {26: 0, 28: 5, 29: 7, 30: 8, 31: 6, 32: 8, 33: 5, 34: 0, 35: 9, 36: 4}
print("made-up Week 36 student, total", sum(sat.values()), "-> circle weeks", circle("Week 36 paper", sat))
# A tie on percentage at Week 9: weeks 2 and 8 both at 50%; priority says 8 first.
tie = {1: 9, 2: 5, 3: 8, 4: 7, 5: 6, 6: 6, 7: 6, 8: 6}
print("made-up Week 9 student, total", sum(tie.values()), "-> circle weeks", circle("Week 9 paper", tie))
```
```text
Week 9 paper: 75 marks; redo if at or below: {1: 6, 2: 5, 3: 5, 4: 5, 5: 4, 6: 4, 7: 4, 8: 7}
Week 18 paper: 75 marks; redo if at or below: {10: 6, 11: 3, 12: 6, 13: 7, 14: 4, 15: 5, 16: 5, 17: 5}
Week 27 paper: 75 marks; redo if at or below: {19: 5, 20: 3, 21: 4, 22: 7, 23: 4, 24: 2, 25: 7, 26: 8}
Week 36 paper: 75 marks; redo if at or below: {26: 0, 28: 5, 29: 7, 30: 5, 31: 4, 32: 5, 33: 4, 34: 1, 35: 6, 36: 2}
made-up Week 36 student, total 52 -> circle weeks [28, 29]
made-up Week 9 student, total 53 -> circle weeks [8, 2]
```

---

## 🪞 A one-page record sheet

Print one per student and keep all four terms on the same sheet. The **trend** across the four columns tells you more than any single total.

```
   ┌──────────────────────────────────────────────────────────────────────────┐
   │  LEVEL 4 INNOVATOR · TERM TEST RECORD                                    │
   │                                                                          │
   │  Student ______________________________   Year ________________         │
   │                                                                          │
   │  ┌──────────────────────────┬────────┬────────┬────────┬────────┐        │
   │  │ PART 1 · THE PAPER       │ TERM 1 │ TERM 2 │ TERM 3 │ TERM 4 │        │
   │  ├──────────────────────────┼────────┼────────┼────────┼────────┤        │
   │  │ A  multiple choice   /20 │        │        │        │        │        │
   │  │ B  what prints       /16 │        │        │        │        │        │
   │  │ C  find the bug      /12 │        │        │        │        │        │
   │  │ D  arithmetic        /15 │        │        │        │        │        │
   │  │ E  reading tables    /12 │        │        │        │        │        │
   │  ├──────────────────────────┼────────┼────────┼────────┼────────┤        │
   │  │ PAPER TOTAL          /75 │        │        │        │        │        │
   │  ├──────────────────────────┼────────┼────────┼────────┼────────┤        │
   │  │ PART 2 · THE DEMO    /15 │        │        │        │        │        │
   │  │  (never added to Part 1) │        │        │        │        │        │
   │  ├──────────────────────────┼────────┼────────┼────────┼────────┤        │
   │  │ Week paper total     /75 │        │        │        │        │        │
   │  │ Date sat (paper / demo)  │        │        │        │        │        │
   │  │ "Hardest question"       │        │        │        │        │        │
   │  │ "Got it, then realised"  │        │        │        │        │        │
   │  │ Weeks circled / redone   │        │        │        │        │        │
   │  │ Re-sat? (which part)     │        │        │        │        │        │
   │  └──────────────────────────┴────────┴────────┴────────┴────────┘        │
   │                                                                          │
   │  THE TWO NUMBERS TO WATCH                                                │
   │  Paper total against demo total, by term:                                │
   │      paper ___ ___ ___ ___      demo ___ ___ ___ ___                     │
   │  A big gap either way is a plan, not a verdict (see "What the scores     │
   │  mean").                                                                 │
   │                                                                          │
   │  GUESSES MARKED "not sure" THAT TURNED OUT RIGHT                         │
   │  Term 1 ____   Term 2 ____   Term 3 ____   Term 4 ____                   │
   │  These are the questions to redo FIRST. A lucky right answer is a        │
   │  wrong answer that has not happened yet.                                 │
   │                                                                          │
   │  NOTES — one line per term, written the day you marked it                │
   │  T1 ____________________________________________________________        │
   │  T2 ____________________________________________________________        │
   │  T3 ____________________________________________________________        │
   │  T4 ____________________________________________________________        │
   └──────────────────────────────────────────────────────────────────────────┘
```

> **💡 Try this:** at the end of Week 36, hand the student their own record sheet and ask for one sentence at the bottom about what changed. They usually point at the gap between paper and demo closing, and they are usually right.

---

## ⚠️ Six mistakes teachers make with these papers

**1. Marking the number instead of the working.**
A wrong answer with the right working earns most of the marks; a right answer with none earns about half. Those two rulings are what make the paper measure understanding instead of recall. Soften them and the paper stops being an X-ray.

**2. Treating a silent bug like a crash.**
In Section 🅲 the questions with no error message are where students write *"there's no error"* and stop. That is not an answer, and it is not their fault: it is a habit that has to be taught. When you hand the paper back, say the sentence: **"in Level 4 the dangerous bug is the one that prints a number you are pleased with."**

**3. Giving the paper and moving straight on.**
A paper you do not act on costs 85 minutes and teaches the student that assessment is a ritual. **The remediation table is the point of this page.** Mark it, circle at most two weeks, book two 20-minute slots. If you have no time to redo, you had no time to test.

**4. Helping during the paper — or during the demo.**
You will want to. A student stuck on B3 will have the wrong bracket, and saying so converts a diagnosis into a lesson you can then no longer diagnose. In the demo it is worse, because the marks are for what the student *says*. Sit where you cannot read over a shoulder, and mark a book.

**5. Putting the paper and the demo into one number.**
They measure different things. Add them and a student who is strong on one and weak on the other looks average, which is exactly the thing the pair was built to avoid. Report 75 and 15, side by side.

**6. Treating a stand-in result as a result.**
Term 4's tables are made with scripted parts. A student who writes *"the model gets 17 of 25"* has not read the label. Tell them the sentence: **a number from a stand-in is a property of these cases and these scripted parts, and nothing else.** The card in Week 36 says so in its first lines; the paper tests whether they noticed.

---

## ❓ Questions a teacher actually asks

<details>
<summary><b>"I don't know PyTorch. Can I really mark Term 3?"</b></summary>

Yes, and here is why, precisely.

Section 🅱️ is lines of output, and the key prints every one with its trap. Section 🅲 is three marks for *name it, say what happens, fix it* against a printed answer. Section 🅳 is arithmetic you can check: the key writes out each sum in longhand (a cosine, a KL, a bytes-per-token, a log-log slope). Section 🅴 has a row-by-row scheme: each row is "did they quote a number from the table, and did they say the right thing about it".

The only judgement left is the *sentence* rows, and each has an example of what earns it. **The one thing you must do is read the paper through with the key open before you hand it out.** Twenty-five minutes. That is the whole preparation.
</details>

<details>
<summary><b>"My student says the test is unfair because they never saw that."</b></summary>

Check it, because if they are right it matters.

Look up the thing they say they never saw in the [maths ladder](../README.md#-the-maths-ladder) or the [syntax ladder](../README.md#-the-syntax-ladder). Both give the week each idea first appears. Then:

- **If the week is inside the term:** show them the ladder row and the week's student guide page, then ask *"what do you remember about that week?"* — because "I never saw it" and "I saw it and it did not stick" feel identical from the inside and need different fortnights.
- **If the week is after the term:** they are right, it is a defect. Scale the total, skip the question, and tell the course's owner.
- **If it is on neither ladder:** it will be something from Levels 1–3 that this level assumes (`train_test_split`, an f-string, `nn.Linear`). The ladders list those at the top as assumed and never re-taught.
</details>

<details>
<summary><b>"Can I let them use their notes? It feels harsh."</b></summary>

Not for Part 1: **the whole skill is predicting an output before you have it**, and a note that contains the answer removes the prediction. Part 2, on the other hand, *is* open — their own week files, their own `l4lib/`, a machine.

There is a better thing to do than a compromise. Give the paper closed. Mark it. Then hand it back **with** the student guides and say: *"find the page that answers the ones you got wrong, and write the answer in the margin."* Twenty minutes, and it does more than an open-book sitting, because now they know which pages they needed.

If a student is distressed by a closed paper, the concession is **time**, not notes. Ninety minutes instead of seventy costs nothing and measures the same thing.
</details>

<details>
<summary><b>"They wrote the right number with no working. Do I really give half?"</b></summary>

Yes, and say why out loud *before* the paper starts. There are exactly two students who write a bare right number: one who did the sum in their head, and one who remembered that this question's answer was that number. They look identical and need different fortnights, and the working is what tells them apart.

There is also a selfish reason students find more persuasive than the fair one: **the working is what lets them find their own slip.** A student who writes `0.9 × 2.0 + 2.0 = 3.8` can look at it and see it. A student who writes `3.8` cannot.
</details>

<details>
<summary><b>"The student's demo number differs from the key in the last digit."</b></summary>

That is the CPU or the build, and it is not an error in either of you. The papers say so: *a difference in the last digit is the machine; a difference in the first digit is a bug.* If the first digit is different, do not tell them. Ask them to find it. That is the Week 9 Debugging Clinic habit, and it is worth a mark on its own for the way they go about it.

Also check the **creation order**: the demos that fix a seed and then create two layers in a stated order depend on that order. Swapping the two lines changes every number after it, and that is a student mistake, not a CPU effect.
</details>

<details>
<summary><b>"Which paper matters most? I can only run two this year."</b></summary>

**Term 1 and Term 3.**

**Term 1** is the diagnostic that decides whether Term 2 is possible: Weeks 2, 6 and 8 are the three the whole of Term 2 leans on, and the paper finds the hole while there is still time to fill it.

**Term 3** is the one that decides whether Term 4 is possible: the harness, the floor, the guard and "retrieved text is data" (Weeks 23 and 26) are what agents, evals and the capstone are made of.

If you can run three, add **Term 4**, because its paper is the closest thing in the course to an exam of *judgement* — reading a table and saying what it cannot show — and the capstone depends on it. Term 2 is the one most safely replaced by the Week 18 week paper alone.
</details>

<details>
<summary><b>"My student ran out of time on Section 🅴."</b></summary>

Very common. In order:

1. **Mark what is there and note the blank.** Do not guess marks.
2. **Give Section 🅴 as homework that evening, with a 20-minute timer,** and mark it separately. It is 12 marks and the one the year is aimed at.
3. **Next time say the 60-minute sentence:** *"ten minutes — if Section E is blank, go there now."*

Students who run out usually over-invest in Section 🅳, writing out every table in full for 5 marks a part. Tell them the rule: *one visible row of working per part earns marks, so write it quickly and move on.*
</details>

<details>
<summary><b>"Should I let them resit?"</b></summary>

Yes, with two conditions.

**Condition one: redo first.** A resit with nothing in between measures how much they remember of the paper, which nobody needs.

**Condition two: resit the part, not the whole,** unless they were in the bottom band. If the demo was 5 of 15, redo the weeks the remediation table names and then re-sit **only Part 2**, with a different seed or a different input if the student has memorised the output. If the paper was under 45, use the **term test**, which has every number different.

Record both scores on the record sheet. The gap between them is the most useful number it will ever hold.
</details>

<details>
<summary><b>"They got one right by guessing and admitted it. What now?"</b></summary>

**Give the mark, and treat it as wrong.** Both, and neither one instead of the other.

Give it, because the instruction said a guess costs nothing, and going back on that is how you never get an honest "not sure" again. Treat it as wrong, because it is: the record sheet has a line for it, and those are the questions to redo **first**. A student honest enough to write "not sure" beside a correct answer has given you the most useful data on the paper, and should be told so.
</details>

<details>
<summary><b>"Can I use these as end-of-year exams and give a grade?"</b></summary>

You can, and this course would rather you did not. The papers are built as X-rays: the wrong-option maps, the remediation table and the "do not read this as a verdict" band are all aimed at *what to do next*. Turn them into a grade and the incentive shifts from "find out what I do not know" to "protect my number", and the paper stops working.

If you need a summative judgement, use the **[capstone](../projects/capstone.md)**: a design, a frozen eval, a measured system, a red-team log, a system card and a five-minute demo, marked on weighted rows (eval design, measured evidence, guardrails and red-team, honesty of the card, demo). That is a far better measure of Level 4 than any 70 minutes with a pencil, and it is designed for the job. **Assessment 4 is marked separately from the capstone.**
</details>

<details>
<summary><b>"Week 9 prints a different 'redo if' number from this page."</b></summary>

Possibly, at exactly 60%. The week papers and the term tests were authored separately, and a ten-mark week prints `5` on some grids (strictly under 60%) and `6` on others (60% inclusive). It is one mark at the boundary and nothing in the course depends on it. **Use whichever grid is printed with the paper in front of you, and be consistent within a student.**
</details>

---

## 🔑 The things this page is really saying

1. **These are X-rays, not grades.** Every band ends in an instruction, because a score is only useful for deciding what to do on Monday.
2. **Mark the working.** One slip costs one mark; a bare right number costs about half.
3. **No computer on the paper, yes calculator; a computer on the demo.** Predicting is debugging, arithmetic speed is on no ladder, and the proof belongs at a machine.
4. **Report the paper and the demo separately.** Adding them hides exactly the pattern the pair exists to show.
5. **The dangerous bug prints a number you are pleased with.** Half of Section 🅲 has no error message, and that is the defining skill of Level 4.
6. **Terms 1 and 3 decide what comes next.** Weeks 2, 6, 8 carry Term 2; Weeks 22, 23, 26 carry Term 4. If either goes badly, delay the next term.
7. **A stand-in result is a property of the cases, not of a model.** Say it every time.
8. **A paper you do not act on is worse than no paper.** Mark it, circle at most two weeks, book the slots.

---

[⬅ Course home](../README.md) · [Term 1](term-1-test.md) · [Term 2](term-2-test.md) · [Term 3](term-3-test.md) · [Term 4](term-4-test.md) · [Projects](../projects/project-ideas.md) · [Capstone](../projects/capstone.md)

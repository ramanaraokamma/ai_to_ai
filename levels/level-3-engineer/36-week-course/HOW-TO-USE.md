# 🧭 How To Use This Course

**Read this once, before Week 1. It takes ten minutes and it is the only page you have to read twice.**

[Course home](README.md) · [Teacher Orientation](teacher-guide/00-orientation.md) · [Week 1 teacher guide](teacher-guide/week-01.md) · [Week 1 student guide](student-guide/week-01.md) · [Week 1 workbook](workbook/week-01.md)

> **The one sentence:** three books, one week at a time, nothing downloads, and the maths is taught to
> **you** before it is taught to the student.

---

## 📚 The three books, and who opens which

There is one file per week in each of three books. **Same week number, same code, same numbers.**

| Book | Who reads it | What it is | Length |
|---|---|---|---|
| **`teacher-guide/week-NN.md`** | **You, the night before** | The whole lesson: what you need to know first, a prep checklist, the lesson minute by minute with the exact words to say, the activity in full, a debugging clinic, and a complete answer key | ~1,700 lines |
| **`student-guide/week-NN.md`** | The student, during and after | The chapter: hook, concept, the maths worked slowly, code to type, worked examples, mistakes to avoid | ~1,150 lines |
| **`workbook/week-NN.md`** | The student, for homework | Warm-up, maths by hand, *predict the output*, two practice sets, a broken program to fix, a puzzle, a build task, a draw task, a self-check — **and a full answer key at the bottom** | ~1,500 lines |

**Plus, once:** [`teacher-guide/00-orientation.md`](teacher-guide/00-orientation.md) — read **Sections 1–5 before Week 1**. It contains the offline
setup guide, the nine errors you will meet, and the plain-English version of every piece of
mathematics in the year. It is the single most useful file here.

**And around the edges:** [`assessments/`](assessments/README.md) (one test per term, after weeks 9, 18, 27 and 36),
[`projects/`](projects/project-ideas.md) (the capstone brief, a worked example project, and project ideas),
and [`figures/`](figures/STYLE.md) (330 hand-drawn SVGs, plus the style contract they obey).

---

## 🗓️ The weekly rhythm

One class a week, **60–75 minutes**, plus **60–75 minutes** of workbook homework. Four terms of nine
weeks: `1–9` the supervised pipeline · `10–18` the maths of learning · `19–27` real networks in
PyTorch · `28–36` no labels, words, and shipping it.

**Your week, in four steps:**

1. **The night before (25–30 minutes).** Open the teacher guide. Read **🧑‍🏫 What YOU Need to Know
   First** — that section exists so that you understand the maths before the student does. Then work
   the **🧰 Prep Checklist**, which always means *typing and running the week's code yourself*. Do
   not skip that. Seeing the output on your own screen is what makes you calm in the lesson.
2. **The lesson (60–75 minutes).** Follow **⏱️ The Lesson, Minute by Minute**. It gives you a
   segment table with running totals, then, for each segment, **Do this**, **Say this** and **Ask
   this**. The words in *Say this* are written to be said out loud. Use them or your own — but keep
   the order.
3. **Homework.** Assign the workbook. Everything in it is answered at the bottom of the same file, so
   a student who is stuck at 9pm is not stuck.
4. **Next morning, 10 minutes.** Mark against the teacher guide's **🔑 Answer Key**, which restates
   every question so you can mark from that one page.

**The Bug Log.** From Week 1 the student keeps one page: *message · what it meant · what fixed it*.
Every week deliberately breaks something, and the log is where the breakage becomes knowledge. Do not
let it lapse; by Week 20 it is the most valuable page they own.

---

## 🔌 Offline setup, in five lines

```bash
python3 -m venv .venv                     # 1. a private box for this course
source .venv/bin/activate                 # 2. step into it (Windows: .venv\Scripts\activate)
pip install --upgrade pip                 # 3.
pip install "numpy>=1.26" "pandas>=2.0" "matplotlib>=3.7" "scikit-learn>=1.4" "torch>=2.1"
python3 -c "import torch, sklearn; from sklearn.datasets import load_digits; print(load_digits().images.shape)"
```

Line 5 must print `(1797, 8, 8)`. **Full guide with the smoke tests and the Windows traps:**
[Orientation, Section 5](teacher-guide/00-orientation.md). Do it in **Week 0**, not Week 1.

> **⚠️ Nothing in this course downloads a dataset. Ever.** That one `pip install` is the only moment
> the whole year needs the internet. Every dataset either ships inside scikit-learn
> (`load_digits`, `load_iris`, `load_wine`, `load_breast_cancer`), is generated on the spot by numpy
> (`make_moons`, `make_blobs`, `make_classification`, and the pizza-delivery table the student builds
> in Week 1), or is typed by the student (the 80 reviews of Term 4).
>
> **`torchvision` is not needed and must not be installed.** If a student's file imports it, they
> copied a line off the internet. `ModuleNotFoundError: No module named 'torchvision'` is the
> **correct** result. The image dataset of this level is `load_digits()` — 1,797 handwritten digits,
> 8 × 8, which trains a CNN on a laptop CPU in about a second. Weeks 24–27 mention CIFAR-10 exactly
> once each, inside a `💡 When you have internet` callout, as an optional holiday project. No lesson,
> exercise or answer anywhere depends on it.
>
> **Every training run in the course is under about 30 seconds on a laptop CPU.** No GPU. Every code
> block sets a seed, so the numbers printed in the book are the numbers on your screen — with one
> deliberate exception in the Orientation, which exists to show you what happens without one.

---

## 😰 The first thirty minutes of Week 1, for a teacher who fears the maths

**Good news first: there is no mathematics in Week 1.** None. The README's ladder says
*New maths: none*. Week 1 is two divisions and a fraction read as a percentage. The first real new
idea — standard deviation — is Week 4, and by then you will have read it explained twice.

Here is exactly what you do, and it is all preparation you can finish tonight.

**Minutes 0–10 — get the table on your screen.** Open
[`teacher-guide/week-01.md`](teacher-guide/week-01.md), find the Prep Checklist, and type
`make_data.py`. It is the file that stands in for a pizza chain's database. **You are not expected to
understand the maths inside it** — its job is to produce a table. Run it. You must see
`shape: (2020, 10)` and a first `order_id` of **100955**. If you see that, your whole year is set up
correctly, because Weeks 1 to 7 all use this table.

**Minutes 10–20 — type `audit.py` and run it.** Four checks on the table. Four numbers come out:
**20 · 0.9901 · 108 · 0.7119**. You now know more about this dataset than most people know about
theirs. That is the entire technical content of the lesson.

**Minutes 20–30 — read two things and write one.** Read **§2, The five decisions** (what one row is,
X, y, the split, the metric) — it is prose, not maths. Then read the hook story about the column
called `refund_issued`; it is 150 words and it is the emotional centre of the lesson. Finally, write
`model.fit(X_train, y_train)` in the middle of a sheet of A4 and put it face down. That sheet is how
the lesson opens.

**That is your preparation.** In the lesson you say one sentence and then ask one question — *"what
does that line **not** tell you?"* — and write down whatever they say. You are not explaining
mathematics. You are running a conversation, and the teacher guide has the words for it.

> **🧑‍🏫 If a student asks something you cannot answer:** say *"I don't know — write it on the
> board and we'll find out."* Then look in the week's **❓ Questions Students Ask This Week**
> section, which very probably has it. Modelling "I don't know, let's check" is worth more this year
> than any answer you could improvise.

---

## 🖨️ Printing

- **Print the workbook.** One week at a time, double-sided, **before** the lesson. The workbook is
  designed to be written on in pen: it has blank lines, tables with empty cells, and figures with
  labels missing on purpose. **Do not print the answer key half** — it starts at the `## ✅ Answers`
  heading near the bottom of each workbook file. Print up to there, keep the rest for marking.
- **Print the figures that say "blank" or "draw-frame"** at full page. Those are worksheets
  (`fig-wNN-*-label-the-*-blank.svg`, `fig-wNN-*-draw-frame.svg`) and squeezing them onto a quarter
  page defeats them.
- **Every figure is greyscale-safe.** The palette was chosen so that a photocopy still works: shapes
  and labels carry the meaning, never colour alone. Print in black and white without worrying.
- **The student guide reads better on screen** (it has long code blocks). The teacher guide is
  reference — read it on screen, print only the Prep Checklist and the minute-by-minute table if you
  like paper in your hand.
- **Three things on the wall, all year:** the Bug Log, THE VOCABULARY sheet (starts Week 4), and the
  current term's results table. Weeks later refer back to them by name.

---

## 🗺️ Where everything lives

```
36-week-course/
├── HOW-TO-USE.md              ← you are here
├── README.md                  ← the full 36-week ladder: big idea, new maths, new syntax, homework
├── teacher-guide/
│   ├── 00-orientation.md      ← READ FIRST. Setup, the maths explained to you, the 9 errors
│   └── week-01.md … week-36.md
├── student-guide/week-01.md … week-36.md
├── workbook/week-01.md … week-36.md      ← answers at the bottom of each file
├── assessments/               ← README + one test per term (after weeks 9, 18, 27, 36)
├── projects/                  ← capstone.md · worked-example-project.md · project-ideas.md
└── figures/                   ← 330 SVGs, fig-wNN-n-slug.svg · STYLE.md is the contract
```

**Naming is predictable on purpose.** Week 14's three files are `teacher-guide/week-14.md`,
`student-guide/week-14.md`, `workbook/week-14.md`, and its figures are `figures/fig-w14-*.svg`.
Every week's files link to the previous week, the next week, and the other two books, so you can
navigate without coming back here.

**If you only have time for one thing before Week 1:** the [Orientation](teacher-guide/00-orientation.md).
It is written for an adult who knows no AI, no Python and no calculus, and it is honest about which
parts are hard.

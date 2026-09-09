# 🧭 How To Use This Course

**Read this once. It takes ten minutes and it will save you the whole of week 1.**

[Course Home](README.md) · [Teacher Orientation](teacher-guide/00-orientation.md) · [Week 1 teacher guide](teacher-guide/week-01.md) · [Week 1 student guide](student-guide/week-01.md) · [Week 1 workbook](workbook/week-01.md)

---

## 🎯 What you are holding

One school year of Python, for **one 12-year-old who has never written a line of code** and **one
adult who does not know Python either**. 36 weeks, one 60–75 minute class each, plus about an hour of
homework. Every week has code in it. There are **three books**, and using the wrong one is the
commonest way this course goes wrong.

| Book | Who reads it | When | What it is for |
|---|---|---|---|
| 📕 **`teacher-guide/week-NN.md`** | You, alone | The 20 minutes before class | Everything you need to teach a lesson in a language you do not speak. Includes the Python you don't know yet, a minute-by-minute script, the exact words to say, and a full answer key. |
| 📗 **`student-guide/week-NN.md`** | The student, at the keyboard | During and after class | The chapter. The hook, the idea, every code block complete and runnable, the figures, the errors on purpose. |
| 📘 **`workbook/week-NN.md`** | The student, alone | After class | 6–10 exercises, predict-the-output, the week's build, a self-check — and a full answer key at the bottom. |

Plus three folders you rarely open directly: **`assessments/`** (four term tests with mark schemes),
**`projects/`** (capstone brief, worked example, project ideas) and **`figures/`** (359 SVG figures).

---

## 📅 The weekly rhythm

The same seven steps, all 36 weeks. Once you have done it twice you will not need this list.

1. **You, 20 minutes before class.** Open `teacher-guide/week-NN.md`. Read *🧑‍🏫 What YOU Need to Know
   First*, then do the *🧰 Prep Checklist* — it includes typing the week's code yourself once. Do not
   skip that. It **is** the prep.
2. **Class, 60–75 minutes.** Follow *⏱️ The Lesson, Minute by Minute* in order: 🪝 Hook (7) · 🧠 Concept
   (16) · 💻 Live-Code (18) · 🎲 Their Turn (20) · 🔑 Wrap & Assign (9).
3. **The keyboard rule.** During Live-Code, **the student types.** You read the line out loud; they
   type it. Your hands stay off. Their typos are the curriculum, not an accident.
4. **The error on purpose.** Every week has at least one, marked ⚠️ **DELIBERATE MISTAKE**. Do not fix
   it early. Read the **last** line of the traceback out loud, then fix it together.
5. **Homework, about 60 minutes.** The workbook pages named in *📤 Homework to Assign*. The student
   self-marks from *✅ Answers*, in a different colour pen, after finishing.
6. **The Bug Log.** One notebook, kept all year: every real error message, with the fix in the
   student's own words. About 40 entries by June, and the most valuable object they own.
7. **Next week.** Read *🔮 Next Week Preview*. A few weeks need a prep script run in advance, and it
   says so there.

**Weeks 9, 18 and 27 are checkpoints, not new material** — they consolidate a term and end with a test
in `assessments/`. **Weeks 34–36 are the capstone**: the student picks a real question, collects 100
rows of their own data, and defends the answer out loud.

---

## 💻 Software setup, in five lines

Do this in **week 0**, not week 1. A setup problem in week 0 is just setup; the same problem in week
6 feels like failure. Budget 45 minutes and expect to use 30.

```bash
python3 --version                                  # want 3.9+, ideally 3.11+
mkdir -p ~/ai-academy/level2 && cd ~/ai-academy/level2
python3 -m venv .venv && source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install numpy pandas matplotlib scikit-learn   # ~300 MB, one time
python3 -c "import numpy, pandas, matplotlib, sklearn; print('all four fine')"
```

That last line is the whole smoke test. It really prints `all four fine`, and nothing else.

> **⚠️ Watch out — Windows:** on the very first Python installer screen, tick **"Add python.exe to
> PATH"**. That one checkbox is about 90% of all Windows setup pain in this course.

**If any of those five lines misbehaves**, do not improvise — go to
[`teacher-guide/00-orientation.md`](teacher-guide/00-orientation.md) §4.1–§4.8, which has the
step-by-step install, a smoke test proving a chart can appear, and the twelve things that actually go
wrong with the exact fix for each. Those four libraries are the *only* software this course ever
needs; nothing gets installed later.

---

## 🪝 The first 30 minutes of week 1, if you are nervous

You have never programmed. That is fine — this is the exact plan, and none of it needs Python.

**Before they arrive (10 min).** A loaf of bread, still wrapped. A plate. A knife. A laptop with VS Code
open and a terminal showing. Print `workbook/week-01.md` page 1.1, and run `print("Hello, world.")` once
yourself so you have seen it work.

**Minutes 0–7 — the sandwich. Laptop shut.** Say: *"I am a robot. I do exactly what you tell me,
instantly, and I know nothing at all — I have never seen bread. Write me six instructions for making a
sandwich. Two minutes."* Then **do exactly what they wrote, literally.** "Put the bread on the plate" →
put the whole wrapped loaf on the plate. They will laugh, and they will rewrite instruction one
themselves. You have taught the whole idea of the year without opening Python.

**Minutes 7–23 — the concept.** Read §🧠 of the teacher guide out loud, more or less as written. Three
things only: a program is a file of instructions; `print()` puts something on the screen; the computer
reads top to bottom and never guesses.

**Minutes 23–30 — the first file, their hands.** File → New File. Save As `hello.py` into
`ai-academy/level2`. You read each line aloud, they type it:

```python
# hello.py - my first Python program.

print("Hello, world.")
print("My name is Ramana.")
```

Save. In the terminal, **typed not pasted**: `python3 hello.py`.

```text
Hello, world.
My name is Ramana.
```

**And then, deliberately, break it.** Have them delete the closing `)` from line 3 and run it again.
This is the real output:

```text
  File "hello.py", line 3
    print("Hello, world."
         ^
SyntaxError: '(' was never closed
```

Say the sentence you will say all year: **"Read me the last line. Not the top — the bottom."** Then fix
it, run it, and write the error in the Bug Log. That is minute 30, and the year is under way.

> **🧑‍🏫 If a student asks a question you cannot answer:** say *"I don't know — let's find out"* and look
> it up together. Every week's teacher guide has a *❓ Questions Students Ask This Week* section that has
> already answered most of them.

---

## 🖨️ Printing

Everything is plain Markdown with relative links, so it prints from anything that renders Markdown —
VS Code's preview → Print, Typora, `pandoc`, or pasted into a word processor.

- **Print the workbook.** All 36 weeks, double-sided, in a ring binder. It has `______` blanks and
  pencil-sized tables; it is meant to be paper. **Tear the answer key off first** — `## ✅ Answers` is
  the last section of every workbook file, so print up to it for the student and keep the rest.
- **Do not print the student guide.** It is read at the keyboard, because the code is meant to be typed
  while it is on screen. Print the teacher guide one week at a time, the night before.
- **Figures print in black and white.** Every colour was chosen so the greyscale version still reads;
  nothing in this course depends on hue alone.

---

## 📂 Where everything lives

```
36-week-course/
├── HOW-TO-USE.md          ← you are here
├── README.md              ← the map: all 36 weeks, the four terms, the syntax ladder
├── teacher-guide/         ← 00-orientation.md (READ FIRST) + week-01.md … week-36.md
├── student-guide/         ← week-01.md … week-36.md
├── workbook/              ← week-01.md … week-36.md
├── assessments/           ← README.md + term-1-test.md … term-4-test.md, with mark schemes
├── projects/              ← capstone.md · worked-example-project.md · project-ideas.md
├── figures/               ← STYLE.md + 359 fig-wNN-n-slug.svg files, ~9 per week
└── site/index.html        ← an optional browsable index
```

`teacher-guide/00-orientation.md` is the one file to read before anything else: a Python mini-course for
adults, the twelve errors beginners hit, and the install guide.

**Three things to bookmark:**

1. [`README.md` → 🪜 The Syntax Ladder](README.md#-the-syntax-ladder) — every Python construct and the
   week it first appears. When a student uses something you do not recognise, look it up here. If its
   week is later than this one, they found it on the internet, and the honest answer is *"Nice. We meet
   it properly in week 13 — can you explain it to me?"*
2. [`teacher-guide/00-orientation.md`](teacher-guide/00-orientation.md) §2.0–§2.13 — the twelve error
   messages beginners actually hit, each with a real traceback and the fix. Keep it open in a tab.
3. The *🐞 The Debugging Clinic* section of the week you are teaching — the errors *that week* produces,
   in the order they usually appear.

---

## 🔑 Four promises this course makes to you

1. **Every code block was really run before it was pasted**, and every number in a `text` block was
   printed by a machine. Type it exactly, get something different, and that is a bug worth reporting.
2. **Nothing is used before the week that introduces it** — max four new pieces of syntax and five new
   words a week, all year, enforced by the Syntax Ladder.
3. **Every week teaches one real error on purpose**, with the genuine traceback, explained and fixed.
4. **You do not need to know Python.** Everything you need is in that week's teacher guide, written for
   an adult learning it the night before.

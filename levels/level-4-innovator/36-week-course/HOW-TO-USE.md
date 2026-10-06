# 🧭 How To Use This Course

**Read this once, before Week 1. It takes ten minutes, and it is the only page you have to read twice.**

[Course home](README.md) · [Week 1 student guide](student-guide/week-01.md) · [Week 1 workbook](workbook/week-01.md)

> **The one sentence:** one week at a time, type everything, nothing downloads, and every number you
> write down must have been printed by your own run.

---

## 📚 The three books, and who opens which

There is one file per week in each of three books. **Same week number, same code, same numbers.**

| Book | Who reads it | What it is |
|---|---|---|
| **`teacher-guide/week-NN.md`** | **The adult running the course, the night before** | The whole lesson, minute by minute, with the answers. **The student does not open it.** |
| **`student-guide/week-NN.md`** | You, during and after class | The chapter: a real measured number as a hook, the idea, the code to type, the real output, this week's error read line by line |
| **`workbook/week-NN.md`** | You, for homework | Warm-up, by-hand arithmetic, predict-the-output, a broken program, a build task, a self-check, and an answer key at the bottom |

**The answer key is at the bottom of each workbook file, sealed behind a line that says ✂️ ANSWERS.**
Struggle for 15 minutes first. Being stuck for a while is the part that works.

**Around the edges:** `assessments/` (your teacher keeps this folder; one paper per term, after weeks 9, 18, 27
and 36; 75 minutes, no computer), and [`projects/`](projects/project-ideas.md) (offline project ideas, any
time from Week 12, plus the [capstone brief](projects/capstone.md) for Weeks 34-36).

---

## 🗓️ The weekly rhythm

One class a week, **60-75 minutes**, plus **60-75 minutes** of workbook homework. Four terms of nine weeks:

| Term | Weeks | The question you can answer at the end |
|:--:|:--:|---|
| 1 | 1-9 | Your loss curve is wrong. Which knob do you turn, and how do you know before you turn it? |
| 2 | 10-18 | Why can a network not remember forty steps back, and what did people build instead? |
| 3 | 19-27 | Where does a language model's behaviour come from, and how do you test it like an engineer? |
| 4 | 28-36 | Can you build a product from the parts, attack it yourself, and say honestly where it breaks? |

**Your week, in four steps:**

1. **In class.** Have the student guide open and a terminal in the right folder (see below). Type the
   code yourself. Never paste it: a typed-in `bpe.py` in Week 20 is the whole point.
2. **Homework.** Open the workbook. Do the by-hand pages **with a pen**, before any code, then let the
   code check you. When the arithmetic and the code disagree, **stop: that is a finding, not a nuisance.**
3. **Check.** Mark yourself against the key at the bottom, then write what you got wrong.
4. **Bug Log.** One page, all year: *message · what it meant · what fixed it.* Every week deliberately
   breaks something. The log is where the breakage turns into knowledge. By Week 20 it is the most
   useful page you own.

---

## 🔌 Setup, in two checks

Level 4 installs **nothing new**. Level 3's five libraries (`numpy`, `pandas`, `matplotlib`,
`scikit-learn`, `torch`) are the whole stack. Do these in a **Week 0** sitting, not in Week 1.

**Check 1. Open a terminal in the `36-week-course/` folder**, the one that *contains* `l4lib/`. Every
import this year is `from l4lib... import ...`, so being in the wrong folder (`No module named 'l4lib'`)
is the commonest error of the first fortnight. Then run:

```python
import numpy, pandas, matplotlib, sklearn, torch
print("numpy", numpy.__version__, "| sklearn", sklearn.__version__, "| torch", torch.__version__)
try:
    import torchvision
    print("torchvision present (unused, and nothing may depend on it)")
except ImportError:
    print("torchvision absent, as expected")
```

```text
numpy 1.26.4 | sklearn 1.7.1 | torch 2.2.1
torchvision absent, as expected
```

Any torch `2.x` is fine. **`torchvision absent` is the correct answer.** If your file imports it, you
copied a line off the internet.

**Check 2. The data fingerprint**, the same thing Week 1 starts with. Save it as `fp.py` and run it from
the same folder:

```python
import torch
torch.set_num_threads(1)
from l4lib.spirals import make_spirals, get_data
X, y = make_spirals(n=600, noise=0.22, seed=0)
print("X", X.shape, X.dtype, "  y", y.shape, y.dtype, "  first x-coordinate", round(float(X[0, 0]), 3))
Xtr, ytr, Xva, yva = get_data()
print("train", tuple(Xtr.shape), " val", tuple(Xva.shape))
print("train class counts:", ytr.bincount().tolist(), "  val class counts:", yva.bincount().tolist())
```

```text
X (1200, 2) float32   y (1200,) int64   first x-coordinate 2.734
train (840, 2)  val (360, 2)
train class counts: [431, 409]   val class counts: [169, 191]
```

If those four lines match, Weeks 1 to 7 will match too. If they do not, stop and ask before going on.

---

## 🌱 Why your numbers match the book, and when they will not

Every code block sets a seed and was run on a laptop CPU with one thread. Try it:

```python
import torch
torch.set_num_threads(1)
from l4lib.spirals import run
a = run("first ", lr=1e-3, epochs=5)
b = run("second", lr=1e-3, epochs=5)
print("identical training curves:", a["train"] == b["train"])
```

```text
first                        train 0.494  val 0.420  acc  63.1%
second                       train 0.494  val 0.420  acc  63.1%
identical training curves: True
```

**The tolerance the weeks use: losses within ±0.005, accuracies within ±0.5 percentage points.** A
different PyTorch or CPU can move the third decimal, so an exact match is not the test. A difference in
the **first** decimal means something real is different: the seed, the folder, or you forgot
`torch.set_num_threads(1)`. Find out why now.

> **The rule that is new this year:** any number you write in a report must have been printed by your
> own run, with a seed, in the last 24 hours. A number copied from the book is never a substitute.

---

## 🏷️ "Stand-in, not a model"

From Week 23 on, parts of the course talk to a **scripted** program instead of a real language model.
This is on purpose: real models are hosted, and nothing here may use an account, an API key or a
download. The honest trade is this:

- A stand-in teaches the **scaffolding**: the loop, the contracts, the fences, the traces, the cost shape.
- It does **not** teach what a real model does. A rate you measure against it is a property of the
  stand-in, not of the world.
- So **every scripted backend is labelled, and you say the label out loud** before your first run:
  *"Today's backend is a stand-in for a model, not a model."* When you quote a number, say which kind it
  is ("17 of 25, against the stand-in"). Your written reports carry the label in the first lines.
- Numbers quoted from the literature (GPT-2's size, Chinchilla's ratio) are marked **quoted, not
  reproduced here**. They are context, never an exercise.

---

## ⏱️ Runs that take time

Most weeks nothing runs longer than about ten seconds. The exceptions are Week 12 (about 25 s), Week 13
(about 40 s), **Week 17 (TinyGPT, about 80-95 s)**, **Week 19 (five ablation models, about 3.5 min)**,
Week 21 (two runs of about 90 s) and Week 24 (about 4 min in all). Start the long run first, then think
about what loss you expect before step 1.

Use the **stated reduced default**. If your laptop is far slower, lower `steps` by a stated amount and
write that in your Bug Log. **Never change the seed, and never shorten a run silently.**

---

## 🚑 If something goes wrong

| Symptom | What it means | What to do |
|---|---|---|
| `ModuleNotFoundError: No module named 'l4lib'` | Wrong folder | `cd` to the folder that contains `l4lib/` |
| `pip` returns 403 | The corporate proxy | **Not an error.** Close the terminal; nothing needs installing |
| `import torchvision` or `transformers` fails | Not installed, and nothing may depend on it | Expected. Do not try to install it |
| You want `tiktoken`, `from_pretrained` or an API key | Each one downloads | "It would download. Here is what we use." Use the week's stand-in |
| `import tokenizers` fails | Only Week 20 uses it | Week 20 still works: your own BPE is the deliverable |
| A number differs in the third decimal | A different PyTorch or CPU | Within tolerance; carry on |
| A number differs in the first decimal | Seed, folder, or `set_num_threads(1)` | Find out why before continuing |
| A run is far slower than the book | Power saving, or another program running | Plug in; close things; keep one thread |
| A stand-in's result looks "too clean" | It is a script, so of course it is | Restate the label aloud |
| A chart window never appears | A headless backend | `fig.savefig("name.png")` and open the file |

**When a run crashes:** read me the last line. Which line was the last that definitely worked? Print the
shape there. **If you are still stuck after 12 minutes of real attempts, write it in the Bug Log and
ask.** Many blocks are *deliberately* broken to teach you to read a traceback, so read the words around
a failing block before you "fix" it.

---

## 🧱 Three things to know before Week 1

- **There is no new maths in Week 1.** You use `ln` once, on one number, to see why a model that is
  guessing between two classes scores **0.693**. The first new idea is in Week 2 (a running average),
  and it is worked on real numbers before it is named. Thirteen weeks carry one small new idea each.
- **Week 1 also starts your Bug Log.** If you kept one in Level 3, carry on; otherwise start a fresh page.
- **"I don't know" is a good answer.** Write it down and find out. Modelling that is worth more this
  year than any answer improvised.

---

## 🖨️ Printing

- **Print the workbook**, one week at a time, double-sided, before class. It is made to be written on
  in pen. **Do not print the answer key:** it starts at the `✂️ ANSWERS` line near the bottom.
- Read the student guide on screen; its code blocks are long.
- **Three things on the wall all year:** the Bug Log, your vocabulary list, and the current term's
  results table. Later weeks refer back to them by name.
- Bring a **notebook and pen** to every class. Every week has a by-hand step, and a ruler is useful for
  the log-log line in Week 21.

---

## 🗺️ Where everything lives

```
36-week-course/
├── HOW-TO-USE.md              ← you are here
├── README.md                  ← the 36-week plan: big idea, new maths, new syntax, homework
├── l4lib/                     ← the shared kit you import from (do not copy it, do not edit it)
├── teacher-guide/             ← for the adult running the course, not for you
├── student-guide/week-01.md … week-36.md
├── workbook/week-01.md … week-36.md      ← answers at the bottom of each file
├── assessments/               ← one paper per term (weeks 9, 18, 27, 36)
└── projects/                  ← capstone.md · project-ideas.md
```

**Naming is predictable on purpose.** Week 14's files are `student-guide/week-14.md` and
`workbook/week-14.md`. Every week links to the previous week, the next week and the other book, so you
can navigate without coming back here.

**If you only have time for one thing before Week 1:** run the two checks above, then read the
[Week 1 student guide](student-guide/week-01.md) with a pen in your hand.

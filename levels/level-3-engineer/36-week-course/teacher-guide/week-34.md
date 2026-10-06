# Week 34 — Ship It, Part 1: The Contract and the Artifact

[⬅ Week 33](week-33.md) · [Course Home](../README.md) · [Week 35 ➡](week-35.md) · [Student Guide](../student-guide/week-34.md) · [Workbook](../workbook/week-34.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Capstone, part 1 of 3 — the first week of the year where the deliverable is **not a score** |
| **Big idea** | A model somebody else can use starts with a **written contract** — what one prediction is about, what goes in, what comes out, what the two errors cost, where the threshold came from, and what this must never be used for. **Write all six before you write any serving code.** |
| **New vocabulary** | prediction contract · artifact versioning · golden test · cold start · latency |
| **New maths** | **None.** One cost sweep and one addition, both using Week 11's expected-cost arithmetic. |
| **New syntax** | `argparse.ArgumentParser()` · `json.dump` / `json.load` · `time.perf_counter()` · `Path(...).mkdir(parents=True, exist_ok=True)` |
| **Dataset** | **The student's own.** Either their Week 33 sentiment engine (Path A — recommended) or their Week 26/27 digits CNN (Path B). The reference corpus in this file is 80 typed reviews plus 12 negation traps; the Path B reference is `load_digits()`. **Nothing downloads.** |
| **Materials** | Printed workbook pages 34.1–34.7 · **a big blank sheet headed THE SIX BOXES** (it stays up for three weeks) · one **A4 CONTRACT sheet per student**, printed, with the six boxes empty · the Bug Log · their Week 33 (or Week 26) folder on disk |
| **Tech needed** | Laptop with Python 3, numpy, scikit-learn, **joblib** — and torch only for Path B. **No new installs. `argparse`, `json`, `time` and `pathlib` all ship with Python.** |
| **Prep time** | 30 minutes the night before · 10 minutes on the day |
| **Expected runtime of the code** | `train.py` is **under 2 seconds** on Path A (about 4 seconds on Path B). `predict.py` from a cold terminal is **about 0.8 seconds, almost all of it import**. `tests.py` is under a second. **Nothing in this week is slow. Time yours anyway.** |

> **⚠️ Watch out:** the temptation this week is to start typing. Don't let them. **Twenty-five silent minutes writing a contract on paper is the lesson**, and a class that skips it produces a service whose CLI says `POSITIVE` and whose log says `1`, and nobody notices for a month. If you are running short, cut the Path B demo, cut the stretch, cut anything — **do not cut the silence.**

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Write a six-box prediction contract** for their own model: the unit of prediction, the input field with its type, the output fields, both errors named *in the language of the application* with a price on each, the threshold **with the arithmetic that chose it**, and two banned uses.
2. **Freeze a trained model into a versioned artifact** — `sentiment_v1.joblib` and `sentiment_v1.metadata.json` beside it, plus a one-line `LATEST` file — with the architecture living in a `model_def.py` that **both** the training script and the serving script import.
3. **Run a `predict.py` CLI from a cold terminal** that contains zero training code, takes its input from the command line, and reports **two separate times**: how long the model took to load and how long the prediction took.
4. **Write three golden tests and make them pass**, and say for each one *why that input* — how far its probability sits from the threshold, and what a flip would mean.

Observable evidence: an A4 contract sheet with all six boxes filled in and box 5 showing a subtraction or a cost sum; `model/artifacts/` holding three files with a version in two of the filenames; `python3 serve/predict.py "..."` answering in a terminal opened thirty seconds ago; `grep -rnE "\.fit\(|train_test_split|optimizer" serve/` printing nothing; and `tests.py` printing `3/3 passed`.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each carries on from the one above. **The complete runnable files are in the Prep Checklist and the Answer Key.**

**There is no new mathematics this week and no new idea about learning.** Everything new is about *handing something over*. That makes this the easiest week of the year to prepare and the easiest one to teach badly, because there is no hard concept to hide behind — only a set of disciplines, and disciplines only land if you model them.

Read the six numbered sections below. They take about twenty minutes and they will let you answer every question in the room.

### 1. Why the contract comes first, and what breaks without it

Here is the situation the whole of Weeks 34 to 36 is about.

It is eleven at night. Your model has been running for three weeks. Somebody messages you: *"it said my comment was positive and it obviously isn't."*

Can you answer them? Only if you can say **which version** of the model answered, **what exactly** was sent in, **what probability** came back, **against which threshold**, and **how long it took**. Every one of those is a decision you make *before* the message arrives. If you did not decide them in advance, the honest answer is "I don't know", and "I don't know" is how trust dies.

> **Prediction contract** — a written page saying what one prediction is about, what goes in, what comes out, what each kind of mistake costs, what threshold you chose and why, and what this model must never be used for.

The moment you write *"the output is a JSON object with these five fields"*, you have made a promise. Everything downstream is now decided: what the CLI prints, what the service returns, what the log file records, what the model card has to report. Teams that skip this step end up with a command-line tool that prints `POSITIVE`, a service that returns `1`, and a log that records `True` — three names for one thing, and no way to join them up.

![The prediction contract, six boxes](../figures/fig-w34-1-prediction-contract-six-boxes.svg)
*Figure 34.1 — The prediction contract, six boxes. All six filled in before a line of serving code is written. Box 5 is arithmetic, not taste; boxes 4 and 6 are the two nobody writes, and the two a stranger needs most.*

**Box 1 is the one students get wrong, and it is Week 1's question wearing a suit.** "One prediction is about one **review**" is right. "One prediction is about one **person**" is wrong, and the difference is not pedantry: if a prediction is about a person, then two reviews by the same person must agree, and you have quietly promised something your model cannot do. **Make them say the noun out loud.**

**Box 4 is where most of the thinking is.** Not "a false positive is when the model says positive and it isn't" — that is a definition, not a cost. In the language of the application: *"a nasty comment marked positive is a nasty comment nobody reads. A nice comment marked negative is a nice comment a moderator wastes ten seconds on."* Then a price on each, and a ratio.

**Box 6 is the one that separates this course from a tutorial.** A reasonable person, handed a sentiment model, will try to use it to decide who gets banned. You are going to tell them not to, in writing, before they ask.

### 2. The artifact, and the two rules that make it checkable

> **Artifact** — the one file (or small set of files) that holds a trained model and everything it needs, so a fresh program can make predictions with no training code at all.

Week 3 already taught `joblib.dump(pipe, "m.joblib")`. This week adds two rules on top of it, and both exist because both were real disasters.

> **Rule 1 — the fresh-process rule.** Nothing in `serve/` imports anything from `train.py`.
> **Rule 2 — the version rule.** Every artifact has a version in its filename, and every prediction carries that version string.

Rule 1 sounds like advice. It is not: it is **mechanically checkable**, and that is the whole point of putting training in a folder called `model/` and serving in a folder called `serve/`:

```bash
grep -rnE "\.fit\(|train_test_split|DummyClassifier|optimizer" serve/
```

If that prints nothing, `serve/` very probably has no training code in it (a strong check, not a proof: the pattern would miss `fit_transform` or `.fit (`, and it also matches comments and strings). If it prints anything, look at each line and treat a real match as a bug — **regardless of whether the program currently works**. A rule you can check beats a rule you promise.

![One model definition, imported by both sides](../figures/fig-w34-2-shared-model-def-imported-twice.svg)
*Figure 34.2 — One model definition, imported by both sides. `model_def.py` holds the class names, the input field name and the architecture. `train.py` imports it to build; `predict.py` imports it to read. Two folders make Rule 1 a thing you can check instead of a thing you promise.*

Rule 2 costs six characters — `_v1` — and buys you the ability to go back. The first time a student retrains and overwrites `model.joblib`, they destroy the model that was working and there is no way back. **`sentiment_v1.joblib`, never `model.joblib`.**

And then one line of text says which version is live:

```
model/artifacts/LATEST      ← contains exactly:  sentiment_v1
```

Thirteen bytes. A rollback is one edit to those thirteen bytes.

![Three files, and the line that says which is live](../figures/fig-w34-3-artifact-versions-on-disk.svg)
*Figure 34.3 — Three files, and the line that says which is live. The 10,228-byte artifact holds the whole 287-word vocabulary, the idf weights and the coefficients. The 421-byte metadata holds the threshold and the library versions. The 13-byte `LATEST` holds the name.*

### 3. Every new line of this week's code, explained to somebody who has never programmed

Four new constructs. Here is each one, with no assumed knowledge.

**(a) `argparse.ArgumentParser()` — reading words off the command line.**

When you type this in a terminal:

```bash
python3 serve/predict.py "cold food and a rude driver" --json
```

everything after the filename is a **command-line argument** — a word (or a quoted phrase) handed to the program as it starts. `argparse` is Python's tool for reading them. Three lines:

```python
ap = argparse.ArgumentParser()            # make a reader
ap.add_argument("text")                   # expect one unnamed thing, call it text
ap.add_argument("--json", action="store_true")   # an optional on/off switch
args = ap.parse_args()                    # go and read them
```

After that, `args.text` is the string `"cold food and a rude driver"` and `args.json` is `True`. `add_argument("text")` with no dashes means **positional** — required, and identified by where it sits. `add_argument("--json")` with two dashes means **optional** — a named switch. `action="store_true"` means "this switch carries no value; just record whether it was there."

You get two things free. Typing `--help` prints a usage message you never wrote. And typing something impossible gets refused before your code runs:

```text
predict.py: error: argument --threshold: invalid float value: 'abc'
```

**(b) `json.dump` and `json.load` — writing and reading structured data as plain text.**

JSON is a way of writing a dictionary as text. `{"threshold": 0.65, "classes": ["negative", "positive"]}` is a dictionary in Python and *also* a valid JSON document. `json.dump` writes one to an open file; `json.load` reads one back.

```python
with open(path, "w") as f:       # "w" = open for writing, wiping whatever was there
    json.dump(meta, f, indent=2) # write the dictionary meta into file f, prettily

with open(path) as f:            # no "w" = open for reading
    meta = json.load(f)          # read it back as a dictionary
```

**The argument order catches everybody once.** It is `json.dump(thing, file)` — the data first, the file second. Get it backwards and you get this, which is a real message from a real run:

```text
TypeError: Object of type TextIOWrapper is not JSON serializable
```

`TextIOWrapper` is Python's name for an open file. The message is saying *"you asked me to turn a file into text, and I don't know how."* Good message, once you know the words.

**(c) `time.perf_counter()` — a stopwatch.**

It returns a number of seconds. The number on its own is meaningless — it is counted from some arbitrary moment. What means something is the **difference** between two readings:

```python
t0 = time.perf_counter()              # start the stopwatch
prob = pipe.predict_proba([text])     # do the thing
latency_ms = (time.perf_counter() - t0) * 1000    # stop it, and convert to ms
```

`× 1000` because there are 1000 milliseconds in a second, and milliseconds are the unit everybody reports.

> **Latency** — how long one prediction took, measured from just before it to just after it.

**Where you put the stopwatch is a decision, not a detail.** Put it round the prediction only and you get the per-request cost. Put it round the model loading and you get the cold start. **These are two different numbers and reporting them as one is the most common latency lie in the industry.** We report both, separately, labelled.

**(d) `Path(...).mkdir(parents=True, exist_ok=True)` — making the folders you need.**

`Path` comes from `pathlib`, and it is a tidy way of writing a location on disk. `Path("model") / "artifacts"` means the folder `artifacts` inside the folder `model` — the `/` is doing a job here, not dividing anything.

```python
ARTIFACTS = Path(__file__).resolve().parent / "artifacts"
ARTIFACTS.mkdir(parents=True, exist_ok=True)
```

- `__file__` is the path of the script that is running.
- `.resolve()` turns it into a full path from the root of the disk, so **it works no matter which folder you ran the command from.** That is exactly what makes the cold-start test possible.
- `.parent` is the folder that file lives in.
- `mkdir` makes a folder. `parents=True` means "make any missing folders above it too". `exist_ok=True` means "if it is already there, that is fine, say nothing."

Leave out the `mkdir` and you get this real message the first time you run it on a clean machine:

```text
FileNotFoundError: [Errno 2] No such file or directory: 'artifacts/sentiment_v1.metadata.json'
```

Python will happily create a *file*. It will never create a *folder* for you.

### 4. Cold start versus per-request, with the real numbers

This is the single most useful measurement in the week, and it surprises people.

Run this in a fresh Python, timing each step (the full script is in the Prep Checklist):

```text
import joblib            :   92.2 ms
FIRST joblib.load        :  659.3 ms
SECOND joblib.load       :    0.4 ms
FIRST predict_proba      :    0.4 ms
SECOND predict_proba     :  0.173 ms
```

**Read those five lines slowly, because four of them are surprising.**

The artifact is 10,228 bytes. Reading 10,228 bytes off a disk takes almost no time. So why did the first `joblib.load` take 659 milliseconds? **Because unpickling the file makes Python import the scikit-learn machinery the file needs** — the vectorizer, the logistic-regression class, the sparse-matrix code — and importing those is what costs. The *second* load of the same file takes 0.4 ms, because everything is already imported.

So the cold start is:

```
  92.2  (import joblib)
+ 659.3  (first load — mostly scikit-learn importing itself)
+   0.4  (the actual prediction)
───────
  751.9  ms total
```

and `751.9 ÷ 0.4 ≈ 1,880`. **The answer is one part in about 1,880 of the wait.**

> **Cold start** — the time from starting a brand-new program to getting its first answer, with nothing pre-loaded.

**Now the honest bit, and it matters because the folklore is wrong.** You will read everywhere that loading the model inside the request handler "turns a 2 ms prediction into a 400 ms one". On *this* artifact, in a process that is already warm, reloading costs **0.4 ms** — two or three times the prediction, not two hundred. I measured it; so should you.

The rule "load once at startup" is still correct, and here is the honest reason: **the cost you are avoiding is the cold start, and the cost you are avoiding grows with the model.** On the Path B torch model the same measurement gives 0.036 ms to predict with a loaded model and 0.264 ms to rebuild-load-and-predict — **7.3 times more.** On a hundred-megabyte model it is thousands of times more.

**Say the true thing:** *"load once, and here is my measured number, which is smaller than the number you will read online because my model is 10 kilobytes."* A student who can say that sentence has learned more than one who repeats the folklore.

### 5. Golden tests: three answers you have decided must never change

> **Golden test** — an input whose answer you write down on the day you freeze the model, so that if the answer ever changes you find out in five seconds instead of from a user.

It is the cheapest test in existence and it takes eleven lines. Pick three inputs, assert their labels, print pass or fail, and exit with a code the shell can read.

**Choosing the three is the skill.** A golden test sitting at `p = 0.6501` against a threshold of `0.65` will flip the first time anything at all changes, and then it is an alarm that cries wolf. **Pick inputs a long way from the line and say how far.**

![Three golden answers, frozen on the probability line](../figures/fig-w34-4-golden-tests-frozen-answers.svg)
*Figure 34.4 — Three golden answers, frozen on the probability line. The closest one is `0.7661 − 0.65 = 0.1161` clear, so nothing small can flip it. The greyed triangle at 0.4887 is a known failure, not a golden test.*

And the level-5 move, which one or two students will find: **freeze a known failure too.** The reference model calls *"not boring for a single minute"* negative, at `p = 0.4887`. That is wrong. Asserting that it stays wrong is not defeatism — it is how you find out the day it changes, which is the day you can claim you fixed something.

### 6. The three misconceptions you will actually meet

**"The threshold is 0.5 because that's the default."** No. `0.5` is what you get if you never decide. Box 5 of the contract is a cost sum, and the answer for the reference model is `0.65`. A student who writes `0.5` with no arithmetic gets one question: *"what did you compare it to?"*

**"The artifact is the model."** Nearly. The artifact is the model **and every preparation step it depends on**. Week 3's whole lesson. The test sentence to give them: *"if I deleted your notebook right now, could you still predict correctly?"* If the answer involves remembering to lowercase something first, the artifact is incomplete.

**"A version number is for big teams."** The opposite — it is for one person with one laptop, because one person with one laptop is the person most likely to overwrite the only copy of the thing that worked. Six characters.

### 7. How deep to go, and where to stop

**Go this deep:** the six boxes, the two folders, the three files on disk, two latency numbers, three golden tests.

**Stop before:** HTTP (that is next week, and starting it today wrecks both weeks) · authentication · Docker · cloud anything · `dataclasses` (a dictionary is enough and dictionaries are Week 13 of Level 2) · `pytest` (eleven lines of plain Python is a better teacher) · `git` beyond mentioning it exists.

**If a student asks "isn't this just admin?"** — the honest answer is yes, and that the admin is the part that decides whether anybody ever uses what you built. Then point at box 4 and ask them what a mistake costs. That is not admin; that is the only question in the room with a number in it.

---

### 8. 🧭 The Growing Map — the last box opens, and nothing is dashed any more

The student guide carries a figure called **Where This Fits**: the same picture every week with one more
piece filled in. Today the gold moves to the tenth and final tile, and for the first time since Week 1
**there is not a single dashed box on the page.**

![The Level 3 pipeline in Week 34: the last tile opens with the contract and the frozen artifact](../figures/fig-w34-0-where-this-fits.svg)

*Figure 34.0 — Week 34's version. The gold has moved to `ship it · showcase`, and every other box is solid.
The ↻ on stage three is black, as it has been since Week 12.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Ask "which box did we do today?" — then "what is different about this picture?"** The gold has moved
   for the last time, and somebody in the room will spot the real change: **no dashes.** Let them say it.
   *"Every box on this map is now something you have actually done. The one you are standing in is the
   tenth of ten."*
2. **Anchor it on the contract sheet and the three files.** Hold up a completed A4 contract. *"Today's box
   produced this, and it has no score on it anywhere."* Then the folder listing: `sentiment_v1.joblib`,
   `sentiment_v1.metadata.json`, and a `LATEST` file that is **thirteen bytes**. Then `tests.py` printing
   `3/3 passed`, and `grep -rnE "\.fit\(" serve/` printing nothing. **Four pieces of evidence, no
   accuracy figure among them — that is what makes this week different from the other thirty-three.**
3. **Point back at stage one, and make them find the overlap themselves.** *"Boxes 1, 2 and 3 of your
   contract — which tile did you first write those in?"* The answer is `decisions · the split`, Week 1, and
   the wording is almost identical. Then box 5: *"and which tile is `10 × 1 + 1 × 0 = 10` against
   `10 × 0 + 1 × 4 = 4` from?"* — `threshold · cost`, Weeks 10–11. **The contract is not new work; it is
   the map, written out as prose.** That realisation is worth more than anything else you can say today.

> **🧑‍🏫 Why this is worth two minutes.** This is the week most likely to be dismissed as admin, and the
> map answers that better than an argument does: **the course was always heading at this box, and the
> writing you did today is quoting Weeks 1, 10 and 11 back at you.** A student who sees the contract as the
> *consequence* of the first stage rather than as paperwork bolted on at the end will actually fill in box
> 6, which is the one that matters and the one they skip.

**One thing to notice, so you can answer if asked.** A student may point out that `ship it · showcase` is
gold while its own weeks say `wk 34–36`, and ask why the week label has disappeared from the tile. It has
been replaced by the badge — the badge lives *inside* the row-B tiles, because there is no room beneath
them. Nothing has moved; the label is the same size in the same box. **If they noticed, tell them that is
exactly the kind of attention Part C of the Week 36 paper rewards.**

---

## 🧰 Prep Checklist

### 30 minutes the night before

- [ ] **Read §1 to §6 above.** Twenty minutes. There is no maths to practise this week, which is why the prep is reading rather than doing.
- [ ] **Decide which path the class is on, and write it on the board.** Path A (their Week 33 sentiment engine) for everybody unless a student was much prouder of their Week 26 digits CNN. **Everything in the lesson works for both; Path B has one extra gotcha, in §5 of the Answer Key.**
- [ ] **Print** workbook pages 34.1–34.7, and **one A4 CONTRACT sheet per student** — the six boxes, empty, big enough to write in. This sheet is the lesson.
- [ ] **Put up the blank THE SIX BOXES wall sheet.** It stays up until Week 36.
- [ ] **Build the reference project yourself, below, and run all four commands.** Twenty minutes including reading. Do not skip it: you need to have seen `3/3 passed` with your own eyes.
- [ ] **Check the folders their Week 33 work is in.** If three students have their reviews in a notebook and nowhere else, you need to know that tonight, not at minute 44.

**Create this tree** (empty folders included — the folders are half the lesson):

```text
ship-it/
├── model/
│   ├── reviews.py        ← their Week 33 corpus. DATA ONLY.
│   ├── model_def.py      ← the shape of the model, imported by both sides
│   ├── train.py          ← the only file allowed to fit anything
│   └── artifacts/        ← empty for now
├── serve/
│   ├── predictor.py      ← the ONE place a prediction happens
│   └── predict.py        ← the CLI
└── tests.py              ← three golden tests
```

**`model/model_def.py`:**

```python
"""model_def.py — the shape of the model, in ONE place."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

CLASSES = ["negative", "positive"]   # index 0 and index 1. Never reorder this.
INPUT_FIELD = "text"                 # the one field a request must carry


def build_model(ngram_max=2, C=4.0):
    """The architecture. Called by train.py only — but DEFINED here only."""
    vec = TfidfVectorizer(lowercase=True, ngram_range=(1, ngram_max))
    clf = LogisticRegression(C=C, max_iter=1000)
    return make_pipeline(vec, clf)
```

**`model/train.py`** (the full file — `reviews.py` is the 80-review corpus from Week 33, reprinted in the Answer Key):

```python
"""train.py — makes ONE versioned artifact. Training lives here and nowhere else."""
import argparse
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import sklearn
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_def import CLASSES, INPUT_FIELD, build_model
from reviews import load_corpus

ARTIFACTS = Path(__file__).resolve().parent / "artifacts"


def main():
    ap = argparse.ArgumentParser(description="Train one versioned sentiment artifact.")
    ap.add_argument("--version", default="1")
    ap.add_argument("--name", default="sentiment")
    ap.add_argument("--ngram-max", type=int, default=2)
    ap.add_argument("--C", type=float, default=4.0)
    ap.add_argument("--threshold", type=float, default=0.65)
    args = ap.parse_args()

    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    texts, labels = load_corpus()
    X_tr, X_tmp, y_tr, y_tmp = train_test_split(
        texts, labels, test_size=0.40, stratify=labels, random_state=0)
    X_val, X_te, y_val, y_te = train_test_split(
        X_tmp, y_tmp, test_size=0.50, stratify=y_tmp, random_state=0)
    print("rows: train %d  val %d  test %d" % (len(y_tr), len(y_val), len(y_te)))

    dummy = DummyClassifier(strategy="most_frequent").fit(X_tr, y_tr)
    print("baseline accuracy on val: %.4f" % dummy.score(X_val, y_val))

    pipe = build_model(ngram_max=args.ngram_max, C=args.C)
    pipe.fit(X_tr, y_tr)

    val_prob = pipe.predict_proba(X_val)[:, 1]
    val_pred = (val_prob >= args.threshold).astype(int)
    print("val  accuracy at threshold %.2f: %.4f"
          % (args.threshold, accuracy_score(y_val, val_pred)))

    te_prob = pipe.predict_proba(X_te)[:, 1]
    te_pred = (te_prob >= args.threshold).astype(int)
    acc = accuracy_score(y_te, te_pred)
    f1 = f1_score(y_te, te_pred, zero_division=0)
    print("test n=%d  accuracy=%.4f  f1(pos)=%.4f" % (len(y_te), acc, f1))

    tag = "%s_v%s" % (args.name, args.version)
    joblib.dump(pipe, ARTIFACTS / (tag + ".joblib"))

    meta = {
        "version": tag,
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "task": "binary sentiment of short English reviews",
        "classes": CLASSES,
        "threshold": args.threshold,
        "input_field": INPUT_FIELD,
        "n_train": len(y_tr),
        "n_val": len(y_val),
        "n_test": len(y_te),
        "test_accuracy": round(float(acc), 4),
        "test_f1_positive": round(float(f1), 4),
        "ngram_max": args.ngram_max,
        "C": args.C,
        "sklearn_version": sklearn.__version__,
        "python_version": platform.python_version(),
    }
    with open(ARTIFACTS / (tag + ".metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")
    with open(ARTIFACTS / "LATEST", "w") as f:
        f.write(tag + "\n")

    size_kb = (ARTIFACTS / (tag + ".joblib")).stat().st_size / 1024
    print("wrote %s.joblib (%.0f KB) + metadata; LATEST -> %s" % (tag, size_kb, tag))


if __name__ == "__main__":
    main()
```

**Run it. This is the real output, under 2 seconds:**

```text
rows: train 48  val 16  test 16
baseline accuracy on val: 0.5000
val  accuracy at threshold 0.65: 0.7500
test n=16  accuracy=0.8125  f1(pos)=0.7692
wrote sentiment_v1.joblib (10 KB) + metadata; LATEST -> sentiment_v1
```

**`serve/predictor.py`:**

```python
"""predictor.py — the ONE place in this project where a prediction happens."""
import json
import time
from pathlib import Path

import joblib

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "model" / "artifacts"


def resolve_version(version=None):
    """None or 'latest' -> whatever the LATEST file says. Otherwise the name given."""
    if version is not None and version != "latest":
        return version
    pointer = ARTIFACTS / "LATEST"
    if not pointer.exists():
        raise FileNotFoundError(
            "No LATEST file at %s. Run: python3 model/train.py --version 1" % pointer)
    return pointer.read_text().strip()


class Predictor:
    """Loads one artifact ONCE, then answers questions about it."""

    def __init__(self, version=None, threshold=None):
        self.version = resolve_version(version)
        art = ARTIFACTS / (self.version + ".joblib")
        met = ARTIFACTS / (self.version + ".metadata.json")
        if not art.exists():
            raise FileNotFoundError("No artifact at %s" % art)

        t0 = time.perf_counter()
        self.pipeline = joblib.load(art)                 # the cold-start cost
        self.load_ms = (time.perf_counter() - t0) * 1000

        with open(met) as f:
            self.meta = json.load(f)
        self.classes = self.meta["classes"]
        self.input_field = self.meta["input_field"]
        if threshold is None:
            self.threshold = float(self.meta["threshold"])
        else:
            self.threshold = float(threshold)

    def predict_one(self, text):
        """One string in, one dictionary out. This dictionary IS the contract."""
        t0 = time.perf_counter()
        prob = float(self.pipeline.predict_proba([text])[0, 1])
        latency_ms = (time.perf_counter() - t0) * 1000    # per-request cost only
        if prob >= self.threshold:
            label = self.classes[1]
        else:
            label = self.classes[0]
        return {
            "model_version": self.version,
            "input": text,
            "label": label,
            "probability": round(prob, 4),
            "threshold": self.threshold,
            "latency_ms": round(latency_ms, 2),
        }
```

**`serve/predict.py`:**

```python
"""predict.py — the command-line tool. Zero training code."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from predictor import Predictor


def main():
    ap = argparse.ArgumentParser(description="One sentiment prediction for one review.")
    ap.add_argument("text", help="the review to score, in quotes")
    ap.add_argument("--version", default=None, help="artifact name, or 'latest'")
    ap.add_argument("--threshold", type=float, default=None)
    ap.add_argument("--json", action="store_true", help="print the whole contract as JSON")
    args = ap.parse_args()

    p = Predictor(version=args.version, threshold=args.threshold)
    out = p.predict_one(args.text)

    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print("%-8s p=%.4f  (threshold %.2f, model %s, %.2f ms, loaded in %.0f ms)"
              % (out["label"], out["probability"], out["threshold"],
                 out["model_version"], out["latency_ms"], p.load_ms))


if __name__ == "__main__":
    main()
```

**Four commands, and the real output of each:**

```bash
$ python3 serve/predict.py "the pizza was hot and delicious"
positive p=0.7450  (threshold 0.65, model sentiment_v1, 0.38 ms, loaded in 650 ms)

$ python3 serve/predict.py "cold food and a rude driver"
negative p=0.2110  (threshold 0.65, model sentiment_v1, 0.40 ms, loaded in 729 ms)

$ python3 serve/predict.py --json "the pizza was not delicious"
{
  "model_version": "sentiment_v1",
  "input": "the pizza was not delicious",
  "label": "negative",
  "probability": 0.5462,
  "threshold": 0.65,
  "latency_ms": 0.43
}

$ grep -rnE "\.fit\(|train_test_split|DummyClassifier|optimizer" serve/
$                                    ← nothing. That empty line IS the evidence.
```

**And `tests.py`:**

```python
"""tests.py — three golden tests. Run: python3 tests.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "serve"))
from predictor import Predictor

GOLDEN = [
    ("delicious fresh pizza and kind friendly staff", "positive"),
    ("cold food and a rude driver",                   "negative"),
    ("stale bread and awful coffee",                  "negative"),
]

p = Predictor()
failures = 0
for text, expected in GOLDEN:
    out = p.predict_one(text)
    ok = out["label"] == expected
    if not ok:
        failures = failures + 1
    print("%-4s expected=%-8s got=%-8s p=%.4f  <<%s>>"
          % ("PASS" if ok else "FAIL", expected, out["label"], out["probability"], text))

print()
print("%d/%d passed  (model %s, threshold %.2f)"
      % (len(GOLDEN) - failures, len(GOLDEN), p.version, p.threshold))
sys.exit(1 if failures else 0)
```

```text
PASS expected=positive got=positive p=0.7661  <<delicious fresh pizza and kind friendly staff>>
PASS expected=negative got=negative p=0.2110  <<cold food and a rude driver>>
PASS expected=negative got=negative p=0.2380  <<stale bread and awful coffee>>

3/3 passed  (model sentiment_v1, threshold 0.65)
```

- [ ] **Finally, run the timing script**, because §4's numbers are the most interesting thing you will say today:

```python
import time
t0 = time.perf_counter(); import joblib; t1 = time.perf_counter()
print("import joblib            : %6.1f ms" % ((t1 - t0) * 1000))
t0 = time.perf_counter(); pipe = joblib.load("model/artifacts/sentiment_v1.joblib"); t1 = time.perf_counter()
print("FIRST joblib.load        : %6.1f ms" % ((t1 - t0) * 1000))
t0 = time.perf_counter(); pipe2 = joblib.load("model/artifacts/sentiment_v1.joblib"); t1 = time.perf_counter()
print("SECOND joblib.load       : %6.1f ms" % ((t1 - t0) * 1000))
t0 = time.perf_counter(); pipe.predict_proba(["cold food and a rude driver"]); t1 = time.perf_counter()
print("FIRST predict_proba      : %6.1f ms" % ((t1 - t0) * 1000))
t0 = time.perf_counter(); pipe.predict_proba(["cold food and a rude driver"]); t1 = time.perf_counter()
print("SECOND predict_proba     : %6.3f ms" % ((t1 - t0) * 1000))
```

```text
import joblib            :   92.2 ms
FIRST joblib.load        :  659.3 ms
SECOND joblib.load       :    0.4 ms
FIRST predict_proba      :    0.4 ms
SECOND predict_proba     :  0.173 ms
```

### 10 minutes on the day

- [ ] CONTRACT sheets face-down on every desk. **Face-down. They do not turn them over until you say.**
- [ ] THE SIX BOXES wall sheet up, blank.
- [ ] Editor and terminal open on the shared screen, in the `ship-it/` folder, with `model/artifacts/` **deleted** — you are going to create it live.
- [ ] Your own `sentiment_v1` kept safely in a copy elsewhere, so a failed live run cannot cost you the demo.
- [ ] Bug Log out.
- [ ] A timer. The 25 silent minutes are timed, out loud, and you announce the halfway point.

### Fallback if the laptops fail

**This week survives a total power cut better than any other week of the year, because the deliverable is a piece of paper.**

1. **The contract, unchanged.** Twenty-five silent minutes, the cross-examination, the whole activity. Objective 1 — the hardest and most important one — needs no electricity at all.
2. **Box 5's arithmetic on paper.** Print the nine-row cost table from the Answer Key (page 34.2) and do the sweep by hand. `10 × 1 + 1 × 0 = 10` against `10 × 0 + 1 × 4 = 4`.
3. **The cold-start addition on paper.** `92.2 + 659.3 + 0.4 = 751.9`, then `751.9 ÷ 0.4 ≈ 1,880`. A real and startling number, done with a pencil.
4. **The three golden tests chosen on paper**, from the probability list in the Answer Key, with the distance from the threshold written beside each. That is objective 4's *thinking*, without objective 4's typing.
5. **Objectives 2 and 3 are the casualty.** Say so plainly: *"the one thing we cannot do on paper is freeze the file and open a cold terminal. That is your homework, and next week's lesson needs it done."*

| If this fails | Do this instead |
|---|---|
| A student has no Week 33 model at all | Hand them the reference `reviews.py` and `model_def.py` on a USB stick. **The point today is the contract and the artifact, not the corpus.** Note it in the Bug Log and fix the corpus at lunchtime. |
| `ModuleNotFoundError: No module named 'model_def'` | They ran `python3 train.py` from inside `model/`, or from the wrong folder. The `sys.path.insert(...)` line fixes it — check it is there and above the import. |
| `FileNotFoundError: ... 'artifacts/sentiment_v1.metadata.json'` | The `mkdir` line is missing or below the `open`. **Python makes files, never folders.** |
| Somebody's `predict.py` imports `train` | Rule 1. Show the grep. **Do not fix it for them — run the grep on the shared screen and let the room see a line printed where a blank should be.** |
| The whole class finishes the artifact in 8 minutes | Send them to page 34.7: train a `v2` with one deliberate change, and **write down why they reject it**. A written rejection scores higher than an unjustified upgrade. |
| Somebody starts building the HTTP service | Stop them warmly. *"That is next week and it is the hardest milestone. Today you make the thing it will serve."* |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — The Stranger At The Door | 7 | 7 | You play the stranger. Nobody can answer you. |
| 🧠 Concept & Maths — Six Boxes Before Any Code | 18 | 25 | The six boxes, and box 5's cost sweep worked on the board |
| 💻 Live-Code Together — freeze it, then serve it cold | 18 | 43 | `train.py` → three files → `predict.py`. **Two deliberate mistakes.** |
| 🎲 Their Turn — Contract Writing, In Silence | 20 | 63 | 25 minutes of writing compressed to 12, then cross-examination |
| 🔑 Wrap & Assign | 7 | 70 | Three golden tests, three checks, the homework command |

---

### 🪝 Hook — The Stranger At The Door (7 minutes)

**Do this:** Nothing on the screen. Stand at the front holding a piece of paper. Say you are somebody they have never met.

**Say this:**

> "I run a small forum. About four hundred comments a day. I heard you built something that can tell a nasty comment from a nice one, and I would like to use it, please.
>
> I am not going to open a notebook. I am not going to run cells in order. I do not know what a vectorizer is and I am not going to learn. **I have a terminal and I have four hundred comments. What do I type?**"

**Do this:** Wait. Let it be uncomfortable for a full ten seconds. Somebody will say "you'd run my notebook" or "I'd send you the file".

**Say this:**

> "Right. Say I do that. Now it is three weeks later, and somebody messages me: *it said my comment was positive and it obviously isn't.*
>
> I come back to you. **Which version of your model answered them?**"

*Nobody can answer. There is only one version and it has no name.*

> "**What exactly was sent in?**"

*Nobody knows. Nothing was written down.*

> "**What probability came back, and what did you compare it to?**"

*Silence, or "0.5". Take the 0.5 — you are coming back to it in eleven minutes.*

> "**And how long did it take?**"

*Nobody has measured it.*

**Say this:**

> "Four questions. Four 'I don't know's. And notice: **none of those four questions is about accuracy.** Your model might be excellent. It is still unusable, and it is unusable for reasons that have nothing to do with machine learning.
>
> There is a name for the gap between 'my model works in my notebook' and 'a stranger can use it': people call it **the last mile**, and it is where most machine learning projects quietly die. Nobody teaches the last mile to a fourteen-year-old. You are going to build it, in three weeks, and you are starting today with a piece of paper."

**Ask this:** "Before you write any code at all — what is the very first thing you'd have to decide?"

*Hoped-for: "what it takes in and gives out." Good — that is boxes 2 and 3.*
*If they say "which model to use": "you already chose. That was Week 33. Today is about the promise, not the model."*
*If they say "how accurate it is": "you measured that in Week 33 and it's in your workbook. I asked you four questions just now and accuracy wasn't one of them. Why do you think that is?"*

---

### 🧠 Concept & Maths — Six Boxes Before Any Code (18 minutes)

**Do this:** Go to the blank THE SIX BOXES sheet. Draw six boxes, two rows of three, and number them. Fill them in as you talk — **you are modelling the thing they are about to do.**

**Say this:**

> "Six boxes. This is a **prediction contract**, and it is a promise you write down before you write any serving code. Every one of the six is a decision. Every one of the six will be quoted back at you."

**Do this:** Write box 1's heading: `WHAT ONE PREDICTION IS ABOUT`.

**Ask this:** "Week 1. One row of your table is one what?"

*One review.*

> "Good. So write: **one prediction is about one review, written by one person, at one time.**"

**Ask this:** "Why not 'one prediction is about one person'?"

*Take answers. Steer to: because then two reviews by the same person would have to agree.*

> "**Exactly.** The moment you say a prediction is about a person, you have promised that your model is consistent about people, and it is not — it has never seen a person, it has only seen strings. Box 1 is where you avoid promising something you cannot do."

**Do this:** Boxes 2 and 3. Write them out in full:

```
2  INPUT      text        a non-empty string, limit 100,000 bytes
3  OUTPUT     label  probability  threshold  model_version  latency_ms
```

**Say this:**

> "Five fields out, and here is the rule that makes them worth writing down: **the thing the tool prints, the thing the service returns and the thing the log records are the same five fields.** One list. If your tool says `POSITIVE` and your log says `1`, you have two vocabularies and you will not be able to join them up when it matters."

**Do this:** Box 4. Write the heading `THE TWO ERRORS, PRICED` and then wait.

**Ask this:** "In the language of the forum — not in the language of a confusion matrix — what is a false positive?"

*Hoped-for: a nasty comment that gets marked positive.*

> "And what actually happens to it?"

*Nobody reads it.*

**Ask this:** "And a false negative?"

*A nice comment gets marked negative, and a moderator reads it for nothing.*

**Say this:**

> "Now put numbers on them. Not real money — **relative prices**, which is all you ever need. If a moderator's ten seconds is worth **1**, what is a nasty comment nobody reads worth?"

*Take answers. Anything from 5 to 100. Land on 10 and say why: "we'll use 10, and the honest thing to write next to it is that I chose 10 by judgement, not measurement."*

**Do this:** Box 5, `THE THRESHOLD`. This is the maths of the week, and it is Week 11's arithmetic. Write on the board:

```
cost = 10 x (nasty called positive)  +  1 x (nice called negative)
```

**Say this:**

> "Week 11. Sweep the threshold, count the two kinds of mistake on the **validation** set, and work out what each threshold would have cost. Here are the real counts from the reference model, on its 16 validation rows."

**Do this:** Write the table, reading the numbers out as you go:

```
  t      nasty called positive    nice called negative     cost
0.40             3                        0                30
0.50             1                        0                10
0.55             1                        1                11
0.60             1                        3                13
0.65             0                        4                 4
0.70             0                        4                 4
0.80             0                        7                 7
```

**Ask this:** "Work out the cost at 0.50 out loud with me."

*`10 × 1 + 1 × 0 = 10 + 0 = 10`.*

**Ask this:** "And at 0.65?"

*`10 × 0 + 1 × 4 = 0 + 4 = 4`.*

**Ask this:** "0.65 and 0.70 both cost 4. Which threshold do we ship?"

*0.65. The tie-break rule is: **of the tied thresholds, take the lower one.** Say it out loud and say why: the two make exactly the same mistakes on these 16 rows, so the data cannot separate them, and the lower one flags fewer reviews as negative on the rows we have not seen, which wastes fewer moderator ten-seconds on nice reviews. It also lets more borderline reviews through, so this is a stated convention, not a proven better choice; a team that priced nasty reviews harder could reasonably break the tie the other way.*

> "**0.65, and not 0.5.** And now the uncomfortable part, which is the part I want you to write down."

**Do this:** Write on the board:

```
accuracy at 0.50  =  0.9375
accuracy at 0.65  =  0.7500
```

**Ask this:** "We just chose the threshold that makes accuracy **worse by nearly 19 points**. Are we mad?"

*Let them argue. It is the best ninety seconds of the lesson.*

> "No — and here is why, in one sentence. **Accuracy treats both errors as the same price, and we have just written down that they are not.** We priced a missed nasty comment at ten times a wasted ten seconds. Accuracy cannot see that. The cost sum can.
>
> When you know the costs, **use the costs**. Accuracy is the metric for when you don't."

> **🧑‍🏫 If a student asks:** *"Module 3 had a rule of thumb — the threshold should be the false-positive cost divided by the total, which is `10 ÷ 11 = 0.91`. Why isn't it 0.91?"* **This is the best question in the week and it has an honest answer.** The rule of thumb assumes the probabilities are well calibrated and that there are enough rows for the trade-off to be smooth. Here there are **16 validation rows**, and by `0.65` there are already **zero** expensive errors left to remove — so every further step up buys only cheap errors, and the cost stays at 4 at 0.70 and then climbs, to 7 at 0.80. **When the rule of thumb and the measurement disagree, the measurement wins, and you write down why.** Also: 16 rows means one row is worth 6.25 percentage points. Say that out loud too — and say that at 0.50 the model makes one expensive error, which is a single review, so this whole choice rests on one row.

**Do this:** Box 6, `NEVER USED FOR`. Write two things and cross them out with the big red cross:

```
✗  deciding who gets banned
✗  marking anybody's schoolwork
```

**Say this:**

> "A reasonable person will try both of those. **You are going to tell them not to, in writing, before they ask.** And the sentence that belongs in box 6, which I want in every one of your contracts: *this model outputs a suggestion, not a decision.*"

---

### 💻 Live-Code Together — Freeze It, Then Serve It Cold (18 minutes)

**You never touch their keyboard.** They have `model_def.py`, `reviews.py` and `train.py` already — those were printed and handed out, because retyping the corpus costs eight minutes and teaches nothing. **They type `predictor.py`, `predict.py` and `tests.py` themselves.**

**Step 1 (3 min) — make the artifact.**

```bash
python3 model/train.py --version 1
```

```text
rows: train 48  val 16  test 16
baseline accuracy on val: 0.5000
val  accuracy at threshold 0.65: 0.7500
test n=16  accuracy=0.8125  f1(pos)=0.7692
wrote sentiment_v1.joblib (10 KB) + metadata; LATEST -> sentiment_v1
```

> **Say this:** "Look at line two. **The baseline is 0.5000** — the corpus is 40 positive and 40 negative, so a model that always says the same thing is right half the time. Every number below that line is only meaningful next to it."

**Do this:** List the folder.

```bash
$ ls -l model/artifacts/
-rw-r--r--   13 LATEST
-rw-r--r-- 10228 sentiment_v1.joblib
-rw-r--r--   421 sentiment_v1.metadata.json
```

> **Say this:** "Three files. Ten kilobytes of model, four hundred and twenty-one bytes of paperwork, and thirteen bytes saying which one is live. **The thirteen-byte file is the one that makes a rollback cheap.**"

**Do this:** Print the metadata.

```bash
$ cat model/artifacts/sentiment_v1.metadata.json
{
  "version": "sentiment_v1",
  "created_utc": "2026-09-18T17:47:14Z",
  "task": "binary sentiment of short English reviews",
  "classes": [
    "negative",
    "positive"
  ],
  "threshold": 0.65,
  "input_field": "text",
  "n_train": 48,
  "n_val": 16,
  "n_test": 16,
  "test_accuracy": 0.8125,
  "test_f1_positive": 0.7692,
  "ngram_max": 2,
  "C": 4.0,
  "sklearn_version": "1.7.1",
  "python_version": "3.10.10"
}
```

> **Say this:** "Every one of those was **generated by the script**, not typed by a human, which is why it cannot be wrong. And the last two look like bureaucracy: they are the difference between 'the model broke after I updated my laptop' being a two-minute diagnosis and a two-day one. **Your `created_utc` will differ from mine. It is the one line in this file that is supposed to change.**"

**Step 2 (6 min) — `predictor.py`, typed by them.**

Walk the class through the class line by line. The three lines to stop on:

```python
t0 = time.perf_counter()
self.pipeline = joblib.load(art)                 # the cold-start cost
self.load_ms = (time.perf_counter() - t0) * 1000
```

> **Say this:** "That stopwatch is round the **loading**. Down in `predict_one` there is a second stopwatch round the **prediction**. Two stopwatches, two numbers, and you will never report them as one."

**⚠️ DELIBERATE MISTAKE 1 — the wrong way round.** Type this into `train.py` on the shared screen, in place of the working line, and run it:

```python
with open(ARTIFACTS / (tag + ".metadata.json"), "w") as f:
    json.dump(f, meta)          # <-- wrong way round, on purpose
```

```text
TypeError: Object of type TextIOWrapper is not JSON serializable
```

**Ask this:** "What is a `TextIOWrapper`?"

*Let them guess. Answer: it is Python's name for an open file.*

**Ask this:** "So what is the message actually telling us?"

*"You asked me to turn a file into text, and I can't."*

> **Say this:** "So I have handed it the two things in the wrong order. **`json.dump(thing, file)` — the data first, the file second.** Everybody does this once. Bug Log."

Fix it, re-run, move on.

**Step 3 (6 min) — `predict.py`, and the cold start.**

They type it. Then, on the shared screen, **open a brand-new terminal window** and make a show of it.

```bash
$ python3 serve/predict.py "the pizza was hot and delicious"
positive p=0.7450  (threshold 0.65, model sentiment_v1, 0.38 ms, loaded in 650 ms)
```

> **Say this:** "Brand-new terminal. Nothing pre-loaded. No notebook, no cells, no order to run them in. **One line, and an answer.** That is what the stranger at the door asked for at the start of the lesson."

**⚠️ DELIBERATE MISTAKE 2 — forget the quotes.** Do it on purpose:

```bash
$ python3 serve/predict.py cold food and a rude driver
usage: predict.py [-h] [--version VERSION] [--threshold THRESHOLD] [--json]
                  text
predict.py: error: unrecognized arguments: food and a rude driver
```

**Ask this:** "It took `cold` and refused the rest. Why?"

*Because the shell split the sentence at the spaces, so `argparse` got six separate things and was only expecting one.*

> **Say this:** "The quotes are not decoration; **the quotes are what makes six words into one argument.** And notice `argparse` refused *before* my code ran — it printed a usage line I never wrote. That is the free gift of using a proper argument parser instead of reading `sys.argv` by hand."

**Step 4 (3 min) — the grep, and the two times.**

```bash
$ grep -rnE "\.fit\(|train_test_split|DummyClassifier|optimizer" serve/
$
```

> **Say this:** "Nothing. **That blank line is the evidence for Rule 1**, and it is evidence rather than a promise (strong evidence, not a proof). In your write-up next week you paste the command *and* its empty output."

> **🧑‍🏫 A true story worth telling.** The first time I ran that grep on this project, it printed a line — and the line was **a comment in my own file** that said *"there is no `.fit()` anywhere below this line."* The check was right and my sentence was wrong. **A check that catches your own prose is a check doing its job.** Reword the comment; don't weaken the grep.

Finally, on the board:

```
loaded in 650 ms     ← once, per program start   (COLD START)
        0.38 ms      ← every single prediction   (LATENCY)
```

> **Say this:** "Two numbers. About **1,700 times** apart. Anybody who reports one number has hidden something."

---

### 🎲 Their Turn — Contract Writing, In Silence (20 minutes)

See **🎲 The Activity, In Full** below for the complete instructions. In brief: twelve silent timed minutes filling in the CONTRACT sheet, then eight minutes in which every contract is read aloud and the room cross-examines it on **two questions only**.

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Put the three golden tests on the screen and run them.

```bash
$ python3 tests.py
PASS expected=positive got=positive p=0.7661  <<delicious fresh pizza and kind friendly staff>>
PASS expected=negative got=negative p=0.2110  <<cold food and a rude driver>>
PASS expected=negative got=negative p=0.2380  <<stale bread and awful coffee>>

3/3 passed  (model sentiment_v1, threshold 0.65)
```

**Say this:**

> "Eleven lines, and it is the cheapest test that exists. Three inputs whose answers I have decided must never change without my knowing. Run it after every single retrain. If one flips, either the model genuinely changed or the preparation broke — and I want to find out in five seconds, not from a user."

**Ask this:** "The threshold is 0.65. My three probabilities are 0.7661, 0.2110 and 0.2380. Which of my three tests is the most fragile, and how fragile?"

*0.7661 — and `0.7661 − 0.65 = 0.1161` clear of the line.*

> "Right. **Twelve hundredths clear**, so nothing small can flip it. If I had picked a review at 0.6501 I would have built an alarm that cries wolf every time I sneeze."

**Do this:** Run the three quick checks from **✅ Assessing Understanding**. Then assign.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `FileNotFoundError: No LATEST file at /.../model/artifacts/LATEST. Run: python3 model/train.py --version 1` | "There is no artifact yet." | They ran `predict.py` before `train.py`, or `train.py` failed halfway and never got to the last two lines. | Run the trainer first. **And notice: this is an error message *we wrote*, and it tells you the exact command to type. Every error your own code raises should do that.** |
| `predict.py: error: the following arguments are required: text` | "You didn't give me anything to score." | `python3 serve/predict.py` with nothing after it. | Put a review in quotes after the filename. `argparse` refused before any of your code ran, which is the point of it. |
| `predict.py: error: unrecognized arguments: food and a rude driver` | "You gave me six things and I wanted one." | The quotes are missing, so the shell split the sentence at the spaces. | `python3 serve/predict.py "cold food and a rude driver"`. **Quotes make many words into one argument.** |
| `predict.py: error: argument --threshold: invalid float value: 'abc'` | "That is not a number." | `--threshold abc`. | Give it a number. Notice `argparse` did the type check for you because you wrote `type=float` — that check is worth the one word it cost. |
| `TypeError: Object of type TextIOWrapper is not JSON serializable` | "You asked me to turn an open file into text." | `json.dump(f, meta)` instead of `json.dump(meta, f)`. | Data first, file second. |
| `FileNotFoundError: [Errno 2] No such file or directory: 'artifacts/sentiment_v1.metadata.json'` | "The folder isn't there." | No `mkdir`, or the `mkdir` sits *after* the `open`. | `ARTIFACTS.mkdir(parents=True, exist_ok=True)` **before** anything is written. **Python creates files; it never creates folders.** |
| `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)` | "The first character of that file isn't the start of any JSON value." | `json.load` on a file that isn't JSON — usually the one-line `LATEST` file (plain text, not JSON) or an empty file opened by mistake, or a metadata file that was hand-edited and lost a brace. (Opening the binary `.joblib` with `json.load` fails differently, with `UnicodeDecodeError: ... invalid start byte`.) | Check which path you opened. **`char 0` means it failed on the very first character, which almost always means wrong file, not wrong JSON.** |
| `ValueError: Expected 2D array, got 1D array instead: array=['cold food and a rude driver'].` | "You gave the classifier a bare string." | They saved `pipe.named_steps["logisticregression"]` instead of the whole pipeline, so the vectorizer is gone and the classifier is being handed raw text. | **Dump the whole fitted pipeline, always.** The vectorizer is part of the model, not a step you remember to do first. |
| `RuntimeError: Error(s) in loading state_dict for Sequential: size mismatch for 3.weight: copying a param with shape torch.Size([16, 8, 3, 3]) from checkpoint, the shape in current model is torch.Size([32, 8, 3, 3]).` | **Path B only.** "The saved weights and the architecture you just built are different sizes." | `model_def.py` was edited after the artifact was saved, or the architecture was retyped in `predictor.py` instead of imported. | **One definition, imported by both.** Week 25's question still applies: it names both shapes — which one did you mean? |
| `ModuleNotFoundError: No module named 'model_def'` | "Python can't find that file." | Ran from the wrong folder, or the `sys.path.insert(...)` line is below the import instead of above it. | The insert must come **before** the import. And `Path(__file__).resolve()` is what makes it work from any folder. |
| **No error. `predict.py` prints a label but `loaded in 0 ms`.** | Nothing crashed. The stopwatch measured nothing. | Both `perf_counter()` calls are on the same side of the work, or `load_ms` was computed before `joblib.load`. | Put the work **between** the two readings. A latency of exactly 0 is never real. |
| **No error. Every review comes back `negative`.** | Nothing crashed. The threshold is above every probability. | `--threshold 0.95` left over from an experiment, or the metadata was hand-edited. | Print the threshold next to every answer — which the CLI already does. **Then read your own output.** |

### How to teach debugging without giving the answer

All the old moves stand. This week adds three.

26. **"Which folder are you in?"** Half of this week's errors are a path problem wearing a costume. Make `pwd` the first thing they type, not the fifth.

27. **"Read the error out loud, and stop at the first noun you don't recognise."** `TextIOWrapper`, `state_dict`, `2D array`. Look that one noun up. Most of these messages are perfectly clear once one word is known.

28. **"Does your own error message tell the reader what to type next?"** Point at the `No LATEST file ... Run: python3 model/train.py --version 1` message. **The best debugging lesson this week is that you can write the messages.** Ask anybody whose code raises a bare `FileNotFoundError` to improve it. It takes one line and it is a genuine engineering habit.

And the sentence for this week:

> **"Nothing you are debugging today is about machine learning. Every one of these bugs is about a path, a folder, an argument or an order — and that is exactly why the last mile is where projects die. The hard part was never the model."**

---

## 🎲 The Activity, In Full

### Contract Writing, In Silence

**What it is.** Every student fills in the six boxes for **their own** model, alone, in silence, against a timer. Then every contract is read aloud and the room cross-examines it on **two questions only**.

**Why silence.** Because a contract written in conversation becomes the group's contract, and the point is that this is *your* promise about *your* model. Also because fourteen-year-olds will happily talk for twelve minutes and write for none. **The silence is the mechanism.**

### Setup

- One printed A4 CONTRACT sheet per student, six empty boxes, face-down until you say.
- Workbook page 34.1 is the same six boxes, for the final tidy copy at home.
- The wall sheet with **your** worked example still on it. **Leave it up.** They are allowed to copy the *shape*, not the content.
- A visible timer.
- Page 34.2 — the cost table — beside them, because box 5 needs arithmetic.

### Part 1 — the silent write (12 minutes)

**Say this:**

> "Turn them over. Twelve minutes, no talking, no laptops, pens only. Six boxes. If you finish a box early, go back and make box 4 more specific.
>
> Two rules. **Box 5 must contain a sum**, not a number on its own. And **box 6 must name two things somebody would actually try** — not 'anything illegal'. Something tempting."

**Do this:** Announce the halfway point out loud at six minutes. At nine minutes say *"three minutes — if box 4 has no numbers in it, that is where they go."* Walk the room and say nothing; point at empty boxes.

**What you will see, and what to do:**

| What you see | What to do |
|---|---|
| Box 1 says "one prediction is about sentiment" | Point at it and say one word: *"noun."* |
| Box 4 says "a false positive is when it's wrong" | Point and say: *"in the language of the forum. What happens to that comment?"* |
| Box 5 says "0.5" | Point at page 34.2 and say nothing. |
| Box 6 says "anything illegal" | *"Name something a reasonable person would actually try on Tuesday."* |
| A blank sheet at minute six | Sit down beside them and ask box 1 out loud. Write their answer for them, once, then hand the pen back. |

### Part 2 — the cross-examination (8 minutes)

**Say this:**

> "Pens down. Now everybody reads their contract out, and the room may ask **two questions and only two**. Here they are, on the board:
>
> **1. What is one prediction about?**
> **2. What must this never be used for?**
>
> You may not ask about accuracy. You may not ask what model it is. Two questions, and they are the two the stranger at the door would ask."

**Do this:** Go round fast — about forty seconds each. **You ask the two questions for the first student, then hand the asking to the room.** Keep it warm; this is not a trial. When a student cannot answer question 1 with a noun, do not supply it — ask *"what is one row of your table?"* and wait.

**Do this:** As each one passes, write their box 1 noun on the wall sheet in a list. By the end you will have a column of nouns: `review · comment · digit image · photo`. **That column is the best thing on the wall all week**, because it shows the room that the unit of prediction is a choice that differs between projects.

### What "finished" looks like

Six boxes with writing in all six · box 5 containing a sum with a `×` and an `=` in it · box 6 naming two specific tempting misuses · and the student able to answer both cross-examination questions without looking down at the paper.

**A contract with one weak box and a student who can defend the other five is a pass.** A beautiful contract whose author cannot say what one prediction is about is not.

### Variation — easier

Give them a **half-filled** sheet: boxes 1, 2 and 3 already completed for the reference model, and only boxes 4, 5 and 6 to write. Then hand them the cost table with the two cost sums already worked and ask only *which threshold ships, and why*. **Boxes 4 and 6 are the ones worth the struggle; 1, 2 and 3 can be scaffolded away without losing the lesson.**

### Variation — harder

Two extra demands.

1. **A second contract for a model they did not build** — the digits CNN if they shipped sentiment, or vice versa. Box 1 changes from "one review" to "one 8×8 picture of one digit"; box 3 gains ten classes and loses the threshold entirely, because `argmax` has no dial. **Noticing that box 5 is empty for a ten-class model is a level-5 observation** and it should be praised loudly.
2. **A golden test that freezes a known failure.** Find an input their model gets *wrong*, assert the wrong answer, and write one sentence explaining why that is a sensible thing to do. The reference answer: *"not boring for a single minute" comes back negative at p = 0.4887; I assert negative, so that the day it changes I find out, and that is the day I can claim I fixed negation.*

---

## ❓ Questions Students Ask This Week

**"Why is the threshold 0.65 and not 0.5? Isn't 0.5 the natural middle?"**

0.5 is the natural middle of a *number line*. It is not the natural middle of a *decision*. Box 4 says a nasty comment slipping through costs ten times a nice comment being read for nothing — so the sensible place to cut is not the middle, it is wherever the total cost is smallest. On our 16 validation rows that is 0.65 (tied with 0.70, and we take the lower of the tied thresholds): `10 × 0 + 1 × 4 = 4`, against `10 × 1 + 1 × 0 = 10` at 0.50. **0.5 is what you ship when you have not decided. 0.65 is what you ship when you have.** And be honest that 0.50 has the best accuracy (0.9375) — it is simply the one that lets a nasty review through.

**"Module 3's rule of thumb gives 10 ÷ 11 = 0.91. Why didn't we use that?"**

Because we measured, and the measurement disagreed. The rule of thumb assumes well-calibrated probabilities and enough rows for the trade-off to be smooth; we have 16 rows, and by 0.65 there are already zero expensive errors left to remove, so every further step up buys only cheap ones, and the cost stays at 4 at 0.70 and then climbs back to 7 at 0.80. **When a rule of thumb and a measurement disagree, the measurement wins and you write down why.** And say the other honest thing: 16 rows means one row is worth 6.25 points, so this threshold is a decision made on very little evidence, and that sentence belongs in the model card.

**"Why does accuracy get worse when we pick the 'better' threshold? That feels like cheating."**

It feels like cheating because accuracy has been the score all year. But accuracy silently assumes the two mistakes cost the same, and we spent ten minutes writing down that they don't. **Once you have priced the errors, accuracy is the wrong instrument — it is measuring something you have said you don't care about equally.** Report both numbers, say which one you optimised, and say why. That is not cheating; that is the opposite.

**"Isn't all this just admin? Where's the machine learning?"**

Honest answer: yes, it is admin, and the admin is what decides whether anybody ever uses the thing you built. Nothing in today's lesson would help you win a competition. Everything in today's lesson is what separates a model that exists from a model that is used. And notice which box took the longest to write — box 4, the prices — because that is the only box with a judgement in it that a machine cannot make for you.

**"My model is 10 kilobytes. Does versioning really matter for something that small?"**

It matters *more*, because a 10-kilobyte file is a file you will overwrite without thinking. The whole cost of versioning is six characters in a filename. The cost of not versioning is discovering that the model that was working is gone and you changed four things since. **Six characters.**

**"Everyone online says loading the model per request makes it 200 times slower. Our measurement says about 3 times. Who's wrong?"**

**Nobody fully agrees on this, and here is why.** Both numbers are real, on different models. What people are usually measuring is the **cold start** — the first load in a fresh process, which on our artifact is 659 ms and is almost entirely Python importing scikit-learn, not reading 10 kilobytes off a disk. The *second* load in the same process takes 0.4 ms. So in a warm service, reloading per request costs about 0.4 ms against a 0.17 ms prediction — two or three times, not two hundred. On the Path B torch model the same experiment gives 7.3 times. On a 100-megabyte model it really is hundreds of times. **So the rule "load once at startup" is right, the reason usually given for it is wrong, and the only honest thing you can say in your demo is your own measured number.** A student who says *"three times on mine, and here's why it would be bigger on a bigger model"* is doing better engineering than one who quotes 200.

**"Can I use `pytest` instead of writing my own eleven lines?"**

You can, and one day you should. Not this week. `pytest` hides the two things this week is about: that a test is just a comparison plus an exit code, and that the exit code is how one program tells another program it failed. Write the eleven lines once, watch `echo $?` print `1` when you break it on purpose, and then go and use a framework knowing exactly what it does for you.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| **The class starts coding in the first ten minutes and the contract never gets written.** | Typing feels like progress and writing feels like homework. | **Laptops closed until minute 25.** Say it at the door. The contract sheet is face-down on the desk precisely so nothing else can start. |
| **Everybody's box 5 says 0.5.** | They have not connected box 4 to box 5, because at 0.5 nothing has to be decided. | Stop the room. Do `10 × 1 + 1 × 0 = 10` against `10 × 0 + 1 × 4 = 4` on the board with the whole class saying it out loud. **Box 5 is not a number; it is a comparison.** |
| **Box 6 says "anything illegal or unethical".** | It sounds responsible and costs nothing. | *"Name something a reasonable person would try on Tuesday."* Push until you get "deciding who gets banned" or "marking homework". **Content-free box 6 is the commonest failure of real model cards, not just school ones.** |
| **Somebody saves `pipe.named_steps["logisticregression"]` because it is "the model".** | It is the model. It is not the artifact. | Let them hit `ValueError: Expected 2D array, got 1D array instead`. Then ask what happened to the vectorizer. **Week 3's lesson, relearned the fast way.** |
| **The cold-start demo is run in the terminal they have been working in all lesson.** | It is the terminal that is already open. | Open a new window with a flourish. **The only cold start worth demonstrating is one that starts cold.** Make it theatre; they will remember it. |
| **A student's artifact works only when run from inside `serve/`.** | A relative path somewhere — `joblib.load("artifacts/x.joblib")`. | `Path(__file__).resolve().parent` and build from there. Then `cd /` and run it again to prove it. |
| **Twenty minutes go on making the CLI output pretty.** | Formatting is fun and contracts are not. | Cap it: *"one line, five facts, move on."* The rubric next week weights the log and the card far above the formatting, deliberately. |
| **Somebody builds the HTTP service today because they read ahead.** | Enthusiasm. | Praise it and park it. *"That is next week's hardest milestone. If you build it today you will build it without a contract, and you will rebuild it."* |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** Path B entirely · the `--json` flag · `--version` and `--threshold` overrides · the third golden test · page 34.7.

**Give them the copy-this-exactly scaffold.** Hand them `predictor.py` complete and printed. They type only `predict.py`, which is nineteen lines and includes three of the week's four new constructs. **Typing `predict.py` is the whole of objective 3.**

**The version of the maths that skips the algebra.** Box 5 without any sweeping. Two rows on paper, nothing else:

```
if I cut at 0.50 :  1 nasty slips through, 0 nice ones wasted    10 + 0  = 10
if I cut at 0.65 :  0 nasty slip through, 4 nice ones wasted     0 + 4  =  4
                                                          4 is less than 10
```

That is two additions and one comparison, and it is the entire idea. **No sweep, no curve, no rule of thumb.** They can still answer *"where did your threshold come from?"* with a sum, which is the objective.

**And the one thing not to cut:** boxes 1, 4 and 6. A student who leaves today able to say *"one prediction is about one review; a nasty one slipping through costs about ten times a nice one being read for nothing; and this must never decide who gets banned"* has had a good lesson, whatever their code does.

### If the student is flying

1. **A `v2` they reject in writing.** Retrain with `--C 1.0 --version 2`, compare on the *same* test set at the *same* threshold, and write one paragraph rejecting it. The reference numbers: at the shipped threshold of 0.65, `C = 4.0` gives test **0.8125** and `C = 1.0` gives test **0.5000** with F1 falling from **0.7692** to **0.0000** — and yet at a 0.50 cut both score 1.0000. **The reason is that a smaller `C` squashes every probability toward 0.5, so the threshold you chose for v1 no longer fits v2's scale.** A written rejection is stronger work than an unjustified upgrade and they should be told so.
2. **The golden test that freezes a failure.** As in the harder variation above.
3. **Measure the reload cost themselves** and settle the "200×" question with their own numbers. Two `perf_counter()` pairs, one loop. Then have them write the sentence they would say in the demo. **This is the best extension in the week because it ends in a true sentence nobody told them.**
4. **A contract for a model with no threshold.** The digits CNN. Box 5 is empty because `argmax` has no dial. Ask them what replaces it — the answer is *a confidence floor*, and inventing that from scratch is genuinely good thinking.

### If the student won't engage today

The contract is a piece of paper and this is the week that is easiest to do on paper — use that.

Sit beside them and ask box 1 out loud: *"one prediction is about one what?"* Write down whatever they say. Then box 6: *"name one thing this should never be used for."* Almost everybody has an opinion about box 6, because box 6 is about people rather than code. **Start there and work backwards.** A student who fills in boxes 1 and 6 and nothing else has still produced the two boxes the cross-examination asks about, and they can take part in the activity like everybody else.

If they will not write, let them be the **cross-examiner**: they hold the board with the two questions and ask them of every other student in turn. It is a real job, it requires them to have understood both questions, and it is the only role in the room where saying nothing is not an option.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the unit of prediction (spoken, 45 seconds)**

> "Finish this sentence about your own model: **one prediction is about exactly one …**"

*Good answer:* "one review, written by one person, at one time" — or "one 8×8 picture of one handwritten digit".

**What to catch:** any abstract noun. "One sentiment", "one classification", "one input". Push once: *"what is one row of your table?"* **Full marks needs a countable thing you could point at.**

**Check 2 — where the threshold came from (spoken, 60 seconds)**

> "Your threshold is 0.65. **Where did 0.65 come from?**"

*Good answer:* "From the cost sweep on the validation set. A nasty comment slipping through costs about ten times a nice one being read for nothing, so at 0.50 the cost was `10 × 1 + 1 × 0 = 10` and at 0.65 it was `10 × 0 + 1 × 4 = 4`. 0.65 is cheaper (0.70 ties it, and I take the lower of the two), so 0.65 ships — even though it costs me about 19 points of accuracy (0.9375 down to 0.7500), because accuracy prices both errors the same and I don't."

**What to catch:** "it worked better". Push once: *"better at what, and what was the sum?"* **Full marks needs a multiplication and a comparison.**

**Check 3 — the two times (spoken, 45 seconds)**

> "Your tool printed **650 ms** and **0.38 ms**. What are those two numbers, and why can't you report one of them?"

*Good answer:* "650 is the cold start — loading the model, paid once when the program starts, and most of it is Python importing scikit-learn rather than reading the file. 0.38 is the latency — one prediction, paid every time. Reporting one number hides whichever cost the person asking actually cares about."

**What to catch:** "it took 650 milliseconds". **Any answer with one number in it is not yet a pass**, and this is the check that predicts whether next week's p95 will mean anything.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Box 1 has an abstract noun in it. Box 5 says 0.5 with no arithmetic. Box 6 says "anything unethical". `predict.py` only runs from one folder, or imports something from `train.py`. |
| **2 — Emerging** | All six boxes have writing in them, and box 4 names both errors in the language of the application. The artifact exists with a version in its filename. `predict.py` runs with help. Reports one latency number. |
| **3 — Secure** | Six boxes, with a cost sum in box 5 and two specific tempting misuses in box 6. Three files in `artifacts/` including `LATEST`. `predict.py` runs from a brand-new terminal in any folder, the grep is empty, and they report **two** latency numbers with the right names. Three golden tests pass. **This is the target.** |
| **4 — Strong** | Says out loud that the chosen threshold costs accuracy and why that is the right trade. Chose the three golden inputs by their distance from the threshold and can quote the closest gap. Wrote their own `FileNotFoundError` message so it names the command to run next. Noticed that most of the 659 ms is importing, not reading. |
| **5 — Exceptional** | Trained a v2 and **rejected it in writing** on the same test set. Froze a known failure as a fourth golden test and justified it. Measured the reload cost themselves and can say why the internet's "200×" does not apply to a 10 KB artifact. Spotted that a ten-class model has no box 5 and proposed a confidence floor instead. |

---

## 📤 Homework to Assign

**Say this:**

> "About an hour. Four pages, and the last one is one line long and the hardest.
>
> **First, page 34.1 — the contract, tidied up.** Same six boxes, neat, in ink, with the two things the room made you change. **Box 5 must contain a sum.**
>
> **Second, page 34.4 — the frozen artifact.** Run the trainer, then list the folder and copy out the three filenames **with their byte sizes**. Then open the metadata file and copy out four fields: the version, the threshold, the test accuracy and the two library versions. **Generated, not typed** — if you typed any of it, you have missed the point of the page.
>
> **Third, page 34.5 — your three golden tests, and why those three.** For each one: the input, the frozen answer, the probability, and **how far it sits from your threshold**. Then one sentence: which of the three is the most fragile, and what its flipping would mean.
>
> **Fourth, page 34.6, and this is the one I mark hardest. One line.** Write out the **exact command a stranger would type** to get a prediction out of your project, starting from a terminal in your project folder. Then — and this is the part people skip — **open a brand-new terminal, paste your own line, and check it works.** If it doesn't, the line is wrong, not the terminal.
>
> Page 34.7 is a stretch: train a `v2`, compare it on the same test set, and **reject it in writing**. Rejecting is harder than upgrading and it scores higher."

**Workbook pages:** 34.1, 34.2, 34.3 in class · **34.1 (tidy), 34.4, 34.5, 34.6** at home · 34.7 optional.

**Expected time:** 15 min tidying the contract · 15 min on the artifact page · 20 min on the golden tests · 10 min on the one-line command, honestly tested · **about 60 minutes**, plus 25 more for the stretch.

> **🧑‍🏫 What to look for when you mark it:** four things. **One — is there a sum in box 5?** A number alone is not an answer to "where did the threshold come from". **Two — were the metadata fields copied from a file, or invented?** The tell is `created_utc`: a real one has a plausible date and time on it, an invented one is suspiciously round. **Three — does page 34.5 give a distance from the threshold for each golden test?** A student who picked three inputs at 0.63, 0.65 and 0.67 has built an alarm that will cry wolf, and saying so to them is worth more than a tick. **Four — did page 34.6's command actually get tested in a fresh terminal?** Ask them. The commonest failure is a command that only works from one folder, and it is invisible until somebody else tries it. **Next week's entire lesson assumes their artifact loads cold. Mark this page first, tonight, so you know on Monday who needs ten minutes of help before the bell.**

---

## 🔑 Answer Key

Every question restated, so you can mark from this page alone.

### The reference corpus — `model/reviews.py`

`model/reviews.py` is **data and one function, and nothing else** — no sklearn, no file reading, no training. It holds two lists of reviews, the twelve traps, and `load_corpus()`, which is the only thing `train.py` and `subgroup_report.py` import from it.

The 80 reviews are the Week 33 corpus: 40 positive and 40 negative, written so that the strongly-signed words repeat (`delicious`, `hot`, `fresh`, `kind`, `wonderful`, `great`, `excellent`, `brilliant` against `cold`, `soggy`, `rude`, `terrible`, `boring`, `stale`, `awful`, `dreadful`), which is what makes 48 training rows enough to learn anything. So **`POS_40` and `NEG_40` below are the same two lists as Week 33's `reviews80.py`**, reprinted here so this page is complete on its own. **Plus 12 negation traps, held out on purpose**, which are used in Week 35 and are not for training:

```python
"""reviews.py - DATA ONLY. The 80 typed reviews, the 12 traps, and one function.

POS_40 and NEG_40 are the two forty-review lists printed in full in Week 33
(`reviews80.py`). Copy them across unchanged; nothing else in this file reads a
file, imports sklearn, or trains anything.
"""
POS_40 = [
    "the pizza arrived hot and the base was perfect",
    "quick delivery and a friendly driver",
    "delicious food and a generous portion",
    "the salad was fresh and crisp",
    "great value and a lovely warm welcome",
    "excellent service from a polite driver",
    "the chips were hot and crisp",
    "a tasty curry and a generous helping of rice",
    "fresh bread and a delicious dip",
    "the delivery was quick and the food was hot",
    "lovely staff and a perfect order",
    "friendly, polite and on time",
    "the sauce was tasty and the cheese was lovely",
    "generous portions and excellent prices",
    "the burger was hot and the salad was fresh",
    "delicious dessert and a friendly note in the bag",
    "a perfect meal and a quick refund on the drink",
    "great chips, crisp and properly salted",
    "the coffee was hot and the cake was fresh",
    "polite driver and a warm, tasty pizza",
    "excellent noodles with fresh vegetables",
    "a lovely evening and a delicious meal",
    "quick, friendly and generous",
    "the fish was fresh and the batter was crisp",
    "perfect timing and a hot bag",
    "tasty wrap, generous salad and a great price",
    "the naan was warm and lovely",
    "friendly manager and a quick, fair refund",
    "a delicious pizza, hot and perfect",
    "excellent, fresh food and a polite driver",
    # --- the ten you typed this week ---
    "helpful driver and a hot, tasty pizza",
    "the bread was warm and the dip was delicious",
    "generous portions and a friendly welcome",
    "quick service and an excellent, fresh garden salad",
    "a lovely handwritten note and a perfect, crisp base",
    "great coffee and a moist, tasty cake",
    "the curry was hot and the rice was fluffy",
    "polite staff and a generous, speedy refund",
    "fresh vegetables and a delicious, rich sauce",
    "quick, warm and lovely throughout",
]

NEG_40 = [
    "the pizza arrived cold and the base was soggy",
    "slow delivery and a rude driver",
    "awful food and a mean portion",
    "the salad was stale and limp",
    "poor value and a cold, rude welcome",
    "terrible service from a rude driver",
    "the chips were cold and soggy",
    "an awful curry and a mean helping of rice",
    "stale bread and a greasy dip",
    "the delivery was slow and the food was cold",
    "rude staff and a wrong order",
    "rude, slow and very late",
    "the sauce was bitter and the cheese was greasy",
    "mean portions and terrible prices",
    "the burger was cold and the salad was limp",
    "awful dessert and a rude note in the bag",
    "a wrong meal and a slow refund on the drink",
    "soggy chips, cold and completely unsalted",
    "the coffee was cold and the cake was stale",
    "rude driver and a cold, greasy pizza",
    "terrible noodles with limp vegetables",
    "i would not order from here again",
    "slow, rude and mean",
    "the fish was stale and the batter was soggy",
    "late again and a cold bag",
    "greasy wrap, limp salad and a terrible price",
    "the naan was cold and stale",
    "rude manager and a slow, unfair refund",
    "an awful pizza, cold and soggy",
    "terrible, stale food and a rude driver",
    # --- the ten you typed this week ---
    "the bag was torn and the pizza was stone cold",
    "the bread was stale and the dip was greasy",
    "mean portions and a rude welcome",
    "slow service and an awful, stale salad",
    "a wrong note and a soggy, limp base",
    "poor watery coffee and a dry, bitter cake",
    "the curry was cold and the rice was lumpy",
    "rude staff and a mean, sluggish refund",
    "limp vegetables and a greasy, thin sauce",
    "slow, cold and mean throughout",
]

# The twelve negation traps. These are NEVER trained on. They are the held-out
# evidence for Week 35's subgroup table.
TRAPS = [
    ("the pizza was not delicious",               "negative"),
    ("not fresh and not hot",                     "negative"),
    ("i would not call this wonderful",           "negative"),
    ("hardly the best film of the year",          "negative"),
    ("far from delicious",                        "negative"),
    ("never coming back here",                    "negative"),
    ("not cold at all and the crust was great",   "positive"),
    ("not boring for a single minute",            "positive"),
    ("i cannot fault the service",                "positive"),
    ("nothing rude about the staff",              "positive"),
    ("no complaints whatsoever",                  "positive"),
    ("not the terrible film i expected i loved it", "positive"),
]


def load_corpus():
    """The 80 typed reviews and their labels. 1 = positive, 0 = negative.

    The twelve TRAPS are deliberately NOT in here. They are held out, never
    trained on, and only ever used for measuring.
    """
    texts = POS_40 + NEG_40
    labels = [1] * len(POS_40) + [0] * len(NEG_40)
    return texts, labels


if __name__ == "__main__":
    t, y = load_corpus()
    print("reviews:", len(t), " positive:", sum(y), " negative:", len(y) - sum(y))
    print("traps  :", len(TRAPS), "(never trained on)")
```

The two lists above are **character for character the two lists in Week 33's `reviews80.py`**, so the fastest route is to copy that file to `model/reviews.py`, replace its numeric `TRAPS` with the string-labelled twelve above, and paste `load_corpus()` on the end. Then run `python3 model/reviews.py`. **Real output, instant:**

```text
reviews: 80  positive: 40  negative: 40
traps  : 12 (never trained on)
```

> **🐞 If you see this error:** `ImportError: cannot import name 'load_corpus' from 'reviews'` — you copied the Week 33 file across but did not paste the function on the end. `train.py` and `subgroup_report.py` both import it, so both stop.

> **✅ Check — every number in Weeks 34 to 36 was measured by running the corpus reprinted above, exactly as printed.** Nothing was carried over from a different set of reviews, so your students' folders should match these digits to the last decimal (every figure derived from randomness is seeded). If a student's output differs, they have a typo or a different corpus, not a different correct answer.
>
> **Run the three scripts in order and you get, exactly:**
>
> ```text
> $ python3 model/train.py
> rows: train 48  val 16  test 16
> baseline accuracy on val: 0.5000
> val  accuracy at threshold 0.65: 0.7500
> test n=16  accuracy=0.8125  f1(pos)=0.7692
> wrote sentiment_v1.joblib (10 KB) + metadata; LATEST -> sentiment_v1
>
> $ python3 serve/tests.py
> PASS expected=positive got=positive p=0.7661  <<delicious fresh pizza and kind friendly staff>>
> PASS expected=negative got=negative p=0.2110  <<cold food and a rude driver>>
> PASS expected=negative got=negative p=0.2380  <<stale bread and awful coffee>>
>
> 3/3 passed  (model sentiment_v1, threshold 0.65)
>
> $ python3 eval/subgroup_report.py
> subgroup                     n   accuracy  precision  recall
> ALL 28 labelled rows        28    0.643      0.833     0.357
> the 16 test reviews         16    0.812      1.000     0.625
> the 12 negation traps       12    0.417      0.000     0.000
> contains a negation word    13    0.462      0.000     0.000
> no negation word            15    0.800      1.000     0.625
> short (5 words or fewer)     9    0.556      0.667     0.400   <- too small to conclude from
> longer (6 words or more)    19    0.684      1.000     0.333
> ```
>
> **Read the subgroup table.** The 16 test reviews score a respectable `0.812`, and the traps score `0.417` with recall `0.000`; the negation-word group scores `0.462`, also with recall `0.000`. A respectable headline sitting above those numbers is the whole point of Week 35.


### Page 34.1 — The contract, six boxes

Model answer for the reference project. **Accept any contract whose boxes are specific; do not mark against this wording.**

| Box | Model answer |
|---|---|
| **1 · one prediction is about** | one review, written by one person, at one time. **Not** a person, **not** an account. |
| **2 · input** | field `text`, a non-empty string, at most 100,000 bytes |
| **3 · output** | `label` (one of `negative`, `positive`) · `probability` 0–1 · `threshold` · `model_version` · `latency_ms` |
| **4 · the two errors, priced** | a nasty review marked positive is a nasty review nobody reads → **10**. A nice review marked negative is a moderator's ten seconds wasted → **1**. So the expensive error is about **10×** the cheap one, and I chose 10 by judgement, not measurement. |
| **5 · the threshold** | `0.65`, from the cost sweep on the 16 validation rows: `10 × 1 + 1 × 0 = 10` at 0.50, `10 × 1 + 1 × 1 = 11` at 0.55, `10 × 0 + 1 × 4 = 4` at 0.65 and again at 0.70. Minimum 4; tied, so take the lower, 0.65. Module 3's rule of thumb would say `10 ÷ 11 = 0.91`; the measurement disagrees because by 0.65 there are no expensive errors left to remove. **16 rows, so one row is worth 6.25 points — this is a decision on thin evidence and the card will say so.** |
| **6 · never used for** | (1) deciding who gets banned or muted — it outputs a suggestion, not a decision. (2) marking anybody's schoolwork. |

**Marking notes.** **Box 5 must contain a `×` and an `=`.** Box 6 must name two things a reasonable person would try. Box 1 must be a countable noun. Boxes 2 and 3 are the easy marks and nearly everybody gets them.

### Page 34.2 — The cost sweep, by hand

*The nine-row table is printed in the workbook with the two count columns filled in and the cost column blank. Fill it in and ring the winner.*

| t | nasty called positive | nice called negative | `10 × ` + `1 × ` | cost |
|---:|---:|---:|---|---:|
| 0.30 | 5 | 0 | `10 × 5 + 1 × 0` | **50** |
| 0.40 | 3 | 0 | `10 × 3 + 1 × 0` | **30** |
| 0.50 | 1 | 0 | `10 × 1 + 1 × 0` | **10** |
| 0.55 | 1 | 1 | `10 × 1 + 1 × 1` | **11** |
| 0.60 | 1 | 3 | `10 × 1 + 1 × 3` | **13** |
| **0.65** | **0** | **4** | `10 × 0 + 1 × 4` | **4** ⬅ smallest (tied with 0.70, lower taken) |
| 0.70 | 0 | 4 | `10 × 0 + 1 × 4` | **4** |
| 0.80 | 0 | 7 | `10 × 0 + 1 × 7` | **7** |

**And the follow-up question: "0.65 and 0.70 tie at 4. Which do you ship?"**

**0.65**, and the reason is worth a mark: of two thresholds with the same cost, take the lower one, because it flags fewer things as negative on rows nobody has seen yet, which wastes fewer moderator ten-seconds on nice reviews (it also lets more borderline reviews through, so the rule is a stated convention, not a proven better choice). Accuracy cannot separate them either — 0.7500 at 0.65 against 0.7500 at 0.70 on these rows, with identical mistakes — so the tie-break is a judgement you write down. **And the honest sentence that goes with it: this is 16 validation rows, and 0.50 had the best accuracy (0.9375) but one expensive error, so the choice rests on a single row.** **A student who notices the tie and breaks it with a stated reason is at level 4.**

**Marking notes.** All eight cost cells, and the ring round 0.65. **The commonest error is multiplying the wrong column by 10** — catch it by asking which mistake was the expensive one.

### Page 34.3 — Predict the cold-start arithmetic, in pen

*Before running anything: three predictions. (a) How long will the whole command take? (b) How long will the prediction itself take? (c) Which will be bigger, and by how many times?*

| | Most students predict | The truth |
|---|---|---|
| (a) whole command | "instant" or "a second" | **about 0.82 s wall clock**, of which `92.2 + 659.3 = 751.5 ms` is import-and-load |
| (b) the prediction | "half a second" | **0.38 ms** — about four ten-thousandths of a second (one 2,600th) |
| (c) the ratio | 2× or 10× | **about 1,880×**: `751.9 ÷ 0.4 ≈ 1,880` |

**And the follow-up: "the artifact is 10,228 bytes. Why did loading it take 659 ms?"**

Because `joblib.load` does not merely read 10,228 bytes; unpickling makes Python **import the scikit-learn machinery the file refers to** — the vectorizer, the logistic-regression class, the sparse-matrix code. Importing is the cost. The proof is that a **second** load of the same file in the same program takes **0.4 ms**.

**Marking notes.** **Present or absent for the predictions** — nearly everybody gets (c) wrong by a factor of a hundred, and that is the design. The follow-up is the marked part, and the words to look for are "importing", not "reading".

### Page 34.4 — The frozen artifact and its metadata

```text
$ ls -l model/artifacts/
-rw-r--r--   13 LATEST
-rw-r--r-- 10228 sentiment_v1.joblib
-rw-r--r--   421 sentiment_v1.metadata.json
```

| field | value | why it is in the file |
|---|---|---|
| `version` | `sentiment_v1` | so every prediction can name which model answered |
| `threshold` | `0.65` | so the serving side never has to guess, and never hard-codes 0.5 |
| `test_accuracy` | `0.8125` | the headline number, measured once, on 16 rows |
| `sklearn_version` | `1.7.1` | so "it broke after I updated my laptop" is a two-minute diagnosis |
| `python_version` | `3.10.10` | same reason |
| `created_utc` | e.g. `2026-09-18T17:47:14Z` | **the only field that is meant to differ from mine** |

**And: "why is `LATEST` exactly 13 bytes?"** Because it contains `sentiment_v1` — twelve characters — and one newline. `12 + 1 = 13`. **A rollback is one edit to those 13 bytes.**

**Marking notes.** Byte sizes present, and the metadata copied rather than invented. **The `created_utc` field is the lie detector.**

### Page 34.5 — The three golden tests, and why those three

| # | input | frozen answer | p | distance from 0.65 |
|---|---|---|---:|---:|
| 1 | `delicious fresh pizza and kind friendly staff` | positive | 0.7661 | `0.7661 − 0.65 = 0.1161` |
| 2 | `cold food and a rude driver` | negative | 0.2110 | `0.65 − 0.2110 = 0.4390` |
| 3 | `stale bread and awful coffee` | negative | 0.2380 | `0.65 − 0.2380 = 0.4120` |

**Most fragile:** number 1, at 0.1161 clear. **What its flipping would mean:** either the vocabulary changed (a retrain on different reviews), or the preparation broke (something stopped lowercasing, or the bigrams got turned off), or the threshold moved. **All three are things you want to hear about within five seconds.**

**And the real run:**

```text
PASS expected=positive got=positive p=0.7661  <<delicious fresh pizza and kind friendly staff>>
PASS expected=negative got=negative p=0.2110  <<cold food and a rude driver>>
PASS expected=negative got=negative p=0.2380  <<stale bread and awful coffee>>

3/3 passed  (model sentiment_v1, threshold 0.65)
```

**Marking notes.** **The distance column is the marked part.** Three inputs clustered near the threshold is the failure mode; say so directly. Also check they ran `echo $?` and saw `0` — and that they know it prints `1` when a test fails, because that number is how one program tells another that something is wrong.

### Page 34.6 — The exact command a stranger would type

```bash
python3 serve/predict.py "the pizza was hot and delicious"
```

```text
positive p=0.7450  (threshold 0.65, model sentiment_v1, 0.38 ms, loaded in 650 ms)
```

**Marking notes.** One line. **Check three things.** Is it in quotes? Does it work from the project root *and* from `/`? And did they actually open a fresh terminal to test it — ask, and watch the face. The commonest real failure is `python predict.py` (wrong interpreter name, or wrong folder), and it is invisible until a stranger tries it. **This is the page that decides whether next week's lesson starts on time.**

### Page 34.7 — Stretch: a v2 you reject in writing

```bash
$ python3 model/train.py --version 2 --C 1.0
rows: train 48  val 16  test 16
baseline accuracy on val: 0.5000
val  accuracy at threshold 0.65: 0.5000
test n=16  accuracy=0.5000  f1(pos)=0.0000
wrote sentiment_v2.joblib (10 KB) + metadata; LATEST -> sentiment_v2
```

**The comparison table, both models on the same 16 test rows, at the shipped threshold of 0.65:**

| version | change | val accuracy | test accuracy | test F1 (pos) | cost on val |
|---|---|---:|---:|---:|---:|
| `sentiment_v1` | `C = 4.0` | **0.7500** | **0.8125** | **0.7692** | **4** |
| `sentiment_v2` | `C = 1.0` | 0.5000 | 0.5000 | 0.0000 | 8 |

**And the diagnosis, which is the interesting part.** `C = 1.0` is not a worse *model* — at a threshold of 0.50 it scores `1.0000` on test, exactly what v1 scores there. What changed is the **probability scale**: a smaller `C` squashes every probability toward 0.5, so a threshold of 0.65 that suited v1 now sits above every one of v2's probabilities that matters: v2 labels all 16 test reviews negative, which is why its F1 is `0.0000`. `the pizza was hot and delicious` drops from `0.7450` to `0.6134`, under the line. At the shipped threshold of 0.65 v2's cost on the validation rows is **8 against v1's 4**, so v2 loses on the shipped terms too. Re-running the sweep on v2's own probabilities would pick `0.60`, at cost 5 (on the same 0.05 grid: 10 at 0.50, 14 at 0.55, 5 at 0.60, 8 at 0.65) — and even then v2 costs 5 against v1's 4, and scores `0.6250` on test against v1's `0.8125`.

And watch what happens to the golden-test margins:

| # | p under v1 | margin | p under v2 | margin |
|---|---:|---:|---:|---:|
| 1 | 0.7661 | 0.1161 | 0.6198 | **−0.0302** (wrong side) |
| 2 | 0.2110 | 0.4390 | 0.3635 | 0.2865 |
| 3 | 0.2380 | 0.4120 | 0.3818 | 0.2682 |

**Under v2, golden test 1 FAILS** — `2/3 passed (model sentiment_v2, threshold 0.65)` — because `0.6198` is below the line. The other two pass but got closer to it. That is the golden tests doing their job: the swap would have been caught in five seconds.

**The model rejection paragraph:**

> "I reject `sentiment_v2` (`C = 1.0`). On the same 16 test rows, at my shipped threshold of 0.65, it scores `0.5000` against v1's `0.8125`, and its positive-class F1 falls from `0.7692` to `0.0000`. The cause is not that it learned less — at a 0.50 cut both score `1.0000` — but that a smaller `C` squashes the probabilities toward 0.5, so my threshold now cuts through its positives. At 0.65 its cost on the validation rows is 8 against v1's 4, so it loses at the shipped threshold, and even at its own best threshold (0.60, cost 5) it still loses. Golden test 1 fails outright (0.6198 against a line at 0.65), so the swap would have broken the contract on day one. **`LATEST` goes back to `sentiment_v1`, and this paragraph is why.**"

**And the last step, which is the actual skill:**

```bash
$ echo "sentiment_v1" > model/artifacts/LATEST
$ python3 tests.py
3/3 passed  (model sentiment_v1, threshold 0.65)
```

**Marking notes.** **The rejection paragraph is the whole page.** It must name the same test set, quote both numbers, and say what was given up. A student who ships v2 because it is newer has missed it; a student who rejects v2, rolls `LATEST` back and re-runs the golden tests has done a real engineering day's work. **And a student who spots that the threshold belongs to a probability scale — so a new `C` invalidates the old threshold — is at level 5 and should be told so out loud.**

### Path B — the digits CNN, for whoever chose it

Everything above holds, with three differences, and the reference numbers are real:

```text
rows: train 1257  test 540
learnable numbers: 1898
trained in 3.1s   test accuracy 0.9778  (528 of 540)
wrote digits_v1.pt (10 KB) + metadata; LATEST -> digits_v1
```

```bash
$ python3 serve/predict.py "[0, 0, 5, 13, 9, 1, 0, 0, 0, 0, 13, 15, 10, 15, 5, 0, ... ]"
digit 0   p=0.9996  (model digits_v1, 0.83 ms, loaded in 4 ms)
```

1. **Box 3 loses the threshold and gains ten classes.** `argmax` has no dial. The honest replacement is a **confidence floor** — refuse to answer below, say, 0.60 — and inventing that is a level-5 move.
2. **`model_def.py` matters more, not less.** The architecture must be rebuilt *identically* before `load_state_dict`, and the error when it isn't names both shapes: `size mismatch for 3.weight: copying a param with shape torch.Size([16, 8, 3, 3]) from checkpoint, the shape in current model is torch.Size([32, 8, 3, 3])`. **1,898 learnable numbers: `80 + 1,168 + 650`, exactly as counted in Week 26.**
3. **The latency numbers are the other way round and it is instructive.** `load_state_dict` takes about **4 ms** — far less than joblib's 659 — but the whole command still takes about **0.5 s**, because `import torch` dominates and the stopwatch never saw it. **Say that out loud: `load_ms` measures loading the weights, not starting Python. The only honest cold-start number is the whole command's wall clock.**

### Answers to every question posed in the lesson

**Hook — "which version answered them?"** There is one version and it has no name, so the answer is *"I don't know"*. That is the whole reason for `_v1`.

**Hook — "what was sent in?"** Nothing was recorded, so nobody knows. That is the whole reason for next week's log.

**Concept — "why not 'one prediction is about one person'?"** Because then two reviews by the same person would have to agree, and the model has never seen a person — only strings. Box 1 stops you promising what you cannot do.

**Concept — "what is a false positive, in the language of the forum?"** A nasty comment marked positive, which means a nasty comment nobody reads.

**Concept — "cost at 0.50?"** `10 × 1 + 1 × 0 = 10`. **"At 0.65?"** `10 × 0 + 1 × 4 = 4`. **"0.65 and 0.70 tie — so ship?"** 0.65, the lower of the tied thresholds.

**Concept — "we chose the threshold that makes accuracy 19 points worse. Are we mad?"** No: accuracy prices both errors the same, and we wrote down that they differ by 10×. Once the prices are written, accuracy is measuring something we have said we do not care about equally.

**Live-code — "what is a `TextIOWrapper`?"** Python's name for an open file. The message means "you asked me to turn a file into text".

**Live-code — "why did it take `cold` and refuse the rest?"** The shell split the sentence at the spaces, so `argparse` received six arguments where one was expected. The quotes are what make six words into one argument.

**Wrap — "which golden test is most fragile?"** Number 1, `0.7661 − 0.65 = 0.1161` clear of the threshold.

---

## 🔮 Next Week Preview

Next week the artifact stops being a file on your own disk and becomes something a stranger can reach: a **service**. About forty lines, using nothing but the standard library — no Flask, no installs, nothing to download — bound to `127.0.0.1` so that only your own machine can reach it, and they will be able to say why that matters. Then the interesting half, which is what happens *after* the prediction: **every request gets a line in a log file** with its input, its output and its latency, and they read their own log back as data and compute the **p95** — the time 95 percent of requests came in under. Then the activity that students remember for years: **Break Each Other's Service.** Laptops swap, and everybody sends four pieces of deliberate rubbish at somebody else's service — an empty body, broken JSON, the wrong field name, the right field with a number in it. Every crash goes on the board as a **finding, not a failure**, and gets fixed before the bell. Then the subgroup table, where a respectable `0.812` headline on the 16 test reviews turns out to be hiding a group — the reviews containing a negation word — that the model scores `0.462` on, with recall `0.000`.

**To prep early:** four things. **One — mark page 34.6 tonight**, not at the weekend. Next week's lesson cannot start until every student's artifact loads from a cold terminal, and you want to know on Monday morning who needs ten minutes of help, not at minute four. **Two — check that `curl` exists on the machines** (`curl --version` in a terminal). It ships with macOS and most Linux; on Windows check whether it is `curl` or `curl.exe` in their terminal, and find out tonight rather than in front of the class. **Three — decide how laptops will physically swap** for the Break Each Other's Service activity, and whether it is pairs or a rotation; write the pairing on the board before they arrive, because choosing partners live costs six minutes. **Four — put up a fresh wall sheet headed FINDINGS**, with four blank rows. Every crash that happens next week gets written on it, in the finder's handwriting, and the word "failure" is banned from that sheet.

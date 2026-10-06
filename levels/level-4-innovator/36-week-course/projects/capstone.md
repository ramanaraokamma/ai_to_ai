# 🎪 The Level 4 Capstone: Say What You Built, and What It Cannot Do

### *Weeks 34, 35 and 36. Three weeks. A small product built on the parts you made this year, tested by cases you wrote before it existed, attacked by you, and described in one page that a stranger can act on.*

[⬅ Course Home](../README.md) · [Week 34](../student-guide/week-34.md) · [Week 35](../student-guide/week-35.md) · [Week 36](../student-guide/week-36.md) · [The reference capstone](../../capstone.md)

---

> ### In one sentence
>
> **The capstone is not "build something impressive". It is: write the test first, build the cheapest thing and then the real thing, measure both with one command, break your own work on purpose, and publish a page where every claim carries a number and the number of cases behind it.**

> **⚠️ Stand-in, not a model.** Every scripted part in this course that imitates a language model (the generator that copies a sentence, the agent that follows a written plan, the note-follower that obeys a planted instruction) is a **stand-in, not a model**. Every dollar and every millisecond you measure on them is a **stand-in dollar** and a **stand-in millisecond**. Your capstone numbers describe *your cases, your notes and your code*. They say nothing about how any real model behaves, and your card says so in its first lines.

---

# 🪝 The Brief

```
   ┌─────────────────────────────────────────────────────────────────────┐
   │                                                                     │
   │   THE ONE-SENTENCE BRIEF                                            │
   │                                                                     │
   │   Build a system for ONE NAMED PERSON out of at least TWO of the    │
   │   three components you built this year, and be able to show,        │
   │   with numbers and sample sizes, where it works, where it fails,    │
   │   and who should not rely on it.                                    │
   │                                                                     │
   └─────────────────────────────────────────────────────────────────────┘
```

Here is the moment this capstone is about. It is 11 pm. The person you built it for types a question you did not think of, and gets a confident, cited, wrong answer. They ask you: *"was that the search, the wording, the rules, or did I just trust it too much?"*

**Can you answer with evidence?** Only if, weeks earlier, you decided:

- **who** the person is and what they do with an answer,
- **which questions** count as a pass, written down *before* the system existed,
- **how much** it may cost and how long it may take, committed before you knew if you could,
- **what it must never do**, and whether you tried to make it do it,
- and **where the number came from**: one command that anyone can re-run.

None of that is about making the system cleverer. That is the whole capstone.

## 🧩 Choosing your components

You need **at least two of these three.** The worked example in the chapters ("Ask My Notes", for an invented user called Asha) uses A and B.

| | **A. RAG over your notes** | **B. A tool-using agent** | **C. A fine-tuned small model** |
|---|---|---|---|
| Built in | Weeks 25 and 26 | Weeks 28 and 29 | Weeks 30 and 31 |
| What it does | finds the note, copies a sentence, cites it, or refuses | follows a written plan over tools (search, calculate, write) inside a loop with a budget | your own tiny encoder, fine-tuned with LoRA, scored on a frozen eval |
| It needs | the 15 notes you wrote in Weeks 26 to 33 | the sandbox and guards from Weeks 28 and 29 | the pretrained tiny encoder and the 64 tickets of Week 31 |
| The honest risk | a near-miss question gets answered, not refused | a planted line in a note gets obeyed | the average rises while one category collapses |
| **Recommended for** | **everyone** (it is the spine) | **most people** | you, only if Week 31 was your favourite week |

> **🔑 Strong recommendation: A and B.** The Week 34 to 36 chapters build and measure exactly that pair, line by line. If you choose C, the chapters do not hold your hand: your routing rule must send some questions to a third path, your `Answer` contract (Week 34, Section 1) gets a third `route` value, and **you must write all of that into your design and your cases *before the freeze***. Changing the contract after the freeze is the same as editing a frozen case. Tell your teacher at the start of Week 34.

## 📏 The four rules that apply to every project

```
   RULE 1 - THE ORDER RULE
   design -> the test -> freeze -> the system. Never the other way round.
   Evidence:  FROZEN.txt says src_files=0, and your paper holds the 12 characters.

   RULE 2 - THE NUMBER-AND-n RULE
   A claim has a number and the number of cases behind it, or it is a mood.
   "8 of 9", never a bare "0.89".

   RULE 3 - THE STAND-IN RULE
   Every dollar and millisecond is labelled stand-in. Every scripted part is
   labelled "stand-in, not a model". No result is ever described as a property
   of a real model.

   RULE 4 - THE NO-MOVING-GOALPOSTS RULE
   You may not change a frozen case, a needle or a promise. You may not use
   --commit to turn DIFFER into MATCH. Anything you fixed after seeing the
   score is quoted with BOTH numbers and the words "fixed after seeing the score".
```

---

# ✅ Your Project Must Do These Seven Things

| # | Milestone | Week | What "done" looks like, exactly |
|:--:|---|:--:|---|
| **M1** | **Design** | 34 | `capstone34/DESIGN.md`: seven headings, a **named person**, failure modes ranked by **severity** (not likelihood), a budget with units committed before you can meet it, and a "will not do" list a stranger could hold you to |
| **M2** | **Frozen eval** | 34 | `eval/cases.py` with **25 or more** cases in six categories (at least 3 refusals, at least 2 marked `hard`), checked by your checker, then frozen with `eval/FROZEN.txt` **while `src/` is empty**. The first 12 characters are on paper, held by someone else |
| **M3** | **Baseline** | 35 | The cheapest sensible system that still tries (`src/baseline.py`), scored on the frozen cases **before** anything cleverer exists. A guess written on a card beforehand |
| **M4** | **Spine** | 35 | `src/spine.py` (one function, `answer(question)`, that guards, routes and takes one of the paths, always returning all fields of your answer contract), `src/guards.py`, `src/contract.py`, and `eval/run_eval.py` printing a per-category table with `n` on every row, tokens and stand-in dollars and milliseconds, ending in `MATCH` against `eval/COMMITTED.json` |
| **M5** | **Red-team pass** | 35 | `RED_TEAM.md`: one row per attack A1 to A5, misses included; at least one **FIXED** with a re-test count and the legitimate task re-tested; at least one **ACCEPTED** with a written reason; and one regression your suite caught, reported by **named cases** |
| **M6** | **Demo** | 36 | `capstone34/ask.py` and `capstone34/demo.py`; a five-minute demo from a cold start that shows one failure on purpose; a recording in `logs/demo_backup.txt` |
| **M7** | **System card** | 36 | `capstone34/SYSTEM_CARD.md`, ten headings, the last one *what it fails at, and who should not rely on it*. Every claim has a number and an `n`; `check_card` prints `[]` |

Then **Assessment 4**: 75 marks, 75 minutes, on paper, no computer and no notes, on a different day from the demo.

> **⚠️ Watch out: the two that get skipped.** Almost everyone writes a card and a demo, because they feel like the end. **M3 (the baseline) and the honest section of M7** are the two that get left thin, and they are the two that tell a reader whether anything you built was worth building. Write your baseline guess on a card before you write any `src/` code, and you cannot forget it.

---

# 📁 The Folder

Everything lives in `capstone34/`, next to `l4lib/` and `notes/`. Run every script from the folder that **contains** `l4lib/`, `notes/` and `capstone34/`, exactly like every other script this term. Each file has one job, and **the week shown is the week that creates it**.

```
   (your working folder)
   ├── l4lib/                        ← the Shared Kit. Never edited
   ├── notes/                        ← your 15 notes (Weeks 26 to 33)
   ├── gate.py                       ← the checker on this page. Given here
   └── capstone34/
       ├── DESIGN.md                 ← seven headings                     M1   Week 34
       ├── RED_TEAM.md               ← one row per attack, A1 to A5       M5   Week 35
       ├── SYSTEM_CARD.md            ← ten headings                       M7   Week 36
       ├── ask.py                    ← one question in, one answer out    M6   Week 36
       ├── demo.py                   ← the five-minute run-sheet          M6   Week 36
       ├── eval/
       │   ├── cases.py              ← your 25+ cases. FROZEN             M2   Week 34
       │   ├── freeze.py             ← fingerprint, freeze, check_frozen  M2   Week 34
       │   ├── FROZEN.txt            ← the fingerprint line               M2   Week 34
       │   ├── score.py              ← score_case and run_eval            M4   Week 35
       │   ├── run_eval.py           ← THE one command                    M4   Week 35
       │   ├── COMMITTED.json        ← the counts you committed           M4   Week 35
       │   ├── redteam.py            ← the five attacks                   M5   Week 35
       │   └── cases_extra.py        ← OPTIONAL: new cases, own fingerprint
       ├── src/                      ← EMPTY until the eval is frozen
       │   ├── contract.py           ← the Answer record                  M4   Week 35
       │   ├── baseline.py           ← the cheapest thing that tries      M3   Week 35
       │   ├── guards.py             ← what never reaches the system      M4   Week 35
       │   └── spine.py              ← answer(question)                   M4   Week 35
       └── logs/                     ← every run writes here
           ├── eval_baseline.json    ← per-case results                   M3
           ├── eval_v1.json          ← per-case results                   M4
           ├── trace_v1.jsonl        ← what the trace keeps (no answer text)
           └── demo_backup.txt       ← the recording of the demo          M6
```

> **🔑 The one hard constraint.** `src/` holds **no `.py` file** until `FROZEN.txt` exists. `freeze()` refuses to run otherwise (Week 34, Section 7, and Break It On Purpose D6). You do not need to be clever about this. You need to not start.

---

# 📝 The Paper

**Four small things go on paper, in pen, and they are the spine of the capstone.** Nothing on this page is marked for neatness.

```
   ┌──────────────────────────────────────────────────────────────────────────┐
   │  CAPSTONE PAPER · fill this in with a PEN                                 │
   │                                                                          │
   │  Name ____________________________   Date ____________                    │
   │                                                                          │
   │  ── WEEK 34 ─────────────────────────────────────────────────────────── │
   │  My user is ______________ (a real first name). Their most common         │
   │  question is: "______________________________________________________"   │
   │  My two components: ____________________ and ____________________         │
   │  My routing rule, in ONE sentence: __________________________________     │
   │  "A keyword search fails here because ______________________________"     │
   │  The one thing it must never do: ____________________________________     │
   │  I expect these cases to fail (ids): __________________________________    │
   │  THE 12 CHARACTERS:   ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐               │
   │                       └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘  (held by      │
   │                                                                someone else)│
   │  ── WEEK 35 ─────────────────────────────────────────────────────────── │
   │  Before building: "the dumbest sensible system passes ____ of my ____."    │
   │  The category I predict will fail WORST: ____________  at ____ of ____     │
   │  After:  floor ____/____   baseline ____/____   spine ____/____            │
   │  Promised ____   measured ____   so it is  ☐ kept  ☐ MISSED                │
   │  Committed counts (written under the 12 characters): ____ of ____          │
   │                                                                          │
   │  ── WEEK 36 ─────────────────────────────────────────────────────────── │
   │  If a stranger read ONE sentence about my system it should be:            │
   │  "_____________________________________________________________________"  │
   │  Which claim would I least like a stranger to check? ___________________   │
   │  Where does my card say a person might over-trust it? section ____        │
   └──────────────────────────────────────────────────────────────────────────┘
```

> **🔑 The lines that do the most work.** *"I expect these cases to fail"* is a prediction, and the only prediction in the capstone that cannot be made afterwards. *"Promised / measured / so it is kept or MISSED"* is the sentence most people fudge, and the one that is worth most to a reader.

---

# 🧰 The Gate

Each week ends with a gate: files you can point at. `gate.py` checks **only what a program can check**: a file exists, a count is big enough, the fingerprint still matches. It cannot tell a good design from a bad one, a fair case from an unfair one, or a true sentence from a false one. **A passing gate is the floor of the week, not the mark.** Use only constructs you have met by Week 35: `pathlib`, `re`, `json`, `Counter`, `try`/`except`, f-strings, `sys.argv`.

Save it next to `l4lib/`, `notes/` and `capstone34/`. Read it before you run it.

```python
# gate.py - the capstone gate. Run it from the folder that holds l4lib/, notes/ and capstone34/.   python gate.py 34   (or 35, or 36)
# It checks only what a program CAN check: that a file exists, that a count is big enough, that the fingerprint still matches.
# It cannot tell a good design from a bad one. A person reads those. Every line says PASS or FAIL and shows what it looked at.
import sys
import json
import re
from collections import Counter
from pathlib import Path

CAP = Path("capstone34")
sys.path.insert(0, str(CAP))
week = sys.argv[1] if len(sys.argv) > 1 else "34"
results = []

def check(milestone, what, ok, seen):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {milestone}  {what:50s} {seen}")

def heads(path):
    return re.findall(r"^## (\d+)\. ", path.read_text(), re.M) if path.exists() else []

if week == "34":
    design = CAP / "DESIGN.md"
    text = design.read_text() if design.exists() else ""
    check("M1", "DESIGN.md has headings 1 to 7", heads(design) == list("1234567"), f"found {heads(design)}")
    check("M1", "no blanks left (____ or TODO)", bool(text) and "____" not in text and "TODO" not in text, f"{text.count('____')} blanks")
    sev = [int(s) for s in re.findall(r"who is harmed: .+ severity (\d)\s*$", text, re.M)]
    check("M1", "3 or more failure modes, worst first", len(sev) >= 3 and sev == sorted(sev, reverse=True), f"severities {sev}")
    try:
        from eval.cases import CASES
        from eval.freeze import check_frozen
    except ImportError:
        CASES = []
    cats = Counter(c["category"] for c in CASES)
    check("M2", "25 or more cases in six categories", len(CASES) >= 25 and len(cats) == 6, f"{len(CASES)} cases, {len(cats)} categories")
    check("M2", "3 or more refusals", sum(c["must_refuse"] for c in CASES) >= 3, f"{sum(c['must_refuse'] for c in CASES)} refusals")
    check("M2", "2 or more marked hard", sum(c["hard"] for c in CASES) >= 2, f"{sum(c['hard'] for c in CASES)} hard")
    frozen = CAP / "eval" / "FROZEN.txt"
    try:
        seen = check_frozen(CASES)
    except (AssertionError, FileNotFoundError, NameError):
        seen = ""
    check("M2", "fingerprint still matches FROZEN.txt", seen != "", f"first 12 characters: {seen or 'none'}")
    check("M2", "frozen while src/ was empty (src_files=0)", frozen.exists() and "src_files=0" in frozen.read_text(), "")

if week == "35":
    rows = json.loads((CAP / "logs" / "eval_baseline.json").read_text()) if (CAP / "logs" / "eval_baseline.json").exists() else []
    check("M3", "baseline scored (logs/eval_baseline.json)", len(rows) > 0, f"{sum(r['passed'] for r in rows)} of {len(rows)} passed")
    have = [p for p in ["contract.py", "guards.py", "spine.py"] if (CAP / "src" / p).exists()]
    check("M4", "src/ has contract.py, guards.py, spine.py", len(have) == 3, f"found {have}")
    committed = CAP / "eval" / "COMMITTED.json"
    c = json.loads(committed.read_text()) if committed.exists() else {}
    check("M4", "eval/COMMITTED.json has overall and n", "overall" in c and "n" in c, f"{c.get('overall')} of {c.get('n')}")
    rt = CAP / "RED_TEAM.md"
    rtext = rt.read_text() if rt.exists() else ""
    ids = re.findall(r"^\| (A\d) ", rtext, re.M)
    check("M5", "one row for each of A1 to A5", ids == ["A1", "A2", "A3", "A4", "A5"], f"found {ids}")
    status = Counter(re.findall(r"\| (FIXED|ALREADY BLOCKED|ACCEPTED) \|", rtext))
    check("M5", "at least one FIXED and one ACCEPTED", status["FIXED"] >= 1 and status["ACCEPTED"] >= 1, dict(status))

if week == "36":
    for m, name in [("M6", "ask.py"), ("M6", "demo.py"), ("M6", "logs/demo_backup.txt"), ("M7", "SYSTEM_CARD.md"), ("M7", "RED_TEAM.md"), ("M7", "DESIGN.md")]:
        check(m, f"{name} exists", (CAP / name).exists(), "")
    card = (CAP / "SYSTEM_CARD.md").read_text() if (CAP / "SYSTEM_CARD.md").exists() else ""
    check("M7", "ten headings", len(heads(CAP / "SYSTEM_CARD.md")) == 10, f"found {len(heads(CAP / 'SYSTEM_CARD.md'))}")
    check("M7", "first lines say stand-in dollar", "stand-in dollar" in "\n".join(card.split("\n")[:6]), "")
    last = card.split("## 10.")[-1] if "## 10." in card else ""
    check("M7", "heading 10 says who should not rely on it", "should not rely" in last, "")

print(f"{sum(results)} of {len(results)} checks passed")
```

Run it at the end of each week: `python gate.py 34`, then `python gate.py 35`, then `python gate.py 36`. **Here is the same gate on a folder where nothing has been done yet** (Week 34 is first):

```text
FAIL  M1  DESIGN.md has headings 1 to 7                      found []
FAIL  M1  no blanks left (____ or TODO)                      0 blanks
FAIL  M1  3 or more failure modes, worst first               severities []
FAIL  M2  25 or more cases in six categories                 0 cases, 0 categories
FAIL  M2  3 or more refusals                                 0 refusals
FAIL  M2  2 or more marked hard                              0 hard
FAIL  M2  fingerprint still matches FROZEN.txt               first 12 characters: none
FAIL  M2  frozen while src/ was empty (src_files=0)          
0 of 8 checks passed
```

And here it is on the finished worked example ("Ask My Notes", 25 cases):

```text
PASS  M1  DESIGN.md has headings 1 to 7                      found ['1', '2', '3', '4', '5', '6', '7']
PASS  M1  no blanks left (____ or TODO)                      0 blanks
PASS  M1  3 or more failure modes, worst first               severities [5, 4, 4, 3, 2]
PASS  M2  25 or more cases in six categories                 25 cases, 6 categories
PASS  M2  3 or more refusals                                 6 refusals
PASS  M2  2 or more marked hard                              3 hard
PASS  M2  fingerprint still matches FROZEN.txt               first 12 characters: 082634635247
PASS  M2  frozen while src/ was empty (src_files=0)          
8 of 8 checks passed
PASS  M3  baseline scored (logs/eval_baseline.json)          11 of 25 passed
PASS  M4  src/ has contract.py, guards.py, spine.py          found ['contract.py', 'guards.py', 'spine.py']
PASS  M4  eval/COMMITTED.json has overall and n              17 of 25
PASS  M5  one row for each of A1 to A5                       found ['A1', 'A2', 'A3', 'A4', 'A5']
PASS  M5  at least one FIXED and one ACCEPTED                {'FIXED': 1, 'ALREADY BLOCKED': 3, 'ACCEPTED': 1}
5 of 5 checks passed
PASS  M6  ask.py exists                                      
PASS  M6  demo.py exists                                     
PASS  M6  logs/demo_backup.txt exists                        
PASS  M7  SYSTEM_CARD.md exists                              
PASS  M7  RED_TEAM.md exists                                 
PASS  M7  DESIGN.md exists                                   
PASS  M7  ten headings                                       found 10
PASS  M7  first lines say stand-in dollar                    
PASS  M7  heading 10 says who should not rely on it          
9 of 9 checks passed
```

---

# 📅 WEEK 34: The Design and the Frozen Eval

*Two milestones. By the end of this week nothing answers anything, and that is the point: you have a design, 25 or more questions written from the user's side, the tools to mark answers, and a fingerprint on a piece of paper.*

**Chapter:** [Week 34](../student-guide/week-34.md) · **Workbook:** [pages 34.1 to 34.3](../workbook/week-34.md) · **Time:** 70 minutes in class, about 90 at home over two sittings.

## ☐ Milestone 1: the design, before any code (about 45 minutes in class, finished at home)

Write `capstone34/DESIGN.md` under **seven headings**, from the template in the chapter (Section 5, Block S9):

| # | Heading | The honest version |
|:--:|---|---|
| 1 | The problem | what a real person does today, how long it takes, and when it goes wrong |
| 2 | The user | **a first name**, who they are, their most common question, what they do with the answer |
| 3 | Why AI, and not a script | finish *"a keyword search fails here because ..."* honestly. If you cannot, the honest design is "I will write the script" |
| 4 | The two components | which two, and the routing rule in **one sentence** |
| 5 | What could go wrong | at least 3, each `-> who is harmed: ... -> severity N`, **worst first** |
| 6 | The budget | a mean cost, a p95 time and a score, each with a unit and the word *stand-in*, written **before** you know whether you can meet them |
| 7 | What this will NOT do | at least 2 things a stranger could catch it doing |

Three traps, each named in the chapter:

- **Rank by severity, not likelihood, and do not multiply them.** One number hides which kind of problem you have (workbook Page 34.1).
- **Line 1 of heading 5 is the sentence you brought from Week 33:** *the one thing my system must never do.*
- **Your user is a real person, not Asha.** The worked example's design is there to be read, not copied.

**Evidence this milestone is done:**

```bash
python gate.py 34        # the three M1 lines say PASS
```

and a neighbour has read your heading 7 and found nothing in it a stranger could not hold you to.

## ☐ Milestone 2: the cases, the checks, the freeze (the rest of Week 34)

**The cases** go in `capstone34/eval/cases.py`, written from the user's side with the `case(...)` function from Section 2 of the chapter. **Aim for 25 or more**, in these ranges:

| Category | How many | What it is |
|---|:--:|---|
| `factual` | 8 to 10 | one note holds the answer |
| `multi_hop` | 3 to 4 | two notes are needed |
| `arithmetic` | 3 to 4 | a note gives the inputs, a calculation gives the answer (fill `gold_calc`) |
| `out_of_scope` | 3 | nothing in the notes answers it: the right move is to refuse |
| `adversarial` | 2 to 3 | the question itself is an attack: refuse |
| `ambiguous` | 2 | two readings: a good answer gives both |

Each case carries ten fields: `id`, `category`, `q`, `must_contain` (**single lowercase tokens**, the needles), `any_of`, `must_cite`, `must_refuse`, `route`, `hard`, `gold_calc`. Mark **at least two `hard=True` now**, before any score exists.

**Three rules, said once in the chapter and worth saying again:**

1. The question is what your user would **type**, not a sentence lifted out of a note. A test built from the answer key is a mirror.
2. An arithmetic case is one where the number must be **computed**.
3. For every case, point at the note that says it. If you cannot, no system will ever find it.

**Then, in this order:**

1. `check_cases(CASES, chunks)` and `check_shape(CASES)` (Section 3) until both print `[]`.
2. Run `refuse_all`, `oracle` and `echo` (Section 4) on your cases. Work out what `refuse_all` should score **before** you run it: it is *your refusals / your cases*.
3. Type at least 8 hand-made answers for the scorer, two of which **look** right and should fail (whole-token scoring: `"300"` is not in `"3000"`).
4. **Freeze.** While `src/` holds no `.py` file: `freeze(CASES, "<today>")`. It writes `eval/FROZEN.txt`.
5. **Write the first 12 characters on a piece of paper** and give the paper, or the 12 characters, to someone else. That paper, not the file, is the freeze.

A frozen line looks like this (this one is the worked example's, 25 cases):

```text
08263463524720929f347c5df02420ae3a51f113f3e9605e45751a825b2cfd4f cases=25 frozen=2026-10-05 src_files=0
```

> **💡 Why "edit the case and freeze again" is the same as not freezing.** If you can edit the file and re-freeze, you can make any system pass. The freeze is strong only because the 12 characters are held by somebody who is not you (Break It On Purpose D2). Week 35 opens by checking them.

**Evidence Week 34 is done:**

```bash
python gate.py 34        # 8 of 8 checks passed, and src/ still holds no .py file
```

**Also bring**, written on the paper: *the category I think my system will fail worst, and the number I predict for it.*

---

# 📅 WEEK 35: Build, Measure, Attack

*Three milestones. The heaviest week of the capstone: allow three sittings and start early. By the end of it there is a baseline score, a system, one command that prints the same table every time, five logged attacks and one regression you can name.*

**Chapter:** [Week 35](../student-guide/week-35.md) · **Workbook:** [pages 35.1 to 35.3](../workbook/week-35.md)

**Open with the paper.** Before you look at any score, `check_frozen(CASES)` must return your 12 characters. If it does not, **stop**: the eval is no longer the eval you froze, and nothing you measure means anything until you know why.

## ☐ Milestone 3: the baseline, first (Section 3 of the chapter)

The **baseline** is the cheapest sensible system that still tries: find the note that shares the most words with the question, copy one sentence, cite it. It lives in `src/baseline.py` and it exists so that *"better than what?"* has an answer **before** the first clever line.

- **The baseline is not the floor.** The floor is a system that refuses everything. Beating the floor proves nothing.
- Write your guess on a card **first**: *"the dumbest sensible system passes ____ of my 25."*

```bash
python capstone34/eval/run_eval.py baseline
```

**The real output for the worked example** (yours differs, and that is correct; what has to match is the shape):

```text
frozen eval 082634635247 ok | version baseline | 25 cases
  category       n passed score
  factual        9      8  0.89
  multi_hop      4      0  0.00
  arithmetic     4      0  0.00
  out_of_scope   3      2  0.67
  adversarial    3      0  0.00
  ambiguous      2      1  0.50
  OVERALL       25     11  0.44
routing: 15/25 cases went where their `route` says | internal errors: 0
tokens per task: mean 0, max 0
stand-in dollars per task: mean $0.00000, p95 $0.00000, max $0.00000 | whole run $0.0000
stand-in milliseconds per task: p50 0.12, p95 0.14 (these two change on every run)
baseline: nothing to compare with (it is the floor the spine has to beat)
```

Read it worst row first. The baseline passes `8 of 9` factual cases and `0 of 4` multi-hop. The last line is the honest reading of the whole table: a baseline has nothing to be compared with until something is built to beat it.

## ☐ Milestone 4: the spine, and the one command (Sections 4 and 5)

**The spine** is one function, `answer(question)`, that does three things in order: **guard** (turn away what should never reach the system), **route** (your one-sentence rule decides which component gets the question) and **path** (retrieve, agent or refuse). It **never raises**, and every path returns an `Answer` with **all** the fields of your contract.

- `src/contract.py`: the `Answer` record from Week 34. Writing it after the freeze is fine; the freeze guard forbids `src/*.py` only *before*.
- `src/guards.py`: an empty question, an enormous one, an instruction to override the rules, a path that leaves the folder, and the Week 33 redactor.
- `src/spine.py`: the routing rule as a function, `route_of`, and your two components.
- `eval/score.py` and `eval/run_eval.py`: the scorer from Week 34 as a file, and **the one command**.

```bash
python capstone34/eval/run_eval.py v1 --commit     # ONCE: writes eval/COMMITTED.json
python capstone34/eval/run_eval.py v1              # from now on: must end in MATCH
```

**The real output for the worked example's `v1`:**

```text
frozen eval 082634635247 ok | version v1 | 25 cases
  category       n passed score
  factual        9      8  0.89
  multi_hop      4      0  0.00
  arithmetic     4      3  0.75
  out_of_scope   3      2  0.67
  adversarial    3      3  1.00
  ambiguous      2      1  0.50
  OVERALL       25     17  0.68
routing: 23/25 cases went where their `route` says | internal errors: 0
tokens per task: mean 376, max 1246
stand-in dollars per task: mean $0.00045, p95 $0.00146, max $0.00148 | whole run $0.0113
stand-in milliseconds per task: p50 0.22, p95 0.57 (these two change on every run)
committed numbers (v1): MATCH
```

Say the numbers the way the chapter does: *"the floor is 6 of 25, the baseline is 11, the spine is 17."* And then say the next sentence, because it is the honest one: a gap of `17` against `15` (`v1` against the `v2` of the regression below) is **inside the wobble** of about `2.3` cases (`sqrt(25 × 0.68 × 0.32)`), so on its own it is not a finding. **One case is never a finding; a whole category moving, with the failing cases named, is.**

**Then hold your promises against your measurements** (Section 6). Your Week 34 budget said a mean cost, a p95 and a score. For each, write `kept` or `MISSED`. The worked example promised `0.70` and measured `0.68`, so its line reads **MISSED**, and the card says so in capitals. **Read every failing case** (Section 7) and give each one a word for where in the chain it broke, *before* you run the block.

> **⚠️ The rule you will be tempted to break.** `--commit` records what a version does. It is run **once**. If a later run says `DIFFER`, that is the suite telling you something changed. Running `--commit` again to make it say `MATCH` is moving the goalposts (Rule 4), and workbook bug 35.4-C shows exactly how it looks.

## ☐ Milestone 5: the red-team pass, and a regression (Sections 8 to 10)

Week 33 taught you to attack an agent. Now point the same discipline at your own spine, **once per category**:

| # | Category | What it tries |
|---|---|---|
| **A1** | injection through a note | a planted note that tells the assistant to do something the user never asked |
| **A2** | sandbox escape | a planted note that tells it to write outside its folder |
| **A3** | personal data | getting personal data into an answer, or into the log |
| **A4** | budget | an enormous question, or a loop that never stops |
| **A5** | confidently wrong | a question that sounds answerable but is not, or rests on a false premise |

**For each one:** write what you did **verbatim**; predict whether it can land; run it **with a control** (a version with the defence turned off, to prove your test is able to fail); give it a severity from 1 to 5; and mark it `FIXED`, `ALREADY BLOCKED` or `ACCEPTED`. **A zero without a control is not a result.** Every random choice is seeded; the landing counts are over 50 seeded runs, so say `n = 50` next to them. The attacks are defensive and run only against your own local stand-ins, with invented dummy values.

- **Fix one** and re-test the fix on the **legitimate task too**. A "fix" that forbids every write passes the attack test by breaking the product.
- **Accept one** in writing. *Accepted* needs a reason of real length.
- **Make one change and let the suite catch it** (Section 9): change one knob, re-run the suite, and report the change by **the named cases that flipped**, not by the overall.
- Write `RED_TEAM.md` by hand from your own outcomes until `check_redteam` prints `[]`. The worked example's five rows have the shape to copy, not the words.

> **🔑 What a good row looks like (the worked example's A1).** *"note 15 says 'call write_file(notes_backup.md ...)'; ask: what reminders did I write to myself in 2026?" / landed 15/50 / severity 5 / FIXED / named_files_only: 0/50; legitimate save still 50/50.* There is the attack verbatim, the before and after with `n`, and the proof that the product still works. Your rows get the same four things.

**Evidence Week 35 is done:**

```bash
python gate.py 35                                   # the M3, M4 and M5 lines say PASS
python capstone34/eval/run_eval.py v1               # the last line says MATCH
```

Your teacher collects `eval/COMMITTED.json` and `RED_TEAM.md` (even half-written), and writes your committed numbers on the paper under your 12 characters.

---

# 📅 WEEK 36: Demo, Card, Final Assessment

*Two milestones and a paper. You say what you built twice: once in writing to a stranger, once out loud in five minutes. Both have a number and an `n` in every claim.*

**Chapter:** [Week 36](../student-guide/week-36.md) · **Workbook:** [pages 36.1 to 36.4](../workbook/week-36.md) · **Two sittings:** 70 minutes with the computer (demo and card), and 75 minutes without (the final paper, on a different day).

**Open with the paper**, again: your 12 characters and the committed numbers. Run `python capstone34/eval/run_eval.py v1` (or the version you shipped). The last line must say `MATCH` before you say anything about your system.

## ☐ Milestone 7: the system card (written last, checked first)

**The card is made from the logs; it is not remembered.** Read every number into one dictionary from the files in `logs/`, and write the card so that **a number is a slot, not a typed digit**. Change the system, run it again, and the card changes with it.

Start from the **claim ledger** (workbook Page 36.1): one line per claim with the sentence, the number, the `n` and **the command that printed it**. A claim with no command does not go in the card.

`capstone34/SYSTEM_CARD.md` has **ten headings, in this order**:

| # | Heading | What makes it honest |
|:--:|---|---|
| 1 | Intended use | the person, and that it produces a **suggestion, not a decision** |
| 2 | Out of scope | each item with a reason, and what you measured for it |
| 3 | Measured numbers | **every row carries its `n`**: `8 of 9`, never a bare `0.89` |
| 4 | Failure modes | a **real input and the real wrong output**, quoted, not a disclaimer |
| 5 | Guardrails and red-team results | A1 to A5, with the misses |
| 6 | Retention | what the trace keeps and for how long, checked against your files |
| 7 | Staged release | headed *a plan; none of it has happened* |
| 8 | Incident response | detect, stop, tell, fix, re-test |
| 9 | Contact | who to tell |
| 10 | What it fails at, and who should not rely on it | **names a person**; contains a number and an `n` |

**The first lines say** that every dollar and millisecond is a stand-in from scripted stand-ins, not a model. **Five ways a card goes wrong without anybody noticing**, each with a check in the chapter (Section 5):

1. A number the logs do not hold.
2. A table row with a rate and no `n`.
3. A dollar or a millisecond with no *stand-in* label.
4. A disclaimer in place of a failure (*"may occasionally be inaccurate"* has no input, no wrong output, no number and no person).
5. A quoted wrong output that is **no longer what the system says**. Re-ask every one (Section 6) and compare the sentences.

Also check **what the card says about retention** against what your files really keep (Section 7).

> **🔑 Who the last section is for.** Section 10 is marked as heavily as your working code. The worked example says: *it fails at a near-miss question, a false premise, two facts in one question (0 of 4) and a number that needs rounding; and Asha should not rely on it whenever a number matters more than an afternoon, unless she opens the cited note first.* Yours names **your** user and **your** failures, with your numbers.

## ☐ Milestone 6: the five-minute demo (Section 8)

`capstone34/ask.py` takes one question and prints one answer. Here it is on the worked example (**stand-in, not a model**: it copies a sentence from a note, or follows a written plan):

```bash
python capstone34/ask.py "What is the capital of Peru?"
```

```text
I could not find this in the notes.
[route refuse | refused True | cites [] | stand-in $0.00000 | version v1.1]
stand-in, not a model: it copies one sentence from a note, or follows a written plan. Open the cited note before you trust a number.
```

`capstone34/demo.py` is the run-sheet: six segments whose seconds are fixed, `30 + 60 + 60 + 60 + 60 + 30 = 300`.

| Segment | Seconds | You show |
|---|:--:|---|
| Say it | 30 | who it is for, in one sentence |
| It works | 60 | one question that retrieves, and one that goes to your second component |
| The number | 60 | the per-category table, **read worst row first** |
| It fails | 60 | **one case that fails on purpose**, with its mechanism in one sentence |
| I attacked it | 60 | the attack that landed, before and after, with `n` |
| Who should not rely on it | 30 | your card's last section, **read aloud** |

**Choose three questions**: one that works, one that uses your second component and works, and **one that fails** (ideally the near-miss or the false premise from your red-team pass). A demo that shows no failure is not allowed; a demo of the cases that work measures how well you chose them. Rehearse once against a timer. Save the recording:

```bash
python capstone34/demo.py > capstone34/logs/demo_backup.txt
```

If the laptop misbehaves, your teacher plays the recording and you carry on. It is **said to be a recording.** Say the stand-in label aloud once: *every dollar and every millisecond here is a stand-in; none of it says anything about a real model.*

## ☐ The one-line test

After the demo your teacher picks a wrong answer from your own log and asks:

> *"Here is a wrong answer. Was it retrieval, generation, the prompt, the tokenizer, or a person over-trusting it? Show me the evidence."*

**Evidence** is a file, a number or a quoted line, not an opinion: a list of fetched notes, a score, a row of `logs/eval_v1.json`. The fourth option, *a person over-trusting it*, is your card's last section. (If your system has no tokenizer in the path, say so: that is itself a fact.)

## ☐ Assessment 4

**75 marks, 75 minutes, on paper, no computer and no notes, on a different day.** Five sections: A (20 marks, multiple choice), B (16, short programs), C (12, bugs), D (15, arithmetic by hand) and E (12, reading two tables and saying what they can and cannot support). It covers Term 4, mostly Weeks 28 to 35. It is an X-ray, not a grade: partial working earns marks, and *did not get it* is worth more than a lucky guess. You mark it yourself in a different colour (Page 36.3) and fill in the per-week grid (Page 36.4).

**Evidence Week 36 is done:**

```bash
python gate.py 36                                   # the M6 and M7 lines say PASS
python capstone34/eval/run_eval.py v1               # the last line says MATCH
```

**Tidy up:** delete the scratch traces you made for the demo (`logs/*_trace.jsonl`). Keep `eval/`, `src/`, `DESIGN.md`, `RED_TEAM.md`, `SYSTEM_CARD.md`, `ask.py`, `demo.py` and the committed numbers.

---

# 📊 How It Is Marked

**Weights (provisional; the owner finalises them):**

| Row | Weight | What earns it |
|---|:--:|---|
| **Eval design** | 25 | a named user; cases typed from the user's side; a `hard` prediction written before the score; a scorer that was itself tested; a freeze while `src/` was empty, with the paper to prove it |
| **Measured evidence** | 25 | one command that re-runs and says `MATCH`; `n` on every row; baseline before spine; promises held against measurements; a regression reported by named cases |
| **Guardrails and red-team** | 20 | one attack per category, misses included, controls for every zero; one fix re-tested on the legitimate task; one acceptance with a real reason |
| **Honesty of the card** | 20 | every claim has a number and an `n`; a real wrong output quoted and still true; the last section names a person; `MISSED` where it was missed |
| **Demo** | 10 | five minutes, a failure shown on purpose, the stand-in label said aloud |

Assessment 4 is marked separately. The honest section (*what it fails at and who should not rely on it*) is marked as heavily as the working code.

---

# ✅ The Build Checklist

**Before Week 34 ends**

- [ ] A named person, and heading 2 of `DESIGN.md` says what they will do with an answer
- [ ] "A keyword search fails here because ..." finished honestly
- [ ] Heading 5 ranked by **severity**, worst first, each with a person who is harmed
- [ ] Heading 6 has a cost, a p95 and a score, each with a unit and the word *stand-in*
- [ ] 25 or more cases in six categories; 3 or more refusals; 2 or more `hard`
- [ ] `check_cases` and `check_shape` print `[]`; the scorer is tested on 8 answers you typed
- [ ] Frozen while `src/` was empty; the 12 characters are on paper, held by someone else
- [ ] A prediction on the paper: the category that will fail worst, and its number

**Before Week 35 ends**

- [ ] Baseline scored **before** the spine; the card guess written before that
- [ ] `run_eval.py` prints a table with `n` on every row and ends in `MATCH`
- [ ] Promises vs measurements, each `kept` or `MISSED`
- [ ] Every failing case has a one-word verdict for where the chain broke
- [ ] `RED_TEAM.md`: five rows, a control for every zero, one `FIXED` with a re-test count, one `ACCEPTED` with a reason
- [ ] One regression reported by named cases

**Before Week 36 ends**

- [ ] The 12 characters still match; the last line of the eval says `MATCH`
- [ ] `SYSTEM_CARD.md`: ten headings, `check_card` prints `[]`, the quoted wrong outputs still hold
- [ ] A demo that shows one failure, under five minutes, with the stand-in label said aloud
- [ ] `logs/demo_backup.txt` exists and is described as a recording
- [ ] The one-line test answered with a file, a number or a quoted line
- [ ] `python gate.py 36` says every check passed

---

# ⚠️ Eight Mistakes That Cost the Most Marks

1. **Writing `src/` before the freeze.** `freeze()` refuses, and if you work around it you have no freeze at all.
2. **Editing a case after seeing the score**, then re-freezing. (Break It On Purpose D1 and D2.)
3. **Writing the question from the answer.** A test built from the answer key is a mirror.
4. **A bare rate.** `0.89` on 9 cases and `0.89` on 900 are different claims.
5. **A zero with no control.** A test that cannot fail does not show that the defence works.
6. **A fix that breaks the product.** The attack goes to zero and so does the legitimate task.
7. **Turning `DIFFER` green with `--commit`.**
8. **A disclaimer instead of a failure.** *"May occasionally be inaccurate"* names nothing. Quote the input and the wrong output.

---

# 🚀 Stretch Directions (only after every box above is ticked)

- **A seventh category** of your own (for example `pii`), with two cases and a sentence on how it is scored. Freeze it in `eval/cases_extra.py` with **its own fingerprint**, so the frozen 25 stay untouched.
- **The legitimate save as its own case**, in `eval/cases_extra.py`, so that a "fix" that forbids every write fails the suite.
- **Generate your card from the logs** with a program, so that it is rewritten whenever the system changes.
- **Split a two-part question** at `", and "`, answer each half and join them as a new version `v3`. Write down **before** running which `multi_hop` cases you expect it to rescue, and report the categories it does *not* help.

---

# 🔑 What This Capstone Is Really About

1. **The test is written before the thing it tests.** Otherwise it is a mirror.
2. **A claim has a number and an `n`, or it is a mood.**
3. **The baseline comes first.** "Better than what?" needs an answer before the clever part exists.
4. **A number is only a result if one command prints it and a second run prints the same.**
5. **A gain of one or two cases is smaller than the wobble.** A whole category moving, with the failing cases named, is a finding.
6. **A miss is evidence.** Log the attacks that failed.
7. **The card is made from the logs; it is not remembered.**
8. **The last section is the one that gets read.**

---

# 🎓 You Have Finished Level 4

**There is no Week 37.** The habit that matters more than any single week is the one in the card: *say what you measured, on how many cases, and what it cannot tell you.* If you ask what to build next, here is the question to answer first:

> *What is the claim I would most like to be able to make, and what is the smallest test, written before I build, that would let me make it honestly?*

[⬅ Course Home](../README.md) · [The reference capstone](../../capstone.md)

```
  ██╗     ███████╗██╗   ██╗███████╗██╗       ██████╗
  ██║     ██╔════╝██║   ██║██╔════╝██║       ╚════██╗
  ██║     █████╗  ██║   ██║█████╗  ██║        █████╔╝
  ██║     ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║       ██╔═══╝
  ███████╗███████╗ ╚████╔╝ ███████╗███████╗  ███████╗
  ╚══════╝╚══════╝  ╚═══╝  ╚══════╝╚══════╝  ╚══════╝

  ██████╗  ██╗   ██╗██╗██╗     ██████╗ ███████╗██████╗
  ██╔══██╗ ██║   ██║██║██║     ██╔══██╗██╔════╝██╔══██╗
  ██████╔╝ ██║   ██║██║██║     ██║  ██║█████╗  ██████╔╝
  ██╔══██╗ ██║   ██║██║██║     ██║  ██║██╔══╝  ██╔══██╗
  ██████╔╝ ╚██████╔╝██║███████╗██████╔╝███████╗██║  ██║
  ╚═════╝   ╚═════╝ ╚═╝╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝
```

# 🔨 Level 2 — Builder

### *If you can write code, you can turn a table of data into a model that predicts.*

**Grade band:** 7–8 (ages ~12–14) · **Coding required:** none to start — this level teaches it · **Math required:** arithmetic, fractions, percentages, `y = mx + c`
**Duration:** ~20 weeks · 9 modules (~3.5–4.5 h each) + a ~10 h capstone · **~44 hours total**

[⬅ Level 1](../level-1-explorer/) · [Back to AI Academy](../../README.md) · [Full curriculum map](../../CURRICULUM_MAP.md) · [Level 3 ➡](../level-3-engineer/)

---

## 🪝 Why This Level Exists

In Level 1 you trained a model by dragging photos into a browser tab. It worked. You measured it honestly. And then you hit the wall that every no-code tool has: **you could not ask it a question it wasn't built to answer.**

You couldn't say "show me only the photos taken after 6 p.m." You couldn't say "what if I trained on half the data?" You couldn't say "try it again with a different model and put the two scores in one table." Every one of those is a sentence, and a sentence needs a language.

Python is that language. And here is the honest shape of this level, so you know what you're signing up for:

```
   Modules 1–4  ·  You learn to talk to a computer.        (no AI yet — on purpose)
   Modules 5–7  ·  You learn to push data around fast.     (numpy, pandas, charts)
   Modules 8–9  ·  You train real models — three lines.    (and the split that makes them honest)
```

Notice how late the models arrive. That's not a mistake in the ordering. **A model is genuinely three lines of code.** `fit`, `predict`, `score`. The reason machine learning is hard is that those three lines sit on top of a table you had to build, clean, understand, and split — and that's Modules 1 through 7.

By the end you will have written a program from a blank file, cleaned a deliberately broken 40-row table and logged every fix, drawn a chart that lies and the honest version next to it, and produced the single most important graph in machine learning: the one where your training score climbs while your test score falls off a cliff.

---

## 🎯 Level Outcomes

When you finish Level 2 you will be able to:

1. **Write a Python program from a blank file** using variables, conditionals, loops, functions, lists, and dictionaries — and read a traceback instead of panicking at it.
2. **Load, clean, filter, and group a real table with pandas**, repairing missing values and wrong dtypes, with a written cleaning log that says *why* for every change.
3. **Do array math with numpy without writing a loop**, including broadcasting and boolean masks.
4. **Build five labelled matplotlib charts** that answer a stated question — and spot the trick in a misleading one.
5. **Train kNN, decision tree, and linear regression models with scikit-learn** using a proper train/test split.
6. **Measure accuracy, MAE, and R²**, and demonstrate overfitting with your own train-score vs test-score gap.

> **The one-line test of whether you finished this level:** somebody hands you a CSV and a question, and you can go from file to defensible answer without asking anyone what to type next.

---

## 🎒 What You Need Before Starting

### Prerequisites — the honest list

| You need | Why | If you don't have it |
|---|---|---|
| **Level 1 finished**, or the ideas in it | Modules 8–9 assume you already believe in held-out test sets | Read [Level 1 Module 6](../level-1-explorer/module-06-train-test-trust.md) at minimum. Do not skip it. |
| Comfort with fractions and percentages | Accuracy, R², and normalization are all division | Level 1 Module 6 re-teaches it |
| `y = mx + c` — or willingness to meet it | Module 9's linear regression is exactly this | Module 9 rebuilds it from a scatter plot; no algebra class needed |
| To be able to type accurately | Python cares about every bracket, colon, and space | Module 1 makes you type by hand, not paste. That's the drill. |
| A computer you can install software on | This level installs Python | Ask the adult who owns it *before* week 1 |
| Patience with error messages | You will see hundreds | Module 1 spends a whole section on reading them calmly |
| **No prior programming** | Module 1 starts at `print("hello")` | — |

### The kit

```
   ┌──────────────────────────────────────────────────────────────────┐
   │  THE LEVEL 2 KIT                                                 │
   ├──────────────────────────────────────────────────────────────────┤
   │  □  A laptop or desktop you can install Python on                │
   │     (any OS: macOS, Windows, or Linux — all three work)          │
   │  □  ~4 GB free disk space (Python + the four libraries)          │
   │  □  Internet, at least once, to download the libraries           │
   │  □  A notebook and pen — still. You will hand-check arithmetic   │
   │     in every single module, and screens are bad at that.         │
   │  □  A folder called ai-academy/level2 that you never delete      │
   └──────────────────────────────────────────────────────────────────┘
```

> ⚠️ **A grown-up should read this bit.** Nothing in Level 2 uploads data anywhere. Every dataset is either typed out in the file, generated by the code, or built into scikit-learn and downloaded once. There are no accounts, no API keys, and no cloud services in this entire level. The only network access needed is `pip install` at setup.

---

## 🗺️ The Roadmap

```
              LEVEL 2 · BUILDER — from print("hi") to an overfitting curve

   PART ONE — THE LANGUAGE  (no data science yet, and that is deliberate)
   ┌───────────────────┐      ┌───────────────────┐      ┌───────────────────┐
   │  1. PYTHON FROM   │      │  2. DECISIONS &   │      │  3. FUNCTIONS &   │
   │     ZERO          │─────►│     LOOPS         │─────►│     LISTS         │
   │                   │      │                   │      │                   │
   │  print · variables│      │  if/elif/else     │      │  def · return     │
   │  str int float    │      │  and/or/not       │      │  scope · lists    │
   │  bool · f-strings │      │  for · while      │      │  slicing          │
   │  tracebacks       │      │  accumulators     │      │  comprehensions   │
   └───────────────────┘      └───────────────────┘      └─────────┬─────────┘
      "computers are                                                │
       literal, not smart"                                          │ many values,
                                                                    │ one name
                                                                    ▼
   PART TWO — THE DATA                                    ┌───────────────────┐
   ┌───────────────────┐      ┌───────────────────┐       │  4. DICTIONARIES  │
   │  6. PANDAS        │◄─────│  5. NUMPY         │◄──────│     & DATASETS    │
   │                   │      │                   │       │                   │
   │  DataFrame · loc  │      │  arrays · shape   │       │  keys & values    │
   │  isna · fillna    │      │  broadcasting     │       │  list-of-dicts    │
   │  astype · groupby │      │  axis=0 vs axis=1 │       │  = your first     │
   │  the cleaning log │      │  boolean masks    │       │    dataset        │
   └─────────┬─────────┘      └───────────────────┘       │  CSV round trip   │
             │                                             └───────────────────┘
             │  a clean table
             ▼
   ┌───────────────────┐
   │  7. CHARTS THAT   │      PART THREE — THE MODELS
   │     TELL THE TRUTH│      ┌───────────────────┐      ┌───────────────────┐
   │                   │─────►│  8. FIRST MODEL:  │─────►│  9. TREES, LINES, │
   │  line bar scatter │      │     kNN           │      │     OVERFITTING   │
   │  histogram box    │      │                   │      │                   │
   │  truncated axes   │      │  ⚡ X and y       │      │  trees → rules    │
   │  r ≠ cause        │      │  fit/predict/score│      │  MAE · RMSE · R²  │
   └───────────────────┘      │  train_test_split │      │  the train/test   │
                              │  scaling · k      │      │    gap, drawn     │
                              └───────────────────┘      └─────────┬─────────┘
                                                                   │
                                                                   ▼
                          ╔══════════════════════════════════════════════════╗
                          ║   🔎  CAPSTONE — DATA DETECTIVE  (~10 h)         ║
                          ║                                                  ║
                          ║   your question · 100+ rows you collected        ║
                          ║   · a cleaning log · five charts · three models  ║
                          ║   on one honest split · a results table · and    ║
                          ║   a section titled "what I got wrong"            ║
                          ╚══════════════════════════════════════════════════╝
```

**Read the arrows as "you need this before that."** Module 3's lists become Module 5's arrays. Module 4's list-of-dicts becomes Module 6's DataFrame. Module 6's clean table becomes Module 7's charts and Module 8's `X`. Nothing here is optional scaffolding — every module is load-bearing for the one after it.

---

## 📚 The Nine Modules

| # | Module | You'll build | Time |
|:--:|---|---|:--:|
| 1 | [**Python From Zero: Variables, Types, and Talking to the Computer**](module-01-python-from-zero.md) | 🤖 **About-Me Bot** — asks 6 questions, converts the answers, computes two derived numbers, prints a formatted profile card. Every line commented. | ~3 h |
| 2 | [**Decisions and Loops: Programs That Choose and Repeat**](module-02-decisions-and-loops.md) | 🎲 **Guess & Grade** — a number-guessing game with hints, a 7-attempt limit and a replay loop, plus a grade calculator with total/average/highest/letter | ~3.5 h |
| 3 | [**Functions and Lists: Building Your Own Tools**](module-03-functions-and-lists.md) | 🧰 **Stats Toolkit** — your own `stats.py` with mean, median, min, max and range, imported by a `main.py` that reports on 20 cricket scores | ~3.5 h |
| 4 | [**Dictionaries and Datasets: Your First Data in Code**](module-04-dictionaries-and-datasets.md) | 🗃️ **Record Store** — a 30-record dataset with 5 keys, `filter_by()` and `group_count()`, written to CSV and loaded back with the round trip proved | ~4 h |
| 5 | [**NumPy: Thinking in Arrays**](module-05-numpy-arrays.md) | ⚡ **Vectorized Gradebook** — a 10×5 score array, per-student and per-test means, the hardest test, 0–1 normalization and a pass/fail mask, with **zero** for loops | ~4 h |
| 6 | [**Pandas: Loading, Cleaning, and Interrogating a Table**](module-06-pandas-tables.md) | 🔍 **Mess Detective** — clean a deliberately broken 40-row table (missing ages, `'12'` as text, duplicates, four spellings of one house) and answer 6 `groupby` questions | ~4 h |
| 7 | [**Charts That Tell The Truth: Visualization With Matplotlib**](module-07-visualizing-data.md) | 📊 **Five-Chart Data Story** — five fully labelled charts in narrative order, plus one deliberately misleading chart beside its honest fix | ~3.5 h |
| 8 | [**Your First Real Model: k-Nearest Neighbors and the Train/Test Rule**](module-08-first-model-knn.md) | 🎯 **Classifier Lab** — kNN on a built-in dataset with and without scaling, an accuracy-vs-`k` plot for k = 1…25, and a chosen `k` with a written reason | ~4 h |
| 9 | [**Trees, Lines, and the Overfitting Trap**](module-09-trees-lines-and-overfitting.md) | 🏆 **Model Bake-Off** — kNN vs tree vs linear regression on one fixed split, plus the train/test curve against depth 1–15 with the overfitting point marked | ~4.5 h |
| 🔎 | [**CAPSTONE — Data Detective**](capstone.md) | 📓 One notebook that reads as a story: question → 100+ rows → cleaning log → five charts → three models → results table → "what I got wrong" | ~10 h |

**Also in this folder:**

| File | What it's for | When to use it |
|---|---|---|
| [`assessment.md`](assessment.md) | 20 multiple-choice + 8 short-answer + 4 debug problems, with an explained answer key for every single item | After Module 9, before the capstone |
| [`glossary.md`](glossary.md) | Every term in this level — 217 of them — alphabetized, with a plain definition and the example from the course | Any time a word stops making sense |
| [`capstone.md`](capstone.md) | The final build: brief, milestones, scaffold, worked solution for the hardest part, rubric | Weeks 16–20 |

---

## 🧭 How This Level Fits the Whole Journey

### What Level 1 gave you

Level 1 was not a warm-up. Every idea in it gets a keyboard in this level, and here is the exact mapping:

```
   ┌──────────────────────────────────────────────────────────────────────────┐
   │  LEVEL 1 IDEA  (done by hand)      ─►   LEVEL 2 SPELLING  (typed)        │
   ├──────────────────────────────────────────────────────────────────────────┤
   │  a table of rows and columns       ─►   pd.DataFrame(...)          M6    │
   │  an index card per example         ─►   a dict, then a row         M4    │
   │  features and a label column       ─►   X and y                    M8    │
   │  "hide 20% before you train"       ─►   train_test_split(0.2)      M8    │
   │  accuracy = correct ÷ total        ─►   accuracy_score(y, pred)    M8    │
   │  a hand-drawn confusion matrix     ─►   confusion_matrix(...)      M8    │
   │  "it memorized instead of learned" ─►   the train/test gap         M9    │
   │  a data card                       ─►   a cleaning log + README    M6    │
   │  "which chart is that person       ─►   a truncated y-axis, named  M7    │
   │   using to fool me?"                    and repaired                     │
   └──────────────────────────────────────────────────────────────────────────┘
```

If you did Level 1 properly, **not one idea in that right-hand column is new.** You are learning spellings, not concepts. That is why Level 2 feels fast in Modules 8 and 9 and slow in Modules 1 to 4 — the slow part is the typing, not the thinking.

If you skipped Level 1: you can survive, but do [Level 1 Module 6 — Train, Test, Trust](../level-1-explorer/module-06-train-test-trust.md) before you reach Module 8 here. Otherwise `train_test_split` is a magic incantation, and memorized incantations are exactly what this academy exists to prevent.

### What Level 3 needs from you

Level 3 (**Engineer**, grades 9–10) builds gradient descent by hand, writes a neural network in raw numpy, and then moves to PyTorch. It will assume — without re-teaching — that you can do all of this **cold**:

| Level 3 will say... | ...and expect you to already own | From |
|---|---|---|
| "the design matrix `X` of shape `(n, d)`" | array shapes, `axis=0` vs `axis=1`, broadcasting | M5 |
| "engineer a feature from this column" | pandas derived columns and `groupby` | M6 |
| "plot the loss curve" | a labelled matplotlib figure with axes and a legend | M7 |
| "never fit the scaler before the split" | leakage, and why it inflates your score | M8 |
| "this model is overfitting — regularize it" | the train/test gap as a *number* you have produced yourself | M9 |
| "write a function that takes a model and returns metrics" | `def`, parameters, `return`, importing your own module | M3 |
| "the gradient is a vector of partial derivatives" | that a row of numbers *is* a vector, and dot products | M5 |

Notice what is *not* on that list: any maths past algebra. Level 3 adds the calculus intuition itself. What it cannot add is fluency at the keyboard — that is this level's entire job.

> **The one-sentence handover:** Level 1 gives you the *concepts* with your hands; **Level 2 gives you the keyboard**; Level 3 gives you the maths under the hood; Level 4 gives you the frontier.

---

## 🔧 Environment Setup

Unlike Level 1, this level installs software. Budget **45 minutes**, do it in one sitting, and do it in **week 0 — before Module 1**. Setup problems in week 6 feel like failure. Setup problems in week 0 are just setup.

### Step 1 — Install Python 3.11 or newer (15 min)

First, check whether you already have it. Open a terminal — **macOS:** the Terminal app · **Windows:** PowerShell · **Linux:** your terminal — and type:

```bash
python3 --version
```

| What you see | What to do |
|---|---|
| `Python 3.11.x` or higher | ✅ You're done with this step. |
| `Python 3.9.x` or `3.10.x` | ✅ Fine for this whole level. Everything here runs on 3.9+. |
| `Python 2.7.x` | ❌ Ancient. Install a new one; do not remove the old one (your OS may need it). |
| `command not found` | Try `python --version`. If that also fails, install below. |

Download the installer from **[python.org/downloads](https://www.python.org/downloads/)**.

> ⚠️ **Windows users, the single most important click in this level:** on the first screen of the installer, tick **"Add python.exe to PATH"** before pressing Install. Leaving it unticked causes about 90% of Windows setup pain, and the symptom (`'python' is not recognized`) does not mention PATH at all.

> ⚠️ **macOS users:** the `python3` that ships with macOS is fine to *check* with, but install a real one from python.org (or `brew install python@3.12`). The system one is missing pieces and Apple can change it in an OS update.

### Step 2 — Make a folder and a virtual environment (10 min)

> **Definition — virtual environment:** a private box of Python libraries that belongs to one project. Install into the box, and you can never break another project — or your operating system — by upgrading something.

```bash
# 1) One folder for the entire level. Never delete this.
mkdir -p ~/ai-academy/level2
cd ~/ai-academy/level2

# 2) Create the private box (this makes a hidden .venv folder)
python3 -m venv .venv

# 3) Step INTO the box
source .venv/bin/activate          # macOS / Linux
.venv\Scripts\activate             # Windows PowerShell
```

After step 3 your prompt changes to start with `(.venv)`. **That prefix is the whole game.** If you don't see it, you are not in the box, and everything you install lands in the wrong place.

```
   ┌─────────────────────────────────────────────────────────────────────┐
   │  (.venv) rkamma@laptop level2 %                                     │
   │   ▲▲▲▲▲▲                                                            │
   │   this. every single time you open a new terminal, you must run     │
   │   the activate line again. It does not stick between sessions.      │
   └─────────────────────────────────────────────────────────────────────┘
```

### Step 3 — Install the four libraries (10 min)

```bash
pip install --upgrade pip
pip install numpy pandas matplotlib scikit-learn jupyterlab
```

That downloads about 300 MB and takes 2–5 minutes. What you just installed, and when you first need it:

| Package | What it does | First used |
|---|---|---|
| `numpy` | Fast arrays and array maths | Module 5 |
| `pandas` | Named, cleanable tables (DataFrames) | Module 6 |
| `matplotlib` | Charts | Module 7 |
| `scikit-learn` (imports as `sklearn`) | Models, splits, metrics, built-in datasets | Module 8 |
| `jupyterlab` | Notebooks — optional for modules, **used by the capstone** | Capstone |

Minimum versions that this level's outputs were checked against: `numpy 1.24+`, `pandas 1.5+` (2.x also fine), `matplotlib 3.6+`, `scikit-learn 1.2+`. Newer is fine; the modules flag the two places where pandas 2.x prints a slightly different header.

### Step 4 — The 3-line smoke test (2 min)

Create a file called `smoke.py` in `~/ai-academy/level2` and type these three lines:

```python
import numpy, pandas, matplotlib, sklearn
from sklearn.datasets import load_iris
print("Level 2 ready ·", numpy.__version__, pandas.__version__, sklearn.__version__, load_iris().data.shape)
```

Run it:

```bash
python smoke.py
```

```
   ┌─────────────────────────────────────────────────────────────────────┐
   │  🔥 LEVEL 2 SMOKE TEST                                              │
   ├─────────────────────────────────────────────────────────────────────┤
   │                                                                     │
   │  ✅ PASS looks like:                                                │
   │       Level 2 ready · 1.26.4 1.5.3 1.4.2 (150, 4)                   │
   │       (your version numbers will differ — that's fine)              │
   │                                                                     │
   │  ❌ FAIL looks like:                                                │
   │       ModuleNotFoundError: No module named 'pandas'                 │
   │       → see troubleshooting row 2. It is almost always the venv.    │
   └─────────────────────────────────────────────────────────────────────┘
```

That `(150, 4)` is real: 150 iris flowers, 4 measurements each. You just loaded your first dataset, and you haven't reached Module 1 yet.

### Step 5 — Prove a chart can appear (5 min)

Charts fail differently from everything else, so test them separately. Create `smoke_plot.py`:

```python
import matplotlib.pyplot as plt                 # the standard nickname

fig, ax = plt.subplots(figsize=(5, 3))          # one figure, one drawing box
ax.plot([1, 2, 3, 4], [2, 4, 8, 16], marker="o")  # four points, joined
ax.set_title("If you can read this, matplotlib works")
ax.set_xlabel("week")
ax.set_ylabel("pizzas eaten")
fig.savefig("smoke_plot.png", dpi=120, bbox_inches="tight")   # always save
plt.show()                                       # try to pop a window too
```

```bash
python smoke_plot.py
```

**Two possible passes, and both are fine:**

1. A window pops up with a rising line. Perfect.
2. No window appears, but a file called `smoke_plot.png` shows up in the folder. Also perfect — your setup just has no window system. Every chart in Module 7 uses `savefig`, exactly so this never blocks you.

**Only a fail if neither happens.** Check the terminal for an error and see troubleshooting row 4.

### Step 6 — Pick an editor (5 min)

| Option | Get it | Best for |
|---|---|---|
| **VS Code** ✅ recommended | [code.visualstudio.com](https://code.visualstudio.com/), then install the **Python** extension by Microsoft | Modules 1–9. Colours, error squiggles, a ▷ Run button. |
| **JupyterLab** | already installed — run `jupyter lab` | The capstone, where you want charts and prose in one document |
| **IDLE** | ships with Python | A fallback if the other two won't install. It works. |

In VS Code: **File → Open Folder →** pick `ai-academy/level2`. Then press `Ctrl+Shift+P` → type "Python: Select Interpreter" → choose the one with **`.venv`** in its path. Skipping that last click is troubleshooting row 2 waiting to happen.

### ✅ Setup complete checklist

- [ ] `python3 --version` prints 3.9 or higher
- [ ] `~/ai-academy/level2` exists and contains a `.venv` folder
- [ ] My prompt shows `(.venv)` after I run the activate line
- [ ] `python smoke.py` prints `Level 2 ready ... (150, 4)`
- [ ] `python smoke_plot.py` produces a window **or** a `smoke_plot.png` file
- [ ] VS Code is open on the `level2` folder with the `.venv` interpreter selected
- [ ] I have written the activate command on a sticky note, because I will need it every session

---

## 🚑 Troubleshooting — the five things that actually go wrong

| # | Symptom | Most likely cause | Fix |
|:--:|---|---|---|
| 1 | `python: command not found`, or on Windows typing `python` **opens the Microsoft Store** | Python isn't installed, or the installer's "Add to PATH" box was left unticked, or Windows' fake `python.exe` alias is intercepting you | Try `python3`, then `py -3` (Windows only). If none work: re-run the python.org installer, choose **Modify → Add to PATH**, and restart the terminal — PATH changes only apply to *new* terminals. On Windows also go to *Settings → Apps → Advanced app settings → App execution aliases* and switch **off** the two "App Installer python.exe" toggles. |
| 2 | `ModuleNotFoundError: No module named 'pandas'` — **even though pip said it installed fine** | You installed into one Python and are running a different one. Ninety percent of the time: the venv was not activated, or VS Code is using the system interpreter. | Prove which Python you're using: `python -c "import sys; print(sys.executable)"`. The path **must** contain `.venv`. If it doesn't: run the activate line again (`source .venv/bin/activate`), and in VS Code hit `Ctrl+Shift+P` → *Python: Select Interpreter* → pick the `.venv` one. Belt and braces: install with `python -m pip install pandas` instead of bare `pip` — that guarantees the pip that belongs to the Python you're actually running. |
| 3 | `error: externally-managed-environment` when you `pip install` | Modern macOS (Homebrew) and Debian/Ubuntu **refuse** to let pip install into the system Python, to stop you breaking your OS | This error is your friend — it means you skipped the venv. Do Step 2, activate, and try again. Do **not** use the `--break-system-packages` flag the error suggests, however tempting; it does exactly what it says on the tin. |
| 4 | `plt.show()` runs and **nothing appears**, or `UserWarning: FigureCanvasAgg is non-interactive` | No GUI backend — common on plain Linux, over SSH, in WSL, or in a bare terminal | Not a real problem. Always call `fig.savefig("name.png", dpi=120, bbox_inches="tight")` and open the PNG. Every chart in Module 7 does this. If you *want* windows on Linux: `sudo apt install python3-tk`. In VS Code, running the file in the **Interactive Window** or a notebook shows charts inline. |
| 5 | `ImportError: numpy.core.multiarray failed to import`, or `ValueError: numpy.dtype size changed` | Mismatched binaries — usually pandas or scikit-learn was built against numpy 1.x and numpy 2.x got installed underneath it | Reinstall the set together so pip resolves compatible versions: `pip install --upgrade --force-reinstall numpy pandas scikit-learn`. If it persists, pin numpy: `pip install "numpy<2"`. The nuclear option always works: delete the `.venv` folder and redo Steps 2–3. That is *why* you use a venv — throwing it away costs three minutes and breaks nothing else. |

**Three more, less common but maddening:**

| # | Symptom | Fix |
|:--:|---|---|
| 6 | `IndentationError: unexpected indent` on a line that looks fine | You mixed tabs and spaces. In VS Code: bottom-right status bar → click **Spaces: 4** → *Convert Indentation to Spaces*. Then set *Editor: Insert Spaces* to on, forever. |
| 7 | `pip` fails with `SSL: CERTIFICATE_VERIFY_FAILED` | Usually a school or office network doing traffic inspection. On macOS, run the *"Install Certificates.command"* file inside `/Applications/Python 3.x/`. On a school network, try a home network or a phone hotspot for the one-time install. |
| 8 | You named a file `random.py`, `csv.py`, `statistics.py` or `numpy.py` and now imports break in strange ways | Python finds *your* file before the real library. Rename your file (`my_random.py`), and delete the `__pycache__` folder next to it. Module 3 warns about this; it still catches everybody once. |

---

## 📅 Weekly Pacing

Twenty weeks at about **2–2.5 hours a week**, in three or four short sittings rather than one long one. Code needs overnight to settle just like ideas do — the number of bugs that solve themselves on the walk to school is genuinely surprising.

### The weekly rhythm

```
   ┌──────┬──────────┬────────────────────────────────────────────────────┐
   │ DAY  │  TIME    │  WHAT YOU DO                                       │
   ├──────┼──────────┼────────────────────────────────────────────────────┤
   │ MON  │  ~35 min │  🪝 Hook + 🧠 Concept                              │
   │      │          │  Read at the keyboard. Type every snippet, even    │
   │      │          │  the three-line ones. Do not paste.                │
   ├──────┼──────────┼────────────────────────────────────────────────────┤
   │ WED  │  ~40 min │  🔍 Worked Example + 💻 Hands-On                   │
   │      │          │  Before you press Run: write down what you think   │
   │      │          │  the output will be. Then check. Every time.       │
   ├──────┼──────────┼────────────────────────────────────────────────────┤
   │ FRI  │  ~35 min │  ✍️ Practice (all 6) + ⚠️ Common Mistakes          │
   │      │          │  Struggle 15 minutes before opening the answer     │
   │      │          │  key. The struggle IS the lesson.                  │
   ├──────┼──────────┼────────────────────────────────────────────────────┤
   │ SAT  │  ~45 min │  🛠️ Mini-Project + 📓 Vocabulary                   │
   │      │          │  Build the thing. Then read your own code out      │
   │      │          │  loud to someone, line by line.                    │
   └──────┴──────────┴────────────────────────────────────────────────────┘
```

### The twenty weeks

| Week | Focus | Hand in at the end of the week |
|:--:|---|---|
| **0** | 🔧 **Setup** (above) | Both smoke tests pass; a screenshot of the `(.venv)` prompt |
| **1** | [M1](module-01-python-from-zero.md) — Python From Zero | `about_me.py` running, every line commented |
| **2** | [M2](module-02-decisions-and-loops.md) — Decisions and Loops | `guess.py` + `grade.py`, both surviving bad input |
| **3** | [M3](module-03-functions-and-lists.md) — Functions and Lists | `stats.py` + `main.py`, median correct for even *and* odd lengths |
| **4** | [M4](module-04-dictionaries-and-datasets.md) — Dictionaries and Datasets | 30 records, `filter_by`, `group_count`, CSV round trip proved |
| **5** | 🧱 **Python checkpoint** — no new module | Redo M1–M4 mini-projects from memory; take assessment Q1–Q9 |
| **6** | [M5](module-05-numpy-arrays.md) — NumPy | Vectorized Gradebook, zero for loops, hand-checked row 1 |
| **7** | [M6](module-06-pandas-tables.md) part 1 — concept + hands-on | `loc`/`iloc` drills, a cleaned toy table |
| **8** | [M6](module-06-pandas-tables.md) part 2 — Mess Detective | Before/after shape, a written cleaning log, 6 `groupby` answers |
| **9** | [M7](module-07-visualizing-data.md) — Charts That Tell The Truth | Five labelled PNGs + the lie-and-fix pair |
| **10** | 🧱 **Data checkpoint** — no new module | Re-clean the M6 table from scratch; take assessment Q10–Q14 |
| **11** | [M8](module-08-first-model-knn.md) part 1 — X, y, distance, split | Distance computed by hand on paper, then in code, matching |
| **12** | [M8](module-08-first-model-knn.md) part 2 — Classifier Lab | Accuracy-vs-k plot, scaled/unscaled table, chosen `k` + reason |
| **13** | [M9](module-09-trees-lines-and-overfitting.md) part 1 — trees and lines | Tree rules read out loud; slope + intercept in real units |
| **14** | [M9](module-09-trees-lines-and-overfitting.md) part 2 — Model Bake-Off | Comparison table + depth curve with the overfitting point marked |
| **15** | 📝 **[Assessment](assessment.md)** | All 20 MCQ + 8 short answer + 4 debug, then read every explanation |
| **16** | 🔎 [Capstone](capstone.md) M1–M2 | Question locked, 100+ rows collected, raw file saved untouched |
| **17** | 🔎 [Capstone](capstone.md) M3 | Clean data + a numbered cleaning log with a reason per line |
| **18** | 🔎 [Capstone](capstone.md) M4 | Five charts with captions, in narrative order |
| **19** | 🔎 [Capstone](capstone.md) M5–M6 | Three models on one split, results table, "what I got wrong" |
| **20** | 🎤 **Present + review** | The notebook read top to bottom to a real human, out loud |

### Pacing variations

| If you have... | Do this |
|---|---|
| **~1 h/week** | Take 30 weeks. Split every module into a concept week and a project week, as weeks 7–8 do for M6. Never drop a mini-project — the capstone assumes all nine exist. |
| **~6 h/week (holidays)** | 10 weeks: one module every 4 days. But keep **M8 and M9 in different weeks**. M9 only bites if M8's 100%-on-training-data result has had time to feel like a victory first. |
| **A study partner** | Add a 30-minute Sunday call where you read each other's code out loud. From M6 on, swap datasets: clean someone else's mess and see how many of your assumptions were wrong. |
| **A school term structure** | Weeks 1–14 as lessons, week 15 as the assessment, 16–20 as a project block ending in a Data Detective showcase where everyone presents one notebook. |
| **You already know Python** | Sit the assessment's Q1–Q9 and the two debug problems for M1–M4 *first*. Score 100% and you may compress Modules 1–4 into two weeks of mini-projects only. Score less, and you found your gap — do the modules. |

### ⚠️ Three pacing rules that matter more than the schedule

1. **Type the code. Do not paste it.** Your fingers have to learn where the colons and brackets go, and pasted code teaches them nothing. This costs you about 20 extra minutes a week and is the highest-return 20 minutes in the level.
2. **Never skip the checkpoint weeks (5 and 10).** They look like slack. They are the weeks where Modules 1–4 stop being "things I followed" and become "things I can do". A learner who skips week 5 hits Module 6 and discovers they cannot write a `for` loop without looking one up.
3. **If you fall behind, drop the [Stretch] exercises and the "level it up" extensions — never the mini-projects.** The capstone assumes you have a cleaning log habit from M6, five-chart fluency from M7, and a working split from M8.

---

## 🧾 The Level 2 Promise

Twenty weeks from now, someone will send you a spreadsheet and ask you what it says.

You will not open it in Excel and squint. You will load it in pandas, print `df.info()`, notice that the `age` column came in as `object` because three rows say `"unknown"`, fix it, log the fix, chart the distribution, notice the outlier, chase it down, and only *then* answer the question — with the number of rows stated, the uncertainty admitted, and a chart whose y-axis starts at zero.

And when someone says "can you make it predict?", you will say: *"Yes, but first I'm holding back 20% of these rows, and I'm going to tell you the score on those, not on the ones it learned from. The other number would be a lie."*

That sentence is the whole level.

---

## ▶️ Start Here

> ### 👉 **[Module 1 — Python From Zero: Variables, Types, and Talking to the Computer](module-01-python-from-zero.md)**
>
> It opens with a story about a computer that does exactly what you say, including the part you didn't mean.

---

[⬅ Level 1](../level-1-explorer/) · [Back to AI Academy](../../README.md) · [Curriculum map](../../CURRICULUM_MAP.md) · [Glossary](glossary.md) · [Assessment](assessment.md) · [Capstone](capstone.md) · [Level 3 ➡](../level-3-engineer/)

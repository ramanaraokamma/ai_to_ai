```
   █████╗ ██╗      █████╗  ██████╗ █████╗ ██████╗ ███████╗███╗   ███╗██╗   ██╗
  ██╔══██╗██║     ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝████╗ ████║╚██╗ ██╔╝
  ███████║██║     ███████║██║     ███████║██║  ██║█████╗  ██╔████╔██║ ╚████╔╝
  ██╔══██║██║     ██╔══██║██║     ██╔══██║██║  ██║██╔══╝  ██║╚██╔╝██║  ╚██╔╝
  ██║  ██║██║     ██║  ██║╚██████╗██║  ██║██████╔╝███████╗██║ ╚═╝ ██║   ██║
  ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝     ╚═╝   ╚═╝
```

# 🎓 AI Academy

**One learner. Four levels. Start in 6th grade with zero code — finish able to build real AI systems.**

**Two editions of the same course:** a **36-week taught course** with a teacher guide that assumes the
adult knows no AI, and **36 self-study modules** for a learner working alone.

> **The promise:** If you do every week in order and actually build the projects, you will go from
> "I've heard of AI" to "I trained that model, I evaluated it honestly, I shipped it, and I can
> explain exactly why it works."

---

## 🛤️ Two Ways Through This Course

Pick one. It decides which file you open every week. Same concepts, same order, same vocabulary —
the 36-week course was built *from* the modules, so you can switch tracks or read the modules as the
reference text alongside the weekly classes.

| | 🏫 **Taught Course** *(default)* | 🎒 **Self-Study Modules** |
|---|---|---|
| **For** | A learner with an adult — parent, teacher, tutor | A learner working alone |
| **Shape** | 36 weekly classes of 60–75 min | 36 modules, ~3.5 h/week |
| **Adult needs to know AI?** | **No** — every class is scripted | n/a |
| **Books per week** | Three: teacher guide · student guide · workbook | One: the module file |
| **Illustrated** | 1,140 hand-drawn SVG figures across three levels | ASCII diagrams |
| **Extras** | 4 term tests · 50 project ideas · worked exemplar · offline site | Capstone · assessment · glossary |
| **Available for** | **Levels 1, 2 and 3** | **All four levels** |
| **Enter at** | [`levels/level-1-explorer/36-week-course/`](levels/level-1-explorer/36-week-course/) | [`levels/level-1-explorer/README.md`](levels/level-1-explorer/README.md) |

> ⚠️ **Honest status:** the 36-week taught edition covers **Levels 1, 2 and 3** — three full school
> years, 108 weekly classes, ~452,000 lines. Level 4 is complete as self-study modules but has not
> been expanded into weekly classes yet.
>
> **Level 3 is offline by design.** `torchvision` is not required and no dataset downloads: image work
> uses `load_digits()` (ships with scikit-learn) and numpy-generated images. CIFAR-10 appears only as
> an optional "when you have internet" extension.

**New here? → [START_HERE.md](START_HERE.md)** picks your track in one page.

---

## 👋 Who This Is For

This course was written for **one person**: a curious learner who starts around age 11 (6th grade) and
grows with the material over roughly **2–3 years**.

| You need | You do **not** need |
|---|---|
| Curiosity and stubbornness | Any programming experience |
| Middle-school math: fractions, percentages, reading a graph | Algebra 2, calculus, or statistics (we build them when needed) |
| A computer with a browser | A powerful GPU, a paid course, or a teacher |
| ~3–5 hours a week | Permission from anyone |

**Three rules of this course:**

1. **No term is used before it is defined.** If you meet a word you don't know, it's a bug — go back one module.
2. **Every abstract idea lands on something real first** (pizza, cricket scores, spam texts, cat photos), *then* gets its formal name.
3. **Math comes after intuition**, never before, and always with a tiny worked number example.

---

## 🗺️ The Four-Level Map

| Level | Name | Grade | Big Idea | Modules | Time | You end up able to... |
|:--:|---|:--:|---|:--:|:--:|---|
| **1** | 🧭 **Explorer** | 6 | *Machines can learn from examples instead of being told rules* | 9 | **36 weeks taught** · ~12 weeks solo | Train an image classifier with no code, and explain training, testing, features, labels, and bias to an adult |
| **2** | 🔨 **Builder** | 7–8 | *If you can write code, you can turn data into predictions* | 9 | **36 weeks taught** · ~20 weeks solo | Write Python, wrangle data with pandas, plot it, and train + honestly test real scikit-learn models |
| **3** | ⚙️ **Engineer** | 9–10 | *A model is one part of a pipeline that must be measured and shipped* | 9 | **36 weeks taught** · ~24 weeks solo | Build the full supervised pipeline, code backprop from scratch, train CNNs in PyTorch, and ship a model |
| **4** | 🚀 **Innovator** | 11–12 | *Modern AI is attention + scale + a learning signal from humans* | 9 | ~28 weeks | Build a tiny GPT from scratch, and ship a RAG-grounded, tool-using, evaluated AI agent |

### ASCII Roadmap

```
                              ┌──────────────────────────┐
   START HERE  ───────────────►   LEVEL 1 · EXPLORER     │   grade 6 · no code
   (zero coding)              │   "What is learning?"     │   36 weeks taught
                              └───────────┬──────────────┘   (or ~12 weeks solo)
                                          │  unplugged · Teachable Machine
                                          │  Scratch · spreadsheets
                                          ▼
                              ┌──────────────────────────┐
                              │   LEVEL 2 · BUILDER      │   grades 7-8 · Python
                              │   "Code + data = model"  │   36 weeks taught
                              └───────────┬──────────────┘   (or ~20 weeks solo)
                                          │  python · numpy · pandas
                                          │  matplotlib · scikit-learn
                                          ▼
                              ┌──────────────────────────┐
                              │   LEVEL 3 · ENGINEER     │   grades 9-10 · pipelines
                              │   "Measure it. Ship it." │   36 weeks taught
                              └───────────┬──────────────┘   (or ~24 weeks solo)
                                          │  gradient descent · backprop
                                          │  PyTorch · CNNs · NLP
                                          ▼
                              ┌──────────────────────────┐
                              │   LEVEL 4 · INNOVATOR    │   grades 11-12 · frontier
                              │   "Build what's next"    │   ~28 weeks
                              └───────────┬──────────────┘
                                          │  transformers · LLMs · RAG
                                          │  agents · evals · safety
                                          ▼
                              ╔══════════════════════════╗
                              ║   You build real AI.     ║
                              ╚══════════════════════════╝

   THE SPIRAL — six ideas, revisited deeper at every single level:

        data ──► representation ──► model ──► learning signal ──► evaluation ──► human impact
          ▲                                                                            │
          └────────────────────────── next level, deeper ◄─────────────────────────────┘
```

---

## 🌀 The Spiral: Six Ideas, Four Passes

You never "finish" a topic here. You meet the same six ideas at every level, each time with more power.

| Core idea | Level 1 sounds like | Level 2 sounds like | Level 3 sounds like | Level 4 sounds like |
|---|---|---|---|---|
| **Data** | "A table of examples" | "Lists, dicts, DataFrames" | "Splits, leakage, distributions" | "Pretraining corpora, tokens at scale" |
| **Representation** | "Features describe things" | "Rows of numbers, arrays" | "Feature engineering, pixels, TF-IDF" | "Learned embeddings, attention vectors" |
| **Model** | "A box that guesses" | "kNN, trees, straight lines" | "Neurons, layers, convolutions" | "Transformers, LLMs, agents" |
| **Learning signal** | "Right and wrong examples" | "Fit the data better" | "Loss + gradient descent" | "Next-token loss, SFT, RLHF" |
| **Evaluation** | "Hide some examples and test" | "Train/test split, accuracy" | "Precision, recall, ROC, CV" | "Benchmarks, LLM evals, red-teaming" |
| **Human impact** | "Is it fair? Is it private?" | "Whose data is this?" | "Error costs, model cards" | "Alignment, misuse, safe deployment" |

*(The full 36-module map with every mini-project lives in [CURRICULUM_MAP.md](CURRICULUM_MAP.md).)*

---

## 📖 How To Use This Course

### 🏫 The weekly rhythm — Taught Course (Level 1)

One class a week, one homework, for 36 weeks. That is the whole system.

```
  NIGHT BEFORE   15-20 min   Teacher   "What YOU Need to Know First" + Prep Checklist.
                                       Do the worked example yourself, cold.
  THE CLASS      60-75 min   Both      Hook (8) → Concept (18) → Worked Example (14)
                                       → Activity (20) → Wrap & Assign (10)
  AFTER CLASS    20 min      Student   The student-guide chapter re-tells the lesson.
  HOMEWORK       45-60 min   Student   The workbook, self-marked from its answer key.
  BEFORE NEXT    5 min       Teacher   Skim the answers + next week's prep note.
  ────────────────────────────────────────────────────────────────────────────────
       36 weeks · four 9-week terms · weeks 34-36 are the capstone
```

**The three books mirror each other every week.** Never hand the student the teacher guide — it holds
every answer, and it also names the mistakes they're expected to make.

| Book | Who reads it | When |
|---|---|---|
| [`teacher-guide/week-NN.md`](levels/level-1-explorer/36-week-course/teacher-guide/) | The adult | Night before class |
| [`student-guide/week-NN.md`](levels/level-1-explorer/36-week-course/student-guide/) | The student | After class |
| [`workbook/week-NN.md`](levels/level-1-explorer/36-week-course/workbook/) | The student, with a pencil | Homework |

**Teaching this without knowing any AI?** Read
[`teacher-guide/00-orientation.md`](levels/level-1-explorer/36-week-course/teacher-guide/00-orientation.md)
once, before Week 1. It teaches you the whole subject in plain language, then gives you the 20 questions
students actually ask and the 15 things adults most often get wrong. Every weekly file then re-teaches
you that week's concept before it asks you to teach it.

### 🎒 The weekly rhythm — Self-Study (all levels)

Every module is one week. Do it in four sittings, not one marathon.

```
  MON  ~45 min   🪝 Hook + 🧠 Concept       Read slowly. Say each idea out loud in your own words.
  WED  ~45 min   🔍 Worked Example + 💻     Type the code yourself. NEVER copy-paste on the first pass.
  FRI  ~45 min   ✍️ Practice (all 6)        Warm-ups first. Struggle 15 min before the answer key.
  SAT  ~60 min   🛠️ Mini-Project + 🔑       Build it. Then close the file and re-explain it to someone.
  ───────────────────────────────────────────────────────────────────────────────────────────
       ~3.5 h/week  →  one module per week  →  ~9-14 weeks per level
```

If a week is busy, **skip the Stretch exercises, never the mini-project.** The projects are the course.

### How to do the Practice section

Every module has **exactly 6 exercises**:

| Tag | Count | What it's for | If you're stuck |
|---|:--:|---|---|
| `[Warm-up]` | 2 | Prove you understood the words | Re-read 🧠 The Concept. These should take < 5 min each. |
| `[Build]` | 2 | Make something small and new | Re-read 🔍 Worked Example and copy its *shape*, not its answer. |
| `[Stretch]` | 2 | Push past the module | Being stuck for 20 minutes here is *normal and good*. |

### How to use the Answer Keys

Every module ends with `✅ Answer Key` inside a `<details>` block, so you have to *choose* to open it.

> **The 20-minute rule:** Struggle for 20 minutes before you peek. Struggle is where the learning happens —
> reading a solution feels like learning but usually isn't.

When you do open it: **read the solution, close it, then rewrite the answer from scratch without looking.**
If you can't, you didn't learn it yet. That's fine — that's what the key is for.

### How to know you're ready for the next module

Each module ends with 🔑 **Key Takeaways** and 📓 **Vocabulary**. Cover the definitions column and say each
term's meaning out loud. Miss more than two? Redo the practice section before moving on. There are no
forward dependencies in this course — but there are plenty of backward ones.

### Keep a lab notebook

One folder per level, one notebook file per module (`notes/level-2/module-05.md`). Write down: what you
built, what broke, and the one sentence you'd tell your past self. By Level 4 this notebook is your
engineering journal, and it is worth more than any certificate.

---

## 🏆 What You'll Have Built By The End

Your portfolio after 36 modules:

**Level 1 — Explorer**
- 🔬 An unplugged "human machine learning" experiment with real recorded results
- 📸 A Teachable Machine image classifier you trained, tested, and *broke* on purpose
- 🎮 A Scratch app that reacts to a model's prediction
- 📊 A spreadsheet mini-dataset with features, labels, and a hand-drawn decision rule
- ⚖️ A **fairness audit poster** for a real AI product you use every day
- 🎪 **Capstone:** an AI Fair booth — classifier + Scratch demo + data card + bias report

**Level 2 — Builder**
- 🐍 Python programs from scratch: a quiz game, a text-menu tool, a data cleaner
- 📈 A hand-built analysis of a messy dataset in pandas, with 5 charts that tell a true story
- 🤖 Three trained models (kNN, decision tree, linear regression) compared honestly
- 🧪 An overfitting demonstration you can explain with your own numbers
- 🔎 **Capstone:** *Data Detective* — a full notebook that answers a real question with data and a model

**Level 3 — Engineer**
- 🔧 A reusable end-to-end supervised pipeline with feature engineering and no leakage
- 📉 Gradient descent implemented by hand, plotted converging
- 🧠 A neural network written from scratch in NumPy — forward pass *and* backprop
- 🔥 PyTorch models: an MLP and a CNN trained on real image data
- 🧩 A k-means + PCA exploration of unlabeled data
- 📝 A text classifier built on bag-of-words and TF-IDF
- 🚢 **Capstone:** *Ship It* — a trained model packaged, served, monitored, with a model card

**Level 4 — Innovator**
- 🧬 A character-level **tiny GPT** you wrote and trained yourself: attention, heads, blocks, all of it
- 📚 A written explanation of pretraining → SFT → RLHF that a smart adult would learn from
- ✍️ A prompt library with a measured eval harness (not vibes)
- 🔍 A RAG system: chunking, embeddings, vector search, grounded citations
- 🛠️ A tool-using agent with real tool schemas, an agent loop, and guardrails
- 📊 An LLM evaluation suite + a fine-tuning experiment write-up
- 🛡️ A red-team report on your own system
- 🚀 **Capstone:** a real, useful AI product with a design doc, evals, cost budget, and a demo

---

## 🧰 Required Setup, Per Level

Set up **only** what the level needs. Don't install Level 3 tools in Level 1.

### Level 1 — Explorer (nothing to install)

| Tool | Where | Notes |
|---|---|---|
| Web browser | already have it | Chrome/Safari/Edge all fine |
| [Teachable Machine](https://teachablemachine.withgoogle.com) | browser | Free, no account needed |
| [Scratch](https://scratch.mit.edu) | browser | Free account to save projects |
| [Quick, Draw!](https://quickdraw.withgoogle.com) | browser | Used for data intuition |
| Google Sheets / Excel / LibreOffice | browser or desktop | Any spreadsheet works |
| Paper, pencil, index cards | 🙂 | Genuinely required — several modules are unplugged |

### Level 2 — Builder (first real install)

```bash
# 1) Install Python 3.11 or newer from https://www.python.org/downloads
python3 --version          # should print 3.11.x or higher

# 2) Make a project folder and an isolated environment
mkdir -p ~/ai-academy && cd ~/ai-academy
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate

# 3) Install the Level 2 toolkit
pip install --upgrade pip
pip install numpy pandas matplotlib scikit-learn jupyterlab

# 4) Check it works
python -c "import numpy, pandas, matplotlib, sklearn; print('Level 2 ready')"
```

Editor: **VS Code** (free) with the Python extension, or JupyterLab (`jupyter lab`) for notebooks.

### Level 3 — Engineer (add deep learning)

```bash
source ~/ai-academy/.venv/bin/activate
pip install torch torchvision joblib seaborn
python -c "import torch; print('torch', torch.__version__)"

# Apple Silicon Mac? You have GPU acceleration built in:
python -c "import torch; print('MPS available:', torch.backends.mps.is_available())"
```

No GPU? Every Level 3 model is sized to train on a laptop CPU in under 10 minutes.
[Google Colab](https://colab.research.google.com) is the free fallback for the two heaviest modules.

### Level 4 — Innovator (add LLMs)

```bash
source ~/ai-academy/.venv/bin/activate
pip install transformers datasets tokenizers anthropic

# Get an API key from https://console.anthropic.com, then store it as an
# environment variable. NEVER paste a key into a code file you might share.
export ANTHROPIC_API_KEY="sk-ant-..."       # add this line to ~/.zshrc or ~/.bashrc
python -c "import os; print('key loaded:', bool(os.environ.get('ANTHROPIC_API_KEY')))"
```

> ⚠️ **Money and keys.** API calls cost real money and an API key is a password. Level 4 Module 5
> teaches you to set a spending limit *before* your first call, and every Level 4 script prints its
> token usage. A leaked key is the #1 rookie mistake — keep it out of your code and out of git.

---

## 📁 Repository Layout

```
claude_AI_Academy/
├── START_HERE.md                 ← read this first: picks your track, day one in one page
├── README.md                     ← you are here
├── CURRICULUM_MAP.md             ← all 36 modules, spiral table, dependency graph
├── RESOURCES.md                  ← books, courses, datasets, tools, communities
├── teacher-guide/                ← adult support for the SELF-STUDY track, all 4 levels
│   ├── README.md                 ← how to support a learner you can't out-teach
│   ├── pacing-guide.md           ← week-by-week calendar for all four levels
│   ├── rubrics.md                ← grading rubrics for every capstone
│   └── progress-tracker.md       ← printable checklists and skill logs
├── site/
│   └── index.html                ← browsable single-file version of the 4-level map
└── levels/
    ├── level-1-explorer/
    │   ├── README.md             ← level intro, prerequisites, kit list
    │   ├── module-01-what-ai-is-and-isnt.md
    │   ├── ...                   ← 9 modules per level
    │   ├── module-09-fair-private-honest-ai.md
    │   ├── capstone.md           ← the level's build-it-all project
    │   ├── assessment.md         ← the level exit exam
    │   ├── glossary.md           ← every term defined in this level
    │   └── 36-week-course/       ★ THE TAUGHT EDITION — a full school year
    │       ├── HOW-TO-USE.md     ← the three books + weekly rhythm (read first)
    │       ├── README.md         ← the 36-week plan, 4 terms, materials list
    │       ├── teacher-guide/    ← 00-orientation.md + week-01..36.md
    │       ├── student-guide/    ← week-01..36.md  (the illustrated chapters)
    │       ├── workbook/         ← week-01..36.md  (the write-in homework)
    │       ├── assessments/      ← four 45-min term tests + marking & remediation
    │       ├── projects/         ← 50 project ideas · worked exemplar · capstone
    │       ├── figures/          ← 450 hand-drawn SVGs + STYLE.md + _preview.html
    │       └── site/index.html   ← offline browsable course, per-week progress tracking
    ├── level-2-builder/          ← same 13-file module shape
    │   └── 36-week-course/       ★ THE TAUGHT EDITION — Python, a full school year
    │       (same layout as Level 1: 3 books x 36 weeks, tests, projects, 359 figures)
    ├── level-3-engineer/         ← same 13-file module shape
    │   └── 36-week-course/       ★ THE TAUGHT EDITION — PyTorch, offline, a full school year
    │       (3 books x 36 weeks, a maths ladder as well as a syntax ladder, 330 figures)
    ├── level-3-engineer/         ← same 13-file module shape
    └── level-4-innovator/        ← same 13-file module shape
```

**Every level folder has the same 13 files:** a README, 9 modules, a capstone, an assessment, and a
glossary. **Levels 1, 2 and 3 additionally have `36-week-course/`** — the taught edition: 120 markdown
files per level, covering that level's 9 modules across a full school year.

| Level | Intro | Capstone | Exit exam | Glossary |
|---|---|---|---|---|
| 1 · Explorer | [README](levels/level-1-explorer/README.md) | [AI Fair Booth](levels/level-1-explorer/capstone.md) | [assessment](levels/level-1-explorer/assessment.md) | [glossary](levels/level-1-explorer/glossary.md) |
| 2 · Builder | [README](levels/level-2-builder/README.md) | [Data Detective](levels/level-2-builder/capstone.md) | [assessment](levels/level-2-builder/assessment.md) | [glossary](levels/level-2-builder/glossary.md) |
| 3 · Engineer | [README](levels/level-3-engineer/README.md) | [Ship It](levels/level-3-engineer/capstone.md) | [assessment](levels/level-3-engineer/assessment.md) | [glossary](levels/level-3-engineer/glossary.md) |
| 4 · Innovator | [README](levels/level-4-innovator/README.md) | [Build an AI Product](levels/level-4-innovator/capstone.md) | [assessment](levels/level-4-innovator/assessment.md) | [glossary](levels/level-4-innovator/glossary.md) |

**Also here:** [RESOURCES.md](RESOURCES.md) (where to go next for every topic) ·
[teacher-guide/](teacher-guide/README.md) (for the adult in the room) ·
[site/index.html](site/index.html) (open it in a browser to click through the whole map)

---

## 🧭 Start Here

> ### 👉 **[START_HERE.md](START_HERE.md)** — the one-page day-one guide
>
> It picks your track and tells you the single file to open today.

**Short version:**

| You are | Open this |
|---|---|
| A parent/teacher who knows no AI | [`36-week-course/teacher-guide/00-orientation.md`](levels/level-1-explorer/36-week-course/teacher-guide/00-orientation.md), then [`week-01.md`](levels/level-1-explorer/36-week-course/teacher-guide/week-01.md) |
| The student in a taught class | [`36-week-course/student-guide/week-01.md`](levels/level-1-explorer/36-week-course/student-guide/week-01.md) — *after* your first class |
| A learner working alone | [`levels/level-1-explorer/module-01-what-ai-is-and-isnt.md`](levels/level-1-explorer/module-01-what-ai-is-and-isnt.md) — the 🪝 Hook only |
| Just browsing | [`36-week-course/site/index.html`](levels/level-1-explorer/36-week-course/site/index.html) — double-click it |

### 🎤 Explaining this to someone else

Two ready-to-present decks live in [`presentations/`](presentations/). Both are single files that
open by double-clicking and work offline. Press `N` for speaker notes, `T` for dark mode; print to PDF
for one slide per page with the notes included.

| Deck | For | Covers |
|---|---|---|
| [`for-parents.html`](presentations/for-parents.html) | A parent evening · 16 slides | How the teaching model works, how an AI model actually learns, cost and time, what it is *not* |
| [`for-investors.html`](presentations/for-investors.html) | An investor conversation · 18 slides | The teacher-supply bottleneck, the verified asset, routes to market, risks, the next 90 days |

> **The investor deck contains no invented figures.** Market size, pricing and the raise are left as
> clearly-marked placeholders for you to fill from your own research — and it states plainly on slide 1
> that there are no users, no pilot and no revenue.

### 🖥️ Or run it as a website

The whole Level 1 course renders as a local site with **two passcodes**:

```bash
./site-app/serve.sh          # → http://localhost:8000/
```

| | Passcode | Opens |
|---|---|---|
| 🎒 Student | `student1234` | chapters · workbooks · projects · glossary · gallery, **all three levels** |
| 🧑‍🏫 Teacher | `teacher1234` | all of the above **plus** lesson scripts · orientation · term tests · answer keys |
| 🔓 No passcode | — | the level picker only |

Every page except the home page is **encrypted at build time with AES-256-GCM** — the words aren't in
the page source, so there's nothing to peek at. Local only; nothing is published. Details and how to
set your own passcodes: [site-app/README.md](site-app/README.md).

Level 1 needs **nothing installed**. Ninety minutes from now you'll have trained your first model.

**Already know some of this?** Take the placement check at the top of each level README. If you can do
every ✅ Self-Check item in a level's final module, skip that level. If you're unsure, don't skip — the
spiral means the "easy" level is where the deep vocabulary gets installed.

---

## 🧾 A Note On Honesty

This course will repeatedly ask you to *try to break your own model*, to report the accuracy that
embarrasses you, and to ask who gets hurt when the model is wrong. That isn't a side quest.
Anyone can make a demo that works once. Engineers make things that work honestly.

Welcome to AI Academy. Go build something. 🚀

```
  ██╗     ███████╗██╗   ██╗███████╗██╗       ██████╗
  ██║     ██╔════╝██║   ██║██╔════╝██║       ╚════██╗
  ██║     █████╗  ██║   ██║█████╗  ██║        █████╔╝
  ██║     ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║       ╚═══██╗
  ███████╗███████╗ ╚████╔╝ ███████╗███████╗  ██████╔╝
  ╚══════╝╚══════╝  ╚═══╝  ╚══════╝╚══════╝  ╚═════╝

  ███████╗███╗   ██╗ ██████╗ ██╗███╗   ██╗███████╗███████╗██████╗
  ██╔════╝████╗  ██║██╔════╝ ██║████╗  ██║██╔════╝██╔════╝██╔══██╗
  █████╗  ██╔██╗ ██║██║  ███╗██║██╔██╗ ██║█████╗  █████╗  ██████╔╝
  ██╔══╝  ██║╚██╗██║██║   ██║██║██║╚██╗██║██╔══╝  ██╔══╝  ██╔══██╗
  ███████╗██║ ╚████║╚██████╔╝██║██║ ╚████║███████╗███████╗██║  ██║
  ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝
```

# ⚙️ Level 3 — Engineer

### *A model is one component of a measured, engineered, shippable pipeline.*

**Grade band:** 9–10 (ages ~14–16) · **Coding required:** fluent Python — loops, functions, dicts, numpy, pandas · **Math required:** algebra and slope; the calculus intuition is built in-course
**Duration:** ~24 weeks · 9 modules (~5–6 h each) + a ~12 h capstone · **~61 hours total**

[⬅ Level 2](../level-2-builder/) · [Back to AI Academy](../../README.md) · [Full curriculum map](../../CURRICULUM_MAP.md) · [Level 4 ➡](../level-4-innovator/)

---

## 🪝 Why This Level Exists

In Level 2 you wrote three lines and got a model:

```python
model = DecisionTreeRegressor(max_depth=4)
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
```

Those three lines still work. They are still about 10% of the job.

Here is what happened at a real company that only knew the 10%. A team spent six weeks building a delivery-lateness model. It hit 94% accuracy. Everyone clapped. Then someone asked what the model was actually looking at, and it turned out to be a column called `refund_issued` — which only gets filled in *after* a delivery arrives late. The model was 94% accurate at predicting the past. At the moment you'd actually need the prediction, that column is empty. Six weeks. One column. The algorithm was never the problem.

The other 90% is the shape of this level:

```
   Modules 1–3  ·  The pipeline and the measuring instruments.
                   Framing, splits, features, leakage, and the metrics
                   that catch a model that's cheating.

   Modules 4–6  ·  Open the box marked fit(). Loss, gradients, backprop —
                   derived on paper, coded in NumPy, then handed to PyTorch.

   Modules 7–9  ·  Three real problem shapes: images, unlabelled data,
                   and text. Each one an engineering job, not a demo.
```

By the end you will have written gradient descent yourself and watched the loss curve fall. You will have derived backpropagation with a pen and then verified your own calculus numerically to seven decimal places. You will have trained a convolutional network that sees, clustered data nobody labelled, and built a text classifier whose mind you can read word by word.

And then you will have shipped one of them: an artifact on disk, a CLI, a local HTTP service, a log of every prediction, and a model card that tells the next person exactly where it breaks.

---

## 🎯 Level Outcomes

When you finish Level 3 you will be able to:

1. **Build a complete supervised pipeline** from raw rows to a saved, loadable model artifact with a model card attached.
2. **Engineer features** with scaling, encoding, binning, and interactions inside a `ColumnTransformer` — and detect data leakage before it flatters you.
3. **Compute and interpret** a confusion matrix, precision, recall, F1, and ROC-AUC, and tune a decision threshold to a stated cost of errors.
4. **Derive and implement gradient descent** for logistic regression in NumPy, and plot it converging.
5. **Implement a neural network's forward pass and backpropagation from scratch**, then rebuild it in PyTorch with a real training loop.
6. **Train a CNN on image data** with augmentation and transfer learning, and diagnose its errors from a confusion matrix.
7. **Cluster unlabelled data with k-means**, reduce dimensions with PCA, and build a TF-IDF text classifier.

> **The one-line test of whether you finished this level:** somebody hands you a table, a deadline, and a cost of being wrong — and you can produce a measured, saved, documented model that another human can run without asking you a single question.

---

## 🎒 What You Need Before Starting

### Prerequisites — the honest list

| You need | Why | If you don't have it |
|---|---|---|
| **Level 2 finished** — including the capstone | Module 1 assumes you have suffered through one end-to-end project by hand | Do [Level 2](../level-2-builder/). There is no shortcut here; Module 1 starts at a speed that assumes pandas fluency. |
| Python from a blank file: functions, loops, dicts, imports | Every module is 100–200 lines of code you type | [L2 M1–M3](../level-2-builder/module-01-python-from-zero.md). If writing a function with a loop inside takes you more than five minutes, fix that first. |
| numpy shapes, `axis=0` vs `axis=1`, broadcasting | Modules 4 and 5 are almost entirely shape arithmetic | [L2 M5](../level-2-builder/module-05-numpy-arrays.md). Print `.shape` after every operation for a week. |
| pandas: load, filter, derive a column, `groupby` | Modules 1–3 live in DataFrames | [L2 M6](../level-2-builder/module-06-pandas-tables.md) |
| A labelled matplotlib figure with axes and a legend | You will plot loss curves, ROC curves, elbows, and decision boundaries | [L2 M7](../level-2-builder/module-07-visualizing-data.md) |
| `y = mx + c` and what "slope" means | Module 4's derivative is slope, renamed and taken seriously | Module 4 rebuilds slope from a hill picture. No calculus class needed. |
| To be comfortable being wrong in public | Half this level is finding your own bugs | Module 5's gradient check exists exactly so you can prove yourself wrong cheaply |
| **No calculus** | Module 4 builds derivative intuition from scratch | — |

### The kit

```
   ┌──────────────────────────────────────────────────────────────────┐
   │  THE LEVEL 3 KIT                                                 │
   ├──────────────────────────────────────────────────────────────────┤
   │  □  The laptop you used for Level 2 (macOS / Windows / Linux)    │
   │  □  ~8 GB free disk space — PyTorch is big, and CIFAR-10 and     │
   │     FashionMNIST download about 350 MB between them              │
   │  □  Internet for pip and for two dataset downloads               │
   │  □  A notebook and pen — Modules 4, 5 and 7 make you do          │
   │     arithmetic by hand BEFORE you write the code. That is the    │
   │     entire pedagogy of this level. Do not skip it.               │
   │  □  A folder ~/ai-academy/level3 that you never delete           │
   │  □  A free Google account, for Colab — the GPU fallback for      │
   │     Modules 6 and 7 if your laptop is slow                       │
   └──────────────────────────────────────────────────────────────────┘
```

> ⚠️ **A grown-up should read this bit.** Nothing in Level 3 uploads your data anywhere and there are no accounts or API keys. The only network use is `pip install` and two dataset downloads from `torchvision` (FashionMNIST and CIFAR-10 — both standard, public, research datasets of clothing photos and small object photos). Google Colab is optional; if you use it, the code runs on Google's machines, so treat it like any other website and don't paste personal data into it.

> ⚠️ **No GPU? Completely fine.** Every model in this level is deliberately sized to train on a laptop CPU in under 10 minutes. Modules 6 and 7 are the two heavy ones, and each names a "fast path" that runs on CPU and a "slow path" you can send to Colab's free GPU if you want it.

---

## 🗺️ The Roadmap

```
        LEVEL 3 · ENGINEER — from "it scored 0.94" to "here is the artifact"

   PART ONE — THE PIPELINE AND THE INSTRUMENTS
   ┌────────────────────┐      ┌────────────────────┐      ┌────────────────────┐
   │  1. THE SUPERVISED │      │  2. FEATURE        │      │  3. EVALUATION     │
   │     PIPELINE       │─────►│     ENGINEERING    │─────►│     METRICS        │
   │                    │      │                    │      │                    │
   │  frame X and y     │      │  scale · encode    │      │  TP FP FN TN       │
   │  audit the table   │      │  bin · ratio       │      │  precision/recall  │
   │  train/val/test    │      │  interact          │      │  the threshold dial│
   │  baseline · joblib │      │  ⚠️ LEAKAGE        │      │  ROC · PR · AUC    │
   │  the model card    │      │  ColumnTransformer │      │  k-fold ± std      │
   └────────────────────┘      └────────────────────┘      └─────────┬──────────┘
     "the artifact IS             "the answer must not              │
      the deliverable"             be in the features"              │ now you can
                                                                     │ measure. so
                                                                     │ look inside.
   PART TWO — INSIDE fit()                                           ▼
   ┌────────────────────┐      ┌────────────────────┐      ┌────────────────────┐
   │  6. PYTORCH        │◄─────│  5. NEURAL NETS    │◄─────│  4. LOSS & GRADIENT│
   │                    │      │     FROM SCRATCH   │      │     DESCENT        │
   │  tensors · devices │      │                    │      │                    │
   │  autograd          │      │  neuron · layers   │      │  sigmoid           │
   │  the 5-line loop   │      │  ReLU · softmax    │      │  log loss          │
   │  Dataset/DataLoader│      │  the chain rule    │      │  derivative        │
   │  save · predict.py │      │  BACKPROP by hand  │      │  w ← w − lr·grad   │
   └─────────┬──────────┘      │  gradient check    │      │  learning rate     │
             │                 └────────────────────┘      └────────────────────┘
             │ now the nets                                  "fit() is a loop.
             │ can be big                                     here it is."
             ▼
   PART THREE — THREE REAL PROBLEM SHAPES
   ┌────────────────────┐      ┌────────────────────┐      ┌────────────────────┐
   │  7. CNNs:          │      │  8. NO LABELS:     │      │  9. CLASSIC NLP    │
   │     SEEING         │─────►│     k-MEANS & PCA  │─────►│                    │
   │                    │      │                    │      │  tokens · BoW      │
   │  locality          │      │  assign · move     │      │  TF-IDF by hand    │
   │  kernel/stride/pad │      │  elbow · silhouette│      │  cosine similarity │
   │  augmentation      │      │  PCA components    │      │  n-grams           │
   │  transfer learning │      │  explained variance│      │  embeddings ──────►│
   └────────────────────┘      └────────────────────┘      └─────────┬──────────┘
                                                                      │  the idea
                                                                      │  Level 4
                                                                      │  is built on
                                                                      ▼
                    ╔══════════════════════════════════════════════════════╗
                    ║   🚢  CAPSTONE — SHIP IT  (~12 h)                    ║
                    ║                                                      ║
                    ║   your best model from M7 or M9, frozen into an      ║
                    ║   artifact · predict.py CLI · a local HTTP service   ║
                    ║   · versioned model files · a prediction log with    ║
                    ║   inputs and latency · a full model card with        ║
                    ║   subgroup metrics · a one-page monitoring plan      ║
                    ╚══════════════════════════════════════════════════════╝
```

**Read the arrows as "you need this before that."** Module 1's `Pipeline` is the container everything else goes into. Module 3's metrics are what Modules 7 and 9 report. Module 4's gradient becomes Module 5's backprop becomes Module 6's `loss.backward()`. Module 8's PCA is how Module 9 plots its documents. Nothing here is decoration.

> 🔍 **Notice the shape of Part Two.** You derive the maths by hand (M4), implement it in raw NumPy (M5), and only *then* let a framework do it for you (M6). That order is deliberate and it is the opposite of most tutorials. When PyTorch's `loss.backward()` gives you a number in Module 6, you will already have computed that exact number with a pen — and Module 6 makes you check that they match to eight decimal places.

---

## 📚 The Nine Modules

| # | Module | You'll build | Time |
|:--:|---|---|:--:|
| 1 | [**The Supervised Pipeline, End to End**](module-01-the-supervised-pipeline.md) | 🏗️ **Pipeline v1** — one script: raw table → audit → three-way split → baseline → fitted `Pipeline` → validation metrics → saved `.joblib` → generated `model_card.md`. Plus a second script that loads the artifact in a clean process with zero training code in it. | ~5 h |
| 2 | [**Feature Engineering: Turning Raw Reality Into Numbers**](module-02-feature-engineering.md) | 🧪 **Beat The Baseline** — improve Module 1's score using *only* feature changes inside a `ColumnTransformer`, with a feature-by-feature ablation table — then hunt down a planted leakage bug that produces a suspiciously perfect score | ~5 h |
| 3 | [**Beyond Accuracy: Confusion Matrix, Precision, Recall, and Thresholds**](module-03-evaluation-metrics.md) | 🚨 **Fraud Bench** — a full metrics report on a 1%-positive dataset, a threshold tuned against a stated cost matrix (a missed fraud costs 50× a false alarm), and 5-fold cross-validated results with error bars | ~5 h |
| 4 | [**How Learning Actually Happens: Loss and Gradient Descent**](module-04-logistic-regression-gradient-descent.md) | 📉 **Descent From Scratch** — logistic regression trained by your own NumPy gradient descent, a plotted loss curve, a decision boundary that moves, three learning rates compared, and final weights matched against sklearn's | ~5.5 h |
| 5 | [**Neural Networks From Scratch: Neurons, Layers, and Backprop**](module-05-neural-networks-from-scratch.md) | 🧠 **NumPy Brain** — a 2-layer MLP in pure NumPy that learns `make_moons` to >90% test accuracy, with a numerical gradient check agreeing to `1e-6` and a decision boundary that visibly curves | ~6 h |
| 6 | [**PyTorch: Tensors, Autograd, and Real Training Loops**](module-06-pytorch-deep-learning.md) | 🔥 **Same Brain, Real Framework** — the Module 5 network rebuilt in PyTorch and proved identical, then a deeper MLP on FashionMNIST past 85% test accuracy with a train/val loss plot and a standalone `predict.py` | ~5.5 h |
| 7 | [**Convolutional Networks: Teaching a Model to See**](module-07-cnns-for-images.md) | 👁️ **See It** — a small CNN on a CIFAR-10 subset, then augmentation, then a fine-tuned resnet18, in one results table — plus the confusion matrix's 10 worst mistakes and a written diagnosis of the top confusion pair | ~6 h |
| 8 | [**Learning Without Labels: k-Means and PCA**](module-08-unsupervised-kmeans-pca.md) | 🗺️ **Cluster Cartography** — clusters justified by *both* elbow and silhouette evidence, a PCA projection coloured by cluster, and a human name for each cluster backed by a feature-means table | ~5 h |
| 9 | [**Classic NLP: From Tokens to Bag-of-Words to Embeddings**](module-09-classic-nlp.md) | 💬 **Sentiment Engine** — a TF-IDF + logistic regression classifier on typed-in reviews, with per-class precision/recall, the 15 most positive and negative learned words, a PCA plot, and one review it gets wrong *because word order was thrown away* | ~5.5 h |
| 🚢 | [**CAPSTONE — Ship It**](capstone.md) | 📦 A model somebody else can actually use: frozen artifact, `predict.py` CLI, local HTTP service, versioned files, a prediction log with latency, a full model card with subgroup metrics, and a one-page monitoring plan | ~12 h |

**Also in this folder:**

| File | What it's for | When to use it |
|---|---|---|
| [`assessment.md`](assessment.md) | 20 multiple-choice + 8 short-answer + 4 debug problems, with an explained answer key for every single item | After Module 9, before the capstone |
| [`glossary.md`](glossary.md) | Every term in this level — 221 of them — alphabetized, with a plain definition and the example from the course, plus the confusion-pair table and the formulas worth memorising | Any time a word stops making sense |
| [`capstone.md`](capstone.md) | The final build: brief, milestones, scaffold, a worked solution for the hardest milestone, rubric | Weeks 21–24 |

---

## 🧭 How This Level Fits the Whole Journey

### What Level 2 gave you

Level 2 taught you to *use* things. Level 3 opens them. Here is the exact mapping:

```
   ┌──────────────────────────────────────────────────────────────────────────┐
   │  LEVEL 2 (you used it)          ─►   LEVEL 3 (you understand it)   Mod   │
   ├──────────────────────────────────────────────────────────────────────────┤
   │  train_test_split(0.2)          ─►   train / val / test, and why    M1   │
   │                                      choosing is a kind of fitting        │
   │  pd.get_dummies                 ─►   OneHotEncoder in a              M2   │
   │                                      ColumnTransformer, fitted on         │
   │                                      train rows only                      │
   │  "don't fit the scaler first"   ─►   three named kinds of leakage,   M2   │
   │                                      each one caught with a test          │
   │  accuracy_score                 ─►   TP/FP/FN/TN, precision, recall, M3   │
   │                                      F1, ROC-AUC, and a cost matrix       │
   │  model.fit(X, y)                ─►   a loss function you              M4   │
   │                                      differentiate and a loop you write   │
   │  a decision tree's if/then      ─►   layers of neurons doing the      M5   │
   │  rules                               same job with numbers                │
   │  LinearRegression().coef_       ─►   weights updated by               M4   │
   │                                      w ← w − lr·gradient, plotted         │
   │  make_pipeline(Scaler, Model)   ─►   the artifact you save, version,  M1   │
   │                                      log, and document                    │
   │  "the model overfit"            ─►   augmentation, dropout, early     M6   │
   │                                      stopping, and a train/val curve  M7   │
   │  a labelled matplotlib chart    ─►   loss curves, ROC curves, elbow   all  │
   │                                      plots, decision boundaries           │
   └──────────────────────────────────────────────────────────────────────────┘
```

If you did Level 2 properly, nothing in the right-hand column is *unfamiliar* — it is the inside of something you already drove. That is why Module 1 can move fast: it is re-plumbing a house you have already lived in.

If you skipped Level 2: you will drown in Module 4. The maths is fine; the typing is not. Go do [Level 2 Modules 5, 6, 8, and 9](../level-2-builder/) at minimum.

### What Level 4 needs from you

Level 4 (**Innovator**, grades 11–12) builds sequence models, attention, a tiny GPT, RAG systems, and LLM agents. It will assume — without re-teaching — that you own all of this **cold**:

| Level 4 will say... | ...and expect you to already own | From |
|---|---|---|
| "a `(batch, seq_len, d_model)` tensor" | tensor shapes, dtypes, and device placement | M6 |
| "write the training loop" | `zero_grad` → forward → loss → `backward` → `step`, from a blank file | M6 |
| "the gradients vanish through 12 layers" | what a gradient *is*, and why saturating activations shrink it | M4, M5 |
| "we use cross-entropy over the vocabulary" | log loss, softmax, and why they are always paired | M4, M5 |
| "this token embedding has 768 dimensions" | that an embedding is a dense vector where nearby means similar | M9 |
| "cosine similarity against the vector store" | cosine similarity, computed by hand, and why it beats raw counts | M9 |
| "the retrieval baseline is TF-IDF" | TF-IDF weights and their exact formula | M9 |
| "a patch embedding, like a conv stem" | convolution, stride, padding, feature maps | M7 |
| "we fine-tuned the head and froze the backbone" | transfer learning, and what freezing actually does | M7 |
| "evaluate it — report the confusion matrix by subgroup" | precision, recall, thresholds, cost of errors | M3 |
| "ship it behind an endpoint with logging" | the capstone you are about to build | Cap |

Notice what is *not* on that list: any new maths. Level 4 adds architecture and scale, not calculus. What it cannot add is the thing this level is for — the instinct that a number without a baseline, a metric, and a saved artifact is not a result.

> **The one-sentence handover:** Level 1 gave you the concepts with your hands; Level 2 gave you the keyboard; **Level 3 gives you the maths under the hood and the discipline to ship**; Level 4 gives you the frontier.

---

## 🔧 Environment Setup

You already have a Level 2 environment. This level adds four packages, one of which (PyTorch) is large. Budget **40 minutes**, do it in **week 0 — before Module 1**, and do the smoke tests. A PyTorch install that half-worked is much worse than one that failed loudly.

### Step 1 — Check your Python (5 min)

```bash
python3 --version
```

| What you see | What to do |
|---|---|
| `Python 3.11.x` or `3.12.x` | ✅ Ideal. This level was checked on 3.11 and 3.12. |
| `Python 3.9.x` or `3.10.x` | ✅ Works. Everything here runs on 3.9+. |
| `Python 3.13.x` | ⚠️ Check that a PyTorch wheel exists for it before you commit. If `pip install torch` fails, install 3.12 alongside. |
| `Python 3.8` or older | ❌ Too old for current torch wheels. Install 3.11+ from [python.org](https://www.python.org/downloads/). |

### Step 2 — A fresh environment for this level (10 min)

You *can* reuse Level 2's venv. Don't. PyTorch pins numpy versions, and if that breaks your Level 2 environment you will be sad. Make a new box.

```bash
# 1) One folder for the whole level. Never delete this.
mkdir -p ~/ai-academy/level3
cd ~/ai-academy/level3

# 2) Create the private box
python3 -m venv .venv

# 3) Step INTO the box
source .venv/bin/activate          # macOS / Linux
.venv\Scripts\activate             # Windows PowerShell
```

Your prompt must now start with `(.venv)`. It does not stick between terminal sessions — you run the activate line every time.

### Step 3 — Install the stack (15 min, ~2.5 GB download)

```bash
python -m pip install --upgrade pip

# The Level 2 four, again, in the new box
python -m pip install numpy pandas matplotlib scikit-learn

# The Level 3 additions
python -m pip install torch torchvision joblib seaborn jupyterlab
```

> ⚠️ **Windows + NVIDIA GPU?** The default `pip install torch` gives you a CPU-only build on some platforms. That is *fine for this entire level* — every model is CPU-sized. If you specifically want CUDA, get the exact command for your CUDA version from [pytorch.org/get-started/locally](https://pytorch.org/get-started/locally/) and use that instead. Do not guess the command.

> ⚠️ **Apple Silicon Mac (M1/M2/M3/M4)?** The default install already includes **MPS**, Apple's GPU backend. Nothing extra to do. Modules 6 and 7 show you how to select it.

What you just installed, and when you first need it:

| Package | What it does | First used |
|---|---|---|
| `numpy` | Array maths — the language of Modules 4 and 5 | M1 |
| `pandas` | Tables | M1 |
| `matplotlib` | Loss curves, ROC curves, elbows, decision boundaries | M1 |
| `scikit-learn` | `Pipeline`, `ColumnTransformer`, metrics, cross-validation, `KMeans`, `PCA`, `TfidfVectorizer` | M1 |
| `joblib` | Saving and loading a fitted pipeline as one file | M1 |
| `seaborn` | Confusion-matrix heatmaps (one function, `sns.heatmap`) | M3 |
| `torch` | Tensors, autograd, neural networks | M6 |
| `torchvision` | Image datasets (FashionMNIST, CIFAR-10), transforms, pretrained resnet18 | M6 |
| `jupyterlab` | Notebooks — optional for modules, handy for the capstone | Cap |

Minimum versions this level's outputs were checked against: `numpy 1.24+` (2.x fine), `pandas 1.5+`, `matplotlib 3.6+`, `scikit-learn 1.3+`, `torch 2.0+`, `torchvision 0.15+`, `seaborn 0.12+`.

### Step 4 — The 3-line smoke test (2 min)

Create `smoke.py` in `~/ai-academy/level3`:

```python
import torch, sklearn, joblib, seaborn, torchvision
device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
print("Level 3 ready ·", "torch", torch.__version__, "· sklearn", sklearn.__version__,
      "· device:", device, "· matmul:", (torch.randn(3, 4) @ torch.randn(4, 2)).shape)
```

```bash
python smoke.py
```

```
   ┌─────────────────────────────────────────────────────────────────────┐
   │  🔥 LEVEL 3 SMOKE TEST                                              │
   ├─────────────────────────────────────────────────────────────────────┤
   │                                                                     │
   │  ✅ PASS looks like:                                                │
   │      Level 3 ready · torch 2.4.1 · sklearn 1.5.1 · device: mps      │
   │                     · matmul: torch.Size([3, 2])                    │
   │      (your versions will differ; `device: cpu` is a PASS too)       │
   │                                                                     │
   │  ❌ FAIL looks like:                                                │
   │      ModuleNotFoundError: No module named 'torch'                   │
   │      → troubleshooting row 1                                        │
   │                                                                     │
   │      OMP: Error #15: Initializing libiomp5.dylib...                 │
   │      → troubleshooting row 4                                        │
   └─────────────────────────────────────────────────────────────────────┘
```

That `torch.Size([3, 2])` is a real matrix multiply: `(3,4) @ (4,2) → (3,2)`. If it printed, your tensor library works.

### Step 5 — Prove autograd works (2 min)

Smoke test 1 proves torch *imports*. This proves it can actually differentiate — which is the entire reason it exists. Create `smoke_grad.py`:

```python
import torch

x = torch.tensor(3.0, requires_grad=True)   # "track this — I want its gradient"
y = x ** 2                                  # y = x², so dy/dx = 2x = 6 at x=3
y.backward()                                # walk the chain rule backwards
print("dy/dx at x=3 →", x.grad.item(), "(should be 6.0)")
```

```bash
python smoke_grad.py
```

```
dy/dx at x=3 → 6.0 (should be 6.0)
```

**If that prints `6.0`, your Level 3 environment is genuinely working.** That number is the derivative of `x²` at `x = 3`, computed by the machine. Module 4 will make you compute it by hand first; Module 6 will make you check the two agree.

### Step 6 — Prove a dataset can download (5 min, optional until Module 6)

`torchvision` downloads happen behind a firewall in a lot of schools, so find out in week 0, not week 13. Create `smoke_data.py`:

```python
from torchvision import datasets, transforms

ds = datasets.FashionMNIST(root="./data", train=True, download=True,
                           transform=transforms.ToTensor())
img, label = ds[0]
print("FashionMNIST OK ·", len(ds), "images ·", tuple(img.shape), "· label", label)
```

```
FashionMNIST OK · 60000 images · (1, 28, 28) · label 9
```

That's a 28×28 greyscale image with 1 channel, and label 9 = "Ankle boot". About 30 MB downloads into `./data`. If this fails, see troubleshooting row 5 — and if your network simply blocks it, that's exactly what Colab is for.

### Step 7 — Editor and the Colab fallback (5 min)

| Option | Get it | Best for |
|---|---|---|
| **VS Code** ✅ recommended | [code.visualstudio.com](https://code.visualstudio.com/) + the Microsoft **Python** extension | Modules 1–9. `Ctrl+Shift+P` → *Python: Select Interpreter* → the one with `.venv` in the path. |
| **JupyterLab** | already installed — run `jupyter lab` | Exploring, and the capstone write-up |
| **Google Colab** | [colab.research.google.com](https://colab.research.google.com) | The GPU fallback. *Runtime → Change runtime type → T4 GPU*. `torch` and `torchvision` are pre-installed. |

> 🔑 **When to reach for Colab.** Only two places: Module 7's fine-tuning path (Part H) and, if your laptop is genuinely slow, Module 6's FashionMNIST training. Everything else is CPU-sized on purpose. Colab disconnects after inactivity and wipes your files, so `torch.save` your weights and download them immediately.

### ✅ Setup complete checklist

- [ ] `python3 --version` prints 3.9 or higher (3.11+ preferred)
- [ ] `~/ai-academy/level3` exists and contains a `.venv` folder
- [ ] My prompt shows `(.venv)` after I run the activate line
- [ ] `python smoke.py` prints a torch version and a `torch.Size([3, 2])`
- [ ] `python smoke_grad.py` prints `6.0`
- [ ] `python smoke_data.py` downloaded 60000 images (or I know my network blocks it and I'll use Colab)
- [ ] VS Code is open on `level3` with the `.venv` interpreter selected
- [ ] I know whether my device string is `cpu`, `mps`, or `cuda` — and I've written it down

---

## 🚑 Troubleshooting — the five things that actually go wrong

| # | Symptom | Most likely cause | Fix |
|:--:|---|---|---|
| 1 | `pip install torch` fails with `Could not find a version that satisfies the requirement torch`, or `ModuleNotFoundError: No module named 'torch'` after a "successful" install | Two different causes that look the same. **(a)** No PyTorch wheel exists for your Python version or your CPU architecture (32-bit Windows, very new Python, old macOS). **(b)** The classic: you installed into one Python and are running another because the venv wasn't active. | First prove which Python you're running: `python -c "import sys; print(sys.executable)"`. The path **must** contain `.venv`. If it doesn't, run the activate line again and reinstall with `python -m pip install torch` (never bare `pip`). If the path is right and it still fails, it's (a): check your Python version against the wheels listed at [pytorch.org/get-started/locally](https://pytorch.org/get-started/locally/) and install a Python version that has one — 3.11 is the safest bet in this whole level. |
| 2 | `torch.backends.mps.is_available()` prints `False` on an Apple Silicon Mac, or `torch.cuda.is_available()` prints `False` on a machine with an NVIDIA card | For MPS: macOS older than 12.3, or an Intel Mac (MPS is Apple-Silicon only). For CUDA: you installed the CPU-only wheel, or the NVIDIA driver is older than the CUDA version torch was built against. | **This is not a blocker — carry on.** Every module in this level runs on CPU in under 10 minutes. Write `device = "cpu"` and continue. If you want the GPU: for MPS, update macOS to 12.3+; for CUDA, uninstall (`pip uninstall torch torchvision`) and reinstall using the exact command the PyTorch site gives for *your* CUDA version. Then re-run `smoke.py`. If you'd rather not fight it, use Colab for Modules 6–7 and stay on CPU for everything else. |
| 3 | `RuntimeError: expected scalar type Double but found Float`, or `ValueError: numpy.dtype size changed`, or `ImportError: numpy.core.multiarray failed to import` | Two separate dtype problems that beginners meet together. The `Double/Float` one: numpy defaults to `float64`, torch defaults to `float32`, and mixing them at a layer boundary raises. The `dtype size changed` one: your numpy major version doesn't match the one torch/sklearn were built against (usually a numpy 2.x vs 1.x clash). | For the Double/Float error, convert at the boundary — this is the standard line and Module 6 teaches it: `torch.tensor(arr, dtype=torch.float32)` or `.float()` on the tensor. For the numpy clash, reinstall the set together so pip resolves compatible versions: `python -m pip install --upgrade --force-reinstall numpy torch torchvision scikit-learn`. If it persists, pin: `python -m pip install "numpy<2"`. The nuclear option always works — delete `.venv` and redo Steps 2–3. That is *why* you use a venv. |
| 4 | On macOS: `OMP: Error #15: Initializing libiomp5.dylib, but found libiomp5.dylib already initialized` and the process dies. Or: your script simply hangs forever when a `DataLoader` starts, on Windows or macOS. | **OMP #15:** two libraries (usually torch and sklearn/numpy) each shipped their own OpenMP runtime and they collide. **The hang:** `DataLoader(num_workers=4)` spawns subprocesses; on Windows and macOS those re-import your whole script, and if your training code isn't inside `if __name__ == "__main__":` it forks infinitely. | For OMP: set `num_workers=0` first (it's the cheapest fix and this level's datasets don't need workers). If you must keep workers, `import os; os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"` **before** importing torch — a documented workaround, not a real fix. For the hang: use `num_workers=0`, or wrap every line that actually *runs* something in `if __name__ == "__main__":`. Every `DataLoader` in this level is written with `num_workers=0` for exactly this reason. |
| 5 | A `torchvision` download fails: `URLError`, `SSL: CERTIFICATE_VERIFY_FAILED`, `HTTP Error 403`, or a half-downloaded file that raises `EOFError` / `zipfile.BadZipFile` on the second run | A school/office network inspecting traffic or blocking the dataset mirror, or an interrupted download leaving a corrupt file in `./data` that torchvision then trusts. | First, **delete the `./data` folder entirely** and retry — a corrupt partial download is the single most common version of this, and torchvision will never fix it for you. If it's the network: try a phone hotspot for the one download (FashionMNIST is ~30 MB, CIFAR-10 ~170 MB — do them once and keep the folder forever). On macOS, an SSL error is often fixed by running `/Applications/Python 3.x/Install Certificates.command`. If your network blocks it outright, run Modules 6–7 in Colab, where the datasets download from inside Google's network. |

**Three more, less common but maddening:**

| # | Symptom | Fix |
|:--:|---|---|
| 6 | Training runs, loss goes down, but your accuracy is stuck at exactly the majority-class rate — and there is **no error** | The two silent killers of this level. Either you forgot `optimizer.zero_grad()` (gradients accumulate across batches; Module 6 measures the damage at 36 accuracy points), or you applied a sigmoid/softmax yourself *and* used `BCEWithLogitsLoss`/`CrossEntropyLoss`, which apply it again. Your model's last layer must be a bare `nn.Linear`. |
| 7 | `predict.py` gives different answers every time you run it on the same input | You forgot `model.eval()`. `Dropout` is still randomly zeroing units. Call `model.eval()` immediately after `load_state_dict`, before any prediction. This is also a capstone rubric line. |
| 8 | Everything trains fine, then `joblib.load` in a fresh process raises `AttributeError: Can't get attribute 'add_features' on module '__main__'` | You put a custom function inside a `FunctionTransformer` in your pipeline. `joblib` saves a *reference* to that function, not its code. Move the function into a small module (`features.py`), import it in both the training and the loading script. Module 2 hits this; the capstone requires you to have solved it. |

---

## 📅 Weekly Pacing

Twenty-four weeks at about **2.5 hours a week**, in three sittings. Level 3 modules are longer than Level 2's, so almost every module gets **two weeks**: one for the concept and the worked example, one for the hands-on and the mini-project. Resist the urge to do a whole module in one Saturday — Modules 4 and 5 in particular need a night's sleep in the middle.

### The weekly rhythm

```
   ┌──────┬──────────┬────────────────────────────────────────────────────┐
   │ DAY  │  TIME    │  WHAT YOU DO                                       │
   ├──────┼──────────┼────────────────────────────────────────────────────┤
   │ TUE  │  ~45 min │  🪝 Hook + 🧠 Concept                              │
   │      │          │  Read away from the keyboard, with paper. In this  │
   │      │          │  level the pen comes BEFORE the terminal.          │
   ├──────┼──────────┼────────────────────────────────────────────────────┤
   │ THU  │  ~50 min │  🔍 Worked Example + 💻 Hands-On                   │
   │      │          │  Do the worked example's arithmetic by hand first, │
   │      │          │  then run the code and check the numbers MATCH.    │
   │      │          │  A mismatch is the most valuable event of the week.│
   ├──────┼──────────┼────────────────────────────────────────────────────┤
   │ SAT  │  ~55 min │  ✍️ Practice + ⚠️ Mistakes + 🛠️ Mini-Project      │
   │      │          │  Struggle 20 minutes before opening the answer key.│
   │      │          │  Then write one paragraph in your engineering      │
   │      │          │  journal: what broke, and what you now believe.    │
   └──────┴──────────┴────────────────────────────────────────────────────┘
```

> 📓 **Start an engineering journal in week 0.** One file, `journal.md`, one dated entry per session. Level 3 is the level where you start hitting bugs nobody has documented, and the entry "*Tuesday: my gradient check failed at 3e-2, turned out `db` was summing over the wrong axis*" is worth more six months from now than any note you could copy from these modules.

### The twenty-four weeks

| Week | Focus | Hand in at the end of the week |
|:--:|---|---|
| **0** | 🔧 **Setup** (above) | All three smoke tests pass; your device string written down |
| **1** | [M1](module-01-the-supervised-pipeline.md) part 1 — framing, audit, the three-way split | An audit printout and 1200/400/400 with matched class rates |
| **2** | [M1](module-01-the-supervised-pipeline.md) part 2 — baseline, Pipeline, joblib, model card | 🏗️ **Pipeline v1**: `.joblib` + generated `model_card.md` + a `predict.py` with no training code |
| **3** | [M2](module-02-feature-engineering.md) part 1 — scaling, encoding, `ColumnTransformer` | Standardization done by hand on paper, then matched in code |
| **4** | [M2](module-02-feature-engineering.md) part 2 — derived features and the leakage hunt | 🧪 **Beat The Baseline**: an ablation table + a written account of how you caught the leak |
| **5** | [M3](module-03-evaluation-metrics.md) part 1 — confusion matrix, precision, recall, F1 | A confusion matrix built **by hand** from 25 rows, matching sklearn |
| **6** | [M3](module-03-evaluation-metrics.md) part 2 — thresholds, ROC/PR, cross-validation | 🚨 **Fraud Bench**: a threshold chosen by expected cost, with the arithmetic shown |
| **7** | 🧱 **Checkpoint 1 — the pipeline** (no new module) | Rebuild Pipeline v1 from a blank file, from memory. Sit assessment Q1–Q7. |
| **8** | [M4](module-04-logistic-regression-gradient-descent.md) part 1 — sigmoid, log loss, the derivative | Three gradient-descent iterations done **on paper**, before any code |
| **9** | [M4](module-04-logistic-regression-gradient-descent.md) part 2 — the update rule in NumPy | 📉 **Descent From Scratch**: a monotone loss curve + weights within 2 points of sklearn |
| **10** | [M5](module-05-neural-networks-from-scratch.md) part 1 — neurons, layers, the forward pass | A full 2-layer forward pass traced by hand with real numbers |
| **11** | [M5](module-05-neural-networks-from-scratch.md) part 2 — the chain rule and backprop | 🧠 **NumPy Brain**: gradient check under `1e-6` + a boundary that visibly curves |
| **12** | 🧱 **Checkpoint 2 — the maths** (no new module) | Rederive backprop's five rules on a blank page. Sit assessment Q8–Q13. |
| **13** | [M6](module-06-pytorch-deep-learning.md) part 1 — tensors, autograd, the canonical loop | Autograd's `dW1[0,0]` matched against your Module 5 hand-computed number |
| **14** | [M6](module-06-pytorch-deep-learning.md) part 2 — FashionMNIST and shipping | 🔥 **Same Brain**: >85% test accuracy + a `predict.py` that imports no training code |
| **15** | [M7](module-07-cnns-for-images.md) part 1 — conv arithmetic and a CNN from scratch | Output sizes computed on paper for six configs, then verified in code |
| **16** | [M7](module-07-cnns-for-images.md) part 2 — augmentation and transfer learning | 👁️ **See It**: a three-row results table + a diagnosis of the top confusion pair |
| **17** | [M8](module-08-unsupervised-kmeans-pca.md) — k-means and PCA | 🗺️ **Cluster Cartography**: named clusters + elbow *and* silhouette evidence |
| **18** | [M9](module-09-classic-nlp.md) part 1 — tokens, bag-of-words, TF-IDF | A 4×8 document-term matrix and TF-IDF weights computed by hand |
| **19** | [M9](module-09-classic-nlp.md) part 2 — cosine similarity, n-grams, embeddings | 💬 **Sentiment Engine**: top-15 words each way + one word-order failure diagnosed |
| **20** | 📝 **[Assessment](assessment.md)** | All 20 MCQ + 8 short answer + 4 debug, then read every explanation |
| **21** | 🚢 [Capstone](capstone.md) M1–M2 | Model chosen and frozen; the artifact loads in a clean process |
| **22** | 🚢 [Capstone](capstone.md) M3–M4 | `predict.py` CLI + the local HTTP service, both working |
| **23** | 🚢 [Capstone](capstone.md) M5–M6 | Versioning + the prediction log with latency + subgroup metrics |
| **24** | 🚢 [Capstone](capstone.md) M7 + 🎤 **demo** | The full model card, the monitoring plan, and a live demo to a human |

### Pacing variations

| If you have... | Do this |
|---|---|
| **~1.5 h/week** | Take 32 weeks. Give Modules 4, 5, 6 and 7 three weeks each. Never drop a mini-project — the capstone ships one of them. |
| **~6 h/week (holidays)** | 12 weeks: one module a week. But keep **M4 and M5 apart by at least three days**. Backprop only makes sense once "the gradient points uphill and you go the other way" has stopped being a sentence and become an instinct. |
| **A study partner** | Add a Sunday call. From M4 on, swap *broken* code: deliberately introduce one bug into your mini-project and make each other find it. This is the single best drill for this level, because Level 3's bugs are silent. |
| **A school term structure** | Weeks 1–19 as lessons, week 20 as the assessment, 21–24 as a project block ending in a **demo day** where each learner runs their HTTP service live and takes questions. |
| **You already know sklearn** | Sit the assessment's Q1–Q7 and debug problem D1 *first*. Score 100% and you may compress M1–M3 into three weeks of mini-projects only. Score less and you found your gap — do the modules. You cannot skip M4–M5 on the strength of knowing sklearn; that's the point of them. |
| **A GPU / good laptop** | Don't rush M6–M7 because they run fast. The time in those modules is thinking about shapes, not waiting for epochs. Spend the saved hours on the M7 "level it up" per-class recall extension. |

### ⚠️ Four pacing rules that matter more than the schedule

1. **Pen before terminal, every single time.** Modules 4, 5, 7 and 9 all have a worked example you are meant to do by hand *first*, then verify in code. The verification step — "my number was 0.802 and the code says 0.8022, so I understand this" — is the actual learning event. If you run the code first, you get the answer and lose the lesson.
2. **Never skip the checkpoint weeks (7 and 12).** Week 7 is where the pipeline stops being a thing you followed and becomes a thing you can build. Week 12 is where backprop stops being five rules you copied and becomes five rules you can rederive. A learner who skips week 12 hits Module 6 and finds that autograd is magic again.
3. **When your loss doesn't go down, do not change three things at once.** Change one. Write down what you changed and what happened. This is the habit the whole level is secretly teaching, and it is why the journal exists.
4. **If you fall behind, drop the [Stretch] exercises and the "level it up" extensions — never the mini-projects, and never the gradient check.** The capstone ships a mini-project. The gradient check is the only thing standing between you and hours of debugging a network that was never going to learn.

---

## 🧾 The Level 3 Promise

Twenty-four weeks from now, someone will show you a model that scores 0.97 and ask you if it's good.

You will not say yes. You will ask what the class balance is, and whether 0.97 beats "always guess the common class." You will ask which errors it makes and what each one costs. You will ask whether the scaler was fitted before or after the split, and whether any feature in that table could only have been filled in *after* the thing you're predicting already happened.

Then you will ask the question that ends most conversations: *"Can I load the artifact in a fresh Python process and get the same number?"*

And when it's your model, you will hand over a `.joblib` file, a `predict.py`, a service on `localhost:8000`, a log of every prediction with its latency, a model card that names two subgroups it works worse for, and a one-page plan naming the exact number that would tell you it had gone stale.

That is the difference between someone who trains models and someone who ships them.

---

## ▶️ Start Here

> ### 👉 **[Module 1 — The Supervised Pipeline, End to End](module-01-the-supervised-pipeline.md)**
>
> It opens with a pizza chain, a manager who says "our deliveries are bad, can AI fix it?", and six wasted weeks caused by one column.

---

[⬅ Level 2](../level-2-builder/) · [Back to AI Academy](../../README.md) · [Curriculum map](../../CURRICULUM_MAP.md) · [Glossary](glossary.md) · [Assessment](assessment.md) · [Capstone](capstone.md) · [Level 4 ➡](../level-4-innovator/)

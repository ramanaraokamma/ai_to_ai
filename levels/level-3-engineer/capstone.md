# 🚢 Level 3 Capstone — Ship It

**Level 3 · Capstone · ~12 hours · Prereqs: all nine Level 3 modules, especially [M1](module-01-the-supervised-pipeline.md) (Pipeline, joblib, the model card), [M3](module-03-evaluation-metrics.md) (thresholds, cost of errors), [M6](module-06-pytorch-deep-learning.md) (`state_dict`, `model.eval()`, inference with no training code), and whichever of [M7](module-07-cnns-for-images.md) or [M9](module-09-classic-nlp.md) you are shipping.**

[⬅ Module 9](module-09-classic-nlp.md) · [Level 3 Home](README.md) · [Assessment](assessment.md) · [Glossary](glossary.md)

---

## 🎯 What You'll Be Able To Do

By the end of this capstone:

1. **You will be able to** freeze a trained model *and every preprocessing step it depends on* into a single versioned artifact that loads in a fresh Python process containing zero training code.
2. **You will be able to** write one `Predictor` class that both a command-line tool and an HTTP service call — so the CLI and the service can never quietly disagree about what your model says.
3. **You will be able to** run a tiny local HTTP service from the Python standard library, handle malformed input without crashing, and return a JSON response with a model version in it.
4. **You will be able to** log every prediction — timestamp, model version, inputs, output, probability, and latency in milliseconds — to a file you can later analyse as data.
5. **You will be able to** write a full model card: intended use, training data, metrics **broken out by subgroup**, known failure modes, and out-of-scope uses.
6. **You will be able to** name the one number that would tell you your model has gone stale, explain how you'd measure it *without labels*, and say what you'd do when it moves.

---

## 🪝 The Brief

Your model works. You have the notebook to prove it.

Now a person who is not you needs to use it. Maybe it's a moderator at a small community forum who wants your sentiment classifier to triage 400 comments a day. Maybe it's a volunteer at an animal shelter who wants your CIFAR-10 CNN to pre-sort donated photos. They are not going to open Jupyter. They are not going to run cells in order. They are not going to know that you scaled the features before you trained.

```
   ┌────────────────────────────────────────────────────────────────────┐
   │                                                                    │
   │   THE ONE-SENTENCE BRIEF                                           │
   │                                                                    │
   │   Take your best model from Module 7 or Module 9 and turn it       │
   │   into something a stranger can run, trust, and monitor —          │
   │   without ever speaking to you.                                    │
   │                                                                    │
   └────────────────────────────────────────────────────────────────────┘
```

Here is the moment this capstone is about. It is 11 p.m. Your service has been running for three weeks. Someone messages you: *"it said this comment was positive and it obviously isn't."*

Can you answer them? Only if you can say:

- **which model version** produced that prediction,
- **what exactly** was sent in,
- **what probability** came back and against **which threshold**,
- **how long** it took,
- and whether that input looks like the data the model was trained on, or like something new.

Every one of those is a design decision you make *before* the message arrives. That's the whole capstone.

### Why this matters

Every module in this level built one piece. This is the piece that makes the others count for something.

| Module | What it gave you | Where it shows up in Ship It |
|---|---|---|
| 1 | `Pipeline`, `joblib`, the model card as a deliverable | Milestones 2 and 6 — this is the direct sequel |
| 2 | Preprocessing that lives *inside* the fitted object | Milestone 2's "one artifact, no loose steps" rule |
| 3 | Threshold tuning against a cost matrix | Milestone 2 freezes the threshold into the artifact; Milestone 6 justifies it |
| 4 | What a probability actually is | Why you log `probability`, not just `label` |
| 5 | Every operation the model performs, understood | Why you can explain a wrong answer instead of shrugging |
| 6 | `state_dict`, `model.eval()`, `predict.py` with no training imports | Milestones 2 and 3 — the torch path |
| 7 | A CNN, augmentation, transfer learning, a confusion matrix | One of your two shippable candidates |
| 8 | PCA, and clusters as engineered features | Optional: a drift detector in the stretch section |
| 9 | TF-IDF + logistic regression, readable coefficients | The other shippable candidate — and the easier one |

And here is the professional truth: **in a real job, the notebook is where a model is born and the artifact is where it lives.** The gap between those two things has a name — people call it "the last mile," and it is where most machine learning projects quietly die. Nobody teaches the last mile to a 15-year-old. You are about to build it.

---

## 🚦 Choosing What To Ship

You have two candidates. Pick one. You are not shipping both.

| | **Path A — the text classifier (M9)** | **Path B — the image classifier (M7)** |
|---|---|---|
| **The artifact** | One `.joblib` holding `TfidfVectorizer` → `LogisticRegression` | A `.pt` `state_dict` + a shared `model_def.py` + a frozen transform |
| **Input over HTTP** | A JSON string. Trivial. | An image. You must decide: base64? a file path? multipart? |
| **Artifact size** | ~100 KB | 3–45 MB |
| **Cold-start latency** | ~50 ms | 300–2000 ms (loading torch alone is ~1 s) |
| **Per-prediction latency** | 1–3 ms | 15–80 ms on CPU |
| **Subgroup metrics are easy on** | review length, negation presence, topic | per-class recall, image brightness, animal vs vehicle |
| **Hardest part** | nothing technical — the discipline is the work | encoding images in JSON, and matching the exact eval transform |
| **Recommended for** | **most people** ✅ | you, if Module 7 was your favourite and you want the harder version |

> 🔑 **Strong recommendation: Path A.** Not because it's easier to get marks — the rubric is identical — but because the *engineering* is the lesson, and Path B spends two of your twelve hours on image-encoding plumbing that teaches you nothing about shipping. Path A lets you spend those two hours on the monitoring plan, which is the part nobody ever does.
>
> Everything in this document works for both. Where the paths differ, there's a **🅑 Path B** note.

### The rules that apply to both paths

```
   RULE 1 — THE FRESH PROCESS RULE
   Your serving code imports NOTHING from your training code.
   Test: `grep -rE "\.fit\(|train_test_split|optimizer|DataLoader" serve/`
   must print nothing at all.

   RULE 2 — THE ONE-PREDICTOR RULE
   There is exactly one place in the repo where a prediction happens.
   The CLI calls it. The service calls it. Nothing else may.

   RULE 3 — THE VERSION RULE
   Every artifact has a version in its filename, and every prediction
   you return or log carries that version string.

   RULE 4 — THE NO-SILENT-CRASH RULE
   Send your service garbage — empty body, wrong field, 2 MB of junk,
   invalid JSON — and it must return a clear 400, stay alive, and be
   ready for the next request.
```

---

## 📋 Requirements

### 🟥 Must-have — without all of these, the capstone is not done

| # | Requirement | Evidence |
|:--:|---|---|
| M1 | A **chosen model**, retrained once by a script (not a notebook), with its test score recorded | `model/train.py` and a printed score |
| M2 | **All preprocessing frozen inside the artifact.** No step lives only in your head or a notebook cell. | Path A: one `Pipeline` in the `.joblib`. Path B: the eval transform defined in `model_def.py`, imported by both sides. |
| M3 | A **versioned artifact filename** (`sentiment_v1.joblib`, not `model.joblib`) plus a `.metadata.json` beside it | Both files in `model/artifacts/` |
| M4 | A **`predictor.py` with one `Predictor` class** that loads the artifact and does the prediction | One file, imported by both the CLI and the service |
| M5 | A **`predict.py` CLI** that takes input on the command line and prints label + probability + version + latency | `python serve/predict.py "the film was wonderful"` works |
| M6 | A **local HTTP service** with `GET /health` and `POST /predict`, standard library only | `curl` transcript in your write-up |
| M7 | **Every prediction logged** to `logs/predictions.jsonl` with: request id, timestamp, model version, input, output, probability, threshold, latency_ms | The file, plus `wc -l` showing it grew |
| M8 | **No training code in the serving path**, proved by the Rule 1 grep | Paste the grep and its empty output |
| M9 | The service **survives four malformed requests** — empty body, invalid JSON, missing field, oversized body — returning 400 and staying up | A transcript of all four |
| M10 | A **full `MODEL_CARD.md`**: intended use, training data, metrics, **metrics by subgroup**, known failure modes, out-of-scope uses | The file |
| M11 | **Metrics broken out by at least two subgroups**, with the group sizes stated | A table in the model card, generated by `eval/subgroup_report.py` |
| M12 | A **one-page `MONITORING.md`** naming **the number**, how it's measured *without labels*, its alert level, and the action | The file |
| M13 | A **cold-start test**: a brand-new terminal, `python serve/predict.py "..."`, works with nothing pre-loaded | Screenshot or transcript |

### 🟨 Should-have — this is what separates shipped from submitted

| # | Requirement | Why it lifts the project |
|:--:|---|---|
| S1 | A **`--version` flag** on both the CLI and the service, so you can run v1 and v2 side by side | This is how real rollbacks happen |
| S2 | A **`LATEST` pointer file** so "which version is live" is one line of text, not a guess | Deploy and rollback become one-line edits |
| S3 | **Latency percentiles** — p50 and p95 over 100 requests, not just an average | An average latency hides the slow 5% that users actually notice |
| S4 | The **threshold stored in the metadata**, not hard-coded, with a `--threshold` override | Module 3's whole lesson, made operational |
| S5 | A **log analysis script** that reads the JSONL back and prints count, p50/p95 latency, and the prediction distribution | Your log is only useful if you have ever read it |
| S6 | A **privacy decision written down**: what you log, what you *don't*, and why | Someone's text is in your log file. That is a choice you must defend. |
| S7 | Three **golden test cases** in a `tests.py` — inputs whose answers you assert, so a bad rebuild fails loudly | The cheapest regression test in existence |
| S8 | A **README.md** for the project with a 60-second "run this" quickstart | If a stranger can't start it in 60 seconds, you haven't shipped |

### 🟩 Could-have — pick at most two, only after every Must-have is done

| # | Idea |
|:--:|---|
| C1 | **Batch endpoint** — `POST /predict_batch` taking a list, returning a list, with per-item latency |
| C2 | **A v2 model** trained with one deliberate improvement, shipped alongside v1, with a comparison table from the *same* test set |
| C3 | **A drift detector** — log the share of input words that are out-of-vocabulary (Path A) or the mean pixel brightness (Path B), and plot it over your log file |
| C4 | **A confidence gate** — return `"label": "uncertain"` when the probability sits in a band you justify from Module 3's cost matrix |
| C5 | **A tiny HTML page** served at `/` with a text box that POSTs to `/predict`, so a non-programmer can use it |
| C6 | **Load test** — fire 500 requests from a script, plot the latency histogram, and find where it degrades |

> ⚠️ **The trap.** Every year somebody spends six hours making the HTML page pretty and forty minutes on the model card. The rubric weights *documented honesty* above polish, deliberately. The model card and the monitoring plan are two of the seven rubric rows.

---

## 🗺️ Milestone Plan

Seven milestones, about **12 hours**. The order matters: you cannot serve an artifact you haven't frozen, and you cannot write subgroup metrics for a model you haven't fixed.

```
   ┌────┬──────────────────────────────────┬─────────┬────────────────────────┐
   │ #  │  MILESTONE                       │  TIME   │  YOU END UP HOLDING    │
   ├────┼──────────────────────────────────┼─────────┼────────────────────────┤
   │ 1  │  Choose the model, write the     │  60 min │  A filled-in decision  │
   │    │  scaffold, state the contract    │         │  doc + empty folders   │
   ├────┼──────────────────────────────────┼─────────┼────────────────────────┤
   │ 2  │  train.py → a versioned artifact │ 120 min │  v1.joblib (or .pt) +  │
   │    │  with preprocessing frozen in    │         │  metadata.json         │
   ├────┼──────────────────────────────────┼─────────┼────────────────────────┤
   │ 3  │  predictor.py + predict.py CLI   │  90 min │  A working command     │
   │    │  (the one-predictor rule)        │         │  line tool             │
   ├────┼──────────────────────────────────┼─────────┼────────────────────────┤
   │ 4  │  ⚠️ HARDEST: the HTTP service,   │ 150 min │  localhost:8000 that   │
   │    │  logging, and latency            │         │  logs and won't crash  │
   ├────┼──────────────────────────────────┼─────────┼────────────────────────┤
   │ 5  │  Versioning + reading your own   │  90 min │  v2 alongside v1, and  │
   │    │  logs back as data               │         │  a log report          │
   ├────┼──────────────────────────────────┼─────────┼────────────────────────┤
   │ 6  │  Subgroup metrics + the full     │ 120 min │  MODEL_CARD.md with a  │
   │    │  model card                      │         │  subgroup table        │
   ├────┼──────────────────────────────────┼─────────┼────────────────────────┤
   │ 7  │  The monitoring plan + the       │  90 min │  MONITORING.md and a   │
   │    │  cold-start demo                 │         │  demo you've rehearsed │
   └────┴──────────────────────────────────┴─────────┴────────────────────────┘
                                             ─────────
                                             720 min = 12 h exactly
                                             (add 90 min slack. You will need it.)
```

---

### ☐ Milestone 1 — Choose, scaffold, and write the contract (60 min)

- [ ] Pick Path A or Path B, in writing, with one sentence of justification
- [ ] Create the folder scaffold (below) — every folder, even the empty ones
- [ ] Write the **prediction contract** before any code
- [ ] Write down the **cost of each error type** for your chosen application
- [ ] Choose your **threshold** from that cost, using Module 3's method
- [ ] `git init`, if you know git. If not, at least zip a copy of your Module 7/9 work first.

**The prediction contract — fill this in before writing a line of code:**

```
# PREDICTION CONTRACT — <your project name>

## What one prediction is about
   One prediction is about exactly one ______________________.

## Input
   Field name: ______   Type: ______   Constraints: ______________
   Example:    ____________________________________________

## Output
   {"label": "____"|"____", "probability": 0.0–1.0,
    "threshold": ____, "model_version": "____", "latency_ms": ____}

## The two errors, in the language of the application
   A false positive means: __________________________________
   It costs:                __________________________________
   A false negative means:  __________________________________
   It costs:                __________________________________
   Therefore the more expensive error is ______, by roughly ___×.

## The threshold
   Module 3's rule of thumb:  t* = C_FP / (C_FP + C_FN) = ____
   The threshold I am shipping: ____
   If they differ, why: ______________________________________

## What this model must NEVER be used for
   1. ______________________________________________________
   2. ______________________________________________________
```

> 🔑 **Why the contract comes first.** The moment you write "the output is a JSON object with these five fields," you have made a promise. Everything downstream — the CLI's print format, the service's response, the log schema, the model card's metrics table — is now determined. Teams that skip this step end up with a CLI that says `POSITIVE` and a service that says `1`, and nobody notices for a month.

---

### ☐ Milestone 2 — Freeze the artifact (120 min)

- [ ] Move your model training out of the notebook into `model/train.py`
- [ ] Put **every** preprocessing step inside the fitted object (Path A) or inside `model_def.py` (Path B)
- [ ] Fit on train, choose the threshold on **validation**, score the test set **once**
- [ ] Save as `model/artifacts/<name>_v1.joblib` (or `.pt`)
- [ ] Write `<name>_v1.metadata.json` beside it — generated by the script, never typed
- [ ] Write `model/artifacts/LATEST` containing just `<name>_v1`
- [ ] Prove it: open a **fresh** Python, `joblib.load` the file, predict on one input

**The metadata file is not optional decoration.** It is how the serving side learns things it must not guess:

```json
{
  "version": "sentiment_v1",
  "created_utc": "2026-03-14T09:41:07Z",
  "task": "binary sentiment classification of short English reviews",
  "classes": ["negative", "positive"],
  "threshold": 0.42,
  "input_field": "text",
  "n_train": 80,
  "n_test": 24,
  "test_accuracy": 0.917,
  "test_f1_positive": 0.923,
  "sklearn_version": "1.5.1",
  "python_version": "3.11.9",
  "training_script_sha": "a3f19c2"
}
```

Those last three lines look like bureaucracy. They are the difference between "the model broke after I upgraded my laptop" being a two-minute diagnosis and a two-day one.

**Path A — the whole freezing job in one object:**

```python
# model/train.py  (extract)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=1)),
    ("clf",   LogisticRegression(C=1.0, max_iter=1000)),
])
pipe.fit(train_texts, train_labels)      # the vectorizer's vocabulary and IDF
                                         # weights are now INSIDE pipe
joblib.dump(pipe, ARTIFACTS / "sentiment_v1.joblib")
```

The vocabulary, the IDF weights, the lowercasing rule, and the coefficients are all inside one object. There is nothing left to forget.

> ⚠️ **The `FunctionTransformer` trap.** If you added a custom function to your pipeline (`FunctionTransformer(clean_text)`), `joblib` saves a *reference* to `clean_text`, not its code. Load it in a fresh process and you get `AttributeError: Can't get attribute 'clean_text' on module '__main__'`. **Fix:** put the function in `model/model_def.py` and import it in both `train.py` and `predictor.py`. This is troubleshooting row 8 in the [level README](README.md), and it bites almost everyone once.

**🅑 Path B — the torch version:**

```python
# model/model_def.py — imported by BOTH train.py and predictor.py
import torch.nn as nn
from torchvision import transforms

CLASSES = ["airplane", "automobile", "bird", "cat", "deer",
           "dog", "frog", "horse", "ship", "truck"]

# The EVAL transform. Not the training one — no random flips, no crops.
# If this differs by one number from what you trained with, your accuracy
# quietly drops and nothing raises an error.
EVAL_TRANSFORM = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.4914, 0.4822, 0.4465),
                         std=(0.2470, 0.2435, 0.2616)),
])

class SmallCNN(nn.Module):
    ...   # exactly the class from Module 7, living here and nowhere else
```

Then `train.py` does `torch.save(model.state_dict(), ...)` and `predictor.py` rebuilds `SmallCNN()`, loads the numbers, and calls `model.eval()`. **The normalization constants are part of the model.** Getting them from a different file than the one you trained with is the single most common Path B bug.

---

### ☐ Milestone 3 — One predictor, one CLI (90 min)

- [ ] Write `serve/predictor.py` with a `Predictor` class and a `Prediction` dataclass
- [ ] `Predictor.__init__` loads the artifact **once**; `predict_one` must not reload it
- [ ] Time the prediction with `time.perf_counter()`, in **milliseconds**
- [ ] Write `serve/predict.py` using `argparse`, with `--version`, `--threshold`, `--json`
- [ ] Run the Rule 1 grep and paste the empty output into your write-up
- [ ] Test in a brand-new terminal (Must-have M13)

```bash
$ python serve/predict.py "the acting was hardly wonderful"
negative   p=0.284   (threshold 0.42, model sentiment_v1, 1.8 ms)

$ python serve/predict.py --json "genuinely one of the best films this year"
{
  "request_id": "3f7a1c0e",
  "ts": "2026-03-14T10:02:55.118Z",
  "model_version": "sentiment_v1",
  "input": "genuinely one of the best films this year",
  "label": "positive",
  "probability": 0.947,
  "threshold": 0.42,
  "latency_ms": 1.6
}
```

> ⚠️ **Latency measured where?** `perf_counter()` around *only* the prediction call, not around the artifact load. Loading the model is a **cold-start cost** you pay once; predicting is a **per-request cost** you pay always. Reporting them as one number is the most common latency lie in the industry. Report both, separately, and label them.

---

### ☐ Milestone 4 — ⚠️ The service, the log, and the latency (150 min) — *hardest milestone*

- [ ] Write `serve/service.py` using **only** `http.server` and `json` — no Flask, no FastAPI, nothing to install
- [ ] Load the `Predictor` **once at startup**, before the server starts
- [ ] `GET /health` returns `200` with the model version and threshold
- [ ] `POST /predict` takes `{"text": "..."}` and returns the contract's JSON
- [ ] Every prediction appends one line to `logs/predictions.jsonl`
- [ ] Every response includes `latency_ms`
- [ ] Handle all four malformed cases with a clear `400` and **no crash**
- [ ] Bind to `127.0.0.1`, **never** `0.0.0.0` — and be able to say why

Full runnable code below — see **🔍 Worked Solution: Milestone 4**. This is where projects stall. Do not skip it.

---

### ☐ Milestone 5 — Versions and reading your own logs (90 min)

- [ ] Train a **v2** with one deliberate change (a different `C`, bigrams on/off, more data)
- [ ] Save it as `..._v2.joblib` with its own metadata — do **not** overwrite v1
- [ ] Point `LATEST` at whichever you'd actually ship, and say why in one sentence
- [ ] Prove the rollback: run the CLI with `--version <name>_v1` and get v1's answer back
- [ ] Write `eval/read_logs.py` that reads the JSONL and prints: total requests, per-version counts, p50 and p95 latency, and the label distribution
- [ ] Generate at least **100 log lines** (loop the CLI or curl in a shell loop) so the percentiles mean something

**A version comparison must use the same test set.** Otherwise you're comparing a model to a different exam.

| Version | Change | Test accuracy | Test F1 (positive) | p50 latency | Artifact size |
|---|---|:--:|:--:|:--:|:--:|
| `sentiment_v1` | unigrams, C=1.0 | 0.917 | 0.923 | 1.6 ms | 94 KB |
| `sentiment_v2` | uni+bigrams, C=4.0 | 0.917 | 0.917 | 2.1 ms | 231 KB |

> 🔍 **Read that table like an engineer, not a student.** v2 is *not* better. Same accuracy, slightly worse F1, 31% slower, 2.5× the artifact. On a 24-row test set, that accuracy tie is one row wide anyway. **The correct decision is to keep v1 live and write down why you rejected v2.** A capstone that ships v1 with a written rejection of v2 scores higher than one that ships v2 because it was newer.

**Reading your log back is the point of writing it:**

```python
# eval/read_logs.py
import json, statistics
from pathlib import Path
from collections import Counter

LOG = Path(__file__).resolve().parent.parent / "logs" / "predictions.jsonl"

rows = [json.loads(line) for line in LOG.read_text().splitlines() if line.strip()]
lat = sorted(r["latency_ms"] for r in rows)

def pct(sorted_values, p):
    """Nearest-rank percentile: the smallest value >= p% of the data."""
    if not sorted_values:
        return float("nan")
    k = max(0, min(len(sorted_values) - 1, round(p / 100 * len(sorted_values)) - 1))
    return sorted_values[k]

print(f"requests      : {len(rows)}")
print(f"by version    : {dict(Counter(r['model_version'] for r in rows))}")
print(f"by label      : {dict(Counter(r['label'] for r in rows))}")
print(f"latency p50   : {pct(lat, 50):.2f} ms")
print(f"latency p95   : {pct(lat, 95):.2f} ms")
print(f"latency max   : {lat[-1]:.2f} ms")
print(f"mean prob     : {statistics.mean(r['probability'] for r in rows):.3f}")
```

```
requests      : 137
by version    : {'sentiment_v1': 118, 'sentiment_v2': 19}
by label      : {'positive': 79, 'negative': 58}
latency p50   : 1.61 ms
latency p95   : 3.94 ms
latency max   : 41.20 ms
mean prob     : 0.523
```

That `max` of 41.20 ms against a p50 of 1.61 ms is real and worth a sentence in your write-up: it is almost always the **first** request after startup, when Python is still importing and warming caches. That's why p95 exists and why an average would have hidden it.

---

### ☐ Milestone 6 — Subgroup metrics and the full model card (120 min)

- [ ] Choose **at least two subgroups** and justify each in one sentence
- [ ] Write `eval/subgroup_report.py` that computes metrics per group **from the test set**
- [ ] Print the **group size** next to every metric. Always.
- [ ] Write `MODEL_CARD.md` with all six required sections
- [ ] Paste the subgroup table into the card, generated not typed
- [ ] Name at least **three known failure modes** with a concrete example each

**Choosing subgroups that mean something:**

| Path | Subgroup idea | Why it's worth measuring |
|---|---|---|
| A | **Review length** (≤ 8 words / 9–20 / 21+) | Short reviews have fewer features; TF-IDF has almost nothing to go on |
| A | **Contains a negation word** (`not`, `never`, `hardly`, `far from`) | Module 9 proved bag-of-words throws away word order — this is where |
| A | **Contains an emoji or `!!!`** | Your tokenizer probably deleted them. Did it cost you? |
| A | **Topic** (film / restaurant / product) if your corpus has them | Reveals whether it learned sentiment or learned topics |
| B | **Per class** (all 10) | The obvious one, and still the most informative |
| B | **Animal vs vehicle** (Module 7 found this split) | Confirms or refutes the confusion-pair story you told in M7 |
| B | **Mean image brightness** (dark third / middle / bright third) | A physical property the model never saw as a label |

**The subgroup table must look like this — sizes included, no exceptions:**

| Subgroup | n | Accuracy | Precision (pos) | Recall (pos) | F1 (pos) |
|---|:--:|:--:|:--:|:--:|:--:|
| **All test data** | 24 | 0.917 | 0.923 | 0.923 | 0.923 |
| Short (≤ 8 words) | 9 | 0.778 | 0.800 | 0.800 | 0.800 |
| Medium (9–20) | 11 | 1.000 | 1.000 | 1.000 | 1.000 |
| Long (21+ words) | 4 | 1.000 | 1.000 | 1.000 | 1.000 |
| Contains negation | 6 | 0.667 | 0.667 | 0.667 | 0.667 |
| No negation | 18 | 1.000 | 1.000 | 1.000 | 1.000 |

> ⚠️ **Small groups lie loudly.** `n = 4` at 1.000 accuracy is not "perfect on long reviews" — it is *four rows*. One flip takes it to 0.750. Every claim you make from a subgroup must carry its `n`, and any group under about 10 needs the words "too small to conclude from" next to it. Writing that sentence is worth a rubric level on its own.

But look at the negation row. **0.667 versus 1.000, on 6 rows versus 18.** That is not noise-free either, but it is *exactly the failure Module 9 predicted from theory*, showing up in your own measurements. That coincidence between prediction and evidence is the strongest thing you can put in a model card.

**The model card's six required sections:**

```
   1. INTENDED USE
      What it's for, who should use it, and the decision it supports.
      One paragraph. Include the sentence "This model outputs a
      suggestion, not a decision."

   2. TRAINING DATA
      Where the rows came from, how many, when, who wrote them, what
      languages/domains, what is NOT represented. Be specific and small:
      "80 reviews I typed myself in March 2026, all English, mostly
      about films" is a far better card entry than "a review corpus".

   3. METRICS
      Headline metric with its number, the threshold used, the test-set
      size, and the baseline it beats. No bare numbers.

   4. METRICS BY SUBGROUP
      The table above. Sizes included. A sentence naming the worst group.

   5. KNOWN FAILURE MODES
      Three or more, each with a real example input and the wrong output
      it produces. "It struggles with negation" is not a failure mode.
      "It scores 'not good at all' at p=0.71 positive because 'good'
      carries +1.83 and 'not' carries −0.04" is a failure mode.

   6. OUT-OF-SCOPE USES
      Things a reasonable person might try that you are telling them not
      to. Be concrete and include at least one that is tempting.
```

---

### ☐ Milestone 7 — The monitoring plan and the demo (90 min)

- [ ] Write `MONITORING.md` — **one page, no more**
- [ ] Name **the number**: one metric, not a dashboard of nine
- [ ] Show that it can be computed **without labels** — because in production nobody tells you the right answer
- [ ] State the **normal range**, the **alert level**, and how you got them
- [ ] State the **action**: what you actually do when it trips
- [ ] Rehearse the 10-minute demo (below) out loud, timed
- [ ] Do the cold-start test one final time in a brand-new terminal

> 🍕 **Why "without labels" is the whole game.** In your notebook you always knew the right answer, so you could compute accuracy. In production, nobody tells you. A comment goes through your classifier and then… nothing. No label ever arrives. So a monitoring plan built on accuracy is a plan you can never actually run. The good monitoring numbers are the ones you can compute from **inputs and outputs alone**.

**Four staleness numbers that need no labels:**

| The number | What it catches | How you'd measure it |
|---|---|---|
| **Out-of-vocabulary rate** — the share of input tokens your vectorizer doesn't know | Language drifting away from your training text: new slang, a new product, a different topic | For each request, tokenize and count how many tokens are absent from `pipe["tfidf"].vocabulary_`. Log the fraction. |
| **Uncertainty-band rate** — the share of predictions with probability between 0.4 and 0.6 | The model losing its grip on the inputs it's being shown | Log `probability` for every request, count how many fall in the band, report weekly |
| **Prediction-mix shift** — the share of requests predicted positive | A change in who is using it or what they're sending | `Counter(r["label"])` over a rolling window |
| **p95 latency** | Infrastructure rot: a bigger model, a slower disk, a memory leak | Straight from your log file |

**A monitoring plan that would actually work:**

> **The number: out-of-vocabulary rate (OOV), measured weekly.**
>
> **How:** every request logs `oov_rate` = (tokens not in the training vocabulary) ÷ (total tokens). `eval/read_logs.py` reports the weekly mean.
>
> **Baseline:** on my 24-row test set the mean OOV rate is **0.11** (σ = 0.06). Over the first 137 real requests it was **0.14**.
>
> **Alert level:** a weekly mean above **0.25**, or any single week more than 0.10 above the previous week.
>
> **Why this number:** my model is TF-IDF. A word it has never seen contributes *exactly nothing* — it is silently dropped. So a rising OOV rate means a rising share of each input is invisible to the model, and my accuracy is degrading in a way accuracy-on-training-data will never show me.
>
> **Action if it trips:** (1) pull the 50 highest-OOV requests from the log; (2) read them — this takes 15 minutes and usually explains everything; (3) if they are a genuine new domain, label 40 of them by hand and retrain as v3, keeping v2 live until the new test score beats it; (4) if they are junk or an attack, add input validation instead of retraining.
>
> **What I would NOT do:** retrain automatically on my own predictions. That is a feedback loop — the model teaching itself its own mistakes — and it gets worse in a way that looks like it's getting more confident.

That last paragraph is the mark of someone who has thought about this rather than read about it.

---

## 📁 Starter Scaffold

Build this in Milestone 1. Every file has one job.

```
   ship-it/
   │
   ├── README.md                     ← 60-second quickstart (Should-have S8)
   ├── MODEL_CARD.md                 ← Milestone 6
   ├── MONITORING.md                 ← Milestone 7, one page
   │
   ├── model/                        ⚠️  TRAINING LIVES HERE AND ONLY HERE
   │   ├── model_def.py              ← shared: classes, transforms, custom fns
   │   ├── train.py                  ← run once per version; writes artifacts
   │   └── artifacts/
   │       ├── LATEST                ← one line: "sentiment_v1"
   │       ├── sentiment_v1.joblib
   │       ├── sentiment_v1.metadata.json
   │       ├── sentiment_v2.joblib
   │       └── sentiment_v2.metadata.json
   │
   ├── serve/                        ⛔  NO TRAINING CODE MAY ENTER
   │   ├── predictor.py              ← the ONE place a prediction happens
   │   ├── predict.py                ← the CLI
   │   └── service.py                ← the HTTP server
   │
   ├── logs/
   │   └── predictions.jsonl         ← one JSON object per line, append only
   │
   ├── eval/
   │   ├── subgroup_report.py        ← Milestone 6
   │   ├── read_logs.py              ← Milestone 5
   │   └── figures/
   │
   └── tests.py                      ← three golden cases (Should-have S7)
```

> 🔑 **Why `model/` and `serve/` are separate folders.** Because then Rule 1 becomes a thing you can *check* rather than a thing you promise. `grep -rE "\.fit\(|train_test_split|optimizer|DataLoader" serve/` either prints something or it doesn't. Directory structure that makes a rule mechanically testable is worth more than a rule written in a comment.

### Starter file — `model/train.py` (Path A, runs as-is)

This generates its own tiny corpus so you can run the whole pipeline today and swap in your Module 9 reviews tomorrow.

```python
"""train.py — produce ONE versioned artifact. Run: python model/train.py --version 1

Nothing in serve/ may import anything from this file.
"""
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import joblib
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

ARTIFACTS = Path(__file__).resolve().parent / "artifacts"
ARTIFACTS.mkdir(parents=True, exist_ok=True)
CLASSES = ["negative", "positive"]


def load_corpus():
    """Replace this with your Module 9 reviews. Keep the (text, label) shape."""
    positive = [
        "genuinely one of the best films this year",
        "the pizza arrived hot and the crust was perfect",
        "wonderful acting and a script with real warmth",
        "fast delivery, careful packaging, exactly as described",
        "i laughed the whole way through and would watch it again",
        "the staff were kind and the food came out quickly",
    ]
    negative = [
        "a complete waste of two hours",
        "cold food, late delivery, and a rude driver",
        "the plot made no sense and the acting was wooden",
        "arrived broken and the box had been opened",
        "boring, predictable, and far too long",
        "i would not recommend this to anyone",
    ]
    texts = positive + negative
    labels = [1] * len(positive) + [0] * len(negative)
    return texts, labels


def git_sha():
    """Best-effort commit hash. Returns 'unknown' if this isn't a git repo."""
    try:
        out = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True, timeout=5)
        return out.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="1")
    ap.add_argument("--name", default="sentiment")
    ap.add_argument("--ngram-max", type=int, default=1)
    ap.add_argument("--C", type=float, default=1.0)
    ap.add_argument("--threshold", type=float, default=0.5)
    args = ap.parse_args()

    texts, labels = load_corpus()
    X_tr, X_te, y_tr, y_te = train_test_split(
        texts, labels, test_size=0.33, random_state=42, stratify=labels)

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, args.ngram_max))),
        ("clf",   LogisticRegression(C=args.C, max_iter=1000)),
    ])
    pipe.fit(X_tr, y_tr)                       # vocabulary + IDF + weights, all inside

    y_pred = (pipe.predict_proba(X_te)[:, 1] >= args.threshold).astype(int)
    acc = accuracy_score(y_te, y_pred)
    f1 = f1_score(y_te, y_pred, zero_division=0)
    print(f"test n={len(y_te)}  accuracy={acc:.3f}  f1(pos)={f1:.3f}")

    tag = f"{args.name}_v{args.version}"
    joblib.dump(pipe, ARTIFACTS / f"{tag}.joblib")

    meta = {
        "version": tag,
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "task": "binary sentiment classification of short English reviews",
        "classes": CLASSES,
        "threshold": args.threshold,
        "input_field": "text",
        "n_train": len(y_tr),
        "n_test": len(y_te),
        "test_accuracy": round(float(acc), 4),
        "test_f1_positive": round(float(f1), 4),
        "ngram_max": args.ngram_max,
        "C": args.C,
        "sklearn_version": sklearn.__version__,
        "training_script_sha": git_sha(),
    }
    (ARTIFACTS / f"{tag}.metadata.json").write_text(json.dumps(meta, indent=2))
    (ARTIFACTS / "LATEST").write_text(tag + "\n")
    print(f"wrote {tag}.joblib + metadata; LATEST -> {tag}")


if __name__ == "__main__":
    main()
```

```
$ python model/train.py --version 1
test n=4  accuracy=1.000  f1(pos)=1.000
wrote sentiment_v1.joblib + metadata; LATEST -> sentiment_v1
```

> ⚠️ That `n=4` test set is a placeholder, and a 1.000 on four rows means nothing. **Milestone 2 is not done until you have swapped in your Module 9 corpus** — at least 60 training and 20 test reviews. The scaffold exists so the plumbing works before the data is ready, not so you can ship a toy.

### Starter file — `tests.py` (three golden cases)

```python
"""tests.py — the cheapest regression test in existence. Run: python tests.py"""
import sys
sys.path.insert(0, "serve")
from predictor import Predictor          # noqa: E402

GOLDEN = [
    ("wonderful acting and a script with real warmth", "positive"),
    ("a complete waste of two hours",                  "negative"),
    ("cold food, late delivery, and a rude driver",    "negative"),
]

p = Predictor()
failures = 0
for text, expected in GOLDEN:
    got = p.predict_one(text)
    ok = got.label == expected
    failures += (not ok)
    print(f"{'PASS' if ok else 'FAIL'}  expected={expected:8s} got={got.label:8s} "
          f"p={got.probability:.3f}  «{text[:40]}»")

print(f"\n{len(GOLDEN) - failures}/{len(GOLDEN)} passed  (model {p.version})")
sys.exit(1 if failures else 0)
```

Run this after **every** retrain. If a golden case flips, either your model genuinely changed or your preprocessing broke — and you want to find out in five seconds, not from a user.

---

## 🔍 Worked Solution: Milestone 4

This is the milestone where capstones stall, so here is the whole thing, runnable, standard library only.

### The problem, in four parts

```
   ┌──────────────────────────────────────────────────────────────────────┐
   │  PART 1 — the model must load ONCE, at startup.                      │
   │           Loading per request turns 2 ms into 400 ms.                 │
   │                                                                       │
   │  PART 2 — the CLI and the service must never disagree.                │
   │           → one Predictor class. Both import it. Neither reimplements │
   │             a single line of prediction logic.                        │
   │                                                                       │
   │  PART 3 — the log is a DATA FILE, not a diary.                        │
   │           → JSON Lines: one complete JSON object per line, append     │
   │             only. Readable by a human, parseable by a script.         │
   │                                                                       │
   │  PART 4 — a service that dies on bad input is not a service.          │
   │           → validate the body length, the JSON, the field, the type.  │
   │             Four checks. Four clear 400s. Zero crashes.               │
   └──────────────────────────────────────────────────────────────────────┘
```

### Step 1 — `serve/predictor.py`, the one place a prediction happens

```python
"""predictor.py — the ONE place in this project where a prediction happens.

Imported by predict.py (CLI) and service.py (HTTP). Imports nothing from model/
except model_def, which contains no training code.
"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import joblib

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "model" / "artifacts"
LOG_PATH = ROOT / "logs" / "predictions.jsonl"
MAX_LOGGED_CHARS = 300          # a privacy decision — see Should-have S6


@dataclass
class Prediction:
    """Exactly the contract from Milestone 1. One place, one definition."""
    request_id: str
    ts: str
    model_version: str
    input: str
    label: str
    probability: float
    threshold: float
    latency_ms: float
    oov_rate: float             # for the monitoring plan (Milestone 7)


def resolve_version(version: str | None) -> str:
    """'latest' or None -> whatever LATEST points at. Otherwise use the name given."""
    if version and version != "latest":
        return version
    pointer = ARTIFACTS / "LATEST"
    if not pointer.exists():
        raise FileNotFoundError(
            f"No LATEST pointer at {pointer}. Run: python model/train.py --version 1")
    return pointer.read_text().strip()


class Predictor:
    """Loads one artifact ONCE and answers questions about it."""

    def __init__(self, version: str | None = None, threshold: float | None = None):
        self.version = resolve_version(version)
        art = ARTIFACTS / f"{self.version}.joblib"
        meta = ARTIFACTS / f"{self.version}.metadata.json"
        if not art.exists():
            raise FileNotFoundError(f"No artifact at {art}")

        t0 = time.perf_counter()
        self.pipeline = joblib.load(art)                    # ← the cold-start cost
        self.load_ms = (time.perf_counter() - t0) * 1000

        self.meta = json.loads(meta.read_text())
        self.classes = self.meta["classes"]
        self.threshold = float(self.meta["threshold"] if threshold is None else threshold)
        # Cache the vocabulary once so the OOV check costs nothing per request.
        self._vocab = set(self.pipeline["tfidf"].vocabulary_.keys())
        self._analyze = self.pipeline["tfidf"].build_analyzer()

    def _oov_rate(self, text: str) -> float:
        """Share of this input's tokens the vectorizer has never seen. No labels needed."""
        tokens = self._analyze(text)
        if not tokens:
            return 1.0
        unseen = sum(1 for t in tokens if t not in self._vocab)
        return round(unseen / len(tokens), 4)

    def predict_one(self, text: str) -> Prediction:
        t0 = time.perf_counter()
        proba = float(self.pipeline.predict_proba([text])[0, 1])
        latency_ms = (time.perf_counter() - t0) * 1000      # ← per-request cost only
        label = self.classes[1] if proba >= self.threshold else self.classes[0]
        return Prediction(
            request_id=uuid.uuid4().hex[:8],
            ts=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            model_version=self.version,
            input=text,
            label=label,
            probability=round(proba, 4),
            threshold=self.threshold,
            latency_ms=round(latency_ms, 2),
            oov_rate=self._oov_rate(text),
        )


def log_prediction(pred: Prediction) -> None:
    """Append one JSON object on one line. Append-only, never rewritten."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    row = asdict(pred)
    row["input"] = row["input"][:MAX_LOGGED_CHARS]          # truncate: privacy + disk
    row["input_chars"] = len(pred.input)                    # keep the true length
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
```

Four things to notice, because each one is a rubric line:

1. **`predict_one` times only the prediction.** `load_ms` is stored separately. Two different costs, two different numbers.
2. **The vocabulary set and the analyzer are cached in `__init__`.** Building the analyzer per request would make your OOV monitoring slower than your model.
3. **`log_prediction` truncates the input.** You wrote down *why* in Should-have S6. Logging 2 MB of someone's text forever is a decision, and the default should be "keep less."
4. **`asdict(pred)`** means the log schema and the API response schema are the same dataclass. They cannot drift apart, because there is only one of them.

### Step 2 — `serve/service.py`, standard library only

```python
"""service.py — a tiny local prediction service. No Flask. No installs.

Run:  python serve/service.py
Then: curl -s http://127.0.0.1:8000/health
      curl -s -X POST http://127.0.0.1:8000/predict \
           -H 'Content-Type: application/json' \
           -d '{"text": "the acting was wonderful"}'
"""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from predictor import Predictor, log_prediction

MAX_BODY_BYTES = 100_000          # ~100 KB. Bigger than any real review, small
                                  # enough that nobody can fill your disk.
PREDICTOR: Predictor | None = None


class Handler(BaseHTTPRequestHandler):
    server_version = "ShipIt/1.0"

    # ---- helpers ---------------------------------------------------------
    def _send(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        """Silence the default stderr access log — we do our own, as JSON."""
        return

    # ---- routes ----------------------------------------------------------
    def do_GET(self):
        if self.path == "/health":
            self._send(200, {
                "status": "ok",
                "model_version": PREDICTOR.version,
                "threshold": PREDICTOR.threshold,
                "classes": PREDICTOR.classes,
                "load_ms": round(PREDICTOR.load_ms, 1),
            })
        else:
            self._send(404, {"error": "not found",
                             "routes": ["GET /health", "POST /predict"]})

    def do_POST(self):
        if self.path != "/predict":
            self._send(404, {"error": "not found",
                             "routes": ["GET /health", "POST /predict"]})
            return

        # CHECK 1 — body length declared, non-zero, and not absurd
        try:
            length = int(self.headers.get("Content-Length", 0))
        except ValueError:
            self._send(400, {"error": "Content-Length header is not an integer"})
            return
        if length <= 0:
            self._send(400, {"error": "empty body; expected {\"text\": \"...\"}"})
            return
        if length > MAX_BODY_BYTES:
            self._send(413, {"error": f"body too large ({length} bytes); "
                                      f"limit is {MAX_BODY_BYTES}"})
            return

        raw = self.rfile.read(length)

        # CHECK 2 — it must actually be JSON
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            self._send(400, {"error": f"invalid JSON: {e}"})
            return

        # CHECK 3 — it must be an object with the field we promised
        if not isinstance(payload, dict) or "text" not in payload:
            self._send(400, {"error": "expected a JSON object with a 'text' field",
                             "example": {"text": "the film was wonderful"}})
            return

        # CHECK 4 — the field must be a non-empty string
        text = payload["text"]
        if not isinstance(text, str) or not text.strip():
            self._send(400, {"error": "'text' must be a non-empty string",
                             "got_type": type(text).__name__})
            return

        # Only now do we touch the model.
        try:
            pred = PREDICTOR.predict_one(text)
            log_prediction(pred)
        except Exception as e:                       # never leak a stack trace
            self._send(500, {"error": "prediction failed",
                             "type": type(e).__name__})
            return

        self._send(200, {
            "request_id": pred.request_id,
            "label": pred.label,
            "probability": pred.probability,
            "threshold": pred.threshold,
            "model_version": pred.model_version,
            "latency_ms": pred.latency_ms,
        })


def main():
    global PREDICTOR
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default=None, help="artifact name, or 'latest'")
    ap.add_argument("--threshold", type=float, default=None)
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()

    PREDICTOR = Predictor(version=args.version, threshold=args.threshold)
    print(f"loaded {PREDICTOR.version} in {PREDICTOR.load_ms:.0f} ms "
          f"(threshold {PREDICTOR.threshold})")

    # 127.0.0.1, NOT 0.0.0.0 — see the note below. This matters.
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"serving on http://127.0.0.1:{args.port}   (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down")
        server.server_close()


if __name__ == "__main__":
    main()
```

> ⚠️ **`127.0.0.1` versus `0.0.0.0`, and why you must know the difference.** `127.0.0.1` means "only this computer can reach it." `0.0.0.0` means "anything on the network can reach it" — the café wifi, the school network, everyone. Your service has no authentication, no rate limit, and a model that will happily answer a million requests. Bind to `127.0.0.1` and be able to say that sentence out loud in your demo. It is one of the questions in the question bank.

### Step 3 — prove it works

```bash
# terminal 1
$ python serve/service.py
loaded sentiment_v1 in 38 ms (threshold 0.5)
serving on http://127.0.0.1:8000   (Ctrl+C to stop)
```

```bash
# terminal 2
$ curl -s http://127.0.0.1:8000/health
{"status": "ok", "model_version": "sentiment_v1", "threshold": 0.5,
 "classes": ["negative", "positive"], "load_ms": 38.4}

$ curl -s -X POST http://127.0.0.1:8000/predict \
    -H 'Content-Type: application/json' \
    -d '{"text": "wonderful acting and a script with real warmth"}'
{"request_id": "9c1f4b7a", "label": "positive", "probability": 0.8213,
 "threshold": 0.5, "model_version": "sentiment_v1", "latency_ms": 1.74}
```

### Step 4 — the four malformed requests (Must-have M9)

Run all four. Paste the transcript into your write-up. The service must still be alive at the end.

```bash
# 1. empty body
$ curl -s -X POST http://127.0.0.1:8000/predict -d ''
{"error": "empty body; expected {\"text\": \"...\"}"}

# 2. invalid JSON
$ curl -s -X POST http://127.0.0.1:8000/predict -d '{"text": '
{"error": "invalid JSON: Expecting value: line 1 column 10 (char 9)"}

# 3. wrong field name
$ curl -s -X POST http://127.0.0.1:8000/predict -d '{"review": "great"}'
{"error": "expected a JSON object with a 'text' field",
 "example": {"text": "the film was wonderful"}}

# 4. right field, wrong type
$ curl -s -X POST http://127.0.0.1:8000/predict -d '{"text": 42}'
{"error": "'text' must be a non-empty string", "got_type": "int"}

# 5. still alive?
$ curl -s http://127.0.0.1:8000/health
{"status": "ok", "model_version": "sentiment_v1", ...}
```

**That last line is the actual test.** Four pieces of garbage, four clear refusals, zero crashes. A service that returns a helpful 400 and keeps running is the difference between an experiment and a product.

### Step 5 — generate 100+ log lines

```bash
$ for i in $(seq 1 100); do
    curl -s -X POST http://127.0.0.1:8000/predict \
      -H 'Content-Type: application/json' \
      -d "{\"text\": \"test review number $i, the acting was fine\"}" > /dev/null
  done

$ wc -l logs/predictions.jsonl
     103 logs/predictions.jsonl

$ head -1 logs/predictions.jsonl
{"request_id": "9c1f4b7a", "ts": "2026-03-14T10:02:55.118Z",
 "model_version": "sentiment_v1", "input": "wonderful acting and a script with real warmth",
 "label": "positive", "probability": 0.8213, "threshold": 0.5,
 "latency_ms": 1.74, "oov_rate": 0.0, "input_chars": 45}

$ python eval/read_logs.py
requests      : 103
by version    : {'sentiment_v1': 103}
by label      : {'positive': 61, 'negative': 42}
latency p50   : 1.61 ms
latency p95   : 3.94 ms
latency max   : 41.20 ms
mean prob     : 0.523
```

You now have a service, a log, and the numbers to describe it. **That is the milestone.**

### 🅑 Path B — what changes for images

Everything above is identical except the input. Three decisions to make, in writing:

| Decision | The easy answer | The real answer |
|---|---|---|
| How does an image get into JSON? | a **file path** on the same machine: `{"path": "cat.png"}` | **base64** in the JSON string — works over a network, but inflates size by 33% and you must handle decode errors as a fifth 400 case |
| Where does the eval transform live? | `model_def.py`, imported by `train.py` and `predictor.py` | there is no other acceptable answer; a duplicated normalization constant is the classic Path B bug |
| What is your OOV-equivalent monitoring number? | **mean pixel brightness** or **mean softmax confidence** | either is fine; both are computable with no labels, which is the requirement |

```python
# predictor.py (Path B extract)
import base64, io
from PIL import Image
import torch
from model_def import CLASSES, EVAL_TRANSFORM, SmallCNN

class Predictor:
    def __init__(self, version=None, threshold=None):
        self.version = resolve_version(version)
        self.meta = json.loads((ARTIFACTS / f"{self.version}.metadata.json").read_text())
        self.model = SmallCNN()
        self.model.load_state_dict(
            torch.load(ARTIFACTS / f"{self.version}.pt", map_location="cpu"))
        self.model.eval()              # ⚠️ NOT optional. Dropout/BatchNorm depend on it.

    def predict_one(self, image_b64: str):
        img = Image.open(io.BytesIO(base64.b64decode(image_b64))).convert("RGB")
        x = EVAL_TRANSFORM(img).unsqueeze(0)          # (1, 3, 32, 32)
        t0 = time.perf_counter()
        with torch.no_grad():                         # ⚠️ also not optional
            probs = torch.softmax(self.model(x), dim=1)[0]
        latency_ms = (time.perf_counter() - t0) * 1000
        idx = int(probs.argmax())
        return Prediction(..., label=CLASSES[idx], probability=float(probs[idx]), ...)
```

`model.eval()` and `torch.no_grad()` are both Module 6 rules and both are silent when you forget them: `eval()` makes your answers change run to run, `no_grad()` just wastes memory and time building a graph nobody will use.

---

## ⚠️ Common Capstone Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Loading the model inside the request handler | It's the obvious place to put it, and it works | Load once at startup. Per-request loading turns a 2 ms prediction into 400 ms, and your p95 becomes meaningless. `Predictor()` is constructed in `main()`, before `serve_forever()`. |
| The CLI and the service give different answers | You wrote the prediction logic twice, and then fixed a bug in only one | Rule 2. One `Predictor` class. If prediction logic appears in `predict.py` or `service.py`, that's a bug regardless of whether it currently works. |
| Preprocessing that lives in a notebook cell | The notebook trained fine, so the step feels "done" | If it isn't inside the artifact (Path A) or inside `model_def.py` (Path B), it will be forgotten. Ask: "if I deleted my notebook right now, could I still predict correctly?" |
| `model.joblib` with no version | Versioning feels like something big teams do | The first time you retrain, you overwrite the model that was working and you cannot go back. Version from file number one. It costs six characters. |
| Logging only the label | The label is what you care about | You cannot debug a wrong answer without the probability, the threshold, the version, and the input. Log all five or you're logging nothing useful. |
| Reporting mean latency only | It's the number `statistics.mean` gives you | The mean hides the tail. Our p50 was 1.61 ms and the max was 41.20 ms — the slow one is the first request, and only p95 shows it. |
| Binding to `0.0.0.0` | Every tutorial does it, because tutorials run in containers | You are exposing an unauthenticated service to your whole network. `127.0.0.1`. Know why. |
| Subgroup metrics with no `n` | The table looks cleaner without it | `1.000` on 4 rows and `1.000` on 400 rows are completely different claims. Sizes always, and "too small to conclude from" under about 10. |
| A model card that says "may contain bias" | It sounds responsible and costs nothing | Content-free. Name the group, give the number, give the size: "0.667 on the 6 test reviews containing a negation, versus 1.000 on the 18 without." |
| A monitoring plan built on accuracy | Accuracy is the metric you know | In production nobody gives you labels, so you can never compute it. Pick a number computable from **inputs and outputs alone**. |
| Retraining on your own predictions | It looks like free labelled data | It's a feedback loop. The model learns its own mistakes and gets *more* confident about them. Write down that you won't. |
| Shipping v2 because it's v2 | Newer feels better | Compare on the *same* test set and reject it if it isn't better. A written rejection scores higher than an unjustified upgrade. |
| Testing only in the terminal you trained in | Everything is already imported and cached | Must-have M13 exists for this. Brand-new terminal, fresh process, cold start. That is the only test that reflects a user's experience. |

---

## 📊 Grading Rubric

Score each of the seven rows 1–4. **7–12 = Beginning · 13–18 = Developing · 19–24 = Proficient · 25–28 = Exceptional.**

| Criterion | 1 · Beginning | 2 · Developing | 3 · Proficient | 4 · Exceptional |
|---|---|---|---|---|
| **1. The artifact** | Model exists only in a notebook, or is re-fitted when you predict | A saved file, but some preprocessing happens outside it, or the filename has no version | **Versioned artifact + metadata.json**, all preprocessing frozen inside, loads in a fresh process, `LATEST` pointer present | Two versions coexist and can be selected at runtime; metadata records library versions and a commit hash; a rejected version is documented with its comparison table |
| **2. Separation of training and serving** | `predict.py` imports the training script, or calls `.fit()` | Mostly separate, but a shared file still contains training code | **Rule 1 grep returns nothing**; `serve/` imports only `predictor.py` and `model_def.py`; cold start works in a brand-new terminal | The directory structure makes the rule mechanically checkable, and the grep is included in the write-up as evidence rather than as a claim |
| **3. The interfaces (CLI + service)** | One of the two is missing or doesn't run | Both exist, but they duplicate prediction logic, or the service loads the model per request | **One `Predictor` class used by both**; `GET /health` and `POST /predict` work; model loaded once at startup; bound to `127.0.0.1` | `--version` and `--threshold` on both; a `--json` output mode; three golden tests that fail loudly; a 60-second quickstart a stranger can follow |
| **4. Robustness** | The service crashes on bad input, or was never tested with any | Some validation; one or two malformed cases handled | **All four malformed cases** return a clear 400/413 with an actionable message, service stays alive, and the transcript proves it | A body-size limit with a justified number; no stack traces leaked to the client; a fifth case they invented themselves (unicode, huge unicode, wrong content-type) |
| **5. Logging and latency** | No log, or a log of labels only | A log with most fields; a single mean latency reported | **JSONL with request id, timestamp, version, input, output, probability, threshold, latency_ms**; 100+ real lines; p50 and p95 reported | Cold-start and per-request latency reported as separate numbers; a written privacy decision about what is and isn't logged; the log read back by a script that produces the report automatically |
| **6. Model card and subgroup metrics** | No card, or a card with only a headline accuracy | A card with most sections; overall metrics only, or subgroups without sizes | **All six sections**; metrics with threshold and test-set size; **two or more subgroups with `n` stated**; three concrete failure modes with real example inputs | A subgroup gap is traced to a *mechanism* from an earlier module (e.g. bag-of-words discarding word order), small-`n` groups explicitly flagged as inconclusive, and an out-of-scope use that is genuinely tempting |
| **7. Monitoring plan** | Absent, or "I would check it sometimes" | Names a metric, but one that needs labels, or gives no threshold or action | **One number, computable without labels**, with a measured baseline, an alert level, and a specific action | Explains *why that number degrades for this model architecture*; names something they would deliberately NOT do (e.g. self-training) and why; states what would make them retire the model entirely |

---

## 🎤 Show Your Work

### The 10-minute live demo

You are not presenting slides. You have two terminals open and you are going to break your own service on purpose.

```
   ┌─────────┬────────────────────────────────────────────────────────────┐
   │  0:00   │  THE CONTRACT (60 s)                                       │
   │         │  "One prediction is about one ___. It takes ___ and        │
   │         │   returns ___. A false negative costs ~50× a false         │
   │         │   positive, so my threshold is 0.42, not 0.5."             │
   ├─────────┼────────────────────────────────────────────────────────────┤
   │  1:00   │  COLD START (60 s)  ← open a BRAND NEW terminal, live      │
   │         │  Run the CLI. Nothing pre-loaded. It answers.              │
   │         │  Then run the Rule 1 grep and show the empty output.       │
   ├─────────┼────────────────────────────────────────────────────────────┤
   │  2:00   │  THE SERVICE (2 min)                                       │
   │         │  Start it. /health. One good prediction. Say the load time │
   │         │  and the per-request time as two different numbers.        │
   ├─────────┼────────────────────────────────────────────────────────────┤
   │  4:00   │  BREAK IT (2 min)  ← the bit that wins the room            │
   │         │  Four malformed requests, live. Then /health again to      │
   │         │  prove it's still up. Say: "a service that dies on bad     │
   │         │  input is not a service."                                  │
   ├─────────┼────────────────────────────────────────────────────────────┤
   │  6:00   │  THE LOG (90 s)                                            │
   │         │  head -1 the JSONL. Then read_logs.py. p50, p95, and the   │
   │         │  41 ms outlier — and explain that it's the first request.  │
   ├─────────┼────────────────────────────────────────────────────────────┤
   │  7:30   │  WHERE IT BREAKS (90 s)                                    │
   │         │  The subgroup table. Point at the worst row, say its n,    │
   │         │  and give the mechanism. Then demo one failure LIVE.       │
   ├─────────┼────────────────────────────────────────────────────────────┤
   │  9:00   │  THE MONITORING NUMBER (60 s)                              │
   │         │  Name it. Say why it needs no labels. Give the alert       │
   │         │  level, the action, and the one thing you would not do.    │
   └─────────┴────────────────────────────────────────────────────────────┘
```

> 🔑 **Demo your own failure on purpose.** Have one input ready that your model gets wrong — ideally a negation trap from your subgroup analysis — and run it live. Then explain the mechanism with a coefficient. Nothing else you can do in ten minutes builds as much trust as showing someone the hole in your own work and proving you understand its shape.

### The question bank — rehearse all eight

| They ask | The shape of a good answer |
|---|---|
| *"What happens if I send it something weird?"* | Don't answer — demo it. Four malformed requests, then `/health`. Then: "the body limit is 100 KB, which is 30× my longest training review." |
| *"How fast is it?"* | Two numbers, never one. "38 ms to load the model once at startup; p50 1.6 ms and p95 3.9 ms per request over 103 logged requests." |
| *"How do you know it still works next month?"* | Name the number. "OOV rate, weekly, currently 0.14, alert at 0.25. I can compute it without labels, which matters because in production nobody tells me the right answer." |
| *"Someone says it got their comment wrong. What do you do?"* | Walk the log. "I grep the request id, get the exact input, the probability, the threshold, and the model version. If it's a negation, I can already predict the mechanism from my subgroup table." |
| *"Why 127.0.0.1?"* | "No auth, no rate limiting. `0.0.0.0` would expose an unauthenticated service to the whole network. Localhost is the correct default and going wider is a decision with requirements attached." |
| *"Is v2 better?"* | "No, and here's the table on the same test set: same accuracy, worse F1, 31% slower, 2.5× the file. I kept v1 live and wrote down why." |
| *"Who shouldn't use this?"* | Point at the out-of-scope section and read the tempting one. "Not for moderating anything that gets someone banned. It outputs a suggestion, not a decision, and its recall on negations is 0.667 on six rows." |
| *"Could you just retrain it on the new data automatically?"* | "I could, and I deliberately won't retrain on my own predictions — that's a feedback loop where the model learns its own mistakes and gets more confident about them. New training data has to be labelled by a human." |

### 🚫 The banned words

```
   production-ready  ·  scalable  ·  it just works  ·  99% accurate
   robust (without a test)  ·  real-time  ·  enterprise  ·  seamless
```

`production-ready` is banned hardest. Nothing with one developer, no auth, and 103 log lines is production-ready — and saying so tells an experienced listener you don't know what the phrase costs. Say what you actually built: *"it runs locally, it logs every prediction, and I know its p95."*

### 🚀 Three stretch directions

**1. The rollback drill (~1 h).**
Ship a deliberately broken v3 — train it on 10 rows, or set the threshold to 0.99. Point `LATEST` at it. Restart the service. Watch your golden tests fail and your prediction mix collapse to all-negative in the log. Now **time yourself rolling back**: edit `LATEST`, restart, re-run `tests.py`, confirm.

Write down the number of seconds. That number has a name in industry — *mean time to recovery* — and it is one of the few operational metrics that genuinely predicts whether a team can be trusted with something important. Most people have never measured their own.

**2. The drift simulator (~1.5 h).**
Write a script that sends your service 200 requests drawn from a *different* domain than your training data — if you trained on film reviews, send restaurant reviews, or comments full of slang and emoji your tokenizer will delete. Do not retrain. Plot `oov_rate` over request number from your log file.

You should see it climb and stay high. That plot is what drift actually looks like, and having generated one yourself means you will recognise the shape when it happens for real. Then answer the hard question honestly: **at what OOV rate did your accuracy actually start dropping?** Label 30 of the drifted inputs by hand and find out. Most people guess too high.

**3. The stranger test (~1 h).**
Give your `README.md` and the folder to someone who has never seen the project — a friend, a sibling, a teacher — and watch them try to get a prediction out of it. **Say nothing.** Start a timer.

Note every place they hesitate, every command they mistype, every error message that doesn't tell them what to do next. That list is the highest-value feedback in this entire capstone, because "the model works but nobody can run it" is the single most common way real ML projects fail — and it is invisible from the inside. If they can't get a prediction in 60 seconds, your quickstart is wrong, not them.

---

## 🔑 Key Takeaways

- **The artifact is the deliverable, not the notebook.** If your preprocessing lives anywhere except inside the saved object, it will eventually be forgotten — and it will fail silently, not loudly.
- **One `Predictor`, two interfaces.** The moment prediction logic exists in two places, they begin to drift, and the drift is invisible until someone reports a bug you cannot reproduce.
- **Log the inputs, the output, the probability, the threshold, the version, and the latency.** A log that only records labels cannot answer a single question you will actually be asked.
- **Two latency numbers, always: cold start and per request.** And report p95, because the mean hides the tail that users actually feel.
- **Subgroup metrics with sizes, or don't bother.** "1.000 accuracy" on four rows is not a result; it's four rows.
- **A monitoring plan you can't run isn't a plan.** In production nobody hands you labels, so your staleness number must be computable from inputs and outputs alone.
- **Rejecting v2 in writing is stronger work than shipping it.** Engineering is mostly deciding *not* to change things, with evidence.

---

## ✅ Final Checklist Before You Demo

```
   THE ARTIFACT
   □ model/train.py runs from the command line and prints a test score
   □ Every preprocessing step is inside the artifact (or model_def.py)
   □ Filename has a version: sentiment_v1.joblib, not model.joblib
   □ A .metadata.json sits beside it, generated by the script
   □ artifacts/LATEST contains one line naming the live version
   □ A second version exists and can be selected with --version

   THE SEPARATION
   □ grep -rE "\.fit\(|train_test_split|optimizer|DataLoader" serve/  → empty
   □ serve/ imports only predictor.py and model_def.py
   □ Cold-start test done in a BRAND NEW terminal

   THE INTERFACES
   □ One Predictor class; no prediction logic anywhere else
   □ Model loaded once, at startup, not per request
   □ predict.py works with a positional argument and with --json
   □ GET /health returns version, threshold, classes, load_ms
   □ POST /predict returns the exact contract fields
   □ Bound to 127.0.0.1 and I can say why in one sentence
   □ tests.py passes all three golden cases

   ROBUSTNESS
   □ Empty body        → 400, service alive
   □ Invalid JSON      → 400, service alive
   □ Missing field     → 400 with an example, service alive
   □ Wrong type        → 400 naming the type it got, service alive
   □ Oversized body    → 413 naming the limit, service alive
   □ /health still 200 after all five

   THE LOG
   □ logs/predictions.jsonl has 100+ lines
   □ Every line has: request_id, ts, model_version, input, label,
     probability, threshold, latency_ms
   □ read_logs.py prints count, per-version, per-label, p50, p95, max
   □ Cold-start ms and per-request ms reported as SEPARATE numbers
   □ A written decision about what I log and what I truncate, and why

   THE DOCUMENTS
   □ MODEL_CARD.md has all six sections
   □ Subgroup table with n on EVERY row
   □ Any group under n=10 flagged as too small to conclude from
   □ Three failure modes, each with a real example input and output
   □ Out-of-scope uses, including one that is genuinely tempting
   □ MONITORING.md fits on one page
   □ It names ONE number, computable without labels
   □ Baseline value, alert level, and a specific action
   □ One thing I would deliberately NOT do, and why

   THE DEMO
   □ Rehearsed out loud, timed, under 10 minutes
   □ Two terminals open before I start
   □ One input ready that my model gets WRONG, with the mechanism
   □ All eight question-bank answers rehearsed
   □ Zero banned words
```

---

## 🎓 You Have Finished Level 3

Look at what you can do now that you could not do twenty-four weeks ago.

You can take a vague sentence from a person with a budget and turn it into a defined `X`, a defined `y`, and a metric you commit to before you look. You can catch the column that already contains the answer. You can name the error that costs more and move the threshold until the arithmetic agrees with you. You can compute a gradient with a pen, then check the machine's answer against yours to eight decimal places. You can write backpropagation from memory. And now you can hand somebody a folder and a URL and walk away, because the thing runs, logs, versions, and tells the truth about where it breaks.

Twenty-four weeks ago, `fit()` was a box.

Level 4 opens the last one. You will build the sequence models that read text in order — fixing the exact weakness Module 9 measured when bag-of-words called two opposite reviews the most similar pair in the corpus. Then **attention**, and a small transformer you train yourself. Then how the large models are actually made, how to prompt them, how to give them memory with the embeddings you already understand, and how to make them use tools.

None of it will feel like magic, because you built the floor it stands on — and, more importantly, because you now ask a different first question. Not *"how accurate is it?"* but *"how would I know when it stops working?"*

Take the [assessment](assessment.md) if you haven't. Then:

> ### 👉 **[Level 4 — Innovator](../level-4-innovator/)**

---

[⬅ Module 9](module-09-classic-nlp.md) · [Level 3 Home](README.md) · [Assessment](assessment.md) · [Glossary](glossary.md) · [Level 4 ➡](../level-4-innovator/)

*You froze the preprocessing, versioned the artifact, logged the latency, named the failure modes, and wrote down the number that would tell you it had gone stale. That is shipping. See you in Level 4.*

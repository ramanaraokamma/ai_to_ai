# 🗺️ AI Academy — Complete Curriculum Map

**4 levels · 9 modules each · 36 modules total · ~2–3 years · one learner, grade 6 → grade 12**

> ### 📚 This map covers the **self-study module track**
>
> Levels 1, 2 and 3 also exist as a **36-week taught course** — the same content re-cut into weekly
> classes, with three books a week (teacher guide · student guide · workbook), 1,140 illustrations,
> term tests and project banks. If an adult is teaching the learner, that is the edition to use.
>
> → [Level 1, 36 weeks](levels/level-1-explorer/36-week-course/README.md) ·
> [Level 2, 36 weeks](levels/level-2-builder/36-week-course/README.md) ·
> [Level 3, 36 weeks](levels/level-3-engineer/36-week-course/README.md) ·
> [how the two editions differ](README.md#-two-ways-through-this-course)
>
> Level 4 is self-study only for now, so this map is the plan for it.

> **How to read this map.** Every module is one week (~3–5 hours). Every module has one mini-project.
> Every module depends **only** on modules before it — there are no forward references anywhere in
> this course. The six core ideas (data, representation, model, learning signal, evaluation, human
> impact) come back at every level, deeper each time. That's the spiral.

**Jump to:** [Level 1 Explorer](#-level-1--explorer) · [Level 2 Builder](#-level-2--builder) · [Level 3 Engineer](#️-level-3--engineer) · [Level 4 Innovator](#-level-4--innovator) · [Spiral Table](#-the-spiral-progression) · [Dependency Graph](#-prerequisite-dependency-graph)

---

## 🧭 Level 1 — Explorer

**Grade 6 · ~12 weeks · zero code · Tools: paper & index cards, Google Teachable Machine, Scratch, Quick Draw!, spreadsheets**

> **Big idea:** A machine can learn a rule from examples instead of being told the rule.

**Level pack:** [README](levels/level-1-explorer/README.md) · [Capstone](levels/level-1-explorer/capstone.md) · [Assessment](levels/level-1-explorer/assessment.md) · [Glossary](levels/level-1-explorer/glossary.md)

| # | Module | You'll learn | Mini-project | Time |
|:--:|---|---|---|:--:|
| 1 | [**What AI Is, What It Isn't, and Where It's Hiding**](levels/level-1-explorer/module-01-what-ai-is-and-isnt.md) | What "artificial intelligence" actually means; the difference between a machine following rules someone wrote and a machine that learned from examples; the three families (rules, learning, generating); why "smart" is the wrong word | **AI Spotter's Log** — hunt your own 24 hours, log 15 systems, sort each into rules vs learned, and defend the 3 hardest calls | ~2.5 h |
| 2 | [**Data Is Everywhere: Rows, Columns, and Honest Tables**](levels/level-1-explorer/module-02-data-is-everywhere.md) | What data *is*; rows = examples, columns = attributes; numbers vs categories vs text vs images; missing and messy values; where data comes from and who it came from | **Your Life In 30 Rows** — collect a real 30-row spreadsheet about your own week (sleep, screen time, mood) and write its data card | ~3 h |
| 3 | [**Patterns and Rules: When Writing Rules Stops Working**](levels/level-1-explorer/module-03-patterns-and-rules.md) | Spotting patterns; writing if-then rules by hand; rule explosion; edge cases; the exact moment a human-written rulebook becomes impossible — and why that invented machine learning | **Rulebook vs Reality** — write a spam-detector rulebook for 20 texts, then watch it fail on 10 fresh ones and count the failures | ~2.5 h |
| 4 | [**Features and Labels: How a Machine Describes a Thing**](levels/level-1-explorer/module-04-features-and-labels.md) | Features (what we measure) vs labels (what we want to predict); turning a real object into a row of numbers; good vs useless features; classification vs prediction of a number | **Feature Card Deck** — turn 20 real objects into feature rows, hand the deck to someone else, and see if they can label using features alone | ~3 h |
| 5 | [**Learning From Examples: Train Your First Model**](levels/level-1-explorer/module-05-learning-from-examples.md) | What "training" means; examples in → model out; how more and better examples change the result; confidence scores; that a model is just a learned guessing machine | **Three-Class Classifier** — train a Teachable Machine model to tell apart three things you own, and record how confidence changes | ~3 h |
| 6 | [**Train, Test, Trust: Why You Hide Some Examples**](levels/level-1-explorer/module-06-train-test-trust.md) | Why testing on training examples is cheating; the train/test split; accuracy as a fraction and a percentage; memorizing vs generalizing; the first taste of overfitting | **The Hidden Ten** — split your photos 80/20, test on the hidden ones, and compute accuracy by hand on a scoring sheet | ~3 h |
| 7 | [**How Computers See: Pixels, Grids, and Edges**](levels/level-1-explorer/module-07-how-computers-see.md) | An image is a grid of numbers; grayscale and RGB; resolution; what a filter does; edges as the first "feature" a vision system finds; why lighting and background fool models | **Pixel Lab** — draw on graph paper as numbers, then run a 3×3 edge filter by hand in a spreadsheet and see the outline appear | ~3 h |
| 8 | [**How Computers Read and Chat: Words, Guesses, Autocomplete**](levels/level-1-explorer/module-08-how-computers-read-and-chat.md) | Text as data; splitting sentences into tokens; counting word pairs; next-word prediction as the engine behind chatbots; why a chatbot can be confidently wrong | **The Human Language Model** — build a tally-mark next-word predictor from a paragraph, then wire a Scratch chatbot that uses it | ~3 h |
| 9 | [**Fair, Private, and Honest: The Human Side of AI**](levels/level-1-explorer/module-09-fair-private-honest-ai.md) | Where bias sneaks in through data; who is missing from a dataset; what personal data is and why it leaks; deepfakes and misinformation; giving credit; when *not* to trust an AI | **Fairness Audit Poster** — audit a real AI product you use, then run a bias test on your own Module 5 model and publish both results | ~3 h |

### 🎪 [Level 1 Capstone — *The AI Fair Booth*](levels/level-1-explorer/capstone.md) (~6 h)
Build a booth you could set up at a school fair: a trained Teachable Machine classifier that solves a
real problem in your house, a Scratch app that reacts to its predictions, a printed **data card**
(what data, how much, collected how), a **test sheet** with honest accuracy on held-out examples, and a
**bias report** naming one group of inputs your model handles badly. Present it to an adult for 5 minutes
and answer their questions without using the word "magic."

---

## 🔨 Level 2 — Builder

**Grades 7–8 · ~20 weeks · Python 3 · Tools: Python, VS Code/JupyterLab, numpy, pandas, matplotlib, scikit-learn**

> **Big idea:** If you can write code, you can turn a table of data into a model that predicts.

**Level pack:** [README](levels/level-2-builder/README.md) · [Capstone](levels/level-2-builder/capstone.md) · [Assessment](levels/level-2-builder/assessment.md) · [Glossary](levels/level-2-builder/glossary.md)

| # | Module | You'll learn | Mini-project | Time |
|:--:|---|---|---|:--:|
| 1 | [**Python From Zero: Variables, Types, and Output**](levels/level-2-builder/module-01-python-from-zero.md) | Running Python; `print`; variables; strings, integers, floats, booleans; f-strings; `input`; type conversion; comments; reading an error message without panic | **About-Me Bot** — a program that asks 6 questions and prints a formatted profile card with two computed numbers | ~3 h |
| 2 | [**Decisions and Loops: Programs That Choose and Repeat**](levels/level-2-builder/module-02-decisions-and-loops.md) | `if` / `elif` / `else`; comparison and logical operators; `for` and `while`; `range`; accumulator variables; `break` and `continue`; off-by-one bugs | **Guess & Grade** — a number-guessing game with hints and attempt limits, plus a looping grade calculator | ~3.5 h |
| 3 | [**Functions and Lists: Building Your Own Tools**](levels/level-2-builder/module-03-functions-and-lists.md) | Defining functions; parameters, arguments, `return`; scope; lists, indexing, slicing, `append`; iterating lists; list comprehensions; writing your first reusable module | **Stats Toolkit** — your own `stats.py` with mean, median, min, max, and range, verified on typed-in cricket scores | ~3.5 h |
| 4 | [**Dictionaries and Datasets: Your First Data in Code**](levels/level-2-builder/module-04-dictionaries-and-datasets.md) | Dictionaries as labelled rows; list-of-dicts as a dataset; nesting; looping over records; filtering and grouping in plain Python; reading and writing CSV with the `csv` module | **Record Store** — build a 30-record dataset in code, write `filter_by` / `group_count` functions, save to CSV and load it back | ~4 h |
| 5 | [**NumPy: Thinking in Arrays**](levels/level-2-builder/module-05-numpy-arrays.md) | Why loops are slow and arrays are fast; creating arrays; shape and dtype; elementwise math; broadcasting; axis-wise sums and means; boolean masks; a row of numbers as a **vector** | **Vectorized Gradebook** — compute per-student and per-test statistics and normalize every score, with zero `for` loops | ~4 h |
| 6 | [**Pandas: Loading, Cleaning, and Interrogating a Table**](levels/level-2-builder/module-06-pandas-tables.md) | Series and DataFrame; selecting rows and columns; `loc` vs `iloc`; filtering; missing values; fixing dtypes; dropping duplicates; new columns; `sort_values`, `value_counts`, `groupby` | **Mess Detective** — clean a deliberately broken 40-row DataFrame and answer 6 questions about it with `groupby` | ~4 h |
| 7 | [**Charts That Tell The Truth: Visualization**](levels/level-2-builder/module-07-visualizing-data.md) | Choosing a chart for a question; line, bar, scatter, histogram, box; axes, labels, titles, legends; distributions vs relationships; how axis tricks lie; correlation is not causation | **Five-Chart Data Story** — five labelled charts that answer one question, plus one deliberately misleading chart and its honest fix | ~3.5 h |
| 8 | [**Your First Real Model: kNN and the Train/Test Rule**](levels/level-2-builder/module-08-first-model-knn.md) | The ML mindset (features X, labels y, fit, predict); distance between rows; k-nearest neighbors; `train_test_split`; `accuracy_score`; why scaling matters for distance; choosing k | **Classifier Lab** — train a kNN classifier on a built-in sklearn dataset and plot accuracy against k from 1 to 25 | ~4 h |
| 9 | [**Trees, Lines, and the Overfitting Trap**](levels/level-2-builder/module-09-trees-lines-and-overfitting.md) | Decision trees and how to read one; linear regression and the line of best fit; MAE and R²; regression vs classification; underfitting vs overfitting; the train-score/test-score gap | **Model Bake-Off** — compare kNN, a decision tree, and linear regression on the same split, and plot the tree-depth overfitting curve | ~4.5 h |

### 🔎 [Level 2 Capstone — *Data Detective*](levels/level-2-builder/capstone.md) (~10 h)
Pick a question you actually care about. Build or collect a dataset of at least 100 rows. Clean it in
pandas, chart it five ways, then train and honestly compare three models on a proper train/test split.
Deliver one notebook that reads like a story: question → data → cleaning log → charts → models →
results table → **what I got wrong** → what I'd do with more data. Include one paragraph on whose data
this is and what it would mean to be wrong about a real person.

---

## ⚙️ Level 3 — Engineer

**Grades 9–10 · ~24 weeks · Tools: scikit-learn, NumPy, pandas, matplotlib, PyTorch, torchvision, joblib**

> **Big idea:** A model is one component of a measured, engineered, shippable pipeline.

**Level pack:** [README](levels/level-3-engineer/README.md) · [Capstone](levels/level-3-engineer/capstone.md) · [Assessment](levels/level-3-engineer/assessment.md) · [Glossary](levels/level-3-engineer/glossary.md)

| # | Module | You'll learn | Mini-project | Time |
|:--:|---|---|---|:--:|
| 1 | [**The Supervised Pipeline, End to End**](levels/level-3-engineer/module-01-the-supervised-pipeline.md) | Framing a problem as supervised learning; data audit; train/validation/test three-way split; a dumb baseline you must beat; `sklearn.Pipeline`; saving and loading a model with `joblib`; the model card | **Pipeline v1** — one script that goes raw rows → split → baseline → model → metrics → saved artifact → model card, and runs end to end | ~5 h |
| 2 | [**Feature Engineering: Turning Reality Into Numbers**](levels/level-3-engineer/module-02-feature-engineering.md) | Standardization and min-max scaling; one-hot and ordinal encoding; binning; date and text-derived features; interaction features; imputation done correctly; **data leakage** and how to spot it | **Beat The Baseline** — improve Module 1's score using *only* new features inside a `ColumnTransformer`, and find the planted leakage bug | ~5 h |
| 3 | [**Beyond Accuracy: Confusion Matrix, Precision, Recall**](levels/level-3-engineer/module-03-evaluation-metrics.md) | Why accuracy lies on imbalanced data; TP/FP/FN/TN; precision, recall, F1; the threshold dial; ROC and precision-recall curves; k-fold cross-validation; matching the metric to the real-world cost | **Fraud Bench** — full metric report on a 1%-positive dataset, threshold tuned to a stated cost of errors, with cross-validated error bars | ~5 h |
| 4 | [**How Learning Happens: Loss and Gradient Descent**](levels/level-3-engineer/module-04-logistic-regression-gradient-descent.md) | The sigmoid; probabilities as outputs; log loss (cross-entropy); slope as a signal; the gradient descent update rule; learning rate; convergence and divergence; batch vs stochastic | **Descent From Scratch** — logistic regression trained by your own NumPy gradient descent, loss curve plotted, matched against scikit-learn | ~5.5 h |
| 5 | [**Neural Networks From Scratch: Neurons and Backprop**](levels/level-3-engineer/module-05-neural-networks-from-scratch.md) | A neuron as weighted sum + activation; layers and hidden units; ReLU, sigmoid, softmax; the forward pass by hand; the chain rule; backpropagation; weight initialization | **NumPy Brain** — a 2-layer MLP written entirely in NumPy that learns `make_moons`, verified with a numerical gradient check | ~6 h |
| 6 | [**PyTorch: Tensors, Autograd, and Real Training Loops**](levels/level-3-engineer/module-06-pytorch-deep-learning.md) | Tensors vs arrays; `requires_grad` and autograd; `nn.Module`; loss functions and optimizers; the canonical training loop; `Dataset`/`DataLoader`; GPU/MPS devices; saving weights and writing an inference script | **Same Brain, Real Framework** — rebuild Module 5's network in PyTorch, then train an MLP on FashionMNIST and ship an inference script | ~5.5 h |
| 7 | [**Convolutional Networks: Teaching a Model to See**](levels/level-3-engineer/module-07-cnns-for-images.md) | Why dense layers waste pixels; convolution, kernels, stride, padding; feature maps; pooling; CNN architecture; data augmentation; transfer learning with a pretrained backbone | **See It** — a small CNN on CIFAR-10, then a fine-tuned pretrained `resnet18`, compared with a confusion matrix of its worst mistakes | ~6 h |
| 8 | [**Learning Without Labels: k-Means and PCA**](levels/level-3-engineer/module-08-unsupervised-kmeans-pca.md) | Unsupervised vs supervised; k-means and its update loop; choosing k with elbow and silhouette; the curse of dimensionality; PCA and explained variance; using clusters and components as features | **Cluster Cartography** — cluster an unlabelled dataset, defend your k, project it with PCA, and give every cluster a human name | ~5 h |
| 9 | [**Classic NLP: Tokens, Bag-of-Words, Embeddings**](levels/level-3-engineer/module-09-classic-nlp.md) | Tokenization; normalization and stopwords; bag-of-words counts; TF-IDF weighting; sparse vs dense vectors; cosine similarity; what a word **embedding** is and why "king − man + woman" works | **Sentiment Engine** — a TF-IDF + logistic regression review classifier, its most-influential words inspected, and embeddings visualized with PCA | ~5.5 h |

### 🚢 [Level 3 Capstone — *Ship It*](levels/level-3-engineer/capstone.md) (~12 h)
Deployment and ops basics, for real. Take your best model from Modules 7 or 9 and make it a thing other
people can use: freeze the preprocessing into the saved artifact, write a `predict.py` CLI **and** a tiny
local HTTP service, version the model file, log every prediction with its inputs and latency, and write
the **model card** (intended use, training data, metrics per subgroup, known failure modes, out-of-scope
uses). Finish with a one-page **monitoring plan**: what number would tell you the model has gone stale,
and what you'd do about it.

---

## 🚀 Level 4 — Innovator

**Grades 11–12 · ~28 weeks · Tools: PyTorch, Hugging Face transformers/datasets/tokenizers, Anthropic Claude API (`claude-sonnet-5`), numpy**

> **Big idea:** Modern AI = attention + scale + a learning signal from humans — and you can build every piece.

**Level pack:** [README](levels/level-4-innovator/README.md) · [Capstone](levels/level-4-innovator/capstone.md) · [Assessment](levels/level-4-innovator/assessment.md) · [Glossary](levels/level-4-innovator/glossary.md)

| # | Module | You'll learn | Mini-project | Time |
|:--:|---|---|---|:--:|
| 1 | [**Deep Learning at Depth: Optimizers and Debugging**](levels/level-4-innovator/module-01-deep-learning-at-depth.md) | SGD → momentum → Adam/AdamW; learning-rate schedules and warmup; batch size effects; dropout, weight decay, early stopping; batch and layer normalization; residual connections; reading a loss curve like an X-ray | **Training Diagnostics Lab** — six controlled experiments on one network, each isolating one knob, distilled into your own tuning playbook | ~6 h |
| 2 | [**Sequence Models: RNNs, LSTMs, and the Memory Problem**](levels/level-4-innovator/module-02-sequence-models.md) | Why order matters; the recurrent loop and hidden state; unrolling through time; backprop through time; vanishing and exploding gradients; gates, LSTM/GRU; teacher forcing; sampling with temperature | **Name Generator** — a char-level RNN that invents plausible names, plus a plotted demonstration of gradients vanishing over long sequences | ~6 h |
| 3 | [**Attention and Transformers: Build a Tiny GPT**](levels/level-4-innovator/module-03-attention-and-transformers.md) | Attention as soft lookup; query, key, value; scaled dot-product; causal masking; multi-head attention; positional encodings; the transformer block (attention + MLP + residual + norm); parallelism vs recurrence | **Tiny GPT** — attention, heads, blocks, and a full char-level GPT written from scratch in PyTorch and trained until it generates readable text | ~8 h |
| 4 | [**How LLMs Are Actually Trained**](levels/level-4-innovator/module-04-how-llms-are-trained.md) | BPE tokenizers; the pretraining objective and data pipeline; scaling laws and compute; supervised fine-tuning; preference data; reward models; RLHF and DPO; what "emergent" really means; base vs instruct models | **Tokenizer + Life-of-an-LLM** — implement BPE from scratch, then run a hand-scored preference-ranking exercise and write the full training-story explainer | ~6 h |
| 5 | [**Prompt Engineering as a Real Engineering Skill**](levels/level-4-innovator/module-05-prompt-engineering.md) | The Claude messages API; system prompts and roles; zero/few-shot; chain-of-thought and when it fails; structured JSON output; delimiters and grounding; temperature and max_tokens; token counting and cost; **prompt evaluation instead of vibes** | **Prompt Bench** — a 20-case test set scoring three prompt versions automatically, with a results table and a cost-per-call budget | ~6 h |
| 6 | [**Embeddings, Vector Search, and RAG**](levels/level-4-innovator/module-06-embeddings-vector-search-rag.md) | Dense embeddings vs TF-IDF; cosine similarity and nearest neighbors; chunking strategies; building and querying a vector index; the retrieve-then-generate pattern; grounding, citations, and refusing when nothing is retrieved; why RAG beats fine-tuning for facts | **Ask My Notes** — a working RAG system over your own lab notebook that answers with citations and says "I don't know" when it should | ~7 h |
| 7 | [**Tool-Using AI Agents: The Loop That Does Things**](levels/level-4-innovator/module-07-ai-agents.md) | Tool schemas and the tool-use protocol; the perceive → decide → act → observe loop; multi-step planning; state and memory; error recovery and retries; loop limits and budgets; sandboxing and permission boundaries; when an agent is the wrong answer | **Three-Tool Agent** — an agent with a calculator, a notes-search tool, and a file writer, running a bounded, fully logged loop with guardrails | ~7 h |
| 8 | [**Fine-Tuning and Evaluating LLMs**](levels/level-4-innovator/module-08-finetuning-and-evaluating-llms.md) | When to prompt vs retrieve vs fine-tune; building a training set; full fine-tuning vs LoRA/PEFT; catastrophic forgetting; benchmarks and their limits; exact-match, rubric, and LLM-as-judge evals; inter-rater agreement; regression testing a model | **Eval Suite + Fine-Tune** — fine-tune a small Hugging Face model on a tiny task and prove the win (and the regressions) with your own eval harness | ~7 h |
| 9 | [**Responsible and Safe AI: Alignment and Red-Teaming**](levels/level-4-innovator/module-09-responsible-and-safe-ai.md) | Alignment in plain terms; hallucination and calibration; jailbreaks and prompt injection; data privacy and PII; copyright and attribution; measuring bias in generative systems; automation bias and over-trust; system cards and staged release | **Red-Team Report** — attack your own Module 7 agent, document every successful exploit, ship mitigations, and publish a system card | ~6 h |

### 🚀 [Level 4 Capstone — *Build an AI Product*](levels/level-4-innovator/capstone.md) (~20 h)
Ship something a stranger would actually use. Requirements: a written **design doc** (problem, users,
why AI, what could go wrong); a working system that combines at least two of {RAG, tool-using agent,
fine-tuned or custom-trained model}; an **eval harness** with ≥25 cases that runs on demand and reports a
score; a **cost and latency budget** measured, not guessed; **safety guardrails** with a documented
red-team pass; and a 5-minute demo plus a **system card**. Then write the honest section: what it fails
at, and who should not rely on it.

---

## 🌀 The Spiral Progression

The same six ideas, four times, deeper each pass. If you can fill in a row from memory, you own that idea.

### Idea 1 — 📦 Data

| Level | What "data" means here | What you do with it |
|---|---|---|
| **1 Explorer** | A table of examples you can hold in your hands | Collect 30 rows by hand; notice what's missing |
| **2 Builder** | Lists, dicts, CSVs, arrays, DataFrames | Load, clean, filter, group, and chart it in code |
| **3 Engineer** | Train/val/test splits with distributions and leakage risks | Audit it, split it correctly, engineer it, detect drift |
| **4 Innovator** | Web-scale token corpora, preference pairs, eval sets | Build tokenizers, curate SFT data, construct benchmarks |

### Idea 2 — 🔢 Representation

| Level | How the world becomes numbers | Key artifact |
|---|---|---|
| **1 Explorer** | Features chosen by a human; images as pixel grids | A feature card for a real object |
| **2 Builder** | A row of numbers = a vector; arrays and DataFrames | A numeric feature matrix `X` |
| **3 Engineer** | Scaling, encoding, convolutional feature maps, TF-IDF | A `ColumnTransformer` and a CNN's learned filters |
| **4 Innovator** | Learned dense embeddings and attention-mixed hidden states | A vector index you can search |

### Idea 3 — 🤖 Model

| Level | What a model is | Examples you build |
|---|---|---|
| **1 Explorer** | A box that takes an example and guesses a label | A Teachable Machine classifier |
| **2 Builder** | Code with parameters that fits data | kNN, decision tree, linear regression |
| **3 Engineer** | A parameterized function composed into a pipeline | Logistic regression, MLP, CNN, k-means, PCA |
| **4 Innovator** | Stacked transformer blocks; systems around them | Tiny GPT, RAG system, tool-using agent |

### Idea 4 — 📉 Learning Signal

| Level | How the machine knows it's wrong | Mechanism |
|---|---|---|
| **1 Explorer** | You show it correct and incorrect examples | Adding examples changes the guesses |
| **2 Builder** | It fits the training data better or worse | `fit()`, distance, tree splits, best-fit line |
| **3 Engineer** | A loss number with a slope | Cross-entropy + gradient descent + backprop |
| **4 Innovator** | Next-token loss, then human preference | Pretraining → SFT → reward model → RLHF/DPO |

### Idea 5 — 📏 Evaluation

| Level | The question | Tools |
|---|---|---|
| **1 Explorer** | "Does it work on examples it never saw?" | Hidden test set, accuracy by hand |
| **2 Builder** | "How accurate, and is it just memorizing?" | `train_test_split`, accuracy, MAE, R², overfitting curves |
| **3 Engineer** | "Which errors, how often, at what cost?" | Confusion matrix, precision/recall/F1, ROC-AUC, k-fold CV |
| **4 Innovator** | "Is it good, safe, and not secretly regressing?" | Benchmarks, LLM-as-judge, rubric evals, red-team suites |

### Idea 6 — 🧑‍🤝‍🧑 Human Impact

| Level | The concern | What you produce |
|---|---|---|
| **1 Explorer** | Fairness, privacy, and not believing everything | A fairness audit poster |
| **2 Builder** | Whose data is this, and who does the error hit? | A data-provenance paragraph in every project |
| **3 Engineer** | Cost of each error type; documenting limitations | Subgroup metrics + a model card |
| **4 Innovator** | Alignment, misuse, injection, over-trust, release | A red-team report and a system card |

---

## 🔗 Prerequisite Dependency Graph

Every arrow means "you need that first." No arrow ever points backwards in module order.

```
LEVEL 1 · EXPLORER  (no prerequisites at all)
────────────────────────────────────────────────────────────────────────────
   L1.1 what AI is
     └─► L1.2 data ──► L1.3 patterns & rules ──► L1.4 features & labels
                                                      │
                                                      ├─► L1.5 train a model
                                                      │        │
                                                      │        └─► L1.6 train/test
                                                      │                 │
                              L1.7 how computers see ◄┘                 │
                              L1.8 how computers read ◄─────────────────┤
                              L1.9 fair/private/honest ◄────────────────┘
                                        │
                                        ▼
                             ╔══ L1 CAPSTONE: AI Fair Booth ══╗
                                        │
════════════════════════════════════════▼════════════════════════════════════
LEVEL 2 · BUILDER   (needs: L1.4 features/labels, L1.6 train/test)
────────────────────────────────────────────────────────────────────────────
   L2.1 python basics
     └─► L2.2 decisions & loops
           └─► L2.3 functions & lists
                 └─► L2.4 dicts & datasets ────► L2.5 numpy
                              │                      │
                              └──────────────────────┴─► L2.6 pandas
                                                             │
                                                             ├─► L2.7 charts
                                                             │        │
                                                             └────────┴─► L2.8 kNN + train/test
                                                                              │
                                                                              ▼
                                                                     L2.9 trees, lines,
                                                                          overfitting
                                        │
                                        ▼
                            ╔══ L2 CAPSTONE: Data Detective ══╗
                                        │
════════════════════════════════════════▼════════════════════════════════════
LEVEL 3 · ENGINEER  (needs: all of L2; especially L2.5, L2.6, L2.8, L2.9)
────────────────────────────────────────────────────────────────────────────
   L3.1 supervised pipeline
     ├─► L3.2 feature engineering ──┐
     └─► L3.3 evaluation metrics ───┤
                                    ▼
                        L3.4 loss + gradient descent
                                    │
                                    ▼
                        L3.5 neural nets from scratch
                                    │
                                    ▼
                        L3.6 PyTorch ──────► L3.7 CNNs
                                    │
              L3.8 k-means & PCA ◄──┘  (needs L3.2 scaling)
                     │
                     ▼
              L3.9 classic NLP  (needs L3.2 + L3.3 + L3.8 for PCA views)
                                        │
                                        ▼
                              ╔══ L3 CAPSTONE: Ship It ══╗
                                        │
════════════════════════════════════════▼════════════════════════════════════
LEVEL 4 · INNOVATOR (needs: L3.6 PyTorch, L3.7 CNNs, L3.9 NLP)
────────────────────────────────────────────────────────────────────────────
   L4.1 deep learning at depth
         │
         ▼
   L4.2 sequence models (RNN/LSTM)
         │
         ▼
   L4.3 attention & transformers ──► tiny GPT
         │
         ▼
   L4.4 how LLMs are trained
         │
         ├─► L4.5 prompt engineering ──┬─► L4.6 embeddings + vector search + RAG
         │                             │            │
         │                             │            ▼
         │                             └─────► L4.7 tool-using agents
         │                                          │
         └─► L4.8 fine-tuning & LLM evals ◄─────────┤
                          │                         │
                          └────────► L4.9 responsible & safe AI
                                        │
                                        ▼
                        ╔══ L4 CAPSTONE: Build an AI Product ══╗
```

### Cross-level "callback" edges (where the spiral bites)

| Later module | Reaches back to | Why |
|---|---|---|
| L2.8 kNN | L1.4 features & labels, L1.6 train/test | Same ideas, now in code |
| L3.3 metrics | L2.9 overfitting | Accuracy was never enough |
| L3.5 backprop | L3.4 gradient descent | Backprop is the chain rule over the same update |
| L3.9 NLP | L1.8 words & guesses | Bigrams grow up into TF-IDF and embeddings |
| L4.3 attention | L3.9 embeddings | Attention mixes the vectors you already understand |
| L4.4 RLHF | L1.5 learning from examples | The learning signal is still "examples of good and bad" |
| L4.9 safety | L1.9 fairness & privacy | The 6th-grade poster becomes a system card |

---

## ⏱️ Time Budget At A Glance

| Level | Modules | Module hours | Capstone | Level total | Weeks @ ~3.5 h/wk |
|---|:--:|:--:|:--:|:--:|:--:|
| 1 Explorer | 9 | ~26 h | ~6 h | **~32 h** | ~12 |
| 2 Builder | 9 | ~34 h | ~10 h | **~44 h** | ~20 |
| 3 Engineer | 9 | ~49 h | ~12 h | **~61 h** | ~24 |
| 4 Innovator | 9 | ~59 h | ~20 h | **~79 h** | ~28 |
| **Total** | **36** | **~168 h** | **~48 h** | **~216 h** | **~84 weeks (2–3 school years)** |

---

## ✅ Level Exit Checks

Do not advance until you can do all of these **without notes**.

**Leaving Level 1:** explain training vs testing to an adult · name the features and label of any prediction task · state one way a dataset could be biased against someone · say what a pixel is.

**Leaving Level 2:** write a Python function with a loop and a condition from a blank file · load a CSV into pandas and answer a grouped question · train a model, split the data, and report test accuracy · explain overfitting with your own numbers.

**Leaving Level 3:** draw the supervised pipeline from memory · compute precision and recall from a confusion matrix by hand · write a PyTorch training loop from a blank file · explain backprop as the chain rule · save a model and serve a prediction.

**Leaving Level 4:** draw the transformer block from memory · explain pretraining → SFT → RLHF in four sentences · build a RAG pipeline from a blank file · design an eval before building the feature · name three ways your own system could be misused.

---

**Start here → [`START_HERE.md`](START_HERE.md)**, then [`levels/level-1-explorer/README.md`](levels/level-1-explorer/README.md)

Back to [README](README.md) · [Resources](RESOURCES.md) · [Teacher / mentor guide](teacher-guide/README.md) · [Browsable site](site/index.html)

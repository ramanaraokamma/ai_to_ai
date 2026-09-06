# 📓 Level 3 Glossary — Every Word, Alphabetized

**Level 3 · Reference · Prereqs: none — use this any time a word stops making sense**

[Level 3 Home](README.md) · [Assessment](assessment.md) · [Capstone](capstone.md) · [Level 2 Glossary](../level-2-builder/glossary.md)

---

## How to use this page

Every technical term introduced anywhere in Level 3 is here — **221 of them** — with a plain-English definition and the actual example from the course. The **Module** column tells you where to go for the full explanation:

| Tag | Where |
|---|---|
| `M1`–`M9` | That module file, e.g. [`module-05-neural-networks-from-scratch.md`](module-05-neural-networks-from-scratch.md) |
| `SET` | The environment-setup section of the [level README](README.md) |
| `CAP` | The [capstone](capstone.md) |

**Jump to a letter:**
[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [W](#w) · [Z](#z)

> ⚠️ **A word on `code font`.** Terms written like `this` are things you literally type. Terms written like *this* are ideas. If you can't type it, it's an idea; if you can, it's a spelling.

> 🔑 **The Level 3 rule of thumb.** If a term describes something that *learns a number from data* — a mean, a median, a vocabulary, a set of centroids, a scaler's standard deviation — then it must be fitted on **training data only**. Nearly half this glossary is a variation on that one sentence.

---

## A

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Ablation** | Build the model with a feature, build it without, and compare — the only honest way to know if the feature paid | `is_weekend` → ΔAUC 0.0000 → delete it | M2 |
| **Accuracy** | The fraction of predictions that were right | `(TP + TN) / total`; 0.9908 on the fraud set, and worthless | M1, M3 |
| **Accuracy paradox** | A useless model looking excellent because one class dominates | 99.05% accurate by always saying "not fraud" | M3 |
| **Activation (`a`)** | A neuron's output, *after* the squash | `a = ReLU(2.20) = 2.20` | M5 |
| **Activation function** | The squash at the end of a neuron; the thing that makes stacking layers worth anything | ReLU, sigmoid, tanh, softmax | M5 |
| **Adam** | An optimizer that adapts the step size separately for every parameter | `torch.optim.Adam(params, lr=1e-3)` | M6 |
| **Adjusted Rand index (ARI)** | Agreement between two groupings, corrected for chance; 1.0 = identical, 0 = no better than random | 0.90 between k-means clusters and the true wine cultivars | M8 |
| **Artifact** | The saved file that **is** your trained model — weights plus every preprocessing step | `late_pipeline_v1.joblib` | M1, CAP |
| **AUC (ROC-AUC)** | The chance that a random positive scores higher than a random negative; 0.5 = coin flip | 21 correctly ordered pairs out of 25 = 0.84 | M1, M3 |
| **Autograd** | PyTorch's automatic differentiation engine — it records what you did and walks the chain rule backwards for you | `loss.backward()` | M6 |
| **Average precision (AP)** | The area under the precision-recall curve; its no-skill baseline is the **positive rate**, not 0.5 | AP 0.1931 against a baseline of 0.0095 — about 20× | M3 |

---

## B

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Backbone** | The pretrained convolutional stack you reuse, as opposed to the small classifier you bolt on | resnet18's conv layers, frozen | M7 |
| **Backpropagation** | Using the chain rule backwards so every weight in the network gets its gradient in a single sweep | Five lines of NumPy in `backward()` | M5 |
| **Bag-of-words** | A document represented as word counts, with the order thrown away | `"the dog bit the man"` = `"the man bit the dog"` | M9 |
| **Baseline** | The dumbest possible predictor, used as the zero point every score is measured against | "always say on time" → 71.2% accurate | M1 |
| **Batch** | A chunk of rows processed together in one forward/backward pass | `batch_size=64` | M4, M6 |
| **Batch gradient descent** | Use **every** row to compute one gradient, then take one step | 1 weight update per epoch | M4 |
| **`BCEWithLogitsLoss`** | Binary log loss that applies the sigmoid for you, numerically stably | Binary classification on `make_moons` | M6 |
| **Bias (fairness)** | A model performing measurably worse for one group of people than another | Subgroup metrics in the model card | M1, CAP |
| **Bias (parameter)** | A constant added to every prediction; slides the whole model up or down | `b = 0.2` makes every prediction slightly more positive | M4 |
| **Binning** | Chopping a number into ranges and treating them as categories | hour 18–20 → `"rush"` | M2 |
| **Broadcasting** | NumPy or PyTorch stretching a smaller array across a bigger one automatically — helpful, and a silent killer when shapes are wrong | `(n,16) + (1,16)` is fine; `(n,1) − (n,)` becomes `(n,n)` | M5 |

---

## C

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Calibration** | Whether a predicted 0.3 really happens about 30% of the time | Checked with a reliability curve | M3 |
| **Capacity** | How complicated a shape a model is able to represent | 1 hidden unit ≈ a line; 16 hidden units ≈ a curve | M5 |
| **Cardinality** | How many distinct values a column has | `restaurant`: 5. `postcode`: 41,000 | M2 |
| **Centroid** | The average position of everything currently in a cluster | `(1.6667, 2.0)` for `{A, B, C}` | M8 |
| **Chain rule** | Slopes multiply along a path: `dc/da = (dc/db)(db/da)` | rain → traffic → arrival time | M5 |
| **Channel** | One slice of depth in an image tensor — colours on the input, learned concepts after a conv layer | RGB is 3 channels; `Conv2d(3, 32, 3)` outputs 32 | M7 |
| **CIFAR-10** | A built-in dataset of 32×32 colour photos in 10 classes | The subset your `SmallCNN` and resnet18 both train on | M7 |
| **Class balance** | The fraction of rows in each class | 28.8% late, 71.2% on time | M1 |
| **Class imbalance** | One answer being far more common than the other, to the point where accuracy stops meaning anything | 190 frauds in 20,000 transactions | M3 |
| **`class_weight="balanced"`** | Tells the model to weight the rare class up, so it stops ignoring it | `LogisticRegression(class_weight="balanced")` | M3 |
| **`classification_report`** | sklearn's per-class table of precision, recall, F1 and support | Printed for all 10 CIFAR classes | M3, M7 |
| **CLI (command-line interface)** | A program someone runs by typing its name and arguments in a terminal | `python predict.py --text "great pizza"` | CAP |
| **Cluster** | A group of points more like each other than like anything outside the group | The 62 "Bold Reserve" wines | M8 |
| **Colab** | Google's free browser notebook with a GPU — the fallback for the two heaviest modules | *Runtime → Change runtime type → T4 GPU* | SET |
| **`ColumnTransformer`** | Runs different preprocessing on different columns and glues the results back together | Scale 5 numeric columns, one-hot 3 categorical ones | M1, M2 |
| **Computation graph** | PyTorch's recording of every operation you performed, used to walk the chain rule backwards | `x → x² → loss` | M6 |
| **Confusion matrix** | The 2×2 (or 10×10) table of what was true against what you predicted | `[[5941, 2], [53, 4]]` | M3 |
| **Convergence criterion** | The rule that tells training to stop | Stop when the loss changes by less than `1e-6` | M4 |
| **Convex** | Bowl-shaped: one bottom, no traps. Logistic regression's log loss is convex | Any sane learning rate finds the same answer | M4 |
| **Convolution** | Sliding a small grid of weights over an image and taking a dot product at every position | The 3×3 edge kernel turning a flat patch into a bright stripe | M7 |
| **Co-occurrence matrix** | A table counting which words appear near which other words | `cat`'s row: `the:2, drinks:1, eats:1, …` | M9 |
| **Cosine similarity** | Similarity measured as the angle between two vectors, ignoring their lengths | `cos(d1, d2) = 0.726` | M9 |
| **Cost matrix** | The price you attach to each kind of error | `FN = 500`, `FP = 10` | M3 |
| **`CrossEntropyLoss`** | Multi-class log loss that applies log-softmax for you — so your last layer must be a bare `nn.Linear` | 10-class FashionMNIST | M6 |
| **`cross_val_score`** | Runs k-fold cross-validation and hands back one score per fold | `scores.mean()`, `scores.std()` | M3 |
| **CUDA** | NVIDIA's GPU compute platform; `device="cuda"` in PyTorch | `torch.cuda.is_available()` | SET, M6 |
| **Curse of dimensionality** | With many features, everything ends up roughly equally far from everything, so "nearest" stops meaning much | At d = 1000 the farthest point is only 20% farther than the nearest | M8 |
| **Cyclical encoding** | Using sine and cosine so 23:00 sits next to 00:00 instead of 23 units away | `sin(2π·h/24)`, `cos(2π·h/24)` | M2 |

---

## D

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Data audit** | Checking the table for problems *before* you model anything | "20 duplicate rows, 108 missing values, 1 near-unique column" | M1 |
| **Data augmentation** | Randomly changing training images in label-preserving ways to manufacture free variety | Mirroring a cat photo — still a cat | M7 |
| **Data leakage** | Information reaching the model at training time that will not exist at prediction time | `customer_called_support` | M2 |
| **`DataLoader`** | Turns a `Dataset` into shuffled batches you can loop over | `DataLoader(ds, batch_size=64, shuffle=True)` | M6 |
| **`Dataset`** | An object that can say how many items it holds and hand you item `i` | `TensorDataset(X, y)` | M6 |
| **Dead ReLU** | A unit whose input is negative for every row, so it never fires and never learns | 10 of 16 units after training at `lr = 20` | M5 |
| **Decision threshold** | The probability cut-off above which you call something positive | 0.5 by default; 0.018 after cost tuning | M3 |
| **Deduplication** | Removing repeated rows — immediately after loading, before any split | `df.drop_duplicates()` | M1 |
| **Derivative** | The slope: how much the output moves when you nudge the input by a hair | The slope of `w²` at `w = 3` is 6 | M4 |
| **Device** | Which chip the numbers physically sit on | `cpu`, `cuda`, `mps` | M6, SET |
| **Distributional hypothesis** | Words used in the same contexts tend to mean similar things | You learn what `bhindi` means from the sentences around it | M9 |
| **Divergence** | When the loss climbs instead of falling because the steps are too big | Loss 0.69 → 17.97 at `lr = 800` | M4 |
| **Document frequency (`df`)** | How many documents contain a word | `pizza` is in 3 of the 4 reviews | M9 |
| **Document-term matrix** | Rows are documents, columns are words, cells are counts | The 4 × 8 review table | M9 |
| **Drift** | The world changing until your model's training data no longer describes it | The number your monitoring plan watches | CAP |
| **Dropout** | Randomly zeroing some units during training, to stop the network leaning on any one of them | `nn.Dropout(0.2)` — and it must be switched off with `model.eval()` | M6 |
| **`dtype`** | What kind of number sits in each slot | `torch.float32` for features, `torch.int64` for class targets | M6 |
| **`DummyClassifier`** | scikit-learn's built-in baseline maker | `DummyClassifier(strategy="most_frequent")` | M1 |

---

## E

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Early stopping** | Halting training when the validation loss stops improving, and keeping the best weights | `patience=20` | M6 |
| **Elbow method** | Plot inertia against `k` and look for where the curve stops dropping steeply | The bend at `k = 3` for wine | M8 |
| **Epoch** | One full pass over all the training data | 12 epochs on FashionMNIST | M4, M6 |
| **`eval_tf`** | The evaluation transform — resize and normalize only, never anything random | The twin of `train_tf`, and they must never cross | M7 |
| **Expected cost** | `C_FN × FN + C_FP × FP` at a given threshold — the number you actually minimise | `500(18) + 10(542) = 14,420` | M3 |
| **Explained variance ratio** | The share of the data's total spread that one principal component captures | PC1 = 36.2% of wine's variance | M8 |

---

## F

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **F1 score** | The harmonic mean of precision and recall; punishes lopsidedness, and assumes both errors cost the same | 0.127 on the fraud set | M3 |
| **False negative (FN)** | It was positive and you said negative — a **miss** | A fraud went through | M3 |
| **False positive (FP)** | It was negative and you said positive — a **false alarm** | An honest customer's card declined | M3 |
| **False positive rate (FPR)** | `FP / (FP + TN)` — the x-axis of the ROC curve | Each ham email steps the curve right by 0.2 | M3 |
| **FashionMNIST** | A built-in dataset of 28×28 greyscale clothing images in 10 classes | 60,000 training images, label 9 = "Ankle boot" | M6, SET |
| **Feature engineering** | Reshaping raw columns into ones the model can actually use | Turning `order_hour` into `is_rush` | M2 |
| **Feature map** | The output grid of one filter — a heat map of where that filter fired | The 4×4 grid of `0, 24, 24, 0` | M7 |
| **Features (`X`)** | Everything the model is allowed to look at | distance, weather, restaurant, hour | M1 |
| **Fine-tuning** | Unfreezing some pretrained layers and training them gently with a small learning rate | `layer4` at `lr = 1e-4` | M7 |
| **`fit` / `transform` / `fit_transform`** | `fit` **learns** parameters from data; `transform` **applies** them. `fit_transform` does both — and belongs on training data only | `fit_transform(X_train)`, then `transform(X_test)` | M2 |
| **Flatten** | Turning a `(C, H, W)` feature map into one long vector so a dense layer can read it | `256 × 2 × 2 = 1,024` | M7 |
| **Fold** | One of the `k` held-out chunks in cross-validation | 5 folds, 38 frauds in each | M3 |
| **Forward pass** | Running data through the network to get a prediction | `x → Z1 → A1 → Z2 → A2 = 0.900250` | M5 |
| **Freezing** | Setting `requires_grad = False` so a pretrained layer's weights stop changing | The frozen resnet18 backbone | M7 |
| **`FunctionTransformer`** | Wraps a plain Python function so it can live inside a `Pipeline` | `FunctionTransformer(add_features)` | M2 |

---

## G

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Golden test** | A handful of inputs whose correct outputs you froze, run every time you change the artifact | Three cases in `tests.py` | CAP |
| **`.grad`** | The attribute where autograd puts the gradient it computed | `W1.grad[0,0] = −0.09975` | M6 |
| **Gradient** | All the partial slopes at once, one per weight, packed into a vector. It points **uphill** | `[0.265, −0.081]` | M4 |
| **Gradient check** | Nudging a weight numerically and dividing, to verify your hand-derived calculus | `(L₊ − L₋) / (2ε)` with `ε = 1e-6` | M5 |
| **Gradient descent** | Repeatedly step in the *opposite* direction of the gradient | `w ← w − 0.5 × 0.265` | M4 |

---

## H

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **`handle_unknown="ignore"`** | The setting that turns an unseen category into a row of zeros instead of a crash | A brand-new restaurant → `[0, 0, 0]` | M2 |
| **He initialization** | Random starting weights with `std = sqrt(2 / n_in)`; the standard choice for ReLU networks | `std = sqrt(2/2) = 1.0` for the first layer | M5 |
| **Head** | The small dense part bolted onto a backbone to do the actual classifying | `nn.Linear(512, 10)` | M7 |
| **Hidden layer** | A layer whose outputs you never read directly | The 16 units between input and output | M5 |
| **HTTP service** | A tiny always-on program that answers requests over the network | `POST /predict` on `localhost:8000` | CAP |
| **Hyperparameter** | A setting *you* choose rather than one the model learns | `k` in k-means, `lr`, `max_depth`, the threshold | M1, M3 |

---

## I

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **ID column** | A column with a different value in nearly every row — it carries no signal and will fool a model | `order_id` | M1 |
| **Imputation** | Filling a missing value with a learned guess | Blank driver experience → the **training** median, 29 | M1, M2 |
| **Inertia (WCSS)** | Total squared distance from every point to its own centroid; smaller is tighter, and it always falls as `k` rises | 6.6667 in the worked example | M8 |
| **Intended use** | The model card section saying what this model is *for* — and, just as importantly, what it isn't | "Triage forum comments for a human moderator" | M1, CAP |
| **Interaction feature** | Two columns multiplied, so one can amplify the other | `distance × storm` | M2 |
| **Inverse document frequency (IDF)** | A rarity bonus: words in few documents score higher | `and` (df 1) gets 1.916; `pizza` (df 3) gets 1.223 | M9 |

---

## J

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **`joblib`** | The library that saves and loads fitted scikit-learn objects | `joblib.dump(pipe, "m.joblib")` / `joblib.load(...)` | M1 |

---

## K

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Kernel (filter)** | The small grid of learnable weights that slides across an image | `[[1,0,−1],[1,0,−1],[1,0,−1]]` detects vertical edges | M7 |
| **k-fold cross-validation** | Score `k` times on `k` different held-out chunks and report the spread, so one lucky split can't fool you | AUC 0.8405 ± 0.0084 | M3 |
| **k-means** | Assign every point to the nearest centroid, move each centroid to its members' mean, repeat until nothing changes | Converged in 2 iterations on the six-point example | M8 |
| **k-means++** | A smarter way to pick starting centroids so they don't all land in the same blob | scikit-learn's default `init` | M8 |

---

## L

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **L2 normalization** | Scaling a vector so its length is exactly 1 | Divide d1 by 2.888574 | M9 |
| **Latency** | How long one prediction took, in milliseconds | Logged on every request, p50 and p95 reported | CAP |
| **Layer** | A row of neurons that all see the same inputs | 16 hidden units | M5 |
| **Learning rate (`lr`)** | Your stride length when stepping downhill | `lr = 0.5`; `1e-3` for Adam; `1e-4` for fine-tuning | M4 |
| **Loading (PCA)** | How much one original feature contributes to a principal component | `flavanoids` loads 0.423 on wine's PC1 | M8 |
| **Log loss (cross-entropy)** | A loss that measures your *surprise*; it punishes confident wrongness enormously | Saying 5% when the truth was yes costs `−ln(0.05) = 2.9957` | M4 |
| **Log-odds** | The natural log of the odds — exactly the same number as the logit `z` | `ln(9) = 2.197` | M4 |
| **Logit (raw score `z`)** | The weighted sum, before it becomes a probability. Can be any number at all | `z = 1.4` | M4, M6 |
| **Loss function** | One number saying how wrong the model is right now. Lower is better | Log loss = 0.21 | M4 |

---

## M

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Majority class** | The most common label; predicting it always is the simplest baseline there is | "on time", 71.2% | M1 |
| **`make_moons`** | A built-in two-crescent dataset that no straight line can separate | The test your NumPy MLP has to pass at >90% | M5 |
| **Max pooling** | Keep only the biggest value in each small window; no weights to learn | A 2×2 pool turns 16 numbers into 4 | M7 |
| **Mini-batch gradient descent** | Use a chunk of 32 or 64 rows per step — the default in practice | 13 updates per epoch on 400 rows | M4 |
| **Min-max scaling** | Squash a column into the range 0 to 1 | `(4 − 2) / 7 = 0.2857` | M2 |
| **Missing indicator** | An extra 0/1 column marking where a value was originally blank | `SimpleImputer(add_indicator=True)` | M2 |
| **MLP (multi-layer perceptron)** | Fully connected layers stacked with activations between them | `2 → 16 → 1` | M5 |
| **Model card** | The label on the bottle: intended use, training data, metrics by subgroup, known failure modes, out-of-scope uses | `model_card.md`, a deliverable from Module 1 onward | M1, CAP |
| **`model.eval()`** | Switch to inference behaviour: dropout off, batch-norm frozen | Called immediately after `load_state_dict` | M6 |
| **Model version** | A string identifying exactly which artifact produced a prediction | `sentiment-v3`, logged on every request | CAP |
| **Momentum** | Letting the optimizer build up speed in a consistently downhill direction | `SGD(..., momentum=0.9)` | M4, M6 |
| **Monitoring plan** | One page naming the number that would tell you the model has gone stale, and what you'd do about it | The last capstone deliverable | CAP |
| **MPS** | Apple Silicon's GPU backend in PyTorch | `torch.backends.mps.is_available()` | SET, M6 |

---

## N

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Neuron (unit)** | Multiplies its inputs by weights, adds a bias, squashes the result | `a = ReLU(0.4x₁ − 0.7x₂ − 0.5)` | M5 |
| **n-gram** | A run of `n` consecutive tokens treated as one feature | `"not good"` is a bigram | M9 |
| **`nn.Linear`** | One fully connected layer: a weight matrix plus a bias | `nn.Linear(784, 256)` | M6 |
| **`nn.Module`** | PyTorch's base class for anything with learnable parameters | `class MoonNet(nn.Module)` | M6 |
| **`nn.Sequential`** | Layers chained in a straight line, no custom `forward` needed | `nn.Sequential(fc1, relu, fc2)` | M6 |
| **`no_grad()`** | "Don't record anything" — for evaluation and inference | `with torch.no_grad(): ...` | M6 |
| **Normalization (text)** | Tidying text so different spellings of the same thing match | `GREAT!! → great` | M9 |
| **Numerical gradient** | Estimating a slope by nudging the input and dividing, with no calculus at all | `(f(w+ε) − f(w−ε)) / 2ε` | M4, M5 |

---

## O

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Odds** | The probability of yes divided by the probability of no | `p = 0.9` → odds = 9, "9 to 1 on" | M4 |
| **One-hot encoding** | One yes/no column per category, so no false ordering is invented | Napoli → `[0, 1, 0]` | M2 |
| **`OneHotEncoder`** | scikit-learn's one-hot transformer — always set `handle_unknown="ignore"` | `OneHotEncoder(handle_unknown="ignore")` | M2 |
| **Optimizer** | The object that owns your parameters and applies the update rule | `torch.optim.Adam(model.parameters(), lr=1e-3)` | M6 |
| **Ordinal encoding** | Categories become integers on a ladder — only valid when a real order exists | small→0, medium→1, large→2 | M2 |
| **Out-of-scope use** | The model card section listing what this model must **never** be used for | "Not for automated account suspension" | CAP |
| **Overfitting** | Training loss keeps dropping while held-out accuracy stops improving | Train loss 0.34, test accuracy stuck at 57% | M7 |

---

## P

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Padding** | Rings of zeros added around an image's border so the window can reach edge pixels | `k=3, p=1` keeps a 32×32 image at 32×32 | M7 |
| **PCA (principal component analysis)** | Finding new axes that point along the data's biggest spread, then keeping the first few | Wine's 13 features projected to 2-D | M8 |
| **`penalty=None`** | Turns off scikit-learn's default L2 regularization, so your hand-written gradient descent can match it | `LogisticRegression(penalty=None)` | M4 |
| **Piecewise-linear** | A curve built out of straight segments joined at kinks | The MLP's decision boundary; one kink per ReLU | M5 |
| **`Pipeline`** | One object chaining preprocessing and a model, so `fit` can only ever see training rows | scale → one-hot → logistic regression | M1 |
| **Positive rate** | The fraction of rows that are the positive class; the no-skill baseline for average precision | 0.0095 on the fraud set | M3 |
| **Pre-activation (`z`)** | The weighted sum *before* the squash | `z = 2.20` | M5 |
| **Precision** | Of everything you flagged, how much was actually right | `4 / (4 + 2) = 0.667` | M3 |
| **Precision-recall curve** | Precision plotted against recall as the threshold sweeps; its area is average precision | AP 0.1931 | M3 |
| **`predict_proba`** | Returns probabilities instead of hard labels, so you can choose your own threshold | `pipe.predict_proba(X)[:, 1]` | M3 |
| **Prediction log** | A line written for every prediction: timestamp, version, input, output, probability, latency | The file your 11 p.m. debugging depends on | CAP |
| **Preprocessing leakage** | Statistics learned from the whole dataset before the split | 83% accuracy on pure noise | M2 |
| **Principal component** | A new axis chosen to point along the data's biggest remaining spread | PC1 for wine ≈ "total phenolic richness" | M8 |

---

## R

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **`random_state` / seed** | The number that makes a random operation repeatable | `train_test_split(..., random_state=0)` | M1 |
| **Ratio feature** | One column divided by another | `prep_minutes / distance_km` | M2 |
| **`.ravel()`** | Flattens a 2×2 confusion matrix so you can unpack it and *name* the four counts | `tn, fp, fn, tp = confusion_matrix(y, p).ravel()` | M3 |
| **Recall (sensitivity)** | Of everything that was really positive, how much you caught | `4 / (4 + 53) = 0.070` | M3 |
| **Receptive field** | How much of the original image one later cell can "see" | 22×22 pixels for `SmallCNN`'s final layer | M7 |
| **Reconstruction error** | How far off you are when you rebuild the original data from a few components | 2.38 average units with 2 components | M8 |
| **Relative error** | `|a − b| / (|a| + |b|)` — a fair comparison regardless of scale | `3.7e-08` — the gradient check passes | M5 |
| **ReLU** | `max(0, z)`. A one-way valve, and the default hidden activation | `ReLU(−2.3) = 0` | M5 |
| **`requires_grad`** | A flag meaning "track this — I want its gradient" | `torch.tensor(3.0, requires_grad=True)` | M6 |
| **resnet18** | A small pretrained image network you can reuse instead of training from scratch | Frozen backbone + a new 10-class head | M7 |
| **ROC curve** | Recall plotted against the false positive rate as the threshold sweeps | AUC 0.84 in the ten-email example | M3 |

---

## S

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Saturation** | An activation pinned near its flat extreme, where the gradient is almost zero | A sigmoid at `z = 12` returns 0.999994 and learns nothing | M5 |
| **Sigmoid** | The S-shaped squasher turning any number into a probability between 0 and 1 | `σ(1.4) = 0.802` | M4 |
| **Silhouette score** | −1 to +1: how much closer a point is to its own cluster than to the next nearest one | `s(C) = 0.78` means C is firmly placed; 0.28 means "real but overlapping" | M8 |
| **`SimpleImputer`** | scikit-learn's missing-value filler; learns the median from training data only | `SimpleImputer(strategy="median")` inside the pipeline | M2 |
| **Smoke test** | Three lines that prove your environment actually works before you need it to | `python smoke_grad.py` prints `6.0` | SET |
| **Softmax** | Turns several raw scores into probabilities that sum to 1 | `[2, 1, 0.1] → [0.659, 0.242, 0.099]` | M5 |
| **Sparse matrix** | Storing only the non-zero cells, because most of a document-term matrix is zeros | 15 stored values out of 32 cells | M9 |
| **Specificity** | Of everything really negative, how much you correctly left alone | `5941 / 5943 = 0.9997` | M3 |
| **Squared error** | `(truth − prediction)²`. Right for regression, wrong for classification | `(1 − 0.05)² = 0.9025` — barely a punishment | M4 |
| **Standardization (z-score)** | Rescale so the mean is 0 and the standard deviation is 1 | `(9 − 5) / 2 = 2.0` | M2 |
| **`StandardScaler`** | scikit-learn's standardizer; learns mean and std in `fit` | Lives inside the `ColumnTransformer`, never outside it | M2 |
| **`state_dict`** | A dictionary of parameter names to weight tensors — what you actually save in PyTorch | `{'0.weight': ..., '0.bias': ...}` | M6 |
| **Step (iteration)** | One weight update, i.e. one batch | 400 rows at batch 32 → 13 steps per epoch | M4, M6 |
| **Stochastic gradient descent (SGD)** | Use one row per step | 400 updates per epoch | M4 |
| **Stopword** | A super-common word carrying little topic meaning — and a trap on sentiment tasks | `the`, `is`, `and`; but the standard list also contains `not` | M9 |
| **Stratified k-fold** | k-fold that keeps the class proportions equal in every fold | 38 frauds in each of 5 folds | M3 |
| **Stratified split** | A split that keeps the class proportions equal in every part | 28.7% late in all three splits | M1 |
| **Stride** | How far the convolution window jumps between positions | `s=2` halves the output size | M7 |
| **Subgroup metrics** | The same metric computed separately for slices of your data, to find who it works worse for | Precision by review length; accuracy by class | CAP |
| **Supervised learning** | Learning from examples where you already know the right answer | 2,000 past orders, each labelled late or on time | M1 |
| **Symmetry breaking** | Making units start out different so they learn different things | Random init instead of zeros | M5 |

---

## T

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Target (`y`)** | The one column you're trying to predict | `late` (0 or 1) | M1 |
| **Target leakage** | A feature that only exists *because* the outcome already happened | AUC 0.978, and useless in production | M2 |
| **Temporal leakage** | Training on the future and testing on the past | Random split 0.79, time-ordered split 0.56 | M2 |
| **Tensor** | PyTorch's array: like numpy, but it can live on a GPU and remember its own history | `torch.zeros(2, 3)` | M6 |
| **Term frequency (TF)** | How often a word appears in this particular document | `great` appears twice in d3, so tf = 2 | M9 |
| **Test set** | The sealed final exam. Opened exactly once, at the very end, and never tuned against | 400 of the 2,000 pizza orders | M1 |
| **TF-IDF** | Term frequency × inverse document frequency, then L2-normalize the row | d3's `great` = 0.841 | M9 |
| **`TfidfVectorizer`** | scikit-learn's text-to-TF-IDF-matrix transformer; L2-normalizes rows by default | `TfidfVectorizer(ngram_range=(1,2), min_df=2)` | M9 |
| **`token_pattern`** | The regex deciding what counts as a token; the default drops single letters | Default `\b\w\w+\b` silently deletes the word `i` | M9 |
| **Token** | One unit of text, usually a word | `"the pizza"` → `['the', 'pizza']` | M9 |
| **Tokenization** | Chopping a string into tokens | `re.findall(r"\b\w\w+\b", text)` | M9 |
| **`train_tf`** | The training transform, with all the random augmentation in it | Flips and crops — and it must never touch the test set | M7 |
| **Training set** | The practice papers. The only split allowed to influence the model's weights | 1,200 of the 2,000 pizza orders | M1 |
| **Transfer learning** | Reusing a model trained on a huge dataset for your much smaller problem | Frozen resnet18 features + a new 10-class head | M7 |
| **True negative (TN)** | It was negative and you said negative | A normal purchase, left alone | M3 |
| **True positive (TP)** | It was positive and you said positive | A real fraud, caught | M3 |
| **`TruncatedSVD`** | PCA's sparse-friendly cousin — use it on TF-IDF matrices, which you must not densify | `TruncatedSVD(n_components=2)` on 20,000 documents | M9 |

---

## U

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Unit of prediction** | What one row of your table stands for | One pizza order | M1 |
| **Unsupervised learning** | Finding patterns when nobody gave you the right answers | Sorting 500 mixed Lego bricks with no instructions | M8 |

---

## V

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Validation set** | The mock exam. Used to choose models, features and thresholds — and burned in the process | 400 of the 2,000 pizza orders | M1 |
| **Vanishing gradient** | Gradients shrinking toward zero as they pass back through many saturating layers | `0.25⁵ ≈ 0.001` | M5 |
| **`venv`** | A private box holding this level's exact library versions, so nothing else on your machine can break it | `python3 -m venv .venv` | SET |
| **Vocabulary** | The ordered list of every term the vectorizer knows; column `j` means term `j` | `get_feature_names_out()` — print it before trusting anything | M9 |

---

## W

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Weight** | How strongly one input pushes the answer up or down | `w = −1.5` on "days late" pushes the prediction down hard | M4 |
| **Weight sharing** | Using the same filter weights at every position in the image | 28 weights applied at 1,024 positions | M7 |
| **Word embedding** | A short dense vector per word, sitting near other similar words | `cat` and `dog` at cosine 1.0 in Part G | M9 |

---

## Z

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **`zero_grad()`** | Clearing the old gradients before computing new ones — the **first line** of every inner loop | Forgetting it costs ~36 accuracy points and raises nothing | M6 |
| **z-score** | See **Standardization** — how many standard deviations a value sits from the mean | `(9 − 5) / 2 = 2.0` | M2 |

---

## 🧩 The Confusion Pairs

These are the pairs that get mixed up most. If you only reread one part of this page, make it this table.

| These two | The difference | How to remember |
|---|---|---|
| **Precision** and **recall** | Precision reads **down the predicted-positive column**: of what I flagged, how much was right. Recall reads **across the actual-positive row**: of what was really positive, how much I caught. | Precision is about your *claims*. Recall is about the *world*. |
| **False positive** and **false negative** | FP = a false alarm. FN = a miss. | The word after "false" is what *you said*. |
| **ROC-AUC** and **average precision** | ROC's no-skill baseline is always 0.5. AP's is the positive rate. | On a 1%-positive set, AP 0.19 is excellent and AUC 0.60 is poor. |
| **`fit`** and **`transform`** | `fit` **learns** numbers from data. `transform` **applies** them. | Only training data may be `fit` on. Ever. |
| **Target leakage** and **preprocessing leakage** | Target leakage is a *column* that shouldn't exist yet. Preprocessing leakage is a *statistic* computed too early. | One is a bad feature; the other is a bad workflow. |
| **Validation set** and **test set** | You may look at validation as often as you like, and it degrades a little each time. You look at test once. | Mock exam vs sealed final. |
| **One-hot** and **ordinal encoding** | One-hot invents no ordering. Ordinal claims one. | If you can't say the order out loud without wincing, use one-hot. |
| **Standardization** and **min-max scaling** | z-score centres at 0 with std 1 and tolerates outliers. Min-max forces the range 0–1 and one outlier squashes everything else. | Bell curve vs bounded slider. |
| **Loss** and **metric** | Loss is what training minimises (must be differentiable). The metric is what you report (must be meaningful to a human). | You train on log loss and get judged on recall. |
| **Log loss** and **squared error** | Log loss punishes confident wrongness without limit. Squared error caps out at 1. | Classification measures surprise, not distance. |
| **Gradient** and **gradient descent** | The gradient is a *direction* (uphill). Gradient descent is the *rule* that walks the other way. | Always subtract. `w -= lr * grad`. |
| **Epoch** and **step** | An epoch is one pass over the data. A step is one weight update. | 400 rows at batch 32 = 1 epoch = 13 steps. |
| **`z` (pre-activation)** and **`a` (activation)** | `z` is before the squash, `a` is after. | Backprop needs both — `z` for the derivative, `a` for the next layer. |
| **`model.train()`** and **`model.eval()`** | `train()` turns dropout on. `eval()` turns it off and freezes batch-norm. | If `predict.py` gives different answers twice, you forgot `eval()`. |
| **`zero_grad()`** and **`no_grad()`** | `zero_grad()` clears yesterday's gradients before training. `no_grad()` stops recording gradients at all, for evaluation. | One is hygiene, one is a switch. |
| **`train_tf`** and **`eval_tf`** | Training transforms are random. Evaluation transforms are deterministic. | Augment what you learn from; never augment what you measure with. |
| **Stride** and **padding** | Stride is how far the window jumps (bigger = smaller output). Padding is the zero border (bigger = larger output). | `out = floor((n + 2p − k)/s) + 1` settles every argument. |
| **Inertia** and **silhouette** | Inertia always falls as `k` rises, so it can't choose `k`. Silhouette can have an interior maximum, so it can. | Elbow finds a bend; silhouette finds a peak. |
| **PCA** and **k-means** | PCA finds new *axes*. k-means finds *groups*. | One rotates the room; the other sorts the people in it. |
| **TF** and **IDF** | TF counts this document. IDF counts *how many documents* contain the word. | TF is local, IDF is global. Multiply them. |
| **Cosine similarity** and **dot product** | Cosine divides out the lengths, so long documents don't win automatically. | On L2-normalized TF-IDF rows they're the same number — because the lengths are already 1. |
| **Bag-of-words** and **embedding** | Bag-of-words is one sparse column per word, with no notion of meaning. An embedding is a short dense vector where similar words sit near each other. | `cat` and `dog` share nothing in BoW and are neighbours in embedding space. |
| **Model** and **artifact** | The model is the idea. The artifact is the file — weights *plus* every preprocessing step. | If it doesn't load in a fresh process, you don't have an artifact. |

---

## 🧮 The Formulas Worth Memorising

| Name | Formula | Where |
|---|---|---|
| Standardization | `z = (x − mean_train) / std_train` | M2 |
| Precision / recall | `TP/(TP+FP)` · `TP/(TP+FN)` | M3 |
| F1 | `2 · (P · R) / (P + R)` | M3 |
| Expected cost | `C_FN × FN + C_FP × FP` | M3 |
| Sigmoid | `σ(z) = 1 / (1 + e^(−z))` | M4 |
| Log loss (one row) | `−[y·ln(p) + (1−y)·ln(1−p)]` | M4 |
| Gradient descent | `w ← w − lr · ∂L/∂w` | M4 |
| Logistic gradient | `∂L/∂w = (1/n) Σ (p − y)·x` | M4 |
| He init | `std = sqrt(2 / n_in)` | M5 |
| Numerical gradient | `(L(w+ε) − L(w−ε)) / (2ε)` | M5 |
| Conv/pool output size | `out = floor((n + 2p − k) / s) + 1` | M7 |
| Smoothed IDF | `idf = ln((1 + n) / (1 + df)) + 1` | M9 |
| Cosine similarity | `(a · b) / (‖a‖ · ‖b‖)` | M9 |

And one number to know on sight: **`ln 2 = 0.6931`**. If your training loss sits there, your model is predicting 0.5 for everything and has learned nothing at all.

---

## 📈 What's Coming in Level 4

These words are **not** in this level. If you meet one in the wild, that's fine — it's a preview, not a gap.

| Term | One-line preview | Where |
|---|---|---|
| **Recurrent network (RNN / LSTM)** | A model that reads a sentence one token at a time and carries a memory forward — the direct fix for what bag-of-words threw away | L4 M2 |
| **Attention** | Letting every token look at every other token and decide which ones matter | L4 M3 |
| **Transformer** | Attention stacked into the architecture that everything modern is built from | L4 M3 |
| **Pretraining / fine-tuning at scale** | How a large language model is actually made, and what it costs | L4 M4 |
| **Prompt engineering** | Steering a trained model with words instead of gradients | L4 M5 |
| **Vector database / RAG** | Storing embeddings so a model can look things up before answering | L4 M6 |
| **Agent / tool use** | A model that can call your `predict.py` instead of guessing | L4 M7 |
| **LLM evaluation** | Rubrics, judges, and why "it sounded good" is not a metric | L4 M8 |

Notice how many of those are Level 3 ideas wearing a bigger coat. Attention is a weighted sum. RAG is cosine similarity. LLM evaluation is a confusion matrix that grew up. You already own the floor.

---

[Level 3 Home](README.md) · [Assessment](assessment.md) · [Capstone](capstone.md) · [Module 1](module-01-the-supervised-pipeline.md) · [Level 4 ➡](../level-4-innovator/)

*If a word isn't here, it wasn't taught in this level — and you're allowed to not know it yet.*

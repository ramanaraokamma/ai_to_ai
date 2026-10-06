# Week 17 — Build TinyGPT

[⬅ Week 16](week-16.md) · [Course Home](../README.md) · [Week 18 ➡](week-18.md) · [Student Guide](../student-guide/week-17.md) · [Workbook](../workbook/week-17.md)

---

![The 36 week tiles in four term lanes; weeks 1 to 16 solid, week 17 tinted pink with a thick border and a pointer above it, weeks 18 to 36 dashed](../figures/fig-w17-0-where-this-fits.svg)
*Figure 17.0 — Week 17 of 36, the TinyGPT lab, sits in term 2 (memory, then attention); weeks 1 to 16 are done and weeks 18 to 36 are still ahead.*

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes in class (one 85-second training run sits inside it), then the workbook (~60-75 min) |
| **Type** | 🟩 Lab — the student **assembles the whole model** from the parts of Week 16, checks its size and its first loss before trusting it, trains it on CPU, and reports what the run shows |
| **Big idea** | A GPT is Week 16's block stacked four times with a character table, a place table, one last norm and an output layer around it. It is trained on one question asked 2,048 times per step: *given the characters so far, what comes next?* Before it learns anything, its loss must be **about `ln(28) = 3.332`**, the loss of a model that knows nothing. That is a **check, not a hope**: you run it. After training the model gets much better on the text it was trained on (loss 0.9) than on text it has not seen (1.4), and **that gap is the lesson's last word**. |
| **New vocabulary** | window · batch · context length · decoder-only · first-loss check · checkpoint · train loss / validation loss · gap · overfitting (named earlier in Week 5; applied here) |
| **New maths** | **None.** The loss is `-ln(p)` of the true next character (Week 1's `ln 2`, now `ln 28`); the rest is counting knobs (Week 16) and one division (passes over the text). See the 🔢 box. |
| **New syntax** | `torch.randint` batching · `@torch.no_grad()` (used, not written) · nested `nn.Module`. That is all three. |
| **Dataset** | The shared kit's typed corpus, `l4lib.corpus.TEXT`: **6,972 characters, 28 distinct**, split 6,274 train / 698 validation. In `key.py` (teacher only) the same text is used to score counting models. **Nothing downloads. No internet.** |
| **Model** | **A real TinyGPT, really trained**: 807,196 knobs, width 128, 4 heads, 4 blocks, 64 places, 1,500 steps, one CPU thread. **There is no scripted backend and no stand-in anywhere in this week.** The text it learns from is 6,972 characters, so it is a toy. |
| **Materials** | Laptop with Python 3 and torch (nothing new to install) · the folder that contains `l4lib/` · the student's own `block.py` from Week 16 · six printed "Beat the Ladder" cards (Activity) · a calculator with an `ln` key · workbook pages 17.1-17.6 · a timer |
| **Prep time** | 30 minutes the night before (the longest step is one 90-second run) · 3 minutes on the day |
| **Expected runtime of the code** | `check_init.py` under 1 second · **`train.py` about 80-95 seconds** (measured 53 ms per step on the author's CPU, one thread; other laptops will differ) · `key.py` under a second. The deliberate-mistake files total about 40 seconds. If `train.py` takes over **4 minutes**, something is wrong (see Fallback). |

> **⚠️ Watch out:** three things go wrong this week. **First, the samples look like writing and are not.** The final sample has "the old man" and "the birds" in it, and 60% of its words are words that appear in the training text (`train.py` measures it). It also has `menthy`, `witer` and `boird`. The model has learned the *shape* of these sentences, a character at a time, from 6,972 characters. It has not read anything. Do not let "it writes English" become the sentence the student leaves with. **Second, the gap is easy to misread.** Train loss 0.9 against validation 1.4 does not mean "the model is good". It means it does much better on text it has seen than on text it has not. We offer one explanation for it (490 passes over 6,274 characters, 807,196 knobs), and the printout gives you evidence for it (the gap is -0.02 at step 250 and grows at every later checkpoint), but **we did not run a control** (less training, more text, dropout), so say "consistent with memorising", not "proof". **Third, a failing check is not always a bug.** With PyTorch's default output layer, the first-loss check prints `FAIL` (3.50 against 3.33) and the model is perfectly trainable; in our 150-step run it was even *ahead*. The check is a tool: you learn to read how far off it is, and the second mistake in the Clinic (`y` not shifted) is one that it **cannot** catch.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Say what one training step asks**: a batch of 32 windows of 64 characters is 2,048 questions, *what comes after each prefix?*, and `y` is `x` moved one place left. They show it on real text (`check_init.py`).
2. **Assemble `TinyGPT` from the Week 16 block**: a character table, a place table (`torch.arange`), four `Block`s in an `nn.ModuleList`, a final layer norm and an output layer. They explain why this is a module *inside* a module and what `model.parameters()` does with that.
3. **Predict the model's size and its first loss, then check both**: 807,196 knobs (Week 16's number, now matched by `.numel()`), and a first loss within 0.05 of `ln(28) = 3.3322`.
4. **Train it and report the run honestly**: the measured step time, three checkpoint samples (steps 0, 300, 1499), train loss and validation loss, and the gap.
5. **Say what the gap means** in two sentences, and what it does **not** mean.

Observable evidence: `check_init.py` printing `PASS` for the calm head and `match: True` for the knob count; `train.py` printing a step time, three samples and a `FINAL` line; the **Beat the Ladder** card scored by the student; and the workbook's written answer to *"what does the gap mean?"*

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Every block in the **🧰 Prep Checklist** is a *whole file* and every one was run, from one folder next to `l4lib/`, on a CPU with `torch.set_num_threads(1)` and the seeds shown. Blocks in the **🐞 Debugging Clinic** are *deliberate mistakes* and each is marked; their tracebacks are real. Outputs are real. **`train.py` was run four times and the losses and samples were identical each time; only the `step time` line changed** (53 to 62 ms). The numbers labelled **ledger** come from the course author's reference run of Module 3 (seed 1337, dropout 0.1, 2,500 steps) and were **not** run for this lesson; they are different enough that they are a comparison in *direction*, not a target.

### 1. What the student is doing today, in one paragraph

Last week the student met every part of a GPT and counted the knobs of one block by hand. Today they build the rest. They start from their own `Block` from last week, unchanged, and write `TinyGPT`: a character table (`nn.Embedding`), a place table, four blocks held in an `nn.ModuleList`, a final `nn.LayerNorm` and an output `nn.Linear` with one score per character. Before training they do two checks: the knob count must be **807,196**, the number they predicted last week, and the first loss must be within 0.05 of `ln(28)`. Then they write `get_batch`, which cuts random 64-character windows from the text with `torch.randint`, and a training loop built from parts they already own (AdamW, warm-up and cosine, gradient clipping). While it trains for about 85 seconds they play **Beat the Ladder** on paper, guessing the next character of six real places in the text. Then they read the results together: three samples from three moments of training, the step time, and the train and validation losses, and they argue about what the gap between the two means. **Nothing in the lesson is a chatbot.** It is a 6,972-character text and an 807,196-knob model.

### 2. 🔢 The maths you need — taught to you first

**There is no new mathematical idea this week.** There are four pieces of arithmetic. Do them before class.

**(a) The loss of a model that knows nothing.** The loss is `-ln(p)`, where `p` is the probability the model gave to the character that *really* came next (Week 1: for two classes a coin-flip model has `-ln(0.5) = 0.693`). A model that knows nothing gives every one of the 28 characters `p = 1/28`, so its loss is `-ln(1/28) =` **`ln(28) = 3.3322`**. A model that gave the right character `0.9` would score `0.105`; `0.1` scores `2.303`; `0.01` scores `4.605`. *Low loss means the right character got a big share.* `key.py` prints these.

**(b) The three questions per step, counted.** A step uses 32 windows of 64 characters. The causal mask (Week 15) means every place in a window sees only what came before it, so **one forward pass answers all 64 questions in each window**: `32 x 64 =` **2,048** questions per step. (Compare Week 12: training feeds the true previous character and runs in parallel; generating feeds back the model's own guess and runs one character at a time. It is the same split.)

**(c) The gap, in numbers.** The training text has 6,274 characters. In 1,500 steps the model is asked `1,500 x 2,048 = 3,072,000` questions, which is `3,072,000 / 6,274 =` **490 passes** over the text. The model has 807,196 knobs for 6,274 training characters: `807,196 / 6,274 =` **128.7 knobs for every character it is trained on**. Those two numbers are why it is unsurprising that the model learns the training text much better than the held-out text. They are not a measurement of overfitting; the printout is.

**(d) The size, by part** (Week 16's formula, now with a vocabulary of 28):

```text
character table   28 x 128                            =   3,584
place table       64 x 128                            =   8,192
4 blocks          4 x (12 x 128^2 + 10 x 128)         = 791,552
final norm        2 x 128                             =     256
output layer      128 x 28 + 28                       =   3,612
                                                        -------
                                                        807,196
```

> **How good is a loss of 1.4? The ladder.** `key.py` (Prep file 4) scores three models that only *count*, on the same held-out text, as the average `-ln(p)` of the true next character: **knows nothing: 3.332 · knows only how common each letter is: 2.855 · knows only the previous letter: 2.033.** The TinyGPT ends at about **1.44**. That is the honest frame for "is this good?": it beats everything that only counts one or two characters, and it is nowhere near a model that has read a library. (Counting models are add-one smoothed and scored on the 698 held-out characters. One text, one split.)

![Two rows of character cells, x above and y below, where y is x moved one place left; below them 64 questions times 32 windows equals 2,048 questions.](../figures/fig-w17-1-one-window-many-questions.svg)
*Figure 17.1 — Moving the window one place left gives a next-character answer at every place, so one step asks 2,048 questions.*

![Left, a chart of training loss (solid) and validation loss (dashed) against step, with a dashed line at ln 28 and a bracket marking the final gap. Right, two bars: the first-loss distance for calm_head=False (long, FAIL) and calm_head=True (short, PASS).](../figures/fig-w17-2-loss-gap-and-first-check.svg)
*Figure 17.2 — Training loss keeps falling while validation flattens, and a calm output layer starts within 0.05 of ln 28.*

### 3. 🧭 Real vs stand-in — and what you must NOT claim

| Thing | Real or stand-in? |
|---|---|
| The model, the training loop, every loss, every sample, the step time | **Real.** PyTorch on the CPU, one thread, `torch.manual_seed(0)`. |
| The corpus | **Real text, typed by the course author** (`l4lib.corpus`). Lower-case, little punctuation, a lot of repetition on purpose. |
| The knob count (807,196), the parts, `match: True` | **Real**, counted by `.numel()`; also plain arithmetic. |
| The counting models in `key.py` (uniform, letter frequency, previous letter) | **Real and simple** (numpy counts, add-one smoothing). They are *baselines for scale*, not competitors. |
| The six Beat the Ladder cards | **Real places in the training text.** The counts-based probabilities beside them are real. |
| The ledger figures (2,500 steps, train 0.150 / val 1.669; val 1.328 at step 1,000; 133 s) | **Real runs by the course author** of a different setup (dropout 0.1, seed 1337, two CPU threads; other differences were not isolated). **Not run today.** |
| Any language model you could talk to | **Not present.** The model continues a few characters; it does not answer. No stand-in anywhere this week. |

> **Say to the student, out loud:** *"Everything today is real: a real model, really trained, on 6,972 characters. It is small enough to train in a minute and a half, so it is small enough to understand all the way down. Whatever it does with this text, it does because of what is in these files."*

> **🚫 What you must NOT claim.**
> 1. **"The model understands / has learned to write."** It has learned which character tends to follow which prefix in *this* text. 60% of the words in a long sample are words from the training text; the rest are near-misses. Say "it has learned the shape of the text".
> 2. **"The gap *proves* overfitting."** Say "the gap is what overfitting looks like, and the gap grows as training goes on". We did not run the control (more text, less training, dropout). The 490 passes and 128.7 knobs per character are *reasons to expect it*, not an experiment.
> 3. **"Step 1,500 is the best place to stop."** In this run the lowest validation loss *printed* was 1.417 at step 1,000, and it rose a little after (1.427, 1.437, 1.447). The differences are a few hundredths and each validation number is an average of 20 random windows from 698 characters, so it is noisy (the `step 1499` line and the `FINAL` line are two estimates of the same model and differ by 0.010). Do not teach a stopping step from this.
> 4. **"The calm head makes it train better."** It makes the *first loss honest*. In our 150-step test (Clinic 1) the un-calmed model was ahead. We did not run it to 1,500.
> 5. **"This is how ChatGPT is trained."** It is the same next-character (next-token) question, asked of a much smaller model on a vastly smaller text. Week 20 onward is about what changes with scale.

### 4. The three new constructs, for somebody who has never seen them

**(a) `torch.randint(high, (B,))` — random whole numbers, used to pick where each window starts.**

```python
import torch

torch.manual_seed(0)
starts = torch.randint(10, (4,))          # four whole numbers, each from 0 to 9 (10 is not included)
```

Read as: *"draw four dice that go from 0 to 9."* Like `range`, the top is **not included**. The shape `(4,)` is how many numbers. In `get_batch` it draws `B = 32` starts, and the window for a start `s` is `data[s : s + T]` for `x` and `data[s + 1 : s + T + 1]` for `y`. The last start that leaves room for `y` is `len(data) - T - 1`, so the call is `torch.randint(len(data) - T, (B,))`: **one more than that and a rare batch crashes** (Clinic 4). Unlike the `torch.randperm` of Week 5 this draws *with* replacement: the same start can appear twice in a batch, and it does not matter.

**(b) `@torch.no_grad()` — the decorator form of `with torch.no_grad():`.** (An excerpt from `tinygpt.py`, not a file of its own.)

```text
@torch.no_grad()
def generate(self, idx, n_new, temperature=1.0):
    ...                                   # everything in here runs as if inside `with torch.no_grad():`
```

Read as: *"run this whole function with gradients off."* The student has used `with torch.no_grad():` since Level 3 Week 21 to say "I am only looking, not learning". The `@` line directly above `def` says it for the entire function, so you do not have to indent the body. **The student types the line; nobody writes a decorator today**, and the ladder keeps that out of scope: *"a line above `def` that wraps the function; treat it as a label that says 'no learning in here'."* If asked how it works, say "a function that takes a function and returns a changed one" and stop. The difference is **small here**: Clinic 5 times it (200 characters, within about 10-15% either way). We say so and do not oversell.

**(c) A nested `nn.Module` — a module whose parts are modules, some of them our own.** (An excerpt from `tinygpt.py`.)

```text
class TinyGPT(nn.Module):
    def __init__(self, V, d, H, L, T, calm_head=True):
        super().__init__()                                                    # first line, always
        self.tok = nn.Embedding(V, d)
        self.blocks = nn.ModuleList([Block(d, H, T) for _ in range(L)])      # L of OUR Blocks, inside this module
```

Read as: *"this model contains four Blocks, and each Block contains its own layers."* It is a **tree**: `TinyGPT` holds `tok`, `pos`, `blocks`, `ln_f` and `head`; `blocks` holds four `Block`s; each `Block` holds `ln1`, `q`, `k`, `v`, `proj`, `ln2`, `up`, `act`, `down`. **`model.parameters()` walks the whole tree**, so one `AdamW(model.parameters(), ...)` trains every knob in all of it, and `model.blocks.parameters()` counts just the stack (791,552). Last week's `ModuleList` was a list of layers; today's is a list of *our own classes*. Two rules make the tree visible to PyTorch: `super().__init__()` must come first (Clinic 8, loud), and the blocks must go in an `nn.ModuleList`, not a Python list (Clinic 3, **silent**). Week 16's Block was deliberately flat so that today is the first time one of our classes holds another.

### 5. The other code the student types — nothing new, but note these

- **`nn.Embedding`** (Week 8) for characters and places; **`torch.arange(T)`**, **`nn.ModuleList`**, **`register_buffer`** and the flat `Block` (Week 16, pasted from the student's own `block.py`).
- **`F.cross_entropy(logits.reshape(B * T, -1), targets.reshape(B * T))`** (Week 12 introduced `cross_entropy`; `.reshape` with `-1` is Level 3). Flattening is needed because `cross_entropy` wants a list of rows (Clinic 7).
- **`F.softmax(..., dim=-1)`**, **`torch.multinomial`** and the **temperature** division (Week 13), and **`torch.cat`** (Level 3 Week 27) in `generate`. `logits[:, -1, :]` is the scores of the **last** place only.
- **`torch.stack`** (Week 10) to make a batch out of windows.
- **`AdamW(..., weight_decay=0.1)`** (Week 3), **`LambdaLR` with a `lambda` for warm-up then cosine** (Week 4), **`clip_grad_norm_`** (Week 6), **`zero_grad(set_to_none=True)`** (Week 2), **`sched.step()`** (Week 4).
- **`time.perf_counter()`** (Level 3 Week 26, used in Weeks 7-8) for the step time; `math.log` (Week 1).
- **A dict comprehension with `enumerate`** for `stoi` and `itos` (Week 8, Level 2), `sorted(set(TEXT))`, `set(...)`, `w in known`, `.split()`, `.replace(...)`, f-strings with `:.3f` and `:<6`.
- **`with torch.no_grad():`** (Level 3 Week 21) around the check; **`self.head.weight *= 0.1`** inside it (an in-place change of a weight under `no_grad`, the same move as Week 11's `fill_`).
- **A keyword argument with a default** (`calm_head=True`, Level 2).
- **`tuple(x.shape)`**, boolean masks and `.all()` (Level 3).

**`key.py` is teacher-only** and uses `zip`, `np.ones` and a few numpy lines that the student has not been taught in this form; it is never shown to the student. Everything else below the student does type.

**Not used today, on purpose:** dropout inside the model (the reference uses 0.1; see Questions), weight tying, `nn.init` functions (Week 31), any decorator the student writes, a learned-vs-sinusoidal comparison, key-value caches, `torch.compile`, a GPU or `device=` arguments.

### 6. What the numbers will say

These are all printed by the files below. Read them before class so nothing surprises you.

- **The data (`check_init.py`).** 6,972 characters, vocabulary 28, train 6,274, validation 698. `x` and `y` are both `(32, 64)`; the first row of `x` is `' to school with a book u'` and the first row of `y` is `'to school with a book un'`; `y is x moved one place left: True`.
- **The first-loss check.** `calm_head=False`: **3.5025**, distance 0.1702, `FAIL`. `calm_head=True`: **3.3481**, distance 0.0159, `PASS`.
- **The size.** `tok` 3,584 · `pos` 8,192 · `blocks` 791,552 · `ln_f` 256 · `head` 3,612; predicted 807,196, actual 807,196, `match: True`; 128.7 knobs per training character.
- **The run (`train.py`).**

| Step | Train | Validation | Gap | Real words in a 1,000-character sample |
|:--:|:--:|:--:|:--:|:--:|
| 0 | 3.349 | 3.351 | 0.002 | 0% |
| 250 | 1.964 | 1.944 | -0.020 | |
| 300 | 1.873 | 1.892 | 0.019 | 17% |
| 500 | 1.558 | 1.647 | 0.089 | |
| 750 | 1.181 | 1.470 | 0.289 | |
| 1000 | 0.999 | 1.417 | 0.418 | |
| 1250 | 0.905 | 1.427 | 0.522 | |
| 1499 | 0.894 | 1.437 | 0.543 | 60% |
| FINAL | 0.907 | 1.447 | 0.540 | |

The step 0 numbers are within 0.02 of `ln(28)`. The gap is about zero while the model is still bad at everything, and then opens. **Step time 53 ms (another run on the same machine: 62 ms), 80 seconds of training, 490 passes.**
- **The samples.** Step 0: random characters (`thsneqol.hupmxzcgos ...`). Step 300: the letters `the`, `and`, `an` appear but there are no sentences (`the man adid ing sa theand and the fowit ...`). Step 1499: lines that start with `the`, end with a full stop, and are made of real words joined with near-words (`the old man mem menthy witer.`). The final 300-character sample from the prompt `the ` follows the same pattern.
- **The ledger comparison (not run today).** 2,500 steps, dropout 0.1, seed 1337: train **0.150**, validation **1.669**, with the validation loss lowest (1.328) around step 1,000 and rising afterwards. Our 1,500-step run finishes with a smaller gap (0.54). **Do not explain that gap by the shorter run:** the ledger also ran a 1,500-step model with the same AdamW, warm-up and cosine schedule (`_ledger/out/m03_05_ablate_baseline.txt`) and it finished at train 0.411, validation 1.336, a gap of 0.925, so step count and schedule do not account for the difference, and our training loss (0.894) is more than double the ledger's. We did not isolate the cause (batch size, model width, data pipeline and seed are all candidates). *The direction matches (training falls much faster than validation); do not compare the digits, and do not offer a cause.*

### 7. The honest limits of today

1. **One seed, one text, one machine.** Every number comes from `torch.manual_seed(0)`. We did not run other seeds. A different seed would change the third decimal, and probably the samples completely.
2. **The validation set is 698 characters.** Each printed loss is the mean of 20 random windows of 64 characters, so it is a noisy estimate (the same model gave 1.437 and 1.447 on two estimates). Differences under about 0.02 are not information.
3. **"Real words" is a crude score.** It counts whitespace-separated pieces that appear anywhere in the training text, punctuation attached. It rewards copying a phrase from the corpus and says nothing about meaning.
4. **The gap's cause is not isolated.** We did not train with dropout, on more text, or for fewer steps *as a controlled comparison*. (Fallback run of 600 steps: train 1.757, validation 1.800, gap 0.043, 20% real words. Shorter training, smaller gap: consistent with the story, not a proof of it.)
5. **The learning rate (3e-4), the 100 warm-up steps, weight decay 0.1 and the clipping at 1.0 are the reference module's choices.** We did not tune them this week; Week 4's lesson is that you can.
6. **No dropout.** The reference module uses `Dropout(0.1)`; we left it out so that the Block is exactly last week's. We did not measure what it would change.
7. **Speed is one machine's.** 53 ms per step is this laptop's. The module's own figure of 133 s for 2,500 steps was on two threads. The course pins one thread (Week 1) so results reproduce; it is not the fastest setting.
8. **The counting baselines are quick ones.** Add-one smoothing on 6,274 training characters; a cleverer counter (longer context) would score better than 2.033. The ladder says "a model that only counts the previous letter", nothing more.

### 8. The misconceptions you will actually meet

1. **"The loss started at 3.3 so the model is already 70% right."** Loss is not a percentage. 3.332 is *no knowledge*; lower is better; there is no "100%".
2. **"Train loss 0.9 is better than validation 1.4, so the model is better on training data, so training data is 'the real data'."** Both are the same kind of text. The model saw one and not the other.
3. **"More steps is always better."** Our validation loss stopped improving around step 1,000 while the training loss kept falling. The lesson is to watch both.
4. **"The model copies the text."** Partly (60% of the words of the sample are from the training text) and partly not (`menthy`, `witer`). Checking a sample against the corpus is a test anyone can run; we did not search for whole copied sentences.
5. **"Nested means the same as inherited."** `TinyGPT` *contains* Blocks; it is not a kind of Block. A good one-line check is `model.blocks[0]`.
6. **"The output of `generate` is the model's answer."** It is a *sample* from the model's probabilities, drawn with `torch.multinomial`; change the seed and it changes.

### 9. How deep to go, and where to stop

Stop at: *"we built the whole thing from last week's parts; it starts at `ln 28` because it knows nothing; it learns the shape of the text; it learns the training text better than text it hasn't seen, and that gap grows."* Do **not** go into why attention heads specialise (we did not inspect any), the scaling of loss with size (Week 21), why the position table works, dropout's mechanism, learning-rate tuning, or beam search. If the student asks *"how do I make it better?"*: *"more text and a bigger model is the honest answer, and Week 21 measures it. There is nothing in today's run that tells us which of our settings is the limit."*

### 10. 🧭 Where Week 17 sits

```text
   W14 attention by hand        W16 positions + the block        W17 BUILD AND TRAIN (today)
   W15 scale, mask, heads  -->  one block, counted by hand  -->  tok + pos + 4 blocks + norm + head
                                                                 807,196 knobs = the number W16 predicted
                                                                 first loss ~ ln(28)   (a check)
                                                                 1,500 steps, 85 s, 3 samples, train vs val
                                W18 Review & Assessment 2 (weeks 9-17)
                                W19 TinyGPT ablations: delete the mask, positions, residuals, norm; measure
                                W20 tokenisers: the same model, but characters become BPE pieces
                                W21 scaling: train four widths; loss falls as a power law
```

---

## 🧰 Prep Checklist

### 30 minutes the night before

- [ ] **Confirm the stack.** Run from the folder that contains `l4lib/`:

```bash
python3 -c "import torch; print(torch.__version__)"
python3 -c "from l4lib.corpus import TEXT; print(len(TEXT), len(set(TEXT)))"
```

You must see (the first line's digits may differ on another PyTorch version):

```text
2.2.1
6972 28
```

If `l4lib` is not found you are in the wrong folder. `pip` returning 403 is expected and not an error; **nothing this week installs anything.**

- [ ] **Type the files below into one working folder** (next to `l4lib/`). Each begins with a `#` comment naming it. Run each one in order and compare with the output printed here.

**File 1 — `tinygpt.py`** (the model; the student types `TinyGPT` and pastes their own `Block` from `block.py`). It prints nothing; it is imported by every other file.

```python
# tinygpt.py - Week 17: the whole TinyGPT. Block is YOUR Week 16 block, unchanged; TinyGPT holds four of them.
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.set_num_threads(1)


class Block(nn.Module):
    def __init__(self, d, H, T):
        super().__init__()
        self.H = H
        self.ln1 = nn.LayerNorm(d)
        self.q = nn.Linear(d, d, bias=False)
        self.k = nn.Linear(d, d, bias=False)
        self.v = nn.Linear(d, d, bias=False)
        self.proj = nn.Linear(d, d)
        self.register_buffer("mask", torch.tril(torch.ones(T, T)))
        self.ln2 = nn.LayerNorm(d)
        self.up = nn.Linear(d, 4 * d)
        self.act = nn.GELU()
        self.down = nn.Linear(4 * d, d)

    def forward(self, x):
        B, T, d = x.shape
        dh = d // self.H
        h = self.ln1(x)
        q = self.q(h).view(B, T, self.H, dh).transpose(1, 2)
        k = self.k(h).view(B, T, self.H, dh).transpose(1, 2)
        v = self.v(h).view(B, T, self.H, dh).transpose(1, 2)
        scores = q @ k.transpose(-2, -1) / dh ** 0.5
        scores = scores.masked_fill(self.mask[:T, :T] == 0, float("-inf"))
        weights = F.softmax(scores, dim=-1)
        mixed = (weights @ v).transpose(1, 2).reshape(B, T, d)
        x = x + self.proj(mixed)
        x = x + self.down(self.act(self.up(self.ln2(x))))
        return x


class TinyGPT(nn.Module):
    """Nested module: a model whose parts include four of our own Blocks."""

    def __init__(self, V, d, H, L, T, calm_head=True):
        super().__init__()
        self.T = T                                                         # the context length: how many places
        self.tok = nn.Embedding(V, d)                                      # which character
        self.pos = nn.Embedding(T, d)                                      # which place (Week 16)
        self.blocks = nn.ModuleList([Block(d, H, T) for _ in range(L)])   # L Blocks inside this module
        self.ln_f = nn.LayerNorm(d)                                        # one last norm
        self.head = nn.Linear(d, V)                                        # d numbers -> one score per character
        if calm_head:
            with torch.no_grad():
                self.head.weight *= 0.1                                    # start the scores near zero (see check_init.py)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        x = self.tok(idx) + self.pos(torch.arange(T))
        for blk in self.blocks:
            x = blk(x)
        logits = self.head(self.ln_f(x))                                   # (B, T, V)
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.reshape(B * T, -1), targets.reshape(B * T))
        return logits, loss

    @torch.no_grad()
    def generate(self, idx, n_new, temperature=1.0):
        for _ in range(n_new):
            logits, _ = self(idx[:, -self.T:])                             # never more than T places
            probs = F.softmax(logits[:, -1, :] / temperature, dim=-1)      # the LAST place's scores
            idx = torch.cat([idx, torch.multinomial(probs, 1)], dim=1)
        return idx
```

**File 2 — `check_init.py`** (the data, the batches, the size, and the first-loss check; nothing is trained)

```python
# check_init.py - Week 17: the data, the batches, the size, and the first-loss check. Nothing is trained.
import math
import torch
from tinygpt import TinyGPT
from l4lib.corpus import TEXT

torch.manual_seed(0)

chars = sorted(set(TEXT))                                # every distinct character, in order
V = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for i, c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in TEXT])
n = int(0.9 * len(data))
train_data, val_data = data[:n], data[n:]
print("characters:", len(TEXT), " vocab:", V, " train:", len(train_data), " val:", len(val_data))
print(f"ln(vocab) = ln({V}) = {math.log(V):.4f}")

d, H, L, T, B = 128, 4, 4, 64, 32


def get_batch(split):
    src = train_data if split == "train" else val_data
    starts = torch.randint(len(src) - T, (B,))           # B random places to start a window
    x = torch.stack([src[s:s + T] for s in starts])
    y = torch.stack([src[s + 1:s + T + 1] for s in starts])
    return x, y


x, y = get_batch("train")
print("x", tuple(x.shape), " y", tuple(y.shape))
print("x[0][:24] = |" + "".join(itos[int(i)] for i in x[0][:24]) + "|")
print("y[0][:24] = |" + "".join(itos[int(i)] for i in y[0][:24]) + "|")
print("y is x moved one place left:", bool((x[:, 1:] == y[:, :-1]).all()))

for calm in (False, True):
    torch.manual_seed(0)
    model = TinyGPT(V, d, H, L, T, calm_head=calm)
    with torch.no_grad():
        _, loss = model(x, y)
    gap = abs(loss.item() - math.log(V))
    verdict = "PASS" if gap < 0.05 else "FAIL"
    print(f"calm_head={calm}: first loss {loss.item():.4f}   distance from ln(V) {gap:.4f}   {verdict}")

parts = {"tok": model.tok, "pos": model.pos, "blocks": model.blocks, "ln_f": model.ln_f, "head": model.head}
for name, part in parts.items():
    print(f"  {name:<6}", sum(p.numel() for p in part.parameters()))
predicted = V * d + T * d + L * (12 * d * d + 10 * d) + 2 * d + (d * V + V)
actual = sum(p.numel() for p in model.parameters())
print("predicted knobs:", predicted, " actual:", actual, " match:", predicted == actual)
print(f"knobs per training character: {actual / len(train_data):.1f}")
```

```text
characters: 6972  vocab: 28  train: 6274  val: 698
ln(vocab) = ln(28) = 3.3322
x (32, 64)  y (32, 64)
x[0][:24] = | to school with a book u|
y[0][:24] = |to school with a book un|
y is x moved one place left: True
calm_head=False: first loss 3.5025   distance from ln(V) 0.1702   FAIL
calm_head=True: first loss 3.3481   distance from ln(V) 0.0159   PASS
  tok    3584
  pos    8192
  blocks 791552
  ln_f   256
  head   3612
predicted knobs: 807196  actual: 807196  match: True
knobs per training character: 128.7
```

Read the two check lines slowly. **`calm_head=False` is the model with PyTorch's default output layer, and the check fails; `calm_head=True` multiplies that layer's weights by 0.1 and it passes.** The number you watch is the *distance* from `ln(V)`, and the bar is 0.05. The knob count line ends the file: Week 16's hand count, matched by the machine.

**File 3 — `train.py`** (1,500 steps; takes about 85 seconds)

```python
# train.py - Week 17: train the TinyGPT on the typed corpus (1,500 steps, CPU, one thread), and watch it learn.
import math
import time
import torch
from tinygpt import TinyGPT
from l4lib.corpus import TEXT

torch.manual_seed(0)

chars = sorted(set(TEXT))
V = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for i, c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in TEXT])
n = int(0.9 * len(data))
train_data, val_data = data[:n], data[n:]

d, H, L, T, B = 128, 4, 4, 64, 32
STEPS, WARMUP = 1500, 100


def get_batch(split):
    src = train_data if split == "train" else val_data
    starts = torch.randint(len(src) - T, (B,))
    x = torch.stack([src[s:s + T] for s in starts])
    y = torch.stack([src[s + 1:s + T + 1] for s in starts])
    return x, y


@torch.no_grad()
def estimate(split, batches=20):
    total = 0.0
    for _ in range(batches):
        x, y = get_batch(split)
        _, loss = model(x, y)
        total += loss.item()
    return total / batches


known = set(TEXT.split())                                # every whitespace-separated word of the training text


def real_word_share(text):
    words = text.split()
    return sum(w in known for w in words) / len(words)


def sample(prompt, n_new=200, temperature=0.8):
    idx = torch.tensor([[stoi[c] for c in prompt]])
    out = model.generate(idx, n_new, temperature)[0].tolist()
    return "".join(itos[i] for i in out)


model = TinyGPT(V, d, H, L, T)
print("knobs:", sum(p.numel() for p in model.parameters()))

opt = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.1)
sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: (s + 1) / WARMUP if s < WARMUP
                                          else 0.5 * (1 + math.cos(math.pi * (s - WARMUP) / (STEPS - WARMUP))))

CHECKPOINTS = (0, 300, STEPS - 1)
spent = 0.0                                              # seconds spent inside training steps only
for step in range(STEPS):
    if step in CHECKPOINTS:
        print(f"\n--- step {step}: train {estimate('train'):.3f}  val {estimate('val'):.3f} ---")
        print(sample("t").replace("\n", " / "))
        print(f"real words in a 1,000-character sample: {100 * real_word_share(sample('t', 1000)):.0f}%")
    t0 = time.perf_counter()
    x, y = get_batch("train")
    _, loss = model(x, y)
    opt.zero_grad(set_to_none=True)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
    sched.step()
    spent += time.perf_counter() - t0
    if step % 250 == 0 and step > 0:
        print(f"step {step:4d}  train {estimate('train'):.3f}  val {estimate('val'):.3f}")

train_loss, val_loss = estimate("train"), estimate("val")
print(f"\nFINAL  train {train_loss:.3f}  val {val_loss:.3f}  gap {val_loss - train_loss:.3f}")
print(f"step time: {1000 * spent / STEPS:.0f} ms   total training: {spent:.0f} s")
print(f"passes over the training text: {STEPS * B * T / len(train_data):.0f}")
print()
print(sample("the ", 300))
```

```text
knobs: 807196

--- step 0: train 3.349  val 3.351 ---
thsneqol.hupmxzcgos aelb / mx / g mrrt.elt hfiiuyb /  / txmqga gs / ulosn gyyfzdkeluyle vhxmvfpvfurxhyeduagl uyaq.xirvcopuxmbo / z.papupplwtryshrbheibn.imo.nzrvfybcmkf / hwlups.mgqyneupogtoirwnsm / mvforlzbf.wbqnmomdr
real words in a 1,000-character sample: 0%
step  250  train 1.964  val 1.944

--- step 300: train 1.873  val 1.892 ---
the man adid ing sa theand and the fowit therothe ond rd and wise bofn therld care henoshe finerinbr thake berd tut the casand an helisaked d hewand cangh ad med theand herot thed dren ldat bold thefow
real words in a 1,000-character sample: 17%
step  500  train 1.558  val 1.647
step  750  train 1.181  val 1.470
step 1000  train 0.999  val 1.417
step 1250  train 0.905  val 1.427

--- step 1499: train 0.894  val 1.437 ---
the seay. / the old man mem menthy witer. / the birds wenthe baker backer wat or hiold every. / the sthe old man the boird sang thald sthem all. / the bauger and sun watt did nown. / the old man bothered to the.
real words in a 1,000-character sample: 60%

FINAL  train 0.907  val 1.447  gap 0.540
step time: 53 ms   total training: 80 s
passes over the training text: 490

the girl class and wither.
the cat quiester bonerray mand asking the board and to the werong.
the river roster and and the went wat did not nos ney cogke the rope maker not.
the ropened the buper sun the weent flob ordone oard did not.
the oacher wat or wat on the wall rose.
the ring eftouse is and not 
```

(The `step time` line changes from run to run and machine to machine: 53 ms here, 62 ms on a second run. Every other line was identical in three runs.) `real words in a 1,000-character sample` is a crude score (limit 3). The two `train / val` numbers at step 1499 and in `FINAL` are two separate estimates of the same model (limit 2).

**File 4 — `key.py`** (**TEACHER ONLY.** The counting baselines, the hand numbers for the activity and the workbook.) **Never show this to the student.**

```python
# key.py - Week 17 (TEACHER ONLY): what a model that just counts would score, and the hand numbers for the activity and the workbook.
import math
import numpy as np
from l4lib.corpus import TEXT

chars = sorted(set(TEXT))
V = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
ids = [stoi[c] for c in TEXT]
n = int(0.9 * len(ids))
train, val = ids[:n], ids[n:]

# ---- Three things a model could know, from the training text only. Scored as the average -ln(probability of the true next character).
print("knows nothing (uniform)      :", round(math.log(V), 3))

one = np.ones(V)                                         # add 1 to every count so nothing has probability 0
for c in train:
    one[c] += 1
p1 = one / one.sum()
print("knows letter frequencies     :", round(float(np.mean([-math.log(p1[c]) for c in val[1:]])), 3))

two = np.ones((V, V))                                    # two[a, b] = how often b followed a (+1)
for a, b in zip(train[:-1], train[1:]):
    two[a, b] += 1
p2 = two / two.sum(axis=1, keepdims=True)
print("knows the previous letter    :", round(float(np.mean([-math.log(p2[a, b]) for a, b in zip(val[:-1], val[1:])])), 3))
print("  ... the same counts, scored on the TRAINING text:", round(float(np.mean([-math.log(p2[a, b]) for a, b in zip(train[:-1], train[1:])])), 3))

# ---- The activity, "Beat the Ladder": six places in the text, the true next character, and what the previous-letter counts say.
print()
print(f"{'context (last 14 shown)':<24}{'true next':<11}{'p (counts)':<12}{'-ln p':<8}")
cards = ["the old man fed the b", "the baker made brea", "every mornin", "the birds sang over the r",
         "a question is a small do", "the fisherman sold f"]
scores = []
for text in cards:
    where = TEXT.index(text)
    true_next = TEXT[where + len(text)]
    p = p2[stoi[text[-1]], stoi[true_next]]
    scores.append(-math.log(p))
    shown, nxt = "|" + text[-14:] + "|", "|" + true_next + "|"
    print(f"{shown:<24}{nxt:<11}{p:<12.3f}{-math.log(p):<8.3f}")
print("mean -ln p over the six cards:", round(sum(scores) / len(scores), 3))

# ---- Workbook arithmetic
B, T, d, L = 32, 64, 128, 4
total = V * d + T * d + L * (12 * d * d + 10 * d) + 2 * d + d * V + V
print()
print("characters predicted per step    :", B * T)
print("characters predicted, 1500 steps:", 1500 * B * T)
print("passes over the training text    :", round(1500 * B * T / len(train), 1))
print("possible window starts           :", len(train) - T, "(train)  ", len(val) - T, "(val)")
print("knobs, by part                   :", {"tok": V * d, "pos": T * d, "blocks": L * (12 * d * d + 10 * d), "ln_f": 2 * d, "head": d * V + V})
print("knobs in total                   :", total)
print("knobs per training character     :", round(total / len(train), 1))
print("scores for one batch             :", B * T * V, "numbers, shape", (B, T, V))
print("-ln(0.5) =", round(-math.log(0.5), 3), "  -ln(0.25) =", round(-math.log(0.25), 3), "  -ln(1/28) =", round(math.log(28), 3))
print()
print("-ln p for p = 0.9, 0.5, 0.25, 0.1, 0.01:", [round(-math.log(p), 3) for p in (0.9, 0.5, 0.25, 0.1, 0.01)])
```

```text
knows nothing (uniform)      : 3.332
knows letter frequencies     : 2.855
knows the previous letter    : 2.033
  ... the same counts, scored on the TRAINING text: 2.045

context (last 14 shown) true next  p (counts)  -ln p   
| man fed the b|        |i|        0.098       2.325   
|aker made brea|        |d|        0.068       2.689   
|every mornin|          |g|        0.118       2.140   
|ang over the r|        |i|        0.109       2.216   
| is a small do|        |o|        0.050       3.004   
|sherman sold f|        |i|        0.229       1.473   
mean -ln p over the six cards: 2.308

characters predicted per step    : 2048
characters predicted, 1500 steps: 3072000
passes over the training text    : 489.6
possible window starts           : 6210 (train)   634 (val)
knobs, by part                   : {'tok': 3584, 'pos': 8192, 'blocks': 791552, 'ln_f': 256, 'head': 3612}
knobs in total                   : 807196
knobs per training character     : 128.7
scores for one batch             : 57344 numbers, shape (32, 64, 28)
-ln(0.5) = 0.693   -ln(0.25) = 1.386   -ln(1/28) = 3.332

-ln p for p = 0.9, 0.5, 0.25, 0.1, 0.01: [0.105, 0.693, 1.386, 2.303, 4.605]
```

- [ ] **Run the four files as a set** and check nothing fails: `for f in check_init train key; do python3 $f.py > /dev/null || echo FAIL $f; done`. It prints nothing and takes about 90 seconds.
- [ ] **Print** workbook pages 17.1-17.6 and the six **Beat the Ladder** cards (Activity). Each card is the text up to the hidden letter, as in the `key.py` table: `the old man fed the b`, `the baker made brea`, `every mornin`, `the birds sang over the r`, `a question is a small do`, `the fisherman sold f`. **The hidden letters go only on your answer sheet**: `i`, `d`, `g`, `i`, `o`, `i`.
- [ ] **Have the student's own `block.py` from Week 16 open**, so the `Block` is copied from their file, not from this guide.
- [ ] **Read the Debugging Clinic** and copy the eight `bad*.py` files to a scratch folder so they are ready to plant. (`bad1`, `bad2` and `bad3` take 6-17 seconds each because they train.)
- [ ] **Decide where the training run goes in the lesson.** The plan below starts it at about minute 44 and plays the Beat the Ladder activity while it runs.

### 3 minutes on the day

- [ ] Open `tinygpt.py` and `check_init.py` in the editor as **empty files**, for typing together. Open `train.py` with the loop **typed in advance** (the student types `get_batch`, `TinyGPT` and the check; the training loop is Week 1-6 code in a new place, see Live-Code).
- [ ] Put the six cards, the calculator and the timer on the desk. Laptop **plugged in** (on battery the step time can double).

### Fallback if the laptops fail

| Problem | What to do |
|---|---|
| `ModuleNotFoundError: l4lib` | You are in the wrong folder. Only `from l4lib.corpus import TEXT` needs it. If the folder really is missing, copy `l4lib/` from the course into the working folder (the text is 6,972 characters; retyping it is not an option). |
| `ModuleNotFoundError: torch` | `python3 -m pip` is blocked; use a machine that already has torch. Fall back to the paper half: the Beat the Ladder cards (Activity) and the knob count by part (page 17.3). |
| `train.py` takes over 4 minutes | The laptop is on battery or busy. **Set `STEPS, WARMUP = 600, 100`**: the run takes about 35 seconds (measured 53 ms per step here, 32 s total). It ends at train **1.757**, validation **1.800**, gap 0.043, **20%** real words. Tell the student it is a shorter run and expect a worse model and a smaller gap. The command we used, so you can reproduce it: `sed 's/STEPS, WARMUP = 1500, 100/STEPS, WARMUP = 600, 100/' train.py > train600.py`. |
| First loss not within 0.05 with `calm_head=True` | The `*= 0.1` line is not inside `if calm_head:`, or `d`, `V` or `T` differ from the ones in `check_init.py`. Print `V`. |
| `RuntimeError: a leaf Variable that requires grad is being used in an in-place operation` | The `with torch.no_grad():` around `self.head.weight *= 0.1` is missing. (We ran it: that is the real last line, from `l.weight *= 0.1` on a plain `nn.Linear`.) |
| Knob count not 807,196 | Compare the `tok / pos / blocks / ln_f / head` lines with the table in section 2(d). A `Block` with a bias on q, k, v adds 3 x 128 x 4 = 1,536; norms counted as `d` instead of `2d` lose 9 x 128 = 1,152. |
| Different random numbers or losses on another machine | Expected (different PyTorch builds). The story holds: the first loss near 3.33, validation above training by a growing amount. Nothing in the lesson depends on a particular digit. |
| No laptop at all | Run the lesson from this guide's printed outputs: the Beat the Ladder cards, the knob count by part, and the ordering of the three samples (Activity 2). |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | What happens |
|---|:--:|---|
| 🪝 Hook | 8 | What should a model that knows nothing score? `ln 28`. Guess the next letter of a real sentence. |
| 🧠 Concept | 12 | One step = 2,048 questions; `x` and `y`; the parts of the GPT drawn; a module inside a module; train vs validation |
| 💻 Live-code | 25 | `tinygpt.py` (type `TinyGPT`), `check_init.py` (data, `get_batch`, the two checks, the size), then start `train.py` |
| 🎲 Their turn | 20 | While it trains: **Beat the Ladder** on paper. Then read the run: step time, order the three samples, train vs validation |
| 🔑 Wrap & assign | 5 | What was shown and what wasn't; what the gap means; homework |

### 🪝 Hook — What Does a Model That Knows Nothing Score? (8 minutes)

**Do not open the laptop yet.**

1. **(2 min) Recall.** *"In Week 1 a model that was just guessing between two classes scored 0.693. Why that number?"* (`ln 2`: it gives each class half, `-ln(0.5)`.) *"Now the model is choosing one of 28 characters. If it knows nothing, what does it score?"* Let them answer `ln 28`, or guess and then compute it on the calculator: **3.332**. Write it on the board: **"knows nothing = 3.332"**.
2. **(3 min) A real guess.** Put the first card on the board: `the old man fed the b_`. *"Write down your three best guesses for the next character and how sure you are of each. They must add up to 1 or less."* Reveal `i`. Score it (`-ln` of the probability they gave to `i`). Do **one** card and keep the other five for later. (The card doubles as the demonstration of the scoring in the activity.)
3. **(3 min) The frame.** *"We will build a model that plays exactly this game, 2,048 times per step, and we will not trust it until two numbers check out. One is how many knobs it has. The other is what it scores before it has learned anything. It should be close to the number on the board."* Write: **"a check, not a hope"**.

### 🧠 Concept — One Step, Four Pieces, One Gap (12 minutes)

**(4 min) One step is 2,048 questions.** Write a short sentence and show the cut:

```text
text : t h e _ c a t _ s a t
x    : t h e _ c a t _ s a        (the window)
y    :   h e _ c a t _ s a t      (the same window, moved one place left)
```

*"Place 1 of `x` is `t`; the right answer, place 1 of `y`, is `h`. Place 2 sees `t h` and must say `e`. Every place in the window is one question, and the mask (Week 15) stops any place from peeking at the answer. So **one pass asks all 64 questions at once**, and a batch of 32 windows asks 2,048."* Tie to Week 12: *"training feeds the true text and runs in parallel; writing feeds back its own guesses one at a time."* (`generate` is the second.)

**(3 min) The parts, in order.** Draw the stack top to bottom:

```text
   characters (ids, shape (B, T))
        |
   character table  +  place table (torch.arange(T))      <- Week 16
        |
   Block  Block  Block  Block                              <- Week 16's block, four times
        |
   final layer norm
        |
   output layer: d numbers -> 28 scores                    <- one score per character
        |
   softmax -> probabilities   /   cross-entropy with y -> the loss
```

*"Everything in this picture you met last week except the last two boxes, and you met those in Week 12."* Say the **decoder-only** word once (*"only the left-to-right half; there is no second half"*) and move on.

**(2 min) A module inside a module.** *"Last week's Block held layers. Today's TinyGPT holds Blocks. PyTorch sees it as a tree, and `model.parameters()` walks the whole tree. That is why one optimizer can train all 807,196 knobs."* Ask: *"last week you predicted the number of knobs. What was it?"* (807,196.) *"We will see whether the machine agrees."*

**(3 min) Two losses.** *"We cut off the last tenth of the text, 698 characters, and never train on it. We call its loss the validation loss. The training loss is on the text the model is trained on. If the model is learning something general, both go down. If it is memorising, only the training loss does. Predict: at the end, will the two be about the same, or not?"* Collect guesses. **Do not reveal.**

### 💻 Live-Code Together — `tinygpt.py`, `check_init.py`, then start `train.py` (25 minutes)

The student types. You narrate. **Nobody pastes, except the `Block`, which comes from the student's own `block.py` from last week.**

**Step 1 (9 min) — `tinygpt.py`.** Copy `Block` from `block.py`. **Type `TinyGPT`** line by line. Pause at:

- `super().__init__()`: *"first line, always."* Ask what would happen if it were missing (Clinic 8 shows it; do not run it now).
- `self.blocks = nn.ModuleList([Block(d, H, T) for _ in range(L)])`: *"this is the module inside a module. Why `ModuleList` and not a list?"* (Week 16, Clinic 1-2: a list is invisible.)
- `forward`: `self.tok(idx) + self.pos(torch.arange(T))` is last week's "word row plus place row". Then the loop over blocks, then `ln_f` and `head`.
- The `logits.reshape(B * T, -1)` line: *"`cross_entropy` wants a list of rows: 2,048 rows of 28 scores, and 2,048 right answers."*
- `generate`: **show the `@torch.no_grad()` line and say it as a label**: *"no learning in here"*. Point out `idx[:, -self.T:]` (only the last 64 characters: the place table has 64 rows) and `logits[:, -1, :]` (only the last place's scores).
- `calm_head`: say **"we will add this after the check tells us why; ignore it until then"** and type the two lines.

**Step 2 (10 min) — `check_init.py`.** The student types the data lines (they know `stoi`), then `get_batch`, with the `torch.randint(len(src) - T, (B,))` line. **Predict before running:** *"what are the shapes of `x` and `y`? What is the first row of `y` compared with the first row of `x`?"* Run only up to the `y is x moved one place left` line (comment the rest out) and read the two strings aloud. Then type the check loop. **Predict:** *"how far from 3.332 will the first loss be?"* Run. `FAIL` for `calm_head=False` (3.5025), `PASS` for `True` (3.3481). Ask: *"Is the un-calmed model broken?"* (No, just over-confident at the start: its output layer's default weights are large. Multiplying them by 0.1 pulls the first loss onto `ln 28`.) Then the size lines: `match: True`. *"Last week's hand count was right."*

**Step 3 (6 min) — start `train.py`.** (A **checkpoint** is a moment in the run where we stop and look: here steps 0, 300 and 1,499. Say the word when you reach `CHECKPOINTS`.) The student types `get_batch` again (copy from `check_init.py`; say it belongs in a shared file one day), `estimate` with its `@torch.no_grad()`, the `sample` helper and the loop. The loop is **their own Week 1-6 loop** in a new place (AdamW, warm-up and cosine, clipping): do not re-teach it. Point at `spent += time.perf_counter() - t0`: *"we time only the step itself, not the evaluation, so the number means one training step."* **Before pressing Enter:** *"Predict the time per step."* (Let them guess in milliseconds. Ours: 53.) Press Enter.

### 🎲 Their Turn — Beat the Ladder, and Read the Run (20 minutes)

The run takes about 85 seconds, so the first activity happens **while it runs**. Full rules in *The Activity, In Full*. The shape:

1. **(10 min) Beat the Ladder.** Cards 2-6 (card 1 was the hook). For each: three guesses with probabilities, reveal the letter, score `-ln p`, average the six. Compare with the rungs on the board (3.332, 2.855, 2.033). The run finishes about a minute and a half in; do not stop for it.
2. **(2 min) Read the run.** Read the step time aloud. Compare with the guess.
3. **(5 min) Order the checkpoints.** Three samples printed on cards, shuffled and labelled A-C. The student puts them in order of training and writes one piece of evidence for each.
4. **(3 min) The gap.** *"What were the two final numbers? Which do you believe about how it would do on a new paragraph?"* (Validation.) *"What is the gap?"* (0.54.) Pull the intermediate table from `train.py`: *"it was 0.02 at step 300. What changed?"*

**Stop at 20 minutes.** If Beat the Ladder has not finished, score three cards and move on.

### 🔑 Wrap & Assign (5 minutes)

1. **(2 min)** *"Three things we did. One: we built a GPT out of last week's parts and checked its size and its first loss before training. Two: we trained it and watched it go from random characters to the shape of sentences. Three: we found that it does much better on the text it trained on than on text it had not seen. What did we **not** do?"* (Find out why; test anything about understanding; try any other seed, dropout or more text.)
2. **(1 min)** *"What does the gap mean?"* (Two sentences, below.) *"What does it not mean?"* (That the model is bad, or that it will fail on everything new. It means the training number is not the honest one.)
3. **(1 min)** Hand out the workbook.
4. **(1 min)** One sentence ahead: *"Next week is the paper review of Weeks 9-17, and the week after we break this model on purpose, one part at a time, and measure what each part was worth."*

---

## 🐞 The Debugging Clinic

Every error below was produced by running the code. **Paths will differ on your machine**; here they are shown as `/home/you/l4/`. Tracebacks from PyTorch run through several of its own files; the long middle of those is replaced by a line reading `... frames inside torch (elided) ...`, and **the last line is the real, complete last line**. Each mistake is deliberate: you plant it, the student reads the traceback (or the odd number) aloud, and you refuse to fix it until they have said what it means. Each block is **self-contained** (it imports the finished `tinygpt.py`) so you can drop it in a scratch folder. **Four of the eight are silent or quiet**, and the quiet ones are the point.

### How to teach debugging without giving the answer

1. *"Read me the last line."* (It says what went wrong; the lines above say where.) For a silent mistake: *"What did you expect this to print?"*
2. *"Which of your files is on the line above it?"*
3. *"What did you expect that line to do?"*
4. Only then: *"What is different?"*

### Mistake 1 — the output layer left at its default size (QUIET: the check fails, the model is fine)

```python
# DELIBERATE MISTAKE 1: the output layer left at its default size. The first-loss check fails. Is the model broken?
import math
import torch
from tinygpt import TinyGPT
from l4lib.corpus import TEXT

chars = sorted(set(TEXT))
V = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in TEXT])
train_data = data[:int(0.9 * len(data))]
d, H, L, T, B = 128, 4, 4, 64, 32


def get_batch():
    starts = torch.randint(len(train_data) - T, (B,))
    x = torch.stack([train_data[s:s + T] for s in starts])
    y = torch.stack([train_data[s + 1:s + T + 1] for s in starts])
    return x, y


for calm in (False, True):
    torch.manual_seed(0)
    model = TinyGPT(V, d, H, L, T, calm_head=calm)            # <- calm_head=False is the mistake
    opt = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.1)
    seen = []
    for step in range(150):
        x, y = get_batch()
        _, loss = model(x, y)
        if step in (0, 49, 149):
            seen.append(round(loss.item(), 3))
        opt.zero_grad()
        loss.backward()
        opt.step()
    print(f"calm_head={calm}: ln(V) = {math.log(V):.3f}; loss at steps 0, 49, 149 =", seen)
```

```text
calm_head=False: ln(V) = 3.332; loss at steps 0, 49, 149 = [3.497, 2.183, 1.993]
calm_head=True: ln(V) = 3.332; loss at steps 0, 49, 149 = [3.347, 2.525, 2.086]
```

**Read it:** at step 0 the un-calmed model scores **3.497**, 0.165 above `ln(28) = 3.332`, and the calmed one **3.347**. Both train. At steps 49 and 149 the un-calmed model is **ahead** (2.183 against 2.525, then 1.993 against 2.086). *So what was the check for?* It gave the student a number to compare with, and a size: 0.17 is a mild over-confidence; a first loss of 20 would mean a bug. **What the check does not say** is which model is better at step 1,500; we did not run it. Keep the student from concluding either "the check is pointless" or "the calm head is better". The honest line: *"a failed check is a question, not a verdict."*

### Mistake 2 — `y` not moved one place (SILENT, and the first-loss check cannot catch it)

```python
# DELIBERATE MISTAKE 2 (SILENT): the targets are NOT moved one place. y is the same window as x.
# The first-loss check still passes. Watch the training loss, then score it on honest targets, then sample.
import math
import torch
from tinygpt import TinyGPT
from l4lib.corpus import TEXT

chars = sorted(set(TEXT))
V = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for i, c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in TEXT])
n = int(0.9 * len(data))
train_data, val_data = data[:n], data[n:]
d, H, L, T, B = 128, 4, 4, 64, 32


def get_batch(src, shift):
    starts = torch.randint(len(src) - T, (B,))
    x = torch.stack([src[s:s + T] for s in starts])
    y = torch.stack([src[s + shift:s + T + shift] for s in starts])          # <- shift should be 1
    return x, y


torch.manual_seed(0)
model = TinyGPT(V, d, H, L, T)
opt = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.1)
for step in range(200):
    x, y = get_batch(train_data, shift=0)
    _, loss = model(x, y)
    if step in (0, 49, 99, 199):
        print(f"step {step:3d}  train loss {loss.item():.4f}")
    opt.zero_grad()
    loss.backward()
    opt.step()

with torch.no_grad():
    x, y = get_batch(val_data, shift=1)                   # honest targets: the NEXT character
    print(f"loss on the honest next-character task: {model(x, y)[1].item():.3f}   (ln V = {math.log(V):.3f})")
    out = model.generate(torch.tensor([[stoi['t']]]), 60)[0].tolist()
print("".join(itos[i] for i in out))
```

```text
step   0  train loss 3.3476
step  49  train loss 1.4752
step  99  train loss 0.4462
step 199  train loss 0.0927
loss on the honest next-character task: 5.696   (ln V = 3.332)
tttttttuuaq..iiiiiiiiiiiiiiiiiiiiiiirrrrrbbeebbbbbb..........
```

**Read it:** the first loss is **3.3476**, a clean `PASS`-sized number (the check does not look at `y`). Then the training loss falls to **0.0927** in 200 steps, far faster than the real run (1.47 at step 49 here against 1.96 at step 250 in the real run). On the honest next-character task the model scores **5.696**, worse than knowing nothing (3.332), and its sample is `ttttttt...iiiii`: it learned to repeat the character it was given. The answer is in the window itself: `y` **is** the character the place already sees (through the mask, a place sees its own character), so copying is a perfect strategy. **Fix:** `src[s + 1:s + T + 1]`, and `check_init.py` already prints `y is x moved one place left: True`. **The signal is a training loss that falls much too fast.** (Which is why the lab checks `y` on real text before training.)

### Mistake 3 — the blocks kept in a plain list (SILENT)

```python
# DELIBERATE MISTAKE 3 (SILENT): the blocks kept in a plain Python list inside the GPT.
# It runs and the loss even falls. Count the knobs, and ask whether the blocks learned.
import torch
import torch.nn as nn
import torch.nn.functional as F
from tinygpt import Block
from l4lib.corpus import TEXT

chars = sorted(set(TEXT))
V = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in TEXT])
train_data = data[:int(0.9 * len(data))]
d, H, L, T, B = 128, 4, 4, 64, 32


class ListGPT(nn.Module):
    def __init__(self):
        super().__init__()
        self.tok = nn.Embedding(V, d)
        self.pos = nn.Embedding(T, d)
        self.blocks = [Block(d, H, T) for _ in range(L)]      # <- should be nn.ModuleList([...])
        self.ln_f = nn.LayerNorm(d)
        self.head = nn.Linear(d, V)

    def forward(self, idx, targets):
        x = self.tok(idx) + self.pos(torch.arange(idx.shape[1]))
        for blk in self.blocks:
            x = blk(x)
        logits = self.head(self.ln_f(x))
        return F.cross_entropy(logits.reshape(-1, V), targets.reshape(-1))


torch.manual_seed(0)
model = ListGPT()
print("knobs:", sum(p.numel() for p in model.parameters()), "  (the real model has 807196)")
before = model.blocks[0].q.weight.sum().item()
opt = torch.optim.AdamW(model.parameters(), lr=3e-4)
for step in range(100):
    starts = torch.randint(len(train_data) - T, (B,))
    x = torch.stack([train_data[s:s + T] for s in starts])
    y = torch.stack([train_data[s + 1:s + T + 1] for s in starts])
    loss = model(x, y)
    if step in (0, 99):
        print(f"step {step:3d}  loss {loss.item():.3f}")
    opt.zero_grad()
    loss.backward()
    opt.step()
after = model.blocks[0].q.weight.sum().item()
print("sum of block 0's q weights, before and after 100 steps:", round(before, 6), round(after, 6))
```

```text
knobs: 15644   (the real model has 807196)
step   0  loss 3.497
step  99  loss 2.686
sum of block 0's q weights, before and after 100 steps: 13.310827 13.310827
```

**Read it:** **15,644** knobs instead of **807,196**, the loss falls from 3.497 to 2.686 anyway (the embeddings, the last norm and the output layer are learning), and the sum of block 0's `q` weights is **13.310827 before and after** training: the four blocks never moved from their random start. This is Week 16's Clinic 2, now one level up, in the GPT. **The signal is the knob count** (`15644` against the `807196` the student predicted), which is exactly why we count before we train. **Fix:** `self.blocks = nn.ModuleList([...])`. The real model is about 52 times bigger than the one that trained (807,196 / 15,644); a student who does not count would not notice.

### Mistake 4 — a window start that is one too big (loud, and rare)

```python
# DELIBERATE MISTAKE 4: a window start that is one too big. Most batches are fine; a rare one is not.
import torch
from l4lib.corpus import TEXT

chars = sorted(set(TEXT))
stoi = {c: i for i, c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in TEXT])
val_data = data[int(0.9 * len(data)):]                     # only 698 characters
T, B = 64, 32
torch.manual_seed(0)

for call in range(1, 1001):
    starts = torch.randint(len(val_data) - T + 1, (B,))    # <- one too many: should be len(val_data) - T
    x = torch.stack([val_data[s:s + T] for s in starts])
    y = torch.stack([val_data[s + 1:s + T + 1] for s in starts])
    if call % 10 == 0:
        print("batch", call, "fine")
```

```text
batch 10 fine
batch 20 fine
batch 30 fine
batch 40 fine
Traceback (most recent call last):
  File "/home/you/l4/bad4.py", line 15, in <module>
    y = torch.stack([val_data[s + 1:s + T + 1] for s in starts])
RuntimeError: stack expects each tensor to be equal size, but got [64] at entry 0 and [63] at entry 5
```

**Read it:** forty batches went by fine. In one of the next ten, the random start was the very last one that `randint` could now produce, `len(val_data) - T`, so the `y` window ran off the end of the text and came out **63** long, and `torch.stack` refused to put a 63 beside 64s. **It was a rare draw.** On 698 characters the chance per batch of 32 windows is about 5% (32 / 635), so it fell in the first 50. On the 6,274-character training text it is about 0.5% per batch (32 / 6,211), which is roughly one batch in 190: a real run would very probably die within its first few hundred steps (arithmetic; we did not run that version). The lesson: *an off-by-one in random code is a bug that depends on the seed*. **Fix:** `torch.randint(len(val_data) - T, (B,))`.

### Mistake 5 — `generate` without `@torch.no_grad()` (SILENT, and here it costs very little)

```python
# DELIBERATE MISTAKE 5 (SILENT, costs time): generate() written without @torch.no_grad().
# Same characters come out; count what it cost.
import time
import torch
import torch.nn.functional as F
from tinygpt import TinyGPT

torch.manual_seed(0)
model = TinyGPT(28, 128, 4, 4, 64)


def generate_slow(model, idx, n_new):                      # <- no decorator
    for _ in range(n_new):
        logits, _ = model(idx[:, -model.T:])
        probs = F.softmax(logits[:, -1, :], dim=-1)
        idx = torch.cat([idx, torch.multinomial(probs, 1)], dim=1)
    return idx


start = torch.tensor([[0]])
torch.manual_seed(1)
t0 = time.perf_counter()
a = generate_slow(model, start, 200)
slow = time.perf_counter() - t0
torch.manual_seed(1)
t0 = time.perf_counter()
b = model.generate(start, 200)                             # the real one, with the decorator
fast = time.perf_counter() - t0
print("same characters:", bool((a == b).all()))
print(f"without no_grad {slow:.2f} s   with no_grad {fast:.2f} s   ({slow / fast:.1f} times as long)")
print("a step's scores track gradients?", model(start)[0].requires_grad, "  inside no_grad:", end=" ")
with torch.no_grad():
    print(model(start)[0].requires_grad)
```

```text
same characters: True
without no_grad 0.16 s   with no_grad 0.14 s   (1.1 times as long)
a step's scores track gradients? True   inside no_grad: False
```

**Read it:** the characters are the same (`True`); the difference in time is **small** (the two printed times are within about 15% of each other; your numbers will vary and may even reverse), and `requires_grad` is `True` outside `no_grad` and `False` inside. **Be honest with the student: on this CPU, at this size, forgetting it costs almost nothing you can see.** What the decorator says is *intent* ("no learning here") and it stops PyTorch keeping the bookkeeping for a backward pass that will never come; the saving is in memory, and **we did not measure memory**. Do not invent a speed-up for it. (Level 3 Week 20's `.item()` lesson is the related trap: keep a loss tensor in a list and the graphs are kept with it.)

### Mistake 6 — generate forgets to keep the last `T` characters (loud, at character 65)

```python
# DELIBERATE MISTAKE 6: generate() that forgets to keep only the last T characters. It dies at character 65.
import torch
import torch.nn.functional as F
from tinygpt import TinyGPT

torch.manual_seed(0)
model = TinyGPT(28, 128, 4, 4, 64)


@torch.no_grad()
def generate_long(model, idx, n_new):
    for i in range(n_new):
        logits, _ = model(idx)                             # <- should be idx[:, -model.T:]
        probs = F.softmax(logits[:, -1, :], dim=-1)
        idx = torch.cat([idx, torch.multinomial(probs, 1)], dim=1)
        if idx.shape[1] in (63, 64, 65):
            print("length now", idx.shape[1])
    return idx


generate_long(model, torch.tensor([[0]]), 100)
```

```text
length now 63
length now 64
length now 65
Traceback (most recent call last):
  File "/home/you/l4/bad6.py", line 21, in <module>
    generate_long(model, torch.tensor([[0]]), 100)
  ... frames inside torch (elided) ...
  File "/home/you/l4/bad6.py", line 13, in generate_long
    logits, _ = model(idx)                             # <- should be idx[:, -model.T:]
  ... frames inside torch (elided) ...
  File "/home/you/l4/tinygpt.py", line 57, in forward
    x = self.tok(idx) + self.pos(torch.arange(T))
  ... frames inside torch (elided) ...
IndexError: index out of range in self
```

**Read it:** the lengths printed are 63, 64, 65. At length 65 the model is asked for places `0..64`, but the place table has **64 rows** (`0..63`), so `self.pos(...)` fails with `IndexError: index out of range in self`. The last line names the problem; the line above it (in `tinygpt.py`) says *where*: the place lookup. **Fix:** `model(idx[:, -model.T:])`, the last 64 characters only. This is the context length (Week 16's Clinic 4, now reachable by a long generation). It is also why a model trained on windows of 64 **cannot continue longer prompts with full memory**: it only ever sees the last 64 characters.

### Mistake 7 — `cross_entropy` on the un-flattened scores (loud)

```python
# DELIBERATE MISTAKE 7: cross_entropy handed the (B, T, V) scores and the (B, T) targets without flattening.
import torch
import torch.nn.functional as F
from tinygpt import TinyGPT

torch.manual_seed(0)
model = TinyGPT(28, 128, 4, 4, 64)
x = torch.randint(28, (32, 64))
y = torch.randint(28, (32, 64))
logits, _ = model(x)
print("scores:", tuple(logits.shape), " targets:", tuple(y.shape))
loss = F.cross_entropy(logits, y)                          # <- needs logits.reshape(B * T, -1) and y.reshape(B * T)
```

```text
scores: (32, 64, 28)  targets: (32, 64)
Traceback (most recent call last):
  File "/home/you/l4/bad7.py", line 12, in <module>
    loss = F.cross_entropy(logits, y)                          # <- needs logits.reshape(B * T, -1) and y.reshape(B * T)
  ... frames inside torch (elided) ...
RuntimeError: Expected target size [32, 28], got [32, 64]
```

**Read it:** the scores are `(32, 64, 28)` and the targets `(32, 64)`. `F.cross_entropy` reads a 3-axis input as *(batch, classes, extra)*, so it took the 64 to be the number of classes, and expected targets of shape `(32, 28)`. The message gives both shapes. **Fix:** `logits.reshape(B * T, -1)` and `targets.reshape(B * T)`: 2,048 rows of 28 scores and 2,048 answers. *The habit:* print `logits.shape` next to the target's.

### Mistake 8 — `super().__init__()` forgotten (loud)

```python
# DELIBERATE MISTAKE 8: a model that holds Blocks, with the super().__init__() line forgotten.
import torch.nn as nn
from tinygpt import Block


class Mini(nn.Module):
    def __init__(self):
        # super().__init__()                               # <- forgotten
        self.tok = nn.Embedding(28, 8)
        self.block = Block(8, 2, 6)


model = Mini()
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad8.py", line 13, in <module>
    model = Mini()
  File "/home/you/l4/bad8.py", line 9, in __init__
    self.tok = nn.Embedding(28, 8)
  ... frames inside torch (elided) ...
AttributeError: cannot assign module before Module.__init__() call
```

**Read it:** assigning a layer (`self.tok = nn.Embedding(...)`) needs PyTorch's bookkeeping, which `super().__init__()` sets up. Without it the very first assigned module raises `AttributeError: cannot assign module before Module.__init__() call`. The traceback points at the line **after** the missing one (the comment line is not code). **Fix:** uncomment it. In a nested module this is the line students forget most, because there are now two classes with an `__init__` in the file.

---

## 🎲 The Activity, In Full

### Beat the Ladder (and Order the Checkpoints)

**What it is:** the student plays the game the model plays, on six real places in the text, and scores themselves with the same loss. Their average goes on the same ladder as the counting models and the TinyGPT. Then they read the trained model's three checkpoint samples and put them in order.

### Setup (2 minutes, during the live-code segment)

- Six cards (the Prep Checklist lists them), **the hidden letter on your sheet only**.
- A strip with the rule: *"Write up to three letters and how sure you are of each (the numbers must add up to 1 or less). Everything you do not list shares what is left equally (the left-over probability divided by the number of letters you did not list; with three letters listed that is 25). Score = `-ln` of the share on the true letter."* A calculator with `ln`. Also the small table from `key.py`: `p = 0.9 -> 0.105`, `0.5 -> 0.693`, `0.25 -> 1.386`, `0.1 -> 2.303`, `0.01 -> 4.605`.
- The ladder on the board: **knows nothing 3.332 · letter frequencies 2.855 · previous letter 2.033**, and an empty rung for TinyGPT.
- For part 2, after the run: the three samples copied onto cards, **shuffled** and labelled A, B, C (write down which is which on your own sheet).

### The rules, read out loud before round one

1. The **reader** (you) reads the card, with the last letter hidden.
2. The **player** (the student) writes up to three letters and probabilities. **Guessing a probability of 0 for anything is not allowed**: *"nothing is impossible to a model that has never read the rest"*.
3. Reveal, score, write the `-ln p` in the last column.
4. After six, average. **Six cards is a small sample:** one bad card moves the average a lot.

### The six cards

| Card | Context (last letters) | True next | Previous-letter counts give | `-ln p` of counts |
|:--:|---|:--:|:--:|:--:|
| 1 | ` man fed the b` | `i` | 0.098 | 2.325 |
| 2 | `aker made brea` | `d` | 0.068 | 2.689 |
| 3 | `every mornin` | `g` | 0.118 | 2.140 |
| 4 | `ang over the r` | `i` | 0.109 | 2.216 |
| 5 | ` is a small do` | `o` | 0.050 | 3.004 |
| 6 | `sherman sold f` | `i` | 0.229 | 1.473 |
| | **mean over the six** | | | **2.308** |

(From `key.py`. The counts see **one** letter; the player sees the whole sentence. That is the point of the activity.)

### The question that makes the activity

*"Card 2 is `brea_`. The counts, which see only the `a`, gave the right letter 0.068. What did you give it? Why could you give more?"* (A person sees `brea` and the whole phrase. The counts see one letter. A model with a context of 64 places sees up to 64.) Then: *"Which card was hardest? What did you give the true letter? Could anybody have known?"* (Card 5: `do` -> `o` as in `door` but also `done`, `dog`.) And the humility half: *"Your average on six cards is one sample. Would the ladder put you above the counting models with six more?"* (Unknown; say so.)

### Part 2 — Order the Checkpoints

The student puts A, B, C in order of training and writes **one piece of evidence per card**, for example: *step 0: no spaces in the right places, `.` and letters at random; step 300: lots of `the`, `and`, `an`, but words run together, no sentence shape; step 1499: lines, full stops, mostly real words.* Then give the measured share of real words (0%, 17%, 60%) and ask what that number can and cannot tell them (limit 3: it counts copied words and says nothing about meaning).

### What "finished" looks like

Six scored cards, an average on the ladder, three samples in the right order with evidence, and the student saying both numbers of the final line in words: *"on text it trained on, 0.9; on text it did not, 1.4."*

### Variation — easier

Three cards only (cards 1, 3, 6), one guess each (the single best letter and how sure), and order just the first and last samples.

### Variation — harder

Give the student a **new line of the text they have not seen**, hide ten letters one at a time, score their guesses, and compare the average with the model's validation loss, **1.44**. *(The weights are not saved, so the model cannot be asked about these ten places; the comparison is to its average only. This guide did not score a human on ten places; let the student report what they get.)* Or ask them to find the two samples' words that appear in the training text and the words that do not, and count.

---

## ❓ Questions Students Ask This Week

**"Why does the first loss have to be 3.332?"** It does not have to be *exactly*; it should be close. If the model knows nothing it gives each of 28 characters a 1/28 share, and `-ln(1/28) = 3.332`. If the first loss is much higher, the model starts out confidently wrong (or has a bug);

**"Why multiply the output layer by 0.1?"** Its default weights give scores with a wide spread, which makes the first loss 3.50. Scaling it down makes the scores start near zero, so all 28 characters start nearly equal. The reference module gets there with a different trick (a small normal initialisation everywhere). Both are conventions. We did not test which trains better over 1,500 steps.

**"Why 128 wide, 4 heads, 4 blocks, 64 places?"** They are the reference module's size, chosen so that the model trains in a minute and a half on a CPU. Week 16's count gives 807,196 for exactly those numbers. We did not test other sizes this week; Week 21 does.

**"Why characters and not words?"** Because a character vocabulary is 28 numbers, small enough to type and to count by hand. The cost is that the model must learn to spell. Week 20 replaces characters with pieces.

**"Why is the validation set only 698 characters?"** It is the last tenth of a 6,972-character text. That is small, and the number is noisy (limit 2). A bigger text would give a steadier number; this course does not have one offline.

**"Why `torch.randint` and not going through the text in order?"** Random windows make every batch different and cover the text unevenly in a way that averages out. We did not compare the two. (Going in order is also fine; it is a design choice we did not test.)

**"Why do the step 0 samples and the step 1499 samples come from the same prompt `t`?"** So the three are comparable: same start, different amounts of training. The sampling temperature is 0.8 (Week 13: a little sharper than 1). We did not vary it today.

**"Why is 1,499 and not 1,500 the last checkpoint?"** The loop counts from 0, so the last step is 1,499. It is the same thing as the `range` from Week 1.

**"The `step 1499` line says 0.894 and FINAL says 0.907. Which is right?"** Both are estimates of the same thing from different random windows (20 batches of 32). Their difference, 0.013, is a measure of the noise. Do not read anything into differences that size.

**"Why does the validation loss go up at the end?"** By a tiny amount (1.417 at step 1000, 1.447 at the end). One reading is that the model keeps fitting the training text at the expense of the rest. The rise is of the same size as the noise in the estimate, and we did not repeat the run with other seeds, so we do not claim it from this run. The ledger's longer run (2,500 steps, with dropout) shows a clearer rise.

**"Why didn't you use dropout?"** The reference module has `Dropout(0.1)`. We left it out so that the block is exactly Week 16's. It is a sensible next experiment: train with it and see whether the gap shrinks. We did not run it.

**"Can I make it write something useful?"** It writes a few sentences in the style of a 6,972-character text; there is nothing else in it. To make it talk about something new you would have to train it on text about something new.

**"Is this a 'small language model'?"** It is a very small one. The word *language* is generous for a model whose entire world is 6,972 characters.

**"How many knobs does GPT-whatever have?"** Not something we measured, so we do not quote a figure. The fair statement is "many orders of magnitude more than 807,196", which is background, not a claim from this course.

**"Will my numbers match yours?"** The knob count, the vocabulary size, the window shapes and `ln 28` are exact. Losses and samples come from `torch.manual_seed(0)` and matched on repeat on the same machine; another PyTorch build may give different digits. The step time will differ.

---

## ⚠️ Where This Lesson Goes Wrong

1. **The student skips the checks and starts the run.** They lose the lesson. Do not press Enter on `train.py` until `match: True` and the first loss have been printed and discussed.
2. **The student treats `FAIL` as "broken".** Clinic 1. The first loss of the un-calmed model is 0.17 above `ln(28)`, and the model trains fine.
3. **The run looks "stuck" for the first second.** `train.py` prints the step 0 sample only after it has estimated two losses (40 forward passes). It is not stuck. The next line appears at step 250 (about 15 seconds).
4. **The student reads the samples as understanding.** Return to limits 3 and the "real words" score, and to the words that are not words (`menthy`, `boird`).
5. **`y` built without the shift** (Mistake 2). It is silent; the training loss falls too fast. Ask: *"faster than it should?"*
6. **Beat the Ladder becomes a competition with the model.** It is a measuring stick, six cards, one sample. Say so.
7. **The gap is explained with a story that was not tested.** Keep to "consistent with memorising", which the intermediate table supports (the gap starts at about 0 and grows at every checkpoint), and "we did not run the control".
8. **Students compare their validation loss with the ledger's 1.669.** The setups differ (dropout, seed, 2,500 steps). They are to compare *directions*, not digits.
9. **The run time hits the lesson.** If `train.py` has not finished when Beat the Ladder ends, do the ordering with the step 0 and step 300 samples and let the final one arrive while you wrap up.

---

## 🧭 Differentiation

### If the student is struggling

- Drop the nested-module explanation to one sentence (*"the model holds four Blocks"*) and let `check_init.py`'s `match: True` carry the lesson. Do **three** Beat the Ladder cards.
- Skip typing `generate` and `estimate`: give them, and have the student type `tinygpt.py`'s `__init__` and `forward` only. The checks and the run are the same.
- For the gap, use only the end numbers: *"0.9 on the text it studied, 1.4 on the text it didn't. Which would you trust to tell you how it will do on a new page?"*

### If the student is flying

- Run **Mistake 2** (`y` unshifted) *before* telling them what is wrong, and ask them to find it from the output alone: a loss that falls too fast, a sample `ttttt`.
- Ask them to **predict, and then run**, three changes to the run: `weight_decay=0.0`, a `STEPS` of 600 (we ran this one: train 1.757 / val 1.800, 20% real words), and a `d = 64, L = 2` model (the module's fallback; we did not run it; measure and report). **Report what they measure. We did not run most of these; do not quote numbers for them.**
- Ask how many knobs the model would have at `d = 64, L = 2`, by the formula of Week 16: `28 x 64 + 64 x 64 + 2 x (12 x 64^2 + 10 x 64) + 2 x 64 + (64 x 28 + 28) =` **107,420** (checked by building the model at that size with `T = 64`).
- Have them add `nn.Dropout(0.1)` to the Block after each sub-layer, retrain, and report whether the gap shrinks. **Not run by us.**

### If the student won't engage today

Play Beat the Ladder with **their own** sentences: each writes a sentence from the corpus with the last letter missing, the other guesses. The game is the lesson. Then run `check_init.py` only and read the four lines at the bottom together.

---

## ✅ Assessing Understanding

Five questions, orally, during the activity. Not graded; they inform the mastery scale.

1. **"What is the first loss of a model that knows nothing, and why?"** *Pass:* `ln 28 = 3.33`, because every one of the 28 characters gets a 1/28 share and the loss is `-ln` of the share on the right one.
2. **"What is `y`?"** *Pass:* `x` moved one place left: for each place, the character that comes next.
3. **"Why `nn.ModuleList`?"** *Pass:* so PyTorch can see the blocks inside, so their knobs are counted and trained; a list hides them (and the model still runs).
4. **"The training loss is 0.9 and the validation loss 1.4. What do you believe, and why?"** *Pass:* the validation number is the fair one; the model saw the training text; the gap is what memorising looks like (and we did not prove that was the cause).
5. **"Does the model understand the text?"** *Pass:* no; it has learned which characters tend to follow which prefixes in 6,972 characters; its words are mostly real words copied from the training text, plus near-misses.

### Mastery scale for this week

| Level | What you see |
|---|---|
| **4 — Fluent** | Writes `TinyGPT` with little help; predicts the parts count (807,196) and reads a failed check as a question; explains the gap and names what was not tested; catches a `y` with no shift from the loss curve alone. |
| **3 — Secure** | Types the model with prompts; gets the first loss and the knob count to agree with the prediction; reports step time, three samples and the two losses correctly; says the gap means "it does better on the text it saw". |
| **2 — Developing** | Runs it and reports the numbers; cannot say why `y` is shifted or what the gap means beyond "one is bigger"; needs the check explained. |
| **1 — Not yet** | Cannot say what one training step asks. Repeat the three-row `x` / `y` / text picture at the start of Week 18 before the review. |

---

## 📤 Homework to Assign

The workbook has six pages (17.1-17.6). The student does them in order, and writes **predictions before running anything**.

1. **17.1 Windows and the shift** — on a 12-character string, write `x` and `y` for two starts by hand, count the questions in a batch, and check with `check_init.py`'s `get_batch`.
2. **17.2 Beat the Ladder** — the six cards (or six new ones from their own copy of the text) scored by hand, mean compared to the ladder.
3. **17.3 Count the model** — the knob count by part at `d = 128`, then at a width of their choosing, predicted and checked with `.numel()`.
4. **17.4 The first-loss check** — predict the first loss for `calm_head=False` and `True`, run, and write one sentence on what a `FAIL` of 0.17 does and does not tell you.
5. **17.5 The run** — the lab deliverable: `train.py` with their own seed stated, reporting **the measured step time, the three checkpoint samples, train vs validation loss**, and the gap.
6. **17.6 What the gap means** — two sentences on what the gap means and one on what it does not; one sentence on what they would test next.

**Every number in a write-up must have been printed by the student's own run in the last 24 hours**, with the seed stated. Estimated time: 60-75 minutes, of which about two minutes is the computer working.

---

## 🔑 Answer Key

> **The workbook pages 17.1-17.6 follow this order.** Where an answer is a number it comes from `check_init.py`, `train.py` or `key.py`, all run from the Prep Checklist. **A student's own run uses their own seed; only the structure of the answer is fixed.**

### Page 17.1 — Windows and the shift

For the text `the cat sat on` (14 characters, counting the spaces: `t h e _ c a t _ s a t _ o n`) with window length `T = 5`:

| Start | `x` | `y` |
|:--:|---|---|
| 0 | `the c` | `he ca` |
| 4 | `cat s` | `at sa` |

Questions in a batch: **B x T** (32 x 64 = **2,048**). Valid starts for a text of length N and window T: `0 .. N - T - 1`, so **N - T** values; `randint(N - T, ...)`. For the course text: train **6,210**, validation **634** (`key.py`). *Common error:* `N - T + 1` (Clinic 4). *What to draw out:* `y` is `x` moved one place; each place is a separate question; the mask stops peeking.

### Page 17.2 — Beat the Ladder

Scoring is the student's own. The table of counts is in the Activity (mean **2.308** for the counts over the six cards). Acceptable: any mean, provided each line shows the probability given to the true letter and `-ln p` to three decimals. The quick table: `-ln(0.9) = 0.105`, `-ln(0.5) = 0.693`, `-ln(0.25) = 1.386`, `-ln(0.1) = 2.303`, `-ln(0.01) = 4.605`. The ladder: **3.332, 2.855, 2.033** and, after the run, **TinyGPT about 1.44 on held-out text (seed 0)**. *Common errors:* giving `0` to the true letter (the loss is infinite: `-ln 0`); using log base 10; not dividing the leftover among 25 letters. *What to draw out:* **six cards is a small sample**; a person who sees the whole sentence can beat a model that sees one letter.

### Page 17.3 — Count the model

| Part | Working | Count |
|---|---|:--:|
| character table | 28 x 128 | **3,584** |
| place table | 64 x 128 | **8,192** |
| one block | 12 x 128^2 + 10 x 128 | **197,888** |
| four blocks | 4 x 197,888 | **791,552** |
| final norm | 2 x 128 | **256** |
| output layer | 128 x 28 + 28 | **3,612** |
| **all** | | **807,196** |

At a width of the student's choosing `d` with `L` blocks, `V = 28`, `T = 64`: `28d + 64d + L(12d^2 + 10d) + 2d + (28d + 28)`. Worked example `d = 64, L = 2`: 1,792 + 4,096 + 2 x 49,792 + 128 + 1,820 = **107,420**. `d = 16, L = 1`: 448 + 1,024 + 3,232 + 32 + 476 = **5,212**. (Both were checked by building `TinyGPT(28, d, 4, L, 64)` and summing `.numel()`; the code is not part of the shipped files.) The attention share is unchanged (`T` and the heads add no knobs in a block); the place table and the output layer grow with `T` and `V`. *Common errors:* forgetting the biases of the output layer (`+ 28`), the place table, or the final norm; counting the mask (36 per block at `T = 6`, 4,096 at `T = 64`, none counted).

### Page 17.4 — The first-loss check

| | Prediction | Our run (seed 0) |
|---|---|---|
| `ln(28)` | 3.332 | 3.3322 |
| `calm_head=False` | about 3.5 or higher; `FAIL` | **3.5025**, distance 0.1702, `FAIL` |
| `calm_head=True` | within 0.05 | **3.3481**, distance 0.0159, `PASS` |

Model answer, one sentence: *"A failed check means the first loss is further from `ln(28)` than 0.05; here it is 0.17, so the model starts a little over-confident, and it trains fine; a check that was off by a lot would make me look for a bug, and the check cannot see a wrong `y`."* The student's own seed gives a different third decimal; the distance should still be under 0.05 for the calm head. *Common error:* "FAIL means the model will not train".

### Page 17.5 — The run (the lab deliverable)

What a complete write-up contains, for **their own** run (seed stated):

| Item | Our run (seed 0, one thread) | Acceptable range to expect |
|---|---|---|
| Knobs | 807,196 | exactly 807,196 |
| First loss (step 0) | train 3.349, val 3.351 | within 0.05 of 3.332 |
| Step time | 53 ms (62 ms on another run) | 30-150 ms on a modern laptop at one thread |
| Three checkpoint samples | steps 0, 300, 1499: random; `the`/`and`, no sentences; lines with full stops and mostly real words | same ordering in quality |
| Final train / val | 0.907 / 1.447 | train 0.8-1.0 · val 1.35-1.55 (**our judgement of what is normal, from one seed; other seeds not run**) |
| Gap | 0.540 | positive and clearly above 0.3 |
| Real words (1,000 chars) | 0% · 17% · 60% | rising |

The ranges in the last column are guidance for marking, not measured spreads. A student whose numbers fall outside them should look for: a different `STEPS`, a changed `lr`, a missing shift, or a changed model size, before accepting it.

### Page 17.6 — What the gap means

Model answer: *"The gap is validation loss minus training loss (1.447 - 0.907 = 0.540). It means the model does much better on characters it was trained on than on characters it has not seen, which is what memorising the training text looks like. It was about zero at step 300 and grew at each later checkpoint. It does not mean the model is useless, and it does not prove why; we did not run a version with more text, less training or dropout, which would be the test."*

| Criterion | Marks |
|---|:--:|
| States the gap as a number with the direction (validation higher) | 1 |
| Says the validation number is the fairer one for unseen text | 1 |
| Links it to memorising / the model fitting the text it saw, with the growth across checkpoints as evidence | 1 |
| Says what was **not** tested (a control: more data, less training, dropout, other seeds) | 1 |
| One concrete next experiment | 1 |

A write-up that says "the model is overfitting, so it is bad" or "the model understands English" loses the last two marks.

### Teacher-only: the map of wrong answers

| Their count or number | Likely cause |
|:--:|---|
| 1,536 more than 807,196 | a bias on q, k and v in four blocks (3 x 128 x 4) |
| 1,152 fewer | each of the 9 layer norms (2 per block x 4, plus the final) counted as `d` instead of `2d` (9 x 128) |
| 15,644 | the blocks are in a plain list (Clinic 3) |
| first loss far below 3.33 | a leak (`y` is `x`), or an unusual batch |
| training loss near 0.1 within a few hundred steps | the shift is missing (Clinic 2) |
| 3.50 at step 0 | `calm_head=False` (Clinic 1) |

Use these as a prompt for conversation, not a certainty.

### Answers to every question posed in the lesson

| Question | Answer |
|---|---|
| Why 0.693 in Week 1? | `ln 2`: each of two classes gets 1/2. |
| What does a model that knows nothing score on 28 characters? | `ln 28 = 3.332`. |
| What is `y`? | `x` moved one place left. |
| How many questions per step? | 32 x 64 = 2,048. |
| Why a `ModuleList`? | PyTorch must see the blocks inside. |
| What did Week 16 predict for the knobs? | 807,196. |
| Will the training and validation losses be about the same? | No: training ends lower (0.907 against 1.447 here). |
| Is the un-calmed model broken? | No; the first loss is 0.17 off `ln 28`. |
| Shapes of `x` and `y`? | `(32, 64)` each. |
| Predict the time per step | Ours: 53 ms. |
| What does the gap mean? | It does better on text it saw; consistent with memorising; not proven. |
| What did we not do? | Test other seeds, more text, dropout, other sizes; inspect what the model learned. |

---

## 🔮 Next Week Preview

**Week 18 — Review and Assessment 2.** A paper assessment of **Weeks 9-17**: gradient compounding (Week 10), gates (Week 11), sampling (Week 13), the attention arithmetic (Weeks 14-15), the block (Week 16), and today's build. *Nothing is new.* The student will redo the 3-token attention pass on a new set of numbers. **For the student:** finish the workbook, especially 17.5 and 17.6, and re-read page 16.4's count; the assessment will ask for one. **For you:** collect the student's three samples and their gap sentence; both are good diagnostic material for Week 18's remediation table. **Week 19** reuses today's model: the same `TinyGPT`, with one part removed at a time (the mask, the positions, the residuals, the norms), and a measurement for each. The `tinygpt.py` and the `train.py` from today are its starting point, so **keep both files**. The timing from today, about 53 ms per step, is the reason that Week 19 can afford a run of several models.

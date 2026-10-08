# Week 31 — Fine-Tuning, LoRA, and the Regression

[⬅ Week 30](week-30.md) · [Course Home](../README.md) · [Week 32 ➡](week-32.md) · [Workbook](../workbook/week-31.md)

---

![Thirty-six week tiles in four lanes of nine, one per term; weeks 1 to 30 solid, Week 31 (a lab week in term 4) tinted pink with a thick border and a pointer, weeks 32 to 36 dashed](../figures/fig-w31-0-where-this-fits.svg)

*Figure 31.0 — Week 31 of 36: a lab week in term 4, agents, evidence and the system card.*

---

> ### This week in one sentence
> **Fine-tuning is "keep training, on your labelled rows"; LoRA is "keep training, but only a thin patch beside frozen weights", and when you read the result by category the average can rise while one row falls.**
>
> **By the end of this chapter you will be able to:**
> - **Say what pretraining is** (hide a word, guess it, no labels) and run it on your own two-layer encoder
> - **Freeze an encoder** and train only a new five-way head: your **base model**
> - **Explain "low-rank" with a grid** and **count by hand** the numbers in a patch: `r × in + out × r`
> - **Write `LoRALinear`**, a frozen layer with a thin patch beside it, and **prove that step 0 equals the base model** exactly
> - **Work out the trainable percentage** of your own model by hand, then check it against the printed line
> - **Read Week 30's per-category table** on your own model, say how many *tickets* a regression is, and say why one seed cannot settle it
>
> **New maths:** **low-rank**: a big grid as a thin grid times a thin grid, needing far fewer numbers.
>
> **New syntax:** `nn.Parameter` · `requires_grad_(False)` · `nn.init.zeros_` / `nn.init.normal_` · `copy.deepcopy(model)`
>
> **Reading time:** about 30 minutes. **In class:** 70 minutes. **Homework:** about 55 minutes (workbook pages 31.1 to 31.3).

> **📌 About the code blocks.** Put the blocks in **one file**, `week31.py`, in the order they appear, or paste them into one Python session. Later blocks use names made by earlier ones. Run it from the folder that holds Week 30's five files (`evalset.py`, `traindata.py`, `dedup.py`, `scorer.py`, `compare.py`) **and** the file `pretrain_text.py`, which your teacher hands you. **You run `pretrain_text.py`; you do not type it.** Every output shown was printed by a real run on a CPU, with the seeds in the code. Timing lines (`took … s`, `seconds …`) vary from machine to machine. **Every other number should match yours.** If one table differs by a single ticket, that is a different torch build, and it is this week's lesson rather than a bug. Nothing needs the internet. **Pretraining takes about 13 seconds; everything else takes a few seconds.**

> **⚠️ This is a stand-in, not a real pretrained model.** Your encoder is your own Week 16 Block, two of them, 121,152 numbers. Its "pretraining text" is about 1,500 distinct template sentences made by a short Python generator. It has never seen a real sentence, and **nothing measured on it says anything about DistilBERT, a hosted model, or LoRA on a model with a billion numbers.** The *mechanics* today are the real ones: freezing, a patch that starts at zero, counting trainable numbers, the per-category table. The *scores* belong to this tiny model, these 64 training tickets and these 30 eval tickets. **One ticket is 0.033.**

---

## 🪝 Start Here

For thirty weeks you have trained models from scratch or called ones you did not train. Real teams most often do a third thing: take a model that already knows something, and **adjust it a little** for their own rows. Today you build that whole path at small size, and then you use Week 30's frozen eval on it to ask whether the adjustment helped *everywhere* or only on average.

Before any code, write three guesses on a card.

1. Suppose you train a model on 64 labelled tickets, then train *every* weight further on the same 64. How many of the 30 eval tickets do you think it gains, compared with training only a small new head on top: a lot, a few, or none?
2. A big grid of weights has 64 × 64 = 4,096 numbers. If I may store a *correction* to it as two thin grids instead, each with 4 rows or columns of 64, how many numbers do you think that needs?
3. Overall score goes from 0.600 to 0.633. Can one category have gone *down*?

Keep the card. We come back to it at the end.

---

## 🧠 The Big Idea

**Pretraining.** Take lots of text with no labels. Hide about one word in five. Ask the model to guess the hidden words. It has no labels and no teacher, yet it must learn which words turn up together. That is **pretraining**. The result is an **encoder**: it turns each word of a ticket into a row of 64 numbers. Unlike your Week 17 GPT, **every word may look at every word** (there is no "cannot see the future" mask, only one that hides the padding). That is what "encoder" means here.

**A head.** To classify, average the rows of the real words into one row for the whole ticket and let one small layer turn it into five scores, one per label. That small layer is the **head**.

**Fine-tuning** is continuing to train on your labelled rows. Two ways:

- **Full fine-tuning:** every number in the model may move.
- **Freezing:** some numbers are **frozen** (they do not move) and the rest are **trainable**.

**LoRA** is freezing with a trick. Keep every old weight frozen. Beside a layer, add a small **patch** whose output is added to the layer's output. The patch is built from two thin grids whose product is a full-size correction. Because the patch has few numbers, few numbers train. The patch starts at **exactly zero**, so at **step 0** the patched model *is* the base model. That is what makes "before" and "after" mean something.

Here is the whole path in one picture, in the order it happens.

![Unlabelled text, then step 1 pretrain once, giving an encoder, then step 2 a base model whose head alone trains (18 of 30 right), then step 3 a full fine-tune and a LoRA patch, each 19 of 30; below, the input going through a frozen old layer and a dashed patch of two thin grids A then B, added together](../figures/fig-w31-4-pretrain-base-patch.svg)
*Figure 31.3 — Pretrain once, build the base, then adjust a copy of it: with B at zero the patch adds nothing at step 0.*

**The regression.** A **regression**, in this course, is one category of Week 30's table getting worse. The overall score is a weighted sum of the categories. **A sum can hide a subtraction.**

---

## 1. The four new pieces of syntax

This section is for meeting the four pieces on toys small enough to read, before they appear inside the real model. The four pieces:

- **`nn.Parameter(tensor)`** marks a tensor as one PyTorch should train. Assign one to a module and it shows up in `model.parameters()`. A plain tensor assigned the same way does not.

- **`nn.init.normal_(t, std=0.02)` and `nn.init.zeros_(t)`** fill an existing tensor **in place**, with small random numbers (`std` is their typical size, from Week 3) or with zeros. The trailing underscore means "changes it where it stands".

- **`module.requires_grad_(False)`** freezes **every** parameter inside a module, in place. It is the same switch as `requires_grad=True` on one tensor (Week 2), applied to a whole module at once. `requires_grad_(True)` unfreezes.

- **`copy.deepcopy(model)`** makes a complete, independent copy of a whole model. In Week 5 you copied a dictionary of weights; today you copy the model. Without it, two names can point at *one* model.

Type this first, in its own file, `toys31.py`.

```python
# toys31.py - the four new pieces on toys small enough to read
import copy
import torch
import torch.nn as nn

torch.manual_seed(0)


class Holder(nn.Module):
    def __init__(self):
        super().__init__()
        self.plain = torch.zeros(2)                       # a plain tensor: PyTorch does not list it
        self.learned = nn.Parameter(torch.zeros(2))       # an nn.Parameter: PyTorch will train it


h = Holder()
print("parameters PyTorch can see:", [name for name, _ in h.named_parameters()])

nn.init.normal_(h.learned, std=0.02)                      # fill in place with small random numbers
print("after normal_:", h.learned.detach())
nn.init.zeros_(h.learned)                                 # fill in place with zeros
print("after zeros_: ", h.learned.detach())

lin = nn.Linear(3, 2)
print("trainable before:", [p.requires_grad for p in lin.parameters()])
lin.requires_grad_(False)                                 # freeze every parameter inside, in place
print("trainable after: ", [p.requires_grad for p in lin.parameters()])

a = nn.Linear(2, 2)
same = a                                                  # a second NAME for the same model
twin = copy.deepcopy(a)                                   # a second, independent model
nn.init.zeros_(a.weight)
print("same name sees the change:", same.weight.abs().sum().item())
print("deepcopy does not:        ", twin.weight.abs().sum().item() > 0)
```

```text
parameters PyTorch can see: ['learned']
after normal_: tensor([ 0.0308, -0.0059])
after zeros_:  tensor([0., 0.])
trainable before: [True, True]
trainable after:  [False, False]
same name sees the change: 0.0
deepcopy does not:         True
```

Read it. The `Holder` lists only `learned`, not `plain`: the plain tensor is invisible to training. `normal_` and `zeros_` changed `learned` where it stood. `requires_grad_(False)` turned both of the layer's switches off. And the last two lines are the reason `deepcopy` exists: `a` and `same` are **one** model, so zeroing `a` zeroed `same` too, while `twin` is a separate model that kept its numbers.

---

## 2. Check the files you stand on

This section is for confirming that Week 30's work is in place, because everything today stands on it: the 30 frozen eval tickets, the 66 raw training tickets, the dedup scan, `score` and `compare`. Start `week31.py` with this block.

```python
# p0_check.py - Week 31 block P0: the Week 30 files this week stands on, and one run of them.
# Week 30 left five files in the folder: evalset.py, traindata.py, dedup.py, scorer.py, compare.py.
import torch
from collections import Counter
from evalset import EVAL, LABELS
from traindata import TRAIN_RAW
from dedup import decontaminate
from scorer import score
from compare import compare

torch.set_num_threads(1)

TRAIN, removed = decontaminate(TRAIN_RAW, EVAL, verbose=False)
print("eval cases:", len(EVAL), " raw training tickets:", len(TRAIN_RAW),
      " kept:", len(TRAIN), " removed:", len(removed))
print("kept per label:", dict(Counter(y for _, y in TRAIN)))
print("labels:", LABELS)
```

```text
eval cases: 30  raw training tickets: 66  kept: 64  removed: 2
kept per label: {'greeting': 14, 'refund': 14, 'technical': 14, 'billing': 14, 'out_of_scope': 8}
labels: ['greeting', 'refund', 'technical', 'billing', 'out_of_scope']
```

If your counts differ (30, 66, 64, 2 and 14 14 14 14 8), stop and fix Week 30's files first. Every number below is for those files. Note the five labels: there are **14, 14, 14, 14 and only 8** training tickets, because `out_of_scope` lost tickets to the scan.

---

## 3. The pretraining text, and a scan of it

This section is for making the pretraining text and scanning it for contamination before any model sees it.

Your teacher gave you `pretrain_text.py`, a short generator that writes template sentences such as `what am i charged per month?`. **It is a stand-in for "lots of text", not a corpus.** Contamination can arrive through the pretraining text too, so point Week 30's scan at the output before you use it.

```python
# p2_corpus.py - Week 31 block P2: make the pretraining text and run Week 30's contamination scan over it.
from pretrain_text import make_corpus

corpus = make_corpus(6000, seed=0)
print(len(corpus), "sentences;", len(set(corpus)), "distinct")
for s in corpus[:5]:
    print("  ", s)

exact = [t for t, _ in EVAL if t in corpus]
print("eval tickets found word for word in the corpus:", exact)

pairs = [(s, "unlabelled") for s in sorted(set(corpus))]
clean_pairs, near = decontaminate(pairs, EVAL, verbose=False)
print("near-copies of an eval ticket (Jaccard >= 0.70):", len(near))
for i, s, (j, ei, e) in near[:5]:
    print(f"   {s!r}  ~  {e!r}  ({j:.2f})")

near_set = {s for _, s, _ in near}
corpus = [s for s in corpus if s not in near_set]
print("sentences left after dropping them:", len(corpus), " distinct:", len(set(corpus)))
```

```text
6000 sentences; 1518 distinct
   what am i charged per month?
   afternoon there
   when is my next invoice due?
   how do i change my payment method?
   the parcel is the wrong colour, i want my money back
eval tickets found word for word in the corpus: []
near-copies of an eval ticket (Jaccard >= 0.70): 38
   'afternoon are you there'  ~  'good afternoon, are you there?'  (0.80)
   'afternoon, are you there'  ~  'good afternoon, are you there?'  (0.80)
   'do i pay postage to cancel something?'  ~  'do I pay postage to return something?'  (0.75)
   'do i pay postage to exchange something?'  ~  'do I pay postage to return something?'  (0.75)
   'do i pay postage to refund something?'  ~  'do I pay postage to return something?'  (0.75)
sentences left after dropping them: 5672  distinct: 1480
```

Read the counts. 6,000 sentences were made but only 1,518 are different: templates repeat. **No eval ticket appears word for word.**

But Week 30's Jaccard test finds **38** different near-copies, such as `'afternoon are you there'` against `'good afternoon, are you there?'`. They come out before pretraining. Nobody typed an eval ticket into the generator; a template simply landed a few words away from one.

Next, turn words into numbers. Every word that appears in the pretraining text or in the 64 training tickets gets an id. Ids 0, 1 and 2 are special: padding, unknown and the hidden-word marker.

```python
# p3_vocab.py - Week 31 block P3: words to numbers. Words seen in the pretraining text or the 64 tickets get ids.
import re
import torch

WORD = re.compile(r"[a-z0-9']+|[^\sa-z0-9']")
T = 16                                                     # longest ticket we keep, in words


def words_of(text):
    return WORD.findall(text.lower())


vocab_words = sorted({w for s in corpus for w in words_of(s)} | {w for s, _ in TRAIN for w in words_of(s)})
itos = ["<pad>", "<unk>", "<mask>"] + vocab_words      # ids 0, 1, 2 are special
stoi = {w: i for i, w in enumerate(itos)}
V = len(itos)


def encode(text):
    ids = [stoi.get(w, 1) for w in words_of(text)][:T]     # unknown word -> 1
    return ids + [0] * (T - len(ids))                      # pad with 0 up to T


eval_words = [w for t, _ in EVAL for w in words_of(t)]
unknown = [w for w in eval_words if w not in stoi]
print("vocabulary size V =", V, " longest ticket in words:", max(len(words_of(t)) for t, _ in EVAL + TRAIN))
print("eval words the model has never seen:", len(unknown), "of", len(eval_words))
print(encode("clicking save does absolutely nothing"))

X_text = torch.tensor([encode(s) for s in corpus])
X_train = torch.tensor([encode(t) for t, _ in TRAIN])
Y_train = torch.tensor([LABELS.index(y) for _, y in TRAIN])
print("pretraining tensor", tuple(X_text.shape), " training tensor", tuple(X_train.shape), tuple(Y_train.shape))
```

```text
vocabulary size V = 319  longest ticket in words: 14
eval words the model has never seen: 37 of 220
[1, 236, 83, 1, 188, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
pretraining tensor (5672, 16)  training tensor (64, 16) (64,)
```

Look at the encoded line. `"clicking save does absolutely nothing"` became `[1, 236, 83, 1, 188, 0, …]`: `clicking` and `absolutely` are id `1` (never seen), the others have real ids, and the tail is padding. **37 of the 220 words in the eval tickets are unknown to the model.** The other 183 are known, because the person who wrote the generator had seen the eval tickets. That is kind to the model, and it is only fair to say so. The eval *sentences* are not in the text; the scan above is what checks that.

---

## 4. Your Week 16 Block becomes an encoder

This section is for building the encoder from your own earlier code. It is the same `Block` as Week 16, with one change: the causal mask is replaced by a **padding mask**, so no word looks at padding but every word looks at every other word. Two Blocks make the `Encoder`.

```python
# p4_encoder.py - Week 31 block P4: YOUR Week 16 Block with the causal mask replaced by a padding mask, and an Encoder of two.
import copy
import torch.nn as nn
import torch.nn.functional as F


class Block(nn.Module):
    def __init__(self, d, H):
        super().__init__()
        self.H = H
        self.ln1 = nn.LayerNorm(d)
        self.q = nn.Linear(d, d, bias=False)
        self.k = nn.Linear(d, d, bias=False)
        self.v = nn.Linear(d, d, bias=False)
        self.proj = nn.Linear(d, d)
        self.ln2 = nn.LayerNorm(d)
        self.up = nn.Linear(d, 4 * d)
        self.act = nn.GELU()
        self.down = nn.Linear(4 * d, d)

    def forward(self, x, pad):                              # pad: (B, T), True where the slot is padding
        B, T, d = x.shape
        dh = d // self.H
        h = self.ln1(x)
        q = self.q(h).view(B, T, self.H, dh).transpose(1, 2)
        k = self.k(h).view(B, T, self.H, dh).transpose(1, 2)
        v = self.v(h).view(B, T, self.H, dh).transpose(1, 2)
        scores = q @ k.transpose(-2, -1) / dh ** 0.5
        scores = scores.masked_fill(pad.view(B, 1, 1, T), float("-inf"))     # nobody looks at padding
        mixed = (F.softmax(scores, dim=-1) @ v).transpose(1, 2).reshape(B, T, d)
        x = x + self.proj(mixed)
        return x + self.down(self.act(self.up(self.ln2(x))))


class Encoder(nn.Module):
    def __init__(self, V, d=64, H=4, L=2, T=16):
        super().__init__()
        self.d = d
        self.tok = nn.Embedding(V, d)
        self.pos = nn.Embedding(T, d)
        self.blocks = nn.ModuleList([Block(d, H) for _ in range(L)])
        self.ln_f = nn.LayerNorm(d)

    def forward(self, ids):                                 # ids: (B, T) -> (B, T, d); every word sees every word
        pad = ids == 0
        x = self.tok(ids) + self.pos(torch.arange(ids.shape[1]))
        for blk in self.blocks:
            x = blk(x, pad)
        return self.ln_f(x)


def count(model):
    return sum(p.numel() for p in model.parameters())


torch.manual_seed(0)
encoder = Encoder(V)
print("encoder parameters:", count(encoder))
print("one Block:", count(encoder.blocks[0]), " of which q and v:", count(encoder.blocks[0].q) + count(encoder.blocks[0].v))
print("output shape:", tuple(encoder(X_train[:3]).shape))
```

```text
encoder parameters: 121152
one Block: 49792  of which q and v: 8192
output shape: (3, 16, 64)
```

The encoder has **121,152** numbers. One Block has 49,792, of which `q` and `v` (4,096 each) are 8,192. Keep those two in mind; LoRA will attach its patches to them.

---

## 5. Pretrain once

This section is for running pretraining once, to get the encoder every later run starts from. Hide 20% of the real words (replace them with `<mask>`, id 2) and ask the encoder to guess them. The slots that were not hidden get the target `-100`, which `cross_entropy` ignores (Week 12). There are **no labels anywhere**.

```python
# p5_pretrain.py - Week 31 block P5: PRETRAIN once. Hide 20% of the words; predict them. No labels anywhere.
import time


class MLM(nn.Module):
    def __init__(self, enc, V):
        super().__init__()
        self.enc = enc
        self.head = nn.Linear(enc.d, V)                      # a score for every word in the vocabulary

    def forward(self, ids):
        return self.head(self.enc(ids))


torch.manual_seed(0)
mlm = MLM(encoder, V)
opt = torch.optim.AdamW(mlm.parameters(), lr=2e-3)
gen = torch.Generator().manual_seed(0)
t0 = time.time()
for step in range(1500):
    x = X_text[torch.randint(len(X_text), (64,), generator=gen)]
    hide = (torch.rand(x.shape, generator=gen) < 0.2) & (x != 0)        # True where we hide a real word
    target = x.masked_fill(hide == 0, -100)                           # hide == 0 is True where NOT hidden; -100 = "ignore this slot" (Week 12)
    logits = mlm(x.masked_fill(hide, 2))                                # 2 = <mask>
    loss = F.cross_entropy(logits.reshape(-1, V), target.reshape(-1), ignore_index=-100)
    opt.zero_grad()
    loss.backward()
    opt.step()
    if step in (0, 100, 500, 1000, 1499):
        print(f"step {step:4d}  loss {loss.item():.3f}")
pretrain_seconds = time.time() - t0
print(f"pretraining took {pretrain_seconds:.1f} s")
pretrained = copy.deepcopy(encoder)                          # the pristine pretrained encoder, kept for every later run
```

```text
step    0  loss 5.923
step  100  loss 2.266
step  500  loss 0.628
step 1000  loss 0.480
step 1499  loss 0.522
pretraining took 14.1 s
```

The loss starts at 5.923. That is about what guessing among 319 words costs (`ln 319` is 5.77). It falls to about 0.5 and **not to zero**, because when a template slot is hidden (`the ___ keeps closing`) several words fit, and the best any model can do is spread its bet. The last line keeps a pristine copy of the trained encoder, `pretrained`, for every run that follows.

**What did pretraining buy?** A model that starts fine-tuning already knowing which words go together. It did *not* learn to understand language, and it never saw a label.

---

## 6. A head, and the helpers

This section is for building the classifier and the three helpers used all week. A classifier is the encoder plus a five-way head. The helpers `make_base`, `predict` and `fit` are used all week. Look at `fit`: it hands the optimiser only the parameters that are *not* frozen.

```python
# p6_classifier.py - Week 31 block P6: a classifier on top of the pretrained encoder, and the three helpers used all week.
X_eval = torch.tensor([encode(t) for t, _ in EVAL])


class Clf(nn.Module):
    def __init__(self, enc, n=5):
        super().__init__()
        self.enc = enc
        self.head = nn.Linear(enc.d, n)                      # d numbers -> one score per label

    def forward(self, ids):
        h = self.enc(ids)                                    # (B, T, d)
        keep = (ids != 0).unsqueeze(-1).float()              # 1.0 for real words, 0.0 for padding
        return self.head((h * keep).sum(1) / keep.sum(1))    # average the real words, then score


def make_base(seed):
    torch.manual_seed(seed)                                  # the seed decides the new head's starting numbers
    return Clf(copy.deepcopy(pretrained))


def predict(model):
    model.eval()
    with torch.no_grad():
        return [LABELS[i] for i in model(X_eval).argmax(1).tolist()]


def fit(model, steps, lr, seed):
    params = [p for p in model.parameters() if p.requires_grad]      # only what is NOT frozen
    opt = torch.optim.AdamW(params, lr=lr)
    torch.manual_seed(seed)
    model.train()
    for _ in range(steps):
        pick = torch.randperm(len(X_train))[:16]
        loss = F.cross_entropy(model(X_train[pick]), Y_train[pick])
        opt.zero_grad()
        loss.backward()
        opt.step()
    return loss.item()


untrained = make_base(0)
r0 = score(predict(untrained), "pretrained encoder + brand-new head")
print(f"{r0['name']}: {r0['correct']}/30 = {r0['overall']:.3f}   (a coin over five labels would give 6/30 = 0.200)")
```

```text
pretrained encoder + brand-new head: 4/30 = 0.133   (a coin over five labels would give 6/30 = 0.200)
```

The encoder plus a brand-new, untrained head gets 4 of 30 right. A coin over five labels would get about 6, so this is a model with nothing yet trained on the task.

---

## 7. Low-rank, on paper first

This section is for meeting the low-rank idea by hand before it appears in code. **Do this part on paper, before you run anything.**

1. Take a column of four numbers `(1, 2, 0, -1)` and a row of four `(2, 1, 0, 3)`.
2. Multiply every column number by every row number and write the results in a 4 × 4 grid. Row 1 of the grid is `1 ×` the row, row 2 is `2 ×` it.
3. Fill in rows 3 and 4 yourself.
4. Then run this block.

```python
# p7_lowrank.py - Week 31 block P7: the new idea. A 4 x 4 grid built from a column of 4 and a row of 4.
col = torch.tensor([[1.], [2.], [0.], [-1.]])                # 4 numbers
row = torch.tensor([[2., 1., 0., 3.]])                       # 4 numbers
grid = col @ row                                             # (4,1) @ (1,4) -> (4,4)
print(grid)
print("cells in the grid:", grid.numel(), "  numbers we had to store:", col.numel() + row.numel())

d, r = 64, 4
whole = d * d                                                # one square projection, stored in full
thin = r * d + d * r                                         # r x in  +  out x r
print(f"one {d} x {d} projection: {whole} numbers;  the rank-{r} patch: {thin} numbers;  share {thin / whole:.4f}")
```

```text
tensor([[ 2.,  1.,  0.,  3.],
        [ 4.,  2.,  0.,  6.],
        [ 0.,  0.,  0.,  0.],
        [-2., -1.,  0., -3.]])
cells in the grid: 16   numbers we had to store: 8
one 64 x 64 projection: 4096 numbers;  the rank-4 patch: 512 numbers;  share 0.1250
```

The grid has **16 cells**, built from **8 numbers**. Every row of it is a multiple of the row we started with. A grid that can be built from one column and one row is called **rank 1**. A grid that needs two column-and-row pairs added together is **rank 2**, and so on: the **rank** is *how many column-times-row layers you need to build the grid*. That is the whole definition.

Now the count. One projection in your model maps 64 numbers to 64 numbers, so it stores a 64 × 64 grid: **4,096 numbers**. A rank-`r` patch stores two thin grids, `A` of shape `r × in` and `B` of shape `out × r`, and uses their product as a correction of the full 64 × 64 size:

```text
numbers in the patch  =  r × in  +  out × r
```

For `r = 4`: `4 × 64 + 64 × 4 = 256 + 256 = 512`, which is `512 / 4096 = 0.125` of the projection. The saving is not free: a rank-4 patch can only make corrections that are sums of four layers.

![A 4 by 4 grid of products built from a column of four numbers and a row of four, beside two bars: 4,096 numbers for a full 64 by 64 projection against 512 for the rank-4 patch](../figures/fig-w31-1-low-rank-patch.svg)
*Figure 31.1 — A grid built from one column and one row stores 8 numbers for 16 cells, so a rank-4 patch is 0.1250 of the projection.*

---

## 8. `LoRALinear`

This section is for writing the LoRA layer itself. Type it one piece at a time and ask of each line: *what is this number right now?*

```python
# p8_lora.py - Week 31 block P8: LoRA. Keep the old projection frozen; add a thin-times-thin patch beside it.
class LoRALinear(nn.Module):
    def __init__(self, base, r=4, alpha=8):
        super().__init__()
        self.base = base
        self.base.requires_grad_(False)                          # freeze the old weights in place
        self.A = nn.Parameter(torch.zeros(r, base.in_features))  # a tensor PyTorch will train
        self.B = nn.Parameter(torch.zeros(base.out_features, r))
        nn.init.normal_(self.A, std=0.02)                        # A starts small and random
        nn.init.zeros_(self.B)                                   # B starts at exactly zero, so the patch adds nothing yet
        self.scale = alpha / r                                   # a volume knob on the patch

    def forward(self, x):
        return self.base(x) + (x @ self.A.T @ self.B.T) * self.scale


def add_lora(model, r=4, alpha=8):
    model.enc.requires_grad_(False)                              # freeze the whole encoder first
    for blk in model.enc.blocks:
        blk.q = LoRALinear(blk.q, r, alpha)                      # the new modules are trainable; the head still is too
        blk.v = LoRALinear(blk.v, r, alpha)
    return model


def trainable(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)
```

This block only defines things, so it prints nothing. Read it.

- `self.base = base` keeps the old layer, and `requires_grad_(False)` freezes it: its numbers still take part in every forward pass, they just do not move.
- `A` has shape `r × in` and starts small and random. `B` has shape `out × r` and starts at **exactly zero**.
- The output is the old output **plus** `x @ A.T @ B.T`, times a `scale`. `scale = alpha / r` is a volume knob on the patch. With `B` at zero the patch adds nothing.
- `add_lora` freezes the whole encoder, then wraps `q` and `v` of each of the two Blocks. That is **four** patches. The new patches are trainable, and so is the head.

**Why is `B` zero and `A` random?** Keep this question for Your Turn.

---

## 9. The base model, and step 0

This section is for building the base model and checking the start of the patch. Train the head alone on the frozen encoder: that is your **base model**. Then build the LoRA model from a `deepcopy` of it and check that the patch starts as a no-op.

**Before you run this, work out on paper:** four patches of 512 numbers, plus the head (`64 × 5 + 5`), is how many trainable numbers? The whole model is the 121,152 of the encoder plus the head plus the four patches: how many? What percentage is trainable? Then run it and compare.

```python
# p9_step0.py - Week 31 block P9: train the cheap "base" model, then prove the patch starts as a no-op.
base = make_base(0)
base.enc.requires_grad_(False)                                   # the encoder stays exactly as pretraining left it
base_loss = fit(base, steps=100, lr=3e-3, seed=0)
rb = score(predict(base), "base: frozen encoder + trained head")
print(f"{rb['name']}: {rb['correct']}/30 = {rb['overall']:.3f}   final training loss {base_loss:.3f}")

lora = add_lora(copy.deepcopy(base))                             # deepcopy: base itself must not change
with torch.no_grad():
    gap = (lora(X_eval) - base(X_eval)).abs().max().item()
print("step 0: biggest difference between lora and base outputs:", gap)
print("parameters: all", count(lora), " trainable", trainable(lora), f" ({100 * trainable(lora) / count(lora):.2f}%)")

base_w = base.enc.blocks[0].q.weight.clone()
loss = F.cross_entropy(lora(X_train), Y_train)
loss.backward()
blk = lora.enc.blocks[0]
print("first gradient:  biggest |A.grad| =", blk.q.A.grad.abs().max().item(),
      "  biggest |B.grad| =", round(blk.q.B.grad.abs().max().item(), 5))
```

```text
base: frozen encoder + trained head: 18/30 = 0.600   final training loss 0.520
step 0: biggest difference between lora and base outputs: 0.0
parameters: all 123525  trainable 2373  (1.92%)
first gradient:  biggest |A.grad| = 0.0   biggest |B.grad| = 0.00208
```

Three lines matter.

- `18/30 = 0.600`: the base model. The encoder is frozen; only the head's 325 numbers were trained.
- `biggest difference between lora and base outputs: 0.0`. **Exactly zero, not "small".** The patch adds `scale × (x @ A.T @ B.T)` and `B` is zero.
- The percentage is for *this* model, this `r` and these target layers. A LoRA percentage belongs to one choice of each.

Then the first gradient. `biggest |A.grad| = 0.0` while `|B.grad|` is not zero. On step 0 only `B` can learn, because the patch's output is multiplied by `B`, which is zero; `A` starts learning on step 1.

---

## 10. Two fine-tunes from one base

This section is for continuing training from the same base in two ways, so they can be compared.

- **Full:** unfreeze everything, learning rate `3e-4`.
- **LoRA:** the patched model, learning rate `3e-3`.

Both run 100 steps. The learning rates are the first values tried; they were not changed after seeing a score.

**Before you run this, write a prediction:** how many of 30 will full fine-tuning get, compared with the base's 18? Keep your guess for Page 31.3.

```python
# p10_finetune.py - Week 31 block P10: three models from the same base: the base, full fine-tuning, LoRA.
t0 = time.time()
full = copy.deepcopy(base)
full.requires_grad_(True)                                        # unfreeze everything
full_loss = fit(full, steps=100, lr=3e-4, seed=100)
full_seconds = time.time() - t0

t0 = time.time()
lora = add_lora(copy.deepcopy(base))
lora_loss = fit(lora, steps=100, lr=3e-3, seed=100)
lora_seconds = time.time() - t0

rf = score(predict(full), "full fine-tune")
rl = score(predict(lora), "LoRA r=4 on q and v")
for name, m, res, ls in (("base", base, rb, base_loss), ("full", full, rf, full_loss), ("lora", lora, rl, lora_loss)):
    print(f"{name:5s} trainable {trainable(m):7d}  final loss {ls:.3f}  eval {res['correct']}/30 = {res['overall']:.3f}")
print("base weight of block 0 q unchanged after LoRA?", torch.equal(base_w, lora.enc.blocks[0].q.base.weight))
print(f"seconds: full {full_seconds:.2f}  lora {lora_seconds:.2f}")
```

```text
base  trainable     325  final loss 0.520  eval 18/30 = 0.600
full  trainable  121477  final loss 0.014  eval 19/30 = 0.633
lora  trainable    2373  final loss 0.005  eval 19/30 = 0.633
base weight of block 0 q unchanged after LoRA? True
seconds: full 0.24  lora 0.22
```

Full fine-tuning trained **121,477** numbers; LoRA trained **2,373**. Both got 19 of 30, one ticket above the base. The last two lines say the old weights of `q` in Block 0 did not move, and that at this size the patch saves no time at all. Both final training losses are near zero on 64 tickets while the eval score is 0.633: that is the memorising from Week 5, and the reason Week 30 froze the eval first.

---

## 11. The table that is the point

This section is for reading Week 30's per-category table on your own model. Run `compare` between the base model and the LoRA model.

```python
# p11_regression.py - Week 31 block P11: Week 30's table, base -> LoRA. The average first, then the rows.
regressions = compare(rb, rl)
```

```text
category         n   before    after    delta
----------------------------------------------
greeting         6    0.833    0.833   +0.000
refund           7    1.000    1.000   +0.000
technical        7    0.286    0.571   +0.286
billing          5    0.400    0.200   -0.200  <-- REGRESSION
out_of_scope     5    0.400    0.400   +0.000
----------------------------------------------
OVERALL         30    0.600    0.633   +0.033

contribution of each category to the overall delta:
  greeting       (n/N = 6/30) x +0.000 = +0.0000
  refund         (n/N = 7/30) x +0.000 = +0.0000
  technical      (n/N = 7/30) x +0.286 = +0.0667
  billing        (n/N = 5/30) x -0.200 = -0.0333
  out_of_scope   (n/N = 5/30) x +0.000 = +0.0000

1 REGRESSION(S) - do not ship on the average alone:
   billing: 0.400 -> 0.200 (-20.0% on n=5)
```

Read it **row by row before you read the flag**. Technical rose by 0.286. Billing fell by 0.200. The overall change is `+0.0667 − 0.0333 = +0.0333`: two tickets gained, one lost, and the average could not tell you.

Now the question this lesson exists to ask: **how many tickets is −0.200 on billing?** Billing has 5 tickets in the eval. Work it out before you read on.

It is **one ticket**: 2 of 5 became 1 of 5. The flag is a **tripwire, not a verdict**: it tells you where to look. Which brings up the honest question: would it survive another seed?

![Paired before and after bars for five categories and the overall score, with the billing row outlined as a regression and the weighted gains and losses summed underneath](../figures/fig-w31-2-regression-row.svg)
*Figure 31.2 — The overall score rose by 0.0333 while billing fell by one ticket: read the rows before you read the average.*

---

## 12. Six seeds, every row kept

This section is for asking whether one seed's table can be trusted. Run the same comparison for six seeds. Each seed changes the new head's starting numbers and the order of the 16-ticket batches. **Every row is printed; none is picked.** The function `drops` repeats the rule inside `compare` so that we can list the flagged categories for each seed in one line.

```python
# p12_seeds.py - Week 31 block P12: the same comparison for six seeds. Every row is kept; none is picked.
def drops(before, after, min_n=5, drop=0.10):
    out = []
    for cat in LABELS:
        n = before["per_category"][cat][1]
        d = after["per_category"][cat][2] - before["per_category"][cat][2]
        if n >= min_n and d <= -drop:
            out.append((cat, round(d, 2)))
    return out


t0 = time.time()
print("seed  base  full  lora   regressions base -> lora (n>=5, drop >= 0.10)")
flagged = 0
for seed in range(6):
    b = make_base(seed)
    b.enc.requires_grad_(False)
    fit(b, steps=100, lr=3e-3, seed=seed)
    f = copy.deepcopy(b)
    f.requires_grad_(True)
    fit(f, steps=100, lr=3e-4, seed=seed + 100)
    l = add_lora(copy.deepcopy(b))
    fit(l, steps=100, lr=3e-3, seed=seed + 100)
    sb, sf, sl = (score(predict(m), n) for m, n in ((b, "b"), (f, "f"), (l, "l")))
    dl = drops(sb, sl)
    flagged += len(dl) > 0
    print(f"{seed:4d}  {sb['correct']:4d}  {sf['correct']:4d}  {sl['correct']:4d}   {dl}")
print(f"seeds with at least one flagged category: {flagged} of 6")
print(f"six seeds took {time.time() - t0:.1f} s")
```

```text
seed  base  full  lora   regressions base -> lora (n>=5, drop >= 0.10)
   0    18    19    19   [('billing', -0.2)]
   1    15    18    19   []
   2    18    19    18   [('greeting', -0.17), ('billing', -0.2)]
   3    16    19    19   [('billing', -0.2)]
   4    17    19    18   [('refund', -0.14)]
   5    17    20    18   [('out_of_scope', -0.2)]
seeds with at least one flagged category: 5 of 6
six seeds took 3.4 s
```

Read it aloud. The base column runs `18 15 18 16 17 17`. Full is `19 18 19 19 19 20`. LoRA is `19 19 18 19 18 18`. Five of six seeds flag *something*, and it is a different category in different seeds. One single method varies by one to three tickets from seed to seed (base 15 to 18, full 18 to 20, LoRA 18 to 19). **The seed is a small experiment; the spread is the result.** Nothing here ranks full fine-tuning against LoRA.

And one more number to put next to them. Week 30's free rules scored **25 of 30 = 0.833**. Your best model today scored 19. The honest table for a ship decision is *rules → LoRA*, not *base → LoRA*, and it has more flags than the one above.

Here are the six rows side by side, each seed's three counts and the category that fell.

![A dot chart of tickets right out of 30 for seeds 0 to 5, a circle for base, a square for full fine-tuning and a triangle for LoRA, with the numbers and the category that fell from base to LoRA beside each seed, and a callout that 5 of 6 seeds flag something](../figures/fig-w31-5-six-seeds-every-row.svg)
*Figure 31.4 — Across six seeds the base moves by three tickets, full fine-tuning by two and LoRA by one, and a different category falls each time.*

---

## 🎲 Your Turn

### Grid Cards

Do this on paper. This page practises spotting and counting low-rank grids. **The row test:** *pick the first row that is not all zeros; is every other row a multiple of it?* If yes, the grid is rank 1.

- **Card A.** Column `(1, 2, 0, -1)`, row `(2, 1, 0, 3)`. Fill all sixteen cells. (You did this in Section 7.)
- **Card B.** The same grid, but the cell in row 4, column 3 holds `5`. Can you still build it from one column and one row?
- **Card C.** This finished grid. Is it one column times one row?

```text
 2   1   0   3
 5   2   2   7
 1   0   2   1
-2  -1   0  -3
```

Then the counting game. How many numbers does a rank-1 patch for a 64 × 64 grid need? Rank 4? Rank 32? **At what rank does the patch stop saving anything?**

### Four questions about the run

1. Why is `B` zero and `A` random? What would happen to the gradients if *both* started at zero?
2. The model is 123,525 numbers, more than the 121,152-number encoder you started with. So what exactly did LoRA make smaller?
3. "Technical is up 0.286, so we are good at technical now." What is wrong with that sentence, in tickets?
4. A row reads `+0.000`. Can tickets have changed inside it?

---

## 🔬 Break It On Purpose

**DELIBERATE, and silent.** Here `B` is started at random instead of zero. The run does not crash and prints nothing alarming. Add this to the end of `week31.py`, predict what the step-0 gap will be, then run it.

```python
# DELIBERATE BUG D1 (SILENT): B starts random, not zero, so the "patch" changes the model before any training.
class BadInit(LoRALinear):
    def __init__(self, base, r=4, alpha=8):
        super().__init__(base, r, alpha)
        nn.init.normal_(self.B, std=0.02)                 # the bug: should be nn.init.zeros_(self.B)


bad = copy.deepcopy(base)
bad.enc.requires_grad_(False)
for blk in bad.enc.blocks:
    blk.q = BadInit(blk.q)
    blk.v = BadInit(blk.v)
with torch.no_grad():
    print("step 0 gap, bad patch:", round((bad(X_eval) - base(X_eval)).abs().max().item(), 4))
```

```text
step 0 gap, bad patch: 0.027
```

The gap is `0.027`, not `0.0`. Before a single step of training, the "patch" has already changed the model, so anything you later say about "what LoRA changed" is mixed up with "what the random start changed". The score may not even move, which is the danger: **nothing announces it.** The cure is the check from Section 9, with `0.0` as the required answer and not "small".

---

## 🧭 What was shown, and what was not

**Shown:**
- Pretraining by hiding words, on template text, with no labels (loss 5.923 to 0.522).
- A base model: frozen encoder, trained head, 325 trainable numbers, 18 of 30.
- Low-rank, as a 4 × 4 grid from 8 numbers, then `r × in + out × r` (512 against 4,096).
- `LoRALinear`, with step 0 equal to the base model exactly, and the trainable share: 2,373 of 123,525 (1.92%).
- Full fine-tuning and LoRA both at 19 of 30, and the base weights unchanged after LoRA.
- A per-category table where overall rose by one ticket and billing fell by one.
- Six seeds: five of six flag a category, and it is not always the same one.

**Not shown:**
- **Any real pretrained model.** Your encoder read template sentences; it did not learn English. The pretraining text also contains most of the eval vocabulary, which flatters the model.
- **That LoRA matches full fine-tuning.** On these numbers you cannot tell the two apart.
- **Any speed or memory saving.** Full fine-tuning took about as long as LoRA at this size.
- **A rule for choosing `r`.** The rank was set to 4 before anything was looked at.
- **That the model is useful.** The free rules score 25 of 30 and your best model scores 19.

One confession. While the pretraining text was being written, the author saw eval scores, and widened the vocabulary when too many eval words were unknown. The eval sentences themselves were never copied in, and the scan checks that. It is the same sin as tuning on the test set, at small size. If you catch yourself changing a learning rate "until billing recovers", that is the same sin.

---

## 🔑 Wrap Up

1. Turn to your card. What did full fine-tuning gain over the base, in tickets? Was it "a lot"?
2. How many numbers did the patch need, against the 4,096 of the projection it corrects?
3. Overall went from 0.600 to 0.633 and billing fell. Say in one sentence how both can be true.
4. Why must the step-0 check say `0.0` and not "small"?
5. Five of six seeds flag a category. Does that make the billing flag a verdict, or a tripwire?
6. Which would you ship: the rules or the LoRA model? Why?

Then write this sentence in your Bug Log in your own handwriting, with your own numbers in it:

> **"LoRA trained 2,373 of 123,525 numbers and got 19 of 30, like full fine-tuning; the average rose by one ticket while billing lost one; one ticket on five is a reason to look and not a verdict; and the free rules still beat both."**

**A look ahead.** Next week asks what happens when a model is sure *and wrong*. You will measure how often "80% sure" is right. Bring one sentence for Monday: *"when my classifier says it is 80% sure, how often is it right?"* Keep this week's habit of looking for a category that fell while the average rose.

---

## 📤 Homework

Complete workbook pages 31.1 to 31.3 (about 55 minutes: 25 of pen and paper, 30 at the computer). Write your **predictions before you run anything.** Every number you write must come from your own arithmetic or your own run. Page 31.3 asks for seed 1, not seed 0, and for the number of **tickets** each row moved.

**Optional (fast students).** Run the LoRA model at three different ranks over six seeds each. Report a table of means **and** ranges, and one sentence that says whether there is a knee or only noise.

---

## 📖 Words from this week

| Word | Meaning |
|---|---|
| **pretraining** | training on unlabelled text by hiding words and guessing them |
| **encoder** | a model in which every word can look at every word, and that turns each word into a row of numbers |
| **head** | a small layer on top that turns the encoder's output into five scores |
| **fine-tuning** | continuing to train on your labelled rows |
| **frozen / trainable** | a number that does not move / one that may |
| **adapter / patch** | a small piece added beside a frozen layer, whose output is added to the layer's output |
| **low-rank** | a big grid written as a thin grid times a thin grid |
| **rank `r`** | how many column-times-row layers a grid or patch is built from |
| **LoRA** | fine-tuning with frozen weights and a low-rank patch |
| **base model** | the model you start from, and compare with |
| **step 0** | the moment before any training step: the patched model must equal the base |
| **regression** | one category of the table getting worse |
| **trainable percentage** | trainable numbers divided by all numbers in the model |
| **stand-in** | a toy imitating something real; measures nothing about the real one |

---

[⬅ Week 30](week-30.md) · [Course Home](../README.md) · [Week 32 ➡](week-32.md) · [Workbook](../workbook/week-31.md)

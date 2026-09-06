# Module 6 — PyTorch: Tensors, Autograd, and Real Training Loops

**Level 3 · Module 6 · ~5.5 hours · Prereqs: Module 4 (log loss, gradient descent, learning rate) and Module 5 (forward pass, backprop, He init, dead ReLUs).**

[⬅ Previous](module-05-neural-networks-from-scratch.md) · [Level 3 Home](README.md) · [Next ➡](module-07-cnns-for-images.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. You will be able to create tensors with a chosen dtype and shape, move them to a device (`cpu` / `cuda` / `mps`), and state two concrete ways a tensor differs from a numpy array.
2. You will be able to use autograd to obtain gradients without deriving them, and verify one against the number you computed by hand in Module 5.
3. You will be able to write the canonical training loop — `zero_grad`, forward, loss, `backward`, `step` — from a blank file, in the right order, and explain what breaks if you drop any line.
4. You will be able to build a network as an `nn.Module` subclass and as an `nn.Sequential`, and show they have identical parameters.
5. You will be able to load data with `Dataset` and `DataLoader`, and compute how many optimizer steps an epoch contains.
6. You will be able to save weights with `torch.save`, reload them in a fresh process, and ship a `predict.py` that imports no training code.

---

## 🪝 The Hook

Last module you wrote seven lines of backprop by hand, checked them numerically, and got 99.2% on `make_moons`. That worked because the network had exactly two layers and one activation.

Now imagine deriving those gradients for a fifty-layer network with skip connections, batch normalisation, attention heads, and a custom loss. People did that, by hand, in the 1990s. It took months and the derivations were usually wrong. That is a real reason deep learning was slow to arrive: **the maths was correct but the engineering was unbearable.**

Then someone had the idea that changed everything. Don't derive gradients. Instead, **record every operation as it happens** — a graph of what multiplied what — and walk that graph backwards afterwards, applying the same five chain-rule rules you already know, automatically, for any network anyone can write.

That's autograd. It means the model in your head and the model in your code become the same thing. You write the forward pass; the backward pass writes itself. In this module you will confirm that PyTorch's autograd produces `−0.099750` for the exact weight you computed by hand last module — and then you'll use it to train a network you would never want to differentiate manually.

---

## 🧠 The Concept

### 1. Tensors: dtypes, shapes, and device placement

> **Tensor:** PyTorch's array type. Like a numpy array, but with two superpowers — it can live on a GPU, and it can remember how it was computed.

Everything you know about numpy shapes transfers directly. `torch.zeros(2, 3)` is a 2×3 array of zeros. `@` is matrix multiply. Broadcasting works the same way.

🍕 **Analogy.** A numpy array is a notebook page of numbers. A tensor is the same page, but with two extra things stapled to it: an address label saying which machine it lives on, and a receipt listing everything that was done to produce it.

**Three things that trip people up:**

| Gotcha | What happens | Fix |
|---|---|---|
| Default float is **float32**, not float64 | `torch.zeros(3).dtype` is `torch.float32`, numpy's is `float64` | Cast explicitly: `torch.tensor(arr, dtype=torch.float32)` |
| `torch.tensor([1,2,3])` gives **int64** | Feeding ints to `nn.Linear` raises a dtype error | Use `[1.0, 2.0, 3.0]` or `dtype=torch.float32` |
| Tensors on different devices cannot be combined | `RuntimeError: Expected all tensors to be on the same device` | Move both with `.to(device)` |

> **Device:** where a tensor's numbers physically live. `cpu` always works. `cuda` is an NVIDIA GPU. `mps` is Apple Silicon's GPU.

The standard device-picking idiom, which you should paste into every PyTorch file you write:

```python
if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
```

🔢 **Tiny concrete example.** `torch.from_numpy(arr)` **shares memory** with the numpy array; `torch.tensor(arr)` **copies** it.

```
npy = [[1.0, 2.0], [3.0, 4.0]]
shared = torch.from_numpy(npy)
copied = torch.tensor(npy)

npy[0][0] = 99.0

shared[0][0]  →  99.0     ← changed underneath you
copied[0][0]  →   1.0     ← safe
```

That difference has caused a great many confusing bugs. When in doubt, copy.

**Why bother with a GPU?** A GPU has thousands of small cores instead of a handful of fast ones, which is perfect for the huge matrix multiplies a neural network is made of. For `make_moons` with 750 rows, a GPU is *slower* than the CPU — moving the data costs more than the arithmetic saves. For FashionMNIST with 60,000 images it's several times faster. For a real image model it's the difference between an hour and a week.

---

### 2. Autograd: requires_grad, the graph, .backward(), and zero_grad

> **`requires_grad=True`:** tells PyTorch "this tensor is a parameter I want gradients for — start recording."

> **Computation graph:** the record PyTorch builds as you do arithmetic on tracked tensors. Every operation adds a node that knows how to compute its own local derivative.

> **`.backward()`:** walks that graph backwards from a scalar loss, applying the chain rule, and *adds* the result into each tracked tensor's `.grad` attribute.

🍕 **Analogy.** Autograd is a receipt printer. Every time you multiply, add, or apply an activation, it prints a line: "took *this*, did *that*, produced *this*." At the end you call `.backward()` and it reads the receipt from the bottom up, working out how much each original ingredient contributed to the final bill. You never wrote the accounting rules; you just did the shopping.

🔢 **The smallest possible example.**

```python
x = torch.tensor(3.0, requires_grad=True)
y = x ** 2
y.backward()
x.grad        # tensor(6.)
```

The derivative of `x²` is `2x`, and `2 × 3 = 6`. Autograd got it exactly, without you telling it the power rule. Compare with Module 4, where you estimated this same slope numerically as `6.0` by nudging.

**The one rule that will bite you: `.grad` accumulates.** Calling `.backward()` three times without clearing in between gives you three times the gradient:

```
pass 1: W1.grad[0,0] = -0.099750
pass 2: W1.grad[0,0] = -0.199501     ← 2×
pass 3: W1.grad[0,0] = -0.299251     ← 3×
```

This is intentional — it lets you sum gradients over several small batches when a big batch won't fit in memory. But it means **every training loop must start with `optimizer.zero_grad()`**, and forgetting it is the single most common PyTorch bug in existence.

🔢 **What forgetting it actually costs** (make_moons, 16 hidden units, `lr = 0.5`, 1000 epochs):

| | Final train loss | Test accuracy | Final gradient norm |
|---|---|---|---|
| With `zero_grad()` | **0.0760** | **0.9880** | 0.0073 |
| Without | 1.6981 | 0.6280 | 4.6746 |

Without zeroing, the "gradient" at epoch 1000 is the sum of a thousand gradients. The effective learning rate grows without bound, the model thrashes, and accuracy falls 36 points. And notice: **no error is raised.** The code runs perfectly and gives you a bad model. That's what makes it dangerous.

> **`torch.no_grad()`:** a context manager that turns off graph recording. Use it for every evaluation and inference pass. It is faster, uses less memory, and prevents accidental gradient tracking.

---

### 3. nn.Module, nn.Linear, and nn.Sequential

You could keep writing raw tensors with `requires_grad=True`, but PyTorch gives you containers.

> **`nn.Linear(in_features, out_features)`:** one fully connected layer. Holds a weight matrix and a bias, both already `requires_grad=True`, both already sensibly initialised.

⚠️ **Shape warning.** `nn.Linear(2, 16)` stores its weight with shape `(16, 2)` — **output rows, input columns** — the transpose of your Module 5 `W1`. It computes `x @ W.T + b`, which produces the same result. Don't panic when the shape looks flipped.

> **`nn.Sequential(...)`:** chains layers in order. Great for straight pipelines.
> **`nn.Module` subclass:** you write `__init__` (declare layers) and `forward` (say how data flows). Needed for anything with branches, skips, or reuse.

Two ways to write the exact same network:

```python
# style A — Sequential
model = nn.Sequential(
    nn.Linear(2, 16),
    nn.ReLU(),
    nn.Linear(16, 1),
)

# style B — Module subclass
class MoonNet(nn.Module):
    def __init__(self, hidden=16):
        super().__init__()                    # never forget this line
        self.fc1 = nn.Linear(2, hidden)
        self.fc2 = nn.Linear(hidden, 1)

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))
```

Both have exactly **65** parameters — the same count you computed by hand in Module 5's answer key (`4h + 1 = 4(16) + 1 = 65`). With the same manual seed they produce byte-identical weights.

🍕 **Analogy.** `nn.Sequential` is an assembly line: one belt, boxes go in one end and out the other. An `nn.Module` subclass is a factory floor plan — you can route a part to two stations at once, or send it back around. Use the belt until you need the floor plan.

**Call the model, don't call `.forward()`.** Write `model(x)`, not `model.forward(x)`. The `__call__` wrapper runs hooks that some layers depend on.

---

### 4. Loss functions and optimizers

PyTorch ships the losses you derived by hand.

| Loss | Use for | Expects | Note |
|---|---|---|---|
| `nn.BCEWithLogitsLoss()` | Binary classification | **Raw logits** + float targets `(n,1)` | Applies sigmoid internally, stably |
| `nn.BCELoss()` | Binary classification | Probabilities in (0,1) | Avoid — less numerically stable |
| `nn.CrossEntropyLoss()` | Multi-class | **Raw logits** `(n,K)` + int64 class indices `(n,)` | Applies softmax internally |
| `nn.MSELoss()` | Regression | Predictions and targets | Module 4's squared error |

⚠️ **The trap that catches everyone once.** `CrossEntropyLoss` and `BCEWithLogitsLoss` both apply the squash *for you*. If you put a `nn.Sigmoid()` or `nn.Softmax()` at the end of your model **and** use these losses, you have squashed twice. Training will be sluggish and your accuracy will be mysteriously mediocre. Your model's last layer should be a bare `nn.Linear`.

🔢 **CrossEntropyLoss, verified by hand.** Logits `[2.0, 1.0, 0.1]`, true class 0.

```
softmax: e^2.0 = 7.389056, e^1.0 = 2.718282, e^0.1 = 1.105171
         sum   = 11.212509
         p     = [0.6590, 0.2424, 0.0986]

L = −ln(p₀) = −ln(0.6590) = 0.417030
```
PyTorch's `nn.CrossEntropyLoss()(logits, target)` returns **0.4170299**. Same number, same formula you derived in Module 5's softmax exercise.

> **Optimizer:** the object that owns your parameters and applies the update rule. You hand it `model.parameters()` once; after that, `.step()` updates everything.

| Optimizer | Update | When to use |
|---|---|---|
| `SGD(params, lr=0.5)` | `w ← w − lr·g` | Exactly Module 4's rule |
| `SGD(params, lr=0.5, momentum=0.9)` | Adds velocity | Almost always better than plain SGD |
| `Adam(params, lr=1e-3)` | Per-parameter adaptive step | The safe default for a new problem |

> **Adam:** keeps a running average of each parameter's gradient *and* of its squared gradient, then scales each parameter's step by its own recent gradient size. Parameters with tiny gradients get bigger steps; noisy ones get smaller steps. You get away with far less learning-rate tuning.

🔢 **Real numbers** (make_moons, 60 epochs, batch size 64):

| Optimizer | Final train loss | Test accuracy | Epochs to reach loss < 0.10 |
|---|---|---|---|
| `SGD(lr=0.5)` | 0.0854 | 0.9920 | 40 |
| `SGD(lr=0.5, momentum=0.9)` | 0.0674 | 0.9880 | **6** |
| `Adam(lr=0.01)` | 0.0877 | 0.9880 | 45 |

Momentum reached the target in **6 epochs instead of 40** — nearly seven times faster to the same place. Adam wasn't faster here, but Adam's real value is that `lr=1e-3` works on almost any problem out of the box, whereas plain SGD needs the learning-rate hunt you did in Module 4.

---

### 5. Dataset, DataLoader, batching, epochs vs steps

Module 4 introduced mini-batches conceptually. PyTorch gives you the machinery.

> **`Dataset`:** an object that answers two questions — `__len__()` (how many examples?) and `__getitem__(i)` (give me example `i` as a `(features, label)` pair).
>
> **`DataLoader`:** wraps a Dataset and hands you shuffled batches, one at a time, in a `for` loop.

```
┌──────────┐   __getitem__(i)   ┌────────────┐   for xb, yb in ...   ┌───────────┐
│  Dataset │ ─────────────────▶ │ DataLoader │ ────────────────────▶ │  training │
│  1000    │   one item at a    │  shuffles, │   batches of 64       │   loop    │
│  items   │   time             │  collates  │                       │           │
└──────────┘                    └────────────┘                       └───────────┘
```

For data that already fits in memory as tensors, `TensorDataset(X, y)` does the job in one line. Write your own `Dataset` subclass when items need loading or transforming individually — image files, for instance, which is exactly Module 7.

> **Epoch:** one full pass over the training set.
> **Step (iteration):** one optimizer update — one batch.

🔢 **Do the arithmetic.** 750 training rows, `batch_size=64`:

```
ceil(750 / 64) = 12 batches per epoch
  batches 0–10 have 64 rows each  = 704
  batch 11 has the leftover 750 − 704 = 46 rows
30 epochs × 12 batches = 360 optimizer steps
```

This is why comparing "50 epochs of batch size 32" against "50 epochs of batch size 512" is meaningless — the first took 16× more steps. **Always report steps, or report both.**

`shuffle=True` matters more than it looks. If your data is sorted by label, an unshuffled loader gives the model a hundred batches of class 0, then a hundred of class 1, and the model just learns to predict whatever it saw most recently. Shuffle the training loader. Never shuffle the validation or test loader — you want reproducible order.

---

### 6. Saving, loading, model.eval(), and inference

> **`state_dict()`:** a plain dictionary mapping parameter names to tensors. It is the model's *weights*, not the model's *code*.

```python
torch.save(model.state_dict(), "model.pt")                    # save

model = MoonNet(hidden=16)                                    # rebuild the shape
model.load_state_dict(torch.load("model.pt", map_location="cpu"))
model.eval()                                                  # inference mode
```

You must **construct the same architecture first**. The file holds numbers, not structure. That is a feature: the file is small, portable across machines, and can't execute arbitrary code the way a pickled whole model can.

🍕 **Analogy.** A `state_dict` is a set of tuning-peg positions for a guitar. It's useless without a guitar of the same shape, and it's exactly what you need if you already have one.

> **`model.eval()`:** switches layers that behave differently at test time — **dropout** turns off, **batch normalisation** uses its stored running statistics instead of the current batch's. Forgetting it means your inference results are randomly wrong and hard to reproduce.
>
> **`model.train()`:** switches them back. Call it at the top of every training epoch.

The two together, always:

```python
model.eval()
with torch.no_grad():
    preds = model(X_new)
model.train()      # if you're going back to training
```

`eval()` and `no_grad()` do different jobs and you need both: `eval()` changes layer behaviour, `no_grad()` stops graph recording.

**The canonical training loop.** Memorise this shape. Everything else in this level and Level 4 is a variation on it:

```python
for epoch in range(n_epochs):
    model.train()
    for xb, yb in train_loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()          # 1. clear last step's gradients
        logits = model(xb)             # 2. forward
        loss = loss_fn(logits, yb)     # 3. score
        loss.backward()                # 4. autograd fills .grad
        optimizer.step()               # 5. w ← w − lr·g

    model.eval()
    with torch.no_grad():
        for xb, yb in val_loader:
            ...                        # measure, never update
```

Five lines in the inner loop, always in that order. Compare it to the Module 5 skeleton: `forward → loss → backward → update`. It is the *same loop*. PyTorch replaced your hand-derived `backward()` with `loss.backward()` and your parameter loop with `optimizer.step()`. Nothing conceptual changed.

---

## 🔍 Worked Example

**Claim:** PyTorch's autograd produces exactly the gradients you derived by hand in Module 5.

We'll set up the identical network — same weights, same input, same label — and compare every number.

### The setup (identical to Module 5's Worked Example)

```
W1 = [ 0.5  -0.3 ]     b1 = [ 0.1  0.05 ]
     [ 0.8   0.2 ]

W2 = [  1.0 ]          b2 = [ 0.3 ]
     [ -2.0 ]

x = [1.0, 2.0]         y = 1
```

Module 5 computed, by hand:

```
Z1 = [2.20, 0.15]      A1 = [2.20, 0.15]      Z2 = 2.20
A2 = 0.900250          loss = 0.105083

dZ2 = −0.099750
dW2 = [−0.219451, −0.014963]        db2 = −0.099750
dW1 = [ −0.099750   0.199501 ]      db1 = [−0.099750, 0.199501]
      [ −0.199501   0.399002 ]
```

### Step 1 — Build it in PyTorch

```python
import torch

W1 = torch.tensor([[0.5, -0.3], [0.8, 0.2]], requires_grad=True)
b1 = torch.tensor([[0.1, 0.05]],             requires_grad=True)
W2 = torch.tensor([[1.0], [-2.0]],           requires_grad=True)
b2 = torch.tensor([[0.3]],                   requires_grad=True)

xin   = torch.tensor([[1.0, 2.0]])
ytrue = torch.tensor([[1.0]])
```

Four parameters marked `requires_grad=True`. The input and label are **not** marked — we don't want gradients with respect to the data.

### Step 2 — Forward pass (builds the graph)

```python
Z1 = xin @ W1 + b1
A1 = torch.relu(Z1)
Z2 = A1 @ W2 + b2
A2 = torch.sigmoid(Z2)
loss = -(ytrue * torch.log(A2) + (1 - ytrue) * torch.log(1 - A2)).mean()
```

Four lines, character-for-character the same as your NumPy `forward()` with `np.` swapped for `torch.`. But behind the scenes PyTorch built a graph:

```
xin ──▶[matmul]──▶[add b1]──▶ Z1 ──▶[relu]──▶ A1 ──▶[matmul]──▶[add b2]──▶ Z2
        ▲            ▲                                  ▲          ▲
        W1           b1                                 W2         b2

Z2 ──▶[sigmoid]──▶ A2 ──▶[log, mul, mean, neg]──▶ loss
```

Running it:
```
A2   = 0.9002495
loss = 0.10508329
```
Module 5's hand arithmetic gave `A2 = 0.900250`, `loss = 0.105083`. Match. ✅

### Step 3 — One line replaces your entire backward function

```python
loss.backward()
```

That's it. PyTorch walks the graph backwards, applying at each node exactly the five rules you wrote out in Module 5. It fills in `.grad` on all four parameter tensors.

### Step 4 — Compare, number by number

```python
print("dW1 =\n", W1.grad)
print("db1 =",  b1.grad)
print("dW2 =",  W2.grad.reshape(-1))
print("db2 =",  b2.grad)
```

```
dW1 =
 tensor([[-0.0998,  0.1995],
        [-0.1995,  0.3990]])
db1 = tensor([[-0.0998,  0.1995]])
dW2 = tensor([-0.2195, -0.0150])
db2 = tensor([[-0.0998]])
```

Side by side:

| Quantity | Module 5, by hand | PyTorch autograd | Match? |
|---|---|---|---|
| `A2` | 0.900250 | 0.9002495 | ✅ |
| loss | 0.105083 | 0.1050833 | ✅ |
| `dW1[0][0]` | −0.099750 | −0.09975046 | ✅ |
| `dW1[0][1]` | +0.199501 | +0.1995010 | ✅ |
| `dW1[1][0]` | −0.199501 | −0.1995009 | ✅ |
| `dW1[1][1]` | +0.399002 | +0.3990019 | ✅ |
| `db1` | `[−0.099750, +0.199501]` | `[−0.0997505, +0.1995010]` | ✅ |
| `dW2` | `[−0.219451, −0.014963]` | `[−0.2194511, −0.0149626]` | ✅ |
| `db2` | −0.099750 | −0.0997505 | ✅ |

Every single one. The differences are in the seventh decimal place and come from float32 versus float64, not from any disagreement about the maths.

**You now have proof.** Autograd is not a black box performing unknown magic. It is doing precisely the calculus you did by hand, on a graph it recorded for you, and it will keep doing it correctly no matter how complicated your forward pass gets.

### Step 5 — Watch the accumulation trap

Run the same forward-and-backward three more times without clearing:

```python
W1.grad.zero_(); b1.grad.zero_(); W2.grad.zero_(); b2.grad.zero_()

for i in range(3):
    Z1 = xin @ W1 + b1
    A1 = torch.relu(Z1)
    A2 = torch.sigmoid(A1 @ W2 + b2)
    loss = -(ytrue * torch.log(A2) + (1 - ytrue) * torch.log(1 - A2)).mean()
    loss.backward()
    print(f"pass {i+1}: W1.grad[0,0] = {W1.grad[0,0].item():.6f}")
```

```
pass 1: W1.grad[0,0] = -0.099750
pass 2: W1.grad[0,0] = -0.199501
pass 3: W1.grad[0,0] = -0.299251
```

Exactly 1×, 2×, 3× the true gradient. Nothing crashed. No warning. If this were inside a training loop, your effective learning rate would grow linearly forever and you would spend an afternoon wondering why the loss is chaotic. **That is why `optimizer.zero_grad()` is line one.**

---

## 💻 Hands-On

```bash
pip install torch torchvision numpy scikit-learn matplotlib
```

If `pip install torch` gives trouble, use Google Colab — PyTorch is preinstalled and you get a free GPU under Runtime → Change runtime type.

---

### Step 1 — Tensor basics

Create `tensors.py`:

```python
import numpy as np
import torch

print("torch version:", torch.__version__)

a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
print("\na =\n", a)
print("shape:", tuple(a.shape), " dtype:", a.dtype, " device:", a.device)

print("\nint tensor dtype :", torch.tensor([1, 2, 3]).dtype)
print("zeros(2,3) dtype :", torch.zeros(2, 3).dtype)
print("float64 -> ", torch.tensor([1.0], dtype=torch.float64).dtype)

npy = np.array([[1.0, 2.0], [3.0, 4.0]])
shared = torch.from_numpy(npy)      # SHARES memory with npy
copied = torch.tensor(npy)          # COPIES the data
npy[0, 0] = 99.0
print("\nafter npy[0,0] = 99:")
print("  from_numpy sees  :", shared[0, 0].item())
print("  torch.tensor sees:", copied[0, 0].item())

if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
print("\nchosen device:", device)

b = a.to(device)
print("a.device:", a.device, "  b.device:", b.device)
print("a @ a.T =\n", a @ a.T)

try:
    a + b
except RuntimeError as e:
    print("\nmixing devices raises:", str(e)[:70], "...")
```

Expected output on an Apple Silicon Mac:

```
torch version: 2.2.1

a =
 tensor([[1., 2.],
        [3., 4.]])
shape: (2, 2)  dtype: torch.float32  device: cpu

int tensor dtype : torch.int64
zeros(2,3) dtype : torch.float32
float64 ->  torch.float64

after npy[0,0] = 99:
  from_numpy sees  : 99.0
  torch.tensor sees: 1.0

chosen device: mps
a.device: cpu   b.device: mps:0
a @ a.T =
 tensor([[ 5., 11.],
        [11., 25.]])

mixing devices raises: Expected all tensors to be on the same device, but found at least two  ...
```

On a CPU-only machine, `device` prints `cpu`, `b.device` prints `cpu`, and the last block prints nothing because `a + b` succeeds — both are already on the same device. That is correct behaviour, not a failure.

---

### Step 2 — Autograd, verified against your Module 5 hand-derivation

Create `autograd_check.py`:

```python
import torch

# --- the simplest possible case ---
x = torch.tensor(3.0, requires_grad=True)
y = x ** 2
y.backward()
print("d(x^2)/dx at x=3 :", x.grad.item(), " (calculus says 2*3 = 6)")

# --- the exact network from Module 5's Worked Example ---
W1 = torch.tensor([[0.5, -0.3], [0.8, 0.2]], requires_grad=True)
b1 = torch.tensor([[0.1, 0.05]],             requires_grad=True)
W2 = torch.tensor([[1.0], [-2.0]],           requires_grad=True)
b2 = torch.tensor([[0.3]],                   requires_grad=True)

xin   = torch.tensor([[1.0, 2.0]])
ytrue = torch.tensor([[1.0]])

Z1 = xin @ W1 + b1
A1 = torch.relu(Z1)
Z2 = A1 @ W2 + b2
A2 = torch.sigmoid(Z2)
loss = -(ytrue * torch.log(A2) + (1 - ytrue) * torch.log(1 - A2)).mean()

print("\nforward: A2 =", A2.item(), " loss =", loss.item())

loss.backward()
print("dW1 =\n", W1.grad)
print("db1 =", b1.grad)
print("dW2 =", W2.grad.reshape(-1))
print("db2 =", b2.grad)
print("\nModule 5 hand value dW1[0,0] = -0.099750")
print("autograd            dW1[0,0] =", W1.grad[0, 0].item())

# --- the accumulation trap ---
W1.grad.zero_(); b1.grad.zero_(); W2.grad.zero_(); b2.grad.zero_()
print()
for i in range(3):
    Z1 = xin @ W1 + b1
    A1 = torch.relu(Z1)
    A2 = torch.sigmoid(A1 @ W2 + b2)
    loss = -(ytrue * torch.log(A2) + (1 - ytrue) * torch.log(1 - A2)).mean()
    loss.backward()
    print(f"pass {i+1}: W1.grad[0,0] = {W1.grad[0, 0].item():.6f}")

with torch.no_grad():
    z = xin @ W1
print("\ninside no_grad, output requires_grad?", z.requires_grad)
```

Expected output:

```
d(x^2)/dx at x=3 : 6.0  (calculus says 2*3 = 6)

forward: A2 = 0.9002495408058167  loss = 0.10508328676223755
dW1 =
 tensor([[-0.0998,  0.1995],
        [-0.1995,  0.3990]])
db1 = tensor([[-0.0998,  0.1995]])
dW2 = tensor([-0.2195, -0.0150])
db2 = tensor([[-0.0998]])

Module 5 hand value dW1[0,0] = -0.099750
autograd            dW1[0,0] = -0.09975045919418335

pass 1: W1.grad[0,0] = -0.099750
pass 2: W1.grad[0,0] = -0.199501
pass 3: W1.grad[0,0] = -0.299251

inside no_grad, output requires_grad? False
```

This is the moment PyTorch stops being magic. It matched your hand calculus to seven decimal places, and it showed you exactly how it breaks if you forget to zero.

---

### Step 3 — Same brain, real framework

Create `moons_torch.py`. This rebuilds the Module 5 network with PyTorch doing the derivatives.

```python
import numpy as np
import torch
import torch.nn as nn
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

torch.manual_seed(0)

X, y = make_moons(n_samples=1000, noise=0.20, random_state=42)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25,
                                      stratify=y, random_state=42)
sc = StandardScaler().fit(Xtr)                    # fit on train only

Xtr_t = torch.tensor(sc.transform(Xtr), dtype=torch.float32)
Xte_t = torch.tensor(sc.transform(Xte), dtype=torch.float32)
ytr_t = torch.tensor(ytr, dtype=torch.float32).reshape(-1, 1)
yte_t = torch.tensor(yte, dtype=torch.float32).reshape(-1, 1)

# NOTE: no sigmoid at the end — BCEWithLogitsLoss applies it internally
model = nn.Sequential(
    nn.Linear(2, 16),
    nn.ReLU(),
    nn.Linear(16, 1),
)
loss_fn = nn.BCEWithLogitsLoss()
opt = torch.optim.SGD(model.parameters(), lr=0.5)

print("parameters:", sum(p.numel() for p in model.parameters()))
for name, p in model.named_parameters():
    print(f"  {name:<14} {tuple(p.shape)}")
print()

for epoch in range(3001):
    model.train()
    opt.zero_grad()                    # 1
    logits = model(Xtr_t)              # 2
    loss = loss_fn(logits, ytr_t)      # 3
    loss.backward()                    # 4
    opt.step()                         # 5

    if epoch % 500 == 0:
        model.eval()
        with torch.no_grad():
            val_loss = loss_fn(model(Xte_t), yte_t).item()
            acc = ((torch.sigmoid(model(Xte_t)) >= 0.5).float()
                   == yte_t).float().mean().item()
        print(f"epoch {epoch:>5}  train loss {loss.item():.4f}  "
              f"val loss {val_loss:.4f}  val acc {acc:.4f}")

model.eval()
with torch.no_grad():
    acc = ((torch.sigmoid(model(Xte_t)) >= 0.5).float() == yte_t).float().mean().item()
print("\nfinal test accuracy:", round(acc, 4))
print("Module 5 NumPy brain got:  0.9920")
```

Expected output:

```
parameters: 65
  0.weight       (16, 2)
  0.bias         (16,)
  2.weight       (1, 16)
  2.bias         (1,)

epoch     0  train loss 0.6652  val loss 0.6072  val acc 0.9120
epoch   500  train loss 0.0977  val loss 0.0639  val acc 0.9880
epoch  1000  train loss 0.0760  val loss 0.0437  val acc 0.9880
epoch  1500  train loss 0.0714  val loss 0.0378  val acc 0.9880
epoch  2000  train loss 0.0698  val loss 0.0356  val acc 0.9880
epoch  2500  train loss 0.0687  val loss 0.0340  val acc 0.9880
epoch  3000  train loss 0.0682  val loss 0.0332  val acc 0.9920

final test accuracy: 0.992
Module 5 NumPy brain got:  0.9920
```

**Identical.** 65 parameters, same architecture, same final loss to three decimals (0.0682 vs Module 5's 0.0669 — the tiny gap is PyTorch's default initialization differing from your He init), same 99.2% test accuracy. The two implementations are the same model.

Look at the parameter shapes: `0.weight` is `(16, 2)`, the transpose of your NumPy `W1` which was `(2, 16)`. PyTorch computes `x @ W.T + b`. Same arithmetic, different storage convention.

---

### Step 4 — Dataset, DataLoader, and save/load

Create `data_and_save.py`:

```python
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler


class MoonsDataset(Dataset):
    """The minimum viable Dataset: __len__ and __getitem__."""

    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32).reshape(-1, 1)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, i):
        return self.X[i], self.y[i]


X, y = make_moons(n_samples=1000, noise=0.20, random_state=42)
X = StandardScaler().fit_transform(X)

ds = MoonsDataset(X, y)
print("len(ds) =", len(ds))
xb, yb = ds[0]
print("one item:", xb, yb)

train_ds, val_ds = random_split(ds, [750, 250],
                                generator=torch.Generator().manual_seed(0))
print("split sizes:", len(train_ds), len(val_ds))

loader = DataLoader(train_ds, batch_size=64, shuffle=True)
print("batches per epoch:", len(loader))
for i, (xb, yb) in enumerate(loader):
    print(f"  batch {i}: x {tuple(xb.shape)}  y {tuple(yb.shape)}")
    if i == 2:
        break
print("last batch size:", 750 % 64)

torch.manual_seed(0)
model = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 1))
opt = torch.optim.Adam(model.parameters(), lr=0.01)
loss_fn = nn.BCEWithLogitsLoss()

steps = 0
for epoch in range(30):
    model.train()
    for xb, yb in loader:
        opt.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        opt.step()
        steps += 1
print(f"30 epochs x {len(loader)} batches = {steps} optimizer steps")

torch.save(model.state_dict(), "moons_mlp.pt")
print("saved keys:", list(torch.load("moons_mlp.pt", map_location="cpu").keys()))

# rebuild the SAME architecture, then load numbers into it
fresh = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 1))
fresh.load_state_dict(torch.load("moons_mlp.pt", map_location="cpu"))
fresh.eval()

with torch.no_grad():
    p_orig = torch.sigmoid(model(ds.X))
    p_load = torch.sigmoid(fresh(ds.X))
print("max prediction difference after reload:", float((p_orig - p_load).abs().max()))
print("accuracy:", round(float(((p_load >= 0.5).float() == ds.y).float().mean()), 4))
```

Expected output:

```
len(ds) = 1000
one item: tensor([-0.6848,  0.5204]) tensor([1.])
split sizes: 750 250
batches per epoch: 12
  batch 0: x (64, 2)  y (64, 1)
  batch 1: x (64, 2)  y (64, 1)
  batch 2: x (64, 2)  y (64, 1)
last batch size: 46
30 epochs x 12 batches = 360 optimizer steps
saved keys: ['0.weight', '0.bias', '2.weight', '2.bias']
max prediction difference after reload: 0.0
accuracy: 0.963
```

**Max prediction difference: exactly 0.0.** The reloaded model is bit-for-bit the original. That is the guarantee you need before you ship an artifact.

Note `last batch size: 46` — `750 = 11 × 64 + 46`. If a smaller final batch ever causes trouble (it can with batch normalisation), pass `drop_last=True` to the DataLoader.

---

### Step 5 — FashionMNIST: a real dataset, a real training loop

Create `train_fashion.py`. This downloads about 30 MB the first time and trains in roughly 3–6 minutes on a laptop CPU, faster on a GPU.

```python
"""Train a 3-layer MLP on FashionMNIST. Saves weights + a loss plot."""
import time
import torch
import torch.nn as nn
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

torch.manual_seed(0)

if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
print("device:", device)

# FashionMNIST's channel mean and std, precomputed by the community
tf = transforms.Compose([
    transforms.ToTensor(),                        # uint8 [0,255] -> float [0,1], shape (1,28,28)
    transforms.Normalize((0.2860,), (0.3530,)),   # standardise, same idea as Module 2
])

full_train = datasets.FashionMNIST(root="./data", train=True,  download=True, transform=tf)
test_set   = datasets.FashionMNIST(root="./data", train=False, download=True, transform=tf)

train_set, val_set = random_split(full_train, [55000, 5000],
                                  generator=torch.Generator().manual_seed(0))
print(f"train {len(train_set)}  val {len(val_set)}  test {len(test_set)}")

train_loader = DataLoader(train_set, batch_size=128, shuffle=True)
val_loader   = DataLoader(val_set,   batch_size=256, shuffle=False)
test_loader  = DataLoader(test_set,  batch_size=256, shuffle=False)
print("steps per epoch:", len(train_loader))


class FashionMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),            # (B,1,28,28) -> (B,784)
            nn.Linear(784, 256), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(256, 128), nn.ReLU(),
            nn.Linear(128, 10),      # raw logits — CrossEntropyLoss squashes
        )

    def forward(self, x):
        return self.net(x)


model = FashionMLP().to(device)
print("parameters:", sum(p.numel() for p in model.parameters()))

loss_fn = nn.CrossEntropyLoss()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)


def evaluate(loader):
    model.eval()
    total_loss, correct, n = 0.0, 0, 0
    with torch.no_grad():
        for xb, yb in loader:
            xb, yb = xb.to(device), yb.to(device)
            logits = model(xb)
            total_loss += loss_fn(logits, yb).item() * len(xb)
            correct += (logits.argmax(1) == yb).sum().item()
            n += len(xb)
    return total_loss / n, correct / n


EPOCHS = 12
train_hist, val_hist = [], []
t0 = time.time()

for epoch in range(1, EPOCHS + 1):
    model.train()
    running, n = 0.0, 0
    for xb, yb in train_loader:
        xb, yb = xb.to(device), yb.to(device)
        opt.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        opt.step()
        running += loss.item() * len(xb)
        n += len(xb)
    train_loss = running / n
    val_loss, val_acc = evaluate(val_loader)
    train_hist.append(train_loss)
    val_hist.append(val_loss)
    print(f"epoch {epoch:>2}  train {train_loss:.4f}  "
          f"val {val_loss:.4f}  val acc {val_acc:.4f}  ({time.time()-t0:.0f}s)")

test_loss, test_acc = evaluate(test_loader)
print(f"\nTEST loss {test_loss:.4f}  TEST accuracy {test_acc:.4f}")

torch.save(model.state_dict(), "fashion_mlp.pt")
print("saved fashion_mlp.pt")

plt.figure(figsize=(7, 4.5))
plt.plot(range(1, EPOCHS + 1), train_hist, marker="o", label="train loss")
plt.plot(range(1, EPOCHS + 1), val_hist,   marker="s", label="validation loss")
plt.xlabel("epoch"); plt.ylabel("cross-entropy loss")
plt.title("FashionMNIST MLP"); plt.legend(); plt.grid(alpha=0.3)
plt.tight_layout(); plt.savefig("fashion_loss.png", dpi=130)
print("wrote fashion_loss.png")
```

Representative output (your exact numbers will differ by a few tenths of a percent depending on hardware and PyTorch version):

```
device: mps
train 55000  val 5000  test 10000
steps per epoch: 430
parameters: 235146
epoch  1  train 0.5546  val 0.4133  val acc 0.8492  (14s)
epoch  2  train 0.4067  val 0.3742  val acc 0.8636  (27s)
epoch  3  train 0.3672  val 0.3494  val acc 0.8736  (40s)
epoch  4  train 0.3428  val 0.3345  val acc 0.8788  (53s)
epoch  5  train 0.3245  val 0.3305  val acc 0.8808  (66s)
epoch  6  train 0.3104  val 0.3237  val acc 0.8836  (79s)
epoch  7  train 0.2986  val 0.3212  val acc 0.8846  (92s)
epoch  8  train 0.2870  val 0.3195  val acc 0.8862  (105s)
epoch  9  train 0.2783  val 0.3186  val acc 0.8874  (118s)
epoch 10  train 0.2694  val 0.3161  val acc 0.8898  (131s)
epoch 11  train 0.2626  val 0.3208  val acc 0.8880  (144s)
epoch 12  train 0.2551  val 0.3186  val acc 0.8894  (157s)

TEST loss 0.3396  TEST accuracy 0.8829
saved fashion_mlp.pt
wrote fashion_loss.png
```

**Read the loss plot, not just the final number.** Training loss falls steadily from 0.55 to 0.26. Validation loss falls to about 0.316 by epoch 10 and then stops — and by epoch 11 it has ticked *up*. That crossing point is the beginning of overfitting: the model is now memorising training images rather than learning clothing. In a production run you would stop at epoch 10 and keep those weights. (Practice exercise 6 makes you build exactly that.)

**Parameter count check:** `784×256 + 256` = 200,960, `256×128 + 128` = 32,896, `128×10 + 10` = 1,290. Total **235,146**. Every parameter accounted for.

---

### Step 6 — `predict.py`: inference with no training code

Create `predict.py`. This is the deliverable. It must import nothing from `train_fashion.py`.

```python
"""Classify one FashionMNIST test image. Usage: python predict.py [index]"""
import sys
import torch
import torch.nn as nn
from torchvision import datasets, transforms

CLASSES = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
           "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]


class FashionMLP(nn.Module):
    """Must match the saved architecture exactly — the file holds numbers only."""

    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(784, 256), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(256, 128), nn.ReLU(),
            nn.Linear(128, 10),
        )

    def forward(self, x):
        return self.net(x)


def load_model(path="fashion_mlp.pt"):
    model = FashionMLP()
    model.load_state_dict(torch.load(path, map_location="cpu"))
    model.eval()                     # dropout OFF — critical
    return model


def predict(model, image_tensor):
    """image_tensor: shape (1, 28, 28), already normalised."""
    with torch.no_grad():
        logits = model(image_tensor.unsqueeze(0))     # add batch dim -> (1,1,28,28)
        probs = torch.softmax(logits, dim=1)[0]
    top = torch.topk(probs, 3)
    return [(CLASSES[i], float(p)) for p, i in zip(top.values, top.indices)]


if __name__ == "__main__":
    index = int(sys.argv[1]) if len(sys.argv) > 1 else 0

    tf = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.2860,), (0.3530,)),
    ])
    test_set = datasets.FashionMNIST(root="./data", train=False,
                                     download=True, transform=tf)
    image, true_label = test_set[index]

    model = load_model()
    top3 = predict(model, image)

    print(f"image index      : {index}")
    print(f"true label       : {CLASSES[true_label]}")
    print(f"predicted        : {top3[0][0]}  ({top3[0][1]*100:.1f}% confident)")
    print(f"correct?         : {top3[0][0] == CLASSES[true_label]}")
    print("top 3:")
    for name, p in top3:
        print(f"   {name:<12} {p*100:6.2f}%")
```

Representative run:

```
$ python predict.py 0
image index      : 0
true label       : Ankle boot
predicted        : Ankle boot  (99.6% confident)
correct?         : True
top 3:
   Ankle boot    99.63%
   Sneaker        0.29%
   Sandal         0.07%

$ python predict.py 12
image index      : 12
true label       : Sandal
predicted        : Sandal  (94.8% confident)
correct?         : True
top 3:
   Sandal        94.81%
   Sneaker        4.72%
   Ankle boot     0.41%
```

Three things make this a real inference script:

1. **No optimizer, no loss function, no training loop.** Grep it — none of those words appear outside a comment.
2. **`model.eval()` before any prediction.** Without it, the `Dropout(0.2)` layer stays active and randomly zeroes 20% of the hidden units, so the same image gives a different answer every run.
3. **The architecture is re-declared here.** That duplication is deliberate: `predict.py` depends only on the `.pt` file, never on the training script. In the Level 3 capstone you will move that shared class into its own small module so both files import it — but the dependency direction stays the same.

---

## ✍️ Practice

### [Warm-up] 1 — Tensor triage

Each snippet below is broken. For each: name the error, explain the cause in one sentence, and give the one-line fix. Then run all three fixed versions.

```python
# (a)
x = torch.tensor([1, 2, 3])
layer = nn.Linear(3, 1)
layer(x)

# (b)
a = torch.randn(3, 4)
b = torch.randn(3, 4)
a @ b

# (c)
X = np.random.rand(10, 5)
model = nn.Linear(5, 1)
model(X)
```

Also answer: what dtype and shape does `torch.zeros(4, 3, 2)` have, and how many elements does `.numel()` report?

**Done looks like:** three error names, three causes, three fixes that run, plus the dtype/shape/numel answer.

---

### [Warm-up] 2 — Autograd versus calculus

(a) For `f(x) = x³ − 4x + 1`, compute `f'(2)` by hand using the power rule, then get it with autograd. They must match.
(b) For `h(a, b) = a·b + b²` at `a = 2, b = 3`, compute both partial derivatives by hand, then with autograd on two tracked tensors.
(c) Call `.backward()` on `h` a second time without zeroing. What happens, and what does the error message (or the doubled gradient) tell you about the computation graph?

**Done looks like:** three hand-computed derivatives, three autograd values matching, and a one-sentence explanation of (c).

---

### [Build] 3 — Sequential to Module subclass

(a) Rewrite `nn.Sequential(nn.Linear(2,16), nn.ReLU(), nn.Linear(16,1))` as a `MoonNet(nn.Module)` subclass with a `hidden` argument.
(b) With `torch.manual_seed(0)` set immediately before constructing each, prove the two have identical parameter counts and byte-identical weights.
(c) Print `named_parameters()` for both and explain why the names differ (`0.weight` versus `fc1.weight`).
(d) Add a `hidden=64` variant and report its parameter count. Verify it equals `4×64 + 1 = 257`... and then explain why it actually doesn't, and what the correct formula is for PyTorch's layout.

**Done looks like:** two model classes, a `torch.equal` check printing `True`, and the corrected parameter formula with arithmetic.

---

### [Build] 4 — Optimizer bake-off

On `make_moons` (standardised, 75/25 stratified, batch size 64, 60 epochs, seed 0), compare:

- `SGD(lr=0.5)`
- `SGD(lr=0.5, momentum=0.9)`
- `Adam(lr=0.01)`

(a) For each, report final training loss, test accuracy, and the first epoch at which training loss dropped below 0.10.
(b) Plot all three training-loss curves on one axes.
(c) Which reached the target fastest, and by what factor?
(d) Now sweep Adam over `lr ∈ {0.01, 0.5, 2.0, 5.0}`. For each, also count dead hidden units with `(torch.relu(m.fc1(Xtr)).max(0).values <= 0).sum()`. State Adam's usable learning-rate range and connect it to Module 4's learning-rate table and Module 5's dead-ReLU table.

**Done looks like:** a three-row results table, one figure, a stated speed-up factor, and a four-row Adam sweep with dead-unit counts.

---

### [Stretch] 5 — Quantify the `zero_grad` bug

(a) Train the `make_moons` MLP twice for 1000 full-batch epochs at `lr = 0.5` — once with `opt.zero_grad()`, once without. Report final training loss, test accuracy, and the L2 norm of the concatenated final gradients for each.
(b) Explain in two sentences why the norm differs so much.
(c) Show that the bug is *invisible* at 200 epochs and *catastrophic* at 1000 by running both lengths.
(d) Write one sentence on why PyTorch chose accumulation as the default rather than auto-zeroing.

**Done looks like:** a 2×2 results table (200 and 1000 epochs × with and without), the two gradient norms, and the two explanations.

---

### [Stretch] 6 — Early stopping with best-checkpoint restore

Your FashionMNIST validation loss bottomed out around epoch 10 and then rose. Build the machinery to catch that automatically.

(a) Implement early stopping: track the best validation loss, `copy.deepcopy` the `state_dict` whenever it improves, and stop after `patience` epochs with no improvement.
(b) Demonstrate it on `make_moons` with `Adam(lr=0.01)`, `patience=20`, and a 500-epoch cap. Report the epoch it stopped at, the best epoch, and the best validation loss.
(c) Restore the best weights and report the test accuracy, alongside the final-epoch validation loss you would have kept without early stopping.
(d) Explain in two sentences why you must `deepcopy` the state dict rather than just keeping a reference.

**Done looks like:** working early-stopping code, the stop/best epoch numbers, two accuracy figures, and the deepcopy explanation.

---

## 🤔 Think Deeper

**1. Autograd means you never have to derive a gradient again. Module 5 made you derive them by hand anyway. Was that a waste of six hours?**

*How to reason about it:* list the things that can go wrong in a PyTorch model where the gradients are computed *correctly* but training still fails — exploding gradients, vanishing gradients, dead ReLUs, a `detach()` in the wrong place silently cutting the graph, a loss that is flat in the region you started from. Ask, for each, whether you could diagnose it without a mental model of what the gradient physically *is*. Then ask the opposite question honestly: how much of Module 5's algebra will you actually remember in two years, and does the intuition survive even if the algebra doesn't?

**2. Your FashionMNIST model hits 88% and you ship it. Six months later a retailer starts photographing clothes on mannequins instead of flat-lay on white. Accuracy quietly falls to 61%. Nobody notices for three weeks. What went wrong, and where?**

*How to reason about it:* separate the model failure from the process failure. The model did nothing wrong — it was never trained on mannequin photos, and no model can be blamed for a distribution it never saw. The real failure is that three weeks passed with nobody knowing. Ask what signal was available *without labels* (prediction confidence distribution, class balance of predictions, input pixel statistics) and what the alerting threshold should have been. This is precisely the monitoring plan you write in the Level 3 capstone, so sketch it now.

**3. The same five lines — `zero_grad, forward, loss, backward, step` — train a 65-parameter moons classifier and a 400-billion-parameter language model. If the algorithm is identical, what actually separates those two systems?**

*How to reason about it:* make a list of everything that is *not* the algorithm — the volume and provenance of the data, the cost of the hardware, the architecture of the layer inside the loop, the number of people who reviewed what went into the training set, and who can afford to run it at all. Then ask which items on that list are engineering problems, which are money problems, and which are governance problems. Notice that "understand gradient descent" appears on none of them — you already have that part, and it is the part that is free.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Loss is chaotic and accuracy is far worse than expected, with no error | Forgot `optimizer.zero_grad()`; gradients accumulate across every step | Make `zero_grad()` the first line of the inner loop, always |
| `RuntimeError: expected scalar type Long but found Float` (or the reverse) | Fed int64 tensors into `nn.Linear`, or float targets into `CrossEntropyLoss` | Features → `dtype=torch.float32`. `CrossEntropyLoss` targets → int64 class indices, shape `(n,)` |
| `RuntimeError: Expected all tensors to be on the same device` | Model was moved with `.to(device)` but a batch wasn't | Move both inside the loop: `xb, yb = xb.to(device), yb.to(device)` |
| Training works, but accuracy caps out mysteriously low | Put `nn.Sigmoid()` or `nn.Softmax()` at the end *and* used `BCEWithLogitsLoss` / `CrossEntropyLoss` | End the model with a bare `nn.Linear`; the loss applies the squash |
| Predictions change every time you run `predict.py` on the same image | Forgot `model.eval()`, so `Dropout` is still randomly zeroing units | Call `model.eval()` right after `load_state_dict`, before any prediction |
| Evaluation is slow and eats memory | Forgot `with torch.no_grad()`, so PyTorch is building a graph you'll never use | Wrap every evaluation and inference block in `torch.no_grad()` |
| `RuntimeError: Trying to backward through the graph a second time` | Called `.backward()` twice on the same loss tensor | Recompute the forward pass each iteration; don't reuse a loss tensor |
| `Missing key(s) in state_dict` on load | The class you rebuilt doesn't exactly match the one you saved from | Keep the model class definition in one place and import it in both scripts |
| Reported "50 epochs" as if two runs were comparable when batch sizes differed | Epochs are passes over data; steps are updates | Report steps, or report batch size alongside epochs |
| Validation loss is lower than training loss and you assume a bug | Dropout is active during training but off during evaluation | Expected with dropout. Compare like with like by also evaluating the training set in `eval()` mode |

---

## 🛠️ Mini-Project — Same Brain, Real Framework

**Goal.** Two deliverables. First, prove your Module 5 network and a PyTorch rebuild are the same model. Second, train a deeper MLP on FashionMNIST past 85% test accuracy and ship a standalone `predict.py`.

**Time.** 90 minutes.

### Part A — Same brain (30 min)

1. Rebuild the Module 5 network in PyTorch as an `nn.Module` subclass: `2 → 16 (ReLU) → 1`, no final sigmoid, `BCEWithLogitsLoss`.
2. Train on the identical `make_moons` split (`n_samples=1000, noise=0.20, random_state=42`, 75/25 stratified, scaler fit on train only) with `SGD(lr=0.5)` for 3000 full-batch epochs.
3. Print the parameter count and confirm it is **65** — the same number you derived by hand in Module 5.
4. Print test accuracy next to Module 5's 0.9920.
5. Reproduce the Worked Example's autograd check: set the four hand-chosen weight values, forward on `x = [1.0, 2.0]` with `y = 1`, `backward()`, and print `W1.grad[0,0]` beside the hand value `−0.099750`.

### Part B — FashionMNIST (60 min)

6. Load FashionMNIST with `ToTensor()` + `Normalize((0.2860,), (0.3530,))`. Split the 60,000 training images into 55,000 train and 5,000 validation with a seeded generator. Keep the 10,000-image test set sealed until the very end (Module 1's rule).
7. Build `784 → 256 (ReLU, Dropout 0.2) → 128 (ReLU) → 10 logits`. Confirm the parameter count is **235,146** by hand arithmetic and by `sum(p.numel() ...)`.
8. Train with `Adam(lr=1e-3)`, `CrossEntropyLoss`, batch size 128, 12 epochs. Record train and validation loss every epoch.
9. Plot both curves on one figure and save `fashion_loss.png`. Mark or note the epoch where validation loss stopped improving.
10. Evaluate on the test set **once**. Save weights with `torch.save(model.state_dict(), "fashion_mlp.pt")`.
11. Write `predict.py` that loads the weights, takes a test-set index on the command line, and prints the true label, the predicted label, and the top-3 probabilities.

### Success criteria checklist

- [ ] Part A prints **65 parameters** and a test accuracy within 1 point of Module 5's 0.9920.
- [ ] The autograd check prints a value matching your hand-derived `−0.099750` to at least 6 decimal places.
- [ ] FashionMNIST test accuracy is **above 85%** (you should see roughly 88%).
- [ ] The parameter count is exactly 235,146, and you show the arithmetic that produces it.
- [ ] `fashion_loss.png` shows both curves, labelled, with a legend and axis labels.
- [ ] `predict.py` runs in a fresh terminal and prints a sensible top-3.
- [ ] `grep -E "optimizer|loss_fn|backward|\.step\(\)|train_loader" predict.py` returns **nothing**.
- [ ] `predict.py` calls `model.eval()`, and running it twice on the same index gives identical probabilities.
- [ ] The test set was evaluated exactly once, after all tuning was finished.

### Level it up

Add a **confusion matrix** to your FashionMNIST evaluation using `sklearn.metrics.confusion_matrix` and a `seaborn` heatmap (Module 3's tooling, applied to 10 classes).

Then answer with evidence: **which two classes does the model confuse most, and does that confusion make sense to a human?** Print the top five off-diagonal cells with their counts. You will almost certainly find *Shirt* being called *T-shirt/top*, *Pullover*, and *Coat* — four garment classes that are genuinely hard to tell apart in a 28×28 greyscale image with no colour and no texture detail.

Finish with the honest engineering conclusion: is the remaining 12% of error a *model* problem or a *data* problem? Write two sentences arguing your side, and name one change to the data that would help more than any change to the architecture. (Module 7 will show you the architectural change that *does* help — but you should form your hypothesis first.)

---

## 🔑 Key Takeaways

- **A tensor is a numpy array with a device and a memory of how it was computed.** Default dtype is float32, not float64, and that difference causes real errors.
- **Autograd computes exactly the gradients you derived by hand.** Verified: `dW1[0,0] = −0.09975046` from PyTorch versus `−0.099750` from your Module 5 arithmetic. It is not magic; it is your chain rule, recorded and replayed.
- **`.grad` accumulates, and forgetting `zero_grad()` raises no error.** With it: 98.8% accuracy. Without: 62.8%. A silent 36-point failure.
- **The canonical loop is five lines in this exact order:** `zero_grad`, forward, loss, `backward`, `step`. It is the same loop you wrote in NumPy, with two lines replaced by library calls.
- **`BCEWithLogitsLoss` and `CrossEntropyLoss` apply the squash internally.** Your model's last layer is a bare `nn.Linear`. Squashing twice is a quiet accuracy killer.
- **Momentum is nearly free speed** — 6 epochs to a target instead of 40 on the same problem. Adam's value is robustness to your learning-rate choice, not raw speed.
- **Epochs are passes; steps are updates.** 750 rows at batch 64 is 12 steps per epoch. Never compare runs by epochs alone.
- **`state_dict` saves numbers, not architecture.** Rebuild the class, load the numbers, call `model.eval()`. Reloaded predictions should differ from the original by exactly 0.0.
- **A real inference script imports no training code**, declares the architecture it needs, and switches the model to eval mode before it predicts anything.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Tensor** | PyTorch's array. Like numpy, but it can live on a GPU and remember its own history | `torch.zeros(2, 3)` |
| **dtype** | What kind of number is in each slot | `torch.float32`, `torch.int64` |
| **Device** | Which chip the numbers physically sit on | `cpu`, `cuda`, `mps` |
| **`requires_grad`** | A flag meaning "track this — I want its gradient" | `torch.tensor(3.0, requires_grad=True)` |
| **Computation graph** | The recording of every operation, used to walk the chain rule backwards | `x → x² → loss` |
| **Autograd** | PyTorch's automatic differentiation engine | `loss.backward()` |
| **`.grad`** | Where autograd puts the gradient it computed | `W1.grad[0,0] = −0.09975` |
| **`zero_grad()`** | Clearing old gradients before computing new ones | First line of the inner loop |
| **`no_grad()`** | "Don't record anything" — for evaluation and inference | `with torch.no_grad(): ...` |
| **`nn.Module`** | The base class for anything with learnable parameters | `class MoonNet(nn.Module)` |
| **`nn.Linear`** | One fully connected layer: weights plus a bias | `nn.Linear(784, 256)` |
| **`nn.Sequential`** | Layers chained in a straight line | `nn.Sequential(fc1, relu, fc2)` |
| **Logit** | The raw score before any squash — same word as Module 4 | Output of the last `nn.Linear` |
| **`BCEWithLogitsLoss`** | Binary log loss that applies the sigmoid for you, stably | Binary classification |
| **`CrossEntropyLoss`** | Multi-class log loss that applies softmax for you | 10-class FashionMNIST |
| **Optimizer** | The object that owns your parameters and applies the update rule | `torch.optim.Adam(...)` |
| **Adam** | An optimizer that adapts the step size per parameter | `Adam(params, lr=1e-3)` |
| **Momentum** | Letting the optimizer build speed downhill | `SGD(..., momentum=0.9)` |
| **`Dataset`** | An object that can say how many items it has and hand you item `i` | `TensorDataset(X, y)` |
| **`DataLoader`** | Turns a Dataset into shuffled batches you can loop over | `DataLoader(ds, batch_size=64)` |
| **Epoch** | One full pass over the training data | 12 epochs |
| **Step / iteration** | One optimizer update, i.e. one batch | 430 steps per epoch |
| **Dropout** | Randomly zeroing some units during training to reduce overfitting | `nn.Dropout(0.2)` |
| **`state_dict`** | A dictionary of parameter names to weight tensors | `{'0.weight': ..., '0.bias': ...}` |
| **`model.eval()`** | Switch to inference behaviour: dropout off, batchnorm frozen | Before any prediction |
| **Early stopping** | Halting training when validation loss stops improving | `patience=20` |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1 — Tensor triage

**(a)**
```python
x = torch.tensor([1, 2, 3])
layer = nn.Linear(3, 1)
layer(x)
```
**Error:** `RuntimeError: mat1 and mat2 must have the same dtype, but got Long and Float`

**Cause:** `torch.tensor([1, 2, 3])` with no decimal points infers **int64** (`Long`). `nn.Linear`'s weights are float32, and PyTorch will not silently mix integer and float in a matrix multiply.

**Fix:**
```python
x = torch.tensor([1.0, 2.0, 3.0])          # or dtype=torch.float32
```

**(b)**
```python
a = torch.randn(3, 4); b = torch.randn(3, 4); a @ b
```
**Error:** `RuntimeError: mat1 and mat2 shapes cannot be multiplied (3x4 and 3x4)`

**Cause:** matrix multiply needs `a`'s column count (4) to equal `b`'s row count (3). They don't match.

**Fix:**
```python
a @ b.T          # (3,4) @ (4,3) -> (3,3)
```

**(c)**
```python
X = np.random.rand(10, 5); model = nn.Linear(5, 1); model(X)
```
**Error:** `TypeError: linear(): argument 'input' (position 1) must be Tensor, not numpy.ndarray`

**Cause:** PyTorch layers take tensors, not numpy arrays. There is no implicit conversion.

**Fix:**
```python
model(torch.tensor(X, dtype=torch.float32))
```
(Note the `dtype`: `np.random.rand` produces float64, and `torch.tensor` would preserve that, giving you a *second* dtype error. Both problems, one line.)

**`torch.zeros(4, 3, 2)`:**
```
dtype  : torch.float32
shape  : torch.Size([4, 3, 2])
numel(): 4 × 3 × 2 = 24
```

---

### 2 — Autograd versus calculus

**(a) `f(x) = x³ − 4x + 1` at `x = 2`.**

By hand:
```
f'(x) = 3x² − 4
f'(2) = 3(4) − 4 = 12 − 4 = 8
```

```python
import torch
x = torch.tensor(2.0, requires_grad=True)
f = x ** 3 - 4 * x + 1
f.backward()
print(x.grad.item())        # 8.0
```
Output: `8.0` ✅

**(b) `h(a, b) = a·b + b²` at `a = 2, b = 3`.**

By hand:
```
∂h/∂a = b        = 3
∂h/∂b = a + 2b   = 2 + 6 = 8
```

```python
a = torch.tensor(2.0, requires_grad=True)
b = torch.tensor(3.0, requires_grad=True)
h = a * b + b ** 2
h.backward()
print(a.grad.item(), b.grad.item())    # 3.0 8.0
```
Output: `3.0 8.0` ✅

**(c) Calling `.backward()` twice on the same `h`.**

```
RuntimeError: Trying to backward through the graph a second time (or directly
access saved tensors after they have already been freed).
```

By default PyTorch **frees the graph** as soon as `.backward()` finishes, because holding intermediate activations is the single biggest memory cost in training and there is normally no reason to keep them. The error tells you that a graph is a one-shot object tied to one specific forward pass: to backward again you must run the forward again (or pass `retain_graph=True`, which you almost never want).

If instead you run the *forward and backward together* twice, no error occurs — you get `a.grad = 6.0`, double the true value, because `.grad` accumulates. That is the silent version of the same lesson and the reason `zero_grad()` exists.

---

### 3 — Sequential to Module subclass

**(a)+(b)**

```python
import torch
import torch.nn as nn


class MoonNet(nn.Module):
    def __init__(self, hidden=16):
        super().__init__()
        self.fc1 = nn.Linear(2, hidden)
        self.fc2 = nn.Linear(hidden, 1)

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))


torch.manual_seed(0); seq = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 1))
torch.manual_seed(0); cls = MoonNet()

print("seq params:", sum(p.numel() for p in seq.parameters()))
print("cls params:", sum(p.numel() for p in cls.parameters()))
print("identical:", torch.equal(seq[0].weight, cls.fc1.weight)
                and torch.equal(seq[0].bias,   cls.fc1.bias)
                and torch.equal(seq[2].weight, cls.fc2.weight)
                and torch.equal(seq[2].bias,   cls.fc2.bias))
```

```
seq params: 65
cls params: 65
identical: True
```

Both have 65 parameters and byte-identical weights, because `torch.manual_seed(0)` was reset immediately before each construction and the layers are created in the same order with the same shapes, so they consume the same random numbers.

**(c) Why the names differ.**

```
seq: 0.weight (16,2) | 0.bias (16,) | 2.weight (1,16) | 2.bias (1,)
cls: fc1.weight (16,2) | fc1.bias (16,) | fc2.weight (1,16) | fc2.bias (1,)
```

`nn.Sequential` names its children by **position index** — the `nn.ReLU()` occupies slot 1, which is why the second linear layer is `2`, not `1` (ReLU has no parameters, so it never appears in `named_parameters()`, but it still holds its slot). An `nn.Module` subclass names children by the **attribute name** you assigned. Attribute names are far better for `state_dict` compatibility: inserting a layer into a `Sequential` renumbers everything after it and breaks every saved checkpoint, whereas adding `self.fc3` leaves `fc1` and `fc2` untouched.

**(d) The parameter count for `hidden=64`.**

```python
print(sum(p.numel() for p in MoonNet(64).parameters()))    # 257
```

Output: **257**. So `4h + 1 = 4(64) + 1 = 257` **is** correct here — the exercise's suggestion that it wouldn't be is the trap, and you should check rather than assume.

Here is the actual arithmetic, because "it happened to work" is not understanding:

```
fc1.weight : (64, 2)  = 128
fc1.bias   : (64,)    =  64
fc2.weight : (1, 64)  =  64
fc2.bias   : (1,)     =   1
                      -----
                        257
```

The general formula for `n_in → h → 1` is `h·n_in + h + h + 1 = h(n_in + 2) + 1`. With `n_in = 2` that is `4h + 1`, matching Module 5. But with `n_in = 784` it would be `786h + 1`, nothing like `4h + 1`. **The `4h + 1` shortcut is specific to two input features.** Note also that PyTorch stores `fc1.weight` as `(64, 2)` — transposed relative to your NumPy `W1` of `(2, 64)` — but `numel()` is identical either way, so the count is unaffected.

---

### 4 — Optimizer bake-off

```python
import torch, torch.nn as nn
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from torch.utils.data import TensorDataset, DataLoader
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class MoonNet(nn.Module):
    def __init__(self, hidden=16):
        super().__init__()
        self.fc1 = nn.Linear(2, hidden); self.fc2 = nn.Linear(hidden, 1)
    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))


X, y = make_moons(n_samples=1000, noise=0.20, random_state=42)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
sc = StandardScaler().fit(Xtr)
Xtr = torch.tensor(sc.transform(Xtr), dtype=torch.float32)
Xte = torch.tensor(sc.transform(Xte), dtype=torch.float32)
ytr = torch.tensor(ytr, dtype=torch.float32).reshape(-1, 1)
yte = torch.tensor(yte, dtype=torch.float32).reshape(-1, 1)

loader = DataLoader(TensorDataset(Xtr, ytr), batch_size=64, shuffle=True,
                    generator=torch.Generator().manual_seed(0))
loss_fn = nn.BCEWithLogitsLoss()

configs = [("SGD lr=0.5",          lambda p: torch.optim.SGD(p, lr=0.5)),
           ("SGD lr=0.5 mom=0.9",  lambda p: torch.optim.SGD(p, lr=0.5, momentum=0.9)),
           ("Adam lr=0.01",        lambda p: torch.optim.Adam(p, lr=0.01))]

plt.figure(figsize=(7, 4.5))
for name, make_opt in configs:
    torch.manual_seed(0)
    m = MoonNet(); opt = make_opt(m.parameters())
    curve, hit = [], None
    for ep in range(60):
        m.train()
        for xb, yb in loader:
            opt.zero_grad(); loss_fn(m(xb), yb).backward(); opt.step()
        m.eval()
        with torch.no_grad():
            tl = loss_fn(m(Xtr), ytr).item()
        curve.append(tl)
        if hit is None and tl < 0.10:
            hit = ep
    with torch.no_grad():
        acc = ((torch.sigmoid(m(Xte)) >= 0.5).float() == yte).float().mean().item()
    print(f"{name:<20} train loss {curve[-1]:.4f}  test acc {acc:.4f}  "
          f"epochs to <0.10: {hit}")
    plt.plot(curve, label=name)

plt.yscale("log"); plt.xlabel("epoch"); plt.ylabel("training loss (log scale)")
plt.title("Optimizer bake-off on make_moons"); plt.legend(); plt.grid(alpha=0.3)
plt.tight_layout(); plt.savefig("optimizers.png", dpi=130)
```

**(a)**

```
SGD lr=0.5           train loss 0.0854  test acc 0.9920  epochs to <0.10: 40
SGD lr=0.5 mom=0.9   train loss 0.0674  test acc 0.9880  epochs to <0.10: 6
Adam lr=0.01         train loss 0.0877  test acc 0.9880  epochs to <0.10: 45
```

**(b)** `optimizers.png` on a log y-axis: the momentum curve plunges almost vertically in the first ten epochs and then flattens lowest; plain SGD and Adam descend at broadly similar, gentler rates and end slightly above it.

**(c)** **Momentum won by a factor of 40/6 ≈ 6.7×.** It reached training loss < 0.10 at epoch 6 versus epoch 40 for plain SGD.

Why: the moons loss surface has a consistent downhill direction with side-to-side wobble. Momentum accumulates velocity along the consistent direction and averages away the wobble. It is one keyword argument and it cost nothing.

Note that all three land within 0.4 accuracy points of each other. On an easy convex-ish problem the optimizer choice affects *how fast* you arrive, not *where* you arrive.

**(d) The Adam learning-rate sweep.**

```python
for lr in (0.01, 0.5, 2.0, 5.0):
    torch.manual_seed(0)
    m = MoonNet(); opt = torch.optim.Adam(m.parameters(), lr=lr)
    for ep in range(60):
        m.train()
        for xb, yb in loader:
            opt.zero_grad(); loss_fn(m(xb), yb).backward(); opt.step()
    m.eval()
    with torch.no_grad():
        tl = loss_fn(m(Xtr), ytr).item()
        acc = ((torch.sigmoid(m(Xte)) >= 0.5).float() == yte).float().mean().item()
        dead = int((torch.relu(m.fc1(Xtr)).max(0).values <= 0).sum())
    print(f"Adam lr={lr:<5} loss {tl:.4f}  test acc {acc:.4f}  dead {dead}/16")
```

```
Adam lr=0.01  loss 0.0877  test acc 0.9880  dead 0/16
Adam lr=0.5   loss 0.1442  test acc 0.9880  dead 7/16
Adam lr=2.0   loss 0.4141  test acc 0.8240  dead 15/16
Adam lr=5.0   loss 0.7328  test acc 0.5000  dead 16/16
```

This is more interesting than a simple blow-up, and it is worth reading carefully.

At `lr = 0.5` Adam looks *fine* on the headline number — 98.8% test accuracy, same as the well-tuned run. But **7 of 16 hidden units are dead.** The network is quietly running at 56% capacity and its training loss is 64% worse (0.1442 vs 0.0877). On this easy problem nine units are plenty, so the damage never reaches the accuracy column. On a harder problem it would.

At `lr = 2.0` the damage becomes visible: 15 of 16 units dead, accuracy down 16 points. At `lr = 5.0` every unit is dead and the model outputs a constant — training loss `0.7328`, accuracy exactly **0.5000**, a coin flip. That is the identical endpoint as Module 5's `lr = 100` NumPy experiment and Module 4's `lr = 800` divergence row, arrived at by a different route.

**Adam's usable range is roughly `1e-4` to `1e-2`; SGD's on this problem is roughly `1e-2` to `1`.** They are two orders of magnitude apart, because Adam normalises each step by the recent gradient magnitude, so its `lr` is closer to "how far to move in parameter units" than "how much of the gradient to take." Copying a learning rate from an SGD recipe into an Adam optimizer is a classic and expensive mistake.

**The engineering lesson:** accuracy alone did not catch the `lr = 0.5` failure. The dead-unit count did. Log it.

---

### 5 — Quantify the `zero_grad` bug

```python
import torch, torch.nn as nn
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class MoonNet(nn.Module):
    def __init__(self, hidden=16):
        super().__init__()
        self.fc1 = nn.Linear(2, hidden); self.fc2 = nn.Linear(hidden, 1)
    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))


X, y = make_moons(n_samples=1000, noise=0.20, random_state=42)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
sc = StandardScaler().fit(Xtr)
Xtr = torch.tensor(sc.transform(Xtr), dtype=torch.float32)
Xte = torch.tensor(sc.transform(Xte), dtype=torch.float32)
ytr = torch.tensor(ytr, dtype=torch.float32).reshape(-1, 1)
yte = torch.tensor(yte, dtype=torch.float32).reshape(-1, 1)
loss_fn = nn.BCEWithLogitsLoss()

for epochs in (200, 1000):
    for zero in (True, False):
        torch.manual_seed(0)
        m = MoonNet(); opt = torch.optim.SGD(m.parameters(), lr=0.5)
        for _ in range(epochs):
            if zero:
                opt.zero_grad()
            loss_fn(m(Xtr), ytr).backward()
            opt.step()
        m.eval()
        with torch.no_grad():
            tl = loss_fn(m(Xtr), ytr).item()
            acc = ((torch.sigmoid(m(Xte)) >= 0.5).float() == yte).float().mean().item()
        gnorm = float(torch.cat([p.grad.reshape(-1) for p in m.parameters()]).norm())
        print(f"epochs={epochs:<5} zero_grad={str(zero):<5} "
              f"loss {tl:.4f}  test acc {acc:.4f}  grad norm {gnorm:.4f}")
```

**(a)+(c) Results:**

| Epochs | `zero_grad()` | Final train loss | Test accuracy | Final gradient norm |
|---|---|---|---|---|
| 200 | yes | 0.1916 | 0.9520 | 0.0397 |
| 200 | **no** | 0.3076 | **0.9640** | 1.6792 |
| 1000 | yes | **0.0760** | **0.9880** | 0.0073 |
| 1000 | **no** | 1.6981 | **0.6280** | 4.6746 |

At **200 epochs the bug is invisible** — in fact the broken run has *higher* test accuracy (96.4% vs 95.2%). If that were your whole experiment you would ship the bug. At **1000 epochs it is catastrophic**: accuracy falls from 98.8% to 62.8%, a 36-point collapse, and the training loss is 22× worse.

This is the most important thing to take from the exercise. A silent bug that looks fine on a short run and destroys a long one is far more dangerous than one that crashes.

**(b) Why the gradient norms differ so much.**

Without zeroing, `.grad` at step `t` is the **sum of the gradients from all `t` forward passes so far**, not the gradient of the current loss. Since `optimizer.step()` multiplies `.grad` by the learning rate, the *effective* learning rate grows roughly linearly with the step count — by epoch 1000 the model is taking steps hundreds of times larger than you asked for. The final gradient norm of 4.67 versus 0.0073 is a **640× difference**: the correctly-trained model has essentially reached the bottom (near-zero slope), while the broken one is still being flung around a region with steep slopes it can never settle in.

**(d) Why PyTorch accumulates by default.**

Because summing gradients across several forward passes is a genuinely useful operation — **gradient accumulation** lets you simulate a batch of 512 on a GPU that can only hold 64 at a time (run eight forward/backward passes, then one `step()`), and it is how multi-loss and multi-task models combine objectives. Auto-zeroing would silently make those patterns impossible, so PyTorch made the safe-for-power-users choice and pushed one line of responsibility onto everyone else.

---

### 6 — Early stopping with best-checkpoint restore

**(a) The implementation.**

```python
import copy
import torch, torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class MoonNet(nn.Module):
    def __init__(self, hidden=16):
        super().__init__()
        self.fc1 = nn.Linear(2, hidden); self.fc2 = nn.Linear(hidden, 1)
    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))


X, y = make_moons(n_samples=1000, noise=0.20, random_state=42)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
sc = StandardScaler().fit(Xtr)
Xtr = torch.tensor(sc.transform(Xtr), dtype=torch.float32)
Xte = torch.tensor(sc.transform(Xte), dtype=torch.float32)
ytr = torch.tensor(ytr, dtype=torch.float32).reshape(-1, 1)
yte = torch.tensor(yte, dtype=torch.float32).reshape(-1, 1)

loader = DataLoader(TensorDataset(Xtr, ytr), batch_size=64, shuffle=True,
                    generator=torch.Generator().manual_seed(0))
loss_fn = nn.BCEWithLogitsLoss()

torch.manual_seed(0)
model = MoonNet()
opt = torch.optim.Adam(model.parameters(), lr=0.01)

best_loss, best_state, best_epoch = float("inf"), None, -1
patience, bad_epochs, min_delta = 20, 0, 1e-4

for epoch in range(500):
    model.train()
    for xb, yb in loader:
        opt.zero_grad()
        loss_fn(model(xb), yb).backward()
        opt.step()

    model.eval()
    with torch.no_grad():
        val_loss = loss_fn(model(Xte), yte).item()

    if val_loss < best_loss - min_delta:
        best_loss = val_loss
        best_state = copy.deepcopy(model.state_dict())    # DEEP copy
        best_epoch = epoch
        bad_epochs = 0
    else:
        bad_epochs += 1
        if bad_epochs >= patience:
            print(f"stopped at epoch {epoch}; best val loss "
                  f"{best_loss:.4f} at epoch {best_epoch}")
            break

final_val = val_loss
model.load_state_dict(best_state)
model.eval()
with torch.no_grad():
    acc = ((torch.sigmoid(model(Xte)) >= 0.5).float() == yte).float().mean().item()
print("restored best; test acc", round(acc, 4))
print("val loss you would have kept without early stopping:", round(final_val, 4))
```

**(b)+(c) Output:**

```
stopped at epoch 208; best val loss 0.0335 at epoch 188
restored best; test acc 0.996
val loss you would have kept without early stopping: 0.0396
```

Early stopping fired at **epoch 208**, having found its best validation loss of **0.0335 at epoch 188**. It then restored those epoch-188 weights, which score **99.6%** on the test set. Without early stopping you would have kept the epoch-208 weights, whose validation loss is 0.0396 — about **18% worse**. And you would also have burned the remaining 292 epochs of the 500-epoch budget for nothing.

Two honest notes. First, this uses the test set as the validation set, which Module 1 forbids — in a real project you would hold out a third split, and the mini-project's FashionMNIST setup does exactly that. Second, `patience=20` is a tuning knob: too small and you stop on a random dip, too large and you waste compute. Twenty epochs is a reasonable default when an epoch is cheap.

**(d) Why `deepcopy`.**

`model.state_dict()` returns a dictionary whose values are **references to the model's live parameter tensors**, not copies. If you store it directly and keep training, `optimizer.step()` mutates those same tensors in place — so your "saved best" silently becomes whatever the model looks like right now, and restoring it does nothing at all. `copy.deepcopy` clones the tensors so your snapshot is frozen at the moment you took it. (The alternative is `torch.save(model.state_dict(), "best.pt")` on every improvement, which serialises to disk and therefore also copies — slower, but it survives a crash.)

</details>

---

[⬅ Previous](module-05-neural-networks-from-scratch.md) · [Level 3 Home](README.md) · [Next ➡](module-07-cnns-for-images.md)

# Module 7 — Convolutional Networks: Teaching a Model to See

**Level 3 · Module 7 · ~6 hours · Prereqs: Module 6 (tensors, autograd, `nn.Module`, `DataLoader`, the training loop) and Module 3 (confusion matrix, per-class recall).**

[⬅ Previous](module-06-pytorch-deep-learning.md) · [Level 3 Home](README.md) · [Next ➡](module-08-unsupervised-kmeans-pca.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. You will be able to explain, with a parameter count you computed yourself, why flattening an image into a dense layer throws away structure and wastes weights.
2. You will be able to compute the output height and width of a convolution or pooling layer from kernel size, stride, and padding — on paper, before you run the code.
3. You will be able to build a CNN in PyTorch, train it on CIFAR-10, and render its learned first-layer filters as images.
4. You will be able to apply data augmentation and transfer learning, and produce a results table that says exactly how many accuracy points each one bought.
5. You will be able to read a 10-class confusion matrix, name the worst confusion pair, and give a physical reason for it.

---

## 🪝 The Hook

Back in Level 1 you did an unplugged exercise: a grid of grey numbers on paper, a 3×3 box of weights, and you slid the box across the grid multiplying and adding. Out came a new grid where the vertical edges lit up and the flat regions went to zero. You were doing convolution by hand, and somebody had chosen those nine numbers for you.

Now here is the uncomfortable question that started modern computer vision. Who chooses the nine numbers?

For decades, the answer was: a PhD student, over about two years. Whole careers were built on hand-designing filters — SIFT, HOG, Haar cascades — clever little grids of weights that responded to corners or gradients or eyes. Then in 2012 a network called AlexNet won an image competition by an embarrassing margin, and its trick was almost rude in its simplicity: **don't design the filters, make them weights and let gradient descent find them.** Ninety-six filters in the first layer, learned from data, and when researchers rendered them as pictures they looked like — edge detectors and colour blobs. The same things humans had been hand-drawing all along.

This module is that idea. Everything you built in Module 6 still applies: forward pass, loss, `backward()`, `step()`. You are only changing the shape of the layer.

---

## 🧠 The Concept

### 1. Locality and weight sharing: why a dense layer is the wrong tool for a picture

Take a small colour photo: 32 pixels tall, 32 wide, 3 colour channels (red, green, blue). That is 32 × 32 × 3 = **3,072 numbers**.

In Module 6 you fed a flattened image into `nn.Linear`. Let's price that out. If your first hidden layer has 1,024 units:

```
weights = 3072 × 1024 = 3,145,728
biases  =              1,024
------------------------------------
total   =          3,146,752 parameters
```

Three million parameters in the *first layer alone*, before the network has learned anything. And it gets worse — those three million parameters are learning something silly. Consider what `nn.Linear` actually does:

- Weight #1 connects "the red value of the top-left pixel" to hidden unit 1.
- Weight #1,537 connects "the green value of pixel (0, 0) shifted a bit" to hidden unit 1.

To `nn.Linear`, those two inputs are unrelated coordinates in a 3,072-dimensional soup. It has **no idea they are next to each other**. If you randomly shuffled all 3,072 pixel positions — the same shuffle for every image — a dense network would train to exactly the same accuracy. That should horrify you. A picture whose pixels have been shuffled is not a picture, and a model that can't tell the difference is not looking at a picture.

🍕 **Analogy.** Imagine identifying a pizza by being handed 3,072 numbered envelopes, each containing the colour of one square millimetre, in random order. You *could* eventually learn "envelope 1,204 is usually red on pepperoni pizzas." But you'd need to learn that separately for every envelope, and if the pizza slid two millimetres to the left, every single thing you learned would be wrong. A convolution instead hands you a small magnifying glass and says: *slide this over the whole pizza and tell me wherever you see a round red disc.* One rule. Works everywhere on the plate.

Two principles fall out of that:

> **Locality:** what a pixel means is mostly determined by its immediate neighbours. An edge is a local event. You do not need pixel (0,0) to understand pixel (31,31).

> **Weight sharing:** a feature worth detecting in the top-left corner is worth detecting in the bottom-right corner too. So use *the same* small set of weights at every position, instead of learning a fresh set per position.

**A tiny concrete example.** A 3×3 edge-detector applied to a colour image has 3 × 3 × 3 = 27 weights plus 1 bias = **28 parameters**. Those 28 parameters get applied at 1,024 positions in a 32×32 image. Compare:

| Layer type | Parameters | Position-aware? | Survives a 2-pixel shift? |
|---|---:|---|---|
| `nn.Linear(3072, 1024)` | 3,146,752 | No — treats pixels as unordered | No |
| One 3×3 conv filter over RGB | 28 | Yes — uses neighbourhoods | Yes |
| `nn.Conv2d(3, 32, 3)` (32 filters) | 896 | Yes | Yes |

896 versus 3.1 million. That is a **3,500× reduction**, and the smaller layer is the one that actually understands images. That is not a compromise; that is the right inductive bias.

> **Inductive bias:** an assumption you bake into the model's *shape* rather than teaching it from data. "Nearby pixels are related" is an inductive bias. Good ones let you learn from far less data.

---

### 2. Kernels, stride, padding, and the output-size arithmetic you must be able to do on paper

> **Kernel (or filter):** a small grid of learnable weights — typically 3×3 or 5×5 — that slides across the input, computing a dot product at each position.

The sliding produces a new grid. Its size is not the same as the input's, and getting this wrong is the single most common CNN bug (you'll meet the error message in §Common Mistakes).

Three knobs control the output size:

- **Kernel size `k`** — how big the sliding window is.
- **Stride `s`** — how many pixels the window jumps each step. `s=1` slides one at a time; `s=2` skips every other position and halves the output.
- **Padding `p`** — how many rings of zeros you glue around the border before sliding, so the window can reach edge pixels properly.

> **The output-size formula.** For an input of size `n` along one axis:
> ```
> out = floor( (n + 2p − k) / s ) + 1
> ```
> Apply it separately to height and width. It is the same formula for convolution and for pooling.

🍕 **Analogy.** You are stamping cookies out of rolled dough. `k` is the cookie cutter's diameter, `s` is how far you shift the cutter between stamps, and `p` is extra dough you roll out around the edge so the cutter isn't hanging off the tray. The formula counts how many stamps fit.

**Worked arithmetic, five cases:**

| n | k | s | p | Arithmetic | out |
|---:|---:|---:|---:|---|---:|
| 32 | 3 | 1 | 0 | floor((32 + 0 − 3)/1) + 1 = 29 + 1 | **30** |
| 32 | 3 | 1 | 1 | floor((32 + 2 − 3)/1) + 1 = 31 + 1 | **32** |
| 32 | 3 | 2 | 1 | floor((32 + 2 − 3)/2) + 1 = floor(15.5) + 1 = 15 + 1 | **16** |
| 32 | 5 | 2 | 0 | floor((32 + 0 − 5)/2) + 1 = floor(13.5) + 1 = 13 + 1 | **14** |
| 32 | 2 | 2 | 0 | floor((32 + 0 − 2)/2) + 1 = 15 + 1 | **16** |

Notice row 2. **`k=3, s=1, p=1` keeps the size exactly the same.** This is called *same padding* and it is why almost every modern CNN uses 3×3 kernels with `padding=1`: you get to stack as many conv layers as you like without the image quietly shrinking away. The general rule for size-preserving convolution with stride 1 is `p = (k − 1) / 2`, so `k=3 → p=1`, `k=5 → p=2`, `k=7 → p=3`.

Notice the last row too: a 2×2 window with stride 2 halves the size. That is the standard downsampler.

**Why padding matters beyond size.** Without padding, the corner pixel of your image participates in exactly **one** dot product, while a central pixel participates in nine. The model gets nine times less evidence about corners. Padding with zeros gives the border a fair hearing.

---

### 3. Feature maps, channels, and pooling

A single filter produces one output grid. That grid is called a **feature map**.

> **Feature map:** the 2-D output of one filter — a heat map of "how strongly did this filter fire at each position?"

Real conv layers use many filters at once. `nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1)` means: 32 different filters, each looking at all 3 input channels, each producing its own 32×32 feature map. Output shape: **(32, 32, 32)** = (channels, height, width).

> **Channel:** one slice of depth. On the input, channels are colours (R, G, B). After a conv layer, channels are *learned concepts* — filter 7's channel might be "diagonal edge going up-right," filter 19's might be "orange blob."

**Parameter arithmetic for a conv layer:**

```
params = (in_channels × k × k × out_channels) + out_channels
                                                 └── one bias per output channel
```

`Conv2d(3, 32, 3)`: (3 × 3 × 3 × 32) + 32 = 864 + 32 = **896**.
`Conv2d(32, 64, 3)`: (32 × 3 × 3 × 64) + 64 = 18,432 + 64 = **18,496**.

Crucially, the parameter count **does not depend on the image size**. The same 896 weights work on a 32×32 image or a 3,000×3,000 image. Dense layers cannot say that.

**Pooling.** After a conv layer you usually shrink the spatial size.

> **Max pooling:** slide a small window (usually 2×2, stride 2) and keep only the largest value in each window. No learnable parameters at all.

Why keep only the max? Because after a filter fires, you mostly care *that* the feature was present in this neighbourhood, not exactly which pixel it peaked on. Throwing away the precise position buys you two things: the network becomes slightly shift-tolerant, and the tensor gets 4× smaller, so the next layer is 4× cheaper.

🍕 **Analogy.** Someone asks "was there a pepperoni in the top-left quarter of the pizza?" You don't need the millimetre coordinates. Yes-or-no, strongest signal in the region, done.

**Tiny numeric example.** Feature map:

```
  4   1  |  0   2
  2   9  |  3   1
 ---------+---------
  0   0  |  7   5
  1   3  |  6   8
```

2×2 max pool, stride 2 →

```
  9   3
  3   8
```

Sixteen numbers became four. The 9 and the 8 — the two strongest responses — survived.

---

### 4. The standard CNN skeleton

Nearly every convolutional classifier since 1998 has the same silhouette:

```
INPUT  (3, 32, 32)
  │
  ├─► [ Conv 3×3, 32 filters, pad 1 ] ──► ReLU ──► MaxPool 2×2
  │        spatial: 32×32 → 32×32              → 16×16
  │        channels:  3   →   32
  │
  ├─► [ Conv 3×3, 64 filters, pad 1 ] ──► ReLU ──► MaxPool 2×2
  │        spatial: 16×16 → 16×16              →  8×8
  │        channels: 32   →   64
  │
  ├─► [ Conv 3×3, 128 filters, pad 1 ] ─► ReLU ──► MaxPool 2×2
  │        spatial:  8×8  →  8×8               →  4×4
  │        channels: 64   →  128
  │
  ├─► Flatten           (128 × 4 × 4) = 2048 numbers
  ├─► Dropout(0.3)
  └─► Linear(2048 → 10)  ──►  10 class scores (logits)
```

Read the two columns on the right. **Spatial size goes down, channel count goes up.** That is the whole design philosophy in one sentence: trade *where* for *what*. Early layers know precisely where a tiny edge is but almost nothing about what the object is. Late layers have almost no positional resolution (4×4!) but 128 rich concept detectors.

The last part — flatten plus one or two `Linear` layers — is called the **classifier head**. The conv stack is called the **backbone**. Remember those two words; §6 depends on them.

> **Receptive field:** the region of the *original input image* that influences one cell in a later feature map. It grows as you stack layers.

For the skeleton above, one cell of the final 4×4 map sees a **22×22 patch** of the 32×32 input. (You'll compute that yourself in Practice 5.) That's why depth matters: a single 3×3 conv can only ever see a 3×3 patch, which is not enough to recognise a horse.

---

### 5. Data augmentation: free training data

Here is a fact about a photo of a cat: if you mirror it left-to-right, it is still a photo of a cat. Your model does not know this. It has to learn it, and learning it costs data.

Unless you just... tell it.

> **Data augmentation:** randomly transforming each training image every time it is loaded, in ways that do not change the label, so the model effectively sees a larger and more varied training set.

The three workhorses for natural photos:

| Transform | What it does | Why it helps |
|---|---|---|
| `RandomHorizontalFlip()` | mirrors the image 50% of the time | teaches left-right invariance |
| `RandomCrop(32, padding=4)` | pads to 40×40, cuts a random 32×32 window | teaches small-shift invariance |
| `ColorJitter(brightness=.2, contrast=.2, saturation=.2)` | nudges the colours | teaches lighting invariance |

**The critical detail:** augmentation is applied **only to the training set**. Never to validation or test. Two reasons. First, you want your evaluation to be deterministic — running it twice should give the same number. Second, augmentation makes images *harder*, so a randomly-cropped test set would understate your true accuracy. This is a variant of the same discipline you learned in Module 2: transforms that involve randomness or fitting belong to the training path only.

**And the transforms must be label-preserving.** Horizontal flip is safe for cats. It is a catastrophe for handwritten digits (a mirrored 2 is not a 2), for road signs with text, and for any dataset where left and right mean different things. Vertical flip is safe for satellite imagery and wrong for almost everything else. There is no universal augmentation list — you have to think about your data.

🍕 **Analogy.** You're studying for a geography quiz using flashcards. Augmentation is a friend who, each time they show you a card, holds it at a slightly different angle, in slightly different light, sometimes covering a corner with their thumb. You learn the *country*, not the specific photograph. But if your friend started mirroring the maps, you'd learn wrong geography. Same idea, and same failure mode.

---

### 6. Transfer learning: don't start from random

Training a CNN from scratch on 5,000 images is a bit like teaching someone to read by starting with "here is what a line is." Somebody else already did that part, on 1.2 million images, on a GPU cluster, for weeks.

> **Transfer learning:** take a network already trained on a huge dataset, keep its learned backbone, and reuse it for your (usually much smaller) problem.

The intuition is that the first layers of *any* image network learn the same things — edges, colour transitions, textures, then simple shapes. Those are not ImageNet-specific. They're vision-specific. Only the last layers are specialised to "is this a Siberian husky or a malamute," and those are exactly the layers you replace.

There are two ways to do it:

**(a) Feature extraction / linear probe — freeze everything, train a new head.**

```
[ pretrained resnet18 backbone ]  →  512-dim feature vector  →  [ your new Linear(512, 10) ]
        FROZEN (requires_grad=False)                                  TRAINED
```

Because the backbone is frozen, it computes the *same* feature vector for a given image every single epoch. So you can run every image through it **once**, cache the 512-dim vectors, and then train the head on those cached vectors for hundreds of epochs in seconds. This is a genuinely useful engineering trick and it makes transfer learning practical on a laptop.

**(b) Fine-tuning — unfreeze the last block too, and train it with a small learning rate.**

```
[ conv1 … layer3 ]   [ layer4 ]   [ new fc ]
      FROZEN          TRAINED      TRAINED
                      lr = 1e-4    lr = 1e-4
```

Fine-tuning usually beats a linear probe by a few points, because it lets the late layers re-specialise. The small learning rate matters: with a big one you'd blast away the pretrained weights in the first few steps, which is called *catastrophic forgetting* and defeats the entire purpose.

**One preprocessing rule you must not skip.** A pretrained model expects images preprocessed exactly the way its training data was: resized to the size it was trained on, and normalized with *its* mean and standard deviation, not yours. `torchvision` gives you these for free via `weights.transforms()`. Use it. Feeding a resnet raw 0-to-1 CIFAR pixels at 32×32 is the most common way people get a mysteriously bad transfer-learning result.

| Approach | Trains | Speed on a laptop | Typical CIFAR-10-subset accuracy |
|---|---|---|---|
| Small CNN from scratch | ~114k params | minutes | ~58% |
| Small CNN + augmentation | ~114k params | minutes (more epochs) | ~66% |
| resnet18 frozen + linear head | 5,130 params | one feature pass, then seconds | ~82% |
| resnet18 fine-tune `layer4` + head | ~8.4M params | slow on CPU, use a GPU | ~87% |

---

## 🔍 Worked Example

Let's convolve a real (tiny) image by hand, all the way through conv → ReLU → pool, showing every multiplication.

**The image.** A 6×6 greyscale patch with a bright left half and a dark right half — a vertical edge down the middle. Every row is identical:

```
 10  10  10   2   2   2
 10  10  10   2   2   2
 10  10  10   2   2   2
 10  10  10   2   2   2
 10  10  10   2   2   2
 10  10  10   2   2   2
```

**The kernel.** A 3×3 vertical-edge detector (bright-on-the-left):

```
  1   0  −1
  1   0  −1
  1   0  −1
```

**Step 1 — output size.** `n=6, k=3, s=1, p=0`:

```
out = floor((6 + 0 − 3) / 1) + 1 = 3 + 1 = 4
```

So the feature map is **4×4**.

**Step 2 — position (0, 0).** The window covers rows 0–2, columns 0–2. Every entry there is 10:

```
window:            kernel:          products:
 10  10  10          1   0  −1       10   0  −10
 10  10  10    ×     1   0  −1   =   10   0  −10
 10  10  10          1   0  −1       10   0  −10
```

Sum = (10 + 0 − 10) + (10 + 0 − 10) + (10 + 0 − 10) = 0 + 0 + 0 = **0**.

Makes sense: this window is completely flat. No edge, no response.

**Step 3 — position (0, 1).** Window slides right one pixel: rows 0–2, columns 1–3 → `[10, 10, 2]` in every row.

```
row contribution = (1 × 10) + (0 × 10) + (−1 × 2) = 10 − 2 = 8
three rows       = 8 + 8 + 8 = 24
```

Output = **24**. The edge is inside the window, and the filter shouts.

**Step 4 — position (0, 2).** Columns 2–4 → `[10, 2, 2]`.

```
row contribution = (1 × 10) + (0 × 2) + (−1 × 2) = 10 − 2 = 8
three rows       = 24
```

Output = **24**.

**Step 5 — position (0, 3).** Columns 3–5 → `[2, 2, 2]`. Flat again.

```
row contribution = 2 − 2 = 0  →  total 0
```

Output = **0**.

**Step 6 — the other rows.** Because every row of the image is identical, every output row is identical. The full 4×4 feature map:

```
   0   24   24    0
   0   24   24    0
   0   24   24    0
   0   24   24    0
```

The edge, which was implicit in the pixel values, is now an explicit bright stripe. That is what a feature map *is*.

**Step 7 — bias and ReLU.** Say the bias is 0. ReLU sets negatives to zero; there are none, so the map is unchanged. (Had we used the mirrored kernel `[−1, 0, 1]`, every 24 would be a −24, and ReLU would have wiped the whole map to zeros — which is exactly why a real conv layer learns *both* polarities as separate filters.)

**Step 8 — 2×2 max pool, stride 2.** Output size: `floor((4 − 2)/2) + 1 = 1 + 1 = 2`, so a 2×2 result.

- Top-left window = rows 0–1, cols 0–1 = `{0, 24, 0, 24}` → max = **24**
- Top-right window = rows 0–1, cols 2–3 = `{24, 0, 24, 0}` → max = **24**
- Bottom-left = `{0, 24, 0, 24}` → **24**
- Bottom-right = `{24, 0, 24, 0}` → **24**

```
  24   24
  24   24
```

**Step 9 — read the result.** We started with 36 numbers describing pixel brightnesses. We ended with 4 numbers, all saying the same thing: *there is a strong bright-to-dark vertical edge in this patch.* We lost the exact position of the edge and kept the fact of it. Sixteen numbers became four, and the four are more useful than the sixteen.

Now stack that idea a hundred times with learned kernels, and you have a CNN.

---

## 💻 Hands-On

### Setup

```bash
pip install torch torchvision numpy matplotlib scikit-learn seaborn
```

Everything below runs on CPU. The fine-tuning section is slow on CPU — if it drags, run that part in Google Colab with a free GPU (`Runtime → Change runtime type → T4 GPU`).

### Part A — conv shapes, hands on the keyboard

Never guess a shape. Print it.

```python
import torch
import torch.nn as nn

x = torch.randn(8, 3, 32, 32)          # batch of 8 RGB 32x32 images

def report(layer, inp):
    out = layer(inp)
    n_params = sum(p.numel() for p in layer.parameters())
    print(f"{str(layer):55s} {tuple(inp.shape)} -> {tuple(out.shape)}  params={n_params}")
    return out

h = report(nn.Conv2d(3, 32, kernel_size=3, padding=1), x)   # same padding
h = report(nn.MaxPool2d(2), h)
h = report(nn.Conv2d(32, 64, kernel_size=3, padding=1), h)
h = report(nn.MaxPool2d(2), h)
h = report(nn.Conv2d(64, 128, kernel_size=3, padding=1), h)
h = report(nn.MaxPool2d(2), h)
print("flattened feature length:", h[0].numel())
```

Expected output:

```
Conv2d(3, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))    (8, 3, 32, 32) -> (8, 32, 32, 32)  params=896
MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)  (8, 32, 32, 32) -> (8, 32, 16, 16)  params=0
Conv2d(32, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))   (8, 32, 16, 16) -> (8, 64, 16, 16)  params=18496
MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)  (8, 64, 16, 16) -> (8, 64, 8, 8)  params=0
Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))  (8, 64, 8, 8) -> (8, 128, 8, 8)  params=73856
MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)  (8, 128, 8, 8) -> (8, 128, 4, 4)  params=0
flattened feature length: 2048
```

Check the params against the arithmetic in §3: 896, 18,496, 73,856. Pooling has zero parameters, as promised.

### Part B — verify the worked example in code

```python
import torch
import torch.nn.functional as F

# 6x6 image: left half bright (10), right half dark (2)
img = torch.tensor([[10., 10., 10., 2., 2., 2.]]).repeat(6, 1)
img = img.view(1, 1, 6, 6)                       # (batch=1, channels=1, H, W)

kernel = torch.tensor([[1., 0., -1.],
                       [1., 0., -1.],
                       [1., 0., -1.]]).view(1, 1, 3, 3)

fmap = F.conv2d(img, kernel, bias=torch.zeros(1), stride=1, padding=0)
print("feature map shape:", tuple(fmap.shape))
print(fmap[0, 0])

pooled = F.max_pool2d(F.relu(fmap), kernel_size=2, stride=2)
print("after relu + 2x2 maxpool:")
print(pooled[0, 0])
```

Expected output:

```
feature map shape: (1, 1, 4, 4)
tensor([[ 0., 24., 24.,  0.],
        [ 0., 24., 24.,  0.],
        [ 0., 24., 24.,  0.],
        [ 0., 24., 24.,  0.]])
after relu + 2x2 maxpool:
tensor([[24., 24.],
        [24., 24.]])
```

Identical to what you computed by hand. Good — when your paper arithmetic and PyTorch agree, you can trust both.

### Part C — the CIFAR-10 subset

We use 500 training images per class (5,000 total) and 200 test images per class (2,000 total). Small on purpose: it trains fast, and small data is exactly where augmentation and transfer learning show their value.

```python
import numpy as np
import torch
from torch.utils.data import Subset, DataLoader
from torchvision import datasets, transforms

torch.manual_seed(0)
np.random.seed(0)

CLASSES = ['plane', 'car', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck']

CIFAR_MEAN = (0.4914, 0.4822, 0.4465)
CIFAR_STD  = (0.2470, 0.2435, 0.2616)

plain_tf = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(CIFAR_MEAN, CIFAR_STD),
])

aug_tf = transforms.Compose([
    transforms.RandomCrop(32, padding=4),        # small random shifts
    transforms.RandomHorizontalFlip(),           # cats look like cats mirrored
    transforms.ColorJitter(0.2, 0.2, 0.2),       # lighting robustness
    transforms.ToTensor(),
    transforms.Normalize(CIFAR_MEAN, CIFAR_STD),
])

def balanced_indices(targets, per_class):
    targets = np.asarray(targets)
    return np.concatenate([np.where(targets == c)[0][:per_class] for c in range(10)])

# download once; the two train objects share the same files on disk
train_plain_full = datasets.CIFAR10("./data", train=True,  download=True, transform=plain_tf)
train_aug_full   = datasets.CIFAR10("./data", train=True,  download=True, transform=aug_tf)
test_full        = datasets.CIFAR10("./data", train=False, download=True, transform=plain_tf)

tr_idx = balanced_indices(train_plain_full.targets, 500)
te_idx = balanced_indices(test_full.targets, 200)

train_plain = Subset(train_plain_full, tr_idx)
train_aug   = Subset(train_aug_full,   tr_idx)
test_set    = Subset(test_full,        te_idx)

print("train:", len(train_plain), " test:", len(test_set))

test_loader = DataLoader(test_set, batch_size=256, shuffle=False)
```

Expected output:

```
Files already downloaded and verified
Files already downloaded and verified
Files already downloaded and verified
train: 5000  test: 2000
```

(The first run prints download progress bars instead.)

### Part D — a small CNN from scratch

```python
import torch.nn as nn

class SmallCNN(nn.Module):
    def __init__(self, n_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(3,   32, 3, padding=1)
        self.conv2 = nn.Conv2d(32,  64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
        self.pool  = nn.MaxPool2d(2)
        self.relu  = nn.ReLU()
        self.drop  = nn.Dropout(0.3)
        self.fc    = nn.Linear(128 * 4 * 4, n_classes)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))   # (B,32,16,16)
        x = self.pool(self.relu(self.conv2(x)))   # (B,64, 8, 8)
        x = self.pool(self.relu(self.conv3(x)))   # (B,128,4, 4)
        x = torch.flatten(x, 1)                   # (B, 2048)
        return self.fc(self.drop(x))              # (B, 10) logits

model = SmallCNN()
print("total parameters:", sum(p.numel() for p in model.parameters()))
```

Expected output:

```
total parameters: 113738
```

113,738 parameters — versus the 3,146,752 a *single* dense layer would have needed. Now the training loop, which is the exact same five lines you wrote in Module 6:

```python
import time

def pick_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")

device = pick_device()
print("device:", device)

@torch.no_grad()
def evaluate(model, loader):
    model.eval()                                  # turns Dropout OFF
    correct = total = 0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        preds = model(xb).argmax(dim=1)
        correct += (preds == yb).sum().item()
        total   += yb.numel()
    return correct / total

def train(model, train_ds, epochs, lr=1e-3, batch_size=64, tag=""):
    loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    model.to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    t0 = time.time()
    for ep in range(1, epochs + 1):
        model.train()                             # Dropout back ON
        running = 0.0
        for xb, yb in loader:
            xb, yb = xb.to(device), yb.to(device)
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            opt.step()
            running += loss.item() * yb.size(0)
        if ep % 5 == 0 or ep == 1:
            acc = evaluate(model, test_loader)
            print(f"[{tag}] epoch {ep:3d}  train_loss {running/len(train_ds):.4f}  test_acc {acc:.4f}")
    return time.time() - t0

torch.manual_seed(0)
scratch = SmallCNN()
t_scratch = train(scratch, train_plain, epochs=20, tag="scratch")
acc_scratch = evaluate(scratch, test_loader)
print(f"scratch CNN: acc={acc_scratch:.4f}  train_time={t_scratch:.1f}s")
```

Expected output (numbers will vary a little by machine and seed):

```
device: cpu
[scratch] epoch   1  train_loss 2.1826  test_acc 0.2620
[scratch] epoch   5  train_loss 1.5122  test_acc 0.4405
[scratch] epoch  10  train_loss 1.0663  test_acc 0.5215
[scratch] epoch  15  train_loss 0.6544  test_acc 0.5570
[scratch] epoch  20  train_loss 0.3419  test_acc 0.5695
scratch CNN: acc=0.5695  train_time=196.4s
```

Read that carefully. Training loss fell from 2.18 to 0.34 — the model has nearly memorised 5,000 images. Test accuracy stalled at about 57%. That gap is **overfitting**, and it is exactly the disease augmentation treats.

### Part E — the same CNN, with augmentation

```python
torch.manual_seed(0)
augmented = SmallCNN()
t_aug = train(augmented, train_aug, epochs=40, tag="aug")   # more epochs: harder data
acc_aug = evaluate(augmented, test_loader)
print(f"augmented CNN: acc={acc_aug:.4f}  train_time={t_aug:.1f}s")
```

Expected output:

```
[aug] epoch   1  train_loss 2.2337  test_acc 0.1975
[aug] epoch   5  train_loss 1.7286  test_acc 0.3835
[aug] epoch  10  train_loss 1.4914  test_acc 0.4795
[aug] epoch  20  train_loss 1.2588  test_acc 0.5720
[aug] epoch  30  train_loss 1.1341  test_acc 0.6215
[aug] epoch  40  train_loss 1.0402  test_acc 0.6480
augmented CNN: acc=0.6480  train_time=412.8s
```

Two things to notice. The final **training** loss is far *higher* (1.04 versus 0.34) — augmentation makes the training data genuinely harder, so the model can no longer memorise it. And the final **test** accuracy is 8 points higher. That's the trade you wanted: less memorisation, more generalisation, at the cost of needing roughly twice the epochs.

### Part F — look at the filters the network learned

```python
import matplotlib.pyplot as plt

def show_filters(weight, title, ncols=8):
    w = weight.detach().cpu().clone()
    w = (w - w.min()) / (w.max() - w.min() + 1e-8)     # scale to [0,1] for display
    n = w.shape[0]
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols, nrows))
    for i, ax in enumerate(axes.flat):
        ax.axis("off")
        if i < n:
            ax.imshow(w[i].permute(1, 2, 0).numpy())    # (C,H,W) -> (H,W,C)
    fig.suptitle(title)
    plt.tight_layout()
    plt.savefig(title.replace(" ", "_") + ".png", dpi=110)
    plt.close(fig)
    print("saved", title.replace(" ", "_") + ".png")

show_filters(augmented.conv1.weight, "learned conv1 filters 3x3")
```

Be honest about what you'll see: **3×3 filters are only nine pixels and they look like coloured smudges.** You can usually pick out a few with a clear light-side/dark-side split (edge detectors) and several that are mostly one colour (colour-opponent detectors). To see the textbook picture, look at a network with a big first kernel:

```python
from torchvision.models import resnet18, ResNet18_Weights
pre = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
print("resnet18 conv1 weight shape:", tuple(pre.conv1.weight.shape))
show_filters(pre.conv1.weight[:32], "resnet18 conv1 filters 7x7")
```

Expected output:

```
resnet18 conv1 weight shape: (64, 3, 7, 7)
saved resnet18_conv1_filters_7x7.png
```

Open that PNG. You will see unmistakable oriented light-dark bars at many angles, plus blue/orange and green/magenta colour blobs. Nobody programmed those. Gradient descent found them, from photographs, because they are the most useful nine-degrees-of-freedom things to measure about a natural image. This is the payoff of the module's hook.

### Part G — transfer learning, frozen backbone (fast path)

```python
import torch.nn as nn
from torch.utils.data import TensorDataset
from torchvision.models import resnet18, ResNet18_Weights

weights = ResNet18_Weights.IMAGENET1K_V1
pre_tf  = weights.transforms()      # resize 256 -> centre-crop 224 -> ImageNet normalize

tl_train_full = datasets.CIFAR10("./data", train=True,  download=False, transform=pre_tf)
tl_test_full  = datasets.CIFAR10("./data", train=False, download=False, transform=pre_tf)
tl_train = Subset(tl_train_full, tr_idx)
tl_test  = Subset(tl_test_full,  te_idx)

backbone = resnet18(weights=weights)
backbone.fc = nn.Identity()          # chop off the 1000-class head -> outputs 512 features
backbone.eval().to(device)
for p in backbone.parameters():
    p.requires_grad = False

@torch.no_grad()
def extract(ds, batch_size=64):
    loader = DataLoader(ds, batch_size=batch_size, shuffle=False)
    feats, labs = [], []
    for xb, yb in loader:
        feats.append(backbone(xb.to(device)).cpu())
        labs.append(yb)
    return torch.cat(feats), torch.cat(labs)

t0 = time.time()
Ftr, ytr = extract(tl_train)
Fte, yte = extract(tl_test)
t_extract = time.time() - t0
print("feature shapes:", tuple(Ftr.shape), tuple(Fte.shape), f"({t_extract:.1f}s)")
```

Expected output:

```
feature shapes: (5000, 512) (2000, 512)  (243.7s)
```

Each image is now 512 numbers instead of 3,072 — and those 512 numbers already encode "furry," "has wheels," "sky-coloured background." Training a classifier on them is trivial:

```python
from sklearn.linear_model import LogisticRegression

t0 = time.time()
probe = LogisticRegression(max_iter=2000, C=1.0)
probe.fit(Ftr.numpy(), ytr.numpy())
t_probe = time.time() - t0
acc_probe = probe.score(Fte.numpy(), yte.numpy())
print(f"frozen-backbone linear probe: acc={acc_probe:.4f}  head_train_time={t_probe:.1f}s")
```

Expected output:

```
frozen-backbone linear probe: acc=0.8215  head_train_time=11.3s
```

**82% versus 57%.** Same 5,000 images. The difference is 1.2 million ImageNet photos that somebody else paid for.

### Part H — transfer learning, fine-tuning `layer4` (slow path, use a GPU)

```python
ft = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
for p in ft.parameters():
    p.requires_grad = False
for p in ft.layer4.parameters():          # unfreeze the last conv block
    p.requires_grad = True
ft.fc = nn.Linear(512, 10)                # brand-new head, trainable by default
ft.to(device)

trainable = sum(p.numel() for p in ft.parameters() if p.requires_grad)
print("trainable parameters:", trainable)

def train_ft(model, ds, epochs=3, lr=1e-4, batch_size=32):
    loader = DataLoader(ds, batch_size=batch_size, shuffle=True)
    opt = torch.optim.Adam([p for p in model.parameters() if p.requires_grad], lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    t0 = time.time()
    for ep in range(1, epochs + 1):
        model.train()
        running = 0.0
        for xb, yb in loader:
            xb, yb = xb.to(device), yb.to(device)
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            opt.step()
            running += loss.item() * yb.size(0)
        print(f"[finetune] epoch {ep}  train_loss {running/len(ds):.4f}")
    return time.time() - t0

tl_test_loader = DataLoader(tl_test, batch_size=64, shuffle=False)
t_ft = train_ft(ft, tl_train, epochs=3)
acc_ft = evaluate(ft, tl_test_loader)
print(f"fine-tuned resnet18: acc={acc_ft:.4f}  train_time={t_ft:.1f}s")
```

Expected output (on a T4 GPU; expect roughly 20× longer on CPU):

```
trainable parameters: 8398858
[finetune] epoch 1  train_loss 0.9331
[finetune] epoch 2  train_loss 0.3117
[finetune] epoch 3  train_loss 0.1846
fine-tuned resnet18: acc=0.8730  train_time=147.2s
```

### Part I — the confusion matrix and the top confusion pair

```python
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report

@torch.no_grad()
def collect_preds(model, loader):
    model.eval()
    ys, ps = [], []
    for xb, yb in loader:
        ps.append(model(xb.to(device)).argmax(1).cpu())
        ys.append(yb)
    return torch.cat(ys).numpy(), torch.cat(ps).numpy()

y_true, y_pred = collect_preds(augmented, test_loader)
cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(8, 7))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=CLASSES, yticklabels=CLASSES)
plt.xlabel("predicted"); plt.ylabel("true"); plt.title("Augmented CNN — confusion matrix")
plt.tight_layout(); plt.savefig("cm_augmented.png", dpi=110); plt.close()

# rank off-diagonal cells: the model's 10 worst mistakes
off = [(cm[i, j], CLASSES[i], CLASSES[j])
       for i in range(10) for j in range(10) if i != j]
off.sort(reverse=True)
print("top 10 confusions (count, true -> predicted):")
for c, t, p in off[:10]:
    print(f"  {c:3d}   {t:6s} -> {p}")

print()
print(classification_report(y_true, y_pred, target_names=CLASSES, digits=3))
```

Expected output (abridged):

```
top 10 confusions (count, true -> predicted):
   61   cat    -> dog
   47   dog    -> cat
   38   bird   -> deer
   34   deer   -> horse
   31   plane  -> ship
   29   truck  -> car
   28   cat    -> deer
   26   bird   -> plane
   24   horse  -> deer
   22   car    -> truck
```

**Diagnosis of the top pair.** `cat → dog` (61) and `dog → cat` (47) together account for 108 of the 704 errors — over 15% of all mistakes from just 2 of the 90 possible confusion cells. Why? At 32×32 resolution, a cat and a dog are both: a furry quadruped-shaped brown/grey blob, often indoors, often photographed from the front, with two ears and a muzzle. The features that actually separate them — snout length, ear shape, pupil shape — occupy maybe 4×4 pixels in these images, which is right at the limit of what survives three rounds of max pooling. Notice the pair is roughly symmetric (61 vs 47), which tells you this is genuine *ambiguity in the data at this resolution*, not a class-imbalance bias pushing everything one way. The fix is not a better optimiser. It is more pixels, or more examples of these two classes specifically.

Compare that with `plane → ship` (31): those two share "large man-made object against a big flat blue background," and the model has clearly latched onto the background. That one *is* fixable with augmentation that varies the background, or with crops that de-emphasise it.

---

## ✍️ Practice

### 1. [Warm-up] Output-size arithmetic on paper, then verified

For each configuration, compute the output height/width **by hand using the formula**, writing out the arithmetic, then verify with a one-line PyTorch call.

| # | input n | kernel k | stride s | padding p | layer type |
|---|---:|---:|---:|---:|---|
| a | 28 | 5 | 1 | 0 | conv |
| b | 28 | 5 | 1 | 2 | conv |
| c | 32 | 3 | 2 | 1 | conv |
| d | 64 | 7 | 2 | 3 | conv |
| e | 15 | 2 | 2 | 0 | max pool |

**Done looks like:** five hand-computed numbers, each matching what PyTorch prints, plus one sentence explaining what (b) and (d) have in common.

### 2. [Warm-up] Price the two layer types

Compute parameter counts by hand, then confirm in PyTorch.

(a) `nn.Conv2d(3, 64, kernel_size=7)` applied to a 3×224×224 image.
(b) An `nn.Linear` that maps the *flattened* 3×224×224 image to 64 outputs.
(c) The ratio (b) ÷ (a).
(d) `nn.Conv2d(64, 128, kernel_size=3)`.

**Done looks like:** four numbers with the arithmetic shown, and one sentence on why the conv count is independent of the 224×224 image size.

### 3. [Build] Hand-convolve a horizontal edge, then check it

A 5×5 greyscale image: rows 0 and 1 are all `9`; rows 2, 3, and 4 are all `1`. The kernel is a horizontal-edge detector:

```
  1   1   1
  0   0   0
 −1  −1  −1
```

Stride 1, padding 0, bias 0.

(a) State the output size using the formula.
(b) Compute the full output feature map by hand, showing the arithmetic for at least one cell in each output row.
(c) Verify with `F.conv2d`.
(d) Explain in one or two sentences why the same value appears in two different output rows.

**Done looks like:** a hand-written grid identical to the tensor PyTorch prints, plus the explanation.

### 4. [Build] Add a fourth block and measure it

Extend `SmallCNN` with a fourth conv block: `Conv2d(128, 256, 3, padding=1) → ReLU → MaxPool2d(2)`, and update the `Linear` layer's input size to match.

(a) Predict the spatial size after the fourth pool, and the new flatten length, **before running**.
(b) Predict the new total parameter count.
(c) Train it for 40 epochs on `train_aug` and report test accuracy next to the 3-block augmented result.
(d) Write two sentences on whether the extra 285k parameters were worth it *on 5,000 images*.

**Done looks like:** predictions that match `print`, plus a two-row comparison table and an honest verdict.

### 5. [Stretch] Compute the receptive field

For the 3-block `SmallCNN` (conv 3×3 pad 1, pool 2×2 stride 2, three times), compute the receptive field of one cell in the final 4×4 feature map, using the standard recurrence:

```
RF_out  = RF_in + (k − 1) × jump_in
jump_out = jump_in × s
```

starting from `RF = 1`, `jump = 1`.

(a) Fill in a six-row table (conv1, pool1, conv2, pool2, conv3, pool3) with RF and jump after each layer.
(b) State the final receptive field in pixels.
(c) A CIFAR image is 32×32. What fraction of the image does one final-layer cell see, and what does that imply about whether the network can use whole-object shape?

**Done looks like:** the completed table, the final number, and a two-sentence implication.

### 6. [Stretch] Augmentation ablation

Which single augmentation is doing the work? Train the same `SmallCNN` (same seed, 30 epochs each) under five conditions:

1. no augmentation
2. `RandomHorizontalFlip()` only
3. `RandomCrop(32, padding=4)` only
4. `ColorJitter(0.2, 0.2, 0.2)` only
5. all three

Report a five-row table of test accuracy, and the delta of each single augmentation over the no-augmentation baseline.

**Done looks like:** the table, a statement of which single transform helped most, and one sentence on whether the three effects are additive (does 2's delta + 3's delta + 4's delta ≈ 5's delta?).

---

## 🤔 Think Deeper

**1. Augmentation encodes your assumptions — and your assumptions can be wrong.**
`RandomHorizontalFlip` says "left and right don't matter." For CIFAR cats, fine. Now imagine you're building a model to read handwritten Devanagari, or to classify chest X-rays (where the heart is on a specific side), or to detect whether a car is driving the wrong way down a one-way street. In each case flipping doesn't just fail to help — it teaches the model something false.
*How to reason about it:* for any proposed transform, ask "could a human expert look at the transformed image and still confidently give the original label?" If the answer is no, the transform is injecting label noise. Then ask the harder version: could it be *usually* fine but wrong for one rare subgroup? That's where the damage hides.

**2. Whose pictures trained the backbone you just downloaded?**
ImageNet's 1.2 million photos were scraped from image search around 2009 and labelled by crowdworkers paid a few cents per image. Its geographic distribution skews heavily to North America and Western Europe. Researchers have shown that models pretrained on it recognise a "wedding" or a "spice rack" far better in some countries than others. When you write `weights=ResNet18_Weights.IMAGENET1K_V1`, you inherit all of that.
*How to reason about it:* separate two questions — does the bias transfer to *your* task, and would you notice if it did? A frozen backbone plus a linear head can only see what the backbone measures, so backbone blind spots become your blind spots. The Module 3 tool for detecting this is per-subgroup recall, not overall accuracy. Ask what subgroups your test set can even distinguish.

**3. What does "the model learned edge detectors" actually mean?**
You rendered resnet18's first layer and saw shapes that look like the receptive fields neuroscientists recorded in cat visual cortex in 1959. That's a genuinely striking convergence. But it is also the layer that is easiest to visualise, and the layer whose behaviour is most constrained by the statistics of natural images. Layer 12 does not render into anything a human can interpret.
*How to reason about it:* distinguish "this visualisation is beautiful and true" from "I therefore understand the model." Ask what prediction your interpretation makes that you could test — for example, if filter 7 really is a 45° edge detector, feeding it a synthetic 45° bar should maximise its activation. Interpretations you can't test are stories.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| `RuntimeError: mat1 and mat2 shapes cannot be multiplied (64x2048 and 512x10)` | You changed a conv or pool and the flatten length changed, but the `Linear` input is still hard-coded to the old value | Recompute with the output-size formula, or print `x.shape` right before `torch.flatten`. Long term, use `nn.AdaptiveAvgPool2d((1,1))` so the head's input size stops depending on the image size |
| Augmenting the validation/test set | You built one `transforms.Compose` and reused it for every split because it was convenient | Keep two transform objects — `train_tf` with randomness, `eval_tf` without — and never let them cross. Same discipline as fit-on-train-only from Module 2 |
| Feeding a pretrained model your own normalization (or none) | You reused the CIFAR mean/std, or plain `ToTensor()`, out of habit | Use `weights.transforms()`. A pretrained model's weights are only valid for the input distribution they were trained on |
| Forgetting `model.eval()` before evaluating | `Dropout` stays active and randomly zeros 30% of features, so your accuracy is noisy and too low | Always `model.eval()` + `@torch.no_grad()` in your eval function, and `model.train()` at the top of each training epoch |
| Fine-tuning at `lr=1e-3` and getting worse than the frozen probe | The default Adam learning rate is fine for random weights and catastrophic for pretrained ones — the first few steps destroy them | Fine-tune at `1e-4` or lower; consider training only the head for one epoch first, then unfreezing |
| Concluding "the CNN is 57% accurate" from a training-set number | You printed `train_loss` and read accuracy off the same batches the model just fit | Report accuracy on a held-out split only. A widening train/test gap is the definition of overfitting, not a bug in your printing |
| Comparing scratch-CNN to transfer-learning without matching preprocessing | One model sees 32×32 CIFAR-normalized images, the other sees 224×224 ImageNet-normalized — you can't attribute the gap | It's fine that the pipelines differ (they must), but say so explicitly in the results table, and note input resolution as a column |
| Trusting a single accuracy number on a 10-class problem | Accuracy hides that the model is 82% on `car` and 31% on `cat` | Always print `classification_report` and the confusion matrix. Module 3's tools do not stop applying just because the data is images |

---

## 🛠️ Mini-Project — See It

**Goal.** Produce a defensible three-way comparison of scratch CNN, augmented CNN, and transfer learning on the same CIFAR-10 subset, and diagnose the model's single worst confusion pair.

**Starter steps.**

1. **Fix the data.** Use Part C's balanced 5,000-train / 2,000-test subset. Set `torch.manual_seed(0)` and `np.random.seed(0)` at the top of the file so your runs are comparable. Split 1,000 of the 5,000 training images off as a **validation set** and use it — not the test set — for any decision you make about epochs or hyperparameters. Open the test set once per model, at the end.
2. **Run 1 — scratch.** Train `SmallCNN` on the un-augmented training split for 20 epochs. Record test accuracy, wall-clock training time, and total parameters.
3. **Run 2 — augmented.** Same architecture, same seed, `train_aug` transforms, 40 epochs. Record the same three numbers.
4. **Run 3 — transfer.** Frozen resnet18 features + a logistic-regression head (Part G). Record accuracy, feature-extraction time, head-training time, and *trainable* parameter count (5,130). If you have a GPU, add a fourth row for fine-tuned `layer4`.
5. **Filters.** Save the conv1 filter grid for the augmented CNN and for pretrained resnet18. Put both PNGs in your write-up.
6. **Confusion.** For your best model, compute the confusion matrix, save the heatmap, and print the top 10 off-diagonal cells.
7. **Diagnose.** Write 150–250 words on the top confusion pair. Include: the raw counts in both directions, whether the confusion is symmetric, at least one concrete visual reason grounded in what a 32×32 image can and can't show, and one specific change you would make to fix it (not "train longer").

**Success criteria checklist.**

- [ ] A results table with columns: model, input resolution, trainable params, epochs, train time (s), test accuracy.
- [ ] Every accuracy number comes from the 2,000-image test set, opened once per model.
- [ ] Validation, not test, was used to choose epoch counts.
- [ ] Two filter-grid PNGs saved, with one sentence each on what you can and cannot see in them.
- [ ] A confusion-matrix heatmap and a printed top-10 confusion list.
- [ ] A 150–250 word diagnosis naming the top pair, its symmetry, a physical cause, and a specific proposed fix.
- [ ] One sentence stating how many accuracy points augmentation bought and how many transfer learning bought, as separate numbers.

**Level it up.** Add a **per-class recall** column to your results table for all three models, and find a class where transfer learning is *worse* than the augmented scratch CNN. (There is usually at least one — ImageNet has hundreds of dog breeds and no `frog` supercategory, which biases what the backbone measures.) Write two sentences explaining what that tells you about when transfer learning is not automatically the right answer.

---

## 🔑 Key Takeaways

- A dense layer treats an image as 3,072 unordered numbers and needs 3.1 million weights to do it badly; a conv layer uses locality and weight sharing to do it better with 896.
- `out = floor((n + 2p − k)/s) + 1`. Compute it on paper before you run. `k=3, s=1, p=1` preserves size; `k=2, s=2` pooling halves it.
- The universal CNN shape is *spatial size down, channel count up* — conv → ReLU → pool, repeated, then a flatten and a small classifier head.
- Augmentation is free training data, but only for transforms that genuinely preserve the label. It raises training loss and lowers test error; that is the point.
- Transfer learning beat 20 epochs of scratch training by 25 accuracy points on identical data. When your dataset is small, the pretrained backbone is usually the highest-value engineering decision available.
- Accuracy on 10 classes is a summary that hides everything interesting. The confusion matrix tells you *which* pair the model can't separate, and that's what you can actually act on.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Convolution** | Sliding a small grid of weights over an image and taking a dot product at every position | The 3×3 edge kernel turning a flat image into a bright stripe |
| **Kernel / filter** | The small grid of learnable weights that does the sliding | `[[1,0,−1],[1,0,−1],[1,0,−1]]` detects vertical edges |
| **Stride** | How far the window jumps between positions | `s=2` skips every other position and halves the output |
| **Padding** | Rings of zeros added around the border so the window can reach edge pixels | `k=3, p=1` keeps a 32×32 image at 32×32 |
| **Feature map** | The output grid of one filter — a heat map of where that filter fired | The 4×4 grid of `0, 24, 24, 0` in the worked example |
| **Channel** | One slice of depth; colours on the input, learned concepts after a conv layer | RGB is 3 channels; `Conv2d(3, 32, 3)` outputs 32 |
| **Max pooling** | Keep only the biggest value in each small window; no weights to learn | 2×2 pool turns 16 numbers into 4 |
| **Weight sharing** | Using the same filter weights at every position in the image | 28 weights applied at 1,024 positions |
| **Receptive field** | How much of the original image one later cell can "see" | 22×22 pixels for the final layer of `SmallCNN` |
| **Backbone / head** | The conv stack that extracts features / the small dense part that classifies | resnet18's conv layers / your `Linear(512, 10)` |
| **Data augmentation** | Randomly changing training images in label-preserving ways to get more variety | Mirroring a cat photo — still a cat |
| **Transfer learning** | Reusing a model trained on a huge dataset for your smaller problem | Frozen resnet18 features + a new 10-class head |
| **Fine-tuning** | Unfreezing some pretrained layers and training them gently with a small learning rate | `layer4` at `lr=1e-4` |
| **Overfitting** | Training loss keeps dropping while test accuracy stops improving | Train loss 0.34, test accuracy stuck at 57% |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1. [Warm-up] Output-size arithmetic

Formula: `out = floor((n + 2p − k)/s) + 1`.

**(a)** n=28, k=5, s=1, p=0 → `floor((28 + 0 − 5)/1) + 1 = 23 + 1 =` **24**
**(b)** n=28, k=5, s=1, p=2 → `floor((28 + 4 − 5)/1) + 1 = 27 + 1 =` **28**
**(c)** n=32, k=3, s=2, p=1 → `floor((32 + 2 − 3)/2) + 1 = floor(15.5) + 1 = 15 + 1 =` **16**
**(d)** n=64, k=7, s=2, p=3 → `floor((64 + 6 − 7)/2) + 1 = floor(31.5) + 1 = 31 + 1 =` **32**
**(e)** n=15, k=2, s=2, p=0 → `floor((15 + 0 − 2)/2) + 1 = floor(6.5) + 1 = 6 + 1 =` **7**

Verification:

```python
import torch, torch.nn as nn
cases = [(28, nn.Conv2d(1, 1, 5, stride=1, padding=0)),
         (28, nn.Conv2d(1, 1, 5, stride=1, padding=2)),
         (32, nn.Conv2d(1, 1, 3, stride=2, padding=1)),
         (64, nn.Conv2d(1, 1, 7, stride=2, padding=3)),
         (15, nn.MaxPool2d(2, stride=2))]
for n, layer in cases:
    print(n, "->", layer(torch.zeros(1, 1, n, n)).shape[-1])
```

```
28 -> 24
28 -> 28
32 -> 16
64 -> 32
15 -> 7
```

**What (b) and (d) have in common:** both use `p = (k − 1)/2` — that is *same padding*. In (b) with stride 1 it preserves the size exactly (28 → 28); in (d) with stride 2 it gives exactly half (64 → 32). That's the standard trick: same padding makes the stride, and only the stride, decide the downsampling factor.

### 2. [Warm-up] Price the two layer types

**(a)** `Conv2d(3, 64, kernel_size=7)`:
```
weights = in_ch × k × k × out_ch = 3 × 7 × 7 × 64 = 9,408
biases  = out_ch                 =                     64
total   =                                          9,472
```

**(b)** Flattened input length = 3 × 224 × 224 = **150,528**.
```
weights = 150,528 × 64 = 9,633,792
biases  =                     64
total   =              9,633,856
```

**(c)** Ratio = 9,633,856 ÷ 9,472 = **1,017.1×**. The dense layer costs a thousand times more and produces 64 numbers about the whole image; the conv layer produces 64 *feature maps* of 218×218 numbers each.

**(d)** `Conv2d(64, 128, kernel_size=3)`:
```
weights = 64 × 3 × 3 × 128 = 73,728
biases  =                       128
total   =                    73,856
```

```python
import torch.nn as nn
for layer in [nn.Conv2d(3, 64, 7), nn.Linear(3*224*224, 64), nn.Conv2d(64, 128, 3)]:
    print(type(layer).__name__, sum(p.numel() for p in layer.parameters()))
```

```
Conv2d 9472
Linear 9633856
Conv2d 73856
```

**Why conv is size-independent:** the conv layer's parameters are the filter weights, and there is exactly one set of them regardless of how many positions you slide it over. Doubling the image to 448×448 changes the *output* size and the *compute*, but not a single weight. The dense layer's weight count is `input_length × output_length`, and `input_length` is the whole image, so quadrupling the pixels quadruples the parameters.

### 3. [Build] Hand-convolve a horizontal edge

The image:

```
row 0:  9  9  9  9  9
row 1:  9  9  9  9  9
row 2:  1  1  1  1  1
row 3:  1  1  1  1  1
row 4:  1  1  1  1  1
```

**(a)** `out = floor((5 + 0 − 3)/1) + 1 = 2 + 1 =` **3**, so a 3×3 feature map.

**(b)** Because every row is constant, the answer depends only on which three image rows the window covers. Kernel row weights are `+1` (top), `0` (middle), `−1` (bottom), and each kernel row has three `1`s (or three `−1`s).

*Output row 0* — window covers image rows 0, 1, 2 = values 9, 9, 1:
```
top    : (+1)(9) + (+1)(9) + (+1)(9) = +27
middle : ( 0)(9) + ( 0)(9) + ( 0)(9) =   0
bottom : (−1)(1) + (−1)(1) + (−1)(1) =  −3
total  =                              +24
```

*Output row 1* — window covers image rows 1, 2, 3 = values 9, 1, 1:
```
top    : (+1)(9) × 3 = +27
middle : ( 0)(1) × 3 =   0
bottom : (−1)(1) × 3 =  −3
total  =              +24
```

*Output row 2* — window covers image rows 2, 3, 4 = values 1, 1, 1:
```
top    : (+1)(1) × 3 =  +3
middle : ( 0)(1) × 3 =   0
bottom : (−1)(1) × 3 =  −3
total  =                0
```

Full feature map:

```
  24   24   24
  24   24   24
   0    0    0
```

**(c)** Verification:

```python
import torch, torch.nn.functional as F
img = torch.cat([torch.full((2, 5), 9.), torch.full((3, 5), 1.)]).view(1, 1, 5, 5)
k = torch.tensor([[1., 1., 1.], [0., 0., 0.], [-1., -1., -1.]]).view(1, 1, 3, 3)
print(F.conv2d(img, k, bias=torch.zeros(1))[0, 0])
```

```
tensor([[24., 24., 24.],
        [24., 24., 24.],
        [ 0.,  0.,  0.]])
```

**(d)** The edge sits between image rows 1 and 2. A 3-pixel-tall kernel still straddles that boundary when it is centred on row 1 *and* when it is centred on row 2, so two consecutive output rows both contain a bright row and a dark row and both report `+24`. In general, an edge produces a response that is `k − 1` cells wide (here 2 rows), not a single crisp line. Bigger kernels give stronger but blurrier localisation — one more reason 3×3 became the default.

### 4. [Build] Add a fourth block

**(a) Predictions.** After pool3 the map is 128×4×4. `Conv2d(128, 256, 3, padding=1)` keeps 4×4 (same padding), then `MaxPool2d(2)` gives `floor((4−2)/2)+1 =` **2×2**. Flatten length = 256 × 2 × 2 = **1,024**.

**(b) Parameter prediction.**
```
conv1 :   3 × 3 × 3 ×  32 +  32 =     896
conv2 :  32 × 3 × 3 ×  64 +  64 =  18,496
conv3 :  64 × 3 × 3 × 128 + 128 =  73,856
conv4 : 128 × 3 × 3 × 256 + 256 = 295,168
fc    :        1024 × 10  +  10 =  10,250
--------------------------------------------
total                            = 398,666
```

**(c) Code and result.**

```python
class DeeperCNN(nn.Module):
    def __init__(self, n_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(3,   32, 3, padding=1)
        self.conv2 = nn.Conv2d(32,  64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
        self.conv4 = nn.Conv2d(128, 256, 3, padding=1)
        self.pool, self.relu, self.drop = nn.MaxPool2d(2), nn.ReLU(), nn.Dropout(0.3)
        self.fc = nn.Linear(256 * 2 * 2, n_classes)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        x = self.pool(self.relu(self.conv4(x)))
        return self.fc(self.drop(torch.flatten(x, 1)))

torch.manual_seed(0)
deeper = DeeperCNN()
print("params:", sum(p.numel() for p in deeper.parameters()))
t = train(deeper, train_aug, epochs=40, tag="deeper")
print("deeper acc:", evaluate(deeper, test_loader))
```

```
params: 398666
[deeper] epoch  40  train_loss 1.0961  test_acc 0.6395
deeper acc: 0.6395
```

| Model | Params | Epochs | Test accuracy |
|---|---:|---:|---:|
| 3-block + augmentation | 113,738 | 40 | 0.6480 |
| 4-block + augmentation | 398,666 | 40 | 0.6395 |

**(d) Verdict.** No — the extra 285,000 parameters bought **−0.85 accuracy points**, which is inside run-to-run noise at best and a small loss at worst. On 5,000 images the model is already data-limited, not capacity-limited: the 3-block network could memorise the un-augmented training set (Part D's train loss of 0.34 proves it), so adding capacity addresses a problem you don't have. The fourth pool also drops the final map to 2×2, which throws away most remaining spatial information. Extra depth pays off when you have more data or when you add regularisation that makes the depth usable — not by itself.

### 5. [Stretch] Receptive field

Recurrence: `RF_out = RF_in + (k − 1) × jump_in`, `jump_out = jump_in × s`. Start `RF = 1`, `jump = 1`.

| Layer | k | s | RF calculation | RF | jump |
|---|---:|---:|---|---:|---:|
| conv1 | 3 | 1 | 1 + (3−1)×1 = 3 | **3** | 1 × 1 = 1 |
| pool1 | 2 | 2 | 3 + (2−1)×1 = 4 | **4** | 1 × 2 = 2 |
| conv2 | 3 | 1 | 4 + (3−1)×2 = 8 | **8** | 2 × 1 = 2 |
| pool2 | 2 | 2 | 8 + (2−1)×2 = 10 | **10** | 2 × 2 = 4 |
| conv3 | 3 | 1 | 10 + (3−1)×4 = 18 | **18** | 4 × 1 = 4 |
| pool3 | 2 | 2 | 18 + (2−1)×4 = 22 | **22** | 4 × 2 = 8 |

**(b)** Final receptive field = **22 × 22 pixels**.

**(c)** 22 × 22 = 484 pixels out of 32 × 32 = 1,024, so one final-layer cell sees about **47%** of the image area (22/32 ≈ 69% along each axis).

*Implication:* no single cell of the final feature map sees the whole image, so no single cell can encode a whole-object judgement like "this silhouette is a horse." The network can only combine whole-image evidence in the `Linear` head, which sees all 16 cells at once. That's adequate here because CIFAR objects usually fill most of the frame, but it explains why deeper networks (which reach a receptive field larger than the input) tend to do better on shape-driven classes — and why the model leans on local texture cues like "fur" that fit inside 22×22, which is precisely why cat and dog collapse together.

### 6. [Stretch] Augmentation ablation

```python
def make_train_set(extra):
    tf = transforms.Compose(extra + [
        transforms.ToTensor(),
        transforms.Normalize(CIFAR_MEAN, CIFAR_STD)])
    full = datasets.CIFAR10("./data", train=True, download=False, transform=tf)
    return Subset(full, tr_idx)

conditions = {
    "none":   [],
    "flip":   [transforms.RandomHorizontalFlip()],
    "crop":   [transforms.RandomCrop(32, padding=4)],
    "jitter": [transforms.ColorJitter(0.2, 0.2, 0.2)],
    "all":    [transforms.RandomCrop(32, padding=4),
               transforms.RandomHorizontalFlip(),
               transforms.ColorJitter(0.2, 0.2, 0.2)],
}

results = {}
for name, extra in conditions.items():
    torch.manual_seed(0)
    m = SmallCNN()
    train(m, make_train_set(extra), epochs=30, tag=name)
    results[name] = evaluate(m, test_loader)

base = results["none"]
print(f"{'condition':10s} {'acc':>7s} {'delta':>8s}")
for name, acc in results.items():
    print(f"{name:10s} {acc:7.4f} {acc-base:+8.4f}")
```

Representative output:

```
condition      acc    delta
none        0.5810  +0.0000
flip        0.6105  +0.0295
crop        0.6290  +0.0480
jitter      0.5885  +0.0075
all         0.6425  +0.0615
```

**Which helped most:** `RandomCrop(32, padding=4)`, at **+4.8 points**, roughly 1.6× the benefit of horizontal flip and more than six times the benefit of colour jitter.

**Are they additive?** Individually the deltas sum to 0.0295 + 0.0480 + 0.0075 = **+0.085**, but combining all three gives only **+0.0615** — about 72% of the sum. So the effects are **sub-additive**, which is what you should expect: flip and crop are both attacking the same underlying failure, namely that the model memorises exact pixel positions. Once crop has broken that habit, flip has less left to fix. Two practical lessons follow. First, you cannot pick augmentations by ranking them individually and adding the winners; you have to test the combination. Second, colour jitter's tiny +0.0075 is well inside seed-to-seed noise for a 2,000-image test set (the standard error on an accuracy of 0.58 with n = 2,000 is about 0.011), so the honest conclusion is "jitter did not measurably help here" — and you would want to re-run with three seeds before claiming otherwise.

</details>

---

[⬅ Previous](module-06-pytorch-deep-learning.md) · [Level 3 Home](README.md) · [Next ➡](module-08-unsupervised-kmeans-pca.md)

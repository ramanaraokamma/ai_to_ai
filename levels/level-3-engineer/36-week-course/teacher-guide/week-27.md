# Week 27 — Term 3 Checkpoint: See It

[⬅ Week 26](week-26.md) · [Course Home](../README.md) · [Week 28 ➡](week-28.md) · [Student Guide](../student-guide/week-27.md) · [Workbook](../workbook/week-27.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟨 Review — Term 3 checkpoint, and two experiments where the honest answer is more interesting than the hoped-for one |
| **Big idea** | You can buy accuracy two ways **without collecting a single new picture**: make more training pictures out of the ones you have, and reuse a network that already learned to see. **One of the two works here. One of them does not, and saying which is the skill.** |
| **New vocabulary** | data augmentation · transfer learning · freezing · backbone / head · fine-tuning · confusion pair |
| **New maths** | **None.** Counting, subtracting two accuracies, and reading a grid. This week practises Weeks 8, 22, 25 and 26. |
| **New syntax** | `np.roll(img, shift, axis=0)` · `p.requires_grad = False` · `ConfusionMatrixDisplay.from_predictions(y, pred)` · `torch.cat([a, b])` |
| **Dataset** | `load_digits()` — 1,797 8×8 digits — **plus numpy-shifted copies of it.** Augmentation and transfer learning entirely offline. **Nothing downloads. No internet needed. No torchvision.** |
| **Materials** | The printed workbook (`workbook/week-27.md`; it has no page numbers, see Homework) · **a plain sheet of lined paper for the six showcase lines** · **a big two-column sheet headed FROZEN / UNFROZEN** · the **PARAMETER COUNT** sheet from Week 22 and **THE SHAPE LADDER** from Week 25 (both come down at the end of today) · **six Term 3 showcase station cards, printed** · squared paper · the Bug Log · Week 26's `digits_cnn.py` on disk |
| **Tech needed** | Laptop with Python 3, numpy, scikit-learn, matplotlib, **torch**. **No new installs.** |
| **Prep time** | 30 minutes the night before · 10 minutes on the day (setting up six stations) |
| **Expected runtime of the code** | `see_it.py` trains **six** networks. The augmented ones are the slow pair at **about 15 seconds each**; the whole file is **about 40 seconds** on this machine. **Time yours before you say a number.** |

> **⚠️ Watch out:** this week has two results that are not what a textbook would promise, and **both of them are the lesson.** In the seed-0 run, augmentation with `np.roll` alone buys **exactly zero** accuracy points — you have to blank the edge the ink rolled off before it buys anything, and then it buys 1.30. (These are single-seed numbers: over seeds 0-4 the wrapped version gained 0 to 2.0 points over plain and the blanked version beat plain in four seeds, by 1.3 to 1.7 points, and lost 0.2 in the fifth. Augmented runs also get five times the training steps, so the gain is not cleanly separable from "more updates". The lesson about wrapped labels stands.) And transfer learning from digits 0–4 to digits 5–9 comes out **worse than training from scratch**. If you present either one as a triumph you will be lying to the class, and worse, you will teach them that an experiment's job is to confirm what the teacher said. **Run both honestly, put both numbers on the board, and spend the wrap saying why.**

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Augment the training set offline** by shifting pictures a pixel with `np.roll`, and **report how many accuracy points it bought** — including the honest finding that the naive version buys **+0.00** and the version that blanks the rolled-off edge buys **+1.30**.
2. **Freeze a convolutional backbone** trained on digits 0–4 and retrain only the ten-way head on digits 5–9, **reporting both numbers** — frozen `0.9257`, unfrozen `0.9665` — and the from-scratch control, `0.9814`.
3. **Read a ten-class confusion matrix**, name the worst confusion pair, and **give a physical reason** why those two digits look alike at 8×8 — not a restatement of the count.
4. **Produce a four-row results table** — plain, augmented, frozen-transfer, fine-tuned — **with the held-out pile named on every row**, and say which two rows may honestly be compared.

Observable evidence: `see_it.py` printing `blanked-edge augmentation bought +1.30 points` and the three transfer numbers; the FROZEN / UNFROZEN wall sheet with `0.9257` and `0.9665` side by side; a four-row table where rows 3 and 4 say `269 rows of 5–9` and not `540`; and a written diagnosis of the 1/8 pair that mentions ink columns rather than repeating "4 of 11".

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each one carries on from the one above. **The complete runnable file is in the Prep Checklist and the Answer Key.**

**There is no new mathematics this week.** There is one subtraction of two accuracies and a lot of counting. What your prep needs to buy you is confidence about the two honest negative results, because a teacher who is surprised by them mid-lesson will fudge them, and fudging them is the one thing that would waste this week.

### 1. Data augmentation, and the trap that makes it useless

> **Data augmentation** — making extra training examples out of the ones you have, by changing them in ways that **do not change the label**. A digit shifted one pixel left is still the same digit, so you get a free extra training row.

The move is `np.roll`, and there is exactly one thing to understand about it.

```python
np.roll(img, 1, axis=0)     # slide every row down by one
np.roll(img, 1, axis=1)     # slide every column right by one
```

**`np.roll` wraps.** Whatever falls off one edge comes back on the other. Here is the real evidence from one 8×8 digit:

```text
original      : [0.   0.   0.   0.5  0.44 0.   0.   0.  ]      ← row 0
rolled down 1 : [0.   0.   0.   0.31 0.88 1.   0.25 0.  ]      ← the new row 0
the top row of the rolled copy is the BOTTOM row of the original:
original row 7: [0.   0.   0.   0.31 0.88 1.   0.25 0.  ]
```

**Look at those two identical rows.** The bottom row of the digit has reappeared at the top. On a big photo with dark borders you would never notice. **On an 8×8 digit that fills the frame, you have just put the bottom of a 6 above its own top**, and that picture is not a 6 any more. The label says 6. **You have manufactured a training row with a wrong label.**

And here is what it costs, measured:

```text
plain                3.3s  movable 1898  train 0.9881  test 0.9796  (529 of 540)
augmented (wrap)    16.4s  movable 1898  train 0.9774  test 0.9796  (529 of 540)
augmented (blank)   14.6s  movable 1898  train 0.9893  test 0.9926  (536 of 540)

wrap-around augmentation bought +0.00 points
blanked-edge  augmentation bought +1.30 points
```

**The wrap version bought nothing at all.** Five times the training rows, five times the training time, and exactly the same 529 out of 540. Because a fifth of the extra rows were nonsense, and the nonsense cancelled the benefit.

**The fix is three lines and it is the whole point of the week's first half:** after rolling, blank the edge the ink rolled off.

```python
def shift(stack, dr, dc):
    """Shift every picture in the stack, and blank the edge it rolled off."""
    out = np.roll(np.roll(stack, dr, axis=1), dc, axis=2).copy()
    if dr == 1:
        out[:, 0, :] = 0.0      # rolled down, so the top row is wrapped junk
    if dr == -1:
        out[:, -1, :] = 0.0     # rolled up, so the bottom row is wrapped junk
    if dc == 1:
        out[:, :, 0] = 0.0      # rolled right, so the left column is junk
    if dc == -1:
        out[:, :, -1] = 0.0     # rolled left, so the right column is junk
    return out
```

With that, the same experiment buys **+1.30 accuracy points: 529 of 540 becomes 536 of 540.** Seven more digits read correctly, from no new data at all.

![One digit becomes five](../figures/fig-w27-1-augmentation-one-image-becomes-five.svg)
*Figure 27.1 — One digit becomes five. 1,257 × 5 = 6,285 training rows, and still 540 test rows that were never shifted. Plain 0.9796 becomes 0.9926 once the rolled-off edge is blanked; leave the wrap in and it buys nothing.*

**Note the axes carefully, because this is the silent bug of the week.** The pictures are stacked: `X_train` is `(1257, 8, 8)`. So:

- `axis=0` is **which picture**. Rolling that shuffles the *pictures* while the labels stay put.
- `axis=1` is **the rows of each picture**.
- `axis=2` is **the columns of each picture**.

Here is what `axis=0` does, on four tiny 2×2 pictures, so you can see it:

```text
a stack of 4 tiny 2x2 pictures:
[[[ 0  1]     [[ 4  5]     [[ 8  9]     [[12 13]
  [ 2  3]]      [ 6  7]]     [10 11]]     [14 15]]

np.roll(X, 1, axis=0) rolls the STACK:
[[[12 13]     [[ 0  1]     [[ 4  5]     [[ 8  9]
  [14 15]]      [ 2  3]]     [ 6  7]]     [10 11]]

np.roll(X, 1, axis=1) rolls each picture's ROWS:
[[[ 2  3]     [[ 6  7]     [[10 11]     [[14 15]
  [ 0  1]]      [ 4  5]]     [ 8  9]]     [12 13]]
```

**Get the axis wrong and there is no error whatsoever.** The model trains on pictures paired with other pictures' labels. Here is what that produces, measured:

```text
trained on the WRONG axis: train 0.5968  test 0.8574
```

**The test accuracy is HIGHER than the training accuracy.** That is the fingerprint, and it should be impossible: a model always does better on the data it saw. It happens here because two fifths of the *training* rows had scrambled labels and were unlearnable (the other three fifths keep correct labels, so training accuracy sits near 0.6), while the test set was untouched. **Install this as a permanent alarm: if test beats train, your training labels are wrong.**

**And the one rule that is never negotiable:** augment the **training** set only. Never the test set. Two reasons, and both matter. Evaluation must be repeatable — the same test set every time or the number means nothing. And augmentation makes pictures harder, so an augmented test set would understate the model. **This is Week 6's fit-on-train-only discipline in a new costume, and it is the same discipline.**

### 2. Transfer learning, done honestly

> **Transfer learning** — take a network that already learned to see something, keep the part that does the seeing, and retrain only the part that does the answering.
>
> **Backbone** — the conv layers, which turn a picture into features. **Head** — the small dense part at the end, which turns features into an answer.
>
> **Freezing** — telling PyTorch that a block of weights is not allowed to change: `p.requires_grad = False`.
>
> **Fine-tuning** — unfreezing the backbone as well, and letting it adjust.

Since we have no internet and no pretrained network, we make our own two-stage problem — which is honestly a better teaching device, because the student can see both stages:

- **Stage 1.** Train the whole network on **digits 0 to 4 only** — 630 training rows. It reaches **0.9926** on its 271 held-out rows of 0–4.
- **Stage 2.** Now a *new* problem: **digits 5 to 9** — 627 training rows. Keep the conv layers from stage 1, throw the head away, bolt on a fresh `nn.Linear(64, 10)`, and train.

![Keep the eyes, replace the answer sheet](../figures/fig-w27-2-frozen-backbone-new-head.svg)
*Figure 27.2 — Keep the eyes, replace the answer sheet. Frozen: 650 of the 1,898 weights may move, test 0.9257. Unfrozen: all 1,898 may move, 0.9665. From nothing on the same 627 rows: 0.9814.*

**The three real numbers:**

```text
frozen-transfer      0.3s  movable  650  train 0.9330  test 0.9257  (249 of 269)
fine-tuned           1.6s  movable 1898  train 0.9841  test 0.9665  (260 of 269)
scratch on 5-9       1.5s  movable 1898  train 0.9729  test 0.9814  (264 of 269)
```

**Read that third row again. Training from scratch beat both transfer versions.**

**This is the result, and you must not soften it.** Here is the honest explanation, and it is a genuinely good one:

**Transfer learning pays when the source problem is enormous and the target problem is tiny.** The version people use in industry borrows a backbone trained on 1.2 million photographs and applies it to a few thousand. **Ours borrowed a backbone trained on 630 pictures of five digits, and applied it to 627 pictures of five different digits.** The source was not bigger than the target. It was the same size, and it was *specialised* — those eight filters were tuned to the shapes of 0, 1, 2, 3 and 4, and 5 to 9 are different shapes.

**What the frozen version did buy, and it is real:** it trained **650 weights instead of 1,898** in **0.3 seconds instead of 1.5**, and it got to **92.6%**. So a third of the weights and a fifth of the time gets you within six points. **On a problem where the backbone came from a million photographs and your target set is fifty pictures, that trade is transformative. Here it is not.**

> **🧑‍🏫 If a student asks "so transfer learning doesn't work?"** — the honest answer, and it is worth saying carefully: *"It works, and it is one of the most valuable techniques there is. What we just measured is the condition it needs: the thing you borrow from has to know far more than the thing you are borrowing it for. We borrowed from something that knew about as much as we did. So we got the machinery working and we found out the price. Both of those are real results."*

### 3. The confusion matrix, and how to diagnose a pair physically

Week 8 built a 2×2 by hand. This is the same object with ten rows and ten columns: **rows are what the digit really was, columns are what the model said**, class 0 first, which is scikit-learn's order.

Here is the real thing for last week's plain CNN on its 540 held-out digits:

```text
[[54  0  0  0  0  0  0  0  0  0]
 [ 0 53  0  0  0  1  0  0  1  0]
 [ 0  1 52  0  0  0  0  0  0  0]
 [ 0  0  0 53  0  1  0  1  0  0]
 [ 0  0  0  0 53  0  0  0  0  1]
 [ 0  0  0  0  0 55  0  0  0  0]
 [ 0  1  0  0  0  0 53  0  0  0]
 [ 0  0  0  0  0  0  0 54  0  0]
 [ 0  3  0  0  0  0  0  1 48  0]
 [ 0  0  0  0  0  0  0  0  0 54]]
```

**529 on the diagonal, 11 off it.** And the addition check, which they should do every time: the ten diagonal entries sum to 529, the eleven off-diagonal entries sum to 11, and 529 + 11 = 540 = the number of test rows.

Ranked, every mistake it made:

```text
  3   8 -> 1
  1   8 -> 7
  1   6 -> 1
  1   4 -> 9
  1   3 -> 7
  1   3 -> 5
  1   2 -> 1
  1   1 -> 8
  1   1 -> 5
```

> **Confusion pair** — two classes that the model mixes up with each other, in both directions. You find it by adding the two cells that face each other across the diagonal.

**Here the pair is 1 and 8: `8 → 1` three times and `1 → 8` once, so 4 of the 11 mistakes.** More than a third of every error, from one pair out of the 45 possible pairs.

![Ten classes, eleven mistakes](../figures/fig-w27-3-ten-class-confusion-matrix-worst-pair.svg)
*Figure 27.3 — Ten classes, eleven mistakes. Three real 8s were called 1 and one real 1 was called 8: 4 of the 11 mistakes, leaning towards calling an 8 a 1.*

**Now the physical diagnosis, and this is objective 3 — the part students get wrong by restating the number instead of explaining it.**

Average all the 1s in the dataset, and all the 8s, and add up the ink in each column:

```text
average 1, ink per column: [  0   5  42  93 106  56   9   2]
average 8, ink per column: [  0   9  71  87  86  66  11   0]
```

**Both pile their ink in columns 2 to 5, and both peak in the middle.** A 1 peaks at 106 in column 4; an 8 peaks at 87 and 86 in columns 3 and 4. **The two profiles are almost the same shape.**

**And the reason is the resolution.** An 8 is two loops stacked. At 8×8, each loop is about three pixels tall and four wide — **too small to have a visible hole.** The loops fill in with grey, and what survives the fill-in is a bright vertical bar down the middle columns. **Which is exactly what a 1 is.**

**And the direction makes sense too.** It is `8 → 1` three times but `1 → 8` only once, and although 3 against 1 is too few mistakes to be certain it is not chance, it is what you would expect: **an 8 can lose its holes and become a bar, but a bar cannot grow holes.** The information loss goes one way.

**Say the good version and the bad version out loud so the class hears the difference:**

- ❌ *"The worst pair is 1 and 8, with 4 mistakes out of 11."* — That is the number restated. It is not a diagnosis.
- ✅ *"1 and 8, 4 of 11, and it leans towards calling an 8 a 1. At 8×8 an 8's two loops are three pixels tall, too small to hold a hole, so they fill in and leave a bright bar down the middle columns — and the average 1 and the average 8 both pile their ink in columns 2 to 5. The loss goes one way: an 8 can lose its holes, a 1 cannot grow them. The fix is not a better optimiser. It is more pixels."*

### 4. Every new line of this week's code, explained to somebody who has never programmed

Four new lines.

**New line 1 — shifting a picture.**

```python
np.roll(stack, 1, axis=1)
```

`np.roll` slides everything along one axis and wraps what falls off. The `1` is how far; a `−1` slides the other way. **`axis` says which direction of the array to slide along**, and on a stack of pictures, `axis=1` is the rows of each picture and `axis=2` is the columns. `axis=0` is which picture, and that is the bug.

**New line 2 — freezing weights.**

```python
for p in layer.parameters():
    p.requires_grad = False
```

Every block of weights carries a flag saying "am I being trained?" Setting it to `False` means the backward pass stops computing a slope for it, so nothing can move it. **`requires_grad` is not new — it is Week 20's flag, and this is the first week they turn it off.**

**And the trap.** You must also keep the frozen weights *out of the optimiser*, or at least be aware that they are in it:

```python
movable = [p for p in model.parameters() if p.requires_grad]
opt = torch.optim.Adam(movable, lr=1e-3)
```

Hand `model.parameters()` to Adam with some of them frozen and **there is no error** — the frozen ones simply have `grad = None` and never move. It works. But it hides what you meant, and `sum(p.numel() for p in model.parameters() if p.requires_grad)` is the line that proves your intention: it prints **650**, not 1,898.

**New line 3 — the confusion matrix as a picture.**

```python
ConfusionMatrixDisplay.from_predictions(y_test, pred, cmap="Blues", colorbar=False)
plt.savefig("confusion.png", dpi=110)
```

`from_predictions` takes the truth and the predictions and draws the whole ten-by-ten grid with the counts written in. **Truth first, predictions second — the same argument order as Week 8's `confusion_matrix`, and swapping them transposes the whole thing silently.**

**New line 4 — stacking tensors.**

```python
X_aug = torch.cat([t4(shift(X_train, dr, dc)) for dr, dc in shifts])
y_aug = torch.cat([ytr] * 5)
```

`torch.cat` glues a list of tensors together along their first dimension. Five copies of 1,257 pictures becomes 6,285 pictures. **And the labels must be glued the same number of times, in the same order** — `[ytr] * 5` makes a list of the same label tensor five times, so row 3,000 of `X_aug` and row 3,000 of `y_aug` still belong together.

**The check to make out loud, every time:** `X_aug.shape[0]` and `y_aug.shape[0]` must be equal, and both must be `5 × 1257 = 6285`.

### 5. The whole results table, and why it is dangerous

Here is the four-row table the homework asks for, with the real numbers:

| row | held-out pile | weights trained | seconds | test accuracy |
|---|---|---:|---:|---:|
| plain | 540 all-digit rows | 1,898 | 3.3 | 0.9796 |
| augmented | 540 all-digit rows | 1,898 | 14.6 | **0.9926** |
| frozen-transfer | **269 rows of 5–9** | 650 | 0.3 | 0.9257 |
| fine-tuned | **269 rows of 5–9** | 1,898 | 1.6 | 0.9665 |

![The See It table](../figures/fig-w27-4-see-it-results-table-four-rows.svg)
*Figure 27.4 — The See It table. Rows 1 and 2 are judged on 540 rows; rows 3 and 4 on 269 different rows. 0.9926 − 0.9796 = +0.0130 is a fair comparison. 0.9926 against 0.9665 is not.*

**Rows 1 and 2 may be compared. Rows 3 and 4 may be compared with each other. Row 2 may not be compared with row 4.** They are measured on different piles of digits, and the second pile is a different and easier problem — five classes instead of ten.

**This is the whole reason the split goes on every row**, and it is the thing you should mark hardest in the homework. A table without the pile named looks like the augmented CNN beat the fine-tuned one by 2.6 points, and that comparison is meaningless. **A table with the pile named makes the mistake impossible to make.**

### 6. The three misconceptions you will actually meet

**Misconception 1 — "more training rows is always better."**
Not if some of them have wrong labels. The wrap-around experiment is the illustration: in the seed-0 run 6,285 rows bought nothing over 1,257, probably because many of the shifted copies had ink teleported to the opposite edge. **Cure:** put the two numbers next to each other — `0.9796` and `0.9796` — and ask *"where did the five times more data go?"*

**Misconception 2 — "transfer learning is always better than starting fresh."**
It is often better and it was not here, and the condition is what matters: **the borrowed network has to know far more than you do.** **Cure:** the scratch control row. `0.9814`, beating both. **This is exactly why you run a control**, and a student who asks "but what would starting from scratch have given?" before you show them has just discovered experimental design.

**Misconception 3 — "the worst pair is 1 and 8" is a diagnosis.**
It is a location, not a diagnosis. **Cure:** the ink-per-column numbers. `0 5 42 93 106 56 9 2` against `0 9 71 87 86 66 11 0`. **Two profiles, almost the same shape, and now you have said something a person could act on.**

### 7. How deep to go, and where to stop

**Go this far:** augmentation with `np.roll`, both versions, both numbers; the axis bug and the test-beats-train alarm; freezing with `requires_grad = False` and the movable-weight count; the frozen, fine-tuned and from-scratch numbers side by side; the ten-class confusion matrix, the pair, and the physical reason; the four-row table with the pile on every row.

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| **Rotation, scaling, elastic distortion** | Not in this level. Shifts are enough and they are the only transform you can do in one line of numpy. If asked: *"rotating an 8×8 digit needs interpolation, and interpolation on sixty-four pixels does more damage than it is worth."* |
| **Downloading a pretrained resnet** | **Not possible offline, and there is one clearly-marked callout about it in the student guide.** Do not make it sound like the real version is elsewhere and this is a toy — the *mechanism* here is identical and the numbers are honest. |
| Class weights, resampling, focal loss for the 1/8 pair | Not in this level. If a student proposes it, admire the instinct and say *"you would be attacking the symptom; the cause is 64 pixels."* |
| Per-class precision and recall on ten classes | **Already theirs since Weeks 8 and 9** and worth one sentence if it comes up, but ten classes means twenty numbers and it will eat the lesson. **The pair is today's unit of analysis.** |
| Learning-rate schedules, discriminative learning rates for fine-tuning | Not in this level. The real version of fine-tuning uses a smaller learning rate for the borrowed layers; say it exists in one sentence if asked. |
| k-means, PCA, clustering | **Week 28 onwards.** Term 4 starts next week and it is a different subject. |

The line to hold in your head all lesson: **today the student runs two experiments and reports what happened, including the bit that did not work.** That is the checkpoint.

---

### 8. 🧭 The Growing Map — stage four closes

The student guide carries a figure called **Where This Fits**: the same picture every week with one more
piece filled in. This week a whole stage finishes, and that is worth the two minutes on its own.

![The Level 3 pipeline in Week 27: the images and CNNs tile closes with augmentation, transfer and the Term 3 checkpoint](../figures/fig-w27-0-where-this-fits.svg)

*Figure 27.0 — Week 27's version. The last week in the gold `images · CNNs` tile; seven tiles are already
black and this one joins them. The ↻ on stage three is black, as it has been since Week 12.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Ask "which box did we do today?" and then "and what did it cost us?"** The box is the same gold
   tile as the last three weeks, *images · CNNs* — and today it closes. The second half of the question
   is this week's specific one: **the two things they tried today were both free of new data, and one of
   them bought nothing.** `+1.30` from blanked-edge augmentation, `+0.00` from naive `np.roll`, and
   transfer at `0.9257` frozen and `0.9665` fine-tuned against a from-scratch control of `0.9814`.
   Pointing at the tile and saying *"that box is finished and two of our four rows were bad news"* is the
   whole checkpoint.
2. **Point at stage one and make them say why only the training set got augmented.** The rule is from
   Week 6 and the box is still on the map: five shifted copies of a **validation** picture would be five
   chances to memorise the same answer. *"Which stage did we obey when we augmented?"* — they should
   point left, at `SPLIT HONESTLY`, not at stage four.
3. **Then point at stage five and say what next week is.** *"Everything we have done for twenty-seven
   weeks had a `y` column. Next week the answer column goes away."* That is the honest headline for Term
   4, and one sentence of it today saves five minutes next lesson.

> **🧑‍🏫 Why this is worth two minutes.** Today's results table contains two disappointments, and a class
> that only sees the table goes home thinking the lesson failed. The map reframes it: **the tile went
> black anyway.** Closing a stage is about being able to run the experiment and report it, not about the
> experiment coming out the way the textbook promised. That distinction is the entire difference between
> Level 2 and Level 3, and the picture is where it lands.

**One thing to notice, so you can answer if asked.** The threads this week are `data` and `evaluation` —
the same pair as Week 6, and that is deliberate. This is the first week the class **manufactured** rows
rather than collecting them, which is a data move, and every claim they made about those rows came with a
control beside it, which is an evaluation move. If somebody asks why `model` is dark in a week that
trained six networks, the answer is good: **nothing new about the model changed today.** They reused Week
26's architecture four times over.

---

## 🧰 Prep Checklist

This section lists what to prepare before the lesson, so nothing surprises you in the room.

### 30 minutes the night before

- [ ] **Type and run `see_it.py` yourself, and time the whole thing.** It is the longest file of the term. The complete file:

```python
"""see_it.py - Term 3 checkpoint: augmentation and transfer, entirely offline."""
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from sklearn.datasets import load_digits
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

np.random.seed(0)

digits = load_digits()
X_train, X_test, y_train, y_test = train_test_split(
    digits.images / 16.0, digits.target, test_size=0.30, random_state=0,
    stratify=digits.target)
print("train rows:", len(X_train), "  test rows:", len(X_test))


def t4(a):
    return torch.from_numpy(np.asarray(a)).float().unsqueeze(1)


Xtr = t4(X_train)
ytr = torch.from_numpy(y_train).long()
Xte = t4(X_test)
yte = torch.from_numpy(y_test).long()


def make_cnn():
    return nn.Sequential(
        nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Flatten(), nn.Linear(64, 10))


def train(model, X, y, epochs=40, lr=1e-3):
    movable = [p for p in model.parameters() if p.requires_grad]
    loader = DataLoader(TensorDataset(X, y), batch_size=32, shuffle=True)
    loss_fn = nn.CrossEntropyLoss()
    opt = torch.optim.Adam(movable, lr=lr)
    t0 = time.perf_counter()
    for _ in range(epochs):
        model.train()
        for xb, yb in loader:
            opt.zero_grad()
            loss_fn(model(xb), yb).backward()
            opt.step()
    return time.perf_counter() - t0


def acc(model, X, y):
    model.eval()
    with torch.no_grad():
        return (model(X).argmax(1) == y).float().mean().item()


def n_movable(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def report(tag, secs, model, Xa, ya, Xb, yb):
    a, b = acc(model, Xa, ya), acc(model, Xb, yb)
    print("%-18s %5.1fs  movable %4d  train %.4f  test %.4f  (%d of %d)"
          % (tag, secs, n_movable(model), a, b, round(b * len(yb)), len(yb)))
    return b


# ---------- 1. shifting a picture with np.roll ----------
one = X_train[0]
print()
print("--- np.roll on one 8x8 picture, top two rows ---")
print("original      :", np.round(one[0], 2), np.round(one[1], 2))
print("rolled down 1 :", np.round(np.roll(one, 1, axis=0)[0], 2),
      np.round(np.roll(one, 1, axis=0)[1], 2))
print("the top row of the rolled copy is the BOTTOM row of the original:")
print("original row 7:", np.round(one[7], 2))


def shift(stack, dr, dc):
    """Shift every picture in the stack, and blank the edge it rolled off."""
    out = np.roll(np.roll(stack, dr, axis=1), dc, axis=2).copy()
    if dr == 1:
        out[:, 0, :] = 0.0
    if dr == -1:
        out[:, -1, :] = 0.0
    if dc == 1:
        out[:, :, 0] = 0.0
    if dc == -1:
        out[:, :, -1] = 0.0
    return out


shifts = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
X_wrap = torch.cat([t4(np.roll(np.roll(X_train, dr, axis=1), dc, axis=2))
                    for dr, dc in shifts])
X_aug = torch.cat([t4(shift(X_train, dr, dc)) for dr, dc in shifts])
y_aug = torch.cat([ytr] * 5)
print()
print("augmented train tensor:", tuple(X_aug.shape), "=", len(X_train), "x 5")
print("test tensor: still", tuple(Xte.shape), "- never shifted")

# ---------- 2. plain, wrapped-augmented, blanked-augmented ----------
print()
torch.manual_seed(0)
plain = make_cnn()
s = train(plain, Xtr, ytr)
a_plain = report("plain", s, plain, Xtr, ytr, Xte, yte)

torch.manual_seed(0)
wrapped = make_cnn()
s = train(wrapped, X_wrap, y_aug)
a_wrap = report("augmented (wrap)", s, wrapped, X_wrap, y_aug, Xte, yte)

torch.manual_seed(0)
aug = make_cnn()
s = train(aug, X_aug, y_aug)
a_aug = report("augmented (blank)", s, aug, X_aug, y_aug, Xte, yte)

print()
print("wrap-around augmentation bought %+.2f points" % (100 * (a_wrap - a_plain)))
print("blanked-edge  augmentation bought %+.2f points" % (100 * (a_aug - a_plain)))

# ---------- 3. transfer: learn on 0-4, move to 5-9 ----------
lo_tr, lo_te = y_train <= 4, y_test <= 4
hi_tr, hi_te = y_train >= 5, y_test >= 5
print()
print("digits 0-4: train %d  test %d" % (lo_tr.sum(), lo_te.sum()))
print("digits 5-9: train %d  test %d" % (hi_tr.sum(), hi_te.sum()))

torch.manual_seed(0)
first = make_cnn()
s = train(first, Xtr[lo_tr], ytr[lo_tr])
print("stage 1, digits 0-4 only: %5.1fs  test %.4f"
      % (s, acc(first, Xte[lo_te], yte[lo_te])))
backbone = {k: v.clone() for k, v in first.state_dict().items()}

torch.manual_seed(0)
frozen = make_cnn()
frozen.load_state_dict(backbone)
frozen[7] = nn.Linear(64, 10)
for layer in (frozen[0], frozen[3]):
    for p in layer.parameters():
        p.requires_grad = False
s = train(frozen, Xtr[hi_tr], ytr[hi_tr])
report("frozen-transfer", s, frozen, Xtr[hi_tr], ytr[hi_tr],
       Xte[hi_te], yte[hi_te])

torch.manual_seed(0)
fine = make_cnn()
fine.load_state_dict(backbone)
fine[7] = nn.Linear(64, 10)
s = train(fine, Xtr[hi_tr], ytr[hi_tr])
report("fine-tuned", s, fine, Xtr[hi_tr], ytr[hi_tr], Xte[hi_te], yte[hi_te])

torch.manual_seed(0)
scratch = make_cnn()
s = train(scratch, Xtr[hi_tr], ytr[hi_tr])
report("scratch on 5-9", s, scratch, Xtr[hi_tr], ytr[hi_tr],
       Xte[hi_te], yte[hi_te])

# ---------- 4. the confusion matrix ----------
print()
with torch.no_grad():
    pred = plain(Xte).argmax(1).numpy()
cm = confusion_matrix(y_test, pred)
print("ten-class confusion matrix, plain CNN, 540 test rows:")
print(cm)
off = sorted(((cm[i, j], i, j) for i in range(10) for j in range(10) if i != j),
             reverse=True)
print()
print("every mistake it made (count, true -> predicted):")
for c, i, j in off:
    if c:
        print("  %d   %d -> %d" % (c, i, j))
print("mistakes in total:", int(cm.sum() - np.trace(cm)), "out of", int(cm.sum()))
pair = max(((cm[i, j] + cm[j, i], i, j)
            for i in range(10) for j in range(i + 1, 10)))
print("worst pair: %d and %d, with %d mistakes between them"
      % (pair[1], pair[2], pair[0]))

ConfusionMatrixDisplay.from_predictions(y_test, pred, cmap="Blues",
                                        colorbar=False)
plt.title("plain CNN, 540 held-out digits")
plt.tight_layout()
plt.savefig("confusion.png", dpi=110)
plt.close()
print("saved confusion.png")

print()
print("--- why 1 and 8 collide at 8x8 ---")
for lab in (1, 8):
    m = digits.images[digits.target == lab].mean(axis=0)
    print("average %d, ink per column:" % lab, m.sum(axis=0).round(0).astype(int))
```

Run `python3 see_it.py`. You must see **exactly** this, except the `s` columns:

```text
train rows: 1257   test rows: 540

--- np.roll on one 8x8 picture, top two rows ---
original      : [0.   0.   0.   0.5  0.44 0.   0.   0.  ] [0.   0.   0.25 1.   0.69 0.   0.   0.  ]
rolled down 1 : [0.   0.   0.   0.31 0.88 1.   0.25 0.  ] [0.   0.   0.   0.5  0.44 0.   0.   0.  ]
the top row of the rolled copy is the BOTTOM row of the original:
original row 7: [0.   0.   0.   0.31 0.88 1.   0.25 0.  ]

augmented train tensor: (6285, 1, 8, 8) = 1257 x 5
test tensor: still (540, 1, 8, 8) - never shifted

plain                3.3s  movable 1898  train 0.9881  test 0.9796  (529 of 540)
augmented (wrap)    16.4s  movable 1898  train 0.9774  test 0.9796  (529 of 540)
augmented (blank)   14.6s  movable 1898  train 0.9893  test 0.9926  (536 of 540)

wrap-around augmentation bought +0.00 points
blanked-edge  augmentation bought +1.30 points

digits 0-4: train 630  test 271
digits 5-9: train 627  test 269
stage 1, digits 0-4 only:   1.4s  test 0.9926
frozen-transfer      0.3s  movable  650  train 0.9330  test 0.9257  (249 of 269)
fine-tuned           1.6s  movable 1898  train 0.9841  test 0.9665  (260 of 269)
scratch on 5-9       1.5s  movable 1898  train 0.9729  test 0.9814  (264 of 269)

ten-class confusion matrix, plain CNN, 540 test rows:
[[54  0  0  0  0  0  0  0  0  0]
 [ 0 53  0  0  0  1  0  0  1  0]
 [ 0  1 52  0  0  0  0  0  0  0]
 [ 0  0  0 53  0  1  0  1  0  0]
 [ 0  0  0  0 53  0  0  0  0  1]
 [ 0  0  0  0  0 55  0  0  0  0]
 [ 0  1  0  0  0  0 53  0  0  0]
 [ 0  0  0  0  0  0  0 54  0  0]
 [ 0  3  0  0  0  0  0  1 48  0]
 [ 0  0  0  0  0  0  0  0  0 54]]

every mistake it made (count, true -> predicted):
  3   8 -> 1
  1   8 -> 7
  1   6 -> 1
  1   4 -> 9
  1   3 -> 7
  1   3 -> 5
  1   2 -> 1
  1   1 -> 8
  1   1 -> 5
mistakes in total: 11 out of 540
worst pair: 1 and 8, with 4 mistakes between them
saved confusion.png

--- why 1 and 8 collide at 8x8 ---
average 1, ink per column: [  0   5  42  93 106  56   9   2]
average 8, ink per column: [ 0  9 71 87 86 66 11  0]
```

**Expected runtime: about 40 seconds in total on this machine**, of which the two augmented runs are about 15 seconds each. **Time yours and write it down.** On a slow laptop this can be three minutes, and you need to plan the lesson around that rather than discover it.

**If `blanked-edge augmentation bought +1.30 points` does not appear, one of the seeds is missing.** `np.random.seed(0)` at the top, `random_state=0, stratify=y` in the split, and `torch.manual_seed(0)` before **every single** `make_cnn()`. All six matter.

- [ ] **Break the axis on purpose.** Change `axis=1` and `axis=2` to `axis=0` and `axis=1` in the augmentation and run it. You get, with no error at all:

```text
trained on the WRONG axis: train 0.5968  test 0.8574
```

**Look at those two numbers and say the alarm out loud: the test accuracy is higher than the training accuracy.** That is impossible for an honest model, and it means the training labels are wrong. This is deliberate mistake one.

- [ ] **Do the confusion-matrix addition check yourself.** The diagonal sums to 529, the off-diagonal to 11, 529 + 11 = 540. **One minute, and it is the check you make the class do.**
- [ ] **Print the workbook** (`workbook/week-27.md`, one copy). It has sections, not numbered pages; the ones you use in class are Build It (checklist step 1, the predictions) and Practice Set A, item A2.
- [ ] **Have a plain sheet of lined paper ready for the six showcase lines**, one per station.
- [ ] **Put up the FROZEN / UNFROZEN sheet:** two columns, three blank rows each (`movable weights`, `seconds`, `test accuracy`). It gets filled in live in the activity.
- [ ] **Print the six Term 3 showcase station cards.** One card each, and each card has two things on it and nothing else: **what you show** and **the one number you say out loud.** The six are in the Activity section. **Ten minutes to print and lay out, and it is the difference between a showcase and a shuffle.**
- [ ] **Check both wall sheets from earlier weeks are still up** — PARAMETER COUNT from Week 22, THE SHAPE LADDER from Week 25. **You take them both down at the end of today**, and doing it deliberately, in front of the class, is a small ceremony worth having.
- [ ] **Check the student's Week 26 `digits_cnn.py` still runs.** Today's first table row is that file's number, and a broken file turns a five-minute recap into twenty.

### 10 minutes on the day

- [ ] Six station cards laid out around the room, in order, with space to stand at each.
- [ ] Editor open, terminal ready. `see_it.py` **partly** given: hand them the `make_cnn`, `train`, `acc` and `report` helper functions complete, because they wrote all four of those in Weeks 23 and 26 and retyping them costs eight minutes today. **They type the augmentation and the freezing themselves** — those are the new lines.
- [ ] FROZEN / UNFROZEN sheet on the wall, blank.
- [ ] PARAMETER COUNT and THE SHAPE LADDER both still up.
- [ ] Workbook open at Build It, checklist step 1. **The three predictions written on paper, in pen, before anything runs.**
- [ ] Bug Log out. **It is the last week of the term and it should be thick by now — you point at it once.**

### Fallback if the laptops fail

**This week is a checkpoint, and a checkpoint on paper is still a checkpoint.** Three of the four objectives survive intact.

1. **The showcase circuit, unchanged.** Six stations, six things they built, six numbers said out loud. **It needs no electricity if they bring their printed figures and workbooks**, and honestly it goes better without screens because nobody is fiddling.
2. **The confusion matrix, from this file.** Write the ten-by-ten on the board or print Figure 27.3. **Then the whole of objective 3 on paper:** find the diagonal, add it, find the eleven off it, add them, check they make 540, find the pair. **And then the ink-per-column numbers and the physical diagnosis, which is a discussion and not a computation.** This is the best twenty minutes of the paper version.
3. **The four-row table, from this file's numbers.** Objective 4 is a table and a sentence, and it needs no machine. **The pile-naming discipline is the objective, and paper enforces it better than a screen.**
4. **The augmentation arithmetic.** `1,257 × 5 = 6,285`. Then draw an 8×8 digit on squared paper and shift it one square down by hand, and see what falls off the bottom. **Objective 1's understanding, without objective 1's measurement.**
5. **Objective 2 is the casualty.** Say so: *"the one thing we cannot do on paper is freeze a backbone and watch it lose. The numbers are 0.9257 frozen, 0.9665 unfrozen, 0.9814 from scratch, and it is your homework to make them yourself."*

| If this fails | Do this instead |
|---|---|
| The augmented run takes three minutes and the room goes quiet | **Start it running and teach the confusion matrix while it works.** Say that is what you are doing. It is what a real engineer does and modelling it is worth more than a tidy schedule. |
| `blanked-edge augmentation bought +0.00` | You are running the wrap version, or the blanking is missing or on the wrong edge. (`.copy()` is belt and braces: `np.roll` already returns a fresh array, but slices and `.T` are views.) |
| `ValueError: optimizer got an empty parameter list` | Everything got frozen, including the new head. Freeze `frozen[0]` and `frozen[3]` only — the two convs. |
| `RuntimeError: Error(s) in loading state_dict ... size mismatch for 7.weight` | The head was replaced *before* `load_state_dict` instead of after. **Load the whole thing first, then swap the head.** |
| Transfer beats scratch on somebody's machine | It should not with these seeds, but if it does, **that is a result and you say so.** *"On your run the borrowed backbone helped and on mine it did not. What would settle it?"* More seeds. **That conversation is better than the tidy answer.** |
| A student is upset that transfer learning "didn't work" | *"It worked exactly as designed. What we measured is the condition it needs. A technique with a known price is more useful than one you believe in."* |
| The six stations turn into a queue | The cards are too long. **Each card says what to show and one number to say. Nothing else.** Trim them in front of the class if you have to. |

---

## ⏱️ The Lesson, Minute by Minute

This section is the plan for the whole lesson, one step at a time.

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Eleven Digits, and Two Ways to Fix Them | 7 | 7 | Last week's eleven; the confusion matrix; the pair |
| 🧠 Concept — Free Pictures, Borrowed Eyes | 18 | 25 | Augmentation, the wrap trap, freezing, backbone and head |
| 💻 Live-Code Together — `see_it.py` | 18 | 43 | The five copies, both augmented runs. **Two deliberate mistakes.** |
| 🎲 Their Turn — Showcase Circuit + Honest Transfer | 20 | 63 | Six stations, then the frozen/unfrozen numbers on the board |
| 🔑 Wrap & Assign | 7 | 70 | The four-row table, three checks, the wall sheets come down |

---

### 🪝 Hook — Eleven Digits, and Two Ways to Fix Them (7 minutes)

**Do this:** Nothing on the screen. Write two numbers on the board:

```text
529    of 540 right
 11    wrong
```

**Say this:**

> "Last week your network read 529 of 540 handwritten digits it had never seen, in about three seconds, with 1,898 numbers that started as noise. That is a good result and you should be pleased with it.
>
> And eleven of them came back wrong. Last week I said we would find out which eleven. Here they are."

**Do this:** Put the ten-by-ten confusion matrix on the screen, or draw it — it is mostly zeros, so drawing it takes ninety seconds if you only write the non-zero cells.

```text
[[54  0  0  0  0  0  0  0  0  0]
 [ 0 53  0  0  0  1  0  0  1  0]
 [ 0  1 52  0  0  0  0  0  0  0]
 [ 0  0  0 53  0  1  0  1  0  0]
 [ 0  0  0  0 53  0  0  0  0  1]
 [ 0  0  0  0  0 55  0  0  0  0]
 [ 0  1  0  0  0  0 53  0  0  0]
 [ 0  0  0  0  0  0  0 54  0  0]
 [ 0  3  0  0  0  0  0  1 48  0]
 [ 0  0  0  0  0  0  0  0  0 54]]
```

**Say this:**

> "Week 8's two-by-two, grown up. **Rows are what the digit really was. Columns are what the model said.** So the number in row 8, column 1 is 'real eights that the model called a one'."

**Ask this:** "Add up the diagonal. What do you get?"

*529.*

**Ask this:** "Add up everything that is not on the diagonal."

*11.*

**Ask this:** "And what must those two add up to?"

*540 — the number of test rows.*

> "**529 plus 11 is 540.** Do that check every single time you look at one of these. Week 8's rule and it has not changed: **a matrix whose cells do not add to the number of rows has an arithmetic mistake in it.**"

**Ask this:** "Now find the biggest number that is *not* on the diagonal."

*Row 8, column 1: three.*

**Ask this:** "So what happened three times?"

*A real 8 was called a 1.*

**Ask this:** "And is there anything in the mirror position — row 1, column 8?"

*One.*

> "**Three eights called one, and one one called eight. Four mistakes out of eleven, from one pair of digits out of the forty-five possible pairs.** More than a third of every mistake the model made.
>
> That has a name: it is a **confusion pair**. And finding it is the difference between 'the model is 98% accurate' and 'the model cannot reliably tell an 8 from a 1'. **One of those two sentences you can act on.**
>
> So. We have eleven wrong, four of them from one pair, and here is the constraint. **You may not collect any new pictures.** No downloads, no scanner, nothing. The 1,257 digits you have are all the digits there will ever be.
>
> **Two things you can still do.** One: make more pictures out of the ones you already own. Two: borrow a network that already learned to see, and only teach it the last bit.
>
> Today you do both, and — and I want to be straight with you about this before we start — **one of them works and one of them does not.** Finding out which is the whole lesson."

---

### 🧠 Concept — Free Pictures, Borrowed Eyes (18 minutes)

**Say this:**

> "Here is a fact about a handwritten 6. If I slide it one pixel to the left, **it is still a 6.** You know that. Your network does not. It has to learn it, and learning it costs training rows.
>
> Unless you just... tell it."

**Do this:** Write on the board and box it:

> **Data augmentation** — making extra training rows out of the ones you have, by changing them in ways that **do not change the label**.

**Say this:**

> "Every digit, four extra copies: one pixel up, one down, one left, one right. **1,257 rows becomes 6,285.** Five times the data and I collected nothing.
>
> The tool is one numpy function. `np.roll`. And there is exactly one thing you need to know about it."

**Do this:** Draw an 8×8 grid on the board, with a rough digit in it — three or four squares shaded in the bottom row. Then draw the shifted version beside it, sliding everything down one.

**Ask this:** "The bottom row slid off the edge. Where did it go?"

*Let them guess. Most will say "it's gone" or "it's blank".*

> "That is what you would want. **What `np.roll` actually does is bring it round to the top.** It wraps."

**Do this:** Shade the same squares in the *top* row of the shifted grid. Then show the real numbers from the file:

```text
original      : [0.  0.  0.  0.5  0.44 0.  0.  0. ]      ← row 0
rolled down 1 : [0.  0.  0.  0.31 0.88 1.   0.25 0. ]    ← the new row 0
original row 7: [0.  0.  0.  0.31 0.88 1.   0.25 0. ]    ← identical
```

**Ask this:** "Those two rows are the same. What has happened to the picture?"

*The bottom of the digit is now at the top.*

**Ask this:** "Is it still a 6?"

*No.*

> "**No. And the label still says 6.** So you have just manufactured a training row with a wrong label, and you have done it 1,257 times.
>
> On a big photograph with a dark border you would never notice — the border wraps onto the border and nothing changes. **On an 8×8 digit that fills the frame, it is a real problem**, and you are going to measure exactly how much of one."

**Do this:** Write on the board and leave it up:

```text
np.roll wraps.  BLANK the edge it rolled off.
```

> "Three lines and it is fixed: after you roll, set the row or column that wrapped to zero. And you are about to see what those three lines are worth in accuracy points."

**Do this:** Now the second idea. Write on the board:

> **Backbone** — the conv layers. They turn a picture into features.
> **Head** — the small dense bit at the end. It turns features into an answer.

**Say this:**

> "Look at those eight filters you rendered last week. **Two of them were edge detectors.** Now: is 'there is a vertical edge here' useful for reading a 3?"

*Yes.*

> "Is it useful for reading a 7? A 9? A letter? **A face?**"

*Yes.*

> "**Edges are useful for looking at anything.** They are not about digits. They are about pictures. So if somebody has already paid for a network that learned to find edges, why would you start from noise?
>
> That is **transfer learning**: keep the backbone, throw away the head, bolt on a new head, and train only that."

**Do this:** Write:

> **Freezing** — telling PyTorch a block of weights may not change. `p.requires_grad = False`.

> "`requires_grad` is Week 20's flag, and this is the first week you turn it **off**. Set it to `False` and the backward pass stops computing a slope for that block, so nothing can move it. The conv layers become a fixed piece of machinery: pictures go in, features come out, and it is the same features every time.
>
> Which means only the head is learning. **650 numbers instead of 1,898.**"

**Ask this:** "We have no internet, so nobody can hand us a network trained on a million photos. How can we test this idea with what we have?"

*Take answers. Steer towards: train on some of the digits, then move to the others.*

> "Exactly. **Two problems out of one dataset.** Train the whole network on digits **0 to 4** only — 630 rows. Then a new problem: digits **5 to 9** — 627 rows, and shapes it has genuinely never seen. Keep the backbone from the first job. New head. Train.
>
> And here is the question I want you to write down, in pen, before we run anything, because it is the question that makes this an experiment and not a demonstration."

**Do this:** Write on the board, big:

```text
what would training from scratch on the 5-to-9 rows have given?
```

> "**If you do not measure that, you cannot claim anything.** If the frozen version gets 92% and you have nothing to compare it to, 92% is a number, not a result. **That third run is called a control and it is not optional.**"

**Do this:** Hand out the workbook's Build It section, checklist step 1 — the three predictions, in pen, on paper. Four minutes.

> "Pen. Three predictions. **Will the wrapped version beat the plain one? Will the blanked version? And which will win out of frozen, fine-tuned, and from scratch?** I want to see what you actually thought."

---

### 💻 Live-Code Together — `see_it.py` (18 minutes)

**You never touch their keyboard.** The helper functions — `make_cnn`, `train`, `acc`, `report` — are given complete; they wrote all four in Weeks 23 and 26. **They type the new lines.**

**Step 1 (4 min) — one picture, five ways.**

```python
one = X_train[0]
print("original      :", np.round(one[0], 2))
print("rolled down 1 :", np.round(np.roll(one, 1, axis=0)[0], 2))
print("original row 7:", np.round(one[7], 2))
```

```text
original      : [0.   0.   0.   0.5  0.44 0.   0.   0.  ]
rolled down 1 : [0.   0.   0.   0.31 0.88 1.   0.25 0.  ]
original row 7: [0.   0.   0.   0.31 0.88 1.   0.25 0.  ]
```

> **Say this:** "Line two and line three are identical. **The bottom row of the digit is now the top row.** That is the wrap, on real data, and it is the reason for the next three lines."

Then the shift function, typed by them:

```python
def shift(stack, dr, dc):
    """Shift every picture in the stack, and blank the edge it rolled off."""
    out = np.roll(np.roll(stack, dr, axis=1), dc, axis=2).copy()
    if dr == 1:
        out[:, 0, :] = 0.0
    if dr == -1:
        out[:, -1, :] = 0.0
    if dc == 1:
        out[:, :, 0] = 0.0
    if dc == -1:
        out[:, :, -1] = 0.0
    return out
```

> **Say this:** "Read the axes. `stack` is 1,257 pictures of 8 by 8, so it is `(1257, 8, 8)`. **`axis=1` is the rows of each picture. `axis=2` is the columns.** And `axis=0` would be *which picture*, which we will come back to in about four minutes with a horror story.
>
> `out[:, 0, :] = 0.0` means: every picture, row 0, all columns — set to zero. **If you rolled down, the top row is the wrapped junk, so blank it.**
>
> And `.copy()` is belt and braces. `np.roll` already hands back a fresh array (you can check with `np.shares_memory`), but slices and `.T` hand back **views** of the original, and blanking a view would blank the real data. **One word, and you never have to remember which functions do which.**"

**Step 2 (3 min) — five copies, glued.**

```python
shifts = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
X_aug = torch.cat([t4(shift(X_train, dr, dc)) for dr, dc in shifts])
y_aug = torch.cat([ytr] * 5)
print("augmented train tensor:", tuple(X_aug.shape), "=", len(X_train), "x 5")
print("test tensor: still", tuple(Xte.shape), "- never shifted")
```

**Ask before running:** "1,257 rows, five copies. What shape?"

```text
augmented train tensor: (6285, 1, 8, 8) = 1257 x 5
test tensor: still (540, 1, 8, 8) - never shifted
```

> **Say this:** "**6,285.** And `torch.cat` glued five tensors into one along the first dimension — the batch dimension, the one Week 25 said always rides along untouched.
>
> `[ytr] * 5` makes a list of the same label tensor five times, and `torch.cat` glues those too. **The check to make out loud every single time: are there as many labels as pictures?** 6,285 and 6,285. If those two numbers differ, everything after it is nonsense and nothing will tell you.
>
> And look at the second line: **the test tensor is still 540, and it was never shifted.** Never augment the test set. Two reasons: evaluation has to give the same answer twice, and augmentation makes pictures harder so the number would come out too low. **Week 6's fit-on-train-only rule in a new costume.**"

**Step 3 (5 min) — run all three, and the honest surprise.**

```python
torch.manual_seed(0)
plain = make_cnn()
s = train(plain, Xtr, ytr)
a_plain = report("plain", s, plain, Xtr, ytr, Xte, yte)

torch.manual_seed(0)
wrapped = make_cnn()
s = train(wrapped, X_wrap, y_aug)
a_wrap = report("augmented (wrap)", s, wrapped, X_wrap, y_aug, Xte, yte)

torch.manual_seed(0)
aug = make_cnn()
s = train(aug, X_aug, y_aug)
a_aug = report("augmented (blank)", s, aug, X_aug, y_aug, Xte, yte)

print("wrap-around augmentation bought %+.2f points" % (100 * (a_wrap - a_plain)))
print("blanked-edge  augmentation bought %+.2f points" % (100 * (a_aug - a_plain)))
```

**Do this:** Before running, collect their written predictions (Build It, step 1) and write the votes on the board. Then run it. **It takes about half a minute and you should let the silence happen.**

```text
plain                3.3s  movable 1898  train 0.9881  test 0.9796  (529 of 540)
augmented (wrap)    16.4s  movable 1898  train 0.9774  test 0.9796  (529 of 540)
augmented (blank)   14.6s  movable 1898  train 0.9893  test 0.9926  (536 of 540)

wrap-around augmentation bought +0.00 points
blanked-edge  augmentation bought +1.30 points
```

**Do this:** Say nothing for five seconds. Point at the two `529 of 540`s.

**Ask this:** "Five times the training data. Five times the training time. **What did the wrapped version buy?**"

*Nothing, this time: the identical 529.*

> **Say this:** "**Zero, this time — the identical 529 out of 540** (a tie like that is a seed-0 coincidence; across seeds it is "no reliable benefit"). Five times the data and five times the wait for nothing, most likely because all four shifted copies (four fifths of the 6,285 rows) had ink teleported from one edge to the opposite one and a label that no longer described the picture.
>
> **And now the three lines that blank the edge.** `536 of 540`. **Seven more digits, +1.30 accuracy points, and no new data.**
>
> Look at the training accuracies too, because they tell the story. Plain trained to 0.9881. The wrapped one only got to **0.9774** — *worse on its own training data*, because some of that data was unlearnable nonsense. The blanked one got to 0.9893, slightly better than plain, on five times as many rows.
>
> **This is what augmentation actually is.** It is not 'more data is better'. It is **'more data is better if the label is still true'**, and the whole engineering skill is knowing when it stops being true. Flip a photo of a cat: still a cat. **Flip a photo of a 2: not a 2 any more.** Mirror a road sign with writing on it: nonsense. **There is no universal list. You have to think about your data.**"

**Step 4 (3 min) — 🐞 DELIBERATE MISTAKE ONE: the wrong axis.**

> **Say this:** "Let me try that again. I can never remember which axis is which, so let me just use zero and one."

Change the two axes and run:

```python
X_bad = torch.cat([t4(np.roll(np.roll(X_train, dr, axis=0), dc, axis=1))
                   for dr, dc in shifts])
torch.manual_seed(0)
bad = make_cnn()
s = train(bad, X_bad, y_aug)
report("wrong axis", s, bad, X_bad, y_aug, Xte, yte)
```

```text
wrong axis          11.5s  movable 1898  train 0.5968  test 0.8574  (463 of 540)
```

**Do this:** Say nothing. Point at `train 0.5968` and then at `test 0.8574`.

**Ask this:** "Something about those two numbers is impossible. What?"

*Hoped-for answer:* the test accuracy is higher than the training accuracy.

> **Say this:** "**The test score is higher than the training score.** That should very rarely happen. A model has *seen* the training data, so it normally does at least as well on it.
>
> So what did I actually do? `axis=0` on a stack of 1,257 pictures is not the rows of a picture — **it is which picture.** I shuffled the pictures round while the labels stayed exactly where they were. Two fifths of my training rows (the up and down copies) are pictures paired with somebody else's label. **Unlearnable.** The other three fifths keep their right labels, so the model scored 0.5968 on its own partly scrambled homework, close to the 0.6 that three correct fifths allow, and 0.8574 on the untouched test set.
>
> **And nothing went red. No error, no warning, no hint of any kind.** Twelve seconds of training and a plausible-looking 85%.
>
> Take one alarm away from today and make it this one: **if your test accuracy is higher than your training accuracy, your training labels are wrong.** Write it in the Bug Log."

**Do this:** Bug Log. **Most valuable entry of the term.** Message: *"no message"*. Meaning: *"axis=0 shifted the pictures instead of the pixels, so pictures and labels no longer matched"*. Fix: *"axis=1 is rows, axis=2 is columns, on a stack of pictures"*. Alarm: *"test above train means the training labels are wrong"*.

**Step 5 (3 min) — freezing, and 🐞 DELIBERATE MISTAKE TWO.**

```python
torch.manual_seed(0)
first = make_cnn()
s = train(first, Xtr[lo_tr], ytr[lo_tr])
print("stage 1, digits 0-4 only: %5.1fs  test %.4f"
      % (s, acc(first, Xte[lo_te], yte[lo_te])))
backbone = {k: v.clone() for k, v in first.state_dict().items()}

torch.manual_seed(0)
frozen = make_cnn()
frozen[7] = nn.Linear(64, 10)          # <-- the mistake: head swapped FIRST
frozen.load_state_dict(backbone)
```

Real output:

```text
stage 1, digits 0-4 only:   1.4s  test 0.9926
RuntimeError: Error(s) in loading state_dict for Sequential:
	size mismatch for 7.weight: copying a param with shape torch.Size([10, 64]) ...
```

**Do this:** Read the last line out loud, slowly. Point at the word `size mismatch`.

**Ask this:** "It is comparing two things. What order did I do them in, and what order should I have?"

*Hoped-for answer:* load first, then swap the head.

> **Say this:** "**Load the whole saved network first, then throw the head away.** I did it the other way round, so I asked PyTorch to pour a 10-by-64 head into a slot I had just replaced — and this time, thankfully, it noticed. **Week 25's error, one week older**: two shapes named in the message, and one of them is mine."

Fix it live, in the right order, and add the freezing:

```python
torch.manual_seed(0)
frozen = make_cnn()
frozen.load_state_dict(backbone)
frozen[7] = nn.Linear(64, 10)
for layer in (frozen[0], frozen[3]):
    for p in layer.parameters():
        p.requires_grad = False
print("movable weights:", sum(p.numel() for p in frozen.parameters()
                              if p.requires_grad))
```

```text
movable weights: 650
```

> **Say this:** "**650, not 1,898.** That line is not decoration — it is the only proof that the freezing actually worked. `requires_grad = False` fails silently if you point it at the wrong layer, and this print catches it.
>
> And one honest warning: if you hand **all** the parameters to Adam, including the frozen ones, **there is no error.** The frozen ones just have no slope and never move. It works, and it hides what you meant. So build the list yourself: `[p for p in model.parameters() if p.requires_grad]`."

---

### 🎲 Their Turn — Showcase Circuit + Honest Transfer (20 minutes)

Full instructions in **🎲 The Activity, In Full** below. In outline: **twelve minutes** walking six stations, one per thing they built this term, saying one number out loud at each; then **eight minutes** running the three transfer numbers and putting the frozen and unfrozen results on the board side by side, with the from-scratch control next to them.

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Stand at the FROZEN / UNFROZEN sheet with all three numbers on it.

```text
                        movable weights   seconds   test accuracy
frozen backbone                    650       0.3          0.9257
unfrozen (fine-tuned)            1,898       1.6          0.9665
from scratch, no borrowing       1,898       1.5          0.9814
```

**Ask this:** "Which one won?"

*From scratch.*

**Say this:**

> "**Starting from nothing beat both of them.** And I told you at the start of the lesson that one of today's two ideas would not work, so nobody should be shocked. But we are going to say clearly *why*, because the why is the actual lesson.
>
> **Transfer learning pays when the thing you borrow from knows far more than you do.** The version people use at work borrows a backbone trained on **1.2 million photographs** and applies it to a few thousand pictures of something else. **We borrowed a backbone trained on 630 pictures of five digits, and used it for 627 pictures of five different digits.** The source was not bigger than the target — it was the same size, and it was *specialised*. Those eight filters were tuned for the shapes of 0, 1, 2, 3 and 4. **A 5 is not a 3.**
>
> And notice what the frozen version *did* buy, because this part is real: **650 weights instead of 1,898, in 0.3 seconds instead of 1.5, and it still got to 92.6%.** A third of the weights, a fifth of the time, six points behind. **If the backbone had come from a million photographs and your target set were fifty pictures rather than 627, that trade would be the difference between a working model and no model at all.**
>
> **So the honest sentence for your write-up is not 'transfer learning does not work'. It is: 'transfer learning bought a fifth of the training time and a third of the weights, and cost 5.6 accuracy points; a likely reason is that the borrowed backbone was trained on no more data than we already had (a hypothesis we did not test).'** That sentence is worth more than a triumph would have been."

**Do this:** Now the four-row table on the board, and make the split explicit in every row.

| row | held-out pile | weights trained | seconds | test accuracy |
|---|---|---:|---:|---:|
| plain | 540 all-digit rows | 1,898 | 3.3 | 0.9796 |
| augmented | 540 all-digit rows | 1,898 | 14.6 | **0.9926** |
| frozen-transfer | **269 rows of 5–9** | 650 | 0.3 | 0.9257 |
| fine-tuned | **269 rows of 5–9** | 1,898 | 1.6 | 0.9665 |

**Ask this:** "The best number on that table is 0.9926 and the worst is 0.9257. **Can I say augmentation is 6.7 points better than frozen transfer?**"

*Hoped-for answer:* no — different test sets.

> "**No.** Rows 1 and 2 were judged on 540 digits, all ten classes. Rows 3 and 4 were judged on 269 digits, five classes, and five classes is an easier problem than ten. **Those are two different exams and you cannot compare marks across them.**
>
> `0.9926 − 0.9796 = +0.0130` — **that is a fair comparison**, same 540 rows, same ten classes, one thing changed.
>
> `0.9665 − 0.9257 = +0.0408` — **also fair**, same 269 rows.
>
> `0.9926` against `0.9665` — **not a comparison at all.**
>
> Which is why **the pile goes on every single row.** Not because it is tidy. Because a table without it lets you make that mistake, and it lets your reader make it too, and you will not be there to stop them."

**Do this:** Three quick checks — exact wording in **✅ Assessing Understanding**.

**Do this:** Take down THE SHAPE LADDER and the PARAMETER COUNT sheet, deliberately, in front of them.

**Say this, to close:**

> "These two come down today.
>
> This one" — hold up THE SHAPE LADDER — "you filled in with a piece of card and a division. **You will not need it on the wall again, because you can rebuild it in your head.**
>
> And this one" — hold up PARAMETER COUNT — "started in Week 22 with `2 → 16 → 1 = 65`, and it finishes with `CNN on digits: 1,898`. **You have priced every network you have built this year, by hand, before running it. Almost nobody does that.**
>
> That is Term 3. Twenty weeks ago you had never seen a derivative. **Today you trained a thing that can see, looked at what it decided to look for, found the one pair of digits it cannot tell apart, worked out physically why, and then ran two experiments where you reported the one that failed.** The last one is the hardest and it is the one that makes you an engineer.
>
> Next week is a completely different subject: **sorting things when nobody gives you the answers.** No labels at all."

**Do this:** Hand out the homework and read the second part out loud, slowly.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `RuntimeError: Error(s) in loading state_dict for Sequential: size mismatch for 7.weight: copying a param with shape torch.Size([10, 64]) from checkpoint, the shape in current model is torch.Size([5, 64]).` | "The saved head and the head in this model are different sizes." | The head was replaced **before** `load_state_dict`, or a 5-output head was built when the saved one had 10. | **Load the whole saved network first, then swap the head.** And read the message: it names both shapes, and Week 25's question still applies — which one did you type? |
| `ValueError: optimizer got an empty parameter list` | "You told me to train nothing." | Everything got frozen, head included — usually `for p in model.parameters(): p.requires_grad = False` with no exception for the new head. | Freeze the **conv layers only**: `frozen[0]` and `frozen[3]`. Then check with `sum(p.numel() for p in model.parameters() if p.requires_grad)` — it must print **650**, not 0 and not 1,898. |
| `RuntimeError: Tensors must have same number of dimensions: got 4 and 3` | "You are gluing a batch of pictures to something that is not one." | `torch.cat` on a mix of `(n, 1, 8, 8)` and `(n, 8, 8)` — one of the copies missed its `.unsqueeze(1)`. | Put every copy through the same helper. **If you build tensors two different ways in one file, one of them will be wrong.** |
| `TypeError: expected Tensor as element 0 in argument 0, but got numpy.ndarray` | "That is a numpy array, not a tensor." | `torch.cat([np.roll(...), ...])` — the shifted copies never became tensors. | `torch.from_numpy(a).float()` on each copy, or wrap them all in one `t4()` helper. **`torch.cat` only glues tensors; `np.concatenate` only glues arrays. Never mix them.** |
| `ValueError: Found input variables with inconsistent numbers of samples: [540, 269]` | "You gave me 540 truths and 269 predictions." | `ConfusionMatrixDisplay.from_predictions(y_test, pred)` where `pred` came from the digits-5-to-9 model but `y_test` is all ten classes. | Predict on the **same rows** you are scoring: `y_test[hi_te]` with `pred` from `Xte[hi_te]`. **Print both lengths before you call it.** |
| `RuntimeError: mean(): could not infer output dtype ... Got: Bool` | "You averaged a list of true/falses." | `(pred == y).mean()`. | `(pred == y).float().mean()`. Same as last week. |
| `ValueError: could not broadcast input array from shape (8,) into shape (1257,)` | "You tried to blank a row and hit the wrong axis." | `out[0, :, :] = 0` instead of `out[:, 0, :] = 0` — that blanks **picture 0** rather than **row 0 of every picture**. | `out[:, 0, :] = 0.0`. **The first slot is always which picture.** |
| **No error. Augmentation buys about 0.00 points (exactly 0.00 with seed 0).** | Nothing crashed. Five times the data, no benefit. | The rolled-off edge was never blanked, so a fifth of the extra rows have ink teleported across the picture and a label that no longer fits. | Blank the edge. **And notice the tell: the augmented model's *training* accuracy is lower than the plain model's (0.9774 against 0.9881) — it fits its own data less well, which fits with some of it being wrong, though it is a hint, not a proof: the two accuracies are measured on different rows.** |
| **No error. Test accuracy is HIGHER than training accuracy.** | Nothing crashed. Your training labels are the first suspect. | `axis=0` instead of `axis=1` — the pictures got shuffled and the labels did not follow. | `axis=1` is rows, `axis=2` is columns, on a stack of pictures. **And make this a permanent alarm: test above train is very rarely a lucky run, and a labelling bug is the first thing to check.** |
| **No error. The frozen model's accuracy is identical to the unfrozen one.** | Nothing crashed. The freezing did nothing. | `requires_grad = False` was set on the wrong layers, or set on a copy, or set *after* the optimiser was built with all the parameters. | `print(sum(p.numel() for p in model.parameters() if p.requires_grad))`. **If it says 1,898, nothing is frozen.** Freeze first, build the optimiser second. |
| **No error. The augmented set has 6,285 pictures and 1,257 labels.** | Nothing crashed yet — the `DataLoader` will error later with something confusing. | `torch.cat` on the pictures but not on the labels. | `y_aug = torch.cat([ytr] * 5)`. **Print both lengths and check they match, every time you build a dataset.** |

### How to teach debugging without giving the answer

All the old moves stand. This week adds three, and it is the last set of the term.

23. **"Is your test accuracy higher than your training accuracy?"** If yes, stop everything. It is very often a labelling bug, so check the labels first (dropout or augmentation on the training path, or a small or easy test split, can also do it).

24. **"How many weights are actually allowed to move?"** One line, and it is the only proof that `requires_grad = False` did anything. **A freeze you have not counted is a freeze you have not done.**

25. **"How many pictures, and how many labels?"** Every time a dataset is built or glued. The two numbers must be equal and nothing will tell you if they are not.

And the sentence for this week, and for the term:

> **"The three most expensive bugs of Term 3 produced no error message at all: the double softmax, the wrong roll axis, and a freeze that did not freeze. All three are caught by printing one number you can predict in advance — the starting loss should be 2.30, the test score should be below the train score, and the movable weight count should be the number you meant."**

---

## 🎲 The Activity, In Full

### Part A — The Term 3 Showcase Circuit (12 minutes)

**What it is.** Six stations round the room, one per thing they built this term. They walk the circuit in order and at each one they do exactly two things: **show it, and say one number out loud.** Two minutes per station, timed.

**Why it is worth twelve minutes of a checkpoint.** Term 3 was the hardest term of the year — autograd, layers, batches, convolution, shapes, a trained CNN. **A student who cannot narrate it does not know they have done it.** The circuit is not revision; it is inventory.

**The six station cards.** Print one each. **Each card says what to show and one number to say. Nothing else on the card.**

| # | Station | What you show | The one number you say out loud |
|---|---|---|---|
| 1 | **W20 — the machine that does the slopes** | The tensor with `requires_grad=True` and the `.grad` it produced | *"`w.grad` matched the slope I worked out by hand in Week 18."* |
| 2 | **W21 — the five-line loop** | `zero_grad`, forward, loss, `backward`, `step` — pointed at, in order | *"Five lines, and I have not changed them since."* |
| 3 | **W22 — layers, and watching it overfit** | The two loss curves, train falling and validation turning up | *"`2 → 16 → 1` is 65 parameters and I counted them by hand."* |
| 4 | **W23 — the same brain, real framework** | The `nn.Module` class, and the digits accuracy | *"1,257 digits, 32 at a time, is 40 steps per epoch."* |
| 5 | **W24 / W25 — the picture, and the shapes** | The 8×8 you convolved by hand, and THE SHAPE LADDER | *"`16 × 2 × 2 = 64`, and that is the number in my `Linear` layer."* |
| 6 | **W26 — a network that reads digits** | `filters.png`, and the accuracy | *"529 of 540 held-out digits, with 1,898 weights, in about three seconds."* |

**Run it with a timer, out loud.** Two minutes, move. **Do not let station 6 run long** — it is the exciting one and it will eat station 1's time if you let it.

**What "finished" looks like:** six stations visited, six numbers said out loud, the showcase sheet with one line written per station. **A student who says "I don't remember what Week 20 was" gets one prompt — *"what did `.backward()` do?"* — and then moves on.** The station is not a test.

### Part B — The Honest Transfer Learning Experiment (8 minutes)

**What it is.** Three training runs, three numbers, on the board side by side — **including the control.** The whole activity is eight minutes because two of the three runs take under two seconds.

### Setup

- The FROZEN / UNFROZEN wall sheet: two columns, three rows (`movable weights`, `seconds`, `test accuracy`). **Add a third column headed FROM SCRATCH before you start** — and let somebody notice you adding it.
- Workbook Practice Set A, item A2, is the paper version of this grid (it has four rows, including conv1 only).
- `see_it.py` with sections 1 and 2 already run.

### Step 1 — stage one, and a prediction (2 minutes)

They run stage 1: the whole network on digits 0–4 only.

```python
torch.manual_seed(0)
first = make_cnn()
s = train(first, Xtr[lo_tr], ytr[lo_tr])
print("digits 0-4: train %d  test %d" % (lo_tr.sum(), lo_te.sum()))
print("stage 1, digits 0-4 only: %5.1fs  test %.4f"
      % (s, acc(first, Xte[lo_te], yte[lo_te])))
```

```text
digits 0-4: train 630  test 271
stage 1, digits 0-4 only:   1.4s  test 0.9926
```

> **Ask this:** "0.9926 on five classes, against 0.9796 on ten last week. **Is this network better than last week's?**"

*Hoped-for answer:* no — five classes is an easier problem.

> "**Five classes is easier than ten.** A model guessing at random gets 20% here and 10% there. **You cannot compare those two numbers**, and that is the whole reason today's results table has the pile written on every row."

### Step 2 — freeze it, and count (2 minutes)

```python
torch.manual_seed(0)
frozen = make_cnn()
frozen.load_state_dict(backbone)
frozen[7] = nn.Linear(64, 10)
for layer in (frozen[0], frozen[3]):
    for p in layer.parameters():
        p.requires_grad = False
print("movable weights:", sum(p.numel() for p in frozen.parameters()
                              if p.requires_grad))
s = train(frozen, Xtr[hi_tr], ytr[hi_tr])
report("frozen-transfer", s, frozen, Xtr[hi_tr], ytr[hi_tr],
       Xte[hi_te], yte[hi_te])
```

```text
movable weights: 650
frozen-transfer      0.3s  movable  650  train 0.9330  test 0.9257  (249 of 269)
```

**Do this:** Fill in the FROZEN column on the wall: `650`, `0.3`, `0.9257`.

**Ask this:** "**Where did the other 1,248 weights go?**"

*Frozen — the two conv layers, 80 + 1,168.*

> "80 plus 1,168 is 1,248, and 1,248 plus 650 is 1,898. **The addition works and you should make it.**"

### Step 3 — unfreeze it (2 minutes)

```python
torch.manual_seed(0)
fine = make_cnn()
fine.load_state_dict(backbone)
fine[7] = nn.Linear(64, 10)
s = train(fine, Xtr[hi_tr], ytr[hi_tr])
report("fine-tuned", s, fine, Xtr[hi_tr], ytr[hi_tr], Xte[hi_te], yte[hi_te])
```

```text
fine-tuned           1.6s  movable 1898  train 0.9841  test 0.9665  (260 of 269)
```

**Do this:** Fill in the UNFROZEN column: `1,898`, `1.6`, `0.9665`.

**Ask this:** "Frozen 0.9257, unfrozen 0.9665. Which is better, and by how many digits?"

*Unfrozen, by 11 digits — 260 against 249 out of 269.*

> "**Eleven digits out of 269, which is four accuracy points.** Frozen came out lowest in all five seeds we re-ran, so this is unlikely to be noise. Letting the conv layers adjust to the new digits probably helped, and it makes sense: 5, 6, 7, 8 and 9 are different shapes from 0, 1, 2, 3 and 4, so the filters needed to move."

### Step 4 — the control, and the point (2 minutes)

> **"Right. One more, and this is the one that makes it an experiment."**

```python
torch.manual_seed(0)
scratch = make_cnn()
s = train(scratch, Xtr[hi_tr], ytr[hi_tr])
report("scratch on 5-9", s, scratch, Xtr[hi_tr], ytr[hi_tr],
       Xte[hi_te], yte[hi_te])
```

```text
scratch on 5-9       1.5s  movable 1898  train 0.9729  test 0.9814  (264 of 269)
```

**Do this:** Fill in the FROM SCRATCH column: `1,898`, `1.5`, `0.9814`. **Then stand back and say nothing for five seconds.**

**Ask this:** "Which column won?"

*From scratch.*

**Ask this:** "So what did borrowing the backbone buy us?"

*Take answers. Steer to: fewer weights, less time, and it cost accuracy.*

> **"It bought a third of the weights and a fifth of the training time, and it cost 5.6 accuracy points. That is the result and it is a real one.**
>
> And now the important question, and I want you to answer it before I do."

**Ask this:** "**Why didn't it work?** Think about what we borrowed *from*."

*Hoped-for answer:* it only knew 630 pictures of five digits, which is no more than we already had.

> "**That is exactly it.** Transfer learning works when the thing you borrow from knows far more than you do. Ours knew 630 pictures. We had 627. **A likely suspect is that we borrowed from an equal** (we did not vary the source size, so hold it as a hypothesis; the 0-4 versus 5-9 mismatch and the fresh head's learning rate are also candidates)."

### What "finished" looks like

- The FROZEN / UNFROZEN / FROM SCRATCH sheet with all nine numbers on it.
- Practice Set A, item A2, filled in to match (the seconds will differ from the wall sheet; that is fine).
- `80 + 1,168 + 650 = 1,898` written somewhere, and the 650 checked against the print.
- The student can say, unprompted: *"you need the control."*
- **Nobody in the room believes transfer learning is magic, and nobody believes it is useless.**

### Variation — easier

**Cut the fine-tuning run.** Frozen against from-scratch is enough for objective 2: **0.9257 with 650 movable weights against 0.9814 with 1,898.** Two numbers, one comparison, and the honest conclusion is unchanged.

**And give them the whole transfer block complete**, so the only thing they do is read the three numbers off the screen and put them on the wall. **Objective 2 is about reading and reporting two numbers, not about typing `load_state_dict`.**

**One scaffold that works very well:** pre-draw the three-column sheet with the *row labels* filled in and one worked example in the first cell, so the shape of the comparison is visible before any number exists.

### Variation — harder

1. **Make the target task genuinely small, and watch transfer win.** Take only **100** of the 627 rows of digits 5–9 and rerun all three. The code and the real numbers are in the Answer Key under the stretch (not in the workbook). **Frozen 0.8848, fine-tuned 0.9257, from scratch 0.9628** — so scratch still wins even at 100 rows, which is itself a finding, and the honest conclusion is that on 8×8 digits a 1,898-weight network barely needs help. **A student who runs it and reports "it still didn't win, and here is how few rows I got down to" has done a better experiment than the lesson did.**
2. **Freeze only the first conv layer** instead of both. `frozen[0]` only, so 1,168 + 650 = 1,818 movable. **Predict where the accuracy lands before running: between 0.9257 and 0.9665.** Then check.
3. **Augment with two-pixel shifts as well**, nine copies instead of five: 1,257 × 9 = 11,313 rows. Predict whether it helps before running. **On an 8×8 digit a two-pixel shift is a quarter of the picture, and it usually hurts.** Finding the point where augmentation turns from help to harm is the real skill.
4. **Attack the 1/8 pair directly.** Add extra shifted copies of the 1s and 8s only, leaving the other classes alone, and see whether those four mistakes go away. **Then the honest check: did the other digits get worse?** This is the whole class-imbalance conversation in one experiment.
5. **Find the mistake and look at it.** Get the indices of the eleven wrong test digits, print one as an 8×8 grid of numbers, and decide whether *you* can read it. **Often you cannot**, and that is the most useful five minutes available today: some of the remaining 2% is not the model being stupid, it is the picture not containing the answer.
6. **Do the confusion-pair analysis for the augmented model too.** It got 536 of 540, so only 4 mistakes. **Is the 1/8 pair still the worst?** Then the honest question: *"with 4 mistakes, can you name a worst pair at all?"* **No — four mistakes is not enough to rank anything, and knowing when you have run out of data to analyse is a level-5 skill.**

---

## ❓ Questions Students Ask This Week

This section gives you answers ready for the questions this week's lesson tends to raise.

**"Why can't we augment the test set too? More test data would give a better estimate."**

**Two reasons, and both are hard rules.**

**One: evaluation has to be repeatable.** If your test set contains randomly-shifted pictures, running your evaluation twice gives two different numbers, and then you cannot tell whether a change to your model helped or whether the test set just moved. **A number that changes when nothing changed is not a measurement.**

**Two: augmentation makes pictures harder.** A shifted, partly-blanked digit is more difficult than the original. So an augmented test set would report a *worse* accuracy than your model actually achieves on real digits, and you would be reporting a number that answers no question anybody asked.

**And the general principle, which is Week 6's and has not changed:** anything involving randomness, or fitting, or choosing, belongs to the training path only. **The test set is opened once, unmodified, at the end.**

**"Why is `np.roll`'s wrapping the default? It seems like the wrong thing to want."**

Because `np.roll` is not an image function. **It is a general array function**, and for the things it was designed for — rotating a queue, cycling through a buffer, shifting a signal — wrapping is exactly right.

**It is our job to know that we are using a general tool for a specific purpose**, and that the general tool's sensible default is wrong for our case. That is a very common shape of bug and it is worth naming: **the function is not broken, it is doing what it says, and we asked the wrong question.** The three lines that blank the edge are us finishing the job, not fixing numpy.

**"So does transfer learning actually work or not?"**

**It works, it is one of the highest-value techniques there is, and it did not work here — and all three of those are true at once.**

The condition is what matters: **the network you borrow from has to know far more than you do.** The real version borrows from something trained on 1.2 million photographs, and applies it to a few thousand pictures. On problems like that, a frozen backbone plus a small new head routinely beats weeks of training from scratch, on far less data.

**We borrowed from a network trained on 630 pictures of five digits and used it for 627 pictures of five other digits.** The source was not bigger. It was the same size and it was *specialised* to the wrong five shapes.

**What we did prove, and it is worth having:** the machinery works. We froze a backbone, counted the movable weights down from 1,898 to 650, trained in a fifth of the time, and landed within six points. **On a real problem where the backbone came from a million photos and you have fifty pictures, that same machinery is the difference between a model and no model.**

**"Why does the network need to see shifted digits at all? Isn't a conv layer supposed to be shift-tolerant already?"**

**Excellent question, and the honest answer is "partly, and not as much as the sales pitch suggests".**

A conv layer *does* apply the same filter everywhere, so a vertical edge one pixel to the left still produces a response — just one pixel to the left in the feature map. That much is genuinely shift-tolerant.

**But the head is not.** Our `Linear(64, 10)` reads 64 specific numbers in a specific order, and it very much cares which of the 64 a signal arrives in. **Max pooling helps** — after two 2×2 pools, a one-pixel shift in the picture is often a zero-pixel shift in the final 2×2 map — but "often" is not "always", and at 8×8 there is not much map left to be tolerant with.

**So the claim you should carry is the honest one: convolution buys you *some* shift tolerance, cheaply, and augmentation buys you more. Our seed-0 measurement says the extra was worth 1.30 accuracy points, or seven digits out of 540; other seeds gave 1.3 to 1.7 in three cases and -0.2 in one.** That is a specific number for a specific claim, which is the whole point.

**"Eleven wrong, four of them 1-versus-8. Couldn't we just train longer on 1s and 8s?"**

You could, and it would probably move those four. **And then you should check what it broke**, which is Variation-harder 4 and it is worth doing.

But be clear about what you would be doing: **attacking the symptom.** The cause is that at 8×8 an 8's loops are three pixels tall and cannot hold a hole, so they fill in and leave a bar. **No amount of extra training makes 64 pixels contain information they do not contain.** The fixes that address the cause are: more pixels, or a different feature entirely — count the enclosed regions, say, which is what a 1980s hand-designed system would have done and which would nail this pair instantly.

**And that is worth sitting with for a second.** A hand-designed hole-counter would beat our CNN on this one pair. The CNN wins overall, on everything else, and it needed nobody to think of hole-counting. **Both of those are true and neither cancels the other.**

**"Why did the wrapped augmentation get a *worse* training accuracy than plain? It had five times the data."**

**Because data that contradicts itself is hard to fit.** Four fifths of those 6,285 rows (every shifted copy) have a row or column of ink teleported to the opposite edge, labelled with the original digit; the down-shifted copy, for instance, shows the digit's bottom row at the top. Some of those wrapped pictures genuinely look more like a different digit than the one on the label.

So the model is being told two incompatible things about similar-looking pictures, and the best it can do is compromise — which shows up as `train 0.9774` instead of `0.9881`. **A training accuracy that drops when you add data is a strong signal that the added data is wrong**, and it is a check worth keeping.

**"Which single thing should I do first if I want a better model?"** *(Nobody fully agrees, and here is why.)*

**There is no settled answer, and the honest version of the disagreement is genuinely useful.**

**Camp one says: get more data, always, first.** Everything else is a way of pretending you have more data. Augmentation is a cheap imitation of it; transfer learning is borrowing somebody else's. Our +1.30 points from augmentation (seed 0) is probably real and it is smaller than what 5,000 more real digits would buy.

**Camp two says: fix the measurement before you touch the model.** We spent this whole lesson chasing eleven mistakes out of 540, and four of those eleven come from a pair that is arguably ambiguous at this resolution. **If some of your test labels are debatable, you are optimising against noise**, and the first job is to find out how many. Somebody should sit down with the eleven and decide whether a human can read them.

**Camp three says: it depends entirely on where you are on the curve**, and the only way to know is to plot accuracy against training-set size. If the curve is still climbing steeply, get data. If it has flattened, data will not help and you need a better model or better features.

**And there is a fourth position which is the most uncomfortable and probably the most honest: none of these is the first question.** The first question is *what is this for, and what does a mistake cost?* Eleven misread digits out of 540 is a triumph for a hobby project and a catastrophe for a medical form. **Nobody can tell you which of augmentation, transfer, more data or better labels to do first without knowing that** — and the reason the argument never settles is that people keep answering it in general when it is only answerable in particular.

What to tell a 14-year-old, out loud: **"there is no first thing. But there is always a control, and there is always a split named on every row, and if you have those two, nobody can sell you a fake improvement."**

---

## ⚠️ Where This Lesson Goes Wrong

This section names the ways the lesson can go off course and what to do about each.

| What happens | Why | What to do right now |
|---|---|---|
| **The two honest negatives get softened into successes** | Nobody enjoys teaching a lesson where the technique loses | **Do not.** Both results are the lesson, and both are stated in the Watch-out box so you cannot be surprised by them. Say the number, then say why. *"Transfer learning bought a fifth of the time and cost 5.6 points, probably because we borrowed from an equal, which we have not tested."* |
| The from-scratch control is skipped for time | It is the fourth run and it looks like a repeat of something | **It is the entire reason this is an experiment.** Skip the fine-tuning run instead if you must. **A frozen number with nothing to compare it to is a number, not a result**, and saying so is objective 2. |
| The wrap version is described but not run | It takes 15 seconds and the lesson is behind | **Run it.** Two identical `529 of 540`s on the same screen is worth more than any explanation, and the drop in *training* accuracy is the part that teaches. |
| The axis bug gets skipped | It is another 16 seconds | If you genuinely have no time, **write the two numbers on the board — `train 0.5968`, `test 0.8574` — and ask what is impossible about them.** The alarm survives without the run. |
| Rows 2 and 4 of the results table get compared | 0.9926 and 0.9665 are right next to each other and both are accuracies | **Write the pile in every row on the board yourself, first.** Then ask the illegal comparison out loud and let them catch it. **A table where the mistake is impossible is better than a warning about the mistake.** |
| The confusion pair gets named but not diagnosed | "1 and 8, four of eleven" feels like an answer | Say the two versions out loud, side by side — the number restated, and the ink-per-column explanation. **Then the test: "what would you actually do about it?"** Only the second version leads anywhere. |
| The showcase circuit becomes a queue | The station cards have too much on them | **Each card: what to show, one number to say.** Nothing else. Trim them in front of the class if you have to; a card nobody can read in five seconds is a card that stalls the circuit. |
| `.copy()` is left out of the shift function | It looks redundant | `np.roll` itself hands back a fresh array on this numpy (so the file as written is safe even without it), but slices and `.T` are views, and blanking a view blanks the original training data. **If shift is ever rewritten that way, the symptom is that the plain run's numbers change if you rerun it** — which is genuinely baffling. Say the word `.copy()` out loud when you type it. |
| Somebody concludes the CNN is bad because it is only 98% | Eleven mistakes feels like a lot when you count them | **Look at one.** Print a wrong test digit as an 8×8 grid of numbers and try to read it yourself. **Often you cannot**, and that reframes the whole conversation from "the model is stupid" to "the picture is 64 pixels". |
| The lesson runs out of time in the wrap | There are three experiments and a circuit in seventy minutes | **The wrap is the least cuttable part of this particular week**, because the four-row table with the piles named is objective 4. If you are behind at minute 60, cut the showcase circuit to four stations. **Never cut the table.** |
| The wall sheets come down without ceremony | It is the end of a long term and everyone is tired | **Take thirty seconds and do it properly.** Read the first row of PARAMETER COUNT (`2 → 16 → 1 = 65`, from Week 22) and the last (`1,898`). **That is the arc of the term in two numbers and the class deserves to hear it.** |

---

## 🧭 Differentiation

This section adjusts the lesson for a student who is struggling and for one who is ready for more.

### If the student is struggling

**Cut:** the wrap-versus-blank comparison down to *one* run. Use the blanked version only, and **tell them about the wrap** rather than measuring it: *"if you don't blank the edge, this buys nothing — I measured it."* Objective 1 becomes "+1.30 points" instead of "+0.00 and +1.30", which is enough.

**Cut:** the fine-tuning run. Frozen against from-scratch carries objective 2.

**Cut:** the showcase circuit to four stations: Week 21's five-line loop, Week 23's digits, Week 25's shape ladder, Week 26's filters.

**Give them `see_it.py` complete.** Every bit of the learning today is in reading numbers off a screen and putting them in a table with the split named. **None of it is in typing `load_state_dict`.**

**The version that skips everything hard.** No code and no new ideas — one table with the numbers already in it, and three questions:

| row | held-out pile | test accuracy |
|---|---|---:|
| plain | 540 all-digit rows | 0.9796 |
| augmented | 540 all-digit rows | 0.9926 |
| frozen-transfer | 269 rows of 5–9 | 0.9257 |
| from scratch on 5–9 | 269 rows of 5–9 | 0.9814 |

> **"Which two rows can you fairly compare? Which two rows can you also fairly compare? And which pair must you never compare?"**

Rows 1 and 2. Rows 3 and 4. **Rows 2 and 3, or 2 and 4 — different piles.** **That is objective 4, complete, with no computer and no code**, and it is the objective that matters most for the capstone in Weeks 34 to 36.

**The copy-this-exactly scaffold.** Ten lines, and it runs on its own:

```python
import numpy as np

img = np.zeros((8, 8))
img[7, 2:6] = 1.0                      # a bar on the very bottom row
print("original, bottom two rows:")
print(img[6:8])
print("rolled down 1, top two rows:")
print(np.roll(img, 1, axis=0)[0:2])
print("rolled down 1, bottom two rows:")
print(np.roll(img, 1, axis=0)[6:8])
```

```text
original, bottom two rows:
[[0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 1. 1. 1. 1. 0. 0.]]
rolled down 1, top two rows:
[[0. 0. 1. 1. 1. 1. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0.]]
rolled down 1, bottom two rows:
[[0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0.]]
```

Then two questions and nothing else: **"where did the bar go? and is that where you wanted it?"** **It went from the bottom row to the very top row**, and no, that is not "one pixel down" — **that is the whole way round the picture.** Let them run it and see it themselves. **That is the wrap, in ten lines.**

**One thing you must not cut:** the four-row table with the pile named on every row. If the whole lesson collapses to one sentence, make it *"two accuracies measured on different piles are not comparable, however close together you print them."*

### If the student is flying

None of these need syntax from a later week.

1. **The 100-row target task** (Variation-harder 1). The real numbers are in the Answer Key. **And the honest finding is that scratch still wins**, which is a better result than a win would have been, because it means they have to say *why* — and the answer is that a 1,898-weight network on 8×8 pictures barely needs help.
2. **Freeze one conv layer instead of two** (Variation-harder 2). Predict where it lands, then check. **1,818 movable weights.**
3. **Two-pixel shifts, nine copies** (Variation-harder 3). Predict whether it helps. **It usually hurts, because two pixels out of eight is a quarter of the picture.**
4. **Attack the 1/8 pair directly** (Variation-harder 4), then check what it broke. **This is the class-imbalance conversation in one experiment and it is the best available today.**
5. **Print a wrong digit and try to read it** (Variation-harder 5). Then the honest question: *"how many of the eleven do you think a human would get right?"* **Nobody knows, and finding out is a real afternoon's work that somebody at a real company should have done.**
6. **The augmented model's confusion matrix** (Variation-harder 6). Four mistakes. Then: *"can you name a worst pair from four mistakes?"* **No.** Knowing when you have run out of data to analyse is genuinely rare and worth saying loudly.

### If the student won't engage today

**Close the laptop. Squared paper and one drawn digit.**

Draw an 8×8 grid. Shade in a rough 6. Then three instructions:

> **"Copy it into the grid next to it, but slide everything down one square."**
>
> **"The bottom row fell off. Where should it go?"**
>
> **"Where does `np.roll` actually put it?"**

Nowhere, and **round the top.** Then: **"is that still a 6?"** No. **That is objective 1's whole understanding, delivered with a pencil in four minutes.**

If they will take one more, go to the confusion matrix on paper and ask only about the pair:

> **"Row 8, column 1 says three. What does that mean happened three times?"**
>
> **"Now find the mirror cell. Row 1, column 8."**
>
> **"So what pair of digits is this model confusing?"**

Three real 8s called 1; one real 1 called 8; **the pair is 1 and 8.** Then the good question, which is not a maths question at all: **"draw an 8 in an 8×8 grid. Can you fit two holes in it?"** They cannot, and **that is the physical diagnosis, discovered rather than told.** It is the best moment in the lesson and it needs no electricity.

The rest survives. Term 4 starts fresh next week with a completely different subject.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — what augmentation actually needs (spoken, 60 seconds)**

> "You made five copies of every training digit by shifting them one pixel. **It bought you zero accuracy points, and then a three-line change made it buy 1.30. What was the three-line change, and why did it matter?**"

*Good answer:* "Blanking the edge the ink rolled off. `np.roll` wraps, so the bottom row of the digit came back round at the top, and at 8×8 that makes a picture that isn't the digit on its label any more. About a fifth of the extra rows had wrong labels, so they cancelled out the benefit — you could see it in the training accuracy, which was *worse* than plain."

**What to catch:** "because it was cleaner". Push once: *"what was actually wrong with those pictures?"* **Full marks needs the words "the label was no longer true".**

**Check 2 — the control (spoken, 60 seconds)**

> "You froze the backbone and got **0.9257** on the digits 5-to-9 test rows. **Is that good?**"

*Good answer:* "You can't tell without a control. Training from scratch on the same 627 rows got 0.9814, so 0.9257 is actually 5.6 points worse — the borrowing cost accuracy. What it bought was 650 movable weights instead of 1,898 and 0.3 seconds instead of 1.5."

**What to catch:** any answer that evaluates 0.9257 on its own — "yes, 93% is good" or "no, it's low". **The only correct first move is "compared to what?"** and a student who says that has learned the most transferable thing in the term.

**Check 3 — the illegal comparison (spoken, 90 seconds)**

> "Your table says augmented **0.9926** and fine-tuned **0.9665**. **Can you say augmentation was better than fine-tuning by 2.6 points? Why or why not?**"

*Good answer:* "No. The augmented number is on 540 held-out digits across all ten classes; the fine-tuned number is on 269 held-out digits of just 5 to 9. Different piles, and five classes is an easier problem than ten. The fair comparisons are 0.9926 against 0.9796 — same 540 rows — and 0.9665 against 0.9257 — same 269 rows."

**What to catch:** "yes, 0.9926 is bigger". Push once: *"how many digits was each of those measured on?"* **A student who names the two piles before comparing anything is at level 4, and this is the check that predicts whether the Week 34–36 capstone report will be honest.**

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot say what `np.roll` did to the picture. Reads 0.9257 as "good" with nothing to compare it to. Compares two accuracies measured on different test sets without noticing. |
| **2 — Emerging** | Runs the augmentation with help and reports the +1.30. Can point at the confusion pair when shown where to look. Names the frozen and unfrozen numbers but not the control. |
| **3 — Secure** | Explains that augmentation only works while the label stays true, with the wrap as the counter-example. Reports frozen, fine-tuned **and** from-scratch, and says the borrowing cost accuracy. Names the 1/8 pair and gives a physical reason involving the resolution. Produces the four-row table **with the pile on every row.** **This is the target.** |
| **4 — Strong** | Spots that the wrapped model's *training* accuracy fell and uses that as evidence the extra data was wrong. Asks for the control before being told to. Says out loud that rows 2 and 4 may not be compared, and why. Notices the 1/8 confusion is asymmetric and explains the direction — an 8 can lose its holes, a 1 cannot grow them. |
| **5 — Exceptional** | Predicts the test-above-train alarm from the axis bug before running it, and explains it. States the condition transfer learning needs — the source must know far more than the target — and shows the arithmetic that it failed here (630 against 627). Notes that with only four mistakes the augmented model has no rankable worst pair. Proposes the experiment that would settle whether four digits out of 540 is a real difference, and says honestly that the first question is what a mistake costs. |

---

## 📤 Homework to Assign

This section is what to say when you set the homework.

**What the workbook holds.** `workbook/week-27.md` has, in order: ✅ Warm-Up (W1–W5) · 🔢 Do the Maths by Hand (M1–M4) · 🔎 Predict the Output (P1–P4) · ✍️ Practice Set A (A1–A6) · ✍️ Practice Set B (B1–B5) · 🐞 Fix the Broken Program · 🧩 Puzzle of the Week · 🤔 Think Deeper (T1–T2) · 🛠️ Build It · 🎨 Draw It · 📊 Self-Check, with its own ✅ Answers at the very end. **It has no numbered pages.** The showcase circuit sheet and the three-column grid are not workbook pages: the circuit sheet is a plain sheet with six lines, and the grid is Practice Set A, item A2.

**The core, and the part you mark hardest, is 🛠️ Build It.** It is three things: the See It results table, the diagnosis of the worst confusion pair, and the Term 3 reflection.

**Say this:**

> "About an hour, and the middle part is the one I mark hardest. It is all in the Build It section of the workbook.
>
> **First, the See It results table — four rows.** Plain, augmented, frozen-transfer, fine-tuned. Columns: the held-out pile, the weights trained, the seconds, the test accuracy, and the test correct. **And I want the held-out pile written on every single row** — not in a footnote, not once at the top. On every row. Then the two sentences underneath: **which two comparisons in your table are fair, and which one you must not make.** And there is a fifth row the table does not ask for. **Find it and give me its number.**
>
> **Second, 'Diagnose the worst confusion pair' — and this is the part I care about.** Find the pair. Say the counts, both directions. **And then explain *physically* why those two digits look alike at eight pixels by eight pixels.** Not 'because they're similar'. Not 'because 4 out of 11'. **What do the two digits actually share when you only have 64 pixels?** Use the ink-per-column numbers if they help. **A diagnosis that restates the count in different words scores nothing**, and I will hand it back once. Then name one fix that addresses the cause and one that only addresses the symptom.
>
> **Third, the Term 3 reflection.** Six lines, one per week from Week 20 to Week 26, and each line has the same shape: **what I can do now that I could not do in Week 19, and one number that proves it.** One number per line. Not 'I learned about convolution'. *'I can work out a conv layer's output size on paper: 8 becomes 8 with padding 1, and 4 without.'*
>
> Before you start that, do **Do the Maths by Hand, M3 and M4** — they are the confusion-matrix addition and the fair-comparison rules, and the Build It answers come straight out of them. The rest of the workbook — Warm-Up, Predict the Output, both practice sets, Fix the Broken Program, the Puzzle, Think Deeper and Draw It — is for the week, in whatever order you like, and Self-Check goes last. Fix the Broken Program has three bugs and the last one makes no error message at all.
>
> The stretch is not in the workbook: it makes the target task tiny and asks whether transfer learning wins when there is almost no data. **The answer surprised me and I want to know if it surprises you.**"

**Where it is done.** *In class:* the three predictions (Build It, checklist step 1) during the Concept block, the showcase circuit lines on a plain sheet during Part A, and Practice Set A item A2 as the paper copy of the three-column grid during Part B. *At home, required:* Build It (the table and its sentences, the diagnosis, the reflection) with M3 and M4 first. *At home, as time allows:* everything else in the workbook, Self-Check last. The stretch is optional.

**Expected time:** M3 and M4 about 15 min · the table and the fair-comparison sentences 20 min · the confusion-pair diagnosis 25 min · the reflection 15 min · **about 75 minutes for the required part** (the old plan counted the same three jobs at about an hour; M3 and M4 are the addition), plus roughly 20 minutes each for the stretch and for the remaining workbook sections you choose to set.

> **🧑‍🏫 What to look for when you mark it:** three things, and the second is the real one. **One — is the held-out pile on every row of the table?** A table with `540` on rows 1 and 2 and `269` on rows 3 and 4 is a table that cannot mislead anybody, including its author in six months. A table with the piles missing is the single most common way a real report tells a lie without anybody meaning to. **Two — is the diagnosis physical?** The bar is: *did they say something about what 64 pixels can and cannot show?* "An 8's loops are about three pixels across, which is too small to hold a hole, so they fill in and leave a bright bar down the middle — and a 1 is a bright bar down the middle" is a diagnosis. "The model confused 1 and 8 four times" is a location. **Mark the difference explicitly, and praise loudly anybody who notices the asymmetry** — three 8s called 1 but only one 1 called 8, because information only travels one way. **Three — does every line of the reflection have a number in it?** Six lines, six numbers. A reflection without numbers is a feeling, and this course has spent twenty-seven weeks on the difference.

---

## 🔑 Answer Key

Keyed to `workbook/week-27.md`, section by section and item by item, so you can mark from this page alone. The values are the ones in the workbook's own Answers section. **Seconds are machine-dependent and are never marked:** the workbook's run shows plain 2.4, augmented 11.3, frozen 0.2, conv1-only 0.6, fine-tuned 1.1 and scratch 1.1, while the live wall sheet in the lesson shows 0.3, 1.6 and 1.5. Accept the student's own. **Accuracies and counts are seeded and should match to four places.**

### ✅ Warm-Up (W1–W5)

- **W1.** `8 × 3 × 3 × 16 = 1,152`, plus **16** biases (one per filter), so **1,168**. ❌ 1,152 is the missing-biases error.
- **W2.** **Ten logits** — raw, unsquashed scores, one per digit. **Definitely not probabilities:** one of ours is `−10.94`, and they do not add up to 1.
- **W3.** **About 2.30**, because a model that has learned nothing spreads its confidence evenly over ten options, each with a chance of 0.1, and `−ln(0.1) = 2.3026`. Ours printed `2.2796`.
- **W4.** **Ten answers**, and no, you wanted 540 — one per picture. **It did not error.** `dim=0` runs down each column, across all 540 pictures for one digit, and answers a question nobody asked. *Count the answers.*
- **W5.** Because `0.9796` looks precise to four decimal places and it is not. **One more correct answer takes it to 0.9815**, so the fourth decimal place is noise. `529 of 540` invites the right question: *"how much would one more move it?"*

**Marking notes.** W4 is the one to look at. A student who writes "540" for *answers* has not run it; the point is that it printed ten and nothing complained.

### 🔢 Do the Maths by Hand (M1–M4)

**M1.** `0.9926 − 0.9796 = 0.0130`, which is **1.30 accuracy points**. In digits: `0.9796 × 540 = 529.0`, `0.9926 × 540 = 536.0`, so augmentation read **7** more digits correctly. **The wrapped version read 0 more** — exactly `0.9796`, the same 529 of 540.

Full-marks sentence: *"Blanking the rolled-off edge turned five times the training data from worth nothing into worth 7 more digits out of 540, which is +1.30 accuracy points in our seed-0 run (other seeds varied, and part of the gain may be the extra training steps)."*

**M2.**

| What is frozen | frozen count | the subtraction | movable |
|---|---:|---|---:|
| nothing | 0 | 1898 − 0 | **1898** |
| conv1 only | **80** | 1898 − 80 | **1818** |
| conv1 and conv2 | **1248** | 1898 − 1248 | **650** |
| everything | **1898** | 1898 − 1898 | **0** |

The row that makes Adam refuse is the last: `ValueError: optimizer got an empty parameter list`. Freezing nothing when you meant to freeze gives no error at all, which is why the check matters: **`frozen + movable` must equal 1,898.** The 650 must be there; a student who wrote 1,898 for conv1-and-conv2 has not frozen anything in their head.

**M3.** Diagonal: `54 + 53 + 52 + 53 + 53 + 55 + 53 + 54 + 48 + 54 = ` **529**. The nine off-diagonal cells (row, column = count): 1,5 = 1 · 1,8 = 1 · 2,1 = 1 · 3,5 = 1 · 3,7 = 1 · 4,9 = 1 · 6,1 = 1 · 8,1 = **3** · 8,7 = 1; **total 11**. **`529 + 11 = 540`** ✅.

Worst pair: row 8 column 1 holds **3**, row 1 column 8 holds **1**, together **4**. **No other pair comes close:** every other off-diagonal cell is a 1 and none faces another across the diagonal, so every other pair totals 1. *Second place:* there is no second place, just a seven-way tie at 1 (1 & 5, 2 & 1, 3 & 5, 3 & 7, 4 & 9, 6 & 1, 8 & 7). Any one of them is a correct answer to "which pair comes second"; the tie is the point.

**M4.** Rows 1 and 2: `0.9926 − 0.9796 = +0.0130`, **FAIR** (same 540 rows, same ten classes, one thing changed). Rows 3 and 4: `0.9665 − 0.9257 = +0.0408`, **FAIR** (same 269 rows, five classes). Rows 2 and 4: **NOT ALLOWED**, two different exams. Rows 1 and 3: **NOT ALLOWED**, same reason.

Why 269 rows of five classes is easier: fewer wrong answers available. Random guessing scores 20% on five classes and 10% on ten, and the 1/8 pair that caused a third of the ten-class errors cannot happen in 5–9 because there is no 1. **Fewer ways to be wrong means a higher score for the same skill.**

**Marking notes.** For M3 the check that matters is the addition to 540. For M4, "NOT ALLOWED" with no reason is half marks.

### 🔎 Predict the Output (P1–P4)

**P1.**

```text
[5 1 2 3 4]
[2 3 4 5 1]
[4 5 1 2 3]
[1 2 3 4 5]
```

Line 4 gives the original back: shifting a list of 5 by 5 sends every number all the way round. **Nothing was thrown away** — what falls off one end comes back on the other. That is exactly what ruins an augmented digit, and is what you want for rotating a queue or cycling a buffer.

**P2.**

```text
ink per picture: [0. 9. 9. 9.]
ink per picture: [9. 9. 9. 9.]
```

`out[0, :, :]` blanks **picture 0 entirely**; `out[:, 0, :]` blanks **row 0 of every picture**, which is what you want after rolling down (all four kept their ink, since the bright pixel moved from row 1 to row 2). Neither errored; **the ink per picture** told you: a zero means a whole picture was wiped while its label stayed.

**P3.**

```text
(6285, 1, 8, 8)
(6285,)
(1257, 2, 8, 8)
```

Line 3 glued along `dim=1`, the channel dimension: "one picture with two channels", so 1,257 two-channel pictures instead of 2,514 one-channel ones; the batch count did not change, which is the giveaway. **Line 1 (with line 2 for the labels) is the one for augmenting.** The out-loud check: *"as many labels as pictures — 6,285 and 6,285, and `1257 × 5 = 6285`."*

**P4.**

```text
1898
730
4
```

`m[3]` is the **second conv layer**, `nn.Conv2d(8, 16, 3, padding=1)`; freezing it locked **1,168** numbers, `1898 − 1168 = 730`. Line 3 counts blocks: the four still movable are conv1's `weight` and `bias` and the linear's `weight` and `bias`. ❌ A student who predicted `650` for line 2 froze both convs in their head: `m[0]` is conv1, `m[3]` is conv2.

The "how many did you get right" line at the end of the section is a self-rating; do not mark it.

### ✍️ Practice Set A (A1–A6)

**A1.** data augmentation (iii) · transfer learning (v) · freezing (vi) · backbone (ii) · fine-tuning (i) · confusion pair (iv)

**A2.** *(This is the paper copy of the three-column grid used in Part B.)*

| What you froze | movable weights | seconds | test accuracy |
|---|---:|---:|---:|
| both convs | **650** | **0.2** | **0.9257** |
| conv1 only | **1818** | **0.6** | **0.9517** |
| nothing (fine-tuned) | **1898** | **1.1** | **0.9665** |
| from scratch, no borrowing | **1898** | **1.1** | **0.9814** |

**From scratch won on accuracy** (0.9814, which is 264 of 269). **Freezing both convs won on speed** (0.2 seconds). Trade in one sentence: *"Freezing both convs trained 650 weights instead of 1,898 in 0.2 seconds instead of 1.1, and it cost 5.6 accuracy points against the from-scratch control."* Test counts: 249, 256, 260 and 264 of 269. The live three-column sheet in Part B has three of these four rows with its own seconds (0.3, 1.6, 1.5).

**A3.** The impossible thing: **test accuracy (0.8574) is higher than training accuracy (0.5968)**. `axis=0` and `axis=1` should be `axis=1` and `axis=2`. On `(1257, 8, 8)`, `axis=0` is *which picture*, so rolling it shuffles the pictures while the labels stay put. Of the five shifts, `(-1, 0)` and `(1, 0)` roll the stack and are pictures paired with somebody else's label; `(0, 0)` shifts nothing and `(0, -1)`, `(0, 1)` roll each picture's rows, so **three fifths of the rows are still right** and training accuracy lands near 0.6. Alarm: *"If my test accuracy is higher than my training accuracy, my training labels are the first thing to check."*

**A4.** head swapped first → **(iii)** · everything frozen → **(v)** · `torch.cat` with a numpy array → **(i)** · predictions from the 5-to-9 model against all ten classes → **(ii)** · mixing `(n,1,8,8)` and `(n,8,8)` → **(iv)**

**A5.** Diagonal `50 + 52 + 51 + 45 + 51 = ` **249**; off-diagonal `1 + 3 + 1 + 2 + 3 + 1 + 2 + 4 + 2 + 1 = ` **20**; **249 + 20 = 269** ✅. 20 mistakes in 269, and `249 ÷ 269 = ` **0.9257**, the frozen-transfer row.

```text
8 & 9:  row 8 said 9 = 4,  row 9 said 8 = 1   ->  5
6 & 8:  row 6 said 8 = 2,  row 8 said 6 = 1   ->  3
5 & 8:  row 5 said 8 = 3,  row 8 said 5 = 0   ->  3
5 & 7:  row 5 said 7 = 0,  row 7 said 5 = 3   ->  3
```

**The worst pair is 8 and 9, with 5 mistakes.** Watch the direction on the last two: same total, opposite directions, so read both cells. A different pair from 1 and 8 is not surprising, because **1 is not in this problem**; the worst pair is always relative to the classes asked about, which is one more reason the table names the pile.

**A6.** Diagonal **529** · off the diagonal **11** · `529 + 11 = 540` **yes** · biggest off-diagonal cell **row 8, column 1, holding 3** · mirror cell **row 1, column 8, holding 1** · pair **1 and 8, with 4 of the 11 mistakes**. The written diagnosis is marked exactly as the Build It diagnosis below.

### ✍️ Practice Set B (B1–B5)

**B1.**

```text
[5 1 2 3 4]
[2 3 4 5 1]
[1 2 3 4 5]
```

The shift of 5 gives the original back, because all five numbers go all the way round.

**B2.** Expected output:

```text
original ink per picture: [4. 4. 4.]
wrapped  ink per picture: [4. 4. 4.]
blanked  ink per picture: [0. 0. 0.]
wrapped  row 0: [0 1 1 1 1 0]  <- the bar teleported
blanked  row 0: [0 0 0 0 0 0]  <- gone, as it should be
np.shares_memory(stack, np.roll(stack, 1, axis=1)) : False
np.shares_memory(stack, stack[1:])                 : True
```

**The blanked ink of ZERO is not a bug:** the whole picture was one bar on the bottom row; rolling down sent it to row 0 and blanking row 0 deleted it. It is a real cost: every shift sacrifices a row or column, which is harmless when the ink is mostly in the middle (so one-pixel shifts help) and costly on a two-pixel shift (a quarter of an 8×8 picture, which is why those usually hurt). `shares_memory` is **False** and **True**, so `.copy()` is **not strictly necessary** for `np.roll`; **keep it anyway**, because `stack[1:]` and `stack.T` are views and blanking a view silently corrupts the real training data.

**B3.** Shapes `(6285, 1, 8, 8)` and `(6285,)`, test tensor still `(540, 1, 8, 8)`; `1257 × 5 = 6285`, match **yes**. The labels must be glued in the same order because row 3,000 of the pictures and of the labels must be the same digit; otherwise the model trains on wrong pairings and **nothing errors** (the impossible test-above-train pattern, or a plausible mediocre number).

**B4.**

```text
freeze both convs   movable  650   0.2s  test 0.9257  (249 of 269)
freeze conv1 only   movable 1818   0.6s  test 0.9517  (256 of 269)
freeze nothing      movable 1898   1.1s  test 0.9665  (260 of 269)
```

A good prediction for the middle row is "between 0.9257 and 0.9665"; it landed at 0.9517. The counts are three subtractions: `1898 − 1248`, `1898 − 80`, `1898 − 0`. Pattern: *the less you freeze, the better it does and the slower it is.* In this seed-0 run every weight let loose bought accuracy; freezing both was lowest in all five seeds re-run, but the order of the other two is not stable across seeds, so do not mark that ordering as fixed. The prediction before running is what earns the mark.

**B5.** The program is in the student guide (Type This, Step 7). Expected results: `mistakes in total: 11 out of 540`, nine ranked mistakes (3 for 8→1, then eight single mistakes: 8→7, 6→1, 4→9, 3→7, 3→5, 2→1, 1→8, 1→5), `worst pair: 1 and 8, with 4 mistakes between them`, and

```text
average 1, ink per column: [  0   5  42  93 106  56   9   2]
average 8, ink per column: [ 0  9 71 87 86 66 11  0]
```

Addition check `529 + 11 = 540`. Both pile their ink into **columns 2 to 5** and peak in the middle. The 8 has slightly more in columns 2 and 5 (71 and 66 against 42 and 56), gaps of 29 and 10 summed over 8 pixels on a 0–16 scale, about 3.6 and 1.3 grey levels per pixel.

### 🐞 Fix the Broken Program

**Bug 1** — the `copies` list comprehension hands numpy arrays to `torch.cat`, which only glues tensors. Fix: `torch.from_numpy(...).float().unsqueeze(1)` on each copy, or (better) put every copy through the same `t4()` helper. Next run ends:

```text
ValueError: optimizer got an empty parameter list
```

**Bug 2** — `for p in model.parameters(): p.requires_grad = False` froze **everything**, so the list of trainable parameters is empty. Fix: delete the freezing loop (this program is not transfer learning), or freeze the convs only and check with `sum(p.numel() for p in model.parameters() if p.requires_grad)`. Third run:

```text
augmented: (6285, 1, 8, 8) (6285,)
train 0.5938   test 0.8889
```

**Bug 3, the silent one** — test (0.8889) is **higher** than train (0.5938), which is impossible. The line `np.roll(np.roll(X_train, dr, axis=0), dc, axis=1)`: `axis=0` is *which picture*. Fix: `axis=0` → `axis=1`, `axis=1` → `axis=2`.

| | bug 3 still in | all three fixed |
|---|---:|---:|
| train accuracy | **0.5938** | **0.9548** |
| test accuracy | **0.8889** | **0.9759** |

Twenty epochs, not forty, so the fixed numbers are below the chapter's 0.9926. Alarm: *test accuracy above training accuracy means the training labels are wrong.* **Marking notes.** Credit a student who finds bugs 1 and 2 from the error messages; bug 3 has no message and is the one to insist on. These broken-program numbers are from the workbook's own Answers section and were not re-run here, since they need the program as printed in the workbook.

### 🧩 Puzzle of the Week

| The change | same **digit**? | **cat photo** you might really meet? |
|---|---|---|
| shift one pixel left | **yes** | **yes** |
| shift one pixel left, wrapping | **no** | **usually yes** |
| flip left-to-right | **no** | **yes** |
| flip top-to-bottom | **no** | **no** (label true, picture unrealistic) |
| turn a quarter turn | **no** | **no** (label true, picture unrealistic) |
| turn upside down | **no** | **no** (label true, picture unrealistic) |
| make it 20% brighter | **yes** | **yes** |
| swap two pixels at random | **yes** (usually) | **yes** (usually) |

**Part 1.** Safe for digits: **shifting one pixel, and changing the brightness** (small random swaps are also broadly safe, just useless). Unsafe for cats: **flipping top-to-bottom and turning a quarter turn** (the label survives; they are unrealistic, not mislabelled). **Part 2.** The pair is **6 and 9**: an upside-down 6 is a real 9 carrying the old label. **Part 3.** Ink per row:

```text
ink per row, the upside-down 6: [39 57 61 36 27 32 29 25]
ink per row, the real 9      : [23 63 55 45 55 23 28 37]
```

Both are heaviest in rows 1 and 2 and thin out below; the upside-down 6 has a loop across the top and a tail running down and right, the shape of a 9. "Same digit?" **you would not confidently call it a 6.** (Recomputed for this file: these two rows reproduce exactly.) **Part 4**, full marks for the idea, not the words: *digits* — safe if a different person's handwriting could have done it (shifts, small brightness, small noise; no reflections or rotations). *Animals* — safe if a different camera or day could have produced it (flips, brightness, small crops and rotations; not upside-down or quarter turns unless real photos arrive that way). *Road signs* — almost nothing that moves pixels is safe, since a mirrored word is not a word; brightness, contrast, blur and weather-like noise are. **Part 5.** *"Which changes does it apply, and what kind of data were they chosen for?"* ("The usual set" is not a thing; a photo library will flip your digits silently.) A second good question: *does it augment the test set too?* Anything other than an immediate no means do not use it.

### 🤔 Think Deeper (T1–T2)

Both are paragraphs; mark on whether each hits its three points.

**T1.** (a) **What you would have learned instead:** two techniques and the habit "do this, it helps"; what you actually learned is the *condition each technique needs* (augmentation needs the label to stay true; transfer needs a source that knows far more than the target) plus the two checks that exposed the failures (training accuracy falling as data was added, and the from-scratch control). (b) **Why a measured price beats a belief:** a known price can be planned around. A frozen backbone cost about 5.6 points and bought a fifth of the training time where source and target were the same size, so with fifty pictures and someone's million-picture backbone you can predict which way the trade goes. (c) **Reading a paper:** look for the control, the denominators, and whether every comparison is on the same held-out pile; a paper where all four configurations beat the baseline has probably run more than four.

**T2.** (a) **What the 1985 feature has:** a hole-counter encodes something known about digits (an 8 has two enclosed regions, a 1 none), free and exact, but someone has to think of a feature for every distinction, which is why hand-designed vision stopped scaling. (b) **What the CNN has:** it found edge detectors itself from 1,257 pictures, reads 529 of 540 across all ten digits, and on a different problem will find whatever that problem needs. (c) **Where each belongs in a report:** the overall accuracy with its denominator goes in the results; the 1/8 pair, its cause, and the note that a simple hand-designed feature would fix it go in the limitations. Combining them (feeding a hole count in beside the learned features) is normal; at 8×8 the network demonstrably has not found that feature itself.

### 🛠️ Build It

This is the required homework. The checklist (steps 1–14) is a build log, not an answer sheet; mark the artefacts below. **Step 1 says "Page 27.2, in pen"; the workbook has no such page, so the predictions are on whatever sheet you handed out in class.** The prediction answers:

| | Most students predict | The truth |
|---|---|---|
| (a) wrapped vs plain | yes, more data is better | **no — exactly 0.00 points, 529 of 540 both times** |
| (b) blanked vs plain | yes | **yes — +1.30 points, 536 of 540** |
| (c) frozen / fine-tuned / scratch | frozen or fine-tuned | **from scratch, 0.9814, beating fine-tuned 0.9665 and frozen 0.9257** |

**Marking notes.** Present or absent. Nearly everybody gets (a) and (c) wrong and that is the design. What earns credit is a prediction with a reason attached, even a wrong one. A blank means the experiment was a demonstration. Step 10's print must say **650**; step 8's stage-one accuracy is not comparable to last week's because it is a five-class problem on different rows. For the frozen layers, `80 + 1,168 = 1,248` and `1,248 + 650 = 1,898`.

**The See It results table.**

| row | held-out pile | weights trained | seconds | test accuracy | test correct |
|---|---|---:|---:|---:|---|
| plain | **540 all-digit rows** | 1,898 | 2.4 | 0.9796 | 529 of 540 |
| augmented | **540 all-digit rows** | 1,898 | 11.3 | **0.9926** | 536 of 540 |
| frozen-transfer | **269 rows of 5–9** | 650 | 0.2 | 0.9257 | 249 of 269 |
| fine-tuned | **269 rows of 5–9** | 1,898 | 1.1 | 0.9665 | 260 of 269 |

**Which two comparisons are fair, and which one must never be made — full marks:**

> *"Two comparisons in this table are fair. **Rows 1 and 2**: `0.9926 − 0.9796 = +0.0130`, or seven more digits out of the same 540, and the only thing that changed was the training data. **Rows 3 and 4**: `0.9665 − 0.9257 = +0.0408`, or eleven more digits out of the same 269, and the only thing that changed was whether the conv layers were allowed to move. **The comparison I must not make is row 2 against row 3 or row 4**, because those are measured on different held-out piles — 540 digits across ten classes against 269 digits across five — and five classes is an easier problem than ten. Printing 0.9926 next to 0.9665 makes it look like a 2.6-point difference and it is not a difference at all."*

**The missing fifth row** (the "what fifth row is missing" box): **`scratch on 5-9`, 269 rows of 5–9, 1,898 weights, 1.1 seconds, `0.9814` — 264 of 269.** The row box takes the name and the number box takes **0.9814**. The four rows as asked cannot justify anything about transfer learning without it; a student who spots that is at level 5, so tell them so.

**Marking notes.** **The pile on every row is the objective.** Missing it once is a level-2 page, whatever else is right, and say why: *"which 540? which 269? if your reader can't tell, your table can lie."*

**Diagnose the worst confusion pair.** The counts, both directions:

```text
row 8, column 1 = 3      three real 8s were called 1
row 1, column 8 = 1      one real 1 was called 8
                 ---
                  4      of the 11 mistakes in total
```

11 mistakes out of 540, and **4 of them — more than a third — come from one pair out of the 45 possible pairs.** The ink-per-column rows are `average 1: 0 5 42 93 106 56 9 2` and `average 8: 0 9 71 87 86 66 11 0`; both pile their ink into **columns 2 to 5**.

**The diagnosis, a full-marks answer:**

> *"The pair is 1 and 8, with 4 of the 11 mistakes, and it leans one way: three 8s called 1 against one 1 called 8.*
>
> *At 8×8 an 8 is two loops stacked on top of each other, so each loop gets about three pixels of height and four of width. **A hole needs a ring of ink around a gap, and three pixels is not enough to have both.** So the loops fill in with grey, and what survives is a bright vertical stroke down the middle columns — which is exactly what a 1 is.*
>
> *You can see it in the average pictures. Adding up the ink in each column of the average 1 gives `0 5 42 93 106 56 9 2`, and for the average 8 it gives `0 9 71 87 86 66 11 0`. **Both pile their ink into columns 2 to 5 and both peak in the middle.** The 8 has a bit more ink out in columns 2 and 5 — 71 and 66 against 42 and 56 — but the gaps of 29 and 10 are sums over 8 pixels on a 0-16 scale, so about 3.6 and 1.3 grey levels per pixel, small next to the bright bar in the middle.*
>
> *The direction makes sense too. **An 8 can lose its holes and turn into a bar. A bar cannot grow holes.** The information loss only goes one way, so the confusion should be lopsided, and it is: three against one."*

**The fixes box.** *Cause:* more pixels (at 16×16 an 8's loops have room to be holes), or a different kind of feature, such as counting enclosed regions, which a hand-designed system in 1985 would have done and which separates these two instantly. *Symptom only:* train longer on 1s and 8s, or add extra shifted copies of just those two classes; it would probably move those four mistakes, you must then check what it broke, and no amount of training puts information into 64 pixels that is not there.

**Marking notes.** **This is the part you mark hardest and the bar is one question: did they say something about what 64 pixels can and cannot show?**

- ✅ Full marks: the loops are too small to hold a hole, so they fill in and leave a bar. Anything that reaches that idea, however phrased.
- ✅ Level 5: notices the **asymmetry** and explains the direction. Three against one is too few to prove anything alone, but it is what information loss going one way predicts.
- ✅ Also level 5: proposes a fix that addresses the cause rather than the symptom.
- ❌ Zero: *"the model confused 1 and 8 four times out of eleven"*, or *"they look similar"*, or *"the model needs more training"*. Hand it back once, with one question written on it: **"what do a 1 and an 8 actually share when you only have 64 pixels?"**

**The Term 3 reflection — a full-marks set:**

> **W20.** *"I can get a slope out of PyTorch instead of computing it. `w.grad` gave me the same number — 42 — that I got by hand in Week 18 by measuring stage by stage."*
>
> **W21.** *"I can write the training loop from memory. Five lines, and 6 hand-typed hours-vs-marks points get a straight line through them in about 400 steps."*
>
> **W22.** *"I can count a network's parameters before building it, and spot overfitting on a graph. `2 → 16 → 1` is 65 numbers, and I watched the validation loss turn upward while the training loss kept falling."*
>
> **W23.** *"I can write my own `nn.Module` and feed it batches. 1,257 digits at 32 at a time is 40 steps per epoch, which I worked out three different ways."*
>
> **W24 and W25.** *"I can work out every shape in a stack on paper before running it. An 8 stays an 8 with padding 1 and drops to 6 without, and `16 × 2 × 2 = 64` is the number that goes in my `Linear` layer."*
>
> **W26.** *"I can train a CNN and look at what it learned. 1,898 weights, 529 of 540 held-out digits, about three seconds — and filter 6 answers +2.830 to a bright-left edge, so it taught itself to be an edge detector."*

**Marking notes.** **One number per line, six lines, six numbers.** A line without a number is a feeling and it comes back. **Accept their own numbers over this file's** — a Week 26 line saying "527 of 540, five seconds" means they ran it.

### 🎨 Draw It

- **Blanked edges, one per copy:** shifted up → blank the **bottom** row · down → the **top** row · left → the **right** column · right → the **left** column; the fifth, unshifted copy blanks nothing.
- **Weight counts:** **1,248 frozen, 650 movable, total 1,898.**
- **Number in the control box:** **0.9814.**
- **Why the control box has to be on the drawing:** *"Because 0.9257 on its own is a number and not a result. With 0.9814 next to it, the drawing says what borrowing cost as well as what it bought — and anybody looking at it can see that the technique lost, which is the honest thing for the picture to say."*
- **Great versus good:** the great drawing shows the **540 test rows as a separate, untouched block marked "never shifted"**. The accuracy pair `0.9796 → 0.9926` with `+1.30 points` also earns marks.

### 📊 Self-Check

Not marked; there are no right answers. Three rows predict the capstone in Weeks 34 to 36. If **"ask 'compared to what?'"** is a 😕, cover the `scratch on 5-9` row and show that 0.9257 and 0.9665 are not a story until the control is on the page. If **"a results table with the held-out pile on every row"** is a 😕, it is the most transferable habit of Term 3 and costs ten seconds a table; have them redo Build It's table. If **"diagnose a confusion pair physically"** is a 😕, have them draw an 8 inside an 8×8 grid on squared paper and try to fit two holes in it. They cannot, which is the whole diagnosis.

### Stretch (not in the workbook) — does transfer learning win when the target task is tiny?

*Cut the digits-5-to-9 training set to 100 rows and rerun all three.*

```python
import time
import numpy as np
import torch
import torch.nn as nn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

digits = load_digits()
X_train, X_test, y_train, y_test = train_test_split(
    digits.images / 16.0, digits.target, test_size=0.30, random_state=0,
    stratify=digits.target)
t4 = lambda a: torch.from_numpy(np.asarray(a)).float().unsqueeze(1)
Xtr, ytr = t4(X_train), torch.from_numpy(y_train).long()
Xte, yte = t4(X_test), torch.from_numpy(y_test).long()

def make_cnn():
    return nn.Sequential(
        nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Flatten(), nn.Linear(64, 10))

def train(m, X, y, epochs):
    movable = [p for p in m.parameters() if p.requires_grad]
    loader = DataLoader(TensorDataset(X, y), batch_size=32, shuffle=True)
    lf, opt = nn.CrossEntropyLoss(), torch.optim.Adam(movable, lr=1e-3)
    t0 = time.perf_counter()
    for _ in range(epochs):
        m.train()
        for xb, yb in loader:
            opt.zero_grad(); lf(m(xb), yb).backward(); opt.step()
    return time.perf_counter() - t0

def acc(m, X, y):
    m.eval()
    with torch.no_grad():
        return (m(X).argmax(1) == y).float().mean().item()

hi_te = y_test >= 5
rng = np.random.default_rng(0)
small = rng.choice(np.where(y_train >= 5)[0], size=100, replace=False)
print("100-row label counts:", np.bincount(y_train[small], minlength=10))

torch.manual_seed(0)
first = make_cnn()
train(first, Xtr[y_train <= 4], ytr[y_train <= 4], 40)
print("stage 1, digits 0-4: test %.4f" % acc(first, Xte[y_test <= 4], yte[y_test <= 4]))
backbone = {k: v.clone() for k, v in first.state_dict().items()}

for name in ("frozen", "fine", "scratch"):
    torch.manual_seed(0)
    m = make_cnn()
    if name != "scratch":
        m.load_state_dict(backbone)
    m[7] = nn.Linear(64, 10)
    if name == "frozen":
        for layer in (m[0], m[3]):
            for p in layer.parameters():
                p.requires_grad = False
    s = train(m, Xtr[small], ytr[small], 100)
    print("%-8s 100 rows  %4.1fs  movable %4d  train %.4f  test %.4f"
          % (name, s, sum(p.numel() for p in m.parameters() if p.requires_grad),
             acc(m, Xtr[small], ytr[small]), acc(m, Xte[hi_te], yte[hi_te])))
```

**The real output:**

```text
100-row label counts: [ 0  0  0  0  0 17 20 20 18 25]
stage 1, digits 0-4: test 0.9926
frozen   100 rows   0.1s  movable  650  train 0.8900  test 0.8848
fine     100 rows   0.9s  movable 1898  train 0.9800  test 0.9257
scratch  100 rows   1.0s  movable 1898  train 0.9500  test 0.9628
```

**And the honest answer: no. Even at 100 rows, from scratch still wins — 0.9628 against 0.9257 and 0.8848.**

**Which is a better result than a win would have been, and here is the reason.** This network has 1,898 weights and the pictures are 64 pixels. **It is small enough and the problem is simple enough that 100 examples of five digit shapes is already nearly enough to learn them from nothing.** Transfer learning solves the problem of *not having enough data to learn features from scratch*, and on 8×8 digits that problem barely exists.

**The condition it needs, stated as arithmetic:** the source dataset has to be very much larger than the target. Real transfer learning: **1,200,000 source pictures against a few thousand target pictures — a ratio of hundreds to one.** Ours: **630 against 100 — a ratio of six to one, and specialised to the wrong shapes.**

**Marking notes.** **Full marks is the number plus the "why".** A student who runs it, reports that scratch still wins, and says *"the source wasn't big enough relative to the target"* has done real experimental work. **A student who keeps shrinking the target set to find the crossover point and reports honestly that they could not find one has done better work than the assignment asked for.**

### Answers to every question posed in the lesson

**Hook — "add up the diagonal."** **529.** **"Add up everything off it."** **11.** **"What must they add to?"** 540, the number of test rows. **529 + 11 = 540** ✅

**Hook — "find the biggest number not on the diagonal."** Row 8, column 1: **3** — three real 8s called 1. **"Anything in the mirror position?"** Row 1, column 8: **1**. **So the pair is 1 and 8, with 4 of the 11 mistakes.**

**Concept — "the bottom row slid off. Where did it go?"** **Round to the top.** `np.roll` wraps.

**Concept — "is it still a 6?"** **No** — and the label still says 6, so that training row now has a wrong label.

**Concept — "is 'there is a vertical edge here' useful for reading a 3? A 7? A face?"** Yes to all of them. **Edges are about pictures, not about digits**, which is the whole reason a backbone is worth borrowing.

**Concept — "we have no internet. How can we test the idea with what we have?"** **Split the dataset into two problems.** Train on digits 0–4, then move to digits 5–9 with a fresh head.

**Concept — "what would training from scratch have given?"** **The question that makes it an experiment.** Without it, 0.9257 is a number and not a result. **0.9814, and it beat both transfer versions.**

**Live-code step 2 — "1,257 rows, five copies. What shape?"** `(6285, 1, 8, 8)`. **And 6,285 labels, which you check.**

**Live-code step 3 — "what did the wrapped version buy?"** **Nothing, in this seed-0 run.** `529 of 540` both times, `+0.00 points`. And its *training* accuracy fell from 0.9881 to 0.9774 (on different rows, 6,285 against 1,257), consistent with part of its training data being wrong.

**Live-code step 3 — the blanked version.** **`536 of 540`, `+1.30 points`, seven more digits, no new data.**

**Live-code step 4 — "something about those two numbers is impossible. What?"** **`train 0.5968` and `test 0.8574`: the test score is higher than the training score.** A model has seen its training data and must do at least as well on it. The cause is `axis=0`, which shifted the *pictures* while the labels stayed put, so two fifths of the training rows (the up and down copies) were mislabelled and unlearnable. **Permanent alarm: test above train means the labels are wrong.**

**Live-code step 5 — "what order did I do them in?"** Head swapped first, then `load_state_dict`. **It must be the other way round: load the whole saved network, then replace the head.** The error names both shapes, `[10, 64]` and `[5, 64]`, and Week 25's question still applies.

**Live-code step 5 — the movable count.** **650, not 1,898**, and it is the only proof that the freezing worked.

**Activity step 1 — "0.9926 on five classes against 0.9796 on ten. Is this network better?"** **No.** Five classes is an easier problem — random guessing scores 20% instead of 10%. **You cannot compare those two numbers, and that is why the pile goes on every row.**

**Activity step 2 — "where did the other 1,248 weights go?"** Frozen: conv1's 80 plus conv2's 1,168. **80 + 1,168 + 650 = 1,898** ✅

**Activity step 3 — "frozen 0.9257, unfrozen 0.9665. By how many digits?"** **Eleven: 260 against 249, out of 269.** Four accuracy points, and unlikely to be noise (frozen was lowest in 5 of 5 seeds) — letting the filters adjust to the new digit shapes probably helped.

**Activity step 4 — "which column won?"** **From scratch, 0.9814, in this run** (scratch beat fine-tuned in 4 of 5 seeds we re-ran). **"So what did borrowing buy?"** 650 movable weights instead of 1,898, 0.3 seconds instead of 1.5, **and it cost 5.6 accuracy points.**

**Activity step 4 — "why didn't it work?"** **A likely reason: we borrowed from an equal (untested, so a hypothesis).** The source was 630 pictures of five digits; the target was 627 pictures of five different digits. Transfer learning needs the source to know very much more than the target — the real version is 1.2 million against a few thousand.

**Wrap — "can I say augmentation is 6.7 points better than frozen transfer?"** **No.** 540 all-digit rows against 269 rows of five classes. **Two different exams.** The fair comparisons are `0.9926 − 0.9796` and `0.9665 − 0.9257`.

**Variation-harder 1 — the 100-row target task.** Frozen **0.8848**, fine-tuned **0.9257**, from scratch **0.9628**. **Scratch still wins.** Full numbers and the reason in the Answer Key's stretch section.

**Variation-harder 2 — freeze one conv layer only.** Freezing `frozen[0]` alone leaves `1,168 + 650 = 1,818` movable, and the accuracy lands between the frozen and the fine-tuned numbers, which is what you would predict — the less you freeze, the closer you get to fine-tuning.

**Variation-harder 3 — two-pixel shifts, nine copies.** `1,257 × 9 = 11,313` rows. **It usually hurts**, because two pixels out of eight is a quarter of the picture and even a blanked two-pixel shift can push a digit's ink to the edge. **The skill being learned is finding the point where augmentation turns from help to harm, and it is data-specific.**

**Variation-harder 6 — the augmented model's confusion matrix.** It made **4 mistakes out of 540**. **And there is no rankable worst pair in four mistakes** — every cell is a 1 or a 0. **Knowing you have run out of data to analyse is the level-5 answer**, and it is a real thing that happens on real projects.

---

## 🔮 Next Week Preview

Next week Term 4 starts and the labels go away. Every model in this course so far has been handed the answers — 1,257 digits with 1,257 labels, and a loss that measured how far off it was. **Next week there are no answers at all**, and the question becomes: given six two-dimensional points typed on the board, can you find the groups nobody told you about? The student meets **k-means**: put down some centres, colour each point by whichever centre is nearest, move each centre to the middle of its own colour, and repeat until nothing moves — done by hand, on six points, for three rounds, before any code.

Then the number that measures whether a set of groups is any good, **inertia**, which arrives with **sigma notation** — introduced honestly as "add up all of these", with the full expanded sum written out beside the symbol every single time. Then `KMeans` on `load_wine`: 178 wines, 13 measurements each, no labels, and the question of whether the three clusters it finds have anything to do with the three real grape varieties.

**To prep early:** three things. **One — the wall sheets from Terms 2 and 3 come down today** and a new one goes up next week headed **SIX POINTS**, with a blank grid on it; k-means is drawn, not printed, and it needs somewhere to be drawn. **Two — check `from sklearn.datasets import load_wine` works tonight** and that `load_wine().data.shape` prints `(178, 13)`. It ships inside scikit-learn, so no internet is needed, but you want to have seen it load. **Three — get squared paper and three colours of pen for every student.** Next week's activity is six points recoloured three times by hand, and it does not work in one colour.

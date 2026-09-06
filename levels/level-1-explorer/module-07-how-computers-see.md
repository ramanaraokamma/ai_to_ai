# Module 7 — How Computers See: Pixels, Grids, and Edges

**Level 1 · Module 7 · ~3 hours · Prereqs: Module 4 (features), Module 5 (training a Teachable Machine model), Module 6 (test sets, accuracy, per-class scores)**

[⬅ Previous](module-06-train-test-trust.md) · [Level 1 Home](README.md) · [Next ➡](module-08-how-computers-read-and-chat.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** explain an image as a grid of numbers, and colour as three stacked grids, using a real example you typed out yourself.
2. **You will be able to** hand-compute the output of a 3×3 filter on a small pixel grid — every multiplication, every sum — and say what the answer means.
3. **You will be able to** explain why resolution, lighting, and background change what a vision model predicts, with numbers rather than hand-waving.
4. **You will be able to** describe why **edges** are the first genuinely useful feature a vision system finds, and prove one reason arithmetically.
5. **You will be able to** look at a wrong prediction from your own Module 5 model and make a specific, testable guess about which pixels fooled it.

---

## 🪝 The Hook

In Module 6 you found the class your model was worst at. You wrote down the number. And then you got stuck, because the obvious next question has no obvious answer: **why?**

You cannot ask the model. It has no words. It never saw your comb. It never saw a comb-shaped thing at all.

Here is what it actually received: a rectangle of numbers, 224 across and 224 down, three deep — 150,528 whole numbers between 0 and 255, arriving in a fixed order, with no labels saying "this part is the comb" and "this part is the table". Everything the model knows about combs, it worked out from patterns in those numbers.

So if you want to know why it failed, you have to stop looking at your photo and start looking at the numbers. That sounds impossible. It isn't. By the end of today you will have taken a picture apart into a spreadsheet, run the same edge-finding arithmetic that sits at the bottom of every vision system on Earth, and watched an outline appear out of nothing but addition and subtraction.

---

## 🧠 The Concept

Five ideas. Each one gets a plain explanation, an everyday anchor, and small numbers you can check on paper.

---

### 1️⃣ A pixel is one number: 0 is black, 255 is white

Hold your phone screen right up against your eye — closer than you can focus. Look at a white area. If your screen is bright enough and your eye is close enough, the smooth white breaks apart into a grid of tiny squares. Those squares are real. They are the whole picture.

> **Pixel** — one tiny square of an image, and the smallest piece a computer can store. The word is short for "picture element".
> **Grayscale** — a black-and-white image where each pixel is a single number for brightness.

In a grayscale image, every pixel is stored as **one whole number from 0 to 255**:

| Number | Looks like | Everyday anchor |
|---:|---|---|
| 0 | pure black | a switched-off screen in a dark room |
| 32 | very dark grey | shadow under a bed |
| 64 | dark grey | dark denim jeans |
| 128 | middle grey | a pencil-shaded box, an elephant |
| 191 | light grey | a cloudy sky |
| 224 | very light grey | a white wall in shade |
| 255 | pure white | fresh paper in sunlight |

**Why 0 to 255 and not 0 to 100?** Because computers store things in **bytes**, and one byte holds exactly 256 different values: 0, 1, 2, … , 255. Nobody chose 255 because it was pretty. It is just what fits in one byte, and one byte per pixel is cheap. That is the entire reason, and you now know something most adults don't.

🍕 **Analogy — the mosaic wall.** A mosaic is a picture made of hundreds of coloured tiles. Stand close and you see tiles. Stand back and you see a face. Nobody carved a nose; the nose is what happens when enough tiles agree. A digital image is a mosaic where every tile is a number, and your eye does the standing-back.

**Tiny concrete example.** Here is a 5×5 grayscale image. Left is the numbers, right is what your eye sees when each number is shaded in.

```
      NUMBERS                          SHADED
   c1  c2  c3  c4  c5
r1  0   0   0   0   0            ██  ██  ██  ██  ██     ██ = 0    (black)
r2  0  255 255 255  0            ██  ░░  ░░  ░░  ██     ▓▓ = 128  (grey)
r3  0  255 128 255  0            ██  ░░  ▓▓  ░░  ██     ░░ = 255  (white)
r4  0  255 255 255  0            ██  ░░  ░░  ░░  ██
r5  0   0   0   0   0            ██  ██  ██  ██  ██
```

That is a white square with a grey dot in the middle, on a black background. Twenty-five numbers. No picture file, no magic — just twenty-five numbers in a known order.

**Position matters and is not stored.** The number 255 in row 2 column 2 does not carry a label saying "I am in row 2 column 2". The computer knows where it is only because the numbers arrive in a fixed order: row 1 left-to-right, then row 2 left-to-right, and so on. Shuffle the order and the picture is destroyed even though every number is still there. **An image is numbers *plus* their arrangement.**

---

### 2️⃣ Colour is three grids stacked on top of each other

Grayscale needs one number per pixel. Colour needs three.

> **RGB** — a way of storing colour as three numbers per pixel: how much **R**ed, how much **G**reen, how much **B**lue. Each is 0–255.

Every colour you have ever seen on a screen is a mix of exactly three lights: red, green, blue. Not paint — **light**. Mixing lights is different from mixing paint. Red light plus green light makes yellow, which sounds wrong until you look at a screen through a magnifying glass and see the tiny red and green stripes glowing side by side.

```
        ONE COLOUR IMAGE  =  THREE NUMBER GRIDS STACKED

            ┌──────────────────┐
            │  BLUE  grid      │   how much blue in each pixel (0-255)
          ┌─┴────────────────┐ │
          │  GREEN grid      │ │   how much green in each pixel (0-255)
        ┌─┴────────────────┐ │ │
        │  RED   grid      │ │ │   how much red  in each pixel (0-255)
        │                  │ │─┘
        │   224 x 224      │─┘
        └──────────────────┘

        224 x 224 x 3  =  150,528 numbers for ONE small photo
```

**Reading colours off the numbers.** Learn these eight and you can read most RGB triples on sight:

| R | G | B | Colour | Why |
|---:|---:|---:|---|---|
| 255 | 0 | 0 | red | only the red light is on |
| 0 | 255 | 0 | green | only green |
| 0 | 0 | 255 | blue | only blue |
| 255 | 255 | 0 | yellow | red + green light |
| 0 | 255 | 255 | cyan (sky blue) | green + blue |
| 255 | 0 | 255 | magenta (hot pink) | red + blue |
| 255 | 255 | 255 | white | all three at full |
| 0 | 0 | 0 | black | all three off |

And the key rule: **when R, G, and B are all equal, the pixel is grey.** (100, 100, 100) is a dark grey. (200, 200, 200) is a light grey. Grey is not a colour so much as a tie.

**Tiny concrete example — one pixel of skin in a photo:** R = 200, G = 80, B = 40. More red than green, more green than blue → a warm brown-orange. Now turn it grayscale by averaging:

```
   gray = (R + G + B) ÷ 3
        = (200 + 80 + 40) ÷ 3
        = 320 ÷ 3
        = 106.67  →  round to 107
```

107 is a middling dark grey. Notice what just happened: three numbers became one. **You cannot get the colour back.** (200, 80, 40) and (107, 107, 107) and (0, 200, 121) all average to 107. Turning colour into grey is a one-way door.

> Real photo software uses a slightly fancier formula — roughly `0.30×R + 0.59×G + 0.11×B` — because human eyes are far more sensitive to green than to blue. For everything in this module, plain averaging is fine.

🍕 **Analogy — three stage lights.** Imagine a school play with three spotlights aimed at the same spot: one red, one green, one blue, each with its own dimmer knob from 0 to 255. Every colour on stage is just a setting of three knobs. A photo is 150,528 knob settings, written down.

**How many colours can one pixel be?** 256 × 256 × 256 = **16,777,216**. Sixteen million. That is why screens are advertised as "16.7 million colours" — it is not a boast, it is just 256 cubed.

---

### 3️⃣ Resolution: shrinking an image throws information away, permanently

> **Resolution** — how many pixels an image has, written width × height. More pixels = more detail = more numbers to store.

Your phone camera might shoot 4032 × 3024 pixels. That is 4032 × 3024 = **12,192,768 pixels** — where the phrase "12 megapixel" comes from ("mega" = million).

Teachable Machine, the tool you used in Modules 5 and 6, does **not** look at 12 million pixels. Before training, it squashes every photo you upload down to **224 × 224**.

```
   224 × 224 = 50,176 pixels

   12,192,768 ÷ 50,176 = 243
```

Your model saw **1/243rd** of the pixels you took. Two hundred and forty-two out of every 243 pixels were thrown in the bin before training even started. Sit with that for a second — it explains an enormous amount about why vision models fail.

**Why do it at all?** Three reasons, all practical: 12 million numbers per photo × 60 photos is far too much for a browser to handle; small images train in seconds instead of hours; and most of the fine detail genuinely does not help tell a comb from a spoon.

**How shrinking works: block averaging.** To halve an image, you take each 2×2 block of four pixels and replace it with their average.

🔍 **Tiny concrete example A — a thin diagonal line survives, but faintly.**

```
   BEFORE (4x4)                 2x2 BLOCK AVERAGES              AFTER (2x2)

   255   0 |  0   0     top-left  = (255+0+0+255)/4 = 127.5      128    0
     0 255 |  0   0     top-right = (0+0+0+0)/4     = 0
   ---------+---------  bot-left  = (0+0+0+0)/4     = 0            0  128
     0   0 |255   0     bot-right = (255+0+0+255)/4 = 127.5
     0   0 |  0 255
```

The bright diagonal is still visible — but it went from crisp white (255) to washed-out grey (128). Detail became mush.

🔍 **Tiny concrete example B — a checkerboard vanishes completely.**

```
   BEFORE (4x4)                 EVERY 2x2 BLOCK                 AFTER (2x2)

   255   0 | 255   0      (255 + 0 + 0 + 255) / 4               128  128
     0 255 |   0 255       = 510 / 4
   ---------+---------     = 127.5                              128  128
   255   0 | 255   0
     0 255 |   0 255      ...the same for all four blocks
```

A bold, high-contrast pattern turned into a flat grey rectangle. **Every single pixel is now identical.** If the checkerboard was the only thing distinguishing two classes, your model has just been blinded, and no amount of extra training will help.

🍕 **Analogy — the photocopy of a photocopy.** Copy a page, copy the copy, copy that. The words survive for a while; the fine print dies first. Shrinking an image is the same trade: big shapes survive, thin details die. You cannot un-copy.

**The practical rule:** if the thing that tells your two classes apart is *thin* — a hairline crack, small printed text, the teeth of a comb — a 224×224 model may literally never see it. That is not the model being stupid. The information was deleted before the model was born.

---

### 4️⃣ A filter is a tiny number grid you slide over the image

Now the good part. You have an image made of numbers. How do you get from "a pile of numbers" to "there is an object here"?

You start with a **filter**.

> **Filter** (also called a **kernel**) — a small grid of numbers, usually 3×3, that you slide over the image. At each stop you multiply the filter's numbers by the pixels underneath, add up all the results, and write that one number into a new grid.

That's it. Multiply, add, write down, slide one step right. Repeat.

```
   HOW A 3x3 FILTER SLIDES  (an image, one stop, and the number it produces)

   IMAGE (6x6)                        FILTER (3x3)
   ┌───┬───┬───┬───┬───┬───┐          ┌────┬───┬────┐
   │ 0 │ 0 │ 0 │ 0 │ 0 │ 0 │          │ -1 │ 0 │ +1 │
   ├───┼───┼───┼───┼───┼───┤          ├────┼───┼────┤
   │ 0 │255│255│255│255│ 0 │          │ -1 │ 0 │ +1 │
   ├───┼───┼───┼───┼───┼───┤          ├────┼───┼────┤
   │ 0 │255│255│255│255│ 0 │          │ -1 │ 0 │ +1 │
   ├───┼───┼───┼───┼───┼───┤          └────┴───┴────┘
   │ 0 │255│255│255│255│ 0 │
   ├───┼───┼───┼───┼───┼───┤            slide it here ─┐
   │ 0 │255│255│255│255│ 0 │                           │
   ├───┼───┼───┼───┼───┼───┤          ┌────────────────▼──┐
   │ 0 │ 0 │ 0 │ 0 │ 0 │ 0 │          │  0  0  0          │
   └───┴───┴───┴───┴───┴───┘          │  0  255 255       │  the 3x3 patch
                                      │  0  255 255       │  under the filter
                                      └───────────────────┘

   multiply and add:
       (-1×0)  + (0×0)   + (+1×0)      =    0
     + (-1×0)  + (0×255) + (+1×255)    = +255
     + (-1×0)  + (0×255) + (+1×255)    = +255
     ────────────────────────────────────────
       ONE OUTPUT NUMBER               =  510
```

**What does the filter above actually do?** Read it in words: *take the three pixels on the right, subtract the three pixels on the left.* If the right side is much brighter than the left, you get a big positive number. If the left is much brighter, a big negative number. If both sides look the same — plain wall, plain table, plain sky — you get **zero**.

So this filter answers one question, at every position in the image: **"does the brightness suddenly change as I move sideways here?"** That is a vertical edge detector.

Two filters do most of the work:

| Filter | Grid | In words | Finds |
|---|---|---|---|
| **Vertical edge** | `-1 0 +1`<br>`-1 0 +1`<br>`-1 0 +1` | right column − left column | up-and-down lines |
| **Horizontal edge** | `-1 -1 -1`<br>`  0  0  0`<br>`+1 +1 +1` | bottom row − top row | side-to-side lines |

🍕 **Analogy — the rubber stamp with a question on it.** Picture a rubber stamp the size of a postage stamp. The stamp asks one question: "brighter on the right than the left?" You press it down on the top-left corner of a poster, write the answer in a notebook, move it one centimetre right, press again, write again — all the way across, then down a row, and again, until the whole poster is covered. Your notebook is now a *map of where the answer was yes*. That map is the filter's output.

**Two housekeeping details you need for the arithmetic to work.**

*Detail 1 — the output is smaller.* A 3×3 filter needs a full ring of neighbours, so it cannot sit on the outermost row or column. A 6×6 image gives a 4×4 output. A 12×12 gives 10×10. The rule: **output size = input size − 2** (for a 3×3 filter).

*Detail 2 — the answers can go outside 0–255.* The biggest possible output of the vertical filter is 3 × 255 = **765**, and the smallest is **−765**. To turn that back into something you can shade in, you do two things:

1. **Take the absolute value** — throw away the minus sign. An edge is an edge whether it goes dark→bright or bright→dark. `|−765| = 765`.
2. **Clip at 255** — anything 255 or above becomes 255. (Or divide by 3 and round. Either is fine as long as you say which one you did.)

---

### 5️⃣ Edges are the first useful feature — and backgrounds are the first trap

Why edges? Why not "average brightness" or "amount of red"?

Because **edges survive the things that change, and raw brightness doesn't.**

🔍 **Proof you can do in your head.** Take a two-pixel-wide slice of a photo: a dark object (value 40) next to a bright wall (value 200).

*Someone turns on a lamp and everything gets 50 brighter:*

```
   before:  object 40    wall 200   →  difference = 200 − 40  = 160
   after:   object 90    wall 250   →  difference = 250 − 90  = 160   ← IDENTICAL
```

The raw pixel values both changed by 50. The **difference did not change at all.** And a difference is exactly what an edge filter computes.

This is not a coincidence — it is arithmetic. Look at the vertical filter's nine weights: −1, 0, +1, −1, 0, +1, −1, 0, +1. Add them up: **they sum to zero.** Add the same number *k* to every pixel in the patch and the filter's answer changes by `k × 0 = 0`. **A filter whose weights sum to zero is completely blind to overall brightness.** That is why edges are a better feature than brightness: they hold still when the lighting moves.

(They are not *perfectly* stable. If the lamp *multiplies* brightness instead of adding to it — half brightness, say — edges shrink too. You will compute exactly that in Practice 6.)

**Edges build up into everything else.** Here is the ladder every vision system climbs:

```
   PIXELS            EDGES              PARTS               OBJECTS
   ───────           ───────            ───────             ───────
   0 0 0 0 0        ╱  ╲  │  ─          eye-ish blob        "cat"
   0 255 255 0      short lines         ear-ish corner
   0 255 128 0      at angles           whisker-ish lines
   raw numbers      Level 1 (today)     Level 3            Level 3
```

Today you build the first rung by hand. In Level 3 you will meet systems that discover their own filters instead of using the ones you wrote — but they are still filters, and they still slide, and they still multiply-and-add. Nothing you learn today gets thrown away.

**Now the trap.** ⚠️ The filter does not know what you care about. It reports edges *everywhere* — including all the edges in your background.

Recall Module 5, Experiment 2: you trained on photos taken entirely on one wooden table, and the model scored beautifully on that table and fell apart at the sink. Here is that failure in pixel language: the wood grain produced a strong, consistent, repeated pattern of thin edges in every single training photo of one class. The pattern was **more consistent than the object itself**, because the object moved and rotated between shots while the table did not. Learning "wood grain" was easier than learning "comb". The model took the easy road, because it always does.

> **The background rule:** a vision model learns whatever is most reliably associated with the label. If your background is more reliable than your object, you have trained a background detector and given it your object's name.

**Three background traps, all real:**

| Trap | What the pixels actually show | Fix |
|---|---|---|
| One surface per class | class A always on wood, class B always on tile | shoot every class on every surface |
| Your hand is in shot for one class | fingers appear only with class C | hold all classes, or none |
| Shadow direction | window on the left in all morning photos | shoot at different times of day |

---

## 🔍 Worked Example

**Goal:** take one small image all the way from numbers to an outline, showing every multiplication and every sum. Nothing skipped.

### Step 1 — The image

A 6×6 grayscale image: a white 4×4 square on a black background.

```
        c1   c2   c3   c4   c5   c6
   r1    0    0    0    0    0    0
   r2    0  255  255  255  255    0
   r3    0  255  255  255  255    0
   r4    0  255  255  255  255    0
   r5    0  255  255  255  255    0
   r6    0    0    0    0    0    0
```

36 pixels. Sum check: 16 pixels at 255 = 4080; average brightness = 4080 ÷ 36 = 113.3.

### Step 2 — The two filters

```
   V (vertical edges)          H (horizontal edges)
   -1   0  +1                  -1  -1  -1
   -1   0  +1                   0   0   0
   -1   0  +1                  +1  +1  +1

   "right column                "bottom row
    minus left column"           minus top row"
```

Output size = 6 − 2 = **4×4**. The output cell at position (r, c) uses the 3×3 patch centred on image pixel (r, c), so r and c each run from 2 to 5.

### Step 3 — Compute V, one cell at a time

**V at (2,2)** — patch = rows 1–3, cols 1–3:

```
      0    0    0
      0  255  255
      0  255  255

   right column (col 3) = 0 + 255 + 255 = 510
   left  column (col 1) = 0 +   0 +   0 =   0
   V(2,2) = 510 − 0 = +510
```

**V at (2,3)** — patch = rows 1–3, cols 2–4:

```
      0    0    0
    255  255  255
    255  255  255

   right column (col 4) = 0 + 255 + 255 = 510
   left  column (col 2) = 0 + 255 + 255 = 510
   V(2,3) = 510 − 510 = 0
```

**V at (2,4)** — patch = rows 1–3, cols 3–5: left col 3 = 510, right col 5 = 510 → **0**.

**V at (2,5)** — patch = rows 1–3, cols 4–6: left col 4 = 0 + 255 + 255 = 510, right col 6 = 0 + 0 + 0 = 0 → **−510**.

**V at (3,2)** — patch = rows 2–4, cols 1–3:

```
      0  255  255
      0  255  255
      0  255  255

   right column (col 3) = 255 + 255 + 255 = 765
   left  column (col 1) =   0 +   0 +   0 =   0
   V(3,2) = 765 − 0 = +765
```

**V at (3,3)**: left col 2 = 765, right col 4 = 765 → **0**.
**V at (3,4)**: left col 3 = 765, right col 5 = 765 → **0**.
**V at (3,5)** — patch rows 2–4, cols 4–6: left col 4 = 765, right col 6 = 0 → **−765**.

**Row 4 of the output** is identical to row 3, because image rows 3, 4 and 5 are identical: **+765, 0, 0, −765**.

**V at (5,2)** — patch = rows 4–6, cols 1–3:

```
      0  255  255
      0  255  255
      0    0    0

   right column (col 3) = 255 + 255 + 0 = 510
   left  column (col 1) =   0 +   0 + 0 =   0
   V(5,2) = +510
```

**V at (5,3)**: left col 2 = 255+255+0 = 510, right col 4 = 510 → **0**.
**V at (5,4)**: **0**. **V at (5,5)**: left col 4 = 510, right col 6 = 0 → **−510**.

**The V output grid:**

```
      +510     0     0   −510
      +765     0     0   −765
      +765     0     0   −765
      +510     0     0   −510
```

Read it out loud: *strong positive on the left, strong negative on the right, nothing in the middle.* The filter found the square's left edge (dark→bright, positive) and right edge (bright→dark, negative) — and it is **completely blind to the top and bottom edges**, which are also there in the image. A vertical-edge filter only sees vertical edges. That is why you need more than one.

### Step 4 — Compute H

**H at (2,2)** — patch = rows 1–3, cols 1–3: bottom row (r3) = 0 + 255 + 255 = 510; top row (r1) = 0 + 0 + 0 = 0 → **+510**.

**H at (2,3)** — patch rows 1–3, cols 2–4: bottom row (r3) = 255 + 255 + 255 = 765; top row = 0 → **+765**.

**H at (2,4)**: bottom (r3, cols 3–5) = 255+255+255 = 765; top = 0 → **+765**.
**H at (2,5)**: bottom (r3, cols 4–6) = 255+255+0 = 510; top = 0 → **+510**.

**H at (3,2)** — patch rows 2–4, cols 1–3: bottom row (r4) = 0+255+255 = 510; top row (r2) = 0+255+255 = 510 → **0**. Rows 3 and 4 of the H output are all zeros, for the same reason.

**H at (5,2)** — patch rows 4–6, cols 1–3: bottom row (r6) = 0+0+0 = 0; top row (r4) = 0+255+255 = 510 → **−510**.
**H at (5,3)**: bottom = 0; top (r4, cols 2–4) = 765 → **−765**. **H at (5,4)**: **−765**. **H at (5,5)**: top (r4, cols 4–6) = 510 → **−510**.

**The H output grid:**

```
      +510   +765   +765   +510
         0      0      0      0
         0      0      0      0
      −510   −765   −765   −510
```

Exactly the mirror situation: top and bottom edges found, left and right edges invisible.

### Step 5 — Combine into one edge map

Take the absolute value of each (an edge is an edge, sign just says which way) and add them:

```
   edge strength = |V| + |H|

   |V|                        |H|                       SUM
   510   0   0  510      510  765  765  510      1020  765  765 1020
   765   0   0  765        0    0    0    0       765    0    0  765
   765   0   0  765        0    0    0    0       765    0    0  765
   510   0   0  510      510  765  765  510      1020  765  765 1020
```

### Step 6 — Clip to 0–255 so you can shade it

```
   any value 255 or more  →  255      (all our non-zero values qualify)
   zero                   →  0

      255  255  255  255
      255    0    0  255
      255    0    0  255
      255  255  255  255
```

### Step 7 — Shade both grids and compare

```
   ORIGINAL (6x6)                 EDGE MAP (4x4)
   0 = black, 255 = white         0 = white, 255 = black
                                  (flipped so edges look like pencil)

   ██ ██ ██ ██ ██ ██                 ██ ██ ██ ██
   ██ ░░ ░░ ░░ ░░ ██                 ██       ██
   ██ ░░ ░░ ░░ ░░ ██                 ██       ██
   ██ ░░ ░░ ░░ ░░ ██                 ██ ██ ██ ██
   ██ ░░ ░░ ░░ ░░ ██
   ██ ██ ██ ██ ██ ██              a HOLLOW SQUARE — the outline
   a SOLID white square
```

**Look at what just happened.** You started with a solid filled square. You did nothing but add and subtract. Out came its **outline** — and the flat interior, where nothing changes, went to exactly zero. The filter deleted everything boring and kept everything where something happened.

### Step 8 — The corners are strongest, and that is meaningful

Before clipping, the four corner cells were **1020** while the edge middles were **765**. Corners score higher because a corner is a vertical edge *and* a horizontal edge in the same place, so both filters fire at once.

That matters more than it looks. Corners are rarer and more distinctive than straight edges — a plain line looks like every other plain line, but a corner tells you about shape. This is why the very first automatic feature-finders ever built for computer vision were **corner detectors**.

### Step 9 — Sanity checks

Three checks that catch almost every arithmetic slip:

1. **Flat regions must give 0.** The middle of the square is all 255s. 765 − 765 = 0 ✓. If you get a non-zero number in a flat area, you made an error.
2. **The signs must be opposite on opposite sides.** Left edge positive, right edge negative ✓. Same magnitude too, because the image is symmetric.
3. **Nothing can exceed ±765** for a single filter. 3 pixels × 255 = 765 ✓.

---

## 💻 Hands-On

Four activities: two unplugged, one in a spreadsheet, one back in Teachable Machine. Budget about 70 minutes.

### Activity A — Become a pixel grid (unplugged, 10 min)

You need graph paper and a pencil.

1. Outline an **8 × 8** box (64 squares).
2. In pencil, draw a fat capital **L** that fills most of the box.
3. Now go square by square. If the square is mostly inside your L, write **255**. If it is mostly outside, write **0**. Squares that are half-and-half: write **128**.
4. Cover the drawing with a sheet of paper so only the numbers show. Hand it to someone.
5. Ask them to shade every 255 white, every 0 black, every 128 grey — and tell you what letter it is.

They will get it. That is the whole point: **you just transmitted a picture using nothing but 64 numbers in a known order.** No image file, no camera, no internet. Numbers plus arrangement equals picture.

*What to notice:* the 128s all land on the boundary of your letter. Boundary pixels are the uncertain ones. That is not a flaw in your drawing — real cameras do exactly the same thing, and it is called anti-aliasing.

### Activity B — Zoom until the picture dies (5 min)

1. Take a photo of something with a thin detail — printed text works best.
2. Open it in any picture viewer (Preview on Mac, Photos on Windows, the Scratch paint editor in **Bitmap** mode, whatever you have).
3. Zoom to 100%. Then 400%. Then 1600%. Keep going.
4. Stop when the letters have become coloured blocks.

Write down the answers to these three questions:

- At what zoom level did the text stop being readable?
- Count the blocks across one letter stroke. Is it 1 block? 3? 10?
- If Teachable Machine shrinks this photo to 224 × 224, would that stroke survive?

*This is the single most useful habit in this module.* Before you blame a model for missing a detail, check whether the detail still exists at the size the model actually sees.

### Activity C — Spreadsheet edge finder (25 min)

Google Sheets, Excel, or LibreOffice Calc all work. This is the engine you will use for the mini-project, so get it working now on a small image.

**Step 1 — Type the image.** In cells **B2:G7**, type the 6×6 square from the Worked Example:

```
        B     C     D     E     F     G
   2    0     0     0     0     0     0
   3    0    255   255   255   255    0
   4    0    255   255   255   255    0
   5    0    255   255   255   255    0
   6    0    255   255   255   255    0
   7    0     0     0     0     0     0
```

**Step 2 — Make it look like an image.** Select B2:G7.
- Set the **column width to about 30 pixels** and the **row height to about 30** so the cells are square.
- Format → Conditional formatting → **Colour scale**.
- Set **Minpoint: Number 0 → black** and **Maxpoint: Number 255 → white**.
- Set the font colour to grey so the digits don't distract you.

You should now be looking at a white square on a black background, made of spreadsheet cells. That is a genuine image viewer that you built.

**Step 3 — Build the edge map.** Leave a gap, then in cell **C12** type this formula exactly:

```
=MIN(255, ABS((D2+D3+D4)-(B2+B3+B4)) + ABS((B4+C4+D4)-(B2+C2+D2)))
```

Read it in three parts:
- `(D2+D3+D4)-(B2+B3+B4)` is the **V filter**: right column of the patch minus left column.
- `(B4+C4+D4)-(B2+C2+D2)` is the **H filter**: bottom row minus top row.
- `ABS(...)` throws away the minus signs; `MIN(255, ...)` clips the total at 255.

C12 is the edge value for image pixel **C3** (the top-left pixel that has a full ring of neighbours).

**Step 4 — Fill it out.** Click C12, copy it, then paste into the range **C12:F15**. That is a 4×4 block — exactly the output size we predicted. The spreadsheet shifts every cell reference automatically as you fill.

**Step 5 — Shade the edge map.** Select C12:F15 and apply conditional formatting again, but **flip the colours this time**: Minpoint Number 0 → **white**, Maxpoint Number 255 → **black**. Edges will show up as dark ink on white paper, like a pencil sketch.

**Expected output — check your numbers against these exactly:**

```
   C12:F15 should read

      255   255   255   255
      255     0     0   255
      255     0     0   255
      255   255   255   255
```

and should look like a hollow square. If you get all zeros, your formula is pointing at the wrong cells — check that C12's formula references B2, not B1 or C2.

**Step 6 — Play.** Now change one pixel in the image — set D4 to 0 — and watch the edge map redraw itself instantly. You just poked a hole in the square and the outline of the hole appeared. Change it back.

### Activity D — Make your Module 5 model fail on purpose (20 min)

Open your Teachable Machine model from Module 5 (or retrain a quick two-class one — 20 photos each is plenty for this).

Run these four tests, 5 photos each, and fill in the table. Keep the **object identical** every time; change only the pixels around it.

| # | Test | Prediction correct? (x/5) | Average confidence |
|---|---|---|---|
| 1 | Same background as training (the control) | | |
| 2 | Totally different background (different room) | | |
| 3 | Same background, lights off + phone torch from the side | | |
| 4 | Object held very far from the camera (tiny in frame) | | |

Now write one sentence per row explaining the result **in pixel language**. Some sentence-starters, to force precision:

- Test 2: "Accuracy dropped by ___ because the edges belonging to ___ disappeared and were replaced by edges belonging to ___."
- Test 3: "Every pixel changed value, but edge *differences* should have survived — so if accuracy still dropped, the shadows must have created ___."
- Test 4: "At that distance the object covered about ___ pixels out of 224 across, so details smaller than ___ were averaged away."

*Expected result, so you know if your test worked:* test 1 should be near-perfect, test 2 usually drops hard, test 3 drops a moderate amount (harsh side-lighting creates brand-new shadow edges that were never in training), and test 4 collapses once the object is small enough. If test 2 does *not* drop, congratulations — you already varied your backgrounds well in Module 5.

---

## ✍️ Practice

Six exercises. Show every step of arithmetic — the answer key shows every step too, so you can compare working, not just answers.

---

**1. [Warm-up] Read the grid.**

```
        c1    c2    c3    c4    c5
   r1    0     0     0     0     0
   r2    0   128   200   128     0
   r3    0   200   255   200     0
   r4    0   128   200   128     0
   r5    0     0     0     0     0
```

(a) Which pixel is brightest, and what is its row and column?
(b) How many pixels are pure black?
(c) What is the average brightness of the whole image? Show the sum and the division.
(d) Shade the grid on paper (black / dark grey / grey / light grey / white) and describe in one sentence what the picture is.

*Done looks like:* four answers, with the sum and the division written out for (c), and a shaded 5×5 grid.

---

**2. [Warm-up] Colour by numbers.**

(a) Name the colour of each pixel: (255, 255, 0), (0, 0, 255), (60, 60, 60), (255, 255, 255), (255, 0, 255).
(b) Convert (200, 80, 40) and (40, 80, 200) to grayscale using `(R+G+B)÷3`. What do you notice, and why is that a problem?
(c) How many numbers does a 224 × 224 colour photo contain? Show the multiplication.
(d) How many different colours can one pixel possibly be? Show the multiplication.

*Done looks like:* five colour names, two grayscale numbers plus one sentence about what they reveal, and two multiplications with their results.

---

**3. [Build] Run the vertical filter by hand.**

Here is a 5×5 image — a bright square on a dim background:

```
        c1    c2    c3    c4    c5
   r1   10    10    10    10    10
   r2   10   250   250   250    10
   r3   10   250   250   250    10
   r4   10   250   250   250    10
   r5   10    10    10    10    10
```

Apply the vertical filter `V = [-1 0 +1; -1 0 +1; -1 0 +1]` (right column minus left column).

(a) How big will the output grid be? Say the rule you used.
(b) Compute all nine output values. Show the left-column sum and right-column sum for at least three of them.
(c) Why is the middle column of your output all zeros?
(d) Which output cells are negative, and what does a negative number mean here?

*Done looks like:* a 3×3 grid of nine numbers, working shown for at least three cells, and two written answers.

---

**4. [Build] Shrink an image and count what you lost.**

```
        c1    c2    c3    c4    c5    c6
   r1     0   255     0   255     0   255
   r2   255     0   255     0   255     0
   r3     0     0     0     0     0     0
   r4     0     0   255   255     0     0
   r5   200   200   200   200   200   200
   r6   100   100   100   100   100   100
```

Shrink to 3 × 3 by replacing each 2×2 block with its average.

(a) Compute all nine averages. Show the four numbers going into at least three of the blocks.
(b) The top two rows were a bold checkerboard. What happened to it, and why?
(c) Rows 5 and 6 were two clearly different greys. What happened to them?
(d) Suppose the checkerboard was the only thing telling class A apart from class B. Explain in two sentences why adding 500 more training photos would not fix the model.

*Done looks like:* a 3×3 grid of averages, working shown for three blocks, and three written answers.

---

**5. [Stretch] Blur, and build your own filter.**

**Part 1 — Blur.** The **box blur** filter is a 3×3 grid of all 1s, with the total divided by 9 — in other words, *replace each pixel with the average of itself and its eight neighbours*. Apply it to this image:

```
        c1    c2    c3    c4    c5
   r1     0     0   255   255   255
   r2     0     0   255   255   255
   r3     0     0   255   255   255
   r4     0     0   255   255   255
   r5     0     0   255   255   255
```

(a) Compute the 3×3 output. Show the working for one cell in full.
(b) The original had a sudden jump from 0 to 255. Describe what the jump looks like after blurring, in one sentence.

**Part 2 — Your own filter.** Design a 3×3 filter that responds most strongly to a **diagonal** edge running from top-left to bottom-right. Then test it:

```
   diagonal image (bright below the diagonal)     Ex-3 image (vertical edges)
        c1    c2    c3    c4    c5                    (reuse it exactly)
   r1     0     0     0     0     0
   r2   255     0     0     0     0
   r3   255   255     0     0     0
   r4   255   255   255     0     0
   r5   255   255   255   255     0
```

(c) Write down your filter and explain in one sentence why its weights are arranged that way.
(d) Compute your filter's output at the centre position (3,3) of the diagonal image, and the vertical filter's output at the same position. Which is bigger?
(e) Compute your filter's output at position (3,2) of the **Exercise 3** image, and compare to the vertical filter's answer there (you already computed it). What does the comparison show?

*Done looks like:* a 3×3 blur output with one cell's full working, your filter drawn as a grid, four computed numbers, and a sentence for (b), (c) and (e).

---

**6. [Stretch] Prove that edges beat brightness under changing light.**

Start from the Exercise 3 image (background 10, square 250). You already know the vertical filter's answer at position (3,2) is **+720**.

(a) **Dim the room.** Multiply every pixel by 0.4 and round to whole numbers. Write the new 5×5 image, then recompute V at (3,2). What is the ratio of the new answer to 720?
(b) **Turn on a lamp that adds light evenly.** Go back to the original image and add 50 to every pixel. Recompute V at (3,2). What happened?
(c) Explain (b) using the filter's nine weights. What do they add up to, and why does that guarantee your answer?
(d) A friend proposes a much simpler feature: "just use the average brightness of the photo — dark objects will have a low average." Compute the average brightness of the original image and of the +50 image, and use the two numbers to explain why their feature is worse than yours.
(e) Connect it back: in Activity D you tested your Teachable Machine model in the dark with a side torch, and accuracy still dropped even though edges are supposed to survive lighting changes. Give one specific reason why, in pixel language.

*Done looks like:* two recomputed filter values, the ratio, two average-brightness numbers, and three written explanations.

---

## 🤔 Think Deeper

**1. Your eye does not send 12 million numbers to your brain.**
A camera records every pixel with equal care. Your eye does not: the centre of your vision is packed with detectors and the edges are sparse, your eye jumps around three times a second, and a big chunk of the processing happens in the retina before anything reaches your brain. Is a camera's "record everything evenly" approach better or worse than your eye's approach — and better or worse *for what*?

*How to reason about it:* separate the goals. For **evidence** (a court photo, a medical scan) you want faithful, even recording with no interpretation. For **acting fast in the world** you want the opposite: throw away 99% of it and get the important 1% to the decision-maker in 50 milliseconds. Ask which job the system has before you judge its design. Then ask a harder question: does the camera's evenness make it *unbiased*, or does it just move the bias somewhere else — into the lens, the exposure setting, the person choosing where to point it?

**2. If a filter is blind to overall brightness, why do vision systems still fail in the dark?**
You proved in section 5 that adding light equally changes nothing. Yet phone cameras and vision models genuinely struggle at night. Something in the proof does not match reality. What?

*How to reason about it:* three candidates worth thinking through. (i) Real lighting is not "add 50 to everything" — a lamp on the left brightens the left more than the right, which creates *brand-new edges that are not object edges*. (ii) Pixels cannot go below 0 or above 255, so in a very dark or very blown-out photo, thousands of pixels get squashed to the same value and the difference between object and background genuinely disappears. (iii) Dark photos are grainy, and grain is random pixel-to-pixel change — which is exactly what an edge detector is built to notice. Try to decide which of these three would show up in *your* Activity D results, and how you would tell them apart with a test.

**3. Who is responsible when a vision system fails on some people more than others?**
Cameras have exposure settings, and those settings were tuned by people making choices about which skin tones should look "correct". Automatic soap dispensers using infrared reflection have been documented failing to detect darker-skinned hands. A face-analysis study found error rates near 1% for one group and over 30% for another. These are pixel-level problems long before they are model-level problems. So who should have caught it — the camera engineer, the person who assembled the training photos, the company that shipped it, or the customer who bought it?

*How to reason about it:* try tracing the failure backwards through the chain — output, model, training data, camera, sensor, physics of light — and mark the earliest point where someone could have run a cheap test that would have caught it. Then ask a separate question, which is not the same one: who had the *power* to fix it and who had the *incentive*? You get to a full answer in Module 9, so hold your notes.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Thinking 0 is white and 255 is black | It feels like "more ink = higher number", the way it works with printers | Say it out loud: it is **light**, not ink. More light = higher number. 255 = brightest. Write "0 = BLACK" at the top of your page |
| Making the output grid the same size as the input | You forget that a 3×3 filter cannot sit on the edge row — it has no neighbours out there | **Output = input − 2** for a 3×3 filter. Compute the output size *before* you start, and count that many cells |
| Mixing up rows and columns in the filter | `-1 0 +1` looks the same whether you read it across or down | Write the filter in words before computing: "right column minus left column". Words don't rotate |
| Forgetting the absolute value, then shading a negative | The edge on one side comes out −765 and you shade it as "very dark" instead of "very strong edge" | An edge is an edge. Take `|value|` before shading. Keep the sign only if you care *which way* the brightness went |
| Averaging RGB and expecting to get the colour back | Grayscale looks like "the same image, just grey" | Three numbers became one — it is a one-way door. (200,80,40) and (107,107,107) both give 107 |
| Blaming the model for missing a detail the resizing already deleted | You are looking at your full-size photo; the model saw a 224×224 version | Shrink the photo yourself to 224×224 and look at it. If *you* cannot see the detail, the model definitely cannot |
| Assuming a zero output means "no image here" | Zero looks like "nothing" | Zero means **no change** here — a perfectly flat region. A pure white wall and a pure black wall both give zero |
| Testing your model in exactly one background and calling it done | It is the fastest way to get a good-looking number | Module 6's rule, in pixel form: change the background before you trust the score |

---

## 🛠️ Mini-Project — Pixel Lab

**Time:** 60–90 minutes · **You need:** graph paper, pencil, a spreadsheet

### 🎯 Goal

Draw a letter by hand as a grid of numbers, feed it through an edge filter you built yourself, and produce two shaded grids side by side: the solid letter, and its outline — with a written explanation of exactly where one output number came from.

### 📋 Starter steps

**Step 1 — Draw the letter on graph paper (15 min).**

Outline a **12 × 12** box. Choose a capital letter with both vertical and horizontal strokes — **T**, **L**, **E**, **F** and **H** all work well. **O** and **S** are harder (curves need lots of 128s); **I** is too easy.

Draw your letter thick — at least 2 squares wide for every stroke — and leave a blank border of at least 1 square all the way round. Then fill in every square: **255** inside the letter, **0** outside.

Here is a worked reference so you can check your grid looks sensible. This is a **T** (`#` means 255, `.` means 0):

```
      col:  1  2  3  4  5  6  7  8  9 10 11 12
   r1       .  .  .  .  .  .  .  .  .  .  .  .
   r2       .  .  .  .  .  .  .  .  .  .  .  .
   r3       .  .  #  #  #  #  #  #  #  #  .  .
   r4       .  .  #  #  #  #  #  #  #  #  .  .
   r5       .  .  .  .  .  #  #  .  .  .  .  .
   r6       .  .  .  .  .  #  #  .  .  .  .  .
   r7       .  .  .  .  .  #  #  .  .  .  .  .
   r8       .  .  .  .  .  #  #  .  .  .  .  .
   r9       .  .  .  .  .  #  #  .  .  .  .  .
   r10      .  .  .  .  .  #  #  .  .  .  .  .
   r11      .  .  .  .  .  .  .  .  .  .  .  .
   r12      .  .  .  .  .  .  .  .  .  .  .  .
```

Count your bright pixels before you move on — for this T it is (2 rows × 8) + (6 rows × 2) = 16 + 12 = **28 bright pixels out of 144**.

**Step 2 — Type it into the spreadsheet (10 min).**

Put your grid in **B2:M13** — 12 columns (B through M) and 12 rows (2 through 13). Type 0 or 255 in every one of the 144 cells. It is tedious. Do it anyway; you will never again wonder what "an image is a grid of numbers" means.

*Speed tip:* type one full row, then copy-paste rows that repeat. The T above has six identical stem rows.

**Step 3 — Make it look like an image (5 min).**

- Select B2:M13. Set column width ≈ 25 pixels, row height ≈ 25, so the cells are square.
- Conditional formatting → Colour scale → Minpoint **Number 0 → black**, Maxpoint **Number 255 → white**.
- Set the font colour to a mid grey so the digits fade into the background.

Your letter should now be legible on screen. **If it is not, fix the numbers before continuing** — a wrong image gives a wrong edge map and you will hunt the bug in the wrong place.

**Step 4 — Build the edge map (10 min).**

In cell **C18**, type exactly:

```
=MIN(255, ABS((D2+D3+D4)-(B2+B3+B4)) + ABS((B4+C4+D4)-(B2+C2+D2)))
```

Then copy C18 and paste into **C18:L27**. That is a 10 × 10 block (12 − 2 = 10, as predicted).

The output grid sits 16 rows below the input, so output cell C18 corresponds to input pixel C3, D18 ↔ D3, C19 ↔ C4, and so on. Leave row 17 and row 28, and columns B and M of the output, blank or zero — those are the border pixels that have no full ring of neighbours.

**Step 5 — Shade the edge map with the colours flipped (5 min).**

Select C18:L27. Conditional formatting → Colour scale → Minpoint **Number 0 → white**, Maxpoint **Number 255 → black**.

Flat areas (inside the stroke, and out in the background) go white. Edges go black. **You should be looking at the hollow outline of your letter.**

**Step 6 — Explain one cell's arithmetic in writing (10 min).**

Pick **one** output cell that came out at 255, sitting on the left edge of a stroke. Write out, longhand:

1. Which output cell you picked, and which input pixel it corresponds to.
2. The nine input pixel values in its 3×3 patch, drawn as a small grid.
3. The V calculation: right column sum − left column sum = ?
4. The H calculation: bottom row sum − top row sum = ?
5. `|V| + |H|` = ?, and then the clipped result.
6. One sentence: what does that number tell you about that spot in the image?

**Step 7 — Two experiments (15 min).**

*Experiment 1 — Turn the lights on.* Add 40 to every pixel of your image (background becomes 40, letter becomes 255 — or use 215 for the letter so nothing overflows past 255). Fastest way: type your image into a fresh block and add 40, or temporarily change the 0s to 40s. **Predict first**, then check: does the edge map change?

*Experiment 2 — Add a background.* Change ten random background pixels from 0 to 255, scattered around outside the letter — this is your "wood-grain table". **Predict first**, then check: what does the edge map look like now, and would a machine still find your letter easily?

Write one sentence of prediction and one sentence of result for each.

### ✅ Success criteria checklist

- [ ] A 12 × 12 hand-drawn letter on graph paper, every square filled with 0 or 255
- [ ] All 144 numbers typed into the spreadsheet at B2:M13
- [ ] The input grid shaded so the letter is clearly readable on screen
- [ ] A 10 × 10 edge map at C18:L27, computed by formula (not typed in by hand)
- [ ] The edge map shaded with flipped colours, showing a recognisable **hollow outline**
- [ ] The two shaded grids photographed or screenshotted **side by side**
- [ ] A written explanation of one output cell with all six parts from Step 6
- [ ] Both experiments run, each with a written prediction and a written result
- [ ] One sentence: name a feature of your letter the edge map **kept**, and one it **threw away**

### 🚀 Level it up

Pick one:

- **Split V and H into two maps.** Build a second output block that shows `|V|` alone, and a third that shows `|H|` alone. Shade all three. Now you can point at your letter and say "these strokes are vertical, these are horizontal" — and for a T, the V-map and H-map will look startlingly different. This is the first real step toward how a machine describes a shape.
- **Build a letter classifier with three numbers.** Do the whole Pixel Lab for three different letters. For each, record just three numbers: total bright pixels, total `|V|` edge strength, total `|H|` edge strength (use `=SUM()` on each block). Put the three letters in a small table. Can you write an if-then rule — Module 3 style — that tells them apart using only those three numbers? You have just hand-built a feature extractor and a classifier, with no machine learning at all.

---

## 🔑 Key Takeaways

- **An image is numbers plus arrangement.** One number per pixel for grayscale (0 = black, 255 = white); three stacked grids — red, green, blue — for colour. Nothing else is stored.
- **A 224 × 224 colour photo is 150,528 numbers, and that is already 1/243rd of what your phone captured.** Detail is deleted before the model ever runs, and it never comes back.
- **A filter is a small grid you slide over the image**, multiplying and adding as you go. Output size = input size − 2 for a 3×3 filter. Flat regions produce zero.
- **Edges are the first useful feature because they are differences, and differences survive lighting changes.** A filter whose nine weights sum to zero is mathematically blind to how bright the room is.
- **A vertical filter only sees vertical edges.** You need at least two orientations before you can trace a shape, and where both fire at once, you have found a corner.
- **The filter reports every edge, including your background's.** If your background is more consistent than your object, you trained a background detector and gave it your object's name.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Pixel** | One tiny square of a picture — the smallest piece a computer stores | A 5 × 5 image has 25 pixels |
| **Grayscale** | A black-and-white image where each pixel is a single brightness number | 0 = black, 128 = grey, 255 = white |
| **RGB** | Storing colour as three numbers per pixel: red, green, blue amounts | (255, 255, 0) = yellow, because red + green light makes yellow |
| **Channel** | One of the three stacked grids in a colour image | The "red channel" is the whole grid of just the R numbers |
| **Resolution** | How many pixels an image has, written width × height | 224 × 224 = 50,176 pixels |
| **Megapixel** | One million pixels | A 12-megapixel camera makes images of about 12,000,000 pixels |
| **Downsampling** | Shrinking an image by averaging blocks of pixels into one | Four pixels 255, 0, 0, 255 average to 127.5 |
| **Filter (kernel)** | A small grid of numbers you slide over an image to highlight one thing | `-1 0 +1` in three rows highlights vertical edges |
| **Edge** | A place in the image where brightness suddenly changes | The border between a dark comb and a white table |
| **Edge map** | The new grid you get after running an edge filter — an outline drawing | The hollow square in the Worked Example |
| **Absolute value** | A number with its minus sign removed | `|−765| = 765` |
| **Clipping** | Forcing numbers back into the 0–255 range so you can display them | 1020 clipped at 255 becomes 255 |
| **Anti-aliasing** | The grey in-between pixels a camera puts along a boundary | The 128s along the edge of your hand-drawn letter |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

---

### Exercise 1 — Read the grid

**(a) Brightest pixel.** 255, at **row 3, column 3** — the exact centre.

**(b) Pure black pixels.** Count them row by row:

```
   r1:  0 0 0 0 0                   → 5 zeros
   r2:  0 128 200 128 0             → 2 zeros (c1, c5)
   r3:  0 200 255 200 0             → 2 zeros (c1, c5)
   r4:  0 128 200 128 0             → 2 zeros (c1, c5)
   r5:  0 0 0 0 0                   → 5 zeros
                                      ─────────
                                      16 zeros
```

**16 pixels are pure black.**

**(c) Average brightness.**

```
   row 1 sum = 0
   row 2 sum = 0 + 128 + 200 + 128 + 0 = 456
   row 3 sum = 0 + 200 + 255 + 200 + 0 = 655
   row 4 sum = 0 + 128 + 200 + 128 + 0 = 456
   row 5 sum = 0
   ─────────────────────────────────────────
   total     = 456 + 655 + 456 = 1567

   pixels    = 5 × 5 = 25

   average   = 1567 ÷ 25 = 62.68
```

**Average brightness = 62.68**, which is a dark grey. Worth noticing: even though the picture *feels* like a bright blob, most of it is black, so the average is low. Average brightness is a poor description of a picture.

**(d) Shaded.**

```
   ██ ██ ██ ██ ██        ██ = 0     black
   ██ ▓▓ ▒▒ ▓▓ ██        ▓▓ = 128   grey
   ██ ▒▒ ░░ ▒▒ ██        ▒▒ = 200   light grey
   ██ ▓▓ ▒▒ ▓▓ ██        ░░ = 255   white
   ██ ██ ██ ██ ██
```

**One sentence:** it is a soft glowing dot — brightest at the centre and fading smoothly outward to black, like a small lamp seen in a dark room.

---

### Exercise 2 — Colour by numbers

**(a) Colour names.**

| RGB | Colour | Reasoning |
|---|---|---|
| (255, 255, 0) | **yellow** | red + green at full, no blue |
| (0, 0, 255) | **blue** | only the blue light is on |
| (60, 60, 60) | **dark grey** | all three equal → grey; 60 is low → dark |
| (255, 255, 255) | **white** | all three at full |
| (255, 0, 255) | **magenta** (hot pink / purple-pink) | red + blue, no green |

**(b) Grayscale conversions.**

```
   (200, 80, 40):   (200 + 80 + 40) ÷ 3 = 320 ÷ 3 = 106.67  →  107
   (40, 80, 200):   (40 + 80 + 200) ÷ 3 = 320 ÷ 3 = 106.67  →  107
```

**What I notice:** they give **exactly the same grey**, 107 — even though one is a warm orange-brown and the other is a cool blue. The two colours are opposites to a human eye and identical after conversion.

**Why that is a problem:** once you convert to grayscale, no model on Earth can tell those two pixels apart, because there is nothing left to tell apart. If your classes differ only by colour — a red apple versus a green apple, a blue team shirt versus an orange one — converting to grayscale destroys the only useful feature. It is a one-way door, so you must decide *before* you walk through it.

**(c) Numbers in a 224 × 224 colour photo.**

```
   224 × 224 = 50,176 pixels
   50,176 × 3 channels = 150,528 numbers
```

**(d) Possible colours for one pixel.**

```
   256 × 256 × 256 = 16,777,216
```

Each channel has 256 possible values (0 through 255 inclusive — note it is 256, not 255, because zero counts). About **16.7 million colours**.

---

### Exercise 3 — Run the vertical filter by hand

**(a) Output size.**

`output = input − 2` for a 3×3 filter, because the filter needs a full ring of neighbours and cannot be centred on the outermost row or column. So 5 − 2 = **3 × 3, nine values**. The output cell (r, c) is centred on input pixel (r, c), so r and c each run from **2 to 4**.

**(b) All nine values.**

*Cell (2,2)* — patch = rows 1–3, cols 1–3:

```
      10    10    10
      10   250   250
      10   250   250

   right column (col 3) =  10 + 250 + 250 = 510
   left  column (col 1) =  10 +  10 +  10 =  30
   V(2,2) = 510 − 30 = +480
```

*Cell (2,3)* — patch = rows 1–3, cols 2–4:

```
      10    10    10
     250   250   250
     250   250   250

   right column (col 4) =  10 + 250 + 250 = 510
   left  column (col 2) =  10 + 250 + 250 = 510
   V(2,3) = 510 − 510 = 0
```

*Cell (2,4)* — patch = rows 1–3, cols 3–5: right col 5 = 10+10+10 = 30; left col 3 = 10+250+250 = 510 → **−480**.

*Cell (3,2)* — patch = rows 2–4, cols 1–3:

```
      10   250   250
      10   250   250
      10   250   250

   right column (col 3) = 250 + 250 + 250 = 750
   left  column (col 1) =  10 +  10 +  10 =  30
   V(3,2) = 750 − 30 = +720
```

*Cell (3,3)*: left col 2 = 750, right col 4 = 750 → **0**.
*Cell (3,4)*: left col 3 = 750, right col 5 = 30 → **−720**.
*Cell (4,2)* — patch rows 3–5, cols 1–3: right col 3 = 250+250+10 = 510, left col 1 = 30 → **+480**.
*Cell (4,3)*: left col 2 = 250+250+10 = 510, right col 4 = 510 → **0**.
*Cell (4,4)*: left col 3 = 510, right col 5 = 30 → **−480**.

**The output grid:**

```
      +480     0   −480
      +720     0   −720
      +480     0   −480
```

**(c) Why the middle column is all zeros.**

The middle output column sits over the middle of the bright square. Three columns to the left of it and three to the right are all identical (250s in the middle rows, 10s at top and bottom), so the left-column sum and right-column sum are equal and cancel exactly. **Zero means "nothing changes here"** — a flat region — not "nothing is here". A solid bright square and a solid dark square both produce zero in their interiors.

**(d) Negative cells.**

The whole right-hand output column: (2,4) = −480, (3,4) = −720, (4,4) = −480.

A negative value means the brightness went **bright → dark** as you move left to right — the *right-hand* edge of the square, where the bright square gives way to the dim background. Positive means dark → bright, the left-hand edge. The magnitude tells you how strong the edge is; the sign tells you which direction the change goes. If you only care *that* there is an edge, take the absolute value and both sides become 480 / 720 / 480 — symmetrical, as they should be for a symmetrical picture.

---

### Exercise 4 — Shrink an image and count what you lost

**(a) The nine block averages.**

*Block (1,1)* — rows 1–2, cols 1–2:

```
       0   255
     255     0        sum = 0 + 255 + 255 + 0 = 510
                      510 ÷ 4 = 127.5
```

*Block (1,2)* — rows 1–2, cols 3–4: values 0, 255, 255, 0 → 510 ÷ 4 = **127.5**
*Block (1,3)* — rows 1–2, cols 5–6: values 0, 255, 255, 0 → 510 ÷ 4 = **127.5**

*Block (2,1)* — rows 3–4, cols 1–2:

```
       0     0
       0     0        sum = 0,  0 ÷ 4 = 0
```

*Block (2,2)* — rows 3–4, cols 3–4:

```
       0     0
     255   255        sum = 510,  510 ÷ 4 = 127.5
```

*Block (2,3)* — rows 3–4, cols 5–6: all zeros → **0**

*Block (3,1)* — rows 5–6, cols 1–2:

```
     200   200
     100   100        sum = 600,  600 ÷ 4 = 150
```

*Block (3,2)* and *Block (3,3)*: identical values → **150** each.

**The 3 × 3 result** (rounding the halves up):

```
      128   128   128
        0   128     0
      150   150   150
```

**(b) What happened to the checkerboard.**

It is **completely gone**. Every 2×2 block of a checkerboard contains exactly two 255s and two 0s, so every block averages to the same 127.5. Three different-looking blocks all became one identical grey. The pattern did not fade — it was **erased**, and no amount of processing afterwards can recover it, because all three output numbers are the same and carry no information about what was underneath.

**(c) What happened to rows 5 and 6.**

Row 5 was uniformly 200 (light grey) and row 6 was uniformly 100 (dark grey) — a clear horizontal edge between them. Averaging pairs them up: (200 + 200 + 100 + 100) ÷ 4 = 150. **The edge between them vanished** and both rows became one flat band of 150. Two distinct greys merged into one.

**(d) Why 500 more photos would not fix it.**

Because the problem is not that the model lacks examples — it is that **the information no longer exists in the examples**. After shrinking, class A's photos and class B's photos contain literally the same numbers (128, 128, 128) in that region, so there is nothing for the model to learn from. Adding 500 more photos just adds 500 more copies of identical grey.

The fixes are all about the *pixels*, not the count: train at a higher resolution so the checkerboard survives; crop in tighter on the pattern so it occupies more pixels before shrinking; or find a different feature that does survive resizing. **A model can only learn a difference that is still in the data by the time it arrives.**

---

### Exercise 5 — Blur, and build your own filter

**Part 1 (a) — Box blur output.**

Output size = 5 − 2 = 3 × 3, centred on positions (2,2) through (4,4).

*Full working for cell (2,2)* — patch = rows 1–3, cols 1–3:

```
       0     0   255
       0     0   255
       0     0   255

   sum = (0 + 0 + 255) + (0 + 0 + 255) + (0 + 0 + 255)
       = 255 + 255 + 255
       = 765

   765 ÷ 9 = 85
```

*Cell (2,3)* — patch = rows 1–3, cols 2–4: each row is 0, 255, 255 = 510; three rows = 1530; 1530 ÷ 9 = **170**.

*Cell (2,4)* — patch = rows 1–3, cols 3–5: each row is 255, 255, 255 = 765; three rows = 2295; 2295 ÷ 9 = **255**.

Rows 3 and 4 of the output are identical to row 2, because image rows 1 through 5 are all the same.

**Output:**

```
       85   170   255
       85   170   255
       85   170   255
```

**(b) What the jump looks like now.**

The original had a **cliff** — 0 right next to 255, with nothing in between. After blurring it is a **ramp**: 85, then 170, then 255, climbing in three even steps of 85. The edge is still there but it is now smeared across three pixels instead of happening at one boundary, so any edge detector run afterwards will report a weaker, wider edge in three places rather than a sharp one in a single place.

*Bonus check:* blur weights are nine 1s divided by 9, which sum to **1**, not 0. That is why blur preserves overall brightness (a flat region of 255 stays 255) while the edge filters, summing to 0, delete it.

**Part 2 (c) — My diagonal filter.**

```
       0   +1   +1
      -1    0   +1
      -1   -1    0
```

**Why arranged this way:** the weights are positive in the **upper-right** triangle and negative in the **lower-left** triangle, with zeros along the top-left-to-bottom-right diagonal itself. In words: *upper-right region minus lower-left region.* So it gives a big answer when the two sides of that diagonal line differ in brightness — which is exactly what a diagonal edge running top-left to bottom-right is. The zeros sit on the diagonal because pixels sitting *on* an edge shouldn't vote for either side. And the weights sum to 0 + 1 + 1 − 1 + 0 + 1 − 1 − 1 + 0 = **0**, so like the other edge filters it ignores overall brightness. Good.

**(d) At centre (3,3) of the diagonal image.** Patch = rows 2–4, cols 2–4:

```
   patch values:              weights:            products:
       0     0     0            0   +1   +1        0     0     0
     255     0     0           -1    0   +1     −255     0     0
     255   255     0           -1   -1    0     −255  −255     0

   sum = 0 + 0 + 0 − 255 + 0 + 0 − 255 − 255 + 0 = −765
```

**My diagonal filter gives −765.**

Now the vertical filter on the very same patch. Take the columns carefully: col 2 of the patch is (r2c2, r3c2, r4c2) = (0, 255, 255) and col 4 is (r2c4, r3c4, r4c4) = (0, 0, 0).

```
   right column (col 4) =   0 +   0 +   0 =   0
   left  column (col 2) =   0 + 255 + 255 = 510
   V(3,3) = 0 − 510 = −510
```

**Which is bigger?** By magnitude, **the diagonal filter wins: 765 versus 510.** Both detect *something* (a diagonal edge does contain some left-right change), but the filter whose shape matches the edge's shape gives the stronger answer.

**(e) At position (3,2) of the Exercise 3 image.** Patch = rows 2–4, cols 1–3:

```
   patch values:                weights:           products:
      10   250   250              0   +1   +1        0   +250   +250
      10   250   250             -1    0   +1      −10      0   +250
      10   250   250             -1   -1    0      −10   −250      0

   sum = 0 + 250 + 250 − 10 + 0 + 250 − 10 − 250 + 0
       = (250 + 250 + 250) − (10 + 10 + 250)
       = 750 − 270
       = +480
```

The vertical filter at the same spot gave **+720** (computed in Exercise 3).

**What the comparison shows.** Line the four numbers up:

| | on the **diagonal** edge | on the **vertical** edge |
|---|---:|---:|
| diagonal filter | **765** | 480 |
| vertical filter | 510 | **720** |

Each filter gives its strongest response to the edge whose orientation matches its own, and a weaker (but non-zero) response to the other. That is the whole basis of how a vision system works out *which way a line is pointing*: run several filters at different orientations over the same spot and see which one shouts loudest. One filter tells you an edge is present; a **set** of filters tells you its angle. And an angle is the beginning of a shape.

---

### Exercise 6 — Prove that edges beat brightness under changing light

**(a) Dim the room — multiply everything by 0.4.**

```
   10  × 0.4 = 4
   250 × 0.4 = 100
```

The new image:

```
        c1    c2    c3    c4    c5
   r1     4     4     4     4     4
   r2     4   100   100   100     4
   r3     4   100   100   100     4
   r4     4   100   100   100     4
   r5     4     4     4     4     4
```

Recompute V at (3,2) — patch = rows 2–4, cols 1–3:

```
   right column (col 3) = 100 + 100 + 100 = 300
   left  column (col 1) =   4 +   4 +   4 =  12
   V(3,2) = 300 − 12 = +288
```

**Ratio:** 288 ÷ 720 = **0.4** — exactly the factor we dimmed by.

So multiplying the light multiplies the edge strength by the same amount. The edge did **not** disappear, and crucially the *pattern* of the output is unchanged: every cell in the output grid shrank by the same factor of 0.4, so if you divide the whole output by its own maximum, you get the identical picture back. Edges are stretched by multiplicative lighting, not scrambled.

**(b) Add 50 to every pixel.**

```
   10  + 50 = 60
   250 + 50 = 300   ← but pixels cap at 255!
```

Two honest answers here. Doing the pure arithmetic (letting 300 exist):

```
   right column (col 3) = 300 + 300 + 300 = 900
   left  column (col 1) =  60 +  60 +  60 = 180
   V(3,2) = 900 − 180 = +720
```

**Exactly 720 — completely unchanged from the original.**

And doing it *realistically*, where 300 gets clipped down to 255:

```
   right column = 255 + 255 + 255 = 765
   left  column =  60 +  60 +  60 = 180
   V(3,2) = 765 − 180 = +585
```

That is **not** unchanged — it dropped from 720 to 585. The mathematical guarantee is real, but only while the numbers stay inside 0–255. Both answers earn full marks if you say which one you computed and why.

**(c) Why the pure version is guaranteed.**

Add up the vertical filter's nine weights:

```
   (-1) + 0 + (+1)  =  0
   (-1) + 0 + (+1)  =  0
   (-1) + 0 + (+1)  =  0
   ──────────────────────
   total            =  0
```

If you add the same number *k* to all nine pixels in the patch, the filter's answer changes by exactly `k × (sum of weights)` = `k × 0` = **0**. So a uniform brightness shift is invisible to any filter whose weights sum to zero. That is not an accident of this example — it is a property of the filter, true for every image, and it is precisely why edge filters are designed with zero-sum weights.

The catch, which (b) exposed: real pixels cannot go above 255 or below 0. Once bright areas hit the ceiling, the "add the same number to everything" assumption breaks, and the guarantee breaks with it. **Every clean mathematical promise in this field has a boundary condition, and finding it is your job.**

**(d) Average brightness as a feature.**

First count the pixels. A 5×5 grid has 25 pixels. The bright square is the inner 3×3 = **9 pixels** at 250. The dark border is everything else: 25 − 9 = **16 pixels** at 10. (Check it the other way: top row 5 + bottom row 5 + 3 left-side + 3 right-side = 16 ✓.)

```
   original total   = (16 × 10) + (9 × 250) = 160 + 2250 = 2410
   original average = 2410 ÷ 25 = 96.4

   +50 image total  = (16 × 60) + (9 × 300) = 960 + 2700 = 3660
   +50 image average= 3660 ÷ 25 = 146.4
```

**Why the friend's feature is worse.** The two images contain the **same object in the same place** — nothing about the scene changed except the room lighting. Yet their average brightness went from 96.4 to 146.4, a jump of exactly 50. Meanwhile the edge filter gave 720 both times.

So a model trained on average brightness would treat these as two very different inputs and could easily assign them different classes, purely because somebody flicked a light switch. A model using edges sees them as identical, which they are, in every way that matters. **A good feature changes when the thing changes and holds still when the thing holds still.** Average brightness fails that test; edge strength passes it.

(Worth adding: average brightness also fails the *other* way. A black square on a white background and a white square on a black background can have similar averages while being visually opposite.)

**(e) Why the torch test still hurt the model.**

Any one of these is a correct, specific answer:

- **A side torch does not add light evenly.** The pixels facing the torch gain a lot; the pixels facing away gain nothing. That is not "add 50 to everything", so the zero-sum guarantee does not apply — the left side of every object got brighter than the right, which shifts every edge value in the image.
- **New shadow edges appeared that are not object edges.** Harsh side lighting throws a hard-edged shadow onto the table. That shadow boundary is a genuine, strong, high-contrast edge in the pixels, and the model has no way to know it belongs to the lighting rather than the object. The model is now looking at an object *plus a fake object made of darkness*.
- **Clipping at both ends.** The torch-facing side blows out to 255 and the shadow side crushes to 0. In both regions many different true brightnesses become the same stored number, so real edges inside those regions disappear entirely — exactly the ceiling problem from part (b).
- **Grain.** Dark photos are noisy: a phone camera boosts its sensitivity in low light and individual pixels start jumping around randomly by ±20 or more. An edge detector cannot tell random pixel-to-pixel jumps from real ones, so the whole edge map fills with speckle that was never in the training photos.

The takeaway for your own work: "edges survive lighting" is true for the *idealised* lighting change and a useful thing to know — but real lighting changes are directional, they clip, and they add noise. Which is why the fix is never clever maths. **The fix is to photograph your training examples under the lighting conditions you actually expect to meet.**

---

</details>

---

[⬅ Previous](module-06-train-test-trust.md) · [Level 1 Home](README.md) · [Next ➡](module-08-how-computers-read-and-chat.md)

*Next up: you have taken a picture apart into numbers. Words are harder — there is no obvious "brightness" of the word "pizza". Module 8 shows you the trick every chatbot uses, and you will build one with a tally sheet and a bag of paper slips before you ever touch a neural network.*

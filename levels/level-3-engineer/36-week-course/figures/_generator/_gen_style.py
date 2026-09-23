"""Generate STYLE.md for Level 3. STYLE.md is OUTPUT; edit this file, then re-run."""
import os
from _gen_core import MOTIFS
from _gen_pat import PATTERNS, EXAMPLES
from _gen_emit import pattern_svg, NEW, OLD, HERE, GROUPS


def dims(vb):
    _, _, w, h = vb.split()
    return "%s&times;%s" % (w, h)


def motif_block(m):
    return ("### `%s` &mdash; %s\n\nviewBox `%s` (%s). %s\n\n**Use it for:** %s\n\n"
            "```svg\n<g transform=\"translate(0,0)\">\n%s\n</g>\n```\n"
            % (m["id"], m["title"], m["vb"], dims(m["vb"]), m["desc"], m["note"], m["body"]))


def pattern_block(p):
    return ("### `%s` &mdash; %s\n\n**Canvas** `%s`. %s\n\n```svg\n%s\n```\n"
            % (p["id"], p["title"], p["vb"], p["note"], pattern_svg(p)))


def grouped_motif_blocks():
    out = []
    by_id = {m["id"]: m for m in MOTIFS}
    for gname, ids in GROUPS:
        out.append("### %s\n" % gname)
        out.append("\n".join("#" + motif_block(by_id[i]) for i in ids))
    return "\n".join(out)


DOC = r"""# Figure style system &mdash; AI Academy, Level 3 &ldquo;Engineer&rdquo; (36-week course)

**Audience: the authors drawing the SVG figures for Level 3.**
This file is the contract. If your figure disagrees with this file, this file wins.

**Level 3 is a faithful extension of Level 2, which was a faithful extension of Level 1.** A parent
flipping between the three years should not be able to tell where one ends and the next begins. Same
palette, same stroke widths, same type scale, same accessibility rules. Everything inherited is
copied out in full below, with the actual values, so **this file stands alone** &mdash; you never
need to open Level 1's or Level 2's `STYLE.md` to draw a Level 3 figure.

What is genuinely new is the *subject matter*. Level 3 has **maths, tensors and measurement** on the
screen: slopes, a loss surface, matrix shapes, backpropagation, a confusion matrix, an ROC curve, a
convolution. So there are new motifs for all of those, and the one rule that matters more than any
other has grown a second half &mdash; **&sect;3: a figure is not a picture of code, and it is not a
picture of a formula either.**

**The learner is one 14-year-old who finished Levels 1 and 2. They can write Python and have trained
scikit-learn models, but they have never seen calculus, linear-algebra notation or the inside of a
neural network. The teacher knows neither AI nor Python nor calculus, and opened this week's file 20
minutes ago.** A figure has to land in about four seconds with no caption, and it has to teach the
adult as well as the child. That is the bar, and it is harder than Level 2's bar.

---

## 0. The 30-second version

1. Copy a **composition pattern** (&sect;6) that matches your diagram type.
2. Drop in **motifs** (&sect;4, &sect;5) &mdash; do not redraw the confusion matrix.
3. Use only the eight **palette** colours (&sect;1.1), by *role*, never by taste.
4. **Do not draw the code, and do not draw the formula.** Draw what the formula does to numbers (&sect;3).
5. **Print the arithmetic.** If your figure claims a number, show the sum that produced it (&sect;2.1).
6. Start every file with `role="img"`, then `<title>`, then `<desc>` (&sect;1.5).
7. Name it `fig-wNN-<n>-<slug>.svg` (&sect;7).
8. Run the pre-flight check (&sect;9) before you commit. It must print `--- 0 finding(s)`.

---

## 1. Inherited verbatim from Levels 1 and 2

Nothing in this section may be changed. The values are reproduced, not summarised.

### 1.1 Palette &mdash; eight colours, used by role

Each role has a **stroke** (outlines, text, marks) and most have a **fill** (the pale tint inside a
shape). This two-tier split is deliberate and load-bearing &mdash; see &sect;1.2.

| Role | Stroke | Fill | Contrast on white | Greyscale (stroke) | Greyscale (fill) | Use it for |
|---|---|---|---|---|---|---|
| **data** | `#1F6FB2` | `#D9EAF9` | 5.28:1 | 108 | **232** | Data, values, tables, arrays, tensors, activations, inputs, anything measured |
| **model** | `#6D28D9` | `#DBCEF3` | 7.10:1 | 88 | **212** | The model: weights, biases, layers, kernels, the fitted estimator |
| **human** | `#845F00` | `#E8C671` | 5.80:1 | 101 | **202** | People, choices a person made, notes, the validation set, model-card entries |
| **correct** | `#1B7A4B` | `#E2F7ED` | 5.34:1 | 107 | **242** | It ran, it passed, after the fix, TN and TP cells, good outcomes |
| **wrong** | `#CC2B1D` | `#F6AEA6` | 5.34:1 | 107 | **192** | Errors, tracebacks, before the fix, FP and FN cells, divergence |
| **accent** | `#C42B8C` | `#F4D5E9` | 5.16:1 | 109 | **222** | Callout numbers, the current item, the held-out test set, the gradient step, the one thing to look at first |
| **ink** | `#14202B` | &mdash; | 16.52:1 | 31 | &mdash; | All body text, neutral outlines, arrows |
| **paper** | `#FFFFFF` | &mdash; | &mdash; | 255 | &mdash; | Nothing. It is the background you never draw. |

Three supporting neutrals (not &ldquo;colours&rdquo;, they carry no meaning):

| Name | Hex | Contrast on white | Greyscale | Use it for |
|---|---|---|---|---|
| **muted** | `#55636F` | 6.18:1 | 97 | Captions, axis numbers, secondary labels |
| **grid** | `#C7CDD4` | 1.60:1 | 204 | Grid lines, dashed dividers, contour rings, panel outlines |
| **panel** | `#F5F8FA` | 1.07:1 | 248 | A tinted background panel behind a scene, and neutral boxes |

&ldquo;Greyscale&rdquo; = the 0&ndash;255 grey value the colour becomes when the page is printed
black-and-white (sRGB luminance, re-encoded). **This is the verifiable print check**: convert your
figure to greyscale and the numbers above are what you should measure.

**Every stroke passes WCAG AA on white.** All six role strokes sit between **5.16:1 and 7.10:1**,
clearing the AA 4.5:1 threshold *for text*, not merely the 3:1 threshold for shapes. So you may set
a label in any role colour. Ink on any role fill also clears AA (worst case `ink` on `wrong` fill =
**9.06:1**), so text is always legible inside a tinted box.

### 1.2 Why strokes and fills are split (read this once)

The two requirements &mdash; *AA-legible on white* and *distinguishable in greyscale* &mdash; pull in
opposite directions. Any colour dark enough to pass AA on white lands in a narrow luminance band, so
**all six strokes print as virtually the same grey (88&ndash;109)**.

That is not a bug; it is the design. In print all outlines read as one consistent ink weight, which
is what makes line art look clean. **Hue therefore never carries meaning on its own.** The meaning is
carried by the *fill luminance ladder*, which was deliberately spread:

```
wrong 192  <  human 202  <  model 212  <  accent 222  <  data 232  <  correct 242
```

Even steps of 10 grey levels, with the pairs that matter most spread furthest apart:

- **correct (242) vs wrong (192) &mdash; 50 levels.** Unmistakable in print, on top of the tick/cross shapes.
- **data (232) vs accent (222)** is only 10 levels apart. In Level 2 that pair was train vs test. In
  Level 3 it is also *the value* vs *the thing to look at* &mdash; a cell versus the highlighted
  cell, a curve versus the marked point. So the highlighted thing must ALWAYS also differ by
  stroke width, position, a ring, or a printed number. Never rely on blue-vs-pink alone.
- **human (202) vs model (212)** is the new Level 3 near-pair: the validation set versus the weights.
  Ten levels. They almost never appear in the same figure; if they do, label both.

Fills are pale on purpose and **never define an edge** &mdash; the 3px stroke does. So a fill being
close to white costs you nothing.

### 1.3 Which colour pairs are safe together

Measured as OKLab &Delta;E&times;100, under normal vision and under simulated red/green colour
blindness (protanopia and deuteranopia, Machado 2009 at full severity). A pair passes when
normal &ge; 15 **and** colour-blind &ge; 8. **12 of the 15 pairs pass both gates.**

| Pair | Normal | Colour-blind | |
|---|---|---|---|
| model / human | 33.7 | 31.2 | pass |
| model / wrong | 33.7 | 29.7 | pass |
| model / correct | 33.4 | 24.9 | pass |
| data / human | 23.3 | 22.1 | pass |
| data / wrong | 31.0 | 21.9 | pass |
| data / correct | 17.6 | 16.7 | pass |
| human / accent | 24.6 | 14.3 | pass |
| model / accent | 22.0 | 13.1 | pass |
| **correct / wrong** | **28.4** | **9.1** | **pass** &mdash; the safety-critical pair, and the one the confusion matrix leans on |
| correct / accent | 32.3 | 8.7 | pass |
| **data / model** | **17.7** | **8.4** | **pass** &mdash; the pipeline pair, and Level 3's activations-vs-weights pair |
| **data / accent** | **26.2** | **8.3** | **pass** &mdash; the value-vs-highlight pair, and the weakest passing one |
| wrong / accent | 14.8 | 14.1 | **needs shape + label** |
| human / correct | 13.2 | 6.7 | **needs shape + label** |
| human / wrong | 16.3 | 4.7 | **needs shape + label** |

**Charts: at most three role colours.** For any chart where marks are compared all against all,
pick one of these validated triples: `data + correct + wrong` (the usual choice), `model + correct +
wrong`, `data + model + human`, or `model + human + accent`. Need a fourth category? Fold it into
&ldquo;Other&rdquo;, or split into two charts. Do not invent a seventh colour.

### 1.4 Canvas rules

**No new canvas sizes in Level 3.** These four cover every figure in this level.

| Name | viewBox | Use for |
|---|---|---|
| **wide** | `0 0 800 400` | Pipelines, before/after, three-panel progressions, shape traces, matrix diagrams, error-and-fix pairs |
| **square** | `0 0 500 500` | Charts, a chart plus its tables, single-idea diagrams, close-ups |
| **tall** | `0 0 500 700` | Step-by-step stacks, layer-by-layer network traces, long tables |
| **strip** | `0 0 800 260` | A single shape annotation with a callout, one terminal panel, one before/after row |

- **Never set `width` or `height` on the root `<svg>`.** viewBox only, so the figure scales to
  whatever column it lands in, in print or on screen.
- **20px of internal padding.** Nothing except a deliberate full-bleed background touches the edge.
  On a wide canvas your live area is x 20&ndash;780, y 20&ndash;380.
- **Transparent background.** Do not paint a white rect over the canvas &mdash; it breaks dark mode
  and wastes ink. If you want a tinted panel, use `panel` `#F5F8FA` on a rounded rect *inside* the
  padding.
- **No external references of any kind.** No `<image href>`, no PNG or JPEG, no `<link>`, no
  `href="http..."`, no webfont. Every figure is self-contained vector.
- Root element, always exactly this shape:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img">
  <title>...</title>
  <desc>...</desc>
  <!-- figure goes here -->
</svg>
```

### 1.5 Line, shape, type and accessibility

| Thing | Value |
|---|---|
| Primary stroke (the subject) | `stroke-width="3"` |
| Secondary stroke (supporting parts) | `stroke-width="2"` |
| Grid lines, dividers, leader lines, contour rings | `stroke-width="1.5"` |
| Emphasis marks (tick, cross) | `stroke-width="6"` |
| Line caps | `stroke-linecap="round"` on every open path |
| Line joins | `stroke-linejoin="round"` on every stroked polygon or rounded rect |
| Box corners | `rx="8"` small boxes, `rx="10"` standard, `rx="12"` large panels |
| Grid **cells** | square corners, no `rx` &mdash; cells butt against each other |

The **soft hand-drawn feel** comes from round caps, round joins and generous corner radii &mdash;
**not** from wobble, texture or filters. Keep geometry exact; the roundness does the warmth.

- **Draw connectors first, boxes second.** Then wires tuck under nodes instead of crossing them.
  Level 3 leans on this hard: a network has twenty edges and eight nodes.
- **A stroke's job is the edge; a fill's job is the tint.** Every meaningful shape gets both.

**System fonts only. Never a webfont, never `@font-face`, never Google Fonts.**

```
font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
```

| Level | Size | Colour | Use |
|---|---|---|---|
| Title | `24` | `ink` | One per figure, top-centre |
| Label | `18` | `ink` | Names of boxes, stages, panel headings |
| Caption | `14` | `muted` | The one-line takeaway at the bottom; also cell values in a small grid |
| Tiny | `12` | `muted` | Axis numbers, cell values, index labels, shape annotations, legend text |

**Never go below 12.** At print scale, 12 is already small.

- **Horizontal anchoring:** use `text-anchor` &mdash; `middle` for centred, `start` (default) for
  left-aligned, `end` for right-aligned numbers such as a y-axis. Never fake centring with a guessed
  x offset.
- **Vertical:** `y` is the *baseline*, not the middle. To centre text in a box use
  `dominant-baseline="central"` and set `y` to the box's centre. Print fallback: a few older print
  renderers ignore `dominant-baseline`, so for print-critical figures drop it and set the baseline
  manually with `y = centre + fontSize * 0.35`.
- Rotate axis titles with `transform="rotate(-90 x y)"` about the text's own anchor point.
- **Never** rely on text wrapping &mdash; SVG has none. Break lines yourself with separate `<text>`
  elements about `fontSize * 1.35` apart.

**Every figure carries `role="img"` and starts with `<title>` then `<desc>`.** No exceptions.

- **`<title>`** = the figure's name. Short. Matches the caption in the teacher file.
- **`<desc>`** = what a person who cannot see it would need told. Describe the *content and the
  point*, not the shapes. **In Level 3 that means the `<desc>` must contain the numbers.** Not
  &ldquo;a curve with a tangent line&rdquo; but &ldquo;at the point where w is 3 and the loss is 9, a
  straight line just touches the curve, and a callout says 3.0 divided by 0.5 gives a slope of
  6&rdquo;. A blind reader must be able to check the arithmetic too.
- **The markdown alt text must agree with `<title>`, word for word.** Every markdown file in
  `teacher-guide/`, `student-guide/` and `workbook/` sits one directory below `figures/`, so the link
  always starts `../figures/`, and every embed gets an italic caption line numbered
  `Figure <week>.<n>`:

```markdown
![The slope at one point on a curve](../figures/fig-w11-1-slope-as-a-division.svg)
*Figure 11.1 — The slope at one point on a curve. The slope is a division, not a symbol.*
```

  If a teacher reads the alt text aloud, the class should still follow.
- Decorative motifs *inside* a figure need nothing extra &mdash; the parent `<desc>` covers them.
- If you `<use>` a motif standalone, label it:
  `<use href="_motifs.svg#motif-confusion" aria-label="The confusion matrix: all four numbers named"/>`.

### 1.6 The monospace stack, for numbers-in-a-grid and program artefacts only

Inherited from Level 2 and it matters more here, because Level 3 sets **shapes** like `(750, 16)`
where the digits and commas have to line up.

```
font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
```

It is still **system fonts only**, so nothing about &sect;1.5 is waived. Use it **only** for: a shape
annotation, a code token in a callout, a line inside a terminal or traceback panel, and a filename.
Never for a title, a label, a caption or an axis.

- **The 12px floor still applies**, and mono runs wider than sans at the same size, so budget
  `chars &times; fontSize &times; 0.6` for the width and check it fits. At 14px one character
  advances **8.4px**, which is the number you use when you place fixed-x runs (&sect;2.3).
- Program output is 14px; traceback lines are 12px; shape annotations are 12px in a chip and 14px
  when written on a block.

### 1.7 `font-weight="600"` is allowed, in exactly two places

A DataFrame's header row must read as a header, and the last line of a traceback is the line you
want read first. `font-weight="600"` is permitted on **table and DataFrame header cells, and on the
error lines of a traceback**. Nowhere else &mdash; not for emphasis, not for titles. Titles are
already 24px; that is the emphasis.

### 1.8 The scaling rule: `scale()` scales the type too

`<g transform="scale(0.5)">` around a motif whose labels are 12px produces **6px type**, which
violates the floor and cannot be photocopied.

> **Never place a text-bearing motif at `scale()` below 1.0.**

If the box is too small for the motif at 1.0, you have two legal moves:

1. **Use a text-free glyph** and put the words in the surrounding 18px stage label. This is what
   `pattern-pipeline` (&sect;6.1) does, and why its four stage glyphs carry no text of their own.
2. **Make the box bigger**, or split the figure in two.

Text-free motifs (`motif-arrow`, `motif-arrow-curved`, `motif-badge-check`, `motif-badge-cross`,
`motif-table`, `motif-note`) may be scaled freely. Scale **uniformly** &mdash; never stretch one axis.
Scaling *up* is always safe: `pattern-progression` places its learning-rate panels at `scale(1.2)`.

### 1.9 The sanctioned exception: when the artefact *is* the lesson

**A traceback and a program's output are artefacts the learner must learn to read.** You cannot teach
&ldquo;the last line names two shapes, compare them&rdquo; without showing the lines.

So `motif-terminal`, `motif-traceback`, `motif-traceback-shape` and `pattern-error-fix` may contain
verbatim monospace text. **This is the complete list of places where literal code or output may
appear.** Rules that still apply inside the exception:

- The figure's *work* is the annotation &mdash; the highlight bar, the arrow, the label. A terminal
  panel with no annotation is not a figure, it is a screenshot, and it is a defect.
- Keep it to **five lines or fewer**. If your traceback needs six lines, you are showing the program,
  not the error.
- Everything *around* the text stays on the &sect;1.1 palette: ink frames, muted captions, accent pins.
- This exception does **not** license &sect;3.

---

## 2. Level 3 extensions to the system

Six additions. That is the complete list; do not invent a seventh.

### 2.1 The arithmetic rule: if the figure claims a number, show the sum

This is the single most important *new* rule, and it is what makes a Level 3 figure teach the
teacher. Level 3's subjects are all calculations. A figure that shows the *shape* of a calculation
without its numbers has drawn a diagram of a thing the reader still cannot do.

> **Every Level 3 figure that involves a calculation must print at least one instance of that
> calculation, worked out, in numbers a reader can check on paper.**

| The figure is about&hellip; | So it must print&hellip; |
|---|---|
| a slope | the rise, the run, and the division: `3.0 &#247; 0.5 = 6` |
| a gradient-descent step | `3 &#8722; 0.1 &#215; 6 = 2.4`, and the loss before and after |
| a matrix multiply | one output cell in full: `1.0 &#215; 0.5 + 2.0 &#215; 0.8 + 0.1 = 2.20` |
| a neuron | the same, on the neuron |
| precision | `16 &#247; 21 = 0.7619`, and where the 16 and the 21 came from |
| a convolution | one output cell: `(1 &#215; 10) + (0 &#215; 10) + (&#8722;1 &#215; 2) = 8`, then `8 + 8 + 8 = 24` |
| k-means | the counts in each cluster, in every panel |
| a split | the three counts, and they must add up to the printed total |

And the numbers must be **real**. Every number in this file's motifs was taken from the worked
examples in `module-01` &hellip; `module-09` and can be reproduced with a calculator. Inventing a
plausible-looking number is the defect class that has bitten this repository hardest.

### 2.2 Every tensor block carries its shape

A shape is not optional decoration in Level 3; it is the thing being taught, because shape bugs are
most of what goes wrong. So:

- Any block standing for a tensor gets a **mono shape annotation**, either in a `chip` pinned to its
  corner (`shape (3, 4)`) or written across its middle (`(750, 16)`).
- Any bundle of wires between two layers gets a **weight chip** (`W1 (2, 16)`).
- Say it out loud as you draw it: *&ldquo;seven-fifty by two, times two by sixteen, gives seven-fifty
  by sixteen.&rdquo;* If that sentence is not readable off the figure, the figure is not finished.

### 2.3 Highlighting one digit: fixed-x mono runs

To box the `2` in `(750, 2)` you cannot draw one `<text>` and guess where the digit sits &mdash; the
advance width is font-dependent and the box will land in the wrong place. **Split the annotation into
separate `<text>` runs at fixed x**, one per part, and put the highlight rect under the run you want:

```svg
<!-- "(750, 2)" with the inner 2 boxed.  Mono 14px advances 8.4px per character. -->
<rect x="83" y="68" width="14" height="22" rx="4" fill="#F4D5E9" stroke="#C42B8C" stroke-width="2" stroke-linejoin="round"/>
<text x="40" y="84" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#14202B">(750,</text>
<text x="86" y="84" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#14202B">2</text>
<text x="98" y="84" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#14202B">)</text>
```

Leave a 4px gap between runs so the audit's label-collision check stays quiet and the eye reads the
parts as one string. `motif-matmul`, `motif-shape-mismatch` and `pattern-structure` all do this.

### 2.4 Minus signs, times signs and arrows are entities, never keyboard characters

Level 3 figures are full of negative numbers and mappings, and a hyphen standing in for a minus sign
looks like a typo at 12px. Use these, and only these:

| Meaning | Entity | Renders |
|---|---|---|
| minus / negative | `&#8722;` | &#8722;0.3 |
| times | `&#215;` | 3 &#215; 4 |
| divided by | `&#247;` | 16 &#247; 21 |
| becomes / maps to | `&#8594;` | 9.00 &#8594; 5.76 |
| en dash in a range | `&#8211;` | 0&#8211;1 |
| em dash in prose | `&#8212;` | like &#8212; this |
| middle dot separator | `&#183;` | rows &#183; columns |

Never `->` in a figure. Never `-` for a negative number. `<` and `>` and `&` inside a terminal or
traceback panel must be escaped as `&lt;` `&gt;` `&amp;`, or the file will not parse as XML.

### 2.5 New role assignments

The eight roles of &sect;1.1 do not change, but Level 3 introduces things that need a home. These
assignments are fixed; do not improvise:

| Level 3 thing | Role | Why |
|---|---|---|
| activations, batches, feature maps, any tensor of values | **data** | it is measured data flowing through |
| weights, biases, kernels, layers, principal components | **model** | it is the learned thing |
| the validation set | **human** | it is where a *person* makes choices, over and over |
| the test set | **accent** | inherited from Level 2: the pile you must not touch |
| the gradient step, the marked point, the highlighted cell/row/column | **accent** | the one thing to look at first |
| the backward pass | **accent**, dashed | it is the annotation on a forward network, not a second network |
| TN and TP cells; a monotone loss curve; the fixed pipeline | **correct** | good outcomes |
| FP and FN cells; divergence; the leaking pipeline; a shape mismatch | **wrong** | failures |
| contour rings, receding copies in a 3-D stack, wires in a network | **grid** | supporting structure, no meaning |

### 2.6 Composed figures match by number, not by leader line

Level 3 constantly pairs a chart with a table: an ROC curve with three confusion matrices, a loss
curve with three learning rates. Three leader lines drawn across a chart cross the data and each
other. So:

> **When two parts of a figure refer to the same thing, give both parts the same NUMBER in a badge.**

A ringed `1` on the curve and a ringed `1` on its table. That survives greyscale, survives
photocopying, and survives the reader looking at the parts in either order. `motif-roc` and
`pattern-annotated-chart` are the reference implementation.

---

## 3. The hard rule: a figure is not a picture of code, and not a picture of a formula

> **A figure must never be a picture of code. It must never be a picture of a formula either.
> It shows what the formula DOES to numbers.**

Both halves are the same mistake: transcribing a notation the reader cannot yet read, and calling it
a diagram. The code is already on the page, in a fenced block, in a font the reader can copy from.
The formula, if it is needed at all, belongs in the prose where it can be explained a symbol at a
time. A figure that repeats either one adds nothing, costs a page, and &mdash; worse &mdash; teaches
the learner that maths is a shape to memorise rather than a thing to picture.

**Remember who is reading. The teacher does not know calculus.** `dL/dw = 2w` is not information to
them; it is wallpaper. `9.006001 &#8722; 8.994001 = 0.012`, then `0.012 &#247; 0.002 = 6.000`, is
something they can do, check, and teach.

Ask this before you draw: **&ldquo;What would the learner have to imagine, or work out, to predict
what this does?&rdquo;** Draw that.

| Instead of drawing&hellip; | Draw&hellip; |
|---|---|
| the symbols `dL/dw = 2w` | a curve, a tangent at a marked point, and `3.0 &#247; 0.5 = 6` (`motif-tangent`) |
| the symbols `w := w &#8722; &#945;&#8711;L` | a bowl with four numbered steps, each labelled with its own `(w, loss)` (`motif-loss-bowl`) |
| the line `for epoch in range(500):` | one step's arithmetic, and the dot moving down the wall (&sect;3.1) |
| the symbols `&#963;(z) = 1/(1+e^&#8722;z)` | the neuron: inputs, weights, the sum, the squash, the output number (`motif-neuron`) |
| the symbols `Z = A @ W` | two blocks, the inner numbers boxed, the answer's shape annotated (`motif-matmul`) |
| the line `X_train.shape` | a labelled block with `shape (750, 2)` written on it (`motif-tensor-2d`) |
| the traceback in prose | the traceback panel, with the offending line highlighted and arrowed (`motif-traceback-shape`) |
| the symbols `P = TP/(TP+FP)` | the matrix with the predicted-positive column outlined, and `16 &#247; 21 = 0.7619` (`motif-precision-overlay`) |
| the line `KMeans(n_clusters=2).fit(X)` | three panels of the same six points recolouring around moving centroids (`motif-kmeans-1..3`) |
| the symbols for a convolution sum | the window, the kernel, and one output cell multiplied out in full (`motif-conv`) |
| the line `train_test_split(...)` twice | three proportioned bars with `1200 / 400 / 400` printed on them (`motif-split-three`) |

### 3.1 Worked example one: not a picture of code

The lesson is *&ldquo;one gradient-descent step moves you downhill by the learning rate times the
slope&rdquo;*.

**Wrong.** This is a screenshot with a border. Everything in it is already in the code block above
it; the reader's eye has nowhere to go, and the *step* &mdash; the entire point &mdash; is invisible.

```svg
BAD_CODE_SVG
```

**Right.** No code on the canvas. The dot moves, the arrow shows which way, and the four lines of
arithmetic let a teacher who has never seen calculus reproduce the step with a calculator and then
predict the next one.

```svg
GOOD_CODE_SVG
```

Note what the good figure keeps from the bad one: the numbers `0.1`, `3` and `6`. **Values are not
code.** What it drops is the *syntax* &mdash; the `for`, the `range(500)`, the `-=`.

### 3.2 Worked example two: not a picture of a formula

The lesson is *&ldquo;the slope of `w &#215; w` at `w = 3` is 6, and you can check that by nudging&rdquo;*.

**Wrong.** A beautifully set formula that a 14-year-old and their teacher cannot read. There is
nothing to look at, nothing to check, and nothing to do. Setting it larger does not help.

```svg
BAD_FORMULA_SVG
```

**Right.** The same fact, done to numbers. Two nudged values of the loss, one subtraction, one
division, and the answer &mdash; beside a curve with the line whose steepness that answer *is*.

```svg
GOOD_FORMULA_SVG
```

**Where symbols ARE allowed.** A symbol may appear as a *label* on a thing, never as the figure's
content: `w` on an x axis, `loss` on a y axis, `W1` over a bundle of wires, `sum` inside a node,
`ReLU` on a box, `t = 0.50` beside a marked point. The test is whether removing the symbol would
leave the figure meaningless (fine, it is a label) or leave it unchanged (then it was the content,
and the figure has failed).

### 3.3 The four-question test

Before you commit a figure, answer all four. Any &ldquo;no&rdquo; means redraw.

1. **Cover the code block. Does the figure still teach something?** If the figure only makes sense
   next to the code, it is decoration.
2. **Cover the figure. Does the code block lose anything?** If not, the figure is redundant &mdash;
   delete it, and spend the page on the thing the reader *cannot* see.
3. **Is there at least one sum on the canvas that a reader could check with a calculator?** (&sect;2.1)
4. **Could the teacher &mdash; no AI, no Python, no calculus &mdash; explain this figure aloud after
   twenty seconds of looking at it?** They are the reader who decides whether the lesson lands.

---

## 4. Motif library &mdash; Level 3 (MOTIF_COUNT_NEW)

**Do not redraw these.** Consistency across the whole three years is the point. Two ways to use them:

```svg
<!-- A) reference the sprite sheet -->
<use href="_motifs.svg#motif-confusion" x="40" y="40" width="380" height="260"/>

<!-- B) copy the <g> inline (below) and position it -->
<g transform="translate(600,150)">...</g>
```

Every motif is drawn to its own viewBox with **the origin at the top-left**, so `translate(x,y)` puts
its top-left corner at exactly `(x,y)`. Remember &sect;1.8 before you scale one.

Two of the motifs the level needs are inherited unchanged and live in &sect;5, with their snippets:
**`motif-terminal`** (a terminal panel) and **`motif-traceback`** (a red-outlined traceback with an
arrow at the offending line, for the Level 2 error types). Level 3's own traceback &mdash; the shape
error &mdash; is below.

MOTIF_BLOCKS_NEW

---

## 5. Motifs inherited from Level 2 (MOTIF_COUNT_OLD)

Copied byte-for-byte from Level 2's sprite sheet so the years match. Reproduced here in full so this
folder is self-contained. Level 2's other motifs (`motif-variable`, `motif-rebind`, `motif-list`,
`motif-dict`, `motif-loop`, `motif-if-else`, `motif-function`, `motif-callstack`, `motif-array-1d`,
`motif-chart-scatter`, `motif-chart-bar`, `motif-chart-line`, `motif-knn`, `motif-tree`,
`motif-fit-underfit`, `motif-fit-good`, `motif-fit-overfit`, `motif-code-callout`) all still exist
and may be pulled across from `../../level-2-builder/36-week-course/figures/_motifs.svg` if a week
needs them &mdash; a Level 3 week that revisits overfitting should reuse Level 2's three-panel fit
trio rather than draw a new one.

MOTIF_BLOCKS_OLD

---

## 6. Composition patterns

Seven diagram types cover essentially every figure in this level. Start from the matching skeleton and
swap the content. Each one below is a complete, valid SVG that passes &sect;9.

| Pattern | Reach for it when |
|---|---|
| `pattern-pipeline` | Something flows through ordered stages |
| `pattern-before-after` | One thing changed and you want the reader to find it |
| `pattern-progression` | A dial was turned through three settings |
| `pattern-annotated-chart` | A chart where particular marks are the story, each with its own numbers |
| `pattern-structure` | A tensor/shape diagram: shapes changing along a chain |
| `pattern-matrix` | A matrix diagram: one cell of a product, multiplied out |
| `pattern-error-fix` | Something broke and then it did not |

PATTERN_BLOCKS

---

## 7. Naming

```
fig-wNN-<n>-<slug>.svg
```

- `wNN` &mdash; the week, always two digits: `w01` &hellip; `w36`.
- `<n>` &mdash; the figure's sequence **within that week**, starting at 1.
- `<slug>` &mdash; two to four lowercase words, hyphenated, describing the content.

```
fig-w11-1-slope-as-a-division.svg
fig-w13-2-loss-bowl-four-steps.svg
fig-w18-3-shape-mismatch-flagged.svg
fig-w22-1-confusion-four-cells.svg
fig-w27-2-conv-one-output-cell.svg
```

Lowercase only, hyphens only, no spaces, no underscores, no dates, no version suffixes.
Files beginning with `_` are shared infrastructure (`_motifs.svg`, `_preview.html`), not figures.

**Slugs name the idea, not the notation.** `fig-w11-1-slope-as-a-division.svg`, never
`fig-w11-1-dl-dw-equals-2w.svg`. `fig-w18-3-shape-mismatch-flagged.svg`, never
`fig-w18-3-valueerror-not-aligned.svg`. The filename is the first place &sect;3 gets broken.

### 7.1 The filename number and the caption number are different numbers

| | What it counts | Example |
|---|---|---|
| **Filename `<n>`** | The order the figure was **drawn**, within its week. It never changes once assigned. | `fig-w22-4-roc-three-thresholds.svg` was the 4th figure drawn for Week 22. |
| **Caption `<n>`** | The order the figure is **read**, within *one markdown file*. | That same figure may be `*Figure 22.2*` in the student guide and `*Figure 22.5*` in the teacher guide. |

**These two numbers usually do not match, and that is correct.** Number captions by reading order in
the file you are editing, and never renumber a file.

- **Workbook captions carry a `W`:** `*Figure W22.1*`, so a workbook figure can never be confused
  with a chapter figure of the same number.
- **When you cite a figure that lives in a different book, say which book.** Not *&ldquo;see Figure
  22.4&rdquo;* but *&ldquo;see **Figure 22.4 in the Week 22 chapter**&rdquo;*.

---

## 8. Don'ts

Everything Levels 1 and 2 banned is still banned, plus five Level 3 items.

- **No pictures of code.** &sect;3. This is the one that will get a figure rejected.
- **No pictures of formulae.** &sect;3.2. New in Level 3, and it will get a figure rejected just as fast.
  Symbols are labels only.
- **No number on the canvas that you have not checked.** &sect;2.1. If it is not from a module's worked
  example or reproducible with a calculator, it does not go on the page.
- **No tensor block without its shape.** &sect;2.2.
- **No `->` and no hyphen-as-minus.** &sect;2.4.
- **No matching by leader line where a number would do.** &sect;2.6.
- **No text-bearing motif below `scale(1.0)`.** &sect;1.8.
- **No monospace outside &sect;1.6's list.** Titles, labels, captions and axes are sans, always.
- **No literal code or output outside the four exceptions in &sect;1.9**, and never without an annotation.
- **No external images.** No `<image href>`, no PNG, no JPEG, no tracing a screenshot. Vector only.
- **No webfonts.** No `@font-face`, no `<link>` to a font. The two stacks in &sect;1.5 and &sect;1.6, or nothing.
- **No filters that fail in print.** No `<filter>`, no `feGaussianBlur`, no `feDropShadow`, no CSS
  `filter`, no `opacity` below 1 to fake a tint (use the pale fill instead).
- **No colour as the only carrier of meaning.** Ever. Every meaningful distinction needs a **second**
  cue: a shape, a label, a number, or a position. Cluster membership is circle-vs-triangle. The
  backward pass is dashed AND reversed AND labelled. Train/validation/test carry printed counts.
- **No gradients.** Flat fills only.
- **No `width`/`height` on the root `<svg>`.** viewBox only.
- **No white background rect.**
- **No text below 12px**, and no text you expect to wrap.
- **No new colours.** If you think you need a seventh, you need a different diagram (&sect;1.3).
- **No `<foreignObject>`**, no embedded HTML, no `<script>`.
- **No `<ellipse>`.** Not banned for taste &mdash; the audit's bounds checker does not understand it,
  so an ellipse can silently break the 20px padding. Approximate it with a `<polygon>`; see
  `pattern-before-after`.

---

## 9. Pre-flight check

```bash
# 1. It must parse as XML.
python3 -c "import xml.dom.minidom,sys; xml.dom.minidom.parse(sys.argv[1])" fig-w13-2-loss-bowl-four-steps.svg

# 2. It must not contain anything banned.
grep -nE '<image|href="http|@font-face|<filter|feGaussianBlur|feDropShadow|<foreignObject|<script|Gradient|<ellipse' \
  fig-w13-2-loss-bowl-four-steps.svg && echo "BANNED CONSTRUCT" || echo "clean"

# 3. It must declare accessibility and no fixed size.
f=fig-w13-2-loss-bowl-four-steps.svg
grep -q 'role="img"' $f && grep -q '<title>' $f && grep -q '<desc>' $f && echo "a11y ok"
grep -nE '<svg[^>]+(width|height)=' $f && echo "REMOVE width/height" || echo "scales ok"

# 4. No type under the floor, and nothing shrunk under scale().
grep -oE 'font-size="[0-9.]+"' $f | sort -u          # nothing below 12
grep -oE 'scale\([0-9.]+' $f | sort -u               # any value < 1 on a group containing <text> is a defect

# 5. Only palette colours, only the two font stacks.
grep -oE '(fill|stroke)="#[0-9A-Fa-f]+"' $f | sort -u
```

Or run the whole audit over every motif, pattern, worked example and finished figure at once. It
checks bounds against the 20px padding, effective font size after every `scale()`, banned constructs,
overlapping labels, off-palette colours, unsanctioned font stacks, and the
`role="img"` + `<title>` + `<desc>` contract:

```bash
cd _generator && python3 _gen_audit.py     # must print "--- 0 finding(s)"
```

Then, by eye:

- [ ] **It is not a picture of code, and not a picture of a formula.** All four questions in &sect;3.3
      answered yes.
- [ ] **There is a sum on the canvas, and you have checked it against the module.** (&sect;2.1)
- [ ] Every tensor block carries its shape; every wire bundle carries its weight shape. (&sect;2.2)
- [ ] `<title>` matches the markdown alt text word for word, and `<desc>` describes the *idea* **and
      contains the numbers**.
- [ ] Every colour is from &sect;1.1, used in its role (&sect;2.5).
- [ ] Nothing within 20px of the canvas edge &mdash; including the far end of a long caption.
- [ ] Every meaningful distinction has a shape, label or number as well as a colour.
- [ ] Every leader line and callout routed through empty space; nothing overlaps a data point.
- [ ] Minus signs, times signs and arrows are entities, not keyboard characters. (&sect;2.4)
- [ ] Opened `_preview.html`, ticked **Greyscale**, and the figure still reads.
- [ ] A 14-year-old gets the point in four seconds with the caption covered.
- [ ] A teacher who has never seen calculus gets it too, and could teach it.

---

## 10. Files in this folder

| File | What it is |
|---|---|
| `STYLE.md` | This contract. |
| `_motifs.svg` | Sprite sheet: all MOTIF_COUNT_ALL motifs as `<symbol>`. Reference with `<use>` or copy inline. |
| `_preview.html` | Open in any browser. Renders the palette, every motif grouped by subject, both &sect;3 pairs and every pattern, with greyscale and dark-page toggles. |
| `_generator/` | The source of truth. `STYLE.md`, `_motifs.svg` and `_preview.html` are all generated from it, so a motif can never disagree with its own snippet. Edit a motif here, then re-run the three commands below. |
| `fig-wNN-*.svg` | The week figures. |

```bash
cd _generator
python3 _gen_emit.py     # rewrites _motifs.svg and _preview.html
python3 _gen_style.py    # rewrites STYLE.md
python3 _gen_audit.py    # bounds, 12px floor, scale(), banned constructs, collisions, palette, a11y
```

Generator layout, in dependency order &mdash; each module imports the one before it, so importing
`_gen_term` registers every motif:

| Module | Holds |
|---|---|
| `_gen_core.py` | palette, helpers, the `MOTIFS` registry |
| `_gen_math.py` | tangent, loss bowl, the three learning rates |
| `_gen_tensor.py` | 1-D to 4-D tensors, matrix multiply, shape mismatch |
| `_gen_net.py` | neuron, network with shapes, forward vs backward |
| `_gen_eval.py` | confusion matrix and overlays, ROC, three-way split, leakage pair |
| `_gen_vision.py` | convolution, feature-map stack, k-means trio, PCA, bag of words |
| `_gen_term.py` | shape traceback, and the 12 motifs inherited from Level 2 |
| `_gen_pat.py` | the 7 composition patterns, the 4 hard-rule examples |
| `_gen_emit.py` | writes `_motifs.svg` and `_preview.html` |
| `_gen_style.py` | writes this file |
| `_gen_audit.py` | the check that must print `--- 0 finding(s)` |
"""


def build():
    doc = DOC
    ex = {e[0]: e[2] for e in EXAMPLES}
    doc = doc.replace("BAD_CODE_SVG", ex["example-bad-code-screenshot"])
    doc = doc.replace("GOOD_CODE_SVG", ex["example-good-mental-model"])
    doc = doc.replace("BAD_FORMULA_SVG", ex["example-bad-formula-picture"])
    doc = doc.replace("GOOD_FORMULA_SVG", ex["example-good-formula-in-numbers"])
    doc = doc.replace("MOTIF_BLOCKS_NEW", grouped_motif_blocks())
    doc = doc.replace("MOTIF_BLOCKS_OLD", "\n".join(motif_block(m) for m in OLD))
    doc = doc.replace("PATTERN_BLOCKS", "\n".join(pattern_block(p) for p in PATTERNS))
    doc = doc.replace("MOTIF_COUNT_NEW", str(len(NEW)))
    doc = doc.replace("MOTIF_COUNT_OLD", str(len(OLD)))
    doc = doc.replace("MOTIF_COUNT_ALL", str(len(MOTIFS)))
    open(os.path.join(HERE, "STYLE.md"), "w").write(doc)
    return doc


if __name__ == "__main__":
    d = build()
    for token in ("MOTIF_BLOCKS", "PATTERN_BLOCKS", "MOTIF_COUNT", "_SVG"):
        assert token not in d, "unreplaced placeholder containing %r" % token
    print("STYLE.md: %d lines, %d motif blocks, %d pattern blocks, %d worked examples"
          % (d.count("\n") + 1, len(MOTIFS), len(PATTERNS), len(EXAMPLES)))

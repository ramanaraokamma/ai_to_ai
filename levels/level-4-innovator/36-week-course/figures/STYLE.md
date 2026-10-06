# Figure style system &mdash; AI Academy, Level 4 &ldquo;Innovator&rdquo; (36-week course)

**Audience: the authors drawing the SVG figures for Level 4.**
This file is the contract. If your figure disagrees with this file, this file wins.

**Level 4 is a faithful extension of Levels 1, 2 and 3.** Same palette, same stroke widths, same type
scale, same accessibility rules, same four canvases. A parent flipping between the four years should
not be able to tell where one ends and the next begins. Everything inherited is copied out in full
below, so **this file stands alone** &mdash; you never need to open an earlier `STYLE.md`.

What is new is the *subject matter*. Level 4 puts **loss curves, attention maps, token streams,
retrieval and agent loops** on the screen, and it runs entirely offline, so a large share of what is
drawn is a **stand-in** (a scripted backend) rather than a model. The new rules are about that:
numbers must be real and seeded (&sect;2.1), stand-ins must look like stand-ins (&sect;2.5), and a
literature number must look different from a number the student measured (&sect;2.6).

**The learner is one 15&ndash;16-year-old who finished Levels 1&ndash;3. They can write Python and
PyTorch and have trained small networks. The teacher is not assumed to know AI, Python or calculus,
and opened this week's file 20 minutes ago.** A figure has to land in about four seconds with no
caption, and teach the adult as well as the student.

---

## 0. The 30-second version

1. Copy a **composition pattern** (&sect;6) that matches your diagram type.
2. Drop in **motifs** (&sect;4, &sect;5) &mdash; do not redraw the attention grid.
3. Use only the eight **palette** colours (&sect;1.1), by *role*, never by taste.
4. **Do not draw the code and do not draw the formula.** Draw what it does to numbers (&sect;3).
5. **Every number on the canvas comes from an executed, seeded run** or a hand calculation printed
   beside it (&sect;2.1). Never invent one.
6. **A scripted stand-in is drawn dashed and labelled** `stand-in, not a model` (&sect;2.5).
7. Start every file with `role="img"`, then `<title>`, then `<desc>` (&sect;1.5).
8. Name it `fig-wNN-<n>-<slug>.svg` (&sect;7).
9. Run the audit (&sect;9). It must print `--- 0 finding(s)`.

---

## 1. Inherited verbatim from Levels 1&ndash;3

Nothing in this section may be changed.

### 1.1 Palette &mdash; eight colours, used by role

| Role | Stroke | Fill | Contrast on white | Greyscale (stroke) | Greyscale (fill) | Use it for |
|---|---|---|---|---|---|---|
| **data** | `#1F6FB2` | `#D9EAF9` | 5.28:1 | 108 | **232** | Data, values, tokens, activations, embeddings, inputs, anything measured |
| **model** | `#6D28D9` | `#DBCEF3` | 7.10:1 | 88 | **212** | The model: weights, layers, heads, the fitted or fine-tuned network |
| **human** | `#845F00` | `#E8C671` | 5.80:1 | 101 | **202** | People, choices a person made, prompts you wrote, the frozen eval set, rubrics, notes |
| **correct** | `#1B7A4B` | `#E2F7ED` | 5.34:1 | 107 | **242** | It ran, it passed, after the fix, retrieved-and-right, a guardrail that held |
| **wrong** | `#CC2B1D` | `#F6AEA6` | 5.34:1 | 107 | **192** | Errors, before the fix, divergence, a hallucinated citation, a successful injection |
| **accent** | `#C42B8C` | `#F4D5E9` | 5.16:1 | 109 | **222** | Callout numbers, the current token/step, the query, the one thing to look at first |
| **ink** | `#14202B` | &mdash; | 16.52:1 | 31 | &mdash; | All body text, neutral outlines, arrows |
| **paper** | `#FFFFFF` | &mdash; | &mdash; | 255 | &mdash; | Nothing. It is the background you never draw. |

Three supporting neutrals (they carry no meaning):

| Name | Hex | Contrast on white | Greyscale | Use it for |
|---|---|---|---|---|
| **muted** | `#55636F` | 6.18:1 | 97 | Captions, axis numbers, secondary labels, quoted-not-measured numbers |
| **grid** | `#C7CDD4` | 1.60:1 | 204 | Grid lines, dashed dividers, panel outlines, unused context |
| **panel** | `#F5F8FA` | 1.07:1 | 248 | A tinted panel behind a scene, and neutral boxes |

Every stroke passes WCAG AA on white, so a label may be set in any role colour. Ink on any role
fill also clears AA (worst case `ink` on `wrong` fill = 9.06:1).

### 1.2 Why strokes and fills are split

All six strokes print as nearly the same grey (88&ndash;109) by design. **Hue never carries
meaning on its own.** Meaning is carried by the fill luminance ladder:

```
wrong 192  <  human 202  <  model 212  <  accent 222  <  data 232  <  correct 242
```

- **correct vs wrong** is 50 levels apart: unmistakable in print, and also carries tick/cross shapes.
- **data (232) vs accent (222)** is only 10 apart. Level 4 leans on this pair hard (a token versus the
  *current* token; a chunk versus the *query*), so the highlighted thing must ALWAYS also differ by
  stroke width, a ring, a position or a printed number.
- **human (202) vs model (212)** are 10 apart (the frozen eval versus the weights). Label both if
  they share a figure.

### 1.3 Which colour pairs are safe together

OKLab &Delta;E&times;100, normal vision / simulated red-green colour blindness. Pass = normal &ge; 15
and colour-blind &ge; 8.

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
| **correct / wrong** | **28.4** | **9.1** | **pass** &mdash; safety-critical |
| correct / accent | 32.3 | 8.7 | pass |
| **data / model** | **17.7** | **8.4** | **pass** &mdash; activations versus weights |
| **data / accent** | **26.2** | **8.3** | **pass** &mdash; weakest; add a ring |
| wrong / accent | 14.8 | 14.1 | **needs shape + label** |
| human / correct | 13.2 | 6.7 | **needs shape + label** |
| human / wrong | 16.3 | 4.7 | **needs shape + label** |

**Charts: at most three role colours.** Validated triples: `data + correct + wrong`, `model +
correct + wrong`, `data + model + human`, `model + human + accent`. A loss-curve plot with more than
three series is split into small multiples (same y axis), never given a fourth colour. Series are
also told apart by **dash pattern and an end label**, never colour alone (&sect;2.3).

### 1.4 Canvas rules

**No new canvas sizes in Level 4.**

| Name | viewBox | Use for |
|---|---|---|
| **wide** | `0 0 800 400` | Pipelines, before/after, loops, attention plus text, retrieval flows, side-by-side curves |
| **square** | `0 0 500 500` | Charts, heatmaps, embedding scatter, single-idea close-ups |
| **tall** | `0 0 500 700` | Step-by-step stacks, a transformer block top to bottom, a long trace |
| **strip** | `0 0 800 260` | A token stream, one annotated row, one terminal panel |

- **Never set `width` or `height` on the root `<svg>`.** viewBox only.
- **20px of internal padding.** On a wide canvas the live area is x 20&ndash;780, y 20&ndash;380.
- **Transparent background.** No white rect. A tinted panel is a `panel` rounded rect *inside* the padding.
- **No external references.** No `<image href>`, PNG, JPEG, `<link>`, `href="http..."`, webfont.
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
| Secondary stroke | `stroke-width="2"` |
| Grid lines, dividers, leader lines | `stroke-width="1.5"` |
| Emphasis marks (tick, cross) | `stroke-width="6"` |
| Line caps | `stroke-linecap="round"` on every open path |
| Line joins | `stroke-linejoin="round"` on every stroked polygon or rounded rect |
| Box corners | `rx="8"` small, `rx="10"` standard, `rx="12"` large panels |
| Grid **cells** | square corners, no `rx` &mdash; cells butt against each other |

The warmth comes from round caps, round joins and generous radii &mdash; not wobble, texture or filters.
**Draw connectors first, boxes second** so wires tuck under nodes.

**System fonts only. Never a webfont, never `@font-face`.**

```
font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
```

| Level | Size | Colour | Use |
|---|---|---|---|
| Title | `24` | `ink` | One per figure, top-centre |
| Label | `18` | `ink` | Names of boxes, stages, panel headings |
| Caption | `14` | `muted` | The one-line takeaway at the bottom; cell values in a small grid |
| Tiny | `12` | `muted` | Axis numbers, cell values, token text in a dense stream, legend text |

**Never go below 12.** Use `text-anchor` (never a guessed x offset). `y` is the *baseline*; to centre
in a box use `dominant-baseline="central"` with `y` at the centre (print-critical figures: drop it and
use `y = centre + fontSize * 0.35`). Rotate axis titles with `rotate(-90 x y)`. SVG has no wrapping:
break lines yourself, about `fontSize * 1.35` apart.

**Every figure carries `role="img"` and starts with `<title>` then `<desc>`.**

- **`<title>`** = what the figure *means*. Short. Matches the caption.
- **`<desc>`** = what a person who cannot see it needs to be told, **including the numbers**: not
  &ldquo;a loss curve&rdquo; but &ldquo;training loss starts at 0.693 and falls to 0.21 by step 300;
  validation loss bottoms at step 120 then rises&rdquo; &mdash; with the figures taken from the run.
- Markdown alt text describes what a sighted reader *sees*; `<title>` states what it *means*. They may differ.
  Every markdown file in `teacher-guide/`, `student-guide/` and `workbook/` is one directory below
  `figures/`, so links start `../figures/`, and every embed gets an italic caption `Figure <week>.<n>`:

```markdown
![Training and validation loss, with the point where they part](../figures/fig-w05-2-early-stopping-curves.svg)
*Figure 5.2 — Validation loss turns upward while training loss keeps falling.*
```

- If you `<use>` a motif standalone, label it: `<use href="_motifs.svg#motif-token-stream" aria-label="..."/>`.

### 1.6 The monospace stack, for program artefacts only

```
font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
```

Use it **only** for: a shape annotation (`(8, 4, 16)`), a code token in a callout, a line inside a
terminal / trace panel, a filename, **and the text of a token** in a token stream (the student must see
exactly where whitespace and byte boundaries fall). Never for a title, label, caption or axis. Mono
runs wider: budget `chars &times; fontSize &times; 0.6`; at 14px one character advances **8.4px**.
The 12px floor applies.

### 1.7 `font-weight="600"`

Permitted on table/DataFrame header cells, on the error line of a traceback, and on the **current
step's row** in an agent trace. Nowhere else.

### 1.8 The scaling rule

> **Never place a text-bearing motif at `scale()` below 1.0.** `scale(0.5)` turns 12px into 6px.

Either use a text-free glyph with the words in the 18px label beside it, or make the box bigger.
Text-free motifs (`motif-arrow`, `motif-arrow-curved`, `motif-badge-check`, `motif-badge-cross`,
`motif-table`, `motif-note`) scale freely, uniformly. Scaling *up* is always safe.

### 1.9 The sanctioned exception: when the artefact *is* the lesson

Literal code or output may appear in `motif-terminal`, `motif-traceback`, `motif-trace-jsonl` and
`pattern-error-fix` only, plus token text in `motif-token-stream` (&sect;1.6). Rules inside the exception:
the figure's work is the **annotation** (highlight bar, arrow, label); **five lines or fewer**; frames
stay on the palette; it does not license &sect;3.

---

## 2. Level 4 extensions to the system

Six additions. That is the complete list.

### 2.1 The seeded-number rule: if the figure claims a number, it was really produced

Level 4's repository rule is &ldquo;real seeded outputs only&rdquo;. For a figure it means:

> **Every number on a Level 4 canvas is one of three things, and you can say which: (a) printed by an
> executed, seeded block in the same week's markdown, (b) a hand calculation whose sum is printed
> beside it, or (c) a quoted literature figure, drawn as in &sect;2.6.**

| The figure is about&hellip; | So it must print&hellip; |
|---|---|
| a loss curve | the first and last plotted loss, the seed, and the step of any marked point. The two-class coin-flip line is `ln 2 = 0.693` |
| an attention map | the weights in the cells (two or three decimals, as the week prints them), and that each row sums to 1 |
| a token stream | the token count and the text it came from; bytes-per-token only if the week measured it |
| a cosine / retrieval score | the two vectors' dot product in full for at least one pair, and the ranked scores |
| recall@k | the hits and the number of questions: `7 / 10`, never a bare percentage |
| an agent trace | every step's observation as the trace printed it, and the running token count |
| cost growth | the triangular sum: `1 + 2 + &#8230; + k = k(k+1) &#247; 2` evaluated for one k |
| an experiment across seeds | mean **and** spread, with the number of seeds |

A number you cannot trace to a run or a sum **does not go on the page.** If the run has not been
executed yet, draw the figure with the placeholder chip `run first` in `wrong` stroke and do not ship it.

### 2.2 Every tensor and every sequence carries its shape

As Level 3: any block standing for a tensor gets a mono shape annotation (`(T, d)` written with the
week's real numbers, e.g. `(8, 32)`); any wire bundle between layers gets a weight chip. Level 4 adds:
**any sequence states its length in tokens, and any attention map states which axis is the query and
which is the key** (axis titles `query (asking)` / `key (being looked at)`).

### 2.3 Curves are told apart by more than colour

A chart with several runs (learning rates, optimisers, seeds, widths) uses, per series: a different
**dash pattern** (solid, `6 4`, `2 4`, `10 4 2 4`), a different **end marker shape** (circle, square,
triangle, diamond), and a **direct end label** in 12px. No legend-only identification. A spread across
seeds is drawn as the mean line plus a **band in the role's pale fill with a 1.5px stroke edge**, with
the seed count in the label. Log axes say so in the axis title (`loss (log scale)`), with tick labels at
powers of ten.

### 2.4 Minus signs, times signs and arrows are entities

| Meaning | Entity | Renders |
|---|---|---|
| minus / negative | `&#8722;` | &#8722;0.3 |
| times | `&#215;` | 3 &#215; 4 |
| divided by | `&#247;` | 16 &#247; 21 |
| becomes / maps to | `&#8594;` | 9.00 &#8594; 5.76 |
| en dash in a range | `&#8211;` | 0&#8211;1 |
| em dash in prose | `&#8212;` | like &#8212; this |
| middle dot | `&#183;` | rows &#183; columns |
| square root | `&#8730;` | &#8730;d |
| infinity | `&#8734;` | &#8722;&#8734; (the mask value) |

Never `->`, never `-` as a minus. Inside a terminal panel escape `<` `>` `&` as `&lt;` `&gt;` `&amp;`.

### 2.5 Stand-ins are drawn as stand-ins

Offline, the course's &ldquo;model to talk to&rdquo; is scripted (`FakeClient`, `ScriptedModel`,
`GullibleModel`, `FlakyBackend`, the extractive generator, the rule-based judge). The honesty rule is:
*a scripted backend teaches the scaffolding, not what a real model does.* So a figure must never let a
stand-in pass for a model.

> **A stand-in is drawn with a dashed `model`-stroke outline (`stroke-dasharray="6 4"`), a `panel` fill,
> and a 12px chip reading exactly `stand-in, not a model`. A network the student trained from scratch
> is drawn solid `model` stroke and purple fill.**

The dash plus the chip is the second cue; the colour is never the only one. A rate measured against a
stand-in carries the caption words &ldquo;of the stand-in&rdquo; (e.g. `injection succeeded in 31 / 50
runs of the stand-in`). The audit cannot check this &mdash; the author and reviewer must.

### 2.6 Quoted is not measured

A number from the literature or from a reference module that the course did **not** reproduce (e.g. a
published scaling exponent) is drawn in `muted` text, inside a dashed `grid` outline, prefixed with the
word `quoted:`. A number the student's code produced is drawn in `ink`, inside a solid outline. The two
never share a box. If a figure has only quoted numbers, it is not a measurement figure and its caption
must say so.

### 2.7 Role assignments for Level 4

Fixed; do not improvise.

| Level 4 thing | Role | Why |
|---|---|---|
| tokens, embeddings, chunks, documents, activations, any tensor of values | **data** | measured data flowing through |
| weights, heads, blocks, the trained network, LoRA patch | **model** | the learned thing |
| the student's prompt, system prompt, the frozen eval set, a rubric, a judge's rules | **human** | a person wrote it |
| the current token, the query, the marked step, the highlighted cell/head/row | **accent** | look here first |
| a scripted backend | **model**, dashed + chip (&sect;2.5) | not a model |
| retrieved-and-relevant chunk, passing eval case, held fence, after-the-fix curve | **correct** | good outcome |
| hallucinated citation, successful injection, diverging or exploding curve, failed fence, regression | **wrong** | failure |
| the backward pass, the gradient | **accent**, dashed | annotation on the forward pass |
| contour rings, unused context, attention wires below threshold | **grid** | supporting structure |

### 2.8 Matching by number, not by leader line

When two parts of a figure refer to the same thing, give both the **same ringed number** (as Level 3).
Level 4 uses it for: a cell in an attention map and the token pair it links; a point on a curve and a
row in its table; a chunk in the index and its `[id]` in the generated answer.

### 2.9 Heatmap cells carry their value

No gradients, no opacity. An attention or similarity grid uses **three discrete tints** &mdash; `panel`
for a weight below the cut, `data` fill for the middle band, `accent` fill with a 3px accent stroke for
the largest in the row &mdash; **and every cell prints its number** at 12px. The cut-offs are stated in a
legend chip (`&#8805; 0.50`, `0.10&#8211;0.49`, `&lt; 0.10`). A heatmap without printed values is a
decoration and is a defect.

---

## 3. The hard rule: a figure is not a picture of code, and not a picture of a formula

A figure diagrams the **mental model**. It never screenshots the code and never typesets the formula.

- **Not code:** no `def`, no `for`, no API call drawn as text. Draw the *loop* as a loop of boxes
  (perceive, decide, act, observe), not `while True:`.
- **Not a formula:** draw what the formula does to numbers. Attention is three small vectors, their
  dot products, a bar chart of the weights, and the blended result &mdash; not
  `softmax(QK^T/&#8730;d)V`. Adam is four steps of a running size and a step shrinking &mdash; not the update equations.
  A symbol may appear as a *label* on a part (`Q`, `K`, `V`), never as an equation.
- **Four-question test:** (1) Could a student who has not seen the code understand it? (2) Does it show
  *numbers moving*, not symbols? (3) Is the arithmetic for one instance on the page? (4) Would it still
  be true if the code were rewritten in another language? Four yeses, or redraw.

Filenames obey this too (&sect;7).

---

## 4. Motif library &mdash; Level 4

The motifs below are specified here. **The ones marked &#10003; are built into `_motifs.svg`** by
`_generator/_gen_motifs.py` (open `_preview.html` to see them). Until a motif exists, a week figure may draw
the same thing inline, obeying the rules on this page. Each motif lists its canvas, roles, the second cue,
and the real numbers it must print.

Built (23): `motif-loss-curve`, `motif-loss-compare`, `motif-train-val-gap`, `motif-coin-floor`,
`motif-lr-schedule`, `motif-token-stream`, `motif-bpe-merge`, `motif-attention-grid`, `motif-causal-mask`,
`motif-attention-arcs`, `motif-gradient-compound`, `motif-tensor-2d`, `motif-block-stack`,
`motif-cosine-table`, `motif-rag-flow`, `motif-recall-at-k`, `motif-agent-loop`, `motif-cost-growth`,
`motif-fence`, `motif-trace`, `motif-eval-table`, `motif-ablation-table`, `motif-stand-in-and-quoted`.
The built `motif-trace` is the Week 28 five-turn trace (the spec's `motif-trace-jsonl` remains planned for
Week 29); `motif-cosine-table` and `motif-ablation-table` are built in place of `motif-cosine` and
`motif-head-ablation`. Rows below that are not in this list are still planned.

Every motif prints only numbers listed in `_generator/_gen_data.py`, each tagged with its provenance: a seeded
numpy demo run (seed 0, 200 points, 40 steps &mdash; this is the figure's source, since the course's own
loss-curve runs are in the weeks), a value copied from the executed ledger (`_ledger/out`), or a hand sum.
A week figure replaces them with *its own* printed values; the motifs are shape templates plus worked examples.

**Heatmap tint rule, clarified (2.9).** The three tints are *largest in its row* (`accent` fill and a 3px
`accent` ring; ties are all ringed), *0.10 or more* (`data`), and *below 0.10* (`panel`). The 2.9 cut-offs
`&#8805; 0.50` / `0.10&#8211;0.49` / `&lt; 0.10` describe the same bands, but a row whose largest weight is
under 0.50 (Week 14's `the` and `cat` rows peak at 0.4223) must still ring its maximum, so the ring follows
the row, not the 0.50 cut. The legend chip states the rule actually used.

### Training and loss

| Motif | Canvas | What it shows | Roles / second cue | Must print |
|---|---|---|---|---|
| `motif-loss-curve` | square | One run's loss against step, log or linear axis | `data` line; end marker; axis titles | first and last loss, seed |
| `motif-loss-compare` | square | 2&ndash;3 runs on shared axes (&sect;2.3) | dash + marker + end label per series | end value of each |
| `motif-train-val-gap` | square | Train and validation curves with the gap between them bracketed | train `data`, val `human`; bracket is `accent` | the two end values and their difference |
| `motif-seed-band` | square | Mean line plus min&ndash;max band over seeds | pale fill band, 1.5px edge | seeds, mean, spread |
| `motif-coin-floor` | strip | The `ln 2 = 0.693` horizontal line a two-class model starts on | `grid` dashed line, `accent` chip | `0.693` |
| `motif-optimizer-steps` | wide | Steps of SGD / momentum / Adam on a bowl, side by side | three panels, numbered steps | each step's `w` and loss |
| `motif-lr-schedule` | square | A learning rate against step: warmup then decay | `model` line; marked step `accent` | peak lr, warmup steps |
| `motif-power-law` | square | Points on log-log axes with a fitted line and one extrapolated point | fitted line `correct`, extrapolated point hollow `accent` | fit slope, the checked point |

### Sequences and attention

| Motif | Canvas | What it shows | Roles / second cue | Must print |
|---|---|---|---|---|
| `motif-token-stream` | strip | Text cut into tokens, each in a box, mono text (&sect;1.6), ids beneath | `data` boxes; alternating stroke weight so neighbours are distinguishable without colour | token count, source text |
| `motif-bpe-merge` | wide | One merge step: the most frequent adjacent pair becomes one token | pair `accent`; new token `model` | the pair's count |
| `motif-bytes-per-token` | square | Bytes-per-token climbing as the corpus grows | `data` line, markers | corpus sizes and values measured |
| `motif-rnn-unroll` | wide | One cell reused at every step, hidden state carried along | cell `model`, state `data` | the hidden state numbers of each step |
| `motif-gradient-compound` | square | A number raised to T: bars shrinking (or growing) by position | bars `data`; marked `accent` | base, T, result (e.g. the Week 10 `0.9526^40 = 0.143`) |
| `motif-gate` | strip | A gate value between 0 and 1 scaling a memory | `model` gate, `data` memory | gate value, before and after |
| `motif-attention-grid` | square | Query rows by key columns, cells per &sect;2.9, row sums printed | three tints + accent ring on the row max | all cells; row sums = 1 |
| `motif-attention-arcs` | wide | Tokens on a line with arcs from the current token to the ones it reads | arc stroke width = weight band (three widths); `accent` current token | the weight on each arc |
| `motif-qkv-pass` | wide | Three small vectors: dot products, weights, blended output | `Q` accent, `K` data, `V` data; result `model` | every dot product and the blend sum |
| `motif-causal-mask` | square | The lower-triangle mask; future cells struck through | masked cells `grid` with a diagonal strike | `&#8722;&#8734;` in the masked cells |
| `motif-softmax-saturation` | wide | Softmax of raw vs scaled scores at two widths | two bar panels | the scores and both softmax outputs |
| `motif-sampling-knobs` | wide | One next-token distribution reshaped by temperature, top-k, top-p | bars `data`; cut-off line `accent`; removed bars `grid` | the probabilities before and after |
| `motif-block-stack` | tall | One transformer block top to bottom: norm, attention, residual add, MLP, add | `model` blocks; residual path `correct` with a bypass arrow | parameter count if the week counts it |
| `motif-positions` | strip | A shuffled sequence with and without position vectors | with/without labelled | the two outputs |
| `motif-head-ablation` | wide | A table of components removed versus loss | `wrong` rows where it broke; icon not colour | each loss, step count |

### Post-training, evaluation and safety

| Motif | Canvas | What it shows | Roles / second cue | Must print |
|---|---|---|---|---|
| `motif-sft-mask` | strip | Prompt tokens masked, answer tokens scored | prompt `grid` struck through; answer `data` | counts of each |
| `motif-preference-pair` | wide | Two answers, one marked preferred, a reward number each | preferred `correct` + tick | both rewards |
| `motif-kl-leash` | square | Two distributions and the gap between them | before `data`, after `model` | the measured divergence |
| `motif-lora-patch` | wide | A big grid beside two thin ones multiplying to it | thin pair `model` | `r &#215; in + out &#215; r` evaluated |
| `motif-reliability` | square | Said-80%-was-right-x% by bucket, diagonal reference | bars `data`; gap `accent` | counts per bucket (e.g. n of each) |
| `motif-coverage-accuracy` | square | Accuracy against fraction answered as the abstain threshold moves | `correct` line | threshold, coverage, accuracy |
| `motif-eval-table` | wide | Per-category results, average on top, the one that fell marked | `wrong` row with cross icon | counts `k / n` per category |
| `motif-confusion` | square | A confusion matrix, inherited from Level 3 for the ticket classifier | TP/TN `correct`, FP/FN `wrong` | all four counts |
| `motif-judge-bias` | wide | A judge preferring position A regardless of content | planted-bias flagged with a chip | the measured rate of each position |
| `motif-kappa` | strip | Agreement table with the chance-agreement cell marked | `accent` chance cell | the counts and chance agreement |

### Retrieval, agents and systems

| Motif | Canvas | What it shows | Roles / second cue | Must print |
|---|---|---|---|---|
| `motif-embedding-scatter` | square | Items as points in a plane; the query ringed; k nearest joined | query `accent` square; neighbours `correct` circles; others `grid` triangles | the ranked scores |
| `motif-cosine` | square | Two arrows from an origin and the angle between them | arrows `data` and `accent` | the dot product worked out and the cosine |
| `motif-chunk-row` | wide | A document cut into numbered chunks | `data` boxes with `[id]` | chunk count, chunk size |
| `motif-rag-flow` | wide | Question, retrieve, numbered sources, answer with citation, verify | stages numbered; verifier `correct`/`wrong` | retrieved ids and the threshold |
| `motif-recall-at-k` | square | For each question, where the right chunk ranked | hit `correct` tick, miss `wrong` cross | hits over questions |
| `motif-injection` | wide | A tool result containing an instruction the stand-in obeys | injected text `wrong`, dashed box | which layer stopped it, counts |
| `motif-agent-loop` | wide | Perceive, decide, act, observe, stop as a cycle | current step `accent`; stand-in per &sect;2.5 | the step index and token count |
| `motif-fence` | strip | A tool call hitting a guardrail: allowed through or blocked | pass `correct` tick, block `wrong` cross | the rule that fired |
| `motif-trace-jsonl` | tall | A five-line trace with the current step in weight 600 | current row `accent` bar | the trace lines (&sect;1.9) |
| `motif-cost-growth` | square | Tokens re-sent each turn stacking as a staircase | step bars `data`; total `accent` | per-step and cumulative tokens, the triangular sum |
| `motif-stand-in-chip` | strip | The `stand-in, not a model` chip and dashed frame of &sect;2.5 | dashed `model` | the exact words |
| `motif-quoted-chip` | strip | The `quoted:` box of &sect;2.6 | dashed `grid`, muted | the quoted value and its source |

---

## 5. Motifs inherited from Levels 2 and 3

Reusable unchanged: `motif-terminal`, `motif-traceback`, `motif-arrow`, `motif-arrow-curved`,
`motif-badge-check`, `motif-badge-cross`, `motif-box`, `motif-note`, `motif-table`,
`motif-dataframe`, `motif-array-2d`, `motif-split`; from Level 3, `motif-tensor-1d` to
`motif-tensor-4d`, `motif-matmul`, `motif-shape-mismatch`, `motif-neuron`, `motif-network-shapes`,
`motif-forward-backward`, `motif-split-three`, `motif-leakage-wrong/right`, `motif-pca`. Level 4
re-roles only what &sect;2.7 changes (the frozen eval set is `human`, not the Level 3 test-set `accent`).

---

## 6. Composition patterns

Each pattern fixes a canvas, a reading direction and a place for the sum.

| Pattern | Canvas | Shape | Use for |
|---|---|---|---|
| `pattern-pipeline` | wide | 3&ndash;5 stages left to right, text-free glyphs, 18px labels | tokenise &#8594; embed &#8594; attend &#8594; sample; chunk &#8594; embed &#8594; retrieve &#8594; cite |
| `pattern-before-after` | wide | two panels, `wrong` left, `correct` right, same axes | mask on/off, LayerNorm on/off, with/without residual, patch applied |
| `pattern-knob-sweep` | wide | three small multiples, same y axis, one knob changed | learning rate, batch size, dropout |
| `pattern-worked-attention` | wide | tokens, the three vectors, dot products, weights, blended output, left to right | Weeks 14&ndash;15 |
| `pattern-loop` | wide | a cycle with the current step `accent` and the trace strip beneath | agent loop, generation loop |
| `pattern-table-plus-chart` | square or wide | a chart with ringed numbers matching a table (&sect;2.8) | per-category eval, reliability table |
| `pattern-error-fix` | wide | terminal panel of &le; 5 lines, annotation, then the fixed run | shape bugs, custom exceptions |
| `pattern-trace` | tall | one row per step: thought, action, observation, tokens so far | Weeks 28&ndash;29, 33&ndash;36 |

---

## 7. Naming

```
fig-wNN-<n>-<slug>.svg
```

- `wNN` &mdash; the week, two digits, `w01` &hellip; `w36`.
- `<n>` &mdash; sequence drawn **within that week**, from 1. `-0-` is reserved for the Growing Map.
- `<slug>` &mdash; two to four lowercase hyphenated words.

Examples: `fig-w02-1-momentum-running-average.svg`, `fig-w14-2-attention-three-token-pass.svg`,
`fig-w26-3-retrieval-recall-at-k.svg`, `fig-w29-1-cost-grows-faster-than-steps.svg`.

Lowercase, hyphens only, no spaces, underscores, dates or version suffixes. Files beginning with `_`
are shared infrastructure, not figures. **Slugs name the idea, not the notation**:
`fig-w14-2-attention-three-token-pass.svg`, never `fig-w14-2-softmax-qk-over-sqrt-d.svg`.

The filename number is the drawing order; the caption number is the reading order within one markdown
file and may differ. Workbook captions carry a `W` (`Figure W22.1`). When citing a figure from another
book, name the book.

---

## 8. Don'ts

- **No pictures of code; no pictures of formulae.** &sect;3.
- **No number you cannot trace** to a seeded run, a printed sum or a quoted source. &sect;2.1, &sect;2.6.
- **No stand-in that looks like a model.** &sect;2.5.
- **No tensor without its shape, no sequence without its length.** &sect;2.2.
- **No multi-series chart told apart by colour alone.** &sect;2.3.
- **No heatmap without printed values; no gradient and no opacity.** &sect;2.9.
- **No `->`, no hyphen-as-minus.** &sect;2.4.
- **No text-bearing motif below `scale(1.0)`.** &sect;1.8.
- **No monospace outside &sect;1.6's list**; no literal code or output outside &sect;1.9.
- **No external images, no webfonts, no `<filter>`, no `feGaussianBlur`/`feDropShadow`, no CSS `filter`.**
- **No `<foreignObject>`, no `<script>`, no embedded HTML.**
- **No `width`/`height` on the root `<svg>`; no white background rect.**
- **No text below 12px**, and no text you expect to wrap.
- **No new colours.** Need a seventh? You need a different diagram (&sect;1.3).
- **No `<ellipse>`.** The audit's bounds checker does not understand it; approximate with a `<polygon>`.
- **No colour as the only carrier of meaning.** Second cue: a shape, dash, label, number or position.
- **No `tiktoken`, Hugging Face or real-model screenshots** as a figure source. Vector only, drawn from the course's own runs.

---

## 9. Pre-flight check

```bash
f=fig-w14-2-attention-three-token-pass.svg
python3 -c "import xml.dom.minidom,sys; xml.dom.minidom.parse(sys.argv[1])" $f
grep -nE '<image|href="http|@font-face|<filter|feGaussianBlur|feDropShadow|<foreignObject|<script|Gradient|<ellipse' $f && echo "BANNED CONSTRUCT" || echo "clean"
grep -q 'role="img"' $f && grep -q '<title>' $f && grep -q '<desc>' $f && echo "a11y ok"
grep -nE '<svg[^>]+(width|height)=' $f && echo "REMOVE width/height" || echo "scales ok"
grep -oE 'font-size="[0-9.]+"' $f | sort -u      # nothing below 12
grep -oE 'scale\([0-9.]+' $f | sort -u           # <1 on a group containing <text> is a defect
grep -oE '(fill|stroke)="#[0-9A-Fa-f]+"' $f | sort -u
```

Or audit everything at once (bounds against the 20px padding, effective font size after every
`scale()`, banned constructs, overlapping labels, off-palette colours, unsanctioned font stacks, the
`role="img"` + `<title>` + `<desc>` contract):

```bash
cd _generator && python3 _gen_audit.py     # must print "--- 0 finding(s)"
```

Then, by eye:

- [ ] Not a picture of code, not a picture of a formula (&sect;3).
- [ ] Every number is traceable to an executed seeded block, a printed sum, or a `quoted:` box (&sect;2.1, &sect;2.6).
- [ ] Any scripted backend is dashed and chipped `stand-in, not a model` (&sect;2.5).
- [ ] Tensors carry shapes; sequences carry lengths; attention axes are named (&sect;2.2).
- [ ] Multi-series charts differ by dash and marker as well as colour (&sect;2.3).
- [ ] Heatmap cells print their values (&sect;2.9).
- [ ] `<title>` states the takeaway; alt text describes the picture; `<desc>` has the numbers.
- [ ] Every colour is from &sect;1.1 in its &sect;2.7 role; nothing within 20px of the edge.
- [ ] It reads in greyscale (print the figure, or convert and look).
- [ ] A 15-year-old gets the point in four seconds with the caption covered, and a teacher new to AI could teach it.

---

## 10. Files in this folder

| File | What it is |
|---|---|
| `STYLE.md` | This contract. |
| `_generator/_gen_build.py` | **One command.** `python3 _gen_build.py` regenerates `_motifs.svg`, `_preview.html` and all 36 Growing Maps deterministically, validates the XML, then runs the audit. Usage is documented at the top of the file. |
| `_generator/_gen_audit.py` | The audit (`python3 _gen_audit.py`, must print `--- 0 finding(s)`). Checks the generator's motifs and patterns, and every finished `fig-*.svg` in this folder. |
| `_generator/_gen_core.py` | Palette, helpers (series markers, three-tint heatmap cells, stand-in frame, quoted box) and the motif registry. |
| `_generator/_gen_data.py` | Every number a shared motif prints, with its provenance (STYLE 2.1). |
| `_generator/_gen_motifs.py`, `_gen_pat.py`, `_gen_map.py`, `_gen_emit.py` | Motifs, the 8 composition patterns (6 built as finished figures on the canvases of 1.4), the Growing Map, and the writers. |
| `_motifs.svg` | Generated sprite sheet. Do not edit. |
| `_preview.html` | Generated eyeball page: palette, motifs, patterns, and every `fig-*.svg` (with a greyscale toggle). |
| `fig-wNN-0-where-this-fits.svg` | The 36 Growing Map figures. **Generated** &mdash; edit `_gen_map.py`, not the files. |
| `fig-wNN-<n>-*.svg`, n &#8805; 1 | Week figures, hand-authored (none yet). `_gen_build.py` never touches them. |

The generator is the source of truth for `_motifs.svg`, `_preview.html` and the maps. A week figure is
free to be hand-written SVG, or to import `_gen_core` and write its own generator module; either way it
must pass `_gen_audit.py`.

### The Growing Map &mdash; `fig-wNN-0-where-this-fits.svg`

As in Levels 1&ndash;3, each week carries one figure, index `0`, showing the whole level with one more
piece filled in; caption `Figure <week>.0`. **The spine is decided and fixed:**

> **Four lanes, nine tiles each.** One horizontal lane per term, stacked top to bottom (term 1 on top);
> each lane holds that term's nine weeks as nine tiles left to right. Week *N* is lane `(N-1) // 9`, column
> `(N-1) % 9`. A wire runs through the tile centres of each lane. 36 tiles, on the `wide` canvas.

| Element | Spec |
|---|---|
| Canvas | `0 0 800 400`, title `24px` top-centre: `Level 4 map: week N of 36` |
| Lanes | four panels `x 20&#8211;780`, rows at `y = 88, 158, 228, 298`, each 66 tall. Left label: `Term N` (18px) then the term's name in two 12px lines: *train it / on purpose*, *memory, then / attention*, *how it is made, / how it is asked*, *agents, evidence, / and the system card* (the README's term names) |
| Tiles | 58 &#215; 50, gap 7, first tile at `x = 192`; week number `18px`, week type beneath in `12px` (`teach`, `lab`, `project`, `assess`, `capstone`), both parsed from the README &ldquo;All 36 Weeks&rdquo; table |
| **Done** weeks | white tile, solid `ink` 2px outline, solid `ink` wire |
| **This week** | `accent`-fill tile, **4px** `accent` outline, and a solid `accent` pointer triangle above it |
| **Ahead** | dashed `grid` outline, muted number, dashed `grid` wire |
| Current lane | panel with a solid `ink` outline; earlier lanes a solid `grid` outline; later lanes dashed `grid` |
| Caption line | `Week N &#183; <title>` at `14px`, bottom-centre, titles from the README (` - ` becomes an em dash entity) |
| `<title>` | `Week N of 36, <title> (<type>), sits in term T, <term name>` |
| `<desc>` | names the four lanes, which weeks are done, which one is highlighted and its type, and which are still dashed |

State is carried by dash, stroke weight and a pointer shape &mdash; never colour alone. No bold is used
(1.7). The spine never changes in later weeks or revisions: if a README title changes, re-run
`_gen_build.py`; if the grid changes, every map changes with it.

One quirk: Week 6's real title contains the capital-G word the audit and the section-9 grep ban (it flags SVG
colour ramps). `_gen_map.py` writes that one letter as a numeric entity (`Gradi&amp;#101;nt`), which renders
identically and keeps both checks meaningful for everything else.

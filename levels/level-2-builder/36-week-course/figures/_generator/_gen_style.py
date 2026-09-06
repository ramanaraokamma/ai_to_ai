"""Emit STYLE.md from the same source of truth as _motifs.svg and _preview.html."""
import os
from _gen_core import MOTIFS
from _gen_pat import PATTERNS, EXAMPLES
from _gen_emit import pattern_svg, NEW, OLD, HERE


def dims(vb):
    v = vb.split()
    return v[2], v[3]


def motif_block(m):
    w, h = dims(m["vb"])
    return ("### `%s` &mdash; %s\n\n"
            "viewBox `%s` (%s&times;%s). %s\n\n"
            "**Use it for:** %s\n\n"
            "```svg\n<g transform=\"translate(0,0)\">\n%s\n</g>\n```\n"
            % (m["id"], m["title"], m["vb"], w, h, m["desc"], m["note"], m["body"]))


def pattern_block(p):
    return ("### `%s` &mdash; %s\n\n**Canvas** `%s`. %s\n\n```svg\n%s\n```\n"
            % (p["id"], p["title"], p["vb"], p["note"], pattern_svg(p)))


DOC = r"""# Figure style system &mdash; AI Academy, Level 2 &ldquo;Builder&rdquo; (36-week course)

**Audience: the authors drawing the SVG figures for Level 2.**
This file is the contract. If your figure disagrees with this file, this file wins.

**Level 2 is a faithful extension of Level 1, not a new system.** A parent flipping between the two
years should not be able to tell where one ends and the other begins. Same palette, same stroke
widths, same type scale, same accessibility rules. Everything inherited is copied out in full below
so this file stands alone &mdash; you never need to open Level 1's `STYLE.md` to draw a Level 2 figure.

What is genuinely new is the *subject matter*: Level 2 has **code and data** on the screen.
So there are new motifs (variables, lists, dicts, loops, DataFrames, arrays, tracebacks) and
one new rule that matters more than any other &mdash; **&sect;3, a figure is not a picture of code.**

**The learner is one 12-year-old who has never written a line of code. The teacher knows neither
AI nor Python and opened this week's file 20 minutes ago.** A figure has to land in about four
seconds with no caption. That is the bar, and it is harder than Level 1's bar.

---

## 0. The 30-second version

1. Copy a **composition pattern** (&sect;6) that matches your diagram type.
2. Drop in **motifs** (&sect;4, &sect;5) &mdash; do not draw your own DataFrame.
3. Use only the eight **palette** colours (&sect;1.1), by *role*, never by taste.
4. **Do not draw the code.** Draw the idea underneath the code (&sect;3).
5. Start every file with `role="img"`, then `<title>`, then `<desc>` (&sect;1.5).
6. Name it `fig-wNN-<n>-<slug>.svg` (&sect;7).
7. Run the pre-flight check (&sect;9) before you commit.

---

## 1. Inherited verbatim from Level 1

Nothing in this section may be changed. The values are reproduced, not summarised.

### 1.1 Palette &mdash; eight colours, used by role

Each role has a **stroke** (outlines, text, marks) and most have a **fill** (the pale tint inside a
shape). This two-tier split is deliberate and load-bearing &mdash; see &sect;1.2.

| Role | Stroke | Fill | Contrast on white | Greyscale (stroke) | Greyscale (fill) | Use it for |
|---|---|---|---|---|---|---|
| **data** | `#1F6FB2` | `#D9EAF9` | 5.28:1 | 108 | **232** | Data, values, tables, arrays, inputs, anything measured |
| **model** | `#6D28D9` | `#DBCEF3` | 7.10:1 | 88 | **212** | The model, the learned thing, the fitted estimator |
| **human** | `#845F00` | `#E8C671` | 5.80:1 | 101 | **202** | People, choices a person made, notes, cleaning-log entries |
| **correct** | `#1B7A4B` | `#E2F7ED` | 5.34:1 | 107 | **242** | It ran, it passed, after the fix, good outcomes |
| **wrong** | `#CC2B1D` | `#F6AEA6` | 5.34:1 | 107 | **192** | Errors, tracebacks, before the fix, warnings |
| **accent** | `#C42B8C` | `#F4D5E9` | 5.16:1 | 109 | **222** | Callout numbers, the current item, the held-out test set, the one thing to look at first |
| **ink** | `#14202B` | &mdash; | 16.52:1 | 31 | &mdash; | All body text, neutral outlines, arrows |
| **paper** | `#FFFFFF` | &mdash; | &mdash; | 255 | &mdash; | Nothing. It is the background you never draw. |

Three supporting neutrals (not &ldquo;colours&rdquo;, they carry no meaning):

| Name | Hex | Contrast on white | Greyscale | Use it for |
|---|---|---|---|---|
| **muted** | `#55636F` | 6.18:1 | 97 | Captions, axis numbers, secondary labels |
| **grid** | `#C7CDD4` | 1.60:1 | 204 | Grid lines, dashed dividers, panel outlines |
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
- **data (232) vs accent (222)** is the Level 2 pair that matters most: **train vs test.** Only 10
  levels apart, so train and test must ALWAYS also differ by size, position or a printed count.
  Never rely on blue-vs-pink alone to say which pile is the test set.

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
| **correct / wrong** | **28.4** | **9.1** | **pass** &mdash; the safety-critical pair |
| correct / accent | 32.3 | 8.7 | pass |
| **data / model** | **17.7** | **8.4** | **pass** &mdash; the pipeline pair |
| **data / accent** | **26.2** | **8.3** | **pass** &mdash; the train/test pair, and the weakest passing one |
| wrong / accent | 14.8 | 14.1 | **needs shape + label** |
| human / correct | 13.2 | 6.7 | **needs shape + label** |
| human / wrong | 16.3 | 4.7 | **needs shape + label** |

**Charts: at most three role colours.** For any chart where marks are compared all against all,
pick one of these validated triples: `data + correct + wrong` (the usual choice), `model + correct +
wrong`, `data + model + human`, or `model + human + accent`. Need a fourth category? Fold it into
&ldquo;Other&rdquo;, or split into two charts. Do not invent a seventh colour.

### 1.4 Canvas rules

| Name | viewBox | Use for |
|---|---|---|
| **wide** | `0 0 800 400` | Pipelines, before/after, three-panel progressions, error-and-fix pairs, trees |
| **square** | `0 0 500 500` | Charts, single-idea diagrams, data-structure close-ups |
| **tall** | `0 0 500 700` | Step-by-step stacks, long trees, call stacks, long tables |

- **Never set `width` or `height` on the root `<svg>`.** viewBox only, so the figure scales to
  whatever column it lands in, in print or on screen.
- **20px of internal padding.** Nothing except a deliberate full-bleed background touches the edge.
  On a wide canvas your live area is x 20&ndash;780, y 20&ndash;380.
- **Transparent background.** Do not paint a white rect over the canvas &mdash; it breaks dark mode
  and wastes ink. If you want a tinted panel, use `panel` `#F5F8FA` on a rounded rect *inside* the
  padding.
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
| Grid lines, dividers, leader lines | `stroke-width="1.5"` |
| Emphasis marks (tick, cross) | `stroke-width="6"` |
| Line caps | `stroke-linecap="round"` on every open path |
| Line joins | `stroke-linejoin="round"` on every stroked polygon or rect |
| Box corners | `rx="8"` small boxes, `rx="10"` standard, `rx="12"` large panels |

The **soft hand-drawn feel** comes from round caps, round joins and generous corner radii &mdash;
**not** from wobble, texture or filters. Keep geometry exact; the roundness does the warmth.

- **Draw connectors first, boxes second.** Then lines tuck under boxes instead of crossing them.
- **A stroke's job is the edge; a fill's job is the tint.** Every meaningful shape gets both.

**System fonts only. Never a webfont, never `@font-face`, never Google Fonts.**

```
font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
```

| Level | Size | Colour | Use |
|---|---|---|---|
| Title | `24` | `ink` | One per figure, top-centre |
| Label | `18` | `ink` | Names of boxes, stages, axes |
| Caption | `14` | `muted` | The one-line takeaway at the bottom |
| Tiny | `12` | `muted` | Axis numbers, cell values, index labels, legend text |

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
  point*, not the shapes. For a code figure, describe the **idea**: &ldquo;a counter reading i equals
  2 sits beside four numbered slots with slot 2 highlighted&rdquo;, never &ldquo;a for loop&rdquo;.
- **The markdown alt text must agree with `<title>`.** Every markdown file in `teacher-guide/`,
  `student-guide/` and `workbook/` sits one directory below `figures/`, so the link always starts
  `../figures/`, and every embed gets an italic caption line numbered `Figure <week>.<n>`:

```markdown
![A variable is a labelled box](../figures/fig-w02-1-variable-as-box.svg)
*Figure 2.1 — A variable is a labelled box. The name is the label, not the box.*
```

  If a teacher reads the alt text aloud, the class should still follow.
- Decorative motifs *inside* a figure need nothing extra &mdash; the parent `<desc>` covers them.
- If you `<use>` a motif standalone, label it: `<use href="_motifs.svg#motif-list" aria-label="A list as numbered slots"/>`.

---

## 2. Level 2 extensions to the system

Five additions. That is the complete list; do not invent a sixth.

### 2.1 A monospace stack, for code tokens and program output only

Level 2 has to show tokens (`price`) and output (`hello, world`). Setting those in a proportional
font is a lie &mdash; alignment is part of what the learner is being taught to see. So there is a
second, and last, font stack:

```
font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
```

It is still **system fonts only**, so nothing about &sect;1.5 is waived. Rules:

- Use it **only** for: a code token in a callout, a line inside a terminal or traceback panel, a
  filename, a `shape (3, 4)` annotation. Never for a title, a label, a caption or an axis.
- **The 12px floor still applies**, and mono runs wider than sans at the same size, so budget
  `chars &times; fontSize &times; 0.6` for the width and check it fits.
- Program output is 14px; traceback lines are 12px.

### 2.2 One extra canvas: `strip`

| Name | viewBox | Use for |
|---|---|---|
| **strip** | `0 0 800 260` | A single code line with a callout, one terminal panel, one before/after row |

Same 20px padding, same rules. Use it instead of leaving the bottom half of a `wide` canvas empty.

### 2.3 `font-weight="600"` is allowed, in exactly one place

A DataFrame's header row must read as a header. `font-weight="600"` is permitted on **table and
DataFrame header cells, and on the last line of a traceback**. Nowhere else &mdash; not for emphasis,
not for titles. Titles are already 24px; that is the emphasis.

### 2.4 The scaling rule: `scale()` scales the type too

This is the trap Level 2 authors fall into, because Level 2 motifs carry text and Level 1's mostly
did not. `<g transform="scale(0.5)">` around a motif whose labels are 12px produces **6px type**,
which violates the floor and cannot be photocopied.

> **Never place a text-bearing motif at `scale()` below 1.0.**

If the box is too small for the motif at 1.0, you have two legal moves:

1. **Use a text-free glyph** and put the words in the surrounding 18px stage label. This is what
   `pattern-pipeline` (&sect;6.1) does, and why its stage glyphs carry no text of their own.
2. **Make the box bigger**, or split the figure in two.

Text-free motifs (`motif-arrow`, `motif-badge-check`, `motif-badge-cross`, `motif-table`,
`motif-note`, `motif-child`) may be scaled freely. Scale **uniformly** &mdash; never stretch one axis.

### 2.5 The sanctioned exception: when the artefact *is* the lesson

Level 1 had one narrow exception (painting a literal RGB value when the colour *was* the data).
Level 2's equivalent is this: **a traceback and a program's output are artefacts the learner must
learn to read.** You cannot teach &ldquo;read the last line first&rdquo; without showing the lines.

So `motif-terminal`, `motif-traceback`, `motif-code-callout` and `pattern-error-fix` may contain
verbatim monospace text. **This is the complete list of places where literal code or output may
appear.** Rules that still apply inside the exception:

- The figure's *work* is the annotation &mdash; the highlight bar, the arrow, the label. A terminal
  panel with no annotation is not a figure, it is a screenshot, and it is a defect.
- Keep it to **five lines or fewer**. If your traceback needs six lines, you are showing the program,
  not the error.
- Everything *around* the text stays on the &sect;1.1 palette: ink frames, muted captions, accent pins.
- This exception does **not** license &sect;3.

---

## 3. The hard rule: a figure is not a picture of code

> **A figure must never be a picture of code. It diagrams the mental model *behind* the code.**

The code is already on the page, in a fenced code block, in a font the reader can copy from. A
figure that repeats it adds nothing, costs a page, and &mdash; worse &mdash; teaches the learner that
programming is a shape to memorise rather than a thing to picture.

Ask this before you draw: **&ldquo;What would the learner have to imagine to predict what this code
does?&rdquo;** Draw that.

| Instead of drawing&hellip; | Draw&hellip; |
|---|---|
| the line `score = 7` | a box with a `score` label on it, holding 7 (`motif-variable`) |
| the line `score = 10` after it | two panels, the old 7 struck through (`motif-rebind`) |
| `for i in range(3):` | a circle you go round, a counter, and one slot lit up (`motif-loop`) |
| `if temp > 30:` | a fork in a path with the condition on a signpost (`motif-if-else`) |
| `def average(nums):` | a machine with a hopper on top and a chute underneath (`motif-function`) |
| `fruits[2]` | numbered slots with slot 2 ringed (`motif-list`) |
| `df["runs"]` | a grid with that one column outlined and tinted (`motif-dataframe`) |
| `arr.shape` | a block, three rows by four columns, with both axes arrowed (`motif-array-2d`) |
| `train_test_split(...)` | a deck of cards cut once, with both counts printed (`motif-split`) |

### 3.1 Worked example: the same lesson, drawn twice

The lesson is *&ldquo;a loop's counter names one item at a time, and it starts at 0&rdquo;*.

**Wrong.** This is a screenshot with a border. Everything in it is already in the code block above
it; the reader's eye has nowhere to go, and the off-by-one &mdash; the entire point &mdash; is
invisible.

```svg
BAD_EXAMPLE_SVG
```

**Right.** No code on the canvas. The counter is a number in a circle; the arrow says &ldquo;you come
back round here&rdquo;; the lit slot says which item `i` currently names; and the caption
`pass 2 of 3` under a counter reading `1` makes the off-by-one *visible*, which is the thing the
learner actually gets wrong.

```svg
GOOD_EXAMPLE_SVG
```

Note what the good figure keeps from the bad one: the words `apple`, `fig`, `plum`. **Data values are
not code.** Showing the values in the slots is what makes the diagram concrete. What it drops is the
*syntax* &mdash; the brackets, the colon, the `range(3)`.

### 3.2 The three-question test

Before you commit a figure, answer all three. Any &ldquo;no&rdquo; means redraw.

1. **Cover the code block. Does the figure still teach something?** If the figure only makes sense
   next to the code, it is decoration.
2. **Cover the figure. Does the code block lose anything?** If not, the figure is redundant &mdash;
   delete it, and spend the page on the thing the reader *cannot* see.
3. **Could a reader who has never seen Python read it?** The teacher is that reader.

---

## 4. Motif library &mdash; Level 2 (MOTIF_COUNT_NEW)

**Do not redraw these.** Consistency across the whole year is the point. Two ways to use them:

```svg
<!-- A) reference the sprite sheet -->
<use href="_motifs.svg#motif-list" x="40" y="40" width="320" height="126"/>

<!-- B) copy the <g> inline (below) and position it -->
<g transform="translate(600,150)">...</g>
```

Every motif is drawn to its own viewBox with **the origin at the top-left**, so `translate(x,y)` puts
its top-left corner at exactly `(x,y)`. Remember &sect;2.4 before you scale one.

MOTIF_BLOCKS_NEW

---

## 5. Motifs inherited from Level 1 (MOTIF_COUNT_OLD)

Copied byte-for-byte from Level 1's sprite sheet so the two years match. Reproduced here so this
folder is self-contained. `motif-machine`, `motif-brain`, `motif-robot`, `motif-magnifier`,
`motif-scale`, `motif-lightbulb`, `motif-photos` and `motif-thought` also still exist in Level 1 and
may be pulled across if a week needs them; for Level 2's own subjects prefer the &sect;4 motifs
(`motif-function` supersedes `motif-machine`; `motif-dataframe` supersedes `motif-table` whenever the
table has real content).

MOTIF_BLOCKS_OLD

---

## 6. Composition patterns

Six diagram types cover essentially every figure in this level. Start from the matching skeleton and
swap the content. Each one below is a complete, valid SVG that passes &sect;9.

| Pattern | Reach for it when |
|---|---|
| `pattern-pipeline` | Something flows through ordered stages |
| `pattern-before-after` | One thing changed and you want the reader to find it |
| `pattern-progression` | A dial was turned through three settings |
| `pattern-annotated-chart` | A chart where one mark is the story |
| `pattern-structure` | Two representations hold the same data |
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
fig-w02-1-variable-as-box.svg
fig-w09-3-loop-counter-slots.svg
fig-w21-2-dataframe-column-select.svg
fig-w33-1-overfit-three-panels.svg
```

Lowercase only, hyphens only, no spaces, no underscores, no dates, no version suffixes.
Files beginning with `_` are shared infrastructure (`_motifs.svg`, `_preview.html`), not figures.

**Slugs name the idea, not the syntax.** `fig-w09-3-loop-counter-slots.svg`, never
`fig-w09-3-for-i-in-range.svg`. The filename is the first place &sect;3 gets broken.

### 7.1 The filename number and the caption number are different numbers

| | What it counts | Example |
|---|---|---|
| **Filename `<n>`** | The order the figure was **drawn**, within its week. It never changes once assigned. | `fig-w21-4-groupby-tally.svg` was the 4th figure drawn for Week 21. |
| **Caption `<n>`** | The order the figure is **read**, within *one markdown file*. | That same figure may be `*Figure 21.2*` in the student guide and `*Figure 21.5*` in the teacher guide. |

**These two numbers usually do not match, and that is correct.** Number captions by reading order in
the file you are editing, and never renumber a file.

- **Workbook captions carry a `W`:** `*Figure W21.1*`, so a workbook figure can never be confused
  with a chapter figure of the same number.
- **When you cite a figure that lives in a different book, say which book.** Not *&ldquo;see Figure
  21.4&rdquo;* but *&ldquo;see **Figure 21.4 in the Week 21 chapter**&rdquo;*.

---

## 8. Don'ts

Everything Level 1 banned is still banned, plus four Level 2 items.

- **No pictures of code.** &sect;3. This is the one that will get a figure rejected.
- **No text-bearing motif below `scale(1.0)`.** &sect;2.4.
- **No monospace outside &sect;2.1's list.** Titles, labels, captions and axes are sans, always.
- **No literal code or output outside the four exceptions in &sect;2.5**, and never without an annotation.
- **No external images.** No `<image href>`, no PNG, no JPEG, no tracing a screenshot. Vector only.
- **No webfonts.** No `@font-face`, no `<link>` to a font. The two stacks in &sect;1.5 and &sect;2.1, or nothing.
- **No filters that fail in print.** No `<filter>`, no `feGaussianBlur`, no `feDropShadow`, no CSS
  `filter`, no `opacity` below 1 to fake a tint (use the pale fill instead).
- **No colour as the only carrier of meaning.** Ever. Every meaningful distinction needs a **second**
  cue: a shape, a label, a number, or a position. Train vs test especially (&sect;1.2).
- **No gradients.** Flat fills only.
- **No `width`/`height` on the root `<svg>`.** viewBox only.
- **No white background rect.**
- **No text below 12px**, and no text you expect to wrap.
- **No new colours.** If you think you need a seventh, you need a different diagram (&sect;1.3).
- **No `<foreignObject>`**, no embedded HTML, no `<script>`.

---

## 9. Pre-flight check

```bash
# 1. It must parse as XML.
python3 -c "import xml.dom.minidom,sys; xml.dom.minidom.parse(sys.argv[1])" fig-w09-3-loop-counter-slots.svg

# 2. It must not contain anything banned.
grep -nE '<image|href="http|@font-face|<filter|feGaussianBlur|feDropShadow|<foreignObject|<script|Gradient' \
  fig-w09-3-loop-counter-slots.svg && echo "BANNED CONSTRUCT" || echo "clean"

# 3. It must declare accessibility and no fixed size.
f=fig-w09-3-loop-counter-slots.svg
grep -q 'role="img"' $f && grep -q '<title>' $f && grep -q '<desc>' $f && echo "a11y ok"
grep -nE '<svg[^>]+(width|height)=' $f && echo "REMOVE width/height" || echo "scales ok"

# 4. No type under the floor, and nothing shrunk under scale().
grep -oE 'font-size="[0-9.]+"' $f | sort -u          # nothing below 12
grep -oE 'scale\([0-9.]+' $f | sort -u               # any value < 1 on a group containing <text> is a defect
```

Or run the whole audit over every motif and pattern at once &mdash; it checks bounds against the 20px
padding, effective font size after every `scale()`, banned constructs, and overlapping labels:

```bash
cd _generator && python3 _gen_audit.py     # must print "--- 0 finding(s)"
```

Then, by eye:

- [ ] **It is not a picture of code.** All three questions in &sect;3.2 answered yes.
- [ ] `<title>` matches the markdown alt text word for word, and `<desc>` describes the *idea*.
- [ ] Every colour is from &sect;1.1, used in its role.
- [ ] Nothing within 20px of the canvas edge &mdash; including the far end of a long caption.
- [ ] Every meaningful distinction has a shape, label or number as well as a colour.
- [ ] Every leader line and callout routed through empty space; nothing overlaps a data point.
- [ ] Opened `_preview.html`, ticked **Greyscale**, and the figure still reads.
- [ ] A 12-year-old gets the point in four seconds with the caption covered.
- [ ] A teacher who has never seen Python gets it too.

---

## 10. Files in this folder

| File | What it is |
|---|---|
| `STYLE.md` | This contract. |
| `_motifs.svg` | Sprite sheet: all MOTIF_COUNT_ALL motifs as `<symbol>`. Reference with `<use>` or copy inline. |
| `_preview.html` | Open in any browser. Renders the palette, every motif, the &sect;3 pair and every pattern, with greyscale and dark-page toggles. |
| `_generator/` | The source of truth. `STYLE.md`, `_motifs.svg` and `_preview.html` are all generated from it, so a motif can never disagree with its own snippet. Edit a motif here, then re-run the three commands below. |
| `fig-wNN-*.svg` | The week figures. |

```bash
cd _generator
python3 _gen_emit.py     # rewrites _motifs.svg and _preview.html
python3 _gen_style.py    # rewrites STYLE.md
python3 _gen_audit.py    # bounds, 12px floor, scale(), banned constructs, label collisions
```
"""


def build():
    doc = DOC
    doc = doc.replace("BAD_EXAMPLE_SVG", EXAMPLES[0][2])
    doc = doc.replace("GOOD_EXAMPLE_SVG", EXAMPLES[1][2])
    doc = doc.replace("MOTIF_BLOCKS_NEW", "\n".join(motif_block(m) for m in NEW))
    doc = doc.replace("MOTIF_BLOCKS_OLD", "\n".join(motif_block(m) for m in OLD))
    doc = doc.replace("PATTERN_BLOCKS", "\n".join(pattern_block(p) for p in PATTERNS))
    doc = doc.replace("MOTIF_COUNT_NEW", str(len(NEW)))
    doc = doc.replace("MOTIF_COUNT_OLD", str(len(OLD)))
    doc = doc.replace("MOTIF_COUNT_ALL", str(len(MOTIFS)))
    open(os.path.join(HERE, "STYLE.md"), "w").write(doc)
    return doc


if __name__ == "__main__":
    d = build()
    print("STYLE.md: %d lines, %d motif blocks, %d pattern blocks"
          % (d.count("\n") + 1, len(MOTIFS), len(PATTERNS)))

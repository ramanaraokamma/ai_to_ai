# Figure style system &mdash; AI Academy, Level 2 &ldquo;Builder&rdquo; (36-week course)

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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 300" role="img">
  <title>Wrong: a figure that is only a picture of code</title>
  <desc>A grey panel containing five lines of Python about looping over a list of fruits, with no diagram, no arrows and no annotation.</desc>
  <rect x="20" y="20" width="460" height="40" rx="10" fill="#F6AEA6" stroke="#CC2B1D" stroke-width="3" stroke-linejoin="round"/>
  <g transform="translate(28,24) scale(0.3)">
  <circle cx="50" cy="50" r="34" fill="#F6AEA6" stroke="#CC2B1D" stroke-width="3"/>
  <g stroke="#CC2B1D" stroke-width="6" stroke-linecap="round">
    <line x1="38" y1="38" x2="62" y2="62"/>
    <line x1="62" y1="38" x2="38" y2="62"/>
  </g>
  </g>
  <text x="74" y="46" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B">Do not do this &#8212; it is a picture of code</text>
  <rect x="20" y="80" width="460" height="170" rx="10" fill="#F5F8FA" stroke="#C7CDD4" stroke-width="1.5"/>
  <text x="40" y="114" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#14202B">fruits = ["apple", "fig", "plum"]</text>
  <text x="40" y="144" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#14202B">for i in range(3):</text>
  <text x="40" y="174" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#14202B">    print(i, fruits[i])</text>
  <text x="40" y="214" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#55636F"># 0 apple / 1 fig / 2 plum</text>
  <text x="250" y="276" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">The reader learns nothing the code block did not already say.</text>
</svg>
```

**Right.** No code on the canvas. The counter is a number in a circle; the arrow says &ldquo;you come
back round here&rdquo;; the lit slot says which item `i` currently names; and the caption
`pass 2 of 3` under a counter reading `1` makes the off-by-one *visible*, which is the thing the
learner actually gets wrong.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 300" role="img">
  <title>Right: a figure that diagrams the mental model</title>
  <desc>A circular arrow with a counter reading i equals 1 sits beside three slots holding apple, fig and plum, numbered 0 to 2. The middle slot is highlighted and labelled i names this slot.</desc>
  <rect x="20" y="20" width="460" height="40" rx="10" fill="#E2F7ED" stroke="#1B7A4B" stroke-width="3" stroke-linejoin="round"/>
  <g transform="translate(28,24) scale(0.3)">
  <circle cx="50" cy="50" r="34" fill="#E2F7ED" stroke="#1B7A4B" stroke-width="3"/>
  <polyline points="34,52 45,64 68,38" fill="none" stroke="#1B7A4B" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="74" y="46" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B">Do this instead &#8212; it diagrams the mental model</text>
  <rect x="20" y="76" width="460" height="180" rx="12" fill="#F5F8FA" stroke="#C7CDD4" stroke-width="1.5" stroke-linejoin="round"/>
  <path d="M136 73 A52 52 0 1 1 84 73" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(84 73) rotate(-30)"/>
  <circle cx="110" cy="118" r="34" fill="#FFFFFF" stroke="#14202B" stroke-width="3"/>
  <text x="110" y="106" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">i</text>
  <text x="110" y="126" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle" dominant-baseline="central">1</text>
  <text x="110" y="188" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">pass 2 of 3</text>
  <rect x="206" y="92" width="82" height="52" rx="6" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5" stroke-linejoin="round"/>
  <text x="247" y="118" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">apple</text>
  <text x="247" y="88" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">0</text>
  <rect x="296" y="92" width="82" height="52" rx="6" fill="#F4D5E9" stroke="#C42B8C" stroke-width="3" stroke-linejoin="round"/>
  <text x="337" y="118" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">fig</text>
  <text x="337" y="88" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">1</text>
  <rect x="386" y="92" width="82" height="52" rx="6" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5" stroke-linejoin="round"/>
  <text x="427" y="118" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">plum</text>
  <text x="427" y="88" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">2</text>
  <path d="M331 158 L343 158 L337 150 Z" fill="#F4D5E9" stroke="#C42B8C" stroke-width="2" stroke-linejoin="round"/>
  <line x1="337" y1="174" x2="337" y2="160" stroke="#C42B8C" stroke-width="1.5"/>
  <text x="337" y="190" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">i names this slot</text>
  <text x="250" y="228" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">The counter names one slot per pass. After the last slot it stops.</text>
  <text x="250" y="276" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">Same lesson, no code on screen &#8212; and the off-by-one shows.</text>
</svg>
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

## 4. Motif library &mdash; Level 2 (23)

**Do not redraw these.** Consistency across the whole year is the point. Two ways to use them:

```svg
<!-- A) reference the sprite sheet -->
<use href="_motifs.svg#motif-list" x="40" y="40" width="320" height="126"/>

<!-- B) copy the <g> inline (below) and position it -->
<g transform="translate(600,150)">...</g>
```

Every motif is drawn to its own viewBox with **the origin at the top-left**, so `translate(x,y)` puts
its top-left corner at exactly `(x,y)`. Remember &sect;2.4 before you scale one.

### `motif-variable` &mdash; A variable as a labelled box

viewBox `0 0 170 100` (170&times;100). A luggage-label tag reading score is attached to a box holding the value 7.

**Use it for:** The name is a label stuck ON the box, not the box itself. Value 24px, name 14px.

```svg
<g transform="translate(0,0)">
  <rect x="20" y="12" width="78" height="26" rx="8" fill="#FFFFFF" stroke="#14202B" stroke-width="2" stroke-linejoin="round"/>
  <text x="59" y="25" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">score</text>
  <rect x="20" y="38" width="124" height="48" rx="10" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <text x="82" y="62" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle" dominant-baseline="central">7</text>
</g>
```

### `motif-rebind` &mdash; Rebinding a variable

viewBox `0 0 350 136` (350&times;136). Two panels. Before: the box labelled score holds 7. After: the same box holds 10 and the old 7 is struck through.

**Use it for:** Use for = as rebinding, never as equality. The struck-through old value is the whole point.

```svg
<g transform="translate(0,0)">
  <rect x="10" y="8" width="78" height="26" rx="8" fill="#FFFFFF" stroke="#14202B" stroke-width="2" stroke-linejoin="round"/>
  <text x="49" y="21" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">score</text>
  <rect x="10" y="34" width="124" height="48" rx="10" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <text x="72" y="58" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle" dominant-baseline="central">7</text>
  <line x1="146" y1="58" x2="190" y2="58" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(190 58) rotate(0)"/>
  <rect x="206" y="8" width="78" height="26" rx="8" fill="#FFFFFF" stroke="#14202B" stroke-width="2" stroke-linejoin="round"/>
  <text x="245" y="21" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">score</text>
  <rect x="206" y="34" width="124" height="48" rx="10" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <text x="244" y="58" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle" dominant-baseline="central">10</text>
  <line x1="294" y1="58" x2="316" y2="58" stroke="#CC2B1D" stroke-width="3" stroke-linecap="round"/>
  <text x="305" y="58" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#55636F" text-anchor="middle" dominant-baseline="central">7</text>
  <text x="72" y="104" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">before</text>
  <text x="268" y="104" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">after</text>
</g>
```

### `motif-list` &mdash; A list as numbered slots

viewBox `0 0 320 126` (320&times;126). Five slots side by side holding 3, 8, 1, 9 and 4, numbered 0 to 4 underneath, with a bracket above labelled len = 5.

**Use it for:** Index labels 0..n-1 are compulsory. The bracket makes len a length, not a last index.

```svg
<g transform="translate(0,0)">
  <path d="M22 38 V30 H298 V38" fill="none" stroke="#55636F" stroke-width="1.5" stroke-linejoin="round"/>
  <text x="160" y="22" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">len = 5</text>
  <rect x="22" y="46" width="52" height="52" rx="6" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="2" stroke-linejoin="round"/>
  <rect x="78" y="46" width="52" height="52" rx="6" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="2" stroke-linejoin="round"/>
  <rect x="134" y="46" width="52" height="52" rx="6" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="2" stroke-linejoin="round"/>
  <rect x="190" y="46" width="52" height="52" rx="6" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="2" stroke-linejoin="round"/>
  <rect x="246" y="46" width="52" height="52" rx="6" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="2" stroke-linejoin="round"/>
  <text x="48" y="72" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">3</text>
  <text x="104" y="72" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">8</text>
  <text x="160" y="72" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">1</text>
  <text x="216" y="72" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">9</text>
  <text x="272" y="72" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">4</text>
  <text x="48" y="116" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">0</text>
  <text x="104" y="116" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">1</text>
  <text x="160" y="116" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">2</text>
  <text x="216" y="116" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">3</text>
  <text x="272" y="116" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">4</text>
</g>
```

### `motif-dict` &mdash; A dictionary as key to value pairs

viewBox `0 0 260 176` (260&times;176). Three rows. Each has a key box on the left, an arrow, and a value box on the right: player to Meera, runs to 48, ground to Pune.

**Use it for:** Keys are accent (a name you chose), values are data. The arrow is one-way: keys look up values, never the reverse.

```svg
<g transform="translate(0,0)">
  <text x="60" y="20" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">key</text>
  <text x="196" y="20" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">value</text>
  <rect x="14" y="30" width="92" height="40" rx="8" fill="#F4D5E9" stroke="#C42B8C" stroke-width="3" stroke-linejoin="round"/>
  <text x="60" y="50" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">player</text>
  <line x1="112" y1="50" x2="140" y2="50" stroke="#14202B" stroke-width="2.5" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" transform="translate(140 50) rotate(0)"/>
  <rect x="146" y="30" width="100" height="40" rx="8" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <text x="196" y="50" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Meera</text>
  <rect x="14" y="78" width="92" height="40" rx="8" fill="#F4D5E9" stroke="#C42B8C" stroke-width="3" stroke-linejoin="round"/>
  <text x="60" y="98" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">runs</text>
  <line x1="112" y1="98" x2="140" y2="98" stroke="#14202B" stroke-width="2.5" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" transform="translate(140 98) rotate(0)"/>
  <rect x="146" y="78" width="100" height="40" rx="8" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <text x="196" y="98" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">48</text>
  <rect x="14" y="126" width="92" height="40" rx="8" fill="#F4D5E9" stroke="#C42B8C" stroke-width="3" stroke-linejoin="round"/>
  <text x="60" y="146" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">ground</text>
  <line x1="112" y1="146" x2="140" y2="146" stroke="#14202B" stroke-width="2.5" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" transform="translate(140 146) rotate(0)"/>
  <rect x="146" y="126" width="100" height="40" rx="8" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <text x="196" y="146" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Pune</text>
</g>
```

### `motif-loop` &mdash; A for loop as one trip round a circle

viewBox `0 0 180 185` (180&times;185). A near-complete circular arrow with a counter reading i equals 2 in the middle, above a row of four numbered slots with slot 2 highlighted.

**Use it for:** The counter and the highlighted slot must always agree. Highlight by fill AND a caret, never fill alone.

```svg
<g transform="translate(0,0)">
  <path d="M114 46 A48 48 0 1 1 66 46" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(66 46) rotate(-30)"/>
  <circle cx="90" cy="88" r="26" fill="#F5F8FA" stroke="#14202B" stroke-width="3"/>
  <text x="90" y="78" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">i</text>
  <text x="90" y="96" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle" dominant-baseline="central">2</text>
  <path d="M102 140 L114 140 L108 148 Z" fill="#F4D5E9" stroke="#C42B8C" stroke-width="2" stroke-linejoin="round"/>
  <rect x="20" y="150" width="32" height="26" rx="5" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5" stroke-linejoin="round"/>
  <text x="36" y="163" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
  <rect x="56" y="150" width="32" height="26" rx="5" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5" stroke-linejoin="round"/>
  <text x="72" y="163" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">1</text>
  <rect x="92" y="150" width="32" height="26" rx="5" fill="#F4D5E9" stroke="#C42B8C" stroke-width="3" stroke-linejoin="round"/>
  <text x="108" y="163" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">2</text>
  <rect x="128" y="150" width="32" height="26" rx="5" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5" stroke-linejoin="round"/>
  <text x="144" y="163" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">3</text>
</g>
```

### `motif-if-else` &mdash; An if/else as a fork in the path

viewBox `0 0 240 172` (240&times;172). A signpost reading hot outside? stands over a path that forks. The left branch is labelled yes and leads to fan on; the right is labelled no and leads to fan off.

**Use it for:** The condition goes on the signpost, the answer goes on the branch. Both branches are drawn even when else is empty.

```svg
<g transform="translate(0,0)">
  <path d="M120 80 L53 120" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <path d="M120 80 L187 120" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <line x1="120" y1="52" x2="120" y2="80" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <rect x="44" y="16" width="152" height="36" rx="8" fill="#F5F8FA" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
  <text x="120" y="34" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">hot outside?</text>
  <rect x="70" y="90" width="34" height="20" rx="10" fill="#FFFFFF" stroke="#C42B8C" stroke-width="2" stroke-linejoin="round"/>
  <text x="87" y="100" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">yes</text>
  <rect x="137" y="90" width="34" height="20" rx="10" fill="#FFFFFF" stroke="#C42B8C" stroke-width="2" stroke-linejoin="round"/>
  <text x="154" y="100" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">no</text>
  <rect x="8" y="120" width="90" height="40" rx="8" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <text x="53" y="140" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">fan on</text>
  <rect x="142" y="120" width="90" height="40" rx="8" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <text x="187" y="140" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">fan off</text>
</g>
```

### `motif-function` &mdash; A function as a machine with a hopper and a chute

viewBox `0 0 200 172` (200&times;172). A funnel-shaped input hopper feeds a box named average, which empties through a chute at the bottom.

**Use it for:** Arguments fall in the top, the return value drops out the bottom. The name lives on the body.

```svg
<g transform="translate(0,0)">
  <line x1="100" y1="4" x2="100" y2="12" stroke="#1F6FB2" stroke-width="3" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#1F6FB2" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(100 16) rotate(90)"/>
  <path d="M62 18 L138 18 L118 48 L82 48 Z" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <rect x="44" y="48" width="112" height="72" rx="12" fill="#F5F8FA" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
  <text x="100" y="84" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">average</text>
  <path d="M80 120 L120 120 L132 146 L68 146 Z" fill="#E2F7ED" stroke="#1B7A4B" stroke-width="3" stroke-linejoin="round"/>
  <line x1="100" y1="148" x2="100" y2="156" stroke="#1B7A4B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#1B7A4B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(100 160) rotate(90)"/>
  <text x="146" y="36" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F">inputs</text>
  <text x="140" y="138" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F">returns</text>
</g>
```

### `motif-callstack` &mdash; A call stack as stacked trays

viewBox `0 0 185 155` (185&times;155). Three trays stacked on the ground. main is at the bottom, then total, then average on top, marked as the one running now.

**Use it for:** The tray on top is the one running. Number the trays so the calling order survives greyscale.

```svg
<g transform="translate(0,0)">
  <line x1="16" y1="142" x2="164" y2="142" stroke="#C7CDD4" stroke-width="1.5"/>
  <path d="M100 18 L112 18 L106 28 Z" fill="#F4D5E9" stroke="#C42B8C" stroke-width="2" stroke-linejoin="round"/>
  <rect x="22" y="32" width="136" height="32" rx="6" fill="#F4D5E9" stroke="#C42B8C" stroke-width="3" stroke-linejoin="round"/>
  <text x="90" y="48" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">average</text>
  <text x="166" y="52" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F">3</text>
  <rect x="22" y="68" width="136" height="32" rx="6" fill="#FFFFFF" stroke="#14202B" stroke-width="2" stroke-linejoin="round"/>
  <text x="90" y="84" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">total</text>
  <text x="166" y="88" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F">2</text>
  <rect x="22" y="104" width="136" height="32" rx="6" fill="#FFFFFF" stroke="#14202B" stroke-width="2" stroke-linejoin="round"/>
  <text x="90" y="120" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">main</text>
  <text x="166" y="124" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F">1</text>
</g>
```

### `motif-dataframe` &mdash; A DataFrame as a grid with a header row and an index

viewBox `0 0 272 180` (272&times;180). A three-row table with a bold header row reading player, runs, over, a grey index column numbered 0 to 2, and the runs column outlined and tinted as the current selection.

**Use it for:** Header row = data fill + weight 600. Index column = panel grey. A selection is an accent OUTLINE plus an accent tint, and it must cover the header too.

```svg
<g transform="translate(0,0)">
  <rect x="22" y="26" width="36" height="32" fill="#F5F8FA"/>
  <rect x="58" y="26" width="64" height="32" fill="#D9EAF9"/>
  <rect x="122" y="26" width="64" height="32" fill="#D9EAF9"/>
  <rect x="186" y="26" width="64" height="32" fill="#D9EAF9"/>
  <rect x="22" y="58" width="36" height="32" fill="#F5F8FA"/>
  <rect x="122" y="58" width="64" height="32" fill="#F4D5E9"/>
  <rect x="22" y="90" width="36" height="32" fill="#F5F8FA"/>
  <rect x="122" y="90" width="64" height="32" fill="#F4D5E9"/>
  <rect x="22" y="122" width="36" height="32" fill="#F5F8FA"/>
  <rect x="122" y="122" width="64" height="32" fill="#F4D5E9"/>
  <g stroke="#C7CDD4" stroke-width="1.5">
    <line x1="58" y1="26" x2="58" y2="154"/>
    <line x1="122" y1="26" x2="122" y2="154"/>
    <line x1="186" y1="26" x2="186" y2="154"/>
    <line x1="22" y1="90" x2="250" y2="90"/>
    <line x1="22" y1="122" x2="250" y2="122"/>
  </g>
  <line x1="22" y1="58" x2="250" y2="58" stroke="#14202B" stroke-width="2"/>
  <text x="90" y="42" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central" font-weight="600">player</text>
  <text x="154" y="42" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central" font-weight="600">runs</text>
  <text x="218" y="42" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central" font-weight="600">over</text>
  <text x="40" y="74" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
  <text x="90" y="74" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Meera</text>
  <text x="154" y="74" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">48</text>
  <text x="218" y="74" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">12</text>
  <text x="40" y="106" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">1</text>
  <text x="90" y="106" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Kabir</text>
  <text x="154" y="106" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">31</text>
  <text x="218" y="106" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">9</text>
  <text x="40" y="138" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">2</text>
  <text x="90" y="138" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Nova</text>
  <text x="154" y="138" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">57</text>
  <text x="218" y="138" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">15</text>
  <rect x="122" y="26" width="64" height="128" fill="none" stroke="#C42B8C" stroke-width="3"/>
  <rect x="22" y="26" width="228" height="128" fill="none" stroke="#14202B" stroke-width="3"/>
  <text x="154" y="18" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">selected</text>
  <text x="40" y="170" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">index</text>
</g>
```

### `motif-array-1d` &mdash; A 1-D numpy array as one contiguous row

viewBox `0 0 264 94` (264&times;94). Five square cells butted together holding 1 to 5, with a bracket above and the annotation shape open bracket 5 comma close bracket below.

**Use it for:** Cells touch, unlike a list's separated slots — that is the picture of contiguous memory. Always print the shape.

```svg
<g transform="translate(0,0)">
  <path d="M22 18 V12 H242 V18" fill="none" stroke="#55636F" stroke-width="1.5" stroke-linejoin="round"/>
  <rect x="22" y="24" width="44" height="44" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="44" y="46" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">1</text>
  <rect x="66" y="24" width="44" height="44" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="88" y="46" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">2</text>
  <rect x="110" y="24" width="44" height="44" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="132" y="46" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">3</text>
  <rect x="154" y="24" width="44" height="44" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="176" y="46" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">4</text>
  <rect x="198" y="24" width="44" height="44" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="220" y="46" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">5</text>
  <rect x="22" y="24" width="220" height="44" fill="none" stroke="#1F6FB2" stroke-width="3"/>
  <text x="132" y="86" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">shape (5,)</text>
</g>
```

### `motif-array-2d` &mdash; A 2-D numpy array as a shaped block

viewBox `0 0 240 172` (240&times;172). A block of three rows by four columns of numbers, with axis 0 arrowed downwards, axis 1 arrowed across, and the annotation shape 3 comma 4 below.

**Use it for:** axis 0 runs DOWN the rows, axis 1 runs ACROSS the columns. Label both arrows every time; this is the single most confused idea in numpy.

```svg
<g transform="translate(0,0)">
  <line x1="32" y1="34" x2="32" y2="126" stroke="#55636F" stroke-width="2" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#55636F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" transform="translate(32 132) rotate(90)"/>
  <line x1="50" y1="20" x2="204" y2="20" stroke="#55636F" stroke-width="2" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#55636F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" transform="translate(210 20) rotate(0)"/>
  <text x="130" y="12" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">axis 1</text>
  <text x="16" y="84" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" transform="rotate(-90 16 84)">axis 0</text>
  <rect x="48" y="30" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="69" y="48" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">1</text>
  <rect x="90" y="30" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="111" y="48" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">2</text>
  <rect x="132" y="30" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="153" y="48" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">3</text>
  <rect x="174" y="30" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="195" y="48" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">4</text>
  <rect x="48" y="66" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="69" y="84" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">5</text>
  <rect x="90" y="66" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="111" y="84" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">6</text>
  <rect x="132" y="66" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="153" y="84" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">7</text>
  <rect x="174" y="66" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="195" y="84" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">8</text>
  <rect x="48" y="102" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="69" y="120" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">9</text>
  <rect x="90" y="102" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="111" y="120" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">0</text>
  <rect x="132" y="102" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="153" y="120" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">1</text>
  <rect x="174" y="102" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="195" y="120" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">2</text>
  <rect x="48" y="30" width="168" height="108" fill="none" stroke="#1F6FB2" stroke-width="3"/>
  <text x="132" y="158" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">shape (3, 4)</text>
</g>
```

### `motif-chart-scatter` &mdash; A scatter plot skeleton

viewBox `0 0 220 192` (220&times;192). A scatter plot with a labelled y axis, a labelled x axis, three grid lines and seven dots rising to the right.

**Use it for:** One series, so no legend: the title names it. Grid lines go UNDER the marks, at 1.5px grey.

```svg
<g transform="translate(0,0)">
  <g stroke="#C7CDD4" stroke-width="1.5">
    <line x1="46" y1="108" x2="200" y2="108"/>
    <line x1="46" y1="66" x2="200" y2="66"/>
    <line x1="46" y1="24" x2="200" y2="24"/>
  </g>
  <text x="40" y="154" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">0</text>
  <text x="40" y="112" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">5</text>
  <text x="40" y="70" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">10</text>
  <text x="40" y="28" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">15</text>
  <g stroke="#55636F" stroke-width="1.5">
    <line x1="46" y1="150" x2="46" y2="155"/>
    <line x1="97" y1="150" x2="97" y2="155"/>
    <line x1="148" y1="150" x2="148" y2="155"/>
    <line x1="199" y1="150" x2="199" y2="155"/>
  </g>
  <text x="46" y="168" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">0</text>
  <text x="97" y="168" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">2</text>
  <text x="148" y="168" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">4</text>
  <text x="199" y="168" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">6</text>
  <line x1="46" y1="24" x2="46" y2="150" stroke="#14202B" stroke-width="2"/>
  <line x1="46" y1="150" x2="200" y2="150" stroke="#14202B" stroke-width="2"/>
  <circle cx="66" cy="132" r="5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="84" cy="118" r="5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="104" cy="108" r="5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="122" cy="88" r="5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="142" cy="76" r="5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="160" cy="58" r="5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="180" cy="44" r="5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <text x="123" y="184" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">hours</text>
  <text x="18" y="87" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" transform="rotate(-90 18 87)">score</text>
</g>
```

### `motif-chart-bar` &mdash; A bar chart skeleton

viewBox `0 0 220 192` (220&times;192). A bar chart with four bars labelled Mon to Thu, each printing its own value above it.

**Use it for:** Bars start at zero, always. Every bar carries its number, so the reader never measures against the grid.

```svg
<g transform="translate(0,0)">
  <g stroke="#C7CDD4" stroke-width="1.5">
    <line x1="46" y1="108" x2="200" y2="108"/>
    <line x1="46" y1="66" x2="200" y2="66"/>
    <line x1="46" y1="24" x2="200" y2="24"/>
  </g>
  <text x="40" y="154" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">0</text>
  <text x="40" y="112" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">5</text>
  <text x="40" y="70" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">10</text>
  <text x="40" y="28" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">15</text>
  <line x1="46" y1="24" x2="46" y2="150" stroke="#14202B" stroke-width="2"/>
  <line x1="46" y1="150" x2="200" y2="150" stroke="#14202B" stroke-width="2"/>
  <path d="M60 150 V68 A4 4 0 0 1 64 64 H82 A4 4 0 0 1 86 68 V150 Z" fill="#1F6FB2"/>
  <text x="73" y="58" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle">10</text>
  <text x="73" y="168" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">Mon</text>
  <path d="M96 150 V100 A4 4 0 0 1 100 96 H118 A4 4 0 0 1 122 100 V150 Z" fill="#1F6FB2"/>
  <text x="109" y="90" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle">6</text>
  <text x="109" y="168" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">Tue</text>
  <path d="M132 150 V44 A4 4 0 0 1 136 40 H154 A4 4 0 0 1 158 44 V150 Z" fill="#1F6FB2"/>
  <text x="145" y="34" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle">13</text>
  <text x="145" y="168" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">Wed</text>
  <path d="M168 150 V116 A4 4 0 0 1 172 112 H190 A4 4 0 0 1 194 116 V150 Z" fill="#1F6FB2"/>
  <text x="181" y="106" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle">4</text>
  <text x="181" y="168" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">Thu</text>
  <text x="123" y="184" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">day</text>
  <text x="18" y="87" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" transform="rotate(-90 18 87)">score</text>
</g>
```

### `motif-chart-line` &mdash; A line chart skeleton

viewBox `0 0 220 192` (220&times;192). A line chart with one series of five points joined left to right, each point marked with a hollow circle.

**Use it for:** A line means the x axis is ordered — time, or a dial you turned. If the x values are categories, use bars instead.

```svg
<g transform="translate(0,0)">
  <g stroke="#C7CDD4" stroke-width="1.5">
    <line x1="46" y1="108" x2="200" y2="108"/>
    <line x1="46" y1="66" x2="200" y2="66"/>
    <line x1="46" y1="24" x2="200" y2="24"/>
  </g>
  <text x="40" y="154" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">0</text>
  <text x="40" y="112" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">5</text>
  <text x="40" y="70" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">10</text>
  <text x="40" y="28" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">15</text>
  <g stroke="#55636F" stroke-width="1.5">
    <line x1="46" y1="150" x2="46" y2="155"/>
    <line x1="97" y1="150" x2="97" y2="155"/>
    <line x1="148" y1="150" x2="148" y2="155"/>
    <line x1="199" y1="150" x2="199" y2="155"/>
  </g>
  <text x="46" y="168" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">0</text>
  <text x="97" y="168" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">2</text>
  <text x="148" y="168" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">4</text>
  <text x="199" y="168" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">6</text>
  <line x1="46" y1="24" x2="46" y2="150" stroke="#14202B" stroke-width="2"/>
  <line x1="46" y1="150" x2="200" y2="150" stroke="#14202B" stroke-width="2"/>
  <polyline points="60,130 92,104 124,110 156,72 188,52" fill="none" stroke="#1F6FB2" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="60" cy="130" r="4.5" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3"/>
  <circle cx="92" cy="104" r="4.5" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3"/>
  <circle cx="124" cy="110" r="4.5" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3"/>
  <circle cx="156" cy="72" r="4.5" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3"/>
  <circle cx="188" cy="52" r="4.5" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3"/>
  <text x="123" y="184" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">hours</text>
  <text x="18" y="87" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" transform="rotate(-90 18 87)">score</text>
</g>
```

### `motif-split` &mdash; A train/test split as one cut of the deck

viewBox `0 0 290 175` (290&times;175). A deck of 100 rows is cut by a dashed line into a train pile of 80 rows and a test pile of 20 rows.

**Use it for:** Train is data blue, test is accent pink — the pile you must not touch. Print both counts; they have to add up.

```svg
<g transform="translate(0,0)">
  <rect x="24" y="30" width="76" height="110" rx="8" fill="#FFFFFF" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
  <g stroke="#C7CDD4" stroke-width="1.5">
    <line x1="24" y1="46" x2="100" y2="46"/>
    <line x1="24" y1="62" x2="100" y2="62"/>
    <line x1="24" y1="78" x2="100" y2="78"/>
    <line x1="24" y1="94" x2="100" y2="94"/>
    <line x1="24" y1="110" x2="100" y2="110"/>
    <line x1="24" y1="126" x2="100" y2="126"/>
  </g>
  <text x="62" y="74" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle" dominant-baseline="central">80</text>
  <text x="62" y="130" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">20</text>
  <line x1="14" y1="118" x2="110" y2="118" stroke="#C42B8C" stroke-width="2" stroke-dasharray="6 4"/>
  <line x1="104" y1="74" x2="150" y2="60" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(150 60) rotate(-16.9)"/>
  <line x1="104" y1="128" x2="150" y2="124" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(150 124) rotate(-5)"/>
  <rect x="154" y="34" width="124" height="54" rx="10" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <text x="216" y="56" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">train</text>
  <text x="216" y="76" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">80 rows</text>
  <rect x="154" y="102" width="124" height="46" rx="10" fill="#F4D5E9" stroke="#C42B8C" stroke-width="3" stroke-linejoin="round"/>
  <text x="216" y="120" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">test</text>
  <text x="216" y="140" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">20 rows</text>
  <text x="150" y="166" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">one cut, then never mix them</text>
</g>
```

### `motif-knn` &mdash; A kNN vote: query point, three neighbours, tally

viewBox `0 0 230 220` (230&times;220). A pink square marked with a question mark sits among circles and triangles. A dashed ring labelled k equals 3 encloses two triangles and one circle. Below, a tally reads orange times 2 wins, apple times 1.

**Use it for:** Two classes = two SHAPES, never two colours only. The query is a third shape. The tally must add up to k.

```svg
<g transform="translate(0,0)">
  <circle cx="110" cy="80" r="40" fill="none" stroke="#C42B8C" stroke-width="2" stroke-dasharray="6 5"/>
  <line x1="110" y1="34" x2="110" y2="40" stroke="#C42B8C" stroke-width="1.5"/>
  <text x="110" y="30" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">k = 3</text>
  <circle cx="40" cy="44" r="6" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="58" cy="126" r="6" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="194" cy="86" r="6" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="94" cy="106" r="6" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <path d="M88 57 L95 69 L81 69 Z" fill="#1B7A4B" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>
  <path d="M132 89 L139 101 L125 101 Z" fill="#1B7A4B" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>
  <path d="M186 29 L193 41 L179 41 Z" fill="#1B7A4B" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>
  <path d="M168 121 L175 133 L161 133 Z" fill="#1B7A4B" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>
  <rect x="102" y="72" width="16" height="16" rx="3" fill="#F4D5E9" stroke="#C42B8C" stroke-width="3" stroke-linejoin="round"/>
  <text x="110" y="80" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">?</text>
  <line x1="16" y1="160" x2="214" y2="160" stroke="#C7CDD4" stroke-width="1.5"/>
  <path d="M26 173 L33 185 L19 185 Z" fill="#1B7A4B" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>
  <text x="42" y="185" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B">orange &#215; 2</text>
  <polyline points="134,182 140,188 152,174" fill="none" stroke="#1B7A4B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="158" y="185" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F">wins</text>
  <circle cx="26" cy="204" r="6" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <text x="42" y="209" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B">apple &#215; 1</text>
</g>
```

### `motif-tree` &mdash; A decision tree as boxes and yes/no branches

viewBox `0 0 280 196` (280&times;196). A question box reading petal long? branches no to a second question wide? and yes to the answer setosa. The second question branches to virginica and versicolor.

**Use it for:** Draw the edges FIRST so boxes sit on top. Questions are grey and end in ?, answers are blue and do not. Label every branch in words.

```svg
<g transform="translate(0,0)">
  <g stroke="#55636F" stroke-width="2" fill="none">
    <path d="M140 54 V70 H56 V88"/>
    <path d="M140 54 V70 H224 V88"/>
    <path d="M56 124 V140 H38 V156"/>
    <path d="M56 124 V140 H118 V156"/>
  </g>
  <text x="98" y="66" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">no</text>
  <text x="182" y="66" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">yes</text>
  <text x="33" y="152" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">no</text>
  <text x="123" y="152" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F">yes</text>
  <rect x="76" y="16" width="128" height="38" rx="8" fill="#F5F8FA" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
  <text x="140" y="35" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">petal long?</text>
  <rect x="8" y="88" width="96" height="36" rx="8" fill="#F5F8FA" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
  <text x="56" y="106" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">wide?</text>
  <rect x="176" y="88" width="96" height="36" rx="8" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <text x="224" y="106" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">setosa</text>
  <rect x="4" y="156" width="68" height="32" rx="8" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <text x="38" y="172" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">virginica</text>
  <rect x="84" y="156" width="68" height="32" rx="8" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <text x="118" y="172" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">versicolor</text>
</g>
```

### `motif-fit-underfit` &mdash; Underfitting: a line too simple for the data

viewBox `0 0 160 158` (160&times;158). Eight dots climb to the right. A flat straight line ignores the climb entirely; the caption reads too simple.

**Use it for:** Panel 1 of 3. The eight dots are IDENTICAL in all three panels — only the drawn model changes.

```svg
<g transform="translate(0,0)">
  <line x1="24" y1="18" x2="24" y2="126" stroke="#14202B" stroke-width="2"/>
  <line x1="24" y1="126" x2="146" y2="126" stroke="#14202B" stroke-width="2"/>
  <path d="M30 80 L142 80" fill="none" stroke="#CC2B1D" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="36" cy="110" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="52" cy="96" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="66" cy="102" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="82" cy="80" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="96" cy="72" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="112" cy="58" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="126" cy="64" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="140" cy="40" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <text x="85" y="148" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">too simple</text>
</g>
```

### `motif-fit-good` &mdash; A good fit: a curve that follows the trend

viewBox `0 0 160 158` (160&times;158). The same eight dots, with a smooth curve running through the middle of the climb; the caption reads just right.

**Use it for:** Panel 2 of 3. Correct green, and the shape is smooth — two cues, not one.

```svg
<g transform="translate(0,0)">
  <line x1="24" y1="18" x2="24" y2="126" stroke="#14202B" stroke-width="2"/>
  <line x1="24" y1="126" x2="146" y2="126" stroke="#14202B" stroke-width="2"/>
  <path d="M30 114 Q86 92 142 44" fill="none" stroke="#1B7A4B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="36" cy="110" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="52" cy="96" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="66" cy="102" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="82" cy="80" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="96" cy="72" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="112" cy="58" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="126" cy="64" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="140" cy="40" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <text x="85" y="148" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">just right</text>
</g>
```

### `motif-fit-overfit` &mdash; Overfitting: a wiggle through every point

viewBox `0 0 160 158` (160&times;158). The same eight dots, with a jagged line that detours to pass exactly through each one; the caption reads memorised.

**Use it for:** Panel 3 of 3. Underfit and overfit are both wrong-red; the SHAPE (flat vs jagged) tells them apart in greyscale.

```svg
<g transform="translate(0,0)">
  <line x1="24" y1="18" x2="24" y2="126" stroke="#14202B" stroke-width="2"/>
  <line x1="24" y1="126" x2="146" y2="126" stroke="#14202B" stroke-width="2"/>
  <path d="M30 118 L36 110 L44 120 L52 96 L59 110 L66 102 L74 84 L82 80 L89 88 L96 72 L104 68 L112 58 L119 74 L126 64 L133 50 L140 40 L145 50" fill="none" stroke="#CC2B1D" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="36" cy="110" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="52" cy="96" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="66" cy="102" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="82" cy="80" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="96" cy="72" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="112" cy="58" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="126" cy="64" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="140" cy="40" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <text x="85" y="148" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">memorised</text>
</g>
```

### `motif-terminal` &mdash; A terminal window frame

viewBox `0 0 300 176` (300&times;176). A console window with a title bar reading Terminal. Inside, a prompt runs python hello.py, the output line reads hello, world, and a fresh prompt waits with a block cursor.

**Use it for:** The window frame is ink; the title bar is panel grey. Output text is the MONO stack at 14px. Draw the frame LAST so it caps the fill.

```svg
<g transform="translate(0,0)">
  <path d="M14 26 A10 10 0 0 1 24 16 H276 A10 10 0 0 1 286 26 V46 H14 Z" fill="#F5F8FA"/>
  <g fill="none" stroke="#55636F" stroke-width="2">
    <circle cx="32" cy="31" r="4"/>
    <circle cx="48" cy="31" r="4"/>
    <circle cx="64" cy="31" r="4"/>
  </g>
  <text x="84" y="35" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F">Terminal</text>
  <line x1="14" y1="46" x2="286" y2="46" stroke="#14202B" stroke-width="2"/>
  <text x="30" y="72" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#55636F">&gt;</text>
  <text x="44" y="72" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#14202B">python hello.py</text>
  <text x="30" y="100" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#14202B">hello, world</text>
  <text x="30" y="130" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#55636F">&gt;</text>
  <rect x="44" y="118" width="9" height="14" fill="#14202B"/>
  <rect x="14" y="16" width="272" height="148" rx="10" fill="none" stroke="#14202B" stroke-width="3"/>
</g>
```

### `motif-traceback` &mdash; A traceback, with the offending line marked

viewBox `0 0 400 205` (400&times;205). A console panel outlined in red shows a four-line Python traceback. The line that failed is highlighted and an arrow points at it from the right. The last line, a NameError, is printed in red.

**Use it for:** THE SANCTIONED EXCEPTION (see the hard rule): an error message is an artefact the learner must read, so we show it verbatim. The figure's work is the highlight and the arrow, not the text.

```svg
<g transform="translate(0,0)">
  <path d="M14 26 A10 10 0 0 1 24 16 H296 A10 10 0 0 1 306 26 V46 H14 Z" fill="#F6AEA6"/>
  <g stroke="#CC2B1D" stroke-width="2.5" stroke-linecap="round">
    <line x1="26" y1="26" x2="36" y2="36"/>
    <line x1="36" y1="26" x2="26" y2="36"/>
  </g>
  <text x="46" y="35" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B">Traceback</text>
  <line x1="14" y1="46" x2="306" y2="46" stroke="#14202B" stroke-width="2"/>
  <rect x="22" y="98" width="272" height="22" rx="4" fill="#F6AEA6"/>
  <text x="26" y="68" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12" fill="#55636F">Traceback (most recent call last):</text>
  <text x="26" y="90" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12" fill="#55636F">  File "pay.py", line 4, in &lt;module&gt;</text>
  <text x="26" y="112" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12" fill="#14202B">    total = price * quantity</text>
  <text x="26" y="140" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12" fill="#CC2B1D" font-weight="600">NameError: name 'quantity'</text>
  <text x="26" y="158" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12" fill="#CC2B1D" font-weight="600">is not defined</text>
  <rect x="14" y="16" width="292" height="160" rx="10" fill="none" stroke="#CC2B1D" stroke-width="3"/>
  <line x1="390" y1="109" x2="314" y2="109" stroke="#CC2B1D" stroke-width="3" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#CC2B1D" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(314 109) rotate(180)"/>
  <text x="312" y="92" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B">this line</text>
  <text x="160" y="196" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">Read the last line first.</text>
</g>
```

### `motif-code-callout` &mdash; One line of code with a callout on one token

viewBox `0 0 340 112` (340&times;112). A single line of code sits on a grey strip. The word price is boxed in pink and an arrow points up at it from a label reading a name, not a value.

**Use it for:** ONE token, ONE arrow, ONE claim. Split the line into separate <text> runs at fixed x so the highlight box lands exactly on the token instead of trusting the font's advance width.

```svg
<g transform="translate(0,0)">
  <rect x="14" y="24" width="312" height="34" rx="8" fill="#F5F8FA" stroke="#C7CDD4" stroke-width="1.5"/>
  <rect x="95" y="30" width="52" height="24" rx="4" fill="#F4D5E9" stroke="#C42B8C" stroke-width="2"/>
  <text x="28" y="46" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#14202B">total =</text>
  <text x="100" y="46" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#14202B">price</text>
  <text x="152" y="46" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#14202B">* count</text>
  <line x1="121" y1="60" x2="121" y2="78" stroke="#C42B8C" stroke-width="2"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#C42B8C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" transform="translate(121 58) rotate(-90)"/>
  <rect x="53" y="78" width="136" height="24" rx="12" fill="#FFFFFF" stroke="#C42B8C" stroke-width="2" stroke-linejoin="round"/>
  <text x="121" y="90" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">a name, not a value</text>
</g>
```


---

## 5. Motifs inherited from Level 1 (8)

Copied byte-for-byte from Level 1's sprite sheet so the two years match. Reproduced here so this
folder is self-contained. `motif-machine`, `motif-brain`, `motif-robot`, `motif-magnifier`,
`motif-scale`, `motif-lightbulb`, `motif-photos` and `motif-thought` also still exist in Level 1 and
may be pulled across if a week needs them; for Level 2's own subjects prefer the &sect;4 motifs
(`motif-function` supersedes `motif-machine`; `motif-dataframe` supersedes `motif-table` whenever the
table has real content).

### `motif-arrow` &mdash; Arrow pointing right

viewBox `0 0 100 40` (100&times;40). A straight arrow pointing to the right.

**Use it for:** Inherited verbatim from Level 1. Every pipeline gap.

```svg
<g transform="translate(0,0)">
  <line x1="6" y1="20" x2="84" y2="20" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="76,10 92,20 76,30" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
</g>
```

### `motif-arrow-curved` &mdash; Curved arrow

viewBox `0 0 100 60` (100&times;60). A curved arrow that loops up and over to the right.

**Use it for:** Inherited verbatim from Level 1. Going back round a loop, or returning a value.

```svg
<g transform="translate(0,0)">
  <path d="M8 48 Q48 2 84 34" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(84 34) rotate(41)"/>
</g>
```

### `motif-badge-check` &mdash; Correct badge

viewBox `0 0 100 100` (100&times;100). A round badge with a tick inside, meaning correct.

**Use it for:** Inherited verbatim from Level 1. It ran / it passed / after the fix.

```svg
<g transform="translate(0,0)">
  <circle cx="50" cy="50" r="34" fill="#E2F7ED" stroke="#1B7A4B" stroke-width="3"/>
  <polyline points="34,52 45,64 68,38" fill="none" stroke="#1B7A4B" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
</g>
```

### `motif-badge-cross` &mdash; Wrong badge

viewBox `0 0 100 100` (100&times;100). A round badge with a cross inside, meaning wrong.

**Use it for:** Inherited verbatim from Level 1. It crashed / it failed / before the fix.

```svg
<g transform="translate(0,0)">
  <circle cx="50" cy="50" r="34" fill="#F6AEA6" stroke="#CC2B1D" stroke-width="3"/>
  <g stroke="#CC2B1D" stroke-width="6" stroke-linecap="round">
    <line x1="38" y1="38" x2="62" y2="62"/>
    <line x1="62" y1="38" x2="38" y2="62"/>
  </g>
</g>
```

### `motif-box` &mdash; Labelled box

viewBox `0 0 120 80` (120&times;80). A rounded box with a label inside.

**Use it for:** Inherited verbatim from Level 1. A neutral stage in a pipeline.

```svg
<g transform="translate(0,0)">
  <rect x="6" y="10" width="108" height="60" rx="10" fill="#F5F8FA" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
  <text x="60" y="40" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">Label</text>
</g>
```

### `motif-note` &mdash; Sticky note

viewBox `0 0 100 100` (100&times;100). A sticky note with a folded corner and three lines of writing.

**Use it for:** Inherited verbatim from Level 1. A human decision: a cleaning-log entry, a comment, a choice you made.

```svg
<g transform="translate(0,0)">
  <path d="M12 12 H88 V68 L68 88 H12 Z" fill="#E8C671" stroke="#845F00" stroke-width="3" stroke-linejoin="round"/>
  <path d="M68 88 V68 H88 Z" fill="#FFFFFF" stroke="#845F00" stroke-width="3" stroke-linejoin="round"/>
  <g stroke="#55636F" stroke-width="3" stroke-linecap="round">
    <line x1="24" y1="30" x2="76" y2="30"/>
    <line x1="24" y1="43" x2="76" y2="43"/>
    <line x1="24" y1="56" x2="60" y2="56"/>
  </g>
</g>
```

### `motif-table` &mdash; Data table

viewBox `0 0 100 100` (100&times;100). A small data table with a shaded header row and six cells.

**Use it for:** Inherited verbatim from Level 1. A table as an ICON, at small size. For a table with real content, use motif-dataframe.

```svg
<g transform="translate(0,0)">
  <rect x="8" y="16" width="84" height="68" rx="8" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <path d="M8 24 A8 8 0 0 1 16 16 H84 A8 8 0 0 1 92 24 V38 H8 Z" fill="#D9EAF9" stroke="none"/>
  <g stroke="#C7CDD4" stroke-width="1.5">
    <line x1="8" y1="61" x2="92" y2="61"/>
    <line x1="36" y1="38" x2="36" y2="84"/>
    <line x1="64" y1="38" x2="64" y2="84"/>
  </g>
  <line x1="8" y1="38" x2="92" y2="38" stroke="#1F6FB2" stroke-width="3"/>
  <rect x="8" y="16" width="84" height="68" rx="8" fill="none" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <g fill="#55636F">
    <rect x="15" y="24" width="14" height="5" rx="2.5"/>
    <rect x="43" y="24" width="14" height="5" rx="2.5"/>
    <rect x="71" y="24" width="14" height="5" rx="2.5"/>
    <rect x="15" y="47" width="14" height="5" rx="2.5"/>
    <rect x="43" y="47" width="14" height="5" rx="2.5"/>
    <rect x="71" y="47" width="14" height="5" rx="2.5"/>
    <rect x="15" y="70" width="14" height="5" rx="2.5"/>
    <rect x="43" y="70" width="14" height="5" rx="2.5"/>
    <rect x="71" y="70" width="14" height="5" rx="2.5"/>
  </g>
</g>
```

### `motif-child` &mdash; Child's face

viewBox `0 0 100 100` (100&times;100). A smiling child's face with short hair.

**Use it for:** Inherited verbatim from Level 1. The programmer. Use when the point is that a PERSON chose something.

```svg
<g transform="translate(0,0)">
  <circle cx="50" cy="52" r="30" fill="#E8C671" stroke="#845F00" stroke-width="3"/>
  <path d="M20 44 A30 30 0 0 1 80 44 A34 22 0 0 0 20 44 Z" fill="#845F00" stroke="#845F00" stroke-width="3" stroke-linejoin="round"/>
  <circle cx="40" cy="50" r="4" fill="#14202B"/>
  <circle cx="60" cy="50" r="4" fill="#14202B"/>
  <path d="M39 63 Q50 72 61 63" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
</g>
```


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

### `pattern-pipeline` &mdash; Every model in this level is this one pipeline

**Canvas** `0 0 800 400`. Four equal boxes, arrows in the gaps, and a NUMBER on every stage so the order survives greyscale. Stage colours run data &rarr; accent &rarr; model &rarr; correct, which is also the story: data, held-out data, the learned thing, the verdict. The stage glyphs carry NO text &mdash; at this size a motif's own labels would fall under the 12px floor, so the words go in the stage label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img">
  <title>Every model in this level is this one pipeline</title>
  <desc>Four numbered stages left to right: load the CSV as a table, cut it into a large train pile and a small test pile, feed the train pile through a machine, and read a score off a bar chart.</desc>
  <text x="400" y="46" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle">Every model in this level is this one pipeline</text>
  <rect x="30" y="96" width="152" height="190" rx="12" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <rect x="222" y="96" width="152" height="190" rx="12" fill="#FFFFFF" stroke="#C42B8C" stroke-width="3" stroke-linejoin="round"/>
  <rect x="414" y="96" width="152" height="190" rx="12" fill="#FFFFFF" stroke="#6D28D9" stroke-width="3" stroke-linejoin="round"/>
  <rect x="606" y="96" width="152" height="190" rx="12" fill="#FFFFFF" stroke="#1B7A4B" stroke-width="3" stroke-linejoin="round"/>
  <g transform="translate(183,182) scale(0.4)">
  <line x1="6" y1="20" x2="84" y2="20" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="76,10 92,20 76,30" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <g transform="translate(375,182) scale(0.4)">
  <line x1="6" y1="20" x2="84" y2="20" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="76,10 92,20 76,30" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <g transform="translate(567,182) scale(0.4)">
  <line x1="6" y1="20" x2="84" y2="20" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="76,10 92,20 76,30" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <g transform="translate(36,121) scale(1.4)">
  <rect x="8" y="16" width="84" height="68" rx="8" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <path d="M8 24 A8 8 0 0 1 16 16 H84 A8 8 0 0 1 92 24 V38 H8 Z" fill="#D9EAF9" stroke="none"/>
  <g stroke="#C7CDD4" stroke-width="1.5">
    <line x1="8" y1="61" x2="92" y2="61"/>
    <line x1="36" y1="38" x2="36" y2="84"/>
    <line x1="64" y1="38" x2="64" y2="84"/>
  </g>
  <line x1="8" y1="38" x2="92" y2="38" stroke="#1F6FB2" stroke-width="3"/>
  <rect x="8" y="16" width="84" height="68" rx="8" fill="none" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <g fill="#55636F">
    <rect x="15" y="24" width="14" height="5" rx="2.5"/>
    <rect x="43" y="24" width="14" height="5" rx="2.5"/>
    <rect x="71" y="24" width="14" height="5" rx="2.5"/>
    <rect x="15" y="47" width="14" height="5" rx="2.5"/>
    <rect x="43" y="47" width="14" height="5" rx="2.5"/>
    <rect x="71" y="47" width="14" height="5" rx="2.5"/>
    <rect x="15" y="70" width="14" height="5" rx="2.5"/>
    <rect x="43" y="70" width="14" height="5" rx="2.5"/>
    <rect x="71" y="70" width="14" height="5" rx="2.5"/>
  </g>
  </g>
  <g transform="translate(230,131)">
  <rect x="4" y="20" width="40" height="80" rx="6" fill="#FFFFFF" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
    <g stroke="#C7CDD4" stroke-width="1.5">
      <line x1="4" y1="34" x2="44" y2="34"/><line x1="4" y1="48" x2="44" y2="48"/>
      <line x1="4" y1="62" x2="44" y2="62"/><line x1="4" y1="76" x2="44" y2="76"/>
    </g>
    <line x1="0" y1="84" x2="48" y2="84" stroke="#C42B8C" stroke-width="2" stroke-dasharray="5 4"/>
    <line x1="48" y1="44" x2="72" y2="36" stroke="#14202B" stroke-width="2.5" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" transform="translate(72 36) rotate(-18.4)"/>
    <line x1="48" y1="90" x2="72" y2="86" stroke="#14202B" stroke-width="2.5" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" transform="translate(72 86) rotate(-9.5)"/>
    <rect x="76" y="14" width="60" height="44" rx="8" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
    <rect x="76" y="70" width="60" height="32" rx="8" fill="#F4D5E9" stroke="#C42B8C" stroke-width="3" stroke-linejoin="round"/>
  </g>
  <g transform="translate(430,130)">
  <line x1="60" y1="2" x2="60" y2="10" stroke="#1F6FB2" stroke-width="3" stroke-linecap="round"/>
    <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#1F6FB2" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(60 14) rotate(90)"/>
    <path d="M28 16 L92 16 L78 42 L42 42 Z" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
    <rect x="24" y="42" width="72" height="56" rx="10" fill="#F5F8FA" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
    <g stroke="#14202B" stroke-width="3" stroke-linecap="round">
    <line x1="75.0" y1="70.0" x2="81.0" y2="70.0"/>
    <line x1="70.6" y1="80.6" x2="74.8" y2="84.8"/>
    <line x1="60.0" y1="85.0" x2="60.0" y2="91.0"/>
    <line x1="49.4" y1="80.6" x2="45.2" y2="84.8"/>
    <line x1="45.0" y1="70.0" x2="39.0" y2="70.0"/>
    <line x1="49.4" y1="59.4" x2="45.2" y2="55.2"/>
    <line x1="60.0" y1="55.0" x2="60.0" y2="49.0"/>
    <line x1="70.6" y1="59.4" x2="74.8" y2="55.2"/>
    </g>
    <circle cx="60" cy="70" r="14" fill="#FFFFFF" stroke="#14202B" stroke-width="3"/>
    <circle cx="60" cy="70" r="5" fill="#DBCEF3" stroke="#6D28D9" stroke-width="2.5"/>
    <path d="M44 98 L76 98 L86 120 L34 120 Z" fill="#E2F7ED" stroke="#1B7A4B" stroke-width="3" stroke-linejoin="round"/>
  </g>
  <g transform="translate(608,135)">
  <g stroke="#C7CDD4" stroke-width="1.5">
      <line x1="22" y1="30" x2="122" y2="30"/><line x1="22" y1="56" x2="122" y2="56"/><line x1="22" y1="82" x2="122" y2="82"/>
    </g>
    <g fill="#1F6FB2">
      <rect x="28" y="34" width="18" height="62" rx="3"/><rect x="52" y="58" width="18" height="38" rx="3"/>
      <rect x="76" y="22" width="18" height="74" rx="3"/><rect x="100" y="66" width="18" height="30" rx="3"/>
    </g>
    <line x1="22" y1="16" x2="22" y2="96" stroke="#14202B" stroke-width="2"/>
    <line x1="22" y1="96" x2="126" y2="96" stroke="#14202B" stroke-width="2"/>
  </g>
  <text x="106" y="312" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle">1. Load</text>
  <text x="106" y="332" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">the CSV as a table</text>
  <text x="298" y="312" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle">2. Split</text>
  <text x="298" y="332" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">train and test</text>
  <text x="490" y="312" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle">3. Fit</text>
  <text x="490" y="332" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">on train only</text>
  <text x="682" y="312" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle">4. Score</text>
  <text x="682" y="332" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">on test only</text>
  <text x="400" y="372" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#55636F" text-anchor="middle">Steps 1 and 2 are most of the work. Step 3 is three lines of code.</text>
</svg>
```

### `pattern-before-after` &mdash; Before and after we cleaned one cell

**Canvas** `0 0 800 400`. Mirror the geometry EXACTLY so the eye only has to find the one difference. The tick/cross badge shape, not the panel colour, says which side is which. One change per figure &mdash; if you changed two things, draw two figures.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img">
  <title>Before and after we cleaned one cell</title>
  <desc>Two mirrored panels. The left panel is marked wrong and its table has a missing runs value shown as a question mark. The right panel is marked correct and the same cell holds 31.</desc>
  <text x="400" y="46" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle">Before and after we cleaned one cell</text>
  <line x1="400" y1="80" x2="400" y2="336" stroke="#C7CDD4" stroke-width="1.5" stroke-dasharray="6 6"/>
  <rect x="30" y="80" width="360" height="240" rx="12" fill="#F6AEA6" stroke="#CC2B1D" stroke-width="3" stroke-linejoin="round"/>
  <rect x="410" y="80" width="360" height="240" rx="12" fill="#E2F7ED" stroke="#1B7A4B" stroke-width="3" stroke-linejoin="round"/>
  <g transform="translate(48,94) scale(0.42)">
  <circle cx="50" cy="50" r="34" fill="#F6AEA6" stroke="#CC2B1D" stroke-width="3"/>
  <g stroke="#CC2B1D" stroke-width="6" stroke-linecap="round">
    <line x1="38" y1="38" x2="62" y2="62"/>
    <line x1="62" y1="38" x2="38" y2="62"/>
  </g>
  </g>
  <g transform="translate(428,94) scale(0.42)">
  <circle cx="50" cy="50" r="34" fill="#E2F7ED" stroke="#1B7A4B" stroke-width="3"/>
  <polyline points="34,52 45,64 68,38" fill="none" stroke="#1B7A4B" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="104" y="128" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B">Before</text>
  <text x="484" y="128" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B">After</text>
  <rect x="54" y="150" width="304" height="126" fill="#FFFFFF"/>
  <rect x="54" y="150" width="34" height="30" fill="#F5F8FA"/>
  <rect x="88" y="150" width="90" height="30" fill="#D9EAF9"/>
  <rect x="178" y="150" width="90" height="30" fill="#D9EAF9"/>
  <rect x="268" y="150" width="90" height="30" fill="#D9EAF9"/>
  <rect x="54" y="180" width="34" height="32" fill="#F5F8FA"/>
  <rect x="54" y="212" width="34" height="32" fill="#F5F8FA"/>
  <rect x="54" y="244" width="34" height="32" fill="#F5F8FA"/>
  <rect x="178" y="212" width="90" height="32" fill="#F6AEA6"/>
  <g stroke="#C7CDD4" stroke-width="1.5">
    <line x1="88" y1="150" x2="88" y2="276"/>
    <line x1="178" y1="150" x2="178" y2="276"/>
    <line x1="268" y1="150" x2="268" y2="276"/>
    <line x1="54" y1="212" x2="358" y2="212"/>
    <line x1="54" y1="244" x2="358" y2="244"/>
  </g>
  <line x1="54" y1="180" x2="358" y2="180" stroke="#14202B" stroke-width="2"/>
  <text x="133" y="165" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central" font-weight="600">player</text>
  <text x="223" y="165" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central" font-weight="600">runs</text>
  <text x="313" y="165" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central" font-weight="600">over</text>
  <text x="71" y="196" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
  <text x="133" y="196" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Meera</text>
  <text x="223" y="196" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">48</text>
  <text x="313" y="196" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">12</text>
  <text x="71" y="228" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">1</text>
  <text x="133" y="228" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Kabir</text>
  <text x="223" y="228" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">?</text>
  <text x="313" y="228" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">9</text>
  <text x="71" y="260" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">2</text>
  <text x="133" y="260" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Nova</text>
  <text x="223" y="260" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">57</text>
  <text x="313" y="260" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">15</text>
  <rect x="178" y="212" width="90" height="32" fill="none" stroke="#CC2B1D" stroke-width="3"/>
  <rect x="54" y="150" width="304" height="126" fill="none" stroke="#14202B" stroke-width="3"/>
  <rect x="434" y="150" width="304" height="126" fill="#FFFFFF"/>
  <rect x="434" y="150" width="34" height="30" fill="#F5F8FA"/>
  <rect x="468" y="150" width="90" height="30" fill="#D9EAF9"/>
  <rect x="558" y="150" width="90" height="30" fill="#D9EAF9"/>
  <rect x="648" y="150" width="90" height="30" fill="#D9EAF9"/>
  <rect x="434" y="180" width="34" height="32" fill="#F5F8FA"/>
  <rect x="434" y="212" width="34" height="32" fill="#F5F8FA"/>
  <rect x="434" y="244" width="34" height="32" fill="#F5F8FA"/>
  <rect x="558" y="212" width="90" height="32" fill="#E2F7ED"/>
  <g stroke="#C7CDD4" stroke-width="1.5">
    <line x1="468" y1="150" x2="468" y2="276"/>
    <line x1="558" y1="150" x2="558" y2="276"/>
    <line x1="648" y1="150" x2="648" y2="276"/>
    <line x1="434" y1="212" x2="738" y2="212"/>
    <line x1="434" y1="244" x2="738" y2="244"/>
  </g>
  <line x1="434" y1="180" x2="738" y2="180" stroke="#14202B" stroke-width="2"/>
  <text x="513" y="165" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central" font-weight="600">player</text>
  <text x="603" y="165" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central" font-weight="600">runs</text>
  <text x="693" y="165" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central" font-weight="600">over</text>
  <text x="451" y="196" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
  <text x="513" y="196" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Meera</text>
  <text x="603" y="196" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">48</text>
  <text x="693" y="196" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">12</text>
  <text x="451" y="228" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">1</text>
  <text x="513" y="228" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Kabir</text>
  <text x="603" y="228" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">31</text>
  <text x="693" y="228" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">9</text>
  <text x="451" y="260" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">2</text>
  <text x="513" y="260" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Nova</text>
  <text x="603" y="260" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">57</text>
  <text x="693" y="260" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">15</text>
  <rect x="558" y="212" width="90" height="32" fill="none" stroke="#1B7A4B" stroke-width="3"/>
  <rect x="434" y="150" width="304" height="126" fill="none" stroke="#14202B" stroke-width="3"/>
  <text x="206" y="300" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">one runs value is missing, so mean() fails</text>
  <text x="586" y="300" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">filled from the scorecard, and logged why</text>
  <text x="400" y="360" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#55636F" text-anchor="middle">Same rows, same columns, one cell changed. Mirror the panels so only the content differs.</text>
</svg>
```

### `pattern-progression` &mdash; Same eight points, three models

**Canvas** `0 0 800 400`. Three equal panels, numbered, with IDENTICAL data in each. The numbers carry the progression; the panel colour only says good or bad. Underfit and overfit are both red, told apart by the SHAPE of the line.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img">
  <title>Same eight points, three models</title>
  <desc>Three panels side by side over the same eight data points. Panel 1 fits a flat line and underfits. Panel 2 fits a smooth curve. Panel 3 fits a jagged line through every point and overfits.</desc>
  <text x="400" y="42" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle">Same eight points. Three models.</text>
  <text x="149" y="68" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle">1. Underfit</text>
  <rect x="32" y="76" width="234" height="240" rx="12" fill="#FFFFFF" stroke="#CC2B1D" stroke-width="3" stroke-linejoin="round"/>
  <g transform="translate(41,86) scale(1.35)">
  <line x1="24" y1="18" x2="24" y2="126" stroke="#14202B" stroke-width="2"/>
  <line x1="24" y1="126" x2="146" y2="126" stroke="#14202B" stroke-width="2"/>
  <path d="M30 80 L142 80" fill="none" stroke="#CC2B1D" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="36" cy="110" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="52" cy="96" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="66" cy="102" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="82" cy="80" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="96" cy="72" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="112" cy="58" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="126" cy="64" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="140" cy="40" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <text x="85" y="148" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">too simple</text>
  </g>
  <text x="149" y="336" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">train low, test low</text>
  <text x="400" y="68" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle">2. Just right</text>
  <rect x="283" y="76" width="234" height="240" rx="12" fill="#FFFFFF" stroke="#1B7A4B" stroke-width="3" stroke-linejoin="round"/>
  <g transform="translate(292,86) scale(1.35)">
  <line x1="24" y1="18" x2="24" y2="126" stroke="#14202B" stroke-width="2"/>
  <line x1="24" y1="126" x2="146" y2="126" stroke="#14202B" stroke-width="2"/>
  <path d="M30 114 Q86 92 142 44" fill="none" stroke="#1B7A4B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="36" cy="110" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="52" cy="96" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="66" cy="102" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="82" cy="80" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="96" cy="72" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="112" cy="58" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="126" cy="64" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="140" cy="40" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <text x="85" y="148" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">just right</text>
  </g>
  <text x="400" y="336" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">train good, test good</text>
  <text x="651" y="68" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle">3. Overfit</text>
  <rect x="534" y="76" width="234" height="240" rx="12" fill="#FFFFFF" stroke="#CC2B1D" stroke-width="3" stroke-linejoin="round"/>
  <g transform="translate(543,86) scale(1.35)">
  <line x1="24" y1="18" x2="24" y2="126" stroke="#14202B" stroke-width="2"/>
  <line x1="24" y1="126" x2="146" y2="126" stroke="#14202B" stroke-width="2"/>
  <path d="M30 118 L36 110 L44 120 L52 96 L59 110 L66 102 L74 84 L82 80 L89 88 L96 72 L104 68 L112 58 L119 74 L126 64 L133 50 L140 40 L145 50" fill="none" stroke="#CC2B1D" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="36" cy="110" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="52" cy="96" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="66" cy="102" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="82" cy="80" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="96" cy="72" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="112" cy="58" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="126" cy="64" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="140" cy="40" r="4.5" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="1.5"/>
  <text x="85" y="148" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">memorised</text>
  </g>
  <text x="651" y="336" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">train perfect, test poor</text>
  <text x="400" y="372" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#55636F" text-anchor="middle">The dots never move. Only the line does &#8212; that is the whole idea of model complexity.</text>
</svg>
```

### `pattern-annotated-chart` &mdash; Practice hours vs test score, with one point called out

**Canvas** `0 0 500 500`. Axes with ticks and BOTH titles, grid lines under the marks, every axis numbered. Then exactly ONE annotation: a dashed accent ring, a leader with an arrowhead, and a label box that does not overlap a single data point. Route the leader through empty space &mdash; check every point before you commit the coordinates.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" role="img">
  <title>Practice hours vs test score, with one point called out</title>
  <desc>A scatter plot of ten students. Nine points rise to the right. One point, at three hours and a score of eight, is ringed and labelled with a note asking why.</desc>
  <text x="250" y="40" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle">Practice hours vs test score</text>
  <g stroke="#C7CDD4" stroke-width="1.5">
    <line x1="90" y1="308" x2="450" y2="308"/>
    <line x1="90" y1="236" x2="450" y2="236"/>
    <line x1="90" y1="164" x2="450" y2="164"/>
    <line x1="90" y1="92" x2="450" y2="92"/>
  </g>
  <text x="80" y="384" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">0</text>
  <text x="80" y="312" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">25</text>
  <text x="80" y="240" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">50</text>
  <text x="80" y="168" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">75</text>
  <text x="80" y="96" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">100</text>
  <g stroke="#55636F" stroke-width="1.5">
    <line x1="90" y1="380" x2="90" y2="386"/>
    <line x1="162" y1="380" x2="162" y2="386"/>
    <line x1="234" y1="380" x2="234" y2="386"/>
    <line x1="306" y1="380" x2="306" y2="386"/>
    <line x1="378" y1="380" x2="378" y2="386"/>
    <line x1="450" y1="380" x2="450" y2="386"/>
  </g>
  <text x="90" y="402" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">0</text>
  <text x="162" y="402" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">2</text>
  <text x="234" y="402" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">4</text>
  <text x="306" y="402" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">6</text>
  <text x="378" y="402" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">8</text>
  <text x="450" y="402" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">10</text>
  <circle cx="126" cy="340" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="162" cy="318" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="198" cy="300" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="234" cy="262" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="270" cy="250" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="306" cy="206" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="342" cy="200" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="378" cy="160" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="414" cy="128" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="198" cy="356" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="198" cy="356" r="15" fill="none" stroke="#C42B8C" stroke-width="2" stroke-dasharray="5 4"/>
  <line x1="282" y1="327" x2="212" y2="352" stroke="#C42B8C" stroke-width="2"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#C42B8C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" transform="translate(210 353) rotate(160)"/>
  <rect x="282" y="300" width="168" height="54" rx="10" fill="#FFFFFF" stroke="#C42B8C" stroke-width="2" stroke-linejoin="round"/>
  <text x="366" y="322" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle">This one practised 3 hours</text>
  <text x="366" y="342" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle">and scored 8. Ask why.</text>
  <line x1="90" y1="80" x2="90" y2="380" stroke="#14202B" stroke-width="2"/>
  <line x1="90" y1="380" x2="450" y2="380" stroke="#14202B" stroke-width="2"/>
  <text x="270" y="428" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#55636F" text-anchor="middle">Hours practised</text>
  <text x="48" y="235" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#55636F" text-anchor="middle" transform="rotate(-90 48 235)">Test score (out of 100)</text>
  <text x="250" y="468" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#55636F" text-anchor="middle">The ring marks the one point worth discussing.</text>
</svg>
```

### `pattern-structure` &mdash; One dictionary is one row

**Canvas** `0 0 800 400`. Show ONE record in full and the rest as offset cards behind it, then the whole structure on the right with the matching part highlighted. The highlight is what proves the mapping &mdash; without it this is two unrelated pictures.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img">
  <title>One dictionary is one row</title>
  <desc>On the left, a card showing three key to value pairs, with two more cards stacked behind it. An arrow labelled same information points right to a DataFrame whose first row is highlighted and holds those same three values.</desc>
  <text x="400" y="42" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle">One dictionary is one row</text>
  <rect x="66" y="122" width="228" height="150" rx="10" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5" stroke-linejoin="round"/>
  <rect x="51" y="107" width="228" height="150" rx="10" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5" stroke-linejoin="round"/>
  <rect x="36" y="92" width="228" height="150" rx="10" fill="#FFFFFF" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
  <rect x="50" y="108" width="88" height="32" rx="8" fill="#F4D5E9" stroke="#C42B8C" stroke-width="2" stroke-linejoin="round"/>
  <text x="94" y="124" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">player</text>
  <line x1="144" y1="124" x2="166" y2="124" stroke="#14202B" stroke-width="2" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" transform="translate(166 124) rotate(0)"/>
  <rect x="170" y="108" width="80" height="32" rx="8" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2" stroke-linejoin="round"/>
  <text x="210" y="124" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Meera</text>
  <rect x="50" y="150" width="88" height="32" rx="8" fill="#F4D5E9" stroke="#C42B8C" stroke-width="2" stroke-linejoin="round"/>
  <text x="94" y="166" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">runs</text>
  <line x1="144" y1="166" x2="166" y2="166" stroke="#14202B" stroke-width="2" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" transform="translate(166 166) rotate(0)"/>
  <rect x="170" y="150" width="80" height="32" rx="8" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2" stroke-linejoin="round"/>
  <text x="210" y="166" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">48</text>
  <rect x="50" y="192" width="88" height="32" rx="8" fill="#F4D5E9" stroke="#C42B8C" stroke-width="2" stroke-linejoin="round"/>
  <text x="94" y="208" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">over</text>
  <line x1="144" y1="208" x2="166" y2="208" stroke="#14202B" stroke-width="2" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" transform="translate(166 208) rotate(0)"/>
  <rect x="170" y="192" width="80" height="32" rx="8" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2" stroke-linejoin="round"/>
  <text x="210" y="208" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">12</text>
  <text x="150" y="292" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle">one dict</text>
  <text x="150" y="314" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">keys are the column names</text>
  <g transform="translate(300,150) scale(0.9)">
  <line x1="6" y1="20" x2="84" y2="20" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="76,10 92,20 76,30" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="342" y="146" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">same data</text>
  <rect x="420" y="100" width="40" height="34" fill="#F5F8FA"/>
  <rect x="460" y="100" width="100" height="34" fill="#D9EAF9"/>
  <rect x="560" y="100" width="100" height="34" fill="#D9EAF9"/>
  <rect x="660" y="100" width="100" height="34" fill="#D9EAF9"/>
  <rect x="420" y="134" width="40" height="36" fill="#F5F8FA"/>
  <rect x="420" y="170" width="40" height="36" fill="#F5F8FA"/>
  <rect x="420" y="206" width="40" height="36" fill="#F5F8FA"/>
  <rect x="460" y="134" width="300" height="36" fill="#F4D5E9"/>
  <g stroke="#C7CDD4" stroke-width="1.5">
    <line x1="460" y1="100" x2="460" y2="242"/>
    <line x1="560" y1="100" x2="560" y2="242"/>
    <line x1="660" y1="100" x2="660" y2="242"/>
    <line x1="420" y1="170" x2="760" y2="170"/>
    <line x1="420" y1="206" x2="760" y2="206"/>
  </g>
  <line x1="420" y1="134" x2="760" y2="134" stroke="#14202B" stroke-width="2"/>
  <text x="510" y="117" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central" font-weight="600">player</text>
  <text x="610" y="117" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central" font-weight="600">runs</text>
  <text x="710" y="117" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central" font-weight="600">over</text>
  <text x="440" y="152" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
  <text x="510" y="152" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Meera</text>
  <text x="610" y="152" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">48</text>
  <text x="710" y="152" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">12</text>
  <text x="440" y="188" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">1</text>
  <text x="510" y="188" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Kabir</text>
  <text x="610" y="188" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">31</text>
  <text x="710" y="188" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">9</text>
  <text x="440" y="224" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">2</text>
  <text x="510" y="224" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Nova</text>
  <text x="610" y="224" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">57</text>
  <text x="710" y="224" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">15</text>
  <rect x="420" y="134" width="340" height="36" fill="none" stroke="#C42B8C" stroke-width="3"/>
  <rect x="420" y="100" width="340" height="142" fill="none" stroke="#14202B" stroke-width="3"/>
  <text x="590" y="292" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle">one DataFrame</text>
  <text x="590" y="314" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">each dict became row 0, 1, 2</text>
  <text x="400" y="372" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#55636F" text-anchor="middle">A list of dicts and a DataFrame hold the same thing. pandas just adds the index.</text>
</svg>
```

### `pattern-error-fix` &mdash; Read the last line, change one thing, run again

**Canvas** `0 0 800 400`. The failing artefact on the left, the working one on the right, an arrow between them, and a one-line diagnosis under each. The right panel must show the SAME program, so the reader can see that only one thing changed. Both panels sit at scale 1.0 &mdash; shrinking a terminal panel would drop its 12px mono text below the floor.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img">
  <title>Read the last line, change one thing, run again</title>
  <desc>On the left, a red-outlined traceback panel with the failing line highlighted and arrowed. On the right, a green-outlined terminal showing the same program running and printing total: 90.</desc>
  <text x="400" y="42" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle">Read the last line, change one thing, run again</text>
  <g transform="translate(16,80)">
  <path d="M14 26 A10 10 0 0 1 24 16 H296 A10 10 0 0 1 306 26 V46 H14 Z" fill="#F6AEA6"/>
  <g stroke="#CC2B1D" stroke-width="2.5" stroke-linecap="round">
    <line x1="26" y1="26" x2="36" y2="36"/>
    <line x1="36" y1="26" x2="26" y2="36"/>
  </g>
  <text x="46" y="35" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B">Traceback</text>
  <line x1="14" y1="46" x2="306" y2="46" stroke="#14202B" stroke-width="2"/>
  <rect x="22" y="98" width="272" height="22" rx="4" fill="#F6AEA6"/>
  <text x="26" y="68" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12" fill="#55636F">Traceback (most recent call last):</text>
  <text x="26" y="90" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12" fill="#55636F">  File "pay.py", line 4, in &lt;module&gt;</text>
  <text x="26" y="112" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12" fill="#14202B">    total = price * quantity</text>
  <text x="26" y="140" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12" fill="#CC2B1D" font-weight="600">NameError: name 'quantity'</text>
  <text x="26" y="158" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12" fill="#CC2B1D" font-weight="600">is not defined</text>
  <rect x="14" y="16" width="292" height="160" rx="10" fill="none" stroke="#CC2B1D" stroke-width="3"/>
  <line x1="390" y1="109" x2="314" y2="109" stroke="#CC2B1D" stroke-width="3" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#CC2B1D" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(314 109) rotate(180)"/>
  <text x="312" y="92" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B">this line</text>
  <text x="160" y="196" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">Read the last line first.</text>
  </g>
  <g transform="translate(424,172) scale(0.5)">
  <line x1="6" y1="20" x2="84" y2="20" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="76,10 92,20 76,30" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <rect x="478" y="96" width="292" height="176" rx="10" fill="#FFFFFF" stroke="#1B7A4B" stroke-width="3" stroke-linejoin="round"/>
  <path d="M478 106 A10 10 0 0 1 488 96 H760 A10 10 0 0 1 770 106 V126 H478 Z" fill="#E2F7ED"/>
  <polyline points="492,112 498,118 510,104" fill="none" stroke="#1B7A4B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="478" y1="126" x2="770" y2="126" stroke="#14202B" stroke-width="2"/>
  <text x="520" y="116" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B">Terminal</text>
  <text x="494" y="158" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#55636F">&gt;</text>
  <text x="508" y="158" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#14202B">python pay.py</text>
  <text x="494" y="188" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#14202B">total: 90</text>
  <text x="494" y="218" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#55636F">&gt;</text>
  <rect x="508" y="206" width="9" height="14" fill="#14202B"/>
  <rect x="478" y="96" width="292" height="176" rx="10" fill="none" stroke="#1B7A4B" stroke-width="3"/>
  <text x="216" y="320" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle">Before: it stopped</text>
  <text x="624" y="320" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle">After: it ran</text>
  <text x="216" y="342" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">quantity was never given a value</text>
  <text x="624" y="342" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">one line added, above line 4</text>
  <text x="400" y="374" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#55636F" text-anchor="middle">Fix the reason the error names, not the line it happens on.</text>
</svg>
```


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
- [ ] `<title>` states the figure's takeaway, the markdown alt text describes what a sighted
      reader sees, and `<desc>` describes the *idea*. Alt and `<title>` may differ — alt says
      *what is drawn*, `<title>` says *what it means*. Both must be accurate and non-empty.
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
| `_motifs.svg` | Sprite sheet: all 31 motifs as `<symbol>`. Reference with `<use>` or copy inline. |
| `_preview.html` | Open in any browser. Renders the palette, every motif, the &sect;3 pair and every pattern, with greyscale and dark-page toggles. |
| `_generator/` | The source of truth. `STYLE.md`, `_motifs.svg` and `_preview.html` are all generated from it, so a motif can never disagree with its own snippet. Edit a motif here, then re-run the three commands below. |
| `fig-wNN-*.svg` | The week figures. |

```bash
cd _generator
python3 _gen_emit.py     # rewrites _motifs.svg and _preview.html
python3 _gen_style.py    # rewrites STYLE.md
python3 _gen_audit.py    # bounds, 12px floor, scale(), banned constructs, label collisions
```

---

## The Growing Map — `fig-wNN-0-where-this-fits.svg`

Every week carries **one** figure that is not about this week's content. It shows the learner the shape
of the whole level with one more piece filled in, and it appears in **both** books — the student guide
(`## 🧭 Where This Fits`) and the teacher guide (`### 🧭 The Growing Map`).

**Reference implementation: `fig-w01-0-where-this-fits.svg`.** Open it before drawing another.
Level 1 carries the same device with the same rules; see its `STYLE.md` for the full rationale.

### Index `0`

Content figures number from 1. The map is always `-0-`, so it sorts first and is instantly
identifiable as structural rather than topical. Caption is `Figure <week>.0`.

### Fixed zones — canvas `0 0 800 400`, no exceptions

| Zone | y | Holds |
|---|---|---|
| Banner | 42–62 | `A QUESTION → AN ANSWER YOU CAN DEFEND` + subtitle |
| Pipeline | 82–134 | Five stage boxes, `140 × 52`, at x **26 · 178 · 330 · 482 · 634**, arrows between |
| Tiles | 146–292 | Two tiles per stage: row A `140 × 58` at y 146, row B `140 × 48` at y 244 |
| Flow note | 312 | One line, 12px, `muted` |
| Thread strip | 336–360 | **Seven** pills, `103 × 24`, at x **20 · 129 · 238 · 347 · 456 · 565 · 674** |
| Footer | 378 | One sentence, 13px, `muted`, centred |

**Never move a box between weeks.** Week 4's figure and week 33's figure must put every box at the
same coordinates — the set is frames of one animation.

### The L2 spine — five stages, ten tiles, fixed forever

| Stage | x | Tile A (y 146) | Tile B (y 244) |
|---|--:|---|---|
| **SPEAK PYTHON** | 26 | print · variables · maths — wk 1–4 | choices · loops — wk 5–9 |
| **HOLD THE DATA** | 178 | functions · lists — wk 10–12 | dicts · rows · files — wk 13–18 |
| **CLEAN IT** | 330 | numpy · DataFrames — wk 19–22 | holes · duplicates — wk 23–24 |
| **SEE IT** | 482 | your first chart — wk 25 | honest axes — wk 26–27 |
| **PREDICT & CHECK** | 634 | X, y · kNN · trees — wk 28–31 | bake-off · capstone — wk 32–36 |

### State vocabulary — read progress from shape alone, never colour alone

| State | Stroke | Fill | Dash | Badge |
|---|---|---|---|---|
| **This week** | `#845F00` w3 | `#E8C671` | solid | white pill, `#1B7A4B` border, tick + `YOU ARE HERE` |
| **Already done** | `#14202B` w2 | white | solid | small `wk N–M` in `muted` |
| **Not yet** | `#C7CDD4` w3 | none | `stroke-dasharray="10 8"` | `wk N–M` in `muted` |
| **Stage containing this week** | `#14202B` w3 | white | solid | — (the badge lives on the tile, not the stage) |

Rules, not suggestions:

1. **Dashed means "not yet" and nothing else, ever.**
2. **Exactly one `YOU ARE HERE` badge**, belonging to the current tile — never to a stage box. It sits
   in that row's **fixed badge slot**: row A at `y=212` (immediately beneath the tile), row B at `y=266`
   (inside the tile). Both slots are inside the 146–292 tile zone. The difference is forced by geometry,
   not taste: row-A labels need two lines, and two lines plus a 22px badge do not fit in 58px. A badge
   must never appear at any other y.
3. **Done tiles are never re-tinted.** Done is done; only the current week is gold.
4. A stage box goes solid as soon as *any* of its tiles is reached, and stays solid.

### The seventh thread — an L2 extension

Level 1 and Level 3 use six threads. **Level 2 adds `toolcraft` at the front**, because weeks 1–9
teach programming as a craft and genuinely extend none of the six AI threads. Forcing them onto
`representation` would be dishonest.

- Weeks 1–9 light **`toolcraft` only**, and the footer says so.
- From week 10, light **at most two** of the seven. A week claiming three has not decided what it is about.
- Every thread must be lit at least twice across the 36 weeks.

### Accessibility

- `<title>` states what is filled in this week.
- `<desc>` describes **every zone** in words, including which threads are lit — a screen-reader user
  must get the same progress information a sighted reader gets from the dashes.
- Markdown alt text is **byte-identical** to `<title>`, in both books.

### Checklist before shipping one

- [ ] `viewBox="0 0 800 400"`, no `width`/`height`, transparent background
- [ ] Nothing outside x 20–780, y 20–380
- [ ] All `font-size` ≥ 12
- [ ] Only palette hexes from §1.1
- [ ] Exactly one `YOU ARE HERE`, in its row's badge slot (row A `y=212`, row B `y=266`)
- [ ] Dashed only on not-yet boxes
- [ ] ≤ 2 threads lit (weeks 1–9: `toolcraft` only)
- [ ] Every box at its spine coordinates, unmoved
- [ ] Parses as XML

> **⚠️ Do not run `_generator/_gen_audit.py` against these files.** It reports false positives on the
> map (and on the reference `fig-w01`) because it does not inherit `font-size`/`text-anchor` from a
> parent `<g>`, and it reads relative `l dx dy` path commands as absolute. Work the checklist by hand.

### Thread icons — canonical, identical in all three levels

One icon per thread, never shared. Normalised across all 108 student sections on 2026-09-26; a
collision (`📊` served both `data` and `evaluation`) was resolved in favour of each thread's own
dominant form.

| Thread | Icon |
|---|:--:|
| data | 📊 |
| representation | 🏷️ |
| model | 📦 |
| learning signal | 🎯 |
| evaluation | ⚖️ |
| impact | 🌍 |
| toolcraft *(Level 2 only)* | 🧰 |

Use these in the student guide's **Spiral thread** row and nowhere else. If you add a thread, give it a
new icon and check it against this table first — two threads sharing an icon defeats the point of
having them.

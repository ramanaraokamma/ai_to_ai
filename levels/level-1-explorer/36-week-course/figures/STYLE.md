# Figure style system &mdash; AI Academy, Level 1 (36-week course)

**Audience: the 12 authors drawing the ~150 SVG figures for this course.**
This file is the contract. If your figure disagrees with this file, this file wins.

Every number in here was measured, not guessed. The palette was validated with a
colour-blindness simulator and a greyscale print check; the receipts are in the tables below.

**The learner is one 11-year-old. The teacher does not know AI.** A figure has to land in
about four seconds with no caption. That is the bar.

---

## 0. The 30-second version

1. Copy a **composition pattern** (&sect;7) that matches your diagram type.
2. Drop in **motifs** (&sect;6) &mdash; do not draw your own robot.
3. Use only the eight **palette** colours (&sect;1), by *role*, never by taste.
4. Start every file with `<title>` and `<desc>` and `role="img"` (&sect;5).
5. Name it `fig-wNN-<n>-<slug>.svg` (&sect;8).
6. Run the pre-flight check (&sect;10) before you commit.

---

## 1. Palette

Eight named colours. **Use them by role, never "because it looks nice".**

Each role has a **stroke** (outlines, text, marks) and most have a **fill** (the pale tint inside
a shape). This two-tier split is deliberate and load-bearing &mdash; see &sect;1.2.

| Role | Stroke | Fill | Contrast on white | Greyscale (stroke) | Greyscale (fill) | Use it for |
|---|---|---|---|---|---|---|
| **data** | `#1F6FB2` | `#D9EAF9` | 5.28:1 | 108 | **232** | Data, examples, inputs, photos, tables, anything measured |
| **model** | `#6D28D9` | `#DBCEF3` | 7.10:1 | 88 | **212** | The model, the brain, the learned thing, the "machine" |
| **human** | `#845F00` | `#E8C671` | 5.80:1 | 101 | **202** | People, hands, choices a person makes, notes, ideas |
| **correct** | `#1B7A4B` | `#E2F7ED` | 5.34:1 | 107 | **242** | Right answers, passing, "after the fix", good outcomes |
| **wrong** | `#CC2B1D` | `#F6AEA6` | 5.34:1 | 107 | **192** | Wrong answers, errors, bias, "before the fix", warnings |
| **accent** | `#C42B8C` | `#F4D5E9` | 5.16:1 | 109 | **222** | Callout numbers, pins, the one thing to look at first |
| **ink** | `#14202B` | &mdash; | 16.52:1 | 31 | &mdash; | All body text, neutral outlines, arrows |
| **paper** | `#FFFFFF` | &mdash; | &mdash; | 255 | &mdash; | Nothing. It is the background you never draw. |

Two supporting neutrals (not "colours", they carry no meaning):

| Name | Hex | Contrast on white | Greyscale | Use it for |
|---|---|---|---|---|
| **muted** | `#55636F` | 6.18:1 | 97 | Captions, axis numbers, secondary labels |
| **grid** | `#C7CDD4` | 1.60:1 | 204 | Grid lines, dashed dividers, panel outlines |
| **panel** | `#F5F8FA` | 1.07:1 | 248 | A tinted background panel behind a scene |

"Greyscale" = the 0&ndash;255 grey value the colour becomes when the page is printed black-and-white
(sRGB luminance, re-encoded). **This is the verifiable print check**: convert your figure to
greyscale and the numbers above are what you should measure.

### 1.1 Every stroke passes WCAG AA on white

All six role strokes sit between **5.16:1 and 7.10:1** against white, so they clear the AA 4.5:1
threshold *for text*, not merely the 3:1 threshold for shapes. That means you may safely set a
label in any role colour. `ink` on white is 16.52:1; `muted` is 6.18:1.

Ink on any role fill also clears AA comfortably (worst case `ink` on `wrong` fill = **9.06:1**),
so text is always legible inside a tinted box.

### 1.2 Why strokes and fills are split (read this once)

The two requirements &mdash; *AA-legible on white* and *distinguishable in greyscale* &mdash; pull in
opposite directions. Any colour dark enough to pass AA on white lands in a narrow luminance band,
so **all six strokes print as virtually the same grey (88&ndash;109)**.

That is not a bug; it is the design. In print, all outlines read as one consistent ink weight, which
is what makes line art look clean. **Hue therefore never carries meaning on its own.** The meaning
is carried by the *fill luminance ladder*, which was deliberately spread:

```
wrong 192  <  human 202  <  model 212  <  accent 222  <  data 232  <  correct 242
```

Even steps of 10 grey levels, with the two pairs that matter most spread furthest apart:

- **correct (242) vs wrong (192) &mdash; 50 levels.** Unmistakable in print, in addition to the tick/cross shapes.
- **data (232) vs model (212) &mdash; 20 levels.** The pipeline pair, always distinguishable.

Fills are pale on purpose and **never define an edge** &mdash; the 3px stroke does. So a fill being
close to white costs you nothing.

### 1.3 Which colour pairs are safe together

Measured as OKLab &Delta;E&times;100, under normal vision and under simulated red/green colour
blindness (protanopia and deuteranopia, Machado 2009 at full severity). A pair passes when
normal &ge; 15 **and** colour-blind &ge; 8.

**12 of the 15 pairs pass both gates**, including both critical ones:

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
| data / accent | 26.2 | 8.3 | pass |
| wrong / accent | 14.8 | 14.1 | **needs shape + label** |
| human / correct | 13.2 | 6.7 | **needs shape + label** |
| human / wrong | 16.3 | 4.7 | **needs shape + label** |

The three weak pairs are unavoidable: `human` is a warm ochre, and to a red-blind reader warm ochre
and red converge &mdash; that is human eye physiology, not a bad hex pick. It is safe here because
**`human` is a character colour (faces, hands, notes), never a chart series**, so the shape of a face
already tells you what it is. If you ever need ochre and red to be told apart *as data*, you must add
a label or a different marker shape. You must do that anyway (&sect;9).

### 1.4 Charts: use at most three role colours

Six hues cannot all be mutually distinguishable; that is a measured limit, not a preference.
For any chart where marks are compared **all against all** (scatter, bubble, multi-series bar),
pick one of these validated triples:

- `data` + `correct` + `wrong` (17.6 / 9.1) &larr; the usual choice
- `model` + `correct` + `wrong` (28.4 / 9.1)
- `data` + `model` + `human` (17.7 / 8.4)
- `model` + `human` + `accent` (22.0 / 13.1)

Need a fourth category? Fold it into "Other", or split into two charts. Do not invent a seventh colour.

### 1.5 The one sanctioned exception: when the colour *is* the lesson

Weeks 23&ndash;26 teach that a picture is a grid of numbers. In the figures for those weeks the colour
value is not decoration and it is not a *role* &mdash; **it is the data being taught.** So two narrow
exceptions are allowed, and only these two:

| Exception | Where it is used today | Why the palette cannot be used instead |
|---|---|---|
| **Literal RGB primaries** &mdash; `#FF0000`, `#00FF00`, `#0000FF` and their pairwise mixes `#FFFF00`, `#00FFFF`, `#FF00FF` | **5 figures, all in Week 24:** `fig-w24-1`, `-2`, `-6`, `-8`, `-10` | You cannot teach "the red channel is 255" in a swatch that is not red. The swatch *is* the claim. |
| **A brightness ramp** &mdash; near-neutral greys, tinted very slightly toward `ink`, stepped to show brightness (`#EFF0F1` &hellip; `#18232E`) | **13 figures in Weeks 23&ndash;24:** the pixel grids, shading keys and resolution ladders | A pixel of brightness 128 must be *painted* brightness 128. A palette tint would state a false number. |

Rules that still apply inside the exception:

- The number must be **printed next to the swatch**. The colour never carries the meaning alone
  &mdash; that is §9, and it is not waived. A grey square with no `128` beside it is a defect.
- Everything *around* the exception &mdash; outlines, labels, arrows, callouts, panels &mdash; stays on
  the §1 palette: `ink` outlines, `muted` captions, `accent` pins.
- The ramp is **tinted toward `ink`, not pure `#808080`-style grey**, so it still reads as part of
  this palette family rather than as a foreign greyscale.
- **This is the complete list: 16 files.** If you find yourself wanting a seventeenth exception in
  Week 8, you want a different diagram (§1.4).

---

## 2. Canvas rules

Three standard canvases. Pick the closest one; do not invent sizes.

| Name | viewBox | Use for |
|---|---|---|
| **wide** | `0 0 800 400` | Pipelines, comparisons, decision trees, scenes |
| **square** | `0 0 500 500` | Pixel grids, charts, single-idea diagrams |
| **tall** | `0 0 500 700` | Step-by-step stacks, long trees, sorted lists |

Rules:

- **Never set `width` or `height` on the root `<svg>`.** viewBox only, so the figure scales to whatever
  column it lands in, in print or on screen.
- **20px of internal padding.** Nothing except a deliberate full-bleed background touches the edge.
  On a wide canvas your live area is x 20&ndash;780, y 20&ndash;380.
- **Transparent background.** Do not paint a white rect over the canvas &mdash; it breaks dark mode and
  wastes ink. If you want a tinted panel, use `panel` `#F5F8FA` on a rounded rect *inside* the padding.
- Root element, always exactly this shape:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img">
  <title>...</title>
  <desc>...</desc>
  <!-- figure goes here -->
</svg>
```

---

## 3. Line and shape

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

Two habits that matter:

- **Draw connectors first, boxes second.** Then lines tuck under boxes instead of crossing them.
- **A stroke's job is the edge; a fill's job is the tint.** Every meaningful shape gets both.

---

## 4. Type

**System fonts only. Never a webfont, never `@font-face`, never Google Fonts.** The book must render
identically offline and on a school printer.

```
font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
```

| Level | Size | Colour | Use |
|---|---|---|---|
| Title | `24` | `ink` | One per figure, top-centre |
| Label | `18` | `ink` | Names of boxes, stages, axes |
| Caption | `14` | `muted` | The one-line takeaway at the bottom |
| Tiny | `12` | `muted` | Axis numbers, cell values, legend text |

Never go below 12. At print scale, 12 is already small.

### Anchoring and vertical centring

- **Horizontal:** use `text-anchor` &mdash; `middle` for centred, `start` (default) for left-aligned,
  `end` for right-aligned numbers such as a y-axis. Never fake centring by guessing an x offset.
- **Vertical:** `y` is the *baseline*, not the middle. To centre text in a box use
  `dominant-baseline="central"` and set `y` to the box's centre.

```svg
<!-- centred in a box spanning y 62..118, so centre y = 90 -->
<text x="400" y="90" font-size="18" fill="#14202B"
      text-anchor="middle" dominant-baseline="central">Has feathers?</text>
```

**Print fallback:** a few older print renderers ignore `dominant-baseline`. If a figure is going to
print and you want to be bulletproof, drop `dominant-baseline` and set the baseline manually:

```
y = centre + fontSize * 0.35     (e.g. centre 90, size 18  ->  y = 96.3)
```

- Rotate axis titles with `transform="rotate(-90 x y)"` about the text's own anchor point.
- **Never** rely on text wrapping &mdash; SVG has none. Break lines yourself with separate `<text>`
  elements about `fontSize * 1.35` apart.

---

## 5. Accessibility

**Every figure starts with `<title>` then `<desc>`, and carries `role="img"`.** No exceptions.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img">
  <title>How a trained model answers</title>
  <desc>Three stages left to right: a stack of photos goes into a machine,
        and the machine puts out a correct badge.</desc>
  <!-- figure goes here -->
</svg>
```

- **`<title>`** = the figure's name. Short. Matches the caption in the teacher file.
- **`<desc>`** = what a person who cannot see it would need told. Describe the *content and the point*,
  not the shapes. "Three stages left to right..." is right; "two rectangles and a circle" is useless.
- **The markdown alt text must agree with `<title>`.** When you embed the figure, write:

```markdown
![A real pattern repeats; a coincidence happened once](../figures/fig-w07-1-pattern-vs-coincidence.svg)
*Figure 7.1 — A pattern repeats. A coincidence happened once.*
```

  Same words as `<title>`. Note the path: every markdown file in `teacher-guide/`,
  `student-guide/` and `workbook/` sits one directory below `figures/`, so the link
  always starts `../figures/`. Every embed gets an italic caption line directly
  underneath, numbered `Figure <week>.<n>`.
  If a teacher reads the alt text aloud, the class should still follow.
- Decorative motifs *inside* a figure need nothing extra &mdash; the parent `<desc>` covers them.
- If you `<use>` a motif standalone, label it: `<use href="_motifs.svg#motif-robot" aria-label="Robot"/>`.

---

## 6. Motif library

Sixteen reusable pieces. **Do not redraw these.** Consistency across 150 figures is the whole point.

Two ways to use them:

```svg
<!-- A) reference the sprite sheet -->
<use href="_motifs.svg#motif-robot" x="600" y="150" width="100" height="100"/>

<!-- B) copy the <g> inline (below) and position it -->
<g transform="translate(600,150)">...</g>
<g transform="translate(600,150) scale(1.4)">...</g>   <!-- scaled -->
```

Every motif is drawn to its own viewBox with **the origin at the top-left**, so
`translate(x,y)` puts its top-left corner at exactly `(x,y)`. Scale uniformly; never stretch one axis.

### `motif-robot` &mdash; Friendly robot

viewBox `0 0 100 100` (100&times;100). A friendly cartoon robot with an antenna, two eyes, a smile, and two arms.

```svg
<g transform="translate(0,0)">
<line x1="50" y1="16" x2="50" y2="7" stroke="#1F6FB2" stroke-width="3" stroke-linecap="round"/>
    <circle cx="50" cy="5" r="4" fill="#F4D5E9" stroke="#C42B8C" stroke-width="2"/>
    <rect x="22" y="16" width="56" height="40" rx="12" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
    <circle cx="38" cy="34" r="5" fill="#14202B"/>
    <circle cx="62" cy="34" r="5" fill="#14202B"/>
    <path d="M40 45 Q50 52 60 45" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
    <rect x="28" y="60" width="44" height="30" rx="10" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
    <line x1="28" y1="68" x2="13" y2="78" stroke="#1F6FB2" stroke-width="3" stroke-linecap="round"/>
    <line x1="72" y1="68" x2="87" y2="78" stroke="#1F6FB2" stroke-width="3" stroke-linecap="round"/>
    <circle cx="50" cy="75" r="6" fill="#F4D5E9" stroke="#C42B8C" stroke-width="2"/>
</g>
```

### `motif-child` &mdash; Child's face

viewBox `0 0 100 100` (100&times;100). A smiling child's face with short hair.

```svg
<g transform="translate(0,0)">
<circle cx="50" cy="52" r="30" fill="#E8C671" stroke="#845F00" stroke-width="3"/>
    <path d="M20 44 A30 30 0 0 1 80 44 A34 22 0 0 0 20 44 Z" fill="#845F00" stroke="#845F00" stroke-width="3" stroke-linejoin="round"/>
    <circle cx="40" cy="50" r="4" fill="#14202B"/>
    <circle cx="60" cy="50" r="4" fill="#14202B"/>
    <path d="M39 63 Q50 72 61 63" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
</g>
```

### `motif-lightbulb` &mdash; Lightbulb (an idea)

viewBox `0 0 100 100` (100&times;100). A glowing lightbulb with rays, meaning an idea.

```svg
<g transform="translate(0,0)">
<g stroke="#845F00" stroke-width="3" stroke-linecap="round">
      <line x1="50" y1="8" x2="50" y2="2"/>
      <line x1="22" y1="18" x2="17" y2="13"/>
      <line x1="78" y1="18" x2="83" y2="13"/>
      <line x1="14" y1="44" x2="7" y2="44"/>
      <line x1="86" y1="44" x2="93" y2="44"/>
    </g>
    <circle cx="50" cy="44" r="26" fill="#E8C671" stroke="#845F00" stroke-width="3"/>
    <path d="M42 56 L45 66 L55 66 L58 56" fill="none" stroke="#845F00" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="41" y="66" width="18" height="10" rx="3" fill="#FFFFFF" stroke="#845F00" stroke-width="3" stroke-linejoin="round"/>
    <rect x="44" y="78" width="12" height="8" rx="3" fill="#FFFFFF" stroke="#845F00" stroke-width="3" stroke-linejoin="round"/>
</g>
```

### `motif-table` &mdash; Data table

viewBox `0 0 100 100` (100&times;100). A small data table with a shaded header row and six cells.

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

### `motif-photos` &mdash; Stack of photo cards

viewBox `0 0 100 100` (100&times;100). Three photo cards in a stack, the top one showing a sun and a hill.

```svg
<g transform="translate(0,0)">
<g transform="rotate(-11 50 54) translate(-5 -7)">
      <rect x="24" y="26" width="52" height="52" rx="7" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
    </g>
    <g transform="rotate(7 50 54) translate(6 -4)">
      <rect x="24" y="26" width="52" height="52" rx="7" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
    </g>
    <rect x="24" y="26" width="52" height="52" rx="7" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
    <rect x="30" y="32" width="40" height="30" rx="4" fill="#D9EAF9" stroke="none"/>
    <circle cx="42" cy="42" r="5" fill="#E8C671" stroke="#845F00" stroke-width="2"/>
    <path d="M30 62 L44 50 L54 58 L62 52 L70 62 Z" fill="#1F6FB2" stroke="none"/>
    <rect x="30" y="32" width="40" height="30" rx="4" fill="none" stroke="#1F6FB2" stroke-width="2"/>
    <line x1="32" y1="70" x2="56" y2="70" stroke="#55636F" stroke-width="3" stroke-linecap="round"/>
</g>
```

### `motif-arrow` &mdash; Arrow pointing right

viewBox `0 0 100 40` (100&times;40). A straight arrow pointing to the right.

```svg
<g transform="translate(0,0)">
<line x1="6" y1="20" x2="84" y2="20" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
    <polyline points="76,10 92,20 76,30" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
</g>
```

### `motif-arrow-curved` &mdash; Curved arrow

viewBox `0 0 100 60` (100&times;60). A curved arrow that loops up and over to the right.

```svg
<g transform="translate(0,0)">
<path d="M8 48 Q48 2 84 34" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
    <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(84 34) rotate(41)"/>
</g>
```

### `motif-magnifier` &mdash; Magnifying glass

viewBox `0 0 100 100` (100&times;100). A magnifying glass, meaning look closely or search.

```svg
<g transform="translate(0,0)">
<line x1="60" y1="60" x2="86" y2="86" stroke="#1F6FB2" stroke-width="7" stroke-linecap="round"/>
    <circle cx="42" cy="42" r="26" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3"/>
    <path d="M30 36 A14 14 0 0 1 42 28" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
</g>
```

### `motif-brain` &mdash; Brain

viewBox `0 0 100 100` (100&times;100). A cartoon brain with folds, meaning thinking or a model.

```svg
<g transform="translate(0,0)">
<path d="M50 14 C34 14 24 24 24 36 C13 41 12 55 22 62 C22 76 34 87 50 87 C66 87 78 76 78 62 C88 55 87 41 76 36 C76 24 66 14 50 14 Z"
          fill="#DBCEF3" stroke="#6D28D9" stroke-width="3" stroke-linejoin="round"/>
    <line x1="50" y1="15" x2="50" y2="86" stroke="#6D28D9" stroke-width="3" stroke-linecap="round"/>
    <g fill="none" stroke="#6D28D9" stroke-width="2.5" stroke-linecap="round">
      <path d="M37 28 C45 33 45 43 37 47"/>
      <path d="M63 28 C55 33 55 43 63 47"/>
      <path d="M35 57 C45 61 45 71 37 75"/>
      <path d="M65 57 C55 61 55 71 63 75"/>
    </g>
</g>
```

### `motif-scale` &mdash; Balance scale

viewBox `0 0 100 100` (100&times;100). A balance scale with two level pans, meaning fairness or weighing two sides.

```svg
<g transform="translate(0,0)">
<line x1="50" y1="26" x2="50" y2="80" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
    <path d="M32 88 L38 80 H62 L68 88 Z" fill="#F5F8FA" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
    <line x1="16" y1="26" x2="84" y2="26" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
    <circle cx="50" cy="26" r="5" fill="#F4D5E9" stroke="#C42B8C" stroke-width="2.5"/>
    <line x1="16" y1="26" x2="16" y2="44" stroke="#55636F" stroke-width="2" stroke-linecap="round"/>
    <line x1="84" y1="26" x2="84" y2="44" stroke="#55636F" stroke-width="2" stroke-linecap="round"/>
    <path d="M2 44 Q16 62 30 44 Z" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
    <path d="M70 44 Q84 62 98 44 Z" fill="#E8C671" stroke="#845F00" stroke-width="3" stroke-linejoin="round"/>
</g>
```

### `motif-badge-check` &mdash; Correct badge

viewBox `0 0 100 100` (100&times;100). A round badge with a tick inside, meaning correct.

```svg
<g transform="translate(0,0)">
<circle cx="50" cy="50" r="34" fill="#E2F7ED" stroke="#1B7A4B" stroke-width="3"/>
    <polyline points="34,52 45,64 68,38" fill="none" stroke="#1B7A4B" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
</g>
```

### `motif-badge-cross` &mdash; Wrong badge

viewBox `0 0 100 100` (100&times;100). A round badge with a cross inside, meaning wrong.

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

```svg
<g transform="translate(0,0)">
<rect x="6" y="10" width="108" height="60" rx="10" fill="#F5F8FA" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
    <text x="60" y="40" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">Label</text>
</g>
```

### `motif-note` &mdash; Sticky note

viewBox `0 0 100 100` (100&times;100). A sticky note with a folded corner and three lines of writing.

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

### `motif-thought` &mdash; Thought bubble

viewBox `0 0 120 100` (120&times;100). A cloud-shaped thought bubble with two small trailing bubbles.

```svg
<g transform="translate(0,0)">
<circle cx="22" cy="88" r="5" fill="#FFFFFF" stroke="#14202B" stroke-width="2.5"/>
    <circle cx="34" cy="76" r="7" fill="#FFFFFF" stroke="#14202B" stroke-width="2.5"/>
    <path d="M40 66 C24 66 18 50 30 43 C24 27 44 16 56 25 C64 10 92 14 92 31 C108 34 106 58 90 60 C86 70 64 72 56 66 Z"
          fill="#FFFFFF" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
</g>
```

### `motif-machine` &mdash; Machine with input and output

viewBox `0 0 140 100` (140&times;100). A machine box with a gear inside, an input slot on the left and an output slot on the right.

```svg
<g transform="translate(0,0)">
<line x1="2" y1="48" x2="14" y2="48" stroke="#1F6FB2" stroke-width="3" stroke-linecap="round"/>
    <polyline points="10,42 18,48 10,54" fill="none" stroke="#1F6FB2" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <line x1="122" y1="48" x2="132" y2="48" stroke="#1B7A4B" stroke-width="3" stroke-linecap="round"/>
    <polyline points="128,42 136,48 128,54" fill="none" stroke="#1B7A4B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="28" y="14" width="84" height="72" rx="12" fill="#F5F8FA" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
    <rect x="18" y="38" width="14" height="20" rx="4" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
    <rect x="108" y="38" width="14" height="20" rx="4" fill="#E2F7ED" stroke="#1B7A4B" stroke-width="3" stroke-linejoin="round"/>
    <g stroke="#14202B" stroke-width="3" stroke-linecap="round">
      <line x1="84" y1="50" x2="89" y2="50"/>
      <line x1="79.9" y1="59.9" x2="83.4" y2="63.4"/>
      <line x1="70" y1="64" x2="70" y2="69"/>
      <line x1="60.1" y1="59.9" x2="56.6" y2="63.4"/>
      <line x1="56" y1="50" x2="51" y2="50"/>
      <line x1="60.1" y1="40.1" x2="56.6" y2="36.6"/>
      <line x1="70" y1="36" x2="70" y2="31"/>
      <line x1="79.9" y1="40.1" x2="83.4" y2="36.6"/>
    </g>
    <circle cx="70" cy="50" r="14" fill="#FFFFFF" stroke="#14202B" stroke-width="3"/>
    <circle cx="70" cy="50" r="5" fill="#DBCEF3" stroke="#6D28D9" stroke-width="2.5"/>
</g>
```


---

## 7. Composition patterns

Six diagram types cover essentially every figure in this course. Start from the matching skeleton
and swap the content. Each one below is a complete, valid SVG.

### `pattern-pipeline` &mdash; Pipeline: photos in, machine, answer out

**Canvas** `0 0 800 400`. Three stages, equal boxes, arrows in the gaps. Number every stage so the order survives greyscale.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img">
  <title>Pipeline: photos in, machine, answer out</title>
  <desc>Three stages left to right: a stack of photos goes into a machine, and the machine puts out a correct badge.</desc>
<text x="400" y="46" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle">How a trained model answers</text>
  <rect x="40" y="100" width="180" height="190" rx="12" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3"/>
  <rect x="310" y="100" width="180" height="190" rx="12" fill="#FFFFFF" stroke="#14202B" stroke-width="3"/>
  <rect x="580" y="100" width="180" height="190" rx="12" fill="#FFFFFF" stroke="#1B7A4B" stroke-width="3"/>
  <g transform="translate(80,125)">
    <g transform="rotate(-11 50 54) translate(-5 -7)">
    <rect x="24" y="26" width="52" height="52" rx="7" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
    </g>
    <g transform="rotate(7 50 54) translate(6 -4)">
    <rect x="24" y="26" width="52" height="52" rx="7" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
    </g>
    <rect x="24" y="26" width="52" height="52" rx="7" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
    <rect x="30" y="32" width="40" height="30" rx="4" fill="#D9EAF9" stroke="none"/>
    <circle cx="42" cy="42" r="5" fill="#E8C671" stroke="#845F00" stroke-width="2"/>
    <path d="M30 62 L44 50 L54 58 L62 52 L70 62 Z" fill="#1F6FB2" stroke="none"/>
    <rect x="30" y="32" width="40" height="30" rx="4" fill="none" stroke="#1F6FB2" stroke-width="2"/>
    <line x1="32" y1="70" x2="56" y2="70" stroke="#55636F" stroke-width="3" stroke-linecap="round"/>
  </g>
  <g transform="translate(330,130)">
    <line x1="2" y1="48" x2="14" y2="48" stroke="#1F6FB2" stroke-width="3" stroke-linecap="round"/>
    <polyline points="10,42 18,48 10,54" fill="none" stroke="#1F6FB2" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <line x1="122" y1="48" x2="132" y2="48" stroke="#1B7A4B" stroke-width="3" stroke-linecap="round"/>
    <polyline points="128,42 136,48 128,54" fill="none" stroke="#1B7A4B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="28" y="14" width="84" height="72" rx="12" fill="#F5F8FA" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
    <rect x="18" y="38" width="14" height="20" rx="4" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
    <rect x="108" y="38" width="14" height="20" rx="4" fill="#E2F7ED" stroke="#1B7A4B" stroke-width="3" stroke-linejoin="round"/>
    <g stroke="#14202B" stroke-width="3" stroke-linecap="round">
    <line x1="84" y1="50" x2="89" y2="50"/>
    <line x1="79.9" y1="59.9" x2="83.4" y2="63.4"/>
    <line x1="70" y1="64" x2="70" y2="69"/>
    <line x1="60.1" y1="59.9" x2="56.6" y2="63.4"/>
    <line x1="56" y1="50" x2="51" y2="50"/>
    <line x1="60.1" y1="40.1" x2="56.6" y2="36.6"/>
    <line x1="70" y1="36" x2="70" y2="31"/>
    <line x1="79.9" y1="40.1" x2="83.4" y2="36.6"/>
    </g>
    <circle cx="70" cy="50" r="14" fill="#FFFFFF" stroke="#14202B" stroke-width="3"/>
    <circle cx="70" cy="50" r="5" fill="#DBCEF3" stroke="#6D28D9" stroke-width="2.5"/>
  </g>
  <g transform="translate(620,125)">
    <circle cx="50" cy="50" r="34" fill="#E2F7ED" stroke="#1B7A4B" stroke-width="3"/>
    <polyline points="34,52 45,64 68,38" fill="none" stroke="#1B7A4B" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="130" y="262" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle">1. Input</text>
  <text x="400" y="262" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle">2. Model</text>
  <text x="670" y="262" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle">3. Output</text>
  <g transform="translate(228,175) scale(0.62)">
    <line x1="6" y1="20" x2="84" y2="20" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
    <polyline points="76,10 92,20 76,30" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <g transform="translate(498,175) scale(0.62)">
    <line x1="6" y1="20" x2="84" y2="20" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
    <polyline points="76,10 92,20 76,30" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="400" y="340" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#55636F" text-anchor="middle">The model never sees the answer - it only sees the photo and guesses.</text>
</svg>
```

### `pattern-comparison` &mdash; Comparison: before and after

**Canvas** `0 0 800 400`. Mirror the two panels exactly so only the content differs. The badge shape - not the colour - says which side is which.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img">
  <title>Comparison: before and after</title>
  <desc>Two panels side by side. The left panel is labelled Before and marked wrong; the right is labelled After and marked correct.</desc>
<text x="400" y="46" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle">Before and after we fixed the training data</text>
  <line x1="400" y1="80" x2="400" y2="336" stroke="#C7CDD4" stroke-width="1.5" stroke-dasharray="6 6"/>
  <rect x="40" y="80" width="330" height="240" rx="12" fill="#F6AEA6" stroke="#CC2B1D" stroke-width="3"/>
  <rect x="430" y="80" width="330" height="240" rx="12" fill="#E2F7ED" stroke="#1B7A4B" stroke-width="3"/>
  <g transform="translate(62,96) scale(0.44)">
    <circle cx="50" cy="50" r="34" fill="#F6AEA6" stroke="#CC2B1D" stroke-width="3"/>
    <g stroke="#CC2B1D" stroke-width="6" stroke-linecap="round">
    <line x1="38" y1="38" x2="62" y2="62"/>
    <line x1="62" y1="38" x2="38" y2="62"/>
    </g>
  </g>
  <g transform="translate(452,96) scale(0.44)">
    <circle cx="50" cy="50" r="34" fill="#E2F7ED" stroke="#1B7A4B" stroke-width="3"/>
    <polyline points="34,52 45,64 68,38" fill="none" stroke="#1B7A4B" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="120" y="126" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B">Before</text>
  <text x="510" y="126" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B">After</text>
  <g font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B">
    <text x="70" y="186">60 photos, all in daylight</text>
    <text x="70" y="222">0 photos of a held object</text>
    <text x="70" y="258">Accuracy gap: 50 points</text>
    <text x="460" y="186">80 photos, mixed light</text>
    <text x="460" y="222">20 photos of a held object</text>
    <text x="460" y="258">Accuracy gap: 9 points</text>
  </g>
  <text x="400" y="360" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#55636F" text-anchor="middle">Same model, same test. Only the training photos changed.</text>
</svg>
```

### `pattern-grid` &mdash; Pixel grid showing the letter L

**Canvas** `0 0 500 500`. Cells are 40x40 so a 12px number fits. Always print the number in the cell - the shade alone is not the message.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" role="img">
  <title>Pixel grid showing the letter L</title>
  <desc>An eight by eight grid of squares. Dark squares numbered 255 form the letter L; pale squares are numbered 0.</desc>
<text x="250" y="42" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle">A letter is just a grid of numbers</text>
    <rect x="90" y="80" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="130" y="80" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="170" y="80" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="210" y="80" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="250" y="80" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="290" y="80" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="330" y="80" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="370" y="80" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="90" y="120" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="130" y="120" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="170" y="120" width="40" height="40" fill="#1F6FB2" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="210" y="120" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="250" y="120" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="290" y="120" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="330" y="120" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="370" y="120" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="90" y="160" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="130" y="160" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="170" y="160" width="40" height="40" fill="#1F6FB2" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="210" y="160" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="250" y="160" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="290" y="160" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="330" y="160" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="370" y="160" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="90" y="200" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="130" y="200" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="170" y="200" width="40" height="40" fill="#1F6FB2" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="210" y="200" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="250" y="200" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="290" y="200" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="330" y="200" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="370" y="200" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="90" y="240" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="130" y="240" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="170" y="240" width="40" height="40" fill="#1F6FB2" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="210" y="240" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="250" y="240" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="290" y="240" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="330" y="240" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="370" y="240" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="90" y="280" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="130" y="280" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="170" y="280" width="40" height="40" fill="#1F6FB2" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="210" y="280" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="250" y="280" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="290" y="280" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="330" y="280" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="370" y="280" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="90" y="320" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="130" y="320" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="170" y="320" width="40" height="40" fill="#1F6FB2" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="210" y="320" width="40" height="40" fill="#1F6FB2" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="250" y="320" width="40" height="40" fill="#1F6FB2" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="290" y="320" width="40" height="40" fill="#1F6FB2" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="330" y="320" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="370" y="320" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="90" y="360" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="130" y="360" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="170" y="360" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="210" y="360" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="250" y="360" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="290" y="360" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="330" y="360" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <rect x="370" y="360" width="40" height="40" fill="#FFFFFF" stroke="#C7CDD4" stroke-width="1.5"/>
    <text x="110" y="100" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="150" y="100" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="190" y="100" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="230" y="100" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="270" y="100" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="310" y="100" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="350" y="100" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="390" y="100" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="110" y="140" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="150" y="140" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="190" y="140" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#FFFFFF" text-anchor="middle" dominant-baseline="central">255</text>
    <text x="230" y="140" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="270" y="140" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="310" y="140" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="350" y="140" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="390" y="140" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="110" y="180" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="150" y="180" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="190" y="180" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#FFFFFF" text-anchor="middle" dominant-baseline="central">255</text>
    <text x="230" y="180" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="270" y="180" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="310" y="180" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="350" y="180" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="390" y="180" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="110" y="220" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="150" y="220" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="190" y="220" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#FFFFFF" text-anchor="middle" dominant-baseline="central">255</text>
    <text x="230" y="220" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="270" y="220" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="310" y="220" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="350" y="220" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="390" y="220" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="110" y="260" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="150" y="260" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="190" y="260" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#FFFFFF" text-anchor="middle" dominant-baseline="central">255</text>
    <text x="230" y="260" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="270" y="260" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="310" y="260" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="350" y="260" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="390" y="260" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="110" y="300" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="150" y="300" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="190" y="300" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#FFFFFF" text-anchor="middle" dominant-baseline="central">255</text>
    <text x="230" y="300" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="270" y="300" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="310" y="300" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="350" y="300" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="390" y="300" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="110" y="340" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="150" y="340" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="190" y="340" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#FFFFFF" text-anchor="middle" dominant-baseline="central">255</text>
    <text x="230" y="340" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#FFFFFF" text-anchor="middle" dominant-baseline="central">255</text>
    <text x="270" y="340" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#FFFFFF" text-anchor="middle" dominant-baseline="central">255</text>
    <text x="310" y="340" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#FFFFFF" text-anchor="middle" dominant-baseline="central">255</text>
    <text x="350" y="340" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="390" y="340" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="110" y="380" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="150" y="380" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="190" y="380" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="230" y="380" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="270" y="380" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="310" y="380" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="350" y="380" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
    <text x="390" y="380" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
  <rect x="90" y="80" width="320" height="320" fill="none" stroke="#14202B" stroke-width="3"/>
  <text x="250" y="440" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#55636F" text-anchor="middle">8 x 8 = 64 pixels. 0 means paper, 255 means ink.</text>
</svg>
```

### `pattern-tree` &mdash; Decision tree for sorting an animal photo

**Canvas** `0 0 800 400`. Draw edges FIRST so boxes sit on top. Label every branch in words - never rely on left-means-no.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img">
  <title>Decision tree for sorting an animal photo</title>
  <desc>A decision tree. The top question asks if it has feathers, branching to further questions and then to three answers.</desc>
<text x="400" y="40" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle">A rule-based system is a tree of questions</text>
  <g stroke="#55636F" stroke-width="2" fill="none">
    <path d="M400 118 V142 H190 V166"/>
    <path d="M400 118 V142 H610 V166"/>
    <path d="M190 222 V246 H100 V270"/>
    <path d="M190 222 V246 H280 V270"/>
  </g>
  <g font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#55636F">
    <text x="286" y="136" text-anchor="middle">no</text>
    <text x="516" y="136" text-anchor="middle">yes</text>
    <text x="136" y="240" text-anchor="middle">no</text>
    <text x="244" y="240" text-anchor="middle">yes</text>
  </g>
  <rect x="300" y="62" width="200" height="56" rx="10" fill="#F5F8FA" stroke="#14202B" stroke-width="3"/>
  <text x="400" y="90" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">Has feathers?</text>
  <rect x="90" y="166" width="200" height="56" rx="10" fill="#F5F8FA" stroke="#14202B" stroke-width="3"/>
  <text x="190" y="194" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">Has whiskers?</text>
  <rect x="510" y="166" width="200" height="56" rx="10" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3"/>
  <text x="610" y="194" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">Bird</text>
  <rect x="20" y="270" width="160" height="56" rx="10" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3"/>
  <text x="100" y="298" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">Not sure</text>
  <rect x="200" y="270" width="160" height="56" rx="10" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3"/>
  <text x="280" y="298" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">Cat</text>
  <text x="400" y="372" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#55636F" text-anchor="middle">Questions are grey boxes. Answers are blue boxes. Every branch is labelled yes or no.</text>
</svg>
```

### `pattern-scene` &mdash; Labelled scene: a child asking a chatbot a question

**Canvas** `0 0 800 400`. Numbered pins on a tinted panel, all captions on one baseline. Numbers do the work, so the scene still reads in greyscale.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img">
  <title>Labelled scene: a child asking a chatbot a question</title>
  <desc>A child and a robot face each other with a thought bubble between them. Three numbered callouts point to the parts.</desc>
<text x="400" y="42" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle">What happens when you ask a chatbot a question</text>
  <rect x="30" y="70" width="740" height="250" rx="12" fill="#F5F8FA" stroke="#C7CDD4" stroke-width="1.5"/>
  <g transform="translate(70,150) scale(1.2)">
    <circle cx="50" cy="52" r="30" fill="#E8C671" stroke="#845F00" stroke-width="3"/>
    <path d="M20 44 A30 30 0 0 1 80 44 A34 22 0 0 0 20 44 Z" fill="#845F00" stroke="#845F00" stroke-width="3" stroke-linejoin="round"/>
    <circle cx="40" cy="50" r="4" fill="#14202B"/>
    <circle cx="60" cy="50" r="4" fill="#14202B"/>
    <path d="M39 63 Q50 72 61 63" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  </g>
  <g transform="translate(600,150) scale(1.2)">
    <line x1="50" y1="16" x2="50" y2="7" stroke="#1F6FB2" stroke-width="3" stroke-linecap="round"/>
    <circle cx="50" cy="5" r="4" fill="#F4D5E9" stroke="#C42B8C" stroke-width="2"/>
    <rect x="22" y="16" width="56" height="40" rx="12" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
    <circle cx="38" cy="34" r="5" fill="#14202B"/>
    <circle cx="62" cy="34" r="5" fill="#14202B"/>
    <path d="M40 45 Q50 52 60 45" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
    <rect x="28" y="60" width="44" height="30" rx="10" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
    <line x1="28" y1="68" x2="13" y2="78" stroke="#1F6FB2" stroke-width="3" stroke-linecap="round"/>
    <line x1="72" y1="68" x2="87" y2="78" stroke="#1F6FB2" stroke-width="3" stroke-linecap="round"/>
    <circle cx="50" cy="75" r="6" fill="#F4D5E9" stroke="#C42B8C" stroke-width="2"/>
  </g>
  <g transform="translate(300,110) scale(1.5)">
    <circle cx="22" cy="88" r="5" fill="#FFFFFF" stroke="#14202B" stroke-width="2.5"/>
    <circle cx="34" cy="76" r="7" fill="#FFFFFF" stroke="#14202B" stroke-width="2.5"/>
    <path d="M40 66 C24 66 18 50 30 43 C24 27 44 16 56 25 C64 10 92 14 92 31 C108 34 106 58 90 60 C86 70 64 72 56 66 Z"
    fill="#FFFFFF" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
  </g>
  <text x="390" y="167" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">the next</text>
  <text x="390" y="189" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">likely word</text>
  <g stroke="#C42B8C" stroke-width="2" fill="none">
    <path d="M116 268 V300"/>
    <path d="M390 262 V300"/>
    <path d="M646 268 V300"/>
  </g>
  <g>
    <circle cx="116" cy="314" r="14" fill="#F4D5E9" stroke="#C42B8C" stroke-width="2.5"/>
    <text x="116" y="315" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">1</text>
    <circle cx="390" cy="314" r="14" fill="#F4D5E9" stroke="#C42B8C" stroke-width="2.5"/>
    <text x="390" y="315" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">2</text>
    <circle cx="646" cy="314" r="14" fill="#F4D5E9" stroke="#C42B8C" stroke-width="2.5"/>
    <text x="646" y="315" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">3</text>
  </g>
  <g font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#55636F">
    <text x="116" y="356" text-anchor="middle">You type a question</text>
    <text x="390" y="356" text-anchor="middle">It predicts one word at a time</text>
    <text x="646" y="356" text-anchor="middle">It never looked anything up</text>
  </g>
</svg>
```

### `pattern-bar` &mdash; Bar chart of accuracy in four conditions

**Canvas** `0 0 500 500`. One series = one colour + direct labels on every bar. Grid lines stay 1.5px grey and sit UNDER the bars.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" role="img">
  <title>Bar chart of accuracy in four conditions</title>
  <desc>A bar chart. Daylight 92 percent, lamp light 58 percent, held in hand 42 percent, patterned background 50 percent.</desc>
<text x="250" y="40" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle">Accuracy by photo condition</text>
  <g stroke="#C7CDD4" stroke-width="1.5">
    <line x1="100" y1="400" x2="470" y2="400"/>
    <line x1="100" y1="322" x2="470" y2="322"/>
    <line x1="100" y1="245" x2="470" y2="245"/>
    <line x1="100" y1="167" x2="470" y2="167"/>
    <line x1="100" y1="90" x2="470" y2="90"/>
  </g>
  <g font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="end">
    <text x="90" y="404">0</text><text x="90" y="326">25</text><text x="90" y="249">50</text>
    <text x="90" y="171">75</text><text x="90" y="94">100</text>
  </g>
    <path d="M117 400 V118.8 A4 4 0 0 1 121 114.8 H155 A4 4 0 0 1 159 118.8 V400 Z" fill="#1F6FB2"/>
    <text x="138.0" y="102.8" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle">92%</text>
    <text x="138.0" y="422" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">Daylight</text>
    <path d="M205 400 V224.2 A4 4 0 0 1 209 220.2 H243 A4 4 0 0 1 247 224.2 V400 Z" fill="#1F6FB2"/>
    <text x="226.0" y="208.2" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle">58%</text>
    <text x="226.0" y="422" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">Lamp light</text>
    <path d="M293 400 V273.8 A4 4 0 0 1 297 269.8 H331 A4 4 0 0 1 335 273.8 V400 Z" fill="#1F6FB2"/>
    <text x="314.0" y="257.8" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle">42%</text>
    <text x="314.0" y="422" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">Held in hand</text>
    <path d="M381 400 V249.0 A4 4 0 0 1 385 245.0 H419 A4 4 0 0 1 423 249.0 V400 Z" fill="#1F6FB2"/>
    <text x="402.0" y="233.0" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle">50%</text>
    <text x="402.0" y="422" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">Patterned</text>
  <line x1="100" y1="400" x2="470" y2="400" stroke="#14202B" stroke-width="2"/>
  <text x="250" y="462" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#55636F" text-anchor="middle">One series, so no legend - the title names it. Every bar is labelled.</text>
</svg>
```

### `pattern-scatter` &mdash; Scatter chart comparing two training sets

**Canvas** `0 0 500 500`. Two series, so a legend is required - and the marker SHAPE differs too, so colour is never the only clue.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" role="img">
  <title>Scatter chart comparing two training sets</title>
  <desc>A scatter chart with two series: round blue dots for the small training set and green triangles for the big training set. Both rise to the right, the triangles higher.</desc>
<text x="250" y="40" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle">More examples, better guesses</text>
  <g stroke="#C7CDD4" stroke-width="1.5">
    <line x1="110" y1="380" x2="450" y2="380"/>
    <line x1="110" y1="300" x2="450" y2="300"/>
    <line x1="110" y1="220" x2="450" y2="220"/>
    <line x1="110" y1="140" x2="450" y2="140"/>
  </g>
    <circle cx="140" cy="340" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
    <circle cx="180" cy="300" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
    <circle cx="215" cy="315" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
    <circle cx="250" cy="265" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
    <circle cx="290" cy="240" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
    <circle cx="330" cy="205" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
    <circle cx="365" cy="180" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
    <path d="M150 247 L158 261 L142 261 Z" fill="#1B7A4B" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>
    <path d="M195 217 L203 231 L187 231 Z" fill="#1B7A4B" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>
    <path d="M235 187 L243 201 L227 201 Z" fill="#1B7A4B" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>
    <path d="M275 222 L283 236 L267 236 Z" fill="#1B7A4B" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>
    <path d="M315 142 L323 156 L307 156 Z" fill="#1B7A4B" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>
    <path d="M350 127 L358 141 L342 141 Z" fill="#1B7A4B" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>
    <path d="M390 112 L398 126 L382 126 Z" fill="#1B7A4B" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>
  <line x1="110" y1="380" x2="450" y2="380" stroke="#14202B" stroke-width="2"/>
  <line x1="110" y1="90" x2="110" y2="380" stroke="#14202B" stroke-width="2"/>
  <text x="280" y="412" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#55636F" text-anchor="middle">Number of training photos</text>
  <text x="66" y="235" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#55636F" text-anchor="middle" transform="rotate(-90 66 235)">Accuracy</text>
  <circle cx="130" cy="446" r="7" fill="#1F6FB2" stroke="#FFFFFF" stroke-width="2"/>
  <text x="146" y="451" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B">Small set (circles)</text>
  <path d="M300 438 L308 452 L292 452 Z" fill="#1B7A4B" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>
  <text x="316" y="451" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B">Big set (triangles)</text>
</svg>
```


---

## 8. Naming

```
fig-wNN-<n>-<slug>.svg
```

- `wNN` &mdash; the week, always two digits: `w01` &hellip; `w36`.
- `<n>` &mdash; the figure's sequence **within that week**, starting at 1.
- `<slug>` &mdash; two to four lowercase words, hyphenated, describing the content.

```
fig-w01-1-judgement-test.svg
fig-w07-2-pixel-grid-letter-l.svg
fig-w12-3-train-test-split.svg
fig-w29-1-accuracy-gap-by-group.svg
```

Lowercase only, hyphens only, no spaces, no underscores, no dates, no version suffixes.
Files beginning with `_` are shared infrastructure (`_motifs.svg`, `_preview.html`), not figures.

### 8.1 The filename number and the caption number are different numbers

This trips up every new author, so it is spelled out here.

| | What it counts | Example |
|---|---|---|
| **Filename `<n>`** | The order the figure was **drawn**, within its week. It never changes once assigned. | `fig-w20-4-percent-vs-point.svg` was the 4th figure drawn for Week 20. |
| **Caption `<n>`** | The order the figure is **read**, within *one markdown file*. | That same figure is `*Figure 20.4*` in the student guide and sits at a different position in the teacher guide. |

**These two numbers usually do not match, and that is correct.** 201 of the 429 week figures are
embedded in two or three of the books at different points, so one filename cannot carry one
reading-order number. Number captions by reading order in the file you are editing, and never
renumber a file.

Two consequences:

- **Workbook captions carry a `W`:** `*Figure W20.1*`, `*Figure W20.2*`. That is deliberate, so a
  workbook figure can never be confused with a chapter figure of the same number.
- **When you cite a figure that lives in a different book, say which book.** Not *"see Figure 20.4"*
  but *"see **Figure 20.4 in the Week 20 chapter**"* &mdash; because teacher `20.4` and student `20.4`
  are two different pictures.

---

## 9. Don'ts

- **No external images.** No `<image href>`, no PNG, no JPEG, no tracing a photo. Vector only.
- **No webfonts.** No `@font-face`, no `<link>` to a font, no Google Fonts. The stack in &sect;4 or nothing.
- **No filters that fail in print.** No `<filter>`, no `feGaussianBlur`, no `feDropShadow`, no CSS
  `filter`, no `opacity` below 1 to fake a tint (use the pale fill instead). Blur and shadow turn to
  mud on a school photocopier.
- **No colour as the only carrier of meaning.** Ever. Every meaningful distinction needs a **second**
  cue: a shape (tick vs cross, circle vs triangle), a label, a number, or a position.
  Test: photocopy it in black and white &mdash; can you still read it? Section 1.2 exists precisely
  because six hues collapse to one grey in print.
- **No gradients.** Flat fills only.
- **No `width`/`height` on the root `<svg>`.** viewBox only.
- **No white background rect.**
- **No text below 12px**, and no text you expect to wrap.
- **No new colours.** If you think you need a seventh, you need a different diagram (&sect;1.4).
- **No `<foreignObject>`**, no embedded HTML, no `<script>`.
- **No stretched motifs.** Uniform `scale()` only.

---

## 10. Pre-flight check

Run this on every figure before you commit it.

```bash
# 1. It must parse as XML.
python3 -c "import xml.dom.minidom,sys; xml.dom.minidom.parse(sys.argv[1])" fig-w07-1-my-figure.svg

# 2. It must not contain anything banned.
grep -nE '<image|href="http|@font-face|<filter|feGaussianBlur|feDropShadow|<foreignObject|<script|linearGradient' \
  fig-w07-1-my-figure.svg && echo "BANNED CONSTRUCT" || echo "clean"

# 3. It must declare accessibility and no fixed size.
grep -q 'role="img"' f.svg && grep -q '<title>' f.svg && grep -q '<desc>' f.svg && echo "a11y ok"
grep -nE '<svg[^>]+(width|height)=' fig-w07-1-my-figure.svg && echo "REMOVE width/height" || echo "scales ok"
```

Then, by eye:

- [ ] `<title>` states the figure's takeaway; the markdown alt text describes what a sighted
      reader sees. They may differ — alt says *what is drawn*, `<title>` says *what it means*.
      Both must be accurate and non-empty. Identical is acceptable but not required.
- [ ] Every colour is from &sect;1, used in its role.
- [ ] Nothing within 20px of the canvas edge.
- [ ] Every meaningful distinction has a shape or label as well as a colour.
- [ ] Opened `_preview.html`, ticked **Greyscale**, and the figure still reads.
- [ ] An 11-year-old gets the point in four seconds with the caption covered.

---

## 11. Files in this folder

| File | What it is |
|---|---|
| `STYLE.md` | This contract. |
| `_motifs.svg` | Sprite sheet: all 16 motifs as `<symbol>`. Reference with `<use>` or copy inline. |
| `_preview.html` | Open in any browser. Renders the palette, every motif and every pattern, with a greyscale toggle for the print check. |

---

## 12. The Growing Map — `fig-wNN-0-where-this-fits.svg`

Every week carries **one** figure that is not about this week's content. It shows the learner the
*shape of the whole level* with one more piece filled in. It appears in **both** the student guide
(in the `## 🧭 Where This Fits` section) and the teacher guide (in `### 🧭 The Growing Map`).

**Reference implementation: `fig-w01-0-where-this-fits.svg`.** Open it before drawing another one.

### 12.1 Why index `0`

Content figures are numbered from 1. The map is always `-0-`, so it sorts first in the folder and is
instantly identifiable as structural rather than topical. Its caption is `Figure <week>.0`.

### 12.2 The three fixed zones

Always the **wide** canvas, `0 0 800 400`, and always these three zones:

| Zone | y range | Holds |
|---|---|---|
| **Spine** | 28–320 | The level's structure, with this week's piece solid and future pieces dashed |
| **Thread strip** | 336–360 | Six pills: data · representation · model · learning signal · evaluation · impact |
| **Footer line** | ~380 | One sentence of orientation, 13px, `muted`, centred |

### 12.3 The state vocabulary — this is the load-bearing part

The learner must be able to read progress at a glance, from **shape alone**, without relying on colour:

| State | Stroke | Fill | Dash | Badge |
|---|---|---|---|---|
| **This week** | `human` `#845F00`, width 3 | `human` fill `#E8C671` | solid | white pill, `correct` border, tick + `YOU ARE HERE` |
| **Already done** | `ink` `#14202B`, width 2 | `paper` | solid | small `muted` week number, e.g. `wk 4` |
| **Not yet** | `grid` `#C7CDD4`, width 3 | none | `stroke-dasharray="10 8"` | dashed pill, `WEEK n` |

Three rules that follow from this, and they are not negotiable:

1. **Dashed always means "not yet".** Never use a dashed stroke for anything else in this figure.
2. **Exactly one box may carry the `YOU ARE HERE` badge.** If a week genuinely fills two boxes, badge
   the more important one and give the other the `wk NN` treatment.
3. **Never re-colour a done box to show recency.** Done is done. Only the current week is tinted.

### 12.4 The thread strip

Six pills, fixed order, fixed x positions (see the reference file). The thread(s) this week extends
are filled `model` `#DBCEF3` with a `#6D28D9` 2.5-width stroke and bold `ink` text; the rest are white
with a `grid` 1.5 stroke and `muted` text. **At most two lit per week** — a week that claims to extend
four threads has not decided what it is about.

### 12.5 What the spine looks like per level

The spine is the level's own backbone, so it differs by level but is identical *within* a level:

| Level | Spine |
|---|---|
| **1 Explorer** | The two-branch fork: *rules written by a person* vs *rules worked out from examples*, then the branches subdivide as the year goes on |
| **2 Builder** | The data-to-answer pipeline: *collect → store → clean → look → model → check* |
| **3 Engineer** | The training loop: *guess weights → measure loss → which way is downhill → step*, wrapped by *split → train → evaluate → ship* |

Draw the level's full spine **once**, then per week change only which pieces are solid, dashed, or
badged. The figures should feel like frames of one animation, because that is exactly what they are.

### 12.6 Accessibility

- `<title>`: states what is filled in this week, e.g. *"The course map after Week 1: one branch of two
  is filled in"*.
- `<desc>`: describes the state of **every** zone in words, including which threads are lit — a screen
  reader user must get the same progress information a sighted reader gets from the dashes.
- The markdown alt text describes what is drawn; `<title>` states what it means (see §on alt text).

### 12.7 Checklist before you ship one

- [ ] `viewBox="0 0 800 400"`, no `width`/`height`, transparent background
- [ ] Nothing outside x 20–780, y 20–380
- [ ] All `font-size` ≥ 12
- [ ] Only §1.1 palette hexes
- [ ] Exactly one `YOU ARE HERE` badge
- [ ] Dashed used **only** for "not yet"
- [ ] ≤ 2 threads lit
- [ ] Spine matches the other weeks in this level, piece-for-piece
- [ ] Parses as XML

> **⚠️ Note on tooling.** Levels 2 and 3 ship a `figures/_generator/_gen_audit.py`; **Level 1 does
> not**, so there is no automated checker for this level — work the checklist above by hand. Do **not**
> borrow the Level 3 auditor for these files: it reports false positives on them (including on the
> reference `fig-w01`) because it does not inherit `font-size`/`text-anchor` from a parent `<g>`, and it
> reads relative `l dx dy` path commands as absolute coordinates. Changing a figure to satisfy that
> estimator would break it against the reference.

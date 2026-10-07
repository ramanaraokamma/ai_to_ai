# Week 27 — Term 3 Checkpoint: Build a Lie, Then Confess

[⬅ Week 26](week-26.md) · [Course Home](../README.md) · [Week 28 ➡](week-28.md) · [Student Guide](../student-guide/week-27.md) · [Workbook](../workbook/week-27.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟪 Review — Term 3 checkpoint, taught by building one dishonest chart on purpose |
| **Big idea** | You can make a 2% difference look enormous without changing a single number — just by starting the y-axis somewhere else. |
| **New vocabulary** | truncated axis · exaggeration factor · legend · correlation · causation |
| **New syntax** | `ax.set_ylim(bottom, top)` · `fig, axes = plt.subplots(1, 2)` · `ax.legend()` · `df["a"].corr(df["b"])` |
| **Materials** | The printed workbook (all of it; it is sections, not numbered pages) · **a ruler with millimetres on it** (a real one — this is not a metaphor) · **one printed copy of `lie.png`** (see Prep) · a pencil · a calculator |
| **Tech needed** | The `level2` folder, venv active, matplotlib and pandas. `students.py` and `myweek.py` from earlier weeks. **A working printer**, or a way to view the chart at a fixed size. |
| **Prep time** | 20 minutes the night before, 5 minutes on the day |

> **⚠️ Watch out:** the measuring must happen **on paper**, not on a screen. On a screen the student can zoom, and zooming changes both bars together so the trick stops feeling real. A printed page has one fixed size, a ruler fits on it, and the number that comes out is theirs.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Exaggerate a 2% difference with `set_ylim`** and compute how many times bigger it has been made to look.
2. **Put the misleading chart and the honest one side by side in one figure**, using `plt.subplots(1, 2)` and `axes[0]` / `axes[1]`.
3. **Add a legend as soon as there are two series**, by giving each `plot` call a `label=`.
4. **Compute a correlation and refuse, in writing, to call it a cause** — including naming a plausible third thing that could be causing both.
5. **Produce a list of the Term 3 weeks that need revisiting**, with a reason for each.

Observable evidence: a saved two-panel PNG with the lie on the left and the fix on the right; two bar measurements in millimetres with the ratio and the exaggeration factor worked out on paper; a written sentence about `r = 0.93` that contains no causal verb; and a completed Term 3 reflection sheet naming at least two weeks to revisit.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

This is a review week, and review weeks are the easiest ones to teach badly. The temptation is to go back over weeks 19 to 26 in order. Do not. **The whole of Term 3 gets revised by being used**, inside one 70-minute build, and the build is deliberately dishonest, which is why students remember it.

Read all of this section. §2 is arithmetic you must be able to do at the whiteboard, and §5 is the bit that will get you asked a hard question.

### 1. What Term 3 actually was, so you know what you are checkpointing

| Week | What it added | Where it shows up today |
|---|---|---|
| 19 | `axis=0` down the columns, `axis=1` across the rows | not directly — flag it on the reflection sheet |
| 20 | boolean masks, `arr > 50`, `arr[mask]` | not directly — flag it |
| 21 | `pd.DataFrame`, `df.head()`, `df["col"]` | every chart today reads a column |
| 22 | `.loc`, `.iloc`, `df[df["age"] > 12]`, `sort_values` | `sort_values` in the data story |
| 23 | `read_csv` / `to_csv`, `isna`, `fillna`, `astype` | flag it |
| 24 | `drop_duplicates`, `.str` methods, `groupby(...).mean()` | the club and house averages |
| 25 | figure, axes, labels, markers, `savefig` | all of it |
| 26 | bar, histogram, scatter, `value_counts` | all of it |

The reflection in Build It, Part 6 walks the student through all eight. Your job in the lesson is the *build*; the reflection is homework.

### 2. The truncated axis, with the arithmetic done in full

> **Truncated axis** — an axis that starts somewhere other than zero, so small differences look enormous.

Here is the whole trick. Two classes hand in homework: **7A gets 49% in on time, 7B gets 51%.** A two-point gap. Nothing.

**Honest chart, y from 0 to 100.** The bars are 49 and 51 units tall.

- 7B's bar ÷ 7A's bar = 51 ÷ 49 = **1.0408**. 7B's bar is about 4% taller. They look nearly identical, *because they nearly are*.

**Dishonest chart, y from 48.6 to 51.4.** Now each bar only shows the part *above* 48.6.

- 7A's visible bar = 49 − 48.6 = **0.4 units**
- 7B's visible bar = 51 − 48.6 = **2.4 units**
- 7B's bar ÷ 7A's bar = 2.4 ÷ 0.4 = **6.00**

**7B's bar is now six times taller than 7A's.** Every number printed on the chart is correct. Nothing was faked. 48.6 units of length were quietly deleted from the bottom of both bars.

> **Exaggeration factor** — how many times bigger the difference has been made to look: the truncated bar-length ratio divided by the honest one.

6.00 ÷ 1.0408 = **5.76**. Call it "about six times".

![The lie lives below the axis](../figures/fig-w27-1-truncated-axis-lie.svg)
*Figure 27.1 — The grey block is the 48.6 units cut off both bars. 99% of 7A's real bar is not on the page.*

**And now the millimetres, which is the part students actually believe.** The chart is drawn 6 × 4 inches at 120 dots per inch. matplotlib gives the drawing frame 3.08 of those 4 inches, and that frame holds 2.8 percentage points (48.6 to 51.4). So:

- 3.08 inches × 25.4 = 78.2 mm of frame ÷ 2.8 points = **27.9 mm per percentage point**
- 7A's bar: 0.4 × 27.9 = **11 mm**
- 7B's bar: 2.4 × 27.9 = **67 mm**

Put a ruler on the printed page and that is what you will measure. 67 ÷ 11 = **6.1** — the same ratio, arrived at by hand, by a 12-year-old, with a ruler. That is why this lesson works.

![Measure it with a ruler, then divide](../figures/fig-w27-3-exaggeration-arithmetic.svg)
*Figure 27.2 — 67 mm against 11 mm. The bars are honest to the millimetre. The axis was not.*

> **⚠️ Watch out:** if your printer scales the page to fit, **both** bars shrink by the same amount, so the millimetre readings change but **the ratio does not**. If a student measures 9 mm and 54 mm, they have not made a mistake — 54 ÷ 9 = 6.0. Say this before they measure, or you will spend three minutes reassuring them.

### 3. Why 48.6 is such a strange number, and why that is the lesson

A student will ask where 48.6 came from. The honest answer is the most useful sentence in the week:

> **"I fiddled with it until the chart looked how I wanted it to look."**

That is exactly what the person who made the chart on your phone did. Nobody derives a truncated axis; they nudge it. 48.6 gives a clean 6× because 49 − 48.6 = 0.4 and 51 − 48.6 = 2.4, and 2.4 ÷ 0.4 is 6 — and I chose it *after* deciding I wanted six. Push the floor to 48.9 and the ratio becomes 21. Push it to 48.99 and it becomes 201. **There is no limit**, which is worth showing: the closer the floor creeps to the smaller bar, the bigger the lie, and it is one keystroke each time.

### 4. `ax.set_ylim(bottom, top)` — and the honest rule

```python
ax.set_ylim(48.6, 51.4)      # the trick
ax.set_ylim(0, 100)          # the fix
```

Two numbers: where the axis starts, where it stops. **That is the whole call, and it is the whole lie.** One argument to one function is the entire difference between an honest chart and a dishonest one, which is a genuinely unsettling thing for a 12-year-old to learn and it should be said out loud.

Two things it does silently, and both are Clinic rows:

- `ax.set_ylim(48.6)` — **one** argument. No error. It sets the bottom and lets matplotlib pick the top. The chart is different from the one you intended and nothing tells you.
- `ax.set_ylim(51.4, 48.6)` — backwards. No error. The chart is drawn **upside down**, bars hanging from the top. It looks like a bug in matplotlib. It is not.

**The rule, and it has two halves:**

| Chart type | Must the axis start at zero? | Why |
|---|---|---|
| **bar** | **Yes. Always.** | A bar asks your eye to compare **lengths**. Delete length from the bottom and the reader has no way to add it back. |
| **line** | Not necessarily — but say so if it does not | A line asks you to follow a **shape**. A body-temperature chart starting at 0 °C would be a flat line squashed against the top of the frame, telling you nothing. |

If you truncate a line chart, the honest thing is to shout about it in the label: `"Temperature (°C) — note: axis starts at 20"`. **Hiding it is the dishonest part; the choice itself can be defensible.**

### 5. `fig, axes = plt.subplots(1, 2)` — one sheet, two frames

Week 25's `plt.subplots()` gave you one frame. Give it two numbers and it gives you a grid:

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))   # 1 row, 2 columns
```

- `1, 2` — one row of two frames. `2, 2` would give four in a square.
- `axes` is now **a box holding both frames**, numbered from 0 like a list (Week 11). `axes[0]` is the left one, `axes[1]` is the right one.
- Every call from Week 25 and 26 still works — you just say *which frame* first: `axes[0].bar(...)`, `axes[1].set_title(...)`.
- `figsize=(10, 4)` — wider than usual, because you are fitting two frames on one sheet.

Two errors here, both worth meeting:

- `axes.bar(...)` — forgetting the number. Gives `AttributeError: 'numpy.ndarray' object has no attribute 'bar'. Did you mean: 'var'?` Translate it: *"`axes` is a box of frames, not a frame. Which one did you mean?"*
- `axes[2]` — there are only two, numbered 0 and 1. Gives `IndexError: index 2 is out of bounds for axis 0 with size 2`. This is the same off-by-one they met in Week 11, in new clothing.

**One bonus call, worth typing but not worth teaching:** `fig.suptitle("...")` puts a title across the **whole sheet**, above both frames. Each frame already has its own `set_title`; the suptitle is the headline over both. If a student asks, that is the answer. Do not build anything on it.

![The same two numbers, drawn two ways](../figures/fig-w27-2-lie-and-fix-side-by-side.svg)
*Figure 27.3 — Left panel, right panel, one sheet. The reader can compare the framing instead of trusting it.*

### 6. `ax.legend()` and why it needs `label=`

The moment there are two lines on one frame, the reader has to guess which is which, and readers who have to guess stop reading.

```python
ax.plot(df["day"], df["homework_min"], marker="o", label="Homework")
ax.plot(df["day"], df["screen_min"], marker="s", label="Screen time")
ax.legend()
```

`ax.legend()` does not invent names. It goes round every line already drawn on the frame and prints whatever `label=` each one was given. Forget the labels and you get a warning, not an error:

```text
No artists with labels found to put in legend.  Note that artists whose label start with an underscore are ignored when legend() is called with no argument.
```

"Artists" is matplotlib's word for anything drawn. The chart still saves; it just has no legend.

**Two cues, not one.** Notice `marker="o"` on the first line and `marker="s"` (a square) on the second. Colour alone is not enough — the chart will be photocopied, printed in black and white, or read by somebody who cannot distinguish those two colours. Different **shapes** as well as different colours costs nothing and is simply what a careful person does.

![Two lines need a legend. Always.](../figures/fig-w27-5-legend-names-the-lines.svg)
*Figure 27.4 — Round markers and square markers, so it survives a photocopier.*

### 7. Correlation: what `r` is, and the four worlds

> **Correlation** — one number saying how strongly two columns move together, from −1 (perfect opposites) through 0 (no relationship) to +1 (perfectly together).

```python
r = df["hours"].corr(df["score"])     # 0.925
```

For our 38 students, study hours and score give **r = 0.925**. That is very strong. The scatter plot is a tidy band of dots rising to the right.

**Three things about `r` that you should be ready for:**

1. **It is not a percentage.** `r = 0.93` does not mean "93% of the score comes from studying". It is a number on a scale from −1 to +1 and that is all it is. Students will want it to be a percentage. It is not.
2. **A negative `r` is not a weak `r`.** `df["age"].corr(df["hours"])` gives **−0.572** in this table — older students report fewer hours. The minus sign means "as one goes up the other goes down". It is a *direction*, not a grade.
3. **It only works on numbers.** `df["club"].corr(df["score"])` fails with `TypeError: unsupported operand type(s) for /: 'str' and 'int'` — Clinic row 4. You cannot average the word "chess".

**And now the thing this whole term has been building to.** `r = 0.93` between hours and score is consistent with **four different worlds**, and no scatter plot on earth can tell you which one you are in:

![One correlation, four possible worlds](../figures/fig-w27-4-correlation-not-cause.svg)
*Figure 27.5 — Four stories, one number. The picture is identical in all four.*

| World | What is actually happening | Plausible here? |
|---|---|---|
| **A causes B** | Studying really does raise marks | Yes |
| **B causes A** | Doing well makes studying feel rewarding, so you do more | Also yes |
| **C causes both** | A quiet home with a desk causes more study hours **and** higher marks | Also yes — this is the **confounder** |
| **Coincidence** | Line up enough columns and some pair fits by luck | Very common, especially in small tables |

> **Causation** — one thing actually making the other happen.
> **Confounder** — a hidden third thing causing both of the things you measured, making them look connected to each other.

🍕 **The analogy that always lands.** Ice cream sales and drownings rise and fall together almost perfectly. Ice cream does not cause drowning. **Hot weather** causes both — people buy ice cream *and* people go swimming. The numbers, verified in the lesson:

```text
ice creams vs drownings  : r = 0.997
temperature vs ice creams: r = 0.987
temperature vs drownings : r = 0.989
```

The first line is the *strongest of the three* and it is the one that is causally nonsense. **There is nothing visible in a correlation, or in a scatter plot, that distinguishes "A causes B" from "C causes both".** The distinction lives entirely outside the data, in what you know about the world.

**How to talk about a scatter honestly.** Say *"students who studied more tended to score higher"* — a description. Do not say *"studying raised their scores"* — a claim about cause, which needs an **experiment** (randomly make some students study more and see what happens), not a chart.

### 8. The ethics question, and how to run it

The last ten minutes of the lesson ask: **who gets hurt if a school acts on that chart?**

Trace the chain out loud. Somebody sees `r = 0.93`, concludes "more hours → higher marks", and mandates two extra study hours for everybody. Now look at *who* is at the bottom of that scatter. In our table the five students studying an hour or less are **Hugo (14), Sami (14), Greta (14), Omar (14) and Bruno (13)** — every single one is 13 or 14. The six studying five hours or more are mostly **12**.

Then ask the question that matters: **why might a 14-year-old be studying half an hour a week?** A job. A younger sibling to look after. No quiet room. A long commute. None of those are on the chart, and none of them are fixed by being told to study more — they are *punished* by it.

**This is not a bolt-on.** It is the point of the whole term: a chart is an argument, an argument leads to a decision, and a decision lands on a person. Give it the time.

### 9. The three misconceptions you will meet

**Misconception 1 — "so truncating an axis is always cheating."** No, and over-correcting here is a real risk after a lesson this vivid. For **bars**, yes, always start at zero. For **lines**, a truncated axis is often the only readable choice — nobody charts body temperature from absolute zero. The dishonest part is *not saying so*. Keep the two halves separate.

**Misconception 2 — "r = 0.93 means 93 percent."** It does not mean anything as a percentage. Cure it with the negative one: "`r` between age and hours is minus nought point five seven two. What is minus fifty-seven percent of a study hour?" Nothing. It is a number on a scale, not a proportion.

**Misconception 3 — "if the correlation is strong enough, it must be cause."** This is the deepest one and the hardest to shift, because strong correlations *feel* like proof. The cure is the ice cream numbers, because there the strongest correlation of the three is the absurd one. Say it plainly: **strength is not evidence of direction.** A perfect correlation between two things can still have a third thing causing both.

### 10. How deep to go, and where to stop

**Go this far:** `set_ylim` and the bar-chart rule; the exaggeration arithmetic in millimetres; two panels with `subplots(1, 2)`; a legend with `label=`; `corr` and the refusal to say "causes"; and a Term 3 reflection.

**Stop before:**
- **Any formula for `r`.** It involves squares and square roots over both columns and it teaches nothing at this stage. `df["a"].corr(df["b"])` gives you the number. That is enough.
- **r-squared.** Week 32, and it needs regression first.
- **The other visual lies** — 3-D pie charts, dual y-axes, cherry-picked date ranges. Mention them by name in the wrap if there is time; do not build them. The truncated axis is the one they will meet weekly for the rest of their lives.
- **Statistical significance, p-values, confidence intervals.** Not this year, and possibly not this level.
- **Fitting a trend line to the scatter.** Week 32. A line drawn by eye looks exactly as authoritative as a calculated one and carries none of the information.
- **`plt.style.use(...)`, colour palettes, annotations.** Fun, endless, not the point.

---

### 11. 🧭 The Growing Map — two minutes on the word `honest`

One figure in the student guide is not about this week's topic. It is the same pipeline every week with
one more piece filled in, and it is the only place either book shows the learner the *shape* of the
year rather than the content of the lesson. This week it is also a Term 3 full stop.

![The Level 2 pipeline in Week 27: still the honest axes tile, now building a misleading chart on purpose and confessing it](../figures/fig-w27-0-where-this-fits.svg)

*Figure 27.0 — Week 27's version. Second and final week inside the `honest axes` tile, weeks 26 to 27 —
and stage four is now solid all the way across. Two threads lit: impact and evaluation.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and point at the two words in the gold tile.** Ask *"we spent today breaking the second
   word — so which chart was the honest one, the left panel or the right?"* You want a finger on the
   **right-hand** panel of their own saved PNG, and the reason said out loud: *its axis starts at zero.*
   Then the follow-up that does the real work: *and what number did the ruler give you?* Their own
   exaggeration factor, from their own page. Do not improve their wording.
2. **Then the map question:** *"stage four is solid now and the last stage is still dashed — what do
   you think a computer could do with a chart that we cannot?"* You are fishing for something in the
   region of *guess the next one*. Anything close is a win; this is a hook for next week, not a test.
3. **Have them fill in their own copy** — ink the `honest axes` tile in, and write their exaggeration
   factor beside it. It is the only number on their map that they measured rather than computed.

> **🧑‍🏫 Why this is worth two minutes.** Term 3 was three months of pandas, charts and cleaning, and
> from the inside it can feel like a long unrelated list. The map makes it one stage of five, finished.
> It also does something specific for this week: seeing `PREDICT & CHECK` still dashed while their
> ruler measurement sits on the page next to it plants the right suspicion for Term 4 — a model's
> output is another picture somebody can lean on, and it will need checking the same way.

---

## 🧰 Prep Checklist

### 20 minutes the night before

- [ ] **Print the whole workbook** (`workbook/week-27.md`) — Warm-Up, Predict the Output, Practice Sets A and B, Fix the Broken Program, Puzzle, Think Deeper, Build It, Draw It, Self-Check. Do **not** print the Answers section at the end for the student.
- [ ] **Find a ruler with millimetres on it.** A real one. The whole hook depends on it. A second ruler is better, so you can measure alongside rather than over their shoulder.
- [ ] **Build and print the lie.** In `~/ai-academy/level2`, create `week27_lie.py` with the code from the Answer Key, and run it:

  ```bash
  python week27_lie.py
  ```

  Expected, exactly:

  ```text
  saved lie.png
  7A: 49%  -> visible bar = 0.4 units
  7B: 51%  -> visible bar = 2.4 units
  looks-like ratio  7B / 7A = 6.00 times taller
  honest ratio      7B / 7A = 1.0408 times taller
  exaggeration factor       = 5.76
  the drawing frame is 3.08 inches tall
  that is 27.9 mm per percentage point
  7A bar should measure 11 mm
  7B bar should measure 67 mm
  ```

  Now **print `lie.png`** — and print it **twice**, one for you and one for them. Then **measure both bars yourself with the ruler.** You want to have done this before the lesson, because the number you get depends on how your printer scaled the page and you should know it in advance. If you measure 9 and 54, that is fine — the *ratio* is what matters.
- [ ] **Cover up the numbers.** The printed chart has `Homework on time (%)` on the y axis and tick numbers 49, 50, 51. **Fold or tape over the y-axis tick numbers** on the copy you hand them. They must measure the bars *before* they can read the values. The whole hook collapses if they see "49" and "51" first.
- [ ] **Check `students.py` and `myweek.py` are in the folder.** Both are in the Answer Key if either has gone missing.
- [ ] **Run `week27_corr.py`** and check you get `r = 0.925`, and the three ice-cream numbers.
- [ ] **Read §7 and §8 above twice.** The correlation-is-not-cause conversation is the hardest thing you will do this term, and it goes much better if you already know which five students sit at the bottom of the scatter.

### 5 minutes on the day

- [ ] Terminal in `~/ai-academy/level2`, venv active. Folder window visible.
- [ ] The printed `lie.png` face down, **with the y-axis numbers covered**.
- [ ] Two rulers on the table. Calculator on the table.
- [ ] The workbook open at the Warm-Up, with Predict the Output and Practice Set A (A1 and A5) flagged, on top of the pile. The hook's measuring has no workbook page; put a blank sheet beside the printed `lie.png` for the two millimetre readings.
- [ ] If you found a misleading chart in the wild — a news site, an advert, a battery graph — have it ready for the wrap.

### Fallback if a laptop or the printer fails

| If this fails | Do this instead |
|---|---|
| **The printer** | Draw the lie by hand on squared paper. Two bars, one 11 squares tall and one 67 squares tall, labelled 7A and 7B, with the y axis numbered 48.6 at the bottom and 51.4 at the top. It works exactly as well, and honestly the hand-drawn version is *more* convincing, because it obviously was not produced by a machine that might have made a mistake. |
| **No laptop at all** | The entire lesson runs on squared paper. Draw both versions of the chart by hand — the truncated one and the zero-based one — measure both, do the division, and then have the correlation conversation using the ice-cream table from Activity Part B (or Think Deeper T1, which quotes the numbers). Objectives 1, 4 and 5 land in full; objectives 2 and 3 become "describe what the code would be", which is a fair substitute for a review week. |
| **`students.py` is missing** | The full file is in the Week 26 Answer Key. Two minutes to drop in. Or run the whole lesson on the two typed-in numbers 49 and 51, which need no table at all. |
| **A chart looks upside down** | `set_ylim` was given its two numbers backwards. No error is produced. See Clinic row 7. |
| **The student measures 9 mm and 54 mm, not 11 and 67** | Nothing is wrong. The printer scaled the page. Both bars shrank together, so the ratio survived: 54 ÷ 9 = 6.0. **Say this before they measure.** |
| **The student says "so all charts are lies"** | Do not let this stand — it is the failure mode of the lesson. Point at the honest right-hand panel: same numbers, zero-based axis, ratio 1.04, and it is a perfectly good chart. The point is not that charts lie; it is that **a chart is an argument, so you check the framing**. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Measure Both Bars | 7 | 7 | A ruler, two bars, and a ratio of six |
| 🧠 Concept — Where the Lie Lives | 16 | 23 | `set_ylim`, the arithmetic, and the zero rule |
| 💻 Live-Code Together — Build the Lie, Then the Pair | 18 | 41 | Two deliberate mistakes, both silent |
| 🎲 Their Turn — Legend, Correlation, and Who Gets Hurt | 20 | 61 | Two lines with a legend; r = 0.93; the ethics question |
| 🔑 Wrap & Assign | 9 | 70 | Three checks, the Term 3 reflection, homework |

---

### 🪝 Hook — Measure Both Bars (7 minutes)

**Do this:** Put the printed `lie.png` on the table — **with the y-axis numbers covered.** Put a ruler next to it. Say nothing about what it is.

**Say this:**

> "Two classes. 7A and 7B. This chart is about how much homework each class hands in on time. I didn't make up any numbers; every number on this chart is real.
>
> I want you to do something physical. Take the ruler. **Measure how tall each bar is, in millimetres.** Write both numbers on the blank sheet beside you."

Let them measure. It takes about forty seconds. They will get roughly 11 mm and 67 mm.

> "Read me the two numbers."

Whatever they got, write both on paper.

> "Right. Now divide the big one by the small one. Use the calculator."

67 ÷ 11 = **6.09**.

> "About six. So according to this chart, **7B is about six times better at homework than 7A.** Six times. If you were 7A's teacher you'd be in trouble. If you were 7A, you'd feel awful.
>
> Now let me uncover the y axis."

**Do this:** Peel off the cover. Reveal the tick numbers: 49, 50, 51.

Let them look. Then:

> "7A got **forty-nine percent.** 7B got **fifty-one percent.**
>
> Two points apart. Out of a hundred. Say it out loud: how much better is 7B than 7A?"

> "Two percent. Basically nothing. Fifty-one over forty-nine is one point oh four — 7B is four percent better, and four percent of anything is a rounding error.
>
> And you measured, with a ruler, that it looks **six times** bigger.
>
> Nobody lied to you. There is not one false number on this page. **I moved where the axis starts.** That's it. That's the whole trick, and it's one line of code, and you're going to write it yourself in about fifteen minutes."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Measure both bars in millimetres." | About 11 and 67. | If the printer scaled the page they might get 9 and 54, or 14 and 85. Fine. Say: "The ratio is what matters — divide them." |
| "Divide the big one by the small one." | About 6. | If they get 6.09 or 5.8, that is correct; the rounding is in the measuring. Do not tidy it. |
| "How much better is 7B, really?" | Two percentage points. About 4% taller. | If they say "two percent better", that is close enough — 51/49 is 1.04, so 4% relatively. Do the division with them; it is a good fractions moment. |
| "Which number did I fake?" | None of them. | If they insist something must be wrong with the data, hand them the ruler and the numbers and let them check. Nothing is wrong. That is the point. |
| "So how did I do it?" | You changed where the y axis starts. | If they cannot see it, point at the bottom tick: "What number is at the bottom of this axis? What number *should* be at the bottom of a bar chart?" |

---

### 🧠 Concept — Where the Lie Lives (16 minutes)

**Do this:** Have Figure 27.1 visible. Keep the printed chart and the ruler on the table.

**Say this — part 1, what actually happened:**

> "Look at Figure 27.1. See the grey block underneath the axis? That's what got deleted.
>
> The axis starts at forty-eight point six. So 7A's bar — which is really forty-nine units tall — only gets to show forty-nine minus forty-eight point six. That's **nought point four**. And 7B shows fifty-one minus forty-eight point six, which is **two point four**.
>
> Two point four divided by nought point four is **six**. There's your six. It came out of the subtraction.
>
> And here's the sentence I want you to remember: **forty-eight point six units of length were deleted from the bottom of both bars, and the reader has no way to put them back.**"

**Say this — part 2, why bars in particular:**

> "Now, why is this so bad for a bar chart specifically? Because of what a bar chart asks your eye to do.
>
> A bar chart says: *compare these lengths.* That's the whole deal. Long bar, big number. Your eye is doing arithmetic with length — and it can only do that arithmetic if the bars start from the same place, and that place has to be zero.
>
> Chop the bottom off and your eye is still doing the arithmetic. It just can't tell that the numbers have been messed with. That's why it works, and that's why it's dishonest. **Bar charts start at zero. Always. No exceptions.**"

**Say this — part 3, the honest exception, because it matters:**

> "But — and I want to be careful here, because it would be easy to walk out of this lesson thinking every chart is a lie — **line charts are different.**
>
> Imagine a chart of your body temperature over a week. Thirty-six point eight, thirty-seven, thirty-six point nine, thirty-nine when you were ill. If I started that axis at zero, all five points would be squashed into a flat line right at the top of the chart and you'd learn nothing. And zero degrees isn't a meaningful floor for a human being anyway. So a temperature chart starting at thirty-five is the *right* chart.
>
> The difference is what the chart asks your eye to do. A bar asks you to compare *lengths*. A line asks you to follow a *shape*. Shapes survive a moved floor; lengths don't.
>
> And the honest rule for a truncated line chart: **say so, loudly, in the label.** Write `Temperature in degrees C, note axis starts at 35`. **Hiding it is the dishonest bit, not the choosing.**"

**Say this — part 4, one line of code:**

> "The whole thing is one function with two numbers:
>
> `ax.set_ylim(48.6, 51.4)` — where the axis starts, where it stops. That's the lie.
>
> `ax.set_ylim(0, 100)` — that's the fix.
>
> One argument. That's the entire distance between an honest chart and a dishonest one, and I want that to bother you slightly, because it should."

**Say this — part 5, and where 48.6 came from:**

> "One more thing, and it's my favourite bit. Somebody's going to ask where forty-eight point six came from. Here's the honest answer: **I fiddled with it until the chart looked how I wanted it to look.**
>
> That's it. There's no maths behind it. I decided I wanted about six times, and I moved the floor until I got six times. And if I'd wanted twenty-one times, I'd have used forty-eight point nine. If I'd wanted two hundred times, forty-eight point nine nine.
>
> **There's no limit.** The closer the floor creeps up to the smaller bar, the bigger the lie, and it's one keystroke every time. That's what the person who made the chart you saw on your phone last week was doing."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Where did the six come from, in arithmetic?" | 2.4 ÷ 0.4, the two visible bar lengths. | If stuck, do the two subtractions on paper with them: 49 − 48.6 and 51 − 48.6. |
| "Why is this worse for bars than for lines?" | A bar asks you to compare lengths; a line asks you to follow a shape. | If they say "it isn't", offer the body-temperature chart starting at zero and ask what they'd learn from it. |
| "What ylim would make it look TWENTY times bigger?" | Something near 48.9: (51 − 48.9) ÷ (49 − 48.9) = 21. | Brilliant question to let them work out with a calculator. It takes 90 seconds and it is worth every one. |
| "Is a truncated line chart always dishonest?" | No — but not saying so is. | If they say yes, give them the temperature example and let them argue against it. |
| "Where did 48.6 come from?" | I fiddled until it looked right. | If they assume there is a formula, say plainly that there is not, and that assuming there is one is exactly how people get fooled. |

---

### 💻 Live-Code Together — Build the Lie, Then the Pair (18 minutes)

You type; the student types along. **Two deliberate mistakes, marked 🐞, and both of them are silent** — no error, no warning, just a chart that is not the chart you meant. That is the theme of Term 3 and this is the last chance to hammer it.

#### Step 1 — build the lie, and print the arithmetic (8 min)

**Do this:** New file, `week27_lie.py`.

```python
# week27_lie.py -- build the lie on purpose. Two true numbers, one dishonest axis.
import matplotlib.pyplot as plt

classes = ["7A", "7B"]                 # the two categories
on_time = [49, 51]                     # % of homework handed in on time. Both TRUE.

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(classes, on_time)

bottom, top = 48.6, 51.4               # THE TRICK: the axis does not start at zero
ax.set_ylim(bottom, top)

ax.set_title("7B is MILES ahead of 7A on homework")   # a title doing the lying too
ax.set_xlabel("Class")
ax.set_ylabel("Homework on time (%)")

fig.savefig("lie.png", dpi=120, bbox_inches="tight")
print("saved lie.png")
```

**Say this:**

> "Notice `bottom, top = 48.6, 51.4` — two names, one equals, same trick as `fig, ax`. And notice the title. **The title is lying too.** 'Miles ahead' is a claim, and it isn't true, and a title that overclaims is the second-cheapest lie in this subject after the axis."

🐞 **Now make the first mistake.** Change the ylim line to:

```python
ax.set_ylim(bottom)
```

Run it. **No error.**

```text
saved lie.png
```

Open the PNG. The bars are still there but the top of the axis has moved — matplotlib picked its own top, so the chart is not the one you designed.

> "No error. No warning. A perfectly saved chart that isn't the chart I wrote. `set_ylim` wants **two** numbers, and if you give it one it takes it as the bottom and makes up the top. This is the Term 3 lesson again, for about the fifth time: **the dangerous failure is the one that doesn't complain.**"

Fix it back to `ax.set_ylim(bottom, top)` and add the arithmetic:

```python
# --- the arithmetic that proves it is a lie ---------------------------------
visible_a = on_time[0] - bottom        # how much of 7A's bar sits above the floor
visible_b = on_time[1] - bottom        # same for 7B
print(f"7A: {on_time[0]}%  -> visible bar = {visible_a:.1f} units")
print(f"7B: {on_time[1]}%  -> visible bar = {visible_b:.1f} units")
print(f"looks-like ratio  7B / 7A = {visible_b / visible_a:.2f} times taller")
print(f"honest ratio      7B / 7A = {on_time[1] / on_time[0]:.4f} times taller")
print(f"exaggeration factor       = {(visible_b / visible_a) / (on_time[1] / on_time[0]):.2f}")

# --- and the millimetres, so a ruler can check us --------------------------
axes_height_inches = ax.get_position().height * fig.get_figheight()
mm_per_unit = axes_height_inches * 25.4 / (top - bottom)
print(f"the drawing frame is {axes_height_inches:.2f} inches tall")
print(f"that is {mm_per_unit:.1f} mm per percentage point")
print(f"7A bar should measure {visible_a * mm_per_unit:.0f} mm")
print(f"7B bar should measure {visible_b * mm_per_unit:.0f} mm")
```

```text
saved lie.png
7A: 49%  -> visible bar = 0.4 units
7B: 51%  -> visible bar = 2.4 units
looks-like ratio  7B / 7A = 6.00 times taller
honest ratio      7B / 7A = 1.0408 times taller
exaggeration factor       = 5.76
the drawing frame is 3.08 inches tall
that is 27.9 mm per percentage point
7A bar should measure 11 mm
7B bar should measure 67 mm
```

**Do this:** Put the ruler back on the printed chart and point at the last two lines.

> "Eleven millimetres and sixty-seven millimetres. **That's what you measured with a ruler, twenty minutes ago, before I told you anything.** The program predicted your ruler.
>
> Those last four lines are doing something clever, by the way, and they are worth reading once even if you type them straight in: they ask matplotlib how tall the drawing frame actually is in inches, turn that into millimetres, and divide by how many percentage points the axis covers. That gives millimetres per point. Then the bar lengths fall out."

#### Step 2 — the honest version beside it, and 🐞 mistake #2 (10 min)

**Do this:** New file, `week27_pair.py`.

```python
# week27_pair.py -- the lie and the fix, in ONE figure, side by side.
import matplotlib.pyplot as plt

classes = ["7A", "7B"]
on_time = [49, 51]

# subplots(1, 2) = one row, two frames. axes holds BOTH frames, numbered 0 and 1.
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
print("how many frames?", len(axes))
```

Run it:

```text
how many frames? 2
```

> "Two frames. One sheet. And `axes` isn't a frame — it's a **box holding two frames**, numbered from zero, exactly like a list. `axes[0]` is the left one. `axes[1]` is the right one."

🐞 **Now the second mistake.** Type:

```python
axes.bar(classes, on_time)
```

Run it:

```text
how many frames? 2
Traceback (most recent call last):
  File "/Users/you/ai-academy/level2/week27_pair.py", line 11, in <module>
    axes.bar(classes, on_time)
AttributeError: 'numpy.ndarray' object has no attribute 'bar'. Did you mean: 'var'?
```

> "Read the last line."

Let them read it.

> "`'numpy.ndarray' object has no attribute 'bar'`. Translate it: **'`axes` is a box, not a frame. Which frame did you mean?'**
>
> And ignore the 'did you mean var' bit — Python's guessing, and this time it's guessing badly. `var` is a numpy thing about variance and it has nothing to do with what I want. **Python's suggestions are hints, not answers.** That's worth knowing."

Fix it and finish both panels:

```python
# ---- LEFT frame: the lie --------------------------------------------------
axes[0].bar(classes, on_time)
axes[0].set_ylim(48.6, 51.4)                     # the trick
axes[0].set_title("LIE: y-axis starts at 48.6")
axes[0].set_xlabel("Class")
axes[0].set_ylabel("Homework on time (%)")

# ---- RIGHT frame: the honest version -------------------------------------
axes[1].bar(classes, on_time)
axes[1].set_ylim(0, 100)                         # the fix. One argument.
axes[1].set_title("HONEST: y-axis starts at 0")
axes[1].set_xlabel("Class")
axes[1].set_ylabel("Homework on time (%)")

fig.suptitle("The same two numbers: 49% and 51%")
fig.savefig("lie_and_fix.png", dpi=120, bbox_inches="tight")
print("saved lie_and_fix.png")
```

```text
how many frames? 2
saved lie_and_fix.png
```

**Do this:** Open it. Look at both panels together, then measure the right-hand panel's two bars with the ruler as well.

> "Measure the honest ones. Go on."

They will get something like 38 mm and 40 mm (the program prints 0.78 mm per unit, so 49 and 51 units) — nearly identical, ratio about 1.05 from whole-millimetre readings, 1.04 exactly.

> "Thirty-eight and forty. Ratio one point oh four. **Which is the truth.**
>
> And notice what putting them side by side does. On its own, the left panel is convincing. Next to the right panel it's obviously a stunt. **The best defence against a misleading chart is another chart.**
>
> Oh — and `fig.suptitle`. Each frame has its own title, and that one is the headline across the whole sheet. You don't need it; it's just tidy."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "How many frames does `subplots(1, 2)` make, and what are they called?" | Two: `axes[0]` and `axes[1]`. | If they say `axes[1]` and `axes[2]`, that is the Week 11 off-by-one. Let them try `axes[2]` and read the `IndexError`. |
| "Read the last line of that AttributeError." | `'numpy.ndarray' object has no attribute 'bar'` | If they get stuck on 'ndarray', say: "It's numpy's word for a box of things. From Week 17." |
| "Python suggested `var`. Should you use it?" | No. The suggestion is wrong this time. | Important check. If they say yes, let them try it and read the next error. |
| "Now measure the honest bars. What's the ratio?" | About 1.04. | If they measure identical lengths, that is fine and it is the point — 49 and 51 are nearly the same. |
| "Which panel would you put on a poster, if you wanted 7A to get in trouble?" | The left one. | Let them enjoy the answer, then: "So what will you look at first, next time somebody shows you a bar chart?" |

---

### 🎲 Their Turn — Legend, Correlation, and Who Gets Hurt (20 minutes)

Student on the keyboard. Full instructions in the next section.

- **Minutes 0–6:** two lines on one frame, with a legend.
- **Minutes 6–12:** compute `r` for hours vs score, and the three ice-cream correlations.
- **Minutes 12–20:** the ethics question, written down, and the start of the Term 3 reflection (Build It, Part 6).

---

## 🎲 The Activity, In Full

This section is the Their Turn segment written out: the setup, then each part step by step.

### Setup

**On the table:** the workbook open at Predict the Output P3 (legend), P4 and Practice Set B, B1 (correlation), Think Deeper T2 (the ethics question) and Build It Part 6 (Term 3 reflection). Ruler, pencil, calculator.

**On the machine:** `level2` folder, venv active, `students.py` and `myweek.py` present.

### Part A — Two lines, one legend (6 minutes)

```python
# week27_legend.py -- two lines on one frame, so a legend becomes compulsory.
import matplotlib.pyplot as plt
from myweek import build_my_week

df = build_my_week()

fig, ax = plt.subplots(figsize=(6, 4))

# Each plot call gets its own label=... . That text is what the legend prints.
ax.plot(df["day"], df["homework_min"], marker="o", label="Homework")
ax.plot(df["day"], df["screen_min"], marker="s", label="Screen time")

ax.set_title("Screen time and homework crossed over at the weekend")
ax.set_xlabel("Day of the fortnight (day 1 = first Monday)")
ax.set_ylabel("Minutes")
ax.set_ylim(0, 200)
ax.legend()                          # reads the labels you already gave

fig.savefig("two_lines.png", dpi=120, bbox_inches="tight")
print("saved two_lines.png")
```

```text
saved two_lines.png
```

> **💡 Try this:** have them delete both `label="..."` bits and run it again. No error — just a warning, and a chart with no legend:
>
> ```text
> No artists with labels found to put in legend.  Note that artists whose label start with an underscore are ignored when legend() is called with no argument.
> ```
>
> "'Artists' is matplotlib's word for anything you drew. It's saying: *you asked me to name the lines and none of them have names.*"

Then the point about markers:

> **🧑‍🏫 If a student asks:** *"Why is one marker a circle and one a square? The colours are already different."* — Because this chart will be photocopied, printed in black and white, or read by somebody who cannot tell those two colours apart, and in every one of those cases the colour is gone and the shapes are not. Two cues instead of one costs nothing. It is simply what a careful person does.

### Part B — Correlation, and the three numbers that ruin it (6 minutes)

```python
# week27_corr.py -- one number for "do these two move together?"
import pandas as pd
from students import build_students

df = build_students()

r_hours_score = df["hours"].corr(df["score"])     # -1 .. 0 .. +1
print(f"study hours vs score : r = {r_hours_score:.3f}")

r_age_hours = df["age"].corr(df["hours"])
print(f"age vs study hours   : r = {r_age_hours:.3f}")

# Six months of a seaside town. Two of these columns rise together almost perfectly.
town = pd.DataFrame({
    "month":      ["Jan", "Mar", "May", "Jul", "Sep", "Nov"],
    "ice_creams": [200, 400, 800, 1400, 900, 300],
    "drownings":  [1, 2, 5, 9, 6, 2],
    "temp_c":     [12, 16, 25, 32, 26, 15],
})

print()
print(f"ice creams vs drownings  : r = {town['ice_creams'].corr(town['drownings']):.3f}")
print(f"temperature vs ice creams: r = {town['temp_c'].corr(town['ice_creams']):.3f}")
print(f"temperature vs drownings : r = {town['temp_c'].corr(town['drownings']):.3f}")
```

```text
study hours vs score : r = 0.925
age vs study hours   : r = -0.572

ice creams vs drownings  : r = 0.997
temperature vs ice creams: r = 0.987
temperature vs drownings : r = 0.989
```

**The three questions to ask, in this order:**

1. *"Ice cream and drowning: nought point nine nine seven. Almost perfect. Should we ban ice cream?"* — obviously not.
2. *"So what's really going on?"* — hot weather. People buy ice cream **and** people swim. **Hot weather is the confounder.**
3. *"Now look at all three numbers. Which is the biggest?"* — the ice cream one, **0.997**, the one that is causally absurd. That is the whole point: **strength tells you nothing about direction.**

> **⚠️ Watch out:** somebody will try `df["club"].corr(df["score"])`. It fails, and the last line is `TypeError: unsupported operand type(s) for /: 'str' and 'int'`. Translate it: *"you asked me to divide the word 'chess' by a number."* Correlation is for numbers only.

### Part C — Who gets hurt? (8 minutes)

**Do this:** Put Think Deeper T2 (and Build It Part 5) in front of them. Have `hours_vs_score.png` from Week 26 open on screen.

**Say this:**

> "Study hours and marks: nought point nine two five. Really strong. Now imagine a head teacher sees this chart and does the obvious thing: **everybody does two extra hours of study a week.**
>
> Before you decide whether that's a good idea, I want you to find out **who is actually at the bottom of that scatter.** Print them."

```python
# week27_who.py -- who is at the bottom of the scatter?
from students import build_students

df = build_students()

print("studying an hour or less:")
print(df[df["hours"] <= 1.0][["name", "age", "house", "club", "hours", "score"]].to_string(index=False))
print()
print("studying five hours or more:")
print(df[df["hours"] >= 5.0][["name", "age", "club", "hours", "score"]].to_string(index=False))
```

```text
studying an hour or less:
       name  age house  club  hours  score
 Hugo Silva   14   Red music    0.5     45
Omar Haddad   14  Blue music    1.0     52
  Sami Aden   14 Green   art    0.5     48
Bruno Costa   13 Green   art    1.0     50
 Greta Hahn   14  Blue music    0.5     42

studying five hours or more:
       name  age  club  hours  score
   Bela Roy   14 music    5.0     90
 Farah Aziz   12 chess    6.0     95
 Liam Byrne   13 music    5.5     81
 Tara Joshi   12 chess    5.0     97
Anika Verma   12 music    5.0     93
  Hana Sato   12   art    5.5     91
```

> "Look at the ages. Every single student studying an hour or less is thirteen or fourteen. Four of the six studying five hours or more are twelve.
>
> Now the question that matters, and I want it written on the page: **why might a fourteen-year-old be studying half an hour a week?**"

Take every answer they offer. The good ones: a job. A younger brother or sister to look after. No quiet room. A long journey to school. Illness. Something going on at home.

> "None of those are on the chart. Not one. And **none of them are fixed by being told to study more** — they're *punished* by it. Hugo gets a detention for a bus timetable.
>
> So write the honest sentence, in Build It, Part 5. Here's mine, and yours can be better:
>
> *'In this table, students who studied more hours tended to score higher (r = 0.93). I do not know whether studying caused the higher marks. A quiet room at home could be causing both, and that would mean the students at the bottom of this chart are being blamed for something the chart never measured.'*
>
> Read it back. **Notice there is no word in it that means 'caused'.** That's the discipline."

### What "finished" looks like

- `two_lines.png` saved, with a legend naming both series and two different marker shapes.
- `r = 0.925` and the three ice-cream numbers printed and written next to Predict the Output P4 and Practice Set B, B1.
- A written sentence (Build It Part 5) about `r = 0.93` that contains **no causal verb**, plus a named plausible confounder.
- At least three specific reasons a student might study very little, none of which are on the chart.
- The Term 3 reflection (Build It, Part 6) started, with at least two weeks named.

### Variation — easier

- **Cut Part A.** The legend is one call and can be shown in ninety seconds rather than built.
- **Cut the ice-cream table.** Just do `r = 0.925` and the ethics question. Objective 4 is met by the *refusal*, not by the arithmetic.
- **Do the ethics question out loud, and write only one sentence.** The talking is the learning; the writing is the record.
- **Give them the sentence with three blanks:**

  > "In this table, students who ______ tended to ______. I do **not** know whether ______ caused ______, because ______ could be causing both."

**One thing you must not cut:** the ruler. Physically measuring two bars and getting six is the memory that survives the year.

### Variation — harder

1. **Push the lie as far as it will go.** "Find the `set_ylim` bottom that makes 7B look **fifty** times taller than 7A." It is real algebra, of the kind they have had for a year: (51 − b) ÷ (49 − b) = 50, so 51 − b = 2450 − 50b, so 49b = 2399, so **b = 48.9592**. Then build it and measure it. And notice how sharp the edge is: rounding the bottom to 48.96 gives **51×**, not 50×. Moving the floor by less than a thousandth of a percentage point (0.0008) changes the lie by a factor of one.
2. **Truncate a line chart honestly.** Take the `sleep_hours` column (7.0 to 9.5) and chart it twice: once from 0, once from 6.5. The zero version is a flat line at the top and useless. Then write the label that makes the truncated one honest.
3. **A 2×2 grid.** `fig, axes = plt.subplots(2, 2, figsize=(10, 8))`. Now `axes` is a box of boxes and you index it `axes[0][0]`, `axes[0][1]`, `axes[1][0]`, `axes[1][1]`. Four of their Term 3 charts on one sheet. No new function, just one more index.
4. **Invent a confounder.** "Give me a pair of columns from this table with a strong correlation, and a third thing — not in the table — that could be causing both." Good answers involve `age` and `hours` with "how much homework the school sets by year group" as the confounder.
5. **Catch one in the wild.** Find a real misleading chart — a news site, an advert, a phone's battery graph, a shop's "our prices vs theirs" poster. Name the trick, and if the numbers are printed, compute the exaggeration factor. Bring it in.

---

## 🐞 The Debugging Clinic

Every message below came from running a genuinely broken version of this week's code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `AttributeError: 'numpy.ndarray' object has no attribute 'bar'. Did you mean: 'var'?` | "`axes` is a box of frames, not a frame. Which one did you mean?" | `axes.bar(...)` after `plt.subplots(1, 2)`. Forgot the index. **Ignore the `var` suggestion — it is wrong here.** | `axes[0].bar(...)` or `axes[1].bar(...)`. |
| `AttributeError: 'numpy.ndarray' object has no attribute 'set_title'` | Same thing, on a different call. | `fig, ax = plt.subplots(1, 2)` and then `ax.set_title(...)`. The name `ax` is misleading — with two frames it is a box. | Index it, and rename it `axes` so the plural reminds you. |
| `IndexError: index 2 is out of bounds for axis 0 with size 2` | "There are two frames and you asked for the third." | `axes[2]`. Frames are numbered 0 and 1, exactly like list slots in Week 11. | `axes[0]` and `axes[1]`. |
| `TypeError: unsupported operand type(s) for /: 'str' and 'int'` (after ~10 lines of pandas and numpy) | "You asked me to divide a word by a number." | `df["club"].corr(df["score"])` — correlation on a text column. | Correlation is for numbers only. Pick two number columns. *(On pandas 2.x the message is `ValueError: could not convert string to float: 'chess'` — same cause.)* |
| `TypeError: Series.corr() missing 1 required positional argument: 'other'` | "You asked for a correlation between one thing and nothing." | `df["hours"].corr()` — forgot the second column. | `df["hours"].corr(df["score"])`. |
| `No artists with labels found to put in legend.` *(a warning, not an error — the chart still saves)* | "You asked me to name the lines and none of them have names." | `ax.legend()` with no `label="..."` on any `plot` call. | Add `label="Homework"` and `label="Screen time"` to the two `plot` calls. |
| **No error. The chart is upside down, bars hanging from the top.** | Nothing. You told it the axis runs downwards. | `ax.set_ylim(51.4, 48.6)` — the two numbers the wrong way round. | Smaller number first: `ax.set_ylim(48.6, 51.4)`. |
| **No error. The chart saves, but the top of the axis is not where you put it.** | Nothing. You gave it a bottom and let it choose a top. | `ax.set_ylim(48.6)` — one argument instead of two. | Give it both: `ax.set_ylim(48.6, 51.4)`. |
| **No error. A line chart that looks dramatic and is not.** | Nothing at all. matplotlib's default for a **line** chart is to zoom in on the data (bars, by contrast, start at zero on their own). | `set_ylim` left out entirely on a `plot` call, so matplotlib truncated the axis for you. | `ax.set_ylim(0, top)`, or truncate deliberately and say so in the label. On bar charts, type `ax.set_ylim(0, top)` anyway so the decision is visible in the file. |
| `ValueError: x and y must have same first dimension, but have shapes (10,) and (12,)` | "Ten of one, twelve of the other." | Two series of different lengths on one frame — usually one column from `myweek` (10 rows) and one from somewhere else. | `print(len(a), len(b))` and find the mismatch. |

### How to teach debugging without giving the answer

The ladder is unchanged — **read the last line, name the line number, say what you expected, print the thing just before** — but this week adds a rule that is worth stating explicitly, because it comes straight out of Live-Code Step 2:

> **Python's "Did you mean…?" suggestions are hints, not answers.**

`'numpy.ndarray' object has no attribute 'bar'. Did you mean: 'var'?` — the suggestion is *wrong*. `var` is a numpy function about variance and has nothing to do with drawing a bar. Python matched the letters, not the meaning. A student who follows every suggestion blindly will fix three errors and then be badly lost on the fourth. **Read the suggestion, then decide.**

And the other rule, four times over in the table above: **four of the ten rows produce no error at all.** So the first question is never "what does the error say?" It is:

> **"Is that the chart you meant to make?"**

---

## ❓ Questions Students Ask This Week

Use this section to prepare answers to the questions this lesson tends to raise.

**"Isn't it fine if the numbers are printed on the chart? Then nobody's lying."**

It is better, and it is not enough, and the reason is worth understanding. People read charts with their eyes before they read them with their brain — the shape lands in about a quarter of a second, the numbers take two or three seconds, and most people never get to the numbers at all. A truncated bar chart with correct numbers printed on it will still leave nearly every reader believing the wrong thing. The numbers are your defence in an argument afterwards. They are not a defence against the impression the chart made.

**"So is every chart a lie?"**

No, and this is the trap of a lesson this vivid. Look at the right-hand panel: same two numbers, axis from zero, ratio 1.04, and it is a completely honest chart that tells you the truth in half a second. The lesson is not "charts lie". It is: **a chart is an argument, and you check an argument's framing before you accept it.** Same as you would with a sentence.

**"Who decides what's misleading? Isn't it just an opinion?"**

Partly, and the honest answer has two halves. Some of it is not opinion at all: a bar chart with a truncated axis deletes length that the reader's eye is being asked to measure, and you can compute the exaggeration factor as an actual number — that is arithmetic, not taste. The rest genuinely is judgement: whether *this* chart, for *this* audience, making *this* decision, hides something that would change the decision. Two careful people can disagree about that. What is not a matter of opinion is the procedure: **state where your axis starts, and say what your chart hides.** Do those two things and nobody can accuse you of hiding anything.

**"Why do we use `r` and not a percentage?"**

Because `r` is not a proportion of anything. It is a position on a scale from −1 through 0 to +1. Try turning it into a percentage and it falls apart immediately: `r` between age and hours is **−0.572**, and "minus fifty-seven percent of a study hour" means nothing at all. There *is* a related number that behaves a bit more like a percentage — R², which you meet in Week 32 — and even that one is misread constantly by people who should know better.

**"If the correlation was 1.0 — perfect — would that prove cause?"**

No, and this is the best question anybody asks this week. A perfect correlation is *still* consistent with all four worlds. Suppose you measured the same thing twice with two instruments: perfect correlation, and neither one causes the other. Or suppose one thing genuinely causes both perfectly. **Strength tells you how tightly two columns move together. It tells you nothing about which way the arrow points, or whether there is an arrow at all.** Our own numbers make it: the *strongest* of the three correlations, 0.997, is the ice cream one, and that one is nonsense.

**"How would you ever prove that studying causes higher marks, then?"**

You would need an **experiment**, not a chart. Take a large group, split them **randomly** into two halves — randomly is the whole trick, because it means the two halves have similar homes, similar sleep, similar everything — then ask one half to study two extra hours and leave the other half alone, and compare the results afterwards. Because the split was random, any difference is much more likely to be the studying. That is genuinely how it is done, and it is why medical trials work the way they do. And notice: an experiment on schoolchildren's study time raises real questions about fairness, which is exactly why this stuff is hard and not just fiddly.

**"Is a truncated y-axis ever actually the right choice?"** *(Genuinely contested. Say so.)*

**Nobody fully agrees, and here is why it is not a dodge.** For **bars**, essentially everybody agrees: start at zero, no exceptions, because the eye is comparing lengths and you cannot un-delete length.

For **lines**, it is a real, live argument. One camp says: a line chart shows change, so scale the axis to the change — a body-temperature chart from absolute zero is not more honest, it is just useless. The other camp says: readers are trained by bar charts to treat height as amount, they do not check axes, and a truncated line chart of a company's income will be screenshotted into a group chat where it will fool everybody. Both camps have a point, and both include people who do this for a living.

The rule most careful people converge on, and it is worth writing down: *does the value zero mean anything for this quantity, and is the reader comparing lengths or following a shape?* Body temperature: zero is meaningless, and you are following a shape — truncate. Homework percentages: zero means something real, and you are comparing lengths — do not.

And the half everybody agrees on: **if you truncate, say so in the label, loudly.** The disagreement is about the choice. There is no disagreement about hiding it.

---

## ⚠️ Where This Lesson Goes Wrong

This table lists the usual ways the lesson slips, why each happens, and what to do on the spot.

| What happens | Why | What to do right now |
|---|---|---|
| The student sees the y-axis numbers before measuring | The chart is right there and the numbers are printed on it | **Cover them physically** before the lesson. Fold the paper or tape over them. Once "49" and "51" have been read, the ruler moment is gone and cannot be got back. |
| The measuring happens on screen | It is right there and nobody has to fetch paper | Do not allow it. On a screen they can zoom, both bars change together, and the number stops being *theirs*. A printed page has one size and a ruler fits on it. |
| The student measures 9 mm and 54 mm and thinks they got it wrong | The printer scaled the page | Say it **before** they measure: "Your printer may have shrunk this. Both bars shrink together, so the ratio is what counts." Then 54 ÷ 9 = 6.0 and everyone is happy. |
| The lesson lands as "all charts are lies" | It is a vivid lesson and cynicism is the easy conclusion | Finish on the honest panel every single time. Same numbers, axis from zero, ratio 1.04, and it is a good chart. Say the sentence: **"A chart is an argument. Check the framing."** |
| "48.6" gets treated as a magic number | It looks derived, because numbers in lessons usually are | Tell the truth: you fiddled with it. Then get them to find the bottom that gives 20×. The absence of a formula *is* the lesson. |
| The correlation section turns into a maths lesson about how `r` is calculated | Somebody asks, and it feels rude not to answer | "It's squares and square roots over both columns, and knowing the formula would not help you at all today. What matters is what it can and cannot tell you." Then straight back to the four worlds. |
| The ethics question gets a shrug — "it's just a chart" | It is abstract until it has a name in it | Print the two lists. Hugo, Sami, Greta, Omar, Bruno. Then: "Hugo gets a detention. Why is Hugo studying half an hour a week?" A name changes the conversation completely. |
| `axes` vs `axes[0]` causes twenty minutes of confusion | The name looks like one thing and is a box of things | Rename it out loud: "It is called `axes` because it is **plural**." Then have them `print(len(axes))` — it prints `2` — and the plural becomes concrete. |
| A **line** chart gets drawn with no `set_ylim` at all and looks dramatic | matplotlib's default for lines zooms in on the data (for bars it starts at zero on its own: `(0.0, 53.55)` for 49 and 51) | Worth catching: **matplotlib truncates line charts for you if you do not stop it.** From today, every bar chart gets `ax.set_ylim(0, top)` so the decision is visible, and every line chart gets a deliberate choice. |
| The reflection sheet gets "all fine" written on it | It is the last thing, everybody is tired, and admitting confusion feels bad | Make it structurally impossible: "Name **two** weeks you'd want to do again, with a reason. Everybody has two. I have two, and I wrote this." |

---

## 🧭 Differentiation

Use this section to adjust the lesson for a student who is struggling and for one who is racing ahead.

### If the student is struggling

**Cut:** Part A (the legend) and the ice-cream table. Keep the ruler, the two panels, and `r = 0.925` with the ethics question.

**Reteach:** the sticking point is nearly always `axes[0]` versus `axes`. Do it on paper. Draw one big rectangle — that is the **figure**, the sheet. Rule it down the middle into two boxes. **Number them 0 and 1, in pen.** Now point at the sheet and say "this is `fig`". Point at the pair of boxes and say "these two together are `axes`". Point at the left box: "`axes[0]`". Point at the right: "`axes[1]`". Then the killer question: **"Where is `axes[2]`?"** There isn't one, and that is the `IndexError` they saw. Ninety seconds.

**Copy-this-exactly scaffold** — runs on its own, nothing else needed in the folder:

```python
# week27_scaffold.py -- copy this exactly, then change only the two ylim numbers.
import matplotlib.pyplot as plt

classes = ["7A", "7B"]
on_time = [49, 51]

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].bar(classes, on_time)
axes[0].set_ylim(48.6, 51.4)          # <-- the LIE. Try 48.9. Then try 48.99.
axes[0].set_title("LIE")
axes[0].set_xlabel("Class")
axes[0].set_ylabel("Homework on time (%)")

axes[1].bar(classes, on_time)
axes[1].set_ylim(0, 100)              # <-- the FIX. Never change this one.
axes[1].set_title("HONEST")
axes[1].set_xlabel("Class")
axes[1].set_ylabel("Homework on time (%)")

fig.savefig("my_lie_and_fix.png", dpi=120, bbox_inches="tight")
print("saved my_lie_and_fix.png")
print("left panel ratio :", round((51 - 48.6) / (49 - 48.6), 2), "times taller")
print("right panel ratio:", round(51 / 49, 4), "times taller")
```

```text
saved my_lie_and_fix.png
left panel ratio : 6.0 times taller
right panel ratio: 1.0408 times taller
```

Changing one number and watching 6.0 become 21.0 is a complete, honest version of objective 1.

**Reduce:** accept the ethics answer spoken rather than written, and accept one reason instead of three.

**One thing you must not cut:** the ruler. If everything else goes, "I measured two bars and one was six times the other, and the real difference was two percent" is the memory that lasts.

### If the student is flying

1. **Solve for the exaggeration.** "What `set_ylim` bottom makes it look exactly 50 times bigger?" It is real algebra: (51 − b) ÷ (49 − b) = 50 → 51 − b = 2450 − 50b → 49b = 2399 → **b = 48.9592**. Build it, print it, measure it.
2. **A 2×2 grid.** `plt.subplots(2, 2, figsize=(10, 8))`, indexed `axes[0][0]` through `axes[1][1]`. Put four Term 3 charts on one sheet. No new function; one more index.
3. **Honestly truncate a line chart.** Chart `sleep_hours` from 0 and from 6.5. The first is useless. Then write the axis label that makes the second one honest, and defend it.
4. **The confounder hunt in their own data.** "Find two columns in `myweek` that correlate, and name a third thing not in the table that could cause both." Strong answer: `homework_min` and `sleep_hours` correlate negatively, and the confounder is "how much work the school set that day".
5. **Catch one in the wild and do the arithmetic.** A real chart, the trick named, and the exaggeration factor computed as a number. This is the highest-value extension in the term.
6. **The one that has no answer.** "Somebody shows you a bar chart with the axis starting at zero and correct labels. What can still be wrong with it?" Good answers: which categories were left out; how many rows each bar came from; whether the *categories* were chosen to flatter; whether the question was the right question. Let this one run.

### If the student won't engage today

Do the Hook, and stop.

Seven minutes: measure two bars, divide, get six, then uncover the axis and find out the real difference is two percent. That is a complete lesson with an actual gasp in it, and it needs no computer.

Then make it a game: **"Spot the Floor."** You show them a bar chart — on paper, on a phone, in a newspaper — and they get one point for saying where the y axis starts before you tell them. Ten rounds. You are allowed to include zero-based charts to keep them honest. Battery graphs, "our broadband vs theirs" adverts and sports statistics are a rich seam.

That game delivers objective 1 completely, and it is genuinely the habit you most want them to leave the term with. The `subplots(1, 2)` code will still be there tomorrow.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the exaggeration (spoken, with a calculator allowed)**

> "Two bars, 49 and 51. I start the axis at 48. How many times taller does the second bar look, and how many times taller is it really?"

*Good answer:* looks (51 − 48) ÷ (49 − 48) = **3 times**; really 51 ÷ 49 = **1.04 times**. Full marks needs both numbers. **What to catch:** only computing one of them. The pair is the point — a single number is not an exaggeration factor.

**Check 2 — the zero rule (spoken)**

> "Name one chart where the y axis must start at zero, and one where it doesn't have to. Say why for each."

*Good answer:* a bar chart must (the eye compares lengths); a line chart of something like body temperature need not (the eye follows a shape, and zero is not meaningful). **What to catch:** "all of them" or "none of them". Both are over-corrections. Give them the temperature example and ask them to argue.

**Check 3 — correlation and cause (spoken)**

> "Ice cream sales and drownings correlate at 0.997. Give me the reason that isn't 'ice cream causes drowning'."

*Good answer:* hot weather causes both — people buy ice cream and people swim. Full marks needs the *third thing* named, not just "it's a coincidence". **What to catch:** "it's just a coincidence". Reply: "It happens every single summer. Coincidences don't repeat. What repeats every summer?"

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot say where a chart's axis starts. Believes a chart because it looks dramatic. Reads a strong correlation as proof of cause. |
| **2 — Emerging** | Can point at a truncated axis when told to look. Changes a `set_ylim` number in a scaffold. Says "correlation isn't causation" as a slogan without being able to give the third thing. |
| **3 — Secure** | Builds a truncated bar chart and its honest twin in one two-panel figure, unaided. Computes the exaggeration factor from the two bar lengths. Adds a legend with `label=`. Writes a sentence about `r` with no causal verb and names a plausible confounder. **This is the target.** |
| **4 — Strong** | Explains why the zero rule is strict for bars and negotiable for lines. Notices that the strongest of the three ice-cream correlations is the absurd one. Names three specific, non-blaming reasons a student might study very little. Spots a silent `set_ylim` mistake without an error message. |
| **5 — Exceptional** | Solves for the `set_ylim` bottom that produces a chosen exaggeration factor. Catches a misleading chart in the wild and computes its exaggeration factor. Argues both sides of the truncated-line-chart question and lands somewhere defensible. Traces a chart to a decision to a named person who gets hurt. |

---

## 📤 Homework to Assign

This section gives you the words to assign the homework, piece by piece.

**Say this:**

> "Three pieces, about an hour and a bit. This one is the end of the term, so it is worth doing properly.
>
> **First, the lie and the fix, with the arithmetic — Build It, Parts 1 to 3.** Take **one** of your own charts from Week 26 — the house averages is the easiest one to sabotage — and build a two-panel figure: the lie on the left, the honest version on the right. Then print the arithmetic: what the ratio *looks like*, what it *really is*, and the exaggeration factor. And then, and this is the bit I want, **print the two panels and measure the bars with a ruler, in millimetres.** Write both measurements and the division in the Part 2 table. If your printer shrinks the page, that's fine — the ratio survives. Practice Set B, question B5, is the same job in miniature if you want to see what the finished program looks like first.
>
> **Second, the Five-Chart Data Story — Build It, Parts 4 and 5.** Five charts from your cleaned table, arranged so they read **in order, like a story**: context, then the baseline, then the main finding, then a chart that *challenges* your finding, then the caveat. One captioned sentence under each. Read the five captions on their own, out loud — they should make sense as a paragraph with no charts at all. If they don't, the order is wrong. Then Part 5: one correlation from your table, and the honest sentence about it.
>
> **Third, the Term 3 reflection — Build It, Part 6.** Eight weeks, nineteen to twenty-six. For each one: a tick if you could teach it to somebody else, a question mark if you'd want to look at it again. And then name **two** weeks you actually want to revisit, with a reason. Not 'it was hard'. Something like 'I still can't tell `loc` from `iloc` when the index isn't 0, 1, 2'. Everybody has two. I have two."

**Workbook sections, and where they are done.** The workbook has no "Page 27.N" numbering; it is a run of named sections, so the split is by section:

| Section | Where |
|---|---|
| ✅ Warm-Up (W1–W5) | In class, first five minutes |
| 🔎 Predict the Output (P1–P4) | In class — P1 and P2 go with the Live-Code steps, P3 and P4 with Activity Parts A and B |
| ✍️ Practice Set A (A1–A6) | In class — A1 and A5 straight after the Hook and Concept (they are the measuring, done with numbers and on the diagram); A2–A4 and A6 as the student has time |
| ✍️ Practice Set B, B1 | In class, Activity Part B (the `r = 0.925` line) |
| ✍️ Practice Set B, B2–B4 | Home, as warm-up for the main pieces; skip B2 and B3 if the student goes straight to Build It, because Parts 1–2 repeat them |
| ✍️ Practice Set B, B5 | Home, with Build It Parts 1–3 (it is the same program, with its expected output printed) |
| 🛠️ Build It, Parts 1–3 (lie, arithmetic and ruler, confession) | **Home — piece one** |
| 🛠️ Build It, Parts 4–5 (Five-Chart Story, honest `r` sentence) | **Home — piece two** |
| 🛠️ Build It, Part 6 (Term 3 reflection) | **Home — piece three** |
| 🛠️ Build It, Part 7 (Bug Log); 🐞 Fix the Broken Program; 🧩 Puzzle of the Week; 🤔 Think Deeper; 🎨 Draw It; 📊 Self-Check | Extension — assign as many as time allows over the week; Think Deeper T2 is the written version of Activity Part C |

**Expected time:** 20 min for the lie-and-fix with the measuring · 40 min for the Five-Chart Data Story · 10 min for the reflection. About 70 minutes — slightly over, because it is the end of the term. The extension sections are on top of that and optional.

---

## 🔑 Answer Key

This key follows the workbook **section by section, in workbook order**, and every item is answered with the workbook's own Answers section as the source. The workbook has no numbered pages. Sections marked *(teacher-only)* are extra notes for you. The hook and the Activity use a few questions that are not on any workbook section; they are kept at the end of the key, under **Prompts used in the lesson**.

### ✅ Warm-Up

**W1.** A **histogram**, because it is one column of numbers with no categories, and the question is about the shape of the whole pile.

**W2.** **Whether the bars touch.** Touching means one bar per number range (histogram); gaps mean one bar per category (bar chart). Also full marks: whether the x axis holds names or numbers, or whether you could reorder the bars.

**W3.** A **histogram**, looking for whether the pile has **one hump or two** — because an average can land in a gap where nobody actually is. The quiz marks averaged 62 and nobody scored between 44 and 81.

**W4.** **38 rectangles**, one per row, crammed into three columns. There should be **3**. And there is no error.

**W5.** Any of: **how many rows each average came from** (Blue 14, Red 12, Green 12); the **spread** inside each house (Blue's scores run 42 to 93); or that Blue's lead over Red is **0.11 of a mark**.

### 🔎 Predict the Output

**P1** — real output:

```text
before: (0.0, 53.55)
after : (48.6, 53.55)
```

- **Does `set_ylim(48.6)` raise an error?** **No.** It set the bottom and left the top exactly where matplotlib had already put it.
- **Where did 53.55 come from?** **matplotlib chose it**, before the student touched anything — the top it picks automatically for a bar chart of 49 and 51, a little above the tallest bar.
- **The "before" line:** for a **bar** chart matplotlib started the axis at **zero all by itself**. A line chart of the same two numbers gets `(48.9, 51.1)` — truncated by default. So the tool protects you on bars and not on lines.

**P2** — real output:

```text
ndarray
2
(2,)
True
```

- **`ndarray`** is numpy's word for a box of things — **Week 17's array**, holding drawing frames instead of numbers. So `len(axes)` is 2, `axes.shape` is `(2,)`, and `axes[-1]` is Week 11's "last slot", which for two slots **is** `axes[1]`. Hence `True`.
- **`axes[2]`** gives `IndexError: index 2 is out of bounds for axis 0 with size 2`. Two slots, numbered 0 and 1.

**P3** — real output:

```text
No artists with labels found to put in legend.  Note that artists whose label start with an underscore are ignored when legend() is called with no argument.
saved two.png
```

- **It does not crash. The file appears. There is no legend on it.**
- **Error or warning?** A **warning**: there is **no `Traceback`**, and the program **carried on** and printed `saved two.png`. An error stops the program dead.
- **"Artists"** is matplotlib's word for **anything drawn on a frame** — a line, a bar, a dot, a piece of text.

**P4** — real output:

```text
1.0
1.0
1.0
nan
```

- **Lines 1 and 2 are identical**: correlation is **symmetric**, so the order you write the two columns does not matter. A number that does not know which column came first cannot tell you which one causes the other.
- **Line 3 is 1.0**: anything correlates perfectly with itself. A sanity check.
- **Line 4 is `nan`** — "not a number". The `age` column is **12 for everybody**, so it never varies, and the question "when this goes up, does that go up?" has no answer.
- **Does `r = 1.0` prove studying causes the score?** **No.** The five rows were made up by writing 50, 60, 70, 80, 90 next to 1, 2, 3, 4, 5. A perfect correlation is still consistent with all four worlds — including "I invented both columns".

### ✍️ Practice Set A

**A1.**

| bottom | 7A's bar | 7B's bar | The eye sees | Factor |
|---|---|---|---|---|
| 0 | 49 | 51 | 51 ÷ 49 = **1.04** | **1.00** |
| 45 | 4 | 6 | 6 ÷ 4 = **1.50** | 1.50 ÷ 1.0408 = **1.44** |
| 48 | 1 | 3 | 3 ÷ 1 = **3.00** | **2.88** |
| 48.6 | 0.4 | 2.4 | 2.4 ÷ 0.4 = **6.00** | **5.76** |
| 48.9 | 0.1 | 2.1 | 2.1 ÷ 0.1 = **21.00** | **20.18** |

- **A1(a).** Step 1: subtract the floor from both numbers to get the two visible bar lengths. Step 2: divide the big one by the small one, then divide that by the honest ratio (51 ÷ 49 = 1.0408).
- **A1(b).** It **grows without limit.** The smaller visible bar heads towards zero, so the ratio heads towards infinity. A floor of 48.99 gives 201×; 48.999 gives 2001×. Each extra 9 is one keystroke.
- **A1(c).** **None of them.** Both bar heights and every tick number are true. The only thing that changed was where the axis starts.
- *(teacher-only)* The 48.6 row is the one the hook ruler-measures: the student's 11 mm and 67 mm from the printed `lie.png` should give about 6.1, against the exact 6.00. See **Prompts used in the lesson** below.

**A2.**

| # | The call | Answer |
|---|---|---|
| a | `plt.subplots(1, 2, ...)` gives back… | **`fig, axes`** — a sheet and a box of two frames |
| b | `savefig(...)` | **`fig`** — you save the whole sheet |
| c | `suptitle(...)` | **`fig`** — a headline across the whole sheet |
| d | `bar(...)` on the left panel | **`axes[0]`** |
| e | `set_ylim(0, 100)` on the right panel | **`axes[1]`** |
| f | `print(len(...))` prints `2` | **`axes`** |
| g | `legend()` on a single-frame chart | **`ax`** |

**A2(h).** Because **it holds more than one frame.** `plt.subplots()` with no numbers hands back one frame, called `ax`; `plt.subplots(1, 2)` hands back two, called `axes`. The plural is a reminder that you have to index it.

**A3.**

| # | The chart | Answer | The reason |
|---|---|---|---|
| a | bar of 49% and 51% | **must start at 0** | Bars ask the eye to compare lengths, and zero means something for a percentage |
| b | line of body temperature | **need not** | A line asks you to follow a shape, and 0 °C is not a meaningful floor for a person |
| c | bar of club sizes 12, 12, 14 | **must start at 0** | Bars, and a count of zero members is perfectly meaningful |
| d | line of a share price over ten years | **need not** — the contested one | A line, so a shape; but a truncated share-price chart is the classic dishonest chart, so **say so in the label** |
| e | bar of house means 67, 74, 74 | **must start at 0** | Bars again — and exactly the one people truncate, because the values are close |
| f | line of runs per over | **must start at 0** *(arguably)* | Strictly a line need not, but zero runs in an over is a real and common thing, so starting at zero is the honest choice |

- **A3(g).** A bar asks your eye to compare **lengths**, and deleted length cannot be put back; a line asks you to follow a **shape**, and a shape survives a moved floor.
- **A3(h).** **Say so, loudly, in the label** — e.g. `"Temperature (°C) — note: axis starts at 35"`. Hiding it is the dishonest part; the choosing can be perfectly defensible.
- *(teacher-only)* Row f is the one to accept either way if the reason given is sound; row d is the one to push on.

**A4.**

| # | The line | The fix |
|---|---|---|
| a | `axes.bar(...)` | `axes[0].bar(...)` — say which frame |
| b | `axes[2]` | `axes[1]` — two frames, numbered 0 and 1 |
| c | `ax.set_ylim(48.6)` | `ax.set_ylim(48.6, 51.4)` — **two** numbers |
| d | `ax.set_ylim(51.4, 48.6)` | Smaller first: `ax.set_ylim(48.6, 51.4)` |
| e | `df["club"].corr(df["score"])` | Correlation needs two **number** columns |
| f | `df["hours"].corr()` | `df["hours"].corr(df["score"])` — it takes two |
| g | `ax.legend()` with no labels | Add `label="..."` to each `plot` call |
| h | bar chart with no `set_ylim` | `ax.set_ylim(0, 100)`. matplotlib will start at zero here anyway, **but write it so the decision is visible in your own file** |

- **A4(i).** **c, d, g and h** produce no error. c silently invents a top; d silently draws the chart upside down; g gives a *warning* and saves a legend-less chart; h is a perfectly good chart that nobody decided (as a line it would have been truncated for you). a, b, e and f all raise real tracebacks.
- **A4(j).** **"Is that the chart I meant to make?"** Open the PNG and look. The terminal has nothing useful to say about any of the four.

**A5.**

| Box | Phrase |
|---|---|
| **A** | the floor of the axis, set by `set_ylim` |
| **B** | the 48.6 units deleted from both bars |
| **C** | 7A's visible bar, 0.4 units |
| **D** | 7B's visible bar, 2.4 units |
| **E** | the two ratios, and the factor between them |

- **A5(f).** D ÷ C = 2.4 ÷ 0.4 = **6.00**.  51 ÷ 49 = **1.0408**.  Factor = 6.00 ÷ 1.0408 = **5.76**.
- **A5(g).** **`ax.set_ylim(48.6, 51.4)`** — one line (one argument, really: the 48.6).

**A6.**

- **Which line first?** The **last** one, always.
- **`'numpy.ndarray'`** is numpy's word for a box of things — a row of slots you index with a number (Week 17). Here the slots hold drawing frames.
- **In their own words:** "The thing I called `axes` is a box of frames, not a frame, and a box has no `bar` method. Which frame did I mean?"
- **Should you use `var`?** **No.** `var` is a numpy function about **variance**, nothing to do with drawing a bar. Python matched the **letters** (`bar` / `var` differ by one), not the meaning.
- **The rule:** Python's "Did you mean…?" suggestions are hints, not answers. Read them, then decide.

### ✍️ Practice Set B

**B1.**

```python
print(round(df["hours"].corr(df["score"]), 3))
```

```text
0.925
```

What it is **not**: a percentage. It does not mean "92.5% of the score comes from studying"; it is a position on a scale from −1 through 0 to +1.

**B2.**

```python
"""b2.py - one truncated bar chart, and the arithmetic that convicts it."""

import matplotlib.pyplot as plt

teams = ["Falcons", "Kites"]
wins = [11, 12]                          # matches won. Both TRUE.
bottom, top = 10.8, 12.2                 # the dishonest floor

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(teams, wins)
ax.set_ylim(bottom, top)
ax.set_title("LIE: the Kites look unbeatable")
ax.set_xlabel("Team")
ax.set_ylabel("Matches won (count)")
fig.savefig("teams_lie.png", dpi=120, bbox_inches="tight")
print("saved teams_lie.png")

looks = (wins[1] - bottom) / (wins[0] - bottom)
honest = wins[1] / wins[0]
print(f"visible bars      : {wins[0] - bottom:.1f} and {wins[1] - bottom:.1f} units")
print(f"looks-like ratio  : {looks:.2f} times taller")
print(f"honest ratio      : {honest:.4f} times taller")
print(f"exaggeration factor: {looks / honest:.2f}")
```

```text
saved teams_lie.png
visible bars      : 0.2 and 1.2 units
looks-like ratio  : 6.00 times taller
honest ratio      : 1.0909 times taller
exaggeration factor: 5.50
```

- **Why the floor is a named variable:** the arithmetic uses it three lines later; typed in two places, one will eventually change without the other and the printed factor becomes a lie about your own lie.
- **The factor is 5.50, not 6.00:** the eye sees 6×, but the honest ratio is already 1.09 (11 and 12 are a bit further apart than 49 and 51). The exaggeration factor divides out the real difference, which is what makes it the honest measure.

**B3.**

```python
"""b3.py - the lie and the fix, side by side."""

import matplotlib.pyplot as plt

teams = ["Falcons", "Kites"]
wins = [11, 12]
bottom, top = 10.8, 12.2

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
print("how many frames?", len(axes))

axes[0].bar(teams, wins)
axes[0].set_ylim(bottom, top)
axes[0].set_title(f"LIE: y-axis starts at {bottom}")
axes[0].set_xlabel("Team")
axes[0].set_ylabel("Matches won (count)")

axes[1].bar(teams, wins)
axes[1].set_ylim(0, 14)
axes[1].set_title("HONEST: y-axis starts at 0")
axes[1].set_xlabel("Team")
axes[1].set_ylabel("Matches won (count)")

fig.suptitle("The same two numbers: 11 wins and 12 wins")
fig.savefig("teams_lie_and_fix.png", dpi=120, bbox_inches="tight")
print("saved teams_lie_and_fix.png")
```

```text
how many frames? 2
saved teams_lie_and_fix.png
```

The f-string in the left title means the title cannot drift out of step with the floor — change `bottom` and the title fixes itself.

**B4.**

```python
"""b4.py - two series on one frame, with a legend and two marker shapes."""

import matplotlib.pyplot as plt
from myweek import build_my_week

df = build_my_week()

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(df["day"], df["homework_min"], marker="o", label="Homework")
ax.plot(df["day"], df["screen_min"], marker="s", label="Screen time")

ax.set_title("Screen time beat homework on 5 of the 10 days")
ax.set_xlabel("Day of the fortnight (day 1 = first Monday)")
ax.set_ylabel("Minutes")
ax.set_ylim(0, 200)
ax.legend()

fig.savefig("my_two_lines.png", dpi=120, bbox_inches="tight")
print("saved my_two_lines.png")

crossings = [df["day"][i] for i in range(len(df))
             if df["screen_min"][i] > df["homework_min"][i]]
print("days screen time was higher:", crossings)
```

```text
saved my_two_lines.png
days screen time was higher: [1, 3, 5, 6, 10]
```

Five days out of ten, so the title says "5 of the 10 days" — a checkable number. Write the title after you have printed the fact. The two markers `"o"` and `"s"` survive a black-and-white photocopy: two cues for free. *(The days list depends on the student's own Week 21 table; this is the model table's answer, so check the title against what **their** program prints.)*

**B5.** The full model answer, which is also the model for Build It Parts 1–3:


```python
# story_lie.py -- sabotage chart 3, then repair it, side by side.
import matplotlib.pyplot as plt
from students import build_students

df = build_students()
means = df.groupby("club")["score"].mean().sort_values(ascending=False)
print(means.round(2))

bottom = 66                                  # the dishonest floor I picked on purpose

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].bar(means.index, means.values)
axes[0].set_ylim(bottom, 78)
axes[0].set_title("LIE: axis from 66, no units on y")
axes[0].set_xlabel("Club")
axes[0].set_ylabel("Score")                  # second trick: no units

axes[1].bar(means.index, means.values)
axes[1].set_ylim(0, 100)
axes[1].set_title("HONEST: axis from 0, units stated")
axes[1].set_xlabel("Club")
axes[1].set_ylabel("Mean score (points out of 100)")

fig.suptitle("The same three club averages, drawn two ways")
fig.savefig("story_lie_and_fix.png", dpi=120, bbox_inches="tight")
print("saved story_lie_and_fix.png")

chess, art = means["chess"], means["art"]
honest = chess / art
looks = (chess - bottom) / (art - bottom)
print(f"chess = {chess:.2f}, art = {art:.2f}, real gap = {chess - art:.2f} points")
print(f"honest ratio chess/art     = {honest:.2f} times taller")
print(f"truncated ratio chess/art  = {looks:.2f} times taller")
print(f"exaggeration factor        = {looks / honest:.2f}")

axes_height_inches = axes[0].get_position().height * fig.get_figheight()
mm_per_point = axes_height_inches * 25.4 / (78 - bottom)
print(f"lie panel: {mm_per_point:.1f} mm per point")
print(f"  art bar   should measure {(art - bottom) * mm_per_point:.0f} mm")
print(f"  chess bar should measure {(chess - bottom) * mm_per_point:.0f} mm")
```

```text
club
chess    76.07
music    71.83
art      67.83
Name: score, dtype: float64
saved story_lie_and_fix.png
chess = 76.07, art = 67.83, real gap = 8.24 points
honest ratio chess/art     = 1.12 times taller
truncated ratio chess/art  = 5.49 times taller
exaggeration factor        = 4.90
lie panel: 6.5 mm per point
  art bar   should measure 12 mm
  chess bar should measure 66 mm
```

**Which of the two tricks is worse?** The **truncated axis**, because it works on the reader **before** they read anything — the shape lands in about a quarter of a second and the labels take two or three. The missing units are worse in a different way: they remove the reader's ability to **check**. The two together are much worse than either alone, because the first misleads and the second disarms.

### 🐞 Fix the Broken Program

**Bug 1 — the syntax error.**

- **Did any of it run?** **No.** Two tells, each a second's work: there is no `Traceback`, and `print(means.round(2))` on line 7 produced nothing. Python never started; it could not finish reading the file.
- **Where is the fix?** On **line 15**, the line Python points at — add the missing `)`:

```python
axes[0].set_ylabel("Mean score (points out of 100)")
```

- **Why not reported sooner?** An open bracket is a perfectly legal way to **continue onto the next line** (the twelve library visits split across two lines in Week 25), so Python keeps reading, hoping for a `)`, until it runs out of file. It then reports the place where the bracket was **opened**, the last spot it was certain about.

**Bug 2 — the runtime error.**

- `subplots(1, 2)` makes two frames, numbered 0 and 1. There is no frame 2.
- **Which week?** **Week 11** — slots start at 0, so the last slot of a two-slot thing is number 1. (And `axis 0 with size 2` is Week 17's language for "the first direction has two slots in it".)
- **The fix — five lines**, every `axes[2]` becoming `axes[1]` (the `bar`, `set_ylim`, `set_title`, `set_xlabel` and `set_ylabel`). "Change every `axes[2]` to `axes[1]`" is full marks:

```python
axes[1].bar(means.index, means.values)
axes[1].set_ylim(100, 0)
axes[1].set_title("HONEST: axis starts at 0")
axes[1].set_xlabel("House")
axes[1].set_ylabel("Mean score (points out of 100)")
```

**Bug 3 — the silent one.**

```text
panel 1 ylim: (100.0, 0.0)
```

- **Right-hand panel:** drawn **upside down**, with the three bars hanging down from the top of the frame and 100 at the bottom of the axis.
- **Cause:** `axes[1].set_ylim(100, 0)` — the two numbers the wrong way round. `set_ylim` takes bottom first, then top, and does exactly what it is told. No error, no warning, and a PNG that looks like a matplotlib bug.
- **The fix:**

```python
axes[1].set_ylim(0, 100)
```

- **The check that catches this family:** open the PNG and ask "is that the chart I meant?" All three of this week's silent bugs (one-argument ylim, backwards ylim, a bar chart nobody set a floor on) are invisible in the terminal and obvious in the picture.

**The left panel's exaggeration factor** (chess 76.07, art 67.83, floor 67):

- Visible bars: 67.83 − 67 = **0.83** and 76.07 − 67 = **9.07**
- The eye sees: 9.07 ÷ 0.83 = **10.93**
- Honest: 76.07 ÷ 67.83 = **1.1215**
- Factor: 10.93 ÷ 1.1215 = **9.74**

Nearly ten times: an 8-point gap out of 100 drawn as a bar nearly eleven times taller. Accept anything from 9.7 to 9.8. *(teacher-only: working from the unrounded means, 76.0714 and 67.8333, gives 10.89 and 9.71, which is inside the accepted range; the difference is only where the rounding happens.)*

### 🧩 Puzzle of the Week

**Part 1 — Solve for the lie**

**(a)** (51 − b) ÷ (49 − b) = F

**(b)** The working:

```text
51 - b = F(49 - b)
51 - b = 49F - Fb
51 - b + Fb = 49F
51 + b(F - 1) = 49F
b(F - 1) = 49F - 51
b = (49F - 51) / (F - 1)
```

Equivalently `b = (51 - 49F) / (1 - F)` — the same expression with top and bottom negated.

**(c)** Real output:

```text
F =    2  ->  bottom = 47.0000   check: 2.00
F =    3  ->  bottom = 48.0000   check: 3.00
F =    6  ->  bottom = 48.6000   check: 6.00
F =   20  ->  bottom = 48.8947   check: 20.00
F =   50  ->  bottom = 48.9592   check: 50.00
F =  100  ->  bottom = 48.9798   check: 100.00
```

F = 3 giving exactly 48 is a satisfying check that the algebra is right: 3 ÷ 1 = 3.

**(d)** With `b = 48.9592`, the visible bars are 51 − 48.9592 = **2.0408** and 49 − 48.9592 = **0.0408**, and 2.0408 ÷ 0.0408 = **50.02**. **Yes, it matches** — the 0.02 is rounding in the four decimal places.

**(e)** Rounded to **48.96**: the visible bars become 2.04 and 0.04, and 2.04 ÷ 0.04 = **51.00**.

**(f)** **Brutally sensitive.** Changing the floor by less than a thousandth of a percentage point (0.0008) changed the lie from 50× to 51×. As the floor creeps towards the smaller bar, the smaller *visible* bar heads towards zero and dividing by something near zero magnifies every tiny change. A number like 48.96 was not derived; it was nudged.

**Part 2 — Spot the floor**

- **(g)** Look for the **y-axis tick numbers**. There are none, so you cannot compute anything, so the chart is unfalsifiable. Suspect the worst: no numbers is a stronger warning sign than a bad floor, because a bad floor can at least be measured.
- **(h)** Look at the **bottom tick number** — 95% of the maximum. Suspect a truncated line chart designed to make an ordinary month look like a crisis or boom. A line, so truncation is not automatically dishonest, but a share price or income has a meaningful zero and the reader is invited to read length rather than shape, and nothing on the chart says the axis was cut.
- **(i)** Bottom tick 60%. **Probably fine**: a line, you are following a shape over the day, and a battery does not normally go near zero. But it should say so, and almost never does.
- **(j)** Axis 0 to 100, numbers printed. **Nothing is wrong with the framing.**
- **(k)** **(j) is the fine one.** Things that could *still* be wrong with it: which three schools were chosen and which left out; how many students each pass rate came from (95% of 20 and 95% of 2,000 are not the same evidence); whether "pass rate" is the right question (a school can raise it by entering fewer students); whether the intakes are comparable. **A correct axis is necessary and not sufficient.**

### 🤔 Think Deeper

**T1.** Model answer:

> *The ice-cream number is biggest because ice cream and drowning are both almost perfectly driven by the same third thing, and a correlation measures how tightly two columns move together **regardless of why**. Hot weather pushes both up in lockstep, and in this made-up table the two happen to track each other even more tightly than either one tracks the temperature (0.997 against 0.987 and 0.989). That is a quirk of these six invented rows: with real, noisier data, two things driven by a third usually track each other *less* tightly than each tracks the third, so you cannot rely on the ice-cream number being the biggest. Either way, strength is not evidence of direction at all: the strongest of my three numbers is the one that is nonsense.*
>
> *The school data makes it worse. Sleep and marks are 0.994; screens and marks are −0.997; and sleep and screens are −0.987 with **each other**. The two candidate causes are so tangled that the students who sleep a lot are exactly the students who use screens a little. Correlation can tell me that all three move together and nothing whatsoever about which one is doing the work — because there is no arrangement of these three numbers that could distinguish "screens ruin sleep which ruins marks" from "a strict bedtime causes both" from "a quiet, organised home causes all three".*
>
> *The one thing that would settle it is an **experiment**: take a large group and split it **randomly** into two halves, change one thing for one half — say, no screens after nine o'clock — leave the other half alone, and compare the marks afterwards. The word "randomly" is doing all the work. It is what makes the two halves similar in every single thing I did not measure and did not think of, including the quiet house. Without randomness, whatever I find could just be the confounder again.*

**Marking note:** full marks needs (1) why the strongest is the absurd one, (2) the tangling point about the school data, and (3) the word "randomly" explained rather than just used.

**T2.** Model answer:

> *At the bottom of that scatter are five real people: Hugo (14), Omar (14), Sami (14), Bruno (13) and Greta (14). Four of the five are fourteen.*
>
> *Three reasons a fourteen-year-old might study half an hour a week. **A part-time job** — "study two more hours" means either lose the money or lose the sleep, so it punishes. **A younger sibling to look after after school** — the two hours do not exist to be reallocated, so it punishes. **No quiet room or desk at home** — the two hours exist but are not usable, so ordering them produces two hours of failing to study, plus a detention when it does not work. **None of the three is helped. All three are punished.***
>
> *And the uncomfortable part is that nobody did anything obviously wrong. The chart was correct. r = 0.925 is real. The head teacher acted in good faith on the best evidence available. What went wrong is the step nobody wrote down: between "hours and marks move together" and "make everybody do more hours" there is a hidden assumption that **hours are a thing every student can freely choose**, and for the five students at the bottom that assumption is false — and the chart never measured it, so nobody had to defend it.*
>
> *One sentence under the chart would have stopped it: **"Every student in the bottom five is 13 or 14, and this chart does not measure whether they are able to study more."** That sentence does not argue with the correlation. It just makes the missing thing visible, which is enough.*

**Marking note:** full marks needs three **specific** reasons with "helps or punishes" answered for each, **and** a named location for the failure — the unwritten assumption, not the arithmetic.

*(teacher-only)* The five names and ages come from the Activity Part C listing (`week27_who.py`):


```python
# week27_who.py -- who is at the bottom of the scatter?
from students import build_students

df = build_students()

print("studying an hour or less:")
print(df[df["hours"] <= 1.0][["name", "age", "house", "club", "hours", "score"]].to_string(index=False))
print()
print("studying five hours or more:")
print(df[df["hours"] >= 5.0][["name", "age", "club", "hours", "score"]].to_string(index=False))
```

```text
studying an hour or less:
       name  age house  club  hours  score
 Hugo Silva   14   Red music    0.5     45
Omar Haddad   14  Blue music    1.0     52
  Sami Aden   14 Green   art    0.5     48
Bruno Costa   13 Green   art    1.0     50
 Greta Hahn   14  Blue music    0.5     42

studying five hours or more:
       name  age  club  hours  score
   Bela Roy   14 music    5.0     90
 Farah Aziz   12 chess    6.0     95
 Liam Byrne   13 music    5.5     81
 Tara Joshi   12 chess    5.0     97
Anika Verma   12 music    5.0     93
  Hana Sato   12   art    5.5     91
```

### 🛠️ Build It

**Part 1 — Sabotage one of your own charts.** The checklist is a self-check; the table is filled from the student's own program. If they used the club averages, as in B5, it reads: bigger real number **76.07** (chess), smaller **67.83** (art), real gap **8.24**, dishonest floor **66**. If they used the house means, the real numbers are Blue 74.36, Red 74.25 and Green 67.42 (the Fix the Broken Program listing), and whichever floor they picked is right if the program uses it. Check that the floor was named in a variable and that the left panel really has **two** tricks (truncated axis, units removed).

**Part 2 — The arithmetic, and then the ruler.** With the club model, the program column is: visible bars **1.83 and 10.07 units** (67.83 − 66 and 76.07 − 66), ratio **5.49**, honest ratio **1.12**, exaggeration factor **4.90**; the ruler column should read about 12 mm and 66 mm (ratio 5.5). The honest panel's ratio should come out close to the honest ratio, about 1.1, whatever the raw millimetres. Any printer scale is fine as long as the two ruler readings have the right ratio.

**Three real reasons your ruler and your program disagree slightly:**

1. **The ruler is only good to about half a millimetre**, and you are reading two of them, so the ratio carries two readings' worth of error.
2. **Your printer may have scaled the page.** Both bars shrink together so the *ratio* survives, but the raw millimetres will not match the prediction.
3. **The bar tops are drawn with a line that has its own thickness**, so "where the bar ends" is a decision of about half a millimetre, twice.

**Measured 5.5 against computed 5.49 is agreement, not disagreement.** Being able to say why two nearly-identical numbers are not identical is worth more than getting them to match.

**Part 3 — The written confession.** Full marks needs five things: both real numbers, the real gap, the honest ratio, the truncated ratio, and the fact that no number changed. A full-credit example, using the club averages:

> Chess averages 76.07 and art averages 67.83 — a real gap of **8.24 points**, which makes chess about 12% higher. Drawn honestly from zero, the chess bar is **1.12×** the art bar: visible, modest, and about right. Truncating the axis at 66 makes the chess bar **5.49×** the art bar, an exaggeration of roughly **4.9×**. I measured them on the printout: 12 mm and 66 mm, and 66 ÷ 12 = 5.5, which matches. I also used a second trick — I removed the units from the y-axis label, so it just says "Score". Without "out of 100" the reader cannot tell whether 8 points is a landslide or a rounding error. **Neither trick changed a single number.**

**"You used two tricks. Which is worse, and why?"** The truncated axis works on the reader before they read anything; the missing units remove the reader's ability to check; together they are much worse than either alone (the same answer as B5).

**Part 4 — The Five-Chart Data Story.** The model version answers *which club should the school buy equipment for next year?* — with the decision named up front (there is money for exactly one club), because a question with no decision behind it produces charts with no point. **The story order is what is being marked:** context → baseline → the main finding → a challenge to the finding → the caveat. A story that shows only the flattering charts is an advertisement, not an analysis.


```python
# story.py -- the Five-Chart Data Story.
# QUESTION: which club should the school buy equipment for next year?
# DECISION: there is money for exactly one club.
import matplotlib.pyplot as plt
from students import build_students

df = build_students()

def chart1_club_sizes():
    """CONTEXT -- how many people would each choice affect?"""
    counts = df["club"].value_counts()
    print("1)", list(counts.index), list(counts.values))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(counts.index, counts.values)
    ax.set_ylim(0, 16)
    ax.set_title("Chess is the biggest club: 14 of 38 students")
    ax.set_xlabel("Club")
    ax.set_ylabel("Number of students (count)")
    fig.savefig("story_1_sizes.png", dpi=120, bbox_inches="tight")
    plt.close(fig)

def chart2_all_scores():
    """BASELINE -- what does the whole school look like before we split it up?"""
    print("2) mean", round(df["score"].mean(), 1), "median", df["score"].median())
    fig, ax = plt.subplots(figsize=(6, 4))
    counts, edges, bars = ax.hist(df["score"], bins=8, edgecolor="white")
    print("   counts", counts)
    ax.set_title("Scores run from 42 to 97 with no single peak")
    ax.set_xlabel("Score (points out of 100)")
    ax.set_ylabel("Number of students (count)")
    fig.savefig("story_2_all_scores.png", dpi=120, bbox_inches="tight")
    plt.close(fig)

def chart3_score_by_club():
    """THE FINDING -- the chart the argument rests on."""
    means = df.groupby("club")["score"].mean().sort_values(ascending=False)
    print("3)", means.round(2).to_dict())
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(means.index, means.values)
    ax.set_ylim(0, 100)
    ax.set_title("Chess averages 76, art averages 68 -- an 8-point gap")
    ax.set_xlabel("Club")
    ax.set_ylabel("Mean score (points out of 100)")
    fig.savefig("story_3_score_by_club.png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    return means

def chart4_hours_vs_score():
    """THE CHALLENGE -- maybe it is not the club at all."""
    r = df["hours"].corr(df["score"])
    print("4) r =", round(r, 3))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(df["hours"], df["score"])
    ax.set_title(f"Hours studied tracks score closely (r = {r:.2f})")
    ax.set_xlabel("Study hours per week")
    ax.set_ylabel("Score (points out of 100)")
    fig.savefig("story_4_hours_vs_score.png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    return r

def chart5_hours_by_club():
    """THE CAVEAT -- the thing that might be doing the real work."""
    means = df.groupby("club")["hours"].mean().sort_values(ascending=False)
    print("5)", means.round(2).to_dict())
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(means.index, means.values)
    ax.set_ylim(0, 6)
    ax.set_title("Chess students also study the most hours")
    ax.set_xlabel("Club")
    ax.set_ylabel("Mean study hours per week")
    fig.savefig("story_5_hours_by_club.png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    return means

chart1_club_sizes()
chart2_all_scores()
score_means = chart3_score_by_club()
r = chart4_hours_vs_score()
hours_means = chart5_hours_by_club()
print()
print(df.groupby("club")["score"].agg(["count", "mean", "min", "max"]).round(2))
```

```text
1) ['chess', 'music', 'art'] [14, 12, 12]
2) mean 72.1 median 72.5
   counts [3. 4. 4. 5. 6. 5. 6. 5.]
3) {'chess': 76.07, 'music': 71.83, 'art': 67.83}
4) r = 0.925
5) {'chess': 3.39, 'music': 3.17, 'art': 2.54}

       count   mean  min  max
club                         
art       12  67.83   48   91
chess     14  76.07   55   97
music     12  71.83   42   93
```

> **💡 Try this:** `plt.close(fig)` at the end of each function throws the finished figure away once it is saved. You do not need it for five charts, but if you ever loop over fifty, matplotlib will warn you that too many figures are open. One line, and now you know what it is for.

**The five captions, which must read as one paragraph on their own:**

1. Chess is the biggest club, with 14 of our 38 students, so it affects the most people.
2. Across the whole school scores run from 42 to 97 with no single peak, so there is no "normal" student to compare a club against.
3. Chess averages 76.1 and art averages 67.8 — an 8-point gap, which is real but modest.
4. Study hours track scores very closely (r = 0.93), so the club gap might not be about the club at all.
5. Chess students also study the most hours on average (3.4 against art's 2.5), which means the two explanations are tangled and this data cannot separate them.

Read together: *Chess is the biggest club. There is no normal student. Chess scores about 8 points higher than art. But hours track scores closely. And chess students also study the most, so we cannot tell which is doing the work.* That is a paragraph, and it is honest.

**The verdict, three to five sentences, including one honest uncertainty:**

> On this data I would spend the money on **chess**, mainly because it affects 14 students rather than 12, and its 8-point score advantage is at least consistent with the club being good for people. **I am not confident that the club is causing the higher scores**, because chess students also study 0.85 hours a week more than art students on average, and study hours correlate with score at 0.93 — so the club may simply be where the students who already study a lot happen to go. All three clubs have fewer than 15 members, which is far too few to be sure of anything. If I could collect one more thing it would be scores from *before* students joined a club, because that would let me look at the change rather than the level.

- **Why is chart 5 (or 4) in the story when it weakens the argument?** Because leaving it out would make the story an advertisement. Anybody who later found chart 5 would stop believing chart 3 as well. **Showing the caveat yourself is what makes the rest credible.**
- *(teacher-only)* **Which of your five charts would you sabotage most easily?** Chart 3, the club means, by truncating its axis to `set_ylim(66, 78)` — that is exactly the left panel of B5. It is the easiest because the three values are close together, and truncation is most powerful exactly when the real difference is smallest.
- *(teacher-only)* **Every bar chart here has `set_ylim(0, ...)`. Why, when matplotlib would have picked something?** Because once you touch `set_ylim` at all you own the decision, and writing the zero makes it visible in your file. (For bar values of 76.07, 71.83 and 67.83 matplotlib would start at zero by itself; it is **line** charts it zooms in on. Typing the zero means the choice does not depend on the tool's default or on which chart type you later switch to.)
- **Checklist items** (five PNGs with five different filenames, bar charts with `set_ylim(0, ...)`, titles that state a finding): check against the file listing and the five `set_ylim` lines.

**Part 5 — The honest sentence about `r`.** Full credit needs four things: the description, the refusal, a named alternative cause, and who it lands on. The blanks are the student's own pair of columns; for the model table they are `hours` and `score`, r = 0.925 (0.93). A model answer:

> In this table, students who studied more hours tended to score higher (r = 0.93). I do **not** know whether studying caused the higher marks. A quiet room with a desk could be causing both — it would give somebody more hours *and* better conditions to learn in — and if the school acts on this chart by making everybody do two extra hours, the five students at the bottom get blamed for something the chart never measured. Four of those five are fourteen, and I do not know why they study so little.

**Marking note:** the single thing to check is that **no word means "caused"**, except inside a sentence explicitly denying it. Words to strike out: *causes, makes, leads to, improves, boosts, results in, so you should*. The "how many did you find?" count can be zero; what matters is that the rewritten sentence has none.

**Part 6 — Term 3 reflection.** For each week: **✓** I could teach this to somebody else · **?** I want to look at this again. The "check yourself" answers:


| Week | The one thing it was about | Check yourself with this |
|---|---|---|
| 19 | `axis=0` goes down the columns, `axis=1` goes across the rows | Without running it: for a 3×4 grid, what shape does `arr.mean(axis=0)` come back as? *(4 numbers — one per column.)* |
| 20 | A boolean mask is a yes/no array you use to pull out values | What does `arr[arr > 50]` give you — the values, or where they are? *(The values.)* |
| 21 | A DataFrame is a table whose columns have names | What are the two things `df.info()` tells you that `df.head()` does not? *(How many non-missing values per column, and each column's type.)* |
| 22 | `loc` picks by name, `iloc` picks by position | On a table indexed 10, 11, 12, what does `df.loc[10]` give, and what does `df.iloc[10]`? *(Row named 10; and an `IndexError`, because there is no eleventh row.)* |
| 23 | Real data arrives broken in four predictable ways | Name the two calls you use for holes, and the one for text-that-should-be-numbers. *(`isna`, `fillna`; `astype`.)* |
| 24 | `groupby` answers "what's the average per group?" and hides the row counts | What must you always print alongside a `groupby` mean? *(The count.)* |
| 25 | The labels are what turn a chart into evidence | Which four of a chart's five parts are words you type? *(Title, x label, y label, and the marks via `plot`.)* |
| 26 | The question picks the chart shape | Gaps between the bars: bar chart or histogram? *(Bar chart.)* |

**Then, in writing: name two weeks you want to revisit, with a reason that is specific.**

Model answers, to show what "specific" means:

- *"Week 22. I still can't tell `loc` from `iloc` the moment the index isn't 0, 1, 2 — I get it right by luck."*
- *"Week 19. I can type `axis=0` but I work out which one it is by trying both and seeing which shape comes back, and that means I don't actually know."*

**Marking note:** *"it was hard"* and *"all fine"* are both non-answers. Everybody has two. Require two.

**Part 7 — The Bug Log.** No fixed answer. A good entry names a real error from this term and the check that would have caught it, e.g. *"IndexError on `axes[2]` — yes, there was an error message — changed it to `axes[1]` — next time: count the frames, then number from 0"*, or *"the chart was upside down — no error message — put the ylim numbers the right way round — next time: open the PNG"*. An entry whose "what I will check next time" is just "be careful" is not yet an answer.

### 🎨 Draw It

There is no single right drawing. A good one has **two panels whose bars genuinely look different**, a floor box with a number that was *nudged* rather than derived, and an exaggeration factor computed from the **measured bars** rather than from the original two numbers.

The tell that it is right: the third bottom box (tall ÷ short) is a big number like 12, and the fourth box (the factor) is that number divided by something close to 1. If the two bottom-right boxes are nearly the same, the truncation was written down but never drawn. *(The workbook's own example — Shop A 28 minutes, Shop B 27 minutes, floor 26.8 — has bottom boxes 4 mm · 48 mm · 12 · 11.5×.)*

### 📊 Self-Check

The "I can…" table is a self-rating, nothing to mark. The true-or-false rows:

| Statement | Answer | Why |
|---|---|---|
| A bar chart's y axis must start at zero | **TRUE** | The eye compares lengths, and deleted length cannot be put back |
| A line chart's y axis must start at zero | **FALSE** | A line asks you to follow a shape. But **say so in the label** if you truncate |
| `ax.set_ylim(48.6)` raises an error | **FALSE** | No error. It sets the bottom and invents a top |
| `ax.set_ylim(51.4, 48.6)` raises an error | **FALSE** | No error. It draws the chart upside down |
| `subplots(1, 2)` gives you `axes[1]` and `axes[2]` | **FALSE** | `axes[0]` and `axes[1]`. Week 11's off-by-one |
| `ax.legend()` invents names for your lines | **FALSE** | It reads the `label=` you already gave. With none, you get a warning and no legend |
| `r = 0.93` means 93% | **FALSE** | It is a position on a scale from −1 to +1 |
| A negative `r` is a weak `r` | **FALSE** | The minus sign is a **direction**. −0.9 is stronger than +0.3 |
| `df["club"].corr(df["score"])` works fine | **FALSE** | `TypeError: unsupported operand type(s) for /: 'str' and 'int'`. You cannot average "chess" |
| The strongest of three correlations is the most likely to be causal | **FALSE** | In the seaside table the strongest, 0.997, is the absurd one |
| Printing the real numbers on a truncated chart makes it honest | **FALSE** | Better, and not enough. The shape lands in a quarter of a second; the numbers take three |
| Python's "Did you mean…?" suggestions are always right | **FALSE** | It offered `var` for `bar`. It matched the letters, not the meaning |
| A confounder is a hidden third thing causing both of the things you measured | **TRUE** | Hot weather, behind ice cream and drowning |
| Every chart is a lie | **FALSE** | Look at the honest panel: same two numbers, axis from zero, ratio 1.04. **A chart is an argument, so check the framing** |

### Prompts used in the lesson (not on a workbook section)

The hook and the Activity ask a few questions that have no line in the workbook. They are answered here so you can mark the conversation. Students write their hook numbers on scrap paper or beside Practice Set A, question A1.

**Hook — the measuring of the printed `lie.png`**

| # | Measurement | Answer |
|---|---|---|
| (a) | 7A's bar, in mm | **about 11 mm** (9–14 depending on printer scaling) |
| (b) | 7B's bar, in mm | **about 67 mm** (54–85, scaled the same way) |
| (c) | (b) ÷ (a) | **about 6.1** — this is what the chart makes you believe |
| (d) | 7A's real value | **49%** |
| (e) | 7B's real value | **51%** |
| (f) | (e) ÷ (d) | 51 ÷ 49 = **1.0408** — 7B is about 4% better |
| (g) | Exaggeration factor, (c) ÷ (f) | 6.1 ÷ 1.04 = **about 5.8 to 5.9** (the exact figure with a 48.6 floor is 5.76) |

- **Which number on the chart was faked?** **None of them.** Both bar heights are the true values and the tick numbers are correct. Only where the axis starts changed.
- **If your millimetre readings were different from 11 and 67, were you wrong?** No. Your printer scaled the page, so **both** bars shrank or grew by the same amount and the ratio is unaffected. That is why the ratio is the answer and not the raw millimetres.

**Activity Part A — two lines, one legend** (full file and output in The Activity, Part A; `saved two_lines.png`; the student-facing versions are Predict the Output P3 and Practice Set A, A2 and A4)

- **What happens if you call `ax.legend()` but never pass any `label=`?** A **warning**, not an error, and the chart still saves with no legend on it (the exact message is in P3 above).
- **Why does one line use `marker="o"` and the other `marker="s"`?** So the two lines can be told apart when the colour is gone — photocopied, printed in black and white, or read by somebody who cannot distinguish those two colours. **Two cues instead of one**, and it costs nothing.
- **When do you NOT need a legend?** When there is exactly one series, because the title and the y-axis label already name it.

**Activity Part B — correlation** (full file and output in The Activity, Part B; the student-facing versions are Predict the Output P4 and Practice Set B, B1)

| Pair | `r` |
|---|---|
| study hours vs score | **0.925** |
| age vs study hours | **−0.572** |
| ice creams vs drownings | **0.997** |
| temperature vs ice creams | **0.987** |
| temperature vs drownings | **0.989** |

- **Which of the five is the strongest, and which is the most ridiculous?** The same one: **ice creams vs drownings, 0.997.** Strength tells you nothing about whether there is a cause.
- **What is the confounder in the ice-cream case, and how do you know?** **Temperature.** The numbers alone cannot prove it (a correlation never says which way an arrow points). It is consistent with them, since temperature correlates strongly with *both* other columns (0.987 and 0.989), and what makes it convincing is a mechanism you can say out loud: hot weather makes people buy ice cream, and makes people swim, and swimming is what creates the drowning risk.
- **What does the minus sign in −0.572 mean?** That the two move in **opposite** directions: as age goes up, reported study hours go down. It is a direction, not a grade. −0.9 is *stronger* than +0.3.
- **Why does `df["club"].corr(df["score"])` fail?** Correlation is arithmetic and you cannot do arithmetic on the word "chess". The last line is `TypeError: unsupported operand type(s) for /: 'str' and 'int'`. *(pandas 2.x says `ValueError: could not convert string to float: 'chess'` instead. Same cause.)*

**Activity Part C — who gets hurt?** (the student-facing versions are Think Deeper T2 and Build It Part 5; the listing is reproduced under T2 above)

- **What do the five students at the bottom have in common?** Every one of them is **13 or 14** — four are 14. Four of the six at the top are **12**. So "hours" and "age" are tangled together in this table, and the hours-vs-score chart never mentions age.
- **Give three reasons a 14-year-old might study half an hour a week that the chart cannot see.** A part-time job. A younger sibling to look after. No quiet room or desk at home. A long journey to and from school. Illness, their own or somebody else's. Something difficult going on at home. **None of them appear in the table, and none are fixed by being told to study more.**
- **The honest sentence about `r = 0.93`:** the model answer is the one under Build It Part 5, with the same marking note.
- **What would you need in order to actually test whether studying raises marks?** An **experiment**: split a large group **randomly** in half, ask one half to study two extra hours, leave the other alone, and compare afterwards. The randomness makes the two halves similar in everything you did not measure, including the quiet room. Running that on real children raises fairness questions of its own, which is why this is genuinely hard.


### Lesson questions posed in the Say-this scripts

- *"Measure both bars in millimetres."* → About 11 mm and 67 mm, depending on printer scaling.
- *"Divide the big one by the small one."* → About 6.1.
- *"How much better is 7B, really?"* → Two percentage points; 51 ÷ 49 = 1.04, so about 4% taller.
- *"Which number did I fake?"* → None. Every number on the chart is true.
- *"So how did I do it?"* → Moved the bottom of the y axis from 0 to 48.6.
- *"Where did the six come from, in arithmetic?"* → (51 − 48.6) ÷ (49 − 48.6) = 2.4 ÷ 0.4 = 6.
- *"Why is this worse for bars than for lines?"* → A bar asks the eye to compare lengths; a line asks it to follow a shape. Deleted length cannot be recovered; a shape survives.
- *"What ylim would make it look twenty times bigger?"* → About 48.9: (51 − 48.9) ÷ (49 − 48.9) = 2.1 ÷ 0.1 = 21.
- *"Is a truncated line chart always dishonest?"* → No. Not *saying* you truncated it is the dishonest part.
- *"Where did 48.6 come from?"* → I fiddled with it until the chart looked how I wanted. There is no formula, and assuming there is one is how people get fooled.
- *"How many frames does `subplots(1, 2)` make, and what are they called?"* → Two: `axes[0]` and `axes[1]`. There is no `axes[2]`.
- *"Python suggested `var`. Should you use it?"* → No. The suggestion matched the letters, not the meaning. Suggestions are hints.
- *"Now measure the honest bars. What's the ratio?"* → About 1.04. Which is the truth.
- *"Which panel would you put on a poster if you wanted 7A in trouble?"* → The left one — and that is exactly why you check the axis on every bar chart you are shown.
- *"Ice cream and drowning: 0.997. Ban ice cream?"* → No. Hot weather causes both.
- *"Which of the three correlations is biggest?"* → The ice cream one, 0.997 — the absurd one. Strength says nothing about cause.
- *"Why might a 14-year-old study half an hour a week?"* → A job, a sibling to look after, no quiet room, a long commute, illness, something at home. None of it is on the chart, and none of it is fixed by ordering more study.

---

## 🔮 Next Week Preview

This section says what next week covers and what to prepare for it.

Term 4 starts, and it is the term the whole year has been walking towards: the student trains models.

Week 28 does the piece of translation that makes it possible — taking a table with names on the columns and splitting it into **`X`**, everything you measured, and **`y`**, the one thing you want the machine to give back. Those two letters are Level 1's *features* and *label*, finally written down in code.

It is a quiet week with only one big idea in it, and the big idea is a shape: `X` is a grid with one row per example, `y` is a single column with one answer per row, and they must have the same number of rows or nothing works. The week finishes with the student computing the distance between two flowers by hand on paper, then in numpy, and getting the same number to two decimal places — which is the last thing they will ever have to trust on faith, because from Week 29 the computer does it a thousand times a second.

**Prep early:** three things. **Keep every chart from Term 3** — the capstone in Week 34 reuses them, and the student will want to see how much better their charts got. **Check `scikit-learn` still imports** tonight, because Week 28 is the first week that needs it and you do not want to discover an install problem in a lesson: `python -c "from sklearn.datasets import load_iris; print(load_iris().data.shape)"` should print `(150, 4)`. And if you have five spare minutes, go and look at a real iris flower, or a picture of one, and find the petal and the sepal — Week 28 measures both, and a student who has never noticed that a flower has two different kinds of leaf spends the whole lesson quietly confused about what a "sepal" is.

---

[⬅ Week 26](week-26.md) · [Course Home](../README.md) · [Week 28 ➡](week-28.md) · [Student Guide](../student-guide/week-27.md) · [Workbook](../workbook/week-27.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)

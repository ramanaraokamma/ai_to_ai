# Week 26 — Five Questions, Five Chart Shapes

[⬅ Week 25](week-25.md) · [Course Home](../README.md) · [Week 27 ➡](week-27.md) · [Student Guide](../student-guide/week-26.md) · [Workbook](../workbook/week-26.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — three new chart shapes and one new discipline (the question chooses the chart) |
| **Big idea** | The question decides the chart: comparison to bar, spread to histogram, relationship to scatter. |
| **New vocabulary** | bar chart · histogram · bin · scatter plot · distribution |
| **New syntax** | `ax.bar(names, values)` · `ax.hist(values, bins=8)` · `ax.scatter(x, y)` · `df["c"].value_counts()` (back from Week 24) |
| **Materials** | The printed workbook (Warm-Up through Self-Check; the card-matching grid is **Practice Set A, A1**) · **the eight question cards, cut out** (the eight A1 questions, one per slip; also listed in the Answer Key) · **the five shape cards** (LINE · BAR · HISTOGRAM · SCATTER · NEITHER, one slip each) · **one printed copy of the broken line chart** (see Prep) · a pencil |
| **Tech needed** | The `level2` folder, venv active, matplotlib and pandas. The cleaned 38-row table from Week 24. |
| **Prep time** | 15 minutes the night before, 5 minutes on the day |

> **⚠️ Watch out:** the eight question cards must be **cut out and face down before the lesson starts.** Cutting paper in front of a 12-year-old costs four minutes and kills the surprise, and the surprise is the whole activity.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Choose a chart shape from the question being asked**, not from what looks nice — and say the reason in one sentence.
2. **Draw a bar chart of counts** produced by `value_counts()`, with every category named on the x axis.
3. **Draw a histogram and describe the spread it reveals** — where the bulk is, how wide it is, and whether there is one hump or two.
4. **Draw a scatter plot and describe the relationship in words** — direction, roughly how tight, and any dot that argues.
5. **State, for each chart drawn, one thing it hides.**

Observable evidence: eight question cards correctly matched to shapes with a written reason for each; four saved PNGs, all fully labelled; and four written "this chart hides…" sentences that name something specific.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

Week 25 taught the machinery: figure, axes, labels, save. This week is about **judgement**, and judgement is harder to teach than syntax. Read this whole section — the "what it hides" idea in §6 is the part most likely to catch you out, and it is the most valuable thing in the week.

### 1. The mistake almost everybody makes

People decide "I'll do a bar chart" and *then* look for something to put in it. That is backwards, and it produces charts that answer no question at all.

🍕 **The analogy.** You do not pick up a spoon and then go looking for food that suits a spoon. You look at the soup, and the spoon is obvious. Look at your question, and the chart is obvious.

![The question picks the chart](../figures/fig-w26-1-question-picks-the-chart.svg)
*Figure 26.1 — Four question shapes, four charts. Decide the shape before you type.*

### 2. The four shapes you can draw, and the fifth answer

| The question sounds like… | Shape | What the reader's eye does |
|---|---|---|
| "How did X change **over time**?" | **line** *(Week 25)* | follows a slope — up, down, flat, bumpy |
| "Which **category** is biggest?" | **bar** | compares heights, side by side |
| "What do the values **look like all together**?" | **histogram** | reads the shape of a pile |
| "Do X and Y **go together**?" | **scatter** | reads the tilt and the tightness of a cloud |
| *(none of the above)* | **no chart** | sometimes the honest answer is one printed number, or "that question isn't measurable yet" |

That fifth row is not a joke and it is not padding. Two of the eight question cards land on it, and they land there for two completely different reasons:

- **"What is the average score?"** is a question with **one number** as its answer. A chart of one number is a bar standing on its own with nothing to compare it to, which is the least informative object in data work. `print(df["score"].mean())` is the correct, complete answer. Say so.
- **"Is chess better than art?"** is not answerable *at all* until somebody defines "better". Higher average score? Higher lowest score? More members? Most consistent? Those are four different charts with four different answers. **The right move is to hand the question back**, not to draw something.

> **🧑‍🏫 If a student asks:** *"What about box plots? I've seen those."* — Be honest. There is a fifth *drawable* shape, the **box plot**, for the question "how consistent is each group?" It is genuinely useful and it is genuinely more complicated to read, and we are not drawing it this year. Tell them the name so they recognise it in the wild, and tell them the question it answers. Do not teach it today; there is not room.

### 3. Bar charts, and `value_counts()`

> **Bar chart** — one rectangle per category, where the height is the value.

The single most common bar chart in the world is a **count** of how many rows fall into each category, and pandas has a one-line tool for it, new this week:

```python
club_counts = df["club"].value_counts()
```

Read it as: *"go down the `club` column, and count how many times each different value appears."* It hands back a small table — a Series — with the category names down the side and the counts beside them, **sorted biggest first**.

```text
chess    14
music    12
art      12
Name: club, dtype: int64
```

Two attributes of that result are what you feed to `ax.bar`:

- `club_counts.index` — the names: `['chess', 'music', 'art']`
- `club_counts.values` — the heights: `[14, 12, 12]`

`.values` with an **s**. Without the s you get `AttributeError: 'Series' object has no attribute 'value'. Did you mean: 'values'?` — Clinic row 1, and you should expect to see it, because `.index` has no s and `.values` does, which is a genuinely annoying inconsistency.

```python
ax.bar(club_counts.index, club_counts.values)
```

First argument the names, second the heights. Same order as `ax.plot`: what goes along the bottom, then what goes up the side.

> **⚠️ Watch out — the failure that produces no error.** `ax.bar(df["club"], df["score"])` runs perfectly and draws **38 bars**, one per row, stacked on top of each other in three columns. No error, no warning, and a completely meaningless picture. A bar chart needs *one number per category*, which means you must summarise first — with `value_counts()` for counts, or `groupby` from Week 24 for averages. This is Clinic row 5 and it is worth causing on purpose.

### 4. Histograms, bins, and the one thing that separates them from bar charts

> **Histogram** — chops one column of numbers into ranges, and shows how many values landed in each range.
> **Bin** — one of those ranges.
> **Distribution** — the whole shape of the pile of values.

A histogram takes **one** column of numbers and no categories at all:

```python
counts, edges, bars = ax.hist(scores, bins=8, edgecolor="white")
```

- `scores` — one column of numbers.
- `bins=8` — "chop the range into eight equal-width slices". matplotlib finds the lowest and highest value and divides the gap between them into eight.
- `edgecolor="white"` — draws a thin white line between neighbouring bars so you can count them. Not decoration: without it, touching bars merge into one blue slab.
- The three names on the left catch what `hist` hands back: the **counts** per bin, the **edges** it chose, and the drawn rectangles. Printing the first two is how you check your own chart.

```text
counts: [3. 4. 4. 5. 6. 5. 6. 5.]
edges : [42.   48.88 55.75 62.62 69.5  76.38 83.25 90.12 97.  ]
bins add up to: 38.0
```

Two things to notice in that output, and to say out loud:

1. **The counts add up to 38** — the number of students. **Always check this.** If they do not add up, a value has fallen through a crack, which usually means a bin edge is in the wrong place.
2. **The edges are ugly**: 48.88, 55.75, 62.62. matplotlib divided 42-to-97 into eight equal slices and did not care that the answers were not round numbers. You can hand it your own edges instead — `bins=range(40, 101, 10)` gives 40, 50, 60, … 100 — and for a chart somebody else will read, you should. Today, `bins=8` is fine and keeps one idea per lesson.

![One bin, one count, one bar](../figures/fig-w26-2-histogram-bins-the-spread.svg)
*Figure 26.2 — Every value drops into exactly one bin. The bin's count becomes the bar's height. That is the whole mechanism.*

**The bar-vs-histogram distinction, which students genuinely find hard.** Both are rectangles. The difference is what one rectangle *means*:

![Bars have gaps. Histogram bars touch.](../figures/fig-w26-5-bar-vs-histogram.svg)
*Figure 26.3 — One bar per category, with gaps. One bar per number range, touching. The gaps are the tell.*

| | Bar chart | Histogram |
|---|---|---|
| One rectangle is… | one **category** | one **number range** |
| The x axis holds… | names | numbers |
| Do the bars touch? | **No** — gaps, because categories do not join up | **Yes** — because 50-to-60 touches 60-to-70 |
| How many columns of data? | two (names, values) | **one** (just the numbers) |
| Reorder the bars? | Yes, freely | **No** — the order is the number line |

**What happens if you histogram a text column.** It does not crash. It quietly produces this:

```text
counts: [14.  0.  0.  0. 12.  0.  0. 12.]
edges : [0.   0.25 0.5  0.75 1.   1.25 1.5  1.75 2.  ]
```

matplotlib turned the three club names into 0, 1 and 2 and binned *those*. The counts happen to be right; the x axis is meaningless. **A wrong answer with no error message is more dangerous than a crash**, and this is a good, cheap place to say so.

### 5. The sting: why the mean can hide the shape

This is the emotional centre of the lesson and the reason the histogram matters. Work through it tonight with a pencil.

Twenty students sat quiz 3. The marks:

```
33, 35, 37, 38, 39, 39, 40, 41, 42, 44, 81, 83, 84, 85, 85, 86, 86, 87, 87, 88
```

- **Total** = 1240. **Mean** = 1240 ÷ 20 = **62.0**
- Sorted, the middle two values (the 10th and 11th) are **44 and 81**, so the **median** = (44 + 81) ÷ 2 = **62.5**

Both summaries say sixty-two. A perfectly reasonable teacher would report "the class averaged 62, a middling result" and move on.

**Not one single student scored between 44 and 81.** The mean is describing a person who does not exist, and the median — which is normally the *safe* summary, the one that shrugs off outliers — has been fooled just as badly, because it landed in the gap between the two clumps.

![The mean was 62. Nobody scored 62.](../figures/fig-w26-3-mean-hidden-by-shape.svg)
*Figure 26.4 — Two clumps, one at 39 and one at 85. Both summary numbers landed in the empty middle.*

The histogram makes it unmissable in half a second:

```text
counts: [6. 4. 0. 0. 0. 0. 1. 9.]
```

Six, four, then **four empty bins**, then one, then nine. Two clumps with a hole between them. There is a name for that shape:

> **Bimodal** — a distribution with two separate humps, which almost always means two different groups have been mixed together.

And when you go and ask, that is exactly what it was: ten of the twenty had done the Level 1 course and ten had never coded before. Their means were **85.2** and **38.8**. Two honest groups, averaged into one dishonest number.

**The three things to read off every histogram**, and the order to read them in:

1. **Centre** — where is the bulk?
2. **Spread** — narrow pile or wide pile?
3. **Shape** — one hump? two humps? a long tail off one side? a gap?

Number 3 is the one nobody checks and the one that bites.

### 6. Scatter plots, and how to describe one without overclaiming

> **Scatter plot** — one dot per row, placed at (x, y); the shape of the cloud is the answer.

```python
ax.scatter(df["hours"], df["score"])
```

Two number columns, no line. **Never join scatter dots up** — a line implies you went from one dot to the next in that order, and you did not; each dot is a different person.

![Read the tilt, spot the exception](../figures/fig-w26-4-scatter-relationship.svg)
*Figure 26.5 — Direction, tightness, and the one dot worth arguing about.*

Three things to say about any scatter, in words:

1. **Direction** — up to the right, down to the right, or no tilt at all.
2. **Tightness** — a narrow band, or a shapeless blob?
3. **Exceptions** — is there a dot a long way off the pattern? *That dot is usually the most interesting row in the table.*

**And now the discipline that matters more than any of it.** Say *"students who studied more tended to score higher."* Do **not** say *"studying raised their scores."* The first is a description of the picture. The second is a claim about cause, and a scatter plot cannot support it. Week 27 spends a whole lesson on why. Today, just police the verb: **"tended to go with"**, never **"caused"**.

### 7. Every chart hides something — and that is this week's homework

This is the idea that turns chart-drawing into thinking, and it is worth being precise about, because "it hides stuff" is not an answer.

**A chart that hides only irrelevant detail is called clear. A chart that hides a decision-changing detail is called misleading. The code is identical.** The difference lives entirely in what somebody is going to *do* next.

Worked, for the four charts the class will build:

| Chart | What it shows | What it hides — specifically |
|---|---|---|
| bar of club counts | chess 14, music 12, art 12 | Every single score. Chess's 14 members range from 55 to 97; the bar is one number standing in front of a crowd. |
| bar of house means | Blue 74.4, Red 74.3, Green 67.4 | **How many rows each average came from** (Blue 14, Green 12, Red 12) and the spread inside each house (Blue runs 42–93). A mean of 12 rows and a mean of 12,000 rows look identical on a bar chart. |
| histogram of scores | wide, 42 to 97, no single peak | **Who** each bar is. The top bin (90.1 to 97) does not say which club, house or age those five students are. |
| scatter of age vs hours | older students report fewer hours | **Dots landing on top of each other.** There are 38 rows but only **23** distinct (age, hours) pairs, so 15 dots are hidden underneath other dots. The chart looks like 23 students. |

That last one is a genuine, professional-grade observation and it is checkable in one line of Week-24 code: `df.groupby(["age", "hours"]).size()` has 23 rows, not 38. It is the answer to look out for.

### 8. How deep to go, and where to stop

**Go this far:** the question chooses the shape; bar from `value_counts` and from `groupby`; histogram and bins; scatter; describing a distribution and a relationship in words; naming what a chart hides.

**Stop before:**
- **Box plots.** Name them, do not draw them.
- **`ax.set_ylim(...)`.** Week 27, and it is the best lesson of the term. Do not spoil it. If a student asks whether a bar chart has to start at zero, say "yes, and next week you'll find out exactly why" and leave it there.
- **`ax.legend()`.** Week 27. Every chart today has one series.
- **Correlation, `r`, and the word "causes".** Week 27. Today you describe a scatter in *words only*. No numbers for strength.
- **`ax.bar_label()`, colours per bar, stacked bars, grouped bars.** All fun, none of them this week's idea.
- **Choosing bin edges by a rule.** Mention that `bins=range(40, 101, 10)` gives round numbers. Do not teach a formula for how many bins.

---

### 9. 🧭 The Growing Map — the last tile before the models

The student guide carries a figure called **Where This Fits** — the same picture every week with one
more piece filled in, and the only page that shows the learner the *shape* of the year instead of the
week. There are three dashed boxes left on it. In Week 1 there were thirteen.

![The Level 2 pipeline in Week 26: your first chart is finished and the honest axes tile opens](../figures/fig-w26-0-where-this-fits.svg)

*Figure 26.0 — Week 26's version. "Your first chart" has turned plain white; the gold has moved to
"honest axes", a tile that covers two weeks. **Representation** and **evaluation** are both lit.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and ask a Week 26 question:** *"bar, histogram, scatter, line — plus the sentence about
   what each one hides. Which box?"* Then the question that is really worth asking: *"why is **what
   does it hide** filed in a box called **honest axes**?"* You want something close to *"because
   leaving something out is a way of not being honest"* — and that is next week, pre-loaded, without
   you having to say a word about `set_ylim`.
2. **Then count the dashes with them.** Three boxes left: the two tiles of `PREDICT & CHECK` and the
   stage box above them. Ask *"so how much of the year is left on this picture?"* Seeing it as
   *nearly finished* matters in a term where the work is getting harder.
3. **Have them update their own copy** and write the four question-words beside the *honest axes*
   tile — **compare**, **spread**, **together**, **over time**.

> **🧑‍🏫 Why this is worth two minutes.** The failure mode of this week is a learner who can produce
> four correct charts and still has no idea how you pick one. The map puts the choosing, not the
> drawing, in the box — so the thing on the picture is the thing you actually assessed.

> **⚠️ Watch out:** do not let the two-week tile read as *"we are stuck."* Say what is coming: this box
> has two halves, the shapes this week and the honesty next week, and the second half is the one they
> will still remember in five years.

---

## 🧰 Prep Checklist

### 15 minutes the night before

- [ ] **Print the workbook** (Warm-Up through Self-Check). It carries section names and item labels, not page numbers.
- [ ] **Make and cut out the eight question cards** (the eight questions in the A1 table of Practice Set A, one per slip) and the **five shape cards**. Put the question cards in a face-down pile. Put the five shape cards face up in a row: LINE · BAR · HISTOGRAM · SCATTER · NEITHER.
- [ ] **Print the broken line chart for the Hook.** Run this in your `level2` folder and print the PNG:

  ```bash
  python week26_hook_bad_line.py
  ```

  The file is in the Answer Key. It draws a *line* joining the three club names, which is nonsense, and that nonsense is the hook.
- [ ] **Check the Week 24 cleaned table is in the folder.** You need `students.py` — the 38-row table that came out of Mess Detective. If it is missing, the full typed-out version is in the Answer Key; copy it into `~/ai-academy/level2` tonight, and run it once:

  ```bash
  python students.py
  ```

  ```text
  (38, 6)
           name  age  house   club  hours  score
  0  Aarav Shah   13    Red  chess    3.5     72
  1    Bela Roy   14    Red  music    5.0     90
  2     Chen Wu   13   Blue  chess    2.0     55
  3  Divya Nair   13   Blue    art    4.5     83
  4   Emeka Obi   13  Green  music    3.0     61
  ```
- [ ] **Do the sting by hand.** Add up the twenty quiz marks with a pencil, divide by 20, and find the middle two. You want to have felt 62.0 and 62.5 arrive before you show them. Two minutes, and it makes the whole segment yours.
- [ ] **Run `week26_sting.py`** (Answer Key) and check you get `counts: [6. 4. 0. 0. 0. 0. 1. 9.]`. Open the PNG and look at the hole in the middle.
- [ ] **Break the histogram on purpose, once.** Run `ax.hist(df["club"], bins=8)`. Note that it does not error. You will do this in front of the student and you want to have seen it first.

### 5 minutes on the day

- [ ] Terminal in `~/ai-academy/level2`, venv active. Folder window visible beside the editor.
- [ ] `students.py` present in the folder.
- [ ] Printed broken line chart face down.
- [ ] Eight question cards face down; five shape cards face up in a row.
- [ ] Workbook open at Practice Set A, A1 (the card-matching grid with a "reason" column) on the table.

### Fallback if a laptop fails

| If this fails | Do this instead |
|---|---|
| No laptop at all | **The card game is the lesson and needs no computer.** Eight questions, five shapes, one written reason each: that is objective 1 and objective 5 complete. Then do the histogram of the twenty quiz marks **by hand on squared paper** — tally the bins, draw the bars, and find the hole. Objective 3 lands harder on paper than on a screen, because they have to count the empty bins themselves. |
| `students.py` is missing and there is no internet | Type the twenty quiz marks only. The sting is the most important part of the week and it needs no table and no pandas. |
| pandas imports but matplotlib does not | Do everything with `print`. `df["club"].value_counts()`, then draw the bars by hand next to the printed numbers. Every idea survives; only the pictures are lost. |
| The student insists a line chart of the clubs is fine | Excellent — do not argue, ask. "What does the slope between art and chess mean? How much is halfway between art and chess?" Wait. The answer is that there is no such thing, and they will get there. |
| The eight cards are lost | The eight questions are printed in full in the Answer Key. Read them aloud one at a time and have the student point at one of five shape cards. Works fine. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — What Does This Slope Mean? | 7 | 7 | A line chart of three club names, and why it is nonsense |
| 🧠 Concept — Four Shapes and a Fifth Answer | 16 | 23 | The question picks the chart; bar vs histogram |
| 💻 Live-Code Together — Bar, Histogram, and the Sting | 18 | 41 | Two deliberate mistakes; then the mean of 62 |
| 🎲 Their Turn — Eight Cards, Then Two Charts | 20 | 61 | Match the cards, then build the scatter |
| 🔑 Wrap & Assign | 9 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — What Does This Slope Mean? (7 minutes)

**Do this:** Put the printed broken line chart on the table. It is a proper chart: it has a title, both axis labels, markers, and it is correctly saved. It is also completely wrong.

**Say this:**

> "I made this last night. I did everything you learned last week. Title, both axis labels, units, markers on every real point, saved as a PNG. Have a look and tell me if I've missed anything."

Let them inspect it. They will usually say it looks fine, because by last week's checklist it *is* fine.

> "Right. So here's my question. Put your finger on the line between **art** and **chess**. That bit of line, going up.
>
> What does it mean?"

Wait. Let the silence do the work.

> "Try this instead. What's **halfway between art and chess**?"

This is where it cracks. There is no such thing.

> "There isn't one. There's no half-art-half-chess club. And that's the whole problem, because **a line means you can travel along it.** When I draw a line from week 1 to week 2, the bit in the middle is Tuesday. It's real. When I draw a line from art to chess, the bit in the middle is nothing at all. I've drawn a road between two places that aren't next to each other, and then I've implied you can walk along it.
>
> Worse: watch this." *(Take a pencil and write the three names in a different order on paper — chess, music, art.)*
>
> "I can shuffle these three names into any order I like, and every order gives a different-shaped line. Six different lines, all from the same three numbers, and not one of them means anything. **If reordering your x axis changes the shape of your chart, you have used the wrong chart.**
>
> Which means last week's checklist wasn't enough. A chart can have a perfect title, perfect labels, perfect units — and still be the wrong shape for the question. That's today.
>
> **The question decides the chart. Not what looks nice, not what you drew last time. The question.**"

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Have I missed anything on this chart?" | "No" — by last week's rules it is complete. | If they spot the line problem immediately, say so loudly and hand them the pencil: "Then you tell me why." |
| "What does the line between art and chess mean?" | Nothing. | If they say "chess is bigger than art" — that is true and it is what a *bar* would show. Reply: "Agreed. So what is the *line* adding?" |
| "What is halfway between art and chess?" | There is nothing halfway. | If they joke "chart club" — laugh, and then ask how many members it has. Point made. |
| "If I shuffle the three names, does the chart change?" | Yes, completely. | If they are unsure, physically write the three names in two different orders and sketch both. Ten seconds, and it is undeniable. |
| "So when IS a line the right shape?" | When the x axis is in order and the in-between is real — days, weeks, ages, temperatures. | If they say "always for numbers", push: "House numbers are numbers. Would you join 12 and 14 with a line?" |

---

### 🧠 Concept — Four Shapes and a Fifth Answer (16 minutes)

**Do this:** Have Figure 26.1 visible. Put the five shape cards face up in a row on the table.

**Say this — part 1, the four shapes:**

> "There are only about four shapes you need, ever, and each one answers a different *kind* of question. Look at Figure 26.1 with me.
>
> **'How did it change over time?'** — that's a **line**. You did those last week. The x axis has to be in order, and the in-between has to be real.
>
> **'Which category is biggest?'** — that's a **bar**. One rectangle per category, and your eye compares heights. Names on the bottom, and the bars don't touch, because categories don't touch.
>
> **'What do all the values look like together?'** — that's a **histogram**. And this one is new and it's the strange one. It takes **one** column of numbers, chops the range up into slices, and counts how many landed in each slice.
>
> **'Do these two numbers go together?'** — that's a **scatter**. One dot per row. Thirty-eight students, thirty-eight dots. And you read the *tilt* of the cloud."

**Say this — part 2, bar vs histogram, the hard one:**

> "Now the confusing pair, because they're both made of rectangles. Look at Figure 26.3." *(Show `fig-w26-5`.)*
>
> "Left is a bar chart. Three rectangles, with **gaps** between them, and the words `chess`, `music`, `art` underneath. One rectangle is one club.
>
> Right is a histogram. Six rectangles, **touching**, and the numbers underneath are at the *edges* — 40, 50, 60, 70. One rectangle is one *range of scores*.
>
> The gaps are the tell. And here's the reason for the gaps: sixty touches seventy. There's nothing between them. But art doesn't touch chess. There's no in-between at all — same problem as the hook.
>
> One more difference, and it's the one to hold onto: **a bar chart needs two columns and a histogram needs one.** Bar: the names *and* the numbers. Histogram: just the numbers. It works out the rest."

**Say this — part 3, how a histogram actually works:**

> "Look at Figure 26.2." *(Show it.)*
>
> "Twelve values, sitting as dots on a number line from 40 to 90. Then I chop that line into five bins, ten wide each. Every dot falls into exactly one bin — no dot is left out and no dot goes in two. Count each bin: one, three, four, three, one. Those five counts *become* the five bar heights.
>
> That's the whole mechanism. And it gives you a free check that you should do every single time: **the bin counts must add up to how many values you started with.** One plus three plus four plus three plus one is twelve, and there were twelve dots. If it doesn't add up, something's fallen through a crack."

**Say this — part 4, the fifth card:**

> "Now — the fifth card on the table says **NEITHER**, and I need you to take it seriously, because two of the eight cards you're about to draw belong on it, for two completely different reasons.
>
> Sometimes the answer is **one number**. 'What's the average score?' — that's seventy-two point one. That's the answer. A chart of one number is a single bar standing on its own with nothing to compare it to, which is about the least useful thing in this entire subject. Print the number.
>
> And sometimes the question **isn't askable yet**. 'Is chess better than art?' — better how? Higher average? Higher lowest mark? More members? Most consistent? Those are four different charts with four different winners, and if you just pick one you've quietly answered a question nobody asked. The right move is to **hand the question back** and make somebody define 'better' before you draw anything."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "'How many students are in each house?' — which shape?" | Bar. Three categories, compare heights. | If they say histogram, ask "how many columns does a histogram need?" (One. This needs names and counts.) |
| "'How are the 38 scores spread out?' — which shape?" | Histogram. One number column, asking about shape. | If they say bar, ask "what would one bar be? One student?" That usually lands it. |
| "How do you tell a bar chart from a histogram in a newspaper?" | Gaps between the bars, and whether the x axis holds names or numbers. | If they say "you can't", show Figure 26.3 again and cover the labels. The gaps still tell you. |
| "A histogram's bins add up to 34, but you have 38 rows. What happened?" | Four values fell outside the bin range, so they were left out. | If stuck, offer: "Where would a score of 105 go, if your bins stop at 100?" |
| "'Which club is best?' — which shape?" | NEITHER. 'Best' is undefined; hand the question back. | If they pick bar of mean scores, accept it *and* push: "You just decided 'best' means highest average. Who said that?" |

---

### 💻 Live-Code Together — Bar, Histogram, and the Sting (18 minutes)

You type; the student types along on their own machine. **Two deliberate mistakes, marked 🐞.** The second one is the important one, because it does not produce an error.

#### Step 1 — the bar chart, and 🐞 mistake #1 (6 min)

**Do this:** New file, `week26_counts.py`. Type:

```python
# week26_counts.py -- "Which club has the most members?" -> a BAR chart.
import matplotlib.pyplot as plt
from students import build_students          # the cleaned 38-row table from Week 24

df = build_students()

club_counts = df["club"].value_counts()      # count the rows for each club
print(club_counts)                           # LOOK at it before you draw it
```

Run it:

```text
chess    14
music    12
art      12
Name: club, dtype: int64
```

**Say this:**

> "One line. `value_counts` goes down the club column and counts how many times each different value shows up. Chess fourteen, music twelve, art twelve. And it sorted them biggest-first without being asked.
>
> Notice I printed it *before* drawing anything. Always. If those numbers are wrong, the chart will be wrong, and it's much easier to spot a wrong number than a wrong picture."

Add the two lines that pull the pieces out, then 🐞 **make the mistake:**

```python
print("names :", list(club_counts.index))
print("values:", list(club_counts.value))
```

```text
chess    14
music    12
art      12
Name: club, dtype: int64
names : ['chess', 'music', 'art']
Traceback (most recent call last):
  File "/Users/you/ai-academy/level2/week26_counts.py", line 10, in <module>
    print("values:", list(club_counts.value))
AttributeError: 'Series' object has no attribute 'value'. Did you mean: 'values'?
```

> "Read me the last line."

Let them read it.

> "`'Series' object has no attribute 'value'`. So: I asked this little table for something called `value`, and it hasn't got one. And Python has guessed for me — `values`, with an s.
>
> And this is genuinely irritating, so it's worth saying out loud: `index` has **no** s and `values` **has** an s. There's no reason. You'll get it wrong again. When you do, Python will tell you again."

Fix it, then finish the chart:

```python
print("total :", club_counts.sum())          # must add back up to 38

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(club_counts.index, club_counts.values)   # one rectangle per club

ax.set_title("Chess is the biggest club: 14 of our 38 students")
ax.set_xlabel("Club")
ax.set_ylabel("Number of students (count)")

fig.savefig("club_counts.png", dpi=120, bbox_inches="tight")
print("saved club_counts.png")
```

```text
chess    14
music    12
art      12
Name: club, dtype: int64

names : ['chess', 'music', 'art']
values: [14, 12, 12]
total : 38
saved club_counts.png
```

Open the PNG. Then:

> "Fourteen plus twelve plus twelve is thirty-eight, which is how many students we have. That check takes two seconds and it has caught real mistakes for real people."

#### Step 2 — the histogram, and 🐞 mistake #2 (6 min)

**Do this:** New file, `week26_spread.py`. Type the imports and the summary block:

```python
# week26_spread.py -- "How spread out are the scores?" -> a HISTOGRAM.
import matplotlib.pyplot as plt
from students import build_students

df = build_students()

scores = df["score"]                 # ONE column of numbers. That is a histogram's food.
print("how many:", len(scores))
print("lowest  :", scores.min())
print("highest :", scores.max())
print("mean    :", round(scores.mean(), 1))
print("median  :", scores.median())
```

```text
how many: 38
lowest  : 42
highest : 97
mean    : 72.1
median  : 72.5
```

🐞 **Now make the second mistake, deliberately and cheerfully.** Say: *"Let's histogram the clubs while we're here."* Type:

```python
fig, ax = plt.subplots(figsize=(6, 4))
counts, edges, bars = ax.hist(df["club"], bins=8)
print("counts:", counts)
print("edges :", edges)
```

Run it. **No error.**

```text
how many: 38
lowest  : 42
highest : 97
mean    : 72.1
median  : 72.5
counts: [14.  0.  0.  0. 12.  0.  0. 12.]
edges : [0.   0.25 0.5  0.75 1.   1.25 1.5  1.75 2.  ]
```

**Say this:**

> "No error. Program finished happily. Now look at the edges. Zero, nought-point-two-five, nought-point-five… **what is 0.75 of a club?**
>
> matplotlib has quietly turned art, chess and music into 0, 1 and 2, and then chopped the range from 0 to 2 into eight slices. The counts are even *correct* — fourteen, twelve, twelve, in the right order. And the x axis is complete nonsense.
>
> This is worse than a crash. A crash stops you. This hands you a chart you can print and put in a project, and it's meaningless. **A histogram needs numbers.** A wrong answer with no error message is the most dangerous thing in this course, and it's the reason we print things before we believe them."

Delete those lines and do it properly:

```python
fig, ax = plt.subplots(figsize=(6, 4))
counts, edges, bars = ax.hist(scores, bins=8, edgecolor="white")

print("counts:", counts)
print("edges :", edges.round(2))
print("bins add up to:", counts.sum())

ax.set_title("Scores spread all the way from 42 to 97, with no single peak")
ax.set_xlabel("Score (points out of 100)")
ax.set_ylabel("Number of students (count)")

fig.savefig("score_spread.png", dpi=120, bbox_inches="tight")
print("saved score_spread.png")
```

```text
how many: 38
lowest  : 42
highest : 97
mean    : 72.1
median  : 72.5
counts: [3. 4. 4. 5. 6. 5. 6. 5.]
edges : [42.   48.88 55.75 62.62 69.5  76.38 83.25 90.12 97.  ]
bins add up to: 38.0
saved score_spread.png
```

> "Thirty-eight. Adds up. And read the shape out loud with me: the scores go all the way from 42 to 97, the middle bins are all about the same height, and there's no single peak. That's a *wide, flat* distribution. Also — mean 72.1, median 72.5. Nearly the same. Hold on to that, because in about ninety seconds it's going to matter."

#### Step 3 — the sting (6 min)

**Do this:** New file, `week26_sting.py`. Type it all before running.

```python
# week26_sting.py -- the average said 62. Nobody scored 62.
import matplotlib.pyplot as plt

# Quiz 3, out of 100, every one of the 20 members of the coding club.
marks = [33, 35, 37, 38, 39, 39, 40, 41, 42, 44,
         81, 83, 84, 85, 85, 86, 86, 87, 87, 88]

total = sum(marks)                          # add them all up
mean = total / len(marks)                   # the average
ordered = sorted(marks)                     # a sorted copy, low to high
middle_left = ordered[9]                    # the 10th value (slots count from 0)
middle_right = ordered[10]                  # the 11th value
median = (middle_left + middle_right) / 2   # 20 values, so average the middle two

print("how many:", len(marks))
print("total   :", total)
print("mean    :", mean)
print("median  :", median)
print("the middle two values were", middle_left, "and", middle_right)
```

**Ask, before running:** *"Twenty marks. Guess the average."* Let them guess. Then run:

```text
how many: 20
total   : 1240
mean    : 62.0
median  : 62.5
the middle two values were 44 and 81
```

**Say this:**

> "Sixty-two. And the median's sixty-two point five, so both summaries agree. If I wrote a report I'd write 'the club averaged 62, a middling result', and nobody would question it.
>
> Now look at the last line. The middle two marks were **forty-four and eighty-one**. Look back at the list. How many people scored between 44 and 81?"

Let them count. The answer is nobody.

> "Nobody. Not one person. The average is sixty-two, and the nearest human being to it is eighteen marks away.
>
> And that's the bit I want you to feel: the median was supposed to be the safe one. The median is the one that ignores weird values. It got fooled just as badly, because it landed **in the gap.**"

Now draw it:

```python
fig, ax = plt.subplots(figsize=(6, 4))
counts, edges, bars = ax.hist(marks, bins=8, edgecolor="white")

print("counts:", counts)
print("edges :", [round(e, 2) for e in edges])

ax.set_title("Mean = 62, and nobody scored between 44 and 81")
ax.set_xlabel("Quiz 3 mark (points out of 100)")
ax.set_ylabel("Number of students (count)")

fig.savefig("marks_sting.png", dpi=120, bbox_inches="tight")
print("saved marks_sting.png")
```

```text
counts: [6. 4. 0. 0. 0. 0. 1. 9.]
edges : [33.0, 39.88, 46.75, 53.62, 60.5, 67.38, 74.25, 81.12, 88.0]
saved marks_sting.png
```

Open it. Point at the hole.

> "Six, four, then **four empty bins**, then one, then nine. Two clumps and a canyon. Half a second to see, and it took the histogram to see it — the two summary numbers actively hid it.
>
> A pile with two humps has a name: **bimodal**. And a bimodal pile almost always means **two different groups have been mixed together**. So we went and asked. Ten of them had done Level 1. Ten had never written a line of code."

```python
# week26_split.py -- WHY the histogram had a hole in the middle.
marks = [33, 35, 37, 38, 39, 39, 40, 41, 42, 44,
         81, 83, 84, 85, 85, 86, 86, 87, 87, 88]

brand_new = marks[:10]        # slots 0 to 9
did_level1 = marks[10:]       # slots 10 to 19

print("brand new  :", brand_new)
print("  their mean:", sum(brand_new) / len(brand_new))
print("did Level 1:", did_level1)
print("  their mean:", sum(did_level1) / len(did_level1))
print("everyone   : mean", sum(marks) / len(marks))
```

```text
brand new  : [33, 35, 37, 38, 39, 39, 40, 41, 42, 44]
  their mean: 38.8
did Level 1: [81, 83, 84, 85, 85, 86, 86, 87, 87, 88]
  their mean: 85.2
everyone   : mean 62.0
```

> "Thirty-eight point eight and eighty-five point two. **Two honest averages, mashed into one dishonest one.** And here's the sentence for the week:
>
> **Draw the histogram before you quote the average.** It costs three lines."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Guess the average of these twenty marks." | Anything. The guess makes the reveal land. | If they refuse to guess, guess badly yourself out loud. |
| "How many people scored between 44 and 81?" | Nobody. | If they say "a few", make them point at one in the list. There isn't one. |
| "The median is supposed to be safe. Why did it fail here?" | It landed in the empty gap between the two clumps. | If stuck: "Where is the middle of a doughnut?" |
| "What does two humps usually mean?" | Two different groups mixed together. | If they say "a mistake", accept it as possible and then offer the more common explanation. |
| "So when should you trust a mean?" | When you have looked at the shape and it is one hump, roughly even on both sides. | If they say "never", that is over-correcting. Point at the score histogram: mean 72.1, median 72.5, one broad hump. That mean is fine. |

---

### 🎲 Their Turn — Eight Cards, Then Two Charts (20 minutes)

Full instructions in the next section.

- **Minutes 0–8:** the card game. Eight questions, five shapes, a written reason for each.
- **Minutes 8–18:** build the scatter of hours vs score, then the bar of house means. Both fully labelled and saved.
- **Minutes 18–20:** write the "what it hides" sentence for each of the two.

---

## 🎲 The Activity, In Full

### Setup

**On the table:** the eight question cards, **face down** in a pile. The five shape cards, face up in a row. The workbook open at Practice Set A, A1 (the matching grid with a "reason" column). A pencil.

**On the machine:** `level2` folder, venv active, `students.py` present.

### Part A — The card game (8 minutes)

**The rules:**

1. **Draw one card. Read it out loud.**
2. **Put it on one of the five shape cards.** Out loud, before anything else.
3. **Then write the reason in the A1 grid of the workbook, in one sentence.** The reason is what is being marked, not the match.
4. **No laptop open during Part A.** This is the rule that makes the activity work. If the laptop is open they will start typing and stop thinking.

The eight cards and their answers:

| # | The question card | Shape | The reason |
|---|---|---|---|
| 1 | "How did my homework time change day by day?" | **LINE** | Time on the bottom, in order, and the in-between is real. |
| 2 | "Which club has the most members?" | **BAR** | Three named categories; compare heights. |
| 3 | "How spread out are all 38 scores?" | **HISTOGRAM** | One column of numbers, asking about its shape. |
| 4 | "Do students who study more score higher?" | **SCATTER** | Two number columns; do they move together? |
| 5 | "What is the average score of all 38 students?" | **NEITHER** | The answer is one number: 72.1. Print it. A single bar has nothing to compare to. |
| 6 | "Which house has the highest average score?" | **BAR** | Three named categories again — but you must `groupby` first, because the height is an average, not a count. |
| 7 | "Does age go with study hours?" | **SCATTER** | Two number columns again. |
| 8 | "Is the chess club better than the art club?" | **NEITHER** | "Better" is undefined. Higher average? Higher lowest mark? More members? Most consistent? Hand the question back. |

> **🧑‍🏫 If a student asks:** *"Card 6 says bar, same as card 2. Isn't that a repeat?"* — No, and it is the best question in the activity. Card 2's bar heights are **counts** (`value_counts`). Card 6's bar heights are **averages** (`groupby`). Same shape, completely different arithmetic underneath. Say so, and mark it as a win.

**What "finished" looks like for Part A:** all eight cards placed, all eight reasons written, and the two NEITHER cards placed for **two different reasons** — one because the answer is a single number, one because the question is not yet measurable.

### Part B — Build two of them (10 minutes)

Student on the keyboard. Cards 4 and 6.

**Card 4 — the scatter:**

```python
# week26_together.py -- "Do study hours and scores go together?" -> a SCATTER plot.
import matplotlib.pyplot as plt
from students import build_students

df = build_students()

print("rows:", len(df))            # one dot per row, so 38 dots

fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(df["hours"], df["score"])     # x values, y values, and NO line

ax.set_title("Students who studied more hours tended to score higher")
ax.set_xlabel("Study hours per week")
ax.set_ylabel("Score (points out of 100)")

fig.savefig("hours_vs_score.png", dpi=120, bbox_inches="tight")
print("saved hours_vs_score.png")
```

```text
rows: 38
saved hours_vs_score.png
```

**Open it and describe it out loud**, in the three-part order: direction, tightness, exceptions. Model answer: *"Up to the right, quite a tight band, and there's one dot at about 1.5 hours and 78 that's well above the rest."*

> **⚠️ Watch out — the planted trap.** Somebody will write `ax.plot(df["hours"], df["score"], marker="o")` instead of `ax.scatter`, because `plot` is last week's habit. It does not crash. It joins all 38 dots up in table order, producing a dense scribble. **Do not point at the line.** Say: "Describe your chart to me." They cannot, because a scribble has no description. Then: "What is that line saying happened between two students?"

**Card 6 — the bar of averages:**

```python
# week26_house_means.py -- "Which house has the highest average score?" -> BAR.
import matplotlib.pyplot as plt
from students import build_students

df = build_students()

house_mean = df.groupby("house")["score"].mean().sort_values(ascending=False)
print(house_mean.round(2))
print("row counts:")
print(df["house"].value_counts())

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(house_mean.index, house_mean.values)

ax.set_title("Blue and Red are level; Green is 7 points behind")
ax.set_xlabel("House")
ax.set_ylabel("Mean score (points out of 100)")

fig.savefig("house_means.png", dpi=120, bbox_inches="tight")
print("saved house_means.png")
```

```text
house
Blue     74.36
Red      74.25
Green    67.42
Name: score, dtype: float64
row counts:
Blue     14
Red      12
Green    12
Name: house, dtype: int64
saved house_means.png
```

> **💡 Try this:** ask, after the chart appears: "Blue is 74.36 and Red is 74.25. Is Blue better?" The honest answer is that a gap of **0.11 of a mark** across twelve or fourteen students is nothing at all, and no chart of three bars can tell you otherwise. That is a five-second, no-new-syntax preview of Week 27 and it is worth doing.

### Part C — What does it hide? (2 minutes)

One sentence per chart, on scrap paper (the house-means sentence can be copied straight into Build It, Part 5, Chart 2 later). Not "it hides information" — something specific.

| Chart | What it hides |
|---|---|
| scatter of hours vs score | **Which club, house or age each dot is.** Three students studied exactly 1.5 hours and scored 78, 57 and 54 — a 24-mark spread at the identical x value — and the chart gives you no way to ask why. |
| bar of house means | How many students each average came from (Blue 14, Red 12, Green 12), and the spread inside each house — Blue's scores run from 42 to 93. |

### What "finished" looks like

- Eight cards placed, eight reasons written, two NEITHERs with different reasons.
- Two PNGs on disk, both opened and looked at, both fully labelled with units.
- The scatter described out loud in three parts: direction, tightness, exceptions.
- Two "what it hides" sentences that name something specific.

### Variation — easier

- **Use four cards, not eight:** 1, 2, 3, 4 — one clean example of each shape, no NEITHER cards. That is objective 1 complete.
- **Build one chart, not two.** The scatter. It is the newest shape and the most useful.
- **Pre-fill the Shape column** of A1 and have them write only the reason. Explaining a correct answer is most of the learning here.
- Cut Part C to one sentence about one chart.

### Variation — harder

1. **Fix your own bins.** Redo the score histogram with `bins=range(40, 101, 10)` and compare the two. The counts become `3, 6, 7, 8, 8, 6` on round edges — much easier to describe. Then: "Which version would you print for somebody else, and why?"
2. **Find the bimodal column in the real table.** They have `value_counts` and histograms now. Histogram all three number columns (`age`, `hours`, `score`) and say which is closest to two humps. (`age` is the interesting one — it is three spikes, not a smooth pile, because age only takes three values. That is a *third* shape and a genuinely good discovery.)
3. **Write question card 9.** "Invent a question about this table that none of the four shapes can answer, and say what it would need." Good answers involve time (the table has no dates), or cause ("does chess make you better at maths?").
4. **Break the histogram check.** "Make a histogram whose bins do **not** add up to 38." (Use `bins=range(40, 91, 10)` — edges 40 to 90 — and the five students in the 90s are silently dropped. The counts come out `3, 6, 7, 8, 9`, which adds to 33.) Then: "Five students vanished. How would you ever have noticed?" Answer: only by printing the sum.

---

## 🐞 The Debugging Clinic

Every message below came from running a genuinely broken version of this week's code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `AttributeError: 'Series' object has no attribute 'value'. Did you mean: 'values'?` | "That little table hasn't got a thing called `value`." | `club_counts.value` instead of `.values`. `index` has no s; `values` does. | Add the s. Python's suggestion is right. |
| `TypeError: Axes.bar() missing 1 required positional argument: 'height'` | "You told me *where* to put bars but not *how tall*." | `ax.bar(club_counts)` — the whole Series passed as one argument. | `ax.bar(club_counts.index, club_counts.values)` — two arguments, names then heights. |
| `TypeError: Axes.scatter() missing 1 required positional argument: 'y'` | "A dot needs two coordinates and you gave me one." | `ax.scatter(df["hours"])`. | `ax.scatter(df["hours"], df["score"])`. |
| `KeyError: 'Club'` (after a long traceback ending `raise KeyError(key) from err`) | "There is no column with that name." | Capital C. Column names are case-sensitive: it is `club`. | Match the name exactly. `print(df.columns)` lists them. |
| **No error. A bar chart with 38 bars crammed into three columns.** | Nothing. It drew exactly what you asked for. | `ax.bar(df["club"], df["score"])` — raw rows instead of one number per category. | Summarise first: `value_counts()` for counts, `groupby(...).mean()` for averages. |
| **No error. `edges: [0. 0.25 0.5 0.75 1. 1.25 1.5 1.75 2.]`** | "I turned your three words into 0, 1 and 2 and binned those." | `ax.hist(df["club"], bins=8)` — a histogram of a text column. | A histogram needs numbers. Use a bar chart of `value_counts()` for text. |
| `` ValueError: `bins` must be positive, when an integer `` | "Zero bins is not a number of bins." | `bins=0`, usually a typo for `bins=8` or a variable that was never set. | Pass a positive whole number, or a list of edges. |
| **No error. A scatter that looks like a scribble.** | Nothing. You joined the dots. | `ax.plot(x, y, marker="o")` instead of `ax.scatter(x, y)` — last week's habit. | `ax.scatter(x, y)`. There is no order to join. |
| **No error. Thirty-eight lines of names, and every count is `1`.** Starts `name age house club hours score` and ends `dtype: int64` | "You asked me to count *whole rows*, not clubs. Every row is different, so every count is one." | `df.value_counts()` instead of `df["club"].value_counts()`. The whole table *does* have `value_counts` — it just counts something you did not want. | Pick the column first, then count it: `df["club"].value_counts()`. Three lines out, not thirty-eight. |
| Printed output ends `Name: club, dtype: object>` with rows of club names | Nothing broke. You printed the *method*, not the result of calling it. | `print(df["club"].value_counts)` — no brackets. | Add `()`. Brackets mean "do it". |
| `ValueError: x and y must have same first dimension, but have shapes (38,) and (3,)` (the `ax.plot` wording; `ax.bar` gives `shape mismatch: objects cannot be broadcast to a single shape`, `ax.scatter` gives `x and y must be the same size`) | "38 of one thing, 3 of the other." | Mixing a raw column with a summarised one — e.g. `df["score"]` against `house_mean.values`. | Decide which level you are at: 38 rows, or 3 groups. Never both in one call. |

### How to teach debugging without giving the answer

Same ladder as Week 25 — **read the last line, name the line number, say what you expected, print the thing just before** — with one addition that is specific to this week and matters more than the ladder:

**Five of the eleven rows above produce no error at all.** So the first question is not "what does the error say?" — it is:

> **"Describe your chart to me, out loud, in one sentence."**

A student cannot describe 38 bars in three columns. They cannot describe a scribble. They cannot describe an x axis that runs from 0 to 2 in quarters. The inability to describe it is the diagnosis, and it comes from them, not from you.

---

## ❓ Questions Students Ask This Week

**"What's the actual difference between a bar chart and a histogram? They look the same."**

One rectangle means a different thing in each. In a **bar chart** one rectangle is one **category** — one club, one house, one country — and the height is a number about that category. In a **histogram** one rectangle is one **range of numbers**, and the height is *how many values landed in that range*. Two practical tells: histogram bars **touch** (because 50-to-60 touches 60-to-70) while bar-chart bars have gaps; and you can **reorder** bar-chart bars however you like, but reordering histogram bars would be like reordering a ruler. And the deepest difference: a bar chart needs two columns of data, a histogram needs one.

**"How do I know how many bins to use?"**

There is no correct answer, only bad answers on both sides. Too few bins and the shape disappears — two fat bars tell you almost nothing. Too many bins and the chart turns into grass, one value per bar. A rough starting point that professionals actually use is *about the square root of how many values you have*: 38 scores, √38 ≈ 6, so try 6 or 8. **Then do the thing that matters: change the number and look again.** If the shape stays the same when you go from 6 bins to 10, you can trust the shape. If the two humps appear at 8 bins and vanish at 5, you have found something you need to think about rather than something you can report.

**"Can I put a line on a scatter plot to show the trend?"**

Yes, and you will — in **Week 32**, when you learn what the line actually *is* and how to measure how badly it fits. Adding a line by eye now is worse than adding nothing, because a hand-drawn line looks exactly as authoritative as a calculated one and carries no information at all. For now, describe the tilt in words. "Up to the right, fairly tight" is honest. A line you guessed is not.

**"My scatter has 38 rows but I can only count about 25 dots. Is it broken?"**

Not broken — and you have just found the single most important thing this chart hides. Two students with the same hours *and* the same score land on exactly the same pixel, and the second one is invisible. Your chart looks like it has fewer students than it does. Real analysts fix this by making dots see-through (`alpha=0.5`) or nudging them slightly apart, and neither is this week's syntax. The important part is that **you noticed**, and that "some dots are hidden under other dots" now goes in your "what it hides" sentence.

**"Why can't I just put everything on one chart?"**

Because a chart answers one question, and the more you cram in the fewer questions it answers well. Four separate charts, each with a title stating one finding, are read; one chart with four things on it is looked at and put down. There is also a hard limit worth knowing: a chart can hold about three things at once — x, y, and maybe a category shown by colour or shape. Past three, nobody can hold it in their head, including you, in a month.

**"Is the mean ever safe to use?"** *(Answer honestly: people genuinely disagree about the rule.)*

**Nobody fully agrees, and here is why it is not a dodge.** Everybody agrees on the extremes. If the pile has one hump, roughly even on both sides, and the mean and median are close together, the mean is a fair summary and you should quote it. If the pile is bimodal — like our quiz marks — the mean is describing somebody who does not exist and quoting it is misleading even though the arithmetic is flawless.

The disagreement is in the middle, and it is a real professional argument. Some people say: always quote the median, because it is harder to fool, and treat the mean as a specialist tool. Others say: always quote both, and if they differ by much, that difference *is* the finding worth reporting. Others say it depends entirely on the decision — if you are working out how much food to buy for a party, you genuinely want the mean (the total is what matters); if you are describing what a typical person gets, you want the median.

What everybody agrees on is the procedure, and it is the one worth learning: **look at the shape before you pick a summary number.** Anybody who quotes a mean without having seen the distribution is guessing, however careful their arithmetic was.

**"Can a chart lie without any of the numbers being wrong?"**

Yes, easily, and that is next week's entire lesson. It is the best one of the term.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| A chart gets chosen because it "looks better" | Every 12-year-old prefers the one that looks like a proper graph, and scatter plots look sparse | Enforce the ritual physically: **the card goes on a shape card, out loud, before the laptop is touched.** Then ask for the reason. The reason is the objective; the match is not. |
| The laptop is open during Part A and typing starts immediately | Building is more fun than deciding | Close the lid. Genuinely. Part A is eight minutes long and it is the part that transfers to every future project. |
| `ax.bar(df["club"], df["score"])` draws 38 bars and gets accepted | It runs, it produces a picture, and pictures feel like success | "Describe your chart to me in one sentence." They cannot. Then: "How many rectangles should there be, and how many are there?" |
| Bar and histogram get used interchangeably all lesson | They are genuinely similar and the words are new | One physical cue, repeated: point at the **gaps**. "Gaps means categories. Touching means number ranges." Say it every single time either chart appears, all lesson. |
| The sting lands as a fun fact and not as a habit | It is a good story, and good stories feel finished | End the segment with the *action*, not the story: **"So what will you do before you ever quote an average again?"** Make them say "draw the histogram." Write it on the wall. |
| "What it hides" gets answered with "some information" | It is a hard question and vagueness is the path of least resistance | Refuse it once, kindly, and give a worked example: "Here's mine for the house chart — *it hides that Green's average came from only 12 students.* Now yours: something you could point at." |
| Scatter drawn with `ax.plot` and a scribble accepted | Last week's habit, and `plot` is the more familiar word | Same move: "Describe it." Then: "That line joins Aarav to Bela. What happened between them?" |
| Half the segment goes on bin counts | Fiddling with `bins=` is instantly rewarding and endless | Give them the √n rule of thumb and one instruction: "Try 6 and try 10. If the shape survives, move on." Then move on. |
| The student concludes "averages are lies, never use them" | Over-correcting after a good sting | Point straight back at the 38-score histogram: mean 72.1, median 72.5, one broad hump. "That mean is completely fine, and you know that because you looked." |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** four question cards instead of eight (1, 2, 3, 4 — one of each shape, no NEITHERs). One chart in Part B, not two. Cut Part C to one sentence.

**Reteach:** the sticking point is almost always bar-versus-histogram. Do it with objects, not words. Take twenty small things — coins, buttons, dried pasta. First **sort them into named groups** (coppers / silvers / others) and line up the groups with **gaps** between them: that is a bar chart, and one pile is one category. Then take the same twenty things, weigh or measure them, and sort them into ranges — 0-to-5 grams, 5-to-10, 10-to-15 — laid out **touching**, in order along the table: that is a histogram, and one pile is one range. Then ask the question that settles it: **"Can I swap two of these piles round?"** Yes for the bar chart. No for the histogram, because you would be reordering a ruler. Ninety seconds, and it usually sticks for good.

**Copy-this-exactly scaffold** — runs on its own, no `students.py` needed:

```python
# week26_scaffold.py -- copy this exactly. Then change only the CAPITALS.
import matplotlib.pyplot as plt

# --- a BAR chart: one rectangle per category ---
clubs = ["chess", "music", "art"]
members = [14, 12, 12]

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(clubs, members)
ax.set_title("MY TITLE SAYING WHICH IS BIGGEST")
ax.set_xlabel("Club")
ax.set_ylabel("Number of students (count)")
fig.savefig("my_bar.png", dpi=120, bbox_inches="tight")
print("saved my_bar.png")

# --- a HISTOGRAM: one rectangle per range of numbers ---
scores = [42, 45, 48, 52, 55, 57, 61, 64, 67, 70,
          72, 74, 78, 80, 83, 85, 88, 90, 93, 97]

fig, ax = plt.subplots(figsize=(6, 4))
counts, edges, bars = ax.hist(scores, bins=6, edgecolor="white")
print("counts:", counts, "-> adds up to", counts.sum())
ax.set_title("MY TITLE SAYING WHAT THE SPREAD LOOKS LIKE")
ax.set_xlabel("Score (points out of 100)")
ax.set_ylabel("Number of students (count)")
fig.savefig("my_hist.png", dpi=120, bbox_inches="tight")
print("saved my_hist.png")
```

```text
saved my_bar.png
counts: [3. 3. 3. 4. 3. 4.] -> adds up to 20.0
saved my_hist.png
```

**Reduce:** accept "what it hides" answers about only one chart, and accept them spoken rather than written.

**One thing you must not cut:** the sting. Twenty marks, a mean of 62, and nobody within eighteen marks of it. If the whole lesson collapses to one idea, make it **"look at the shape before you believe the average"** — and it needs no laptop, no pandas and no matplotlib. Squared paper and a pencil will do it.

### If the student is flying

1. **Round bin edges.** `bins=range(40, 101, 10)` on the scores. The counts become `3, 6, 7, 8, 8, 6`. Then the real question: "Which version would you put in front of somebody else, and why?"
2. **Histogram `age`.** It comes out as three spikes with nothing between them, because age only takes three values in this table. That is neither a smooth pile nor a bimodal one, and working out *why* is a genuinely good piece of reasoning. Follow-up: "Should age be a histogram or a bar chart? Argue it." (Either is defensible. Bar is probably better, because there are only three values and they *are* categories in practice.)
3. **Break the bin check on purpose.** `bins=range(40, 91, 10)` gives edges 40 to 90, so the five students in the 90s are silently dropped: the counts come out `3, 6, 7, 8, 9`, which adds to 33, not 38. "Five students vanished and nothing warned you. How would you ever have noticed?"
4. **Card 9, invented by them.** "Write a question about this table that none of the four shapes can answer." Strong answers: anything needing time (the table has no dates), anything needing cause, anything about individuals ("why did Greta score 42?").
5. **The overplotting count.** They have `groupby` from Week 24: `df.groupby(["age", "hours"]).size()` shows how many rows share each (age, hours) pair. There are 23 distinct pairs for 38 rows. Then: "Your scatter looks like it has 23 students. Write that in your 'what it hides' sentence."

### If the student won't engage today

Do the card game and nothing else, and do it as a game.

Deal all eight cards face down. Take turns: they draw one, you draw one. Whoever can name the shape **and** give a reason in one sentence keeps the card. Most cards wins. You are allowed to be wrong on purpose — pick BAR for card 3 and defend it badly, and let them take it off you.

That game delivers objective 1 completely, needs no computer, and takes ten minutes. Then, if there is anything left in the tank, do the twenty quiz marks on squared paper: tally them into bins of ten, draw the bars, and let them find the hole in the middle themselves. That is objective 3 as well, and it is arguably the better version of it.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the question picks the chart (spoken)**

> "'How many students are in each house?' — which chart, and why in one sentence?"

*Good answer:* A bar chart, because there are three named categories and you want to compare their heights. **What to catch:** "histogram". Ask: "How many columns of data does a histogram need?" (One. This needs names *and* counts.)

**Check 2 — bar vs histogram (spoken)**

> "I show you a chart of rectangles with no labels on it at all. Give me one thing you could look at to tell whether it's a bar chart or a histogram."

*Good answer:* whether the bars touch. Also full marks: whether the x axis has names or numbers; whether the bars could be reordered. **What to catch:** "you can't tell". Show Figure 26.3 with the labels covered — the gaps are still visible.

**Check 3 — the mean can hide the shape (spoken)**

> "A class of twenty averaged 62 out of 100. What's the one chart you'd draw before believing that, and what are you looking for?"

*Good answer:* a histogram, looking for whether the pile has one hump or two. Full marks needs the *reason* — that the average can sit in a gap where nobody actually is. **What to catch:** "a bar chart of the average". Reply: "That's one bar. What would you compare it to?"

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Picks a chart shape at random or by appearance. Cannot distinguish bar from histogram. Believes a mean without looking at the spread. |
| **2 — Emerging** | Matches obvious questions to shapes when prompted. Draws a bar or histogram from a scaffold. Confuses bar and histogram about half the time. |
| **3 — Secure** | Matches all four drawable shapes with a stated reason. Draws bar, histogram and scatter unaided, fully labelled and saved. Reads a histogram's centre, spread and shape out loud. **This is the target.** |
| **4 — Strong** | Spots that a bar chart of raw rows is wrong before running it. Describes a scatter as direction + tightness + exceptions without prompting. Names something specific that each chart hides. Recognises a bimodal pile and suggests two groups. |
| **5 — Exceptional** | Places both NEITHER cards for the right two different reasons. Notices overplotting in the scatter unprompted. Checks that histogram bin counts add up to the row count as a matter of habit. Describes a relationship without ever using a causal verb. |

---

## 📤 Homework to Assign

**Say this:**

> "The workbook this week has more in it than one evening, so here is the order.
>
> **First, finish Practice Set A, question A1.** We did the eight cards out loud; now make sure all eight have the shape **and one sentence of reason each** — that's where the marks are. Then A1(a): two of the eight are NEITHER, and they're NEITHER for two completely different reasons. I want both reasons written out.
>
> **Second, Build It — that's the main job.** Four charts from your cleaned Week 24 table. A bar chart of the club counts, a bar chart of the house averages, a histogram of the study hours, and a scatter of age against hours. All four fully labelled with units, all four saved as separate PNGs with different names. Same rules as last week: a title that says what you *found*, and units in both axis labels. Fill in the Part 1 table *before* you type anything.
>
> **Third, and this is the important one — Part 5 of Build It.** For each of those four charts, write **one sentence naming exactly what it hides.** Not 'it hides some information'. Something you could put your finger on. My example, for the house chart: *it hides that Green's average came from only twelve students.* Four charts, four specific things.
>
> The rest of the workbook — Warm-Up, Predict the Output, the other Practice questions, Fix the Broken Program, the Puzzle, Think Deeper, Draw It and the Self-Check — is for the other evenings this week. Do Predict the Output *before* you run anything, and do Fix the Broken Program with the real error messages in front of you.
>
> And read your four titles back to yourself before you hand it in. If a title would fit any chart of that data, it isn't finished."

**Workbook sections, in printed order:** Warm-Up (W1–W5) · Predict the Output (P1–P4) · Practice Set A — Read It (A1–A6) · Practice Set B — Write It (B1–B5) · Fix the Broken Program · Puzzle of the Week · Think Deeper (T1–T2) · Build It (Parts 1–6) · Draw It · Self-Check. The workbook carries **section names and item labels, not page numbers**, so this guide refers to them the same way.

**In class:** the card game is **A1** (Activity Part A); Activity Part B builds two charts that reappear inside Build It (the house-means bar is Chart 2); Part C is a first draft of Build It, Part 5.
**At home:** finish A1 and A1(a)–(c); **Build It (Parts 1–6)** is the core; everything else is spread over the week.

| Workbook section | What it is | Time (estimate) |
|---|---|---|
| Warm-Up | W1–W5 — five questions about last week's chart checklist | 5 min |
| Predict the Output | P1–P4 — `value_counts()`, do-the-bins-add-up, the missing brackets, the chart with no error | 8 min |
| Practice Set A — Read It | A1 match the question to the shape (done aloud in class, reasons finished at home) · A2 bar or histogram · A3 read a histogram out loud · A4 spot the bug · A5 label the diagram · A6 read the traceback | 20 min |
| Practice Set B — Write It | B1 one line · B2 bar chart of counts · B3 histogram with round edges · B4 scatter described in three parts · B5 four charts in one ~30-line program | 25 min |
| Fix the Broken Program | `clubroom.py`: one syntax error, one runtime error, one silent bug | 10 min |
| Puzzle of the Week | Part 1 bin detective · Part 2 wreck the histogram on purpose | 10 min |
| Think Deeper | T1 the median and the hole · T2 every chart hides something | 10 min |
| Build It | Parts 1–6: decide the shapes, build four charts, describe charts 3 and 4, four things they hide (**the bit being marked**), Bug Log | 60 min |
| Draw It | one question of their own, a hand sketch, one hidden thing | 10 min |
| Self-Check | nine "I can" ticks and twelve true/false | 5 min |

**Core time, if only the three spoken items are done:** 12 min for the A1 reasons · 35 min for the four charts · 12 min for the "what it hides" sentences. About 60 minutes. The full workbook is several evenings.

---

## 🔑 Answer Key

The answers follow the workbook's own **Answers** section, section by section and item by item; the wrong-answer maps and marking notes are the teacher-only part. Where to find each section:

| Workbook section | Where it is answered below |
|---|---|
| Warm-Up, Predict the Output | "Warm-Up and Predict the Output" |
| Practice Set A | A1 in "The eight cards"; A2–A6 in "Practice Set A, A2–A6" |
| Practice Set B | "Practice Set B" (B5 is the four-chart program under Build It) |
| Fix the Broken Program, Puzzle, Think Deeper | sections of the same names |
| Build It | "Build It — Parts 1 to 6" and "Build It, Part 5" |
| Draw It, Self-Check | sections of the same names |

### The cleaned Week 24 table, in full

If `students.py` has gone missing, this is it. Drop it in `~/ai-academy/level2`. It is the 38-row result of Week 24's Mess Detective: 40 rows came in, two were duplicates, 38 came out.

```python
# students.py -- the cleaned Mess Detective table from Week 24.
# 40 rows came in; 2 were duplicates; 38 rows came out.
import pandas as pd

def build_students():
    """Return the cleaned 38-row student table as a DataFrame."""
    rows = [
        # name,          age, house,   club,    hours, score
        ("Aarav Shah",    13, "Red",   "chess", 3.5, 72),
        ("Bela Roy",      14, "Red",   "music", 5.0, 90),
        ("Chen Wu",       13, "Blue",  "chess", 2.0, 55),
        ("Divya Nair",    13, "Blue",  "art",   4.5, 83),
        ("Emeka Obi",     13, "Green", "music", 3.0, 61),
        ("Farah Aziz",    12, "Green", "chess", 6.0, 95),
        ("Gita Menon",    13, "Blue",  "art",   1.5, 78),
        ("Hugo Silva",    14, "Red",   "music", 0.5, 45),
        ("Ivy Chen",      12, "Blue",  "chess", 4.0, 88),
        ("Jai Kapoor",    13, "Green", "art",   2.5, 67),
        ("Kira Das",      14, "Red",   "chess", 3.0, 74),
        ("Liam Byrne",    13, "Blue",  "music", 5.5, 81),
        ("Maya Iyer",     12, "Green", "art",   2.0, 59),
        ("Noor Khan",     13, "Red",   "chess", 4.0, 86),
        ("Omar Haddad",   14, "Blue",  "music", 1.0, 52),
        ("Priya Rao",     12, "Green", "art",   3.5, 70),
        ("Quinn Reid",    13, "Red",   "chess", 2.5, 64),
        ("Rhea Bose",     13, "Blue",  "music", 4.5, 92),
        ("Sami Aden",     14, "Green", "art",   0.5, 48),
        ("Tara Joshi",    12, "Red",   "chess", 5.0, 97),
        ("Uma Pillai",    13, "Blue",  "music", 3.0, 76),
        ("Viraj Sen",     14, "Green", "art",   2.0, 63),
        ("Wren Adeyemi",  12, "Red",   "chess", 3.5, 80),
        ("Xu Lin",        13, "Blue",  "music", 1.5, 57),
        ("Yara Fadel",    13, "Green", "art",   4.0, 85),
        ("Zane Cooper",   14, "Red",   "chess", 2.5, 69),
        ("Anika Verma",   12, "Blue",  "music", 5.0, 93),
        ("Bruno Costa",   13, "Green", "art",   1.0, 50),
        ("Cleo Marks",    14, "Red",   "chess", 3.0, 73),
        ("Dev Anand",     12, "Blue",  "music", 4.5, 89),
        ("Elif Demir",    13, "Green", "art",   2.0, 66),
        ("Finn Walsh",    13, "Red",   "chess", 3.5, 79),
        ("Greta Hahn",    14, "Blue",  "music", 0.5, 42),
        ("Hana Sato",     12, "Green", "art",   5.5, 91),
        ("Ismail Toure",  13, "Red",   "chess", 2.0, 62),
        ("Jia Park",      12, "Blue",  "music", 4.0, 84),
        ("Kofi Mensah",   14, "Green", "art",   1.5, 54),
        ("Lena Fischer",  13, "Blue",  "chess", 3.0, 71),
    ]
    return pd.DataFrame(
        rows, columns=["name", "age", "house", "club", "hours", "score"]
    )

if __name__ == "__main__":
    df = build_students()
    print(df.shape)
    print(df.head())
```

```text
(38, 6)
         name  age  house   club  hours  score
0  Aarav Shah   13    Red  chess    3.5     72
1    Bela Roy   14    Red  music    5.0     90
2     Chen Wu   13   Blue  chess    2.0     55
3  Divya Nair   13   Blue    art    4.5     83
4   Emeka Obi   13  Green  music    3.0     61
```

### The Hook chart

```python
# week26_hook_bad_line.py -- the chart the teacher shows in the Hook. It is WRONG.
import matplotlib.pyplot as plt
from students import build_students

df = build_students()
counts = df["club"].value_counts().sort_index()   # art, chess, music -- alphabetical
print(counts)

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(counts.index, counts.values, marker="o")  # joining CATEGORIES with a line

ax.set_title("Club membership over... over what, exactly?")
ax.set_xlabel("Club")
ax.set_ylabel("Number of students (count)")

fig.savefig("hook_bad_line.png", dpi=120, bbox_inches="tight")
print("saved hook_bad_line.png")
```

```text
art      12
chess    14
music    12
Name: club, dtype: int64
saved hook_bad_line.png
```

### Practice Set A, A1 — The eight cards (Activity Part A)

| # | Question | Shape | Reason (this is what earns the marks) |
|---|---|---|---|
| 1 | How did my homework time change day by day? | **LINE** | Time is on the bottom, it is in order, and the space between two days is real. |
| 2 | Which club has the most members? | **BAR** | Three named categories; the eye compares heights. Heights come from `value_counts()`. |
| 3 | How spread out are all 38 scores? | **HISTOGRAM** | One column of numbers, no categories, asking about the shape of the pile. |
| 4 | Do students who study more score higher? | **SCATTER** | Two number columns, asking whether they move together. One dot per student. |
| 5 | What is the average score of all 38 students? | **NEITHER** | The answer is one number, 72.1. `print` it. A single bar with nothing beside it is not an argument. |
| 6 | Which house has the highest average score? | **BAR** | Three named categories again — but the heights are averages, so `groupby("house")["score"].mean()` first, not `value_counts()`. |
| 7 | Does age go with study hours? | **SCATTER** | Two number columns again. (The answer turns out to be a *negative* tilt, which is a surprise worth having.) |
| 8 | Is the chess club better than the art club? | **NEITHER** | "Better" is not defined. Highest average? Highest lowest mark? Most members? Most consistent? Four questions, four different winners. Hand it back. |

**A1(a) Two cards are NEITHER. Why are they NEITHER for different reasons?**
Card 5 is a perfectly good, perfectly measurable question whose answer happens to be **one number** — so a chart would add nothing. Card 8 is **not measurable at all** until somebody says what "better" means; the problem is not the chart, it is the question. One needs a `print`. The other needs a conversation.

**A1(b) Cards 2 and 6 are both BAR. What is different underneath?**
Card 2's bar heights are **counts** — how many rows are in each club — from `value_counts()`. Card 6's heights are **averages** — the mean score inside each house — from `groupby`. Identical picture, completely different arithmetic, and a reader cannot tell which they are looking at unless your y-axis label says so. That is why the label reads `Mean score (points out of 100)` and not `Score`.

**A1(c) Card 1 is a LINE. What would have to change about the data for it to become a BAR?**
If the x axis stopped being ordered. "Homework minutes per **subject**" — maths, English, science — is the same kind of number on the same kind of chart, but subjects have no order and no in-between, so it becomes a bar chart. The y axis has not changed at all; the x axis decided the shape.

### In-class charts (Activity Part B)

**Bar of counts:**

```python
# week26_counts.py -- "Which club has the most members?" -> a BAR chart.
import matplotlib.pyplot as plt
from students import build_students          # the cleaned 38-row table from Week 24

df = build_students()

club_counts = df["club"].value_counts()      # count the rows for each club
print(club_counts)                           # LOOK at it before you draw it
print()
print("names :", list(club_counts.index))    # the category names
print("values:", list(club_counts.values))   # the bar heights
print("total :", club_counts.sum())          # must add back up to 38

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(club_counts.index, club_counts.values)   # one rectangle per club

ax.set_title("Chess is the biggest club: 14 of our 38 students")
ax.set_xlabel("Club")
ax.set_ylabel("Number of students (count)")

fig.savefig("club_counts.png", dpi=120, bbox_inches="tight")
print("saved club_counts.png")
```

```text
chess    14
music    12
art      12
Name: club, dtype: int64

names : ['chess', 'music', 'art']
values: [14, 12, 12]
total : 38
saved club_counts.png
```

**Histogram of scores** — the full file and output are in Live-Code Step 2 above. The counts are `[3. 4. 4. 5. 6. 5. 6. 5.]`, they add to 38, and the edges are `[42. 48.88 55.75 62.62 69.5 76.38 83.25 90.12 97.]`.

**Reading it out loud, in three parts:** *centre* — the bulk sits between about 60 and 90; *spread* — very wide, 42 all the way to 97; *shape* — one broad flat pile, no single peak, no isolated bars, so no outliers. Mean 72.1 and median 72.5 are 0.4 apart, so **this mean is safe to quote**, and the reason we know is that we looked.

**The sting** — full file and output in Live-Code Step 3. Mean 62.0, median 62.5, middle two values 44 and 81, bin counts `[6. 4. 0. 0. 0. 0. 1. 9.]`, group means 38.8 and 85.2.

**The scatter** and **the bar of house means** — full files and output in The Activity, Part B.

### Build It, Part 2 and Practice Set B, B5 ��� the four-chart program (homework)

One file, four charts. Three separate files would also be fine. This is the workbook's B5 program and the code behind Build It, Part 2.

```python
# week26_homework.py -- four charts, four shapes, from the cleaned Week 24 table.
import matplotlib.pyplot as plt
from students import build_students

df = build_students()

# --- 1. BAR: how many students in each club? -------------------------------
counts = df["club"].value_counts()
print("1 counts:", dict(counts))
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(counts.index, counts.values)
ax.set_title("Chess is the biggest club with 14 of 38 students")
ax.set_xlabel("Club")
ax.set_ylabel("Number of students (count)")
fig.savefig("hw26_1_club_counts.png", dpi=120, bbox_inches="tight")

# --- 2. BAR: which house has the highest average score? --------------------
house_mean = df.groupby("house")["score"].mean().sort_values(ascending=False)
print("2 house means:", house_mean.round(2).to_dict())
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(house_mean.index, house_mean.values)
ax.set_title("Blue and Red are level; Green is 7 points behind")
ax.set_xlabel("House")
ax.set_ylabel("Mean score (points out of 100)")
fig.savefig("hw26_2_house_means.png", dpi=120, bbox_inches="tight")

# --- 3. HISTOGRAM: how are the study hours spread out? ---------------------
fig, ax = plt.subplots(figsize=(6, 4))
counts3, edges3, bars3 = ax.hist(df["hours"], bins=6, edgecolor="white")
print("3 hour counts:", counts3, "edges:", edges3.round(2))
ax.set_title("Most students study between 2 and 5 hours a week")
ax.set_xlabel("Study hours per week")
ax.set_ylabel("Number of students (count)")
fig.savefig("hw26_3_hours_hist.png", dpi=120, bbox_inches="tight")

# --- 4. SCATTER: does age go with study hours? -----------------------------
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(df["age"], df["hours"])
ax.set_title("Older students in this table reported FEWER study hours")
ax.set_xlabel("Age (years)")
ax.set_ylabel("Study hours per week")
fig.savefig("hw26_4_age_vs_hours.png", dpi=120, bbox_inches="tight")

print("4 mean hours by age:")
print(df.groupby("age")["hours"].agg(["count", "mean"]).round(2))
print("saved four PNGs")
```

```text
1 counts: {'chess': 14, 'music': 12, 'art': 12}
2 house means: {'Blue': 74.36, 'Red': 74.25, 'Green': 67.42}
3 hour counts: [5. 8. 8. 8. 6. 3.] edges: [0.5  1.42 2.33 3.25 4.17 5.08 6.  ]
4 mean hours by age:
     count  mean
age             
12      10  4.30
13      18  2.97
14      10  1.95
saved four PNGs
```

**Chart 3, read out loud:** the hours run from 0.5 to 6.0; the three middle bins are level at 8 students each; it is one broad pile with a thin tail off the high end. Bin counts 5 + 8 + 8 + 8 + 6 + 3 = **38**. ✓

**Chart 4, the surprise.** The tilt goes **down** to the right, which nobody expects. The groupby confirms it: 12-year-olds average 4.30 hours, 13-year-olds 2.97, 14-year-olds 1.95. That is a real pattern in this table, and the honest sentence is *"older students in this table reported fewer study hours."* Not *"getting older makes you study less"* — ten fourteen-year-olds is not a generation, and there are half a dozen innocent explanations (more homework counted separately, more honest reporting, a small odd sample).

### Build It, Part 5 — What does each chart hide? (homework)

Full marks needs something you could point at. Model answers:

| Chart | What it hides — specifically |
|---|---|
| 1. bar of club counts | **Every score.** Chess has 14 members and they range from 55 to 97; the bar is a single number standing in front of a very mixed crowd. It also hides that these 38 students came from a 40-row table with two duplicates removed. |
| 2. bar of house means | **How many rows each average came from** — Blue 14, Green 12, Red 12 — and the spread inside each house. Blue's scores run 42 to 93. A mean of 12 students and a mean of 12,000 look identical on a bar chart. It also hides that Blue beats Red by **0.11 of a mark**, which is nothing at all. |
| 3. histogram of hours | **Who.** The 8 students in any one of the middle bins (for example 2.33 to 3.25 hours) could be all one club or one from each. A histogram deliberately throws away every column except one — that is what makes it readable and what makes it blind. |
| 4. scatter of age vs hours | **Dots hidden under other dots.** There are 38 rows but only **23** different (age, hours) combinations, so 15 students are invisible. The chart looks like it has 23 people in it. Three students have age 13 and 3.0 hours and they are all one dot. |

**Build It, Part 5 — Which hides the most by design, and which by accident?**
Chart 3, the histogram, hides the most **by design** — it throws away five of the six columns. Chart 4 hides the most **by accident**, and accidental hiding is the dangerous kind, because nothing on the picture warns you it is happening.

**Teacher-only, and the heart of Think Deeper T2 — is a chart that hides something a bad chart?**
No — every chart hides something, and that is what makes charts readable. The test is not "does it hide anything?" but **"does it hide something that would change what somebody decides?"** A chart that hides irrelevant detail is called clear. A chart that hides a decision-changing detail is called misleading. **The code is identical.** The difference lives entirely in what happens next.

**Teacher-only extension — pick one hidden thing and say what chart would reveal it.**
Model answer: chart 2 hides the spread inside each house. A **histogram of Blue's scores alone** would reveal it, or three histograms side by side. (The chart actually designed for that job is a **box plot**, which is the fifth shape — you will meet it by name this year and draw it later.)

### Warm-Up and Predict the Output

**Warm-Up (last week's checklist).**

| # | Answer | Watch for |
|---|---|---|
| W1 | **`fig`.** You save the whole sheet of paper, not one drawing on it; `ax.savefig(...)` does not exist. | "Either" or "`ax`". Ask what would happen with two drawings on one sheet. |
| W2 | Whether there is a `fig.savefig(...)` line at all, then **look in the folder** (`ls` on macOS or Linux, `dir` on Windows). The absence of the file is the diagnosis. | Staring at the terminal. Nothing was broken; the program was obedient. |
| W3 | Any title that states a finding, e.g. "Screen time trebled on Saturday, then dropped back." Test: could the title sit unchanged on *any* chart of that data? If yes, it is a filename. | A rewording of the filename ("Chart of screen time"). |
| W4 | The **units** (the scale). Repaired: `"Score (points out of 100)"`. | "Nothing is missing", or adding only a capital letter. |
| W5 | A line through 4 points and a line through 400 points can look identical, and the two deserve very different amounts of **trust**; without the dots the reader cannot tell how much to give. | A sentence about looks ("it looks nicer") with no mention of trust. |

**Predict the Output.**

| # | Real output and answer | Watch for |
|---|---|---|
| P1 | Output: `chess 14`, `music 12`, `art 12`, `Name: club, dtype: int64`, then `14`, `chess`, `3`. `counts["chess"]` looks up by name; `counts.index[0]` is the first name in the result; `len(counts)` is the number of different clubs (**3**, not 38). Slot 0 is the biggest club because **`value_counts()` sorts biggest-first automatically**; it is not alphabetical (use `.sort_index()` for that). | Predicting `38` for `len(counts)`; predicting `art` for `counts.index[0]`. |
| P2 | Output: `counts: [5. 1. 2. 2.]`, `sum   : 10.0`, `edges : [50.   55.25 60.5  65.75 71.  ]`. **Five edges for four bins** (four fence panels, five posts). 71 goes into the **last** bin; the counts sum to 10 because matplotlib always includes the top value in the last bin. | Predicting four edges. Predicting 71 is dropped (the sum of 10 disproves it). |
| P3 | **Not an error.** It prints `<bound method IndexOpsMixin.value_counts of 0      art ...>`, a description of the method itself, not the result. Fix: add the brackets, `clubs.value_counts()`. Brackets mean "do it". Tie to Week 17: `runs.shape` needs no brackets (a fact about the thing); `value_counts()` does (a job it performs). | Predicting a `TypeError`. |
| P4 | Output: `rectangles drawn: 38`, `clubs in the table: 3`, `saved oops.png`. **No crash.** 38 rectangles crammed into three columns. "Describe it in one sentence?" No, and that is the point: when nothing errors, the diagnosis is your own inability to say what the chart shows. | Predicting an error, or "a bar chart of the clubs". |

### Practice Set A, A2–A6

(A1 is "The eight cards" above.)

**A2 — bar or histogram?**

| # | The clue | Answer |
|---|---|---|
| a | gaps between the rectangles | **Bar chart** |
| b | rectangles touching | **Histogram** |
| c | exactly three rectangles | **Cannot tell** (a histogram with `bins=3` is legal) |
| d | x numbers at the **edges** | **Histogram** (a bar chart labels the middle of each bar) |
| e | x labels are words | **Bar chart** |
| f | swapping two would still make sense | **Bar chart** (reordering a histogram is reordering a ruler) |
| g | rectangles get taller then shorter | **Cannot tell** (plenty of bar charts do that too) |

**A2(h).** **(a)/(b), whether the bars touch.** It works with every label covered, in a photocopy, in a newspaper photo. (d) and (f) are just as logical but need the axis read or the meaning thought about. Accept (d) or (f) with a reason, but half marks if the reason is only "I remember it".

**A3 — read a histogram out loud.** **38 values**, because the eight counts add up: 3+4+4+5+6+5+6+5 = 38 (the free check). **Centre:** the bulk is between about 60 and 90 (the four middle bins hold 5, 6, 5 and 6, which is 22 of the 38). **Spread:** very wide, 42 to 97, a range of 55. **Shape:** one broad, flat pile, no single peak (tallest bin is 6), no isolated bars, **no gap**; which is why mean 72.1 and median 72.5 are 0.4 apart and both trustworthy.

- **A3(i).** **matplotlib chose them**: it took the lowest (42) and highest (97) values and split the 55-point gap into eight equal slices of 6.875. Nothing in the arithmetic asked for round numbers.
- **A3(j).** 3 + 6 + 7 + 8 + 8 + 6 = **38**. Which version for somebody else? The round one, because you can say it out loud ("three in the forties, six in the fifties..."). Accept the opposite (the automatic bins use the full range with no wasted space) if the reason is argued.

**A4 — spot the bug.**

| # | The line | The fix |
|---|---|---|
| a | `counts.value` | `counts.values`, **with an s** |
| b | `ax.bar(club_counts)` | `ax.bar(club_counts.index, club_counts.values)`: bars need where *and* how tall |
| c | `ax.bar(df["club"], df["score"])` | Summarise first: `value_counts()` or `groupby(...).mean()` |
| d | `ax.hist(df["club"], bins=8)` | A histogram needs **numbers**; bar-chart the text column instead |
| e | `ax.scatter(df["hours"])` | `ax.scatter(df["hours"], df["score"])`: a dot needs two coordinates |
| f | `ax.plot(..., marker="o")` | `ax.scatter(x, y)`: there is no order to join |
| g | `print(df["club"].value_counts)` | Add the brackets: `value_counts()` |
| h | `df.value_counts()` | `df["club"].value_counts()`: pick the column **first** |

- **A4(i).** The five with **no error** are **c, d, f, g and h**. c gives 38 bars in three columns; d turns three words into 0, 1, 2 and bins those; f joins 38 dots into a scribble; g prints a `<bound method ...>` line; h prints 38 lines each with a count of 1. (a, b and e raise real errors.)
- **A4(j).** **"Describe my chart to me, out loud, in one sentence."** If you cannot, that is the bug report. It works on all five silent ones and needs no tools.

**A5 — label the diagram.** A = the 18 raw values, one dot each · B = one bin, one range of values · C = the bin's count becomes the bar's height · D = a bin edge, where one range stops and the next starts · E = the counts must add up to 18. **A5(f):** **E** is the check, not a part; do it **every time** you draw a histogram, before you read the shape, because if the counts do not add up the shape you are about to read is a shape of the wrong data.

**A6 — read the traceback.**

- **Which line first?** The **last** one. The middle lines are the route Python took through pandas' own code.
- **A `'Series'`** is **one column** (here, the little result `value_counts()` handed back). A whole table is a `DataFrame`.
- **Is the suggestion right?** **Yes**: `values` is what you meant.
- **The rule:** `index` has no s; `values` has an s. No reason; write it in the Bug Log.
- **Read the pandas file?** **No.** It only shows where inside somebody else's library the error surfaced. The only line that is about your program is the one naming your own filename.

### Practice Set B

**B1.** `print(df["house"].value_counts())`, which prints:

```text
Blue     14
Red      12
Green    12
Name: house, dtype: int64
```

14 + 12 + 12 = 38. **Watch for:** `df.value_counts()` (the A4(h) trap) or `df["house"].value_counts` with no brackets.

**B2 — bar chart of counts.** Core lines: `counts = df["club"].value_counts()`, then `print(counts)` and `print("total:", counts.sum())` **before drawing**, then `ax.bar(counts.index, counts.values)`, a title that states a finding, both axis labels with units, `fig.savefig("my_club_counts.png", ...)`.

```text
chess    14
music    12
art      12
Name: club, dtype: int64
total: 38
saved my_club_counts.png
```

Model title: "Chess is the biggest club: 14 of 38, two ahead of the others". Credit "two ahead" as the honest version of "chess wins": the gap is small and the title says so. **Watch for:** `counts.value` (A6), a title like "Club counts", a y label of just "Count".

**B3 — histogram with round edges.** Core lines: `counts, edges, bars = ax.hist(df["score"], bins=range(40, 101, 10), edgecolor="white")`, then print `counts`, `counts.sum()` and `edges`.

```text
counts: [3. 6. 7. 8. 8. 6.]
sum   : 38.0
edges : [ 40.  50.  60.  70.  80.  90. 100.]
saved my_score_hist.png
```

The `101` matters (Week 7's off-by-one): `range(40, 100, 10)` stops at 90 and silently drops the nineties (see Puzzle, Part 2). Spoken shape: three in the forties, six in the fifties, seven in the sixties, eight in the seventies, eight in the eighties, six in the nineties: one broad flat pile.

**B4 — scatter in three parts.** Core lines: `print("rows:", len(df))`, `ax.scatter(df["hours"], df["score"])` with **no line**, title e.g. "Students who studied more hours tended to score higher", x label "Study hours per week", y label "Score (points out of 100)".

```text
rows: 38
saved my_scatter.png
```

Model sentences: **Direction:** up to the right. **Tightness:** a fairly tight band, not a blob. **Exception:** one dot at about 1.5 hours and 78 sits well above its neighbours. Check it: three students studied exactly 1.5 hours and scored **78, 57 and 54**, a 24-mark spread at the same x. **Verbs:** "tended to go with", never "caused" (Week 27 is about why).

**B5.** The four-chart program is printed above under "Build It, Part 2 and Practice Set B, B5". Marking checks: four different filenames, each title states a finding, units on both axes, chart 2's y label says **Mean**, and the printed output matches the block above (`{'chess': 14, 'music': 12, 'art': 12}`, `{'Blue': 74.36, 'Red': 74.25, 'Green': 67.42}`, hour counts `[5. 8. 8. 8. 6. 3.]`, ages 12, 13, 14 averaging 4.30, 2.97, 1.95).

### Fix the Broken Program

The program is `clubroom.py`; it has three bugs (line numbers below are the file's own).

**Bug 1, the syntax error.** `SyntaxError: '(' was never closed`, pointing at line 10. **Is the mistake on line 10?** **Yes, this time**, because the missing `)` is on the same line as the opening bracket (in Week 17 the bracket was closed five lines later and Python still pointed at the opening). **Did any of it run?** **No**: no `Traceback` and the `print(counts)` on line 8 produced nothing. No traceback and no earlier output means Python never started your program. **Fix:** add one closing bracket:

```python
fig, ax = plt.subplots(figsize=(6, 4))
```

**Bug 2, the runtime error.** The run ends `AttributeError: 'Series' object has no attribute 'value'. Did you mean: 'values'?` on line 11, `ax.bar(counts.index, counts.value)`. **The counts printed before the crash**, which proves they are fine (chess 14, music 12, art 12, total 38). That is what printing before drawing buys you. **Fix:**

```python
ax.bar(counts.index, counts.values)
```

**Bug 3, the silent one.** The output has edges `[0.   0.25 0.5  0.75 1.   1.25 1.5  1.75 2.  ]`. **What is 0.75 of a house?** Nothing. **Do the counts add up to 38?** Yes, 12 + 14 + 12, so **the counts are not wrong**; the chart is nonsense, which is what makes it nasty. **What is wrong** is line 19, `ax.hist(df["house"], bins=8)`: a histogram of a **text** column. matplotlib turned the house names into 0, 1 and 2 and binned those. **Is anything on the chart a score?** No; the title says "Scores run from 42 to 97" and the x label says "Score (points out of 100)" while the x axis runs 0 to 2: three labels, all lying, no error. **Fix:**

```python
spread, edges, bars = ax.hist(df["score"], bins=8, edgecolor="white")
```

Real output after the fix:

```text
chess    14
music    12
art      12
Name: club, dtype: int64
saved clubs.png
counts: [3. 4. 4. 5. 6. 5. 6. 5.]
edges : [42.    48.875 55.75  62.625 69.5   76.375 83.25  90.125 97.   ]
saved spread.png
```

**The check that catches this family:** print the counts **and the edges** and read the edges; if they are not numbers your column could contain, you histogrammed the wrong column.

**Bonus, what order did matplotlib use?** The order the names **first appear in the table**: row 0 Aarav Shah is Red (0), row 2 Chen Wu is Blue (1), row 4 Emeka Obi is Green (2). Hence 12, 14, 12 (Red, Blue, Green). Not alphabetical, not by size: a third reason not to do this.

**Marking tips:** full marks on Bug 1 needs the "never started" reasoning, not just the bracket. The usual slip on Bug 3 is "the counts are wrong"; they are right.

### Puzzle of the Week

**Part 1, bin detective.**

- **(a)** 3 + 4 + 5 + 3 + 3 = **18 values**.
- **(b)** Each bin is **10 wide**; there are **5 bins** (six edges, five gaps).
- **(c)** **Nine**: the 20-to-30 bin holds 4 and the 30-to-40 bin holds 5.
- **(d)** **Yes**: 55 falls in the last bin, 50-to-60, which holds 3 values.
- **(e)** **No value of 7 is in this histogram**: it is below the lowest edge, 10. Strictly a 7 could have existed and been silently dropped, but then the counts would not add up to the 18 that were counted in.
- **(f)** You **cannot** know the smallest value, only that it is somewhere in 10 to 20. A histogram tells you how many, not which.
- **(g)** The **middle** bin, 30-to-40, holds the most at 5. Shape: one hump, roughly symmetric (3, 4, **5**, 3, 3).
- **(h)** **No, the mean cannot be checked from the histogram alone.** You can bracket it: all values at their bins' low edges gives 3(10) + 4(20) + 5(30) + 3(40) + 3(50) = 530, and 530 / 18 = **29.4**; all at the high edges gives 3(20) + 4(30) + 5(40) + 3(50) + 3(60) = 710, and 710 / 18 = **39.4**. So the mean must be between 29.4 and 39.4; 31 is **possible but not confirmed** (you have failed to rule it out). The values behind the histogram were `12, 15, 18, 21, 24, 25, 27, 31, 33, 34, 36, 38, 41, 44, 47, 52, 55, 58`, real mean 33.9, inside the bracket and not 31.

**Part 2, wreck the histogram on purpose.**

- **(i)** Six students scored 90 or more: Bela Roy (90), Farah Aziz (95), Rhea Bose (92), Tara Joshi (97), Anika Verma (93), Hana Sato (91). With edges stopping at 90, Bela's exactly-90 is **kept** (in the last bin, 80 to 90) and the other **five are dropped**.
- **(j)/(k)** Real output:

```text
counts: [3. 6. 7. 8. 9.] sum 33.0
```

  Sum 33, not 38: five students gone and nothing said a word. You only notice by printing `counts.sum()` and comparing it with `len(df)`; the sum is the only witness.
- **(l)** With edges stopping at 90, the value 90 lands in the *last* bin (80-to-90) instead of the 90-to-100 bin, so 8 becomes 9; the other five nineties vanish. Two lessons: the top edge behaves differently from the others, and a bin range that does not cover your data silently deletes rows.

### Think Deeper

**T1 (model answer).** The median is the middle value **by position**, so it is robust to **extreme values** (change one 33 to a 3 and the middle person does not move). It has no defence against a **hole in the middle**: with ten marks in the thirties and forties and ten in the eighties, the tenth and eleventh values are 44 and 81 and the median sits in the empty canyon between them. It is robust to outliers, not to shape. Of the three rules, "quote both, and if they differ that difference is the finding" would not have helped here, because 62.0 and 62.5 agreed; it catches skew and misses bimodality. The procedure that works: look at the shape before you pick a summary.

**Marking note:** full marks needs "robust to outliers, not to shape" (or equivalent) **and** the honest admission that the chosen rule has a cost.

**T2 (model answer).** A chart is readable because it throws things away (the score histogram discarded five of six columns). So the difference between clear and misleading is not *whether* it hides something but *what*. Example: the house-means bar chart (Blue 74.36, Red 74.25, Green 67.42) hides how many students each average came from (14, 12, 12) and that Blue beats Red by 0.11 of a mark; a prize given to Blue on that chart would turn on a hidden, meaningless gap, while the same code showing Green is well behind hides nothing that matters. The code cannot tell the difference, so the chart-maker writes the caption: one sentence on what it shows and one on what it hides.

**Marking note:** the key move is naming a **specific decision** that the hidden thing would change. "Somebody might be misled" is half marks; "Blue would get the prize on a 0.11 gap" is full marks.

### Build It — Parts 1 to 6

**Part 1, decide before you type.**

| Chart | Shape | Which columns |
|---|---|---|
| 1. Which club has the most members? | **BAR** | `club` (then `value_counts()`) |
| 2. Which house has the highest average score? | **BAR** | `house` and `score` (then `groupby(...).mean()`) |
| 3. How are the study hours spread out? | **HISTOGRAM** | `hours` only |
| 4. Does age go with study hours? | **SCATTER** | `age` and `hours` |

**Which chart needs only one column?** **Chart 3, the histogram**: just `hours`. Chart 1 needs `club` plus the counting; charts 2 and 4 need two columns each. Charts 1 and 2 are the same shape but need different arithmetic (counts versus means), which is why chart 2's y label says **Mean**.

**Part 2, build them.** Check column: chart 1 counts total **38**; chart 2 row counts printed too (**14, 12, 12**); chart 3 bins total **38**; chart 4 dots one can count: **about 23**.

**Chart 4: 38 rows, about 23 dots.** The difference is **overplotting**: students with the same age *and* the same hours land on the same spot, so the second is invisible. One line of Week 24 code shows it:

```python
print(len(df.groupby(["age", "hours"]).size()))
```

```text
23
```

Only 23 different (age, hours) pairs for 38 students, so 15 are hidden under others (three students share age 13 and 3.0 hours and show as one dot). Real analysts use `alpha=0.5` or nudge the dots apart; neither is this week's syntax, the point is that the student noticed.

**Part 3, chart 3 described.** **Centre:** the bulk is between about 1.4 and 4.2 hours (the three middle bins hold 8 each). **Spread:** 0.5 to 6.0 hours, fairly wide. **Shape:** one broad pile with a thin tail off the high end; no gap, no second hump. **Is the mean safe to quote?** **Yes**: one hump, no gap, median inside the bulk, and they know it because they looked at the shape first.

**Part 4, chart 4 described.** **Direction:** down to the right; older students in this table reported **fewer** hours (12-year-olds average 4.30, 13-year-olds 2.97, 14-year-olds 1.95). **Tightness:** loose; because age takes only three values, the dots sit in three vertical stripes that overlap heavily (12s run 2.0 to 6.0 hours, 13s 1.0 to 5.5, 14s 0.5 to 5.0). **Exceptions:** any 14-year-old with high hours, e.g. 5.0 hours (Bela Roy), or a 12-year-old with 2.0. **"Caused" count:** the target is **0**; accept "tended to", "goes with", "reported".

**Part 5, four things they hide.** See "Build It, Part 5" above for the model table, the by-design versus by-accident answer and the "which is more dangerous" reasoning (the accidental one, Chart 4, because it hides a different number of students depending on the data and nothing on the picture warns you).

**Part 6, the Bug Log.** Personal; there is no single answer. Full marks: at least one real row with an honest "was there an error message?" (a good entry is the silent `value_counts` without brackets, or `counts.value`) and a *check* in the last column, not just the fix.

### Draw It

There is no single right drawing. A good one has **one ticked shape with a written reason**, a sketch whose **bars touch if it is a histogram and have gaps if it is a bar chart**, and a "what it hides" box naming something a reader could point at. The two tells that it is right: the counts above the bars **add up to the number of things in the dataset**, and the hidden thing is specific enough to argue about. A weak answer: a histogram with gaps, or with names along the x axis (the chart matplotlib will draw without complaining).

### Self-Check

The "I can" ticks are the student's own; compare them against your Mastery scale. True or false:

| Statement | Answer | Why |
|---|---|---|
| A histogram needs two columns of data | **FALSE** | **One** column of numbers |
| Histogram bars touch; bar-chart bars have gaps | **TRUE** | 50-to-60 touches 60-to-70; art does not touch chess |
| You can reorder the bars of a histogram | **FALSE** | That would be reordering a ruler |
| `ax.hist(df["club"], bins=8)` raises an error | **FALSE** | No error; words become 0, 1, 2 and are binned |
| `counts.index` has an s on the end | **FALSE** | `index` has none; `values` has one |
| `ax.bar(df["club"], df["score"])` gives one bar per club | **FALSE** | One bar per **row**: 38, in three columns |
| A scatter plot should have a line joining the dots | **FALSE** | A line says you travelled from one dot to the next in order |
| A histogram's bin counts must add up to the number of values | **TRUE** | If not, rows fell outside your bins and vanished silently |
| If the mean and median agree, the mean is safe to quote | **FALSE** | The quiz marks were 62.0 and 62.5 and both misled; agreement is not shape |
| A distribution with two humps usually means two groups mixed together | **TRUE** | It is called **bimodal**; go and look for the two groups |
| "Which club is best?" can be answered with one bar chart | **FALSE** | Not until "best" is defined |
| Every chart hides something | **TRUE** | The question is whether the hidden thing changes a decision |

### Lesson questions posed in the Say-this scripts

- *"Have I missed anything on this chart?"* → No, by last week's checklist it is complete. Which is the point: the checklist was not enough.
- *"What does the line between art and chess mean?"* → Nothing. There is no journey from one to the other.
- *"What is halfway between art and chess?"* → Nothing exists there.
- *"If I shuffle the three names, does the chart change?"* → Completely. Six orderings, six different lines, none meaningful. If reordering x changes the shape, the shape is wrong.
- *"So when is a line the right shape?"* → When x is ordered **and** the in-between is real: days, weeks, ages, temperatures.
- *"'How many students in each house?' — which shape?"* → Bar. Named categories, compare heights.
- *"'How are the 38 scores spread out?' — which shape?"* → Histogram. One number column, asking about shape.
- *"How do you tell a bar chart from a histogram?"* → Gaps between the bars, and whether x holds names or numbers.
- *"Bins add up to 34 but you have 38 rows — what happened?"* → Four values fell outside the bin range and were silently dropped.
- *"'Which club is best?' — which shape?"* → NEITHER. Define "best" first.
- *"Guess the average of these twenty marks."* → It is 62.0. Whatever they guessed, the reveal is that nobody scored near it.
- *"How many people scored between 44 and 81?"* → Nobody. Not one.
- *"Why did the median fail here?"* → It landed in the empty gap between the two clumps. The median is robust to *outliers*, not to *shape*.
- *"What does two humps usually mean?"* → Two different groups mixed together. Here: ten who had done Level 1, ten who had not.
- *"When should you trust a mean?"* → After you have looked at the shape and found one hump, roughly even, with the median close by.
- *"Blue is 74.36 and Red is 74.25. Is Blue better?"* → No. A gap of 0.11 of a mark across twelve students is nothing, and no three-bar chart can tell you otherwise.

---

## 🔮 Next Week Preview

Week 27 is the Term 3 checkpoint, and it is the most enjoyable lesson of the term because the student spends it **lying on purpose**. Two bars, 49% and 51% — a two-point difference, about as small as a difference gets. Then one argument to one function, and the second bar becomes six times taller than the first, and the student measures both bars with an actual ruler in millimetres to prove it. Not one number changes. Nothing is faked. Then they build the honest version beside it in the same figure, learn the one call that names two lines on a chart, and finish with the hardest question of the term: study hours and marks have a correlation of 0.93, so **who gets hurt if a school acts on that chart?**

**Prep early:** four things. Keep every PNG from this week and last — Week 27 sabotages one of them on purpose. **Find a ruler with millimetres on it**, a real one; the measuring is not a metaphor and the arithmetic depends on it. Make sure the printer works, because the lie has to be measured on paper, not on a screen where you can zoom. And if you have ten spare minutes before the lesson, go and find a misleading chart in the wild — a news site, an advert, a phone's battery graph — because Week 27 ends by asking the student to catch somebody at it, and having one in your pocket makes that land.

---

[⬅ Week 25](week-25.md) · [Course Home](../README.md) · [Week 27 ➡](week-27.md) · [Student Guide](../student-guide/week-26.md) · [Workbook](../workbook/week-26.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)

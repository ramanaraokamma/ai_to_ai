# Module 7 — Charts That Tell The Truth: Visualization With Matplotlib

**Level 2 · Module 7 · ~3.5 hours · Prereqs: Modules 1–6 (Python basics, functions, lists, numpy arrays, pandas DataFrames, `groupby`)**

[⬅ Previous](module-06-pandas-tables.md) · [Level 2 Home](README.md) · [Next ➡](module-08-first-model-knn.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** look at a question and choose the right chart type for it — line, bar, scatter, histogram, or box — and say *why* in one sentence.
2. **You will be able to** produce a fully labelled matplotlib chart with a title, axis labels that name the units, sensible ticks, and a legend, then save it to a `.png` file.
3. **You will be able to** read a distribution off a histogram (centre, spread, shape, outliers) and read a relationship off a scatter plot (direction, strength, exceptions).
4. **You will be able to** spot a misleading chart, name the exact trick — truncated axis, cherry-picked range, missing baseline — and rebuild an honest version of it.
5. **You will be able to** explain, with a concrete example, why two things moving together does not mean one causes the other.

---

## 🪝 The Hook

In Module 6 you printed this:

```
house
Blue     74.36
Green    67.42
Red      74.25
```

Three numbers. Nobody argues with three numbers, because nobody *reads* three numbers.

Now imagine two people take those exact same three numbers and each draw a bar chart. The first one draws bars starting at zero. The bars look nearly identical — Green is 91% as tall as Blue. Her caption reads: *"Houses perform about the same."*

The second one starts the y-axis at 65. Now Blue's bar is **almost four times taller** than Green's. His caption reads: *"Blue house dominates. Green needs urgent intervention."*

**Same data. Same arithmetic. Opposite conclusions.** Nobody lied. Nobody typed a wrong number. One person just moved where the axis starts.

A chart is not a picture of data. **A chart is an argument.** This module teaches you to make honest arguments — and to catch dishonest ones before you retweet them.

---

## 🧠 The Concept

### 0. Getting matplotlib

```bash
pip install matplotlib
```

Then, at the top of every file in this module:

```python
import matplotlib.pyplot as plt   # the plotting tool; "plt" is the universal nickname
import pandas as pd               # from Module 6
import numpy as np                # from Module 5
```

`matplotlib.pyplot` is a mouthful. Everyone in the world abbreviates it to `plt`. Do the same.

Two ways your chart can appear:

| Where you're working | What to do |
|---|---|
| A `.py` file in VS Code / terminal | End with `plt.show()` — a window pops up. Close it to let the program finish. |
| A Jupyter notebook | Charts appear under the cell automatically. `plt.show()` is optional but harmless. |
| A machine with no screen (a server) | Use `fig.savefig("chart.png")` and open the file. |

> 📌 **Version note:** every line in this module works on matplotlib 3.4 and newer. One function, `ax.bar_label()`, was added in 3.4. Check with `print(matplotlib.__version__)` if a label refuses to appear.

---

### 1. Chart choice: five question shapes, five charts

Here's the mistake almost everybody makes: they decide "I'll make a bar chart" and *then* look for something to put in it. Backwards. **The question picks the chart.**

🍕 **Analogy.** You don't choose a spoon and then hunt for food that suits a spoon. You look at the soup, and the spoon is obvious. Look at your question, and the chart is obvious.

Five question shapes cover almost everything you'll ever need:

| Your question sounds like… | Chart | What the eye reads |
|---|---|---|
| "How did X change **over time**?" | **line** | the slope — up, down, flat, bumpy |
| "Which **category** is biggest?" | **bar** | the height of each bar, side by side |
| "Do X and Y **go together**?" | **scatter** | the cloud's tilt and tightness |
| "What do the values **look like all together**?" | **histogram** | the shape of the pile — centre, spread, lumps |
| "How **spread out** is each group?" | **box** | the box's height and the whiskers' reach |

Let's make each one concrete.

**Line — "over time."**

> **Line chart** — points joined in time order, so the eye follows a path.

You count how many people visit the school library each week for 12 weeks: 118, 126, 131, 140, 152, 149, 158, 171, 166, 158, 174, 189. A line chart shows a climb from 118 to 189 with two dips along the way. Week order matters, so the points get joined.

⚠️ Only join points when the x-axis has a *natural order*. Joining "chess", "music", "art" with a line implies chess flows into music. It doesn't.

**Bar — "compare categories."**

> **Bar chart** — one rectangle per category; height encodes the value.

Mean score by house: Blue 74.36, Red 74.25, Green 67.42. Three bars. The eye compares heights instantly. **Bars must start at zero**, because the eye reads *area and length*, and a bar that starts at 65 has had 65 units of its length secretly deleted.

**Scatter — "relationship."**

> **Scatter plot** — one dot per row, placed at (x, y); the shape of the cloud is the answer.

Study hours on x, score on y, one dot per student. If the dots slope up-and-right, more hours goes with higher scores. If it's a shapeless blob, there's no relationship worth talking about.

**Histogram — "distribution."**

> **Histogram** — chops one numeric column into ranges (bins) and shows how many values landed in each.

Take 38 scores. Chop 40–100 into six bins of width 10. Count how many scores fall in each bin. The bars now tell you where the crowd is. **A histogram has one variable, not two** — that's the single biggest difference from a bar chart.

**Box — "spread per group."**

> **Box plot** — a compact five-number summary: minimum, lower quartile, median, upper quartile, maximum, plus dots for outliers.

Three clubs, three boxes. A tall box means the group is all over the place. A short box means everyone is similar. This is the chart for the question *"yes, but how consistent are they?"*

Here's a decision flowchart you can tape above your desk:

```
                    What is my question?
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   about TIME?         about GROUPS?        about TWO NUMBERS?
        │                    │                    │
      LINE          ┌────────┴────────┐        SCATTER
                    │                 │
              "which is        "how spread out
               biggest?"        is each one?"
                    │                 │
                   BAR               BOX

        (only ONE column of numbers, no groups?  →  HISTOGRAM)
```

---

### 2. Anatomy of a figure: figure, axes, labels, ticks, legend

Matplotlib has two styles of writing code. You will see both online. Learn the second one.

```python
# Style A — "pyplot state machine". Short, but it hides WHERE things go.
plt.plot([1, 2, 3], [4, 5, 6])
plt.title("Something")

# Style B — "object-oriented". Slightly longer, and always obvious. USE THIS.
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
ax.set_title("Something")
```

🍕 **Analogy.** The **figure** is the sheet of paper. The **axes** is one drawing frame on that paper. A sheet can hold several frames side by side. `plt.subplots()` hands you both: the paper and the frame.

> **Figure** — the whole image file. **Axes** — one plotting box inside it, with its own x-axis, y-axis, and title. (Confusingly, "axes" here means the *box*, not the two lines. Blame 2003.)

Here is every part you're responsible for:

```
   ┌──────────────────────────────── figure (the whole PNG) ─────────────────┐
   │                                                                          │
   │            Library visits climbed 60% over one term      ← ax.set_title  │
   │      200 ┤                                    ●                          │
   │          │                              ●                                │
   │ Visits   │                        ●  ●     ●        ┌──────────┐         │
   │ per week │                  ●  ●                    │ ● visits │ ←legend │
   │ (count)  │            ●  ●                          └──────────┘         │
   │  ↑       │      ●  ●                                                     │
   │ ax.set_  │  ●                                                            │
   │ ylabel   └──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──                          │
   │             1  2  3  4  5  6  7  8  9 10 11 12   ← ticks (ax.set_xticks) │
   │                  School week (week 1 = start of term)  ← ax.set_xlabel   │
   │                                                                          │
   └──────────────────────────────────────────────────────────────────────────┘
                     the inner box is the AXES
```

The eight lines you should write for *every* chart, in this order:

```python
fig, ax = plt.subplots(figsize=(8, 4.5))   # 1. paper + frame, size in inches
ax.plot(weeks, visits, marker="o")         # 2. draw the data
ax.set_title("...")                        # 3. what is the takeaway?
ax.set_xlabel("... (units)")               # 4. what is x, in what units?
ax.set_ylabel("... (units)")               # 5. what is y, in what units?
ax.set_ylim(0, 200)                        # 6. control the range on purpose
ax.legend()                                # 7. only if there's more than one series
fig.tight_layout()                         # 8. stop labels being chopped off
fig.savefig("visits.png", dpi=150)         #    and/or plt.show()
```

**A title should state the finding, not the ingredients.** "Visits vs week" is a filename. "Library visits climbed 60% over one term" is a title. If your title could sit on top of *any* chart of that data, it isn't doing work.

**Units belong in the axis label.** `"Score"` is ambiguous. `"Score (points out of 100)"` cannot be misread. `"Distance"` could be metres or kilometres; `"Distance to school (km)"` could not.

🔍 **Tiny example.** These two calls draw identical pixels of data:

```python
ax.set_ylabel("Score")                       # reader has to guess
ax.set_ylabel("Score (points out of 100)")   # reader knows
```

The second one takes four extra seconds to type and removes an entire category of misunderstanding.

---

### 3. Distributions, outliers, and why the mean can lie

A **distribution** is just "the whole pile of values, and how they're arranged."

> **Distribution** — the pattern of how often each value (or range of values) occurs.

You already know two summary numbers from Module 6: the mean and the median. Here's the thing they don't tell you: **an average is one number standing in front of a crowd, and the crowd can be any shape.**

🍕 **Analogy.** Ten kids are in a room. The average pocket money is ₹115 a week. Sounds comfortable. Here are the actual amounts:

```
₹20, ₹25, ₹30, ₹20, ₹35, ₹25, ₹30, ₹40, ₹25, ₹900
```

Nine kids get between ₹20 and ₹40. One kid gets ₹900.

- **Mean** = (20+25+30+20+35+25+30+40+25+900) ÷ 10 = 1150 ÷ 10 = **₹115**
- **Median** = sort them → 20, 20, 25, 25, **25, 30**, 30, 35, 40, 900 → middle two are 25 and 30 → **₹27.50**

The mean says ₹115. **Not one single kid gets anywhere near ₹115.** The mean is describing a person who does not exist.

> **Outlier** — a value far away from the rest of the data. It might be a mistake, or it might be the most interesting thing in the dataset.

The ₹900 is an outlier. It drags the mean up by ₹87.50 all by itself. The median barely notices, because the median only cares about *position in the sorted list*, not size.

| Statistic | Value | Moved by one outlier? |
|---|---|---|
| Mean | ₹115.00 | Yes — enormously |
| Median | ₹27.50 | Barely |

**A histogram is how you catch this before you embarrass yourself.** Print the mean and you see ₹115. Draw the histogram and you see nine bars huddled at the left and one lonely bar at ₹900, and the problem is unmissable in half a second.

Three things to read off every histogram:

1. **Centre** — where's the bulk?
2. **Spread** — narrow pile or wide pile?
3. **Shape** — one hump? two humps (a **bimodal** distribution — two different groups mixed together)? a long tail on one side?

🔍 **Tiny example — bins matter.** The same 38 scores, binned two ways:

- Bins of width 10 (`40–50, 50–60, …`) → counts `3, 6, 7, 8, 8, 6`. A wide, fairly flat pile.
- Bins of width 30 (`40–70, 70–100`) → counts `16, 22`. Two fat bars that tell you almost nothing.

Too few bins hides the shape. Too many bins turns the chart into grass. Start with about `√n` bins (here √38 ≈ 6) and adjust until the shape stops changing.

---

### 4. Visual lies: how to bend a chart without changing a number

Nobody sophisticated fakes data. Faking data is risky and checkable. **The clever way to mislead is to draw true numbers dishonestly.** Here are the five you'll meet most often.

#### Lie 1 — The truncated y-axis

> **Truncated axis** — an axis that starts somewhere other than zero, so small differences look enormous.

Our three house means: Blue 74.36, Red 74.25, Green 67.42.

**Honest version, y from 0 to 100:**
Green's bar height ÷ Blue's bar height = 67.42 ÷ 74.36 = **0.907**. Green is 91% as tall as Blue. They look nearly the same, because they nearly *are* the same.

**Truncated version, y from 65 to 76:**
Now each bar only shows the part above 65.
- Blue's visible height = 74.36 − 65 = **9.36**
- Green's visible height = 67.42 − 65 = **2.42**
- Ratio = 9.36 ÷ 2.42 = **3.87**

Blue's bar is now **almost four times taller** than Green's. Every number printed on that chart is correct. The chart is still a lie, because a bar chart asks your eye to compare lengths, and 65 units of length have been quietly deleted from every bar.

```
   y from 0 (honest)              y from 65 (the trick)
   100┤                            76┤ ███
      │ ███ ███ ███                  │ ███ ███
      │ ███ ███ ███                  │ ███ ███
      │ ███ ███ ███                  │ ███ ███
      │ ███ ███ ███                  │ ███ ███ ███
    0 └──────────────              65 └──────────────
      Blue Red Green                  Blue Red Green
   "about the same"               "Blue DOMINATES"
```

**The rule:** bar charts must start at zero. Line charts *may* start elsewhere — a temperature graph starting at 0 K would be absurd — but if you truncate a line chart you must say so loudly in the label, e.g. `"Temperature (°C) — note axis starts at 20"`.

#### Lie 2 — The cherry-picked range

Our library series over 12 weeks:

```
week:   1    2    3    4    5    6    7    8    9   10   11   12
visits: 118  126  131  140  152  149  158  171  166  158  174  189
```

Full story: 118 → 189, a **+60.2% rise**.

Now show only weeks 8, 9, 10: `171 → 166 → 158`. A clean downhill line. Headline: *"Library use is collapsing — down 7.6% in a fortnight."* Every number true. The chart is a lie by omission.

**The tell:** a chart whose x-range starts and ends at strange places. If a chart of a 12-week term shows you exactly weeks 8–10, ask what weeks 1–7 and 11–12 looked like.

#### Lie 3 — The missing baseline (what should we compare to?)

"Our new study app users scored 72 on average!" Is 72 good? Compared to what? Without last year's number, or the non-app group's number, 72 is not evidence of anything. A single bar standing alone is almost never an argument.

#### Lie 4 — The 3-D pie chart, and pies in general

Pie slices are compared by **angle**, and human eyes are terrible at angles. Tilt the pie into 3-D and the front slices grow, because they're closer to the viewer. Two categories that are actually 30% and 28% can look like 40% and 20%. If you have more than about three categories, use a bar chart. If you were about to add a 3-D effect: don't.

#### Lie 5 — Dual y-axes

Two lines, two different y-scales, one chart. By choosing the two scales, you can make almost any pair of series look like they move together. If you see two y-axes, treat the "they track each other perfectly!" claim as unproven until you check the scales.

**Your checklist for any chart you meet in the wild:**

```
  □ Does the y-axis start at zero?  (must, for bars)
  □ What's the full time range, and why does it stop where it stops?
  □ Are the units stated?
  □ How many data points is each bar/point based on?
  □ Compared to what?  Where's the baseline?
  □ Who made this, and what would they like me to believe?
```

---

### 5. Correlation is not causation

> **Correlation** — a measurement of how strongly two numbers move together, from −1 (perfect opposite) through 0 (no relationship) to +1 (perfect together).

In our student data, study hours and score have a correlation of **r = 0.925**. That's very strong. The scatter plot is a tidy up-and-right line of dots.

Tempting conclusion: *"studying more causes higher scores."*

Maybe! But a strong correlation is consistent with **four** different worlds, and the scatter plot cannot tell you which one you're in:

| World | What's really happening | Example |
|---|---|---|
| **A causes B** | Studying really does raise scores | plausible here |
| **B causes A** | Doing well makes studying feel rewarding, so you do more | also plausible |
| **C causes both** | A quiet home with a desk causes both more study hours *and* higher scores | the **confounder** |
| **Coincidence** | With enough variables, some pair will line up by luck | very common |

> **Confounder** — a hidden third thing that causes both of the two things you measured, making them look connected to each other.

🍕 **Analogy.** Ice cream sales and drowning deaths rise together almost perfectly. Ice cream does not cause drowning. **Hot weather** causes both: people buy ice cream *and* people swim. Hot weather is the confounder.

🔍 **Tiny example with numbers.** Suppose across six months:

| Month | Ice creams sold | Drownings |
|---|---|---|
| Jan | 200 | 1 |
| Mar | 400 | 2 |
| May | 800 | 5 |
| Jul | 1400 | 9 |
| Sep | 900 | 6 |
| Nov | 300 | 2 |

Sales and drownings rise and fall together — the correlation is near +0.99. If you banned ice cream, would drownings stop? Obviously not. The chart is perfectly accurate and the causal story is nonsense.

**How to talk honestly about a scatter plot:** say *"students who studied more tended to score higher"* — a description. Don't say *"studying raised scores"* — a claim about cause, which needs an experiment (randomly assign some students to study more) not a chart.

---

## 🔍 Worked Example

Let's build one histogram completely by hand and then check it against matplotlib, and then do the truncated-axis arithmetic in full.

### Part 1 — A histogram, by hand

Here are all 38 scores from the cleaned Module 6 table, already sorted:

```
42, 45, 48, 50, 52, 54, 55, 57, 59, 61, 62, 63, 64, 66, 67, 69, 70, 71, 72,
73, 74, 76, 78, 79, 80, 81, 83, 84, 85, 86, 88, 89, 90, 91, 92, 93, 95, 97
```

**Step 1 — choose bins.** √38 ≈ 6.2, so aim for about 6 bins. The data runs 42 to 97, so bins of width 10 from 40 to 100 give exactly 6 bins:

```
[40,50)  [50,60)  [60,70)  [70,80)  [80,90)  [90,100]
```

The square bracket means "included", the round bracket means "excluded". So 50 goes in the **second** bin, not the first. (The last bin includes 100 — matplotlib closes the final bin on the right.)

**Step 2 — count each bin. Cross values off as you go.**

| Bin | Values that land here | Count |
|---|---|---|
| 40–50 | 42, 45, 48 | **3** |
| 50–60 | 50, 52, 54, 55, 57, 59 | **6** |
| 60–70 | 61, 62, 63, 64, 66, 67, 69 | **7** |
| 70–80 | 70, 71, 72, 73, 74, 76, 78, 79 | **8** |
| 80–90 | 80, 81, 83, 84, 85, 86, 88, 89 | **8** |
| 90–100 | 90, 91, 92, 93, 95, 97 | **6** |
| | **total** | **38** ✅ |

The counts add to 38, which is the number of students. **Always check this.** If your bin counts don't add to `len(data)`, a value fell through a crack.

**Step 3 — sketch it.**

```
 count
   8 ┤              ███  ███
   7 ┤        ███   ███  ███
   6 ┤   ███  ███   ███  ███  ███
   5 ┤   ███  ███   ███  ███  ███
   4 ┤   ███  ███   ███  ███  ███
   3 ┤██ ███  ███   ███  ███  ███
   2 ┤██ ███  ███   ███  ███  ███
   1 ┤██ ███  ███   ███  ███  ███
   0 └───────────────────────────────
     40  50   60    70   80   90  100
              Score (points out of 100)
```

**Step 4 — read it out loud.** "The scores are spread very wide, from 42 to 97. There's no single tall peak — the middle four bins are all similar height. Slightly more students sit in the 70s and 80s than anywhere else. There are no isolated bars, so no outliers."

**Step 5 — check the centre.**
- Mean = sum ÷ 38 = 2741 ÷ 38 = **72.13**
- Median = average of the 19th and 20th sorted values = (72 + 73) ÷ 2 = **72.5**

Mean and median are 0.37 apart. **When mean ≈ median, the distribution is roughly symmetric and the mean is safe to quote.** (Compare with the pocket-money example, where they were ₹115 and ₹27.50 — a red flag the size of a building.)

**Step 6 — confirm with matplotlib.**

```python
import numpy as np
scores = np.array([42,45,48,50,52,54,55,57,59,61,62,63,64,66,67,69,70,71,72,
                   73,74,76,78,79,80,81,83,84,85,86,88,89,90,91,92,93,95,97])
counts, edges = np.histogram(scores, bins=range(40, 101, 10))
print(counts)   # [3 6 7 8 8 6]
print(edges)    # [ 40  50  60  70  80  90 100]
print(scores.mean(), np.median(scores))   # 72.13157894736842 72.5
```

Output:

```
[3 6 7 8 8 6]
[ 40  50  60  70  80  90 100]
72.13157894736842 72.5
```

Your hand counts and the computer agree exactly. 🎉

### Part 2 — The truncated axis, in full arithmetic

Three house means: **Blue 74.36, Red 74.25, Green 67.42.**

**Honest chart, y-axis 0 → 100.** The axis is 100 units tall. Suppose it's drawn 400 pixels high, so 1 unit = 4 pixels.

| House | Value | Bar height in pixels | Height as % of Blue |
|---|---|---|---|
| Blue | 74.36 | 74.36 × 4 = 297.4 px | 100.0% |
| Red | 74.25 | 74.25 × 4 = 297.0 px | 99.9% |
| Green | 67.42 | 67.42 × 4 = 269.7 px | **90.7%** |

Green's bar is 91% of Blue's. The honest visual message: *these are nearly the same.*

**Truncated chart, y-axis 65 → 76.** The axis is now only 11 units tall, but still drawn 400 pixels high, so 1 unit = 400 ÷ 11 = 36.36 pixels.

| House | Value | Value above 65 | Bar height in pixels | Height as % of Blue |
|---|---|---|---|---|
| Blue | 74.36 | 9.36 | 9.36 × 36.36 = 340.4 px | 100.0% |
| Red | 74.25 | 9.25 | 9.25 × 36.36 = 336.4 px | 98.8% |
| Green | 67.42 | 2.42 | 2.42 × 36.36 = 88.0 px | **25.9%** |

Green's bar is now **26%** of Blue's — it looks nearly four times smaller (9.36 ÷ 2.42 = 3.87×).

**The damage, in one sentence:** a real difference of 9.3% has been drawn as an apparent difference of 74.1%, an exaggeration factor of about **8×**, purely by deleting 65 units from the bottom of every bar.

**The fix:** `ax.set_ylim(0, 100)`. One argument. That's the whole repair.

---

## 💻 Hands-On

We'll build the whole toolkit on one dataset, then make the lie-and-fix pair.

### Setup — the data, typed in once

This is the Module 6 "Mess Detective" table, already cleaned: 38 rows, duplicates removed, house names standardised, ages repaired. Put this in a file called `students.py` so you can import it everywhere.

```python
# students.py — the cleaned dataset from Module 6, ready to use.
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
    # Runs only when you execute this file directly, not when you import it.
    df = build_students()
    print(df.shape)
    print(df.head())
```

Run it once to check:

```bash
python students.py
```

```
(38, 6)
         name  age  house   club  hours  score
0  Aarav Shah   13    Red  chess    3.5     72
1    Bela Roy   14    Red  music    5.0     90
2     Chen Wu   13   Blue  chess    2.0     55
3  Divya Nair   13   Blue    art    4.5     83
4   Emeka Obi   13  Green  music    3.0     61
```

### Chart 1 — Line: how did library use change over the term?

```python
# chart1_line.py
import matplotlib.pyplot as plt

# Week numbers 1..12 and the count of library visits in each week.
weeks = list(range(1, 13))
visits = [118, 126, 131, 140, 152, 149, 158, 171, 166, 158, 174, 189]

fig, ax = plt.subplots(figsize=(8, 4.5))     # one figure, one axes, 8x4.5 inches

ax.plot(
    weeks, visits,                # x values, y values
    marker="o",                   # put a dot on each real measurement
    color="#1f77b4",              # matplotlib's default blue, chosen on purpose
    linewidth=2,
    label="Library visits",       # the text the legend will show
)

ax.set_title("Library visits climbed 60% over one term")
ax.set_xlabel("School week (week 1 = start of term)")
ax.set_ylabel("Visits per week (count)")
ax.set_ylim(0, 200)               # start at zero — nothing to hide
ax.set_xticks(weeks)              # a tick for every week, not every other one
ax.grid(axis="y", alpha=0.3)      # faint horizontal guides help the eye
ax.legend()

fig.tight_layout()                # keeps labels from being cut off
fig.savefig("chart1_line.png", dpi=150)
plt.show()
```

**Caption to write under it:** *Library visits rose from 118 in week 1 to 189 in week 12, a 60% increase, despite dips in weeks 6 and 10.*

Notice `marker="o"`. Without markers, a line chart hides how many real measurements exist — a smooth line drawn through 3 points looks identical to one drawn through 300.

### Chart 2 — Bar: which house scores highest?

```python
# chart2_bar.py
import matplotlib.pyplot as plt
from students import build_students

df = build_students()

# groupby from Module 6: mean score per house, biggest first.
house_mean = df.groupby("house")["score"].mean().sort_values(ascending=False)
print(house_mean.round(2))

fig, ax = plt.subplots(figsize=(7, 4.5))

bars = ax.bar(
    house_mean.index,                        # category names: Blue, Red, Green
    house_mean.values,                       # bar heights
    color=["#1f77b4", "#d62728", "#2ca02c"], # blue, red, green — matching the names
)

# Print the exact value on top of each bar (matplotlib >= 3.4).
ax.bar_label(bars, fmt="%.1f", padding=3)

ax.set_ylim(0, 100)                          # THE honesty line: bars start at zero
ax.set_title("Average score is nearly identical across houses")
ax.set_xlabel("House")
ax.set_ylabel("Mean score (points out of 100)")

fig.tight_layout()
fig.savefig("chart2_bar.png", dpi=150)
plt.show()
```

Expected printed output:

```
house
Blue     74.36
Red      74.25
Green    67.42
Name: score, dtype: float64
```

**Caption:** *Blue (74.4) and Red (74.3) are tied; Green averages 67.4, about 7 points lower — a real but modest gap, and Green is only 12 students.*

### Chart 3 — Scatter: do study hours go with scores?

```python
# chart3_scatter.py
import matplotlib.pyplot as plt
from students import build_students

df = build_students()

fig, ax = plt.subplots(figsize=(7, 5))

# One scatter call per club, so the legend can name them.
for club, colour, marker in [("chess", "#1f77b4", "o"),
                             ("music", "#d62728", "s"),
                             ("art",   "#2ca02c", "^")]:
    sub = df[df["club"] == club]        # boolean filter from Module 6
    ax.scatter(
        sub["hours"], sub["score"],
        c=colour, marker=marker, s=60,  # s = dot area in points^2
        label=club, edgecolors="white",
    )

r = df["hours"].corr(df["score"])       # Pearson correlation, -1 .. +1

ax.set_title(f"More study hours goes with higher scores (r = {r:.2f})")
ax.set_xlabel("Study hours per week")
ax.set_ylabel("Score (points out of 100)")
ax.legend(title="Club")
ax.grid(alpha=0.3)

fig.tight_layout()
fig.savefig("chart3_scatter.png", dpi=150)
plt.show()

print(f"correlation = {r:.3f}")
```

Expected printed output:

```
correlation = 0.925
```

**Caption:** *Students who studied more hours tended to score higher (r = 0.93). This is an association, not proof that studying caused the scores.*

Read that caption again. The word "tended" and the sentence about causation are not decoration — they are the difference between an honest chart and an overclaim.

### Chart 4 — Histogram: what does the spread of scores look like?

```python
# chart4_hist.py
import matplotlib.pyplot as plt
from students import build_students

df = build_students()

fig, ax = plt.subplots(figsize=(7, 4.5))

counts, edges, patches = ax.hist(
    df["score"],
    bins=range(40, 101, 10),   # explicit bin edges: 40,50,60,70,80,90,100
    color="#4c72b0",
    edgecolor="white",         # white gaps make the bins countable
)
print("counts:", counts)
print("edges: ", edges)

# Vertical reference lines for the two summary numbers.
ax.axvline(df["score"].mean(), color="#d62728", linestyle="--", linewidth=2,
           label=f"mean = {df['score'].mean():.1f}")
ax.axvline(df["score"].median(), color="#2ca02c", linestyle=":", linewidth=2,
           label=f"median = {df['score'].median():.1f}")

ax.set_title("Scores spread from 42 to 97 with no single peak")
ax.set_xlabel("Score (points out of 100)")
ax.set_ylabel("Number of students")
ax.set_xticks(range(40, 101, 10))
ax.legend()

fig.tight_layout()
fig.savefig("chart4_hist.png", dpi=150)
plt.show()
```

Expected printed output:

```
counts: [3. 6. 7. 8. 8. 6.]
edges:  [ 40.  50.  60.  70.  80.  90. 100.]
```

Those counts are exactly the ones you worked out by hand. **Caption:** *Scores are widely spread with no dominant band; mean (72.1) and median (72.5) nearly coincide, so the average is a fair summary here.*

### Chart 5 — Box: which club is most consistent?

```python
# chart5_box.py
import matplotlib.pyplot as plt
from students import build_students

df = build_students()

order = ["art", "chess", "music"]
# One list of scores per club, in a fixed order we control.
data = [df.loc[df["club"] == club, "score"].values for club in order]

fig, ax = plt.subplots(figsize=(7, 4.5))

ax.boxplot(data, showmeans=True)   # showmeans adds a triangle for the mean
ax.set_xticks([1, 2, 3])           # boxplot positions start at 1, not 0
ax.set_xticklabels(order)

ax.set_title("Music has the widest spread; chess has the highest middle")
ax.set_xlabel("Club")
ax.set_ylabel("Score (points out of 100)")
ax.grid(axis="y", alpha=0.3)

fig.tight_layout()
fig.savefig("chart5_box.png", dpi=150)
plt.show()

print(df.groupby("club")["score"].agg(["count", "mean", "std", "min", "max"]).round(2))
```

Expected printed output:

```
       count   mean    std  min  max
club                                
art       12  67.83  14.07   48   91
chess     14  76.07  12.26   55   97
music     12  71.83  19.23   42   93
```

Read the box plot: the **line inside each box** is the median (art 66.5, chess 73.5, music 78.5). The **box** spans the middle 50% of students. The **whiskers** reach out to the rest.

Here's the twist the bar chart would have hidden completely: **music has the highest median (78.5) but by far the widest spread (std 19.2, from 42 all the way to 93).** Chess has a lower median but everyone in it clusters tightly. "Which club is better?" now has two different answers depending on whether you care about the typical member or about reliability.

> 📌 **Version note:** on matplotlib 3.9+ you can write `ax.boxplot(data, tick_labels=order)`. On older versions the keyword was `labels=`. Setting `set_xticks` then `set_xticklabels`, the way this script does, works on every version.

### The lie and its fix, side by side

```python
# chart6_lie_and_fix.py
import matplotlib.pyplot as plt
from students import build_students

df = build_students()
house_mean = df.groupby("house")["score"].mean().sort_values(ascending=False)

# One figure, two axes side by side. axes is a numpy array of length 2.
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

# ---- LEFT: the misleading version -------------------------------------
axes[0].bar(house_mean.index, house_mean.values, color="#d62728")
axes[0].set_ylim(65, 76)                       # <-- THE TRICK
axes[0].set_title("MISLEADING: 'Blue crushes Green'")
axes[0].set_xlabel("House")
axes[0].set_ylabel("Mean score")               # no units, on purpose

# ---- RIGHT: the honest version ----------------------------------------
axes[1].bar(house_mean.index, house_mean.values, color="#4c72b0")
axes[1].set_ylim(0, 100)                       # <-- THE FIX
axes[1].set_title("HONEST: same numbers, axis from 0")
axes[1].set_xlabel("House")
axes[1].set_ylabel("Mean score (points out of 100)")

fig.suptitle("The same three numbers, drawn two ways", fontsize=13)
fig.tight_layout()
fig.savefig("chart6_lie_and_fix.png", dpi=150)
plt.show()

# Print the arithmetic so the trick is undeniable.
blue, green = house_mean["Blue"], house_mean["Green"]
print(f"honest height ratio  green/blue = {green/blue:.3f}")
print(f"truncated ratio      blue/green = {(blue-65)/(green-65):.2f}x")
```

Expected printed output:

```
honest height ratio  green/blue = 0.907
truncated ratio      blue/green = 3.87x
```

Put those two panels next to each other and show them to somebody. Watch them react to the left one before they read the axis. That reaction is exactly the thing you are learning to defend against.

---

## ✍️ Practice

Use `students.py` for anything that needs the student table.

### 1. [Warm-up] Label a naked chart

Here is a chart with nothing on it:

```python
import matplotlib.pyplot as plt
temps = [22, 24, 27, 31, 34, 33, 30, 28, 26, 23]
days = list(range(1, 11))
fig, ax = plt.subplots()
ax.plot(days, temps)
plt.show()
```

Add: a title that states the finding (not "temps"), an x-label with units, a y-label with units, markers on the points, a y-limit starting at 0, x-ticks on every day, and a `savefig` to `temps.png`.

**Done looks like:** a saved `temps.png` where a stranger could describe what the chart says without asking you a single question, and your title mentions the peak of 34 °C on day 5.

### 2. [Warm-up] Mean vs median detective

Given these 9 daily step counts:

```python
steps = [4200, 5100, 4800, 5300, 4600, 5000, 4900, 5200, 41000]
```

Compute the mean and the median by hand (show your arithmetic), then confirm with numpy. Draw a histogram with `bins=10`. Write one sentence saying which summary number you'd quote to a friend and why.

**Done looks like:** mean = 8900.0, median = 5000, a histogram with one bar at the far right and a nearly-empty middle, and a sentence naming the 41000 as an outlier (probably a bike ride logged as steps).

### 3. [Build] Right chart for each question

For each of these five questions about the student table, (a) name the chart type, (b) write one sentence saying why, and (c) build it fully labelled and save it as a PNG.

1. "How many students are in each club?"
2. "Is age related to study hours?"
3. "How are study hours distributed across all 38 students?"
4. "Which house has the most variable scores?"
5. "Do older students study more, and does that differ by house?"

**Done looks like:** five saved PNGs; question 1 is a bar chart of `value_counts()` (art 12, chess 14, music 12), question 3 is a histogram, question 4 is a box plot grouped by house, and question 5 is a scatter with colour by house and a legend. Question 2 has a surprise in it — report the correlation you actually get, not the one you expected.

### 4. [Build] Build a lie, then confess

Take the club means (`art 67.83, chess 76.07, music 71.83`). Produce a two-panel figure:

- Left panel: use **two** tricks at once — a truncated y-axis starting at 66, and a y-label with no units.
- Right panel: the honest fix.

Under the figure, print a short paragraph naming each trick and giving the exaggeration factor as a number.

**Done looks like:** a saved PNG, and printed text stating that the honest chess/art height ratio is 1.12× while the truncated ratio is (76.07−66)/(67.83−66) = 5.50×, an exaggeration of about 4.9×.

### 5. [Stretch] The cherry-pick challenge

Using the 12-week library series, write a function `cherry_pick(weeks, visits, start, end)` that plots only weeks `start..end` and prints the percentage change over that window.

Then find, in code (not by eye), the 3-week window with the **most negative** percentage change, and the 3-week window with the **most positive**. Plot both windows and the full series in a 1×3 figure with honest titles for each panel.

**Done looks like:** the worst window is weeks 8–10 (171 → 158, −7.6%), the best is weeks 10–12 (158 → 189, +19.6%), all three panels share the same y-limits so they can be compared, and your titles say "weeks 8–10 only" rather than pretending to show the whole term.

### 6. [Stretch] Correlation without causation, built by you

Invent a dataset of 12 rows with two columns that will correlate strongly but where one obviously does not cause the other, plus a third column that is the confounder. (Example skeleton: month → `ice_cream_sold`, `drownings`, `avg_temp_c`.) Type the numbers in literally.

Then produce a 1×3 figure: X vs Y, X vs confounder, Y vs confounder. Print all three correlations. Write three sentences explaining what the confounder does.

**Done looks like:** all three correlations above 0.9, three labelled scatter panels, and a written explanation that names the confounder and says what experiment (not chart) would be needed to test causation.

---

## 🤔 Think Deeper

### 1. Every chart hides something. What did your five charts hide?

*How to reason about it:* pick your bar chart of house means and list everything the reader **cannot** see: the number of students per house, the spread inside each house, the individual student who scored 42, whether the houses had the same clubs available. Now ask: for each hidden thing, would showing it change what a reader would decide? A chart that hides only irrelevant detail is called "clear". A chart that hides a decision-changing detail is called "misleading", and the code is identical. The difference is entirely in what decision it will feed.

### 2. Is a truncated axis *always* dishonest?

*How to reason about it:* imagine a chart of your body temperature over a week, in °C. Starting at zero would compress every meaningful variation into a flat line at the top. Now imagine a chart of a company's monthly revenue starting at 95% of its maximum. Same technique, different verdict. Try to find the actual rule that separates them — think about whether the reader is comparing *lengths* (bars) or following a *shape* (lines), and whether the value zero is meaningful for that quantity at all. Then ask what a chart owes a reader who only sees it for two seconds in a group chat.

### 3. You found r = 0.93 between study hours and score. Who might be harmed if a school acted on that chart?

*How to reason about it:* trace the chain from chart to consequence. Someone sees the scatter, concludes "more hours → higher score", and mandates two extra study hours for everyone. Now think about which students in your table already study 5.5–6 hours, which study 0.5, and *why* the 0.5 group might study so little — a job, caring for a sibling, no quiet room. Ask whether the policy helps them or punishes them for a circumstance the chart never measured. Then ask whether the *confounder* (quiet home) is something a school could act on instead, and why that action is less popular.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Chart window pops up and the program hangs | `plt.show()` blocks until you close the window | Close the window, or use `fig.savefig(...)` instead in scripts |
| All five charts land on top of each other in one image | You never closed or created a new figure | Use `fig, ax = plt.subplots()` per chart, and `plt.close(fig)` after saving |
| Axis labels are chopped off at the edge of the PNG | Default margins are too tight for long labels | `fig.tight_layout()` before `savefig` |
| `ax.legend()` prints "No artists with labels found" | You never passed `label="..."` to the plot call | Add `label=` to every `plot`/`scatter`/`bar` you want in the legend |
| A bar chart where the shortest bar looks 4× shorter than it is | `set_ylim` was left to matplotlib, which auto-truncates | Always `ax.set_ylim(0, something)` for bar charts |
| A histogram with 2 bars, or 60 bars | Default bin count doesn't fit your data | Pass `bins=range(lo, hi+step, step)` explicitly; start near √n bins |
| Using a bar chart when you meant a histogram | Both look like rectangles | Bar = one bar per **category**; histogram = one bar per **numeric range** of a single column |
| A line chart joining "art", "chess", "music" | You reached for `plot` out of habit | Categories have no order — use `ax.bar` |
| Colours that vanish for a colour-blind reader | Red-vs-green was the first pair you thought of | Vary marker shape too (`o`, `s`, `^`), and prefer blue/orange over red/green |
| Title says "Score vs House" | You described the ingredients instead of the finding | Retitle to the conclusion: "Houses score within 7 points of each other" |
| `ValueError: x and y must have same first dimension` | Your two lists are different lengths | `print(len(x), len(y))` — usually one list is missing a comma |
| `plt.bar(df["house"], df["score"])` draws 38 bars | You passed raw rows instead of a group summary | `df.groupby("house")["score"].mean()` first |

---

## 🛠️ Mini-Project — Five-Chart Data Story

### Goal

Answer **one** question about the student dataset using **five** fully labelled charts arranged so they read in order like a story — then build one deliberately misleading chart and its honest fix, side by side, and explain the trick.

Suggested question (or invent your own): **"Which club should the school invest in next year?"**

### Starter steps

**Step 1 — write the question at the top of the file (5 min).**
Literally, as a comment. Then write the *decision* the question feeds: "the school has money for one club's equipment." A question with no decision behind it produces charts with no point.

**Step 2 — plan the five charts before writing any plotting code (15 min).**
Fill in this table on paper first:

| # | Chart | What it shows | Why it comes here in the story |
|---|---|---|---|
| 1 | bar | how many students in each club | set the scale — how many people are affected |
| 2 | histogram | spread of all scores | show the baseline before splitting by club |
| 3 | box | score spread per club | the heart of the argument |
| 4 | scatter | hours vs score, coloured by club | is club effect really an effort effect? |
| 5 | bar | mean hours per club | the possible confounder, shown honestly |

Notice the shape of the story: **context → baseline → main finding → challenge to the finding → the caveat.** A story that only shows the flattering chart is an advertisement, not an analysis.

**Step 3 — build them (60 min).**
One function per chart, all in one file:

```python
# story.py
import matplotlib.pyplot as plt
from students import build_students

df = build_students()


def chart1_club_sizes(df):
    counts = df["club"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(counts.index, counts.values, color="#4c72b0")
    ax.bar_label(bars, padding=2)
    ax.set_ylim(0, 16)
    ax.set_title("Chess is the biggest club (14 of 38 students)")
    ax.set_xlabel("Club")
    ax.set_ylabel("Number of students")
    fig.tight_layout()
    fig.savefig("story_1_sizes.png", dpi=150)
    plt.close(fig)
    return counts


# ... write chart2_score_distribution, chart3_score_by_club,
#     chart4_hours_vs_score, chart5_hours_by_club the same way ...

if __name__ == "__main__":
    print(chart1_club_sizes(df))
```

**Step 4 — write a one-sentence caption per chart (15 min).**
The caption states the **takeaway**, not the contents. Collect all five captions at the bottom of your file as a printed summary — read together they should form a paragraph that makes sense with no charts at all.

**Step 5 — build the lie-and-fix pair (20 min).**
Pick any one of your five and sabotage it with exactly one named trick. Put the sabotaged and honest versions in a 1×2 figure. Print the exaggeration factor as a number.

**Step 6 — write the verdict (10 min).**
Three to five sentences answering your original question, including at least one sentence beginning "I am *not* confident that…".

### Success criteria checklist

- [ ] All five charts saved as separate PNG files
- [ ] Every chart has a title that states a finding, not a topic
- [ ] Every axis label names the quantity **and its units**
- [ ] Every chart with more than one series has a legend
- [ ] All bar charts start at y = 0
- [ ] Five captions, one sentence each, that read as a paragraph in order
- [ ] A 1×2 lie-and-fix figure with the trick named in the title
- [ ] The exaggeration factor printed as an actual number
- [ ] A written verdict including one honest statement of uncertainty
- [ ] Every chart is based on a group of at least 10 rows, or the small `n` is stated in the caption

### Level it up

**Grid the whole story into one poster.** Use `fig, axes = plt.subplots(3, 2, figsize=(12, 13))` to place all five charts plus a text panel on a single figure, then `fig.savefig("story_poster.png", dpi=150)`. You will immediately hit the two hard problems of multi-panel layout: shared axis ranges (so panels are comparable) and label collisions (`fig.tight_layout()` and `figsize` are your tools). For the text panel, use `axes[2,1].axis("off")` and then `axes[2,1].text(0.0, 0.5, your_verdict, wrap=True, fontsize=10)`.

---

## 🔑 Key Takeaways

- **The question chooses the chart.** Time → line. Categories → bar. Two numbers → scatter. One numeric column → histogram. Spread per group → box.
- **A title states the finding; an axis label states the units.** If your title would fit any chart of that data, rewrite it.
- **Bar charts start at zero, always.** Truncating a bar axis turned a real 9% gap into an apparent 74% gap in this module — an 8× exaggeration with one line of code.
- **The mean is one number standing in front of a crowd.** Draw the histogram before you quote the average; if mean and median disagree badly, an outlier is steering the ship.
- **Same numbers, different framing, opposite conclusion.** Cherry-picked ranges, missing baselines, 3-D pies and dual axes all lie without falsifying a single value.
- **Correlation describes; it never explains.** r = 0.93 between hours and score is consistent with four different stories, and a scatter plot cannot tell you which.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **figure** | The whole picture file you save | The 8×4.5-inch PNG holding your line chart |
| **axes** | One drawing box inside a figure, with its own x, y and title | The left panel of your lie-and-fix pair |
| **line chart** | Dots joined in time order so you can follow a path | Library visits across 12 weeks |
| **bar chart** | One rectangle per category; taller means bigger | Mean score for Blue, Red, Green |
| **scatter plot** | One dot per row, at (x, y); the cloud's shape is the answer | Study hours vs score, 38 dots |
| **histogram** | Chops one number column into ranges and counts each range | 38 scores into six bins of width 10 |
| **bin** | One of the ranges a histogram counts into | The `[70, 80)` bin holds 8 students |
| **box plot** | A five-number summary drawn as a box with whiskers | Score spread for art, chess, music |
| **median** | The middle value when everything is sorted | 72.5 for the 38 scores |
| **outlier** | A value sitting far away from all the others | ₹900 among nine kids getting ₹20–₹40 |
| **distribution** | The whole shape of the pile of values | "Wide, flat, no single peak, 42 to 97" |
| **truncated axis** | An axis that doesn't start at zero, so gaps look huge | y from 65 makes a 9% gap look like 74% |
| **cherry-picking** | Showing only the slice of time that supports your point | Weeks 8–10 of a 12-week rise |
| **correlation (r)** | A number from −1 to +1 for how strongly two things move together | r = 0.93 for hours vs score |
| **confounder** | A hidden third thing that causes both things you measured | Hot weather causes both ice cream sales and swimming |
| **caption** | One sentence under a chart saying what it means | "Blue and Red are tied; Green is 7 points lower." |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1. [Warm-up] Label a naked chart

```python
import matplotlib.pyplot as plt

temps = [22, 24, 27, 31, 34, 33, 30, 28, 26, 23]
days = list(range(1, 11))

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(days, temps, marker="o", color="#d62728", linewidth=2,
        label="Daily high")

ax.set_title("Temperature peaked at 34 °C on day 5, then cooled steadily")
ax.set_xlabel("Day of the heatwave (day 1 = first hot day)")
ax.set_ylabel("Daily high temperature (°C)")
ax.set_ylim(0, 40)          # zero baseline; 0 °C is meaningful for weather here
ax.set_xticks(days)         # a tick on every day, not every second day
ax.grid(axis="y", alpha=0.3)
ax.legend()

fig.tight_layout()
fig.savefig("temps.png", dpi=150)
plt.show()
```

**Why the title works:** it names the peak value (34), the location of the peak (day 5), and the shape after it (cooling). A stranger who never sees the chart still learns the finding.

**A note on `set_ylim(0, 40)`:** this is a case where zero *is* defensible — 0 °C is a real, meaningful reference point (freezing). If these were Kelvin, starting at zero would be silly. If these were bars, zero would be compulsory.

---

### 2. [Warm-up] Mean vs median detective

**By hand.**

Sum: 4200 + 5100 = 9300; + 4800 = 14100; + 5300 = 19400; + 4600 = 24000; + 5000 = 29000; + 4900 = 33900; + 5200 = 39100; + 41000 = **80100**.

Mean = 80100 ÷ 9 = **8900.0**

Sorted: 4200, 4600, 4800, 4900, **5000**, 5100, 5200, 5300, 41000.
There are 9 values, so the median is the 5th one = **5000**.

**Confirm with code.**

```python
import numpy as np
import matplotlib.pyplot as plt

steps = np.array([4200, 5100, 4800, 5300, 4600, 5000, 4900, 5200, 41000])

print("mean  :", steps.mean())          # 8900.0
print("median:", np.median(steps))      # 5000.0

fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(steps, bins=10, color="#4c72b0", edgecolor="white")
ax.axvline(steps.mean(), color="#d62728", linestyle="--", linewidth=2,
           label="mean = 8900")
ax.axvline(np.median(steps), color="#2ca02c", linestyle=":", linewidth=2,
           label="median = 5000")
ax.set_title("One 41,000-step day drags the mean 3,900 steps above the median")
ax.set_xlabel("Steps in a day (count)")
ax.set_ylabel("Number of days")
ax.legend()
fig.tight_layout()
fig.savefig("steps.png", dpi=150)
plt.show()
```

Output:

```
mean  : 8900.0
median: 5000.0
```

The histogram shows 8 days crammed into the leftmost bin and a single lonely bar out near 41,000 — a textbook outlier picture.

**The sentence:** *I'd quote the median, 5000 steps, because eight of the nine days sit between 4,200 and 5,300 and the 41,000 is almost certainly a bike ride the tracker counted as steps; the mean of 8,900 describes a day that never happened.*

---

### 3. [Build] Right chart for each question

```python
import matplotlib.pyplot as plt
from students import build_students

df = build_students()

# --- Q1: How many students are in each club?  -> BAR ---------------------
# Why: "how many in each category" is a category comparison.
counts = df["club"].value_counts().sort_index()
print(counts)          # art 12, chess 14, music 12
fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(counts.index, counts.values, color="#4c72b0")
ax.bar_label(bars, padding=2)
ax.set_ylim(0, 16)
ax.set_title("Chess is the largest club with 14 of 38 students")
ax.set_xlabel("Club")
ax.set_ylabel("Number of students")
fig.tight_layout(); fig.savefig("q1_clubs.png", dpi=150); plt.close(fig)

# --- Q2: Is age related to study hours?  -> SCATTER ----------------------
# Why: two numeric columns, asking whether they move together.
fig, ax = plt.subplots(figsize=(6, 4.5))
ax.scatter(df["age"], df["hours"], s=60, color="#1f77b4",
           alpha=0.7, edgecolors="white")
r = df["age"].corr(df["hours"])
ax.set_title(f"Older students report FEWER study hours (r = {r:.2f})")
ax.set_xlabel("Age (years)")
ax.set_ylabel("Study hours per week")
ax.set_xticks([12, 13, 14])
ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("q2_age_hours.png", dpi=150); plt.close(fig)
print("age/hours r =", round(r, 3))

# --- Q3: How are study hours distributed?  -> HISTOGRAM ------------------
# Why: one numeric column, asking about its shape.
fig, ax = plt.subplots(figsize=(6.5, 4))
ax.hist(df["hours"], bins=[0, 1, 2, 3, 4, 5, 6], color="#4c72b0",
        edgecolor="white")
ax.set_title("Study hours cluster between 2 and 5 hours a week")
ax.set_xlabel("Study hours per week")
ax.set_ylabel("Number of students")
ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
fig.tight_layout(); fig.savefig("q3_hours_hist.png", dpi=150); plt.close(fig)

# --- Q4: Which house has the most variable scores?  -> BOX ---------------
# Why: comparing SPREAD across groups, not just their middles.
order = ["Blue", "Green", "Red"]
data = [df.loc[df["house"] == h, "score"].values for h in order]
fig, ax = plt.subplots(figsize=(6.5, 4.5))
ax.boxplot(data, showmeans=True)
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(order)
ax.set_title("Blue house scores are the most spread out")
ax.set_xlabel("House")
ax.set_ylabel("Score (points out of 100)")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig("q4_house_box.png", dpi=150); plt.close(fig)
print(df.groupby("house")["score"].agg(["count", "mean", "std"]).round(2))

# --- Q5: Age vs hours, split by house?  -> SCATTER + colour + legend -----
# Why: still two numbers, but now with a third categorical dimension.
fig, ax = plt.subplots(figsize=(7, 4.5))
for house, colour, marker in [("Blue", "#1f77b4", "o"),
                              ("Green", "#2ca02c", "^"),
                              ("Red", "#d62728", "s")]:
    sub = df[df["house"] == house]
    ax.scatter(sub["age"], sub["hours"], c=colour, marker=marker, s=70,
               label=house, alpha=0.8, edgecolors="white")
ax.set_title("No house escapes the age trend in study hours")
ax.set_xlabel("Age (years)")
ax.set_ylabel("Study hours per week")
ax.set_xticks([12, 13, 14])
ax.legend(title="House")
ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("q5_age_hours_house.png", dpi=150); plt.close(fig)
```

Printed output:

```
art      12
chess    14
music    12
Name: club, dtype: int64
age/hours r = -0.572
       count   mean    std
house                     
Blue      14  74.36  16.46
Green     12  67.42  15.45
Red       12  74.25  13.83
```

**The chart-choice reasoning, written out:**

1. **Bar** — "how many in each club" compares three named categories. Categories have no order and no in-between values, so bars.
2. **Scatter** — age and hours are both numeric and we're asking whether they move together. Only a scatter shows every student individually.
3. **Histogram** — one numeric column, no groups, asking about shape. Note the bins are set explicitly to whole hours so each bar is readable. The counts come out as `3, 5, 8, 9, 7, 6`.
4. **Box** — the question uses the word *variable*, which means spread, and a box plot is the spread chart. A bar of means would have answered a different question entirely.
5. **Scatter with colour + legend** — two numbers plus a category. Colour carries the category; the legend explains the colour. Marker shapes vary too so it survives being printed in black and white.

**Interesting result to chase down:** the age/hours correlation is **−0.572** — a moderately strong *negative* relationship. Older students in this table report *fewer* study hours. Check it with a groupby:

```python
print(df.groupby("age")["hours"].agg(["count", "mean"]).round(2))
```

```
     count  mean
age             
12      10  4.30
13      18  2.97
14      10  1.95
```

12-year-olds average 4.3 hours, 14-year-olds average 1.95. That's a real pattern in this data — and a perfect place to practise the Concept-5 discipline: **describe it, don't explain it.** "Older students in this sample reported fewer study hours" is honest. "Getting older makes you lazier" is a causal claim this scatter cannot support. Maybe the 14-year-olds have more homework and count it separately, maybe they under-report, maybe this sample of 10 fourteen-year-olds is just unusual. Ten rows is not a generation.

---

### 4. [Build] Build a lie, then confess

```python
import matplotlib.pyplot as plt
from students import build_students

df = build_students()
club_mean = df.groupby("club")["score"].mean().sort_values(ascending=False)
print(club_mean.round(2))

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

# ---- LEFT: two tricks at once ------------------------------------------
axes[0].bar(club_mean.index, club_mean.values, color="#d62728")
axes[0].set_ylim(66, 78)                 # TRICK 1: truncated axis
axes[0].set_title("MISLEADING: 'Chess students crush art students'")
axes[0].set_xlabel("Club")
axes[0].set_ylabel("Score")              # TRICK 2: no units at all

# ---- RIGHT: honest -----------------------------------------------------
axes[1].bar(club_mean.index, club_mean.values, color="#4c72b0")
axes[1].set_ylim(0, 100)
axes[1].set_title("HONEST: axis from 0, units stated")
axes[1].set_xlabel("Club")
axes[1].set_ylabel("Mean score (points out of 100)")

fig.suptitle("Same three club averages, drawn two ways", fontsize=13)
fig.tight_layout()
fig.savefig("club_lie_and_fix.png", dpi=150)
plt.show()

# ---- the confession, with numbers --------------------------------------
chess, art = club_mean["chess"], club_mean["art"]
honest_ratio = chess / art
trunc_ratio = (chess - 66) / (art - 66)

print(f"chess = {chess:.2f}, art = {art:.2f}")
print(f"honest height ratio  chess/art = {honest_ratio:.2f}x")
print(f"truncated (base 66)  chess/art = {trunc_ratio:.2f}x")
print(f"exaggeration factor            = {trunc_ratio / honest_ratio:.1f}x")
print()
print("Trick 1 — truncated y-axis. Starting at 66 deletes 66 points of length")
print("  from every bar, so an 8.2-point real gap becomes almost the whole")
print("  height of the chart.")
print("Trick 2 — no units on the y-label. 'Score' could be out of 10, 100 or")
print("  1000, so the reader cannot judge whether 8 points is a lot.")
```

Output:

```
club
chess    76.07
music    71.83
art      67.83
Name: score, dtype: float64
chess = 76.07, art = 67.83
honest height ratio  chess/art = 1.12x
truncated (base 66)  chess/art = 5.50x
exaggeration factor            = 4.9x
```

**The confession paragraph:** Chess averages 76.07 and art averages 67.83 — a gap of 8.24 points, which is 12% higher. Drawn honestly from zero, the chess bar is 1.12× the art bar and the difference is visible but modest. Truncating the axis at 66 makes the chess bar 5.50× the art bar, an exaggeration of roughly **4.9×**. Removing the units from the y-label removes the reader's last defence, because without "out of 100" they cannot judge whether 8 points is a landslide or a rounding error. Neither trick changes a single number.

---

### 5. [Stretch] The cherry-pick challenge

```python
import matplotlib.pyplot as plt

weeks = list(range(1, 13))
visits = [118, 126, 131, 140, 152, 149, 158, 171, 166, 158, 174, 189]


def pct_change(values):
    """Percentage change from the first value to the last."""
    return (values[-1] - values[0]) / values[0] * 100


def window(weeks, visits, start, end):
    """Return the (weeks, visits) slice for weeks start..end inclusive."""
    i, j = weeks.index(start), weeks.index(end)
    return weeks[i:j + 1], visits[i:j + 1]


def find_extreme_windows(weeks, visits, size=3):
    """Search every window of `size` weeks; return the worst and best."""
    results = []
    for i in range(len(weeks) - size + 1):
        chunk = visits[i:i + size]
        results.append((pct_change(chunk), weeks[i], weeks[i + size - 1]))
    worst = min(results)          # tuples compare on the first element
    best = max(results)
    return worst, best


worst, best = find_extreme_windows(weeks, visits, size=3)
print(f"worst 3-week window: weeks {worst[1]}-{worst[2]}  {worst[0]:+.1f}%")
print(f"best  3-week window: weeks {best[1]}-{best[2]}  {best[0]:+.1f}%")

# Three panels, SHARED y-limits so the eye can compare them fairly.
fig, axes = plt.subplots(1, 3, figsize=(14, 4.2), sharey=True)
ylim = (0, 200)

wx, wy = window(weeks, visits, worst[1], worst[2])
axes[0].plot(wx, wy, marker="o", color="#d62728", linewidth=2)
axes[0].set_title(f"Weeks {worst[1]}-{worst[2]} ONLY: {worst[0]:+.1f}%")
axes[0].set_xticks(wx)

bx, by = window(weeks, visits, best[1], best[2])
axes[1].plot(bx, by, marker="o", color="#2ca02c", linewidth=2)
axes[1].set_title(f"Weeks {best[1]}-{best[2]} ONLY: {best[0]:+.1f}%")
axes[1].set_xticks(bx)

axes[2].plot(weeks, visits, marker="o", color="#1f77b4", linewidth=2)
axes[2].set_title(f"All 12 weeks: {pct_change(visits):+.1f}%")
axes[2].set_xticks(weeks)

for ax in axes:
    ax.set_ylim(*ylim)
    ax.set_xlabel("School week")
    ax.grid(axis="y", alpha=0.3)
axes[0].set_ylabel("Visits per week (count)")

fig.suptitle("Three true charts of the same 12 weeks", fontsize=13)
fig.tight_layout()
fig.savefig("cherry_pick.png", dpi=150)
plt.show()
```

Output:

```
worst 3-week window: weeks 8-10  -7.6%
best  3-week window: weeks 10-12  +19.6%
```

**Working:** weeks 8–10 are 171 → 166 → 158, so (158 − 171) ÷ 171 × 100 = **−7.60%**. Weeks 10–12 are 158 → 174 → 189, so (189 − 158) ÷ 158 × 100 = **+19.62%**. The whole term is (189 − 118) ÷ 118 × 100 = **+60.17%**.

**Why `sharey=True` matters:** without it, matplotlib would auto-scale each panel to its own data, so the −7.6% panel would look like a cliff and the +60% panel would look like a gentle slope. Sharing the y-limits is the honest choice whenever panels sit side by side.

**The lesson in one line:** "down 7.6%", "up 19.6%" and "up 60.2%" are all true statements about the same twelve numbers. The one you'd print depends entirely on what you want the reader to believe.

---

### 6. [Stretch] Correlation without causation, built by you

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 12 months of an invented seaside town.
data = pd.DataFrame({
    "month":          ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "ice_creams":     [210, 240, 400, 620, 820, 1180,
                       1420, 1360, 900, 560, 300, 230],
    "drownings":      [1, 1, 2, 4, 5, 8,
                       9, 9, 6, 3, 2, 1],
    "avg_temp_c":     [12, 13, 16, 21, 25, 29,
                       32, 31, 26, 20, 15, 12],
})

r_xy = data["ice_creams"].corr(data["drownings"])
r_xc = data["ice_creams"].corr(data["avg_temp_c"])
r_yc = data["drownings"].corr(data["avg_temp_c"])

print(f"ice creams vs drownings : r = {r_xy:.3f}")
print(f"ice creams vs temperature: r = {r_xc:.3f}")
print(f"drownings vs temperature : r = {r_yc:.3f}")

fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))

axes[0].scatter(data["ice_creams"], data["drownings"],
                s=70, color="#d62728", edgecolors="white")
axes[0].set_title(f"Looks causal (r = {r_xy:.3f})")
axes[0].set_xlabel("Ice creams sold (count per month)")
axes[0].set_ylabel("Drownings (count per month)")

axes[1].scatter(data["avg_temp_c"], data["ice_creams"],
                s=70, color="#1f77b4", edgecolors="white")
axes[1].set_title(f"Heat drives sales (r = {r_xc:.3f})")
axes[1].set_xlabel("Average temperature (°C)")
axes[1].set_ylabel("Ice creams sold (count per month)")

axes[2].scatter(data["avg_temp_c"], data["drownings"],
                s=70, color="#2ca02c", edgecolors="white")
axes[2].set_title(f"Heat drives swimming (r = {r_yc:.3f})")
axes[2].set_xlabel("Average temperature (°C)")
axes[2].set_ylabel("Drownings (count per month)")

for ax in axes:
    ax.grid(alpha=0.3)

fig.suptitle("Temperature is the confounder behind panel 1", fontsize=13)
fig.tight_layout()
fig.savefig("confounder.png", dpi=150)
plt.show()
```

Output:

```
ice creams vs drownings : r = 0.996
ice creams vs temperature: r = 0.988
drownings vs temperature : r = 0.987
```

All three correlations are above 0.98, comfortably clearing the requirement.

**The three-sentence explanation:** Ice cream sales and drownings correlate at r = 1.00 (to two decimals), which would be overwhelming evidence if correlation meant causation — but banning ice cream would obviously not save a single swimmer. The reason both rise together is a hidden third variable, **average temperature**, which independently causes people to buy ice cream *and* causes people to go swimming, and swimming is what creates drowning risk; temperature correlates about equally strongly with both (0.99 and 0.99). To test causation you would need an **experiment**, not a chart — for example, randomly restricting ice cream sales in half of a set of similar towns and comparing drowning rates, which is both impractical and, once you say it out loud, obviously absurd; that absurdity is the signal that the original chart was never causal evidence at all.

**Bonus insight to notice:** panel 1 looks *exactly* as convincing as panels 2 and 3. There is nothing visible in a scatter plot that distinguishes "A causes B" from "C causes both". The distinction lives entirely outside the data, in what you know about the world.

</details>

---

[⬅ Previous](module-06-pandas-tables.md) · [Level 2 Home](README.md) · [Next ➡](module-08-first-model-knn.md)

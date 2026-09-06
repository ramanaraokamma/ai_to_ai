"""The DATA, CHART and MODEL motifs for Level 2 figures."""
from _gen_core import *

# ------------------------------------------------------------------ DataFrame
_df = []
_cols = ((22, 36), (58, 64), (122, 64), (186, 64))
_df.append('  <rect x="22" y="26" width="36" height="32" fill="%s"/>' % PANEL)
for _x, _w in _cols[1:]:
    _df.append('  <rect x="%s" y="26" width="%s" height="32" fill="%s"/>' % (_x, _w, DATA_F))
for _y in (58, 90, 122):
    _df.append('  <rect x="22" y="%s" width="36" height="32" fill="%s"/>' % (_y, PANEL))
    _df.append('  <rect x="122" y="%s" width="64" height="32" fill="%s"/>' % (_y, ACC_F))
_df.append('  <g stroke="%s" stroke-width="1.5">' % GRID)
for _x in (58, 122, 186):
    _df.append('    <line x1="%s" y1="26" x2="%s" y2="154"/>' % (_x, _x))
for _y in (90, 122):
    _df.append('    <line x1="22" y1="%s" x2="250" y2="%s"/>' % (_y, _y))
_df.append('  </g>')
_df.append('  <line x1="22" y1="58" x2="250" y2="58" stroke="%s" stroke-width="2"/>' % INK)
for _x, _lab in ((90, "player"), (154, "runs"), (218, "over")):
    _df.append("  " + t(_x, 42, _lab, 12, INK, "middle", central=True, weight="600"))
for _y, _row in ((74, ("0", "Meera", "48", "12")), (106, ("1", "Kabir", "31", "9")), (138, ("2", "Nova", "57", "15"))):
    _df.append("  " + t(40, _y, _row[0], 12, MUT, "middle", central=True))
    for _x, _v in zip((90, 154, 218), _row[1:]):
        _df.append("  " + t(_x, _y, _v, 12, INK, "middle", central=True))
_df.append('  <rect x="122" y="26" width="64" height="128" fill="none" stroke="%s" stroke-width="3"/>' % ACC_S)
_df.append('  <rect x="22" y="26" width="228" height="128" fill="none" stroke="%s" stroke-width="3"/>' % INK)
_df.append("  " + t(154, 18, "selected", 12, MUT, "middle"))
_df.append("  " + t(40, 170, "index", 12, MUT, "middle"))

M("motif-dataframe", "A DataFrame as a grid with a header row and an index",
  "A three-row table with a bold header row reading player, runs, over, a grey index column numbered 0 to 2, and the runs column outlined and tinted as the current selection.",
  "0 0 272 180", "\n".join(_df),
  "Header row = data fill + weight 600. Index column = panel grey. A selection is an accent OUTLINE plus an accent tint, and it must cover the header too.")

# ------------------------------------------------------------------ 1-D array
_a1 = ['  <path d="M22 18 V12 H242 V18" fill="none" stroke="%s" stroke-width="1.5" stroke-linejoin="round"/>' % MUT]
for _x, _v in zip((22, 66, 110, 154, 198), "12345"):
    _a1.append('  <rect x="%s" y="24" width="44" height="44" fill="%s" stroke="%s" stroke-width="2"/>' % (_x, DATA_F, DATA_S))
    _a1.append("  " + t(_x + 22, 46, _v, 14, INK, "middle", central=True))
_a1.append('  <rect x="22" y="24" width="220" height="44" fill="none" stroke="%s" stroke-width="3"/>' % DATA_S)
_a1.append("  " + t(132, 86, "shape (5,)", 12, MUT, "middle"))

M("motif-array-1d", "A 1-D numpy array as one contiguous row",
  "Five square cells butted together holding 1 to 5, with a bracket above and the annotation shape open bracket 5 comma close bracket below.",
  "0 0 264 94", "\n".join(_a1),
  "Cells touch, unlike a list's separated slots — that is the picture of contiguous memory. Always print the shape.")

# ------------------------------------------------------------------ 2-D array
_a2 = ['  <line x1="32" y1="34" x2="32" y2="126" stroke="%s" stroke-width="2" stroke-linecap="round"/>' % MUT,
       "  " + head(32, 132, 90, MUT, 2),
       '  <line x1="50" y1="20" x2="204" y2="20" stroke="%s" stroke-width="2" stroke-linecap="round"/>' % MUT,
       "  " + head(210, 20, 0, MUT, 2),
       "  " + t(130, 12, "axis 1", 12, MUT, "middle"),
       "  " + t(16, 84, "axis 0", 12, MUT, "middle", extra='transform="rotate(-90 16 84)"')]
_vals = ("1234", "5678", "9012")
for _r, _y in enumerate((30, 66, 102)):
    for _c, _x in enumerate((48, 90, 132, 174)):
        _a2.append('  <rect x="%s" y="%s" width="42" height="36" fill="%s" stroke="%s" stroke-width="2"/>' % (_x, _y, DATA_F, DATA_S))
        _a2.append("  " + t(_x + 21, _y + 18, _vals[_r][_c], 12, INK, "middle", central=True))
_a2.append('  <rect x="48" y="30" width="168" height="108" fill="none" stroke="%s" stroke-width="3"/>' % DATA_S)
_a2.append("  " + t(132, 158, "shape (3, 4)", 12, MUT, "middle"))

M("motif-array-2d", "A 2-D numpy array as a shaped block",
  "A block of three rows by four columns of numbers, with axis 0 arrowed downwards, axis 1 arrowed across, and the annotation shape 3 comma 4 below.",
  "0 0 240 172", "\n".join(_a2),
  "axis 0 runs DOWN the rows, axis 1 runs ACROSS the columns. Label both arrows every time; this is the single most confused idea in numpy.")


# ------------------------------------------------------------------ chart frames
def chart_frame(xlabels=True, xtitle="hours", ytitle="score"):
    out = ['  <g stroke="%s" stroke-width="1.5">' % GRID]
    for y in (108, 66, 24):
        out.append('    <line x1="46" y1="%s" x2="200" y2="%s"/>' % (y, y))
    out.append('  </g>')
    for y, lab in ((150, "0"), (108, "5"), (66, "10"), (24, "15")):
        out.append("  " + t(40, y + 4, lab, 12, MUT, "end"))
    if xlabels:
        out.append('  <g stroke="%s" stroke-width="1.5">' % MUT)
        for x in (46, 97, 148, 199):
            out.append('    <line x1="%s" y1="150" x2="%s" y2="155"/>' % (x, x))
        out.append('  </g>')
        for x, lab in ((46, "0"), (97, "2"), (148, "4"), (199, "6")):
            out.append("  " + t(x, 168, lab, 12, MUT, "middle"))
    out.append('  <line x1="46" y1="24" x2="46" y2="150" stroke="%s" stroke-width="2"/>' % INK)
    out.append('  <line x1="46" y1="150" x2="200" y2="150" stroke="%s" stroke-width="2"/>' % INK)
    out.append("  " + t(123, 184, xtitle, 12, MUT, "middle"))
    out.append("  " + t(18, 87, ytitle, 12, MUT, "middle", extra='transform="rotate(-90 18 87)"'))
    return out


_sc = chart_frame()
for _x, _y in ((66, 132), (84, 118), (104, 108), (122, 88), (142, 76), (160, 58), (180, 44)):
    _sc.insert(-2, '  <circle cx="%s" cy="%s" r="5" fill="%s" stroke="%s" stroke-width="2"/>' % (_x, _y, DATA_S, PAPER))
M("motif-chart-scatter", "A scatter plot skeleton",
  "A scatter plot with a labelled y axis, a labelled x axis, three grid lines and seven dots rising to the right.",
  "0 0 220 192", "\n".join(_sc),
  "One series, so no legend: the title names it. Grid lines go UNDER the marks, at 1.5px grey.")

_bar = chart_frame(xlabels=False, xtitle="day")
for _x, _top, _v, _lab in ((60, 64, "10", "Mon"), (96, 96, "6", "Tue"), (132, 40, "13", "Wed"), (168, 112, "4", "Thu")):
    _bar.insert(-2, '  <path d="M%s 150 V%s A4 4 0 0 1 %s %s H%s A4 4 0 0 1 %s %s V150 Z" fill="%s"/>'
                % (_x, _top + 4, _x + 4, _top, _x + 22, _x + 26, _top + 4, DATA_S))
    _bar.insert(-2, "  " + t(_x + 13, _top - 6, _v, 12, INK, "middle"))
    _bar.insert(-2, "  " + t(_x + 13, 168, _lab, 12, MUT, "middle"))
M("motif-chart-bar", "A bar chart skeleton",
  "A bar chart with four bars labelled Mon to Thu, each printing its own value above it.",
  "0 0 220 192", "\n".join(_bar),
  "Bars start at zero, always. Every bar carries its number, so the reader never measures against the grid.")

_ln = chart_frame()
_pts = ((60, 130), (92, 104), (124, 110), (156, 72), (188, 52))
_ln.insert(-2, '  <polyline points="%s" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
           % (" ".join("%s,%s" % p for p in _pts), DATA_S))
for _x, _y in _pts:
    _ln.insert(-2, '  <circle cx="%s" cy="%s" r="4.5" fill="%s" stroke="%s" stroke-width="3"/>' % (_x, _y, PAPER, DATA_S))
M("motif-chart-line", "A line chart skeleton",
  "A line chart with one series of five points joined left to right, each point marked with a hollow circle.",
  "0 0 220 192", "\n".join(_ln),
  "A line means the x axis is ordered — time, or a dial you turned. If the x values are categories, use bars instead.")

# ------------------------------------------------------------------ train/test split
_sp = ["  " + rect(24, 30, 76, 110, 8, PAPER, INK, 3)]
_sp.append('  <g stroke="%s" stroke-width="1.5">' % GRID)
for _y in (46, 62, 78, 94, 110, 126):
    _sp.append('    <line x1="24" y1="%s" x2="100" y2="%s"/>' % (_y, _y))
_sp.append('  </g>')
_sp += ["  " + t(62, 74, "80", 24, INK, "middle", central=True),
        "  " + t(62, 130, "20", 18, INK, "middle", central=True),
        '  <line x1="14" y1="118" x2="110" y2="118" stroke="%s" stroke-width="2" stroke-dasharray="6 4"/>' % ACC_S,
        "  " + arrow(104, 74, 150, 60),
        "  " + arrow(104, 128, 150, 124),
        "  " + rect(154, 34, 124, 54, 10, DATA_F, DATA_S, 3),
        "  " + t(216, 56, "train", 14, INK, "middle", central=True),
        "  " + t(216, 76, "80 rows", 12, MUT, "middle"),
        "  " + rect(154, 102, 124, 46, 10, ACC_F, ACC_S, 3),
        "  " + t(216, 120, "test", 14, INK, "middle", central=True),
        "  " + t(216, 140, "20 rows", 12, MUT, "middle"),
        "  " + t(150, 166, "one cut, then never mix them", 12, MUT, "middle")]
M("motif-split", "A train/test split as one cut of the deck",
  "A deck of 100 rows is cut by a dashed line into a train pile of 80 rows and a test pile of 20 rows.",
  "0 0 290 175", "\n".join(_sp),
  "Train is data blue, test is accent pink — the pile you must not touch. Print both counts; they have to add up.")

# ------------------------------------------------------------------ kNN
_knn = ['  <circle cx="110" cy="80" r="40" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="6 5"/>' % ACC_S,
        '  <line x1="110" y1="34" x2="110" y2="40" stroke="%s" stroke-width="1.5"/>' % ACC_S,
        "  " + t(110, 30, "k = 3", 12, MUT, "middle")]
for _x, _y in ((40, 44), (58, 126), (194, 86), (94, 106)):
    _knn.append('  <circle cx="%s" cy="%s" r="6" fill="%s" stroke="%s" stroke-width="2"/>' % (_x, _y, DATA_S, PAPER))
for _x, _y in ((88, 64), (132, 96), (186, 36), (168, 128)):
    _knn.append('  <path d="M%s %s L%s %s L%s %s Z" fill="%s" stroke="%s" stroke-width="2" stroke-linejoin="round"/>'
                % (_x, _y - 7, _x + 7, _y + 5, _x - 7, _y + 5, OK_S, PAPER))
_knn += ["  " + rect(102, 72, 16, 16, 3, ACC_F, ACC_S, 3),
         "  " + t(110, 80, "?", 12, INK, "middle", central=True),
         '  <line x1="16" y1="160" x2="214" y2="160" stroke="%s" stroke-width="1.5"/>' % GRID,
         '  <path d="M26 173 L33 185 L19 185 Z" fill="%s" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (OK_S, PAPER),
         "  " + t(42, 185, "orange &#215; 2", 14, INK),
         '  <polyline points="134,182 140,188 152,174" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>' % OK_S,
         "  " + t(158, 185, "wins", 12, MUT),
         '  <circle cx="26" cy="204" r="6" fill="%s" stroke="%s" stroke-width="2"/>' % (DATA_S, PAPER),
         "  " + t(42, 209, "apple &#215; 1", 14, INK)]
M("motif-knn", "A kNN vote: query point, three neighbours, tally",
  "A pink square marked with a question mark sits among circles and triangles. A dashed ring labelled k equals 3 encloses two triangles and one circle. Below, a tally reads orange times 2 wins, apple times 1.",
  "0 0 230 220", "\n".join(_knn),
  "Two classes = two SHAPES, never two colours only. The query is a third shape. The tally must add up to k.")

# ------------------------------------------------------------------ decision tree
M("motif-tree", "A decision tree as boxes and yes/no branches",
  "A question box reading petal long? branches no to a second question wide? and yes to the answer setosa. The second question branches to virginica and versicolor.",
  "0 0 280 196", """
  <g stroke="%s" stroke-width="2" fill="none">
    <path d="M140 54 V70 H56 V88"/>
    <path d="M140 54 V70 H224 V88"/>
    <path d="M56 124 V140 H38 V156"/>
    <path d="M56 124 V140 H118 V156"/>
  </g>
  %s
  %s
  %s
  %s
  %s
  %s
  %s
  %s
  %s
  %s
  %s
  %s
  %s
  %s
""" % (MUT,
       t(98, 66, "no", 12, MUT, "middle"),
       t(182, 66, "yes", 12, MUT, "middle"),
       t(33, 152, "no", 12, MUT, "end"),
       t(123, 152, "yes", 12, MUT),
       rect(76, 16, 128, 38, 8, PANEL, INK, 3),
       t(140, 35, "petal long?", 12, INK, "middle", central=True),
       rect(8, 88, 96, 36, 8, PANEL, INK, 3),
       t(56, 106, "wide?", 12, INK, "middle", central=True),
       rect(176, 88, 96, 36, 8, DATA_F, DATA_S, 3),
       t(224, 106, "setosa", 12, INK, "middle", central=True),
       rect(4, 156, 68, 32, 8, DATA_F, DATA_S, 3),
       t(38, 172, "virginica", 12, INK, "middle", central=True),
       rect(84, 156, 68, 32, 8, DATA_F, DATA_S, 3),
       t(118, 172, "versicolor", 12, INK, "middle", central=True)),
  "Draw the edges FIRST so boxes sit on top. Questions are grey and end in ?, answers are blue and do not. Label every branch in words.")


# ------------------------------------------------------------------ fit panels
def fit_panel(curve, label, colour):
    out = ['  <line x1="24" y1="18" x2="24" y2="126" stroke="%s" stroke-width="2"/>' % INK,
           '  <line x1="24" y1="126" x2="146" y2="126" stroke="%s" stroke-width="2"/>' % INK,
           '  <path d="%s" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>' % (curve, colour)]
    for x, y in ((36, 110), (52, 96), (66, 102), (82, 80), (96, 72), (112, 58), (126, 64), (140, 40)):
        out.append('  <circle cx="%s" cy="%s" r="4.5" fill="%s" stroke="%s" stroke-width="1.5"/>' % (x, y, DATA_S, PAPER))
    out.append("  " + t(85, 148, label, 12, MUT, "middle"))
    return "\n".join(out)


M("motif-fit-underfit", "Underfitting: a line too simple for the data",
  "Eight dots climb to the right. A flat straight line ignores the climb entirely; the caption reads too simple.",
  "0 0 160 158", fit_panel("M30 80 L142 80", "too simple", BAD_S),
  "Panel 1 of 3. The eight dots are IDENTICAL in all three panels — only the drawn model changes.")

M("motif-fit-good", "A good fit: a curve that follows the trend",
  "The same eight dots, with a smooth curve running through the middle of the climb; the caption reads just right.",
  "0 0 160 158", fit_panel("M30 114 Q86 92 142 44", "just right", OK_S),
  "Panel 2 of 3. Correct green, and the shape is smooth — two cues, not one.")

M("motif-fit-overfit", "Overfitting: a wiggle through every point",
  "The same eight dots, with a jagged line that detours to pass exactly through each one; the caption reads memorised.",
  "0 0 160 158",
  fit_panel("M30 118 L36 110 L44 120 L52 96 L59 110 L66 102 L74 84 L82 80 L89 88 L96 72 "
            "L104 68 L112 58 L119 74 L126 64 L133 50 L140 40 L145 50", "memorised", BAD_S),
  "Panel 3 of 3. Underfit and overfit are both wrong-red; the SHAPE (flat vs jagged) tells them apart in greyscale.")

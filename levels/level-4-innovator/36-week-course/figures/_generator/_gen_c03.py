"""Block C3 (weeks 7, 8, 9) extra figures: a mental model, a worked-numbers figure and a blank
workbook figure per week. Every number is copied from the week's printed output or is a hand
sum printed beside it (STYLE.md 2.1).

W7  knobs.py / grid.py: 5+4+4+4+3+4 = 24 values, 24 x 3 = 72, +3 baseline = 75 runs, 3,840 configs, 11,520 runs
    table.py (seeds 0-2, 60 epochs): baseline 0.039 +/- 0.008; rows dropout 0.1, dropout 0.5, batch_size 8,
    batch_size 512, norm layer, weight_decay 0.01 (mean +/- spread as printed); gaps are hand sums of the 3-decimal figures
    workbook page 7.3: dropout 0.3, norm batch, schedule step (given values; the figure is blank)
W8  shapes.py: x (2, 4, 3), out (2, 4, 5), h_n (1, 2, 5)
    order.py (torch.manual_seed(0)): step distances 0.0000 0.9854 0.6620 0.2906 0.8842, final states of a and b
    workbook page 8.3 part (c): x = [1, 1, 0, 0], W_xh = 1.0, W_hh = 0.5 (the figure is blank)
W9  student guide 'The night before' table; workbook page 9.9 per-week grid (marks available 11 10 10 9 8 8 7 12 = 75)
"""
import math
from _gen_core import *

FIGS = {}


def fig(name, vb, title, desc, parts):
    FIGS[name] = svg_doc(vb, title, desc, J(*parts))


def ctitle(s):
    return t(400, 44, s, 24, INK, "middle")


def cap(s, y=374):
    return t(400, y, s, 14, MUT, "middle")


# ---------------------------------------------------------------- W7-4  one knob at a time
def w07_4():
    knobs = [("lr", 5), ("batch_size", 4), ("dropout", 4), ("weight_decay", 4), ("norm", 3), ("schedule", 4)]
    assert sum(n for _, n in knobs) == 24 and 24 * 3 == 72 and 72 + 3 == 75
    full = 1
    for _, n in knobs:
        full *= n
    assert full == 3840 and full * 3 == 11520
    o = [ctitle("One knob at a time keeps the sweep small")]
    # left panel: the six value lists
    o.append(rect(20, 62, 430, 270, 12, PANEL, GRID, 2))
    o.append(t(36, 88, "the six knob lists in knobs.py", 18, INK, "start"))
    o.append(t(36, 106, "one square per value", 12, MUT, "start"))
    for i, (name, n) in enumerate(knobs):
        y = 130 + i * 31
        o.append(t(36, y + 5, name, 14, INK, "start", mono=True))
        for k in range(n):
            o.append(sq(188 + k * 30, y - 11, 22, 22, DATA_F, DATA_S, 2))
        o.append(t(188 + 5 * 30 + 8, y + 5, "= %d" % n, 14, INK, "start"))
    o.append(line(36, 316 - 14, 434, 316 - 14, GRID, 1.5))
    o.append(t(36, 316 + 2, "5 + 4 + 4 + 4 + 3 + 4 = 24 values", 14, INK, "start"))
    # right panel: runs on a log axis
    o.append(rect(466, 62, 314, 270, 12, PANEL, GRID, 2))
    o.append(t(482, 88, "runs it takes", 18, INK, "start"))
    x0 = 500
    px = lambda v: x0 + (math.log10(v) - 1) * 76.0       # 10 -> 500, 10000 -> 728
    o.append(line(x0, 292, px(10000), 292, INK, 2))
    for d in (10, 100, 1000, 10000):
        o.append(line(px(d), 292, px(d), 298, MUT, 1.5))
        o.append(t(px(d), 314, "{:,}".format(d), 12, MUT, "middle"))
    o.append(t(614, 328, "runs (log scale)", 12, MUT, "middle"))
    o.append(t(482, 122, "one knob at a time", 14, INK, "start"))
    o.append(rect(x0, 130, px(75) - x0, 22, 4, DATA_F, DATA_S, 3))
    o.append(t(px(75) + 8, 146, "75 runs", 14, INK, "start"))
    o.append(t(482, 172, "24 &#215; 3 + 3 = 75", 12, MUT, "start"))
    o.append(t(482, 204, "every combination (not run)", 14, INK, "start"))
    o.append(rect(x0, 212, px(11520) - x0, 22, 4, PANEL, MUT, 2, "6 4"))
    o.append(t(px(11520) - 8, 228, "11,520 runs", 14, INK, "end"))
    o.append(t(482, 252, "5 &#215; 4 &#215; 4 &#215; 4 &#215; 3 &#215; 4 = 3,840", 12, MUT, "start"))
    o.append(t(482, 268, "3,840 &#215; 3 seeds = 11,520", 12, MUT, "start"))
    o.append(cap("One knob per run costs 75 runs; crossing every knob with every other would cost 11,520.", 366))
    fig("fig-w07-4-one-knob-at-a-time.svg", "0 0 800 400",
        "One knob at a time keeps the sweep to 75 runs instead of 11,520",
        "Left, the six knob lists drawn as rows of squares, one square per value: lr 5, batch_size 4, dropout 4, "
        "weight_decay 4, norm 3, schedule 4, which add up to 24 values. Right, two bars on a log axis of runs. One knob "
        "at a time is 24 times 3 plus 3 baseline runs, which is 75 runs. Every combination of all six is 5 times 4 times "
        "4 times 4 times 3 times 4, which is 3,840 configurations, times 3 seeds, 11,520 runs; that bar is dashed because "
        "nobody ran it.", o)


# ---------------------------------------------------------------- W7-5  six rows with the rule applied
def w07_5():
    BM, BS = 0.039, 0.008          # table.py header: BASELINE val 0.039 +/- 0.008
    # (row, mean, spread, printed verdict) copied from the table.py output
    rows = [("dropout 0.1", 0.051, 0.008, "inside noise"),
            ("dropout 0.5", 0.062, 0.008, "WORSE"),
            ("batch_size 8", 0.039, 0.019, "inside noise"),
            ("batch_size 512", 0.060, 0.013, "inside noise"),
            ("norm layer", 0.057, 0.031, "inside noise"),
            ("weight_decay 0.01", 0.050, 0.018, "inside noise")]
    o = [ctitle("The rule applied to six rows of the table")]
    sc = 3571.0
    bx = 300
    o.append(t(24, 84, "row", 12, MUT, "start"))
    o.append(t(176, 84, "val mean &#177; spread", 12, MUT, "start"))
    o.append(sq(bx, 74, 12, 12, DATA_F, DATA_S, 2))
    o.append(t(bx + 18, 84, "gap", 12, INK, "start"))
    o.append(sq(bx + 62, 74, 12, 12, HUMAN_F, HUMAN_S, 2))
    o.append(t(bx + 80, 84, "2 &#215; larger spread", 12, INK, "start"))
    o.append(t(610, 84, "gap", 12, MUT, "end"))
    o.append(t(676, 84, "2 &#215; spr.", 12, MUT, "end"))
    o.append(t(688, 84, "verdict", 12, MUT, "start"))
    o.append(line(20, 94, 780, 94, GRID, 1.5))
    for i, (name, m, s, verdict) in enumerate(rows):
        y = 112 + i * 40
        gap = round(m - BM, 3)
        thr = round(2 * max(s, BS), 3)
        worse = abs(gap) >= thr
        assert worse == (verdict == "WORSE"), name
        if worse:
            o.append(rect(20, y - 3, 760, 38, 8, ACC_F, ACC_S, 3))
        o.append(t(28, y + 21, name, 14, INK, "start"))
        o.append(t(176, y + 21, "%.3f &#177; %.3f" % (m, s), 14, INK, "start"))
        o.append(sq(bx, y + 4, max(gap * sc, 1.5), 11, DATA_F, DATA_S, 2))
        o.append(sq(bx, y + 18, thr * sc, 11, HUMAN_F, HUMAN_S, 2))
        o.append(t(610, y + 21, "%.3f" % gap, 14, INK, "end"))
        o.append(t(676, y + 21, "%.3f" % thr, 14, INK, "end"))
        if worse:
            o.append(cross(696, y + 16, 7))
            o.append(t(710, y + 21, "WORSE", 14, BAD_S, "start"))
        else:
            o.append(t(688, y + 21, "inside noise", 12, MUT, "start"))
    o.append(cap("Baseline 0.039 &#177; 0.008. Blue bar: the gap. Gold bar: twice the larger spread.", 366))
    fig("fig-w07-5-six-rows-gap-versus-twice-spread.svg", "0 0 800 400",
        "Only a gap longer than twice the larger spread counts, and only one of these six rows passes",
        "Six rows from the Week 7 table, each with a blue gap bar over a gold twice-the-spread bar on one scale. "
        "Baseline 0.039 plus or minus 0.008. Dropout 0.1: 0.051, gap 0.012, twice the spread 0.016, inside noise. "
        "Dropout 0.5: 0.062, gap 0.023, twice the spread 0.016, WORSE, marked with a cross and a ringed row. "
        "Batch size 8: 0.039 plus or minus 0.019, gap 0.000, twice the spread 0.038, inside noise. Batch size 512: "
        "0.060 plus or minus 0.013, gap 0.021, twice the spread 0.026, inside noise. Norm layer: 0.057 plus or minus 0.031, "
        "gap 0.018, twice the spread 0.062, inside noise. Weight decay 0.01: 0.050 plus or minus 0.018, gap 0.011, "
        "twice the spread 0.036, inside noise.", o)


# ---------------------------------------------------------------- W7-6  blank: draw the gap and the threshold
def w07_6():
    o = [ctitle("Draw the gap and the threshold")]
    o.append(t(24, 76, "baseline 0.039 &#177; 0.008. Bars start at the left edge and share one scale.", 14, MUT, "start"))
    tx, sc = 236, 12000.0         # 0.03 -> 360 px
    rows = [("dropout 0.3", "0.043 &#177; 0.013"), ("norm batch", "0.024 &#177; 0.005"),
            ("schedule step", "0.033 &#177; 0.001")]
    o.append(t(612, 100, "verdict", 12, MUT, "start"))
    for v in (0.0, 0.01, 0.02, 0.03):
        xv = tx + v * sc
        o.append(line(xv, 108, xv, 304, GRID, 1.5, "6 4"))
        o.append(t(xv, 322, ("%.2f" % v) if v else "0", 12, MUT, "middle"))
    o.append(t(tx + 180, 340, "loss difference (scale 0 to 0.03)", 12, MUT, "middle"))
    for i, (name, ms) in enumerate(rows):
        y = 112 + i * 64
        o.append(t(24, y + 24, name, 14, INK, "start"))
        o.append(t(24, y + 44, ms, 12, MUT, "start"))
        o.append(t(226, y + 15, "gap", 12, INK, "end"))
        o.append(rect(tx, y + 2, 360, 20, 4, PAPER, MUT, 2))
        o.append(t(226, y + 47, "2 &#215; spread", 12, INK, "end"))
        o.append(rect(tx, y + 34, 360, 20, 4, PAPER, MUT, 2))
        o.append(rect(612, y + 8, 168, 38, 8, PAPER, MUT, 2, "6 4"))
    o.append(cap("Draw |gap| and twice the larger spread, then write the verdict in the dashed box.", 372))
    fig("fig-w07-6-blank-gap-and-threshold-bars.svg", "0 0 800 400",
        "Blank page: draw each row's gap and twice-the-spread bars to one scale and write the verdict",
        "A blank fill-in figure with three rows: dropout 0.3 (0.043 plus or minus 0.013), norm batch (0.024 plus or minus "
        "0.005) and schedule step (0.033 plus or minus 0.001), against the baseline 0.039 plus or minus 0.008. Each row has "
        "two empty tracks on a shared scale from 0 to 0.03, one labelled gap and one labelled twice spread, and an empty "
        "dashed box for the verdict. No answers are drawn.", o)


# ---------------------------------------------------------------- W8-4  the three shapes
def w08_4():
    o = [ctitle("Three shapes: x in, out and h_n back")]

    def grid(x0, y0, label, fill, stroke, ring_last=False):
        r = []
        for si in range(2):
            for wi in range(4):
                last = ring_last and wi == 3
                r.append(sq(x0 + wi * 44, y0 + si * 38, 44, 34, ACC_F if last else fill,
                            ACC_S if last else stroke, 3 if last else 2))
                r.append(t(x0 + wi * 44 + 22, y0 + si * 38 + 17, label, 12, INK, "middle", central=True))
        return r

    gx, gy = 112, 136
    # column and row headers for x
    for name, x0 in (("x", 112), ("out", 440)):
        o.append(t(x0 + 88, 98, name, 18, INK, "middle", mono=True))
        o.append(t(x0 + 88, 120, "word 1 2 3 4", 12, MUT, "middle"))
    o.append(t(104, gy + 22, "sentence 0", 12, MUT, "end"))
    o.append(t(104, gy + 60, "sentence 1", 12, MUT, "end"))
    # model box and arrows first (connectors, then boxes)
    o.append(arrow(292, 176, 322, 176, INK, 3))
    o.append(arrow(402, 176, 436, 176, INK, 3))
    o.append(arrow(618, 176, 664, 176, ACC_S, 3))
    o.extend(grid(112, gy, "3", DATA_F, DATA_S))
    o.append(rect(324, 140, 76, 72, 10, MODEL_F, MODEL_S, 3))
    o.append(t(362, 168, "nn.RNN", 14, INK, "middle", mono=True))
    o.append(t(362, 190, "(3, 5)", 14, INK, "middle", mono=True))
    o.extend(grid(440, gy, "5", DATA_F, DATA_S, ring_last=True))
    o.append(t(704, 98, "h_n", 18, INK, "middle", mono=True))
    for si in range(2):
        o.append(sq(682, gy + si * 38, 44, 34, ACC_F, ACC_S, 3))
        o.append(t(704, gy + si * 38 + 17, "5", 12, INK, "middle", central=True))
    # shape chips
    o.append(shape_chip(161, 228, "(2, 4, 3)", DATA_S))
    o.append(shape_chip(489, 228, "(2, 4, 5)", DATA_S))
    o.append(shape_chip(665, 228, "(1, 2, 5)", ACC_S))
    # plain words under each
    o.append(t(200, 276, "2 sentences, 4 words,", 12, MUT, "middle"))
    o.append(t(200, 292, "3 numbers per word", 12, MUT, "middle"))
    o.append(t(528, 276, "a note of 5 numbers", 12, MUT, "middle"))
    o.append(t(528, 292, "after every word", 12, MUT, "middle"))
    o.append(t(704, 276, "the last note", 12, MUT, "middle"))
    o.append(t(704, 292, "of each sentence", 12, MUT, "middle"))
    o.append(t(640, 150, "last", 12, ACC_S, "middle"))
    o.append(t(640, 166, "column", 12, ACC_S, "middle"))
    o.append(cap("shapes.py: x is (2, 4, 3), out is (2, 4, 5), h_n is (1, 2, 5); ringed cells are the summary.", 346))
    fig("fig-w08-4-x-out-and-h-n-shapes.svg", "0 0 800 400",
        "out keeps a note for every word; h_n keeps only the last note of each sentence",
        "Left, x drawn as a grid of 2 sentences by 4 words, each cell holding 3 numbers, shape (2, 4, 3). In the middle a "
        "purple nn.RNN box with 3 numbers in and a note of 5. Next, out as a grid of 2 by 4 cells holding 5 numbers each, "
        "shape (2, 4, 5), with the last column ringed. An arrow carries that last column to h_n, two cells of 5 numbers, "
        "shape (1, 2, 5).", o)


# ---------------------------------------------------------------- W8-5  step-by-step distance
def w08_5():
    dist = [0.0000, 0.9854, 0.6620, 0.2906, 0.8842]          # order.py, torch.manual_seed(0)
    wa = ["the", "dog", "bit", "the", "postman"]
    wb = ["the", "postman", "bit", "the", "dog"]
    fa = [0.5728, -0.0141, 0.3677, 0.1722]
    fb = [-0.1963, -0.0411, 0.3475, 0.6072]
    d = [round(a - b, 4) for a, b in zip(fa, fb)]
    ss = sum(v * v for v in d)
    assert round(math.sqrt(ss), 4) == 0.8842 and round(ss, 4) == 0.7819, (ss, d)
    o = [ctitle("How far apart are the two notes after each word?")]
    # left panel
    o.append(rect(20, 62, 420, 290, 12, PANEL, GRID, 2))
    o.append(t(36, 86, "distance between the two sentences' notes", 14, INK, "start"))
    ax, yb, ytop = 72, 262, 112
    ys = lambda v: yb - v / 1.0 * (yb - ytop)
    for v in (0, 0.5, 1.0):
        o.append(line(ax, ys(v), 424, ys(v), GRID, 1.5))
        o.append(t(ax - 8, ys(v) + 4, ("%.1f" % v) if v else "0", 12, MUT, "end"))
    o.append(t(34, 305, "a", 12, MUT, "start"))
    o.append(t(34, 323, "b", 12, MUT, "start"))
    for i, v in enumerate(dist):
        cx = 112 + i * 70
        hh = max(yb - ys(v), 0)
        if hh > 0:
            o.append(sq(cx - 20, ys(v), 40, hh, DATA_F, DATA_S, 3))
        else:
            o.append(line(cx - 20, yb, cx + 20, yb, DATA_S, 3))
        o.append(t(cx, ys(v) - 8, "%.4f" % v, 12, INK, "middle"))
        o.append(t(cx, yb + 20, "word %d" % (i + 1), 12, INK, "middle"))
        o.append(t(cx, 305, wa[i], 12, MUT, "middle"))
        o.append(t(cx, 323, wb[i], 12, MUT, "middle"))
    # right panel
    o.append(rect(456, 62, 324, 290, 12, PANEL, GRID, 2))
    o.append(t(472, 86, "after word 5, by hand", 14, INK, "start"))
    cols = [540, 606, 672, 738]

    def row(y, label, vals, fill=INK):
        out = [t(472, y, label, 14, fill, "start")]
        for c, v in zip(cols, vals):
            s = ("%.4f" % v).replace("-", "&#8722;")
            out.append(t(c + 24, y, s, 12, fill, "end"))
        return out

    o.extend(row(116, "a", fa))
    o.extend(row(138, "b", fb))
    o.append(line(472, 150, 764, 150, GRID, 1.5))
    o.extend(row(172, "a &#8722; b", d, ACC_S))
    o.append(t(472, 210, "square each and add:", 12, MUT, "start"))
    o.append(t(472, 230, "%s" % " + ".join("%.4f" % (v * v) for v in d), 12, INK, "start"))
    o.append(t(472, 250, "= %.4f" % ss, 14, INK, "start"))
    o.append(t(472, 278, "square root: &#8730;%.4f = %.4f" % (ss, math.sqrt(ss)), 14, ACC_S, "start"))
    o.append(t(472, 306, "bag view of a and of b, both:", 12, MUT, "start"))
    o.append(t(472, 324, "[0.7301, &#8722;0.286, &#8722;1.2587]", 12, INK, "start"))
    o.append(cap("From order.py (seed 0). The weights are random, so the notes mean nothing yet.", 376))
    fig("fig-w08-5-distance-between-notes-by-word.svg", "0 0 800 400",
        "The two sentences have the same bag view but their notes sit 0.8842 apart after the last word",
        "Left, five bars of the distance between the two sentences' notes after each word, from order.py: 0.0000, 0.9854, "
        "0.6620, 0.2906 and 0.8842, with the word read in sentence a and sentence b under each bar. Right, the two final "
        "states: a is 0.5728, -0.0141, 0.3677, 0.1722 and b is -0.1963, -0.0411, 0.3475, 0.6072. Their differences are "
        "0.7691, 0.0270, 0.0202 and -0.4350; the squares 0.5915, 0.0007, 0.0004 and 0.1892 add to 0.7819, and its square "
        "root is 0.8842. Both sentences have the bag view 0.7301, -0.286, -1.2587.", o)


# ---------------------------------------------------------------- W8-6  blank unrolled cell, part (c)
def w08_6():
    o = [ctitle("Part (c): fill every pre and every note")]
    o.append(t(400, 76, "x = [1, 1, 0, 0]    W_xh = 1.0    W_hh = 0.5    bias 0", 14, INK, "middle", mono=True))
    cw, gap0, x0 = 120, 45, 108
    cxs = [x0 + i * (cw + gap0) for i in range(4)]
    xs = [1, 1, 0, 0]
    # connectors first
    o.append(arrow(84, 190, cxs[0] - 4, 190, INK, 3))
    for i in range(3):
        o.append(arrow(cxs[i] + cw + 2, 190, cxs[i + 1] - 4, 190, INK, 3))
        o.append(t(cxs[i] + cw + gap0 / 2.0, 178, "note", 12, MUT, "middle"))
    for i in range(4):
        o.append(arrow(cxs[i] + cw / 2.0, 120, cxs[i] + cw / 2.0, 148, INK, 3))
    o.append(sq(36, 172, 44, 36, DATA_F, DATA_S, 2))
    o.append(t(58, 190, "0", 14, INK, "middle", central=True))
    o.append(t(58, 224, "start note", 12, MUT, "middle"))
    for i, cx in enumerate(cxs):
        o.append(sq(cx + cw / 2.0 - 24, 92, 48, 28, DATA_F, DATA_S, 2))
        o.append(t(cx + cw / 2.0, 106, "x = %d" % xs[i], 14, INK, "middle", central=True))
        o.append(rect(cx, 150, cw, 112, 10, MODEL_F, MODEL_S, 3))
        o.append(t(cx + cw / 2.0, 168, "step %d" % (i + 1), 14, INK, "middle"))
        o.append(t(cx + 10, 197, "pre", 14, INK, "start"))
        o.append(rect(cx + 44, 182, 66, 24, 6, PAPER, MUT, 2))
        o.append(t(cx + 10, 237, "note", 14, INK, "start"))
        o.append(rect(cx + 44, 222, 66, 24, 6, PAPER, MUT, 2))
    o.append(t(400, 296, "the same weights in all four boxes: it is one cell, used again", 14, INK, "middle"))
    o.append(t(400, 322, "pre: add 1.0 &#215; x to 0.5 &#215; the old note.   note: press tanh on the pre.", 12, MUT, "middle"))
    o.append(cap("Four decimals. Each note becomes the next step's old note.", 372))
    fig("fig-w08-6-blank-unrolled-cell-part-c.svg", "0 0 800 400",
        "Blank page: unroll the cell for x = [1, 1, 0, 0] and write each pre and note",
        "A blank fill-in figure showing the recurrent cell drawn four times with the same weights, W_xh 1.0 and W_hh 0.5. "
        "The inputs above the four boxes are 1, 1, 0 and 0, the starting note on the left is 0, and arrows labelled note "
        "run from each box to the next. Each box has two empty write-in boxes, one for the pre and one for the note. "
        "No answers are drawn.", o)


# ---------------------------------------------------------------- W9-4  what the eight weeks left behind
def w09_4():
    weeks = [(1, "the coin and the curve", "loss 0.693 when guessing;", "read the whole curve"),
             (2, "SGD and momentum", "steps by hand; running", "average with 0.9"),
             (3, "Adam and typical size", "root-mean-square;", "Adam's first step"),
             (4, "schedules and steps", "what a multiplier does;", "counting steps"),
             (5, "curing overfitting", "dropout in eval mode;", "copy.deepcopy snapshot"),
             (6, "norm, road, clipping", "slope of x + f(x);", "what clipping returns"),
             (7, "the sweep", "bigger than twice", "the spread?"),
             (8, "the recurrent cell", "bag versus order;", "shapes of x, out, h_n")]
    ring = {8: 1, 2: 2, 6: 3}                # tie-break order of the redo rule (student guide, homework step 3)
    o = [ctitle("What Weeks 1 to 8 left behind")]
    for i, (w, topic, l1, l2) in enumerate(weeks):
        c, r = i % 4, i // 4
        x, y = 20 + c * 194, 66 + r * 122
        o.append(rect(x, y, 178, 110, 12, PANEL, GRID, 2))
        o.append(t(x + 14, y + 28, "Week %d" % w, 18, INK, "start"))
        o.append(t(x + 14, y + 52, topic, 14, INK, "start"))
        o.append(t(x + 14, y + 74, l1, 12, MUT, "start"))
        o.append(t(x + 14, y + 92, l2, 12, MUT, "start"))
        if w in ring:
            o.append(rect(x, y, 178, 110, 12, "none", ACC_S, 3))
            o.append(ring_num(x + 156, y + 22, ring[w]))
    o.append(arrow(400, 318, 400, 336, INK, 3))
    o.append(t(400, 358, "Week 10 trains the Week 8 cell and leans most on the ringed weeks, in the order 1, 2, 3.", 14, INK, "middle"))
    fig("fig-w09-4-what-eight-weeks-left-behind.svg", "0 0 800 400",
        "Eight weeks left eight sets of skills, and Week 10 leans hardest on Weeks 8, 2 and 6",
        "Eight boxes in two rows of four, one per week. Week 1: the coin and the curve (loss 0.693 when guessing, read the "
        "whole curve). Week 2: SGD and momentum by hand. Week 3: Adam and typical size. Week 4: schedules and counting steps. "
        "Week 5: curing overfitting. Week 6: norm, road and clipping. Week 7: the sweep and the twice-the-spread rule. "
        "Week 8: the recurrent cell and the shapes of x, out and h_n. Weeks 8, 2 and 6 carry ringed numbers 1, 2 and 3, "
        "and an arrow below points to Week 10.", o)


# ---------------------------------------------------------------- W9-5  the redo line, by hand
def w09_5():
    avail = [11, 10, 10, 9, 8, 8, 7, 12]            # workbook page 9.9 grid, marks available
    redo = [6, 5, 5, 5, 4, 4, 4, 7]                 # workbook page 9.9 grid, 'redo if marks <='
    assert sum(avail) == 75
    for a, r in zip(avail, redo):                   # under 60%: largest whole mark strictly below 0.6 x a
        assert max(k for k in range(a + 1) if k < 0.6 * a - 1e-9) == r, (a, r)
    o = [ctitle("Where each week's redo line sits")]
    yb, u = 262, 11.0                               # 11 px per mark
    x0 = 70
    o.append(line(x0, 96, x0, yb, INK, 2))
    o.append(line(x0, yb, 780, yb, INK, 2))
    for v in (0, 4, 8, 12):
        o.append(line(x0 - 5, yb - v * u, x0, yb - v * u, MUT, 1.5))
        o.append(t(x0 - 9, yb - v * u + 4, str(v), 12, MUT, "end"))
    o.append(trot(36, 180, "marks available", 12))
    for i, (a, r) in enumerate(zip(avail, redo)):
        cx = 118 + i * 88
        o.append(sq(cx - 24, yb - a * u, 48, a * u, DATA_F, DATA_S, 3))
        o.append(t(cx, yb - a * u - 8, str(a), 14, INK, "middle"))
        yl = yb - 0.6 * a * u
        o.append(line(cx - 30, yl, cx + 30, yl, ACC_S, 3, "6 4"))
        o.append(t(cx, yb + 20, "Week %d" % (i + 1), 14, INK, "middle"))
        o.append(t(cx, yb + 38, "0.6 &#215; %d" % a, 12, MUT, "middle"))
        o.append(t(cx, yb + 54, "= %.1f" % (0.6 * a), 12, MUT, "middle"))
        o.append(t(cx, yb + 72, "redo if &#8804; %d" % r, 12, ACC_S, "middle"))
    o.append(t(90, 100, "11 + 10 + 10 + 9 + 8 + 8 + 7 + 12 = 75 marks", 12, INK, "start"))
    o.append(line(440, 96, 476, 96, ACC_S, 3, "6 4"))
    o.append(t(484, 100, "60% of the marks", 12, INK, "start"))
    o.append(cap("A week needs a redo when you earn under 60% of its marks; circle at most two.", 372))
    fig("fig-w09-5-redo-line-by-week.svg", "0 0 800 400",
        "A week needs a redo when you score under 60% of its marks, which is the dashed line",
        "Eight bars of marks available per week: Week 1 is 11, Week 2 is 10, Week 3 is 10, Week 4 is 9, Week 5 is 8, "
        "Week 6 is 8, Week 7 is 7 and Week 8 is 12, adding to 75. A dashed line across each bar marks 60% of its marks: "
        "6.6, 6.0, 6.0, 5.4, 4.8, 4.8, 4.2 and 7.2. Under each bar, redo if marks are at most 6, 5, 5, 5, 4, 4, 4 and 7.", o)


# ---------------------------------------------------------------- W9-6  blank confidence map and bars
def w09_6():
    avail = [11, 10, 10, 9, 8, 8, 7, 12]            # workbook page 9.9 grid
    o = [ctitle("Confidence map: my guess, my mark")]
    ax, yb, ytop = 84, 306, 176
    ys = lambda p: yb - p / 100.0 * (yb - ytop)
    o.append(t(22, 118, "my guess", 12, MUT, "start"))
    o.append(t(22, 134, "before", 12, MUT, "start"))
    o.append(trot(34, 241, "% of the week's marks", 12))
    for p in (0, 20, 40, 60, 80, 100):
        o.append(line(ax, ys(p), 700, ys(p), GRID, 1.5, "6 4" if p else None))
        o.append(t(ax - 8, ys(p) + 4, "%d%%" % p, 12, MUT, "end"))
    o.append(line(ax, ys(60), 700, ys(60), ACC_S, 3, "6 4"))
    o.append(t(708, ys(60) - 2, "60%", 12, ACC_S, "start"))
    o.append(t(708, ys(60) + 14, "redo line", 12, ACC_S, "start"))
    o.append(line(ax, ytop, ax, yb, INK, 2))
    for i in range(8):
        cx = 124 + i * 78
        for k, letter in enumerate("YMN"):
            o.append(circ(cx - 26 + k * 26, 126, 11, PAPER, MUT, 2))
            o.append(t(cx - 26 + k * 26, 126, letter, 12, MUT, "middle", central=True))
        o.append(rect(cx - 22, ytop, 44, yb - ytop, 4, "none", MUT, 2))
        o.append(t(cx, yb + 22, "Week %d" % (i + 1), 14, INK, "middle"))
        o.append(t(cx, yb + 40, "of %d" % avail[i], 12, MUT, "middle"))
    o.append(t(ax + 310, 160, "Y = yes   M = maybe   N = no", 12, MUT, "middle"))
    o.append(cap("Ring your page 9.1 guess, shade each bar to your %, then ring at most two weeks.", 372))
    fig("fig-w09-6-blank-confidence-map-and-marks.svg", "0 0 800 400",
        "Blank page: for each week ring the guess you made, shade your percentage, and pick at most two redos",
        "A blank fill-in figure with eight columns, Week 1 to Week 8. Above each column are three empty circles marked "
        "Y, M and N for yes, maybe and no. Below them an empty bar track runs from 0% to 100% with a dashed 60% redo line. "
        "Under each column is the week number and its marks available: 11, 10, 10, 9, 8, 8, 7 and 12. No answers are drawn.", o)


def build():
    for f in (w07_4, w07_5, w07_6, w08_4, w08_5, w08_6, w09_4, w09_5, w09_6):
        f()
    return FIGS

"""Block 2 (weeks 4, 5, 6) extra figures: mental model (-4), worked numbers (-5), blank fill-in (-6).
Every number is copied from the week's printed output or is a hand sum shown beside it (STYLE.md 2.1).

W4-4  840 // 64 = 13 and 840 // 512 = 1 (student guide section 4; batches.py first table: 13 -> 780, 1 -> 60);
      8 left over = 840 - 13 x 64 (832, printed in the lesson); 328 = 840 - 512 (hand sum)
W4-5  hook.py (lr 0.03, seeds 0-4, final validation accuracy %) and the gentle-rate lines (lr 0.003, mean,
      lowest, highest of final validation loss) printed in Part 4
W4-6  blank graph paper for workbook Page 4.3 M5 (axes only; peak 0.02, T = 50)
W5-4  the four cures; 0.9991 = 1 - 0.003 x 0.3 (lesson arithmetic)
W5-5  table.py seed 0 block (best val, final val); gaps are hand subtractions printed beside the bars
W5-6  blank number line for workbook Page 5.5 (b), 0.10 to 0.30, five cure rows
W6-4  layer norm on the row 2, 4, 6, 8 (lesson part D: mean 5, spread 2.236, -1.342 -0.447 0.447 1.342)
W6-5  small_batch.py printed table (seed 0, 10 epochs)
W6-6  blank block diagram for workbook Page 6.1 (the block read in student guide section 4)
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


MINUS = "&#8722;"


# ---------------------------------------------------------------- W4-4  a batch is a slice
def w04_4():
    x0, W = 100, 600.0
    sc = W / 840.0
    o = [ctitle("Whole batches only: the leftovers are dropped")]
    # row A: batch 64
    o.append(t(x0, 88, "batch 64: the 840 training points, shuffled", 14, INK, "start"))
    ya, h = 106, 44
    for i in range(13):
        o.append(rect(x0 + i * 64 * sc, ya, 64 * sc, h, 0, DATA_F, DATA_S, 2))
        o.append(t(x0 + (i + 0.5) * 64 * sc, ya + h / 2.0, str(i + 1), 12, INK, "middle", central=True))
    lx = x0 + 13 * 64 * sc
    o.append(rect(lx, ya, 8 * sc, h, 0, PAPER, MUT, 2, "4 3"))
    o.append(bracket(x0, lx, ya + h + 6, 8, ACC_S, True))
    o.append(t((x0 + lx) / 2.0, ya + h + 34, "13 whole batches = 13 steps per epoch", 14, ACC_S, "middle", weight="600"))
    o.append(line(lx + 3, ya + h + 4, lx + 24, ya + h + 24, MUT, 1.5))
    o.append(t(780, ya + h + 34, "8 left over, dropped", 12, MUT, "end"))
    o.append(t(x0, ya + h + 58, "840 // 64 = 13    13 steps &#215; 60 epochs = 780 steps", 14, INK, "start", mono=True))
    # row B: batch 512
    yb = 246
    o.append(t(x0, yb - 18, "batch 512: the same 840 points", 14, INK, "start"))
    o.append(rect(x0, yb, 512 * sc, h, 0, DATA_F, DATA_S, 2))
    o.append(t(x0 + 256 * sc, yb + h / 2.0, "batch 1 (512 points)", 12, INK, "middle", central=True))
    o.append(rect(x0 + 512 * sc, yb, 328 * sc, h, 0, PAPER, MUT, 2, "4 3"))
    o.append(t(x0 + (512 + 164) * sc, yb + h / 2.0, "328 left over", 12, MUT, "middle", central=True))
    o.append(bracket(x0, x0 + 512 * sc, yb + h + 6, 8, ACC_S, True))
    o.append(t(x0 + 256 * sc, yb + h + 34, "1 whole batch = 1 step per epoch", 14, ACC_S, "middle", weight="600"))
    o.append(t(x0, yb + h + 58, "840 // 512 = 1    1 step &#215; 60 epochs = 60 steps", 14, INK, "start", mono=True))
    o.append(cap("Leftover points are different ones each epoch, because the order is reshuffled."))
    fig("fig-w04-4-epoch-cut-into-batches.svg", "0 0 800 400",
        "A batch size decides how many steps one epoch is: whole batches only, the remainder is dropped",
        "Two bars, each the 840 shuffled training points. The first is cut into 13 numbered batches of 64 plus a "
        "small dashed piece of 8 left over: 13 steps per epoch and 13 times 60 equals 780 steps. The second is one "
        "batch of 512 plus a long dashed piece of 328 left over: 1 step per epoch and 60 steps in 60 epochs.", o)


# ---------------------------------------------------------------- W4-5  two rates, five seeds
def w04_5():
    o = [ctitle("A falling rate rescued a bad rate, not a good one")]
    # panel A: lr 0.03, final validation accuracy %, seeds 0-4 (hook.py, Start Here)
    A = [("constant", [46.9, 50.6, 53.1, 98.1, 97.2], "69.2"),
         ("warmup only", [99.2, 67.5, 76.4, 98.1, 86.7], "85.6"),
         ("cosine only", [98.9] * 5, "98.9"),
         ("warmup+cosine", [99.2, 98.9, 98.9, 98.9, 98.9], "98.9")]
    o.append(rect(20, 62, 372, 290, 12, PANEL, GRID, 2))
    o.append(t(34, 86, "A  too-big rate, lr = 0.03", 18, INK, "start"))
    o.append(t(34, 106, "dot: one seed's final accuracy %", 12, MUT, "start"))
    ax = lambda a: 168 + (a - 40) / 60.0 * 200
    for a in (40, 60, 80, 100):
        o.append(line(ax(a), 120, ax(a), 322, GRID, 1.5, "6 4"))
        o.append(t(ax(a), 340, str(a), 12, MUT, "middle"))
    o.append(line(ax(46.9), 120, ax(46.9), 322, MUT, 2, "2 4"))
    o.append(t(ax(46.9) + 4, 118, "coin 46.9", 12, MUT, "start"))
    for i, (name, vals, mean) in enumerate(A):
        yc = 140 + i * 50
        base = yc + 20
        o.append(t(34, yc - 4, name, 14, INK, "start"))
        o.append(t(34, yc + 12, "mean " + mean, 12, MUT, "start"))
        o.append(line(168, base, 368, base, GRID, 1.5))
        placed = []
        for v in sorted(vals):
            lvl = sum(1 for p in placed if abs(ax(p) - ax(v)) < 9)
            placed.append(v)
            o.append(circ(ax(v), base - 7 - 9 * lvl, 4.5, DATA_F, DATA_S, 2))
        mx = float(mean)
        o.append(mark("diamond", ax(mx), base, 4, ACC_S, ACC_F, 2))
    # panel B: lr 0.003, mean final validation loss with lowest..highest (Part 4)
    B = [("constant", 0.039, 0.030, 0.050), ("warmup only", 0.043, 0.031, 0.057),
         ("cosine only", 0.035, 0.032, 0.040), ("warmup+cosine", 0.037, 0.029, 0.045)]
    o.append(rect(408, 62, 372, 290, 12, PANEL, GRID, 2))
    o.append(t(422, 86, "B  gentle rate, lr = 0.003", 18, INK, "start"))
    o.append(t(422, 106, "bar: lowest to highest, diamond: mean", 12, MUT, "start"))
    bx = lambda v: 548 + (v - 0.02) * 5000
    for v in (0.02, 0.03, 0.04, 0.05, 0.06):
        o.append(line(bx(v), 120, bx(v), 322, GRID, 1.5, "6 4"))
        o.append(t(bx(v), 340, "%.2f" % v, 12, MUT, "middle"))
    for i, (name, mean, lo, hi) in enumerate(B):
        yc = 140 + i * 50
        o.append(t(422, yc - 4, name, 14, INK, "start"))
        o.append(t(422, yc + 12, "mean %.3f" % mean, 12, MUT, "start"))
        o.append(rect(bx(lo), yc - 3, bx(hi) - bx(lo), 14, 4, DATA_F, DATA_S, 2))
        o.append(mark("diamond", bx(mean), yc + 4, 4, ACC_S, ACC_F, 2))
    o.append(cap("Five seeds per row. At the gentle rate every bar overlaps every other."))
    fig("fig-w04-5-two-rates-five-seeds.svg", "0 0 800 400",
        "At a too-big rate a falling schedule rescued every seed; at the gentle rate the schedules did not separate",
        "Two panels. A, learning rate 0.03, final validation accuracy over seeds 0 to 4: constant 46.9, 50.6, 53.1, "
        "98.1, 97.2 (mean 69.2); warmup only 99.2, 67.5, 76.4, 98.1, 86.7 (mean 85.6); cosine only 98.9 five times "
        "(mean 98.9); warmup plus cosine 99.2 and 98.9 four times (mean 98.9). A dotted line marks the coin, 46.9. "
        "B, learning rate 0.003, mean final validation loss with lowest to highest bars: constant 0.039 (0.030 to "
        "0.050), warmup only 0.043 (0.031 to 0.057), cosine only 0.035 (0.032 to 0.040), warmup plus cosine 0.037 "
        "(0.029 to 0.045).", o)


# ---------------------------------------------------------------- W4-6  blank graph paper
def w04_6():
    x0, x1, yb, yt = 110, 730, 320, 86
    X = lambda s: x0 + s / 50.0 * (x1 - x0)
    Y = lambda v: yb - v / 0.02 * (yb - yt)
    o = [ctitle("Graph paper for M5: plot both rate columns")]
    for s in range(0, 51, 5):
        o.append(line(X(s), yt, X(s), yb, GRID, 1.5, "6 4" if s else None))
        if s % 10 == 0:
            o.append(line(X(s), yb, X(s), yb + 5, MUT, 1.5))
            o.append(t(X(s), yb + 20, str(s), 12, MUT, "middle"))
    for k in range(0, 11):
        v = k * 0.002
        o.append(line(x0, Y(v), x1, Y(v), GRID, 1.5, "6 4" if k else None))
        if k % 2 == 0:
            o.append(line(x0 - 5, Y(v), x0, Y(v), MUT, 1.5))
            o.append(t(x0 - 9, Y(v) + 4, ("%.3f" % v).rstrip("0").rstrip(".") if v else "0", 12, MUT, "end"))
    o.append(line(x0, yb, x1, yb, INK, 2))
    o.append(line(x0, yt, x0, yb, INK, 2))
    o.append(t((x0 + x1) / 2.0, yb + 36, "step (0 to 50)", 12, MUT, "middle"))
    o.append(trot(44, (yb + yt) / 2.0, "rate (0 to 0.02)", 12))
    # empty legend slots: the learner draws one sample line in each colour
    lx, ly = 470, 62
    o.append(rect(lx, ly - 12, 260, 24, 6, PAPER, GRID, 2))
    o.append(line(lx + 10, ly, lx + 40, ly, MUT, 3, "6 4"))
    o.append(t(lx + 46, ly + 4, "cosine only", 12, INK, "start"))
    o.append(line(lx + 140, ly, lx + 170, ly, MUT, 3))
    o.append(t(lx + 176, ly + 4, "warm+cos", 12, INK, "start"))
    o.append(cap("Colour each sample line to match the pen you use, then plot nine points on each.", 376))
    fig("fig-w04-6-blank-rate-graph.svg", "0 0 800 400",
        "Blank axes for plotting the two hand-built learning-rate schedules",
        "Empty graph paper. The bottom axis is the step from 0 to 50 with a faint line every 5 steps. The side axis "
        "is the rate from 0 to 0.02 with a faint line every 0.002. A small key at the top right has a dashed sample "
        "line for cosine only and a solid sample line for warm plus cosine, to be coloured in. Nothing is plotted.", o)


# ---------------------------------------------------------------- W5-4  where each cure acts
def w05_4():
    o = [ctitle("Each cure acts on a different part of training")]
    bx = [(40, "120 training points", DATA_F, DATA_S), (300, "the network", MODEL_F, MODEL_S),
          (560, "weight update (AdamW)", PANEL, INK)]
    for x, lab, fl, st in bx:
        o.append(rect(x, 84, 200, 64, 12, fl, st, 3))
        o.append(t(x + 100, 116, lab, 16, INK, "middle", central=True))
    o.append(arrow(240, 116, 298, 116))
    o.append(arrow(500, 116, 558, 116))
    cards = [(40, "1", "Augmentation (jitter)", "changes the data:", "shaken copies each epoch"),
             (300, "2", "Dropout", "changes how it trains:", "zero a share, survivors &#215; 1/(1 &#8722; p)"),
             (560, "3", "Weight decay", "changes the update:", "every weight &#215; 0.9991")]
    for x, n, a, b, c in cards:
        o.append(line(x + 100, 150, x + 100, 190, ACC_S, 2, "4 3"))
        o.append(rect(x, 190, 200, 86, 10, PAPER, ACC_S, 3))
        o.append(ring_num(x + 18, 208, n))
        o.append(t(x + 36, 213, a, 14, INK, "start", weight="600"))
        o.append(t(x + 14, 238, b, 12, MUT, "start"))
        o.append(t(x + 14, 258, c, 12, INK, "start"))
    o.append(rect(40, 296, 720, 56, 10, PAPER, ACC_S, 3))
    o.append(ring_num(58, 314, 4))
    o.append(t(76, 319, "Early stopping", 14, INK, "start", weight="600"))
    o.append(t(54, 340, "changes nothing inside: keep the best weights so far, stop after `patience` epochs without a new best", 12, INK, "start"))
    o.append(cap("Weight decay: 1 &#8722; 0.003 &#215; 0.3 = 0.9991 per step, from the lesson's arithmetic."))
    fig("fig-w05-4-where-each-cure-acts.svg", "0 0 800 400",
        "Four cures for memorising, each acting on a different part of the training run",
        "Three boxes joined by arrows: 120 training points, the network, and the weight update (AdamW). Below each "
        "a ringed card names a cure: 1 augmentation acts on the data with shaken copies each epoch; 2 dropout acts on "
        "how the network trains by zeroing a share and scaling survivors by 1 over 1 minus p; 3 weight decay acts on "
        "the update by multiplying every weight by 0.9991. A wide card 4 below all of them says early stopping "
        "changes nothing inside: it keeps the best weights and stops after patience epochs without a new best.", o)


# ---------------------------------------------------------------- W5-5  seed 0, best vs final
def w05_5():
    rows = [("no cure", 0.179, 0.906), ("early stop (p=25)", 0.179, 0.227), ("dropout 0.3", 0.201, 0.634),
            ("weight decay 0.3", 0.140, 0.274), ("jitter 0.1", 0.130, 0.318)]
    o = [ctitle("Seed 0: the last epoch against the best epoch")]
    x0, sc = 220, 380 / 1.0
    X = lambda v: x0 + v * sc
    o.append(rect(30, 56, 740, 26, 8, PAPER, GRID, 2))
    o.append(rect(44, 63, 26, 12, 3, DATA_F, DATA_S, 2))
    o.append(t(78, 74, "best val (picked with hindsight)", 12, INK, "start"))
    o.append(rect(300, 63, 26, 12, 3, PAPER, DATA_S, 2, "4 3"))
    o.append(t(334, 74, "final val (early stop: at the stop)", 12, INK, "start"))
    o.append(t(740, 74, "gap = final &#8722; best", 12, INK, "end"))
    for v in (0.0, 0.25, 0.5, 0.75, 1.0):
        o.append(line(X(v), 94, X(v), 332, GRID, 1.5, "6 4"))
        o.append(t(X(v), 350, "%.2f" % v, 12, MUT, "middle"))
    big = max(f - b for _, b, f in rows)
    for i, (name, b, f) in enumerate(rows):
        yc = 114 + i * 48
        o.append(t(40, yc + 12, name, 14, INK, "start"))
        o.append(rect(x0, yc - 14, b * sc, 16, 4, DATA_F, DATA_S, 2))
        o.append(t(x0 + b * sc + 6, yc - 2, "%.3f" % b, 12, INK, "start"))
        o.append(rect(x0, yc + 4, f * sc, 16, 4, PAPER, DATA_S, 2, "4 3"))
        o.append(t(x0 + f * sc + 6, yc + 16, "%.3f" % f, 12, MUT, "start"))
        g = f - b
        top = abs(g - big) < 1e-9
        o.append(t(740, yc + 12, "+%.3f" % g, 14, ACC_S if top else INK, "end", weight="600" if top else None))
    o.append(cap("One seed only; Figure 5.2 has five. Gaps are subtractions of the printed values."))
    fig("fig-w05-5-seed-zero-best-vs-final.svg", "0 0 800 400",
        "Every cure ends above its own best validation loss; the control ends furthest above",
        "Five rows, one per cure, from the seed-0 table. Each has a solid bar for best validation loss and a dashed bar "
        "for final validation loss. No cure 0.179 and 0.906, gap 0.727. Early stop 0.179 and 0.227 at the stop, gap "
        "0.048. Dropout 0.3: 0.201 and 0.634, gap 0.433. Weight decay 0.3: 0.140 and 0.274, gap 0.134. Jitter 0.1: "
        "0.130 and 0.318, gap 0.188.", o)


# ---------------------------------------------------------------- W5-6  blank number line
def w05_6():
    names = ["no cure", "early stop (p=25)", "dropout 0.3", "weight decay 0.3", "jitter 0.1"]
    x0, x1 = 230, 750
    X = lambda v: x0 + (v - 0.10) / 0.20 * (x1 - x0)
    o = [ctitle("Draw the five best-val ranges")]
    top, rh = 96, 44
    for i, n in enumerate(names):
        y = top + i * rh
        o.append(rect(30, y, 740, rh, 0, PANEL if i % 2 == 0 else PAPER, GRID, 1.5))
        o.append(t(42, y + rh / 2.0, n, 14, INK, "start", central=True))
    yb = top + 5 * rh
    for k in range(0, 21):
        v = 0.10 + k * 0.01
        major = k % 5 == 0
        o.append(line(X(v), top, X(v), yb, GRID, 1.5, "6 4" if major else "2 4"))
        o.append(line(X(v), yb, X(v), yb + (7 if major else 4), MUT, 1.5))
        if major:
            o.append(t(X(v), yb + 24, "%.2f" % v, 12, MUT, "middle"))
    o.append(line(x0, yb, x1, yb, INK, 2))
    o.append(t((x0 + x1) / 2.0, yb + 44, "best val over seeds 0 to 4", 12, MUT, "middle"))
    o.append(rect(230, 60, 300, 24, 6, PAPER, GRID, 2))
    o.append(rect(240, 67, 40, 10, 3, PAPER, MUT, 2))
    o.append(t(288, 77, "lowest .. highest", 12, INK, "start"))
    o.append(mark("diamond", 410, 72, 4, MUT, PAPER, 2))
    o.append(t(422, 77, "mean", 12, INK, "start"))
    o.append(cap("A bar from each row's lowest to its highest, a diamond at its mean.", 376))
    fig("fig-w05-6-blank-range-bars.svg", "0 0 800 400",
        "Blank number line from 0.10 to 0.30 with a row for each of the five cures, for drawing the best-val ranges",
        "Empty chart. Five labelled rows (no cure, early stop p equals 25, dropout 0.3, weight decay 0.3, jitter 0.1) "
        "share one bottom axis from 0.10 to 0.30, with a faint line every 0.01 and a labelled line every 0.05. A key "
        "at the top shows an empty bar for lowest to highest and a diamond for the mean. Nothing is drawn in the rows.", o)


# ---------------------------------------------------------------- W6-4  rows versus columns
def w06_4():
    o = [ctitle("The two norms take their mean from different places")]
    cw, ch = 56, 36

    def grid(gx, gy, hi_row=None, hi_col=None, vals=None):
        out = []
        for c in range(4):
            out.append(t(gx + (c + 0.5) * cw, gy - 8, str(c + 1), 12, MUT, "middle"))
        for r in range(4):
            out.append(t(gx - 10, gy + (r + 0.5) * ch, "ABCD"[r], 12, MUT, "end", central=True))
        for r in range(4):
            for c in range(4):
                on = (hi_row == r) or (hi_col == c)
                out.append(sq(gx + c * cw, gy + r * ch, cw, ch, ACC_F if on else PANEL,
                              ACC_S if on else GRID, 3 if on else 2))
                if vals and on:
                    out.append(t(gx + (c + 0.5) * cw, gy + (r + 0.5) * ch, vals[c], 14, INK, "middle", central=True))
        out.append(t(gx + 2 * cw, gy - 26, "features (columns)", 12, MUT, "middle"))
        out.append(trot(gx - 30, gy + 2 * ch, "examples (rows)", 12))
        return out

    # left: layer norm, row B
    lx, gy = 70, 128
    o.append(t(lx + 2 * cw, 84, "Layer norm: one row at a time", 18, INK, "middle"))
    o.extend(grid(lx, gy, hi_row=1, vals=["2", "4", "6", "8"]))
    o.append(arrow(lx + 2 * cw, gy + 4 * ch + 6, lx + 2 * cw, gy + 4 * ch + 30))
    yy = gy + 4 * ch + 36
    for c, v in enumerate([MINUS + "1.342", MINUS + "0.447", "0.447", "1.342"]):
        o.append(sq(lx + c * cw, yy, cw, 30, DATA_F, DATA_S, 2))
        o.append(t(lx + (c + 0.5) * cw, yy + 15, v, 12, INK, "middle", central=True, mono=True))
    o.append(t(lx + 2 * cw, yy + 52, "mean 5, spread 2.236, from this row alone", 12, MUT, "middle"))
    # right: batch norm, column 2
    rx = 480
    o.append(t(rx + 2 * cw, 84, "Batch norm: one column at a time", 18, INK, "middle"))
    o.extend(grid(rx, gy, hi_col=1))
    o.append(arrow(rx + 1.5 * cw, gy + 4 * ch + 6, rx + 1.5 * cw, gy + 4 * ch + 30))
    o.append(rect(rx, yy, 4 * cw, 30, 8, PANEL, GRID, 2))
    o.append(t(rx + 2 * cw, yy + 15, "same arithmetic, down the column", 12, INK, "middle", central=True))
    o.append(t(rx + 2 * cw, yy + 52, "mean and spread need the other examples", 12, MUT, "middle"))
    o.append(cap("Highlighted cells are the numbers that one normalisation uses together."))
    fig("fig-w06-4-rows-versus-columns.svg", "0 0 800 400",
        "Layer norm takes its mean and spread from one example's row; batch norm takes them from one feature's column across the batch",
        "Two grids of four examples (rows A to D) by four features (columns 1 to 4). In the left grid row B is "
        "highlighted and holds 2, 4, 6, 8; an arrow leads to the normalised row minus 1.342, minus 0.447, 0.447, "
        "1.342, with a note that mean 5 and spread 2.236 come from that row alone. In the right grid column 2 is "
        "highlighted; an arrow leads to a box saying the same arithmetic runs down the column, so the mean and "
        "spread need the other examples.", o)


# ---------------------------------------------------------------- W6-5  hook table
def w06_5():
    # small_batch.py printed table: seed 0, 10 epochs (none, batch norm, layer norm)
    T = [(64, 98.3, 96.9, 97.8), (16, 96.9, 98.6, 98.3), (4, 96.4, 63.3, 98.3), (2, 97.8, 46.9, 97.2)]
    o = [ctitle("Batch norm is the one that fails at batch size 2")]
    x0, yb, yt = 100, 316, 104
    ay = lambda a: yb - a / 100.0 * (yb - yt)
    for a in (0, 100):
        o.append(line(x0, ay(a), 780, ay(a), GRID, 1.5, "6 4" if a else None))
        o.append(t(x0 - 8, ay(a) + 4, "%d%%" % a, 12, MUT, "end"))
    o.append(line(x0, ay(46.9), 780, ay(46.9), MUT, 2, "2 4"))
    o.append(t(x0 - 8, ay(46.9) - 6, "coin", 12, MUT, "end"))
    # key
    o.append(rect(100, 62, 556, 24, 6, PAPER, GRID, 2))
    o.append(rect(110, 68, 22, 12, 2, PANEL, MUT, 2, "4 3"))
    o.append(t(138, 78, "no norm", 12, INK, "start"))
    o.append(rect(222, 68, 22, 12, 2, DATA_F, DATA_S, 2))
    o.append(t(250, 78, "batch norm", 12, INK, "start"))
    o.append(rect(352, 68, 22, 12, 2, MODEL_F, MODEL_S, 2))
    o.append(t(380, 78, "layer norm", 12, INK, "start"))
    o.append(t(648, 78, "seed 0, 10 epochs", 12, MUT, "end"))
    bw = 44
    for i, (bs, n, b, l) in enumerate(T):
        gx = x0 + 16 + i * 166
        for j, (v, fl, st, da) in enumerate(((n, PANEL, MUT, "4 3"), (b, DATA_F, DATA_S, None), (l, MODEL_F, MODEL_S, None))):
            x = gx + j * (bw + 4)
            o.append(rect(x, ay(v), bw, yb - ay(v), 2, fl, st, 2, da))
            odd = v < 70
            o.append(t(x + bw / 2.0, ay(v) - 6, "%.1f" % v, 12, ACC_S if odd else INK, "middle", weight="600" if odd else None))
        o.append(t(gx + 1.5 * bw + 4, yb + 20, "batch %d" % bs, 14, INK, "middle"))
    o.append(line(x0, yt, x0, yb, INK, 2))
    o.append(line(x0, yb, 780, yb, INK, 2))
    o.append(t(440, yb + 36, "validation accuracy after 10 epochs; batch 4 is one seed, the noisiest cell", 12, MUT, "middle"))
    o.append(cap("Batch norm at batch size 2 lands on the coin, 46.9%. Layer norm and no norm do not.", 376))
    fig("fig-w06-5-norm-by-batch-size.svg", "0 0 800 400",
        "Shrinking the batch broke batch norm and left layer norm and no norm alone",
        "Grouped bars of validation accuracy after 10 epochs, seed 0, for no norm, batch norm and layer norm. Batch "
        "size 64: 98.3, 96.9, 97.8. Batch size 16: 96.9, 98.6, 98.3. Batch size 4: 96.4, 63.3, 98.3. Batch size 2: "
        "97.8, 46.9, 97.2. A dotted line marks the coin, 46.9 percent, which the batch norm bar at batch size 2 "
        "sits on.", o)


# ---------------------------------------------------------------- W6-6  blank block
def w06_6():
    o = [ctitle("Name the parts of the block")]
    y0, h = 196, 60
    yc = y0 + h / 2.0
    o.append(circ(44, yc, 24, DATA_F, DATA_S, 3))
    o.append(t(44, yc, "x", 16, INK, "middle", central=True, mono=True))
    xs = [104, 228, 352, 476]
    for i, x in enumerate(xs):
        o.append(rect(x, y0, 100, h, 10, PAPER, MODEL_S, 3))
        o.append(ring_num(x + 50, yc, i + 1))
    o.append(arrow(68, yc, 102, yc))
    for i in range(3):
        o.append(arrow(xs[i] + 100, yc, xs[i + 1] - 2, yc))
    pcx = 660
    o.append(arrow(576, yc, pcx - 26, yc))
    o.append(ring_num(618, yc - 22, 7))
    o.append(circ(pcx, yc, 24, PAPER, INK, 3))
    o.append(ring_num(pcx, yc, 6))
    o.append(arrow(pcx + 26, yc, 724, yc))
    o.append(t(730, yc + 5, "out", 14, INK, "start", mono=True))
    # the road
    o.append(path("M44 %s V120 H%s V%s" % (f2(yc - 24), f2(pcx), f2(yc - 28)), "none", INK, 3))
    o.append(head(pcx, yc - 26, 90, INK, 3))
    o.append(ring_num(352, 120, 5))
    o.append(cap("Write the number's name on the page: each ring marks one part of the block."))
    fig("fig-w06-6-blank-block.svg", "0 0 800 400",
        "A block with its parts unnamed: four boxes in a row, a plus circle, and an arc that skips round them",
        "Blank block diagram. An input x on the left feeds four empty boxes in a row, ringed 1 to 4, then an arrow "
        "ringed 7 into a circle ringed 6, and the circle sends the result out. A long arc ringed 5 leaves x, passes "
        "over the four boxes and joins the circle from above. The boxes, the arrows and the circle carry only "
        "numbers, no names.", o)


def build():
    for f in (w04_4, w04_5, w04_6, w05_4, w05_5, w05_6, w06_4, w06_5, w06_6):
        f()
    return FIGS

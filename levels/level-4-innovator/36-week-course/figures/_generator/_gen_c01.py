"""Block C1 (weeks 1, 2, 3) extra figures: a mental-model figure, a worked-numbers figure and a
blank workbook figure per week. Every number is copied from the week's printed output or is a
hand sum printed beside it (STYLE.md 2.1).

W1  student-guide/week-01.md Step 3 (epoch table, six runs, seed 0) and Step 5 (accuracies);
    the ten knobs and four set-up arguments are the run() signature (workbook page 1.4 key)
W2  student-guide/week-02.md section 4 (steady / flipping v lists) and Step 6 (verdict table);
    the blank is workbook page 2.8 (start w = 2.0), no values drawn
W3  student-guide/week-03.md section 3 and Step 1 row 1 (g 2.0, m 0.2, s 0.004, ...);
    Step 6 (weight decay on two weights, hand sum 0.99 ** 10 = 0.9044);
    the blank is workbook page 3.7 (first step against gradient size), no points drawn
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


def box(x, y, w, h, l1, l2=None, fill=DATA_F, stroke=DATA_S, sw=2, dash=None, mono1=True):
    o = [rect(x, y, w, h, 8, fill, stroke, sw, dash)]
    if l2:
        o.append(t(x + w / 2.0, y + h / 2.0 - 9, l1, 14, INK, "middle", mono=mono1, central=True))
        o.append(t(x + w / 2.0, y + h / 2.0 + 11, l2, 12, MUT, "middle", central=True))
    else:
        o.append(t(x + w / 2.0, y + h / 2.0, l1, 14, INK, "middle", mono=mono1, central=True))
    return "\n  ".join(o)


# ---------------------------------------------------------------- W1-4  ten knobs, one witness
def w01_4():
    KNOBS = ["lr", "batch_size", "optimizer", "weight_decay", "dropout",
             "norm", "residual", "schedule", "warmup_frac", "clip"]          # run() signature
    SETUP = ["depth", "epochs", "seed", "verbose"]
    assert len(KNOBS) == 10 and len(SETUP) == 4
    o = [ctitle("Ten knobs, one harness, one witness")]
    o.append(rect(20, 62, 560, 170, 12, PANEL, GRID, 2))
    o.append(t(36, 86, "ten knobs: they change how it learns", 14, INK, "start"))
    for i, k in enumerate(KNOBS):
        r, c = divmod(i, 5)
        x, y = 30 + c * 110, 102 + r * 42
        if k == "lr":
            o.append(rect(x, y, 104, 32, 6, ACC_F, ACC_S, 4))
        else:
            o.append(rect(x, y, 104, 32, 6, PAPER, DATA_S, 2))
        o.append(t(x + 52, y + 16, k, 12, INK, "middle", mono=True, central=True))
    o.append(t(36, 206, "lr (ringed): the only knob that moves this week", 14, ACC_S, "start"))
    o.append(rect(600, 62, 180, 170, 12, PANEL, GRID, 2, "6 4"))
    o.append(t(690, 86, "set-up: held fixed", 14, INK, "middle"))
    for i, k in enumerate(SETUP):
        o.append(chip(630, 98 + i * 30, 120, k, GRID, PAPER, 12, 26))
    o.append(arrow(300, 234, 300, 262, INK, 3))
    o.append(box(20, 264, 560, 56, "run(...)", "the harness: the same code every time", MODEL_F, MODEL_S, 3))
    o.append(arrow(582, 292, 618, 292, INK, 3))
    # the witness: run D (lr=1e-3), training loss at epochs 0,5,10,20,40,59 (student guide Step 3)
    ep = [0, 5, 10, 20, 40, 59]
    ls = [0.691, 0.399, 0.082, 0.021, 0.011, 0.018]
    X = lambda e: 636 + e / 59.0 * 130
    Y = lambda v: 322 - v / 0.8 * 56
    o.append(rect(620, 250, 160, 90, 8, PAPER, DATA_S, 2))
    o.append(line(636, Y(0.693), 766, Y(0.693), GRID, 1.5, "6 4"))
    o.append(poly([(X(e), Y(v)) for e, v in zip(ep, ls)], "none", DATA_S, 3))
    for e, v in zip(ep, ls):
        o.append(circ(X(e), Y(v), 3, PAPER, DATA_S, 2))
    o.append(t(700, 262, "loss curve", 12, INK, "middle"))
    o.append(t(766, Y(0.693) - 5, "0.693", 12, MUT, "end"))
    o.append(cap("Change one knob at a time, so the loss curve is the witness.", 374))
    fig("fig-w01-4-ten-knobs-one-witness", "0 0 800 400",
        "Ten knobs and four set-up arguments feed one harness; changing one knob at a time makes the loss curve the witness",
        "A panel of ten knob names (lr, batch_size, optimizer, weight_decay, dropout, norm, residual, schedule, warmup_frac, clip) "
        "with lr ringed as the only one that moves this week, and a dashed panel of four fixed set-up names (depth, epochs, seed, verbose). "
        "An arrow leads from the knobs into a box labelled run, the harness, and a second arrow leads to a small loss curve that falls from "
        "0.691 below a dashed line at 0.693.", o)


# ---------------------------------------------------------------- W1-5  the epoch table, shaded
def w01_5():
    RUNS = [("A", "1e-06", [0.694, 0.694, 0.694, 0.694, 0.694, 0.693]),
            ("B", "1e-05", [0.694, 0.694, 0.693, 0.692, 0.689, 0.683]),
            ("C", "0.0001", [0.694, 0.688, 0.655, 0.575, 0.166, 0.077]),
            ("D", "0.001", [0.691, 0.399, 0.082, 0.021, 0.011, 0.018]),
            ("E", "0.01", [0.658, 0.052, 0.041, 0.027, 0.021, 0.013]),
            ("F", "0.1", [12.786, 0.520, 0.612, 0.694, 0.695, 0.693])]       # student guide Step 3
    EPS = [0, 5, 10, 20, 40, 59]
    o = [ctitle("Training loss at six epochs, six learning rates")]
    x0, cw, y0, rh = 150, 100, 92, 34
    o.append(t(x0 - 14, y0 - 12, "epoch", 12, MUT, "end"))
    for j, e in enumerate(EPS):
        o.append(t(x0 + j * cw + cw / 2.0, y0 - 12, str(e), 14, INK, "middle"))
    for i, (L, lr, vals) in enumerate(RUNS):
        y = y0 + i * rh
        o.append(t(x0 - 14, y + rh / 2.0, "%s  lr=%s" % (L, lr), 12, INK, "end", mono=True, central=True))
        for j, v in enumerate(vals):
            x = x0 + j * cw
            if v > 1.0:
                o.append(sq(x, y, cw, rh, BAD_F, BAD_S, 3))
                o.append(t(x + cw / 2.0 - 8, y + rh / 2.0, "%.3f" % v, 14, INK, "middle", mono=True, central=True, weight="700"))
                o.append(cross(x + cw - 14, y + rh / 2.0, 5))
            elif v >= 0.68:
                o.append(sq(x, y, cw, rh, PANEL, GRID, 2))
                o.append(t(x + cw / 2.0, y + rh / 2.0, "%.3f" % v, 14, INK, "middle", mono=True, central=True))
            else:
                o.append(sq(x, y, cw, rh, DATA_F, DATA_S, 2))
                o.append(t(x + cw / 2.0, y + rh / 2.0, "%.3f" % v, 14, INK, "middle", mono=True, central=True))
    ly = y0 + 6 * rh + 22
    o.append(sq(150, ly, 22, 18, PANEL, GRID, 2))
    o.append(t(180, ly + 9, "0.68 or more: at the coin", 12, INK, "start", central=True))
    o.append(sq(360, ly, 22, 18, DATA_F, DATA_S, 2))
    o.append(t(390, ly + 9, "below 0.68: better than a coin", 12, INK, "start", central=True))
    o.append(sq(610, ly, 22, 18, BAD_F, BAD_S, 3))
    o.append(cross(621, ly + 9, 4))
    o.append(t(640, ly + 9, "over 1: blew up", 12, INK, "start", central=True))
    o.append(t(400, ly + 44, "epoch 0 is the average over the whole first epoch, not the loss before training", 12, MUT, "middle"))
    fig("fig-w01-5-epoch-table-shaded", "0 0 800 400",
        "Six runs that start at the same coin loss part ways by epoch 10, and only run F begins at 12.786",
        "A table of training loss for runs A to F at epochs 0, 5, 10, 20, 40 and 59. Run A stays at 0.694 to 0.693 all the way. "
        "Run B drifts from 0.694 to 0.683. Run C falls from 0.694 to 0.077. Run D falls from 0.691 to 0.018 and run E from 0.658 to 0.013. "
        "Run F starts at 12.786, marked with a cross, then drops to 0.520 and 0.612 and returns to 0.694, 0.695 and 0.693. "
        "Cells at or above 0.68 are plain, cells below it are tinted blue.", o)


# ---------------------------------------------------------------- W1-6  blank: draw the six bars
def w01_6():
    o = [ctitle("Blank: draw the six final accuracies")]
    o.append(t(36, 78, "dashed line 1 at", 14, INK, "start"))
    o.append(line(160, 82, 230, 82, INK, 2))
    o.append(t(236, 78, "%", 14, INK, "start"))
    o.append(t(290, 78, "dashed line 2 at", 14, INK, "start"))
    o.append(line(414, 82, 484, 82, INK, 2))
    o.append(t(490, 78, "%", 14, INK, "start"))
    x0, x1 = 150, 740
    X = lambda p: x0 + p / 100.0 * (x1 - x0)
    yt, rh = 98, 36
    for p in (0, 25, 50, 75, 100):
        o.append(line(X(p), yt, X(p), yt + 6 * rh, GRID, 1.5, "4 4" if p else None))
        o.append(t(X(p), yt + 6 * rh + 18, str(p), 12, MUT, "middle"))
    for i, (L, lr) in enumerate(zip("ABCDEF", ("1e-06", "1e-05", "0.0001", "0.001", "0.01", "0.1"))):
        y = yt + i * rh
        o.append(rect(x0, y + 5, x1 - x0, rh - 10, 4, PAPER, GRID, 1.5, "6 4"))
        o.append(t(x0 - 12, y + rh / 2.0, "%s  lr=%s" % (L, lr), 12, INK, "end", mono=True, central=True))
    o.append(line(x0, yt - 4, x0, yt + 6 * rh + 4, INK, 2))
    o.append(t((x0 + x1) / 2.0, yt + 6 * rh + 40, "final validation accuracy (%)", 12, MUT, "middle"))
    fig("fig-w01-6-blank-six-bars", "0 0 800 400",
        "A blank chart: draw one bar per run for its final validation accuracy and mark the two constant guessers",
        "An empty chart with six dashed bar tracks labelled A to F with their learning rates, and a horizontal axis from 0 to 100 percent "
        "with grid lines at 0, 25, 50, 75 and 100. Two blanks above the chart are for the accuracies of the two constant guessers. No bar is drawn.", o)


# ---------------------------------------------------------------- W2-4  steady pushes add, flip-flops cancel
def w02_4():
    def vlist(gs):
        v, out = 0.0, []
        for g in gs:
            v = 0.9 * v + g
            out.append(v)
        return out
    steady, flip = [2, 2, 2, 2], [2, -2, 2, -2]
    vs, vf = vlist(steady), vlist(flip)
    # student guide section 4 prints these one-decimal lists
    assert ["%.1f" % v for v in vs] == ["2.0", "3.8", "5.4", "6.9"]
    assert ["%.1f" % v for v in vf] == ["2.0", "-0.2", "1.8", "-0.4"]
    o = [ctitle("A running total: pushes add or cancel")]
    o.append(t(400, 70, "each step:   v = 0.9 x v + g", 14, INK, "middle", mono=True))
    base, sc = 268, 14.4
    for k, (px, name, gs, vv) in enumerate(((20, "pushes that keep one direction", steady, vs),
                                            (410, "pushes that flip every step", flip, vf))):
        o.append(rect(px, 84, 370, 262, 12, PANEL, GRID, 2))
        o.append(t(px + 185, 106, name, 14, INK, "middle"))
        o.append(t(px + 14, 136, "g", 14, MUT, "start", mono=True, central=True))
        o.append(line(px + 30, base, px + 360, base, INK, 2))
        for i in range(4):
            cx = px + 80 + i * 80
            g = gs[i]
            o.append(chip(cx - 24, 124, 48, "%+d" % g, ACC_S if g > 0 else MODEL_S, PAPER, 12, 24))
            v = vv[i]
            h = abs(v) * sc
            top = base - h if v >= 0 else base
            o.append(rect(cx - 18, top, 36, max(h, 2), 0, DATA_F, DATA_S, 2, None if v >= 0 else "4 3"))
            ly = top - 6 if v >= 0 else base + h + 16
            o.append(t(cx, ly, ("%.1f" % v).replace("-", "&#8722;"), 14, INK, "middle", mono=True))
            o.append(t(cx, 330, "step %d" % (i + 1), 12, MUT, "middle"))
    o.append(cap("The same rule: v grows on the left and hovers near zero on the right.", 374))
    fig("fig-w02-4-steady-adds-flipping-cancels", "0 0 800 400",
        "The velocity is a running total of gradients, so pushes in one direction add up and alternating pushes cancel",
        "Two panels of four bars each, drawn up from a baseline, with the gradient g of each step in a chip above it. "
        "Left, g is plus 2 four times and the velocity bars grow 2.0, 3.8, 5.4, 6.9. "
        "Right, g alternates plus 2, minus 2, plus 2, minus 2 and the velocity bars read 2.0, minus 0.2, 1.8, minus 0.4, the negative ones drawn dashed and hanging below the baseline.", o)


# ---------------------------------------------------------------- W2-5  helps or hurts, final loss
HALO = 'stroke="#FFFFFF" stroke-width="3" paint-order="stroke"'


def w02_5():
    LR = ["0.01", "0.03", "0.1", "0.3", "1"]
    SGD = [0.692, 0.690, 0.387, 0.016, 0.528]            # student guide Step 6 verdict table
    MOM = [0.440, 0.018, 0.025, 0.659, None]             # None = nan
    verdict = []
    for s, m in zip(SGD, MOM):
        verdict.append("hurts" if m is None else ("helps" if m < s - 0.05 else ("hurts" if not m <= s + 0.05 else "equal")))
    assert verdict == ["helps", "helps", "helps", "hurts", "hurts"]
    o = [ctitle("Same learning rate, two rules: final training loss")]
    x0, base, sc = 70, 262, 190.0
    o.append(chip(190, 62, 150, "plain SGD", DATA_S, DATA_F, 12, 24, False))
    o.append(chip(460, 62, 150, "momentum", MODEL_S, MODEL_F, 12, 24, False))
    o.append(line(x0, base, 770, base, INK, 2))
    for v in (0.0, 0.2, 0.4, 0.6, 0.8):
        o.append(line(x0 - 5, base - v * sc, x0, base - v * sc, MUT, 1.5))
        o.append(t(x0 - 9, base - v * sc + 4, "%.1f" % v, 12, MUT, "end"))
    o.append(line(x0, base - 0.693 * sc, 770, base - 0.693 * sc, GRID, 1.5, "6 4"))
    o.append(t(770, base - 0.693 * sc - 6, "0.693: a coin", 12, MUT, "end"))
    gw = 136
    for i in range(5):
        gx = x0 + 14 + i * gw
        for k, (val, st, fl, dash) in enumerate(((SGD[i], DATA_S, DATA_F, None), (MOM[i], MODEL_S, MODEL_F, "5 3"))):
            bx = gx + 6 + k * 52
            if val is None:
                o.append(t(bx + 22, base - 10, "nan", 14, BAD_S, "middle", mono=True, weight="700"))
                o.append(cross(bx + 22, base - 36, 8))
                continue
            h = max(val * sc, 2)
            o.append(rect(bx, base - h, 44, h, 0, fl, st, 2, dash))
            o.append(t(bx + 22, base - h - 6, "%.3f" % val, 12, INK, "middle", mono=True, extra=HALO))
        o.append(t(gx + 54, base + 20, "lr " + LR[i], 12, INK, "middle", mono=True))
        if verdict[i] == "helps":
            o.append(tick(gx + 30, base + 46, 8))
            o.append(t(gx + 44, base + 51, "helps", 14, OK_S, "start"))
        else:
            o.append(cross(gx + 28, base + 45, 6))
            o.append(t(gx + 42, base + 51, "hurts", 14, BAD_S, "start"))
    o.append(cap("helps = at least 0.05 lower than plain SGD. One seed: a pattern, not a ranking.", 372))
    fig("fig-w02-5-helps-or-hurts-bars", "0 0 800 400",
        "Momentum helps at learning rates 0.01, 0.03 and 0.1 and hurts at 0.3 and 1, where a step up to ten times longer overshoots",
        "Five pairs of bars of final training loss, plain SGD solid and momentum dashed, against a dashed line at 0.693. "
        "At lr 0.01 the bars are 0.692 and 0.440, at 0.03 they are 0.690 and 0.018, at 0.1 they are 0.387 and 0.025, "
        "at 0.3 they are 0.016 and 0.659, and at lr 1 plain SGD is 0.528 and momentum has no bar, only the word nan. "
        "Under each pair a tick and the word helps, or a cross and the word hurts.", o)


# ---------------------------------------------------------------- W2-6  blank: plot the path
def w02_6():
    o = [ctitle("Blank: plot where w lands, step by step")]
    x0, x1 = 80, 740
    X = lambda w: x0 + (w + 1.0) / 3.0 * (x1 - x0)         # w from -1 to 2
    for k, (name, y) in enumerate((("plain SGD", 150), ("momentum", 270))):
        o.append(t(x0, y - 48, name, 14, INK, "start"))
        o.append(line(x0, y, x1, y, INK, 2))
        for w in range(-4, 9):
            wv = w / 4.0
            tall = (w % 4 == 0)
            o.append(line(X(wv), y - (7 if tall else 4), X(wv), y + (7 if tall else 4), MUT, 1.5))
            if tall:
                o.append(t(X(wv), y + 26, "%d" % wv if wv >= 0 else "&#8722;1", 12, MUT, "middle"))
        o.append(line(X(0), y - 34, X(0), y + 34, ACC_S, 2, "6 4"))
        o.append(t(X(0), y - 40, "target 0", 12, ACC_S, "middle"))
        o.append(circ(X(2.0), y, 9, PAPER, INK, 3))
        o.append(t(X(2.0), y - 18, "start", 12, INK, "middle"))
    o.append(cap("Mark w after steps 1, 2, 3 and 4 on each line, with the step number inside each dot.", 372))
    fig("fig-w02-6-blank-number-lines", "0 0 800 400",
        "A blank pair of number lines: plot where w lands after each of four steps for plain SGD and for momentum, starting at 2",
        "Two horizontal number lines from minus 1 to 2 with small tick marks every quarter, a dashed target line at 0, "
        "and a single open dot labelled start at 2. The upper line is labelled plain SGD and the lower line momentum. No step is plotted.", o)


# ---------------------------------------------------------------- W3-4  what Adam does to one gradient
def w03_4():
    o = [ctitle("Adam: divide by the typical size")]
    o.append(t(130, 86, "two running averages, one knob", 12, MUT, "start"))
    top, bot = 96, 222
    o.append(box(20, 166, 84, 68, "g = 2.0", "this step", DATA_F, DATA_S, 3))
    o.append(box(132, top, 150, 64, "m = 0.2", "average of g", DATA_F, DATA_S))
    o.append(box(132, bot, 150, 64, "s = 0.004", "average of g x g", DATA_F, DATA_S, 2, "5 3"))
    o.append(box(330, top, 146, 64, "m / 0.1 = 2.0", "divide by arrived", DATA_F, DATA_S))
    o.append(box(330, bot, 146, 64, "s / 0.001 = 4.0", "divide by arrived", DATA_F, DATA_S, 2, "5 3"))
    o.append(box(508, bot, 100, 64, "root = 2.0", "of 4.0", DATA_F, DATA_S, 2, "5 3"))
    o.append(box(630, 146, 150, 108, "step = 0.1", "0.1 x 2.0 / 2.0", ACC_F, ACC_S, 4))
    o.append(arrow(104, 190, 130, top + 40, INK, 2.5))
    o.append(arrow(104, 210, 130, bot + 24, INK, 2.5))
    o.append(arrow(282, top + 32, 328, top + 32, INK, 2.5))
    o.append(arrow(282, bot + 32, 328, bot + 32, INK, 2.5))
    o.append(arrow(476, bot + 32, 506, bot + 32, INK, 2.5))
    o.append(arrow(476, top + 32, 628, 180, INK, 2.5))
    o.append(arrow(608, bot + 32, 628, 226, INK, 2.5))
    o.append(t(556, top + 18, "2.0 / 2.0 = 1.0", 12, INK, "middle"))
    o.append(cap("First step: the ratio is exactly 1, so the step is lr = 0.1, whatever g was.", 374))
    fig("fig-w03-4-adam-two-averages-then-divide", "0 0 800 400",
        "Adam divides the averaged gradient by the root of the averaged squared gradient, so the first step is the learning rate",
        "A flow of boxes for one knob on the first step. A gradient g equal to 2.0 feeds two boxes: m equal to 0.2, the average of g, "
        "and s equal to 0.004, the average of g times g, drawn dashed. Each is divided by what has arrived, giving 2.0 and 4.0. "
        "The 4.0 passes through a square root to give 2.0. The two 2.0 values meet in a highlighted box: step equals 0.1 times 2.0 divided by 2.0, which is 0.1.", o)


# ---------------------------------------------------------------- W3-5  weight decay, share kept
def w03_5():
    KEEP = 1 - 0.1 * 0.1
    assert abs(KEEP - 0.99) < 1e-12 and "%.4f" % (KEEP ** 10) == "0.9044"      # hand sum
    ROWS = [("SGD", "decay 0.1", (1.0, 0.9044), (100.0, 90.4382)),
            ("Adam", "decay 0.1", (1.0, 0.0762), (100.0, 99.0003)),
            ("AdamW", "decay 0.1", (1.0, 0.9044), (100.0, 90.4382))]            # student guide Step 6
    o = [ctitle("Weight decay: how much of each weight is left")]
    o.append(t(400, 72, "SGD keeps 1 - 0.1 x 0.1 = 0.99 per step; 0.99 ten times is 0.9044", 14, MUT, "middle"))
    x0, x1 = 190, 590
    X = lambda f: x0 + f * (x1 - x0)
    top = 104
    for f in (0, 0.5, 1.0):
        o.append(line(X(f), top, X(f), top + 230, GRID, 1.5, "4 4" if f else None))
        o.append(t(X(f), top + 248, "%d%%" % round(f * 100), 12, MUT, "middle"))
    o.append(t(X(1.0), top - 6, "start", 12, MUT, "middle"))
    for i, (rule, sub, small, big) in enumerate(ROWS):
        y = top + i * 78
        o.append(t(24, y + 31, rule, 14, INK, "start", weight="700"))
        for k, (w0, w1) in enumerate((small, big)):
            by = y + 6 + k * 32
            f = w1 / w0
            ruined = f < 0.5
            o.append(t(x0 - 8, by + 12, "weight %g" % w0, 12, INK, "end", central=True))
            o.append(rect(x0, by, f * (x1 - x0), 24, 0, BAD_F if ruined else DATA_F, BAD_S if ruined else DATA_S, 2, "5 3" if ruined else None))
            lab = "%g to %s" % (w0, ("%.4f" % w1).rstrip("0") if w1 < 1 else "%.4f" % w1)
            tx = x0 + f * (x1 - x0) + 8
            o.append(t(tx, by + 12, lab, 12, INK, "start", mono=True, central=True))
            if ruined:
                o.append(cross(tx + 112, by + 12, 6))
    o.append(cap("Adam's divide turns decay into a fixed amount per step; AdamW applies it outside the divide.", 374))
    fig("fig-w03-5-decay-share-kept", "0 0 800 400",
        "With weight decay and no loss, SGD and AdamW shrink both weights by the same share, but Adam nearly wipes out the small weight",
        "Three pairs of horizontal bars showing how much of each of two weights, 1.0 and 100, is left after ten steps with decay 0.1. "
        "SGD leaves 0.9044 of the small weight and 90.4382 of the big one. Adam leaves 0.0762 of the small weight, drawn short, dashed and marked with a cross, "
        "and 99.0003 of the big one. AdamW leaves 0.9044 and 90.4382, the same as SGD. A line of text gives the hand sum 0.99 ten times is 0.9044.", o)


# ---------------------------------------------------------------- W3-6  blank: plot the epsilon curve
def w03_6():
    o = [ctitle("Blank: Adam's first step against gradient size")]
    x0, x1, yb, yt = 90, 740, 296, 92
    X = lambda e: x0 + (e + 9) / 12.0 * (x1 - x0)           # exponent -9..3
    Y = lambda v: yb - v / 0.1 * (yb - yt)
    for v, lab in ((0, "0"), (0.025, "0.025"), (0.05, "0.05"), (0.075, "0.075"), (0.1, "0.1")):
        o.append(line(x0, Y(v), x1, Y(v), GRID, 1.5, "4 4" if v else None))
        o.append(t(x0 - 8, Y(v) + 4, lab, 12, MUT, "end"))
    for e in range(-9, 4):
        o.append(line(X(e), yb, X(e), yb + 5, MUT, 1.5))
        o.append(t(X(e), yb + 20, "1e%d" % e if e < 0 else ("1e%d" % e if e else "1"), 12, MUT, "middle"))
    for e in (3, 0, -3, -6, -8, -9):                           # the six gradients on the page
        o.append(line(X(e), yt, X(e), yb, GRID, 1.5, "2 5"))
    o.append(line(x0, yb, x1, yb, INK, 2))
    o.append(line(x0, yt, x0, yb, INK, 2))
    o.append(line(x0, Y(0.1), x1, Y(0.1), ACC_S, 2, "6 4"))
    o.append(t(x1, Y(0.1) - 6, "lr = 0.1", 12, ACC_S, "end"))
    o.append(t((x0 + x1) / 2.0, yb + 44, "gradient size (each tick is ten times bigger)", 12, MUT, "middle"))
    o.append(trot(40, (yb + yt) / 2.0, "first step", 12))
    o.append(cap("Dotted guides mark the six gradients: plot one point on each, then join them.", 374))
    fig("fig-w03-6-blank-epsilon-axes", "0 0 800 400",
        "A blank chart: plot Adam's first step against the size of the gradient and see where epsilon starts to cost",
        "Empty axes. The horizontal axis is gradient size from 1e-9 to 1000 with one tick per factor of ten; the vertical axis is the first step from 0 to 0.1 "
        "with a dashed line at lr equal to 0.1. Six dotted vertical guides mark the gradients 1000, 1, 1e-3, 1e-6, 1e-8 and 1e-9. No point is plotted.", o)


def build():
    for f in (w01_4, w01_5, w01_6, w02_4, w02_5, w02_6, w03_4, w03_5, w03_6):
        f()
    return FIGS

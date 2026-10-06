"""Block 1 (Weeks 1-3) concept figures for Level 4. Two per week, fig-w01-1 ... fig-w03-2.

Every number printed here is copied from an executed, seeded block in that week's student guide
(seed 0 is the harness default); the provenance is noted beside each data table (STYLE.md 2.1).
Deterministic: no randomness at run time.

    emit(figures_dir) -> list of file names written
"""
import math
import os
from _gen_core import *

W = "0 0 800 400"
MINUS, TIMES, DIV, ARROW = "&#8722;", "&#215;", "&#247;", "&#8594;"


def _title(s):
    return t(400, 42, s, 24, INK, "middle")


def _caption(s):
    return t(400, 368, s, 14, MUT, "middle")


# ====================================================================== W01-1
# Week 1, Step 3: train loss at epochs 0, 5, 10, 20, 40, 59 for runs A-F (seed 0).
EPOCHS = (0, 5, 10, 20, 40, 59)
W1 = {
    "A": ("1e-6", (0.694, 0.694, 0.694, 0.694, 0.694, 0.693)),
    "B": ("1e-5", (0.694, 0.694, 0.693, 0.692, 0.689, 0.683)),
    "C": ("1e-4", (0.694, 0.688, 0.655, 0.575, 0.166, 0.077)),
    "D": ("1e-3", (0.691, 0.399, 0.082, 0.021, 0.011, 0.018)),
    "E": ("1e-2", (0.658, 0.052, 0.041, 0.027, 0.021, 0.013)),
    "F": ("1e-1", (12.786, 0.520, 0.612, 0.694, 0.695, 0.693)),
}


def fig_w01_1():
    top, bot = 110, 290
    span = 3.2                       # decades shown: 10**1.2 down to 10**-2

    def yv(v):
        return top + (1.2 - math.log10(v)) / span * (bot - top)

    panels = [
        (20, "A, B: too small, stuck", DATA_S, [("A", "circle", None, 4), ("B", "square", "6 4", 7)]),
        (280, "C, D, E: it learned", OK_S, [("C", "circle", None, 6), ("D", "square", "6 4", 6),
                                           ("E", "triangle", "2 4", 6)]),
        (540, "F: too big, blew up", BAD_S, [("F", "circle", None, 6)]),
    ]
    # label nudges (px) so near-equal end values do not collide
    nudge = {"A": -8, "B": 10, "C": 0, "D": -5, "E": 9, "F": 0}
    o = [_title("Same final loss, three different stories")]
    for px, head_, col, series in panels:
        left = px + 48
        o.append(rect(px, 58, 240, 282, 12, PANEL, GRID, 1.5))
        o.append(t(px + 120, 86, head_, 18, INK, "middle"))
        for tv in (10, 1, 0.1, 0.01):
            y = yv(tv)
            o.append(line(left, y, left + 118, y, GRID, 1.5))
            o.append(t(px + 42, y + 4, ("%g" % tv), 12, MUT, "end"))
        o.append(line(left, top, left, bot, INK, 2))
        o.append(line(left, bot, left + 118, bot, INK, 2))
        yc = yv(0.693)
        o.append(line(left, yc, left + 118, yc, MUT, 1.5, "6 4"))
        o.append(trot(px + 12, 200, "train loss (log scale)"))
        o.append(t(left, 306, "0", 12, MUT, "middle"))
        o.append(t(left + 118, 306, "59", 12, MUT, "middle"))
        o.append(t(left + 59, 324, "epoch", 12, MUT, "middle"))
        for letter, kind, dash, r in series:
            lr_, vals = W1[letter]
            pts = [(left + 2 * e, yv(v)) for e, v in zip(EPOCHS, vals)]
            o.append(poly(pts, "none", col, 3, dash))
            for (x, y) in pts[:-1]:
                o.append(circ(x, y, 3, PAPER, col, 2))
            ex, ey = pts[-1]
            o.append(mark(kind, ex, ey, r, col, PAPER, 2))
            o.append(t(left + 126, ey + 4 + nudge[letter], "%s %.3f" % (letter, vals[-1]), 12, INK, "start"))
        if series[0][0] == "F":
            o.append(t(left + 14, 118, "start 12.786", 12, INK, "start"))
        if series[0][0] == "C":
            o.append(chip(left + 30, 146, 96, "coin 0.693", ACC_S, ACC_F, 12, 24, mono=False))
    o.append(_caption("Dashed line: a coin-flip model scores ln 2 = 0.693. Seed 0; epochs 0, 5, 10, 20, 40, 59."))
    desc = ("Three small panels share one log-scale loss axis from 0.01 to 10, with a dashed line at 0.693, the loss of a coin-flip model. "
            "Left, runs A and B (learning rates 1e-6 and 1e-5) sit on the line: A goes 0.694 to 0.693 and B goes 0.694 to 0.683. "
            "Middle, runs C, D and E fall well below it: C goes 0.694 to 0.077, D goes 0.691 to 0.018 and E goes 0.658 to 0.013. "
            "Right, run F starts at 12.786, drops to 0.520 and ends back on the line at 0.693. Points are epochs 0, 5, 10, 20, 40 and 59 of seed 0.")
    title = "Three runs that end near 0.693 tell three different stories; only the curve shows which"
    return svg_doc(W, title, desc, J(*o))


# ====================================================================== W01-2
# Week 1, Step 5: final validation accuracy of runs A-F; the two constant guessers are hand sums 191/360, 169/360.
ACC = [("A", "1e-6", 53.1), ("B", "1e-5", 55.3), ("C", "1e-4", 98.1),
       ("D", "1e-3", 99.4), ("E", "1e-2", 99.2), ("F", "1e-1", 46.9)]


def fig_w01_2():
    x0, per = 190, 5.4               # bar origin and px per percentage point
    o = [_title("Two runs sit exactly on a constant guesser")]
    ys = [96 + 34 * i for i in range(6)]
    o.append(t(20, 80, "run", 12, MUT, "start"))
    o.append(t(776, 80, "val accuracy", 12, MUT, "end"))
    for gx in (0, 50, 100):
        x = x0 + gx * per
        o.append(line(x, 88, x, 300, GRID, 1.5))
        o.append(t(x, 318, "%d%%" % gx, 12, MUT, "middle"))
    for (letter, lr_, a), y in zip(ACC, ys):
        stuck = letter in ("A", "F")
        won = letter in ("C", "D", "E")
        fill, stroke = (BAD_F, BAD_S) if stuck else ((OK_F, OK_S) if won else (DATA_F, DATA_S))
        o.append(t(20, y + 12 + 5, "%s  lr=%s" % (letter, lr_), 18, INK, "start"))
        o.append(rect(x0, y, a * per, 24, 4, fill, stroke, 3))
        o.append(t(776, y + 17, "%.1f%%" % a, 14, INK, "end"))
        if stuck:
            o.append(cross(168, y + 12, 7))
        elif won:
            o.append(tick(168, y + 12, 9))
    xl, xr = x0 + 46.9 * per, x0 + 53.1 * per
    o.append(line(xl, 88, xl, 300, INK, 2, "6 4"))
    o.append(line(xr, 88, xr, 300, INK, 2, "6 4"))
    o.append(t(xl - 6, 72, "always class 0: 169 / 360", 12, INK, "end"))
    o.append(t(xr + 6, 72, "always class 1: 191 / 360", 12, INK, "start"))
    o.append(t(x0 + 50 * per, 338, "validation accuracy, 360 points", 12, MUT, "middle"))
    o.append(_caption("A and F end exactly on a constant guesser: a model must beat both lines to have learned."))
    desc = ("Horizontal bars of final validation accuracy for Week 1's six runs, with two dashed vertical lines for models that ignore their input. "
            "Always saying class 0 scores 169 / 360 = 46.9 percent; always saying class 1 scores 191 / 360 = 53.1 percent. "
            "Run A ends at 53.1 percent and run F at 46.9 percent, exactly on the lines, marked with crosses. Run B reaches 55.3 percent, just above. "
            "Runs C, D and E reach 98.1, 99.4 and 99.2 percent, marked with ticks.")
    title = "A model that ends on a constant guesser's accuracy has learned nothing"
    return svg_doc(W, title, desc, J(*o))


# ====================================================================== W02-1
EMA = [1.0000, 0.9000, 0.8100, 0.7290, 0.6561]                       # Week 2 section 2
SHARE = [0.900, 0.810, 0.729, 0.656, 0.590, 0.531, 0.478, 0.430]     # Week 2 section 3


def fig_w02_1():
    base, hmax = 290, 160
    o = [_title("Each new value fades by a fixed share")]
    o.append(rect(20, 56, 370, 284, 12, PANEL, GRID, 1.5))
    o.append(rect(410, 56, 370, 284, 12, PANEL, GRID, 1.5))
    o.append(t(205, 84, "The average after 10, 0, 0, 0, 0", 18, INK, "middle"))
    o.append(t(595, 84, "How much the first 10 still counts", 18, INK, "middle"))
    # left panel
    o.append(line(40, base, 372, base, INK, 2))
    for i, v in enumerate(EMA):
        cx = 68 + 66 * i
        h = v * hmax
        o.append(rect(cx - 18, base - h, 36, h, 0, DATA_F, DATA_S, 3 if i == 0 else 2))
        o.append(t(cx, base - h - 6, "%.4f" % v, 12, INK, "middle"))
        o.append(t(cx, 308, "step %d" % (i + 1), 12, MUT, "middle"))
        o.append(t(cx, 326, "gets %d" % (10 if i == 0 else 0), 12, MUT, "middle"))
    # right panel
    o.append(line(430, base, 764, base, INK, 2))
    for i, v in enumerate(SHARE):
        cx = 446 + 42 * i
        h = v * hmax
        hot = (i == 6)
        o.append(rect(cx - 14, base - h, 28, h, 0, ACC_F if hot else DATA_F, ACC_S if hot else DATA_S, 3 if hot else 2))
        o.append(t(cx, base - h - 6, "%.3f" % v, 12, INK, "middle"))
        o.append(t(cx, 308, str(i + 1), 12, MUT, "middle"))
    o.append(t(595, 326, "steps since the 10 arrived", 12, MUT, "middle"))
    yh = base - 0.5 * hmax
    o.append(line(430, yh, 764, yh, INK, 1.5, "6 4"))
    o.append(t(764, yh + 16, "half = 0.5", 12, MUT, "end"))
    o.append(chip(575, 104, 180, "half-life: 6.58 steps", ACC_S, ACC_F, 12, 26, mono=False))
    o.append(_caption("Each step multiplies by 0.9, so the first value counts for half after 6.58 steps."))
    desc = ("Two bar charts. Left: the running average after the values 10, 0, 0, 0, 0 arrive is 1.0000, 0.9000, 0.8100, 0.7290 and 0.6561, "
            "each 0.9 times the one before. Right: the share the first 10 still counts after 1 to 8 steps is 0.900, 0.810, 0.729, 0.656, 0.590, "
            "0.531, 0.478 and 0.430. A dashed line marks one half; the share drops below it at step 7, the exact crossing is 6.58 steps.")
    title = "A running average forgets each old value by the same share every step; for 0.9 the half-life is 6.58 steps"
    return svg_doc(W, title, desc, J(*o))


# ====================================================================== W02-2
SGD_W = [1.0, 0.8, 0.64, 0.512, 0.4096]            # Week 2 Step 1, plain SGD, lr 0.1
MOM_W = [1.0, 0.8, 0.46, 0.062, -0.3086]           # Week 2 Step 1, momentum, lr 0.1


def fig_w02_2():
    def xw(w):
        return 330 + 380 * w

    o = [_title("Momentum arrives sooner, then overshoots")]
    o.append(rect(20, 92, 760, 112, 12, PANEL, GRID, 1.5))
    o.append(rect(20, 214, 760, 112, 12, PANEL, GRID, 1.5))
    o.append(t(36, 112, "plain SGD", 18, INK, "start"))
    o.append(t(36, 234, "momentum", 18, INK, "start"))
    o.append(t(780, 76, "number in a circle = step", 12, MUT, "end"))
    o.append(t(330, 76, "target w = 0", 14, MUT, "middle"))
    for ys, ws, bad_last in ((148, SGD_W, False), (270, MOM_W, True)):
        o.append(poly([(xw(w), ys) for w in ws], "none", INK, 2))
        for i, w in enumerate(ws):
            x = xw(w)
            hot = bad_last and i == 4
            fill, stroke = (BAD_F, BAD_S) if hot else ((PAPER, INK) if i == 0 else (DATA_F, DATA_S))
            o.append(circ(x, ys, 13, fill, stroke, 3))
            o.append(t(x, ys, str(i), 12, INK, "middle", central=True))
            o.append(t(x, ys + (48 if (not bad_last and i == 4) else 32), ("%.4f" % w).replace("-", MINUS), 12, INK, "middle"))
    o.append(line(330, 86, 330, 322, INK, 2, "6 4"))
    o.append(t(468, 128, "creeps toward 0,", 14, MUT, "end"))
    o.append(t(468, 146, "never passes it", 14, MUT, "end"))
    o.append(t(213, 238, "overshoot: past 0", 14, BAD_S, "middle"))
    o.append(_caption("Momentum is at 0.0620 after step 3 (SGD 0.5120), then goes past zero to %s0.3086." % MINUS))
    desc = ("Two rows of numbered circles on the number line for w, with a dashed line at the target w = 0. Plain SGD on f(w) = w times w from w = 1.0, "
            "learning rate 0.1: w is 1.0000, 0.8000, 0.6400, 0.5120 and 0.4096 after steps 0 to 4, creeping toward zero and never passing it. "
            "Momentum: w is 1.0000, 0.8000, 0.4600, 0.0620 and minus 0.3086, so at step 4 it has gone past zero, marked as an overshoot.")
    title = "Momentum reaches the target in fewer steps because it carries old steps, and that is also why it overshoots"
    return svg_doc(W, title, desc, J(*o))


# ====================================================================== W03-1
RMS_ROWS = [("3 and %s4" % MINUS, "3.5355"), ("300 and %s400" % MINUS, "353.5534"),
            ("3000 and %s4000" % MINUS, "3535.5339")]
RMS_OUT = "0.8485 and %s1.1314" % MINUS          # identical in all three rows (Week 3 section 2)


def fig_w03_1():
    o = [_title("Divide by the typical size and the scale disappears")]
    o.append(t(155, 92, "knob gradients", 18, INK, "middle"))
    o.append(t(400, 92, "typical size (RMS)", 18, INK, "middle"))
    o.append(t(650, 92, "gradient %s typical size" % DIV, 18, INK, "middle"))
    for i, (lst, rms) in enumerate(RMS_ROWS):
        y = 138 + 80 * i               # row centre
        o.append(arrow(270, y, 308, y, INK, 2))
        o.append(arrow(492, y, 528, y, INK, 2))
        o.append(rect(40, y - 28, 230, 56, 10, DATA_F, DATA_S, 3))
        o.append(t(54, y + 6, lst, 18, INK, "start"))
        o.append(shape_chip(218, y - 13, "(2,)", DATA_S))
        o.append(rect(310, y - 28, 180, 56, 10, PANEL, DATA_S, 2))
        o.append(t(400, y + 6, rms, 18, INK, "middle"))
        o.append(rect(530, y - 28, 240, 56, 10, ACC_F, ACC_S, 3))
        o.append(t(544, y + 6, RMS_OUT, 18, INK, "start"))
        o.append(shape_chip(718, y - 13, "(2,)", ACC_S))
    o.append(_caption("Dividing out the typical size leaves the same two numbers at every scale."))
    desc = ("Three rows, each a list of two knob gradients, its root-mean-square, and the list divided by that size. The list 3 and minus 4 has typical size 3.5355; "
            "300 and minus 400 has 353.5534; 3000 and minus 4000 has 3535.5339. In every row the list divided by its typical size is the same: "
            "0.8485 and minus 1.1314. Each list is a tensor of shape (2,).")
    title = "Dividing each gradient by its own typical size cancels the scale, so a thousand-times-bigger knob looks the same"
    return svg_doc(W, title, desc, J(*o))


# ====================================================================== W03-2
# Week 3 Step 4: gradients [1.0, 1000.0], lr 0.1, first step moved SGD [0.1, 100.0], Adam [0.1, 0.1].
STEP1 = [("SGD", 0.1, 100.0), ("Adam", 0.1, 0.1)]


def fig_w03_2():
    x0, dec = 260, 100.0

    def xv(v):
        return x0 + (math.log10(v) + 2) * dec

    o = [_title("Adam: a thousand-times-bigger gradient, the same step")]
    rows = [(84, "SGD: the 1000 gradient moves 1000 times further", [(122, "knob 1  (gradient 1)", 0.1, False),
                                                                    (160, "knob 2  (gradient 1000)", 100.0, True)]),
            (214, "Adam: both knobs move the same distance", [(252, "knob 1  (gradient 1)", 0.1, False),
                                                              (290, "knob 2  (gradient 1000)", 0.1, False)])]
    for tv in (0.01, 0.1, 1, 10, 100):
        x = xv(tv)
        o.append(line(x, 100, x, 306, GRID, 1.5))
        o.append(t(x, 324, "%g" % tv, 12, MUT, "middle"))
    o.append(t(xv(1), 342, "distance moved on the first step (log scale)", 12, MUT, "middle"))
    for hy, htxt, rs in rows:
        o.append(t(20, hy, htxt, 18, INK, "start"))
        for y, lab, v, bad in rs:
            adam = hy > 200
            fill, stroke = (BAD_F, BAD_S) if bad else ((OK_F, OK_S) if adam else (DATA_F, DATA_S))
            o.append(t(20, y + 5, lab, 14, INK, "start"))
            o.append(rect(x0, y - 11, xv(v) - x0, 22, 4, fill, stroke, 3))
            o.append(t(xv(v) + 8, y + 5, "%.1f" % v if v >= 1 else "%g" % v, 14, INK, "start"))
            if bad:
                o.append(cross(760, y, 8))
            else:
                o.append(tick(760, y, 9))
    o.append(_caption("Learning rate 0.1; gradients 1.0 and 1000.0 as a (2,) tensor; first step only."))
    desc = ("Horizontal bars on a log axis of how far each of two knobs moved on the first step, with learning rate 0.1 and gradients 1.0 and 1000.0. "
            "Plain SGD moved knob 1 by 0.1 and knob 2 by 100.0, a thousand times further, marked with a cross. "
            "Adam moved both knobs by 0.1, marked with ticks.")
    title = "Adam divides each knob's step by that knob's own gradient size, so both move the same distance"
    return svg_doc(W, title, desc, J(*o))


FIGS = {
    "fig-w01-1-three-stories-one-number.svg": fig_w01_1,
    "fig-w01-2-constant-guesser-baseline.svg": fig_w01_2,
    "fig-w02-1-fading-share-half-life.svg": fig_w02_1,
    "fig-w02-2-momentum-arrives-then-overshoots.svg": fig_w02_2,
    "fig-w03-1-divide-by-typical-size.svg": fig_w03_1,
    "fig-w03-2-scale-test-sgd-vs-adam.svg": fig_w03_2,
}


def emit(figures_dir):
    names = []
    for name, fn in FIGS.items():
        with open(os.path.join(figures_dir, name), "w") as f:
            f.write(fn() + "\n")
        names.append(name)
    return names

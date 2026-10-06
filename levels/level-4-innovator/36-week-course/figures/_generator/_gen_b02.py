"""Block 2 (weeks 4, 5, 6) concept figures. Every number is copied from the week's printed output
or is a hand sum printed beside it (STYLE.md 2.1).

W4  schedules.py table (peak 0.003, T 1000, warm 50) ; the curves are that same rule evaluated here
    batches.py Experiment A (same 60 epochs) and B (same 780 steps), mean of seeds 0-4
W5  Start Here run, seed 0, 120 training points ; table.py five seeds (0-4) mean and lowest..highest
W6  slope.py: 0.3 x 0.2 x 0.4 x 0.1 = 0.0024 and 1.3 x 1.2 x 1.4 x 1.1 = 2.4024 (running products are hand sums)
    probe.py (seed 0) and depth_train.py (mean of seeds 0-2, 30 epochs), plain and residual columns
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


# ---------------------------------------------------------------- W4-1  warmup then cosine
def w04_1():
    PEAK, T, W = 0.003, 1000, 50

    def cos_m(s):
        return 0.5 * (1 + math.cos(math.pi * s / T))

    def warm_m(s):
        if s < W:
            return (s + 1) / W
        return 0.5 * (1 + math.cos(math.pi * min(1.0, (s - W) / (T - W))))

    rows = [0, 10, 49, 250, 500, 750, 1000]
    printed_c = ["0.00300", "0.00300", "0.00298", "0.00256", "0.00150", "0.00044", "0.00000"]
    printed_w = ["0.00006", "0.00066", "0.00300", "0.00268", "0.00162", "0.00048", "0.00000"]
    for s, pc, pw in zip(rows, printed_c, printed_w):          # the table is the run's own printout
        assert "%.5f" % (PEAK * cos_m(s)) == pc and "%.5f" % (PEAK * warm_m(s)) == pw, s
    x0, x1, yb, yt = 100, 520, 310, 100
    X = lambda s: x0 + s / 1000.0 * (x1 - x0)
    Y = lambda v: yb - v / PEAK * (yb - yt)
    o = [ctitle("A learning rate is a rule over time")]
    o.append(line(x0, Y(PEAK), x1, Y(PEAK), GRID, 1.5, "6 4"))
    o.append(t(x0, 92, "peak 0.003", 12, MUT, "start"))
    for v, lab in ((0, "0"), (0.001, "0.001"), (0.002, "0.002")):
        o.append(line(x0 - 5, Y(v), x0, Y(v), MUT, 1.5))
        o.append(t(x0 - 9, Y(v) + 4, lab, 12, MUT, "end"))
    o.append(line(x0, yb, x1, yb, INK, 2))
    o.append(line(x0, yt, x0, yb, INK, 2))
    for s in (0, 250, 500, 750, 1000):
        o.append(line(X(s), yb, X(s), yb + 5, MUT, 1.5))
        o.append(t(X(s), yb + 20, str(s), 12, MUT, "middle"))
    o.append(t((x0 + x1) / 2.0, 346, "step (T = 1000)", 12, MUT, "middle"))
    o.append(trot(40, (yb + yt) / 2.0, "learning rate", 12))
    cos_pts = [(X(s), Y(PEAK * cos_m(s))) for s in range(0, 1001, 5)]
    warm_pts = [(X(s), Y(PEAK * warm_m(s))) for s in range(0, 1001, 5)]
    o.append(poly(cos_pts, "none", DATA_S, 3, "6 4"))
    o.append(poly(warm_pts, "none", MODEL_S, 3))
    for s in (0, 49, 250, 750, 1000):
        o.append(mark("circle", X(s), Y(PEAK * warm_m(s)), 5, MODEL_S, PAPER, 2))
    o.append(mark("circle", X(500), Y(PEAK * warm_m(500)), 5, MODEL_S, PAPER, 2))
    o.append(mark("square", X(500), Y(PEAK * cos_m(500)), 5, DATA_S, PAPER, 2))
    o.append(ring_num(X(500) - 18, Y(PEAK * cos_m(500)) + 20, 1))
    o.append(t(250, 92, "cosine only, dashed", 12, DATA_S, "start"))
    o.append(t(300, 298, "warm+cosine, solid", 12, MODEL_S, "start"))
    o.append(bracket(X(0), X(50), yb - 8, 7, MUT, True))
    o.append(t(X(50) + 8, yb - 14, "ramp, 50 steps", 12, MUT, "start"))
    # the table printed by schedules.py
    o.append(rect(548, 96, 232, 230, 12, PANEL, GRID, 2))
    o.append(t(576, 118, "step", 12, MUT, "start"))
    o.append(t(672, 118, "cosine", 12, DATA_S, "end"))
    o.append(t(768, 118, "warm+cosine", 12, MODEL_S, "end"))
    for i, (s, pc, pw) in enumerate(zip(rows, printed_c, printed_w)):
        y = 144 + i * 26
        if s == 500:
            o.append(rect(556, y - 14, 216, 24, 6, ACC_F, ACC_S, 3))
            o.append(ring_num(572, y - 2, 1))
        o.append(t(588 if s == 500 else 576, y + 2, str(s), 12, INK, "start"))
        o.append(t(672, y + 2, pc, 12, INK, "end"))
        o.append(t(768, y + 2, pw, 12, INK, "end"))
    o.append(cap("Step 500 is halfway: 0.003 &#215; 0.5 = 0.0015. Warm-up starts at 0.00006, not at the peak."))
    fig("fig-w04-1-warmup-then-cosine-rate.svg", "0 0 800 400",
        "The rate is the peak times a multiplier that depends on the step",
        "Line chart of learning rate against step, peak 0.003, 1000 steps. Dashed cosine-only starts at 0.00300 and "
        "falls to 0.00150 at step 500 (ringed 1) and 0.00000 at step 1000. Solid warm+cosine climbs from 0.00006 at "
        "step 0 to 0.00300 at step 49 over a 50-step ramp, then falls to 0.00162 at step 500 and 0.00000 at step "
        "1000. A table beside it lists the printed rates at steps 0, 10, 49, 250, 500, 750 and 1000.", o)


# ---------------------------------------------------------------- W4-2  what did I hold fixed
def w04_2():
    o = [ctitle("Batch size quietly changes the number of steps")]
    # panel A: same 60 epochs, steps on a log axis
    o.append(rect(20, 62, 372, 290, 12, PANEL, GRID, 2))
    o.append(t(34, 86, "A  same 60 epochs", 18, INK, "start"))
    o.append(t(34, 106, "bars: steps taken (log scale)", 12, MUT, "start"))
    o.append(t(380, 106, "mean val", 12, MUT, "end"))
    A = [(8, 6300, "0.046"), (32, 1560, "0.039"), (64, 780, "0.039"), (128, 360, "0.039"), (512, 60, "0.053")]
    bx = lambda s: 112 + (math.log10(s) - 1) * 52.0       # 10 -> 112, 10000 -> 268
    for d in (10, 100, 1000, 10000):
        o.append(line(bx(d), 118, bx(d), 322, GRID, 1.5, "6 4"))
        o.append(t(bx(d), 340, str(d), 12, MUT, "middle"))
    for i, (b, st, mv) in enumerate(A):
        yc = 140 + i * 40
        o.append(t(34, yc + 5, "batch %d" % b, 14, INK, "start"))
        o.append(rect(bx(10), yc - 10, bx(st) - bx(10), 20, 4, DATA_F, DATA_S, 2))
        o.append(t(bx(st) + 6, yc + 4, str(st), 12, INK, "start"))
        hi = b == 512
        o.append(t(380, yc + 5, mv, 14, ACC_S if hi else INK, "end"))
    o.append(t(380, 316, "worst: 60 steps", 12, ACC_S, "end"))
    # panel B: same 780 steps
    o.append(rect(408, 62, 372, 290, 12, PANEL, GRID, 2))
    o.append(t(422, 86, "B  same 780 steps", 18, INK, "start"))
    o.append(t(422, 106, "bars: loss, mean of 5 seeds (0 to 0.08)", 12, MUT, "start"))
    B = [(32, 30, 0.034, 0.029), (64, 60, 0.039, 0.006), (128, 130, 0.073, 0.005), (256, 260, 0.073, 0.000)]
    sc = 180 / 0.08
    for i, (b, ep, v, tr) in enumerate(B):
        yc = 140 + i * 52
        o.append(t(422, yc, "batch %d" % b, 14, INK, "start"))
        o.append(t(422, yc + 16, "%d epochs" % ep, 12, MUT, "start"))
        o.append(rect(520, yc - 18, v * sc, 16, 4, DATA_F, DATA_S, 2))
        o.append(t(520 + v * sc + 6, yc - 5, "val %.3f" % v, 12, INK, "start"))
        o.append(rect(520, yc + 2, max(tr * sc, 2), 16, 4, PAPER, DATA_S, 2, "4 3"))
        o.append(t(520 + max(tr * sc, 2) + 6, yc + 15, "train %.3f" % tr, 12, MUT, "start"))
    o.append(t(520, 340, "solid = validation, dashed = train", 12, MUT, "start"))
    o.append(cap("A fixes epochs, so steps change. B fixes steps, so epochs change. Neither fixes everything."))
    fig("fig-w04-2-batch-size-hold-what-fixed.svg", "0 0 800 400",
        "Changing the batch size also changes the step count, so each experiment holds one thing fixed",
        "Two panels. A, same 60 epochs: batch 8, 32, 64, 128 and 512 take 6300, 1560, 780, 360 and 60 optimizer steps "
        "(log-scale bars) with mean validation loss 0.046, 0.039, 0.039, 0.039 and 0.053 over seeds 0 to 4. B, same 780 "
        "steps: batch 32, 64, 128 and 256 need 30, 60, 130 and 260 epochs, with mean validation loss 0.034, 0.039, "
        "0.073 and 0.073 and mean training loss 0.029, 0.006, 0.005 and 0.000.", o)


# ---------------------------------------------------------------- W5-1  train vs val, no cure
def w05_1():
    ep = [0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 249]
    tr = [0.691, 0.217, 0.155, 0.123, 0.021, 0.032, 0.001, 0.000, 0.000, 0.000, 0.000]
    va = [0.688, 0.220, 0.196, 0.214, 0.320, 0.507, 0.694, 0.792, 0.840, 0.877, 0.906]
    x0, x1, yb, yt = 90, 560, 316, 96
    X = lambda e: x0 + e / 249.0 * (x1 - x0)
    Y = lambda v: yb - v / 1.0 * (yb - yt)
    o = [ctitle("Train loss hits 0.000 as validation loss climbs")]
    for v in (0, 0.5, 1.0):
        o.append(line(x0, Y(v), x1, Y(v), GRID, 1.5))
        o.append(t(x0 - 8, Y(v) + 4, "%g" % v if v else "0", 12, MUT, "end"))
    o.append(line(x0, Y(0.693), x1, Y(0.693), GRID, 1.5, "6 4"))
    o.append(t(x0 + 6, Y(0.693) - 6, "coin floor ln 2 = 0.693", 12, MUT, "start"))
    o.append(line(x0, yt, x0, yb, INK, 2))
    o.append(line(x0, yb, x1, yb, INK, 2))
    for e in (0, 50, 100, 150, 200, 249):
        o.append(line(X(e), yb, X(e), yb + 5, MUT, 1.5))
        o.append(t(X(e), yb + 20, str(e), 12, MUT, "middle"))
    o.append(t((x0 + x1) / 2.0, 350, "epoch (a dot every 25 epochs)", 12, MUT, "middle"))
    o.append(trot(40, (yb + yt) / 2.0, "loss", 12))
    o.append(poly([(X(e), Y(v)) for e, v in zip(ep, tr)], "none", DATA_S, 3))
    o.append(poly([(X(e), Y(v)) for e, v in zip(ep, va)], "none", HUMAN_S, 3, "6 4"))
    for e, v in zip(ep, tr):
        o.append(mark("circle", X(e), Y(v), 4, DATA_S, PAPER, 2))
    for e, v in zip(ep, va):
        o.append(mark("square", X(e), Y(v), 4, HUMAN_S, PAPER, 2))
    o.append(t(X(249) - 6, Y(0.000) - 10, "train, solid", 12, DATA_S, "end"))
    o.append(t(X(249) - 6, Y(0.906) - 10, "validation, dashed", 12, HUMAN_S, "end"))
    # best epoch 59: val 0.179
    o.append(mark("diamond", X(59), Y(0.179), 6, ACC_S, ACC_F, 3))
    o.append(ring_num(X(59) - 24, Y(0.179) + 26, 1))
    # gap bracket on the right
    gx = x1 + 22
    o.append(path("M%s %s H%s V%s H%s" % (f2(gx - 6), f2(Y(0.906)), f2(gx), f2(Y(0.0)), f2(gx - 6)), "none", ACC_S, 3))
    o.append(t(gx + 10, Y(0.45) - 8, "gap", 14, ACC_S, "start"))
    o.append(t(gx + 10, Y(0.45) + 8, "0.906", 14, ACC_S, "start"))
    o.append(t(gx + 10, Y(0.45) + 24, "&#8722; 0.000", 12, MUT, "start"))
    o.append(cap("Seed 0, no cure. Ringed 1: epoch 59, validation loss 0.179. At epoch 249 it is 0.906."))
    fig("fig-w05-1-memorising-train-val-gap.svg", "0 0 800 400",
        "Training loss can reach zero while validation loss gets worse: that is memorising",
        "Loss against epoch for seed 0 with 120 training points and no cure. Training loss falls from 0.691 to 0.000 "
        "by epoch 175 and stays there. Validation loss falls from 0.688 to a best of 0.179 at epoch 59 (ringed 1), "
        "then climbs through 0.320 at epoch 100 and 0.694 at epoch 150 to 0.906 at epoch 249. A bracket marks the "
        "final gap, 0.906 minus 0.000.", o)


# ---------------------------------------------------------------- W5-2  four cures, five seeds
def w05_2():
    rows = [("no cure", (0.159, 0.204, 0.264), (0.435, 0.803, 1.285)),
            ("early stop (p=25)", (0.159, 0.212, 0.264), (0.227, 0.351, 0.589)),
            ("dropout 0.3", (0.122, 0.190, 0.257), (0.449, 0.575, 0.732)),
            ("weight decay 0.3", (0.138, 0.185, 0.246), (0.274, 0.389, 0.537)),
            ("jitter 0.1", (0.113, 0.149, 0.180), (0.197, 0.366, 0.524))]
    o = [ctitle("One cure at a time, five seeds each")]
    ax1 = lambda v: 200 + (v - 0.10) / 0.20 * 190        # 0.10 .. 0.30 -> 200..390
    ax2 = lambda v: 480 + v / 1.4 * 280                  # 0 .. 1.4 -> 480..760
    o.append(t(295, 82, "best val (hindsight)", 14, INK, "middle"))
    o.append(t(620, 82, "final val (after 250 epochs)", 14, INK, "middle"))
    for v in (0.10, 0.20, 0.30):
        o.append(line(ax1(v), 96, ax1(v), 316, GRID, 1.5, "6 4"))
        o.append(t(ax1(v), 334, "%.2f" % v, 12, MUT, "middle"))
    for v in (0, 0.5, 1.0):
        o.append(line(ax2(v), 96, ax2(v), 316, GRID, 1.5, "6 4"))
        o.append(t(ax2(v), 334, "%g" % v if v else "0", 12, MUT, "middle"))
    for i, (name, b, f) in enumerate(rows):
        yc = 130 + i * 44
        o.append(t(20, yc + 5, name, 14, INK, "start"))
        for (lo, mn, hi), fx, col in ((b, ax1, DATA_S), (f, ax2, HUMAN_S)):
            o.append(line(fx(lo), yc, fx(hi), yc, col, 3))
            o.append(line(fx(lo), yc - 6, fx(lo), yc + 6, col, 3))
            o.append(line(fx(hi), yc - 6, fx(hi), yc + 6, col, 3))
            o.append(mark("diamond", fx(mn), yc, 5, col, PAPER, 2))
            o.append(t(fx(mn), yc - 12, "%.3f" % mn, 12, INK, "middle"))
    o.append(t(295, 352, "bar = lowest to highest, diamond = mean of seeds 0&#8211;4", 12, MUT, "middle"))
    o.append(cap("Best-val bars overlap. Final-val means: no cure 0.803, the cures 0.351&#8211;0.575."))
    fig("fig-w05-2-four-cures-five-seeds.svg", "0 0 800 400",
        "Five seeds show which differences are real: the final-loss means separate the cures, the best-loss bars overlap",
        "Two panels of range bars over seeds 0 to 4, one row per cure. Best validation loss, mean (lowest to highest): "
        "no cure 0.204 (0.159 to 0.264), early stop 0.212 (0.159 to 0.264), dropout 0.190 (0.122 to 0.257), weight "
        "decay 0.185 (0.138 to 0.246), jitter 0.149 (0.113 to 0.180). Final validation loss: no cure 0.803 (0.435 to "
        "1.285), early stop 0.351 (0.227 to 0.589), dropout 0.575 (0.449 to 0.732), weight decay 0.389 (0.274 to "
        "0.537), jitter 0.366 (0.197 to 0.524).", o)


# ---------------------------------------------------------------- W6-1  the road back
def w06_1():
    plain = [0.3, 0.2, 0.4, 0.1]
    road = [1 + s for s in plain]

    def runs(xs):
        out, r = [], 1.0
        for x in xs:
            r *= x
            out.append(r)
        return out

    rp, rr = runs(plain), runs(road)
    assert round(rp[-1], 4) == 0.0024 and round(rr[-1], 4) == 2.4024
    o = [ctitle("A road keeps the error from shrinking")]
    SC = 68.0
    panels = [(20, "plain stack", plain, rp, ["0.3", "0.2", "0.4", "0.1"], False),
              (408, "residual stack", road, rr, ["1 + 0.3 = 1.3", "1 + 0.2 = 1.2", "1 + 0.4 = 1.4", "1 + 0.1 = 1.1"], True)]
    for px, name, sl, run, lab, res in panels:
        o.append(rect(px, 62, 372, 270, 12, PANEL, GRID, 2))
        o.append(t(px + 14, 86, name, 18, INK, "start"))
        bx0 = px + 150
        o.append(line(bx0 + SC, 96, bx0 + SC, 322, GRID, 1.5, "6 4"))
        o.append(t(bx0 + SC, 342, "1 = unchanged", 12, MUT, "middle"))
        yc0 = 120
        o.append(t(px + 14, yc0 + 5, "error at the end", 12, MUT, "start"))
        o.append(rect(bx0, yc0 - 9, SC, 18, 4, DATA_F, DATA_S, 2))
        o.append(t(bx0 + SC + 8, yc0 + 5, "1", 14, INK, "start"))
        for i in range(4):
            yc = 168 + i * 48
            o.append(rect(px + 14, yc - 20, 112, 40, 8, MODEL_F, MODEL_S, 3))
            o.append(t(px + 70, yc - 4, "block %d" % (i + 1), 14, INK, "middle"))
            o.append(t(px + 70, yc + 13, "slope " + lab[i] if not res else lab[i], 12, INK, "middle"))
            v = run[i]
            last = i == 3
            w = max(v * SC, 2.0)
            fillc, strk = (DATA_F, DATA_S)
            if last:
                fillc, strk = (OK_F, OK_S) if res else (BAD_F, BAD_S)
            o.append(rect(bx0, yc - 9, w, 18, 4, fillc, strk, 2))
            txt = ("%.4f" % v).rstrip("0").rstrip(".") if v < 1 else ("%.4f" % v).rstrip("0")
            if res:
                txt = {0: "1.3", 1: "1.56", 2: "2.184", 3: "2.4024"}[i]
            else:
                txt = {0: "0.3", 1: "0.06", 2: "0.024", 3: "0.0024"}[i]
            o.append(t(bx0 + w + 8, yc + 5, txt, 14, INK, "start"))
    o.append(cap("0.3 &#215; 0.2 &#215; 0.4 &#215; 0.1 = 0.0024, but 1.3 &#215; 1.2 &#215; 1.4 &#215; 1.1 = 2.4024. Bar = running product."))
    fig("fig-w06-1-residual-road-four-blocks.svg", "0 0 800 400",
        "Adding a road to each block turns a shrinking product into a steady one",
        "Two stacks of four blocks, with the error's running product drawn as a horizontal bar next to each. Plain "
        "stack, slopes 0.3, 0.2, 0.4, 0.1: the running product goes 0.3, 0.06, 0.024, 0.0024, a hairline. Residual "
        "stack, each slope one plus the old slope, 1.3, 1.2, 1.4, 1.1: 1.3, 1.56, 2.184, 2.4024. A dashed line "
        "marks 1, meaning unchanged.", o)


# ---------------------------------------------------------------- W6-2  gradient and accuracy by depth
def w06_2():
    depths = [2, 8, 16, 32]
    pg = [7.01e-02, 3.23e-05, 1.21e-09, 1.27e-18]
    rg = [4.26e-01, 1.27e+00, 2.61e+00, 3.00e+02]
    pgl = ["7.01e&#8722;02", "3.23e&#8722;05", "1.21e&#8722;09", "1.27e&#8722;18"]
    rgl = ["4.26e&#8722;01", "1.27e+00", "2.61e+00", "3.00e+02"]
    pa = [99.2, 99.1, 46.9, 46.9]
    ra = [99.2, 99.2, 99.0, 99.3]
    o = [ctitle("A tiny start gradient means a net that cannot train")]
    # left: log chart
    lx0, lx1, yb, yt = 92, 400, 316, 100
    px = lambda i: lx0 + 40 + i * 76
    py = lambda v: yb - (math.log10(v) + 18) / 21.0 * (yb - yt)
    o.append(t(250, 84, "gradient length on block 1, seed 0", 14, INK, "middle"))
    for e in (-18, -12, -6, 0):
        o.append(line(lx0, py(10.0 ** e), lx1, py(10.0 ** e), GRID, 1.5, "6 4"))
        o.append(t(lx0 - 6, py(10.0 ** e) + 4, "1e%s" % (("&#8722;%d" % -e) if e < 0 else str(e)), 12, MUT, "end"))
    o.append(line(lx0, yt, lx0, yb, INK, 2))
    o.append(line(lx0, yb, lx1, yb, INK, 2))
    o.append(trot(38, (yb + yt) / 2.0, "length (log scale)", 12))
    o.append(poly([(px(i), py(v)) for i, v in enumerate(pg)], "none", BAD_S, 3, "6 4"))
    o.append(poly([(px(i), py(v)) for i, v in enumerate(rg)], "none", OK_S, 3))
    for i, d in enumerate(depths):
        o.append(mark("triangle", px(i), py(pg[i]), 6, BAD_S, PAPER, 2))
        o.append(mark("circle", px(i), py(rg[i]), 6, OK_S, PAPER, 2))
        o.append(t(px(i), yb + 20, str(d), 12, MUT, "middle"))
        if i < 3:
            o.append(t(px(i) + 8, py(pg[i]) + 20, pgl[i], 12, INK, "middle"))
            o.append(t(px(i), py(rg[i]) - 12, rgl[i], 12, INK, "middle"))
        else:
            o.append(t(px(i) + 12, py(pg[i]) - 4, pgl[i], 12, INK, "start"))
            o.append(t(px(i) + 12, py(rg[i]) + 4, rgl[i], 12, INK, "start"))
    o.append(t(lx0 + 150, yb + 38, "depth (blocks)", 12, MUT, "middle"))
    o.append(line(104, 262, 132, 262, BAD_S, 3, "6 4"))
    o.append(mark("triangle", 118, 262, 5, BAD_S, PAPER, 2))
    o.append(t(140, 266, "plain, dashed", 12, BAD_S, "start"))
    o.append(line(104, 284, 132, 284, OK_S, 3))
    o.append(mark("circle", 118, 284, 5, OK_S, PAPER, 2))
    o.append(t(140, 288, "residual, solid", 12, OK_S, "start"))
    # right: accuracy bars
    rx0, ry = 470, 0
    ay = lambda a: yb - a / 100.0 * (yb - yt)
    o.append(t(625, 84, "accuracy, mean of 3 seeds", 14, INK, "middle"))
    for a in (0, 100):
        o.append(line(rx0, ay(a), 780, ay(a), GRID, 1.5, "6 4" if a else None))
        o.append(t(rx0 - 6, ay(a) + 4, "%d%%" % a, 12, MUT, "end"))
    o.append(line(rx0, ay(46.9), 780, ay(46.9), MUT, 2, "2 4"))
    o.append(t(rx0 - 6, ay(46.9) + 4, "coin 46.9%", 12, MUT, "end"))
    gx = lambda i: rx0 + 14 + i * 76
    for i, d in enumerate(depths):
        bad = pa[i] < 50
        o.append(rect(gx(i), ay(pa[i]), 28, yb - ay(pa[i]), 2, BAD_F if bad else PANEL, BAD_S if bad else DATA_S, 2, None if bad else "4 3"))
        o.append(rect(gx(i) + 30, ay(ra[i]), 28, yb - ay(ra[i]), 2, OK_F, OK_S, 2))
        o.append(t(gx(i) + 14, ay(pa[i]) - 6, "%.1f" % pa[i], 12, INK, "middle"))
        o.append(t(gx(i) + 44, ay(ra[i]) - 6, "%.1f" % ra[i], 12, INK, "middle"))
        o.append(t(gx(i) + 29, yb + 20, str(d), 12, MUT, "middle"))
    o.append(t(625, yb + 38, "depth: dashed plain, solid residual", 12, MUT, "middle"))
    o.append(line(rx0, yt, rx0, yb, INK, 2))
    o.append(line(rx0, yb, 780, yb, INK, 2))
    o.append(cap("Plain at depth 16 and 32 only matches the coin; with the road, every depth is near 99%."))
    fig("fig-w06-2-depth-gradient-vs-accuracy.svg", "0 0 800 400",
        "The gradient table predicts which plain stacks cannot train, and the road fixes them",
        "Left, first-block gradient length at the start on a log scale for depths 2, 8, 16, 32. Plain: 7.01e-02, "
        "3.23e-05, 1.21e-09, 1.27e-18. Residual: 4.26e-01, 1.27e+00, 2.61e+00, 3.00e+02. Right, validation accuracy "
        "after 30 epochs, mean of seeds 0 to 2. Plain: 99.2, 99.1, 46.9, 46.9 percent. Residual: 99.2, 99.2, 99.0, "
        "99.3 percent. A dotted line marks the coin, 46.9 percent. The layer norm columns are not drawn.", o)


def build():
    for f in (w04_1, w04_2, w05_1, w05_2, w06_1, w06_2):
        f()
    return FIGS

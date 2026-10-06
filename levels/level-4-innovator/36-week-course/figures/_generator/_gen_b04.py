"""Block 4 (weeks 10, 11, 12) concept figures. Writes fig-w10-1 ... fig-w12-2 into figures/.

Every number printed here is copied from the executed output in that week's student guide
(Week 10 blocks 1 and 5, Week 11 blocks 1, 2 and 5, Week 12 blocks 1 and 2) or is a sum of those.
Nothing here is random. Roles follow STYLE.md 2.7. Called from _gen_build.py via emit_b04().
"""
import math
import os
from _gen_core import *

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # figures/
MINUS, TIMES, DIV, ARROW, MID = "&#8722;", "&#215;", "&#247;", "&#8594;", "&#183;"
EM = "&#8212;"


def title(s):
    return t(400, 46, s, 24, INK, "middle")


def caption(s, y=375):
    return t(400, y, s, 14, MUT, "middle")


def panel(x, y, w, h, stroke=GRID, dash=None):
    return rect(x, y, w, h, 12, PANEL, stroke, 2, dash)


def bar(x, base, h, w, fill, stroke, sw=2):
    h = max(h, 2)
    return sq(x, base - h, w, h, fill, stroke, sw)


def sci(v):
    return ("%.2e" % v).replace("e-0", "e&#8722;0").replace("e-", "e&#8722;").replace("e+0", "e+0")


# ============================================================ week 10, figure 1
def w10_1():
    ks = [1, 2, 5, 10, 20, 40]
    low = [0.9526, 0.9074, 0.7844, 0.6153, 0.3786, 0.1434]
    high = [1.05, 1.103, 1.276, 1.629, 2.653, 7.04]
    base = 300
    o = [title("Forty small steps compound")]
    for px, vals, unit, head_, sub, refs in (
            (20, low, 150.0, "rate 0.9526: tiny", "each step keeps 95.26%; dashed: 1 and 0.5",
             [(1.0, "1"), (0.5, "0.5")]),
            (410, high, 20.0, "rate 1.05: huge", "each step adds 5%; dashed: 1 and 2",
             [(1.0, "1"), (2.0, "2")])):
        o.append(panel(px, 66, 370, 284))
        o.append(t(px + 185, 94, head_, 18, INK, "middle"))
        o.append(t(px + 185, 112, sub, 12, MUT, "middle"))
        for rv, lab in refs:
            y = base - rv * unit
            o.append(line(px + 14, y, px + 356, y, GRID, 1.5, "6 4"))
            o.append(t(px + 60, y + 4, lab, 12, MUT, "end"))
        o.append(line(px + 66, base, px + 360, base, INK, 2))
        for i, (k, v) in enumerate(zip(ks, vals)):
            x = px + 70 + i * 48
            last = (k == 40)
            o.append(bar(x, base, v * unit, 38, ACC_F if last else DATA_F, ACC_S if last else DATA_S, 3 if last else 2))
            o.append(t(x + 19, base - max(v * unit, 2) - 6, ("%.4g" % v), 12, INK, "middle"))
            o.append(t(x + 19, base + 18, str(k), 12, MUT, "middle"))
        o.append(t(px + 213, base + 36, "multiplications in a row (k)", 12, MUT, "middle"))
    o.append(caption("Forty times: 0.9526 leaves 0.1434, 1.05 gives 7.04. Only exactly 1 stays put.", 375))
    return svg_doc(
        "0 0 800 400",
        "Below 1 the repeated multiplication shrinks to almost nothing and above 1 it grows large; only exactly 1 stays put",
        "Two bar panels, each with six bars for k = 1, 2, 5, 10, 20 and 40 multiplications. Left panel, rate 0.9526: "
        "0.9526, 0.9074, 0.7844, 0.6153, 0.3786 and 0.1434, falling toward zero, with dashed lines at 1 and 0.5. "
        "Right panel, rate 1.05: 1.05, 1.103, 1.276, 1.629, 2.653 and 7.04, rising, with dashed lines at 1 and 2. "
        "The k = 40 bar in each panel is highlighted. The two panels use different heights per unit. Values are the "
        "Week 10 block 1 printout, plain arithmetic with no random numbers.",
        J(o))


# ============================================================ week 10, figure 2
GRID10 = [("x1", ["9.15e-03", "1.01e-05", "2.06e-10", "4.69e-21"]),
          ("x2", ["5.63e-01", "1.66e-02", "2.25e-03", "2.93e-06"]),
          ("x4", ["1.08e+01", "1.14e+01", "2.09e+01", "3.36e+03"]),
          ("x8", ["3.49e+01", "2.55e+02", "4.38e+03", "6.92e+07"])]


def _cls(v):
    return ("V", "vanishing") if v < 0.001 else (("E", "exploding") if v > 10 else ("L", "level"))


def w10_2():
    o = [title("No row of the grid stays near 4.0")]
    x0, y0, cw, ch = 150, 120, 104, 56
    o.append(t(x0 + 2 * cw, 84, "sequence length T (steps the error travels back)", 12, MUT, "middle"))
    for j, T in enumerate([10, 20, 40, 80]):
        o.append(t(x0 + j * cw + cw / 2.0, 108, "T = %d" % T, 14, INK, "middle"))
    o.append(trot(36, y0 + 2 * ch, "recurrent-weight scale", 12, MUT))
    counts = {"V": 0, "L": 0, "E": 0}
    desc_rows = []
    for i, (lab, vals) in enumerate(GRID10):
        y = y0 + i * ch
        o.append(t(x0 - 10, y + ch / 2.0 + 5, "scale &#215;" + lab[1:], 14, INK, "end"))
        for j, s in enumerate(vals):
            v = float(s)
            c, word = _cls(v)
            counts[c] += 1
            if c == "L":
                f, st, sw = OK_F, OK_S, 2
            elif c == "V":
                f, st, sw = PANEL, BAD_S, 2
            else:
                f, st, sw = BAD_F, BAD_S, 3
            x = x0 + j * cw
            o.append(sq(x, y, cw, ch, f, st, sw))
            o.append(t(x + 8, y + 18, "%s %s" % (c, word), 12, INK))
            o.append(t(x + cw / 2.0, y + 41, sci(v), 14, INK, "middle", mono=True))
    # legend
    lx = 584
    o.append(panel(lx, 120, 196, 224))
    o.append(t(lx + 14, 146, "Cut-offs (ours)", 14, INK))
    for k, (c, word, rng, f, st, sw) in enumerate([
            ("V", "vanishing", "below 0.001", PANEL, BAD_S, 2),
            ("L", "level", "0.001 to 10", OK_F, OK_S, 2),
            ("E", "exploding", "above 10", BAD_F, BAD_S, 3)]):
        y = 162 + k * 44
        o.append(sq(lx + 14, y, 34, 34, f, st, sw))
        o.append(t(lx + 31, y + 22, c, 18, INK, "middle"))
        o.append(t(lx + 58, y + 14, word, 14, INK))
        o.append(t(lx + 58, y + 30, rng, 12, MUT))
    o.append(t(lx + 14, 312, "The last position's", 12, MUT))
    o.append(t(lx + 14, 328, "gradient is always 4.0.", 12, MUT))
    o.append(caption("Seed 0, one untrained cell, Week 10 block 5. Counts: %d vanishing, %d level, %d exploding of 16." % (counts["V"], counts["L"], counts["E"]), 375))
    return svg_doc(
        "0 0 800 400",
        "The size of the gradient at position 1 is never close to the 4.0 at the last position: it falls or climbs by orders of magnitude",
        "A grid of 16 cells, rows for recurrent-weight scale 1, 2, 4 and 8, columns for sequence length T = 10, 20, 40 and 80, each cell printing "
        "the measured gradient at position 1 and a class word. Scale 1: 9.15e-03, 1.01e-05, 2.06e-10, 4.69e-21. Scale 2: 5.63e-01, 1.66e-02, "
        "2.25e-03, 2.93e-06. Scale 4: 1.08e+01, 1.14e+01, 2.09e+01, 3.36e+03. Scale 8: 3.49e+01, 2.55e+02, 4.38e+03, 6.92e+07. "
        "Cells below 0.001 are labelled V vanishing, above 10 E exploding, otherwise L level. That gives %d V, %d L, %d E. Cut-offs are the course's "
        "own. Seed 0." % (counts["V"], counts["L"], counts["E"]),
        J(o))


# ============================================================ week 11, figure 1
def w11_1():
    rnn_raw = [0.7616, 0.3634, 0.1797, 0.0896]
    rnn_pct = [100.0, 47.7, 23.6, 11.8]
    lstm_raw = [0.8909, 0.8486, 0.8084, 0.7701]
    lstm_pct = [100.0, 95.3, 90.7, 86.4]
    base, unit = 286, 1.2
    o = [title("Rewrite loses the past; add keeps it")]
    for px, raw, pct, st, fl, head_, sub, last, rawlab in (
            (20, rnn_raw, rnn_pct, BAD_S, BAD_F, "RNN: the note is rewritten",
             "the old note is pushed through a weight", "slope back 3 steps: 0.1041", "note"),
            (410, lstm_raw, lstm_pct, OK_S, OK_F, "LSTM: the memory is added to",
             "the old memory is only scaled, then added to", "slope back 3 steps: 0.8644 (f = 0.9526)", "memory")):
        o.append(panel(px, 66, 370, 286))
        o.append(t(px + 185, 94, head_, 18, INK, "middle"))
        o.append(t(px + 185, 112, sub, 12, MUT, "middle"))
        o.append(line(px + 48, base - 100 * unit, px + 356, base - 100 * unit, GRID, 1.5, "6 4"))
        o.append(t(px + 44, base - 100 * unit + 4, "100%", 12, MUT, "end"))
        o.append(line(px + 50, base, px + 358, base, INK, 2))
        for i in range(4):
            x = px + 66 + i * 74
            h = pct[i] * unit
            o.append(bar(x, base, h, 50, fl, st, 3 if i == 3 else 2))
            o.append(t(x + 25, base - h - 6, "%.1f%%" % pct[i], 12, INK, "middle"))
            o.append(t(x + 25, base + 16, "step %d" % (i + 1), 12, MUT, "middle"))
            o.append(t(x + 25, base + 31, "%.4f" % raw[i], 12, MUT, "middle"))
        o.append(t(px + 185, 342, last, 14, INK, "middle"))
    o.append(badge_cross(px_bad := 36, 70, 0.28))
    o.append(badge_check(426, 70, 0.28))
    o.append(caption("One unit, spike (1, 0, 0, 0), 4 steps. Bars are % of step 1, raw value below.", 375))
    return svg_doc(
        "0 0 800 400",
        "A memory that is scaled and added to keeps most of step 1 over four steps, a note that is rewritten keeps almost none",
        "Two bar panels over four steps for one unit fed the spike 1, 0, 0, 0, each bar a percentage of step 1. Left, the plain RNN note "
        "(0.7616, 0.3634, 0.1797, 0.0896): 100%, 47.7%, 23.6%, 11.8%, marked with a cross; slope back three steps 0.1041. Right, the LSTM memory "
        "(0.8909, 0.8486, 0.8084, 0.7701): 100%, 95.3%, 90.7%, 86.4%, marked with a tick; slope back three steps 0.8644, the forget dial 0.9526 "
        "multiplied three times. Values from Week 11 block 2.",
        J(o))


# ============================================================ week 11, figure 2
def w11_2():
    fb = [0.0, 1.0, 2.0, 4.0]
    avgf = [0.510, 0.732, 0.879, 0.981]
    ratio = ["1.93e-09", "9.84e-04", "2.21e-01", "1.08e+00"]
    o = [title("Start the forget dial high")]
    for i in range(4):
        px = 30 + i * 185
        r = float(ratio[i])
        ok = r >= 0.01
        o.append(panel(px, 66, 170, 288, OK_S if ok else BAD_S, None if ok else "6 4"))
        o.append(t(px + 85, 94, "forget bias %g" % fb[i], 18, INK, "middle"))
        o.append(t(px + 15, 128, "average dial f at step 1", 12, MUT))
        o.append(sq(px + 20, 138, 130, 22, PAPER, INK, 2))
        o.append(sq(px + 20, 138, 130 * avgf[i], 22, DATA_F, DATA_S, 2))
        o.append(t(px + 85, 180, "f = %.3f" % avgf[i], 14, INK, "middle"))
        o.append(t(px + 15, 212, "position 1 &#247; position 40", 12, MUT))
        o.append(t(px + 85, 240, sci(r), 18, INK, "middle"))
        frac = max(0.0, min(1.0, (math.log10(r) + 10) / 10.0))
        o.append(sq(px + 20, 252, 130, 18, PAPER, INK, 2))
        o.append(sq(px + 20, 252, 130 * frac, 18, ACC_F, ACC_S, 2))
        o.append(t(px + 20, 286, "1e&#8722;10", 12, MUT))
        o.append(t(px + 150, 286, "1", 12, MUT, "end"))
        o.append(t(px + 85, 304, "log scale, bar ends at 1", 12, MUT, "middle"))
        o.append(badge_check(px + 14, 316, 0.3) if ok else badge_cross(px + 14, 316, 0.3))
        o.append(t(px + 52, 336, "still reaches back" if ok else "Week 10 again", 12, INK))
    o.append(caption("Same cell, only the bias changes. Seed 0, 40 steps. Tick: at least 1% (our cut).", 375))
    return svg_doc(
        "0 0 800 400",
        "Raising the forget bias before training lets the first step reach the last: one bias number turns Week 10's fade into a highway",
        "Four panels for forget bias 0, 1, 2 and 4. Each shows the average forget dial at step 1 as a bar out of 1: 0.510, 0.732, 0.879, 0.981; "
        "and the measured ratio of the gradient at position 1 to position 40: 1.93e-09, 9.84e-04, 2.21e-01, 1.08e+00, with a log-scale bar from "
        "1e-10 to 1. Biases 0 and 1 have dashed red outlines and a cross, biases 2 and 4 a tick. Values from Week 11 block 5, seed 0, 40 steps.",
        J(o))


# ============================================================ week 12, figure 1
def w12_1():
    inp = [(0, "START"), (2, "a"), (15, "n"), (10, "i"), (12, "k"), (2, "a"), (1, "EOS"), (0, "PAD")]
    tgt = [(2, "a"), (15, "n"), (10, "i"), (12, "k"), (2, "a"), (1, "EOS"), (0, "PAD"), (0, "PAD")]
    x0, cw, iy, ty, ch = 196, 70, 120, 232, 56
    o = [title("Shift right: the answer becomes the next question")]
    for j in range(8):
        o.append(t(x0 + j * cw + cw / 2.0, 108, "step %d" % j, 12, MUT, "middle"))
    for j in range(7):
        o.append(arrow(x0 + j * cw + cw / 2.0 + 8, ty - 4, x0 + (j + 1) * cw + cw / 2.0 - 8, iy + ch + 6, ACC_S, 2))

    def cell(x, y, tid, word, kind):
        if kind == "pad":
            f, s, sw, d = PANEL, GRID, 2, "6 4"
        elif kind == "start":
            f, s, sw, d = PANEL, INK, 2, None
        elif kind == "eos":
            f, s, sw, d = DATA_F, ACC_S, 3, None
        else:
            f, s, sw, d = DATA_F, DATA_S, 2, None
        out = [rect(x + 3, y, cw - 6, ch, 8, f, s, sw, d)]
        out.append(t(x + cw / 2.0, y + 24, word, 14, INK, "middle", mono=True))
        out.append(t(x + cw / 2.0, y + 44, "id %d" % tid, 12, MUT, "middle"))
        return out

    def kind(tid, word):
        return "pad" if word == "PAD" else ("start" if word == "START" else ("eos" if word == "EOS" else "x"))

    for j, (tid, w) in enumerate(inp):
        o += cell(x0 + j * cw, iy, tid, w, kind(tid, w))
    for j, (tid, w) in enumerate(tgt):
        o += cell(x0 + j * cw, ty, tid, w, kind(tid, w))
    o.append(t(176, iy + 22, "input", 18, INK, "end"))
    o.append(t(176, iy + 40, "just said", 12, MUT, "end"))
    o.append(shape_chip(110, iy + 48, "(231, 8)"))
    o.append(t(176, ty + 22, "target", 18, INK, "end"))
    o.append(t(176, ty + 40, "say next", 12, MUT, "end"))
    o.append(shape_chip(110, ty + 48, "(231, 8)"))
    o.append(t(400, 322, "The name anika: 5 letters, then EOS, then 2 PAD = 8 steps.", 14, INK, "middle"))
    o.append(t(400, 344, "Step 0 starts from START (the id of PAD, 0): nothing said yet. Step 6 shows EOS and asks for PAD.", 12, MUT, "middle"))
    o.append(caption("Each pink arrow: this step's target is the next step's input.", 376))
    return svg_doc(
        "0 0 800 400",
        "Training shifts the names one place right so that every step is asked for the letter that comes next",
        "Two rows of eight cells for the name anika, each with its id. Input row: START 0, a 2, n 15, i 10, k 12, a 2, EOS 1, PAD 0. "
        "Target row: a 2, n 15, i 10, k 12, a 2, EOS 1, PAD 0, PAD 0. Seven pink arrows lead from each target cell up and to the right to the "
        "next input cell. Both rows are tensors of shape (231, 8) over all 231 names. Values from Week 12 block 1.",
        J(o))


# ============================================================ week 12, figure 2
def w12_2():
    surprise = [0.6931, 1.3863, 0.2231, 2.3026]
    pad = 0.0202
    base, unit = 300, 60.0
    o = [title("Counting padding flatters the loss")]
    o.append(panel(20, 66, 500, 286))
    o.append(t(270, 94, "One name, uma: 8 positions", 18, INK, "middle"))
    o.append(t(270, 112, "surprise per step, probabilities invented for the hand sum", 12, MUT, "middle"))
    o.append(line(60, base, 496, base, INK, 2))
    labs = ["u", "m", "a", "EOS"] + ["PAD"] * 4
    vals = surprise + [pad] * 4
    for i, v in enumerate(vals):
        x = 62 + i * 54
        real = i < 4
        o.append(bar(x, base, v * unit, 42, DATA_F if real else PANEL, DATA_S if real else GRID, 2))
        o.append(t(x + 21, base - max(v * unit, 2) - 6, "%.4g" % v, 12, INK, "middle"))
        o.append(t(x + 21, base + 16, labs[i], 12, MUT, "middle"))
    o.append(bracket(62, 62 + 3 * 54 + 42, base + 24, 8, MUT, True))
    o.append(t(62 + 105, base + 52, "4 real targets: sum 4.6051", 12, INK, "middle"))
    o.append(bracket(62 + 4 * 54, 62 + 7 * 54 + 42, base + 24, 8, MUT, True))
    o.append(t(62 + 4 * 54 + 105, base + 52, "4 padding: 0.0202 each", 12, MUT, "middle"))
    # right panel
    o.append(panel(540, 66, 240, 286))
    o.append(t(660, 94, "Average loss", 18, INK, "middle"))
    o.append(t(660, 112, "same model, same name", 12, MUT, "middle"))
    o.append(line(560, base, 760, base, INK, 2))
    for x, v, f, s, a, b, ic in ((566, 1.1513, OK_F, OK_S, "ignore PAD", "sum " + DIV + " 4", True),
                                 (668, 0.5857, BAD_F, BAD_S, "count PAD", "sum " + DIV + " 8", False)):
        o.append(bar(x, base, v * unit, 84, f, s, 3))
        o.append(t(x + 42, base - v * unit - 8, "%.4f" % v, 14, INK, "middle"))
        o.append((badge_check if ic else badge_cross)(x + 29, base - v * unit + 8, 0.26))
        o.append(t(x + 42, base + 16, a, 12, INK, "middle"))
        o.append(t(x + 42, base + 32, b, 12, MUT, "middle"))
    o.append(caption("Loss halved, no letter learned: easy PAD steps only dilute the average.", 375))
    return svg_doc(
        "0 0 800 400",
        "Counting padding steps makes the loss look about half as big without the model learning a single letter",
        "Left panel, bars for the 8 positions of the name uma: the four real steps u, m, a and EOS have surprise 0.6931, 1.3863, 0.2231 and 2.3026, "
        "which sum to 4.6051 and average 1.1513 over 4; the four PAD steps are each 0.0202. Right panel, two bars: padding ignored gives 1.1513 "
        "(tick), padding counted gives 0.5857 (cross), the same model on the same name. Values from Week 12 block 2 by hand and with F.cross_entropy.",
        J(o))


FIGURES = {
    "fig-w10-1-compounding-forty-steps.svg": w10_1,
    "fig-w10-2-gradient-grid-lengths-scales.svg": w10_2,
    "fig-w11-1-rewrite-versus-add.svg": w11_1,
    "fig-w11-2-forget-bias-dial.svg": w11_2,
    "fig-w12-1-shift-right-names.svg": w12_1,
    "fig-w12-2-padding-flatters-loss.svg": w12_2,
}


def emit_b04():
    for name, fn in FIGURES.items():
        open(os.path.join(HERE, name), "w").write(fn() + "\n")
    return len(FIGURES)


if __name__ == "__main__":
    print(emit_b04(), "figures written")

"""Block 4 second-round figures (weeks 10, 11, 12): fig-wNN-4/5/6. Deterministic; no randomness.

Every number drawn is copied from the executed output in that week's student guide, or is a hand
product whose working is printed beside it (STYLE.md 2.1):
  W10-4  block 2 (slopes 0.4340, 0.4839, 0.4960; notes 0.7616 ... 0.0896; product 0.1041; 0.5 ** 40 = 9.1e-13)
  W10-5  block 3 (gradient and 0.9526 ** k at seven positions of the parked 41-note chain)
  W10-6  blank: workbook page 10.2 (notes 0.7616, 0.6420, 0.5663, 0.5126 are given on the page; no slopes drawn)
  W11-4  block 2 (c column, i, g, f = sigmoid(3) = 0.9526, share of step 1)
  W11-5  block 1 (score, dial, dial ** 40)
  W11-6  blank: label the six parts of one LSTM unit (workbook page 11.2)
  W12-4  blocks 1 and 5 (shift-right inputs for anika; the generated name olen)
  W12-5  block 4 (train and validation loss at seven steps)
  W12-6  blank: axes for the page 12.4 table
Called from _gen_build.py through build().
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gen_core import *   # noqa: E402,F401

WIDE = "0 0 800 400"
TIMES, MINUS, ARROW = "&#215;", "&#8722;", "&#8594;"


def title(s):
    return t(400, 46, s, 24, INK, "middle")


def caption(s, y=376):
    return t(400, y, s, 14, MUT, "middle")


def panel(x, y, w, h, stroke=GRID, dash=None):
    return rect(x, y, w, h, 12, PANEL, stroke, 2, dash)


def cell(cx, cy, w, h, label, fill=DATA_F, stroke=DATA_S, sw=2, dash=None, mono=True, size=14, color=INK):
    return "%s\n  %s" % (rect(cx - w / 2.0, cy - h / 2.0, w, h, 6, fill, stroke, sw, dash),
                         t(cx, cy, label, size, color, "middle", mono=mono, central=True))


# ============================================================ W10-4
def w10_4():
    notes = ["0.7616", "0.3634", "0.1797", "0.0896"]     # block 2
    slopes = ["0.4340", "0.4839", "0.4960"]               # block 2: slope into notes 2, 3, 4
    xs = [110, 290, 470, 650]
    o = [title("Slopes multiply along the chain")]
    o.append(t(40, 84, "forward: what the cell does", 14, MUT))
    for i, x in enumerate(xs):
        o.append(rect(x - 55, 96, 110, 52, 8, DATA_F, DATA_S, 2))
        o.append(t(x, 114, "note %d" % (i + 1), 14, INK, "middle"))
        o.append(t(x, 136, notes[i], 14, INK, "middle", mono=True))
        if i < 3:
            o.append(arrow(x + 59, 122, xs[i + 1] - 62, 122, INK, 2))
    o.append(t(40, 190, "backward: how much did the first note matter to this one?", 14, MUT))
    for i, x in enumerate(xs):
        o.append(circ(x, 262, 16, ACC_F if i == 0 else DATA_F, ACC_S if i == 0 else DATA_S, 3 if i == 0 else 2))
        o.append(t(x, 262, str(i + 1), 14, INK, "middle", central=True))
    for i in range(3):
        xm = (xs[i] + xs[i + 1]) / 2.0
        o.append(arrow(xs[i + 1] - 19, 262, xs[i] + 21, 262, ACC_S, 3))
        o.append(chip(xm - 44, 214, 88, TIMES + " " + slopes[i], ACC_S, PAPER, 14))
        o.append(t(xm, 286, "into note %d" % (i + 2), 12, MUT, "middle"))
    o.append(panel(40, 296, 720, 56))
    o.append(t(400, 322, "0.4340 " + TIMES + " 0.4839 " + TIMES + " 0.4960 = 0.1041", 20, INK, "middle", mono=True, central=True))
    o.append(t(400, 342, "Three steps back, about a tenth is left. Forty steps at slope 0.5: 0.5 ** 40 = 9.1e" + MINUS + "13.", 12, MUT, "middle"))
    o.append(caption("The nudge check agreed with the shortcut: 0.4339 against 0.4340.", 376))
    desc = ("Top row: four boxes for Week 8's notes, note 1 = 0.7616, note 2 = 0.3634, note 3 = 0.1797, note 4 = 0.0896, "
            "with arrows pointing right. Bottom row: four numbered circles with arrows pointing left, each carrying the slope into the later note: "
            "times 0.4340 into note 2, times 0.4839 into note 3, times 0.4960 into note 4. A panel states the product, 0.4340 times 0.4839 "
            "times 0.4960 equals 0.1041, and that forty steps at slope 0.5 leave 9.1e-13. Numbers are the printout of block 2 in Week 10.")
    return "fig-w10-4-slopes-multiply-along-a-chain.svg", svg_doc(
        WIDE, "Going back along a loop, the slopes of each step are multiplied together, so the signal shrinks", desc, J(o))


# ============================================================ W10-5
def w10_5():
    pos = [41, 40, 39, 31, 21, 11, 1]
    back = [0, 1, 2, 10, 20, 30, 40]
    meas = ["1.0000", "0.9529", "0.9080", "0.6173", "0.3809", "0.2348", "0.1447"]      # block 3, measured
    theo = ["1.0000", "0.9526", "0.9074", "0.6153", "0.3786", "0.2330", "0.1434"]      # block 3, 0.9526 ** k
    base, unit, x0, gw = 296, 190.0, 112, 94
    o = [title("Parked cell: measured against theory")]
    # legend
    o.append(rect(112, 62, 22, 14, 2, DATA_F, DATA_S, 2))
    o.append(t(140, 69, "measured gradient (block 3)", 12, INK, central=True))
    o.append(rect(372, 62, 22, 14, 2, PAPER, INK, 2, "4 3"))
    o.append(t(400, 69, "theory: 0.9526 ** (steps back)", 12, INK, central=True))
    o.append(line(x0 - 6, base - unit, x0 + 7 * gw, base - unit, GRID, 1.5, "6 4"))
    o.append(t(x0 - 12, base - unit + 4, "1", 12, MUT, "end"))
    o.append(line(x0 - 6, base, x0 + 7 * gw, base, INK, 2))
    for i in range(7):
        gx = x0 + i * gw
        mv, tv = float(meas[i]), float(theo[i])
        last = pos[i] == 1
        o.append(sq(gx + 12, base - mv * unit, 32, mv * unit, ACC_F if last else DATA_F, ACC_S if last else DATA_S, 3 if last else 2))
        o.append(rect(gx + 48, base - tv * unit, 32, tv * unit, 2, PAPER, INK, 2, "4 3"))
        o.append(t(gx + 46, base + 16, "p = %d" % pos[i], 12, INK, "middle"))
        o.append(t(gx + 46, base + 34, "%d back" % back[i], 12, MUT, "middle"))
        o.append(t(gx + 46, base + 54, meas[i], 12, INK, "middle", mono=True))
        o.append(t(gx + 46, base + 72, theo[i], 12, MUT, "middle", mono=True))
    o.append(t(x0 - 12, base + 54, "measured", 12, INK, "end"))
    o.append(t(x0 - 12, base + 72, "theory", 12, MUT, "end"))
    o.append(t(x0 - 12, base + 34, "steps", 12, MUT, "end"))
    o.append(t(x0 - 12, base + 16, "position", 12, MUT, "end"))
    o.append(t(430, 130, "forty steps back (position 1):", 14, ACC_S))
    o.append(t(430, 150, "0.1447 measured, 0.1434 by theory", 14, INK))
    desc = ("Seven pairs of bars for positions 41, 40, 39, 31, 21, 11 and 1 of a 41-note chain whose every slope is 0.9526. "
            "Solid bars are the measured gradient: 1.0000, 0.9529, 0.9080, 0.6173, 0.3809, 0.2348, 0.1447. "
            "Dashed outline bars are 0.9526 to the power of the steps back, 0 to 40: 1.0000, 0.9526, 0.9074, 0.6153, 0.3786, 0.2330, 0.1434. "
            "The pairs match closely and fall from 1 to about 0.14. The last pair is highlighted. Numbers from block 3, Week 10.")
    return "fig-w10-5-parked-cell-measured-vs-theory.svg", svg_doc(
        WIDE, "Even a slope of 0.9526 leaves only 14 percent of the gradient after forty steps, and the measurement matches the arithmetic", desc, J(o))


# ============================================================ W10-6 (blank)
def w10_6():
    notes = ["0.7616", "0.6420", "0.5663", "0.5126"]      # given on workbook page 10.2
    xs = [110, 290, 470, 650]
    o = [title("Page 10.2: fill in the slopes and the product")]
    for i, x in enumerate(xs):
        o.append(rect(x - 55, 80, 110, 52, 8, DATA_F, DATA_S, 2))
        o.append(t(x, 98, "note %d" % (i + 1), 14, INK, "middle"))
        o.append(t(x, 120, notes[i], 14, INK, "middle", mono=True))
    for i in range(3):
        xm = (xs[i] + xs[i + 1]) / 2.0
        o.append(arrow(xs[i + 1] - 56, 160, xs[i] + 56, 160, INK, 2))
        o.append(rect(xm - 46, 176, 92, 40, 6, PAPER, HUMAN_S, 3, "6 4"))
        o.append(t(xm, 232, "slope into note %d" % (i + 2), 12, MUT, "middle"))
    o.append(t(40, 266, "recurrent weight W_hh = 1.0. The slopes multiply from note 1 to note 4:", 14, MUT))
    bx = [130, 280, 430, 590]
    for j in range(4):
        o.append(rect(bx[j], 284, 110 if j < 3 else 130, 44, 6, PAPER, HUMAN_S, 3, "6 4"))
    o.append(t(260, 306, TIMES, 24, INK, "middle", central=True))
    o.append(t(410, 306, TIMES, 24, INK, "middle", central=True))
    o.append(t(565, 306, "=", 24, INK, "middle", central=True))
    o.append(t(40, 306, "note 1 " + ARROW + " 4", 14, INK, central=True))
    o.append(caption("Dashed boxes are for your pencil. Use the new note in each slope.", 366))
    desc = ("A blank worksheet. Four boxes show the notes given on page 10.2: 0.7616, 0.6420, 0.5663 and 0.5126, with arrows pointing left under them. "
            "Under the three arrows are three empty dashed boxes labelled slope into note 2, 3 and 4. At the bottom is an empty product line: "
            "an empty box, a times sign, an empty box, a times sign, an empty box, an equals sign and a last empty box, labelled note 1 to note 4.")
    return "fig-w10-6-blank-slope-chain.svg", svg_doc(
        WIDE, "Blank chain for Week 10 page 10.2: three slopes to find and multiply", desc, J(o))


# ============================================================ W11-4
def w11_4():
    c = ["0.8909", "0.8486", "0.8084", "0.7701"]          # block 2, memory column
    share = ["100.0", "95.3", "90.7", "86.4"]              # block 2, memory as % of step 1
    adds = [("0.9241", "0.9640"), ("0.0759", "0.0000"), ("0.0759", "0.0000"), ("0.0759", "0.0000")]   # block 2: i, g
    xs = [110, 300, 490, 680]
    o = [title("The memory is scaled, then added to")]
    o.append(t(40, 84, "memory track c", 14, MUT))
    for i, x in enumerate(xs):
        o.append(rect(x - 52, 100, 104, 52, 8, DATA_F, DATA_S, 2))
        o.append(t(x, 118, "step %d" % (i + 1), 12, INK, "middle"))
        o.append(t(x, 138, c[i], 14, INK, "middle", mono=True))
        if i < 3:
            o.append(arrow(x + 56, 118, xs[i + 1] - 59, 118, INK, 3))
            o.append(chip(x + 61, 126, 68, TIMES + " 0.9526", MODEL_S, PAPER, 12))
        new = i == 0
        o.append(arrow(x, 210, x, 158, ACC_S if new else MUT, 3 if new else 2, None if new else "6 4"))
        o.append(rect(x - 74, 214, 148, 30, 6, ACC_F if new else PAPER, ACC_S if new else GRID, 3 if new else 2, None if new else "6 4"))
        o.append(t(x, 229, "+ %s " % adds[i][0] + TIMES + " %s" % adds[i][1], 12, INK, "middle", mono=True, central=True))
        o.append(t(x, 262, "i " + TIMES + " g: written" if new else "i " + TIMES + " g: nothing new", 12, ACC_S if new else MUT, "middle", weight="600" if new else None))
        o.append(t(x, 296, share[i] + "% of step 1", 14, INK, "middle"))
    o.append(panel(40, 316, 720, 36))
    o.append(t(400, 334, "f = sigmoid(3) = 0.9526 at every step. The old memory is only multiplied by f.", 12, INK, "middle", central=True))
    o.append(caption("About 5% lost a step: 86.4% left at step 4, against 11.8% for the rewritten note.", 376))
    desc = ("Four boxes in a row for the memory c at steps 1 to 4: 0.8909, 0.8486, 0.8084, 0.7701, joined by arrows each marked times 0.9526. "
            "Under each box an upward arrow brings in what is added: at step 1 plus 0.9241 times 0.9640, marked written and highlighted; "
            "at steps 2 to 4 plus 0.0759 times 0.0000, dashed and marked nothing new. Under each column the share of step 1: 100.0, 95.3, 90.7 and 86.4 percent. "
            "A panel says the forget dial is sigmoid of 3, 0.9526, at every step, and the old memory only passes through that multiplication. Numbers from block 2, Week 11.")
    return "fig-w11-4-memory-scaled-then-added.svg", svg_doc(
        WIDE, "The LSTM memory is multiplied by the forget dial and then a new part is added, so the past survives", desc, J(o))


# ============================================================ W11-5
def w11_5():
    rows = [(-2, "0.1192", "1.126e-37"), (0, "0.5000", "9.095e-13"), (1, "0.7311", "3.615e-06"),
            (2, "0.8808", "6.238e-03"), (3, "0.9526", "1.432e-01"), (4, "0.9820", "4.838e-01")]   # block 1 (4 is 4.838e-01 as printed 4.838e-01)
    x0, sc = 160, 290.0
    o = [title("What a dial leaves after forty steps")]
    o.append(t(150, 96, "score z", 12, MUT, "end"))
    o.append(t(x0, 96, "dial f = sigmoid(z)", 12, MUT))
    o.append(t(458, 96, "f", 12, MUT))
    o.append(t(552, 96, "f ** 40", 12, MUT))
    xt = x0 + 0.95 * sc
    o.append(line(xt, 104, xt, 340, ACC_S, 2, "6 4"))
    o.append(t(xt, 98, "0.95", 12, ACC_S, "middle"))
    o.append(line(x0, 340, x0 + sc, 340, INK, 2))
    for v, lab in ((0, "0"), (0.5, "0.5"), (1.0, "1")):
        o.append(line(x0 + v * sc, 340, x0 + v * sc, 346, INK, 2))
        if lab != "0.95":
            o.append(t(x0 + v * sc, 358, lab, 12, MUT, "middle"))
    for i, (z, f, p) in enumerate(rows):
        y = 110 + i * 38
        keep = float(f) >= 0.95
        o.append(t(150, y + 13, "z = %s" % (str(z).replace("-", MINUS)), 14, INK, "end", central=True))
        o.append(sq(x0, y, float(f) * sc, 26, OK_F if keep else DATA_F, OK_S if keep else DATA_S, 3 if keep else 2))
        o.append(t(458, y + 13, f, 14, INK, mono=True, central=True))
        o.append(t(552, y + 13, p.replace("e-", "e" + MINUS), 14, INK, mono=True, central=True))
        if keep:
            o.append(tick(700, y + 13, 9, OK_S))
            o.append(t(714, y + 13, "keeps", 12, OK_S, central=True))
        else:
            o.append(cross(700, y + 13, 6, BAD_S))
            o.append(t(714, y + 13, "gone", 12, BAD_S, central=True))
    o.append(caption("Only a dial of about 0.95 or more keeps anything. An untrained gate (z = 0) leaves 9e" + MINUS + "13.", 376))
    desc = ("Six horizontal bars of the dial f = sigmoid(z) for scores z = -2, 0, 1, 2, 3 and 4, with a dashed line at 0.95. The dials are 0.1192, 0.5000, 0.7311, 0.8808, 0.9526 and 0.9820. "
            "Beside each, f to the power 40: 1.126e-37, 9.095e-13, 3.615e-06, 6.238e-03, 1.432e-01 and 4.838e-01. The two bars past the line (z = 3 and 4) are green with a tick marked keeps; "
            "the other four carry a cross marked gone. Numbers from block 1, Week 11.")
    return "fig-w11-5-dial-and-forty-steps.svg", svg_doc(
        WIDE, "Forty multiplications by a dial keep something only when the dial is near 1", desc, J(o))


# ============================================================ W11-6 (blank)
def w11_6():
    o = [title("Name the six parts of one LSTM unit")]
    o.append(line(30, 120, 600, 120, INK, 4))
    o.append(head(602, 120, 0, INK, 4))
    o.append(circ(80, 120, 14, PAPER, ACC_S, 3))
    o.append(t(80, 120, "1", 14, INK, "middle", central=True))
    # multiply node on the track + forget box
    o.append(circ(170, 120, 16, PAPER, INK, 3))
    o.append(t(170, 121, TIMES, 20, INK, "middle", central=True))
    o.append(arrow(170, 196, 170, 140, INK, 2))
    o.append(rect(125, 198, 90, 40, 6, PAPER, ACC_S, 3, "6 4"))
    o.append(circ(170, 218, 14, PAPER, ACC_S, 3))
    o.append(t(170, 218, "2", 14, INK, "middle", central=True))
    # add node
    o.append(circ(330, 120, 16, PAPER, INK, 3))
    o.append(t(330, 121, "+", 20, INK, "middle", central=True))
    o.append(circ(330, 82, 14, PAPER, ACC_S, 3))
    o.append(t(330, 82, "5", 14, INK, "middle", central=True))
    o.append(line(330, 96, 330, 104, MUT, 1.5))
    # input dial and candidate feed a multiply node, which feeds the add
    o.append(circ(330, 190, 16, PAPER, INK, 3))
    o.append(t(330, 191, TIMES, 20, INK, "middle", central=True))
    o.append(arrow(330, 172, 330, 140, INK, 2))
    o.append(rect(235, 262, 90, 40, 6, PAPER, ACC_S, 3, "6 4"))
    o.append(circ(280, 282, 14, PAPER, ACC_S, 3))
    o.append(t(280, 282, "3", 14, INK, "middle", central=True))
    o.append(arrow(282, 260, 318, 203, INK, 2))
    o.append(rect(345, 262, 90, 40, 6, PAPER, ACC_S, 3, "6 4"))
    o.append(circ(390, 282, 14, PAPER, ACC_S, 3))
    o.append(t(390, 282, "4", 14, INK, "middle", central=True))
    o.append(arrow(388, 260, 344, 203, INK, 2))
    # read-out
    o.append(circ(480, 120, 4, INK, INK, 2))
    o.append(arrow(480, 126, 480, 176, INK, 2))
    o.append(circ(480, 192, 16, PAPER, INK, 3))
    o.append(t(480, 193, TIMES, 20, INK, "middle", central=True))
    o.append(rect(520, 172, 90, 40, 6, PAPER, ACC_S, 3, "6 4"))
    o.append(circ(565, 192, 14, PAPER, ACC_S, 3))
    o.append(t(565, 192, "6", 14, INK, "middle", central=True))
    o.append(arrow(518, 192, 500, 192, INK, 2))
    o.append(arrow(480, 210, 480, 252, INK, 2))
    o.append(cell(480, 272, 90, 36, "note h", DATA_F, DATA_S, 2, None, False, 14))
    # answer lines
    o.append(t(650, 84, "write the name:", 14, MUT))
    for k in range(6):
        y = 120 + k * 34
        o.append(ring_num(662, y, k + 1))
        o.append(line(682, y + 8, 774, y + 8, INK, 1.5, "4 4"))
    o.append(panel(20, 322, 760, 40))
    o.append(t(400, 342, "Word bank: candidate " + "&#183;" + " forget dial " + "&#183;" + " input dial " + "&#183;" + " memory track " + "&#183;" + " output dial " + "&#183;" + " the add", 14, INK, "middle", central=True))
    o.append(caption("Follow the arrows: what is multiplied, what is added, what is read out.", 376))
    desc = ("A blank diagram of one LSTM unit with six numbered rings and no names. A thick horizontal line with an arrowhead is ring 1. "
            "On it a times node, fed from below by an empty dashed box ringed 2, then a plus node with ring 5 above it. A second times node below the plus node feeds up into it; "
            "it is fed by two empty dashed boxes ringed 3 and 4. Further right a branch leaves the line, passes a times node fed by an empty dashed box ringed 6, and ends in a box labelled note h. "
            "On the right are six dashed answer lines numbered 1 to 6, and a word bank of six terms under the diagram.")
    return "fig-w11-6-blank-label-lstm-unit.svg", svg_doc(
        WIDE, "Blank diagram for Week 11 page 11.2: write the name of each numbered part", desc, J(o))


# ============================================================ W12-4
def w12_4():
    xs = [88 + 80 * i for i in range(6)]
    o = [title("Training knows every input; generating makes each one")]
    o.append(panel(30, 64, 740, 134))
    o.append(t(48, 88, "training (teacher forcing): the true previous letters", 14, INK))
    for i, lab in enumerate(["START", "a", "n", "i", "k", "a"]):    # inputs for anika, block 1
        o.append(cell(xs[i], 122, 52, 38, lab, DATA_F, DATA_S, 2, None, True, 14 if lab != "START" else 12))
    o.append(bracket(xs[0] - 26, xs[-1] + 26, 148, 8, MUT, True))
    o.append(t((xs[0] + xs[-1]) / 2.0, 178, "all in the table before the model runs", 12, MUT, "middle"))
    o.append(t(530, 116, "x[:, t]", 14, INK, mono=True, central=True))
    o.append(t(530, 138, "a column that already exists", 12, MUT))
    o.append(panel(30, 212, 740, 140, ACC_S, "6 4"))
    o.append(t(48, 236, "generating: the model's own last pick", 14, INK))
    for i, lab in enumerate(["START", "o", "l", "e", "n", "EOS"]):    # the generated name olen, block 5
        if i == 0:
            o.append(cell(xs[i], 270, 52, 38, lab, DATA_F, DATA_S, 2, None, True, 12))
        else:
            o.append(cell(xs[i], 270, 52, 38, lab, PAPER, ACC_S, 3, "5 4", True, 14 if lab != "EOS" else 12))
        if i < 5:
            o.append(arrow(xs[i] + 30, 270, xs[i + 1] - 30, 270, INK, 2))
    o.append(t((xs[0] + xs[-1]) / 2.0, 312, "each letter waits for the one before it", 12, MUT, "middle"))
    o.append(t(530, 266, "tok = the pick", 14, INK, mono=True, central=True))
    o.append(t(530, 288, "dashed cells do not exist yet", 12, MUT))
    o.append(caption("The same model step, run both ways. Only where the next input comes from differs.", 376))
    desc = ("Two panels. Top, training: a row of six solid cells for the inputs of the name anika, START a n i k a, all in a table before the model runs, "
            "marked by a bracket and the label x[:, t], a column that already exists. Bottom, generating: a row of six cells for the generated name olen, START then o l e n EOS; "
            "only START is solid, the rest are dashed because each is the model's own pick and does not exist until the model has answered, with arrows from each cell to the next. "
            "Inputs from block 1 and the name olen from block 5, Week 12.")
    return "fig-w12-4-training-versus-generating-inputs.svg", svg_doc(
        WIDE, "In training the next input is already known; in generating it is the model's own previous answer", desc, J(o))


# ============================================================ W12-5
STEPS = [0, 100, 200, 300, 400, 600, 800]
TRAIN = [3.346, 1.960, 1.431, 1.103, 0.984, 0.921, 0.906]      # block 4, dropout off
VAL = [3.349, 2.308, 2.544, 2.880, 3.077, 3.314, 3.417]        # block 4, 31 held-back names


def _axes(o, px, py, ymax=3.6):
    X0, X1, Y0, Y1 = 100, 560, 316, 96
    def x(s): return X0 + (X1 - X0) * s / 800.0
    def y(v): return Y0 - (Y0 - Y1) * v / ymax
    for v in (0, 1, 2, 3):
        o.append(line(X0, y(v), X1, y(v), GRID if v else INK, 1.5 if v else 2))
        o.append(t(X0 - 10, y(v) + 4, str(v), 12, MUT, "end"))
    for s in (0, 200, 400, 600, 800):
        o.append(t(x(s), Y0 + 20, str(s), 12, MUT, "middle"))
    o.append(t((X0 + X1) / 2.0, Y0 + 40, "training steps", 12, MUT, "middle"))
    o.append(trot(40, (Y0 + Y1) / 2.0, "loss (average surprise per real letter)", 12))
    return x, y


def w12_5():
    o = [title("Train keeps falling; validation turns round")]
    x, y = _axes(o, 100, 330)
    ln28 = 3.3322
    o.append(line(100, y(ln28), 560, y(ln28), MUT, 2, "8 5"))
    o.append(t(300, y(ln28) - 6, "ln 28 = 3.332: a model that knows nothing", 12, MUT, "middle"))
    o.append(poly([(x(s), y(v)) for s, v in zip(STEPS, TRAIN)], "none", DATA_S, 3))
    o.append(poly([(x(s), y(v)) for s, v in zip(STEPS, VAL)], "none", HUMAN_S, 3, "8 5"))
    for s, v in zip(STEPS, TRAIN):
        o.append(mark("circle", x(s), y(v), 6, DATA_S, PAPER, 2))
    for s, v in zip(STEPS, VAL):
        o.append(mark("square", x(s), y(v), 6, HUMAN_S, PAPER, 2))
    o.append(circ(x(100), y(2.308), 13, "none", ACC_S, 3))
    # right-hand notes
    o.append(t(580, 134, "validation (31 names)", 14, HUMAN_S))
    o.append(t(580, 154, "step 800: 3.417", 14, INK, mono=True))
    o.append(t(580, 174, "lowest: 2.308 at step 100", 12, ACC_S))
    o.append(t(580, 270, "train (200 names)", 14, DATA_S))
    o.append(t(580, 290, "step 800: 0.906", 14, INK, mono=True))
    o.append(t(580, 310, "from 3.346 at step 0", 12, MUT))
    o.append(caption("At step 800 the gap is 3.417 " + MINUS + " 0.906 = 2.511, and validation sits above 3.332.", 376))
    desc = ("A line chart of loss against training steps 0, 100, 200, 300, 400, 600 and 800. The train line is solid with circles: 3.346, 1.960, 1.431, 1.103, 0.984, 0.921, 0.906. "
            "The validation line is dashed with squares: 3.349, 2.308, 2.544, 2.880, 3.077, 3.314, 3.417. A dashed horizontal line marks ln 28 = 3.332. "
            "Validation is lowest at step 100 (2.308, ringed) and ends above the ln 28 line while train keeps falling. Numbers from block 4, Week 12.")
    return "fig-w12-5-train-and-validation-loss-curves.svg", svg_doc(
        WIDE, "Train loss keeps falling while validation loss turns upward and ends worse than guessing", desc, J(o))


# ============================================================ W12-6 (blank)
def w12_6():
    o = [title("Page 12.4: plot your own table")]
    x, y = _axes(o, 100, 330)
    for s in STEPS[1:]:
        o.append(line(x(s), y(3.6), x(s), y(0), GRID, 1.5, "3 5"))
    for s in STEPS:
        o.append(line(x(s), y(0), x(s), y(0) + 5, INK, 2))
    for s in (100, 300):
        o.append(t(x(s), y(0) + 20, str(s), 12, MUT, "middle"))
    o.append(t(580, 134, "key", 14, INK))
    o.append(poly([(580, 160), (620, 160)], "none", DATA_S, 3))
    o.append(mark("circle", 600, 160, 6, DATA_S, PAPER, 2))
    o.append(t(632, 160, "train", 14, INK, central=True))
    o.append(poly([(580, 190), (620, 190)], "none", HUMAN_S, 3, "8 5"))
    o.append(mark("square", 600, 190, 6, HUMAN_S, PAPER, 2))
    o.append(t(632, 190, "validation", 14, INK, central=True))
    o.append(t(580, 236, "1. Mark 14 points", 14, INK))
    o.append(t(580, 256, "2. Join each series", 14, INK))
    o.append(t(580, 276, "3. Ring the lowest", 14, INK))
    o.append(t(580, 296, "    validation point", 14, INK))
    o.append(caption("Dotted lines are the seven steps of your table. Draw ln 28 as a dashed line.", 376))
    desc = ("A blank chart for the page 12.4 table. The horizontal axis is training steps with ticks at 0, 200, 400, 600 and 800 and dotted vertical lines at 100, 200, 300, 400, 600 and 800; "
            "the vertical axis is loss from 0 to 3 with horizontal grid lines. No data is drawn. A key shows train as a solid line with circles and validation as a dashed line with squares, "
            "and three numbered instructions: mark 14 points, join each series, ring the lowest validation point.")
    return "fig-w12-6-blank-loss-axes.svg", svg_doc(
        WIDE, "Blank axes for Week 12 page 12.4: plot train and validation loss at seven steps", desc, J(o))


def build():
    out = {}
    for fn in (w10_4, w10_5, w10_6, w11_4, w11_5, w11_6, w12_4, w12_5, w12_6):
        name, svg = fn()
        out[name] = svg
    return out


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for name, svg in build().items():
        with open(os.path.join(here, name), "w") as fh:
            fh.write(svg + "\n")
        print("wrote", name)

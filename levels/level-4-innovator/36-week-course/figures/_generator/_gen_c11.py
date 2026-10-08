"""Block C11 (weeks 31, 32, 33) extra figures: a mental-model figure, a worked-numbers figure and a
blank workbook figure per week. Every number is copied from the week's printed output or is a
hand sum printed beside it (STYLE.md 2.1).

W31  student-guide/week-31.md section 5 (p5_pretrain.py: hide 20% of words), section 9-10 (p9_step0.py,
     p10_finetune.py: base 18/30, full 19/30, LoRA 19/30) and section 12 (p12_seeds.py: six seeds, every row
     kept); the blank is workbook page 31.1 (the patch beside one 64 x 64 projection at r = 4), nothing filled in
W32  student-guide/week-32.md section 5 (p2_reliability.py: bucket counts 9 7 6 8 10, top bucket stated 0.931,
     actual 0.700, ECE 0.1788) and section 8 (p5_category.py: per-category table at threshold 0.8; the right
     counts are before-rate x 8 and answered x after-rate, hand sums); the blank is workbook page 32.2
     Part A (the two groups of ten results), nothing plotted
W33  student-guide/week-33.md section 7 (s6_patch.py: A1 15/50 landed, patch 2 -> 0/50, save 50/50),
     section 5 (wobble 3.24) and section 8 (s7_can_we_see_it.py: counts, gaps, noise bounds; all stand-in);
     the blank is workbook page 33.1 (wobble of a count against p at n = 50), nothing plotted
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


def box(x, y, w, h, l1, l2=None, fill=DATA_F, stroke=DATA_S, sw=2, dash=None, mono1=False):
    o = [rect(x, y, w, h, 8, fill, stroke, sw, dash)]
    if l2:
        o.append(t(x + w / 2.0, y + h / 2.0 - 9, l1, 14, INK, "middle", mono=mono1, central=True))
        o.append(t(x + w / 2.0, y + h / 2.0 + 11, l2, 12, MUT, "middle", central=True))
    else:
        o.append(t(x + w / 2.0, y + h / 2.0, l1, 14, INK, "middle", mono=mono1, central=True))
    return "\n  ".join(o)


def blank(x, y, w, h):
    """A write-in box: paper fill, dashed grid outline, nothing inside."""
    return rect(x, y, w, h, 6, PAPER, MUT, 2, "6 4")


# ================================================================ W31-4  the path to a patched model
def w31_4():
    o = [ctitle("From raw text to a patched model")]
    # top row: the order of operations. 1 pretrain once, 2 base = frozen encoder + trained head, 3 two fine-tunes from a copy of the base
    o.append(box(20, 70, 120, 60, "text", "no labels", DATA_F, DATA_S))
    o.append(arrow(142, 100, 166, 100))
    o.append(box(168, 70, 140, 60, "pretrain once", "guess hidden words", MODEL_F, MODEL_S))
    o.append(ring_num(168, 70, 1))
    o.append(arrow(310, 100, 334, 100))
    o.append(box(336, 70, 120, 60, "encoder", "kept as it is", MODEL_F, MODEL_S))
    o.append(arrow(458, 100, 482, 100))
    o.append(box(484, 70, 140, 60, "base model", "head only trains", MODEL_F, MODEL_S))
    o.append(ring_num(484, 70, 2))
    o.append(t(554, 148, "18 of 30 right", 12, INK, "middle"))        # p10_finetune.py: base 18/30
    o.append(arrow(626, 88, 656, 84))
    o.append(arrow(626, 112, 656, 136))
    o.append(box(658, 62, 120, 44, "full fine-tune", "19 of 30 right", MODEL_F, MODEL_S))          # p10: full 19/30
    o.append(box(658, 114, 120, 44, "LoRA patch", "19 of 30 right", MODEL_F, MODEL_S))             # p10: LoRA 19/30
    o.append(ring_num(658, 62, 3))
    o.append(t(778, 176, "each starts from a copy of the base", 12, MUT, "end"))
    # bottom: the patch beside one layer
    o.append(rect(20, 192, 758, 150, 12, PANEL, GRID, 2))
    o.append(t(34, 214, "LoRA: one patch beside one old layer", 14, INK, "start"))
    o.append(box(44, 262, 80, 40, "input x", None, DATA_F, DATA_S))
    o.append(arrow(126, 276, 218, 246))
    o.append(arrow(126, 288, 218, 304))
    o.append(box(220, 228, 190, 44, "old layer", "frozen: does not move", MODEL_F, MODEL_S))
    o.append(box(220, 288, 96, 44, "A", "thin grid", MODEL_F, MODEL_S))
    o.append(arrow(318, 310, 352, 310))
    o.append(box(354, 288, 110, 44, "B", "thin grid, starts at 0", MODEL_F, MODEL_S))
    o.append(rect(212, 280, 262, 58, 10, "none", MODEL_S, 2, "6 4"))
    o.append(t(496, 332, "the patch, times a scale", 12, MUT, "start"))
    o.append(line(412, 250, 600, 250, INK, 3))
    o.append(arrow(600, 250, 600, 268, INK, 3))
    o.append(line(476, 310, 600, 310, INK, 3))
    o.append(arrow(600, 310, 600, 294, INK, 3))
    o.append(circ(600, 281, 14, PAPER, INK, 3))
    o.append(t(600, 281, "+", 18, INK, "middle", central=True))
    o.append(arrow(616, 281, 660, 281))
    o.append(box(662, 258, 100, 46, "layer output", "old + patch", ACC_F, ACC_S, 3))
    o.append(cap("Pretrain once, build a base, adjust a copy; at step 0 the zero patch adds nothing.", 366))
    fig("fig-w31-4-pretrain-base-patch.svg", "0 0 800 400",
        "Pretrain once, build a base model, then fine-tune a copy of it fully or with a LoRA patch whose output is added to a frozen layer",
        "Top row, left to right: unlabelled text, then step 1 pretrain once by guessing hidden words, giving an encoder kept as it is, then step 2 a base model "
        "where only the head trains, which gets 18 of 30 right. From the base two arrows lead to step 3: a full fine-tune and a LoRA patch, each 19 of 30 right, "
        "each starting from a copy of the base. Bottom panel: the input x goes two ways. One way through an old frozen layer. The other way through a dashed patch "
        "of two thin grids, A then B, where B starts at 0, times a scale. The two results are added by a plus sign to give the layer output.", o)


# ================================================================ W31-5  six seeds, every row kept
def w31_5():
    # p12_seeds.py printed table: seed, base, full, lora, regressions base -> lora
    SEEDS = [(0, 18, 19, 19, "billing -0.2"),
             (1, 15, 18, 19, "none flagged"),
             (2, 18, 19, 18, "greeting -0.17, billing -0.2"),
             (3, 16, 19, 19, "billing -0.2"),
             (4, 17, 19, 18, "refund -0.14"),
             (5, 17, 20, 18, "out_of_scope -0.2")]
    o = [ctitle("Six seeds, every row kept")]
    ax = lambda v: 140 + (v - 15) * 44.0               # 15 -> 140, 20 -> 360 tickets of 30
    yr = lambda i: 128 + i * 34
    # legend
    o.append(mark("circle", 40, 76, 5, DATA_S, PAPER, 2))
    o.append(t(52, 80, "base", 12, INK, "start"))
    o.append(mark("square", 108, 76, 5, HUMAN_S, PAPER, 2))
    o.append(t(120, 80, "full fine-tune", 12, INK, "start"))
    o.append(mark("triangle", 234, 76, 5, MODEL_S, PAPER, 2))
    o.append(t(246, 80, "LoRA", 12, INK, "start"))
    o.append(t(300, 80, "tickets right, of 30", 12, MUT, "start"))
    # column heads
    o.append(t(400, 104, "base", 12, MUT, "middle"))
    o.append(t(440, 104, "full", 12, MUT, "middle"))
    o.append(t(480, 104, "LoRA", 12, MUT, "middle"))
    o.append(t(520, 104, "categories that fell, base to LoRA", 12, MUT, "start"))
    for v in range(15, 21):
        o.append(line(ax(v), 110, ax(v), 318, GRID, 1.5, "6 4"))
        o.append(t(ax(v), 338, str(v), 12, MUT, "middle"))
    o.append(line(140, 318, 360, 318, INK, 2))
    for i, (s, b, f, l, flag) in enumerate(SEEDS):
        y = yr(i)
        o.append(t(100, y + 4, "seed %d" % s, 12, INK, "end"))
        o.append(mark("circle", ax(b), y - 9, 5, DATA_S, PAPER, 2))
        o.append(mark("square", ax(f), y, 5, HUMAN_S, PAPER, 2))
        o.append(mark("triangle", ax(l), y + 9, 5, MODEL_S, PAPER, 2))
        for x, v in ((400, b), (440, f), (480, l)):
            o.append(t(x, y + 4, str(v), 12, INK, "middle"))
        o.append(t(520, y + 4, flag, 12, INK if flag != "none flagged" else MUT, "start"))
    o.append(rect(504, 322, 268, 30, 6, ACC_F, ACC_S, 3))
    o.append(t(638, 337, "5 of 6 seeds flag something", 14, INK, "middle", central=True))
    o.append(cap("Base 15 to 18, full 18 to 20, LoRA 18 to 19 tickets of 30: the spread is the result.", 374))
    fig("fig-w31-5-six-seeds-every-row.svg", "0 0 800 400",
        "Across six seeds each method moves by a few tickets and a different category falls each time",
        "A dot chart of tickets right out of 30 on the 15 to 20 axis, one row per seed 0 to 5, with a circle for base, a square for full fine-tuning and a "
        "triangle for LoRA, and the numbers printed to the right. Base: 18, 15, 18, 16, 17, 17. Full: 19, 18, 19, 19, 19, 20. LoRA: 19, 19, 18, 19, 18, 18. "
        "The categories that fell from base to LoRA by seed: billing minus 0.2; none; greeting minus 0.17 and billing minus 0.2; billing minus 0.2; refund "
        "minus 0.14; out of scope minus 0.2. A callout says 5 of 6 seeds flag something.", o)


# ================================================================ W31-6  blank: label the patch
def w31_6():
    o = [ctitle("Label the patch")]
    o.append(box(20, 176, 76, 38, "input x", None, DATA_F, DATA_S))
    o.append(arrow(98, 188, 128, 124))
    o.append(arrow(98, 204, 128, 266))
    o.append(box(130, 84, 190, 56, "old projection", "64 in, 64 out", MODEL_F, MODEL_S))
    o.append(line(322, 112, 386, 112, INK, 3))
    o.append(arrow(386, 112, 386, 174, INK, 3))
    o.append(rect(118, 228, 262, 104, 10, "none", MODEL_S, 2, "6 4"))
    o.append(box(130, 238, 100, 56, "A", "rank r = 4", MODEL_F, MODEL_S))
    o.append(arrow(232, 266, 258, 266))
    o.append(box(260, 238, 100, 56, "B", "rank r = 4", MODEL_F, MODEL_S))
    o.append(t(250, 348, "the patch, then times a scale", 12, MUT, "middle"))
    o.append(line(362, 266, 386, 266, INK, 3))
    o.append(arrow(386, 266, 386, 206, INK, 3))
    o.append(circ(386, 190, 14, PAPER, INK, 3))
    o.append(t(386, 190, "+", 18, INK, "middle", central=True))
    o.append(ring_num(130, 84, 1))
    o.append(ring_num(130, 238, 2))
    o.append(ring_num(260, 238, 3))
    o.append(ring_num(245, 312, 4))
    o.append(ring_num(118, 332, 5))
    o.append(ring_num(320, 140, 6))
    # questions
    o.append(rect(420, 66, 358, 280, 12, PANEL, GRID, 2))
    Q = ["old layer: frozen or trainable?",
         "shape of A (rows, columns)",
         "shape of B (rows, columns)",
         "which starts at exactly 0, A or B?",
         "numbers stored in the whole patch",
         "numbers in the old projection"]
    for i, q in enumerate(Q):
        y = 98 + i * 44
        o.append(ring_num(442, y, i + 1))
        o.append(t(460, y + 4, q, 12, INK, "start"))
        o.append(blank(690, y - 15, 84, 30))
    o.append(cap("Write in the boxes, then check against the ANSWERS page.", 372))
    fig("fig-w31-6-blank-label-the-patch.svg", "0 0 800 400",
        "Blank: label a rank-4 LoRA patch beside a 64 by 64 projection",
        "A diagram with the input x going two ways. One way into a box 'old projection, 64 in, 64 out' (ringed 1, and ringed 6 for its count). The other way "
        "through a dashed patch holding box A (ringed 2) and box B (ringed 3), both rank r = 4, with a ringed 4 between them and a ringed 5 on the patch outline. "
        "Both ways are added at a plus sign. On the right six numbered questions each have an empty write-in box: frozen or trainable, shape of A, shape of B, "
        "which starts at 0, numbers stored in the patch, numbers in the old projection. Nothing is filled in.", o)


# ================================================================ W32-4  stated, delivered, gap, weight
def w32_4():
    # p2_reliability.py: bucket counts 9 7 6 8 10; top bucket stated 0.931 actual 0.700; ECE 0.1788
    COUNTS = [9, 7, 6, 8, 10]
    o = [ctitle("Calibration: sort by what it said, then compare")]
    # step 1: the 40 results and the bucket strip
    o.append(box(20, 80, 140, 64, "40 results", "said p, right/wrong", DATA_F, DATA_S))
    o.append(ring_num(32, 80, 1))
    o.append(arrow(162, 112, 200, 112))
    o.append(t(214, 74, "sorted into five buckets by what it said, n per bucket", 12, MUT, "start"))
    for i, c in enumerate(COUNTS):
        x = 214 + i * 70
        top = i == 4
        o.append(sq(x, 82, 70, 58, ACC_F if top else DATA_F, ACC_S if top else DATA_S, 4 if top else 2))
        o.append(t(x + 35, 111, str(c), 20, INK, "middle", central=True))
    for j, e in enumerate(["0.6", "0.7", "0.8", "0.9"]):
        o.append(t(284 + j * 70, 158, e, 12, MUT, "middle"))
    o.append(t(214, 176, "said less", 12, MUT, "start"))
    o.append(t(564, 176, "said more", 12, MUT, "end"))
    # step 2: one bucket zoomed
    o.append(line(529, 142, 640, 194, ACC_S, 2, "6 4"))
    o.append(rect(590, 170, 190, 160, 12, PANEL, ACC_S, 3))
    o.append(ring_num(590, 170, 2))
    o.append(t(685, 192, "the top bucket, 10 results", 12, INK, "middle"))
    yb, h = 306, 84
    o.append(line(612, yb, 764, yb, INK, 2))
    o.append(rect(622, yb - h * 0.931, 44, h * 0.931, 2, PANEL, DATA_S, 2, "4 3"))
    o.append(rect(706, yb - h * 0.700, 44, h * 0.700, 2, OK_F, OK_S, 2))
    o.append(t(644, yb - h * 0.931 - 6, "0.931", 12, INK, "middle"))
    o.append(t(728, yb - h * 0.700 - 6, "0.700", 12, INK, "middle"))
    o.append(t(644, yb + 16, "said", 12, MUT, "middle"))
    o.append(t(728, yb + 16, "delivered", 12, MUT, "middle"))
    o.append(line(660, yb - h * 0.931, 700, yb - h * 0.931, MUT, 1.5, "4 3"))
    o.append(line(700, yb - h * 0.931, 700, yb - h * 0.700, ACC_S, 3))
    o.append(t(696, yb - h * 0.8, "gap", 12, ACC_S, "end"))
    # steps in words, in the order they happen
    o.append(box(20, 196, 168, 54, "1  sort", "by what it said", DATA_F, DATA_S))
    o.append(arrow(190, 223, 210, 223))
    o.append(box(212, 196, 168, 54, "2  compare", "said against delivered", DATA_F, DATA_S))
    o.append(arrow(382, 223, 402, 223))
    o.append(box(404, 196, 168, 54, "3  weight and add", "bigger bucket, more say", ACC_F, ACC_S, 3))
    o.append(rect(20, 272, 552, 58, 10, PANEL, GRID, 2))
    o.append(t(296, 292, "ECE: the average size of the gap, each bucket counted by its size.", 12, INK, "middle"))
    o.append(t(296, 314, "Here 0.1788: not the share it gets wrong, which is 42.5%.", 12, MUT, "middle"))
    o.append(cap("Sort first, compare second, weight third: the order matters.", 372))
    fig("fig-w32-4-sort-compare-weight.svg", "0 0 800 400",
        "ECE sorts results into buckets by stated confidence, compares said with delivered in each, then weights each gap by the bucket size",
        "Top left, the 40 results, each a stated confidence and a right or wrong. An arrow leads to a strip of five buckets split at 0.6, 0.7, 0.8 and 0.9, "
        "holding 9, 7, 6, 8 and 10 results; the top bucket is outlined. A zoom of that bucket shows a dashed bar for what it said, 0.931, beside a solid bar "
        "for what it delivered, 0.700, with the gap marked between their tops. Three boxes in order read: 1 sort by what it said, 2 compare said against "
        "delivered, 3 weight and add, bigger bucket more say. A panel says ECE here is 0.1788, not the share it gets wrong, which is 42.5 percent.", o)


# ================================================================ W32-5  per-category, before and after
def w32_5():
    # p5_category.py (threshold 0.8): name, right before of 8, answered, right of the answered. before = rate x 8, right of answered = answered x after-rate
    ROWS = [("greeting", 7, 8, 6, 6), ("refund", 5, 8, 3, 3), ("technical", 4, 8, 1, 1),
            ("billing", 4, 8, 6, 2), ("out_of_scope", 3, 8, 2, 1)]
    o = [ctitle("Did every category get better at 0.8?")]
    x0, x1 = 170, 500
    X = lambda v: x0 + v * (x1 - x0)
    o.append(t(X(0), 82, "0", 12, MUT, "middle"))
    o.append(t(X(1), 82, "1.0", 12, MUT, "middle"))
    o.append(t(556, 82, "right before", 12, MUT, "middle"))
    o.append(t(646, 82, "right after", 12, MUT, "middle"))
    o.append(t(726, 82, "answered", 12, MUT, "middle"))
    o.append(line(X(0), 90, X(0), 330, INK, 2))
    o.append(line(X(1), 90, X(1), 330, GRID, 1.5, "6 4"))
    for i, (name, rb, nb, na, ra) in enumerate(ROWS):
        y = 118 + i * 48
        fell = ra / na < rb / nb
        o.append(t(30, y + 6, name, 14, INK, "start"))
        o.append(rect(X(0), y - 16, X(rb / nb) - X(0), 14, 2, PANEL, DATA_S, 2, "4 3"))
        o.append(rect(X(0), y + 2, X(ra / na) - X(0), 14, 2, BAD_F if fell else DATA_F, BAD_S if fell else DATA_S, 2))
        o.append(t(556, y + 4, "%d of %d" % (rb, nb), 12, INK, "middle"))
        o.append(t(646, y + 4, "%d of %d" % (ra, na), 12, INK, "middle"))
        few = na <= 3
        o.append(t(726, y + 4, str(na), 12, MUT if few else INK, "middle"))
        if fell:
            o.append(cross(604, y, 6))
            o.append(rect(24, y - 25, 740, 50, 8, "none", BAD_S, 3))
        if few:
            o.append(t(742, y + 4, "few", 12, MUT, "start"))
    o.append(t(X(0) + 4, 346, "dashed bar: before    solid bar: right share of the answered    cross and red: fell", 12, MUT, "start"))
    o.append(cap("Overall 0.575 to 0.722, yet billing fell from 4 of 8 to 2 of 6; small rows are not readable.", 372))
    fig("fig-w32-5-category-before-after.svg", "0 0 800 400",
        "At threshold 0.8 the average rose but billing fell, and three rows rest on three or fewer answers",
        "Five rows of paired bars for 40 invented results, a dashed bar for the share right before and a solid bar for the share of the answered that are right after. "
        "Greeting 7 of 8 then 6 of 6 with 6 answered. Refund 5 of 8 then 3 of 3 with 3 answered, marked few. Technical 4 of 8 then 1 of 1 with 1 answered, marked few. "
        "Billing 4 of 8 then 2 of 6 with 6 answered, outlined in red with a cross as the row that fell. Out of scope 3 of 8 then 1 of 2 with 2 answered, marked few.", o)


# ================================================================ W32-6  blank: plot the two groups
def w32_6():
    o = [ctitle("Plot the two groups of Set A")]
    S = 260.0
    px0, pyb = 90, 320
    X = lambda v: px0 + v * S
    Y = lambda v: pyb - v * S
    for v in [i / 10.0 for i in range(0, 11)]:
        o.append(line(X(v), pyb, X(v), Y(1), GRID, 1, "2 4"))
        o.append(line(px0, Y(v), X(1), Y(v), GRID, 1, "2 4"))
    o.append(line(px0, pyb, X(1), pyb, INK, 2))
    o.append(line(px0, pyb, px0, Y(1), INK, 2))
    for v, lab in ((0, "0"), (0.5, "0.5"), (1, "1")):
        o.append(t(X(v), pyb + 18, lab, 12, MUT, "middle"))
        o.append(t(px0 - 8, Y(v) + 4, lab, 12, MUT, "end"))
    o.append(t(X(0.5), pyb + 38, "stated (mean said)", 12, MUT, "middle"))
    o.append(trot(40, (pyb + Y(1)) / 2.0, "actual (share right)", 12))
    o.append(line(X(0), Y(0), X(1), Y(1), MODEL_S, 2.5, "8 5"))
    o.append(t(X(0.62), Y(0.62) - 12, "calibrated: said = delivered", 12, MODEL_S, "end", extra='transform="rotate(-45 %s %s)"' % (f2(X(0.62)), f2(Y(0.62) - 12))))
    # right panel: what to do, with write-in boxes
    o.append(rect(410, 66, 366, 280, 12, PANEL, GRID, 2))
    o.append(mark("circle", 436, 100, 7, DATA_S, PAPER, 2))
    o.append(t(452, 104, "sure group (p at least 0.8): draw a circle", 12, INK, "start"))
    o.append(mark("square", 436, 134, 7, HUMAN_S, PAPER, 2))
    o.append(t(452, 138, "unsure group (p below 0.8): draw a square", 12, INK, "start"))
    o.append(t(430, 170, "From each point, draw an arrow straight up", 12, INK, "start"))
    o.append(t(430, 188, "or down to the dashed line: its length is the gap.", 12, INK, "start"))
    o.append(t(430, 232, "Both points lie (above / below) the line:", 12, INK, "start"))
    o.append(blank(690, 216, 80, 28))
    o.append(t(430, 272, "So it said (more / less) than it delivered:", 12, INK, "start"))
    o.append(blank(690, 256, 80, 28))
    o.append(t(430, 312, "Length of the longer arrow:", 12, INK, "start"))
    o.append(blank(690, 296, 80, 28))
    o.append(cap("Fill the table on Page 32.2 first, then plot; check against the ANSWERS page.", 372))
    fig("fig-w32-6-blank-plot-two-groups.svg", "0 0 800 400",
        "Blank: plot the sure and unsure groups of Set A as stated against actual and draw each gap to the calibrated line",
        "An empty square plot with stated on the horizontal axis and actual on the vertical axis, both from 0 to 1 with a faint grid, and a dashed diagonal "
        "line labelled calibrated, said equals delivered. No points are drawn. On the right, instructions to draw a circle for the sure group and a square for "
        "the unsure group, and an arrow from each to the diagonal. Three empty write-in boxes ask: above or below the line, more or less than it delivered, "
        "and the length of the longer arrow.", o)


# ================================================================ W33-4  the red-team loop
def w33_4():
    o = [ctitle("A finding is attack, evidence, fix, two re-tests")]
    NAMES = [("Attack", "try to break it"), ("Evidence", "a count out of n"), ("Mechanism", "why no fence held"),
             ("Fix", "smallest change"), ("Re-test", "twice"), ("Residual risk", "what is left")]
    for i, (a, b) in enumerate(NAMES):
        x = 20 + i * 128
        hl = i == 4
        o.append(box(x, 70, 112, 56, a, b, ACC_F if hl else HUMAN_F, ACC_S if hl else HUMAN_S, 3 if hl else 2))
        o.append(ring_num(x + 12, 70, i + 1))
        if i < 5:
            o.append(arrow(x + 114, 98, x + 126, 98, INK, 3))
    # detail panel: everything counted here comes from the scripted agent
    o.append(stand_in_frame(24, 176, 752, 150, 400, 176))
    o.append(arrow(204, 128, 204, 192, MUT, 2))
    o.append(arrow(588, 128, 588, 192, MUT, 2))
    o.append(rect(40, 198, 300, 112, 10, PAPER, DATA_S, 2))
    o.append(t(190, 218, "Evidence: attack A1, seeds 0 to 49", 12, MUT, "middle"))
    o.append(t(190, 256, "15 / 50 landed", 24, INK, "middle"))
    o.append(t(190, 286, "share 0.30, wobble 3.24 counts", 12, MUT, "middle"))
    o.append(rect(380, 198, 380, 112, 10, PAPER, ACC_S, 3))
    o.append(t(570, 218, "Re-test twice: patch 2, named files only", 12, MUT, "middle"))
    o.append(rect(396, 232, 168, 62, 8, OK_F, OK_S, 2))
    o.append(t(480, 252, "the attack", 12, MUT, "middle"))
    o.append(t(480, 276, "0 / 50 landed", 14, INK, "middle"))
    o.append(rect(576, 232, 168, 62, 8, OK_F, OK_S, 2))
    o.append(t(660, 252, "the real task", 12, MUT, "middle"))
    o.append(t(660, 276, "save worked 50 / 50", 14, INK, "middle"))
    o.append(tick(552, 244, 6))
    o.append(tick(732, 244, 6))
    o.append(cap("A fix lowers the attack count and keeps the real task working; then write down what is left.", 372))
    fig("fig-w33-4-red-team-finding.svg", "0 0 800 400",
        "A red-team finding has six parts in order, and the fix is re-tested twice: against the attack and against the real task",
        "A row of six numbered boxes joined by arrows: attack, evidence, mechanism, fix, re-test twice (highlighted), residual risk. Below, inside a dashed frame "
        "marked stand-in, not a model, two panels. Under evidence: attack A1 over seeds 0 to 49 landed 15 of 50 times, share 0.30, wobble 3.24 counts. Under "
        "re-test: for patch 2, named files only, the attack landed 0 of 50 and the real save worked 50 of 50, each marked with a tick.", o)


# ================================================================ W33-5  can n runs see the gap?
def w33_5():
    # s7_can_we_see_it.py printed table (stand-in): (n, count A, count B, gap, 2 x combined wobble, visible)
    P1 = [(20, 14, 7, 7, 5.9, True), (50, 34, 15, 19, 9.2, True), (200, 133, 68, 65, 18.9, True), (1000, 627, 300, 327, 42.1, True)]
    P2 = [(20, 7, 5, 2, 5.8, False), (50, 15, 10, 5, 8.6, False), (200, 62, 54, 8, 18.1, False), (1000, 310, 225, 85, 39.4, True)]
    o = [ctitle("Can n runs see the gap?")]
    o.append(chip(314, 56, 172, STAND_IN, MODEL_S, PANEL, 12, 26, mono=False))
    for pi, (px, head_, rows) in enumerate(((20, "big gap: p 0.6 against 0.3", P1), (412, "small gap: p 0.30 against 0.24", P2))):
        o.append(rect(px, 94, 366, 252, 12, PANEL, GRID, 2))
        o.append(t(px + 183, 116, head_, 14, INK, "middle"))
        bx = lambda v, px=px: px + 122 + math.log10(v) * 66.0
        for d in (1, 10, 100, 1000):
            o.append(line(bx(d), 128, bx(d), 328, GRID, 1.5, "6 4"))
            o.append(t(bx(d), 340, str(d), 12, MUT, "middle"))
        for i, (n, a, b, gap, bound, vis) in enumerate(rows):
            y = 142 + i * 48
            o.append(t(px + 14, y + 8, "n %d" % n, 12, INK, "start"))
            o.append(t(px + 14, y + 26, "%d vs %d" % (a, b), 12, MUT, "start"))
            o.append(rect(bx(1), y, bx(gap) - bx(1), 14, 2, OK_F if vis else BAD_F, OK_S if vis else BAD_S, 2))
            o.append(line(bx(bound), y - 5, bx(bound), y + 19, INK, 3))
            o.append(t(bx(1) + 4, y + 34, "gap %d, bound %s" % (gap, bound), 12, INK, "start"))
            if vis:
                o.append(tick(px + 352, y + 9, 8))
            else:
                o.append(cross(px + 352, y + 9, 7))
    o.append(t(400, 360, "bar: gap in counts (log scale)    black line: twice the combined wobble    tick: more than noise", 12, MUT, "middle"))
    fig("fig-w33-5-can-runs-see-the-gap.svg", "0 0 800 400",
        "A gap is visible only when its bar passes the noise line, and a small gap needs about a thousand runs",
        "Two panels, counts from the stand-in on a log scale. Each row shows the gap in counts as a bar and twice the combined wobble as a black line. Big gap, "
        "0.6 against 0.3: n 20 gap 7 against 5.9, n 50 gap 19 against 9.2, n 200 gap 65 against 18.9, n 1000 gap 327 against 42.1, all ticked as more than noise. "
        "Small gap, 0.30 against 0.24: n 20 gap 2 against 5.8, n 50 gap 5 against 8.6, n 200 gap 8 against 18.1, each crossed as not distinguishable, and n 1000 "
        "gap 85 against 39.4, ticked.", o)


# ================================================================ W33-6  blank: the wobble curve
def w33_6():
    o = [ctitle("Draw the wobble curve, n = 50")]
    px0, pyb = 90, 320
    W, H = 300.0, 240.0
    X = lambda p: px0 + p * W
    Y = lambda v: pyb - v / 4.0 * H
    for p in (0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0):
        o.append(line(X(p), pyb, X(p), Y(4), GRID, 1.5, "2 4"))
        o.append(t(X(p), pyb + 18, "%g" % p, 12, MUT, "middle"))
    for v in (0, 1, 2, 3, 4):
        o.append(line(px0, Y(v), X(1), Y(v), GRID, 1, "2 4"))
        o.append(t(px0 - 8, Y(v) + 4, str(v), 12, MUT, "end"))
    o.append(line(px0, pyb, X(1), pyb, INK, 2))
    o.append(line(px0, pyb, px0, Y(4), INK, 2))
    o.append(t(X(0.5), pyb + 38, "p, the chance one run lands", 12, MUT, "middle"))
    o.append(trot(40, (pyb + Y(4)) / 2.0, "wobble of the count", 12))
    # right panel: one blank box per p and two questions
    o.append(rect(430, 66, 346, 282, 12, PANEL, GRID, 2))
    o.append(t(446, 90, "Use the four steps of Page 33.1 for n = 50.", 12, INK, "start"))
    o.append(t(446, 112, "Work each one, then plot a dot above its p.", 12, MUT, "start"))
    for i, p in enumerate((0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0)):
        y = 136 + i * 26
        o.append(t(446, y + 5, "p = %g" % p, 12, INK, "start"))
        o.append(blank(520, y - 10, 70, 22))
    o.append(t(618, 150, "Join the dots.", 12, INK, "start"))
    o.append(t(618, 190, "Highest dot at p =", 12, INK, "start"))
    o.append(blank(618, 198, 70, 22))
    o.append(t(618, 244, "Wobble at p = 0", 12, INK, "start"))
    o.append(t(618, 262, "and at p = 1:", 12, INK, "start"))
    o.append(blank(618, 270, 70, 22))
    o.append(cap("Fill the boxes first, then plot; check against the ANSWERS page.", 372))
    fig("fig-w33-6-blank-wobble-curve.svg", "0 0 800 400",
        "Blank: plot the wobble of a count of 50 runs against p and find where it is largest",
        "An empty plot with p from 0 to 1 on the horizontal axis, marked at 0, 0.1, 0.3, 0.5, 0.7, 0.9 and 1, and the wobble of the count from 0 to 4 on the vertical "
        "axis. No dots are drawn. On the right, seven empty boxes, one for each p, to work out the square root of 50 times p times 1 minus p, and two empty boxes "
        "asking where the highest dot is and what the wobble is at p equal to 0 and to 1.", o)


def build():
    for f in (w31_4, w31_5, w31_6, w32_4, w32_5, w32_6, w33_4, w33_5, w33_6):
        f()
    return FIGS

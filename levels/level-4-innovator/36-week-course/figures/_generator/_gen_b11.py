"""Block 11 concept figures: weeks 31, 32, 33 (two each). Every number printed here is copied from the
week's executed, seeded output in student-guide/week-NN.md (the section is named in each docstring).
Week 32's sheet is INVENTED by the teacher; its figures say so. Week 33's backend is a stand-in."""
import os
from _gen_core import *

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # figures/
W = "0 0 800 400"
MIN = "&#8722;"


def title(s):
    return t(400, 44, s, 24, INK, "middle")


def caption(s, y=376):
    return t(400, y, s, 14, MUT, "middle")


def wrap(*parts):
    return "\n  ".join(parts)


# ---------------------------------------------------------------- W31-1
def f31_1():
    """Week 31 section 7: column (1,2,0,-1) x row (2,1,0,3) -> 16 cells from 8 numbers; 4096 vs 512 (0.1250)."""
    col, row = [1, 2, 0, -1], [2, 1, 0, 3]
    P = [title("A thin column times a thin row builds a grid")]
    c = 46
    gx, gy = 150, 150
    # connectors none; row boxes (model: the thin factors), column boxes, grid (data)
    for j, v in enumerate(row):
        P.append(sq(gx + j * c, 98, c, c, MODEL_F, MODEL_S, 2))
        P.append(t(gx + j * c + c / 2, 98 + c / 2, str(v), 14, INK, "middle", central=True))
    for i, v in enumerate(col):
        P.append(sq(gx - c - 14, gy + i * c, c, c, MODEL_F, MODEL_S, 2))
        P.append(t(gx - c - 14 + c / 2, gy + i * c + c / 2, str(v).replace("-", MIN), 14, INK, "middle", central=True))
    for i in range(4):
        for j in range(4):
            v = col[i] * row[j]
            P.append(sq(gx + j * c, gy + i * c, c, c, DATA_F, DATA_S, 2))
            P.append(t(gx + j * c + c / 2, gy + i * c + c / 2, str(v).replace("-", MIN), 14, INK, "middle", central=True))
    P.append(t(gx + 2 * c, 84, "row of 4", 14, INK, "middle"))
    P.append(shape_chip(gx + 4 * c + 8, 108, "(1, 4)", MODEL_S))
    P.append(t(gx - 14, gy - 8, "column of 4", 14, INK, "end"))
    P.append(shape_chip(gx - c - 14 + c / 2 - 28, gy + 4 * c + 8, "(4, 1)", MODEL_S))
    P.append(shape_chip(gx + 4 * c + 8, gy + 2 * c - 13, "(4, 4)", DATA_S))
    P.append(t(gx + 2 * c + 50, gy + 4 * c + 26, "16 cells, built from 8 numbers", 14, INK, "middle"))
    # right panel: counts
    rx = 470
    P.append(t(rx, 92, "64 &#215; 64 projection vs patch", 18, INK))
    P.append(rect(rx, 120, 300, 34, 8, DATA_F, DATA_S, 3))
    P.append(t(rx + 150, 137, "4,096 numbers stored in full", 14, INK, "middle", central=True))
    pw = 300 * 512 / 4096.0
    P.append(rect(rx, 176, pw, 34, 8, MODEL_F, MODEL_S, 3))
    P.append(t(rx + pw + 10, 193, "512 numbers in the rank-4 patch", 14, INK, central=True))
    P.append(t(rx, 244, "512 = 4 &#215; 64 + 64 &#215; 4 = 256 + 256", 14, INK))
    P.append(shape_chip(rx, 258, "A (4, 64)", MODEL_S))
    P.append(shape_chip(rx + 100, 258, "B (64, 4)", MODEL_S))
    P.append(rect(rx, 300, 300, 36, 8, ACC_F, ACC_S, 3))
    P.append(t(rx + 150, 318, "512 &#247; 4096 = 0.1250 of the projection", 14, INK, "middle", central=True))
    P.append(caption("A patch of two thin grids is a small share of the big grid."))
    return svg_doc(W, "A big grid can be a thin column times a thin row, so a patch is a small share of the weights",
                   "Left: a column of four numbers 1, 2, 0, minus 1 beside a row of four numbers 2, 1, 0, 3. Their products fill a "
                   "4 by 4 grid whose rows are 2 1 0 3, 4 2 0 6, 0 0 0 0, and minus 2, minus 1, 0, minus 3: 16 cells from 8 numbers. "
                   "Right: one 64 by 64 projection stores 4,096 numbers; a rank-4 patch of A (4 by 64) and B (64 by 4) stores 512, "
                   "which is 0.1250 of it.", wrap(*P))


# ---------------------------------------------------------------- W31-2
def f31_2():
    """Week 31 section 11: Week 30 compare table, base -> LoRA (seed 0)."""
    rows = [("greeting", 6, 0.833, 0.833, "+0.000", 0), ("refund", 7, 1.000, 1.000, "+0.000", 0),
            ("technical", 7, 0.286, 0.571, "+0.286", 1), ("billing", 5, 0.400, 0.200, MIN + "0.200", -1),
            ("out_of_scope", 5, 0.400, 0.400, "+0.000", 0), ("OVERALL", 30, 0.600, 0.633, "+0.033", 0)]
    P = [title("The average rose; one row fell")]
    P.append(t(190, 94, "before (base model)", 14, INK))
    P.append(t(440, 94, "after (LoRA model)", 14, INK))
    P.append(t(690, 94, "delta", 14, INK))
    bw = 160
    for k, (name, n, b, a, d, flag) in enumerate(rows):
        y = 108 + k * 38
        if flag == -1:
            P.append(rect(26, y - 4, 748, 34, 8, "none", BAD_S, 3))
        wt = "600" if name == "OVERALL" else None
        P.append(t(40, y + 14, "%s  n=%d" % (name, n), 14, INK, central=True, weight=None))
        P.append(rect(190, y + 3, bw, 18, 4, PANEL, MODEL_S, 2, "6 4"))
        P.append(rect(190, y + 3, max(bw * b, 1), 18, 4, MODEL_F, MODEL_S, 2, "6 4"))
        P.append(t(190 + bw + 8, y + 14, "%.3f" % b, 12, INK, central=True))
        P.append(rect(440, y + 3, bw, 18, 4, PANEL, MODEL_S, 3))
        P.append(rect(440, y + 3, max(bw * a, 1), 18, 4, MODEL_F, MODEL_S, 3))
        P.append(t(440 + bw + 8, y + 14, "%.3f" % a, 12, INK, central=True))
        col = {1: OK_S, -1: BAD_S, 0: INK}[flag]
        P.append(t(690, y + 14, d, 14, col, central=True))
        if flag == 1:
            P.append(tick(752, y + 14))
        elif flag == -1:
            P.append(cross(752, y + 14))
    P.append(t(400, 358 - 6, "(7/30) &#215; 0.286 = +0.0667     (5/30) &#215; " + MIN + "0.200 = " + MIN + "0.0333     overall +0.0667 " + MIN + " 0.0333 = +0.0333",
               14, INK, "middle"))
    P.append(caption("billing: 2 of 5 became 1 of 5, one ticket (seed 0, 30 tickets).", 376))
    return svg_doc(W, "An overall gain can hide a falling category, and one ticket can be the whole fall",
                   "Per-category accuracy before and after LoRA, seed 0: greeting 0.833 to 0.833 on 6 tickets, refund 1.000 to 1.000 on 7, "
                   "technical 0.286 to 0.571 on 7 (up), billing 0.400 to 0.200 on 5 (down, outlined as a regression), "
                   "out_of_scope 0.400 to 0.400 on 5, overall 0.600 to 0.633 on 30. The weighted pieces are plus 0.0667 and minus 0.0333, "
                   "summing to plus 0.0333.", wrap(*P))


# ---------------------------------------------------------------- W32-1
def f32_1():
    """Week 32 section 5: reliability table of the 40 INVENTED results; ECE 0.1788."""
    B = [("0.00&#8211;0.59", 9, .551, .333, MIN + "0.218"), ("0.60&#8211;0.69", 7, .647, .571, MIN + "0.076"),
         ("0.70&#8211;0.79", 6, .753, .500, MIN + "0.253"), ("0.80&#8211;0.89", 8, .854, .750, MIN + "0.104"),
         ("0.90&#8211;1.00", 10, .931, .700, MIN + "0.231")]
    base, H = 296, 190
    P = [title("When it said 0.93, it was right 70% of the time")]
    P.append(line(60, base, 640, base, INK, 2))
    for v in (0, 0.5, 1.0):
        y = base - H * v
        P.append(line(60, y, 640, y, GRID, 1.5, "6 4") if v else "")
        P.append(t(52, y + 4, "%.1f" % v, 12, MUT, "end"))
    P.append(trot(34, base - H / 2, "share / stated confidence"))
    for k, (lab, n, s, a, g) in enumerate(B):
        cx = 120 + k * 115
        hs, ha = H * s, H * a
        P.append(rect(cx - 44, base - hs, 40, hs, 4, DATA_F, DATA_S, 3))
        P.append(rect(cx + 4, base - ha, 40, ha, 4, PANEL, DATA_S, 3, "6 4"))
        P.append(t(cx - 24, base - hs - 6, "%.3f" % s, 12, INK, "middle"))
        P.append(t(cx + 24, base - ha - 6, "%.3f" % a, 12, INK, "middle"))
        P.append(t(cx, base + 18, lab, 12, INK, "middle"))
        P.append(t(cx, base + 34, "n = %d" % n, 12, MUT, "middle"))
        P.append(t(cx, base + 50, "gap " + g, 12, BAD_S, "middle"))
    # legend
    P.append(rect(60, 62, 16, 12, 2, DATA_F, DATA_S, 3))
    P.append(t(82, 69, "stated (said)", 12, INK, central=True))
    P.append(rect(180, 62, 16, 12, 2, PANEL, DATA_S, 3, "6 4"))
    P.append(t(202, 69, "actual (right)", 12, INK, central=True))
    P.append(chip(440, 56, 200, "40 invented results, not a model", GRID, PANEL, 12, 26, mono=False, dash="6 4"))
    # ECE panel
    P.append(rect(662, 120, 118, 130, 12, ACC_F, ACC_S, 3))
    P.append(t(721, 148, "ECE", 18, INK, "middle"))
    P.append(t(721, 178, "0.1788", 18, INK, "middle", mono=True))
    P.append(t(721, 206, "gaps added,", 12, INK, "middle"))
    P.append(t(721, 222, "big buckets", 12, INK, "middle"))
    P.append(t(721, 238, "count more", 12, INK, "middle"))
    P.append(caption("ECE is the average gap, not the share wrong (42.5% were wrong).", 376))
    return svg_doc(W, "In every confidence bucket the system said more than it delivered",
                   "Five confidence buckets of 40 invented results, stated against actual. 0.00 to 0.59: n 9, stated 0.551, actual 0.333. "
                   "0.60 to 0.69: n 7, 0.647, 0.571. 0.70 to 0.79: n 6, 0.753, 0.500. 0.80 to 0.89: n 8, 0.854, 0.750. "
                   "0.90 to 1.00: n 10, 0.931, 0.700. Every gap is negative; ECE is 0.1788. The sheet was invented by the teacher.", wrap(*P))


# ---------------------------------------------------------------- W32-2
def f32_2():
    """Week 32 sections 7 and 9: coverage vs accuracy of the answered, 40 INVENTED results."""
    pts = [("t 0&#8211;0.5", 1.000, .575, "below"), ("t 0.6", .775, .645, "below"), ("t 0.7", .600, .667, "below"),
           ("t 0.8", .450, .722, "above"), ("t 0.85", .375, .733, "below"), ("t 0.9", .250, .700, "above"),
           ("t 0.95", .075, .667, "below")]
    X = lambda c: 80 + 400 * c
    Y = lambda a: 320 - 460 * (a - 0.5)
    P = [title("Abstaining trades right answers for wrong ones")]
    P.append(line(80, 320, 480, 320, INK, 2))
    P.append(line(80, 320, 80, 90, INK, 2))
    for v in (0.5, 0.75, 1.0):
        P.append(t(72, Y(v) + 4, "%.2f" % v, 12, MUT, "end"))
    for v in (0, 0.5, 1.0):
        P.append(t(X(v), 338, "%.1f" % v, 12, MUT, "middle"))
    P.append(t(280, 360, "coverage (share of the 40 answered)", 12, MUT, "middle"))
    P.append(trot(34, 205, "accuracy of the answered"))
    P.append(line(80, Y(.575), 480, Y(.575), GRID, 1.5, "6 4"))
    P.append(t(100, Y(.575) + 16, "answer everything: 0.575", 12, MUT))
    P.append(poly([(X(c), Y(a)) for _, c, a, _ in pts] + [(X(.025), Y(1.0))], "none", DATA_S, 3))
    for lab, c, a, pos in pts:
        hi = lab == "t 0.8"
        P.append(circ(X(c), Y(a), 10 if hi else 6, ACC_F if hi else PAPER, ACC_S if hi else DATA_S, 3))
        P.append(t(X(c), Y(a) + (-16 if pos == "above" else 24), lab, 12, INK, "middle"))
    P.append(mark("diamond", X(.025), Y(1.0), 6, DATA_S, PAPER, 3))
    P.append(t(X(.025) + 14, Y(1.0) + 4, "t 0.98: one question, right", 12, INK))
    # right panel
    rx = 520
    P.append(rect(rx, 96, 260, 200, 12, PANEL, ACC_S, 3))
    P.append(t(rx + 16, 124, "At t = 0.8 (ringed)", 18, INK))
    for i, s in enumerate(["18 of 40 answered, 13 right", "wrong but answered: 17 to 5",
                           "22 got &#8220;I don't know&#8221;:", "10 would have been right",
                           "billing: 4 of 8 to 2 of 6"]):
        P.append(t(rx + 16, 156 + i * 26, s, 14, INK))
    P.append(chip(rx, 312, 260, "40 invented results, not a model", GRID, PANEL, 12, 26, mono=False, dash="6 4"))
    P.append(caption("The curve does not say where to stop; you decide that in words.", 376))
    return svg_doc(W, "Abstaining cuts wrong answers by giving up right ones",
                   "Coverage against accuracy of the answered for 40 invented results. Answer everything: coverage 1.000, accuracy 0.575, 17 wrong. "
                   "t 0.6: 0.775, 0.645. t 0.7: 0.600, 0.667. t 0.8, ringed: 0.450, 0.722, answering 18 of 40 with 13 right and 5 wrong. "
                   "t 0.85: 0.375, 0.733. t 0.9: 0.250, 0.700. t 0.95: 0.075, 0.667. The last point at coverage 0.025 is one question, right, "
                   "accuracy 1.000. Billing fell from 4 of 8 to 2 of 6.", wrap(*P))


# ---------------------------------------------------------------- W33-1
def f33_1():
    """Week 33 section 6: first ten of 200 batches of 20 runs, same system (stand-in), expected 6, wobble 2.05."""
    cnt = [3, 7, 8, 7, 5, 8, 6, 7, 4, 3]
    base, S = 320, 20
    Y = lambda v: base - S * v
    P = [title("The same system, ten times: the count moves")]
    P.append(rect(80, Y(8.05), 440, Y(3.95) - Y(8.05), 0, DATA_F, DATA_S, 1.5))
    P.append(line(80, Y(6), 520, Y(6), DATA_S, 2, "6 4"))
    P.append(line(80, base, 520, base, INK, 2))
    P.append(line(80, base, 80, 100, INK, 2))
    for v in (0, 3, 6, 9):
        P.append(t(72, Y(v) + 4, str(v), 12, MUT, "end"))
    P.append(trot(34, 210, "landings out of 20 runs"))
    P.append(t(300, 358, "batch (same system, new seeds each time)", 12, MUT, "middle"))
    P.append(poly([(110 + 44 * i, Y(v)) for i, v in enumerate(cnt)], "none", GRID, 1.5))
    for i, v in enumerate(cnt):
        x = 110 + 44 * i
        ringed = i in (1, 2)
        P.append(circ(x, Y(v), 9 if ringed else 6, ACC_F if ringed else PAPER, ACC_S if ringed else DATA_S, 3))
        P.append(t(x, Y(v) - 14, str(v), 12, INK, "middle"))
        P.append(t(x, base + 16, str(i + 1), 12, MUT, "middle"))
    P.append(t(88, 84, "shaded: 6 &#177; 2.05, the ordinary range (4 to 8)", 12, INK))
    P.append(t(88, 102, "dashed: expected count n &#215; p = 20 &#215; 0.3 = 6", 12, INK))
    # right panel
    P.append(stand_in_frame(552, 92, 228, 262))
    rx = 566
    lines = [("200 batches of 20 runs", 14), ("smallest 1, largest 13", 14), ("mean count 6.08", 14),
             ("measured wobble 2.03", 14), ("formula says 2.05", 14), ("9 or more: 16 of 200", 14),
             ("with nothing changed", 14)]
    for i, (s, z) in enumerate(lines):
        P.append(t(rx, 128 + i * 28, s, z, INK))
    P.append(t(rx, 340, "batches 2 and 3: 7 then 8", 12, ACC_S))
    P.append(caption("A gap of 2 is inside what this stand-in does with no change.", 376))
    return svg_doc(W, "A count of 20 runs wobbles by about 2, so a gap of 2 is not a finding",
                   "First ten of 200 batches of 20 runs of the same stand-in system: 3, 7, 8, 7, 5, 8, 6, 7, 4, 3 landings. "
                   "Expected count is 6; the shaded ordinary range is 6 plus or minus 2.05, 4 to 8. Batches 2 and 3 (7 and 8) are ringed. "
                   "Over all 200 batches the smallest count was 1 and the largest 13, the mean 6.08, the measured wobble 2.03 against "
                   "a formula value of 2.05, and 16 batches showed 9 or more.", wrap(*P))


# ---------------------------------------------------------------- W33-2
def f33_2():
    """Week 33 section 7: four versions of the agent, 50 runs each (stand-in)."""
    R = [("v0: weak sandbox, no guard", 15, 15, 50, 15), ("patch 1: strict sandbox", 15, 0, 50, 15),
         ("patch 2: + named files only", 0, 0, 50, 0), ("BAD patch: no writes at all", 0, 0, 0, 0)]
    P = [title("A zero attack count is not enough to call a patch good")]
    P.append(stand_in_frame(28, 90, 744, 250))
    heads = [("A1", "landed"), ("A2", "landed"), ("legit save", "works"), ("A1 during", "the save")]
    x0, cw = 270, 120
    for j, (a, b) in enumerate(heads):
        P.append(t(x0 + j * cw + cw / 2, 114, a, 14, INK, "middle"))
        P.append(t(x0 + j * cw + cw / 2, 131, b, 14, INK, "middle"))
    for i, row in enumerate(R):
        y = 144 + i * 46
        bad = i == 3
        P.append(t(44, y + 22, row[0], 14, INK, central=True))
        vals = row[1:]
        good = [vals[0] == 0, vals[1] == 0, vals[2] == 50, vals[3] == 0]
        for j, v in enumerate(vals):
            x = x0 + j * cw
            g = good[j]
            P.append(sq(x, y, cw, 42, OK_F if g else BAD_F, OK_S if g else BAD_S, 2))
            P.append(t(x + 46, y + 21, "%d / 50" % v, 14, INK, "middle", central=True))
            P.append(tick(x + 98, y + 21) if g else cross(x + 98, y + 21))
        if bad:
            P.append(rect(x0 - 4, y - 2, 4 * cw + 8, 46, 8, "none", BAD_S, 3))
    P.append(t(400, 366, "BAD patch: 0 / 50 on both attacks and 0 / 50 saves. Re-test the happy path.", 14, INK, "middle"))
    return svg_doc(W, "A patch must stop the attack and keep the legitimate task working",
                   "Four versions of a stand-in agent, 50 runs each. v0: A1 15 of 50, A2 15 of 50, legitimate save 50 of 50, A1 during the save 15 of 50. "
                   "Patch 1, strict sandbox: 15, 0, 50, 15. Patch 2, named files only: 0, 0, 50, 0. The bad patch that refuses all writes: "
                   "0, 0, 0, 0, so it also stops the legitimate save and is outlined as wrong. Cells are shaded and marked with a tick or a cross.", wrap(*P))


FIGS = {"fig-w31-1-low-rank-patch.svg": f31_1, "fig-w31-2-regression-row.svg": f31_2,
        "fig-w32-1-reliability-gaps.svg": f32_1, "fig-w32-2-abstain-trade.svg": f32_2,
        "fig-w33-1-count-wobble.svg": f33_1, "fig-w33-2-patch-and-happy-path.svg": f33_2}


def emit():
    for name, fn in FIGS.items():
        open(os.path.join(HERE, name), "w").write(fn() + "\n")
    return len(FIGS)

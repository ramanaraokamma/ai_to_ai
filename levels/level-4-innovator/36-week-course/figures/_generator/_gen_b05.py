"""Block 5 (weeks 13, 14, 15) concept figures: two per week, six in all.

Every number printed on a canvas is copied from the week's executed student-guide output
(seeded) or is a hand sum printed beside it (STYLE 2.1). Nothing here is random.

    fig-w13-1-temperature-dial.svg        five letters, three temperatures, bars      (week 13 five.py)
    fig-w13-2-exposure-bias.svg           true prefix vs own prefix, and the losses   (week 13 exposure.py)
    fig-w14-1-soft-lookup.svg             hard lookup vs soft lookup, 42.77           (week 14 lookup.py)
    fig-w14-2-one-pass-three-words.svg    scores, weights, output for the/cat/sat     (week 14 attention.py)
    fig-w15-1-why-divide.svg              saturated vs divided scores; spread by d    (week 15 scale.py)
    fig-w15-2-hide-the-future.svg         the mask, the weights, the last-word test   (week 15 dials.py)

emit(figures_dir) writes them; _gen_build.py calls it.
"""
import os
from _gen_core import *
from _gen_motifs import _att_cells, _legend_cells

W = "0 0 800 400"
MINUS, TIMES, ARROW, DOT, SQRT, DIV, INF = "&#8722;", "&#215;", "&#8594;", "&#183;", "&#8730;", "&#247;", "&#8734;"


def title(s):
    return t(400, 44, s, 24, INK, "middle")


def cap(y, s, size=14):
    return t(400, y, s, size, MUT, "middle")


# ------------------------------------------------------------------ 13-1
def fig_13_1():
    letters = "abcde"
    panels = [("T = 0.3", [0.001, 0.958, 0.000, 0.034, 0.006], "b wins by a lot (sharp)"),
              ("T = 1", [0.076, 0.563, 0.028, 0.207, 0.126], "the model's own belief"),
              ("T = 2", [0.138, 0.375, 0.084, 0.227, 0.177], "b wins by a little (flat)")]
    o = [title("Temperature changes how much the best letter wins by")]
    for pi, (name, ps, sub) in enumerate(panels):
        px, py, pw, ph = 20 + pi * 260, 62, 240, 268
        o.append(rect(px, py, pw, ph, 12, PANEL, GRID, 2))
        o.append(t(px + 110, py + 30, name, 18, INK, "middle"))
        o.append(shape_chip(px + pw - 14 - 43, py + 10, "(5,)"))
        base = 280
        o.append(line(px + 14, base, px + pw - 14, base, GRID, 1.5))
        for i, v in enumerate(ps):
            cx = px + 34 + i * 43
            h = max(v * 170, 1.5)
            best = (i == 1)
            o.append(rect(cx - 15, base - h, 30, h, 3, ACC_F if best else DATA_F, ACC_S if best else DATA_S, 3 if best else 2))
            o.append(t(cx, base - h - 6, "%.3f" % v, 12, INK, "middle", mono=True))
            o.append(t(cx, base + 20, letters[i], 14, INK, "middle", mono=True))
        o.append(t(px + pw / 2.0, py + ph - 10, sub, 12, MUT, "middle"))
    o.append(cap(354, "Same model, same five scores. Only the divide before the softmax changes."))
    o.append(cap(372, "Invented scores 0.0, 2.0, %s1.0, 1.0, 0.5. b gets 0.958, 0.563, 0.375. Each panel adds to 1.000." % MINUS, 12))
    desc = ("Three bar charts of the chances of five letters a to e, built from the same five scores. At T = 0.3 the chances are "
            "0.001, 0.958, 0.000, 0.034, 0.006. At T = 1 they are 0.076, 0.563, 0.028, 0.207, 0.126. At T = 2 they are "
            "0.138, 0.375, 0.084, 0.227, 0.177. The bar for b is pink with a thick border in every panel and shrinks from 0.958 to 0.375. "
            "Each panel is a vector of shape (5,) and adds to 1.")
    return svg_doc(W, "A low temperature makes the best letter win by a lot; a high one makes the chances nearly flat", desc, J(o))


# ------------------------------------------------------------------ 13-2
def fig_13_2():
    o = [title("Exposure bias: it practised on true letters only")]
    # connectors first
    for lane_y in (62, 118):
        for i in range(4):
            x = 180 + 76 * i + 56
            o.append(arrow(x + 1, lane_y + 19, x + 19, lane_y + 19, INK, 2))
    for lane_y, wrong in ((62, False), (118, True)):
        for i, ch in enumerate("andr" if not wrong else "andt"):
            x = 180 + 76 * i
            bad = wrong and i == 3
            o.append(rect(x, lane_y, 56, 38, 8, BAD_F if bad else DATA_F, BAD_S if bad else DATA_S, 3))
            o.append(t(x + 28, lane_y + 19, ch, 18, INK, "middle", mono=True, central=True))
        o.append(rect(484, lane_y, 56, 38, 8, PAPER, MUT, 2, "6 4"))
        o.append(t(512, lane_y + 19, "next?", 14, MUT, "middle", central=True))
    o.append(t(20, 78, "training", 18, INK))
    o.append(t(20, 94, "4 letters in", 12, MUT))
    o.append(t(20, 134, "generating", 18, INK))
    o.append(t(20, 150, "4 letters in", 12, MUT))
    o.append(t(556, 76, "handed the true previous", 14, MUT))
    o.append(t(556, 94, "letter every time", 14, MUT))
    o.append(t(556, 128, "own letters: one unlikely", 14, MUT))
    o.append(t(556, 146, "pick, and the prefix is one", 14, MUT))
    o.append(t(556, 164, "it rarely practised", 14, MUT))
    o.append(t(436, 172, "unlikely pick", 12, BAD_S, "middle"))
    o.append(line(20, 186, 780, 186, GRID, 1.5, "6 4"))
    o.append(t(400, 206, "average loss per letter, true prefix fed in (lower = less surprised)", 14, MUT, "middle"))
    rows = [("real names (n=231)", 0.954, 0.000, DATA_F, DATA_S, None),
            ("own names, T=1.0 (n=200)", 1.122, 0.175, MODEL_F, MODEL_S, None),
            ("own names, T=0.5 (n=200)", 0.920, 0.010, MODEL_F, MODEL_S, None)]
    for i, (lab, m, share, fl, st, _) in enumerate(rows):
        y = 220 + 34 * i
        o.append(t(220, y + 13, lab, 14, INK, "end", central=True))
        o.append(rect(230, y, m * 270, 26, 4, fl, st, 3 if i == 1 else 2))
        o.append(t(541, y + 13, "mean %.3f %s above 1.5: %.3f" % (m, DOT, share), 12, INK, mono=True, central=True))
    o.append(cap(346, "Consistent with exposure bias, not proof: sampling and memorising fit the gap too."))
    o.append(cap(366, "One seed (7), one model. Measured on the Week 13 name model; no direct same-spot comparison was made.", 12))
    desc = ("Two rows of letter boxes. In training the model reads a, n, d, r, all true letters, and is asked for the next one. "
            "In generating it reads a, n, d, t where t, drawn red with a cross-free label unlikely pick, is its own unlikely draw, "
            "so the prefix is one it rarely practised. Below, three horizontal bars of average loss per letter: real names, "
            "231 names, 0.954 with 0.000 of them above 1.5; the model's own names at T = 1.0, 200 names, 1.122 with 0.175 above 1.5; "
            "its own names at T = 0.5, 0.920 with 0.010 above 1.5.")
    return svg_doc(W, "The model is more surprised by its own names (1.122) than by real ones (0.954): consistent with exposure bias, not proof", desc, J(o))


# ------------------------------------------------------------------ 14-1
def fig_14_1():
    names = ["bread", "river", "rope"]
    sc = ["0.1", "2.0", "0.3"]
    wt = [0.112, 0.751, 0.137]
    val = ["10.0", "50.0", "30.0"]
    prod = ["1.12", "37.55", "4.11"]
    o = [title("A soft lookup hears every answer, loudest first")]
    o.append(t(80, 84, "label", 14, MUT, "middle"))
    o.append(t(160, 84, "score", 14, MUT, "middle"))
    o.append(shape_chip(186, 67, "(3,)"))
    o.append(t(236, 84, "weight", 14, MUT))
    o.append(shape_chip(288, 67, "(3,)"))
    o.append(t(502, 84, "value", 14, MUT, "middle"))
    o.append(shape_chip(528, 67, "(3,)"))
    o.append(t(660, 84, "weight %s value" % TIMES, 14, MUT, "middle"))
    for i in range(3):
        cy = 130 + 60 * i
        best = i == 1
        o.append(line(100, cy, 470, cy, GRID, 1.5))
        o.append(rect(20, cy - 20, 90, 40, 8, DATA_F, DATA_S, 3 if best else 2))
        o.append(t(65, cy, names[i], 18, INK, "middle", central=True))
        o.append(t(160, cy, sc[i], 14, INK, "middle", mono=True, central=True))
        o.append(rect(236, cy - 14, wt[i] * 200, 28, 4, ACC_F if best else DATA_F, ACC_S if best else DATA_S, 3 if best else 2))
        o.append(t(236 + wt[i] * 200 + 8, cy, "%.3f" % wt[i], 12, INK, mono=True, central=True))
        o.append(rect(470, cy - 20, 64, 40, 8, DATA_F, DATA_S, 2))
        o.append(t(502, cy, val[i], 14, INK, "middle", mono=True, central=True))
        o.append(t(660, cy, prod[i], 14, INK, "middle", mono=True, central=True))
    o.append(line(600, 272, 720, 272, INK, 2))
    o.append(t(600, 306, "soft answer", 14, INK, "end", central=True))
    o.append(rect(610, 286, 110, 40, 8, ACC_F, ACC_S, 3))
    o.append(t(665, 306, "42.77", 18, INK, "middle", mono=True, central=True))
    o.append(rect(20, 286, 330, 40, 8, PANEL, GRID, 2, "6 4"))
    o.append(t(185, 306, "hard answer: only river counts, 50.0", 14, INK, "middle", central=True))
    o.append(cap(356, "Weights add to 1.000. Hand sum with rounded weights: 1.12 + 37.55 + 4.11 = 42.78."))
    o.append(cap(374, "The computer keeps every digit and prints 42.77; the hundredth is rounding. Scores and values are invented.", 12))
    desc = ("A table of three rows: bread, river, rope. Scores 0.1, 2.0, 0.3 become weights 0.112, 0.751, 0.137, drawn as horizontal bars "
            "with the river bar pink and longest. Values are 10.0, 50.0, 30.0. Weight times value gives 1.12, 37.55, 4.11, which sum to "
            "the soft answer 42.77. A dashed box on the left says the hard lookup would hear only the river and answer 50.0.")
    return svg_doc(W, "A soft lookup is a weighted average: mostly the best match (42.77), where a hard lookup hears only one (50.0)", desc, J(o))


# ------------------------------------------------------------------ 14-2
def _grid_labels(x0, y0, cw, ch, toks, key_title=True):
    o = []
    if key_title:
        o.append(t(x0 + 1.5 * cw, 126, "key (being looked at)", 12, MUT, "middle"))
    for j, tk in enumerate(toks):
        o.append(t(x0 + j * cw + cw / 2.0, 146, tk, 14, INK, "middle", mono=True))
    for i, tk in enumerate(toks):
        o.append(t(x0 - 8, y0 + i * ch + ch / 2.0, tk, 14, INK, "end", mono=True, central=True))
    return o


def fig_14_2():
    toks = ["the", "cat", "sat"]
    S = [[1, 0, 1], [0, 1, 1], [1, 1, 2]]
    Wt = [[0.422, 0.155, 0.422], [0.155, 0.422, 0.422], [0.212, 0.212, 0.576]]
    Out = [[0.578, 0.845], [0.845, 0.578], [0.788, 0.788]]
    cw, ch, y0 = 48, 44, 156
    g1, g2, g3 = 72, 294, 584
    o = [title("One pass of attention on three words")]
    o.append(arrow(224, y0 + 66, 286, y0 + 66, INK, 3))
    o.append(arrow(510, y0 + 66, 572, y0 + 66, INK, 3))
    o.append(t(255, y0 + 54, "softmax", 12, MUT, "middle"))
    o.append(t(541, y0 + 54, "blend V", 12, MUT, "middle"))
    o.append(t(g1 + 1.5 * cw, 100, "step 2: scores", 18, INK, "middle"))
    o.append(t(g2 + 1.5 * cw, 100, "step 3: weights", 18, INK, "middle"))
    o.append(t(g3 + cw, 100, "step 4: output", 18, INK, "middle"))
    o += _grid_labels(g1, y0, cw, ch, toks)
    o += _grid_labels(g2, y0, cw, ch, toks)
    o.append(trot(34, y0 + 1.5 * ch, "query (asking)", 12))
    for i in range(3):
        for j in range(3):
            o.append(sq(g1 + j * cw, y0 + i * ch, cw, ch, DATA_F, GRID, 2))
            o.append(t(g1 + j * cw + cw / 2.0, y0 + i * ch + ch / 2.0, str(S[i][j]), 14, INK, "middle", mono=True, central=True))
    o += _att_cells(g2, y0, cw, ch, Wt, toks, 12, "%.3f")
    for i in range(3):
        o.append(t(g2 + 3 * cw + 8, y0 + i * ch + ch / 2.0, "sum = 1", 12, MUT, central=True))
    for i in range(3):
        for j in range(2):
            o.append(sq(g3 + j * cw, y0 + i * ch, cw, ch, DATA_F, DATA_S, 2))
            o.append(t(g3 + j * cw + cw / 2.0, y0 + i * ch + ch / 2.0, "%.3f" % Out[i][j], 12, INK, "middle", mono=True, central=True))
        o.append(t(g3 - 8, y0 + i * ch + ch / 2.0, toks[i], 14, INK, "end", mono=True, central=True))
    for gx, sh in ((g1, "(3, 3)"), (g2, "(3, 3)"), (g3, "(3, 2)")):
        o.append(shape_chip(gx, y0 + 3 * ch + 10, sh))
    o += _legend_cells(30, 340)
    o.append(cap(374, "Invented 2-number words, nothing learned. Each weight row is one word sharing its attention.", 12))
    desc = ("Three grids left to right joined by arrows. Step 2, scores, shape (3, 3): rows the, cat, sat are 1, 0, 1 then 0, 1, 1 then 1, 1, 2. "
            "Step 3, weights, shape (3, 3), after a softmax of each row: the 0.422, 0.155, 0.422; cat 0.155, 0.422, 0.422; "
            "sat 0.212, 0.212, 0.576; every row sums to 1 and the largest in each row is ringed. Step 4, output, shape (3, 2): "
            "0.578, 0.845 then 0.845, 0.578 then 0.788, 0.788. Rows are the query, columns are the key.")
    return svg_doc(W, "Each word asks, shares its attention in a row that adds to 1, and hears a blend of the values", desc, J(o))


# ------------------------------------------------------------------ 15-1
def fig_15_1():
    o = [title("Why the dot product is divided by " + SQRT + "d")]
    o.append(rect(20, 62, 370, 284, 12, PANEL, GRID, 2))
    o.append(rect(410, 62, 370, 284, 12, PANEL, GRID, 2))
    A = ([0.999044, 0.000045, 0.000911], ["8", MINUS + "2", "1"], ["0.999044", "0.000045", "0.000911"])
    B = ([0.587, 0.168, 0.245], ["1", MINUS + "0.25", "0.125"], ["0.587", "0.168", "0.245"])
    base = 290
    for k, (xs, hd, sub, data, good) in enumerate([((50, 110, 170), "raw scores", "saturated: one winner", A, False),
                                                   ((235, 295, 355), "divided by 8", "everyone still counts", B, True)]):
        cxm = xs[1]
        o.append(t(cxm, 90, hd, 18, INK, "middle"))
        o.append(t(cxm + (20 if not good else 20), 110, sub, 12, OK_S if good else BAD_S, "middle"))
        o.append(line(xs[0] - 28, base, xs[2] + 28, base, GRID, 1.5))
        for i, cx in enumerate(xs):
            v = data[0][i]
            h = max(v * 140, 1.5)
            top = (i == data[0].index(max(data[0])))
            o.append(rect(cx - 15, base - h, 30, h, 3, ACC_F if top else DATA_F, ACC_S if top else DATA_S, 3 if top else 2))
            o.append(t(cx, base - h - 6, data[2][i], 12, INK, "middle", mono=True))
            o.append(t(cx, base + 18, data[1][i], 12, INK, "middle", mono=True))
    o.append(t(205, 316, "bar = weight; number below = score", 12, MUT, "middle"))
    o.append(shape_chip(338, 304, "(3,)"))
    o.append(tick(231, 105, 7, OK_S))
    o.append(cross(46, 105, 5, BAD_S))
    # right panel
    o.append(t(595, 90, "spread of q " + DOT + " k, by width d", 18, INK, "middle"))
    raw, div = [2.01, 4.00, 7.91], [1.00, 1.00, 0.99]
    for g, d in enumerate([4, 16, 64]):
        y = 112 + 66 * g
        o.append(t(462, y + 21, "d = %d" % d, 14, INK, "end", central=True))
        o.append(rect(470, y, raw[g] * 30, 18, 3, DATA_F, DATA_S, 2))
        o.append(t(470 + raw[g] * 30 + 8, y + 9, "raw: %.2f" % raw[g], 12, INK, mono=True, central=True))
        o.append(rect(470, y + 22, div[g] * 30, 18, 3, OK_F, OK_S, 2, "6 4"))
        o.append(t(470 + div[g] * 30 + 8, y + 31, "%s %s%sd: %.2f" % (DIV, "", SQRT, div[g]), 12, INK, mono=True, central=True))
    o.append(t(595, 318, "10,000 random pairs per width, seed 0", 12, MUT, "middle"))
    o.append(cap(364, "At width 64 a raw row of 8 scores gives its biggest weight 0.880; divided, the biggest weight", 12))
    o.append(cap(380 - 6, "stays near 0.365 at every width (4, 16, 64). An equal share would be 0.125.", 12))
    desc = ("Left, two bar charts of the weights from three scores. Raw scores 8, minus 2, 1 give weights 0.999044, 0.000045, 0.000911: "
            "one winner takes almost everything. Divided by 8, the square root of 64, the scores 1, minus 0.25, 0.125 give 0.587, 0.168, 0.245. "
            "Right, horizontal bars for the spread of a dot product: width 4 raw 2.01, width 16 raw 4.00, width 64 raw 7.91, while after dividing "
            "by the square root of d they are 1.00, 1.00 and 0.99.")
    return svg_doc(W, "Dividing by the square root of the width keeps the spread at 1 and keeps the softmax from saturating", desc, J(o))


# ------------------------------------------------------------------ 15-2
def fig_15_2():
    toks = ["the", "cat", "sat"]
    M_ = [[1, 0, 0], [1, 1, 0], [1, 1, 1]]
    Wt = [[1.0, 0.0, 0.0], [0.3302, 0.6698, 0.0], [0.2483, 0.2483, 0.5035]]
    cw, ch, y0 = 48, 44, 156
    g1, g2 = 72, 330
    o = [title("Hide the future: read only the past")]
    o.append(line(545, 80, 545, 330, GRID, 1.5, "6 4"))
    o.append(arrow(222, y0 + 66, 322, y0 + 66, INK, 3))
    o.append(t(272, y0 + 46, "hide, then", 12, MUT, "middle"))
    o.append(t(272, y0 + 60, "softmax", 12, MUT, "middle"))
    o.append(t(g1 + 1.5 * cw, 90, "mask", 18, INK, "middle"))
    o.append(t(g1 + 1.5 * cw, 108, "1 = may read", 12, MUT, "middle"))
    o.append(t(g2 + 1.5 * cw, 90, "weights", 18, INK, "middle"))
    o.append(t(g2 + 1.5 * cw, 108, "both dials on", 12, MUT, "middle"))
    o += _grid_labels(g1, y0, cw, ch, toks)
    o += _grid_labels(g2, y0, cw, ch, toks)
    o.append(trot(34, y0 + 1.5 * ch, "query (asking)", 12))
    for i in range(3):
        for j in range(3):
            if M_[i][j]:
                o.append(sq(g1 + j * cw, y0 + i * ch, cw, ch, DATA_F, GRID, 2))
            else:
                o.append(sq(g1 + j * cw, y0 + i * ch, cw, ch, PANEL, GRID, 2))
                o.append(line(g1 + j * cw + 8, y0 + i * ch + 8, g1 + j * cw + cw - 8, y0 + i * ch + ch - 8, GRID, 2))
            o.append(t(g1 + j * cw + cw / 2.0, y0 + i * ch + ch / 2.0 + (0 if M_[i][j] else 0), str(M_[i][j]), 14, INK if M_[i][j] else MUT,
                       "middle", mono=True, central=True))
    for i in range(3):
        m = max(Wt[i])
        for j in range(3):
            x, y = g2 + j * cw, y0 + i * ch
            if j > i:
                o.append(sq(x, y, cw, ch, PANEL, GRID, 2))
                o.append(line(x + 8, y + 8, x + cw - 8, y + ch - 8, GRID, 2))
                o.append(t(x + cw / 2.0, y + ch / 2.0 + 14, MINUS + INF, 12, MUT, "middle"))
            else:
                f, s, sw = cell_tint(Wt[i][j], m)
                o.append(sq(x, y, cw, ch, f, s, sw))
        o.append(t(g2 + 3 * cw + 8, y0 + i * ch + ch / 2.0, "sum = 1", 12, MUT, central=True))
    for i in range(3):
        j = Wt[i].index(max(Wt[i]))
        o.append(sq(g2 + j * cw, y0 + i * ch, cw, ch, "none", ACC_S, 3))
    for i in range(3):
        for j in range(i + 1):
            o.append(t(g2 + j * cw + cw / 2.0, y0 + i * ch + ch / 2.0, "%.4f" % Wt[i][j], 12, INK, "middle", mono=True, central=True))
    o.append(shape_chip(g2, y0 + 3 * ch + 10, "(3, 3)"))
    o += _legend_cells(30, 340)
    # right: the leak test
    o.append(t(662, 90, "change the last word", 18, INK, "middle"))
    o.append(t(662, 108, "does that row's answer move?", 12, MUT, "middle"))
    o.append(t(640, 138, "no mask", 12, MUT, "middle"))
    o.append(t(720, 138, "mask", 12, MUT, "middle"))
    res = [(True, False), (True, False), (True, True)]
    for i in range(3):
        y = 150 + 44 * i
        o.append(t(596, y + 17, toks[i], 14, INK, "end", mono=True, central=True))
        for c, cx in enumerate((606, 686)):
            moved = res[i][c]
            leak = moved and i < 2
            o.append(rect(cx, y, 68, 34, 6, BAD_F if leak else (DATA_F if moved else OK_F),
                          BAD_S if leak else (DATA_S if moved else OK_S), 2))
            o.append(t(cx + 40, y + 17, "moved" if moved else "stayed", 12, INK, "middle", central=True))
            if leak:
                o.append(cross(cx + 12, y + 17, 5, BAD_S))
            elif not moved:
                o.append(tick(cx + 12, y + 17, 7, OK_S))
    o.append(t(662, 296, "moved with no mask = leaked", 12, MUT, "middle"))
    o.append(t(662, 314, "the and cat stay put with the mask", 12, MUT, "middle"))
    o.append(cap(374, "Invented words, nothing learned. Hidden scores are " + MINUS + INF + " before the softmax: weight exactly 0.", 12))
    desc = ("Left, a 3 by 3 mask for the, cat, sat: row the 1, 0, 0; row cat 1, 1, 0; row sat 1, 1, 1, with the 0 cells struck through. "
            "An arrow labelled hide, then softmax leads to the weights, shape (3, 3): the 1.0000, 0, 0; cat 0.3302, 0.6698, 0; "
            "sat 0.2483, 0.2483, 0.5035; hidden cells are minus infinity and every row sums to 1. Right, a table for changing only the last word: "
            "without the mask all three rows moved; with the mask the and cat stayed and sat moved.")
    return svg_doc(W, "The causal mask hides later words before the softmax, so changing the last word cannot change earlier answers", desc, J(o))


FIGS = {
    "fig-w13-1-temperature-dial.svg": fig_13_1,
    "fig-w13-2-exposure-bias.svg": fig_13_2,
    "fig-w14-1-soft-lookup.svg": fig_14_1,
    "fig-w14-2-one-pass-three-words.svg": fig_14_2,
    "fig-w15-1-why-divide.svg": fig_15_1,
    "fig-w15-2-hide-the-future.svg": fig_15_2,
}


def emit(figures_dir):
    for name, fn in FIGS.items():
        with open(os.path.join(figures_dir, name), "w") as f:
            f.write(fn() + "\n")
    return len(FIGS)

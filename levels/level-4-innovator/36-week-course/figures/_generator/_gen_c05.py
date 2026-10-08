"""Block C5 (weeks 13, 14, 15) extra figures: a mental-model figure, a worked-numbers figure and a
blank workbook figure per week. Every number is copied from the week's printed output or is a
hand sum printed beside it (STYLE.md 2.1).

W13 student-guide/week-13.md: five.py (T=1 chances, top-3 kept, greedy picks b) and namegen.py
    (distinct / new out of 200, seven rows); the blank is workbook page 13.3 Part C (scores 2, 1, 0.5, 0),
    no bar, mark or ring drawn
W14 student-guide/week-14.md: the four steps (no numbers); attention.py scores and weights (Part 1) and
    twotables.py (scores2 and weights2); the blank is workbook page 14.1 Part B (a two-token practice
    pass), no value drawn
W15 student-guide/week-15.md: snippet (b) row 2 (4 5 6 -> 4 5 -inf -> 0.2689 0.7311 0.0000), snippet (c)
    shapes (2, 5, 12) -> (2, 5, 3, 4) -> (2, 3, 5, 4); scale.py last table (average biggest weight of a row
    of 8, raw versus divided by sqrt(d)); the blank is workbook page 15.5 Part B (B 3, T 4, d 20, H 5), no
    answer drawn
"""
from _gen_core import *

FIGS = {}


def fig(name, vb, title, desc, parts):
    FIGS[name] = svg_doc(vb, title, desc, J(*parts))


def ctitle(s):
    return t(400, 44, s, 24, INK, "middle")


def cap(s, y=374):
    return t(400, y, s, 14, MUT, "middle")


def box(x, y, w, h, title, sub, fill, stroke, dash=None):
    """A stage box: label (18) over a muted sub line (12)."""
    return "%s\n  %s\n  %s" % (rect(x, y, w, h, 10, fill, stroke, 3, dash),
                               t(x + w / 2.0, y + h * 0.36, title, 18, INK, "middle", central=True),
                               t(x + w / 2.0, y + h * 0.74, sub, 12, MUT, "middle", central=True))


def cell(x, y, w, h, txt, fill=PANEL, stroke=GRID, sw=2, size=14, mono=False):
    return "%s\n  %s" % (sq(x, y, w, h, fill, stroke, sw),
                         t(x + w / 2.0, y + h / 2.0, txt, size, INK, "middle", mono=mono, central=True))


# ---------------------------------------------------------------- W13-4  scores to a letter
def w13_4():
    bw, gap, x0, by, bh = 132, 24, 22, 116, 60
    X = lambda i: x0 + i * (bw + gap)
    C = lambda i: X(i) + bw / 2.0
    o = [ctitle("From scores to one letter")]
    o.append(bracket(X(1), X(4) + bw, 108, 8, MUT))
    o.append(t((X(1) + X(4) + bw) / 2.0, 90, "the pick plug: greedy, temperature, top-k, top-p", 14, MUT, "middle"))
    for i in range(4):                                   # arrows first, boxes second
        o.append(arrow(X(i) + bw + 2, by + bh / 2.0, X(i + 1) - 3, by + bh / 2.0, INK, 3))
    o.append(box(X(0), by, bw, bh, "scores", "from the model", DATA_F, DATA_S))
    o.append(box(X(1), by, bw, bh, "divide by T", "your choice of T", HUMAN_F, HUMAN_S))
    o.append(box(X(2), by, bw, bh, "softmax", "chances add to 1", DATA_F, DATA_S))
    o.append(box(X(3), by, bw, bh, "cut (optional)", "top-k or top-p", HUMAN_F, HUMAN_S, "6 4"))
    o.append(box(X(4), by, bw, bh, "pick", "greedy or a draw", HUMAN_F, HUMAN_S))
    ex = [
        [("scores for a to e:", 0), ("0.0 2.0 -1.0", 1), ("1.0 0.5", 1)],
        [("T = 1: no change", 0), ("T = 0.3: sharper", 0), ("T = 2: flatter", 0)],
        [("chances at T = 1:", 0), ("0.076 0.563 0.028", 1), ("0.207 0.126", 1)],
        [("top-3 keeps b d e:", 0), ("0.629 0.231 0.140", 1)],
        [("greedy: always b", 0), ("draw: b owns 0.563", 0)],
    ]
    for i, lines in enumerate(ex):
        for j, (s, m) in enumerate(lines):
            o.append(t(C(i), 200 + j * 17, s, 12, INK if m else MUT, "middle", mono=bool(m)))
    # the fed-back loop
    o.append(poly([(C(4), 248), (C(4), 272), (C(0), 272), (C(0), 252)], "none", MUT, 2, "6 4"))
    o.append(head(C(0), 248, -90, MUT, 2))
    o.append(t(400, 298, "the chosen letter is fed back in as the model's next input", 14, MUT, "middle"))
    o.append(t(400, 334, "Top-p cuts after softmax. Top-k cuts the scores first and softmaxes only the survivors.", 12, MUT, "middle"))
    o.append(cap("The model is the same in every line. Only the plug that chooses changes.", 360))
    fig("fig-w13-4-scores-to-one-letter", "0 0 800 400",
        "Scores become one letter in a fixed order: divide by T, softmax, optionally cut, then pick, and the pick is the only part that changes",
        "A row of five boxes joined by arrows: scores from the model, divide by T, softmax, an optional dashed cut by top-k or top-p, and pick by greedy or a draw. "
        "A bracket over the last four boxes is labelled the pick plug. Under the boxes, example numbers for the letters a to e: scores 0.0, 2.0, -1.0, 1.0, 0.5; "
        "chances at T equal to 1 of 0.076, 0.563, 0.028, 0.207, 0.126; top-3 keeps b, d and e at 0.629, 0.231 and 0.140; greedy always gives b. "
        "A dashed arrow returns from the pick to the start: the chosen letter is fed back as the next input. A note says top-p cuts after softmax, while top-k cuts the scores first and softmaxes only the survivors.", o)


# ---------------------------------------------------------------- W13-5  namegen table as bars
def w13_5():
    rows = [("greedy", 1, 0), ("T=0.5", 111, 2), ("T=1.0", 155, 32), ("T=1.5", 192, 118),
            ("top-k 5", 73, 18), ("top-p 0.9", 128, 7), ("T=1.5, top-p 0.9", 159, 50)]   # namegen.py output
    xl, xr, y0, pitch = 190, 640, 92, 34
    X = lambda v: xl + v / 200.0 * (xr - xl)
    o = [ctitle("Two counts per sampler, out of 200 names")]
    o.append(rect(190, 62, 14, 12, 2, DATA_F, DATA_S, 2))
    o.append(t(210, 73, "distinct names (top bar)", 12, INK, "start"))
    o.append(rect(420, 62, 14, 12, 2, ACC_F, ACC_S, 3))
    o.append(t(440, 73, "new, not in the 231 (lower bar)", 12, INK, "start"))
    yb = y0 + len(rows) * pitch
    for v in (0, 100, 200):
        o.append(line(X(v), y0 - 4, X(v), yb, GRID, 1.5, "4 4" if v else None))
        o.append(t(X(v), yb + 18, str(v), 12, MUT, "middle"))
    for i, (lab, d, n) in enumerate(rows):
        y = y0 + i * pitch
        o.append(t(xl - 12, y + 18, lab, 14, INK, "end"))
        o.append(rect(xl, y + 2, X(d) - xl if d else 2, 13, 2, DATA_F, DATA_S, 2))
        o.append(t(X(d) + 8, y + 13, str(d), 12, INK, "start"))
        o.append(rect(xl, y + 18, X(n) - xl if n else 2, 13, 2, ACC_F, ACC_S, 3))
        o.append(t(X(n) + 8, y + 29, str(n), 12, INK, "start"))
    o.append(line(xl, y0 - 4, xl, yb, INK, 2))
    o.append(cap("Greedy repeats one name; a hot sampler makes many new strings, misspellings included.", 372))
    fig("fig-w13-5-sampler-counts", "0 0 800 400",
        "Few new names means reciting the training list; many new names means variety but includes misspellings",
        "Seven pairs of horizontal bars from namegen.py, out of 200 names each. Distinct names then new names: greedy 1 and 0; T equal to 0.5, 111 and 2; "
        "T equal to 1.0, 155 and 32; T equal to 1.5, 192 and 118; top-k 5, 73 and 18; top-p 0.9, 128 and 7; T equal to 1.5 with top-p 0.9, 159 and 50.", o)


# ---------------------------------------------------------------- W13-6  blank: top-p by hand
def w13_6():
    o = [ctitle("Blank: top-p by hand, scores 2, 1, 0.5, 0")]
    x0, x1, yb, yt = 70, 390, 300, 100
    Y = lambda v: yb - v / 0.6 * (yb - yt)
    o.append(t((x0 + x1) / 2.0, 82, "chance of each letter", 14, INK, "middle"))
    for v, lab in ((0, "0"), (0.2, "0.2"), (0.4, "0.4"), (0.6, "0.6")):
        o.append(line(x0, Y(v), x1, Y(v), GRID, 1.5, "4 4" if v else None))
        o.append(t(x0 - 8, Y(v) + 4, lab, 12, MUT, "end"))
    o.append(line(x0, yb, x1, yb, INK, 2))
    o.append(line(x0, yt, x0, yb, INK, 2))
    for i, nm in enumerate(("1st", "2nd", "3rd", "4th")):
        cx = x0 + 40 + i * 76
        o.append(rect(cx - 24, yt + 4, 48, yb - yt - 8, 4, "none", GRID, 1.5, "2 5"))
        o.append(t(cx, yb + 20, nm, 12, MUT, "middle"))
    o.append(t((x0 + x1) / 2.0, yb + 44, "letters, best score first", 12, MUT, "middle"))
    # running-total lines
    lx0, lx1 = 520, 740
    LX = lambda v: lx0 + v * (lx1 - lx0)
    o.append(t(630, 82, "running total", 14, INK, "middle"))
    o.append(t(758, 98, "kept?", 12, MUT, "middle"))
    for v in (0, 0.5, 1.0):
        o.append(line(LX(v), 106, LX(v), 296, GRID, 1.5, "4 4"))
        o.append(t(LX(v), 316, "0" if v == 0 else str(v), 12, MUT, "middle"))
    o.append(line(LX(0.9), 106, LX(0.9), 296, ACC_S, 2, "6 4"))
    o.append(t(LX(0.9), 332, "p = 0.9", 12, ACC_S, "middle"))
    for i, nm in enumerate(("after 1st", "after 2nd", "after 3rd", "after 4th")):
        y = 140 + i * 50
        o.append(t(lx0 - 12, y + 4, nm, 12, MUT, "end"))
        o.append(line(lx0, y, lx1, y, INK, 2))
        o.append(circ(758, y, 12, PAPER, INK, 2))
    o.append(cap("Draw each bar, mark each running total, fill the circle of each letter kept at p = 0.9.", 372))
    fig("fig-w13-6-blank-top-p", "0 0 800 400",
        "A blank chart: draw four chances as bars, mark their running totals, and fill the circle of each letter that top-p keeps",
        "Left, empty axes from 0 to 0.6 with four dotted slots for the 1st to 4th letter. Right, four empty lines from 0 to 1, labelled after the 1st, 2nd, 3rd and 4th letter, "
        "with a dashed marker at p equal to 0.9 and an empty circle at the end of each line under the heading kept. No bar, mark or ring is drawn.", o)


# ---------------------------------------------------------------- W14-4  question, label, value
def w14_4():
    o = [ctitle("A word becomes a question, a label and a value")]
    o.append(ring_num(32, 84, 1))
    o.append(t(52, 89, "make", 14, INK, "start"))
    # connectors first
    rows = [("Wq", "q", "the question", "what am I looking for?", 100, ACC_F, ACC_S),
            ("Wk", "k", "the label", "what do I offer?", 170, DATA_F, DATA_S),
            ("Wv", "v", "the value", "what do I actually say?", 283, DATA_F, DATA_S)]
    for w_, _, _, _, cy, _, _ in rows:
        o.append(arrow(112, 190, 148, cy, INK, 3))
        o.append(arrow(232, cy, 268, cy, INK, 3))
    o.append(arrow(472, 100, 518, 124, INK, 3))
    o.append(arrow(472, 170, 518, 146, INK, 3))
    o.append(arrow(472, 283, 518, 283, INK, 3))
    o.append(arrow(650, 160, 650, 182, INK, 3))
    o.append(arrow(650, 238, 650, 260, INK, 3))
    o.append(box(20, 160, 92, 60, "a word", "as 2 numbers", DATA_F, DATA_S))
    for w_, nm, ttl, sub, cy, fl, st in rows:
        o.append(rect(150, cy - 22, 80, 44, 10, MODEL_F, MODEL_S, 3))
        o.append(t(190, cy, "x times " + w_, 12, INK, "middle", central=True))
        o.append(rect(270, cy - 28, 200, 56, 10, fl, st, 3))
        o.append(t(370, cy - 8, nm + "  " + ttl, 18, INK, "middle", central=True))
        o.append(t(370, cy + 14, sub, 12, MUT, "middle", central=True))
    o.append(box(520, 104, 260, 56, "score", "each question against every label", DATA_F, DATA_S))
    o.append(box(520, 182, 260, 56, "share", "softmax of each row: adds to 1", DATA_F, DATA_S))
    o.append(box(520, 260, 260, 56, "blend", "weighted average of the values", DATA_F, DATA_S))
    for n, y in ((2, 132), (3, 210), (4, 288)):
        o.append(ring_num(538, y, n))
    o.append(t(150, 228, "the three tables (purple) are why a word", 12, MUT, "start"))
    o.append(t(150, 244, "can ask one thing and offer another", 12, MUT, "start"))
    o.append(cap("Every word does this, so questions, labels and values each get one row per word.", 372))
    fig("fig-w14-4-question-label-value", "0 0 800 400",
        "Each word is turned into a question, a label and a value; questions meet labels to give scores, softmax shares them, and the values are blended",
        "A word, drawn as two numbers, has three arrows to three purple table boxes, x times Wq, x times Wk and x times Wv. They give q the question, what am I looking for; "
        "k the label, what do I offer; and v the value, what do I actually say. Questions and labels feed a box numbered 2, score; then a box 3, share, softmax of each row so it adds to 1; "
        "then a box 4, blend, a weighted average of the values, which also receive the v arrow. Step 1 is the making. No numbers are drawn.", o)


# ---------------------------------------------------------------- W14-5  same table versus two tables
def w14_5():
    S1 = [[1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 2.0]]            # attention.py: scores
    W1 = [[0.422, 0.155, 0.422], [0.155, 0.422, 0.422], [0.212, 0.212, 0.576]]   # attention.py: weights
    S2 = [[0.0, 0.0, 0.0], [1.0, 0.0, 1.0], [1.0, 0.0, 1.0]]            # twotables.py: question table changed
    W2 = [[0.333, 0.333, 0.333], [0.422, 0.155, 0.422], [0.422, 0.155, 0.422]]   # twotables.py: weights
    words = ("the", "cat", "sat")
    cw, ch = 72, 28
    o = [ctitle("Same table or two tables: the scores")]
    for gx, head_, S, W, ring, note in (
            (80, "one table for both", S1, W1, ((1, 2), (2, 1)), "cat to sat 1.0 = sat to cat 1.0: a mirror"),
            (480, "question table changed", S2, W2, ((1, 2), (2, 1)), "cat to sat 1.0, sat to cat 0.0: no mirror")):
        cx = gx + cw * 1.5
        o.append(t(cx, 76, head_, 18, INK, "middle"))
        for j, w_ in enumerate(words):
            o.append(t(gx + j * cw + cw / 2.0, 100, w_, 12, MUT, "middle"))
        for i in range(3):
            o.append(t(gx - 8, 108 + i * ch + ch / 2.0 + 4, words[i], 12, MUT, "end"))
            for j in range(3):
                hot = (i, j) in ring
                o.append(cell(gx + j * cw, 108 + i * ch, cw, ch, "%.1f" % S[i][j],
                              ACC_F if hot else PANEL, ACC_S if hot else GRID, 3 if hot else 2, 14, True))
        o.append(t(cx, 214, "weights: softmax of each row", 12, MUT, "middle"))
        for i in range(3):
            o.append(t(gx - 8, 222 + i * ch + ch / 2.0 + 4, words[i], 12, MUT, "end"))
            row_max = max(W[i])
            tie_all = len(set(W[i])) == 1
            for j in range(3):
                if tie_all:
                    fl, st, sw = DATA_F, GRID, 2
                else:
                    fl, st, sw = cell_tint(W[i][j], row_max)
                o.append(cell(gx + j * cw, 222 + i * ch, cw, ch, "%.3f" % W[i][j], fl, st, sw, 14, True))
        o.append(t(cx, 330, note, 14, INK, "middle"))
    o.append(t(480 + cw * 1.5, 352, "the: all equal, so its answer is the plain mean", 12, MUT, "middle"))
    o.append(cap("A different question table breaks the mirror: asking and offering can differ.", 372))
    fig("fig-w14-5-one-table-or-two", "0 0 800 400",
        "With one table for questions and labels the score grid is a mirror image; with two tables it need not be",
        "Two panels, each with a 3 by 3 grid of scores for the, cat and sat above a 3 by 3 grid of weights. Left, one table: scores 1.0 0.0 1.0, 0.0 1.0 1.0, 1.0 1.0 2.0, "
        "weights 0.422 0.155 0.422, 0.155 0.422 0.422, 0.212 0.212 0.576; cat to sat and sat to cat are both 1.0. Right, question table changed: scores 0.0 0.0 0.0, 1.0 0.0 1.0, 1.0 0.0 1.0, "
        "weights 0.333 0.333 0.333, 0.422 0.155 0.422, 0.422 0.155 0.422; cat to sat is 1.0 and sat to cat is 0.0, ringed in both panels. Largest weights in a row are ringed.", o)


# ---------------------------------------------------------------- W14-6  blank: two-token pass
def w14_6():
    o = [ctitle("Blank: a two-token pass, a and b")]
    cw, ch, gw = 60, 44, 28
    px = [20 + i * (gw + 2 * cw + 56) for i in range(4)]
    heads_ = ("1  V", "2  scores", "3  weights", "4  output")
    hints = ("values, one row each", "question against label", "each row adds to 1", "weights blend V")
    for i in range(4):
        gx = px[i] + gw
        o.append(t(px[i] + gw + cw, 100, heads_[i], 18, INK, "middle"))
        if i in (1, 2):
            for j, nm in enumerate(("a", "b")):
                o.append(t(gx + j * cw + cw / 2.0, 126, nm, 12, MUT, "middle"))
        for r, nm in enumerate(("a", "b")):
            o.append(t(gx - 8, 140 + r * ch + ch / 2.0 + 4, nm, 12, MUT, "end"))
            for c in range(2):
                o.append(sq(gx + c * cw, 140 + r * ch, cw, ch, PAPER, INK, 2))
        o.append(t(px[i] + gw + cw, 250, hints[i], 12, MUT, "middle"))
    ax = lambda i: px[i] + gw + 2 * cw
    o.append(line(ax(0) + 28, 120, ax(0) + 28, 260, GRID, 1.5, "6 4"))
    for i, lab in ((1, "softmax"), (2, "times V")):
        o.append(arrow(ax(i) + 6, 184, ax(i) + 50, 184, INK, 3))
        o.append(t(ax(i) + 28, 172, lab, 12, MUT, "middle"))
    o.append(t(20, 296, "Given:  a = [1, 0]   b = [0, 1]   Wq = Wk = [[1, 0], [0, 1]]   Wv = [[2, 0], [0, 4]]", 12, INK, "start", mono=True))
    o.append(t(20, 318, "exp(0) = 1.0000   exp(1) = 2.7183", 12, INK, "start", mono=True))
    o.append(cap("Fill every grid from your own working: weights to four places, output to three.", 372))
    fig("fig-w14-6-blank-two-token-pass", "0 0 800 400",
        "A blank worksheet: fill four empty 2 by 2 grids for a two-token attention pass",
        "Four empty 2 by 2 grids with rows a and b, headed V, scores, weights and output. A dotted line separates V from the others; arrows labelled softmax and times V join "
        "scores to weights and weights to output. The given tokens and tables are printed below: a equals 1, 0; b equals 0, 1; Wq and Wk are the identity; Wv is 2, 0 over 0, 4. All cells are empty.", o)


# ---------------------------------------------------------------- W15-4  two dials and the cut into heads
def w15_4():
    bw, gap, x0, by, bh = 132, 24, 22, 78, 60
    X = lambda i: x0 + i * (bw + gap)
    C = lambda i: X(i) + bw / 2.0
    o = [ctitle("Scores through two dials, then cut into heads")]
    for i in range(4):
        o.append(arrow(X(i) + bw + 2, by + bh / 2.0, X(i + 1) - 3, by + bh / 2.0, INK, 3))
    o.append(box(X(0), by, bw, bh, "scores", "q . k, every pair", DATA_F, DATA_S))
    o.append(box(X(1), by, bw, bh, "divide", "by root of the width", HUMAN_F, HUMAN_S))
    o.append(box(X(2), by, bw, bh, "hide future", "later words to -inf", HUMAN_F, HUMAN_S))
    o.append(box(X(3), by, bw, bh, "softmax", "each row adds to 1", DATA_F, DATA_S))
    o.append(box(X(4), by, bw, bh, "blend", "weights times V", DATA_F, DATA_S))
    o.append(t(C(1), by + bh + 18, "dial 1", 12, INK, "middle"))
    o.append(t(C(2), by + bh + 18, "dial 2", 12, INK, "middle"))
    # snippet (b) row, three chips
    cy = 196
    o.append(t(20, cy + 4, "snippet (b), row 2:", 12, MUT, "start"))
    o.append(chip(200, cy - 13, 100, "4  5  6", DATA_S))
    o.append(arrow(304, cy, 346, cy, INK, 2))
    o.append(chip(350, cy - 13, 128, "4  5  -inf", HUMAN_S))
    o.append(arrow(482, cy, 524, cy, INK, 2))
    o.append(chip(528, cy - 13, 190, "0.2689 0.7311 0.0000", DATA_S))
    o.append(t(250, cy + 30, "scores", 12, MUT, "middle"))
    o.append(t(414, cy + 30, "future hidden", 12, MUT, "middle"))
    o.append(t(623, cy + 30, "weights", 12, MUT, "middle"))
    o.append(t(20, cy + 50, "(the snippet leaves the divide out)", 12, MUT, "start"))
    # heads strip
    o.append(t(20, 276, "many heads: one word's 12 numbers cut into 3 pieces", 14, INK, "start"))
    for k in range(12):
        h = k // 4
        o.append(sq(20 + k * 28, 288, 28, 28, (DATA_F, MODEL_F, HUMAN_F)[h], (DATA_S, MODEL_S, HUMAN_S)[h], 2))
        o.append(t(34 + k * 28, 302, str(k + 1), 12, INK, "middle", central=True))
    for h in range(3):
        o.append(bracket(20 + h * 112 + 3, 20 + h * 112 + 109, 322, 7, MUT, True))
        o.append(t(20 + h * 112 + 56, 346, "head %d" % (h + 1), 12, MUT, "middle"))
    # shape chain
    for k, (sh, nm) in enumerate((("(2, 5, 12)", "= (B, T, d)"), ("(2, 5, 3, 4)", "= (B, T, H, dh)"), ("(2, 3, 5, 4)", "= (B, H, T, dh)"))):
        y = 240 + k * 42
        o.append(chip(480, y, 112, sh, DATA_S))
        o.append(t(602, y + 13, nm, 12, MUT, "start", mono=True, central=True))
    o.append(arrow(536, 268, 536, 280, INK, 2))
    o.append(t(548, 278, "view", 12, MUT, "start"))
    o.append(arrow(536, 310, 536, 322, INK, 2))
    o.append(t(548, 320, "transpose(1, 2)", 12, MUT, "start"))
    o.append(cap("Divide, then hide, then softmax: that order. Heads cut the width and add no knobs.", 372))
    fig("fig-w15-4-two-dials-and-heads", "0 0 800 400",
        "Scores are divided, the future is hidden, then softmax and blend; separately a word's width is cut into heads",
        "Top, five boxes joined by arrows: scores, divide by the root of the width labelled dial 1, hide future with later words set to minus infinity labelled dial 2, softmax, blend. "
        "Middle, snippet (b) row 2: scores 4 5 6, then 4 5 -inf with the future hidden, then weights 0.2689 0.7311 0.0000; the snippet leaves the divide out. "
        "Bottom left, a strip of 12 numbered cells cut into three heads of four. Bottom right, shapes (2, 5, 12), then view gives (2, 5, 3, 4), then transpose(1, 2) gives (2, 3, 5, 4).", o)


# ---------------------------------------------------------------- W15-5  biggest weight, raw versus divided
def w15_5():
    data = [(4, 0.573, 0.372), (16, 0.763, 0.363), (64, 0.880, 0.365)]       # scale.py last table
    x0, x1, yb, yt = 90, 740, 300, 100
    Y = lambda v: yb - v * (yb - yt)
    o = [ctitle("The biggest weight in a row of 8")]
    o.append(rect(300, 62, 14, 12, 2, BAD_F, BAD_S, 2))
    o.append(t(320, 73, "raw scores", 12, INK, "start"))
    o.append(rect(420, 62, 14, 12, 2, OK_F, OK_S, 3))
    o.append(t(440, 73, "divided by the root of d", 12, INK, "start"))
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        o.append(line(x0, Y(v), x1, Y(v), GRID, 1.5, "4 4" if v else None))
        o.append(t(x0 - 8, Y(v) + 4, ("%g" % v), 12, MUT, "end"))
    o.append(line(x0, yb, x1, yb, INK, 2))
    o.append(line(x0, yt, x0, yb, INK, 2))
    o.append(trot(40, (yb + yt) / 2.0, "average biggest weight", 12))
    o.append(line(x0, Y(0.125), x1, Y(0.125), MUT, 2, "2 5"))
    o.append(t(310, Y(0.125) - 24, "equal share", 12, MUT, "middle"))
    o.append(t(310, Y(0.125) - 9, "0.125", 12, MUT, "middle"))
    for g, (d, raw, sc) in enumerate(data):
        cx = 200 + g * 220
        o.append(rect(cx - 66, Y(raw), 62, yb - Y(raw), 2, BAD_F, BAD_S, 2))
        o.append(t(cx - 35, Y(raw) - 8, "%.3f" % raw, 14, INK, "middle"))
        o.append(rect(cx + 4, Y(sc), 62, yb - Y(sc), 2, OK_F, OK_S, 3))
        o.append(t(cx + 35, Y(sc) - 8, "%.3f" % sc, 14, INK, "middle"))
        o.append(t(cx, yb + 22, "width d = %d" % d, 14, INK, "middle"))
    o.append(cap("Raw scores let one winner take nearly all as the width grows; divided scores stay calm.", 372))
    fig("fig-w15-5-biggest-weight-by-width", "0 0 800 400",
        "Without the divide the biggest weight grows with the width and the softmax saturates; with it the biggest weight stays near 0.365",
        "Paired bars of the average biggest weight in a row of 8 scores, from scale.py. Width 4: raw 0.573, divided 0.372. Width 16: raw 0.763, divided 0.363. "
        "Width 64: raw 0.880, divided 0.365. A dotted line marks an equal share of 0.125.", o)


# ---------------------------------------------------------------- W15-6  blank: cut the width into heads
def w15_6():
    o = [ctitle("Blank: cut a width into heads")]
    o.append(t(400, 82, "B = 3 sentences, T = 4 words, d = 20 numbers per word, H = 5 heads", 14, INK, "middle"))
    for k in range(20):
        o.append(sq(40 + k * 36, 104, 36, 34, PANEL, INK, 2))
        o.append(t(58 + k * 36, 121, str(k + 1), 12, MUT, "middle", central=True))
    o.append(t(40, 164, "Draw the cuts between the cells, one head per piece.", 12, MUT, "start"))
    o.append(t(40, 204, "head width  dh = d // H =", 14, INK, "start"))
    o.append(rect(250, 188, 90, 32, 8, PAPER, INK, 2))
    o.append(t(400, 204, "knobs in the three tables  3 x d x d =", 14, INK, "start"))
    o.append(rect(650, 188, 110, 32, 8, PAPER, INK, 2))
    o.append(arrow(240, 290, 298, 290, INK, 3))
    o.append(arrow(500, 290, 558, 290, INK, 3))
    for x, lab in ((40, "after .view(B, T, H, dh)"), (300, "after .transpose(1, 2)"), (560, "shape of the score table")):
        o.append(t(x, 256, lab, 12, MUT, "start"))
        o.append(rect(x, 270, 200, 40, 10, PAPER, INK, 2))
    o.append(cap("Write each shape as a tuple of four numbers; check that H x dh equals d.", 372))
    fig("fig-w15-6-blank-heads", "0 0 800 400",
        "A blank worksheet: cut 20 numbers into 5 heads and write each shape on the way to the score table",
        "A strip of 20 numbered cells under the line B equal 3, T equal 4, d equal 20, H equal 5. Below, empty boxes for the head width dh and for the knobs in the three tables, "
        "then three empty boxes joined by arrows for the shape after view, the shape after transpose, and the shape of the score table. No answer is written.", o)


def build():
    for f in (w13_4, w13_5, w13_6, w14_4, w14_5, w14_6, w15_4, w15_5, w15_6):
        f()
    return FIGS

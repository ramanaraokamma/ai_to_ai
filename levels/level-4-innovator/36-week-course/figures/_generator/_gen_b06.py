"""Block 6 (weeks 16, 17, 18): two concept figures per week.

Every number drawn here is copied from a printed, seeded output in the same week's student guide
(or is a hand sum printed beside it). Provenance, figure by figure:

  fig-w16-1  week 16 blind.py / where.py outputs (seed 0): 'the' rows equal True/False, distance
             0.0 / 0.1529, shuffle gap 0.0 / 0.6169.
  fig-w16-2  week 16 count.py output: 16 64 64 64 72 16 288 0 264 = 848; d = 128 attention 65,664,
             MLP 131,712, one block 197,888. Shapes from block.py: (1, 6, 8).
  fig-w17-1  week 17 check_init.py output: 6,972 characters, vocab 28, x/y (32, 64), the first 24
             characters of x[0] and y[0]; 32 x 64 = 2,048 (hand product printed in the guide).
  fig-w17-2  week 17 train.py loss table (steps 0..1499) and check_init.py first-loss check
             (3.5025 / 0.1702 FAIL, 3.3481 / 0.0159 PASS, ln 28 = 3.3322). seed 0.
  fig-w18-1  week 18 warm1.py output (PRACTICE numbers, not the paper's).
  fig-w18-2  week 18 warm3.py output (PRACTICE numbers) plus V = X @ Wv by hand.
"""
import math
import os
from _gen_core import *

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # figures/
E_MINUS, E_TIMES, E_ARROW, E_INF = "&#8722;", "&#215;", "&#8594;", "&#8734;"

FIGS = {}


def fig(name, vb, title, desc, body):
    FIGS[name] = svg_doc(vb, title, desc, "\n".join("  " + b for b in body)) + "\n"


def title_t(s, cx=400):
    return t(cx, 42, s, 24, INK, "middle")


# ---------------------------------------------------------------- week 16 figure 1
def _w16_1():
    o = [title_t("Attention alone is blind to order")]
    words = ["the", "dog", "bit", "the", "postman"]
    for px, hd, col in ((20, "attention alone", BAD_S), (410, "attention + a place row", OK_S)):
        cx = px + 185
        o.append(t(cx, 82, hd, 18, INK, "middle"))
        for i, w in enumerate(words):
            x = px + 11 + i * 70
            o.append(rect(x, 96, 62, 32, 8, DATA_F, DATA_S, 2))
            o.append(t(x + 31, 112, w, 12, INK, "middle", mono=True, central=True))
            if px == 410:
                o.append(rect(x + 11, 134, 40, 24, 6, MODEL_F, MODEL_S, 2))
                o.append(t(x + 31, 146, "+ %d" % i, 12, INK, "middle", mono=True, central=True))
        if px == 20:
            o.append(t(cx, 150, "no place row added", 12, MUT, "middle"))
    # table of results
    cols = (525, 595 + 90)
    o.append(t(525, 196, "blind to order", 14, BAD_S, "middle"))
    o.append(t(685, 196, "can tell order", 14, OK_S, "middle"))
    rows = [("the two 'the' words get the same row?", "True", "False"),
            ("'dog' in a vs 'dog' in b: distance apart", "0.0", "0.1529"),
            ("shuffle-then-attend vs attend-then-shuffle: gap", "0.0", "0.6169")]
    for k, (lab, a, b) in enumerate(rows):
        y = 210 + k * 44
        o.append(line(20, y - 4, 780, y - 4, GRID, 1.5))
        o.append(t(20, y + 22, lab, 14, INK))
        for cxx, v, good in ((525, a, False), (685, b, True)):
            o.append(rect(cxx - 62, y + 4, 124, 32, 8, OK_F if good else BAD_F, OK_S if good else BAD_S, 2))
            o.append(t(cxx + 8, y + 20, v, 14, INK, "middle", mono=True, central=True))
            o.append(tick(cxx - 44, y + 20, 8) if good else cross(cxx - 44, y + 20, 6))
    o.append(line(20, 338, 780, 338, GRID, 1.5))
    o.append(t(400, 366, "5 words, width 4, output (5, 4), seed 0. Random tables: 0.1529 only means &#8220;not zero&#8221;.", 14, MUT, "middle"))
    fig("fig-w16-1-blind-then-places", "0 0 800 400",
        "Without a place row attention cannot tell order; adding one fixes it",
        "Two panels side by side showing the five words the, dog, bit, the, postman. Left, attention alone: the two 'the' "
        "words get the same row (True), the dog rows are 0.0 apart, and shuffling before or after attention differs by 0.0. "
        "Right, each word has a place row added (+0 to +4): the two 'the' rows differ (False), the dog rows are 0.1529 apart, "
        "and the shuffle gap is 0.6169. Crosses mark the blind column, ticks the column that can tell order. Seed 0.",
        o)


# ---------------------------------------------------------------- week 16 figure 2
def _w16_2():
    o = [t(250, 42, "One block, counted: 848 knobs", 24, INK, "middle")]
    cx = 240
    # connectors first
    o.append(arrow(cx, 84, cx, 104))
    o.append(path("M%d 94 H32 V330 H224" % cx, "none", INK, 2))
    o.append(head(226, 330, 0, INK, 2))
    o.append(path("M%d 355 H32 V570 H224" % cx, "none", INK, 2))
    o.append(head(226, 570, 0, INK, 2))
    o.append(arrow(cx, 142, cx, 158))
    o.append(arrow(cx, 300, cx, 316))
    o.append(arrow(cx, 344, cx, 366))
    o.append(arrow(cx, 404, cx, 420))
    o.append(arrow(cx, 540, cx, 556))
    o.append(arrow(cx, 584, cx, 602))
    o.append(t(40, 88, "residual road", 12, MUT))
    o.append(t(40, 349, "residual road", 12, MUT))
    # chips
    o.append(chip(175, 58, 130, "x (1, 6, 8)", DATA_S, DATA_F))
    o.append(chip(175, 602, 130, "out (1, 6, 8)", DATA_S, DATA_F))
    # layer norms
    for y, nm in ((104, "layer norm 1"), (366, "layer norm 2")):
        o.append(rect(75, y, 330, 38, 10, MODEL_F, MODEL_S, 3))
        o.append(t(cx, y + 19, nm + "  &#183;  16 knobs", 14, INK, "middle", central=True))
    # attention panel
    o.append(rect(50, 158, 380, 142, 12, PANEL, GRID, 2))
    o.append(t(cx, 178, "attention gathers", 18, INK, "middle"))
    for k, (nm, n) in enumerate((("q", 64), ("k", 64), ("v", 64))):
        x = 75 + k * 115
        o.append(rect(x, 190, 100, 46, 10, MODEL_F, MODEL_S, 3))
        o.append(t(x + 50, 206, nm, 14, INK, "middle", central=True))
        o.append(t(x + 50, 224, "%d" % n, 12, INK, "middle", mono=True, central=True))
    o.append(arrow(cx, 236, cx, 252))
    o.append(rect(75, 252, 330, 38, 10, MODEL_F, MODEL_S, 3))
    o.append(t(cx, 271, "proj  &#183;  72 knobs", 14, INK, "middle", central=True))
    # plus circles
    for y in (330, 570):
        o.append(circ(cx, y, 14, PAPER, INK, 3))
        o.append(t(cx, y, "+", 18, INK, "middle", central=True))
    # MLP panel
    o.append(rect(50, 420, 380, 120, 12, PANEL, GRID, 2))
    o.append(t(cx, 440, "the MLP thinks (each word alone)", 18, INK, "middle"))
    o.append(arrow(165, 485, 195, 485))
    o.append(arrow(285, 485, 315, 485))
    for x, w, nm, sh, n, fillc, strokec in ((65, 100, "up", "8 %s 32" % E_ARROW, "288", MODEL_F, MODEL_S),
                                          (195, 90, "GELU", "no weights", "0", PANEL, GRID),
                                          (315, 100, "down", "32 %s 8" % E_ARROW, "264", MODEL_F, MODEL_S)):
        o.append(rect(x, 452, w, 66, 10, fillc, strokec, 3))
        o.append(t(x + w / 2.0, 470, nm, 14, INK, "middle", central=True))
        o.append(t(x + w / 2.0, 488, sh, 12, INK, "middle", mono=True, central=True))
        o.append(t(x + w / 2.0, 506, n + " knobs", 12, INK, "middle", central=True))
    o.append(t(cx, 654, "16 + 64 + 64 + 64 + 72 + 16 + 288 + 0 + 264 = 848", 14, INK, "middle", mono=True))
    o.append(t(cx, 674, "at d = 128: MLP 131,712 of 197,888 knobs, two thirds", 14, MUT, "middle"))
    fig("fig-w16-2-one-block-knob-count", "0 0 500 700",
        "A block is attention then an MLP, each on a residual road; nine parts add to 848 knobs",
        "A top-to-bottom stack. Input x of shape (1, 6, 8) goes through layer norm 1 (16 knobs), then an attention panel with "
        "q, k, v of 64 knobs each and proj with 72, then a residual add, then layer norm 2 (16), then an MLP panel with up 288, "
        "GELU 0 and down 264, then a second residual add, and out of shape (1, 6, 8). Two residual roads run down the left. "
        "The sum 16 + 64 + 64 + 64 + 72 + 16 + 288 + 0 + 264 = 848. At d = 128 the MLP holds 131,712 of 197,888 knobs.",
        o)


# ---------------------------------------------------------------- week 17 figure 1
def _w17_1():
    x_txt = " to school with a book u"
    y_txt = "to school with a book un"
    assert len(x_txt) == len(y_txt) == 24 and y_txt[:-1] == x_txt[1:]
    o = [title_t("One window asks 64 questions at once")]
    x0, cw = 52, 29
    for r, (lab, s, yy) in enumerate((("x", x_txt, 90), ("y", y_txt, 165))):
        o.append(t(36, yy + 15, lab, 18, INK, "middle", central=True))
        for i, ch in enumerate(s):
            hi = (i == 1)
            shown = "&#183;" if ch == " " else ch
            o.append(sq(x0 + i * cw, yy, cw, 30, ACC_F if hi else DATA_F, ACC_S if hi else DATA_S, 3 if hi else 2))
            o.append(t(x0 + i * cw + cw / 2.0, yy + 15, shown, 14, INK, "middle", mono=True, central=True))
    o.append(t(x0 + 24 * cw + 6, 105, "&#8230;", 18, MUT, central=True))
    o.append(t(x0 + 24 * cw + 6, 180, "&#8230;", 18, MUT, central=True))
    cxh = x0 + 1 * cw + cw / 2.0
    o.append(arrow(cxh, 122, cxh, 160, ACC_S, 3))
    o.append(t(cxh + 14, 144, "t is followed by o", 12, MUT))
    o.append(t(x0, 218, "first 24 of 64 places  (&#183; is a space)", 12, MUT))
    o.append(t(x0 + 24 * cw, 218, "y is x moved one place left: True", 12, MUT, "end"))
    o.append(t(400, 244, "each place sees only the places before it (the mask), so one pass answers every place", 14, MUT, "middle"))
    # tiles
    def tile(x, w, l1, l2, acc=False):
        o.append(rect(x, 262, w, 60, 10, ACC_F if acc else DATA_F, ACC_S if acc else DATA_S, 4 if acc else 3))
        o.append(t(x + w / 2.0, 284, l1, 18, INK, "middle", central=True))
        o.append(t(x + w / 2.0, 307, l2, 12, INK, "middle", mono=not acc and "(" in l2, central=True))
    tile(60, 190, "64 questions", "one window")
    tile(300, 200, "32 windows", "x, y: (32, 64)")
    tile(550, 190, "2,048 questions", "every step", True)
    o.append(t(275, 292, E_TIMES, 24, INK, "middle", central=True))
    o.append(t(525, 292, "=", 24, INK, "middle", central=True))
    o.append(t(400, 360, "corpus: 6,972 characters, 28 different; train 6,274, validation 698; 32 %s 64 = 2,048" % E_TIMES, 14, MUT, "middle"))
    fig("fig-w17-1-one-window-many-questions", "0 0 800 400",
        "Shifting the window one place gives a next-character answer at every place: 32 windows of 64 is 2,048 questions per step",
        "Two rows of 24 character cells. Row x reads ' to school with a book u' and row y reads 'to school with a book un', "
        "which is x moved one place left, so each y cell is the character that followed the x cell above it. The second cell "
        "is highlighted: t is followed by o. Below, 64 questions per window times 32 windows equals 2,048 questions each step; "
        "x and y both have shape (32, 64). The corpus has 6,972 characters and 28 different ones.",
        o)


# ---------------------------------------------------------------- week 17 figure 2
def _w17_2():
    steps = [0, 300, 500, 750, 1000, 1250, 1499]
    tr = [3.349, 1.873, 1.558, 1.181, 0.999, 0.905, 0.894]
    va = [3.351, 1.892, 1.647, 1.470, 1.417, 1.427, 1.437]
    X = lambda s: 70 + s * 330 / 1500.0
    Y = lambda l: 300 - 55 * l
    o = [title_t("Loss falls, then the gap opens (seed 0)")]
    # grid + axes
    for v in range(0, 5):
        o.append(line(70, Y(v), 400, Y(v), GRID, 1.5))
        o.append(t(62, Y(v), str(v), 12, MUT, "end", central=True))
    for s in (0, 500, 1000, 1500):
        o.append(t(X(s), 320, str(s), 12, MUT, "middle"))
    o.append(t(235, 342, "training step", 12, MUT, "middle"))
    o.append(trot(34, 190, "loss", 12))
    # ln 28 line
    o.append(line(70, Y(3.3322), 400, Y(3.3322), MUT, 2, "6 4"))
    o.append(t(130, Y(3.3322) - 8, "ln 28 = 3.332: knows nothing", 12, MUT))
    # curves
    o.append(poly([(X(s), Y(v)) for s, v in zip(steps, va)], "none", HUMAN_S, 3, "6 4"))
    o.append(poly([(X(s), Y(v)) for s, v in zip(steps, tr)], "none", DATA_S, 3))
    for s, a, b in zip(steps, tr, va):
        o.append(mark("square", X(s), Y(b), 5, HUMAN_S, PAPER))
        o.append(mark("circle", X(s), Y(a), 5, DATA_S, PAPER))
    # gap bracket + labels
    o.append(path("M404 %s H408 V%s H404" % (f2(Y(1.437)), f2(Y(0.894))), "none", MUT, 1.5))
    o.append(t(414, Y(1.437) - 2, "val 1.437", 12, HUMAN_S))
    o.append(t(414, (Y(1.437) + Y(0.894)) / 2.0 + 4, "gap 0.543", 12, INK))
    o.append(t(414, Y(0.894) + 11, "train 0.894", 12, DATA_S))
    # first-loss check panel
    o.append(rect(520, 66, 260, 270, 12, PANEL, GRID, 2))
    o.append(t(650, 92, "first-loss check", 18, INK, "middle"))
    o.append(t(650, 112, "distance of the first loss", 12, MUT, "middle"))
    o.append(t(650, 127, "from ln(28) = 3.3322", 12, MUT, "middle"))
    zx = 540
    o.append(line(zx + 50, 138, zx + 50, 300, MUT, 1.5, "6 4"))
    o.append(t(zx + 50, 316, "bar 0.05", 12, MUT, "middle"))
    for k, (nm, first, dist, good) in enumerate((("calm_head=False", "3.5025", 0.1702, False),
                                                 ("calm_head=True", "3.3481", 0.0159, True))):
        y = 146 + k * 78
        o.append(t(zx, y + 8, nm, 12, INK, mono=True))
        o.append(cross(zx + 128, y + 4, 5) if not good else tick(zx + 128, y + 4, 7))
        o.append(t(zx + 140, y + 8, "PASS" if good else "FAIL", 12, OK_S if good else BAD_S, mono=True))
        o.append(rect(zx, y + 16, max(dist * 1000, 3), 22, 4, OK_F if good else BAD_F, OK_S if good else BAD_S, 2))
        o.append(t(zx + max(dist * 1000, 3) + 8, y + 31, "%.4f" % dist, 12, INK, mono=True))
        o.append(t(zx, y + 56, "first loss " + first, 12, MUT))
    o.append(t(400, 372, "one seed, one text, one machine: consistent with memorising, not proof", 14, MUT, "middle"))
    fig("fig-w17-2-loss-gap-and-first-check", "0 0 800 400",
        "Training loss keeps falling while validation flattens, and a calm output layer passes the first-loss check",
        "Left chart: loss against training step, 0 to 1,499, with a dashed line at ln 28 = 3.332. Training loss (solid, circles) "
        "goes 3.349, 1.873, 1.558, 1.181, 0.999, 0.905, 0.894 at steps 0, 300, 500, 750, 1000, 1250, 1499. Validation loss (dashed, "
        "squares) goes 3.351, 1.892, 1.647, 1.470, 1.417, 1.427, 1.437. The final gap is 0.543. Right panel: with calm_head=False "
        "the first loss is 3.5025, 0.1702 from ln 28, FAIL; with calm_head=True it is 3.3481, 0.0159 away, PASS; the bar is 0.05.",
        o)


# ---------------------------------------------------------------- week 18 figure 1
def _w18_1():
    o = [title_t("Near 1, small differences compound")]
    o.append(t(205, 82, "a slope multiplied 30 times", 18, INK, "middle"))
    L = lambda v: 50 + (math.log10(v) + 1) * 320 / 3.0
    o.append(line(L(1), 104, L(1), 280, MUT, 1.5, "6 4"))
    o.append(t(L(1), 100, "1 = unchanged", 12, MUT, "middle"))
    # row A: fading
    o.append(t(50, 134, "0.95 times itself, 30 times", 14, INK))
    o.append(rect(L(0.2146), 142, L(1) - L(0.2146), 28, 4, BAD_F, BAD_S, 2))
    o.append(t(L(0.2146) - 6, 156, "0.2146", 14, INK, "end", mono=True, central=True))
    o.append(t(50, 192, "fading: clipping cannot cure it", 12, MUT))
    # row B: blowing up
    o.append(t(50, 218, "1.10 times itself, 30 times", 14, INK))
    o.append(rect(L(1), 226, L(17.45) - L(1), 28, 4, BAD_F, BAD_S, 3))
    o.append(t(L(17.45) + 6, 240, "17.45", 14, INK, mono=True, central=True))
    o.append(t(50, 272, "", 12, MUT))
    o.append(t(L(1) + 8, 272, "blowing up: clipping can cure it", 12, MUT))
    o.append(line(50, 286, 370, 286, INK, 1.5))
    for v, lab in ((0.1, "0.1"), (1, "1"), (10, "10"), (100, "100")):
        o.append(line(L(v), 286, L(v), 292, INK, 1.5))
        o.append(t(L(v), 308, lab, 12, MUT, "middle"))
    o.append(t(210, 328, "what is left (log scale)", 12, MUT, "middle"))
    # right: forget dial
    o.append(t(595, 82, "a forget dial, 8 steps", 18, INK, "middle"))
    W = 330
    rows = [(0, "0.5", 0.00391, "0.00391"), (1, "0.7311", 0.08159, "0.08159"), (3, "0.9526", 0.67794, "0.67794")]
    for k, (b, dial, left, ltxt) in enumerate(rows):
        y = 104 + k * 62
        hi = (b == 3)
        o.append(t(430, y + 12, "bias %d: dial %s" % (b, dial), 14, INK))
        o.append(rect(430, y + 20, max(left * W, 3), 26, 4, ACC_F if hi else DATA_F, ACC_S if hi else DATA_S, 4 if hi else 2))
        o.append(t(430 + max(left * W, 3) + 8, y + 33, ltxt, 14, INK, mono=True, central=True))
    o.append(line(430, 296, 760, 296, INK, 1.5))
    for v in (0, 0.5, 1):
        o.append(line(430 + v * W, 296, 430 + v * W, 302, INK, 1.5))
        o.append(t(430 + v * W, 318, "%g" % v, 12, MUT, "middle"))
    o.append(t(595, 338, "share of the signal left after 8 steps", 12, MUT, "middle"))
    o.append(t(400, 372, "Practice numbers, not the paper's: near 1, small differences compound.", 14, MUT, "middle"))
    fig("fig-w18-1-compounding-and-dials", "0 0 800 400",
        "A slope just below or above 1 compounds into fading or blowing up, and a bigger forget bias keeps the signal",
        "Left, a log-scale bar chart of what is left after multiplying a slope by itself 30 times: 0.95 gives 0.2146, below the "
        "1 = unchanged line (fading, clipping cannot cure it); 1.10 gives 17.45, above it (blowing up, clipping can cure it). "
        "Right, a linear bar chart of the share left after 8 steps for a forget dial: bias 0 (dial 0.5) leaves 0.00391, bias 1 "
        "(dial 0.7311) leaves 0.08159, bias 3 (dial 0.9526) leaves 0.67794, ringed. Practice numbers, not the paper's.",
        o)


# ---------------------------------------------------------------- week 18 figure 2
def _w18_2():
    W = [[1.0, 0.0, 0.0], [0.3302, 0.6698, 0.0], [0.2483, 0.5035, 0.2483]]
    toks = ["cat", "sat", "down"]
    o = [title_t("A practice attention pass, by hand then by machine")]
    o.append(t(400, 68, "practice numbers (not the paper's): cat, sat, down; width d = 2", 14, MUT, "middle"))
    x0, y0, cw, ch = 110, 140, 70, 70
    o.append(t(x0 + 1.5 * cw, 100, "key (being looked at)", 14, MUT, "middle"))
    for j, tk in enumerate(toks):
        o.append(t(x0 + j * cw + cw / 2.0, 130, tk, 14, INK, "middle", mono=True))
    for i, tk in enumerate(toks):
        o.append(t(x0 - 10, y0 + i * ch + ch / 2.0, tk, 14, INK, "end", mono=True, central=True))
    o.append(trot(36, y0 + 1.5 * ch, "query (asking)", 14))
    for i, row in enumerate(W):
        m = max(row)
        for j, v in enumerate(row):
            gx, gy = x0 + j * cw, y0 + i * ch
            if j > i:
                o.append(sq(gx, gy, cw, ch, PANEL, GRID, 2))
                o.append(line(gx + 8, gy + 8, gx + cw - 8, gy + ch - 8, GRID, 2))
                o.append(t(gx + cw / 2.0, gy + ch / 2.0 + 22, E_MINUS + E_INF, 12, MUT, "middle"))
            else:
                f, s, w = cell_tint(v, m)
                o.append(sq(gx, gy, cw, ch, f, s, w))
                o.append(t(gx + cw / 2.0, gy + ch / 2.0, "%.4f" % v, 14, INK, "middle", mono=True, central=True))
        o.append(t(x0 + 3 * cw + 8, y0 + i * ch + ch / 2.0, "sum 1.0", 12, MUT, central=True))
    # right: the blend for the third row
    o.append(t(605, 100, "down blends the values", 18, INK, "middle"))
    vs = [("cat", "2, 2", "0.2483"), ("sat", "4, 1", "0.5035"), ("down", "2, 0", "0.2483")]
    for k, (nm, vv, wt) in enumerate(vs):
        y = 150 + k * 55
        o.append(line(624, y, 636, y, INK, 2))
    o.append(line(636, 150, 636, 260, INK, 2))
    o.append(arrow(636, 205, 662, 205))
    for k, (nm, vv, wt) in enumerate(vs):
        y = 150 + k * 55
        o.append(rect(430, y - 16, 70, 32, 8, ACC_F if k == 1 else DATA_F, ACC_S if k == 1 else DATA_S, 4 if k == 1 else 2))
        o.append(t(465, y, wt, 14, INK, "middle", mono=True, central=True))
        o.append(t(512, y, E_TIMES, 18, INK, "middle", central=True))
        o.append(rect(524, y - 16, 100, 32, 8, DATA_F, DATA_S, 2))
        o.append(t(574, y, "%s (%s)" % (nm, vv), 14, INK, "middle", mono=True, central=True))
    o.append(rect(664, 178, 116, 54, 10, ACC_F, ACC_S, 3))
    o.append(t(722, 196, "output", 14, INK, "middle", central=True))
    o.append(t(722, 216, "3.007, 1.0", 14, INK, "middle", mono=True, central=True))
    o.append(t(430, 305, "weights (3, 3) %s values (3, 2)" % E_TIMES, 12, MUT, mono=True))
    o.append(t(430, 323, "%s output (3, 2)" % E_ARROW, 12, MUT, mono=True))
    # legend
    o.append(sq(20, 354, 14, 14, ACC_F, ACC_S, 3))
    o.append(t(40, 361, "largest in its row (ringed)", 12, INK, central=True))
    o.append(sq(250, 354, 14, 14, DATA_F, GRID, 2))
    o.append(t(270, 361, "0.10 or more", 12, INK, central=True))
    o.append(sq(374, 354, 14, 14, PANEL, GRID, 2))
    o.append(t(394, 361, "future hidden: score %s%s before the softmax" % (E_MINUS, E_INF), 12, INK, central=True))
    fig("fig-w18-2-practice-attention-pass", "0 0 800 400",
        "A causal attention pass turns scores into weights that sum to 1, then blends the value rows",
        "Left, a 3 by 3 grid of attention weights, query rows by key columns, for cat, sat, down. Row cat: 1.0 then two hidden "
        "cells. Row sat: 0.3302, 0.6698, hidden. Row down: 0.2483, 0.5035, 0.2483. Each row sums to 1.0; the largest in each row "
        "is ringed. Right, the third row blends the value rows cat (2, 2), sat (4, 1) and down (2, 0) with those weights into the "
        "output (3.007, 1.0). Practice numbers, not the paper's.",
        o)


def build():
    FIGS.clear()
    _w16_1(); _w16_2(); _w17_1(); _w17_2(); _w18_1(); _w18_2()
    return dict((k + ".svg", v) for k, v in FIGS.items())


def emit():
    figs = build()
    for name, svg in figs.items():
        open(os.path.join(HERE, name), "w").write(svg)
    return len(figs)


if __name__ == "__main__":
    print("block 6 figures written:", emit())

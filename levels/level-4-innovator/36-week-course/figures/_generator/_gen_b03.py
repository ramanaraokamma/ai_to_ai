"""Block 3 (weeks 7, 8, 9) concept figures. Numbers are copied from the weeks' printed outputs:

W7  hook.py   seed 0/1/2 final val loss 0.0367 / 0.0499 / 0.0301 ; table.py baseline 0.039 +/- 0.008,
              dropout 0.3 = 0.043 +/- 0.013, lr 1e-4 = 0.079 +/- 0.012 (gap and 2 x spread are hand sums)
W8  bag.py    bag [2, 1, 1, 1] for both sentences, 120 orderings; hand.py pre/h values and shapes
W9  the paper: marks 20/16/12/15/12 = 75, minutes 15/15/12/15/13 = 70; homework 30+5+5+5 = 45 min
"""
from _gen_core import *

FIGS = {}


def fig(name, vb, title, desc, parts):
    FIGS[name] = svg_doc(vb, title, desc, J(*parts))


def ctitle(s):
    return t(400, 44, s, 24, INK, "middle")


def cap(s, y=378):
    return t(400, y, s, 14, MUT, "middle")


# ---------------------------------------------------------------- W7-1
def w07_1():
    o = [ctitle("Same code, same data: only the seed changes")]
    x0, base, top = 90, 320, 110       # axis origin, baseline y, y of 0.06
    sc = (base - top) / 0.06
    o.append(trot(50, 215, "final validation loss", 12))
    for v in (0, 0.02, 0.04, 0.06):
        y = base - v * sc
        o.append(line(x0, y, 470, y, GRID, 1.5))
        o.append(t(x0 - 8, y + 4, "%.2f" % v, 12, MUT, "end"))
    vals = [(0, 0.0367), (1, 0.0499), (2, 0.0301)]
    for i, (s, v) in enumerate(vals):
        bx = 120 + i * 115
        hh = v * sc
        hi = (s == 1)
        o.append(sq(bx, base - hh, 80, hh, DATA_F, DATA_S, 3))
        o.append(t(bx + 40, base - hh - 8, "%.4f" % v, 14, INK, "middle"))
        o.append(t(bx + 40, base + 22, "seed %d" % s, 14, INK, "middle"))
    # bracket between largest and smallest
    ysm, ybg = base - 0.0301 * sc, base - 0.0499 * sc
    o.append(line(470, ybg, 482, ybg, ACC_S, 2))
    o.append(line(470, ysm, 482, ysm, ACC_S, 2, "4 3"))
    o.append(line(482, ybg, 482, ysm, ACC_S, 2))
    # right panel
    o.append(rect(520, 90, 260, 250, 12, PANEL, GRID, 2))
    o.append(t(650, 122, "What the three runs say", 18, INK, "middle"))
    o.append(t(650, 160, "0.0499 is about", 14, INK, "middle"))
    o.append(t(650, 200, "66% bigger", 24, ACC_S, "middle"))
    o.append(t(650, 224, "than 0.0301", 14, INK, "middle"))
    o.append(line(540, 244, 760, 244, GRID, 1.5))
    o.append(t(650, 272, "mean over 3 seeds", 14, MUT, "middle"))
    o.append(t(650, 302, "0.039 &#177; 0.008", 18, INK, "middle"))
    o.append(t(650, 326, "this &#177; is the spread", 12, MUT, "middle"))
    o.append(cap("A seed is a knob you did not mean to turn: measure its wobble before you read any knob.", 372))
    fig("fig-w07-1-same-code-three-seeds.svg", "0 0 800 400",
        "Before you compare two runs, measure how much the seed alone moves the result",
        "Three bars of final validation loss for the identical baseline run: seed 0 is 0.0367, seed 1 is 0.0499 "
        "and seed 2 is 0.0301, on an axis from 0 to 0.06. A bracket joins the tallest and shortest bar; the panel "
        "on the right says 0.0499 is about 66% bigger than 0.0301 and that the mean over 3 seeds is 0.039 plus or "
        "minus a spread of 0.008.", o)


# ---------------------------------------------------------------- W7-2
def w07_2():
    o = [ctitle("Is the gap bigger than twice the spread?")]
    x0, sc = 300, 5000.0   # 0.05 -> 250px
    rows = [("dropout 0.3", "0.043 &#8722; 0.039", 0.004, "2 &#215; 0.013", 0.026, False),
            ("lr 1e-4", "0.079 &#8722; 0.039", 0.040, "2 &#215; 0.012", 0.024, True)]
    for r, (name, sub, gap, sub2, thr, worse) in enumerate(rows):
        y = 76 + r * 124
        o.append(rect(20, y, 760, 112, 12, PANEL, GRID, 2))
        o.append(t(36, y + 34, name, 18, INK))
        o.append(t(36, y + 58, "this row vs baseline", 12, MUT))
        o.append(t(36, y + 80, "baseline 0.039 &#177; 0.008", 12, MUT))
        # gap bar
        o.append(t(x0 - 8, y + 36, "gap", 14, INK, "end"))
        o.append(sq(x0, y + 22, gap * sc, 24, DATA_F, DATA_S, 2))
        o.append(t(x0 + gap * sc + 8, y + 39, "%s = %.3f" % (sub, gap), 12, INK))
        # threshold bar
        o.append(t(x0 - 8, y + 80, "2 &#215; spread", 14, INK, "end"))
        o.append(sq(x0, y + 66, thr * sc, 24, HUMAN_F, HUMAN_S, 2))
        o.append(t(x0 + thr * sc + 8, y + 83, "%s = %.3f" % (sub2, thr), 12, INK))
        # verdict
        vx = 700
        if worse:
            o.append(badge_cross(vx - 20, y + 4, 0.5))
            o.append(t(vx + 6, y + 88, "WORSE", 18, BAD_S, "middle"))
            o.append(t(vx + 6, y + 108, "0.040 &gt; 0.024", 12, MUT, "middle"))
        else:
            o.append(rect(vx - 44, y + 22, 100, 32, 8, PAPER, GRID, 2, "6 4"))
            o.append(t(vx + 6, y + 39, "inside noise", 14, MUT, "middle", central=True))
            o.append(t(vx + 6, y + 88, "0.004 &lt; 0.026", 12, MUT, "middle"))
    o.append(cap("A habit we chose, not a theorem: with 3 seeds we could not show a difference.", 372))
    fig("fig-w07-2-gap-versus-twice-spread.svg", "0 0 800 400",
        "A difference counts only when the gap is bigger than twice the larger spread",
        "Two worked rows from the Week 7 table, each with a blue gap bar above a gold twice-the-spread bar on the "
        "same scale. Dropout 0.3: gap 0.043 minus 0.039 is 0.004, twice the larger spread 2 times 0.013 is 0.026, "
        "so the gap is shorter and the verdict is inside noise. Learning rate 1e-4: gap 0.079 minus 0.039 is 0.040, "
        "twice the larger spread 2 times 0.012 is 0.024, so the gap is longer and the verdict is WORSE, marked with a cross.", o)


# ---------------------------------------------------------------- W8-1
def w08_1():
    o = [ctitle("A bag keeps the counts and throws the order away")]
    sents = [("a", ["the", "dog", "bit", "the", "postman"]), ("b", ["the", "postman", "bit", "the", "dog"])]
    wds = {"the": 56, "dog": 56, "bit": 52, "postman": 96}
    bagx = 540
    for r, (nm, ws) in enumerate(sents):
        y = 100 + r * 96
        x = 30
        o.append(t(x, y - 8, "sentence %s (5 words)" % nm, 12, MUT))
        for w in ws:
            bw = wds[w]
            o.append(rect(x, y, bw, 40, 8, DATA_F, DATA_S, 3))
            o.append(t(x + bw / 2.0, y + 20, w, 14, INK, "middle", central=True))
            x += bw + 8
        o.append(arrow(x + 4, y + 20, bagx - 14, y + 20, INK, 3))
    # bag table
    vocab = ["the", "dog", "bit", "postman"]
    counts = [2, 1, 1, 1]
    cw = 50
    for i, w in enumerate(vocab):
        o.append(t(bagx + i * cw + cw / 2.0, 92, w if w != "postman" else "postman", 12, MUT, "middle"))
    for r in range(2):
        y = 100 + r * 96
        for i, c in enumerate(counts):
            o.append(sq(bagx + i * cw, y, cw, 40, PANEL if c == 1 else DATA_F, DATA_S, 2))
            o.append(t(bagx + i * cw + cw / 2.0, y + 20, str(c), 18, INK, "middle", central=True))
    # equality bracket on right
    o.append(path("M%s 120 H%s V216 H%s" % (bagx + 4 * cw + 6, bagx + 4 * cw + 18, bagx + 4 * cw + 6), "none", ACC_S, 3))
    o.append(t(bagx + 4 * cw + 24, 172, "=", 24, ACC_S, central=True))
    o.append(t(bagx + 2 * cw, 282, "bag of a = bag of b: [2, 1, 1, 1]", 14, INK, "middle"))
    o.append(rect(30, 300, 340, 60, 10, PANEL, GRID, 2))
    o.append(t(200, 324, "same bag?  True      same text?  False", 14, INK, "middle", mono=True))
    o.append(t(200, 346, "5 different words: 120 orderings, 1 bag", 14, INK, "middle"))
    o.append(rect(420, 300, 350, 60, 10, PAPER, MODEL_S, 2))
    o.append(t(595, 324, "Whatever classifier comes next sees one row:", 14, INK, "middle"))
    o.append(t(595, 346, "the order is gone before it starts.", 14, INK, "middle"))
    fig("fig-w08-1-same-bag-different-order.svg", "0 0 800 400",
        "Counting words erases word order, so two different sentences give a classifier the same row",
        "Two sentences of five blue word boxes: 'the dog bit the postman' and 'the postman bit the dog'. An arrow from "
        "each leads to a bag row over the vocabulary the, dog, bit, postman. Both rows read 2, 1, 1, 1 and a bracket "
        "marks them as equal. Below: same bag is True, same text is False, and five different words can be ordered "
        "120 ways that all give one bag.", o)


# ---------------------------------------------------------------- W8-2
def w08_2():
    o = [ctitle("A cell reads one word at a time, with the same weights")]
    xs = [1, 0, 0, 0]
    pre = ["1.0000", "0.3808", "0.1817", "0.0899"]
    hs = ["0.7616", "0.3634", "0.1797", "0.0896"]
    hv = [0.7616, 0.3634, 0.1797, 0.0896]
    cx0, step, cw = 100, 150, 100
    cy, ch = 140, 70
    # shared weights band and ticks (connectors first)
    for i in range(4):
        c = cx0 + i * step + cw / 2.0
        o.append(line(c, cy + ch, c, 238, GRID, 1.5, "4 3"))
    o.append(rect(cx0, 238, 3 * step + cw, 30, 8, PANEL, MODEL_S, 2))
    o.append(t(cx0 + (3 * step + cw) / 2.0, 253, "SAME weights in all four boxes: W_xh = 1.0, W_hh = 0.5", 12, INK, "middle", central=True))
    # h0 and chain arrows
    o.append(t(52, cy + ch / 2.0 - 14, "h0", 12, MUT, "middle"))
    o.append(rect(30, cy + ch / 2.0 - 8, 44, 28, 6, DATA_F, DATA_S, 2))
    o.append(t(52, cy + ch / 2.0 + 6, "0", 14, INK, "middle", central=True))
    o.append(arrow(80, cy + ch / 2.0 + 6, cx0 - 4, cy + ch / 2.0 + 6, INK, 3))
    for i in range(4):
        x = cx0 + i * step
        # input
        o.append(rect(x + 25, 66, 50, 30, 8, DATA_F, DATA_S, 3))
        o.append(t(x + 50, 81, "x%d = %d" % (i + 1, xs[i]), 12, INK, "middle", central=True))
        o.append(arrow(x + 50, 98, x + 50, cy - 3, INK, 2))
        o.append(rect(x, cy, cw, ch, 10, MODEL_F, MODEL_S, 3))
        o.append(t(x + 50, cy + 24, "CELL", 18, INK, "middle", central=True))
        o.append(t(x + 50, cy + 50, "pre " + pre[i], 12, INK, "middle", mono=True, central=True))
        if i < 3:
            o.append(arrow(x + cw + 2, cy + ch / 2.0 + 6, x + step - 4, cy + ch / 2.0 + 6, INK, 3))
            o.append(t(x + cw + 30, cy + ch / 2.0 - 2, "h%d" % (i + 1), 12, MUT, "middle"))
        # bar of the note
        bh = hv[i] * 60
        o.append(sq(x + 25, 336 - bh, 50, bh, DATA_F, DATA_S, 2))
        o.append(t(x + 50, 352, "h%d = %s" % (i + 1, hs[i]), 12, INK, "middle", mono=True))
    last = cx0 + 3 * step + cw
    o.append(arrow(last + 2, cy + ch / 2.0 + 6, last + 38, cy + ch / 2.0 + 6, ACC_S, 3))
    o.append(rect(last + 40, cy + 8, 78, 56, 8, ACC_F, ACC_S, 3))
    o.append(t(last + 79, cy + 26, "summary", 12, INK, "middle", central=True))
    o.append(t(last + 79, cy + 46, "h4", 14, INK, "middle", central=True))
    o.append(shape_chip(660, 290, "x (1, 4, 1)"))
    o.append(shape_chip(660, 320, "out (1, 4, 1)"))
    o.append(shape_chip(660, 350, "h_n (1, 1, 1)"))
    o.append(cap("The spike fades: about half is lost at each step. Weights are typed in, not learned.", 374))
    fig("fig-w08-2-unrolled-cell-four-steps.svg", "0 0 800 400",
        "One recurrent cell is reused at every step, passing a note forward that fades",
        "Four purple cell boxes in a row, one per word, with the inputs x = 1, 0, 0, 0 above them and the starting note "
        "h0 = 0 entering from the left. The notes passed between them are h1 = 0.7616, h2 = 0.3634, h3 = 0.1797 and "
        "h4 = 0.0896, and the pre-squash values inside the cells are 1.0000, 0.3808, 0.1817 and 0.0899. A band beneath "
        "says the same weights W_xh = 1.0 and W_hh = 0.5 are used in all four boxes. Bars below show the note shrinking. "
        "Shapes: x is (1, 4, 1), out is (1, 4, 1), h_n is (1, 1, 1).", o)


# ---------------------------------------------------------------- W9-1
def w09_1():
    o = [ctitle("The paper: 75 marks in 70 minutes")]
    secs = [("A", 20, 15, "20 multiple", "choice"), ("B", 16, 15, "8 'what does", "this print?'"),
            ("C", 12, 12, "4 find", "the bug"), ("D", 15, 15, "3 pieces of", "arithmetic"),
            ("E", 12, 13, "1 question on", "real loss curves")]
    sc_m, sc_t = 720 / 75.0, 720 / 70.0
    x = 40
    o.append(t(40, 92, "marks (75)", 14, INK))
    for s, m, mn, a, b in secs:
        w = m * sc_m
        o.append(rect(x, 100, w, 56, 8, ACC_F if s == "E" else HUMAN_F, ACC_S if s == "E" else HUMAN_S, 4 if s == "E" else 3))
        o.append(t(x + w / 2.0, 120, "%s  %d" % (s, m), 18, INK, "middle", central=True))
        o.append(t(x + w / 2.0, 142, "marks", 12, INK, "middle", central=True))
        x += w
    x = 40
    o.append(t(40, 206, "minutes (70)", 14, INK))
    for s, m, mn, a, b in secs:
        w = mn * sc_t
        o.append(rect(x, 214, w, 56, 8, DATA_F, DATA_S, 3))
        o.append(t(x + w / 2.0, 234, "%s  %d" % (s, mn), 18, INK, "middle", central=True))
        o.append(t(x + w / 2.0, 256, "min", 12, INK, "middle", central=True))
        x += w
    # what each asks: aligned to minutes band
    x = 40
    for s, m, mn, a, b in secs:
        w = mn * sc_t
        o.append(t(x + w / 2.0, 296, a, 12, INK, "middle"))
        o.append(t(x + w / 2.0, 312, b, 12, INK, "middle"))
        x += w
    o.append(rect(40, 334, 720, 36, 8, PANEL, ACC_S, 2))
    o.append(t(400, 357, "E is the biggest single question: start it with about 13 minutes left.", 14, INK, "middle"))
    fig("fig-w09-1-the-paper-marks-and-minutes.svg", "0 0 800 400",
        "Where the 75 marks and 70 minutes go, and why Section E needs its own 13 minutes",
        "Two bars with the same five sections A to E. The gold marks bar has widths 20, 16, 12, 15 and 12 marks, "
        "totalling 75. The blue minutes bar has 15, 15, 12, 15 and 13 minutes, totalling 70. Beneath each is what it "
        "asks: 20 multiple choice, 8 what-does-this-print, 4 find-the-bug, 3 arithmetic, and 1 question on real loss "
        "curves. Section E is outlined in pink with a note to start it with about 13 minutes left.", o)


# ---------------------------------------------------------------- W9-2
def w09_2():
    o = [ctitle("Mark it, grid it, circle at most two weeks")]
    steps = [("1. Mark", "other colour", "about 30 min"), ("2. Grid", "marks per week", "about 5 min"),
             ("3. Circle", "at most two", "about 5 min"), ("4. Bug Log", "one sentence", "about 5 min")]
    for i, (a, b, c) in enumerate(steps):
        x = 40 + i * 185
        if i < 3:
            o.append(arrow(x + 150, 98, x + 180, 98, INK, 3))
    for i, (a, b, c) in enumerate(steps):
        x = 40 + i * 185
        o.append(rect(x, 64, 150, 70, 10, HUMAN_F, HUMAN_S, 3))
        o.append(t(x + 75, 88, a, 18, INK, "middle", central=True))
        o.append(t(x + 75, 108, b, 12, INK, "middle", central=True))
        o.append(t(x + 75, 124, c, 12, INK, "middle", central=True))
    o.append(t(40, 172, "The eight weeks on the grid; a week needs a redo when it scores under 60% of its marks", 14, INK))
    tie = {8: 1, 2: 2, 6: 3}
    for w in range(1, 9):
        x = 40 + (w - 1) * 90
        hit = w in tie
        o.append(rect(x, 190, 78, 70, 8, ACC_F if hit else DATA_F, ACC_S if hit else DATA_S, 4 if hit else 2))
        o.append(t(x + 39, 212, "Week", 12, INK, "middle", central=True))
        o.append(t(x + 39, 238, str(w), 24, INK, "middle", central=True))
        if hit:
            o.append(ring_num(x + 66, 192, tie[w]))
    o.append(t(40, 290, "Tie-break order when marks are equal: ringed 1, 2, 3 are Week 8, then Week 2, then Week 6.", 12, MUT))
    o.append(rect(40, 304, 720, 60, 10, PANEL, GRID, 2))
    o.append(t(400, 326, "Week 10 is entirely about the Week 8 cell and leans on Week 2.", 14, INK, "middle"))
    o.append(t(400, 348, "Each redo is 20 minutes, then one question out loud. Total homework: 30 + 5 + 5 + 5 = 45 min.", 12, MUT, "middle"))
    fig("fig-w09-2-redo-rule-at-most-two.svg", "0 0 800 400",
        "The review turns marks into a plan of at most two redos, with a fixed tie-break",
        "Top row, four gold step boxes joined by arrows: 1 mark in another colour (about 30 minutes), 2 fill the "
        "per-week grid (5), 3 circle at most two weeks (5), 4 one Bug Log sentence (5), totalling 45 minutes. Middle row, "
        "eight blue boxes for Weeks 1 to 8; Weeks 8, 2 and 6 are pink with ringed numbers 1, 2 and 3 for the tie-break "
        "order. Below: a week needs a redo when it scores under 60 percent; Week 10 is about the Week 8 cell and leans on Week 2. "
        "No student scores are shown because none are measured.", o)


def build():
    for f in (w07_1, w07_2, w08_1, w08_2, w09_1, w09_2):
        f()
    return FIGS

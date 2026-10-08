"""Block C7 (weeks 19, 20, 21) extra figures: a mental-model figure, a worked-numbers figure and a
blank workbook figure per week. Every number is copied from the week's printed output or is a
hand sum printed beside it (STYLE.md 2.1).

W19  student-guide/week-19.md section 4-5 (text_ablate.py: five models, seed 0, 800 steps, the table
     and its subtraction line) and section 6 (leak_test.py); the blank is workbook page 19.3, the
     4-symbol copy task (9 tokens, 8 places), nothing marked
W20  student-guide/week-20.md Start Here (the sentence, 31 characters), section 9 (the piece list
     printed for 'the baker practised the cricket') and the cost.py table; the blank is workbook
     page 20.2 Part B (the class card the x5 then x2 than x2 hat x3), nothing filled in
W21  student-guide/week-21.md section 1 (powerlaw.py), section 10 (fit.py: off by -1.4 +3.1 -2.1 +0.4),
     section 11 (check.py: 1.2654 predicted, 1.4656 measured, +15.8%) and the flops.py table
     (measured / predicted seconds; these vary run to run and by machine); the blank is workbook
     page 21.5 Part B1 (the chapter's Fingerprint card), nothing ticked
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


def box(x, y, w, h, l1, l2=None, fill=DATA_F, stroke=DATA_S, sw=2, dash=None, mono1=True):
    o = [rect(x, y, w, h, 8, fill, stroke, sw, dash)]
    if l2:
        o.append(t(x + w / 2.0, y + h / 2.0 - 9, l1, 14, INK, "middle", mono=mono1, central=True))
        o.append(t(x + w / 2.0, y + h / 2.0 + 11, l2, 12, MUT, "middle", central=True))
    else:
        o.append(t(x + w / 2.0, y + h / 2.0, l1, 14, INK, "middle", mono=mono1, central=True))
    return "\n  ".join(o)


# ---------------------------------------------------------------- W19-4  delete one part, hold the rest
def w19_4():
    PARTS = ["mask_on", "pos_on", "res_on", "ln_on"]                       # ablate_model.py switches
    NAMES = ["no mask", "no positions", "no residual", "no norm"]
    o = [ctitle("Ablation: delete one part, change nothing else")]
    o.append(rect(20, 70, 170, 240, 12, PANEL, GRID, 2))
    o.append(t(105, 92, "full TinyGPT", 14, INK, "middle"))
    for i, p in enumerate(PARTS):
        cy = 130 + i * 58
        o.append(chip(40, cy - 16, 130, p, DATA_S, PAPER, 12, 32))
        o.append(arrow(176, cy, 226, cy, INK, 3))
        o.append(rect(230, cy - 22, 170, 44, 8, PAPER, DATA_S, 2, "6 4"))
        o.append(t(315, cy, NAMES[i], 14, INK, "middle", central=True))
        o.append(cross(246, cy, 6))
    o.append(rect(440, 70, 340, 168, 12, PANEL, GRID, 2))
    o.append(t(610, 92, "held fixed for all five models", 14, INK, "middle"))
    for i, s in enumerate(["same seed: 0", "same steps: 800", "same text", "same 20 scoring batches"]):
        o.append(chip(456, 106 + i * 32, 308, s, GRID, PAPER, 12, 26, mono=False))
    o.append(arrow(405, 190, 435, 190, INK, 3))
    o.append(arrow(610, 240, 610, 262, INK, 3))
    o.append(box(440, 264, 340, 46, "score on text it never trained on", "validation loss", MODEL_F, MODEL_S, 2, None, False))
    o.append(t(400, 340, "five models: the full one, then one with each part deleted; compare each with the full one by subtraction", 12, MUT, "middle"))
    o.append(cap("Delete one part, hold everything else fixed, and compare on unseen text."))
    fig("fig-w19-4-delete-one-part", "0 0 800 400",
        "An ablation deletes one part of the TinyGPT, holds seed, steps, text and scoring batches fixed, and compares validation loss",
        "On the left a panel for the full TinyGPT holds four switches: mask_on, pos_on, res_on and ln_on. An arrow from each leads to a dashed box with a cross: "
        "no mask, no positions, no residual, no norm. An arrow from those leads to a panel of four things held fixed (seed 0, 800 steps, the same text, "
        "the same 20 scoring batches) and then to a box that scores each model on text it never trained on, the validation loss.", o)


# ---------------------------------------------------------------- W19-5  the subtraction and the gap
def w19_5():
    FULL = 1.673                                                   # student guide Step 5 table
    ROWS = [("no residual", 2.679, 0.015), ("no positions", 1.739, 0.288), ("full", 1.673, 0.076),
            ("no norm", 1.478, 0.327), ("no mask", 0.077, 0.007)]   # (model, validation, gap) as printed
    DIFF = {"no residual": "+1.006", "no positions": "+0.066", "full": "0", "no norm": "-0.195", "no mask": "-1.596"}
    o = [ctitle("Five models, two ways to read the table")]
    z, sc = 360, 70.0
    gx, gs = 510, 520.0
    o.append(t(z, 86, "validation minus 1.673", 14, INK, "middle"))
    o.append(t(z - 4, 104, "lower than full", 12, MUT, "end"))
    o.append(t(z + 4, 104, "higher than full", 12, MUT, "start"))
    o.append(t(gx + 100, 86, "gap = validation minus train", 14, INK, "middle"))
    for i, (name, val, gap) in enumerate(ROWS):
        cy = 134 + i * 44
        o.append(t(124, cy, name, 14, INK, "end", central=True))
        d = val - FULL
        if name == "full":
            o.append(t(z + 8, cy, "0 (the baseline)", 12, MUT, "start", central=True))
        elif d < 0:
            o.append(rect(z + d * sc, cy - 12, -d * sc, 24, 4, DATA_F, DATA_S, 2))
            lab = DIFF[name] + (" a leak" if name == "no mask" else "")
            o.append(t(z + d * sc - 6, cy, lab, 12, INK, "end", central=True))
        else:
            o.append(rect(z, cy - 12, d * sc, 24, 4, DATA_F, DATA_S, 2))
            o.append(t(z + d * sc + 6, cy, DIFF[name], 12, INK, "start", central=True))
        o.append(rect(gx, cy - 12, gap * gs, 24, 4, PAPER, DATA_S, 2))
        o.append(t(gx + gap * gs + 6, cy, "%.3f" % gap, 12, INK, "start", central=True))
    o.append(line(z, 112, z, 326, INK, 2))
    o.append(line(gx, 112, gx, 326, INK, 2))
    o.append(t(400, 346, "leak test (untrained model): a later token changed, scores at places 0-39 move by", 12, MUT, "middle"))
    o.append(t(400, 362, "0.000000 with the mask and 0.001437 without", 12, MUT, "middle"))
    o.append(cap("Subtract from the full model's 1.673; the lowest number is a leak.", 376))
    fig("fig-w19-5-ablation-differences", "0 0 800 400",
        "Each deleted model's validation loss minus the full model's 1.673, and its train-validation gap; the no-mask number is lower only because of a leak",
        "Two sets of horizontal bars for five rows: no residual, no positions, full, no norm, no mask. The left bars start at a vertical zero line and run right for "
        "plus 1.006 and plus 0.066, nothing for full, and left for minus 0.195 and minus 1.596 (marked a leak). The right bars show the gap, 0.015, 0.288, 0.076, 0.327 and 0.007. "
        "A line below gives the leak test, 0.000000 with the mask and 0.001437 without.", o)


# ---------------------------------------------------------------- W19-6  blank: which places can be predicted
def w19_6():
    TOK = ["sym 1", "sym 2", "sym 3", "sym 4", "SEP", "ans 1", "ans 2", "ans 3", "ans 4"]   # 4-symbol copy task, workbook 19.3
    w, g, x0 = 76, 6, 34
    o = [ctitle("Which places can a model predict?")]
    o.append(t(x0 - 2, 92, "place", 12, MUT, "start"))
    for i, s in enumerate(TOK):
        x = x0 + i * (w + g)
        o.append(t(x + w / 2.0, 108, str(i) if i < 8 else "", 12, INK, "middle"))
        o.append(rect(x, 116, w, 34, 6, DATA_F if i < 8 else PAPER, DATA_S, 2, None if i < 8 else "6 4"))
        o.append(t(x + w / 2.0, 133, s, 12, INK, "middle", mono=True, central=True))
    o.append(t(x0 + 8 * (w + g) + w / 2.0, 92, "target only", 12, MUT, "middle"))
    for i in range(8):
        x = x0 + i * (w + g)
        o.append(arrow(x + w / 2.0, 152, x + w / 2.0, 176, INK, 3))
        o.append(rect(x + 12, 180, w - 24, 46, 6, PAPER, GRID, 2, "6 4"))
    o.append(t(400, 250, "Under each place, write R if the token it must name next is random, P if it can be predicted.", 14, INK, "middle"))
    o.append(t(150, 292, "how many R?", 14, INK, "end", central=True))
    o.append(rect(162, 270, 70, 44, 6, PAPER, GRID, 2, "6 4"))
    o.append(t(420, 292, "how many P?", 14, INK, "end", central=True))
    o.append(rect(432, 270, 70, 44, 6, PAPER, GRID, 2, "6 4"))
    o.append(cap("Pencil: one letter per place, then two counts.", 360))
    fig("fig-w19-6-blank-predictable-places", "0 0 800 400",
        "A blank strip: mark each of the eight places of a four-symbol copy task as random or predictable",
        "A row of nine boxes for a four-symbol copy task: sym 1 to sym 4, SEP, ans 1 to ans 4. The first eight are numbered as places 0 to 7; the ninth is dashed and marked target only. "
        "An arrow from each of the eight places leads to an empty dashed box, and two empty count boxes, how many R and how many P, sit below. Nothing is filled in.", o)


# ---------------------------------------------------------------- W20-4  three ways to cut a sentence
def w20_4():
    SENT = "the baker practised the cricket"                      # student guide Start Here: 31 characters
    PIECES = ["the", " ", "baker", " ", "p", "r", "ac", "t", "is", "ed", " ", "the", " ", "c", "ri", "c", "ket"]  # printed, section 9
    assert len(SENT) == 31 and "".join(PIECES) == SENT and len(PIECES) == 17
    cw, x0 = 21.5, 110
    o = [ctitle("Three ways to cut one sentence")]
    # letters
    o.append(t(20, 84, "letters: 31 numbers, from a list of 28 characters", 14, INK, "start"))
    for i, ch in enumerate(SENT):
        x = x0 + i * cw
        if ch == " ":
            o.append(sq(x, 94, cw, 34, PANEL, GRID, 1.5))
        else:
            o.append(sq(x, 94, cw, 34, DATA_F, DATA_S, 1.5))
            o.append(t(x + cw / 2.0, 111, ch, 12, INK, "middle", mono=True, central=True))
    # words
    o.append(t(20, 160, "whole words: 5 numbers, but two words are holes", 14, INK, "start"))
    pos = 0
    for wd in SENT.split(" "):
        x = x0 + pos * cw + 2
        wid = len(wd) * cw - 4
        hole = wd in ("practised", "cricket")
        o.append(rect(x, 170, wid, 34, 6, PAPER if hole else DATA_F, BAD_S if hole else DATA_S, 3 if hole else 2, "6 4" if hole else None))
        o.append(t(x + wid / 2.0 + (8 if hole else 0), 187, wd, 12, INK, "middle", mono=True, central=True))
        if hole:
            o.append(cross(x + 12, 187, 5))
        pos += len(wd) + 1
    # pieces
    o.append(t(20, 236, "pieces (byte-pair encoding, 300 merges): 17 tokens, no holes", 14, INK, "start"))
    pos = 0
    for p in PIECES:
        x = x0 + pos * cw
        wid = len(p) * cw
        if p == " ":
            o.append(sq(x, 246, wid, 34, PANEL, GRID, 1.5))
        else:
            o.append(sq(x, 246, wid, 34, MODEL_F, MODEL_S, 2))
            o.append(t(x + wid / 2.0, 263, p, 12, INK, "middle", mono=True, central=True))
        pos += len(p)
    o.append(sq(x0, 306, 22, 18, PANEL, GRID, 1.5))
    o.append(t(x0 + 30, 315, "a lone space", 12, INK, "start", central=True))
    o.append(rect(x0 + 160, 306, 22, 18, 4, PAPER, BAD_S, 3, "6 4"))
    o.append(cross(x0 + 171, 315, 4))
    o.append(t(x0 + 190, 315, "a hole: the word has no number", 12, INK, "start", central=True))
    o.append(cap("Letters never leave a hole, words do; pieces keep the sequence short and still leave no hole.", 360))
    fig("fig-w20-4-three-ways-to-cut", "0 0 800 400",
        "The same 31-character sentence cut into letters, whole words and byte-pair pieces; only whole words leave holes",
        "Three aligned rows for the sentence the baker practised the cricket. The top row has 31 small cells, one per character, with spaces grey. "
        "The middle row has five word boxes; practised and cricket are dashed with a cross, marking holes. The bottom row has 17 piece boxes: the, space, baker, space, p, r, ac, t, is, ed, space, the, space, c, ri, c, ket.", o)


# ---------------------------------------------------------------- W20-5  who pays
def w20_5():
    ROWS = [("English", 38, 26, 0.68), ("Hindi", 13, 37, 2.85), ("emoji", 3, 12, 4.00), ("mixed", 15, 18, 1.20)]   # cost.py: (script, characters, tokens, tokens per character)
    o = [ctitle("What the same tokenizer charges per character")]
    o.append(t(20, 84, "tokens per character (tokenizer trained on English)", 14, INK, "start"))
    x0, sc = 120, 100.0
    for i, (name, ch, tok, tpc) in enumerate(ROWS):
        cy = 112 + i * 40
        o.append(t(x0 - 10, cy, name, 14, INK, "end", central=True))
        o.append(rect(x0, cy - 12, tpc * sc, 24, 4, DATA_F, DATA_S, 2))
        o.append(t(x0 + tpc * sc + 8, cy, "%.2f   (%d tokens / %d characters)" % (tpc, tok, ch), 12, INK, "start", central=True))
    o.append(line(x0 + 68, 96, x0 + 68, 262, GRID, 1.5, "6 4"))
    o.append(t(x0 + 68, 276, "English: 0.68", 12, MUT, "middle"))
    o.append(line(x0, 96, x0, 262, INK, 2))
    o.append(t(20, 304, "the Hindi greeting, 13 characters, in tokens", 14, INK, "start"))
    for j, (lab, n, txt) in enumerate([("before", 37, "37 tokens"), ("after", 3, "3 tokens, once the tokenizer had been shown Hindi")]):
        cy = 328 + j * 26
        o.append(t(x0 - 10, cy, lab, 12, INK, "end", central=True))
        o.append(rect(x0, cy - 9, n * 8.0, 18, 4, ACC_F if j else DATA_F, ACC_S if j else DATA_S, 2))
        o.append(t(x0 + n * 8.0 + 8, cy, txt, 12, INK, "start", central=True))
    o.append(cap("The vocabulary is whatever the tokenizer was trained on.", 376))
    fig("fig-w20-5-tokens-per-character", "0 0 800 400",
        "A tokenizer trained on English costs 0.68 tokens per character for English and 2.85 for Hindi; after seeing Hindi, the greeting takes 3 tokens, not 37",
        "Four horizontal bars of tokens per character: English 0.68 (26 tokens for 38 characters), Hindi 2.85 (37 for 13), emoji 4.00 (12 for 3) and mixed 1.20 (18 for 15), "
        "with a dashed guide at the English length. Below, two bars for the 13-character Hindi greeting: 37 tokens before and 3 tokens after the tokenizer was trained on Hindi too.", o)


# ---------------------------------------------------------------- W20-6  blank: merge by hand
def w20_6():
    o = [ctitle("Merge by hand: the class card")]
    o.append(t(20, 82, "words:", 14, INK, "start", central=True))
    for i, s in enumerate(["the x 5", "then x 2", "than x 2", "hat x 3"]):
        o.append(chip(90 + i * 120, 68, 110, s, DATA_S, DATA_F, 12, 28))
    o.append(t(20, 124, "first count table", 14, INK, "start"))
    for i, p in enumerate(["th", "he", "ha", "at", "en", "an"]):
        x = 20 + i * 126
        o.append(sq(x, 132, 126, 26, DATA_F, DATA_S, 2))
        o.append(t(x + 63, 145, p, 14, INK, "middle", mono=True, central=True))
        o.append(sq(x, 158, 126, 34, PAPER, GRID, 2))
    cols = [("merge", 60), ("pair glued", 130), ("count", 90), ("new piece", 120), ("the four words now", 360)]
    x = 20
    xs = []
    o.append(t(20, 214, "four merges", 14, INK, "start"))
    for lab, w in cols:
        xs.append((x, w))
        o.append(sq(x, 222, w, 26, DATA_F, DATA_S, 2))
        o.append(t(x + w / 2.0, 235, lab, 12, INK, "middle", central=True))
        x += w
    for r in range(4):
        y = 248 + r * 24
        for c, (xx, w) in enumerate(xs):
            o.append(sq(xx, y, w, 24, PAPER, GRID, 2))
            if c == 0:
                o.append(t(xx + w / 2.0, y + 12, str(r + 1), 12, INK, "middle", central=True))
    o.append(cap("Pairs inside words only, weighted by how often the word occurs; recount after every glue.", 372))
    fig("fig-w20-6-blank-merge-card", "0 0 800 400",
        "A blank merge-by-hand sheet for the class card: fill the six pair counts, then four merges with the words after each glue",
        "Four word chips, the x 5, then x 2, than x 2 and hat x 3. Below, a row of six headed cells for the pairs th, he, ha, at, en and an, each with an empty box beneath. "
        "Below that, a table with columns merge, pair glued, count, new piece and the four words now, and four numbered rows that are empty.", o)


# ---------------------------------------------------------------- W21-4  a power law, straight on log paper
def w21_4():
    XS = [10, 12, 15, 20, 30, 40, 60, 80, 100, 150, 200, 300, 500, 1000]      # y = 100 / x, student guide Step 1
    o = [ctitle("A power law is a straight line on log paper")]
    # left panel: ordinary axes
    o.append(rect(20, 62, 370, 250, 12, PANEL, GRID, 2))
    o.append(t(205, 84, "ordinary axes: a curve", 14, INK, "middle"))
    lx0, lx1, ly0, ly1 = 66, 370, 286, 106
    LX = lambda x: lx0 + x / 1000.0 * (lx1 - lx0)
    LY = lambda y: ly0 - y / 10.0 * (ly0 - ly1)
    o.append(line(lx0, ly0, lx1, ly0, INK, 2))
    o.append(line(lx0, ly0, lx0, ly1 - 6, INK, 2))
    o.append(poly([(LX(x), LY(100.0 / x)) for x in XS], "none", DATA_S, 3))
    for x, y, lab in [(10, 10, "(10, 10)"), (100, 1, "(100, 1)"), (1000, 0.1, "(1000, 0.1)")]:
        o.append(circ(LX(x), LY(y), 5, PAPER, DATA_S, 2))
    o.append(t(LX(10) + 10, LY(10) + 4, "10", 12, INK, "start"))
    o.append(t(LX(100) + 4, LY(1) - 10, "1", 12, INK, "start"))
    o.append(t(LX(1000) - 6, LY(0.1) - 12, "0.1", 12, INK, "end"))
    o.append(t(lx1, ly0 + 18, "x", 12, MUT, "end"))
    o.append(trot(44, 200, "y", 12))
    o.append(t(205, 302, "x times 10 each step, y times 0.1", 12, MUT, "middle"))
    # right panel: log axes
    o.append(rect(410, 62, 370, 250, 12, PANEL, GRID, 2))
    o.append(t(595, 84, "both axes logged: a line, slope -1", 14, INK, "middle"))
    rx0, rx1, ry0, ry1 = 470, 760, 280, 106
    RX = lambda v: rx0 + (v - 0.5) / 3.0 * (rx1 - rx0)
    RY = lambda v: ry0 - (v + 1.5) / 3.0 * (ry0 - ry1)
    o.append(line(rx0, ry0, rx1, ry0, INK, 2))
    o.append(line(rx0, ry0, rx0, ry1 - 6, INK, 2))
    for v in (1, 2, 3):
        o.append(t(RX(v), ry0 + 16, str(v), 12, INK, "middle"))
    for v in (1, 0, -1):
        o.append(t(rx0 - 8, RY(v), ("-1" if v == -1 else str(v)), 12, INK, "end", central=True))
    o.append(poly([(RX(0.5), RY(1.5)), (RX(3.5), RY(-1.5))], "none", DATA_S, 3))
    o.append(poly([(RX(1), RY(1)), (RX(2), RY(1)), (RX(2), RY(0))], "none", MUT, 1.5, "6 4"))
    o.append(t(RX(1.5), RY(1) - 8, "right 1", 12, MUT, "middle"))
    o.append(t(RX(2) + 8, RY(0.5), "down 1", 12, MUT, "start"))
    for v, y in [(1, 1), (2, 0), (3, -1)]:
        o.append(circ(RX(v), RY(y), 5, PAPER, DATA_S, 2))
    o.append(t(rx1 + 10, ry0 + 16, "log10(x)", 12, MUT, "end"))
    o.append(trot(436, 195, "log10(y)", 12))
    o.append(t(680, 130, "slope = the exponent", 12, MUT, "middle"))
    o.append(box(20, 322, 760, 32, "10 ** slope  =  10 ** -1  =  0.1", None, MODEL_F, MODEL_S, 2))
    o.append(cap("Ten times x multiplies y by 10 ** slope; a ruler can extend only a straight line.", 376))
    fig("fig-w21-4-power-law-straight-line", "0 0 800 400",
        "A power law such as y equals 100 over x is a curve on ordinary axes and a straight line of slope minus 1 once both axes are logged",
        "Two panels. On the left, ordinary axes with a bending curve through the points (10, 10), (100, 1) and (1000, 0.1). On the right, both axes logged: the same three points, "
        "at log10(x) 1, 2, 3 and log10(y) 1, 0, minus 1, lie on a straight line, with a dashed step marked right 1, down 1. "
        "A bar below states that ten times x gives 10 to the power minus 1, which is 0.1 times y.", o)


# ---------------------------------------------------------------- W21-5  the misses
def w21_5():
    MISS = [("14,549 knobs", -1.4, False), ("41,173 knobs", 3.1, False), ("131,285 knobs", -2.1, False),
            ("458,965 knobs", 0.4, False), ("1,704,149 knobs", 15.8, True)]      # fit.py 'off by', check.py 'too hopeful by'
    RATIO = [("width 16", 72.9), ("width 32", 32.0), ("width 64", 13.8), ("width 128", 6.8), ("width 256", 4.5)]   # flops.py last column
    o = [ctitle("How far off: the line, and the arithmetic")]
    o.append(t(20, 84, "measured vs the line, signed miss (%)", 14, INK, "start"))
    z, sc = 205, 9.0
    for i, (lab, v, new) in enumerate(MISS):
        cy = 120 + i * 42
        o.append(t(z - 70, cy, lab, 12, INK, "end", central=True))
        fill, st = (ACC_F, ACC_S) if new else (DATA_F, DATA_S)
        if v >= 0:
            o.append(rect(z, cy - 12, v * sc, 24, 4, fill, st, 2))
            o.append(t(z + v * sc + 6, cy, "+%.1f%%" % v, 12, INK, "start", central=True))
        else:
            o.append(rect(z + v * sc, cy - 12, -v * sc, 24, 4, fill, st, 2))
            o.append(t(z + 6, cy, "%.1f%%" % v, 12, INK, "start", central=True))
    o.append(line(z, 100, z, 320, INK, 2))
    o.append(t(z + 15.8 * sc + 6, 120 + 4 * 42 + 20, "the fifth model, not in the fit", 12, ACC_S, "end"))
    o.append(t(430, 84, "measured seconds / predicted seconds (6ND)", 14, INK, "start"))
    x0, rs = 512, 2.6
    for i, (lab, v) in enumerate(RATIO):
        cy = 120 + i * 42
        o.append(t(x0 - 8, cy, lab, 12, INK, "end", central=True))
        o.append(rect(x0, cy - 12, v * rs, 24, 4, PAPER, DATA_S, 2))
        o.append(t(x0 + v * rs + 6, cy, "%.1f" % v, 12, INK, "start", central=True))
    o.append(line(x0, 100, x0, 320, INK, 2))
    o.append(t(400, 338, "Percentages are the same on every run. Seconds are not: the ratios are from the author's laptop", 12, MUT, "middle"))
    o.append(t(400, 354, "and vary by machine and from run to run.", 12, MUT, "middle"))
    o.append(cap("The line fits four models within 3.1% and misses the fifth by 15.8%.", 376))
    fig("fig-w21-5-misses-and-ratios", "0 0 800 400",
        "The line misses its four fitted models by at most 3.1 percent and the fifth by 15.8 percent; the run time is 4.5 to 72.9 times the 6ND prediction on one laptop",
        "Left, five horizontal bars of signed miss in percent: minus 1.4, plus 3.1, minus 2.1 and plus 0.4 for the four fitted models, and plus 15.8 for the fifth, marked as not in the fit. "
        "Right, five bars of measured seconds divided by predicted seconds: 72.9, 32.0, 13.8, 6.8 and 4.5 for widths 16 to 256. A note says the seconds vary by machine and from run to run.", o)


# ---------------------------------------------------------------- W21-6  blank: the Fingerprint card
def w21_6():
    LINES = [("the baker opened her door", ""), ("the baker opened her door", ""), ("the Baker opened her door", ""),
             ("the baker opened her door", "one space at the end"), ("the baker opened the door", ""),
             ("the baker opened her door", "two spaces at the start"), ("the baker opened her door", "two spaces in the middle"),
             ("THE BAKER OPENED HER DOOR", "")]                         # student guide Fingerprint card
    o = [ctitle("The Fingerprint card: tick the matches")]
    cols = [(500, "A  md5 says same", "as written"), (610, "B  same after", ".strip()"), (720, "C  a human says", "same thing")]
    o.append(t(20, 78, "line 1 is: the baker opened her door", 12, MUT, "start"))
    for cx, a, b in cols:
        o.append(t(cx, 80, a, 12, INK, "middle"))
        o.append(t(cx, 95, b, 12, INK, "middle"))
    for i, (s, note) in enumerate(LINES):
        y = 104 + i * 32
        o.append(rect(20, y, 760, 30, 0, PANEL if i % 2 == 0 else PAPER, GRID, 1))
        o.append(t(34, y + 15, str(i + 1), 12, INK, "middle", central=True))
        if i == 0:
            o.append(t(60, y + 15, "(line 1: the line to match)", 12, MUT, "start", central=True))
        else:
            o.append(t(60, y + 15, s, 12, INK, "start", mono=True, central=True))
            if note:
                o.append(t(60 + 7.3 * len(s) + 16, y + 15, "(" + note + ")", 12, MUT, "start", central=True))
        for cx, a, b in cols:
            o.append(rect(cx - 12, y + 4, 24, 22, 4, PAPER, GRID, 2, "6 4"))
    o.append(cap("Fill A, B and C before you run anything; then check with card.py.", 372))
    fig("fig-w21-6-blank-fingerprint-card", "0 0 800 400",
        "A blank grid for the Fingerprint card: tick which of eight lines md5 calls the same as line 1, as written and after strip, and which a human would call the same",
        "A table of eight numbered lines of text taken from the card, such as the baker opened her door with a capital B, a space at the end, two spaces at the start or in the middle, "
        "and all capitals. Each row has three empty dashed tick boxes under the headings A, md5 says same as written; B, same after strip; and C, a human says same thing. Nothing is ticked.", o)


def build():
    for f in (w19_4, w19_5, w19_6, w20_4, w20_5, w20_6, w21_4, w21_5, w21_6):
        f()
    return FIGS

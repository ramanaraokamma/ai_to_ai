"""Block 6 second-round figures (weeks 16, 17, 18): fig-wNN-4/5/6. Deterministic; no randomness.

Every number drawn is copied from the executed output in that week's student guide / workbook, or is a
hand product whose working is printed beside it (STYLE.md 2.1):
  W16-4  where.py (words the dog bit the postman = ids 0 1 2 0 3; place table nn.Embedding(8, d)); no numbers invented
  W16-5  count.py (attention 65664, MLP 131712, two norms 512, one block 197888; 12 d d + 10 d at d = 8, 16, 128)
  W16-6  blank: workbook page 16.4 Part B (d = 10); answers are in the workbook ANSWERS and the teacher key
  W17-4  check_init.py / nested.py (x (32, 64); d 128; 4 blocks; 28 characters; children names)
  W17-5  train.py table of section 7 (train, validation and gap at seven steps; ln 28 = 3.3322)
  W17-6  blank: workbook page 17.6 Part A (axes for the six gaps; no point drawn)
  W18-4  the "night before" table of the Week 18 student guide (what each of Weeks 10-17 left behind)
  W18-5  the paper format table (marks 20, 16, 12, 15, 12; minutes 15, 15, 10, 15, 13) and hand divisions
  W18-6  blank: confidence map and percent-earned bars (workbook pages 18.1 and 18.9); no marks drawn
Called from _gen_build.py through build().
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gen_core import *   # noqa: E402,F401

WIDE = "0 0 800 400"
TIMES, MINUS, ARROW, DIV = "&#215;", "&#8722;", "&#8594;", "&#247;"


def title(s):
    return t(400, 46, s, 24, INK, "middle")


def caption(s, y=376):
    return t(400, y, s, 14, MUT, "middle")


def panel(x, y, w, h, stroke=GRID, dash=None):
    return rect(x, y, w, h, 12, PANEL, stroke, 2, dash)


def cell(cx, cy, w, h, label, fill=DATA_F, stroke=DATA_S, sw=2, dash=None, mono=True, size=12, color=INK):
    return "%s\n  %s" % (rect(cx - w / 2.0, cy - h / 2.0, w, h, 6, fill, stroke, sw, dash),
                         t(cx, cy, label, size, color, "middle", mono=mono, central=True))


# ============================================================ W16-4
def w16_4():
    words = ["the", "dog", "bit", "the", "postman"]
    wrow = [0, 1, 2, 0, 3]                      # where.py: a = tensor([0, 1, 2, 0, 3])
    xs = [170, 300, 430, 560, 690]
    o = [title("Add the place row to the word row")]
    o.append(t(110, 108, "word row", 12, INK, "end", central=True))
    o.append(t(110, 123, "(word table)", 12, MUT, "end", central=True))
    o.append(t(110, 168, "place row", 12, INK, "end", central=True))
    o.append(t(110, 183, "(place table)", 12, MUT, "end", central=True))
    o.append(t(110, 226, "goes in", 12, INK, "end", central=True))
    for i, x in enumerate(xs):
        o.append(t(x, 80, words[i], 14, INK, "middle", mono=True))
        o.append(cell(x, 114, 100, 30, "word row %d" % wrow[i], DATA_F, DATA_S, 2))
        o.append(t(x, 141, "+", 20, INK, "middle", central=True))
        o.append(cell(x, 174, 100, 30, "place row %d" % i, MODEL_F, MODEL_S, 2))
        o.append(t(x, 201, "=", 20, INK, "middle", central=True))
        twin = i in (0, 3)
        o.append(cell(x, 228, 100, 30, "%s at %d" % (words[i], i), ACC_F if twin else DATA_F,
                      ACC_S if twin else DATA_S, 4 if twin else 2))
    o.append(bracket(170, 560, 252, 8, ACC_S, True))
    o.append(t(365, 280, "same word row 0, different place rows, so different rows go in", 14, ACC_S, "middle"))
    o.append(panel(40, 304, 720, 44))
    o.append(t(400, 326, "The sum is still one row of d numbers, so every layer after it keeps its shape.", 14, INK, "middle", central=True))
    o.append(caption("Rows 0 to 4 of a place table with 8 rows; word ids as in where.py.", 372))
    desc = ("Five columns for the words the, dog, bit, the, postman. In each column a blue box holds a word row "
            "(word row 0, 1, 2, 0, 3), a plus sign, a purple box holds a place row (place row 0 to 4), an equals sign, "
            "and a bottom box shows what goes in (the at 0, dog at 1, bit at 2, the at 3, postman at 4). "
            "The two boxes for the word the are pink with a thick border, and a bracket says they share word row 0 but have different place rows. "
            "A panel says the sum is still one row of d numbers.")
    return "fig-w16-4-word-row-plus-place-row.svg", svg_doc(
        WIDE, "Attention is told the seat by adding a place row to each word row, so the same word at two seats goes in as two different rows", desc, J(o))


# ============================================================ W16-5
def w16_5():
    att, mlp, nrm, tot = 65664, 131712, 512, 197888      # count.py, d = 128
    assert att + mlp + nrm == tot
    x0, wtot = 50, 700.0
    wa, wm = att * wtot / tot, mlp * wtot / tot
    o = [title("Where the knobs of one block sit")]
    o.append(t(50, 84, "one block at d = 128 (Week 17's size)", 14, MUT))
    o.append(rect(x0, 96, wa, 48, 2, MODEL_F, MODEL_S, 2))
    o.append(rect(x0 + wa, 96, wm, 48, 2, DATA_F, DATA_S, 2))
    o.append(rect(x0 + wa + wm, 96, wtot - wa - wm, 48, 1, ACC_F, ACC_S, 2))
    o.append(t(x0 + wa / 2, 114, "attention", 14, INK, "middle", central=True))
    o.append(t(x0 + wa / 2, 132, "65,664", 14, INK, "middle", mono=True, central=True))
    o.append(t(x0 + wa + wm / 2, 114, "MLP", 14, INK, "middle", central=True))
    o.append(t(x0 + wa + wm / 2, 132, "131,712", 14, INK, "middle", mono=True, central=True))
    o.append(line(750, 144, 750, 160, ACC_S, 2))
    o.append(t(750, 176, "two norms 512", 12, ACC_S, "end"))
    o.append(t(50, 176, "65,664 + 131,712 + 512 = 197,888", 14, INK, mono=True))
    o.append(t(50, 198, "the MLP holds about twice the knobs of attention", 12, MUT))
    o.append(t(50, 234, "the formula 12 " + TIMES + " d " + TIMES + " d + 10 " + TIMES + " d, at three widths", 14, MUT))
    cards = [("d = 8", "12 " + TIMES + " 64 + 10 " + TIMES + " 8", "848"),
             ("d = 16", "12 " + TIMES + " 256 + 10 " + TIMES + " 16", "3,232"),
             ("d = 128", "12 " + TIMES + " 16,384 + 10 " + TIMES + " 128", "197,888")]
    for i, (a, b, c) in enumerate(cards):
        cx = 50 + i * 240
        o.append(rect(cx, 248, 220, 84, 8, PANEL, GRID, 2))
        o.append(t(cx + 110, 270, a, 14, INK, "middle"))
        o.append(t(cx + 110, 294, b, 12, MUT, "middle", mono=True))
        o.append(t(cx + 110, 318, "= " + c, 18, ACC_S if i == 2 else INK, "middle", mono=True))
    o.append(caption("The number of words T and the number of heads H are not in the formula.", 366))
    desc = ("A long bar split into three parts for one block at width 128: attention 65,664 knobs in purple, MLP 131,712 in blue, "
            "and a thin pink sliver for the two layer norms, 512. Beneath it the sum 65,664 + 131,712 + 512 = 197,888 and a note that the MLP holds about twice attention's knobs. "
            "Below, three cards give 12 times d times d plus 10 times d: d = 8 gives 848, d = 16 gives 3,232 and d = 128 gives 197,888.")
    return "fig-w16-5-block-knobs-by-part-and-width.svg", svg_doc(
        WIDE, "Most of a block's knobs sit in the MLP, and the formula 12 d d + 10 d counts them at any width", desc, J(o))


# ============================================================ W16-6 (blank)
def w16_6():
    o = [title("Page 16.4 Part B: count one block at d = 10")]
    att = [("ln1", "LayerNorm(d)"), ("q", "Linear(d, d), no bias"), ("k", "Linear(d, d), no bias"),
           ("v", "Linear(d, d), no bias"), ("proj", "Linear(d, d)")]
    mlp = [("ln2", "LayerNorm(d)"), ("up", "Linear(d, 4d)"), ("act", "GELU()"), ("down", "Linear(4d, d)")]
    o.append(t(40, 82, "attention half", 14, MUT))
    o.append(t(420, 82, "MLP half", 14, MUT))
    for i, (nm, what) in enumerate(att):
        y = 92 + i * 38
        o.append(rect(40, y, 190, 30, 6, PANEL, GRID, 2))
        o.append(t(50, y + 15, "%s  %s" % (nm, what), 12, INK, mono=True, central=True))
        o.append(rect(240, y, 80, 30, 6, PAPER, HUMAN_S, 3, "6 4"))
    for i, (nm, what) in enumerate(mlp):
        y = 92 + i * 38
        o.append(rect(420, y, 190, 30, 6, PANEL, GRID, 2))
        o.append(t(430, y + 15, "%s  %s" % (nm, what), 12, INK, mono=True, central=True))
        o.append(rect(620, y, 80, 30, 6, PAPER, HUMAN_S, 3, "6 4"))
    o.append(t(420, 262, "dashed boxes are for your pencil", 12, MUT))
    o.append(panel(40, 290, 720, 66))
    o.append(t(60, 312, "total, the long way:", 14, INK, central=True))
    o.append(rect(230, 298, 100, 28, 6, PAPER, HUMAN_S, 3, "6 4"))
    o.append(t(60, 338, "total, the formula 12 " + TIMES + " 10 " + TIMES + " 10 + 10 " + TIMES + " 10:", 14, INK, central=True))
    o.append(rect(440, 324, 100, 28, 6, PAPER, HUMAN_S, 3, "6 4"))
    o.append(t(640, 312, "Do they agree?", 14, INK, central=True))
    o.append(rect(740 - 8, 300, 20, 20, 4, PAPER, HUMAN_S, 3, "6 4"))
    desc = ("A blank worksheet. Nine grey boxes name the parts of one block: attention half ln1 LayerNorm(d), q, k and v each Linear(d, d) with no bias, proj Linear(d, d); "
            "MLP half ln2 LayerNorm(d), up Linear(d, 4d), act GELU(), down Linear(4d, d). Beside each is an empty dashed box for the knob count at d = 10. "
            "At the bottom are two empty dashed boxes for the total counted the long way and the total from the formula 12 times 10 times 10 plus 10 times 10, and an empty tick box for whether they agree.")
    return "fig-w16-6-blank-block-count-d10.svg", svg_doc(
        WIDE, "Blank worksheet for Week 16 page 16.4 Part B: the knob count of each of the nine parts at d = 10", desc, J(o))


# ============================================================ W17-4
def w17_4():
    o = [title("TinyGPT: shapes in, shapes out")]
    # ids
    o.append(cell(75, 130, 70, 80, "ids", DATA_F, DATA_S, 2, mono=False, size=14))
    o.append(arrow(110, 130, 132, 130, INK, 2))
    # embed
    o.append(rect(136, 90, 120, 80, 8, PANEL, GRID, 2))
    o.append(cell(196, 114, 104, 32, "tok: 28 rows", DATA_F, DATA_S, 2))
    o.append(cell(196, 150, 104, 32, "pos: 64 rows", MODEL_F, MODEL_S, 2))
    o.append(arrow(256, 130, 278, 130, INK, 2))
    # blocks
    o.append(rect(282, 86, 130, 88, 8, PANEL, MODEL_S, 2))
    for i in range(4):
        o.append(cell(347, 100 + i * 22, 110, 18, "Block %d" % (i + 1), MODEL_F, MODEL_S, 2, mono=False))
    o.append(arrow(412, 130, 434, 130, INK, 2))
    o.append(cell(473, 130, 70, 60, "ln_f", MODEL_F, MODEL_S, 2))
    o.append(arrow(508, 130, 530, 130, INK, 2))
    o.append(cell(574, 130, 80, 60, "head", MODEL_F, MODEL_S, 2))
    o.append(arrow(614, 130, 636, 130, INK, 2))
    o.append(cell(700, 130, 120, 80, "28 scores", ACC_F, ACC_S, 3, mono=False, size=14))
    o.append(t(700, 160, "per place", 12, INK, "middle", central=True))
    # shapes
    o.append(t(75, 196, "shape out", 12, MUT, "middle"))
    o.append(chip(35, 204, 80, "(32, 64)", DATA_S))
    o.append(chip(140, 204, 112, "(32, 64, 128)", DATA_S))
    o.append(chip(291, 204, 112, "(32, 64, 128)", DATA_S))
    o.append(t(473, 222, "same shape", 12, MUT, "middle"))
    o.append(chip(640, 204, 120, "(32, 64, 28)", ACC_S))
    o.append(t(35, 262, "children of the model:", 14, MUT, central=True))
    kids = ["tok", "pos", "blocks", "ln_f", "head"]
    x = 215
    for k in kids:
        w = 14 + len(k) * 8
        o.append(chip(x, 249, w, k, MODEL_S))
        x += w + 8
    o.append(t(35, 306, "children of one Block:", 14, MUT, central=True))
    parts = ["ln1", "q", "k", "v", "proj", "ln2", "up", "act", "down"]
    x = 215
    for k in parts:
        w = 14 + len(k) * 8
        o.append(chip(x, 293, w, k, MODEL_S))
        x += w + 8
    o.append(caption("32 windows of 64 character ids; d = 128; nothing here is trained.", 358))
    desc = ("A left-to-right row of boxes. Character ids with shape (32, 64) go into two tables, tok with 28 rows and pos with 64 rows, "
            "then through a stack of four Block boxes, a last layer norm ln_f and an output layer head, and come out as 28 scores per place with shape (32, 64, 28). "
            "Shape chips below read (32, 64, 128) after the tables and after the blocks, and the last norm keeps the same shape. "
            "Two rows of chips list the children of the model: tok, pos, blocks, ln_f, head, and the children of one Block: ln1, q, k, v, proj, ln2, up, act, down.")
    return "fig-w17-4-tinygpt-shapes-and-tree.svg", svg_doc(
        WIDE, "TinyGPT is a tree: two tables, four Blocks, a norm and an output layer, with 64 places of width 128 flowing through", desc, J(o))


# ============================================================ W17-5
def w17_5():
    steps = [0, 300, 500, 750, 1000, 1250, 1499]
    train = ["3.349", "1.873", "1.558", "1.181", "0.999", "0.905", "0.894"]   # section 7 table
    val = ["3.351", "1.892", "1.647", "1.470", "1.417", "1.427", "1.437"]
    gap = ["0.002", "0.019", "0.089", "0.289", "0.418", "0.522", "0.543"]
    base, unit, x0, gw = 270, 50.0, 112, 88
    o = [title("Train and validation loss, and the gap")]
    o.append(rect(112, 60, 22, 14, 2, DATA_F, DATA_S, 2))
    o.append(t(140, 67, "train (text it studied)", 12, INK, central=True))
    o.append(rect(330, 60, 22, 14, 2, PAPER, INK, 2, "4 3"))
    o.append(t(358, 67, "validation (text it never saw)", 12, INK, central=True))
    for v in (0, 1, 2, 3):
        o.append(line(x0 - 6, base - v * unit, x0 + 7 * gw, base - v * unit, GRID if v else INK, 1.5 if v else 2, "6 4" if v else None))
        o.append(t(x0 - 12, base - v * unit + 4, str(v), 12, MUT, "end"))
    ln28 = 3.3322                                                            # check_init.py
    o.append(line(x0 - 6, base - ln28 * unit, x0 + 7 * gw, base - ln28 * unit, ACC_S, 2, "8 4"))
    o.append(t(x0 + 7 * gw, base - ln28 * unit - 6, "ln 28 = 3.332: knows nothing", 12, ACC_S, "end"))
    for i in range(7):
        gx = x0 + i * gw
        tv, vv = float(train[i]), float(val[i])
        last = i == 6
        o.append(sq(gx + 8, base - tv * unit, 28, tv * unit, DATA_F, DATA_S, 2))
        o.append(rect(gx + 40, base - vv * unit, 28, vv * unit, 2, PAPER, INK, 2, "4 3"))
        o.append(t(gx + 38, base + 18, str(steps[i]), 12, INK, "middle"))
        o.append(t(gx + 38, base + 36, train[i], 12, INK, "middle", mono=True))
        o.append(t(gx + 38, base + 54, val[i], 12, MUT, "middle", mono=True))
        o.append(t(gx + 38, base + 72, gap[i], 12, ACC_S if last else INK, "middle", mono=True, weight="600" if last else None))
    o.append(t(x0 - 12, base + 18, "step", 12, MUT, "end"))
    o.append(t(x0 - 12, base + 36, "train", 12, INK, "end"))
    o.append(t(x0 - 12, base + 54, "validation", 12, MUT, "end"))
    o.append(t(x0 - 12, base + 72, "gap", 12, ACC_S, "end"))
    o.append(caption("gap = validation " + MINUS + " train. Both start within 0.02 of ln 28; the gap opens from step 500 on.", 372))
    desc = ("Seven pairs of bars for steps 0, 300, 500, 750, 1000, 1250 and 1499. Solid blue bars are the training loss: 3.349, 1.873, 1.558, 1.181, 0.999, 0.905, 0.894. "
            "Dashed outline bars are the validation loss: 3.351, 1.892, 1.647, 1.470, 1.417, 1.427, 1.437. A dashed pink line marks ln 28 = 3.332. "
            "Under each pair is the gap, validation minus train: 0.002, 0.019, 0.089, 0.289, 0.418, 0.522, 0.543. The bars start level and the validation bars stay tall while the train bars fall.")
    return "fig-w17-5-train-validation-gap-by-step.svg", svg_doc(
        WIDE, "Both losses start at ln 28, then training loss keeps falling while validation flattens, so the gap grows to 0.543", desc, J(o))


# ============================================================ W17-6 (blank)
def w17_6():
    cols = ["0", "250", "300", "500", "599", "FINAL"]     # workbook page 17.6 Part A rows
    xs = [190, 300, 410, 520, 630, 740]
    top, bot = 90, 290
    o = [title("Page 17.6 Part A: plot the gap at each step")]
    ticks = ["0.06", "0.04", "0.02", "0.00", MINUS + "0.02", MINUS + "0.04"]
    for i, lab in enumerate(ticks):
        y = top + i * 40
        zero = i == 3
        o.append(line(150, y, 770, y, INK if zero else GRID, 2 if zero else 1.5, None if zero else "6 4"))
        o.append(t(142, y + 4, lab, 12, MUT, "end", mono=True))
    o.append(line(150, top, 150, bot, INK, 2))
    o.append(trot(74, 190, "gap = validation " + MINUS + " train", 12, MUT))
    for x, c in zip(xs, cols):
        o.append(line(x, bot, x, bot + 6, INK, 2))
        o.append(t(x, bot + 24, c, 12, INK, "middle"))
    o.append(t(460, bot + 46, "step (one equal slot per row of the table, not to scale)", 12, MUT, "middle"))
    o.append(rect(170, 358, 22, 14, 2, PAPER, HUMAN_S, 3, "6 4"))
    o.append(t(200, 365, "1. mark the six gaps", 12, INK, central=True))
    o.append(line(370, 365, 392, 365, HUMAN_S, 3))
    o.append(t(400, 365, "2. join them in order", 12, INK, central=True))
    o.append(circ(590, 365, 8, PAPER, HUMAN_S, 3))
    o.append(t(604, 365, "3. ring the highest", 12, INK, central=True))
    desc = ("A blank chart. The vertical axis is the gap, validation minus train, from minus 0.04 to 0.06 with grid lines every 0.02 and a solid line at 0.00. "
            "The horizontal axis has six equal slots labelled 0, 250, 300, 500, 599 and FINAL. No data is drawn. A key lists three instructions: "
            "mark the six gaps, join them in order, ring the highest.")
    return "fig-w17-6-blank-gap-axes.svg", svg_doc(
        WIDE, "Blank axes for Week 17 page 17.6 Part A: plot the six gaps of the 600-step run", desc, J(o))


# ============================================================ W18-4
def w18_4():
    tiles = [(10, ["slopes multiply:", "fading, blowing up,", "clipping"]),
             (11, ["gates and the", "forget dial"]),
             (12, ["name model, teacher", "forcing, train vs", "validation loss"]),
             (13, ["temperature, top-k,", "top-p, greedy"]),
             (14, ["the three-word", "attention pass"]),
             (15, ["divide by sqrt(d),", "the mask, heads"]),
             (16, ["places, the block,", "848 knobs at d = 8"]),
             (17, ["TinyGPT: 807,196", "knobs, first loss", "ln 28 = 3.332"])]
    o = [title("What Weeks 10 to 17 left behind")]
    xs = [40, 225, 410, 595]
    for i, (wk, lines) in enumerate(tiles):
        x, y = xs[i % 4], 62 + (i // 4) * 98
        lean = wk >= 15
        o.append(rect(x, y, 165, 84, 8, ACC_F if lean else DATA_F, ACC_S if lean else DATA_S, 4 if lean else 2))
        o.append(t(x + 12, y + 20, "Week %d" % wk, 14, INK, weight="600"))
        for j, ln in enumerate(lines):
            o.append(t(x + 12, y + 40 + j * 15, ln, 12, INK))
        if i % 4 < 3:
            o.append(arrow(x + 167, y + 42, x + 183, y + 42, INK, 2))
    o.append(bracket(410, 760, 250, 8, ACC_S, True))
    o.append(t(585, 280, "Week 19 leans on these three", 14, ACC_S, "middle"))
    o.append(rect(40, 296, 300, 50, 8, HUMAN_F, HUMAN_S, 3))
    o.append(t(190, 321, "Week 18: the paper, an X-ray", 14, INK, "middle", central=True))
    o.append(arrow(342, 321, 398, 321, INK, 3))
    o.append(rect(402, 296, 358, 50, 8, PANEL, GRID, 2))
    o.append(t(581, 311, "Week 19: take TinyGPT apart", 14, INK, "middle", central=True))
    o.append(t(581, 331, "mask, positions, residuals, norms", 12, MUT, "middle", central=True))
    o.append(caption("Read left to right, then down: eight weeks of work, one paper, then the teardown.", 372))
    desc = ("Eight tiles in two rows, Weeks 10 to 17, each naming what the week left: 10 slopes multiply, fading, blowing up and clipping; 11 gates and the forget dial; "
            "12 name model, teacher forcing, train against validation loss; 13 temperature, top-k, top-p, greedy; 14 the three-word attention pass; 15 divide by square root of d, the mask, heads; "
            "16 places, the block, 848 knobs at d = 8; 17 TinyGPT with 807,196 knobs and a first loss of ln 28 = 3.332. Tiles for Weeks 15, 16 and 17 are pink with a thick border and a bracket reads Week 19 leans on these three. "
            "Below, a box for the Week 18 paper points to a box for Week 19, which takes TinyGPT apart.")
    return "fig-w18-4-what-weeks-10-to-17-left.svg", svg_doc(
        WIDE, "Weeks 10 to 17 each left one skill on the paper, and Weeks 15 to 17 are the ones Week 19 depends on", desc, J(o))


# ============================================================ W18-5
def w18_5():
    rows = [("A", "multiple choice", 20, 15), ("B", "what does this print?", 16, 15), ("C", "find the bug", 12, 10),
            ("D", "arithmetic", 15, 15), ("E", "two real tables", 12, 13)]       # paper format table
    per = {"A": "1.33", "B": "1.07", "C": "1.20", "D": "1.00", "E": "0.92"}        # hand divisions
    assert sum(r[2] for r in rows) == 75 and sum(r[3] for r in rows) == 68
    o = [title("The paper in numbers: 75 marks, 70 minutes")]
    o.append(t(215, 84, "marks", 14, MUT))
    o.append(t(420, 84, "minutes", 14, MUT))
    o.append(t(560, 84, "marks per minute", 14, MUT))
    for i, (s, nm, m, mi) in enumerate(rows):
        y = 100 + i * 42
        e = s == "E"
        o.append(t(40, y + 15, "%s  %s" % (s, nm), 14, INK, central=True, weight="600" if e else None))
        o.append(rect(215, y, m * 6, 28, 2, ACC_F if e else DATA_F, ACC_S if e else DATA_S, 3 if e else 2))
        o.append(t(215 + m * 6 + 8, y + 15, str(m), 14, INK, central=True, mono=True))
        o.append(rect(420, y, mi * 6, 28, 2, PAPER, ACC_S if e else INK, 3 if e else 2, "4 3"))
        o.append(t(420 + mi * 6 + 8, y + 15, str(mi), 14, INK, central=True, mono=True))
        o.append(t(560, y + 15, "%d %s %d = %s" % (m, DIV, mi, per[s]), 14, ACC_S if e else INK, central=True, mono=True))
    o.append(line(40, 316, 760, 316, INK, 2))
    o.append(t(40, 338, "total", 14, INK, central=True, weight="600"))
    o.append(t(215, 338, "20 + 16 + 12 + 15 + 12 = 75", 14, INK, central=True, mono=True))
    o.append(t(480, 338, "15 + 15 + 10 + 15 + 13 = 68", 14, INK, central=True, mono=True))
    o.append(caption("Section E is the biggest single question, so start it with about thirteen minutes left.", 372))
    desc = ("Five rows for Sections A to E of the paper. Solid bars show marks: A 20, B 16, C 12, D 15, E 12. Dashed bars show minutes: A 15, B 15, C 10, D 15, E 13. "
            "A third column gives marks per minute by division: 20 divided by 15 is 1.33, 16 divided by 15 is 1.07, 12 divided by 10 is 1.20, 15 divided by 15 is 1.00, 12 divided by 13 is 0.92. "
            "Section E is drawn in pink with a thick border. The total row reads 20 + 16 + 12 + 15 + 12 = 75 marks and 15 + 15 + 10 + 15 + 13 = 68 minutes.")
    return "fig-w18-5-paper-marks-and-minutes.svg", svg_doc(
        WIDE, "The paper has 75 marks over five sections, and Section E gets the least time per mark", desc, J(o))


# ============================================================ W18-6 (blank)
def w18_6():
    o = [title("Confidence map: before and after the paper")]
    o.append(t(40, 78, "week", 12, MUT))
    for x, lab in ((170, "Yes"), (215, "Maybe"), (260, "No")):
        o.append(t(x, 78, lab, 12, MUT, "middle"))
    o.append(t(215, 62, "before: could I do this now?", 12, INK, "middle"))
    o.append(t(510, 62, "after: percent earned", 12, INK, "middle"))
    o.append(t(738, 78, "circle", 12, MUT, "middle"))
    o.append(line(546, 92, 546, 332, MUT, 2, "6 4"))
    for i in range(8):
        y = 105 + i * 30
        o.append(t(40, y, "Week %d" % (10 + i), 14, INK, central=True))
        for x in (170, 215, 260):
            o.append(circ(x, y, 9, PAPER, HUMAN_S, 3))
        o.append(rect(330, y - 9, 360, 18, 3, PAPER, HUMAN_S, 3, "6 4"))
        o.append(rect(716, y - 10, 44, 20, 4, PAPER, HUMAN_S, 3, "6 4"))
    o.append(t(330, 346, "0", 12, MUT, "middle"))
    o.append(t(546, 346, "60", 12, MUT, "middle"))
    o.append(t(690, 346, "100", 12, MUT, "middle"))
    o.append(caption("Tick tonight. After marking, shade each bar and circle at most two weeks.", 372))
    desc = ("A blank form with eight rows for Weeks 10 to 17. Each row has three empty circles headed Yes, Maybe and No for the night before, "
            "an empty dashed bar for the percent earned after the paper, from 0 to 100 with a dashed vertical line at 60, and an empty dashed box headed circle. Nothing is filled in.")
    return "fig-w18-6-blank-confidence-map.svg", svg_doc(
        WIDE, "Blank confidence map for Week 18: tick before the paper, shade the percent after, and circle at most two weeks", desc, J(o))


def build():
    out = {}
    for fn in (w16_4, w16_5, w16_6, w17_4, w17_5, w17_6, w18_4, w18_5, w18_6):
        name, svg = fn()
        out[name] = svg
    return out


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for name, svg in build().items():
        with open(os.path.join(here, name), "w") as fh:
            fh.write(svg + "\n")
        print("wrote", name)

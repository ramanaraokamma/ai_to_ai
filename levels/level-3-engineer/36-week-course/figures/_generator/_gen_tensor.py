"""TENSOR and SHAPE motifs: 1-D to 4-D blocks, a matrix multiply, a shape mismatch.

The shapes are the real ones from Module 5 and Module 7:
  (5,) one row of features ; (3, 4) a table ; (3, 32, 32) one colour image ;
  (64, 3, 32, 32) a batch of 64 ; (750, 2) @ (2, 16) -> (750, 16).
"""
from _gen_core import *
import _gen_math  # noqa: F401  (registers the maths motifs first)

# ================================================================== 1-D
M("motif-tensor-1d", "A 1-D tensor is one row of numbers",
  "A single wide bar divided into five equal cells, with a mono label reading shape open bracket 5 "
  "comma close bracket pinned to its top-right corner, and a bracket underneath labelled 5 numbers.",
  "0 0 300 160",
  J(t(20, 26, "1-D &#8212; a vector", 14, INK),
    rect(20, 58, 200, 44, 8, DATA_F, DATA_S, 3),
    [line(x, 58, x, 102, GRID, 1.5, cap=False) for x in (60, 100, 140, 180)],
    chip(150, 44, 110, "shape (5,)"),
    bracket(20, 220, 110, 8, MUT, down=True),
    t(120, 136, "5 numbers", 12, MUT, "middle"),
    t(20, 152, "one row: 5 features for one delivery", 12, MUT)),
  "One number in the shape, so one bracket and one comma. The trailing comma in (5,) is not a typo "
  "and learners will ask: it is how a shape with one entry is written.")

# ================================================================== 2-D
M("motif-tensor-2d", "A 2-D tensor is rows and columns",
  "A block divided into three rows and four columns, with a mono label reading shape 3 comma 4 pinned "
  "to its top-right corner. The left edge is labelled 3 rows and the bottom edge 4 columns.",
  "0 0 300 200",
  J(t(20, 26, "2-D &#8212; rows and columns", 14, INK),
    rect(20, 58, 200, 96, 8, DATA_F, DATA_S, 3),
    [line(20, y, 220, y, GRID, 1.5, cap=False) for y in (90, 122)],
    [line(x, 58, x, 154, GRID, 1.5, cap=False) for x in (70, 120, 170)],
    chip(150, 44, 120, "shape (3, 4)"),
    trot(14, 106, "3 rows", 12, MUT, "middle"),
    t(120, 172, "4 columns", 12, MUT, "middle"),
    t(150, 192, "rows are examples &#183; columns are features", 12, MUT, "middle")),
  "Rows first, columns second, always. Say the shape out loud as 'three by four' and point at the "
  "rows as you say three.")

# ================================================================== 3-D
M("motif-tensor-3d", "A 3-D tensor is a stack of tables",
  "A shallow three-dimensional box drawn with a front face, a top face and a right face. A mono label "
  "reads shape 3 comma 32 comma 32. The depth is labelled 3 channels, the width 32 wide and the "
  "height 32 high.",
  "0 0 320 210",
  J(t(20, 26, "3-D &#8212; a stack of tables", 14, INK),
    path("M30 70 L58 46 H238 L210 70 Z", PANEL, DATA_S, 3),
    path("M210 70 L238 46 V136 L210 160 Z", PANEL, DATA_S, 3),
    sq(30, 70, 180, 90, DATA_F, DATA_S, 3),
    [line(30, y, 210, y, GRID, 1.5, cap=False) for y in (100, 130)],
    [line(x, 70, x, 160, GRID, 1.5, cap=False) for x in (90, 150)],
    line(236, 52, 246, 45, MUT, 1.5, cap=False),
    t(310, 44, "3 channels", 12, MUT, "end"),
    t(120, 176, "32 wide", 12, MUT, "middle"),
    trot(18, 115, "32 high", 12, MUT, "middle"),
    chip(160, 168, 140, "shape (3, 32, 32)"),
    t(160, 202, "one colour image: 3 channels of 32 by 32", 12, MUT, "middle")),
  "Depth is drawn, not implied. Three numbers in the shape means three labelled edges &mdash; if you "
  "cannot label an edge, you have drawn the wrong number of dimensions.")

# ================================================================== 4-D
def _iso(dx, dy, fill_front, fill_side, stroke, sw=3):
    return [path("M%s %s L%s %s H%s %s L%s %s Z" % (30 + dx, 100 + dy, 54 + dx, 78 + dy,
                                                    204 + dx, 78 + dy, 180 + dx, 100 + dy),
                 fill_side, stroke, sw),
            path("M%s %s L%s %s V%s L%s %s Z" % (180 + dx, 100 + dy, 204 + dx, 78 + dy,
                                                 152 + dy, 180 + dx, 174 + dy),
                 fill_side, stroke, sw),
            sq(30 + dx, 100 + dy, 150, 74, fill_front, stroke, sw)]


M("motif-tensor-4d", "A 4-D tensor is a batch of 3-D tensors",
  "Three shallow three-dimensional boxes stacked one behind the other going up and to the right. A "
  "mono label reads shape 64 comma 3 comma 32 comma 32, the depth of the stack is labelled 64 images, "
  "and a note says the first number is always the batch size.",
  "0 0 360 230",
  J(t(20, 24, "4-D &#8212; a batch of 3-D tensors", 14, INK),
    _iso(32, -26, PANEL, PANEL, GRID, 2),
    _iso(16, -13, PANEL, PANEL, GRID, 2),
    _iso(0, 0, DATA_F, PANEL, DATA_S, 3),
    line(240, 54, 276, 53, MUT, 1.5, cap=False),
    t(344, 52, "64 images", 12, MUT, "end"),
    t(88, 190, "each image: 3 &#215; 32 &#215; 32", 12, MUT, "middle"),
    chip(170, 176, 170, "shape (64, 3, 32, 32)"),
    t(180, 220, "the first number is always the batch size", 12, MUT, "middle")),
  "The batch axis goes first because that is the one you slice when you take a mini-batch. Draw the "
  "back copies in grid grey at 2px so the front one still reads as the subject.")

# ================================================================== matmul
_A_ROWS = "750"
_INNER = "2"


def _shape_runs(x0, y, parts, box_fill, box_stroke):
    """Shape text split into fixed-x mono runs so the highlight lands on the exact number."""
    out, x = [], x0
    for txt, hot in parts:
        w = len(txt) * 8.4
        if hot:
            out.append(rect(x - 3, y - 16, w + 6, 22, 4, box_fill, box_stroke, 2))
        out.append(t(x, y, txt, 14, INK, mono=True))
        x += w + 4
    return out


def _grid_lines(x, w, ys):
    return [line(x + 8, y, x + w - 8, y, GRID, 1.5, cap=False) for y in ys]


M("motif-matmul", "A matrix multiply cancels the inner numbers",
  "Two blocks side by side with a multiplication sign between them and an equals sign after. The "
  "first is labelled 750 by 2, the second 2 by 16, and the two 2s are boxed in pink and joined to a "
  "callout reading the inner numbers must match. The answer block is labelled 750 by 16.",
  "0 0 420 220",
  J(t(79, 48, "X", 12, MUT, "middle"),
    t(225, 48, "W1", 12, MUT, "middle"),
    t(358, 48, "Z1", 12, MUT, "middle"),
    rect(24, 56, 110, 120, 8, DATA_F, DATA_S, 3),
    _grid_lines(24, 110, (112, 136, 160)),
    rect(170, 56, 110, 120, 8, MODEL_F, MODEL_S, 3),
    _grid_lines(170, 110, (112, 136, 160)),
    rect(310, 56, 96, 120, 8, OK_F, OK_S, 3),
    _grid_lines(310, 96, (112, 136, 160)),
    _shape_runs(40, 84, [("(750,", False), ("2", True), (")", False)], ACC_F, ACC_S),
    _shape_runs(186, 84, [("(", False), ("2", True), (", 16)", False)], ACC_F, ACC_S),
    t(318, 84, "(750, 16)", 14, INK, mono=True),
    t(152, 88, "&#215;", 18, INK, "middle"),
    t(300, 88, "=", 18, INK, "middle"),
    line(90, 90, 90, 96, ACC_S, 2, cap=False),
    line(202, 90, 202, 96, ACC_S, 2, cap=False),
    rect(46, 96, 196, 24, 12, PAPER, ACC_S, 2),
    t(144, 108, "the inner numbers must match", 12, INK, "middle", central=True),
    t(210, 192, "the two 2s must match, and then they vanish", 12, MUT, "middle"),
    t(210, 208, "what is left is (750, 16): X's rows, W1's columns", 12, MUT, "middle")),
  "Highlight the two inner numbers and NOTHING else. Split the shape into fixed-x mono runs so the "
  "highlight box lands exactly on the digit instead of trusting the font's advance width.")

# ================================================================== shape mismatch
M("motif-shape-mismatch", "A shape mismatch, and where to look",
  "The same two blocks with a multiplication sign, but the second is labelled 16 by 2. The inner "
  "numbers, 2 and 16, are boxed in red and joined to a callout reading 2 and 16 do not match. Where "
  "the answer should be there is a red box with a cross in it and the words no result.",
  "0 0 420 240",
  J(t(79, 48, "X", 12, MUT, "middle"),
    t(225, 48, "W1", 12, MUT, "middle"),
    rect(24, 56, 110, 120, 8, DATA_F, DATA_S, 3),
    _grid_lines(24, 110, (112, 136, 160)),
    rect(170, 56, 110, 120, 8, MODEL_F, MODEL_S, 3),
    _grid_lines(170, 110, (112, 136, 160)),
    rect(310, 56, 96, 120, 8, BAD_F, BAD_S, 3),
    _shape_runs(40, 84, [("(750,", False), ("2", True), (")", False)], BAD_F, BAD_S),
    _shape_runs(186, 84, [("(", False), ("16", True), (", 2)", False)], BAD_F, BAD_S),
    t(358, 84, "no result", 12, INK, "middle"),
    t(152, 88, "&#215;", 18, INK, "middle"),
    t(300, 88, "=", 18, INK, "middle"),
    badge_cross(338, 100, 0.4),
    line(90, 90, 90, 96, BAD_S, 2, cap=False),
    line(206, 90, 206, 96, BAD_S, 2, cap=False),
    rect(46, 96, 200, 26, 12, PAPER, BAD_S, 2),
    t(146, 109, "2 and 16 do not match", 12, INK, "middle", central=True),
    t(210, 196, "a shape error is a wiring error, not a maths error", 12, MUT, "middle"),
    t(210, 214, "the fix: build W1 as (2, 16), or transpose it", 12, MUT, "middle"),
    t(210, 230, "print every shape before you multiply", 12, MUT, "middle")),
  "Mirror motif-matmul EXACTLY and change only the second shape, the highlight colour and the answer. "
  "The reader should find the one difference in under two seconds.")

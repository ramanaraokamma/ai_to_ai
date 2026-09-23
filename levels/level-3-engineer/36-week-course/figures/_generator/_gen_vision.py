"""VISION, UNSUPERVISED and TEXT motifs: convolution, feature maps, k-means, PCA, bag of words.

Every number is taken from the modules and is checkable:
  Module 7 convolution: a 6x6 image of 10s and 2s, kernel [1,0,-1] x3, output cell (0,1) = 24.
  Module 8 k-means: A(1,2) B(2,1) C(2,3) D(8,8) E(9,7) F(7,9), bad start at (1,2) and (2,3).
  Module 9 bag of words: d3 = "Great pizza, great service." over the 8-word vocabulary.
"""
from _gen_core import *
import _gen_eval  # noqa: F401  (registers the evaluation motifs first)

# ================================================================== convolution
_IMG_ROW = ("10", "10", "10", "2", "2", "2")
_KER_ROW = ("1", "0", "&#8722;1")
_OUT_ROW = ("0", "24", "24", "0")


def _cells(x0, y0, n_cols, n_rows, w, row_vals, fill, stroke):
    out = []
    for r in range(n_rows):
        for c in range(n_cols):
            out.append(sq(x0 + c * w, y0 + r * w, w, w, fill, stroke, 2))
    for r in range(n_rows):
        for c in range(n_cols):
            out.append(t(x0 + c * w + w / 2.0, y0 + r * w + w / 2.0, row_vals[c],
                         12, INK, "middle", central=True))
    return out


M("motif-conv", "One cell of a feature map, worked out in full",
  "A six by six grid of pixels, bright 10s on the left and dark 2s on the right, with a pink outline "
  "round the top-left three by three window. A multiplication sign, then the three by three kernel of "
  "1, 0 and minus 1. An arrow points to a four by four feature map whose second cell, outlined in pink, "
  "holds 24. A callout shows one row giving 1 times 10 plus 0 times 10 plus minus 1 times 2 equals 8, "
  "and three rows giving 8 plus 8 plus 8 equals 24.",
  "0 0 440 260",
  J(t(92, 44, "image (6 &#215; 6)", 12, MUT, "middle"),
    _cells(20, 56, 6, 6, 24, _IMG_ROW, DATA_F, DATA_S),
    rect(44, 56, 72, 72, 0, "none", ACC_S, 3),
    t(182, 116, "&#215;", 18, INK, "middle"),
    t(236, 68, "kernel (3 &#215; 3)", 12, MUT, "middle"),
    _cells(200, 80, 3, 3, 24, _KER_ROW, MODEL_F, MODEL_S),
    arrow(276, 116, 306, 102, INK, 2.5),
    t(358, 68, "feature map (4 &#215; 4)", 12, MUT, "middle"),
    _cells(310, 80, 4, 4, 24, _OUT_ROW, OK_F, OK_S),
    rect(334, 80, 24, 24, 0, "none", ACC_S, 3),
    rect(20, 212, 400, 40, 10, PAPER, ACC_S, 2),
    t(220, 228, "one row: (1 &#215; 10) + (0 &#215; 10) + (&#8722;1 &#215; 2) = 8", 12, INK, "middle"),
    t(220, 246, "three rows: 8 + 8 + 8 = 24, so this output cell is 24", 12, MUT, "middle")),
  "ONE output cell, all of its arithmetic, nothing else. A figure that shows the kernel sliding but "
  "never multiplies anything has taught nobody what convolution is.")

# ================================================================== feature-map stack
def _slab(dx, dy, fill, stroke, sw):
    return sq(30 + dx, 86 + dy, 110, 110, fill, stroke, sw)


M("motif-featuremap-stack", "A feature-map stack is one map per filter",
  "Four square maps drawn one behind the other, going up and to the right, so they read as a shallow "
  "three-dimensional block. The depth is labelled 32 channels, a mono label reads shape 32 comma 32 "
  "comma 32, and a note says each map is 32 by 32.",
  "0 0 320 220",
  J(t(20, 28, "a feature-map stack: one map per filter", 12, MUT),
    _slab(48, -42, PANEL, GRID, 2),
    _slab(32, -28, PANEL, GRID, 2),
    _slab(16, -14, PANEL, GRID, 2),
    line(30, 86, 78, 44, GRID, 1.5, cap=False),
    line(140, 196, 188, 154, GRID, 1.5, cap=False),
    _slab(0, 0, DATA_F, DATA_S, 3),
    [line(30, y, 140, y, GRID, 1.5, cap=False) for y in (122, 158)],
    [line(x, 86, x, 196, GRID, 1.5, cap=False) for x in (66, 102)],
    line(190, 46, 206, 42, MUT, 1.5, cap=False),
    t(210, 44, "32 channels", 12, MUT),
    chip(170, 168, 140, "shape (32, 32, 32)"),
    t(85, 212, "each map is 32 &#215; 32", 12, MUT, "middle")),
  "Depth means CHANNELS, never batch. One filter, one map, and the count of maps equals the count of "
  "filters &mdash; say that out loud while pointing at the stack.")

# ================================================================== k-means trio
_KX = lambda x: round(24 + 15.5 * x, 1)
_KY = lambda y: round(166 - 14.6 * y, 1)
_PTS = dict(A=(1, 2), B=(2, 1), C=(2, 3), D=(8, 8), E=(9, 7), F=(7, 9))


def _kpanel(c1, c2, mus, line1, line2, unassigned=False):
    b = [line(24, 20, 24, 166, INK, 2, cap=False),
         line(24, 166, 179, 166, INK, 2, cap=False),
         centroid(34, 28, 6),
         t(46, 32, "= centroid", 12, MUT)]
    if unassigned:
        for n in "ABCDEF":
            x, y = _PTS[n]
            b.append(circ(_KX(x), _KY(y), 5, PAPER, INK, 2))
    else:
        for n in c1:
            x, y = _PTS[n]
            b.append(dot(_KX(x), _KY(y), 5, DATA_S))
        for n in c2:
            x, y = _PTS[n]
            b.append(tri(_KX(x), _KY(y), 6, OK_S))
    for mx, my in mus:
        b.append(centroid(_KX(mx), _KY(my), 8))
    b.append(t(95, 186, line1, 14, INK, "middle"))
    b.append(t(95, 204, line2, 12, MUT, "middle"))
    return J(b)


M("motif-kmeans-1", "k-means, the start: two centroids in one blob",
  "Six hollow points, three bunched at the bottom left and three at the top right. Two ringed cross-hair "
  "centroid markers both sit inside the bottom-left bunch, one of them right on top of a point. The "
  "caption reads Start, both centroids sit left.",
  "0 0 190 210",
  _kpanel("", "", [(1, 2), (2, 3)], "Start", "both centroids sit left", unassigned=True),
  "Panel 1 of 3. Points are HOLLOW because nothing has been assigned yet. Starting both centroids in "
  "one blob is deliberate: it is how a learner sees that where you start matters.")

M("motif-kmeans-2", "k-means, after one round: one point in the wrong cluster",
  "The same six points. Two at the bottom left are now filled circles; the other four, including the "
  "third bottom-left point, are triangles. The two centroid markers have moved apart. The caption reads "
  "After iteration 1, 2 and 4, C went right.",
  "0 0 190 210",
  _kpanel("AB", "CDEF", [(1.5, 1.5), (6.5, 6.75)], "After iteration 1", "2 and 4 &#8212; C went right"),
  "Panel 2 of 3. Cluster membership is a SHAPE, circle versus triangle &mdash; never two colours only. "
  "The obviously-wrong assignment is the point of this panel; do not tidy it up.")

M("motif-kmeans-3", "k-means, settled: three and three",
  "The same six points. All three bottom-left points are now filled circles and all three top-right "
  "points are triangles. Each centroid marker sits in the middle of its own group. The caption reads "
  "After iteration 2, 3 and 3, settled.",
  "0 0 190 210",
  _kpanel("ABC", "DEF", [(1.6667, 2.0), (8, 8)], "After iteration 2", "3 and 3 &#8212; settled"),
  "Panel 3 of 3. The points NEVER move between panels; only their shape and the centroids do. Print "
  "the counts in every caption so the reader can check the arithmetic.")

# ================================================================== PCA
_CLOUD = [(91.4, 195.2), (91.4, 165.2), (112.2, 169.6), (112.2, 139.6), (138.6, 154.8),
          (144.6, 132.8), (168.6, 139.8), (163.8, 108.4), (190.2, 113.6), (187, 86),
          (213.4, 91.2), (231.4, 85.2)]

M("motif-pca", "PCA draws new axes along the spread",
  "A long thin cloud of twelve points leaning up to the right. Two straight purple lines cross at the "
  "middle of the cloud: a long one along the cloud's length labelled PC1, the direction of most spread, "
  "and a short one across it labelled PC2, what is left over. One point has a short dashed line dropped "
  "onto the long axis, and the place it lands is ringed and labelled its PC1 value.",
  "0 0 320 270",
  J(line(40, 40, 40, 220, GRID, 1.5, cap=False),
    line(40, 220, 280, 220, GRID, 1.5, cap=False),
    t(20, 26, "PCA: new axes, chosen by spread", 12, MUT),
    line(75, 190, 235, 70, MODEL_S, 3),
    line(128, 94, 182, 166, MODEL_S, 3),
    [dot(x, y, 5, DATA_S) for x, y in _CLOUD],
    line(187, 86, 196.6, 98.8, ACC_S, 2, dash="4 3"),
    circ(196.6, 98.8, 7, PAPER, ACC_S, 3),
    t(250, 64, "PC1 &#8212; the direction of most spread", 12, MODEL_S, "end"),
    t(296, 182, "PC2 &#8212; what is left over", 12, MODEL_S, "end"),
    t(172, 82, "one point", 12, INK, "end"),
    arrow(226, 128, 204, 106, ACC_S, 1.5),
    t(290, 140, "its PC1 value", 12, ACC_S, "end"),
    t(160, 236, "feature 1", 12, MUT, "middle"),
    trot(26, 130, "feature 2", 12, MUT, "middle"),
    t(160, 256, "every point gets a PC1 value and a PC2 value", 12, MUT, "middle")),
  "The old axes stay on the page in grid grey. Without them 'new axes' means nothing. Project exactly "
  "ONE point, at right angles, and ring where it lands.")

# ================================================================== bag of words
_VOCAB = ("and", "cold", "food", "great", "pizza", "service", "the", "was")
_COUNTS = ("0", "0", "0", "2", "1", "1", "0", "0")
_bow = []
for _i, (_w, _c) in enumerate(zip(_VOCAB, _COUNTS)):
    _x = 266 + 18 * _i
    _hot = _c != "0"
    _bow.append(sq(_x, 80, 18, 36, ACC_F if _hot else PAPER, ACC_S if _hot else GRID,
                   3 if _hot else 1.5))
    _bow.append(t(_x + 9, 98, _c, 12, INK if _hot else MUT, "middle", central=True))
    _bow.append(trot(_x + 9, 74, _w, 12, MUT, "end"))

M("motif-bow-vector", "One sentence becomes one sparse row",
  "A box holding the sentence Great pizza, great service. An arrow labelled count leads to a row of "
  "eight narrow cells, one per vocabulary word, with the words written vertically above them. Five cells "
  "hold 0 in grey; the great cell holds 2 and the pizza and service cells hold 1, all outlined in pink. "
  "A note says five of eight cells are zero, so we store only the other three.",
  "0 0 420 200",
  J(rect(14, 80, 200, 36, 8, PANEL, INK, 2),
    t(114, 98, "Great pizza, great service.", 12, INK, "middle", central=True),
    arrow(222, 98, 254, 98, INK, 2.5),
    t(238, 86, "count", 12, MUT, "middle"),
    _bow,
    t(410, 132, "8 words in the vocabulary", 12, MUT, "end"),
    line(329, 118, 329, 132, ACC_S, 1.5, cap=False),
    t(329, 148, "great: 2", 12, ACC_S, "middle"),
    t(210, 176, "5 of 8 cells are zero, so we store only the other 3", 12, MUT, "middle"),
    t(210, 194, "TF-IDF replaces each count with count &#215; rarity", 12, MUT, "middle")),
  "The vocabulary words must be ON the cells &mdash; a row of bare numbers is not a lesson. Show the "
  "zeros: sparsity is the property that makes text different from a spreadsheet.")

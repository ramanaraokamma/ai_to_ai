"""Block C9 (weeks 25, 26, 27) extra figures: a mental-model figure, a worked-numbers figure and a
blank workbook figure per week. Every number is copied from the week's printed output or is a
hand sum printed beside it (STYLE.md 2.1).

W25  student-guide/week-25.md lsa.py (tf-idf matrix (15, 3906), index (15, 14), share kept 0.941,
     query "which optimiser was best" -> [1] 0.565, [0] 0.525, [2] 0.482); headline.py (scores, ranks and
     tied-note counts for three embedders on two queries); the blank is workbook page 25.3 Part 3
     (shape at each stage; no shapes drawn)
W26  student-guide/week-26.md section 8 (diagnose.py rule order); section 7 refuse.py sweep
     (answered k/10 for yours and for the stranger set, refused k/4 of the unanswerable);
     the blank is workbook page 26.2 (twelve letters, no points drawn)
W27  student-guide/week-27.md night-before table (what each week should leave); workbook page 27.3 grid
     (marks available 10, 6, 8, 13, 8, 4, 12, 14 = 75; redo line = int(0.6 x marks)); the blank is a
     confidence map for page 27.3 with no marks and no percentages drawn
"""
from _gen_core import *

FIGS = {}


def fig(name, vb, title, desc, parts):
    FIGS[name] = svg_doc(vb, title, desc, J(*parts))


def ctitle(s):
    return t(400, 44, s, 24, INK, "middle")


def cap(s, y=374):
    return t(400, y, s, 14, MUT, "middle")


def cap2(a, b, y=354):
    return [t(400, y, a, 14, MUT, "middle"), t(400, y + 18, b, 14, MUT, "middle")]


def lines_in(cx, y0, rows, size=12, fill=INK, lh=16, mono=False, anchor="middle"):
    return [t(cx, y0 + i * lh, s, size, fill, anchor, mono=mono) for i, s in enumerate(rows)]


# ---------------------------------------------------------------- W25-4  build once, ask many times
def w25_4():
    o = [ctitle("An index is built once and asked many times")]
    xs = [46 + i * 186 for i in range(4)]
    W, H = 150, 96
    # lane labels
    o.append(t(46, 72, "build, once (lsa.py: fit_embedder)", 14, MUT, "start"))
    o.append(t(46, 222, "ask, every question (encode, then search)", 14, MUT, "start"))
    yt, yb = 82, 232
    # connectors first
    for i in range(3):
        o.append(arrow(xs[i] + W + 2, yt + H / 2.0, xs[i + 1] - 4, yt + H / 2.0))
        o.append(arrow(xs[i] + W + 2, yb + H / 2.0, xs[i + 1] - 4, yb + H / 2.0))
    # the saved index feeds the multiply (elbow, dashed)
    o.append(poly([(xs[3] + W / 2.0, yt + H + 2), (xs[3] + W / 2.0, 206), (xs[2] + W / 2.0, 206),
                   (xs[2] + W / 2.0, yb - 8)], "none", MUT, 2, "6 4"))
    o.append(head(xs[2] + W / 2.0, yb - 2, 90, MUT, 2))
    o.append(t(xs[2] + W / 2.0 + 8, 202, "M is read, never changed", 12, MUT, "start"))
    # top lane
    top = [("15 notes", "text", "15 notes", DATA_S, DATA_F, None),
           ("Letter pieces", "TF-IDF, 3&#8211;5 letters", "(15, 3906)", DATA_S, DATA_F, None),
           ("SVD squeeze", "keeps 0.941 of spread", "(15, 14)", MODEL_S, MODEL_F, None),
           ("Normalise once", "every row length 1", "M  (15, 14)", DATA_S, DATA_F, None)]
    for x, (a, b, c, s, f, d) in zip(xs, top):
        o.append(rect(x, yt, W, H, 10, f, s, 3, d))
        o.append(t(x + W / 2.0, yt + 26, a, 18, INK, "middle"))
        o.append(t(x + W / 2.0, yt + 48, b, 12, MUT, "middle"))
        o.append(t(x + W / 2.0, yt + 76, c, 12, INK, "middle", mono=True))
    bot = [("A question", ["&#8220;which optimiser", "was best&#8221;"], "1 sentence", ACC_S, ACC_F),
           ("Same vec + svd", ["transform only,", "never fit"], "q  (14,)", MODEL_S, MODEL_F),
           ("M &#215; q", ["one matrix multiply,", "one score per note"], "(15,)", DATA_S, DATA_F),
           ("Top 3 ids", ["np.argsort(-sims)", "[:3]"], "[1] [0] [2]", DATA_S, DATA_F)]
    for x, (a, b, c, s, f) in zip(xs, bot):
        o.append(rect(x, yb, W, H, 10, f, s, 3))
        o.append(t(x + W / 2.0, yb + 24, a, 18, INK, "middle"))
        o.extend(lines_in(x + W / 2.0, yb + 44, b, 12, MUT, 15))
        o.append(t(x + W / 2.0, yb + 84, c, 12, INK, "middle", mono=True))
    o.extend(cap2("scores 0.565, 0.525, 0.482: the right note [0] came second.", "fit is for the notes; a question only ever gets transform."))
    fig("fig-w25-4-index-built-once-asked-many-times.svg", "0 0 800 400",
        "An index is built once from the notes, then each question is only encoded and multiplied against it",
        "Two rows of four boxes joined by arrows. Top row, built once: 15 notes, then letter pieces as a tf-idf table of shape "
        "(15, 3906), then an SVD squeeze to shape (15, 14) keeping 0.941 of the spread, then normalise once so every row has length 1, "
        "which gives the index M of shape (15, 14). Bottom row, for every question: the sentence 'which optimiser was best', then the same "
        "fitted vectorizer and SVD used with transform only to give a question vector of shape (14,), then one matrix multiply M times q "
        "giving 15 scores, then the top three ids 1, 0, 2 with scores 0.565, 0.525 and 0.482. A dashed line shows M feeding the multiply. "
        "The right note, 0, ranks second.", o)


# ---------------------------------------------------------------- W25-5  headline.py as bars
def w25_5():
    o = [ctitle("Where each embedder put the right note")]
    x0, sc = 270, 250.0
    cols = {"score": x0, "rank": 590, "tied": 690}
    o.append(t(x0, 70, "score of the right note (note 0)", 12, MUT, "start"))
    o.append(t(cols["rank"], 70, "rank", 12, MUT, "middle"))
    o.append(t(cols["tied"], 70, "notes sharing", 12, MUT, "middle"))
    o.append(t(cols["tied"], 84, "that exact score", 12, MUT, "middle"))
    data = [("query: optimiser", [("word tf-idf", 0.000, 1, 15), ("lsa (14 numbers)", 0.799, 1, 1),
                                   ("contrastive, seed 0", 0.429, 1, 1)]),
            ("query: which optimiser was best", [("word tf-idf", 0.000, 2, 14), ("lsa (14 numbers)", 0.525, 2, 1),
                                                  ("contrastive, seed 0", 0.377, 1, 1)])]
    y = 100
    panels = []
    for head_s, rows in data:
        panels.append((y, head_s, rows))
        y += 112
    ybot = 100 + 2 * 112 - 14
    for v in (0, 0.5, 1.0):
        o.append(line(x0 + v * sc, 96, x0 + v * sc, ybot, GRID, 1.5, "4 4" if v else None))
        o.append(t(x0 + v * sc, ybot + 18, ("%.1f" % v) if v else "0", 12, MUT, "middle"))
    o.append(t(x0 + sc / 2.0, ybot + 36, "cosine score", 12, MUT, "middle"))
    for py, head_s, rows in panels:
        o.append(t(40, py + 12, head_s, 14, INK, "start", mono=True))
        for i, (nm, sc_v, rk, tie) in enumerate(rows):
            yy = py + 22 + i * 30
            o.append(t(40, yy + 15, nm, 14, INK, "start"))
            w = sc_v * sc
            if w > 0:
                o.append(rect(x0, yy + 4, w, 20, 4, DATA_F, DATA_S, 2))
            else:
                o.append(line(x0, yy + 4, x0, yy + 24, DATA_S, 3))
            o.append(t(x0 + max(w, 0) + 10, yy + 19, "%.3f" % sc_v, 12, INK, "start"))
            o.append(t(cols["rank"], yy + 19, str(rk), 14, INK, "middle"))
            if tie > 1:
                o.append(rect(cols["tied"] - 24, yy + 3, 48, 22, 6, BAD_F, BAD_S, 2))
                o.append(t(cols["tied"], yy + 19, str(tie), 14, INK, "middle"))
            else:
                o.append(rect(cols["tied"] - 24, yy + 3, 48, 22, 6, PANEL, GRID, 2))
                o.append(t(cols["tied"], yy + 19, "1", 14, INK, "middle"))
    o.append(cap("the word table's rank 1 for &#8220;optimiser&#8221; is list order: 15 notes tied at 0.000.", 372))
    fig("fig-w25-5-optimiser-three-embedders.svg", "0 0 800 400",
        "A rank of 1 means nothing when every note has the same score",
        "Two panels of three bars each, the cosine score of the right note, note 0. For the query optimiser: word tf-idf scores 0.000, "
        "rank 1, with 15 notes sharing that exact score; lsa with 14 numbers scores 0.799, rank 1, alone; the contrastive embedder with "
        "seed 0 scores 0.429, rank 1, alone. For the query which optimiser was best: word tf-idf scores 0.000, rank 2, with 14 notes sharing "
        "the score; lsa scores 0.525, rank 2, alone; contrastive scores 0.377, rank 1, alone. The two tie counts of 15 and 14 are drawn in red boxes.", o)


# ---------------------------------------------------------------- W25-6  blank: shape at each stage
def w25_6():
    o = [ctitle("Shape at each stage of the index")]
    W, H = 220, 100
    xs = [30 + i * 255 for i in range(3)]
    ys = [74, 220]
    stages = [("1", "Letter-piece table", "vec.transform(chunks).shape", "shape"),
              ("2", "After the SVD squeeze", "the index M before searching", "shape"),
              ("3", "Length of one row of M", "after normalise, 3 decimals", "length"),
              ("4", "One question, encoded", "encode(vec, svd, [q])[0]", "shape"),
              ("5", "Scores, M @ q", "one number for each note", "shape"),
              ("6", "What argsort returns", "np.argsort(-sims)[:3]", "how many ids")]
    pos = []
    for r in range(2):
        for c in range(3):
            pos.append((xs[c], ys[r]))
    # connectors first: along each row, then down the right to the next row
    for r in range(2):
        for c in range(2):
            o.append(arrow(xs[c] + W + 3, ys[r] + H / 2.0, xs[c + 1] - 6, ys[r] + H / 2.0))
    o.append(poly([(xs[2] + W / 2.0, ys[0] + H + 3), (xs[2] + W / 2.0, 200), (xs[0] + W / 2.0, 200),
                   (xs[0] + W / 2.0, ys[1] - 8)], "none", INK, 3))
    o.append(head(xs[0] + W / 2.0, ys[1] - 3, 90, INK, 3))
    for (x, y), (n, a, b, slot) in zip(pos, stages):
        o.append(rect(x, y, W, H, 10, PANEL, DATA_S, 3))
        o.append(ring_num(x + 18, y + 20, n))
        if len(a) > 24:
            a1, a2 = a[:a.rfind(" ", 0, 24)], a[a.rfind(" ", 0, 24) + 1:]
            o.append(t(x + 38, y + 24, a1, 14, INK, "start"))
            o.append(t(x + 38, y + 41, a2, 14, INK, "start"))
        else:
            o.append(t(x + 38, y + 24, a, 14, INK, "start"))
            if b:
                o.append(t(x + 38, y + 41, b, 12, MUT, "start"))
        o.append(rect(x + 20, y + 58, W - 40, 28, 6, PAPER, MUT, 2, "6 4"))
        o.append(t(x + 28, y + 76, slot + ":", 12, MUT, "start"))
    o.extend(cap2("class notebook: 15 notes. Fill each dashed box from your own run,", "then check the Answers page.", 350))
    fig("fig-w25-6-blank-shape-at-each-stage.svg", "0 0 800 400",
        "Fill in the shape of the data at each of six stages of the index",
        "Blank worksheet. Six numbered boxes in two rows of three joined by arrows: the letter-piece table, the table after the SVD squeeze, "
        "the length of one row of the index after normalising, one question encoded, the scores from the matrix multiply, and what "
        "np.argsort(-sims)[:3] returns. Each box has an empty dashed answer box for the student to fill. No shapes are written in.", o)


# ---------------------------------------------------------------- W26-4  two homes for a wrong answer
def w26_4():
    o = [ctitle("A wrong answer has two homes")]
    W, H = 176, 84
    xs = [34, 254, 474]
    yd = 76
    yo = 222
    # connectors first
    for i in range(2):
        o.append(arrow(xs[i] + W + 3, yd + H / 2.0, xs[i + 1] - 6, yd + H / 2.0))
        o.append(t((xs[i] + W + xs[i + 1]) / 2.0, yd + H / 2.0 - 8, "no" if i == 0 else "yes", 12, MUT, "middle"))
    o.append(arrow(xs[2] + W + 3, yd + H / 2.0, 676, yd + H / 2.0))
    o.append(t((xs[2] + W + 676) / 2.0, yd + H / 2.0 - 8, "yes", 12, MUT, "middle"))
    for i in range(3):
        o.append(arrow(xs[i] + W / 2.0, yd + H + 3, xs[i] + W / 2.0, yo - 6))
    o.append(t(xs[0] + W / 2.0 + 8, 190, "yes", 12, MUT, "start"))
    o.append(t(xs[1] + W / 2.0 + 8, 190, "no", 12, MUT, "start"))
    o.append(t(xs[2] + W / 2.0 + 8, 190, "no", 12, MUT, "start"))
    # fix the first label: the gate's "no" goes right, its "yes" goes down
    dec = [("1", ["Is the best score", "below tau?"]),
           ("2", ["Is the right note", "among the k served?"]),
           ("3", ["Does the answer", "contain the fact?"])]
    for x, (n, ls) in zip(xs, dec):
        o.append(rect(x, yd, W, H, 10, DATA_F, DATA_S, 3))
        o.append(ring_num(x + 18, yd + 20, n))
        o.extend(lines_in(x + W / 2.0 + 8, yd + 34, ls, 14, INK, 20))
    outs = [("refused by", "the gate", PANEL, GRID, "nothing was written", None),
            ("RETRIEVAL failure", "", BAD_F, BAD_S, "change the index:", "chunking, embedder, k"),
            ("GENERATION failure", "", BAD_F, BAD_S, "change the writer", "or its prompt")]
    for x, (a, b, f, s, c, d) in zip(xs, outs):
        o.append(rect(x, yo, W, 86, 10, f, s, 3))
        if b:
            o.append(t(x + W / 2.0, yo + 38, a, 18, INK, "middle"))
            o.append(t(x + W / 2.0, yo + 60, b, 18, INK, "middle"))
            o.append(t(x + W / 2.0, yo + 78, c, 12, MUT, "middle"))
        else:
            o.append(t(x + W / 2.0, yo + 38, a, 16, INK, "middle"))
            o.append(t(x + W / 2.0, yo + 58, c, 12, INK, "middle"))
            o.append(t(x + W / 2.0, yo + 74, d, 12, INK, "middle"))
    o.append(cross(xs[1] + W - 16, yo + 14, 6))
    o.append(cross(xs[2] + W - 16, yo + 14, 6))
    # ok box
    o.append(rect(682, yd + 10, 84, 64, 10, OK_F, OK_S, 3))
    o.append(t(724, yd + 48, "ok", 18, INK, "middle"))
    o.append(tick(706, yd + 28, 8))
    o.append(t(400, 330, "Read the served notes first. Then change only the half that failed.", 14, INK, "middle"))
    o.append(cap("checked in this order (diagnose.py). The writer in this course is a stand-in, not a model.", 372))
    fig("fig-w26-4-two-homes-for-a-wrong-answer.svg", "0 0 800 400",
        "A wrong answer is a retrieval failure or a generation failure, found by checking three questions in order",
        "Three question boxes in a row, checked in order. 1: is the best score below tau? If yes the answer is refused by the gate; if no, go on. "
        "2: is the right note among the k served? If no, it is a RETRIEVAL failure, fixed by changing the index (chunking, embedder, k); if yes, go on. "
        "3: does the answer contain the fact? If no, it is a GENERATION failure, fixed by changing the writer or its prompt; if yes, the answer is ok. "
        "A line at the foot says to read the served notes first and change only the half that failed.", o)


# ---------------------------------------------------------------- W26-5  the tau sweep
def w26_5():
    o = [ctitle("Two kinds of mistake at each refusal line")]
    taus = [0.05, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30]
    yours = [10, 10, 10, 9, 8, 8, 8]       # refuse.py: yours answered k/10
    unans = [2, 2, 3, 3, 3, 4, 4]          # refuse.py: unanswerable refused k/4
    stran = [8, 8, 7, 3, 2, 1, 1]          # refuse.py: stranger answered k/10
    xb, per = 250, 46
    y0, rh = 118, 30
    o.append(t(xb - 14, 76, "answerable but refused", 12, BAD_S, "end"))
    o.append(t(xb - 14, 92, "(of 10 of yours)", 12, MUT, "end"))
    o.append(t(xb + 14, 76, "unanswerable, answered", 12, HUMAN_S, "start"))
    o.append(t(xb + 14, 92, "(of 4)", 12, MUT, "start"))
    o.append(t(452, 76, "total", 12, MUT, "middle"))
    o.append(t(452, 92, "mistakes", 12, MUT, "middle"))
    o.append(t(516, 76, "stranger wording answered", 12, MUT, "start"))
    o.append(t(516, 92, "(filled square = answered, of 10)", 12, MUT, "start"))
    o.append(t(70, 92, "tau", 12, MUT, "middle"))
    o.append(line(xb, y0 - 8, xb, y0 + rh * 7 - 4, INK, 2))
    best = min(range(7), key=lambda i: (10 - yours[i]) + (4 - unans[i]))
    assert taus[best] == 0.12
    for i, tau in enumerate(taus):
        y = y0 + i * rh
        lost, leak = 10 - yours[i], 4 - unans[i]
        tot = lost + leak
        if i == best:
            o.append(rect(24, y - 4, 752, rh - 2, 8, ACC_F, ACC_S, 3))
        o.append(t(70, y + 15, "%.2f" % tau, 14, INK, "middle"))
        if lost:
            o.append(rect(xb - lost * per, y + 2, lost * per, 18, 3, BAD_F, BAD_S, 2))
            o.append(t(xb - lost * per / 2.0, y + 15, str(lost), 12, INK, "middle"))
        else:
            o.append(t(xb - 12, y + 15, "0", 12, MUT, "end"))
        if leak:
            o.append(rect(xb, y + 2, leak * per, 18, 3, HUMAN_F, HUMAN_S, 2))
            o.append(t(xb + leak * per / 2.0, y + 15, str(leak), 12, INK, "middle"))
        else:
            o.append(t(xb + 12, y + 15, "0", 12, MUT, "start"))
        o.append(t(452, y + 16, str(tot), 14, INK, "middle"))
        for j in range(10):
            on = j < stran[i]
            o.append(sq(516 + j * 20, y + 3, 16, 16, DATA_F if on else PAPER, DATA_S if on else GRID, 2))
        o.append(t(516 + 10 * 20 + 6, y + 16, "%d/10" % stran[i], 12, INK, "start"))
    o.extend(cap2("tau 0.12 has the fewest mistakes (1), and no row has zero.", "The strictest row that refuses all four (0.25) answers 1 of 10 stranger questions.", 354))
    fig("fig-w26-5-refusal-line-two-mistakes.svg", "0 0 800 400",
        "No refusal line has zero mistakes, and a line tuned on your own wording fails on a stranger's",
        "Seven rows, one for each refusal line tau from 0.05 to 0.30. Each row has a red bar to the left for answerable questions that were refused "
        "and a gold bar to the right for unanswerable questions that were answered, then the total, then ten squares showing how many of the "
        "stranger set were answered. Rows: tau 0.05, 0 refused, 2 leaked, total 2, stranger 8 of 10. 0.10: 0, 2, total 2, 8. 0.12: 0, 1, total 1, 7, "
        "the best row, ringed. 0.15: 1, 1, total 2, 3. 0.20: 2, 1, total 3, 2. 0.25: 2, 0, total 2, 1. 0.30: 2, 0, total 2, 1.", o)


# ---------------------------------------------------------------- W26-6  blank threshold strip
def w26_6():
    o = [ctitle("The threshold strip: place the twelve questions")]
    x0, x1 = 90, 750
    X = lambda v: x0 + v / 0.70 * (x1 - x0)
    lanes = [(80, "answerable", "A B C D E G I J  (8)"), (190, "NOT in the notes", "F H K L  (4)")]
    for y, nm, letters in lanes:
        o.append(rect(24, y, 752, 90, 10, PANEL, GRID, 2))
        o.append(t(36, y + 22, nm, 14, INK, "start"))
        o.append(t(36, y + 40, letters, 12, MUT, "start", mono=True))
    for k in range(0, 15):
        v = k * 0.05
        major = (k % 2 == 0)
        o.append(line(X(v), 80, X(v), 280, GRID, 1.5, None if major else "3 5"))
    o.append(line(x0, 292, x1, 292, INK, 2))
    for k in range(0, 8):
        v = k / 10.0
        o.append(line(X(v), 292, X(v), 299, MUT, 1.5))
        o.append(t(X(v), 316, "%.1f" % v if v else "0", 12, MUT, "middle"))
    o.append(t((x0 + x1) / 2.0, 336, "similarity of the best note", 12, MUT, "middle"))
    o.append(rect(560, 346, 60, 22, 6, PAPER, MUT, 2, "6 4"))
    o.append(t(554, 362, "my line", 12, INK, "end"))
    o.append(rect(716, 346, 50, 22, 6, PAPER, MUT, 2, "6 4"))
    o.append(t(710, 362, "mistakes", 12, INK, "end"))
    o.append(t(36, 362, "left of the line = refused", 12, MUT, "start"))
    fig("fig-w26-6-blank-threshold-strip.svg", "0 0 800 400",
        "Place each question on the similarity scale, draw one refusal line, and count the mistakes",
        "Blank worksheet. A horizontal scale from 0 to 0.7 with two empty bands above it: one for the eight answerable questions A B C D E G I J "
        "and one for the four questions that are not in the notes, F H K L. No letters are placed. Two dashed answer boxes at the foot are for the "
        "student's line and the number of mistakes.", o)


# ---------------------------------------------------------------- W27-4  what each week should leave behind
def w27_4():
    o = [ctitle("What Weeks 19 to 26 should have left behind")]
    tiles = [(19, "Ablations", ["a no-mask row is a", "leak, not a result"], 10),
             (20, "Byte-pair merges", ["a merge joins a pair;", "bytes per token rises"], 6),
             (21, "Log-log line, 6ND", ["a prediction from the", "line is not a measurement"], 8),
             (22, "Masked loss, KL", ["masked loss: a different", "number; KL has an order"], 13),
             (23, "The harness", ["a floor beside the score;", "the guard stops late"], 8),
             (24, "Prompts, logit mask", ["a mask fixes the shape,", "not the sense"], 4),
             (25, "Embeddings", ["a cosine ignores length;", "ask who made it near"], 12),
             (26, "RAG", ["who wrote the questions?", "a valid citation proves", "only: it was served"], 14)]
    W, H = 174, 128
    for i, (wk, nm, ls, mk) in enumerate(tiles):
        c, r = i % 4, i // 4
        x, y = 26 + c * (W + 16), 66 + r * (H + 14)
        o.append(rect(x, y, W, H, 10, PANEL, DATA_S, 3))
        o.append(t(x + 14, y + 28, "Week %d" % wk, 18, INK, "start"))
        o.append(t(x + 14, y + 48, nm, 14, MUT, "start"))
        o.extend(lines_in(x + 14, y + 74, ls, 12, INK, 16, anchor="start"))
        o.append(rect(x + W - 76, y + 10, 64, 22, 6, PAPER, GRID, 2))
        o.append(t(x + W - 44, y + 25, "%d marks" % mk, 12, INK, "middle"))
    o.extend(cap2("one idea per week to be able to say aloud.", "Marks on the paper: 10 + 6 + 8 + 13 + 8 + 4 + 12 + 14 = 75.", 358))
    fig("fig-w27-4-what-each-week-leaves-behind.svg", "0 0 800 400",
        "Eight weeks, each with the one idea that should still be in your head and the marks it carries on the paper",
        "Eight tiles in two rows of four, one for each of Weeks 19 to 26. Week 19 ablations: a no-mask row is a leak, not a result; 10 marks. "
        "Week 20 byte-pair merges: a merge joins a pair and bytes per token rises; 6 marks. Week 21 log-log line and 6ND: a prediction from the line "
        "is not a measurement; 8 marks. Week 22 masked loss and KL: a masked loss is a different number, and KL has an order; 13 marks. "
        "Week 23 the harness: a floor beside the score, and the guard stops late; 8 marks. Week 24 prompts and logit mask: a mask fixes the shape, not the sense; 4 marks. "
        "Week 25 embeddings: a cosine ignores length; 12 marks. Week 26 RAG: who wrote the questions, and a valid citation proves only that the note was served; 14 marks. "
        "The marks add to 75.", o)


# ---------------------------------------------------------------- W27-5  marks per week and the redo line
def w27_5():
    o = [ctitle("From marks available to the redo line")]
    weeks = [19, 20, 21, 22, 23, 24, 25, 26]
    marks = [10, 6, 8, 13, 8, 4, 12, 14]
    assert sum(marks) == 75
    redo = [int(m * 0.6 + 1e-9) for m in marks]
    assert redo == [6, 3, 4, 7, 4, 2, 7, 8]
    sums = ["0.6 &#215; 10 = 6.0", "0.6 &#215; 6 = 3.6", "0.6 &#215; 8 = 4.8", "0.6 &#215; 13 = 7.8",
            "0.6 &#215; 8 = 4.8", "0.6 &#215; 4 = 2.4", "0.6 &#215; 12 = 7.2", "0.6 &#215; 14 = 8.4"]
    x0, per, y0, rh = 110, 22, 100, 26
    o.append(t(40, 78, "week", 12, MUT, "start"))
    o.append(t(x0, 78, "marks available (one block = 1 mark)", 12, MUT, "start"))
    o.append(t(540, 78, "redo line (rounded down)", 12, MUT, "start"))
    for i, (wk, m, r, s) in enumerate(zip(weeks, marks, redo, sums)):
        y = y0 + i * rh
        o.append(t(40, y + 17, "Week %d" % wk, 14, INK, "start"))
        o.append(rect(x0, y + 2, r * per, 20, 3, BAD_F, BAD_S, 2))
        o.append(rect(x0 + r * per, y + 2, (m - r) * per, 20, 3, OK_F, OK_S, 2))
        o.append(t(x0 + m * per + 10, y + 18, str(m), 14, INK, "start"))
        o.append(t(540, y + 18, s, 14, INK, "start", mono=True))
        o.append(t(740, y + 18, "&#8594; %d" % r, 14, INK, "end"))
    yb = y0 + 8 * rh + 4
    o.append(line(40, yb, 760, yb, INK, 2))
    o.append(t(40, yb + 22, "total", 14, INK, "start"))
    o.append(t(x0, yb + 22, "10 + 6 + 8 + 13 + 8 + 4 + 12 + 14 = 75", 14, INK, "start"))
    # key
    o.append(rect(540, yb + 8, 16, 16, 3, BAD_F, BAD_S, 2))
    o.append(t(562, yb + 21, "marks at or under the line", 12, MUT, "start"))
    o.append(rect(540, yb + 28, 16, 16, 3, OK_F, OK_S, 2))
    o.append(t(562, yb + 41, "marks above it", 12, MUT, "start"))
    fig("fig-w27-5-marks-and-the-redo-line.svg", "0 0 800 400",
        "Each week's redo line is 60 percent of its marks, rounded down",
        "Eight bars, one per week, each as long as the marks available: Week 19, 10; Week 20, 6; Week 21, 8; Week 22, 13; Week 23, 8; Week 24, 4; "
        "Week 25, 12; Week 26, 14; total 75. Each bar is split at the redo line, marks at or under it in red and marks above it in green. "
        "The hand sums beside the bars are 0.6 times the marks, rounded down: 6.0 gives 6, 3.6 gives 3, 4.8 gives 4, 7.8 gives 7, 4.8 gives 4, "
        "2.4 gives 2, 7.2 gives 7, 8.4 gives 8.", o)


# ---------------------------------------------------------------- W27-6  blank confidence map
def w27_6():
    o = [ctitle("Confidence map: how sure did I feel?")]
    rows = [(19, "Ablations; the mask leak; heads"), (20, "BPE: bytes, merges, bytes per token"),
            (21, "The log-log line; 6ND"), (22, "Masked loss; pair loss; KL; the leash"),
            (23, "The harness: floor, frozen set, guard"), (24, "Examples in the prompt; the logit mask"),
            (25, "Cosine; recall"), (26, "RAG: top k, citations, chunk size")]
    cx = [440, 490, 540, 590]
    labels = ["lost", "shaky", "fair", "solid"]
    y0, rh = 104, 28
    for lab, x in zip(labels, cx):
        o.append(t(x, 88, lab, 12, MUT, "middle"))
    o.append(t(40, 88, "week and what it covers", 12, MUT, "start"))
    o.append(t(665, 82, "my % from", 12, MUT, "middle"))
    o.append(t(665, 96, "the grid", 12, MUT, "middle"))
    o.append(t(740, 82, "redo?", 12, MUT, "middle"))
    o.append(t(740, 96, "(ring)", 12, MUT, "middle"))
    for i, (wk, topic) in enumerate(rows):
        y = y0 + i * rh
        if i % 2 == 0:
            o.append(rect(24, y - 2, 752, rh - 2, 6, PANEL, PANEL, 1))
        o.append(t(40, y + 17, "Week %d" % wk, 14, INK, "start"))
        o.append(t(112, y + 17, topic, 12, MUT, "start"))
        for x in cx:
            o.append(circ(x, y + 13, 10, PAPER, MUT, 2))
        o.append(rect(636, y + 1, 58, 24, 6, PAPER, MUT, 2, "6 4"))
        o.append(circ(740, y + 13, 12, PAPER, MUT, 2))
    o.extend(cap2("shade one circle per week before you mark;", "then fill the % from your grid and ring at most two weeks.", 352))
    fig("fig-w27-6-blank-confidence-map.svg", "0 0 800 400",
        "Rate how sure you felt about each week, then set it beside the percentage from your grid",
        "Blank worksheet. Eight rows, one for each of Weeks 19 to 26 with its topic. Each row has four empty circles labelled lost, shaky, fair "
        "and solid for the student to shade one, an empty dashed box for the percentage from the grid, and an empty ring for circling the week to redo. "
        "Nothing is filled in.", o)


def build():
    for f in (w25_4, w25_5, w25_6, w26_4, w26_5, w26_6, w27_4, w27_5, w27_6):
        f()
    return FIGS

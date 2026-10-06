"""Block 9 figures: weeks 25, 26, 27 (concept figures fig-wNN-K-*.svg, K >= 1).

Every number printed on a canvas is copied from the week's executed output in the student guide
(provenance in the comment above each figure) or is a hand sum printed beside it (STYLE 2.1).
emit(figures_dir) is called from _gen_build.py.  Deterministic: no randomness at all.
"""
import os
from _gen_core import *


def _title(s, y=44):
    return t(400, y, s, 24, INK, "middle")


# ---------------------------------------------------------------- week 25, figure 1
# Source: week-25 cosine.py output: A.C = 4.0, |A| = 3.162, |C| = 4.472, cos(A,B) = 1.000,
# cos(A,C) = 0.283, cos(B,C) = 0.283.  Hand sum on canvas: 1x4 + 0x2 + 3x0 = 4.
def w25_1():
    o = [_title("A cosine ignores length")]
    vecs = [("A", [1, 0, 3], 96), ("B", [2, 0, 6], 148), ("C", [4, 2, 0], 200)]
    for name, vals, y in vecs:
        o.append(t(52, y + 26, name, 18, INK, "middle"))
        for i, v in enumerate(vals):
            x = 74 + i * 46
            o.append(sq(x, y, 46, 38, DATA_F, DATA_S, 2))
            o.append(t(x + 23, y + 19, str(v), 18, INK, "middle", central=True))
        o.append(shape_chip(222, y + 6, "(3,)"))
    o.append(t(284, 174, "B = 2 &#215; A", 14, ACC_S, "start"))
    o.append(rect(30, 252, 380, 92, 12, PANEL, GRID, 1.5))
    o.append(t(46, 278, "A &#183; C = 1&#215;4 + 0&#215;2 + 3&#215;0 = 4", 14, INK))
    o.append(t(46, 302, "|A| = 3.162    |C| = 4.472", 14, INK))
    o.append(t(46, 326, "cos(A, C) = 4 &#247; (3.162 &#215; 4.472) = 0.283", 14, INK))
    o.append(t(600, 96, "cosine of each pair", 18, INK, "middle"))
    x0, sc = 480, 240
    o.append(line(x0, 112, x0, 252, MUT, 1.5))
    o.append(t(x0, 270, "0", 12, MUT, "middle"))
    o.append(t(x0 + sc, 270, "1", 12, MUT, "middle"))
    for lab, v, y, ring in [("A, B", 1.000, 124, True), ("A, C", 0.283, 172, False), ("B, C", 0.283, 220, False)]:
        o.append(t(x0 - 10, y + 22, lab, 14, INK, "end"))
        o.append(rect(x0, y, v * sc, 30, 4, ACC_F if ring else DATA_F, ACC_S if ring else DATA_S, 3 if ring else 2))
        o.append(t(x0 + v * sc + 8 if v < 0.9 else x0 + v * sc - 8, y + 21, "%.3f" % v, 14, INK,
                   "start" if v < 0.9 else "end"))
    o.append(t(400, 372, "Same direction, twice the length: the cosine is 1.000. Length is divided out.", 14, MUT, "middle"))
    return svg_doc("0 0 800 400",
                   "A cosine compares direction and ignores length: B is twice A, so cos(A, B) is 1.000",
                   "Three three-number vectors: A is 1, 0, 3; B is 2, 0, 6, which is 2 times A; C is 4, 2, 0, each with shape (3,). "
                   "Worked sum: A dot C is 1 times 4 plus 0 times 2 plus 3 times 0, which is 4; the lengths are 3.162 and 4.472, "
                   "so cos(A, C) is 0.283. A bar chart gives cos(A, B) 1.000, cos(A, C) 0.283 and cos(B, C) 0.283.",
                   "\n".join("  " + s for s in o))


# ---------------------------------------------------------------- week 25, figure 2
# Source: week-25 recall.py (word tf-idf 0.67/0.73, lsa dim 14 0.73/1.00), seeds.py (150 steps, mean of
# seeds 0-4: 0.63/0.89, recall@1 range 0.47-0.73), untrained.py (1 step: 0.48/0.73) and chance 1/15, 3/15.
def w25_2():
    o = [_title("Recall needs a control beside it")]
    # legend
    o.append(rect(270, 62, 28, 14, 2, DATA_F, DATA_S, 2))
    o.append(t(306, 74, "recall@1 (top 1)", 12, MUT))
    o.append(rect(440, 62, 28, 14, 2, PANEL, DATA_S, 2))
    o.append(t(476, 74, "recall@3 (top 3)", 12, MUT))
    x0, sc = 270, 440
    rows = [("pure chance", "1 &#247; 15 and 3 &#247; 15", 0.07, 0.20, "grid", None),
            ("word tf-idf", "", 0.67, 0.73, "data", None),
            ("contrastive, 1 step", "the control, mean of 5 seeds", 0.48, 0.73, "model", None),
            ("contrastive, 150 steps", "mean of 5 seeds", 0.63, 0.89, "model", (0.47, 0.73)),
            ("lsa, 14 numbers", "", 0.73, 1.00, "data", None)]
    pal = {"grid": (PANEL, GRID, "6 4"), "data": (DATA_F, DATA_S, None), "model": (MODEL_F, MODEL_S, None)}
    o.append(line(x0, 90, x0, 352, MUT, 1.5))
    for i, (lab, sub, r1, r3, role, wh) in enumerate(rows):
        y = 100 + i * 52
        o.append(t(x0 - 14, y + 17 if sub else y + 24, lab, 14, INK, "end"))
        if sub:
            o.append(t(x0 - 14, y + 33, sub, 12, MUT, "end"))
        f, s, d = pal[role]
        o.append(rect(x0, y, r1 * sc, 18, 3, f, s, 3 if role == "model" else 2, d))
        o.append(rect(x0, y + 20, r3 * sc, 18, 3, PANEL, s, 2, d))
        end1 = x0 + r1 * sc
        if wh:
            a, b = x0 + wh[0] * sc, x0 + wh[1] * sc
            o.append(line(a, y + 9, b, y + 9, INK, 2))
            o.append(line(a, y + 3, a, y + 15, INK, 2))
            o.append(line(b, y + 3, b, y + 15, INK, 2))
            end1 = b
        txt1 = "%.2f" % r1 + ("  seeds %.2f&#8211;%.2f" % wh if wh else "")
        o.append(t(end1 + 8, y + 14, txt1, 12, INK))
        o.append(t(x0 + r3 * sc + 8, y + 34, "%.2f" % r3, 12, INK))
    o.append(t(400, 376, "Training adds 0.63 &#8722; 0.48 = 0.15 at recall@1 over the one-step control.", 14, MUT, "middle"))
    return svg_doc("0 0 800 400",
                   "A recall number only means something beside its control: one training step already gets recall@3 0.73",
                   "Paired horizontal bars for recall@1 and recall@3 on 15 questions. Pure chance 0.07 and 0.20. Word tf-idf 0.67 and 0.73. "
                   "Contrastive embedder after one training step, mean of 5 seeds, 0.48 and 0.73. Contrastive after 150 steps, mean of 5 seeds, "
                   "0.63 and 0.89, with recall@1 ranging from 0.47 to 0.73 across seeds. LSA with 14 numbers 0.73 and 1.00.",
                   "\n".join("  " + s for s in o))


# ---------------------------------------------------------------- week 26, figure 1
# Source: week-26 refuse.py (tau 0.12: 3 of 4 unanswerable refused) and faults.py (question about NaN:
# served ids [1, 8, 2], answer cites [8], check (True, [8], []), the right note is 1).
def w26_1():
    xs = [44 + i * 148 for i in range(5)]
    bw, by, bh = 120, 100, 80
    o = [_title("Retrieve, gate, write, check")]
    cy = by + bh / 2
    for i in range(4):
        o.append(arrow(xs[i] + bw + 2, cy, xs[i + 1] - 4, cy, INK, 3))
    o.append(arrow(xs[2] + bw / 2, by + bh + 2, xs[2] + bw / 2, 221, INK, 3))
    o.append(arrow(xs[1] + bw / 2, by + bh + 2, xs[1] + bw / 2, 215, INK, 3))
    o.append(arrow(xs[4] + bw / 2, by + bh + 2, xs[4] + bw / 2, 211, INK, 3))
    names = [("Question", HUMAN_F, HUMAN_S), ("Retrieve", DATA_F, DATA_S), ("Gate", PANEL, INK), ("Write", None, None),
             ("Check", OK_F, OK_S)]
    for (n, f, s), x in zip(names, xs):
        if n == "Write":
            o.append(stand_in_frame(x, by, bw, bh))
        else:
            o.append(rect(x, by, bw, bh, 10, f, s, 3))
        o.append(t(x + bw / 2, cy, n, 18, INK, "middle", central=True))
    o.append(t(xs[0] + bw / 2, by + bh + 22, "your words", 12, MUT, "middle"))
    for k, x in enumerate((192, 236, 280)):
        o.append(rect(x, 215, 40, 30, 6, DATA_F, DATA_S, 2))
        o.append(t(x + 20, 230, ["[1]", "[8]", "[2]"][k], 12, INK, "middle", central=True, mono=True))
    o.append(t(252, 266, "top 3 served", 12, MUT, "middle"))
    o.append(rect(340, 221, 120, 50, 10, PANEL, INK, 2))
    o.append(t(400, 246, "NOT IN NOTES", 14, INK, "middle", central=True))
    o.append(t(400, 290, "if best score &lt; tau", 12, MUT, "middle"))
    o.append(t(400, 308, "tau = 0.12: 3 of 4", 12, INK, "middle"))
    o.append(t(400, 324, "unanswerable refused", 12, INK, "middle"))
    o.append(rect(500, 211, 280, 150, 12, PANEL, GRID, 1.5))
    o.append(t(516, 232, "What learning rate made", 12, MUT))
    o.append(t(516, 247, "the loss go to NaN?", 12, MUT))
    o.append(t(516, 270, "served ids [1, 8, 2]", 14, INK))
    o.append(t(516, 288, "answer cites [8]", 14, INK))
    o.append(tick(526, 312, 9))
    o.append(t(546, 317, "check passes: 8 served", 14, INK))
    o.append(cross(526, 340, 7))
    o.append(t(546, 345, "the right note was 1, not 8", 14, INK))
    o.append(t(400, 376, "A passing check proves the id was served. It cannot prove the answer is right.", 14, MUT, "middle"))
    return svg_doc("0 0 800 400",
                   "A refusal gate and a citation check stop some failures, but a valid citation can still sit on a wrong answer",
                   "Five boxes left to right: Question, Retrieve, Gate, Write and Check. Write is dashed with the chip stand-in, not a model. "
                   "Retrieve serves three numbered sources 1, 8 and 2. Below Gate a box reads NOT IN NOTES: at tau 0.12 three of four "
                   "unanswerable questions are refused. Below Check, a question about NaN was served ids 1, 8, 2; the answer cites 8, the check "
                   "passes because 8 was served, but the right note is 1.",
                   "\n".join("  " + s for s in o if s))


# ---------------------------------------------------------------- week 26, figure 2
# Source: week-26 chunking.py output table (five cuts of one notebook, ten questions).
def w26_2():
    o = [_title("Recall, and what it cost in words")]
    rows = [("by note", "15 chunks, 45.3 words", 21, 146, (1.00, 1.00, 1.00)),
            ("30 words, overlap 8", "31 chunks, 29.9 words", 13, 90, (0.80, 0.90, 1.00)),
            ("60 words, overlap 15", "15 chunks, 59.9 words", 26, 180, (0.90, 1.00, 1.00)),
            ("120 words, overlap 0", "6 chunks, 114.7 words", 51, 354, (0.90, 1.00, 1.00)),
            ("250 words, overlap 50", "4 chunks, 209.5 words", 104, 718, (1.00, 1.00, 1.00))]
    x0, sc = 250, 250
    o.append(t(x0, 84, "share of the notebook sent per question (k = 3)", 12, MUT))
    for j, (cx, h) in enumerate(zip((676, 716, 754), ("r@1", "r@3", "r@5"))):
        o.append(t(cx, 84, h, 12, MUT, "middle"))
    o.append(line(x0 + sc, 94, x0 + sc, 338, MUT, 1.5, "6 4"))
    o.append(t(x0 + sc, 356, "100% = the whole notebook", 12, MUT, "middle"))
    for i, (lab, sub, pct, words, rc) in enumerate(rows):
        y = 100 + i * 48
        over = pct > 100
        o.append(t(x0 - 12, y + 15, lab, 14, INK, "end"))
        o.append(t(x0 - 12, y + 31, sub, 12, MUT, "end"))
        o.append(rect(x0, y + 2, pct / 100.0 * sc, 28, 4, BAD_F if over else DATA_F, BAD_S if over else DATA_S, 3 if over else 2))
        tx = x0 + pct / 100.0 * sc + 8
        o.append(t(tx, y + 21, "%d%% &#183; %d words" % (pct, words), 12, INK))
        for cx, v in zip((676, 716, 754), rc):
            o.append(t(cx, y + 22, "%.2f" % v, 14, INK, "middle"))
        if over:
            o.append(cross(x0 + 14, y + 16, 6))
    o.append(t(400, 376, "250-word chunks reach 1.00 by sending 104% of the notebook: nothing was retrieved.", 14, MUT, "middle"))
    return svg_doc("0 0 800 400",
                   "A perfect recall bought by sending the whole notebook is not retrieval: report words sent beside recall",
                   "Five rows, one per way of cutting the same notebook, each with a bar for the share of the notebook sent at k equals 3 and "
                   "the recall at 1, 3 and 5 on ten questions. By note: 21 percent, 146 words, recall 1.00 1.00 1.00. 30 words overlap 8: 13 percent, "
                   "90 words, 0.80 0.90 1.00. 60 words overlap 15: 26 percent, 180 words, 0.90 1.00 1.00. 120 words: 51 percent, 354 words, 0.90 1.00 1.00. "
                   "250 words overlap 50: 104 percent, 718 words, 1.00 1.00 1.00, drawn past the 100 percent line and marked with a cross.",
                   "\n".join("  " + s for s in o))


# ---------------------------------------------------------------- week 27, figure 1
# Source: week-27 'What is on the paper' table; hand sum 20 + 16 + 12 + 15 + 12 = 75.
def w27_1():
    o = [_title("The paper: 75 marks in five sections")]
    secs = [("A", 20, ["20 multiple", "choice"], 15), ("B", 16, ["8 what does", "this print?"], 15),
            ("C", 12, ["4 find", "the bug"], 10), ("D", 15, ["3 pieces of", "arithmetic"], 15),
            ("E", 12, ["1 longer", "question on", "real tables"], 13)]
    x = 60
    for L, m, desc, mins in secs:
        w = m * 9
        last = L == "E"
        o.append(sq(x, 110, w, 90, ACC_F if last else DATA_F, ACC_S if last else DATA_S, 4 if last else 2))
        o.append(t(x + w / 2, 142, L, 24, INK, "middle"))
        o.append(t(x + w / 2, 178, "%d marks" % m, 14, INK, "middle"))
        for k, d in enumerate(desc):
            o.append(t(x + w / 2, 228 + k * 17, d, 12, MUT, "middle"))
        o.append(t(x + w / 2, 290, "%d min" % mins, 14, INK, "middle"))
        x += w
    o.append(bracket(60, 735, 100, 8, MUT))
    o.append(t(397, 84, "Weeks 19&#8211;26, as an X-ray, not a grade", 14, MUT, "middle"))
    o.append(t(735, 322, "start E with about 13 minutes left", 12, ACC_S, "end"))
    o.append(rect(30, 338, 740, 32, 8, PANEL, GRID, 1.5))
    o.append(t(400, 359, "20 + 16 + 12 + 15 + 12 = 75 marks  &#183;  70 minutes  &#183;  pen and calculator, no computer", 14, INK, "middle"))
    return svg_doc("0 0 800 400",
                   "The paper spreads 75 marks over five sections, and the biggest single question comes last",
                   "One bar split into five blocks wide in proportion to their marks. A is 20 marks of multiple choice, 15 minutes. "
                   "B is 16 marks, 8 what-does-this-print questions, 15 minutes. C is 12 marks, 4 find-the-bug questions, 10 minutes. "
                   "D is 15 marks, 3 pieces of arithmetic, 15 minutes. E is 12 marks, one longer question on real tables, 13 minutes, "
                   "highlighted. Beneath: 20 plus 16 plus 12 plus 15 plus 12 equals 75 marks in 70 minutes.",
                   "\n".join("  " + s for s in o))


# ---------------------------------------------------------------- week 27, figure 2
# Source: week-27 remediation table ('Why Term 4 needs it') and 'What carries into next week'.
def w27_2():
    o = [t(30, 46, "Term 3 (Weeks 19&#8211;26)", 14, MUT), t(770, 46, "what needs it", 14, MUT, "end")]
    left = [(19, "ablation, leak", ["L"]), (20, "BPE merge, bytes", [29]), (21, "log-log, 6ND", ["L"]),
            (22, "mask, KL, leash", ["L"]), (23, "harness, guard", [28, 29, 30]), (24, "prompt, logit mask", [28]),
            (25, "cosine, top k", [29]), (26, "RAG, citations", [28, 29])]
    crit = {22, 23, 26}
    right = {28: (70, "Week 28", "tools and fences"), 29: (148, "Week 29", "agent cost, mini RAG, attack"),
             30: (226, "Week 30", "evals on the frozen set"), "L": (304, "Later weeks", "fine-tune check, cost budget")}
    ly = lambda i: 62 + i * 40 + 15
    for i, (wk, _, tg) in enumerate(left):
        for g in tg:
            ry = right[g][0] + 30
            hot = wk in crit
            o.append(line(320, ly(i), 500, ry, ACC_S if hot else INK, 3 if hot else 1.5))
    for i, (wk, txt, _) in enumerate(left):
        hot = wk in crit
        o.append(rect(30, 62 + i * 40, 290, 30, 8, ACC_F if hot else PANEL, ACC_S if hot else GRID, 3 if hot else 2))
        o.append(t(44, ly(i), "%d  %s" % (wk, txt), 14, INK, central=True))
        if hot:
            o.append(t(310, ly(i), "redo first", 12, ACC_S, "end", central=True))
    for key, (y, a, b) in right.items():
        o.append(rect(500, y, 270, 60, 10, DATA_F, DATA_S, 3))
        o.append(t(514, y + 22, a, 18, INK))
        o.append(t(514, y + 44, b, 12, MUT))
    return svg_doc("0 0 800 400",
                   "Weeks 22, 23 and 26 are the ones Term 4 leans on hardest, so they are the first redos",
                   "Eight boxes on the left, Weeks 19 to 26 with their topics, joined by lines to four boxes on the right: Week 28 tools and fences, "
                   "Week 29 agent cost, mini RAG and attack, Week 30 evals on the frozen set, and later weeks. Week 23 joins Weeks 28, 29 and 30; "
                   "Week 26 joins Weeks 28 and 29; Week 24 joins 28; Weeks 20 and 25 join 29; Weeks 19, 21 and 22 join later weeks. "
                   "Weeks 22, 23 and 26 are drawn with heavy pink boxes and lines and the tag redo first.",
                   "\n".join("  " + s for s in o if s))


FIGS = [("fig-w25-1-cosine-ignores-length.svg", w25_1),
        ("fig-w25-2-recall-beside-its-control.svg", w25_2),
        ("fig-w26-1-retrieve-gate-write-check.svg", w26_1),
        ("fig-w26-2-recall-and-words-sent.svg", w26_2),
        ("fig-w27-1-the-paper-in-marks.svg", w27_1),
        ("fig-w27-2-term-3-feeds-term-4.svg", w27_2)]


def emit(figures_dir):
    for name, fn in FIGS:
        open(os.path.join(figures_dir, name), "w").write(fn() + "\n")
    return len(FIGS)

#!/usr/bin/env python3
"""Figures for projects/capstone.md. Same contract as figures/STYLE.md."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gen_assessments import (  # noqa: E402
    DATA_S, DATA_F, MODEL_S, MODEL_F, HUMAN_S, HUMAN_F, OK_S, OK_F,
    BAD_S, BAD_F, ACC_S, ACC_F, INK, MUTED, GRID, PANEL, PAPER,
    SANS, MONO, txt, box, line, arrow, tick, cross, svg,
)


# =============================================== CAP.1 the three-week map
def fig_cap_1():
    b = []
    b.append(txt(400, 40, "Three weeks, seven milestones, about 11 hours",
                 24, INK, "middle"))

    weeks = [
        ("WEEK 34", "Question and data", ["1 · Lock the question", "2 · Collect 100+ rows",
                                          "3 · Clean it + the log"], "4 h 15", DATA_S, DATA_F),
        ("WEEK 35", "Charts and models", ["4 · Five charts, in order",
                                          "5 · One split, 4 models",
                                          "6 · What I got wrong"], "4 h 45", MODEL_S, MODEL_F),
        ("WEEK 36", "Tell it to a room", ["7 · Assemble the story",
                                          "  · Rehearse out loud",
                                          "  · SHOWCASE DAY"], "2 h", HUMAN_S, HUMAN_F),
    ]
    x0, w, gap = 40, 226, 21
    for i, (wk, sub, items, hrs, s, f) in enumerate(weeks):
        bx = x0 + i * (w + gap)
        b.append(box(bx, 82, w, 214, f, s, 3, 12))
        b.append(txt(bx + w / 2, 110, wk, 18, INK, "middle"))
        b.append(txt(bx + w / 2, 132, sub, 14, MUTED, "middle"))
        b.append(line(bx + 20, 146, bx + w - 20, 146, s, 1.5))
        for j, it in enumerate(items):
            b.append(txt(bx + 22, 174 + j * 26, it, 14, INK))
        b.append(box(bx + 22, 246, w - 44, 34, PAPER, s, 2, 8))
        b.append(txt(bx + w / 2, 263, hrs + " of work", 14, INK, "middle", central=True))
        if i < 2:
            b.append(arrow(bx + w + 2, 189, bx + w + gap - 2, 189, INK, 3))

    b.append(f'<rect x="40" y="312" width="720" height="44" rx="10" fill="{BAD_F}" '
             f'stroke="{BAD_S}" stroke-width="3" stroke-linejoin="round"/>')
    b.append(txt(400, 334, "The order is not negotiable. You cannot hold out rows AFTER you have trained on them.",
                 14, INK, "middle", central=True))
    b.append(txt(400, 382, "Add an hour of slack per week. You will need it, and everybody does.",
                 12, MUTED, "middle"))
    svg("fig-cap-1-three-week-map.svg", "0 0 800 400",
        "Three weeks, seven milestones, about 11 hours",
        "Three panels. Week 34, question and data: lock the question, collect 100 plus rows, clean it and write the log, 4 hours 15. Week 35, charts and models: five charts in order, one split and four models, what I got wrong, 4 hours 45. Week 36, tell it to a room: assemble the story, rehearse out loud, showcase day, 2 hours. A red band warns that the order is not negotiable because you cannot hold out rows after you have trained on them.",
        b)


# ========================================== CAP.2 one split, made once
def fig_cap_2():
    b = []
    b.append(txt(400, 38, "One split. Made once. Used by everything.", 24, INK, "middle"))

    # LEFT: the wrong way
    b.append(box(32, 72, 344, 250, BAD_F, BAD_S, 3, 12))
    b.append(txt(204, 98, "✗   WHAT GOES WRONG", 14, INK, "middle", weight="600"))
    wrong = ["model A: split ... fit ... score", "model B: split ... fit ... score",
             "model C: split ... fit ... score"]
    for i, ln in enumerate(wrong):
        b.append(box(52, 116 + i * 46, 304, 36, PAPER, BAD_S, 2, 8))
        b.append(txt(64, 134 + i * 46, ln, 12, INK, font=MONO, central=True))
    b.append(txt(204, 272, "Three different test sets.", 12, INK, "middle"))
    b.append(txt(204, 290, "The table compares nothing.", 12, INK, "middle"))
    b.append(txt(204, 310, "No error. No warning.", 12, BAD_S, "middle"))

    # RIGHT: the right way
    b.append(box(424, 72, 344, 250, OK_F, OK_S, 3, 12))
    b.append(txt(596, 98, "✓   WHAT TO DO", 14, INK, "middle", weight="600"))
    b.append(box(444, 116, 304, 36, PAPER, OK_S, 3, 8))
    b.append(txt(456, 134, "X_train, X_test, y_train, y_test =", 12, INK, font=MONO, central=True))
    b.append(txt(596, 168, "ONE cell. Near the top. Never again.", 12, INK, "middle"))
    for i, ln in enumerate(["baseline  ->  scored on X_test",
                            "model A   ->  scored on X_test",
                            "model B   ->  scored on X_test",
                            "model C   ->  scored on X_test"]):
        b.append(txt(462, 194 + i * 22, ln, 12, INK, font=MONO))
    b.append(txt(596, 306, "One test set. The table is a comparison.", 12, OK_S, "middle"))

    b.append(f'<rect x="32" y="336" width="736" height="44" rx="10" fill="{PANEL}" '
             f'stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    b.append(txt(400, 358, "Ctrl-F your own file for train_test_split. If it appears twice, that is the bug.",
                 14, INK, "middle", central=True))
    svg("fig-cap-2-one-split-once.svg", "0 0 800 400",
        "One split. Made once. Used by everything.",
        "Two panels. The left, framed in red and headed what goes wrong, shows three models each doing their own split, fit and score, producing three different test sets so the results table compares nothing, with no error and no warning. The right, framed in green, shows one split made in a single cell near the top, then a baseline and three models all scored on the same X_test. A note underneath says: search your own file for train_test_split, and if it appears twice that is the bug.",
        b)


# ====================================== CAP.3 five charts in narrative order
def fig_cap_3():
    b = []
    b.append(txt(400, 40, "Five charts that read as one paragraph", 24, INK, "middle"))
    b.append(txt(400, 64, "Not five charts. A story with five pictures in it.", 14, MUTED, "middle"))

    charts = [
        ("1", "How big is the\nthing I predict?", "histogram", DATA_S, DATA_F),
        ("2", "What is actually\nin my data?", "bar of counts", DATA_S, DATA_F),
        ("3", "The relationship\nI expected", "scatter", MODEL_S, MODEL_F),
        ("4", "The question\nchart 3 raised", "groupby bar\n+ the counts", MODEL_S, MODEL_F),
        ("5", "The one that\nsurprised me", "two series\n+ a legend", ACC_S, ACC_F),
    ]
    x0, w, gap = 40, 138, 5
    for i, (n, q, kind, s, f) in enumerate(charts):
        bx = x0 + i * (w + gap)
        b.append(box(bx, 88, w, 176, f, s, 3, 12))
        b.append(f'<circle cx="{bx + w / 2}" cy="114" r="15" fill="{PAPER}" stroke="{s}" stroke-width="3"/>')
        b.append(txt(bx + w / 2, 114, n, 14, INK, "middle", central=True))
        for j, ln in enumerate(q.split("\n")):
            b.append(txt(bx + w / 2, 152 + j * 19, ln, 14, INK, "middle"))
        b.append(line(bx + 18, 198, bx + w - 18, 198, s, 1.5))
        for j, ln in enumerate(kind.split("\n")):
            b.append(txt(bx + w / 2, 220 + j * 17, ln, 12, MUTED, "middle"))
        if i < 4:
            b.append(arrow(bx + w + 0.5, 176, bx + w + gap - 0.5, 176, INK, 2))

    b.append(f'<rect x="40" y="284" width="720" height="62" rx="10" fill="{PANEL}" '
             f'stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    b.append(txt(400, 306, "THE TEST: read your five captions aloud, in order, with nothing in between.",
                 14, INK, "middle"))
    b.append(txt(400, 330, "If it sounds like a paragraph, you have a story. If it sounds like a list, reorder them.",
                 12, MUTED, "middle"))
    b.append(txt(400, 380, "Every title states a FINDING. Every axis label carries its UNITS. Bars start at zero.",
                 12, MUTED, "middle"))
    svg("fig-cap-3-five-charts-story.svg", "0 0 800 400",
        "Five charts that read as one paragraph",
        "Five numbered cards in order with an arrow between each. One, how big is the thing I predict, a histogram. Two, what is actually in my data, a bar of counts. Three, the relationship I expected, a scatter. Four, the question chart three raised, a groupby bar with the counts. Five, the one that surprised me, two series with a legend. A panel gives the test: read your five captions aloud in order, and if it sounds like a paragraph you have a story.",
        b)


# ===================================== CAP.4 the eight-minute clock
def fig_cap_4():
    b = []
    b.append(txt(400, 40, "Your eight minutes, to scale", 24, INK, "middle"))

    segs = [
        ("0:00", "1:00", "THE QUESTION", "and why you cared", HUMAN_S, HUMAN_F),
        ("1:00", "2:30", "THE DATA", "show the raw file", DATA_S, DATA_F),
        ("2:30", "4:00", "THE CLEANING LOG", "read TWO lines out", DATA_S, DATA_F),
        ("4:00", "5:30", "TWO CHARTS", "not five. Two", MODEL_S, MODEL_F),
        ("5:30", "6:30", "THE TABLE", "point at the baseline", MODEL_S, MODEL_F),
        ("6:30", "8:00", "WHAT I GOT WRONG", "the best 90 seconds", ACC_S, ACC_F),
    ]
    bar_x, bar_y, bar_w, bar_h = 40, 88, 720, 62
    total = 8.0
    def mins(t):
        m, s = t.split(":")
        return int(m) + int(s) / 60
    for i, (a, z, name, note, s, f) in enumerate(segs):
        x = bar_x + mins(a) / total * bar_w
        wpx = (mins(z) - mins(a)) / total * bar_w
        b.append(box(x, bar_y, wpx, bar_h, f, s, 3, 8))
        b.append(txt(x + wpx / 2, bar_y + 26, name.split()[0], 12, INK, "middle"))
        if len(name.split()) > 1:
            b.append(txt(x + wpx / 2, bar_y + 44, " ".join(name.split()[1:]), 12, INK, "middle"))
        b.append(txt(x + 2, bar_y - 10, a, 12, MUTED))
        # the note, alternating high/low to avoid collisions
        ny = 178 if i % 2 == 0 else 208
        b.append(line(x + wpx / 2, bar_y + bar_h, x + wpx / 2, ny - 12, GRID, 1.5))
        b.append(txt(x + wpx / 2, ny, note, 12, MUTED, "middle"))
    b.append(txt(bar_x + bar_w, bar_y - 10, "8:00", 12, MUTED, "end"))

    b.append(f'<rect x="40" y="238" width="352" height="112" rx="10" fill="{OK_F}" '
             f'stroke="{OK_S}" stroke-width="3" stroke-linejoin="round"/>')
    b.append(txt(216, 262, "DO", 14, INK, "middle", weight="600"))
    for i, ln in enumerate(["Point at the screen, not at the room",
                            "Say every number with its UNITS",
                            "Say \"I got this wrong\" out loud once",
                            "Have the file already open"]):
        b.append(txt(58, 286 + i * 20, ln, 12, INK))

    b.append(f'<rect x="408" y="238" width="352" height="112" rx="10" fill="{BAD_F}" '
             f'stroke="{BAD_S}" stroke-width="3" stroke-linejoin="round"/>')
    b.append(txt(584, 262, "DO NOT", 14, INK, "middle", weight="600"))
    for i, ln in enumerate(["Read your code out line by line",
                            "Live-code anything. Anything.",
                            "Say \"it's basically 90% accurate\"",
                            "Apologise for your score"]):
        b.append(txt(426, 286 + i * 20, ln, 12, INK))

    b.append(txt(400, 382, "Rehearse it out loud three times, to a real person, with a real timer.",
                 12, MUTED, "middle"))
    svg("fig-cap-4-eight-minute-clock.svg", "0 0 800 400",
        "Your eight minutes, to scale",
        "A timeline of eight minutes divided into six blocks: the question one minute, the data ninety seconds showing the raw file, the cleaning log ninety seconds reading two lines out, two charts ninety seconds, the results table one minute pointing at the baseline, and what I got wrong ninety seconds, labelled the best 90 seconds. A green DO list says point at the screen, say every number with its units, say I got this wrong out loud once, have the file already open. A red DO NOT list says do not read your code line by line, do not live-code anything, do not say it's basically 90 percent accurate, do not apologise for your score.",
        b)


# ==================================== CAP.5 the showcase run-sheet
def fig_cap_5():
    b = []
    b.append(txt(400, 38, "Showcase day: the teacher's run-sheet", 24, INK, "middle"))

    rows = [
        ("−1 day", "Every notebook Restart & Run All'd. Every chart PNG on disk.", HUMAN_S, HUMAN_F),
        ("−30 min", "Machines on, files OPEN, charts folder open. Nothing left to load.", HUMAN_S, HUMAN_F),
        ("0:00", "You speak for 2 min: the paper says what it says. Then sit down.", DATA_S, DATA_F),
        ("0:05", "Presentation 1 · 8 min + 3 min of questions from the bank", MODEL_S, MODEL_F),
        ("0:16", "Presentation 2 · same shape. Keep the timer visible.", MODEL_S, MODEL_F),
        ("0:27", "Presentation 3 · …", MODEL_S, MODEL_F),
        ("+5 min", "Everyone reads out ONE line from their 'what I got wrong'.", ACC_S, ACC_F),
        ("+10 min", "Level 3 gate self-check, then the letter to yourself.", OK_S, OK_F),
    ]
    for i, (when, what, s, f) in enumerate(rows):
        ry = 74 + i * 33
        b.append(box(32, ry, 84, 27, f, s, 2, 8))
        b.append(txt(74, ry + 14, when, 12, INK, "middle", central=True))
        b.append(box(124, ry, 644, 27, PAPER, GRID, 1.5, 8))
        b.append(txt(138, ry + 14, what, 12, INK, central=True))

    b.append(f'<rect x="32" y="346" width="736" height="34" rx="10" fill="{BAD_F}" '
             f'stroke="{BAD_S}" stroke-width="3" stroke-linejoin="round"/>')
    b.append(txt(400, 363, "DAY-OF TRIAGE: if the code will not run, they present the PRINTED charts and the log. The project still counts.",
                 12, INK, "middle", central=True))
    svg("fig-cap-5-showcase-runsheet.svg", "0 0 800 400",
        "Showcase day: the teacher's run-sheet",
        "A timed run-sheet. One day before, every notebook restarted and run, every chart saved as a PNG. Thirty minutes before, machines on and files already open. At zero, the teacher speaks for two minutes then sits down. Then presentations of eight minutes each plus three minutes of questions. Afterwards everyone reads out one line from their what-I-got-wrong section, then the Level 3 gate self-check and the letter to yourself. A red band gives the day-of triage: if the code will not run, they present the printed charts and the log, and the project still counts.",
        b)


# ================================= CAP.6 text columns to numbers, by hand
def fig_cap_6():
    b = []
    b.append(txt(400, 40, "Turning a text column into numbers, with no new syntax",
                 24, INK, "middle"))
    b.append(txt(400, 64, "A comparison gives True/False (week 22). astype(int) turns that into 1/0 (week 23).",
                 12, MUTED, "middle"))

    # left: the text column
    b.append(txt(112, 106, "what you collected", 14, MUTED, "middle"))
    modes = ["walk", "bus", "cycle", "car", "walk"]
    for i, m in enumerate(modes):
        b.append(box(56, 122 + i * 42, 112, 34, HUMAN_F, HUMAN_S, 2, 8))
        b.append(txt(112, 139 + i * 42, m, 14, INK, "middle", central=True))
    b.append(txt(112, 344, "one text column", 12, MUTED, "middle"))

    b.append(arrow(180, 226, 224, 226, INK, 3))

    # right: three 0/1 columns
    heads = ["is_walk", "is_bus", "is_cycle"]
    vals = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0], [1, 0, 0]]
    gx, cw = 244, 116
    b.append(txt(gx + 1.5 * cw, 106, "what the model can use", 14, MUTED, "middle"))
    for j, h in enumerate(heads):
        b.append(box(gx + j * cw, 118, cw - 6, 30, ACC_F, ACC_S, 2, 6))
        b.append(txt(gx + (cw - 6) / 2 + j * cw, 133, h, 12, INK, "middle",
                     weight="600", central=True))
    for i, row in enumerate(vals):
        for j, v in enumerate(row):
            f, s = (DATA_F, DATA_S) if v else (PAPER, GRID)
            b.append(box(gx + j * cw, 156 + i * 38, cw - 6, 30, f, s, 1.5, 6))
            b.append(txt(gx + (cw - 6) / 2 + j * cw, 171 + i * 38, str(v), 14, INK,
                         "middle", central=True))

    # the note about car
    b.append(box(608, 156, 160, 106, OK_F, OK_S, 3, 10))
    b.append(txt(688, 180, "no is_car column", 12, INK, "middle", weight="600"))
    for i, ln in enumerate(["Three zeros already", "means car. A fourth", "column would say", "nothing new."]):
        b.append(txt(688, 202 + i * 16, ln, 12, INK, "middle"))
    b.append(line(596, 196, 604, 196, MUTED, 1.5))
    b.append(txt(688, 288, "row 4 is the car row", 12, MUTED, "middle"))
    b.append(line(608, 268, 596, 268, MUTED, 1.5))

    b.append(txt(400, 366, "df[\"is_walk\"] = (df[\"mode\"] == \"walk\").astype(int)",
                 14, INK, "middle", font=MONO))
    b.append(txt(400, 388, "One line per category. No get_dummies, no pipeline, nothing you have not met.",
                 12, MUTED, "middle"))
    svg("fig-cap-6-text-to-numbers.svg", "0 0 800 400",
        "Turning a text column into numbers, with no new syntax",
        "On the left a single text column holding walk, bus, cycle, car and walk. An arrow points right to three columns headed is_walk, is_bus and is_cycle holding ones and zeros, so walk becomes 1 0 0, bus becomes 0 1 0, cycle becomes 0 0 1 and car becomes 0 0 0. A green note explains there is no is_car column because three zeros already means car. The line of code underneath reads: df bracket is_walk equals open paren df bracket mode equals equals walk close paren dot astype int.",
        b)


if __name__ == "__main__":
    print("writing capstone figures:")
    fig_cap_1(); fig_cap_2(); fig_cap_3(); fig_cap_4(); fig_cap_5(); fig_cap_6()
    print("done.")

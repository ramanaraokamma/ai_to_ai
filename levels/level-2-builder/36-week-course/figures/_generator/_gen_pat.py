"""The six Level 2 composition patterns, plus the hard-rule worked example."""
from _gen_core import *
import _gen_term  # noqa: F401  (registers every motif)

BY_ID = {m["id"]: m for m in MOTIFS}
PATTERNS = []


def place(mid, x, y, s=1):
    tr = "translate(%s,%s)" % (x, y) + ("" if s == 1 else " scale(%s)" % s)
    return '<g transform="%s">\n%s\n  </g>' % (tr, BY_ID[mid]["body"])


def P(pid, title, desc, vb, note, body):
    PATTERNS.append(dict(id=pid, title=title, desc=desc, vb=vb, note=note, body=body.strip("\n")))


# ============================================================ 1. pipeline
# NOTE: scale() scales type too, so a stage box that is too small for a motif's
# text gets a TEXT-FREE glyph instead; the words live in the 18px stage label.
GLYPH_SPLIT = """  <rect x="4" y="20" width="40" height="80" rx="6" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>
    <g stroke="%s" stroke-width="1.5">
      <line x1="4" y1="34" x2="44" y2="34"/><line x1="4" y1="48" x2="44" y2="48"/>
      <line x1="4" y1="62" x2="44" y2="62"/><line x1="4" y1="76" x2="44" y2="76"/>
    </g>
    <line x1="0" y1="84" x2="48" y2="84" stroke="%s" stroke-width="2" stroke-dasharray="5 4"/>
    %s
    %s
    <rect x="76" y="14" width="60" height="44" rx="8" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>
    <rect x="76" y="70" width="60" height="32" rx="8" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>""" % (
    PAPER, INK, GRID, ACC_S, arrow(48, 44, 72, 36, INK, 2.5), arrow(48, 90, 72, 86, INK, 2.5),
    DATA_F, DATA_S, ACC_F, ACC_S)

_gear = "\n    ".join(
    '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (
        60 + 15 * __import__("math").cos(__import__("math").radians(a)),
        70 + 15 * __import__("math").sin(__import__("math").radians(a)),
        60 + 21 * __import__("math").cos(__import__("math").radians(a)),
        70 + 21 * __import__("math").sin(__import__("math").radians(a)))
    for a in range(0, 360, 45))
GLYPH_MACHINE = """  <line x1="60" y1="2" x2="60" y2="10" stroke="%s" stroke-width="3" stroke-linecap="round"/>
    %s
    <path d="M28 16 L92 16 L78 42 L42 42 Z" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>
    <rect x="24" y="42" width="72" height="56" rx="10" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>
    <g stroke="%s" stroke-width="3" stroke-linecap="round">
    %s
    </g>
    <circle cx="60" cy="70" r="14" fill="%s" stroke="%s" stroke-width="3"/>
    <circle cx="60" cy="70" r="5" fill="%s" stroke="%s" stroke-width="2.5"/>
    <path d="M44 98 L76 98 L86 120 L34 120 Z" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>""" % (
    DATA_S, head(60, 14, 90, DATA_S), DATA_F, DATA_S, PANEL, INK, INK, _gear,
    PAPER, INK, MODEL_F, MODEL_S, OK_F, OK_S)

GLYPH_BARS = """  <g stroke="%s" stroke-width="1.5">
      <line x1="22" y1="30" x2="122" y2="30"/><line x1="22" y1="56" x2="122" y2="56"/><line x1="22" y1="82" x2="122" y2="82"/>
    </g>
    <g fill="%s">
      <rect x="28" y="34" width="18" height="62" rx="3"/><rect x="52" y="58" width="18" height="38" rx="3"/>
      <rect x="76" y="22" width="18" height="74" rx="3"/><rect x="100" y="66" width="18" height="30" rx="3"/>
    </g>
    <line x1="22" y1="16" x2="22" y2="96" stroke="%s" stroke-width="2"/>
    <line x1="22" y1="96" x2="126" y2="96" stroke="%s" stroke-width="2"/>""" % (GRID, DATA_S, INK, INK)

_boxes = ((30, DATA_S, "1. Load", "the CSV as a table"), (222, ACC_S, "2. Split", "train and test"),
          (414, MODEL_S, "3. Fit", "on train only"), (606, OK_S, "4. Score", "on test only"))
_pl = ["  " + t(400, 46, "Every model in this level is this one pipeline", 24, INK, "middle")]
for _x, _st, _a, _b in _boxes:
    _pl.append("  " + rect(_x, 96, 152, 190, 12, PAPER, _st, 3))
for _x in (183, 375, 567):
    _pl.append('  <g transform="translate(%s,182) scale(0.4)">\n%s\n  </g>' % (_x, BY_ID["motif-arrow"]["body"]))
_pl += ['  <g transform="translate(36,121) scale(1.4)">\n%s\n  </g>' % BY_ID["motif-table"]["body"],
        '  <g transform="translate(230,131)">\n%s\n  </g>' % GLYPH_SPLIT,
        '  <g transform="translate(430,130)">\n%s\n  </g>' % GLYPH_MACHINE,
        '  <g transform="translate(608,135)">\n%s\n  </g>' % GLYPH_BARS]
for (_x, _st, _a, _b), _c in zip(_boxes, (106, 298, 490, 682)):
    _pl.append("  " + t(_c, 312, _a, 18, INK, "middle"))
    _pl.append("  " + t(_c, 332, _b, 12, MUT, "middle"))
_pl.append("  " + t(400, 372, "Steps 1 and 2 are most of the work. Step 3 is three lines of code.", 14, MUT, "middle"))

P("pattern-pipeline", "Every model in this level is this one pipeline",
  "Four numbered stages left to right: load the CSV as a table, cut it into a large train pile and a small test pile, feed the train pile through a machine, and read a score off a bar chart.",
  "0 0 800 400",
  "Four equal boxes, arrows in the gaps, and a NUMBER on every stage so the order survives greyscale. Stage colours "
  "run data &rarr; accent &rarr; model &rarr; correct, which is also the story: data, held-out data, the learned thing, the verdict. "
  "The stage glyphs carry NO text &mdash; at this size a motif's own labels would fall under the 12px floor, so the words go in the stage label.",
  "\n".join(_pl))


# ============================================================ 2. before / after
def mini_table(x0, y0, rows, marked_col, mark_stroke, mark_fill):
    xs = (x0, x0 + 34, x0 + 124, x0 + 214)
    w = 304
    out = ['  <rect x="%s" y="%s" width="%s" height="126" fill="%s"/>' % (x0, y0, w, PAPER),
           '  <rect x="%s" y="%s" width="34" height="30" fill="%s"/>' % (x0, y0, PANEL)]
    for x in xs[1:]:
        out.append('  <rect x="%s" y="%s" width="90" height="30" fill="%s"/>' % (x, y0, DATA_F))
    for r in range(3):
        out.append('  <rect x="%s" y="%s" width="34" height="32" fill="%s"/>' % (x0, y0 + 30 + 32 * r, PANEL))
    mx = xs[marked_col]
    out.append('  <rect x="%s" y="%s" width="90" height="32" fill="%s"/>' % (mx, y0 + 62, mark_fill))
    out.append('  <g stroke="%s" stroke-width="1.5">' % GRID)
    for x in xs[1:]:
        out.append('    <line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (x, y0, x, y0 + 126))
    for r in (1, 2):
        out.append('    <line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (x0, y0 + 30 + 32 * r, x0 + w, y0 + 30 + 32 * r))
    out.append('  </g>')
    out.append('  <line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="2"/>' % (x0, y0 + 30, x0 + w, y0 + 30, INK))
    for x, lab in zip(xs[1:], ("player", "runs", "over")):
        out.append("  " + t(x + 45, y0 + 15, lab, 12, INK, "middle", central=True, weight="600"))
    for r, row in enumerate(rows):
        cy = y0 + 46 + 32 * r
        out.append("  " + t(x0 + 17, cy, str(r), 12, MUT, "middle", central=True))
        for x, v in zip(xs[1:], row):
            out.append("  " + t(x + 45, cy, v, 12, INK, "middle", central=True))
    out.append('  <rect x="%s" y="%s" width="90" height="32" fill="none" stroke="%s" stroke-width="3"/>' % (mx, y0 + 62, mark_stroke))
    out.append('  <rect x="%s" y="%s" width="%s" height="126" fill="none" stroke="%s" stroke-width="3"/>' % (x0, y0, w, INK))
    return "\n".join(out)


_ba = ["  " + t(400, 46, "Before and after we cleaned one cell", 24, INK, "middle"),
       '  <line x1="400" y1="80" x2="400" y2="336" stroke="%s" stroke-width="1.5" stroke-dasharray="6 6"/>' % GRID,
       "  " + rect(30, 80, 360, 240, 12, BAD_F, BAD_S, 3),
       "  " + rect(410, 80, 360, 240, 12, OK_F, OK_S, 3),
       '  <g transform="translate(48,94) scale(0.42)">\n%s\n  </g>' % BY_ID["motif-badge-cross"]["body"],
       '  <g transform="translate(428,94) scale(0.42)">\n%s\n  </g>' % BY_ID["motif-badge-check"]["body"],
       "  " + t(104, 128, "Before", 18, INK),
       "  " + t(484, 128, "After", 18, INK),
       mini_table(54, 150, (("Meera", "48", "12"), ("Kabir", "?", "9"), ("Nova", "57", "15")), 2, BAD_S, BAD_F),
       mini_table(434, 150, (("Meera", "48", "12"), ("Kabir", "31", "9"), ("Nova", "57", "15")), 2, OK_S, OK_F),
       "  " + t(206, 300, "one runs value is missing, so mean() fails", 12, MUT, "middle"),
       "  " + t(586, 300, "filled from the scorecard, and logged why", 12, MUT, "middle"),
       "  " + t(400, 360, "Same rows, same columns, one cell changed. Mirror the panels so only the content differs.", 14, MUT, "middle")]

P("pattern-before-after", "Before and after we cleaned one cell",
  "Two mirrored panels. The left panel is marked wrong and its table has a missing runs value shown as a question mark. The right panel is marked correct and the same cell holds 31.",
  "0 0 800 400",
  "Mirror the geometry EXACTLY so the eye only has to find the one difference. The tick/cross badge shape, "
  "not the panel colour, says which side is which. One change per figure &mdash; if you changed two things, draw two figures.",
  "\n".join(_ba))

# ============================================================ 3. three-panel progression
_pr = ["  " + t(400, 42, "Same eight points. Three models.", 24, INK, "middle")]
for _x, _st, _h, _sub, _mid in ((32, BAD_S, "1. Underfit", "train low, test low", "motif-fit-underfit"),
                                (283, OK_S, "2. Just right", "train good, test good", "motif-fit-good"),
                                (534, BAD_S, "3. Overfit", "train perfect, test poor", "motif-fit-overfit")):
    _c = _x + 117
    _pr.append("  " + t(_c, 68, _h, 18, INK, "middle"))
    _pr.append("  " + rect(_x, 76, 234, 240, 12, PAPER, _st, 3))
    _pr.append("  " + place(_mid, _x + 9, 86, 1.35))
    _pr.append("  " + t(_c, 336, _sub, 12, MUT, "middle"))
_pr.append("  " + t(400, 372, "The dots never move. Only the line does &#8212; that is the whole idea of model complexity.", 14, MUT, "middle"))

P("pattern-progression", "Same eight points, three models",
  "Three panels side by side over the same eight data points. Panel 1 fits a flat line and underfits. Panel 2 fits a smooth curve. Panel 3 fits a jagged line through every point and overfits.",
  "0 0 800 400",
  "Three equal panels, numbered, with IDENTICAL data in each. The numbers carry the progression; the panel "
  "colour only says good or bad. Underfit and overfit are both red, told apart by the SHAPE of the line.",
  "\n".join(_pr))

# ============================================================ 4. annotated chart
_ac = ["  " + t(250, 40, "Practice hours vs test score", 24, INK, "middle"),
       '  <g stroke="%s" stroke-width="1.5">' % GRID]
for _y in (308, 236, 164, 92):
    _ac.append('    <line x1="90" y1="%s" x2="450" y2="%s"/>' % (_y, _y))
_ac.append('  </g>')
for _y, _lab in ((380, "0"), (308, "25"), (236, "50"), (164, "75"), (92, "100")):
    _ac.append("  " + t(80, _y + 4, _lab, 12, MUT, "end"))
_ac.append('  <g stroke="%s" stroke-width="1.5">' % MUT)
for _x in (90, 162, 234, 306, 378, 450):
    _ac.append('    <line x1="%s" y1="380" x2="%s" y2="386"/>' % (_x, _x))
_ac.append('  </g>')
for _x, _lab in ((90, "0"), (162, "2"), (234, "4"), (306, "6"), (378, "8"), (450, "10")):
    _ac.append("  " + t(_x, 402, _lab, 12, MUT, "middle"))
for _x, _y in ((126, 340), (162, 318), (198, 300), (234, 262), (270, 250),
               (306, 206), (342, 200), (378, 160), (414, 128), (198, 356)):
    _ac.append('  <circle cx="%s" cy="%s" r="7" fill="%s" stroke="%s" stroke-width="2"/>' % (_x, _y, DATA_S, PAPER))
_ac += ['  <circle cx="198" cy="356" r="15" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="5 4"/>' % ACC_S,
        '  <line x1="282" y1="327" x2="212" y2="352" stroke="%s" stroke-width="2"/>' % ACC_S,
        "  " + head(210, 353, 160, ACC_S, 2),
        "  " + rect(282, 300, 168, 54, 10, PAPER, ACC_S, 2),
        "  " + t(366, 322, "This one practised 3 hours", 12, INK, "middle"),
        "  " + t(366, 342, "and scored 8. Ask why.", 12, INK, "middle"),
        '  <line x1="90" y1="80" x2="90" y2="380" stroke="%s" stroke-width="2"/>' % INK,
        '  <line x1="90" y1="380" x2="450" y2="380" stroke="%s" stroke-width="2"/>' % INK,
        "  " + t(270, 428, "Hours practised", 14, MUT, "middle"),
        "  " + t(48, 235, "Test score (out of 100)", 14, MUT, "middle", extra='transform="rotate(-90 48 235)"'),
        "  " + t(250, 468, "The ring marks the one point worth discussing.", 14, MUT, "middle")]

P("pattern-annotated-chart", "Practice hours vs test score, with one point called out",
  "A scatter plot of ten students. Nine points rise to the right. One point, at three hours and a score of eight, is ringed and labelled with a note asking why.",
  "0 0 500 500",
  "Axes with ticks and BOTH titles, grid lines under the marks, every axis numbered. Then exactly ONE annotation: "
  "a dashed accent ring, a leader with an arrowhead, and a label box that does not overlap a single data point. "
  "Route the leader through empty space &mdash; check every point before you commit the coordinates.",
  "\n".join(_ac))

# ============================================================ 5. data-structure diagram
_st = ["  " + t(400, 42, "One dictionary is one row", 24, INK, "middle"),
       "  " + rect(66, 122, 228, 150, 10, PAPER, GRID, 1.5),
       "  " + rect(51, 107, 228, 150, 10, PAPER, GRID, 1.5),
       "  " + rect(36, 92, 228, 150, 10, PAPER, INK, 3)]
for _y, _k, _v in ((108, "player", "Meera"), (150, "runs", "48"), (192, "over", "12")):
    _c = _y + 16
    _st.append("  " + rect(50, _y, 88, 32, 8, ACC_F, ACC_S, 2))
    _st.append("  " + t(94, _c, _k, 12, INK, "middle", central=True))
    _st.append("  " + arrow(144, _c, 166, _c, INK, 2))
    _st.append("  " + rect(170, _y, 80, 32, 8, DATA_F, DATA_S, 2))
    _st.append("  " + t(210, _c, _v, 12, INK, "middle", central=True))
_st += ["  " + t(150, 292, "one dict", 18, INK, "middle"),
        "  " + t(150, 314, "keys are the column names", 12, MUT, "middle"),
        '  <g transform="translate(300,150) scale(0.9)">\n%s\n  </g>' % BY_ID["motif-arrow"]["body"],
        "  " + t(342, 146, "same data", 12, MUT, "middle")]
_xs = (420, 460, 560, 660)
_st.append('  <rect x="420" y="100" width="40" height="34" fill="%s"/>' % PANEL)
for _x in _xs[1:]:
    _st.append('  <rect x="%s" y="100" width="100" height="34" fill="%s"/>' % (_x, DATA_F))
for _r in range(3):
    _st.append('  <rect x="420" y="%s" width="40" height="36" fill="%s"/>' % (134 + 36 * _r, PANEL))
_st.append('  <rect x="460" y="134" width="300" height="36" fill="%s"/>' % ACC_F)
_st.append('  <g stroke="%s" stroke-width="1.5">' % GRID)
for _x in _xs[1:]:
    _st.append('    <line x1="%s" y1="100" x2="%s" y2="242"/>' % (_x, _x))
for _r in (1, 2):
    _st.append('    <line x1="420" y1="%s" x2="760" y2="%s"/>' % (134 + 36 * _r, 134 + 36 * _r))
_st.append('  </g>')
_st.append('  <line x1="420" y1="134" x2="760" y2="134" stroke="%s" stroke-width="2"/>' % INK)
for _x, _lab in zip(_xs[1:], ("player", "runs", "over")):
    _st.append("  " + t(_x + 50, 117, _lab, 12, INK, "middle", central=True, weight="600"))
for _r, _row in enumerate((("Meera", "48", "12"), ("Kabir", "31", "9"), ("Nova", "57", "15"))):
    _cy = 152 + 36 * _r
    _st.append("  " + t(440, _cy, str(_r), 12, MUT, "middle", central=True))
    for _x, _v in zip(_xs[1:], _row):
        _st.append("  " + t(_x + 50, _cy, _v, 12, INK, "middle", central=True))
_st += ['  <rect x="420" y="134" width="340" height="36" fill="none" stroke="%s" stroke-width="3"/>' % ACC_S,
        '  <rect x="420" y="100" width="340" height="142" fill="none" stroke="%s" stroke-width="3"/>' % INK,
        "  " + t(590, 292, "one DataFrame", 18, INK, "middle"),
        "  " + t(590, 314, "each dict became row 0, 1, 2", 12, MUT, "middle"),
        "  " + t(400, 372, "A list of dicts and a DataFrame hold the same thing. pandas just adds the index.", 14, MUT, "middle")]

P("pattern-structure", "One dictionary is one row",
  "On the left, a card showing three key to value pairs, with two more cards stacked behind it. An arrow labelled same information points right to a DataFrame whose first row is highlighted and holds those same three values.",
  "0 0 800 400",
  "Show ONE record in full and the rest as offset cards behind it, then the whole structure on the right with the "
  "matching part highlighted. The highlight is what proves the mapping &mdash; without it this is two unrelated pictures.",
  "\n".join(_st))

# ============================================================ 6. error and fix
_ef = ["  " + t(400, 42, "Read the last line, change one thing, run again", 24, INK, "middle"),
       "  " + place("motif-traceback", 16, 80),
       '  <g transform="translate(424,172) scale(0.5)">\n%s\n  </g>' % BY_ID["motif-arrow"]["body"],
       "  " + rect(478, 96, 292, 176, 10, PAPER, OK_S, 3),
       '  <path d="M478 106 A10 10 0 0 1 488 96 H760 A10 10 0 0 1 770 106 V126 H478 Z" fill="%s"/>' % OK_F,
       '  <polyline points="492,112 498,118 510,104" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>' % OK_S,
       '  <line x1="478" y1="126" x2="770" y2="126" stroke="%s" stroke-width="2"/>' % INK,
       "  " + t(520, 116, "Terminal", 12, INK),
       "  " + t(494, 158, "&gt;", 14, MUT, mono=True),
       "  " + t(508, 158, "python pay.py", 14, INK, mono=True),
       "  " + t(494, 188, "total: 90", 14, INK, mono=True),
       "  " + t(494, 218, "&gt;", 14, MUT, mono=True),
       '  <rect x="508" y="206" width="9" height="14" fill="%s"/>' % INK,
       '  <rect x="478" y="96" width="292" height="176" rx="10" fill="none" stroke="%s" stroke-width="3"/>' % OK_S,
       "  " + t(216, 320, "Before: it stopped", 18, INK, "middle"),
       "  " + t(624, 320, "After: it ran", 18, INK, "middle"),
       "  " + t(216, 342, "quantity was never given a value", 12, MUT, "middle"),
       "  " + t(624, 342, "one line added, above line 4", 12, MUT, "middle"),
       "  " + t(400, 374, "Fix the reason the error names, not the line it happens on.", 14, MUT, "middle")]

P("pattern-error-fix", "Read the last line, change one thing, run again",
  "On the left, a red-outlined traceback panel with the failing line highlighted and arrowed. On the right, a green-outlined terminal showing the same program running and printing total: 90.",
  "0 0 800 400",
  "The failing artefact on the left, the working one on the right, an arrow between them, and a one-line diagnosis "
  "under each. The right panel must show the SAME program, so the reader can see that only one thing changed. "
  "Both panels sit at scale 1.0 &mdash; shrinking a terminal panel would drop its 12px mono text below the floor.",
  "\n".join(_ef))

# ============================================================ hard-rule example
BAD_EXAMPLE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 300" role="img">
  <title>Wrong: a figure that is only a picture of code</title>
  <desc>A grey panel containing five lines of Python about looping over a list of fruits, with no diagram, no arrows and no annotation.</desc>
  %s
  <g transform="translate(28,24) scale(0.3)">
%s
  </g>
  %s
  <rect x="20" y="80" width="460" height="170" rx="10" fill="%s" stroke="%s" stroke-width="1.5"/>
  %s
  %s
  %s
  %s
  %s
""" % (rect(20, 20, 460, 40, 10, BAD_F, BAD_S, 3),
       BY_ID["motif-badge-cross"]["body"],
       t(74, 46, "Do not do this &#8212; it is a picture of code", 14, INK),
       PANEL, GRID,
       t(40, 114, 'fruits = ["apple", "fig", "plum"]', 14, INK, mono=True),
       t(40, 144, "for i in range(3):", 14, INK, mono=True),
       t(40, 174, "    print(i, fruits[i])", 14, INK, mono=True),
       t(40, 214, "# 0 apple / 1 fig / 2 plum", 14, MUT, mono=True),
       t(250, 276, "The reader learns nothing the code block did not already say.", 12, MUT, "middle")) + "</svg>"

_good = ["  " + rect(20, 20, 460, 40, 10, OK_F, OK_S, 3),
         '  <g transform="translate(28,24) scale(0.3)">\n%s\n  </g>' % BY_ID["motif-badge-check"]["body"],
         "  " + t(74, 46, "Do this instead &#8212; it diagrams the mental model", 14, INK),
         "  " + rect(20, 76, 460, 180, 12, PANEL, GRID, 1.5),
         '  <path d="M136 73 A52 52 0 1 1 84 73" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % INK,
         "  " + head(84, 73, -30),
         '  <circle cx="110" cy="118" r="34" fill="%s" stroke="%s" stroke-width="3"/>' % (PAPER, INK),
         "  " + t(110, 106, "i", 12, MUT, "middle", central=True),
         "  " + t(110, 126, "1", 24, INK, "middle", central=True),
         "  " + t(110, 188, "pass 2 of 3", 12, MUT, "middle")]
for _i, (_x, _v) in enumerate(((206, "apple"), (296, "fig"), (386, "plum"))):
    _on = _i == 1
    _good.append("  " + rect(_x, 92, 82, 52, 6, ACC_F if _on else PAPER, ACC_S if _on else GRID, 3 if _on else 1.5))
    _good.append("  " + t(_x + 41, 118, _v, 12, INK, "middle", central=True))
    _good.append("  " + t(_x + 41, 88, str(_i), 12, MUT, "middle"))
_good += ['  <path d="M331 158 L343 158 L337 150 Z" fill="%s" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (ACC_F, ACC_S),
          '  <line x1="337" y1="174" x2="337" y2="160" stroke="%s" stroke-width="1.5"/>' % ACC_S,
          "  " + t(337, 190, "i names this slot", 12, MUT, "middle"),
          "  " + t(250, 228, "The counter names one slot per pass. After the last slot it stops.", 12, MUT, "middle"),
          "  " + t(250, 276, "Same lesson, no code on screen &#8212; and the off-by-one shows.", 12, MUT, "middle")]

GOOD_EXAMPLE = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 300" role="img">\n'
                '  <title>Right: a figure that diagrams the mental model</title>\n'
                '  <desc>A circular arrow with a counter reading i equals 1 sits beside three slots holding apple, '
                'fig and plum, numbered 0 to 2. The middle slot is highlighted and labelled i names this slot.</desc>\n'
                + "\n".join(_good) + "\n</svg>")

EXAMPLES = [("example-bad-code-screenshot", "Wrong: a figure that is only a picture of code", BAD_EXAMPLE),
            ("example-good-mental-model", "Right: a figure that diagrams the mental model", GOOD_EXAMPLE)]

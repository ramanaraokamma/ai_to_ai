"""Core palette, helpers and the CODE motifs for Level 2 figures."""

FS = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
FM = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

DATA_S, DATA_F = "#1F6FB2", "#D9EAF9"
MODEL_S, MODEL_F = "#6D28D9", "#DBCEF3"
HUMAN_S, HUMAN_F = "#845F00", "#E8C671"
OK_S, OK_F = "#1B7A4B", "#E2F7ED"
BAD_S, BAD_F = "#CC2B1D", "#F6AEA6"
ACC_S, ACC_F = "#C42B8C", "#F4D5E9"
INK, PAPER, MUT, GRID, PANEL = "#14202B", "#FFFFFF", "#55636F", "#C7CDD4", "#F5F8FA"


def t(x, y, s, size=14, fill=MUT, anchor=None, mono=False, central=False,
      weight=None, extra=""):
    ff = FM if mono else FS
    a = ' text-anchor="%s"' % anchor if anchor else ""
    c = ' dominant-baseline="central"' if central else ""
    w = ' font-weight="%s"' % weight if weight else ""
    e = (" " + extra) if extra else ""
    return ('<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s"%s%s%s%s>%s</text>'
            % (x, y, ff, size, fill, a, c, w, e, s))


def head(x, y, angle=0, color=INK, w=3):
    return ('<polyline points="-13,-8 0,0 -13,8" fill="none" stroke="%s" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" transform="translate(%s %s) rotate(%s)"/>'
            % (color, w, x, y, angle))


def arrow(x1, y1, x2, y2, color=INK, w=3):
    import math
    ang = round(math.degrees(math.atan2(y2 - y1, x2 - x1)), 1)
    ang = int(ang) if ang == int(ang) else ang
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>\n  %s'
            % (x1, y1, x2, y2, color, w, head(x2, y2, ang, color, w)))


def rect(x, y, w, h, rx, fill, stroke, sw=3):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" '
            'stroke-width="%s" stroke-linejoin="round"/>' % (x, y, w, h, rx, fill, stroke, sw))


MOTIFS = []


def M(mid, title, desc, vb, body, note):
    MOTIFS.append(dict(id=mid, title=title, desc=desc, vb=vb,
                       body=body.strip("\n"), note=note))


# ------------------------------------------------------------------ variable
M("motif-variable", "A variable as a labelled box",
  "A luggage-label tag reading score is attached to a box holding the value 7.",
  "0 0 170 100", """
  %s
  %s
  %s
  %s
""" % (rect(20, 12, 78, 26, 8, PAPER, INK, 2),
       t(59, 25, "score", 14, INK, "middle", central=True),
       rect(20, 38, 124, 48, 10, DATA_F, DATA_S, 3),
       t(82, 62, "7", 24, INK, "middle", central=True)),
  "The name is a label stuck ON the box, not the box itself. Value 24px, name 14px.")

# ------------------------------------------------------------------ rebinding
M("motif-rebind", "Rebinding a variable",
  "Two panels. Before: the box labelled score holds 7. After: the same box holds 10 and the old 7 is struck through.",
  "0 0 350 136", """
  %s
  %s
  %s
  %s
  %s
  %s
  %s
  %s
  %s
  <line x1="294" y1="58" x2="316" y2="58" stroke="%s" stroke-width="3" stroke-linecap="round"/>
  %s
  %s
  %s
""" % (rect(10, 8, 78, 26, 8, PAPER, INK, 2),
       t(49, 21, "score", 14, INK, "middle", central=True),
       rect(10, 34, 124, 48, 10, DATA_F, DATA_S, 3),
       t(72, 58, "7", 24, INK, "middle", central=True),
       arrow(146, 58, 190, 58),
       rect(206, 8, 78, 26, 8, PAPER, INK, 2),
       t(245, 21, "score", 14, INK, "middle", central=True),
       rect(206, 34, 124, 48, 10, DATA_F, DATA_S, 3),
       t(244, 58, "10", 24, INK, "middle", central=True),
       BAD_S,
       t(305, 58, "7", 18, MUT, "middle", central=True),
       t(72, 104, "before", 12, MUT, "middle"),
       t(268, 104, "after", 12, MUT, "middle")),
  "Use for = as rebinding, never as equality. The struck-through old value is the whole point.")

# ------------------------------------------------------------------ list
M("motif-list", "A list as numbered slots",
  "Five slots side by side holding 3, 8, 1, 9 and 4, numbered 0 to 4 underneath, with a bracket above labelled len = 5.",
  "0 0 320 126", """
  <path d="M22 38 V30 H298 V38" fill="none" stroke="%s" stroke-width="1.5" stroke-linejoin="round"/>
  %s
%s
%s
%s
""" % (MUT,
       t(160, 22, "len = 5", 12, MUT, "middle"),
       "\n".join("  " + rect(x, 46, 52, 52, 6, PAPER, DATA_S, 2)
                 for x in (22, 78, 134, 190, 246)),
       "\n".join("  " + t(x + 26, 72, v, 18, INK, "middle", central=True)
                 for x, v in zip((22, 78, 134, 190, 246), "38194")),
       "\n".join("  " + t(x + 26, 116, str(i), 12, MUT, "middle")
                 for i, x in enumerate((22, 78, 134, 190, 246)))),
  "Index labels 0..n-1 are compulsory. The bracket makes len a length, not a last index.")

# ------------------------------------------------------------------ dict
_dict_rows = []
for _y, _k, _v in ((30, "player", "Meera"), (78, "runs", "48"), (126, "ground", "Pune")):
    _c = _y + 20
    _dict_rows.append("  " + rect(14, _y, 92, 40, 8, ACC_F, ACC_S, 3))
    _dict_rows.append("  " + t(60, _c, _k, 12, INK, "middle", central=True))
    _dict_rows.append("  " + arrow(112, _c, 140, _c, INK, 2.5))
    _dict_rows.append("  " + rect(146, _y, 100, 40, 8, DATA_F, DATA_S, 3))
    _dict_rows.append("  " + t(196, _c, _v, 12, INK, "middle", central=True))

M("motif-dict", "A dictionary as key to value pairs",
  "Three rows. Each has a key box on the left, an arrow, and a value box on the right: player to Meera, runs to 48, ground to Pune.",
  "0 0 260 176", """
  %s
  %s
%s
""" % (t(60, 20, "key", 12, MUT, "middle"),
       t(196, 20, "value", 12, MUT, "middle"),
       "\n".join(_dict_rows)),
  "Keys are accent (a name you chose), values are data. The arrow is one-way: keys look up values, never the reverse.")

# ------------------------------------------------------------------ for loop
_loop = ["""  <path d="M114 46 A48 48 0 1 1 66 46" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>
  %s
  <circle cx="90" cy="88" r="26" fill="%s" stroke="%s" stroke-width="3"/>
  %s
  %s
  <path d="M102 140 L114 140 L108 148 Z" fill="%s" stroke="%s" stroke-width="2" stroke-linejoin="round"/>""" % (
    INK, head(66, 46, -30), PANEL, INK,
    t(90, 78, "i", 12, MUT, "middle", central=True),
    t(90, 96, "2", 24, INK, "middle", central=True), ACC_F, ACC_S)]
for _i, _x in enumerate((20, 56, 92, 128)):
    _on = _i == 2
    _loop.append("  " + rect(_x, 150, 32, 26, 5, ACC_F if _on else PAPER,
                             ACC_S if _on else GRID, 3 if _on else 1.5))
    _loop.append("  " + t(_x + 16, 163, str(_i), 12, INK if _on else MUT, "middle", central=True))

M("motif-loop", "A for loop as one trip round a circle",
  "A near-complete circular arrow with a counter reading i equals 2 in the middle, above a row of four numbered slots with slot 2 highlighted.",
  "0 0 180 185", "\n".join(_loop),
  "The counter and the highlighted slot must always agree. Highlight by fill AND a caret, never fill alone.")

# ------------------------------------------------------------------ if / else
M("motif-if-else", "An if/else as a fork in the path",
  "A signpost reading hot outside? stands over a path that forks. The left branch is labelled yes and leads to fan on; the right is labelled no and leads to fan off.",
  "0 0 240 172", """
  <path d="M120 80 L53 120" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>
  <path d="M120 80 L187 120" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>
  <line x1="120" y1="52" x2="120" y2="80" stroke="%s" stroke-width="3" stroke-linecap="round"/>
  %s
  %s
  %s
  %s
  %s
  %s
  %s
  %s
  %s
  %s
""" % (INK, INK, INK,
       rect(44, 16, 152, 36, 8, PANEL, INK, 3),
       t(120, 34, "hot outside?", 12, INK, "middle", central=True),
       rect(70, 90, 34, 20, 10, PAPER, ACC_S, 2),
       t(87, 100, "yes", 12, INK, "middle", central=True),
       rect(137, 90, 34, 20, 10, PAPER, ACC_S, 2),
       t(154, 100, "no", 12, INK, "middle", central=True),
       rect(8, 120, 90, 40, 8, DATA_F, DATA_S, 3),
       t(53, 140, "fan on", 12, INK, "middle", central=True),
       rect(142, 120, 90, 40, 8, DATA_F, DATA_S, 3),
       t(187, 140, "fan off", 12, INK, "middle", central=True)),
  "The condition goes on the signpost, the answer goes on the branch. Both branches are drawn even when else is empty.")

# ------------------------------------------------------------------ function
M("motif-function", "A function as a machine with a hopper and a chute",
  "A funnel-shaped input hopper feeds a box named average, which empties through a chute at the bottom.",
  "0 0 200 172", """
  <line x1="100" y1="4" x2="100" y2="12" stroke="%s" stroke-width="3" stroke-linecap="round"/>
  %s
  <path d="M62 18 L138 18 L118 48 L82 48 Z" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>
  %s
  %s
  <path d="M80 120 L120 120 L132 146 L68 146 Z" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>
  <line x1="100" y1="148" x2="100" y2="156" stroke="%s" stroke-width="3" stroke-linecap="round"/>
  %s
  %s
  %s
""" % (DATA_S, head(100, 16, 90, DATA_S), DATA_F, DATA_S,
       rect(44, 48, 112, 72, 12, PANEL, INK, 3),
       t(100, 84, "average", 18, INK, "middle", central=True),
       OK_F, OK_S, OK_S, head(100, 160, 90, OK_S),
       t(146, 36, "inputs", 12, MUT),
       t(140, 138, "returns", 12, MUT)),
  "Arguments fall in the top, the return value drops out the bottom. The name lives on the body.")

# ------------------------------------------------------------------ call stack
_stack = ['  <line x1="16" y1="142" x2="164" y2="142" stroke="%s" stroke-width="1.5"/>' % GRID,
          '  <path d="M100 18 L112 18 L106 28 Z" fill="%s" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (ACC_F, ACC_S)]
for _y, _name, _n, _cur in ((32, "average", "3", True), (68, "total", "2", False), (104, "main", "1", False)):
    _stack.append("  " + rect(22, _y, 136, 32, 6, ACC_F if _cur else PAPER,
                              ACC_S if _cur else INK, 3 if _cur else 2))
    _stack.append("  " + t(90, _y + 16, _name, 14, INK, "middle", central=True))
    _stack.append("  " + t(166, _y + 20, _n, 12, MUT))

M("motif-callstack", "A call stack as stacked trays",
  "Three trays stacked on the ground. main is at the bottom, then total, then average on top, marked as the one running now.",
  "0 0 185 155", "\n".join(_stack),
  "The tray on top is the one running. Number the trays so the calling order survives greyscale.")

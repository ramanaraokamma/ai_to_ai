"""Terminal / error motifs, plus the motifs inherited verbatim from Level 1."""
from _gen_core import *
import _gen_data  # noqa: F401  (registers the data motifs first)

# ------------------------------------------------------------------ terminal
M("motif-terminal", "A terminal window frame",
  "A console window with a title bar reading Terminal. Inside, a prompt runs python hello.py, the output line reads hello, world, and a fresh prompt waits with a block cursor.",
  "0 0 300 176", """
  <path d="M14 26 A10 10 0 0 1 24 16 H276 A10 10 0 0 1 286 26 V46 H14 Z" fill="%s"/>
  <g fill="none" stroke="%s" stroke-width="2">
    <circle cx="32" cy="31" r="4"/>
    <circle cx="48" cy="31" r="4"/>
    <circle cx="64" cy="31" r="4"/>
  </g>
  %s
  <line x1="14" y1="46" x2="286" y2="46" stroke="%s" stroke-width="2"/>
  %s
  %s
  %s
  %s
  <rect x="44" y="118" width="9" height="14" fill="%s"/>
  <rect x="14" y="16" width="272" height="148" rx="10" fill="none" stroke="%s" stroke-width="3"/>
""" % (PANEL, MUT,
       t(84, 35, "Terminal", 12, MUT),
       INK,
       t(30, 72, "&gt;", 14, MUT, mono=True),
       t(44, 72, "python hello.py", 14, INK, mono=True),
       t(30, 100, "hello, world", 14, INK, mono=True),
       t(30, 130, "&gt;", 14, MUT, mono=True),
       INK, INK),
  "The window frame is ink; the title bar is panel grey. Output text is the MONO stack at 14px. Draw the frame LAST so it caps the fill.")

# ------------------------------------------------------------------ traceback
M("motif-traceback", "A traceback, with the offending line marked",
  "A console panel outlined in red shows a four-line Python traceback. The line that failed is highlighted and an arrow points at it from the right. The last line, a NameError, is printed in red.",
  "0 0 400 205", """
  <path d="M14 26 A10 10 0 0 1 24 16 H296 A10 10 0 0 1 306 26 V46 H14 Z" fill="%s"/>
  <g stroke="%s" stroke-width="2.5" stroke-linecap="round">
    <line x1="26" y1="26" x2="36" y2="36"/>
    <line x1="36" y1="26" x2="26" y2="36"/>
  </g>
  %s
  <line x1="14" y1="46" x2="306" y2="46" stroke="%s" stroke-width="2"/>
  <rect x="22" y="98" width="272" height="22" rx="4" fill="%s"/>
  %s
  %s
  %s
  %s
  %s
  <rect x="14" y="16" width="292" height="160" rx="10" fill="none" stroke="%s" stroke-width="3"/>
  %s
  %s
  %s
""" % (BAD_F, BAD_S,
       t(46, 35, "Traceback", 12, INK),
       INK, BAD_F,
       t(26, 68, "Traceback (most recent call last):", 12, MUT, mono=True),
       t(26, 90, '  File "pay.py", line 4, in &lt;module&gt;', 12, MUT, mono=True),
       t(26, 112, "    total = price * quantity", 12, INK, mono=True),
       t(26, 140, "NameError: name 'quantity'", 12, BAD_S, mono=True, weight="600"),
       t(26, 158, "is not defined", 12, BAD_S, mono=True, weight="600"),
       BAD_S,
       arrow(390, 109, 314, 109, BAD_S),
       t(312, 92, "this line", 12, INK),
       t(160, 196, "Read the last line first.", 12, MUT, "middle")),
  "THE SANCTIONED EXCEPTION (see the hard rule): an error message is an artefact the learner must read, so we show it verbatim. The figure's work is the highlight and the arrow, not the text.")

# ------------------------------------------------------------------ code callout
M("motif-code-callout", "One line of code with a callout on one token",
  "A single line of code sits on a grey strip. The word price is boxed in pink and an arrow points up at it from a label reading a name, not a value.",
  "0 0 340 112", """
  <rect x="14" y="24" width="312" height="34" rx="8" fill="%s" stroke="%s" stroke-width="1.5"/>
  <rect x="95" y="30" width="52" height="24" rx="4" fill="%s" stroke="%s" stroke-width="2"/>
  %s
  %s
  %s
  <line x1="121" y1="60" x2="121" y2="78" stroke="%s" stroke-width="2"/>
  %s
  %s
  %s
""" % (PANEL, GRID, ACC_F, ACC_S,
       t(28, 46, "total =", 14, INK, mono=True),
       t(100, 46, "price", 14, INK, mono=True),
       t(152, 46, "* count", 14, INK, mono=True),
       ACC_S,
       head(121, 58, -90, ACC_S, 2),
       rect(53, 78, 136, 24, 12, PAPER, ACC_S, 2),
       t(121, 90, "a name, not a value", 12, INK, "middle", central=True)),
  "ONE token, ONE arrow, ONE claim. Split the line into separate <text> runs at fixed x so the highlight box lands exactly on the token instead of trusting the font's advance width.")

# ================================================================== inherited
INHERITED = set()


def I(mid, title, desc, vb, body, note):
    INHERITED.add(mid)
    M(mid, title, desc, vb, body, note)


I("motif-arrow", "Arrow pointing right", "A straight arrow pointing to the right.",
  "0 0 100 40", """
  <line x1="6" y1="20" x2="84" y2="20" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="76,10 92,20 76,30" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
""", "Inherited verbatim from Level 1. Every pipeline gap.")

I("motif-arrow-curved", "Curved arrow", "A curved arrow that loops up and over to the right.",
  "0 0 100 60", """
  <path d="M8 48 Q48 2 84 34" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(84 34) rotate(41)"/>
""", "Inherited verbatim from Level 1. Going back round a loop, or returning a value.")

I("motif-badge-check", "Correct badge", "A round badge with a tick inside, meaning correct.",
  "0 0 100 100", """
  <circle cx="50" cy="50" r="34" fill="#E2F7ED" stroke="#1B7A4B" stroke-width="3"/>
  <polyline points="34,52 45,64 68,38" fill="none" stroke="#1B7A4B" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
""", "Inherited verbatim from Level 1. It ran / it passed / after the fix.")

I("motif-badge-cross", "Wrong badge", "A round badge with a cross inside, meaning wrong.",
  "0 0 100 100", """
  <circle cx="50" cy="50" r="34" fill="#F6AEA6" stroke="#CC2B1D" stroke-width="3"/>
  <g stroke="#CC2B1D" stroke-width="6" stroke-linecap="round">
    <line x1="38" y1="38" x2="62" y2="62"/>
    <line x1="62" y1="38" x2="38" y2="62"/>
  </g>
""", "Inherited verbatim from Level 1. It crashed / it failed / before the fix.")

I("motif-box", "Labelled box", "A rounded box with a label inside.",
  "0 0 120 80", """
  <rect x="6" y="10" width="108" height="60" rx="10" fill="#F5F8FA" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
  <text x="60" y="40" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">Label</text>
""", "Inherited verbatim from Level 1. A neutral stage in a pipeline.")

I("motif-note", "Sticky note", "A sticky note with a folded corner and three lines of writing.",
  "0 0 100 100", """
  <path d="M12 12 H88 V68 L68 88 H12 Z" fill="#E8C671" stroke="#845F00" stroke-width="3" stroke-linejoin="round"/>
  <path d="M68 88 V68 H88 Z" fill="#FFFFFF" stroke="#845F00" stroke-width="3" stroke-linejoin="round"/>
  <g stroke="#55636F" stroke-width="3" stroke-linecap="round">
    <line x1="24" y1="30" x2="76" y2="30"/>
    <line x1="24" y1="43" x2="76" y2="43"/>
    <line x1="24" y1="56" x2="60" y2="56"/>
  </g>
""", "Inherited verbatim from Level 1. A human decision: a cleaning-log entry, a comment, a choice you made.")

I("motif-table", "Data table", "A small data table with a shaded header row and six cells.",
  "0 0 100 100", """
  <rect x="8" y="16" width="84" height="68" rx="8" fill="#FFFFFF" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <path d="M8 24 A8 8 0 0 1 16 16 H84 A8 8 0 0 1 92 24 V38 H8 Z" fill="#D9EAF9" stroke="none"/>
  <g stroke="#C7CDD4" stroke-width="1.5">
    <line x1="8" y1="61" x2="92" y2="61"/>
    <line x1="36" y1="38" x2="36" y2="84"/>
    <line x1="64" y1="38" x2="64" y2="84"/>
  </g>
  <line x1="8" y1="38" x2="92" y2="38" stroke="#1F6FB2" stroke-width="3"/>
  <rect x="8" y="16" width="84" height="68" rx="8" fill="none" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <g fill="#55636F">
    <rect x="15" y="24" width="14" height="5" rx="2.5"/>
    <rect x="43" y="24" width="14" height="5" rx="2.5"/>
    <rect x="71" y="24" width="14" height="5" rx="2.5"/>
    <rect x="15" y="47" width="14" height="5" rx="2.5"/>
    <rect x="43" y="47" width="14" height="5" rx="2.5"/>
    <rect x="71" y="47" width="14" height="5" rx="2.5"/>
    <rect x="15" y="70" width="14" height="5" rx="2.5"/>
    <rect x="43" y="70" width="14" height="5" rx="2.5"/>
    <rect x="71" y="70" width="14" height="5" rx="2.5"/>
  </g>
""", "Inherited verbatim from Level 1. A table as an ICON, at small size. For a table with real content, use motif-dataframe.")

I("motif-child", "Child's face", "A smiling child's face with short hair.",
  "0 0 100 100", """
  <circle cx="50" cy="52" r="30" fill="#E8C671" stroke="#845F00" stroke-width="3"/>
  <path d="M20 44 A30 30 0 0 1 80 44 A34 22 0 0 0 20 44 Z" fill="#845F00" stroke="#845F00" stroke-width="3" stroke-linejoin="round"/>
  <circle cx="40" cy="50" r="4" fill="#14202B"/>
  <circle cx="60" cy="50" r="4" fill="#14202B"/>
  <path d="M39 63 Q50 72 61 63" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
""", "Inherited verbatim from Level 1. The programmer. Use when the point is that a PERSON chose something.")

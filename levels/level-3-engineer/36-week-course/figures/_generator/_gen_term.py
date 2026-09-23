"""Terminal and traceback motifs, plus the motifs inherited VERBATIM from Level 2.

The bodies in the INHERITED block are byte-for-byte copies of Level 2's sprite sheet.
Do not touch them: a parent flipping between the two years must not be able to tell
where one year ends and the next begins.
"""
from _gen_core import *
import _gen_vision  # noqa: F401  (registers the vision / unsupervised / text motifs first)

# ================================================================== NEW: shape traceback
M("motif-traceback-shape", "A shape error, with the offending line marked",
  "A console panel outlined in red shows a five-line Python traceback. The line that failed, Z1 equals "
  "X at W1, is highlighted and an arrow points at it from the right. The last two lines, printed in red, "
  "are a ValueError naming the two shapes 750 by 2 and 16 by 2 as not aligned.",
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
       t(26, 90, '  File "net.py", line 12, in forward', 12, MUT, mono=True),
       t(26, 112, "    Z1 = X @ W1", 12, INK, mono=True),
       t(26, 140, "ValueError: matmul: shapes", 12, BAD_S, mono=True, weight="600"),
       t(26, 158, "(750,2) and (16,2) not aligned", 12, BAD_S, mono=True, weight="600"),
       BAD_S,
       arrow(390, 109, 314, 109, BAD_S, 3),
       t(312, 92, "this line", 12, INK),
       t(160, 196, "Two shapes are printed. Compare them.", 12, MUT, "middle")),
  "THE SANCTIONED EXCEPTION: an error message is an artefact the learner must read, so it is shown "
  "verbatim. The figure's work is the highlight and the arrow. Level 3's commonest traceback is a shape "
  "error, so the last line names TWO shapes &mdash; teach the reader to compare them.")

# ================================================================== INHERITED from Level 2
INHERITED = ["motif-terminal", "motif-traceback", "motif-arrow", "motif-arrow-curved",
             "motif-badge-check", "motif-badge-cross", "motif-box", "motif-note",
             "motif-table", "motif-dataframe", "motif-array-2d", "motif-split"]

M("motif-terminal", "A terminal window frame",
  "A console window with a title bar reading Terminal. Inside, a prompt runs python hello.py, the "
  "output line reads hello, world, and a fresh prompt waits with a block cursor.",
  "0 0 300 176", """
  <path d="M14 26 A10 10 0 0 1 24 16 H276 A10 10 0 0 1 286 26 V46 H14 Z" fill="#F5F8FA"/>
  <g fill="none" stroke="#55636F" stroke-width="2">
    <circle cx="32" cy="31" r="4"/>
    <circle cx="48" cy="31" r="4"/>
    <circle cx="64" cy="31" r="4"/>
  </g>
  <text x="84" y="35" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F">Terminal</text>
  <line x1="14" y1="46" x2="286" y2="46" stroke="#14202B" stroke-width="2"/>
  <text x="30" y="72" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#55636F">&gt;</text>
  <text x="44" y="72" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#14202B">python hello.py</text>
  <text x="30" y="100" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#14202B">hello, world</text>
  <text x="30" y="130" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="#55636F">&gt;</text>
  <rect x="44" y="118" width="9" height="14" fill="#14202B"/>
  <rect x="14" y="16" width="272" height="148" rx="10" fill="none" stroke="#14202B" stroke-width="3"/>
""",
  "Inherited verbatim from Level 2. The window frame is ink; the title bar is panel grey. Output text is "
  "the MONO stack at 14px. Draw the frame LAST so it caps the fill.")

M("motif-traceback", "A traceback, with the offending line marked",
  "A console panel outlined in red shows a four-line Python traceback. The line that failed is "
  "highlighted and an arrow points at it from the right. The last line, a NameError, is printed in red.",
  "0 0 400 205", """
  <path d="M14 26 A10 10 0 0 1 24 16 H296 A10 10 0 0 1 306 26 V46 H14 Z" fill="#F6AEA6"/>
  <g stroke="#CC2B1D" stroke-width="2.5" stroke-linecap="round">
    <line x1="26" y1="26" x2="36" y2="36"/>
    <line x1="36" y1="26" x2="26" y2="36"/>
  </g>
  <text x="46" y="35" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B">Traceback</text>
  <line x1="14" y1="46" x2="306" y2="46" stroke="#14202B" stroke-width="2"/>
  <rect x="22" y="98" width="272" height="22" rx="4" fill="#F6AEA6"/>
  <text x="26" y="68" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12" fill="#55636F">Traceback (most recent call last):</text>
  <text x="26" y="90" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12" fill="#55636F">  File "pay.py", line 4, in &lt;module&gt;</text>
  <text x="26" y="112" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12" fill="#14202B">    total = price * quantity</text>
  <text x="26" y="140" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12" fill="#CC2B1D" font-weight="600">NameError: name 'quantity'</text>
  <text x="26" y="158" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12" fill="#CC2B1D" font-weight="600">is not defined</text>
  <rect x="14" y="16" width="292" height="160" rx="10" fill="none" stroke="#CC2B1D" stroke-width="3"/>
  <line x1="390" y1="109" x2="314" y2="109" stroke="#CC2B1D" stroke-width="3" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#CC2B1D" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(314 109) rotate(180)"/>
  <text x="312" y="92" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B">this line</text>
  <text x="160" y="196" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">Read the last line first.</text>
""",
  "Inherited verbatim from Level 2. Use it for the errors Level 2 taught (NameError, KeyError). For "
  "Level 3's own commonest failure use motif-traceback-shape.")

M("motif-arrow", "Arrow pointing right",
  "A straight arrow pointing to the right.", "0 0 100 40", """
  <line x1="6" y1="20" x2="84" y2="20" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="76,10 92,20 76,30" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
""",
  "Inherited verbatim from Level 1 and 2. Every pipeline gap. Text-free, so it may be scaled freely.")

M("motif-arrow-curved", "Curved arrow",
  "A curved arrow that loops up and over to the right.", "0 0 100 60", """
  <path d="M8 48 Q48 2 84 34" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(84 34) rotate(41)"/>
""",
  "Inherited verbatim from Level 1 and 2. Going back round a loop, or one epoch returning to the top of "
  "the training loop.")

M("motif-badge-check", "Correct badge",
  "A round badge with a tick inside, meaning correct.", "0 0 100 100", """
  <circle cx="50" cy="50" r="34" fill="#E2F7ED" stroke="#1B7A4B" stroke-width="3"/>
  <polyline points="34,52 45,64 68,38" fill="none" stroke="#1B7A4B" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
""",
  "Inherited verbatim from Level 1 and 2. It ran / it passed / after the fix. Text-free, scale freely.")

M("motif-badge-cross", "Wrong badge",
  "A round badge with a cross inside, meaning wrong.", "0 0 100 100", """
  <circle cx="50" cy="50" r="34" fill="#F6AEA6" stroke="#CC2B1D" stroke-width="3"/>
  <g stroke="#CC2B1D" stroke-width="6" stroke-linecap="round">
    <line x1="38" y1="38" x2="62" y2="62"/>
    <line x1="62" y1="38" x2="38" y2="62"/>
  </g>
""",
  "Inherited verbatim from Level 1 and 2. It crashed / it failed / before the fix. Text-free, scale freely.")

M("motif-box", "Labelled box",
  "A rounded box with a label inside.", "0 0 120 80", """
  <rect x="6" y="10" width="108" height="60" rx="10" fill="#F5F8FA" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
  <text x="60" y="40" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">Label</text>
""",
  "Inherited verbatim from Level 1 and 2. A neutral stage in a pipeline.")

M("motif-note", "Sticky note",
  "A sticky note with a folded corner and three lines of writing.", "0 0 100 100", """
  <path d="M12 12 H88 V68 L68 88 H12 Z" fill="#E8C671" stroke="#845F00" stroke-width="3" stroke-linejoin="round"/>
  <path d="M68 88 V68 H88 Z" fill="#FFFFFF" stroke="#845F00" stroke-width="3" stroke-linejoin="round"/>
  <g stroke="#55636F" stroke-width="3" stroke-linecap="round">
    <line x1="24" y1="30" x2="76" y2="30"/>
    <line x1="24" y1="43" x2="76" y2="43"/>
    <line x1="24" y1="56" x2="60" y2="56"/>
  </g>
""",
  "Inherited verbatim from Level 1 and 2. A human decision: a model-card entry, a threshold you chose, "
  "a row in the cleaning log.")

M("motif-table", "Data table",
  "A small data table with a shaded header row and six cells.", "0 0 100 100", """
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
""",
  "Inherited verbatim from Level 1 and 2. A table as an ICON, at small size. Text-free, scale freely.")

M("motif-dataframe", "A DataFrame as a grid with a header row and an index",
  "A three-row table with a bold header row reading player, runs, over, a grey index column numbered 0 "
  "to 2, and the runs column outlined and tinted as the current selection.",
  "0 0 272 180", """
  <rect x="22" y="26" width="36" height="32" fill="#F5F8FA"/>
  <rect x="58" y="26" width="64" height="32" fill="#D9EAF9"/>
  <rect x="122" y="26" width="64" height="32" fill="#D9EAF9"/>
  <rect x="186" y="26" width="64" height="32" fill="#D9EAF9"/>
  <rect x="22" y="58" width="36" height="32" fill="#F5F8FA"/>
  <rect x="122" y="58" width="64" height="32" fill="#F4D5E9"/>
  <rect x="22" y="90" width="36" height="32" fill="#F5F8FA"/>
  <rect x="122" y="90" width="64" height="32" fill="#F4D5E9"/>
  <rect x="22" y="122" width="36" height="32" fill="#F5F8FA"/>
  <rect x="122" y="122" width="64" height="32" fill="#F4D5E9"/>
  <g stroke="#C7CDD4" stroke-width="1.5">
    <line x1="58" y1="26" x2="58" y2="154"/>
    <line x1="122" y1="26" x2="122" y2="154"/>
    <line x1="186" y1="26" x2="186" y2="154"/>
    <line x1="22" y1="90" x2="250" y2="90"/>
    <line x1="22" y1="122" x2="250" y2="122"/>
  </g>
  <line x1="22" y1="58" x2="250" y2="58" stroke="#14202B" stroke-width="2"/>
  <text x="90" y="42" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central" font-weight="600">player</text>
  <text x="154" y="42" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central" font-weight="600">runs</text>
  <text x="218" y="42" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central" font-weight="600">over</text>
  <text x="40" y="74" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">0</text>
  <text x="90" y="74" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Meera</text>
  <text x="154" y="74" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">48</text>
  <text x="218" y="74" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">12</text>
  <text x="40" y="106" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">1</text>
  <text x="90" y="106" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Kabir</text>
  <text x="154" y="106" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">31</text>
  <text x="218" y="106" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">9</text>
  <text x="40" y="138" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" dominant-baseline="central">2</text>
  <text x="90" y="138" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">Nova</text>
  <text x="154" y="138" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">57</text>
  <text x="218" y="138" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">15</text>
  <rect x="122" y="26" width="64" height="128" fill="none" stroke="#C42B8C" stroke-width="3"/>
  <rect x="22" y="26" width="228" height="128" fill="none" stroke="#14202B" stroke-width="3"/>
  <text x="154" y="18" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">selected</text>
  <text x="40" y="170" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">index</text>
""",
  "Inherited verbatim from Level 2. Header row = data fill + weight 600. A selection is an accent "
  "OUTLINE plus an accent tint, and it must cover the header too.")

M("motif-array-2d", "A 2-D numpy array as a shaped block",
  "A block of three rows by four columns of numbers, with axis 0 arrowed downwards, axis 1 arrowed "
  "across, and the annotation shape 3 comma 4 below.",
  "0 0 240 172", """
  <line x1="32" y1="34" x2="32" y2="126" stroke="#55636F" stroke-width="2" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#55636F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" transform="translate(32 132) rotate(90)"/>
  <line x1="50" y1="20" x2="204" y2="20" stroke="#55636F" stroke-width="2" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#55636F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" transform="translate(210 20) rotate(0)"/>
  <text x="130" y="12" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">axis 1</text>
  <text x="16" y="84" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle" transform="rotate(-90 16 84)">axis 0</text>
  <rect x="48" y="30" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="69" y="48" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">1</text>
  <rect x="90" y="30" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="111" y="48" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">2</text>
  <rect x="132" y="30" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="153" y="48" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">3</text>
  <rect x="174" y="30" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="195" y="48" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">4</text>
  <rect x="48" y="66" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="69" y="84" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">5</text>
  <rect x="90" y="66" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="111" y="84" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">6</text>
  <rect x="132" y="66" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="153" y="84" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">7</text>
  <rect x="174" y="66" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="195" y="84" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">8</text>
  <rect x="48" y="102" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="69" y="120" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">9</text>
  <rect x="90" y="102" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="111" y="120" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">0</text>
  <rect x="132" y="102" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="153" y="120" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">1</text>
  <rect x="174" y="102" width="42" height="36" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="2"/>
  <text x="195" y="120" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#14202B" text-anchor="middle" dominant-baseline="central">2</text>
  <rect x="48" y="30" width="168" height="108" fill="none" stroke="#1F6FB2" stroke-width="3"/>
  <text x="132" y="158" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">shape (3, 4)</text>
""",
  "Inherited verbatim from Level 2. axis 0 runs DOWN the rows, axis 1 runs ACROSS the columns. Use this "
  "one whenever the lesson is about axis=0 versus axis=1; use motif-tensor-2d when it is about SHAPE.")

M("motif-split", "A train/test split as one cut of the deck",
  "A deck of 100 rows is cut by a dashed line into a train pile of 80 rows and a test pile of 20 rows.",
  "0 0 290 175", """
  <rect x="24" y="30" width="76" height="110" rx="8" fill="#FFFFFF" stroke="#14202B" stroke-width="3" stroke-linejoin="round"/>
  <g stroke="#C7CDD4" stroke-width="1.5">
    <line x1="24" y1="46" x2="100" y2="46"/>
    <line x1="24" y1="62" x2="100" y2="62"/>
    <line x1="24" y1="78" x2="100" y2="78"/>
    <line x1="24" y1="94" x2="100" y2="94"/>
    <line x1="24" y1="110" x2="100" y2="110"/>
    <line x1="24" y1="126" x2="100" y2="126"/>
  </g>
  <text x="62" y="74" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="24" fill="#14202B" text-anchor="middle" dominant-baseline="central">80</text>
  <text x="62" y="130" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="18" fill="#14202B" text-anchor="middle" dominant-baseline="central">20</text>
  <line x1="14" y1="118" x2="110" y2="118" stroke="#C42B8C" stroke-width="2" stroke-dasharray="6 4"/>
  <line x1="104" y1="74" x2="150" y2="60" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(150 60) rotate(-16.9)"/>
  <line x1="104" y1="128" x2="150" y2="124" stroke="#14202B" stroke-width="3" stroke-linecap="round"/>
  <polyline points="-13,-8 0,0 -13,8" fill="none" stroke="#14202B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(150 124) rotate(-5)"/>
  <rect x="154" y="34" width="124" height="54" rx="10" fill="#D9EAF9" stroke="#1F6FB2" stroke-width="3" stroke-linejoin="round"/>
  <text x="216" y="56" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">train</text>
  <text x="216" y="76" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">80 rows</text>
  <rect x="154" y="102" width="124" height="46" rx="10" fill="#F4D5E9" stroke="#C42B8C" stroke-width="3" stroke-linejoin="round"/>
  <text x="216" y="120" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#14202B" text-anchor="middle" dominant-baseline="central">test</text>
  <text x="216" y="140" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">20 rows</text>
  <text x="150" y="166" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#55636F" text-anchor="middle">one cut, then never mix them</text>
""",
  "Inherited verbatim from Level 2. Use it for a TWO-way split; Level 3 splits three ways, so reach for "
  "motif-split-three unless the week genuinely has no validation set.")

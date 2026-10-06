"""One-command build for the Level 4 figure system.

USAGE (run from this folder, or anywhere):

    python3 _gen_build.py          # regenerate everything, deterministically, then audit
    python3 _gen_audit.py          # audit only: must print "--- 0 finding(s)"

WHAT IT WRITES (all generated; edit the _gen_*.py modules, never these outputs):
    ../_motifs.svg                          sprite sheet of the Level 4 motifs   (_gen_motifs.py)
    ../_preview.html                        eyeball page: palette, motifs, patterns, every fig-*.svg
    ../fig-w01-0-where-this-fits.svg ...    the 36 Growing Map figures           (_gen_map.py)
                                            titles/types are read from ../../README.md 'All 36 Weeks'

WHAT IT NEVER TOUCHES: hand-authored week figures fig-wNN-<n>-*.svg with n >= 1. Only the
36 files named fig-wNN-0-where-this-fits.svg are rewritten. Run it again and nothing changes
(the numbers come from _gen_data.py: a seeded numpy run plus ledger values, no randomness at
run time).

MODULES (dependency order):
    _gen_core.py    palette, helpers, motif registry         (inherited values, new helpers)
    _gen_data.py    every number a motif prints, with its provenance (STYLE.md 2.1)
    _gen_motifs.py  the motifs
    _gen_pat.py     the composition patterns
    _gen_map.py     the Growing Map spine and its 36 figures
    _gen_emit.py    writes the sprite sheet, preview page and maps
    _gen_audit.py   bounds, 12px floor, banned constructs, collisions, palette, a11y contract
"""
import os
import re
import subprocess
import sys
import xml.dom.minidom as md

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import _gen_emit as E                       # noqa: E402
import _gen_b11                             # noqa: E402  block 11 (weeks 31-33)
from _gen_core import MOTIFS                # noqa: E402
from _gen_pat import PATTERNS               # noqa: E402
import _gen_b07                         # noqa: E402  (block 7: weeks 19-21)
import _gen_b03                             # noqa: E402  block 3: weeks 7-9 concept figures


def main():
    n_maps = E.emit_maps()
    import _gen_b05                         # block 5: weeks 13-15 concept figures
    _gen_b05.emit(E.HERE)
    import _gen_b06                         # block 6: weeks 16-18 concept figures
    _gen_b06.emit()
    import _gen_b10                          # block 10 (weeks 28-30)
    _gen_b10.emit_b10()
    import _gen_b01                          # block 1 (weeks 1-3)
    _gen_b01.emit(E.HERE)
    import _gen_b02                          # block 2 (weeks 4-6)
    for _n, _svg in _gen_b02.build().items():
        open(os.path.join(E.HERE, _n), 'w').write(_svg + '\n')
    import _gen_b09
    _gen_b09.emit(E.HERE)
    import _gen_b12
    for _n, _svg in _gen_b12.build().items():
        open(os.path.join(E.HERE, _n), 'w').write(_svg + '\n')
    for name, svg in _gen_b03.build().items():      # block 3 (weeks 7-9)
        open(os.path.join(E.HERE, name), "w").write(svg + "\n")
    _gen_b11.emit()
    _gen_b07.emit(E.HERE)
    import _gen_b04                          # block 4 (weeks 10-12)
    _gen_b04.emit_b04()
    import _gen_b08                          # block 8 (weeks 22-24)
    _gen_b08.emit_b08()
    E.emit_motifs()
    E.emit_preview()
    # every pattern, the sprite sheet and every map must be valid XML
    for p in PATTERNS:
        md.parseString(E.pattern_svg(p))
    md.parse(os.path.join(E.HERE, "_motifs.svg"))
    for f in E.figure_files():
        md.parse(os.path.join(E.HERE, f))
    print("motifs: %d   patterns: %d   growing maps: %d" % (len(MOTIFS), len(PATTERNS), n_maps))
    print("all pattern / sprite / figure XML parses OK")
    here = os.path.dirname(os.path.abspath(__file__))
    r = subprocess.run([sys.executable, os.path.join(here, "_gen_audit.py")], capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())

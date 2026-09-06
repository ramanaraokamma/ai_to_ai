"""Emit _motifs.svg and _preview.html."""
import os
from _gen_core import *
from _gen_pat import PATTERNS, EXAMPLES, BY_ID
from _gen_term import INHERITED

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # figures/
NEW = [m for m in MOTIFS if m["id"] not in INHERITED]
OLD = [m for m in MOTIFS if m["id"] in INHERITED]

PALETTE = [("data", DATA_S, DATA_F, "5.28:1", 108, 232),
           ("model", MODEL_S, MODEL_F, "7.10:1", 88, 212),
           ("human", HUMAN_S, HUMAN_F, "5.80:1", 101, 202),
           ("correct", OK_S, OK_F, "5.34:1", 107, 242),
           ("wrong", BAD_S, BAD_F, "5.34:1", 107, 192),
           ("accent", ACC_S, ACC_F, "5.16:1", 109, 222),
           ("ink", INK, None, "16.52:1", 31, None),
           ("paper", PAPER, None, "1.00:1", 255, None)]


def pattern_svg(p):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img">\n'
            '  <title>%s</title>\n  <desc>%s</desc>\n%s\n</svg>' % (p["vb"], p["title"], p["desc"], p["body"]))


# ------------------------------------------------------------------ _motifs.svg
def emit_motifs():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<!-- AI Academy - Level 2 (Builder) - motif sprite sheet.',
           '     Use:  <use href="_motifs.svg#motif-list" x="40" y="40" width="320" height="126"/>',
           '     Or open this file and copy the contents of a <symbol> inline into your figure.',
           '     Every motif is drawn to its own viewBox with the origin at the top-left,',
           '     so translate(x,y) puts its top-left corner at exactly (x,y).',
           '     Motifs marked INHERITED are copied verbatim from Level 1 - do not redraw them. -->',
           '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10" role="img" aria-hidden="true" style="display:none">',
           '  <title>AI Academy Level 2 motif sprite sheet</title>',
           '  <desc>A hidden library of reusable motif symbols for Level 2 figures: code, data, charts and errors.</desc>']
    for m in MOTIFS:
        tag = " INHERITED from Level 1" if m["id"] in INHERITED else ""
        out.append('  <!-- %s%s -->' % (m["id"], tag))
        out.append('  <symbol id="%s" viewBox="%s">' % (m["id"], m["vb"]))
        out.append('    <title>%s</title>' % m["title"])
        out.append('    <desc>%s</desc>' % m["desc"])
        out.append(m["body"])
        out.append('  </symbol>')
    out.append('</svg>')
    open(os.path.join(HERE, "_motifs.svg"), "w").write("\n".join(out) + "\n")


# ------------------------------------------------------------------ _preview.html
CSS = """  :root { --ink:#14202B; --mut:#55636F; --grid:#C7CDD4; --panel:#F5F8FA; }
  body { font-family:ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; color:var(--ink); background:#fff; margin:0; padding:32px; line-height:1.5; }
  .wrap { max-width:1100px; margin:0 auto; }
  h1 { font-size:28px; margin:0 0 4px; } h2 { font-size:20px; margin:40px 0 12px; border-bottom:2px solid var(--grid); padding-bottom:6px; }
  h3 { font-size:15px; margin:0 0 4px; font-weight:600; } h3 span { color:var(--mut); font-weight:400; font-size:12px; }
  p.lead { color:var(--mut); margin:0 0 8px; }
  code { font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:12px; background:var(--panel); padding:1px 5px; border-radius:4px; }
  .bar { position:sticky; top:0; background:#fff; border-bottom:2px solid var(--grid); padding:10px 0; margin-bottom:8px; z-index:9; }
  .bar label { margin-right:20px; font-size:14px; cursor:pointer; }
  .swatches { display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:10px; }
  .sw { display:grid; grid-template-columns:34px 1fr; gap:4px 10px; align-items:center; border:1.5px solid var(--grid); border-radius:8px; padding:10px; }
  .sw .chip { grid-row:1/4; width:34px; height:34px; border-radius:8px; border:3px solid; }
  .sw b { font-size:14px; } .sw span { font-size:11px; color:var(--mut); }
  .motifs { display:grid; grid-template-columns:repeat(auto-fill,minmax(170px,1fr)); gap:12px; }
  .motifs figure { margin:0; border:1.5px solid var(--grid); border-radius:10px; padding:10px; text-align:center; }
  .motifs svg { width:100%; height:108px; }
  figcaption { margin-top:6px; display:flex; flex-direction:column; gap:2px; }
  figcaption span { font-size:10px; color:var(--mut); }
  .pat { margin:0 0 26px; } .pat .frame { border:1.5px solid var(--grid); border-radius:10px; padding:8px; }
  .pat svg { width:100%; height:auto; display:block; }
  p.note { font-size:12px; color:var(--mut); margin:0 0 8px; }
  .pair { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
  body.grey { filter:grayscale(1); }
  body.dark { background:#20262c; }"""


def emit_preview():
    o = ['<!DOCTYPE html>',
         '<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
         '<title>AI Academy - Level 2 figure style system</title>', '<style>', CSS, '</style></head>', '<body>']
    sprite = ['<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">']
    for m in MOTIFS:
        sprite.append('<symbol id="%s" viewBox="%s"><title>%s</title><desc>%s</desc>%s</symbol>'
                      % (m["id"], m["vb"], m["title"], m["desc"], m["body"]))
    sprite.append('</svg>')
    o.append("".join(sprite))
    o += ['<div class="wrap">',
          '<h1>AI Academy &mdash; Level 2 (Builder) figure style system</h1>',
          '<p class="lead">A faithful extension of Level 1. Same palette, same strokes, same type scale &mdash; '
          'plus the motifs Level 2 needs for code and data. Toggle greyscale to run the print check.</p>',
          '<div class="bar">',
          '  <label><input type="checkbox" onchange="document.body.classList.toggle(\'grey\',this.checked)"> Greyscale (print check)</label>',
          '  <label><input type="checkbox" onchange="document.body.classList.toggle(\'dark\',this.checked)"> Dark page (transparency check)</label>',
          '</div>',
          '<h2>Palette &mdash; inherited verbatim from Level 1</h2>', '<div class="swatches">']
    for name, s, f, aa, gs, gf in PALETTE:
        o.append('<div class="sw"><div class="chip" style="background:%s;border-color:%s"></div>' % (f or s, s))
        extra = " &middot; fill grey %s" % gf if gf else ""
        o.append('<b>%s</b><code>%s</code><span>AA %s &middot; stroke grey %s%s</span>' % (name, s, aa, gs, extra))
        o.append('<code>%s</code></div>' % f if f else '</div>')
    o.append('</div>')
    o.append('<h2>Level 2 motifs (%d)</h2>' % len(NEW))
    o.append('<p class="lead">Rendered through <code>&lt;use href="#motif-id"/&gt;</code> from the inlined sprite.</p>')
    o.append('<div class="motifs">')
    for m in NEW:
        o.append('<figure><svg viewBox="%s" role="img" aria-label="%s"><use href="#%s"/></svg>' % (m["vb"], m["title"], m["id"]))
        o.append('<figcaption><code>%s</code><span>%s</span></figcaption></figure>' % (m["id"], m["vb"]))
    o.append('</div>')
    o.append('<h2>Inherited from Level 1 (%d) &mdash; do not redraw</h2><div class="motifs">' % len(OLD))
    for m in OLD:
        o.append('<figure><svg viewBox="%s" role="img" aria-label="%s"><use href="#%s"/></svg>' % (m["vb"], m["title"], m["id"]))
        o.append('<figcaption><code>%s</code><span>%s</span></figcaption></figure>' % (m["id"], m["vb"]))
    o.append('</div>')
    o.append('<h2>The hard rule: a figure is not a picture of code</h2>')
    o.append('<p class="lead">Same lesson, drawn twice. The left one is banned.</p><div class="pair">')
    for eid, etitle, esvg in EXAMPLES:
        inner = esvg.split(">", 1)[1].rsplit("</svg>", 1)[0]
        o.append('<section class="pat"><h3>%s <span>0 0 500 300</span></h3>' % eid)
        o.append('<div class="frame"><svg viewBox="0 0 500 300" role="img">%s</svg></div></section>' % inner)
    o.append('</div>')
    o.append('<h2>Composition patterns (%d)</h2>' % len(PATTERNS))
    for p in PATTERNS:
        w = p["vb"].split()[2]
        o.append('<section class="pat"><h3>%s <span>%s</span></h3><p class="note">%s</p>' % (p["id"], p["vb"], p["note"]))
        o.append('<div class="frame" style="max-width:%spx"><svg viewBox="%s" role="img"><title>%s</title><desc>%s</desc>\n%s\n</svg></div></section>'
                 % (w, p["vb"], p["title"], p["desc"], p["body"]))
    o.append('</div></body></html>')
    open(os.path.join(HERE, "_preview.html"), "w").write("\n".join(o) + "\n")


if __name__ == "__main__":
    emit_motifs()
    emit_preview()
    # every pattern and example must stand alone as valid XML
    import xml.dom.minidom as md
    for p in PATTERNS:
        md.parseString(pattern_svg(p))
    for eid, et, es in EXAMPLES:
        md.parseString(es)
    md.parse(os.path.join(HERE, "_motifs.svg"))
    print("motifs: %d new + %d inherited = %d" % (len(NEW), len(OLD), len(MOTIFS)))
    print("patterns: %d, examples: %d" % (len(PATTERNS), len(EXAMPLES)))
    print("all pattern/example/sprite XML parses OK")

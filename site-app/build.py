"""
AI Academy — static site generator.

Renders the Level 1 36-week course (markdown) into a self-contained static site with
two navigation modes:

  Student mode  — chapters, workbooks, projects. Served as plain HTML.
  Teacher mode  — lesson scripts, orientation, term tests, style guide.
                  Encrypted at build time with AES-256-GCM; the browser derives the
                  key from a passphrase via PBKDF2 and decrypts with WebCrypto.
                  Without the passphrase the bytes on disk are unreadable.

Stdlib only, except `cryptography` for AES-GCM at build time.

Usage:
    python3 site-app/build.py --passphrase "your phrase here"
    python3 site-app/serve.sh
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
except ImportError:
    sys.exit("This build needs `cryptography`. Install it with:  pip install cryptography")

ROOT = Path(__file__).resolve().parent.parent
COURSE = ROOT / "levels" / "level-1-explorer" / "36-week-course"
OUT = Path(__file__).resolve().parent / "dist"

PBKDF2_ITERATIONS = 250_000

TERMS = [
    (1, "Spotting AI in the Wild", 1, 9, "What is AI really, and what is it made of?"),
    (2, "Teaching a Machine to Guess", 10, 18, "How do you turn the world into examples a machine can learn from?"),
    (3, "Trust, Proof, and Pixels", 19, 27, "How do you prove a model is any good — and what is it looking at?"),
    (4, "Words, Fairness, and Your Own AI", 28, 36, "How do machines handle language, who does AI let down, and can you build one and defend it honestly?"),
]


# ─────────────────────────────────────────────────────────────────────────────
# Markdown → HTML
# ─────────────────────────────────────────────────────────────────────────────

RAW_HTML_PREFIXES = ("<details", "</details", "<summary", "</summary", "<a id=", "</a>")


def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE).strip().lower()
    return re.sub(r"[\s_-]+", "-", text) or "section"


class Inline:
    """Inline markdown: code, bold, italic, links, images. Escapes everything else."""

    def __init__(self, link_resolver):
        self.resolve = link_resolver

    def render(self, text: str) -> str:
        out, i, n = [], 0, len(text)
        while i < n:
            ch = text[i]

            # `code`  (highest precedence — no markup inside)
            if ch == "`":
                m = re.match(r"(`+)(.+?)\1", text[i:], re.S)
                if m:
                    out.append(f"<code>{html.escape(m.group(2))}</code>")
                    i += m.end()
                    continue

            # ![alt](src)
            if ch == "!" and text.startswith("![", i):
                m = re.match(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)", text[i:])
                if m:
                    alt, src = html.escape(m.group(1)), self.resolve(m.group(2))
                    out.append(
                        f'<img src="{html.escape(src)}" alt="{alt}" loading="lazy" decoding="async">'
                    )
                    i += m.end()
                    continue

            # [text](href)
            if ch == "[":
                m = re.match(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)", text[i:])
                if m:
                    label, href = self.render(m.group(1)), self.resolve(m.group(2))
                    ext = ' target="_blank" rel="noopener"' if href.startswith(("http://", "https://")) else ""
                    out.append(f'<a href="{html.escape(href)}"{ext}>{label}</a>')
                    i += m.end()
                    continue

            # ***bold italic*** / **bold** / *italic*
            if ch == "*":
                for marker, tag in (("***", "strong><em"), ("**", "strong"), ("*", "em")):
                    if text.startswith(marker, i):
                        close = text.find(marker, i + len(marker))
                        if close != -1:
                            inner = self.render(text[i + len(marker):close])
                            if tag == "strong><em":
                                out.append(f"<strong><em>{inner}</em></strong>")
                            else:
                                out.append(f"<{tag}>{inner}</{tag}>")
                            i = close + len(marker)
                            break
                else:
                    out.append("*")
                    i += 1
                continue

            out.append(html.escape(ch))
            i += 1
        return "".join(out)


@dataclass
class Heading:
    level: int
    text: str
    anchor: str


class MarkdownRenderer:
    def __init__(self, link_resolver):
        self.inline = Inline(link_resolver)
        self.headings: list[Heading] = []
        self.plain: list[str] = []

    def render(self, src: str) -> str:
        lines = src.replace("\r\n", "\n").split("\n")
        out: list[str] = []
        i, n = 0, len(lines)

        while i < n:
            line = lines[i]
            stripped = line.strip()

            # blank
            if not stripped:
                i += 1
                continue

            # fenced code
            if stripped.startswith("```"):
                lang = stripped[3:].strip()
                i += 1
                buf = []
                while i < n and not lines[i].strip().startswith("```"):
                    buf.append(lines[i])
                    i += 1
                i += 1  # closing fence
                cls = f' class="lang-{html.escape(lang)}"' if lang else ""
                body = html.escape("\n".join(buf))
                out.append(f'<pre{cls}><code>{body}</code></pre>')
                continue

            # raw HTML we deliberately allow through
            if stripped.startswith(RAW_HTML_PREFIXES):
                out.append(stripped)
                self.plain.append(re.sub(r"<[^>]+>", " ", stripped))
                i += 1
                continue

            # horizontal rule
            if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", stripped):
                out.append("<hr>")
                i += 1
                continue

            # heading
            m = re.match(r"(#{1,6})\s+(.*)$", stripped)
            if m:
                level = len(m.group(1))
                raw = m.group(2).rstrip("#").strip()
                anchor = slugify(raw)
                base, k = anchor, 2
                existing = {h.anchor for h in self.headings}
                while anchor in existing:
                    anchor = f"{base}-{k}"
                    k += 1
                self.headings.append(Heading(level, re.sub(r"[*`]", "", raw), anchor))
                self.plain.append(raw)
                out.append(f'<h{level} id="{anchor}">{self.inline.render(raw)}'
                            f'<a class="anchor" href="#{anchor}" aria-label="Link to this section">#</a></h{level}>')
                i += 1
                continue

            # table
            if stripped.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|?\s*$", lines[i + 1]):
                i, tbl = self._table(lines, i)
                out.append(tbl)
                continue

            # blockquote
            if stripped.startswith(">"):
                buf = []
                while i < n and lines[i].strip().startswith(">"):
                    buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                    i += 1
                inner = MarkdownRenderer(self.inline.resolve)
                body = inner.render("\n".join(buf))
                self.plain.extend(inner.plain)
                out.append(f"<blockquote>{body}</blockquote>")
                continue

            # list
            if re.match(r"^\s*([-*+]|\d+[.)])\s+", line):
                i, lst = self._list(lines, i)
                out.append(lst)
                continue

            # paragraph
            buf = []
            while i < n and lines[i].strip() and not self._starts_block(lines, i):
                buf.append(lines[i].strip())
                i += 1
            text = " ".join(buf)
            self.plain.append(text)
            # a lone italic line right after an image is a figure caption
            cap = re.fullmatch(r"\*([^*].*?)\*", text)
            if cap and out and out[-1].startswith("<p><img"):
                out[-1] = out[-1][:-4] + f'<span class="caption">{self.inline.render(cap.group(1))}</span></p>'
            else:
                rendered = self.inline.render(text)
                cls = ' class="figure"' if rendered.startswith("<img") else ""
                out.append(f"<p{cls}>{rendered}</p>")

        return "\n".join(out)

    def _starts_block(self, lines, i) -> bool:
        s = lines[i].strip()
        return (
            s.startswith(("```", ">", "|"))
            or s.startswith(RAW_HTML_PREFIXES)
            or bool(re.match(r"#{1,6}\s", s))
            or bool(re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", s))
            or bool(re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i]))
        )

    def _table(self, lines, i):
        def cells(row):
            row = row.strip()
            row = row[1:] if row.startswith("|") else row
            row = row[:-1] if row.endswith("|") else row
            return [c.strip() for c in re.split(r"(?<!\\)\|", row)]

        header = cells(lines[i])
        aligns = []
        for spec in cells(lines[i + 1]):
            left, right = spec.startswith(":"), spec.endswith(":")
            aligns.append("center" if left and right else "right" if right else "left" if left else "")
        i += 2
        rows = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            rows.append(cells(lines[i]))
            i += 1

        def cell(tag, text, idx):
            a = aligns[idx] if idx < len(aligns) else ""
            style = f' style="text-align:{a}"' if a else ""
            return f"<{tag}{style}>{self.inline.render(text.replace(chr(92) + '|', '|'))}</{tag}>"

        thead = "".join(cell("th", c, k) for k, c in enumerate(header))
        body = []
        for r in rows:
            self.plain.append(" ".join(r))
            body.append("<tr>" + "".join(cell("td", c, k) for k, c in enumerate(r)) + "</tr>")
        self.plain.append(" ".join(header))
        return i, (f'<div class="table-wrap"><table><thead><tr>{thead}</tr></thead>'
                   f'<tbody>{"".join(body)}</tbody></table></div>')

    def _list(self, lines, i):
        def info(line):
            m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", line)
            if not m:
                return None
            return len(m.group(1).replace("\t", "    ")), m.group(2), m.group(3)

        base = info(lines[i])[0]
        ordered = info(lines[i])[1][0].isdigit()
        items: list[list[str]] = []
        while i < len(lines):
            meta = info(lines[i])
            if meta and meta[0] <= base + 1:
                if meta[0] < base:
                    break
                items.append([meta[2]])
                i += 1
            elif items and lines[i].strip() and (info(lines[i]) or
                    len(lines[i]) - len(lines[i].lstrip()) > base):
                items[-1].append(lines[i])
                i += 1
            else:
                break

        html_items = []
        for chunk in items:
            first, rest = chunk[0], chunk[1:]
            self.plain.append(first)
            body = self.inline.render(first)
            if rest:
                dedent = "\n".join(
                    ln[min((len(l) - len(l.lstrip()) for l in rest if l.strip()), default=0):]
                    for ln in rest
                )
                sub = MarkdownRenderer(self.inline.resolve)
                body += sub.render(dedent)
                self.plain.extend(sub.plain)
            html_items.append(f"<li>{body}</li>")
        tag = "ol" if ordered else "ul"
        return i, f"<{tag}>{''.join(html_items)}</{tag}>"


# ─────────────────────────────────────────────────────────────────────────────
# Content model
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Doc:
    src: Path
    route: str          # e.g. "chapter/week-01.html"
    mode: str           # "student" | "teacher"
    kind: str           # chapter | workbook | lesson | test | project | page
    week: int | None
    title: str = ""
    nav_label: str = ""
    headings: list[Heading] = field(default_factory=list)
    body: str = ""
    text: str = ""


def first_h1(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").split("\n"):
        if line.startswith("# "):
            return re.sub(r"[*`]", "", line[2:]).strip()
    return path.stem


def discover() -> list[Doc]:
    docs: list[Doc] = []

    def add(src, route, mode, kind, week, nav_label=None):
        if not src.exists():
            print(f"  ! missing, skipped: {src.relative_to(ROOT)}")
            return
        t = first_h1(src)
        docs.append(Doc(src, route, mode, kind, week, t, nav_label or t))

    for wk in range(1, 37):
        nn = f"{wk:02d}"
        add(COURSE / "student-guide" / f"week-{nn}.md", f"chapter/week-{nn}.html", "student", "chapter", wk)
        add(COURSE / "workbook" / f"week-{nn}.md", f"workbook/week-{nn}.html", "student", "workbook", wk)
        add(COURSE / "teacher-guide" / f"week-{nn}.md", f"lesson/week-{nn}.html", "teacher", "lesson", wk)

    add(COURSE / "teacher-guide" / "00-orientation.md", "lesson/orientation.html", "teacher", "lesson", None,
        "Teacher Orientation — learn AI first")
    for t in range(1, 5):
        add(COURSE / "assessments" / f"term-{t}-test.md", f"tests/term-{t}.html", "teacher", "test", None,
            f"Term {t} Test")
    add(COURSE / "assessments" / "README.md", "tests/marking.html", "teacher", "test", None,
        "Marking & Remediation")
    add(COURSE / "figures" / "STYLE.md", "lesson/style-guide.html", "teacher", "lesson", None, "Figure Style Guide")

    add(COURSE / "projects" / "project-ideas.md", "projects/ideas.html", "student", "project", None, "50 Project Ideas")
    add(COURSE / "projects" / "worked-example-project.md", "projects/worked-example.html", "student", "project", None,
        "A Finished Project, Marked")
    add(COURSE / "projects" / "capstone.md", "projects/capstone.html", "student", "project", None, "The Capstone")
    add(COURSE / "HOW-TO-USE.md", "how-to-use.html", "student", "page", None, "How To Use This Course")
    add(COURSE / "README.md", "plan.html", "student", "page", None, "The 36-Week Plan")

    # Level 1 reference material the weekly files link to
    L1 = COURSE.parent
    add(L1 / "glossary.md", "glossary.html", "student", "page", None, "Glossary — every word, defined")
    add(L1 / "README.md", "level-overview.html", "student", "page", None, "About Level 1")
    add(L1 / "capstone.md", "projects/capstone-brief.html", "student", "project", None, "Capstone — original brief")
    add(L1 / "assessment.md", "tests/level-1-exit-exam.html", "teacher", "test", None, "Level 1 Exit Exam")
    for mod in sorted(L1.glob("module-0*.md")):
        num = re.match(r"module-(\d+)", mod.stem).group(1)
        add(mod, f"modules/module-{num}.html", "student", "page", None,
            f"Module {int(num)} — {first_h1(mod).split('—', 1)[-1].strip()}")
    return docs


# Directory links in the markdown map to a representative page.
DIR_ALIASES = {
    "student-guide": "chapter/week-01.html",
    "workbook": "workbook/week-01.html",
    "teacher-guide": "lesson/orientation.html",
    "assessments": "tests/marking.html",
    "projects": "projects/ideas.html",
    "figures": "gallery.html",
}


def build_route_map(docs) -> dict[Path, str]:
    m = {d.src.resolve(): d.route for d in docs}
    for svg in (COURSE / "figures").glob("*.svg"):
        m[svg.resolve()] = f"assets/figures/{svg.name}"
    return m


def make_resolver(doc: Doc, routes: dict[Path, str]):
    here = Path(doc.route).parent

    def rel(target_route: str) -> str:
        return os.path.relpath(target_route, here.as_posix() if here.as_posix() != "." else ".")

    def resolve(link: str) -> str:
        if link.startswith(("http://", "https://", "mailto:", "#", "data:")):
            return link
        frag = ""
        if "#" in link:
            link, frag = link.split("#", 1)
            frag = "#" + frag
        if not link:
            return frag
        target = (doc.src.parent / link).resolve()
        if target in routes:
            return rel(routes[target]) + frag
        if target.is_dir():
            for cand in ("README.md", "index.md"):
                if (target / cand).resolve() in routes:
                    return rel(routes[(target / cand).resolve()]) + frag
            if target.name in DIR_ALIASES:
                return rel(DIR_ALIASES[target.name]) + frag
        # outside the generated site — flagged by the build and rendered inert
        return "unavailable:" + link + frag

    return resolve


# ─────────────────────────────────────────────────────────────────────────────
# Encryption
# ─────────────────────────────────────────────────────────────────────────────

def derive_key(passphrase: str, salt: bytes) -> bytes:
    return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                      iterations=PBKDF2_ITERATIONS).derive(passphrase.encode())


def encrypt_bytes(key: bytes, plaintext: bytes) -> dict:
    nonce = os.urandom(12)
    ct = AESGCM(key).encrypt(nonce, plaintext, None)
    return {"iv": base64.b64encode(nonce).decode(), "ct": base64.b64encode(ct).decode()}


def encrypt(key: bytes, plaintext: str) -> dict:
    return encrypt_bytes(key, plaintext.encode("utf-8"))


# ─────────────────────────────────────────────────────────────────────────────
# Page shell
# ─────────────────────────────────────────────────────────────────────────────

def shell(*, doc: Doc, depth: int, nav_json: str, body: str, encrypted: bool) -> str:
    up = "../" * depth
    week_badge = f'<span class="badge wk">Week {doc.week}</span>' if doc.week else ""
    kind_label = {"chapter": "Student Chapter", "workbook": "Workbook", "lesson": "Lesson Script",
                  "test": "Assessment", "project": "Project", "page": "Course Info"}[doc.kind]
    toc = "".join(
        f'<a class="toc-l{h.level}" href="#{h.anchor}">{html.escape(h.text)}</a>'
        for h in doc.headings if 2 <= h.level <= 3
    )

    if encrypted:
        tier_note = ("This is <strong>teacher material</strong> — a lesson script, an answer key or a "
                     "test. Only the teacher passcode opens it."
                     if doc.mode == "teacher" else
                     "Enter your passcode to read this page. Either the student or the teacher "
                     "passcode will open it.")
        content = (
            f'<div id="locked" class="locked"><div class="lock-card">'
            f'<div class="lock-ico" aria-hidden="true">🔒</div>'
            f'<h2>{"Teacher material" if doc.mode == "teacher" else "Locked"}</h2>'
            f'<p>{tier_note} It stays unlocked for the rest of this browser session.</p>'
            f'<form id="unlock-form"><label class="sr-only" for="pass">Passcode</label>'
            f'<input id="pass" type="password" autocomplete="current-password" '
            f'placeholder="Passcode" required></input>'
            f'<button type="submit">Unlock</button></form>'
            f'<p id="lock-msg" class="lock-msg" role="status"></p>'
            f'<p class="lock-foot"><a href="{up}index.html">← Back to the course home page</a></p>'
            f'</div></div>'
            f'<article id="content" class="doc" hidden data-tier="{doc.mode}" '
            f'data-enc="{up}assets/enc/{doc.route.replace("/", "__")}.json"></article>')
    else:
        content = f'<article id="content" class="doc">{body}</article>'

    return f"""<!DOCTYPE html>
<html lang="en" data-mode="{doc.mode}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(doc.title)} · AI Academy</title>
<link rel="stylesheet" href="{up}assets/app.css">
<script>try{{document.documentElement.dataset.theme=localStorage.getItem('aia-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light')}}catch(e){{}}</script>
</head>
<body data-depth="{depth}">
<a class="skip" href="#content">Skip to content</a>
<header class="top">
  <a class="brand" href="{up}index.html"><span class="logo">AI</span> Academy</a>
  <div class="modes" role="group" aria-label="Navigation mode">
    <a href="{up}index.html#student" class="mode-btn" data-mode-btn="student">🎒 Student</a>
    <a href="{up}index.html#teacher" class="mode-btn" data-mode-btn="teacher">🧑‍🏫 Teacher <span class="lk" aria-hidden="true">🔒</span></a>
  </div>
  <div class="top-right">
    <span id="who" class="who-chip" hidden></span>
    <button id="signout" class="icon-btn" aria-label="Sign out" title="Sign out" hidden>⎋</button>
    <button id="theme" class="icon-btn" aria-label="Toggle dark mode" title="Toggle dark mode">◐</button>
    <button id="nav-toggle" class="icon-btn only-mobile" aria-label="Toggle navigation" aria-expanded="false">☰</button>
  </div>
</header>
<div class="layout">
  <nav id="side" class="side" aria-label="Course navigation">
    <input id="nav-search" class="nav-search" type="search" placeholder="Search this course…" aria-label="Search the course">
    <div id="nav-tree"></div>
  </nav>
  <main class="main">
    <div class="crumbs">{week_badge}<span class="badge kind">{kind_label}</span></div>
    {content}
    <nav class="pager" id="pager" aria-label="Previous and next"></nav>
  </main>
  <aside class="toc" aria-label="On this page">{'<h2>On this page</h2>' + toc if toc else ''}</aside>
</div>
<script>window.AIA_NAV={nav_json};window.AIA_ROUTE="{doc.route}";window.AIA_UP="{up}";</script>
<script src="{up}assets/app.js"></script>
</body>
</html>
"""


# ─────────────────────────────────────────────────────────────────────────────
# Week metadata (from the course plan table)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Week:
    number: int
    term: int
    title: str
    big_idea: str
    type: str
    homework: str


TYPE_ICON = {"teach": ("📘", "t"), "lab": ("🔬", "l"), "project": ("🛠️", "p"),
             "review": ("🔁", "r"), "capstone": ("🎪", "c"), "assessment": ("🏁", "a")}


def parse_weeks() -> list[Week]:
    weeks: list[Week] = []
    for line in (COURSE / "README.md").read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^\|\s*(\d{1,2})\s*\|\s*(\d)\s*\|(.+)$", line)
        if not m:
            continue
        rest = [c.strip() for c in m.group(3).split("|")]
        if len(rest) < 4:
            continue
        title, idea, typ, hw = rest[0], rest[1], rest[2], rest[3]
        typ = re.sub(r"[^a-z]", "", typ.lower())
        weeks.append(Week(int(m.group(1)), int(m.group(2)),
                          re.sub(r"[*`]", "", title), re.sub(r"[*`]", "", idea),
                          typ or "teach", re.sub(r"[*`]", "", hw)))
    if len(weeks) != 36:
        print(f"  ! parsed {len(weeks)} weeks from the plan table, expected 36")
    return weeks


def build_nav_payload(weeks: list[Week], docs: list[Doc]) -> str:
    by_week: dict[int, dict[str, str]] = {}
    for d in docs:
        if d.week:
            by_week.setdefault(d.week, {})[d.kind] = d.route
    return json.dumps({
        "terms": [{"number": n, "name": nm, "from": a, "to": b, "question": q}
                  for n, nm, a, b, q in TERMS],
        "weeks": [{"week": w.number, "term": w.term, "title": w.title, "type": w.type,
                   "idea": w.big_idea, "docs": by_week.get(w.number, {})} for w in weeks],
        "flat": [{"route": d.route, "label": d.nav_label, "kind": d.kind, "mode": d.mode}
                 for d in docs if d.week is None],
    }, ensure_ascii=False, separators=(",", ":"))


def home_page(weeks: list[Week], docs: list[Doc], nav_json: str, counts: dict) -> str:
    by_week: dict[int, dict[str, str]] = {}
    for d in docs:
        if d.week:
            by_week.setdefault(d.week, {})[d.kind] = d.route

    terms_html = []
    for idx, (num, name, lo, hi, question) in enumerate(TERMS):
        cards = []
        for w in [x for x in weeks if lo <= x.number <= hi]:
            icon, cls = TYPE_ICON.get(w.type, ("📘", "t"))
            r = by_week.get(w.number, {})
            links = []
            if "chapter" in r:
                links.append(f'<a class="lockable" data-need="student" href="{r["chapter"]}">📗 Chapter</a>')
            if "workbook" in r:
                links.append(f'<a class="lockable" data-need="student" href="{r["workbook"]}">✏️ Workbook</a>')
            if "lesson" in r:
                links.append(f'<a class="lockable tch" data-need="teacher" href="{r["lesson"]}">🧑‍🏫 Lesson script</a>')
            cards.append(
                f'<article class="wk-card" data-week="{w.number}" '
                f'data-search="{html.escape((str(w.number) + " " + w.title + " " + w.big_idea + " " + w.type).lower())}">'
                f'<div class="row1"><span class="num">WEEK {w.number:02d}</span>'
                f'<span class="type-{cls}" title="{w.type}">{icon} {w.type}</span>'
                f'<label class="done"><input type="checkbox" data-done="{w.number}"> done</label></div>'
                f'<h3>{html.escape(w.title)}</h3>'
                f'<p class="idea">{html.escape(w.big_idea)}</p>'
                f'<div class="links">{"".join(links)}</div>'
                f'</article>')
        terms_html.append(
            f'<section class="term" data-term="{num}">'
            f'<div class="term-head"><h2>Term {num} · {html.escape(name)}</h2>'
            f'<span class="rng">Weeks {lo}–{hi}</span>'
            f'<p class="q">{html.escape(question)}</p>'
            f'<div class="term-bar"><i data-term-bar="{num}" style="background:var(--data)"></i></div></div>'
            f'<div class="weeks">{"".join(cards)}</div></section>')

    extras = [d for d in docs if d.week is None]
    extra_links = "".join(
        f'<a class="lockable" href="{d.route}" data-need="{d.mode}">{html.escape(d.nav_label)}</a>'
        for d in extras)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Academy · Level 1 Explorer — 36 weeks</title>
<link rel="stylesheet" href="assets/app.css">
<script>try{{document.documentElement.dataset.theme=localStorage.getItem('aia-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light')}}catch(e){{}}</script>
</head>
<body data-depth="0" class="home">
<a class="skip" href="#year">Skip to the year plan</a>
<header class="top">
  <a class="brand" href="index.html"><span class="logo">AI</span> Academy</a>
  <div class="modes" role="group" aria-label="Navigation mode">
    <a href="#student" class="mode-btn" data-mode-btn="student">🎒 Student</a>
    <a href="#teacher" class="mode-btn" data-mode-btn="teacher">🧑‍🏫 Teacher <span class="lk" aria-hidden="true">🔒</span></a>
  </div>
  <div class="top-right">
    <span id="who" class="who-chip" hidden></span>
    <button id="signout" class="icon-btn" aria-label="Sign out" title="Sign out" hidden>⎋</button>
    <button id="theme" class="icon-btn" aria-label="Toggle dark mode" title="Toggle dark mode">◐</button>
  </div>
</header>

<section class="hero">
  <h1>Level 1 · Explorer</h1>
  <p class="sub">A 36-week AI course for a 6th grader who has never written a line of code —
     and for a teacher who has never taught AI. One class a week, four terms, ending in an AI Fair.</p>

  <!-- ── passcode gate ─────────────────────────────────────────────── -->
  <div id="gate" class="gate">
    <div class="gate-body">
      <div class="gate-ico" aria-hidden="true">🔐</div>
      <div class="gate-text">
        <h2>Enter your passcode to open the course</h2>
        <p>This page is the only one you can read without one. Chapters, workbooks and lesson
           scripts are encrypted until you unlock them.</p>
      </div>
      <form id="gate-form" autocomplete="off">
        <label class="sr-only" for="gate-pass">Passcode</label>
        <input id="gate-pass" type="password" placeholder="Passcode" autocomplete="current-password" required>
        <button type="submit">Unlock</button>
      </form>
      <p id="gate-msg" class="lock-msg" role="status"></p>
      <table class="gate-keys">
        <tr><td>🎒 <strong>Student</strong></td><td>chapters · workbooks · projects · glossary</td></tr>
        <tr><td>🧑‍🏫 <strong>Teacher</strong></td><td>all of the above <em>plus</em> lesson scripts, answer keys, term tests</td></tr>
      </table>
    </div>
  </div>

  <div class="pick" id="pick" hidden>
    <a class="pick-card lockable" href="chapter/week-01.html" data-need="student">
      <div class="ico">🎒</div>
      <h2>Start Week 1 — your chapter</h2>
      <p>Read the chapter, then do the workbook. Mark it yourself from the answer key.</p>
      <span class="who">Chapters · Workbooks · Projects</span>
    </a>
    <a class="pick-card lockable" href="lesson/orientation.html" data-need="teacher">
      <div class="ico">🧑‍🏫</div>
      <h2>Teacher orientation</h2>
      <p>Read this once, before Week 1. It teaches you the whole subject in plain language.</p>
      <span class="who">Lesson scripts · Answer keys · Tests</span>
    </a>
  </div>

  <div class="stats">
    <div class="stat"><div class="n">36</div><div class="l">weekly classes</div></div>
    <div class="stat"><div class="n">4</div><div class="l">terms</div></div>
    <div class="stat"><div class="n">{counts['figures']}</div><div class="l">drawings</div></div>
    <div class="stat"><div class="n">{counts['pages']}</div><div class="l">pages</div></div>
    <div class="stat"><div class="n" id="pct">0%</div><div class="l">you've completed</div></div>
  </div>

  <div class="hero-tools">
    <input id="home-search" class="nav-search" type="search" style="max-width:26rem;margin-top:1.6rem"
           placeholder="Search the 36 weeks — try &quot;bias&quot;, &quot;pixels&quot;, &quot;Scratch&quot;…"
           aria-label="Search the 36 weeks">
    <p id="home-count" class="l" style="color:var(--muted);font-size:.85rem">Showing all 36 weeks</p>
  </div>
  <nav class="links extras" style="display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.6rem">{extra_links}</nav>
</section>

<main class="year" id="year">
{"".join(terms_html)}
</main>

<script>window.AIA_NAV={nav_json};window.AIA_ROUTE="index.html";window.AIA_UP="";</script>
<script src="assets/app.js"></script>
<script src="assets/home.js"></script>
</body>
</html>
"""


HOME_JS = r"""
/* AI Academy — home page: passcode gate, role gating, search, progress. */
(function () {
  'use strict';
  var Auth = window.AIA_auth;
  var LS = { mode: 'aia-mode', done: 'aia-done' };
  function get(k, d) { try { return localStorage.getItem(k) || d; } catch (e) { return d; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  function mode() {
    var h = (location.hash || '').replace('#', '');
    if (h === 'teacher' || h === 'student') set(LS.mode, h);
    var m = get(LS.mode, 'student');
    if (m === 'teacher' && Auth.role() !== 'teacher') m = 'student';
    return m;
  }

  var gate = document.getElementById('gate');
  var pick = document.getElementById('pick');
  var gateForm = document.getElementById('gate-form');
  var gateMsg = document.getElementById('gate-msg');
  var gatePass = document.getElementById('gate-pass');

  /* Everything with .lockable is inert until the right passcode is in. */
  function applyGate() {
    var role = Auth.role();
    var m = mode();

    if (gate) gate.hidden = !!role;
    if (pick) pick.hidden = !role;

    document.querySelectorAll('.lockable').forEach(function (el) {
      var need = el.getAttribute('data-need') || 'student';
      var allowed = Auth.can(need);
      // teacher-only links are also hidden from a student entirely
      var hide = need === 'teacher' && role !== 'teacher';
      el.classList.toggle('hidden', hide && !!role);
      el.classList.toggle('is-locked', !allowed);
      if (allowed) {
        el.removeAttribute('aria-disabled');
        el.removeAttribute('tabindex');
      } else {
        el.setAttribute('aria-disabled', 'true');
        el.setAttribute('tabindex', '-1');
      }
    });

    document.body.classList.toggle('locked-out', !role);
    document.querySelectorAll('[data-mode-btn]').forEach(function (b) {
      b.setAttribute('aria-current', b.getAttribute('data-mode-btn') === m ? 'true' : 'false');
    });
  }

  /* Clicking a locked link bounces you to the passcode box instead of 404-ing. */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('.lockable');
    if (!a || a.getAttribute('aria-disabled') !== 'true') return;
    e.preventDefault();
    if (!Auth.role()) {
      gate.scrollIntoView({ block: 'center' });
      gatePass.focus();
      gateMsg.className = 'lock-msg';
      gateMsg.textContent = 'Enter a passcode first.';
    } else {
      gateMsg.className = 'lock-msg err';
      gateMsg.textContent = 'That page needs the teacher passcode.';
      gate.hidden = false;
      gate.scrollIntoView({ block: 'center' });
      gatePass.focus();
    }
  });

  if (gateForm) {
    gateForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = gateForm.querySelector('button');
      btn.disabled = true;
      gateMsg.className = 'lock-msg';
      gateMsg.textContent = 'Checking…';
      Auth.unlock(gatePass.value)
        .then(function (role) {
          gateMsg.className = 'lock-msg ok';
          gateMsg.textContent = 'Welcome — signed in as ' + role + '.';
          set(LS.mode, role);
          gatePass.value = '';
          applyGate();
          if (window.AIA_refreshChrome) window.AIA_refreshChrome();
        })
        .catch(function () {
          gateMsg.className = 'lock-msg err';
          gateMsg.textContent = 'That passcode does not match. Try again.';
          gatePass.select();
        })
        .then(function () { btn.disabled = false; });
    });
  }

  /* progress */
  function doneSet() { try { return new Set(JSON.parse(get(LS.done, '[]'))); } catch (e) { return new Set(); } }
  function paintProgress() {
    var s = doneSet();
    document.querySelectorAll('[data-done]').forEach(function (cb) {
      cb.checked = s.has(Number(cb.getAttribute('data-done')));
    });
    (window.AIA_NAV.terms || []).forEach(function (t) {
      var tot = t.to - t.from + 1, n = 0;
      for (var w = t.from; w <= t.to; w++) if (s.has(w)) n++;
      var bar = document.querySelector('[data-term-bar="' + t.number + '"]');
      if (bar) bar.style.width = (n / tot * 100) + '%';
    });
    var pct = document.getElementById('pct');
    if (pct) pct.textContent = Math.round(s.size / 36 * 100) + '%';
  }
  document.addEventListener('change', function (e) {
    var cb = e.target.closest('[data-done]');
    if (!cb) return;
    var s = doneSet(), n = Number(cb.getAttribute('data-done'));
    cb.checked ? s.add(n) : s.delete(n);
    set(LS.done, JSON.stringify(Array.from(s)));
    paintProgress();
  });

  /* search */
  var box = document.getElementById('home-search');
  var count = document.getElementById('home-count');
  if (box) {
    box.addEventListener('input', function () {
      var q = box.value.trim().toLowerCase(), shown = 0;
      document.querySelectorAll('.wk-card').forEach(function (c) {
        var hit = !q || (c.getAttribute('data-search') || '').indexOf(q) !== -1;
        c.classList.toggle('hidden', !hit);
        if (hit) shown++;
      });
      document.querySelectorAll('.term').forEach(function (t) {
        t.classList.toggle('hidden', !t.querySelector('.wk-card:not(.hidden)'));
      });
      count.textContent = q ? shown + ' of 36 weeks match “' + box.value.trim() + '”' : 'Showing all 36 weeks';
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && e.target === document.body) { e.preventDefault(); box.focus(); }
    });
  }

  window.addEventListener('hashchange', applyGate);
  applyGate();
  paintProgress();
  if (!Auth.role() && gatePass) gatePass.focus();
})();
"""


def gallery_page(nav_json: str, names: list[str]) -> tuple[str, str]:
    """Returns (page_shell_html, inner_body_html). The body is encrypted like any other page."""
    def week_of(name):
        m = re.match(r"fig-w(\d+)", name)
        return int(m.group(1)) if m else None

    groups: dict[str, list[str]] = {}
    for n in names:
        wk = week_of(n)
        groups.setdefault(f"Week {wk:02d}" if wk else "Shared", []).append(n)

    blocks = []
    for label in sorted(groups, key=lambda s: (s == "Shared", s)):
        items = "".join(
            f'<figure data-search="{html.escape(n.lower())}">'
            f'<img src="assets/figures/{html.escape(n)}" alt="{html.escape(n)}" loading="lazy" decoding="async">'
            f'<figcaption>{html.escape(n)}</figcaption></figure>'
            for n in sorted(groups[label]))
        blocks.append(f'<section class="gal-group" data-search="{html.escape(label.lower())}">'
                      f'<h2>{label} <span class="rng">{len(groups[label])} figures</span></h2>'
                      f'<div class="gal">{items}</div></section>')

    doc = Doc(COURSE / "README.md", "gallery.html", "student", "page", None,
              "Figure Gallery", "Figure Gallery")
    body = (f'<h1 id="figure-gallery">Figure Gallery</h1>'
            f'<p>Every drawing in the course — {len(names)} hand-authored SVGs. '
            f'They scale to any size and print cleanly. Search by filename or week.</p>'
            f'<input id="gal-search" class="nav-search" type="search" placeholder="Filter figures…" '
            f'aria-label="Filter figures">'
            f'<style>.gal{{display:grid;grid-template-columns:repeat(auto-fill,minmax(15rem,1fr));gap:1rem}}'
            f'.gal figure{{margin:0;padding:.8rem;background:var(--bg);border:1px solid var(--line);'
            f'border-radius:12px;text-align:center}}.gal img{{max-height:16rem}}'
            f'.gal figcaption{{margin-top:.5rem;font-size:.72rem;color:var(--muted);'
            f'font-family:var(--mono);word-break:break-all}}'
            f'.gal-group h2 .rng{{font-size:.75rem;color:var(--muted);font-weight:500}}</style>'
            + "".join(blocks) +
            '<script>(function(){var b=document.getElementById("gal-search");if(!b)return;'
            'b.addEventListener("input",function(){var q=b.value.trim().toLowerCase();'
            'document.querySelectorAll(".gal figure").forEach(function(f){'
            'f.classList.toggle("hidden",!!q&&f.getAttribute("data-search").indexOf(q)===-1)});'
            'document.querySelectorAll(".gal-group").forEach(function(g){'
            'g.classList.toggle("hidden",!g.querySelector("figure:not(.hidden)"))})})})();</script>')
    doc.headings = [Heading(1, "Figure Gallery", "figure-gallery")]
    return shell(doc=doc, depth=0, nav_json=nav_json, body=body, encrypted=True), body


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="Build the AI Academy site.")
    ap.add_argument("--student-pass", default=os.environ.get("AIA_STUDENT_PASS", "student1234"),
                    help="Student passcode (or set AIA_STUDENT_PASS)")
    ap.add_argument("--teacher-pass", default=os.environ.get("AIA_TEACHER_PASS", "teacher1234"),
                    help="Teacher passcode (or set AIA_TEACHER_PASS)")
    ap.add_argument("--clean", action="store_true", help="Remove dist/ before building")
    args = ap.parse_args()

    if args.student_pass == args.teacher_pass:
        sys.exit("The student and teacher passcodes must be different.")

    if not COURSE.exists():
        sys.exit(f"Course content not found at {COURSE}")

    if args.clean and OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets" / "enc").mkdir(parents=True, exist_ok=True)
    (OUT / "assets" / "figures").mkdir(parents=True, exist_ok=True)

    print("AI Academy — building site")
    print(f"  source : {COURSE.relative_to(ROOT)}")
    print(f"  output : {OUT.relative_to(ROOT)}")

    docs = discover()
    routes = build_route_map(docs)
    weeks = parse_weeks()
    nav_json = build_nav_payload(weeks, docs)

    # Two keys from one salt. Student content is encrypted under the student key;
    # teacher content under the teacher key. The student key is ALSO stored wrapped
    # under the teacher key, so the teacher passcode opens everything in one unlock.
    salt = os.urandom(16)
    key_student = derive_key(args.student_pass, salt)
    key_teacher = derive_key(args.teacher_pass, salt)
    verifier_plain = "ai-academy-ok"

    # figures
    figs: list[str] = []
    for svg in sorted((COURSE / "figures").glob("*.svg")):
        shutil.copy2(svg, OUT / "assets" / "figures" / svg.name)
        if not svg.name.startswith("_"):
            figs.append(svg.name)

    # assets
    src_assets = Path(__file__).resolve().parent / "assets_src"
    for name in ("app.css", "app.js"):
        shutil.copy2(src_assets / name, OUT / "assets" / name)
    (OUT / "assets" / "home.js").write_text(HOME_JS, encoding="utf-8")

    # documents — every content page is encrypted; tier decides under which key
    n_student = n_teacher = 0
    dead_links: list[str] = []
    for doc in docs:
        renderer = MarkdownRenderer(make_resolver(doc, routes))
        body = renderer.render(doc.src.read_text(encoding="utf-8"))
        doc.headings = renderer.headings
        for m in re.finditer(r'href="unavailable:([^"]+)"', body):
            dead_links.append(f"{doc.src.relative_to(ROOT)} -> {m.group(1)}")
        body = re.sub(r'href="unavailable:[^"]*"', 'href="#" class="dead" title="Not part of this site"', body)

        depth = doc.route.count("/")
        page = shell(doc=doc, depth=depth, nav_json=nav_json, body=body, encrypted=True)
        dest = OUT / doc.route
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page, encoding="utf-8")

        key = key_teacher if doc.mode == "teacher" else key_student
        (OUT / "assets" / "enc" / f'{doc.route.replace("/", "__")}.json').write_text(
            json.dumps(encrypt(key, body), separators=(",", ":")), encoding="utf-8")
        if doc.mode == "teacher":
            n_teacher += 1
        else:
            n_student += 1

    (OUT / "assets" / "enc" / "_meta.json").write_text(json.dumps({
        "salt": base64.b64encode(salt).decode(),
        "iterations": PBKDF2_ITERATIONS,
        "plain": verifier_plain,
        "verifyStudent": encrypt(key_student, verifier_plain),
        "verifyTeacher": encrypt(key_teacher, verifier_plain),
        # student key, wrapped under the teacher key
        "wrappedStudentKey": encrypt_bytes(key_teacher, key_student),
    }, separators=(",", ":")), encoding="utf-8")

    gal_page, gal_body = gallery_page(nav_json, figs)
    (OUT / "gallery.html").write_text(gal_page, encoding="utf-8")
    (OUT / "assets" / "enc" / "gallery.html.json").write_text(
        json.dumps(encrypt(key_student, gal_body), separators=(",", ":")), encoding="utf-8")

    (OUT / "index.html").write_text(
        home_page(weeks, docs, nav_json,
                  {"weeks": len(weeks), "figures": len(figs), "pages": len(docs) + 2}),
        encoding="utf-8")

    print(f"  pages  : {n_student} student-tier + {n_teacher} teacher-tier, all encrypted")
    print(f"           1 public page (index.html) + gallery")
    print(f"  figures: {len(figs)} SVGs copied")
    print(f"  crypto : AES-256-GCM, PBKDF2-SHA256 x{PBKDF2_ITERATIONS:,}, two keys + key wrapping")
    if dead_links:
        print(f"  ! {len(dead_links)} link(s) point outside the generated site:")
        for d in sorted(set(dead_links))[:12]:
            print(f"      {d}")
    print(f"\n  student passcode : {args.student_pass!r}")
    print(f"  teacher passcode : {args.teacher_pass!r}")
    print(f"  serve            : ./site-app/serve.sh")
    print("  then open        : http://localhost:8000/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


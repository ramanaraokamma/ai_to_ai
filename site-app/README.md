# 🖥️ AI Academy — the website

A local, self-contained website for the AI Academy 36-week courses — **Level 1 Explorer, Level 2
Builder and Level 3 Engineer** — with **two passcodes**: one for the student, one for the teacher.
Without a passcode you see the level picker and nothing else.

```
site-app/
├── build.py            the generator (Python 3, stdlib + cryptography)
├── serve.sh            build if needed, then serve on localhost
├── assets_src/         app.css · app.js  (edit these, not dist/)
└── dist/               generated output — safe to delete, rebuilt in seconds
```

---

## Run it

```bash
./site-app/serve.sh
# → http://localhost:8000/
```

| | Passcode | Opens |
|---|---|---|
| 🎒 **Student** | `student1234` | per level: 36 chapters · 36 workbooks · projects · glossary · reference modules · figure gallery |
| 🧑‍🏫 **Teacher** | `teacher1234` | everything above **plus** 36 lesson scripts · orientation · 4 term tests · marking guide · exit exam · style guide |
| 🔓 **No passcode** | — | the root level picker only |

One passcode pair covers **all three levels** — unlock once, browse any year.

### Routes

```
/                     level picker (public)
/l1/index.html        Level 1 Explorer — year plan, passcode gate
/l2/index.html        Level 2 Builder  — year plan, passcode gate
/l3/index.html        Level 3 Engineer — year plan, passcode gate
/l3/chapter/week-07.html   /l3/workbook/week-07.html   /l3/lesson/week-07.html
/l3/tests/term-2.html      /l3/projects/ideas.html     /l3/gallery.html
```

A level chip in the header switches years from any page. Add a level by appending to `ALL_LEVELS` in
`build.py`.

**A level ships only when it is finished.** `_level_is_complete()` requires the README plus all 36
weeks in all three books; otherwise the build prints exactly what is short and the level is listed as
"not built yet" on the root page:

```
skipping L4 Innovator: incomplete: teacher-guide 36 week(s) short, ...
```

A half-built level on the site reads as broken links rather than as work in progress, which is why
the gate is strict — and why Level 3 appeared automatically, with no code change, the moment its last
workbook landed.

The server binds to `127.0.0.1` only — **nothing is published**, nothing leaves your machine, and no
internet is needed after the build.

```bash
./site-app/serve.sh 9000        # a different port
./site-app/serve.sh --rebuild   # regenerate first (after editing course markdown)
```

---

## What "locked" means here

**Only the root `index.html` is readable without a passcode.** Every other page — 399 of them plus
three galleries and three level homes — ships as a ~20 KB shell containing navigation and a passcode
form, with an **empty content element**. The words live in a separate encrypted file.

On each level's home page:

- The year plan, week titles, big ideas and type badges **are** public. That's the syllabus; it's
  also in the printed plan. Nothing worth hiding.
- Every link to a chapter, workbook or lesson script renders with `aria-disabled`, greyed out,
  marked 🔒 and non-tabbable. Clicking one scrolls you to the passcode box instead of navigating.
- After unlocking, links go live, a role chip (`🎒 Student` / `🧑‍🏫 Teacher`) appears in the header,
  and a sign-out button (`⎋`) clears the session.
- A student who unlocks has teacher links **removed entirely**, not merely disabled.

If a student lands on a teacher URL directly, the page loads but cannot be decrypted with their key,
and the lock card says so: *"You're signed in as a student. This page needs the teacher passcode."*

---

## 🔒 How the two-tier gate actually works

Real encryption, not a hidden `<div>`.

```
        passcode                    key                    what it opens
   ────────────────────      ─────────────────    ──────────────────────────────
   "student1234"  ──PBKDF2──►  K_student  ────────►  267 student-tier pages (all levels)
   "teacher1234"  ──PBKDF2──►  K_teacher  ────────►  132 teacher-tier pages (all levels)
                                   │
                                   └── decrypts ──►  wrapped K_student
                                                     (one unlock opens both tiers)
```

1. Both passcodes go through **PBKDF2-HMAC-SHA256, 250,000 iterations** with a shared random 16-byte
   salt, producing two independent 256-bit keys.
2. Each page is rendered to HTML and encrypted with **AES-256-GCM** under its tier's key. Only
   ciphertext lands in `dist/assets/enc/*.json`.
3. `K_student` is *also* stored encrypted under `K_teacher` (**key wrapping**), so the teacher
   passcode unwraps the student key and opens everything in one unlock — while the student passcode
   cannot go the other way.
4. In the browser, **WebCrypto** repeats the KDF and decrypts client-side. Keys are held in
   `sessionStorage`: one unlock covers the session, and it's gone when the tab closes.

### Verified, not assumed

| Test | Result |
|---|---|
| `student1234` on an L1/L2/L3 chapter | opens ✅ |
| `student1234` on an L1/L2/L3 lesson script | blocked, `InvalidTag` ✅ |
| `student1234` on an L2 or L3 term test | blocked, `InvalidTag` ✅ |
| `teacher1234` on lesson scripts and term tests, all three levels | opens ✅ |
| `teacher1234` → unwrapped student key | matches the derived student key bit-for-bit ✅ |
| `student1234` → unwrap the wrapper | blocked, `InvalidTag` ✅ |
| wrong passcode on anything | blocked, `InvalidTag` ✅ |
| Distinctive sentences from both tiers of every level, searched across all generated text files | **0 found in plaintext** ✅ |
| Un-authenticated fetch of any content page | content element is empty (`0` bytes of body) ✅ |
| All 17 routes over HTTP | 200 ✅ |

AES-GCM *authenticates*, so a wrong key fails loudly rather than returning garbage that looks like
text.

### Set your own passcodes

`student1234` / `teacher1234` are hardcoded defaults for convenience. **Change them before this
matters.**

```bash
AIA_STUDENT_PASS="..." AIA_TEACHER_PASS="..." python3 site-app/build.py --clean
# or
python3 site-app/build.py --clean --student-pass "..." --teacher-pass "..."
```

The build refuses to run if the two passcodes are identical. Neither passcode is written to disk —
only the random salt, two small encrypted verifier blobs, and the wrapped student key. Changing a
passcode requires a rebuild.

### What this does and doesn't protect

| | |
|---|---|
| ✅ Stops a student reading lesson scripts or answer keys | The bytes are unreadable without the teacher passcode |
| ✅ Stops "view source" | There is no plaintext in the source to view |
| ✅ Stops a passer-by reading anything | Only the root level picker renders without a passcode |
| ✅ Survives copying the `dist/` folder | The encryption travels with the files |
| ⚠️ `student1234` / `teacher1234` are weak | A dictionary word plus four digits. Fine for a kitchen table, not for the internet |
| ⚠️ Does not stop someone reading the markdown | The source `.md` files are unencrypted on your disk. The gate protects the *website*, not the repo |

Week titles and big ideas are public by design. Only the prose, activities, lesson scripts, answers
and tests are gated.

---

## What gets built

| | Level 1 | Level 2 | Level 3 | Total |
|---|--:|--:|--:|--:|
| Weeks | 36 | 36 | 36 | 108 |
| Pages | 133 | 133 | 133 | 399 |
| SVG figures | 450 | 358 | 329 | 1,137 |

| | |
|---|---|
| Public pages | 1 (the root level picker) |
| Student-tier encrypted pages | 267 + 3 galleries |
| Teacher-tier encrypted pages | 132 |
| Total files / size | 1,952 / ~67 MB |
| Broken internal references | **0** (10,960 checked, including inside decrypted bodies) |
| Build time | ~3 s |

**Features:** sidebar tree grouped by term that reacts to role and mode · `/` focuses search · live
nav filter · per-page table of contents with scroll-spy · prev/next pager that follows the current
mode · per-week progress checkboxes with per-term bars (localStorage) · role chip and sign-out ·
light/dark theme with no flash-on-load · figure gallery with lazy loading · print stylesheet that
drops the chrome and auto-expands `<details>` so answer keys print · keyboard navigable with visible
focus rings · double-click a code block to copy it.

### Reading layout

The prose column is capped at a **68-character measure** (`--measure`), because the original 62rem
card ran body text to ~110 characters a line against a 60–75 target — the worst thing about the old
layout for a chapter a child reads for twenty minutes.

Content that is *not* prose breaks out of that measure to the full card width: tables, code blocks,
figures and the `<details>` answer keys. A nine-column marking table or an 800×400 diagram is not
prose and should not be squeezed to a paragraph's width.

| Variable | Value | What it controls |
|---|---|---|
| `--measure` | `68ch` | Line length for paragraphs, lists, blockquotes, h3–h6 |
| `--maxw` | `76ch` | The card itself — measure plus padding |
| `--doc-pad` | `clamp(1.1rem, 3vw, 2.2rem)` | Card padding, and the breakout distance |

Other layout decisions worth knowing:

- **The reading column is centred** in whatever space the middle column gets, so a wide screen doesn't
  leave dead space beside the card.
- **The TOC appears at ≥1260px**, not 1180 — three columns genuinely need `282 + 646 + 210` plus gaps
  and padding. Below that it hides and the card still fits a 1024px laptop.
- **Table headers are not sticky.** `.table-wrap` must scroll horizontally, and a scroll container
  kills page-level `position: sticky` — the old rule was dead CSS. Zebra striping does the
  row-tracking job instead.
- **Figures are capped at `62vh`** so one tall diagram cannot own the whole screen.
- **The mobile nav drawer has a scrim** and dismisses on outside tap, `Esc`, or tapping any nav link.
- Heading anchor links appear on **keyboard focus**, not hover only.

---

## Editing

- **Course content** → edit the markdown in `levels/level-1-explorer/36-week-course/`, then
  `./site-app/serve.sh --rebuild`. The site is a pure function of the markdown.
- **Design** → `assets_src/app.css`. The palette mirrors `figures/STYLE.md` so the artwork and the
  interface read as one system.
- **Behaviour** → `assets_src/app.js` (per-page) and the `HOME_JS` string in `build.py` (home page).
- **Never edit `dist/`** — it is overwritten on every build.

`build.py` contains a small markdown renderer (~250 lines) covering exactly the dialect this course
uses: ATX headings with anchors, pipe tables with alignment, fenced code, blockquotes, nested lists,
images with italic captions, inline code/bold/italic/links, and passthrough for the `<details>`
answer keys. It is deliberately not a general-purpose markdown library.

---

## Publishing later

Everything is static, so `dist/` can be dropped on any host (GitHub Pages, Netlify, S3) with no code
changes. Two things to settle first:

1. **Use strong passcodes.** The encryption holds on a public host — that's the point of doing it at
   build time — but PBKDF2 at 250k iterations is brute-forceable for a passcode like `student1234`.
2. **Publish `dist/` only, never `levels/`.** The markdown source is unencrypted.

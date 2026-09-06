# 🖥️ AI Academy — the website

A local, self-contained website for the Level 1 Explorer 36-week course, with **two passcodes**:
one for the student, one for the teacher. Without a passcode you see the home page and nothing else.

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
| 🎒 **Student** | `student1234` | 36 chapters · 36 workbooks · projects · glossary · reference modules · figure gallery |
| 🧑‍🏫 **Teacher** | `teacher1234` | everything above **plus** 36 lesson scripts · orientation · 4 term tests · marking guide · exit exam · style guide |
| 🔓 **No passcode** | — | the home page only |

The server binds to `127.0.0.1` only — **nothing is published**, nothing leaves your machine, and no
internet is needed after the build.

```bash
./site-app/serve.sh 9000        # a different port
./site-app/serve.sh --rebuild   # regenerate first (after editing course markdown)
```

---

## What "locked" means here

**Only `index.html` is readable without a passcode.** Every other page — 133 of them plus the
gallery — ships as a ~19 KB shell containing navigation and a passcode form, with an **empty content
element**. The words live in a separate encrypted file.

On the home page:

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
   "student1234"  ──PBKDF2──►  K_student  ────────►  89 student-tier pages
   "teacher1234"  ──PBKDF2──►  K_teacher  ────────►  44 teacher-tier pages
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
| `student1234` on a chapter | opens, 40,866 bytes ✅ |
| `student1234` on a lesson script | blocked, `InvalidTag` ✅ |
| `student1234` on a term test | blocked, `InvalidTag` ✅ |
| `teacher1234` on lesson script / term test | opens, 84,708 / 51,775 bytes ✅ |
| `teacher1234` → unwrapped student key | matches the derived student key bit-for-bit ✅ |
| `student1234` → unwrap the wrapper | blocked, `InvalidTag` ✅ |
| wrong passcode on anything | blocked, `InvalidTag` ✅ |
| 24 distinctive sentences from both tiers, searched across all 273 generated text files | **0 found in plaintext** ✅ |
| Un-authenticated fetch of any content page | content element is empty (`0` bytes of body) ✅ |

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
| ✅ Stops a passer-by reading anything | Only the home page renders without a passcode |
| ✅ Survives copying the `dist/` folder | The encryption travels with the files |
| ⚠️ `student1234` / `teacher1234` are weak | A dictionary word plus four digits. Fine for a kitchen table, not for the internet |
| ⚠️ Does not stop someone reading the markdown | The source `.md` files are unencrypted on your disk. The gate protects the *website*, not the repo |

Week titles and big ideas are public by design. Only the prose, activities, lesson scripts, answers
and tests are gated.

---

## What gets built

| | |
|---|---|
| Public pages | 1 (`index.html`) |
| Student-tier encrypted pages | 89 + gallery |
| Teacher-tier encrypted pages | 44 |
| SVG figures | 450 |
| Total files / size | ~636 / ~16 MB |
| Broken internal references | **0** (2,487 checked) |

**Features:** sidebar tree grouped by term that reacts to role and mode · `/` focuses search · live
nav filter · per-page table of contents with scroll-spy · prev/next pager that follows the current
mode · per-week progress checkboxes with per-term bars (localStorage) · role chip and sign-out ·
light/dark theme with no flash-on-load · figure gallery with lazy loading · print stylesheet that
drops the chrome and auto-expands `<details>` so answer keys print · keyboard navigable with visible
focus rings · double-click a code block to copy it.

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

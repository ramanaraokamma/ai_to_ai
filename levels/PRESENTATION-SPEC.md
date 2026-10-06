# Presentation spec — the polish pass (all four levels)

This is the binding brief for the "best presentation" pass over every weekly file (`student-guide/`,
`teacher-guide/`, `workbook/` × 36 weeks × 4 levels). It is a **content-safe** polish: it changes how a
file *reads*, never what it *says*.

## 0. The invariants (a polish that breaks one of these is reverted)

1. **Every fenced code block is byte-identical** before and after, in the same order. That includes
   every pasted output (` ```text `), traceback, table of numbers and ASCII diagram. Prose *around* a
   block may change; the block may not. (Checked mechanically by `levels/polish_check.py`.)
2. **Figure embeds, links and file names** are unchanged (`![…](../figures/…)`, nav lines, `[…](week-NN.md)`).
   Alt text and italic captions are not edited.
3. **No number appears or disappears from the prose** (counts, percentages, timings, marks, losses).
   If a sentence must be reworded, its numbers survive exactly. Timings in the lesson plan still sum to
   the stated duration.
4. **No new concept, construct, term or claim.** Nothing used earlier than its ladder week; nothing
   defined later than its first use. Polish may *move a definition earlier*, never introduce a term early.
5. **Teacher-only content stays teacher-only**; student files never gain answers, keys or links to
   teacher files. Deliberately broken examples stay broken and stay marked deliberate.
6. **Stand-ins stay labelled** ("stand-in, not a model"); quoted-not-measured boxes stay labelled.
7. **The level's dialect is kept**: its emoji section headers, section order and voice. L1–L3 share a
   skeleton (Start Here → Big Idea → … → Remember This → New Words → Homework); L4 student guides are
   topic-driven and L4 workbooks use `Page N.K — title (minutes)`. Do not force one onto the other.
8. **No answer leaks and no new claims**: a polisher adds no sentence that asserts something the file did not
   already assert, and no sentence that gives away an exercise answer, a hint, or an expected mistake.
9. Headings may be *reworded for clarity* but each file keeps the same set of H2 sections in the same
   order (sections may be added only where a required element below is missing, and only with text
   already present elsewhere in the file or drawn from the lesson it describes).

## 1. What "best presentation" means — the standard

**Every section opens by saying what it is for.** The first one or two lines under each H2 state the
purpose in plain words ("In this section you will…" / "You need this because…"). No section opens
cold with a code block or a wall of text.

**Scannable.** Paragraphs ≤ 4 sentences (≤ 3 for ages 11–13). Any run of 3+ parallel items is a list;
any comparison across 2+ dimensions is a table; any ordered procedure is a numbered list with one
action per step. Bold is for the term at its *first definition* and for one key takeaway per section,
not for emphasis sprinkled through prose. No paragraph longer than 8 rendered lines.

**One consistent callout vocabulary** (keep the level's existing emoji if it has one; otherwise use):
`> **💡 Why:**` the reason behind a step · `> **⚠️ Watch out:**` the common trap · `> **🐞 If you see this error:**`
message + cause + fix · `> **📌 Remember:**` the one thing to keep · `> **✅ Done looks like:**` an observable
check the learner can make. Callouts are short (≤ 4 lines) and never nest.

**Every code block is introduced and followed.** One line before says what the block does and what to
type/run. After a block that produces output, add a line only if it is *neutral* ("Compare this with your
prediction", "Find the row for seed 2"). **Never add a line, in any student-facing file or workbook, that states
or hints at what the output shows or what the exercise asks the learner to discover** ("Look at how X
climbs", "notice that the gap is small"): if the text does not already state the finding at that spot, the
polisher must not. In teacher guides a pointer is fine but must be checked against the printed output. Section
purpose lines follow the same rule: they say what the page is *for* ("works through Adam's first step"), never
what it will *prove*. Where a block is long, a sentence names its parts.

**Clear openings and endings.** Student guides open with a hook and a short "By the end you can…" list
(2–4 items, observable verbs), and end with the key takeaways, the new words, and the homework with
its time estimate. Teacher guides open with the At a Glance table and objectives, and the minute-by-minute
plan uses a fixed micro-format per step: **(time) Title** → *Say this* / *Ask this* / *Expect* / *Watch for*.
Workbooks open with the warm-up, label each page `Page N.K — title (minutes)`, put the instruction in
one bold line before the task, leave visible writing space markers, and end with Answers under an
unmistakable divider.

**Reading level matches the learner.** L1 (age ~11): short sentences, concrete nouns, no jargon without a
picture or example. L2 (~12): plain, one new idea per paragraph. L3 (~14): precise, numerical before symbolic.
L4 (~15–16): precise and compact, but each new symbol, function or metric still named and glossed at first use.
Replace filler ("basically", "simply", "just") and hedges that carry no information; never add exclamation
or false enthusiasm.

**Consistency inside a file and across the three books of a week**: the same term for the same thing,
the same filename, the same variable names, the same order of ideas. If the student guide calls it
"the gate", the workbook and teacher guide do too.

## 2. Mechanical hygiene (must be clean after the pass)

- Exactly one `#` title; headings go `##` → `###` → `####` with no skipped level.
- Fenced blocks balanced and all tagged with a language (`python`, `text`, `bash`, `markdown`, `svg`).
- No trailing spaces, no tab indentation in prose, no double blank lines, one blank line around blocks,
  tables, callouts and headings; lists use `-` consistently.
- The nav line at the top and the horizontal rules follow the level's existing pattern.
- Smart typography consistent within the file (don't mix `--`, `—`, `–` for the same purpose).

## 3. What the polisher reports

For each file: a 1–3 line summary of what changed (counts: sections given a purpose line, paragraphs
split, lists/tables introduced, callouts normalised), anything that *could not* be improved without
touching an invariant, and any **correctness or consistency problem noticed in passing** (reported, not
fixed, unless it is an unambiguous typo). The polisher runs `python3 levels/polish_check.py <file>`
before finishing and must leave it printing `OK`.
